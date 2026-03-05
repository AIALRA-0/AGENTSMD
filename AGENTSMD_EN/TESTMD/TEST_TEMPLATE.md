# TEST_TEMPLATE

## Record rules

* TESTMD for entry mode（entry），by test topic `Key` Maintain unified testing specifications。
* same `Key` Keep only one currently valid entry。
* `Key` Update the entry if it already exists and refresh the filename timestamp；`Key` Create a new entry if it does not exist。

## Metadata

* **Modifier：** [actuatorAgentname]
* **Type：** [STANDARD / ACCEPTANCE / EVAL / REGRESSION / PERFORMANCE / SECURITY / COMPATIBILITY / OTHER]
* **Key：** [Test subject unique key]

## Summary

* [Summarize the core content of this test specification，A word is necessary，Single line output]

## Test Matrix

* [TEST-001 | Test range(module/process) | Test type(UNIT/INTEGRATION/E2E/EVAL/REGRESSION/PERF/SECURITY) | Test standards(threshold/Coverage/Accuracy) | testing tools | pass conditions]
* [TEST-002 | Test range(module/process) | Test type(UNIT/INTEGRATION/E2E/EVAL/REGRESSION/PERF/SECURITY) | Test standards(threshold/Coverage/Accuracy) | testing tools | pass conditions]
* [Other test matrix details that must be recorded，Multiple outputs possible，One sentence per item]

## Special Requirements

* [special request（Such as testing preconditions、Data desensitization、Grayscale environment、manual review point），Multiple outputs possible，One sentence per item]
* [Special risk boundaries and exemption conditions，Multiple outputs possible，One sentence per item]
* [Other special requirements that must be recorded，Multiple outputs possible，One sentence per item]

## Thought

* [The background reasons for setting this test specification，Multiple outputs possible，One sentence per item]
* [The basis for judging the selection of this standard and tool，Multiple outputs possible，One sentence per item]
* [Other test reflections that must be documented，Multiple outputs possible，One sentence per item]

## Action

* [This test specifies landing actions，Multiple outputs possible，One sentence per item]
* [This linkage update action（Such as CHANGE/SPEC/RUN），Multiple outputs possible，One sentence per item]
* [Other implementation details that must be recorded，Multiple outputs possible，One sentence per item]

## Observation

* [The results after the test specification is executed，Multiple outputs possible，One sentence per item]
* [Quality control、The impact of release cadence，Multiple outputs possible，One sentence per item]
* [Other observation details that must be recorded，Multiple outputs possible，One sentence per item]
