# 文明之核：v2.8.0 最小治理闭环契约

状态：v2.8.0 最小治理闭环契约
范围：Civilization Core - Subspace Memory System
性质：设计契约；不新增执行能力；不声明系统完成

本文定义 v2.8.0 对以下链路的最小受治理闭环验证：

natural language task
-> Codex CLI implementation
-> terminal / OpenClaw validation
-> ChatGPT review
-> GitHub PR / tag

该契约的目的不是提高自动化权力，而是证明治理交接是否成立：自然语言任务能
否在边界清晰、证据可复核、执行受控、最终权威仍由人类保留的条件下，完成从
实现、验证、复核到版本记录的最小闭环。

## 1. v2.8.0 阶段定位

v2.8.0 位于以下阶段之后：

- v2.7 read-only OpenClaw audit review
- v2.8-pre Civilization Core alignment document
- v2.8-pre-2 stage governance supplements

这些前置阶段已经建立只读审计、阶段校准、治理补章和边界原则，但仍不能证明
完整闭环已经成立。v2.8.0 必须先验证最小闭环，再考虑更强的协调或自动化。

因此，v2.8.0 的阶段定位是“最小治理闭环验证”，不是“自治执行升级”，也不是
“Civilization Core 完成”。它只验证各组件能否按受限职责完成一次可追溯交接。

## 2. 最小治理闭环定义

v2.8.0 的闭环必须严格按以下顺序成立：

1. Human Operator 给出自然语言任务和边界。
2. ChatGPT 将任务转化为受限任务简报，明确范围、禁止项和验证要求。
3. Codex CLI 读取仓库上下文，并应用最小必要实现或文档变更。
4. Terminal / OpenClaw 只执行受控验证。
5. ChatGPT 复核 diff、测试输出、风险和治理边界合规性。
6. Human Operator 决定 PR 合并和 tag。
7. GitHub 记录版本链、PR、commit 和 tag。

闭环中的每一步都只能产生证据或交接，不能把上一环节的通过状态自动升级为下
一环节的授权。

## 3. 组件职责边界

| 组件 | 允许角色 | 禁止角色 | 产生证据 | 交接对象 |
| --- | --- | --- | --- | --- |
| Human Operator | 给出任务边界；决定合并、发布和现实世界执行 | 将最终授权委托给自动系统；在未复核证据时创建 release tag | 自然语言任务、明确批准、合并或标签决策 | ChatGPT、GitHub |
| ChatGPT | 转换任务简报；协调复核；审查 diff、测试输出、风险和边界 | 取代人类最终权威；直接声明系统完成；把审计记录当作执行授权 | 任务简报、复核结论、风险说明、边界合规说明 | Codex CLI、Human Operator |
| Hermes Memory Fabric | 召回和组织上下文；提供证据化历史线索 | 将 recall 视为 durable memory；绕过治理写入长期记忆；触发执行 | 召回摘要、来源线索、治理状态提示 | ChatGPT、Codex CLI |
| Codex CLI | 读取仓库；执行最小实现或文档变更；总结变更文件 | 合并 PR；创建或改写 tag；发布版本；越界修改无关文件 | 文件变更、diff、验证摘要、git status 结果 | Terminal / OpenClaw、ChatGPT |
| Terminal / OpenClaw | 运行受控验证；执行 tests、grep、diff、status、smoke scripts | 仅因 audit record 已批准而执行；执行现实世界动作；泄露敏感输出 | 测试结果、smoke 结果、diff/status 证据、摘要化输出 | ChatGPT |
| GitHub | 记录 PR、commit、版本链和 tag | 在 release tag 后重写历史；替代人类发布判断；隐式批准变更 | PR、commit、merge 记录、tag、release 边界 | Human Operator、项目历史 |

硬性原则如下：

- Human Operator 保留最终权威。
- ChatGPT 负责复核和协调，但不拥有最终权威。
- Hermes 召回和组织上下文，但 recall 不是 durable memory。
- Codex CLI 实施最小变更，但不能 merge、tag 或 release。
- OpenClaw / terminal 在控制下验证，但不能仅因 approved audit records 自动执行。
- GitHub 记录治理事实，但 release tag 之后不得重写历史。

