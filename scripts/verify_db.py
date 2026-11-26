
import asyncio

from sqlalchemy import inspect

from src.knowly.db.init_db import init_db
from src.knowly.db.session import engine


async def main():

    await init_db()

    async with engine.connect() as connection:

        tables = await connection.run_sync(
            lambda conn: inspect(conn).get_table_names()
        )

    print("Database verification successful.")
    print("Tables created:")

    for table in tables:
        print(f"- {table}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
