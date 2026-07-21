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

CHECKPOINT = "4746"
CLAIM_ID = "L-588"
MARKER = "PPC4161_STATIC_PPN_ELLIPTIC_SLICE_GAP_PROOF_OR_LORENTZIAN_ENERGY_BOUND_4746"
PACKET_MARKER = "PPC4161_PACKET_STATIC_PPN_ELLIPTIC_SLICE_GAP_PROOF_OR_LORENTZIAN_ENERGY_BOUND_4746"
DECISION = "STATIC_LOCAL_TEST_GAP_BOUND_DERIVED_CONDITIONALLY_LORENTZIAN_ENERGY_BOUND_STAGED_FULL_OWNER_SYMBOLS_STILL_UNSIGNED"
NEXT_TARGET = "4747-Y5-R2FR-static-gap-constant-source-and-owner-symbol-completion.md"

DOC_PATH = POST / "4746-Y5-R2FR-static-PPN-elliptic-slice-gap-proof-or-lorentzian-energy-bound.md"
FORMAL_PATH = FORMAL / "762-PPC4161-static-PPN-elliptic-slice-gap-proof-or-lorentzian-energy-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_SOURCE_REGISTER.csv"
STATIC_OPERATOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_STATIC_OPERATOR_SETUP.csv"
STATIC_GAP_PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_STATIC_GAP_PROOF.csv"
STATIC_TEST_ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_STATIC_TEST_ARENA_MAPPING.csv"
LORENTZIAN_ENERGY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_LORENTZIAN_ENERGY_BOUND.csv"
OWNER_SYMBOL_COMPLETION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_OWNER_SYMBOL_COMPLETION_LEDGER.csv"
RESIDUAL_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_RESIDUAL_BOUND_LAW.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4746_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4746_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4746_0_4745_doc", POST / "4745-Y5-R2FR-adjoint-principal-symbol-UCP-ellipticity-gate-or-CzeroMode-bound-runner.md", "STATIC_PPN_ELLIPTIC_SLICE_ONLY", "4746 static fork handoff"),
    ("SRC4746_1_4745_formal", FORMAL / "761-PPC4161-adjoint-principal-symbol-UCP-ellipticity-gate-or-CzeroMode-bound-runner.md", "static spatial", "formal static branch"),
    ("SRC4746_2_4745_symbols", SOURCE_DIR / "P8_Y5_R2FR_4745_ADJOINT_PRINCIPAL_SYMBOL_DERIVATION.csv", "SYM4745_4_principal_symbols", "minimal symbol spine"),
    ("SRC4746_3_4745_DN", SOURCE_DIR / "P8_Y5_R2FR_4745_DN_ELLIPTICITY_UCP_GATE.csv", "DN4745_4_gap", "DN gap theorem gate"),
    ("SRC4746_4_4745_lorentzian", SOURCE_DIR / "P8_Y5_R2FR_4745_LORENTZIAN_CAUTION_AUDIT.csv", "LOR4745_2_hyperbolic_route", "Lorentzian energy fallback"),
    ("SRC4746_5_4745_kernel", SOURCE_DIR / "P8_Y5_R2FR_4745_PHYSICAL_KERNEL_AUDIT.csv", "PK4745_5_physical_bound", "physical kernel bound"),
    ("SRC4746_6_4745_czero", SOURCE_DIR / "P8_Y5_R2FR_4745_CZEROMODE_BOUND_RUNNER.csv", "CZG4745_2_finite_runner", "CzeroMode finite law"),
    ("SRC4746_7_4744_boundary", SOURCE_DIR / "P8_Y5_R2FR_4744_PARENT_BOUNDARY_TRACE_CONTRACT.csv", "PBC4744_1_admissible_class", "static domain contract"),
    ("SRC4746_8_4742_gap", SOURCE_DIR / "P8_Y5_R2FR_4742_SPECTRAL_GAP_COERCIVITY_PROOF.csv", "PROOF4742_1_spectral_gap", "spectral gap amplitude precedent"),
    ("SRC4746_9_4282_threshold", SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv", "PR4282_1_threshold_144", "transition threshold"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    STATIC_OPERATOR_CSV,
    STATIC_GAP_PROOF_CSV,
    STATIC_TEST_ARENA_CSV,
    LORENTZIAN_ENERGY_CSV,
    OWNER_SYMBOL_COMPLETION_CSV,
    RESIDUAL_BOUND_CSV,
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


def static_operator_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "STATOP4746_0_static_reduction",
            "STATIC_PPN_ELLIPTIC_SLICE_ONLY: W_loc -> Sigma_loc with Riemannian h_ij and parent-fixed lapse/shift/background fields",
            "Defines the arena where elliptic/UCP/gap logic is legal.",
            "STATIC_ROUTE_CONDITIONAL",
        ),
        (
            "STATOP4746_1_domain",
            "M_adm^stat=H^1_0(Sigma_loc,E_m) cap Q_perp cap M_phys_allowed",
            "Carries the 4744 boundary trace contract to the spatial collar.",
            "DOMAIN_CONDITIONAL",
        ),
        (
            "STATOP4746_2_operator",
            "D_stat := spatial/static reduction of D_adj with time derivatives removed or algebraically constrained before scoring",
            "This is not the full Lorentzian operator; it is the local-test operator.",
            "OPERATOR_DEFINED_CONDITIONALLY",
        ),
        (
            "STATOP4746_3_principal_symbol",
            "sigma_DN(D_stat)(x,p) = spatial part of sigma_DN(D_adj)(x,k) with p_i != 0",
            "The DN symbol test is performed on real nonzero spatial covectors.",
            "SYMBOL_TEST_DEFINED",
        ),
        (
            "STATOP4746_4_laplacian",
            "L_stat := D_stat^*D_stat on M_adm^stat",
            "Static gap theorem is applied to the nonnegative self-adjoint spatial operator.",
            "GAP_OPERATOR_DEFINED_CONDITIONALLY",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "operator_id": operator_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for operator_id, formula, meaning, status in specs
    ]


