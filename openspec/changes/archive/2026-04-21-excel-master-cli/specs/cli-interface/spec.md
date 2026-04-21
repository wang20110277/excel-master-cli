## ADDED Requirements

### Requirement: CLI entry point and version
The system SHALL provide a `epm` command as the CLI entry point. The command SHALL support `--version` flag to display the current version and `-h` for help.

#### Scenario: Display version
- **WHEN** user runs `epm --version`
- **THEN** system prints the version string and exits

#### Scenario: Display help
- **WHEN** user runs `epm -h`
- **THEN** system prints usage information including all available subcommands

### Requirement: create command
The system SHALL provide a `epm create` command that generates an Excel file from an input document. The command SHALL accept `--template`, `--input`, `--output`, `--format`, `--resume`, and `--clean` options.

#### Scenario: Create Excel from file input
- **WHEN** user runs `epm create --template test-case --input cases.md`
- **THEN** system parses the input file, applies the template, and writes output to `./output.xlsx`

#### Scenario: Create Excel with custom output path
- **WHEN** user runs `epm create --template requirements --input req.json --output /path/to/result.xlsx`
- **THEN** system writes the generated Excel to the specified output path

#### Scenario: Create Excel from stdin
- **WHEN** user pipes data with `--input -` and `--format json`
- **THEN** system reads from stdin and processes the input

#### Scenario: Missing required template
- **WHEN** user runs `epm create --input file.md` without `--template`
- **THEN** system exits with an error message indicating template is required

#### Scenario: Clean restart
- **WHEN** user runs `epm create --template test-case --input file.md --clean`
- **THEN** system ignores any existing cache and processes from the beginning

### Requirement: list-templates command
The system SHALL provide a `epm list-templates` command that displays all available templates (built-in and user-defined).

#### Scenario: List all templates
- **WHEN** user runs `epm list-templates`
- **THEN** system prints a table of template names, display names, and descriptions, including both built-in and user-defined templates

### Requirement: show-schema command
The system SHALL provide a `epm show-schema <template>` command that displays the input data structure required by a specific template.

#### Scenario: Show template schema
- **WHEN** user runs `epm show-schema test-case`
- **THEN** system prints the YAML schema for the test-case template including field names, headers, types, and validation rules

#### Scenario: Unknown template
- **WHEN** user runs `epm show-schema nonexistent`
- **THEN** system exits with an error indicating the template was not found

### Requirement: template-init command
The system SHALL provide a `epm template-init <name>` command that initializes a custom template directory at `~/.epm/templates/<name>/` with a scaffold `template.xlsx` and `schema.yaml`.

#### Scenario: Initialize custom template
- **WHEN** user runs `epm template-init my-report`
- **THEN** system creates `~/.epm/templates/my-report/` with `template.xlsx` and `schema.yaml` files

#### Scenario: Template already exists
- **WHEN** user runs `epm template-init my-report` and the directory already exists
- **THEN** system exits with an error indicating the template already exists

### Requirement: Input format auto-detection
The system SHALL auto-detect input format by file extension: `.md` → Markdown, `.docx` → Word, `.json` → JSON, `.yaml/.yml` → YAML, others → plain text. For stdin input, the `--format` option SHALL be required.

#### Scenario: Auto-detect markdown
- **WHEN** user provides `--input data.md` without `--format`
- **THEN** system treats the input as Markdown format

#### Scenario: Stdin requires explicit format
- **WHEN** user provides `--input -` without `--format`
- **THEN** system exits with an error indicating format must be specified for stdin
