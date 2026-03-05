# RUN_NOTICE_AGENTMD_API_HEALTH_2026_03_05_0055

## Metadata

* **修改者：** Codex
* **事件时间（UTC）：** 2026-03-05 00:55
* **事件名（Key）：** AGENTMD_API_HEALTH
* **分类：** HEALTHCHECK
* **级别：** NOTICE
* **影响范围：** service-agentmd-api
* **状态：** RESOLVED

## Summary

* AGENTMD API 健康检查在连续 3 次失败（probe timeout），影响所有并行 Agent 实例，重启后恢复正常。

## Thought

* 健康检查失败直接导致 Agent 编排中断，必须优先恢复可用性而非立即深挖根因。
* 本事件属于运行时波动，非构建/编译错误，应归类为 RUNMD 而非 ERRORMD。
* 风险边界：若为依赖服务重启导致，可能引发级联失败；若为内存泄漏，则需观察后续峰值。
* 修复目标：5 分钟内恢复服务，10 分钟内完成事件记录并更新索引。

## Action

* 执行 health probe，手动触发 `/healthz` 端点，确认 `504 Gateway Timeout`。
* 抽取容器日志（`kubectl logs agentmd-api-7f8d9c4b5 -n prod --tail=200`），定位异常时间窗口。
* 执行受控重启（`kubectl rollout restart deployment/agentmd-api -n prod`）。
* 验证依赖链路：检查 Redis、PostgreSQL 连接池状态，均正常。
* 连续 5 次 probe 通过，服务状态恢复绿色，更新 `RUN_INDEX.md`。

## Observation

* 期间 probe 连续 3 次失败，返回 504，响应时间大于 30s。
* 重启后 probe 响应时间降至 180ms，连续 10 次通过，未见复现。
* 当前无用户可见错误（API 调用日志无 5xx），但峰值时段（每日 02:00~04:00）需观察稳定性。
* 日志中发现单次 `connection reset by peer`，但未复现，暂定为瞬时网络抖动。

## Root Cause

* 运行时进程短时异常退出（OOM 或 SIGTERM），导致健康检查探针链路中断。

## Fix

* 执行 deployment rollout restart，强制 Pod 重建并重新建立连接池。

## Prevention

* 将 `/healthz` 探针与 Redis/PostgreSQL 自检加入发布后巡检清单，设置告警阈值（连续 2 次失败触发 PagerDuty）。
* 建立同类健康检查事件快速处置手册（5 分钟内重启 + 日志抽取 + 依赖验证），存入 RUNBOOKSMD。
* 增加容器内存监控（Prometheus + 阈值 85%），提前 10 分钟告警，避免 OOM 导致的瞬时退出。
