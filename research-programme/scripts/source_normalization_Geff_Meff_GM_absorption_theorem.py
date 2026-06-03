from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-normalization-Geff-Meff-GM-absorption-theorem"
STATUS = "Meff_flux_conservation_imported_GM_absorption_not_parent_derived_deltaG_Gdot_rows_remain_active"
CLAIM_CEILING = "source_normalization_GM_absorption_contract_only_no_deltaG_Gdot_PPN_EH_WEP_or_local_GR_pass"
NEXT_TARGET = "379-class-only-boundary-action-noangular-theorem.md"


SOURCE_DOCS = [
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "old N1_Meff conditional flux theorem: closed Pi_M flux gives radially conserved M_eff but calibration remains open",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH weak-field map: Newtonian Poisson limit needs G_eff/kappa/M_eff normalization",
    },
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "Gdot/G contingent guardrail and fifth-force/source-normalization policy",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "source-normalization operator family maps to delta_G, Gdot/G, and Newtonian limit",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "GM absorption tests and force-law contract requiring source normalization",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-force channels and source normalization open for fifth-force/delta_G rows",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward identity and boundary/projector/domain force ownership context",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "universal matter/coframe closure needed for safe GM absorption without WEP leakage",
    },
]


SOURCE_NORMALIZATION_OBJECTS = [
    {
        "object": "kappa_parent",
        "definition_needed": "coefficient multiplying the metric equation in the local EH/metric branch",
        "safe_absorption_role": "sets conversion between stress/source and curvature",
        "current_status": "not_parent_calibrated",
    },
    {
        "object": "G_eff",
        "definition_needed": "Newtonian coupling inferred from local weak-field Poisson limit",
        "safe_absorption_role": "must be constant and universal through the experiment",
        "current_status": "open",
    },
    {
        "object": "M_eff",
        "definition_needed": "conserved absolute S2 harmonic mass flux extracted by Pi_M",
        "safe_absorption_role": "may replace bare mass in measured GM if radially conserved and calibrated",
        "current_status": "conditional_flux_theorem_imported_from_244",
    },
    {
        "object": "GM_measured",
        "definition_needed": "the product actually determined by orbital/lab dynamics",
        "safe_absorption_role": "only universal constant monopole can hide here",
        "current_status": "absorption_tests_written_not_parent_proved",
    },
    {
        "object": "delta_G_residual",
        "definition_needed": "range/source/composition/time-dependent deviation from measured GM normalization",
        "safe_absorption_role": "none; must be scored or kept active",
        "current_status": "active_if_absorption_tests_fail",
    },
    {
        "object": "Gdot_over_G",
        "definition_needed": "secular drift of G_eff or M_eff normalization",
        "safe_absorption_role": "none; contingent source-locked guardrail",
        "current_status": "active_if_time_independence_not_derived",
    },
]


GM_ABSORPTION_THEOREM_ATTEMPT = [
    {
        "step": 1,
        "statement": "Preserve the absolute exterior mass class.",
        "equation": "M_eff(r) = (1/4 pi G_ref) int_{S^2_r} Pi_M J",
        "result": "ordinary mass flux is separated from relative memory exchange",
        "status": "conditional_from_244",
    },
    {
        "step": 2,
        "statement": "Require exterior closure of the mass flux.",
        "equation": "d(Pi_M J) = 0 on S^2 x [r1,r2]",
        "result": "M_eff(r2)-M_eff(r1)=0",
        "status": "conditional_from_244",
    },
    {
        "step": 3,
        "statement": "Define the Newtonian normalization product.",
        "equation": "mu_obs = G_eff M_eff",
        "result": "orbits measure mu_obs, not G_eff and M_eff separately",
        "status": "definition",
    },
    {
        "step": 4,
        "statement": "Safe absorption requires the residual to be only a universal constant monopole.",
        "equation": "delta mu/mu = constant, species-independent, range-independent, time-independent",
        "result": "absorbed into measured GM",
        "status": "conditional_absorption_rule",
    },
    {
        "step": 5,
        "statement": "If any radial, time, species, flux, or range dependence survives, absorption fails.",
        "equation": "partial_r mu != 0 or partial_t mu != 0 or Delta mu_A != 0 or alpha_Y(lambda) != 0",
        "result": "delta_G, Gdot/G, WEP, beta, or fifth-force rows remain active",
        "status": "current_risk",
    },
    {
        "step": 6,
        "statement": "The current branch has conditional M_eff conservation but not parent calibration or universal absorption.",
        "equation": "M_eff conserved != kappa/G_eff/M_eff/GM theorem",
        "result": "no delta_G/Gdot/local-GR pass",
        "status": "fail_parent_derivation",
    },
]


