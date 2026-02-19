# Announcements module

Location
- Router: `app/routers/announcements.py`
- Service: `app/services/announcement_service.py`
- Template: `app/templates/announcements.html`

Responsibilities
- Admins create announcements; everyone can view them on the home page.

Endpoints
- POST `/api/announcements/` — **admin only** — create announcement (form: `title`, `content`, optional `attachment`)
- GET `/api/announcements/` — list announcements for display

Notes
- Announcements are simple content objects; attachments are stored as text references (no complex storage flow in this version).
- UI displays announcements on the homepage and on the announcements page.