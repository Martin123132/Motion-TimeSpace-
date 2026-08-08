from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3020"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5

DOC = ROOT / "3020-Y5-R2FR-second-order-parent-field-equation-coefficient-map-or-beta-square-law-rejection-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3020_00_3019_doc": ROOT / "3019-Y5-R2FR-beta-square-law-source-normalization-gate-under-AX1090.md",
    "SRC3020_01_3019_proof": RESIDUALS / "P8_Y5_R2FR_3019_BETA_SQUARE_LAW_PROOF_ATTEMPT.csv",
    "SRC3020_02_3019_contract": RESIDUALS / "P8_Y5_R2FR_3019_SECOND_ORDER_FIELD_EQUATION_CONTRACT.csv",
    "SRC3020_03_3019_queue": RESIDUALS / "P8_Y5_R2FR_3019_FIRST_COEFFICIENT_FILL_QUEUE.csv",
    "SRC3020_04_3019_next": RESIDUALS / "P8_Y5_R2FR_3019_NEXT_TARGET.csv",
    "SRC3020_05_2749_doc": ROOT / "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md",
    "SRC3020_06_2749_ansatz": RESIDUALS / "P8_Y5_R2FR_2749_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
    "SRC3020_07_2749_euler": RESIDUALS / "P8_Y5_R2FR_2749_EULER_VARIATION_GATE.csv",
    "SRC3020_08_2749_ward_ppn": RESIDUALS / "P8_Y5_R2FR_2749_WARD_PPN_GATE.csv",
    "SRC3020_09_3007_doc": ROOT / "3007-Y5-R2FR-minimal-parent-action-sector-grammar-or-sector-variation-ledger-under-AX1090.md",
    "SRC3020_10_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3020_11_3007_variations": RESIDUALS / "P8_Y5_R2FR_3007_SECTOR_VARIATION_LEDGER.csv",
    "SRC3020_12_3008_doc": ROOT / "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence-or-explicit-residual-split-under-AX1090.md",
    "SRC3020_13_3008_q_action": RESIDUALS / "P8_Y5_R2FR_3008_QLOC_ACTION_EXISTENCE_AUDIT.csv",
    "SRC3020_14_3008_coupling": RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv",
    "SRC3020_15_3009_doc": ROOT / "3009-Y5-R2FR-Gamma-Khat-metric-response-symbol-match-and-coupling-descent-guard-under-AX1090.md",
    "SRC3020_16_3009_symbol_match": RESIDUALS / "P8_Y5_R2FR_3009_REAL_SYMBOL_MATCH_AUDIT.csv",
    "SRC3020_17_3010_doc": ROOT / "3010-Y5-R2FR-first-Gamma-Khat-response-operator-row-or-q_loc-coupling-bound-interface-under-AX1090.md",
    "SRC3020_18_3010_live_gate": RESIDUALS / "P8_Y5_R2FR_3010_LIVE_RESPONSE_COMPONENT_GATE.csv",
    "SRC3020_19_2930_coefficients": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv",
    "SRC3020_20_2920_square_audit": RESIDUALS / "P8_Y5_R2FR_2920_PARENT_SQUARE_LAW_AUDIT.csv",
    "SRC3020_21_2893_beta_law": RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3020_SOURCE_REGISTER.csv",
    "lapse_map": RESIDUALS / "P8_Y5_R2FR_3020_LAPSE_COEFFICIENT_MAP.csv",
    "ownership": RESIDUALS / "P8_Y5_R2FR_3020_PARENT_ACTION_OWNERSHIP_AUDIT.csv",
    "beta_status": RESIDUALS / "P8_Y5_R2FR_3020_BETA_SQUARE_LAW_STATUS.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_3020_SECOND_ORDER_RESIDUAL_OPERATOR_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3020_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3020_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3020_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3020_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3020_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "lapse_copy": LOCAL_BOUNDS / "lapse_coefficient_map_3020_NONCLAIM.csv",
    "ownership_copy": PARENT_ACTION / "parent_action_ownership_audit_3020_NOT_SIGNED.csv",
    "status_copy": LOCAL_BOUNDS / "beta_square_law_status_3020_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3020_LOG_LAPSE_LINEARITY_OR_PARENT_OPERATOR_MAP_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3020_00_3019_doc": "3019 handoff: derive second-order coefficient map or reject beta square route",
    "SRC3020_01_3019_proof": "conditional lapse square-law route and nonclaim verdict",
    "SRC3020_02_3019_contract": "second-order field-equation contract",
    "SRC3020_03_3019_queue": "first coefficient fill queue",
    "SRC3020_04_3019_next": "machine-readable 3020 target",
    "SRC3020_05_2749_doc": "minimal parent weak-field ansatz and EH conditional comparator",
    "SRC3020_06_2749_ansatz": "candidate parent action register",
    "SRC3020_07_2749_euler": "Euler variation gate",
    "SRC3020_08_2749_ward_ppn": "Ward/PPN beta conditional rows",
    "SRC3020_09_3007_doc": "minimal parent action sector grammar",
    "SRC3020_10_3007_grammar": "sector grammar machine rows",
    "SRC3020_11_3007_variations": "sector variation ledger",
    "SRC3020_12_3008_doc": "Gamma/Khat/q_loc action existence and coupling guard",
    "SRC3020_13_3008_q_action": "q_loc action existence audit",
    "SRC3020_14_3008_coupling": "hidden matter/source coupling guard",
    "SRC3020_15_3009_doc": "live Gamma/Khat metric-response symbol match result",
    "SRC3020_16_3009_symbol_match": "machine-readable live symbol match audit",
    "SRC3020_17_3010_doc": "response operator row attempt",
    "SRC3020_18_3010_live_gate": "live response component gate",
    "SRC3020_19_2930_coefficients": "A_source/B_source coefficient ledger",
    "SRC3020_20_2920_square_audit": "parent square-law audit",
    "SRC3020_21_2893_beta_law": "source-normalized beta extraction law",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

