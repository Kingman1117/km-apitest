# 项目文档

## 核心文档

| 文档 | 说明 |
|------|------|
| [测试执行指南.md](测试执行指南.md) | 运行方式、并发策略、限频机制、常见问题 |
| [开发规范.md](开发规范.md) | 用例编写标准、断言规范、契约层、payload 模板、数据清理 |
| [TAPD与通知.md](TAPD与通知.md) | TAPD 自动回填 + 企业微信通知配置 |
| [API转换模板_精简版.md](API转换模板_精简版.md) | HAR → pytest 用例转换工具 |

## 归档文档

历史报告和排障记录位于 `archive/` 目录。

## 快速开始

```bash
# 并发执行（推荐）
powershell -ExecutionPolicy Bypass -File run_tests_concurrent.ps1

# 串行执行
pytest api_tests/ -q
```

## 项目状态

- 测试用例: 40 个（100% 通过）
- 执行耗时: ~103s（串行） / ~87s（并发）
- 架构: Client → Actions → Test 三层分离
