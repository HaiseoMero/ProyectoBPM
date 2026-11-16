import pytest
from app.services.ocean_scorer import (
    AREAS_CHILE,
    calculate_ocean_scores,
    calcular_combinacion_id,
    calcular_porcentajes_bfi44,
    decodificar_combinacion_id,
    evaluar_perfil_vocacional,
    obtener_division,
)

def test_neutral_answers():
    answers = {i: 3 for i in range(1, 45)}
    scores = calculate_ocean_scores(answers)
    assert len(scores) == 5
    for score in scores.values():
        assert score == 0.5

    pcts = calcular_porcentajes_bfi44(answers)
    assert pcts == {"O": 50.0, "C": 50.0, "E": 50.0, "A": 50.0, "N": 50.0}

def test_extreme_answers():
    answers = {i: 5 for i in range(1, 45)}
    scores = calculate_ocean_scores(answers)
    assert len(scores) == 5
    if "E" in scores:
        assert scores["E"] == 0.625

    pcts = calcular_porcentajes_bfi44(answers)
    assert pcts["E"] == 62.5

def test_invalid_input():
    answers = {i: 3 for i in range(1, 45)}
    answers[1] = 6  # invalid value
    with pytest.raises(ValueError):
        calculate_ocean_scores(answers)
    with pytest.raises(ValueError):
        calcular_porcentajes_bfi44(answers)

def test_44_items_required():
    answers = {i: 3 for i in range(1, 40)}  # missing 5 items
    with pytest.raises(ValueError):
        calculate_ocean_scores(answers)
    with pytest.raises(ValueError):
        calcular_porcentajes_bfi44(answers)


def test_base4_bijection_all_1024_combinations():
    seen_ids = set()
    for cid in range(1, 1025):
        decoded = decodificar_combinacion_id(cid)
        assert set(decoded.keys()) == {"O", "C", "E", "A", "N"}
        assert all(0 <= v <= 3 for v in decoded.values())
        re_encoded = calcular_combinacion_id(decoded)
        assert re_encoded == cid
        seen_ids.add(re_encoded)
    assert len(seen_ids) == 1024


def test_evaluar_perfil_vocacional_12_areas_chile():
    assert len(AREAS_CHILE) == 12
    # Perfil idéntico al ideal de Informática, Datos y TI (área 1)
    ideal_ti = AREAS_CHILE[0]["ideal"]
    res = evaluar_perfil_vocacional(ideal_ti)
    assert res["total_posibilidades"] == 1024
    assert 1 <= res["combinacion_id"] <= 1024
    assert len(res["top_recomendaciones"]) == 3
    assert len(res["ranking_completo"]) == 12
    assert res["top_recomendaciones"][0]["slug"] == "informatica_datos_ti"
    assert res["top_recomendaciones"][0]["afinidad_porcentaje"] == 100.0
    assert obtener_division(0.0) == 0
    assert obtener_division(24.99) == 0
    assert obtener_division(25.0) == 1
    assert obtener_division(50.0) == 2
    assert obtener_division(75.0) == 3
    assert obtener_division(100.0) == 3
