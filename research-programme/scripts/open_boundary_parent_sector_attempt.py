from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "open-boundary-parent-sector-attempt"
STATUS = "open_boundary_sector_constructed_positive_arrow_and_trace_conditional_local_silence_not_derived"
CLAIM_CEILING = "effective_open_sector_contract_no_full_parent_amplitude_or_local_GR_promotion"


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
        (ROOT / "292-relative-index-level-theorem-attempt.md", "conditional k=9 relative index"),
        (ROOT / "293-domain-topology-selection-attempt.md", "conditional B3 topology route"),
        (ROOT / "294-endpoint-occupancy-arrow-law-attempt.md", "projector-rank endpoint law"),
        (ROOT / "295-arrow-semigroup-parent-time-attempt.md", "semigroup/H-theorem arrow"),
        (ROOT / "296-positive-coarse-graining-parent-action-attempt.md", "open/Onsager parent-time contract"),
        (ROOT / "297-two-over-27-derivation-stack-ledger.md", "2/27 closure ledger and next target"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def action_terms_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "resolved_axis_field",
            "symbol": "q_r",
            "form": "q_r in A=span{E_11,E_22,E_33}",
            "role": "resolved diagonal axis-load memory variable",
            "status": "effective_field_defined",
        },
        {
            "term": "response_field",
            "symbol": "q_a",
            "form": "q_a multiplies dot(q_r)+Gamma_D R_aniso q_r",
            "role": "Schwinger-Keldysh/response field enforcing dissipative equation",
            "status": "effective_contract",
        },
        {
            "term": "anisotropic_projector",
            "symbol": "R_aniso",
            "form": "R_aniso=I-P_iso, P_iso=(1/3)11^T",
            "role": "two-dimensional residual projector whose rank is Delta n=2",
            "status": "derived_kinematic_projector",
        },
        {
            "term": "dissipative_kernel",
            "symbol": "Gamma_D",
            "form": "Gamma_D=R_aniso M_D R_aniso with M_D positive semidefinite",
            "role": "positive mobility on non-scalar residual modes",
            "status": "conditional_positive_if_M_D_parent_owned",
        },
        {
            "term": "noise_kernel",
            "symbol": "N_D",
            "form": "N_D=2 T_D Gamma_D with T_D>=0",
            "role": "positive open-boundary noise/FDT partner",
            "status": "conditional_positive_if_boundary_state_owned",
        },
        {
            "term": "effective_action",
            "symbol": "S_open",
            "form": "int q_a[dot(q_r)+Gamma_D R_aniso q_r]+(i/2)int q_a N_D q_a",
            "role": "minimal open-boundary influence sector for the arrow",
            "status": "constructed_effective_sector_not_parent_derived",
        },
        {
            "term": "trace_source_coupling",
            "symbol": "S_src",
            "form": "int Lambda_D Tr(P_iso q_r) sqrt(-g) or equivalent scalar stress source",
            "role": "couples only scalar trace charge to FLRW source",
            "status": "conditional_Ward_contract",
        },
        {
            "term": "local_silence_selector",
            "symbol": "sigma_D",
            "form": "Gamma_D,N_D,Lambda_D multiplied by sigma_D with sigma_FLRW=1 and sigma_local=0",
            "role": "would silence local bound domains",
            "status": "closure_unless_sigma_D_parent_derived",
        },
    ]


