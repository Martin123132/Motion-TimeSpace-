from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


CHECKPOINT = "4848"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUN = POST / "runs" / "20260709-4848-H-load-smoke-fit-bg2"
DRY_RUN = POST / "runs" / "20260709-4848-H-load-dry-run"
TIMESTAMP = "2026-07-09T22:15:00+00:00"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "SRC4848_00_4847",
            POST / "4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md",
            "Covariant Hilbert stress",
            "action-derived density and negative-amplitude window",
        ),
        (
            "SRC4848_01_checkpoint",
            POST / "4848-Y5-R2FR-H-load-background-equation-negative-amplitude-window-and-cosmology-smoke-runner.md",
            "H_LOAD_IMPLICIT_BACKGROUND_UNIQUE_BRANCH_DERIVED",
            "human-readable derivation and fit result",
        ),
        (
            "SRC4848_02_formal",
            FORMAL / "864-PPC4161-H-load-implicit-background-and-negative-amplitude-cosmology-smoke.md",
            "H_LOAD_NEGATIVE_AMPLITUDE_COLLAPSES_TO_LCDM",
            "formal-workbench integration",
        ),
        (
            "SRC4848_03_runner",
            POST / "scripts" / "H_load_cosmology_smoke_runner.py",
            "def solve_hload_e",
            "implicit background and real-likelihood runner",
        ),
        (
            "SRC4848_04_config",
            FORMAL / "configs" / "cosmology_background_R1_current.json",
            "DESI_DR2_BAO",
            "data and baseline configuration",
        ),
        (
            "SRC4848_05_pantheon",
            FORMAL / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat",
            "MU_SH0ES",
            "real supernova likelihood data",
        ),
        (
            "SRC4848_06_desi",
            FORMAL / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt",
            "DM_over_rs",
            "real DESI DR2 BAO measurements",
        ),
        (
            "SRC4848_07_results",
            RUN / "results" / "H_load_smoke_results.csv",
            "HLOAD_EXP_NEG",
            "completed fit results",
        ),
        (
            "SRC4848_08_dry",
            DRY_RUN / "results" / "H_load_smoke_results.csv",
            "HLOAD_TANH_NEG",
            "nonzero-amplitude solver dry run",
        ),
        (
            "SRC4848_09_validator",
            Path(__file__).resolve(),
            'CHECKPOINT = "4848"',
            "checkpoint generator and validator",
        ),
    ]
    rows = []
    for source_id, path, needle, role in sources:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "equation_id": "HBG4848_0_definitions",
            "formula": "E=H/H0; q=ell_Q H0; A_H=Gamma_star/(3H0^2); R=F-3yF'",
            "result": "dimensionless background variables",
            "status": "DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "equation_id": "HBG4848_1_closure",
            "formula": "Omega_Gamma0=1-Omega_m0-A_H R(q^3)",
            "result": "E(0)=1 exactly",
            "status": "DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "equation_id": "HBG4848_2_implicit",
            "formula": "E^2=Omega_m0(1+z)^3+1-Omega_m0+A_H[R((qE)^3)-R(q^3)]",
            "result": "action-derived implicit Friedmann equation",
            "status": "DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "equation_id": "HBG4848_3_derivative",
            "formula": "dF_E/dE=2E-3A_H q^3 E^2 R'(y)",
            "result": ">=2E for A_H<=0 and y in/past the negative-amplitude window",
            "status": "UNIQUE_EXPANDING_BRANCH_PROVED",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "equation_id": "HBG4848_4_sign",
            "formula": "A_H[R((qE)^3)-R(q^3)]<=0 for z>=0",
            "result": "negative branch only lowers E^2 relative to LCDM at fixed Omega_m0",
            "status": "SIGN_THEOREM_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
    ]


