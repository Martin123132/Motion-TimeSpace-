from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2793-Y5-R2FR-parent-matter-descent-zero-current-or-DD-coefficient-source-pack-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2793_SOURCE_REGISTER.csv",
    "descent": MTS / "P8_Y5_R2FR_2793_PARENT_MATTER_DESCENT_ATTEMPT.csv",
    "contract": MTS / "P8_Y5_R2FR_2793_ZERO_CURRENT_CLAUSE_CONTRACT.csv",
    "pack": MTS / "P8_Y5_R2FR_2793_DD_COEFFICIENT_SOURCE_PACK.csv",
    "template": MTS / "P8_Y5_R2FR_2793_DD_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
    "pressure": MTS / "P8_Y5_R2FR_2793_COEFFICIENT_PRESSURE_SUMMARY.csv",
    "policy": MTS / "P8_Y5_R2FR_2793_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv",
    "candidate": MTS / "P8_Y5_R2FR_2793_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "runner": MTS / "P8_Y5_R2FR_2793_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2793_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2793_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2793_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2793_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2793_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2793_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "descent_queue": RAB_QUEUE / "JR2793_PARENT_MATTER_DESCENT_ZERO_NONCLAIM.csv",
    "pack_queue": RAB_QUEUE / "JR2793_DD_COEFFICIENT_SOURCE_PACK_NONCLAIM.csv",
    "pressure_queue": RAB_QUEUE / "JR2793_COEFFICIENT_PRESSURE_SUMMARY_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "WEP_PARENT_DESCENT_OR_COEFFICIENT_PACK_2793_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_parent_descent_or_coefficient_pack_2793_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2793_MINIMAL_MATTER_SIGNATURE_OR_COEFFICIENT_INTAKE_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(path: Path, id_column: str, row_id: str) -> dict[str, str]:
    for row in read_rows(path):
        if row.get(id_column) == row_id:
            return row
    return {}


def parse_float(value: Any, default: float = float("nan")) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def source_files() -> dict[str, Path]:
    return {
        "2792_next": MTS / "P8_Y5_R2FR_2792_NEXT_TARGET.csv",
        "2792_zero": MTS / "P8_Y5_R2FR_2792_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
        "2792_dd_map": MTS / "P8_Y5_R2FR_2792_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv",
        "2792_delta": MTS / "P8_Y5_R2FR_2792_COMPOSITION_DELTA_OBSTRUCTION.csv",
        "2792_pressure": MTS / "P8_Y5_R2FR_2792_NONCLAIM_COEFFICIENT_PRESSURE_ROWS.csv",
        "2792_guards": MTS / "P8_Y5_R2FR_2792_NO_CANCELLATION_GUARD.csv",
        "2792_runner": MTS / "P8_Y5_R2FR_2792_PRODUCT_RUNNER_STATUS.csv",
        "2792_gates": MTS / "P8_Y5_R2FR_2792_CLAIM_GATES.csv",
        "2791_range_schema": MTS / "P8_Y5_R2FR_2791_RANGE_ACQUISITION_SCHEMA.csv",
        "2789_products": MTS / "P8_Y5_R2FR_2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv",
        "2787_deltas": MTS / "P8_Y5_R2FR_2787_DD_MATERIAL_DELTA_IMPORT.csv",
        "2785_current_owner": MTS / "P8_Y5_R2FR_2785_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
        "1087_parent_descent_analogue": MTS / "P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
        "1087_zero_contract_analogue": MTS / "P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv",
        "1087_pack_analogue": MTS / "P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK.csv",
    }


