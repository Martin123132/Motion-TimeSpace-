from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


CHECKPOINT = "4849"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
RUNS = {
    "standard": POST / "runs" / "20260709-4849-H-load-positive-smoke-fit",
    "broad": POST / "runs" / "20260709-4849-H-load-positive-broad",
    "strict": POST / "runs" / "20260709-4849-H-load-positive-strict",
}
TIMESTAMP = "2026-07-09T23:00:00+00:00"


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


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC4849_00_4848", POST / "4848-Y5-R2FR-H-load-background-equation-negative-amplitude-window-and-cosmology-smoke-runner.md", "Sign theorem", "negative-branch demotion and implicit equation"),
        ("SRC4849_01_checkpoint", POST / "4849-Y5-R2FR-positive-H-load-total-kinetic-bound-parameterization-or-local-H-load-cosmology-demotion.md", "POSITIVE_H_LOAD_KINETIC_FRACTION_PARAMETERIZATION_DERIVED", "human-readable derivation and robustness result"),
        ("SRC4849_02_formal", FORMAL / "865-PPC4161-positive-H-load-kinetic-fraction-and-robustness-result.md", "POSITIVE_H_LOAD_SH0ES_GAIN_KINETIC_EDGE", "formal-workbench integration"),
        ("SRC4849_03_runner", POST / "scripts" / "H_load_positive_kinetic_smoke_runner.py", "def amplitude_from_fraction", "kinetic-safe real likelihood runner"),
        ("SRC4849_04_standard", RUNS["standard"] / "results" / "H_load_positive_smoke_results.csv", "HLOAD_EXP_POS_KSAFE", "standard 99 percent saturation fit"),
        ("SRC4849_05_broad", RUNS["broad"] / "results" / "H_load_positive_smoke_results.csv", "HLOAD_TANH_POS_KSAFE", "broad 99.9 percent saturation fit"),
        ("SRC4849_06_strict", RUNS["strict"] / "results" / "H_load_positive_smoke_results.csv", "HLOAD_EXP_POS_KSAFE", "strict f_K<=0.8 fit"),
        ("SRC4849_07_pantheon", FORMAL / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat", "MU_SH0ES", "real supernova data"),
        ("SRC4849_08_desi", FORMAL / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt", "DM_over_rs", "real DESI DR2 BAO data"),
        ("SRC4849_09_claims", FORMAL / "02-claims-register.csv", "L-691", "nonclaim register row"),
        ("SRC4849_10_validator", Path(__file__).resolve(), 'CHECKPOINT = "4849"', "checkpoint validator"),
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


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("KFR4849_0_hessian", "G_theta_theta=3 A_H q^2 h(q)", "h(q)<0 on positive-density branch"),
        ("KFR4849_1_amax", "A_max(q)=6/[-27 q^2 h(q)]", "homogeneous kinetic fold occurs at A_H=A_max"),
        ("KFR4849_2_fraction", "A_H=f_K A_max(q), 0<=f_K<1", "physical kinetic-fraction parameter"),
        ("KFR4849_3_kinetic", "K0=6+9G_theta_theta=6(1-f_K)", "positive homogeneous bracket by construction"),
        ("KFR4849_4_root", "partial_E F_E|0=2(1-f_K)", "same fraction controls implicit-root fold"),
        ("KFR4849_5_data_era", "partial_E F_E>=2E(1-f_K)>0 for z>=0", "unique expanding branch when |h| decreases past threshold"),
        ("KFR4849_6_scope", "positive K0 is not full scalar/vector/tensor stability", "parent tau kinetic matrix remains required"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "formula": formula,
            "consequence": consequence,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for theorem_id, formula, consequence in rows
    ]


def fit_rows() -> list[dict[str, Any]]:
    output = []
    for variant, folder in RUNS.items():
        raw = read_csv(folder / "results" / "H_load_positive_smoke_results.csv")
        for row in raw:
            if row["mode"] != "fit":
                continue
            params = json.loads(row["params_json"])
            diagnostics = json.loads(row["diagnostics_json"]) if row["diagnostics_json"] else {}
            output.append(
                {
                    "variant": variant,
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
                    "f_K": params.get("f_K", ""),
                    "q_H": params.get("q_H", ""),
                    "A_H": diagnostics.get("A_H", ""),
                    "A_H_max": diagnostics.get("A_H_max", ""),
                    "omega_gamma0": diagnostics.get("omega_gamma0", ""),
                    "rho_shape0": diagnostics.get("rho_shape0", ""),
                    "homogeneous_kinetic_bracket0": diagnostics.get("homogeneous_kinetic_bracket0", ""),
                    "expected_kinetic_bracket0": diagnostics.get("expected_kinetic_bracket0", ""),
                    "minimum_implicit_derivative": diagnostics.get("minimum_implicit_derivative", ""),
                    "maximum_equation_residual": diagnostics.get("maximum_equation_residual", ""),
                    "edge_flags": row["edge_flags"],
                    "success": row["success"],
                    "status": (
                        "SH0ES_KINETIC_EDGE_LEAD"
                        if row["branch"] == "sh0es" and row["model"].startswith("HLOAD")
                        else "NO_SH0ES_NOT_BEST_BASELINE"
                        if row["branch"] == "no_sh0es" and row["model"].startswith("HLOAD")
                        else "FITTED_BASELINE"
                    ),
                    "valid_for_claim": False,
                    "timestamp_utc": TIMESTAMP,
                }
            )
    return output


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC4849_0_math", "retain kinetic-fraction parameterization", "it ties background uniqueness and homogeneous kinetic sign to one physical margin"),
        ("DEC4849_1_sh0es", "retain SH0ES direction as private lead only", "AIC/BIC gain survives strict cap but every optimizer hits f_K maximum"),
        ("DEC4849_2_no_sh0es", "no independent cosmology promotion", "no-SH0ES is not preferred against best AIC/BIC baseline and sits at q lower edge"),
        ("DEC4849_3_background", "carry bare Gamma0 cancellation explicitly", "broad SH0ES fits require negative omega_Gamma0"),
        ("DEC4849_4_next", "derive parent tau perturbation matrix before more distance fitting", "blind widening would only move closer to the kinetic fold"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for decision_id, decision, reason in rows
    ]


def validation_rows(sources: list[dict[str, Any]], fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    h_fits = [row for row in fits if row["model"].startswith("HLOAD")]
    broad_sh0es = [row for row in h_fits if row["variant"] == "broad" and row["branch"] == "sh0es"]
    strict_sh0es = [row for row in h_fits if row["variant"] == "strict" and row["branch"] == "sh0es"]
    broad_no = [row for row in h_fits if row["variant"] == "broad" and row["branch"] == "no_sh0es"]
    standard_sh0es = [row for row in h_fits if row["variant"] == "standard" and row["branch"] == "sh0es"]
    claim = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-691"]
    checkpoint = (POST / "4849-Y5-R2FR-positive-H-load-total-kinetic-bound-parameterization-or-local-H-load-cosmology-demotion.md").read_text(encoding="utf-8")
    formal = (FORMAL / "865-PPC4161-positive-H-load-kinetic-fraction-and-robustness-result.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    checks = [
        result("VAL4849_00_sources", len(sources) == 11 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4849_01_runs_done", all(json.loads((folder / "status.json").read_text())["status"] == "done" for folder in RUNS.values()), "standard broad strict done"),
        result("VAL4849_02_fit_count", len(fits) == 30 and len(h_fits) == 12, f"fits={len(fits)} H={len(h_fits)}"),
        result("VAL4849_03_converged", all(true(row["success"]) for row in fits), "all fits converged"),
        result(
            "VAL4849_04_kinetic_identity",
            all(
                math.isclose(
                    float(row["homogeneous_kinetic_bracket0"]),
                    float(row["expected_kinetic_bracket0"]),
                    rel_tol=1.0e-12,
                    abs_tol=1.0e-12,
                )
                for row in h_fits
            ),
            "K0=6(1-f_K) on all H rows",
        ),
        result(
            "VAL4849_05_positive_root",
            all(float(row["minimum_implicit_derivative"]) > 0.0 for row in h_fits),
            "all implicit derivatives positive",
        ),
        result(
            "VAL4849_06_equation_residual",
            max(float(row["maximum_equation_residual"]) for row in h_fits) < 3.1e-15,
            "all equation residuals below 3.1e-15",
        ),
        result(
            "VAL4849_07_broad_sh0es_gain",
            len(broad_sh0es) == 2
            and all(float(row["delta_aic_vs_best_baseline"]) < -9.9 for row in broad_sh0es)
            and all(float(row["delta_bic_vs_best_baseline"]) < -6.3 for row in broad_sh0es),
            "broad SH0ES beats fitted AIC/BIC baselines",
        ),
        result(
            "VAL4849_08_broad_edge",
            all("f_K=HIGH" in row["edge_flags"] and "q_H=HIGH" not in row["edge_flags"] for row in broad_sh0es),
            "saturation widening removes q edge but not kinetic edge",
        ),
        result(
            "VAL4849_09_strict_gain_edge",
            len(strict_sh0es) == 2
            and all(float(row["delta_aic_vs_best_baseline"]) < -6.7 for row in strict_sh0es)
            and all(float(row["delta_bic_vs_best_baseline"]) < -3.1 for row in strict_sh0es)
            and all("f_K=HIGH" in row["edge_flags"] for row in strict_sh0es),
            "strict SH0ES gain survives but remains kinetic-edge",
        ),
        result(
            "VAL4849_10_no_sh0es",
            len(broad_no) == 2
            and all(float(row["delta_aic_vs_best_baseline"]) > 0.0 for row in broad_no)
            and all(float(row["delta_bic_vs_best_baseline"]) > 0.0 for row in broad_no)
            and all("q_H=LOW" in row["edge_flags"] for row in broad_no),
            "no-SH0ES not preferred and sits at q lower edge",
        ),
        result(
            "VAL4849_11_standard_to_broad",
            len(standard_sh0es) == 2
            and all("q_H=HIGH" in row["edge_flags"] for row in standard_sh0es)
            and all("q_H=HIGH" not in row["edge_flags"] for row in broad_sh0es),
            "q saturation edge diagnosed as numerical prior artifact",
        ),
        result(
            "VAL4849_12_background_cancellation",
            all(float(row["omega_gamma0"]) < 0.0 for row in broad_sh0es),
            "broad SH0ES rows retain negative bare Gamma0 warning",
        ),
        result(
            "VAL4849_13_claim_documents",
            len(claim) == 1
            and claim[0].get("status") == "positive_H_load_edge_dependent_private_lead_nonclaim"
            and "POSITIVE_H_LOAD_KINETIC_FRACTION_PARAMETERIZATION_DERIVED" in checkpoint
            and "POSITIVE_H_LOAD_SH0ES_GAIN_KINETIC_EDGE" in formal,
            f"L-691 rows={len(claim)}",
        ),
        result(
            "VAL4849_14_resume_compile",
            "Last checkpoint: `4849-" in resume
            and "4850-Y5-R2FR-H-load-scalar-kinetic" in resume
            and compiles(POST / "scripts" / "H_load_positive_kinetic_smoke_runner.py")
            and compiles(Path(__file__).resolve()),
            "resume and scripts valid",
        ),
    ]
    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(result("VAL4849_OVERALL", overall, "POSITIVE_H_LOAD_KINETIC_FRACTION_ROBUSTNESS_VALIDATED_PRIVATE_LEAD_ONLY"))
    return checks


def main() -> int:
    sources = source_rows()
    theorems = theorem_rows()
    fits = fit_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, fits)
    write_csv(OUTPUT / "P8_Y5_R2FR_4849_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4849_KINETIC_FRACTION_THEOREM.csv", theorems)
    write_csv(OUTPUT / "P8_Y5_R2FR_4849_ROBUSTNESS_RESULTS.csv", fits)
    write_csv(OUTPUT / "P8_Y5_R2FR_4849_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4849_VALIDATION.csv", validation)
    overall = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4849_VALIDATION_PASS" if overall else "P8_Y5_BRR545_4849_VALIDATION_FAIL")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
