"""Reglas exploratorias del MVP: seis pares O/C/E/A y descripciones por cuartil."""
from itertools import permutations

import pytest

from app.routers.reporte import CAREER_MATRIX, get_career_areas, get_dimension_interpretation
from app.schemas.reporte import CareerArea


@pytest.mark.parametrize('top1,top2,title', [
    ('O', 'C', 'Tecnología, Ciencias Básicas y Agropecuaria'),
    ('C', 'O', 'Tecnología, Ciencias Básicas y Agropecuaria'),
    ('O', 'E', 'Arte, Arquitectura y Humanidades (Comunicaciones)'),
    ('E', 'O', 'Arte, Arquitectura y Humanidades (Comunicaciones)'),
    ('O', 'A', 'Ciencias Sociales y Humanidades'),
    ('A', 'O', 'Ciencias Sociales y Humanidades'),
    ('C', 'E', 'Administración, Comercio y Derecho'),
    ('E', 'C', 'Administración, Comercio y Derecho'),
    ('C', 'A', 'Salud (Gestión y Cuidados) y Agropecuaria'),
    ('A', 'C', 'Salud (Gestión y Cuidados) y Agropecuaria'),
    ('E', 'A', 'Educación y Salud (Atención Comunitaria)'),
    ('A', 'E', 'Educación y Salud (Atención Comunitaria)'),
])
def test_all_pairs_and_reversed_pairs(top1, top2, title):
    scores = dict.fromkeys('NACEO', 0.1)
    scores.update({top1: 0.9, top2: 0.8})
    original = scores.copy()
    result = get_career_areas(scores)
    assert len(result) == 1 and isinstance(result[0], CareerArea)
    assert result[0].title == title
    assert result[0].carreras
    assert scores == original


@pytest.mark.parametrize('scores', [{}, {'N': 1.0}, {'C': 1.0}])
def test_fewer_than_two_non_n_dimensions_returns_no_area(scores):
    assert get_career_areas(scores) == []


def test_n_dominant_does_not_displace_ocea_pair():
    scores = {'N': 1.0, 'A': 0.9, 'O': 0.8, 'C': 0.7, 'E': 0.6}
    assert get_career_areas(scores)[0].title == 'Ciencias Sociales y Humanidades'


def test_ties_follow_input_order_as_approved_for_mvp():
    scores = dict.fromkeys('OCEAN', 0.5)
    assert get_career_areas(scores)[0].title == 'Tecnología, Ciencias Básicas y Agropecuaria'
    reordered = {'A': 0.5, 'E': 0.5, 'C': 0.5, 'O': 0.5, 'N': 0.5}
    assert get_career_areas(reordered)[0].title == 'Educación y Salud (Atención Comunitaria)'


def test_lower_ties_do_not_change_dominant_pair():
    scores = {'O': 0.9, 'C': 0.8, 'E': 0.1, 'A': 0.1, 'N': 0.1}
    for items in permutations(scores.items()):
        assert get_career_areas(dict(items))[0].title == 'Tecnología, Ciencias Básicas y Agropecuaria'


def test_matrix_covers_exactly_six_unordered_pairs():
    assert set(CAREER_MATRIX) == {
        ('O', 'C'), ('O', 'E'), ('O', 'A'),
        ('C', 'E'), ('C', 'A'), ('E', 'A'),
    }
    for area in CAREER_MATRIX.values():
        assert 'Referencia exploratoria' in area.desc
        assert 'no acredita aptitud profesional ni predice desempeño' in area.desc


@pytest.mark.parametrize('letter', list('OCEAN'))
@pytest.mark.parametrize('first,last', [(0, 25), (26, 50), (51, 75), (76, 100)])
def test_interpretation_quartile_boundaries(letter, first, last):
    assert get_dimension_interpretation(letter, first) == get_dimension_interpretation(letter, last)
    assert get_dimension_interpretation(letter, first)
    if first:
        assert get_dimension_interpretation(letter, first - 1) != get_dimension_interpretation(letter, first)


def test_interpretation_unknown_or_out_of_range_is_empty():
    assert get_dimension_interpretation('X', 50) == ''
    assert get_dimension_interpretation('O', -1) == ''
    assert get_dimension_interpretation('O', 101) == ''
