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


def ensure_vector_dimensions() -> None:
    """Auto-repair: ALTER vector columns to match the SBERT model dimension.

    On Kaggle the model is all-MiniLM-L6-v2 (384 dims) but the Neon DB
    may still have columns typed as vector(1024).  This function detects
    the mismatch and fixes it automatically at startup.
    """
    if not is_postgres():
        return

    from app.core.embedding_engine import VECTOR_SIZE

    with engine.begin() as connection:
        # Check the current column type for job_descriptions
        result = connection.execute(text(
            "SELECT atttypmod FROM pg_attribute "
            "JOIN pg_class ON pg_class.oid = pg_attribute.attrelid "
            "WHERE pg_class.relname = 'job_descriptions' "
            "AND pg_attribute.attname = 'embedding_vector'"
        ))
        row = result.fetchone()
        if row is None:
            return  # Table doesn't exist yet

        current_dim = row[0]  # atttypmod stores the dimension for vector type

        if current_dim == VECTOR_SIZE:
            return  # Already correct

        print(f"[AUTO-FIX] Vector dimension mismatch: DB has {current_dim}, model needs {VECTOR_SIZE}. Altering columns...")

        # Drop indexes first
        connection.execute(text("DROP INDEX IF EXISTS ix_candidate_profiles_embedding_vector_cosine"))
        connection.execute(text("DROP INDEX IF EXISTS ix_job_descriptions_embedding_vector_cosine"))

        # Alter columns (USING NULL clears old data since dimensions changed)
        connection.execute(text(
            f"ALTER TABLE job_descriptions ALTER COLUMN embedding_vector TYPE vector({VECTOR_SIZE}) USING NULL"
        ))
        connection.execute(text(
            f"ALTER TABLE candidate_profiles ALTER COLUMN embedding_vector TYPE vector({VECTOR_SIZE}) USING NULL"
        ))

        # Recreate indexes
        connection.execute(text(f"""
            CREATE INDEX IF NOT EXISTS ix_job_descriptions_embedding_vector_cosine
            ON job_descriptions
            USING ivfflat (embedding_vector vector_cosine_ops)
            WITH (lists = 100)
            WHERE embedding_vector IS NOT NULL
        """))
        connection.execute(text(f"""
            CREATE INDEX IF NOT EXISTS ix_candidate_profiles_embedding_vector_cosine
            ON candidate_profiles
            USING ivfflat (embedding_vector vector_cosine_ops)
            WITH (lists = 100)
            WHERE embedding_vector IS NOT NULL
        """))

        print(f"[AUTO-FIX] Vector columns resized to {VECTOR_SIZE} dimensions.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
