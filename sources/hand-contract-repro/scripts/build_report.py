from pathlib import Path
import datetime
import hashlib
import html
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def main():
    static=json.loads((ROOT/'results/static-results.json').read_text())
    replay=json.loads((ROOT/'results/fresh-replay.json').read_text())
    compile=json.loads((ROOT/'results/compile-results.json').read_text())
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    rows=[]
    for name,label in [('original','原始模型'),('swapped','交换元数据 0/2'),('description_control','仅改描述对照'),('swap_back_control','交换后还原对照')]:
        s=static['variants'][name]
        c=compile['variants'][name]
        rows.append(f"<tr><td>{label}</td><td>{len(s['changed_byte_offsets'])}</td><td>接受</td><td>{c['raw']['exit_code']} → {c['repaired']['exit_code']}</td><td>{c['bytecode_field_output_mapping']['handedness']}</td><td>{c['bytecode_field_output_mapping']['landmarks']}</td><td>12/12，所有输出相同</td></tr>")
    doc='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hand Landmarker 元数据契约：复现与审稿判断</title>
<style>body{font:16px/1.75 system-ui,sans-serif;margin:40px auto;max-width:1100px;padding:0 24px;color:#17242e;background:#fbfcfe}h1{line-height:1.3;font-size:30px}h2{margin-top:34px;font-size:23px}a{color:#075f9b}code,pre{font-family:ui-monospace,monospace;font-size:13px;overflow-wrap:anywhere}pre{background:#eef2f6;padding:16px;white-space:pre-wrap}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;border:1px solid #cad3dd;padding:9px}th{background:#e9f0f7}.callout{background:#e9f4f2;border-left:5px solid #16786d;padding:15px 20px}.note{background:#fff3dd;border-left:5px solid #ba8029;padding:15px 20px}.small{font-size:13px;color:#455a68}@media print{body{margin:12mm;max-width:none}a{color:inherit}pre,table{break-inside:avoid}}</style>
<h1>Hand Landmarker 元数据契约：新实验与可信度判断</h1>
<p class="small">实验日期：2026-10-03 UTC · 单个已确定组件 · 主机 CPU / JVM · 这是一份本次新实验报告，不是对历史记录的重新命名。</p>
<div class="callout"><strong>核心事实可信，已经重新复现；尚不足以确认论文贡献成立。</strong><br>官方模型的嵌入输出元数据与官方执行图的输出契约错位。只交换元数据关联即可改变生成包装器的编译后绑定，同时保留模型所有非元数据字节和本次测试的数值输出。新增测试同时表明，交换索引仍不能使分类解码器正常工作，因此该对照必须叫“元数据关联交换”，不能叫“完整修复”。</div>
<h2>1. 本次确实跑了什么</h2>
<table><tr><th>变体</th><th>变化字节数</th><th>官方结构校验路径</th><th>原始→修补后 javac 退出码</th><th>handedness 输出位置</th><th>landmarks 输出位置</th><th>CPU 对照</th></tr>ROWS</table>
<p>共 4 个变体 × 12 组预定合成输入 = 48 次主实验推理，保存 192 个输出数组。三种干预/对照变体的所有对应输出与原版逐字节一致，最大绝对差为 0。随后从空的生成目录重新执行完整流程，再完成 48 次推理；归一化后的实验结果完全一致。两轮合计 96 次调用，但它们不是 96 个独立样本。重跑使用同一操作者、环境和依赖，不能称为独立研究者复现。</p>
<p>12 组输入为全 0、全 1、常量 0.5、0→1 渐变，以及固定种子 20261003 的 8 组均匀随机 float32 张量。它们验证计算不变性，不验证真实手部图像精度。CPU 推理使用 tflite-runtime 2.14.0、NumPy 1.26.4、一个线程；默认运行时报告启用 XNNPACK。</p>
<h2>2. 样本身份和语义证据</h2>
<p>官方 <a href="https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task">版本 1 task 包</a>与本次下载的 latest 包字节相同，组件 SHA-256 与原稿完全一致：</p>
<pre>6acda74af3fbf40e68265c20c7394b2bad81a16a481dcd79ad7a081887c3d6b9</pre>
<p>图输出顺序为：0 → tensor 165 / Identity / [1,63]；1 → tensor 164 / Identity_1 / [1,1]；2 → tensor 162 / Identity_2 / [1,1]；3 → tensor 166 / Identity_3 / [1,63]。原始元数据依次命名为 handedness、presense score、landmarks、world landmarks。</p>
<p><a href="sources/metadata_schema.fbs">官方元数据 schema</a>将 output_tensor_metadata 与 SubGraph.outputs 按顺序关联。另有 <a href="sources/hand_landmarks_detector_graph.cc">MediaPipe v0.10.14 官方执行图源码</a>直接将输出 0 用作 landmark_tensors，将输出 2 用作 handedness_tensors。这比“63 看起来像关键点”更有证明力；仍只支撑这个组件和所检查的集成路径。</p>
<p>在原始文件中直接交换元数据向量的两个相对偏移，实际只改动偏移 1188、1189、1196、1197 的 4 个字节。文件长度不变；173 个 buffer 中只有 buffer 172 变化，其余 172 个 buffer 和元数据之外的全部文件字节都不变，附带标签 ZIP 也被保留。移除 TFLITE_METADATA 后的规范化哈希相同。详见 <a href="results/static-results.json">static-results.json</a>。</p>
<h2>3. 编译和绑定实验的范围</h2>
<p>tflite-support 0.4.4 的官方生成器对四个变体都输出存在语法错误的 Java。记录未修补 javac 退出码 1，再对每个变体应用完全相同的四条分隔符规则：删除两个多余逗号、补两个缺失分隔符。改动均限定在源文件第 71、315 行。删除逗号和空白后的完整字符序列相同；getter、getBuffer 与 Metadata 构造逻辑逐段比较未变。</p>
<p>Temurin OpenJDK 17.0.12+7，javac --release 8，记录在案的真实 Android/TFLite jars。修补后包装器与相同消费代码全部编译通过；消费类哈希一致。javap 输出验证原版 handedness→0 / landmarks→2，交换版 handedness→2 / landmarks→0。只改描述与交换后还原两个对照的包装器 class 哈希也与原版一致。没有运行 Android Gradle 打包流程。</p>
<p>这复现了原稿的静态机制和退出码模式。由于历史 companion JSON 与原始补丁不可用，不能声称使用了与 R16 完全相同的全部依赖、补丁文件或重建二进制。也不能把旧版生成器结论直接推广到所有 Android Studio / LiteRT 绑定工具。</p>
<p><a href="results/compile-results.json">编译结果</a> · <a href="logs/original-raw-javac.log">原始编译失败日志</a> · <a href="logs/original-syntax.patch">实际补丁</a> · <a href="logs/original-outputs-javap.txt">原版字节码</a> · <a href="logs/swapped-outputs-javap.txt">交换版字节码</a></p>
<h2>4. 新发现：索引交换并不是完整修复</h2>
<div class="note"><strong>生成的分类解码逻辑还有接口不兼容。</strong>模型附带 handedness.txt，内容为 Left、Right 两行。生成的 getter 使用 TensorLabel(labels, tensor).getCategoryList()；此 API 要求存在大于 1 的分类轴，且轴长度等于标签数。</div>
<table><tr><th>主机 JVM 探针</th><th>输入</th><th>实测</th></tr><tr><td>原版 getter 所用的解码表达式</td><td>真实 CPU 全零输入结果，输出 0，[1,63]，2 标签</td><td>IllegalArgumentException: Label number 2 mismatch the shape on axis 1</td></tr><tr><td>交换版 getter 所用的解码表达式</td><td>同样输入的输出 2，[1,1]，2 标签</td><td>IllegalArgumentException: Cannot find an axis to label</td></tr><tr><td>API 正对照</td><td>人工构造 [1,2]，分数 [0.25,0.75]，2 标签</td><td>成功返回 2 个类别</td></tr></table>
<p>探针实际执行官方 TensorLabel 和生成器所用的 DequantizeOp(0,0)，后者在该 float 模型上为恒等处理。探针直接消费保存的 CPU 输出数组，未实例化生成的 Android 包装器，也未运行 Java TFLite 模型解释器。这是隔离的主机后处理异常，不能写成真实用户崩溃或端到端包装器失败。该探索性测试在观察标签内容之后才增加，与预先写下的合成推理测试区分记录。</p>
<p>官方 MediaPipe <a href="sources/tensors_to_classification_calculator.cc">分类计算器</a>对标量分数执行二分类展开；所检查的 Hand 图把标量 p 对应到 Right，并以 1−p 对应到 Left。生成的通用 TensorLabel 表达式并未实现这一特定转换。这里的 [1,2] 正对照只验证 API 基数要求，不声称已经实现完整修复。</p>
<p>第二处应修正文稿的表述：原始关键点输出不能直接叫“归一化坐标”。<a href="sources/tensors_to_landmarks_calculator.cc">官方后处理源码</a>会将 x、y 除以输入宽高，并对 z 应用专门归一化。当前元数据描述本身写着 normalized coordinates；交换元数据不会纠正此描述或自动加入该后处理。应区分原始 63 维坐标与最终归一化关键点。</p>
<p><a href="results/decoder-results.json">探针结果与边界</a> · <a href="scripts/DecoderProbe.java">实际探针代码</a> · <a href="sources/TensorLabel.java">官方 TensorLabel 源码</a></p>
<h2>5. 官方校验器比较</h2>
<p>对四个变体均调用公开流程 MetadataPopulator.with_model_buffer → load_metadata_buffer → populate，均接受。检查保存的 <a href="sources/tflite-support-0.4.4-metadata.py">0.4.4 实现</a>可见相关校验检查标识符、子图数与输入/输出元数据个数等。该实测支持“所测试的结构校验路径没有拒绝此语义错位”；它不等于已经调查所有官方校验器、所有版本或整个工具生态。</p>
<h2>6. 原稿靠不靠谱，论文价值在哪里</h2>
<p><strong>可信部分：</strong>具体样本、输出索引错位、仅改元数据改变生成绑定，以及语法修补前失败/修补后成功，都得到本次新实验支持。原稿主动披露限制，避免直接声称安全、隐私、性能或用户影响，方向是对的。</p>
<p><strong>仍未核实：</strong>工作区没有原稿引用的 R15–R17 冻结记录及 companion JSON，因此本次无法审计 41 例标签、COMP-012 裁决、历史哈希链或旧补丁。这些内容不应被本次单例实验“顺便背书”。按原稿给定的计数，13/41=31.7%，33/41=80.5%；二元 Cohen κ≈0.336，仅是对提供数字的条件算术，受二元重编码和非独立评审流程限制。高比例由 30 个共同非发现主导，不能称为高可靠性。</p>
<p>核对了三个引用的 Crossref / arXiv 元数据，所给标识符对应相关标题；这只确认文献身份，不证明稿件对其方法的概括充分、也不证明新颖性。现有证据更适合作为具体工具链缺陷报告或有边界的短案例。要主张可复用研究贡献，应明确检查规则（索引关联、表示形式、标签数、解码器前提），与具体工具做对照，并在额外模型上验证。不要把“改 metadata 会改 getter 名称”本身当成足够的新颖性。</p>
<p>本次还观察到官方 Hand 图按输出位置接线并配置特定解码器。因此不能从通用生成器的缺陷推出官方 Hand Landmarker 应用同样受影响。未执行官方 Tasks API、真实手图像测试、Android 安装或设备测试；未测延迟、安全、隐私或真实用户影响。</p>
<h2>7. 建议怎样改稿</h2>
<ol><li>中心结论写成：此确定组件存在输出索引—语义关联错误，所测结构校验路径接受该元数据，生成器把关联传播到编译后的接口；该传播在模型计算不变时发生。</li><li>全文把 counterfactual 称为 association-swapped variant，避免“fixed”暗示完整修复。加入标量二分类与通用标签解码器不兼容的新限制。</li><li>修正 normalized landmarks 术语，明确模型原始坐标与官方后处理后的坐标；不要把坐标描述问题混同于索引交换。</li><li>将“全部是历史、没有推理”改为区分历史证据和本次新实验。48 次合成 CPU 推理及主机解码探针只扩大相应证据范围，不能自动升级到设备行为或用户影响。</li><li>41 例 agent 标签记录主要说明审查过程，不能增强单例的统计代表性；可放附录，主文优先呈现精确契约、干预、对照和失败条件。</li><li>论文投稿前仍需人类审计、额外案例或方法价值论证、完整新颖性比较与正式归档。文本中的 鈥� 等乱码也应修复。</li></ol>
<h2>8. 复现与保存</h2>
<p><a href="REPRODUCE.txt">复现说明</a> · <a href="experiment-plan.json">主实验计划</a> · <a href="results/inference-results.json">完整数值摘要</a> · <a href="results/fresh-replay.json">空目录重跑记录</a> · <a href="MANIFEST.json">文件哈希清单</a></p>
<pre>cd /workspace/hand-contract-repro
.venv/bin/python scripts/run_all.py</pre>
<p>压缩包保存原始模型、交换版、官方版本化 task 包、官方契约来源、依赖 jars、全部实验脚本、生成与修补代码、class、日志、输入/输出数组和哈希清单。紧凑包未包含 Python 发行版、Python wheels 或 JDK 压缩包；依赖版本固定，JDK 下载另有精确哈希，恢复完整环境仍需外部包源。工作区与压缩包不是永久公共档案，也不能据此宣称历史 G2 已关闭。</p>
<p class="small">报告生成时间：STAMP<br>新鲜目录重跑归一化结果 SHA-256：REPLAYHASH<br>实验执行、整理及初步判断由 AI 助手完成；没有新增独立人类评审。</p></html>'''
    doc=doc.replace('ROWS',''.join(rows)).replace('STAMP',html.escape(stamp)).replace('REPLAYHASH',replay['normalized_result_sha256'])
    (ROOT/'report.html').write_text(doc)
    selected=[]
    for folder in ['scripts','sources','results','logs','deps','generated','patched','build','replay-evidence']:
        selected.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    for rel in ['report.html','REPRODUCE.txt','requirements.lock','experiment-plan.json','downloads/jdk-download.json','artifacts/original.tflite','artifacts/swapped.tflite','artifacts/official-v1.task','artifacts/handedness.txt']:
        selected.append(ROOT/rel)
    selected=sorted(set(selected))
    files=[]
    for path in selected:
        with path.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
        files.append({'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':digest})
    manifest={'created_utc':stamp,'scope':'Files included in the compact evidence archive; MANIFEST.json itself is excluded to avoid self-reference. Toolchain omissions are disclosed in REPRODUCE.txt.','files':files}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    archive=ROOT.parent/'hand-contract-evidence.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in selected+[ROOT/'MANIFEST.json']:
            z.write(path,arcname='hand-contract-repro/'+str(path.relative_to(ROOT)))
    with archive.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    (ROOT.parent/'hand-contract-evidence.sha256').write_text(digest+'  hand-contract-evidence.zip\n')
    print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'sha256':digest,'files':len(files)+1},indent=2))

if __name__=='__main__':
    main()
