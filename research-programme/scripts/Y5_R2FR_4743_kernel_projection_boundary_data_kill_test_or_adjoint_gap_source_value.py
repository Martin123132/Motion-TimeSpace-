from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4743"
CLAIM_ID = "L-585"
MARKER = "PPC4161_KERNEL_PROJECTION_BOUNDARY_DATA_KILL_TEST_OR_ADJOINT_GAP_SOURCE_VALUE_4743"
PACKET_MARKER = "PPC4161_PACKET_KERNEL_PROJECTION_BOUNDARY_DATA_KILL_TEST_OR_ADJOINT_GAP_SOURCE_VALUE_4743"
DECISION = "KERNEL_PROJECTION_KILL_THEOREM_DERIVED_CONDITIONALLY_BOUNDARY_TRACE_AND_QUOTIENT_DATA_UNSIGNED_CZEROMODE_BOUND_STAGED_NONCLAIM"
NEXT_TARGET = "4744-Y5-R2FR-parent-boundary-trace-contract-or-CzeroMode-source-runner.md"

DOC_PATH = POST / "4743-Y5-R2FR-kernel-projection-boundary-data-kill-test-or-adjoint-gap-source-value.md"
FORMAL_PATH = FORMAL / "759-PPC4161-kernel-projection-boundary-data-kill-test-or-adjoint-gap-source-value.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_SOURCE_REGISTER.csv"
KERNEL_KILL_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_KERNEL_KILL_THEOREM.csv"
BOUNDARY_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_BOUNDARY_TRACE_CONTRACT.csv"
ZERO_MODE_TEST_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_ZERO_MODE_FAMILY_KILL_TEST.csv"
CZEROMODE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_CZEROMODE_BOUND_LAW.csv"
GAP_PROTOCOL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_ADJOINT_GAP_SOURCE_PROTOCOL.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4743_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4743_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4743_0_4742_doc", POST / "4742-Y5-R2FR-adjoint-coercivity-no-zero-mode-proof-or-first-transition-source-value.md", "prove Pi_0 m=0 from boundary/quotient data", "4742 route handoff"),
    ("SRC4743_1_4742_formal", FORMAL / "758-PPC4161-adjoint-coercivity-no-zero-mode-proof-or-first-transition-source-value.md", "`Pi_0 m`: zero-mode projection", "formal kernel obstruction"),
    ("SRC4743_2_4742_proof", SOURCE_DIR / "P8_Y5_R2FR_4742_SPECTRAL_GAP_COERCIVITY_PROOF.csv", "PROOF4742_4_exact_zero", "exact zero implication"),
    ("SRC4743_3_4742_zero_audit", SOURCE_DIR / "P8_Y5_R2FR_4742_ZERO_MODE_KILL_AUDIT.csv", "ZK4742_7_kernel_residual", "kernel residual row"),
    ("SRC4743_4_4742_first_targets", SOURCE_DIR / "P8_Y5_R2FR_4742_FIRST_SOURCE_TARGETS.csv", "FST4742_1_kernel_projection", "first finite source target"),
    ("SRC4743_5_4742_bound", SOURCE_DIR / "P8_Y5_R2FR_4742_FINITE_BOUND_LAW.csv", "FB4742_0_multiplier_amplitude", "amplitude law"),
    ("SRC4743_6_4741_boundary", SOURCE_DIR / "P8_Y5_R2FR_4741_BOUNDARY_READOUT_CERTIFICATE.csv", "BND4741_0_adjoint_boundary", "boundary certificate"),
    ("SRC4743_7_4741_zero_modes", SOURCE_DIR / "P8_Y5_R2FR_4741_ZERO_MODE_LEDGER.csv", "ZM4741_0_killing", "zero-mode families"),
    ("SRC4743_8_4741_matter", SOURCE_DIR / "P8_Y5_R2FR_4741_MATTER_GR_PRESERVATION_CHECK.csv", "MGR4741_3_failure_condition", "matter erasure firewall"),
    ("SRC4743_9_4138_boundary", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv", "TF4138_5_boundary_improvement", "boundary silence precedent"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    KERNEL_KILL_THEOREM_CSV,
    BOUNDARY_CONTRACT_CSV,
    ZERO_MODE_TEST_CSV,
    CZEROMODE_BOUND_CSV,
    GAP_PROTOCOL_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def kernel_kill_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "KKT4743_0_kernel_membership",
            "m in ker(D_adj) means D_adj m=0 on W_loc",
            "Starts from the exact leftover obstruction in 4742.",
            "DEFINITION",
        ),
        (
            "KKT4743_1_trace_map",
            "gamma_boundary m := m|partial W_loc",
            "A boundary trace is the minimal parent-owned datum needed to test the kernel.",
            "TRACE_DEFINED",
        ),
        (
            "KKT4743_2_unique_continuation_kill",
            "D_adj m=0 and gamma_boundary m=0 and UCP(D_adj,W_loc) => m=0",
            "This is the clean kernel-kill theorem: zero trace plus unique continuation kills Pi_0 m.",
            "THEOREM_CONDITIONAL",
        ),
        (
            "KKT4743_3_quotient_kill",
            "Pi_0 m = Pi_phys Pi_0 m + Pi_gauge Pi_0 m; parent quotient requires Pi_gauge Pi_0 m=0",
            "Gauge/representative zero modes are killed only by explicit quotient ownership, not by wishful projection.",
            "QUOTIENT_CONDITIONAL",
        ),
        (
            "KKT4743_4_kernel_bound",
            "||Pi_0 m|| <= C_trace||gamma_boundary m|| + C_q||Pi_gauge Pi_0 m|| + C_phys||Pi_phys Pi_0 m||",
            "If exact killing fails, the kernel obstruction becomes a bounded source row.",
            "FINITE_BOUND_DERIVED",
        ),
        (
            "KKT4743_5_exact_zero_branch",
            "gamma_boundary m=0, Pi_gauge Pi_0 m=0, Pi_phys Pi_0 m=0 => C_zeroMode=0",
            "This closes the 4742 exact zero branch only if the parent owns all three inputs.",
            "EXACT_BRANCH_CONDITIONAL_UNSIGNED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, formula, meaning, status in specs
    ]