lapse_map = [
    base(
        {
            "map_id": "LCM3020_0_generic_lapse",
            "object": "N expansion",
            "assumption_or_definition": "N=1+n1 W/c^2+n2 W^2/c^4+O(W^3)",
            "coefficient_map": "g00=-N^2=-1-2 n1 W/c^2-(2 n2+n1^2)W^2/c^4+O(W^3)",
            "derived_result": "A_source=-n1; B_source=n2+n1^2/2",
            "status": "DERIVED_ALGEBRAIC_MAP",
            "missing_for_claim": "MISSING_PARENT_VALUES_FOR_n1_n2",
        }
    ),
    base(
        {
            "map_id": "LCM3020_1_square_condition",
            "object": "beta square law",
            "assumption_or_definition": "compare B_source=n2+n1^2/2 with A_source^2=n1^2",
            "coefficient_map": "B_source=A_source^2 iff n2=n1^2/2",
            "derived_result": "beta_eff=1 iff the second-order lapse coefficient is half the square of the linear coefficient",
            "status": "EXACT_CONDITION_DERIVED",
            "missing_for_claim": "MISSING_PARENT_LAPSE_COEFFICIENT_THEOREM",
        }
    ),
    base(
        {
            "map_id": "LCM3020_2_exponential_lapse",
            "object": "exponential lapse",
            "assumption_or_definition": "N=exp(-A_source W/c^2)+O(W^3)",
            "coefficient_map": "n1=-A_source; n2=A_source^2/2",
            "derived_result": "B_source=A_source^2 and beta_eff=1",
            "status": "SUFFICIENT_ROUTE_CONFIRMED_CONDITIONAL",
            "missing_for_claim": "MISSING_PARENT_DERIVATION_OF_EXPONENTIAL_LAPSE",
        }
    ),
    base(
        {
            "map_id": "LCM3020_3_log_lapse",
            "object": "log-lapse linearity",
            "assumption_or_definition": "psi_N=-log N=A_source W/c^2+lambda_N W^2/c^4+O(W^3)",
            "coefficient_map": "N=1-A_source W/c^2+(A_source^2/2-lambda_N)W^2/c^4; beta_eff=1-lambda_N/A_source^2",
            "derived_result": "B_source=A_source^2 iff lambda_N=0 in the same source-normalized branch",
            "status": "SHARPEST_PARENT_THEOREM_TARGET",
            "missing_for_claim": "MISSING_PARENT_LOG_LAPSE_LINEARITY_THEOREM",
        }
    ),
    base(
        {
            "map_id": "LCM3020_4_residual_formula",
            "object": "delta_beta_source",
            "assumption_or_definition": "allow independent quadratic log-lapse/source residual lambda_N and extra Delta_B_extra",
            "coefficient_map": "delta_beta_source=(B_source/A_source^2)-1=-(lambda_N/A_source^2)+Delta_B_extra/A_source^2",
            "derived_result": "beta residual is the independent quadratic log-lapse plus extra-sector coefficient, not a first-order GM effect",
            "status": "RESIDUAL_FORMULA_READY_NONCLAIM",
            "missing_for_claim": "MISSING_lambda_N_VALUE; MISSING_DELTA_B_EXTRA_VALUE",
        }
    ),
    base(
        {
            "map_id": "LCM3020_5_verdict",
            "object": "parent coefficient map",
            "assumption_or_definition": "current corpus must provide n1/n2 or psi_N field equation from parent action",
            "coefficient_map": "not present in signed MTS parent action",
            "derived_result": "coefficient algebra is solved; parent ownership is not",
            "status": "MAP_DERIVED_PARENT_VALUES_MISSING",
            "missing_for_claim": "MISSING_SECOND_ORDER_PARENT_FIELD_EQUATION",
        }
    ),
]

