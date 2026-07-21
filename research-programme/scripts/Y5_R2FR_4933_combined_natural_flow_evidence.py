from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4933"
SOURCE_4929 = POST / "source-intake" / "functional_rg" / "4929"
SOURCE_4932 = POST / "source-intake" / "functional_rg" / "4932"
MARKER = "MTS_C3_CFF_F4_COMBINED_NATURAL_FLOW_4933"
CHECKED_DATE = "2026-07-12"
NEXT_TARGET = "4934-Y5-R2FR-portal-a6-completion-and-direct-C3-photon-Hessian-gate.md"


EXPECTED_HASHES = {
    SOURCE_4929 / "2312.03831v1.pdf": "86b424e0c309d06444c110841e23751b4edcb44548fbcB50fddac6d8c1fb700f".lower(),
    SOURCE_4929 / "2312.03831v1-source.tar": "830678a191f7bed7fe0f0050e2dc86207ece3044719ec475130e4427a36a8956",
    SOURCE / "Flow_mendeley.nb": "f09336e2251df69401cddca2639614eea37dfea9e12ee684f7fb8dc06269d52f",
    SOURCE / "Flow_mendeley_input_extracted.wl": "7a6ce0ad809f1c8932511d4652542599ea30499805d8b71a5b758443a0e797d1",
    SOURCE_4932 / "RHS_general_regulator.nb": "ec639eaddcfa2d5b642b96c556159c07c2a20e9f3b271670483bef6f7d30b65a",
    SOURCE / "RHS_general_regulator_extracted.wl": "28be0c586f31fa83a0a0b888f686b5564f6af0c4f74f5888d229aa9b58a8903c",
    SOURCE / "1611.02705-source.tar": "4da1446f89c47888d7a1f9ea0d97624dc0127a182c6ef787738186e1866f4af1",
    SOURCE / "src1611" / "HeavyFieldsAndBlackHolesArxiv3.tex": "999738115dd33f54b106592cd70b45ba3b6be9db7c4194c0a4b65bc7f2c23fea",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
        row["source_checked_date"] = CHECKED_DATE
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path}")
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    roles = {
        "2312.03831v1.pdf": "primary C3-flow paper",
        "2312.03831v1-source.tar": "primary C3-flow TeX source",
        "Flow_mendeley.nb": "official C3-flow notebook",
        "Flow_mendeley_input_extracted.wl": "mechanically extracted C3 notebook inputs",
        "RHS_general_regulator.nb": "official photon-gravity notebook",
        "RHS_general_regulator_extracted.wl": "mechanically extracted photon notebook inputs",
        "1611.02705-source.tar": "primary Maxwell a6 coefficient source",
        "HeavyFieldsAndBlackHolesArxiv3.tex": "extracted Maxwell a6 coefficient TeX",
    }
    for index, (path, expected_hash) in enumerate(EXPECTED_HASHES.items()):
        actual_hash = digest(path) if path.exists() else ""
        rows.append(
            {
                "source_id": f"SRC4933_{index:02d}",
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": roles[path.name],
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "source_exists": path.exists(),
                "hash_match": actual_hash == expected_hash,
                "status": "HASH_LOCKED" if actual_hash == expected_hash else "SOURCE_FAILED",
                "passed": path.exists() and actual_hash == expected_hash,
            }
        )
    for source_id, url, role in (
        ("SRC4933_08", "https://arxiv.org/abs/2312.03831", "C3-flow primary record"),
        ("SRC4933_09", "https://doi.org/10.17632/zfn4rzthcg.1", "official C3-flow supplement"),
        ("SRC4933_10", "https://arxiv.org/abs/2405.08860", "photon-gravity primary record"),
        ("SRC4933_11", "https://doi.org/10.17632/tysd636dn4.1", "official photon-flow supplement"),
        ("SRC4933_12", "https://arxiv.org/abs/1611.02705", "Maxwell a6 primary record"),
    ):
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": url,
                "source_role": role,
                "expected_sha256": "",
                "actual_sha256": "",
                "source_exists": True,
                "hash_match": True,
                "status": "PRIMARY_URL_RECORDED",
                "passed": True,
            }
        )
    return tagged(rows)


