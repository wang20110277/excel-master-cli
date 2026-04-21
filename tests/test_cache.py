"""Tests for the cache module."""

import json
import time
import pytest
from pathlib import Path

from excel_master.cache import (
    save_cache, load_cache, delete_cache, clean_stale_caches, CACHE_DIR,
)


@pytest.fixture
def cache_setup(tmp_path, monkeypatch):
    """Set up cache in temp directory."""
    monkeypatch.chdir(tmp_path)
    yield tmp_path
    # Cleanup
    cache_dir = tmp_path / CACHE_DIR
    if cache_dir.exists():
        for f in cache_dir.glob("*.json"):
            f.unlink()


class TestCache:
    def test_save_and_load(self, cache_setup, tmp_path):
        input_file = tmp_path / "input.md"
        input_file.write_text("test content")

        records = [{"title": "Test"}]
        save_cache(str(input_file), "test-case", records, 1)

        cached = load_cache(str(input_file), "test-case")
        assert cached is not None
        assert len(cached["records"]) == 1
        assert cached["processed_offset"] == 1

    def test_load_nonexistent(self, cache_setup):
        cached = load_cache("nonexistent.md", "test-case")
        assert cached is None

    def test_delete_cache(self, cache_setup, tmp_path):
        input_file = tmp_path / "input.md"
        input_file.write_text("test")

        save_cache(str(input_file), "test-case", [], 0)
        delete_cache(str(input_file), "test-case")

        cached = load_cache(str(input_file), "test-case")
        assert cached is None

    def test_mtime_mismatch_invalidates(self, cache_setup, tmp_path):
        input_file = tmp_path / "input.md"
        input_file.write_text("original")

        save_cache(str(input_file), "test-case", [{"a": 1}], 1)

        # Modify file ( change mtime to 2 seconds earlier to ensure mismatch
        import os
        old_mtime = input_file.stat().st_mtime - 2
        input_file.write_text("modified")
        os.utime(str(input_file), (old_mtime, old_mtime))

        cached = load_cache(str(input_file), "test-case")
        assert cached is None

    def test_clean_stale_caches(self, cache_setup, tmp_path):
        cache_dir = tmp_path / CACHE_DIR
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Create a stale cache file (8 days old)
        stale = cache_dir / "stale.test-case.json"
        stale.write_text("{}")
        # Set mtime to 8 days ago
        old_time = time.time() - (8 * 86400)
        import os
        os.utime(str(stale), (old_time, old_time))

        # Create a fresh cache file
        fresh = cache_dir / "fresh.test-case.json"
        fresh.write_text("{}")

        removed = clean_stale_caches()
        assert removed == 1
        assert not stale.exists()
        assert fresh.exists()
