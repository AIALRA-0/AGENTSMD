#!/usr/bin/env python3
from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "agentsmd_web"
VENV_DIR = BASE_DIR / ".venv_agentsmd_web"
REQ_FILE = APP_DIR / "requirements.txt"
DEFAULT_AGENTS_ROOT = BASE_DIR
DEFAULT_BACKUP_ROOT = DEFAULT_AGENTS_ROOT / "backup"
HOST = "127.0.0.1"
START_PORT = 34000


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def _venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def ensure_venv() -> Path:
    if not _venv_python().exists():
        print("[setup] 创建虚拟环境...")
        _run([sys.executable, "-m", "venv", str(VENV_DIR)])
    return _venv_python()


def install_requirements(py: Path) -> None:
    print("[setup] 安装依赖...")
    _run([str(py), "-m", "pip", "install", "-q", "--upgrade", "pip"]) 
    _run([str(py), "-m", "pip", "install", "-q", "-r", str(REQ_FILE)])


def find_free_port(host: str, start_port: int) -> int:
    port = start_port
    while port < start_port + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if s.connect_ex((host, port)) != 0:
                return port
        port += 1
    raise RuntimeError("No free port found")


def main() -> None:
    if not APP_DIR.exists():
        raise SystemExit(f"Missing app directory: {APP_DIR}")
    if not DEFAULT_AGENTS_ROOT.exists():
        raise SystemExit(f"Missing AGENTSMD directory: {DEFAULT_AGENTS_ROOT}")

    py = ensure_venv()
    install_requirements(py)

    port = find_free_port(HOST, START_PORT)
    url = f"http://{HOST}:{port}"

    env = os.environ.copy()
    env.setdefault("AGENTSMD_ROOT", str(DEFAULT_AGENTS_ROOT))
    env.setdefault("AGENTSMD_BACKUP_ROOT", str(DEFAULT_BACKUP_ROOT))

    print(f"[run] 启动 AGENTSMD 控制台: {url}")
    print("[run] 已加载 AGENTSMD_ROOT 与 AGENTSMD_BACKUP_ROOT 配置")

    proc = subprocess.Popen(
        [
            str(py),
            "-m",
            "uvicorn",
            "app:app",
            "--host",
            HOST,
            "--port",
            str(port),
            "--reload",
        ],
        cwd=str(APP_DIR),
        env=env,
    )

    time.sleep(1.0)
    webbrowser.open(url)

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n[stop] 正在停止服务...")
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
