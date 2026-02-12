# API测试维护 Skill

**版本**: v1.0  
**创建时间**: 2026-02-11  
**用途**: 批量更新、修复和优化API测试用例

---

## 何时使用此Skill

当用户提出以下需求时，自动触发此Skill：
- "批量更新测试用例"
- "修复失败的测试"
- "重构测试代码"
- "添加新的断言"
- "优化测试性能"
- "统一测试风格"

---

## 核心功能

### 1. 批量更新测试用例
### 2. 修复失败测试
### 3. 代码重构
### 4. 添加/更新断言
### 5. 性能优化

---

## 维护场景

### 场景1: 批量更新API端点

**触发条件**: API基础URL变更

**操作步骤**:
1. 识别需要更新的文件
   ```bash
   grep -r "old-domain.com" api_tests/
   ```

2. 批量替换
   ```python
   # 使用StrReplace工具逐个文件更新
   old: "http://old-domain.com/api"
   new: "http://new-domain.com/api"
   ```

3. 验证更新
   ```bash
   pytest api_tests/ -v --collect-only  # 检查语法
   ```

---

### 场景2: 修复失败的测试

**触发条件**: 测试执行失败

**诊断流程**:

#### 步骤1: 分析失败原因
```bash
# 执行失败的测试，查看详细输出
pytest api_tests/test_xxx.py -v -s --tb=long
```

#### 步骤2: 常见失败类型及解决

**类型A: 断言失败**
```python
# 错误
AssertionError: API返回缺少ID: {'success': True, 'data': {...}}

# 原因: ID提取路径不正确
# 解决: 调整ID提取逻辑
item_id = (
    result.get("data", {}).get("id") or
    result.get("data", {}).get("itemId") or
    result.get("id")
)
```

**类型B: 认证失败**
```python
# 错误
AssertionError: Login failed: {'success': False, 'msg': 'token过期'}

# 原因: Session缓存过期
# 解决: 删除缓存文件
rm api_tests/.session_cache.pkl
rm api_tests/.edupc_session_cache.pkl
rm api_tests/.h5_session_cache.pkl
```

**类型C: 数据冲突**
```python
# 错误
AssertionError: 名称已存在

# 原因: 动态数据生成重复
# 解决: 确保使用timestamp fixture
name = f"音频{timestamp}"  # timestamp每次不同
```

**类型D: 频率限制**
```python
# 错误
{"msg": "服务频繁提交请求，请稍后重试"}

# 原因: 请求过快
# 解决: 增加延时
@pytest.fixture(autouse=True)
def rate_limit_delay():
    yield
    time.sleep(3)  # 从2秒增加到3秒
```

#### 步骤3: 应用修复
1. 修改测试代码
2. 重新执行测试
3. 确认修复成功

---

### 场景3: 代码重构

**触发条件**: 代码重复、可读性差

**重构模式**:

#### 模式A: 提取公共逻辑到Fixture

**重构前**:
```python
# 每个测试都重复
def test_add_audio(...):
    name = f"音频{timestamp}"
    result = admin_client.post(...)
    assert result.get("success") is True
    audio_id = result.get("data", {}).get("id")
    assert audio_id
    
def test_add_video(...):
    name = f"视频{timestamp}"
    result = admin_client.post(...)
    assert result.get("success") is True
    video_id = result.get("data", {}).get("id")
    assert video_id
```

**重构后**:
```python
# conftest.py
@pytest.fixture
def assert_create_success():
    def _assert(result, resource_type):
        assert result.get("success") is True, f"{resource_type}创建失败: {result}"
        item_id = result.get("data", {}).get("id") or result.get("id")
        assert item_id, f"未返回{resource_type}ID: {result}"
        return item_id
    return _assert

# 测试文件
def test_add_audio(admin_client, timestamp, assert_create_success):
    name = f"音频{timestamp}"
    result = admin_client.post(...)
    audio_id = assert_create_success(result, "音频")
```

#### 模式B: 使用参数化测试

