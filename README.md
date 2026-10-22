# register-history-witness

Find a real-time-respecting read/write/CAS register linearization or exhaust a bounded search with an explicit UNKNOWN budget state.

For distributed-systems developers examining a tiny completed register trace.

## Quickstart

Python3.10+; no runtime dependencies or external service. The wheel build needs setuptools and wheel from the normal Python registry. Linux shell:

```sh
git clone https://github.com/nripankadas07/register-history-witness.git
cd register-history-witness
python -m venv .venv
. .venv/bin/activate
python -m pip install .
register-history-witness example.json
```

An overlapping read of0 linearizes before the write of1 despite the earlier write invocation. [Expected report](example-output.json).

## Input and interpretation

Start from [example.json](example.json). Inputs are read only. JSON files are UTF8,<=1MiB; duplicate/unknown keys, booleans in integer fields and nonfinite constants reject.

At most16 complete operations on one register. Unique operation IDs, per-client nonoverlapping half-open integer intervals [start,end); end<=next start imposes precedence. Reads return value, writes are successful, CAS has expect/update/result. Values null, bounded integers or strings<=128; no boolean register values. Search memoizes (completed set,value),<=100000 states (state_limit may lower). UNKNOWN is never NOT_LINEARIZABLE. No pending/failed/timed-out ops, multiple keys, histories collected from live systems, distributed clocks or full Jepsen/Porcupine equivalence. A deepest prefix is diagnostic, not a standalone impossibility proof.

Exit0 means analysis completed, including any infeasibility, NOT_LINEARIZABLE, UNKNOWN or reference finding. Inspect the report fields; exit0 is not a health assertion. Exit2 means malformed/unsupported input or I/O failure, with JSON error on stderr and no partial report. No live-system operations, network requests or credential reads occur. Reports may expose supplied identifiers and bytes; review before sharing.

## Verification

```sh
python -m unittest -v
python -m compileall -q register_history_witness.py
python -m pip wheel --no-deps . -w dist
```

18 histories against an independent full permutation oracle, stale reads, overlap, CAS/null, budget UNKNOWN and invalid client histories. [Validation record](VALIDATION.md). CI runs Python3.10/3.12/3.14 on Linux and the installed console outside checkout. Windows/macOS, production workloads and competitor performance remain untested.

## Scope and provenance

Alpha utility. Original AI-assisted code and invented fixtures; standard algorithms independently reimplemented. No third-party implementation/prose copied. MIT. [Candidate brief](BRIEF.json), [research](RESEARCH.md), [support](SUPPORT.md), [contributing](CONTRIBUTING.md), [security](SECURITY.md).

Clock quorum and event-time tools inspect clocks or stream windows; this checks concurrent operation semantics against one register specification.
