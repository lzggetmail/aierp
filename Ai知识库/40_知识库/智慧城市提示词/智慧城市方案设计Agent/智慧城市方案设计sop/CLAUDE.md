# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本代码库中工作时提供指导。

## 仓库概述

这是一个智慧城市方案设计 SOP（标准操作流程）系统 - 一个基于模块化技能的 AI 智能体系统，用于生成完整的智慧城市项目方案。系统通过结构化的 9 步工作流处理用户输入，生成专业的智慧城市解决方案文档。

**核心特征**：这是一个中文系统，用于生成中文智慧城市项目方案（智慧城市方案）。所有面向用户的内容、提示词和输出均使用中文。

## 架构设计

### 模块化技能系统

系统采用**基于技能的架构**，每个处理步骤都实现为独立的"Skill"模块：

- **SmartCity_SOP_Main** - 主控编排器，管理整个工作流
- **SmartCity_Project_Initiator** - 项目初始化与数据收集
- **SmartCity_Data_Checker** - 多格式数据校验（PDF、Excel、CAD、音频）
- **SmartCity_Info_Summary** - 核心信息提取与总结
- **SmartCity_Project_Understand** - 项目理解与业务模块划分
- **SmartCity_Tech_Selection** - 技术方案与软硬件选型
- **SmartCity_Scheme_Writer** - 方案内容撰写（逐章进行）
- **SmartCity_Scheme_Revise** - 基于用户反馈的内容修订
- **SmartCity_Scheme_Output** - 最终交付物生成（文档、表格、指南）

### 数据流转

所有技能通过 `skills/standard-io-format.md` 中定义的**标准化 JSON 格式**进行通信。每个技能遵循相同的输入/输出合约：

```json
{
  "project_id": "SC202601260001",
  "module_name": "SmartCity_*",
  "execute_status": "成功/失败/需用户确认",
  "module_data": {...},
  "error_info": null,
  "next_module": "Next_Module_Name",
  "user_confirm_msg": "..."
}
```

### 项目 ID 格式

项目使用 14 位 ID 标识：`SC + YYYYMMDD + 4位序号`
示例：`SC202601260001`

## 常用开发任务

### 运行测试

每个技能在 `test/` 目录中都有对应的测试文件。运行单个测试：

```bash
python test/test_project_initiator.py
python test/test_data_checker.py
python test/test_scheme_writer.py
```

测试验证内容：
- 标准化 JSON 输出格式
- 输入参数校验
- 中文语言处理
- 缺失/无效数据的错误处理

### 添加新技能

1. 创建技能文件：`skills/SmartCity_YourSkill.md`
2. 遵循 `skills/standard-io-format.md` 中的标准化输入/输出格式
3. 实现 `core_process(input_data)` 函数模式
4. 创建对应的测试文件：`test/test_your_skill.py`
5. 在 `SmartCity_SOP_Main.md` 的模块序列中注册

### 修改 SOP 规则

核心 SOP 规则定义在：
- `智慧城市项目方案设计全流程执行完整提示词V3.md` - 完整工作流规则
- `Prompt模板库.md` - 各类 Agent 的提示词模板

**重要提示**：SOP 规则的修改必须在以下位置同步：
1. 主 SOP 文档（V3）
2. 各个技能实现
3. 测试验证逻辑
4. 标准 I/O 格式定义

### 知识库管理

系统使用三类知识库内容：
1. **场景模板库** - 不同智慧城市领域的预建模板
2. **核心技术资料** - 公司"万物互联引擎"相关材料
3. **适配表** - 技术-场景优先级映射

知识库通过 `SmartCity_KB_Manager` 管理（当前代码库中尚未完全实现）。

## 核心设计模式

### 渐进式工作流与用户确认

工作流在关键检查点暂停等待用户确认：
- 项目初始化后
- 数据校验后（特别是冲突/缺失项）
- 每一章方案撰写后
- 修订后
- 最终输出前

### 冲突解决优先级

当多个数据源冲突时：
1. **用户手工输入**（最高优先级）
2. 用户提供的方案解决对策
3. 全网搜索结果
4. 行业通用规范
5. 知识库模板