**重构前**:
```python
def test_add_audio(...):
    # 添加音频逻辑
    
def test_add_video(...):
    # 添加视频逻辑（几乎相同）
    
def test_add_news(...):
    # 添加图文逻辑（几乎相同）
```

**重构后**:
```python
@pytest.mark.parametrize("resource_type,file_id,api_path", [
    ("音频", "AJQBCAAQNxgAIKrF18sGKICiiKQCMAA4AA", "/ajax/wxAppAudio_h.jsp"),
    ("视频", "AJQBCAAQNxgAIKrF18sGKICiiKQCMAA4BB", "/ajax/wxAppVideo_h.jsp"),
    ("图文", None, "/ajax/wxAppNews_h.jsp"),
])
def test_add_resource(admin_client, timestamp, resource_type, file_id, api_path):
    name = f"{resource_type}{timestamp}"
    data = {"cmd": "add", "name": name}
    if file_id:
        data["fileId"] = file_id
    
    result = admin_client.post(api_path, data=data)
    assert result.get("success") is True
```

---

### 场景4: 添加/更新断言

**触发条件**: 需要更严格的验证

**增强断言**:

#### 基础断言 → 详细断言

**基础版**:
```python
result = admin_client.post(...)
assert result.get("success") is True
```

**增强版**:
```python
result = admin_client.post(...)

# 1. 验证成功标志
assert result.get("success") is True, f"API调用失败: {result}"

# 2. 验证返回数据结构
assert "data" in result, f"响应缺少data字段: {result}"

# 3. 验证ID
item_id = result["data"].get("id")
assert item_id, f"未返回ID: {result}"
assert isinstance(item_id, (int, str)), f"ID类型错误: {type(item_id)}"

# 4. 验证名称
assert result["data"].get("name") == name, f"名称不匹配"

# 5. 验证时间戳
assert "created_at" in result["data"], f"缺少创建时间"
```

#### 添加业务规则验证

```python
# 验证优惠券金额规则
coupon_result = admin_client.post(...)
assert coupon_result["data"]["amount"] >= 100, "优惠券金额不能小于1元"
assert coupon_result["data"]["amount"] <= 1000000, "优惠券金额不能超过10000元"

# 验证订单状态
order_result = h5_client.post(...)
assert order_result["data"]["status"] in ["pending", "paid", "completed"], \
    f"订单状态异常: {order_result['data']['status']}"
```

---

### 场景5: 性能优化

**触发条件**: 测试执行缓慢

**优化策略**:

#### 策略A: 并行执行

```bash
# 安装pytest-xdist
pip install pytest-xdist

# 并行执行（4个worker）
pytest api_tests/ -v -n 4
```

**注意**: 需要确保测试之间无依赖

#### 策略B: 跳过慢速测试

```python
# 标记慢速测试
@pytest.mark.slow
def test_large_data_import(...):
    ...

# 执行时跳过
pytest api_tests/ -v -m "not slow"
```

#### 策略C: 使用缓存

```python
# conftest.py
@pytest.fixture(scope="session")
def test_data_cache():
    """缓存测试数据，避免重复创建"""
    cache = {}
    return cache

# 测试文件
def test_use_cached_data(admin_client, test_data_cache):
    if "audio_id" not in test_data_cache:
        # 首次创建
        result = admin_client.post(...)
        test_data_cache["audio_id"] = result["data"]["id"]
    
    # 使用缓存的ID
    audio_id = test_data_cache["audio_id"]
```

---

## 批量操作工具

### 工具1: 批量更新导入语句

```python
# 脚本: scripts/update_imports.py
import os
import re

def update_imports(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 更新导入
                content = content.replace(
                    'from conftest import',
                    'from api_tests.conftest import'
                )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

update_imports('api_tests/')
```

### 工具2: 批量添加类型提示

```python
# 为所有测试函数添加类型提示
def test_admin_add_audio(
    admin_client: AdminClient,
    timestamp: str
) -> None:
    """管理后台正常添加音频课程"""
    ...
```

