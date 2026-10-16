#!/usr/bin/env python3
"""SugboHop one-command launcher.

    python run.py

Sets up the database (first run), starts the Django API on :8000 and the
Blazor WebAssembly client on :5000, then opens your browser. Ctrl+C stops both.
"""
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLIENT = ROOT / "frontend" / "SugboHop.Client"
API_PORT, WEB_PORT = 8000, 5000
URL = f"http://localhost:{WEB_PORT}"
IS_WIN = os.name == "nt"
STARTUP_TIMEOUT = 300  # first `dotnet run` restores NuGet packages


def say(msg):
    print(f"\n▶ {msg}", flush=True)


def die(msg):
    print(f"\n✖ {msg}", file=sys.stderr)
    sys.exit(1)


def port_open(port):
    try:
        with socket.create_connection(("localhost", port), timeout=0.5):
            return True
    except OSError:
        return False


def manage(*args, quiet=False):
    return subprocess.run(
        [sys.executable, "manage.py", *args],
        cwd=ROOT,
        stdout=subprocess.DEVNULL if quiet else None,
        stderr=subprocess.DEVNULL if quiet else None,
    )


def spawn(cmd):
    kwargs = {"cwd": ROOT}
    if IS_WIN:
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    return subprocess.Popen(cmd, **kwargs)


def stop(proc):
    if proc.poll() is not None:
        return
    try:
        if IS_WIN:
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
        else:
            os.killpg(proc.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def preflight():
    if subprocess.run(
        [sys.executable, "-c", "import django, rest_framework, corsheaders"],
        capture_output=True,
    ).returncode != 0:
        die("Python dependencies missing. Activate your venv, then run:\n"
            "    pip install -r requirements.txt")

    dotnet = shutil.which("dotnet")
    if not dotnet:
        die("The .NET SDK (8 or newer) isn't installed or isn't on PATH.\n"
            "    Download: https://dotnet.microsoft.com/download\n"
            "    Then reopen your terminal and check with: dotnet --version")
    out = subprocess.run([dotnet, "--version"], capture_output=True, text=True).stdout.strip()
    try:
        if int(out.split(".")[0]) < 8:
            die(f".NET SDK {out} found, but version 8 or newer is required.")
    except ValueError:
        pass

    for port, name in ((API_PORT, "API"), (WEB_PORT, "web client")):
        if port_open(port):
            die(f"Port {port} is already in use (needed by the {name}). "
                "Stop whatever is using it and try again.")


def prepare_database():
    say("Preparing database…")
    if manage("migrate", "--noinput", quiet=True).returncode != 0:
        die("Database migration failed. Run `python manage.py migrate` to see the error.")
    has_islands = manage(
        "shell", "-c",
        "import sys; from backend.models import Island; "
        "sys.exit(0 if Island.objects.exists() else 1)",
        quiet=True,
    ).returncode == 0
    if not has_islands:
        say("Seeding Region 7 islands…")
        manage("seed_region7")


def main():
    preflight()
    prepare_database()

    procs = []
    try:
        say(f"Starting Django API on http://localhost:{API_PORT} …")
        procs.append(spawn([sys.executable, "manage.py", "runserver", str(API_PORT)]))

        say(f"Starting Blazor client on {URL} (first run downloads packages — be patient) …")
        procs.append(spawn([
            "dotnet", "run", "--project", str(CLIENT), "--launch-profile", "http",
        ]))

        deadline = time.time() + STARTUP_TIMEOUT
        while not (port_open(API_PORT) and port_open(WEB_PORT)):
            if any(p.poll() is not None for p in procs):
                die("A server exited during startup — see the messages above.")
            if time.time() > deadline:
                die("Timed out waiting for the servers to start.")
            time.sleep(1)

        say(f"SugboHop is running → {URL}   (Ctrl+C to stop)")
        webbrowser.open(URL)

        while all(p.poll() is None for p in procs):
            time.sleep(1)
        die("A server stopped unexpectedly — see the messages above.")
    except KeyboardInterrupt:
        print("\nShutting down…")
    finally:
        for p in procs:
            stop(p)


if __name__ == "__main__":
    main()
