---
name: ai-comic-drama-pipeline
description: Create and continue serialized AI漫剧 projects from reference-story originalization through concept selection, story bible, episodic adaptation, episode beats, 15-second shot scripts, visual asset management, Seedance 2.0 Mini prompts, and continuity review. Use for AI漫剧策划、分集、分镜、资产库、视频提示词或生成质检；do not use for unrelated general fiction writing.
---

# AI漫剧流水线

把项目作为有状态的九阶段生产流程处理。先确认用户要做的阶段；只读取该阶段的参考文件及其明确依赖，不一次加载全部参考资料。

## 路由

| 阶段 | 请求特征 | 读取 |
|---|---|---|
| 1 原创化 | 参考小说、拆机制、生成三个原创方向 | [references/01-originalization.md](references/01-originalization.md) |
| 2 选型 | 三个骨架、评分、选最佳方案 | [references/02-evaluation.md](references/02-evaluation.md) |
| 3 故事总纲 | 胜出骨架、完整长线故事、故事圣经 | [references/03-story-bible.md](references/03-story-bible.md) |
| 4 漫剧改编 | 总纲转分集、集数规划、短视频化 | [references/04-adaptation.md](references/04-adaptation.md) |
| 5 单集节奏 | 某一集、60/75/90秒节拍 | [references/05-episode-beats.md](references/05-episode-beats.md) |
| 6 分镜剧本 | 15秒段落、对白强化、镜头脚本 | [references/06-shot-script.md](references/06-shot-script.md) |
| 7 资产管理 | 角色/LOOK/场景/道具、资产图提示词 | [references/07-assets.md](references/07-assets.md) |
| 8 视频提示词 | Seedance 2.0 Mini、0秒/尾帧、15秒时间轴 | [references/08-seedance.md](references/08-seedance.md) |
| 9 终审 | 生成视频检查、连续性、返修路由 | [references/09-review.md](references/09-review.md) |

用户说“继续”时，读取当前项目的 `project.yaml` 和 `state/continuity.yaml`，从 `current_stage`、`current_episode`、`current_segment` 判断下一步。若没有项目状态但上下文足以判断，继续当前阶段；否则只询问缺失的项目或阶段。

## 项目状态

新项目优先运行 `python scripts/init_project.py --root <项目父目录> --name <项目名> --episodes 60 --duration 90`。状态格式见 [references/project-state.md](references/project-state.md)。每次完成一个阶段：保存阶段产物；更新当前位置；只把确认的新事实写入状态库；运行 `python scripts/validate_project.py <项目目录>`。

## 单一真源

锁定后只能引用或细化：核心卖点、主角欲望、核心矛盾、终局真相、结局方向；角色身份与固定外观；LOOK、场景结构、道具外观；知识状态、道具归属及上一段尾帧状态。

确需修改时，先输出并记录：`原值 → 新值 → 理由 → 连锁影响`。剧情事实优先于生成模型偶发结果；脸漂、多手或穿模不得反写进正式资产库。

## 工作边界

- 阶段1学习抽象机制，不复刻专有表达或连续关键桥段。
- 阶段3保证故事成立；阶段4再短视频化和降本改编。
- 阶段5决定15秒剧情任务；阶段6决定镜头和台词；阶段8只编译执行提示词。
- 阶段7管理基础资产与长期LOOK，不把临时表情、伤势或持物建成新角色。
- 有合格真实尾帧时用图像连续模式；否则使用文字状态链。

## 返修路由

- 故事结构或整集节奏：阶段5。
- 分镜、对白或动作负载：阶段6。
- 角色、LOOK、场景或道具定义：阶段7。
- Seedance时间轴、0秒状态、尾帧或运镜：阶段8。
- 单次随机生成缺陷：只重生成当前片段。

输出唯一明确结果或最终版本，不同时给出多个互相冲突的状态版本。
