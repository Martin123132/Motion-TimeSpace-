from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1885"
BETA_BOUND = 7.8e-05

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md"

INPUTS = {
    "1884_doc": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
    "1884_validation": OUT / "P8_Y5_BRR545_1884_VALIDATION.csv",
    "1884_dpqr_contract": OUT / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_INPUT_CONTRACT.csv",
    "1883_full_vector": OUT / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
    "1584_beta_gate": OUT / "P8_Y5_PARENT_QLOC_1584_BETA_GATE.csv",
    "1585_beta_ledger": OUT / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv",
    "1594_beta_spec": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_SPEC.csv",
    "1594_beta_results": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_RESULTS.csv",
    "1694_delta_w_current": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
    "1810_source_alpha_zero": OUT / "P8_Y5_PARENT_QLOC_1810_BETA_SOURCE_ALPHA_ZERO_THEOREM_AUDIT.csv",
    "1848_beta_eigenvalue": OUT / "P8_Y5_PARENT_QLOC_1848_BETA_EIGENVALUE_ATTEMPT.csv",
    "local_beta_bound": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1884_doc": [
        "NEXT1884_0_primary",
        "BETA_SOURCE_COUPLING_OR_PARENT_ZERO_ROW",
    ],
    "1884_validation": [
        "VAL1884_OVERALL,PASS",
    ],
    "1884_dpqr_contract": [
        "DPQR1884_6_descent_statuses",
        "MISSING_MATTER_READOUT_DESCENT",
    ],
    "1883_full_vector": [
        "PPNV1883_2_beta_second_order",
        "MISSING_BETA_FIELD_EQUATION_AND_CONSERVATION_PROOF",
    ],
    "1584_beta_gate": [
        "BETA1584_1_gamma_not_beta",
        "FAIL_CURRENT_CLAIM_BETA_NOT_DERIVED",
    ],
    "1585_beta_ledger": [
        "BRL1585_0_delta_beta_source",
        "BRL1585_7_total_no_cancellation",
    ],
    "1594_beta_spec": [
        "BVS1594_7_flags",
        "default false",
    ],
    "1594_beta_results": [
        "BVR1594_0_FBR1593_0_beta_source",
        "MISSING_SOURCE_BETA",
    ],
    "1694_delta_w_current": [
        "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor",
        "NONCLAIM_ONLY",
    ],
    "1810_source_alpha_zero": [
        "BZA1810_0_chain_rule_core",
        "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS",
    ],
    "1848_beta_eigenvalue": [
        "BE1848_4_verdict",
        "FAIL_CURRENT_CLAIM",
    ],
    "local_beta_bound": [
        "Will_2014_PPN_beta_table",
        "7.8e-05",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1885_SOURCE_REGISTER.csv",
    "beta_second_order_audit": OUT / "P8_Y5_PARENT_QLOC_1885_BETA_SECOND_ORDER_GATE_AUDIT.csv",
    "source_coupling_audit": OUT / "P8_Y5_PARENT_QLOC_1885_SOURCE_COUPLING_ZERO_AUDIT.csv",
    "beta_residual_contract": OUT / "P8_Y5_PARENT_QLOC_1885_BETA_RESIDUAL_VECTOR_CONTRACT.csv",
    "candidate_template": OUT / "P8_Y5_PARENT_QLOC_1885_BETA_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1885_BETA_SOURCE_VALIDATOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1885_BETA_SOURCE_VALIDATOR_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1885_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1885_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1885_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1885_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1885_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1885_VALIDATION.csv",
}

BETA_TEMPLATE_DOC_COPY = BETA_DOCS / "BETA1885_SOURCE_COUPLING_OR_PARENT_ZERO_TEMPLATE_NONCLAIM.csv"


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def is_placeholder(value: Any) -> bool:
    text = str(value).strip()
    if not text:
        return True
    return any(marker in text.upper() for marker in ("MISSING", "PLACEHOLDER", "TBD", "UNSIGNED", "HYPOTHETICAL"))


