# TicketFlow

TicketFlow is an event ticketing platform for free RSVP events. Organisers create and publish events; attendees register, receive a unique ticket (code + QR), and get checked in at the door. Capacity limits and sold-out handling are built in.

**Status:** Early development — Flask app skeleton with a health check endpoint. Database, auth, and core flows are next.

## Features (planned v1)

- **Organiser:** Create events (draft → published), edit, unpublish, view registrations, check in attendees
- **Attendee:** Browse published events, RSVP (one ticket per user per event), view tickets with QR code
- **Capacity:** Per-event limits with sold-out handling
- **Check-in:** Event owner validates tickets by code or QR scan
- **Cancel:** In-app cancellation (email notifications planned later)

## Tech stack

| Layer | Choice |
|-------|--------|
| Backend | Flask |
| Templates | Jinja2 |
| Database | PostgreSQL (via Docker) — coming in Phase 4 |
| Auth | Flask-Login (planned) |

## Prerequisites

- Python 3.11+ (3.13 tested)
- Git
- Docker Desktop (for PostgreSQL, upcoming)

## Getting started

### 1. Clone the repository

```bash
git clone git@github.com:Dhamma-007/ticketflow.git
cd ticketflow
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Copy the example file and fill in values when you add a database:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key (required before auth/sessions) |
| `DATABASE_URL` | PostgreSQL connection string (Phase 4) |

### 5. Run the app

```bash
flask --app app run
```

The app runs at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 6. Verify

Open [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health) — you should see:

```json
{"status": "ok"}
```

## Project structure (current)

```
ticketflow/
├── app.py              # Flask application entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore
└── README.md
```

## Branching

- `main` — stable releases
- `develop` — active development

## Roadmap

- [x] Phase 3: Project setup + `/health` endpoint
- [ ] Phase 4: Docker PostgreSQL + SQLAlchemy models (User, Event, Ticket)
- [ ] Phase 5: Auth (signup / login)
- [ ] Phase 6: Event CRUD + public listing
- [ ] Phase 7: RSVP + tickets + capacity
- [ ] Phase 8: QR check-in
- [ ] Phase 9: Tests, CI, deploy

## License

Personal learning project — add a license if you open-source it.
