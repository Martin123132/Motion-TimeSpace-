from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "kappa-Geff-local-constancy-lemma"
CHECKPOINT_DOC = "433-kappa-Geff-local-constancy-lemma.md"
STATUS = "kappa_Geff_local_constancy_lemma_written_Bianchi_forces_constancy_only_under_same_frame_conserved_source_premises_not_parent_derived_no_local_GR_pass"
CLAIM_CEILING = "kappa_Geff_local_constancy_lemma_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "434-measured-GM-mu-extra-zero-route.md"


SOURCE_DOCS = [
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "EH/source-normalization pair and kappa-to-G_eff bridge",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "Poisson reduction requires constant universal kappa and measured GM",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "source-normalization channel plan and local bound rows",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Bianchi identity with T_obs nabla kappa_eff source residual term",
    },
    {
        "path": "430-Ward-source-residual-zero-route-gate.md",
        "role": "C5 constant kappa/G_eff route ranking",
    },
    {
        "path": "432-same-frame-matter-functor-zero-route.md",
        "role": "C0 same-frame matter functor remains conditional",
    },
    {
        "path": "runs/20260602-025500-source-normalized-Newtonian-limit-under-identity-closure/results/source_normalization_contract.csv",
        "role": "machine-readable source-normalization contracts",
    },
    {
        "path": "runs/20260602-025500-source-normalized-Newtonian-limit-under-identity-closure/results/weak_field_derivation_steps.csv",
        "role": "weak-field chain defining G_eff and mu_obs",
    },
    {
        "path": "runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/absorption_gate_matrix.csv",
        "role": "GM absorption gates including G_eff constancy and universality",
    },
    {
        "path": "runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/failure_modes.csv",
        "role": "source-normalization failure modes",
    },
    {
        "path": "runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/decision.csv",
        "role": "previous decision retaining deltaG/Gdot/WEP/beta/fifth-force rows",
    },
    {
        "path": "runs/20260602-103000-Ward-source-residual-zero-route-gate/results/route_ranking.csv",
        "role": "C5 hard source-normalization route",
    },
]


CONSTANCY_LEMMA_CHAIN = [
    {
        "step": 1,
        "claim": "Work in one observed frame with an EH-shaped local exterior equation.",
        "mathematical_form": "G_munu[g_obs]+Lambda g_obs_munu = kappa_eff(x,Z,A,lambda) T_obs_munu + S_extra_munu",
        "status": "conditional_branch_only",
        "meaning": "this is not yet parent-derived; it is the local GR-corner test branch",
    },
    {
        "step": 2,
        "claim": "Take the covariant divergence in the observed frame.",
        "mathematical_form": "0 = nabla_mu G^mu_nu = (nabla_mu kappa_eff) T_obs^mu_nu + kappa_eff nabla_mu T_obs^mu_nu + nabla_mu S_extra^mu_nu",
        "status": "identity_pass",
        "meaning": "Bianchi exposes the kappa-gradient exchange term",
    },
    {
        "step": 3,
        "claim": "Impose same-frame matter conservation and no extra exchange.",
        "mathematical_form": "nabla_mu T_obs^mu_nu=0 and nabla_mu S_extra^mu_nu=0 or S_extra=0 in the local exterior",
        "status": "conditional_not_parent_derived",
        "meaning": "requires C0/C1/C3/C4/C7 debts to be silent or retained",
    },
    {
        "step": 4,
        "claim": "For arbitrary ordinary matter stresses, kappa_eff must be locally constant.",
        "mathematical_form": "T_obs^mu_nu nabla_mu kappa_eff=0 for all allowed local T_obs implies nabla_mu kappa_eff=0",
        "status": "conditional_theorem",
        "meaning": "Bianchi can force constancy only when matter stress has enough rank and the branch is source-universal",
    },
    {
        "step": 5,
        "claim": "Vacuum alone cannot prove the plateau.",
        "mathematical_form": "T_obs=0 gives 0=0 for the kappa-gradient term",
        "status": "counterexample_warning",
        "meaning": "a pure local-vacuum plateau axiom would be smuggled, not derived",
    },
    {
        "step": 6,
        "claim": "Convert constant kappa_eff to constant G_eff only in the EH/source unit convention.",
        "mathematical_form": "G_eff = kappa_eff c^4/(8 pi)",
        "status": "algebra_pass_conditional_context",
        "meaning": "absolute calibration and physical mass units remain separate source-normalization debts",
    },
    {
        "step": 7,
        "claim": "Species, source, and range independence are not automatic from spacetime constancy.",
        "mathematical_form": "partial_A kappa_eff = partial_source kappa_eff = partial_lambda kappa_eff = 0",
        "status": "not_parent_derived",
        "meaning": "universality needs its own theorem or retained empirical rows",
    },
]


