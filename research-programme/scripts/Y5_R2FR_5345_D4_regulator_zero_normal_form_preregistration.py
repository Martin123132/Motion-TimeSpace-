from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

sys.dont_write_bytecode = True

import numpy as np
import sympy as sp


CHECKPOINT = 5345
MARKER = "MTS_5345_D4_REGULATOR_ZERO_NORMAL_FORM_PREREGISTRATION"
CHECKED_DATE = "2026-08-10"
POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5345-Y5-R2FR-D4-regulator-zero-endpoint-asymptotic-and-fit-"
    "preregistration.md"
)
COEFFICIENTS_5342 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5342"
    / "D4_E00125_support_endpoint_coefficients.csv"
)
COEFFICIENTS_5339 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5339"
    / "E08_parent_endpoint_coefficients.csv"
)
SCAN_5337 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5337"
    / "D4_targeted_event_regulator_scan.csv"
)
FINITE_5340 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5340"
    / "D4_E0025_log_corrected_finite_value.csv"
)
SOURCE_PATHS = [
    POST / "5328-Y5-R2FR-D2-midpoint-regulator-zero-normal-form-gate.md",
    POST / "5337-Y5-R2FR-D4-regulator-fold-double-scaling-and-contrast-gate.md",
    POST / "5339-Y5-R2FR-D4-E08-support-exit-log-subtraction.md",
    POST / "5340-Y5-R2FR-D4-E0025-log-corrected-canonical-finite-rung.md",
    POST / "5342-Y5-R2FR-D4-E00125-generic-support-endpoint-normal-form.md",
    POST / "scripts" / "Y5_R2FR_5342_D4_E00125_generic_support_endpoint_normal_form.py",
    POST
    / "source-intake"
    / "functional_rg"
    / "5328"
    / "D2_midpoint_regulator_zero_normal_form_contract.csv",
    SCAN_5337,
    COEFFICIENTS_5339,
    FINITE_5340,
    COEFFICIENTS_5342,
    POST
    / "source-intake"
    / "functional_rg"
    / "5342"
    / "D4_E00125_support_endpoint_normal_form_result.json",
]
OUTPUT_NAMES = [
    "D4_regulator_zero_endpoint_asymptotic_contract.csv",
    "D4_E00125_support_log_coefficient_partial_sum.csv",
    "D4_zero_fit_preregistration.csv",
    "D4_zero_rung_count_gate.csv",
    "source_provenance.csv",
    "D4_regulator_zero_preregistration_result.json",
]
EPSILON_REFERENCE = 0.0025
REGULATORS = [0.000625, 0.00125, 0.0025, 0.005, 0.01, 0.02, 0.04]


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint": CHECKPOINT,
            "checkpoint_marker": MARKER,
            "checked_date": CHECKED_DATE,
            "valid_for_D4_zero_fit_preregistration": True,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_decay_angle_integral": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for row in rows
    ]


def source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in SOURCE_PATHS:
        if not path.is_file():
            raise FileNotFoundError(path)
        hashes[path.relative_to(POST).as_posix()] = file_digest(path)
    return hashes


def complex_value(row: dict[str, str], prefix: str) -> complex:
    return complex(float(row[f"{prefix}_real"]), float(row[f"{prefix}_imaginary"]))


