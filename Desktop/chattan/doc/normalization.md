# Normalization and data design

This document explains the normalization decisions used in the database design.

## Goals
- Avoid redundant data and update anomalies.
- Keep data atomic and easy to query for typical app flows (registrations, bookings, complaints).

## Normal forms applied
- 1NF (First Normal Form)
  - All tables contain atomic (indivisible) values — no arrays or comma-separated lists in columns.
  - Example: `event_registrations` is a separate table rather than storing a list of user IDs on `events`.

- 2NF (Second Normal Form)
  - Composite-key dependencies avoided; each non-key column depends on the whole primary key.
  - Example: booking details (date/start/end) are stored on the `bookings` row (dependent on booking id), not duplicated across users.

- 3NF (Third Normal Form)
  - No transitive dependencies: fields that can be derived are not stored redundantly.
  - Example: `EventRegistration` links `user_id` and `event_id` rather than embedding user attributes inside `events`.

## Specific design choices
- Many-to-many (Users ↔ Events) handled with `event_registrations` to avoid repeating groups and to allow per-registration metadata later (e.g., `registered_at`).
- Complaints and bookings are separate entities to model different workflows and lifecycle states (`status`, `assigned_to`).
- `users.phone` is stored as a simple atomic field (no separate contact table required for this scope).

## When to denormalize (future)
- For read-heavy dashboards, consider derived summary tables or materialized views.
- If `user` contact history grows complex, split into `contacts` table.

Conclusion: the current schema follows 3NF for consistency, extensibility and to keep the application logic straightforward.