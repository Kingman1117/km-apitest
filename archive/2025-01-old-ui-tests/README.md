# 旧UI自动化文件归档

**归档时间**: 2026-02-11  
**归档原因**: 项目已全面转向API-first测试策略

## 归档内容

### scripts/
旧的UI自动化相关脚本：
- `capture_api_from_case.js` - API捕获脚本
- `capture_api_from_group.js` - 批量API捕获
- `run_acceptance_pipeline.js` - 旧的验收流程编排
- `run_ui_smoke.js` - UI冒烟测试执行
- `sync_case_api_mapping.js` - 用例API映射同步

### config/
旧的UI自动化配置：
- `acceptance_pipeline.json` - 验收流程配置
- `ui_smoke_plan.json` - UI冒烟测试计划
- `case_api_mapping.json` - 用例到API映射

### case_scripts/
48个旧的UI测试用例JSON文件（已在之前归档）

### api_captures/
4个API捕获文件（已在之前归档）

## 说明

这些文件已不再使用，但保留归档以备将来参考。

如果1个月后确认不再需要，可以安全删除此目录。
