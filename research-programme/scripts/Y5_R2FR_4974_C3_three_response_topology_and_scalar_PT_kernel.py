from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.integrate import quad


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4974"

SOURCE_2605 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4973"
    / "src-2605.29159"
    / "main_new.tex"
)
SOURCE_4911_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_4911_full_offshell_a6_template_projector.py"
)
SOURCE_4912_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector.py"
)
SOURCE_4911_DOC = (
    POST
    / "4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md"
)
SOURCE_4912_DOC = (
    POST
    / "4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-continuum-projector-recovery.md"
)
SOURCE_4935_DOC = (
    POST
    / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md"
)
SOURCE_4973_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4973"
    / "C3_fixed_point_form_factor_kernel_results.json"
)

SCHEME_LOCK_CSV = SOURCE / "C3_parent_scheme_lock.csv"
TOPOLOGY_CSV = SOURCE / "C3_three_response_topology.csv"
SCALAR_KERNEL_CSV = SOURCE / "C3_scalar_PT_m3_local_kernel.csv"
HELICITY_CSV = SOURCE / "C3_scalar_PT_m3_helicity_projection.csv"
COVERAGE_CSV = SOURCE / "C3_kernel_sector_coverage.csv"
RESULT_JSON = SOURCE / "C3_three_response_topology_and_scalar_PT_kernel_results.json"

MARKER = "MTS_4974_C3_THREE_RESPONSE_AND_SCALAR_PT_KERNEL"
CHECKED_DATE = "2026-07-13"

EXPECTED_HASHES = {
    SOURCE_2605: "e3f783efb9df57d19c49e96215e1fbf27470b6053c45d133887ba7233a6c974a",
    SOURCE_4911_SCRIPT: "a99e64b66812fb6e17e1c89fc7acd7c7cb8e750799f629f0c1e07f16796e694f",
    SOURCE_4912_SCRIPT: "8edae30d1df642d711a67add28ca07527f8502f4e317d27ab2292f7c27518c28",
    SOURCE_4911_DOC: "7563e7d0137330d33152139a9345e87c0b83f9698ca25f5f5bec7e767f87b8ea",
    SOURCE_4912_DOC: "7e4f85db4da96bdef35895c3947a24a5162045bbef665cf32b668c7bee6febff",
    SOURCE_4935_DOC: "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    SOURCE_4973_RESULT: "1cd8cd9e789832da84039dda72af2d4deed72fc310fe18dcc9250a07345ceeb1",
}

SCALAR_C3_CONSTANT = 1.0 / (30240.0 * (4.0 * math.pi) ** 2)
HELICITY_PROJECTORS = {"++++": -15.0, "-+++": -1.5}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def parse_vertex_indices(factor: str) -> tuple[int, ...]:
    if not factor.startswith("A"):
        raise ValueError(f"not a Hessian derivative factor: {factor}")
    return tuple(int(value) for value in factor[1:])


def hessian_factor(indices: tuple[int, ...]) -> str:
    return "A" + "".join(str(value) for value in sorted(indices))


def canonical_trace(word: tuple[str, ...]) -> tuple[str, ...]:
    rotations = [word[index:] + word[:index] for index in range(len(word))]
    preferred = [rotation for rotation in rotations if rotation[0] == "G"]
    return min(preferred or rotations)


def differentiate_trace_terms(
    terms: dict[tuple[str, ...], int], source_index: int
) -> dict[tuple[str, ...], int]:
    differentiated: defaultdict[tuple[str, ...], int] = defaultdict(int)
    for word, coefficient in terms.items():
        for position, factor in enumerate(word):
            if factor == "G":
                replacement = ("G", hessian_factor((source_index,)), "G")
                new_word = word[:position] + replacement + word[position + 1 :]
                differentiated[canonical_trace(new_word)] -= coefficient
            elif factor.startswith("A"):
                indices = parse_vertex_indices(factor) + (source_index,)
                replacement = (hessian_factor(indices),)
                new_word = word[:position] + replacement + word[position + 1 :]
                differentiated[canonical_trace(new_word)] += coefficient
    return {
        word: coefficient
        for word, coefficient in differentiated.items()
        if coefficient != 0
    }


def determinant_three_response_terms() -> dict[tuple[str, ...], int]:
    terms = {canonical_trace(("G", "A1")): 1}
    terms = differentiate_trace_terms(terms, 2)
    return differentiate_trace_terms(terms, 3)


