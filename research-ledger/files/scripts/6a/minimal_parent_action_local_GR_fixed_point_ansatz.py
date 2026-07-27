from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "minimal_parent_action_local_GR_fixed_point_ansatz_constructed_not_adopted_current_MTS_derivation_contract_written"
CLAIM_CEILING = "candidate_parent_action_contract_only_no_local_GR_promotion_until_MTS_terms_match_and_pass"
NEXT_TARGET = "512-match-MTS-symbols-to-local-GR-action-blocks.md"

DOC_PATH = Path("511-minimal-parent-action-local-GR-fixed-point-ansatz.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_SOURCE_REGISTER.csv")
ACTION_BLOCKS_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv")
FIXED_POINT_CONDITIONS_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv")
DERIVED_CHAIN_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv")
RESIDUAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_GATE_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube source-measure glue theorem route and M_eff residual runner",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "positive source-free operator plus zero boundary/source charge silence mechanism",
    },
    {
        "source_file": "508-constant-kappa-superselection-or-drift-residual.md",
        "role": "topological/global kappa constancy route",
    },
    {
        "source_file": "507-field-specific-silence-queue-kappa-domain-memory-motion.md",
        "role": "sector queue for kappa, domain, memory, motion/time, and boundary silence",
    },
    {
        "source_file": "347-local-GR-parent-reduction-theorem-attempt.md",
        "role": "earlier parent reduction theorem attempt",
    },
    {
        "source_file": "382-parent-local-action-minimal-contract.md",
        "role": "earlier minimal local parent-action contract",
    },
    {
        "source_file": "384-parent-action-first-variation-obstruction-map.md",
        "role": "first-variation obstruction map for local branch",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_REQUIRED_IDENTITIES.csv",
        "role": "required identities for local-zero/parent fixed-point branch",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv",
        "role": "candidate parent local-zero clause using u, h, X, Qcoh, chi_D",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv",
        "role": "EH reduction, source measure, boundary, and projector requirements",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv",
        "role": "promotion gates for local GR residual vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "M_eff residual runner inherited from 510",
    },
    {
        "source_file": "scripts/minimal_parent_action_local_GR_fixed_point_ansatz.py",
        "role": "this checkpoint generator",
    },
]

ACTION_BLOCK_ROWS = [
    {
        "block_id": "A511_0_EH_core",
        "action_block": "S_EH = (2*kappa0)^-1 integral sqrt(-g_obs) (R[g_obs] - 2 Lambda0)",
        "purpose": "provides the local spin-2 metric operator and EH symplectic charge",
        "fixed_point_requirement": "kappa0 constant; Lambda0 locally negligible or background-subtracted",
        "if_missing": "no GR charge/operator core exists to inherit",
    },
    {
        "block_id": "A511_1_kappa_topological",
        "action_block": "S_kappa_top = integral kappa_eff dA_3",
        "purpose": "makes kappa_eff an integration constant/global sector rather than a local scalar calibration",
        "fixed_point_requirement": "variation in A_3 gives d kappa_eff=0 on connected local domains",
        "if_missing": "G_eff/kappa drift remains a residual",
    },
    {
        "block_id": "A511_2_universal_matter",
        "action_block": "S_matter[psi, g_obs] with no leading species-dependent coupling to extra MTS fields",
        "purpose": "locks the source frame, WEP, and Hilbert source current",
        "fixed_point_requirement": "delta S_matter/dg_obs defines the same source current used by the Noether charge",
        "if_missing": "source mass and orbital mass can separate",
    },
    {
        "block_id": "A511_3_extra_field_silence",
        "action_block": "S_extra = integral sqrt(-g)[-1/2 G_AB(Phi) grad Phi^A grad Phi^B - V(Phi) + C(Phi) R + ...]",
        "purpose": "contains motion/time/domain/memory/range fields without letting them source local GR residuals",
        "fixed_point_requirement": "Phi=Phi0; dV(Phi0)=0; Hessian(V)>0; C(Phi0)=0; dC(Phi0)=0",
        "if_missing": "extra fields create scalar/vector/tensor charge hair",
    },
    {
        "block_id": "A511_4_domain_projector_selector",
        "action_block": "S_selector[u,h,X,Qcoh,chi_D] as constraint/topological/positive operator sector",
        "purpose": "owns the domain/projector variables before cosmology or local readout",
        "fixed_point_requirement": "local stationary compact branch gives X_D=0, Qcoh_D=0, projector stress=0",
        "if_missing": "domain projector becomes a preferred-frame or source-normalization patch",
    },
    {
        "block_id": "A511_5_boundary_reference",
        "action_block": "S_boundary = S_GHY[g_obs] + exact/topological terms with fixed reference subtraction",
        "purpose": "makes the Hamiltonian/Noether charge finite and prevents hidden boundary mass flux",
        "fixed_point_requirement": "extra boundary variation vanishes or is a fixed topological constant in local exterior",
        "if_missing": "worldtube/source-measure equality shifts by boundary bookkeeping",
    },
    {
        "block_id": "A511_6_metric_readout",
        "action_block": "g_readout = g_obs + O((Phi-Phi0)^2) and Pi_M = Pi_EH + O((Phi-Phi0)^2)",
        "purpose": "prevents linear extra-field leakage into Newton/PPN readout",
        "fixed_point_requirement": "no first-order readout coupling; PPN residuals start at explicit bounded second order",
        "if_missing": "a good source-charge theorem can still fail local PPN",
    },
]

