from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.config import APP_NAME
from app.database import engine, get_db

app = FastAPI(title=APP_NAME, version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"uygulama": APP_NAME, "durum": "çalışıyor"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)) -> dict[str, object]:
    """Veritabanı bağlantısını ve tabloların varlığını doğrular."""
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # bağlantı hatası istemciye 503 olarak döner
        raise HTTPException(status_code=503, detail=f"Veritabanına ulaşılamıyor: {exc}") from exc
    return {
        "veritabani": engine.dialect.name,
        "baglanti": "tamam",
        "tablolar": sorted(inspect(engine).get_table_names()),
    }