def wetterich_three_response_terms() -> dict[tuple[str, ...], int]:
    terms = {canonical_trace(("G", "Rdot")): 1}
    for source_index in (1, 2, 3):
        terms = differentiate_trace_terms(terms, source_index)
    return terms


def vertex_content(word: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(len(parse_vertex_indices(factor)) + 2 for factor in word if factor.startswith("A"))
    )


def topology_class(content: tuple[int, ...]) -> str:
    if content == (5,):
        return "Gamma5_contact"
    if content == (3, 4):
        return "Gamma3_Gamma4_mixed"
    if content == (3, 3, 3):
        return "Gamma3_cubed_triangle"
    return "other"


def topology_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    determinant_terms = determinant_three_response_terms()
    wetterich_terms = wetterich_three_response_terms()
    rows: list[dict[str, Any]] = [
        {
            "flow_type": "superseded_two_point_template",
            "term_id": "C3TOP4974_ERRATUM",
            "coefficient": "not_applicable",
            "trace_word": "Gamma4 plus Gamma3-Gamma3",
            "vertex_content": "(4) and (3,3)",
            "topology_class": "two_metric_response_only",
            "interpretation": "the 2605.29159 displayed topology is the second metric derivative used for curvature-squared form factors; it is not a C3 three-response kernel",
            "status": "SUPERSEDED_FOR_C3",
        }
    ]
    for flow_type, terms in (
        ("one_loop_log_determinant", determinant_terms),
        ("exact_Wetterich_field_independent_Rdot", wetterich_terms),
    ):
        for index, (word, coefficient) in enumerate(sorted(terms.items())):
            content = vertex_content(word)
            rows.append(
                {
                    "flow_type": flow_type,
                    "term_id": f"C3TOP4974_{flow_type}_{index:02d}",
                    "coefficient": coefficient,
                    "trace_word": "Tr[" + " ".join(word) + "]",
                    "vertex_content": str(content),
                    "topology_class": topology_class(content),
                    "interpretation": "A_i=delta_i Gamma2=Gamma3; A_ij=Gamma4; A_123=Gamma5",
                    "status": "EXACT_THIRD_RESPONSE_TERM",
                }
            )

    def class_summary(terms: dict[tuple[str, ...], int]) -> dict[str, Any]:
        counts: defaultdict[str, int] = defaultdict(int)
        coefficient_sums: defaultdict[str, int] = defaultdict(int)
        for word, coefficient in terms.items():
            class_name = topology_class(vertex_content(word))
            counts[class_name] += 1
            coefficient_sums[class_name] += coefficient
        return {
            "term_count": len(terms),
            "counts": dict(counts),
            "coefficient_sums": dict(coefficient_sums),
        }

    return tagged(rows), {
        "determinant": class_summary(determinant_terms),
        "wetterich": class_summary(wetterich_terms),
        "determinant_terms": {
            " ".join(word): coefficient for word, coefficient in determinant_terms.items()
        },
    }


def scheme_lock_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "lock_id": "C3LOCK4974_00_SPLIT",
                "object": "metric field split",
                "selected_value": "g_mn=gbar_mn+h_mn; linear background split",
                "source_path": relative(SOURCE_2605),
                "scope": "background proper-time benchmark branch",
                "status": "SOURCE_LOCKED",
            },
            {
                "lock_id": "C3LOCK4974_01_GAUGE",
                "object": "gravity gauge",
                "selected_value": "Lorentz/de Donder gauge alpha=1 and omega_bar=1/2",
                "source_path": relative(SOURCE_2605),
                "scope": "minimal EH Hessian and ghost operator",
                "status": "SOURCE_LOCKED",
            },
            {
                "lock_id": "C3LOCK4974_02_REGULATOR",
                "object": "proper-time regulator",
                "selected_value": "rho_m with m=3; epsilon=1 form-factor scheme; free-scalar benchmark eta_psi=0",
                "source_path": relative(SOURCE_2605),
                "scope": "first-iteration regulator-resolved scalar row",
                "status": "SOURCE_LOCKED_BENCHMARK",
            },
            {
                "lock_id": "C3LOCK4974_03_GRAVITY_GHOST",
                "object": "gravity and ghost inverse operators",
                "selected_value": "EH Laplace-type Hessian plus source-standard vector ghost in the locked gauge",
                "source_path": relative(SOURCE_2605),
                "scope": "propagators locked; C3 Gamma3/Gamma4/Gamma5 vertices not yet assembled",
                "status": "HESSIAN_LOCKED_VERTICES_OPEN",
            },
            {
                "lock_id": "C3LOCK4974_04_MOTION",
                "object": "free massive motion-scalar benchmark Hessian",
                "selected_value": "Gamma_psi^(2)=Z_psi(-Box+m_gap^2); eta_psi=0 benchmark; one real pole",
                "source_path": f"{relative(SOURCE_4935_DOC)};{relative(SOURCE_4912_DOC)}",
                "scope": "exact local C3 threshold benchmark, not the interacting motion completion",
                "status": "CALCULABLE_BENCHMARK_LOCKED",
            },
        ]
    )


