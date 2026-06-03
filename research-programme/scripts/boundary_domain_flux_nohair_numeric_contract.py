from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-domain-flux-nohair-numeric-contract"
CHECKPOINT_DOC = "403-boundary-domain-flux-nohair-numeric-contract.md"
STATUS = "boundary_domain_flux_nohair_numeric_contract_written_alpha3_flux_hardest_rows_explicit_conditional_exits_not_parent_derived_no_PPN_or_local_GR_pass"
CLAIM_CEILING = "boundary_domain_flux_nohair_numeric_contract_only_no_boundary_bulk_domain_flux_PPN_fifth_force_source_or_local_GR_pass"
NEXT_TARGET = "404-selector-blind-matter-axiom-origin.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "total Ward force ledger with boundary/domain/projector/bulk forces",
    },
    {
        "path": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "role": "joint q_BX boundary/bulk force-flux contract",
    },
    {
        "path": "395-preferred-frame-domain-nohair-under-identity-closure.md",
        "role": "domain/projector/preferred-frame coefficient map and no-hair contract",
    },
    {
        "path": "400-runner-v3-numeric-smoke-extension.md",
        "role": "numeric smoke channel bounds and hardest local blockers",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source pair and source-normalization exits",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv",
        "role": "tightest channel bounds from checkpoint 400",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/channel_map.csv",
        "role": "channel-to-observable map from checkpoint 400",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/profile_summary.csv",
        "role": "numeric profile failures from checkpoint 400",
    },
]


CONTRACT_CHANNELS = [
    "bulk_flux_X",
    "domain_projector_flux",
    "unowned_momentum_flux",
    "boundary_species_charge",
    "bulk_X_composition_charge",
    "source_charge_species_split",
    "source_normalization_species_split",
    "domain_scale_drift_per_yr",
    "flux_drift_per_yr",
    "geff_meff_drift_per_yr",
    "memory_kernel_drift_per_yr",
    "boundary_vector_B0i",
    "domain_anisotropy",
    "domain_vector_leakage",
    "projector_vector_leakage",
    "boundary_tracefree_shear",
    "topology_cycle_anisotropy",
    "external_domain_anisotropy",
    "boundary_radial_hair",
    "bulk_X_metric_slip",
    "domain_projector_stress",
]


CHANNEL_EXIT_RULES = {
    "bulk_flux_X": "derive bulk-X flux absent, cancelled in total Ward identity, or retained with alpha3/Gdot budget",
    "domain_projector_flux": "derive domain/projector flux is gauge/topological/Ward-owned, or retain alpha3/Gdot budget",
    "unowned_momentum_flux": "derive total spatial Ward flux owner n_mu B^{mu i}+F_X^i+F_D^i+F_P^i+F_source^i=0",
    "boundary_species_charge": "forbid species-dependent boundary/class charge in parent source sector",
    "bulk_X_composition_charge": "derive q_X/m universal or zero; otherwise WEP-source/fifth-force row remains",
    "source_charge_species_split": "derive species-blind source charge and constants",
    "source_normalization_species_split": "derive source-normalized measured GM independent of species/composition",
    "domain_scale_drift_per_yr": "derive domain scale is nondynamical/topological or its drift is Ward-owned",
    "flux_drift_per_yr": "derive no secular unowned flux drift",
    "geff_meff_drift_per_yr": "derive partial_t ln(G_eff M_eff)=0",
    "memory_kernel_drift_per_yr": "derive memory kernel is locally stationary or source-budgeted",
    "boundary_vector_B0i": "derive boundary action is class-only/scalar/topological with no vector representative",
    "domain_anisotropy": "derive domain selector is scalar/topological or anisotropy is gauge",
    "domain_vector_leakage": "derive no physical domain vector/normal leakage",
    "projector_vector_leakage": "derive projector representative is gauge/metric-independent or stress retained",
    "boundary_tracefree_shear": "derive no trace-free angular boundary hair",
    "topology_cycle_anisotropy": "derive H1/H2/cycle data are absent, topological constants, or explicitly retained",
    "external_domain_anisotropy": "derive no external-domain preferred-location anisotropy",
    "boundary_radial_hair": "derive only constant universal monopole survives or score alpha_B(lambda_B)",
    "bulk_X_metric_slip": "derive source-free massive X no-hair or score alpha_X(lambda_X)",
    "domain_projector_stress": "derive projector/domain stress is varied, owned, or retained in metric equations",
}


