from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4139-Y5-R2FR-Cbeta-qloc-projector-normalization-or-first-beta-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_CBETA_QLOC_PROJECTOR_OR_FIRST_BOUND_4139"
CHECKPOINT_ID = "4139"
DECISION = "CBETA_QLOC_OPERATOR_PROJECTOR_DERIVED_NUMERIC_SCORING_BLOCKED_BY_SOURCE_DENSITY_AND_NORMALIZATION"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4139_00_4138_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_NEXT_TARGET.csv",
        "4139-Y5-R2FR-Cbeta-qloc-projector-normalization-or-first-beta-bound.md",
        "4138 selected C_beta_qloc projector normalization or first beta-bound pack.",
    ),
    "SRC4139_01_4138_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_DA_GRAD_BETA_BOUND_ROWS.csv",
        "D_A_grad_beta_master",
        "4138 D_A_grad/C_beta_qloc interface.",
    ),
    "SRC4139_02_4138_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_STATUS.csv",
        "TRACEFREE_KHAT_IMPROVEMENT_FORMAL_ROUTE_UNSIGNED_BETA_BOUND_ROW_FILLED",
        "4138 status: trace-free route derived but not current-branch signed.",
    ),
    "SRC4139_03_4031_tf_projector": (
        SOURCE_DIR / "P8_Y5_R2FR_4031_CBETA_TF_PROJECTOR.csv",
        "C_beta_TF",
        "Earlier symbolic trace-free beta projector definition.",
    ),
    "SRC4139_04_beta_gate": (
        SOURCE_DIR / "P8_Y5_BETA_QLOC_ACCEPTANCE_GATES.csv",
        "q_loc U2 coefficient has same normalization",
        "Original acceptance gate blocking q_loc beta promotion.",
    ),
    "SRC4139_05_beta_decision": (
        SOURCE_DIR / "P8_Y5_BETA_QLOC_DECISION.csv",
        "compact_shell_budget_below_beta_lock_if_same_normalization",
        "Prior decision that q_loc budget is only provisional without U2 normalization.",
    ),
    "SRC4139_06_3025_core": (
        SOURCE_DIR / "P8_Y5_R2FR_3025_C_BETA_CORE_BOUND_ROWS.csv",
        "7.8e-05",
        "Nonclaim beta core bound lock.",
    ),
    "SRC4139_07_3991_schema": (
        SOURCE_DIR / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_SCHEMA.csv",
        "A_source;B_source",
        "PPN beta source evaluator schema for same-normalized A/B comparison.",
    ),
    "SRC4139_08_3969_q_loc": (
        SOURCE_DIR / "P8_Y5_R2FR_3969_BETA_OBSTRUCTION_BOUND_ROWS.csv",
        "q_loc_U2",
        "Existing q_loc second-order beta obstruction row.",
    ),
    "SRC4139_09_4125_common": (
        SOURCE_DIR / "P8_Y5_R2FR_4125_COMMON_BETA_OBSERVABLE_ROWS.csv",
        "PPN_residual_vector_common",
        "Recent common-beta observable map.",
    ),
    "SRC4139_10_4126_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4126_BETA_COMMON_BOUND_ROWS.csv",
        "PPN_local_GR",
        "Recent common-beta PPN bound row.",
    ),
    "SRC4139_11_3919_inputs": (
        SOURCE_DIR / "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv",
        "A_source",
        "Beta source-normalized input ledger.",
    ),
    "SRC4139_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4139_Cbeta_qloc_projector_normalization_or_first_beta_bound.py",
        "Reproducible generator for this 4139 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def projector_derivation_rows() -> List[dict]:
    data = [
        (
            "PD4139_0_ppn_gauge",
            "same-normalized PPN gauge",
            "g_00=-1+2U-2(1+delta_beta)U^2+O(v^6); nabla^2 U=-4*pi*G_ref*rho_H",
            "Defines the beta target in the same EH/Newton/source frame; otherwise a q_loc number cannot be compared to the 7.8e-05 beta lock.",
            "GAUGE_CONTRACT_WRITTEN",
            "need source-frame U, A_source and calibrated G_ref/M_H convention",
        ),
        (
            "PD4139_1_q_source_density",
            "q_loc second-order source density",
            "S_q00^{(4)}:=Pi_00^{PPN}[P_loc nabla_mu Delta_K^{mu nu}+Euler+boundary+source-normalization pieces]_{U^2}",
            "Turns the vector residual into the actual source term that enters the second-order g_00 equation.",
            "SOURCE_DENSITY_DEFINED",
            "current corpus has not supplied numeric/source-backed S_q00^{(4)}",
        ),
        (
            "PD4139_2_green_solution",
            "PPN Green response",
            "h_00,q^{(4)}(x)=L_00^{-1}S_q00^{(4)}=-1/(4*pi) int_Omega G_Delta(x,x') S_q00^{(4)}(x') d^3x'",
            "This is the operator that converts q_loc/D_A_grad into a metric coefficient rather than a free beta parameter.",
            "GREEN_OPERATOR_DEFINED",
            "need local collar, boundary conditions and units for G_Delta",
        ),
        (
            "PD4139_3_beta_projection",
            "U^2 projection",
            "delta_beta_q_loc=-1/2 * <h_00,q^{(4)},U^2>_Omega / <U^2,U^2>_Omega",
            "Extracts the coefficient of U^2 in the standard PPN beta convention.",
            "PROJECTOR_DERIVED",
            "need inner product/domain/window and source-normalized U",
        ),
        (
            "PD4139_4_Cbeta_definition",
            "same-normalized C_beta_qloc",
            "C_beta_qloc[D]:=-1/(2D) * <L_00^{-1} S_q00^{(4)}[D],U^2>/<U^2,U^2>",
            "Defines C_beta_qloc as an operator norm/response coefficient tied to the residual amplitude D, not an arbitrary fitted constant.",
            "OPERATOR_PROJECTOR_DEFINED",
            "D must be a declared D_A_grad envelope with source-backed units",
        ),
        (
            "PD4139_5_zero_projection",
            "projector-zero theorem",
            "C_beta_qloc=0 if S_q00^{(4)} is pure gauge, compact total divergence with silent boundary, or U^2-orthogonal after L_00^{-1}",
            "This is the cleanest win condition: derive zero by geometry rather than measuring a tiny number.",
            "ZERO_THEOREM_CONDITIONS_DEFINED",
            "none of pure-gauge, boundary-silent divergence or U^2 orthogonality is signed yet",
        ),
        (
            "PD4139_6_bound_norm",
            "conservative operator bound",
            "|delta_beta_q_loc| <= (1/2)*||Pi_U2 L_00^{-1} Pi_00^{PPN}|| * ||S_q00^{(4)}|| / ||U^2||",
            "If the zero theorem fails, the beta problem becomes a bounded source-normalized operator-norm problem.",
            "BOUND_OPERATOR_DERIVED",
            "operator norm and source-density norm are not numeric/source-backed",
        ),
    ]
    rows: List[dict] = []
    for derivation_id, step, formula, meaning, status, blocker in data:
        row = row_base()
        row.update(
            {
                "derivation_id": derivation_id,
                "step": step,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "blocker": blocker,
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def projector_gate_rows() -> List[dict]:
    data = [
        (
            "PG4139_0_same_gauge",
            "same-normalized PPN gauge",
            "U, A_source, G_ref and M_H are the same objects used in the EH/Newton fit and the beta residual.",
            "PARTIAL_SCHEMA_ONLY",
            "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv keeps A_source/B_source as theorem-zero-or-fallback rows, not sourced values.",
        ),
        (
            "PG4139_1_source_density",
            "S_q00^{(4)} supplied",
            "q_loc/D_A_grad is mapped to the actual second-order g_00 source density in PPN gauge.",
            "MISSING_SOURCE_DENSITY",
            "4138 defines D_A_grad envelope but does not provide S_q00^{(4)}.",
        ),
        (
            "PG4139_2_green_kernel",
            "L_00^{-1} kernel supplied",
            "The weak-field Green operator, boundary collar and window function are declared with units.",
            "MISSING_KERNEL",
            "4031 defines a symbolic projector only.",
        ),
        (
            "PG4139_3_U2_projection",
            "U^2 projection supplied",
            "The inner product <.,.>_Omega and normalization <U^2,U^2>_Omega are fixed.",
            "MISSING_PROJECTION_NORMALIZATION",
            "No source-backed U profile/domain/window row exists in this branch.",
        ),
        (
            "PG4139_4_zero_theorem",
            "projection zero theorem",
            "S_q00^{(4)} is pure gauge, boundary-silent total divergence, or Green-orthogonal to U^2.",
            "UNSIGNED_ZERO_THEOREM",
            "boundary/projector/source-normalization gates remain open.",
        ),
        (
            "PG4139_5_beta_lock",
            "beta lock comparison",
            "|delta_beta_q_loc| <= 7.8e-05 after same normalization and no-cancellation envelope.",
            "REFERENCE_ONLY_NOT_SCORE_READY",
            "7.8e-05 is available as a nonclaim lock, but delta_beta_q_loc is not numeric.",
        ),
    ]
    rows: List[dict] = []
    for gate_id, gate, pass_condition, status, evidence in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "pass_condition": pass_condition,
                "status": status,
                "evidence": evidence,
                "gate_passed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def acquisition_pack_rows() -> List[dict]:
    data = [
        (
            "ACQ4139_0_U_profile",
            "U(x)",
            "Newtonian potential profile in the source-normalized PPN domain",
            "potential; dimensionless in c=1 or declared c-units",
            "solve nabla^2 U=-4*pi*G_ref*rho_H with same source mass used in A_source",
            "required before U^2 projection can be computed",
        ),
        (
            "ACQ4139_1_source_density",
            "S_q00^{(4)}(x)",
            "second-order 00 source density produced by q_loc/D_A_grad",
            "same units as L_00 h_00^{(4)}",
            "derive Pi_00^{PPN}[P_loc nabla Delta_K+Euler+boundary+source-normalization] at O(U^2)",
            "main missing object",
        ),
        (
            "ACQ4139_2_green_kernel",
            "G_Delta(x,x')",
            "Green kernel for L_00 in the chosen PPN gauge/collar",
            "length^-1 or declared Poisson-kernel units",
            "declare boundary conditions and domain Omega",
            "needed to turn source density into h_00^{(4)}",
        ),
        (
            "ACQ4139_3_projection_norm",
            "N_U2=<U^2,U^2>_Omega",
            "normalization of the beta U^2 basis function",
            "domain-volume weighted U^4 units",
            "fix inner product/window and compute N_U2",
            "prevents arbitrary rescaling of C_beta_qloc",
        ),
        (
            "ACQ4139_4_operator_norm",
            "C_beta_qloc",
            "-1/(2D_A_grad_envelope)<L_00^{-1}S_q00^{(4)},U^2>/N_U2",
            "dimensionless per declared D_A_grad envelope",
            "compute from source density and Green kernel or prove zero",
            "target coefficient",
        ),
        (
            "ACQ4139_5_beta_bound",
            "delta_beta_q_loc",
            "C_beta_qloc*C_Ploc*(A_TF/L_TF + A_conn/L_conn + A_proj/L_proj + A_srcnorm/L_srcnorm)",
            "dimensionless beta residual",
            "all component amplitudes numeric/source-backed or theorem-zero",
            "only then compare to 7.8e-05",
        ),
        (
            "ACQ4139_6_cross_arena_guard",
            "alpha3/gamma/Gdot guard",
            "same q_loc source density must also be checked against preferred-frame, gamma and drift projections",
            "dimensionless or time^-1 by arena",
            "avoid declaring local-GR from beta alone",
            "prevents beta-only overclaim",
        ),
    ]
    rows: List[dict] = []
    for acquisition_id, symbol, meaning, units, acquisition_rule, role in data:
        row = row_base()
        row.update(
            {
                "acquisition_id": acquisition_id,
                "symbol": symbol,
                "meaning": meaning,
                "units": units,
                "acquisition_rule": acquisition_rule,
                "role": role,
                "current_status": "MISSING_OR_SYMBOLIC_ONLY",
                "numeric_value_present": "False",
                "source_backed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def first_beta_bound_rows() -> List[dict]:
    data = [
        (
            "BB4139_0_operator_projection",
            "delta_beta_q_loc",
            "delta_beta_q_loc=-1/2 <L_00^{-1}S_q00^{(4)},U^2>/<U^2,U^2>",
            "|delta_beta_q_loc| <= 7.8e-05 only after same-normalized numeric S_q00 and U are supplied",
            "dimensionless",
            "U;S_q00^{(4)};L_00^{-1};Omega;N_U2;A_source;source path",
            "FORMULA_DERIVED_INPUTS_MISSING",
        ),
        (
            "BB4139_1_envelope_projection",
            "D_A_grad_beta_envelope",
            "|delta_beta_q_loc| <= |C_beta_qloc|*C_Ploc*(A_TF/L_TF + A_conn/L_conn + A_proj/L_proj + A_srcnorm/L_srcnorm)",
            "absolute no-cancellation envelope below beta lock",
            "dimensionless",
            "C_beta_qloc and every D_A_grad amplitude component",
            "BOUND_FORM_FILLED_NONNUMERIC",
        ),
        (
            "BB4139_2_zero_branch",
            "C_beta_qloc_zero",
            "C_beta_qloc=0 if L_00^{-1}S_q00^{(4)} is U^2-orthogonal or pure gauge/boundary-silent",
            "theorem certificate replaces numeric beta bound",
            "theorem row",
            "pure-gauge proof; boundary flux zero; projection orthogonality",
            "THEOREM_ROUTE_OPEN_UNSIGNED",
        ),
        (
            "BB4139_3_core_lock_reference",
            "beta_lock",
            "abs(delta_beta_total) <= 7.8e-05",
            "comparison lock only; not a q_loc pass",
            "dimensionless",
            "all beta channels and first-order source preconditions",
            "REFERENCE_LOCK_NONCLAIM",
        ),
        (
            "BB4139_4_total_beta_guard",
            "delta_beta_total",
            "|delta_beta_total| <= |delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary|+|delta_beta_readout|",
            "beta pass requires the full absolute vector, not just q_loc",
            "dimensionless",
            "source/R11/q_loc/boundary/readout rows all score-ready",
            "TOTAL_GUARD_FILLED_NONCLAIM",
        ),
    ]
    rows: List[dict] = []
    for bound_id, observable, formula, pass_rule, units, required_inputs, status in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "observable": observable,
                "formula": formula,
                "pass_rule": pass_rule,
                "units": units,
                "required_inputs": required_inputs,
                "status": status,
                "numeric_value_present": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_gate_rows() -> List[dict]:
    data = [
        (
            "DG4139_0_projector_derived",
            "CBETA_QLOC_OPERATOR_PROJECTOR_DERIVED",
            "The PPN beta projector is now an explicit Green/operator projection onto U^2, not an undefined coefficient.",
            "use this as the only allowed C_beta_qloc definition",
        ),
        (
            "DG4139_1_not_numeric",
            "NUMERIC_SCORING_BLOCKED",
            "The actual source density S_q00^{(4)}, U profile, Green kernel, projection norm and A_source convention are not supplied.",
            "no beta score or local-GR claim",
        ),
        (
            "DG4139_2_zero_route",
            "PROJECTOR_ZERO_THEOREM_ROUTE_OPEN",
            "A clean win is still possible if q_loc/D_A_grad is pure gauge, boundary-silent divergence, or Green-orthogonal to U^2.",
            "try zero theorem before chasing fragile numbers",
        ),
        (
            "DG4139_3_bound_pack",
            "FIRST_SOURCE_READY_BOUND_PACK_FILLED",
            "If the zero theorem fails, the exact rows needed for a source-backed C_beta_qloc and delta_beta_q_loc bound are now listed.",
            "acquire source density/kernel/profile rows",
        ),
        (
            "DG4139_4_next",
            "NEXT_QLOC_PPN_SOURCE_DENSITY_SELECTED",
            "The next non-circular task is to derive S_q00^{(4)} from q_loc/D_A_grad in the weak-field equations or prove it has zero U^2 projection.",
            "4140-Y5-R2FR-q-loc-PPN-source-density-extraction-or-projector-zero-proof.md",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4139_0",
            "result": DECISION,
            "summary": (
                "4139 derives the same-normalized operator definition of C_beta_qloc: solve the weak-field g00 "
                "equation for the q_loc/D_A_grad source density and project the Green-response h00^(4) onto U^2. "
                "This converts the beta obstruction into a precise projector/zero theorem/source-acquisition problem. "
                "No numeric beta or local-GR claim is made because S_q00^(4), U, L_00^{-1}, N_U2 and A_source are not source-backed."
            ),
            "operator_projector_derived": "True",
            "projector_zero_signed": "False",
            "numeric_beta_score_ready": "False",
            "source_ready_acquisition_pack_filled": "True",
            "claim_state": "no C_beta_qloc numeric score, q_loc beta pass, total PPN pass, local-GR pass, Newton limit claim, or public evidence claim",
            "next_target": "4140 q_loc PPN source density extraction or projector-zero proof",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4139_0",
            "target_doc": "4140-Y5-R2FR-q-loc-PPN-source-density-extraction-or-projector-zero-proof.md",
            "target_script": "scripts/Y5_R2FR_4140_q_loc_PPN_source_density_extraction_or_projector_zero_proof.py",
            "objective": (
                "derive S_q00^{(4)}=Pi_00^{PPN}[q_loc/D_A_grad] in the weak-field source-normalized equations and test whether "
                "L_00^{-1}S_q00^{(4)} is pure gauge, boundary-silent, or U^2-orthogonal; if not, emit first source-ready numeric density/kernel rows"
            ),
            "success_gate": "S_q00^{(4)} is theorem-zero for beta or source-backed enough to evaluate C_beta_qloc",
            "reason": "4139 defines the projector; the next missing non-circular object is the actual q_loc/D_A_grad source density entering g00 at O(U^2).",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4139_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4139_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4139_CBETA_QLOC_PROJECTOR_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4139_CBETA_QLOC_PROJECTOR_DERIVATION.csv",
        "P8_Y5_R2FR_4139_PROJECTOR_GATES": SOURCE_DIR / "P8_Y5_R2FR_4139_PROJECTOR_GATES.csv",
        "P8_Y5_R2FR_4139_SOURCE_ACQUISITION_PACK": SOURCE_DIR / "P8_Y5_R2FR_4139_SOURCE_ACQUISITION_PACK.csv",
        "P8_Y5_R2FR_4139_FIRST_BETA_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4139_FIRST_BETA_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4139_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4139_DECISION_GATES.csv",
        "P8_Y5_R2FR_4139_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4139_STATUS.csv",
        "P8_Y5_R2FR_4139_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4139_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4139 - Cbeta q_loc Projector Normalization Or First Beta Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- `C_beta_qloc` is now defined as a same-normalized weak-field operator projection, not a loose coefficient.",
        "- No beta/local-GR score is claimed because the actual `S_q00^{(4)}` source density and Green/projection normalization are still missing.",
        "- The next derivation target is therefore the `q_loc/D_A_grad` source density entering `g_00` at `O(U^2)`.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(
        [
            "",
            "## Projector Definition",
            "",
            "Use the same PPN/source frame as the EH/Newton branch:",
            "",
            "`g_00=-1+2U-2(1+delta_beta)U^2+O(v^6)` and `nabla^2 U=-4*pi*G_ref*rho_H`.",
            "",
            "The q_loc source density is defined by",
            "",
            "`S_q00^{(4)}:=Pi_00^{PPN}[P_loc nabla_mu Delta_K^{mu nu}+Euler+boundary+source-normalization pieces]_{U^2}`.",
            "",
            "Then",
            "",
            "`h_00,q^{(4)}=L_00^{-1}S_q00^{(4)}`",
            "",
            "and the beta projection is",
            "",
            "`delta_beta_q_loc=-1/2 * <h_00,q^{(4)},U^2>_Omega / <U^2,U^2>_Omega`.",
            "",
            "So",
            "",
            "`C_beta_qloc[D]:=-1/(2D) * <L_00^{-1} S_q00^{(4)}[D],U^2>/<U^2,U^2>`.",
            "",
            "## Zero Or Bound Fork",
            "",
            "| route | status | blocker |",
            "|---|---|---|",
        ]
    )
    for row in projector_derivation_rows():
        sections.append(f"| {row['step']} | {row['status']} | {row['blocker']} |")
    sections.extend(
        [
            "",
            "## First Acquisition Pack",
            "",
            "| symbol | role | current status |",
            "|---|---|---|",
        ]
    )
    for row in acquisition_pack_rows():
        sections.append(f"| {row['symbol']} | {row['role']} | {row['current_status']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- No `C_beta_qloc` numeric score, `q_loc` beta pass, total PPN pass, local-GR pass, Newton-limit claim, or public evidence claim follows from 4139.",
            "- The useful movement is that the beta projector is now a concrete weak-field calculation target.",
            "",
            "## Next Target",
            "",
            "- `4140-Y5-R2FR-q-loc-PPN-source-density-extraction-or-projector-zero-proof.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4139_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4139_CBETA_QLOC_PROJECTOR_DERIVATION": projector_derivation_rows,
        "P8_Y5_R2FR_4139_PROJECTOR_GATES": projector_gate_rows,
        "P8_Y5_R2FR_4139_SOURCE_ACQUISITION_PACK": acquisition_pack_rows,
        "P8_Y5_R2FR_4139_FIRST_BETA_BOUND_ROWS": first_beta_bound_rows,
        "P8_Y5_R2FR_4139_DECISION_GATES": decision_gate_rows,
        "P8_Y5_R2FR_4139_STATUS": status_rows,
        "P8_Y5_R2FR_4139_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4139_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4139_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4139_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    derivation_text = flatten_rows([outputs["P8_Y5_R2FR_4139_CBETA_QLOC_PROJECTOR_DERIVATION"]])
    derivation_ok = all(
        token in derivation_text
        for token in [
            "g_00=-1+2U",
            "S_q00^{(4)}",
            "L_00^{-1}",
            "delta_beta_q_loc=-1/2",
            "C_beta_qloc[D]",
            "U^2-orthogonal",
            "BOUND_OPERATOR_DERIVED",
        ]
    )
    add("VAL4139_3_projector_derivation", "derivation includes PPN gauge, source density, Green response, U2 projection, C_beta definition and bound norm", derivation_ok, "derivation tokens checked")

    gate_text = flatten_rows([outputs["P8_Y5_R2FR_4139_PROJECTOR_GATES"]])
    gate_ok = all(
        token in gate_text
        for token in [
            "same-normalized PPN gauge",
            "S_q00^{(4)} supplied",
            "L_00^{-1} kernel supplied",
            "U^2 projection supplied",
            "projection zero theorem",
            "7.8e-05",
        ]
    )
    add("VAL4139_4_projector_gates", "gates cover same gauge, source density, Green kernel, U2 projection, zero theorem and beta lock", gate_ok, "gate tokens checked")

    acquisition_text = flatten_rows([outputs["P8_Y5_R2FR_4139_SOURCE_ACQUISITION_PACK"]])
    acquisition_ok = all(
        token in acquisition_text
        for token in [
            "U(x)",
            "S_q00^{(4)}(x)",
            "G_Delta(x,x')",
            "N_U2",
            "C_beta_qloc",
            "delta_beta_q_loc",
            "alpha3/gamma/Gdot guard",
        ]
    )
    add("VAL4139_5_acquisition_pack", "acquisition pack lists U, source density, Green kernel, U2 norm, C_beta, delta_beta and cross-arena guard", acquisition_ok, "acquisition tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4139_FIRST_BETA_BOUND_ROWS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "delta_beta_q_loc=-1/2",
            "D_A_grad_beta_envelope",
            "C_beta_qloc=0",
            "7.8e-05",
            "delta_beta_total",
        ]
    )
    add("VAL4139_6_bound_rows", "bound rows include direct projection, envelope, zero branch, beta lock and total beta guard", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4139_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "CBETA_QLOC_OPERATOR_PROJECTOR_DERIVED",
            "NUMERIC_SCORING_BLOCKED",
            "PROJECTOR_ZERO_THEOREM_ROUTE_OPEN",
            "FIRST_SOURCE_READY_BOUND_PACK_FILLED",
            "NEXT_QLOC_PPN_SOURCE_DENSITY_SELECTED",
        ]
    )
    add("VAL4139_7_decisions", "decisions record projector derivation, blocked scoring, zero route, bound pack and next source-density target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4139_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("operator_projector_derived") == "True"
        and status[0].get("projector_zero_signed") == "False"
        and status[0].get("numeric_beta_score_ready") == "False"
        and status[0].get("source_ready_acquisition_pack_filled") == "True"
    )
    add("VAL4139_8_status", "status records derived projector, unsigned zero, blocked score and filled acquisition pack", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4139_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4140-Y5-R2FR-q-loc-PPN-source-density-extraction-or-projector-zero-proof.md"
    add("VAL4139_9_next_target", "next target is q_loc PPN source-density extraction or projector-zero proof", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4139_10_no_claim_flags", "all generated rows remain no-claim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4139*")) or any(FORMALIZATION.rglob("4139-Y5-R2FR*"))
    add(
        "VAL4139_11_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4139_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4139_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
