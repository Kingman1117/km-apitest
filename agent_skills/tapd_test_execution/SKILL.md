# TAPD测试执行 Skill

**版本**: v1.0  
**创建时间**: 2026-02-11  
**用途**: 自动化TAPD测试计划的执行和结果回填流程

---

## 何时使用此Skill

当用户提出以下需求时，自动触发此Skill：
- "执行第X期验收测试"
- "运行TAPD测试计划"
- "更新测试计划ID"
- "回填测试结果到TAPD"
- "查看TAPD执行结果"

---

## 核心功能

### 1. 更新测试计划配置
### 2. 执行API测试
### 3. 自动回填TAPD
### 4. 生成执行报告
### 5. 故障排查

---

## 执行流程

### 步骤1: 获取测试计划信息

**从用户获取**:
- 测试计划ID（必需）
- 测试计划名称（可选）
- 测试计划URL（可选）

**示例**:
```
用户: "执行第8期验收测试，计划ID是 1150695810001001510"
AI: [提取] plan_id=1150695810001001510, plan_name="第8期验收测试"
```

### 步骤2: 更新配置文件

**文件**: `config/tapd_config.json`

**更新内容**:
```json
{
  "workspace_id": "50695810",
  "api_user": "your_tapd_api_user",
  "api_password": "your_tapd_api_password",
  "base_url": "https://api.tapd.cn",
  "enabled": true,
  
  "current_test_plan": {
    "id": "{新的测试计划ID}",
    "name": "{测试计划名称}",
    "created_at": "{当前日期}",
    "url": "https://www.tapd.cn/50695810/sparrow/test_plan/detail/{计划ID}"
  },
  
  "tester": "自动化测试"
}
```

**操作**:
1. 读取现有配置
2. 更新`current_test_plan`部分
3. 保存配置文件
4. 确认更新成功

### 步骤3: 执行测试

**执行方式选择**:

#### 方式A: 完整执行（推荐）
```bash
pytest api_tests/ -v
```
- 执行所有30个测试用例
- 自动回填所有结果到TAPD
- 适合完整验收

#### 方式B: 分批执行
```bash
# 批次1: 管理后台（17个用例）
pytest api_tests/test_admin_add_*.py -v

# 批次2: EduPC（5个用例）
pytest api_tests/test_c0[1-5]*.py -v

# 批次3: H5（10个用例）
pytest api_tests/test_c0[6-9]*.py api_tests/test_c1*.py -v
```
- 分批执行，避免频率限制
- 每批之间间隔5秒
- 适合调试或部分验证

#### 方式C: 单个测试（调试）
```bash
pytest api_tests/test_admin_add_audio.py -v -s
```
- 用于验证单个用例
- 查看详细输出

### 步骤4: 监控执行过程

**关注输出**:
```
[TAPD] 回填目标: 测试计划 1150695810001001510 - 第8期验收测试

test_admin_add_audio.py::test_admin_add_audio 
[TAPD调试] 从模块提取到用例ID: 1150695810001062392
[TAPD调试] 请求URL: https://api.tapd.cn/tcase_instance/execute
[TAPD调试] 测试计划ID: 1150695810001001510, 用例ID: 1150695810001062392, 结果: pass
[TAPD调试] 响应状态码: 200
[TAPD调试] 响应内容: {"status":1,"data":[],"info":"success"}
[TAPD回填成功] 用例1150695810001062392: PASSED

PASSED [100%]
```

**关键信息**:
- ✓ 用例ID提取成功
- ✓ TAPD API调用成功（status=1）
- ✓ 回填成功标记

### 步骤5: 处理失败情况

**测试失败**:
```python
# 输出示例
[TAPD调试] 结果: no_pass
[TAPD回填成功] 用例1150695810001062XXX: FAILED
```
- 失败用例也会回填到TAPD
- 标记为"不通过"
- 备注中包含错误信息