def boundary_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BTC4743_0_boundary_trace", "gamma_boundary m=0", "multiplier trace vanishes on the local collar boundary", "PARENT_CONTRACT_REQUIRED"),
        ("BTC4743_1_boundary_flux", "B_adj[m]=0", "integration-by-parts flux/corner term vanishes", "PARENT_CONTRACT_REQUIRED"),
        ("BTC4743_2_fixed_collar", "D_v(partial W_loc)=0", "local collar is fixed before vertical variation/readout", "PARENT_CONTRACT_REQUIRED"),
        ("BTC4743_3_fixed_domain", "D_v Dom(D_adj)=0", "operator domain is fixed under the transition variation", "PARENT_CONTRACT_REQUIRED"),
        ("BTC4743_4_compact_support", "supp(m) compact in interior(W_loc)", "strong sufficient condition for trace and flux silence", "OPTIONAL_STRONG_ROUTE"),
        ("BTC4743_5_topological_boundary", "delta_g S_boundary=0 in bulk(W_loc)", "allowed boundary/topological owner contributes no local stress", "OPTIONAL_STRONG_ROUTE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, condition, meaning, status in specs
    ]


def zero_mode_family_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZMF4743_0_killing", "Killing/vector mode", "killed if boundary trace is zero on an open collar boundary and UCP holds", "UNSIGNED_BUT_TESTABLE"),
        ("ZMF4743_1_conformal", "conformal-Killing mode", "killed by fixed scale/quotient representative plus zero boundary trace", "UNSIGNED_BUT_TESTABLE"),
        ("ZMF4743_2_harmonic_scalar", "harmonic scalar mode", "killed by Dirichlet scalar trace or zero-mean plus fixed boundary data", "UNSIGNED_BUT_TESTABLE"),
        ("ZMF4743_3_TT", "TT/superpotential mode", "killed only if TT owner is boundary/topological or explicitly projected from local response", "UNSIGNED_BUT_TESTABLE"),
        ("ZMF4743_4_green", "Green inverse kernel", "killed by fixed inverse on kernel-orthogonal subspace", "UNSIGNED_BUT_TESTABLE"),
        ("ZMF4743_5_corner", "corner/edge mode", "killed by no-corner boundary contract; otherwise contributes to C_boundary", "UNSIGNED_BUT_TESTABLE"),
        ("ZMF4743_6_physical_kernel", "physical kernel mode", "cannot be killed by gauge; must be bounded or shown absent by spectrum", "FINITE_SOURCE_IF_PRESENT"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "family_id": family_id,
            "mode_family": mode_family,
            "kill_condition": kill_condition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for family_id, mode_family, kill_condition, status in specs
    ]


