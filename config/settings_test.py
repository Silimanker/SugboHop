"""Test settings that keep Django's test runner off the Supabase database.

The Supabase pooler role cannot create a ``test_<name>`` database, so tests use
an in-memory SQLite database. Normal development and production use the
``DATABASE_URL`` Supabase connection in ``config.settings``.
"""
import os

# settings.py validates DATABASE_URL at import time. Tests replace DATABASES
# below, so a placeholder is enough to satisfy that validation.
os.environ.setdefault(
    "DATABASE_URL", "postgresql://unused:unused@localhost:5432/unused"
)

from .settings import *  # noqa: E402,F401,F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
