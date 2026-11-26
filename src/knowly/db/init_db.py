
from src.knowly.db.base import Base
from src.knowly.db.session import engine

# Import models so SQLAlchemy registers their tables
from src.knowly.db import models


async def init_db():
    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )
