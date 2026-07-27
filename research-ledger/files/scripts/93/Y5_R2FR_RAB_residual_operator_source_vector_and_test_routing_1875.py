from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1875"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1875-Y5-R2FR-RAB-residual-operator-source-vector-and-test-routing.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1875_SOURCE_REGISTER.csv",
    "residual_vector": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv",
    "test_routing": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_TEST_ROUTING_MATRIX.csv",
    "runner_contract": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RUNNER_BLOCKER_CONTRACT.csv",
    "acquisition_queue": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_COEFFICIENT_ACQUISITION_QUEUE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1875_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1875_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1875_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1875_VALIDATION.csv",
}

SOURCE_NEEDLES = {
    "1874_doc": {
        "path": ROOT / "1874-Y5-R2FR-parent-domain-verticality-for-RAB-or-explicit-residual-field.md",
        "needles": [
            "PARENT_DOMAIN_VERTICALITY_NOT_DERIVED",
            "RAB_CLASSIFIED_AS_EXPLICIT_RESIDUAL_FIELD_CURRENTLY",
            "RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR_SELECTED_NEXT",
        ],
    },
    "1874_requirements": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1874_RAB_RESIDUAL_BOUND_REQUIREMENTS.csv",
        "needles": [
            "MISSING_VERTICALITY_CERTIFICATE_OR_BOUND",
            "MISSING_OPERATOR_SIGNATURE",
            "MISSING_NO_CANCELLATION_GUARD",
        ],
    },
    "1874_classification": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1874_RAB_EXPLICIT_RESIDUAL_FIELD_CLASSIFICATION.csv",
        "needles": [
            "EXPLICIT_RESIDUAL_FIELD_UNTIL_PARENT_VERTICALITY_OR_CONSTRAINT_SIGNED",
            "MASSLESS_PPN_ORBITAL_RESIDUAL",
            "FINITE_RESIDUAL_FIELD_IF_ZR_MR2_PARENT_SIGNED",
        ],
    },
    "1869_component_schema": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv",
        "needles": [
            "FLC1869_1_ZR",
            "MISSING_PARENT_OPERATOR_ZR",
            "FLC1869_8_tau_R10",
        ],
    },
    "1870_first_fill": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1870_FIRST_FILL_ROWS_NONCLAIM.csv",
        "needles": [
            "FF1870_0_QR",
            "MISSING_RANGE_RELATION",
            "MISSING_ABSOLUTE_TAIL_ENVELOPE",
        ],
    },
    "1871_denominator": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1871_SOURCE_DENOMINATOR_ROW_NONCLAIM.csv",
        "needles": [
            "q_R = C_R c^2/(2 G M_*)",
            "SYMBOLIC_CONVENTION_LOCK_READY_NONCLAIM",
            "no-cancellation residual budget",
        ],
    },
    "1872_bound_rows": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1872_CR_PIR_DELTAGAMMA_BOUND_ROWS_NONCLAIM.csv",
        "needles": [
            "|C_R| <= (2 G M_*/c^2) 6.7e-05",
            "MISSING_C_R_VALUE_OR_ZERO_THEOREM",
            "MISSING_NO_CANCELLATION_GUARD",
        ],
    },
    "1691_ppn_vector": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1691_PPN_RESIDUAL_VECTOR.csv",
        "needles": [
            "gamma_minus_1=q_R_hat+delta_gauge+delta_source+delta_boundary+delta_readout+O(U_N)",
            "FORMAL_NONCLAIM_VECTOR_READY",
            "all tails must be theorem-zero or source-bounded absolutely",
        ],
    },
    "1751_finite_vector": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1751_FINITE_RESIDUAL_VECTOR.csv",
        "needles": [
            "RESIDUAL_VECTOR_ACTIVE_NONCLAIM",
            "MISSING_OPERATOR_PROJECTION_NORMS",
            "no cancellation",
        ],
    },
    "1852_cassini_bound": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1852_PPN_OBSERVABLE_BOUND.csv",
        "needles": [
            "PPN1852_0_cassini_gamma",
            "6.7e-05",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        ],
    },
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, payload in SOURCE_NEEDLES.items():
        path = payload["path"]
        ok, detail = path_has_needles(path, payload["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(payload["needles"]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1875": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_0_domain_visibility",
            "coefficient": "Dq[v_R] or Lie_{v_R} e_obs",
            "sector": "parent_domain_geometry",
            "residual_expression": "observer-cell response of R_AB=ln(T^2 S)=2 ln(J_q)",
            "zero_theorem_needed": "parent q_shape with Dq[v_R]=0, or parent constraint/no-pole eliminates R_AB",
            "numeric_bound_needed": "coframe/metric response bound in PPN-compatible units",
            "test_arenas": "PPN;clock;WEP;orbital;local_GR",
            "current_status": "MISSING_VERTICALITY_CERTIFICATE_OR_BOUND",
            "score_effect": "blocks verticality, matter-descent import, and local-GR reduction",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1874_RAB_RESIDUAL_BOUND_REQUIREMENTS.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_1_constraint_owner",
            "coefficient": "lambda_R/current-chain/first-class no-pole owner",
            "sector": "constraint_no_pole",
            "residual_expression": "parent-origin constraint lambda_R R_AB or Hessian degeneracy",
            "zero_theorem_needed": "lambda_R/no-pole owner derived from parent action/current chain",
            "numeric_bound_needed": "not numeric first; either theorem-zero/no-pole or finite operator route",
            "test_arenas": "local_GR;PPN;R10;clock;orbital",
            "current_status": "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "score_effect": "decides derived local-GR route versus finite residual field",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1576_RAB_FINITE_FALLBACK_COMPONENT_ROWS.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_2_operator_ZR",
            "coefficient": "Z_R",
            "sector": "finite_operator",
            "residual_expression": "gradient stiffness/action normalization for retained R_AB mode",
            "zero_theorem_needed": "no-pole theorem or absent mode",
            "numeric_bound_needed": "same-frame parent Hessian/operator extraction with units",
            "test_arenas": "R10;clock;orbital;PPN;local_GR",
            "current_status": "MISSING_PARENT_OPERATOR_ZR",
            "score_effect": "blocks finite alpha(lambda), clock/orbital range and no-pole decision",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_3_operator_MR2_lambda",
            "coefficient": "M_R^2 and lambda_range",
            "sector": "finite_operator",
            "residual_expression": "mass gap and range lambda_range=sqrt(Z_R/M_R^2) after same-normalization",
            "zero_theorem_needed": "no-pole/constraint removes finite mode",
            "numeric_bound_needed": "same-normalized M_R^2 plus derived lambda_range",
            "test_arenas": "R10;clock;orbital",
            "current_status": "MISSING_PARENT_OPERATOR_MR2_OR_RANGE_RELATION",
            "score_effect": "blocks R10 finite-range routing",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1870_FIRST_FILL_ROWS_NONCLAIM.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_4_bulk_source_charges",
            "coefficient": "J_R, beta_source_R, beta_test_R",
            "sector": "bulk_source_test",
            "residual_expression": "matter/source current and source/test reciprocal charges in R_AB normalization",
            "zero_theorem_needed": "parent matter descent/no-marker/source-owner theorem",
            "numeric_bound_needed": "source-backed material charge rows with units and support kernels",
            "test_arenas": "R10;WEP;clock;PPN;orbital;local_GR",
            "current_status": "MISSING_SOURCE_CHARGE_RESOLUTION",
            "score_effect": "blocks source amplitude in all finite and local branches",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1576_RAB_FINITE_FALLBACK_COMPONENT_ROWS.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_5_massless_tail",
            "coefficient": "C_R, Q_cur, Pi_R, kappa_W, M_*",
            "sector": "massless_tail_ppn_orbital",
            "residual_expression": "q_R=C_R c^2/(2GM_*)=-Q_cur c^2/(2 kappa_W G M_*)",
            "zero_theorem_needed": "C_R=0/Pi_R=0 parent theorem",
            "numeric_bound_needed": "absolute C_R or Pi_R bound plus kappa_W and same-frame M_*",
            "test_arenas": "PPN;orbital;local_GR",
            "current_status": "MISSING_C_R_PIR_KAPPA_MSTAR_OR_ZERO_THEOREM",
            "score_effect": "blocks Cassini/light-time/orbital massless-tail score",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1871_SOURCE_DENOMINATOR_ROW_NONCLAIM.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_6_boundary_readout_tail",
            "coefficient": "B_R, Pi_R boundary, epsilon_tail_R",
            "sector": "boundary_readout_hidden_tail",
            "residual_expression": "worldtube/corner/readout/domain tail with no cancellation against bulk",
            "zero_theorem_needed": "proper/exact boundary silence and hidden-tail no-reentry theorem",
            "numeric_bound_needed": "absolute boundary/readout tail envelope with units",
            "test_arenas": "PPN;R10;clock;orbital;local_GR",
            "current_status": "MISSING_BOUNDARY_RESOLUTION_OR_ABSOLUTE_TAIL_ENVELOPE",
            "score_effect": "blocks tail zero, local-GR and no-cancellation gates",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1870_FIRST_FILL_ROWS_NONCLAIM.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_7_constants_markers",
            "coefficient": "Lie_{v_R} theta_A, f_R(R_AB), m_A(R_AB), alpha(R_AB), w_A(R_AB)",
            "sector": "constants_markers_source_weights",
            "residual_expression": "visible constants/material markers/source-only weights coupled to R_AB",
            "zero_theorem_needed": "constant superselection/no-Hom/no-marker/source-label forgetting theorem",
            "numeric_bound_needed": "finite coefficient table for all retained constants/source weights",
            "test_arenas": "clock;WEP;R10;PPN;EM;local_GR",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_COEFFICIENTS",
            "score_effect": "blocks matter blindness and unified local residual closure",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1575_RAB_FINITE_COMPONENT_BOUND_INTERFACE.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_8_projection_kernels",
            "coefficient": "tau_PPN, tau_R10, tau_clock, tau_orbital, tau_WEP",
            "sector": "observable_projection",
            "residual_expression": "arena-specific projection kernels from R_AB residual to measured observables",
            "zero_theorem_needed": "common projection theorem or arena silence",
            "numeric_bound_needed": "source-backed projection kernels and accepted bound curves",
            "test_arenas": "PPN;R10;clock;WEP;orbital",
            "current_status": "MISSING_PROJECTION_KERNELS_OR_ACCEPTED_BOUND_CURVES",
            "score_effect": "blocks all quantitative scoring even if coefficients exist",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_9_no_cancellation",
            "coefficient": "absolute_local_residual_vector",
            "sector": "claim_safety",
            "residual_expression": "sum of gauge/source/readout/projective/boundary/C_R/operator residuals with no cancellation credit",
            "zero_theorem_needed": "every component independently zero or parent identity proving cancellation",
            "numeric_bound_needed": "absolute component bounds in common observable units",
            "test_arenas": "all_local_arenas",
            "current_status": "MISSING_NO_CANCELLATION_GUARD",
            "score_effect": "blocks claim promotion even if one arena appears numerically safe",
            "source_artifact": str(OUT / "P8_Y5_PARENT_QLOC_1872_LOCAL_RESIDUAL_VECTOR_INSERT.csv"),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "vector_id": "RV1875_10_total_gate",
            "coefficient": "R_AB residual vector total",
            "sector": "gate",
            "residual_expression": "R_RAB_total = sum_abs(RV1875_0..RV1875_9)",
            "zero_theorem_needed": "all components theorem-zero in compatible parent action",
            "numeric_bound_needed": "all retained components numeric/source-backed with route-specific bounds",
            "test_arenas": "all_local_arenas",
            "current_status": "RESIDUAL_VECTOR_READY_NONCLAIM_ALL_SCORES_BLOCKED",
            "score_effect": "future runners may consume this vector but must return claim_allowed=false until rows are filled",
            "source_artifact": "1875 synthesis",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def test_routing_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "TR1875_0_local_GR",
            "arena": "local_GR/Newton_limit",
            "allowed_input": "parent-signed constraint/no-pole or all residual vector components theorem-zero",
            "forbidden_input": "closure-only R_AB=0 or verticality by assertion",
            "blocking_rows": "RV1875_0;RV1875_1;RV1875_5;RV1875_6;RV1875_9",
            "current_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "TR1875_1_PPN_orbital_massless",
            "arena": "PPN/orbital/light-time",
            "allowed_input": "C_R/Pi_R massless-tail row plus M_*, kappa_W if needed, tau_PPN/tau_orbital, and no-cancellation",
            "forbidden_input": "finite R10 alpha(lambda) machinery or cancellation against unrelated residuals",
            "blocking_rows": "RV1875_5;RV1875_6;RV1875_8;RV1875_9",
            "current_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "TR1875_2_R10_finite_range",
            "arena": "R10 alpha(lambda)",
            "allowed_input": "Z_R, M_R^2, lambda_range, beta_source_R, beta_test_R, tau_R10, accepted bound curve",
            "forbidden_input": "massless C_R/r tail routed into alpha(lambda)",
            "blocking_rows": "RV1875_2;RV1875_3;RV1875_4;RV1875_8;RV1875_9",
            "current_status": "BLOCKED_NONCLAIM_MASSLESS_ROUTE_FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "TR1875_3_clock_WEP",
            "arena": "clock/WEP/material",
            "allowed_input": "material constants/markers, beta charges, tau_clock/tau_WEP, and source-backed bounds",
            "forbidden_input": "assuming matter blindness from unsigned quotient descent",
            "blocking_rows": "RV1875_4;RV1875_7;RV1875_8;RV1875_9",
            "current_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "TR1875_4_unification_spine",
            "arena": "framework_spine",
            "allowed_input": "explicit choice among constraint/no-pole, quotient representative, or finite residual field",
            "forbidden_input": "using different choices in different tests without a parent transition rule",
            "blocking_rows": "RV1875_0;RV1875_1;RV1875_10",
            "current_status": "CONSISTENCY_GATE_ACTIVE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "RBC1875_0_input_validity",
            "rule": "Every scored coefficient must have theorem_zero_certificate or numeric_value + units + source_path + source_exists.",
            "failure_mode": "MISSING_INPUT_BLOCKS_SCORE",
            "claim_allowed_if_failed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "RBC1875_1_route_separation",
            "rule": "Massless C_R/r tail may enter PPN/orbital only; finite R10 requires Z_R/M_R^2/lambda_range.",
            "failure_mode": "WRONG_ARENA_ROUTE_BLOCKS_SCORE",
            "claim_allowed_if_failed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "RBC1875_2_same_normalization",
            "rule": "Z_R, M_R^2, beta charges, C_R/Pi_R, kappa_W and M_* must be in a declared common parent/source frame.",
            "failure_mode": "NORMALIZATION_MISMATCH_BLOCKS_SCORE",
            "claim_allowed_if_failed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "RBC1875_3_no_cancellation",
            "rule": "No arena can pass by cancellation between unrelated residual vector components unless a parent identity proves that cancellation.",
            "failure_mode": "NO_CANCELLATION_GUARD_BLOCKS_CLAIM",
            "claim_allowed_if_failed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "RBC1875_4_baseline_comparison",
            "rule": "Any empirical residual score must compare against appropriate GR/PPN/baseline under the same data split and projection assumptions.",
            "failure_mode": "BASELINE_MISSING_BLOCKS_PUBLIC_EVIDENCE",
            "claim_allowed_if_failed": False,
            "valid_for_claim": False,
        },
    ]


