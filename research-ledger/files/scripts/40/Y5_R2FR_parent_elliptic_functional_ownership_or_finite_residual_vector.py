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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1751"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1751 - Parent Elliptic Functional Ownership Or Finite Residual Vector"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1751_0_1750_doc",
        "source_key": "1750_handoff",
        "source_path": ROOT / "1750-Y5-R2FR-parent-kinetic-coefficient-or-boundary-amplitude-theorem.md",
        "needles": ["NEXT1750_0_primary", "TARGET_PARENT_ELLIPTIC_FUNCTIONAL_OWNERSHIP"],
    },
    {
        "source_id": "SRC1751_1_1750_kinetic",
        "source_key": "1750_kinetic_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_KINETIC_GAP_THEOREM.csv",
        "needles": ["KGT1750_1_canonical_normalization", "mu_m^2=mu_B/D_m"],
    },
    {
        "source_id": "SRC1751_2_1750_boundary",
        "source_key": "1750_boundary_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_BOUNDARY_AMPLITUDE_THEOREM.csv",
        "needles": ["BAT1750_1_nohair_zero_case", "BAT1750_2_finite_source_bound"],
    },
    {
        "source_id": "SRC1751_3_1750_coefficients",
        "source_key": "1750_coefficient_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_COEFFICIENT_PROVENANCE_AUDIT.csv",
        "needles": ["CPA1750_0_D_m", "NOT_CLAIM_GRADE"],
    },
    {
        "source_id": "SRC1751_4_41_memory_law",
        "source_key": "41_open_system_route",
        "source_path": FORMALIZATION / "41-memory-action-or-relaxation-law-v0.md",
        "needles": ["memory sector = effective open-system parent ingredient", "not yet fundamental closed action"],
    },
    {
        "source_id": "SRC1751_5_54_suppression",
        "source_key": "54_local_suppression_conditions",
        "source_path": FORMALIZATION / "54-local-branch-suppression-conditions.md",
        "needles": ["local_branch_suppression_conditions_sufficient_not_derived", "D_m Delta_h delta m - mu_B delta m = 0"],
    },
    {
        "source_id": "SRC1751_6_56_nojump",
        "source_key": "56_solar_nojump",
        "source_path": FORMALIZATION / "56-solar-transition-no-jump-theorem.md",
        "needles": ["solar_no_jump_theorem_conditional", "Integral_Omega D_m"],
    },
    {
        "source_id": "SRC1751_7_58_plateau_audit",
        "source_key": "58_plateau_rejection",
        "source_path": FORMALIZATION / "58-local-vacuum-plateau-lemma-audit.md",
        "needles": ["local_vacuum_plateau_rejected_as_current_derivation", "PL3: S_cg = 0"],
    },
    {
        "source_id": "SRC1751_8_69_R_lock",
        "source_key": "69_relaxation_functional_lock",
        "source_path": FORMALIZATION / "69-relaxation-functional-lock.md",
        "needles": ["mu_B = gamma_B lambda_R", "ell_scr = sqrt(D_m/mu_B)"],
    },
    {
        "source_id": "SRC1751_9_70_R_lock_results",
        "source_key": "70_relaxation_functional_results",
        "source_path": FORMALIZATION / "70-relaxation-functional-lock-first-results.md",
        "needles": ["relaxation_functional_lock_conditional_not_parent_derived", "parent v0 still does not derive R"],
    },
    {
        "source_id": "SRC1751_10_71_boundary_law",
        "source_key": "71_source_boundary_law",
        "source_path": FORMALIZATION / "71-source-support-boundary-law.md",
        "needles": ["M_bdy exp(-ell_tr/ell_scr)", "K_perp,loc"],
    },
    {
        "source_id": "SRC1751_11_1276_boundary",
        "source_key": "1276_parent_euler_boundary",
        "source_path": RESIDUALS / "P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv",
        "needles": ["ESC1276_7_boundary_no_charge", "CLOSURE_ONLY_CURRENTLY"],
    },
    {
        "source_id": "SRC1751_12_1302_stress",
        "source_key": "1302_memory_stress",
        "source_path": RESIDUALS / "P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
        "needles": ["MSR1302_0_canonical_scalar_stress_form", "MISSING_Z_m_SIGN_AND_VALUE"],
    },
    {
        "source_id": "SRC1751_13_1376_acquisition",
        "source_key": "1376_transition_source_acquisition",
        "source_path": RESIDUALS / "P8_Y5_R10_1376_TRANSITION_PARENT_SOURCE_ACQUISITION.csv",
        "needles": ["TPS1376_5_A_S", "TPS1376_16_shell_projector_or_bound"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_SOURCE_REGISTER.csv",
    "ownership_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_ELLIPTIC_FUNCTIONAL_OWNERSHIP_CONTRACT.csv",
    "variation_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_VARIATION_THEOREM.csv",
    "residual_vector": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_FINITE_RESIDUAL_VECTOR.csv",
    "candidate_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_CANDIDATE_ROWS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1751_VALIDATION.csv",
}


COPY_MAP = {
    "ownership_contract": "R2FR_1751_ELLIPTIC_FUNCTIONAL_OWNERSHIP_CONTRACT.csv",
    "variation_theorem": "R2FR_1751_VARIATION_THEOREM.csv",
    "residual_vector": "R2FR_1751_FINITE_RESIDUAL_VECTOR.csv",
    "candidate_rows": "R2FR_1751_CANDIDATE_ROWS.csv",
    "decision": "R2FR_1751_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1751_CLAIM_GATE.csv",
    "next_target": "R2FR_1751_NEXT_TARGET.csv",
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


def ownership_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EFO1751_0_functional_candidate",
            "parent-owned local elliptic functional",
            "E_m=int_Omega sqrt(h)[0.5 D_m h^ij partial_i delta_m partial_j delta_m + 0.5 mu_B delta_m^2 - J_eff delta_m] + E_boundary",
            "CONTRACT_WRITTEN",
            "must be derived from parent action/open-system variational principle, not introduced only at local readout",
        ),
        (
            "EFO1751_1_field_status",
            "m or delta_m is an independent varied field",
            "variation is performed before projection, domain selection, and observed readout",
            "CANDIDATE_NOT_SIGNED",
            "1301/1302 keep parent field status and no-metric-composite exclusion unsigned",
        ),
        (
            "EFO1751_2_positive_coefficients",
            "D_m>0 and mu_B>=mu_min>0",
            "coercivity gives nohair/amplitude bounds",
            "NOT_DERIVED_AS_PARENT_FLOORS",
            "58 rejects mu_B floor as currently derived; D_m sign/units are supported by equation register but not parent action",
        ),
        (
            "EFO1751_3_covariant_or_controlled_frame",
            "elliptic h^ij operator is a legitimate stationary reduction",
            "parent supplies u^mu/coframe or covariant hyperbolic action whose stationary local limit is elliptic",
            "OPEN_SYSTEM_STATUS_ONLY",
            "41 explicitly selects effective open-system route before a closed fundamental action",
        ),
        (
            "EFO1751_4_source_owner",
            "J_eff is parent-defined",
            "J_eff collects source, m_L drift, coefficient-gradient, boundary/readout and nonlinear terms with no hidden cancellation",
            "MISSING_SOURCE_MAP",
            "source silence and source support powers are not parent-owned",
        ),
        (
            "EFO1751_5_boundary_owner",
            "E_boundary/no-flux/no-growing branch is parent-owned",
            "boundary term is fixed before local test and not tuned to remove PPN residuals",
            "CLOSURE_ONLY_CURRENTLY",
            "1276/58/802/803 keep boundary/no-charge and shell projector unsigned",
        ),
        (
            "EFO1751_6_stress_exchange_owner",
            "Hilbert stress and open-system exchange are routed",
            "using the functional also routes T_m, q^nu, and K_hat divergence into residual ledgers",
            "HARD_RESIDUAL_CONTRACT_NONCLAIM",
            "1302 forbids deleting scalar-memory stress after using it for screening",
        ),
        (
            "EFO1751_7_verdict",
            "parent elliptic functional ownership",
            "EFO1751_0 through EFO1751_6 all parent-signed or source-backed",
            "OWNERSHIP_NOT_CLOSED",
            "1751 cannot claim derived local GR; it must keep finite residual vector live",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "clause": clause,
            "required_statement": required,
            "current_status": status,
            "blocker": blocker,
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for contract_id, clause, required, status, blocker in rows
    ]


def variation_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VAR1751_0_constant_coefficient_variation",
            "fixed D_m, mu_B, m_L and h_ij in local domain",
            "delta E_m=0 gives -D_m Delta_h delta_m + mu_B delta_m = J_eff; equivalently D_m Delta_h delta_m - mu_B delta_m = -J_eff",
            "EXACT_CONDITIONAL_VARIATION",
            "requires parent-fixed coefficients and controlled boundary term",
        ),
        (
            "VAR1751_1_variable_Dm_correction",
            "D_m=D_m(X_B(x)) varies",
            "Euler equation becomes -nabla_i(D_m nabla^i delta_m)+mu_B delta_m=J_eff, producing coefficient-gradient residuals if simplified to D_m Delta_h",
            "EXACT_CORRECTION_IDENTIFIED",
            "retain R_coeff_Dm unless parent proves local constancy or bounds gradients",
        ),
        (
            "VAR1751_2_variable_mL_correction",
            "m_L=m_L(X_B(x)) varies",
            "m=m_L+delta_m gives source terms from Delta_h m_L and coefficient gradients; m_L drift cannot be hidden inside delta_m=0",
            "EXACT_CORRECTION_IDENTIFIED",
            "retain R_mL unless parent proves local fixed point/constant m_L",
        ),
        (
            "VAR1751_3_source_boundary_identity",
            "finite source and boundary terms",
            "coercive identity: int D_m|grad delta_m|^2+int mu_B delta_m^2 = int J_eff delta_m + boundary_flux",
            "EXACT_CONDITIONAL_ENERGY_IDENTITY",
            "exact nohair only if J_eff=0 and boundary_flux=0",
        ),
        (
            "VAR1751_4_nohair_branch",
            "J_eff=0 and boundary_flux=0",
            "positive D_m and mu_B force delta_m=0, grad delta_m=0, Phi_S=0, and the screened profile is exact-zero",
            "EXACT_ZERO_THEOREM_CONDITIONAL",
            "premises are not parent-owned in current corpus",
        ),
        (
            "VAR1751_5_finite_branch",
            "one or more premises fail",
            "all unsilenced source, coefficient, boundary, shell, trace, stress, and K_perp pieces must enter finite residual rows",
            "FINITE_RESIDUAL_BRANCH_REQUIRED",
            "this is the default 1751 status",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "case": case,
            "derived_result": result,
            "status": status,
            "missing_to_promote": missing,
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for theorem_id, case, result, status, missing in rows
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RV1751_0_source_leak",
            "R_source",
            "(1-Pi_B) S_cg",
            "local source leakage if S_cg is not zero or Pi_B is not exactly local",
            "MISSING_SOURCE_SUPPORT_THEOREM",
            "PPN/R10/WEP/clock/orbital/local_GR",
        ),
        (
            "RV1751_1_mL_drift",
            "R_mL",
            "D_m Delta_h m_L + grad D_m dot grad m_L",
            "environmental equilibrium drift reappears even when delta_m is small",
            "MISSING_LOCAL_FIXED_POINT_OR_CONSTANT_mL",
            "PPN/local_GR/clock",
        ),
        (
            "RV1751_2_coefficient_gradient",
            "R_coeff",
            "grad D_m dot grad delta_m + grad mu_B response terms",
            "simplified constant-coefficient gap is unsafe if coefficients vary locally",
            "MISSING_COEFFICIENT_GRADIENT_BOUND",
            "PPN/R10/local_GR",
        ),
        (
            "RV1751_3_boundary_flux",
            "R_boundary",
            "boundary_flux or ambient memory mismatch",
            "nohair proof fails if the local exterior boundary carries an offset",
            "MISSING_BOUNDARY_NOFLUX_OR_AMBIENT_MATCH",
            "PPN/local_GR/orbital",
        ),
        (
            "RV1751_4_shell_projector",
            "R_shell",
            "transition shell Q_trans/Q_proj contribution",
            "generic width or U_B suppression cannot hide a local shell",
            "MISSING_SHELL_PROJECTOR_OR_BOUND",
            "PPN/R10/local_GR",
        ),
        (
            "RV1751_5_trace_gradient",
            "R_trace",
            "nabla[L_cg^-2 F_L(X_B)]",
            "R-lock removes F_1 but not environmental trace gradients",
            "MISSING_TRACE_BASELINE_CONSTANCY",
            "PPN/clock/local_GR",
        ),
        (
            "RV1751_6_trace_stiffness",
            "R_F2",
            "a_F lambda_R memory-jump quadratic response",
            "large trace stiffness can fail local bounds even when dynamic gap screens",
            "MISSING_aF_lambdaR_SOURCE_AND_BOUND",
            "PPN/R10/local_GR",
        ),
        (
            "RV1751_7_memory_stress",
            "R_Tm",
            "Hilbert stress from D_m/Z_m gradients, potential, source/bath and boundary terms",
            "screening kinetic term carries stress that cannot be deleted",
            "MISSING_MEMORY_STRESS_BOUND",
            "PPN/local_GR/conservation",
        ),
        (
            "RV1751_8_Kperp",
            "R_Kperp",
            "divergence/free transverse tensor residual",
            "scalar elliptic functional does not kill homogeneous K_perp modes",
            "MISSING_KPERP_ZERO_OR_BOUND",
            "PPN/preferred_frame/local_GR",
        ),
        (
            "RV1751_9_projection_norms",
            "R_project",
            "A_ref, N_div, N_G, N_D and arena maps",
            "residuals cannot score without observable projection norms",
            "MISSING_OPERATOR_PROJECTION_NORMS",
            "all_local_arenas",
        ),
        (
            "RV1751_10_verdict",
            "finite residual vector",
            "sum of active R_i rows with no cancellation unless parent identity exists",
            "finite residual branch replaces hidden local-GR claim",
            "RESIDUAL_VECTOR_ACTIVE_NONCLAIM",
            "all_local_arenas",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "quantity": quantity,
            "formula_or_description": formula,
            "role": role,
            "current_status": status,
            "arena_links": arenas,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for residual_id, quantity, formula, role, status, arenas in rows
    ]


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAN1751_0_E_m", "E_m functional", "int sqrt(h)[0.5D_m|grad delta_m|^2+0.5mu_B delta_m^2-J_eff delta_m]+E_boundary", "PARENT_OWNERSHIP_CONTRACT_ONLY"),
        ("CAN1751_1_mu_gap", "mu_m^2", "mu_B/D_m only if E_m parent-owned", "THEOREM_CONTRACT_ONLY"),
        ("CAN1751_2_nohair", "Phi_S_zero", "Phi_S=0 only if J_eff=0 and boundary_flux=0 under owned coercive functional", "CONDITIONAL_ZERO_PREMISES_UNSIGNED"),
        ("CAN1751_3_finite_residual_vector", "R_local_vector", "R_source+R_mL+R_coeff+R_boundary+R_shell+R_trace+R_F2+R_Tm+R_Kperp+R_project", "ACTIVE_NONCLAIM_FALLBACK"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_contract": formula,
            "current_status": status,
            "accepted_as_contract": "True",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for row_id, quantity, formula, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1751_0_functional_status",
            "ELLIPTIC_FUNCTIONAL_CONTRACT_WRITTEN_NOT_PARENT_OWNED",
            "the local functional and its variation are exact, but 41/58/1302 show current corpus does not own all parent/action/source/boundary premises",
            "do not promote mu_m^2=mu_B/D_m to a prediction",
        ),
        (
            "DEC1751_1_nohair_status",
            "NOHAIR_THEOREM_REMAINS_CONDITIONAL",
            "positive energy identity gives Phi_S=0 only after source and boundary flux are parent-zero",
            "keep finite residual vector active",
        ),
        (
            "DEC1751_2_residual_status",
            "FINITE_RESIDUAL_VECTOR_REPLACES_HIDDEN_PLATEAU",
            "unowned source, m_L drift, coefficient-gradient, boundary, shell, trace, stress, K_perp and projection pieces are now explicit rows",
            "future local tests must fill or zero these rows",
        ),
        (
            "DEC1751_3_best_next",
            "TARGET_FIRST_RESIDUAL_ZERO_OR_BOUND",
            "the best next move is to try to close one residual row, preferably source support or boundary no-flux, because those unlock the nohair branch",
            "build 1752 source-support/no-flux residual zero-or-bound checkpoint",
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
        ("GATE1751_0_functional", "elliptic functional is parent-owned", "BLOCKED_PARENT_ACTION_OR_OPEN_SYSTEM_OWNERSHIP"),
        ("GATE1751_1_gap", "mu_m^2=mu_B/D_m is prediction-grade", "BLOCKED_Dm_muB_SOURCE_UNITS_FLOORS"),
        ("GATE1751_2_nohair", "Phi_S=0 nohair local branch closes", "BLOCKED_SOURCE_BOUNDARY_PREMISES"),
        ("GATE1751_3_residual_vector", "finite residual vector can score", "BLOCKED_RESIDUAL_INPUTS_MISSING"),
        ("GATE1751_4_shell", "transition shell is zero/projected/bounded", "BLOCKED_SHELL_PROJECTOR_OR_BOUND"),
        ("GATE1751_5_local_reentry", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
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
            "route_id": "NEXT1751_0_primary",
            "next_target": "1752-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md",
            "script": "scripts/Y5_R2FR_source_support_or_boundary_no_flux_first_residual_zero_bound.py",
            "objective": "try to close the first residual row needed by the nohair branch: source support R_source=0/bound or boundary flux R_boundary=0/bound; otherwise keep finite residual rows explicit",
            "success_condition": "one residual row becomes parent-signed/source-backed nonclaim, or a sharper blocker contract is produced without opening local claims",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1751_1_fallback",
            "next_target": "1752b-Y5-R2FR-boundary-shell-projector-or-explicit-Qtrans-row.md",
            "script": "scripts/Y5_R2FR_boundary_shell_projector_or_explicit_Qtrans_row.py",
            "objective": "attack shell projector/explicit Q_trans if source/no-flux rows remain blocked",
            "success_condition": "shell exact-zero/projector theorem or explicit finite row stays nonclaim and source-ready",
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
        "ownership_contract": ownership_contract_rows(),
        "variation_theorem": variation_theorem_rows(),
        "residual_vector": residual_vector_rows(),
        "candidate_rows": candidate_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1751_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1751_{key.upper()}.csv")


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


def residual_vector_active(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["residual_vector"]
    return any(row["residual_id"] == "RV1751_10_verdict" and row["current_status"] == "RESIDUAL_VECTOR_ACTIVE_NONCLAIM" for row in rows) and all(
        row["score_ready"] == "False" and row["claim_allowed"] == "False" for row in rows
    )


def candidate_contracts_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(
        row["accepted_as_contract"] == "True"
        and row["score_ready"] == "False"
        and row["valid_prediction_row"] == "False"
        and row["claim_allowed"] == "False"
        for row in rows_map["candidate_rows"]
    )


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1751_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1751_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1751*"):
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
    ownership = rows_map["ownership_contract"]
    variation = rows_map["variation_theorem"]
    decisions = rows_map["decision"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1751_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1751_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1751_2_contract_written", any(row["contract_id"] == "EFO1751_0_functional_candidate" and row["current_status"] == "CONTRACT_WRITTEN" for row in ownership), "elliptic functional contract is written", "elliptic functional contract missing"),
        check("VAL1751_3_ownership_blocked", any(row["contract_id"] == "EFO1751_7_verdict" and row["current_status"] == "OWNERSHIP_NOT_CLOSED" for row in ownership), "ownership verdict remains blocked", "ownership verdict missing"),
        check("VAL1751_4_variation_exact", any(row["theorem_id"] == "VAR1751_0_constant_coefficient_variation" and row["status"] == "EXACT_CONDITIONAL_VARIATION" for row in variation), "constant-coefficient variation is exact conditional theorem", "variation theorem missing"),
        check("VAL1751_5_variable_corrections", any(row["theorem_id"] == "VAR1751_1_variable_Dm_correction" for row in variation) and any(row["theorem_id"] == "VAR1751_2_variable_mL_correction" for row in variation), "variable coefficient and m_L corrections are explicit", "variable correction rows missing"),
        check("VAL1751_6_residual_vector_active", residual_vector_active(rows_map), "finite residual vector is active and nonclaim", "residual vector missing or claim-enabled"),
        check("VAL1751_7_candidate_contracts_nonclaim", candidate_contracts_nonclaim(rows_map), "candidate rows are nonclaim contracts", "candidate row promoted or malformed"),
        check("VAL1751_8_decision_next", any(row["decision_id"] == "DEC1751_3_best_next" and row["decision"] == "TARGET_FIRST_RESIDUAL_ZERO_OR_BOUND" for row in decisions), "decision selects first residual zero/bound target", "best-next decision missing"),
        check("VAL1751_9_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1751_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1751_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1751_12_next_selected", any(row["route_id"] == "NEXT1751_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1751_13_csv_parse", parsed_ok, "all generated 1751 CSVs parse", "one or more generated 1751 CSVs failed to parse"),
        check("VAL1751_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1751_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1751_16_formalization_untouched", formalization_untouched(), "no 1751 outputs found under formalization-workbench", "1751 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1751_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1751 parent elliptic functional ownership or finite residual vector checkpoint" if overall else "one or more 1751 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1751 writes the exact parent-owned elliptic functional contract, but the current corpus does not yet own it as a parent action/open-system variational principle.",
        "- The variation theorem is clean: fixed coefficients give the screened equation, variable `D_m` and `m_L` generate explicit residual terms rather than disappearing.",
        "- The no-hair route survives only conditionally: `Phi_S=0` follows if `J_eff=0` and boundary flux vanishes under a positive owned functional.",
        "- Because those premises are not parent-signed, 1751 activates the finite residual vector: source leak, `m_L` drift, coefficient gradients, boundary flux, shell, trace gradient, trace stiffness, memory stress, `K_perp`, and projection norms.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Elliptic Functional Ownership Contract",
        markdown_table(rows_map["ownership_contract"], ["contract_id", "clause", "current_status", "blocker"]),
        "",
        "## Variation Theorem",
        markdown_table(rows_map["variation_theorem"], ["theorem_id", "case", "derived_result", "status", "missing_to_promote"]),
        "",
        "## Finite Residual Vector",
        markdown_table(rows_map["residual_vector"], ["residual_id", "quantity", "formula_or_description", "current_status", "arena_links"]),
        "",
        "## Candidate Rows",
        markdown_table(rows_map["candidate_rows"], ["row_id", "quantity", "formula_or_contract", "current_status"]),
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
        "This is the right kind of failure: not vague, not fatal, and not allowed to hide. The parent-owned elliptic route would give a real GR/Newton local bridge, but until it is owned the theory must carry an explicit residual vector into local tests. The next useful win is to zero or bound one of those residuals from the parent theory.",
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
    doc_path = ROOT / "1751-Y5-R2FR-parent-elliptic-functional-ownership-or-finite-residual-vector.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1751_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1751 validation FAIL")
    print("1751 validation PASS")


if __name__ == "__main__":
    main()
