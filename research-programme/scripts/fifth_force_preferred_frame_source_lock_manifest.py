from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "fifth-force-preferred-frame-source-lock-manifest"
STATUS = "preferred_frame_xi_source_locked_fifth_force_parameterized_not_scalar_scored_no_local_GR_pass"
CLAIM_CEILING = "source_lock_manifest_only_no_fifth_force_preferred_frame_PPN_EH_WEP_or_local_GR_pass"
NEXT_TARGET = "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md"


SOURCE_DOCS = [
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "original source-lock checkpoint: gamma/beta/WEP/redshift ready, preferred-frame/xi/fifth-force quarantined",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "source-locked runner policy: numeric ready rows get budgets, missing source locks quarantine rows",
    },
    {
        "path": "369-source-locked-closure-branch-local-bound-runner.md",
        "role": "closure-branch runner with ready budget rows and quarantined preferred-frame/xi/fifth-force rows",
    },
    {
        "path": "370-common-mode-phiC-coefficient-map.md",
        "role": "common-mode phi_C map: fifth-force proxy identified but row still quarantined",
    },
    {
        "path": "372-local-phiC-zero-theorem-or-gradient-bound.md",
        "role": "local phi_C zero theorem conditional; fifth-force gradient proxy killed only in that branch",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "WEP closure/selector audit: eta remains active and no local-GR pass follows",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary residual decomposition including vector/preferred-frame, trace-free, radial, and conservation hazards",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-owned residual map and retained vector/radial/operator rows",
    },
]


EXTERNAL_SOURCES = [
    {
        "source_id": "will_living_reviews_2014_table4",
        "title": "The Confrontation between General Relativity and Experiment - Table 4 Current limits on PPN parameters",
        "url": "https://link.springer.com/article/10.12942/lrr-2014-4/tables/4",
        "use": "source-lock alpha1, alpha2, alpha3, xi preferred-frame/preferred-location PPN targets",
        "source_status": "review_source_locked_for_internal_targets",
        "accessed_date": "2026-06-01",
    },
    {
        "source_id": "pdg_gravity_tests_2025",
        "title": "PDG 2025 Experimental Tests of Gravitational Theory",
        "url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-gravity-tests.pdf",
        "use": "current review cross-check for EEP, local Lorentz invariance, WEP, Gdot/G, gamma, beta, and metric-coupling context",
        "source_status": "current_review_cross_check",
        "accessed_date": "2026-06-01",
    },
    {
        "source_id": "lee_2020_inverse_square_52um",
        "title": "New test of the gravitational 1/r^2 law at separations down to 52 micrometers",
        "url": "https://doi.org/10.1103/PhysRevLett.124.101101",
        "use": "short-range inverse-square-law context: no deviation over 52 micrometers to 3 millimeters in the cited review highlight",
        "source_status": "primary_article_range_anchor",
        "accessed_date": "2026-06-01",
    },
    {
        "source_id": "tan_2020_submillimeter_yukawa",
        "title": "Improvement for Testing the Gravitational Inverse-Square Law at the Submillimeter Range",
        "url": "https://doi.org/10.1103/PhysRevLett.124.051301",
        "use": "Yukawa parameterization anchor: |alpha| <= 1 down to lambda = 48 micrometers and strongest 40-350 micrometer bound",
        "source_status": "primary_article_range_anchor",
        "accessed_date": "2026-06-01",
    },
]