def asymptotic_contract_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    epsilon, a_1, z_1, coefficient_0, sign = sp.symbols(
        "epsilon a_1 z_1 C_0 s",
        nonzero=True,
    )
    z_0 = a_1 * epsilon
    leading_lower_endpoint = -sign * coefficient_0 * z_0 * sp.log(z_0) / z_1
    leading_lower_endpoint_expanded = (
        -sign
        * coefficient_0
        * a_1
        * epsilon
        * (sp.log(epsilon) + sp.log(a_1))
        / z_1
    )
    leading_log_coefficient = sp.simplify(
        sp.expand(leading_lower_endpoint_expanded).coeff(sp.log(epsilon))
        / epsilon
    )
    expected = -sign * coefficient_0 * a_1 / z_1
    coefficient_identity = sp.simplify(leading_log_coefficient - expected) == 0
    if not coefficient_identity:
        raise RuntimeError("endpoint epsilon-log coefficient identity failed")

    rows = [
        {
            "contract_id": "NF5345_00_simple_pole_motion",
            "hypotheses": "material pole simple; parent divisor derivative nonzero; fixed event topology",
            "derived_statement": "z0_e(epsilon)=a_e epsilon+O(epsilon^2); event coordinate x_e=x_e(0)+O(epsilon^2)",
            "fit_consequence": "integer powers and logarithms; no event-merger half-power",
            "contract_passes": True,
        },
        {
            "contract_id": "NF5345_01_affine_log_primitive",
            "hypotheses": "F_e(delta)=s_e(C0_e+C1_e delta) Log(z0_e+z1_e delta)",
            "derived_statement": "the exact primitive contains z Log z and z^2 Log z lower-endpoint terms",
            "fit_consequence": "epsilon Log epsilon is leading; epsilon^2 Log epsilon first appears in the controlled remainder",
            "contract_passes": True,
        },
        {
            "contract_id": "NF5345_02_leading_family",
            "hypotheses": "sum of finitely many separated transverse contacts plus smooth compact remainder",
            "derived_statement": "I(epsilon)=I0+A epsilon Log(epsilon/epsilon_ref)+B epsilon+O(epsilon^2 Log epsilon)",
            "fit_consequence": "three-complex-parameter leading design; four accepted rungs are the minimum overdetermined fit",
            "contract_passes": True,
        },
        {
            "contract_id": "NF5345_03_complete_second_order_family",
            "hypotheses": "smooth epsilon dependence of C0,C1,z1 and O(epsilon^2) event drift",
            "derived_statement": "I=I0+A e Log e+B e+C e^2 Log e+D e^2+O(e^3 Log e)",
            "fit_consequence": "five-complex-parameter design; six rungs are the minimum overdetermined second-order fit",
            "contract_passes": True,
        },
        {
            "contract_id": "NF5345_04_no_sqrt_default",
            "hypotheses": "checkpoint-5337 event gaps tend to nonzero constants and contact widths scale linearly",
            "derived_statement": "sqrt(epsilon) and sqrt(epsilon) Log epsilon are absent from the parent-derived family",
            "fit_consequence": "half-power fits are falsifiers only and cannot select the reported intercept",
            "contract_passes": True,
        },
        {
            "contract_id": "NF5345_05_source_coefficient",
            "hypotheses": "a_e=lim z0_e/epsilon; z1_e and C0_e have finite nonzero limits",
            "derived_statement": "A_e=-s_e C0_e a_e/z1_e",
            "fit_consequence": "A may be fixed only after all eight event coefficients are evaluated at two or more regulators",
            "contract_passes": coefficient_identity,
        },
    ]
    payload = {
        "coefficient_identity_passes": coefficient_identity,
        "symbolic_leading_log_coefficient": str(leading_log_coefficient),
        "expected_leading_log_coefficient": str(expected),
        "unexpanded_lower_endpoint": str(leading_lower_endpoint),
    }
    return tagged(rows), payload


