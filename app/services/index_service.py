from collections import defaultdict
from typing import Dict, Set, List, Any
from rapidfuzz import utils

def build_index(products: List[Any], fields: List[str] = None) -> Dict[str, Set[str]]:
    """
    Cria índice invertido baseado nos campos definidos no modelo Search.
    """
    index: Dict[str, Set[str]] = defaultdict(set)
    # Se não houver campos definidos, o padrão é o nome
    search_fields = fields if fields else ["name"]

    for p in products:
        for field in search_fields:
            # Pega o valor do atributo (ex: p.name ou p.description)
            val = getattr(p, field, None)
            if not val or not isinstance(val, str):
                continue
                
            clean_text = utils.default_process(val)
            if not clean_text:
                continue
                
            words = clean_text.split()
            for word in words:
                index[word].add(p.id)
                # Indexa prefixos (mínimo 3 chars)
                for i in range(3, len(word) + 1):
                    index[word[:i]].add(p.id)
    return index