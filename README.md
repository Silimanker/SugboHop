# SugboHop

Island-hopping transit & micro-hospitality platform for Cebu / Region 7.
Stack: Django REST Framework + Blazor WebAssembly.

## Quick start (one command)
Requires Python 3.10+ and the [.NET SDK 8+](https://dotnet.microsoft.com/download).
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
`run.py` migrates + seeds the database (first run), starts Django (:8000) and the
Blazor client (:5000), and opens http://localhost:5000. Ctrl+C stops both.

## Backend setup (manual)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Admin: http://localhost:8000/admin/

## Roadmap
1. feat(backend): project structure + core models ✅
2. feat(api): REST endpoints, auth views, Region 7 seed script ✅
   + feat(api): ferry pass booking endpoints ✅
3+4. feat(frontend): Blazor client — DTOs, API services, auth state, Razor UI ← current

## API (Milestone 2)
| Method | Path | Auth | Notes |
|---|---|---|---|
| GET | `/api/islands/?featured=true&search=...` | public | paginated, nested `stays`; search matches island name, region, tagline and description |
| GET | `/api/islands/<slug>/` | public | |
| GET | `/api/stays/?island=<slug>` | public | |
| GET | `/api/routes/?island=<slug>` | public | |
| POST | `/api/auth/register/` | public | `{email, password, first_name?, last_name?, phone_number?}` → `{token, user}` |
| POST | `/api/auth/login/` | public | `{email, password}` → `{token, user}` |
| POST | `/api/auth/logout/` | token | revokes token |
| GET/PATCH | `/api/auth/me/` | token | `Authorization: Token <key>` |
| GET/POST | `/api/passes/` | token | own passes; POST `{route_id, travel_date}` |

Seed data: `python manage.py seed_region7` (safe to re-run; includes eight Region 7 destinations).
JSON is snake_case; decimals are emitted as numbers.
