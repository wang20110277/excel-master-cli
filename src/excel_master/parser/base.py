"""Base parser and unified output format."""

from __future__ import annotations

import abc
import warnings
from pathlib import Path
from typing import Any


class ParseResult:
    """Unified output format for all parsers."""

    def __init__(self, source: str, fmt: str, title: str = "",
                 records: list[dict[str, Any]] | None = None):
        self.meta = {
            "source": source,
            "format": fmt,
            "title": title,
        }
        self.records: list[dict[str, Any]] = records or []

    def to_dict(self) -> dict[str, Any]:
        return {"meta": self.meta, "records": self.records}

    def add_record(self, record: dict[str, Any]) -> None:
        self.records.append(record)

    def warn(self, msg: str) -> None:
        warnings.warn(f"[{self.meta['source']}] {msg}", stacklevel=2)


class BaseParser(abc.ABC):
    """Abstract base class for all input parsers."""

    format_name: str = ""

    @abc.abstractmethod
    def parse(self, content: str, source: str = "") -> ParseResult:
        """Parse raw content string into a ParseResult."""

    def parse_file(self, path: str | Path) -> ParseResult:
        """Parse a file by reading its content."""
        p = Path(path)
        content = p.read_text(encoding="utf-8")
        return self.parse(content, source=str(p))


# Parser registry
_PARSERS: dict[str, type[BaseParser]] = {}


def register_parser(fmt: str, cls: type[BaseParser]) -> None:
    _PARSERS[fmt] = cls


def get_parser(fmt: str) -> BaseParser:
    cls = _PARSERS.get(fmt)
    if cls is None:
        raise ValueError(f"Unknown format: {fmt}")
    return cls()


def get_supported_formats() -> list[str]:
    return list(_PARSERS.keys())


def auto_detect_format(path: str) -> str:
    """Detect input format from file extension."""
    ext = Path(path).suffix.lower()
    mapping = {
        ".md": "markdown",
        ".txt": "text",
        ".docx": "docx",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
    }
    fmt = mapping.get(ext)
    if fmt is None:
        p = Path(path)
        if p.is_dir():
            fmt = "image"
        else:
            fmt = "text"
    return fmt
