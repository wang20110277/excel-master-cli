## ADDED Requirements

### Requirement: Unified internal data structure
All parsers SHALL output a unified dict with `meta` and `records` keys. `meta` SHALL contain `source`, `format`, and `title`. `records` SHALL be a list of dicts with field keys matching the schema column `field` names.

#### Scenario: Parser output structure
- **WHEN** any parser processes a valid input file
- **THEN** the output SHALL be `{"meta": {"source": str, "format": str, "title": str}, "records": [dict, ...]}`

### Requirement: Markdown parser
The system SHALL parse Markdown input by mapping heading hierarchy to module groups, Markdown tables to records, and list items to field values.

#### Scenario: Parse Markdown table
- **WHEN** input Markdown contains a table with headers matching schema field keywords
- **THEN** system extracts each table row as a record with fields mapped by column headers

#### Scenario: Parse Markdown with heading groups
- **WHEN** input Markdown uses `##` headings as module names followed by content
- **THEN** system groups records under the appropriate `module` field derived from the heading

### Requirement: Plain text parser
The system SHALL parse plain text input by splitting on `---` separators or blank lines into blocks, then extracting key fields via keyword-based regex matching.

#### Scenario: Parse delimited text blocks
- **WHEN** input text contains records separated by `---` or blank lines
- **THEN** system splits into blocks and extracts fields using schema-defined keywords

#### Scenario: Extract fields by keywords
- **WHEN** a text block contains lines like "优先级：高" or "priority: high"
- **THEN** system maps the value to the `priority` field based on schema extract keywords

### Requirement: Word document parser
The system SHALL parse Word (.docx) files using python-docx, extracting tables as record sources and heading paragraphs as module groups.

#### Scenario: Parse Word table
- **WHEN** a .docx file contains a table with column headers matching schema fields
- **THEN** system extracts each table row as a record

#### Scenario: Parse Word with heading groups
- **WHEN** a .docx file uses heading styles (Heading 1, Heading 2) for module names
- **THEN** system maps heading text to the `module` field for subsequent records

### Requirement: JSON/YAML parser
The system SHALL parse JSON and YAML input by treating the top-level structure as a records array. Field names SHALL be automatically mapped to schema column field names.

#### Scenario: Parse JSON array
- **WHEN** input is a JSON file containing an array of objects
- **THEN** system treats each object as a record, mapping keys to schema fields

#### Scenario: Parse YAML with records key
- **WHEN** input YAML contains a `records` key with a list
- **THEN** system extracts the list as records array

### Requirement: Parser fault tolerance
Parsers SHALL NOT abort on unrecognized content. Unparseable records SHALL be skipped with a warning printed to stderr. Valid records SHALL still be returned.

#### Scenario: Skip malformed record
- **WHEN** input contains a record that cannot be mapped to any schema field
- **THEN** system prints a warning to stderr and skips that record, continuing with remaining records

#### Scenario: Partial parsing success
- **WHEN** input has 10 records but 2 are malformed
- **THEN** system returns 8 valid records and prints 2 warnings