def normalized_scalar_kernel(x_value: float, eta_psi: float = 0.0, epsilon: float = 1.0) -> float:
    return (
        -3.0
        * (2.0 - epsilon * eta_psi)
        * x_value**3
        / (1.0 + x_value) ** 4
    )


def scalar_kernel_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    x_symbol = sp.symbols("x", positive=True)
    normalized_exact = -6 * x_symbol**3 / (1 + x_symbol) ** 4
    positive_weight = sp.simplify(-normalized_exact / (2 * x_symbol))
    cumulative_exact = sp.simplify(sp.integrate(positive_weight, (x_symbol, 0, x_symbol)))
    integral_exact = sp.integrate(positive_weight, (x_symbol, 0, sp.oo))
    derivative = sp.factor(sp.diff(normalized_exact, x_symbol))
    peak_value = sp.simplify(normalized_exact.subs(x_symbol, 3))

    x_values = (
        1.0e-8,
        1.0e-6,
        1.0e-4,
        1.0e-2,
        0.1,
        0.3,
        1.0,
        3.0,
        10.0,
        100.0,
        1.0e4,
        1.0e6,
        1.0e8,
    )
    rows: list[dict[str, Any]] = []
    for x_value in x_values:
        kernel_value = normalized_scalar_kernel(x_value)
        cumulative = (x_value / (1.0 + x_value)) ** 3
        rows.append(
            {
                "row_id": f"C3SCALAR4974_{len(rows):02d}",
                "x_equals_3k2_over_m2": x_value,
                "k_over_m": math.sqrt(x_value / 3.0),
                "m2_dzeta_dlnk_over_C0": kernel_value,
                "positive_UV_to_IR_weight": -kernel_value / (2.0 * x_value),
                "cumulative_IR_to_x_fraction": cumulative,
                "IR_remainder_fraction": 1.0 - cumulative,
                "equation": "d_t zeta=(C0/m^2)[-6 x^3/(1+x)^4], x=3k^2/m^2",
                "status": "EXACT_FREE_SCALAR_PT_M3_LOCAL_KERNEL",
            }
        )

    numeric_integral, numeric_error = quad(
        lambda value: 3.0 * value**2 / (1.0 + value) ** 4,
        0.0,
        np.inf,
        epsabs=1e-13,
        epsrel=1e-13,
        limit=300,
    )
    half_root = 2.0 ** (-1.0 / 3.0)
    half_x = half_root / (1.0 - half_root)
    summary = {
        "C0_exact": "1/[30240(4*pi)^2]",
        "C0_numeric": SCALAR_C3_CONSTANT,
        "effective_mass_squared": "M_k^2=m^2+3k^2",
        "proper_time_identity": "d_t Gamma_k=(3k^2)^3 partial_(M^2)^3 Gamma_1loop(M^2)|M^2=m^2+3k^2",
        "local_flow": "d_t zeta_k=-162 C0 k^6/(m^2+3k^2)^4",
        "normalized_kernel": str(normalized_exact),
        "positive_weight": str(positive_weight),
        "cumulative_fraction": str(cumulative_exact),
        "integral_exact": str(integral_exact),
        "integral_numeric": numeric_integral,
        "integral_numeric_error": numeric_error,
        "kernel_derivative": str(derivative),
        "peak_x": 3.0,
        "peak_value_exact": str(peak_value),
        "half_integral_x": half_x,
        "IR_asymptotic": "m2*d_t_zeta/C0=-6x^3+O(x^4)",
        "UV_asymptotic": "m2*d_t_zeta/C0=-6/x+O(1/x^2)",
    }
    return tagged(rows), summary


