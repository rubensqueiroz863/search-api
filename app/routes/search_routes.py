from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.repositories.product_repository import get_all_products
from app.database.connection import get_db
from app.models.product import Product
from app.models.user import User
from app.models.search import Search
from app.services.search_service import execute_search, apply_filters
from app.schemas.search_dto import SearchCreate, SearchResponse

router = APIRouter()

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# Importe sua model Search e o novo serviço
from app.models.search import Search
from app.services.search_service import execute_search 

@router.get("/search")
async def search_products(
    q: str,
    page: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),

    fuzzy: bool = True,
    sort_by: str = None,
    min_score: int = 50,

    price_min: int = Query(None),
    price_max: int = Query(None),
    subcategory: str = Query(None),
    name_contains: str = Query(None),

    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product).options(selectinload(Product.subcategory))
    )
    products = result.scalars().all()

    filters = {}

    if price_min is not None:
        filters["price_min"] = price_min

    if price_max is not None:
        filters["price_max"] = price_max

    if subcategory:
        filters["subcategory"] = subcategory

    if name_contains:
        filters["name_contains"] = name_contains

    # 3. Criar config
    search_config = Search(
        query=q,
        fuzzy=fuzzy,
        min_score=str(min_score),
        sort_by=sort_by,
        fields=["name"],
        filters=filters if filters else None
    )

    results = execute_search(products, search_config)

    total = len(results)
    start = page * limit
    end = start + limit
    paged_results = results[start:end]

    data = [
        {
            "id": str(p.id),
            "name": p.name,
            "price": p.price,
            "photo": p.photo,
            "subCategory": p.subcategory.name if p.subcategory else None
        }
        for p in paged_results
    ]

    return {
        "data": data,
        "hasMore": end < total,
        "total": total
    }

from datetime import datetime
from sqlalchemy.exc import IntegrityError

@router.post("/search", response_model=SearchResponse)
async def create_search(
    data: SearchCreate,
    session: AsyncSession = Depends(get_db)
):
    if not data.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if not data.email.strip():
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    result = await session.execute(
        select(User).where(User.email == data.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(
        select(Search).where(
            Search.user_id == user.id,
            Search.query == data.query
        )
    )
    search = result.scalar_one_or_none()

    if search:
        search.created_at = datetime.utcnow()
    else:
        search = Search(
            query=data.query,
            filters=data.filters,
            fields=data.fields,
            fuzzy=data.fuzzy,
            min_score=data.min_score,
            sort_by=data.sort_by,
            user_id=user.id,
            created_at=datetime.utcnow()
        )
        session.add(search)

    try:
        await session.commit()
        await session.refresh(search)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Error saving search")

    return SearchResponse(
        id=str(search.id),
        user_id=str(user.id)
    )