ownership_audit = [
    base(
        {
            "audit_id": "OWN3020_0_EH_control",
            "source_object": "EH weak-field core",
            "what_it_would_prove": "standard local GR weak-field beta=1",
            "current_status": "CONDITIONAL_CONTROL_NOT_MTS_ADOPTION",
            "evidence": "2749 says EH core conditionally gives beta=1 but cannot be imported as MTS proof",
            "missing_for_claim": "MISSING_EH_BLOCK_MATCH_TO_MTS_PRIMITIVES; MISSING_SOURCE_READOUT_OWNERSHIP",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_1_parent_grammar",
            "source_object": "3007 total parent action grammar",
            "what_it_would_prove": "single varied parent action with sector stresses and theta/Q_tau pieces",
            "current_status": "GRAMMAR_READY_NOT_SIGNED",
            "evidence": "3007 stages S_parent^loc grammar but marks sector first-variation certificates missing",
            "missing_for_claim": "MISSING_SINGLE_PARENT_ACTION; MISSING_SECTOR_VARIATION_CERTIFICATES",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_2_A_source",
            "source_object": "linear coefficient map",
            "what_it_would_prove": "first-order Newton denominator from parent source density",
            "current_status": "MISSING_PARENT_LINEAR_COEFFICIENT_MAP",
            "evidence": "2930 coefficient ledger keeps A_source unfilled",
            "missing_for_claim": "MISSING_HCORE_SOURCE_DENSITY; MISSING_POSITIVE_MHREF; MISSING_NO_ORBITAL_GM_IMPORT",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_3_B_source",
            "source_object": "second-order coefficient map",
            "what_it_would_prove": "beta numerator in the same source-normalized family",
            "current_status": "MISSING_PARENT_SECOND_ORDER_COEFFICIENT_MAP",
            "evidence": "2930 coefficient ledger and 3019 contract keep B_source unfilled",
            "missing_for_claim": "MISSING_PARENT_SECOND_ORDER_FIELD_EQUATION",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_4_log_lapse_linearity",
            "source_object": "lambda_N=0 theorem",
            "what_it_would_prove": "B_source=A_source^2 without importing Schwarzschild",
            "current_status": "NEW_TARGET_NOT_PARENT_SIGNED",
            "evidence": "3020 algebra identifies the target, but no source file signs the parent equation",
            "missing_for_claim": "MISSING_PARENT_LOG_LAPSE_LINEARITY_OR_HAMILTONIAN_CONSTRAINT_PROOF",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_5_Gamma_Khat_operator",
            "source_object": "extra local Gamma/Khat/q_loc sector",
            "what_it_would_prove": "extra sector does not shift beta through O(W^2)",
            "current_status": "NOT_LIVE_RESPONSE_OPERATOR",
            "evidence": "3008-3010 keep action existence, live Khat metric response, and units/source normalization open",
            "missing_for_claim": "MISSING_LIVE_GAMMA_KHAT_RESPONSE_COMPONENT; MISSING_DELTAK_ZERO_OR_BOUND",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_6_coupling_guard",
            "source_object": "hidden matter/source coupling",
            "what_it_would_prove": "no source-prefactor/non-Hilbert/kappa/ell_J leakage into beta",
            "current_status": "COUPLING_GUARD_NOT_CLOSED",
            "evidence": "3007/3008/3009 keep coupling descent and source bridge unsigned",
            "missing_for_claim": "MISSING_MATTER_DESCENT; MISSING_CONSTANT_KAPPA; MISSING_CONSTANT_ELLJ; MISSING_SOURCE_BRIDGE",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_7_readout",
            "source_object": "fixed-before-readout PPN gauge",
            "what_it_would_prove": "beta comparison is not a coordinate/source calibration artifact",
            "current_status": "MISSING_READOUT_TRANSFER_THROUGH_O_U2",
            "evidence": "2574/2896/3019 keep readout through O(U^2) missing",
            "missing_for_claim": "MISSING_OBSERVED_COFRAME_TO_PPN_GAUGE_MAP",
        }
    ),
    base(
        {
            "audit_id": "OWN3020_8_verdict",
            "source_object": "MTS parent beta square-law ownership",
            "what_it_would_prove": "local beta=1 as a derivation",
            "current_status": "PARENT_OWNERSHIP_NOT_SIGNED",
            "evidence": "coefficient algebra passes; parent action ownership fails closed",
            "missing_for_claim": "MISSING_PARENT_FIELD_EQUATION_MAP_AND_ALL_SILENCE_GUARDS",
        }
    ),
]

