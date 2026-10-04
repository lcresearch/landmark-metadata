#!/usr/bin/env python3
"""Apply completed audit statuses without checking off any human review."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
assert json.loads((ROOT/'verification/fresh-runtime-crosscheck.json').read_text())['status'] == 'PASS'
assert (ROOT/'AUDIT_REPORT.md').exists()
target = pathlib.Path('/workspace/metadata-contract-next/TODO.md')
s = target.read_text()
def replace(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
replace('本次仅更新工作清单，没有启动新实验。', '本轮已完成 agent 技术审计、使用既有工具链的新目录/新 AVD 重建、官方基线对照及指定四篇全文比较。独立人工核验仍未完成。')
replace('- [ ] E1/E2 从保存输入开始的下一轮干净构建复现及加载资产审计。已有初次构建和同 APK replay 不替代此项。', '- [x] E1/E2 从保存输入重新生成、编译、打包并在新 AVD 执行；加入同资产加载前哈希。复用已安装的固定工具链，不是从工具链归档全新安装或独立人类复现。\n- [x] 原始 E1/E2 的独立脚本重算和实际 APK 字节码审计；E3/E4/E5 分母与 Hand 源码/图桥核验。\n- [x] 五个核心文件条件的官方入口、合理简单基线与 E5 对照；E5 相对简单基线/Task 初始化未增加检出。\n- [x] MLGuard、DocTer、ACETest、DARA 指定版本全文核对；不是穷尽新颖性证明。')
replace('状态依据：', '本轮审计：[总报告](../metadata-contract-audit-20261004T062010Z/AUDIT_REPORT.md)、[机器记录](../metadata-contract-audit-20261004T062010Z/results.json)、[稿件修改建议](../metadata-contract-audit-20261004T062010Z/MANUSCRIPT_IMPACT.md)。\n\n状态依据：')
replace('| P0 | E1/E2 最小干净重建与证据审计 | 核心断言重新计算通过，或逐项记录失败／无法验证及其影响 | 待开始 |', '| P0 | E1/E2 最小干净重建与证据审计 | 核心断言重新计算通过，或逐项记录失败／无法验证及其影响 | agent 审计完成；同安装工具链、新输出目录/AVD |')
replace('| P1-A | 官方入口、合理简单基线、既有 E5 对照 | 明确检查范围、实际结果、检测阶段和 E5 的增量 | 待开始 |', '| P1-A | 官方入口、合理简单基线、既有 E5 对照 | 明确检查范围、实际结果、检测阶段和 E5 的增量 | 完成：5 核心文件条件＋1 既有结构负控；无已证实检测增量 |')
replace('| P1-B | 最接近工作的全文核对，可与 P0 并行 | 技术边界对照表；不把摘要检索当成完整新颖性核查 | 待开始 |', '| P1-B | 最接近工作的全文核对 | 技术边界对照表；不把摘要检索当成完整新颖性核查 | 指定 4 篇完成；更广的技术定位仍待收敛 |')
replace('| 条件项 | 消费路径契约分析的小规模扩展 | 超越合理简单基线，并在未参与设计的结构上成立 | 尚未决定实施 |', '| 条件项 | 消费路径契约分析的小规模扩展 | 超越合理简单基线，并在未参与设计的结构上成立 | 未实施；当前对照不支持升级为方法贡献 |')
replace('| P4 | 对已有稿件定点收敛、人工审计与投稿准备 | 贡献与证据相符的完整稿件、最小复现包和明确审核状态 | 初稿已完成；收敛待做 |', '| P4 | 对已有稿件定点收敛、人工审计与投稿准备 | 贡献与证据相符的完整稿件、最小复现包和明确审核状态 | 初稿已完成；本轮发现的定点修改及人工审核待做 |')
# These groups have been completed within their stated audit scope.
start = s.index('## P0：')
end = s.index('## P2：')
part = s[start:end]
part = part.replace('- [ ]', '- [x]').replace('确認', '确认')
part = part.replace('- [x] 对 MLGuard、DocTer、ACETest、DARA 及相关变异/差分测试工作做全文级对照；不同研究目标的工具不计作无法检测本 fixture 的失败基线。', '- [x] 对 MLGuard、DocTer、ACETest、DARA 指定版本做全文级对照；不同研究目标的工具不计作无法检测本 fixture 的失败基线。\n- [ ] 视最终贡献范围补充变异/差分测试及跨工件契约的技术定位；本轮四篇比较不构成穷尽新颖性核查。')
s = s[:start] + part + s[end:]
replace('## P4：在已有初稿上收敛\n', '## P4：在已有初稿上收敛\n\n本轮审计要求先处理以下定点修改（原稿尚未改动）：\n\n- [ ] 收紧稿件 L54–58/L195：E5 是有限模板的正则关联，不能保证所有未知 getter/processor 语法都正确弃权；当前已测 fixture 结果未因此被推翻。\n- [ ] 加入官方入口／简单基线／E5 的对照表，说明当前五条件上 E5 无额外检出，继续定位为支撑工具。\n- [ ] 补入 MLGuard、DocTer、ACETest；明确 vision、实现及技术边界，不把约束提取本身作为新意。\n- [ ] 加入本轮新构建复现及资产身份链，同时披露 harness 哈希观测、复用安装工具链和新 DEX 的比较范围。\n')
replace('- 下一批实际任务：P0 + P1-A；P1-B 可并行。其余按前项结果推进。', '- 下一批实际任务：优先处理本轮审计提出的稿件定点修改，并进行 P2 同 Android 消费者对照；P3 按限定范围查证。P0/P1-A 不再从头重复，除非新增变更或矛盾需要复核。\n- 尚未完成：独立人工审计、同 Android Task 对照、artifact-tied 类序 oracle、限定自然案例查证、独立环境/操作者复现与公开最小复现包。本轮没有增加外部模型或自然缺陷发现。')
assert '- [ ] 独立人工审计。' in s
target.write_text(s)
(ROOT/'TODO.after.md').write_text(s)
print(target)