FIXED_POINT_ROWS = [
    {
        "condition_id": "FP511_0_stationary_local_vacuum",
        "condition": "There exists a compact/local exterior vacuum branch with Phi=Phi0 and local stationary tau.",
        "mathematical_test": "E_A(Phi0)=0; L_tau Phi0=0; exterior source current J_A=0",
        "derives": "extra-sector equations have a fixed point rather than a manually imposed plateau",
        "current_MTS_status": "not_matched",
    },
    {
        "condition_id": "FP511_1_double_zero_nonEH_coupling",
        "condition": "Every non-EH coupling that can alter the metric charge has a double zero at the local fixed point.",
        "mathematical_test": "C_i(Phi0)=0 and partial_A C_i(Phi0)=0; equivalently F_1=0 for linear leakage",
        "derives": "no first-order fifth-force/source-normalization/PPN hair",
        "current_MTS_status": "required_not_proved",
    },
    {
        "condition_id": "FP511_2_positive_mass_gap",
        "condition": "Non-gauge extra modes have a positive source-free operator in the local exterior.",
        "mathematical_test": "integral_A <delta Phi,L delta Phi> >= m_min^2 ||delta Phi||^2 with zero boundary/source flux",
        "derives": "delta Phi=0 or exponentially suppressed hair",
        "current_MTS_status": "sector_by_sector_open",
    },
    {
        "condition_id": "FP511_3_constant_kappa",
        "condition": "The coupling kappa_eff is a global/topological integration constant locally.",
        "mathematical_test": "d kappa_eff=0 from S_kappa_top or equivalent parent superselection sector",
        "derives": "no G_eff drift or radial kappa hair",
        "current_MTS_status": "conditional_from_508",
    },
    {
        "condition_id": "FP511_4_universal_observed_coframe",
        "condition": "All matter species couple to the same observed metric/coframe at leading local order.",
        "mathematical_test": "partial_A ln m_species(Phi0)=0 and same g_obs for source, clock, and orbital readout",
        "derives": "WEP/source-frame closure",
        "current_MTS_status": "open",
    },
    {
        "condition_id": "FP511_5_parent_PiM_lock",
        "condition": "The mass projector Pi_M is the EH/Hamiltonian mass projector at the fixed point.",
        "mathematical_test": "Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0",
        "derives": "no projector mass calibration freedom",
        "current_MTS_status": "open",
    },
    {
        "condition_id": "FP511_6_boundary_no_flux",
        "condition": "Local linking-sphere and worldtube boundary terms have no extra mass flux.",
        "mathematical_test": "integral_boundary Delta(theta,Q,tau)=0 or fixed background subtraction",
        "derives": "worldtube source-measure glue is not shifted",
        "current_MTS_status": "open",
    },
    {
        "condition_id": "FP511_7_metric_PPN_readout",
        "condition": "The weak-field metric readout around the fixed point matches GR through required PPN order.",
        "mathematical_test": "gamma-1=0, beta-1=0, alpha_i=0, zeta_i=0, xi=0 or explicit residuals below bounds",
        "derives": "local GR rather than only Newton-looking leading order",
        "current_MTS_status": "not_derived",
    },
    {
        "condition_id": "FP511_8_local_cosmology_transition_control",
        "condition": "The same action allows cosmological/nonlocal MTS behaviour without leaking into compact local systems.",
        "mathematical_test": "ell_tr/L_cg or activation functional derived from operator spectrum/source scale, not fitted per system",
        "derives": "local GR and cosmological/galaxy MTS can coexist without hand switching",
        "current_MTS_status": "open",
    },
]

