from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.optimize import root


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4936"
NOTEBOOK = SOURCE_DIR / "flows.nb"
EXTRACTED = SOURCE_DIR / "flows_input_extracted.wl"
MANIFEST = SOURCE_DIR / "flows_extraction_manifest.json"
PAPER = POST / "source-intake" / "functional_rg" / "4929" / "src2204" / "R2scalarMES.tex"
OUTPUT = SOURCE_DIR / "scalar_source_flow_evaluation_results.json"
TABLE_OUTPUT = SOURCE_DIR / "scalar_source_fixed_point_reproduction.csv"

MARKER = "MTS_4936_SCALAR_SOURCE_FLOW_EVALUATION"
EXPECTED_HASHES = {
    NOTEBOOK: "841302a39fcf8e665c7dd6ded43a77bedb37dbdce4c2b2cf571b4a48da565bc6",
    EXTRACTED: "314f637a6ae8cb921d6a19a770a7b0a6aa0ebaa4edda2a70dabb97d7d31381fd",
    MANIFEST: "d4b8c06044a271ceaba8956e57870ffdf0ee8cecf04e1494559da8fa9424909c",
    PAPER: "56a906bdfef4af8c1e7a337263636bd0b2d5c863b5d5c52382385b655da4bdd7",
}

SOURCE_POINTS = {
    "A": {
        "g": 0.2519733249374084,
        "g_Dphi4": -17.917913887706213,
        "theta": [0.4035049212269125, 1.9917728373283434],
        "gamma_phi": 0.830223954951144,
    },
    "B": {
        "g": 0.2541860842533906,
        "g_Dphi4": -6.032729822896007,
        "theta": [-0.40887640805948566, 1.967312862810108],
        "gamma_phi": 0.7819082334974441,
    },
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def notebook_expression(lines: list[str], prefix: str, g_symbol: sp.Symbol, x_symbol: sp.Symbol) -> sp.Expr:
    source = next(line[len(prefix) :].rstrip(";") for line in lines if line.startswith(prefix))
    source = re.sub(
        r"Subsuperscript\[g,\(\(DWLPhi\)\^\(4\)\),(\d+)\]",
        r"(x^\1)",
        source,
    )
    source = source.replace("Subscript[g,((DWLPhi)^(4))]", "x")
    source = source.replace("^", "**")
    return sp.sympify(
        source,
        locals={"g": g_symbol, "x": x_symbol, "Pi": sp.pi},
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    hash_failures = {
        path.as_posix(): {"expected": expected, "actual": digest(path)}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if hash_failures:
        raise RuntimeError(f"scalar source-flow hash mismatch: {hash_failures}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["source_sha256"] != EXPECTED_HASHES[NOTEBOOK]:
        raise RuntimeError("notebook extraction manifest does not own the locked notebook")
    lines = EXTRACTED.read_text(encoding="utf-8").splitlines()
    g_symbol, x_symbol = sp.symbols("g x", real=True)
    beta_g = notebook_expression(lines, "WLBetag=", g_symbol, x_symbol)
    beta_x = notebook_expression(lines, "WLBetagDWLPhi4=", g_symbol, x_symbol)
    gamma_phi = notebook_expression(lines, "WLGammaWLPhi=", g_symbol, x_symbol)

    beta_vector = sp.Matrix([beta_g, beta_x])
    stability_matrix = beta_vector.jacobian([g_symbol, x_symbol])
    beta_numeric = sp.lambdify((g_symbol, x_symbol), beta_vector, "numpy")
    stability_numeric = sp.lambdify(
        (g_symbol, x_symbol), stability_matrix, "numpy"
    )
    gamma_numeric = sp.lambdify((g_symbol, x_symbol), gamma_phi, "numpy")

    rows: list[dict[str, Any]] = []
    point_results: dict[str, Any] = {}
    for label, expected in SOURCE_POINTS.items():
        solution = root(
            lambda values: np.asarray(
                beta_numeric(values[0], values[1]), dtype=float
            ).reshape(2),
            np.array([expected["g"], expected["g_Dphi4"]], dtype=float),
            jac=lambda values: np.asarray(
                stability_numeric(values[0], values[1]), dtype=float
            ),
            method="hybr",
            tol=1e-12,
        )
        coordinates = np.asarray(solution.x, dtype=float)
        residual = np.asarray(beta_numeric(*coordinates), dtype=float).reshape(2)
        critical_exponents = np.sort(
            np.real_if_close(
                np.linalg.eigvals(
                    -np.asarray(stability_numeric(*coordinates), dtype=float)
                )
            ).astype(float)
        )
        gamma_value = float(gamma_numeric(*coordinates))
        expected_theta = np.sort(np.asarray(expected["theta"], dtype=float))
        relevant_directions = int(np.count_nonzero(critical_exponents > 0.0))
        point_result = {
            "solver_success": bool(solution.success),
            "solver_message": str(solution.message),
            "g": float(coordinates[0]),
            "g_Dphi4": float(coordinates[1]),
            "beta_residual_infinity_norm": float(np.max(np.abs(residual))),
            "critical_exponents": [float(value) for value in critical_exponents],
            "gamma_phi": gamma_value,
            "relevant_directions": relevant_directions,
            "coordinate_max_abs_error": float(
                np.max(
                    np.abs(
                        coordinates
                        - np.asarray([expected["g"], expected["g_Dphi4"]])
                    )
                )
            ),
            "critical_exponent_max_abs_error": float(
                np.max(np.abs(critical_exponents - expected_theta))
            ),
            "gamma_phi_abs_error": abs(gamma_value - expected["gamma_phi"]),
        }
        point_results[label] = point_result
        rows.append(
            {
                "fixed_point": label,
                "g": point_result["g"],
                "g_Dphi4": point_result["g_Dphi4"],
                "theta_1_sorted": point_result["critical_exponents"][0],
                "theta_2_sorted": point_result["critical_exponents"][1],
                "gamma_phi": gamma_value,
                "relevant_directions": relevant_directions,
                "beta_residual_infinity_norm": point_result[
                    "beta_residual_infinity_norm"
                ],
                "source_reproduced": True,
                "valid_for_MTS_motion_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    additive_x_source = sp.cancel(beta_x.subs(x_symbol, 0))
    additive_x_series = sp.series(additive_x_source, g_symbol, 0, 5)
    gamma_phi_gravity_series = sp.series(
        sp.cancel(gamma_phi.subs(x_symbol, 0)), g_symbol, 0, 4
    )
    leading_additive_x = sp.limit(additive_x_source / g_symbol**2, g_symbol, 0)
    leading_gamma_phi = sp.limit(
        gamma_phi.subs(x_symbol, 0) / g_symbol, g_symbol, 0
    )

    checks = {
        "manifest_owns_notebook": manifest["source_sha256"]
        == EXPECTED_HASHES[NOTEBOOK],
        "all_source_points_converged": all(
            point["solver_success"] for point in point_results.values()
        ),
        "all_beta_residuals_below_1e_10": all(
            point["beta_residual_infinity_norm"] < 1e-10
            for point in point_results.values()
        ),
        "source_coordinates_reproduced": all(
            point["coordinate_max_abs_error"] < 1e-10
            for point in point_results.values()
        ),
        "source_exponents_reproduced": all(
            point["critical_exponent_max_abs_error"] < 1e-9
            for point in point_results.values()
        ),
        "source_gamma_phi_reproduced": all(
            point["gamma_phi_abs_error"] < 1e-10
            for point in point_results.values()
        ),
        "A_has_two_relevant_directions": point_results["A"][
            "relevant_directions"
        ]
        == 2,
        "B_has_one_relevant_direction": point_results["B"][
            "relevant_directions"
        ]
        == 1,
        "gravity_additively_generates_Dphi4": leading_additive_x
        == sp.Rational(406, 5),
        "gravity_generates_scalar_field_kernel": leading_gamma_phi
        == sp.Rational(451, 48) / sp.pi,
    }
    if not all(checks.values()):
        raise RuntimeError(f"scalar source-flow evaluation failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "source": {
            "paper": "Benjamin Knorr, Safe essential scalar-tensor theories, arXiv:2204.08564",
            "supplement_DOI": "10.17632/9v7ftgswc5.1",
            "notebook_file": "flows.nb",
            "evaluation": "exact extracted linear-regulator beta and gamma expressions independently parsed, rooted, differentiated, and evaluated",
        },
        "fixed_points": point_results,
        "derived_source_channels": {
            "beta_gDphi4_at_gDphi4_zero_series": str(additive_x_series),
            "leading_additive_gravity_source": str(leading_additive_x),
            "gamma_phi_at_gDphi4_zero_series": str(gamma_phi_gravity_series),
            "leading_gamma_phi_gravity_channel": str(leading_gamma_phi),
            "theorem": "the source flow has beta_gDphi4(g,0)=(406/5)g^2+O(g^3), so the scalar derivative interaction is not consistently set to zero once gravity is active",
        },
        "MTS_mapping_boundary": {
            "usable_result": "gravity can additively source essential scalar interactions and a nonzero scalar field-redefinition kernel in an explicitly executed primary-source flow",
            "not_yet_usable_as": "a numerical beta coefficient for the MTS fractional potential or the six-derivative O4=C^2(nabla psi)^2 portal",
            "gamma_warning": "gamma_phi is an essential-scheme field-redefinition gamma function and must not be identified numerically with eta_psi without deriving the convention map",
        },
        "checks": checks,
        "claim_boundary": {
            "primary_source_flow_executed": True,
            "gravity_scalar_additive_channel_proved": True,
            "MTS_motion_fixed_point_calculated": False,
            "MTS_O4_beta_calculated": False,
            "full_MTS_trajectory_calculated": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(TABLE_OUTPUT, rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_TABLE_SHA256={digest(TABLE_OUTPUT)}", flush=True)
    print(f"{MARKER}_ADDITIVE_DPHI4_SOURCE={leading_additive_x}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
