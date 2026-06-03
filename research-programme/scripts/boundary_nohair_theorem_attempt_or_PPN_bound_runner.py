from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-nohair-theorem-attempt-or-PPN-bound-runner"
STATUS = "conditional_boundary_nohair_contract_written_proxy_PPN_bound_runner_ready_no_local_GR_promotion"
CLAIM_CEILING = "conditional_nohair_and_proxy_bounds_only_no_official_PPN_or_local_GR_pass_claim"
NEXT_TARGET = "354-official-local-bound-source-lock-or-nohair-proof-deepening.md"


SOURCE_DOCS = [
    (
        "177-parent-action-perturbation-local-GR-contract.md",
        "parent action and local PPN required outputs",
    ),
    (
        "179-local-GR-PPN-silence-contract.md",
        "earlier effective scalar PPN proxy, screened but not derived",
    ),
    (
        "250-local-GR-gate-scorecard-and-test-readiness.md",
        "local GR N-gate scorecard and beta/gamma readiness",
    ),
    (
        "348-N5-projector-stress-conservation-theorem.md",
        "conditional quotient/topological P_D bulk projector silence",
    ),
    (
        "351-local-GR-spin2-rank2-bridge-or-boundary-PPN-gate.md",
        "boundary no-hair route selected after rank-2 bridge rejection",
    ),
    (
        "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "boundary residual decomposition and symbolic PPN vector",
    ),
]


PROXY_BOUNDS = [
    ("gamma_minus_1", 2.3e-5, "proxy_Cassini_like_gamma_scale_not_official_current_bound"),
    ("beta_minus_1", 8.0e-5, "proxy_solar_system_beta_scale_not_official_current_bound"),
    ("alpha1_alpha2_preferred_frame", 4.0e-7, "proxy_preferred_frame_strict_scale_not_official_current_bound"),
    ("xi_anisotropy", 1.0e-3, "proxy_anisotropy_scale_not_official_current_bound"),
    ("alpha_clock", 1.0e-6, "proxy_clock_redshift_scale_not_official_current_bound"),
    ("eta_WEP", 1.0e-14, "proxy_WEP_scale_not_official_current_bound"),
    ("delta_G_or_fifth_force", 1.0e-10, "proxy_fifth_force_scale_not_official_current_bound"),
]


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for filename, role in SOURCE_DOCS:
        path = ROOT / filename
        rows.append(
            {
                "source_path": relpath(path),
                "role": role,
                "exists": "yes" if path.exists() else "no",
                "issue": "" if path.exists() else "missing",
            }
        )
    script_path = Path(__file__).resolve()
    rows.append(
        {
            "source_path": relpath(script_path),
            "role": "this boundary no-hair theorem / proxy-bound builder",
            "exists": "yes" if script_path.exists() else "no",
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def nohair_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "A1_isolated_stationary_exterior",
            "statement": "work in a compact local exterior outside an isolated stationary source",
            "derivation_status": "assumption_for_theorem",
            "consequence_if_true": "time-dependent radiation and cosmological background pieces are excluded from local PPN gate",
            "failure_mode": "external tides or time-dependent memory source enter residual vector",
        },
        {
            "step": "A2_quotient_PD_bulk_silence",
            "statement": "metric-independent quotient/topological P_D has no local bulk projector stress",
            "derivation_status": "conditional_pass_from_348_350",
            "consequence_if_true": "N5 projector stress does not source the compact exterior bulk",
            "failure_mode": "metric-dependent projector reintroduces bulk stress",
        },
        {
            "step": "A3_boundary_action_class_only",
            "statement": "boundary action depends only on total relative class/charge and induced volume, not angular representative data",
            "derivation_status": "not_derived",
            "consequence_if_true": "only a scalar monopole boundary trace can survive",
            "failure_mode": "trace-free shear and angular multipoles are allowed",
        },
        {
            "step": "A4_no_boundary_marker",
            "statement": "no material boundary marker, preferred normal-frame field, or active patch label exists",
            "derivation_status": "not_derived",
            "consequence_if_true": "vector/preferred-frame and anisotropic boundary sectors are forbidden",
            "failure_mode": "marker-local counterterms generate PPN residuals",
        },
        {
            "step": "A5_regular_asymptotic_match",
            "statement": "regular interior/exterior matching plus asymptotic flat local patch eliminates radial scalar hair",
            "derivation_status": "not_derived",
            "consequence_if_true": "boundary trace is absorbed into measured mass rather than a new radial potential",
            "failure_mode": "B_tr^rad(r) shifts gamma, beta, and fifth-force residuals",
        },
        {
            "step": "A6_single_metric_coupling",
            "statement": "matter, clocks, rulers, photons, and local lab standards couple to the same metric/coframe",
            "derivation_status": "not_derived",
            "consequence_if_true": "clock/WEP residuals vanish once metric equations reduce to EH",
            "failure_mode": "nonmetric redshift, WEP, and lensing/ruler mismatch remain",
        },
        {
            "step": "A7_boundary_Ward_identity",
            "statement": "boundary flux is zero or exactly balanced by an owned conserved boundary charge",
            "derivation_status": "not_derived",
            "consequence_if_true": "Bianchi identity closes without fake conservation",
            "failure_mode": "secular dynamics or unowned stress exchange",
        },
    ]


