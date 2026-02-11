# 用例操作脚本格式规范

## 概述
每条 TAPD 测试用例对应一个 JSON 脚本文件，包含确定性的操作步骤。
AI 执行时按脚本逐步调用 MCP 工具，仅在异常时才 snapshot 分析。

## 文件命名
`{caseId}.json` 如 `1150695810001062388.json`

## 脚本结构
```json
{
  "caseId": "用例ID",
  "name": "用例名称",
  "group": "分组标识",
  "needsLogin": "admin|student_h5|student_edupc|none",
  "steps": [ ... ],
  "cleanup": null | { "type": "refund|writeOff", ... },
  "verify": "最终验证的关键文本/URL片段"
}
```

## Action 类型定义

### goto - 页面导航
```json
{ "action": "goto", "url": "完整URL" }
```

### wait - 等待
```json
{ "action": "wait", "ms": 2000 }
```

### click - 点击元素
```json
{
  "action": "click",
  "selector": "主选择器",
  "fallbacks": ["备选选择器1", "备选选择器2"],
  "force": true,
  "description": "操作说明"
}
```

### fill - 填写输入框
```json
{
  "action": "fill",
  "selector": "输入框选择器",
  "value": "填写的值",
  "description": "操作说明"
}
```
value 支持变量：
- `{timestamp}` → Date.now() 后8位
- `{date}` → yyyyMMddHHmmss

### selectResource - 从资源库选择文件
```json
{
  "action": "selectResource",
  "type": "image|video|audio|ebook|file",
  "description": "选择封面图片"
}
```
内部逻辑：
- image → 点 `.fa-basic-upload-view-ui-file-layer--content`
- video/audio/ebook/file → 点 `.fa-basic-upload-file-view-list-item.file`
- 然后点确定按钮

### fillSpinbutton - 填写数字输入框
```json
{
  "action": "fillSpinbutton",
  "index": 0,
  "value": "0.01",
  "description": "填写价格"
}
```

### evaluate - 执行JavaScript
```json
{
  "action": "evaluate",
  "script": "JavaScript代码字符串",
  "description": "操作说明"
}
```

### iframe - iframe内操作
```json
{
  "action": "iframe",
  "iframeSelector": "#mainIframe",
  "steps": [
    { "action": "fill", "selector": "input", "value": "xxx" },
    { "action": "click", "selector": "text=登录" }
  ]
}
```

### iframeClick - 简写的iframe内点击
```json
{
  "action": "iframeClick",
  "iframeSelector": "#mainIframe",
  "selector": "text=购买",
  "force": true
}
```

### submitOrder - H5/edupc 提交订单（封装）
```json
{
  "action": "submitOrder",
  "platform": "h5|edupc",
  "useBalance": true,
  "iframeSelector": "#mainIframe",
  "description": "使用余额抵扣并提交订单"
}
```
内部逻辑（h5）：
1. 在 iframe 内找"使用"按钮启用余额抵扣
2. 勾选购课协议（`.fu-checkbox__icon-wrap` 最后一个）
3. 点击"提交订单"

### checkAgreement - 勾选购课协议
```json
{ "action": "checkAgreement" }
```

### refund - 退款清理
```json
{
  "action": "refund",
  "adminOrderUrl": "http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1#/order/index"
}
```

### writeOff - 核销（实物商品）
```json
{
  "action": "writeOff",
  "adminOrderUrl": "http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1#/order/index"
}
```

### verify - 验证结果
```json
{
  "action": "verify",
  "expect": "成功文本1|成功文本2|url_contains:xxx",
  "snapshot": true,
  "description": "验证创建成功"
}
```

### snapshot - 获取页面快照（仅必要时）
```json
{
  "action": "snapshot",
  "reason": "需要AI分析当前页面状态"
}
```

## 执行规则
1. 按 steps 数组顺序逐步执行
2. 每步执行后如果没有 verify，默认等 500ms 继续下一步
3. click 失败时依次尝试 fallbacks
4. 所有 fallbacks 都失败时才 snapshot 让 AI 分析
5. verify 步骤必须 snapshot 确认结果
6. cleanup 在 verify 通过后执行
