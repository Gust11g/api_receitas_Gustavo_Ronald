from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import table_registry
from settings import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
table_registry.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
