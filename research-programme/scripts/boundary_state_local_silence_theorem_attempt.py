from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-state-local-silence-theorem-attempt"
STATUS = "boundary_state_theorem_not_derived_IR_bath_separation_contract_written"
CLAIM_CEILING = "IR_boundary_bath_selector_contract_no_local_GR_or_Bmem_promotion"


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
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "relative current and conditional local triviality"),
        (ROOT / "292-relative-index-level-theorem-attempt.md", "relative index domain sensitivity"),
        (ROOT / "293-domain-topology-selection-attempt.md", "B3 coherent-domain topology target"),
        (ROOT / "298-open-boundary-parent-sector-attempt.md", "open sector and local silence clauses"),
        (ROOT / "299-local-silence-selector-attempt.md", "selector sufficient conditions and PPN contract"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def spectral_selector_rows() -> list[dict[str, Any]]:
    return [
        {
            "selector_piece": "IR_bath_strength",
            "definition": "b_D = lim_{omega->0+} rho_D(omega)/omega",
            "local_target": "b_D=0",
            "FLRW_target": "b_D>0",
            "what_it_controls": "Gamma_D and N_D in the open sector",
            "status": "clean_selector_contract",
        },
        {
            "selector_piece": "relative_class_norm",
            "definition": "c_D = ||[J_B]_D||",
            "local_target": "c_D=0",
            "FLRW_target": "c_D>0",
            "what_it_controls": "trace source Lambda_D and memory charge",
            "status": "clean_selector_contract",
        },
        {
            "selector_piece": "combined_selector",
            "definition": "sigma_D = Theta(b_D) Theta(c_D)",
            "local_target": "sigma_D=0 if either local factor vanishes",
            "FLRW_target": "sigma_D=1 or nonzero if both factors are active",
            "what_it_controls": "Gamma_D, N_D, Lambda_D together",
            "status": "recommended_selector_contract",
        },
        {
            "selector_piece": "smooth_bound_version",
            "definition": "sigma_D = b_D c_D/(b_D c_D + mu_*^2)",
            "local_target": "sigma_D≈0 when b_D c_D << mu_*^2",
            "FLRW_target": "sigma_D≈1 when b_D c_D >> mu_*^2",
            "what_it_controls": "future numerical local-bound runner",
            "status": "runner_parameterization_not_fundamental",
        },
    ]


def domain_class_rows() -> list[dict[str, Any]]:
    return [
        {
            "domain_class": "local_bound_stationary_domain",
            "boundary_state": "closed or effectively gapped boundary state",
            "relative_class": "target trivial [J_B]=0",
            "IR_bath_prediction": "b_D=0 if no gapless/open boundary bath",
            "selector_result": "sigma_D=0 if relative class also trivial",
            "status": "conditional_silence_target",
            "blocker": "real local systems can radiate/dissipate; parent must define the relevant coarse-grained boundary",
        },
        {
            "domain_class": "FLRW_coherent_domain",
            "boundary_state": "open/horizon-like or coarse-grained cosmological boundary",
            "relative_class": "target nontrivial [J_B]!=0",
            "IR_bath_prediction": "b_D>0 if boundary has gapless bath",
            "selector_result": "sigma_D nonzero",
            "status": "conditional_active_target",
            "blocker": "open bath and nontrivial class not parent-derived",
        },
        {
            "domain_class": "black_hole_or_horizon_local_domain",
            "boundary_state": "local horizon-like bath possible",
            "relative_class": "unknown",
            "IR_bath_prediction": "b_D may be nonzero",
            "selector_result": "dangerous_edge_case",
            "status": "not_silenced_by_simple_bath_rule",
            "blocker": "needs separate local/horizon treatment",
        },
        {
            "domain_class": "laboratory_dissipative_system",
            "boundary_state": "environmental bath exists but not cosmological memory bath",
            "relative_class": "target trivial",
            "IR_bath_prediction": "ordinary dissipation may give nonzero spectral density",
            "selector_result": "safe only if c_D=0 or source coupling ignores non-MTS baths",
            "status": "edge_case_requires_relative_class_filter",
            "blocker": "selector must distinguish ordinary environmental baths from MTS boundary bath",
        },
        {
            "domain_class": "galaxy_or_cluster_bound_domain",
            "boundary_state": "extended but gravitationally bound; may exchange radiation/matter",
            "relative_class": "unknown",
            "IR_bath_prediction": "not automatically zero",
            "selector_result": "cannot declare local silence without bound/test",
            "status": "requires_runner_or_domain_theorem",
            "blocker": "important for not confusing cosmological and galaxy branches",
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_clause": "closed_gapped_boundary_implies_no_open_sector",
            "statement": "If the local boundary state is closed/gapped in the MTS bath channel, then b_D=0 and Gamma_D=N_D=0.",
            "status": "conditional_theorem",
            "proof_status": "standard spectral logic, but MTS bath channel not parent-defined",
            "promotion_blocker": "parent must define rho_D and show local domains are gapped/closed in that channel",
        },
        {
            "theorem_clause": "trivial_relative_class_implies_no_trace_source",
            "statement": "If [J_B]_D=0 and Lambda_D depends on [J_B]_D, then Lambda_D Tr(P_iso q_r)=0.",
            "status": "conditional_theorem",
            "proof_status": "algebraic if source coupling is class-dependent",
            "promotion_blocker": "parent source variation has not forced Lambda_D to depend only on [J_B]",
        },
        {
            "theorem_clause": "FLRW_open_class_remains_active",
            "statement": "If b_D>0 and [J_B]_D nontrivial on the FLRW coherent domain, sigma_D is nonzero.",
            "status": "conditional_theorem",
            "proof_status": "follows from selector definition",
            "promotion_blocker": "FLRW boundary bath and class nontriviality are not derived",
        },
        {
            "theorem_clause": "unified_local_FLRW_separation",
            "statement": "Local silence and FLRW activity follow if local domains are gapped/trivial while FLRW domains are open/nontrivial.",
            "status": "contract_not_derivation",
            "proof_status": "logical separation established",
            "promotion_blocker": "the premise is the missing boundary-state theorem",
        },
    ]


def edge_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "edge_case": "ordinary_environmental_dissipation",
            "risk": "rho_D may be nonzero for non-cosmological baths",
            "needed_fix": "rho_D must be the MTS boundary bath spectral density, not any environmental spectrum",
            "status": "definition_required",
        },
        {
            "edge_case": "black_holes_or_horizons",
            "risk": "local horizon-like boundaries may have gapless baths",
            "needed_fix": "separate theorem showing no dangerous MTS trace source or bounded local residual",
            "status": "requires_future_branch",
        },
        {
            "edge_case": "galaxy_bound_systems",
            "risk": "galaxies are bound but not laboratory-local; selector may be neither zero nor FLRW-like",
            "needed_fix": "do not use local silence theorem to erase galaxy phenomenology without a domain rule",
            "status": "keep_separate_from_galaxy_branch",
        },
        {
            "edge_case": "time_dependent_local_systems",
            "risk": "radiating systems can have low-frequency spectra",
            "needed_fix": "local-bound runner must test residual epsilon_loc if sigma_D is not exactly zero",
            "status": "runner_needed",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited checkpoints exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "IR_bath_selector_defined",
            "status": "pass",
            "evidence": "b_D=lim rho_D(omega)/omega and c_D=||[J_B]_D|| define sigma_D",
            "claim_effect": "boundary-state theorem target made precise",
        },
        {
            "gate": "local_closed_gapped_implies_silence",
            "status": "conditional_pass",
            "evidence": "if b_D=0 and/or c_D=0 then sigma_D=0 and open-sector local source vanishes",
            "claim_effect": "exact sufficient condition retained",
        },
        {
            "gate": "FLRW_open_nontrivial_implies_active",
            "status": "conditional_pass",
            "evidence": "if b_D>0 and c_D>0 then sigma_D nonzero",
            "claim_effect": "selector does not automatically kill cosmology",
        },
        {
            "gate": "boundary_state_parent_derived",
            "status": "fail",
            "evidence": "no parent proof that local domains are closed/gapped/trivial and FLRW domains open/nontrivial",
            "claim_effect": "local silence not promoted",
        },
        {
            "gate": "edge_cases_closed",
            "status": "fail",
            "evidence": "ordinary dissipation, horizons, galaxies, and time-dependent local systems remain edge cases",
            "claim_effect": "needs runner or further theorem",
        },
        {
            "gate": "PPN_bound_verified",
            "status": "fail",
            "evidence": "no epsilon_loc bound run performed",
            "claim_effect": "no local-GR claim",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "boundary-state theorem remains conditional and amplitude stack remains closure-labelled",
            "claim_effect": "2/27 not promoted",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "local_bound_runner_for_epsilon_loc",
            "task": "implement a symbolic/numeric gate that maps sigma_D, Lambda_open, and trace charge to epsilon_loc and PPN residual coefficients",
            "success_gate": "either sigma_D=0 exactly or residuals are below manifest bounds",
        },
        {
            "priority": 2,
            "target": "parent_define_MTS_bath_channel",
            "task": "define rho_D as a specific MTS boundary spectral density, not generic environmental dissipation",
            "success_gate": "ordinary local baths do not accidentally activate sigma_D",
        },
        {
            "priority": 3,
            "target": "edge_case_black_hole_local_branch",
            "task": "separate horizon-like local domains from FLRW coherent domains",
            "success_gate": "horizon baths do not create excluded local PPN/fifth-force effects",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The boundary-state theorem is not derived, but the correct theorem target is now precise: local silence "
                "requires the MTS boundary bath IR strength b_D and/or the relative class norm c_D to vanish locally, while "
                "FLRW activity requires both to be nonzero. This gives an exact separation criterion if true, but the parent "
                "theory has not proved the local/FLRW boundary-state split and several edge cases remain."
            ),
            "next_target": "local_bound_runner_for_epsilon_loc",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "spectral_selector.csv": (
            spectral_selector_rows(),
            ["selector_piece", "definition", "local_target", "FLRW_target", "what_it_controls", "status"],
        ),
        "domain_class_tests.csv": (
            domain_class_rows(),
            ["domain_class", "boundary_state", "relative_class", "IR_bath_prediction", "selector_result", "status", "blocker"],
        ),
        "theorem_attempts.csv": (
            theorem_attempt_rows(),
            ["theorem_clause", "statement", "status", "proof_status", "promotion_blocker"],
        ),
        "edge_cases.csv": (
            edge_case_rows(),
            ["edge_case", "risk", "needed_fix", "status"],
        ),
        "promotion_gates.csv": (
            promotion_gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "next_targets.csv": (
            next_target_rows(),
            ["priority", "target", "task", "success_gate"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "IR_boundary_selector_defined": True,
        "boundary_state_parent_derived_now": False,
        "PPN_bound_verified_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "local_bound_runner_for_epsilon_loc",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Boundary-state local silence theorem attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
