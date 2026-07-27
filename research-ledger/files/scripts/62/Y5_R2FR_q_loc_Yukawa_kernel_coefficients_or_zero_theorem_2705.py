from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2705"
BRANCH_ID = "Y5_R2FR_QLOC_YUKAWA_KERNEL_COEFFICIENTS_OR_ZERO_THEOREM_2705"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2705-Y5-R2FR-q-loc-Yukawa-kernel-coefficients-or-zero-theorem.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2705_SOURCE_REGISTER.csv",
    "coefficient_ladder": RESIDUALS / "P8_Y5_R2FR_2705_QLOC_YUKAWA_COEFFICIENT_LADDER.csv",
    "parent_input_hunt": RESIDUALS / "P8_Y5_R2FR_2705_PARENT_INPUT_HUNT.csv",
    "zero_factor_forks": RESIDUALS / "P8_Y5_R2FR_2705_CX_ZERO_FACTOR_FORKS.csv",
    "alpha_template": RESIDUALS / "P8_Y5_R2FR_2705_R10_ALPHA_PREDICTION_TEMPLATE_NONCLAIM.csv",
    "profile_contract": RESIDUALS / "P8_Y5_R2FR_2705_BOUNDABLE_QLOC_PROFILE_CONTRACT.csv",
    "blocker_ledger": RESIDUALS / "P8_Y5_R2FR_2705_BLOCKER_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2705_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2705_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2705_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2705_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2705_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_alpha_template": LOCAL_BOUNDS / "R10_alpha_lambda_MTS_FINITE_COEFFICIENT_TEMPLATE_2705_NONCLAIM.csv",
    "local_profile_contract": LOCAL_BOUNDS / "q_loc_Yukawa_profile_contract_2705_NONCLAIM.csv",
    "local_zero_forks": LOCAL_BOUNDS / "C_X_zero_factor_forks_2705_NONCLAIM.csv",
    "wep_zero_forks": WEP_RESIDUALS / "C_X_zero_factor_forks_2705_NONCLAIM.csv",
    "source_weight_parent_inputs": SOURCE_WEIGHT / "QLOC_YUKAWA_PARENT_INPUT_HUNT_2705_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2705_CX_ZERO_FACTOR_OR_PARENT_COEFFICIENT_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2705_2704_NEXT",
        "relative_path": "2704-Y5-R2FR-APS-supplement-retrieval-or-q-loc-parent-profile-derivation.md",
        "required_needles": ["NEXT2704_0_selected", "QD2704_2_finite_yukawa_shape", "STATUS2704_1_q_loc", "VAL2704_OVERALL"],
        "purpose": "imports the selected coefficient/zero-theorem target",
    },
    {
        "source_id": "SRC2705_562_FORMULA_DOC",
        "relative_path": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
        "required_needles": ["PR562_2_canonical_mass_and_range", "PR562_4_prefactor", "O562_0_ZX_missing", "V562_3_lambda_prefactor_relations_written"],
        "purpose": "imports the conditional lambda and prefactor derivation",
    },
    {
        "source_id": "SRC2705_562_FORMULA_CSV",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
        "required_needles": ["PR562_2_canonical_mass_and_range", "PR562_4_prefactor", "PR562_5_positive_operator_identity"],
        "purpose": "imports exact symbolic formula rows",
    },
    {
        "source_id": "SRC2705_561_NUMERATOR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_561_DECISION.csv",
        "required_needles": ["D561_0_numerator_factorized", "Qbar_XH", "qbar_XT"],
        "purpose": "imports the numerator factorization route",
    },
    {
        "source_id": "SRC2705_2106_EXTRACTION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2106_EXTRACTION_MATRIX.csv",
        "required_needles": ["EXM2106_0_ZX", "MISSING_ZX", "EXM2106_1_MX2", "MISSING_MX2"],
        "purpose": "imports the latest parent Hessian extraction failure state",
    },
    {
        "source_id": "SRC2705_573_QBAR_CERT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_573_QBAR_XT_CERTIFICATE_STATUS.csv",
        "required_needles": ["QXC573_4_result", "conditional_only_not_parent_derived"],
        "purpose": "imports qbar_XT zero certificate blocker",
    },
    {
        "source_id": "SRC2705_575_QBAR_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_575_QBAR_XT_GATE.csv",
        "required_needles": ["QG575_4_result", "finite qbar_XT retained"],
        "purpose": "imports readout/constant-sector qbar gate status",
    },
    {
        "source_id": "SRC2705_2645_R10_REQUIREMENTS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_NO_SOURCE_PREFACTOR_2645_PROJECTION_REQUIREMENTS.csv",
        "required_needles": ["PRJ2645_2_R10", "MISSING_TAU_R10_K_QBAR_LAMBDA_PROJECTION"],
        "purpose": "imports arena projection requirements for R10 finite coefficient rows",
    },
    {
        "source_id": "SRC2705_2581_QLOC_ZERO",
        "relative_path": "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
        "required_needles": ["GK2581_7_verdict", "QLOC2581_TOTAL", "VAL2581_OVERALL"],
        "purpose": "imports the parent zero theorem route for q_loc",
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


def coefficient_ladder_rows() -> list[dict[str, Any]]:
    return [
        {
            "ladder_id": "CL2705_0_static_operator",
            "object": "parent X-sector static quadratic branch",
            "formula": "(-Z_X Delta + M_X^2) X = J_X",
            "derived_status": "IMPORTED_CONDITIONAL_FROM_562",
            "requires": "parent field owner; Z_X sign/value; M_X^2 sign/value; source split; units",
            "current_status": "RELATION_ONLY_PARENT_VALUES_MISSING",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "ladder_id": "CL2705_1_range",
            "object": "finite Yukawa range",
            "formula": "mu_X^2=M_X^2/Z_X; lambda_X=sqrt(Z_X/M_X^2)",
            "derived_status": "EXACT_IF_ZX_POSITIVE_AND_MX2_POSITIVE",
            "requires": "Z_X>0; M_X^2>0; same X normalization; meter conversion",
            "current_status": "RELATION_ONLY_NO_NUMERIC_LAMBDA",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "ladder_id": "CL2705_2_source_field",
            "object": "source-normalized exterior field",
            "formula": "X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r)",
            "derived_status": "GREEN_FUNCTION_SHAPE_DERIVED_CONDITIONALLY",
            "requires": "Q_X^H(lambda_X); boundary convention; finite-source form factor; same frame",
            "current_status": "QBAR_XH_NOT_PARENT_NUMERIC",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "ladder_id": "CL2705_3_test_response",
            "object": "ordinary test-body response",
            "formula": "a_X/a_N = [s_X Qbar_XH(lambda_X) qbar_XT/(4*pi*Z_X*G_obs)]*(1+r/lambda_X)*exp(-r/lambda_X)",
            "derived_status": "DERIVED_BY_COMBINING_561_562_2704",
            "requires": "s_X; Qbar_XH; qbar_XT; Z_X; G_obs convention; source/test normalization",
            "current_status": "NUMERATOR_AND_ZX_NOT_PARENT_NUMERIC",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "ladder_id": "CL2705_4_alpha_coefficient",
            "object": "single-mode R10 alpha coefficient",
            "formula": "C_X(alpha)=alpha_X(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT; K_X=s_X/(4*pi*Z_X*G_obs)",
            "derived_status": "COEFFICIENT_LAW_CONSOLIDATED",
            "requires": "all factors numeric/source-backed or one factor theorem-zero",
            "current_status": "NO_CLAIM_NUMERIC_ALPHA",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "ladder_id": "CL2705_5_multi_mode_guard",
            "object": "spectral/nonlocal memory extension",
            "formula": "delta a/a_N = integral dlnlambda alpha(lambda)*(1+r/lambda)*exp(-r/lambda)",
            "derived_status": "CONSERVATIVE_EXTENSION_ONLY",
            "requires": "positive spectral measure or no-cancellation envelope",
            "current_status": "NO_SPECTRAL_DENSITY",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def parent_input_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "PIN2705_0_ZX",
            "quantity": "Z_X",
            "role": "kinetic/gradient Hessian residue and alpha prefactor denominator",
            "current_evidence": "2106 extraction matrix: MISSING_ZX",
            "needed_for_promotion": "numeric positive parent-owned Z_X with units and X normalization",
            "status": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "PIN2705_1_MX2",
            "quantity": "M_X^2",
            "role": "mass Hessian / finite range",
            "current_evidence": "2106 extraction matrix: MISSING_MX2",
            "needed_for_promotion": "numeric positive parent-owned M_X^2 in same normalization as Z_X",
            "status": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "PIN2705_2_sX",
            "quantity": "s_X",
            "role": "sign/coupling of X field into local force/readout channel",
            "current_evidence": "562 prefactor row names s_X but no source-signed value",
            "needed_for_promotion": "parent action variation showing s_X=0 or numeric s_X with sign convention",
            "status": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "PIN2705_3_Qbar_XH",
            "quantity": "Qbar_XH(lambda_X)",
            "role": "source body X charge / finite-source form factor per mass",
            "current_evidence": "561 numerator factorized but zero/source value not derived",
            "needed_for_promotion": "parent source integral or theorem Qbar_XH=0 with boundary convention",
            "status": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "PIN2705_4_qbar_XT",
            "quantity": "qbar_XT",
            "role": "ordinary test-body X charge per inertial mass",
            "current_evidence": "573/575 keep qbar_XT finite; zero certificate blocked",
            "needed_for_promotion": "ordinary-matter no-marker/source-current theorem or numeric material projection",
            "status": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "PIN2705_5_tau_R10",
            "quantity": "tau_R10(lambda,geometry)",
            "role": "experiment/source geometry and finite-size projection",
            "current_evidence": "2645 projection requirements: MISSING_TAU_R10_K_QBAR_LAMBDA_PROJECTION",
            "needed_for_promotion": "R10 same-frame projection map including finite source/test normalization",
            "status": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "PIN2705_6_bound_curve",
            "quantity": "alpha_bound(lambda)",
            "role": "external R10 comparison curve",
            "current_evidence": "2704 vector candidate exists but official/QA curve not claim-grade",
            "needed_for_promotion": "official supplement or QA-locked digitized full curve",
            "status": "NONCLAIM_CANDIDATE_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def zero_factor_fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "ZF2705_0_no_active_pole",
            "zero_factor": "no X pole / X absent-gauge-topological",
            "zero_condition": "X is not a propagating parent mode in the local compact branch, or is pure gauge/topological with no local Hilbert force response",
            "current_status": "NOT_PROVED_IN_CURRENT_BRANCH",
            "blocks": "lambda_X and alpha_X remain symbolic if no pole proof fails",
            "next_evidence_needed": "parent degree-count and vertical-generator action signature",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fork_id": "ZF2705_1_sX_zero",
            "zero_factor": "s_X=0",
            "zero_condition": "parent T_GK/q_loc response is independent of X at first order in the local branch",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks": "C_X can survive as a force/readout coupling",
            "next_evidence_needed": "metric-response/action variation showing partial_X T_GK(Phi0)=0 for the physical component",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fork_id": "ZF2705_2_Qbar_XH_zero",
            "zero_factor": "Qbar_XH(lambda_X)=0",
            "zero_condition": "source body has no X monopole/form-factor charge and no boundary flux in the selected frame",
            "current_status": "SOURCE_ZERO_NOT_DERIVED",
            "blocks": "source can radiate/exchange a finite-range fifth-force tail",
            "next_evidence_needed": "J_X=0 plus boundary no-flux, or source integral with units",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fork_id": "ZF2705_3_qbar_XT_zero",
            "zero_factor": "qbar_XT=0",
            "zero_condition": "ordinary test matter descends through the observed quotient and carries no X marker/source charge",
            "current_status": "BLOCKED_BY_573_575",
            "blocks": "ordinary matter can still feel the X tail",
            "next_evidence_needed": "primitive minimal domain, invariant algebra triviality, constant-sector universality, and observed-kernel proof",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fork_id": "ZF2705_4_positive_nohair",
            "zero_factor": "positive operator no-hair",
            "zero_condition": "Z_X>0, M_X^2>0, J_X=0, boundary flux=0, regularity/decay hold",
            "current_status": "CONDITIONAL_IDENTITY_ONLY",
            "blocks": "mass gap alone gives range, not zero force",
            "next_evidence_needed": "source-zero and boundary-silence clauses in the same parent branch",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fork_id": "ZF2705_5_numeric_bound",
            "zero_factor": "not zero: bounded finite C_X",
            "zero_condition": "all factors numeric/source-backed and abs(alpha_X)<=alpha_bound(lambda_X)",
            "current_status": "NOT_SCORE_READY",
            "blocks": "cannot decide viability from symbolic factors",
            "next_evidence_needed": "Z_X,M_X^2,s_X,Qbar_XH,qbar_XT,tau_R10 and QA bound curve",
            "can_claim_zero_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "R10_finite_CX_template_2705",
            "curve_id": "R10_alpha_lambda_MTS_FINITE_COEFFICIENT_TEMPLATE_2705",
            "lambda_value": "sqrt(Z_X/M_X_squared)",
            "lambda_units": "m_after_parent_units",
            "alpha_predicted": "s_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
            "alpha_bound": "MISSING_QA_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "2704 vector candidate is nonclaim; official supplement still blocked",
            "force_law_form": "delta_a_over_a_N=alpha_X*(1+r/lambda_X)*exp(-r/lambda_X)",
            "derivation_status": "SYMBOLIC_COEFFICIENT_LAW_ONLY",
            "formula_reference": "562::PR562_2,PR562_4;2705::CL2705_4",
            "source_file": str(DOC_PATH),
            "assumptions": "Z_X>0;M_X_squared>0;same-frame G_obs;no cancellation;source/test charges parent-signed",
            "valid_for_claim": "false",
            "notes": "No numeric alpha row is produced; this is the exact template future data must fill.",
            "timestamp_utc": stamp(),
        }
    ]


def profile_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "QPROF2705_0_single_mode_profile",
            "profile_object": "q_loc R10 acceleration profile",
            "required_expression": "a_q(r)/a_N(r)=C_X*(1+r/lambda_X)*exp(-r/lambda_X)",
            "coefficient_definition": "C_X=s_X*Qbar_XH(lambda_X)*qbar_XT/(4*pi*Z_X*G_obs)",
            "range_definition": "lambda_X=sqrt(Z_X/M_X^2)",
            "required_inputs": "Z_X;M_X^2;s_X;Qbar_XH;qbar_XT;G_obs convention;source/test geometry;tau_R10",
            "current_status": "CONTRACT_READY_VALUES_MISSING",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "QPROF2705_1_zero_certificate",
            "profile_object": "q_loc theorem-zero replacement",
            "required_expression": "C_X=0 by s_X=0 or Qbar_XH=0 or qbar_XT=0, plus no hidden boundary/projector/readout term",
            "coefficient_definition": "zero factor must be parent-signed before substituting alpha_X=0",
            "range_definition": "not needed if no active pole or exact zero factor is proved",
            "required_inputs": "parent action; matter descent; source-current universality; boundary no-flux; P_loc owner",
            "current_status": "ZERO_CERTIFICATE_NOT_SIGNED",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "contract_id": "QPROF2705_2_multimode_envelope",
            "profile_object": "multi-mode or memory spectral envelope",
            "required_expression": "abs(delta a/a_N)<=int dlnlambda abs(alpha(lambda))*(1+r/lambda)*exp(-r/lambda)",
            "coefficient_definition": "alpha(lambda) from positive spectral measure or no-cancellation sampled bins",
            "range_definition": "lambda grid or spectral support with source-backed weights",
            "required_inputs": "spectral density; positivity; bin units; source/test normalization; bound curve",
            "current_status": "SPECTRAL_INPUTS_MISSING",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2705_0_numeric_parent_values",
            "blocker": "Z_X, M_X^2, s_X, Qbar_XH and qbar_XT are not all parent-sourced",
            "effect": "no numeric alpha_X(lambda_X) prediction exists",
            "next_action": "derive one zero factor or source the first numeric coefficient row",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2705_1_qbar_zero",
            "blocker": "ordinary matter X charge qbar_XT is not zero-proved",
            "effect": "the clean local-GR matter-blindness route remains unsigned",
            "next_action": "ordinary-matter quotient signature or bounded coupling component",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2705_2_source_zero_boundary",
            "blocker": "Qbar_XH/J_X and boundary no-flux are not zero-proved",
            "effect": "positive mass gap gives a Yukawa tail, not silence",
            "next_action": "source-current plus boundary silence proof, or finite source integral",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2705_3_bound_curve_QA",
            "blocker": "R10 external bound curve is candidate-only",
            "effect": "even numeric MTS alpha would need a QA/official bound curve before evidence",
            "next_action": "official supplement or QA acceptance of vector digitization",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2705_0_coefficient_law",
            "gate": "finite alpha coefficient law is exactly consolidated",
            "status": "PASS_NONCLAIM_FORMULA",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "formula is symbolic until parent values or zero factors are sourced",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2705_1_numeric_prediction",
            "gate": "numeric MTS alpha(lambda) prediction",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "Z_X/M_X^2/s_X/Qbar/qbar inputs are missing",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2705_2_zero_theorem",
            "gate": "C_X=0 theorem-zero",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "no zero factor is parent-signed",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2705_3_R10_score",
            "gate": "R10 score can be evidence",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "prediction and bound curve are not claim-grade",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2705_4_local_GR",
            "gate": "local GR/Newton recovery",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "q_loc is not zero-proved and finite residual is not bounded below all local tests",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2705_5_private",
            "gate": "public/GitHub action",
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
            "decision_id": "DEC2705_0_finite_route",
            "decision": "FINITE_ROUTE_FULLY_FACTORIZED",
            "rationale": "lambda_X and alpha_X are now a single explicit product law; missing pieces are named parent inputs, not vague coupling",
            "next_action": "attack one zero factor or source first numeric coefficient row",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2705_1_no_score",
            "decision": "NO_R10_SCORE_YET",
            "rationale": "symbolic alpha rows and candidate digitized bounds are useful plumbing but cannot decide physics",
            "next_action": "do not run evidence comparator until prediction row is numeric/source-backed",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2705_2_best_next",
            "decision": "ZERO_FACTOR_OR_FIRST_NUMERIC_COEFFICIENT_NEXT",
            "rationale": "any one zero factor would be stronger than fitting, while one real coefficient row would make the finite route testable",
            "next_action": "run 2706",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2705_0_selected",
            "selection": "selected_primary",
            "target_doc": "2706-Y5-R2FR-CX-zero-factor-proof-or-first-parent-coefficient-row.md",
            "target_script": "scripts/Y5_R2FR_CX_zero_factor_proof_or_first_parent_coefficient_row_2706.py",
            "task": "try to prove one C_X zero factor from parent action/matter/source/boundary descent; if none closes, source one numeric parent coefficient row for Z_X, M_X^2, s_X, Qbar_XH or qbar_XT with units and no-cancellation guards",
            "success_condition": "one zero-factor certificate is parent-signed, or one finite coefficient input becomes source-backed nonclaim data rather than symbolic text",
            "forbidden_shortcuts": "fit coefficients to R10; set qbar_XT=0 by preference; use symbolic Z_X/M_X^2 as numeric; treat vector curve as official; claim local GR/R10; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2705_0_finite_R10",
            "topic": "finite R10 branch",
            "status": "FACTORIZED_NOT_NUMERIC",
            "meaning": "the finite branch has exact formula shape but no parent-signed coefficient values",
            "next_action": "zero factor or first coefficient row",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2705_1_q_loc",
            "topic": "q_loc/local GR",
            "status": "ZERO_THEOREM_BLOCKED_BUT_FACTORS_NAMED",
            "meaning": "local silence now reduces to no active pole, s_X=0, Qbar_XH=0, qbar_XT=0, or positive no-hair premises",
            "next_action": "attack one factor rather than recircling the whole theorem",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2705_2_data",
            "topic": "R10 data",
            "status": "CANDIDATE_BOUND_HELD",
            "meaning": "2704 vector curve remains useful for smoke only",
            "next_action": "keep data branch parked until MTS prediction improves",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2705_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "all artifacts remain private in post-checkpoint-work",
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
    add("VAL2705_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2705_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    ladder = rows_by_name["coefficient_ladder"]
    add("VAL2705_2_lambda_relation_present", any("lambda_X=sqrt(Z_X/M_X^2)" in row["formula"] for row in ladder), "lambda_X relation is present")
    add("VAL2705_3_alpha_product_present", any("K_X Qbar_XH" in row["formula"] for row in ladder), "alpha product relation is present")

    inputs = rows_by_name["parent_input_hunt"]
    add("VAL2705_4_parent_inputs_missing_recorded", any(row["quantity"] == "Z_X" and row["status"] == "MISSING_PARENT_INPUT" for row in inputs) and any(row["quantity"] == "M_X^2" and row["status"] == "MISSING_PARENT_INPUT" for row in inputs), "Z_X and M_X^2 missing states are recorded")
    add("VAL2705_5_qbar_missing_recorded", any(row["quantity"] == "qbar_XT" and row["status"] == "MISSING_PARENT_INPUT" for row in inputs), "qbar_XT missing state is recorded")

    forks = rows_by_name["zero_factor_forks"]
    add("VAL2705_6_zero_factors_all_nonclaim", all(row["can_claim_zero_now"] == "false" and row["valid_for_claim"] == "false" for row in forks), "all zero-factor forks remain nonclaim")
    add("VAL2705_7_zero_factor_routes_named", len(forks) >= 5, "zero-factor routes are explicitly enumerated")

    alpha = rows_by_name["alpha_template"]
    add("VAL2705_8_alpha_template_symbolic", any("Z_X" in row["alpha_predicted"] and row["valid_for_claim"] == "false" for row in alpha), "alpha prediction template remains symbolic and nonclaim")

    profile = rows_by_name["profile_contract"]
    add("VAL2705_9_profile_contract_ready", any("C_X=" in row["coefficient_definition"] for row in profile), "boundable q_loc profile contract defines C_X")

    gates = rows_by_name["claim_gates"]
    add("VAL2705_10_no_claims", all(row["claim_allowed"] == "false" for row in gates), "all claim gates keep claim_allowed=false")
    add("VAL2705_11_next_2706", any(row["next_id"] == "NEXT2705_0_selected" and "2706" in row["target_doc"] for row in rows_by_name["next_target"]), "2706 target selected")
    add("VAL2705_12_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2705_13_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2705_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2705_PARSE_validation")]
    add(
        "VAL2705_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2705 consolidates the q_loc finite Yukawa coefficient law, records missing parent inputs and zero-factor forks, and selects 2706 zero-factor/first-coefficient work",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Coefficient Ladder", rows_by_name["coefficient_ladder"]),
        ("Parent Input Hunt", rows_by_name["parent_input_hunt"]),
        ("C_X Zero-Factor Forks", rows_by_name["zero_factor_forks"]),
        ("R10 Alpha Prediction Template", rows_by_name["alpha_template"]),
        ("Boundable q_loc Profile Contract", rows_by_name["profile_contract"]),
        ("Blocker Ledger", rows_by_name["blocker_ledger"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decisions", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2705: q_loc Yukawa Kernel Coefficients Or Zero Theorem",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2705 consolidates the finite local branch into one hard product law instead of letting the coupling problem stay foggy. For a single healthy local mode, `lambda_X=sqrt(Z_X/M_X^2)` and `alpha_X(lambda_X)=s_X Qbar_XH(lambda_X) qbar_XT/(4*pi*Z_X*G_obs)`. That is real derivational progress, but it is still not a prediction because every live factor is either symbolic, not parent-signed, or candidate-only. The clean ways forward are now exact: prove one zero factor, or source one real coefficient row.",
        "",
        "## Bottom Line",
        "",
        "- Finite route: exact formula, no numeric promotion.",
        "- Zero route: reduce `C_X=0` to named factors instead of a vague local plateau.",
        "- Data route: 2704 vector curve remains smoke-only until MTS has a real prediction.",
        "- Best next move: 2706 attacks one zero factor or first parent coefficient row.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "coefficient_ladder": coefficient_ladder_rows(),
        "parent_input_hunt": parent_input_hunt_rows(),
        "zero_factor_forks": zero_factor_fork_rows(),
        "alpha_template": alpha_template_rows(),
        "profile_contract": profile_contract_rows(),
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

    write_csv(BRANCH_OUTPUTS["local_alpha_template"], rows_by_name["alpha_template"])
    write_csv(BRANCH_OUTPUTS["local_profile_contract"], rows_by_name["profile_contract"])
    write_csv(BRANCH_OUTPUTS["local_zero_forks"], rows_by_name["zero_factor_forks"])
    write_csv(BRANCH_OUTPUTS["wep_zero_forks"], rows_by_name["zero_factor_forks"])
    write_csv(BRANCH_OUTPUTS["source_weight_parent_inputs"], rows_by_name["parent_input_hunt"])
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
