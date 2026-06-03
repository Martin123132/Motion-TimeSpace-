from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "C3-unit-stress-normalization-parent-action-attempt"
STATUS = "C3a_metric_variation_stress_form_derived_C3b_unit_scale_lock_not_derived"
CLAIM_CEILING = "partial_C3_derivation_no_unit_amplitude_promotion"
B_MEM_FIXED = 2.0 / 27.0
SOURCE_258 = ROOT / "runs" / "20260601-000076-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation" / "results"
SOURCE_259 = ROOT / "runs" / "20260601-000077-memory-stress-normalization-theorem-attempt" / "results"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "252-topological-projector-parent-action-skeleton.md", "local topological parent skeleton"),
        (ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md", "FLRW projector reduction checkpoint"),
        (ROOT / "255-memory-stress-exchange-normalization-or-kappa-mem-free.md", "kappa no-go checkpoint"),
        (ROOT / "258-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation.md", "fixed-vs-kappa empirical anchor"),
        (ROOT / "259-memory-stress-normalization-theorem-attempt.md", "conditional kappa=1 theorem contract"),
        (SOURCE_258 / "fixed_vs_kappa_penalty.csv", "258 kappa penalty row"),
        (SOURCE_259 / "conditional_theorem_status.csv", "259 theorem status row"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def variational_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Use an FLRW minisuperspace memory action S_mem=-int dt lapse*a^3*A_mem*q*F(N)",
            "formula": "N=ln(a0/a), q=r_active/D_cell",
            "status": "ansatz_for_FLRW_reduction",
            "claim_limit": "does not yet define the full local covariant parent action",
        },
        {
            "step": 2,
            "statement": "Lapse variation gives the memory energy density",
            "formula": "rho_mem=A_mem*q*F(N)",
            "status": "derived_within_FLRW_action",
            "claim_limit": "normalization is A_mem, not fixed yet",
        },
        {
            "step": 3,
            "statement": "Scale-factor variation gives the pressure law",
            "formula": "p_mem=-rho_mem-(a/3)*d rho_mem/da = -rho_mem + (1/3)*d rho_mem/dN",
            "status": "derived_within_FLRW_action",
            "claim_limit": "matches Bianchi pressure without adding a pressure closure by hand",
        },
        {
            "step": 4,
            "statement": "The dimensionless cosmology amplitude factorizes",
            "formula": "B_mem=(A_mem/rho_c0)*q = kappa_mem*q",
            "status": "derived_factorization",
            "claim_limit": "C3 unit normalization is equivalent to A_mem=rho_c0",
        },
        {
            "step": 5,
            "statement": "For q=2/27, fixed branch follows only if A_mem=rho_c0",
            "formula": "B_mem=2/27 iff D_cell=27, r_active=2, and A_mem/rho_c0=1",
            "status": "conditional_only",
            "claim_limit": "unit scale lock remains missing",
        },
    ]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "pure_topological_wedge_parent",
            "action_form": "Xi wedge dJ + Upsilon wedge(P_D J-dA)",
            "metric_variation": "zero_bulk_stress",
            "A_mem_result": "0",
            "C3_result": "fails_FLRW_stress",
            "verdict": "good_for_local_silence_not_for_cosmology_amplitude",
        },
        {
            "route": "FLRW_volume_memory_potential",
            "action_form": "-int sqrt(-g) A_mem q F[ln(a0/a)]",
            "metric_variation": "rho=A_mem qF and p=-rho+rho_prime/3",
            "A_mem_result": "free_scale_unless_fixed_elsewhere",
            "C3_result": "C3a_pass_C3b_fail",
            "verdict": "derives_stress_form_but_not_unit_amplitude",
        },
        {
            "route": "critical_density_inserted_action",
            "action_form": "-int sqrt(-g) rho_c0 q F[ln(a0/a)]",
            "metric_variation": "rho=rho_c0 qF",
            "A_mem_result": "rho_c0_by_assumption",
            "C3_result": "formally_passes_but_smuggles_scale",
            "verdict": "closure_written_as_action_unless_rho_c0_scale_lock_is_parent_derived",
        },
        {
            "route": "geometric_EH_scale_lock",
            "action_form": "(M_Pl^2/2)int sqrt(-g)[R-6 H_star^2 qF]",
            "metric_variation": "rho=3 M_Pl^2 H_star^2 qF plus pressure terms",
            "A_mem_result": "rho_c0*(H_star^2/H0^2)",
            "C3_result": "passes_only_if_H_star=H0_is_derived",
            "verdict": "best_route_if_boundary_scale_lock_can_be_proved",
        },
        {
            "route": "four_form_or_flux_memory",
            "action_form": "-1/2 int F4 wedge star F4 plus projector coupling",
            "metric_variation": "cosmological_constant_like_stress_from_flux",
            "A_mem_result": "flux_or_integration_constant",
            "C3_result": "not_unit_without_flux_quantization_and_scale_match",
            "verdict": "may quantize amplitude_but_does_not_currently_select_rho_c0",
        },
        {
            "route": "lagrange_multiplier_density_constraint",
            "action_form": "int sqrt(-g) lambda[rho/rho_c0-qF]",
            "metric_variation": "enforces target by constraint",
            "A_mem_result": "chosen_constraint",
            "C3_result": "tautological_unless_lambda_constraint_is_parent_owned",
            "verdict": "not acceptable as derivation by itself",
        },
    ]


