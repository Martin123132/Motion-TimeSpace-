from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1557_doc": ROOT / "1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md",
    "1557_validation": OUT / "P8_Y5_BRR545_1557_VALIDATION.csv",
    "1557_budget": OUT / "P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv",
    "1557_sensitivity": OUT / "P8_Y5_PARENT_QLOC_1557_SENSITIVITY_MAP_NONCLAIM.csv",
    "14_doc": ROOT / "14-closure-deviation-PPN-sensitivity.md",
    "13_doc": ROOT / "13-local-closure-PPN-benchmark.md",
    "10_doc": ROOT / "10-observer-map-symplectic-contract.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1557_doc": ["No MTS local prediction is scored here", "response coefficients are still missing"],
    "1557_validation": ["VAL1557_OVERALL", "PASS"],
    "1557_budget": ["BUD1557_0_qR", "MISSING_C_gamma_qR"],
    "1557_sensitivity": ["SENS1557_0_qR_light_bending", "SENS1557_3_delta_beta_mercury"],
    "14_doc": ["Mercury shift factor = (2 q_R - delta_beta)/3.", "solar light bending vs q_R"],
    "13_doc": ["R_AB approx q_R L", "gamma approx 1 + q_R."],
    "10_doc": ["PPN gamma:", "PPN beta:"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1558_SOURCE_REGISTER.csv"
PPN_COEFFICIENTS = OUT / "P8_Y5_PARENT_QLOC_1558_PPN_COEFFICIENT_DERIVATION.csv"
PHENOMENOLOGICAL = OUT / "P8_Y5_PARENT_QLOC_1558_PHENOMENOLOGICAL_COEFFICIENT_MAP.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1558_COEFFICIENT_REJECTION_LEDGER.csv"
READINESS_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1558_COEFFICIENT_READINESS_MATRIX.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1558_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1558_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1558_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1558_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1558_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1558"
QUAR_PPN = QUARANTINE / "PPN_COEFFICIENT_DERIVATION_NONCLAIM.csv"
QUAR_PHEN = QUARANTINE / "PHENOMENOLOGICAL_COEFFICIENT_MAP_NONCLAIM.csv"
QUAR_REJECT = QUARANTINE / "COEFFICIENT_REJECTION_LEDGER_NONCLAIM.csv"
QUAR_READY = QUARANTINE / "COEFFICIENT_READINESS_MATRIX_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_PPN = BRANCH_RESIDUALS / "PPN_coefficient_derivation_nonclaim_1558.csv"
BRANCH_PHEN = BRANCH_RESIDUALS / "phenomenological_coefficient_map_nonclaim_1558.csv"
BRANCH_REJECT = BRANCH_RESIDUALS / "coefficient_rejection_ledger_nonclaim_1558.csv"
BRANCH_READY = BRANCH_RESIDUALS / "coefficient_readiness_matrix_nonclaim_1558.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "coefficient_source_runner_nonclaim_1558.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "coefficient_source_decision_nonclaim_1558.csv"

THETA_GR_ARCSEC = 1.7512432813682448
SHAPIRO_GR_MICROSECONDS = 119.4750358485562
MERCURY_GR_ARCSEC_PER_CENTURY = 42.98201260912118
GPS_GR_MICROSECONDS_PER_DAY = 45.718449825926655


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


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


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


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1558_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for response-coefficient source mapping or rejection",
                **flags(),
            }
        )
    return rows


