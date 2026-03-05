# API_INTERNAL_AUTH_LOGIN_2026_03_05_0712

## Metadata

* **修改者：** Codex
* **Type：** INTERNAL
* **Key：** AUTH_LOGIN

## Summary

* 固化内部登录认证 API 的端点、调用方式、鉴权策略、限流阈值与维护责任，作为安全与回归测试基线。

## Source

* SRC-001 | 类型(LOCAL_FILE) | /aialra/AGENTSMD/SPECMD/SPEC_V1.0.0_2026_03_05_0619.md | 登录流程与规格约束来源
* SRC-002 | 类型(LOCAL_FILE) | /aialra/AGENTSMD/SECURITYMD/SECURITY_ERROR_LOGIN_BRUTEFORCE_2026_03_05_0055.md | 安全风控与暴力破解处置约束来源
* SRC-003 | 类型(LOCAL_FILE) | /aialra/AGENTSMD/TESTMD/TEST_STANDARD_QA_BASELINE_2026_03_05_0655.md | 登录接口测试门禁与通过标准来源

## Endpoint

* API-001 | 方法(POST) | /api/v1/auth/login | 用户登录并获取会话令牌 | body={email,password,captcha?} | 200 返回 access_token/refresh_token 与用户摘要
* API-002 | 方法(POST) | /api/v1/auth/refresh | 刷新 access token | body={refresh_token} | 200 返回新 access_token
* API-003 | 方法(POST) | /api/v1/auth/logout | 注销当前会话并撤销 token | header=Authorization + body={refresh_token?} | 200 返回注销成功状态

## Usage

* 调用前置条件：客户端必须完成 captcha 或等效风控校验，且请求体字段完整。
* 最小调用示例：`curl -X POST https://<host>/api/v1/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"***\",\"password\":\"***\"}'`。
* 错误处理：401/403 不重试；429 按 `Retry-After` 退避重试；5xx 采用指数退避最多 3 次。

## Token Policy

* 鉴权方式：登录后使用 `Authorization: Bearer <access_token>` 访问受保护资源。
* token 来源：服务端签发 JWT，客户端只存放短期 access_token，refresh_token 受 HttpOnly/Secure cookie 保护。
* token 生命周期：access_token=15 分钟，refresh_token=7 天；超时必须重新登录。
* token 安全边界：禁止把 token 写入日志、文档或代码仓库；示例仅允许脱敏占位符。

## Quota & Maintenance

* 用量口径：按登录请求数（QPS）、失败率、429 比例、鉴权延迟（P95）监控。
* 限流策略：单 IP 登录接口上限 60 req/min，连续失败超过阈值触发验证码与临时封禁。
* 维护流程：接口变更需联动更新 `SPECMD` 与 `TESTMD`，上线后由 API 负责人执行 24h 观察。

## Thought

* 登录接口同时承载业务入口与安全边界，必须将功能约束与风控约束放在同一条目维护。
* 将 token 策略写成规则而非写明文，可兼顾可执行性与安全合规。
* 明确限流与维护责任可减少线上故障时的责任不清与响应延迟。

## Action

* 按 APIMD 模板重建 `AUTH_LOGIN` 条目并补齐端点、鉴权、用量、维护信息。
* 统一内部 API 的调用示例、错误处理与 token 管理口径，降低多 Agent 接入偏差。
* 同步更新 `API_INDEX.md`，将该条目标记为当前有效入口。

## Observation

* 当前条目已能直接指导登录接口的接入、排障、安全审查与回归测试。
* token 与限流策略已经结构化沉淀，后续变更可在同 `Key` 下持续迭代。
* 与 `SECURITYMD`、`TESTMD`、`SPECMD` 的联动关系已明确，可支持跨部门快速追踪。