### 工具3: 统一代码风格

```bash
# 安装工具
pip install black isort

# 格式化代码
black api_tests/
isort api_tests/
```

---

## 维护检查清单

### 每月检查

- [ ] 运行所有测试，记录失败用例
- [ ] 检查Session缓存是否过期
- [ ] 更新过时的测试数据
- [ ] 检查是否有新的API变更
- [ ] 审查代码重复度
- [ ] 更新文档

### 每季度检查

- [ ] 重构重复代码
- [ ] 优化慢速测试
- [ ] 更新依赖包版本
- [ ] 审查测试覆盖率
- [ ] 清理临时文件
- [ ] 归档旧版本

---

## 常见维护任务

### 任务1: 更新所有测试的timestamp长度

**需求**: 将timestamp从8位改为6位

**操作**:
```python
# conftest.py
@pytest.fixture(scope="session")
def timestamp():
    """生成6位时间戳"""
    return str(int(time.time()))[-6:]  # 从[-8:]改为[-6:]
```

**影响**: 所有使用timestamp的测试

**验证**:
```bash
pytest api_tests/ -v  # 确保所有测试通过
```

---

### 任务2: 统一错误消息格式

**需求**: 所有断言使用统一的错误消息格式

**操作**:
```python
# 统一格式
assert condition, f"[{test_name}] 期望: {expected}, 实际: {actual}"

# 示例
assert result.get("success") is True, \
    f"[添加音频] 期望: success=True, 实际: {result}"
```

---

### 任务3: 添加测试标签

**需求**: 为所有测试添加pytest标记

**操作**:
```python
# 管理后台测试
@pytest.mark.admin
@pytest.mark.create
def test_admin_add_audio(...):
    ...

# C端测试
@pytest.mark.h5
@pytest.mark.order
def test_h5_order_column(...):
    ...
```

---

## 故障预防

### 预防措施1: 定期清理缓存

```bash
# 创建清理脚本: scripts/clean_cache.sh
#!/bin/bash
rm -f api_tests/.session_cache.pkl
rm -f api_tests/.edupc_session_cache.pkl
rm -f api_tests/.h5_session_cache.pkl
rm -rf api_tests/__pycache__
rm -rf api_tests/*/__pycache__
echo "缓存已清理"
```

### 预防措施2: 版本控制忽略

```gitignore
# .gitignore
*.pkl
__pycache__/
*.pyc
.pytest_cache/
htmlcov/
.coverage
```

### 预防措施3: 持续集成检查

```yaml
# .github/workflows/test.yml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest api_tests/ -v --no-tapd-report
```

---

## 维护最佳实践

### 1. 保持测试独立
- 每个测试应该能独立运行
- 不依赖其他测试的执行顺序
- 使用fixture而不是全局变量

### 2. 使用描述性名称
```python
# 好
def test_admin_add_audio_with_valid_data():
    ...

# 不好
def test_audio():
    ...
```

### 3. 及时更新文档
- 修改测试后更新docstring
- 更新README和使用说明
- 记录重要的变更

### 4. 代码审查
- 新增测试前进行审查
- 检查代码风格一致性
- 验证断言的完整性

### 5. 监控测试健康度
- 跟踪失败率
- 记录执行时间
- 定期重构

---

## 快速参考

### 常用维护命令

```bash
# 查找所有失败的测试
pytest api_tests/ -v --lf

# 查看测试覆盖率
pytest api_tests/ --cov=api_tests --cov-report=html

# 检查代码风格
flake8 api_tests/

# 格式化代码
black api_tests/

# 清理缓存
find api_tests/ -type d -name __pycache__ -exec rm -rf {} +
```

### 维护脚本位置

```
scripts/
├── clean_cache.sh           # 清理缓存
├── update_imports.py        # 批量更新导入
├── check_test_health.py     # 检查测试健康度
└── run_test_with_tapd.py    # 执行测试
```

---

**使用此Skill后，AI将能够系统化地维护和优化API测试用例，确保测试质量和可维护性。**
