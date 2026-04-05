from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.product import Product

async def get_all_products(db: AsyncSession):
    """
    Retorna todos os produtos já com a subcategoria carregada
    para evitar lazy load em AsyncSession.
    """
    result = await db.execute(
        select(Product).options(selectinload(Product.subcategory))
    )
    return result.scalars().all()