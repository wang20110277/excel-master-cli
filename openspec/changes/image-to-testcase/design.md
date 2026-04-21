## Context

excel-master-cli 当前支持 Markdown、Text、Word、JSON、YAML 五种输入格式。用户有大量以截图形式保存的产品功能说明需要转为测试用例。

Agent（如 Claude Code）自带多模态视觉能力，可直接读取和分析图片内容，无需调用外部 AI API。

## Goals / Non-Goals

**Goals:**
- 新增 `image` 解析器，扫描文件夹中的图片文件
- agent 通过自身视觉能力读取图片后，将识别结果写入临时 JSON 文件，CLI 解析该 JSON 生成测试用例记录
- 工作流简洁：agent 读图 → 生成 JSON → CLI 生成 Excel

**Non-Goals:**
- 不在 CLI 内部集成外部 AI API
- 不做图片 OCR 纯本地方案
- 不做实时交互式 AI 对话

## Decisions

### 1. 使用 agent 视觉能力 + JSON 中间格式

**选择**: agent（Claude Code）通过 Read 工具直接查看图片，生成结构化 JSON 数据，写入临时文件，CLI 的 `image` 解析器读取该 JSON 文件。

**工作流**:
1. 用户指定图片文件夹路径
2. agent 逐张读取图片，用视觉能力分析内容
3. agent 生成 JSON 格式的测试用例数据，写入临时文件
4. CLI `create` 命令使用 `image` 解析器读取该 JSON 文件，渲染 Excel

**理由**: 零配置、零外部依赖，直接利用 agent 已有的视觉能力。

### 2. ImageParser 读取 agent 生成的 JSON

**选择**: `ImageParser` 解析 JSON 文件，格式为 `[{module, title, steps, expected, ...}, ...]`，直接映射为 `ParseResult.records`。

**理由**: JSON 格式灵活，字段名可与 YAML schema 的 `field` 或 `header` 对齐，复用现有的值解析逻辑。

### 3. CLI 支持 `--input` 指向图片文件夹

**选择**: `--input` 接收文件夹路径时，agent 先生成 JSON 中间文件，CLI 再解析。命令示例：
```
epm create -t test-case -i ./screenshots -f image -o output.xlsx
```

ImageParser 检查输入路径：
- 如果是 JSON 文件：直接解析
- 如果是文件夹：提示需要先生成 JSON 中间文件

## Risks / Trade-offs

- **需要 agent 参与** → 图片识别不自动化，需 agent 会话中执行；可通过脚本封装实现半自动化
- **JSON 格式需对齐模板** → 在 prompt 中明确要求字段名匹配 test-case 模板
