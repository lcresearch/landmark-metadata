# Bounded literature and bibliography re-audit — current retrieval blocked

Scope: current manuscript lines 233–256, all 14 bibliography entries, the four
previously selected method papers, and the repository's preserved literature
audit. This is another automated agent review, not independent human review or
a systematic novelty search. No prior-work tool was rerun.

## Access and evidence status

The first actual request to the pinned MLGuard full text,
`https://arxiv.org/pdf/2309.01379v1`, failed at the environment proxy with
`Tunnel connection failed: 403 Forbidden`. The main agent independently
confirmed that Crossref was also blocked. At that check, the runtime status
reported current observations but network state `unknown`, original spec 1,
and package-manager preset only. The requested additional scholarly domains
were saved in the editable draft but were not established as applied policy.

No proxy, TLS, host, or access-control workaround was attempted. The four PDFs
and earlier Crossref response bodies are absent from this workspace. Therefore
**no fresh full-text or publication-metadata verification was completed** in this
subtask. The historical audit's claim that it previously inspected full texts
is source testimony; reading that report does not independently reproduce it.

The accompanying `retrieve_literature.py` is ready to retrieve only these exact
versions and cited identities after the domain changes take effect. It retains
request URLs, status, final URLs, timestamps, SHA-256 digests, and PDF conversion
results; does not silently substitute different arXiv revisions; and writes all
downloaded material outside Git:

```bash
python /workspace/repro-literature/retrieve_literature.py \
  --output-dir /workspace/repro-literature/retrieval-after-policy-save
```

Required scholarly destinations are `arxiv.org`, `api.crossref.org`, and
`link.springer.com` for the URLs currently in that script. A redirect to another
blocked publisher host must be recorded and handled through environment
settings, not bypassed. Saving a draft alone is not proof that any request works.

## Current technical positioning: internal comparison only

The table below compares the current manuscript against the preserved historical
full-text audit. Agreement is not a newly verified assertion about the external
papers. Page references originate in that historical audit and remain pending
fresh comparison with actual PDF text.

| Work / exact requested version | Current manuscript attribution | Repository audit's stated support | Independent status this turn |
|---|---|---|---|
| MLGuard `2309.01379v1` | Developer-specified ML contracts, probabilistic validation models, generated wrappers; vision and future implementation/evaluation | §3.1–3.3, PDF pp. 3–4; §5 “Future Plans”, p. 4 | Internally consistent; full text and bibliographic identity not freshly verified |
| DocTer `2109.01002v4` | Rules learned from annotated documentation; constraint extraction and conforming/violating input generation | §2.1–2.5, PDF pp. 3–8 | Internally consistent; full text not freshly verified |
| ACETest `2305.17914v2` | Operator validation-code analysis, user-controllability propagation, constraint solving; LLVM/SVF, library-specific handling, Z3 | §3.1–3.3, pp. 3–7; §4, p. 7 | Internally consistent; full text not freshly verified |
| DARA DOI `10.1007/s10664-025-10711-4` | Model-derived architecture features compared with supplied naming/architectural metadata | §7.2.1–7.2.3, pp. 31–33; §7.3.3, p. 40 | Internally consistent; journal PDF not recovered or freshly verified |

The current prose correctly retains distinctions already present in the
repository: MLGuard's reviewed version is described as a proposal; DARA is not
reduced to documentation inspection; DocTer and ACETest are substantive
constraint-extraction/testing precedents. The manuscript does not claim a novel
general algorithm for shape constraints or a new concept of contracts.

Line 240's assertion that those four papers do not demonstrate the same complete
artifact-to-resource-to-generated-getter connection remains a **historical
bounded-review claim**. This subtask cannot independently confirm that negative
claim without the full texts. Even a successful four-paper review would not
establish exhaustive novelty. Do not upgrade it based on this static comparison.

## Bibliography audit

The current manuscript has 14 unique bibliography keys and all 14 are cited.
There are no undefined citation keys, uncited entries, or duplicate keys in the
static check. `/workspace/repro-literature/bibliography-static.json` records the
exact manuscript digest and every entry with its line number.

| Entry | Requested external identity check | Present finding |
|---|---|---|
| MLGuard | Sheng Wong et al.; 2023; SE4SafeML; `10.1145/3617574.3617859` | Matches the identifiers/titles in the repository's earlier audit; authors/year/DOI not independently revalidated |
| DocTer | Danning Xie et al.; ISSTA 2022; `10.1145/3533767.3534220` | Internal title/DOI match. Manuscript explicitly distinguishes the later arXiv v4 revision from publication year; no demonstrated year mismatch |
| ACETest | Jingyi Shi et al.; ISSTA 2023; `10.1145/3597926.3598088` | Internal title/DOI match; external identity pending |
| Meyer | B. Meyer; *Computer* 25(10), 40–51, 1992; `10.1109/2.161279` | DOI and publication tuple are present; external identity pending |
| Stalnaker | T. Stalnaker et al.; stated 2026; `10.1145/3776739` | Full bibliographic identity, title, publication year, venue and abstract not recovered; UNKNOWN rather than validated |
| DARA | W. Jiang et al.; *Empirical Software Engineering* 30:155, 2025; `10.1007/s10664-025-10711-4` | Internal title/DOI match; authors, article number and year pending external verification |
| AIBOM | M. Erfan, A. Ryan, M. R. Rahman; `2607.17242v1`; stated 2026 preprint | Actual arXiv entry, title and authors not recovered; UNKNOWN rather than validated |

The other seven entries are implementation/documentation/artifact references:
metadata schema v0.4.4, code-generation documentation, TensorLabel v0.4.4,
EfficientNet asset, ImageClassifier v0.4.4, and two MediaPipe immutable-commit
source references. They are not scholarly author/year claims. Their actual
artifact/source recovery is handled by the other reproduction subtasks; this
literature subtask does not count the URLs' presence as independent retrieval.

Two bibliography presentation gaps are concrete even without external access:

- `tensorlabel` gives a filename/version and says source/binary are preserved,
  but supplies no URL or fully qualified repository path. Add the versioned
  source URL (and keep exact recovered binary hashes in the evidence index).
- `stalnaker` supplies title, year and DOI without publication venue. Complete
  it only after verifying the DOI metadata. The AIBOM entry likewise needs actual
  arXiv metadata verification before being treated as a checked citation.

No definite scholarly title/author/year/DOI mismatch was established by the
available evidence. That finding means insufficient fresh verification, not a
positive assertion that all bibliography entries are accurate.

## Handoff

Source-only files safe to preserve: this report and `retrieve_literature.py`.
Downloaded PDFs, publisher/API responses, extracted full text and execution
records stay in `/workspace/repro-literature` outside the source repository.
After network changes are applied, retrieve the exact papers, read method and
implementation/evaluation sections, verify each attribution against their full
text, and replace these pending statuses with specific evidence-backed results.
