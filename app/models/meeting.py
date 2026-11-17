from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, BigIntPK
from app.models.enums import MeetingStatus, SlotStatus


class ConsultantMeetingTime(Base):
    """Danışmanın açtığı uygun görüşme saati (FR-03)."""

    __tablename__ = "consultant_meeting_times"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[SlotStatus] = mapped_column(
        Enum(SlotStatus, name="slot_status"), nullable=False, default=SlotStatus.available
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    advisor = relationship("User")
    meetings = relationship("ConsultantMeeting", back_populates="slot")


class ConsultantMeeting(Base):
    """Bir grubun uygun saate yaptığı görüşme talebi (FR-03)."""

    __tablename__ = "consultant_meetings"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    slot_id: Mapped[int] = mapped_column(
        ForeignKey("consultant_meeting_times.id"), nullable=False
    )
    group_id: Mapped[int] = mapped_column(ForeignKey("project_groups.id"), nullable=False)
    requested_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[MeetingStatus] = mapped_column(
        Enum(MeetingStatus, name="meeting_status"), nullable=False, default=MeetingStatus.pending
    )
    topic: Mapped[str | None] = mapped_column(String(250))
    decision_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    slot = relationship("ConsultantMeetingTime", back_populates="meetings")
    group = relationship("ProjectGroup")
    requester = relationship("User")