beta_status = [
    base(
        {
            "status_id": "BSS3020_0_extraction",
            "object": "beta_eff",
            "statement": "beta_eff=B_source/A_source^2",
            "status": "DERIVED_KINEMATIC_GRAMMAR",
            "claim_allowed_now": False,
            "reason": "grammar is not a prediction until coefficients are parent-owned",
        }
    ),
    base(
        {
            "status_id": "BSS3020_1_square_condition",
            "object": "B_source=A_source^2",
            "statement": "equivalent to n2=n1^2/2 or lambda_N=0 in the same source-normalized branch",
            "status": "EXACT_TARGET_DERIVED",
            "claim_allowed_now": False,
            "reason": "target is unsigned by parent field equation",
        }
    ),
    base(
        {
            "status_id": "BSS3020_2_route_rejection",
            "object": "beta square-law route",
            "statement": "not rejected mathematically; rejected as a current claim",
            "status": "ROUTE_RETAINED_CONDITIONAL_CLAIM_REJECTED",
            "claim_allowed_now": False,
            "reason": "clean sufficient mechanism exists, but MTS parent does not yet own it",
        }
    ),
    base(
        {
            "status_id": "BSS3020_3_local_GR",
            "object": "local GR/Newton reduction",
            "statement": "gamma, beta, alpha3, source bridge and readout must close together",
            "status": "NOT_CLAIMABLE",
            "claim_allowed_now": False,
            "reason": "beta square-law alone is insufficient and not signed anyway",
        }
    ),
]

