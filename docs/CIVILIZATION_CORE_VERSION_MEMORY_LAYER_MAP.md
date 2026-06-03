# 文明之核：版本到十五层记忆映射表

状态：v2.10-pre 框架纠偏文档
范围：v2.0 至 v2.9 版本链、十五层记忆、后续 v2.10 方向
性质：版本坐标映射；不新增能力、不改变 release tag、不写入 durable memory

## 1. 映射原则

工程版本不能替代记忆层级。版本号、PR、tag、测试、审计和工具链只是工程事实
或治理封印，不能取代文明之核的十五层记忆坐标。

每一个版本都必须映射回十五层记忆。一个版本可以支撑多个层级，但必须有一个
主层级，用于说明该版本对文明之核最高记忆体系的主要推进。

映射表用于约束叙事边界：它说明版本做了什么、推进了哪一层、支撑了哪些层、
对文明之核意味着什么，以及绝不能跨越的边界。

## 2. v2.0-v2.9 映射表

| Version | Engineering deliverable | Primary memory layer | Supporting memory layers | Civilization Core meaning | Boundary that must not be crossed |
| --- | --- | --- | --- | --- | --- |
| v2.0.0 | token authority boundary | 星律记忆雏形 | 星穹记忆 | 权能分离 | capability is not authority |
| v2.1.0 | shared skill fabric | 星图记忆 | 星域记忆 | 技能结构化与角色/能力图谱 | skill availability is not permission |
| v2.2.0 | local archive import simulation | 星海记忆前置 | 星穹记忆 | 外部能力进入隔离沙盘 | import is not trust |
| v2.3.0 | release integrity audit | 星穹记忆 | 星律记忆 | 版本治理与审计 | tag is a governance seal |
| v2.4.0 | governed proposal pack dry run | 星辰记忆 | 星穹记忆 | 候选记忆提案材料化 | proposal is not write |
| v2.5.0 | governed proposal review gate dry run | 星穹记忆 | 星律记忆 | 评审闸门 | review is not execution permission |
| v2.6.0 | governed approval request dry run | 星穹记忆 | 星律记忆 | 批准请求边界 | approval request is not authorization |
| v2.7.0 | read-only OpenClaw audit review | 星穹记忆 | 星界记忆前置 | 执行面只读观察 | observation is not execution |
| v2.8.0 | OpenClaw audit review smoke validation | 星界记忆前置 | 星穹记忆 | 最小治理闭环开始被验证 | validation is not authorization |
| v2.9.0 | closed-loop evidence validation | 星界记忆入口 | 星海记忆、星穹记忆、星律记忆 | 跨系统闭环证据可验证 | evidence validation is not authorization |

## 3. 当前阶段判断

v2.9.0 之后的当前位置：

- 主定位：星界记忆入口。
- 已具备：星辰、星域、星穹基础。
- 正在形成：星海到星界之间的协同证据结构。
- 未达到：星枢、星律成熟体、星魂、星宙、星源。

需要精确区分：星律已经有早期边界规则，但不是成熟的自执行记忆法律。星枢尚
未作为真实调度中心启动。星源没有达成。

## 4. v2.10 允许方向

v2.10 不应直接跳向执行。合理的下一步方向是：

closed-loop evidence -> governed memory proposal

这表示从星界记忆入口回到星辰、星域、星穹，形成受治理的记忆提案创建流程：
先把闭环证据材料化为候选记忆，限定项目、角色和场景范围，再进入审计和评审
边界。

该方向不得直接写入 durable memory，不得新增记忆写入能力，不得把证据验证、
提案创建、评审通过或审计结果解释为授权。
