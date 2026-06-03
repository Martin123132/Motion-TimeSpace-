from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "fifth-force-range-coupling-map"
STATUS = "fifth_force_range_coupling_contract_written_alphaY_lambdaY_not_parent_derived_row_remains_parameterized_unscored"
CLAIM_CEILING = "fifth_force_range_coupling_map_only_no_fifth_force_PPN_EH_WEP_or_local_GR_pass"
NEXT_TARGET = "378-source-normalization-Geff-Meff-GM-absorption-theorem.md"


SOURCE_DOCS = [
    {
        "path": "370-common-mode-phiC-coefficient-map.md",
        "role": "phi_C gradient proxy for fifth-force pressure and strict local zero theorem route",
    },
    {
        "path": "372-local-phiC-zero-theorem-or-gradient-bound.md",
        "role": "conditional local phi_C zero theorem and gradient fallback",
    },
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "fifth-force row is range-dependent Yukawa contract, not one scalar score",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "operator families feeding scalar/bulk/phi_C/nonlocal fifth-force residuals",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "preferred-frame rows are now finite; fifth-force remains the foggiest local row",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward force channels feeding delta_G/fifth-force residuals",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "symbolic PPN residual vector including delta_G from bulk/radial residuals",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "composition-dependent fifth force must not be double-counted against WEP closure",
    },
]


FORCE_LAW_CONTRACT = [
    {
        "object": "standard_Yukawa_potential",
        "equation": "V(r) = -G m1 m2 / r * [1 + alpha_Y exp(-r/lambda_Y)]",
        "derived_quantity": "a_extra/a_GR = alpha_Y (1 + r/lambda_Y) exp(-r/lambda_Y)",
        "status": "required_contract_before_scalar_scoring",
    },
    {
        "object": "class_metric_phiC_force_proxy",
        "equation": "a_phi/a_GR ~= 0.5 |grad phi_C| / |grad U_GR|",
        "derived_quantity": "if phi_C = 2 alpha_phi U_GR exp(-r/lambda_phi), then a_phi/a_GR ~= alpha_phi (1+r/lambda_phi) exp(-r/lambda_phi)",
        "status": "conditional_map_if_phiC_has_Yukawa_profile",
    },
    {
        "object": "strict_local_zero",
        "equation": "grad(phi_C)=0 and no bulk/radial/nonlocal force channel",
        "derived_quantity": "alpha_Y = 0 for class-metric fifth-force row",
        "status": "conditional_not_parent_derived",
    },
    {
        "object": "universal_monopole_absorption",
        "equation": "a_extra/a_GR = constant universal delta_G with lambda_Y effectively infinite",
        "derived_quantity": "absorbed into measured GM only if universal, conserved, time-independent, and not composition dependent",
        "status": "requires_source_normalization_theorem",
    },
    {
        "object": "non_Yukawa_kernel",
        "equation": "a_extra/a_GR = integral dmu rho(mu) alpha(mu) (1+mu r) exp(-mu r)",
        "derived_quantity": "requires spectral/range distribution, not one lambda_Y",
        "status": "parameterized_unscored_until_kernel_derived",
    },
]


MTS_CHANNEL_FORCE_MAP = [
    {
        "MTS_channel": "common_mode_phiC_gradient",
        "candidate_profile": "phi_C(r) = 2 alpha_phi U_GR(r) exp(-r/lambda_phi)",
        "range_parameter": "lambda_phi",
        "coupling_parameter": "alpha_phi",
        "Yukawa_mapping": "alpha_Y = alpha_phi if force is universal and sourced by measured mass",
        "current_status": "profile_not_derived; local zero theorem conditional",
        "runner_policy": "unscored unless profile/range/coupling or strict zero theorem is derived",
    },
    {
        "MTS_channel": "bulk_X_scalar_or_auxiliary",
        "candidate_profile": "(-Delta + m_X^2) X = q_X rho_source",
        "range_parameter": "lambda_X = 1/m_X",
        "coupling_parameter": "alpha_X proportional to q_X^2/(G m_source m_test) after normalization",
        "Yukawa_mapping": "alpha_Y(lambda_X) once m_X and q_X are parent-derived",
        "current_status": "operator sign, mass gap, and source charge missing",
        "runner_policy": "parameterized_unscored",
    },
    {
        "MTS_channel": "radial_boundary_hair",
        "candidate_profile": "B_rad(r) = A_B exp(-r/L_B)/r or A_B/r in the unscreened limit",
        "range_parameter": "L_B",
        "coupling_parameter": "A_B relative to GM",
        "Yukawa_mapping": "alpha_Y ~ A_B/(GM) if universal and Yukawa-like",
        "current_status": "no radial no-hair/source normalization theorem",
        "runner_policy": "retain as fifth-force/beta/source-normalization residual",
    },
    {
        "MTS_channel": "nonlocal_memory_kernel",
        "candidate_profile": "K(r,r') or spectral superposition of Yukawa modes",
        "range_parameter": "kernel spectrum mu or memory length L_mem",
        "coupling_parameter": "spectral weight rho(mu) alpha(mu)",
        "Yukawa_mapping": "not one alpha_Y unless spectrum collapses to one pole",
        "current_status": "kernel not derived locally",
        "runner_policy": "nonlocal modified-gravity residual, unscored here",
    },
    {
        "MTS_channel": "class_changing_domain_wall",
        "candidate_profile": "surface/transition force localized near boundary layer",
        "range_parameter": "wall thickness ell_wall and domain radius R_D",
        "coupling_parameter": "surface tension or class-jump amplitude",
        "Yukawa_mapping": "not generally Yukawa",
        "current_status": "event/source law missing",
        "runner_policy": "separate domain-wall residual, not scalar-scored as Yukawa",
    },
    {
        "MTS_channel": "species_specific_class_response",
        "candidate_profile": "composition-dependent mediator through F_A(C_D)",
        "range_parameter": "inherits scalar/radial/nonlocal range if mediator exists",
        "coupling_parameter": "Delta F_AB or species charge",
        "Yukawa_mapping": "composition-dependent fifth force only after mediator/range law exists",
        "current_status": "WEP closure axiom required",
        "runner_policy": "controlled first by eta_WEP; do not double-count without a separate range law",
    },
]


