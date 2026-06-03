from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "selector-parent-theorem-attempt"
STATUS = "selector_parent_theorem_conditional_spectral_topological_route_not_parent_closed"
CLAIM_CEILING = "conditional_selector_theorem_no_local_GR_or_PPN_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "299-local-silence-selector-attempt.md", "exact selector sufficient condition"),
        (ROOT / "300-boundary-state-local-silence-theorem-attempt.md", "IR boundary-state selector target"),
        (ROOT / "307-local-branch-status-ledger-and-pivot.md", "local branch ledger and theorem target"),
        (ROOT / "runs" / "20260601-000122-local-silence-selector-attempt" / "results" / "promotion_gates.csv", "selector gate evidence"),
        (ROOT / "runs" / "20260601-000123-boundary-state-local-silence-theorem-attempt" / "results" / "promotion_gates.csv", "boundary-state gate evidence"),
        (ROOT / "runs" / "20260601-000130-local-branch-status-ledger" / "results" / "next_targets.csv", "selector parent theorem target"),
        (ROOT / "scripts" / "selector_parent_theorem_attempt.py", "this selector theorem runner"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def theorem_definition_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "MTS_projected_boundary_bath",
            "symbol": "rho_MTS,D(omega)",
            "definition": "spectral density after projecting out ordinary environmental/EM/matter baths",
            "role": "prevents generic local dissipation from accidentally activating the MTS open sector",
            "status": "required_parent_definition",
        },
        {
            "object": "IR_bath_strength",
            "symbol": "b_D = lim_{omega->0+} rho_MTS,D(omega)/omega",
            "definition": "Ohmic IR strength of the MTS boundary bath",
            "role": "sets dissipative/noise activation in the open sector",
            "status": "selector_factor",
        },
        {
            "object": "relative_boundary_class",
            "symbol": "c_D = ||Pi_rel[J_B]_D||",
            "definition": "norm of the non-exact relative boundary-current/memory class",
            "role": "sets whether the trace-source coupling has a nontrivial memory charge to act on",
            "status": "selector_factor",
        },
        {
            "object": "hard_selector",
            "symbol": "sigma_D = Theta(b_D) Theta(c_D)",
            "definition": "exact silence if either projected bath strength or relative class vanishes",
            "role": "mathematical local silence route",
            "status": "useful_for_theorem_statement",
        },
        {
            "object": "smooth_selector",
            "symbol": "sigma_D = b_D c_D/(b_D c_D + mu_*^2)",
            "definition": "small nonzero selector for quantitative local-bound runners",
            "role": "useful if exact step selector is too sharp for numerical/regularity work",
            "status": "runner_version",
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "projected_bath_contract",
            "parent_statement": "rho_MTS,D is computed from the MTS boundary operator only, not from ordinary EM/matter environmental spectra",
            "mathematical_form": "rho_MTS,D(omega)=rho[P_MTS B_D,P_MTS B_D](omega)",
            "why_needed": "otherwise every warm local lab activates sigma_D",
            "status": "not_parent_derived",
        },
        {
            "contract": "local_gap_contract",
            "parent_statement": "stationary laboratory-local domains are closed/gapped in the projected MTS boundary channel",
            "mathematical_form": "exists omega_gap>0 with rho_MTS,D(omega)=0 for 0<omega<omega_gap",
            "why_needed": "implies b_D=0 and exact local selector silence",
            "status": "conditional_sufficient",
        },
        {
            "contract": "local_relative_triviality_contract",
            "parent_statement": "local bound domains have exact relative boundary-current class",
            "mathematical_form": "Pi_rel[J_B]_D=0 or [J_B]_D=d_A chi with no boundary flux",
            "why_needed": "implies c_D=0 and kills trace-source memory activation",
            "status": "conditional_sufficient",
        },
        {
            "contract": "FLRW_ohmic_contract",
            "parent_statement": "the coherent FLRW domain has an open/gapless MTS boundary bath",
            "mathematical_form": "rho_MTS,FLRW(omega)=eta omega + o(omega), eta>0",
            "why_needed": "gives b_FLRW=eta>0 so cosmology is not silenced",
            "status": "not_parent_derived",
        },
        {
            "contract": "FLRW_relative_nontriviality_contract",
            "parent_statement": "the coherent FLRW domain carries a non-exact relative boundary-current/memory class",
            "mathematical_form": "||Pi_rel[J_B]_FLRW||>0",
            "why_needed": "gives c_FLRW>0 so the memory/trace-source branch can activate",
            "status": "not_parent_derived",
        },
    ]


