from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_RAB_PARENT_THETAR_CONSTRUCTION_OR_QR_PRIOR_WIDTH_2266"
DOC = ROOT / "2266-Y5-R2FR-RAB-parent-ThetaR-construction-or-qR-prior-width-source.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2266_00_2265_doc",
        "source_key": "2265_doc",
        "source_path": ROOT / "2265-Y5-R2FR-RAB-parent-phase-space-owner-or-first-qR-bound-row.md",
        "needles": ["POA2265_6_verdict", "MOC2265_10_verdict", "NEXT2265_0_primary"],
        "role": "handoff: phase-space owner missing, Theta_R selected next",
    },
    {
        "source_id": "SRC2266_01_2265_validation",
        "source_key": "2265_validation",
        "source_path": OUT / "P8_Y5_BRR545_2265_VALIDATION.csv",
        "needles": ["VAL2265_OVERALL", "PASS"],
        "role": "confirms 2265 passed before 2266 starts",
    },
    {
        "source_id": "SRC2266_02_2265_owner_contract",
        "source_key": "2265_owner_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2265_MINIMUM_OWNER_CONTRACT.csv",
        "needles": ["MOC2265_1_theta_R", "MOC2265_10_verdict"],
        "role": "minimum owner contract with missing Theta_R",
    },
    {
        "source_id": "SRC2266_03_constraint_07",
        "source_key": "constraint_07",
        "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": ["S_constraint = integral lambda_R R_AB", "no R_AB kinetic term", "no conserved Q_R"],
        "role": "algebraic nonpropagating candidate block",
    },
    {
        "source_id": "SRC2266_04_observer_10",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "R_AB/J_q target and unsatisfied symplectic contract",
    },
    {
        "source_id": "SRC2266_05_noether_12",
        "source_key": "noether_12",
        "source_path": ROOT / "12-gauge-noether-origin-audit.md",
        "needles": ["delta lambda_R S = R_AB = 0", "first-class parent constraint", "closure-only"],
        "role": "multiplier route and warning against closure-only smuggling",
    },
    {
        "source_id": "SRC2266_06_micro_action",
        "source_key": "micro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "g_{μν} = η_{μν}", "∂²_t ψ"],
        "role": "primitive psi action that could own the base symplectic structure",
    },
    {
        "source_id": "SRC2266_07_macro_action",
        "source_key": "macro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["G_{μν} + Γ_G", "pure GR is recovered", "ψ : ℝ⁴ → ℝ"],
        "role": "macro metric action and GR-limit baseline",
    },
    {
        "source_id": "SRC2266_08_theta_template_1041",
        "source_key": "theta_template_1041",
        "source_path": ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
        "needles": ["delta L_X = E_A delta Y_X^A + nabla_mu Theta_X", "Theta_X/P_X template", "ROUTE_OPEN_NOT_CLOSED"],
        "role": "general symplectic-potential template used to classify algebraic vs derivative blocks",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2266_SOURCE_REGISTER.csv",
    "theta_derivation": OUT / "P8_Y5_PARENT_QLOC_2266_THETAR_DERIVATION_ATTEMPT.csv",
    "candidate_matrix": OUT / "P8_Y5_PARENT_QLOC_2266_THETAR_CANDIDATE_MATRIX.csv",
    "backreaction_contract": OUT / "P8_Y5_PARENT_QLOC_2266_LAMBDAR_BACKREACTION_CONTRACT.csv",
    "qr_prior": OUT / "P8_Y5_PARENT_QLOC_2266_QR_PRIOR_WIDTH_QUEUE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2266_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2266_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2266_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2266_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2266_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2266_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_theta": QUEUE / "JR2266_THETAR_DERIVATION_ATTEMPT_NONCLAIM.csv",
    "queue_backreaction": QUEUE / "JR2266_LAMBDAR_BACKREACTION_CONTRACT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_ThetaR_and_lambdaR_backreaction_refusal_2266.csv",
    "beta_docs": BETA_DOCS / "RAB_THETAR_OR_QR_PRIOR_WIDTH_2266_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def theta_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "TD2266_0_general_variation_rule",
            "object": "finite-jet variation",
            "derivation": "For any parent block L_R(Y,nabla Y,...), delta L_R=E_A delta Y^A + nabla_mu Theta_R^mu(delta Y). Theta_R collects integration-by-parts terms from derivatives of varied fields.",
            "status": "GENERAL_TEMPLATE_READY",
            "blocking_issue": "the actual parent R_AB block still has to be selected",
            "source_paths": source_refs("theta_template_1041"),
            "valid_for_claim": False,
        },
        {
            "derivation_id": "TD2266_1_algebraic_multiplier_block",
            "object": "S_R=int mu lambda_R R_AB[Y]",
            "derivation": "Because L_R contains no nabla(lambda_R) and no nabla(R_AB), delta L_R = mu R_AB delta lambda_R + mu lambda_R delta R_AB + lambda_R R_AB delta mu has no integration-by-parts derivative term from this block.",
            "status": "THETAR_ZERO_FOR_PURE_ALGEBRAIC_BLOCK",
            "blocking_issue": "this proves only the candidate block's Theta_R=0; it does not prove the block belongs to the MTS parent action",
            "source_paths": source_refs("constraint_07", "noether_12"),
            "valid_for_claim": False,
        },
        {
            "derivation_id": "TD2266_2_block_symplectic_consequence",
            "object": "Omega_R and pi_lambda",
            "derivation": "For the pure algebraic block, Theta_R^mu=0 implies omega_R=delta Theta_R=0 for the block and canonical pi_lambda=0 in a Hamiltonian split.",
            "status": "FORMAL_PRIMARY_CONSTRAINT_IF_BLOCK_EXISTS",
            "blocking_issue": "degenerate zero symplectic form is normal for a multiplier but requires the base parent phase space and Hamiltonian to be supplied",
            "source_paths": source_refs("2265_owner_contract", "constraint_07"),
            "valid_for_claim": False,
        },
        {
            "derivation_id": "TD2266_3_zero_equation",
            "object": "delta_lambda equation",
            "derivation": "Varying lambda_R gives R_AB=0, hence T^2S=1 and J_q=1, only inside the selected algebraic multiplier branch.",
            "status": "CONDITIONAL_ZERO_EQUATION",
            "blocking_issue": "the same variation also leaves lambda_R D_Y R_AB in the Y equations; that backreaction must vanish, be gauge, or be solved consistently",
            "source_paths": source_refs("observer_10", "noether_12"),
            "valid_for_claim": False,
        },
        {
            "derivation_id": "TD2266_4_not_a_full_owner",
            "object": "claim-grade Theta_R owner",
            "derivation": "The algebraic block gives a lawful zero Theta_R if assumed, but the current corpus has not derived lambda_R R_AB from psi, phase-volume balance, quotient geometry, or a first-class momentum map.",
            "status": "THETAR_ZERO_BLOCK_DERIVED_PARENT_ORIGIN_MISSING",
            "blocking_issue": "parent origin and lambda_R backreaction/compatibility are now the leading blockers",
            "source_paths": source_refs("2265_doc", "micro_action", "observer_10", "theta_template_1041"),
            "valid_for_claim": False,
        },
    ]


