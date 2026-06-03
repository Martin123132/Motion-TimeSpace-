from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "extra-sector-nohair-priority-gate"
CHECKPOINT_DOC = "441-extra-sector-nohair-priority-gate.md"
STATUS = "extra_sector_nohair_priority_gate_written_P6_second_order_restriction_ranked_first_extra_sectors_retained_no_EH_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "extra_sector_nohair_priority_gate_only_no_EH_Newton_PPN_R10_R11_or_local_GR_pass"
NEXT_TARGET = "442-P6-second-order-operator-restriction-or-R11-demotion.md"


SOURCE_DOCS = [
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "local residual family ceilings and boundary/domain/flux locks",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "operator/source retained ledger and local-bound test plan",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "hidden-variable Euler ledger and R10/R11 row routing",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "operator-family vector contract and R11 theorem-zero routes",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "P0-P9 EH-only parent-premise ladder",
    },
    {
        "path": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "sector-by-sector metric-only reduction attempt",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/family_rollup.csv",
        "role": "source-locked family severity rollup",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/EH_operator_retained_ledger.csv",
        "role": "canonical retained operator-family ledger",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "A0-A9 auxiliary/projector/domain sector rows",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/operator_families.csv",
        "role": "canonical R11 operator-family basis",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/theorem_zero_routes.csv",
        "role": "R11 theorem-zero/fallback routes",
    },
    {
        "path": "runs/20260602-133000-metric-only-second-order-sector-reduction-attempt/results/sector_reduction_matrix.csv",
        "role": "current sector reduction matrix",
    },
    {
        "path": "runs/20260602-133000-metric-only-second-order-sector-reduction-attempt/results/second_order_operator_filter.csv",
        "role": "current second-order operator filter",
    },
    {
        "path": "runs/20260602-133000-metric-only-second-order-sector-reduction-attempt/results/residual_map.csv",
        "role": "current failed-reduction residual map",
    },
    {
        "path": "source-intake/mts_residuals/R10_alpha_lambda_curve_TEMPLATE.csv",
        "role": "R10 curve fallback template",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "R11 vector fallback template",
    },
]


PRIORITY_CRITERIA = [
    {
        "criterion": "EH_impact",
        "scale": "1-5",
        "meaning": "how directly the sector blocks EH-only metric exterior",
        "weight": 3,
    },
    {
        "criterion": "Newton_PPN_impact",
        "scale": "1-5",
        "meaning": "how strongly the sector blocks measured Newton/PPN rows",
        "weight": 2,
    },
    {
        "criterion": "proof_tractability",
        "scale": "1-5",
        "meaning": "how crisp the next theorem attempt is with current corpus ingredients",
        "weight": 2,
    },
    {
        "criterion": "severity",
        "scale": "1-5",
        "meaning": "how tight or dangerous the local observational locks are if the sector survives",
        "weight": 1,
    },
    {
        "criterion": "dependency_leverage",
        "scale": "1-5",
        "meaning": "how many later rungs or rows become cleaner if this sector is resolved",
        "weight": 2,
    },
    {
        "criterion": "fallback_readiness",
        "scale": "1-5",
        "meaning": "how ready the sector is to become executable R10/R11 data if theorem-zero fails",
        "weight": 1,
    },
    {
        "criterion": "scope_risk",
        "scale": "1-5",
        "meaning": "penalty for being too broad/vague for the next focused derivation attempt",
        "weight": -1,
    },
]


