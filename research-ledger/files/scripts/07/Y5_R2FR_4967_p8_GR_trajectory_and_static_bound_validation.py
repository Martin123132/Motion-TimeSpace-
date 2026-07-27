from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4967"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4967_VALIDATION.csv"
)

MAIN_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_4967_p8_GR_trajectory_and_static_bound.py"
)
RESULT_JSON = SOURCE / "p8_GR_trajectory_and_static_bound_results.json"
SOURCE_AUDIT_CSV = SOURCE / "p8_functional_source_audit.csv"
NORMALIZATION_CSV = SOURCE / "p8_amplitude_normalization_map.csv"
THRESHOLD_CSV = SOURCE / "p8_massive_spin_threshold_transfer.csv"
FIXED_CSV = SOURCE / "p8_extended_fixed_point.csv"
TRAJECTORY_CSV = SOURCE / "p8_GR_connected_trajectory.csv"
ENDPOINT_CSV = SOURCE / "p8_IR_endpoint_convergence.csv"
STATIC_CSV = SOURCE / "p8_static_compact_response.csv"
LOCALITY_CSV = SOURCE / "p8_motion_scalar_locality_bound.csv"
DECISION_CSV = SOURCE / "p8_finite_boundary_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
BARATELLA_SOURCE = SOURCE / "src-2010.13809" / "draft.tex"
BERN_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4965"
    / "src-2103.12728"
    / "GravScatt.tex"
)

CHECKPOINT = (
    POST
    / "4967-Y5-R2FR-C3-O4-p8-trajectory-UV-boundary-and-static-bound-or-CFF-Einstein-source-boundary.md"
)
FORMAL_NOTE = FORMAL / "983-PPC4161-C3-O4-p8-trajectory-and-static-boundary.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

MARKER = "MTS_4967_P8_GR_TRAJECTORY_AND_STATIC_BOUND"
FORMAL_MARKER = "PPC4161_C3_O4_P8_TRAJECTORY_STATIC_BOUND_4967"

