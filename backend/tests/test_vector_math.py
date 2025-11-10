import math

from liedetect.services.vector_math import average_vectors, cosine_similarity, final_lie_score, fuse_lie_scores, llm_alignment_score


def test_average_vectors():
    vectors = [[0.2] * 8, [0.4] * 8]
    result = average_vectors(vectors)
    assert result == [0.3] * 8


def test_cosine_similarity_identical():
    vec = [0.1] * 8
    assert math.isclose(cosine_similarity(vec, vec), 1.0)


def test_fuse_lie_scores_defaults():
    score = fuse_lie_scores(0.5, 0.25, 0.75)
    assert math.isclose(score, 0.5, rel_tol=1e-4)


def test_final_lie_score_balances_alignment():
    score = final_lie_score(0.6, 0.2)
    assert math.isclose(score, 0.7, rel_tol=1e-3)


def test_llm_alignment_score_zero():
    vector = [0.0] * 8
    llm_vector = {emotion: 0.1 for emotion in ['angry','calm','disgust','fearful','happy','neutral','sad','surprised']}
    assert llm_alignment_score(vector, llm_vector) == 0.0
