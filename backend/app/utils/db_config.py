import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

BASE = declarative_base()
ENGINE = create_engine(os.getenv("DATABASE_URL"), echo=False)
