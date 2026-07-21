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

CHECKPOINT = "4744"
CLAIM_ID = "L-586"
MARKER = "PPC4161_PARENT_BOUNDARY_TRACE_CONTRACT_OR_CZEROMODE_SOURCE_RUNNER_4744"
PACKET_MARKER = "PPC4161_PACKET_PARENT_BOUNDARY_TRACE_CONTRACT_OR_CZEROMODE_SOURCE_RUNNER_4744"
DECISION = "PARENT_ADMISSIBLE_MULTIPLIER_BOUNDARY_TRACE_CONTRACT_WRITTEN_CZEROMODE_REDUCED_TO_UCP_ELLIPTICITY_AND_PHYSICAL_KERNEL_NONCLAIM"
NEXT_TARGET = "4745-Y5-R2FR-adjoint-principal-symbol-UCP-ellipticity-gate-or-CzeroMode-bound-runner.md"

DOC_PATH = POST / "4744-Y5-R2FR-parent-boundary-trace-contract-or-CzeroMode-source-runner.md"
FORMAL_PATH = FORMAL / "760-PPC4161-parent-boundary-trace-contract-or-CzeroMode-source-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_SOURCE_REGISTER.csv"
PARENT_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_PARENT_BOUNDARY_TRACE_CONTRACT.csv"
ADMISSIBLE_SPACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_ADMISSIBLE_MULTIPLIER_SPACE.csv"
BOUNDARY_FLUX_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_BOUNDARY_FLUX_AUDIT.csv"
CZEROMODE_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_CZEROMODE_SOURCE_RUNNER.csv"
EXACT_BRANCH_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_EXACT_BRANCH_AUDIT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4744_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4744_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4744_0_4743_doc", POST / "4743-Y5-R2FR-kernel-projection-boundary-data-kill-test-or-adjoint-gap-source-value.md", "find or write parent boundary trace contract for m", "4744 target"),
    ("SRC4744_1_4743_formal", FORMAL / "759-PPC4161-kernel-projection-boundary-data-kill-test-or-adjoint-gap-source-value.md", "C_zeroMode <= (C_trace/a_ref)||gamma_boundary m||", "formal CzeroMode bound"),
    ("SRC4744_2_4743_theorem", SOURCE_DIR / "P8_Y5_R2FR_4743_KERNEL_KILL_THEOREM.csv", "KKT4743_2_unique_continuation_kill", "kernel kill theorem"),
    ("SRC4744_3_4743_boundary", SOURCE_DIR / "P8_Y5_R2FR_4743_BOUNDARY_TRACE_CONTRACT.csv", "BTC4743_0_boundary_trace", "boundary trace contract"),
    ("SRC4744_4_4743_czero", SOURCE_DIR / "P8_Y5_R2FR_4743_CZEROMODE_BOUND_LAW.csv", "CZB4743_1_trace_bound", "CzeroMode bound law"),
    ("SRC4744_5_4743_gap", SOURCE_DIR / "P8_Y5_R2FR_4743_ADJOINT_GAP_SOURCE_PROTOCOL.csv", "GAP4743_4_claim_gate", "gap claim gate"),
    ("SRC4744_6_4742_proof", SOURCE_DIR / "P8_Y5_R2FR_4742_SPECTRAL_GAP_COERCIVITY_PROOF.csv", "PROOF4742_4_exact_zero", "exact zero proof"),
    ("SRC4744_7_4741_boundary", SOURCE_DIR / "P8_Y5_R2FR_4741_BOUNDARY_READOUT_CERTIFICATE.csv", "BND4741_0_adjoint_boundary", "adjoint boundary certificate"),
    ("SRC4744_8_4740_variation", SOURCE_DIR / "P8_Y5_R2FR_4740_METRIC_VARIATION_AUDIT.csv", "VAR4740_5_on_shell_metric_null", "on-shell metric nullity"),
    ("SRC4744_9_4138_boundary", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv", "TF4138_5_boundary_improvement", "boundary silence precedent"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    PARENT_CONTRACT_CSV,
    ADMISSIBLE_SPACE_CSV,
    BOUNDARY_FLUX_AUDIT_CSV,
    CZEROMODE_RUNNER_CSV,
    EXACT_BRANCH_AUDIT_CSV,
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


def parent_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PBC4744_0_contract_statement",
            "m=(lambda,eta,rho,xi,chi) is an auxiliary transition-owner multiplier field in M_adm(W_loc)",
            "The parent action owns multipliers as transition-owner auxiliaries, not as ordinary matter fields.",
            "CONTRACT_WRITTEN",
        ),
        (
            "PBC4744_1_admissible_class",
            "M_adm(W_loc)=H^1_0(W_loc,E_m) cap Q_perp cap M_phys_allowed",
            "Dirichlet trace zero is part of the variational domain fixed before scoring.",
            "PARENT_DOMAIN_CONTRACT_CONDITIONAL",
        ),
        (
            "PBC4744_2_boundary_trace",
            "gamma_boundary m=0 follows from m in H^1_0(W_loc,E_m)",
            "This signs the boundary-trace clause if the parent domain contract is accepted.",
            "TRACE_ZERO_CONDITIONAL_PASS",
        ),
        (
            "PBC4744_3_quotient_projection",
            "Q_perp requires Pi_gauge Pi_0 m=0",
            "Gauge/representative kernel leakage is excluded only by a declared quotient subspace.",
            "QUOTIENT_CONDITIONAL_PASS",
        ),
        (
            "PBC4744_4_physical_kernel",
            "M_phys_allowed must either exclude Pi_phys Pi_0 m or carry it as C_phys",
            "Physical zero modes cannot be deleted as gauge; this is the remaining kernel obstruction.",
            "PHYSICAL_KERNEL_UNSIGNED",
        ),
        (
            "PBC4744_5_non_posthoc",
            "M_adm and W_loc are fixed before any PPN/R10/clock/orbital scoring",
            "Prevents the boundary condition from being tuned after seeing local-test residuals.",
            "ANTI_SMUGGLING_GATE",
        ),
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


