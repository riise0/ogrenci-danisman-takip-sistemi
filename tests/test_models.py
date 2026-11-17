"""Model testleri. Bellek içi SQLite kullanır; PostgreSQL gerektirmez."""

from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.models as m
from app.database import Base
from app.models.enums import FeedbackDecision, TaskStatus, UserRole

EXPECTED_TABLES = {
    "users",
    "project_groups",
    "group_members",
    "projects",
    "consultant_meeting_times",
    "consultant_meetings",
    "tasks",
    "submissions",
    "feedback",
}


@pytest.fixture()
def db():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def _user(db, email, role):
    user = m.User(full_name=email, email=email, password_hash="hash", role=role)
    db.add(user)
    db.flush()
    return user


def test_tum_tablolar_olusur(db):
    assert set(inspect(db.get_bind()).get_table_names()) == EXPECTED_TABLES


def test_email_benzersizdir(db):
    _user(db, "a@okul.edu.tr", UserRole.student)
    with pytest.raises(IntegrityError):
        _user(db, "a@okul.edu.tr", UserRole.student)


def test_ogrenci_ayni_gruba_iki_kez_eklenemez(db):
    advisor = _user(db, "hoca@okul.edu.tr", UserRole.advisor)
    student = _user(db, "ogr@okul.edu.tr", UserRole.student)
    group = m.ProjectGroup(name="Grup 1", advisor_id=advisor.id)
    db.add(group)
    db.flush()
    db.add(m.GroupMember(group_id=group.id, student_id=student.id))
    db.flush()
    db.add(m.GroupMember(group_id=group.id, student_id=student.id))
    with pytest.raises(IntegrityError):
        db.flush()


def test_teslim_surumleri_ve_geri_bildirim_korunur(db):
    advisor = _user(db, "hoca@okul.edu.tr", UserRole.advisor)
    student = _user(db, "ogr@okul.edu.tr", UserRole.student)
    group = m.ProjectGroup(name="Grup 1", advisor_id=advisor.id)
    db.add(group)
    db.flush()
    task = m.Task(
        group_id=group.id,
        assigned_by=advisor.id,
        title="Rapor",
        due_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(task)
    db.flush()
    assert task.status == TaskStatus.todo

    first = m.Submission(
        task_id=task.id, uploaded_by=student.id, version_no=1, file_name="r1.pdf", file_path="/f/r1"
    )
    db.add(first)
    db.flush()
    db.add(
        m.Feedback(
            submission_id=first.id,
            advisor_id=advisor.id,
            decision=FeedbackDecision.revision_requested,
            comment="Düzelt",
        )
    )
    db.add(
        m.Submission(
            task_id=task.id, uploaded_by=student.id, version_no=2, file_name="r2.pdf", file_path="/f/r2"
        )
    )
    db.flush()
    db.refresh(task)

    assert [s.version_no for s in task.submissions] == [1, 2]
    assert task.submissions[0].feedback[0].decision == FeedbackDecision.revision_requested


def test_ayni_surum_numarasi_tekrar_edilemez(db):
    advisor = _user(db, "hoca@okul.edu.tr", UserRole.advisor)
    group = m.ProjectGroup(name="Grup 1", advisor_id=advisor.id)
    db.add(group)
    db.flush()
    task = m.Task(
        group_id=group.id,
        assigned_by=advisor.id,
        title="Rapor",
        due_at=datetime.now(timezone.utc),
    )
    db.add(task)
    db.flush()
    for _ in range(2):
        db.add(
            m.Submission(
                task_id=task.id, uploaded_by=advisor.id, version_no=1, file_name="x", file_path="/x"
            )
        )
    with pytest.raises(IntegrityError):
        db.flush()
