# TEST_STANDARD_QA_BASELINE_2026_03_05_0655

## Metadata

* **修改者：** Codex
* **Type：** STANDARD
* **Key：** QA_BASELINE

## Summary

* 固化项目级测试与评估基线，明确各阶段测试范围、标准阈值、工具链与特殊门禁要求。

## Test Matrix

* TEST-001 | AGENTS 规则文档变更 | REGRESSION | 所有受保护模板与索引字段一致性 100% | scripts/md_validate.py | 校验无错误且索引可定位最新条目
* TEST-002 | 部门条目新增或更新 | EVAL | 记录结构完整率=100%，必填区块不得缺失 | scripts/md_validate.py + 人工复核 | Metadata/Summary/核心区块齐全且单行约束通过
* TEST-003 | 自动化脚本修改 | INTEGRATION | lint + validate + index sync 全链路通过 | scripts/check_markdown.sh + scripts/md_sync.sh | 三步执行均成功且无失败清单
* TEST-004 | 发布前质量门禁 | E2E | 关键工作流（需求分析/编码实施/运行排障）可按索引闭环执行 | 人工演练 + 脚本校验 | 三条工作流均可从 AGENTS 跳转到正确部门并完成落库
* TEST-005 | 安全事件处置规范 | SECURITY | SECURITY 条目 Linkage 覆盖率=100% | scripts/md_validate.py + 人工复核 | 每条 SECURITY 至少联动一个 RUN 或 ERROR 条目

## Special Requirements

* 涉及受保护文件（AGENTS、TEMPLATE、INDEX、校验脚本）变更时，必须先完成外部确认再执行测试。
* 涉及生产环境风险的演练（如安全处置、回滚流程）必须使用脱敏数据与隔离环境，不得直连真实生产凭据。
* 关键门禁失败不得“带病继续”，必须先修复后再重新执行完整测试闭环。

## Thought

* 当前框架已进入多部门并行迭代阶段，若无统一测试标准将快速出现格式漂移与门禁失效。
* 测试规范必须覆盖“文档规则正确性 + 自动化脚本可执行性 + 工作流可回放性”三层目标。
* 将标准阈值写入矩阵可以减少口头约定，避免不同执行器对“通过”定义不一致。

## Action

* 建立 `QA_BASELINE` 主题测试条目并写入可量化测试矩阵。
* 将脚本工具链（lint/validate/sync）纳入统一通过条件，形成固定闭环。
* 同步更新 `TEST_INDEX.md`，将该条目标记为当前有效测试基线入口。

## Observation

* 当前测试条目可直接指导后续部门扩展，不需要每次重复定义测试口径。
* 关键质量门禁已可被显式审查，降低“规则写了但没人执行”的风险。
* 后续若新增部门或脚本，只需在同 `Key=QA_BASELINE` 条目迭代更新并刷新时间戳即可。
