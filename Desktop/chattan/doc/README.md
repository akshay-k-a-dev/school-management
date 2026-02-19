# Documentation — Campus Service Hub (Chattan)

This folder contains developer-facing documentation for the project: database schema, dependency notes, normalization explanation and module-level descriptions.

Quick links
- `database_schema.md` — ER / table definitions and quick DDL notes
- `normalization.md` — normalization rationale
- `dependencies.md` — Python packages, install and runtime notes
- `modules/` — module-wise documentation (routers, services, models, frontend)

How to use
1. Read `dependencies.md` and install dependencies in a virtualenv.
2. Inspect `database_schema.md` to understand tables and relationships; `schema.sql` (project root) is the source DDL.
3. Open specific module docs under `modules/` for implementation details and endpoint lists.

If you want, I can generate a single consolidated PDF of these docs or add diagrams (PNG/SVG).