residual_ledger = [
    base(
        {
            "residual_id": "SOR3020_0_lambda_N",
            "symbol": "lambda_N",
            "definition": "independent quadratic log-lapse coefficient in psi_N=-log N",
            "beta_projection": "-lambda_N/A_source^2",
            "current_status": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM",
            "needed_for_score": "lambda_N=0 theorem or source-backed value",
            "beta_bound_abs": BETA_BOUND_ABS,
        }
    ),
    base(
        {
            "residual_id": "SOR3020_1_DeltaB_operator",
            "symbol": "Delta_B_operator",
            "definition": "R11/R2/fR/scalar/vector/tensor/auxiliary operator contribution to B_source",
            "beta_projection": "Delta_B_operator/A_source^2",
            "current_status": "MISSING_OPERATOR_NOHAIR_OR_COEFFICIENT",
            "needed_for_score": "zero theorem or finite operator coefficient rows",
            "beta_bound_abs": BETA_BOUND_ABS,
        }
    ),
    base(
        {
            "residual_id": "SOR3020_2_DeltaK_q_loc",
            "symbol": "Delta_K_beta",
            "definition": "Gamma/Khat metric-response mismatch projected into second-order beta",
            "beta_projection": "K_beta[Delta_K]/A_source^2",
            "current_status": "MISSING_LIVE_RESPONSE_COMPONENT",
            "needed_for_score": "live Khat=K_metric certificate or bound interface values",
            "beta_bound_abs": BETA_BOUND_ABS,
        }
    ),
    base(
        {
            "residual_id": "SOR3020_3_source_current_coupling",
            "symbol": "Delta_B_source_current",
            "definition": "kappa_MTS, ell_J, source-prefactor/non-Hilbert current leakage through O(W^2)",
            "beta_projection": "Delta_B_source_current/A_source^2",
            "current_status": "MISSING_COUPLING_DESCENT",
            "needed_for_score": "matter/source descent and constant coupling/source-current owner",
            "beta_bound_abs": BETA_BOUND_ABS,
        }
    ),
    base(
        {
            "residual_id": "SOR3020_4_readout",
            "symbol": "Delta_B_readout",
            "definition": "second-order observed coframe and PPN gauge transfer residual",
            "beta_projection": "Delta_B_readout/A_source^2",
            "current_status": "MISSING_READOUT_OU2_MAP",
            "needed_for_score": "fixed-before-readout theorem through O(U^2)",
            "beta_bound_abs": BETA_BOUND_ABS,
        }
    ),
    base(
        {
            "residual_id": "SOR3020_5_denominator",
            "symbol": "epsilon_SN",
            "definition": "source-normalized Newton denominator mismatch",
            "beta_projection": "explicit no-absorption guard",
            "current_status": "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD",
            "needed_for_score": "mu_obs=G_eff M_H in same source frame without circular GM fit",
            "beta_bound_abs": BETA_BOUND_ABS,
        }
    ),
    base(
        {
            "residual_id": "SOR3020_6_total",
            "symbol": "Delta_beta_total_abs",
            "definition": "absolute no-cancellation beta envelope",
            "beta_projection": "sum_abs(lambda_N/A_source^2, Delta_B_operator/A_source^2, Delta_K_beta, source_current, readout, epsilon_SN)",
            "current_status": "TOTAL_NOT_SCORE_READY",
            "needed_for_score": "every component theorem-zero or source-backed bounded",
            "beta_bound_abs": BETA_BOUND_ABS,
        }
    ),
]

promotion_gates = [
    base({"gate_id": "GATE3020_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed audit"}),
    base({"gate_id": "GATE3020_1_lapse_map", "gate": "generic second-order lapse coefficient map derived", "result": True, "notes": "A_source=-n1 and B_source=n2+n1^2/2"}),
    base({"gate_id": "GATE3020_2_square_condition", "gate": "exact square-law condition identified", "result": True, "notes": "n2=n1^2/2 or lambda_N=0"}),
    base({"gate_id": "GATE3020_3_parent_values", "gate": "MTS parent supplies n1/n2 or lambda_N equation", "result": False, "notes": "parent field-equation map is not signed"}),
    base({"gate_id": "GATE3020_4_beta_score", "gate": "MTS beta can be scored against comparator", "result": False, "notes": "parent values and residual components missing"}),
    base({"gate_id": "GATE3020_5_local_GR_claim", "gate": "local GR/Newton limit claimable", "result": False, "notes": "gamma coefficients, beta parent ownership, alpha3/current and readout/source bridge remain incomplete"}),
]

