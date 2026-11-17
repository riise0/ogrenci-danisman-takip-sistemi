"""Veritabanı tasarımındaki enum tipleri."""

import enum


class UserRole(str, enum.Enum):
    student = "student"
    advisor = "advisor"


class ProjectStatus(str, enum.Enum):
    proposed = "proposed"
    active = "active"
    completed = "completed"
    archived = "archived"


class SlotStatus(str, enum.Enum):
    available = "available"
    unavailable = "unavailable"


class MeetingStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"
    completed = "completed"


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    submitted = "submitted"
    revision_requested = "revision_requested"
    approved = "approved"
    cancelled = "cancelled"


class FeedbackDecision(str, enum.Enum):
    approved = "approved"
    revision_requested = "revision_requested"
