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
1. feat(backend): project structure + core models  ← current
2. feat(api): REST endpoints, auth views, Region 7 seed script
3. feat(frontend): C# DTOs, HTTP services, Blazor auth state
4. feat(ui): Tailwind → Razor components + API integration