def theorem_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "C3a_metric_variation_stress_form",
            "required_statement": "A parent FLRW reduction varies to rho_mem=A_mem qF and p_mem=-rho_mem+rho_mem_prime/3",
            "status": "derived_conditionally",
            "evidence": "FLRW volume memory action gives both lapse and scale-factor variations",
            "next_action": "embed this FLRW reduction in the full covariant/topological parent action",
        },
        {
            "gate": "C3b_unit_scale_lock",
            "required_statement": "A_mem=rho_c0 with no independent lambda_mem, H_star, flux, or integration constant",
            "status": "not_derived",
            "evidence": "all acceptable stress-producing routes contain A_mem or H_star unless scale lock is assumed",
            "next_action": "derive H_star=H0 or equivalent critical-density normalization from boundary/Noether/Hamiltonian structure",
        },
        {
            "gate": "C3c_local_silence_compatibility",
            "required_statement": "The stress-producing cosmology sector must reduce to zero bulk projector stress in local vacuum",
            "status": "open",
            "evidence": "pure topological route is locally silent; volume stress route is cosmological and needs domain/gating compatibility",
            "next_action": "prove the volume stress is FLRW-only or boundary-common-mode silent locally",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "unit_scale_rescaling_no_go",
            "proof": "Replacing A_mem by lambda*A_mem leaves the variational stress form and Bianchi identity intact while changing B_mem.",
            "consequence": "metric variation and conservation alone cannot choose lambda=1",
        },
        {
            "lemma": "critical_density_insert_no_go",
            "proof": "Writing rho_c0 directly in S_mem produces kappa=1 only because the desired normalization was inserted.",
            "consequence": "rho_c0 must be derived as a parent boundary/integration scale, not typed into the action as a fit convenience",
        },
        {
            "lemma": "local_topology_vs_FLRW_stress_tension",
            "proof": "The local route wants metric-independent wedge terms; the FLRW route needs a metric-volume stress term.",
            "consequence": "the unified action must split topological ownership from metric stress without reintroducing local PPN stress",
        },
        {
            "lemma": "H_star_over_H0_degeneracy",
            "proof": "A geometric term with scale H_star predicts B_mem=q(H_star/H0)^2.",
            "consequence": "unit kappa is equivalent to the new theorem H_star=H0",
        },
    ]


def empirical_rows() -> list[dict[str, Any]]:
    penalty = read_csv(SOURCE_258 / "fixed_vs_kappa_penalty.csv")
    if not penalty:
        return [{"quantity": "258_penalty", "value": "missing", "interpretation": "no imported anchor"}]
    row = penalty[0]
    return [
        {
            "quantity": "fixed_B_mem",
            "value": row["fixed_B_mem"],
            "interpretation": "closure branch amplitude",
        },
        {
            "quantity": "free_B_mem",
            "value": row["kappa_best_B_mem"],
            "interpretation": "best free amplitude on 258 short smoke",
        },
        {
            "quantity": "kappa_best",
            "value": row["kappa_best_kappa_mem"],
            "interpretation": "near unity but not promoted",
        },
        {
            "quantity": "AIC_BIC_tax_paid",
            "value": f"AIC={row['AIC_tax_paid']}; BIC={row['BIC_tax_paid']}",
            "interpretation": "extra amplitude fails information-criterion tax",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "C3 metric stress form has a conditional FLRW derivation",
            "status": "allowed",
            "reason": "volume memory action yields rho and p with the Bianchi pressure law",
        },
        {
            "claim": "C3 unit normalization is derived",
            "status": "forbidden",
            "reason": "A_mem=rho_c0 or H_star=H0 remains an unproved scale lock",
        },
        {
            "claim": "fixed 2/27 is still the clean lead branch",
            "status": "allowed",
            "reason": "258 says free kappa does not pay tax and 260 says unit amplitude is not yet parent-owned",
        },
        {
            "claim": "a pure topological parent action can supply FLRW stress amplitude",
            "status": "forbidden",
            "reason": "metric-independent wedge terms have zero bulk metric stress",
        },
        {
            "claim": "the next theorem is H_star=H0 or A_mem=rho_c0 from parent structure",
            "status": "allowed",
            "reason": "C3b has been isolated as the exact missing step",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "meaning": (
                "C3 splits into a won sub-gate and an open sub-gate. The FLRW memory action can derive the stress form and "
                "Bianchi pressure law, so the route is not empty. But unit normalization still reduces to A_mem=rho_c0, "
                "or equivalently H_star=H0, and that scale-lock theorem is not derived."
            ),
            "next_target": "derive_or_reject_Hstar_equals_H0_boundary_scale_lock_and_local_silence_compatibility",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "FLRW_variational_derivation.csv": (
            variational_derivation_rows(),
            ["step", "statement", "formula", "status", "claim_limit"],
        ),
        "parent_action_route_matrix.csv": (
            route_rows(),
            ["route", "action_form", "metric_variation", "A_mem_result", "C3_result", "verdict"],
        ),
        "C3_theorem_split.csv": (
            theorem_split_rows(),
            ["gate", "required_statement", "status", "evidence", "next_action"],
        ),
        "C3_no_go_lemmas.csv": (
            no_go_rows(),
            ["lemma", "proof", "consequence"],
        ),
        "empirical_anchor_from_258.csv": (
            empirical_rows(),
            ["quantity", "value", "interpretation"],
        ),
        "claim_policy_after_260.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "next_target"],
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
        "C3a_metric_variation_stress_form": "derived_conditionally",
        "C3b_unit_scale_lock": "not_derived",
        "C3c_local_silence_compatibility": "open",
        "B_mem_fixed": B_MEM_FIXED,
        "next_target": "derive_or_reject_Hstar_equals_H0_boundary_scale_lock_and_local_silence_compatibility",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Attempt the C3 unit stress normalization parent-action derivation.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
