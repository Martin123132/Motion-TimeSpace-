# Accepted implementation and retained development attempts

Accepted:
- build_canonical_stress.py and build-canonical-stress/: opt-in native cold point and canonical stress derivative.
- native_context_v2.py, matched_cold_fibre.py, cold_fibre.py: native coefficient adapter and consistent background representation.
- cold_precision_v5.py: high-precision independent coordinate conversion.
- cold_operator_v2.py, collect_cold_v2.py: qualified stable coupled generator and physical-clock mean.
- qualify_adapter_v3.py, validate_cold_v2.py, derive_cold_identities.py, audit_cold.py: final checks.
- seal_stage.ps1: immutable closeout after all workers exit.

Scientific diagnostic progression, not accepted substitutes:
- cold-half-01: native scalar row gate failed at 244.62; candidate matrices not promoted.
- diagnosis-01: identifies gauge-column concentration and why high precision applied after rounding cannot repair it.
- precision-repair-01: high-precision derivative with inconsistently rounded carrier rate; diagnostic residual remains large.
- precision-repair-02: consistent carrier identity, remaining source/background mismatch.
- precision-repair-03: matched H removes that mismatch, but native stress differentiation still exceeds 2e-5.
- precision-repair-06: full high-precision coordinate conversion confirms the remaining native stress cancellation.
- precision-repair-07: canonical stress identities resolve that source error; the accepted 256-node scans then recheck all phases.

Preserved implementation/endpoint failures:
- build-01: checker-name import mismatch before compilation; build-02 fixes the name.
- qualify-01: incorrect target dictionary key; qualify-02 fixes the adapter smoke test.
- precision-repair-04 and precision-repair-05: return-shape errors in intermediate conversion helpers, before successful validation. cold_precision_v3/v4 are NOT accepted implementations.
- independent-half-01: one-ulp N endpoint overshoot after six passing cases. independent-half-02 uses the exact saved endpoint and hashes/reuses those six controls.

Older source files are retained as development records, not recommended entry points.
No failed attempt is silently retried under its previous receipt name.
The six nonzero process exits and intermediate diagnostic residuals are recorded explicitly; successful script exit alone is not a scientific pass.
