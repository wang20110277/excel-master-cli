"""JSON and YAML parser."""

from __future__ import annotations

import json
from typing import Any

import yaml

from .base import BaseParser, ParseResult, register_parser


class JSONYAMLParser(BaseParser):
    """Parse JSON or YAML input into records."""

    format_name = "json_yaml"

    def parse(self, content: str, source: str = "") -> ParseResult:
        fmt = "json" if source.endswith(".json") else "yaml"
        result = ParseResult(source=source, fmt=fmt)

        try:
            if fmt == "json":
                data = json.loads(content)
            else:
                data = yaml.safe_load(content)
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            result.warn(f"Failed to parse {fmt}: {e}")
            return result

        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            if "records" in data:
                records = data["records"]
                if "title" in data:
                    result.meta["title"] = data["title"]
            else:
                records = [data]
        else:
            result.warn(f"Unexpected top-level type: {type(data).__name__}")
            return result

        for i, item in enumerate(records):
            if isinstance(item, dict):
                result.add_record(item)
            else:
                result.warn(f"Skipping non-dict record at index {i}")

        return result


register_parser("json", JSONYAMLParser)
register_parser("yaml", JSONYAMLParser)
