## 1. ImageParser 实现

- [ ] 1.1 创建 `src/excel_master/parser/image.py`，实现 `ImageParser` 类，继承 `BaseParser`
- [ ] 1.2 实现 JSON 数据文件解析：读取 JSON 数组，映射为 ParseResult.records
- [ ] 1.3 实现图片文件夹扫描：支持 PNG/JPG/JPEG/BMP，自然排序
- [ ] 1.4 实现字段名自动匹配：支持 field 名和 header 名两种映射

## 2. CLI 集成

- [ ] 2.1 在 `src/excel_master/parser/base.py` 的 `auto_detect_format` 中添加 image 格式检测
- [ ] 2.2 在 `src/excel_master/parser/__init__.py` 中注册 `ImageParser`
- [ ] 2.3 修改 `src/excel_master/cli.py` 的 `create` 命令，支持 image 格式

## 3. 端到端验证

- [ ] 3.1 使用 agent 视觉能力读取 `tests/项目计划/` 下的图片，生成 JSON 数据
- [ ] 3.2 使用 CLI 从 JSON 生成测试用例 Excel
- [ ] 3.3 验证 Excel 下拉选和背景色格式正确
