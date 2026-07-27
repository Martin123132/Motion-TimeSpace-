from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_BQ_QQ_ALPHA3_2294"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2294-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md"

PATHS = {
    "2293_doc": ROOT / "2293-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md",
    "2293_validation": OUT / "P8_Y5_BRR545_2293_VALIDATION.csv",
    "2293_next": OUT / "P8_Y5_PARENT_QLOC_2293_NEXT_TARGET.csv",
    "2293_compact": OUT / "P8_Y5_PARENT_QLOC_2293_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "2293_residual": OUT / "P8_Y5_PARENT_QLOC_2293_BOUNDARY_RESIDUAL_BETA_ROW.csv",
    "2293_projection": OUT / "P8_Y5_PARENT_QLOC_2293_FIRST_BETA_PROJECTION_TEMPLATE.csv",
    "2293_alpha3": OUT / "P8_Y5_PARENT_QLOC_2293_ALPHA3_BOUND_ANCHOR_LEDGER.csv",
    "2246_doc": ROOT / "2246-Y5-R2FR-RAB-parent-boundary-charge-formula-BR-or-alpha3-projection-bound.md",
    "2246_validation": OUT / "P8_Y5_BRR545_2246_VALIDATION.csv",
    "2246_formula": OUT / "P8_Y5_PARENT_QLOC_2246_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "2246_cocycle": OUT / "P8_Y5_PARENT_QLOC_2246_KBOUNDARY_COCYCLE_CONTRACT.csv",
    "1040_doc": ROOT / "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
    "1040_validation": OUT / "P8_Y5_BRR545_1040_VALIDATION.csv",
    "1040_formula": OUT / "P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "1040_cocycle": OUT / "P8_Y5_R10_1040_KBOUNDARY_COCYCLE_CONTRACT.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCES = [
    ("SRC2294_00_2293_doc", "q_boundary_handoff", PATHS["2293_doc"], ["B_q/Q_q", "2294-Y5-R2FR"], "2293 selected B_q/Q_q formula as the next q-branch target."),
    ("SRC2294_01_2293_validation", "prior_validation", PATHS["2293_validation"], ["VAL2293_OVERALL", "PASS"], "2293 validation passed."),
    ("SRC2294_02_2293_next", "explicit_next_target", PATHS["2293_next"], ["2294-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md", "B_q/Q_q"], "Direct handoff into parent q boundary charge formula."),
    ("SRC2294_03_2293_compact", "proper_compact_zero", PATHS["2293_compact"], ["QQK2293_2_Qq_zero", "QQK2293_3_Kboundary_zero"], "Narrow compact/proper zero inherited into formula contract."),
    ("SRC2294_04_2293_residual", "q_boundary_residuals", PATHS["2293_residual"], ["Qbar_edge_qH(lambda)", "K_boundary_alpha3_q"], "Non-proper/source boundary residuals to be written as coefficient contracts."),
    ("SRC2294_05_2293_projection", "q_projection_template", PATHS["2293_projection"], ["FBP2293_0_boundary_alpha3_q", "FBP2293_1_R10_edge_beta_q"], "Alpha3 and R10 fallback projection templates."),
    ("SRC2294_06_2293_alpha3", "alpha3_anchor", PATHS["2293_alpha3"], ["Will_2014_PPN_alpha3_table", "4e-20"], "q branch alpha3 anchor ledger."),
    ("SRC2294_07_2246_doc", "RAB_formula_precedent", PATHS["2246_doc"], ["B_R/Q_R", "alpha3"], "R2FR R_AB formula scaffold precedent."),
    ("SRC2294_08_2246_validation", "RAB_formula_validation", PATHS["2246_validation"], ["VAL2246_OVERALL", "PASS"], "2246 validation passed."),
    ("SRC2294_09_2246_formula", "RAB_formula_rows", PATHS["2246_formula"], ["BRF2246_1_candidate_charge_density", "BRF2246_2_candidate_QR"], "R_AB boundary charge formula pattern."),
    ("SRC2294_10_2246_cocycle", "RAB_cocycle_rows", PATHS["2246_cocycle"], ["KBC2246_0_contract", "KBC2246_2_source_alpha3"], "R_AB cocycle/alpha3 pattern."),
    ("SRC2294_11_1040_doc", "generic_formula_precedent", PATHS["1040_doc"], ["B_X/Q_X", "alpha3"], "Generic X formula scaffold."),
    ("SRC2294_12_1040_validation", "generic_formula_validation", PATHS["1040_validation"], ["V1040_SUMMARY", "pass"], "1040 validation passed."),
    ("SRC2294_13_1040_formula", "generic_formula_rows", PATHS["1040_formula"], ["BX1040_1_candidate_charge_density", "BX1040_2_candidate_QX"], "Generic B_X/Q_X formula pattern."),
    ("SRC2294_14_1040_cocycle", "generic_cocycle_rows", PATHS["1040_cocycle"], ["KBC1040_0_contract", "KBC1040_2_source_alpha3"], "Generic cocycle/alpha3 pattern."),
    ("SRC2294_15_local_bounds", "external_alpha3_bound", PATHS["local_bounds"], ["R7_alpha3", "4e-20"], "Local bound ledger with source-backed alpha3 anchor."),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2294_SOURCE_REGISTER.csv",
    "formula": OUT / "P8_Y5_PARENT_QLOC_2294_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "owner_gate": OUT / "P8_Y5_PARENT_QLOC_2294_BQ_OWNER_GATE.csv",
    "reference_split": OUT / "P8_Y5_PARENT_QLOC_2294_REFERENCE_PROJECTOR_SPLIT.csv",
    "cocycle": OUT / "P8_Y5_PARENT_QLOC_2294_KBOUNDARY_COCYCLE_CONTRACT.csv",
    "alpha3": OUT / "P8_Y5_PARENT_QLOC_2294_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
    "r10_edge": OUT / "P8_Y5_PARENT_QLOC_2294_R10_EDGE_CONTRACT.csv",
    "mts_template": OUT / "R10_alpha_lambda_curve_MTS_2294_BQ_QQ_ALPHA3_TEMPLATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_PARENT_QLOC_2294_RUNNER_SMOKE_STATUS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2294_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2294_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2294_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2294_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2294_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2294_VALIDATION.csv",
}

BRANCH_COPY_TARGETS = {
    "queue_formula": QUEUE / "JR2294_BQ_QQ_FORMULA_CONTRACT_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2294_ALPHA3_COEFFICIENT_RULE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "parent_Bq_Qq_alpha3_nonclaim_2294.csv",
    "beta_docs": BETA_DOCS / "BQ_QQ_ALPHA3_2294_NONCLAIM.csv",
}


def ensure_dirs() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def contains_all(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def local_alpha3() -> dict[str, str]:
    for row in read_csv(PATHS["local_bounds"]):
        if row.get("row_id") == "R7_alpha3" or row.get("observable") == "alpha3":
            return row
    return {}


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "exists": path.exists(),
            "needles_present": contains_all(path, needles),
            "needles": ";".join(needles),
            "notes": notes,
            "valid_for_claim": False,
        }
        for source_id, role, path, needles, notes in SOURCES
    ]


