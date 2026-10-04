# Agent 技术审计总报告

日期：2026-10-04 UTC。审计范围见 [AUDIT_PLAN.md](AUDIT_PLAN.md)。这是同一工作区中的自动化审计与新构建复现，不是独立人类复现。

**结论：E1/E2 的核心执行证据经原始产物重算和新构建后仍成立；论文需要收紧一处 E5 实现范围表述。基线对照未显示 E5 在五个核心条件上有额外检出能力。** 四篇指定全文已完成比较，但新颖性、独立类序参考与人工审核仍未确立。

## 逐项结论

| 审计项 | 状态 | 依据与实际范围 |
|---|---|---|
| 旧证据完整性 | PASS | 审计前后，旧扩展清单 2,191 项、历史两份清单 691/188 项及原稿修订目录 34 项均匹配；这些清单有重叠，不合计为独立样本数。 |
| 图/权重、metadata、标签资源与打包身份 | PASS | 独立脚本直接解析原始文件；五种模型字节条件中 165 个非 metadata buffers 一致。标签干预保持嵌入 metadata 和 pre-ZIP 前缀；描述控制例外地改变一个 metadata 字节。 |
| 历史 E1/E2 数值与关联 | PASS | 重算 32 份历史 raw 观测和 28 份成功类别列表；分数位、标签位置、999 个变化与两类恢复均符合主张。不是新执行次数或独立模型数。 |
| 实际 getter 与观测无突变 | PASS | 检查实际 APK DEX、生成类与库方法。`getBuffer()` 不重置原 buffer；观测只读取 duplicate，实际 getter 调用真实 TensorLabel。 |
| 新目录/新 AVD 的生成、构建和运行 | PASS | 8 条阶段/变体执行记录，去重为 5 个 artifact×consumer 配置、1 个图；共 16 次输入观测。复用已安装的固定 Python/JDK/SDK。 |
| 官方入口、简单基线与 E5 | PASS，未建立检测增量 | 五个核心条件中，简单 decoder 基线、E5 和 Task 初始化均只拒绝标签删除。读取与填充入口接受五个条件。 |
| E3/E4/E5 分母与 Hand 证据 | PASS | 从逐项记录重算；Hand 源码所绑定组件与焦点组件不同，通过重新核验的图/权重桥建立联系。保留 E3 跨平台、E4 无运行及 Hand 单图边界。 |
| E5 未识别路径的自动弃权保证 | FAIL：文字须收紧 | 正则模板匹配不能保证识别所有未知 getter/processor 语法。未发现当前已测 fixture 的结果因此错误。 |
| 四篇指定相关工作全文核对 | PASS，有界比较 | MLGuard、DocTer、ACETest、DARA 的具体版本、全文、来源、页/节定位已保存。不构成穷尽新颖性证明。 |
| 独立类序参考、人类核验 | UNVERIFIABLE / PENDING | 本轮没有取得或完成，不能升级 E2 为已证明的错误预测，也不能勾选人工审核。 |

## 新执行的关键结果

以下是新生成源码、新编译/打包 APK、新 AVD 上的数据，不是再次运行旧 APK。E1/E2 的共享原版、描述控制和恢复文件有相同字节，不能重复计为独立模型。

| 条件 | 加载 | 推理 | 实际生成 getter | 与原版的关系 |
|---|---|---|---|---|
| 原版 | 成功 | 成功 | 返回 1,000 类别 | 基准 |
| 描述控制 | 成功 | 成功 | 返回 1,000 类别 | raw 和解码结果相同 |
| 标签删除 | 成功 | 成功 | 两个输入均抛出捕获的异常 | raw 与原版相同 |
| 标签置换 | 成功 | 成功 | 返回 1,000 类别 | 所有分数位相同，999 个标签字符串改变 |
| 标签恢复／逆置换恢复 | 成功 | 成功 | 返回 1,000 类别 | raw 和解码结果恢复 |

删除的确切异常仍为 `IllegalArgumentException: Label number 999 mismatch the shape on axis 1`，调用栈包含 `ContractModel$Outputs.getProbabilityAsCategoryList`。异常由 harness 捕获，不是应用崩溃证据。

置换时，RGB 输入的输出位置 904 保持分数 `0.23542051017284393`，标签从 `window screen` 变为 `window shade`。每个输入仍有 999 处标签字符串变化；重复的 `maillot` 解释了唯一不变字符串。新记录的全部 raw、成功 decoded 数据与相应历史记录一致。

