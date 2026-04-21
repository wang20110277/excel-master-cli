## Why

需要一个 CLI 工具将结构化文档（Markdown/文本/Word/JSON/YAML）转换为格式化的 Excel 文档。目前没有统一的方式从文档输入快速生成符合模板规范的测试用例、需求追踪矩阵、项目计划等 Excel 文件。该工具主要面向 AI Agent 集成（通过 skill 文件），同时支持人类直接命令行使用。

## What Changes

- 新增 `epm` CLI 工具，基于 click 框架，支持 `create`、`list-templates`、`show-schema`、`template-init` 命令
- 新增多格式解析层：Markdown、纯文本、Word(.docx)、JSON、YAML 输入解析，统一输出内部 dict 结构
- 新增模板系统：内置 3 个模板（test-case/requirements/project-plan），支持用户自定义模板扩展
- 新增 Excel 渲染引擎：基于 openpyxl，按 schema 映射字段填充模板
- 新增中断续接机制：基于文件 hash 的 cache 系统，支持断点续传
- 新增 AI Agent skill 集成文件（excel-master-skill/skill.md）

## Capabilities

### New Capabilities

- `cli-interface`: CLI 命令定义与入口，包括 create、list-templates、show-schema、template-init 命令及参数处理
- `input-parsing`: 多格式输入解析层，将 Markdown/文本/Word/JSON/YAML 转换为统一内部数据结构
- `template-system`: 模板加载、注册发现、schema 字段映射、内置模板及用户自定义模板管理
- `excel-rendering`: 基于 openpyxl 的 Excel 渲染引擎，按 schema 填充数据并继承模板样式
- `cache-resume`: 解析过程中断续接，基于文件 hash 的 cache 持久化与自动清理

### Modified Capabilities

（无已有能力变更）

## Impact

- **新增代码**: `src/excel_master/` 下完整的 Python 包结构，约 15+ 源文件
- **新增依赖**: click、openpyxl、python-docx、PyYAML、pytest
- **Python 版本**: 要求 3.10+
- **文件系统**: 使用 `~/.epm/templates/` 存放用户自定义模板，`.epm-cache/` 存放续接缓存
- **包管理**: pyproject.toml 定义入口点 `epm = "excel_master.cli:main"`
