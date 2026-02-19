# Services (business logic)

Location: `app/services/`

Purpose
- Encapsulate database operations and business rules so routers remain thin.
- Typical responsibilities: validation, complex queries, overlap checks, registration logic.

Files & responsibilities
- `auth.py` — create/verify users, password hashing and JWT token creation
- `event_service.py` — create/list events, register/unregister users, capacity checks
- `booking_service.py` — create bookings, detect overlap, update status
- `complaint_service.py` — create/list/update complaints, assignment logic
- `announcement_service.py` — create/list announcements
- `dashboard_service.py` — aggregation for admin stats/recent activity

Examples of business logic locations
- Preventing double-booking: `booking_service.create_booking`
- Enforcing event capacity: `event_service.count_registrations` + `register_user_for_event`

Testing suggestions
- Add unit tests for `event_service` registration and `booking_service` overlap logic.
- Mock DB sessions to verify edge cases (capacity exactly full, overlapping edge times, etc.).