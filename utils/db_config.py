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
DB_HOST_token = fernet.encrypt(b"" + os.environ["DB_HOST"].encode())
DB_HOST = fernet.decrypt(DB_HOST_token).decode('utf-8')
DB_NAME_token = fernet.encrypt(b"" + os.environ["DB_NAME"].encode())
DB_NAME = fernet.decrypt(DB_NAME_token).decode('utf-8')
DB_PASS_token = fernet.encrypt(b"" + os.environ["DB_PASS"].encode())
DB_PASS = fernet.decrypt(DB_PASS_token).decode('utf-8')
DB_PORT_token = fernet.encrypt(b"" + os.environ["DB_PORT"].encode())
DB_PORT = fernet.decrypt(DB_PORT_token).decode('utf-8')
DB_USER_token = fernet.encrypt(b"" + os.environ["DB_USER"].encode())
DB_USER = fernet.decrypt(DB_USER_token).decode('utf-8')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


SECRET_KEY_token = fernet.encrypt(b"" + os.environ["SECRET_KEY"].encode())
SECRET_KEY = fernet.decrypt(SECRET_KEY_token).decode('utf-8')
ALGORITHM_token = fernet.encrypt(b"" + os.environ["ALGORITHM"].encode())
ALGORITHM = fernet.decrypt(ALGORITHM_token).decode('utf-8')
ACCESS_TOKEN_EXPIRE_MINUTES_token = fernet.encrypt(b"" + os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"].encode())
ACCESS_TOKEN_EXPIRE_MINUTES = int(fernet.decrypt(ACCESS_TOKEN_EXPIRE_MINUTES_token).decode('utf-8'))
