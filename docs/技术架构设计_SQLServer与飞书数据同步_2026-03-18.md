# AiERP 技术架构设计

> 日期：2026-03-18
> 架构：SQL Server + 飞书多维表格 + AI Agent
> 参考：产品规划讨论记录

---

## 一、总体架构

### 1.1 架构图

```
┌─────────────────────────────────────────────────────────┐
│                      用户层                              │
├─────────────────────────────────────────────────────────┤
│  老客户：Delphi 客户端（核心业务，继续维护）              │
│  新客户：Web 端 + 飞书端（双端配合使用）                  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    前端层                                │
├──────────────────────┬──────────────────────────────────┤
│    Web 前端           │         飞书前端                  │
│ (Vue 3 + 组件库)     │ (多维表格 + 机器人)              │
└──────────────────────┴──────────────────────────────────┘
            ↓                           ↓
┌─────────────────────────────────────────────────────────┐
│                    API 层                                │
├──────────────────────┬──────────────────────────────────┤
│   Web API 服务        │       飞书 API 服务              │
│ (业务接口)           │ (数据同步、消息推送)             │
└──────────────────────┴──────────────────────────────────┘
            ↓                           ↓
┌─────────────────────────────────────────────────────────┐
│                    AI 层                                │
├─────────────────────────────────────────────────────────┤
│          QClaw/QwClaw + Skills                         │
│  - 查询 ERP 数据 Skill                                   │
│  - 创建订单 Skill                                        │
│  - 财务分析 Skill                                        │
│  - 飞书表格操作 Skill                                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    数据层                                │
├──────────────────────┬──────────────────────────────────┤
│   SQL Server          │       飞书多维表格                │
│ (基础数据 + 业务数据) │ (汇总数据 + 任务数据)            │
└──────────────────────┴──────────────────────────────────┘
```

### 1.2 技术栈

| 层级 | 技术选型 | 说明 |
|-----|---------|------|
| **Web 前端** | Vue 3 + Element Plus | 成熟、文档多、易上手 |
| **飞书前端** | 飞书多维表格 + 机器人 | 现成能力，零开发成本 |
| **Web API** | Node.js + Express | 与前端技术栈统一 |
| **飞书 API** | Node.js + @larksuiteoapi/node-sdk | 官方 SDK，稳定可靠 |
| **AI 层** | QClaw/QwClaw | 国内大厂方案，安全可靠 |
| **数据库** | SQL Server | 现有系统，保持稳定 |
| **部署** | Docker + 云服务器 | 容器化，易于维护 |

---

## 二、数据库设计

### 2.1 后端数据库：SQL Server

#### 数据分类

| 表类型 | 表数量 | 数据量级 | 示例表 |
|-------|--------|---------|--------|
| 基础数据 | 10-20 张 | 5 万+ 条 | 客户表、产品表、供应商表、员工表 |
| 业务数据 | 20-30 张 | 50 万+ 条 | 订单表、订单明细表、库存表、财务凭证表 |
| 系统数据 | 5-10 张 | 100 万+ 条 | 权限表、审批流表、日志表 |

#### 核心表示例

```sql
-- 客户表
CREATE TABLE customers (
    customer_id INT PRIMARY KEY IDENTITY(1,1),
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(500),
    customer_level VARCHAR(10), -- A/B/C
    sales_person_id INT,
    created_time DATETIME DEFAULT GETDATE(),
    updated_time DATETIME DEFAULT GETDATE()
);

-- 产品表
CREATE TABLE products (
    product_id INT PRIMARY KEY IDENTITY(1,1),
    product_code VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    specification VARCHAR(200),
    unit VARCHAR(20),
    price DECIMAL(10, 2),
    category VARCHAR(100),
    created_time DATETIME DEFAULT GETDATE(),
    updated_time DATETIME DEFAULT GETDATE()
);

-- 订单表
CREATE TABLE orders (
    order_id INT PRIMARY KEY IDENTITY(1,1),
    order_code VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    order_date DATETIME NOT NULL,
    delivery_date DATETIME,
    total_amount DECIMAL(12, 2),
    status VARCHAR(20), -- 待确认/已确认/生产中/已交付
    sales_person_id INT,
    created_time DATETIME DEFAULT GETDATE(),
    updated_time DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 订单明细表
CREATE TABLE order_details (
    detail_id INT PRIMARY KEY IDENTITY(1,1),
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 库存表
CREATE TABLE inventory (
    inventory_id INT PRIMARY KEY IDENTITY(1,1),
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity INT NOT NULL,
    updated_time DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE (product_id, warehouse_id)
);
```

---

### 2.2 前端数据库：飞书多维表格

#### 数据分类

| 表类型 | 表数量 | 数据量级 | 说明 |
|-------|--------|---------|------|
| 汇总数据 | 5-10 张 | 几千条 | 聚合后的数据，数据量小 |
| 任务数据 | 3-5 张 | 几百条 | 协作数据，日常使用 |
| 分析结果 | 3-5 张 | 几十条 | AI 生成，数量有限 |

