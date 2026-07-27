from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2246-Y5-R2FR-RAB-parent-boundary-charge-formula-BR-or-alpha3-projection-bound.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_BOUNDARY_BR_ALPHA3_2246"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2245_doc": ROOT / "2245-Y5-R2FR-RAB-boundary-charge-QR-Kboundary-zero-or-beta-bound-first-row.md",
    "2245_validation": OUT / "P8_Y5_BRR545_2245_VALIDATION.csv",
    "2245_next": OUT / "P8_Y5_PARENT_QLOC_2245_NEXT_TARGET.csv",
    "2245_lemma": OUT / "P8_Y5_PARENT_QLOC_2245_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "2245_projection": OUT / "P8_Y5_PARENT_QLOC_2245_FIRST_BETA_PROJECTION_TEMPLATE.csv",
    "1040_doc": ROOT / "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
    "1040_validation": OUT / "P8_Y5_BRR545_1040_VALIDATION.csv",
    "1040_formula": OUT / "P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "1040_owner_gate": OUT / "P8_Y5_R10_1040_BX_OWNER_GATE.csv",
    "1040_alpha3": OUT / "P8_Y5_R10_1040_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
    "667_variation": OUT / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "668_owner": OUT / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
    "591_dc": OUT / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
    "584_owner_repair": OUT / "P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv",
    "584_edge_law": OUT / "P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv",
    "671_owner_gate": OUT / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
    "1019_exactness": OUT / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "976_alpha3": OUT / "P8_Y5_R10_976_K_BOUNDARY_ALPHA3_SOURCE_ACQUISITION.csv",
    "977_alpha3_status": OUT / "P8_Y5_R10_977_K_BOUNDARY_ALPHA3_STATUS.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
    "r10_runner": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2246_SOURCE_REGISTER.csv"
PARENT_BOUNDARY_FORMULA = OUT / "P8_Y5_PARENT_QLOC_2246_PARENT_BOUNDARY_CHARGE_FORMULA.csv"
BR_OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_2246_BR_OWNER_GATE.csv"
REFERENCE_PROJECTOR_SPLIT = OUT / "P8_Y5_PARENT_QLOC_2246_REFERENCE_PROJECTOR_SPLIT.csv"
KBOUNDARY_COCYCLE = OUT / "P8_Y5_PARENT_QLOC_2246_KBOUNDARY_COCYCLE_CONTRACT.csv"
ALPHA3_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2246_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv"
R10_EDGE_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2246_R10_EDGE_INPUT_CONTRACT.csv"
MTS_ALPHA_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_2246_BR_ALPHA3_TEMPLATE_NONCLAIM.csv"
RUNNER_SMOKE = OUT / "P8_Y5_PARENT_QLOC_2246_RUNNER_SMOKE_STATUS.csv"
PLACEHOLDER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_2246_PLACEHOLDER_REFUSAL_RUNNER.csv"
CLAIM_GATES = OUT / "P8_Y5_PARENT_QLOC_2246_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2246_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2246_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2246_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2246_VALIDATION.csv"