KAPPA_CONSTANCY_REQUIREMENTS = [
    {
        "requirement": "same_observed_frame",
        "needed_form": "matter, photons, clocks, rods, and source definitions use g_obs/e_obs",
        "current_status": "conditional_from_C0_not_parent_derived",
        "if_missing": "kappa can look constant in one frame while measured matter sees another",
        "rows_at_risk": "R0;R2;R3;R4;R11",
    },
    {
        "requirement": "EH_or_Bianchi_closed_operator",
        "needed_form": "nabla_mu E_metric^mu_nu = 0 with E_metric=G+Lambda g in the local branch",
        "current_status": "conditional_Lovelock_route_not_parent_derived",
        "if_missing": "non-EH divergence can cancel kappa drift",
        "rows_at_risk": "R3;R4;R10;R11",
    },
    {
        "requirement": "separate_matter_conservation",
        "needed_form": "nabla_mu T_obs^mu_nu=0 on matter shell",
        "current_status": "conditional_on_same_frame_matter_functor",
        "if_missing": "matter exchange can absorb nabla kappa",
        "rows_at_risk": "R1;R7;R9;R10",
    },
    {
        "requirement": "no_extra_exchange_stress",
        "needed_form": "nabla_mu S_extra^mu_nu=0 or S_extra retained below bounds",
        "current_status": "not_derived",
        "if_missing": "boundary, domain, projector, or auxiliary exchange cancels T nabla kappa",
        "rows_at_risk": "R3;R4;R7;R8;R9;R10;R11",
    },
    {
        "requirement": "arbitrary_matter_stress_domain",
        "needed_form": "the theorem holds for dust, pressure, EM, clock matter, and composite sources",
        "current_status": "assumption_needed_for_theorem",
        "if_missing": "T^mu_nu nabla_mu kappa=0 may only constrain one projection",
        "rows_at_risk": "R1;R2;R4;R9",
    },
    {
        "requirement": "species_universal_coupling",
        "needed_form": "partial_A kappa_eff=0 and partial_A ln mu_obs=0",
        "current_status": "not_parent_derived",
        "if_missing": "source-normalization WEP charge survives",
        "rows_at_risk": "R1",
    },
    {
        "requirement": "range_independent_coupling",
        "needed_form": "partial_lambda kappa_eff=0 and alpha(lambda)=0 or executable",
        "current_status": "symbolic_deferred",
        "if_missing": "finite-range force is hidden as G_eff(r,lambda)",
        "rows_at_risk": "R10",
    },
    {
        "requirement": "absolute_unit_calibration",
        "needed_form": "one parent-fixed conversion between curvature coefficient, physical mass, and measured GM",
        "current_status": "not_parent_derived",
        "if_missing": "constant kappa is fitted normalization, not measured Newton source proof",
        "rows_at_risk": "R4;R9",
    },
]


