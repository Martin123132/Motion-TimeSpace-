from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-nohair-and-PPN-residual-vector-gate"
STATUS = "boundary_residual_decomposition_and_symbolic_PPN_vector_written_no_nohair_or_local_GR_promotion"
CLAIM_CEILING = "symbolic_PPN_contract_only_no_boundary_nohair_local_GR_or_observational_pass_claim"
NEXT_TARGET = "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md"


SOURCE_DOCS = [
    (
        "177-parent-action-perturbation-local-GR-contract.md",
        "parent action/local-GR outputs and local PPN required variables",
    ),
    (
        "179-local-GR-PPN-silence-contract.md",
        "earlier effective PPN residual vector, screened but not derived",
    ),
    (
        "250-local-GR-gate-scorecard-and-test-readiness.md",
        "local GR N1-N6 scorecard and no trace-free/shear gate",
    ),
    (
        "346-GR-and-derivation-north-star-spine.md",
        "GR reduction and explicit PPN vector contract",
    ),
    (
        "347-local-GR-parent-reduction-theorem-attempt.md",
        "conditional local GR theorem and projector stress alternatives",
    ),
    (
        "348-N5-projector-stress-conservation-theorem.md",
        "conditional quotient/topological local no-bulk projector stress",
    ),
    (
        "351-local-GR-spin2-rank2-bridge-or-boundary-PPN-gate.md",
        "selection of boundary no-hair and PPN residual-vector gate",
    ),
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
            "role": "this boundary no-hair / PPN residual-vector builder",
            "exists": "yes" if script_path.exists() else "no",
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def boundary_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "bulk_MTS_after_quotient_PD",
            "symbol": "E_bulk^MTS",
            "allowed_for_GR": "0",
            "PPN_risk_if_nonzero": "modified Poisson equation, fifth force, non-GR gamma/beta",
            "current_status": "conditional_zero_from_N5_only_for_projector_piece",
            "next_test": "prove all non-projector MTS bulk terms vanish in compact exterior",
        },
        {
            "sector": "boundary_trace_monopole",
            "symbol": "B_tr^mono",
            "allowed_for_GR": "mass renormalization only",
            "PPN_risk_if_nonzero": "renormalized GM is acceptable; radius-dependent trace shifts beta/gamma",
            "current_status": "allowed_conditionally",
            "next_test": "show it is constant monopole charge absorbed into measured mass",
        },
        {
            "sector": "boundary_trace_radial",
            "symbol": "B_tr^rad(r)",
            "allowed_for_GR": "0 or falls below local bounds",
            "PPN_risk_if_nonzero": "new radial potential changes beta/gamma and perihelion timing",
            "current_status": "open",
            "next_test": "derive no radial scalar hair or compute bound",
        },
        {
            "sector": "boundary_tracefree_shear",
            "symbol": "B_TF,ij",
            "allowed_for_GR": "0 through l>=2 no-hair / multipole suppression",
            "PPN_risk_if_nonzero": "anisotropic metric potentials and lensing slip",
            "current_status": "open_hard_local_GR_gate",
            "next_test": "prove trace-free boundary variation vanishes or decays faster than PPN sensitivity",
        },
        {
            "sector": "boundary_vector_preferred_frame",
            "symbol": "B_0i",
            "allowed_for_GR": "0 in preferred local rest frame or pure gauge",
            "PPN_risk_if_nonzero": "alpha1/alpha2 preferred-frame residuals",
            "current_status": "open",
            "next_test": "show no vector/current background survives around compact sources",
        },
        {
            "sector": "clock_ruler_nonmetricity",
            "symbol": "C_clock, C_WEP",
            "allowed_for_GR": "0; all matter, photons, clocks, and rulers couple to same metric",
            "PPN_risk_if_nonzero": "redshift, WEP, lensing/ruler mismatch",
            "current_status": "open",
            "next_test": "derive single physical metric/coframe coupling",
        },
        {
            "sector": "boundary_conservation_flux",
            "symbol": "n_mu B^{mu nu}",
            "allowed_for_GR": "0 or balanced by owned matter/boundary charge",
            "PPN_risk_if_nonzero": "nonconserved stress, Bianchi failure, secular orbital drift",
            "current_status": "open",
            "next_test": "derive boundary Ward identity / flux cancellation",
        },
    ]


