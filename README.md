# MySkill - Custom Clawdbot Skills

个人定制 Clawdbot Agent Skills 仓库。包含博客发布、配置管理等专业工具。

## 📚 Available Skills

### 1. blog-publishing

完整的 MDX 博客发布工作流。包含：
- 📖 完整的写作指南
- 🔐 Firebase 安全认证
- 💻 发布脚本 + Web UI
- 🐛 故障排除指南

**目录结构：**
```
blog-publishing/
├── SKILL.md                    # 完整工作流指南
├── references/
│   ├── mdx-template.md        # 完整的 MDX 示例
│   ├── markdown-cheatsheet.md # Markdown 速查表
│   └── firebase-guide.md      # Firebase 配置调试
├── assets/
│   └── blog-template.mdx      # 快速开始模板
└── scripts/
    └── publish.sh             # 发布脚本
```

**使用场景：**
- 创建新博客文章
- 发布到 Firebase Firestore
- 管理博客元数据
- 故障排除和安全配置

### 2. clawdbot-config

Clawdbot 配置、环境设置和集成指南。包含：
- ⚙️ 配置文件架构
- 🔌 集成模式（GitHub, Discord, Google 等）
- 📝 环境变量管理
- 🚀 部署到 Zeabur 和本地

**目录结构：**
```
clawdbot-config/
├── SKILL.md                    # 完整配置指南
└── references/
    ├── config-schema.md       # 配置文件 JSON schema
    ├── environment-variables.md # 环境变量说明
    ├── integrations.md        # 集成步骤
    └── examples.md            # 实际配置示例
```

**使用场景：**
- 配置 Clawdbot 新集成
- 管理环境变量
- 故障排除部署问题
- 了解配置文件架构

## 🔄 Synchronization

Skills 会自动从主环境同步到这个仓库。同步频率：
- 自动：每小时（通过 cron job）
- 手动：运行 `sync-skills.py` 脚本

```bash
python3 sync-skills.py
```

## 📦 Installation / Usage

### 在 Clawdbot 中使用

1. **复制 skill 文件夹到你的环境：**
   ```bash
   cp -r blog-publishing /your/clawdbot/skills/
   ```

2. **Clawdbot 自动加载 skill**（无需重启）

3. **触发 skill**（通过描述匹配）：
   - 问关于博客的问题 → `blog-publishing` skill 触发
   - 问关于配置的问题 → `clawdbot-config` skill 触发

### 独立使用脚本

某些 skill 包含独立脚本：

```bash
# 博客发布脚本
export BLOG_AUTH_TOKEN="your-token-here"
python3 blog-publishing/scripts/publish.sh your-article.mdx
```

## 🔐 Security

- **不要提交**敏感信息（API 密钥、token 等）
- 使用环境变量存储凭证
- 所有脚本应该从环境变量读取敏感数据

## 📝 Contributing

有想法改进？
1. Fork 仓库
2. 创建新 branch (`git checkout -b feature/my-improvement`)
3. 提交 PR

或直接在主环境中修改，自动同步会推送更改。

## 📅 Changelog

### v1.0.0 (2026-01-29)
- ✅ 初始化仓库
- ✅ 添加 `blog-publishing` skill
- ✅ 添加 `clawdbot-config` skill
- ✅ 设置自动同步机制

## 📖 References

- [Clawdbot 文档](https://docs.clawd.bot)
- [Skill Creator 指南](/app/skills/skill-creator/SKILL.md)

---

**自动同步时间：** 最后同步 @ `[timestamp]`（见 `.sync-info`）