def static_gap_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "SGP4746_0_DN_elliptic_assumption",
            "ker sigma_DN(D_stat)(x,p) cap M_adm^stat = {0} for every p != 0",
            "This is the principal-symbol gate inherited from 4745.",
            "ASSUMPTION_TO_PROVE",
        ),
        (
            "SGP4746_1_Garding",
            "||m||_{H^s}^2 <= C_G(||D_stat m||_{L2}^2 + ||m||_{L2}^2) on Sigma_loc",
            "Elliptic estimate follows once the DN gate and boundary complementing conditions are signed.",
            "THEOREM_CONDITIONAL",
        ),
        (
            "SGP4746_2_Poincare",
            "||m||_{L2}^2 <= C_P L_loc^2 ||nabla_h m||_{L2}^2 for m in H^1_0",
            "The parent boundary trace gives a spatial Poincare inequality on the collar.",
            "THEOREM_CONDITIONAL",
        ),
        (
            "SGP4746_3_gap_bound",
            "lambda_1^stat >= c_DN/(C_P L_loc^2)",
            "This is the first explicit static gap lower-bound law.",
            "DERIVED_SYMBOLIC_BOUND",
        ),
        (
            "SGP4746_4_zero_kernel",
            "D_stat m=0 and gamma_boundary m=0 and C_phys_kernel=0 => m=0",
            "Static zero branch follows once physical kernels and full owner symbols are closed.",
            "EXACT_STATIC_BRANCH_CONDITIONAL",
        ),
        (
            "SGP4746_5_static_amplitude",
            "A_m^stat <= sqrt(C_zeroMode_stat^2 + (C_Dstat^2 + C_boundary_stat)/lambda_1^stat)",
            "Static version of the 4742 multiplier amplitude law.",
            "DERIVED_SYMBOLIC_BOUND",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": proof_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for proof_id, formula, meaning, status in specs
    ]


