"""Plain text parser."""

from __future__ import annotations

import re
from typing import Any

from .base import BaseParser, ParseResult, register_parser


class TextParser(BaseParser):
    """Parse plain text input into records using keyword extraction."""

    format_name = "text"

    def parse(self, content: str, source: str = "") -> ParseResult:
        result = ParseResult(source=source, fmt="text")

        blocks = re.split(r"\n---\n|\n{2,}", content)
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            record = self._extract_fields(block)
            if record:
                result.add_record(record)
            else:
                result.warn(f"Skipping unparseable block: {block[:80]}...")

        return result

    def _extract_fields(self, block: str) -> dict[str, Any]:
        """Extract fields from a text block using common patterns."""
        record: dict[str, Any] = {}

        # Key-value patterns: "key：value" or "key: value"
        for line in block.splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.match(r"^(.+?)\s*[:：]\s*(.+)$", line)
            if m:
                record[m.group(1).strip()] = m.group(2).strip()

        return record


register_parser("text", TextParser)
