---
type: design
tags: [设计, Agent, 架构]
category: 项目文档
project: 示例-代码审查Agent
stage: 设计阶段
created: 2026-03-25
last_updated: 2026-03-25
related: [[需求文档-代码审查Agent]]
---

# Agent架构设计：代码审查Agent

> **项目**：示例-代码审查Agent
> **阶段**：设计阶段
> **日期**：2026-03-25
> **状态**：✅ 已完成

## 🎯 设计目标

基于需求分析，设计一个简单但有效的代码审查Agent：
- 🎯 **专注核心功能**：Python代码的基础审查
- 🎯 **易于实现**：2天内完成
- 🎯 **可扩展**：后续可以添加功能
- 🎯 **可维护**：代码和Prompt清晰

---

## 🏗️ 整体架构

### Agent类型选择

**选择：reviewing Agent**

理由：
- ✅ 符合审查任务的特性
- ✅ 专注于分析和反馈
- ✅ 不需要执行复杂操作

参考：[[Agent架构模式]] 中的"审查Agent模式"

### 架构图

```
用户输入代码文件
       ↓
┌─────────────────────────┐
│   Code Review Agent     │
│                         │
│  1. 读取代码文件         │
│  2. 分析代码结构         │
│  3. 执行检查规则         │
│  4. 生成审查报告         │
└─────────────────────────┘
       ↓
   审查结果输出
```

---

## 🔧 组件设计

### 组件1：文件读取器

**功能**：读取并解析代码文件

**输入**：文件路径
**输出**：代码内容 + 基本信息

**实现要点**：
```python
# 需要的信息
- 文件内容（完整代码）
- 文件大小
- 代码行数
- 文件类型（通过扩展名）
```

**工具选择**：
- 使用基础工具：Read tool
- 为什么？简单直接，不需要额外依赖

### 组件2：代码分析器

**功能**：分析代码结构和特征

**输入**：代码内容
**输出**：结构化信息

**分析维度**：
1. **结构分析**
   - 函数定义
   - 类定义
   - 导入语句
   - 主要代码块

2. **特征提取**
   - 代码复杂度
   - 命名规范
   - 注释覆盖率

**实现方式**：
- 使用Grep tool进行模式匹配
- Claude进行语义分析

### 组件3：规则检查器

**功能**：按规则检查代码问题

**检查规则（P0）**：

| 规则ID | 检查项 | 严重程度 |
|--------|--------|---------|
| R001 | 命名规范 | 低 |
| R002 | 未使用导入 | 中 |
| R003 | 缺少文档字符串 | 中 |
| R004 | 过长函数 | 中 |
| R005 | 异常处理缺失 | 高 |

**检查逻辑**：
```python
for rule in rules:
    if rule.matches(code):
        issues.append({
            'rule': rule.id,
            'severity': rule.severity,
            'location': rule.find_location(code),
            'message': rule.message,
            'suggestion': rule.suggestion
        })
```

### 组件4：报告生成器

**功能**：生成结构化的审查报告

**报告格式**：
```markdown
# 代码审查报告

## 概览
- 文件：example.py
- 行数：150
- 问题总数：5
  - 高：1
  - 中：3
  - 低：1

## 问题详情

### 🔴 高严重度
1. [R005] 异常处理缺失
   - 位置：第45行
   - 问题：文件操作没有异常处理
   - 建议：添加try-except块
   - 代码示例：
   ```python
   try:
       with open(file) as f:
           content = f.read()
   except IOError as e:
       logger.error(f"无法读取文件: {e}")
   ```

### 🟡 中严重度
...

### 🟢 低严重度
...

## 总结
代码质量：良好
主要问题：异常处理和文档
建议：优先修复高严重度问题
```

---

## 📋 接口设计

### 输入接口

**方式1：文件路径**
```bash
review_code("path/to/file.py")
```

**方式2：代码字符串**
```bash
review_code_string(code_string, language="python")
```

**方式3：带配置**
```bash
review_code(
    "path/to/file.py",
    strictness="medium",  # strict/medium/loose
    checks=["style", "bugs", "security"]  # 选择检查类别
)
```

### 输出接口

**结构化输出**：
```json
{
  "file": "example.py",
  "lines": 150,
  "issues": [
    {
      "rule_id": "R005",
      "severity": "high",
      "location": {"line": 45, "column": 0},
      "message": "异常处理缺失",
      "suggestion": "添加try-except块",
      "example": "..."
    }
  ],
  "summary": {
    "total": 5,
    "high": 1,
    "medium": 3,
    "low": 1
  },
  "quality_score": 75
}
```

**人类可读输出**：Markdown格式的报告

---

## 🤖 Prompt设计

### 系统Prompt

```
你是一个专业的Python代码审查助手。你的任务是：

1. 仔细审查提供的Python代码
2. 识别代码中的问题
3. 提供具体的改进建议
4. 教育用户为什么有问题

审查维度：
- 代码风格（命名、格式、注释）
- 常见Bug（未处理异常、边界条件）
- 安全问题（注入、硬编码密钥）
- 性能问题（低效算法、资源泄漏）

输出要求：
- 结构化的JSON格式
- 每个问题包含：位置、描述、建议、示例
- 按严重程度排序
- 提供总体质量评分
```

### 用户Prompt模板

```
请审查以下Python代码：

文件：{filename}
代码：
```python
{code}
```

请检查以下方面：
{check_list}

输出JSON格式的审查结果。
```

---

## 🔨 工具选择

### 需要的工具

| 工具 | 用途 | 数量 |
|------|------|------|
| Read | 读取文件 | unlimited |
| Grep | 搜索模式 | unlimited |
| Bash | 运行代码检查工具（可选） | limited |

### 工具权限

