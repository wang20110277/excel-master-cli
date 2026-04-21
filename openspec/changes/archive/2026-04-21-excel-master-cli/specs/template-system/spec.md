## ADDED Requirements

### Requirement: Template composition
Each template SHALL consist of two files: an Excel template file (`.xlsx`) defining styles (headers, fonts, borders, backgrounds, row heights, column widths, frozen first row) and a YAML schema file defining field mapping rules.

#### Scenario: Load template pair
- **WHEN** system loads template "test-case"
- **THEN** it reads both `test-case.xlsx` (styles) and `test-case.yaml` (field mapping)

### Requirement: Schema YAML structure
Each schema YAML SHALL define: `name`, `display_name`, `description`, and `columns`. Each column SHALL define `field`, `header`, `width`, and optionally `required`, `default`, `validate`, `auto_generate`, `multiline`, and `extract`.

#### Scenario: Schema column with validation
- **WHEN** a column defines `validate: [高, 中, 低]`
- **THEN** system SHALL reject record values not in this list and use the `default` if the field is missing

#### Scenario: Schema column with auto_generate
- **WHEN** a column defines `auto_generate: true`
- **THEN** system SHALL automatically assign sequential IDs (e.g., TC-001, TC-002) if the field is missing from the record

#### Scenario: Schema column with extract keywords
- **WHEN** a column defines `extract: [{keywords: [优先级, priority]}]`
- **THEN** text parser SHALL use these keywords to extract field values from unstructured input

### Requirement: Built-in templates
The system SHALL include three built-in templates: `test-case` (测试用例), `requirements` (需求追踪矩阵), `project-plan` (项目计划表). Each SHALL have a corresponding `.xlsx` and `.yaml` file in `assets/templates/` and `template/schemas/`.

#### Scenario: List built-in templates
- **WHEN** user runs `epm list-templates`
- **THEN** output includes test-case, requirements, and project-plan templates

### Requirement: Template registry and discovery
The system SHALL maintain a template registry that discovers templates from both built-in (`assets/templates/`) and user-defined (`~/.epm/templates/`) locations. User-defined templates with the same name SHALL override built-in templates.

#### Scenario: Discover user template
- **WHEN** `~/.epm/templates/my-report/` contains `template.xlsx` and `schema.yaml`
- **THEN** `epm list-templates` includes "my-report" in the output

#### Scenario: User template overrides built-in
- **WHEN** user creates a template named "test-case" in `~/.epm/templates/`
- **THEN** `epm create --template test-case` uses the user-defined version instead of the built-in one

### Requirement: Custom template initialization
The `epm template-init <name>` command SHALL create a directory at `~/.epm/templates/<name>/` with a scaffold `template.xlsx` (single header row) and `schema.yaml` (minimal example with documentation comments).

#### Scenario: Initialize new template
- **WHEN** user runs `epm template-init custom-report`
- **THEN** system creates `~/.epm/templates/custom-report/template.xlsx` with a default header row and `~/.epm/templates/custom-report/schema.yaml` with example column definitions

### Requirement: Schema field mapping
The renderer SHALL map record dict keys to Excel columns based on the schema `field` names. Missing fields SHALL be filled with the column's `default` value if defined, otherwise left empty.

#### Scenario: Map record to columns
- **WHEN** a record has `{"id": "TC-001", "title": "Login test", "priority": "高"}`
- **THEN** system maps each key to the corresponding column position per schema

#### Scenario: Fill missing field with default
- **WHEN** a record is missing the `status` field and schema defines `default: 待执行`
- **THEN** system fills the status cell with "待执行"