## 4. 允许动作

v2.8.0 可以执行以下动作：

- 创建小型、可测试的文档或代码变更。
- 要求 Codex CLI 执行实际 implementation。
- 运行本地 tests 或 smoke checks。
- 检查 `git diff` 和 `git status`。
- 创建 PR。
- 仅由 Human Operator 合并。
- 仅在 main 已确认 clean 且版本正确后创建 tag。

这些动作必须服务于最小闭环证明，不能被解释为一般化自动执行授权。

## 5. 禁止动作

v2.8.0 必须禁止以下动作：

- 不允许 autonomous OpenClaw execution。
- 未经治理批准，不允许 memory write。
- 不允许把 audit review 作为 execution trigger。
- 不允许 review tools 暴露 `approval_phrase`、`stdout_tail` 或 `stdout`。
- 不允许 tag rewriting。
- 除非确实发布 v2.8.0，不允许修改 `pyproject.toml` 版本号。
- documentation-only 阶段不允许隐藏代码变更。
- 不允许宣称完整 Civilization Core system 已完成。

这些禁止项是闭环验证的边界，不是实现建议。

## 6. Codex CLI 参与验证标准

证明 Codex CLI 实际参与，至少需要以下证据：

- 任务以自然语言交给 Codex CLI。
- Codex 检查仓库上下文，而不是脱离仓库直接生成结果。
- Codex 修改文件。
- Codex 总结被修改的文件。
- terminal `git status` 确认被修改文件。
- ChatGPT 复核结果，而不是直接写入这些文件。

如果实现文件由 ChatGPT 绕过 Codex CLI 直接写入，则该闭环验证失败。

## 7. OpenClaw / Terminal 验证边界

OpenClaw / terminal 在 v2.8.0 中只承担受控验证角色：

- validation 可以运行 tests、grep、diff、status 和 smoke scripts。
- validation 不得执行现实世界动作。
- validation 不得把 approved audit records 当作 commands。
- validation outputs 是 evidence，不是 authorization。
- `stdout` 和 `stdout_tail` 可能包含敏感内容；相关信息只能在必要时谨慎摘要。

验证通过只能说明当前证据满足检查条件，不能自动产生合并、标签、发布或执行
授权。

## 8. 成功标准

v2.8.0 只有在以下条件同时满足时才算成功：

- 任务从自然语言开始。
- Codex CLI 执行实际 implementation。
- validation 受控且可复现。
- ChatGPT 复核 diff 和 test evidence。
- Human Operator 批准 merge。
- GitHub 记录 PR 和 commit。
- release tag 仅在版本被有意发布时创建。
- 治理边界没有被削弱。

成功含义仅限于最小闭环被证明，不代表完整 Civilization Core system 已完成。

## 9. 失败条件

出现以下任一情况，即视为 v2.8.0 闭环验证失败：

- ChatGPT 直接写入 implementation，而不是由 Codex CLI 执行。
- OpenClaw 从 audit approval 触发执行。
- Hermes recall 被当作 durable memory。
- Codex CLI 修改任务范围之外的文件。
- documentation-only 工作中修改 `pyproject.toml`。
- review output 泄露 `approval_phrase`、`stdout_tail` 或 `stdout`。
- main 未合并且 clean 前创建 tag。
- 未有证据即宣称系统完成。

失败条件应被记录为治理证据，并用于后续修正边界或流程，而不是被忽略。

## 10. v2.8.0 后续方向

在最小闭环被证明之后，后续版本可以考虑更强的协调能力，但必须先满足以下条
件：

- governance evidence 已被记录。
- role boundaries 可测试。
- release integrity 能验证新阶段。
- 没有 read-only boundary 被削弱。

任何后续增强都必须继续区分设计契约、实现能力、验证证据和授权事实。v2.8.0
只建立最低闭环契约，不授予 OpenClaw 自动执行权，不把 Hermes recall 升级为
durable memory，也不赋予 Codex CLI merge、tag 或 release 权限。
