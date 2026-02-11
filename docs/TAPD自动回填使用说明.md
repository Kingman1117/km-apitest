# TAPD自动回填功能使用说明

## 功能说明

自动化测试执行完成后，会自动将测试结果回填到TAPD测试计划中，包括：
- 执行状态（通过/失败）
- 执行时间
- 执行人
- 失败原因（如果失败）

---

## 回填成功确认

### 刚才的测试结果

**测试用例**: `test_admin_add_audio` (用例ID: 1150695810001062392)  
**测试计划**: 1150695810001001509  
**回填状态**: [OK] 成功  
**API响应**: `{"status":1,"data":[],"info":"success"}`

### 在TAPD中查看

1. 打开测试计划: https://www.tapd.cn/50695810/sparrow/test_plan/detail/1150695810001001509
2. 找到用例 `1150695810001062392` (管理后台正常添加音频课程)
3. 查看执行记录：
   - 执行结果: **通过**
   - 执行人: **自动化测试**
   - 执行时间: 约3.24秒
   - 备注: 包含执行时间和时间戳

---

## 配置文件

### `config/tapd_config.json`

```json
{
  "workspace_id": "50695810",
  "api_user": "your_tapd_api_user",
  "api_password": "your_tapd_api_password",
  "base_url": "https://api.tapd.cn",
  "enabled": true,
  
  "current_test_plan": {
    "id": "1150695810001001509",
    "name": "2026年第7期验收测试",
    "created_at": "2026-02-11",
    "url": "https://www.tapd.cn/50695810/sparrow/test_plan/detail/1150695810001001509"
  },
  
  "tester": "自动化测试"
}
```

**重要**: 每次创建新测试计划后，只需更新 `current_test_plan.id` 即可。

---

## 使用方式

### 方式1: 直接执行（使用配置文件）

```bash
# 执行所有测试（自动回填TAPD）
pytest api_tests/ -v

# 执行单个测试
pytest api_tests/test_admin_add_audio.py -v

# 执行管理后台测试
pytest api_tests/test_admin_add_*.py -v

# 执行C端测试
pytest api_tests/test_c*.py -v
```

### 方式2: 命令行指定测试计划

```bash
# 指定测试计划ID（不修改配置文件）
pytest api_tests/ -v --tapd-plan=1150695810001001509

# 禁用TAPD回填
pytest api_tests/ -v --no-tapd-report
```

### 方式3: 使用自动化脚本（推荐）

```bash
# 更新配置并执行测试
python scripts/run_test_with_tapd.py --plan-id 1150695810001001509 --plan-name "第7期验收"

# 仅命令行传递（不更新配置）
python scripts/run_test_with_tapd.py --plan-id 1150695810001001509 --no-update-config

# 禁用TAPD回填
python scripts/run_test_with_tapd.py --no-tapd
```

---

## 执行输出示例

```
[TAPD] 回填目标: 测试计划 1150695810001001509 - 2026年第7期验收测试

test_admin_add_audio.py::test_admin_add_audio 
[TAPD调试] 从模块提取到用例ID: 1150695810001062392
[TAPD调试] 请求URL: https://api.tapd.cn/tcase_instance/execute
[TAPD调试] 测试计划ID: 1150695810001001509, 用例ID: 1150695810001062392, 结果: pass
[TAPD调试] 响应状态码: 200
[TAPD调试] 响应内容: {"status":1,"data":[],"info":"success"}
[TAPD回填成功] 用例1150695810001062392: PASSED

PASSED [100%]
```

---

## 每2周执行流程

### 步骤1: 在TAPD创建新测试计划

1. 登录TAPD
2. 创建新测试计划（如: "2026年第8期验收测试"）
3. 关联用例库中的用例
4. 复制测试计划ID（从URL获取，如: `1150695810001001510`）

### 步骤2: 更新配置文件

编辑 `config/tapd_config.json`:

```json
{
  "current_test_plan": {
    "id": "1150695810001001510",  // ← 改为新的测试计划ID
    "name": "2026年第8期验收测试",
    "created_at": "2026-02-25"
  }
}
```

### 步骤3: 执行自动化测试

```bash
# 方式A: 使用脚本（自动更新配置）
python scripts/run_test_with_tapd.py --plan-id 1150695810001001510 --plan-name "第8期验收"

# 方式B: 手动更新配置后执行
pytest api_tests/ -v
```

### 步骤4: 在TAPD查看结果

打开测试计划，查看所有用例的执行记录。

---

## 用例ID映射

所有测试用例都在文件顶部的模块docstring中包含TAPD用例ID：

```python
"""
用例 ID: 1150695810001062392
用例名称: 管理后台正常添加音频课程

接口: POST /ajax/wxAppAudio_h.jsp?cmd=add
"""
```

系统会自动提取这个ID并回填到TAPD。

---

## 当前已支持的用例

### 管理后台创建类（15个）
- 1150695810001062391: 添加音频
- 1150695810001062392: 添加视频
- 1150695810001062393: 添加图文
- ... (共15个)

### EduPC订单流程（5个）
- 1150695810001062371: EduPC系列课订单
- 1150695810001062373: EduPC图文订单
- ... (共5个)

### H5订单流程（10个）
- 1150695810001062372: H5系列课订单
- 1150695810001062376: H5图文订单
- ... (共10个)

**总计**: 30个用例，全部支持自动回填

---

## 故障排查

### 问题1: 回填失败

**检查项**:
1. TAPD API凭证是否正确（`config/tapd_config.json`）
2. 测试计划ID是否正确
3. 用例是否已关联到测试计划
4. 网络是否正常

**查看详细日志**:
```bash
pytest api_tests/test_admin_add_audio.py -v -s
```

### 问题2: 用例ID未提取

**原因**: 测试文件缺少模块级docstring

**解决**: 确保文件顶部有：
```python
"""
用例 ID: 1150695810001062XXX
用例名称: XXX
"""
```

### 问题3: 测试计划中找不到执行记录

**原因**: 用例未关联到测试计划

**解决**: 在TAPD测试计划中，先关联用例库中的用例

---

## 技术细节

### TAPD API

- **接口**: `POST https://api.tapd.cn/tcase_instance/execute`
- **认证**: HTTP Basic Auth
- **参数**:
  - `workspace_id`: 项目ID (50695810)
  - `test_plan_id`: 测试计划ID
  - `tcase_id`: 用例ID
  - `result_status`: pass/no_pass/block
  - `last_executor`: 执行人
  - `result_remark`: 备注

### Pytest Hook

使用 `pytest_runtest_makereport` Hook在测试执行完成后自动回填：

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行完成后自动回填TAPD"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and TAPD_CONFIG.get("enabled"):
        case_id = extract_tapd_case_id(item)
        if case_id:
            # 调用TAPD API回填结果
            ...
```

---

## 常见问题

### Q: 每次都要重新登录TAPD吗？
A: 不需要。API使用Basic Auth，配置一次即可。

### Q: 测试失败会回填吗？
A: 会。失败的用例会标记为"不通过"，并在备注中包含错误信息。

### Q: 可以批量回填吗？
A: 目前是每个用例执行完成后立即回填。如需批量，可以修改代码在所有测试完成后统一回填。

### Q: 回填会影响测试执行吗？
A: 不会。即使TAPD API调用失败，测试仍会继续执行。

---

**更新时间**: 2026-02-11  
**版本**: v1.0  
**负责人**: 自动化测试团队
