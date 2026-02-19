# Models (SQLAlchemy)

Location: `app/models/`

Summary of main models

- User (`users`)
  - Fields: `id`, `name`, `email` (unique), `password_hash`, `role`, `phone`, `created_at`
  - Relationships: `complaints`, `bookings`, `registrations`

- Event (`events`)
  - Fields: `id`, `title`, `description`, `date`, `venue`, `capacity`, `created_by`, `created_at`
  - Relationship: `registrations` (EventRegistration)

- EventRegistration (`event_registrations`)
  - Fields: `id`, `event_id`, `user_id`, `registered_at`
  - Purpose: join table for user ↔ event registrations

- Complaint (`complaints`)
  - Fields: `id`, `user_id`, `title`, `description`, `category`, `status`, `assigned_to`, `image_path`, `created_at`

- Booking (`bookings`)
  - Fields: `id`, `user_id`, `room_name`, `date`, `start_time`, `end_time`, `status`, `created_at`

- Announcement (`announcements`)
  - Fields: `id`, `title`, `content`, `created_by`, `created_at`, `attachment`

Notes
- Relationships are declared via `relationship(...)` for convenient ORM access.
- Primary keys use `Integer` autoincrement; SQLite stores dates as `DATETIME`/ISO strings via SQLAlchemy.
- See `schema.sql` for the canonical DDL.