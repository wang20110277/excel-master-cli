## ADDED Requirements

### Requirement: Cache persistence during parsing
During record parsing, the system SHALL periodically persist already-parsed records to a cache file at `.epm-cache/<input-hash>.<template>.json`. The cache SHALL contain `input_file`, `input_mtime`, `template`, `processed_offset`, and `records`.

#### Scenario: Write cache after parsing
- **WHEN** system has parsed 50 of 100 records
- **THEN** a cache file exists at `.epm-cache/<hash>.test-case.json` containing the 50 parsed records and the processing offset

### Requirement: Automatic resume from cache
When `epm create` is invoked and a valid cache file exists for the same input and template, the system SHALL resume parsing from the cached offset instead of starting over.

#### Scenario: Resume interrupted parsing
- **WHEN** previous run was interrupted after parsing 50 records, and user runs `epm create` again with the same input and template
- **THEN** system loads the 50 cached records and continues parsing from record 51

#### Scenario: Cache mtime mismatch
- **WHEN** the input file's mtime has changed since cache creation
- **THEN** system ignores the cache and re-parses from the beginning

### Requirement: Cache cleanup on completion
After successful Excel generation, the system SHALL delete the corresponding cache file.

#### Scenario: Cache deleted after success
- **WHEN** `epm create` completes successfully
- **THEN** the cache file for that input+template combination is removed

### Requirement: Forced clean start
The `--clean` flag SHALL cause the system to ignore any existing cache and process the input from the beginning.

#### Scenario: Clean flag ignores cache
- **WHEN** user runs `epm create --clean --template test-case --input file.md`
- **THEN** system skips cache lookup and parses the entire input from scratch

### Requirement: Stale cache auto-cleanup
Cache files older than 7 days SHALL be automatically cleaned up at the start of any `epm` command execution.

#### Scenario: Auto-clean old cache
- **WHEN** a cache file is older than 7 days and user runs any `epm` command
- **THEN** system deletes the stale cache file during startup
