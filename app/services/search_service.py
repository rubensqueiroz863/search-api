from typing import List, Dict, Set, Any
from rapidfuzz import process, fuzz, utils
from app.services.index_service import build_index
from app.services.ranking_service import rank

def apply_filters(products: List[Any], filters: Dict[str, Any]) -> List[Any]:
    """
    Filtros avançados:
    Ex:
    {
        "price_min": 1000,
        "price_max": 5000,
        "name_contains": "iphone",
        "subcategory": "Celulares"
    }
    """
    if not filters:
        return products

    filtered = []

    for p in products:
        match = True

        for key, value in filters.items():

            # 🔢 PRICE MIN
            if key == "price_min":
                if not hasattr(p, "price") or p.price < value:
                    match = False
                    break

            # 🔢 PRICE MAX
            elif key == "price_max":
                if not hasattr(p, "price") or p.price > value:
                    match = False
                    break

            # 🔍 NAME CONTAINS
            elif key == "name_contains":
                if value.lower() not in p.name.lower():
                    match = False
                    break

            # 🏷️ SUBCATEGORY
            elif key == "subcategory":
                if not p.subcategory or p.subcategory.name != value:
                    match = False
                    break

            # 🧩 FALLBACK (igualdade simples)
            else:
                if getattr(p, key, None) != value:
                    match = False
                    break

        if match:
            filtered.append(p)

    return filtered

def execute_search(products: List[Any], search_config: Any, index: Dict[str, Set[str]] = None):
    """
    Pipeline que utiliza a instância da model 'Search' para os parâmetros.
    """
    if not products or not search_config.query:
        return []

    # 1. Aplicar filtros brutos (JSON) antes de processar a busca textual
    if search_config.filters:
        products = apply_filters(products, search_config.filters)

    # 2. Construir índice baseado nos campos permitidos (Fields)
    if index is None:
        index = build_index(products, fields=search_config.fields)

    clean_query = utils.default_process(search_config.query)
    words = clean_query.split()
    ids: Set[str] = set()

    # 🔍 ETAPA 1: Match direto no índice
    for word in words:
        if word in index:
            ids.update(index[word])

    # 🧠 ETAPA 2: Fuzzy fallback (Só se 'fuzzy' estiver habilitado na model)
    if not ids and search_config.fuzzy:
        matches = process.extract(
            clean_query,
            index.keys(),
            scorer=fuzz.WRatio,
            processor=utils.default_process,
            score_cutoff=70, # Threshold interno para busca de chaves
            limit=5
        )
        for key, _, _ in matches:
            ids.update(index[key])

    if not ids:
        return []

    # 🔄 Recuperação e Ranking
    products_map = {p.id: p for p in products}
    candidates = [products_map[pid] for pid in ids if pid in products_map]
    
    # Converte min_score de string para int (se necessário)
    m_score = int(search_config.min_score) if search_config.min_score else 50

    return rank(
        candidates, 
        search_config.query, 
        min_score=m_score, 
        sort_by=search_config.sort_by
    )