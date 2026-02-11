# Playwright MCP 在 Cursor 中的配置说明

## 一、配置位置（Cursor 读取的是用户级配置）

- **Windows**：`%USERPROFILE%\.cursor\config\mcp.json`  
  例如：`C:\Users\你的用户名\.cursor\config\mcp.json`
- **macOS/Linux**：`~/.cursor/config/mcp.json`

项目根目录的 `mcp.json` 仅作模板参考，Cursor 实际使用的是上述用户目录下的文件。

---

## 二、配置方式（任选其一）

### 方式 A：通过 Cursor 设置界面（推荐）

1. 打开 **Cursor** → **Settings**（设置）
2. 进入 **Features** → **MCP**，或 **Tools & Integrations** → **MCP Servers**
3. 点击 **+ Add New MCP Server**
4. 填写：
   - **Name**：`playwright`
   - **Command**：`npx`
   - **Args**：`-y`, `@executeautomation/playwright-mcp-server`
5. 保存后重启 Cursor 或重新加载 MCP

### 方式 B：直接编辑用户级 mcp.json

1. 确保目录存在：  
   - Windows：`C:\Users\你的用户名\.cursor\config\`  
   - 若没有 `config` 文件夹，请先创建。
2. 在该目录下创建或编辑 `mcp.json`，内容如下（若已有其他 MCP，把 `playwright` 块合并进现有 `mcpServers` 即可）：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"],
      "disabled": false
    }
  }
}
```

3. 保存文件后，重启 Cursor。

---

## 三、本项目前置准备（在项目目录执行）

在项目根目录 `E:\MCP测试\kmsk` 下执行：

```bash
# 1. 安装 Node 依赖（含 Playwright MCP Server）
npm install

# 2. 安装浏览器（MCP 首次使用也会自动安装，可先手动安装以验证环境）
npx playwright install chromium
```

如需安装全部浏览器：

```bash
npx playwright install
```

---

## 四、验证 MCP 是否生效

1. 重启 Cursor 后，在 Composer/Agent 对话中应能看到 Playwright 相关工具（如 `playwright_navigate`、`playwright_click` 等）。
2. 或打开 **Settings** → **MCP**，确认 `playwright` 为已连接/已启用状态。
3. 若 Cursor 从项目目录启动 MCP 进程，请先在项目目录执行过 `npm install`，以便 `npx` 能正确解析到 `@executeautomation/playwright-mcp-server`。

---

## 五、常见问题

| 现象 | 处理建议 |
|------|----------|
| MCP 列表里没有 playwright | 检查用户级 `mcp.json` 路径和 JSON 格式；重启 Cursor。 |
| 工具报错或无法调用 | 在项目目录执行 `npm install` 和 `npx playwright install chromium`。 |
| 浏览器未安装 | 首次使用 MCP 时会自动下载；也可手动执行 `npx playwright install chromium`。 |
| 修改配置后无变化 | 完全退出 Cursor 再重新打开，或重新加载 MCP。 |

---

## 六、参考

- [Cursor MCP 文档](https://docs.cursor.com/context/mcp)
- [Playwright MCP Server (npm)](https://www.npmjs.com/package/@executeautomation/playwright-mcp-server)
