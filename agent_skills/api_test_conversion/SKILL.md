# API用例转换 Skill

**版本**: v1.0  
**创建时间**: 2026-02-11  
**用途**: 标准化cURL命令到Pytest API测试用例的转换流程

---

## 何时使用此Skill

当用户提供以下内容时，自动触发此Skill：
- cURL命令
- API接口信息
- 要求"转换API测试"、"生成测试用例"等关键词

---

## 转换流程

### 步骤1: 分析cURL命令

从cURL中提取：
1. **请求方法**: GET/POST/PUT/DELETE
2. **URL**: 完整的API端点
3. **请求头**: Content-Type, Cookie等
4. **请求体**: data-raw中的参数
5. **认证信息**: 从Cookie或Header提取

### 步骤2: 识别用例信息

从用户提供的信息中提取：
1. **用例ID**: TAPD用例ID（格式: 1150695810001062XXX）
2. **用例名称**: 中文描述
3. **终端类型**: admin/edupc/h5
4. **业务类型**: 创建/查询/更新/删除/订单流程

### 步骤3: 确定测试文件位置

根据终端类型确定目录：
```
admin终端 → api_tests/admin/test_add_*.py
edupc终端 → api_tests/edupc/test_*.py
h5终端 → api_tests/h5/test_*.py
```

### 步骤4: 生成测试代码

#### 模板结构
```python
"""
用例 ID: {TAPD_ID}
用例名称: {用例名称}

接口: {HTTP方法} {API路径}
"""

def test_{function_name}({client_fixture}, timestamp):
    \"""测试函数docstring\"""
    
    # 1. 准备测试数据（使用动态数据）
    name = f"{前缀}{timestamp}"
    
    # 2. 调用API
    result = {client}.{method}(
        "{api_path}",
        data={
            # 参数映射
        },
        headers={
            # 请求头
        }
    )
    
    # 3. 断言验证
    assert result.get("success") is True, f"操作失败: {result}"
    
    # 4. 提取关键数据（如果需要）
    item_id = result.get("data", {}).get("id") or result.get("id")
    assert item_id, f"未返回ID: {result}"
    
    print(f"[OK] 测试完成: id={item_id}, name={name}")
```

### 步骤5: 动态数据处理

**命名规则**:
- 使用`timestamp` fixture生成6位时间戳
- 格式: `{类型}{timestamp}` (如: 音频123456)
- 长度限制: 优惠券≤10字符，其他≤20字符

**特殊字段**:
- `fileId`: 使用固定的测试文件ID
- `wxappId/wxappAid`: 从client获取
- `stuId`: 从client获取（C端）
- `TOKEN`: 从client获取（C端）

### 步骤6: 断言策略

**基础断言**:
```python
assert result.get("success") is True
```

**ID提取（灵活处理多种响应格式）**:
```python
item_id = (
    result.get("data", {}).get("id") or
    result.get("data", {}).get("{type}Id") or
    result.get("id") or
    result.get("data")
)
```

**特殊情况**:
- 兑换码创建: 不返回ID，仅验证success
- 优惠券: ID在`result["coupon"]["id"]`
- 表单: ID可能是`formId`

### 步骤7: 接口关联处理

**订单流程（C端）**:
```python
# 步骤1: 提交订单
order_result = client.post("/api/.../commitOrder", ...)
order_no = order_result["data"]["orderNo"]

# 步骤2: 查询订单详情（通过admin_client）
order_detail = admin_client.get("/api/manage/order/v2/getOrderDetails", 
                                 params={"orderNo": order_no})
order_item_id = order_detail["data"]["orderInfo"]["itemList"][0]["orderItemId"]

# 步骤3: 退款
refund_result = admin_client.post("/api/manage/refund/refundOrder",
                                   data={"orderItemId": order_item_id, ...})
```

---

## 代码生成规范

### 1. 文件命名
```
管理后台: test_add_{resource}.py
EduPC: test_{action}_{resource}.py
H5: test_{action}_{resource}.py
```

### 2. 函数命名
```python
# 管理后台
def test_admin_add_audio(admin_client, timestamp):

# EduPC
def test_edupc_order_column(edupc_client, admin_client):

# H5
def test_h5_order_news(h5_client, admin_client):
```

### 3. 模块docstring
```python
"""
用例 ID: 1150695810001062392
用例名称: 管理后台正常添加音频课程

接口: POST /ajax/wxAppAudio_h.jsp?cmd=add
"""
```

### 4. 函数docstring
```python
def test_admin_add_audio(admin_client, timestamp):
    """管理后台正常添加音频课程"""
```

### 5. 注释规范
```python
# ===== 步骤1: 准备测试数据 =====
# ===== 步骤2: 调用API =====
# ===== 步骤3: 验证结果 =====
```

---

## Client Fixture使用

### admin_client
```python
# 管理后台客户端
result = admin_client.post(
    "/ajax/wxAppAudio_h.jsp",
    data={"cmd": "add", ...},
    headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
)
```

### edupc_client
```python
# EduPC客户端
result = edupc_client.post(
    "/api/guestAuth/pcOrder/v2/commitOrder",
    data={
        "TOKEN": edupc_client._token,
        "stuId": edupc_client.stu_id,
        ...
    }
)
```

### h5_client
```python
# H5客户端
result = h5_client.post(
    "/api/guestAuth/order/v2/commitOrder",
    data={
        "TOKEN": h5_client._token,
        "stuId": h5_client.stu_id,
        ...
    }
)
```

