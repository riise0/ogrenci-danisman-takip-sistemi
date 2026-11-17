"""Uygulama ayarları. Değerler .env dosyasından veya ortam değişkenlerinden okunur."""

import os

from dotenv import load_dotenv

load_dotenv()

# Örnek: postgresql+psycopg://kullanici:sifre@localhost:5432/sapts
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sapts_dev.db")

APP_NAME = "Öğrenci–Danışman Görüşme ve Proje Takip Sistemi"