#### 核心表示例

```
1. 销售日报表（sales_daily_report）
   字段：日期、总销售额、订单数量、Top3产品、Top3客户
   数据量：每天 1 条，一年 365 条

2. 库存汇总表（inventory_summary）
   字段：产品名称、规格、仓库、库存数量、预警状态
   数据量：按产品聚合，几千条

3. 待办任务表（pending_tasks）
   字段：任务名称、负责人、优先级、截止日期、状态
   数据量：几百条

4. AI 分析报告表（ai_analysis_reports）
   字段：报告日期、分析类型、关键发现、建议措施
   数据量：几十条

5. 异常预警表（alerts）
   字段：预警类型、内容、严重程度、处理状态
   数据量：几百条
```

---

## 三、数据同步设计

### 3.1 同步策略

#### 策略选择

| 数据类型 | 同步方式 | 频率 | 实现方式 |
|---------|---------|------|---------|
| 基础数据 | 单向同步 | 每小时 | 定时任务，增量同步 |
| 业务数据 | 实时同步 | 立即 | 触发器 + API 推送 |
| 汇总数据 | 定时聚合 | 每天 | 定时任务，聚合计算 |
| 任务数据 | 双向同步 | 实时 | API 接口，实时处理 |
| 分析结果 | 单向写入 | 按需 | AI 生成后直接写入 |

#### 同步流程

```
┌─────────────────────────────────────────────────────────┐
│              SQL Server → 飞书：单向同步                  │
├─────────────────────────────────────────────────────────┤
│  1. 定时任务触发                                        │
│  2. 从 SQL Server 查询变更数据（基于时间戳）            │
│  3. 转换为飞书字段格式                                  │
│  4. 调用飞书 API 批量写入                               │
│  5. 记录同步日志                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              飞书 → SQL Server：API 写回                 │
├─────────────────────────────────────────────────────────┤
│  1. 飞书端操作触发（用户或 AI）                          │
│  2. 调用 Web API 接口                                   │
│  3. 验证数据有效性                                      │
│  4. 写入 SQL Server（使用事务）                         │
│  5. 增量同步回飞书（可选）                              │
└─────────────────────────────────────────────────────────┘
```

---

### 3.2 同步服务架构

```
┌─────────────────────────────────────────────────────────┐
│                    同步服务层                            │
├─────────────────────────────────────────────────────────┤
│  定时同步服务                                            │
│  ├── 每小时：同步基础数据（客户、产品）                  │
│  ├── 每天：同步汇总数据（销售日报、库存汇总）            │
│  └── 实时：同步关键数据（待办任务、预警）                │
│                                                          │
│  API 服务                                                │
│  ├── 接收飞书端操作请求                                  │
│  ├── 写入 SQL Server                                     │
│  └── 触发增量同步到飞书                                  │
│                                                          │
│  监控服务                                                │
│  ├── 同步状态监控                                        │
│  ├── 失败重试机制                                        │
│  └── 异常告警                                            │
└─────────────────────────────────────────────────────────┘
```

---

### 3.3 数据一致性保证

#### 事务处理

```javascript
// 使用事务保证一致性
async function syncWithTransaction() {
  const transaction = new sql.Transaction();

  try {
    await transaction.begin();

    // 1. 读取数据（加锁）
    const data = await transaction.request()
      .query('SELECT * FROM products WITH (UPDLOCK)');

    // 2. 同步到飞书
    await syncToFeishu(data);

    // 3. 更新同步时间戳
    await transaction.request()
      .query('UPDATE sync_status SET last_sync = GETDATE()');

    await transaction.commit();
  } catch (err) {
    await transaction.rollback();
    throw err;
  }
}
```

#### 失败重试

```javascript
// 重试机制
async function syncWithRetry(data, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await syncToFeishu(data);
      return; // 成功，退出
    } catch (err) {
      if (i === maxRetries - 1) {
        // 最后一次重试失败，记录日志
        await logSyncFailure(data, err);
        throw err;
      }

      // 指数退避
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

#### 数据映射

```javascript
// 字段映射配置
const fieldMapping = {
  'products': {
    'product_id': { feishu_field: '产品ID', type: 'number' },
    'product_name': { feishu_field: '产品名称', type: 'text' },
    'price': { feishu_field: '价格', type: 'number', precision: 2 },
    'created_date': { feishu_field: '创建日期', type: 'date' }
  }
};

// 自动转换
function mapToFeishu(tableName, record) {
  const mapping = fieldMapping[tableName];
  const fields = {};

  for (const [sqlField, config] of Object.entries(mapping)) {
    fields[config.feishu_field] = convertType(
      record[sqlField],
      config.type
    );
  }

  return { fields };
}
```

---

## 四、AI 层设计

### 4.1 Skills 体系

#### Skill 分类

```
查询类 Skills：
├── 查询库存 Skill
├── 查询订单 Skill
├── 查询客户信息 Skill
└── 查询财务数据 Skill

