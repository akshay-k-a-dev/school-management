# Auth module

Location
- Router: `app/routers/auth.py`
- Services: `app/services/auth.py`
- Schemas: `app/schemas/user.py`

Responsibilities
- User signup and login
- Password hashing (passlib/pbkdf2_sha256)
- JWT creation/validation
- `get_current_user` dependency for protected routes

Important endpoints
- POST `/api/auth/signup` — create a new user (body: name, email, password, role)
- POST `/api/auth/login` — returns `{ access_token, user }`
- GET `/api/auth/me` — returns the authenticated user's public info

Notes
- Password hashing uses `pbkdf2_sha256` via `passlib` in `services/auth.py` (stable across platforms).
- JWT secret is read from `SECRET_KEY` env var; default `dev-secret-change-me` in development.
- `get_current_user` raises 401 on invalid/expired token and is used across routers to enforce auth/roles.