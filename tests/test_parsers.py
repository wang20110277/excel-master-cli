"""Tests for all parsers."""

import json
import pytest
from pathlib import Path

from excel_master.parser import (
    get_parser, auto_detect_format, JSONYAMLParser, MarkdownParser, TextParser,
)


class TestAutoDetect:
    def test_markdown(self):
        assert auto_detect_format("file.md") == "markdown"

    def test_json(self):
        assert auto_detect_format("data.json") == "json"

    def test_yaml(self):
        assert auto_detect_format("data.yaml") == "yaml"
        assert auto_detect_format("data.yml") == "yaml"

    def test_docx(self):
        assert auto_detect_format("doc.docx") == "docx"

    def test_txt(self):
        assert auto_detect_format("notes.txt") == "text"

    def test_unknown_ext(self):
        assert auto_detect_format("file.log") == "text"


class TestJSONParser:
    def test_parse_array(self):
        data = [
            {"id": "TC-001", "title": "Login test"},
            {"id": "TC-002", "title": "Logout test"},
        ]
        parser = JSONYAMLParser()
        result = parser.parse(json.dumps(data), source="test.json")
        assert len(result.records) == 2
        assert result.records[0]["title"] == "Login test"

    def test_parse_object_with_records(self):
        data = {"title": "Test Suite", "records": [{"id": "1", "title": "Test"}]}
        parser = JSONYAMLParser()
        result = parser.parse(json.dumps(data), source="test.json")
        assert result.meta["title"] == "Test Suite"
        assert len(result.records) == 1

    def test_parse_single_object(self):
        data = {"id": "1", "title": "Single"}
        parser = JSONYAMLParser()
        result = parser.parse(json.dumps(data), source="test.json")
        assert len(result.records) == 1
        assert result.records[0]["title"] == "Single"

    def test_invalid_json(self):
        parser = JSONYAMLParser()
        result = parser.parse("{invalid", source="bad.json")
        assert len(result.records) == 0

    def test_non_dict_items_skipped(self):
        data = [{"id": "1"}, "not a dict", 42]
        parser = JSONYAMLParser()
        result = parser.parse(json.dumps(data), source="test.json")
        assert len(result.records) == 1


class TestYAMLParser:
    def test_parse_yaml_array(self, tmp_path):
        content = "- id: TC-001\n  title: Login\n- id: TC-002\n  title: Logout\n"
        parser = get_parser("yaml")
        result = parser.parse(content, source="test.yaml")
        assert len(result.records) == 2

    def test_parse_yaml_with_records_key(self):
        content = "title: My Suite\nrecords:\n  - id: 1\n    title: Test\n"
        parser = get_parser("yaml")
        result = parser.parse(content, source="test.yaml")
        assert result.meta["title"] == "My Suite"
        assert len(result.records) == 1


class TestMarkdownParser:
    def test_parse_table(self):
        content = "# Test Cases\n\n| 用例编号 | 用例标题 | 优先级 |\n|---|---|---|\n| TC-001 | 登录测试 | 高 |\n| TC-002 | 登出测试 | 中 |\n"
        parser = MarkdownParser()
        result = parser.parse(content, source="test.md")
        assert result.meta["title"] == "Test Cases"
        assert len(result.records) == 2
        assert result.records[0]["用例编号"] == "TC-001"

    def test_heading_as_module(self):
        content = "# Tests\n\n## 登录模块\n\n| 编号 | 标题 |\n|---|---|\n| 1 | Login |\n"
        parser = MarkdownParser()
        result = parser.parse(content, source="test.md")
        assert result.records[0]["module"] == "登录模块"

    def test_list_items(self):
        content = "- **标题**: Login test\n- **优先级**: 高\n\n---\n\n- **标题**: Logout test\n- **优先级**: 中\n"
        parser = MarkdownParser()
        result = parser.parse(content, source="test.md")
        assert len(result.records) == 2


class TestTextParser:
    def test_key_value_blocks(self):
        content = "标题: Login test\n优先级: 高\n\n---\n\n标题: Logout test\n优先级: 中"
        parser = TextParser()
        result = parser.parse(content, source="test.txt")
        assert len(result.records) == 2
        assert result.records[0]["标题"] == "Login test"

    def test_colon_cn(self):
        content = "标题：Login test\n优先级：高"
        parser = TextParser()
        result = parser.parse(content, source="test.txt")
        assert result.records[0]["标题"] == "Login test"

    def test_empty_block_skipped(self):
        content = "\n\n\n"
        parser = TextParser()
        result = parser.parse(content, source="empty.txt")
        assert len(result.records) == 0
