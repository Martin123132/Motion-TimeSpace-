from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "universal-matter-coupling-theorem-attempt"
STATUS = "universal_matter_coupling_conditional_theorem_sharpened_direct_WEP_clock_vertices_zero_parent_selector_open"
CLAIM_CEILING = "conditional_universal_coupling_theorem_only_no_WEP_clock_PPN_or_local_GR_pass"
NEXT_TARGET = "361-residual-gauge-principle-for-projected-matter-metric.md"

RUN_359 = ROOT / "runs" / "20260601-190000-source-locked-PPN-residual-runner-from-derived-force-ledger"


SOURCE_DOCS = [
    {
        "path": "204-matter-metric-action-and-ruler-transport-owner-contract.md",
        "role": "matter metric action and dust-label/ruler transport owner",
    },
    {
        "path": "240-universal-coupling-parent-contract-or-local-bound-data-runner.md",
        "role": "earlier N3 universal coframe contract and forbidden vertices",
    },
    {
        "path": "268-projected-matter-metric-parent-action-or-closure.md",
        "role": "projected matter metric action skeleton that removes Cperp source",
    },
    {
        "path": "269-metric-selector-principle-attempt.md",
        "role": "conditional selector theorem from residual gauge invariance",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "local pressure runner identifying WEP/universal coupling as top priority",
    },
    {
        "path": "runs/20260601-190000-source-locked-PPN-residual-runner-from-derived-force-ledger/results/pressure_ranking.csv",
        "role": "source-locked local pressure ranking",
    },
]


THEOREM_AXIOMS = [
    {
        "axiom": "U1_one_observed_coframe",
        "statement": "there exists one observed coframe ehat^a_mu defining ghat_munu for all matter, clocks, rods, photons, and lab standards",
        "status": "contract",
        "if_missing": "no single GR geometry for observables; WEP/clock residuals remain",
    },
    {
        "axiom": "U2_no_direct_MTS_arguments",
        "statement": "S_matter = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A] at fixed ehat, with no direct X/J_rel/V_def/P_D/Cperp/species charge arguments",
        "status": "conditional_action_theorem",
        "if_missing": "species-dependent MTS vertices generate WEP/fifth-force/clock residuals",
    },
    {
        "axiom": "U3_residual_representative_invariance",
        "statement": "matter is invariant under Cperp -> Cperp + eta_perp where P_D eta_perp = 0",
        "status": "not_parent_derived",
        "if_missing": "projected matter metric remains effective closure rather than theorem",
    },
    {
        "axiom": "U4_projected_metric_selector",
        "statement": "matter metric uses ghat_munu = exp(P_D C) g_munu, or equivalent ehat = exp(P_D C/2) e",
        "status": "conditional_on_U3",
        "if_missing": "ordinary exp(C)g sources Cperp through matter trace",
    },
    {
        "axiom": "U5_no_species_specific_compensation",
        "statement": "no species A has its own Weyl factor, charge, mass function, EM coupling function, or clock/ruler map depending on MTS fields",
        "status": "required_selection_rule",
        "if_missing": "composition dependence returns even if a common metric exists for part of the sector",
    },
    {
        "axiom": "U6_owned_selector_stress",
        "statement": "projector/domain/selector stresses used to define P_D C are varied and retained in the Ward ledger",
        "status": "conditional_from_356_357",
        "if_missing": "universal coupling is bought by fake conservation",
    },
    {
        "axiom": "U7_common_mode_local_silence",
        "statement": "the common projected factor P_D C is locally constant/screened/common-mode enough not to create redshift or clock drift residuals",
        "status": "open",
        "if_missing": "WEP may be safe but clock/redshift/common-mode drift remains",
    },
]


