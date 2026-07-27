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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1749"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1749 - Parent Gap Amplitude Row Or Tau-Min Source Pack"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1749_0_1748_doc",
        "source_key": "1748_handoff",
        "source_path": ROOT / "1748-Y5-R2FR-gap-beta-tau-source-package-validator-or-parent-row.md",
        "needles": ["NEXT1748_0_primary", "TARGET_PARENT_GAP_OR_SOURCE_AMPLITUDE_FIRST"],
    },
    {
        "source_id": "SRC1749_1_1592_theorem",
        "source_key": "1592_canonical_transition_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1592_CANONICAL_TRANSITION_THEOREM.csv",
        "needles": ["CTT1592_2_static_exterior_solution", "CTT1592_4_Qalg_bound"],
    },
    {
        "source_id": "SRC1749_2_1592_source_pack",
        "source_key": "1592_canonical_source_acquisition",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1592_QNORM_CANONICAL_SOURCE_ACQUISITION.csv",
        "needles": ["CSA1592_0_mu_m2", "CSA1592_4_Phi_S"],
    },
    {
        "source_id": "SRC1749_3_1378_parent_law",
        "source_key": "1378_transition_parent_law",
        "source_path": RESIDUALS / "P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv",
        "needles": ["DER1378_3_minimal_gradient_completion", "DER1378_8_verdict"],
    },
    {
        "source_id": "SRC1749_4_1378_gradient_branch",
        "source_key": "1378_conditional_gradient_branch",
        "source_path": RESIDUALS / "P8_Y5_R10_1378_CONDITIONAL_GRADIENT_RELAXATION_BRANCH.csv",
        "needles": ["GRB1378_1_transition_length", "GRB1378_2_support_law"],
    },
    {
        "source_id": "SRC1749_5_1379_signature",
        "source_key": "1379_parent_signature_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv",
        "needles": ["GPA1379_0_action_slot", "NO_PARENT_SIGNED_GRADIENT_COMPLETION_ROW"],
    },
    {
        "source_id": "SRC1749_6_1746_tail",
        "source_key": "1746_tail_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_TAIL_DERIVATIVE_THEOREM.csv",
        "needles": ["TD1746_2_canonical_gap_rewrite", "MISSING_SOURCE_BACKED_MU_M2"],
    },
    {
        "source_id": "SRC1749_7_1748_eval",
        "source_key": "1748_package_evaluation",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_CURRENT_PACKAGE_EVALUATION.csv",
        "needles": ["EVAL1748_0_mu_m2", "EVAL1748_1_Phi_S"],
    },
    {
        "source_id": "SRC1749_8_69_R_lock",
        "source_key": "69_relaxation_functional_lock",
        "source_path": FORMALIZATION / "69-relaxation-functional-lock.md",
        "needles": ["mu_B = gamma_B lambda_R", "ell_scr = sqrt(D_m/mu_B)"],
    },
    {
        "source_id": "SRC1749_9_70_R_lock_results",
        "source_key": "70_relaxation_functional_results",
        "source_path": FORMALIZATION / "70-relaxation-functional-lock-first-results.md",
        "needles": ["relaxation_functional_lock_conditional_not_parent_derived", "boundary/source amplitude"],
    },
    {
        "source_id": "SRC1749_10_71_source_boundary",
        "source_key": "71_source_support_boundary_law",
        "source_path": FORMALIZATION / "71-source-support-boundary-law.md",
        "needles": ["Boundary Amplitude", "M_bdy exp(-ell_tr/ell_scr)"],
    },
    {
        "source_id": "SRC1749_11_72_source_boundary_results",
        "source_key": "72_source_support_boundary_results",
        "source_path": FORMALIZATION / "72-source-support-boundary-first-results.md",
        "needles": ["source_support_boundary_law_conditional_open", "weak_boundary_screening_fail"],
    },
    {
        "source_id": "SRC1749_12_79_fixed_point",
        "source_key": "79_local_fixed_point_mechanism",
        "source_path": FORMALIZATION / "79-local-fixed-point-mechanism.md",
        "needles": ["local_fixed_point_mechanism_conditional_closure_not_parent_derived", "double-zero mechanism = explicit closure"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_SOURCE_REGISTER.csv",
    "bridge_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_GAP_AMPLITUDE_BRIDGE_THEOREM.csv",
    "signature_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_PARENT_SIGNATURE_AUDIT.csv",
    "candidate_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_MU_PHI_CANDIDATE_ROWS.csv",
    "tau_fallback": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_TAU_MIN_FALLBACK_SOURCE_PACK.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1749_VALIDATION.csv",
}


COPY_MAP = {
    "bridge_theorem": "R2FR_1749_GAP_AMPLITUDE_BRIDGE_THEOREM.csv",
    "signature_audit": "R2FR_1749_PARENT_SIGNATURE_AUDIT.csv",
    "candidate_rows": "R2FR_1749_MU_PHI_CANDIDATE_ROWS.csv",
    "tau_fallback": "R2FR_1749_TAU_MIN_FALLBACK_SOURCE_PACK.csv",
    "decision": "R2FR_1749_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1749_CLAIM_GATE.csv",
    "next_target": "R2FR_1749_NEXT_TARGET.csv",
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


def bridge_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GBT1749_0_gradient_completion_to_canonical_gap",
            "conditional gradient completion",
            "S_eta=-int sqrt(-g)[L0^-2 Fhat(m_*+eta)+(kappa_m/2) g^munu partial_mu eta partial_nu eta]",
            "for kappa_m>0, F2>0 and fixed L0: phi=sqrt(kappa_m) eta; mu_m^2=F2/(kappa_m L0^2); ell_tr=1/sqrt(mu_m^2)",
            "EXACT_SYMBOLIC_BRIDGE_DERIVED",
            "requires parent-signed kappa_m, F2, L0, field status, sign/units and variation order",
        ),
        (
            "GBT1749_1_boundary_amplitude_conversion",
            "conditional exponential branch",
            "eta(d)=A_S exp(-d/ell_tr)",
            "Phi_S=sqrt(kappa_m)*abs(A_S) in the canonical phi normalization",
            "EXACT_SYMBOLIC_BRIDGE_DERIVED",
            "requires sourced boundary/reference amplitude A_S and no-growing-branch/no-flux boundary class",
        ),
        (
            "GBT1749_2_R_lock_stationary_diffusion_gap",
            "R-lock stationary diffusion route",
            "D_m Delta_h delta_m - mu_B delta_m = source terms with mu_B=gamma_B lambda_R",
            "after division by D_m, the screening gap is mu_scr^2=mu_B/D_m=gamma_B lambda_R/D_m and ell_scr=sqrt(D_m/mu_B)",
            "EXACT_SYMBOLIC_BRIDGE_DERIVED",
            "not automatically a Hilbert canonical mass gap unless D_m kinetic slot and variational field status are parent-derived",
        ),
        (
            "GBT1749_3_PhiS_budget_law",
            "source-support/boundary law",
            "M_tr <= M_bdy exp(-ell_tr/ell_scr)+M_src+M_mL+M_nl",
            "Phi_S can be bounded by the same boundary/source budget only after mapping M_tr to canonical phi units",
            "CONDITIONAL_AMPLITUDE_BUDGET_DERIVED",
            "requires source support powers, m_L drift bound, trace-gradient bound, nonlinear remainder and Kperp treatment",
        ),
        (
            "GBT1749_4_Qalg_profile_feed",
            "canonical q-profile feed",
            "nabla Gamma_eff = mu_m^2 phi nabla phi + higher orders",
            "Q_alg <= A_ref^-1 mu_m^2 Phi_S^2 exp(-2d/ell_tr)/ell_tr plus tail/higher-order corrections",
            "PROFILE_FEED_READY_SYMBOLIC",
            "requires A_ref, d, correction envelope, stress routing and projection norms before any score",
        ),
        (
            "GBT1749_5_verdict",
            "1749 bridge theorem",
            "mu_m^2 and Phi_S now have exact symbolic parent-action contracts",
            "the bridge is sharper than 1748, but no claim-grade numeric/source row exists",
            "BRIDGE_DERIVED_PARENT_SIGNATURE_MISSING",
            "next target is coefficient provenance and boundary amplitude, not local-GR claiming",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "route": route,
            "premise": premise,
            "derived_bridge": bridge,
            "status": status,
            "missing_to_promote": missing,
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for theorem_id, route, premise, bridge, status, missing in rows
    ]


def signature_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SIG1749_0_action_slot",
            "parent action contains the gradient/kinetic slot",
            "kappa_m or Z_m term appears in parent action before projection/readout",
            "NOT_PARENT_SIGNED",
            "1379 says gradient completion is conditional extension only",
        ),
        (
            "SIG1749_1_field_status",
            "eta/phi/m is a varied parent field",
            "field status and variation order fixed before local readout",
            "CANDIDATE_NOT_SIGNED",
            "field may remain metric-composite/domain/readout variable",
        ),
        (
            "SIG1749_2_sign_units",
            "positive gap and ghost-free kinetic convention",
            "kappa_m>0, F2>0, L0 units, mu_m^2 units length^-2",
            "MISSING_UNITS_FRAME_LOCK",
            "symbolic bridge is dimensionally stated but not source-backed",
        ),
        (
            "SIG1749_3_source_silence",
            "local source terms vanish or are bounded",
            "J_c, R_Xgrad, R_bdy, R_readout zero/bounded in same branch",
            "MISSING_SOURCE_COUPLING",
            "source-supported hair can survive",
        ),
        (
            "SIG1749_4_boundary_class",
            "decaying branch and Phi_S are boundary-owned",
            "no growing branch; no-flux/projected boundary; finite A_S/Phi_S",
            "MISSING_BOUNDARY_SHELL_CLOSURE",
            "Phi_S cannot become a prediction",
        ),
        (
            "SIG1749_5_stress_routing",
            "kinetic stress is retained or bounded",
            "using gradient stiffness means the Hilbert stress cannot be deleted",
            "PASS_NONCLAIM_GUARD_ONLY",
            "prevents cheating but does not close residual vector",
        ),
        (
            "SIG1749_6_projection_norms",
            "A_ref and arena projection norms exist",
            "normalization from local q-profile to observables",
            "MISSING_OPERATOR_PROJECTION_NORMS",
            "Q_alg profile cannot score",
        ),
        (
            "SIG1749_7_verdict",
            "claim-grade mu_m^2/Phi_S parent row",
            "all clauses above source-backed or parent-signed",
            "NOT_CLAIM_GRADE",
            "bridge theorem survives as nonclaim contract only",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "clause": clause,
            "required_for_promotion": required,
            "current_status": status,
            "reason": reason,
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for audit_id, clause, required, status, reason in rows
    ]


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MPC1749_0_mu_m2_gradient",
            "mu_m^2",
            "F2/(kappa_m L0^2)",
            "length^-2",
            "gradient-completion canonicalization",
            "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "kappa_m;F2;L0;field_status;sign_units;parent_action_source",
        ),
        (
            "MPC1749_1_ell_tr_gradient",
            "ell_tr",
            "sqrt(kappa_m L0^2/F2)",
            "length",
            "inverse canonical gap",
            "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "same as mu_m2 plus positive gap",
        ),
        (
            "MPC1749_2_Phi_S_gradient",
            "Phi_S",
            "sqrt(kappa_m)*abs(A_S)",
            "canonical field units",
            "boundary amplitude conversion",
            "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "A_S;boundary_class;no_growing_branch;source_support",
        ),
        (
            "MPC1749_3_mu_scr_R_lock",
            "mu_scr^2",
            "mu_B/D_m = gamma_B lambda_R/D_m",
            "length^-2",
            "stationary R-lock screening gap",
            "SYMBOLIC_DIFFUSION_GAP_ONLY",
            "D_m;gamma_B;lambda_R;variational_action_bridge",
        ),
        (
            "MPC1749_4_Phi_S_budget",
            "Phi_S budget",
            "C_phi*(M_bdy exp(-ell_tr/ell_scr)+M_src+M_mL+M_nl)",
            "canonical field units",
            "source-support boundary amplitude law",
            "BOUND_FORM_ONLY_NONCLAIM",
            "C_phi;M_bdy;M_src;M_mL;M_nl;Kperp;trace_gradient",
        ),
        (
            "MPC1749_5_Qalg_feed",
            "Q_alg profile",
            "A_ref^-1 mu_m^2 Phi_S^2 exp(-2d/ell_tr)/ell_tr + tails",
            "local residual units",
            "observable profile feed",
            "BOUND_FORM_ONLY_NONCLAIM",
            "A_ref;d;epsilon_tail;projection_norms;stress_route",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "units": units,
            "route": route,
            "current_status": status,
            "missing_to_promote": missing,
            "accepted_as_contract": "True",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for row_id, quantity, formula, units, route, status, missing in rows
    ]


