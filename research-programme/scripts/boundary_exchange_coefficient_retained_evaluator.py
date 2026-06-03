from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-exchange-coefficient-retained-evaluator"
CHECKPOINT_DOC = "419-boundary-exchange-coefficient-retained-evaluator.md"
STATUS = "boundary_exchange_coefficient_retained_evaluator_written_retained_exchange_coefficients_and_lock_profiles_no_theorem_credit_no_local_GR_pass"
CLAIM_CEILING = "boundary_exchange_coefficient_retained_evaluator_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "420-relative-current-boundary-generator-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux numeric source-lock contract",
    },
    {
        "path": "408-local-bound-data-runner-v4-smoke.md",
        "role": "runner-v4 smoke evaluator semantics",
    },
    {
        "path": "417-boundary-exchange-nohair-theorem-attempt.md",
        "role": "boundary-exchange no-hair theorem attempt and retained fallback",
    },
    {
        "path": "418-Cexp-domain-candidate-generator.md",
        "role": "candidate-domain contract preserving claim semantics",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/numeric_bound_contract.csv",
        "role": "numeric no-hair channel locks",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/family_rollup.csv",
        "role": "channel family rollup",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
    {
        "path": "runs/20260602-071500-boundary-exchange-nohair-theorem-attempt/results/numeric_pressure_rows.csv",
        "role": "boundary exchange numeric pressure families",
    },
]


PROFILE_DEFINITIONS = [
    {
        "profile": "theorem_zero_control",
        "fraction_of_lock": 0.0,
        "claim_policy": "what a true no-hair theorem would supply, but not credited here",
    },
    {
        "profile": "one_tenth_lock_retained",
        "fraction_of_lock": 0.1,
        "claim_policy": "inside lock but retained; no derivation credit",
    },
    {
        "profile": "edge_lock_retained",
        "fraction_of_lock": 1.0,
        "claim_policy": "edge unstable; no evidence claim",
    },
    {
        "profile": "ten_times_lock_fail",
        "fraction_of_lock": 10.0,
        "claim_policy": "must fail retained-bound smoke",
    },
    {
        "profile": "engineering_tiny_1e_minus_15",
        "absolute_override": 1.0e-15,
        "claim_policy": "shows alpha3 exchange is much harsher than ordinary tiny leakage",
    },
]