操作类 Skills：
├── 创建订单 Skill
├── 更新库存 Skill
├── 分配任务 Skill
└── 发送通知 Skill

分析类 Skills（核心价值）：
├── 财务健康分析 Skill
├── 生产效能诊断 Skill
├── 人力饱和度评估 Skill
├── 库存优化建议 Skill
└── 异常检测与预警 Skill
```

#### Skill 示例

```javascript
// 查询库存 Skill
async function queryInventory(productName) {
  // 1. 连接 SQL Server
  const db = await connectToSQLServer();

  // 2. 查询库存
  const result = await db.query(`
    SELECT
      p.product_name,
      p.specification,
      i.quantity,
      w.warehouse_name
    FROM inventory i
    JOIN products p ON i.product_id = p.product_id
    JOIN warehouses w ON i.warehouse_id = w.warehouse_id
    WHERE p.product_name LIKE @productName
  `, [{ name: 'productName', value: `%${productName}%` }]);

  // 3. 返回结果
  return result;
}

// 财务健康分析 Skill
async function analyzeFinancialHealth(startDate, endDate) {
  // 1. 查询财务数据
  const revenue = await queryRevenue(startDate, endDate);
  const costs = await queryCosts(startDate, endDate);
  const profit = revenue - costs;
  const profitMargin = (profit / revenue) * 100;

  // 2. 分析问题
  const issues = [];
  if (profitMargin < 10) {
    issues.push({
      type: '利润率过低',
      severity: '高',
      description: `净利润率仅为 ${profitMargin.toFixed(2)}%，低于行业平均水平`,
      suggestion: '建议审查成本结构，考虑优化采购成本或提高产品价格'
    });
  }

  // 3. 返回分析结果
  return {
    period: { startDate, endDate },
    summary: { revenue, costs, profit, profitMargin },
    issues,
    recommendations: generateRecommendations(issues)
  };
}
```

---

### 4.2 AI Agent 交互流程

```
用户输入（飞书 Chat）
    ↓
AI Agent 接收
    ↓
意图识别
    ├── 查询类 → 调用查询 Skills
    ├── 操作类 → 调用操作 Skills
    └── 分析类 → 调用分析 Skills
    ↓
执行 Skills
    ├── 读取 SQL Server 数据
    ├── 进行数据处理和分析
    └── 生成分析结果
    ↓
结果处理
    ├── 格式化输出
    ├── 写入飞书多维表格（可选）
    └── 推送消息通知
    ↓
返回给用户
```

---

## 五、开发计划

### 5.1 第一阶段：基础架构（2-3 周）

```
✅ 部署 QClaw/QwClaw 到飞书
✅ 搭建 Web 前端框架（Vue 3）
✅ 搭建 Web API 服务（Node.js）
✅ 实现 SQL Server 数据库连接
✅ 实现飞书 ↔ SQL Server 数据同步（基础版）
✅ 实现 1-2 个示例 Skills
```

### 5.2 第二阶段：核心功能（1-2 个月）

**Web 端**：
```
✅ 订单管理（CRUD）
✅ 产品管理
✅ 客户管理
✅ 基础报表查询
```

**飞书端**：
```
✅ AI Chat 查询（库存、订单）
✅ 飞书多维表格展示（汇总数据）
✅ AI 基础分析（销售日报、库存预警）
```

### 5.3 第三阶段：深化能力（3-6 个月）

**Web 端**：
```
✅ 完整的业务流程
✅ 复杂报表分析
✅ 系统配置管理
```

**飞书端**：
```
✅ 高级 AI 分析（财务健康、生产效能、人力评估）
✅ 7×24 监控预警
✅ 任务管理看板
✅ 移动端深度优化
```

---

## 六、技术参考资源

### 6.1 飞书开发资源

- [飞书开放平台](https://open.feishu.cn/)
- [飞书多维表格 API](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-record)
- [飞书机器人开发指南](https://open.feishu.cn/document/server-docs/docs/bot-v3/bot-overview)

### 6.2 SQL Server 开发资源

- [Node.js SQL Server 驱动（mssql）](https://www.npmjs.com/package/mssql)
- [SQL Server CDC（变更数据捕获）](https://docs.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server)

### 6.3 AI Agent 资源

- [OpenClaw 官方文档](https://github.com/antpcs/openclaw)
- [飞书妙搭一键部署 OpenClaw](https://www.feishu.cn/content/article/7615218249831058381)

---

## 文档说明

本文档详细描述了 AiERP 项目的技术架构设计，包括总体架构、数据库设计、数据同步方案、AI 层设计和开发计划等内容。

该文档将作为项目开发的技术指导文档。
