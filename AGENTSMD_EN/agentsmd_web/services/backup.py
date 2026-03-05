from __future__ import annotations

import tarfile
from datetime import datetime
from pathlib import Path


def create_manual_backup(source_root: Path, backup_root: Path) -> tuple[Path, int]:
    backup_root.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y_%m_%d_%H%M%S")
    out_path = backup_root / f"AGENTSMD_backup_{ts}.tar.gz"

    with tarfile.open(out_path, "w:gz") as tar:
        tar.add(source_root, arcname=source_root.name)

    return out_path, out_path.stat().st_size