def candidate_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "TCM2266_0_algebraic_lambdaR",
            "candidate_block": "L_R=mu lambda_R R_AB",
            "Theta_R_result": "Theta_R=0 for the block",
            "zero_result": "delta_lambda gives R_AB=0",
            "main_risk": "lambda_R D_Y R_AB modifies base equations unless lambda_R=0/gauge/orthogonal is proved",
            "rank": 1,
            "current_status": "BEST_ZERO_ROUTE_BUT_PARENT_ORIGIN_AND_BACKREACTION_OPEN",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "TCM2266_1_phase_volume_lambda",
            "candidate_block": "L_R=mu lambda_R ln(J_q^2)",
            "Theta_R_result": "Theta_R=0 if J_q has no derivatives",
            "zero_result": "J_q=1 if lambda_R is parent-derived",
            "main_risk": "phase-volume law is not derived from the psi action or Liouville measure",
            "rank": 2,
            "current_status": "PROMISING_INTERPRETATION_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "TCM2266_2_psi_induced_constraint",
            "candidate_block": "L_R=mu lambda_R F_R[psi,pi_psi]",
            "Theta_R_result": "Theta from psi base action plus algebraic constraint contribution if F_R derivative-free; extra boundary terms if F_R uses gradients",
            "zero_result": "F_R=0 could imply R_AB=0 only if F_R maps exactly to ln(T^2S)",
            "main_risk": "no explicit F_R map from psi covariance to R_AB/J_q exists",
            "rank": 3,
            "current_status": "ROOT_DERIVATION_ROUTE_MAP_MISSING",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "TCM2266_3_derivative_residual",
            "candidate_block": "L_R=-1/2 W nabla R_AB nabla R_AB + J_R R_AB",
            "Theta_R_result": "Theta_R^mu=-W nabla^mu R_AB delta R_AB",
            "zero_result": "not automatic; Q_R=W partial_r R_AB hair appears",
            "main_risk": "this is a finite residual/fifth-force branch, not a local-GR derivation unless no-hair conditions close",
            "rank": 4,
            "current_status": "FINITE_RESIDUAL_FALLBACK_ONLY",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "TCM2266_4_closure_axiom",
            "candidate_block": "set R_AB=0 by local closure definition",
            "Theta_R_result": "none",
            "zero_result": "closure benchmark only",
            "main_risk": "smuggles GR-like AB=1 rather than deriving it",
            "rank": 5,
            "current_status": "DO_NOT_USE_AS_DERIVATION",
            "valid_for_claim": False,
        },
    ]