def admissible_space_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ADM4744_0_multiplier_bundle", "E_m = T*W_loc plus scalar plus symmetric-tensor multiplier slots", "bundle for lambda, eta, rho, xi, chi", "DEFINED_SYMBOLIC"),
        ("ADM4744_1_trace_domain", "H^1_0(W_loc,E_m)", "zero trace by Sobolev closure of compactly supported smooth sections", "TRACE_ZERO_BY_DOMAIN"),
        ("ADM4744_2_compact_support_route", "C_c^\u221e(int W_loc,E_m) dense in H^1_0", "strong support route for boundary silence", "STRONG_ROUTE_AVAILABLE"),
        ("ADM4744_3_quotient_subspace", "Q_perp = ker(Pi_gauge Pi_0)", "removes representative/gauge zero modes from admissible owner multipliers", "QUOTIENT_ROUTE_CONDITIONAL"),
        ("ADM4744_4_physical_subspace", "M_phys_allowed", "physical kernel modes need independent exclusion or finite bound", "UNSIGNED"),
        ("ADM4744_5_matter_separation", "M_adm excludes ordinary matter fields Psi", "boundary contract cannot erase ordinary matter stress-energy", "FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "space_id": space_id,
            "definition": definition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for space_id, definition, meaning, status in specs
    ]


def boundary_flux_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BFA4744_0_green_identity",
            "int_W <D_adj m,n>-<m,D_adj^* n> = int_partialW <gamma m, B_n n>",
            "The boundary form is explicit; it is not thrown away silently.",
            "IDENTITY_SCHEMATIC",
        ),
        (
            "BFA4744_1_dirichlet_flux",
            "gamma_boundary m=0 and gamma_boundary n=0 => B_adj[m,n]=0 for Dirichlet-type boundary forms",
            "Dirichlet admissible multipliers kill the standard boundary flux.",
            "CONDITIONAL_PASS",
        ),
        (
            "BFA4744_2_derivative_boundary_warning",
            "if B_adj contains normal-derivative-only terms not multiplied by gamma m, H^1_0 is insufficient",
            "Higher-derivative owner blocks may need H^2_0 or explicit normal-trace data.",
            "WARNING_CARRY_CBOUNDARY",
        ),
        (
            "BFA4744_3_safe_upgrade",
            "M_adm_strong=H^2_0 or compact-support collar => gamma m=0 and gamma_nabla m=0",
            "Strong admissible space kills both field and normal derivative boundary terms.",
            "STRONG_ROUTE_CONDITIONAL",
        ),
        (
            "BFA4744_4_result",
            "C_boundary=0 only for Dirichlet-form or strong compact-support route; otherwise source C_boundary",
            "Boundary silence is partly advanced but not overclaimed.",
            "NONCLAIM_BOUNDARY_RESULT",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, formula, meaning, status in specs
    ]


