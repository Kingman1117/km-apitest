# KMSK 接口自动化测试框架

基于 `Python + pytest + requests` 的企业级接口自动化测试框架，采用 **Client -> Actions -> Test** 三层架构设计。

## 框架特性

- **三层架构**：Client（HTTP封装） -> Actions（业务逻辑） -> Test（用例编排）
- **多端支持**：Admin管理后台、EduPC教育PC端、H5移动端
- **Session缓存**：30分钟有效期，避免重复登录
- **TAPD集成**：测试结果自动回填到TAPD测试计划
- **企业微信通知**：执行完成后推送汇总报告
- **配置外置**：敏感信息通过环境变量或配置文件管理
- **Skill支持**：兼容 Cursor Agent Skill + MCP 工具链

## 快速开始

### 1. 安装依赖

```bash
pip install -r api_tests/requirements.txt
```

### 2. 配置账号

复制示例配置并填写真实信息：

```bash
cp config/test_plan_config.example.json config/test_plan_config.json
cp config/tapd_config.example.json config/tapd_config.json
```

或使用环境变量（推荐CI/CD场景）：

```bash
export KMSK_ADMIN_USERNAME=your_admin
export KMSK_ADMIN_PASSWORD=your_password
export KMSK_STUDENT_USERNAME=your_student
export KMSK_STUDENT_PASSWORD=your_password
```

### 3. 运行测试

```bash
# 运行全部用例
python scripts/run_api_tests.py

# 按模块运行
python scripts/run_api_tests.py api_tests/admin -v
python scripts/run_api_tests.py api_tests/edupc -v
python scripts/run_api_tests.py api_tests/h5 -v

# 禁用TAPD回填
python scripts/run_api_tests.py --no-tapd-report

# 查看详细输出
python scripts/run_api_tests.py -v -s
```

## 项目结构

```
kmsk/
├── api_tests/                    # 测试代码主目录
│   ├── clients/                  # HTTP客户端层
│   │   ├── base_client.py        # 基类：请求、响应、断言
│   │   ├── admin_client.py       # Admin端客户端
│   │   ├── edupc_client.py       # EduPC端客户端
│   │   └── h5_client.py          # H5端客户端
│   ├── actions/                  # 业务动作层
│   │   ├── content_actions.py    # 内容创建动作
│   │   └── order_actions.py      # 订单相关动作
│   ├── admin/                    # Admin测试用例（17个）
│   ├── edupc/                    # EduPC测试用例（4个）
│   ├── h5/                       # H5测试用例（11个）
│   ├── cross_platform/           # 跨端验收用例（默认不执行）
│   ├── conftest.py               # Pytest配置与fixtures
│   ├── config_loader.py          # 配置加载器
│   ├── data_factory.py           # 测试数据工厂
│   ├── tapd_reporter.py          # TAPD回填模块
│   ├── wecom_notifier.py         # 企业微信通知模块
│   └── requirements.txt          # Python依赖
├── config/                       # 配置文件目录
│   ├── test_data.json            # 测试数据（服务ID、文件ID等）
│   ├── test_plan_config.json     # 账号配置（gitignore）
│   └── tapd_config.json          # TAPD配置（gitignore）
├── scripts/                      # 脚本工具
│   ├── run_api_tests.py          # 测试运行入口
│   ├── run_test_with_tapd.py     # 带TAPD回填的运行
│   └── clear_session_cache.py    # 清除session缓存
├── agent_skills/                 # Cursor Skill定义
├── docs/                         # 项目文档
└── pytest.ini                    # Pytest配置
```

## 用例覆盖

| 模块 | 用例数 | 场景 |
|------|--------|------|
| Admin | 17 | 创建音频、视频、图文、系列课、问答、电子书、线下课、商品、表单、优惠券等 |
| EduPC | 4 | 视频/音频/专栏/系列课订单提交 |
| H5 | 11 | 各类商品订单提交、图书服务、线下课、商品购买 |
| 跨端 | 1 | Admin创建 -> C端查看验证 |

## 环境变量

### 账号配置

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `KMSK_ADMIN_USERNAME` | 管理员账号 | `admin` |
| `KMSK_ADMIN_PASSWORD` | 管理员密码 | `password` |
| `KMSK_STUDENT_USERNAME` | 学员账号 | `student` |
| `KMSK_STUDENT_PASSWORD` | 学员密码 | `password` |

### TAPD配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `TAPD_ENABLED` | 是否启用TAPD回填 | `true` |
| `TAPD_WORKSPACE_ID` | TAPD项目ID | - |
| `TAPD_API_USER` | TAPD API账号 | - |
| `TAPD_API_PASSWORD` | TAPD API密码 | - |
| `TAPD_TEST_PLAN_ID` | 测试计划ID | - |
| `TAPD_REPORT_INTERVAL_SECONDS` | 回填间隔（秒） | `0.3` |

### 企业微信配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `WECOM_ENABLED` | 是否启用通知 | `false` |
| `WECOM_WEBHOOK` | 机器人Webhook地址 | - |

### 运行控制

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `API_RATE_LIMIT_SECONDS` | 用例间隔时间（秒） | `2` |

## 新增用例指南

参考 `docs/用例标准与新增模板.md`，遵循以下规范：

1. **文件命名**：`test_{module}_{feature}.py`
2. **Docstring格式**：
   ```python
   """
   用例 ID: TAPD用例ID
   用例名称: 用例描述
   接口: METHOD /api/path
   """
   ```
3. **测试结构**：Arrange -> Act -> Assert
4. **断言方式**：使用 `client.assert_success(result, "错误描述")`

## Windows路径问题

如果路径包含中文导致PowerShell报错，可创建英文别名：

```powershell
cmd /c mklink /J E:\kmsk "E:\MCP测试\kmsk"
cd /d E:\kmsk
python scripts/run_api_tests.py
```

## 常用命令

```bash
# 清除session缓存（强制重新登录）
python scripts/clear_session_cache.py

# 运行单个用例
python scripts/run_api_tests.py api_tests/admin/test_admin_add_audio.py -v

# 运行包含跨端用例
python scripts/run_api_tests.py -m "cross_platform or not cross_platform"
```

## 相关文档

- [项目结构总览](PROJECT_STRUCTURE.md)
- [用例标准与模板](docs/用例标准与新增模板.md)
- [TAPD自动回填说明](docs/TAPD自动回填使用说明.md)
- [文档索引](docs/README.md)
