"""Markdown parser."""

from __future__ import annotations

import re
from typing import Any

from .base import BaseParser, ParseResult, register_parser


class MarkdownParser(BaseParser):
    """Parse Markdown input into records."""

    format_name = "markdown"

    def parse(self, content: str, source: str = "") -> ParseResult:
        result = ParseResult(source=source, fmt="markdown")
        lines = content.split("\n")

        title = ""
        current_module = ""
        records: list[dict[str, Any]] = []

        # Extract title from first heading
        for line in lines:
            m = re.match(r"^#\s+(.+)", line)
            if m:
                title = m.group(1).strip()
                break
        result.meta["title"] = title

        # Parse tables
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Heading as module group
            heading = re.match(r"^#{1,4}\s+(.+)", line)
            if heading:
                current_module = heading.group(1).strip()
                i += 1
                continue

            # Table detection
            if "|" in line and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|", lines[i + 1].strip()):
                headers, table_records = self._parse_table(lines, i, current_module)
                records.extend(table_records)
                # Skip past the table
                while i < len(lines) and "|" in lines[i]:
                    i += 1
                continue

            i += 1

        # Also parse list-item records if no tables found
        if not records:
            records = self._parse_list_items(content)

        for rec in records:
            result.add_record(rec)

        return result

    def _parse_table(self, lines: list[str], start: int, module: str) -> tuple[list[str], list[dict[str, Any]]]:
        """Parse a Markdown table starting at `start`."""
        headers = self._split_table_row(lines[start])
        records = []
        i = start + 2  # skip header + separator
        while i < len(lines) and "|" in lines[i]:
            values = self._split_table_row(lines[i])
            record: dict[str, Any] = {}
            for j, h in enumerate(headers):
                if j < len(values):
                    record[h] = values[j].strip()
            if module:
                record.setdefault("module", module)
                record.setdefault("所属模块", module)
            if record:
                records.append(record)
            i += 1
        return headers, records

    def _split_table_row(self, line: str) -> list[str]:
        cells = line.strip().strip("|").split("|")
        return [c.strip() for c in cells]

    def _parse_list_items(self, content: str) -> list[dict[str, Any]]:
        """Parse list-item style records separated by blank lines or ---."""
        records: list[dict[str, Any]] = []
        blocks = re.split(r"\n(?:---|\s*)\n", content)
        for block in blocks:
            record: dict[str, Any] = {}
            for line in block.strip().splitlines():
                m = re.match(r"[-*]\s+\*\*(.+?)\*\*[:：]\s*(.*)", line)
                if m:
                    record[m.group(1)] = m.group(2).strip()
                    continue
                m = re.match(r"[-*]\s+(.+?)[:：]\s*(.*)", line)
                if m:
                    record[m.group(1)] = m.group(2).strip()
            if record:
                records.append(record)
        return records


register_parser("markdown", MarkdownParser)
