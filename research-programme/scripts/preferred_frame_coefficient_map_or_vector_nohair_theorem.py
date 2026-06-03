from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "preferred-frame-coefficient-map-or-vector-nohair-theorem"
STATUS = "vector_nohair_conditional_not_parent_derived_preferred_frame_coefficients_mapped_budget_only_no_PPN_pass"
CLAIM_CEILING = "preferred_frame_coefficient_map_only_no_vector_nohair_PPN_EH_fifth_force_WEP_or_local_GR_pass"
NEXT_TARGET = "377-fifth-force-range-coupling-map.md"


SOURCE_DOCS = [
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "symbolic boundary residual vector including B_0i, xi, alpha1/alpha2, and conservation flux hazards",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward force fates and retained preferred-frame/xi residual rows",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH sufficiency stack and vector/preferred-frame operator obstruction",
    },
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "source-locked alpha1/alpha2/alpha3/xi rows and contingent Gdot policy",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "residual modified-gravity operator ledger retaining vector/preferred-frame operators",
    },
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "no marker fields/no radial hair/single metric coupling proof debts and earlier source-lock context",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward identity and projector/domain variation context for flux ownership",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe closure, needed to prevent vector/coframe matter mismatch overclaim",
    },
]


VECTOR_NOHAIR_PREMISES = [
    {
        "premise": "no_physical_marker_vector",
        "required_statement": "domain labels, boundary patch labels, and projector representatives are gauge/bookkeeping, not local vector fields",
        "would_kill": "epsilon_marker_vec and epsilon_P_vector",
        "current_status": "not_parent_derived",
    },
    {
        "premise": "class_only_boundary_action",
        "required_statement": "boundary action depends only on total class/charge/monopole data, not angular or vector representatives",
        "would_kill": "B_0i and l=1 boundary vector hair",
        "current_status": "conditional_template_not_parent_derived",
    },
    {
        "premise": "covariant_domain_selector",
        "required_statement": "domain selector is scalar/topological or Ward-owned, with no preferred local rest frame",
        "would_kill": "epsilon_domain_vec and epsilon_domain_aniso",
        "current_status": "open",
    },
    {
        "premise": "stationary_compact_exterior_regular_vector_equation",
        "required_statement": "any surviving local vector obeys source-free elliptic/massive regular exterior equation",
        "would_kill": "propagating vector preferred-frame mode",
        "current_status": "operator_not_derived",
    },
    {
        "premise": "Ward_owned_flux",
        "required_statement": "boundary/projector/domain flux is zero or exactly balanced in total Ward identity",
        "would_kill": "alpha3-like momentum nonconservation and Gdot/secular drift channels",
        "current_status": "mapped_not_proved",
    },
    {
        "premise": "single_observed_coframe",
        "required_statement": "matter/light/clocks do not see a species-dependent or vector-shifted coframe",
        "would_kill": "coframe vector matter mismatch",
        "current_status": "closure_axiom_required",
    },
]


VECTOR_NOHAIR_ATTEMPT_STEPS = [
    {
        "step": 1,
        "statement": "Decompose the local vector/preferred-frame sector.",
        "equation": "V_vec = {B_0i, u_MTS^i, n_D^i, P_vector^i, flux^i, coframe_slip^i}",
        "result": "all possible alpha_i sources are visible",
        "status": "definition",
    },
    {
        "step": 2,
        "statement": "If marker/domain/projector vectors are gauge or topological representatives, they cannot appear as local matter-visible vectors.",
        "equation": "delta S_ext / delta V_vec = 0 with V_vec pure gauge/bookkeeping",
        "result": "epsilon_marker_vec = epsilon_P_vector = 0",
        "status": "conditional",
    },
    {
        "step": 3,
        "statement": "If the boundary action is class-only and isotropic, it has no l=1 vector source.",
        "equation": "S_boundary = S(Q_rel, M_eff, scalar class data) implies delta S_boundary / delta B_0i = 0",
        "result": "B_0i source absent",
        "status": "conditional",
    },
    {
        "step": 4,
        "statement": "If any vector equation remains, require source-free regular exterior decay or positive mass gap.",
        "equation": "(-Delta + m_V^2) V_i = 0, m_V^2 >= 0, regular/decaying exterior data",
        "result": "V_i = 0 or exponentially screened",
        "status": "operator_needed_not_derived",
    },
    {
        "step": 5,
        "statement": "If boundary/domain flux is Ward-owned, alpha3-like momentum-nonconservation channels vanish.",
        "equation": "n_mu B^{mu i} + F_domain^i + F_projector^i = 0",
        "result": "epsilon_flux = epsilon_momentum_nonconserve = 0",
        "status": "conditional",
    },
    {
        "step": 6,
        "statement": "Because the parent premises are not derived, write the coefficient map instead of claiming no-hair.",
        "equation": "alpha_i = sum_a C_ia epsilon_a",
        "result": "preferred-frame budget runner remains active",
        "status": "actual_current_branch",
    },
]


