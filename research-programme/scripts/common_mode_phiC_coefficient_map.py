from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "common-mode-phiC-coefficient-map"
STATUS = "phiC_weak_field_coefficient_map_written_common_mode_bounds_require_zero_theorem_or_tiny_gradient_no_pass"
CLAIM_CEILING = "coefficient_map_and_budget_only_no_clock_PPN_WEP_fifth_force_EH_or_local_GR_pass"
NEXT_TARGET = "371-WEP-species-universality-or-active-eta-runner.md"


SOURCE_DOCS = [
    {
        "path": "369-source-locked-closure-branch-local-bound-runner.md",
        "role": "source-locked closure branch local-bound runner and budget rows",
    },
    {
        "path": "368-common-mode-class-metric-clock-PPN-residual-gate.md",
        "role": "class-metric residual model and phi_C pressure ratio",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative-invariant matter action and exponential class metric target",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "universal matter coupling and species-vertex pressure",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "source-locked residual pressure ranking",
    },
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "external source locks for gamma, beta, WEP, and redshift targets",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH exterior operator remains separate and underived",
    },
    {
        "path": "runs/20260601-221000-source-locked-closure-branch-local-bound-runner/results/ready_budget_rows.csv",
        "role": "machine-readable closure branch budget rows",
    },
]


WEAK_FIELD_MAP = [
    {
        "map_item": "class_metric",
        "formula": "ghat_mn = exp(phi_C) g_mn",
        "coefficient_readout": "phi_C is a common conformal/class-metric scalar",
        "status": "labelled_closure_branch",
    },
    {
        "map_item": "time_potential_shift",
        "formula": "for g00=-1+2U+..., ghat00 gives U_time ~= U - phi_C/2",
        "coefficient_readout": "clock/redshift sees Delta phi_C with coefficient magnitude about 1/2",
        "status": "weak_field_bookkeeping",
    },
    {
        "map_item": "space_potential_shift",
        "formula": "for gij=(1+2U)deltaij, ghatij gives U_space ~= U + phi_C/2",
        "coefficient_readout": "spatial curvature response differs from time response by order phi_C",
        "status": "weak_field_bookkeeping",
    },
    {
        "map_item": "gamma_proxy",
        "formula": "gamma_eff - 1 ~= phi_C/U_GR or r_grad for local-gradient scoring",
        "coefficient_readout": "unit-magnitude proxy coefficient; sign convention not used for budgets",
        "status": "budget_proxy_not_PPN_derivation",
    },
    {
        "map_item": "fifth_force_proxy",
        "formula": "a_extra/a_GR ~= (1/2)|grad phi_C|/|grad U_GR|",
        "coefficient_readout": "half-gradient proxy if class scalar acts as extra potential",
        "status": "quarantined_until_source_lock",
    },
    {
        "map_item": "beta_second_order",
        "formula": "if phi_C = s1 U + s2 U^2 + ..., beta depends on s1,s2 and residual EH operator",
        "coefficient_readout": "no reliable beta coefficient without second-order field equation",
        "status": "coefficient_missing",
    },
]


COEFFICIENT_BUDGETS = [
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale": 3.1e-5,
        "coefficient_symbol": "c_clock",
        "proxy_coefficient_abs": 0.5,
        "phi_quantity": "|Delta phi_C / Delta U_GR|",
        "required_phi_bound_if_proxy": 6.2e-5,
        "status": "budget_only_no_pass",
    },
    {
        "residual": "gamma_minus_1",
        "source_locked_scale": 2.3e-5,
        "coefficient_symbol": "c_gamma",
        "proxy_coefficient_abs": 1.0,
        "phi_quantity": "r_grad = |grad phi_C|/|grad U_GR| or |phi_C/U_GR|",
        "required_phi_bound_if_proxy": 2.3e-5,
        "status": "budget_only_no_pass",
    },
    {
        "residual": "beta_minus_1",
        "source_locked_scale": 7.8e-5,
        "coefficient_symbol": "c_beta1,c_beta2,c_EH_beta",
        "proxy_coefficient_abs": "",
        "phi_quantity": "s1,s2 in phi_C=s1 U+s2 U^2 plus residual EH operator",
        "required_phi_bound_if_proxy": "",
        "status": "coefficient_missing_second_order_open",
    },
    {
        "residual": "eta_WEP",
        "source_locked_scale": 2.8e-15,
        "coefficient_symbol": "c_WEP_species",
        "proxy_coefficient_abs": 1.0,
        "phi_quantity": "|Delta F_AB(C_D)| or species-specific class response",
        "required_phi_bound_if_proxy": 2.8e-15,
        "status": "species_universality_gate_not_common_mode",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "source_locked_scale": "",
        "coefficient_symbol": "c_5",
        "proxy_coefficient_abs": 0.5,
        "phi_quantity": "r_grad = |grad phi_C|/|grad U_GR|",
        "required_phi_bound_if_proxy": "",
        "status": "quarantined_no_numeric_score",
    },
]