def summary_rows(raw: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in raw:
        if row["mode"] != "fit":
            continue
        params = json.loads(row["params_json"])
        diagnostics = json.loads(row["diagnostics_json"]) if row["diagnostics_json"] else {}
        rows.append(
            {
                "branch": row["branch"],
                "model": row["model"],
                "chi2_total": row["chi2_total"],
                "n_params": row["n_params"],
                "aic": row["aic"],
                "bic": row["bic"],
                "delta_chi2_vs_M0": row["delta_chi2_vs_M0"],
                "delta_aic_vs_best_baseline": row["delta_aic_vs_best_baseline"],
                "delta_bic_vs_best_baseline": row["delta_bic_vs_best_baseline"],
                "best_aic_baseline": row["best_aic_baseline"],
                "best_bic_baseline": row["best_bic_baseline"],
                "A_H": params.get("A_H", ""),
                "q_H": params.get("q_H", ""),
                "omega_m0": params.get("omega_m0", ""),
                "h0": params.get("h0", ""),
                "rd": params.get("rd", ""),
                "maximum_equation_residual": diagnostics.get("maximum_equation_residual", ""),
                "minimum_implicit_derivative": diagnostics.get("minimum_implicit_derivative", ""),
                "homogeneous_kinetic_bracket0": diagnostics.get("homogeneous_kinetic_bracket0", ""),
                "edge_flags": row["edge_flags"],
                "success": row["success"],
                "decision": (
                    "NEGATIVE_H_LOAD_COLLAPSES_TO_LCDM"
                    if row["model"].startswith("HLOAD")
                    else "FITTED_BASELINE"
                ),
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4848_0_negative_H_load",
            "decision": "demote_negative_amplitude_local_H_load_cosmology",
            "reason": "both kernels and both SN branches optimize to A_H=0 and inherit the LCDM chi-square",
            "next_action": "one positive-amplitude total-kinetic-bound test",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4848_1_no_prior_widening",
            "decision": "do_not_widen_negative_A_H_prior",
            "reason": "the sign theorem proves every more-negative value lowers E^2 in the same disfavoured direction",
            "next_action": "change the physically derived sign branch, not the optimizer box",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4848_2_scope",
            "decision": "retain_local_Z_theorem_and_old_N_history_as_separate_branches",
            "reason": "the failed object is the new local H-load background law, not the response-doublet theorem or N/u3 history kernel",
            "next_action": "do not propagate this cosmology failure into unrelated local or EM claims",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4848_3_next",
            "decision": "positive_H_load_kinetic_bound_or_demotion",
            "reason": "sign-complete action test is the final fair local-H-load gate",
            "next_action": "4849 positive-H-load total-kinetic-bound parameterization",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    dry: list[dict[str, str]],
) -> list[dict[str, Any]]:
    h_rows = [row for row in summary if row["model"].startswith("HLOAD")]
    baseline_rows = [row for row in summary if row["model"] == "M0"]
    dry_h = [row for row in dry if row["model"].startswith("HLOAD")]
    claim_rows = read_csv(FORMAL / "02-claims-register.csv")
    claim = [row for row in claim_rows if row.get("claim_id") == "L-690"]
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    checkpoint = (POST / "4848-Y5-R2FR-H-load-background-equation-negative-amplitude-window-and-cosmology-smoke-runner.md").read_text(encoding="utf-8")
    formal = (FORMAL / "864-PPC4161-H-load-implicit-background-and-negative-amplitude-cosmology-smoke.md").read_text(encoding="utf-8")
    run_status = json.loads((RUN / "status.json").read_text(encoding="utf-8"))

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    checks = [
        result(
            "VAL4848_00_sources",
            len(sources) == 10 and all(row["source_exists"] and row["needle_found"] for row in sources),
            f"sources={len(sources)}",
        ),
        result("VAL4848_01_run_done", run_status.get("status") == "done" and (RUN / "DONE.txt").exists(), str(run_status)),
        result("VAL4848_02_fit_count", len(summary) == 10 and len(h_rows) == 4, f"fit={len(summary)} H={len(h_rows)}"),
        result("VAL4848_03_convergence", all(true(row["success"]) for row in summary), "all fits converged"),
        result(
            "VAL4848_04_A_zero",
            all(abs(float(row["A_H"])) < 1.0e-14 for row in h_rows),
            "; ".join(f"{row['branch']}:{row['model']}={row['A_H']}" for row in h_rows),
        ),
        result(
            "VAL4848_05_chi2_LCDM",
            all(
                abs(
                    float(row["chi2_total"])
                    - float(next(base["chi2_total"] for base in baseline_rows if base["branch"] == row["branch"]))
                )
                < 1.0e-7
                for row in h_rows
            ),
            "all H-load fits reproduce branch-matched LCDM chi2",
        ),
        result(
            "VAL4848_06_penalties",
            all(float(row["delta_aic_vs_best_baseline"]) > 0.0 and float(row["delta_bic_vs_best_baseline"]) > 0.0 for row in h_rows),
            "all H-load AIC/BIC deltas are positive",
        ),
        result(
            "VAL4848_07_equation_residual",
            max(float(row["maximum_equation_residual"]) for row in h_rows) < 3.0e-15,
            "fitted implicit equation residuals below 3e-15",
        ),
        result(
            "VAL4848_08_nonzero_dry_solver",
            len(dry_h) == 4
            and max(
                json.loads(row["diagnostics_json"])["maximum_equation_residual"]
                for row in dry_h
            )
            < 3.0e-15,
            "nonzero-amplitude dry rows solve the implicit equation",
        ),
        result(
            "VAL4848_09_positive_derivative",
            all(float(row["minimum_implicit_derivative"]) >= 2.0 for row in h_rows),
            "fitted branch has positive implicit derivative",
        ),
        result(
            "VAL4848_10_claim",
            len(claim) == 1 and claim[0].get("status") == "H_load_negative_amplitude_demoted_private_nonclaim",
            f"L-690 rows={len(claim)}",
        ),
        result(
            "VAL4848_11_documents",
            "H_LOAD_IMPLICIT_BACKGROUND_UNIQUE_BRANCH_DERIVED" in checkpoint
            and "H_LOAD_NEGATIVE_AMPLITUDE_COLLAPSES_TO_LCDM" in formal,
            "checkpoint and formal markers present",
        ),
        result(
            "VAL4848_12_resume",
            "Last checkpoint: `4848-" in resume and "4849-Y5-R2FR-positive-H-load" in resume,
            "resume points from 4848 to 4849",
        ),
        result(
            "VAL4848_13_nonclaim",
            all(not true(row.get("valid_for_claim", False)) for row in sources + summary),
            "all generated evidence remains nonclaim",
        ),
        result(
            "VAL4848_14_compile",
            _compiles(POST / "scripts" / "H_load_cosmology_smoke_runner.py") and _compiles(Path(__file__).resolve()),
            "runner and validator compile from source",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        result(
            "VAL4848_OVERALL",
            overall,
            "H_LOAD_UNIQUE_BACKGROUND_AND_NEGATIVE_AMPLITUDE_REAL_LIKELIHOOD_DEMOTION_VALIDATED",
        )
    )
    return checks


def _compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def main() -> int:
    raw = read_csv(RUN / "results" / "H_load_smoke_results.csv")
    dry = read_csv(DRY_RUN / "results" / "H_load_smoke_results.csv")
    sources = source_rows()
    equations = equation_rows()
    summary = summary_rows(raw)
    decisions = decision_rows()
    validation = validation_rows(sources, summary, dry)
    write_csv(OUTPUT / "P8_Y5_R2FR_4848_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4848_BACKGROUND_EQUATION.csv", equations)
    write_csv(OUTPUT / "P8_Y5_R2FR_4848_SMOKE_RESULTS.csv", summary)
    write_csv(OUTPUT / "P8_Y5_R2FR_4848_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4848_VALIDATION.csv", validation)
    overall = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4848_VALIDATION_PASS" if overall else "P8_Y5_BRR545_4848_VALIDATION_FAIL")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