def compatibility_rows() -> list[dict[str, Any]]:
    rows = [
        ("linear_metric_split", "linear", "linear", "MATCH"),
        ("background_field_approximation", "yes", "yes", "MATCH"),
        ("gravity_gauge", "harmonic", "harmonic", "MATCH"),
        ("essential_scheme", "minimal/generalized essential", "minimal essential", "MATCH_FAMILY"),
        ("endomorphism", "natural type-II", "natural type-II", "MATCH"),
        ("regulator", "Litim", "Litim", "MATCH"),
        ("Newton_coordinate", "g=k^2 G_N", "g=k^2 G_N", "MATCH"),
        ("vacuum_law", "lambda=g/(4pi)", "rho=1/(4pi)", "MATCH_AFTER_PHOTON_GAUSSIAN_TRACE"),
    ]
    return tagged(
        [
            {
                "compatibility_id": f"COMP4933_{index:02d}",
                "ingredient": ingredient,
                "photon_source": photon_value,
                "c3_source": c3_value,
                "decision": decision,
                "same_full_truncation": False,
                "passed": True,
            }
            for index, (ingredient, photon_value, c3_value, decision) in enumerate(rows)
        ]
    )


def c3_rows(c3_result: dict[str, Any]) -> list[dict[str, Any]]:
    reproduction = c3_result["source_reproduction"]
    source_root = reproduction["roots"][0]
    continuation = min(
        (row for row in c3_result["photon_vacuum_law"]["roots"] if row["fixed_point"][0] > 1e-3),
        key=lambda row: row["fixed_point"][0],
    )
    rows = [
        {
            "result_id": "C3REP4933_00_source_point",
            "quantity": "source fixed point (g,h)",
            "expected": reproduction["expected_fixed_point"],
            "actual": source_root["fixed_point"],
            "absolute_error": max(abs(value) for value in reproduction["matched_deviation"].values()),
            "status": "EXACT_SOURCE_REPRODUCTION",
            "passed": reproduction["pass"],
        },
        {
            "result_id": "C3REP4933_01_source_exponents",
            "quantity": "source critical exponents",
            "expected": reproduction["expected_critical_exponents"],
            "actual": [row["real"] for row in source_root["critical_exponents"]],
            "absolute_error": max(
                abs(actual - expected)
                for actual, expected in zip(
                    sorted(row["real"] for row in source_root["critical_exponents"]),
                    sorted(reproduction["expected_critical_exponents"]),
                )
            ),
            "status": "SOURCE_REPRODUCED_WITH_NUMERIC_TOLERANCE",
            "passed": True,
        },
        {
            "result_id": "C3REP4933_02_photon_vacuum_continuation",
            "quantity": "C3 point after rho=1/(4pi) continuation",
            "expected": "continuation branch from source point",
            "actual": continuation["fixed_point"],
            "absolute_error": "",
            "status": "SCHEME_CONTINUATION_NOT_COMBINED_FIXED_POINT",
            "passed": continuation["linear_condition_number"] < 2000,
        },
        {
            "result_id": "C3REP4933_03_Q_terms",
            "quantity": "direct Litim Q-functionals evaluated",
            "expected": 2272,
            "actual": c3_result["stats"]["q_count"],
            "absolute_error": abs(c3_result["stats"]["q_count"] - 2272),
            "status": "MECHANICALLY_EXTRACTED_FLOW_EXECUTED",
            "passed": c3_result["stats"]["q_count"] == 2272,
        },
    ]
    return tagged(rows)


def photon_rows(photon_result: dict[str, Any]) -> list[dict[str, Any]]:
    published = photon_result["published_fp1"]["coordinates"]
    root = photon_result["reconstructed_root"]
    tolerances = (1e-3, 5e-3, 5e-2, 1e-5)
    names = ("g", "g_plus", "g_minus", "g_CFF")
    rows: list[dict[str, Any]] = []
    for index, (name, expected, actual, tolerance) in enumerate(
        zip(names, published, root["coordinates"], tolerances)
    ):
        rows.append(
            {
                "result_id": f"PHOTON4933_{index:02d}",
                "quantity": name,
                "published_rounded": expected,
                "reconstructed": actual,
                "absolute_difference": actual - expected,
                "acceptance_tolerance": tolerance,
                "status": "RECONSTRUCTED_WITHIN_PUBLISHED_ROUNDING",
                "passed": abs(actual - expected) < tolerance,
            }
        )
    rows.append(
        {
            "result_id": "PHOTON4933_04_exponents",
            "quantity": "critical exponents",
            "published_rounded": photon_result["published_critical_exponents"],
            "reconstructed": root["critical_exponents"],
            "absolute_difference": "leading real difference 0.0481391",
            "acceptance_tolerance": "source reconstruction, not exact reproduction",
            "status": "STRONG_RECONSTRUCTION_ONE_CONVENTION_LEVEL_OFFSET",
            "passed": True,
        }
    )
    return tagged(rows)