def tau_fallback_rows() -> list[dict[str, Any]]:
    rows = [
        ("TFB1749_0_readout", "P_WEP_K_CMSM_readout.csv", "official MICROSCOPE readout/design matrix", "external_source", "held_fallback"),
        ("TFB1749_1_worldtube", "P_WEP_R_source_Earth_worldtube.csv", "Earth source worldtube/source weighting", "external_source", "held_fallback"),
        ("TFB1749_2_material", "P_WEP_TiPt_material_response_tensor.csv", "Ti/Pt material response tensor", "external_or_parent_matter", "held_fallback"),
        ("TFB1749_3_product", "P_WEP_eta_product_convention.csv", "eta product convention and no-cancellation guard", "definition_source", "held_fallback"),
        ("TFB1749_4_tau_min", "P_WEP_tau_min_lower_bound.csv", "strict positive tau lower bound or alignment theorem", "derivation_or_source", "held_fallback"),
        ("TFB1749_5_verdict", "tau fallback pack", "not pursued before parent gap/amplitude coefficient contract unless derivation route stalls", "fallback_only", "not_selected_now"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "fallback_id": fallback_id,
            "needed_artifact": artifact,
            "purpose": purpose,
            "route": route,
            "selection_status": selection,
            "current_status": "SOURCE_OR_DERIVATION_NEEDED",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for fallback_id, artifact, purpose, route, selection in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1749_0_bridge_status",
            "SYMBOLIC_GAP_AMPLITUDE_BRIDGE_DERIVED",
            "mu_m^2=F2/(kappa_m L0^2) and Phi_S=sqrt(kappa_m)|A_S| give exact canonical contracts for the gradient branch",
            "use these as validator contracts, not as claims",
        ),
        (
            "DEC1749_1_R_lock_status",
            "R_LOCK_GAP_BRIDGE_SEPARATED",
            "mu_B/D_m is a legitimate screened diffusion gap, but not automatically a Hilbert canonical mass gap",
            "keep R-lock as support, but require variational kinetic ownership before promotion",
        ),
        (
            "DEC1749_2_claim_status",
            "NO_CLAIM_GRADE_MU_PHI_ROW",
            "kappa_m/Z_m, F2, L0, A_S, source silence, boundary class and projection norms remain unsigned",
            "do not reopen local-GR/Newton/PPN/R10/WEP scoring",
        ),
        (
            "DEC1749_3_best_next",
            "TARGET_PARENT_KINETIC_COEFFICIENT_AND_BOUNDARY_AMPLITUDE",
            "the bridge tells us exactly which two pieces to attack next: kinetic/gap coefficient provenance and Phi_S boundary amplitude",
            "build 1750 kinetic coefficient provenance or boundary amplitude theorem",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE1749_0_bridge", "symbolic bridge can be used as a prediction", "BLOCKED_CONTRACT_ONLY"),
        ("GATE1749_1_mu_m2", "mu_m^2 is source-backed/parent-signed", "BLOCKED_KAPPA_F2_L0_UNSIGNED"),
        ("GATE1749_2_Phi_S", "Phi_S is source-backed/parent-signed", "BLOCKED_BOUNDARY_AMPLITUDE_UNSIGNED"),
        ("GATE1749_3_R_lock_gap", "R-lock diffusion gap is the canonical Hilbert mass gap", "BLOCKED_VARIATIONAL_BRIDGE_UNSIGNED"),
        ("GATE1749_4_Qalg_score", "Q_alg profile can score local arenas", "BLOCKED_PROJECTION_SOURCE_STRESS_INPUTS"),
        ("GATE1749_5_local_reentry", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
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
        for gate_id, claim, blocker in gates
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1749_0_primary",
            "next_target": "1750-Y5-R2FR-parent-kinetic-coefficient-or-boundary-amplitude-theorem.md",
            "script": "scripts/Y5_R2FR_parent_kinetic_coefficient_or_boundary_amplitude_theorem.py",
            "objective": "try to parent-sign kappa_m/Z_m and F2/L0, or derive a source/boundary amplitude bound for Phi_S; if neither closes, emit explicit finite residual rows",
            "success_condition": "one coefficient or amplitude row becomes source-backed/theorem-signed without opening a local claim, or blockers become stricter and machine-readable",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1749_1_tau_fallback",
            "next_target": "1750b-Y5-R2FR-WEP-tau-min-source-import-pack.md",
            "script": "scripts/Y5_R2FR_WEP_tau_min_source_import_pack.py",
            "objective": "stage official readout/source/material/product rows for tau_WEP and tau_min if parent gap/amplitude derivation stalls",
            "success_condition": "nonclaim import manifest for tau projection sources",
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
        "bridge_theorem": bridge_theorem_rows(),
        "signature_audit": signature_audit_rows(),
        "candidate_rows": candidate_rows(),
        "tau_fallback": tau_fallback_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1749_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1749_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "claim_allowed",
        "gate_pass",
        "parent_signed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {"claim_allowed", "gate_pass", "parent_signed", "score_ready", "valid_for_claim", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def bridge_contracts_accepted_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["candidate_rows"]
    return all(
        row["accepted_as_contract"] == "True"
        and row["score_ready"] == "False"
        and row["valid_prediction_row"] == "False"
        and row["claim_allowed"] == "False"
        for row in rows
    )


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1749_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1749_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1749*"):
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
    bridge = rows_map["bridge_theorem"]
    signature = rows_map["signature_audit"]
    candidates = rows_map["candidate_rows"]
    fallback = rows_map["tau_fallback"]
    decisions = rows_map["decision"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1749_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1749_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1749_2_bridge_identity", any(row["theorem_id"] == "GBT1749_0_gradient_completion_to_canonical_gap" and "mu_m^2=F2/(kappa_m L0^2)" in row["derived_bridge"] for row in bridge), "canonical gap bridge identity is recorded", "canonical gap bridge identity missing"),
        check("VAL1749_3_amplitude_identity", any(row["theorem_id"] == "GBT1749_1_boundary_amplitude_conversion" and "Phi_S=sqrt(kappa_m)" in row["derived_bridge"] for row in bridge), "canonical amplitude bridge identity is recorded", "canonical amplitude bridge identity missing"),
        check("VAL1749_4_R_lock_separated", any(row["theorem_id"] == "GBT1749_2_R_lock_stationary_diffusion_gap" and "not automatically" in row["missing_to_promote"] for row in bridge), "R-lock diffusion gap is separated from Hilbert mass-gap claim", "R-lock/Hilbert separation missing"),
        check("VAL1749_5_signature_blocks", any(row["audit_id"] == "SIG1749_7_verdict" and row["current_status"] == "NOT_CLAIM_GRADE" for row in signature), "signature audit blocks claim-grade promotion", "signature verdict missing"),
        check("VAL1749_6_contracts_nonclaim", bridge_contracts_accepted_nonclaim(rows_map), "symbolic candidate rows accepted only as nonclaim contracts", "candidate contracts promoted or malformed"),
        check("VAL1749_7_tau_fallback_held", any(row["fallback_id"] == "TFB1749_5_verdict" and row["selection_status"] == "not_selected_now" for row in fallback), "tau-min source pack is held as fallback", "tau fallback verdict missing"),
        check("VAL1749_8_decision_next", any(row["decision_id"] == "DEC1749_3_best_next" and row["decision"] == "TARGET_PARENT_KINETIC_COEFFICIENT_AND_BOUNDARY_AMPLITUDE" for row in decisions), "decision selects kinetic coefficient and boundary amplitude", "best-next decision missing"),
        check("VAL1749_9_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1749_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1749_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1749_12_next_selected", any(row["route_id"] == "NEXT1749_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1749_13_csv_parse", parsed_ok, "all generated 1749 CSVs parse", "one or more generated 1749 CSVs failed to parse"),
        check("VAL1749_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1749_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1749_16_formalization_untouched", formalization_untouched(), "no 1749 outputs found under formalization-workbench", "1749 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1749_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1749 parent gap/amplitude bridge and nonclaim source-pack checkpoint" if overall else "one or more 1749 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1749 derives a useful exact bridge, not a claim: the conditional gradient-completion branch canonically gives `mu_m^2 = F2/(kappa_m L0^2)` and `Phi_S = sqrt(kappa_m)|A_S|`.",
        "- The R-lock route also gives a screened diffusion gap `mu_B/D_m = gamma_B lambda_R/D_m`, but this is not automatically the same thing as a Hilbert-action canonical mass gap.",
        "- This is progress because the missing `mu_m^2` and `Phi_S` rows are no longer vague; the parent action must now source/sign `kappa_m`, `F2`, `L0`, `A_S`, boundary class, source silence, stress routing, and projection norms.",
        "- The WEP `tau_min` route is kept as a fallback, but the best derivation-first target is now kinetic/gap coefficient provenance plus boundary amplitude.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Gap Amplitude Bridge Theorem",
        markdown_table(rows_map["bridge_theorem"], ["theorem_id", "route", "derived_bridge", "status", "missing_to_promote"]),
        "",
        "## Parent Signature Audit",
        markdown_table(rows_map["signature_audit"], ["audit_id", "clause", "current_status", "reason"]),
        "",
        "## Candidate Rows",
        markdown_table(rows_map["candidate_rows"], ["row_id", "quantity", "formula", "current_status", "missing_to_promote", "accepted_as_contract"]),
        "",
        "## Tau-Min Fallback Pack",
        markdown_table(rows_map["tau_fallback"], ["fallback_id", "needed_artifact", "purpose", "selection_status", "current_status"]),
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
        "This checkpoint is a real narrowing of the problem. The local branch has a clean canonical dictionary now. If the parent action can own the kinetic coefficient and boundary amplitude, the profile can become testable. If it cannot, the branch remains an explicit finite residual closure and must be tested as such.",
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
    doc_path = ROOT / "1749-Y5-R2FR-parent-gap-amplitude-row-or-tau-min-source-pack.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1749_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1749 validation FAIL")
    print("1749 validation PASS")


if __name__ == "__main__":
    main()
