"""Apply the completed audit's editorial changes to a new manuscript copy."""
from pathlib import Path
import difflib
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/workspace/metadata-contract-paper-rewrite-20261004T052625Z/manuscript/paper.tex')
original=BASE.read_text();paper=original
def para(prefix,replacement):
    global paper
    assert paper.count(prefix)==1,prefix
    start=paper.index(prefix)
    end=paper.index('\n\n',start)
    paper=paper[:start]+replacement+paper[end:]

paper=paper.replace('Evidence-based rewrite; independent human audit and venue formatting pending','Audit-informed revision; independent human audit and venue formatting pending')
para(r'\begin{abstract}',r'''\begin{abstract}
Model metadata and associated resources participate in executable interfaces through generated bindings and runtime decoding. We study their effects while holding model computation fixed. In an EfficientNet classifier, deleting one associated label preserves the graph, weights, embedded metadata, generated Java, compiled code, and tested numerical outputs, but changes an actual generated Android getter from success to an exception after inference. Restoration recovers success. A predetermined, count-preserving label permutation instead completes every tested stage while changing 999 of 1,000 exposed label strings; scores and output positions remain unchanged. A fresh build and new Android virtual device reproduce both outcomes. An official Task classifier rejects the identical deletion artifact during initialization, establishing different enforcement stages for the two configured consumers. A secondary Hand case supplies a source-backed output-role mismatch, yet its metadata exchange leaves the tested official Task result unchanged. We separate structural acceptance, reference-backed association agreement, and selected-decoder compatibility, with intervention preservation checked separately. A five-condition comparison finds no additional rejection by our supporting pre-flight procedure over an implementation-matched simple baseline or Task initialization. External static checks document abstentions and unsupported paths. The study establishes controlled interface consequences and their consumer boundaries in the tested configurations.
\end{abstract}''')
para('We ask:',r'''Three questions organize the study. \textbf{RQ1:} When computation is held fixed, how can model-package associations change a public interface's behavior? E1/E2 answer through an executed failure, a successful association change, and reversals. \textbf{RQ2:} At which stage do configured consumers enforce the relevant condition? E3 compares two official paths, while Hand bounds the reach of an output-role witness through a task-specific consumer. \textbf{RQ3:} Which conditions can be checked before execution, and which judgments require additional evidence? The official-tool comparison, external scope checks, and pre-flight limits answer this question. EfficientNet is primary because its generated Java compiles without repair.''')
para('The principal contribution',r'''The principal contribution is a controlled execution study with description controls, preserving interventions, reversals, and stage-specific observations. A second contribution is a comparison of enforcement boundaries in explicitly identified consumer configurations. A supporting pre-flight procedure separates structural facts, supplied-reference agreement, and selected-decoder preconditions for recognized generator templates. Official libraries already enforce the observed label-count condition, and our core baseline comparison establishes no additional rejected artifact. The contribution is the executed characterization of the associations and boundaries, supported by a scoped diagnostic tool.''')
para('We inspect the actually generated getter',r'''For recognized Support 0.4.4 generator templates, the checker joins category-getter patterns with tensor and associated-file declarations and a matching default-postprocessor body. The exercised list-based \code{TensorLabel} path~\cite{tensorlabel} has the following conditions. Let the static positive output shape be $d=(d_0,\ldots,d_{r-1})$ and the loaded label list be $L$. The selected axis is
\begin{equation}
a=\min\{j:d_j>1\}.
\end{equation}
This path requires $a$ to exist, $d_a=|L|$, and $a=r-1$ for category-list conversion. Label counting follows the library's treatment of blank lines. Disassembly of the Support API jar used by the Android build confirms the strict final-axis guard. These are conditions of this overload and consumer path; determining which path is selected is a separate analysis obligation. The template matcher's coverage and abstention limits are reported in Section~\ref{sec:scope}.''')
# The old formal paragraph is a single block including the displayed equation.
old_start=paper.index('\\begin{table}[t]',paper.index('\\subsection{Observed failure and reversal}'))
old_end=paper.index('\\end{table}',old_start)+len('\\end{table}')
paper=paper[:old_start]+r'''\begin{table*}[t]
\centering\small
\setlength{\tabcolsep}{6pt}
\begin{tabular}{@{}lrlllll@{}}
\toprule
Condition & Labels & Graph/weights & Generated code & Raw output & Getter & Exposed labels\\
\midrule
Original & 1,000 & baseline & baseline & baseline & success & baseline\\
Description control & 1,000 & same & same & same & success & same\\
Label deletion & 999 & same & same & same & exception & not returned\\
Label permutation & 1,000 & same & same & same & success & 999 changed\\
Restoration / inverse & 1,000 & same & same & same & success & restored\\
\bottomrule
\end{tabular}
\caption{Combined E1/E2 evidence relative to the original. Every condition passes structural population, generation, compilation, packaging, loading, and inference. Code equality concerns generated Java and classes; raw equality concerns both prescribed inputs. The description edit changes embedded metadata but preserves the displayed properties. Shared phase conditions are not independent models. The permutation is detailed in Section~\ref{sec:e2}.}
\label{tab:e1}
\end{table*}'''+paper[old_end:]
fresh=(ROOT/'review/rebuild-evidence-proposal.txt').read_text().split('An additional agent-run construction check',1)[1].split('\n\nEvidence review scope:',1)[0]
fresh='An additional agent-run construction check '+fresh.strip()
fresh=fresh.replace('artifact–consumer','artifact--consumer').replace('not an independent human reproduction nor a reconstruction from archived dependencies','not an independent human reproduction nor a fresh installation of the archived toolchains')
# Keep wording explicit even though the proposal used a different conjunction.
fresh=fresh.replace('neither an independent human reproduction nor a reconstruction from archived dependencies','neither an independent human reproduction nor a fresh installation of the archived toolchains')
paper=paper.replace(r'\section{E3: Different Stages of Contract Enforcement}',r'''\subsection{Fresh construction audit of E1/E2}
\label{sec:rebuild}
'''+fresh+'\n\n'+r'\section{E3: Different Stages of Contract Enforcement}')
para('The command inspects the generated tensor',r'''The command uses regular expressions to extract selected getter, tensor, and associated-file declarations from official generated templates and inspect a matching default postprocessor. For the E1 mutant, it identifies \code{getProbabilityAsCategoryList}, output 0, axis 1 of size 1,000, and 999 loaded labels. This gives a path-specific diagnostic before compilation, loading, or inference. The command reports S, supplied-reference I, selected-path D, and P separately; it does not execute the wrapper.''')
para('This procedure is a supporting implementation',r'''The implementation abstains on dynamic signatures and processing forms it explicitly recognizes as unsupported. It is not a general Java data-flow analysis: full buffer and processor assignments are not traced, and an unmatched getter pattern can be reported as inapplicable rather than unknown. Factory or otherwise unrecognized processor syntax can evade the operation matcher. Such syntax is outside the demonstrated analysis scope; there is no guarantee that every unknown form is correctly reported as abstention. The audit found this limitation in the extraction code, without overturning a recorded fixture outcome.''')
baseline=r'''\subsection{Official checks and a simple baseline}
A subsequent comparison uses the five byte-distinct E1/E2 artifacts in Table~\ref{tab:baseline}. The simple static baseline assumes one graph output, a unique \code{TENSOR\_AXIS\_LABELS} resource, a positive static shape/signature, and the default shape-preserving TensorLabel category path. It applies the library's axis and cardinality conditions without inferring arbitrary getter bindings. Its selected output and resource agree with the actual core bindings inspected in the audit. The unchanged pre-flight rules are rerun with logging redirected to a new evidence directory.

All five files are readable and accepted by metadata population. The simple baseline, pre-flight D, and official Linux Task initialization each reject only the 999-label deletion. Thus, the pre-flight command adds zero rejected conditions over either comparator in this set. Its role here is early diagnosis tied to a generated path, not a demonstrated increase in defect-detection capability. The count-preserving permutation passes, with I still abstaining. These baseline runs stop at Task initialization and add no Task classification or Android execution.

\begin{table*}[t]
\centering\small
\setlength{\tabcolsep}{7pt}
\begin{tabular}{@{}lrlllll@{}}
\toprule
Condition & Labels & Display & Population & Simple baseline & Pre-flight D & Task init.\\
\midrule
Original & 1,000 & readable & accepted & compatible & compatible & pass\\
Description control & 1,000 & readable & accepted & compatible & compatible & pass\\
Label deletion & 999 & readable & accepted & incompatible & incompatible & fail\\
Label permutation & 1,000 & readable & accepted & compatible & compatible & pass\\
Label restoration & 1,000 & readable & accepted & compatible & compatible & pass\\
\bottomrule
\end{tabular}
\caption{Fresh checks of five exact files, with E1/E2 aliases deduplicated. Each has one graph output and one output-metadata entry. Compatible means only the selected static decoder preconditions; Task results concern initialization only. No class-order reference is supplied. The separate structural negative control is described in the text.}
\label{tab:baseline}
\end{table*}

A separate preserved structural control has one graph output, zero output-metadata entries, and the unchanged 1,000-label archive. \code{MetadataDisplayer} reads it, but \code{MetadataPopulator} rejects it in \code{load\_metadata\_buffer} validation before \code{populate} is reached. Metadata-entry cardinality and associated-label cardinality are different conditions, and readability is not population acceptance. This control is reported separately from the five core conditions.

'''
paper=paper.replace(r'\section{Relationship to Existing Work}',baseline+r'\section{Relationship to Existing Work}')
proposal=(ROOT/'review/related-work-proposal.txt').read_text()
related=proposal.split('Executable preconditions',1)[1].split('\n\nNew bibliography entries',1)[0]
related='Executable preconditions'+related
related=related.replace('The reviewed methods and evaluations','The four method papers examined in full')
related=related.replace('its additional capability must be assessed against comparable official checks and simple baselines.','the comparison in Section~\\ref{sec:scope} found no additional rejected core condition over the simple baseline or Task initialization.')
a=paper.index(r'\section{Relationship to Existing Work}')
b=paper.index(r'\section{Validity, Reproduction, and Remaining Work}')
paper=paper[:a]+r'\section{Relationship to Existing Work}'+'\n'+related+'\n\n'+paper[b:]
para('The generated historical Gradle project',r'''The generated historical Gradle project is not built unchanged, and no Android Studio result is claimed. Additional declared APK dependencies were recovered and all initial APKs rebuilt before any Android execution; both build records are preserved. The later construction audit uses new outputs and a new AVD with the same installed toolchain (Section~\ref{sec:rebuild}). The emulator is version 37.2.12 (build 16428233); its API-30 image archive is labeled revision 11 while internal properties report revision 10. Archive digest and runtime fingerprint identify the image. Task wheel/native hashes are archived, but their separate embedded interpreter versions and source-build equivalence are not established. Same-toolchain reconstruction and replay remain distinct from independent researcher reproduction.''')
para('The local package preserves exact models',r'''The local package preserves models, associated payloads, source references, controls, generated Java, classes/DEX, APKs, input/output bytes, exceptions, commands, dependency archives, and SHA-256 manifests. The companion claim map distinguishes historical executions, checks of their retained bytes, and the subsequent construction and baseline runs. Preparing this revision launches no further model experiments. The raw-array audit uses a separate checking implementation; it does not supply an independent observer of the earlier executions. Historical logcat dumps are cumulative, so exception attribution uses per-run device records and execution windows. The package still depends on existing workspace roots; a standalone public deposit, independent human audit, and venue-specific formatting remain open.''')
# Keep full-text versions in an explicit compact paragraph, not as a novelty guarantee.
marker=r'\paragraph{AI assistance and responsibility.}'
note=r'''\paragraph{Literature scope.}
The bounded audit inspected MLGuard, DocTer, and ACETest full texts at arXiv versions 2309.01379v1, 2109.01002v4, and 2305.17914v2, respectively, and DARA's preserved journal version. Publication identities were checked separately; the DocTer revision postdates its 2022 publication. Their tools were not rerun, and Stalnaker positioning remains abstract-based. This comparison is not a systematic search of all relevant contract or deployment work.

'''
paper=paper.replace(marker,note+marker)
para('With graph computation and generated code held fixed',r'''With graph computation and generated code held fixed, an associated-label intervention causes an actual generated Android getter to fail after inference; a count-preserving permutation instead succeeds while changing the exposed association. Restoration reverses both outcomes, and fresh same-toolchain construction reproduces them. The tested Task configuration rejects the cardinality mismatch earlier, while the secondary Hand Task preserves its result on the prescribed input. These observations separate structural acceptance, reference-backed association agreement, and selected-consumer compatibility, with P checking intervention preservation. The simple-baseline comparison places pre-flight checking as a supporting diagnostic tool. The principal result is the controlled execution evidence connecting model-package associations to public-interface behavior and configured enforcement boundaries.''')
bibs=proposal.split('New bibliography entries\n========================\n\n',1)[1].split('\n\nOptional compact',1)[0]
paper=paper.replace(r'\bibitem{meyer}',bibs+'\n\n'+r'\bibitem{meyer}')
paper=paper.replace(r'\begin{thebibliography}{12}',r'\begin{thebibliography}{14}')
(ROOT/'manuscript/paper.tex').write_text(paper)
(ROOT/'manuscript-changes.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),paper.splitlines(True),fromfile=str(BASE),tofile='manuscript/paper.tex')))
print('Wrote audit-informed revision:',ROOT/'manuscript/paper.tex')
