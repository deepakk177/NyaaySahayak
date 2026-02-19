import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load .env for local / non-Docker runs.
# On Render (and in docker-compose) the env var is injected by the platform,
# so load_dotenv() is a no-op — it never overwrites an already-set variable.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Set it in Render → Settings → Environment, "
        "in docker-compose.yml, or in your local .env file."
    )

# pool_pre_ping=True: before handing a connection from the pool, SQLAlchemy
# sends a cheap SELECT 1.  If the connection is stale (e.g. Render's Postgres
# restarted), it is discarded and a fresh one is opened automatically.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