NOHAIR_MECHANISM_TESTS = [
    {
        "mechanism": "total Ward-owned spatial flux",
        "required_equation": "P_loc[n_mu B^{mu i}+F_X^i+F_domain^i+F_projector^i+F_source^i]=0",
        "pays_channels": "bulk_flux_X;domain_projector_flux;unowned_momentum_flux;flux_drift_per_yr",
        "current_status": "mapped_not_parent_derived",
        "verdict": "fail_open",
    },
    {
        "mechanism": "class-only scalar/topological boundary action",
        "required_equation": "S_boundary=S_boundary(Q_rel,M_eff,V_scalar,I_top) and delta S/delta B_TF=delta S/delta B_0i=0",
        "pays_channels": "boundary_vector_B0i;boundary_tracefree_shear",
        "current_status": "conditional_not_parent_derived",
        "verdict": "conditional_only",
    },
    {
        "mechanism": "no radial boundary hair except constant monopole",
        "required_equation": "partial_r mu_B=0 or mu_B=constant universal source-normalized monopole",
        "pays_channels": "boundary_radial_hair",
        "current_status": "coupled_to_source_normalization_not_derived",
        "verdict": "fail_open",
    },
    {
        "mechanism": "positive source-free bulk-X mass gap",
        "required_equation": "(-Delta+m_X^2)X=0, m_X^2>0, regular decaying data -> X=0",
        "pays_channels": "bulk_X_metric_slip",
        "current_status": "conditional_source_free_only",
        "verdict": "conditional_only",
    },
    {
        "mechanism": "sourced bulk-X force law",
        "required_equation": "(-Delta+m_X^2)X=q_X rho -> alpha_X(lambda_X), source/test charge, screening profile",
        "pays_channels": "bulk_X_metric_slip;bulk_X_composition_charge",
        "current_status": "range_coupling_missing",
        "verdict": "fail_open",
    },
    {
        "mechanism": "domain/projector gauge-topological theorem",
        "required_equation": "domain/projector vector representatives are gauge/topological and carry no local stress or flux",
        "pays_channels": "domain_vector_leakage;projector_vector_leakage;domain_anisotropy;domain_projector_flux;domain_projector_stress",
        "current_status": "not_parent_derived",
        "verdict": "fail_open",
    },
    {
        "mechanism": "no domain/topology preferred-location anisotropy",
        "required_equation": "eps_domain_aniso=eps_external_domain_aniso=eps_H1H2_cycle=0 or retained",
        "pays_channels": "domain_anisotropy;external_domain_anisotropy;topology_cycle_anisotropy",
        "current_status": "not_parent_derived",
        "verdict": "fail_open",
    },
]


FLUX_BALANCE_EQUATIONS = [
    {
        "equation_id": "q_BX_local",
        "expression": "q_BX^nu=P_loc[n_mu B^{mu nu}+F_X^nu+F_boundary^nu]",
        "needed_for": "boundary/bulk local source closure",
        "current_status": "contract_written_not_zero_derived",
    },
    {
        "equation_id": "q_BDP_total",
        "expression": "q_BDP^i=P_loc[n_mu B^{mu i}+F_X^i+F_domain^i+F_projector^i+F_source^i]",
        "needed_for": "alpha3 and Gdot/G closure",
        "current_status": "not_parent_derived",
    },
    {
        "equation_id": "domain_vector_nohair",
        "expression": "eps_domain_vec=eps_P_vector=0 or gauge/topological",
        "needed_for": "alpha1/alpha2 preferred-frame closure",
        "current_status": "not_parent_derived",
    },
    {
        "equation_id": "anisotropy_nohair",
        "expression": "eps_domain_aniso=eps_external_domain_aniso=eps_H1H2_cycle=0 or retained",
        "needed_for": "xi and alpha2 closure",
        "current_status": "not_parent_derived",
    },
    {
        "equation_id": "secular_drift_closure",
        "expression": "partial_t ln(G_eff M_eff)+dot_K_memory+dot_F_flux+dot_L_domain=0",
        "needed_for": "Gdot/G closure",
        "current_status": "not_parent_derived",
    },
]