def derived_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation_or_condition": "delta S_open / delta q_a = 0",
            "result": "dot(q_r)+Gamma_D R_aniso q_r=0",
            "what_it_derives": "positive semigroup arrow on residual modes when Gamma_D>=0",
            "status": "conditional_pass",
        },
        {
            "variation_or_condition": "R_aniso=P_axis-P_iso",
            "result": "R_aniso P_iso=0 and Tr(R_aniso)=2",
            "what_it_derives": "non-scalar rank defect Delta n=2",
            "status": "pass_kinematic",
        },
        {
            "variation_or_condition": "Gamma_D=R M_D R, M_D>=0",
            "result": "<Rq,Gamma_D Rq>>=0",
            "what_it_derives": "dF/dtau=-<Rq,Gamma_D Rq><=0",
            "status": "conditional_pass",
        },
        {
            "variation_or_condition": "N_D=2T_D Gamma_D, T_D>=0",
            "result": "N_D>=0 and Gamma_D>=0 on the residual subspace",
            "what_it_derives": "open-boundary positivity if FDT/KMS-like condition is parent-owned",
            "status": "conditional_pass",
        },
        {
            "variation_or_condition": "delta S_src / delta g_mu_nu",
            "result": "T_mem sees Tr(P_iso q_r), not R_aniso q_r",
            "what_it_derives": "scalar trace source and no direct anisotropic FLRW stress in this effective sector",
            "status": "conditional_Ward_pass",
        },
        {
            "variation_or_condition": "sigma_D=0 for local bound domains",
            "result": "Gamma_D=N_D=Lambda_D=0 locally",
            "what_it_derives": "q_loc source silence if the selector theorem exists",
            "status": "closure_not_derived",
        },
    ]


def positivity_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "residual_energy_monotone",
            "calculation": "F=(1/2)<Rq,Rq>, dF/dtau=-<Rq,Gamma_D Rq>",
            "required_condition": "Gamma_D positive semidefinite",
            "status": "conditional_pass",
            "failure_mode": "negative eigenvalue amplifies anisotropic residual",
        },
        {
            "test": "noise_kernel_positive",
            "calculation": "Im S=(1/2)<q_a,N_D q_a>",
            "required_condition": "N_D positive semidefinite",
            "status": "conditional_pass",
            "failure_mode": "negative noise violates open-action positivity",
        },
        {
            "test": "FDT_transfers_positivity",
            "calculation": "N_D=2T_D Gamma_D",
            "required_condition": "T_D>=0 and KMS/FDT-like state",
            "status": "conditional_pass",
            "failure_mode": "without state condition, Gamma_D sign remains input",
        },
        {
            "test": "ordinary_action_countercheck",
            "calculation": "set N_D=0 and Gamma_D=0",
            "required_condition": "none",
            "status": "no_arrow",
            "failure_mode": "reversible sector cannot dissipate residual rank",
        },
    ]


def ward_trace_rows() -> list[dict[str, Any]]:
    return [
        {
            "ward_clause": "scalar_source_only",
            "mathematical_statement": "S_src depends on Tr(P_iso q_r) only",
            "status": "conditional_pass",
            "blocker": "not yet obtained by varying the full parent metric/action",
        },
        {
            "ward_clause": "anisotropic_residual_orthogonal",
            "mathematical_statement": "Tr(R_aniso q_r)=0 for residual modes",
            "status": "pass_kinematic",
            "blocker": "does not by itself prove local silence or full covariance",
        },
        {
            "ward_clause": "Bianchi_compatibility",
            "mathematical_statement": "nabla_mu T_mem^{mu nu}=0 must follow from coupled field equations",
            "status": "not_derived",
            "blocker": "effective source written but no full covariant conservation proof",
        },
        {
            "ward_clause": "no_direct_shear_source_FLRW",
            "mathematical_statement": "R_aniso q_r decays and does not source FLRW scalar stress directly",
            "status": "conditional_pass",
            "blocker": "anisotropic perturbation sector not fully analyzed",
        },
    ]


