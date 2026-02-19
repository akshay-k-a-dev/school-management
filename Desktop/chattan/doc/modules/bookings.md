# Bookings module

Location
- Router: `app/routers/bookings.py`
- Service: `app/services/booking_service.py`
- Model: `app/models/booking.py`

Responsibilities
- Students request room/venue bookings.
- Admin reviews and approves/rejects bookings.
- Overlap checks prevent double-booking of the same room/time.

Endpoints
- POST `/api/bookings/` — **student only** — request a booking (payload: room_name, date, start_time, end_time)
- GET `/api/bookings/me` — list bookings for the current user
- GET `/api/bookings/` — **admin only** — list all bookings
- PUT `/api/bookings/{booking_id}/status` — **admin only** — approve/reject booking

Notes
- Overlap detection is implemented in `services/booking_service.py` and returns an error if an approved booking overlaps the requested slot.
- Booking `status` values: `pending`, `approved`, `rejected` (application logic treats these strings).