def helicity_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    x_values = (1.0e-4, 1.0e-2, 0.1, 1.0, 3.0, 10.0, 100.0, 1.0e4)
    for x_value in x_values:
        scalar_source = normalized_scalar_kernel(x_value)
        for helicity, projector in HELICITY_PROJECTORS.items():
            rows.append(
                {
                    "projection_id": f"C3HEL4974_{helicity}_{x_value:g}",
                    "helicity": helicity,
                    "C3_projector": projector,
                    "x_equals_3k2_over_m2": x_value,
                    "normalized_scalar_C3_source": scalar_source,
                    "projected_helicity_source": projector * scalar_source,
                    "integrated_local_coefficient_over_C0_per_m2": projector,
                    "status": "LOCAL_C3_OPERATOR_HELICITY_PROJECTION",
                }
            )
    ratios: list[float] = []
    for x_value in x_values:
        all_plus = next(
            row["projected_helicity_source"]
            for row in rows
            if row["helicity"] == "++++" and row["x_equals_3k2_over_m2"] == x_value
        )
        single_minus = next(
            row["projected_helicity_source"]
            for row in rows
            if row["helicity"] == "-+++" and row["x_equals_3k2_over_m2"] == x_value
        )
        ratios.append(float(all_plus / single_minus))
    return tagged(rows), {
        "projector_all_plus": HELICITY_PROJECTORS["++++"],
        "projector_single_minus": HELICITY_PROJECTORS["-+++"],
        "ratios": ratios,
        "maximum_factor_ten_residual": max(abs(value - 10.0) for value in ratios),
        "scope": "local C3 operator projection; not an independent finite four-graviton form-factor calculation",
    }


