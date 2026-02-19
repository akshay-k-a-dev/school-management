# Complaints module

Location
- Router: `app/routers/complaints.py`
- Service: `app/services/complaint_service.py`
- Model: `app/models/complaint.py`

Responsibilities
- Students submit complaints (optional image upload).
- Admin can view all complaints and update status / assign staff.

Endpoints
- POST `/api/complaints/` — **student only**, multipart/form-data with `title`, `description`, `category` and optional `file` (image). Returns created complaint.
- GET `/api/complaints/me` — list complaints created by the user
- GET `/api/complaints/` — **admin only** — list all complaints
- PUT `/api/complaints/{complaint_id}/status` — **admin only** — update status and optionally `assigned_to`

Notes
- Uploaded images are validated (MIME type) and limited to **2 MB**; stored in `app/static/uploads/` and referenced by `image_path` on the complaint.
- Status values used by the UI: `pending`, `in_progress`, `resolved` (strings; adapt as needed).
- File validation and size enforcement live in the complaints router (server-side) and are intentionally conservative.