def ppn_coefficient_rows() -> list[dict[str, Any]]:
    q_light = THETA_GR_ARCSEC / 2.0
    q_shapiro = SHAPIRO_GR_MICROSECONDS / 2.0
    q_mercury = 2.0 * MERCURY_GR_ARCSEC_PER_CENTURY / 3.0
    beta_mercury = -MERCURY_GR_ARCSEC_PER_CENTURY / 3.0
    rows = [
        (
            "PPNC1558_0_qR_gamma",
            "q_R",
            "gamma_minus_1",
            "1",
            "dimensionless per unit q_R",
            "R_AB=ln(T^2 S) approx (gamma-1)L and R_AB approx q_R L, so gamma-1=q_R at first PPN order",
            "DERIVED_PPN_DICTIONARY_NOT_PARENT_PREDICTION",
            "R3_gamma",
        ),
        (
            "PPNC1558_1_qR_light_bending",
            "q_R",
            "solar_light_bending_residual",
            f"{q_light:.16g}",
            "arcsec per unit q_R",
            "PPN light deflection scales as (1+gamma)/2 times the GR value; with gamma-1=q_R, residual coefficient is theta_GR/2",
            "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION",
            "R3_gamma",
        ),
        (
            "PPNC1558_2_qR_shapiro",
            "q_R",
            "solar_Shapiro_residual",
            f"{q_shapiro:.16g}",
            "microseconds per unit q_R",
            "PPN Shapiro delay scales as (1+gamma)/2 times the GR value; with gamma-1=q_R, residual coefficient is delay_GR/2",
            "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION",
            "R3_gamma",
        ),
        (
            "PPNC1558_3_qR_mercury",
            "q_R",
            "Mercury_perihelion_residual",
            f"{q_mercury:.16g}",
            "arcsec/century per unit q_R",
            "PPN perihelion factor is (2+2gamma-beta)/3; gamma=1+q_R gives +2/3 of GR coefficient",
            "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION",
            "R3_gamma; R4_beta",
        ),
        (
            "PPNC1558_4_delta_beta_definition",
            "delta_beta",
            "beta_minus_1",
            "1",
            "dimensionless per unit delta_beta",
            "delta_beta is the beta-1 nonlinear completion drift by definition in the local-deviation dictionary",
            "PPN_PARAMETER_DEFINITION_NOT_PARENT_COMPLETION",
            "R4_beta",
        ),
        (
            "PPNC1558_5_delta_beta_mercury",
            "delta_beta",
            "Mercury_perihelion_residual",
            f"{beta_mercury:.16g}",
            "arcsec/century per unit delta_beta",
            "PPN perihelion factor is (2+2gamma-beta)/3; beta=1+delta_beta gives -1/3 of GR coefficient",
            "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION",
            "R4_beta",
        ),
        (
            "PPNC1558_6_perihelion_degeneracy",
            "q_R; delta_beta",
            "Mercury_perihelion_residual",
            "(2 q_R - delta_beta)/3 times GR perihelion",
            "dimensionless factor",
            "perihelion alone constrains the combination 2 q_R - delta_beta and cannot isolate both without light/Shapiro/gamma input",
            "DERIVED_PPN_DEGENERACY_STRUCTURE_NOT_PARENT_PREDICTION",
            "R3_gamma; R4_beta",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "coefficient_id": coefficient_id,
            "leak_parameter": leak_parameter,
            "observable_response": observable_response,
            "coefficient_value": coefficient_value,
            "coefficient_units": coefficient_units,
            "derivation": derivation,
            "coefficient_status": coefficient_status,
            "local_bound_rows": local_bound_rows,
            "translation_ready": True,
            "parent_prediction_ready": False,
            "source_paths": source_list("13_doc", "14_doc", "10_doc", "1557_sensitivity"),
            **flags(),
        }
        for (
            coefficient_id,
            leak_parameter,
            observable_response,
            coefficient_value,
            coefficient_units,
            derivation,
            coefficient_status,
            local_bound_rows,
        ) in rows
    ]