def ppn_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": "gamma_minus_1",
            "symbolic_source": "c_gamma_TF * ||B_TF|| + c_gamma_rad * ||B_tr^rad|| + c_gamma_bulk * ||E_bulk^MTS||",
            "zero_condition": "B_TF=0, B_tr^rad=0, E_bulk^MTS=0",
            "status": "symbolic_not_bounded",
            "claim_allowed": "residual map only",
        },
        {
            "residual": "beta_minus_1",
            "symbolic_source": "c_beta_rad * ||B_tr^rad|| + c_beta_nl * ||nonlinear boundary self-coupling||",
            "zero_condition": "trace boundary is monopole mass renormalization only; no nonlinear scalar hair",
            "status": "symbolic_not_bounded",
            "claim_allowed": "residual map only",
        },
        {
            "residual": "alpha1_alpha2_preferred_frame",
            "symbolic_source": "c_alpha_vec * ||B_0i|| + c_alpha_u * ||u_MTS^i||",
            "zero_condition": "no vector/current background; no preferred local MTS frame",
            "status": "symbolic_not_bounded",
            "claim_allowed": "residual map only",
        },
        {
            "residual": "xi_preferred_location_or_anisotropy",
            "symbolic_source": "c_xi_TF * ||B_TF,l>=2|| + c_xi_ext * ||external-domain anisotropy||",
            "zero_condition": "trace-free boundary multipoles vanish or are screened",
            "status": "symbolic_not_bounded",
            "claim_allowed": "residual map only",
        },
        {
            "residual": "alpha_clock",
            "symbolic_source": "c_clock * ||C_clock|| + c_nonmetric * ||delta g_matter - delta g_photon||",
            "zero_condition": "single metric/coframe coupling for clocks, rods, matter, and photons",
            "status": "symbolic_not_bounded",
            "claim_allowed": "residual map only",
        },
        {
            "residual": "eta_WEP",
            "symbolic_source": "c_WEP * ||C_WEP|| + c_comp * ||composition-dependent MTS charge||",
            "zero_condition": "no composition-dependent MTS charge or nonmetric coupling",
            "status": "symbolic_not_bounded",
            "claim_allowed": "residual map only",
        },
        {
            "residual": "delta_G_or_fifth_force",
            "symbolic_source": "c_G_bulk * ||E_bulk^MTS|| + c_G_rad * ||B_tr^rad||",
            "zero_condition": "no residual bulk source and no radial scalar boundary hair",
            "status": "symbolic_not_bounded",
            "claim_allowed": "residual map only",
        },
    ]


