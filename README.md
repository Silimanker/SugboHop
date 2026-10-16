# SugboHop

Island-hopping transit & micro-hospitality platform for Cebu / Region 7.
Stack: Django REST Framework + Blazor WebAssembly.

## Backend setup
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
2. feat(api): REST endpoints, auth views, Region 7 seed script ← current
3. feat(frontend): C# DTOs, HTTP services, Blazor auth state
4. feat(ui): Tailwind → Razor components + API integration

## API (Milestone 2)
| Method | Path | Auth | Notes |
|---|---|---|---|
| GET | `/api/islands/?featured=true` | public | paginated, nested `stays` |
| GET | `/api/islands/<slug>/` | public | |
| GET | `/api/stays/?island=<slug>` | public | |
| GET | `/api/routes/?island=<slug>` | public | |
| POST | `/api/auth/register/` | public | `{email, password, first_name?, last_name?, phone_number?}` → `{token, user}` |
| POST | `/api/auth/login/` | public | `{email, password}` → `{token, user}` |
| POST | `/api/auth/logout/` | token | revokes token |
| GET/PATCH | `/api/auth/me/` | token | `Authorization: Token <key>` |

Seed data: `python manage.py seed_region7` (safe to re-run).
JSON is snake_case; decimals are emitted as numbers.