def static_test_arena_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ARENA4746_0_PPN", "PPN/static weak-field metric response", "eligible for static elliptic slice if parent reduction is fixed before scoring", "STATIC_ROUTE_ELIGIBLE"),
        ("ARENA4746_1_R10", "short-range inverse-square/fifth-force local response", "eligible for static elliptic slice with fixed collar/domain", "STATIC_ROUTE_ELIGIBLE"),
        ("ARENA4746_2_clock", "clock/redshift quasi-static local response", "eligible if time dependence is perturbative and parent-frozen", "STATIC_ROUTE_CONDITIONAL"),
        ("ARENA4746_3_orbital", "quasi-static orbital weak-field response", "eligible in adiabatic/static limit only", "STATIC_ROUTE_CONDITIONAL"),
        ("ARENA4746_4_GW_dynamic", "gravitational-wave/dynamical local response", "not eligible for elliptic gap; use hyperbolic energy", "LORENTZIAN_ROUTE_REQUIRED"),
        ("ARENA4746_5_EM_dynamic", "time-dependent EM/stress coupling response", "not automatically static; use arena-specific split later", "ROUTE_SPLIT_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": arena_id,
            "arena": arena,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for arena_id, arena, rule, status in specs
    ]


def lorentzian_energy_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "HYP4746_0_energy_definition",
            "E_m[t]=||partial_t m||_{L2(Sigma_t)}^2+||nabla_h m||_{L2(Sigma_t)}^2+||m||_{L2(Sigma_t)}^2",
            "Defines the dynamical multiplier energy on a time slab.",
            "ENERGY_DEFINED",
        ),
        (
            "HYP4746_1_energy_bound",
            "E_m[t2] <= C_hyp(E_m[t1]+int_{t1}^{t2}||D_adj m||^2 dt + Flux_boundary + Curv_coeff)",
            "Lorentzian branch is bounded by energy growth, not set to zero by elliptic gap.",
            "DERIVED_SCHEMATIC_BOUND",
        ),
        (
            "HYP4746_2_zero_dynamic_case",
            "If E_m[t1]=0, D_adj m=0, Flux_boundary=0, Curv_coeff controlled, then E_m[t2]=0",
            "Dynamical zero is possible, but it is an initial/boundary energy theorem.",
            "EXACT_DYNAMIC_BRANCH_CONDITIONAL",
        ),
        (
            "HYP4746_3_finite_residual",
            "C_hyp_energy := sqrt(E_m[t2])/a_ref",
            "Finite residual carried into CzeroMode for full Lorentzian dynamics.",
            "FINITE_SOURCE_REQUIRED",
        ),
        (
            "HYP4746_4_no_static_claim",
            "Do not replace C_hyp_energy by lambda_1^stat^{-1} terms",
            "Prevents static elliptic proof from leaking into dynamical local GR.",
            "FIREWALL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "energy_id": energy_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for energy_id, formula, meaning, status in specs
    ]


def owner_symbol_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("OWN4746_0_TFRI", "sigma_R/sigma_Gamma/sigma_phi", "minimal TFRI sub-symbol exists from 4745", "PARTIAL_PRESENT"),
        ("OWN4746_1_TT", "sigma_TT(k;xi)", "DeltaK/TT-superpotential owner symbol", "MISSING_PARENT_COMPONENT"),
        ("OWN4746_2_quarantine", "sigma_quar(k;chi)", "quarantine/conservation-owner symbol", "MISSING_PARENT_COMPONENT"),
        ("OWN4746_3_boundary", "boundary complementing symbol", "needed for static elliptic boundary problem", "MISSING_PARENT_COMPONENT"),
        ("OWN4746_4_physical_kernel", "C_phys_kernel or Pi_phys Pi_0 m=0", "needed to promote CzeroMode=0", "MISSING_SOURCE_VALUE"),
        ("OWN4746_5_gap_constants", "c_DN, C_P, L_loc", "needed to turn lambda_1^stat bound numeric/source-ready", "MISSING_SOURCE_VALUE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "owner_id": owner_id,
            "symbol_or_quantity": symbol,
            "definition": definition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for owner_id, symbol, definition, status in specs
    ]