ZERO_THEOREM_REQUIREMENTS = [
    {
        "route": "strict_local_class_silence",
        "condition": "phi_C = constant on stationary local/exterior domains, so grad phi_C=0 and Delta phi_C=0",
        "kills": "clock common-mode, gamma proxy, fifth-force proxy from class metric",
        "status": "best_zero_theorem_target_not_derived",
    },
    {
        "route": "universal_species_function",
        "condition": "all matter sectors share the same F(C_D), with no F_A species dependence",
        "kills": "direct WEP class-metric species residual",
        "status": "open_hardest_ready_gate",
    },
    {
        "route": "EH_operator_recovery",
        "condition": "after class-metric selection, exterior dynamics reduce to metric-only EH operator",
        "kills": "residual_EH_operator terms feeding gamma/beta/slip",
        "status": "not_derived",
    },
    {
        "route": "measured_GM_absorption",
        "condition": "a purely universal monopole phi_C contribution is conserved and absorbed into measured GM",
        "kills": "some delta_G-like monopole pressure only",
        "status": "partial_not_enough_for_clock_gamma",
    },
    {
        "route": "source_locked_fifth_force_manifest",
        "condition": "fifth-force/delta_G target scale and branch coefficient are source-locked",
        "kills": "fake quarantine ambiguity",
        "status": "not_done",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "alpha_clock_redshift",
        "update": "replace generic missing coeff_clock with c_clock~1/2 proxy plus required |Delta phi_C/Delta U| <= 6.2e-5 if proxy applies",
        "claim_status": "budget_only",
    },
    {
        "runner_row": "gamma_minus_1",
        "update": "replace generic coeff_gamma_r_grad with unit proxy and required r_grad <= 2.3e-5 if no zero theorem",
        "claim_status": "budget_only",
    },
    {
        "runner_row": "beta_minus_1",
        "update": "keep beta coefficient missing until phi_C second-order expansion and EH residual operator are derived",
        "claim_status": "blocked",
    },
    {
        "runner_row": "eta_WEP",
        "update": "not solved by common-mode phi_C; requires species universality theorem at <=2.8e-15 pressure",
        "claim_status": "hardest_ready_gate",
    },
    {
        "runner_row": "delta_G_or_fifth_force",
        "update": "half-gradient proxy identified, but row remains quarantined until source lock",
        "claim_status": "quarantined",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The common-mode phi_C weak-field map gives proxy coefficients for clock, gamma, and fifth-force pressure, but it demands either local phi_C zero theorems or tiny gradients; beta, WEP universality, fifth-force source locks, and EH recovery remain open.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "prove universal F(C_D) across matter sectors or keep eta_WEP as the active hardest ready gate",
        "pass_condition": "species-specific class responses are forbidden or eta_WEP remains budgeted",
    },
    {
        "priority": 2,
        "target": "372-local-phiC-zero-theorem-or-gradient-bound.md",
        "task": "derive strict local class silence grad(phi_C)=0 or bound r_grad against clock/gamma budgets",
        "pass_condition": "r_grad is theorem-zero, source-bounded, or marked failed",
    },
    {
        "priority": 3,
        "target": "373-fifth-force-preferred-frame-source-lock-manifest.md",
        "task": "source-lock quarantined fifth-force/preferred-frame/xi sectors before numeric scoring",
        "pass_condition": "quarantined rows become ready targets or remain explicitly unscored",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "weak_field_phiC_map_written",
            "status": "pass",
            "evidence": "time/spatial potential shifts and proxy gamma/clock/fifth-force coefficients recorded",
        },
        {
            "gate": "clock_phiC_budget_written",
            "status": "pass",
            "evidence": "proxy bound |Delta phi_C/Delta U| <= 6.2e-5 recorded",
        },
        {
            "gate": "gamma_phiC_budget_written",
            "status": "pass",
            "evidence": "proxy bound r_grad <= 2.3e-5 recorded",
        },
        {
            "gate": "beta_coefficient_derived",
            "status": "fail",
            "evidence": "second-order phi_C map and EH residual operator remain open",
        },
        {
            "gate": "WEP_species_universality_derived",
            "status": "fail",
            "evidence": "common-mode phi_C does not forbid species-specific F_A(C_D)",
        },
        {
            "gate": "fifth_force_numeric_scored",
            "status": "fail",
            "evidence": "fifth-force source lock still missing",
        },
        {
            "gate": "local_bound_or_local_GR_pass_claim",
            "status": "fail",
            "evidence": "coefficient map is budget-only and no zero theorem is derived",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "weak_field_map.csv", WEAK_FIELD_MAP)
    write_csv(results_dir / "coefficient_budgets.csv", COEFFICIENT_BUDGETS)
    write_csv(results_dir / "zero_theorem_requirements.csv", ZERO_THEOREM_REQUIREMENTS)
    write_csv(results_dir / "runner_update.csv", RUNNER_UPDATE)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 370 common-mode phi_C coefficient map artifacts."
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
