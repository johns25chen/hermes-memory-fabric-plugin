# 文明之核：亚空间记忆系统校准

状态：v2.8-pre 治理校准文档
范围：Hermes Memory Fabric、Codex CLI、OpenClaw、GitHub、人类操作者
目标：将当前工程重新对齐到长期目标“Civilization Core - Subspace Memory System”

## 1. 文明之核总目标

本项目不应被理解为单一的 Hermes 插件、OpenClaw 工具、Codex 工作流，或一组
离散脚本。它的长期目标是构建“文明之核”的治理内核：围绕记忆、证据、执行隔
离、审计责任链和多智能体协作建立可验证、可回滚、可追责的基础秩序。

该内核的核心职责不是让系统更快地自动行动，而是让系统在面对长期记忆、跨工
具协作、审批请求、执行能力和版本发布时，始终保持边界清晰：

- 记忆必须有来源、证据、适用范围和治理状态。
- 审计必须记录事实、风险和责任链，但不能自行变成授权。
- 执行必须与观察、分析、审批请求和审批记录隔离。
- 多智能体协作必须通过明确角色、最小权限和可复核交接完成。
- 版本、PR、标签和回滚链必须成为治理事实的一部分，而不是发布后的附属品。

因此，本仓库承载的是长期治理内核的一个实现面。它当前仍处于分阶段验证过程
中，不能被宣称为完整闭环系统。

## 2. 亚空间记忆系统定义

“亚空间记忆系统”是文明之核中的受治理记忆层。它不是普通缓存、聊天历史或
RAG 索引，而是面向长期协作和高风险演进的证据化记忆结构。

亚空间记忆必须具备以下性质：

- 证据绑定：记忆条目必须能够追溯到文档、操作、审计、提案、代码变更或人工
  决策等来源。
- 来源链：记忆不能只保存结论，还应保存可复核的 provenance、时间、范围和生
  成路径。
- 风险边界：记忆读取、写入、审批、执行、外部暴露必须分属不同治理边界。
- 评审闸门：长期记忆写入、策略变化、执行授权和跨系统暴露必须经过显式评审
  或提案流程。
- 批准边界：批准请求、批准意图、批准记录和可执行批准令牌必须严格区分。
- 版本历史：关键治理状态应能映射到 GitHub PR、提交、标签、回滚点和发布封印。
- 可审计性：系统应记录可复核的操作事实，同时避免把敏感 stdout、令牌、审批
  短语或执行尾部内容暴露给评审工具。

该系统的目标不是消除人工判断，而是让人工判断发生在有证据、有边界、有历史
和有责任链的结构中。

## 3. 组件职责边界

### Hermes Memory Fabric

Hermes Memory Fabric 是记忆治理大脑。它负责证据、候选记忆、提案、评审、审
批请求和审计状态的组织与表达。它可以帮助系统识别哪些内容值得进入长期治理
流程，但不得绕过治理闸门直接把历史上下文变成 durable memory、图谱写入、执
行授权或配置变更。

### Codex CLI

Codex CLI 是代码和文档实现代理。它读取仓库、理解局部约束、应用最小必要变
更，并执行可复核验证。Codex 可以创建文档、修改代码、运行测试和总结结果，
但它不拥有最终合并、发布、标签或现实世界执行权限。

### OpenClaw

OpenClaw 是执行之手。它可以承载终端、自动化、外部工具和实际操作能力，但必
须始终受治理边界约束。即使某个审计、提案或审批请求被标记为通过，OpenClaw
也不能仅因“已有通过记录”而自动执行。执行需要独立、明确、当前有效的授权。

### GitHub

GitHub 是版本链、PR、标签、回滚和发布封印。它把治理成果固定为可比较、可回
溯、可复核的版本事实。PR 和 tag 不能只是工程协作工具，也应作为文明之核治
理阶段的版本锚点。

### Human Operator

人类操作者是合并、标签和现实世界执行的最终权威。系统可以提供证据、建议、
审计结果、候选提案和风险说明，但最终授权必须由人类操作者在清楚边界和后果
的前提下给出。

## 4. 借鉴同类系统的精髓与文明之核增强

| 同类系统常见思想 | 可借鉴精髓 | 文明之核增强 |
| --- | --- | --- |
| memory / RAG | 通过检索提升上下文连续性 | 证据支持的受治理记忆；读取不等于写入，召回不等于采纳 |
| tool calling | 让模型调用外部能力 | 能力不是权限；工具可用不代表当前任务可使用 |
| workflow automation | 把重复流程自动化 | 执行必须受审批闸门和最小权限约束 |
| logs | 记录系统行为 | 建立审计责任链；日志事实不能自动升级为授权事实 |
| dry-run | 在无副作用环境中预演 | 安全沙箱；dry-run 通过不代表现实世界许可 |
| release tag | 标记版本点 | 版本封印；将治理状态、回滚点和发布边界固定到版本链 |
| agent collaboration | 多角色协作完成复杂任务 | 角色边界、交接证据和执行隔离必须可审计 |
| approval flow | 引入人工批准 | 批准请求、批准意图、批准记录和批准令牌分层隔离 |

文明之核不是简单复制这些机制，而是把它们纳入同一套边界模型：证据先于结论，
授权独立于能力，执行晚于审计，版本封印高于临时状态。

## 5. v2.0-v2.7 阶段校准