def residual_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "RB4746_0_static",
            "C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2 + (C_Dstat^2+C_boundary_stat)/lambda_1^stat)",
            "Static local-test residual law.",
            "DERIVED_SYMBOLIC_NONNUMERIC",
        ),
        (
            "RB4746_1_gap_insert",
            "lambda_1^stat >= c_DN/(C_P L_loc^2)",
            "Turns the residual law into a geometry/domain/source problem.",
            "DERIVED_SYMBOLIC_NONNUMERIC",
        ),
        (
            "RB4746_2_lorentzian",
            "C_res_dyn <= Pi_owner^dyn(C_hyp_energy+C_TT_kernel+C_quar_kernel+C_boundary_dyn)",
            "Dynamical residual law.",
            "DERIVED_SYMBOLIC_NONNUMERIC",
        ),
        (
            "RB4746_3_score_gate",
            "score_ready=false until c_DN,C_P,L_loc,Pi_owner,C_phys_kernel,sigma_TT,sigma_quar are sourced",
            "No local-test claim is made from symbolic bounds.",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, formula, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4746_0_static_constants", "source c_DN, C_P, L_loc and boundary complementing data", "best_next_route", "needed for a numeric/source-ready static PPN/R10 bound"),
        ("ROUTE4746_1_owner_symbols", "write sigma_TT and sigma_quar parent components", "parallel_required_route", "needed for full owner ellipticity and CzeroMode closure"),
        ("ROUTE4746_2_lorentzian_energy", "turn schematic hyperbolic energy bound into sourced C_hyp_energy", "dynamic_fallback_route", "needed for full local-GR dynamics"),
        ("ROUTE4746_3_claim_now", "claim local PPN/local-GR pass", "rejected", "constants, full symbols and kernel sources remain missing"),
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
        ("GATE4746_0_sources", "All cited 4746 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4746_1_static_gap_law", "Static gap lower-bound law lambda_1^stat >= c_DN/(C_P L_loc^2) is written.", "conditional_pass", False),
        ("GATE4746_2_static_scope", "Static route is limited to parent-specified PPN/R10/clock/orbital arenas.", "conditional_open", False),
        ("GATE4746_3_lorentzian_energy", "Lorentzian branch carries energy bound instead of elliptic gap.", "conditional_open", False),
        ("GATE4746_4_owner_symbols", "sigma_TT/sigma_quar and boundary complementing symbols remain missing.", "closed_unsigned", False),
        ("GATE4746_5_numeric_constants", "c_DN,C_P,L_loc,Pi_owner,C_phys_kernel remain unsourced.", "closed_unsigned", False),
        ("GATE4746_6_no_claim", "No local-GR, Newton, PPN, R10, WEP, clock or orbital claim from 4746.", "closed_firewall", False),
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
        ("FW4746_0_static_scope", "Do not use the static elliptic gap outside parent-specified static/quasi-static local-test arenas."),
        ("FW4746_1_no_symbolic_scoring", "Do not score local tests until constants and owner symbols are source-backed."),
        ("FW4746_2_lorentzian_separate", "Do not replace Lorentzian energy bounds with static lambda_1^stat."),
        ("FW4746_3_no_owner_subblock_overclaim", "Do not claim full owner ellipticity from the TFRI sub-block alone."),
        ("FW4746_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
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
            "summary": "4746 derives a conditional static local-test gap law lambda_1^stat >= c_DN/(C_P L_loc^2) and a separate Lorentzian time-slab energy bound. Static PPN/R10/clock/orbital arenas can proceed toward sourced constants; full dynamics remains on the hyperbolic energy route. Full owner symbols and physical-kernel constants remain unsigned.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4746_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4746_1_science_verdict",
            "status": "static_gap_bound_and_lorentzian_energy_bound_derived_symbolically",
            "detail": "The local branch now has a static gap formula that can become source-ready, and a separate Lorentzian energy fallback for dynamics.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4746 turns the proof into sourceable constants and missing owner-symbol components.",
            "preferred_route": "Source/derive c_DN, C_P, L_loc and boundary complementing data for the static PPN/R10 bound.",
            "fallback_route": "Write sigma_TT/sigma_quar first if full owner ellipticity blocks the static route.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    static_ops: list[dict[str, Any]],
    static_gap: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    energy: list[dict[str, Any]],
    owner_symbols: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4746 Y5 R2FR: Static PPN Elliptic Slice Gap Proof Or Lorentzian Energy Bound

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint turns the 4745 fork into two explicit proof/bound routes.
- Static local-test route:

```text
STATIC_PPN_ELLIPTIC_SLICE_ONLY
D_stat := spatial/static reduction of D_adj
L_stat := D_stat^* D_stat
lambda_1^stat >= c_DN/(C_P L_loc^2)
```

- Lorentzian dynamical route:

```text
E_m[t2] <= C_hyp(E_m[t1]+int ||D_adj m||^2 dt + Flux_boundary + Curv_coeff)
C_hyp_energy := sqrt(E_m[t2])/a_ref
```

- Static PPN/R10/clock/orbital arenas may pursue the gap law.
- Full Lorentzian local-GR dynamics keeps the energy bound.
- No local-test or local-GR claim is made until constants, projections, owner symbols and kernels are sourced.

## Static Operator Setup

{bullet(static_ops, "operator_id", "formula")}

## Static Gap Proof

{bullet(static_gap, "proof_id", "formula")}

## Static Test Arena Mapping

{bullet(arenas, "arena_id", "arena")}

## Lorentzian Energy Bound

{bullet(energy, "energy_id", "formula")}

## Owner Symbol Completion Ledger

{bullet(owner_symbols, "owner_id", "symbol_or_quantity")}

## Residual Bound Law

{bullet(residuals, "bound_id", "formula")}

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

    formal = f"""# 762 PPC4161: Static PPN Elliptic Slice Gap Proof Or Lorentzian Energy Bound

Generated: `{timestamp}`

## Static Gap Law

4746 derives the symbolic static local-test gap law:

```text
lambda_1^stat >= c_DN/(C_P L_loc^2).
```

Inserted into the local owner-amplitude law:

```text
C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2 + (C_Dstat^2+C_boundary_stat)/lambda_1^stat).
```

This is eligible for PPN/R10/clock/orbital arenas only when the static spatial collar and operator are parent-fixed before scoring.

## Lorentzian Route

Full dynamical local GR stays separate:

```text
E_m[t2] <= C_hyp(E_m[t1]+int ||D_adj m||^2 dt + Flux_boundary + Curv_coeff).
```

No Lorentzian elliptic-gap claim is made.

## Remaining Inputs

- `c_DN`, `C_P`, `L_loc`, `Pi_owner`.
- `sigma_TT`, `sigma_quar`, and boundary complementing symbols.
- `C_phys_kernel` or proof of physical-kernel absence.
- `C_hyp_energy` for full dynamics.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4746 derives the static local-test gap law `lambda_1^stat >= c_DN/(C_P L_loc^2)`.
- Static PPN/R10/clock/orbital arenas can use the gap route only with a parent-fixed spatial collar/operator.
- Full Lorentzian local-GR dynamics uses `E_m[t2] <= C_hyp(E_m[t1]+int ||D_adj m||^2 + Flux_boundary + Curv_coeff)`.
- Remaining source targets: `c_DN`, `C_P`, `L_loc`, `Pi_owner`, `sigma_TT`, `sigma_quar`, boundary complementing data, and `C_phys_kernel`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4746 local packet update: static local tests now have a symbolic gap law and full dynamics has a separate hyperbolic energy bound. Next is source constants and full owner-symbol completion.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4746-Y5-R2FR-static-PPN-elliptic-slice-gap-proof-or-lorentzian-energy-bound.md`

## Decision

`{DECISION}`

## What moved forward

- Derived the symbolic static local-test gap law `lambda_1^stat >= c_DN/(C_P L_loc^2)`.
- Mapped PPN/R10/clock/orbital arenas to the static route only when the static collar/operator is parent-fixed.
- Derived the Lorentzian dynamical fallback as a time-slab energy bound with `C_hyp_energy`.
- Identified the next source targets: `c_DN`, `C_P`, `L_loc`, `Pi_owner`, `sigma_TT`, `sigma_quar`, boundary complementing data, and `C_phys_kernel`.

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
        "4746 derives a symbolic static local-test gap law and a separate Lorentzian hyperbolic energy bound for the local-GR transition branch.",
        "Generated source register, static operator setup, static gap proof, static test arena mapping, Lorentzian energy bound, owner symbol ledger, residual bound law, route matrix, gates, firewalls, decision, status, next target and validation.",
        "static_gap_law_lorentzian_energy_bound_symbolic_nonclaim",
        NEXT_TARGET,
        "Scoring static local tests or claiming local GR before constants, owner symbols, projections and kernels are source-backed.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need c_DN, C_P, L_loc, Pi_owner, sigma_TT, sigma_quar, boundary complementing data, C_phys_kernel and C_hyp_energy.",
        "Static PPN elliptic slice gap proof or Lorentzian energy bound",
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
    static_gap: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    energy: list[dict[str, Any]],
    owner_symbols: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4746_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4746_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4746_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4746_2_static_gap_law", "static gap proof includes lambda_1^stat lower bound", any("lambda_1^stat >=" in row["formula"] for row in static_gap), str(STATIC_GAP_PROOF_CSV)))
    checks.append(("VAL4746_3_static_arena_scope", "arena mapping splits static eligible and Lorentzian required arenas", any(row["status"] == "STATIC_ROUTE_ELIGIBLE" for row in arenas) and any(row["status"] == "LORENTZIAN_ROUTE_REQUIRED" for row in arenas), str(STATIC_TEST_ARENA_CSV)))
    checks.append(("VAL4746_4_lorentzian_energy", "Lorentzian energy bound includes C_hyp_energy", any("C_hyp_energy" in row["formula"] for row in energy), str(LORENTZIAN_ENERGY_CSV)))
    checks.append(("VAL4746_5_owner_symbols_missing", "owner symbol ledger keeps sigma_TT and sigma_quar missing", all(any(symbol in row["symbol_or_quantity"] and row["status"] == "MISSING_PARENT_COMPONENT" for row in owner_symbols) for symbol in ["sigma_TT", "sigma_quar"]), str(OWNER_SYMBOL_COMPLETION_CSV)))
    checks.append(("VAL4746_6_residual_bounds", "residual bound law contains static and dynamical bounds", any("C_res_static" in row["formula"] for row in residuals) and any("C_res_dyn" in row["formula"] for row in residuals), str(RESIDUAL_BOUND_CSV)))
    checks.append(("VAL4746_7_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4746_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4746_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4746_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4746_11_claim_row", "claim row L-588 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4746_12_resume", "resume points from 4746 to 4747", "4746-Y5" in resume_text and "4747-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4746_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4746_OVERALL",
            "check": "all 4746 local generation and nonclaim checks pass",
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
    static_ops = static_operator_rows(timestamp)
    static_gap = static_gap_rows(timestamp)
    arenas = static_test_arena_rows(timestamp)
    energy = lorentzian_energy_rows(timestamp)
    owner_symbols = owner_symbol_rows(timestamp)
    residuals = residual_bound_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(STATIC_OPERATOR_CSV, static_ops)
    write_csv(STATIC_GAP_PROOF_CSV, static_gap)
    write_csv(STATIC_TEST_ARENA_CSV, arenas)
    write_csv(LORENTZIAN_ENERGY_CSV, energy)
    write_csv(OWNER_SYMBOL_COMPLETION_CSV, owner_symbols)
    write_csv(RESIDUAL_BOUND_CSV, residuals)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, static_ops, static_gap, arenas, energy, owner_symbols, residuals, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, static_gap, arenas, energy, owner_symbols, residuals, gates, timestamp))


if __name__ == "__main__":
    main()
