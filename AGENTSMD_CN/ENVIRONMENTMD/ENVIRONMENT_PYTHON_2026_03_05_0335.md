# ENVIRONMENT_PYTHON_2026_03_05_0335

## Metadata

* **修改者：** Codex
* **Key：** PYTHON

## Summary

* 记录当前 Python 运行环境真实参数（版本/路径/pip/平台），作为脚本执行与排障基线。

## Thought

* 文档与校验脚本直接依赖 Python 运行环境，缺失该信息会增加排障不确定性。
* 在执行自动化脚本前需要确认 Python 解释器与可调用状态是否正常。
* 该条目用于后续环境变更时快速判断是否由 Python 环境差异导致问题。

## Action

* 执行 `python3 --version` 获取 Python 主版本信息。
* 执行 `which python3` 获取 Python 可执行路径。
* 执行 `python3 -c "import sys,platform;..."` 获取完整解释器与平台信息。
* 执行 `python3 -m pip --version` 获取 pip 版本与安装路径。
* 按 ENVIRONMENT 模板创建 `Key=PYTHON` 的环境条目。
* 同步更新 `ENVIRONMENT_INDEX.md`，将该条目标记为当前最新记录。

## Observation

* 采集时间（UTC）=2026-03-05 03:36 UTC。
* Python 版本=3.11.2。
* Python 可执行路径=`/usr/bin/python3`。
* Python 完整构建信息=`3.11.2 (main, Apr 28 2025, 14:11:48) [GCC 12.2.0]`。
* 运行平台=`Linux-6.8.0-100-generic-x86_64-with-glibc2.36`。
* pip 版本=`23.0.1`，安装路径=`/usr/lib/python3/dist-packages/pip`。
* Python 运行环境可用，可支持当前 AGENTSMD 脚本执行。
* 该条目可作为后续依赖异常、脚本失败场景的快速对照基线。