def nohair_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "boundary_trace_monopole",
            "theorem_verdict": "conditional_allowed",
            "needed_axiom_or_derivation": "class-only boundary action plus conserved total charge",
            "PPN_action": "absorb into measured GM if no radial dependence",
        },
        {
            "sector": "boundary_trace_radial",
            "theorem_verdict": "not_closed",
            "needed_axiom_or_derivation": "regular/asymptotic no radial scalar hair theorem",
            "PPN_action": "bound epsilon_rad if theorem fails",
        },
        {
            "sector": "boundary_tracefree_shear",
            "theorem_verdict": "not_closed_hard_gate",
            "needed_axiom_or_derivation": "boundary class-only action or no angular representative theorem",
            "PPN_action": "bound epsilon_TF and lensing-slip residuals if theorem fails",
        },
        {
            "sector": "boundary_vector_preferred_frame",
            "theorem_verdict": "not_closed",
            "needed_axiom_or_derivation": "no marker/no preferred-frame field theorem",
            "PPN_action": "bound epsilon_vec against preferred-frame proxy",
        },
        {
            "sector": "clock_WEP_nonmetricity",
            "theorem_verdict": "not_closed",
            "needed_axiom_or_derivation": "single metric/coframe coupling theorem",
            "PPN_action": "bound epsilon_clock and epsilon_WEP separately",
        },
        {
            "sector": "bulk_MTS_support",
            "theorem_verdict": "partly_closed_only_for_projector_piece",
            "needed_axiom_or_derivation": "prove non-projector bulk MTS terms vanish",
            "PPN_action": "bound epsilon_bulk if any retained stress remains",
        },
        {
            "sector": "boundary_flux",
            "theorem_verdict": "not_closed",
            "needed_axiom_or_derivation": "owned boundary Ward/Bianchi identity",
            "PPN_action": "do not claim conservation until derived",
        },
    ]


def proxy_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": name,
            "proxy_bound_abs": f"{bound:.6e}",
            "source": source,
            "official_status": "proxy_only_requires_source_lock_before_claim",
        }
        for name, bound, source in PROXY_BOUNDS
    ]


def residual_amplitude_requirement_rows() -> list[dict[str, Any]]:
    rows = []
    for name, bound, source in PROXY_BOUNDS:
        rows.append(
            {
                "residual": name,
                "unit_coefficient_requirement": f"epsilon_{name} < {bound:.6e}",
                "meaning": "if the unknown linear coefficient is O(1), the corresponding residual amplitude must be below this proxy scale",
                "source": source,
                "claim_allowed": "engineering target only, not official pass",
            }
        )
    rows.extend(
        [
            {
                "residual": "gamma_minus_1_mixed_sources",
                "unit_coefficient_requirement": "epsilon_TF + epsilon_rad + epsilon_bulk < 2.300000e-05",
                "meaning": "trace-free, radial, and bulk pieces share the gamma proxy budget",
                "source": "derived_from_proxy_gamma_budget",
                "claim_allowed": "engineering target only",
            },
            {
                "residual": "clock_WEP_split",
                "unit_coefficient_requirement": "epsilon_WEP < 1.000000e-14 is much stricter than epsilon_clock < 1.000000e-06",
                "meaning": "composition-dependent charge is the most dangerous local coupling",
                "source": "derived_from_proxy_clock_WEP_budget",
                "claim_allowed": "engineering target only",
            },
        ]
    )
    return rows


