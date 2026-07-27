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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1750"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1750 - Parent Kinetic Coefficient Or Boundary Amplitude Theorem"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1750_0_1749_doc",
        "source_key": "1749_handoff",
        "source_path": ROOT / "1749-Y5-R2FR-parent-gap-amplitude-row-or-tau-min-source-pack.md",
        "needles": ["NEXT1749_0_primary", "TARGET_PARENT_KINETIC_COEFFICIENT_AND_BOUNDARY_AMPLITUDE"],
    },
    {
        "source_id": "SRC1750_1_1749_candidates",
        "source_key": "1749_mu_phi_candidates",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1749_MU_PHI_CANDIDATE_ROWS.csv",
        "needles": ["MPC1749_0_mu_m2_gradient", "MPC1749_4_Phi_S_budget"],
    },
    {
        "source_id": "SRC1750_2_1376_acquisition",
        "source_key": "1376_transition_source_acquisition",
        "source_path": RESIDUALS / "P8_Y5_R10_1376_TRANSITION_PARENT_SOURCE_ACQUISITION.csv",
        "needles": ["TPS1376_10_F2", "TPS1376_11_L0"],
    },
    {
        "source_id": "SRC1750_3_1379_signature",
        "source_key": "1379_gradient_parent_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv",
        "needles": ["GPA1379_2_kappa_or_Zm", "NO_PARENT_SIGNED_GRADIENT_COMPLETION_ROW"],
    },
    {
        "source_id": "SRC1750_4_1302_stress",
        "source_key": "1302_memory_stress_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
        "needles": ["MSR1302_0_canonical_scalar_stress_form", "MISSING_Z_m_SIGN_AND_VALUE"],
    },
    {
        "source_id": "SRC1750_5_1370_L0",
        "source_key": "1370_L0_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv",
        "needles": ["LCC1370_5_corpus_signature_verdict", "NOT_LIVE_CLAIM_UNTIL_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1750_6_1371_fixed_action",
        "source_key": "1371_fixed_L0_action",
        "source_path": RESIDUALS / "P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv",
        "needles": ["PAI1371_2_strict_double_zero", "PAI1371_4_gradient_source_after_double_zero"],
    },
    {
        "source_id": "SRC1750_7_1276_euler",
        "source_key": "1276_parent_euler_source_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv",
        "needles": ["ESC1276_7_boundary_no_charge", "CLOSURE_ONLY_CURRENTLY"],
    },
    {
        "source_id": "SRC1750_8_69_R_lock",
        "source_key": "69_relaxation_functional_lock",
        "source_path": FORMALIZATION / "69-relaxation-functional-lock.md",
        "needles": ["mu_B = gamma_B lambda_R", "ell_scr = sqrt(D_m/mu_B)"],
    },
    {
        "source_id": "SRC1750_9_70_R_lock_results",
        "source_key": "70_relaxation_functional_results",
        "source_path": FORMALIZATION / "70-relaxation-functional-lock-first-results.md",
        "needles": ["relaxation_functional_lock_conditional_not_parent_derived", "fast local erasure"],
    },
    {
        "source_id": "SRC1750_10_71_boundary_law",
        "source_key": "71_source_support_boundary_law",
        "source_path": FORMALIZATION / "71-source-support-boundary-law.md",
        "needles": ["Boundary Amplitude", "M_bdy exp(-ell_tr/ell_scr)"],
    },
    {
        "source_id": "SRC1750_11_72_boundary_results",
        "source_key": "72_source_support_boundary_results",
        "source_path": FORMALIZATION / "72-source-support-boundary-first-results.md",
        "needles": ["source_support_boundary_law_conditional_open", "weak_boundary_screening_fail"],
    },
    {
        "source_id": "SRC1750_12_05_equations",
        "source_key": "05_equation_register",
        "source_path": FORMALIZATION / "05-equation-register.md",
        "needles": ["D_m Delta_h delta m", "mu_B = gamma_B lambda_R"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_SOURCE_REGISTER.csv",
    "kinetic_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_KINETIC_GAP_THEOREM.csv",
    "boundary_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_BOUNDARY_AMPLITUDE_THEOREM.csv",
    "coefficient_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_COEFFICIENT_PROVENANCE_AUDIT.csv",
    "candidate_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_CANDIDATE_ROWS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1750_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1750_VALIDATION.csv",
}


COPY_MAP = {
    "kinetic_theorem": "R2FR_1750_KINETIC_GAP_THEOREM.csv",
    "boundary_theorem": "R2FR_1750_BOUNDARY_AMPLITUDE_THEOREM.csv",
    "coefficient_audit": "R2FR_1750_COEFFICIENT_PROVENANCE_AUDIT.csv",
    "candidate_rows": "R2FR_1750_CANDIDATE_ROWS.csv",
    "decision": "R2FR_1750_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1750_CLAIM_GATE.csv",
    "next_target": "R2FR_1750_NEXT_TARGET.csv",
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


def kinetic_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KGT1750_0_variational_completion",
            "stationary R-lock equation",
            "D_m Delta_h delta_m - mu_B delta_m = -J_eff",
            "if this is the Euler equation of E_m=int[0.5 D_m |grad delta_m|^2 + 0.5 mu_B delta_m^2 - J_eff delta_m], then D_m is the kinetic coefficient and mu_B is the quadratic restoring coefficient",
            "EXACT_CONDITIONAL_VARIATIONAL_COMPLETION",
            "requires parent-owned E_m or action slot, D_m>0, mu_B>0, field status, and source definition",
        ),
        (
            "KGT1750_1_canonical_normalization",
            "canonical field conversion",
            "phi=sqrt(D_m) delta_m",
            "E_m=int[0.5 |grad phi|^2 + 0.5 (mu_B/D_m) phi^2 - (J_eff/sqrt(D_m)) phi], so mu_m^2=mu_B/D_m and ell_scr=sqrt(D_m/mu_B)",
            "EXACT_CONDITIONAL_CANONICAL_GAP",
            "requires D_m units/sign and variational ownership; not enough if R-lock is only open-system phenomenology",
        ),
        (
            "KGT1750_2_trace_stiffness_separation",
            "Gamma_eff trace response",
            "F_2=a_F lambda_R=a_F mu_B/gamma_B",
            "readout trace stiffness F_2 is not automatically the same as the dynamical screening gap mu_B/D_m; local safety needs both the dynamic gap and readout stiffness bounded",
            "EXACT_SEPARATION_DERIVED",
            "requires a_F, lambda_R, gamma_B and F_L/L_cg gradient ownership",
        ),
        (
            "KGT1750_3_gradient_completion_bridge",
            "old kappa_m branch",
            "S_eta uses kappa_m and L0^-2 F2",
            "the old bridge mu_m^2=F2/(kappa_m L0^2) is recovered as a separate canonical-gradient branch; it can match R-lock only if kappa_m<->D_m and L0/F2 conventions are parent-identified",
            "BRIDGE_COMPATIBILITY_CONDITION_DERIVED",
            "requires parent map between kappa_m, D_m, F2, L0 and the R-lock variables",
        ),
        (
            "KGT1750_4_mobility_stiffness_rule",
            "safe screening design rule",
            "mu_B=gamma_B lambda_R",
            "large local screening should preferably come from mobility gamma_B or kinetic ratio mu_B/D_m, not arbitrarily large trace-coupled lambda_R that also raises F_2",
            "CONDITIONAL_DESIGN_RULE_DERIVED",
            "requires parent reason for gamma_B, lambda_R, a_F and D_m values",
        ),
        (
            "KGT1750_5_verdict",
            "kinetic/gap theorem",
            "D_m route is sharper than kappa_m placeholder",
            "1750 derives a cleaner conditional kinetic coefficient contract but does not parent-sign a claim-grade coefficient",
            "THEOREM_CONTRACT_DERIVED_PARENT_OWNERSHIP_MISSING",
            "next target must parent-own E_m/action slot or demote to explicit finite residual branch",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "object": obj,
            "premise": premise,
            "derived_result": result,
            "status": status,
            "missing_to_promote": missing,
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for theorem_id, obj, premise, result, status, missing in rows
    ]


def boundary_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BAT1750_0_coercive_energy_identity",
            "positive screened operator",
            "(-D_m Delta_h + mu_B) delta_m = J_eff with D_m>0, mu_B>=mu_min>0",
            "multiplying by delta_m gives int D_m |grad delta_m|^2 + int mu_B delta_m^2 = int J_eff delta_m + boundary_flux",
            "EXACT_CONDITIONAL_ENERGY_IDENTITY",
            "requires source term, boundary flux class, domain regularity and observed-frame operator ownership",
        ),
        (
            "BAT1750_1_nohair_zero_case",
            "zero source and silent boundary",
            "J_eff=0 and boundary_flux=0 with coercive D_m,mu_B",
            "energy identity forces delta_m=0; hence Phi_S=0 and the screened local profile is exact-zero in that branch",
            "EXACT_CONDITIONAL_NOHAIR_THEOREM",
            "requires parent-signed source silence and boundary/no-flux class; current corpus has closure-only boundary rows",
        ),
        (
            "BAT1750_2_finite_source_bound",
            "finite source amplitude",
            "nonzero J_eff and finite boundary mismatch",
            "||delta_m|| is bounded by boundary term plus source/mu_B; in canonical units Phi_S <= sqrt(D_m)[M_bdy exp(-d/ell_scr)+M_src+M_mL+M_nl]",
            "CONDITIONAL_AMPLITUDE_BOUND_DERIVED",
            "requires M_bdy, M_src, M_mL, M_nl, D_m, mu_B and source-support powers",
        ),
        (
            "BAT1750_3_boundary_amplitude_contract",
            "Phi_S source row",
            "phi=sqrt(D_m) delta_m at the matching surface",
            "Phi_S=sqrt(D_m) |delta_m|_boundary, and a no-hair branch gives Phi_S=0 only when the boundary/source theorem closes",
            "EXACT_CONDITIONAL_CONVERSION",
            "requires sourced boundary amplitude or parent no-flux/no-growing-branch theorem",
        ),
        (
            "BAT1750_4_shell_obstruction_retained",
            "transition shell",
            "transition support intersects local domain or boundary projector is not owned",
            "generic U_B or width suppression cannot hide the shell; shell current must be exact-zero/projected out by parent identity or included as finite Q_trans/Q_proj",
            "ANTI_CHEAT_GUARD_RETAINED",
            "requires boundary shell projector identity or explicit shell residual bound",
        ),
        (
            "BAT1750_5_verdict",
            "boundary amplitude theorem",
            "coercive operator gives exact zero or finite amplitude law",
            "1750 derives the theorem shape, but current inputs do not close the source/boundary premises",
            "THEOREM_CONTRACT_DERIVED_PREMISES_UNSIGNED",
            "next target must source/derive source silence plus boundary/no-flux class",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "object": obj,
            "premise": premise,
            "derived_result": result,
            "status": status,
            "missing_to_promote": missing,
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for theorem_id, obj, premise, result, status, missing in rows
    ]


def coefficient_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("CPA1750_0_D_m", "D_m", "kinetic/diffusion coefficient for variational R-lock completion", "SUPPORTED_BY_EQUATION_REGISTER_NOT_PARENT_ACTION", "needs parent action/energy slot, sign, units and source"),
        ("CPA1750_1_mu_B", "mu_B", "quadratic restoring coefficient in local stationary memory equation", "SYMBOLIC_RELAXATION_COEFFICIENT", "needs mu_B floor, source of gamma_B lambda_R or Pi_B/tau_L, and units"),
        ("CPA1750_2_gamma_lambda", "gamma_B;lambda_R", "mobility and curvature of R with mu_B=gamma_B lambda_R", "CONDITIONAL_R_LOCK_ONLY", "R functional, mobility law and microscopic origin not parent-derived"),
        ("CPA1750_3_a_F", "a_F", "trace-readout locking coefficient F_2=a_F lambda_R", "MISSING_PARENT_COEFFICIENT", "needed to keep readout stiffness from spoiling local PPN bounds"),
        ("CPA1750_4_kappa_m_Zm", "kappa_m/Z_m", "old gradient-completion kinetic coefficient", "MISSING_Z_M_SIGN_AND_VALUE", "1379/1302 keep sign/value/source missing"),
        ("CPA1750_5_F2", "F2", "second local curvature of trace potential or Fhat at fixed point", "CONDITIONAL_FROM_R_LOCK_OR_MISSING_PARENT_SOURCE", "F2=a_F lambda_R if R-lock is owned; otherwise missing parent source"),
        ("CPA1750_6_L0", "L0", "fixed parent length scale in old bridge", "ACTION_ROLE_SOURCED_NUMERIC_VALUE_MISSING", "fixed-L0 contract admissible but not live parent-signed or scale-set"),
        ("CPA1750_7_A_S", "A_S/Phi_S", "boundary/source amplitude at matching surface", "MISSING_PARENT_SOURCE", "requires source support, boundary class and no-growing-branch/no-flux theorem"),
        ("CPA1750_8_boundary_class", "boundary/no-flux/shell class", "condition selecting decaying/nohair branch", "CLOSURE_ONLY_CURRENTLY", "1276/802/803 reject hidden shell/no-flux shortcut"),
        ("CPA1750_9_projection", "A_ref;projection norms", "observable normalization for Q_alg/Q_trans", "MISSING_OPERATOR_PROJECTION_NORMS", "cannot score local arenas without map"),
        ("CPA1750_10_verdict", "coefficient provenance package", "all coefficient rows needed for local claim", "NOT_CLAIM_GRADE", "theorem contracts are sharper but no coefficient row is source-backed enough to score"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "quantity": quantity,
            "role": role,
            "current_status": status,
            "needed_to_promote": needed,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for audit_id, quantity, role, status, needed in rows
    ]


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAND1750_0_mu_m2_Rlock_variational", "mu_m^2", "mu_B/D_m", "length^-2", "R-lock variational completion", "THEOREM_CONTRACT_ONLY"),
        ("CAND1750_1_phi_Rlock", "phi", "sqrt(D_m) delta_m", "canonical field units", "canonical normalization", "THEOREM_CONTRACT_ONLY"),
        ("CAND1750_2_PhiS_Rlock", "Phi_S", "sqrt(D_m) |delta_m|_boundary", "canonical field units", "boundary amplitude conversion", "THEOREM_CONTRACT_ONLY"),
        ("CAND1750_3_F2_Rlock", "F2", "a_F lambda_R = a_F mu_B/gamma_B", "trace-readout units", "trace stiffness separation", "THEOREM_CONTRACT_ONLY"),
        ("CAND1750_4_PhiS_bound", "Phi_S_bound", "sqrt(D_m)[M_bdy exp(-d/ell_scr)+M_src+M_mL+M_nl]", "canonical field units", "finite source/boundary law", "BOUND_FORM_ONLY_NONCLAIM"),
        ("CAND1750_5_nohair_zero", "Phi_S_zero", "Phi_S=0 if J_eff=0 and boundary_flux=0 under coercive operator", "theorem-zero flag", "exact nohair branch", "CONDITIONAL_ZERO_THEOREM_PREMISES_UNSIGNED"),
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
            "accepted_as_contract": "True",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for row_id, quantity, formula, units, route, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1750_0_kinetic_status",
            "VARIATIONAL_RLOCK_GAP_CONTRACT_DERIVED",
            "if the stationary memory equation is parent-owned as an elliptic variational functional, D_m is the kinetic coefficient and mu_m^2=mu_B/D_m",
            "use this as the preferred canonical gap contract over an unowned kappa_m placeholder",
        ),
        (
            "DEC1750_1_trace_status",
            "TRACE_STIFFNESS_SEPARATED_FROM_DYNAMIC_GAP",
            "F2=a_F lambda_R controls readout stiffness, while mu_B/D_m controls screening; conflating them would hide a PPN failure mode",
            "keep both coefficients in future validators",
        ),
        (
            "DEC1750_2_boundary_status",
            "NOHAIR_AND_FINITE_AMPLITUDE_THEOREM_CONTRACT_DERIVED",
            "coercive energy identity gives exact zero if source and boundary flux vanish, or a finite Phi_S bound otherwise",
            "source/boundary premises still need parent ownership before any claim",
        ),
        (
            "DEC1750_3_claim_status",
            "NO_CLAIM_GRADE_LOCAL_ROW",
            "D_m, mu_B, a_F, source silence, boundary class and projection norms remain unsigned or non-numeric",
            "do not reopen local-GR/Newton/PPN/R10/WEP scoring",
        ),
        (
            "DEC1750_4_best_next",
            "TARGET_PARENT_ELLIPTIC_FUNCTIONAL_OWNERSHIP",
            "the next clean derivation is to prove the stationary memory equation comes from a parent-owned positive elliptic functional with source/boundary terms exposed",
            "build 1751 parent elliptic functional ownership or finite residual vector",
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
        ("GATE1750_0_Rlock_gap", "mu_m^2=mu_B/D_m is claim-grade", "BLOCKED_PARENT_ELLIPTIC_FUNCTIONAL_UNSIGNED"),
        ("GATE1750_1_kinetic_coeff", "D_m or kappa_m/Z_m is source-backed", "BLOCKED_COEFFICIENT_SIGN_UNITS_SOURCE"),
        ("GATE1750_2_trace_coeff", "F2/a_F/lambda_R is source-backed and PPN-safe", "BLOCKED_TRACE_STIFFNESS_SOURCE"),
        ("GATE1750_3_nohair", "Phi_S=0 nohair theorem closes", "BLOCKED_SOURCE_BOUNDARY_PREMISES_UNSIGNED"),
        ("GATE1750_4_finite_amplitude", "Phi_S finite bound can score", "BLOCKED_AMPLITUDE_INPUTS_MISSING"),
        ("GATE1750_5_shell", "transition shell is safely projected/zeroed", "BLOCKED_SHELL_ANTI_CHEAT_GUARD"),
        ("GATE1750_6_local_reentry", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
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
            "route_id": "NEXT1750_0_primary",
            "next_target": "1751-Y5-R2FR-parent-elliptic-functional-ownership-or-finite-residual-vector.md",
            "script": "scripts/Y5_R2FR_parent_elliptic_functional_ownership_or_finite_residual_vector.py",
            "objective": "prove the stationary memory equation is the Euler equation of a parent-owned positive elliptic functional with exposed source and boundary terms, or convert all unowned pieces into finite residual rows",
            "success_condition": "parent-owned D_m/mu_B/source/boundary clauses pass as nonclaim theorem rows, or an explicit residual vector replaces the would-be local GR derivation",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1750_1_fallback",
            "next_target": "1751b-Y5-R2FR-boundary-shell-projector-or-explicit-Qtrans-row.md",
            "script": "scripts/Y5_R2FR_boundary_shell_projector_or_explicit_Qtrans_row.py",
            "objective": "attack the boundary/shell anti-cheat guard directly if the parent elliptic functional route stalls",
            "success_condition": "shell exact-zero/projector theorem or explicit finite Q_trans/Q_proj row remains nonclaim but source-ready",
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
        "kinetic_theorem": kinetic_theorem_rows(),
        "boundary_theorem": boundary_theorem_rows(),
        "coefficient_audit": coefficient_audit_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1750_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1750_{key.upper()}.csv")


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


def candidate_contracts_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(
        row["accepted_as_contract"] == "True"
        and row["score_ready"] == "False"
        and row["valid_prediction_row"] == "False"
        and row["claim_allowed"] == "False"
        for row in rows_map["candidate_rows"]
    )


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1750_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1750_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1750*"):
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
    kinetic = rows_map["kinetic_theorem"]
    boundary = rows_map["boundary_theorem"]
    coefficients = rows_map["coefficient_audit"]
    decisions = rows_map["decision"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1750_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1750_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1750_2_Rlock_gap_identity", any(row["theorem_id"] == "KGT1750_1_canonical_normalization" and "mu_m^2=mu_B/D_m" in row["derived_result"] for row in kinetic), "R-lock variational gap identity is recorded", "R-lock gap identity missing"),
        check("VAL1750_3_trace_separation", any(row["theorem_id"] == "KGT1750_2_trace_stiffness_separation" and "not automatically" in row["derived_result"] for row in kinetic), "trace stiffness is separated from dynamic gap", "trace/dynamic separation missing"),
        check("VAL1750_4_nohair_theorem", any(row["theorem_id"] == "BAT1750_1_nohair_zero_case" and "Phi_S=0" in row["derived_result"] for row in boundary), "conditional nohair theorem is recorded", "nohair theorem missing"),
        check("VAL1750_5_finite_amplitude_bound", any(row["theorem_id"] == "BAT1750_2_finite_source_bound" and "Phi_S <=" in row["derived_result"] for row in boundary), "finite Phi_S amplitude bound is recorded", "finite amplitude bound missing"),
        check("VAL1750_6_coefficients_block_claim", any(row["audit_id"] == "CPA1750_10_verdict" and row["current_status"] == "NOT_CLAIM_GRADE" for row in coefficients), "coefficient package remains nonclaim", "coefficient verdict missing"),
        check("VAL1750_7_candidate_contracts_nonclaim", candidate_contracts_nonclaim(rows_map), "candidate rows are accepted only as nonclaim contracts", "candidate row was promoted or malformed"),
        check("VAL1750_8_decision_next", any(row["decision_id"] == "DEC1750_4_best_next" and row["decision"] == "TARGET_PARENT_ELLIPTIC_FUNCTIONAL_OWNERSHIP" for row in decisions), "decision selects parent elliptic functional ownership", "best-next decision missing"),
        check("VAL1750_9_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1750_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1750_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1750_12_next_selected", any(row["route_id"] == "NEXT1750_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1750_13_csv_parse", parsed_ok, "all generated 1750 CSVs parse", "one or more generated 1750 CSVs failed to parse"),
        check("VAL1750_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1750_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1750_16_formalization_untouched", formalization_untouched(), "no 1750 outputs found under formalization-workbench", "1750 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1750_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1750 parent kinetic coefficient and boundary amplitude theorem checkpoint" if overall else "one or more 1750 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1750 gets a real derivation upgrade: if the stationary memory equation is parent-owned as a positive elliptic functional, then `D_m` is the kinetic coefficient, `phi=sqrt(D_m) delta_m`, and `mu_m^2=mu_B/D_m`.",
        "- This is cleaner than the old placeholder `kappa_m` route, but it is still conditional because the parent action has not yet signed the elliptic functional, source term, boundary class, or coefficient units.",
        "- The trace/readout coefficient is kept separate: `F_2=a_F lambda_R=a_F mu_B/gamma_B` is not the same object as the dynamic screening gap unless the parent theory proves that identification.",
        "- The boundary side also improves: a coercive energy identity gives exact no-hair when source and boundary flux vanish, or a finite `Phi_S` bound when they do not.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Kinetic Gap Theorem",
        markdown_table(rows_map["kinetic_theorem"], ["theorem_id", "object", "derived_result", "status", "missing_to_promote"]),
        "",
        "## Boundary Amplitude Theorem",
        markdown_table(rows_map["boundary_theorem"], ["theorem_id", "object", "derived_result", "status", "missing_to_promote"]),
        "",
        "## Coefficient Provenance Audit",
        markdown_table(rows_map["coefficient_audit"], ["audit_id", "quantity", "current_status", "needed_to_promote"]),
        "",
        "## Candidate Rows",
        markdown_table(rows_map["candidate_rows"], ["row_id", "quantity", "formula", "current_status", "accepted_as_contract"]),
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
        "This is a useful step toward a GR/Newton limit because the local branch now has the right kind of mathematical object: a positive elliptic functional. If the parent action owns that object, the gap and amplitude become derivable. If it does not, the same equations must be treated as explicit finite residual closure and tested rather than claimed.",
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
    doc_path = ROOT / "1750-Y5-R2FR-parent-kinetic-coefficient-or-boundary-amplitude-theorem.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1750_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1750 validation FAIL")
    print("1750 validation PASS")


if __name__ == "__main__":
    main()
