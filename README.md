# SugboHop

SugboHop is an island-hopping discovery and ferry-pass booking app for Cebu and
the Central Visayas (Region 7). Explore featured islands, view stays and ferry
routes, create an account, and manage ferry passes.

## Technology

- **Backend:** Django and Django REST Framework
- **Frontend:** Blazor WebAssembly on .NET 8
- **Database:** SQLite (`db.sqlite3`)

## Requirements

- Python 3.10 or newer
- .NET 8 SDK or newer

Check that both are available in your terminal:

```text
python --version
dotnet --version
```

## Run the app (all-in-one)

After installing the prerequisites and backend packages below, run
`python run.py` from the project root. This is the all-in-one launcher: it
prepares the database, starts both the Django API and Blazor web client, and
opens the app in your browser. You do not need to start the servers separately.

First create and activate a Python virtual environment and install the backend
packages:

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

The final command, `python run.py`, applies database migrations, adds the
Region 7 sample data if the database has no islands, then starts both servers
and opens the app:

- Web app: <http://localhost:5000>
- Django API: <http://localhost:8000/api/>
- Django admin: <http://localhost:8000/admin/>

Press **Ctrl+C** in the terminal to stop both servers. The launcher requires
ports `5000` and `8000` to be free. On later runs, it reuses the existing
SQLite database and does not replace its data.

## Run the servers separately

From the project root, prepare the database and sample data:

```bash
python manage.py migrate
python manage.py seed_region7
```

Start the backend in one terminal:

```bash
python manage.py runserver 8000
```

Start the frontend in another terminal:

```bash
dotnet run --project frontend/SugboHop.Client --launch-profile http
```

Open <http://localhost:5000>. The frontend's API base URL is configured in
`frontend/SugboHop.Client/wwwroot/appsettings.json` and defaults to
`http://localhost:8000/`.

## API overview

The API is served under `/api/`. The main endpoints are:

- `GET /api/islands/` — browse islands; supports `featured=true` and `search=`
- `GET /api/islands/{slug}/` — island details
- `GET /api/stays/?island={slug}` — stays for an island
- `GET /api/routes/?island={slug}` — ferry routes for an island
- `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/logout/`
- `GET`, `PATCH /api/auth/me/` — view or update the signed-in user's profile
- `GET`, `POST /api/passes/` — list or book the signed-in user's ferry passes

Island, stay, and route catalogue endpoints are public and read-only. Profile
and ferry-pass endpoints require authentication.

## Development

Run the backend tests from the project root:

```bash
python manage.py test
```

Create a Django admin account when needed:

```bash
python manage.py createsuperuser
```

The backend reads optional configuration from environment variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (defaults to `True`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated; defaults to `localhost,127.0.0.1`)
- `CORS_ALLOWED_ORIGINS` (comma-separated; defaults to the local frontend URLs)

The defaults are intended for local development, not production deployment.

## Project structure

```text
backend/                         Django API application
  management/commands/          Custom management commands (Region 7 seed data)
  migrations/                   Database schema migrations
  admin.py                      Django admin registrations
  models.py                     Database models
  serializers.py                API serialization and validation
  tests.py                      Backend tests
  urls.py                       API routes
  views.py                      API endpoints
config/                          Django project configuration and entry points
frontend/SugboHop.Client/        Blazor WebAssembly app and its .NET project file
  Components/                    Reusable UI components
  Layout/                        Shared page layout
  Models/                        Frontend API data models
  Pages/                         All routable pages
  Properties/                    Local launch profiles
  Services/                      API clients and application services
  wwwroot/                       Static assets and frontend configuration
  App.razor                      Client-side router
  Program.cs                     Frontend startup and dependency registration
manage.py                        Django command-line entry point
run.py                            All-in-one local development launcher
```

`SugboHop.Client` is the Blazor project directory because it contains the
frontend's `.csproj` file. All routed pages live together in `Pages`; reusable
components, models, and services are grouped by their role instead of being
split between a global folder and feature-specific subfolders.