def czeromode_runner_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CZR4744_0_trace_zero",
            "C_trace_norm",
            "0 if m in H^1_0; MISSING if parent domain not accepted",
            "CONDITIONAL_ZERO",
        ),
        (
            "CZR4744_1_gauge_zero",
            "C_gauge_kernel",
            "0 if Q_perp=ker(Pi_gauge Pi_0) is parent-owned; otherwise MISSING",
            "CONDITIONAL_ZERO",
        ),
        (
            "CZR4744_2_physical_kernel",
            "C_phys_kernel",
            "MISSING_SOURCE_VALUE unless physical kernel absence is proved",
            "MISSING_SOURCE_VALUE",
        ),
        (
            "CZR4744_3_trace_constant",
            "C_trace",
            "MISSING_OPERATOR_CONSTANT until trace estimate is sourced",
            "MISSING_SOURCE_VALUE",
        ),
        (
            "CZR4744_4_kernel_bound",
            "C_zeroMode <= C_trace*C_trace_norm + C_q*C_gauge_kernel + C_phys*C_phys_kernel",
            "score-ready only after physical kernel and constants are sourced",
            "NOT_SCORE_READY",
        ),
        (
            "CZR4744_5_exact_condition",
            "C_trace_norm=0, C_gauge_kernel=0, C_phys_kernel=0 => C_zeroMode=0",
            "exact if parent domain plus physical-kernel absence are both signed",
            "EXACT_CONDITIONAL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": runner_id,
            "quantity": quantity,
            "value_or_formula": value_or_formula,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for runner_id, quantity, value_or_formula, status in specs
    ]