def conditional_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "claim": "gapped projected local bath implies b_D=0",
            "argument": "if rho_MTS,D(omega)=0 on an interval 0<omega<omega_gap, then lim rho/omega=0",
            "result": "b_local=0",
            "proof_status": "proved_from_contract",
        },
        {
            "step": 2,
            "claim": "relative-trivial local class implies c_D=0",
            "argument": "the relative projector kills exact/no-flux boundary currents",
            "result": "c_local=0",
            "proof_status": "proved_from_contract",
        },
        {
            "step": 3,
            "claim": "either local factor zero implies sigma_D=0",
            "argument": "Theta(b_D)Theta(c_D)=0 if b_D=0 or c_D=0",
            "result": "Gamma_D=N_D=Lambda_D=0 in the selector-controlled open sector",
            "proof_status": "proved_from_selector_definition",
        },
        {
            "step": 4,
            "claim": "Ohmic FLRW bath implies b_FLRW>0",
            "argument": "rho_MTS,FLRW(omega)=eta omega+o(omega) gives lim rho/omega=eta",
            "result": "b_FLRW=eta>0",
            "proof_status": "proved_from_contract",
        },
        {
            "step": 5,
            "claim": "nontrivial FLRW relative class implies c_FLRW>0",
            "argument": "the projected relative norm is positive by the nontriviality premise",
            "result": "c_FLRW>0",
            "proof_status": "proved_from_contract",
        },
        {
            "step": 6,
            "claim": "FLRW factors positive imply sigma_FLRW nonzero",
            "argument": "Theta(b_FLRW)Theta(c_FLRW)=1 or smooth selector gives positive b c/(b c+mu_*^2)",
            "result": "cosmological branch can remain active",
            "proof_status": "proved_from_selector_definition",
        },
    ]


