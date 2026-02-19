# Events module

Location
- Router: `app/routers/events.py`
- Service: `app/services/event_service.py`
- Models: `app/models/event.py`, `app/models/registration.py`

Responsibilities
- Admin can create events; students can register/unregister for events.
- Prevent over-capacity registration.
- Expose user's registrations for frontend convenience.

Endpoints (key)
- POST `/api/events/` — **admin only** — create event (payload: title, description, date, venue, capacity)
- GET `/api/events/` — list all events (public)
- GET `/api/events/registrations/me` — returns `{ event_ids: [...] }` for the current user
- POST `/api/events/{event_id}/register` — register current user (auth required; capacity enforced)
- POST `/api/events/{event_id}/unregister` — cancel registration
- GET `/api/events/{event_id}/participants` — **admin only** — list participant IDs

Notes / behaviour
- Registration capacity is enforced in `services/event_service.py`.
- `event_registrations` is a separate table to represent many-to-many relationships (one `EventRegistration` per registration).
- Frontend calls `/registrations/me` to mark already-registered events and to disable Register buttons.