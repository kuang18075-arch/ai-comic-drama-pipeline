# 项目状态规范

项目目录由 `scripts/init_project.py` 创建，YAML使用UTF-8。

- `project.yaml`：参数、当前位置、锁定故事事实。
- `state/characters.yaml`：角色及当前动态状态。
- `state/looks.yaml`：长期服装LOOK。
- `state/scenes.yaml`：固定空间资产。
- `state/props.yaml`：固定道具及当前归属。
- `state/continuity.yaml`：上一完成片段的尾帧状态。
- `story/`、`episodes/`、`reviews/`：阶段产物。

未知字段使用空值或空列表，不编造。ID必须唯一并匹配：角色 `CH-\d{3}`、LOOK `CH-\d{3}-LOOK-[A-Z]`、场景 `LOC-\d{3}`、道具 `PR-\d{3}`。

`project.yaml.locked` 是故事级单一真源；资产中的 `fixed` 和 `forbidden_changes` 是视觉级单一真源；`continuity.yaml` 只记录动态状态。阶段产物通过后再更新，返修草稿不得覆盖通过版。