---

## 常见参数映射

### 管理后台
```python
{
    "_TOKEN": admin_client._token,
    "wxappAid": admin_client.wxapp_aid,
    "wxappId": admin_client.wxapp_id,
    "cmd": "add",  # 或其他操作
    "name": f"{类型}{timestamp}",
    ...
}
```

### C端（EduPC/H5）
```python
{
    "aid": client.aid,
    "wxappId": client.wxapp_id,
    "wxappAid": client.wxapp_aid,
    "TOKEN": client._token,
    "stuId": client.stu_id,
    "edu_aid": client.edu_aid,
    ...
}
```

---

## 错误处理

### 常见错误及解决方案

**1. 名称长度超限**
```python
# 错误: 优惠券名称超过10字符
coupon_name = f"优惠券{timestamp}"  # 可能11字符

# 正确: 控制在10字符内
coupon_name = f"券{timestamp}"  # 7字符
```

**2. 敏感词过滤**
```python
# 错误: 包含敏感词
name = f"TEST_COUPON_{timestamp}"

# 正确: 使用中文或简单前缀
name = f"券{timestamp}"
```

**3. ID提取失败**
```python
# 错误: 固定路径
item_id = result["data"]["id"]

# 正确: 多路径尝试
item_id = (
    result.get("data", {}).get("id") or
    result.get("id") or
    result.get("data")
)
```

---

## 完整示例

### 示例1: 管理后台创建类

**输入**:
```
用例ID: 1150695810001062392
用例名称: 管理后台正常添加音频课程
cURL: curl 'http://i.edu.fkw.com.faidev.cc/ajax/wxAppAudio_h.jsp?...' \
  --data-raw 'cmd=add&name=测试音频&fileId=xxx...'
```

**输出**:
```python
"""
用例 ID: 1150695810001062392
用例名称: 管理后台正常添加音频课程

接口: POST /ajax/wxAppAudio_h.jsp?cmd=add
"""

def test_admin_add_audio(admin_client, timestamp):
    """管理后台正常添加音频课程"""
    name = f"音频{timestamp}"
    
    result = admin_client.post(
        "/ajax/wxAppAudio_h.jsp",
        data={
            "cmd": "add",
            "wxappId": "110",
            "name": name,
            "fileId": "AJQBCAAQNxgAIKrF18sGKICiiKQCMAA4AA",
            ...
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    
    assert result.get("success") is True, f"添加失败: {result}"
    
    audio_id = result.get("data", {}).get("id") or result.get("id")
    assert audio_id, f"未返回音频ID: {result}"
    
    print(f"[OK] 音频添加成功: id={audio_id}, name={name}")
```

### 示例2: C端订单流程

**输入**:
```
用例ID: 1150695810001062372
用例名称: H5端正常提交系列课订单并管理后台退款
终端: H5
流程: 提交订单 → 查询详情 → 退款
```

**输出**:
```python
"""
用例 1150695810001062372: H5端正常提交系列课订单并管理后台退款

流程：
1. H5端提交系列课订单
2. 管理后台查询订单详情获取orderItemId
3. 管理后台退款
"""

def test_h5_order_column_and_refund(h5_client, admin_client):
    """H5端提交系列课订单 -> 管理后台退款"""
    
    # ===== 步骤1: H5端提交订单 =====
    print(f"[H5] 开始提交系列课订单...")
    
    stu_id = h5_client.stu_id or "57711"
    
    order_result = h5_client.post(
        "/api/guestAuth/order/v2/commitOrder",
        data={
            "aid": h5_client.aid,
            "TOKEN": h5_client._token,
            "stuId": stu_id,
            "serviceType": "5",
            "serviceId": "1157",
            ...
        }
    )
    
    assert order_result.get("success") is True
    order_no = order_result["data"]["orderNo"]
    
    # ===== 步骤2: 管理后台查询订单详情 =====
    order_detail = admin_client.get(
        "/api/manage/order/v2/getOrderDetails",
        params={"orderNo": order_no}
    )
    
    order_item_id = order_detail["data"]["orderInfo"]["itemList"][0]["orderItemId"]
    
    # ===== 步骤3: 管理后台退款 =====
    refund_result = admin_client.post(
        "/api/manage/refund/refundOrder",
        data={
            "orderItemId": order_item_id,
            "orderNo": order_no,
            ...
        }
    )
    
    assert refund_result.get("success") is True
    print(f"[OK] 用例完成: 订单 {order_no} 已成功退款")
```

---

## 执行检查清单

转换完成后，确保：
- [ ] 用例ID已添加到模块docstring
- [ ] 使用了正确的client fixture
- [ ] 动态数据使用timestamp
- [ ] 名称长度符合限制
- [ ] 断言逻辑完整
- [ ] 打印输出清晰
- [ ] 代码格式规范
- [ ] 无emoji字符（Windows兼容）

---

## 测试验证

生成代码后立即执行测试：
```bash
pytest api_tests/{module}/test_{name}.py -v -s
```

如果失败，根据错误信息调整：
1. API响应结构不匹配 → 调整ID提取逻辑
2. 参数错误 → 检查cURL映射
3. 认证失败 → 确认client配置

---

**使用此Skill后，AI将自动按照上述标准流程转换所有API用例，确保一致性和质量。**
