# 文明之核：项目跑偏审计与纠偏记录

状态：v2.10-pre 框架纠偏文档
范围：v2.0 至 v2.9 工程叙事、十五层记忆、亚空间记忆系统
性质：只读审计与纠偏记录；不新增能力、不改变 release tag、不写入 durable memory

## 1. 审计结论

v2.0 到 v2.9 的工程链条是有价值的。它逐步建立了权限边界、技能织物、归档
导入模拟、发布完整性审计、受治理提案、评审闸门、审批请求、只读执行观察、
最小闭环验证和 closed-loop evidence validation。

但是，项目叙事多次发生跑偏。根本原因是更高层的文明之核框架和十五层记忆体
系没有被持续强制执行，导致局部工程交付物一度替代了最高坐标系。

## 2. 跑偏点列表

### 把文明之核降级成 Hermes 插件

- 表现：把仓库、工具和文档叙事主要描述为 Hermes Memory Fabric 插件能力。
- 为什么错：Hermes 是记忆治理组件，不是文明之核本体。
- 纠正方式：明确文明之核是总系统，Hermes 只是亚空间记忆系统的工程组件之一。
- 后续防复发规则：任何版本说明必须先写文明之核总目标，再写 Hermes 组件职责。

### 把项目降级成 Codex / OpenClaw / GitHub 工作流

- 表现：把 Codex 实现、OpenClaw 验证、GitHub PR 或 tag 当作项目核心叙事。
- 为什么错：这些是协作、执行观察和版本封印组件，不是最高治理框架。
- 纠正方式：把它们重新放回组件职责边界，服从十五层记忆和文明之核目标。
- 后续防复发规则：任何流程图或阶段说明都必须区分核心、载体、组件和封印。

### 忘记或弱化十五层记忆体系

- 表现：阶段文档讨论了治理边界，但没有持续引用十五层记忆作为最高坐标。
- 为什么错：没有十五层记忆，工程阶段容易只按工具能力或 PR 顺序推进。
- 纠正方式：正式新增十五层记忆总框架文档，并要求未来版本映射回主层级。
- 后续防复发规则：每个版本必须声明主记忆层级和支撑记忆层级。

### 用工程治理分层替代十五层记忆层级

- 表现：把权限、审计、提案、审批、执行观察等工程治理层当作记忆等级。
- 为什么错：工程层是实现维度，十五层记忆是文明之核最高记忆等级体系。
- 纠正方式：保留工程治理层，但把它们映射到十五层记忆，而不是替代十五层记忆。
- 后续防复发规则：任何新增工程层都必须说明其服务的十五层记忆位置。

### v2.7 功能成功但没有真正使用 Codex CLI 完成实现

- 表现：v2.7 的只读 OpenClaw 审计能力成立，但实现过程没有严格完成 Codex CLI
  参与链路。
- 为什么错：阶段目标涉及 Codex CLI 与执行观察面的最小闭环时，绕过 Codex CLI
  会削弱证据链完整性。
- 纠正方式：后续阶段补充 Codex CLI 参与、终端或 OpenClaw 验证、ChatGPT 复核
  与版本封印之间的治理交接。
- 后续防复发规则：若阶段声明需要 Codex CLI，就必须留下 Codex CLI 参与证据。

### v2.8-pre 总纲完成后差点直接推进功能，未先补阶段缺口

- 表现：完成总纲后，推进方向一度转向新功能，而不是先补 v2.0 至 v2.7 的阶段
  治理缺口。
- 为什么错：未补缺口会让后续功能建立在不完整的治理链上。
- 纠正方式：先补阶段治理文档和最小闭环契约，再推进 v2.8 和 v2.9 验证。
- 后续防复发规则：进入新能力前，必须审计上一阶段剩余缺口。

### v2.8 / v2.9 没有第一时间映射回星界记忆

- 表现：v2.8 和 v2.9 已经开始跨系统闭环证据验证，但叙事未立即回扣星界记忆。
- 为什么错：跨系统、跨边界协同记忆应被识别为星界记忆入口，而不是普通闭环工程。
- 纠正方式：新增版本到十五层记忆映射表，把 v2.8 和 v2.9 明确定位到星界记忆前置
  与星界记忆入口。
- 后续防复发规则：每次闭环、跨系统或多组件验证都必须判断是否推进星界记忆。

### 没有把十五层记忆正式写入仓库作为最高罗盘

- 表现：十五层记忆存在为项目上位概念，但没有作为仓库内固定文档被引用。
- 为什么错：未入库的最高框架无法稳定约束版本叙事和工程推进。
- 纠正方式：新增十五层记忆总框架、跑偏审计、版本映射表，并在既有校准文档中
  添加交叉引用。
- 后续防复发规则：未来所有文明之核文档必须优先引用十五层记忆总框架。

## 3. 已纠正内容

- #26 Civilization Core alignment document：建立文明之核与亚空间记忆系统的总
  体校准文本。
- #27 stage governance supplements：补充 v2.0 至 v2.7 阶段治理缺口。
- #28 minimum closed-loop contract：定义 v2.8 最小治理闭环契约。
- #29 v2.8 OpenClaw audit review smoke validation：验证 OpenClaw 审计观察的最
  小闭环烟测。
- #30 v2.9 closed-loop evidence validation：验证跨系统闭环证据可复核。

以上编号仅作为项目历史标签使用，不在本文中发明或绑定 URL。

## 4. 本次补齐的纠偏项

- Fifteen Memory Layers must be formally pinned。
- Version-to-memory-layer mapping must be maintained。
- Future tasks must start with layer mapping。

这些项目是 v2.10-pre 框架纠偏必须补齐的内容。完成文档固定后，仍不得宣称文
明之核系统完成。

## 5. 后续强制自检

- Does this step belong to Civilization Core?
- Which Fifteen Memory Layer does it advance?
- Is it evidence, memory, audit, execution, or authorization?
- Does it confuse recall with memory write?
- Does it confuse audit with authorization?
- Does it confuse observation with execution?
- Does it bypass Codex CLI when Codex participation is required?
- Does it bypass Human Operator final authority?
- Does it alter released tags?