SCORING_DECISION_TREE = [
    {
        "condition": "grad(phi_C)=0 and bulk/radial/nonlocal/vector force channels theorem-zero",
        "decision": "fifth_force_row_theorem_zero",
        "claim_allowed": "conditional only until parent-derived",
        "next_action": "derive local trivial class, no-hair, and EH/source normalization stack",
    },
    {
        "condition": "only universal constant monopole delta_G survives",
        "decision": "absorb_into_measured_GM_if_source_normalization_theorem_holds",
        "claim_allowed": "no until kappa/G_eff/M_eff theorem exists",
        "next_action": "checkpoint 378 source-normalization theorem",
    },
    {
        "condition": "single finite-range scalar profile is derived",
        "decision": "score_against alpha_Y(lambda_Y) source curve",
        "claim_allowed": "only after alpha_Y and lambda_Y are parent-derived",
        "next_action": "compute range-specific bound, not one global number",
    },
    {
        "condition": "nonlocal/multi-range kernel is derived",
        "decision": "score as spectral force kernel, not one Yukawa point",
        "claim_allowed": "requires kernel and source covariance",
        "next_action": "derive or fit bounded spectral weights with no local-GR promotion",
    },
    {
        "condition": "domain wall/class-changing event force is derived",
        "decision": "score as transition stress/surface force",
        "claim_allowed": "no Yukawa pass",
        "next_action": "derive event law and conservation/source ledger",
    },
    {
        "condition": "range/coupling are missing",
        "decision": "remain parameterized_unscored",
        "claim_allowed": "no",
        "next_action": "retain fifth-force row as active debt",
    },
]


ABSORPTION_TESTS = [
    {
        "test": "universal",
        "required_for_absorption": "same response for all matter and clocks",
        "if_failed": "WEP/composition fifth force, eta_WEP active",
        "current_status": "not parent-derived",
    },
    {
        "test": "constant_range_infinite_or_long_unresolved",
        "required_for_absorption": "force is indistinguishable from rescaling GM in the experiment",
        "if_failed": "range-dependent delta_G/fifth-force signal",
        "current_status": "range missing",
    },
    {
        "test": "time_independent",
        "required_for_absorption": "no secular drift in G_eff or M_eff",
        "if_failed": "Gdot/G row active",
        "current_status": "source normalization open",
    },
    {
        "test": "source_normalized",
        "required_for_absorption": "parent action fixes kappa, G_eff, M_eff, and measured GM",
        "if_failed": "delta_G ambiguity remains",
        "current_status": "open",
    },
    {
        "test": "no_hidden_pressure_or_boundary_flux",
        "required_for_absorption": "monopole is conserved and Ward-owned",
        "if_failed": "beta, alpha3, secular drift, or fifth-force rows active",
        "current_status": "Ward ownership mapped not proved",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "delta_G_or_fifth_force_yukawa",
        "before_377": "parameterized_source_context_locked_not_scalar_scored",
        "after_377": "force_law_contract_written_alphaY_lambdaY_required",
        "claim_status": "unscored_until_range_and_coupling_derived",
    },
    {
        "runner_row": "common_mode_phiC_fifth_force_proxy",
        "before_377": "a_extra/a_GR ~ 0.5 r_grad proxy",
        "after_377": "proxy may map to Yukawa only if phi_C profile is derived",
        "claim_status": "conditional_or_unscored",
    },
    {
        "runner_row": "bulk_X_scalar_force",
        "before_377": "operator/source normalization missing",
        "after_377": "requires m_X, q_X, and source charge to define lambda_X and alpha_X",
        "claim_status": "unscored",
    },
    {
        "runner_row": "radial_boundary_hair_force",
        "before_377": "radial scalar hair/no-hair open",
        "after_377": "maps to alpha_Y only after A_B and L_B are derived",
        "claim_status": "unscored",
    },
    {
        "runner_row": "universal_monopole_delta_G",
        "before_377": "possible measured-GM absorption route",
        "after_377": "requires source-normalization/GM absorption theorem",
        "claim_status": "next_checkpoint_target",
    },
]


