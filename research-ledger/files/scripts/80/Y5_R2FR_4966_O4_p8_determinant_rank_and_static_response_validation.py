from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4966"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4966_VALIDATION.csv"
)

MAIN_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_4966_O4_p8_determinant_rank_and_static_response.py"
)
RESULT_JSON = SOURCE / "O4_p8_determinant_rank_and_static_response_results.json"
NORMALIZATION_CSV = SOURCE / "O4_normalization_and_IR_trajectory.csv"
DETERMINANT_CSV = SOURCE / "O4_p8_determinant_source.csv"
RANK_CSV = SOURCE / "p8_two_source_rank_gate.csv"
STATIC_PROJECTOR_CSV = SOURCE / "p8_static_response_projector.csv"
SCHWARZSCHILD_CSV = SOURCE / "p8_Schwarzschild_metric_response.csv"
BOUNDARY_CSV = SOURCE / "p8_finite_boundary_gate.csv"
DECISION_CSV = SOURCE / "p8_4966_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

CHECKPOINT = (
    POST
    / "4966-Y5-R2FR-O4-quadratic-determinant-two-source-p8-rank-and-static-Schwarzschild-response-or-finite-boundary.md"
)
FORMAL_NOTE = (
    FORMAL
    / "982-PPC4161-O4-quadratic-p8-source-rank-and-static-response-boundary.md"
)
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

MARKER = "MTS_4966_O4_P8_RANK_STATIC_RESPONSE"
FORMAL_MARKER = "PPC4161_O4_P8_RANK_STATIC_RESPONSE_4966"