PREFERRED_FRAME_COEFFICIENT_MAP = [
    {
        "residual": "preferred_frame_alpha1",
        "source_locked_scale_abs": 1.0e-4,
        "stricter_context_scale_abs": 4.0e-5,
        "symbolic_map": "alpha1 = C1B eps_B0i + C1D eps_domain_vec + C1P eps_P_vector + C1e eps_coframe_slip",
        "terms": 4,
        "equal_share_ceiling": 2.5e-5,
        "stricter_equal_share_ceiling": 1.0e-5,
        "status": "budget_only_coefficients_missing",
    },
    {
        "residual": "preferred_frame_alpha2",
        "source_locked_scale_abs": 2.0e-9,
        "stricter_context_scale_abs": "",
        "symbolic_map": "alpha2 = C2B eps_B0i + C2D eps_domain_vec + C2A eps_anisotropic_coframe + C2P eps_P_vector",
        "terms": 4,
        "equal_share_ceiling": 5.0e-10,
        "stricter_equal_share_ceiling": "",
        "status": "budget_only_coefficients_missing",
    },
    {
        "residual": "preferred_frame_alpha3",
        "source_locked_scale_abs": 4.0e-20,
        "stricter_context_scale_abs": "",
        "symbolic_map": "alpha3 = C3F eps_unowned_flux + C3M eps_momentum_nonconserve + C3V eps_vector_frame",
        "terms": 3,
        "equal_share_ceiling": 1.3333333333333333e-20,
        "stricter_equal_share_ceiling": "",
        "status": "contingent_budget_only_if_channel_exists",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "source_locked_scale_abs": 4.0e-9,
        "stricter_context_scale_abs": "",
        "symbolic_map": "xi = CxiTF eps_TF_lge2 + CxiExt eps_external_domain_aniso + CxiD eps_domain_aniso + CxiW eps_Weyl2",
        "terms": 4,
        "equal_share_ceiling": 1.0e-9,
        "stricter_equal_share_ceiling": "",
        "status": "budget_only_coefficients_missing",
    },
    {
        "residual": "Gdot_over_G",
        "source_locked_scale_abs": "9.6e-15 yr^-1",
        "stricter_context_scale_abs": "",
        "symbolic_map": "Gdot/G = CGk eps_kappa_dot + CGM eps_Meff_dot + CGK eps_memory_kernel_drift",
        "terms": 3,
        "equal_share_ceiling": "3.2e-15 yr^-1",
        "stricter_equal_share_ceiling": "",
        "status": "contingent_budget_only_if_secular_G_channel_exists",
    },
]


EPSILON_CHANNELS = [
    {
        "epsilon": "eps_B0i",
        "meaning": "boundary vector component surviving in local exterior",
        "theorem_zero_route": "class-only boundary action plus regular source-free vector equation",
        "observable_rows": "alpha1;alpha2",
        "current_status": "not_zero_derived",
    },
    {
        "epsilon": "eps_domain_vec",
        "meaning": "domain selector carries a preferred local velocity/frame",
        "theorem_zero_route": "covariant scalar/topological domain selector with no physical marker vector",
        "observable_rows": "alpha1;alpha2;xi",
        "current_status": "not_zero_derived",
    },
    {
        "epsilon": "eps_P_vector",
        "meaning": "projector/relative-chain representative has vector leakage",
        "theorem_zero_route": "metric-independent topological projector and representative gauge invariance",
        "observable_rows": "alpha1;alpha2",
        "current_status": "conditional_only",
    },
    {
        "epsilon": "eps_coframe_slip",
        "meaning": "observed coframe has a vector offset relative to metric/matter frame",
        "theorem_zero_route": "one parent-selected observed coframe for all matter and light",
        "observable_rows": "alpha1;clock;WEP",
        "current_status": "closure_axiom_required",
    },
    {
        "epsilon": "eps_unowned_flux",
        "meaning": "boundary/projector/domain momentum flux not balanced in Ward identity",
        "theorem_zero_route": "total Ward ledger owns selector stress and boundary flux",
        "observable_rows": "alpha3;Gdot;secular_drift",
        "current_status": "Ward_ownership_open",
    },
    {
        "epsilon": "eps_TF_lge2",
        "meaning": "trace-free l>=2 boundary shear/anisotropy",
        "theorem_zero_route": "class-only boundary action and no angular representative",
        "observable_rows": "xi;gamma;lensing_slip",
        "current_status": "not_zero_derived",
    },
    {
        "epsilon": "eps_external_domain_aniso",
        "meaning": "external-domain preferred-location anisotropy",
        "theorem_zero_route": "domain class depends on invariant scalars only, not external direction markers",
        "observable_rows": "xi",
        "current_status": "not_zero_derived",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "preferred_frame_alpha1",
        "before_376": "source_locked_budget_row_coefficients_missing",
        "after_376": "symbolic_coefficient_map_written",
        "claim_status": "budget_only_no_pass",
    },
    {
        "runner_row": "preferred_frame_alpha2",
        "before_376": "source_locked_budget_row_coefficients_missing",
        "after_376": "symbolic_coefficient_map_written",
        "claim_status": "budget_only_no_pass",
    },
    {
        "runner_row": "preferred_frame_alpha3",
        "before_376": "contingent_source_locked_row",
        "after_376": "flux/momentum nonconservation map written",
        "claim_status": "contingent_budget_only_no_pass",
    },
    {
        "runner_row": "xi_preferred_location_anisotropy",
        "before_376": "source_locked_budget_row_coefficients_missing",
        "after_376": "tracefree/domain anisotropy map written",
        "claim_status": "budget_only_no_pass",
    },
    {
        "runner_row": "Gdot_over_G",
        "before_376": "contingent_source_locked_row",
        "after_376": "secular source-normalization/flux map referenced",
        "claim_status": "contingent_budget_only_no_pass",
    },
]