PROFILE_VALUES = [
    {
        "profile": "theorem_zero",
        "dimensionless_value": 0.0,
        "per_year_value": 0.0,
        "interpretation": "what a real no-hair theorem would supply",
    },
    {
        "profile": "one_tenth_tightest_bound",
        "dimensionless_value": "0.1*bound",
        "per_year_value": "0.1*bound",
        "interpretation": "inside budget only if derived as suppression",
    },
    {
        "profile": "edge_tightest_bound",
        "dimensionless_value": "1.0*bound",
        "per_year_value": "1.0*bound",
        "interpretation": "edge is not stable evidence",
    },
    {
        "profile": "tiny_floor_1e_minus_20",
        "dimensionless_value": 1.0e-20,
        "per_year_value": 1.0e-20,
        "interpretation": "tests whether absurdly tiny flux leaks still matter",
    },
    {
        "profile": "tiny_floor_1e_minus_15",
        "dimensionless_value": 1.0e-15,
        "per_year_value": 1.0e-15,
        "interpretation": "source/WEP-scale leak floor",
    },
    {
        "profile": "engineering_tiny_1e_minus_12",
        "dimensionless_value": 1.0e-12,
        "per_year_value": 1.0e-12,
        "interpretation": "tiny in ordinary terms, fatal for local hard rows",
    },
    {
        "profile": "unit_coupling",
        "dimensionless_value": 1.0,
        "per_year_value": 1.0,
        "interpretation": "raw unsuppressed retained channel",
    },
]


