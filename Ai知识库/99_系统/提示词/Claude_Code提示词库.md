# Claude Code 提示词库

> 来自 Claudesidian 项目的常用提示词（中文版）

---

## ⚠️ 提示词怎么用？

**不是每次都手动输入！**

| 步骤 | 说明 |
|---|---|
| 1. **预配置** | 把提示词写在 `99_系统/提示词/` 目录 |
| 2. **自动加载** | AI 启动时自动读取 |
| 3. **按需调用** | AI 根据场景自动使用 |

**举例**：
```
你：帮我把收件箱整理一下
AI：（自动使用"处理收件箱"提示词）→ 执行
```

---

## 开始工作

### 开始一个会话
<!--
I'm starting work for today.
Can you review what I was working on yesterday
and help me pick up where I left off?
-->
```
我今天开始工作了。
能帮我回顾一下昨天在做什么，
然后帮我继续推进吗？
```
**用法**：让 AI 回顾昨天的工作，帮你继续推进。

---

### 设定模式
<!--
I'm in thinking mode, not writing mode.
Please help me explore [topic] by asking questions
and searching for relevant notes.
-->
```
我现在是思考模式，不是写作模式。
请通过提问和搜索相关笔记，
帮我探索 [主题]。
```
**用法**：
- **思考模式**：探索、提问、搜索、不急着输出
- **写作模式**：开始写、出大纲、润色

---

## 研究与整合

### 寻找关联
<!--
Search my vault for anything related to [topic].
What patterns or connections do you see?
-->
```
搜索我的知识库里所有跟 [主题] 相关的内容。
你发现了什么模式或关联？
```
**用法**：让 AI 全库搜索，找出隐藏的关联。

---

### 整合项目
<!--
Review all notes in [project folder].
Create a synthesis of the key themes, insights, and open questions.
-->
```
回顾 [项目文件夹] 里的所有笔记。
总结出关键主题、洞察和未解决的问题。
```
**用法**：把零散笔记整合成结构化总结。

---

### 周回顾
<!--
Look at all notes created this week.
What are the main themes?
What connections exist between different projects?
-->
```
看看这周创建的所有笔记。
主要主题是什么？不同项目之间有什么关联？
```
**用法**：每周做一次，发现跨项目的模式。

---

## 组织整理

### 处理收件箱
<!--
Review items in 00_Inbox.
Suggest where each should be moved based on PARA method.
Which items could be combined or linked?
-->
```
回顾 00_收件箱 里的内容。
根据 PARA 方法，建议每项应该移到哪个位置。
哪些内容可以合并或链接？
```
**用法**：
- **PARA 方法**：Projects(项目) → Areas(领域) → Resources(资源) → Archives(归档)
- 收件箱思维：先收集，后整理

---

### 找孤儿笔记
<!--
Find notes that aren't linked to any other notes.
Suggest potential connections.
-->
```
找出没有链接到任何其他笔记的内容。
建议可能的关联。
```
**用法**：**孤儿笔记**是指没有双向链接的笔记，容易被遗忘。

---

### 清理附件
<!--
Review files in 05_Attachments.
Which ones aren't referenced in any notes?
Which could be better named?
-->
```
回顾 05_资源 里的文件。
哪些没有被任何笔记引用？
哪些可以重命名得更清晰？
```
**用法**：定期清理无用的附件，保持知识库整洁。

---

## 写作与创作

### 转入写作模式
<!--
I'm ready to move from thinking to writing mode.
Based on our research in [project],
help me create an outline for [deliverable].
-->
```
我准备好从思考模式转入写作模式了。
基于我们在 [项目] 里的研究，
帮我创建 [交付物] 的大纲。
```
**用法**：从探索转入输出，先出大纲再写正文。

---

### 改进草稿
<!--
Review [document].
Don't rewrite it, but give me specific feedback on:
- Structure and flow
- Gaps in logic or evidence
- Areas that need clarification
-->
```
回顾 [文档]。
不要重写它，但给我具体的反馈：
- 结构和流程
- 逻辑或证据的缺口
- 需要澄清的地方
```
**用法**：AI 只给反馈，不直接改，保留你的风格。