def backreaction_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "LBC2266_0_parent_origin",
            "required_condition": "lambda_R R_AB block belongs to the parent action",
            "mathematical_test": "derive lambda_R or the equivalent constraint C_R from psi/phase-volume/quotient primitives before local weak-field specialization",
            "current_status": "MISSING_LAMBDAR_PARENT_ORIGIN",
            "failure_mode": "otherwise the multiplier is an inserted plateau/closure axiom",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LBC2266_1_backreaction_zero",
            "required_condition": "lambda_R D_Y R_AB does not alter the reduced local equations",
            "mathematical_test": "prove lambda_R=0 on shell, D_Y R_AB is pure gauge/constraint-combination, or the modified equations reduce to the same PPN coefficients",
            "current_status": "MISSING_LAMBDAR_ELIMINATION",
            "failure_mode": "the constraint may enforce AB=1 while changing beta, matter coupling, or conservation",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LBC2266_2_constraint_preservation",
            "required_condition": "R_AB=0 is preserved by H_T",
            "mathematical_test": "compute dot R_AB={R_AB,H_T} and show it fixes a harmless multiplier or closes first-class/second-class consistently",
            "current_status": "MISSING_HAMILTONIAN_PRESERVATION",
            "failure_mode": "secondary constraint can generate tertiary conditions or inconsistency",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LBC2266_3_boundary_silence",
            "required_condition": "algebraic block introduces no Q_R edge hair and base boundary terms are compatible",
            "mathematical_test": "show pure block has no derivative boundary term and base parent boundary class gives exact/proper/zero charge",
            "current_status": "PURE_BLOCK_NO_DERIVATIVE_BUT_BASE_BOUNDARY_UNSIGNED",
            "failure_mode": "edge charge can reintroduce an exterior reciprocal residual",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LBC2266_4_matter_readout",
            "required_condition": "matter and clocks descend to the constrained quotient",
            "mathematical_test": "prove S_matter depends only on reduced variables or its R_AB source leg vanishes at required PPN/clock/WEP order",
            "current_status": "MISSING_MATTER_READOUT_DESCENT",
            "failure_mode": "local WEP/clock residuals become live even if geometry has AB=1",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LBC2266_5_verdict",
            "required_condition": "claim-grade algebraic multiplier route",
            "mathematical_test": "LBC2266_0 through LBC2266_4 pass jointly",
            "current_status": "LAMBDAR_BACKREACTION_CONTRACT_UNSIGNED",
            "failure_mode": "Theta_R=0 is a useful formal result but not yet a derived local-GR limit",
            "valid_for_claim": False,
        },
    ]


