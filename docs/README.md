# API 自动化文档索引

## 核心文档

- `专业接口自动化测试框架改造方案.md`：框架设计与改造原则
- `用例标准与新增模板.md`：命名、断言、数据与新增用例模板
- `测试用例清单_完整版.md`：当前已转换用例清单
- `API转换模板_精简版.md`：管理后台创建类用例转换模板
- `C端用例转换模板.md`：C 端订单类用例转换模板
- `API频率限制说明.md`：限频处理策略
- `TAPD自动回填使用说明.md`：TAPD 回填与执行说明
- `TAPD测试计划回填方案_动态计划.md`：动态计划回填方案细节

## 快速执行

```bash
python scripts/run_api_tests.py api_tests/admin -v
python scripts/run_api_tests.py api_tests/edupc -v
python scripts/run_api_tests.py api_tests/h5 -v
python scripts/run_api_tests.py api_tests -v --no-tapd-report
```

启用第三方 pytest 插件（默认禁用）：

```bash
python scripts/run_api_tests.py --with-third-party-plugins api_tests -v
```

Windows 中文路径建议（可选）：

```powershell
cmd /c mklink /J E:\kmsk "E:\MCP测试\kmsk"
cd /d E:\kmsk
python scripts/run_api_tests.py
```

## 配置规范

- 本地配置文件：
  - `config/test_plan_config.json`
  - `config/tapd_config.json`
- 模板文件：
  - `config/test_plan_config.example.json`
  - `config/tapd_config.example.json`
- 生产与 CI 推荐使用环境变量覆盖，不在仓库明文保存账号和密钥。

## 常用环境变量

- 账号相关：
  - `KMSK_ADMIN_USERNAME`
  - `KMSK_ADMIN_PASSWORD`
  - `KMSK_STUDENT_USERNAME`
  - `KMSK_STUDENT_PASSWORD`
- TAPD 相关：
  - `TAPD_ENABLED`
  - `TAPD_WORKSPACE_ID`
  - `TAPD_API_USER`
  - `TAPD_API_PASSWORD`
  - `TAPD_TEST_PLAN_ID`
- 企业微信相关：
  - `WECOM_ENABLED`
  - `WECOM_WEBHOOK`
