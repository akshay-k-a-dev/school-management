# Frontend (templates & static)

Location
- Templates: `app/templates/` (Jinja2)
- Static: `app/static/` — `css/`, `js/`, `uploads/`
- Main client logic: `app/static/js/main.js`

Key templates
- `base.html` — base layout and navigation
- `index.html` — home / announcements / quick stats
- `events.html`, `bookings.html`, `complaints.html`, `announcements.html` — feature pages
- `profile.html` — profile editing and "My events"

Important JS functions (in `main.js`)
- `apiFetch()` — small wrapper used for authenticated fetch requests
- `initHomePage()` / `loadEvents()` — load home and events data
- `initProfilePage()` / `loadProfileEvents()` — profile init and user's events
- Registration UX: `loadEvents()` prefetches `/events/registrations/me` and disables the "Register" button for already-registered events; on successful registration the button becomes `Registered` and is disabled.
- Toasts & UI helpers: `showToast()`, `showUserInNav()`

File uploads
- Complaints accept an optional image (validated on server); uploaded files are stored in `app/static/uploads/` and served via `/static/uploads/`.

Styling
- Basic CSS in `app/static/css/style.css`. The project uses minimal, dependency-free UI (vanilla JS + Jinja2).

Extending the frontend
- Add new template files and corresponding `pages.py` route entries.
- Update `main.js` with new `init*` functions and call them from the page boot strap (check the DOM for expected IDs).
