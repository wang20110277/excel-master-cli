"""Tests for CLI commands."""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from excel_master.cli import main


@pytest.fixture
def runner():
    return CliRunner()


class TestVersion:
    def test_version(self, runner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestListTemplates:
    def test_list_templates(self, runner):
        result = runner.invoke(main, ["list-templates"])
        assert result.exit_code == 0
        assert "test-case" in result.output
        assert "requirements" in result.output
        assert "project-plan" in result.output


class TestShowSchema:
    def test_show_schema(self, runner):
        result = runner.invoke(main, ["show-schema", "test-case"])
        assert result.exit_code == 0
        assert "用例编号" in result.output
        assert "auto_generate" in result.output

    def test_unknown_template(self, runner):
        result = runner.invoke(main, ["show-schema", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output


class TestCreate:
    def test_create_from_json(self, runner, tmp_path):
        input_file = tmp_path / "data.json"
        output_file = tmp_path / "output.xlsx"
        input_file.write_text(json.dumps([
            {"title": "Login test", "module": "Auth", "expected": "Success", "priority": "高"},
        ]))

        result = runner.invoke(main, [
            "create", "--template", "test-case",
            "--input", str(input_file),
            "--output", str(output_file),
        ])
        assert result.exit_code == 0
        assert output_file.exists()
        assert "Generated" in result.output

    def test_create_from_markdown(self, runner, tmp_path):
        input_file = tmp_path / "data.md"
        output_file = tmp_path / "out.xlsx"
        input_file.write_text(
            "# Tests\n\n"
            "| 用例编号 | 用例标题 | 所属模块 | 优先级 | 预期结果 |\n"
            "|---|---|---|---|---|\n"
            "| TC-001 | Login | Auth | 高 | OK |\n"
        )

        result = runner.invoke(main, [
            "create", "--template", "test-case",
            "--input", str(input_file),
            "--output", str(output_file),
        ])
        assert result.exit_code == 0
        assert output_file.exists()

    def test_create_from_stdin(self, runner, tmp_path):
        output_file = tmp_path / "out.xlsx"
        data = json.dumps([{"title": "Test", "module": "M1", "expected": "R1"}])

        result = runner.invoke(main, [
            "create", "--template", "test-case",
            "--input", "-",
            "--format", "json",
            "--output", str(output_file),
        ], input=data)
        assert result.exit_code == 0
        assert output_file.exists()

    def test_create_stdin_without_format(self, runner, tmp_path):
        output_file = tmp_path / "out.xlsx"
        result = runner.invoke(main, [
            "create", "--template", "test-case",
            "--input", "-",
            "--output", str(output_file),
        ], input="{}")
        assert result.exit_code == 1

    def test_create_missing_template(self, runner, tmp_path):
        input_file = tmp_path / "data.json"
        input_file.write_text("[]")

        result = runner.invoke(main, [
            "create", "--template", "nonexistent",
            "--input", str(input_file),
        ])
        assert result.exit_code == 1


class TestTemplateInit:
    def test_template_init(self, runner, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        result = runner.invoke(main, ["template-init", "my-report"])
        assert result.exit_code == 0
        assert (tmp_path / ".epm" / "templates" / "my-report" / "template.xlsx").exists()
        assert (tmp_path / ".epm" / "templates" / "my-report" / "schema.yaml").exists()

    def test_template_init_already_exists(self, runner, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        # Create first
        runner.invoke(main, ["template-init", "my-report"])
        # Try again
        result = runner.invoke(main, ["template-init", "my-report"])
        assert result.exit_code == 1
        assert "already exists" in result.output
