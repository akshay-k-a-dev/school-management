# Profile module

Location
- Router: `app/routers/profile.py`
- Template: `app/templates/profile.html`
- Client: `app/static/js/main.js` (`initProfilePage`, `loadProfileEvents`)

Responsibilities
- View and update user contact info (name, email, phone)
- Change password
- Show "My events" (upcoming & past) for the logged-in user

Endpoints
- GET `/api/profile/` — returns the current user's public info
- PUT `/api/profile/` — update `{ name?, email?, phone? }` (email uniqueness enforced)
- POST `/api/profile/change-password` — change current password (requires `old_password`)
- GET `/api/profile/events` — returns `upcoming` and `past` events the user registered for

Notes
- Profile updates validate unique email and return the updated `user` object.
- Password changes verify current password server-side before replacing the hash.