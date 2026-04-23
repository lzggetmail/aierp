---
type: config
tags: [配置, 规范, Frontmatter]
category: 知识库配置
created: 2026-03-25
last_updated: 2026-03-25
---

# Frontmatter字段说明

> **目的**：建立统一的元数据规范，提高笔记的可检索性和可组织性
> **格式**：YAML格式的文件头元数据
> **位置**：每个Markdown文件的最开头

## 📋 基础格式

```yaml
---
key1: value1
key2: value2
key3: value3
---
```

## 🔧 通用字段

所有笔记类型都应该包含的基础字段：

### 必填字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `type` | 字符串 | 笔记类型 | `concept`, `sop`, `agent-dev` |
| `tags` | 列表 | 标签列表 | `[AI, Agent, 开发]` |
| `created` | 日期 | 创建日期 | `2026-03-25` |
| `last_updated` | 日期 | 最后更新日期 | `2026-03-25` |

### 可选字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `category` | 字符串 | 分类 | `技术文档`, `经验总结` |
| `status` | 字符串 | 状态 | `draft`, `active`, `completed` |
| `related` | 列表 | 相关笔记 | `[[相关笔记1]], [[相关笔记2]]` |
| ` aliases` | 列表 | 别名 | `["别名1", "别名2"]` |
| `author` | 字符串 | 作者 | `Administrator` |
| `source` | 字符串 | 来源 | `https://example.com` |

---

## 📝 各类型笔记字段

### 1. 概念笔记 (type: concept)

```yaml
---
type: concept
tags: [概念, AI]
category: 知识点
domain: AI              # 领域
difficulty: 入门         # 难度：入门|中级|高级
importance: ⭐⭐⭐        # 重要度：⭐|⭐⭐|⭐⭐⭐
created: 2026-03-25
last_updated: 2026-03-25
mastery_level: 理解      # 掌握程度：了解|理解|掌握|精通
related: []
---
```

**字段说明**：
- `domain`: 所属领域（AI, 编程, 方法论等）
- `difficulty`: 难度级别
- `importance`: 重要程度（1-3星）
- `mastery_level`: 个人掌握程度

### 2. Agent开发笔记 (type: agent-dev)

```yaml
---
type: agent-dev
tags: [Agent, 开发]
category: 技术文档
agent_type: general-purpose  # Agent类型
complexity: medium           # 复杂度：simple|medium|complex
created: 2026-03-25
last_updated: 2026-03-25
status: development          # 状态：design|development|testing|production
related: []
---
```

**字段说明**：
- `agent_type`: Agent类型
- `complexity`: 复杂度
- `status`: 开发状态

### 3. SOP文档 (type: sop)

```yaml
---
type: sop
tags: [SOP, 流程]
category: 标准化流程
domain: 开发
scope: 个人                # 适用范围：个人|团队|组织
frequency: on-demand       # 执行频率：daily|weekly|monthly|on-demand
version: 1.0              # 版本号
created: 2026-03-25
last_updated: 2026-03-25
review_date: 2026-04-25   # 下次审查日期
status: active            # 状态：draft|active|deprecated
related: []
---
```

**字段说明**：
- `scope`: 适用范围
- `frequency`: 执行频率
- `version`: 版本号
- `review_date`: 下次审查日期
- `status`: SOP状态

### 4. 项目经验笔记 (type: project-experience)

```yaml
---
type: project-experience
tags: [项目, 经验]
category: 实践经验
project_type: 个人项目     # 项目类型
domain: AI开发
duration: 2周              # 持续时间
outcome: 成功              # 结果：成功|失败|中止|进行中
created: 2026-03-25
last_updated: 2026-03-25
related: []
---
```

**字段说明**：
- `project_type`: 项目类型
- `domain`: 项目领域
- `duration`: 项目持续时间
- `outcome`: 项目结果

### 5. 方法论笔记 (type: methodology)

```yaml
---
type: methodology
tags: [方法论, 学习]
category: 思考框架
domain: 学习
applicability: 通用       # 适用性：通用|特定领域|特定场景
maturity: 已验证          # 成熟度：验证中|已验证|成熟|经典
created: 2026-03-25
last_updated: 2026-03-25
related: []
---
```

**字段说明**：
- `domain`: 适用领域
- `applicability`: 适用范围
- `maturity`: 方法论成熟度

### 6. MOC索引 (type: moc)

```yaml
---
type: moc
tags: [MOC, 索引]
category: 知识地图
scope: main               # 范围：main|sub
created: 2026-03-25
last_updated: 2026-03-25
related: []
---
```

**字段说明**：
- `scope`: MOC层级（主MOC或子MOC）

---

## 🏷️ 标签字段规范

### tags格式

