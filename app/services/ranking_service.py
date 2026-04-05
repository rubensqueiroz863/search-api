from typing import List, Any
from rapidfuzz import fuzz, process, utils

def rank(products: List[Any], query: str, min_score: int = 50, sort_by: str = None):
    """
    Ordena produtos por relevância e aplica filtros de score mínimo.
    """
    if not products or not query:
        return []

    # Mapeia nome -> produto (usamos o nome para o cálculo de score textual principal)
    choices = {p.name: p for p in products}
    
    results = process.extract(
        query,
        choices.keys(),
        scorer=fuzz.WRatio,
        processor=utils.default_process,
        score_cutoff=min_score,
        limit=None
    )
    
    ranked_products = [choices[name] for name, score, _ in results]

    # Se houver um campo de ordenação específico (ex: "price", "created_at")
    if sort_by and ranked_products:
        # Nota: Isso sobrescreve a ordem de relevância do fuzzy
        ranked_products.sort(key=lambda x: getattr(x, sort_by, 0), reverse=True)

    return ranked_products