def coverage_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "sector": "free_massive_real_scalar",
                "Gamma2_status": "EXACT",
                "Gamma3_Gamma4_Gamma5_status": "EXACT_METRIC_DERIVATIVES_IN_4912_DETERMINANT",
                "regulator_status": "PT_M3_ETA0_LOCKED",
                "local_C3_kernel_status": "CALCULATED_AND_INTEGRATED",
                "finite_momentum_status": "NOT_YET_PROJECTED",
                "physical_log_status": "NOT_TESTED_BY_LOCAL_THRESHOLD",
                "next_calculation": "apply the same mass-derivative construction to the finite-momentum 4912 determinant response",
            },
            {
                "sector": "interacting_motion_scalar",
                "Gamma2_status": "LOCAL_MASS_GAP_AND_O4_HESSIANS_PARTIAL",
                "Gamma3_Gamma4_Gamma5_status": "INTERACTION_AND_O4_CONTACTS_NOT_ASSEMBLED",
                "regulator_status": "PT_M3_BRANCH_AVAILABLE_ETA_PSI_TRAJECTORY_OPEN",
                "local_C3_kernel_status": "FREE_POLE_BENCHMARK_ONLY",
                "finite_momentum_status": "OPEN",
                "physical_log_status": "OPEN",
                "next_calculation": "insert eta_psi, pole residues, O4, and interaction contacts without changing the topology",
            },
            {
                "sector": "graviton",
                "Gamma2_status": "EH_LAPLACE_HESSIAN_SOURCE_LOCKED",
                "Gamma3_Gamma4_Gamma5_status": "GAMMA5_AND_MIXED_VERTEX_SET_NOT_ASSEMBLED",
                "regulator_status": "PT_M3_EPSILON1_LOCKED",
                "local_C3_kernel_status": "CURRENT_LOCAL_BETA_ONLY",
                "finite_momentum_status": "OPEN",
                "physical_log_status": "ENDPOINT_ONLY",
                "next_calculation": "derive the complete EH Gamma3 Gamma4 Gamma5 contractions in the locked gauge",
            },
            {
                "sector": "ghost",
                "Gamma2_status": "VECTOR_GHOST_OPERATOR_SOURCE_LOCKED",
                "Gamma3_Gamma4_Gamma5_status": "BACKGROUND_METRIC_CONTACTS_NOT_ASSEMBLED_TO_THIRD_RESPONSE",
                "regulator_status": "PT_M3_LOCKED",
                "local_C3_kernel_status": "COMBINED_LOCAL_BETA_ONLY",
                "finite_momentum_status": "OPEN",
                "physical_log_status": "ENDPOINT_ONLY",
                "next_calculation": "derive ghost metric contacts through the three-response and combine before projection",
            },
            {
                "sector": "four_graviton_physical_amplitude",
                "Gamma2_status": "NOT_THE_LIMITING_OBJECT",
                "Gamma3_Gamma4_Gamma5_status": "C3_THREE_RESPONSE_IS_NECESSARY_NOT_SUFFICIENT",
                "regulator_status": "COMMON_SCHEME_MATCH_REQUIRED",
                "local_C3_kernel_status": "TREE_NORMALIZATION_EXACT",
                "finite_momentum_status": "QUARTIC_CURVATURE_FORM_FACTORS_ALSO_REQUIRED",
                "physical_log_status": "4972_ENDPOINT_EXACT",
                "next_calculation": "after the C3 kernel closes, include the independent R4 form-factor sector for complete 2-to-2 matching",
            },
        ]
    )


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)

    observed_hashes = {path: digest(path) for path in EXPECTED_HASHES}
    hash_checks = {
        relative(path): observed_hashes[path] == expected
        for path, expected in EXPECTED_HASHES.items()
    }
    source_2605_text = SOURCE_2605.read_text(encoding="utf-8")
    source_4912_text = SOURCE_4912_DOC.read_text(encoding="utf-8")

    topology, topology_summary = topology_rows()
    scheme_lock = scheme_lock_rows()
    scalar_kernel, scalar_summary = scalar_kernel_rows()
    helicity, helicity_summary = helicity_rows()
    coverage = coverage_rows()

    determinant_counts = topology_summary["determinant"]["counts"]
    wetterich_counts = topology_summary["wetterich"]["counts"]
    x_symbol, mass_squared, k_squared, c_symbol = sp.symbols(
        "x m2 k2 C0", positive=True
    )
    effective_mass_squared = mass_squared + 3 * k_squared
    direct_mass_derivative = sp.simplify(
        (3 * k_squared) ** 3
        * sp.diff(c_symbol / sp.Symbol("M2", positive=True), sp.Symbol("M2", positive=True), 3)
    )
    expected_mass_derivative = -162 * c_symbol * k_squared**3 / sp.Symbol(
        "M2", positive=True
    ) ** 4
    normalized_from_direct = sp.simplify(
        expected_mass_derivative.subs(
            sp.Symbol("M2", positive=True), effective_mass_squared
        )
        * mass_squared
        / c_symbol
    ).subs(k_squared, x_symbol * mass_squared / 3)

    checks = {
        **{f"source_hash::{key}": value for key, value in hash_checks.items()},
        "2605_displayed_kernel_is_explicit_second_metric_response": (
            "\\frac{\\delta^2 \\mathrm{Tr}" in source_2605_text
            and "\\Gamma_k^{(3)}" in source_2605_text
            and "\\Gamma_k^{(4)}" in source_2605_text
        ),
        "4912_complete_third_determinant_response_is_present": (
            "GK_{123}" in source_4912_text
            and "GK_1GK_2GK_3" in source_4912_text
        ),
        "log_determinant_three_response_has_six_terms": topology_summary[
            "determinant"
        ]["term_count"]
        == 6,
        "log_determinant_has_one_Gamma5_contact": determinant_counts.get(
            "Gamma5_contact"
        )
        == 1,
        "log_determinant_has_three_mixed_terms": determinant_counts.get(
            "Gamma3_Gamma4_mixed"
        )
        == 3,
        "log_determinant_has_two_triangle_orientations": determinant_counts.get(
            "Gamma3_cubed_triangle"
        )
        == 2,
        "Wetterich_three_response_has_thirteen_ordered_terms": topology_summary[
            "wetterich"
        ]["term_count"]
        == 13,
        "Wetterich_has_one_Gamma5_six_mixed_six_triangle": (
            wetterich_counts.get("Gamma5_contact") == 1
            and wetterich_counts.get("Gamma3_Gamma4_mixed") == 6
            and wetterich_counts.get("Gamma3_cubed_triangle") == 6
        ),
        "PT_m3_mass_derivative_identity": sp.simplify(
            direct_mass_derivative - expected_mass_derivative
        )
        == 0,
        "normalized_scalar_kernel_exact": sp.simplify(
            normalized_from_direct + 6 * x_symbol**3 / (1 + x_symbol) ** 4
        )
        == 0,
        "scalar_kernel_IR_endpoint_zero": sp.limit(
            -6 * x_symbol**3 / (1 + x_symbol) ** 4, x_symbol, 0, dir="+"
        )
        == 0,
        "scalar_kernel_UV_endpoint_zero": sp.limit(
            -6 * x_symbol**3 / (1 + x_symbol) ** 4, x_symbol, sp.oo
        )
        == 0,
        "scalar_kernel_IR_cubic_coefficient": sp.limit(
            (-6 * x_symbol**3 / (1 + x_symbol) ** 4) / x_symbol**3,
            x_symbol,
            0,
            dir="+",
        )
        == -6,
        "scalar_kernel_UV_inverse_coefficient": sp.limit(
            x_symbol * (-6 * x_symbol**3 / (1 + x_symbol) ** 4),
            x_symbol,
            sp.oo,
        )
        == -6,
        "scalar_threshold_integrates_to_one": scalar_summary["integral_exact"]
        == "1",
        "scalar_threshold_numeric_integration_pass": math.isclose(
            scalar_summary["integral_numeric"], 1.0, rel_tol=0.0, abs_tol=2e-13
        ),
        "scalar_kernel_peak_is_x3": scalar_summary["peak_value_exact"]
        == "-81/128",
        "scalar_finite_coefficient_recovered": math.isclose(
            SCALAR_C3_CONSTANT,
            2.0941051513379998e-7,
            rel_tol=2e-15,
            abs_tol=0.0,
        ),
        "helicity_factor_ten_pass": helicity_summary[
            "maximum_factor_ten_residual"
        ]
        == 0.0,
        "coverage_keeps_full_MTS_open": all(
            row["valid_for_full_MTS_claim"] is False for row in coverage
        ),
        "all_outputs_are_private_nonclaim": all(
            row["valid_for_full_MTS_claim"] is False
            for row in scheme_lock + topology + scalar_kernel + helicity + coverage
        ),
    }

    write_csv(SCHEME_LOCK_CSV, scheme_lock)
    write_csv(TOPOLOGY_CSV, topology)
    write_csv(SCALAR_KERNEL_CSV, scalar_kernel)
    write_csv(HELICITY_CSV, helicity)
    write_csv(COVERAGE_CSV, coverage)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "decision": {
            "4973_two_point_topology_for_C3": "SUPERSEDED",
            "correct_C3_response_order": "third metric response",
            "one_loop_determinant_topology": "Gamma5 - three Gamma3/Gamma4 mixed + two Gamma3^3 orientations",
            "exact_Wetterich_topology": "one Gamma5 + six ordered Gamma3/Gamma4 + six ordered Gamma3^3 terms with regulator insertion",
            "free_scalar_PT_m3_local_kernel": "CALCULATED_AND_EXACTLY_INTEGRATED",
            "free_scalar_finite_C3_coefficient": "C0/m^2 with C0=1/[30240(4pi)^2]",
            "interacting_motion_kernel": "PARTIAL_OPEN",
            "graviton_ghost_kernel": "OPEN_AT_GAMMA3_GAMMA4_GAMMA5_CONTRACTIONS",
            "physical_logarithmic_endpoint": "NOT_TESTED_BY_LOCAL_SCALAR_THRESHOLD",
            "delta_c_fin_full_parent": "OPEN",
            "full_MTS": False,
        },
        "source_hashes": {
            relative(path): observed_hashes[path] for path in EXPECTED_HASHES
        },
        "topology": topology_summary,
        "scalar_kernel": scalar_summary,
        "helicity": helicity_summary,
        "checks": checks,
        "check_count": len(checks),
        "failed_checks": failed,
        "valid_for_full_MTS_claim": False,
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"{MARKER}_CHECKS={len(checks)}", flush=True)
    print(f"{MARKER}_PASSED={len(checks) - len(failed)}", flush=True)
    print(f"{MARKER}_FAILED={len(failed)}", flush=True)
    print(f"{MARKER}_C0={SCALAR_C3_CONSTANT:.17g}", flush=True)
    print(
        f"{MARKER}_PT_M3_INTEGRAL={scalar_summary['integral_numeric']:.17g}",
        flush=True,
    )
    if failed:
        print(f"{MARKER}_FAILED_IDS={','.join(failed)}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
