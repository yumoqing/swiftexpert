---
name: swiftexpert-repo
version: 1.0.0
description: SWIFT 仓库：472 个文件，主语言Python 22，JSON 5，Shell 1
trigger_conditions:
  - 需要理解、修改或排障 swiftexpert 的代码
  - 在 swiftexpert 里定位入口、数据表、对外契约或构建方式
---

# swiftexpert 仓库技能

> 由仓库实际内容生成的骨架（README/目录/模型定义/契约/构建脚本逐项取证）。新增判断与坑位请直接在下面对应小节补充。

## 定位

**SWIFT**

swift is a module to support swift message pack and unpack, with data validator. Support SWIFT Message standard MT 2018 Swift messages is composed by five blocks, We use a formated excel as SMDF file. it is easy to create and modify. each message identified by message type, can be description by a S

- 远端：`https://github.com/yumoqing/swiftexpert.git`
- 默认分支：`master`（共 2 个提交）
- 最近提交：2020-05-06 `76febe9` second commit
- 规模：472 个文件；Python 22，JSON 5，Shell 1

## 目录结构

- `swiftexpert/` — Python 包源码（模块本体）（378 个文件）
- `old/` — 75 个文件
- `test/` — 测试（13 个文件）
- `design/` — 1 个文件
- 根文件：`README.md`、`SMDFile.md`、`requirement.txt`、`roadmap.md`、`setup.py`

## 构建与运行

- `setup.py`：`swiftexpert` v0.1.0，依赖 0 项
- Python 包 `swiftexpert/`：`__init__.py`、`assemblyline.py`、`identifier.py`、`swift.py`、`swift_charset.py`、`swift_checker.py`、`swift_field.py`、`swift_format.py`

## README 要点与注意（摘自 `README.md`）

- 章节：Standard support、Features、swift message description file

## 建议阅读顺序

1. `README.md`