def czeromode_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CZB4743_0_definition",
            "C_zeroMode := ||Pi_0 m||/a_ref",
            "dimensionless",
            "Defines the first finite residual if the kernel is not killed.",
        ),
        (
            "CZB4743_1_trace_bound",
            "C_zeroMode <= (C_trace/a_ref)||gamma_boundary m|| + (C_q/a_ref)||Pi_gauge Pi_0 m|| + (C_phys/a_ref)||Pi_phys Pi_0 m||",
            "dimensionless",
            "Derived source law for kernel leakage.",
        ),
        (
            "CZB4743_2_exact_trace_case",
            "gamma_boundary m=0 and Pi_gauge Pi_0 m=0 and Pi_phys Pi_0 m=0 => C_zeroMode=0",
            "dimensionless",
            "Exact kernel kill condition.",
        ),
        (
            "CZB4743_3_amplitude_insert",
            "A_m <= sqrt(C_zeroMode^2 + (C_Dadj^2 + C_boundary)/lambda_1^adj)",
            "dimensionless",
            "Feeds the 4743 kernel result back into the 4742 multiplier amplitude law.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "formula": formula,
            "units": units,
            "meaning": meaning,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, formula, units, meaning in specs
    ]


def gap_protocol_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GAP4743_0_principal_symbol", "compute sigma(D_adj)(x,k)", "show injective symbol on kernel-orthogonal sector", "MISSING_OPERATOR_COMPONENTS"),
        ("GAP4743_1_boundary_condition", "choose parent-owned Dirichlet/compact-support/topological boundary class", "make L_adj self-adjoint/nonnegative", "MISSING_PARENT_BOUNDARY_DATA"),
        ("GAP4743_2_gap_definition", "lambda_1^adj=first positive eigenvalue of D_adj^*D_adj", "source numeric/symbolic lower bound after domain is fixed", "MISSING_DOMAIN"),
        ("GAP4743_3_toy_runner", "toy collar eigenvalue smoke run", "optional sanity check only, not a claim", "SAFE_AFTER_SYMBOLIC_SETUP"),
        ("GAP4743_4_claim_gate", "lambda_1^adj>0 plus C_zeroMode=0 plus C_boundary=0", "required before exact local silence promotion", "CLOSED_UNSIGNED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gap_id": gap_id,
            "step": step,
            "purpose": purpose,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gap_id, step, purpose, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4743_0_parent_boundary_trace", "find or write parent boundary trace contract for m", "best_next_route", "would kill Pi_0 m and B_adj together if signed"),
        ("ROUTE4743_1_CzeroMode_source", "carry C_zeroMode as finite source row", "fallback_next_route", "keeps route scoreable if parent boundary data is absent"),
        ("ROUTE4743_2_gap_runner", "build toy adjoint spectral-gap runner", "parallel_smoke_route", "useful only after operator/domain components are fixed"),
        ("ROUTE4743_3_claim_now", "claim local-GR pass", "rejected", "boundary trace, quotient projection and gap are unsigned"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "reason_or_next_requirement": requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, requirement in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4743_0_sources", "All cited 4743 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4743_1_kernel_theorem", "Kernel-kill theorem written with boundary trace and UCP clauses.", "conditional_pass", False),
        ("GATE4743_2_boundary_contract", "Need parent-owned gamma_boundary m=0 and B_adj=0.", "closed_unsigned", False),
        ("GATE4743_3_quotient_contract", "Need quotient/gauge projection ownership.", "closed_unsigned", False),
        ("GATE4743_4_CzeroMode", "Need C_zeroMode=0 or finite sourced bound.", "closed_unsigned", False),
        ("GATE4743_5_gap", "Need lambda_1^adj source after domain is fixed.", "closed_unsigned", False),
        ("GATE4743_6_no_claim", "No local-GR, Newton, PPN, R10, WEP, clock or orbital claim from 4743.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4743_0_no_kernel_vanish_by_assertion", "Do not set Pi_0 m=0 unless boundary trace, quotient, or spectrum kills it."),
        ("FW4743_1_no_unique_continuation_without_operator", "Do not invoke UCP until D_adj principal symbol/domain are fixed."),
        ("FW4743_2_no_trace_without_parent", "Do not impose gamma_boundary m=0 unless the parent action/collar owns it."),
        ("FW4743_3_no_physical_kernel_gauge_kill", "Gauge projection cannot remove physical kernel modes; bound them if present."),
        ("FW4743_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "4743 derives the kernel-projection kill test: D_adj m=0 plus zero boundary trace plus unique continuation kills Pi_0 m, with quotient and physical-kernel terms carried explicitly. Because parent boundary/quotient data are not yet signed, C_zeroMode remains staged as the first finite source value.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4743_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4743_1_science_verdict",
            "status": "kernel_kill_test_derived_boundary_and_quotient_unsigned",
            "detail": "Pi_0 m is no longer vague: it is killed by parent boundary/quotient data or carried as C_zeroMode.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4743 shows the shortest exact route is a parent-owned zero boundary trace/quotient contract; absent that, C_zeroMode must be sourced.",
            "preferred_route": "Search/write the parent boundary trace contract for multipliers on the fixed local collar.",
            "fallback_route": "Create a C_zeroMode source runner and, after domain fixation, a toy adjoint gap smoke runner.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    theorem: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    families: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gap: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4743 Y5 R2FR: Kernel Projection Boundary Data Kill Test Or Adjoint Gap Source Value

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint attacks `Pi_0 m` directly.
- The kernel kill theorem is:

```text
m in ker(D_adj)
gamma_boundary m = 0
UCP(D_adj,W_loc)
-----------------
m=0
```

- The quotient-safe version also requires gauge/representative kernel modes to be parent-projected:

```text
Pi_0 m = Pi_phys Pi_0 m + Pi_gauge Pi_0 m
Pi_gauge Pi_0 m = 0
Pi_phys Pi_0 m = 0 or bounded
```

- Therefore `C_zeroMode=0` is not asserted; it is reduced to boundary trace, quotient projection, and physical-kernel tests.
- If those are not parent-signed, `C_zeroMode` remains the first finite source value.

## Kernel Kill Theorem

{bullet(theorem, "theorem_id", "formula")}

## Boundary Trace Contract

{bullet(boundary, "contract_id", "condition")}

## Zero-Mode Family Test

{bullet(families, "family_id", "mode_family")}

## C_zeroMode Bound Law

{bullet(bounds, "bound_id", "formula")}

## Adjoint Gap Source Protocol

{bullet(gap, "gap_id", "step")}

## Route Matrix

{bullet(routes, "route_id", "route")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 759 PPC4161: Kernel Projection Boundary Data Kill Test Or Adjoint Gap Source Value

Generated: `{timestamp}`

## Kernel Projection Result

4743 narrows the 4742 kernel obstruction to a boundary/quotient theorem:

```text
D_adj m=0,
gamma_boundary m=0,
UCP(D_adj,W_loc)
=> m=0.
```

If the kernel splits into physical and gauge parts, the safe bound is:

```text
C_zeroMode <= (C_trace/a_ref)||gamma_boundary m||
            + (C_q/a_ref)||Pi_gauge Pi_0 m||
            + (C_phys/a_ref)||Pi_phys Pi_0 m||.
```

This means the local-zero route is not dead, but it now needs a parent-owned boundary trace/quotient contract. Without that contract, `C_zeroMode` is carried forward as a finite source row.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4743 derives the kernel kill test: `D_adj m=0`, `gamma_boundary m=0`, and `UCP(D_adj,W_loc)` imply `m=0`.
- The quotient-safe obstruction is split into `Pi_gauge Pi_0 m` and `Pi_phys Pi_0 m`.
- `C_zeroMode` is now bounded by boundary trace, quotient projection, and physical-kernel amplitudes.
- Exact local silence therefore needs a parent-owned boundary trace/quotient contract; otherwise `C_zeroMode` is the first finite source value.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4743 local packet update: the kernel projection obstruction has a kill theorem and a finite fallback law. The next step is parent boundary trace ownership or a C_zeroMode source runner.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4743-Y5-R2FR-kernel-projection-boundary-data-kill-test-or-adjoint-gap-source-value.md`

## Decision

`{DECISION}`

## What moved forward

- Derived the kernel-kill test: `D_adj m=0`, `gamma_boundary m=0`, and `UCP(D_adj,W_loc)` imply `m=0`.
- Split `Pi_0 m` into gauge and physical kernel pieces so quotient projection cannot hide physical modes.
- Derived a `C_zeroMode` bound from boundary trace, quotient projection, and physical-kernel amplitudes.
- Kept the exact branch unsigned until parent boundary trace/quotient data are sourced.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_newton_bridge",
        "4743 derives a kernel-projection kill test and C_zeroMode bound law for the adjoint multiplier obstruction.",
        "Generated source register, kernel kill theorem, boundary trace contract, zero-mode family kill test, CzeroMode bound law, adjoint gap protocol, route matrix, gates, firewalls, decision, status, next target and validation.",
        "kernel_projection_kill_test_boundary_quotient_unsigned_nonclaim",
        NEXT_TARGET,
        "Imposing zero boundary trace or quotient projection without parent ownership, or treating physical kernel modes as gauge.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need parent boundary trace/quotient contract, UCP/operator data, lambda_1^adj, C_zeroMode=0 or finite source bound.",
        "Kernel projection boundary data kill test or adjoint gap source value",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    families: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gap: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4743_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4743_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4743_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4743_2_kernel_theorem", "kernel theorem contains boundary trace and UCP implication", any("gamma_boundary m=0" in row["formula"] and "UCP" in row["formula"] for row in theorem), str(KERNEL_KILL_THEOREM_CSV)))
    checks.append(("VAL4743_3_quotient_split", "kernel theorem splits gauge and physical pieces", any("Pi_phys" in row["formula"] and "Pi_gauge" in row["formula"] for row in theorem), str(KERNEL_KILL_THEOREM_CSV)))
    checks.append(("VAL4743_4_boundary_contract", "boundary contract includes gamma trace and B_adj", any("gamma_boundary" in row["condition"] for row in boundary) and any("B_adj" in row["condition"] for row in boundary), str(BOUNDARY_CONTRACT_CSV)))
    checks.append(("VAL4743_5_family_tests", "zero-mode family test includes physical kernel fallback", any(row["status"] == "FINITE_SOURCE_IF_PRESENT" for row in families), str(ZERO_MODE_TEST_CSV)))
    checks.append(("VAL4743_6_CzeroMode_bound", "C_zeroMode bound law exists", any("C_zeroMode <=" in row["formula"] for row in bounds), str(CZEROMODE_BOUND_CSV)))
    checks.append(("VAL4743_7_gap_protocol", "gap protocol blocks claim until domain/gap source exists", any(row["status"] == "CLOSED_UNSIGNED" for row in gap), str(GAP_PROTOCOL_CSV)))
    checks.append(("VAL4743_8_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4743_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4743_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4743_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4743_12_claim_row", "claim row L-585 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4743_13_resume", "resume points from 4743 to 4744", "4743-Y5" in resume_text and "4744-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4743_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4743_OVERALL",
            "check": "all 4743 local generation and nonclaim checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    theorem = kernel_kill_theorem_rows(timestamp)
    boundary = boundary_contract_rows(timestamp)
    families = zero_mode_family_rows(timestamp)
    bounds = czeromode_bound_rows(timestamp)
    gap = gap_protocol_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(KERNEL_KILL_THEOREM_CSV, theorem)
    write_csv(BOUNDARY_CONTRACT_CSV, boundary)
    write_csv(ZERO_MODE_TEST_CSV, families)
    write_csv(CZEROMODE_BOUND_CSV, bounds)
    write_csv(GAP_PROTOCOL_CSV, gap)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, theorem, boundary, families, bounds, gap, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, boundary, families, bounds, gap, gates, timestamp))


if __name__ == "__main__":
    main()
