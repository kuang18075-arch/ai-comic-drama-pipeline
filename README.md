# AI Comic Drama Pipeline Skill

一个面向 Codex 的有状态 AI 漫剧生产 Skill，覆盖原创化、方案评分、故事总纲、分集改编、单集节奏、15秒分镜、视觉资产、Seedance 2.0 Mini 提示词和生成终审。

## 安装

将仓库目录复制到 `$CODEX_HOME/skills/ai-comic-drama-pipeline`，重启 Codex 后使用 `$ai-comic-drama-pipeline`。

## 新建项目

```powershell
python scripts/init_project.py --root ./projects --name "我的漫剧" --episodes 60 --duration 90
python scripts/validate_project.py "./projects/我的漫剧"
```

Skill 会根据请求按需加载九个流程模块，并通过项目状态文件保持人物、关系、服装、场景、道具和镜头连续性。