MATTER_ACTION_CONTRACT = [
    {
        "object": "observed_coframe",
        "symbol": "ehat^a_mu",
        "definition": "single physical coframe seen by all local matter and measurement standards",
        "allowed_dependence": "may be constructed from parent fields only through a universal selector",
        "forbidden_dependence": "species-specific ehat_A or direct nonmetric charge",
    },
    {
        "object": "observed_metric",
        "symbol": "ghat_munu = eta_ab ehat^a_mu ehat^b_nu",
        "definition": "metric entering local matter action, clocks, rulers, and photon propagation",
        "allowed_dependence": "candidate branch ghat_munu = exp(P_D C) g_munu",
        "forbidden_dependence": "raw exp(C)g if Cperp is a physical local matter source",
    },
    {
        "object": "matter_action",
        "symbol": "S_matter = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A]",
        "definition": "universal metric/coframe coupling with species constants independent of MTS local fields",
        "allowed_dependence": "standard model fields and one observed geometry",
        "forbidden_dependence": "m_A(Z), alpha_EM(Z), q_A X_mu J_A^mu, lambda_A V_def O_A",
    },
    {
        "object": "selector_action",
        "symbol": "S_selector[C, C_D, Cperp, P_D, C_m, ghat]",
        "definition": "auxiliary/constraint skeleton selecting projected matter scalar C_m=P_D C",
        "allowed_dependence": "must be included in parent variation and Ward ledger",
        "forbidden_dependence": "fixed nonvaried nonlocal projector chosen by hand",
    },
]


FORBIDDEN_VERTICES = [
    {
        "vertex": "m_A(Z)",
        "residual": "eta_WEP",
        "why_forbidden": "species masses depending on MTS fields create composition-dependent free fall",
    },
    {
        "vertex": "alpha_EM(Z) or f_A(Z) F^2",
        "residual": "alpha_clock_redshift; eta_WEP",
        "why_forbidden": "spectroscopy and clocks become direct probes of MTS fields",
    },
    {
        "vertex": "q_A X_mu J_A^mu",
        "residual": "eta_WEP; delta_G_or_fifth_force",
        "why_forbidden": "species current charge produces a fifth force",
    },
    {
        "vertex": "lambda_A V_def O_A",
        "residual": "eta_WEP; beta_minus_1",
        "why_forbidden": "defect/load field directly talks to matter outside geometry",
    },
    {
        "vertex": "species_specific_metric ghat_A",
        "residual": "eta_WEP; alpha_clock_redshift; gamma_minus_1",
        "why_forbidden": "different species measure different geometries",
    },
    {
        "vertex": "raw Cperp matter trace source",
        "residual": "eta_WEP; alpha_clock_redshift; gamma_minus_1",
        "why_forbidden": "ordinary exp(C)g couples matter trace to local residual representative",
    },
]


VARIATION_RESULTS = [
    {
        "variation": "delta S_matter / delta Z_I at fixed ehat",
        "result_if_axioms_hold": "0 for every non-geometric MTS variable Z_I",
        "residual_removed": "direct WEP/clock/fifth-force vertices",
        "status": "conditional_exact",
    },
    {
        "variation": "delta S_matter / delta Cperp for projected metric exp(P_D C)g",
        "result_if_axioms_hold": "0",
        "residual_removed": "raw local Cperp trace-source residual",
        "status": "conditional_exact",
    },
    {
        "variation": "delta S_matter / delta C for ordinary exp(C)g",
        "result_if_axioms_hold": "1/2 sqrt(-ghat) T_hat",
        "residual_removed": "none; this is the rejected/open trace-source hazard",
        "status": "hazard_if_raw_C_metric_used",
    },
    {
        "variation": "diffeomorphism Ward identity for matter",
        "result_if_axioms_hold": "nabla_hat_mu T_hat^mu_nu = 0 on matter shell",
        "residual_removed": "nonmetric force term in matter conservation",
        "status": "conditional_exact",
    },
    {
        "variation": "selector/projector/domain variation",
        "result_if_axioms_hold": "retained in parent Ward ledger, not dropped",
        "residual_removed": "fake conservation risk only if selector stress closes",
        "status": "conditional_open",
    },
]


