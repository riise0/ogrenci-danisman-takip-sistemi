"""Tabloları oluşturur:  python -m app.init_db"""

from sqlalchemy import inspect

import app.models  # noqa: F401  (modellerin Base'e kaydolması için)
from app.database import Base, check_connection, engine


def main() -> None:
    check_connection()
    print(f"Bağlantı tamam: {engine.dialect.name}")
    Base.metadata.create_all(engine)
    for name in sorted(inspect(engine).get_table_names()):
        print(f"  tablo: {name}")


if __name__ == "__main__":
    main()
