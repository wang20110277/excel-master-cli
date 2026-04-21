# Excel Master CLI 设计文档

## 概述

`excel-master-cli` 是一个基于 openpyxl 的 CLI 工具，命令前缀 `epm`。核心功能：根据文档输入（Markdown/文本/Word/JSON/YAML），按内置或自定义 Excel 模板生成结构化 Excel 文档。

主要面向 AI Agent（通过 `excel-master-skill/skill.md` 集成），同时支持人类直接命令行使用。

## 架构

```
输入文件 → Parser(解析为统一dict) → Renderer(读模板+schema+数据→填充) → 输出.xlsx
```

### 项目结构

```
excel-master/
├── excel-master-cli/              # CLI 工具主体
│   ├── pyproject.toml             # 入口点 epm = "excel_master.cli:main"
│   ├── src/
│   │   └── excel_master/
│   │       ├── __init__.py
│   │       ├── cli.py             # click 命令定义
│   │       ├── parser/            # 输入解析层
│   │       │   ├── base.py        # 解析器基类 + 统一输出格式
│   │       │   ├── markdown.py
│   │       │   ├── text.py
│   │       │   ├── docx.py
│   │       │   └── json_yaml.py
│   │       ├── template/          # 模板管理层
│   │       │   ├── loader.py      # 加载 .xlsx 模板 + .yaml schema
│   │       │   ├── registry.py    # 模板注册/发现（内置 + 用户自定义）
│   │       │   └── schemas/       # YAML schema 定义字段映射
│   │       │       ├── test-case.yaml
│   │       │       ├── requirements.yaml
│   │       │       └── project-plan.yaml
│   │       ├── renderer/          # Excel 渲染层
│   │       │   └── xlsx.py        # openpyxl 渲染引擎
│   │       └── assets/
│   │           └── templates/     # 内置 .xlsx 模板文件
│   │               ├── test-case.xlsx
│   │               ├── requirements.xlsx
│   │               └── project-plan.xlsx
│   └── tests/
├── excel-master-skill/            # AI Agent skill
│   └── skill.md                   # Agent 使用说明
```

## CLI 命令接口

```
epm -h                          # 查看帮助
epm --version                   # 查看版本

epm list-templates              # 列出所有可用模板（内置+自定义）
epm show-schema <template>      # 显示某个模板需要的输入数据结构

epm create                      # 核心：生成 Excel
  --template <name>             # 模板名 (test-case / requirements / project-plan)
  --input <file|->              # 输入源：文件路径或 "-" 表示 stdin
  --output <file.xlsx>          # 输出路径，默认 ./output.xlsx
  --format <md|txt|docx|json|yaml>  # 输入格式，默认按扩展名自动检测
  --resume                      # 显式续接（默认行为）
  --clean                       # 忽略 cache，重新开始

epm template-init <name>        # 初始化自定义模板目录到 ~/.epm/templates/<name>/
```

### 自动检测规则

文件扩展名映射：`.md` → Markdown, `.docx` → Word, `.json` → JSON, `.yaml/.yml` → YAML, 其他按纯文本。stdin 输入需 `--format` 指定。

## 解析层

### 统一内部数据结构

所有解析器输出相同格式：

```python
{
    "meta": {
        "source": "input.md",
        "format": "markdown",
        "title": "XX系统测试用例"
    },
    "records": [
        {
            "id": "TC-001",
            "module": "登录模块",
            "title": "正常登录",
            "priority": "高",
            "precondition": "用户已注册",
            "steps": "1. 打开登录页\n2. 输入账号密码\n3. 点击登录",
            "expected": "登录成功，跳转首页",
            "status": "待执行"
        }
    ]
}
```

### 各格式解析策略

| 格式 | 解析策略 |
|------|----------|
| Markdown | 标题层级→模块分组，表格→记录，列表项→字段 |
| 纯文本 | `---` 或空行分块，正则提取关键字段 |
| Word (.docx) | python-docx 提取段落和表格，表格行→记录，标题→模块分组 |
| JSON/YAML | 直接作为 records 数组，字段名自动映射到 schema |

### 容错

解析失败不中断，跳过无法识别的记录并输出 warning。

## 中断续处理

解析过程中将已解析的 records 持久化到 cache 文件，中断后重跑自动续接。

### Cache 机制

- Cache 位置：`.epm-cache/<input-hash>.<template>.json`
- 文件内容：`{input_file, input_mtime, template, processed_offset, records}`
- 完成后自动删除 cache

### Cache 清理策略

- 生成完成后自动删除
- `--clean` 强制忽略重新开始
- 输入文件 mtime 变更 → 自动忽略旧 cache
- 超过 7 天的 cache 自动清理

## 模板系统

### 模板组成

每个模板由两部分组成：
1. **Excel 模板文件**（`.xlsx`）：预定义样式（列头、字体、边框、背景色、行高、列宽、冻结首行），只含表头行
2. **Schema YAML**：定义字段映射规则

### Schema YAML 示例（test-case）

```yaml
name: test-case
display_name: 测试用例
description: 软件测试用例文档
columns:
  - field: id
    header: 用例编号
    width: 12
    required: true
    auto_generate: true
  - field: module
    header: 所属模块
    width: 15
    required: true
    extract:
      - keywords: [模块, module, 功能模块, 所属模块]
  - field: title
    header: 用例标题
    width: 30
    required: true
  - field: priority
    header: 优先级
    width: 10
    default: 中
    validate: [高, 中, 低]
    extract:
      - keywords: [优先级, priority]
  - field: precondition
    header: 前置条件
    width: 25
    extract:
      - keywords: [前置条件, 前提, precondition]
  - field: steps
    header: 操作步骤
    width: 40
    multiline: true
  - field: expected
    header: 预期结果
    width: 35
    required: true
  - field: status
    header: 状态
    width: 10
    default: 待执行
    validate: [待执行, 执行中, 通过, 失败, 阻塞]
```

### 渲染流程

1. 加载模板 `.xlsx` → 获取样式表头
2. 加载 schema `.yaml` → 获取字段映射规则
3. 逐条 record：按 schema.columns 映射字段→单元格，缺失字段填 default，auto_generate 自动编号，validate 校验值
4. 数据行继承表头行样式（字体/边框/对齐）
5. 自动调整行高（multiline 字段）
6. 写入输出文件

### 模板扩展

- `epm template-init <name>` → 在 `~/.epm/templates/<name>/` 下生成 `template.xlsx` + `schema.yaml` 供修改
- `epm list-templates` 同时扫描内置 `assets/templates/` + `~/.epm/templates/`

## 内置模板

1. **test-case**：测试用例（用例编号/模块/标题/优先级/前置条件/步骤/预期结果/状态）
2. **requirements**：需求追踪矩阵（需求ID/描述/来源/优先级/状态/负责人/关联用例）
3. **project-plan**：项目计划表（任务ID/任务名/负责人/开始日期/结束日期/状态/备注）

## AI Agent Skill 集成

`excel-master-skill/skill.md` 内容覆盖：

1. **前置检查**：`epm --version` 确认安装，未安装则提示 `pip install -e .`
2. **使用流程**：`list-templates` → `show-schema` → `create`
3. **场景示例**：从 PRD 生成测试用例、从需求文档生成追踪矩阵等
4. **大文件处理**：自动续接、`--clean` 强制重来
5. **错误处理**：查看 warning，修正输入重试

## 技术依赖

- Python 3.10+
- click（CLI 框架）
- openpyxl（Excel 读写）
- python-docx（Word 解析）
- PyYAML（YAML 解析）
- pytest（测试）