def acquisition_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "queue_id": "ACQ1875_0_constraint_or_verticality",
            "priority": 1,
            "target": "q_shape/Dq[v_R]=0 or lambda_R/no-pole parent owner",
            "why_first": "would convert residual branch back into derived local-GR route",
            "required_output": "theorem-zero certificate or explicit failure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "queue_id": "ACQ1875_1_massless_tail",
            "priority": 2,
            "target": "C_R/Pi_R/kappa_W/M_* row",
            "why_first": "enables PPN/orbital bound runner while derivation remains open",
            "required_output": "nonclaim numeric/source row or zero theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "queue_id": "ACQ1875_2_finite_operator",
            "priority": 3,
            "target": "Z_R/M_R^2/lambda_range",
            "why_first": "required before any R10 alpha(lambda) test",
            "required_output": "same-normalized operator/range row or no-pole theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "queue_id": "ACQ1875_3_source_test_charges",
            "priority": 4,
            "target": "J_R/beta_source_R/beta_test_R/material coefficients",
            "why_first": "required for R10/WEP/clock/source amplitudes",
            "required_output": "source-backed charge table or matter-descent zero certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "queue_id": "ACQ1875_4_projection_and_bounds",
            "priority": 5,
            "target": "tau_PPN/tau_R10/tau_clock/tau_orbital/tau_WEP and accepted bounds",
            "why_first": "turns coefficients into observable comparisons",
            "required_output": "projection kernels plus source-backed bound rows",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1875_0_vector",
            "claim": "R_AB residual vector is ready for internal runner consumption",
            "status": "ALLOW_INTERNAL_NONCLAIM_VECTOR",
            "reason": "all active components and route blockers are explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1875_1_local_GR",
            "claim": "derived local GR/Newton from R_AB branch",
            "status": "BLOCKED",
            "reason": "domain verticality/constraint and no-cancellation are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1875_2_PPN_R10_clock_WEP",
            "claim": "any arena score is currently claimable",
            "status": "BLOCKED",
            "reason": "operator/source/projection/bound rows are missing or nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1875_3_public_evidence",
            "claim": "public empirical evidence from this branch",
            "status": "BLOCKED",
            "reason": "runner enforcement and baseline comparisons are not yet run",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1875_0_result",
            "decision": "RAB_RESIDUAL_VECTOR_READY_NONCLAIM",
            "reason": "R_AB is explicit residual field currently, so operator/source/tail/projection/no-cancellation components are unified in one intake vector",
            "consequence": "future tests can be wired without silently importing local-GR theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1875_1_routing",
            "decision": "MASSLESS_AND_FINITE_ROUTES_SEPARATED",
            "reason": "C_R/r is PPN/orbital; Z_R/M_R^2/lambda_range is finite R10/clock/orbital",
            "consequence": "massless hair cannot be scored as R10 alpha(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1875_2_next",
            "decision": "BLOCKING_RUNNER_DRYRUN_SELECTED_NEXT",
            "reason": "the next safety step is an executable runner that consumes the vector and proves every current route blocks",
            "consequence": "1876 should emit machine-readable blocked statuses for PPN/R10/clock/WEP/orbital/local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1875_0_primary",
            "target_doc": "1876-Y5-R2FR-RAB-residual-vector-blocking-runner-dryrun.md",
            "target_script": "scripts/Y5_R2FR_RAB_residual_vector_blocking_runner_dryrun_1876.py",
            "objective": "build a dry-run runner that consumes the 1875 residual vector and emits blocked/nonclaim statuses for local_GR, PPN, R10, clock, WEP, and orbital arenas until every required zero theorem or numeric/source row exists.",
            "selection_status": "selected",
            "success_condition": "runner returns claim_allowed=false in every current arena with exact missing row IDs and forbids massless C_R/r into R10.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1875_1_derivation_parallel",
            "target_doc": "1876b-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
            "target_script": "scripts/Y5_R2FR_qshape_or_lambdaR_parent_origin_source_hunt_1876b.py",
            "objective": "continue derivation-first by trying q_shape or lambda_R parent-origin once more using the vector blockers as the contract.",
            "selection_status": "held_parallel",
            "success_condition": "parent-signed q_shape/constraint owner or explicit permanent residual-field classification.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "residual_vector": residual_vector_rows(),
        "test_routing": test_routing_rows(),
        "runner_contract": runner_contract_rows(),
        "acquisition_queue": acquisition_queue_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in [
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "claim_allowed_if_failed",
            ]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["residual_vector"], QUEUE / "JR1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["test_routing"], QUEUE / "JR1875_RAB_TEST_ROUTING_MATRIX_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["runner_contract"], QUEUE / "JR1875_RAB_RUNNER_BLOCKER_CONTRACT_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1875_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1875_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1875"]) == "true" for row in sources) else "FAIL",
            "detail": "all residual-vector sources exist and contain required needles",
            "valid_for_claim": False,
        }
    )

    vector = rows_by_name["residual_vector"]
    required_statuses = {
        "MISSING_VERTICALITY_CERTIFICATE_OR_BOUND",
        "MISSING_PARENT_CONSTRAINT_ORIGIN",
        "MISSING_PARENT_OPERATOR_ZR",
        "MISSING_PARENT_OPERATOR_MR2_OR_RANGE_RELATION",
        "MISSING_SOURCE_CHARGE_RESOLUTION",
        "MISSING_C_R_PIR_KAPPA_MSTAR_OR_ZERO_THEOREM",
        "MISSING_BOUNDARY_RESOLUTION_OR_ABSOLUTE_TAIL_ENVELOPE",
        "MISSING_CONSTANT_SUPERSELECTION_OR_COEFFICIENTS",
        "MISSING_PROJECTION_KERNELS_OR_ACCEPTED_BOUND_CURVES",
        "MISSING_NO_CANCELLATION_GUARD",
        "RESIDUAL_VECTOR_READY_NONCLAIM_ALL_SCORES_BLOCKED",
    }
    checks.append(
        {
            "validation_id": "VAL1875_1_vector_coverage",
            "status": "PASS" if required_statuses == {row["current_status"] for row in vector} else "FAIL",
            "detail": "R_AB residual vector covers domain, constraint, operator, source, tail, boundary, projection, and no-cancellation",
            "valid_for_claim": False,
        }
    )

    routing = rows_by_name["test_routing"]
    checks.append(
        {
            "validation_id": "VAL1875_2_route_separation",
            "status": "PASS"
            if any(row["arena"] == "R10 alpha(lambda)" and "massless C_R/r tail" in row["forbidden_input"] for row in routing)
            and any(row["arena"] == "PPN/orbital/light-time" for row in routing)
            else "FAIL",
            "detail": "massless and finite-range routes are separated",
            "valid_for_claim": False,
        }
    )

    runner = rows_by_name["runner_contract"]
    checks.append(
        {
            "validation_id": "VAL1875_3_runner_contract",
            "status": "PASS"
            if any(row["failure_mode"] == "MISSING_INPUT_BLOCKS_SCORE" for row in runner)
            and any(row["failure_mode"] == "NO_CANCELLATION_GUARD_BLOCKS_CLAIM" for row in runner)
            and all(bool_string(row["claim_allowed_if_failed"]) == "false" for row in runner)
            else "FAIL",
            "detail": "runner blocker contract forbids scoring missing rows and cancellation credit",
            "valid_for_claim": False,
        }
    )

    acquisition = rows_by_name["acquisition_queue"]
    checks.append(
        {
            "validation_id": "VAL1875_4_acquisition_queue",
            "status": "PASS"
            if len(acquisition) == 5
            and acquisition[0]["target"] == "q_shape/Dq[v_R]=0 or lambda_R/no-pole parent owner"
            else "FAIL",
            "detail": "coefficient acquisition queue is prioritized",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1875_5_claim_gates",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_VECTOR" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim vector is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1875_6_decision",
            "status": "PASS"
            if any(row["decision"] == "RAB_RESIDUAL_VECTOR_READY_NONCLAIM" for row in decisions)
            and any(row["decision"] == "BLOCKING_RUNNER_DRYRUN_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision ledger marks vector ready and selects blocking runner",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1875_7_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1875_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1876 blocking runner target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1875_8_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1875_9_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["residual_vector"].name,
        QUARANTINE / OUTPUTS["runner_contract"].name,
        QUEUE / "JR1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR_NONCLAIM.csv",
        QUEUE / "JR1875_RAB_RUNNER_BLOCKER_CONTRACT_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1875_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1875_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1875*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1875_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1875_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1875_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1875 R_AB residual operator/source vector and test routing checkpoint",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1875 - R_AB Residual Operator/Source Vector And Test Routing

**Private status:** nonclaim checkpoint. No derived local-GR, PPN, R10, WEP, clock, orbital, EM, or cosmology pass is claimed.

## Result

`R_AB` is now treated as an explicit residual field unless a future parent theorem signs verticality or constraint/no-pole. This checkpoint makes that operational:

```text
R_RAB_total =
  domain visibility
+ constraint/no-pole owner
+ finite operator Z_R/M_R^2/lambda_range
+ bulk source/test charges
+ massless C_R/Pi_R tail
+ boundary/readout/hidden tail
+ constants/markers/source weights
+ observable projection kernels
+ no-cancellation guard
```

The key route split is locked:

```text
C_R/r massless tail       -> PPN/orbital/light-time only
Z_R,M_R^2,lambda_range    -> finite R10/clock/orbital only
closure R_AB=0            -> benchmark only unless parent-derived
```

So 1875 is a boring-looking but important piece of plumbing: it tells every future runner exactly what must be zero-derived or source-bounded before any score can be treated as evidence.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Residual Vector

{markdown_table(rows_by_name["residual_vector"])}

## Test Routing

{markdown_table(rows_by_name["test_routing"])}

## Runner Blocker Contract

{markdown_table(rows_by_name["runner_contract"])}

## Acquisition Queue

{markdown_table(rows_by_name["acquisition_queue"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
