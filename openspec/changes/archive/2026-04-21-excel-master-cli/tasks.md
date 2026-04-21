## 1. 项目脚手架

- [x] 1.1 创建 `pyproject.toml`，定义项目元数据、Python 3.10+ 要求、依赖（click, openpyxl, python-docx, PyYAML, pytest）和入口点 `epm = "excel_master.cli:main"`
- [x] 1.2 创建 `src/excel_master/__init__.py` 包结构，定义版本号
- [x] 1.3 创建 `tests/` 目录和 `tests/conftest.py` 测试配置
- [x] 1.4 验证 `pip install -e .` 安装成功，`epm --version` 正常输出

## 2. 解析层基础

- [x] 2.1 实现 `src/excel_master/parser/base.py`：定义解析器基类 `BaseParser`、统一输出格式 `{meta, records}`、解析器注册机制
- [x] 2.2 实现 `src/excel_master/parser/json_yaml.py`：JSON/YAML 解析器，支持 records 数组和顶层对象两种输入格式
- [x] 2.3 实现 `src/excel_master/parser/markdown.py`：Markdown 解析器，提取标题分组、表格行、列表项字段
- [x] 2.4 实现 `src/excel_master/parser/text.py`：纯文本解析器，`---`/空行分块 + 关键词正则提取
- [x] 2.5 实现 `src/excel_master/parser/docx.py`：Word 解析器，python-docx 提取表格和标题
- [x] 2.6 为每个解析器编写 pytest 测试，覆盖正常解析、格式变体、容错跳过场景

## 3. 模板系统

- [x] 3.1 创建 `src/excel_master/template/schemas/test-case.yaml`：测试用例 schema（8 列字段定义）
- [x] 3.2 创建 `src/excel_master/template/schemas/requirements.yaml`：需求追踪矩阵 schema
- [x] 3.3 创建 `src/excel_master/template/schemas/project-plan.yaml`：项目计划 schema
- [x] 3.4 使用 openpyxl 创建内置 xlsx 模板：`src/excel_master/assets/templates/test-case.xlsx`（含表头行、样式、冻结首行、列宽）
- [x] 3.5 创建内置 xlsx 模板：`requirements.xlsx` 和 `project-plan.xlsx`
- [x] 3.6 实现 `src/excel_master/template/loader.py`：加载 .xlsx 模板文件 + .yaml schema，返回模板对象
- [x] 3.7 实现 `src/excel_master/template/registry.py`：模板注册/发现，扫描内置 `assets/templates/` + 用户 `~/.epm/templates/`，用户模板覆盖内置

## 4. Excel 渲染引擎

- [x] 4.1 实现 `src/excel_master/renderer/xlsx.py`：渲染引擎核心 — 加载模板、按 schema 映射 records 到行、写入输出文件
- [x] 4.2 实现数据行样式继承：从表头行复制字体、边框、对齐、填充样式（bold 设为 False）
- [x] 4.3 实现 auto_generate 逻辑：为标记字段自动生成序号（如 TC-001、TC-002）
- [x] 4.4 实现 validate 校验：检查字段值是否在允许列表中，无效值替换为 default 并输出 warning
- [x] 4.5 实现 multiline 字段处理：保留换行符并自动调整行高
- [x] 4.6 为渲染引擎编写测试，覆盖样式继承、字段映射、校验、自动编号等场景

## 5. Cache 续接机制

- [x] 5.1 实现 cache 管理模块：cache 文件读写（`.epm-cache/<hash>.<template>.json`），包含 input_file/mtime/template/offset/records
- [x] 5.2 实现自动续接：create 命令启动时检查 cache，mtime 匹配则从 offset 继续
- [x] 5.3 实现 cache 清理：成功完成后删除 cache；启动时清理 7 天以上旧 cache
- [x] 5.4 实现 `--clean` 参数逻辑：跳过 cache 查找，从头解析
- [x] 5.5 为 cache 机制编写测试，覆盖续接、mtime 失效、清理等场景

## 6. CLI 命令层

- [x] 6.1 实现 `src/excel_master/cli.py` 基础框架：click group、`--version`、`-h` 帮助
- [x] 6.2 实现 `epm list-templates` 命令：调用 registry 获取模板列表并格式化输出
- [x] 6.3 实现 `epm show-schema <template>` 命令：加载 schema 并打印字段信息
- [x] 6.4 实现 `epm create` 命令：串联 parser → cache → renderer 完整流程，支持所有参数
- [x] 6.5 实现输入格式自动检测：按文件扩展名映射格式，stdin 要求 `--format`
- [x] 6.6 实现 `epm template-init <name>` 命令：在 `~/.epm/templates/<name>/` 生成 scaffold 文件
- [x] 6.7 为 CLI 命令编写测试（使用 Click CLI test runner），覆盖各命令的正常和错误路径

## 7. AI Agent Skill 文件

- [x] 7.1 创建 `excel-master-skill/skill.md`：Agent 使用说明，覆盖安装检查、使用流程、场景示例、错误处理

## 8. 集成验证

- [x] 8.1 端到端测试：从 Markdown/JSON/YAML 输入生成 test-case Excel，验证输出内容正确
- [x] 8.2 端到端测试：验证 requirements 和 project-plan 模板生成
- [x] 8.3 验证自定义模板流程：`template-init` → 修改 → `create` 使用自定义模板
- [x] 8.4 验证续接流程：中断后重跑，确认 cache 续接正常工作
