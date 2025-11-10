from __future__ import annotations

import argparse
import tarfile
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from .config import config


def package_model(checkpoint: Path, output: Path) -> Path:
    if not checkpoint.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, 'w:gz') as tar:
        tar.add(checkpoint, arcname='model.pt')
        tar.add(Path(__file__).parent / 'serving' / 'inference.py', arcname='code/inference.py')
    return output


def ensure_bucket(session: boto3.Session, bucket: str, region: Optional[str]) -> None:
    s3 = session.client('s3')
    try:
        if region and region != 'us-east-1':
            s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})
        else:
            s3.create_bucket(Bucket=bucket)
    except ClientError as exc:
        error_code = exc.response['Error'].get('Code')
        if error_code not in {'BucketAlreadyOwnedByYou', 'BucketAlreadyExists'}:
            raise


def deploy_model(
    model_artifact: Path,
    role_arn: str,
    endpoint_name: str,
    image_uri: str,
    instance_type: str = 'ml.m5.large',
    region: Optional[str] = None
) -> None:
    session = boto3.Session(region_name=region)
    actual_region = session.region_name or 'us-east-1'
    bucket = f"{actual_region}-liedetect-models"
    ensure_bucket(session, bucket, actual_region)

    s3 = session.client('s3')
    sagemaker = session.client('sagemaker')

    key = f"audio_lie/{model_artifact.name}"
    s3.upload_file(str(model_artifact), bucket, key)
    model_data = f"s3://{bucket}/{key}"

    model_name = f"{endpoint_name}-model"
    sagemaker.create_model(
        ModelName=model_name,
        PrimaryContainer={
            'Image': image_uri,
            'ModelDataUrl': model_data
        },
        ExecutionRoleArn=role_arn
    )

    config_name = f"{endpoint_name}-config"
    sagemaker.create_endpoint_config(
        EndpointConfigName=config_name,
        ProductionVariants=[
            {
                'VariantName': 'AllTraffic',
                'ModelName': model_name,
                'InstanceType': instance_type,
                'InitialInstanceCount': 1
            }
        ]
    )

    sagemaker.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=config_name
    )
    print(f"Deployment triggered for endpoint {endpoint_name}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Package and deploy AudioLie model to SageMaker')
    parser.add_argument('--checkpoint', type=Path, default=config.processed_dir / 'audio_emotion_net.pt')
    parser.add_argument('--artifact', type=Path, default=Path('artifacts/audio_lie_model.tar.gz'))
    parser.add_argument('--role-arn', required=True)
    parser.add_argument('--endpoint-name', required=True)
    parser.add_argument('--image-uri', required=True, help='SageMaker PyTorch inference image URI')
    parser.add_argument('--instance-type', default='ml.m5.large')
    parser.add_argument('--region', default=None)

    args = parser.parse_args()
    artifact_path = package_model(args.checkpoint, args.artifact)
    deploy_model(
        model_artifact=artifact_path,
        role_arn=args.role_arn,
        endpoint_name=args.endpoint_name,
        image_uri=args.image_uri,
        instance_type=args.instance_type,
        region=args.region
    )