def finite_float(value: Any) -> tuple[bool, float | None]:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


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
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1885": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def beta_second_order_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "B2G1885_0_ppn_definition",
            "gate": "PPN beta grammar",
            "formal_statement": "g_00=-1+2U/c^2-2 beta U^2/c^4+O(c^-6), so delta_beta=beta-1 is a second-order source-normalized observable.",
            "current_result": "FORMAL_TARGET",
            "blocker": "not a prediction until the same observed U=GM/r and second-order readout are owned",
            "claim_effect": "defines what must be derived or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "B2G1885_1_gamma_not_beta",
            "gate": "gamma cannot imply beta",
            "formal_statement": "C_R/q_R_hat controls the first-order reciprocal product channel; it does not fix the nonlinear U^2 coefficient.",
            "current_result": "NO_GAMMA_ONLY_PROMOTION",
            "blocker": "gamma closure can coexist with a live beta/source residual",
            "claim_effect": "local GR requires a beta gate after 1884",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "B2G1885_2_EH_conditional",
            "gate": "EH one-parameter exterior",
            "formal_statement": "If one parent action owns the EH-like local operator, universal matter coupling, measured mass, and Bianchi/source conservation, then the one-parameter exterior gives beta=1.",
            "current_result": "EXACT_CONDITIONAL_ROUTE",
            "blocker": "the EH/source-normalized parent package is not signed by current MTS branch",
            "claim_effect": "usable as target contract, not as proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "B2G1885_3_residual_vector",
            "gate": "second-order residual decomposition",
            "formal_statement": "delta_beta_total_abs=sum abs(delta_beta_source, delta_beta_operator, delta_beta_q_loc, delta_beta_boundary_domain, delta_beta_readout, epsilon_SN).",
            "current_result": "NO_CANCELLATION_VECTOR_REQUIRED",
            "blocker": "1585 components are missing theorem-zero or source-backed finite rows",
            "claim_effect": "beta pass cannot use cancellation or a single component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "B2G1885_4_external_bound",
            "gate": "local beta comparator",
            "formal_statement": "|beta-1| <= 7.8e-05 from the local bound table can test a full MTS delta_beta prediction.",
            "current_result": "BOUND_AVAILABLE_PREDICTION_MISSING",
            "blocker": "the comparator is evidence only after MTS supplies the full source-normalized beta vector",
            "claim_effect": "do not score beta from the bound alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "B2G1885_5_eigenvalue_route",
            "gate": "finite beta eigenvalue",
            "formal_statement": "A parent-owned Hessian/field-space metric spectrum could define beta_eff without post-hoc fitting.",
            "current_result": "NOT_PARENT_OWNED",
            "blocker": "1848 leaves G_X, V_eff, spectrum and trace degeneracy unsigned",
            "claim_effect": "no beta=3 or range/eigenvalue claim is allowed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "B2G1885_6_verdict",
            "gate": "beta=1 or finite beta prediction",
            "formal_statement": "Current MTS parent supplies beta=1 or a finite source-normalized beta residual vector.",
            "current_result": "BETA_GATE_NOT_DERIVED_CURRENT_CORPUS",
            "blocker": "source-normalized parent action, common matter coupling, no-source-only slot, q_loc and boundary/readout silence remain open",
            "claim_effect": "build strict beta/source row contract and move to common-source coupling proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_coupling_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "SCZ1885_0_chain_rule_core",
            "target": "source-coupling zero theorem",
            "formal_statement": "If S_matter and material constants factor through q and v_X lies in ker(Dq), then delta_v S_matter=0 and beta_source/alpha_source markers vanish.",
            "current_status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "missing_for_claim": "parent q/Dq signature, matter functor, constant owner, boundary/readout silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "SCZ1885_1_no_source_only_slot",
            "target": "no independent source/action prefactor",
            "formal_statement": "There is no w_A(X) S_A slot that changes source/test strength while ordinary matter still appears Hilbertian.",
            "current_status": "EXACT_TARGET_NOT_PARENT_DERIVED",
            "missing_for_claim": "object-language action-measure theorem and current-owner proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "SCZ1885_2_tau_role_lock",
            "target": "one tau across source, charge, clock, orbit and boundary",
            "formal_statement": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary after the quotient pushforward.",
            "current_status": "NOT_DERIVED",
            "missing_for_claim": "tau projectability, role-lock certificate and stationarity/admissibility domain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "SCZ1885_3_bound_anchor",
            "target": "source/action-weight bound anchor",
            "formal_statement": "MICROSCOPE supplies a source-backed product bound anchor P=abs(Delta_w_TiPt*tau_WEP)=2.8e-15.",
            "current_status": "BOUND_ANCHOR_ONLY_NONCLAIM",
            "missing_for_claim": "MTS beta/Delta_w prediction row, tau_WEP, material map, and readout kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "SCZ1885_4_countermodel_guard",
            "target": "same-frame wording is not enough",
            "formal_statement": "e_obs=exp(b_g X)e0 or w_A(X)S_A is a live countermodel unless b_g=0 and w_A'=0 are parent-signed.",
            "current_status": "COUNTERMODEL_RETAINED",
            "missing_for_claim": "no-shadow and no-source-only-slot theorem or finite b_g/w_A rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "SCZ1885_5_verdict",
            "target": "common matter/source coupling",
            "formal_statement": "Current MTS parent proves universal matter/source coupling with no hidden source marker.",
            "current_status": "SOURCE_COUPLING_ZERO_NOT_CLOSED",
            "missing_for_claim": "q/Dq, matter descent, no source-only slot, tau role lock, boundary and readout silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def beta_residual_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "BRC1885_0_delta_beta_source",
            "quantity": "delta_beta_source",
            "definition": "B_source/A_source^2 - 1 after measured-GM normalization",
            "required_input": "parent proof B_source=A_source^2 or source-backed A_source/B_source row",
            "units": "dimensionless",
            "claim_gate": "must be zero or finite and source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "BRC1885_1_delta_beta_operator",
            "quantity": "delta_beta_operator",
            "definition": "second-order local field/operator correction not captured by the EH one-parameter family",
            "required_input": "operator theorem-zero or coefficient row with units and source path",
            "units": "dimensionless",
            "claim_gate": "cannot be inferred from gamma",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "BRC1885_2_delta_beta_q_loc",
            "quantity": "delta_beta_q_loc",
            "definition": "physical U2 projection of P_loc(nabla Gamma_eff-div Khat)",
            "required_input": "Ward-zero through O(U2) or beta-normalized q_loc profile",
            "units": "dimensionless",
            "claim_gate": "same PPN arena and source normalization required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "BRC1885_3_delta_beta_boundary_domain",
            "quantity": "delta_beta_boundary_domain",
            "definition": "boundary/domain/projector quadratic stress beta projection",
            "required_input": "no-flux/no-hair theorem or coefficient map with units",
            "units": "dimensionless",
            "claim_gate": "boundary silence must be parent-signed or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "BRC1885_4_delta_beta_readout",
            "quantity": "delta_beta_readout",
            "definition": "second-order mismatch between source metric and observed isotropic PPN readout",
            "required_input": "same observed coframe/readout theorem through O(U2)",
            "units": "dimensionless",
            "claim_gate": "common matter/coframe descent required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "BRC1885_5_epsilon_SN",
            "quantity": "epsilon_SN",
            "definition": "(mu_obs-G_eff M_H)/(G_eff M_H)",
            "required_input": "Gauss/orbital/source-current scorecard",
            "units": "dimensionless",
            "claim_gate": "measured-GM denominator cannot absorb relative source weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "BRC1885_6_delta_beta_total_abs",
            "quantity": "Delta_beta_total_abs",
            "definition": "sum of absolute active beta residual components with no cancellation credit",
            "required_input": "all components theorem-zero or numeric/source-backed",
            "units": "dimensionless",
            "claim_gate": f"Delta_beta_total_abs <= {BETA_BOUND:.2e}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "BRC1885_7_flags",
            "quantity": "valid_for_claim;claim_allowed;score_ready",
            "definition": "row eligibility flags",
            "required_input": "may become true only after source path, convention, arena and component gates all pass",
            "units": "boolean",
            "claim_gate": "False throughout 1885",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def candidate_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "BETA1885_TEMPLATE_PARENT_ZERO",
            "branch_id": BRANCH_ID,
            "route_type": "parent_beta_zero",
            "delta_beta_source": "0",
            "delta_beta_operator": "0",
            "delta_beta_q_loc": "0",
            "delta_beta_boundary_domain": "0",
            "delta_beta_readout": "0",
            "epsilon_SN": "0",
            "Delta_beta_total_abs": "0",
            "beta_bound": f"{BETA_BOUND:.2e}",
            "units": "dimensionless",
            "GM_convention": "same observed U=GM/r and measured source mass",
            "source_path": "MISSING_PARENT_BETA_SOURCE_COUPLING_ZERO_THEOREM",
            "beta_convention": "PPN beta_minus_1 after measured-GM normalization",
            "parent_zero_status": "MISSING_PARENT_INPUT",
            "source_coupling_status": "MISSING_NO_SOURCE_ONLY_SLOT",
            "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
            "boundary_readout_status": "MISSING_BOUNDARY_READOUT_SILENCE",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "BETA1885_TEMPLATE_FINITE_VECTOR",
            "branch_id": BRANCH_ID,
            "route_type": "finite_beta_vector",
            "delta_beta_source": "MISSING_NUMERIC_DELTA_BETA_SOURCE",
            "delta_beta_operator": "MISSING_NUMERIC_DELTA_BETA_OPERATOR",
            "delta_beta_q_loc": "MISSING_NUMERIC_DELTA_BETA_Q_LOC",
            "delta_beta_boundary_domain": "MISSING_NUMERIC_DELTA_BETA_BOUNDARY_DOMAIN",
            "delta_beta_readout": "MISSING_NUMERIC_DELTA_BETA_READOUT",
            "epsilon_SN": "MISSING_NUMERIC_EPSILON_SN",
            "Delta_beta_total_abs": "MISSING_SUM_ABS_VECTOR",
            "beta_bound": f"{BETA_BOUND:.2e}",
            "units": "dimensionless",
            "GM_convention": "MISSING_MEASURED_GM_SOURCE_CONVENTION",
            "source_path": "MISSING_SOURCE_PATH_OR_EXTERNAL_PROVENANCE",
            "beta_convention": "MISSING_PPN_BETA_CONVENTION",
            "parent_zero_status": "not_applicable",
            "source_coupling_status": "finite_source_coupling_rows_required",
            "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT_OR_FINITE_ROW",
            "boundary_readout_status": "MISSING_BOUNDARY_READOUT_ROW",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    source_template = str(OUTPUTS["candidate_template"])
    return [
        {
            "case_id": "CASE1885_0_gamma_only",
            "route_type": "finite_beta_vector",
            "delta_beta_source": "MISSING",
            "delta_beta_operator": "MISSING",
            "delta_beta_q_loc": "MISSING",
            "delta_beta_boundary_domain": "MISSING",
            "delta_beta_readout": "MISSING",
            "epsilon_SN": "MISSING",
            "source_path": str(INPUTS["1883_full_vector"]),
            "GM_convention": "same measured GM as gamma test",
            "beta_convention": "gamma-only shortcut",
            "parent_zero_status": "not_applicable",
            "source_coupling_status": "UNSIGNED",
            "matter_descent_status": "UNSIGNED",
            "boundary_readout_status": "UNSIGNED",
            "closure_used": False,
            "gamma_only": True,
            "comparator_only": False,
            "cancellation_only": False,
            "source_backed_bound_only": False,
            "full_vector_ready": False,
            "derivation_status": "gamma_only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1885_1_comparator_bound_only",
            "route_type": "finite_beta_vector",
            "delta_beta_source": "7.8e-05",
            "delta_beta_operator": "0",
            "delta_beta_q_loc": "0",
            "delta_beta_boundary_domain": "0",
            "delta_beta_readout": "0",
            "epsilon_SN": "0",
            "source_path": str(INPUTS["local_beta_bound"]),
            "GM_convention": "local beta comparator only",
            "beta_convention": "Will 2014 bound",
            "parent_zero_status": "not_applicable",
            "source_coupling_status": "not_supplied",
            "matter_descent_status": "not_supplied",
            "boundary_readout_status": "not_supplied",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": True,
            "cancellation_only": False,
            "source_backed_bound_only": False,
            "full_vector_ready": False,
            "derivation_status": "comparator_bound_not_prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1885_2_EH_closure_import",
            "route_type": "parent_beta_zero",
            "delta_beta_source": "0",
            "delta_beta_operator": "0",
            "delta_beta_q_loc": "0",
            "delta_beta_boundary_domain": "0",
            "delta_beta_readout": "0",
            "epsilon_SN": "0",
            "source_path": str(INPUTS["1585_beta_ledger"]),
            "GM_convention": "EH one-parameter family",
            "beta_convention": "beta=1 by imported EH exterior",
            "parent_zero_status": "CLOSURE_OR_GR_IMPORT",
            "source_coupling_status": "UNSIGNED",
            "matter_descent_status": "UNSIGNED",
            "boundary_readout_status": "UNSIGNED",
            "closure_used": True,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": False,
            "source_backed_bound_only": False,
            "full_vector_ready": False,
            "derivation_status": "closure_benchmark",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1885_3_missing_vector",
            "route_type": "finite_beta_vector",
            "delta_beta_source": "MISSING",
            "delta_beta_operator": "MISSING",
            "delta_beta_q_loc": "MISSING",
            "delta_beta_boundary_domain": "MISSING",
            "delta_beta_readout": "MISSING",
            "epsilon_SN": "MISSING",
            "source_path": "MISSING_SOURCE_PATH",
            "GM_convention": "MISSING_GM_CONVENTION",
            "beta_convention": "MISSING_BETA_CONVENTION",
            "parent_zero_status": "not_applicable",
            "source_coupling_status": "MISSING",
            "matter_descent_status": "MISSING",
            "boundary_readout_status": "MISSING",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": False,
            "source_backed_bound_only": False,
            "full_vector_ready": False,
            "derivation_status": "missing_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1885_4_unsigned_parent_zero",
            "route_type": "parent_beta_zero",
            "delta_beta_source": "0",
            "delta_beta_operator": "0",
            "delta_beta_q_loc": "0",
            "delta_beta_boundary_domain": "0",
            "delta_beta_readout": "0",
            "epsilon_SN": "0",
            "source_path": str(INPUTS["1810_source_alpha_zero"]),
            "GM_convention": "same observed U=GM/r and measured source mass",
            "beta_convention": "PPN beta_minus_1 after measured-GM normalization",
            "parent_zero_status": "UNSIGNED_PARENT_CHAIN",
            "source_coupling_status": "MISSING_NO_SOURCE_ONLY_SLOT",
            "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
            "boundary_readout_status": "MISSING_BOUNDARY_READOUT_SILENCE",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": False,
            "source_backed_bound_only": False,
            "full_vector_ready": False,
            "derivation_status": "parent_zero_unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1885_5_source_backed_bound_anchor",
            "route_type": "finite_beta_vector",
            "delta_beta_source": "MISSING",
            "delta_beta_operator": "MISSING",
            "delta_beta_q_loc": "MISSING",
            "delta_beta_boundary_domain": "MISSING",
            "delta_beta_readout": "MISSING",
            "epsilon_SN": "MISSING",
            "source_path": str(INPUTS["1694_delta_w_current"]),
            "GM_convention": "WEP source-charge anchor only",
            "beta_convention": "Delta_w_TiPt*tau_WEP product convention",
            "parent_zero_status": "not_applicable",
            "source_coupling_status": "BOUND_ANCHOR_ONLY",
            "matter_descent_status": "UNSIGNED",
            "boundary_readout_status": "UNSIGNED",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": False,
            "source_backed_bound_only": True,
            "full_vector_ready": False,
            "derivation_status": "source_backed_bound_anchor_not_mts_prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1885_6_cancellation_tuned",
            "route_type": "finite_beta_vector",
            "delta_beta_source": "1.0e-04",
            "delta_beta_operator": "-1.0e-04",
            "delta_beta_q_loc": "0",
            "delta_beta_boundary_domain": "0",
            "delta_beta_readout": "0",
            "epsilon_SN": "0",
            "source_path": source_template,
            "GM_convention": "same observed U=GM/r and measured source mass",
            "beta_convention": "PPN beta_minus_1 after measured-GM normalization",
            "parent_zero_status": "not_applicable",
            "source_coupling_status": "schema_test_only",
            "matter_descent_status": "schema_test_only",
            "boundary_readout_status": "schema_test_only",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": True,
            "source_backed_bound_only": False,
            "full_vector_ready": True,
            "derivation_status": "schema_test_only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1885_7_schema_complete_nonclaim",
            "route_type": "finite_beta_vector",
            "delta_beta_source": "1.0e-06",
            "delta_beta_operator": "1.0e-06",
            "delta_beta_q_loc": "1.0e-06",
            "delta_beta_boundary_domain": "1.0e-06",
            "delta_beta_readout": "1.0e-06",
            "epsilon_SN": "1.0e-06",
            "source_path": source_template,
            "GM_convention": "same observed U=GM/r and measured source mass",
            "beta_convention": "PPN beta_minus_1 after measured-GM normalization",
            "parent_zero_status": "not_applicable",
            "source_coupling_status": "schema_test_only_signed",
            "matter_descent_status": "schema_test_only_signed",
            "boundary_readout_status": "schema_test_only_signed",
            "closure_used": False,
            "gamma_only": False,
            "comparator_only": False,
            "cancellation_only": False,
            "source_backed_bound_only": False,
            "full_vector_ready": True,
            "derivation_status": "schema_test_only_not_physics_evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    route_type = str(row.get("route_type", "")).strip()
    closure_used = bool_string(row.get("closure_used", "")) == "true"
    gamma_only = bool_string(row.get("gamma_only", "")) == "true"
    comparator_only = bool_string(row.get("comparator_only", "")) == "true"
    cancellation_only = bool_string(row.get("cancellation_only", "")) == "true"
    source_backed_bound_only = bool_string(row.get("source_backed_bound_only", "")) == "true"
    full_vector_ready = bool_string(row.get("full_vector_ready", "")) == "true"
    component_fields = [
        "delta_beta_source",
        "delta_beta_operator",
        "delta_beta_q_loc",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "epsilon_SN",
    ]
    parsed = {field: finite_float(row.get(field, "")) for field in component_fields}
    all_numeric = all(ok for ok, _ in parsed.values())
    total_abs = "not_evaluated"
    total_pass = False
    valid_prediction_row = False
    score_ready = False

    if bool_string(row.get("valid_for_claim", "")) != "false" or bool_string(row.get("claim_allowed", "")) != "false":
        status = "REFUSED_CLAIM_FLAG"
    elif closure_used:
        status = "REFUSED_CLOSURE_OR_GR_IMPORT"
    elif gamma_only:
        status = "REFUSED_GAMMA_ONLY"
    elif comparator_only:
        status = "REFUSED_COMPARATOR_ONLY"
    elif cancellation_only:
        status = "REFUSED_CANCELLATION_ONLY"
    elif source_backed_bound_only:
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    elif route_type not in {"parent_beta_zero", "finite_beta_vector"}:
        status = "REFUSED_BAD_ROUTE_TYPE"
    elif route_type == "parent_beta_zero":
        if not all_numeric or any(abs(value or 0.0) > 1e-12 for _, value in parsed.values()):
            status = "REFUSED_PARENT_ZERO_NUMERIC_MISMATCH"
        elif str(row.get("parent_zero_status", "")) != "PARENT_SIGNED_BETA_SOURCE_COUPLING_ZERO":
            status = "REFUSED_PARENT_BETA_ZERO_UNSIGNED"
        elif any("MISSING" in str(row.get(field, "")).upper() or "UNSIGNED" in str(row.get(field, "")).upper() for field in ("source_coupling_status", "matter_descent_status", "boundary_readout_status")):
            status = "REFUSED_MISSING_SOURCE_COUPLING_PREMISES"
        else:
            valid_prediction_row = True
            score_ready = full_vector_ready
            total_abs = "0"
            total_pass = True
            status = "SCHEMA_READY_PARENT_ZERO_NONCLAIM"
    else:
        if not all_numeric:
            status = "REFUSED_MISSING_BETA_VECTOR_COMPONENTS"
        elif is_placeholder(row.get("source_path", "")):
            status = "REFUSED_MISSING_SOURCE"
        elif is_placeholder(row.get("GM_convention", "")) or is_placeholder(row.get("beta_convention", "")):
            status = "REFUSED_MISSING_CONVENTION"
        elif any("MISSING" in str(row.get(field, "")).upper() or "UNSIGNED" in str(row.get(field, "")).upper() for field in ("source_coupling_status", "matter_descent_status", "boundary_readout_status")):
            status = "REFUSED_MISSING_SOURCE_COUPLING_PREMISES"
        else:
            total_value = sum(abs(value or 0.0) for _, value in parsed.values())
            total_abs = f"{total_value:.12g}"
            total_pass = total_value <= BETA_BOUND
            valid_prediction_row = True
            if "schema_test_only" in str(row.get("derivation_status", "")):
                score_ready = False
                status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
            elif not full_vector_ready:
                score_ready = False
                status = "SCHEMA_READY_BUT_VECTOR_INCOMPLETE"
            elif not total_pass:
                score_ready = False
                status = "SCHEMA_NUMERIC_FAILS_BETA_BOUND_NONCLAIM"
            else:
                score_ready = True
                status = "SCHEMA_READY_NONCLAIM"

    result = dict(row)
    result.update(
        {
            "Delta_beta_total_abs_evaluated": total_abs,
            "beta_bound": f"{BETA_BOUND:.2e}",
            "bound_pass_math": total_pass,
            "validator_status": status,
            "valid_prediction_row": valid_prediction_row,
            "score_ready": score_ready,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return result


def dryrun_result_rows() -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in dryrun_case_rows()]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1885_0_beta_zero_proof_checker",
            "runner": "parent beta/source-coupling zero proof checker",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "EH/beta=1 route is exact only after source-normalized parent action and common matter coupling are signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1885_1_beta_vector_validator",
            "runner": "finite beta residual-vector validator",
            "current_status": "ALLOW_SCHEMA_DRYRUN_NONCLAIM",
            "reason": "schema and failure modes are testable, but no live sourced MTS beta vector exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1885_2_local_gr_scorer",
            "runner": "local GR/Newton scorer",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "gamma/q_R, beta, source coupling, matter descent, boundary/readout and Khat/q_loc are not all closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1885_0_gamma_guard",
            "claim": "gamma/local reciprocal lock implies beta/local GR",
            "status": "BLOCKED",
            "reason": "1584 and 1883 keep beta as an independent second-order component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1885_1_EH_conditional",
            "claim": "EH one-parameter route gives beta=1 if parent action owns the source-normalized package",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "useful target, but MTS parent package is unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1885_2_source_coupling_zero",
            "claim": "common matter/source coupling has no hidden source-only slot",
            "status": "BLOCKED",
            "reason": "1810 makes the chain-rule route exact conditional but not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1885_3_beta_vector",
            "claim": "finite beta vector can be scored against |beta-1|<=7.8e-05",
            "status": "BLOCKED",
            "reason": "no live source-backed vector row exists; only templates and bound anchors exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1885_4_local_gr",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED",
            "reason": "beta/source coupling remains open after 1885",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1885_0_beta_is_independent",
            "decision": "BETA_NOT_DERIVED_FROM_GAMMA",
            "because": "gamma/q_R controls the first-order metric product channel, not the U2 coefficient",
            "next_action": "keep beta in the full vector until a parent theorem or finite vector row closes it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1885_1_EH_target_retained",
            "decision": "EH_ROUTE_CONDITIONAL_TARGET_ONLY",
            "because": "one parent source-normalized EH-like action would solve beta, conservation and common matter together",
            "next_action": "try to parent-sign common matter/no-source-only-slot rather than importing GR exterior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1885_2_source_slot_next",
            "decision": "NO_SOURCE_ONLY_SLOT_IS_NEXT_BEST_ATTACK",
            "because": "1810/1694 show source/action-weight leakage is the live coupling loophole",
            "next_action": "build the no-source-only-slot proof attempt or finite w_R/beta_w row contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1885_0_primary",
            "selection_status": "selected",
            "target_file": "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
            "target_script": "scripts/Y5_R2FR_common_matter_no_source_only_slot_proof_or_finite_wR_row_1886.py",
            "objective": "try to parent-prove that ordinary matter has no hidden source-only/action-weight slot; if not, build a finite w_R/beta_w source-normalized input row contract",
            "success_condition": "a parent-signed no-source-only-slot theorem, or a strict finite source-weight row validator tied to WEP/PPN/Newton without claiming local GR",
            "do_not_do": "do not absorb relative source weights into G_N, do not use WEP bound anchors as MTS predictions, and do not import EH beta=1 as proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PSTAT1885_0_gain",
            "topic": "beta gate",
            "status": "BETA_VECTOR_CONTRACT_READY_NONCLAIM",
            "risk_level": "ROBUSTNESS_GAIN",
            "detail": "beta is now protected from gamma-only, comparator-only and cancellation-only pseudo-passes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "PSTAT1885_1_bottleneck",
            "topic": "source coupling",
            "status": "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED",
            "risk_level": "MAIN_BOTTLENECK",
            "detail": "hidden source/action-weight leakage can spoil Newton/PPN even if gamma and beta templates look tidy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "PSTAT1885_2_best_attack",
            "topic": "next route",
            "status": "COMMON_MATTER_SOURCE_SLOT_PROOF",
            "risk_level": "NEXT_BEST_MOVE",
            "detail": "the cleanest route is parent-signing matter descent/no-source-only-slot, not chasing a numerical beta bound first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "beta_second_order_audit": beta_second_order_audit_rows(),
        "source_coupling_audit": source_coupling_audit_rows(),
        "beta_residual_contract": beta_residual_contract_rows(),
        "candidate_template": candidate_template_rows(),
        "dryrun_cases": dryrun_case_rows(),
        "dryrun_results": dryrun_result_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    ok = True
    for path in paths:
        try:
            rows = csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in ("valid_for_claim", "claim_allowed"):
                if field in row and bool_string(row[field]) != "false":
                    bad.append(f"{path.name}:line{index}:{field}={row[field]}")
    return not bad, "all claim flags false" if not bad else "; ".join(bad)


def missing_statuses_not_claim_ready(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            row_text = " ".join(str(value) for value in row.values()).upper()
            if any(marker in row_text for marker in ("MISSING", "UNSIGNED", "CLOSURE", "IMPORT", "COMPARATOR_ONLY")):
                if bool_string(row.get("valid_for_claim", "false")) != "false" or bool_string(row.get("claim_allowed", "false")) != "false":
                    bad.append(f"{path.name}:line{index}:claim flag with blocked marker")
                if bool_string(row.get("score_ready", "false")) == "true":
                    bad.append(f"{path.name}:line{index}:score_ready with blocked marker")
    return not bad, "blocked-marker rows are not claim-ready" if not bad else "; ".join(bad)


def copy_branch_artifacts() -> None:
    copy_pairs = [
        (OUTPUTS["beta_second_order_audit"], MICROSCOPE_RESIDUALS / OUTPUTS["beta_second_order_audit"].name),
        (OUTPUTS["source_coupling_audit"], QUEUE / "JR1885_SOURCE_COUPLING_ZERO_AUDIT_NONCLAIM.csv"),
        (OUTPUTS["beta_residual_contract"], QUEUE / "JR1885_BETA_RESIDUAL_VECTOR_CONTRACT_NONCLAIM.csv"),
        (OUTPUTS["candidate_template"], BETA_TEMPLATE_DOC_COPY),
        (OUTPUTS["dryrun_results"], QUARANTINE / OUTPUTS["dryrun_results"].name),
    ]
    for src, dst in copy_pairs:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    sources = csv_rows(OUTPUTS["source_register"])
    source_count = len(sources)
    source_ok = sum(1 for row in sources if bool_string(row["source_exists"]) == "true")
    needle_ok = sum(1 for row in sources if row["needle_check"] == "OK")
    checks.append(
        {
            "validation_id": "VAL1885_0_sources_exist",
            "status": "PASS" if source_ok == source_count else "FAIL",
            "detail": f"{source_ok}/{source_count} sources exist",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1885_1_needles_found",
            "status": "PASS" if needle_ok == source_count else "FAIL",
            "detail": f"{needle_ok}/{source_count} source needles found",
            "valid_for_claim": False,
        }
    )

    beta_audit = csv_rows(OUTPUTS["beta_second_order_audit"])
    checks.append(
        {
            "validation_id": "VAL1885_2_gamma_not_beta",
            "status": "PASS"
            if any(row["audit_id"] == "B2G1885_1_gamma_not_beta" and row["current_result"] == "NO_GAMMA_ONLY_PROMOTION" for row in beta_audit)
            else "FAIL",
            "detail": "gamma-only local-GR promotion is explicitly blocked",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1885_3_beta_not_promoted",
            "status": "PASS"
            if any(row["audit_id"] == "B2G1885_6_verdict" and row["current_result"] == "BETA_GATE_NOT_DERIVED_CURRENT_CORPUS" for row in beta_audit)
            else "FAIL",
            "detail": "beta=1 or finite beta prediction is not claimed",
            "valid_for_claim": False,
        }
    )

    source_audit = csv_rows(OUTPUTS["source_coupling_audit"])
    checks.append(
        {
            "validation_id": "VAL1885_4_source_coupling_blockers",
            "status": "PASS"
            if any(row["current_status"] == "EXACT_CONDITIONAL_CHAIN_RULE" for row in source_audit)
            and any(row["current_status"] == "SOURCE_COUPLING_ZERO_NOT_CLOSED" for row in source_audit)
            and any(row["current_status"] == "COUNTERMODEL_RETAINED" for row in source_audit)
            else "FAIL",
            "detail": "chain-rule target, countermodel and failed closure all recorded",
            "valid_for_claim": False,
        }
    )

    contract = csv_rows(OUTPUTS["beta_residual_contract"])
    required_components = {
        "delta_beta_source",
        "delta_beta_operator",
        "delta_beta_q_loc",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "epsilon_SN",
        "Delta_beta_total_abs",
    }
    checks.append(
        {
            "validation_id": "VAL1885_5_beta_vector_components",
            "status": "PASS" if required_components.issubset({row["quantity"] for row in contract}) else "FAIL",
            "detail": f"beta_vector_components={len(contract)}",
            "valid_for_claim": False,
        }
    )

    templates = csv_rows(OUTPUTS["candidate_template"])
    checks.append(
        {
            "validation_id": "VAL1885_6_templates_nonclaim",
            "status": "PASS"
            if len(templates) == 2
            and all(bool_string(row["valid_for_claim"]) == "false" and bool_string(row["claim_allowed"]) == "false" for row in templates)
            and any("MISSING" in " ".join(row.values()).upper() for row in templates)
            else "FAIL",
            "detail": "parent-zero and finite beta vector templates remain nonclaim",
            "valid_for_claim": False,
        }
    )

    dryruns = csv_rows(OUTPUTS["dryrun_results"])
    expected_statuses = {
        "REFUSED_GAMMA_ONLY",
        "REFUSED_COMPARATOR_ONLY",
        "REFUSED_CLOSURE_OR_GR_IMPORT",
        "REFUSED_MISSING_BETA_VECTOR_COMPONENTS",
        "REFUSED_PARENT_BETA_ZERO_UNSIGNED",
        "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    checks.append(
        {
            "validation_id": "VAL1885_7_dryrun_failure_modes",
            "status": "PASS" if expected_statuses.issubset({row["validator_status"] for row in dryruns}) else "FAIL",
            "detail": f"dryrun_statuses={','.join(row['validator_status'] for row in dryruns)}",
            "valid_for_claim": False,
        }
    )

    runners = csv_rows(OUTPUTS["runner_refusal"])
    checks.append(
        {
            "validation_id": "VAL1885_8_runner_refusal",
            "status": "PASS"
            if any(row["current_status"] == "ALLOW_SCHEMA_DRYRUN_NONCLAIM" for row in runners)
            and sum(1 for row in runners if row["current_status"] == "REFUSE_CLAIM_RUN") == 2
            else "FAIL",
            "detail": "proof/local-GR claim runs refuse while schema dryrun is allowed nonclaim",
            "valid_for_claim": False,
        }
    )

    claims = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1885_9_claim_gates",
            "status": "PASS"
            if any(row["status"] == "PASS_CONDITIONAL_NONCLAIM" for row in claims)
            and sum(1 for row in claims if row["status"] == "BLOCKED") == 4
            else "FAIL",
            "detail": "EH route is conditional only; beta/source/local-GR claims blocked",
            "valid_for_claim": False,
        }
    )

    decisions = csv_rows(OUTPUTS["decision"])
    checks.append(
        {
            "validation_id": "VAL1885_10_decision",
            "status": "PASS"
            if any(row["decision"] == "NO_SOURCE_ONLY_SLOT_IS_NEXT_BEST_ATTACK" for row in decisions)
            else "FAIL",
            "detail": "decision selects common matter/source slot as next bottleneck",
            "valid_for_claim": False,
        }
    )

    next_targets = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1885_11_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1885_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1886 no-source-only-slot proof or finite w_R row selected",
            "valid_for_claim": False,
        }
    )

    status_rows = csv_rows(OUTPUTS["project_status"])
    checks.append(
        {
            "validation_id": "VAL1885_12_project_status",
            "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows) else "FAIL",
            "detail": "project status snapshot keeps source coupling as main bottleneck",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1885_13_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_statuses_not_claim_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1885_14_blocked_markers_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1885_15_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["beta_second_order_audit"].name,
        QUEUE / "JR1885_SOURCE_COUPLING_ZERO_AUDIT_NONCLAIM.csv",
        QUEUE / "JR1885_BETA_RESIDUAL_VECTOR_CONTRACT_NONCLAIM.csv",
        BETA_TEMPLATE_DOC_COPY,
        QUARANTINE / OUTPUTS["dryrun_results"].name,
    ]
    checks.append(
        {
            "validation_id": "VAL1885_16_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1885_17_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1885*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1885_18_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1885_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1885_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1885 beta second-order/source-coupling gate or parent-zero row",
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
    content = f"""# 1885 - Beta Second-Order Source-Coupling Gate Or Parent-Zero Row

**Private status:** local-GR derivation gate; no public claim.

## Result

1885 does **not** claim beta or local GR. It does something more useful: it blocks the fake win.

Gamma/q_R work can clean up the first-order reciprocal product channel, but it does not determine the second-order PPN coefficient:

```text
g_00 = -1 + 2U/c^2 - 2 beta U^2/c^4 + O(c^-6)
delta_beta = beta - 1
```

The clean route is still visible: a single parent source-normalized EH-like local action with universal matter coupling and projected conservation would give beta=1. But importing that exterior is just GR-smuggling unless MTS parent-signs the source/matter package.

So 1885 keeps two honest routes:

```text
parent_beta_zero:
  prove source-normalized beta=1 from the parent action.

finite_beta_vector:
  supply all beta residual components and compare sum(abs(component)) <= {BETA_BOUND:.2e}.
```

The live bottleneck is now source coupling: no hidden source-only/action-weight slot, common matter descent, tau role lock, and boundary/readout silence.

## Beta Second-Order Gate Audit

{markdown_table(rows_by_name["beta_second_order_audit"])}

## Source Coupling Zero Audit

{markdown_table(rows_by_name["source_coupling_audit"])}

## Beta Residual Vector Contract

{markdown_table(rows_by_name["beta_residual_contract"])}

## Candidate Template

{markdown_table(rows_by_name["candidate_template"])}

## Validator Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Validator Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

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
