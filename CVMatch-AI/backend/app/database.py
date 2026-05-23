from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

load_dotenv()

# Assuming a default fallback for local dev if not present
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///:memory:"
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
pool_args = {"poolclass": StaticPool} if DATABASE_URL == "sqlite:///:memory:" else {}
if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "", 1)
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args, **pool_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def is_sqlite() -> bool:
    return DATABASE_URL.startswith("sqlite")


def is_postgres() -> bool:
    return DATABASE_URL.startswith(("postgresql", "postgres"))


def ensure_pgvector_extension() -> None:
    """Enable pgvector before SQLAlchemy creates vector columns."""

    if not is_postgres():
        return

    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


def ensure_vector_indexes() -> None:
    """Create cosine indexes used by pgvector similarity searches."""

    if not is_postgres():
        return

    statements = (
        """
        CREATE INDEX IF NOT EXISTS ix_job_descriptions_embedding_vector_cosine
        ON job_descriptions
        USING ivfflat (embedding_vector vector_cosine_ops)
        WITH (lists = 100)
        WHERE embedding_vector IS NOT NULL
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_candidate_profiles_embedding_vector_cosine
        ON candidate_profiles
        USING ivfflat (embedding_vector vector_cosine_ops)
        WITH (lists = 100)
        WHERE embedding_vector IS NOT NULL
        """,
    )
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