def theorem_or_bound_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "Route_A_boundary_nohair_theorem",
            "entry_condition": "A3-A7 can be derived from parent quotient/regularity/single-metric structure",
            "success_output": "B_TF=B_0i=B_tr^rad=C_clock=C_WEP=E_bulk_nonproj=0, monopole trace only",
            "failure_output": "explicit open no-hair axiom list",
            "status_after_353": "attempted_not_closed",
        },
        {
            "route": "Route_B_proxy_PPN_bound_runner",
            "entry_condition": "one or more no-hair sectors remains open",
            "success_output": "epsilon-sector budgets for gamma, beta, preferred-frame, clock, WEP, and fifth-force residuals",
            "failure_output": "needs official source lock and model-specific coefficients",
            "status_after_353": "scaffold_ready_proxy_only",
        },
        {
            "route": "Route_C_modified_exterior_branch",
            "entry_condition": "residual amplitudes are too large or cannot be naturally suppressed",
            "success_output": "honest modified-gravity local branch with no GR promotion",
            "failure_output": "theory not locally viable",
            "status_after_353": "deferred_until_bound_runner_has_coefficients",
        },
    ]


def gate_result_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in sources)
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all cited local-GR/PPN checkpoints and this script exist" if sources_ok else "missing cited source",
        },
        {
            "gate": "boundary_nohair_theorem_attempted",
            "status": "pass",
            "evidence": "A1-A7 theorem contract written",
        },
        {
            "gate": "boundary_nohair_derived",
            "status": "fail",
            "evidence": "A3-A7 not parent-derived",
        },
        {
            "gate": "monopole_trace_safe_condition_identified",
            "status": "conditional_pass",
            "evidence": "pure conserved monopole can be absorbed into measured mass",
        },
        {
            "gate": "proxy_PPN_bound_runner_ready",
            "status": "pass",
            "evidence": "proxy bounds and unit-coefficient residual amplitude budgets emitted",
        },
        {
            "gate": "official_bound_source_locked",
            "status": "fail",
            "evidence": "numeric rows are proxy scales only, not current official source-locked bounds",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "no no-hair theorem and no official bound pass",
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
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The no-hair route now has a precise theorem contract. Quotient P_D can silence the projector bulk piece, "
                "and a pure conserved monopole boundary trace would be safe as measured mass renormalization. But the "
                "needed parent derivations for class-only boundary action, no marker fields, no radial scalar hair, "
                "single-metric coupling, and a boundary Ward identity are still missing. Therefore local GR is not "
                "promoted. The fallback proxy PPN bound runner is ready as an engineering scaffold, but its numeric "
                "scales are not official source-locked bounds."
            ),
            "next_target": NEXT_TARGET,
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    outputs = {
        "source_register.csv": (
            sources,
            ["source_path", "role", "exists", "issue"],
        ),
        "nohair_theorem_attempt.csv": (
            nohair_theorem_attempt_rows(),
            ["step", "statement", "derivation_status", "consequence_if_true", "failure_mode"],
        ),
        "nohair_sector_verdicts.csv": (
            nohair_verdict_rows(),
            ["sector", "theorem_verdict", "needed_axiom_or_derivation", "PPN_action"],
        ),
        "proxy_bound_manifest.csv": (
            proxy_bound_rows(),
            ["residual", "proxy_bound_abs", "source", "official_status"],
        ),
        "residual_amplitude_requirements.csv": (
            residual_amplitude_requirement_rows(),
            ["residual", "unit_coefficient_requirement", "meaning", "source", "claim_allowed"],
        ),
        "theorem_or_bound_route_decision.csv": (
            theorem_or_bound_route_rows(),
            ["route", "entry_condition", "success_output", "failure_output", "status_after_353"],
        ),
        "gate_results.csv": (
            gate_result_rows(sources),
            ["gate", "status", "evidence"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in sources),
        "boundary_nohair_theorem_attempted": True,
        "boundary_nohair_derived": False,
        "proxy_PPN_bound_runner_ready": True,
        "official_bound_source_locked": False,
        "local_GR_or_PPN_promoted": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 353: boundary no-hair theorem attempt or proxy PPN bound runner.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