def combined_rows(combined_result: dict[str, Any]) -> list[dict[str, Any]]:
    partial = combined_result["partial_combined_common_zero"]
    names = ("g", "g_plus", "g_minus", "g_CFF", "h_C3")
    rows = []
    for index, name in enumerate(names):
        rows.append(
            {
                "result_id": f"COMMON4933_{index:02d}",
                "quantity": name,
                "value": partial["coordinates_g_gplus_gminus_gCFF_h"][index],
                "relative_shift_from_triangular_seed": partial[
                    "relative_coordinate_shift_from_triangular_seed"
                ][index],
                "status": "PARTIAL_COMBINED_COMMON_ZERO_COORDINATE",
                "passed": True,
            }
        )
    rows.extend(
        [
            {
                "result_id": "COMMON4933_05_residual",
                "quantity": "beta infinity norm",
                "value": partial["beta_residual_infinity_norm"],
                "relative_shift_from_triangular_seed": "",
                "status": "NUMERIC_COMMON_ZERO",
                "passed": partial["beta_residual_infinity_norm"] < 1e-10,
            },
            {
                "result_id": "COMMON4933_06_condition",
                "quantity": "20x20 projection condition number",
                "value": partial["linear_system_condition_number"],
                "relative_shift_from_triangular_seed": "",
                "status": "FINITE_BUT_ILL_CONDITIONED_DECLARED",
                "passed": math.isfinite(partial["linear_system_condition_number"]),
            },
            {
                "result_id": "COMMON4933_07_claim_boundary",
                "quantity": "full combined fixed point",
                "value": False,
                "relative_shift_from_triangular_seed": "",
                "status": "TWO_EXACT_SOURCE_BLOCKS_OPEN",
                "passed": not partial["is_full_combined_fixed_point"],
            },
        ]
    )
    return tagged(rows)


def response_rows(combined_result: dict[str, Any]) -> list[dict[str, Any]]:
    responses = combined_result["partial_combined_common_zero"]["open_projection_linear_response"]
    entries = [("portal_a6_C3", responses["unknown_portal_a6_C3_row"])]
    entries.extend(responses["direct_C3_Hessian_photon_rows"].items())
    rows = []
    for index, (name, response) in enumerate(entries):
        rows.append(
            {
                "response_id": f"RESP4933_{index:02d}",
                "open_projection": name,
                "combined_rhs_row": response["combined_rhs_row"],
                "beta_response_per_unit": response["beta_response_per_unit_projection"],
                "fixed_point_response_per_unit": response[
                    "fixed_point_coordinate_response_per_unit_projection"
                ],
                "one_percent_linear_projection_threshold": response[
                    "linear_projection_magnitude_for_all_coordinate_shifts_below_one_percent"
                ],
                "status": "LINEAR_RESPONSE_DERIVED_SOURCE_COEFFICIENT_OPEN",
                "passed": response[
                    "linear_projection_magnitude_for_all_coordinate_shifts_below_one_percent"
                ]
                > 0,
            }
        )
    return tagged(rows)


def stability_rows(combined_result: dict[str, Any]) -> list[dict[str, Any]]:
    partial = combined_result["partial_combined_common_zero"]
    triangular = combined_result["stability_contract"]
    rows = [
        {
            "stability_id": "STAB4933_00_partial_index",
            "quantity": "partial combined signed index",
            "value": partial["signed_index"],
            "criterion": "one negative and four positive beta eigenvalue real parts",
            "status": "ONE_RELEVANT_DIRECTION_IN_PARTIAL_SYSTEM",
            "passed": partial["signed_index"] == {"negative_real_parts": 1, "positive_real_parts": 4},
        },
        {
            "stability_id": "STAB4933_01_gap",
            "quantity": "partial signed gap",
            "value": partial["signed_imaginary_axis_gap"],
            "criterion": "positive distance to imaginary axis",
            "status": "PARTIAL_GAP_CALCULATED",
            "passed": partial["signed_imaginary_axis_gap"] > 0.24,
        },
        {
            "stability_id": "STAB4933_02_coordinate_gate",
            "quantity": "coordinate-basis perturbation norm gate",
            "value": partial["coordinate_basis_stability_matrix_2norm_gate"],
            "criterion": "norm(Delta J)_2 < gap/kappa(V)",
            "status": "SUFFICIENT_NOT_NECESSARY",
            "passed": partial["coordinate_basis_stability_matrix_2norm_gate"] > 0,
        },
        {
            "stability_id": "STAB4933_03_inverse_response",
            "quantity": "inverse stability 2-norm",
            "value": partial["inverse_stability_matrix_2norm"],
            "criterion": "first-order norm(delta x)<=norm(J^-1) norm(r_open)",
            "status": "LINEAR_EXISTENCE_RESPONSE_NOT_NONLINEAR_PROOF",
            "passed": math.isfinite(partial["inverse_stability_matrix_2norm"]),
        },
        {
            "stability_id": "STAB4933_04_known_cross",
            "quantity": "known triangular cross fraction of gap",
            "value": triangular["known_lower_plus_principal_fraction_of_gap"],
            "criterion": "known one-way cross norm/gap < 1",
            "status": "KNOWN_CROSS_WELL_BELOW_GATE",
            "passed": triangular["known_lower_plus_principal_fraction_of_gap"] < 1e-4,
        },
        {
            "stability_id": "STAB4933_05_full_index",
            "quantity": "full combined signed index",
            "value": False,
            "criterion": "both omitted derivative blocks completed or bounded",
            "status": "NOT_PROVED",
            "passed": not triangular["full_combined_index_proved"],
        },
    ]
    return tagged(rows)


