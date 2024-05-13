import os
from gino_starlette import Gino
from gino import Gino as BaseGino


DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}"


class PostgresBaseRepository():

    def __init__(self):
        if os.environ['CONSUMER']:
            self.db = BaseGino()
        else:
            if not self.db:
                self.db = Gino(dsn=DATABASE_URL)

    async def connect(self):
        if os.environ['CONSUMER']:
            await self.db.set_bind(DATABASE_URL)


postgres_base_repo = PostgresBaseRepository()
