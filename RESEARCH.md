# Research — 22 October 2026

Demand is **inferred** from this workflow: A stale read may be legal during an overlapping write; sorting completion times alone gives the wrong explanation.

[Exact stars-desc GitHub query](https://github.com/search?q=linearizability%20sort%3Astars-desc&type=repositories), observed 2026-10-22T06:18:36.315Z. Highest-star relevant comparable found in the inspected pool: `anishathalye/porcupine`. Keywords are narrow; established comparables were supplemented directly. The difference-constraints keyword results were mostly unrelated and do not establish market coverage.

| Comparable | Stars | Last push | GitHub license metadata | Workflow and setup |
| --- | ---: | --- | --- | --- |
| [anishathalye/porcupine](https://github.com/anishathalye/porcupine) | 1271 | 2026-09-21T03:23:08Z | MIT | Go checker with executable sequential models and history visualization; broader models and algorithms. |
| [jepsen-io/knossos](https://github.com/jepsen-io/knossos) | 426 | 2026-07-17T20:13:25Z | unknown | Clojure/EDN model and history checking including uncertain operations; README explicitly cautions about algorithm certainty. |
| [microsoft/accordant](https://github.com/microsoft/accordant) | 69 | 2026-09-14T19:04:18Z | MIT | .NET model-based test generation and executable specifications, NuGet setup and samples. |

## Choice and tradeoffs

Find a real-time-respecting read/write/CAS register linearization or exhaust a bounded search with an explicit UNKNOWN budget state. Clock quorum and event-time tools inspect clocks or stream windows; this checks concurrent operation semantics against one register specification.

The established alternatives are broader and may be the right choice for their supported ecosystem. Our small CLI offers one dependency-free runtime and an inspectable JSON report for the stated subset. It sacrifices generality and may reject valid real-world input outside that subset. READMEs/current docs/source and sampled issues were inspected for workflow context; this does not prove competitor feature absence. ATL explicitly supports WAV CUE/LIST, NetworkX explicitly returns negative cycles, and RLEMaskLib performs mask operations without full raster expansion. Our example proves only our behavior.

Installability and first-result instructions are documented above and in upstream READMEs. Competitor clean installs, time to first useful result, reliability, support response and performance were **not measured**. No superiority, adoption or global ranking claim. Stars are research context only. [Exact provenance and sampled issues/PRs](RESEARCH_PROVENANCE.json). Inconclusive GitHub license metadata is not a legal conclusion; NetworkX README states BSD3, Z3 README MIT, and Knossos README EPL. No implementation is reused.

Primary references:
- https://github.com/anishathalye/porcupine
- https://github.com/jepsen-io/knossos