def formula_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BQF2294_0_bulk_pairing",
            "boundary pairing from D C_q",
            "delta int_Sigma epsilon_q C_q contains - int_partialSigma epsilon_q n_mu delta P_q^mu dS plus counterterm/reference/exact variations",
            "PAIRING_SHAPE_FROM_INTEGRATION_BY_PARTS",
            "parent C_q and P_q must still be derived from Theta_q",
            "identifies the only allowed surface-density slot for q edge charge",
        ),
        (
            "BQF2294_1_candidate_charge_density",
            "B_q surface density",
            "B_q = sigma n_mu P_q^mu + B_ct_q + B_ref_q + B_exact_q, with sigma fixed by the G_bulk +/- Q convention",
            "FORMULA_SHAPE_DERIVED_SIGN_CONVENTION_OPEN",
            "P_q, counterterm, reference subtraction, exact primitive, and density convention missing",
            "turns q edge charge into a concrete coefficient contract rather than a vague coupling",
        ),
        (
            "BQF2294_2_candidate_Qq",
            "Q_q boundary charge",
            "Q_q[epsilon]=int_partialSigma epsilon_q B_q dS",
            "CONTRACT_READY_NOT_PARENT_SIGNED",
            "requires Theta_q/L_q sector owner and allowed q boundary class",
            "proper compact branch gives zero; source/large branch remains scoreable residual",
        ),
        (
            "BQF2294_3_exactness_route",
            "exact/pure boundary repair",
            "B_q=d_boundary b_q+B_q^pure and int_partialSigma epsilon_q d_boundary b_q=int_partialpartialSigma epsilon_q b_q-int_partialSigma d_boundary epsilon_q b_q",
            "MATHEMATICAL_ROUTE_ONLY",
            "b_q, harmonic sector, corner terms, and range-kernel derivative term not derived",
            "exactness can close only with boundary-class and range-kernel conditions",
        ),
        (
            "BQF2294_4_verdict",
            "parent B_q/Q_q formula status",
            "B_q/Q_q formula shape is explicit, but parent ownership is not closed",
            "FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED",
            "MISSING_PARENT_LQ_THETAQ_PQ_REFERENCE_PROJECTOR",
            "move to parent q-sector Theta_q/P_q owner or alpha3/R10 nonclaim coefficient rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "formula_id": row[0],
            "object": row[1],
            "formula": row[2],
            "status": row[3],
            "missing_inputs": row[4],
            "claim_effect": row[5],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("BQG2294_0_Lq_owner", "parent q-sector Lagrangian block L_q", "L_q or parent constraint C_q must be selected from the parent action, not reverse-engineered from a bound", "MISSING_LQ_OR_CQ_OWNER", "B_q/Q_q cannot be parent-derived"),
        ("BQG2294_1_Thetaq_owner", "parent symplectic potential Theta_q", "delta L_q=E_q delta q + d Theta_q(delta q) with finite boundary jet order", "MISSING_THETA_Q", "Q_q differentiability and K_boundary bracket cannot be computed"),
        ("BQG2294_2_Pq_owner", "boundary momentum P_q^mu", "P_q is derived from L_q/Theta_q or parent variation, not inserted as a free vector density", "MISSING_PQ_OWNER", "B_q=n.P_q is a contract only"),
        ("BQG2294_3_density_convention", "tensor versus densitized P_q convention", "choose C_q=-nabla_mu P_q^mu+J_q or C_q=-(1/sqrt(g))partial_mu Ptilde_q^mu+J_q before scoring signs/units", "CONVENTION_GATE_OPEN", "B_q sign, volume terms, and units are ambiguous"),
        ("BQG2294_4_boundary_class", "allowed q boundary class", "proper compact, source/worldtube, reference, and range-kernel boundary classes must be separated", "BOUNDARY_CLASS_SPLIT_OPEN", "compact zero cannot be promoted to source/test silence"),
        ("BQG2294_5_verdict", "claim-grade B_q owner package", "BQG2294_0 through BQG2294_4 pass together", "FAIL_CURRENT_CLAIM_BQ_NOT_PARENT_OWNED", "keep B_q/Q_q rows as nonclaim coefficient contracts"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "needed_object": row[1],
            "acceptance_test": row[2],
            "current_status": row[3],
            "if_missing": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def reference_split_rows() -> list[dict[str, Any]]:
    rows = [
        ("RPS2294_0_GR_charge_guard", "observed GR Hamiltonian/reference charges", "ADM/Newtonian mass and observed Hamiltonian generators remain in metric/coframe sector, not in representative q-gauge charge", "boundary generator split and reference subtraction", "GUARD_RETAINED"),
        ("RPS2294_1_representative_q_charge", "proper compact representative-q charge", "Q_q^proper=0 from 2293 collar lemma", "extension to non-proper/source boundary values", "NARROW_ZERO_ONLY"),
        ("RPS2294_2_edge_source_projection", "edge/source residual charge", "Qbar_edge_qH(lambda)=Pi_M^H[int_partialSigma F_lambda epsilon_q B_q dS]/M_H", "Pi_M^H, F_lambda, B_q owner, source boundary class, units", "RETAIN_NONCLAIM_RESIDUAL"),
        ("RPS2294_3_no_double_count", "bulk/edge source split", "Q_q_total=Q_q_bulk+Q_q_edge with orthogonal support or absolute-tail summation", "support split and no-cancellation policy", "CLAIM_BLOCKED_UNTIL_SPLIT_OWNED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "split_id": row[0],
            "object": row[1],
            "rule": row[2],
            "missing": row[3],
            "status": row[4],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def cocycle_rows() -> list[dict[str, Any]]:
    rows = [
        ("KBC2294_0_contract", "boundary cocycle", "K_boundary[epsilon,eta]=delta_eta Q_q[epsilon]-delta_epsilon Q_q[eta]-Q_q[[epsilon,eta]] plus possible i_veta i_vepsilon Omega_boundary convention terms", "differentiable G_q, parent Omega_Y, v_q action on all fields, sign convention", "FORMULA_CONTRACT_ONLY"),
        ("KBC2294_1_proper_zero", "proper compact cocycle", "K_boundary=0 when epsilon_q, eta_q, and required finite jets vanish on the boundary collar", "same finite-jet boundary class as 2293", "NARROW_ZERO_INHERITED"),
        ("KBC2294_2_source_alpha3", "preferred-frame flux projection", "alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q", "K_boundary_alpha3_q, Phi_boundary_local_q, projection normalization", "SOURCE_ANCHOR_READY_COEFFICIENTS_MISSING"),
        ("KBC2294_3_R10_edge", "short-range edge exchange projection", "alpha_q_edge(lambda) uses Qbar_edge_qH(lambda) qbar_qT(lambda) with absolute tails", "B_q, F_lambda, source/test support, K_q^R10(lambda), bound curve", "R10_EDGE_CONTRACT_ONLY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "cocycle_id": row[0],
            "object": row[1],
            "formula": row[2],
            "needed_inputs": row[3],
            "current_status": row[4],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def alpha3_rows() -> list[dict[str, Any]]:
    alpha3 = local_alpha3()
    bound = alpha3.get("upper_bound", "4e-20")
    reference = alpha3.get("reference_path_or_url", "source-intake/local_bounds/local_bound_claims.csv:R7_alpha3")
    rows = [
        ("A3P2294_0_formula", "alpha3", "alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q", bound, "dimensionless", reference, "if Phi_boundary_local_q is numeric and nonzero, |K_boundary_alpha3_q| <= 4e-20/|Phi_boundary_local_q|", "COEFFICIENT_RULE_WRITTEN_PHI_AND_K_MISSING"),
        ("A3P2294_1_theorem_zero_route", "alpha3", "alpha3_MTS_q=0 if K_boundary_alpha3_q=0 or Phi_boundary_local_q=0 from a parent theorem", bound, "dimensionless", reference, "theorem-zero must cite B_q exactness/no-flux or boundary flux amplitude zero", "THEOREM_ZERO_NOT_SIGNED"),
        ("A3P2294_2_numeric_route", "alpha3", "|K_boundary_alpha3_q*Phi_boundary_local_q| <= 4e-20", bound, "dimensionless", reference, "requires source-backed K, Phi, normalization, uncertainty policy, and no-cancellation tail addition", "NUMERIC_ROUTE_INPUTS_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": row[0],
            "observable": row[1],
            "mts_formula": row[2],
            "external_bound": row[3],
            "units": row[4],
            "reference": row[5],
            "coefficient_bound_rule": row[6],
            "current_status": row[7],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def r10_edge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "edge_id": "R10E2294_0_Qbar_edge_qH",
            "quantity": "Qbar_edge_qH(lambda)",
            "formula": "Pi_M^H[int_partialSigma F_lambda(s) epsilon_q B_q(s) dS]/M_H",
            "missing_inputs": "B_q owner; F_lambda; Pi_M^H; source boundary class; units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "edge_id": "R10E2294_1_alpha_edge_bound",
            "quantity": "alpha_q_edge(lambda)",
            "formula": "|alpha_q_edge(lambda)| <= |K_q^R10(lambda)| |Qbar_edge_qH(lambda) qbar_qT(lambda)| + abs_tail_q(lambda)",
            "missing_inputs": "K_q^R10(lambda); qbar_qT; alpha_bound(lambda); absolute tail rows; valid units",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def mts_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "MTS_source_normalized_Newton_branch",
            "branch_id": "BQ_QQ_formula_contract",
            "lambda_value": "MISSING_SOURCE_BOUNDARY_CLASS",
            "alpha_predicted": "MISSING_BQ_OWNER_AND_EDGE_PROJECTION",
            "force_law_form": "Q_q[epsilon]=int_partialSigma epsilon_q(sigma n_mu P_q^mu+B_ct_q+B_ref_q+B_exact_q)dS",
            "derivation_status": "template_invalid_formula_shape_not_parent_owned",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "model": "MTS_source_normalized_Newton_branch",
            "branch_id": "boundary_alpha3_q_projection_bound_rule",
            "lambda_value": "MISSING_NOT_R10_RANGE",
            "alpha_predicted": "MISSING_K_BOUNDARY_ALPHA3_Q_TIMES_PHI_BOUNDARY_LOCAL_Q",
            "force_law_form": "alpha3_MTS_q=K_boundary_alpha3_q Phi_boundary_local_q; |K|<=4e-20/|Phi| if Phi is sourced nonzero",
            "derivation_status": "template_invalid_alpha3_coefficients_missing",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "model": "MTS_source_normalized_Newton_branch",
            "branch_id": "R10_edge_q_beta_contract",
            "lambda_value": "MISSING_PARENT_LAMBDA_Q",
            "alpha_predicted": "MISSING_KQ_QBAR_EDGE_QH_QBAR_QT_TAILS",
            "force_law_form": "|alpha_q_edge(lambda)| <= |K_q^R10(lambda)| |Qbar_edge_qH qbar_qT| + abs_tail",
            "derivation_status": "template_invalid_R10_edge_inputs_missing",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "SMOKE2294_0_runner_status",
            "input_rows": 3,
            "claim_valid_rows": 0,
            "numeric_score_rows": 0,
            "runner_would_claim": False,
            "runner_would_score": False,
            "status": "blocked_nonclaim",
            "valid_for_claim": False,
        }
    ]


def refusal_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        for row in group:
            object_name = row.get("object") or row.get("needed_object") or row.get("quantity") or row.get("observable") or row.get("branch_id")
            status = row.get("status") or row.get("current_status") or row.get("derivation_status") or row.get("missing_inputs") or "NONCLAIM"
            reason = row.get("missing_inputs") or row.get("needed_inputs") or row.get("missing") or row.get("if_missing") or row.get("coefficient_bound_rule") or status
            row_id = row.get("formula_id") or row.get("gate_id") or row.get("split_id") or row.get("cocycle_id") or row.get("projection_id") or row.get("edge_id") or row.get("branch_id")
            rows.append(
                {
                    "branch_id": BRANCH_ID,
                    "refusal_id": f"REF2294_{row_id}",
                    "object": object_name,
                    "status": status,
                    "refusal_status": "not_claim_promoted",
                    "reason": f"{reason};SCORE_READY_FALSE;VALID_FOR_CLAIM_FALSE",
                    "score_ready": False,
                    "valid_for_claim": False,
                }
            )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CGATE2294_0_Bq_formula", "B_q/Q_q is parent-derived", False, "formula shape is explicit, but L_q, Theta_q, P_q, density convention, reference terms, and boundary class are not parent-owned"),
        ("CGATE2294_1_full_local_GR", "full q no-pole/local-GR branch is closed", False, "B_q/Q_q is only one clause; Omega/DCq, degree count, and matter/no-marker descent remain open"),
        ("CGATE2294_2_alpha3", "q alpha3 projection row is executable", False, "source-backed alpha3 bound exists but K_boundary_alpha3_q and Phi_boundary_local_q are missing"),
        ("CGATE2294_3_R10_edge", "R10 q edge row is executable", False, "B_q owner, F_lambda, source/test supports, K_q^R10(lambda), and valid bound curve are missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "reason": row[3],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2294_0_formula_status", "B_q/Q_q is now a concrete formula contract, not a vague missing coupling.", "D C_q boundary pairing fixes the required surface density up to sign/density/reference conventions", "select or derive the parent L_q/Theta_q/P_q package, or retain the formula as a nonclaim coefficient contract"),
        ("DEC2294_1_alpha3_status", "alpha3 has a usable q-boundary coefficient rule but no MTS coefficient yet.", "|K_boundary_alpha3_q Phi_boundary_local_q| <= 4e-20 is the exact scoring inequality once K and Phi exist", "derive theorem-zero for K/Phi or source numeric values with normalization"),
        ("DEC2294_2_R10_status", "R10 edge exchange is a source-test product with absolute tails.", "finite q exchange cannot be scored as a naked linear coupling", "derive B_q, F_lambda, source/test support, K_q^R10(lambda), and alpha_bound(lambda) before scoring"),
        ("DEC2294_3_next_target", "Next target should try to source the parent q-sector symplectic potential.", "Theta_q is the upstream object that would fix P_q, B_q, differentiability, K_boundary, and the alpha3 projection coefficient", "2295-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "2295-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md",
            "script": "scripts/Y5_R2FR_parent_q_sector_Thetaq_Pq_owner_or_boundary_coefficient_prior_2295.py",
            "objective": "try to derive or select the parent q-sector symplectic potential Theta_q and momentum P_q that own B_q; if this cannot close, create nonclaim priors/templates for K_boundary_alpha3_q, Phi_boundary_local_q, and Qbar_edge_qH",
            "include": "candidate L_q blocks, delta L_q, Theta_q, P_q tensor/density convention, boundary finite-jet order, no-flux theorem-zero route, alpha3 coefficient prior schema, R10 edge beta coefficient schema",
            "exclude": "invented numeric K/Phi/Qbar values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
        }
    ]


def copy_branch_files() -> list[dict[str, Any]]:
    copy_plan = {
        "queue_formula": OUTPUTS["formula"],
        "queue_alpha3": OUTPUTS["alpha3"],
        "branch_wep": OUTPUTS["alpha3"],
        "beta_docs": OUTPUTS["r10_edge"],
    }
    rows = []
    for copy_id, source in copy_plan.items():
        dest = BRANCH_COPY_TARGETS[copy_id]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source": str(source),
                "destination": str(dest),
                "source_exists": source.exists(),
                "destination_exists": dest.exists(),
                "notes": "branch/quarantine copy for 2294 B_q/Q_q formula contract",
            }
        )
    return rows


def parse_csvs(paths: list[Path]) -> bool:
    for path in paths:
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def claim_flags_false(paths: list[Path]) -> bool:
    fields = {"valid_for_claim", "score_ready", "claim_allowed", "runner_would_claim", "runner_would_score"}
    for path in paths:
        for row in read_csv(path):
            for field in fields.intersection(row.keys()):
                if str(row[field]).strip().lower() not in {"false", "0", "no"}:
                    return False
    return True


def formalization_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    return sum(1 for path in FORMALIZATION.rglob("*2294*") if not any(part in ignored for part in path.parts))


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    for path in FORMALIZATION.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        try:
            if path.stat().st_mtime >= START_TS:
                return True
        except OSError:
            continue
    return False


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(branch_copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = list(OUTPUTS.values()) + [Path(row["destination"]) for row in branch_copies]
    generated_without_validation = [path for path in generated if path != OUTPUTS["validation"]]
    checks = [
        ("VAL2294_00_sources_exist", all(row["exists"] for row in source_rows()), "all direct and registered 2294 source paths exist"),
        ("VAL2294_01_needles_present", all(row["needles_present"] for row in source_rows()), "all cited source needles are present"),
        ("VAL2294_02_prior_validations", contains_all(PATHS["2293_validation"], ["VAL2293_OVERALL", "PASS"]) and contains_all(PATHS["2246_validation"], ["VAL2246_OVERALL", "PASS"]) and contains_all(PATHS["1040_validation"], ["V1040_SUMMARY", "pass"]), "2293, 2246, and 1040 validations pass overall"),
        ("VAL2294_03_Bq_formula_contract", any(row["formula_id"] == "BQF2294_1_candidate_charge_density" and "B_q" in row["formula"] for row in read_csv(OUTPUTS["formula"])), "B_q/Q_q formula contract is written but not parent-promoted"),
        ("VAL2294_04_owner_gates_fail_safely", any(row["gate_id"] == "BQG2294_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_BQ_NOT_PARENT_OWNED" for row in read_csv(OUTPUTS["owner_gate"])), "owner gates identify missing L_q/Theta_q/P_q package"),
        ("VAL2294_05_reference_projector_guard", any(row["split_id"] == "RPS2294_0_GR_charge_guard" for row in read_csv(OUTPUTS["reference_split"])) and any(row["split_id"] == "RPS2294_2_edge_source_projection" for row in read_csv(OUTPUTS["reference_split"])), "reference/projector split protects GR charges and keeps edge residual"),
        ("VAL2294_06_cocycle_contract", any(row["cocycle_id"] == "KBC2294_0_contract" and "delta_eta Q_q" in row["formula"] for row in read_csv(OUTPUTS["cocycle"])) and any(row["cocycle_id"] == "KBC2294_2_source_alpha3" for row in read_csv(OUTPUTS["cocycle"])), "K_boundary cocycle and alpha3 projection contracts are present"),
        ("VAL2294_07_alpha3_bound_rule", any(row["observable"] == "alpha3" and row["external_bound"] == "4e-20" and row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["alpha3"])), "alpha3 coefficient bound rule uses source-backed anchor but remains nonclaim"),
        ("VAL2294_08_R10_edge_contract_nonclaim", any(row["edge_id"] == "R10E2294_1_alpha_edge_bound" and row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["r10_edge"])), "R10 edge contract remains nonclaim and non-scoreable"),
        ("VAL2294_09_mts_template_nonclaim", all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["mts_template"])), "MTS smoke template has runner schema and no claim-valid rows"),
        ("VAL2294_10_runner_smoke_refuses_claim", read_csv(OUTPUTS["runner"])[0]["runner_would_claim"].lower() == "false", "runner smoke status refuses claim"),
        ("VAL2294_11_claim_gates_blocked", all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["claim_gates"])), "all empirical/local-GR claim gates remain blocked"),
        ("VAL2294_12_next_target_written", read_csv(OUTPUTS["next_target"])[0]["next_target"].startswith("2295-Y5-R2FR-parent-q-sector-Thetaq-Pq"), "next target row is present"),
        ("VAL2294_13_csv_parse", parse_csvs(generated_without_validation), "all generated 2294 CSVs parse cleanly"),
        ("VAL2294_14_claim_flags_false", claim_flags_false(generated_without_validation), "all generated prediction/claim flags remain false"),
        ("VAL2294_15_branch_copies", len(branch_copies) == len(BRANCH_COPY_TARGETS) and parse_csvs([Path(row["destination"]) for row in branch_copies]), "branch/quarantine nonclaim copies exist and parse"),
        ("VAL2294_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2294_17_formalization_no_2294", formalization_count() == 0, "formalization-workbench has no non-venv 2294 artifacts"),
        ("VAL2294_18_formalization_untouched", not formalization_touched(), "formalization-workbench untouched during 2294 run"),
    ]
    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2294_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2294 builds the q B_q/Q_q boundary-charge formula contract, blocks parent ownership claims, writes alpha3/R10 edge nonclaim bounds, and selects Theta_q/P_q ownership next",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def build_doc(
    sources: list[dict[str, Any]],
    formulas: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    references: list[dict[str, Any]],
    cocycles: list[dict[str, Any]],
    alpha3: list[dict[str, Any]],
    r10: list[dict[str, Any]],
    mts: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    source_rows_md = [{**row, "path": rel(Path(row["path"]))} for row in sources]
    copy_rows_md = [{**row, "source": rel(Path(row["source"])), "destination": rel(Path(row["destination"]))} for row in copies]
    return "\n\n".join(
        [
            "# 2294 - Y5/R2FR Parent Boundary Charge Formula B_q or Alpha3 Projection Bound",
            "## Verdict\n"
            "- 2294 turns the q boundary leak into an explicit formula contract: `Q_q[epsilon]=int_partialSigma epsilon_q B_q dS`.\n"
            "- The candidate density is `B_q=sigma n_mu P_q^mu+B_ct_q+B_ref_q+B_exact_q`, but this is not parent-owned until `L_q`, `Theta_q`, and `P_q` are derived or selected.\n"
            "- The alpha3 fallback is now an exact inequality: `|K_boundary_alpha3_q Phi_boundary_local_q| <= 4e-20`, still nonclaim because both MTS coefficients are missing.",
            "## Source Register\n" + md_table(source_rows_md, ["source_id", "role", "path", "exists", "needles_present", "notes", "valid_for_claim"]),
            "## Parent Boundary Charge Formula\n" + md_table(formulas, ["formula_id", "object", "formula", "status", "missing_inputs", "claim_effect", "score_ready", "valid_for_claim"]),
            "## B_q Owner Gate\n" + md_table(owners, ["gate_id", "needed_object", "acceptance_test", "current_status", "if_missing", "claim_allowed", "valid_for_claim"]),
            "## Reference/Projector Split\n" + md_table(references, ["split_id", "object", "rule", "missing", "status", "score_ready", "valid_for_claim"]),
            "## K_boundary Cocycle Contract\n" + md_table(cocycles, ["cocycle_id", "object", "formula", "needed_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "## Alpha3 Projection Coefficient Rule\n" + md_table(alpha3, ["projection_id", "observable", "mts_formula", "external_bound", "reference", "coefficient_bound_rule", "current_status", "score_ready", "valid_for_claim"]),
            "## R10 Edge Contract\n" + md_table(r10, ["edge_id", "quantity", "formula", "missing_inputs", "score_ready", "valid_for_claim"]),
            "## MTS Smoke Template\n" + md_table(mts, ["model", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "score_ready", "valid_for_claim"]),
            "## Runner Smoke Status\n" + md_table(runner, ["runner_id", "input_rows", "claim_valid_rows", "numeric_score_rows", "runner_would_claim", "runner_would_score", "status", "valid_for_claim"]),
            "## Placeholder Refusal Runner\n" + md_table(refusals, ["refusal_id", "object", "status", "refusal_status", "reason", "score_ready", "valid_for_claim"]),
            "## Claim Gates\n" + md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target\n" + md_table(next_target, ["next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
            "## Branch Copies\n" + md_table(copy_rows_md, ["copy_id", "source", "destination", "source_exists", "destination_exists", "notes"]),
            "## Validation\n" + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "This is useful because the coupling problem is no longer foggy. A q edge leak must enter through a named surface density `B_q`, and `B_q` must be owned by `Theta_q/P_q` before it can be claimed. That means the next derivation should go upstream to the q-sector symplectic potential rather than guessing `K_boundary_alpha3_q` or pretending the compact boundary lemma covers physical sources.",
        ]
    ) + "\n"


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    formulas = formula_rows()
    owners = owner_gate_rows()
    references = reference_split_rows()
    cocycles = cocycle_rows()
    alpha3 = alpha3_rows()
    r10 = r10_edge_rows()
    mts = mts_template_rows()
    runner = runner_rows()
    refusals = refusal_rows(formulas, owners, references, cocycles, alpha3, r10, mts)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["formula"], formulas)
    write_csv(OUTPUTS["owner_gate"], owners)
    write_csv(OUTPUTS["reference_split"], references)
    write_csv(OUTPUTS["cocycle"], cocycles)
    write_csv(OUTPUTS["alpha3"], alpha3)
    write_csv(OUTPUTS["r10_edge"], r10)
    write_csv(OUTPUTS["mts_template"], mts)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    validation = validation_rows(copies)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(sources, formulas, owners, references, cocycles, alpha3, r10, mts, runner, refusals, gates, decisions, next_target, copies, validation),
        encoding="utf-8",
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit("2294 validation failed: " + ", ".join(row["check_id"] for row in failed))
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
