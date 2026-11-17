"""Veritabanı bağlantısı: engine, oturum ve model taban sınıfı."""

from collections.abc import Iterator

from sqlalchemy import BigInteger, Integer, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# PostgreSQL'de bigint; SQLite'ta otomatik artan anahtar için integer.
BigIntPK = BigInteger().with_variant(Integer, "sqlite")


class Base(DeclarativeBase):
    """Tüm modellerin taban sınıfı."""


def get_db() -> Iterator[Session]:
    """FastAPI bağımlılığı: istek başına bir veritabanı oturumu açar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> bool:
    """Veritabanına ulaşılabildiğini doğrular."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