```yaml
# 基础格式
tags: [标签1, 标签2, 标签3]

# 多行格式（标签较多时）
tags:
  - 标签1
  - 标签2
  - 标签3
```

### 标签选择顺序

建议按以下顺序组织标签：

```yaml
tags:
  - 内容类型    # 如：概念、SOP、经验
  - 领域        # 如：AI、开发、知识管理
  - 具体主题    # 如：Agent、Prompt
  - 状态        # 如：进行中、已完成
  - 其他        # 如：重要、常用
```

示例：
```yaml
tags: [概念, AI, Agent, 入门]
tags: [SOP, 开发, Agent, 重要, 常用]
tags: [经验, 项目, AI, 已完成]
```

---

## 🔗 相关字段规范

### related字段

用于建立笔记之间的关联：

```yaml
# 单个相关笔记
related: [[相关笔记]]

# 多个相关笔记
related:
  - [[相关笔记1]]
  - [[相关笔记2]]
  - [[相关笔记3]]

# 带说明的相关笔记
related:
  - [[相关笔记1]]: 关系说明
  - [[相关笔记2]]: 关系说明
```

### 使用建议

1. **适度关联**：不是所有笔记都要有关联
2. **双向关联**：A关联B，B也应该关联A
3. **明确关系**：注明关联的原因
4. **定期更新**：随着知识增长更新关联

---

## 📊 日期字段规范

### 日期格式

统一使用 `YYYY-MM-DD` 格式：

```yaml
created: 2026-03-25
last_updated: 2026-03-25
review_date: 2026-04-25
```

### 日期更新规则

| 字段 | 更新时机 |
|------|---------|
| `created` | 创建时设置，不再修改 |
| `last_updated` | 每次修改内容时更新 |
| `review_date` | 按计划设置，到期后更新 |

---

## 🎯 状态字段规范

### 常用状态值

#### 笔记状态
- `draft`: 草稿，未完成
- `active`: 活跃，持续维护
- `completed`: 已完成，不再更新
- `deprecated`: 已废弃，保留参考

#### 项目状态
- `planning`: 计划中
- `in_progress`: 进行中
- `completed`: 已完成
- `on_hold`: 暂停
- `cancelled`: 已取消

#### Agent状态
- `design`: 设计阶段
- `development`: 开发阶段
- `testing`: 测试阶段
- `production`: 生产环境

---

## 💡 最佳实践

### ✅ 推荐做法

1. **完整性**
   - 每个笔记都填写完整的frontmatter
   - 使用模板确保字段完整

2. **一致性**
   - 相同类型的笔记使用相同字段
   - 使用规范的字段值

3. **及时更新**
   - 修改内容时更新 `last_updated`
   - 状态变化时更新 `status`

4. **合理关联**
   - 建立有意义的关联
   - 定期检查和更新关联

### ❌ 避免做法

1. **字段冗余**
   - 不添加无用的字段
   - 不重复已有的信息

2. **不一致**
   - 不使用相似但不相同的字段名
   - 不使用不规范的字段值

3. **不更新**
   - 不让 `last_updated` 过时
   - 不让 `status` 失准

---

## 🔧 工具支持

### Obsidian插件

#### Templater
自动填充frontmatter字段：
```javascript
<%*
let date = tp.date.now("YYYY-MM-DD");
tR += `
---
created: ${date}
last_updated: ${date}
---
`
%>
```

#### MetaEdit
快速编辑frontmatter字段

#### Dataview
基于frontmatter查询和展示

### 检查脚本

定期检查frontmatter完整性：
```javascript
// 检查必需字段
const requiredFields = ['type', 'tags', 'created', 'last_updated'];
// 检查逻辑...
```

---

## 📝 快速参考

### 最小frontmatter

```yaml
---
type: concept
tags: [概念]
created: 2026-03-25
last_updated: 2026-03-25
---
```

### 完整frontmatter

```yaml
---
type: concept
tags: [概念, AI, Agent]
category: 知识点
domain: AI
difficulty: 入门
importance: ⭐⭐⭐
created: 2026-03-25
last_updated: 2026-03-25
mastery_level: 理解
status: active
related:
  - [[相关概念1]]
  - [[相关概念2]]
aliases: ["别名1", "别名2"]
author: Administrator
---
```

---

## 🔄 规范演进

### V1.0 (2026-03-25)
- ✅ 建立基础字段规范
- ✅ 定义各类型笔记字段
- ✅ 制定使用指南

### 未来计划
- [ ] 根据使用情况优化
- [ ] 补充特殊字段
- [ ] 建立字段检查工具

---

**相关文档**：
- [[Tags系统规范]] - 标签使用规范
- [[命名规范]] - 文件命名规范
- [[知识库架构设计]] - 整体架构

**最后更新**：2026-03-25
**下次审查**：2026-04-25