SECTOR_PRIORITY_INPUTS = [
    {
        "sector": "higher_curvature_metric_operators",
        "primary_rung": "P6_second_order_metric_equations",
        "affected_rows": "R3;R4;R8;R10;R11",
        "best_theorem_route": "derive parent second-order/locality/regularity restriction or topological-only higher-curvature combination",
        "fallback_route": "fill R11 R2/fR/Ricci/Weyl coefficients and R10 curve if finite-range scalar mode survives",
        "EH_impact": 5,
        "Newton_PPN_impact": 5,
        "proof_tractability": 3,
        "severity": 4,
        "dependency_leverage": 5,
        "fallback_readiness": 5,
        "scope_risk": 2,
        "decision": "attack_theorem_first_then_R11",
    },
    {
        "sector": "source_normalization_operator",
        "primary_rung": "P8_constant_source_normalization",
        "affected_rows": "R1;R4;R9;R10;R11",
        "best_theorem_route": "derive mu_obs=G_eff M_eff with no time/range/species/radial leakage",
        "fallback_route": "retain source residual coefficients plus Gdot/beta/source-charge/R10 maps",
        "EH_impact": 3,
        "Newton_PPN_impact": 5,
        "proof_tractability": 3,
        "severity": 5,
        "dependency_leverage": 5,
        "fallback_readiness": 4,
        "scope_risk": 2,
        "decision": "high_priority_but_Newton_lane_not_P6",
    },
    {
        "sector": "bulk_X_memory_load",
        "primary_rung": "P3_no_extra_local_propagating_fields",
        "affected_rows": "R1;R3;R4;R9;R10;R11",
        "best_theorem_route": "derive positive source-free local exterior operator and no boundary/domain re-source",
        "fallback_route": "fill R10 alpha_X(lambda_X) and R11 bulk-X coefficient rows",
        "EH_impact": 4,
        "Newton_PPN_impact": 4,
        "proof_tractability": 3,
        "severity": 4,
        "dependency_leverage": 4,
        "fallback_readiness": 4,
        "scope_risk": 2,
        "decision": "parallel_R10_R11_theorem_or_curve",
    },
    {
        "sector": "torsion_nonmetricity_connection",
        "primary_rung": "P4_metric_compatibility_connection",
        "affected_rows": "R0;R1;R2;R11",
        "best_theorem_route": "derive Levi-Civita compatibility from connection/spin-connection variation in observed branch",
        "fallback_route": "fill R11 torsion/nonmetricity coefficient rows and WEP/clock/light-cone caveats",
        "EH_impact": 3,
        "Newton_PPN_impact": 4,
        "proof_tractability": 4,
        "severity": 4,
        "dependency_leverage": 3,
        "fallback_readiness": 5,
        "scope_risk": 1,
        "decision": "crisp_subproblem_after_P6",
    },
    {
        "sector": "boundary_class_terms",
        "primary_rung": "P7_boundary_topological_harmlessness",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "best_theorem_route": "derive class-only topological/Ward-owned boundary action with no local shear/vector/radial/flux hair",
        "fallback_route": "retain boundary coefficients feeding gamma, beta, alpha3, xi, Gdot, and R11",
        "EH_impact": 4,
        "Newton_PPN_impact": 4,
        "proof_tractability": 2,
        "severity": 5,
        "dependency_leverage": 4,
        "fallback_readiness": 3,
        "scope_risk": 3,
        "decision": "important_but_hard_rank_after_crisper_targets",
    },
    {
        "sector": "vector_preferred_frame",
        "primary_rung": "P3_no_extra_local_propagating_fields",
        "affected_rows": "R5;R6;R7;R8;R11",
        "best_theorem_route": "derive no independent local vector/domain normal or pure-gauge alignment without stress",
        "fallback_route": "retain preferred-frame coefficient rows for alpha1/alpha2/alpha3/xi",
        "EH_impact": 4,
        "Newton_PPN_impact": 4,
        "proof_tractability": 2,
        "severity": 5,
        "dependency_leverage": 4,
        "fallback_readiness": 3,
        "scope_risk": 3,
        "decision": "severe_but_needs_domain_projector_subsplit",
    },
    {
        "sector": "projector_domain_stress",
        "primary_rung": "P2_full_Ward_Euler_ownership;P3_no_extra_local_propagating_fields",
        "affected_rows": "R5;R6;R7;R8;R9;R10;R11",
        "best_theorem_route": "derive covariant first-class/topological projector algebra and metric-independent or retained stress",
        "fallback_route": "retain projector/domain stress vector and induced preferred-frame/Gdot/R10/R11 rows",
        "EH_impact": 4,
        "Newton_PPN_impact": 4,
        "proof_tractability": 2,
        "severity": 5,
        "dependency_leverage": 4,
        "fallback_readiness": 3,
        "scope_risk": 4,
        "decision": "split_before_full_attack",
    },
    {
        "sector": "scalar_class_metric",
        "primary_rung": "P3_no_extra_local_propagating_fields",
        "affected_rows": "R2;R3;R4;R9;R10;R11",
        "best_theorem_route": "prove local scalar/class invariant algebra trivial or constant universal with zero stress/source charge",
        "fallback_route": "retain scalar/class coefficient rows and induced clock/PPN/Gdot/R10 maps",
        "EH_impact": 4,
        "Newton_PPN_impact": 4,
        "proof_tractability": 2,
        "severity": 4,
        "dependency_leverage": 4,
        "fallback_readiness": 4,
        "scope_risk": 4,
        "decision": "too_broad_without_subsector_split",
    },
    {
        "sector": "nonlocal_memory_kernel",
        "primary_rung": "P5_local_4D_diffeomorphic_metric_action",
        "affected_rows": "R7;R9;R10;R11",
        "best_theorem_route": "derive compact-local kernel silence/screening or pure constant universal calibration",
        "fallback_route": "retain nonlocal kernel coefficient rows and alpha3/Gdot/R10 maps",
        "EH_impact": 3,
        "Newton_PPN_impact": 4,
        "proof_tractability": 2,
        "severity": 5,
        "dependency_leverage": 3,
        "fallback_readiness": 3,
        "scope_risk": 4,
        "decision": "defer_until_locality_principle_is_sharper",
    },
]