**API回填失败**:
```python
# 输出示例
[TAPD回填失败] 用例1150695810001062XXX: 401 Unauthorized
```
- 检查TAPD API凭证
- 检查测试计划ID是否正确
- 检查用例是否已关联到测试计划

### 步骤6: 生成执行报告

**自动生成内容**:
1. 执行统计（通过/失败数量）
2. 执行时间
3. 回填成功率
4. 失败用例列表

**报告位置**: 控制台输出 + 可选HTML报告

---

## 使用脚本执行（推荐）

### 脚本: `scripts/run_test_with_tapd.py`

**功能**:
- 自动更新配置文件
- 执行测试
- 统计结果
- 生成报告

**使用方式**:

#### 基础用法
```bash
# 指定测试计划ID和名称
python scripts/run_test_with_tapd.py \
  --plan-id 1150695810001001510 \
  --plan-name "第8期验收测试"
```

#### 高级用法
```bash
# 不更新配置文件，仅命令行传递
python scripts/run_test_with_tapd.py \
  --plan-id 1150695810001001510 \
  --no-update-config

# 禁用TAPD回填（仅执行测试）
python scripts/run_test_with_tapd.py --no-tapd

# 执行特定模块
python scripts/run_test_with_tapd.py \
  --plan-id 1150695810001001510 \
  --test-path "api_tests/admin/"
```

---

## 命令行选项

### Pytest内置选项

```bash
# 指定测试计划ID（覆盖配置文件）
pytest api_tests/ -v --tapd-plan=1150695810001001510

# 禁用TAPD回填
pytest api_tests/ -v --no-tapd-report

# 显示详细输出
pytest api_tests/ -v -s

# 仅执行失败的用例
pytest api_tests/ -v --lf

# 停在第一个失败
pytest api_tests/ -v -x
```

---

## TAPD回填机制

### 工作原理

1. **Pytest Hook捕获**:
   ```python
   @pytest.hookimpl(tryfirst=True, hookwrapper=True)
   def pytest_runtest_makereport(item, call):
       # 测试执行完成后自动触发
   ```

2. **提取用例ID**:
   ```python
   # 从模块docstring提取
   """
   用例 ID: 1150695810001062392
   """
   ```

3. **调用TAPD API**:
   ```python
   POST https://api.tapd.cn/tcase_instance/execute
   {
       "workspace_id": "50695810",
       "test_plan_id": "1150695810001001510",
       "tcase_id": "1150695810001062392",
       "result_status": "pass",  # 或 "no_pass"
       "last_executor": "自动化测试",
       "result_remark": "执行时间: 3.24秒\n..."
   }
   ```

4. **记录结果**:
   - 成功: 打印"[TAPD回填成功]"
   - 失败: 打印"[TAPD回填失败]" + 错误信息

### 回填内容

**通过的用例**:
- 执行结果: 通过
- 执行人: 自动化测试
- 执行时间: X.XX秒
- 备注: 自动化测试执行 + 时间戳

**失败的用例**:
- 执行结果: 不通过
- 执行人: 自动化测试
- 执行时间: X.XX秒
- 备注: 失败原因（前500字符）

---

## 验证回填结果

### 在TAPD中查看

1. 打开测试计划URL:
   ```
   https://www.tapd.cn/50695810/sparrow/test_plan/detail/{计划ID}
   ```

2. 查看用例列表，确认：
   - ✓ 执行结果已更新（通过/不通过）
   - ✓ 执行人显示为"自动化测试"
   - ✓ 执行时间已记录
   - ✓ 备注中包含详细信息

3. 统计执行进度：
   - 已执行用例数
   - 通过率
   - 失败用例列表

---

## 故障排查

### 问题1: TAPD回填失败

**症状**:
```
[TAPD回填失败] 用例1150695810001062392: 401 Unauthorized
```