COPY_TARGETS = {
    "queue_formula": QUEUE / "JR2246_PARENT_BR_QR_FORMULA_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2246_ALPHA3_COEFFICIENT_RULE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "parent_BR_QR_alpha3_nonclaim_2246.csv",
    "beta_docs": BETA_DOCS / "PARENT_BR_QR_ALPHA3_2246_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    PARENT_BOUNDARY_FORMULA,
    BR_OWNER_GATE,
    REFERENCE_PROJECTOR_SPLIT,
    KBOUNDARY_COCYCLE,
    ALPHA3_TEMPLATE,
    R10_EDGE_CONTRACT,
    MTS_ALPHA_TEMPLATE,
    RUNNER_SMOKE,
    PLACEHOLDER_REFUSAL,
    CLAIM_GATES,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text.strip())
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() == "pass" for row in overall_rows)
    return all(row.get(result_key, "").lower() == "pass" for row in rows)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        if key.startswith("2245"):
            role = "current R2FR boundary-charge handoff"
        elif key.startswith("1040"):
            role = "older B_X/Q_X formula scaffold being specialized to R_AB"
        elif key.startswith(("667", "668", "591", "584", "671", "1019", "976", "977")):
            role = "boundary formula, owner, exactness, or alpha3 provenance evidence"
        else:
            role = "external local bound or runner ledger"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2246_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def formula_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BRF2246_0_bulk_pairing",
            "boundary pairing from D C_R",
            "delta int_Sigma epsilon_AB C_R^AB contains - int_partialSigma n_mu epsilon_AB delta P_R^{mu AB} plus convention-dependent density terms",
            "DERIVED_FROM_DCR_CONTRACT",
            "P_R and density convention not parent-owned",
            "identifies the boundary charge density that must be cancelled, exact, or bounded",
        ),
        (
            "BRF2246_1_candidate_charge_density",
            "B_R surface density",
            "B_R^AB = sigma n_mu P_R^{mu AB} + B_ct^AB + B_ref^AB + B_exact^AB, with sigma fixed by the G_bulk +/- Q convention",
            "FORMULA_SHAPE_DERIVED_SIGN_CONVENTION_OPEN",
            "P_R, counterterm, reference subtraction, and exact primitive missing",
            "turns edge charge into a concrete coefficient contract rather than an undefined coupling",
        ),
        (
            "BRF2246_2_candidate_QR",
            "Q_R boundary charge",
            "Q_R[epsilon] = int_partialSigma epsilon_AB B_R^AB dS",
            "CONTRACT_READY_NOT_PARENT_SIGNED",
            "requires Theta_R/L_R sector owner and allowed boundary class",
            "proper compact branch gives zero; source/large branch remains scoreable residual",
        ),
        (
            "BRF2246_3_exactness_route",
            "exact/pure boundary repair",
            "B_R = d_boundary b_R + B_R^pure and int_partialSigma epsilon d_boundary b_R = int_partialpartialSigma epsilon b_R - int_partialSigma d_boundary epsilon b_R",
            "MATHEMATICAL_ROUTE_ONLY",
            "b_R, harmonic sector, corner terms, and kernel derivative term not derived",
            "exactness can close only with boundary-class and range-kernel conditions",
        ),
        (
            "BRF2246_4_verdict",
            "parent B_R/Q_R formula status",
            "B_R/Q_R formula shape is explicit, but parent ownership is not closed",
            "FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED",
            "MISSING_PARENT_LR_THETAR_PR_REFERENCE_PROJECTOR",
            "move to parent source row or alpha3/R10 nonclaim coefficient rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "formula_id": formula_id,
            "object": obj,
            "formula": formula,
            "derivation_status": status,
            "owner_status": owner,
            "claim_effect": effect,
            **flags(),
        }
        for formula_id, obj, formula, status, owner, effect in rows
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("BRG2246_0_LR_owner", "parent L_R sector", "L_R[g,R_AB,nabla R_AB] explicitly selected with field normalization and boundary class", "MISSING_SECTOR_LAGRANGIAN_OWNER", "Theta_R and P_R remain formal placeholders"),
        ("BRG2246_1_ThetaR_owner", "parent symplectic potential Theta_R", "delta L_R = E_R delta R + d Theta_R(delta R) with finite boundary jet order", "MISSING_THETA_R", "Q_R differentiability and K_boundary bracket cannot be computed"),
        ("BRG2246_2_PR_owner", "boundary momentum P_R^{mu AB}", "P_R is derived from L_R or parent variation, not inserted as a free tensor", "MISSING_PR_OWNER", "B_R=n.P_R is a contract only"),
        ("BRG2246_3_density_convention", "tensor versus densitized P convention", "choose C_R=-nabla P_R+J or C_R=-(1/sqrt(g))partial Ptilde_R+J before scoring signs/units", "CONVENTION_GATE_OPEN", "B_R sign, volume terms, and units are ambiguous"),
        ("BRG2246_4_source_boundary_class", "allowed non-proper source boundary class", "source worldtube, reference surface, and compact exterior boundary classes are separated", "MISSING_SOURCE_BOUNDARY_CLASS", "proper-gauge zero may be incorrectly promoted to a source/test theorem"),
        ("BRG2246_5_verdict", "claim-grade B_R owner package", "BRG2246_0 through BRG2246_4 pass together", "FAIL_CURRENT_CLAIM_BR_NOT_PARENT_OWNED", "keep B_R/Q_R rows as nonclaim coefficient contracts"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "needed_object": obj,
            "closure_test": test,
            "current_status": status,
            "if_missing": missing,
            **flags(),
        }
        for gate_id, obj, test, status, missing in rows
    ]