FAILURE_MODES = [
    {
        "failure": "vector_nohair_assumed_from_covariance",
        "meaning": "assuming covariance removes all preferred-frame terms without proving marker/domain vectors are gauge",
        "consequence": "false alpha1/alpha2 pass",
    },
    {
        "failure": "alpha3_applied_unconditionally",
        "meaning": "using alpha3 bound even when MTS has no momentum-nonconservation/preferred-frame channel",
        "consequence": "unfair over-penalty instead of contingent guardrail",
    },
    {
        "failure": "xi_folded_into_gamma",
        "meaning": "treating trace-free anisotropy as ordinary gamma residual only",
        "consequence": "preferred-location row hidden",
    },
    {
        "failure": "coframe_slip_hidden_in_WEP",
        "meaning": "letting matter/light see different vector-shifted frames while claiming one observed coframe",
        "consequence": "WEP/clock/preferred-frame channels reopen",
    },
    {
        "failure": "flux_erased_not_owned",
        "meaning": "setting boundary/domain momentum flux to zero without Ward ownership",
        "consequence": "fake Bianchi closure and unsafe alpha3/Gdot claims",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Vector/preferred-frame no-hair is conditionally clear if marker/domain/projector vectors are gauge, boundary action is class-only, local vector equations are source-free/regular, and Ward flux is owned. Those premises are not parent-derived, so alpha1/alpha2/alpha3/xi/Gdot remain budget-only coefficient rows.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive alpha_Y(lambda_Y) or another source-normalized force residual for scalar/bulk/phi_C/nonlocal fifth-force channels",
        "pass_condition": "fifth-force row becomes scalar/range scorable or remains explicitly unscored",
    },
    {
        "priority": 2,
        "target": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "task": "derive kappa, G_eff, M_eff, and measured-GM absorption or keep delta_G/Gdot rows active",
        "pass_condition": "Newtonian source normalization is parent-derived or source-bounded",
    },
    {
        "priority": 3,
        "target": "379-class-only-boundary-action-noangular-theorem.md",
        "task": "attempt the class-only boundary action theorem that would kill B_0i and trace-free angular shear",
        "pass_condition": "boundary vector/shear sources are theorem-zero or retained as coefficients",
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
            "gate": "source_locked_preferred_frame_rows_loaded",
            "status": "pass",
            "evidence": "alpha1, alpha2, alpha3, xi, and contingent Gdot rows imported from checkpoint 374",
        },
        {
            "gate": "vector_nohair_conditional_theorem_written",
            "status": "conditional_pass",
            "evidence": "premise stack written for gauge marker vectors, class-only boundary action, regular vector equation, and Ward-owned flux",
        },
        {
            "gate": "parent_vector_nohair_derived",
            "status": "fail",
            "evidence": "marker/domain/projector gauge status, class-only boundary action, and vector operator are not parent-derived",
        },
        {
            "gate": "preferred_frame_coefficient_map_written",
            "status": "pass",
            "evidence": f"{len(PREFERRED_FRAME_COEFFICIENT_MAP)} residual maps written",
        },
        {
            "gate": "equal_share_budgets_written",
            "status": "pass",
            "evidence": "alpha1, alpha2, alpha3, xi, and Gdot budget ceilings recorded",
        },
        {
            "gate": "PPN_or_preferred_frame_pass_claimed",
            "status": "fail",
            "evidence": "MTS coefficients remain missing",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "vector no-hair is conditional and EH/source/WEP/fifth-force gates remain open",
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
    write_csv(results_dir / "vector_nohair_premises.csv", VECTOR_NOHAIR_PREMISES)
    write_csv(results_dir / "vector_nohair_attempt_steps.csv", VECTOR_NOHAIR_ATTEMPT_STEPS)
    write_csv(results_dir / "preferred_frame_coefficient_map.csv", PREFERRED_FRAME_COEFFICIENT_MAP)
    write_csv(results_dir / "epsilon_channels.csv", EPSILON_CHANNELS)
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
        "preferred_frame_maps_written": len(PREFERRED_FRAME_COEFFICIENT_MAP),
        "parent_vector_nohair_derived": False,
        "preferred_frame_pass_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 376 preferred-frame coefficient map or vector no-hair theorem artifacts."
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
