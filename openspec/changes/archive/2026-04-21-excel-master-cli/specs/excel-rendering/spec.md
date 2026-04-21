## ADDED Requirements

### Requirement: Excel rendering pipeline
The system SHALL render Excel files by loading the template `.xlsx` for styles, loading the schema `.yaml` for field mapping, then iterating over records to fill data rows.

#### Scenario: Full render cycle
- **WHEN** `epm create` is called with a valid template and parsed records
- **THEN** system loads template xlsx, maps each record to a row per schema, applies styles, and writes the output file

### Requirement: Data row style inheritance
Data rows SHALL inherit the header row's styles: font (name, size, bold, color), border (style, sides), alignment (horizontal, vertical, wrap), and fill/background color. The header row's bold property SHALL NOT be inherited.

#### Scenario: Inherit cell styles
- **WHEN** the template header row uses "Microsoft YaHei" font, thin borders, and center alignment
- **THEN** all data rows use the same font, borders, and alignment, but with bold=False

### Requirement: Multiline cell handling
For columns marked `multiline: true` in the schema, the system SHALL preserve newlines in cell content and auto-adjust the row height to fit the content.

#### Scenario: Render multiline content
- **WHEN** a record's `steps` field (multiline: true) contains "1. Step one\n2. Step two\n3. Step three"
- **THEN** the cell displays all lines and the row height is adjusted to fit

### Requirement: Auto-generated field values
For columns with `auto_generate: true`, the system SHALL generate sequential identifiers when the record does not provide a value. The format SHALL be a prefix derived from the template name plus a zero-padded number.

#### Scenario: Auto-generate test case IDs
- **WHEN** records lack the `id` field and the schema has `auto_generate: true` for that column
- **THEN** system assigns TC-001, TC-002, TC-003, etc.

### Requirement: Field value validation
For columns with a `validate` list, the system SHALL check record values against the allowed set. Invalid values SHALL trigger a warning and be replaced with the column's `default` if available.

#### Scenario: Validate priority value
- **WHEN** a record has `priority: "紧急"` but schema validates `[高, 中, 低]`
- **THEN** system prints a warning and uses the default value "中"

#### Scenario: Valid value passes
- **WHEN** a record has `priority: "高"` and schema validates `[高, 中, 低]`
- **THEN** system accepts the value without warning

### Requirement: Output file writing
The system SHALL write the rendered workbook to the path specified by `--output`, defaulting to `./output.xlsx`. The file SHALL be a valid `.xlsx` file openable in Excel, WPS, and LibreOffice Calc.

#### Scenario: Write to default path
- **WHEN** `--output` is not specified
- **THEN** system writes to `./output.xlsx`

#### Scenario: Write to custom path
- **WHEN** `--output /tmp/result.xlsx` is specified
- **THEN** system writes to `/tmp/result.xlsx`

### Requirement: Required field enforcement
For columns marked `required: true` in the schema, the system SHALL warn when a record is missing that field and has no `default` or `auto_generate` fallback.

#### Scenario: Missing required field without fallback
- **WHEN** a record lacks the `title` field (required: true, no default, no auto_generate)
- **THEN** system prints a warning indicating the record is missing a required field