### 内容标注体系

所有生成的内容必须包含来源标注：
- `【手工输入 / 资料专属】` - 用户专属内容
- `【行业通用规范补充】` - 行业标准内容
- `【核心技术融合点】` - 核心技术融合点
- `【全网搜索信息】` - 全网搜索结果

### 场景类型

系统支持 8 种预定义的智慧城市场景：
1. 智慧城市一网统管（城市级治理）
2. 智慧园区（智慧园区/园区）
3. 商业综合体（商业综合体）
4. 智慧后勤（医院/学校后勤）
5. 智慧物业（智慧物业管理）
6. 智慧社区（智慧社区）
7. 智慧农业（智慧农业）
8. 智慧医疗（智慧医疗）

自定义场景受支持并标记为 `is_custom: true`。

## 文件结构

```
智慧城市方案设计sop/
├── skills/                          # 技能定义
│   ├── SmartCity_SOP_Main.md       # 主控编排器
│   ├── SmartCity_Project_Initiator.md
│   ├── SmartCity_Data_Checker.md
│   ├── SmartCity_Info_Summary.md
│   ├── SmartCity_Project_Understand.md
│   ├── SmartCity_Tech_Selection.md
│   ├── SmartCity_Scheme_Writer.md
│   ├── SmartCity_Scheme_Revise.md
│   ├── SmartCity_Scheme_Output.md
│   └── standard-io-format.md       # 标准化 I/O 格式定义
├── test/                           # 每个技能的测试文件
│   ├── test_project_initiator.py
│   ├── test_data_checker.py
│   └── ...
├── .claude/skills/                 # Claude Code 技能集成
│   └── (指向 skills/ 的符号链接)
├── 智慧城市项目方案设计全流程执行完整提示词V3.md
├── Prompt模板库.md
└── Claude Code 开发智慧城市 SOP 对应 Skills 设计与调试优化建议.md
```

## 重要约束

### 中文语言要求
- 所有面向用户的内容必须使用中文
- 方案输出使用专业中文商务/技术语言
- 错误消息和确认提示使用中文

### 数据来源追溯
最终方案中的每条信息都必须能追溯到其来源。切勿编造数据 - 如果数据缺失，明确标注为 `【XX关键资料缺失，相关内容为基于现有信息的合理推导】`

### 章节撰写结构
每章遵循严格的格式规则（来自 SOP V3 第 6.3 节）：
- 总分结构，论点前置
- 每章 3-5 个分支论点，最多 6 个
- 每个分支论点 ≤50 字
- 每个分支论点配 1-3 个支撑点，每个 ≤30 字
- 逐章用户确认（不批量撰写）

### 技术融合要求
公司的"万物互联引擎"必须融入每个方案，包含：
- 具体落地节点
- 与业务系统的集成逻辑
- 对场景的核心价值
- 清晰的 `【核心技术融合点】` 标注

## 故障排查

### 测试失败
如果测试失败，检查：
1. JSON 格式有效性（无尾随逗号，正确引号）
2. 输出中存在所有必需字段
3. `execute_status` 使用正确的枚举值
4. 中文字符编码（UTF-8）
5. 项目 ID 格式为 14 位

### 技能集成问题
当技能无法协同工作时：
1. 验证 `prev_module_data` 正确传递
2. 检查 `next_module` 名称完全匹配
3. 确保 `status` 值有效
4. 审查标准化 I/O 格式合规性

### 内容质量问题
如果生成的内容质量不佳：
1. 检查 `Prompt模板库.md` 中的提示词模板
2. 验证知识库内容已加载
3. 确保用户输入优先于模板
4. 确认正确的来源标注

## 未来开发

### 计划功能
- `SmartCity_KB_Manager` 实现，用于知识库 CRUD 操作
- 全网搜索集成（SOP 中已引用但尚未实现）
- 音频转录流水线集成
- CAD 图纸解析集成
- 持久化状态存储，支持项目恢复

### 已知限制
- 无实际的 MCP/工具集成（当前为模拟/测试实现）
- 知识库被引用但未动态加载
- 状态持久化使用简化的文件方式
- 无实际的 PPT 生成（仅结构定义）
