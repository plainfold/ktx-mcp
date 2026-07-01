from __future__ import annotations

import os
from pathlib import Path


def read_dotenv(path: Path | None = None) -> dict[str, str]:
    env_path = path or Path(".env")
    if not env_path.is_file():
        return {}
    values: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def env_value(name: str, *, dotenv: dict[str, str] | None = None) -> str | None:
    table = dotenv if dotenv is not None else read_dotenv()
    value = os.environ.get(name, "").strip() or table.get(name, "").strip()
    return value or None
