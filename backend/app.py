from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from liedetect import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5001, debug=True)