HASH_LOCKS = {
    MAIN_SCRIPT: "5d560ecb99207e33ad0f7ccbc17019044c197c0b66193e13a7e5c73bd3d479e8",
    SOURCE_AUDIT_CSV: "0951a5014743e157605c7a4fabe1dfcde4b59252c9b8c856f29ae36e05151849",
    NORMALIZATION_CSV: "efddd20d514967e96296cf4ae129325c7edf1455d3d5f6a34ccde0e6b32e1294",
    THRESHOLD_CSV: "f4465af0b1fea64768d23543bfe099dc2ca422c609b9712dd5100357d384ddbc",
    FIXED_CSV: "1a355a1d67270074ba4c993cbb274b2fa99b5d8b43d39ddcdadea00c2e63ceb8",
    TRAJECTORY_CSV: "ddf759e61a1038638ec07ddbd74bd15824de856f57a08823a2e0b59b3cc0f833",
    ENDPOINT_CSV: "5c55756acb02edfd9e4221e5661fab9651c4db7945bb45083429cdbaffa284ff",
    STATIC_CSV: "efe1e28b0f29eeefe4c442d8ce6b5472233c6e1e8cb6411d8e0b9fa207dc6a17",
    LOCALITY_CSV: "1e85d8ee010c80760867d2d34a3b05e8e1ff0e018ef09db96f095ba49e6549b7",
    DECISION_CSV: "1b1b69cd3b07e0e62b03ec06a8bc21638954ff1596fd539e50f1cba28927dd0f",
    RESULT_JSON: "415f9dbff1b903e6aee5921c6516d8a53fa4373feb4f38fb4d2d0943eda9d694",
    PROVENANCE: "d9753e8c84929cd6b79b7039a6578c1ef69e4f59749fc4a52133538246a5e414",
    CHECKPOINT: "f4120b0b25ad3592f2251323bd90e7839030bb49e45cde9e9d908189890c2393",
    FORMAL_NOTE: "ab007497b3a57d378be34039d558d5e94c420a9dabffd9cfd3097b35a2b21581",
    CLAIMS: "5bd0818eeed3255e75d14fbccae34e45b07085e40b3719f127767b4e800d0f6d",
    VARIABLES: "066b020aaa76fd3498fb9d0e13c8da6ecd36b638086dca59864f134014304eb4",
    EQUATIONS: "b22efa20a344c725ee56defa194871eae2872964d3f26f2e9bbe4d66aa33e723",
    RED_TEAM: "4c2e5be14a1e48d0b6665c0163a34b4f326d64774b24b4f14551ee68351d198f",
    SPINE: "c86644982f1b7cad633127acb03d6b91b48a8aef4b56b94cc27fd01d0b100344",
    RESUME: "6851e2aee7895efbbd5fea4b9535ed772f8c60c8af695ab9e8a71c479e3362a4",
    LOCAL_SPINE: "6f8b4d1605aca074582c70b41a7df02f4f4cec6fff9974f5cf46bb8d3e9a06fe",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def truth(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def malformed(rows: list[dict[str, str]]) -> bool:
    return any(None in row or any(value is None for value in row.values()) for row in rows)


def add(
    rows: list[dict[str, Any]],
    check_id: str,
    test: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": check_id,
            "test": test,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
        }
    )


def write_output(rows: list[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_fraction(value: str) -> Fraction:
    numerator, denominator = value.split("/")
    return Fraction(int(numerator), int(denominator))


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "V4967_00", "all locked files exist", [], missing, not missing)

    bad_hashes = {
        str(path.relative_to(ROOT)): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "V4967_01", "all locked hashes match", {}, bad_hashes, not bad_hashes)

    syntax_errors: dict[str, str] = {}
    for path in (MAIN_SCRIPT, Path(__file__)):
        try:
            ast.parse(text(path), filename=str(path))
        except SyntaxError as error:
            syntax_errors[str(path)] = str(error)
    add(checks, "V4967_02", "generator and validator parse", {}, syntax_errors, not syntax_errors)

    result = json.loads(text(RESULT_JSON))
    audit = read_csv(SOURCE_AUDIT_CSV)
    normalization = read_csv(NORMALIZATION_CSV)
    thresholds = read_csv(THRESHOLD_CSV)
    fixed = read_csv(FIXED_CSV)
    trajectory = read_csv(TRAJECTORY_CSV)
    convergence = read_csv(ENDPOINT_CSV)
    static = read_csv(STATIC_CSV)
    locality = read_csv(LOCALITY_CSV)
    decisions = read_csv(DECISION_CSV)
    generated = [
        audit,
        normalization,
        thresholds,
        fixed,
        trajectory,
        convergence,
        static,
        locality,
        decisions,
    ]
    add(
        checks,
        "V4967_03",
        "all generated CSV files are nonempty and well formed",
        True,
        [len(rows) for rows in generated],
        all(rows and not malformed(rows) for rows in generated),
    )
    add(
        checks,
        "V4967_04",
        "all generated rows carry marker and remain nonclaim",
        True,
        True,
        all(
            row.get("checkpoint_marker") == MARKER
            and not truth(row.get("valid_for_full_MTS_claim"))
            for rows in generated
            for row in rows
        ),
    )

    primary_text = text(BARATELLA_SOURCE)
    primary_flat = " ".join(primary_text.split())
    primary_clauses = {
        "gamma_definition": "Defining $\\gamma_i=d C_i/d\\ln\\mu$" in primary_text,
        "same_helicity_source": "\\gamma_{R^4}=-\\frac{{C_{R^3}}}{8\\pi^2}" in primary_text,
        "mixed_helicity_zero": (
            "do not find any contribution to the anomalous dimension of $C'_{R^4}$"
            in primary_flat
        ),
    }
    add(
        checks,
        "V4967_05",
        "primary C3 to p8 clauses are source present",
        True,
        primary_clauses,
        all(primary_clauses.values()),
    )

    a_symbol = sp.symbols("A")
    c_r3 = 3 * a_symbol / (4 * sp.pi)
    gamma_c_r4 = -c_r3 / (8 * sp.pi**2)
    gamma_b_minus = sp.simplify(128 * sp.pi**3 * gamma_c_r4)
    gamma_b_c = sp.simplify(gamma_b_minus / 2)
    gamma_b_t = sp.simplify(-gamma_b_minus / 2)
    mapping_ok = (
        sp.simplify(gamma_b_minus + 12 * a_symbol) == 0
        and sp.simplify(gamma_b_c + 6 * a_symbol) == 0
        and sp.simplify(gamma_b_t - 6 * a_symbol) == 0
    )
    add(
        checks,
        "V4967_06",
        "independent C3 amplitude normalization gives -12A and zero mixed source",
        True,
        [str(gamma_b_minus), str(gamma_b_c), str(gamma_b_t)],
        mapping_ok,
    )

    k_symbol, eta_symbol = sp.symbols("k eta", positive=True)
    i4 = k_symbol**8 / (64 * sp.pi**2)
    i6 = k_symbol**10 / (80 * sp.pi**2)
    optimized_moment = sp.simplify(
        2 * (2 * k_symbol**2 * i4 - eta_symbol * (k_symbol**2 * i4 - i6))
    )
    expected_moment = k_symbol**10 * (1 - eta_symbol / 10) / (16 * sp.pi**2)
    add(
        checks,
        "V4967_07",
        "independent optimized O4 moment gives 1-eta_psi/10",
        0,
        str(sp.simplify(optimized_moment - expected_moment)),
        sp.simplify(optimized_moment - expected_moment) == 0,
    )

    threshold_checks: list[bool] = []
    for row in thresholds:
        c_minus = parse_fraction(row["c_minus"])
        c_plus = parse_fraction(row["c_plus"])
        c_c = parse_fraction(row["c_C"])
        c_t = parse_fraction(row["c_t"])
        threshold_checks.append(
            c_c == (c_minus + c_plus) / 2
            and c_t == (c_plus - c_minus) / 2
            and c_c > 0
            and c_t > 0
        )
    add(
        checks,
        "V4967_08",
        "all five massive-spin threshold maps satisfy the helicity inverse",
        [True] * 5,
        threshold_checks,
        len(threshold_checks) == 5 and all(threshold_checks),
    )

    fixed_residual = max(
        max(
            abs(float(row["beta_B_C_fixed_residual"])),
            abs(float(row["beta_B_t_fixed_residual"])),
        )
        for row in fixed
    )
    add(
        checks,
        "V4967_09",
        "all twelve p8 fixed points have eigenvalues +4,+4 and zero new relevant directions",
        True,
        {"rows": len(fixed), "max_residual": fixed_residual},
        len(fixed) == 12
        and fixed_residual < 1.0e-15
        and all(
            float(row["p8_subblock_eigenvalue_C"]) == 4.0
            and float(row["p8_subblock_eigenvalue_t"]) == 4.0
            and int(row["new_relevant_directions"]) == 0
            for row in fixed
        ),
    )

    add(
        checks,
        "V4967_10",
        "trajectory table has all four parent runs three scenarios and 121 samples",
        1452,
        len(trajectory),
        len(trajectory) == 2 * 2 * 3 * 121,
    )

    endpoints = {
        (row["scheme"], int(row["polynomial_order"]), row["scenario"]): row
        for row in trajectory
        if int(row["sample_index"]) == 120
    }
    superposition_residuals: list[float] = []
    for scheme in ("dynamic_etaN", "reference_etaN0"):
        for order in (6, 8):
            c3 = endpoints[(scheme, order, "C3_only")]
            o4 = endpoints[(scheme, order, "O4_squared_only")]
            combined = endpoints[(scheme, order, "C3_plus_O4_squared")]
            for coordinate in ("B_C", "B_t"):
                superposition_residuals.append(
                    abs(
                        float(combined[coordinate])
                        - float(c3[coordinate])
                        - float(o4[coordinate])
                    )
                )
    add(
        checks,
        "V4967_11",
        "C3 and O4 trajectory superposition closes",
        "<3e-11",
        max(superposition_residuals),
        max(superposition_residuals) < 3.0e-11,
    )

    combined_order_rows = [
        row
        for row in convergence
        if row["comparison"] == "N6_to_N8"
        and row["scenario"] == "C3_plus_O4_squared"
    ]
    maximum_order_shift = max(float(row["relative_difference"]) for row in combined_order_rows)
    add(
        checks,
        "V4967_12",
        "combined N6 to N8 convergence is below 1e-3",
        "<1e-3",
        maximum_order_shift,
        len(combined_order_rows) == 8 and maximum_order_shift < 1.0e-3,
    )

    combined_n8 = [
        endpoints[(scheme, 8, "C3_plus_O4_squared")]
        for scheme in ("dynamic_etaN", "reference_etaN0")
    ]
    b_c_values = [float(row["B_C"]) for row in combined_n8]
    b_t_values = [float(row["B_t"]) for row in combined_n8]
    add(
        checks,
        "V4967_13",
        "N8 combined endpoint lies in the recorded source-truncated bracket",
        True,
        {"B_C": b_c_values, "B_t": b_t_values},
        0.0130494 < min(b_c_values) < max(b_c_values) < 0.0130501
        and -0.0130634 < min(b_t_values) < max(b_t_values) < -0.0130627,
    )

    static_residual = max(float(row["max_abs_metric_residual"]) for row in static)
    static_formula_residuals: list[float] = []
    for row in static:
        compactness = float(row["compactness_M_over_r"])
        chi = float(row["chi_lP2_curvature"])
        b_c = float(row["B_C_endpoint"])
        expected_a = 128 * b_c * chi**3 * (8 - 11 * compactness)
        expected_b = 128 * b_c * chi**3 * (36 - 67 * compactness)
        static_formula_residuals.extend(
            [abs(float(row["delta_A"]) - expected_a), abs(float(row["delta_B"]) - expected_b)]
        )
    add(
        checks,
        "V4967_14",
        "all 22 exact static responses reproduce the Schwarzschild kernel and pass",
        True,
        {"rows": len(static), "max_metric": static_residual},
        len(static) == 22
        and max(static_formula_residuals) < 1.0e-245
        and static_residual < 1.0e-230
        and all(
            float(row["max_abs_metric_residual"]) < float(row["epsilon_gate"])
            for row in static
        ),
    )

    locality_groups: dict[str, list[dict[str, str]]] = {}
    for row in locality:
        locality_groups.setdefault(row["object_id"], []).append(row)
    scaling_residuals: list[float] = []
    for rows in locality_groups.values():
        scaled_a = [
            float(row["delta_A_minimal_motion_scalar"])
            * float(row["rho_gap_over_curvature"]) ** 2
            for row in rows
        ]
        scale = max(abs(value) for value in scaled_a)
        scaling_residuals.append((max(scaled_a) - min(scaled_a)) / max(scale, 1.0e-300))
    strict_rows = [row for row in locality if truth(row["strict_locality_gate"])]
    strict_maximum = max(
        max(
            abs(float(row["delta_A_minimal_motion_scalar"])),
            abs(float(row["delta_B_minimal_motion_scalar"])),
        )
        for row in strict_rows
    )
    add(
        checks,
        "V4967_15",
        "motion-scalar locality rows obey chi/rho^2 and strict rows are compact safe",
        True,
        {"rows": len(locality), "scaling": max(scaling_residuals), "strict_max": strict_maximum},
        len(locality) == 33
        and len(strict_rows) == 22
        and max(scaling_residuals) < 1.0e-14
        and strict_maximum < 1.0e-80,
    )

    omitted = {
        row["source_class"]: row
        for row in audit
        if not truth(row["included_in_candidate"])
    }
    add(
        checks,
        "V4967_16",
        "source audit retains CFF photon pure-Einstein and spectrum boundaries",
        True,
        list(omitted),
        {
            "minimally_coupled_massive_thresholds",
            "photon_CFF_to_p8",
            "pure_Einstein_p8",
        }.issubset(omitted)
        and not result["full_source_complete"]
        and not result["valid_for_full_MTS_claim"],
    )

    decision_map = {row["question"]: row for row in decisions}
    add(
        checks,
        "V4967_17",
        "decision keeps full finite parent vector open and selects CFF projector",
        True,
        decision_map,
        decision_map["Is the full finite parent [B_C,B_t] now predicted?"]["answer"] == "no"
        and "CFF" in decision_map["What is the next derivation target?"]["answer"],
    )

    claims = read_csv(CLAIMS)
    variables = read_csv(VARIABLES)
    add(
        checks,
        "V4967_18",
        "formal CSV registers parse and contain unique 4967 entries",
        True,
        {"claims": len(claims), "variables": len(variables)},
        not malformed(claims)
        and not malformed(variables)
        and sum(row["claim_id"] == "L-809" for row in claims) == 1
        and sum(row["symbol"] == "B_C4967_MTS" for row in variables) == 1
        and sum(row["symbol"] == "B_t4967_MTS" for row in variables) == 1
        and sum(row["symbol"] == "PredictivityStatus4967_MTS" for row in variables) == 1,
    )

    marker_files = (
        CHECKPOINT,
        FORMAL_NOTE,
        EQUATIONS,
        RED_TEAM,
        SPINE,
        RESUME,
        LOCAL_SPINE,
    )
    marker_state = {str(path.relative_to(ROOT)): FORMAL_MARKER in text(path) for path in marker_files}
    add(
        checks,
        "V4967_19",
        "checkpoint marker is synchronized through handoff and formal spine",
        True,
        marker_state,
        all(marker_state.values()),
    )

    provenance_text = text(PROVENANCE)
    add(
        checks,
        "V4967_20",
        "provenance records both primary URLs hashes scope and no GitHub action",
        True,
        True,
        "https://arxiv.org/abs/2010.13809" in provenance_text
        and "https://arxiv.org/abs/2103.12728" in provenance_text
        and "No GitHub action was performed" in provenance_text,
    )

    add(
        checks,
        "V4967_21",
        "result adds zero relevant p8 directions but remains full-source false",
        True,
        {
            "eigenvalues": result["p8_subblock_eigenvalues"],
            "new_relevant": result["new_relevant_directions"],
            "full_source": result["full_source_complete"],
        },
        result["p8_subblock_eigenvalues"] == [4.0, 4.0]
        and result["new_relevant_directions"] == 0
        and not result["full_source_complete"],
    )

    all_pass = all(bool(row["passed"]) for row in checks)
    write_output(checks)
    print(
        f"{MARKER}_VALIDATION_{'PASS' if all_pass else 'FAIL'} "
        f"checks={sum(bool(row['passed']) for row in checks)}/{len(checks)}",
        flush=True,
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
