import pytest
from app.services.ocean_scorer import calculate_ocean_scores

def test_neutral_answers():
    answers = {i: 3 for i in range(1, 45)}
    scores = calculate_ocean_scores(answers)
    assert len(scores) == 5
    for score in scores.values():
        assert score == 0.5

def test_extreme_answers():
    answers = {i: 5 for i in range(1, 45)}
    scores = calculate_ocean_scores(answers)
    assert len(scores) == 5
    if "E" in scores:
        assert scores["E"] == 0.625

def test_invalid_input():
    answers = {i: 3 for i in range(1, 45)}
    answers[1] = 6  # invalid value
    with pytest.raises(ValueError):
        calculate_ocean_scores(answers)

def test_44_items_required():
    answers = {i: 3 for i in range(1, 40)} # missing 5 items
    with pytest.raises(ValueError):
        calculate_ocean_scores(answers)
