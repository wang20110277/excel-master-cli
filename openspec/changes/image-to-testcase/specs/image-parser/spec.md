## ADDED Requirements

### Requirement: ImageParser supports JSON intermediate format input
系统 SHALL 支持读取 JSON 格式的测试用例数据文件，将其解析为测试用例记录列表。JSON 格式为对象数组，每个对象的字段名对齐目标模板的 `field` 或 `header` 名称。

#### Scenario: Valid JSON input
- **WHEN** 用户提供包含测试用例数据的 JSON 文件
- **THEN** 系统将 JSON 数组解析为记录列表，字段自动匹配模板的 field 和 header

#### Scenario: Invalid JSON input
- **WHEN** JSON 文件格式错误或非数组
- **THEN** 系统输出 warning 并返回空记录列表

### Requirement: ImageParser scans image files from a folder
系统 SHALL 支持将文件夹路径作为输入，扫描其中所有 PNG、JPG、JPEG、BMP 格式的图片文件，按文件名自然排序。

#### Scenario: Folder with images
- **WHEN** 用户提供包含图片的文件夹路径
- **THEN** 系统列出所有支持的图片文件路径供 agent 处理

#### Scenario: Folder with no images
- **WHEN** 文件夹中没有任何支持的图片格式
- **THEN** 系统返回空列表并输出 warning

### Requirement: CLI create command supports image format
CLI 的 `create` 命令 SHALL 支持 `--format image` 选项，接受 JSON 数据文件或图片文件夹路径。

#### Scenario: Create from JSON data file
- **WHEN** 用户执行 `epm create -t test-case -i testcases.json -f image -o output.xlsx`
- **THEN** 系统解析 JSON 文件并生成测试用例 Excel

#### Scenario: Create from image folder
- **WHEN** 用户执行 `epm create -t test-case -i ./screenshots -f image -o output.xlsx`
- **THEN** 系统提示需要 agent 先生成 JSON 中间数据，或直接处理已生成的 JSON 文件
