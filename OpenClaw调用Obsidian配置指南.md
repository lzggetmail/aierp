# OpenClaw调用Obsidian配置指南

## 📋 配置概览

本文档提供OpenClaw智能体平台调用Obsidian笔记软件的完整配置方案，支持三种不同的集成方法。

---

## 🔧 方法一：本地文件操作（最推荐）

### 优势
- ✅ 无需额外插件
- ✅ 性能最优，直接文件读写
- ✅ 配置简单，开箱即用
- ✅ 支持相对路径，便于管理

### 配置步骤

#### 1. 设置Vault路径
```python
# OpenClaw配置文件
VAULT_CONFIG = {
    "vault_path": r"D:\AiERP",  # 你的Obsidian vault路径
    "notes_folder": "Ai知识库",  # 笔记存放文件夹
    "attachments_folder": "attachments"  # 附件文件夹
}
```

#### 2. 定义工具函数
```python
import os
from pathlib import Path

class ObsidianTools:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)

    def read_note(self, file_path):
        """读取笔记内容"""
        full_path = self.vault_path / file_path
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_note(self, file_path, content):
        """写入笔记内容"""
        full_path = self.vault_path / file_path
        # 确保目录存在
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def search_notes(self, keyword):
        """搜索笔记"""
        results = []
        for md_file in self.vault_path.rglob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if keyword in content:
                    relative_path = md_file.relative_to(self.vault_path)
                    results.append({
                        "path": str(relative_path),
                        "preview": content[:200]
                    })
        return results

    def list_notes(self, folder=""):
        """列出笔记"""
        target_folder = self.vault_path / folder if folder else self.vault_path
        notes = []
        for md_file in target_folder.rglob("*.md"):
            relative_path = md_file.relative_to(self.vault_path)
            notes.append(str(relative_path))
        return notes
```

#### 3. OpenClaw智能体配置
```python
# OpenClaw智能体配置
AGENT_CONFIG = {
    "name": "Obsidian助手",
    "role": """你是一个专业的Obsidian笔记管理助手，可以帮助用户：
1. 读取和分析笔记内容
2. 创建新的学习笔记
3. 搜索和组织知识
4. 维护笔记间的链接关系

注意事项：
- 文件路径使用相对于vault的路径
- 笔记名称使用中文，便于管理
- 自动添加相关标签
- 保持markdown格式规范
""",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "read_obsidian_note",
                "description": "读取Obsidian笔记的完整内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "笔记的相对路径，例如：Ai知识库/笔记名称.md"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_obsidian_note",
                "description": "创建新的Obsidian笔记",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "笔记的相对路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "笔记的markdown内容"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "笔记标签列表"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_obsidian_notes",
                "description": "在Obsidian vault中搜索包含关键词的笔记",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "folder": {
                            "type": "string",
                            "description": "限定搜索文件夹（可选）"
                        }
                    },
                    "required": ["keyword"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_obsidian_notes",
                "description": "列出指定文件夹下的所有笔记",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "folder": {
                            "type": "string",
                            "description": "文件夹路径（可选，默认列出所有）"
                        }
                    }
                }
            }
        }
    ]
}
```

#### 4. 使用示例
```python
# 创建Obsidian工具实例
obsidian = ObsidianTools(r"D:\AiERP")

# 读取笔记
content = obsidian.read_note("Ai知识库/【AI学习】智能经济新形态与一人公司黄金时代全解析.md")

# 搜索笔记
results = obsidian.search_notes("一人公司")

# 创建新笔记
new_note_content = """# 新建笔记

这是一个通过OpenClaw创建的笔记。

## 标签
#AI学习 #OpenClaw #Obsidian
"""
obsidian.write_note("Ai知识库/新笔记.md", new_note_content)
```

---

## 🌐 方法二：Obsidian Local REST API

### 前置准备
1. 在Obsidian中安装"Local REST API"插件
2. 在插件设置中启用服务
3. 记录端口号（默认27124）和API密钥（如已设置）

### 配置代码
```python
import requests
import json

class ObsidianAPI:
    def __init__(self, base_url="http://localhost:27124", api_key=None):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def get_note(self, file_path):
        """获取笔记内容"""
        url = f"{self.base_url}/notes/{file_path}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_note(self, file_path, content):
        """创建笔记"""
        url = f"{self.base_url}/notes/{file_path}"
        response = requests.post(url, json={"content": content}, headers=self.headers)
        return response.json()

    def search_notes(self, query):
        """搜索笔记"""
        url = f"{self.base_url}/search"
        response = requests.get(url, params={"q": query}, headers=self.headers)
        return response.json()

    def append_to_note(self, file_path, content_to_append):
        """追加内容到笔记"""
        url = f"{self.base_url}/notes/{file_path}/append"
        response = requests.post(url, json={"content": content_to_append}, headers=self.headers)
        return response.json()
```

### OpenClaw集成
```python
# 在OpenClaw中注册API工具
api_tools = [
    {
        "name": "obsidian_api_read",
        "description": "通过REST API读取笔记",
        "function": lambda file_path: obsidian_api.get_note(file_path)
    },
    {
        "name": "obsidian_api_create",
        "description": "通过REST API创建笔记",
        "function": lambda file_path, content: obsidian_api.create_note(file_path, content)
    },
    {
        "name": "obsidian_api_search",
        "description": "通过REST API搜索笔记",
        "function": lambda query: obsidian_api.search_notes(query)
    }
]
```

---

## 💻 方法三：Obsidian CLI命令