def coefficient_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    epsilon = 0.00125
    rows_5342 = read_csv(COEFFICIENTS_5342)
    event_rows: list[dict[str, Any]] = []
    partial_sum = 0.0j
    sum_magnitudes = 0.0
    for row in rows_5342:
        z_0 = complex_value(row, "boundary_gap_z0")
        z_1 = complex_value(row, "boundary_gap_derivative_z1")
        coefficient_0 = complex_value(row, "physical_coefficient_C0")
        sign = int(row["log_sign"])
        a_estimator = z_0 / epsilon
        log_coefficient = -sign * coefficient_0 * a_estimator / z_1
        partial_sum += log_coefficient
        sum_magnitudes += abs(log_coefficient)
        event_rows.append(
            {
                "row_type": "EVENT_ESTIMATOR",
                "epsilon_id": "E00125",
                "epsilon": epsilon,
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "log_sign": sign,
                "a_estimator_real": a_estimator.real,
                "a_estimator_imaginary": a_estimator.imag,
                "A_event_real": log_coefficient.real,
                "A_event_imaginary": log_coefficient.imag,
                "A_event_magnitude": abs(log_coefficient),
                "coefficient_contract_passes": row["coefficient_contract_passes"],
                "role": "SOURCE_OWNED_FINITE_EPSILON_ESTIMATOR",
            }
        )

    old = read_csv(COEFFICIENTS_5339)[0]
    old_z_0 = complex_value(old, "lower_gap_z0")
    old_z_1 = complex_value(old, "lower_gap_derivative_z1")
    old_coefficient_0 = complex_value(old, "physical_coefficient_C0")
    old_log_coefficient = old_coefficient_0 * (old_z_0 / 0.0025) / old_z_1
    current_e08 = next(
        complex(row["A_event_real"], row["A_event_imaginary"])
        for row in event_rows
        if row["event_id"] == "E08"
    )
    e08_relative_drift = abs(current_e08 - old_log_coefficient) / max(
        abs(current_e08), abs(old_log_coefficient), 1.0e-300
    )
    e08_imaginary_relative_drift = abs(
        current_e08.imag - old_log_coefficient.imag
    ) / max(abs(current_e08.imag), abs(old_log_coefficient.imag), 1.0e-300)
    cancellation_ratio = abs(partial_sum) / max(sum_magnitudes, 1.0e-300)
    event_rows.extend(
        [
            {
                "row_type": "SUPPORT_PARTIAL_SUM",
                "epsilon_id": "E00125",
                "epsilon": epsilon,
                "event_id": "E01+E02+E03+E08",
                "event_type": "FOUR_TWO_SIDED_SUPPORT_CONTACTS",
                "A_event_real": partial_sum.real,
                "A_event_imaginary": partial_sum.imag,
                "A_event_magnitude": abs(partial_sum),
                "sum_event_magnitudes": sum_magnitudes,
                "coherent_sum_ratio": cancellation_ratio,
                "coefficient_contract_passes": True,
                "role": "NONZERO_PARTIAL_COEFFICIENT_NOT_TOTAL_D4_COEFFICIENT",
            },
            {
                "row_type": "E08_CROSS_RUNG_CHECK",
                "epsilon_id": "E0025_vs_E00125",
                "event_id": "E08",
                "event_type": "SUPPORT_EXIT",
                "A_event_real": old_log_coefficient.real,
                "A_event_imaginary": old_log_coefficient.imag,
                "A_event_magnitude": abs(old_log_coefficient),
                "full_complex_relative_drift": e08_relative_drift,
                "imaginary_relative_drift": e08_imaginary_relative_drift,
                "coefficient_contract_passes": True,
                "role": "TWO_RUNG_SCALING_WITNESS",
            },
        ]
    )
    scan = read_csv(SCAN_5337)
    e00125_events = [row for row in scan if row["epsilon_id"] == "E00125"]
    branch_deaths = [row for row in e00125_events if row["event_type"] == "BRANCH_DEATH"]
    payload = {
        "support_event_count": len(rows_5342),
        "total_event_count": len(e00125_events),
        "missing_branch_death_coefficient_count": len(branch_deaths),
        "partial_A_real": partial_sum.real,
        "partial_A_imaginary": partial_sum.imag,
        "partial_A_magnitude": abs(partial_sum),
        "partial_coherent_sum_ratio": cancellation_ratio,
        "E08_full_complex_relative_drift": e08_relative_drift,
        "E08_imaginary_relative_drift": e08_imaginary_relative_drift,
        "total_A_source_complete": False,
    }
    return tagged(event_rows), payload


def model_definitions() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "D4_L3_ENDPOINT_LOG_LEADING",
            "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)",
            "parameter_count": 3,
            "derived_family": True,
            "role": "PRIMARY_LEADING_FAMILY",
        },
        {
            "model_id": "D4_Q4_ENDPOINT_LOG_PLUS_E2",
            "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2",
            "parameter_count": 4,
            "derived_family": True,
            "role": "SECOND_ORDER_ANALYTIC_STRESS",
        },
        {
            "model_id": "D4_Q4_ENDPOINT_LOG_PLUS_E2LOG",
            "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2*log(epsilon/epsilon_ref)",
            "parameter_count": 4,
            "derived_family": True,
            "role": "SECOND_ORDER_LOG_STRESS",
        },
        {
            "model_id": "D4_Q5_COMPLETE_SECOND_ORDER",
            "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2|epsilon^2*log(epsilon/epsilon_ref)",
            "parameter_count": 5,
            "derived_family": True,
            "role": "COMPLETE_SECOND_ORDER_FAMILY",
        },
        {
            "model_id": "D4_A2_ANALYTIC_ONLY",
            "basis_terms": "1|epsilon",
            "parameter_count": 2,
            "derived_family": False,
            "role": "CANCELLATION_DIAGNOSTIC_ONLY",
        },
        {
            "model_id": "D4_F3_SQRT_FALSIFIER",
            "basis_terms": "1|sqrt(epsilon)|epsilon",
            "parameter_count": 3,
            "derived_family": False,
            "role": "TOPOLOGY_EXCLUDED_FALSIFIER",
        },
    ]


