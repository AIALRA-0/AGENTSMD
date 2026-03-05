# API_EXTERNAL_OPENAI_RESPONSES_2026_03_05_0713

## Metadata

* **修改者：** Codex
* **Type：** EXTERNAL
* **Key：** OPENAI_RESPONSES

## Summary

* 固化 OpenAI Responses API 的接入说明、鉴权规则、用量口径与维护流程，降低外部依赖调用漂移风险。

## Source

* SRC-001 | 类型(WEB) | <https://platform.openai.com/docs/api-reference/responses> | Responses API 官方端点与参数定义来源
* SRC-002 | 类型(WEB) | <https://platform.openai.com/docs/guides/rate-limits> | 官方限流与配额说明来源
* SRC-003 | 类型(LOCAL_FILE) | /aialra/AGENTSMD/STYLEMD/STYLE_SUFFIX_MD_2026_03_05_0636.md | 文档风格与示例写法约束来源

## Endpoint

* API-001 | 方法(POST) | <https://api.openai.com/v1/responses> | 发起文本/多模态响应请求 | body={model,input,...} | 200 返回 response 对象与 output
* API-002 | 方法(GET) | <https://api.openai.com/v1/responses/{response_id}> | 查询单次响应详情 | path={response_id} | 200 返回指定响应对象
* API-003 | 方法(DELETE) | <https://api.openai.com/v1/responses/{response_id}> | 删除指定响应记录 | path={response_id} | 200 返回删除结果

## Usage

* 调用前置条件：请求头必须包含 `Authorization: Bearer <OPENAI_API_KEY>` 与 `Content-Type: application/json`。
* 最小调用示例：`curl https://api.openai.com/v1/responses -H 'Authorization: Bearer $OPENAI_API_KEY' -H 'Content-Type: application/json' -d '{\"model\":\"gpt-5\",\"input\":\"hello\"}'`。
* 错误处理：429 按退避策略重试并降并发；401 立即中止并检查密钥；5xx 最多重试 3 次且记录失败样本。

## Token Policy

* 鉴权方式：使用 Bearer API Key，密钥通过环境变量 `OPENAI_API_KEY` 注入运行时。
* token 来源：由外部密钥管理或部署平台注入，禁止写入仓库、日志、索引与样例正文。
* token 轮换：建议 30~90 天轮换一次，轮换后必须执行健康检查请求验证新密钥可用。
* 安全边界：不同环境（dev/staging/prod）使用独立 key，并按最小权限原则隔离用途。

## Quota & Maintenance

* 用量口径：按请求数、输入/输出 token、错误率、平均延迟（P95）做日级统计。
* 配额与限流：超出阈值时优先降级非关键任务并触发告警，避免核心流程被全局限流阻断。
* 维护流程：模型版本调整、参数策略变更或 SDK 升级时，必须联动更新 `TESTMD` 与 `TOOLMD`。

## Thought

* 外部 API 变化频繁，若不结构化记录端点与配额策略，调用行为会在多 Agent 场景下快速漂移。
* token 与配额是稳定性与成本的核心约束，必须与用法一起沉淀而不是分散在脚本里。
* 通过单条目维护 `OPENAI_RESPONSES` 可在升级模型时保持变更面可控。

## Action

* 依据官方文档重建 `OPENAI_RESPONSES` 条目并补齐端点、鉴权、限流与维护信息。
* 明确错误处理与重试策略，降低上游抖动对工作流稳定性的影响。
* 同步更新 `API_INDEX.md`，将该条目标记为当前有效入口。

## Observation

* 当前条目可直接用于新接入与故障排查，避免重复查文档导致执行偏差。
* token 管理与配额策略已明确，便于后续成本评估与发布门禁联动。
* 条目已覆盖内外部 API 对齐所需关键字段，可作为 APIMD 的基线样例。