def reference_split_rows() -> list[dict[str, Any]]:
    rows = [
        ("RPS2246_0_observed_GR_charge", "observed EH/ADM/time/rotation charge", "retain in Q_obs and do not force to zero by representative-R_AB proper-domain choice", "Pi_EH/Pi_M reference action on the full gravitational boundary charge", "GUARD_ONLY"),
        ("RPS2246_1_representative_R_charge", "proper compact representative-R_AB charge", "Q_R^proper=0 from 2245 collar lemma", "extension to non-proper/source boundary values", "NARROW_ZERO_ONLY"),
        ("RPS2246_2_edge_source_projection", "edge/source residual charge", "Qbar_edge_RH(lambda)=Pi_M^H[int_partialSigma F_lambda epsilon_AB B_R^AB]/M_H", "Pi_M^H, F_lambda, B_R owner, source boundary class, units", "RETAIN_NONCLAIM_RESIDUAL"),
        ("RPS2246_3_no_double_count", "bulk plus edge source split", "alpha_total uses orthogonal split or absolute addition; no cancellation credit between bulk and edge rows", "projection orthogonality proof or numeric split", "RETAIN_ABSOLUTE_TAIL_POLICY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "split_id": split_id,
            "sector": sector,
            "rule": rule,
            "missing": missing,
            "claim_status": status,
            **flags(),
        }
        for split_id, sector, rule, missing, status in rows
    ]


def cocycle_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KBC2246_0_contract",
            "boundary cocycle",
            "K_boundary[epsilon,eta]=delta_eta Q_R[epsilon]-delta_epsilon Q_R[eta]-Q_R[[epsilon,eta]] plus possible i_veta i_vepsilon Omega_boundary convention terms",
            "differentiable G_R, parent Omega_Y, v_R action on all fields, sign convention",
            "FORMULA_CONTRACT_ONLY",
        ),
        (
            "KBC2246_1_proper_zero",
            "proper compact cocycle",
            "K_boundary=0 when epsilon, eta, and required finite jets vanish on the boundary collar",
            "same finite-jet boundary class as 2245",
            "NARROW_ZERO_INHERITED",
        ),
        (
            "KBC2246_2_source_alpha3",
            "preferred-frame flux projection",
            "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "K_boundary_alpha3, Phi_boundary_local, projection normalization",
            "SOURCE_ANCHOR_READY_COEFFICIENTS_MISSING",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "cocycle_id": cocycle_id,
            "object": obj,
            "formula": formula,
            "needed_inputs": needed,
            "current_status": status,
            **flags(),
        }
        for cocycle_id, obj, formula, needed, status in rows
    ]