BIANCHI_CASE_ANALYSIS = [
    {
        "case_id": "vacuum_only",
        "assumptions": "T_obs=0 and S_extra=0",
        "result": "Bianchi gives no constraint on kappa_eff gradient",
        "verdict": "reject_as_plateau_proof",
    },
    {
        "case_id": "single_dust_flow",
        "assumptions": "T_obs^mu_nu=rho u^mu u^nu with conserved matter",
        "result": "u^mu nabla_mu kappa_eff=0 along that flow only",
        "verdict": "partial_projection_not_full_constancy",
    },
    {
        "case_id": "arbitrary_matter_family",
        "assumptions": "conserved same-frame matter stresses span local timelike/null directions",
        "result": "nabla_mu kappa_eff=0 in the tested local domain",
        "verdict": "conditional_constancy_theorem",
    },
    {
        "case_id": "exchange_owned_but_nonzero",
        "assumptions": "nabla S_extra cancels T_obs nabla kappa_eff",
        "result": "total Ward identity holds while measured G_eff drifts",
        "verdict": "retained_residual_not_GR",
    },
    {
        "case_id": "scalar_kappa_field",
        "assumptions": "kappa_eff=kappa(phi) with phi equation and stress",
        "result": "can be covariant but becomes scalar-tensor/fifth-force branch unless phi is constant",
        "verdict": "modified_gravity_or_bound_route",
    },
    {
        "case_id": "species_or_range_dependent_kappa",
        "assumptions": "kappa_eff(A,lambda) differs by composition or force range",
        "result": "spacetime Bianchi constancy is insufficient for measured universality",
        "verdict": "R1_R10_retained",
    },
]


SOURCE_RESIDUAL_IMPLICATIONS = [
    {
        "term": "delta_kappa_source",
        "zero_route": "derive nabla_mu kappa_eff=0 and partial_A/source/lambda kappa_eff=0",
        "current_status": "conditional_spacetime_constancy_only_not_parent_derived",
        "residual_rows": "R1;R4;R9;R10",
    },
    {
        "term": "T_obs nabla kappa_eff",
        "zero_route": "Bianchi plus same-frame separate matter conservation plus arbitrary stress",
        "current_status": "conditional_theorem_shape",
        "residual_rows": "R9;R10",
    },
    {
        "term": "species_source_charge",
        "zero_route": "derive one universal kappa/source normalization for all compositions",
        "current_status": "not_derived",
        "residual_rows": "R1",
    },
    {
        "term": "time_drift",
        "zero_route": "derive partial_t ln(G_eff M_eff)=0",
        "current_status": "not_derived",
        "residual_rows": "R9",
    },
    {
        "term": "range_dependence",
        "zero_route": "derive no finite-range mediator or supply alpha(lambda) curve",
        "current_status": "symbolic_deferred",
        "residual_rows": "R10",
    },
    {
        "term": "absolute_calibration",
        "zero_route": "derive parent-fixed physical units and Pi_M-to-M_eff calibration",
        "current_status": "not_parent_derived",
        "residual_rows": "R4;R9",
    },
]