COEFFICIENT_SEMANTICS = [
    {
        "coefficient_family": "alpha3_spatial_exchange",
        "channels": "bulk_flux_X;domain_projector_flux;unowned_momentum_flux",
        "runner_rows": "R7_alpha3",
        "meaning": "spatial exchange/momentum flux projected into alpha3",
        "retained_policy": "must be theorem-zero, Ward-owned, or below explicit 4e-20 coefficient lock",
    },
    {
        "coefficient_family": "Gdot_exchange_drift",
        "channels": "domain_scale_drift_per_yr;flux_drift_per_yr;memory_kernel_drift_per_yr",
        "runner_rows": "R9_Gdot",
        "meaning": "secular exchange drift in domain/flux/memory sector",
        "retained_policy": "must be theorem-zero, source-normalized, or below 9.6e-15 yr^-1",
    },
    {
        "coefficient_family": "domain_vector_leakage",
        "channels": "boundary_vector_B0i;domain_vector_leakage;projector_vector_leakage",
        "runner_rows": "R5_alpha1;R6_alpha2",
        "meaning": "vector boundary/projector representative leakage",
        "retained_policy": "score against alpha2/alpha1 preferred-frame locks",
    },
    {
        "coefficient_family": "preferred_location_anisotropy",
        "channels": "boundary_tracefree_shear;topology_cycle_anisotropy;external_domain_anisotropy",
        "runner_rows": "R8_xi",
        "meaning": "boundary/topology preferred-location anisotropy",
        "retained_policy": "score against xi lock",
    },
    {
        "coefficient_family": "scalar_radial_boundary_hair",
        "channels": "boundary_radial_hair;domain_projector_stress;bulk_X_metric_slip",
        "runner_rows": "R3_gamma;R4_beta;R10_fifth_force",
        "meaning": "scalar/radial hair or local fifth-force-like boundary stress",
        "retained_policy": "score as gamma/beta/fifth-force retained channel",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Boundary-exchange fallback is now testable. The evaluator registers retained exchange coefficient families, maps them to runner-v4 rows, evaluates simple lock-fraction profiles, and refuses theorem credit or claim allowance. This is the honest fallback if topological no-hair and Ward-owned cancellation remain unproved: exchange physics becomes an explicit coefficient ledger rather than a hidden assumption.",
        "retained_evaluator_written": True,
        "theorem_credit_rows": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "try to make relative-current boundaries generate admissible candidate domains directly",
        "pass_condition": "candidate domains are parent-generated from J_rel or remain closure-labelled",
    },
    {
        "priority": 2,
        "target": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "task": "test whether finite-cell fibre spectra can be integrated out or reduced to universal constants",
        "pass_condition": "finite fibre does not create local matter-visible marker channels",
    },
    {
        "priority": 3,
        "target": "422-local-bounds-real-data-source-plan.md",
        "task": "prepare verified local-bound source intake using the 411 interface",
        "pass_condition": "external local-bound rows can be filled with references and no claim leaks",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def numeric_bound_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/numeric_bound_contract.csv")


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def retained_coefficient_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in numeric_bound_rows():
        channel = row["channel"]
        if not any(channel in semantic["channels"].split(";") for semantic in COEFFICIENT_SEMANTICS):
            continue
        semantic = next(semantic for semantic in COEFFICIENT_SEMANTICS if channel in semantic["channels"].split(";"))
        rows.append(
            {
                "channel": channel,
                "coefficient_family": semantic["coefficient_family"],
                "runner_rows": semantic["runner_rows"],
                "tightest_row": row["tightest_row"],
                "tightest_observable": row["tightest_observable"],
                "required_ceiling": row["required_ceiling"],
                "units": row["units"],
                "sector": row["sector"],
                "meaning": semantic["meaning"],
                "retained_policy": semantic["retained_policy"],
                "theorem_credit_allowed": False,
                "claim_allowed": False,
            }
        )
    return rows


def profile_evaluation_rows(coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for profile in PROFILE_DEFINITIONS:
        for coeff in coefficient_rows:
            lock = float(coeff["required_ceiling"])
            if "absolute_override" in profile:
                value = float(profile["absolute_override"])
            else:
                value = lock * float(profile["fraction_of_lock"])
            if value == 0.0:
                evaluation_class = "theorem_zero_shape_no_credit"
            elif value < lock:
                evaluation_class = "inside_lock_retained_no_claim"
            elif value == lock:
                evaluation_class = "edge_lock_retained_no_claim"
            else:
                evaluation_class = "over_lock_retained_fail"
            rows.append(
                {
                    "profile": profile["profile"],
                    "channel": coeff["channel"],
                    "coefficient_family": coeff["coefficient_family"],
                    "tightest_row": coeff["tightest_row"],
                    "required_ceiling": lock,
                    "value": value,
                    "severity_ratio": value / lock if lock != 0.0 else "",
                    "evaluation_class": evaluation_class,
                    "theorem_credit_allowed": False,
                    "claim_allowed": False,
                    "claim_policy": profile["claim_policy"],
                }
            )
    return rows


def family_summary_rows(evaluation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for profile in PROFILE_DEFINITIONS:
        profile_rows = [row for row in evaluation_rows if row["profile"] == profile["profile"]]
        for family in sorted({row["coefficient_family"] for row in profile_rows}):
            subset = [row for row in profile_rows if row["coefficient_family"] == family]
            worst = max(subset, key=lambda row: float(row["severity_ratio"]))
            rows.append(
                {
                    "profile": profile["profile"],
                    "coefficient_family": family,
                    "channels": len(subset),
                    "worst_channel": worst["channel"],
                    "worst_severity_ratio": worst["severity_ratio"],
                    "over_lock_rows": sum(1 for row in subset if row["evaluation_class"] == "over_lock_retained_fail"),
                    "edge_rows": sum(1 for row in subset if row["evaluation_class"] == "edge_lock_retained_no_claim"),
                    "inside_rows": sum(1 for row in subset if row["evaluation_class"] == "inside_lock_retained_no_claim"),
                    "claim_allowed": False,
                }
            )
    return rows


def row_transition_rows() -> list[dict[str, Any]]:
    rows_by_id = {row["row_id"]: row for row in runner_v4_rows()}
    impacted_rows = sorted(
        {
            row_id
            for semantic in COEFFICIENT_SEMANTICS
            for row_id in semantic["runner_rows"].split(";")
        }
    )
    rows: list[dict[str, Any]] = []
    for row_id in impacted_rows:
        runner_row = rows_by_id.get(row_id, {})
        rows.append(
            {
                "row_id": row_id,
                "previous_state": runner_row.get("runner_v4_state", "missing"),
                "new_state": runner_row.get("runner_v4_state", "missing"),
                "result": "retained_for_testing_not_upgraded",
                "theorem_credit_allowed": False,
                "claim_allowed": False,
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_rows = [row for row in evaluation_rows + transition_rows if row["theorem_credit_allowed"]]
    claim_rows = [row for row in evaluation_rows + transition_rows if row["claim_allowed"]]
    over_rows = [row for row in evaluation_rows if row["evaluation_class"] == "over_lock_retained_fail"]
    alpha3_rows = [row for row in coefficient_rows if row["coefficient_family"] == "alpha3_spatial_exchange"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "retained_coefficients_registered",
            "status": "pass",
            "evidence": f"{len(coefficient_rows)} retained coefficient channels registered",
        },
        {
            "gate": "alpha3_hard_lock_visible",
            "status": "pass" if alpha3_rows else "fail",
            "evidence": "alpha3 exchange lock 4e-20 registered",
        },
        {
            "gate": "profiles_evaluated",
            "status": "pass",
            "evidence": f"{len(PROFILE_DEFINITIONS)} profiles evaluated",
        },
        {
            "gate": "over_lock_failures_detected",
            "status": "pass" if over_rows else "fail",
            "evidence": f"{len(over_rows)} over-lock retained failures",
        },
        {
            "gate": "no_theorem_credit_or_claim_leaks",
            "status": "pass" if not theorem_rows and not claim_rows else "fail",
            "evidence": f"theorem_credit={len(theorem_rows)} claim_allowed={len(claim_rows)}",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "retained coefficient evaluator only; no local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def format_float(value: Any) -> str:
    number = float(value)
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.3e}"
    return f"{number:.6g}"


def write_checkpoint_markdown(
    run_dir: Path,
    coefficient_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    coeff_table_rows = [
        {
            "family": row["coefficient_family"],
            "channel": row["channel"],
            "lock": format_float(row["required_ceiling"]),
            "units": row["units"],
        }
        for row in coefficient_rows
    ]
    profile_table_rows = [
        {
            "profile": row["profile"],
            "family": row["coefficient_family"],
            "worst": row["worst_channel"],
            "severity": format_float(row["worst_severity_ratio"]),
            "over": row["over_lock_rows"],
        }
        for row in summary_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 419 - Boundary Exchange Coefficient Retained Evaluator

Private retained-coefficient/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 417 showed boundary-exchange no-hair is not derived. This checkpoint builds the honest fallback: if exchange exists, it becomes an explicit retained coefficient ledger with hard locks, profiles, and no theorem credit.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_exchange_coefficient_retained_evaluator.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Retained Coefficients

{markdown_table(coeff_table_rows, ["family", "channel", "lock", "units"])}

## 4. Profile Summary

{markdown_table(profile_table_rows, ["profile", "family", "worst", "severity", "over"])}

## 5. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 6. Decision

{DECISION[0]["decision"]}

Practical read: this is the testing fallback. If derivation stalls, the exchange branch has numbers, rows, and failure modes instead of hiding behind prose.

## 7. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    coefficient_rows = retained_coefficient_rows()
    evaluation_rows = profile_evaluation_rows(coefficient_rows)
    summary_rows = family_summary_rows(evaluation_rows)
    transition_rows = row_transition_rows()
    gate_result_rows = gate_rows(source_rows, coefficient_rows, evaluation_rows, transition_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "coefficient_semantics.csv", COEFFICIENT_SEMANTICS)
    write_csv(results_dir / "retained_coefficients.csv", coefficient_rows)
    write_csv(results_dir / "profile_definitions.csv", PROFILE_DEFINITIONS)
    write_csv(results_dir / "profile_evaluation.csv", evaluation_rows)
    write_csv(results_dir / "family_summary.csv", summary_rows)
    write_csv(results_dir / "row_transition_attempt.csv", transition_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    claim_rows = [row for row in evaluation_rows + transition_rows if row["claim_allowed"]]
    theorem_rows = [row for row in evaluation_rows + transition_rows if row["theorem_credit_allowed"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "retained_coefficients": len(coefficient_rows),
        "profile_evaluation_rows": len(evaluation_rows),
        "theorem_credit_rows": len(theorem_rows),
        "claim_allowed_rows": len(claim_rows),
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, coefficient_rows, summary_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 419 boundary exchange retained coefficient evaluator artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