DERIVED_CHAIN_ROWS = [
    {
        "step_id": "DC511_0",
        "premise": "A511_1 kappa topological sector",
        "variation_or_identity": "delta_{A_3} S gives d kappa_eff=0",
        "derived_result": "constant local G_eff/kappa",
        "MTS_status": "conditional",
    },
    {
        "step_id": "DC511_1",
        "premise": "A511_3 extra field fixed point with FP511_1 and FP511_2",
        "variation_or_identity": "linearized extra equation L_AB delta Phi^B = 0 with L positive and no source/boundary flux",
        "derived_result": "delta Phi=0 or bounded exponential hair",
        "MTS_status": "not_field_matched",
    },
    {
        "step_id": "DC511_2",
        "premise": "A511_0 plus silent extra sectors",
        "variation_or_identity": "delta_g S_parent = delta_g S_EH + zero/residual",
        "derived_result": "local metric equation reduces to EH plus explicit residual vector",
        "MTS_status": "conditional",
    },
    {
        "step_id": "DC511_3",
        "premise": "EH charge fixed point plus A511_5 boundary reference",
        "variation_or_identity": "covariant phase-space Noether/Hamiltonian charge reduces to EH charge",
        "derived_result": "worldtube/source-measure glue inherited conditionally",
        "MTS_status": "not_yet_inherited",
    },
    {
        "step_id": "DC511_4",
        "premise": "A511_2 universal matter and FP511_4",
        "variation_or_identity": "same g_obs defines source stress, clocks, and orbital readout",
        "derived_result": "WEP/source-frame closure",
        "MTS_status": "open",
    },
    {
        "step_id": "DC511_5",
        "premise": "A511_6 metric readout and FP511_7",
        "variation_or_identity": "weak-field expansion around fixed point",
        "derived_result": "Newton and PPN residual vector can be computed rather than assumed",
        "MTS_status": "not_done",
    },
]

RESIDUAL_VECTOR_ROWS = [
    {
        "residual_id": "AR511_0_linear_nonEH_leakage",
        "failure": "F_1 or partial_A C_i(Phi0) is nonzero",
        "observable_effect": "scalar/tensor charge, fifth force, source-normalization drift",
        "required_repair": "derive double zero or compute coupling below local bounds",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "AR511_1_no_mass_gap",
        "failure": "extra-field Hessian/operator is massless, tachyonic, or sign-indefinite",
        "observable_effect": "long-range hair and PPN deviations",
        "required_repair": "derive positive operator or retain finite-range residual curve",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "AR511_2_direct_matter_charge",
        "failure": "matter species carry different extra-field charges",
        "observable_effect": "WEP violation and source-frame split",
        "required_repair": "universal observed-coframe theorem or species residual bound",
        "claim_status": "blocks_source_universality",
    },
    {
        "residual_id": "AR511_3_memory_nonlocal_tail",
        "failure": "memory/history kernel injects local charge or time drift",
        "observable_effect": "Gdot/GMdot, clock drift, local residual hysteresis",
        "required_repair": "local positive kernel silence or explicit time-drift residual",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "AR511_4_domain_projector_stress",
        "failure": "domain/projector selector has stress, preferred frame, or source-normalization shift",
        "observable_effect": "alpha_i/xi/R11 residuals",
        "required_repair": "parent selector theorem with zero local stress or executable residual vector",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "AR511_5_PiM_variation",
        "failure": "Pi_M depends on source, radius, domain, or extra-field state",
        "observable_effect": "measured GM becomes a tunable readout",
        "required_repair": "Pi_M(Phi0)=Pi_EH and first variation zero",
        "claim_status": "blocks_Newton_promotion",
    },
    {
        "residual_id": "AR511_6_boundary_charge",
        "failure": "extra boundary/reference terms carry mass flux",
        "observable_effect": "radial M_eff drift and source-measure mismatch",
        "required_repair": "boundary no-flux theorem or reference-subtracted residual",
        "claim_status": "blocks_source_measure",
    },
    {
        "residual_id": "AR511_7_metric_PPN_tail",
        "failure": "metric readout differs from GR at second order",
        "observable_effect": "gamma, beta, alpha_i, zeta_i, xi residuals",
        "required_repair": "derive PPN vector from action or score against official bounds",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "AR511_8_transition_switching",
        "failure": "ell_tr/L_cg or activation rule is fitted by arena rather than action-derived",
        "observable_effect": "local/cosmology/galaxy branches become patched regimes",
        "required_repair": "derive activation from operator spectrum, source scale, or topological sector",
        "claim_status": "blocks_unified_field_theory_claim",
    },
]

