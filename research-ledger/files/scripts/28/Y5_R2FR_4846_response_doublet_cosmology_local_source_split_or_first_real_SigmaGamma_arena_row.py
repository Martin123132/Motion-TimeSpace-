from __future__ import annotations

import csv
import math
import subprocess
import sys
from pathlib import Path


CHECKPOINT = "4846"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUNNER = POST / "scripts" / "coherent_load_auxiliary_action_runner.py"
TIMESTAMP = "2026-07-09T20:30:00+00:00"


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUTPUT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


def close(value: str, target: float, tolerance: float = 1.0e-12) -> bool:
    return math.isclose(float(value), target, rel_tol=tolerance, abs_tol=tolerance)


def source_compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def result(check_id: str, passed: bool, detail: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "status": "PASS" if passed else "FAIL",
        "detail": detail,
        "valid_for_claim": False,
        "timestamp_utc": TIMESTAMP,
    }


def main() -> int:
    command = [
        sys.executable,
        str(RUNNER),
        "--output-dir",
        str(OUTPUT),
        "--timestamp",
        TIMESTAMP,
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr, file=sys.stderr)
        return completed.returncode

    source = read_csv("P8_Y5_R2FR_4846_SOURCE_REGISTER.csv")
    endpoint = read_csv("P8_Y5_R2FR_4846_ENDPOINT_OBSTRUCTION.csv")
    actions = read_csv("P8_Y5_R2FR_4846_ACTION_CONSTRUCTION.csv")
    branches = read_csv("P8_Y5_R2FR_4846_BRANCH_OUTPUT.csv")
    local = read_csv("P8_Y5_R2FR_4846_LOCAL_ENDPOINT_OUTPUT.csv")
    flrw = read_csv("P8_Y5_R2FR_4846_FLRW_STRESS_OUTPUT.csv")
    decisions = read_csv("P8_Y5_R2FR_4846_DECISION.csv")

    odd_rows = [row for row in endpoint if "analytic_odd" in row["route_id"]]
    determinant = next(row for row in endpoint if row["route_id"] == "EPO4846_3_even_load_determinant")
    nonanalytic = next(row for row in endpoint if row["route_id"] == "EPO4846_2_nonanalytic_escape")
    candidate = next(row for row in branches if row["branch_id"] == "BR4846_1_private_stationary_local")
    forbidden = next(row for row in branches if row["branch_id"] == "BR4846_3_forbidden_hand_switch")
    static_rows = [row for row in local if float(row["s_ell_theta_over_3"]) == 0.0]
    small_rows = [row for row in local if math.isclose(float(row["s_ell_theta_over_3"]), 1.0e-3)]
    roots = {
        row["kernel"]: float(row["positive_density_root_y"])
        for row in flrw
        if math.isclose(float(row["y_ellH_cubed"]), 1.0)
    }

    claim_rows = list(csv.DictReader((FORMAL / "02-claims-register.csv").open(newline="", encoding="utf-8")))
    claim_688 = [row for row in claim_rows if row.get("claim_id") == "L-688"]
    checkpoint_text = (POST / "4846-Y5-R2FR-response-doublet-cosmology-local-source-split-or-first-real-SigmaGamma-arena-row.md").read_text(encoding="utf-8")
    formal_text = (FORMAL / "862-PPC4161-response-doublet-cosmology-local-source-split-and-coherent-load-action.md").read_text(encoding="utf-8")
    resume_text = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    all_datasets = source + endpoint + actions + branches + local + flrw + decisions
    checks = [
        result(
            "VAL4846_00_sources",
            len(source) == 10 and all(bool_text(row["source_exists"]) and bool_text(row["needle_found"]) for row in source),
            f"sources={len(source)}; all paths and needles must resolve",
        ),
        result(
            "VAL4846_01_parity_no_go",
            len(odd_rows) == 2 and all(not bool_text(row["cubic_endpoint_possible"]) for row in odd_rows),
            "analytic exchange-odd response rows cannot produce cubic density",
        ),
        result(
            "VAL4846_02_nonanalytic_escape",
            nonanalytic["status"] == "REJECTED_NONANALYTIC_ORIGIN_ESCAPE",
            nonanalytic["status"],
        ),
        result(
            "VAL4846_03_determinant_cubic",
            bool_text(determinant["cubic_endpoint_possible"]) and determinant["density_leading_power"] == "3",
            determinant["status"],
        ),
        result(
            "VAL4846_04_same_action_branch",
            bool_text(candidate["same_action_local_flrw"])
            and bool_text(candidate["local_active_zero"])
            and bool_text(candidate["flrw_active"]),
            candidate["status"],
        ),
        result(
            "VAL4846_05_forbidden_switch",
            forbidden["status"] == "FAILED_ENVIRONMENT_SWITCH_CONTROL",
            forbidden["status"],
        ),
        result(
            "VAL4846_06_static_endpoint",
            len(static_rows) == 2
            and all(bool_text(row["exact_static_zero"]) for row in static_rows)
            and all(float(row["Gamma_mem_over_Gamma_star"]) == 0.0 for row in static_rows),
            f"static rows={len(static_rows)}",
        ),
        result(
            "VAL4846_07_cubic_quadratic_scaling",
            len(small_rows) == 2
            and all(math.isclose(float(row["Gamma_mem_over_Gamma_star"]) / 1.0e-9, 1.0, rel_tol=5.0e-7) for row in small_rows)
            and all(math.isclose(float(row["dGamma_ds_over_Gamma_star"]) / 3.0e-6, 1.0, rel_tol=5.0e-7) for row in small_rows),
            "F(s^3) scales as s^3 and dF/ds scales as 3s^2",
        ),
        result(
            "VAL4846_08_density_roots",
            close(str(roots["positive_branch_exponential"]), 1.9038136944403834)
            and close(str(roots["global_tanh"]), 1.4192231900240135),
            str(roots),
        ),
        result(
            "VAL4846_09_flrw_finite",
            len(flrw) == 10
            and all(math.isfinite(float(row["kappa_rho_over_Gamma_star"])) for row in flrw)
            and all(math.isfinite(float(row["kappa_p_over_Gamma_star"])) for row in flrw)
            and all(abs(float(row["continuity_residual_over_Gamma_star_H"])) < 1.0e-12 for row in flrw),
            f"FLRW rows={len(flrw)}",
        ),
        result(
            "VAL4846_10_nonclaim",
            all(not bool_text(row.get("valid_for_claim", "false")) for row in all_datasets),
            "all generated rows remain valid_for_claim=false",
        ),
        result(
            "VAL4846_11_claim_register",
            len(claim_688) == 1 and claim_688[0].get("status") == "coherent_load_auxiliary_action_private_nonclaim",
            f"L-688 rows={len(claim_688)}",
        ),
        result(
            "VAL4846_12_documents",
            "ANALYTIC_ODD_RESPONSE_CUBIC_NO_GO_PROVED" in checkpoint_text
            and "PRIVATE_SAME_ACTION_LOCAL_ZERO_FLRW_ACTIVE" in formal_text,
            "checkpoint and formal bridge markers present",
        ),
        result(
            "VAL4846_13_resume",
            "Last checkpoint: `4846-" in resume_text and "4847-Y5-R2FR-coherent-load" in resume_text,
            "resume points from 4846 to 4847",
        ),
        result(
            "VAL4846_14_compile",
            source_compiles(RUNNER) and source_compiles(Path(__file__).resolve()),
            "runner and validator compile from source without creating pycache",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        result(
            "VAL4846_OVERALL",
            overall,
            "ANALYTIC_PARITY_NO_GO_AND_COHERENT_LOAD_SAME_ACTION_LOCAL_FLRW_SPLIT_VALIDATED",
        )
    )
    write_csv(OUTPUT / "P8_Y5_BRR545_4846_VALIDATION.csv", checks)
    print("P8_Y5_BRR545_4846_VALIDATION_PASS" if overall else "P8_Y5_BRR545_4846_VALIDATION_FAIL")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