### 前置准备
1. 安装支持CLI的Obsidian插件（如Advanced URI）
2. 配置命令行工具链

### 配置代码
```python
import subprocess
from pathlib import Path

class ObsidianCLI:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)

    def execute(self, command):
        """执行CLI命令"""
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=self.vault_path
        )
        if result.returncode == 0:
            return result.stdout
        else:
            raise Exception(f"CLI命令执行失败: {result.stderr}")

    def read_note(self, file_path):
        """读取笔记"""
        return self.execute(f"obsidian-cli read '{file_path}'")

    def write_note(self, file_path, content):
        """写入笔记"""
        return self.execute(f"obsidian-cli write '{file_path}' '{content}'")

    def search_notes(self, query):
        """搜索笔记"""
        return self.execute(f"obsidian-cli search '{query}'")
```

---

## 🎯 实战场景配置

### 场景1：自动化笔记整理
```python
ORGANIZER_AGENT = {
    "name": "笔记整理助手",
    "role": """你是笔记整理专家，负责：
1. 分析现有笔记结构
2. 识别重复或过时内容
3. 建议合并或拆分方案
4. 自动添加标签和链接
5. 生成笔记目录索引

工作流程：
1. 先用list_obsidian_notes了解现有笔记
2. 用read_obsidian_note分析内容
3. 提供整理建议
4. 使用create_obsidian_note创建新索引
""",
    "tools": ["read", "write", "search", "list"]
}
```

### 场景2：学习笔记助手
```python
LEARNING_AGENT = {
    "name": "学习笔记助手",
    "role": """你是学习笔记专家，负责：
1. 根据视频/文章内容生成结构化笔记
2. 自动提取核心观点和关键信息
3. 生成思维导图和知识图谱
4. 关联相关知识点
5. 创建复习计划和测试题

使用模板：
- 笔记基础信息
- 核心重点提炼
- 具体操作方法
- 核心观点整理
- 个人学习总结
""",
    "tools": ["read", "write", "search"]
}
```

### 场景3：知识库管理
```python
KNOWLEDGE_AGENT = {
    "name": "知识库管理员",
    "role": """你是知识库管理专家，负责：
1. 维护知识库目录结构
2. 确保笔记间链接正确
3. 检测孤立笔记
4. 生成知识地图
5. 定期备份和归档

注意事项：
- 保持文件命名规范
- 维护标签体系一致性
- 检查内部链接有效性
- 生成月度知识报告
""",
    "tools": ["read", "write", "search", "list"]
}
```

---

## 📝 注意事项

### 文件路径规范
- ✅ 使用相对路径：`Ai知识库/笔记.md`
- ❌ 避免绝对路径：`D:\AiERP\笔记.md`
- ✅ 使用正斜杠：`folder/note.md`
- ❌ 避免反斜杠：`folder\note.md`

### 内容格式规范
- 使用UTF-8编码
- 保持markdown标准格式
- 标签使用 `#标签名` 格式
- 内部链接使用 `[[笔记名]]` 格式

### 性能优化
- 大文件读写考虑分块处理
- 搜索操作可以添加缓存
- 定期清理冗余文件
- 建立索引提升搜索速度

---

## 🚀 快速开始

### 1. 最小配置示例
```python
# 创建Obsidian工具实例（方法一：文件操作）
from obsidian_tools import ObsidianTools

obsidian = ObsidianTools(r"D:\AiERP")

# 读取笔记
content = obsidian.read_note("Ai知识库/【AI学习】智能经济新形态与一人公司黄金时代全解析.md")
print(content)
```

### 2. OpenClaw集成示例
```python
# 在OpenClaw中配置智能体
agent_config = {
    "name": "我的Obsidian助手",
    "tools": [
        obsidian_tools.read_note,
        obsidian_tools.write_note,
        obsidian_tools.search_notes
    ],
    "prompt": "你是我的Obsidian笔记助手，帮我管理知识库"
}

# 注册智能体到OpenClaw
openclaw.register_agent(agent_config)
```

### 3. 测试连接
```python
# 测试Obsidian工具是否正常
try:
    notes = obsidian.list_notes("Ai知识库")
    print(f"找到 {len(notes)} 个笔记")
    print("最新笔记:", notes[-1])
except Exception as e:
    print(f"连接失败: {e}")
```

---

## 📚 扩展阅读

### 相关资源
- [Obsidian官方文档](https://help.obsidian.md/)
- [Local REST API插件](https://github.com/cvluo/obsidian-local-rest-api)
- [Advanced URI插件](https://github.com/Vinzent03/obsidian-advanced-uri)
- [OpenClaw官方文档](https://openclaw.dev/docs)

### 进阶功能
- Obsidian插件开发
- 自定义工作流
- 多vault管理
- 协作编辑
- 版本控制集成

---

## 💬 常见问题

### Q1: 如何处理中文文件名？
A: 使用UTF-8编码，确保文件路径正确转义：
```python
from pathlib import Path
file_path = "Ai知识库/笔记.md"
safe_path = Path(file_path)
```

### Q2: 如何批量处理笔记？
A: 使用glob模式匹配：
```python
for md_file in Path("Ai知识库").glob("*.md"):
    content = obsidian.read_note(str(md_file))
    # 处理内容
```

### Q3: 如何备份笔记？
A: 定期复制整个vault文件夹：
```python
import shutil
shutil.copytree("D:\\AiERP", f"backup_{datetime.now().strftime('%Y%m%d')}")
```

---

**提示**：建议从方法一（本地文件操作）开始，这是最简单且最稳定的方式。等熟悉后再尝试其他方法。
