"""Reglas exploratorias: sin fallback, inferencias profesionales desde N ni desempates arbitrarios.

Las seis asociaciones directas y dos búsquedas inversas se conservan. Estos tests
no constituyen una validación académica de la relación entre rasgos y profesiones.
"""
import pytest
from app.routers.reporte import get_career_areas
from app.schemas.reporte import CareerArea


@pytest.mark.parametrize('top1,top2,title', [
    ('O', 'C', 'Tecnología e Informática'),
    ('C', 'O', 'Ingeniería y Gestión de Procesos'),
    ('E', 'A', 'Comunicación y Relaciones Públicas'),
    ('A', 'E', 'Salud y Educación'),
    ('O', 'E', 'Artes y Diseño'),
    ('C', 'A', 'Administración y Contabilidad'),
    # Solo existe la combinación inversa; debe reutilizarse esa entrada.
    ('E', 'O', 'Artes y Diseño'),
    ('A', 'C', 'Administración y Contabilidad'),
])
def test_existing_and_reversed_combinations(top1, top2, title):
    scores = dict.fromkeys('NACEO', 0.1)
    scores.update({top1: 0.9, top2: 0.8})
    original = scores.copy()
    result = get_career_areas(scores)
    assert len(result) == 1 and isinstance(result[0], CareerArea)
    assert result[0].title == title
    assert result[0].carreras
    assert scores == original


@pytest.mark.parametrize('top1,top2', [
    ('O', 'A'), ('A', 'O'), ('C', 'E'), ('E', 'C'),
    ('N', 'O'), ('N', 'C'), ('N', 'E'), ('N', 'A'),
    ('O', 'N'), ('C', 'N'), ('E', 'N'), ('A', 'N'),
])
def test_uncovered_pairs_and_neuroticism_return_no_area(top1, top2):
    scores = dict.fromkeys('OCEAN', 0.1)
    scores.update({top1: 0.9, top2: 0.8})
    result = get_career_areas(scores)
    assert result == []


@pytest.mark.parametrize('scores', [{}, {'N': 1.0}, {'C': 1.0}])
def test_fewer_than_two_dimensions_returns_no_area(scores):
    assert get_career_areas(scores) == []


@pytest.mark.parametrize('scores', [
    {'O': 0.8, 'C': 0.8, 'N': 0.1},
    {'O': 0.9, 'C': 0.8, 'E': 0.8, 'A': 0.1, 'N': 0.1},
    dict.fromkeys('OCEAN', 0.5),
    {'N': 0.9, 'O': 0.9, 'C': 0.8, 'A': 0.2, 'E': 0.1},
])
def test_ambiguous_ties_return_neutral_regardless_of_json_order(scores):
    from itertools import permutations
    for items in permutations(scores.items()):
        assert get_career_areas(dict(items)) == []


def test_equal_lower_dimensions_do_not_invalidate_unambiguous_existing_rule():
    assert get_career_areas({'O': 0.9, 'C': 0.8, 'E': 0.1, 'A': 0.1, 'N': 0.1})[0].title == 'Tecnología e Informática'


def test_matrix_keeps_only_six_existing_pairs_and_describes_areas_without_suitability_claims():
    from app.routers.reporte import CAREER_MATRIX
    assert set(CAREER_MATRIX) == {('O', 'C'), ('C', 'O'), ('E', 'A'), ('A', 'E'), ('O', 'E'), ('C', 'A')}
    for area in CAREER_MATRIX.values():
        assert 'Referencia exploratoria' in area.desc
        assert 'no acredita afinidad ni aptitud profesional' in area.desc
        assert 'Ideal para' not in area.desc and 'Vocación de servicio' not in area.desc