RESIDUAL_UPDATE = [
    {
        "residual": "eta_WEP",
        "source_locked_scale_abs": 2.8e-15,
        "before_360_status": "hardest ready guardrail; universal coupling debt open",
        "after_360_status": "direct species-dependent vertices conditionally zero if U1-U6 hold",
        "still_open": "parent derivation of U1/U3/U5 and proof no hidden species-specific selector remains",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale_abs": 3.1e-5,
        "before_360_status": "clock/redshift residual retained",
        "after_360_status": "direct clock-sector MTS vertices conditionally zero under one observed coframe",
        "still_open": "common-mode P_D C drift/local redshift silence U7 not derived",
    },
    {
        "residual": "gamma_minus_1",
        "source_locked_scale_abs": 2.3e-5,
        "before_360_status": "nonmetric light/matter mismatch can feed gamma",
        "after_360_status": "matter/photon geometry mismatch conditionally removed if photons share ehat",
        "still_open": "trace-free/boundary/operator residuals remain separate",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "source_locked_scale_abs": "",
        "before_360_status": "quarantined",
        "after_360_status": "direct species-charge fifth force conditionally forbidden",
        "still_open": "bulk X/radial/domain fifth-force sectors remain quarantined",
    },
]


SELECTOR_ROUTE_STATUS = [
    {
        "route": "minimal_metric_postulate",
        "claim": "parent theory simply postulates all matter sees one ehat",
        "status": "closure_if_standalone",
        "risk": "works phenomenologically but does not derive universal coupling from MTS",
    },
    {
        "route": "residual_gauge_invariance",
        "claim": "Cperp is representative/gauge and matter must be invariant under Cperp shifts",
        "status": "best_conditional_route",
        "risk": "requires parent first-class/gauge/cohomology theorem",
    },
    {
        "route": "relative_cohomology_class",
        "claim": "matter couples only to the relative class P_D C, not exact local representative Cperp",
        "status": "supporting_conditional_route",
        "risk": "must show local microcausality/domain projection is constraint-safe",
    },
    {
        "route": "boundary_clock_normalization",
        "claim": "local clocks are normalized to boundary/domain time represented by P_D C",
        "status": "plausible_side_route",
        "risk": "clock/redshift drift U7 remains",
    },
    {
        "route": "raw_exp_C_metric",
        "claim": "matter sees exp(C)g directly",
        "status": "rejected_as_lead",
        "risk": "sources Cperp and reopens local WEP/clock/gamma pressure",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive Cperp as residual gauge/exact representative so exp(P_D C)g is selected before empirical scoring",
        "pass_condition": "P_D C is the unique gauge-invariant matter scalar in the coherent limit",
    },
    {
        "priority": 2,
        "target": "362-common-mode-clock-redshift-silence-for-projected-metric.md",
        "task": "derive or bound local drift/gradient of the common projected matter factor P_D C",
        "pass_condition": "alpha_clock_redshift residual is zero or below source-locked guardrail with coefficients",
    },
    {
        "priority": 3,
        "target": "363-WEP-clock-residual-coefficient-map-after-universal-coupling.md",
        "task": "update the source-locked runner with conditional zero vertices and remaining common-mode residuals",
        "pass_condition": "direct WEP vertices removed conditionally while open residuals stay explicit",
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
    for doc in SOURCE_DOCS:
        source_path = ROOT / doc["path"]
        rows.append(
            {
                "source_file": doc["path"],
                "exists": source_path.exists(),
                "role": doc["role"],
            }
        )
    return rows


def pressure_context_rows() -> list[dict[str, Any]]:
    pressure_path = RUN_359 / "results" / "pressure_ranking.csv"
    if not pressure_path.exists():
        return [
            {
                "pressure_rank": "missing",
                "residual": "missing",
                "source_locked_scale_abs": "",
                "context": "checkpoint 359 pressure ranking missing",
            }
        ]
    with pressure_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = []
        for row in csv.DictReader(handle):
            if row["residual"] in {"eta_WEP", "alpha_clock_redshift", "gamma_minus_1"}:
                rows.append(
                    {
                        "pressure_rank": row["pressure_rank"],
                        "residual": row["residual"],
                        "source_locked_scale_abs": row["source_locked_scale_abs"],
                        "context": row["why_it_matters"],
                    }
                )
        return rows


def gate_result_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["source_file"] for row in source_rows if not row["exists"]]
    open_axioms = sum(1 for row in THEOREM_AXIOMS if row["status"] in {"not_parent_derived", "open", "required_selection_rule", "contract"})
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited source files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "universal_action_contract_written",
            "status": "pass",
            "evidence": "single observed coframe matter action and forbidden vertices listed",
        },
        {
            "gate": "direct_WEP_clock_vertices_zero_conditionally",
            "status": "conditional_pass",
            "evidence": "if matter has no direct MTS arguments at fixed ehat, delta S_matter/delta Z_I = 0",
        },
        {
            "gate": "projected_metric_Cperp_source_removed_conditionally",
            "status": "conditional_pass",
            "evidence": "if ghat=exp(P_D C)g, delta S_matter/delta Cperp=0",
        },
        {
            "gate": "parent_selector_principle_derived",
            "status": "fail",
            "evidence": "residual gauge/cohomology principle for Cperp remains open",
        },
        {
            "gate": "common_mode_clock_silence_derived",
            "status": "fail",
            "evidence": "local drift/gradient of P_D C not derived or bounded with coefficients",
        },
        {
            "gate": "universal_coupling_promoted",
            "status": "fail",
            "evidence": f"{open_axioms} theorem axioms remain contract/open/not parent-derived",
        },
        {
            "gate": "WEP_or_clock_pass_claimed",
            "status": "fail",
            "evidence": "conditional zero of direct vertices is not an observational pass",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "EH/nohair/operator/source-normalization gates remain open",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "direct_WEP_clock_vertices": "conditionally_zero",
            "projected_metric_selector": "conditional_not_parent_derived",
            "WEP_pass_claimed": False,
            "clock_pass_claimed": False,
            "local_GR_promoted": False,
            "main_result": "universal matter coupling can kill direct species/clock vertices by action structure if one observed coframe and projected metric selector are parent-derived",
            "next_target": NEXT_TARGET,
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    run_dir = ROOT / "runs" / f"{args.timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    outputs = {
        "source_register.csv": source_rows,
        "pressure_context.csv": pressure_context_rows(),
        "theorem_axioms.csv": THEOREM_AXIOMS,
        "matter_action_contract.csv": MATTER_ACTION_CONTRACT,
        "forbidden_vertices.csv": FORBIDDEN_VERTICES,
        "variation_results.csv": VARIATION_RESULTS,
        "residual_update.csv": RESIDUAL_UPDATE,
        "selector_route_status.csv": SELECTOR_ROUTE_STATUS,
        "next_queue.csv": NEXT_QUEUE,
        "gate_results.csv": gate_result_rows(source_rows),
        "decision.csv": decision_rows(),
    }
    for name, rows in outputs.items():
        write_csv(results_dir / name, rows)

    status = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "generated": sorted(outputs),
        "source_paths_missing": sum(1 for row in source_rows if not row["exists"]),
        "theorem_axioms": len(THEOREM_AXIOMS),
        "forbidden_vertices": len(FORBIDDEN_VERTICES),
        "direct_WEP_clock_vertices": "conditionally_zero",
        "projected_metric_selector_parent_derived": False,
        "common_mode_clock_silence_derived": False,
        "WEP_pass_claimed": False,
        "clock_pass_claimed": False,
        "local_GR_promoted": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
