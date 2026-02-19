# Dashboard (admin)

Location
- Router: `app/routers/dashboard.py`
- Service: `app/services/dashboard_service.py`
- Frontend: admin section on `app/templates/dashboard.html`, client code in `app/static/js/main.js`

Responsibilities
- Provide counts and recent activity for the admin dashboard.
- Allow exporting a simple PDF report that includes Events, Complaints and Bookings (admin-only).

Endpoints
- GET `/api/admin/dashboard/stats` — returns counts for users, events, complaints and bookings
- GET `/api/admin/dashboard/recent` — recent activity summary
- GET `/api/admin/dashboard/export` — **admin only** — returns a generated PDF (requires `reportlab` on the server)

Notes
- The `/export` endpoint uses `reportlab`. If `reportlab` is not available the endpoint returns a clear 500 error with instructions to install the package.
- Dashboard service composes aggregated queries; add caching or pagination if data grows large.