def local_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_filter": "domain_selector_sigma_D",
            "condition": "sigma_D=1 on cosmological B3 domains, sigma_D=0 on local bound domains",
            "what_it_would_do": "turn off Gamma_D, N_D, and Lambda_D locally",
            "status": "closure_unless_parent_derived",
            "blocker": "no theorem yet selects sigma_D from parent variables",
        },
        {
            "candidate_filter": "relative_class_triviality",
            "condition": "[J_B]_local=0 while [J_B]_FLRW nontrivial",
            "what_it_would_do": "remove local memory charge without deleting cosmological charge",
            "status": "conditional_contract",
            "blocker": "representative and domain class not parent-owned",
        },
        {
            "candidate_filter": "boundary_environment_absent_locally",
            "condition": "N_D=Gamma_D=0 when no open cosmological boundary bath exists",
            "what_it_would_do": "ordinary local domains stay reversible/local-GR-like",
            "status": "plausible_not_derived",
            "blocker": "requires boundary-state theorem",
        },
        {
            "candidate_filter": "screened_trace_coupling",
            "condition": "Lambda_D=0 or suppressed below PPN bounds in local bound domains",
            "what_it_would_do": "prevent scalar trace memory from appearing in local metric tests",
            "status": "needed_not_derived",
            "blocker": "no quantitative PPN bound generated here",
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
            "gate": "open_sector_constructed",
            "status": "pass",
            "evidence": "S_open uses q_r, q_a, Gamma_D, R_aniso, and N_D",
            "claim_effect": "explicit effective parent-sector candidate exists",
        },
        {
            "gate": "positive_arrow_derived",
            "status": "conditional_pass",
            "evidence": "dF/dtau=-<Rq,Gamma_D Rq><=0 if Gamma_D>=0",
            "claim_effect": "semigroup arrow can be owned by open-sector positivity",
        },
        {
            "gate": "noise_FDT_parent_owned",
            "status": "fail",
            "evidence": "positive noise and FDT/KMS boundary state are specified but not derived from MTS parent fields",
            "claim_effect": "Gamma positivity remains conditional",
        },
        {
            "gate": "Ward_trace_coupling_derived",
            "status": "conditional_pass",
            "evidence": "effective source can be written using Tr(P_iso q_r) only",
            "claim_effect": "scalar FLRW source route is explicit but not fully covariant-parent-derived",
        },
        {
            "gate": "Bianchi_conservation_proved",
            "status": "fail",
            "evidence": "no full coupled metric variation/conservation identity is proved here",
            "claim_effect": "field-theory promotion blocked",
        },
        {
            "gate": "local_silence_derived",
            "status": "fail",
            "evidence": "sigma_D/local filter remains a selector contract, not a theorem",
            "claim_effect": "no local-GR/PPN promotion",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "open sector helps the arrow but not B3 topology, Ward conservation, or local silence",
            "claim_effect": "2/27 remains locked closure/theorem target",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "An explicit open-boundary effective sector can be written: q_a enforces dot(q_r)+Gamma_D R_aniso q_r=0, "
                "positive Gamma_D gives monotone decay of the anisotropic residual, N_D=2T_D Gamma_D supplies the field-theory "
                "positivity contract, and a scalar source coupling through Tr(P_iso q_r) gives the Ward trace target. "
                "However, the positive boundary state, full Bianchi conservation, and local silence selector are not derived."
            ),
            "next_target": "derive_local_silence_selector_or_full_Bianchi_conservation_for_open_sector",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "action_terms.csv": (
            action_terms_rows(),
            ["term", "symbol", "form", "role", "status"],
        ),
        "derived_equations.csv": (
            derived_equation_rows(),
            ["variation_or_condition", "result", "what_it_derives", "status"],
        ),
        "positivity_tests.csv": (
            positivity_test_rows(),
            ["test", "calculation", "required_condition", "status", "failure_mode"],
        ),
        "ward_trace_tests.csv": (
            ward_trace_rows(),
            ["ward_clause", "mathematical_statement", "status", "blocker"],
        ),
        "local_silence_tests.csv": (
            local_silence_rows(),
            ["candidate_filter", "condition", "what_it_would_do", "status", "blocker"],
        ),
        "promotion_gates.csv": (
            promotion_gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
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
        "open_sector_constructed": True,
        "positive_arrow_conditionally_owned": True,
        "Ward_trace_conditionally_constructed": True,
        "local_silence_derived_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "derive_local_silence_selector_or_full_Bianchi_conservation_for_open_sector",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open-boundary parent sector attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
