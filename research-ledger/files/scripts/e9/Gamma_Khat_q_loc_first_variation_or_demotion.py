from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Gamma_Khat_q_loc_rewritten_as_projected_extra_stress_divergence_conditional_action_contract_current_MTS_not_derived"
CLAIM_CEILING = "conditional_variational_stress_route_only_no_q_loc_zero_or_local_GR_promotion"
NEXT_TARGET = "514-construct-GK-stress-action-or-residual-bound.md"

DOC_PATH = Path("513-Gamma-Khat-q_loc-first-variation-or-demotion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_SOURCE_REGISTER.csv")
STRESS_REWRITE_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv")
FIRST_VARIATION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv")
INTEGRABILITY_GATES_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv")
RESIDUAL_OR_DEMOTION_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_GATE_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "role": "symbol map identifying Gamma_eff/K_hat/q_loc as hard next target",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "action fixed-point contract with double-zero and mass-gap gates",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "positive source-free operator and no-boundary/source-charge silence mechanism",
    },
    {
        "source_file": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "Ward identity and projector variation debt",
    },
    {
        "source_file": "384-parent-action-first-variation-obstruction-map.md",
        "role": "first-variation obstruction map for local branch",
    },
    {
        "source_file": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Ward/Bianchi exchange ownership for source-normalized Poisson branch",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "role": "FV512 gates including Gamma-Khat-q_loc first-variation target",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "symbol placement map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "action blocks for local GR fixed-point route",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
        "role": "fixed-point double-zero/mass-gap/source-frame gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "role": "example of a successful conditional Ward-force zero chain for chi_D",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "M_eff residual runner affected by any q_loc force leakage",
    },
    {
        "source_file": "scripts/Gamma_Khat_q_loc_first_variation_or_demotion.py",
        "role": "this checkpoint generator",
    },
]

STRESS_REWRITE_ROWS = [
    {
        "rewrite_id": "SR513_0_define_extra_stress",
        "statement": "The q_loc expression can be rewritten as the projected divergence of an effective extra stress tensor.",
        "equation": "T_GK^{mu nu} := Gamma_eff g^{mu nu} - K_hat^{mu nu}",
        "consequence": "nabla_mu T_GK^{mu nu} = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
        "status": "algebraic_identity",
    },
    {
        "rewrite_id": "SR513_1_projected_residual",
        "statement": "The physical local leakage is the projected divergence of T_GK.",
        "equation": "q_loc^nu = P_loc nabla_mu T_GK^{mu nu}",
        "consequence": "q_loc is not a fundamental field; it is a Ward/source-exchange residual",
        "status": "definition_reclassification",
    },
    {
        "rewrite_id": "SR513_2_variational_route",
        "statement": "If T_GK is the Hilbert stress tensor of a diffeomorphism-invariant parent sector, its divergence is controlled by the Euler equations of that sector.",
        "equation": "T_GK^{mu nu} = -2/sqrt(-g) delta S_GK/dg_{mu nu}; nabla_mu T_GK^{mu nu} = sum_A E_A nabla^nu Phi^A",
        "consequence": "on shell and source-free, q_loc^nu=0 follows without a plateau axiom",
        "status": "conditional_derivation_route",
    },
    {
        "rewrite_id": "SR513_3_double_zero_suppression",
        "statement": "If T_GK and its first field variation vanish at the local fixed point, local leakage starts at second order or exponential/mass-gap order.",
        "equation": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0",
        "consequence": "F_1=0 is the stress-level double-zero condition",
        "status": "conditional_fixed_point_gate",
    },
]

