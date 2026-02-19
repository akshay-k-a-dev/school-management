# Dependencies & environment

Recommended Python: 3.10+ (3.11 is supported).

Install (development):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Packages (from `requirements.txt`) and purpose
- fastapi — web framework (API + templating glue)
- uvicorn[standard] — ASGI server for development
- SQLAlchemy — ORM / database access
- python-jose[cryptography] — JWT creation/validation
- passlib[bcrypt] — password hashing utilities (code uses pbkdf2_sha256 via passlib)
- python-multipart — form / file upload parsing
- Jinja2 — server-side HTML templates
- aiofiles — async file handling for uploads/static
- python-dateutil — date parsing/utility functions
- reportlab — (optional) PDF generation for admin export

Notes / gotchas
- `reportlab` may fail to build on systems missing development headers/toolchain; if you see build errors you can:
  - skip installing `reportlab` (PDF export will return a helpful error), or
  - install platform-specific build dependencies so `pip` can build wheels, or
  - run the app in an environment (CI/container) where `reportlab` wheel is available.

Running the server
- Development: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- The app creates a sample admin on first startup: `admin@example.com` / `admin123`.

If you want, I can add a `devcontainer` or Dockerfile to make environment setup reproducible.