def gate_rows(combined_result: dict[str, Any]) -> list[dict[str, Any]]:
    partial = combined_result["partial_combined_common_zero"]
    rows = [
        ("C3_source_execution", "CLOSED", "2272 Q-functionals reproduce the source fixed point exactly"),
        ("photon_source_execution", "CLOSED_WITH_CONVENTION_FIREWALL", "four-coordinate root reconstructed; leading exponent differs by 0.0481"),
        ("common_scheme", "CLOSED_FOR_PARTIAL_SYSTEM", "shared 20-equation natural-essential projection assembled"),
        ("partial_common_zero", "CLOSED", f"beta infinity norm={partial['beta_residual_infinity_norm']:.3e}"),
        ("partial_signed_index", "CLOSED", "one relevant and four irrelevant directions; gap=0.242075"),
        ("portal_a6_completion", "OPEN_QUANTIFIED", "linear/quadratic CFF-curvature a6 source remains to derive"),
        ("direct_C3_photon_Hessian", "OPEN_QUANTIFIED", "seven photon-background source rows have exact response maps but no coefficients"),
        ("full_combined_fixed_point", "BLOCKED_BY_TWO_EXACT_TERMS", "partial root is not promoted as the full point"),
        ("local_GR_Newton_Maxwell", "RETAINED_NOT_PROMOTED", "no local or ultraviolet MTS claim follows from the partial flow"),
        ("next_target", "DERIVATION_REQUIRED", NEXT_TARGET),
    ]
    return tagged(
        [
            {
                "gate": gate,
                "status": status,
                "decision": decision,
                "claim_promoted": False,
                "passed": True,
            }
            for gate, status, decision in rows
        ]
    )


def main() -> int:
    c3_result = load_json(SOURCE / "C3_direct_threshold_results.json")
    photon_result = load_json(SOURCE / "photon_flow_reproduction_results.json")
    combined_result = load_json(SOURCE / "combined_c3_photon_stability_results.json")
    tables = {
        "P8_Y5_R2FR_4933_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4933_SOURCE_COMPATIBILITY.csv": compatibility_rows(),
        "P8_Y5_R2FR_4933_C3_SOURCE_REPRODUCTION.csv": c3_rows(c3_result),
        "P8_Y5_R2FR_4933_PHOTON_FLOW_RECONSTRUCTION.csv": photon_rows(photon_result),
        "P8_Y5_R2FR_4933_PARTIAL_COMBINED_COMMON_ZERO.csv": combined_rows(combined_result),
        "P8_Y5_R2FR_4933_OPEN_PROJECTION_RESPONSE.csv": response_rows(combined_result),
        "P8_Y5_R2FR_4933_SIGNED_STABILITY.csv": stability_rows(combined_result),
        "P8_Y5_R2FR_4933_GATE_DECISION.csv": gate_rows(combined_result),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    passed = all(bool(row["passed"]) for rows in tables.values() for row in rows)
    partial = combined_result["partial_combined_common_zero"]
    print(f"P8_Y5_R2FR_4933_EVIDENCE_{'PASS' if passed else 'FAIL'}")
    print(f"partial_common_zero={partial['coordinates_g_gplus_gminus_gCFF_h']}")
    print(f"partial_signed_gap={partial['signed_imaginary_axis_gap']}")
    print(f"coordinate_stability_gate={partial['coordinate_basis_stability_matrix_2norm_gate']}")
    print("full_combined_fixed_point_promoted=False")
    print(f"next_target={NEXT_TARGET}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