ABSORPTION_GATE_MATRIX = [
    {
        "gate": "absolute_mass_class_preserved",
        "required_condition": "Pi_M extracts ordinary absolute S2 mass flux without erasing mass",
        "if_passes": "ordinary mass can be represented by M_eff",
        "if_fails": "source normalization undefined",
        "current_status": "conditional_pass_from_244",
    },
    {
        "gate": "radial_flux_closed",
        "required_condition": "d(Pi_M J)=0 in compact exterior",
        "if_passes": "M_eff is radially conserved",
        "if_fails": "radial memory hair / fifth force",
        "current_status": "conditional_pass_from_244_not_parent_owned",
    },
    {
        "gate": "absolute_calibration_fixed",
        "required_condition": "parent action fixes the coefficient converting Pi_M J into physical mass units",
        "if_passes": "M_eff has physical normalization",
        "if_fails": "fitted source normalization closure",
        "current_status": "fail_open",
    },
    {
        "gate": "G_eff_constant",
        "required_condition": "G_eff does not depend on radius, time, source, species, or environment in local tests",
        "if_passes": "mu_obs can be constant",
        "if_fails": "delta_G or Gdot/G active",
        "current_status": "not_derived",
    },
    {
        "gate": "universality",
        "required_condition": "same GM normalization for all matter/clocks/compositions",
        "if_passes": "no WEP leakage from source normalization",
        "if_fails": "eta_WEP/composition fifth force active",
        "current_status": "closure_axiom_required",
    },
    {
        "gate": "Ward_owned_monopole",
        "required_condition": "boundary/projector/domain flux associated with M_eff is conserved in total Ward ledger",
        "if_passes": "no fake conservation",
        "if_fails": "alpha3, beta, Gdot, or secular drift active",
        "current_status": "mapped_not_proved",
    },
    {
        "gate": "no_range_dependence",
        "required_condition": "surviving monopole is not a finite-range Yukawa/spectral/domain-wall force",
        "if_passes": "GM absorption possible",
        "if_fails": "fifth-force alpha_Y(lambda) scoring required",
        "current_status": "range_law_missing",
    },
]


RESIDUAL_IMPACT_MAP = [
    {
        "failure": "dM_eff_dr_nonzero",
        "observable_rows": "delta_G_or_fifth_force_yukawa;beta_minus_1",
        "meaning": "radial source hair masquerades as changing enclosed mass",
        "runner_status": "active_unscored_until_range/coupling_or_nohair",
    },
    {
        "failure": "dG_eff_dt_or_dM_eff_dt_nonzero",
        "observable_rows": "Gdot_over_G;secular_orbital_drift",
        "meaning": "source normalization drifts over time",
        "runner_status": "contingent_budget_only",
    },
    {
        "failure": "species_dependent_GM",
        "observable_rows": "eta_WEP;composition_dependent_fifth_force",
        "meaning": "different test bodies see different source normalization",
        "runner_status": "WEP_closure_active",
    },
    {
        "failure": "unowned_boundary_flux",
        "observable_rows": "alpha3;Gdot_over_G;beta_minus_1",
        "meaning": "momentum/energy bookkeeping is not Ward-owned",
        "runner_status": "contingent_budget_only",
    },
    {
        "failure": "constant_universal_monopole_only",
        "observable_rows": "absorbed_into_measured_GM",
        "meaning": "safe case if all absorption gates pass",
        "runner_status": "conditional_not_parent_derived",
    },
]


SOURCE_NORMALIZATION_CONTRACT = [
    {
        "contract_item": "define_reference_G",
        "required_form": "choose or derive G_ref used in M_eff = (4 pi G_ref)^-1 int Pi_M J",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "derive_kappa_to_Geff",
        "required_form": "kappa = 8 pi G_eff/c^4 in the local EH/metric branch, with units fixed",
        "current_status": "conditional_EH_branch_only",
    },
    {
        "contract_item": "prove_Meff_conserved",
        "required_form": "d(Pi_M J)=0 and no radial memory hair in compact exterior",
        "current_status": "conditional_from_244_not_global",
    },
    {
        "contract_item": "prove_GM_absorption",
        "required_form": "G_eff M_eff differs from measured GM only by a constant universal calibration",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "retain_failed_absorption_rows",
        "required_form": "if absorption tests fail, keep delta_G/Gdot/WEP/beta/fifth-force rows active",
        "current_status": "enforced",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "delta_G_or_fifth_force_yukawa",
        "before_378": "parameterized_unscored_requires_alphaY_lambdaY_or_GM_absorption",
        "after_378": "GM_absorption_requires_parent_source_normalization; still active",
        "claim_status": "unscored_or_active_no_pass",
    },
    {
        "runner_row": "Gdot_over_G",
        "before_378": "contingent source-locked row",
        "after_378": "activated if G_eff or M_eff time independence is not derived",
        "claim_status": "contingent_budget_only",
    },
    {
        "runner_row": "beta_minus_1",
        "before_378": "ready budget only; radial/nonlinear source hair open",
        "after_378": "radial memory hair still feeds beta unless no-hair/source theorem closes it",
        "claim_status": "budget_only_no_pass",
    },
    {
        "runner_row": "eta_WEP",
        "before_378": "WEP closure active",
        "after_378": "species-dependent source normalization explicitly linked to eta_WEP",
        "claim_status": "budget_only_no_pass",
    },
    {
        "runner_row": "Newtonian_limit",
        "before_378": "conditional EH/source normalization target",
        "after_378": "requires kappa/G_eff/M_eff/GM theorem",
        "claim_status": "not_promoted",
    },
]