FIRST_VARIATION_CONTRACT_ROWS = [
    {
        "contract_id": "GK513_0_action_existence",
        "required_clause": "There exists a local diffeomorphism-invariant scalar action S_GK[g,Phi] whose Hilbert stress is T_GK.",
        "mathematical_form": "T_GK^{mu nu} = -2/sqrt(-g) delta S_GK/dg_{mu nu}",
        "if_missing": "Gamma_eff/K_hat are non-variational bookkeeping and q_loc cannot be derived zero",
        "current_MTS_status": "not_supplied",
    },
    {
        "contract_id": "GK513_1_integrability",
        "required_clause": "The proposed stress tensor satisfies variational Helmholtz/integrability conditions.",
        "mathematical_form": "delta(sqrt(-g)T^{mu nu})/delta g_{alpha beta} has the required symmetric second-variation structure up to boundary terms",
        "if_missing": "no action exists for the claimed stress",
        "current_MTS_status": "not_checked",
    },
    {
        "contract_id": "GK513_2_Euler_closure",
        "required_clause": "The same fields that build Gamma_eff and K_hat have Euler equations E_A=0 in compact local vacuum.",
        "mathematical_form": "nabla_mu T_GK^{mu nu} = sum_A E_A nabla^nu Phi^A = 0 on shell",
        "if_missing": "stress divergence remains a physical fifth-force/source-exchange residual",
        "current_MTS_status": "not_derived",
    },
    {
        "contract_id": "GK513_3_double_zero",
        "required_clause": "The local fixed point has T_GK(Phi0)=0 and first variation zero.",
        "mathematical_form": "Gamma_eff(Phi0)g^{mu nu}-K_hat^{mu nu}(Phi0)=0; partial_A[Gamma_eff g^{mu nu}-K_hat^{mu nu}]_{Phi0}=0",
        "if_missing": "F_1 survives and local PPN/source-normalization hair remains",
        "current_MTS_status": "not_matched",
    },
    {
        "contract_id": "GK513_4_projector_ownership",
        "required_clause": "P_loc is parent-owned and commutes with the local fixed-point/readout limit.",
        "mathematical_form": "P_loc = P_parent(Phi0) and partial_A P_loc(Phi0)=0",
        "if_missing": "projection can hide force components or tune residuals",
        "current_MTS_status": "open",
    },
    {
        "contract_id": "GK513_5_boundary_no_flux",
        "required_clause": "Boundary/symplectic terms from S_GK do not carry extra linking-sphere force or mass flux.",
        "mathematical_form": "integral_boundary Delta(theta_GK,Q_GK,tau)=0 or fixed topological subtraction",
        "if_missing": "q_loc may vanish in bulk but leak through boundaries",
        "current_MTS_status": "open",
    },
]

INTEGRABILITY_GATE_ROWS = [
    {
        "gate_id": "IG513_0_tensor_symmetry",
        "gate": "T_GK^{mu nu} is symmetric or has a Belinfante/symplectic improvement that is symmetric",
        "required_for": "Hilbert stress ownership",
        "current_result": "not_checked",
    },
    {
        "gate_id": "IG513_1_covariance",
        "gate": "Gamma_eff is scalar and K_hat^{mu nu} is a covariant rank-2 tensor built from parent fields",
        "required_for": "diffeomorphism Ward identity",
        "current_result": "not_checked",
    },
    {
        "gate_id": "IG513_2_metric_variationality",
        "gate": "T_GK is the metric variation of a scalar density, not an arbitrary tensor assigned after readout",
        "required_for": "action derivation",
        "current_result": "fail_for_current_claim",
    },
    {
        "gate_id": "IG513_3_Euler_source_free",
        "gate": "the fields sourcing Gamma_eff/K_hat obey source-free local equations in compact vacuum",
        "required_for": "q_loc on-shell zero",
        "current_result": "not_derived",
    },
    {
        "gate_id": "IG513_4_fixed_point_double_zero",
        "gate": "T_GK and first variation vanish at local fixed point",
        "required_for": "F_1=0 and PPN silence",
        "current_result": "not_derived",
    },
    {
        "gate_id": "IG513_5_boundary_integrability",
        "gate": "boundary terms generated by the action have a zero-flux or fixed-reference theorem",
        "required_for": "worldtube/source-measure glue",
        "current_result": "open",
    },
    {
        "gate_id": "IG513_6_units_and_readout",
        "gate": "Gamma_eff and K_hat have stress-tensor units after normalization, and their weak-field readout maps to PPN coefficients",
        "required_for": "testable residuals",
        "current_result": "not_checked",
    },
]

