# Routers & page routes

All routers are registered in `app/main.py` using `app.include_router(...)` and `app.mount('/static', ...)`.

API router prefixes and purpose
- `app/routers/auth.py` → `/api/auth` — signup / login / token validation
- `app/routers/profile.py` → `/api/profile` — profile endpoints
- `app/routers/complaints.py` → `/api/complaints` — complaints + upload
- `app/routers/events.py` → `/api/events` — events + registrations
- `app/routers/bookings.py` → `/api/bookings` — booking requests and admin actions
- `app/routers/announcements.py` → `/api/announcements` — announcements management
- `app/routers/dashboard.py` → `/api/admin/dashboard` — admin stats + export
- `app/routers/pages.py` → page routes + `/api/home/summary`

Pages (templates)
- `/` → `index.html` (home summary)
- `/login`, `/signup` → authentication pages
- `/profile` → profile editing/view page (must be logged in)
- `/events`, `/complaints`, `/bookings`, `/announcements` → feature pages
- `/admin/dashboard` → admin UI

Auth enforcement
- Protected endpoints use the `get_current_user` dependency from `app/routers/auth.py`.
- Role checks are performed in routers (e.g., `if user.role != 'admin': raise HTTPException(403)`).

Where to add new routes
- Add lightweight route functions in `app/routers/` and place business logic into `app/services/` to keep concerns separate.