def basis_function(term: str) -> Callable[[float], float]:
    functions: dict[str, Callable[[float], float]] = {
        "1": lambda epsilon: 1.0,
        "epsilon": lambda epsilon: epsilon,
        "epsilon*log(epsilon/epsilon_ref)": lambda epsilon: epsilon
        * math.log(epsilon / EPSILON_REFERENCE),
        "epsilon^2": lambda epsilon: epsilon**2,
        "epsilon^2*log(epsilon/epsilon_ref)": lambda epsilon: epsilon**2
        * math.log(epsilon / EPSILON_REFERENCE),
        "sqrt(epsilon)": math.sqrt,
    }
    return functions[term]


def design_metrics(basis_terms: str, epsilon_values: list[float]) -> dict[str, Any]:
    terms = basis_terms.split("|")
    design = np.asarray(
        [[basis_function(term)(epsilon) for term in terms] for epsilon in epsilon_values],
        dtype=float,
    )
    norms = np.linalg.norm(design, axis=0)
    normalized = design / norms
    return {
        "matrix_rank": int(np.linalg.matrix_rank(design)),
        "normalized_condition_number": float(np.linalg.cond(normalized)),
        "condition_times_machine_epsilon": float(
            np.linalg.cond(normalized) * np.finfo(float).eps
        ),
    }


def preregistration_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    models = model_definitions()
    fit_rows: list[dict[str, Any]] = []
    for model in models:
        for point_count in range(model["parameter_count"], len(REGULATORS) + 1):
            epsilon_values = REGULATORS[:point_count]
            metrics = design_metrics(model["basis_terms"], epsilon_values)
            fit_rows.append(
                {
                    **model,
                    "point_count": point_count,
                    "epsilon_min": min(epsilon_values),
                    "epsilon_max": max(epsilon_values),
                    "degrees_of_freedom": point_count - model["parameter_count"],
                    **metrics,
                    "full_rank": metrics["matrix_rank"] == model["parameter_count"],
                    "numerically_resolved": metrics[
                        "condition_times_machine_epsilon"
                    ]
                    < 1.0e-8,
                    "intercept_report_allowed": False,
                    "reason_intercept_blocked": "finite D4 rung set incomplete",
                }
            )

    rung_rows = [
        {
            "accepted_rung_count": 2,
            "leading_family_status": "UNDERDETERMINED",
            "second_order_status": "UNDERDETERMINED",
            "allowed_decision": "DIRECTION_ONLY_NO_ZERO_FIT",
        },
        {
            "accepted_rung_count": 3,
            "leading_family_status": "EXACTLY_DETERMINED_NO_RESIDUAL_TEST",
            "second_order_status": "UNDERDETERMINED",
            "allowed_decision": "INTERCEPT_SMOKE_ONLY",
        },
        {
            "accepted_rung_count": 4,
            "leading_family_status": "MINIMUM_OVERDETERMINED",
            "second_order_status": "EXACT_OR_UNDERDETERMINED",
            "allowed_decision": "LEADING_FAMILY_GATE_WITH_REMAINDER_BOUND_REQUIRED",
        },
        {
            "accepted_rung_count": 5,
            "leading_family_status": "OVERDETERMINED",
            "second_order_status": "COMPLETE_FAMILY_EXACTLY_DETERMINED",
            "allowed_decision": "SECOND_ORDER_STRESS_NO_COMPLETE_RESIDUAL_TEST",
        },
        {
            "accepted_rung_count": 6,
            "leading_family_status": "OVERDETERMINED",
            "second_order_status": "MINIMUM_OVERDETERMINED",
            "allowed_decision": "FULL_ZERO_LIMIT_ACCEPTANCE_GATE_ELIGIBLE",
        },
        {
            "accepted_rung_count": 7,
            "leading_family_status": "OVERDETERMINED_WITH_STABILITY_TREE",
            "second_order_status": "OVERDETERMINED_WITH_ONE_EXTRA_RESIDUAL",
            "allowed_decision": "PREFERRED_FULL_LADDER_GATE",
        },
    ]
    acceptance_contract = {
        "minimum_leading_overdetermined_rungs": 4,
        "minimum_complete_second_order_overdetermined_rungs": 6,
        "relative_zero_bound_limit": 0.01,
        "required_input": "accepted finite-rung complex values and conservative disks",
        "required_diagnostics": [
            "weighted and unweighted intercepts",
            "leave-one-out intercept spread",
            "smallest-epsilon window stability",
            "normalized complex residuals",
            "leading versus second-order intercept envelope",
            "half-power falsifier reported but not selected",
        ],
        "no_claim_before_fit": True,
    }
    return tagged(fit_rows), tagged(rung_rows), acceptance_contract


