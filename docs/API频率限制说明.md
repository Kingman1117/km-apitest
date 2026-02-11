# API频率限制说明

## 问题描述

服务端对订单提交等接口有**频率限制**，连续快速请求会被拦截。

### 错误信息
```json
{
  "msg": "服务频繁提交请求，请稍后重试",
  "rt": -1,
  "success": false
}
```

---

## 解决方案

### 方案1：自动延时（已实现）

在 `api_tests/conftest.py` 中添加了 `rate_limit_delay` fixture：

```python
@pytest.fixture(autouse=True)
def rate_limit_delay():
    """自动在每个测试用例之间添加2秒延时"""
    yield  # 测试执行
    time.sleep(2)  # 测试完成后等待2秒
```

**优点**：
- 自动生效，无需修改测试代码
- 适用于所有测试用例
- 避免频率限制错误

**缺点**：
- 增加总执行时间（每个用例+2秒）

---

### 方案2：分批执行

将测试用例分成多批执行，每批之间手动间隔：

```bash
# 批次1：管理后台创建类
pytest api_tests/test_admin_add_*.py -v

# 等待5秒

# 批次2：EduPC订单
pytest api_tests/test_c0[1-5]*.py -v

# 等待5秒

# 批次3：H5订单
pytest api_tests/test_c0[6-9]*.py -v
pytest api_tests/test_c1*.py -v
```

---

### 方案3：单个执行

对于调试或单独验证，逐个执行：

```bash
pytest api_tests/test_c06_h5_order_news.py -v
# 等待3秒
pytest api_tests/test_c07_h5_order_audio.py -v
```

---

## 受影响的接口

### 高频率限制接口
- ✓ `/api/guestAuth/order/v2/commitOrder` (订单提交)
- ✓ `/api/guestAuth/pcOrder/v2/commitOrder` (PC端订单提交)

### 低频率限制接口
- 管理后台创建类接口（音频、视频等）
- 查询类接口（订单详情、商品列表等）
- 退款接口

---

## 最佳实践

1. **开发调试阶段**：
   - 使用方案3（单个执行）
   - 手动控制执行间隔

2. **CI/CD自动化**：
   - 使用方案1（自动延时）
   - 确保稳定性

3. **本地完整测试**：
   - 使用方案2（分批执行）
   - 平衡速度和稳定性

---

## 配置调整

如果需要调整延时时间，修改 `conftest.py`：

```python
@pytest.fixture(autouse=True)
def rate_limit_delay():
    yield
    time.sleep(3)  # 改为3秒
```

---

## 监控建议

如果仍然遇到频率限制错误：
1. 增加延时时间（2秒 → 3秒 → 5秒）
2. 检查是否有其他进程在并发访问API
3. 联系后端团队确认频率限制策略

---

**更新时间**: 2026-02-11  
**负责人**: 自动化测试团队
