from typing import List, Tuple
from rapidfuzz import fuzz, process, utils


def normalize(text: str) -> str:
    """Normaliza texto (lowercase, remove acentos, etc)."""
    return utils.default_process(text) or ""


def fuzzy_match(query: str, word: str, threshold: int = 80) -> bool:
    """Verifica se duas strings são similares acima de um threshold."""
    if not query or not word:
        return False

    score = fuzz.WRatio(
        query,
        word,
        processor=utils.default_process,
        score_cutoff=threshold
    )
    return score >= threshold


def find_best_matches(
    query: str,
    choices: List[str],
    threshold: int = 80,
    limit: int = 5
) -> List[Tuple[str, float]]:
    """Retorna melhores matches fuzzy."""
    if not query or not choices:
        return []

    return process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        processor=utils.default_process,
        score_cutoff=threshold,
        limit=limit
    )