GATE_TEST_ROWS = [
    {
        "gate_id": "G511_0_contract_sufficiency",
        "gate": "the action blocks and fixed-point conditions are sufficient in principle to derive a local GR branch",
        "result": "pass_conditional",
        "evidence": "A511_0-A511_6 plus FP511_0-FP511_8 imply DC511 chain if matched",
    },
    {
        "gate_id": "G511_1_no_plateau_axiom",
        "gate": "local silence is generated by variational fixed-point/mass-gap/double-zero conditions, not asserted as a plateau",
        "result": "pass",
        "evidence": "FP511_1/FP511_2 replace q_loc plateau assumptions",
    },
    {
        "gate_id": "G511_2_current_MTS_match",
        "gate": "existing MTS symbols and equations are proven to instantiate all action blocks",
        "result": "fail_for_current_claim",
        "evidence": "mapping to Gamma_eff, K_hat, q_loc, chi_D, Qcoh, memory, and Pi_M not yet performed",
    },
    {
        "gate_id": "G511_3_F1_zero",
        "gate": "F_1=0/double-zero condition is derived for every non-EH coupling",
        "result": "fail_for_current_claim",
        "evidence": "FP511_1 is required but not matched to current MTS parent terms",
    },
    {
        "gate_id": "G511_4_PPN_promotion",
        "gate": "local GR/PPN can be claimed",
        "result": "fail_blocked",
        "evidence": "requires symbol matching, first variation, and weak-field PPN expansion",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D511_0",
        "decision": "minimal_fixed_point_route_is_viable_as_a_contract",
        "meaning": "there is a coherent way for MTS to reduce to GR locally without smuggling in a plateau, if the parent action satisfies these clauses",
        "claim_status": "conditional_action_contract",
    },
    {
        "decision_id": "D511_1",
        "decision": "current_MTS_has_not_yet_matched_the_contract",
        "meaning": "the next task is mapping actual MTS variables/equations into these action blocks and checking first variations",
        "claim_status": "local_GR_claim_false",
    },
    {
        "decision_id": "D511_2",
        "decision": "double_zero_and_mass_gap_are_nonnegotiable",
        "meaning": "F_1=0, positive operator, no source charge, and zero boundary flux are the price of derived local GR",
        "claim_status": "required_for_promotion",
    },
    {
        "decision_id": "D511_3",
        "decision": "transition_scale_must_be_derived",
        "meaning": "ell_tr/L_cg cannot be an arena switch; it must come from the same action/operator spectrum or stay as a residual",
        "claim_status": "unification_gate_open",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU511_0",
        "status": "parent_action_fixed_point_contract_written",
        "update": "local GR can be targeted through an EH fixed point plus double-zero/mass-gap/silence conditions",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU511_1",
        "status": "MTS_symbol_mapping_now_required",
        "update": "the next checkpoint must map Gamma_eff, K_hat, q_loc, chi_D, Qcoh, memory, Pi_M, and kappa to the action blocks",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU511_2",
        "status": "overclaim_guard_active",
        "update": "this is a candidate action contract, not proof that current MTS already reduces to GR",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        path = ROOT / item["source_file"]
        rows.append(
            {
                "source_file": item["source_file"],
                "role": item["role"],
                "exists": path.exists(),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    return [
        {
            "check_id": "V511_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V511_1_action_blocks_present",
            "result": "pass",
            "detail": f"action_blocks={len(ACTION_BLOCK_ROWS)}",
        },
        {
            "check_id": "V511_2_fixed_point_conditions_present",
            "result": "pass",
            "detail": f"fixed_point_conditions={len(FIXED_POINT_ROWS)}",
        },
        {
            "check_id": "V511_3_residual_vector_complete",
            "result": "pass",
            "detail": f"residual_rows={len(RESIDUAL_VECTOR_ROWS)}",
        },
        {
            "check_id": "V511_4_no_overclaim",
            "result": "pass",
            "detail": "current_MTS_matched_to_action=false; local_GR_claim_allowed=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys())
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        output.append("| " + " | ".join(values) + " |")
    return "\n".join(output)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 511 - Minimal Parent-Action Local-GR Fixed-Point Ansatz

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This is the cleanest local-GR route so far:

```text
Do not assume q_loc -> 0.
Do not assume a plateau.
Make q_loc -> 0 a consequence of a parent-action fixed point.
```

The minimum structure is an EH core plus universal matter coupling, constant topological kappa, extra-sector double zeros, positive local operators, boundary no-flux, and a weak-field readout that starts as GR.

That route is viable as a **contract**. It is not yet proof that current MTS satisfies the contract.

The big prize is now sharply stated:

```text
If Gamma_eff, K_hat, q_loc, chi_D, Qcoh, memory, Pi_M, and kappa can be matched to these action blocks with the required first variations, then local GR is no longer a smuggled closure. It is derived.
```

## 2. Action Blocks

{markdown_table(ACTION_BLOCK_ROWS)}

## 3. Fixed-Point Conditions

{markdown_table(FIXED_POINT_ROWS)}

## 4. Derived Chain

{markdown_table(DERIVED_CHAIN_ROWS)}

## 5. Residual Vector

{markdown_table(RESIDUAL_VECTOR_ROWS)}

## 6. Gate Tests

{markdown_table(GATE_TEST_ROWS)}

## 7. Decision

{markdown_table(DECISION_ROWS)}

## 8. Source Register

{markdown_table(sources)}

## 9. Validation

{markdown_table(validations)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. What This Buys Us

This ansatz makes the local branch mathematically disciplined:

```text
F_1 = 0 is not a wish; it is a double-zero condition on the parent coupling.
Delta m is not handwaved; it is controlled by the positive Hessian/operator spectrum.
ell_tr/L_cg is not a switch; it must be an activation scale derived from the same operator/source structure.
```

That is exactly the kind of route that can make MTS behave like GR locally while still leaving room for cosmology/galaxy-scale behaviour.

## 12. Claim Ceiling

Allowed:

```text
MTS now has a coherent minimal parent-action contract for deriving local GR.
The contract identifies the exact double-zero, mass-gap, source-frame, projector, boundary, and PPN gates.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived F_1=0 for current MTS couplings.
MTS has derived ell_tr/L_cg from the current parent action.
MTS has matched every MTS variable to the proposed action blocks.
```

## 13. Next Target

`{NEXT_TARGET}`

Next we should map real MTS symbols and equations onto the action blocks. If a symbol cannot be placed inside the action, first variation, boundary term, or readout map, it stays a residual or gets demoted.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-minimal-parent-action-local-GR-fixed-point-ansatz"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (ACTION_BLOCKS_PATH, ACTION_BLOCK_ROWS),
        (FIXED_POINT_CONDITIONS_PATH, FIXED_POINT_ROWS),
        (DERIVED_CHAIN_PATH, DERIVED_CHAIN_ROWS),
        (RESIDUAL_VECTOR_PATH, RESIDUAL_VECTOR_ROWS),
        (GATE_TESTS_PATH, GATE_TEST_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "action_blocks": str(ROOT / ACTION_BLOCKS_PATH),
        "fixed_point_conditions": str(ROOT / FIXED_POINT_CONDITIONS_PATH),
        "derived_chain": str(ROOT / DERIVED_CHAIN_PATH),
        "residual_vector": str(ROOT / RESIDUAL_VECTOR_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "minimal_parent_action_ansatz_written": True,
        "local_GR_fixed_point_derivable_if_clauses_pass": True,
        "current_MTS_matched_to_action": False,
        "plateau_axiom_used": False,
        "double_zero_conditions_required": True,
        "F1_zero_condition_written": True,
        "mass_gap_required": True,
        "ell_tr_over_Lcg_requires_derivation": True,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
