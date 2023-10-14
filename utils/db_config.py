import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from cryptography.fernet import Fernet

import os


def load_env(filename):
    with open(filename) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


load_env('utils/.env')

fernet = Fernet(os.getenv("FERNET_KEY"))

DB_USER = fernet.encrypt(os.getenv("DB_USER").encode()).decode()
DB_PASS = fernet.encrypt(os.getenv("DB_PASS").encode()).decode()
DB_HOST = fernet.encrypt(os.getenv("DB_HOST").encode()).decode()
DB_PORT = fernet.encrypt(os.getenv("DB_PORT").encode()).decode()
DB_NAME = fernet.encrypt(os.getenv("DB_NAME").encode()).decode()


class DBConfig(BaseModel):
    db_host: str
    db_name: str
    db_user: str
    db_pass: Optional[str] = None
    db_port: Optional[int] = None


db_config = DBConfig.model_validate(os.environ)

