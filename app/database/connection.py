from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_DcIsxQ6q7Pir@ep-cold-cell-ac3a1cnd-pooler.sa-east-1.aws.neon.tech/neondb"

# engine async
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

# sessão async
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# base dos models
Base = declarative_base()

# dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session