ROW_TRANSITION_DECISION = [
    {
        "runner_row": "R5_alpha1",
        "current_state": "budget_only",
        "attempt_result": "boundary/domain/projector vector contract written",
        "new_state": "budget_only",
        "why_not_promoted": "vector/gauge/topological no-hair is not parent-derived",
    },
    {
        "runner_row": "R6_alpha2",
        "current_state": "budget_only",
        "attempt_result": "domain anisotropy and vector leakage bounds explicit",
        "new_state": "budget_only",
        "why_not_promoted": "2e-9 alpha2-scale no-hair remains inserted, not derived",
    },
    {
        "runner_row": "R7_alpha3",
        "current_state": "contingent_budget",
        "attempt_result": "flux channels require <=4e-20 or exact Ward cancellation",
        "new_state": "contingent_budget",
        "why_not_promoted": "total Ward flux owner is mapped but not parent-derived",
    },
    {
        "runner_row": "R8_xi",
        "current_state": "budget_only",
        "attempt_result": "domain/topology/boundary anisotropy contract written",
        "new_state": "budget_only",
        "why_not_promoted": "xi-specific preferred-location/topology no-hair remains open",
    },
    {
        "runner_row": "R9_Gdot",
        "current_state": "contingent_budget",
        "attempt_result": "drift channels require <=9.6e-15 yr^-1 or exact cancellation",
        "new_state": "contingent_budget",
        "why_not_promoted": "secular flux/domain/memory/source drift closure is not parent-derived",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The boundary/domain/flux no-hair problem is now a numeric contract. The alpha3 Ward-flux channels are the hardest local rows: each flux channel must be theorem-zero, Ward-cancelled, or below 4e-20 dimensionless before any local PPN claim is possible. Gdot/G drift channels need <=9.6e-15 yr^-1. Domain/vector/anisotropy channels are less brutal but still require explicit no-hair or coefficient maps. The existing corpus has conditional exits—class-only boundary, source-free bulk-X mass gap, gauge/topological domain/projector, and Ward-owned flux—but does not derive them from the parent action. Rows stay retained/budgeted.",
        "alpha3_flux_ceiling": "4e-20 dimensionless per flux channel",
        "Gdot_drift_ceiling": "9.6e-15 yr^-1 per drift channel",
        "flux_nohair_parent_derived": False,
        "domain_projector_nohair_parent_derived": False,
        "PPN_claim_allowed": False,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "look for a deeper motion/time/space origin of selector-blind matter, same-frame selection, and flux silence",
        "pass_condition": "selector/domain/flux silence becomes primitive-derived or explicitly postulated",
    },
    {
        "priority": 2,
        "target": "405-same-frame-EH-source-derived-stack-audit.md",
        "task": "combine checkpoints 401-403 into one strict local-GR necessary/sufficient stack",
        "pass_condition": "every GR/Newton rung is derived, conditional, retained, closure-only, or failed",
    },
    {
        "priority": 3,
        "target": "406-local-runner-v4-derived-vs-closure-queue.py",
        "task": "turn 401-403 row states into runner-v4 with derived/closure/retained separation",
        "pass_condition": "local runner distinguishes theorem-zero, closure-zero, conditional, and numeric retained rows",
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


def aggregate_bound_source_rows() -> list[dict[str, str]]:
    path = ROOT / "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv"
    return read_csv(path)


def contract_bound_rows() -> list[dict[str, Any]]:
    source_rows = aggregate_bound_source_rows()
    by_channel = {row["channel"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []
    for channel in CONTRACT_CHANNELS:
        if channel not in by_channel:
            continue
        source = by_channel[channel]
        bound = float(source["tightest_solo_bound"])
        rows.append(
            {
                "channel": channel,
                "required_ceiling": bound,
                "units": source["bound_units"],
                "tightest_row": source["tightest_row"],
                "tightest_observable": source["tightest_observable"],
                "sector": source["sector"],
                "required_exit": CHANNEL_EXIT_RULES[channel],
                "current_status": "not_parent_derived",
                "claim_policy": "theorem-zero, Ward-owned cancellation, source-budgeted coefficient, or retained residual only",
            }
        )
    rows.sort(key=lambda row: float(row["required_ceiling"]))
    return rows


def profile_value(profile: dict[str, Any], bound: float, units: str) -> float:
    if profile["profile"] == "one_tenth_tightest_bound":
        return 0.1 * bound
    if profile["profile"] == "edge_tightest_bound":
        return bound
    value_key = "per_year_value" if units == "yr^-1" else "dimensionless_value"
    value = profile[value_key]
    return float(value)


def profile_contract_rows(bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for profile in PROFILE_VALUES:
        for bound_row in bound_rows:
            bound = float(bound_row["required_ceiling"])
            value = profile_value(profile, bound, bound_row["units"])
            severity = value / bound if bound else 0.0
            if severity == 0.0:
                verdict = "theorem_zero_profile"
            elif severity < 1.0:
                verdict = "inside_only_if_derived"
            elif severity == 1.0:
                verdict = "edge_unstable"
            else:
                verdict = "over_contract"
            rows.append(
                {
                    "profile": profile["profile"],
                    "channel": bound_row["channel"],
                    "value": value,
                    "required_ceiling": bound,
                    "units": bound_row["units"],
                    "severity_ratio": severity,
                    "verdict": verdict,
                    "interpretation": profile["interpretation"],
                }
            )
    return rows


def profile_summary_rows(profile_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for profile in PROFILE_VALUES:
        subset = [row for row in profile_rows if row["profile"] == profile["profile"]]
        worst = max(subset, key=lambda row: float(row["severity_ratio"]))
        rows.append(
            {
                "profile": profile["profile"],
                "inside_channels": sum(1 for row in subset if float(row["severity_ratio"]) < 1.0),
                "edge_channels": sum(1 for row in subset if float(row["severity_ratio"]) == 1.0),
                "over_contract_channels": sum(1 for row in subset if float(row["severity_ratio"]) > 1.0),
                "worst_channel": worst["channel"],
                "worst_severity_ratio": worst["severity_ratio"],
                "verdict": "fails_contract" if any(float(row["severity_ratio"]) > 1.0 for row in subset) else profile["interpretation"],
            }
        )
    return rows


def family_rollup_rows(bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    families = {
        "alpha3_flux": ["bulk_flux_X", "domain_projector_flux", "unowned_momentum_flux"],
        "source_charge_WEP": [
            "boundary_species_charge",
            "bulk_X_composition_charge",
            "source_charge_species_split",
            "source_normalization_species_split",
        ],
        "Gdot_drift": [
            "domain_scale_drift_per_yr",
            "flux_drift_per_yr",
            "geff_meff_drift_per_yr",
            "memory_kernel_drift_per_yr",
        ],
        "domain_vector_alpha2": [
            "boundary_vector_B0i",
            "domain_anisotropy",
            "domain_vector_leakage",
            "projector_vector_leakage",
        ],
        "xi_anisotropy": [
            "boundary_tracefree_shear",
            "topology_cycle_anisotropy",
            "external_domain_anisotropy",
        ],
        "gamma_beta_fifth_force_hair": [
            "boundary_radial_hair",
            "bulk_X_metric_slip",
            "domain_projector_stress",
        ],
    }
    by_channel = {row["channel"]: row for row in bound_rows}
    rows: list[dict[str, Any]] = []
    for family, channels in families.items():
        present = [by_channel[channel] for channel in channels if channel in by_channel]
        if not present:
            continue
        tightest = min(present, key=lambda row: float(row["required_ceiling"]))
        rows.append(
            {
                "family": family,
                "channels": ";".join(row["channel"] for row in present),
                "tightest_ceiling": tightest["required_ceiling"],
                "units": tightest["units"],
                "tightest_channel": tightest["channel"],
                "tightest_observable": tightest["tightest_observable"],
                "status": "not_parent_derived",
            }
        )
    rows.sort(key=lambda row: float(row["tightest_ceiling"]))
    return rows


def gate_rows(source_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]], profile_summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    over_profiles = [row["profile"] for row in profile_summary if row["verdict"] == "fails_contract"]
    alpha3_rows = [row for row in bound_rows if row["tightest_observable"] == "alpha3"]
    drift_rows = [row for row in bound_rows if row["units"] == "yr^-1"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "numeric_bound_contract_written",
            "status": "pass" if bound_rows else "fail",
            "evidence": f"{len(bound_rows)} boundary/domain/flux/source channels contracted",
        },
        {
            "gate": "alpha3_flux_contract_explicit",
            "status": "pass" if len(alpha3_rows) == 3 else "fail",
            "evidence": f"{len(alpha3_rows)} alpha3 flux channels require 4e-20-scale closure",
        },
        {
            "gate": "Gdot_drift_contract_explicit",
            "status": "pass" if len(drift_rows) == 4 else "fail",
            "evidence": f"{len(drift_rows)} yr^-1 drift channels retained",
        },
        {
            "gate": "nohair_mechanism_tests_written",
            "status": "pass",
            "evidence": f"{len(NOHAIR_MECHANISM_TESTS)} mechanism tests written",
        },
        {
            "gate": "over_contract_profiles_detected",
            "status": "pass" if over_profiles else "fail",
            "evidence": ";".join(over_profiles),
        },
        {
            "gate": "Ward_flux_nohair_parent_derived",
            "status": "fail",
            "evidence": "total Ward flux owner is mapped but not derived",
        },
        {
            "gate": "domain_projector_nohair_parent_derived",
            "status": "fail",
            "evidence": "gauge/topological selector status not parent-derived",
        },
        {
            "gate": "PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "numeric contract only; rows remain retained/budgeted/contingent",
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
    bound_rows: list[dict[str, Any]],
    family_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    hardest_rows = [
        {
            "channel": row["channel"],
            "ceiling": format_float(row["required_ceiling"]),
            "units": row["units"],
            "observable": row["tightest_observable"],
        }
        for row in bound_rows[:12]
    ]
    family_table_rows = [
        {
            "family": row["family"],
            "ceiling": format_float(row["tightest_ceiling"]),
            "units": row["units"],
            "channel": row["tightest_channel"],
        }
        for row in family_rows
    ]
    summary_table_rows = [
        {
            "profile": row["profile"],
            "over": row["over_contract_channels"],
            "worst": row["worst_channel"],
            "severity": format_float(row["worst_severity_ratio"]),
            "verdict": row["verdict"],
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
    text = f"""# 403 - Boundary Domain Flux No-Hair Numeric Contract

Private boundary/domain/flux local-GR checkpoint. This is not a public PPN, fifth-force, source-normalization, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 400 showed the ugly part clearly: local GR is not mainly waiting on a pretty gamma/beta sentence. The hardest rows are unowned flux, domain/projector flux, bulk-X flux, source charge, and secular drift.

This checkpoint turns those rows into a numeric no-hair contract.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_domain_flux_nohair_numeric_contract.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Hardest Channel Ceilings

{markdown_table(hardest_rows, ["channel", "ceiling", "units", "observable"])}

## 4. Family Rollup

{markdown_table(family_table_rows, ["family", "ceiling", "units", "channel"])}

## 5. Allowed Exits

A channel may leave the runner only by one of these exits:

- theorem-zero from the parent action;
- exact Ward-owned cancellation;
- gauge/topological no-hair theorem;
- constant universal source-normalized monopole absorption;
- explicit coefficient/range/source-charge map retained for testing.

Anything else is just hiding a local fifth force, preferred-frame term, or source-normalization residue.

## 6. Profile Contract

{markdown_table(summary_table_rows, ["profile", "over", "worst", "severity", "verdict"])}

## 7. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 8. Decision

{DECISION[0]["decision"]}

Practical read: this is grim only in the useful sense. The numbers are harsh, but that is exactly what a GR-reduction programme needs: no “small enough probably” language. The alpha3 flux row wants exact Ward silence or a suppression below `4e-20`. That is not a fitting target; it is a derivation target.

## 9. Next Target

`{NEXT_TARGET}`

Try to find the primitive MTS reason why matter, frame choice, and flux/domain/projector channels become silent locally. If that primitive reason exists, it may pay multiple debts at once.
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    bound_rows = contract_bound_rows()
    profile_rows = profile_contract_rows(bound_rows)
    profile_summary = profile_summary_rows(profile_rows)
    family_rows = family_rollup_rows(bound_rows)
    gate_result_rows = gate_rows(source_rows, bound_rows, profile_summary)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "numeric_bound_contract.csv", bound_rows)
    write_csv(results_dir / "family_rollup.csv", family_rows)
    write_csv(results_dir / "nohair_mechanism_tests.csv", NOHAIR_MECHANISM_TESTS)
    write_csv(results_dir / "flux_balance_equations.csv", FLUX_BALANCE_EQUATIONS)
    write_csv(results_dir / "profile_contract_evaluator.csv", profile_rows)
    write_csv(results_dir / "profile_contract_summary.csv", profile_summary)
    write_csv(results_dir / "row_transition_decision.csv", ROW_TRANSITION_DECISION)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
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
        "contract_channels": len(bound_rows),
        "family_rollups": len(family_rows),
        "flux_nohair_parent_derived": False,
        "domain_projector_nohair_parent_derived": False,
        "PPN_claim_allowed": False,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, bound_rows, family_rows, profile_summary, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 403 boundary/domain/flux no-hair numeric contract artifacts."
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
