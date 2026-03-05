# TEST_TEMPLATE

## 记录规则

* TESTMD 为条目模式（entry），按测试主题 `Key` 维护统一测试规范。
* 同一 `Key` 仅保留一个当前有效条目。
* `Key` 已存在时更新条目并刷新文件名时间戳；`Key` 不存在时新建条目。

## Metadata

* **修改者：** [执行器Agent的名称]
* **Type：** [STANDARD / ACCEPTANCE / EVAL / REGRESSION / PERFORMANCE / SECURITY / COMPATIBILITY / OTHER]
* **Key：** [测试主题唯一键]

## Summary

* [总结本条测试规范的核心内容，必须一句话，单行输出]

## Test Matrix

* [TEST-001 | 测试范围(模块/流程) | 测试类型(UNIT/INTEGRATION/E2E/EVAL/REGRESSION/PERF/SECURITY) | 测试标准(阈值/覆盖率/准确率) | 测试工具 | 通过条件]
* [TEST-002 | 测试范围(模块/流程) | 测试类型(UNIT/INTEGRATION/E2E/EVAL/REGRESSION/PERF/SECURITY) | 测试标准(阈值/覆盖率/准确率) | 测试工具 | 通过条件]
* [其他必须记录的测试矩阵细节，可以多条输出，每条一句话]

## Special Requirements

* [特殊要求（如测试前置条件、数据脱敏、灰度环境、人工复核点），可以多条输出，每条一句话]
* [特殊风险边界与豁免条件，可以多条输出，每条一句话]
* [其他必须记录的特殊要求，可以多条输出，每条一句话]

## Thought

* [本次测试规范设定的背景原因，可以多条输出，每条一句话]
* [本次标准与工具选择的判断依据，可以多条输出，每条一句话]
* [其他必须记录的测试思考，可以多条输出，每条一句话]

## Action

* [本次测试规范落地动作，可以多条输出，每条一句话]
* [本次联动更新动作（如 CHANGE/SPEC/RUN），可以多条输出，每条一句话]
* [其他必须记录的执行细节，可以多条输出，每条一句话]

## Observation

* [测试规范执行后的结果，可以多条输出，每条一句话]
* [对质量门禁、发布节奏的影响，可以多条输出，每条一句话]
* [其他必须记录的观察细节，可以多条输出，每条一句话]