def exact_branch_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("EX4744_0_trace", "gamma_boundary m=0", "conditional_pass_if_parent_domain_accepted", "PBC4744_1"),
        ("EX4744_1_gauge", "Pi_gauge Pi_0 m=0", "conditional_pass_if_Q_perp_accepted", "PBC4744_3"),
        ("EX4744_2_physical", "Pi_phys Pi_0 m=0", "closed_unsigned", "PBC4744_4"),
        ("EX4744_3_UCP", "UCP(D_adj,W_loc)", "closed_unsigned", "4745 principal-symbol target"),
        ("EX4744_4_gap", "lambda_1^adj>0", "closed_unsigned", "4745 spectral target"),
        ("EX4744_5_boundary_flux", "B_adj=0", "conditional_or_closed_by_derivative_order", "BFA4744_2"),
        ("EX4744_6_matter", "delta S_matter/delta g != 0", "firewall_open", "ordinary matter not in M_adm"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": branch_id,
            "condition": condition,
            "status": status,
            "evidence_or_next": evidence,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for branch_id, condition, status, evidence in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4744_0_principal_symbol", "derive D_adj principal symbol and UCP/ellipticity gate", "best_next_route", "needed to convert boundary trace into actual Pi_0 kill"),
        ("ROUTE4744_1_physical_kernel", "prove absence of Pi_phys Pi_0 m", "parallel_exact_route", "needed for C_zeroMode=0"),
        ("ROUTE4744_2_CzeroMode_runner", "fill C_phys_kernel/C_trace constants for finite C_zeroMode", "fallback_route", "keeps local branch scoreable if physical kernel remains"),
        ("ROUTE4744_3_claim_now", "claim local-GR pass", "rejected", "UCP, gap and physical kernel are not signed"),
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
        ("GATE4744_0_sources", "All cited 4744 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4744_1_boundary_trace", "Parent admissible multiplier boundary trace contract is written.", "conditional_pass", False),
        ("GATE4744_2_flux", "Boundary flux vanishes only for Dirichlet-form or strong compact-support route.", "conditional_open", False),
        ("GATE4744_3_physical_kernel", "Physical kernel absence remains unsigned.", "closed_unsigned", False),
        ("GATE4744_4_UCP_gap", "UCP/ellipticity/spectral gap remain unsigned.", "closed_unsigned", False),
        ("GATE4744_5_CzeroMode", "C_zeroMode remains nonclaim until physical kernel and constants are sourced or proved zero.", "closed_unsigned", False),
        ("GATE4744_6_no_claim", "No local-GR, Newton, PPN, R10, WEP, clock or orbital claim from 4744.", "closed_firewall", False),
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
        ("FW4744_0_no_posthoc_boundary", "Do not impose H^1_0 after seeing local-test residuals; it must be parent-domain data."),
        ("FW4744_1_no_physical_kernel_deletion", "Gauge quotient cannot delete physical zero modes."),
        ("FW4744_2_no_boundary_flux_cheat", "H^1_0 kills standard trace terms, not every possible higher-derivative normal flux."),
        ("FW4744_3_no_matter_boundary_erasure", "Multiplier boundary conditions do not apply to ordinary matter fields."),
        ("FW4744_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
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
            "summary": "4744 writes a parent admissible-multiplier boundary trace contract: m in H^1_0(W_loc,E_m) cap Q_perp gives gamma_boundary m=0 and gauge-kernel removal if accepted as parent domain data before scoring. Full C_zeroMode=0 still needs physical-kernel absence plus UCP/ellipticity/gap; otherwise C_zeroMode remains a finite source runner.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4744_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4744_1_science_verdict",
            "status": "boundary_trace_contract_written_exact_branch_still_needs_UCP_and_physical_kernel",
            "detail": "Boundary trace is now a parent-domain contract rather than a handwave; exact local silence still waits on UCP/ellipticity/gap and physical-kernel absence.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4744 supplies a parent boundary trace/quotient contract, but C_zeroMode=0 still needs UCP/ellipticity/gap and physical-kernel absence.",
            "preferred_route": "Derive the adjoint principal symbol and UCP/ellipticity gate for D_adj on the fixed collar.",
            "fallback_route": "Keep C_zeroMode finite by sourcing C_phys_kernel and trace constants.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    parent: list[dict[str, Any]],
    spaces: list[dict[str, Any]],
    flux: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    exact: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4744 Y5 R2FR: Parent Boundary Trace Contract Or CzeroMode Source Runner

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint writes the parent-domain route for the multiplier boundary trace:

```text
M_adm(W_loc)=H^1_0(W_loc,E_m) cap Q_perp cap M_phys_allowed
m=(lambda,eta,rho,xi,chi) in M_adm
=> gamma_boundary m=0
```

- This is legitimate only if `M_adm` and `W_loc` are fixed in the parent variational problem before any local-test scoring.
- The quotient piece `Q_perp` can remove gauge/representative kernel modes.
- Physical kernel modes are not gauge: they must be proved absent or carried as `C_phys_kernel`.
- Therefore `C_zeroMode=0` is advanced but not claimed.

## Parent Boundary Contract

{bullet(parent, "contract_id", "condition")}

## Admissible Multiplier Space

{bullet(spaces, "space_id", "definition")}

## Boundary Flux Audit

{bullet(flux, "audit_id", "formula")}

## CzeroMode Source Runner

{bullet(runner, "runner_id", "quantity")}

## Exact Branch Audit

{bullet(exact, "branch_id", "condition")}

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

    formal = f"""# 760 PPC4161: Parent Boundary Trace Contract Or CzeroMode Source Runner

Generated: `{timestamp}`

## Boundary Trace Contract

4744 writes the admissible multiplier domain:

```text
M_adm(W_loc)=H^1_0(W_loc,E_m) cap Q_perp cap M_phys_allowed.
```

For `m in M_adm`, the parent-domain condition gives:

```text
gamma_boundary m=0.
```

This can kill the boundary trace part of the 4743 kernel obstruction without post-hoc tuning, provided the domain is fixed before scoring. It also removes gauge/representative kernel leakage if `Q_perp=ker(Pi_gauge Pi_0)` is parent-owned.

## Remaining Exact-Branch Inputs

- `Pi_phys Pi_0 m=0` or a sourced `C_phys_kernel`.
- `UCP(D_adj,W_loc)` from the actual adjoint principal symbol.
- `lambda_1^adj>0` for the fixed domain.
- `B_adj=0` or a higher-derivative boundary flux bound.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4744 writes the admissible multiplier domain `M_adm(W_loc)=H^1_0(W_loc,E_m) cap Q_perp cap M_phys_allowed`.
- This parent-domain contract gives `gamma_boundary m=0` and can remove gauge kernel leakage through `Q_perp`.
- Physical kernel modes remain real: they require absence proof or `C_phys_kernel`.
- Boundary flux is conditionally silent for Dirichlet-form/compact-support routes, otherwise `C_boundary` remains.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4744 local packet update: boundary trace is no longer a vague wish; it is a parent-domain contract. The next proof step is adjoint principal symbol/UCP/ellipticity or a finite `C_zeroMode` bound.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4744-Y5-R2FR-parent-boundary-trace-contract-or-CzeroMode-source-runner.md`

## Decision

`{DECISION}`

## What moved forward

- Wrote the admissible multiplier boundary-trace contract `M_adm=H^1_0(W_loc,E_m) cap Q_perp cap M_phys_allowed`.
- `gamma_boundary m=0` is now parent-domain conditional rather than assumed after the fact.
- Gauge kernel leakage can be removed by `Q_perp`, but physical kernel modes must be proved absent or carried as `C_phys_kernel`.
- Boundary flux is conditionally silent for Dirichlet-form or compact-support routes; higher-derivative normal flux still needs `C_boundary`.

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
        "4744 writes a parent admissible-multiplier boundary trace contract and CzeroMode source runner for the local-GR transition branch.",
        "Generated source register, parent boundary trace contract, admissible multiplier space, boundary flux audit, CzeroMode source runner, exact branch audit, route matrix, gates, firewalls, decision, status, next target and validation.",
        "parent_boundary_trace_contract_written_UCP_physical_kernel_unsigned_nonclaim",
        NEXT_TARGET,
        "Treating an admissible-domain boundary condition as a physical proof of local GR before UCP, gap and physical-kernel absence are established.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need adjoint principal symbol/UCP, lambda_1^adj, physical kernel absence or finite C_phys_kernel, and boundary flux order check.",
        "Parent boundary trace contract or CzeroMode source runner",
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
    parent: list[dict[str, Any]],
    spaces: list[dict[str, Any]],
    flux: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    exact: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4744_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4744_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4744_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4744_2_parent_contract", "parent contract defines M_adm and gamma trace", any("M_adm" in row["condition"] for row in parent) and any("gamma_boundary m=0" in row["condition"] for row in parent), str(PARENT_CONTRACT_CSV)))
    checks.append(("VAL4744_3_admissible_space", "admissible space includes H^1_0, Q_perp and matter separation", any("H^1_0" in row["definition"] for row in spaces) and any("Q_perp" in row["definition"] for row in spaces) and any("ordinary matter" in row["meaning"] for row in spaces), str(ADMISSIBLE_SPACE_CSV)))
    checks.append(("VAL4744_4_boundary_flux", "boundary flux audit carries derivative warning", any(row["status"] == "WARNING_CARRY_CBOUNDARY" for row in flux), str(BOUNDARY_FLUX_AUDIT_CSV)))
    checks.append(("VAL4744_5_CzeroMode_runner", "CzeroMode runner keeps physical kernel missing", any(row["quantity"] == "C_phys_kernel" and row["status"] == "MISSING_SOURCE_VALUE" for row in runner), str(CZEROMODE_RUNNER_CSV)))
    checks.append(("VAL4744_6_exact_branch", "exact branch leaves UCP/gap/physical kernel unsigned", all(any(token in row["condition"] and row["status"] == "closed_unsigned" for row in exact) for token in ["Pi_phys", "UCP", "lambda_1^adj"]), str(EXACT_BRANCH_AUDIT_CSV)))
    checks.append(("VAL4744_7_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4744_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4744_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4744_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4744_11_claim_row", "claim row L-586 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4744_12_resume", "resume points from 4744 to 4745", "4744-Y5" in resume_text and "4745-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4744_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4744_OVERALL",
            "check": "all 4744 local generation and nonclaim checks pass",
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
    parent = parent_contract_rows(timestamp)
    spaces = admissible_space_rows(timestamp)
    flux = boundary_flux_rows(timestamp)
    runner = czeromode_runner_rows(timestamp)
    exact = exact_branch_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(PARENT_CONTRACT_CSV, parent)
    write_csv(ADMISSIBLE_SPACE_CSV, spaces)
    write_csv(BOUNDARY_FLUX_AUDIT_CSV, flux)
    write_csv(CZEROMODE_RUNNER_CSV, runner)
    write_csv(EXACT_BRANCH_AUDIT_CSV, exact)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, parent, spaces, flux, runner, exact, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, parent, spaces, flux, runner, exact, gates, timestamp))


if __name__ == "__main__":
    main()
