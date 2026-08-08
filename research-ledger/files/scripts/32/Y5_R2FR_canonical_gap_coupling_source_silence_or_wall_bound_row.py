from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1747"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1747 - Canonical Gap Coupling Source Silence Or Wall Bound Row"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1747_0_1746_doc",
        "source_key": "1746_handoff",
        "source_path": ROOT / "1746-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md",
        "needles": ["NEXT1746_0_primary", "TARGET_PARENT_GAP_COUPLING_OR_WALL_BOUND"],
    },
    {
        "source_id": "SRC1747_1_1746_tail",
        "source_key": "1746_tail_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_TAIL_DERIVATIVE_THEOREM.csv",
        "needles": ["TD1746_1_exponential_tail_solution", "SCREENED_TAIL_DERIVATIVE_LAW_DERIVED_CONDITIONALLY"],
    },
    {
        "source_id": "SRC1747_2_1746_sources",
        "source_key": "1746_canonical_source_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_CANONICAL_SOURCE_ROWS.csv",
        "needles": ["CSR1746_0_mu_m2", "MISSING_SOURCE_BACKED_CANONICAL_GAP"],
    },
    {
        "source_id": "SRC1747_3_1592_canonical",
        "source_key": "1592_canonical_transition",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1592_CANONICAL_TRANSITION_THEOREM.csv",
        "needles": ["CTT1592_8_verdict", "CONDITIONAL_CANONICAL_THEOREM_DERIVED_NONCLAIM"],
    },
    {
        "source_id": "SRC1747_4_1593_zero",
        "source_key": "1593_coupling_zero",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1593_CANONICAL_COUPLING_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["ZTH1593_8_verdict", "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED"],
    },
    {
        "source_id": "SRC1747_5_1593_package",
        "source_key": "1593_package_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1593_MATTER_PACKAGE_CLAUSE_GATE.csv",
        "needles": ["PKG1593_8_verdict", "PACKAGE_FAILS_CURRENT_CLAIM"],
    },
    {
        "source_id": "SRC1747_6_1594_validator",
        "source_key": "1594_beta_validator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_RESULTS.csv",
        "needles": ["BVR1594_VERDICT", "NO_ACCEPTED_BETA_ROWS"],
    },
    {
        "source_id": "SRC1747_7_1595_bound",
        "source_key": "1595_bound_anchor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv",
        "needles": ["SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor", "EXPLICIT_BOUND_SOURCE_BACKED"],
    },
    {
        "source_id": "SRC1747_8_1693_gate",
        "source_key": "1693_coupling_action_weight_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1693_COUPLING_AND_ACTION_WEIGHT_GATE.csv",
        "needles": ["COUP1693_7_verdict", "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED"],
    },
    {
        "source_id": "SRC1747_9_1694_current",
        "source_key": "1694_current_beta_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
        "needles": ["BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor", "BDW1694_4_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_SOURCE_REGISTER.csv",
    "canonical_package_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_CANONICAL_PACKAGE_GATE.csv",
    "gap_amplitude_source_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv",
    "coupling_source_silence_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_COUPLING_SOURCE_SILENCE_GATE.csv",
    "bound_anchor_import": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_BOUND_ANCHOR_IMPORT.csv",
    "wall_bound_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_WALL_BOUND_ROW.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1747_VALIDATION.csv",
}


COPY_MAP = {
    "canonical_package_gate": "R2FR_1747_CANONICAL_PACKAGE_GATE.csv",
    "gap_amplitude_source_gate": "R2FR_1747_GAP_AMPLITUDE_SOURCE_GATE.csv",
    "coupling_source_silence_gate": "R2FR_1747_COUPLING_SOURCE_SILENCE_GATE.csv",
    "bound_anchor_import": "R2FR_1747_BOUND_ANCHOR_IMPORT.csv",
    "wall_bound_row": "R2FR_1747_WALL_BOUND_ROW.csv",
    "runner_refusal": "R2FR_1747_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1747_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1747_CLAIM_GATE.csv",
    "next_target": "R2FR_1747_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def canonical_package_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CPG1747_0_tail_law", "screened-tail derivative law", "CONDITIONAL_THEOREM_AVAILABLE", "1746 derives |nabla U_B|=U_B/ell_tr for the massive/exponential branch", "not enough without source package"),
        ("CPG1747_1_gap", "canonical mass gap mu_m^2", "MISSING_SOURCE_BACKED_CANONICAL_GAP", "1592/1746 identify mu_m^2 as the invariant range/gap", "ell_tr cannot become numeric or claim-grade"),
        ("CPG1747_2_amplitude", "canonical exterior amplitude Phi_S", "MISSING_CANONICAL_AMPLITUDE", "tail profile needs boundary/source amplitude", "Q_alg and wall residuals cannot score"),
        ("CPG1747_3_coupling", "beta_source beta_test or g_c=0", "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED", "1593/1693 keep the matter package gates unsigned", "range suppression cannot replace coupling suppression"),
        ("CPG1747_4_source_weight", "Delta_w/action-weight source normalization", "ACTIVE_COUNTEREXAMPLE_RETAINED", "1594 rejects the w_A exclusion theorem and validator rejects templates", "Newton/source side remains open"),
        ("CPG1747_5_bound_anchor", "MICROSCOPE Delta_w*tau bound anchor", "SOURCE_BACKED_BOUND_ANCHOR_ONLY", "1595/1694 import a real bound anchor", "not an MTS prediction without tau_WEP/source map"),
        ("CPG1747_6_wall", "transition wall/boundary residual", "BOUND_FORM_ONLY_NONCLAIM", "1746 keeps wall counterbranch", "needs L_wall/support/projection/amplitudes"),
        ("CPG1747_7_verdict", "whole canonical local source package", "NOT_CLOSED_NONCLAIM", "tail maths is good, source package is not", "no local-GR/Newton/PPN/R10 reentry"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "clause": clause,
            "current_status": status,
            "evidence": evidence,
            "claim_effect": effect,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for gate_id, clause, status, evidence, effect in rows
    ]


def gap_amplitude_source_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GAS1747_0_mu_m2", "mu_m^2", "ell_tr=1/sqrt(mu_m^2)", "MISSING_SOURCE_BACKED_CANONICAL_GAP", "parent Hessian/kinetic ratio or direct canonical gap theorem"),
        ("GAS1747_1_Phi_S", "Phi_S", "phi(d)<=Phi_S exp(-d/ell_tr)", "MISSING_CANONICAL_AMPLITUDE", "boundary/source theorem or finite amplitude bound"),
        ("GAS1747_2_d", "d", "distance from local test support to active source/transition boundary", "MISSING_DOMAIN_DISTANCE", "source/support geometry and local arena worldtube"),
        ("GAS1747_3_corrections", "epsilon_Z;epsilon_tail", "curvature/domain/readout corrections to exponential tail", "MISSING_TAIL_ENVELOPE", "tail component bounds or theorem-zero clauses"),
        ("GAS1747_4_projection", "A_ref;N_div;N_G;N_D", "operator/projection norms for observables", "MISSING_OPERATOR_PROJECTION_NORMS", "local residual norm convention and arena operator maps"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_role": role,
            "current_status": status,
            "needed_to_promote": needed,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for row_id, quantity, role, status, needed in rows
    ]


def coupling_source_silence_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CSS1747_0_q_kernel", "Dq_loc[v_phi]=0", "UNSIGNED_KERNEL", "finite beta_geom/qbar row retained"),
        ("CSS1747_1_coframe", "e_obs=Obs_e(q) and no shadow frame", "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED", "finite geometry/shadow-frame coupling retained"),
        ("CSS1747_2_matter_functor", "ordinary matter bundle and vertical lift", "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED", "finite matter-lift/source rows retained"),
        ("CSS1747_3_constants", "ordinary constants/material labels phi-blind", "CONSTANT_SUPERSELECTION_UNSIGNED", "finite beta_const/material rows retained"),
        ("CSS1747_4_action_weights", "no independent w_A S_A", "ACTIVE_COUNTEREXAMPLE", "Delta_w and beta_w rows mandatory"),
        ("CSS1747_5_current_owner", "single Hilbert/source current with Bianchi descent", "CURRENT_OWNER_NOT_DERIVED", "source residual vector retained"),
        ("CSS1747_6_boundary_readout", "boundary/projector/readout tails zero or bounded", "BOUNDARY_READOUT_UNSIGNED", "epsilon_tail rows mandatory"),
        ("CSS1747_7_verdict", "whole source-silence package", "PACKAGE_FAILS_CURRENT_CLAIM", "g_c=0 and beta=0 not claimed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "required_clause": clause,
            "current_status": status,
            "fallback": fallback,
            "clause_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for gate_id, clause, status, fallback in rows
    ]


def bound_anchor_import_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BAI1747_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "quantity": "P_WEP_relative_source_weight",
            "definition": "absolute product bound P=abs(Delta_w_TiPt*tau_WEP)",
            "value_or_bound": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv"),
            "source_anchor": "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "extraction_method": "imported_current_branch_source_backed_bound_anchor",
            "beta_convention": "Delta_w_TiPt*tau_WEP_product_bound_not_individual_beta",
            "arena_map": "MICROSCOPE_WEP;Newton/common_matter_guard;no_R10_or_PPN_score",
            "current_status": "BOUND_ANCHOR_IMPORTED_NONPREDICTION",
            "missing_before_score": "tau_WEP;source_worldtube;material_map;readout_kernel;MTS_prediction",
            "schema_provenance_pass": "True",
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BAI1747_1_current_beta_verdict",
            "quantity": "beta/Delta_w current branch",
            "definition": "one source-backed bound anchor exists, but no MTS beta/Delta_w prediction row exists",
            "value_or_bound": "NONCLAIM_ONLY",
            "units": "mixed",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv"),
            "source_anchor": "BDW1694_4_verdict",
            "extraction_method": "current_branch_validator_status",
            "beta_convention": "canonical_phi_and_Delta_w_conventions_still_required",
            "arena_map": "all_local_arenas_blocked",
            "current_status": "NO_ACCEPTED_PREDICTION_ROW",
            "missing_before_score": "tau_WEP;beta_source;beta_test;Delta_w prediction or theorem-zero",
            "schema_provenance_pass": no(),
            "accepted_for_scoring": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def wall_bound_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "WBR1747_0_transition_wall_gradient",
            "residual": "Q_wall_grad",
            "bound_form": "Q_wall_grad <= C_wall A_S^2 U_B/L_wall",
            "role": "fallback if local support intersects sharp transition wall rather than exponential tail",
            "needed_inputs": "MISSING_C_WALL;MISSING_A_S;MISSING_U_B;MISSING_L_WALL;MISSING_SUPPORT_OVERLAP;MISSING_ARENA_PROJECTION",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "WBR1747_1_boundary_shell",
            "residual": "Q_shell_boundary",
            "bound_form": "Q_shell_boundary <= C_shell A_B U_B^pB/(L0^2 L_wall) + retained projector/readout tails",
            "role": "prevents generic shell suppression from being smuggled into local-GR recovery",
            "needed_inputs": "MISSING_C_SHELL;MISSING_A_B;MISSING_pB;MISSING_L0;MISSING_BOUNDARY_PROJECTOR;MISSING_TAIL_ENVELOPE",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1747_0_tail_package", "canonical tail package adoption", "REFUSE_CLAIM_RUN", "tail law is conditional but mu_m2/Phi_S/source/boundary package is missing"),
        ("RUN1747_1_coupling_zero", "g_c=0 or beta_source=beta_test=0", "REFUSE_CLAIM_RUN", "1593/1693 matter package gates fail and action-weight counterexample remains active"),
        ("RUN1747_2_bound_anchor", "MICROSCOPE Delta_w_tau bound anchor", "REFUSE_SCORE_RUN", "anchor is not an MTS prediction and tau_WEP/source projection is missing"),
        ("RUN1747_3_wall_bound", "finite wall residual scorer", "REFUSE_SCORE_RUN", "wall bound has no sourced amplitudes, support overlap or projection norms"),
        ("RUN1747_4_local_GR", "local GR/Newton/PPN reentry", "REFUSE_CLAIM_RUN", "source/coupling/conservation/Newton gates do not close together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "runner": runner,
            "current_status": status,
            "reason": reason,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for runner_id, runner, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1747_0_tail_status",
            "decision": "TAIL_MATH_READY_SOURCE_PACKAGE_BLOCKED",
            "reason": "1746 gives the required derivative law conditionally, but mu_m2/Phi_S/domain/projection rows remain missing",
            "next_action": "source canonical gap/amplitude or keep wall-bound fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1747_1_coupling_status",
            "decision": "COUPLING_ZERO_NOT_CLOSED",
            "reason": "g_c=0 requires q-kernel, coframe, matter functor, constants, action weights, current owner and boundary/readout silence under one parent action",
            "next_action": "do not use range suppression as coupling suppression; keep beta/Delta_w rows live",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1747_2_bound_status",
            "decision": "BOUND_ANCHOR_IMPORTED_BUT_NO_MTS_PREDICTION",
            "reason": "MICROSCOPE Delta_w*tau bound is source-backed but tau_WEP/source-worldtube/material/readout map is absent",
            "next_action": "source tau_WEP/readout projection before any WEP/Newton use",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1747_3_best_next",
            "decision": "TARGET_GAP_BETA_TAU_SOURCE_PACKAGE_VALIDATOR",
            "reason": "the next useful progress is a unified validator/source pack for mu_m2, Phi_S, beta legs, Delta_w/tau_WEP, tails and wall bounds",
            "next_action": "build 1748 source-package validator or derive one of those rows from parent action",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("GATE1747_0_tail_law", "screened-tail derivative law is live parent-signed", "BLOCKED_PARENT_SOURCE_PACKAGE"),
        ("GATE1747_1_gap_profile", "canonical gap/amplitude profile is source-backed", "BLOCKED_MU_PHI_DISTANCE_INPUTS"),
        ("GATE1747_2_coupling_zero", "g_c=0 or beta_source beta_test zero", "BLOCKED_MATTER_PACKAGE_UNSIGNED"),
        ("GATE1747_3_bound_anchor", "MICROSCOPE bound anchor is an MTS prediction", "BLOCKED_TAU_WEP_SOURCE_MAP"),
        ("GATE1747_4_wall_bound", "transition-wall residual is numerically bounded", "BLOCKED_WALL_INPUTS_MISSING"),
        ("GATE1747_5_local_GR", "local GR/Newton/PPN/R10/WEP scoring can reopen", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": blocker,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for gate_id, claim, blocker in claims
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1747_0_primary",
            "next_target": "1748-Y5-R2FR-gap-beta-tau-source-package-validator-or-parent-row.md",
            "script": "scripts/Y5_R2FR_gap_beta_tau_source_package_validator_or_parent_row.py",
            "objective": "validate/source the first live canonical local package rows: mu_m2, Phi_S, beta_source/test, Delta_w*tau_WEP, tau_WEP, tails, projection norms, and wall bounds; or derive one parent zero theorem",
            "success_condition": "at least one row is parent-signed/source-backed and validator-readable without becoming a score, or a stricter blocker ledger identifies the remaining source package gap",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1747_1_DeltaK",
            "next_target": "1748b-Y5-R2FR-DeltaK-component-operator-norm-bound.md",
            "script": "scripts/Y5_R2FR_DeltaK_component_operator_norm_bound.py",
            "objective": "continue Khat/DeltaK residual path if canonical source package remains blocked",
            "success_condition": "source-backed S_Delta operator norm row or stricter nonclaim refusal",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "canonical_package_gate": canonical_package_gate_rows(),
        "gap_amplitude_source_gate": gap_amplitude_source_gate_rows(),
        "coupling_source_silence_gate": coupling_source_silence_gate_rows(),
        "bound_anchor_import": bound_anchor_import_rows(),
        "wall_bound_row": wall_bound_row_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1747_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1747_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"accepted_for_scoring", "claim_allowed", "clause_signed", "gate_pass", "score_ready", "valid_for_claim", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {"accepted_for_scoring", "claim_allowed", "gate_pass", "score_ready", "valid_for_claim", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1747_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1747_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1747*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    package = rows_map["canonical_package_gate"]
    gap = rows_map["gap_amplitude_source_gate"]
    coupling = rows_map["coupling_source_silence_gate"]
    bound = rows_map["bound_anchor_import"]
    wall = rows_map["wall_bound_row"]
    runners = rows_map["runner_refusal"]
    decisions = rows_map["decision"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1747_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1747_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more required source needles missing"),
        check("VAL1747_2_tail_kept_conditional", any(row["gate_id"] == "CPG1747_0_tail_law" and row["current_status"] == "CONDITIONAL_THEOREM_AVAILABLE" for row in package), "tail law retained as conditional theorem", "tail law gate missing"),
        check("VAL1747_3_gap_inputs_blocked", any(row["row_id"] == "GAS1747_0_mu_m2" and row["current_status"] == "MISSING_SOURCE_BACKED_CANONICAL_GAP" for row in gap), "canonical gap source gate remains blocked", "mu_m2 blocker missing"),
        check("VAL1747_4_coupling_package_fails", any(row["gate_id"] == "CSS1747_7_verdict" and row["current_status"] == "PACKAGE_FAILS_CURRENT_CLAIM" for row in coupling), "coupling source-silence package fail is explicit", "coupling package verdict missing"),
        check("VAL1747_5_bound_anchor_imported_nonclaim", any(row["row_id"] == "BAI1747_0_MICROSCOPE_Delta_w_tau_bound_anchor" and row["schema_provenance_pass"] == "True" and row["valid_prediction_row"] == "False" for row in bound), "source-backed bound anchor imported as nonprediction", "bound anchor missing or promoted"),
        check("VAL1747_6_wall_bounds_nonclaim", all(row["current_status"] == "BOUND_FORM_ONLY_NONCLAIM" and row["score_ready"] == "False" for row in wall), "wall bound rows remain nonclaim", "wall row became score-ready"),
        check("VAL1747_7_runners_refuse", all(row["current_status"].startswith("REFUSE") and row["claim_allowed"] == "False" for row in runners), "all claim/score runners refuse", "one or more runners opened"),
        check("VAL1747_8_decision_next", any(row["decision_id"] == "DEC1747_3_best_next" and row["decision"] == "TARGET_GAP_BETA_TAU_SOURCE_PACKAGE_VALIDATOR" for row in decisions), "decision selects gap/beta/tau source package validator", "decision next route missing"),
        check("VAL1747_9_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1747_10_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1747_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a missing row is marked ready"),
        check("VAL1747_12_next_selected", any(row["route_id"] == "NEXT1747_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1747_13_csv_parse", parsed_ok, "all generated 1747 CSVs parse", "one or more generated CSVs failed to parse"),
        check("VAL1747_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1747_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1747_16_formalization_untouched", formalization_untouched(), "no 1747 outputs found under formalization-workbench", "1747 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1747_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1747 canonical gap coupling source silence or wall-bound validation" if overall else "one or more 1747 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1747 merges the two live strands: the screened-tail derivative law is mathematically available, but the source/coupling package is still not signed.",
        "- The canonical local package now has a clean checklist: `mu_m^2`, `Phi_S`, domain distance, projection norms, `beta_source beta_test`, `Delta_w*tau_WEP`, tail envelope, and wall/shell residuals.",
        "- Existing evidence gives one real source-backed bound anchor, the MICROSCOPE `abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15`, but this is not an MTS prediction and cannot score without `tau_WEP` and source/readout projection.",
        "- Therefore no local-GR/Newton/PPN/R10/WEP reentry is allowed yet; range suppression, by itself, is not coupling suppression.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Canonical Package Gate",
        markdown_table(rows_map["canonical_package_gate"], ["gate_id", "clause", "current_status", "evidence", "claim_effect"]),
        "",
        "## Gap And Amplitude Source Gate",
        markdown_table(rows_map["gap_amplitude_source_gate"], ["row_id", "quantity", "formula_or_role", "current_status", "needed_to_promote"]),
        "",
        "## Coupling Source-Silence Gate",
        markdown_table(rows_map["coupling_source_silence_gate"], ["gate_id", "required_clause", "current_status", "fallback"]),
        "",
        "## Bound Anchor Import",
        markdown_table(rows_map["bound_anchor_import"], ["row_id", "quantity", "value_or_bound", "current_status", "missing_before_score"]),
        "",
        "## Wall Bound Rows",
        markdown_table(rows_map["wall_bound_row"], ["bound_id", "residual", "bound_form", "current_status", "needed_inputs"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["runner_id", "runner", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is where the branch becomes genuinely test-shaped: not public evidence, but the route to evidence is now finite. The theory either derives/source-fills the canonical local package, or it must carry explicit finite residuals into local tests. No more vague plateau, no more hiding coupling in range, no more absorbing relative source weights into measured `G_N`.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1747-Y5-R2FR-canonical-gap-coupling-source-silence-or-wall-bound-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1747_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1747 validation FAIL")
    print("1747 validation PASS")


if __name__ == "__main__":
    main()