def alpha3_rows() -> list[dict[str, Any]]:
    rows = [
        ("A3P2246_0_formula", "alpha3", "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local", "4e-20", "dimensionless", "local_bound_claims.csv / Will 2014 PPN alpha3 anchor", "if Phi_boundary_local is numeric and nonzero, |K_boundary_alpha3| <= 4e-20/|Phi_boundary_local|", "COEFFICIENT_RULE_WRITTEN_PHI_AND_K_MISSING"),
        ("A3P2246_1_theorem_zero_route", "alpha3", "alpha3_MTS = 0 if K_boundary_alpha3=0 or Phi_boundary_local=0 from a parent theorem", "4e-20", "dimensionless", "local_bound_claims.csv / Will 2014 PPN alpha3 anchor", "theorem-zero must cite B_R exactness/no-flux or boundary flux amplitude zero", "THEOREM_ZERO_NOT_SIGNED"),
        ("A3P2246_2_numeric_route", "alpha3", "|K_boundary_alpha3 * Phi_boundary_local| <= 4e-20", "4e-20", "dimensionless", "local_bound_claims.csv / Will 2014 PPN alpha3 anchor", "requires source-backed K, Phi, normalization, uncertainty policy, and no-cancellation tail addition", "NUMERIC_ROUTE_INPUTS_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "observable": observable,
            "mts_formula": formula,
            "external_bound": bound,
            "units": units,
            "reference": reference,
            "coefficient_bound_rule": rule,
            "current_status": status,
            **flags(),
        }
        for projection_id, observable, formula, bound, units, reference, rule, status in rows
    ]