RESIDUAL_SOURCE_LOCK_MANIFEST = [
    {
        "residual": "preferred_frame_alpha1",
        "observable_channel": "orbital polarization / local preferred-frame vector metric",
        "source_locked_scale_abs": 1.0e-4,
        "stricter_context_scale_abs": 4.0e-5,
        "units": "dimensionless PPN alpha1",
        "source_id": "will_living_reviews_2014_table4",
        "MTS_source_channel": "boundary_vector_B0i; marker/projector velocity; coframe vector slip",
        "MTS_coefficient_status": "missing",
        "runner_status_after_374": "source_locked_ready_budget_only",
        "score_allowed": "no",
    },
    {
        "residual": "preferred_frame_alpha2",
        "observable_channel": "spin precession / local preferred-frame vector-tensor metric",
        "source_locked_scale_abs": 2.0e-9,
        "stricter_context_scale_abs": "",
        "units": "dimensionless PPN alpha2",
        "source_id": "will_living_reviews_2014_table4",
        "MTS_source_channel": "boundary_vector_B0i; anisotropic coframe velocity; surviving marker field",
        "MTS_coefficient_status": "missing",
        "runner_status_after_374": "source_locked_ready_budget_only",
        "score_allowed": "no",
    },
    {
        "residual": "preferred_frame_alpha3",
        "observable_channel": "pulsar acceleration / preferred-frame plus momentum nonconservation",
        "source_locked_scale_abs": 4.0e-20,
        "stricter_context_scale_abs": "",
        "units": "dimensionless PPN alpha3",
        "source_id": "will_living_reviews_2014_table4",
        "MTS_source_channel": "nonconserved boundary flux; unowned selector stress; preferred-frame vector leakage",
        "MTS_coefficient_status": "missing",
        "runner_status_after_374": "source_locked_ready_budget_only_if_MTS_predicts_alpha3_channel",
        "score_allowed": "no",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "observable_channel": "preferred-location / anisotropic external-potential coupling",
        "source_locked_scale_abs": 4.0e-9,
        "stricter_context_scale_abs": "",
        "units": "dimensionless PPN xi",
        "source_id": "will_living_reviews_2014_table4",
        "MTS_source_channel": "trace-free boundary shear B_TF; external-domain anisotropy; l>=2 class metric hair",
        "MTS_coefficient_status": "missing",
        "runner_status_after_374": "source_locked_ready_budget_only",
        "score_allowed": "no",
    },
    {
        "residual": "Gdot_over_G",
        "observable_channel": "secular variation of Newton constant",
        "source_locked_scale_abs": 9.6e-15,
        "stricter_context_scale_abs": "",
        "units": "yr^-1 one-sigma scale from LLR summary",
        "source_id": "pdg_gravity_tests_2025",
        "MTS_source_channel": "time-varying common-mode coupling or changing measured-GM normalization",
        "MTS_coefficient_status": "missing_and_only_applicable_if_branch_predicts_Gdot",
        "runner_status_after_374": "source_locked_ready_budget_only_if_applicable",
        "score_allowed": "no",
    },
    {
        "residual": "delta_G_or_fifth_force_yukawa",
        "observable_channel": "range-dependent inverse-square-law / Yukawa deviation",
        "source_locked_scale_abs": "",
        "stricter_context_scale_abs": "",
        "units": "dimensionless Yukawa alpha as a function of range lambda",
        "source_id": "lee_2020_inverse_square_52um; tan_2020_submillimeter_yukawa",
        "MTS_source_channel": "radial scalar hair; bulk X gradient; common-mode phi_C gradient; class-changing boundary force",
        "MTS_coefficient_status": "missing_range_lambda_and_coupling_map",
        "runner_status_after_374": "parameterized_source_locked_but_not_scalar_scored",
        "score_allowed": "no",
    },
]


FIFTH_FORCE_PARAMETERIZATION = [
    {
        "object": "Yukawa_potential_contract",
        "form": "V(r) = -G m1 m2 / r * [1 + alpha_Y exp(-r/lambda_Y)]",
        "why_needed": "fifth-force limits are curves in alpha_Y(lambda_Y), not one universal scalar tolerance",
        "MTS_missing_input": "derive lambda_Y and alpha_Y from phi_C, X, radial hair, boundary force, or class transition law",
        "status": "required_before_scoring",
    },
    {
        "object": "short_range_anchor_52um_to_3mm",
        "form": "inverse-square law tested at separations 52 micrometers to 3 millimeters with no required modification",
        "why_needed": "anchors laboratory short-range force context",
        "MTS_missing_input": "map local MTS force range into this separation interval",
        "status": "source_context_only",
    },
    {
        "object": "submillimeter_yukawa_anchor",
        "form": "|alpha_Y| <= 1 down to lambda_Y = 48 micrometers; strongest quoted 40-350 micrometer bound in Tan et al. abstract",
        "why_needed": "gives one concrete range anchor without pretending it covers all fifth-force scales",
        "MTS_missing_input": "show MTS predicts lambda_Y near this range before using the bound",
        "status": "conditional_range_anchor",
    },
    {
        "object": "solar_system_or_galactic_range",
        "form": "not represented by a single submillimeter torsion-balance number",
        "why_needed": "MTS local phi_C or bulk-X gradients may be long-range, screened, or domain-wall-like",
        "MTS_missing_input": "derive range, screening, composition dependence, and source normalization",
        "status": "quarantine_for_nonlocal_ranges",
    },
]


