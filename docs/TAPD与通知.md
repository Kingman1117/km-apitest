# TAPD 自动回填与企业微信通知

## 1. TAPD 自动回填

### 功能
测试执行完成后，自动将每条用例的 PASSED/FAILED 状态回填到 TAPD 测试计划。

### 前置条件
- TAPD 项目中已创建测试计划
- 每条用例文件头包含 `用例 ID: 19位数字`
- 配置 TAPD API 凭据

### 配置方式

**方式一：配置文件**
```bash
cp config/tapd_config.example.json config/tapd_config.json
# 编辑填入真实凭据
```

**方式二：环境变量（推荐 CI/CD）**
```bash
TAPD_ENABLED=true
TAPD_WORKSPACE_ID=你的项目ID
TAPD_API_USER=API账号
TAPD_API_PASSWORD=API密码
TAPD_TEST_PLAN_ID=测试计划ID
```

### 使用
```bash
# 默认启用
pytest api_tests/ -q

# 指定测试计划
pytest api_tests/ --tapd-plan 12345

# 禁用回填
pytest api_tests/ --no-tapd-report
```

### 回填逻辑
- `pytest_runtest_makereport` hook 在每条用例结束后触发
- 从用例 docstring 或文件头提取 TAPD 用例 ID
- 调用 TAPD API 更新执行状态
- 回填间隔默认 0.3 秒，避免触发 TAPD 限频

---

## 2. 企业微信通知

### 功能
测试全部执行完成后，向企业微信群推送汇总报告。

### 配置
```bash
WECOM_ENABLED=true
WECOM_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
```

### 通知内容
- 总用例数 / 通过数 / 失败数
- 失败用例列表（如有）
- 执行耗时

### 通知策略
- `WECOM_NOTIFY_STRATEGY=always` — 每次都通知
- `WECOM_NOTIFY_STRATEGY=on_failure` — 仅失败时通知（默认）
