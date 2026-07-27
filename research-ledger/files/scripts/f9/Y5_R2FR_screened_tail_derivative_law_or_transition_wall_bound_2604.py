from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_TAIL_LAW_REBASE_2604"
CHECKPOINT_ID = "2604"

DOC = ROOT / "2604-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_LINEAGE_LEDGER.csv",
    "tail_theorem": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_TAIL_DERIVATIVE_THEOREM.csv",
    "package_gate": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_CANONICAL_PACKAGE_GATE.csv",
    "canonical_bridge": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_CANONICAL_SOURCE_BRIDGE.csv",
    "runner_refusal": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2604_VALIDATION.csv",
}

COPY_TARGETS = {
    "tail_theorem": LOCAL_BOUNDS / "Screened_tail_derivative_theorem_2604_NONCLAIM.csv",
    "package_gate": LOCAL_BOUNDS / "Canonical_gap_beta_wall_package_gate_2604_NONCLAIM.csv",
    "next_target": QUEUE / "JR2604_GAP_BETA_TAU_SOURCE_PACKAGE_VALIDATOR_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2604_00_2603_handoff_doc",
            "source_path": ROOT / "2603-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md",
            "needles": ["TLB2603_2_tail_derivative", "NEXT2603_0_selected", "VAL2603_OVERALL"],
            "role": "current branch handoff selecting screened-tail derivative law",
        },
        {
            "source_id": "SRC2604_01_2603_tail_bridge",
            "source_path": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_TAIL_LAW_BRIDGE.csv",
            "needles": ["TLB2603_2_tail_derivative", "TLB2603_3_transition_wall", "TLB2603_4_DeltaK"],
            "role": "current branch tail-law, wall fallback and DeltaK blockers",
        },
        {
            "source_id": "SRC2604_02_1746_doc",
            "source_path": ROOT / "1746-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md",
            "needles": ["TD1746_1_exponential_tail_solution", "TWB1746_0_wall_gradient_residual", "NEXT1746_0_primary", "VAL1746_OVERALL"],
            "role": "prior screened-tail theorem and wall-bound attempt",
        },
        {
            "source_id": "SRC2604_03_1746_tail_theorem",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1746_TAIL_DERIVATIVE_THEOREM.csv",
            "needles": ["TD1746_1_exponential_tail_solution", "TD1746_2_canonical_gap_rewrite", "TD1746_4_wall_counterbranch"],
            "role": "conditional tail derivative theorem rows",
        },
        {
            "source_id": "SRC2604_04_1746_canonical_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1746_CANONICAL_SOURCE_ROWS.csv",
            "needles": ["CSR1746_0_mu_m2", "CSR1746_1_Phi_S", "CSR1746_3_beta_source_test"],
            "role": "missing canonical gap, amplitude and coupling source rows",
        },
        {
            "source_id": "SRC2604_05_1746_wall_bound",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1746_TRANSITION_WALL_BOUND.csv",
            "needles": ["TWB1746_0_wall_gradient_residual", "TWB1746_1_shell_boundary_residual"],
            "role": "finite transition-wall and shell residual bound forms",
        },
        {
            "source_id": "SRC2604_06_1747_doc",
            "source_path": ROOT / "1747-Y5-R2FR-canonical-gap-coupling-source-silence-or-wall-bound-row.md",
            "needles": ["CPG1747_7_verdict", "BAI1747_0_MICROSCOPE_Delta_w_tau_bound_anchor", "NEXT1747_0_primary", "VAL1747_OVERALL"],
            "role": "prior canonical gap, coupling and source-silence gate",
        },
        {
            "source_id": "SRC2604_07_1747_package_gate",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1747_CANONICAL_PACKAGE_GATE.csv",
            "needles": ["CPG1747_0_tail_law", "CPG1747_3_coupling", "CPG1747_7_verdict"],
            "role": "whole canonical package status",
        },
        {
            "source_id": "SRC2604_08_1747_gap_amplitude",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv",
            "needles": ["GAS1747_0_mu_m2", "GAS1747_1_Phi_S", "GAS1747_4_projection"],
            "role": "gap, amplitude, domain and projection source gate",
        },
        {
            "source_id": "SRC2604_09_1747_coupling_silence",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1747_COUPLING_SOURCE_SILENCE_GATE.csv",
            "needles": ["CSS1747_0_q_kernel", "CSS1747_5_current_owner", "CSS1747_7_verdict"],
            "role": "coupling-zero and matter/source-silence failure rows",
        },
        {
            "source_id": "SRC2604_10_1747_bound_anchor",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1747_BOUND_ANCHOR_IMPORT.csv",
            "needles": ["BAI1747_0_MICROSCOPE_Delta_w_tau_bound_anchor", "BAI1747_1_current_beta_verdict"],
            "role": "real WEP bound anchor imported as nonprediction",
        },
        {
            "source_id": "SRC2604_11_1747_wall_bound",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1747_WALL_BOUND_ROW.csv",
            "needles": ["WBR1747_0_transition_wall_gradient", "WBR1747_1_boundary_shell"],
            "role": "transition-wall fallback rows retained after canonical package check",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2604_0_2603",
            "checkpoint": "2603",
            "question": "Can the sigmaX/x_U branch use double zeros to suppress q_loc gradients?",
            "result": "No. 2603 selected a screened-tail derivative law or wall bound because amplitude zeros alone do not control gradients.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "tail derivative theorem or finite wall residual",
        },
        {
            "step_id": "LIN2604_1_1746",
            "checkpoint": "1746",
            "question": "Can abs(nabla U_B) be bounded by U_B/L_tr?",
            "result": "Yes as a conditional theorem for a source-free massive/exponential tail; wall overlap remains a counterbranch.",
            "status": "CONDITIONAL_TAIL_THEOREM_AVAILABLE",
            "next_dependency": "parent gap, amplitude, source silence and boundary class",
        },
        {
            "step_id": "LIN2604_2_1747",
            "checkpoint": "1747",
            "question": "Can that conditional tail theorem be promoted to local GR/Newton recovery?",
            "result": "No. The canonical package lacks mu_m2, Phi_S, beta legs, source weights, projection norms, and wall/shell data.",
            "status": "PARENT_PACKAGE_NOT_CLOSED",
            "next_dependency": "gap-beta-tau source package validator",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def tail_theorem_rows() -> list[dict[str, Any]]:
    source_paths = [
        ROOT / "1746-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md",
        OUT / "P8_Y5_PARENT_QLOC_1746_TAIL_DERIVATIVE_THEOREM.csv",
        OUT / "P8_Y5_PARENT_QLOC_1747_CANONICAL_PACKAGE_GATE.csv",
    ]
    rows = [
        {
            "theorem_id": "TD2604_0_target_condition",
            "claim": "q_loc-safe double-zero branch requires a derivative tail law",
            "calculation": "if f=F(D_L^2), then nabla f=F_prime(D_L^2) 2 D_L nabla D_L; p=2 amplitude zeros do not control q_loc unless nabla D_L is tail-suppressed",
            "current_status": "TARGET_REBASED_FROM_2603",
            "promotion_status": "NECESSARY_NOT_SUFFICIENT",
            "missing_inputs": "MISSING_D_L_TAIL;MISSING_PROJECTOR_NORMS;MISSING_KHAT_SUBTRACTION",
        },
        {
            "theorem_id": "TD2604_1_exponential_tail_solution",
            "claim": "the source-free massive tail satisfies abs(nabla U_B)<=C_U U_B/ell_tr",
            "calculation": "for a canonical exterior equation (Box-mu_m2) phi=0 with decaying boundary data, phi<=Phi_S exp(-d/ell_tr) and abs(nabla phi)<=C_tail Phi_S exp(-d/ell_tr)/ell_tr",
            "current_status": "DERIVED_CONDITIONALLY",
            "promotion_status": "PASS_NONCLAIM_THEOREM",
            "missing_inputs": "MISSING_SOURCE_BACKED_MU_M2;MISSING_PHI_S;MISSING_DOMAIN_DISTANCE;MISSING_BOUNDARY_CLASS",
        },
        {
            "theorem_id": "TD2604_2_canonical_gap_rewrite",
            "claim": "the invariant range parameter is ell_tr=1/sqrt(mu_m2)",
            "calculation": "replace coordinate/split-specific kappa/F2 language with the canonical positive quadratic operator gap mu_m2",
            "current_status": "CANONICAL_REWRITE_READY",
            "promotion_status": "NONCLAIM_UNTIL_PARENT_GAP_SIGNED",
            "missing_inputs": "MISSING_PARENT_HESSIAN;MISSING_KINETIC_NORMALIZATION;MISSING_UNITS",
        },
        {
            "theorem_id": "TD2604_3_positive_operator_generalization",
            "claim": "coercive source-free local operators admit exponential or Agmon-type decay estimates",
            "calculation": "a positive gap, no zero mode, controlled boundary data and no interior source give derivative estimates with constants C_tail and correction envelope epsilon_tail",
            "current_status": "MATHEMATICAL_ROUTE_IDENTIFIED",
            "promotion_status": "NONCLAIM_UNTIL_OPERATOR_CLASS_SIGNED",
            "missing_inputs": "MISSING_COERCIVITY_PROOF;MISSING_NO_ZERO_MODE;MISSING_EPSILON_TAIL;MISSING_DOMAIN_REGULARITY",
        },
        {
            "theorem_id": "TD2604_4_wall_counterbranch",
            "claim": "if local support intersects a sharp transition wall, gradient suppression is replaced by a finite wall residual",
            "calculation": "nabla U_B can scale as O(1/L_wall), so q_loc retains Q_wall_grad <= C_wall Phi_S^2 U_B/L_wall plus shell/projector terms",
            "current_status": "COUNTERBRANCH_RETAINED",
            "promotion_status": "BOUND_FORM_ONLY_NONCLAIM",
            "missing_inputs": "MISSING_L_WALL;MISSING_SUPPORT_OVERLAP;MISSING_C_WALL;MISSING_SHELL_PROJECTOR",
        },
        {
            "theorem_id": "TD2604_5_current_verdict",
            "claim": "the gradient trap is mathematically avoidable but not parent-signed",
            "calculation": "2604 converts the blocker from a calculus objection into a source-package obligation",
            "current_status": "REAL_PROGRESS_NO_LOCAL_GR_CLAIM",
            "promotion_status": "NEXT_GATE_REQUIRED",
            "missing_inputs": "MISSING_GAP_BETA_TAU_PACKAGE;MISSING_DELTAK_OPERATOR_NORM;MISSING_FULL_PPN_VECTOR",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_paths": source_paths,
                "source_paths_exist": all(path.exists() for path in source_paths),
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def package_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CPG2604_0_tail_law",
            "clause": "screened-tail derivative law",
            "current_status": "CONDITIONAL_THEOREM_AVAILABLE",
            "evidence": "1746/2604 derive the massive/exponential branch estimate abs(nabla U_B)<=C_U U_B/ell_tr",
            "claim_effect": "helps x_U only after source package is signed",
        },
        {
            "gate_id": "CPG2604_1_gap",
            "clause": "canonical mass gap mu_m2",
            "current_status": "MISSING_SOURCE_BACKED_CANONICAL_GAP",
            "evidence": "1746/1747 identify mu_m2 as the invariant range/gap",
            "claim_effect": "ell_tr cannot be numeric or parent-owned",
        },
        {
            "gate_id": "CPG2604_2_amplitude",
            "clause": "canonical exterior amplitude Phi_S",
            "current_status": "MISSING_CANONICAL_AMPLITUDE",
            "evidence": "tail profile needs source/boundary amplitude",
            "claim_effect": "q_loc, wall and PPN amplitudes cannot be scored",
        },
        {
            "gate_id": "CPG2604_3_coupling",
            "clause": "beta_source beta_test or g_c=0",
            "current_status": "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED",
            "evidence": "1747 coupling-source-silence package remains unsigned",
            "claim_effect": "range suppression cannot replace coupling suppression",
        },
        {
            "gate_id": "CPG2604_4_source_weight",
            "clause": "Delta_w/action-weight source normalization",
            "current_status": "ACTIVE_COUNTEREXAMPLE_RETAINED",
            "evidence": "1747 keeps action-weight/source rows mandatory",
            "claim_effect": "Newton/source side remains open",
        },
        {
            "gate_id": "CPG2604_5_bound_anchor",
            "clause": "WEP/clock/local bound anchor",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_ONLY",
            "evidence": "1747 imports a real MICROSCOPE-style Delta_w*tau anchor but not an MTS prediction",
            "claim_effect": "can validate units/schema, not theory pass",
        },
        {
            "gate_id": "CPG2604_6_wall",
            "clause": "transition wall and boundary residual",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "evidence": "1746/1747 retain wall and shell residual forms",
            "claim_effect": "needs L_wall, support overlap, projection constants",
        },
        {
            "gate_id": "CPG2604_7_DeltaK",
            "clause": "Khat/DeltaK subtraction silence or finite bound",
            "current_status": "PROJECTION_SCHEMA_WRITTEN_COMPONENTS_MISSING",
            "evidence": "2603 keeps S_Delta as live retained source channel",
            "claim_effect": "PPN/local residual vector remains blocked",
        },
        {
            "gate_id": "CPG2604_8_verdict",
            "clause": "whole local tail-to-GR package",
            "current_status": "NOT_CLOSED_NONCLAIM",
            "evidence": "tail maths is conditionally good; source package and local residual vector are not",
            "claim_effect": "no local-GR/Newton/PPN/R10/WEP reentry",
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def canonical_bridge_rows() -> list[dict[str, Any]]:
    source_paths = [
        OUT / "P8_Y5_PARENT_QLOC_1746_CANONICAL_SOURCE_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv",
        OUT / "P8_Y5_PARENT_QLOC_1747_COUPLING_SOURCE_SILENCE_GATE.csv",
        OUT / "P8_Y5_PARENT_QLOC_1747_BOUND_ANCHOR_IMPORT.csv",
        OUT / "P8_Y5_PARENT_QLOC_1747_WALL_BOUND_ROW.csv",
    ]
    rows = [
        {
            "row_id": "CSR2604_0_mu_m2",
            "quantity": "mu_m2",
            "formula_or_role": "ell_tr=1/sqrt(mu_m2)",
            "current_status": "MISSING_SOURCE_BACKED_CANONICAL_GAP",
            "needed_to_promote": "parent Hessian/kinetic ratio or direct canonical gap theorem",
        },
        {
            "row_id": "CSR2604_1_Phi_S",
            "quantity": "Phi_S",
            "formula_or_role": "phi(d)<=Phi_S exp(-d/ell_tr)",
            "current_status": "MISSING_CANONICAL_AMPLITUDE",
            "needed_to_promote": "boundary/source theorem or finite amplitude bound",
        },
        {
            "row_id": "CSR2604_2_domain_distance",
            "quantity": "d",
            "formula_or_role": "distance from local support to active source or transition boundary",
            "current_status": "MISSING_DOMAIN_DISTANCE",
            "needed_to_promote": "source/support geometry and local arena worldtube",
        },
        {
            "row_id": "CSR2604_3_beta_source_test",
            "quantity": "beta_source*beta_test",
            "formula_or_role": "finite exchange coupling product if source not zero",
            "current_status": "PRODUCT_LAW_READY_VALUES_MISSING",
            "needed_to_promote": "derive beta=0 theorem or source numeric beta legs",
        },
        {
            "row_id": "CSR2604_4_Delta_w_tau_WEP",
            "quantity": "Delta_w*tau_WEP",
            "formula_or_role": "relative source-weight/readout product for WEP-style local tests",
            "current_status": "BOUND_ANCHOR_EXISTS_MTS_PREDICTION_MISSING",
            "needed_to_promote": "tau_WEP map, material map, source current and MTS prediction row",
        },
        {
            "row_id": "CSR2604_5_projection_norms",
            "quantity": "A_ref;N_div;N_G;N_D",
            "formula_or_role": "operator/projection/normalization bridge to observables",
            "current_status": "MISSING_OPERATOR_PROJECTION_NORMS",
            "needed_to_promote": "local residual norm convention and arena operator maps",
        },
        {
            "row_id": "CSR2604_6_wall_width",
            "quantity": "L_wall;support_overlap",
            "formula_or_role": "finite transition-wall residual inputs",
            "current_status": "MISSING_SUPPORT_DOMAIN_AND_WALL_WIDTH",
            "needed_to_promote": "local support exclusion theorem or wall-overlap bound",
        },
        {
            "row_id": "CSR2604_7_boundary_shell",
            "quantity": "Q_shell_boundary",
            "formula_or_role": "C_shell A_B U_B^pB/(L0^2 L_wall) plus projector/readout tails",
            "current_status": "BOUND_FORM_ONLY_INPUTS_MISSING",
            "needed_to_promote": "boundary no-flux theorem or finite shell contribution",
        },
        {
            "row_id": "CSR2604_8_DeltaK",
            "quantity": "S_Delta",
            "formula_or_role": "S_Delta^nu=-Pi_gamma[P_loc nabla_mu Delta_K^{mu nu}]",
            "current_status": "SCHEMA_WRITTEN_COMPONENTS_MISSING",
            "needed_to_promote": "DeltaK components, projectors, units and operator norm bound",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_paths": source_paths,
                "source_paths_exist": all(path.exists() for path in source_paths),
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "runner_id": "RUN2604_0_tail_law_adoption",
            "target": "promote screened-tail theorem into x_U/q_loc profile",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_MU_M2;MISSING_PHI_S;MISSING_DOMAIN_DISTANCE;MISSING_SOURCE_SILENCE;MISSING_BOUNDARY_CLASS",
        },
        {
            "runner_id": "RUN2604_1_gamma_score",
            "target": "sigmaX to Cassini gamma score",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "TAIL_THEOREM_CONDITIONAL_ONLY;MISSING_BG_VALUE;MISSING_XU_NUMERIC;MISSING_DELTAK_BOUND",
        },
        {
            "runner_id": "RUN2604_2_WEP_tau_score",
            "target": "WEP/clock/local tau source score",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "BOUND_ANCHOR_ONLY;MISSING_TAU_MAP;MISSING_BETA_LEGS;MISSING_MTS_PREDICTION_ROW",
        },
        {
            "runner_id": "RUN2604_3_wall_bound_score",
            "target": "transition-wall residual score",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_L_WALL;MISSING_SUPPORT_OVERLAP;MISSING_C_WALL;MISSING_SHELL_PROJECTOR",
        },
        {
            "runner_id": "RUN2604_4_local_GR",
            "target": "local GR/Newton recovery",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "NO_PARENT_SOURCE_PACKAGE;NO_DELTAK_BOUND;NO_FULL_PPN_VECTOR;NO_R10_OR_WEP_PREDICTION_ROW",
        },
    ]
    return [with_stamp({**row, "accepted_for_scoring": False, "claim_allowed": False, "valid_for_claim": False}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2604_0_tail_theorem",
            "claim": "a massive source-free tail gives abs(nabla U_B)<=C_U U_B/ell_tr",
            "gate_status": "PASS_NONCLAIM_ONLY",
            "reason": "valid as a conditional mathematical theorem; not yet parent-owned by MTS coefficients",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2604_1_q_loc_suppression",
            "claim": "q_loc is locally suppressed enough for PPN/local GR",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "requires mu_m2, Phi_S, d, source silence, boundary class, projection norms and DeltaK subtraction",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2604_2_coupling_zero",
            "claim": "local matter/source coupling is zero",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "quotient kernel, matter functor, current owner and action-weight clauses remain unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2604_3_wall_bound",
            "claim": "transition wall residual is finite and below local bounds",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "only the bound form exists; L_wall, overlap, constants and shell terms are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2604_4_local_GR",
            "claim": "local GR/Newton branch is derived",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "conditional tail theorem is not enough without a full parent source package and residual vector",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2604_0_tail_math",
            "decision": "accept the screened-tail derivative law as a conditional theorem",
            "reason": "the massive/exponential exterior branch gives the needed gradient law without an amplitude-to-gradient shortcut",
            "effect": "the gradient trap is not a fatal calculus objection",
        },
        {
            "decision_id": "DEC2604_1_no_promotion",
            "decision": "do not promote the tail theorem into a local-GR claim",
            "reason": "the parent gap, amplitude, source silence, beta legs, wall inputs and DeltaK norm are missing",
            "effect": "all PPN/R10/WEP/Newton/local-GR claims remain blocked",
        },
        {
            "decision_id": "DEC2604_2_best_next",
            "decision": "select the gap-beta-tau source package validator",
            "reason": "the next live bottleneck is ownership of mu_m2, Phi_S, beta_source/test, Delta_w*tau_WEP, projection norms and wall residuals",
            "effect": "2605 should either source/package those rows or derive one parent zero theorem",
        },
        {
            "decision_id": "DEC2604_3_fallback",
            "decision": "retain DeltaK/Khat component-norm route as fallback",
            "reason": "S_Delta remains a live local source channel if the canonical package does not close",
            "effect": "do not erase Khat; bound or derive it",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2604_0_selected",
            "selection_status": "selected",
            "target_file": "2605-Y5-R2FR-gap-beta-tau-source-package-validator-or-parent-row.md",
            "target_script": "scripts/Y5_R2FR_gap_beta_tau_source_package_validator_or_parent_row_2605.py",
            "task": "validate or source the first live canonical local package rows: mu_m2, Phi_S, beta_source/test, Delta_w*tau_WEP, tau_WEP, tails, projection norms and wall bounds; or derive one parent zero theorem",
            "success_condition": "at least one package leg is source-backed or parent-derived, and all nonclaim rows keep claim gates locked until the whole chain closes",
            "fallback_condition": "if package rows cannot be sourced, move to DeltaK/Khat component/operator norm bound",
            "guardrails": "no range-suppression-as-coupling-suppression; no local-GR claim; no numeric PPN/R10/WEP claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2604_1_DeltaK_fallback",
            "selection_status": "held_fallback",
            "target_file": "2605b-Y5-R2FR-DeltaK-component-operator-norm-bound.md",
            "target_script": "scripts/Y5_R2FR_DeltaK_component_operator_norm_bound_2605b.py",
            "task": "source DeltaK components, projectors, units and operator norms if the gap-beta-tau package remains blocked",
            "success_condition": "S_Delta rows carry sourced components and finite bounds without claiming local GR",
            "fallback_condition": "retain explicit closure-only residual",
            "guardrails": "no Khat silence by assertion; no component deletion; no local-GR claim",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2604_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "accepted_for_scoring",
        "valid_prediction_row",
    }
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2604_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    expected_lineage = {"LIN2604_0_2603", "LIN2604_1_1746", "LIN2604_2_1747"}
    add("VAL2604_01_lineage_complete", expected_lineage == {row["step_id"] for row in data["lineage"]}, "lineage ledger covers 2603 plus prior 1746-1747")
    expected_theorems = {"TD2604_1_exponential_tail_solution", "TD2604_4_wall_counterbranch", "TD2604_5_current_verdict"}
    add("VAL2604_02_tail_theorem_complete", expected_theorems.issubset({row["theorem_id"] for row in data["tail_theorem"]}), "tail theorem table includes exponential tail, wall counterbranch and verdict")
    add("VAL2604_03_tail_sources_exist", all(row["source_paths_exist"] is True for row in data["tail_theorem"]), "tail theorem rows cite existing local sources")
    expected_package_clauses = {"screened-tail derivative law", "canonical mass gap mu_m2", "canonical exterior amplitude Phi_S", "beta_source beta_test or g_c=0", "Delta_w/action-weight source normalization", "WEP/clock/local bound anchor", "transition wall and boundary residual", "Khat/DeltaK subtraction silence or finite bound", "whole local tail-to-GR package"}
    add("VAL2604_04_package_gate_complete", expected_package_clauses.issubset({row["clause"] for row in data["package_gate"]}), "canonical package gate covers tail, gap, amplitude, coupling, source weight, bound anchor, wall, DeltaK and verdict")
    expected_bridge = {"mu_m2", "Phi_S", "d", "beta_source*beta_test", "Delta_w*tau_WEP", "A_ref;N_div;N_G;N_D", "L_wall;support_overlap", "Q_shell_boundary", "S_Delta"}
    add("VAL2604_05_canonical_bridge_complete", expected_bridge.issubset({row["quantity"] for row in data["canonical_bridge"]}), "canonical bridge rows cover gap, amplitude, domain, beta, tau, projection, wall, shell and DeltaK")
    add("VAL2604_06_bridge_sources_exist", all(row["source_paths_exist"] is True for row in data["canonical_bridge"]), "canonical bridge rows cite existing local sources")
    add("VAL2604_07_bound_anchor_nonclaim", any(row["gate_id"] == "CPG2604_5_bound_anchor" and row["current_status"] == "SOURCE_BACKED_BOUND_ANCHOR_ONLY" for row in data["package_gate"]), "real bound anchor is retained as nonclaim only")
    add("VAL2604_08_runner_refuses", all(row["accepted_for_scoring"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "all scoring runners refuse promotion")
    add("VAL2604_09_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]) and any(row["gate_id"] == "CG2604_0_tail_theorem" and row["gate_status"] == "PASS_NONCLAIM_ONLY" for row in data["claim_gates"]), "claim gates allow only a conditional nonclaim theorem")
    add("VAL2604_10_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2604-Y5-R2FR-screened-tail*",
            "*Y5_R2FR_screened_tail*2604*",
            "*P8_Y5_TAIL_LAW_REBASE_2604*",
            "*JR2604*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2604_11_no_formalization_artifacts", not formalization_artifacts, "no 2604 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2604_12_next_selected", any(row["route_id"] == "NEXT2604_0_selected" and "2605-Y5-R2FR-gap-beta-tau-source-package-validator" in row["target_file"] for row in data["next"]), "2605 gap-beta-tau source package validator selected")
    add("VAL2604_13_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2604_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2604_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2604_OVERALL",
        overall,
        "2604 rebases the screened-tail theorem, accepts the conditional derivative law, blocks local claims, and selects gap-beta-tau package validation next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2604 Y5 R2FR screened-tail derivative law or finite transition-wall bound",
        "",
        "**Status:** private nonclaim rebase checkpoint. The 2603 tail-law target is now sharpened: the differential tail law is mathematically available on a source-free massive/exponential branch, but it is not promoted to local GR because the parent source package is still unsigned.",
        "",
        "**Main result:** the gradient objection is not fatal. If the local exterior really obeys a positive-gap source-free operator, then `U_B~exp(-d/ell_tr)` gives `abs(nabla U_B)<=C_U U_B/ell_tr`, so the double-zero branch can in principle suppress the gradient terms that worried us. But this is only a conditional theorem. MTS still needs source-backed `mu_m2`, `Phi_S`, domain distance, coupling/source-silence rows, projection norms, wall/shell bounds, and the `DeltaK/Khat` residual before any PPN, R10, WEP, Newton, or local-GR claim is allowed.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Tail Derivative Theorem",
        markdown_table(data["tail_theorem"], ["theorem_id", "claim", "calculation", "current_status", "promotion_status", "missing_inputs", "source_paths", "source_paths_exist", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Canonical Package Gate",
        markdown_table(data["package_gate"], ["gate_id", "clause", "current_status", "evidence", "claim_effect", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Canonical Source Bridge",
        markdown_table(data["canonical_bridge"], ["row_id", "quantity", "formula_or_role", "current_status", "needed_to_promote", "source_paths", "source_paths_exist", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target", "verdict", "failure_reasons", "accepted_for_scoring", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This is a good kind of progress, chume: not a victory lap, but a trap disarmed. We no longer have to fear that double zeros automatically fail because gradients exist; a screened massive tail can carry the needed derivative suppression. The hard work now moves to ownership: prove or source the gap, amplitude, coupling/source-silence, tau/readout, projection and wall inputs. If those do not close, the local branch stays closure-only rather than pretending to be GR.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "tail_theorem": tail_theorem_rows(),
        "package_gate": package_gate_rows(),
        "canonical_bridge": canonical_bridge_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["tail_theorem"], data["tail_theorem"])
    write_csv(OUTPUTS["package_gate"], data["package_gate"])
    write_csv(OUTPUTS["canonical_bridge"], data["canonical_bridge"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2604_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