def build_sources() -> list[dict[str, Any]]:
    roles = {
        "2792_next": "authoritative next target for 2793",
        "2792_zero": "R2FR WEP source-current zero verdict feeding 2793",
        "2792_dd_map": "R2FR parent-to-DD first-row obstruction",
        "2792_delta": "TA6V minus PtRh10 DD material deltas",
        "2792_pressure": "nonclaim coefficient-pressure rows",
        "2792_guards": "no-cancellation and no-absorption guardrails",
        "2792_runner": "nonclaim product runner status",
        "2792_gates": "claim-gate state from prior checkpoint",
        "2791_range_schema": "same-branch range/profile/readout blockers",
        "2789_products": "bulk Earth DD product scale source",
        "2787_deltas": "raw DD material delta import",
        "2785_current_owner": "narrow Hilbert/current-owner precedent",
        "1087_parent_descent_analogue": "R10 parent matter-descent analogue, used as structure not evidence",
        "1087_zero_contract_analogue": "R10 zero-current clause contract analogue",
        "1087_pack_analogue": "R10 DD coefficient pack analogue",
    }
    rows: list[dict[str, Any]] = []
    for source_id, path in source_files().items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "role": roles[source_id],
                "contains_text": bool(read_text(path).strip()) if path.exists() else False,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_descent_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PMD2793_0_theorem_statement",
            "parent matter descent theorem target",
            "If S_matter depends on the parent only through observed quotient geometry/gauge data, gauge-fixed matter fields, and X-trivial representation constants, then for every vertical v_X in ker(Dq), delta_vX S_matter=0 and qbar_XT=0.",
            "This is the clean route to WEP/local-current silence without fitted material coefficients.",
            "2792 left this conditional; 1087 shows the same clause stack on the R10 branch.",
            "THEOREM_CONDITIONAL_ONLY",
            "one parent action signature containing q, observed coframe/connection, matter lift, constants, measure, and boundary clauses",
        ),
        (
            "PMD2793_1_object_language",
            "ordinary matter object language",
            "S_matter may use only e_obs(q(Phi)), omega_obs(q(Phi)), gauge_obs(q(Phi)), Psi_A, theta_A, and universal constants.",
            "Removes source-only material labels and shadow frames from the action before variation.",
            "2792 and 1087 both retain this as a contract, not a parent-signed theorem.",
            "OBJECT_LANGUAGE_NOT_PARENT_SIGNED",
            "parent Lagrangian clause forbidding hidden material/source markers w_A before variation",
        ),
        (
            "PMD2793_2_observed_geometry_descent",
            "coframe/connection/gauge descent",
            "Lie_vX e_obs = Lie_vX omega_obs = Lie_vX gauge_obs = 0 because each is a functor of q(Phi) and Dq[v_X]=0.",
            "Kills geometric source-current leakage by chain rule.",
            "Conditional chain-rule sublemma survives, but the observed functor is not yet parent-owned on the R2FR WEP branch.",
            "CONDITIONAL_CHAIN_RULE_ONLY",
            "parent-defined observed geometry/gauge functor and independent-connection silence",
        ),
        (
            "PMD2793_3_matter_vertical_lift",
            "matter lift along v_X",
            "delta_vX Psi_A is zero, gauge, local-Lorentz/diffeomorphism, or boundary-only for all ordinary species A.",
            "Prevents physical material response from being hidden in the lift.",
            "No all-species parent matter-bundle functor has been signed.",
            "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "parent matter-bundle map assigning every tested ordinary material a fixed/gauge vertical lift",
        ),
        (
            "PMD2793_4_constant_superselection",
            "material constants are X-trivial",
            "Lie_vX theta_A=0 for alpha_EM, mass ratios, nuclear coefficients, clock constants, and representation data unless retained as explicit residual fields.",
            "This is where c_alpha, c_surface, and q_tail either vanish by theorem or become real finite coefficients.",
            "2792 showed nonzero DD deltas, so constant silence cannot be assumed.",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
            "superselection theorem for constants or explicit coefficient source rows",
        ),
        (
            "PMD2793_5_action_measure_no_weights",
            "single action measure and no inert species weights",
            "S_matter has one parent measure/hbar normalization and contains no independent w_A S_A factors that can vary by material before Hilbert variation.",
            "This is the main gate that would kill pre-action WEP leaks.",
            "2792 preserved the pre-action weight leak; 2785 only kills post-variation selector tricks.",
            "PRE_ACTION_WEIGHT_LEAK_SURVIVES",
            "object-language/action-measure clause forbidding source-only inert weights in the parent action",
        ),
        (
            "PMD2793_6_hidden_domain_boundary",
            "hidden/domain/boundary silence",
            "No shadow frame, support shift, edge charge, domain marker, or boundary term contributes to delta_vX S_matter.",
            "Blocks a zero proof from being spoiled at finite source/readout boundaries.",
            "2791/2792 still require same-branch profile/readout and boundary ownership.",
            "HIDDEN_DOMAIN_BOUNDARY_NOT_CLOSED",
            "no-shadow theorem, domain invariance, boundary charge silence, or explicit bounded residual rows",
        ),
        (
            "PMD2793_7_verdict",
            "qbar_XT=0 parent matter-descent theorem",
            "All PMD2793 clauses close from one parent action; therefore WEP source-current vanishes rather than being tuned.",
            "Would provide the cleanest route to local-GR/WEP compatibility.",
            "The sufficient theorem is written, but at least object language, action measure, matter lift, constants, and boundary clauses remain unsigned.",
            "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED",
            "minimal parent ordinary-matter signature clause or finite DD coefficient source intake",
        ),
    ]
    return [
        {
            "descent_id": row[0],
            "needed_clause": row[1],
            "mathematical_statement": row[2],
            "proof_role": row[3],
            "current_evidence": row[4],
            "result": row[5],
            "missing_for_claim": row[6],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZCC2793_0_object_language",
            "ordinary matter action arguments are restricted to quotient-owned observed geometry/gauge fields, owned matter fields, representation data, and universal constants",
            "source-only inert species weights and material markers",
            "OBJECT_LANGUAGE_NOT_SIGNED",
            "PMD2793_1_object_language",
        ),
        (
            "ZCC2793_1_action_measure",
            "one parent matter action measure and hbar normalization before readout/material projection",
            "relative action multipliers w_A that only appear as active source strength",
            "ACTION_MEASURE_NOT_SIGNED",
            "PMD2793_5_action_measure_no_weights",
        ),
        (
            "ZCC2793_2_variation_order",
            "Hilbert/current extraction occurs before any material/readout projection",
            "post-variation material selector redefinitions",
            "CONDITIONAL_SUBTHEOREM_ONLY",
            "2785_current_owner",
        ),
        (
            "ZCC2793_3_matter_functor",
            "ordinary matter fields live in a parent matter-bundle functor over observed quotient geometry with fixed/gauge vertical lift",
            "physical material lift along v_X",
            "PARENT_MATTER_FUNCTOR_NOT_SIGNED",
            "PMD2793_3_matter_vertical_lift",
        ),
        (
            "ZCC2793_4_constant_superselection",
            "ordinary matter constants are X-trivial representation/superselection data unless retained as explicit residual coefficients",
            "alpha/mass/clock/nuclear source-current leaks",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
            "PMD2793_4_constant_superselection",
        ),
        (
            "ZCC2793_5_boundary_domain",
            "support, boundary, and finite-readout domains are quotient-owned or separately bounded on the same branch",
            "finite-source hidden boundary current",
            "BOUNDARY_DOMAIN_NOT_SIGNED",
            "PMD2793_6_hidden_domain_boundary",
        ),
    ]
    return [
        {
            "clause_id": row[0],
            "future_parent_contract": row[1],
            "would_kill": row[2],
            "current_status": row[3],
            "source_row": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DDSP2793_0_c_alpha",
            "c_alpha",
            "N_X * partial_X ln(alpha_EM) evaluated in the same parent branch and normalization used for lambda_X and source profile",
            "dimensionless",
            "parent EM/fine-structure derivative with sign, normalization, and source path",
            "MISSING_PARENT_EM_DERIVATIVE",
            "MISSING_PARENT_SOURCE",
        ),
        (
            "DDSP2793_1_c_surface",
            "c_surface",
            "N_X * partial_X ln(a_surface_or_binding) or the parent-owned nuclear binding response projected into the DD surface row",
            "dimensionless",
            "parent nuclear/surface/binding derivative with sign and normalization",
            "MISSING_PARENT_BINDING_DERIVATIVE",
            "MISSING_PARENT_SOURCE",
        ),
        (
            "DDSP2793_2_c_mass_ratio",
            "c_mass_ratio",
            "N_X * partial_X ln(m_u/m_d, m_e/Lambda_QCD, or other retained mass-ratio channel if not absorbed by universal mass scaling)",
            "dimensionless",
            "parent mass-ratio derivative or proof it is universal/common-mode only",
            "MISSING_PARENT_MASS_RATIO_DERIVATIVE_OR_ZERO_PROOF",
            "MISSING_PARENT_SOURCE",
        ),
        (
            "DDSP2793_3_q_tail",
            "q_tail(A)",
            "absolute envelope for composition response not spanned by c_alpha and c_surface over all tested materials",
            "dimensionless material-response envelope",
            "basis-completeness proof or source-backed residual envelope",
            "MISSING_TAIL_BASIS_AND_ENVELOPE",
            "MISSING_PARENT_OR_EMPIRICAL_SOURCE",
        ),
        (
            "DDSP2793_4_same_branch_normalization",
            "N_X/K_X/lambda_X lock",
            "one normalization connecting Z_X, M_X^2, lambda_X, K_X, source profile, DD coefficients, and readout",
            "branch contract",
            "same parent branch range and Green-function normalization",
            "MISSING_SAME_BRANCH_NORMALIZATION",
            "P8_Y5_R2FR_2791_RANGE_ACQUISITION_SCHEMA.csv",
        ),
        (
            "DDSP2793_5_readout_source_profile",
            "K_MICROSCOPE * Q_source_eff(lambda)",
            "source/readout leg needed before coefficients become an eta prediction",
            "experiment-specific response",
            "official MICROSCOPE arrays plus PREM/profile lambda owner on the same branch",
            "MISSING_PROFILE_READOUT",
            "P8_Y5_R2FR_2791_RANGE_ACQUISITION_SCHEMA.csv",
        ),
    ]
    return [
        {
            "pack_id": row[0],
            "coefficient": row[1],
            "definition": row[2],
            "units": row[3],
            "required_source": row[4],
            "current_status": row[5],
            "source_path": row[6],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("DDTPL2793_0_c_alpha", "c_alpha", "MISSING_NUMERIC_VALUE", "dimensionless", "MISSING_PARENT_EM_DERIVATIVE", "same branch as lambda_X/readout", "False"),
        ("DDTPL2793_1_c_surface", "c_surface", "MISSING_NUMERIC_VALUE", "dimensionless", "MISSING_PARENT_BINDING_DERIVATIVE", "same branch as lambda_X/readout", "False"),
        ("DDTPL2793_2_c_mass_ratio", "c_mass_ratio", "MISSING_NUMERIC_VALUE", "dimensionless", "MISSING_PARENT_MASS_RATIO_DERIVATIVE_OR_ZERO_PROOF", "same branch as lambda_X/readout", "False"),
        ("DDTPL2793_3_q_tail_bound", "q_tail_bound", "MISSING_NUMERIC_VALUE", "dimensionless", "MISSING_TAIL_BASIS_AND_ENVELOPE", "all tested materials, not TA6V/PtRh10 only", "False"),
    ]
    return [
        {
            "template_id": row[0],
            "field": row[1],
            "value": row[2],
            "units": row[3],
            "required_source": row[4],
            "normalization_rule": row[5],
            "valid_for_claim": row[6],
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_pressure_rows() -> list[dict[str, Any]]:
    previous = read_rows(MTS / "P8_Y5_R2FR_2792_NONCLAIM_COEFFICIENT_PRESSURE_ROWS.csv")
    if not previous:
        previous = read_rows(MTS / "P8_Y5_R2FR_2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv")
    rows: list[dict[str, Any]] = []
    fallback = [
        ("Q_alpha_Coulomb", 3.365285544434638e-06, 2.8e-15, 8.320244933243532e-10, "bulk Earth vector, DD basis, and readout are not parent-owned"),
        ("Q_surface_binding", 4.007154691040701e-05, 2.8e-15, 6.987501646143863e-11, "bulk Earth vector, DD basis, and readout are not parent-owned"),
        ("Q_alpha_Coulomb + Q_surface_binding", 4.343683245484165e-05, 2.8e-15, 6.446142229433907e-11, "equal-component assumption is not parent-derived and profile/readout gates remain live"),
    ]
    if previous:
        for index, row in enumerate(previous):
            source_product = parse_float(row.get("source_material_product_abs") or row.get("product_abs"))
            eta_bound = parse_float(row.get("eta_bound"), 2.8e-15)
            coeff = parse_float(row.get("required_abs_coefficient_max") or row.get("coefficient_abs_max"))
            if coeff != coeff and source_product == source_product and source_product > 0:
                coeff = eta_bound / source_product
            rows.append(
                {
                    "pressure_id": f"CPS2793_{index}_{row.get('component', 'component').replace(' ', '_').replace('+', 'plus')}",
                    "component": row.get("component", "MISSING_COMPONENT"),
                    "source_material_product_abs": f"{source_product:.15e}" if source_product == source_product else "MISSING_NUMERIC",
                    "eta_bound": f"{eta_bound:.15e}" if eta_bound == eta_bound else "MISSING_NUMERIC",
                    "required_abs_coefficient_max": f"{coeff:.15e}" if coeff == coeff else "MISSING_NUMERIC",
                    "meaning": "if the coefficient is real in this nonclaim convention, it must sit below this scale",
                    "claim_blocker": row.get("claim_blocker", "source/profile/readout and parent coefficient ownership remain missing"),
                    "valid_for_claim": False,
                    "generated_utc": utc_now(),
                }
            )
    else:
        for index, row in enumerate(fallback):
            rows.append(
                {
                    "pressure_id": f"CPS2793_{index}",
                    "component": row[0],
                    "source_material_product_abs": f"{row[1]:.15e}",
                    "eta_bound": f"{row[2]:.15e}",
                    "required_abs_coefficient_max": f"{row[3]:.15e}",
                    "meaning": "fallback nonclaim pressure scale from earlier bulk Earth rows",
                    "claim_blocker": row[4],
                    "valid_for_claim": False,
                    "generated_utc": utc_now(),
                }
            )
    return rows


def build_policy_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AMC2793_0_pair_line_forbidden",
            "use the TA6V-PtRh10 cancellation line as a theory result",
            "one-pair cancellation is not invariant under changing test materials",
            "derive coefficient vector from parent action or prove it zero for all ordinary materials",
        ),
        (
            "AMC2793_1_basis_completeness",
            "score only c_alpha and c_surface as if they span all ordinary matter response",
            "DD alpha/surface are useful dominant channels but not a parent-complete material basis here",
            "include q_tail(A) envelope or parent completeness theorem",
        ),
        (
            "AMC2793_2_same_branch_requirement",
            "combine coefficients from one branch with lambda/profile/readout from another",
            "this would make range and amplitude independently tuneable",
            "one branch supplies Z_X, M_X^2, N_X, coefficients, K_X, source profile, and readout",
        ),
        (
            "AMC2793_3_universal_mass_absorption",
            "hide a composition-dependent source current inside measured G or universal mass calibration",
            "universal calibration can remove common mode but not material contrast",
            "separate common-mode renormalization from composition-vector residuals",
        ),
    ]
    return [
        {
            "policy_id": row[0],
            "forbidden_move": row[1],
            "why_forbidden": row[2],
            "acceptable_replacement": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    alpha_delta = find_row(MTS / "P8_Y5_R2FR_2792_COMPOSITION_DELTA_OBSTRUCTION.csv", "obstruction_id", "CDO2792_0_alpha_delta")
    surface_delta = find_row(MTS / "P8_Y5_R2FR_2792_COMPOSITION_DELTA_OBSTRUCTION.csv", "obstruction_id", "CDO2792_1_surface_delta")
    return [
        {
            "prediction_id": "WEP2793_0_symbolic_product",
            "observable": "MICROSCOPE-like eta_TA6V_PtRh10",
            "formula": "eta = K_readout * Q_source_eff(lambda_X) * (c_alpha*DeltaQ_alpha + c_surface*DeltaQ_surface + Deltaq_tail)",
            "DeltaQ_alpha": alpha_delta.get("delta_value", "MISSING_DELTA_ALPHA"),
            "DeltaQ_surface": surface_delta.get("delta_value", "MISSING_DELTA_SURFACE"),
            "coefficient_values": "MISSING_c_alpha;MISSING_c_surface;MISSING_q_tail;MISSING_K_readout;MISSING_Q_source_eff",
            "derivation_status": "SYMBOLIC_CONTRACT_ONLY",
            "claim_blocker": "parent coefficients and same-branch source/readout leg missing",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_runner_rows(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_predictions = [row for row in candidate_rows if str(row.get("valid_for_claim")).lower() == "true"]
    return [
        {
            "runner_id": "RUN2793_0_symbolic_runner_refusal",
            "valid_prediction_rows": len(valid_predictions),
            "claim_allowed": False,
            "reason": "candidate product remains symbolic and all source coefficients are missing",
            "expected_result": "RUNNER_REFUSES_WEP_CLAIM",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2793_0_no_numeric_eta",
            "baseline": "MICROSCOPE WEP bound",
            "prediction": "MTS R2FR DD coefficient product",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "c_alpha, c_surface, q_tail, source profile, and readout are not parent-sourced",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gates() -> list[dict[str, Any]]:
    rows = [
        ("CG2793_0_matter_descent", "qbar_XT=0 parent matter descent", False, False, "PMD2793_7_verdict=PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED"),
        ("CG2793_1_coefficient_pack", "DD coefficient source pack", False, False, "c_alpha, c_surface, c_mass_ratio, q_tail, same-branch normalization, and readout are missing"),
        ("CG2793_2_no_cancellation", "all-material no-cancellation policy", True, False, "policy is written and blocks pair-tuned shortcuts; it does not permit a claim"),
        ("CG2793_3_product_runner", "WEP product runner", False, False, "valid_prediction_rows=0"),
        ("CG2793_4_local_GR_WEP_claim", "local-GR/WEP pass", False, False, "neither theorem-zero nor finite sourced coefficient comparison is available"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim_component": row[1],
            "gate_pass": row[2],
            "claim_allowed": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2793_0_zero_route",
            "keep zero-current theorem route alive but unsigned",
            "the exact sufficient theorem is now explicit, yet the parent action has not signed object language, measure, matter lift, constants, and boundary clauses together",
            "try the minimal parent ordinary-matter signature clause next",
        ),
        (
            "DEC2793_1_finite_route",
            "open finite DD coefficient source-pack route as nonclaim fallback",
            "if theorem-zero fails, WEP can still be tested by sourced c_alpha/c_surface/q_tail and same-branch readout",
            "populate coefficient rows only from parent derivation or explicitly sourced empirical intake",
        ),
        (
            "DEC2793_2_no_claim",
            "do not claim WEP/local-GR pass",
            "current checkpoint is a contract and acquisition pack, not an experimental pass",
            "block any claim until gates CG2793_0 or CG2793_1 plus CG2793_3 close",
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2793_0_2794",
            "next_target": "2794-Y5-R2FR-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake-under-AX1090.md",
            "script": "scripts/Y5_R2FR_minimal_parent_ordinary_matter_signature_clause_or_finite_coefficient_intake_under_AX1090_2794.py",
            "objective": "attempt the minimal parent ordinary-matter signature clause that signs object language, action measure, matter functor, constant superselection, variation order, and boundary/domain silence together; if it cannot be derived, open finite DD coefficient intake as explicitly phenomenological and nonclaim",
            "include": "single parent action clause; no species weights; matter bundle over observed quotient; theta_A superselection; variation-before-readout; boundary/domain silence; finite coefficient intake fallback",
            "exclude": "post-hoc coefficient fitting; pair cancellation; unit source proxy; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["descent"], BRANCH_OUTPUTS["descent_queue"], "descent_queue"),
        (OUTPUTS["pack"], BRANCH_OUTPUTS["pack_queue"], "pack_queue"),
        (OUTPUTS["pressure"], BRANCH_OUTPUTS["pressure_queue"], "pressure_queue"),
        (OUTPUTS["contract"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["policy"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows: list[dict[str, Any]] = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2793_{label}",
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= threshold:
            return False
    return True


def any_claim_flag_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() == "true":
                return True
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() == "true":
                return True
    return False


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2793_0_sources_exist", all(row["exists"] for row in sections["sources"]), "every cited local source path exists"),
        ("VAL2793_1_theorem_conditional", any(row["descent_id"] == "PMD2793_0_theorem_statement" and row["result"] == "THEOREM_CONDITIONAL_ONLY" for row in sections["descent"]), "sufficient theorem is written but conditional"),
        ("VAL2793_2_zero_not_signed", any(row["descent_id"] == "PMD2793_7_verdict" and row["result"] == "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED" for row in sections["descent"]), "parent matter descent zero is not claimed"),
        ("VAL2793_3_weight_leak_survives", any(row["descent_id"] == "PMD2793_5_action_measure_no_weights" and row["result"] == "PRE_ACTION_WEIGHT_LEAK_SURVIVES" for row in sections["descent"]), "pre-action species/material weight leak remains explicit"),
        ("VAL2793_4_contract_has_all_clauses", {row["clause_id"] for row in sections["contract"]} >= {"ZCC2793_0_object_language", "ZCC2793_1_action_measure", "ZCC2793_3_matter_functor", "ZCC2793_4_constant_superselection", "ZCC2793_5_boundary_domain"}, "zero-current parent contract contains object-language, measure, matter, constants, and boundary clauses"),
        ("VAL2793_5_pack_has_required_coefficients", {row["coefficient"] for row in sections["pack"]} >= {"c_alpha", "c_surface", "c_mass_ratio", "q_tail(A)", "N_X/K_X/lambda_X lock", "K_MICROSCOPE * Q_source_eff(lambda)"}, "DD coefficient source pack includes coefficient and same-branch/readout slots"),
        ("VAL2793_6_template_nonclaim", all(str(row["valid_for_claim"]).lower() == "false" for row in sections["template"]), "source-pack template rows remain nonclaim"),
        ("VAL2793_7_pressure_numeric", all(parse_float(row["required_abs_coefficient_max"]) == parse_float(row["required_abs_coefficient_max"]) for row in sections["pressure"]), "pressure rows carry numeric coefficient ceilings"),
        ("VAL2793_8_policy_blocks_pair_tuning", any(row["policy_id"] == "AMC2793_0_pair_line_forbidden" for row in sections["policy"]), "one-pair cancellation is forbidden"),
        ("VAL2793_9_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["runner"]), "runner refuses WEP claim"),
        ("VAL2793_10_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2793_11_next_target_2794", any(row["next_id"] == "NEXT2793_0_2794" for row in sections["next"]), "next target is 2794"),
        ("VAL2793_12_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2793_13_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2793_14_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2793_15_no_claim_flags", not any_claim_flag_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2793_16_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2793_17_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2793_18_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2793_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2793 writes the exact parent matter-descent theorem contract and converts the unresolved WEP composition current into a finite DD coefficient source pack. The zero-current route remains alive but unsigned; the coefficient route is source-ready but nonclaim.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2793 — Y5 R2FR Parent Matter Descent Zero Current Or DD Coefficient Source Pack Under AX1090",
        "",
        "## Private Verdict",
        "",
        "The derivation-first route is now sharply stated: if ordinary matter only sees quotient-owned observed geometry/gauge data, fixed/gauge matter lifts, X-trivial representation constants, one parent action measure, and silent boundary/domain terms, then the WEP source-current is theorem-zero. That would be the clean GR-compatible route.",
        "",
        "But 2793 does **not** sign that theorem from the parent action. The pre-action species/material-weight leak, matter-functor lift, constant/superselection route, and boundary/domain silence still require a single parent ordinary-matter signature clause. Therefore the finite DD coefficient source-pack route is opened as a nonclaim fallback.",
        "",
        "No WEP, local-GR, or R2FR pass is claimed.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["source_id", "exists", "role", "path"]),
        "",
        "## Parent Matter Descent Attempt",
        markdown_table(sections["descent"], ["descent_id", "needed_clause", "result", "missing_for_claim"]),
        "",
        "## Zero-Current Clause Contract",
        markdown_table(sections["contract"], ["clause_id", "future_parent_contract", "would_kill", "current_status"]),
        "",
        "## DD Coefficient Source Pack",
        markdown_table(sections["pack"], ["pack_id", "coefficient", "current_status", "required_source"]),
        "",
        "## Template Rows",
        markdown_table(sections["template"], ["template_id", "field", "value", "required_source", "valid_for_claim"]),
        "",
        "## Coefficient Pressure Summary",
        markdown_table(sections["pressure"], ["pressure_id", "component", "source_material_product_abs", "eta_bound", "required_abs_coefficient_max", "claim_blocker"]),
        "",
        "## All-Material No-Cancellation Policy",
        markdown_table(sections["policy"], ["policy_id", "forbidden_move", "why_forbidden", "acceptable_replacement"]),
        "",
        "## Product Candidate",
        markdown_table(sections["candidate"], ["prediction_id", "formula", "derivation_status", "claim_blocker", "valid_for_claim"]),
        "",
        "## Runner And Comparison",
        markdown_table(sections["runner"], ["runner_id", "valid_prediction_rows", "claim_allowed", "expected_result"]),
        "",
        markdown_table(sections["comparisons"], ["comparison_id", "comparison_status", "reason"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "descent": build_descent_rows(),
        "contract": build_contract_rows(),
        "pack": build_pack_rows(),
        "template": build_template_rows(),
        "pressure": build_pressure_rows(),
        "policy": build_policy_rows(),
        "candidate": build_candidate_rows(),
    }
    sections["runner"] = build_runner_rows(sections["candidate"])
    sections["comparisons"] = build_comparison_rows()
    sections["gates"] = build_gates()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)

    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])

    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")

    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