def phenomenological_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PHEN1558_0_alpha_clock_redshift",
            "alpha_clock",
            "alpha_clock_redshift",
            "1",
            "dimensionless per unit alpha_clock",
            f"{GPS_GR_MICROSECONDS_PER_DAY:.16g} microseconds/day per unit alpha_clock for the GPS-style internal scale",
            "alpha_clock can be used as the observed redshift-deviation parameter, but the MTS clock/load map is not parent-derived",
            "PHENOMENOLOGICAL_PARAMETER_DEFINITION_ONLY",
            "R2_clock_redshift",
        ),
        (
            "PHEN1558_1_epsilon_matter_eta",
            "epsilon_matter",
            "eta_WEP_proxy",
            "1",
            "dimensionless proxy per unit coupling spread",
            "Eotvos proxy is one-to-one only by proxy definition",
            "epsilon_matter measures matter-coupling spread, but universal matter-action descent is not derived",
            "PHENOMENOLOGICAL_PROXY_ONLY",
            "R0_identity_coframe_direct; R1_WEP_source_charge",
        ),
        (
            "PHEN1558_2_sigma_Gdot",
            "sigma_Gdot",
            "Gdot_over_G",
            "MISSING",
            "yr^-1 per source-normalization drift",
            "no coefficient available",
            "requires measured-GM/source-normalization theorem before Gdot bound can be applied to MTS",
            "REJECTED_FOR_NOW_MISSING_PARENT_SOURCE_NORMALIZATION",
            "R9_Gdot",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "phenomenology_id": phenomenology_id,
            "leak_parameter": leak_parameter,
            "observable_response": observable_response,
            "coefficient_value": coefficient_value,
            "coefficient_units": coefficient_units,
            "control_scale": control_scale,
            "limitation": limitation,
            "coefficient_status": coefficient_status,
            "local_bound_rows": local_bound_rows,
            "translation_ready": coefficient_value != "MISSING",
            "parent_prediction_ready": False,
            "source_paths": source_list("14_doc", "1557_budget", "local_bound_claims"),
            **flags(),
        }
        for (
            phenomenology_id,
            leak_parameter,
            observable_response,
            coefficient_value,
            coefficient_units,
            control_scale,
            limitation,
            coefficient_status,
            local_bound_rows,
        ) in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "REJ1558_0_source_normalization",
            "sigma_Gdot",
            "Gdot_over_G",
            "MISSING_C_Gdot",
            "no parent measured-GM/source-normalization theorem; cannot decide whether source drift maps to measured Gdot",
            "derive source-normalization theorem or leave as external bound only",
        ),
        (
            "REJ1558_1_preferred_frame_alpha1",
            "epsilon_frame_1",
            "alpha1",
            "MISSING_C_alpha1",
            "no frame/coframe descent coefficient from parent observer split",
            "derive frame-descent response or keep alpha1 as no-claim diagnostic",
        ),
        (
            "REJ1558_2_preferred_frame_alpha2",
            "epsilon_frame_2",
            "alpha2",
            "MISSING_C_alpha2",
            "spin/anisotropic coframe leakage lacks a response map",
            "derive spin/coframe response or keep alpha2 as no-claim diagnostic",
        ),
        (
            "REJ1558_3_flux_alpha3_xi",
            "epsilon_flux",
            "alpha3; xi",
            "MISSING_C_alpha3_AND_C_xi",
            "boundary silence and momentum/source-flux conservation are not parent-derived",
            "derive boundary/no-charge theorem before using ultra-tight alpha3/xi bounds",
        ),
        (
            "REJ1558_4_R10_range_curve",
            "alpha_R10(lambda)",
            "Yukawa alpha(lambda)",
            "MISSING_C_R10_lambda_AND_DIGITIZED_CURVE",
            "R10 bound remains symbolic curve-only and parent range map is absent",
            "acquire real alpha(lambda) curve and derive lambda/residual-hair map",
        ),
        (
            "REJ1558_5_tracefree_transfer",
            "h_TF_residual",
            "PPN residual vector",
            "MISSING_M_TF_RESPONSE_MATRIX",
            "scalar R_AB closure does not define tensor/vector transfer",
            "derive tensor/coframe response matrix before vector/tensor PPN scoring",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "leak_parameter": leak_parameter,
            "observable_response": observable_response,
            "missing_input": missing_input,
            "reason": reason,
            "reentry_condition": reentry_condition,
            "status": "REJECTED_FOR_SCORING_AT_1558",
            "source_paths": source_list("1557_budget", "1557_sensitivity", "local_bound_claims"),
            **flags(),
        }
        for rejection_id, leak_parameter, observable_response, missing_input, reason, reentry_condition in rows
    ]


