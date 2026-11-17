from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, BigIntPK
from app.models.enums import FeedbackDecision, TaskStatus


class Task(Base):
    """Danışmanın gruba atadığı görev (FR-04)."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("project_groups.id"), nullable=False)
    assigned_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"), nullable=False, default=TaskStatus.todo
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    group = relationship("ProjectGroup")
    assigner = relationship("User")
    submissions = relationship(
        "Submission", back_populates="task", order_by="Submission.version_no"
    )


class Submission(Base):
    """Bir göreve yapılan teslim. Her yeni teslim yeni sürümdür; eskiler korunur (FR-05, BR-04)."""

    __tablename__ = "submissions"
    __table_args__ = (UniqueConstraint("task_id", "version_no", name="uq_submission_version"),)

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    version_no: Mapped[int] = mapped_column(Integer, nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    task = relationship("Task", back_populates="submissions")
    uploader = relationship("User")
    feedback = relationship("Feedback", back_populates="submission")


class Feedback(Base):
    """Danışmanın bir teslim için verdiği karar ve yorum (FR-06)."""

    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id"), nullable=False)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    decision: Mapped[FeedbackDecision] = mapped_column(
        Enum(FeedbackDecision, name="feedback_decision"), nullable=False
    )
    comment: Mapped[str | None] = mapped_column(Text)
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    submission = relationship("Submission", back_populates="feedback")
    advisor = relationship("User")
