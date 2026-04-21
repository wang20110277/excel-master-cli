"""Template registry - discovers built-in and user-defined templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .loader import Template, TemplateLoader, TemplateSchema


class TemplateRegistry:
    """Discover and manage templates."""

    def __init__(self):
        self._builtin_dir = Path(__file__).parent.parent / "assets" / "templates"
        self._builtin_schemas = Path(__file__).parent / "schemas"
        self._user_dir = Path.home() / ".epm" / "templates"

    def list_templates(self) -> list[dict[str, Any]]:
        """List all available templates (built-in + user-defined)."""
        templates: dict[str, dict[str, Any]] = {}

        # Built-in templates
        for schema_file in sorted(self._builtin_schemas.glob("*.yaml")):
            try:
                schema = TemplateLoader.load_schema(schema_file)
                templates[schema.name] = {
                    "name": schema.name,
                    "display_name": schema.display_name,
                    "description": schema.description,
                    "source": "built-in",
                }
            except Exception:
                pass

        # User-defined templates (override built-in with same name)
        if self._user_dir.exists():
            for name_dir in sorted(self._user_dir.iterdir()):
                if not name_dir.is_dir():
                    continue
                schema_path = name_dir / "schema.yaml"
                xlsx_path = name_dir / "template.xlsx"
                if schema_path.exists():
                    try:
                        schema = TemplateLoader.load_schema(schema_path)
                        templates[name_dir.name] = {
                            "name": name_dir.name,
                            "display_name": schema.display_name,
                            "description": schema.description,
                            "source": "user",
                        }
                    except Exception:
                        if xlsx_path.exists():
                            templates[name_dir.name] = {
                                "name": name_dir.name,
                                "display_name": name_dir.name,
                                "description": "",
                                "source": "user",
                            }

        return list(templates.values())

    def get_template(self, name: str) -> Template:
        """Load a template by name. User templates override built-in."""
        # Check user templates first
        user_xlsx = self._user_dir / name / "template.xlsx"
        user_schema = self._user_dir / name / "schema.yaml"
        if user_xlsx.exists() and user_schema.exists():
            return TemplateLoader.load(user_xlsx, user_schema)

        # Fall back to built-in
        builtin_xlsx = self._builtin_dir / f"{name}.xlsx"
        builtin_schema = self._builtin_schemas / f"{name}.yaml"
        if builtin_xlsx.exists() and builtin_schema.exists():
            return TemplateLoader.load(builtin_xlsx, builtin_schema)

        raise ValueError(f"Template not found: {name}")

    def get_schema(self, name: str) -> TemplateSchema:
        """Load just the schema for a template."""
        return self.get_template(name).schema
