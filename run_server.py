"""
RecoverAI - Unified Launcher
Starts both Backend (Flask) & Frontend (React/Vite),
and automatically opens RecoverAI in your default web browser.

Usage:
    python run_server.py
"""

import os
import sys
import time
import socket
import signal
import threading
import subprocess
import webbrowser
import urllib.request

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

BACKEND_PORT = 5000
DEFAULT_FRONTEND_PORT = 5173

child_pids = []
shutting_down = False


def log(msg):
    print(f"[RecoverAI] {msg}", flush=True)


def is_port_open(port):
    """Check if TCP port is accepting connections."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False


def wait_for_backend(timeout=30):
    """Wait until Flask backend /api/health responds."""
    start = time.time()
    url = f"http://127.0.0.1:{BACKEND_PORT}/api/health"
    while time.time() - start < timeout:
        if is_port_open(BACKEND_PORT):
            try:
                with urllib.request.urlopen(url, timeout=1) as resp:
                    if resp.status == 200:
                        return True
            except Exception:
                pass
        time.sleep(0.5)
    return False


def find_active_frontend_port():
    """Detect which port Vite is listening on (5173, 5174, 5175, etc.)."""
    for p in [5173, 5174, 5175, 5176, 5177]:
        if is_port_open(p):
            return p
    return None


def kill_pid_tree(pid):
    """Kill process and all its children cleanly."""
    if not pid:
        return
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
        else:
            os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


def cleanup(*_args):
    """Clean exit handler."""
    global shutting_down
    if shutting_down:
        return
    shutting_down = True
    print("\n" + "=" * 55, flush=True)
    log("Shutting down all services...")
    for pid in child_pids:
        kill_pid_tree(pid)
    log("Backend and Frontend stopped. Goodbye!")
    print("=" * 55, flush=True)
    sys.exit(0)


def pipe_output(pipe, prefix):
    """Pipe output lines to console with prefix."""
    try:
        for line in iter(pipe.readline, ''):
            if shutting_down:
                break
            stripped = line.rstrip()
            if stripped:
                print(f"[{prefix}] {stripped}", flush=True)
    except Exception:
        pass


def main():
    global shutting_down

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print()
    print("=" * 65, flush=True)
    print("      RecoverAI - Intelligent Revenue Recovery Assistant", flush=True)
    print("=" * 65, flush=True)
    print()

    # Verify directories
    if not os.path.exists(BACKEND_DIR) or not os.path.exists(FRONTEND_DIR):
        log("ERROR: Make sure to run this script from the project root folder.")
        sys.exit(1)

    # 1. Install frontend deps if missing
    node_modules_dir = os.path.join(FRONTEND_DIR, "node_modules")
    if not os.path.exists(node_modules_dir):
        log("Installing frontend dependencies (npm install)...")
        subprocess.run("npm install", cwd=FRONTEND_DIR, shell=True, check=True)
        log("Dependencies installed successfully.")

    # 2. Start Backend
    log(f"Starting Flask backend (http://127.0.0.1:{BACKEND_PORT})...")
    backend_env = os.environ.copy()
    backend_env["PYTHONUNBUFFERED"] = "1"

    backend_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=BACKEND_DIR,
        env=backend_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    child_pids.append(backend_proc.pid)

    t_back = threading.Thread(target=pipe_output, args=(backend_proc.stdout, "Backend"), daemon=True)
    t_back.start()

    log("Waiting for backend to initialize...")
    if not wait_for_backend(timeout=25):
        log("ERROR: Backend did not start in time. Check backend logs.")
        cleanup()
        return

    log("Backend is ready!")

    # 3. Start Frontend
    log("Starting React/Vite frontend...")
    frontend_proc = subprocess.Popen(
        "npm run dev",
        cwd=FRONTEND_DIR,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    child_pids.append(frontend_proc.pid)

    t_front = threading.Thread(target=pipe_output, args=(frontend_proc.stdout, "Frontend"), daemon=True)
    t_front.start()

    log("Waiting for frontend dev server...")
    frontend_port = None
    for _ in range(40):
        frontend_port = find_active_frontend_port()
        if frontend_port:
            break
        time.sleep(0.5)

    if not frontend_port:
        frontend_port = DEFAULT_FRONTEND_PORT

    frontend_url = f"http://localhost:{frontend_port}"
    log(f"Frontend is ready at {frontend_url}")

    # 4. Open in default browser automatically
    print()
    print("=" * 65, flush=True)
    log(f"LAUNCHING WEB BROWSER -> {frontend_url}")
    print("=" * 65, flush=True)
    print()
    print("  Demo Login Accounts:", flush=True)
    print("    * Finance Manager: manager@recoverai.demo / manager123", flush=True)
    print("    * Finance Analyst: analyst@recoverai.demo / analyst123", flush=True)
    print()
    print("  (Press Ctrl+C at any time to stop both servers)", flush=True)
    print("=" * 65, flush=True)
    print()

    # Small pause to let Vite finish initial handshake
    time.sleep(1)
    webbrowser.open(frontend_url)

    # Monitor subprocesses without premature shutdown
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


if __name__ == "__main__":
    main()
