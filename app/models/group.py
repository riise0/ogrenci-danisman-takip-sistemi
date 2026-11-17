from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, BigIntPK
from app.models.enums import ProjectStatus

# BR-01: bir proje grubunda en fazla 2 öğrenci bulunabilir.
MAX_GROUP_MEMBERS = 2


class ProjectGroup(Base):
    """Öğrenci proje grubu ve sorumlu danışmanı (FR-02, FR-08)."""

    __tablename__ = "project_groups"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    advisor = relationship("User")
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    project = relationship("Project", back_populates="group", uselist=False)


class GroupMember(Base):
    """Grup üyeliği. Bir öğrenci aynı gruba yalnızca bir kez eklenebilir."""

    __tablename__ = "group_members"
    __table_args__ = (UniqueConstraint("group_id", "student_id", name="uq_group_member"),)

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("project_groups.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    group = relationship("ProjectGroup", back_populates="members")
    student = relationship("User")


class Project(Base):
    """Grubun projesi. Her grup için bir proje tanımlanır."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("project_groups.id"), nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"), nullable=False, default=ProjectStatus.proposed
    )
    started_at: Mapped[date | None] = mapped_column(Date)
    completed_at: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    group = relationship("ProjectGroup", back_populates="project")