```yaml
tools:
  - read: all files
  - grep: all files
  - bash: limited to code analysis tools

permissions:
  - read_code: true
  - write_code: false  # 只读，不修改
  - execute: limited
```

参考：[[工具选择决策]]

---

## 🎨 UI/交互设计

### 命令行界面

```bash
# 基本用法
$ claude review code.py

# 带配置
$ claude review code.py --strictness strict --checks style,security

# 批量审查
$ claude review *.py

# 输出格式
$ claude review code.py --format json
$ claude review code.py --format markdown
```

### 交互流程

```
用户：review my_code.py

Agent：
[读取文件]
✓ 已读取 my_code.py (150行)

[分析代码]
✓ 已识别 3个函数，2个类

[检查规则]
✓ 正在检查代码风格...
✓ 正在检查常见Bug...
✓ 正在检查安全问题...

[生成报告]
发现 5 个问题：
  🔴 高：1个
  🟡 中：3个
  🟢 低：1个

[详细报告]
...（markdown格式报告）

是否需要详细解释某个问题？
```

---

## 📊 数据流设计

### 主要数据流

```
代码文件
  ↓
[文件读取器]
  → 代码内容
  ↓
[代码分析器]
  → 结构化信息（AST+）
  ↓
[规则检查器]
  → 问题列表
  ↓
[报告生成器]
  → 审查报告（JSON/MD）
  ↓
  用户
```

### 数据结构

```python
# 代码信息
CodeInfo = {
    'file': str,
    'content': str,
    'lines': int,
    'language': str,
    'functions': List[FunctionInfo],
    'classes': List[ClassInfo]
}

# 问题信息
Issue = {
    'rule_id': str,
    'severity': 'high' | 'medium' | 'low',
    'location': {'line': int, 'column': int},
    'message': str,
    'suggestion': str,
    'example': str
}

# 报告信息
Report = {
    'file': str,
    'code_info': CodeInfo,
    'issues': List[Issue],
    'summary': Summary,
    'quality_score': int
}
```

---

## 🔒 错误处理

### 可能的错误

1. **文件读取错误**
   - 文件不存在
   - 权限不足
   - 编码问题

2. **代码分析错误**
   - 语法错误
   - 不支持的Python版本
   - 损坏的文件

3. **检查规则错误**
   - 规则配置错误
   - 超时

### 错误处理策略

```python
try:
    code = read_file(file_path)
except FileNotFoundError:
    return {"error": "文件不存在", "suggestion": "检查文件路径"}
except PermissionError:
    return {"error": "权限不足", "suggestion": "检查文件权限"}

try:
    issues = check_rules(code)
except SyntaxError as e:
    return {
        "error": "代码语法错误",
        "details": str(e),
        "suggestion": "修复语法错误后再审查"
    }
```

---

## 🧪 测试策略

### 测试用例

| 用例 | 输入 | 预期输出 |
|------|------|---------|
| 正常代码 | 规范的代码 | 无问题或少量低严重度问题 |
| 风险代码 | 有安全问题的代码 | 检测出安全问题 |
| 复杂代码 | 大量嵌套 | 检测出复杂度问题 |
| 错误代码 | 语法错误 | 友好的错误提示 |
| 空文件 | 空Python文件 | 适当的提示 |

### 测试数据集

准备测试文件：
- `test_good.py`：高质量的代码
- `test_bad.py`：各种问题的代码
- `test_security.py`：安全问题的代码
- `test_performance.py`：性能问题的代码

---

## 📝 实现计划

### 实现步骤

**步骤1：基础框架（1小时）**
- [ ] 创建Agent骨架
- [ ] 实现文件读取
- [ ] 基本的Prompt设计

**步骤2：核心功能（3小时）**
- [ ] 实现代码分析
- [ ] 实现P0规则检查
- [ ] 实现报告生成

**步骤3：测试优化（2小时）**
- [ ] 准备测试数据
- [ ] 执行测试用例
- [ ] 优化Prompt和规则

**步骤4：文档总结（1小时）**
- [ ] 编写使用说明
- [ ] 记录开发过程
- [ ] 提炼经验

---

## 💡 设计决策记录

### 决策1：为什么用规则+AI而不是纯AI？

**选项**：
A. 纯AI分析
B. 规则+AI混合
C. 纯规则检查

**选择**：B（规则+AI混合）

**原因**：
- 规则检查快速、一致
- AI理解上下文、给出建议
- 混合方式平衡速度和质量

### 决策2：为什么先只支持Python？

**原因**：
- 时间有限，专注一种语言
- Python是我的主要语言
- 后续可以扩展其他语言

### 决策3：为什么用JSON输出？

**原因**：
- 结构化，易于处理
- 可以转换为其他格式
- 便于集成和测试

---

## ✅ 设计评审

### 设计检查清单
- [x] 是否满足需求？✅ 是的
- [x] 架构是否清晰？✅ 组件职责明确
- [x] 接口是否简洁？✅ 易于使用
- [x] 是否可扩展？✅ 可以添加规则
- [x] 是否可实现？✅ 2天可完成

### 设计确认
这个设计：
- ✅ 明确了组件和接口
- ✅ 定义了数据流
- ✅ 考虑了错误处理
- ✅ 有清晰的实现计划

---

## 📚 参考资料

### 知识库资源
- [[Agent架构模式]]：审查Agent模式
- [[工具选择决策]]：工具选择方法
- [[Prompt工程指南]]：Prompt设计技巧

### 外部资源
- [代码审查最佳实践](#)
- [Python AST文档](#)

---

**下一步**：开始实现，查看 [[2026-03-25-项目初始化]]

**相关笔记**：
- [[2026-03-25-实现核心功能]]：开发过程
- [[问题-工具调用超时]]：问题记录