SEVERITY_LOCKS = [
    {
        "family": "alpha3_flux",
        "tightest_ceiling": "4e-20",
        "observable": "alpha3",
        "sectors_hit": "boundary_class_terms;vector_preferred_frame;projector_domain_stress;nonlocal_memory_kernel",
        "priority_note": "ultratight but broad; needs owned Ward flux or coefficient data",
    },
    {
        "family": "source_charge_WEP",
        "tightest_ceiling": "2.8e-15",
        "observable": "eta_WEP_source_charge",
        "sectors_hit": "source_normalization_operator;bulk_X_memory_load;torsion_nonmetricity_connection",
        "priority_note": "source channel is Newton-critical but not the P6 metric-only gate",
    },
    {
        "family": "Gdot_drift",
        "tightest_ceiling": "9.6e-15 yr^-1",
        "observable": "Gdot_over_G",
        "sectors_hit": "source_normalization_operator;nonlocal_memory_kernel;projector_domain_stress;boundary_class_terms",
        "priority_note": "drift rows force constant measured-GM or explicit residual map",
    },
    {
        "family": "domain_vector_alpha2",
        "tightest_ceiling": "2e-09",
        "observable": "alpha2",
        "sectors_hit": "vector_preferred_frame;projector_domain_stress;boundary_class_terms",
        "priority_note": "vector/domain rows are severe but need a narrower subproblem",
    },
    {
        "family": "xi_anisotropy",
        "tightest_ceiling": "4e-09",
        "observable": "xi",
        "sectors_hit": "boundary_class_terms;projector_domain_stress;vector_preferred_frame;higher_curvature_metric_operators",
        "priority_note": "anisotropy is a clean observable sink for boundary/domain/higher-curvature leakage",
    },
    {
        "family": "gamma_beta_fifth_force_hair",
        "tightest_ceiling": "2.3e-05",
        "observable": "gamma_minus_1",
        "sectors_hit": "bulk_X_memory_load;boundary_class_terms;projector_domain_stress;higher_curvature_metric_operators",
        "priority_note": "less numerically severe than alpha3, but central for GR reduction",
    },
]


NOHAIR_PROOF_CONTRACTS = [
    {
        "sector": "higher_curvature_metric_operators",
        "minimum_proof_contract": "parent principle forbids local higher-derivative metric propagators through tested scales or makes them topological/zero",
        "must_not_use": "Bianchi conservation as uniqueness; EFT smallness as theorem-zero",
        "fallback_if_failed": "R11 R2/fR/Ricci/Weyl rows with weak-field maps",
    },
    {
        "sector": "torsion_nonmetricity_connection",
        "minimum_proof_contract": "connection variation enforces Levi-Civita observed branch and universal matter/light/spin connection",
        "must_not_use": "assuming omega[e] after writing independent connection variables",
        "fallback_if_failed": "R11 torsion/nonmetricity rows plus WEP/clock/light-cone residuals",
    },
    {
        "sector": "bulk_X_memory_load",
        "minimum_proof_contract": "positive source-free exterior operator with no boundary/domain/source re-coupling, or executable source-normalized force law",
        "must_not_use": "mass gap without charge/source normalization",
        "fallback_if_failed": "R10 alpha_X(lambda_X) curve and R11 bulk-X row",
    },
    {
        "sector": "source_normalization_operator",
        "minimum_proof_contract": "derive constant universal measured-GM and mu_extra=0 with no species/time/range/radial dependence",
        "must_not_use": "absorbing range/time/species-dependent effects into measured GM",
        "fallback_if_failed": "R1/R4/R9/R10/R11 source residual vector",
    },
    {
        "sector": "boundary_class_terms",
        "minimum_proof_contract": "class-only topological/Ward-owned boundary action with no local shear, radial, vector, flux, or preferred-location hair",
        "must_not_use": "boundary Euler equation as bulk no-hair",
        "fallback_if_failed": "boundary coefficient vector feeding R3/R4/R7/R8/R9/R11",
    },
    {
        "sector": "vector_preferred_frame",
        "minimum_proof_contract": "prove no independent local vector/domain normal survives, or it is pure gauge/aligned without stress",
        "must_not_use": "covariance alone as no preferred frame",
        "fallback_if_failed": "alpha1/alpha2/alpha3/xi coefficient rows",
    },
    {
        "sector": "projector_domain_stress",
        "minimum_proof_contract": "derive first-class/topological projector algebra and keep/dismiss metric stress lawfully",
        "must_not_use": "dropping projector stress after choosing a convenient domain",
        "fallback_if_failed": "projector/domain stress vector plus induced R rows",
    },
    {
        "sector": "scalar_class_metric",
        "minimum_proof_contract": "prove local quotient/class scalar algebra is trivial or constant universal with zero stress/source charge",
        "must_not_use": "setting scalar profile flat without parent selector",
        "fallback_if_failed": "scalar/class R11 row plus R2/R3/R4/R9/R10 maps",
    },
    {
        "sector": "nonlocal_memory_kernel",
        "minimum_proof_contract": "derive compact-local kernel silence/screening or constant universal calibration",
        "must_not_use": "cosmological memory success as local kernel silence",
        "fallback_if_failed": "nonlocal kernel R11 row plus R7/R9/R10 maps",
    },
]