工作目录模型、APK 内 `assets/model.tflite` 与运行时 AssetManager 读取的哈希一致。这个新增观测在 generated `newInstance` 前，用相同 Context 和同一 asset 名读取；它不拦截 native interpreter 内存。新增代码仅在 harness，生成 Java 未改。新生成类字节与历史类一致；本轮各变体 DEX 一致。由于新增 harness，本轮完整 DEX 不声称与历史 DEX 相同。

根审计另写 [verify_completed_audit.py](verify_completed_audit.py)，从实际 APK、模型、生成类、设备 JSON、RGB/raw/decoded 文件重新检查，而非仅接受重建汇总。结果见 [fresh-runtime-crosscheck.json](verification/fresh-runtime-crosscheck.json)。

## 基线对照对贡献定位的影响

五个核心条件的新对照共用精确模型字节。合理简单基线按所选 TensorLabel 重载的真实选轴、标签解析及返回形式条件判断；实际使用的 Support API jar 也进行了反汇编核对。

- E5 相比该简单基线：新增拒绝条件 **0**。
- E5 相比官方 Task 初始化：新增拒绝条件 **0**。
- E5 比 metadata 读取/填充多指出标签删除的 decoder 不兼容；这反映工具范围不同，不能写成官方没有相关检查。
- 独立列出的既有结构负控是“1 个图输出、0 个 output-metadata 条目”，标签仍为 1,000。读取工具可读，Populator 在 `load_metadata_buffer → _validate_metadata` 拒绝，未到 `populate`。

因此，当前 E5 继续作为提前诊断、定位所选路径的支撑工具。此组结果没有确立独立检测方法创新，也不证明未来在其他配置上没有增量。

## 必须处理的稿件事项

1. **收紧 E5 实现范围。** 原稿 L54–58/L195 应明确有限模板/正则关联。未知 getter 可能落入 `INAPPLICABLE`，未识别的 processor 写法可能绕过操作匹配；不能承诺所有未知情况都会正确弃权。
2. **加入本轮基线结果。** 如实呈现零新增检出，避免把既有标签数量约束当作新规则。
3. **补入直接相关工作。** MLGuard 是契约 wrapper 愿景；DocTer 和 ACETest 已实现约束提取与测试；DARA 比较模型架构与 metadata。四篇内未展示完整焦点关联链，不等于已经证明本研究的方法新颖性。
4. **加入新的重建证据及限定。** 说明新输出目录、新 AVD、复用安装工具链、harness 资产观测和代码比较范围。

可直接用于下一轮修订的文字见 [MANUSCRIPT_IMPACT.md](MANUSCRIPT_IMPACT.md)。本轮没有改写封存稿件。

## 阴性结果与保留边界

- 历史 logcat 是累计记录，成功条件的日志也可能含早先删除条件的异常；必须结合时间窗口与逐次设备记录归属。
- 历史 E2 初次 restoration replay 没有完整结果，仍未分类；单独 recovery 记录提供完成结果。审计不补写那次缺失执行。
- 恢复是标签 payload 和观察行为恢复，原始 ZIP 整文件字节并未恢复。
- E3 仍是 Android generated Java 对 Linux Task；本轮 Task 对照只新运行初始化，没有做同 Android Task 比较或新的 Task classify。
- E4 没有增加外部运行；现有静态不兼容不能重新计为自然端到端缺陷。
- Hand 的八份保存 decoded 记录得到重新核验，没有重跑 Hand 推理，也不推广到所有输入。
- 没有新增模型集合、自然缺陷搜索、独立 class-order oracle、独立操作者/环境复现或人类审核。

## 证据入口

- [原始产物审计](preservation/AUDIT_REPORT.md)及[实际字节码审计](preservation/bytecode/report.md)
- [新构建与运行审计](rebuild/AUDIT_REPORT.md)
- [官方与简单基线对照](baseline/RESULTS.md)
- [逐项稿件审计](claims/AUDIT_REPORT.md)
- [四篇全文比较](literature/AUDIT_REPORT.md)
- [机器记录索引](results.json)、[TODO 更新快照](TODO.after.md)

`SHA256SUMS` 覆盖本轮报告、脚本和产物；可用 `bash commands.sh verify` 只读核验。其范围不包括安装/可写 AVD 状态，具体见 README。当前工作仍依赖已有保存工具链和证据目录，不是完整独立的离线发布包。