def nohair_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "H1_quotient_projector_bulk_silence",
            "required_statement": "quotient/topological P_D removes projector bulk stress in compact exterior",
            "status": "conditional_pass_from_348_350",
            "if_fails": "metric-only local GR route fails at N5",
        },
        {
            "condition": "H2_no_nonprojector_bulk_MTS_support",
            "required_statement": "all remaining MTS fields have no compact-exterior bulk stress or are pure constraints",
            "status": "open",
            "if_fails": "modified Poisson / fifth-force branch",
        },
        {
            "condition": "H3_boundary_trace_only_mass",
            "required_statement": "trace boundary term is constant monopole charge absorbed into measured mass",
            "status": "open",
            "if_fails": "gamma/beta/radial-potential residual",
        },
        {
            "condition": "H4_boundary_tracefree_shear_zero",
            "required_statement": "trace-free/shear boundary variation vanishes or is multipole-suppressed below PPN reach",
            "status": "open_hard_gate",
            "if_fails": "lensing slip / anisotropic potential residual",
        },
        {
            "condition": "H5_no_vector_or_preferred_frame",
            "required_statement": "no local vector/current frame remains after constraints",
            "status": "open",
            "if_fails": "alpha1/alpha2 preferred-frame residuals",
        },
        {
            "condition": "H6_single_metric_matter_coupling",
            "required_statement": "all matter, clocks, rulers, and photons couple to the same physical metric/coframe",
            "status": "open",
            "if_fails": "WEP/clock/redshift/lensing mismatch",
        },
        {
            "condition": "H7_boundary_Ward_conservation",
            "required_statement": "boundary flux is zero or exactly balanced by owned charge so Bianchi identity closes",
            "status": "open",
            "if_fails": "fake conservation / secular dynamics",
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem": "boundary_nohair_to_PPN_zero",
            "statement": (
                "If H1-H7 all hold, the compact exterior reduces to metric-only Einstein-Hilbert with at most "
                "mass renormalization, so gamma-1, beta-1, preferred-frame, clock, WEP, and fifth-force residuals vanish."
            ),
            "status": "conditional_theorem",
            "why_not_promotion": "H2-H7 are not derived",
        },
        {
            "theorem": "trace_monopole_allowed",
            "statement": (
                "A pure boundary monopole trace can be absorbed into measured GM and need not produce PPN violation."
            ),
            "status": "conditional_theorem",
            "why_not_promotion": "need proof boundary trace is exactly monopole and conserved",
        },
        {
            "theorem": "tracefree_shear_no_go_for_GR",
            "statement": (
                "Any surviving trace-free/shear boundary component is a direct non-GR local residual unless bounded below PPN reach."
            ),
            "status": "consistency_no_go",
            "why_not_promotion": "no shear no-hair theorem exists yet",
        },
        {
            "theorem": "single_metric_coupling_needed",
            "statement": (
                "Even with EH bulk equations, nonmetric matter/clock/photon couplings spoil local GR observables."
            ),
            "status": "consistency_no_go",
            "why_not_promotion": "single-metric coupling remains an assumption to derive",
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
            "gate": "boundary_decomposition_written",
            "status": "pass",
            "evidence": "trace, trace-free shear, vector, clock/WEP, bulk, and conservation sectors separated",
        },
        {
            "gate": "symbolic_PPN_residual_vector_written",
            "status": "pass",
            "evidence": "gamma, beta, preferred-frame, anisotropy, clock, WEP, and fifth-force rows emitted",
        },
        {
            "gate": "quotient_PD_projector_bulk_silence",
            "status": "conditional_pass",
            "evidence": "depends on 348/350 topological quotient P_D route",
        },
        {
            "gate": "boundary_nohair_derived",
            "status": "fail",
            "evidence": "trace radial, trace-free shear, vector, clock, and Ward conditions remain open",
        },
        {
            "gate": "PPN_residuals_numerically_bounded",
            "status": "fail",
            "evidence": "this checkpoint is symbolic; no official numeric PPN bound run",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "conditional theorem only; H2-H7 not derived",
        },
        {
            "gate": "next_bound_or_theorem_target_selected",
            "status": "pass",
            "evidence": NEXT_TARGET,
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
                "The local branch now has the correct symbolic police line: after quotient P_D silence, any remaining "
                "boundary or bulk residual must be sorted into trace monopole, radial trace hair, trace-free shear, "
                "vector/preferred-frame, clock/WEP coupling, bulk support, and conservation-flux sectors. A pure "
                "monopole trace can be mass renormalization; trace-free shear, vector backgrounds, nonmetric clock "
                "couplings, or bulk support generate PPN residuals. The residual vector is now explicit, but the "
                "boundary no-hair theorem and numeric bounds are not done, so there is no local-GR or PPN promotion."
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
        "boundary_residual_decomposition.csv": (
            boundary_decomposition_rows(),
            ["sector", "symbol", "allowed_for_GR", "PPN_risk_if_nonzero", "current_status", "next_test"],
        ),
        "symbolic_PPN_residual_vector.csv": (
            ppn_residual_rows(),
            ["residual", "symbolic_source", "zero_condition", "status", "claim_allowed"],
        ),
        "nohair_conditions.csv": (
            nohair_condition_rows(),
            ["condition", "required_statement", "status", "if_fails"],
        ),
        "conditional_theorem_ledger.csv": (
            conditional_theorem_rows(),
            ["theorem", "statement", "status", "why_not_promotion"],
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
        "boundary_decomposition_written": True,
        "symbolic_PPN_residual_vector_written": True,
        "quotient_PD_projector_bulk_silence": "conditional_pass",
        "boundary_nohair_derived": False,
        "PPN_residuals_numerically_bounded": False,
        "local_GR_or_PPN_promoted": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 352: boundary no-hair and symbolic PPN residual vector gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
