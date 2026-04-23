# Claude Code 开发智慧城市 SOP 对应 Skills 设计与调试优化建议

你担心**单 Skills 承载全 SOP 步骤、多 MCP 调用导致程序混乱难调试**的问题非常关键，Claude Code 中 Skills 的设计核心是「**职责解耦、轻量化、可独立调试**」，若将全流程 SOP 揉进一个 Skills，必然会出现逻辑嵌套深、MCP 调用耦合高、调试时定位问题困难的情况。结合智慧城市 SOP 的 8 大核心模块特性，核心解决方案是 **「按 SOP 流程拆分子 Skills + 总控 Skills 调度 + 标准化接口衔接」**，以下是具体可落地的设计思路、拆分原则、调试技巧和避坑点，完全适配 Claude Code 的运行特性。

## 一、核心设计原则：从根源避免程序混乱

在开发前先明确 3 个核心原则，所有 Skills 的设计都围绕这 3 点展开，从底层降低耦合度和调试成本：

1. **单一职责原则**：每个子 Skills 只负责**智慧城市 SOP 中的一个独立环节**，不跨模块处理逻辑，比如 “资料收集校验” 的 Skills 不参与 “方案撰写”，“技术选型分析” 的 Skills 不处理 “方案审核调整”；
2. **低耦合高内聚**：子 Skills 之间仅通过**标准化输入输出**衔接，无直接的 MCP 调用依赖，每个 Skills 仅调用完成自身职责**必需的 MCP**，杜绝无关 MCP 的引入；
3. **可独立调试**：每个子 Skills 均可脱离总控单独运行，传入模拟的标准化输入就能验证功能和 MCP 调用是否正常，无需依赖其他模块的执行结果。

## 二、关键设计方案：按 SOP 拆分子 Skills + 总控 Skills 调度

结合你确认的智慧城市 SOP8 大核心模块（知识库管理、项目初始化、资料收集、信息总结、项目理解、技术选型、方案设计、审核输出），将其拆分为 **「8 个独立子 Skills+1 个总控 Skills」**，总控 Skills 仅做「流程调度、状态管理、接口衔接」，不处理具体业务逻辑，子 Skills 专注单一业务 + 专属 MCP 调用，整体架构如下：

plaintext











```
【总控Skills】SmartCity_SOP_Main
    ↓ 按SOP顺序调度/根据用户确认指令触发
【子Skills1】SmartCity_KB_Manager（知识库管理）
【子Skills2】SmartCity_Project_Initiator（项目初始化）
【子Skills3】SmartCity_Data_Checker（资料收集/校验/冲突处理）
【子Skills4】SmartCity_Info_Summary（项目核心信息总结）
【子Skills5】SmartCity_Project_Understand（项目理解描述）
【子Skills6】SmartCity_Tech_Selection（技术提示与选型分析）
【子Skills7】SmartCity_Scheme_Writer（方案设计与细节撰写）
【子Skills8】SmartCity_Scheme_Revise（方案审核调整）
【子Skills9】SmartCity_Scheme_Output（最终落地输出）
```

### 各 Skills 核心职责与 MCP 调用边界（关键：杜绝 MCP 滥用）

每个子 Skills 仅绑定**完成自身职责的最小 MCP 集合**，不跨模块调用，避免 MCP 混乱，以下是核心划分（可根据你的实际 MCP 类型微调）：