def compute_priority_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in SECTOR_PRIORITY_INPUTS:
        theorem_score = (
            3 * int(row["EH_impact"])
            + 2 * int(row["proof_tractability"])
            + 2 * int(row["dependency_leverage"])
            + int(row["severity"])
            - int(row["scope_risk"])
        )
        data_score = (
            2 * int(row["severity"])
            + 2 * int(row["fallback_readiness"])
            + int(row["Newton_PPN_impact"])
            + int(row["EH_impact"])
            - int(row["scope_risk"])
        )
        combined_score = theorem_score + data_score
        rows.append(
            {
                **row,
                "theorem_score": theorem_score,
                "data_score": data_score,
                "combined_score": combined_score,
            }
        )
    rows.sort(key=lambda item: (-int(item["theorem_score"]), -int(item["combined_score"]), item["sector"]))
    for index, row in enumerate(rows, start=1):
        row["theorem_rank"] = index
    rows.sort(key=lambda item: (-int(item["data_score"]), -int(item["combined_score"]), item["sector"]))
    for index, row in enumerate(rows, start=1):
        row["data_rank"] = index
    rows.sort(key=lambda item: int(item["theorem_rank"]))
    return rows


def route_decisions(priority_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "lane": "next_theorem_attack",
            "chosen_sector": "higher_curvature_metric_operators",
            "target": NEXT_TARGET,
            "why": "highest theorem score and directly controls P6, the second-order metric-equation blocker for EH selection",
            "non_claim": "does not promote EH; it tries to derive or demote P6",
        },
        {
            "lane": "next_crisp_subproblem",
            "chosen_sector": "torsion_nonmetricity_connection",
            "target": "metric-compatibility theorem attempt after P6",
            "why": "best tractability among retained sectors; clean Levi-Civita-or-R11 fork",
            "non_claim": "solves P4 only if derived; not sufficient for EH alone",
        },
        {
            "lane": "next_data_fallback",
            "chosen_sector": priority_rows[0]["sector"],
            "target": "start with top theorem lane if theorem fails; fill its R11 rows first",
            "why": "R11 fallback should follow the sector currently under theorem attack",
            "non_claim": "data fallback is empirical retained-branch viability, not derived local GR",
        },
        {
            "lane": "parallel_Newton_lane",
            "chosen_sector": "source_normalization_operator",
            "target": "source-normalization residual vector refinement",
            "why": "highest Newton/PPN importance but not the P6 metric-only theorem target",
            "non_claim": "Newtonian measured-GM remains conditional",
        },
    ]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "extra-sector no-hair priorities ranked",
        "status": "pass",
        "evidence": "9 retained sectors scored by theorem value and data fallback urgency",
    },
    {
        "claim": "next theorem target selected",
        "status": "pass",
        "evidence": NEXT_TARGET,
    },
    {
        "claim": "all sectors no-haired",
        "status": "fail",
        "evidence": "ranking only; no sector receives theorem-zero credit",
    },
    {
        "claim": "R11 data supplied",
        "status": "fail",
        "evidence": "R11 template exists but remains unfilled",
    },
    {
        "claim": "EH/Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "priority gate only; no derivation or empirical residual pass",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "priority_criteria_written",
        "status": "pass",
        "evidence": "7 scoring criteria recorded",
    },
    {
        "gate": "sector_priority_matrix_written",
        "status": "pass",
        "evidence": "9 extra sectors ranked",
    },
    {
        "gate": "severity_locks_imported",
        "status": "pass",
        "evidence": "6 local family locks mapped to sectors",
    },
    {
        "gate": "nohair_contracts_written",
        "status": "pass",
        "evidence": "9 minimum no-hair proof contracts recorded",
    },
    {
        "gate": "next_theorem_attack_selected",
        "status": "pass",
        "evidence": NEXT_TARGET,
    },
    {
        "gate": "all_sectors_theorem_zero",
        "status": "fail",
        "evidence": "ranking does not derive no-hair",
    },
    {
        "gate": "R10_R11_fallbacks_filled",
        "status": "fail",
        "evidence": "templates exist but no real curve/vector data supplied",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "priority gate only; no EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The extra-sector no-hair queue is now ranked. The best next theorem attack is the P6 second-order operator restriction, because higher-curvature/nonlocal metric operators directly block EH selection and have a crisp theorem-or-R11 fork. Source normalization remains the parallel Newton lane, torsion/nonmetricity is the crisp follow-up subproblem, and boundary/vector/projector/scalar/nonlocal sectors stay retained until narrowed or filled as R11 data. No sector receives theorem-zero credit from this ranking.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "442-P6-second-order-operator-restriction-or-R11-demotion.md",
        "why_next": "highest theorem-priority sector; directly decides whether higher-curvature/nonlocal metric operators are forbidden or retained",
    },
    {
        "rank": 2,
        "target": "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
        "why_next": "crisp torsion/nonmetricity subproblem after P6; clean theorem-or-vector fork",
    },
    {
        "rank": 3,
        "target": "source-normalization residual vector refinement",
        "why_next": "parallel Newton lane; needed for measured-GM even if EH operator is derived",
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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    return [source_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(
    run_dir: Path, priority_rows: list[dict[str, Any]], decision_rows: list[dict[str, Any]], gate_result_rows: list[dict[str, Any]]
) -> None:
    source_rows = source_register_rows()
    text = f"""# 441 - Extra-Sector No-Hair Priority Gate

Private prioritization checkpoint. This is not a public Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, cosmology, local-GR, or unified-field claim.

## 1. Purpose

Checkpoint 440 made the hard list: extra sectors do not vanish for free. This checkpoint ranks the no-hair/reduction work so the next turns attack the most useful theorem target first rather than wandering across every open sector.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/extra_sector_nohair_priority_gate.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Priority Criteria

{markdown_table(PRIORITY_CRITERIA, ["criterion", "scale", "meaning", "weight"])}

## 5. Sector Priority Matrix

{markdown_table(priority_rows, ["theorem_rank", "data_rank", "sector", "primary_rung", "affected_rows", "theorem_score", "data_score", "decision"])}

## 6. Severity Locks

{markdown_table(SEVERITY_LOCKS, ["family", "tightest_ceiling", "observable", "sectors_hit", "priority_note"])}

## 7. No-Hair Proof Contracts

{markdown_table(NOHAIR_PROOF_CONTRACTS, ["sector", "minimum_proof_contract", "must_not_use", "fallback_if_failed"])}

## 8. Route Decisions

{markdown_table(decision_rows, ["lane", "chosen_sector", "target", "why", "non_claim"])}

## 9. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 10. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is the queue discipline. We do not try to solve every monster at once. We hit P6 first because it is the cleanest gate between "EH follows" and "R11 modified-gravity vector required".

## 12. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    priority_rows = compute_priority_rows()
    decision_rows = route_decisions(priority_rows)
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "priority_criteria.csv", PRIORITY_CRITERIA)
    write_csv(results_dir / "sector_priority_matrix.csv", priority_rows)
    write_csv(results_dir / "severity_locks.csv", SEVERITY_LOCKS)
    write_csv(results_dir / "nohair_proof_contracts.csv", NOHAIR_PROOF_CONTRACTS)
    write_csv(results_dir / "route_decisions.csv", decision_rows)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
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
        "priority_criteria": len(PRIORITY_CRITERIA),
        "ranked_sectors": len(priority_rows),
        "severity_locks": len(SEVERITY_LOCKS),
        "nohair_contracts": len(NOHAIR_PROOF_CONTRACTS),
        "route_decisions": len(decision_rows),
        "next_theorem_target": NEXT_TARGET,
        "all_sectors_theorem_zero": False,
        "R10_R11_fallbacks_filled": False,
        "EH_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, priority_rows, decision_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write checkpoint 441 extra-sector no-hair priority gate artifacts.")
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
