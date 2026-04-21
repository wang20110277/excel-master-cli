## Why

当前 excel-master-cli 支持从文本、Markdown、Word 文档等解析数据生成 Excel，但无法处理图片输入。许多项目的产品需求、UI 原型、功能说明以截图形式保存（如 `tests/项目计划/` 下的 PNG 文件），用户需要手动将这些截图内容转为测试用例，效率低下。通过 agent 自身的多模态视觉能力直接识别图片内容并生成结构化测试用例，无需配置外部 AI API。

## What Changes

- 新增 `image` 格式解析器（`ImageParser`），扫描指定文件夹下的图片（PNG/JPG/JPEG/BMP），将图片路径和识别结果关联
- agent（如 Claude Code）通过自身视觉能力读取图片，生成结构化 JSON 数据，CLI 将其解析为测试用例记录
- 不需要外部 API Key、模型配置，完全依赖 agent 内置视觉能力

## Capabilities

### New Capabilities
- `image-parser`: 图片解析器，扫描文件夹中的图片文件，依赖 agent 视觉能力识别内容，输出结构化测试用例记录

### Modified Capabilities

## Impact

- **新增文件**: `src/excel_master/parser/image.py`
- **修改文件**: `src/excel_master/parser/base.py`（格式注册）、`src/excel_master/cli.py`（新增 image 格式支持）
- **无新增外部依赖**: 不需要 openai SDK 或额外的 API Key
