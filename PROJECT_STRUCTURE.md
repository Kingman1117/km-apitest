# 项目结构

## 主目录

```
kmsk/
├── .cursor/
│   └── mcp.json                # MCP 服务配置入口（API-only）
├── api_tests/
│   ├── clients/                 # HTTP 客户端层（Admin/EduPC/H5）
│   ├── actions/                 # 业务动作层（下单、退款、内容创建）
│   ├── admin/                   # 管理后台核心创建用例
│   ├── edupc/                   # EduPC 核心订单用例
│   ├── h5/                      # H5 核心订单用例
│   ├── cross_platform/          # 跨端验收场景（默认不纳入核心回归）
│   ├── conftest.py              # 全局 fixture、TAPD 回填、企业微信通知
│   ├── config_loader.py         # 配置加载与环境变量覆盖
│   ├── tapd_reporter.py         # TAPD 回填封装
│   ├── wecom_notifier.py        # 企业微信通知封装
│   ├── data_factory.py          # 复用请求数据工厂（订单/退款）
│   ├── requirements.txt
│   └── test_data_manager.py
├── config/
│   ├── test_plan_config.json
│   ├── tapd_config.json
│   ├── test_plan_config.example.json
│   ├── tapd_config.example.json
│   └── test_data.json
├── docs/
│   ├── README.md
│   ├── 用例标准与新增模板.md
│   ├── API转换模板_精简版.md
│   ├── C端用例转换模板.md
│   ├── API频率限制说明.md
│   ├── TAPD自动回填使用说明.md
│   ├── TAPD测试计划回填方案_动态计划.md
│   ├── 专业接口自动化测试框架改造方案.md
│   └── 测试用例清单_完整版.md
├── scripts/
│   ├── run_api_tests.py
│   ├── run_test_with_tapd.py
│   ├── check_tapd_case_ids.py
│   ├── clear_edupc_cache.py
│   └── reorganize_tests.py
├── agent_skills/
│   ├── api_test_conversion/      # API 测试转换技能
│   ├── api_test_maintenance/     # API 测试维护技能
│   └── tapd_test_execution/      # TAPD 测试执行技能
├── archive/
├── pytest.ini
└── README.md
```

## 执行说明

- 默认核心回归：`python scripts/run_api_tests.py`
- npm 命令入口（可选）：`npm run test`
- 按端执行：
  - `python scripts/run_api_tests.py api_tests/admin -v`
  - `python scripts/run_api_tests.py api_tests/edupc -v`
  - `python scripts/run_api_tests.py api_tests/h5 -v`
- 禁用 TAPD：`python scripts/run_api_tests.py api_tests -v --no-tapd-report`
- 启用第三方插件：`python scripts/run_api_tests.py --with-third-party-plugins api_tests -v`
