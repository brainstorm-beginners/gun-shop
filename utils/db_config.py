import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from cryptography.fernet import Fernet

load_dotenv()

fernet = Fernet(os.environ.get("FERNET_KEY"))

DB_USER = os.environ.get("DB_USER")
DB_PASS = fernet.encrypt(os.environ.get("DB_PASS").encode()).decode()
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class DBConfig(BaseModel):
    db_host: str
    db_name: str
    db_user: str
    db_pass: Optional[str] = None
    db_port: Optional[int] = None


db_config = DBConfig.model_validate(os.environ)