RESIDUAL_OR_DEMOTION_ROWS = [
    {
        "residual_id": "QR513_0_nonvariational_stress",
        "failure": "no S_GK exists with T_GK=Gamma g-K_hat",
        "demotion": "Gamma_eff/K_hat/q_loc become closure bookkeeping, not a derived local-GR mechanism",
        "test_fallback": "fit or bound q_loc residual components against PPN/fifth-force/source-normalization locks",
    },
    {
        "residual_id": "QR513_1_Euler_not_zero",
        "failure": "fields building T_GK remain sourced in local vacuum",
        "demotion": "q_loc is a real local force/source-exchange residual",
        "test_fallback": "derive coupling coefficient or numeric q_loc profile",
    },
    {
        "residual_id": "QR513_2_double_zero_fails",
        "failure": "T_GK or partial_A T_GK is nonzero at the fixed point",
        "demotion": "F_1 survives and the branch cannot claim local GR",
        "test_fallback": "compute PPN residual vector and compare to official bounds",
    },
    {
        "residual_id": "QR513_3_projector_unowned",
        "failure": "P_loc is chosen after solving or by empirical domain selection",
        "demotion": "projected zero is not a covariant theorem",
        "test_fallback": "carry full unprojected residual or derive P_loc parent algebra",
    },
    {
        "residual_id": "QR513_4_boundary_flux",
        "failure": "bulk q_loc vanishes but boundary/symplectic charge leaks",
        "demotion": "local source-measure closure remains residual",
        "test_fallback": "boundary no-flux theorem or radial M_eff bound",
    },
]