MTS_SOURCE_MAP_REQUIREMENTS = [
    {
        "MTS_channel": "boundary_vector_B0i",
        "observational_rows": "preferred_frame_alpha1;preferred_frame_alpha2",
        "theorem_zero_route": "no physical marker fields; vector representative is pure gauge or constrained topological bookkeeping",
        "budget_route": "derive alpha1/alpha2 coefficients from weak-field metric and compare to source-locked scales",
        "current_status": "coefficient_missing",
    },
    {
        "MTS_channel": "unowned_selector_stress_or_flux",
        "observational_rows": "preferred_frame_alpha3;Gdot_over_G;secular_orbital_drift",
        "theorem_zero_route": "selector/projector stress appears in total Ward ledger and boundary flux cancels",
        "budget_route": "derive nonconservation/preferred-frame coefficient before using alpha3 or Gdot rows",
        "current_status": "Ward_ownership_open",
    },
    {
        "MTS_channel": "trace_free_boundary_shear_B_TF",
        "observational_rows": "xi_preferred_location_anisotropy;gamma_minus_1;lensing_slip",
        "theorem_zero_route": "class-only boundary action has no angular representative or l>=2 source",
        "budget_route": "derive xi coefficient from anisotropic external-potential coupling",
        "current_status": "coefficient_missing",
    },
    {
        "MTS_channel": "radial_scalar_hair_or_bulk_X_gradient",
        "observational_rows": "delta_G_or_fifth_force_yukawa;beta_minus_1;perihelion",
        "theorem_zero_route": "no independent radial scalar charge, or universal conserved monopole absorbed into measured GM",
        "budget_route": "derive alpha_Y(lambda_Y) or a solar-system force coefficient",
        "current_status": "range_and_coupling_missing",
    },
    {
        "MTS_channel": "common_mode_phiC_gradient",
        "observational_rows": "delta_G_or_fifth_force_yukawa;gamma_minus_1;alpha_clock_redshift",
        "theorem_zero_route": "local trivial class gives grad(phi_C)=0",
        "budget_route": "use r_grad only for gamma/clock unless a fifth-force range/coupling map is derived",
        "current_status": "conditional_zero_or_budget_only",
    },
    {
        "MTS_channel": "species_specific_class_response",
        "observational_rows": "eta_WEP;composition_dependent_fifth_force",
        "theorem_zero_route": "parent-selected one observed coframe and common F(C_D)",
        "budget_route": "eta_WEP source-lock already active",
        "current_status": "WEP_closure_axiom_required",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "preferred_frame_alpha1",
        "after_369": "quarantined_no_numeric_source_lock",
        "after_374": "source_locked_ready_budget_only",
        "budget": "alpha1 <= 1e-4 local conservative row; 4e-5 stricter pulsar context retained",
        "pass_claim": "blocked_by_missing_MTS_coefficient",
    },
    {
        "runner_row": "preferred_frame_alpha2",
        "after_369": "quarantined_no_numeric_source_lock",
        "after_374": "source_locked_ready_budget_only",
        "budget": "alpha2 <= 2e-9",
        "pass_claim": "blocked_by_missing_MTS_coefficient",
    },
    {
        "runner_row": "preferred_frame_alpha3",
        "after_369": "not separately listed",
        "after_374": "source_locked_ready_budget_only_if_channel_exists",
        "budget": "alpha3 <= 4e-20",
        "pass_claim": "blocked_by_missing_MTS_coefficient_and_channel_relevance",
    },
    {
        "runner_row": "xi_preferred_location_anisotropy",
        "after_369": "quarantined_no_numeric_source_lock",
        "after_374": "source_locked_ready_budget_only",
        "budget": "xi <= 4e-9",
        "pass_claim": "blocked_by_missing_MTS_coefficient",
    },
    {
        "runner_row": "Gdot_over_G",
        "after_369": "not separately listed",
        "after_374": "source_locked_ready_budget_only_if_branch_predicts_Gdot",
        "budget": "|Gdot/G| one-sigma scale 9.6e-15 yr^-1",
        "pass_claim": "blocked_by_missing_MTS_time_variation_map",
    },
    {
        "runner_row": "delta_G_or_fifth_force_yukawa",
        "after_369": "quarantined_no_numeric_source_lock",
        "after_374": "parameterized_source_locked_but_not_scalar_scored",
        "budget": "requires alpha_Y(lambda_Y), not one scalar number",
        "pass_claim": "blocked_by_missing_range_and_coupling_map",
    },
]