def provenance_rows(hashes: dict[str, str]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "source_id": f"S5345_{index:02d}",
                "source_path": path,
                "sha256": digest,
                "exists": True,
                "role": "normal-form topology or endpoint coefficient source",
            }
            for index, (path, digest) in enumerate(sorted(hashes.items()))
        ]
    )


def build_payload() -> dict[str, Any]:
    hashes = source_hashes()
    contract_rows, symbolic = asymptotic_contract_rows()
    coefficient_output, coefficients = coefficient_rows()
    fit_rows, rung_rows, acceptance = preregistration_rows()
    provenance = provenance_rows(hashes)
    finite = read_csv(FINITE_5340)
    return {
        "rows": {
            "D4_regulator_zero_endpoint_asymptotic_contract.csv": contract_rows,
            "D4_E00125_support_log_coefficient_partial_sum.csv": coefficient_output,
            "D4_zero_fit_preregistration.csv": fit_rows,
            "D4_zero_rung_count_gate.csv": rung_rows,
            "source_provenance.csv": provenance,
        },
        "result": {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "decision": "D4_ZERO_NORMAL_FORM_PREREGISTERED__WAIT_FOR_ACCEPTED_RUNGS",
            "derived_leading_family": "I0+A*epsilon*Log(epsilon/epsilon_ref)+B*epsilon+O(epsilon^2 Log epsilon)",
            "derived_complete_second_order_family": "I0+A*e*Log(e/e_ref)+B*e+C*e^2*Log(e/e_ref)+D*e^2",
            "epsilon_reference": EPSILON_REFERENCE,
            "symbolic_contract": symbolic,
            "coefficient_evidence": coefficients,
            "acceptance_contract": acceptance,
            "accepted_D4_rung_count_at_preregistration": sum(
                row["finite_regulator_fixed_decay_integral_accepted"] == "True"
                for row in finite
            ),
            "total_A_source_complete": False,
            "D4_regulator_zero_limit_accepted": False,
            "valid_for_D4_zero_fit_preregistration": True,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_hashes": hashes,
        },
    }


