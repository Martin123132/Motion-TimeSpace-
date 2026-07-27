from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3829"
BRANCH = "MTS_R2FR_Y5_SCALAR_READOUT_LOCK_CT_CS_BT_OWNER_OR_BOUND_FILL_3829"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3829-Y5-R2FR-scalar-readout-lock-Ct-Cs-Bt-owner-or-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3828 = PCW / "3828-Y5-R2FR-PPN-readout-tail-descent-or-first-residual-vector-bound.md"
CSV_3828_ANSATZ = OUT / "P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv"
CSV_3828_ZERO = OUT / "P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv"
CSV_3828_RESIDUAL = OUT / "P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv"
CSV_3828_READOUT_GATES = OUT / "P8_Y5_R2FR_3828_LOCAL_GR_READOUT_CLAUSE_GATES.csv"
CSV_3828_VALIDATION = OUT / "P8_Y5_BRR545_3828_VALIDATION.csv"
CSV_3826_SCORECARD = OUT / "P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv"
CSV_3821_STRESS = OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_RESIDUAL_ROWS.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3829_SOURCE_REGISTER.csv",
    "coefficient_owner": OUT / "P8_Y5_R2FR_3829_SCALAR_COEFFICIENT_OWNER_MAP.csv",
    "lock_theorem": OUT / "P8_Y5_R2FR_3829_SCALAR_LOCK_CONDITIONAL_THEOREM.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3829_GAMMA_BETA_COEFFICIENT_BOUND_ROWS.csv",
    "residual_budget": OUT / "P8_Y5_R2FR_3829_SCALAR_RESIDUAL_BUDGET.csv",
    "gates": OUT / "P8_Y5_R2FR_3829_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3829_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3829_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3829_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3829_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3829_0_3828_doc", P_3828, "PPN Readout Tail Descent Or First Residual-Vector Bound"),
    ("SRC3829_1_3828_ansatz", CSV_3828_ANSATZ, "ANS3828_1_spatial_curvature"),
    ("SRC3829_2_3828_zero", CSV_3828_ZERO, "ZPPN3828_1_gamma_lock"),
    ("SRC3829_3_3828_residual", CSV_3828_RESIDUAL, "RPPN3828_1_beta"),
    ("SRC3829_4_3828_readout_gates", CSV_3828_READOUT_GATES, "RGATE3828_0_gamma"),
    ("SRC3829_5_3828_validation", CSV_3828_VALIDATION, "VAL3828_2_zero_conditions"),
    ("SRC3829_6_3826_scorecard", CSV_3826_SCORECARD, "KSC3826_7_PPN_readout_tail"),
    ("SRC3829_7_3821_stress", CSV_3821_STRESS, "R3821_5_total"),
    ("SRC3829_8_3818_Poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_scalar_readout_lock_derivation_or_bound",
                "claim_use": "coefficient_owner_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def coefficient_owner_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "coefficient_id": "COEFF3829_0_C_t",
            "coefficient": "C_t",
            "owned_by": "linear Newtonian temporal source normalization",
            "current_route": "3818 weak-field Poisson bridge fixes C_t after choosing Phi=U/c^2",
            "GR_lock_value": "C_t=1 by Newtonian calibration",
            "open_residual": "R_Poisson_norm + R_source_ledger",
            "status": "CONDITIONAL_OWNER_IDENTIFIED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "coefficient_id": "COEFF3829_1_C_s",
            "coefficient": "C_s",
            "owned_by": "linear spatial curvature readout",
            "current_route": "C_s = C_t + S_slip where S_slip is scalar gravitational slip/readout anisotropy",
            "GR_lock_value": "C_s=C_t",
            "open_residual": "S_slip = S_anisotropic_stress + S_extra_scalar + S_boundary + S_readout_rep",
            "status": "OWNER_REDUCED_TO_SLIP_RESIDUAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "coefficient_id": "COEFF3829_2_B_t",
            "coefficient": "B_t",
            "owned_by": "second-order temporal self-coupling",
            "current_route": "B_t = C_t^2 + S_beta where S_beta is nonlinear source/self-coupling mismatch",
            "GR_lock_value": "B_t=C_t^2",
            "open_residual": "S_beta = S_EH2_mismatch + S_extra_scalar2 + S_boundary2 + S_readout2",
            "status": "OWNER_REDUCED_TO_SECOND_ORDER_VERTEX_RESIDUAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "coefficient_id": "COEFF3829_3_S_slip",
            "coefficient": "S_slip",
            "owned_by": "traceless spatial field equation / no anisotropic stress condition",
            "current_route": "(partial_i partial_j - delta_ij nabla^2/3)(Psi-Phi_s) = source_anisotropic + parent_extra + boundary",
            "GR_lock_value": "S_slip=0",
            "open_residual": "missing parent no-slip signature",
            "status": "NEXT_PROOF_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "coefficient_id": "COEFF3829_4_S_beta",
            "coefficient": "S_beta",
            "owned_by": "second-order EH/nonlinear parent vertex",
            "current_route": "second-order 00 equation must have the GR quadratic vertex and no extra scalar self-energy",
            "GR_lock_value": "S_beta=0",
            "open_residual": "missing parent second-order action expansion",
            "status": "BOUND_ROW_REQUIRED_AFTER_SLIP",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def lock_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "LOCK3829_0_Ct_owner",
            "claim_shape": "C_t is fixed by the Newtonian force/Poisson normalization once Phi=U/c^2 is chosen",
            "derivation_status": "CONDITIONAL_FROM_3818",
            "required_clauses": "same source potential; no fitted GM input; source ledger supplies independent normalization",
            "proof_or_bound": "C_t=1 + epsilon_t with epsilon_t bounded by R_Poisson_norm and source-ledger residual",
            "blocks_if_unsigned": "absolute G/source normalization claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "LOCK3829_1_gamma_no_slip",
            "claim_shape": "C_s=C_t if the scalar traceless spatial equation has no anisotropic/extra/boundary/readout source",
            "derivation_status": "CONDITIONAL_THEOREM_FORMULATED_NOT_PARENT_SIGNED",
            "required_clauses": "single metric readout; no anisotropic stress in compact exterior; no extra scalar slip; decaying or fixed boundary; no representative readout morphism",
            "proof_or_bound": "C_s-C_t = S_slip, so gamma-1 = S_slip/C_t + eps_spatial/Phi",
            "blocks_if_unsigned": "PPN gamma/local GR claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "LOCK3829_2_beta_EH2_vertex",
            "claim_shape": "B_t=C_t^2 if the second-order temporal readout is the GR/EH quadratic vertex with no extra scalar self-energy",
            "derivation_status": "CONDITIONAL_THEOREM_FORMULATED_NOT_PARENT_SIGNED",
            "required_clauses": "parent action second variation; Bianchi/conservation; no extra scalar potential term; boundary/reference second-order silence",
            "proof_or_bound": "B_t-C_t^2 = S_beta, so beta-1 = S_beta/C_t^2 + eps_temporal4/Phi^2",
            "blocks_if_unsigned": "PPN beta/local GR claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "LOCK3829_3_scalar_total",
            "claim_shape": "scalar PPN tail closes when epsilon_t, S_slip, and S_beta vanish or are bounded below experiment thresholds",
            "derivation_status": "NONCLAIM_BOUND_CONTRACT",
            "required_clauses": "3818 Poisson owner; 3830 no-slip signature; later second-order vertex signature",
            "proof_or_bound": "R_scalar_PPN = {epsilon_t, S_slip/C_t, S_beta/C_t^2, eps_spatial/Phi, eps_temporal4/Phi^2}",
            "blocks_if_unsigned": "local Newton/GR competitive claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BND3829_0_Ct_Newtonian_norm",
            "observable": "Newtonian normalization",
            "coefficient_relation": "C_t = 1 + epsilon_t",
            "bound_formula": "abs(epsilon_t) <= abs(R_Poisson_norm) + abs(R_source_ledger)",
            "needed_for_claim": "independent source normalization and no fitted-GM input",
            "source_status": "FORMULA_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BND3829_1_gamma",
            "observable": "gamma-1",
            "coefficient_relation": "C_s = C_t + S_slip",
            "bound_formula": "abs(gamma-1) <= abs(S_slip/C_t) + abs(eps_spatial/Phi)",
            "needed_for_claim": "source or theorem bound for S_slip and eps_spatial on local exterior domain",
            "source_status": "FIRST_GAMMA_COEFFICIENT_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BND3829_2_beta",
            "observable": "beta-1",
            "coefficient_relation": "B_t = C_t^2 + S_beta",
            "bound_formula": "abs(beta-1) <= abs(S_beta/C_t^2) + abs(eps_temporal4/Phi^2)",
            "needed_for_claim": "source or theorem bound for S_beta and fourth-order temporal residual",
            "source_status": "FIRST_BETA_COEFFICIENT_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BND3829_3_scalar_pair",
            "observable": "scalar PPN pair",
            "coefficient_relation": "R_scalar_pair = {gamma-1, beta-1}",
            "bound_formula": "norm(R_scalar_pair) <= w_gamma*B_gamma + w_beta*B_beta",
            "needed_for_claim": "declared norm, experimental thresholds, and source-backed coefficient rows",
            "source_status": "INTEGRATED_SCALAR_PAIR_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_budget_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "budget_id": "RB3829_0_slip_anisotropic_stress",
            "feeds": "S_slip",
            "residual_source": "effective anisotropic stress or traceless spatial source",
            "zero_condition": "Pi_eff^TF=0 on compact exterior domain",
            "bound_needed": "norm(Pi_eff^TF)/abs(Phi)",
            "priority": 1,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "RB3829_1_slip_extra_scalar",
            "feeds": "S_slip",
            "residual_source": "extra scalar/disformal spatial-temporal coefficient mismatch",
            "zero_condition": "single Jordan metric/readout coefficient; no representative scalar morphism",
            "bound_needed": "abs(C_s-C_t)_extra/abs(C_t)",
            "priority": 1,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "RB3829_2_slip_boundary",
            "feeds": "S_slip",
            "residual_source": "boundary/harmonic scalar slip mode",
            "zero_condition": "decaying or reference-locked boundary kills homogeneous slip",
            "bound_needed": "abs(S_boundary/C_t)",
            "priority": 2,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "RB3829_3_beta_EH2",
            "feeds": "S_beta",
            "residual_source": "second-order EH vertex mismatch",
            "zero_condition": "parent second variation equals EH quadratic vertex in the local metric sector",
            "bound_needed": "abs(S_EH2_mismatch/C_t^2)",
            "priority": 3,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "RB3829_4_beta_extra_scalar2",
            "feeds": "S_beta",
            "residual_source": "extra scalar quadratic self-energy or second-order readout term",
            "zero_condition": "no independent scalar self-energy in visible metric readout",
            "bound_needed": "abs(S_extra_scalar2/C_t^2)",
            "priority": 3,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3829_0_Ct_owner",
            "gate": "C_t owner identified",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "claim_allowed": False,
            "reason": "3818 supplies the Poisson route but independent source normalization remains guarded",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3829_1_gamma_lock",
            "gate": "C_s=C_t gamma lock",
            "status": "BLOCKED_BY_S_SLIP",
            "claim_allowed": False,
            "reason": "no parent-signed no-slip theorem yet; first gamma bound row emitted",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3829_2_beta_lock",
            "gate": "B_t=C_t^2 beta lock",
            "status": "BLOCKED_BY_S_BETA",
            "claim_allowed": False,
            "reason": "no parent second-order vertex signature yet; first beta bound row emitted",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3829_3_local_GR_Newton",
            "gate": "local GR/Newton scalar readout claim",
            "status": "BLOCKED_BUT_BOUNDED",
            "claim_allowed": False,
            "reason": "gamma/beta are formula-bounded, not source/theorem closed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3829_4_next_target",
            "gate": "next target attacks no-slip first",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "S_slip controls gamma and is the cleanest scalar lock to derive before beta",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3829_0_Ct_route_kept",
            "decision": "keep C_t anchored to the 3818 Poisson route, with source normalization guarded",
            "basis": "this avoids using orbital mu=GM as an input while preserving the Newtonian limit route",
            "consequence": "gamma and beta are now expressed relative to the same calibrated C_t",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3829_1_gamma_reduced_to_slip",
            "decision": "reduce the gamma lock to S_slip=0 or bound S_slip",
            "basis": "C_s=C_t is equivalent to no scalar gravitational slip under the 3828 ansatz",
            "consequence": "3830 should attack the traceless spatial/no-slip condition directly",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3829_2_beta_deferred_after_slip",
            "decision": "defer the deeper beta proof until the scalar slip branch is either closed or bounded",
            "basis": "B_t=C_t^2 requires second-order parent action data and is harder than the linear no-slip condition",
            "consequence": "beta remains formula-bounded but not yet the next derivation target",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3829_0",
            "next_checkpoint": "3830-Y5-R2FR-no-slip-traceless-ij-source-condition-or-gamma-bound-source.md",
            "script": "scripts/Y5_R2FR_3830_no_slip_traceless_ij_source_condition_or_gamma_bound_source.py",
            "objective": "try to prove S_slip=0 from the traceless spatial field equation, no anisotropic stress, fixed boundary, and single metric readout; otherwise emit source-backed gamma bound rows",
            "reason": "3829 reduces the gamma lock C_s=C_t to the no-slip residual S_slip, which is the cleanest next derivation route toward local GR",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_SCALAR_LOCK_REDUCTION",
            "claim": "no gamma/beta/PPN/local-GR/Newton claim",
            "summary": "3829 identifies C_t ownership, reduces C_s=C_t to the scalar slip residual S_slip, reduces B_t=C_t^2 to S_beta, and emits first gamma/beta coefficient-bound rows.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    coefficient_owner: list[dict[str, object]],
    lock_theorems: list[dict[str, object]],
    bounds: list[dict[str, object]],
    residual_budget: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3829 — Scalar Readout Lock Ct/Cs/Bt Owner Or Bound Fill

Private checkpoint. This attacks the scalar PPN locks from 3828. It does not claim local GR/Newton recovery.

Generated: `{timestamp}`

## Result

3829 gets a useful reduction:

- `C_t` is owned by the 3818 Poisson/Newtonian normalization route, still guarded by independent source normalization;
- `C_s=C_t` is equivalent to a no-slip condition `S_slip=0`;
- `B_t=C_t^2` is equivalent to a second-order vertex condition `S_beta=0`.

So the scalar PPN residuals become

`gamma - 1 = S_slip/C_t + eps_spatial/Phi`

`beta - 1 = S_beta/C_t^2 + eps_temporal4/Phi^2`.

That is not a proof of GR yet, but it is a sharper target: prove/bound `S_slip` first, then attack `S_beta`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Scalar Coefficient Owner Map

{markdown_table(coefficient_owner, ["coefficient_id", "coefficient", "current_route", "GR_lock_value", "open_residual", "status"])}

## Conditional Lock Theorem

{markdown_table(lock_theorems, ["theorem_id", "claim_shape", "derivation_status", "proof_or_bound", "blocks_if_unsigned"])}

## Gamma/Beta Bound Rows

{markdown_table(bounds, ["bound_id", "observable", "coefficient_relation", "bound_formula", "source_status"])}

## Scalar Residual Budget

{markdown_table(residual_budget, ["budget_id", "feeds", "residual_source", "zero_condition", "bound_needed", "priority"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

The work moved forward in the useful direction: `gamma` is now a no-slip problem, and `beta` is now a second-order parent-vertex problem. The next route with the least scrutiny is not EM or cosmology; it is the traceless spatial equation:

`(partial_i partial_j - delta_ij nabla^2/3)(Psi-Phi_s) = source_anisotropic + parent_extra + boundary`.

If that right-hand side vanishes or is source-bounded, `C_s=C_t` becomes derivable/bounded instead of assumed.

Next target: `3830-Y5-R2FR-no-slip-traceless-ij-source-condition-or-gamma-bound-source.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3828", "Current State After 3829", 1)
    paragraph = (
        "`3829` reduces the scalar PPN lock problem to two named residuals. `C_t` is conditionally owned by the 3818 Poisson/Newtonian normalization route, "
        "`C_s=C_t` becomes the no-slip condition `S_slip=0`, and `B_t=C_t^2` becomes the second-order vertex condition `S_beta=0`. "
        "The emitted nonclaim bounds are `|gamma-1| <= |S_slip/C_t| + |eps_spatial/Phi|` and "
        "`|beta-1| <= |S_beta/C_t^2| + |eps_temporal4/Phi^2|`. This sharpens the next proof target to the traceless spatial/no-slip equation.\n\n"
    )
    anchor = "`3828` turns"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3829-Y5-R2FR-scalar-readout-lock-Ct-Cs-Bt-owner-or-bound-fill.md`

Target: try to derive the scalar readout locks `C_s=C_t` and `B_t=C_t^2` from parent metric/action descent, or emit first coefficient-bound rows for `gamma` and `beta`.

This is the best next move because 3828 shows these two scalar locks are the least-optional bridge between MTS source coupling and local PPN/GR recovery."""
    new_gate = """`3830-Y5-R2FR-no-slip-traceless-ij-source-condition-or-gamma-bound-source.md`

Target: try to prove `S_slip=0` from the traceless spatial field equation, no anisotropic stress, fixed boundary, and single metric readout; otherwise emit source-backed `gamma` bound rows.

This is the best next move because 3829 reduces the `gamma` lock `C_s=C_t` to the no-slip residual `S_slip`, which is the cleanest linear derivation route toward local GR."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3829_SCALAR_COEFFICIENT_OWNER_MAP.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3829_SCALAR_LOCK_CONDITIONAL_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3829_GAMMA_BETA_COEFFICIENT_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3829_SCALAR_RESIDUAL_BUDGET.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3829_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3829_SCALAR_COEFFICIENT_OWNER_MAP.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3829 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3829 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    coefficient_owner: list[dict[str, object]],
    lock_theorems: list[dict[str, object]],
    bounds: list[dict[str, object]],
    residual_budget: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in coefficient_owner + lock_theorems + bounds + residual_budget + gates)
    add(
        "VAL3829_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3829_1_coefficients",
        "C_t, C_s, B_t, S_slip, and S_beta are all represented",
        all(token in all_text for token in ["C_t", "C_s", "B_t", "S_slip", "S_beta"]),
        "scalar coefficient tokens present",
    )
    add(
        "VAL3829_2_gamma_beta_bounds",
        "gamma and beta coefficient-bound rows exist",
        any(row["observable"] == "gamma-1" for row in bounds) and any(row["observable"] == "beta-1" for row in bounds),
        f"{len(bounds)} bound rows",
    )
    add(
        "VAL3829_3_nonclaim",
        "all scalar owner, theorem, bound, residual, and gate rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in coefficient_owner + lock_theorems + bounds + residual_budget + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3829_4_gamma_blocked_by_slip",
        "gamma lock is reduced to S_slip and remains blocked",
        any(row["gate_id"] == "GATE3829_1_gamma_lock" and row["status"] == "BLOCKED_BY_S_SLIP" for row in gates),
        "gamma gate blocks on S_slip",
    )
    add(
        "VAL3829_5_beta_blocked_by_vertex",
        "beta lock is reduced to S_beta and remains blocked",
        any(row["gate_id"] == "GATE3829_2_beta_lock" and row["status"] == "BLOCKED_BY_S_BETA" for row in gates),
        "beta gate blocks on S_beta",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3829_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3829_7_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "S_slip" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3829*", "P8_Y5_BRR545_3829*", "*Y5_R2FR_3829*", "3829-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3829_8_formalization_clean",
        "formalization-workbench has no 3829 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3829 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3829_9_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    coefficient_owner = coefficient_owner_rows(timestamp)
    lock_theorems = lock_theorem_rows(timestamp)
    bounds = bound_rows(timestamp)
    residual_budget = residual_budget_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["coefficient_owner"], coefficient_owner)
    write_csv(OUTPUTS["lock_theorem"], lock_theorems)
    write_csv(OUTPUTS["bound_rows"], bounds)
    write_csv(OUTPUTS["residual_budget"], residual_budget)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, coefficient_owner, lock_theorems, bounds, residual_budget, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, coefficient_owner, lock_theorems, bounds, residual_budget, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_SCALAR_LOCK_REDUCTION")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
