# Screening validation and scope

The protocol fixed the existing seven-report pool before fresh GitHub retrieval.
The connector returned seven issue bodies and 69 comments; each fetched comment
count matched its issue metadata. All bodies and comments were read. Nineteen
GitHub response files include the report records and selected current example
sources. No new search, additional candidate or maintainer contact occurred.

Initial web-tool access failed for some old TFHub/Drive/overview URLs. Those
failures were not treated as missing artifacts. The retained source helper made
bounded unauthenticated public GETs, with at most 4,096 retained bytes for binary
responses and a 1 MiB limit for text. Five initial links were checked, followed
by the exact DeepLab URL discovered in the official example download script.
No fetched script was executed. HTTP 200 with TFL3 prefixes supports limited
availability, not whole-file identity or verified model structure. Drive returned
HTTP 404; it was not bypassed or replaced with a guessed asset.

Actual initial command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 work/case-screening-20261111/check_link_availability.py \
  --output /tmp/landmark-case-screen-20261111/availability
```

The same module's `inspect` function checked the discovered DeepLab URL into
`/tmp/landmark-case-screen-20261111/deeplab-link/`; its exact requested URL,
redirects, times, response headers and prefix identity are retained there.
The module was imported with `PYTHONDONTWRITEBYTECODE=1`. All seven report pairs,
five linked-source responses, six link observations/prefixes and the web-access
note were copied to `/home/hsz/landmark-evidence/case-screening-20261111/` and
verified byte-for-byte: 33 copied files plus the retention receipt. The committed
[sources.json](sources.json) pins all 34 external records and the source inputs.
Temporary signed download query strings were removed from the committed summary.

The final source checker validates syntax, navigation, all current manuscript and
screening pins, preserved imports and archive resolution. `git diff --check`
passes. The earlier paper-stage 193 regression tests passed; this screening adds
no experiment code or inference. The link helper was tested by the actual bounded
requests above. Source/helper records do not prove independently reproduced
natural cases: that count remains zero.

The current manuscript, its scientific counts and the frozen November evidence
index were not changed by screening. Candidate-specific missing prerequisites,
proposed experiments and stop rules are in [SHORTLIST.md](SHORTLIST.md).