**排查步骤**:
1. 检查`config/tapd_config.json`中的API凭证
2. 验证凭证是否过期
3. 测试API连接:
   ```bash
   curl -u 'your_tapd_api_user:your_tapd_api_password' \
     'https://api.tapd.cn/workspaces/users?workspace_id=50695810'
   ```

**解决方案**:
- 重新生成TAPD API Token
- 更新`tapd_config.json`

---

### 问题2: 用例ID未提取

**症状**:
```
[TAPD调试] 未找到用例ID
```

**排查步骤**:
1. 检查测试文件顶部的模块docstring
2. 确认格式正确:
   ```python
   """
   用例 ID: 1150695810001062392
   用例名称: XXX
   """
   ```

**解决方案**:
- 添加或修正模块docstring
- 确保"用例 ID:"格式正确

---

### 问题3: 测试计划中找不到执行记录

**症状**:
- TAPD API返回成功
- 但测试计划中看不到执行记录

**排查步骤**:
1. 确认测试计划ID正确
2. 确认用例已关联到测试计划
3. 在TAPD中手动搜索用例ID

**解决方案**:
- 在TAPD测试计划中，先关联用例库中的用例
- 确认用例ID与用例库中的ID一致

---

### 问题4: 频率限制错误

**症状**:
```
{"msg": "服务频繁提交请求，请稍后重试", "rt": -1, "success": False}
```

**排查步骤**:
- 检查是否连续快速执行多个测试

**解决方案**:
- 使用分批执行
- 在`conftest.py`中已添加自动延时（2秒）
- 如仍出现，增加延时:
  ```python
  @pytest.fixture(autouse=True)
  def rate_limit_delay():
      yield
      time.sleep(3)  # 增加到3秒
  ```

---

## 每2周执行流程

### 标准流程

```
第1步: 在TAPD创建新测试计划
  ↓
第2步: 复制测试计划ID
  ↓
第3步: 执行自动化脚本
  python scripts/run_test_with_tapd.py \
    --plan-id {新ID} \
    --plan-name "第X期验收"
  ↓
第4步: 等待测试完成（约5-10分钟）
  ↓
第5步: 在TAPD查看执行结果
  ↓
第6步: 处理失败用例（如有）
```

### 时间估算

- **完整执行**: 约10-15分钟（30个用例 + 频率限制延时）
- **分批执行**: 约15-20分钟（包含手动间隔）
- **TAPD回填**: 实时（每个用例完成后立即回填）

---

## 执行检查清单

执行前确认：
- [ ] 已在TAPD创建新测试计划
- [ ] 已复制测试计划ID
- [ ] 已关联所有用例到测试计划
- [ ] `config/tapd_config.json`中的凭证有效
- [ ] 网络连接正常

执行中监控：
- [ ] 测试用例正常执行
- [ ] TAPD回填成功标记出现
- [ ] 无频率限制错误
- [ ] 无认证失败错误

执行后验证：
- [ ] 在TAPD中查看执行记录
- [ ] 确认通过率符合预期
- [ ] 记录失败用例
- [ ] 生成执行报告

---

## 快速参考

### 常用命令

```bash
# 完整执行（推荐）
python scripts/run_test_with_tapd.py --plan-id {ID} --plan-name "{名称}"

# 仅执行测试（不回填）
pytest api_tests/ -v --no-tapd-report

# 查看TAPD配置
cat config/tapd_config.json

# 测试单个用例
pytest api_tests/test_admin_add_audio.py -v -s
```

### 配置文件位置

```
config/tapd_config.json          # TAPD配置
api_tests/conftest.py            # Pytest配置和TAPD Hook
scripts/run_test_with_tapd.py    # 执行脚本
```

### 文档位置

```
docs/TAPD自动回填使用说明.md              # 详细使用说明
docs/TAPD测试计划回填方案_动态计划.md     # 技术方案
docs/API频率限制说明.md                   # 频率限制处理
```

---

**使用此Skill后，AI将自动完成测试计划更新、测试执行、TAPD回填的全流程，确保高效和准确。**
