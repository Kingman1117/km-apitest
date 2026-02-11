# Skill + MCP 自动化验收测试方案

> 基于 AI Agent + Playwright MCP 实现 TAPD 测试用例的智能化执行
> 
> **归档说明**: 此为旧方案文档，项目已转为API优先测试策略

---

## 方案概述

本方案通过 **AI Skill（知识库）** 与 **Playwright MCP（浏览器自动化协议）** 的结合，实现从 TAPD 测试平台读取测试用例，并自动执行 UI 验收测试。

## 核心价值

- 从"写代码"到"写用例"
- 智能化测试执行
- 自然语言驱动的智能自动化

## 技术架构

- AI Agent (Claude)
- Skill 知识库
- Playwright MCP
- 浏览器实例

## Token 消耗优化

优化策略：
1. 精简 Skill 文档（节省 73%）
2. 减少 browser_snapshot 调用
3. 使用 browser_run_code 批量操作

---

*文档版本：v1.1*  
*归档日期：2026-02-11*  
*原因：项目已转为纯API测试策略*