FAILURE_MODES = [
    {
        "failure": "one_number_fifth_force_bound",
        "meaning": "using one scalar tolerance for all fifth-force ranges",
        "consequence": "fake precision; wrong experiment/range comparison",
    },
    {
        "failure": "phiC_gradient_proxy_overclaim",
        "meaning": "treating r_grad as a Yukawa alpha without deriving the radial profile",
        "consequence": "invalid fifth-force score",
    },
    {
        "failure": "GM_absorption_without_source_theorem",
        "meaning": "absorbing a monopole into measured GM without proving universality/conservation",
        "consequence": "hides delta_G, Gdot, WEP, or beta residuals",
    },
    {
        "failure": "composition_fifth_force_double_count",
        "meaning": "counting species-dependent class response as both eta_WEP and independent fifth force without a mediator law",
        "consequence": "unfair or confused residual accounting",
    },
    {
        "failure": "domain_wall_called_Yukawa",
        "meaning": "scoring a class-transition surface force with a point-source Yukawa bound",
        "consequence": "wrong observable and wrong source geometry",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The fifth-force row now has an exact force-law contract: either theorem-zero, universal monopole absorbed by a source-normalization theorem, Yukawa/spectral range-coupling derived and scored, or explicitly unscored. MTS has not yet derived alpha_Y(lambda_Y), so delta_G/fifth-force remains parameterized and active.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive kappa, G_eff, M_eff, and measured-GM absorption or keep delta_G/Gdot rows active",
        "pass_condition": "Newtonian source normalization is parent-derived or source-bounded",
    },
    {
        "priority": 2,
        "target": "379-class-only-boundary-action-noangular-theorem.md",
        "task": "attempt the class-only boundary action theorem that would kill B_0i and trace-free angular shear",
        "pass_condition": "boundary vector/shear sources are theorem-zero or retained as coefficients",
    },
    {
        "priority": 3,
        "target": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "task": "derive or reject a massive/source-free bulk-X equation with m_X and q_X sufficient to define alpha_X(lambda_X)",
        "pass_condition": "bulk scalar force is theorem-zero, Yukawa-scored, or explicitly retained unscored",
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
            "gate": "Yukawa_force_law_contract_written",
            "status": "pass",
            "evidence": "V(r) and a_extra/a_GR alpha_Y(lambda_Y) relation written",
        },
        {
            "gate": "MTS_channels_mapped_to_range_coupling",
            "status": "pass",
            "evidence": f"{len(MTS_CHANNEL_FORCE_MAP)} MTS channels mapped",
        },
        {
            "gate": "phiC_proxy_limited_to_profile_derived_case",
            "status": "pass",
            "evidence": "r_grad proxy is not treated as alpha_Y without phi_C(r)",
        },
        {
            "gate": "GM_absorption_tests_written",
            "status": "pass",
            "evidence": "universality, range, time-independence, source normalization, and Ward ownership tests recorded",
        },
        {
            "gate": "alphaY_lambdaY_parent_derived",
            "status": "fail",
            "evidence": "no MTS channel has derived both range and coupling",
        },
        {
            "gate": "fifth_force_scalar_scored",
            "status": "fail",
            "evidence": "fifth-force row remains parameterized/unscored",
        },
        {
            "gate": "local_GR_or_PPN_pass_claimed",
            "status": "fail",
            "evidence": "force law contract only; no local pass",
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
    write_csv(results_dir / "force_law_contract.csv", FORCE_LAW_CONTRACT)
    write_csv(results_dir / "MTS_channel_force_map.csv", MTS_CHANNEL_FORCE_MAP)
    write_csv(results_dir / "scoring_decision_tree.csv", SCORING_DECISION_TREE)
    write_csv(results_dir / "absorption_tests.csv", ABSORPTION_TESTS)
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
        "force_channels_mapped": len(MTS_CHANNEL_FORCE_MAP),
        "alphaY_lambdaY_parent_derived": False,
        "fifth_force_scalar_score_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 377 fifth-force range-coupling map artifacts."
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