def qr_prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "QPW2266_0_zero_branch_width",
            "target": "q_R",
            "prior_type": "theorem_zero_width",
            "parent_input_needed": "lambda_R parent origin plus lambda_R backreaction elimination",
            "candidate_value_or_width": "0 only if LBC2266 contract closes",
            "units": "dimensionless",
            "status": "ZERO_WIDTH_NOT_CLAIMABLE",
            "source_path": rel(OUTPUTS["backreaction_contract"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QPW2266_1_finite_branch_width",
            "target": "q_R",
            "prior_type": "finite_parent_prior_width",
            "parent_input_needed": "normalization of residual R_AB operator or psi-to-R_AB map",
            "candidate_value_or_width": "MISSING_PARENT_WIDTH",
            "units": "dimensionless",
            "status": "PRIOR_WIDTH_SOURCE_MISSING",
            "source_path": rel(OUTPUTS["candidate_matrix"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QPW2266_2_QR_boundary_width",
            "target": "reciprocal_charge_Q_R",
            "prior_type": "boundary_charge_width",
            "parent_input_needed": "base boundary class plus exact/proper/zero charge theorem or finite charge normalization",
            "candidate_value_or_width": "MISSING_BOUNDARY_WIDTH",
            "units": "declared_boundary_normalization",
            "status": "BOUNDARY_PRIOR_WIDTH_SOURCE_MISSING",
            "source_path": rel(OUTPUTS["backreaction_contract"]),
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2266_0_full_theta_owner",
            "attempted_claim": "claim-grade Theta_R/Omega_R owner found",
            "runner_result": "BLOCKED",
            "blocked_by": "TD2266_4 says Theta_R=0 only for assumed algebraic block; parent origin missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2266_1_local_gr_zero",
            "attempted_claim": "local GR/Newton derived from algebraic multiplier",
            "runner_result": "BLOCKED",
            "blocked_by": "LBC2266_5_verdict=LAMBDAR_BACKREACTION_CONTRACT_UNSIGNED",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2266_2_qR_prior",
            "attempted_claim": "q_R/Q_R prior width is source-backed",
            "runner_result": "BLOCKED",
            "blocked_by": "QPW2266 rows lack parent width/value inputs",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2266_3_derivative_residual_as_zero",
            "attempted_claim": "derivative R_AB residual is a local-GR zero proof",
            "runner_result": "REJECTED",
            "blocked_by": "derivative block carries Theta_R and possible Q_R hair unless no-hair theorem closes",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2266_0_theta_zero_block",
            "claim": "Theta_R=0 for pure algebraic multiplier block",
            "gate_pass": False,
            "reason": "formal block result is true only conditionally and is not a parent-origin claim",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2266_1_lambdar_origin",
            "claim": "lambda_R R_AB arises from MTS primitives",
            "gate_pass": False,
            "reason": "no psi/phase-volume/quotient derivation supplied yet",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2266_2_backreaction",
            "claim": "lambda_R backreaction is harmless",
            "gate_pass": False,
            "reason": "lambda_R=0/gauge/orthogonality or equivalent PPN preservation not proved",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2266_3_qR_width",
            "claim": "finite q_R/Q_R prior width sourced",
            "gate_pass": False,
            "reason": "parent residual normalization is missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2266_4_local_GR",
            "claim": "derived local GR/Newton/PPN",
            "gate_pass": False,
            "reason": "still not achieved",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2266_0_formal_gain",
            "decision": "PURE_ALGEBRAIC_BLOCK_THETAR_ZERO",
            "reason": "if the parent really contains nonderivative lambda_R R_AB, that block has no symplectic boundary term and no independent propagating R_AB kinetic mode",
            "next_action": "use this as a conditional lemma, not a local-GR claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2266_1_new_blocker",
            "decision": "LAMBDAR_ORIGIN_AND_BACKREACTION_NOW_DOMINATE",
            "reason": "the hard issue shifts from finding a nonzero Theta_R to proving lambda_R R_AB is parent-derived and does not spoil the reduced equations",
            "next_action": "derive lambda_R from phase-volume/quotient/psi primitives or prove lambda_R=0/gauge after variation",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2266_2_finite_branch",
            "decision": "QR_PRIOR_WIDTH_STILL_UNSOURCED",
            "reason": "if the algebraic branch fails, finite q_R/Q_R needs a parent normalization, not an external bound",
            "next_action": "keep q_R prior rows nonclaim until parent width/value exists",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2266_3_next",
            "decision": "LAMBDAR_ORIGIN_OR_BACKREACTION_ELIMINATION_NEXT",
            "reason": "this is now the shortest path to derived local GR: origin plus harmless multiplier backreaction",
            "next_action": "2267-Y5-R2FR-RAB-lambdaR-origin-or-backreaction-elimination.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2266_0_primary",
            "next_target": "2267-Y5-R2FR-RAB-lambdaR-origin-or-backreaction-elimination.md",
            "script": "scripts/Y5_R2FR_RAB_lambdaR_origin_or_backreaction_elimination_2267.py",
            "objective": "try to derive lambda_R R_AB from phase-volume/quotient/psi primitives or prove that lambda_R backreaction vanishes/is gauge after imposing R_AB=0; otherwise keep the branch closure-only",
            "selection_status": "selected",
            "success_condition": "lambda_R has a parent origin and the reduced equations keep GR/Newton/PPN coefficients, or the route is explicitly demoted and finite q_R prior sourcing begins",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2266_theta",
            "source_path": rel(OUTPUTS["theta_derivation"]),
            "target_path": rel(COPY_TARGETS["queue_theta"]),
            "target_exists": COPY_TARGETS["queue_theta"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_theta"]),
            "reason": "Theta_R derivation attempt copied as nonclaim queue",
        },
        {
            "copy_id": "BC2266_backreaction",
            "source_path": rel(OUTPUTS["backreaction_contract"]),
            "target_path": rel(COPY_TARGETS["queue_backreaction"]),
            "target_exists": COPY_TARGETS["queue_backreaction"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_backreaction"]),
            "reason": "lambda_R backreaction contract copied as nonclaim queue",
        },
        {
            "copy_id": "BC2266_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]),
            "reason": "branch-locked WEP/local refusal gates",
        },
        {
            "copy_id": "BC2266_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]),
            "reason": "portable Theta_R/backreaction decision ledger",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    theta = read_csv(OUTPUTS["theta_derivation"])
    matrix = read_csv(OUTPUTS["candidate_matrix"])
    backreaction = read_csv(OUTPUTS["backreaction_contract"])
    qr = read_csv(OUTPUTS["qr_prior"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2266_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2266_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2266_2_prior_validation",
            any(row["source_key"] == "2265_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2265 validation passes",
        ),
        (
            "VAL2266_3_theta_zero_block_written",
            any(row["derivation_id"] == "TD2266_1_algebraic_multiplier_block" and row["status"] == "THETAR_ZERO_FOR_PURE_ALGEBRAIC_BLOCK" for row in theta),
            "algebraic multiplier Theta_R=0 block lemma written",
        ),
        (
            "VAL2266_4_parent_origin_not_claimed",
            any(row["derivation_id"] == "TD2266_4_not_a_full_owner" and row["status"] == "THETAR_ZERO_BLOCK_DERIVED_PARENT_ORIGIN_MISSING" for row in theta)
            and all(row["valid_for_claim"].lower() == "false" for row in theta),
            "Theta_R formal gain is not parent-promoted",
        ),
        (
            "VAL2266_5_candidate_matrix",
            {row["candidate_id"] for row in matrix}
            >= {"TCM2266_0_algebraic_lambdaR", "TCM2266_1_phase_volume_lambda", "TCM2266_2_psi_induced_constraint", "TCM2266_3_derivative_residual", "TCM2266_4_closure_axiom"},
            "all Theta_R candidate routes classified",
        ),
        (
            "VAL2266_6_backreaction_contract_unsigned",
            any(row["contract_id"] == "LBC2266_5_verdict" and row["current_status"] == "LAMBDAR_BACKREACTION_CONTRACT_UNSIGNED" for row in backreaction)
            and all(row["valid_for_claim"].lower() == "false" for row in backreaction),
            "lambda_R backreaction contract remains unsigned",
        ),
        (
            "VAL2266_7_qr_prior_nonclaim",
            all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in qr),
            "q_R/Q_R prior-width rows remain nonclaim",
        ),
        (
            "VAL2266_8_refusal_blocks",
            all(row["score_eligible"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in refusal),
            "refusal runner blocks local claims",
        ),
        (
            "VAL2266_9_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates are all blocked",
        ),
        (
            "VAL2266_10_next_selected",
            any(row["route_id"] == "NEXT2266_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2267 target selected",
        ),
        ("VAL2266_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2266 CSVs parse"),
        (
            "VAL2266_12_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass")
            ),
            "no generated score/claim/gate flags are true",
        ),
        (
            "VAL2266_13_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2266_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2266_15_formalization_no_2266",
            not any(
                path.is_file()
                and (path.name.startswith("2266-") or (path.name.startswith("P8_Y5") and "2266" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2266 output files",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2266_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2266 derives Theta_R=0 for a pure algebraic multiplier block, keeps parent origin/backreaction unsigned, and selects 2267",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    theta = read_csv(OUTPUTS["theta_derivation"])
    matrix = read_csv(OUTPUTS["candidate_matrix"])
    backreaction = read_csv(OUTPUTS["backreaction_contract"])
    qr = read_csv(OUTPUTS["qr_prior"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2266 - Y5/R2FR R_AB Parent Theta_R Construction Or q_R Prior Width Source",
        "",
        "## Verdict",
        "",
        "2266 makes a real mathematical gain: for the pure nonderivative multiplier block `S_R=int mu lambda_R R_AB`, the block symplectic potential is exactly zero. There is no integration-by-parts boundary term from that block, so `Theta_R=0`, `omega_R=0`, and the Hamiltonian split has the expected multiplier primary constraint `pi_lambda≈0` if the block exists.",
        "",
        "That is useful, but it is not the full local-GR derivation. It proves the algebraic-block lemma, not the parent origin of the block. The remaining sharp blocker is now `lambda_R`: why does the parent MTS action contain this multiplier, and why does the `lambda_R D_Y R_AB` backreaction not distort the reduced weak-field equations?",
        "",
        "So the route is better than before: we do not need to hunt a mysterious nonzero `Theta_R` for the zero branch. We need to derive the algebraic multiplier's origin and eliminate or gauge its backreaction. If that fails, the branch becomes closure-only and finite `q_R/Q_R` prior-width sourcing takes over.",
        "",
        "No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Theta_R Derivation Attempt",
        table(["derivation_id", "object", "derivation", "status", "blocking_issue", "source_paths", "valid_for_claim"], theta),
        "",
        "## Theta_R Candidate Matrix",
        table(["candidate_id", "candidate_block", "Theta_R_result", "zero_result", "main_risk", "rank", "current_status", "valid_for_claim"], matrix),
        "",
        "## lambda_R Backreaction Contract",
        table(["contract_id", "required_condition", "mathematical_test", "current_status", "failure_mode", "valid_for_claim"], backreaction),
        "",
        "## q_R/Q_R Prior-Width Queue",
        table(["row_id", "target", "prior_type", "parent_input_needed", "candidate_value_or_width", "units", "status", "source_path", "score_ready", "valid_for_claim"], qr),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is a forward step, not a loop. The old blocker said 'find the R_AB phase-space owner'. The new result says: for the zero route the R_AB block should not own a propagating phase space at all; it should be an algebraic multiplier block with zero Theta. The real fight is now whether MTS can derive that multiplier from its primitives and show its backreaction is harmless. That is a much narrower and more attackable target.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["theta_derivation"], theta_derivation_rows())
    write_csv(OUTPUTS["candidate_matrix"], candidate_matrix_rows())
    write_csv(OUTPUTS["backreaction_contract"], backreaction_contract_rows())
    write_csv(OUTPUTS["qr_prior"], qr_prior_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["theta_derivation"], COPY_TARGETS["queue_theta"])
    shutil.copyfile(OUTPUTS["backreaction_contract"], COPY_TARGETS["queue_backreaction"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