FAILURE_MODES = [
    {
        "failure": "M_eff_conservation_mistaken_for_GM_absorption",
        "meaning": "radially conserved mass flux is treated as calibrated measured GM",
        "consequence": "delta_G/source-normalization closure hidden",
    },
    {
        "failure": "G_eff_drift_ignored",
        "meaning": "time dependence of G_eff or M_eff is not mapped to Gdot/G",
        "consequence": "secular local bounds bypassed",
    },
    {
        "failure": "species_dependent_source_normalization_hidden",
        "meaning": "different compositions see different effective GM",
        "consequence": "WEP violation disguised as source calibration",
    },
    {
        "failure": "radial_hair_absorbed_into_mass",
        "meaning": "r-dependent source profile is called measured mass",
        "consequence": "fifth force/beta residual erased incorrectly",
    },
    {
        "failure": "Ward_flux_not_owned",
        "meaning": "M_eff is declared conserved without total stress/flux identity",
        "consequence": "fake Bianchi closure and alpha3/Gdot risk",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Checkpoint 244 gives a useful conditional M_eff flux-conservation theorem, but GM absorption needs more: absolute calibration, constant universal G_eff, universal coupling, Ward-owned flux, no range/time/species dependence. Those are not parent-derived, so delta_G/Gdot/WEP/beta/fifth-force source-normalization rows remain active.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt the class-only boundary action theorem that would kill B_0i, trace-free angular shear, and radial/vector boundary hair",
        "pass_condition": "boundary vector/shear/radial sources are theorem-zero or retained as coefficients",
    },
    {
        "priority": 2,
        "target": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "task": "derive or reject a massive/source-free bulk-X equation with m_X and q_X sufficient to define alpha_X(lambda_X)",
        "pass_condition": "bulk scalar force is theorem-zero, Yukawa-scored, or explicitly retained unscored",
    },
    {
        "priority": 3,
        "target": "381-local-GR-debt-ledger-rollup-after-360-378.md",
        "task": "roll up all local-GR debts after WEP/EH/preferred-frame/fifth-force/source-normalization gates",
        "pass_condition": "ready rows, conditional theorem rows, and active failure rows are separated",
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
            "gate": "Meff_flux_theorem_imported",
            "status": "conditional_pass",
            "evidence": "checkpoint 244 closed Pi_M flux gives radially conserved M_eff if parent conditions hold",
        },
        {
            "gate": "GM_absorption_tests_written",
            "status": "pass",
            "evidence": "absolute class, radial closure, calibration, G_eff constancy, universality, Ward ownership, and no-range gates recorded",
        },
        {
            "gate": "absolute_calibration_parent_derived",
            "status": "fail",
            "evidence": "coefficient converting Pi_M flux to physical mass units remains open",
        },
        {
            "gate": "G_eff_constancy_parent_derived",
            "status": "fail",
            "evidence": "no theorem fixes radius/time/source/species/environment independence",
        },
        {
            "gate": "measured_GM_absorption_parent_derived",
            "status": "fail",
            "evidence": "constant universal calibration relation G_eff M_eff = GM_measured is not parent-derived",
        },
        {
            "gate": "deltaG_Gdot_rows_retained",
            "status": "pass",
            "evidence": "delta_G/fifth-force and Gdot/G remain active or contingent when absorption gates fail",
        },
        {
            "gate": "local_GR_or_PPN_pass_claimed",
            "status": "fail",
            "evidence": "source-normalization contract only",
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
    write_csv(results_dir / "source_normalization_objects.csv", SOURCE_NORMALIZATION_OBJECTS)
    write_csv(results_dir / "GM_absorption_theorem_attempt.csv", GM_ABSORPTION_THEOREM_ATTEMPT)
    write_csv(results_dir / "absorption_gate_matrix.csv", ABSORPTION_GATE_MATRIX)
    write_csv(results_dir / "residual_impact_map.csv", RESIDUAL_IMPACT_MAP)
    write_csv(results_dir / "source_normalization_contract.csv", SOURCE_NORMALIZATION_CONTRACT)
    write_csv(results_dir / "runner_update.csv", RUNNER_UPDATE)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
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
        "Meff_flux_theorem_imported": True,
        "measured_GM_absorption_parent_derived": False,
        "deltaG_Gdot_rows_retained": True,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 378 source-normalization G_eff/M_eff/GM absorption artifacts."
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