QUARANTINE_POLICY = [
    {
        "sector": "preferred_frame_alpha1_alpha2_xi",
        "policy_after_374": "not quarantined for missing external bounds; still budget-only until MTS coefficients exist",
        "allowed_use": "internal guardrail rows",
        "forbidden_use": "claiming preferred-frame or PPN pass",
    },
    {
        "sector": "alpha3_and_Gdot",
        "policy_after_374": "ready only if the MTS branch actually predicts nonconservation/preferred-frame or secular-G channels",
        "allowed_use": "contingent guardrail",
        "forbidden_use": "penalizing the branch for a channel not present in its weak-field map",
    },
    {
        "sector": "fifth_force_yukawa",
        "policy_after_374": "parameterized quarantine: sources exist, but no scalar score until lambda_Y and alpha_Y map are derived",
        "allowed_use": "write the force-law contract and range anchors",
        "forbidden_use": "substituting gamma/beta/WEP or a random proxy as a fifth-force score",
    },
    {
        "sector": "composition_dependent_fifth_force",
        "policy_after_374": "covered first by eta_WEP unless a separate mediator/range law is derived",
        "allowed_use": "link to WEP closure and future species symmetry theorem",
        "forbidden_use": "double-counting eta_WEP and fifth-force rows as independent passes",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Preferred-frame alpha1/alpha2 and xi now have source-locked numeric internal targets, with alpha3 and Gdot/G retained as contingent guardrails. Fifth-force/delta_G is source-locked only as a range-dependent Yukawa contract and remains unscored until MTS derives range and coupling.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "separate Einstein-Hilbert exterior derivation from residual modified-gravity operator testing",
        "pass_condition": "EH operator is derived, or residual operator coefficients are retained and source-bounded",
    },
    {
        "priority": 2,
        "target": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "task": "derive B0i/vector marker no-hair or map alpha1/alpha2 coefficients",
        "pass_condition": "preferred-frame channels are theorem-zero or budgeted against alpha1/alpha2",
    },
    {
        "priority": 3,
        "target": "377-fifth-force-range-coupling-map.md",
        "task": "derive alpha_Y(lambda_Y) or another range/coupling map for radial scalar/bulk-X/phi_C fifth force",
        "pass_condition": "fifth-force row becomes a valid scalar/range score or remains explicitly unscored",
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
    preferred_ready = [
        row
        for row in RESIDUAL_SOURCE_LOCK_MANIFEST
        if str(row["runner_status_after_374"]).startswith("source_locked_ready")
    ]
    fifth_force_rows = [
        row
        for row in RESIDUAL_SOURCE_LOCK_MANIFEST
        if row["residual"] == "delta_G_or_fifth_force_yukawa"
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "external_sources_recorded",
            "status": "pass",
            "evidence": f"{len(EXTERNAL_SOURCES)} external source URLs recorded",
        },
        {
            "gate": "preferred_frame_numeric_source_locked",
            "status": "pass",
            "evidence": "alpha1, alpha2, alpha3, and xi rows loaded from Will PPN table",
        },
        {
            "gate": "Gdot_contingent_guardrail_written",
            "status": "pass",
            "evidence": "PDG 2025 LLR Gdot/G scale retained only if the branch predicts secular G variation",
        },
        {
            "gate": "fifth_force_parameterized",
            "status": "pass" if fifth_force_rows else "fail",
            "evidence": "Yukawa alpha(lambda) contract written; not reduced to one scalar target",
        },
        {
            "gate": "ready_rows_have_missing_coefficients_visible",
            "status": "pass",
            "evidence": f"{len(preferred_ready)} source-locked/contingent rows marked no score because MTS coefficients are missing",
        },
        {
            "gate": "fifth_force_numeric_scored",
            "status": "fail",
            "evidence": "range lambda_Y and coupling alpha_Y are not derived from MTS",
        },
        {
            "gate": "preferred_frame_or_PPN_pass_claimed",
            "status": "fail",
            "evidence": "source locks are internal guardrails only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "WEP closure, phi_C silence, EH exterior, vector no-hair, and fifth-force map remain incomplete",
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
    write_csv(results_dir / "external_source_lock.csv", EXTERNAL_SOURCES)
    write_csv(results_dir / "residual_source_lock_manifest.csv", RESIDUAL_SOURCE_LOCK_MANIFEST)
    write_csv(results_dir / "fifth_force_parameterization.csv", FIFTH_FORCE_PARAMETERIZATION)
    write_csv(results_dir / "MTS_source_map_requirements.csv", MTS_SOURCE_MAP_REQUIREMENTS)
    write_csv(results_dir / "runner_update.csv", RUNNER_UPDATE)
    write_csv(results_dir / "quarantine_policy.csv", QUARANTINE_POLICY)
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
        "external_sources_recorded": len(EXTERNAL_SOURCES),
        "fifth_force_scalar_score_allowed": False,
        "preferred_frame_pass_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 374 fifth-force/preferred-frame source-lock manifest artifacts."
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
