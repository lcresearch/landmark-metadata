"""Record the completed editorial revision and update the working TODO once."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OLD = Path('/workspace/metadata-contract-paper-rewrite-20261004T052625Z')
AUDIT = Path('/workspace/metadata-contract-audit-20261004T062010Z')
TODO = Path('/workspace/metadata-contract-next/TODO.md')
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def write(name, value):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        f.write(value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False) + '\n')

# Regenerate only in a disposable directory, leaving the reviewed source intact.
with tempfile.TemporaryDirectory(prefix='manuscript-editor-check-') as td:
    temp = Path(td)
    (temp/'scripts').mkdir()
    (temp/'manuscript').mkdir()
    shutil.copytree(ROOT/'review', temp/'review')
    shutil.copy2(ROOT/'scripts/revise_manuscript.py', temp/'scripts/revise_manuscript.py')
    result = subprocess.run(['python', str(temp/'scripts/revise_manuscript.py')], text=True, capture_output=True, check=True)
    assert sha(temp/'manuscript/paper.tex') == sha(ROOT/'manuscript/paper.tex')
    assert (temp/'manuscript-changes.patch').read_bytes() == (ROOT/'manuscript-changes.patch').read_bytes()
    write('verification/editor-reproduction.json', {
        'status':'PASS', 'created_utc':NOW, 'method':'Run saved editor script in a disposable directory using the sealed prior source and saved proposals.',
        'source_sha256':sha(ROOT/'manuscript/paper.tex'), 'patch_sha256':sha(ROOT/'manuscript-changes.patch'),
        'source_byte_equal':True, 'patch_byte_equal':True, 'model_experiments_run':False,
    })

preserved = []
for base in [OLD, AUDIT]:
    manifest = base/'SHA256SUMS'
    count = 0
    for line in manifest.read_text().splitlines():
        digest, filename = line.split(maxsplit=1)
        filename = filename.lstrip('*')
        assert sha(base/filename) == digest, str(base/filename)
        count += 1
    preserved.append({'root':str(base), 'manifest_sha256':sha(manifest), 'verified_entries':count, 'status':'PASS'})
write('verification/preserved-packages.json', {'created_utc':NOW, 'packages':preserved, 'read_only_verification':True})

write('verification/visual-review.json', {
    'status':'PASS', 'created_utc':NOW, 'reviewer':'AI assistant', 'human_verification':False,
    'pdf_sha256':sha(ROOT/'manuscript/paper.pdf'), 'pages_inspected':list(range(1,9)),
    'method':'Inspect all eight rendered page PNGs at 100 dpi; LaTeX diagnostics independently checked.',
    'observations':'Tables, equations, references and text fit the generic two-column layout without visible clipping or overlap. Page 3 has an ordinary column continuation within the window shade witness phrase.',
    'venue_page_fit_claimed':False,
})
write('review/RESOLUTION.md', f'''# 交叉审读与采纳记录

三份交叉审读由 AI agents 完成，均不是人工核验。审读源文件 SHA-256 为 `bb289e96e311363ba92099e5a5fa357b5a8005aa321283be022a189cd2391b4d`。

- execution-final-review.txt：通过；执行计数、资产身份链和 DEX 比较范围得到保留。
- baseline-final-review.txt：通过；采纳建议，将简单基线的资源前提明确为 **a unique** TENSOR_AXIS_LABELS resource。
- literature-final-review.txt：通过；采纳建议，将区别限定为 **The four method papers examined in full**。

两处精确化之后，最终源文件 SHA-256 为 `{sha(ROOT/'manuscript/paper.tex')}`。三份原始审读报告仍对应审读时的版本；最终版本另通过自动化证据检查、编辑脚本重建检查及八页版面检查。
''')
write('verification/CHECK_NOTES.md', '''# 检查说明

首次最终证据检查在 PDF 文本抽取断言处停止：双栏阅读顺序将跨栏的 “window shade” 拆开，导致全文连续字符串检查失败。源文件及渲染页面中的内容正确，所有前置实验断言已通过。

检查器改为在 LaTeX 源码中核对完整短语，并在 PDF 抽取文本中核对对应词项；同时查看全部八页渲染结果。没有修改实验数据或稿件中的该见证。最终检查通过，见 revision-check.json。

这次编辑没有重新执行模型实验；稿件新增的 Android 重建和基线结果来自之前已封存的 agent 审计。人工核验仍未完成。
''')

todo = TODO.read_text()
assert todo == (ROOT/'TODO.before.md').read_text(), 'TODO changed during revision; reconcile before applying.'
todo = todo.replace('独立人工核验仍未完成。', '本轮审计结论已纳入新稿，并完成交叉审读、证据检查和八页通用版面检查。独立人工核验仍未完成。', 1)
todo = todo.replace('- [已完成的论文初稿](../metadata-contract-paper-rewrite-20261004T052625Z/manuscript/paper.pdf)', '- [当前审计修订稿](../metadata-contract-paper-revision-20261004T065132Z/manuscript/paper.pdf)')
todo = todo.replace('- [初稿修订状态](../metadata-contract-paper-rewrite-20261004T052625Z/REVISION_STATUS.json)', '- [本轮修订记录](../metadata-contract-paper-revision-20261004T065132Z/REVISION_NOTES.md)\n- [本轮修订状态](../metadata-contract-paper-revision-20261004T065132Z/REVISION_STATUS.json)')
todo = todo.replace('初稿已完成；本轮发现的定点修改及人工审核待做', '审计定点修订完成；人工审核、独立包与 venue 格式待做')
todo = todo.replace('本轮审计要求先处理以下定点修改（原稿尚未改动）：', '本轮审计提出的定点修改已在新版本完成；旧封存稿保持不变：')
for start in ['收紧稿件 L54–58/L195', '加入官方入口／简单基线／E5', '补入 MLGuard、DocTer、ACETest', '加入本轮新构建复现及资产身份链', '用三个问题组织主论证', 'E1/E2 合并呈现干预', 'S/I/D 分开', '清晰陈述已证明的正面结论']:
    assert '- [ ] '+start in todo, start
    todo = todo.replace('- [ ] '+start, '- [x] '+start, 1)
todo = todo.replace('收紧稿件 L54–58/L195：', '收紧旧稿对应段落（新版第 2、7.2 节）：')
todo = todo.replace('- [ ] Hand 保留参考支持的关联见证与消费边界；复杂溯源放补充材料，不从一张图片推论所有输入均不受影响。', '- [x] Hand 保留参考支持的关联见证与消费边界；不从一张图片推论所有输入均不受影响。\n- [ ] 按最终 venue 篇幅压缩 Hand 复杂溯源，并整理正式补充材料。')
todo = todo.replace('- [ ] 整理最小重建包、逐项 claim-to-artifact 对应；确定 venue 后再检查模板、页数与披露要求。', '- [x] 更新逐项 claim-to-artifact 对应及输入哈希；本轮共 12 项主张、51 个固定来源。\n- [ ] 整理独立可用的公开最小重建包；确定 venue 后再检查模板、页数与披露要求。当前 8 页通用阅读版不代表 venue 页数达标。')
todo = todo.replace('优先处理本轮审计提出的稿件定点修改，并进行 P2 同 Android 消费者对照；P3 按限定范围查证。', '进行 P2 同 Android 消费者对照；P3 按限定范围查证。审计提出的稿件定点修改已完成，后续根据新证据局部更新。')
TODO.write_text(todo)
write('TODO.after.md', todo)

write('REVISION_NOTES.md', '''# 审计后的论文修订

已在新目录修订稿件；旧稿与旧审计包未被修改。本轮是稿件编辑，没有新增模型实验。

1. 主论证继续以受控执行证据为中心：契约定义 → E1 实际 getter 失败 → E2 成功但关联变化 → E3 配置间检查阶段差异 → Hand 参考语义与消费边界 → 外部检查与预检限制。S/I/D 分开，P 单列为干预保持性证据。
2. 将 E1/E2 的干预、描述控制、数值保持及恢复合为一张主表；加入已封存审计中的新目录构建和新 AVD 执行。明确 8 份阶段/变体执行记录、5 个独特 artifact–consumer 配置、16 次输入观测，保留工具链复用及 harness 改动限制。
3. 新增官方入口、合理简单基线、E5 和 Task 初始化对照表。在五个核心条件上，E5 没有增加检出；因此保持支撑工具定位。另述张量 metadata 数量负控，避免与删除一行标签混淆。
4. 修正 E5 范围：有限模板正则匹配不等于完整 Java 数据流分析，也不能保证所有未知语法都正确弃权。此范围问题没有推翻当前已测 fixture 的结果。
5. 补入 MLGuard、DocTer、ACETest，并修正 DARA 的技术定位。区别限定于四篇指定全文，未宣称穷尽新颖性。
6. 明确旧/新生成 classes 与新构建 DEX 的比较范围、加载前资产哈希的范围、历史累积 logcat 的归因限制；保留 E3 跨平台、E2 类序参考缺失、Hand 单图和待人工核验边界。

## 检查与产物

- PDF：8 页通用双栏阅读版；已检查全部页面，没有可见重叠或截断，LaTeX 无未解析引用或 overfull 警告。不声明符合具体 venue 篇幅。
- 三路 AI 交叉审读通过，建议采纳记录见 review/RESOLUTION.md；不计作人工审计。
- 自动化核对 12 项主张，固定 51 个来源哈希；编辑脚本在临时目录重建得到相同源文件与 diff。
- 旧稿和审计包分别按原清单只读验证；结果见 verification/preserved-packages.json。
- 当前 TODO 已更新，更新前后副本均保存在此目录。

## 后续工作

优先完成 P2 同 Android 消费者对照；P3 按限定范围查证独立类序参考及自然案例。人工核验、独立可用的公开复现包和 venue 格式仍待完成。当前基线结果不支持把 E5 提升为独立方法贡献。
''')

check = json.loads((ROOT/'verification/revision-check.json').read_text())
write('REVISION_STATUS.json', {
    'created_utc':NOW, 'status':'AUDIT_INFORMED_DRAFT_COMPLETE', 'activity':'Editorial revision of existing empirical manuscript',
    'manuscript_sha256':sha(ROOT/'manuscript/paper.tex'), 'pdf_sha256':sha(ROOT/'manuscript/paper.pdf'),
    'pages_in_generic_reading_layout':8, 'claim_count':12, 'source_provenance_count':51,
    'automatic_check_status':check['status'], 'agent_cross_reviews':3, 'all_pages_visually_inspected':True,
    'model_experiments_run_during_editing':False, 'independent_human_verification_complete':False, 'venue_fit_claimed':False,
    'source_reproduction':'byte-identical source and patch in temporary directory',
    'old_packages_verified':preserved, 'todo_path':str(TODO), 'todo_after_sha256':sha(TODO),
    'open_items':['same-Android Task comparison','bounded artifact-tied class-order reference inquiry','bounded natural-case inquiry','human audit','standalone public reproduction deposit','venue formatting'],
    'contribution_position':'Controlled empirical execution study; pre-flight checker is a supporting tool with no additional rejection established on the five core conditions.',
})
write('commands.sh', '''#!/usr/bin/env bash
# Editorial commands used for this revision, in order. Run rebuilds in a COPY
# of this directory; never overwrite a sealed package or historical evidence.
set -euo pipefail
cd /workspace/metadata-contract-paper-revision-20261004T065132Z
python scripts/revise_manuscript.py
bash build.sh
# The first map creation wrote CLAIM_EVIDENCE.json then stopped at an overly
# strict PDF contiguous-text assertion. CHECK_NOTES.md records the correction.
# Initial invocation: python scripts/verify_revision.py --write-map --record verification/revision-check.json
python scripts/verify_revision.py --record verification/revision-check.json
# The following one-time finalizer also updates the editable project TODO.
python scripts/finalize_revision.py
# Seal with a sorted SHA-256 manifest, then verify it (see scripts/seal_revision.py).
python scripts/seal_revision.py
''')
write('README.md', '''# Audit-informed manuscript revision

Read `manuscript/paper.pdf` and `REVISION_NOTES.md`. `manuscript/paper.tex` is the editable source; `manuscript-changes.patch` compares it with the preserved previous manuscript. `CLAIM_EVIDENCE.json` maps 12 claims to evidence, and `SOURCE_PROVENANCE.json` pins 51 inputs.

`verification/` records automated source/evidence checks, source regeneration, preservation of old packages and visual review. `review/` retains three AI reviews and their resolution. `TODO.before.md` and `TODO.after.md` preserve the task-list update.

The revision is an 8-page generic reading draft, not a venue-ready submission. Independent human audit is pending. No model experiment was launched during editing; the fresh Android construction and baseline comparisons reported in the paper come from the previously sealed audit.

To rebuild the PDF, copy this directory elsewhere and run `bash build.sh` in the copy with a compatible TeX installation. Original tooling: Python 3.12.14, pdfTeX 1.40.26 (TeX Live 2025/dev/Debian), Poppler 25.03.0. PDF binary reproducibility is not claimed. `python scripts/verify_revision.py` checks against preserved workspace evidence; it requires the external roots named in the provenance file. This manuscript package is not the standalone experiment reproduction deposit. The one-time finalization script mutates the working TODO and should not be rerun on the sealed package.
''')
print(json.dumps({'status':'PASS','root':str(ROOT),'preserved_packages':preserved,'todo_updated':str(TODO)}, indent=2))