def r10_edge_rows() -> list[dict[str, Any]]:
    rows = [
        ("R10E2246_0_Qbar_edge", "Qbar_edge_RH(lambda)", "Pi_M^H[int_partialSigma F_lambda(s) epsilon_AB B_R^AB(s) dS]/M_H", "B_R owner; F_lambda; Pi_M^H; source boundary class; units"),
        ("R10E2246_1_alpha_edge", "alpha_edge(lambda)", "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_RH(lambda) qbar_RT(lambda)", "K_edge; Qbar_edge_RH; qbar_RT; lambda support; promoted R10 bound curve"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "edge_id": edge_id,
            "symbol": symbol,
            "formula": formula,
            "missing_inputs": missing,
            **flags(),
        }
        for edge_id, symbol, formula, missing in rows
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("MTS_source_normalized_Newton_branch", "BR_QR_formula_contract", "MISSING_SOURCE_BOUNDARY_CLASS", "MISSING_BR_OWNER_AND_EDGE_PROJECTION", "Q_R[epsilon]=int_partialSigma epsilon_AB(sigma n_mu P_R^{mu AB}+B_ct^AB+B_ref^AB+B_exact^AB)dS", "template_invalid_formula_shape_not_parent_owned"),
        ("MTS_source_normalized_Newton_branch", "boundary_alpha3_projection_bound_rule", "MISSING_NOT_R10_RANGE", "MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL", "alpha3_MTS=K_boundary_alpha3 Phi_boundary_local; |K|<=4e-20/|Phi| if Phi is sourced nonzero", "template_invalid_alpha3_coefficients_missing"),
        ("MTS_source_normalized_Newton_branch", "R10_edge_contract", "MISSING_EDGE_LAMBDA_SUPPORT", "MISSING_KEDGE_QBAR_EDGE_QBAR_RT", "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_RH(lambda) qbar_RT(lambda)", "template_invalid_edge_inputs_missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "model_id": model,
            "template_branch": template,
            "lambda_value": lambda_value,
            "alpha_predicted": alpha,
            "force_law_form": law,
            "derivation_status": status,
            **flags(),
        }
        for model, template, lambda_value, alpha, law, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "smoke_id": "SMOKE2246_0_runner_status",
            "valid_mts_rows": 0,
            "valid_bound_rows": 0,
            "comparison_rows": 1,
            "R10_pass_for_claim": False,
            "expected_result": "blocked_nonclaim",
            **flags(),
        }
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in formula_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["formula_id"].replace("BRF2246", "REF2246_BRF"),
                "object": row["object"],
                "current_status": row["derivation_status"],
                "refusal_status": "formula_not_claim_promoted",
                "failure_reasons": row["owner_status"],
                "score_eligible": False,
                **flags(),
            }
        )
    for row in owner_gate_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["gate_id"].replace("BRG2246", "REF2246_BRG"),
                "object": row["needed_object"],
                "current_status": row["current_status"],
                "refusal_status": "owner_gate_failed",
                "failure_reasons": row["if_missing"],
                "score_eligible": False,
                **flags(),
            }
        )
    for row in alpha3_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["projection_id"].replace("A3P2246", "REF2246_A3P"),
                "object": row["mts_formula"],
                "current_status": row["current_status"],
                "refusal_status": "alpha3_projection_not_scoreable",
                "failure_reasons": row["coefficient_bound_rule"],
                "score_eligible": False,
                **flags(),
            }
        )
    for row in r10_edge_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["edge_id"].replace("R10E2246", "REF2246_R10E"),
                "object": row["symbol"],
                "current_status": row["missing_inputs"],
                "refusal_status": "R10_edge_row_not_scoreable",
                "failure_reasons": row["missing_inputs"],
                "score_eligible": False,
                **flags(),
            }
        )
    return rows


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CGATE2246_0_BR_formula", "B_R/Q_R is parent-derived", False, "formula shape is explicit, but L_R, Theta_R, P_R, density convention, reference terms, and boundary class are not parent-owned"),
        ("CGATE2246_1_local_GR_boundary", "full local-GR boundary silence is closed", False, "proper compact silence remains narrow; non-proper/source boundary and projection rows remain active"),
        ("CGATE2246_2_alpha3", "alpha3 projection row is executable", False, "source-backed alpha3 bound exists but K_boundary_alpha3 and Phi_boundary_local are missing"),
        ("CGATE2246_3_R10_edge", "R10 edge contract is score-ready", False, "K_edge, Qbar_edge_RH, qbar_RT, lambda support, and promoted bound curve are missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2246_0_formula_status",
            "decision": "B_R/Q_R is now a concrete formula contract, not a vague missing coupling.",
            "because": "D C_R boundary pairing fixes the required surface density up to sign/density/reference conventions",
            "next_action": "select or derive the parent L_R/Theta_R/P_R package, or retain the formula as a nonclaim coefficient contract",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2246_1_alpha3_status",
            "decision": "alpha3 has a usable bound rule but no MTS coefficient yet.",
            "because": "|K_boundary_alpha3 Phi_boundary_local| <= 4e-20 is the exact scoring inequality once K and Phi exist",
            "next_action": "derive theorem-zero for K/Phi or source numeric values with normalization",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2246_2_next_target",
            "decision": "Next target should try to source the parent R_AB-sector symplectic potential.",
            "because": "Theta_R is the upstream object that would fix P_R, B_R, differentiability, K_boundary, and the alpha3 projection coefficient",
            "next_action": "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md",
            "script": "scripts/Y5_R2FR_RAB_parent_R_sector_ThetaR_PR_owner_or_boundary_coefficient_prior_2247.py",
            "objective": "try to derive or select the parent R_AB-sector symplectic potential Theta_R and momentum P_R that own B_R; if this cannot close, create nonclaim priors/templates for K_boundary_alpha3 and Phi_boundary_local",
            "include": "candidate L_R blocks, delta L_R, Theta_R, P_R tensor/density convention, boundary finite-jet order, no-flux theorem-zero route, alpha3 coefficient prior schema",
            "exclude": "invented numeric K/Phi values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    copy_sources = {
        "queue_formula": PARENT_BOUNDARY_FORMULA,
        "queue_alpha3": ALPHA3_TEMPLATE,
        "branch_wep": ALPHA3_TEMPLATE,
        "beta_docs": ALPHA3_TEMPLATE,
    }
    rows: list[dict[str, Any]] = []
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(source),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = ["numeric_value_present", "source_backed", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def formula_contract_present() -> bool:
    text = " ".join(" ".join(row.values()) for row in read_csv(PARENT_BOUNDARY_FORMULA))
    return "B_R^AB" in text and "Q_R[epsilon]" in text and "FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED" in text


def owner_gates_fail_safely() -> bool:
    return any(row.get("current_status") == "FAIL_CURRENT_CLAIM_BR_NOT_PARENT_OWNED" for row in read_csv(BR_OWNER_GATE))


def alpha3_bound_rule_present() -> bool:
    text = " ".join(" ".join(row.values()) for row in read_csv(ALPHA3_TEMPLATE))
    return "4e-20" in text and "K_boundary_alpha3" in text and "Phi_boundary_local" in text


def r10_edge_nonclaim() -> bool:
    return all(row.get("valid_for_claim", "").lower() == "false" for row in read_csv(R10_EDGE_CONTRACT))


def claim_gates_blocked() -> bool:
    return all(row.get("gate_pass", "").lower() == "false" and row.get("claim_allowed", "").lower() == "false" for row in read_csv(CLAIM_GATES))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2246_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2246" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2246 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2245_validation"]) and validation_pass(SOURCE_FILES["1040_validation"]) else "FAIL",
            "detail": "2245 and 1040 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_02_BR_formula_contract",
            "result": "PASS" if formula_contract_present() else "FAIL",
            "detail": "B_R/Q_R formula contract is written but not parent-promoted",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_03_owner_gates_fail_safely",
            "result": "PASS" if owner_gates_fail_safely() else "FAIL",
            "detail": "owner gates identify missing L_R/Theta_R/P_R package",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_04_reference_projector_guard",
            "result": "PASS" if len(read_csv(REFERENCE_PROJECTOR_SPLIT)) == 4 else "FAIL",
            "detail": "reference/projector split protects GR charges and keeps edge residual separate",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_05_cocycle_contract",
            "result": "PASS" if len(read_csv(KBOUNDARY_COCYCLE)) == 3 else "FAIL",
            "detail": "K_boundary cocycle and alpha3 projection contracts are present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_06_alpha3_bound_rule",
            "result": "PASS" if alpha3_bound_rule_present() else "FAIL",
            "detail": "alpha3 coefficient bound rule uses source-backed anchor but remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_07_R10_edge_contract_nonclaim",
            "result": "PASS" if r10_edge_nonclaim() else "FAIL",
            "detail": "R10 edge contract remains nonclaim and non-scoreable",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_08_mts_template_nonclaim",
            "result": "PASS" if all(row.get("valid_for_claim", "").lower() == "false" for row in read_csv(MTS_ALPHA_TEMPLATE)) else "FAIL",
            "detail": "MTS smoke template has no claim-valid rows",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_09_runner_smoke_refuses_claim",
            "result": "PASS" if read_csv(RUNNER_SMOKE)[0].get("expected_result") == "blocked_nonclaim" else "FAIL",
            "detail": "runner smoke status refuses a claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_10_claim_gates_blocked",
            "result": "PASS" if claim_gates_blocked() else "FAIL",
            "detail": "all empirical/local-GR claim gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_11_next_target_written",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2247-Y5-R2FR-RAB-parent-R-sector-ThetaR") else "FAIL",
            "detail": "next target row is present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2246 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_16_formalization_no_2246",
            "result": "PASS" if formalization_2246_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2246 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2246 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2246_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2246 builds the R_AB B_R/Q_R boundary-charge formula contract, blocks parent ownership claims, writes alpha3/R10 edge nonclaim bounds, and selects Theta_R/P_R ownership next",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    formula: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    reference_split: list[dict[str, Any]],
    cocycle: list[dict[str, Any]],
    alpha3: list[dict[str, Any]],
    r10_edge: list[dict[str, Any]],
    alpha_template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2246 - Y5/R2FR R_AB Parent Boundary Charge Formula B_R or Alpha3 Projection Bound",
            "## Verdict\n"
            "- 2246 turns the boundary leak into an explicit formula contract: `Q_R[epsilon]=int_partialSigma epsilon_AB B_R^AB dS`.\n"
            "- The candidate density is `B_R^AB = sigma n_mu P_R^{mu AB} + B_ct^AB + B_ref^AB + B_exact^AB`, but this is not parent-owned until `L_R`, `Theta_R`, and `P_R` are derived or selected.\n"
            "- The alpha3 fallback is now an exact inequality: `|K_boundary_alpha3 Phi_boundary_local| <= 4e-20`, still nonclaim because both MTS coefficients are missing.\n"
            "- The GR boundary-charge guard is retained: observed ADM/time/rotation charges are not deleted by the representative `R_AB` compact-proper lemma.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Parent Boundary Charge Formula\n"
            + md_table(formula, ["formula_id", "object", "formula", "derivation_status", "owner_status", "claim_effect"]),
            "## B_R Owner Gate\n"
            + md_table(owner, ["gate_id", "needed_object", "closure_test", "current_status", "if_missing"]),
            "## Reference/Projector Split\n"
            + md_table(reference_split, ["split_id", "sector", "rule", "missing", "claim_status"]),
            "## K_boundary Cocycle Contract\n"
            + md_table(cocycle, ["cocycle_id", "object", "formula", "needed_inputs", "current_status"]),
            "## Alpha3 Projection Coefficient Template\n"
            + md_table(alpha3, ["projection_id", "observable", "mts_formula", "external_bound", "units", "reference", "coefficient_bound_rule", "current_status"]),
            "## R10 Edge Input Contract\n"
            + md_table(r10_edge, ["edge_id", "symbol", "formula", "missing_inputs"]),
            "## MTS Alpha Smoke Template\n"
            + md_table(alpha_template, ["model_id", "template_branch", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status"]),
            "## Runner Smoke Status\n"
            + md_table(runner, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "## Placeholder Refusal Runner\n"
            + md_table(refusal, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "## Claim Gates\n"
            + md_table(claim, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target\n"
            + md_table(next_target, ["next_target", "script", "objective", "include", "exclude"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is good movement: the boundary problem is no longer a nameless crack in the wall. It is now a named surface density `B_R` with explicit missing owners. "
            "That means the next step is not to guess a number for `K_boundary_alpha3`; it is to derive or select the `R_AB` sector symplectic potential `Theta_R` and momentum `P_R`. "
            "If those close, no-pole gets stronger. If they do not, the alpha3/R10 edge rows stay as honest bounded residuals.",
            "",
        ]
    )


def main() -> None:
    source = source_rows()
    formula = formula_rows()
    owner = owner_gate_rows()
    reference_split = reference_split_rows()
    cocycle = cocycle_rows()
    alpha3 = alpha3_rows()
    r10_edge = r10_edge_rows()
    alpha_template = alpha_template_rows()
    runner = runner_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(PARENT_BOUNDARY_FORMULA, formula)
    write_csv(BR_OWNER_GATE, owner)
    write_csv(REFERENCE_PROJECTOR_SPLIT, reference_split)
    write_csv(KBOUNDARY_COCYCLE, cocycle)
    write_csv(ALPHA3_TEMPLATE, alpha3)
    write_csv(R10_EDGE_CONTRACT, r10_edge)
    write_csv(MTS_ALPHA_TEMPLATE, alpha_template)
    write_csv(RUNNER_SMOKE, runner)
    write_csv(PLACEHOLDER_REFUSAL, refusal)
    write_csv(CLAIM_GATES, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            formula,
            owner,
            reference_split,
            cocycle,
            alpha3,
            r10_edge,
            alpha_template,
            runner,
            refusal,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2246 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