decision = [
    base(
        {
            "decision_id": "DEC3020_0_coefficient_map",
            "decision": "derive the generic lapse-to-beta coefficient map",
            "rationale": "it isolates the exact second-order condition needed for beta=1",
            "consequence": "future work can target log-lapse linearity rather than vague Schwarzschild matching",
        }
    ),
    base(
        {
            "decision_id": "DEC3020_1_route_status",
            "decision": "retain the beta square-law route as conditional but reject it as a current claim",
            "rationale": "a clean mechanism exists, but current MTS does not parent-sign the lapse normal form",
            "consequence": "no beta/PPN/Newton/local-GR promotion",
        }
    ),
    base(
        {
            "decision_id": "DEC3020_2_next",
            "decision": "select log-lapse linearity or parent operator map as 3021",
            "rationale": "lambda_N=0 is the minimal theorem that would prove B_source=A_source^2 without importing EH",
            "consequence": "3021 should try to derive psi_N=-log N as a single linear source potential through O(W^2)",
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3020_0_3021",
            "target_doc": "3021-Y5-R2FR-log-lapse-linearity-theorem-or-parent-operator-residual-map-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_log_lapse_linearity_theorem_or_parent_operator_residual_map_under_AX1090_3021.py",
            "mission": "try to derive lambda_N=0 from the parent Hamiltonian/field-equation normal form; if absent, map lambda_N and extra operator/source/readout pieces as explicit beta residuals",
            "success_condition": "either parent action signs psi_N=-log N=A_source W/c^2+O(W^3), or lambda_N and all second-order parent residuals remain explicit nonclaim rows",
            "forbidden": "no Schwarzschild/EH import as MTS proof; no measured-GM shortcut; no gamma-only pass; no hidden cancellation; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["lapse_map"], lapse_map)
write_csv(OUTPUTS["ownership"], ownership_audit)
write_csv(OUTPUTS["beta_status"], beta_status)
write_csv(OUTPUTS["residuals"], residual_ledger)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("lapse_copy", "lapse_map"),
    ("ownership_copy", "ownership"),
    ("status_copy", "beta_status"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3020_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = source_register + lapse_map + ownership_audit + beta_status + residual_ledger + promotion_gates + decision + next_target

validation_rows = [
    {"validation_id": "VAL3020_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3020_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3020_02_lapse_map_derivation", "passed": any(row["map_id"] == "LCM3020_0_generic_lapse" and "A_source=-n1" in row["derived_result"] for row in lapse_map), "requirement": "generic lapse-to-A/B coefficient map is recorded", "evidence": OUTPUTS["lapse_map"].name},
    {"validation_id": "VAL3020_03_square_condition", "passed": any(row["map_id"] == "LCM3020_1_square_condition" and "n2=n1^2/2" in row["coefficient_map"] for row in lapse_map), "requirement": "exact beta square-law condition is recorded", "evidence": OUTPUTS["lapse_map"].name},
    {"validation_id": "VAL3020_04_log_lapse_target", "passed": any(row["map_id"] == "LCM3020_3_log_lapse" and "lambda_N=0" in row["derived_result"] for row in lapse_map), "requirement": "log-lapse linearity target is recorded", "evidence": OUTPUTS["lapse_map"].name},
    {"validation_id": "VAL3020_05_parent_not_signed", "passed": any(row["audit_id"] == "OWN3020_8_verdict" and row["current_status"] == "PARENT_OWNERSHIP_NOT_SIGNED" for row in ownership_audit) and any(row["gate_id"] == "GATE3020_3_parent_values" and not boolish(row["result"]) for row in promotion_gates), "requirement": "coefficient map is not promoted to parent-signed MTS proof", "evidence": f"{OUTPUTS['ownership'].name}; {OUTPUTS['gates'].name}"},
    {"validation_id": "VAL3020_06_residual_ledger_present", "passed": any(row["symbol"] == "lambda_N" for row in residual_ledger) and any(row["symbol"] == "Delta_beta_total_abs" for row in residual_ledger), "requirement": "second-order residual ledger includes lambda_N and no-cancellation total", "evidence": OUTPUTS["residuals"].name},
    {"validation_id": "VAL3020_07_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3020 generated ledgers"},
    {"validation_id": "VAL3020_08_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3020 generated ledgers"},
    {"validation_id": "VAL3020_09_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3020_10_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3020_11_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3020_12_next_target_selected", "passed": next_target[0]["target_doc"].startswith("3021-Y5-R2FR-log-lapse-linearity"), "requirement": "next target selects log-lapse linearity theorem or parent residual map", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3020_99_overall",
        "passed": overall_pass,
        "requirement": "all 3020 validation checks pass",
        "evidence": "aggregate of VAL3020_00 through VAL3020_12",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3020 - Second-Order Parent Field-Equation Coefficient Map Or Beta Square-Law Rejection under AX1090

Status: `Y5_R2FR_3020_lapse_coefficient_map_derived_parent_values_missing_log_lapse_next`

## Verdict

3020 makes the beta lock more exact.

Write the local observed lapse as

`N=1+n1 W/c^2+n2 W^2/c^4+O(W^3)`.

Then

`g00=-N^2=-1-2 n1 W/c^2-(2 n2+n1^2)W^2/c^4+O(W^3)`.

Comparing with

`g00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(W^3)`

gives the coefficient map

`A_source=-n1`, and `B_source=n2+n1^2/2`.

So the beta square law

`B_source=A_source^2`

is equivalent to

`n2=n1^2/2`.

Equivalently, if

`psi_N=-log N=A_source W/c^2+lambda_N W^2/c^4+O(W^3)`,

then

`beta_eff=1-lambda_N/A_source^2` up to the retained extra-sector residuals.

Thus the sharp theorem target is now:

`lambda_N=0`, i.e. no independent quadratic log-lapse term in the same source-normalized branch.

That is a genuine derivation gain. But current MTS does not yet parent-sign the lapse equation, the `n1/n2` coefficient values, the source denominator, the extra-sector no-hair map, or the readout/source-current guards. Therefore 3020 rejects the beta square law as a current claim, while retaining it as a precise route.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Lapse Coefficient Map

{md_table(lapse_map, ["map_id", "object", "assumption_or_definition", "coefficient_map", "derived_result", "status", "missing_for_claim"])}

## Parent Action Ownership Audit

{md_table(ownership_audit, ["audit_id", "source_object", "what_it_would_prove", "current_status", "evidence", "missing_for_claim"])}

## Beta Square-Law Status

{md_table(beta_status, ["status_id", "object", "statement", "status", "claim_allowed_now", "reason"])}

## Second-Order Residual Operator Ledger

{md_table(residual_ledger, ["residual_id", "symbol", "definition", "beta_projection", "current_status", "needed_for_score"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "target_script", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["lapse_map"]}`
- `{OUTPUTS["ownership"]}`
- `{OUTPUTS["beta_status"]}`
- `{OUTPUTS["residuals"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["lapse_copy"]}`
- `{BRANCH_OUTPUTS["ownership_copy"]}`
- `{BRANCH_OUTPUTS["status_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass without parent-signed `lambda_N=0` or source-backed finite residuals below the comparator.
- No EH/Schwarzschild import as MTS proof.
- No measured-`GM` absorption shortcut.
- No gamma-only local-GR or PPN pass.
- No hidden cancellation across residual families.
- No `alpha3` pass without source-current/no-flux theorem-zero or an ultratight bound.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