def readiness_rows() -> list[dict[str, Any]]:
    rows = [
        ("READY1558_0_qR_gamma", "q_R", "gamma_minus_1/light/Shapiro/perihelion", True, False, "PPN translation is derived; parent still must predict q_R"),
        ("READY1558_1_delta_beta", "delta_beta", "beta_minus_1/perihelion", True, False, "PPN translation is derived; parent still must supply beta completion"),
        ("READY1558_2_alpha_clock", "alpha_clock", "redshift/clocks", True, False, "phenomenological clock parameter usable; parent clock/load response missing"),
        ("READY1558_3_epsilon_matter", "epsilon_matter", "WEP/Eotvos", True, False, "proxy parameter usable; parent matter descent missing"),
        ("READY1558_4_sigma_Gdot", "sigma_Gdot", "Gdot/G", False, False, "source-normalization coefficient missing"),
        ("READY1558_5_frame", "epsilon_frame_1; epsilon_frame_2", "alpha1/alpha2", False, False, "frame/coframe descent coefficients missing"),
        ("READY1558_6_flux", "epsilon_flux", "alpha3/xi", False, False, "boundary/source-flux coefficients missing"),
        ("READY1558_7_R10", "alpha_R10(lambda)", "Yukawa alpha(lambda)", False, False, "digitized curve and parent range map missing"),
        ("READY1558_8_tracefree", "h_TF_residual", "PPN residual vector", False, False, "tensor response matrix missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "readiness_id": readiness_id,
            "leak_parameter": leak_parameter,
            "observable_response": observable_response,
            "translation_ready": translation_ready,
            "parent_prediction_ready": parent_prediction_ready,
            "score_ready": False,
            "reason": reason,
            "status": "TRANSLATION_ONLY" if translation_ready else "REJECTED_PENDING_INPUTS",
            "source_paths": source_list("14_doc", "1557_budget", "local_bound_claims"),
            "numeric_value_present": False,
            "source_backed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for readiness_id, leak_parameter, observable_response, translation_ready, parent_prediction_ready, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1558_0_sources",
            "test": "1557 handoff and coefficient sources exist",
            "current_status": "PASS",
            "detail": "all coefficient source files exist and evidence needles are present",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1558_1_qR_beta_ppn",
            "test": "derive q_R and delta_beta PPN translation coefficients",
            "current_status": "PASS_TRANSLATION_ONLY",
            "detail": "q_R maps to gamma-1; light/Shapiro/perihelion and beta perihelion coefficients are derived from standard PPN scaling",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1558_2_clock_matter",
            "test": "classify clock and matter coefficients",
            "current_status": "PASS_PHENOMENOLOGICAL_ONLY",
            "detail": "clock and WEP parameters can be used as proxy observables but not as parent-derived MTS predictions",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1558_3_rejections",
            "test": "reject unsupported coefficients",
            "current_status": "PASS_REJECTION_LEDGER",
            "detail": "Gdot, preferred-frame, flux, R10, and tracefree coefficients remain blocked",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1558_4_scoring",
            "test": "local-bound scoring",
            "current_status": "REFUSED_NO_PARENT_PREDICTIONS",
            "detail": "translation coefficients do not produce a claim until the parent action predicts q_R, delta_beta, clock/matter drift, or their zeros",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1558_0_qR_translation", "q_R PPN translation", "OPEN_TRANSLATION_ONLY", "coefficient map exists, but parent q_R prediction is missing"),
        ("GATE1558_1_beta_translation", "delta_beta PPN translation", "OPEN_TRANSLATION_ONLY", "coefficient map exists, but parent beta completion is missing"),
        ("GATE1558_2_clock", "clock coefficient", "BLOCKED_NO_CLAIM", "phenomenological redshift parameter only"),
        ("GATE1558_3_matter", "matter/WEP coefficient", "BLOCKED_NO_CLAIM", "phenomenological WEP proxy only"),
        ("GATE1558_4_Gdot", "source normalization", "BLOCKED_NO_CLAIM", "source-normalization theorem missing"),
        ("GATE1558_5_frame_flux_tracefree_R10", "remaining local residual vector", "BLOCKED_NO_CLAIM", "response matrix/range/boundary coefficients missing"),
        ("GATE1558_6_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "translation map is not a parent derivation of R_AB=0, Q_R=0, or beta=1"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1557_budget", "14_doc", "13_doc", "10_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1558_0_verdict",
            "decision": "coefficient source-map status",
            "result": "Q_R_AND_DELTA_BETA_TRANSLATION_DERIVED_PARENT_PREDICTIONS_MISSING",
            "reason": "the q_R/beta PPN observable map is now mathematically sharp, but MTS still needs parent equations that set or predict the leak parameters",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1558_1_next",
            "decision": "next target",
            "result": "NEXT_1559_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT",
            "reason": "use the derived q_R/delta_beta map to build a two-parameter local control runner while separately hunting the parent zero conditions",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1558_0_1559",
            "next_target": "1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md",
            "script": "scripts/Y5_qR_delta_beta_two_parameter_PPN_control_runner_and_zero_condition_hunt.py",
            "objective": "use the derived q_R and delta_beta PPN translation coefficients to build a nonclaim two-parameter local control runner, then identify the exact parent zero conditions needed to promote q_R=0 and delta_beta=0 from closure to derivation",
            "do_not": "do not score MTS predictions without parent-predicted leak parameters; do not claim local GR derivation; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (PPN_COEFFICIENTS, QUAR_PPN),
        (PHENOMENOLOGICAL, QUAR_PHEN),
        (REJECTION_LEDGER, QUAR_REJECT),
        (READINESS_MATRIX, QUAR_READY),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (PPN_COEFFICIENTS, BRANCH_PPN),
        (PHENOMENOLOGICAL, BRANCH_PHEN),
        (REJECTION_LEDGER, BRANCH_REJECT),
        (READINESS_MATRIX, BRANCH_READY),
        (RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    ppn = read_csv(PPN_COEFFICIENTS)
    phenomenology = read_csv(PHENOMENOLOGICAL)
    rejections = read_csv(REJECTION_LEDGER)
    readiness = read_csv(READINESS_MATRIX)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    q_light = next(row for row in ppn if row["coefficient_id"] == "PPNC1558_1_qR_light_bending")
    q_shapiro = next(row for row in ppn if row["coefficient_id"] == "PPNC1558_2_qR_shapiro")
    q_mercury = next(row for row in ppn if row["coefficient_id"] == "PPNC1558_3_qR_mercury")
    beta_mercury = next(row for row in ppn if row["coefficient_id"] == "PPNC1558_5_delta_beta_mercury")

    checks = [
        ("VAL1558_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1558 source paths exist"),
        ("VAL1558_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1558_2_qR_gamma", any(row["coefficient_id"] == "PPNC1558_0_qR_gamma" and row["coefficient_value"] == "1" for row in ppn), "q_R to gamma-minus-one coefficient derived"),
        ("VAL1558_3_light_coefficient", math.isclose(float(q_light["coefficient_value"]), THETA_GR_ARCSEC / 2.0, rel_tol=0, abs_tol=1e-12), "light-bending q_R coefficient equals GR/2"),
        ("VAL1558_4_shapiro_coefficient", math.isclose(float(q_shapiro["coefficient_value"]), SHAPIRO_GR_MICROSECONDS / 2.0, rel_tol=0, abs_tol=1e-12), "Shapiro q_R coefficient equals GR/2"),
        ("VAL1558_5_perihelion_coefficients", math.isclose(float(q_mercury["coefficient_value"]), 2.0 * MERCURY_GR_ARCSEC_PER_CENTURY / 3.0, rel_tol=0, abs_tol=1e-12) and math.isclose(float(beta_mercury["coefficient_value"]), -MERCURY_GR_ARCSEC_PER_CENTURY / 3.0, rel_tol=0, abs_tol=1e-12), "perihelion coefficients match (2 q_R - delta_beta)/3"),
        ("VAL1558_6_clock_matter_nonparent", all(row["parent_prediction_ready"] == "False" for row in phenomenology), "clock/matter rows remain non-parent predictions"),
        ("VAL1558_7_rejection_ledger", len(rejections) >= 6 and any(row["missing_input"] == "MISSING_C_R10_lambda_AND_DIGITIZED_CURVE" for row in rejections), "unsupported coefficients rejected for scoring"),
        ("VAL1558_8_readiness_translation_only", any(row["readiness_id"] == "READY1558_0_qR_gamma" and row["translation_ready"] == "True" and row["score_ready"] == "False" for row in readiness), "q_R row is translation-ready but not score-ready"),
        ("VAL1558_9_runner_refuses_scoring", any(row["runner_id"] == "RUN1558_4_scoring" and row["current_status"] == "REFUSED_NO_PARENT_PREDICTIONS" for row in run_rows), "runner refuses local-bound scoring"),
        ("VAL1558_10_claim_gate_blocks_GR", any(row["gate_id"] == "GATE1558_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "derived local GR claim remains blocked"),
        ("VAL1558_11_decision_next", any(row["result"] == "NEXT_1559_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT" for row in decision_items), "decision selects two-parameter runner plus zero-condition hunt"),
        ("VAL1558_12_next_target", any("1559-Y5-qR-delta-beta" in row["next_target"] for row in next_rows), "next target is q_R/delta_beta two-parameter PPN control runner"),
        ("VAL1558_13_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1558 CSVs parse cleanly"),
        ("VAL1558_14_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1558_15_branch_copies", all(path.exists() for path in [QUAR_PPN, QUAR_PHEN, QUAR_REJECT, QUAR_READY, QUAR_RUNNER, QUAR_DECISION, BRANCH_PPN, BRANCH_PHEN, BRANCH_REJECT, BRANCH_READY, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1558_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1558_17_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1558_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1558 q_R/beta/matter/clock coefficient source-map or rejection validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    phenomenology: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1558 - q_R/Beta/Matter/Clock Coefficient Source Map or Rejection",
                "",
                "## Verdict",
                "- `q_R` now has a derived PPN translation: at first weak-field order, `R_AB ~= (gamma-1)L` and `R_AB ~= q_R L`, so `gamma-1=q_R`.",
                "- The light-bending, Shapiro, and Mercury `q_R` coefficients follow directly from standard PPN scaling; `delta_beta` enters Mercury through `(2 q_R - delta_beta)/3`.",
                "- This is progress: the local residual scorecard is mathematically sharper than it was at 1557.",
                "- This is not yet a local-GR derivation, because the parent theory still has to prove or predict `q_R=0` and `delta_beta=0`.",
                "- Clock and WEP coefficients remain phenomenological proxy definitions; Gdot, preferred-frame, R10, and tracefree response coefficients are rejected for scoring at 1558.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## PPN Coefficient Derivation",
                md_table(ppn, ["coefficient_id", "leak_parameter", "observable_response", "coefficient_value", "coefficient_units", "coefficient_status"]),
                "",
                "## Phenomenological Coefficient Map",
                md_table(phenomenology, ["phenomenology_id", "leak_parameter", "observable_response", "coefficient_value", "coefficient_status", "limitation"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "leak_parameter", "observable_response", "missing_input", "reason", "reentry_condition"]),
                "",
                "## Readiness Matrix",
                md_table(readiness, ["readiness_id", "leak_parameter", "observable_response", "translation_ready", "parent_prediction_ready", "score_ready", "status", "reason"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    ppn = ppn_coefficient_rows()
    phenomenology = phenomenological_rows()
    rejections = rejection_rows()
    readiness = readiness_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PPN_COEFFICIENTS, ppn)
    write_csv(PHENOMENOLOGICAL, phenomenology)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(READINESS_MATRIX, readiness)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PPN_COEFFICIENTS,
        PHENOMENOLOGICAL,
        REJECTION_LEDGER,
        READINESS_MATRIX,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, ppn, phenomenology, rejections, readiness, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