---

## 学习与发展

### 探索新主题
<!--
I want to learn about [topic].
Start by searching my vault for any existing knowledge.
Then help me identify what I need to research.
-->
```
我想学习 [主题]。
先搜索我的知识库里已有的相关知识。
然后帮我识别需要进一步研究什么。
```
**用法**：先查现有知识，再补缺口。

---

### 构建论点
<!--
I'm trying to argue that [thesis].
Search my notes for supporting evidence.
What counterarguments should I address?
-->
```
我想论证 [论点]。
搜索我的笔记找支持证据。
我应该处理哪些反驳论点？
```
**用法**：论点 + 反驳论点，全面思考。

---

## 项目管理

### 项目状态
<!--
Review the project in [folder].
What's the current status?
What are the next actions needed?
-->
```
回顾 [文件夹] 里的项目。
当前状态是什么？
需要哪些下一步行动？
```
**用法**：快速检查项目进度。

---

### 创建回顾
<!--
[Project] is now complete.
Review all notes and create a retrospective covering:
- What was accomplished
- Key learnings
- What to do differently next time
-->
```
[项目] 现在完成了。
回顾所有笔记，创建一个回顾，包括：
- 完成了什么
- 关键收获
- 下次可以改进什么
```
**用法**：**回顾/复盘**是项目结束后的总结。

---

## 日常操作

### 晨间回顾
<!--
Good morning. Show me:
- Any notes modified yesterday
- Open tasks or questions
- What should I focus on today?
-->
```
早上好。给我看：
- 昨天修改了哪些笔记
- 未完成的任务或问题
- 我今天应该关注什么
```
**用法**：每天早上的快速对齐。

---

### 日终总结
<!--
End of day review:
- What did I accomplish today?
- What questions or ideas emerged?
- What should I prioritize tomorrow?
-->
```
日终回顾：
- 我今天完成了什么？
- 有什么问题或想法出现？
- 我明天应该优先做什么？
```
**用法**：每天下班前的总结。

---

## 高级技巧

### 跨项目分析
<!--
Compare insights from [Project A] and [Project B].
What patterns exist across both?
What could each learn from the other?
-->
```
比较 [项目A] 和 [项目B] 的洞察。
两者之间有什么模式？
它们可以互相学到什么？
```
**用法**：发现跨项目的共同模式。

---

### 知识缺口
<!--
Analyze my notes on [topic].
What aspects am I missing?
What questions haven't I asked?
-->
```
分析我关于 [主题] 的笔记。
我缺少哪些方面？
我还没有问什么问题？
```
**用法**：**知识缺口**是你不知道自己不知道的东西。

---

### 想法发展
<!--
I have this rough idea: [idea]
Search for related concepts in my vault.
Help me develop this into something more concrete.
-->
```
我有这个粗略的想法：[想法]
搜索我的知识库里相关的概念。
帮我把它发展成更具体的东西。
```
**用法**：从模糊想法到具体计划。

---

## 💡 使用技巧

1. **明确模式**（思考模式 vs 写作模式）
2. **引用具体文件夹**
3. **要问题，不只是答案**
4. **要综合，不只是搜索**
5. **自由迭代**——保持对话

---

## 🎯 核心理念

| 模式 | 特点 | 说明 |
|---|---|---|
| **思考模式** | 探索、提问、搜索、不急着输出 | 适合研究阶段 |
| **写作模式** | 开始写、出大纲、润色 | 适合输出阶段 |

---

## 🔗 关联笔记

- [[OrbitOS]]
- [[信息收集工具链]]
- [[AI工具协同]]

---

## 来源

- GitHub: https://github.com/heyitsnoah/claudesidian
- 路径: 06_Metadata/Reference/Common Claude Code Prompts.md
- 翻译：2026年03月24日
