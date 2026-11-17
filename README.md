# Öğrenci–Danışman Görüşme ve Proje Takip Sistemi

SE 342 Software Validation and Testing dersi projesi. Öğrenci proje grupları ile danışman
öğretim üyeleri arasındaki görüşmeleri, görevleri, dosya teslimlerini ve geri bildirimleri
tek bir ortamda yönetir.

## Teknolojiler

- Python 3.12+ ve FastAPI
- SQLAlchemy 2.0 (ORM)
- PostgreSQL (yerel deneme için SQLite da desteklenir)
- pytest

## Klasör yapısı

```
app/
  config.py      Ayarlar (.env üzerinden DATABASE_URL)
  database.py    Veritabanı bağlantısı ve oturum yönetimi
  init_db.py     Tabloları oluşturan betik
  main.py        FastAPI uygulaması
  models/        Veritabanı modelleri
tests/           Model testleri
```

## Modeller

| Model | Tablo | İlgili gereksinim |
|---|---|---|
| User | users | FR-01, FR-07 |
| ProjectGroup | project_groups | FR-02, FR-08 |
| GroupMember | group_members | FR-02 |
| Project | projects | FR-08 |
| ConsultantMeetingTime | consultant_meeting_times | FR-03 |
| ConsultantMeeting | consultant_meetings | FR-03 |
| Task | tasks | FR-04 |
| Submission | submissions | FR-05 |
| Feedback | feedback | FR-06 |

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

`.env` dosyasındaki `DATABASE_URL` değerini kendi veritabanınıza göre düzenleyin.

## Çalıştırma

```bash
python -m app.init_db
uvicorn app.main:app --reload
```

- `GET /` uygulamanın çalıştığını gösterir.
- `GET /health/db` veritabanı bağlantısını ve tabloları doğrular.

## Testler

```bash
pytest
```

## Proje yönetimi

Gereksinimler, sprintler ve görevler JIRA üzerinde (SAPTS projesi) takip edilir.