|         子 Skills 名称         |                  核心职责                   |               专属调用 MCP 类型               |         禁止调用 MCP         |
| :----------------------------: | :-----------------------------------------: | :-------------------------------------------: | :--------------------------: |
|      SmartCity_KB_Manager      |       知识库加载、更新适配、版本校验        |     文档存储 / 读取 MCP、配置文件解析 MCP     |   所有业务类、格式生成 MCP   |
|  SmartCity_Project_Initiator   |        项目信息收集、初始化参数生成         |          无（仅用户交互 + 参数封装）          |    所有 MCP（纯逻辑处理）    |
|     SmartCity_Data_Checker     | 资料格式校验、缺失 / 冲突识别、提交清单生成 | 文件解析 MCP（PDF/Excel/ 音频）、对比校验 MCP |     知识库、格式生成 MCP     |
|     SmartCity_Info_Summary     |     核心信息提取、模块结构化、来源标注      |               无（纯数据整理）                |           所有 MCP           |
|  SmartCity_Project_Understand  |  业务模块划分、通用内容补充、建设边界界定   |           行业规范查询 MCP（可选）            |    方案撰写、格式生成 MCP    |
|    SmartCity_Tech_Selection    |     技术适配分析、软硬件选型、标注生成      |         技术库查询 MCP、场景适配 MCP          |    文档编辑、格式生成 MCP    |
|    SmartCity_Scheme_Writer     |     章节撰写、技术融合点标注、格式校验      |        Markdown 生成 MCP、字数统计 MCP        |    文件解析、行业查询 MCP    |
|    SmartCity_Scheme_Revise     |     修改意见响应、内容调整、总览表更新      |        Markdown 编辑 MCP、表格同步 MCP        |    技术选型、文件解析 MCP    |
|    SmartCity_Scheme_Output     |       定稿生成、配套表输出、格式优化        |        Markdown 导出 MCP、表格生成 MCP        |      所有业务处理类 MCP      |
| **SmartCity_SOP_Main（总控）** | 流程调度、用户确认交互、状态记录、异常兜底  |              **无任何业务 MCP**               | 所有具体业务 MCP（仅做调度） |

### 标准化接口设计：子 Skills 之间的衔接核心

混乱的根源之一是「数据传递无标准」，因此必须为所有子 Skills 定义**统一的输入（Input）/ 输出（Output）格式**，采用**JSON 结构**（Claude Code 对 JSON 解析 / 封装支持最好），所有子 Skills 的输入输出均遵循此规范，总控 Skills 仅负责传递标准化数据，无需处理数据格式转换。

#### 1. 通用输入格式（所有子 Skills 基础输入，可按需扩展）

json











```
{
  "project_id": "项目唯一标识（总控生成，如SC20260124001）",
  "project_type": "智慧城市细分场景（如智慧园区/智慧医疗）",
  "user_info": "用户手工输入的专属信息（字符串/结构化对象）",
  "prev_module_data": "上一模块输出的标准化数据（JSON）",
  "status": "当前流程状态（待执行/已确认/需调整）",
  "extra_params": "模块专属扩展参数（如撰写章节编号/修改意见）"
}
```

#### 2. 通用输出格式（所有子 Skills 基础输出，可按需扩展）

json











```
{
  "project_id": "项目唯一标识（与输入一致）",
  "module_name": "当前模块名称（如资料收集校验）",
  "execute_status": "执行状态（成功/失败/需用户确认）",
  "module_data": "当前模块生成的核心业务数据（JSON，供下一模块使用）",
  "error_info": "错误信息（失败时填写，含错误位置/MCP调用问题）",
  "next_module": "建议下一个执行的模块（如信息总结）",
  "user_confirm_msg": "需用户确认的内容（需确认时填写，如冲突项清单/总结报告）"
}
```

**关键优势**：无论哪个子 Skills，总控和其他模块都能按固定格式解析数据，无需关注内部逻辑，调试时只需检查 JSON 字段是否完整，即可快速定位 “数据传递问题” 还是 “模块内部逻辑问题”。

## 三、总控 Skills（SmartCity_SOP_Main）核心设计：极简调度，不做业务

总控 Skills 是整个 SOP 的 “大脑”，但**代码量最少、逻辑最简单**，仅负责 4 件事，**不调用任何业务 MCP、不处理任何具体业务逻辑**，从根源避免总控成为 “混乱中心”，核心功能如下：

1. **流程初始化**：接收用户启动指令（场景 + 基础信息），生成项目唯一标识（project_id），初始化流程状态（待执行），调用第一个子 Skills（SmartCity_Project_Initiator）；
2. **按序调度**：根据上一个子 Skills 的输出「next_module」和「execute_status」，自动调用下一个子 Skills，传递标准化输入数据；
3. **用户交互衔接**：当子 Skills 输出「execute_status = 需用户确认」时，暂停流程，将「user_confirm_msg」推送给用户，接收用户确认 / 修改指令后，再继续调度下一个模块；
4. **状态管理与异常兜底**：记录每个模块的执行状态、执行时间、输出数据，若某个子 Skills 输出「execute_status = 失败」，立即暂停流程，将「error_info」推送给用户，支持用户选择 “重新执行当前模块” 或 “跳过（手动处理）”，避免单模块失败导致全流程崩溃。