| 版本阶段 | 技术交付物 | 文明之核层级 | 借鉴精髓 | 强化的治理原则 | 剩余缺口 |
| --- | --- | --- | --- | --- | --- |
| v2.0 token authority boundary contract dry run | 令牌权限边界契约 dry-run | 授权边界层 | capability / token contract | 授权材料必须与执行能力分离 | 尚未形成真实批准令牌闭环 |
| v2.1 shared skill fabric | 共享技能织物文档和边界 | 多智能体协作层 | shared skills / reusable workflow | 技能共享必须保留职责和来源边界 | 技能调用与治理状态尚未完整联动 |
| v2.2 local archive import simulation | 本地归档导入模拟 | 证据摄取层 | archive import / migration | 导入先模拟，不能直接污染长期记忆 | 真实大规模导入仍需治理闸门验证 |
| v2.3 release integrity audit | 发布完整性审计 | 版本封印层 | release audit / integrity check | 发布状态必须可复核、可回滚、可封印 | 审计通过仍不等于自动发布授权 |
| v2.4 governed proposal pack dry run | 受治理提案包 dry-run | 记忆提案层 | proposal packaging | 候选记忆必须打包、标识、可评审 | 提案包仍未进入真实写入审批闭环 |
| v2.5 governed proposal review gate dry run | 提案评审闸门 dry-run | 评审闸门层 | review gate | 评审决策必须结构化且可阻断 | review 结果不能自动生成执行许可 |
| v2.6 governed approval request dry run | 审批请求信封 dry-run | 审批请求层 | approval workflow | 审批请求不是批准令牌 | 尚未验证批准令牌签发与执行隔离 |
| v2.7 read-only OpenClaw audit review | 只读 OpenClaw 审计观察窗口 | 执行观察层 | executor audit / read-only monitor | 观察执行面不能触发执行面 | Hermes + Codex CLI + OpenClaw 最小闭环仍未完成验证 |

这些阶段已经建立了从权限边界、技能协作、归档模拟、发布审计、提案包、评审
闸门、审批请求到只读执行观察的连续治理骨架。但它们仍主要是 dry-run、只读
或静态审计性质，不能被解释为完整的生产级自治系统。

### v2.8-pre-2 阶段补章

阶段 0、阶段 1 以及 v2.0-v2.7 的逐项治理缺口补齐，见
[`CIVILIZATION_CORE_STAGE_SUPPLEMENTS_V2_0_TO_V2_7.md`](CIVILIZATION_CORE_STAGE_SUPPLEMENTS_V2_0_TO_V2_7.md)。
该补章只补充阶段性治理边界，不新增能力、不改变标签、不宣称系统完成。

### v2.8.0 最小治理闭环契约

v2.8.0 的最小闭环验证契约见
[`CIVILIZATION_CORE_MINIMUM_CLOSED_LOOP_V2_8.md`](CIVILIZATION_CORE_MINIMUM_CLOSED_LOOP_V2_8.md)。
该契约只定义 natural language task -> Codex CLI implementation -> terminal /
OpenClaw validation -> ChatGPT review -> GitHub PR / tag 的治理交接边界，不新增
自动执行能力，不改变既有版本标签，也不宣称文明之核系统完成。

## 6. 不可破坏原则

- observation is not execution
- audit is not authorization
- memory recall is not memory write
- approval request is not approval token
- dry-run pass is not real-world permission
- tool availability is not tool permission
- approved audit records must not trigger execution
- approval_phrase, stdout_tail, and stdout must not be exposed by review tools

这些规则是当前阶段的硬约束。任何未来功能、自动化、代理协作或审批扩展，都
不得削弱这些边界。

## 7. 当前阶段定位

v2.7 已完成只读 OpenClaw 审计观察窗口，证明系统可以把执行面作为被观察对象
纳入治理视野，并强调审计、stdout、审批短语和执行尾部内容的敏感边界。

但是，Hermes + Codex CLI + OpenClaw 的最小闭环尚未被完整验证。当前已经证明
的是若干治理构件的存在、dry-run 行为、只读审计能力和阶段性版本封印；尚未
证明的是自然语言任务从记忆治理、代码实现、终端验证、审查复核到 GitHub 版
本封印之间的完整、最小、受控闭环。

因此，当前阶段应被定位为“闭环前的治理校准完成”，而不是“闭环系统完成”。

## 8. v2.8-pre 与 v2.8 方向

v2.8-pre 定义为本文档本身：一次面向“Civilization Core - Subspace Memory
System”的目标校准。它不修改代码、不改变测试、不调整 `pyproject.toml`、不
移动既有 release tag，只把项目宪章、边界模型和下一步方向固定为仓库内的明
确治理文本。

v2.8.0 的方向是最小闭环验证：

1. natural language task：由人类操作者给出自然语言任务和边界。
2. Codex CLI implementation：Codex CLI 在仓库内执行最小必要实现或文档变更。
3. terminal / OpenClaw validation：通过终端或 OpenClaw 执行受控、可复核、无
   越权的验证。
4. ChatGPT review：由 ChatGPT 对结果、风险、边界和证据进行复核。
5. GitHub PR / tag：由 GitHub 承载 PR、合并决策、标签和版本封印。

v2.8.0 的目标不是扩大自动化权限，而是验证最小可行治理闭环是否成立。只有当
每个环节都能证明“证据可追溯、权限不外溢、执行不自触发、版本可回滚、人类
仍为最终权威”时，文明之核的亚空间记忆系统才进入下一阶段建设。