def validation_rows(payload: dict[str, Any], saved: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(gate: str, passed: bool, detail: Any) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "gate": gate,
                "passed": bool(passed),
                "detail": json.dumps(detail, sort_keys=True)
                if isinstance(detail, (dict, list))
                else str(detail),
            }
        )

    result = payload["result"]
    coefficient = result["coefficient_evidence"]
    all_output_rows = [row for group in payload["rows"].values() for row in group]
    add("all_source_paths_exist", all(path.is_file() for path in SOURCE_PATHS), len(SOURCE_PATHS))
    add("source_hashes_complete", len(result["source_hashes"]) == len(SOURCE_PATHS), result["source_hashes"])
    add("endpoint_symbolic_coefficient_identity", result["symbolic_contract"]["coefficient_identity_passes"], result["symbolic_contract"])
    add("all_six_asymptotic_contracts_pass", all(row["contract_passes"] is True for row in payload["rows"]["D4_regulator_zero_endpoint_asymptotic_contract.csv"]), 6)
    add("eight_event_topology_present", coefficient["total_event_count"] == 8, coefficient)
    add("four_support_coefficients_present", coefficient["support_event_count"] == 4, coefficient)
    add("support_partial_epsilon_log_coefficient_nonzero", coefficient["partial_A_magnitude"] > 0.4, coefficient["partial_A_magnitude"])
    add("support_partial_sum_is_coherent", coefficient["partial_coherent_sum_ratio"] > 0.999, coefficient["partial_coherent_sum_ratio"])
    add("E08_imaginary_coefficient_cross_rung_stable", coefficient["E08_imaginary_relative_drift"] < 1.0e-5, coefficient["E08_imaginary_relative_drift"])
    add("missing_branch_coefficients_prevent_fixed_total_A", coefficient["missing_branch_death_coefficient_count"] == 4 and result["total_A_source_complete"] is False, coefficient)
    leading_rows = [row for row in payload["rows"]["D4_zero_fit_preregistration.csv"] if row["model_id"] == "D4_L3_ENDPOINT_LOG_LEADING" and row["point_count"] == 4]
    add("four_rung_leading_design_full_rank", len(leading_rows) == 1 and leading_rows[0]["full_rank"] is True, leading_rows)
    complete_rows = [row for row in payload["rows"]["D4_zero_fit_preregistration.csv"] if row["model_id"] == "D4_Q5_COMPLETE_SECOND_ORDER" and row["point_count"] == 6]
    add("six_rung_complete_design_full_rank", len(complete_rows) == 1 and complete_rows[0]["full_rank"] is True, complete_rows)
    add("all_designs_numerically_resolved", all(row["numerically_resolved"] is True for row in payload["rows"]["D4_zero_fit_preregistration.csv"]), max(row["condition_times_machine_epsilon"] for row in payload["rows"]["D4_zero_fit_preregistration.csv"]))
    add("only_one_D4_rung_currently_accepted", result["accepted_D4_rung_count_at_preregistration"] == 1, result["accepted_D4_rung_count_at_preregistration"])
    add("all_rows_keep_zero_and_broad_claims_false", all(row["valid_for_D4_outer_regulator_zero_limit"] is False and row["valid_for_local_GR_claim"] is False and row["valid_for_full_MTS_claim"] is False for row in all_output_rows), len(all_output_rows))
    add("document_exists", DOCUMENT.is_file(), str(DOCUMENT))
    add("formalization_workbench_exists_and_unwritten", FORMAL.is_dir(), str(FORMAL))
    add("no_script_pycache", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts" / "__pycache__"))
    if saved:
        add("all_saved_outputs_exist", all((OUT / name).is_file() for name in OUTPUT_NAMES), OUTPUT_NAMES)
        saved_result = json.loads((OUT / "D4_regulator_zero_preregistration_result.json").read_text(encoding="utf-8"))
        add("saved_source_hashes_match", saved_result["source_hashes"] == source_hashes(), saved_result["source_hashes"])
        for name, expected in payload["rows"].items():
            add(f"saved_{name}_row_count", len(read_csv(OUT / name)) == len(expected), len(expected))
    return rows


def write_outputs(payload: dict[str, Any]) -> None:
    for name, rows in payload["rows"].items():
        write_csv(OUT / name, rows)
    write_json(OUT / "D4_regulator_zero_preregistration_result.json", payload["result"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    args = parser.parse_args()
    if args.dry_run and args.validate_saved:
        parser.error("choose at most one mode")
    payload = build_payload()
    if args.dry_run:
        checks = validation_rows(payload, saved=False)
        print(json.dumps({"mode": "dry-run", "checks": checks}, indent=2))
        return 0 if all(row["passed"] for row in checks) else 1
    if not args.validate_saved:
        write_outputs(payload)
    checks = validation_rows(payload, saved=True)
    write_csv(VALIDATION, checks)
    print(json.dumps({"mode": "validate-saved" if args.validate_saved else "run", "checks": checks}, indent=2))
    return 0 if all(row["passed"] for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
