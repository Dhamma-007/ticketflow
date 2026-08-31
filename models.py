import enum
from datetime import datetime, timezone

from app import db


def utc_now():
    return datetime.now(timezone.utc)


class EventStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class TicketStatus(enum.Enum):
    VALID = "valid"
    USED = "used"
    CANCELLED = "cancelled"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    organised_events = db.relationship(
        "Event",
        back_populates="organiser",
        foreign_keys="Event.organiser_id",
    )
    tickets = db.relationship("Ticket", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    organiser_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    venue = db.Column(db.String(255), nullable=False)
    starts_at = db.Column(db.DateTime(timezone=True), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum(EventStatus, name="event_status"),
        default=EventStatus.DRAFT,
        nullable=False,
    )
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    organiser = db.relationship(
        "User",
        back_populates="organised_events",
        foreign_keys=[organiser_id],
    )
    tickets = db.relationship("Ticket", back_populates="event")

    def __repr__(self):
        return f"<Event {self.title}>"


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    ticket_code = db.Column(db.String(32), unique=True, nullable=False, index=True)
    status = db.Column(
        db.Enum(TicketStatus, name="ticket_status"),
        default=TicketStatus.VALID,
        nullable=False,
    )
    checked_in_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    user = db.relationship("User", back_populates="tickets")
    event = db.relationship("Event", back_populates="tickets")

    __table_args__ = (
        db.UniqueConstraint("user_id", "event_id", name="uq_ticket_user_event"),
    )

    def __repr__(self):
        return f"<Ticket {self.ticket_code}>"