BOUND_FALLBACK_MATRIX = [
    {
        "quantity_if_not_derived": "partial_t ln G_eff",
        "runner_row": "R9_Gdot",
        "bound_or_required_data": "9.6e-15 yr^-1 source lock from local ledger",
        "action": "score numeric drift; no theorem-zero credit",
    },
    {
        "quantity_if_not_derived": "partial_A ln mu_obs",
        "runner_row": "R1_WEP_source_charge",
        "bound_or_required_data": "2.8e-15 source-normalization/WEP lock from local ledger",
        "action": "keep four-channel R1 source subscore",
    },
    {
        "quantity_if_not_derived": "range-dependent delta G or alpha(lambda)",
        "runner_row": "R10_fifth_force",
        "bound_or_required_data": "executable alpha(lambda) curve required",
        "action": "symbolic row cannot pass",
    },
    {
        "quantity_if_not_derived": "nonlinear source-normalization shift",
        "runner_row": "R4_beta",
        "bound_or_required_data": "7.8e-05 beta/source-normalization lock from local ledger",
        "action": "score beta/source residual separately from direct Poisson algebra",
    },
    {
        "quantity_if_not_derived": "boundary/domain/projector mass flux",
        "runner_row": "R3;R4;R7;R8;R9;R11",
        "bound_or_required_data": "retained coefficient vector plus Ward-owned flux evidence",
        "action": "do not absorb as measured GM",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "Bianchi can force local spacetime constancy of kappa_eff",
        "status": "conditional_pass",
        "evidence": "if same-frame matter is separately conserved, extra exchange is zero, and matter stresses are arbitrary",
    },
    {
        "claim": "vacuum plateau derives kappa constancy",
        "status": "fail",
        "evidence": "T_obs=0 makes the kappa-gradient term vanish identically",
    },
    {
        "claim": "current MTS parent action derives constant universal G_eff",
        "status": "fail",
        "evidence": "C0 same-frame, EH selection, exchange silence, and source normalization remain unproved",
    },
    {
        "claim": "spacetime constancy solves species/source/range universality",
        "status": "fail",
        "evidence": "partial_A, source calibration, and alpha(lambda) debts are independent of nabla_mu kappa",
    },
    {
        "claim": "C5 row can be promoted to local-GR theorem-zero",
        "status": "fail",
        "evidence": "0 residual row upgrades; bound fallback remains required",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "constancy_lemma_chain_written",
        "status": "pass",
        "evidence": "7 Bianchi/constancy stages recorded",
    },
    {
        "gate": "vacuum_plateau_rejected",
        "status": "pass",
        "evidence": "vacuum T=0 cannot constrain kappa_eff gradient",
    },
    {
        "gate": "conditional_Bianchi_constancy_written",
        "status": "conditional_pass",
        "evidence": "T_obs^mu_nu nabla_mu kappa_eff=0 implies nabla kappa=0 only for arbitrary conserved same-frame stresses",
    },
    {
        "gate": "same_frame_parent_derived",
        "status": "fail",
        "evidence": "C0 remains closure/conditional from checkpoint 432",
    },
    {
        "gate": "EH_operator_parent_derived",
        "status": "fail",
        "evidence": "non-EH operator ledger remains retained",
    },
    {
        "gate": "extra_exchange_silenced",
        "status": "fail",
        "evidence": "boundary/domain/projector/auxiliary exchange terms remain retained or open",
    },
    {
        "gate": "species_source_range_universality_derived",
        "status": "fail",
        "evidence": "spacetime Bianchi constancy does not prove partial_A/source/lambda independence",
    },
    {
        "gate": "absolute_calibration_derived",
        "status": "fail",
        "evidence": "Pi_M-to-M_eff and physical GM calibration remain source-normalization debts",
    },
    {
        "gate": "runner_rows_promoted_to_theorem_zero",
        "status": "fail",
        "evidence": "0 row upgrades; R1/R4/R9/R10 remain retained or symbolic",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "C5 lemma attempt only; no Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The C5 kappa/G_eff route gets a real conditional lemma: in a same-frame EH branch with separately conserved matter, no extra exchange stress, and arbitrary ordinary matter stresses, Bianchi forces nabla_mu kappa_eff=0, so G_eff=kappa_eff c^4/(8 pi) is locally spacetime-constant in that branch. But vacuum alone cannot prove this, and the current MTS parent action has not derived the required same-frame, EH-selection, exchange-silence, species-universality, range-independence, or absolute source-calibration premises. Therefore C5 is sharpened but not promoted; R1/R4/R9/R10 remain retained or symbolic.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "434-measured-GM-mu-extra-zero-route.md",
        "why_next": "even constant kappa does not prove mu_obs=G_eff M_eff with no hidden source/time/range/species correction",
    },
    {
        "rank": 2,
        "target": "auxiliary/projector local Euler-equation ledger",
        "why_next": "C1 is still the highest-ranked Ward route for killing off-shell exchange terms",
    },
    {
        "rank": 3,
        "target": "filled MTS local residual vector smoke",
        "why_next": "any non-derived kappa/source terms need numeric or executable residual entries",
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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    return [source_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 433 - Kappa/G_eff Local Constancy Lemma

Private C5/source-normalization derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 432 sharpened the same-frame matter functor but did not derive it. This checkpoint attacks the next source-normalization pressure point: can `kappa_eff/G_eff` be derived constant, universal, and source/species/range independent, or must it remain a retained residual?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/kappa_Geff_local_constancy_lemma.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Constancy Lemma Chain

{markdown_table(CONSTANCY_LEMMA_CHAIN, ["step", "claim", "status", "meaning"])}

Exact conditional lemma:

```text
Assume a same-frame local EH branch:

G_munu[g_obs] + Lambda g_obs_munu
  = kappa_eff(x,Z,A,lambda) T_obs_munu + S_extra_munu.

Bianchi gives

0 = (nabla_mu kappa_eff) T_obs^mu_nu
    + kappa_eff nabla_mu T_obs^mu_nu
    + nabla_mu S_extra^mu_nu.

If nabla_mu T_obs^mu_nu=0, if S_extra is zero or separately conserved,
and if ordinary local matter stresses span the tested directions,
then nabla_mu kappa_eff=0.
```

This proves only a conditional spacetime-constancy lemma. It does not prove species, source, range, or absolute measured-GM universality.

## 5. Kappa Constancy Requirements

{markdown_table(KAPPA_CONSTANCY_REQUIREMENTS, ["requirement", "current_status", "if_missing", "rows_at_risk"])}

## 6. Bianchi Case Analysis

{markdown_table(BIANCHI_CASE_ANALYSIS, ["case_id", "result", "verdict"])}

## 7. Source-Residual Implications

{markdown_table(SOURCE_RESIDUAL_IMPLICATIONS, ["term", "zero_route", "current_status", "residual_rows"])}

## 8. Bound Fallback Matrix

{markdown_table(BOUND_FALLBACK_MATRIX, ["quantity_if_not_derived", "runner_row", "bound_or_required_data", "action"])}

## 9. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 10. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is one of the better derivation moves so far. Bianchi gives us a genuine pressure mechanism, but only after we stop asking empty vacuum to do the work. The theory has to earn same-frame conserved matter and no extra exchange; then `kappa_eff` has nowhere left to hide.

## 12. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "constancy_lemma_chain.csv", CONSTANCY_LEMMA_CHAIN)
    write_csv(results_dir / "kappa_constancy_requirements.csv", KAPPA_CONSTANCY_REQUIREMENTS)
    write_csv(results_dir / "Bianchi_case_analysis.csv", BIANCHI_CASE_ANALYSIS)
    write_csv(results_dir / "source_residual_implications.csv", SOURCE_RESIDUAL_IMPLICATIONS)
    write_csv(results_dir / "bound_fallback_matrix.csv", BOUND_FALLBACK_MATRIX)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
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
        "constancy_lemma_chain_steps": len(CONSTANCY_LEMMA_CHAIN),
        "kappa_constancy_requirements": len(KAPPA_CONSTANCY_REQUIREMENTS),
        "Bianchi_cases": len(BIANCHI_CASE_ANALYSIS),
        "conditional_spacetime_constancy_lemma": True,
        "vacuum_plateau_rejected": True,
        "same_frame_parent_derived": False,
        "EH_operator_parent_derived": False,
        "extra_exchange_silenced": False,
        "species_source_range_universality_derived": False,
        "absolute_calibration_derived": False,
        "theorem_zero_upgrades": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 433 kappa/G_eff local constancy lemma artifacts."
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