**总控 Skills 代码核心特点**：仅包含「条件判断（状态）+ 模块调用（子 Skills）+ 数据传递（JSON）」，无嵌套循环、无复杂逻辑，行数控制在 50 行以内，调试几乎无成本。

## 四、子 Skills 开发技巧：轻量化、可独立调试、MCP 调用规范化

### 1. 子 Skills 代码轻量化：单个 Skills 代码行数控制在 100 行以内

Claude Code 中 Skills 的最佳实践是 “小而精”，单个 Skills 代码行数过多会导致调试时翻找困难，因此子 Skills 开发时需做到：

- 避免复杂嵌套：最多 1 层 if-else 判断（如 “是否存在用户专属信息”“MCP 调用是否成功”），杜绝多层嵌套；
- 重复逻辑封装：将 “输入参数校验”“JSON 格式封装”“MCP 调用结果解析” 等重复逻辑封装为**内部小函数**（如`check_input_params(input)`、`parse_mcp_result(res)`），函数行数控制在 10 行以内；
- 只做核心事：比如 SmartCity_Scheme_Writer 仅负责 “按规则撰写章节内容 + 标注”，不做 “内容审核”“格式导出”，这些交给后续模块。

### 2. MCP 调用规范化：杜绝乱调用，做好 “调用前校验 + 调用后处理 + 异常捕获”

MCP 调用是子 Skills 中最容易出问题的环节，需为每个 MCP 调用添加 “三层保障”，确保调用可控、问题可定位：

python



运行









```
# 子Skills中MCP调用的标准模板（适配Claude Code）
def call_mcp_example(mcp_name, mcp_params):
    # 1. 调用前：参数校验（确保MCP所需参数完整）
    required_params = ["project_type", "module_data"]
    for param in required_params:
        if param not in mcp_params:
            return {"status": "fail", "error": f"MCP调用参数缺失：{param}"}
    # 2. 调用中：异常捕获（捕获MCP调用超时、失败等问题）
    try:
        mcp_result = claude_mcp.call(mcp_name, mcp_params)  # Claude Code MCP调用原生方法
    except TimeoutError:
        return {"status": "fail", "error": f"MCP {mcp_name} 调用超时"}
    except Exception as e:
        return {"status": "fail", "error": f"MCP {mcp_name} 调用失败：{str(e)}"}
    # 3. 调用后：结果解析（将MCP返回结果转为标准化格式，避免后续处理混乱）
    if not mcp_result or "data" not in mcp_result:
        return {"status": "fail", "error": f"MCP {mcp_name} 返回结果无效：{mcp_result}"}
    return {"status": "success", "data": mcp_result["data"]}
```

**额外要求**：每个子 Skills 中，MCP 调用代码**集中放在一个函数中**，不分散在业务逻辑里，调试时只需检查这个函数，即可快速定位 MCP 调用问题。

### 3. 可独立调试：为每个子 Skills 编写 “模拟测试用例”

每个子 Skills 开发完成后，**无需启动总控**，直接在 Skills 末尾添加「模拟测试代码」，传入符合标准的输入 JSON，即可单独验证功能和 MCP 调用是否正常，测试用例示例：

python



运行









```
# SmartCity_Data_Checker 子Skills的模拟测试用例（单独运行即可）
if __name__ == "__main__":
    # 模拟总控传入的标准化输入
    test_input = {
        "project_id": "SC20260124001",
        "project_type": "智慧园区",
        "user_info": "手工输入：项目预算500万，交付时间2026年6月",
        "prev_module_data": {"data_list": ["需求文档.pdf", "软硬件清单.xlsx"]},
        "status": "待执行",
        "extra_params": {}
    }
    # 调用当前Skills核心函数
    test_output = core_process(test_input)
    # 打印输出，验证是否符合标准化格式
    print("模拟执行结果：", json.dumps(test_output, ensure_ascii=False, indent=2))
```

**调试优势**：若子 Skills 执行失败，可直接通过测试用例定位是「输入参数问题」「MCP 调用问题」还是「业务逻辑问题」，无需启动全流程，大幅提升调试效率。

## 五、整体开发与调试流程：分阶段推进，逐步联调