def domain_test_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "domain": "stationary_lab_local_domain",
            "projected_bath": "gapped_or_closed",
            "relative_class": "trivial",
            "b_value": 0.0,
            "c_value": 0.0,
            "ordinary_bath_present": "possible_but_projected_out",
            "interpretation": "clean exact local silence case",
        },
        {
            "domain": "ordinary_warm_lab_with_EM_bath",
            "projected_bath": "zero_if_projection_is_correct",
            "relative_class": "trivial",
            "b_value": 0.0,
            "c_value": 0.0,
            "ordinary_bath_present": "yes",
            "interpretation": "passes only if rho_MTS excludes generic EM/environmental spectra",
        },
        {
            "domain": "time_dependent_radiating_local_system",
            "projected_bath": "uncertain_low_frequency_tail",
            "relative_class": "trivial_or_small",
            "b_value": 0.02,
            "c_value": 0.0,
            "ordinary_bath_present": "yes",
            "interpretation": "hard selector stays silent if c_D=0, smooth leakage needs runner",
        },
        {
            "domain": "local_horizon_or_black_hole_edge",
            "projected_bath": "gapless_possible",
            "relative_class": "possibly_nontrivial",
            "b_value": 0.7,
            "c_value": 0.6,
            "ordinary_bath_present": "horizon_bath",
            "interpretation": "danger edge case, not covered by lab-local silence theorem",
        },
        {
            "domain": "galaxy_or_cluster_extended_bound_domain",
            "projected_bath": "mixed_or_coarse_grained",
            "relative_class": "possibly_nontrivial",
            "b_value": 0.3,
            "c_value": 0.5,
            "ordinary_bath_present": "astrophysical",
            "interpretation": "must not be erased by laboratory local-silence theorem",
        },
        {
            "domain": "FLRW_coherent_domain",
            "projected_bath": "ohmic_open",
            "relative_class": "nontrivial",
            "b_value": 1.0,
            "c_value": 1.0,
            "ordinary_bath_present": "not_the_relevant_variable",
            "interpretation": "cosmological branch active if parent owns the FLRW contracts",
        },
    ]
    rows: list[dict[str, Any]] = []
    mu_sq = 0.1
    for case in cases:
        b_value = float(case["b_value"])
        c_value = float(case["c_value"])
        hard_sigma = 1.0 if b_value > 0.0 and c_value > 0.0 else 0.0
        smooth_sigma = 0.0 if b_value * c_value == 0.0 else (b_value * c_value) / (b_value * c_value + mu_sq)
        if case["domain"] == "FLRW_coherent_domain" and hard_sigma > 0.0:
            status = "active_if_contracts_derived"
        elif case["domain"] in {"local_horizon_or_black_hole_edge", "galaxy_or_cluster_extended_bound_domain"} and hard_sigma > 0.0:
            status = "defer_edge_case"
        elif hard_sigma == 0.0:
            status = "silent_under_selector"
        else:
            status = "unsafe"
        rows.append(
            {
                **case,
                "hard_sigma": hard_sigma,
                "smooth_sigma_mu_sq_0p1": smooth_sigma,
                "status": status,
            }
        )
    return rows


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "generic local dissipation can define b_D",
            "result": "fail",
            "reason": "ordinary warm systems have environmental/EM baths and would activate the selector",
            "repair": "rho_D must be MTS-projected",
        },
        {
            "claim": "local boundedness alone implies b_D=0",
            "result": "fail",
            "reason": "bound systems can radiate, dissipate, or contain gapless ordinary fields",
            "repair": "need projected closed/gapped boundary-channel theorem",
        },
        {
            "claim": "relative triviality alone protects all local systems",
            "result": "partial",
            "reason": "it kills trace-source memory activation but does not by itself define the bath/noise channel",
            "repair": "use the product selector or prove a shared projector",
        },
        {
            "claim": "FLRW activity follows from nonzero H alone",
            "result": "fail",
            "reason": "a curvature/expansion scalar is not the same as an MTS boundary spectral density and class",
            "repair": "derive the horizon/coherent-domain boundary bath and relative class",
        },
        {
            "claim": "the selector theorem can cover black holes and galaxies automatically",
            "result": "fail",
            "reason": "horizons and extended bound systems can have nontrivial boundary states",
            "repair": "keep separate edge branches and empirical gates",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited selector checkpoints/runs/scripts exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "selector_objects_defined",
            "status": "pass",
            "evidence": "rho_MTS,D, b_D, c_D, hard and smooth sigma_D are explicit",
            "claim_effect": "the theorem target is mathematically well-posed",
        },
        {
            "gate": "conditional_local_silence_proved",
            "status": "conditional_pass",
            "evidence": "projected local gap and/or relative triviality imply sigma_D=0",
            "claim_effect": "exact local silence follows if the parent contracts hold",
        },
        {
            "gate": "conditional_FLRW_activity_proved",
            "status": "conditional_pass",
            "evidence": "Ohmic projected bath plus nontrivial relative class imply sigma_FLRW nonzero",
            "claim_effect": "the selector can spare cosmology if FLRW contracts hold",
        },
        {
            "gate": "generic_bath_problem_closed",
            "status": "fail",
            "evidence": "ordinary local EM/environmental baths would activate an unprojected selector",
            "claim_effect": "rho_D must be MTS-projected before promotion",
        },
        {
            "gate": "local_gap_parent_derived",
            "status": "fail",
            "evidence": "no parent theorem proves local domains are gapped/closed in the MTS boundary channel",
            "claim_effect": "local silence not parent-owned",
        },
        {
            "gate": "local_relative_triviality_parent_derived",
            "status": "fail",
            "evidence": "no parent theorem proves Pi_rel[J_B]_local=0",
            "claim_effect": "trace-source local silence not parent-owned",
        },
        {
            "gate": "FLRW_ohmic_bath_parent_derived",
            "status": "fail",
            "evidence": "no derivation of rho_MTS,FLRW(omega)=eta omega+o(omega)",
            "claim_effect": "cosmological activity remains a contract",
        },
        {
            "gate": "FLRW_relative_class_parent_derived",
            "status": "fail",
            "evidence": "no derivation of nonzero FLRW relative boundary-current class",
            "claim_effect": "cosmological memory activation remains a contract",
        },
        {
            "gate": "edge_cases_closed",
            "status": "fail",
            "evidence": "horizons, galaxies, and time-dependent local systems remain separate domains",
            "claim_effect": "no blanket local-GR theorem",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "selector parent theorem remains conditional",
            "claim_effect": "local branch remains theorem target/effective closure",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "selector theorem does not derive global 2/27 amplitude",
            "claim_effect": "B_mem remains empirical closure/theorem target",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "MTS_projector_definition",
            "task": "define P_MTS B_D so rho_MTS,D excludes ordinary EM/matter/environmental baths",
            "success_gate": "ordinary warm local domains have b_D=0 unless the MTS-specific boundary channel is active",
        },
        {
            "priority": 2,
            "target": "local_gap_or_relative_triviality_theorem",
            "task": "derive either rho_MTS,D(omega)=0 near omega=0 or Pi_rel[J_B]_D=0 for laboratory-local domains",
            "success_gate": "sigma_D=0 follows without manual selector closure",
        },
        {
            "priority": 3,
            "target": "FLRW_boundary_bath_theorem",
            "task": "derive an Ohmic/gapless projected bath and nontrivial relative class for the coherent FLRW domain",
            "success_gate": "cosmology remains active by theorem, not by selector assumption",
        },
        {
            "priority": 4,
            "target": "edge_domain_manifest",
            "task": "separate lab-local, horizon-local, galaxy/cluster, and FLRW domains before making local claims",
            "success_gate": "the local silence theorem does not erase galaxy phenomenology or mishandle horizons",
        },
        {
            "priority": 5,
            "target": "empirical_holdout_pivot",
            "task": "return to strict empirical holdout testing while the selector theorem remains conditional",
            "success_gate": "MTS branches stay competitive without using the unresolved local theorem as evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "decision": "selector theorem has a clean spectral/topological route but is not parent-closed",
            "recommended_next": "define the MTS boundary projector or pivot to empirical holdout testing",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    outputs = {
        "source_register": source_register_rows(),
        "theorem_definitions": theorem_definition_rows(),
        "parent_contracts": parent_contract_rows(),
        "conditional_proof": conditional_proof_rows(),
        "domain_tests": domain_test_rows(),
        "no_go_tests": no_go_rows(),
        "promotion_gates": promotion_gate_rows(),
        "next_targets": next_target_rows(),
        "decision": decision_rows(),
    }

    write_csv(results_dir / "source_register.csv", outputs["source_register"], ["source", "role", "exists"])
    write_csv(
        results_dir / "theorem_definitions.csv",
        outputs["theorem_definitions"],
        ["object", "symbol", "definition", "role", "status"],
    )
    write_csv(
        results_dir / "parent_contracts.csv",
        outputs["parent_contracts"],
        ["contract", "parent_statement", "mathematical_form", "why_needed", "status"],
    )
    write_csv(
        results_dir / "conditional_proof.csv",
        outputs["conditional_proof"],
        ["step", "claim", "argument", "result", "proof_status"],
    )
    write_csv(
        results_dir / "domain_tests.csv",
        outputs["domain_tests"],
        [
            "domain",
            "projected_bath",
            "relative_class",
            "b_value",
            "c_value",
            "ordinary_bath_present",
            "interpretation",
            "hard_sigma",
            "smooth_sigma_mu_sq_0p1",
            "status",
        ],
    )
    write_csv(results_dir / "no_go_tests.csv", outputs["no_go_tests"], ["claim", "result", "reason", "repair"])
    write_csv(results_dir / "promotion_gates.csv", outputs["promotion_gates"], ["gate", "status", "evidence", "claim_effect"])
    write_csv(results_dir / "next_targets.csv", outputs["next_targets"], ["priority", "target", "task", "success_gate"])
    write_csv(results_dir / "decision.csv", outputs["decision"], ["status", "claim_ceiling", "decision", "recommended_next"])

    payload = {
        "run_slug": RUN_SLUG,
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": relpath(run_dir),
        "outputs": {name: len(rows) for name, rows in outputs.items()},
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Attempt the selector parent theorem via spectral/topological contracts.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
