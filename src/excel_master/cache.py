"""Cache management for resume support."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any


CACHE_DIR = ".epm-cache"
MAX_CACHE_AGE_DAYS = 7


def _cache_key(input_path: str, template: str) -> str:
    """Generate cache filename from input path and template name."""
    h = hashlib.md5(f"{input_path}:{template}".encode()).hexdigest()[:12]
    return f"{h}.{template}.json"


def _cache_dir() -> Path:
    return Path(CACHE_DIR)


def cache_path(input_path: str, template: str) -> Path:
    return _cache_dir() / _cache_key(input_path, template)


def save_cache(
    input_path: str,
    template: str,
    records: list[dict[str, Any]],
    offset: int,
) -> Path:
    """Save parsing progress to cache."""
    p = cache_path(input_path, template)
    p.parent.mkdir(parents=True, exist_ok=True)

    input_file = Path(input_path)
    data = {
        "input_file": str(input_path),
        "input_mtime": input_file.stat().st_mtime if input_file.exists() else 0,
        "template": template,
        "processed_offset": offset,
        "records": records,
    }
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def load_cache(
    input_path: str, template: str
) -> dict[str, Any] | None:
    """Load cache if valid. Returns None if not found or stale."""
    p = cache_path(input_path, template)
    if not p.exists():
        return None

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    # Check mtime
    input_file = Path(input_path)
    if input_file.exists():
        current_mtime = input_file.stat().st_mtime
        cached_mtime = data.get("input_mtime", 0)
        if abs(current_mtime - cached_mtime) > 1:
            return None

    return data


def delete_cache(input_path: str, template: str) -> None:
    """Delete cache file after successful generation."""
    p = cache_path(input_path, template)
    if p.exists():
        p.unlink()


def clean_stale_caches() -> int:
    """Remove cache files older than MAX_CACHE_AGE_DAYS. Returns count removed."""
    cache_dir = _cache_dir()
    if not cache_dir.exists():
        return 0

    removed = 0
    cutoff = time.time() - (MAX_CACHE_AGE_DAYS * 86400)
    for f in cache_dir.glob("*.json"):
        if f.stat().st_mtime < cutoff:
            f.unlink()
            removed += 1
    return removed