建议按「**子 Skills 独立开发→单模块调试→总控 Skills 开发→全流程联调→优化**」的步骤推进，避免一次性开发全流程导致问题集中，无法定位：

### 阶段 1：子 Skills 独立开发 + 单模块调试（核心阶段，占 80% 工作量）

1. 按 SOP 模块顺序，逐个开发子 Skills，每个 Skills 开发完成后，通过「模拟测试用例」单独运行，验证：

   - 输入参数校验是否有效；
   - MCP 调用是否成功，结果是否符合预期；
   - 输出数据是否遵循标准化 JSON 格式；
   - 业务逻辑是否符合 SOP 规则（如是否按要求标注、是否拆分软硬件投入）；

   

2. 单个子 Skills 调试通过后，再开发下一个，确保每个子 Skills 都是 “可用状态”。

### 阶段 2：总控 Skills 开发（极简开发，10% 工作量）

基于标准化接口，开发总控 Skills，仅实现「流程调度、状态管理、用户交互」核心功能，无需处理任何业务逻辑，开发完成后，通过模拟子 Skills 输出，验证总控的调度逻辑是否正常。

### 阶段 3：全流程联调（10% 工作量）

1. 从第一个子 Skills（SmartCity_Project_Initiator）开始，由总控调度，逐步执行每个模块，**每执行一个模块，暂停并检查输出数据**，确保数据传递无问题；

2. 重点测试「用户确认环节」和「异常兜底环节」：

   - 模拟子 Skills “需用户确认”，验证总控是否能暂停并接收用户指令；
   - 模拟某个子 Skills “执行失败”，验证总控是否能捕获异常并提供兜底选项；

   

3. 若联调中发现问题，

   先定位是子 Skills 问题还是总控调度问题

   ：

   - 若单个子 Skills 单独运行正常，联调失败→大概率是总控数据传递问题；
   - 若单个子 Skills 单独运行失败→子 Skills 内部问题，返回阶段 1 重新调试。

   

### 阶段 4：优化（持续进行）

1. 优化 MCP 调用性能：对频繁调用的 MCP，添加缓存（如行业规范查询 MCP），避免重复调用；
2. 优化用户体验：简化用户确认环节的提示信息，让用户操作更便捷；
3. 优化代码：删除冗余代码，合并重复函数，提升 Skills 运行效率。

## 六、避坑点：Claude Code 中开发 Skills 的关键注意事项

1. **避免在 Skills 中存储全局状态**：Claude Code 中 Skills 的全局变量可能会在多次调用后被覆盖，所有状态信息均由**总控 Skills 统一管理**，子 Skills 仅通过输入输出传递数据，无全局状态；
2. **MCP 调用超时处理**：部分 MCP（如大文件解析、文档生成）可能存在超时问题，需在子 Skills 中为 MCP 调用添加**超时时间限制**，并捕获超时异常，避免单 MCP 调用超时导致整个 Skills 卡死；
3. **JSON 格式严格性**：Claude Code 对 JSON 解析的严格性较高，所有子 Skills 的输出必须是**合法的 JSON 格式**，避免出现语法错误（如逗号结尾、引号不匹配），导致总控无法解析；
4. **避免子 Skills 之间的直接依赖**：所有子 Skills 之间的衔接必须通过**总控 Skills**，禁止子 Skills 直接调用其他子 Skills，否则会导致流程混乱，调试困难；
5. **代码注释规范化**：在每个子 Skills 的 MCP 调用处、核心业务逻辑处添加简洁注释，标注 “对应 SOP 哪条规则”，方便后续维护和调试（如`# 按SOP规则，拆分硬件/软件/运维投入，无数值则标注缺失`）。

## 七、总结

将智慧城市 SOP 转化为 Claude Code 的 Skills，**核心不是 “整合” 而是 “拆分”**，通过「**8+1**」的 Skills 架构（8 个子 Skills+1 个总控 Skills），实现：

1. 每个子 Skills「单一职责、轻量化、可独立调试」，解决 “内容太多、MCP 调用太乱” 的问题；
2. 标准化 JSON 接口实现子 Skills 与总控的低耦合衔接，数据传递可控；
3. 总控 Skills 极简调度，不做业务，避免成为 “混乱中心”；
4. 分阶段开发与调试，逐步推进，避免问题集中。