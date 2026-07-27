from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2706"
BRANCH_ID = "Y5_R2FR_CX_ZERO_FACTOR_PROOF_OR_FIRST_PARENT_COEFFICIENT_ROW_2706"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2706-Y5-R2FR-CX-zero-factor-proof-or-first-parent-coefficient-row.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2706_SOURCE_REGISTER.csv",
    "zero_factor_audit": RESIDUALS / "P8_Y5_R2FR_2706_CX_ZERO_FACTOR_PROOF_AUDIT.csv",
    "coefficient_hunt": RESIDUALS / "P8_Y5_R2FR_2706_PARENT_COEFFICIENT_ROW_HUNT.csv",
    "product_gate": RESIDUALS / "P8_Y5_R2FR_2706_CX_PRODUCT_GATE.csv",
    "first_coefficient_contract": RESIDUALS / "P8_Y5_R2FR_2706_FIRST_COEFFICIENT_INPUT_CONTRACT_NONCLAIM.csv",
    "blocker_ledger": RESIDUALS / "P8_Y5_R2FR_2706_BLOCKER_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2706_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2706_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2706_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2706_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2706_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_zero_factor_audit": LOCAL_BOUNDS / "C_X_zero_factor_proof_audit_2706_NONCLAIM.csv",
    "local_first_contract": LOCAL_BOUNDS / "R10_alpha_lambda_MTS_CX_FIRST_COEFFICIENT_CONTRACT_2706_NONCLAIM.csv",
    "source_weight_contract": SOURCE_WEIGHT / "CX_FIRST_COEFFICIENT_CONTRACT_2706_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2706_PARENT_ACTION_COEFFICIENT_OWNER_EXTRACTION_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2706_2705_RESULT",
        "relative_path": "2705-Y5-R2FR-q-loc-Yukawa-kernel-coefficients-or-zero-theorem.md",
        "required_needles": ["CL2705_4_alpha_coefficient", "ZF2705_3_qbar_XT_zero", "NEXT2705_0_selected"],
        "purpose": "imports the product law and selected 2706 task",
    },
    {
        "source_id": "SRC2706_562_FORMULA",
        "relative_path": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
        "required_needles": ["PR562_2_canonical_mass_and_range", "PR562_4_prefactor", "PR562_5_positive_operator_identity"],
        "purpose": "imports lambda, K_X and no-hair identities",
    },
    {
        "source_id": "SRC2706_2106_EXTRACTION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2106_EXTRACTION_MATRIX.csv",
        "required_needles": ["EXM2106_0_ZX", "MISSING_ZX", "EXM2106_1_MX2", "MISSING_MX2"],
        "purpose": "checks whether Z_X or M_X^2 have become parent-owned",
    },
    {
        "source_id": "SRC2706_2663_CHARGE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_CHARGE_NORMALIZATION_2663_CHARGE_DERIVATION.csv",
        "required_needles": ["CHG2663_3_KX_prefactor", "CHG2663_4_test_response", "CHG2663_7_verdict"],
        "purpose": "imports the exact source/test charge normalization contract",
    },
    {
        "source_id": "SRC2706_2663_KX_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_CHARGE_NORMALIZATION_2663_KX_NORMALIZATION_GATE.csv",
        "required_needles": ["KX2663_0_ZX", "KX2663_1_sign", "KX2663_5_verdict"],
        "purpose": "checks K_X inputs Z_X, s_X and frame normalization",
    },
    {
        "source_id": "SRC2706_2664_QBAR_ROW",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv",
        "required_needles": ["QXH2664_0_bulk_source_current", "QXH2664_3_projected_Qbar", "QXH2664_5_alpha_feed"],
        "purpose": "imports the source-side Qbar_XH coefficient contract",
    },
    {
        "source_id": "SRC2706_2664_QBAR_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_INPUT_GATE.csv",
        "required_needles": ["QG2664_0_parent_rhoX", "MISSING_PARENT_SOURCE_CURRENT", "QG2664_2_PiM"],
        "purpose": "checks why Qbar_XH is not numeric or zero",
    },
    {
        "source_id": "SRC2706_1044_PULLBACK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
        "required_needles": ["MPD1044_7_exact_theorem_if_signed", "qbar_XT=0", "MPD1044_8_current_verdict"],
        "purpose": "imports the strongest qbar_XT zero theorem currently available",
    },
    {
        "source_id": "SRC2706_1045_FUNCTOR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "required_needles": ["MFS1045_0_parent_field_quotient", "MFS1045_5_constants_split", "MFS1045_6_verdict"],
        "purpose": "checks whether the parent ordinary-matter functor signs qbar_XT zero",
    },
    {
        "source_id": "SRC2706_1045_QBAR_GEOM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv",
        "required_needles": ["QG1045_1_functor_chain_rule", "QG1045_3_shadow_countermodel", "QG1045_4_current_verdict"],
        "purpose": "imports the chain-rule qbar_geom zero attempt and countermodel",
    },
    {
        "source_id": "SRC2706_573_QBAR_CERT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_573_QBAR_XT_CERTIFICATE_STATUS.csv",
        "required_needles": ["QXC573_4_result", "conditional_only_not_parent_derived"],
        "purpose": "confirms the qbar_XT zero certificate remains blocked",
    },
    {
        "source_id": "SRC2706_575_QBAR_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_575_QBAR_XT_GATE.csv",
        "required_needles": ["QG575_4_result", "finite qbar_XT retained"],
        "purpose": "confirms the finite qbar_XT branch remains active",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def zero_factor_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ZPA2706_0_no_active_pole",
            "candidate_zero_factor": "no physical X pole",
            "would_zero_CX_because": "if X is gauge/topological or absent from the local Hilbert spectrum, lambda_X and alpha_X are not physical observables",
            "strongest_current_evidence": "2705 names no-active-pole fork; 2581 q_loc zero package remains unsigned",
            "missing_parent_clause": "degree count plus vertical-generator action signature showing no local propagating X mode",
            "countermodel_or_risk": "a massive scalar/vector representative with a source current gives a finite Yukawa tail",
            "proof_status": "FAIL_NO_PARENT_DEGREE_SIGNATURE",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ZPA2706_1_sX_zero",
            "candidate_zero_factor": "s_X=0",
            "would_zero_CX_because": "C_X=s_X Qbar_XH qbar_XT/(4*pi*Z_X*G_obs)",
            "strongest_current_evidence": "2663 fixes K_X=s_X/(4*pi*Z_X*G_obs) as the correct normalization gate",
            "missing_parent_clause": "parent variation proving the physical local readout/force channel is independent of X at first order",
            "countermodel_or_risk": "any nonzero readout vertex or representative metric leakage makes s_X finite",
            "proof_status": "FAIL_SX_UNSIGNED",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ZPA2706_2_Qbar_XH_zero",
            "candidate_zero_factor": "Qbar_XH(lambda_X)=0",
            "would_zero_CX_because": "a source body with zero X monopole/form-factor charge cannot source the local Yukawa tail",
            "strongest_current_evidence": "2664 stages Qbar_XH as bulk + edge + shadow projected charge over M_H_ref",
            "missing_parent_clause": "rho_X=0 or source integral zero, Pi_M^H lock, M_H_ref lock, and boundary/edge no-flux in the same branch",
            "countermodel_or_risk": "compact source inner boundary can encode Q_X^H even when the exterior operator is positive",
            "proof_status": "FAIL_SOURCE_CURRENT_BOUNDARY_UNSIGNED",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ZPA2706_3_qbar_XT_zero",
            "candidate_zero_factor": "qbar_XT=0",
            "would_zero_CX_because": "ordinary test matter would not respond to X if its action descends entirely through X-blind observed geometry and fixed constants",
            "strongest_current_evidence": "1044 proves the conditional chain-rule theorem; 1045 narrows the functor and vertical lift gates",
            "missing_parent_clause": "single parent action signing observed coframe functor, matter bundle/lift, no shadow frame, constant superselection, and boundary silence",
            "countermodel_or_risk": "universal conformal/disformal shadow frame or material marker makes qbar_XT nonzero without visibly breaking covariance",
            "proof_status": "CONDITIONAL_THEOREM_STRONG_NOT_PARENT_SIGNED",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ZPA2706_4_positive_nohair",
            "candidate_zero_factor": "positive no-hair source-free branch",
            "would_zero_CX_because": "Z_X>0, M_X^2>0, J_X=0 and zero boundary flux force X=0 by the positive-operator identity",
            "strongest_current_evidence": "562 writes the exact identity and all missing premises",
            "missing_parent_clause": "Z_X>0, M_X^2>0, J_X=0, boundary flux=0, regularity and decay simultaneously",
            "countermodel_or_risk": "positive mass gap alone gives a decaying fifth-force profile rather than silence",
            "proof_status": "FAIL_NOHAIR_PREMISES_UNSIGNED",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "ZPA2706_5_product_verdict",
            "candidate_zero_factor": "C_X product zero",
            "would_zero_CX_because": "C_X=0 follows if no active X pole, s_X=0, Qbar_XH=0, or qbar_XT=0 is parent-signed",
            "strongest_current_evidence": "2705 product law is exact and all zero routes are named",
            "missing_parent_clause": "at least one signed zero factor or a no-active-pole theorem",
            "countermodel_or_risk": "finite factors produce a testable but currently unbounded R10/PPN/clock/orbital residual",
            "proof_status": "FAIL_NO_ZERO_FACTOR_SIGNED",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def coefficient_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "COEF2706_0_ZX",
            "quantity": "Z_X",
            "role_in_CX": "kinetic residue and K_X denominator",
            "best_local_source": "P8_Y5_PARENT_QLOC_2106_EXTRACTION_MATRIX.csv::EXM2106_0_ZX; P8_Y5_R10_CHARGE_NORMALIZATION_2663_KX_NORMALIZATION_GATE.csv::KX2663_0_ZX",
            "current_value": "MISSING_ZX",
            "units": "parent_X_gradient_units_required",
            "source_backed_contract": "true",
            "numeric_ready": "false",
            "no_cancellation_guard": "field rescaling must lock Z_X f_X^2 before alpha promotion",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "COEF2706_1_MX2",
            "quantity": "M_X^2",
            "role_in_CX": "finite range lambda_X=sqrt(Z_X/M_X^2)",
            "best_local_source": "P8_Y5_PARENT_QLOC_2106_EXTRACTION_MATRIX.csv::EXM2106_1_MX2; 562::PR562_2",
            "current_value": "MISSING_MX2",
            "units": "parent_X_mass_hessian_units_required",
            "source_backed_contract": "true",
            "numeric_ready": "false",
            "no_cancellation_guard": "range cannot be fitted independently of Z_X normalization",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "COEF2706_2_sX",
            "quantity": "s_X",
            "role_in_CX": "readout/force sign and coupling numerator",
            "best_local_source": "P8_Y5_R10_CHARGE_NORMALIZATION_2663_KX_NORMALIZATION_GATE.csv::KX2663_1_sign",
            "current_value": "MISSING_SIGN_CONVENTION",
            "units": "readout_coupling_units_required",
            "source_backed_contract": "true",
            "numeric_ready": "false",
            "no_cancellation_guard": "s_X=0 requires a theorem, not a preferred gauge convention",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "COEF2706_3_Qbar_XH",
            "quantity": "Qbar_XH(lambda_X)",
            "role_in_CX": "source-body X charge per Hamiltonian mass",
            "best_local_source": "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv::QXH2664_3_projected_Qbar",
            "current_value": "MISSING_ARENA_PROJECTION",
            "units": "parent_X_charge_per_Hamiltonian_mass",
            "source_backed_contract": "true",
            "numeric_ready": "false",
            "no_cancellation_guard": "bulk, edge and shadow source terms must be separately zeroed or bounded",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "COEF2706_4_qbar_XT",
            "quantity": "qbar_XT",
            "role_in_CX": "ordinary test-body X response",
            "best_local_source": "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv::MPD1044_7; P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv::QG1045_4",
            "current_value": "FINITE_BRANCH_RETAINED_ZERO_NOT_SIGNED",
            "units": "dimensionless_after_mass_normalization",
            "source_backed_contract": "true",
            "numeric_ready": "false",
            "no_cancellation_guard": "geometry, constants, marker, source-weight and non-Hilbert pieces need an absolute envelope",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "COEF2706_5_tau_R10",
            "quantity": "tau_R10(lambda,geometry)",
            "role_in_CX": "maps source/test coefficient into the R10 apparatus convention",
            "best_local_source": "P8_Y5_NO_SOURCE_PREFACTOR_2645_PROJECTION_REQUIREMENTS.csv::PRJ2645_2_R10",
            "current_value": "MISSING_TAU_R10_K_QBAR_LAMBDA_PROJECTION",
            "units": "dimensionless_geometry_projection",
            "source_backed_contract": "true",
            "numeric_ready": "false",
            "no_cancellation_guard": "tau cannot be set to one unless geometry/source normalization is derived",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def product_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CPG2706_0_exact_product",
            "statement": "C_X=s_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
            "result": "EXACT_CONDITIONAL_PRODUCT_LAW",
            "claim_effect": "formula can be cited as a contract, not as a numeric prediction",
            "gate_pass": "true",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CPG2706_1_zero_proof",
            "statement": "C_X=0 iff one parent-signed zero factor or no-active-pole theorem closes",
            "result": "BLOCKED_NO_ZERO_FACTOR_SIGNED",
            "claim_effect": "no local-GR/R10 silence claim",
            "gate_pass": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CPG2706_2_finite_prediction",
            "statement": "finite C_X is score-ready only if Z_X, M_X^2, s_X, Qbar_XH, qbar_XT and tau_R10 are numeric/source-backed",
            "result": "BLOCKED_NO_NUMERIC_PARENT_ROW",
            "claim_effect": "do not run R10 comparator as evidence",
            "gate_pass": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CPG2706_3_first_contract",
            "statement": "Qbar_XH has the most concrete first coefficient contract: projected bulk+edge+shadow source charge over M_H_ref",
            "result": "CONTRACT_SELECTED_NOT_NUMERIC",
            "claim_effect": "2707 should extract parent action/source-current owner rather than fit alpha",
            "gate_pass": "true",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def first_coefficient_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "FCC2706_0_selected_Qbar_XH",
            "selected_quantity": "Qbar_XH(lambda_X)",
            "reason_selected": "it is the most concrete finite coefficient slot already split into bulk, edge, shadow, projector and denominator pieces",
            "contract_formula": "Qbar_XH(lambda)=Pi_M^H[ integral_{Sigma_H cap W_source} W_lambda rho_X dV_H + Q_edge_X^H(lambda) + Q_shadow_X^H(lambda) ] / M_H_ref",
            "required_parent_inputs": "rho_X; Sigma_H; W_source; W_lambda; dV_H; Q_edge; Q_shadow; Pi_M^H; M_H_ref; units; source paths",
            "current_status": "FIRST_COEFFICIENT_CONTRACT_SELECTED_NOT_NUMERIC",
            "source_path": str(RESIDUALS / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv"),
            "numeric_value": "MISSING_PARENT_SOURCE_CURRENT_AND_ARENA_PROJECTION",
            "units": "parent_X_charge_per_Hamiltonian_mass",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "FCC2706_1_zero_alternative",
            "selected_quantity": "Qbar_XH(lambda_X)=0",
            "reason_selected": "same source contract supplies the clean zero route if every source component and boundary flux vanishes",
            "contract_formula": "rho_X=0 and Q_edge_X=0 and Q_shadow_X=0 and no boundary flux imply Qbar_XH=0",
            "required_parent_inputs": "source-current theorem; boundary no-flux; no shadow source; projector silence; regular compact-source domain",
            "current_status": "ZERO_ALTERNATIVE_BLOCKED_UNSIGNED",
            "source_path": str(RESIDUALS / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_INPUT_GATE.csv"),
            "numeric_value": "not_applicable_until_zero_theorem_signed",
            "units": "zero_factor",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2706_0_no_signed_zero",
            "blocker": "no C_X zero factor is parent-signed",
            "effect": "local vacuum silence remains a conditional theorem, not a proof",
            "next_action": "extract parent action ownership of X/source-current/matter functor",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2706_1_no_numeric_parent_row",
            "blocker": "Z_X, M_X^2, s_X, Qbar_XH and qbar_XT remain nonnumeric or unsigned",
            "effect": "finite local branch cannot be scored against R10/PPN/clocks/orbits",
            "next_action": "derive one coefficient from the parent action before any new comparator run",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2706_2_shadow_countermodel",
            "blocker": "a conformal/disformal or material-marker shadow frame remains a countermodel to qbar_XT=0",
            "effect": "ordinary matter descent cannot be promoted from covariance alone",
            "next_action": "make no-shadow/no-marker terms explicit in the parent action or retain finite bounds",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2706_3_source_boundary",
            "blocker": "source-current and boundary flux are not both zero-proved",
            "effect": "positive operator/no-hair identity does not remove a compact-source Yukawa charge",
            "next_action": "derive source-current owner and boundary charge formula together",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2706_0_contract",
            "gate": "C_X product and first Qbar_XH contract may be cited internally",
            "status": "PASS_NONCLAIM_CONTRACT",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "contract is exact enough to guide derivation but contains missing parent inputs",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2706_1_zero_factor",
            "gate": "C_X=0 theorem-zero",
            "status": "BLOCKED_NO_ZERO_FACTOR_SIGNED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "no active-pole, s_X, Qbar_XH, qbar_XT and no-hair routes all retain unsigned clauses",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2706_2_numeric_alpha",
            "gate": "numeric alpha_X(lambda_X) row",
            "status": "BLOCKED_NO_NUMERIC_PARENT_COEFFICIENT",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "first coefficient contract is not a value",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2706_3_local_GR",
            "gate": "local GR/Newton recovery from q_loc silence",
            "status": "BLOCKED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "finite residual or exact zero remains unresolved",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2706_4_private",
            "gate": "GitHub/public action",
            "status": "PRIVATE_NO_ACTION",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "private checkpoint only",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2706_0_zero_attempt",
            "decision": "ZERO_PROOF_NOT_CLOSED",
            "rationale": "the qbar_XT route is mathematically strong but still depends on a parent-signed matter functor/no-shadow/no-marker stack",
            "next_action": "do not assert a local-vacuum plateau; keep the zero theorem as a parent-action contract",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2706_1_first_contract",
            "decision": "QBAR_XH_SELECTED_AS_FIRST_COEFFICIENT_CONTRACT",
            "rationale": "Qbar_XH is the cleanest source-side coefficient because it forces source current, edge, shadow, projector and mass denominator into one row",
            "next_action": "extract parent action source-current owner or zero theorem for Qbar_XH",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2706_2_best_route",
            "decision": "MOVE_UPSTREAM_TO_PARENT_ACTION_OWNER_EXTRACTION",
            "rationale": "R10/data cannot decide anything until at least one C_X factor is derived or numerically sourced",
            "next_action": "2707 should target the parent action field owner and coefficient extraction, not another comparator",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2706_0_selected",
            "selection": "selected_primary",
            "target_doc": "2707-Y5-R2FR-parent-action-coefficient-owner-extraction.md",
            "target_script": "scripts/Y5_R2FR_parent_action_coefficient_owner_extraction_2707.py",
            "task": "extract a parent-action owner for the X sector and one coefficient slot: prove no physical X pole, derive s_X=0, or fill/source the first Qbar_XH/Z_X/s_X row with units",
            "success_condition": "one C_X factor becomes parent-signed zero or one coefficient receives a real parent-owned numeric/source row; otherwise demote finite local branch to explicit closure input",
            "forbidden_shortcuts": "fit to R10; set tau_R10=1; set qbar_XT=0 by covariance; use 2704 vector curve as claim evidence; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2706_0_CX",
            "topic": "C_X coupling",
            "status": "PRODUCT_EXACT_ZERO_UNSIGNED",
            "meaning": "the coupling wall is now localized to named factors rather than an undefined local residual",
            "next_action": "derive one factor from parent action",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2706_1_local_GR",
            "topic": "local GR/Newton",
            "status": "NOT_CLAIMED",
            "meaning": "MTS has a conditional route to silence but not a signed proof or local bound",
            "next_action": "parent action coefficient owner extraction",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2706_2_best_leap",
            "topic": "best route",
            "status": "UPSTREAM_ACTION_NOT_MORE_DATA",
            "meaning": "more bound-curve work is secondary until MTS supplies one real C_X input",
            "next_action": "2707 parent owner extraction",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2706_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "all outputs remain under post-checkpoint-work",
            "next_action": "keep private",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validate(generated_paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = rows_by_name["source_register"]
    add("VAL2706_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2706_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    audits = rows_by_name["zero_factor_audit"]
    add("VAL2706_2_all_zero_routes_nonclaim", all(row["can_claim_zero_now"] == "false" and row["valid_for_claim"] == "false" for row in audits), "all zero factor audits remain nonclaim")
    add("VAL2706_3_qbar_conditional_theorem_retained", any(row["audit_id"] == "ZPA2706_3_qbar_XT_zero" and "CONDITIONAL" in row["proof_status"] for row in audits), "qbar_XT conditional theorem retained but unsigned")
    add("VAL2706_4_product_zero_blocked", any(row["audit_id"] == "ZPA2706_5_product_verdict" and row["proof_status"] == "FAIL_NO_ZERO_FACTOR_SIGNED" for row in audits), "product zero is blocked")

    hunts = rows_by_name["coefficient_hunt"]
    add("VAL2706_5_all_core_coefficients_listed", {"Z_X", "M_X^2", "s_X", "Qbar_XH(lambda_X)", "qbar_XT"}.issubset({row["quantity"] for row in hunts}), "all core coefficient slots are listed")
    add("VAL2706_6_no_numeric_promotion", all(row["numeric_ready"] == "false" and row["valid_for_claim"] == "false" for row in hunts), "no coefficient row is promoted as numeric")

    contract = rows_by_name["first_coefficient_contract"]
    add("VAL2706_7_first_contract_selected", any(row["contract_id"] == "FCC2706_0_selected_Qbar_XH" for row in contract), "first Qbar_XH coefficient contract selected")
    add("VAL2706_8_contract_nonclaim", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in contract), "first coefficient contract is nonclaim")

    product = rows_by_name["product_gate"]
    add("VAL2706_9_product_law_present", any("C_X=s_X*Qbar_XH" in row["statement"] and row["gate_pass"] == "true" for row in product), "C_X product law is present")
    add("VAL2706_10_claims_blocked", all(row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]), "all claim gates keep claim_allowed=false")
    add("VAL2706_11_next_2707", any(row["next_id"] == "NEXT2706_0_selected" and "2707" in row["target_doc"] for row in rows_by_name["next_target"]), "2707 target selected")
    add("VAL2706_12_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2706_13_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2706_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2706_PARSE_validation")]
    add(
        "VAL2706_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2706 tries the C_X zero proof, rejects promotion, selects Qbar_XH as first coefficient contract, and routes 2707 upstream to parent-action coefficient ownership",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Zero-Factor Proof Audit", rows_by_name["zero_factor_audit"]),
        ("Parent Coefficient Row Hunt", rows_by_name["coefficient_hunt"]),
        ("C_X Product Gate", rows_by_name["product_gate"]),
        ("First Coefficient Contract", rows_by_name["first_coefficient_contract"]),
        ("Blocker Ledger", rows_by_name["blocker_ledger"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decisions", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2706: C_X Zero-Factor Proof Or First Parent Coefficient Row",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2706 takes the coupling wall head-on. The exact product `C_X=s_X Qbar_XH(lambda_X) qbar_XT/(4*pi*Z_X*G_obs)` is solid as a contract, but no zero factor is parent-signed. The strongest near-proof is still the ordinary-matter pullback route: if the parent action signs the observed coframe functor, matter lift, no-shadow/no-marker constants and boundary silence, then `qbar_XT=0`. Current corpus does not yet sign that stack, so the local branch is not a GR/Newton proof. The best leap is upstream: extract the parent action owner of the X sector and force one coefficient to become real.",
        "",
        "## Bottom Line",
        "",
        "- Zero route: mathematically sharp but still unsigned.",
        "- Finite route: product law exact, no numeric coefficient row yet.",
        "- First coefficient target: `Qbar_XH(lambda_X)` because it exposes source current, edge, shadow, projector and denominator debt in one place.",
        "- Best next move: 2707 parent-action coefficient owner extraction, not another R10 comparator.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "zero_factor_audit": zero_factor_audit_rows(),
        "coefficient_hunt": coefficient_hunt_rows(),
        "product_gate": product_gate_rows(),
        "first_coefficient_contract": first_coefficient_contract_rows(),
        "blocker_ledger": blocker_rows(),
        "claim_gates": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }

    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_zero_factor_audit"], rows_by_name["zero_factor_audit"])
    write_csv(BRANCH_OUTPUTS["local_first_contract"], rows_by_name["first_coefficient_contract"])
    write_csv(BRANCH_OUTPUTS["source_weight_contract"], rows_by_name["first_coefficient_contract"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    branch_rows = branch_copy_rows()
    rows_by_name["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)

    write_doc(rows_by_name)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
