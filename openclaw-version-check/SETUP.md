# OpenClaw Version Check Skill - Setup Guide

## 已完成的内容

✅ **Cron 任务**已设置
- 每天 UTC 9:00 自动提醒检查 OpenClaw 版本
- Job ID: `bce602cb-772a-4989-91a0-33875cc4c444`

✅ **Skill 已创建并打包**
- 文件: `openclaw-version-check.skill`
- 包含: 版本检查脚本 + GitHub 同步脚本 + 参考文档

## 下一步：同步到 GitHub

### 方式 1：手动上传到 myskill 仓库

```bash
# 1. 解压 skill 包
tar -xzf openclaw-version-check.skill

# 2. 进入你的 myskill 仓库
cd /path/to/myskill

# 3. 复制 skill 文件夹
cp -r openclaw-version-check ./skills/

# 4. 提交和推送
git add skills/openclaw-version-check/
git commit -m "Add openclaw-version-check skill"
git push origin main
```

### 方式 2：使用内置的 GitHub Sync（推荐）

先配置环境变量：

```bash
# 在 Zeabur 中设置这些环境变量
export GITHUB_REPO="your-username/myskill"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
export VERSION_LOG_PATH="./logs"
```

然后运行脚本：

```bash
./skills/openclaw-version-check/scripts/check_version.sh
./skills/openclaw-version-check/scripts/sync_to_github.sh
```

## 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置 scope: `repo` (完整的仓库控制权)
4. 点击 "Generate token"
5. **立即复制** token（只显示一次！）

## 自动化流程

在 Zeabur 中设置 Cron 任务，每 6 小时自动检查和同步：

```bash
0 */6 * * * cd /home/node/.openclaw/workspace && ./skills/openclaw-version-check/scripts/check_version.sh && ./skills/openclaw-version-check/scripts/sync_to_github.sh
```

## 验证设置

运行测试：

```bash
# 检查版本
./skills/openclaw-version-check/scripts/check_version.sh

# 应该输出类似:
# ✅ Version check completed
#    Current:  2026.1.29
#    Latest:   2026.1.29
#    Status:   up-to-date
#    Log:      ./version-history.json
```

## 文件结构

```
myskill/
├── skills/
│   └── openclaw-version-check/
│       ├── SKILL.md                    # Skill 定义
│       ├── scripts/
│       │   ├── check_version.sh        # 检查版本脚本
│       │   └── sync_to_github.sh       # GitHub 同步脚本
│       └── references/
│           ├── API.md                  # NPM API 参考
│           └── GITHUB-SYNC.md          # GitHub 同步指南
└── logs/
    └── version-history.json            # 版本历史日志
```

## 故障排除

### 问题：Permission denied

```bash
chmod +x ./skills/openclaw-version-check/scripts/*.sh
```

### 问题：jq 未安装

脚本使用 `grep` 和 `sed`，不需要 `jq`。如果出错，检查 `/app/package.json` 路径是否正确。

### 问题：GitHub 认证失败

- 确保 `GITHUB_TOKEN` 有效（未过期）
- 确保 token 有 `repo` scope
- 检查 `GITHUB_REPO` 格式：`username/repo`
