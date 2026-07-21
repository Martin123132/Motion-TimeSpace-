from __future__ import annotations

import csv
import math
import subprocess
import sys
from pathlib import Path


CHECKPOINT = "4847"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUNNER = POST / "scripts" / "coherent_load_covariant_stress_runner.py"
TIMESTAMP = "2026-07-09T21:30:00+00:00"


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUTPUT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def true(value: str) -> bool:
    return value.strip().lower() == "true"


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def check(check_id: str, passed: bool, detail: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "status": "PASS" if passed else "FAIL",
        "detail": detail,
        "valid_for_claim": False,
        "timestamp_utc": TIMESTAMP,
    }


def main() -> int:
    completed = subprocess.run(
        [sys.executable, str(RUNNER), "--output-dir", str(OUTPUT), "--timestamp", TIMESTAMP],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        print(completed.stdout)
        print(completed.stderr, file=sys.stderr)
        return completed.returncode

    sources = read_csv("P8_Y5_R2FR_4847_SOURCE_REGISTER.csv")
    theorems = read_csv("P8_Y5_R2FR_4847_COVARIANT_STRESS_THEOREM.csv")
    stress = read_csv("P8_Y5_R2FR_4847_STRESS_OUTPUT.csv")
    windows = read_csv("P8_Y5_R2FR_4847_STABILITY_WINDOW.csv")
    ward = read_csv("P8_Y5_R2FR_4847_WARD_TAU_OUTPUT.csv")
    decisions = read_csv("P8_Y5_R2FR_4847_DECISION.csv")
    old_flrw = read_csv("P8_Y5_R2FR_4846_FLRW_STRESS_OUTPUT.csv")

    static = [row for row in stress if float(row["y"]) == 0.0]
    negative_windows = [row for row in windows if row["Gamma_star_sign"] == "negative"]
    positive_windows = [row for row in windows if row["Gamma_star_sign"] == "positive"]
    external = next(row for row in ward if row["ward_id"] == "WARD4847_2_external_u_forbidden")
    local_ward = next(row for row in ward if row["ward_id"] == "WARD4847_3_stationary_local")
    claim_rows = list(csv.DictReader((FORMAL / "02-claims-register.csv").open(newline="", encoding="utf-8")))
    claim = [row for row in claim_rows if row.get("claim_id") == "L-689"]
    checkpoint = (POST / "4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md").read_text(encoding="utf-8")
    formal = (FORMAL / "863-PPC4161-coherent-load-covariant-Hilbert-stress-tau-Euler-and-stability-window.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    common_match = True
    for new_row in stress:
        new_y = float(new_row["y"])
        if not any(math.isclose(new_y, target, rel_tol=0.0, abs_tol=1.0e-14) for target in (0.1, 1.0, 3.0)):
            continue
        old_row = next(
            row
            for row in old_flrw
            if row["kernel"] == new_row["kernel"]
            and math.isclose(float(row["y_ellH_cubed"]), new_y, rel_tol=0.0, abs_tol=1.0e-14)
        )
        common_match &= math.isclose(
            float(new_row["kappa_rho_over_Gamma_star"]),
            float(old_row["kappa_rho_over_Gamma_star"]),
            rel_tol=1.0e-13,
            abs_tol=1.0e-13,
        )
        common_match &= math.isclose(
            float(new_row["kappa_p_over_Gamma_star"]),
            float(old_row["kappa_p_over_Gamma_star"]),
            rel_tol=1.0e-13,
            abs_tol=1.0e-13,
        )

    all_rows = sources + theorems + stress + windows + ward + decisions
    validations = [
        check(
            "VAL4847_00_sources",
            len(sources) == 7 and all(true(row["source_exists"]) and true(row["needle_found"]) for row in sources),
            f"sources={len(sources)}",
        ),
        check(
            "VAL4847_01_theorems",
            len(theorems) == 8
            and any(row["theorem_id"] == "CHS4847_2_stress" for row in theorems)
            and any(row["theorem_id"] == "CHS4847_5_tau_pullback" for row in theorems),
            "covariant stress and tau pullback theorem rows present",
        ),
        check(
            "VAL4847_02_static_zero",
            len(static) == 2
            and all(float(row["kappa_rho_over_Gamma_star"]) == 0.0 for row in static)
            and all(float(row["kappa_p_over_Gamma_star"]) == 0.0 for row in static)
            and all(float(row["G_theta_over_Gamma_star_ell"]) == 0.0 for row in static),
            f"static rows={len(static)}",
        ),
        check(
            "VAL4847_03_perfect_fluid",
            all(row["heat_flux"] == "0" and row["anisotropic_stress"] == "0" for row in stress),
            "all minimal-sector heat and anisotropic rows vanish",
        ),
        check(
            "VAL4847_04_rho_plus_p_identity",
            max(abs(float(row["rho_plus_p_identity_residual"])) for row in stress) < 1.0e-14,
            "rho+p=dot(G_theta)/kappa",
        ),
        check(
            "VAL4847_05_flrw_reproduction",
            common_match,
            "covariant stress reproduces 4846 lapse/scale-factor rows",
        ),
        check(
            "VAL4847_06_hessian_roots",
            math.isclose(float(negative_windows[0]["lower_y"]), 2.0 / 3.0, rel_tol=1.0e-12)
            and math.isclose(float(negative_windows[1]["lower_y"]), 0.6114532915782878, rel_tol=1.0e-12),
            "exponential and tanh G_theta_theta roots",
        ),
        check(
            "VAL4847_07_negative_windows",
            len(negative_windows) == 2
            and all(true(row["positive_density"]) for row in negative_windows)
            and all(true(row["positive_G_theta_theta"]) for row in negative_windows)
            and all(true(row["positive_density_and_G_convexity_window"]) for row in negative_windows),
            "negative-amplitude density/convexity windows exist for both kernels",
        ),
        check(
            "VAL4847_08_positive_branch_guard",
            len(positive_windows) == 2
            and all(true(row["positive_density"]) for row in positive_windows)
            and all(not true(row["positive_G_theta_theta"]) for row in positive_windows),
            "positive-amplitude large-y branch retains total kinetic bound",
        ),
        check(
            "VAL4847_09_ward",
            external["status"] == "FAILED_EXTERNAL_FLOW_CONTROL"
            and local_ward["status"] == "EXACT_LOCAL_MEMORY_STRESS_AND_EULER_ZERO_PRIVATE",
            f"{external['status']}; {local_ward['status']}",
        ),
        check(
            "VAL4847_10_nonclaim",
            all(not true(row.get("valid_for_claim", "false")) for row in all_rows),
            "all generated rows remain nonclaim",
        ),
        check(
            "VAL4847_11_claim",
            len(claim) == 1 and claim[0].get("status") == "coherent_load_covariant_stress_private_nonclaim",
            f"L-689 rows={len(claim)}",
        ),
        check(
            "VAL4847_12_documents",
            "COVARIANT_COHERENT_LOAD_HILBERT_STRESS_DERIVED" in checkpoint
            and "COHERENT_LOAD_COVARIANT_STRESS_AND_STABILITY_WINDOW" in formal,
            "checkpoint and formal bridge markers present",
        ),
        check(
            "VAL4847_13_resume",
            "Last checkpoint: `4847-" in resume and "4848-Y5-R2FR-H-load" in resume,
            "resume points from 4847 to 4848",
        ),
        check(
            "VAL4847_14_compile",
            compiles(RUNNER) and compiles(Path(__file__).resolve()),
            "runner and validator compile from source",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(
        check(
            "VAL4847_OVERALL",
            overall,
            "COVARIANT_STRESS_TAU_EULER_AND_DENSITY_KINETIC_PRECHECK_WINDOWS_VALIDATED",
        )
    )
    write_csv(OUTPUT / "P8_Y5_BRR545_4847_VALIDATION.csv", validations)
    print("P8_Y5_BRR545_4847_VALIDATION_PASS" if overall else "P8_Y5_BRR545_4847_VALIDATION_FAIL")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