HASH_LOCKS = {
    MAIN_SCRIPT: "4993aef2dd60f05bccf6ab5a42369aeaa7cc5206bf95886907e0cd1b2b5925e7",
    RESULT_JSON: "e8cc0dc517587fe378c8dade2a4afacbe3f2341557d9111428830351401e0765",
    NORMALIZATION_CSV: "de5339f609739e4563d746a014f913f0f81087616540f7ee6fafd3b18eee2337",
    DETERMINANT_CSV: "85cdf4a61f4c19525aeaa3c92df3439a08db79fe498a1fe5d03eff17b2cf469e",
    RANK_CSV: "eb6673358b3c590fe3b7c522fa49385f308872dcc0371c2da7ce8443823547df",
    STATIC_PROJECTOR_CSV: "911ec54a3701d62180e373616555ca04bf0e8d2d126d603365cafb55c827848b",
    SCHWARZSCHILD_CSV: "866115c3ecc2d00e26b8d8e24fbcd3c90a616fc87689dcbde1c6310e2158de20",
    BOUNDARY_CSV: "47c347dd6908168df4de7d992197731c8f9cbf2781c3f18d4b8755719a3bb14f",
    DECISION_CSV: "e440e146319f8283fc6703d7a808e829ec15795bc05277c478f85409e616b622",
    PROVENANCE: "7c6796b663ed16058a0ec72edd74544e21f1dda1120236bbd6a55de287a39f58",
    CHECKPOINT: "b4be5a6dfe32ea06381c69ea826e4cf108badead6cfb5cafdf8e29bad0ab772e",
    FORMAL_NOTE: "6195dfc6d5356fdf6f486fb5143dc82ba87bf71f254069f4cbe8eb636dd7e83a",
    CLAIMS: "71ab756ee999fb60219bd4dca9246cef3dde2d982973365edd25b5719e650f3f",
    VARIABLES: "d81177b72b0e42f8680d296b90edffdbeb07cd47cec18289d1570d0ce2b2bdbf",
    EQUATIONS: "d0c890c9ffbd9871c52cc2ab36be55bcecb9dee86b1ad8c2256d459d4d567687",
    RED_TEAM: "21e59b66752222e16d1e10bd9a16ab07f84a67b23b42d909e7a36507a4bbb887",
    SPINE: "28caba4c029a750a0e6c4e2b64631cc7faf9067eff5f1954b52f7623f9c72187",
    RESUME: "3adb28d3a71a3f3a18c908facabff6575fa850ef54d697937cf638ebb6e5e709",
    LOCAL_SPINE: "6b9d184824665b65d535974f132cf1ba6bff687b4d91e8f93b67067e97c351cd",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


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


def independent_static_checks() -> dict[str, bool]:
    radius, mass = sp.symbols("r M", positive=True)
    f_metric = 1 - 2 * mass / radius
    H_t = 1152 * mass**3 * (32 * radius - 67 * mass) / radius**12
    H_r = 1152 * mass**3 * (4 * radius - 11 * mass) / radius**12
    H_angle = -1152 * mass**3 * (18 * radius - 41 * mass) / radius**12
    response_A = 128 * mass**3 * (8 * radius - 11 * mass) / radius**10
    response_B = 128 * mass**3 * (36 * radius - 67 * mass) / radius**10

    conservation = sp.simplify(
        sp.diff(H_r, radius)
        + sp.diff(f_metric, radius) / (2 * f_metric) * (H_r - H_t)
        + 2 / radius * (H_r - H_angle)
    )
    G_t = sp.simplify(
        (radius * sp.diff(response_B, radius) + response_B) / radius**2
    )
    G_r = sp.simplify(
        (
            radius
            * (
                response_B * sp.diff(f_metric, radius) / f_metric
                + sp.diff(response_A, radius)
                - response_A * sp.diff(f_metric, radius) / f_metric
            )
            + response_B
        )
        / radius**2
    )
    epsilon = sp.symbols("epsilon")
    A = f_metric + epsilon * response_A
    B = f_metric + epsilon * response_B
    G_angle_exact = (
        B * sp.diff(A, radius, 2) / (2 * A)
        - B * sp.diff(A, radius) ** 2 / (4 * A**2)
        + sp.diff(A, radius) * sp.diff(B, radius) / (4 * A)
        + B * sp.diff(A, radius) / (2 * A * radius)
        + sp.diff(B, radius) / (2 * radius)
    )
    G_angle = sp.simplify(
        sp.diff(G_angle_exact, epsilon).subs(epsilon, 0)
    )
    potential = response_A / 2
    acceleration = sp.simplify(-sp.diff(potential, radius))
    expected_acceleration = (
        128 * mass**3 * (36 * radius - 55 * mass) / radius**11
    )
    return {
        "conservation": conservation == 0,
        "tt": sp.simplify(G_t + H_t) == 0,
        "rr": sp.simplify(G_r + H_r) == 0,
        "angular": sp.simplify(G_angle + H_angle) == 0,
        "acceleration": sp.simplify(acceleration - expected_acceleration) == 0,
    }


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(checks, "V4966_00", "all locked files exist", [], missing, not missing)

    bad_hashes = {
        str(path.relative_to(ROOT)): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "V4966_01", "all locked hashes match", {}, bad_hashes, not bad_hashes)

    syntax_errors: dict[str, str] = {}
    for path in (MAIN_SCRIPT, Path(__file__)):
        try:
            ast.parse(text(path), filename=str(path))
        except SyntaxError as error:
            syntax_errors[str(path)] = str(error)
    add(checks, "V4966_02", "generator and validator parse", {}, syntax_errors, not syntax_errors)

    result = json.loads(text(RESULT_JSON))
    normalization_rows = read_csv(NORMALIZATION_CSV)
    determinant_rows = read_csv(DETERMINANT_CSV)
    rank_rows = read_csv(RANK_CSV)
    projector_rows = read_csv(STATIC_PROJECTOR_CSV)
    metric_rows = read_csv(SCHWARZSCHILD_CSV)
    boundary_rows = read_csv(BOUNDARY_CSV)
    decision_rows = read_csv(DECISION_CSV)
    generated_tables = [
        normalization_rows,
        determinant_rows,
        rank_rows,
        projector_rows,
        metric_rows,
        boundary_rows,
        decision_rows,
    ]
    add(
        checks,
        "V4966_03",
        "all generated CSV files are nonempty and well formed",
        True,
        [len(rows) for rows in generated_tables],
        all(rows and not malformed(rows) for rows in generated_tables),
    )
    add(
        checks,
        "V4966_04",
        "all generated rows carry marker and remain nonclaim",
        True,
        True,
        all(
            row.get("checkpoint_marker") == MARKER
            and not truth(row.get("valid_for_full_MTS_claim"))
            for rows in generated_tables
            for row in rows
        ),
    )

    source_state = result["source_state"]
    add(
        checks,
        "V4966_05",
        "all inherited source hashes and clauses pass",
        True,
        source_state,
        not source_state["missing"]
        and not source_state["bad_hashes"]
        and all(source_state["clauses"].values()),
    )

    normalization = result["normalization"]
    add(
        checks,
        "V4966_06",
        "physical portal normalization is U4=utilde/g^2=W_O4",
        "U4=w_O4/l_P^4=utilde_O4/g^2=W_O4",
        normalization["physical_IR_coordinate"],
        normalization["physical_IR_coordinate"]
        == "U4=w_O4/l_P^4=utilde_O4/g^2=W_O4",
    )
    add(
        checks,
        "V4966_07",
        "both N8 U4 endpoints are finite nonzero and negative",
        True,
        [normalization["U4_min"], normalization["U4_max"]],
        normalization["nonzero_on_both_schemes"]
        and normalization["U4_min"] < normalization["U4_max"] < 0,
    )
    add(
        checks,
        "V4966_08",
        "N8 U4 scheme spread is below 1e-4",
        "<1e-4",
        normalization["relative_spread"],
        normalization["relative_spread"] < 1.0e-4,
    )

    determinant = result["O4_determinant"]
    add(
        checks,
        "V4966_09",
        "all determinant algebra checks pass",
        True,
        determinant["checks"],
        all(determinant["checks"].values()),
    )
    add(
        checks,
        "V4966_10",
        "linear derivative-free O4 p8 source is zero",
        "ZERO",
        determinant["linear_p8_source"],
        determinant["linear_p8_source"] == "ZERO",
    )
    add(
        checks,
        "V4966_11",
        "quadratic O4 source is B_C-only with [1,1] helicity direction",
        [1, 1],
        determinant["helicity_source_direction"],
        determinant["helicity_source_direction"] == [1, 1]
        and determinant["MTS_Bt_log_residue"] == "0",
    )

    U4 = sp.symbols("U4", nonzero=True)
    mu = sp.symbols("mu_psi", positive=True)
    residue_matrix = sp.Matrix(
        [
            [1 / (60480 * sp.pi * mu**4), 3 * U4**2 * mu**4 / sp.pi],
            [1 / (50400 * sp.pi * mu**4), 3 * U4**2 * mu**4 / sp.pi],
        ]
    )
    residue_det = sp.factor(residue_matrix.det())
    add(
        checks,
        "V4966_12",
        "independent residue determinant matches exactly",
        "-U4**2/(100800*pi**2)",
        str(residue_det),
        residue_det == -U4**2 / (100800 * sp.pi**2),
    )
    rank = result["two_source_rank"]
    add(
        checks,
        "V4966_13",
        "known motion source-direction rank is two",
        2,
        rank["known_motion_source_direction_rank"],
        rank["direction_determinant"] == "-1/5"
        and rank["known_motion_source_direction_rank"] == 2
        and all(rank["checks"].values()),
    )
    add(
        checks,
        "V4966_14",
        "rank closure is not promoted to a finite total vector",
        False,
        rank["total_finite_parent_vector_known"],
        not rank["total_finite_parent_vector_known"],
    )

    static = result["static_response"]
    add(
        checks,
        "V4966_15",
        "all generator Schwarzschild tensor checks pass",
        True,
        static["checks"],
        all(static["checks"].values()),
    )
    independent = independent_static_checks()
    add(
        checks,
        "V4966_16",
        "independent conservation and three field equations pass",
        True,
        independent,
        all(independent.values()),
    )
    add(
        checks,
        "V4966_17",
        "static real and helicity projectors have rank one",
        [[1, 0], ["1/2", "1/2"], 1],
        [
            static["static_projector_real_basis"],
            static["static_projector_helicity_basis"],
            static["static_projector_rank"],
        ],
        static["static_projector_real_basis"] == [1, 0]
        and static["static_projector_helicity_basis"] == ["1/2", "1/2"]
        and static["static_projector_rank"] == 1,
    )
    add(
        checks,
        "V4966_18",
        "Y squared first variation is an exact parity zero",
        "ZERO_BY_PARITY",
        static["Y2_first_variation"],
        static["Y2_first_variation"] == "ZERO_BY_PARITY",
    )
    add(
        checks,
        "V4966_19",
        "fixed-mass Schwarzschild A and B kernels match",
        True,
        static["metric_response"],
        static["metric_response"]["delta_A_over_bC"]
        == "128*M**3*(-11*M + 8*r)/r**10"
        and static["metric_response"]["delta_B_over_bC"]
        == "128*M**3*(-67*M + 36*r)/r**10",
    )
    add(
        checks,
        "V4966_20",
        "static metric table contains no unit-weight placeholder",
        True,
        [row["status"] for row in metric_rows],
        any(row["response_id"] == "SCHW4966_05_A" for row in metric_rows)
        and any(row["response_id"] == "SCHW4966_06_B" for row in metric_rows)
        and all("MISSING" not in " ".join(row.values()) for row in metric_rows),
    )

    boundary_status = {row["boundary_id"]: row["current_status"] for row in boundary_rows}
    add(
        checks,
        "V4966_21",
        "finite p8 boundary and remaining source classes remain explicit",
        "OPEN",
        boundary_status,
        boundary_status["BOUND4966_02_finite_pair"] == "OPEN"
        and boundary_status["BOUND4966_03_gravity"] == "OPEN"
        and boundary_status["BOUND4966_04_photon"] == "OPEN",
    )
    decision = result["decision"]
    add(
        checks,
        "V4966_22",
        "claim boundary remains all-operator false and full-MTS false",
        [False, False],
        [decision["exact_all_operator_compact_GR"], decision["full_MTS"]],
        not decision["exact_all_operator_compact_GR"]
        and not decision["full_MTS"]
        and decision["total_finite_p8_vector"] == "OPEN",
    )
    add(
        checks,
        "V4966_23",
        "decision ledger selects finite matching rather than another basis audit",
        "SELECT_4967_FINITE_MATCHING",
        [row["status"] for row in decision_rows],
        any(
            row["decision_id"] == "DEC4966_06_next"
            and row["status"] == "SELECT_4967_FINITE_MATCHING"
            for row in decision_rows
        ),
    )

    claim_rows = read_csv(CLAIMS)
    claim_matches = [row for row in claim_rows if row["claim_id"] == "L-808"]
    add(
        checks,
        "V4966_24",
        "claims register contains exactly one L-808 nonclaim row",
        1,
        len(claim_matches),
        len(claim_matches) == 1
        and "finite_matching_open_private_nonclaim" in claim_matches[0]["status"],
    )
    variable_rows = read_csv(VARIABLES)
    required_symbols = (
        "U4_4966",
        "DeltaBCO4_4966",
        "P8MotionSourceRank4966_MTS",
        "StaticP8Projector4966_MTS",
        "P8SchwarzschildResponse4966_MTS",
        "PredictivityStatus4966_MTS",
    )
    counts = {
        symbol: sum(row["symbol"] == symbol for row in variable_rows)
        for symbol in required_symbols
    }
    add(
        checks,
        "V4966_25",
        "variable audit contains all six 4966 symbols exactly once",
        {symbol: 1 for symbol in required_symbols},
        counts,
        all(count == 1 for count in counts.values()),
    )
    add(
        checks,
        "V4966_26",
        "formal registers are well-formed and marker-synchronized",
        True,
        FORMAL_MARKER,
        not malformed(claim_rows)
        and not malformed(variable_rows)
        and all(
            FORMAL_MARKER in text(path)
            for path in (EQUATIONS, RED_TEAM, SPINE, FORMAL_NOTE)
        ),
    )
    add(
        checks,
        "V4966_27",
        "resume and local spine point to checkpoint 4966",
        True,
        [text(RESUME)[:500], text(LOCAL_SPINE)[:200]],
        "Last checkpoint: `4966-" in text(RESUME)
        and FORMAL_MARKER in text(RESUME)
        and "Through 4966" in text(LOCAL_SPINE)
        and FORMAL_MARKER in text(LOCAL_SPINE),
    )
    add(
        checks,
        "V4966_28",
        "checkpoint and formal note preserve the finite-boundary warning",
        True,
        True,
        "finite total [B_C,B_t]" in text(CHECKPOINT)
        and "finite total p8 vector" in text(FORMAL_NOTE)
        and "= open" in text(CHECKPOINT)
        and "= open" in text(FORMAL_NOTE)
        and "full MTS" in text(CHECKPOINT),
    )
    add(
        checks,
        "V4966_29",
        "working root is not a Git checkout",
        False,
        (ROOT / ".git").exists(),
        not (ROOT / ".git").exists(),
    )

    all_passed = all(row["passed"] for row in checks)
    add(
        checks,
        "V4966_30",
        "overall checkpoint validation",
        True,
        all_passed,
        all_passed,
    )
    write_output(checks)
    print(f"{MARKER}_VALIDATION_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_VALIDATION_PASS={sum(row['passed'] for row in checks)}/{len(checks)}", flush=True)
    return 0 if all(row["passed"] for row in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
