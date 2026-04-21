## Context

当前没有统一的工具能将结构化文档（Markdown/Word/JSON 等）快速转换为格式规范的 Excel 文件。团队在生成测试用例、需求追踪矩阵、项目计划等文档时，需要手动在 Excel 中排版，效率低下且容易出错。

本项目构建一个 Python CLI 工具 `epm`，核心流水线：**输入文件 → Parser → Renderer → 输出 .xlsx**。主要面向 AI Agent 通过 skill 文件调用，同时支持人类直接使用。

## Goals / Non-Goals

**Goals:**

- 提供简洁的 CLI 接口，支持多格式输入到 Excel 的一键转换
- 内置常用模板（测试用例、需求追踪、项目计划），开箱即用
- 支持用户自定义模板扩展，通过 `template-init` 初始化
- 实现解析中断续接，处理大文件时具备容错能力
- 为 AI Agent 提供清晰的 skill 集成文档

**Non-Goals:**

- 不做 Excel 到文档的反向转换
- 不做 GUI 或 Web 界面
- 不支持 `.xls` 旧格式，仅 `.xlsx`
- 不做 Excel 公式计算或图表生成
- 不做多语言国际化（界面语言为中文）

## Decisions

### D1: CLI 框架选择 Click

**选择**: Click（而非 argparse、typer）

**理由**: Click 装饰器风格代码简洁，支持子命令、参数验证、帮助文本自动生成。相比 typer 不引入额外类型依赖，相比 argparse 减少样板代码。

### D2: 统一内部数据结构

**选择**: 所有解析器输出相同格式的 `{meta, records}` dict

**理由**: 解耦解析层与渲染层，任何格式输入都映射到统一结构，渲染层只需处理一种数据格式。便于后续扩展新格式（只需新增解析器）。

### D3: Schema-driven 渲染

**选择**: 每个模板配套 YAML schema 定义字段映射规则

**理由**: schema 声明式定义字段映射、默认值、校验规则，渲染引擎通用化。新增模板只需新增 schema + xlsx 模板文件，无需改动渲染代码。

### D4: 模板双层结构（xlsx + schema.yaml）

**选择**: Excel 模板只负责样式，YAML schema 负责数据映射逻辑

**理由**: 样式和数据逻辑分离。用户修改模板时只需关注 Excel 样式，字段映射通过 YAML 配置，降低定制门槛。

### D5: Cache 基于文件内容 hash

**选择**: Cache 文件名包含 `<input-hash>.<template>.json`，存储解析进度

**理由**: 同一输入文件内容变化时自动失效，无需手动管理。mtime 变更也作为失效条件，双重保障。

### D6: 项目结构采用 src layout

**选择**: `src/excel_master/` 而非顶层包目录

**理由**: src layout 防止意外导入未安装的本地代码，是 Python 打包的推荐实践。通过 `pyproject.toml` 定义入口点。

## Risks / Trade-offs

- **[复杂文档解析不准]** → Markdown/纯文本解析依赖启发式规则，对于非标准格式可能提取失败。缓解：容错跳过 + warning 输出，用户可调整输入格式。
- **[Word 文档格式多样性]** → python-docx 提取依赖文档结构一致性，复杂排版可能丢失信息。缓解：以表格为主要提取来源，段落作为补充。
- **[模板样式继承复杂度]** → openpyxl 样式对象需逐属性复制。缓解：仅继承核心样式（字体、边框、对齐），不复制条件格式等高级特性。
- **[大文件内存占用]** → openpyxl 默认将整个工作簿加载到内存。缓解：当前面向单工作表场景，单次数据量有限；后续可切换 openpyxl read_only/write_only 模式。
