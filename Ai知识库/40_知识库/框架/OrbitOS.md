# OrbitOS

> 一个 AI 驱动的 Obsidian 生产力框架

---

## 核心理念

> **你是中心，万物围绕你运转**（Orbit = 轨道）

项目、知识、日常任务如同行星一般环环相扣——而管理这一切，只需用自然语言和 AI 聊聊天。

---

## GitHub 地址

- OrbitOS: https://github.com/MarsWang42/OrbitOS
- Claudesidian: https://github.com/heyitsnoah/claudesidian

---

## Metadata 是什么？

Metadata 是 Obsidian 知识库的**操作系统**，包含：

| 目录 | 内容 |
|---|---|
| **Reference/** | 文档、指南、AI 提示词库 |
| **Templates/** | 笔记模板（项目/日记/研究） |
| **Agents/** | AI 角色配置（如研究助手、编辑助手） |
| **Workflows/** | 工作流文档（周回顾、项目完成检查清单） |

---

## OrbitOS vs Claudesidian

| 项目 | 文件结构 | Metadata 位置 |
|---|---|---|
| **OrbitOS** | PARA 方法 | `99_系统/` |
| **Claudesidian** | 6 目录结构 | `06_Metadata/` |

**本质相同**，都是存放系统配置、模板、提示词。

---

## 博主的做法

结合了两个项目的优点：
- **OrbitOS** 的 PARA 文件结构
- **Claudesidian** 的 Metadata 设计理念

---

## 安装方式

### 方式一：Git Sparse Checkout（仅下载中文版本）

```bash
git clone --filter=blob:none --sparse https://github.com/MarsWang42/OrbitOS.git my-vault
cd my-vault
git sparse-checkout set CN
mv CN/* CN/.* . 2>/dev/null; rmdir CN
```

### 方式二：使用 degit（无 git 历史，更简单）

```bash
npx degit MarsWang42/OrbitOS/CN my-vault
```

---

## 文件结构

```
├── 00_收件箱/      # 快速捕获 —— AI 会处理到合适位置
├── 10_日记/        # 每日日志 (YYYY-MM-DD.md) —— 每天由 AI 生成
├── 20_项目/        # 活跃项目 —— AI 协助创建并跟踪进度
├── 30_研究/        # 深度研究笔记 —— AI 结构化
├── 40_知识库/      # 原子概念 —— AI 提取可复用定义
├── 50_资源/        # 精选内容 —— 通讯、产品发布、参考资料
├── 90_计划/        # 执行方案 —— AI 起草，你批准，然后归档
└── 99_系统/        # 系统配置
    ├── 归档/       # 历史记录 (按年/月组织)
    ├── 提示词/     # 针对不同领域的 AI 人设
    └── 模板/       # Markdown 模板
```

---

## AI 对知识库的分析能力

Codex 可以对整个 Obsidian 知识库进行分析：

- **全库搜索**：扫描所有 `.md` 文件
- **智能关联**：找出相关的项目、研究、知识库条目
- **生成报告**：输出分析结果

**示例**：
> "汇总一下整个库里跟 openclaw 联网搜索相关的项目"

Codex 会输出：
- 相关项目：50_资源/...
- 相关研究：30_研究/...
- 相关知识点：40_知识库/...

---

## 核心命令

| 命令 | 用途 | 适用场景 |
|---|---|---|
| `/start-my-day` | AI 引导每日规划与回顾 | 每天早上 |
| `/kickoff` | 把想法变成结构化项目 | 启动新计划 |
| `/research` | 深度调研，自动整理成知识 | 学习一个领域 |
| `/ask` | 快问快答，不留笔记 | 简单问题 |
| `/brainstorm` | 互动式头脑风暴 | 打磨想法 |
| `/parse-knowledge` | 把零散文本整理进知识库 | 处理笔记、文章 |
| `/archive` | 清理已完成的内容 | 定期维护 |

---

## 关键特性

### 1. AI 驱动工作流

AI 不只是存储，它会主动：
- 捕捉灵感 → 变成结构化项目
- 规划每日 → 基于工作推荐重点
- 深入研究 → 整理成知识库
- 串联一切 → 自动建立双向链接

### 2. 智能知识图谱

- **项目** 链接到 **研究笔记**
- **每日笔记** 链接到 **项目**
- **知识库** 是原子概念，可随处引用
- **研究笔记** 链接回源头概念

### 3. C.A.P. 项目结构

每个项目都遵循：
- **Context（背景）**：要做什么？怎样算成功？
- **Actions（行动）**：分阶段的任务清单
- **Progress（进展）**：带时间戳的更新

---

## 设计哲学

1. **AI 是伙伴**：不只是工具，是协作者
2. **先记下来，再整理**：收件箱不丢失灵感
3. **连接比分类重要**：双向链接构建知识图谱
4. **每日节奏**：每日笔记锚定一切
5. **渐进式结构化**：想法逐步变清晰

---

## 关联笔记

- [[Obsidian文件结构-PARA方法]]
- [[信息收集工具链]]
- [[AI工具协同]]

---

## 来源

- GitHub: https://github.com/MarsWang42/OrbitOS
- 博主直播引用
