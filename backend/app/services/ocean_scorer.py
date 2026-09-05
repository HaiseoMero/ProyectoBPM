"""Algoritmo de scoring del Big Five Inventory (BFI-44).

Referencia: John, O. P., & Srivastava, S. (1999).
The Big Five trait taxonomy.
"""

REVERSE_ITEMS: set[int] = {2, 6, 8, 9, 12, 18, 21, 23, 24, 27, 31, 34, 35, 37, 41, 43}

DIMENSION_ITEMS: dict[str, list[int]] = {
    "O": [5, 10, 15, 20, 25, 30, 35, 40, 41, 44],  # Openness - 10 items
    "C": [3, 8, 13, 18, 23, 28, 33, 38, 43],        # Conscientiousness - 9 items
    "E": [1, 6, 11, 16, 21, 26, 31, 36],             # Extraversion - 8 items
    "A": [2, 7, 12, 17, 22, 27, 32, 37, 42],         # Agreeableness - 9 items
    "N": [4, 9, 14, 19, 24, 29, 34, 39],             # Neuroticism - 8 items
}

DIMENSION_NAMES: dict[str, str] = {
    "O": "Apertura a la Experiencia",
    "C": "Responsabilidad (Conciencia)",
    "E": "Extraversión",
    "A": "Amabilidad",
    "N": "Neuroticismo (Estabilidad Emocional)",
}


def calculate_ocean_scores(answers: dict[int, int]) -> dict[str, float]:
    """Calculate normalized OCEAN scores from BFI-44 answers.
    
    Args:
        answers: Mapping of question_id (1-44) to Likert value (1-5).
        
    Returns:
        Dict with dimension letters as keys and normalized scores (0.0-1.0) as values.
        
    Raises:
        ValueError: If any question_id or Likert value is out of range,
                    or if not all 44 items are provided.
    """
    if len(answers) != 44:
        raise ValueError(f"Se requieren exactamente 44 respuestas, se recibieron {len(answers)}")
    
    for qid, val in answers.items():
        if not (1 <= qid <= 44):
            raise ValueError(f"ID de pregunta fuera de rango: {qid}")
        if not (1 <= val <= 5):
            raise ValueError(f"Valor Likert fuera de rango para pregunta {qid}: {val}")
    
    # Apply reverse scoring
    adjusted: dict[int, int] = {}
    for qid, val in answers.items():
        adjusted[qid] = (6 - val) if qid in REVERSE_ITEMS else val
    
    # Calculate mean score per dimension, normalized to 0-1
    scores: dict[str, float] = {}
    for dim, items in DIMENSION_ITEMS.items():
        vals = [adjusted[i] for i in items]
        raw_mean = sum(vals) / len(vals)  # 1.0 - 5.0
        scores[dim] = round((raw_mean - 1) / 4, 4)  # Normalize to 0.0 - 1.0
    
    return scores


def get_dominant_dimensions(scores: dict[str, float], top_n: int = 2) -> list[str]:
    """Return the top N dominant dimension letters, sorted by score descending."""
    return sorted(scores, key=lambda d: scores[d], reverse=True)[:top_n]