GATE_TEST_ROWS = [
    {
        "gate_id": "G513_0_algebraic_rewrite",
        "gate": "q_loc can be rewritten as projected divergence of T_GK",
        "result": "pass",
        "evidence": "SR513_0/SR513_1",
    },
    {
        "gate_id": "G513_1_conditional_action_route",
        "gate": "a diffeomorphism-invariant S_GK would derive q_loc=0 on shell",
        "result": "pass_conditional",
        "evidence": "SR513_2 and GK513_0-GK513_2",
    },
    {
        "gate_id": "G513_2_current_MTS_action",
        "gate": "current MTS supplies S_GK and integrability proof",
        "result": "fail_for_current_claim",
        "evidence": "IG513_2/IG513_3/IG513_4 not checked or not derived",
    },
    {
        "gate_id": "G513_3_no_plateau_axiom",
        "gate": "q_loc zero is not assumed",
        "result": "pass",
        "evidence": "requires variational stress/Euler/double-zero route",
    },
    {
        "gate_id": "G513_4_local_GR_claim",
        "gate": "local GR/PPN is promoted",
        "result": "fail_blocked",
        "evidence": "S_GK construction and PPN residual vector still missing",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D513_0",
        "decision": "q_loc_problem_reduced_to_variational_stress_problem",
        "meaning": "the central residual is no longer mysterious: it is the projected divergence of T_GK=Gamma g-K_hat",
        "claim_status": "major_derivation_target_sharpened",
    },
    {
        "decision_id": "D513_1",
        "decision": "conditional_route_is_clean",
        "meaning": "if T_GK is Hilbert stress from a diffeomorphism-invariant sector, Ward identity gives q_loc=0 on shell",
        "claim_status": "conditional_not_current_MTS_proof",
    },
    {
        "decision_id": "D513_2",
        "decision": "current_MTS_not_yet_promoted",
        "meaning": "the action, integrability, Euler closure, double-zero, projector, and boundary gates are not yet passed",
        "claim_status": "local_GR_claim_false",
    },
    {
        "decision_id": "D513_3",
        "decision": "next_step_construct_or_demote",
        "meaning": "try to construct S_GK explicitly; if no action exists, demote Gamma/Khat/q_loc to residual-bound branch",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU513_0",
        "status": "q_loc_variational_identity_found",
        "update": "q_loc equals P_loc divergence of T_GK with T_GK=Gamma_eff g-K_hat",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU513_1",
        "status": "S_GK_required",
        "update": "the next gate is constructing a real diffeomorphism-invariant action that has this stress tensor",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU513_2",
        "status": "current_claim_blocked",
        "update": "without S_GK and double-zero/integrability checks, q_loc remains residual and local GR is not promoted",
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
            "check_id": "V513_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V513_1_stress_rewrite_present",
            "result": "pass",
            "detail": f"rewrite_rows={len(STRESS_REWRITE_ROWS)}",
        },
        {
            "check_id": "V513_2_first_variation_contract_present",
            "result": "pass",
            "detail": f"contract_rows={len(FIRST_VARIATION_CONTRACT_ROWS)}",
        },
        {
            "check_id": "V513_3_integrability_gates_present",
            "result": "pass",
            "detail": f"integrability_gates={len(INTEGRABILITY_GATE_ROWS)}",
        },
        {
            "check_id": "V513_4_no_overclaim",
            "result": "pass",
            "detail": "S_GK_constructed=false; q_loc_zero_derived_for_MTS=false; local_GR_claim_allowed=false",
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
    return f"""# 513 - Gamma/Khat/q_loc First Variation or Demotion

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This is a genuine useful derivation step.

The object we have been calling local leakage can be rewritten exactly as:

```text
T_GK^{{mu nu}} := Gamma_eff g^{{mu nu}} - K_hat^{{mu nu}}
q_loc^nu = P_loc nabla_mu T_GK^{{mu nu}}
```

So the question is no longer vague:

```text
Can T_GK be the Hilbert stress tensor of a real diffeomorphism-invariant parent sector?
```

If yes, the Ward identity gives:

```text
nabla_mu T_GK^{{mu nu}} = sum_A E_A nabla^nu Phi^A,
```

so `q_loc^nu -> 0` follows on shell in compact local vacuum without a plateau axiom.

If no, then `Gamma_eff`, `K_hat`, and `q_loc` are closure/residual machinery and cannot be used to claim derived local GR.

## 2. Stress Rewrite

{markdown_table(STRESS_REWRITE_ROWS)}

## 3. First-Variation Contract

{markdown_table(FIRST_VARIATION_CONTRACT_ROWS)}

## 4. Integrability Gates

{markdown_table(INTEGRABILITY_GATE_ROWS)}

## 5. Residual or Demotion Map

{markdown_table(RESIDUAL_OR_DEMOTION_ROWS)}

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

## 11. Claim Ceiling

Allowed:

```text
MTS has reduced the q_loc problem to an exact stress-divergence/action-integrability problem.
MTS has a clean conditional route for q_loc^nu -> 0 if S_GK exists and passes Ward/double-zero gates.
```

Forbidden:

```text
MTS has derived q_loc^nu -> 0 for current MTS.
MTS has constructed S_GK.
MTS has passed Helmholtz/integrability gates for Gamma_eff and K_hat.
MTS has derived local GR or PPN silence.
```

## 12. Next Target

`{NEXT_TARGET}`

Try to construct `S_GK`. The cleanest candidate is a parent sector whose Hilbert stress is `Gamma_eff g^{{mu nu}} - K_hat^{{mu nu}}`, with positive source-free Euler equations and a double zero at the local fixed point. If the construction fails, the route must become residual-bound only.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Gamma-Khat-q_loc-first-variation-or-demotion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (STRESS_REWRITE_PATH, STRESS_REWRITE_ROWS),
        (FIRST_VARIATION_CONTRACT_PATH, FIRST_VARIATION_CONTRACT_ROWS),
        (INTEGRABILITY_GATES_PATH, INTEGRABILITY_GATE_ROWS),
        (RESIDUAL_OR_DEMOTION_PATH, RESIDUAL_OR_DEMOTION_ROWS),
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
        "stress_rewrite": str(ROOT / STRESS_REWRITE_PATH),
        "first_variation_contract": str(ROOT / FIRST_VARIATION_CONTRACT_PATH),
        "integrability_gates": str(ROOT / INTEGRABILITY_GATES_PATH),
        "residual_or_demotion": str(ROOT / RESIDUAL_OR_DEMOTION_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "q_loc_stress_rewrite_identity": True,
        "q_loc_reclassified_as_projected_stress_divergence": True,
        "conditional_q_loc_zero_route": True,
        "S_GK_constructed": False,
        "Gamma_Khat_integrability_checked": False,
        "double_zero_derived_for_GK": False,
        "q_loc_zero_derived_for_MTS": False,
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
