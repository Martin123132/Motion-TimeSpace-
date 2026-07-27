from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "S_GK_candidate_action_constructed_metric_response_route_current_MTS_not_matched_residual_branch_retained"
CLAIM_CEILING = "candidate_Gamma_Khat_action_only_no_q_loc_zero_until_metric_response_and_fixed_point_are_proved"
NEXT_TARGET = "515-match-Gamma-eff-Khat-to-metric-response-action.md"

DOC_PATH = Path("514-construct-GK-stress-action-or-residual-bound.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_GK_STRESS_ACTION_SOURCE_REGISTER.csv")
ACTION_CANDIDATES_PATH = Path("source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv")
METRIC_RESPONSE_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv")
FIXED_POINT_GATES_PATH = Path("source-intake/mts_residuals/P8_GK_LOCAL_FIXED_POINT_GATES.csv")
RESIDUAL_BOUND_BRANCH_PATH = Path("source-intake/mts_residuals/P8_GK_RESIDUAL_BOUND_BRANCH.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_GK_STRESS_ACTION_GATE_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_GK_STRESS_ACTION_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_GK_STRESS_ACTION_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_GK_STRESS_ACTION_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "stress divergence identity and S_GK contract",
    },
    {
        "source_file": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "role": "symbol placement map identifying Gamma/Khat/q_loc as hard target",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal local-GR fixed point and double-zero/mass-gap gates",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "positive source-free operator silence mechanism",
    },
    {
        "source_file": "137-auxiliary-geometric-memory-action-owner.md",
        "role": "auxiliary memory action owner route",
    },
    {
        "source_file": "143-domain-selector-variational-action-attempt.md",
        "role": "domain selector action and chi_D variation warnings",
    },
    {
        "source_file": "384-parent-action-first-variation-obstruction-map.md",
        "role": "first-variation obstruction map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "role": "513 first-variation contract to satisfy",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
        "role": "513 integrability gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
        "role": "511 fixed-point gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "512 symbol map",
    },
    {
        "source_file": "scripts/construct_GK_stress_action_or_residual_bound.py",
        "role": "this checkpoint generator",
    },
]

ACTION_CANDIDATE_ROWS = [
    {
        "candidate_id": "GK514_A_metric_response_scalar_density",
        "candidate_action": "S_GK = - integral sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
        "stress_form": "T_GK^{mu nu} = Gamma_eff g^{mu nu} - K_metric^{mu nu}",
        "required_identification": "K_hat^{mu nu} = K_metric^{mu nu} := 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} minus the volume term convention",
        "why_useful": "Gamma_eff and K_hat become one variational object; q_loc becomes the Ward residual",
        "current_status": "best_candidate_not_matched_to_existing_MTS",
    },
    {
        "candidate_id": "GK514_B_positive_auxiliary_fields",
        "candidate_action": "S_GK = integral sqrt(-g)[-1/2 G_AB(Phi) nabla Phi^A nabla Phi^B - V(Phi)]",
        "stress_form": "T_GK built from kinetic tensor plus potential; match to Gamma g - K_hat up to sign convention",
        "required_identification": "Gamma_eff is potential plus kinetic trace part; K_hat is kinetic/elastic anisotropic response",
        "why_useful": "positive Hessian/mass gap can derive local silence",
        "current_status": "conditional_candidate_needs_symbol_match",
    },
    {
        "candidate_id": "GK514_C_topological_exact_sector",
        "candidate_action": "S_GK = integral dB_GK or topological density",
        "stress_form": "bulk T_GK=0 with possible boundary charge",
        "required_identification": "Gamma_eff g - K_hat is exact/improvement stress with zero local boundary flux",
        "why_useful": "can kill bulk q_loc without introducing propagating fields",
        "current_status": "boundary_flux_risk_open",
    },
    {
        "candidate_id": "GK514_D_residual_branch",
        "candidate_action": "no S_GK accepted",
        "stress_form": "T_GK is bookkeeping only",
        "required_identification": "none; q_loc is explicit residual",
        "why_useful": "keeps theory honest and testable if construction fails",
        "current_status": "fallback_required",
    },
]

METRIC_RESPONSE_CONTRACT_ROWS = [
    {
        "contract_id": "MR514_0_scalar_density",
        "requirement": "Gamma_eff is a covariant scalar density input to S_GK, not a post-readout fitted function.",
        "test": "Gamma_eff = Gamma_eff(g,Phi,nabla Phi,D,topological data) with declared units and no data-fit selector",
        "if_fail": "candidate A fails; q_loc remains residual",
    },
    {
        "contract_id": "MR514_1_Khat_metric_response",
        "requirement": "K_hat is exactly the metric response of Gamma_eff, including derivative/boundary terms.",
        "test": "K_hat^{mu nu} = K_metric^{mu nu} from delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} under a fixed sign convention",
        "if_fail": "Gamma and Khat are independent knobs and cannot derive q_loc zero",
    },
    {
        "contract_id": "MR514_2_Ward_identity",
        "requirement": "Diffeomorphism invariance of S_GK gives the q_loc expression as a Ward residual.",
        "test": "nabla_mu T_GK^{mu nu} = sum_A E_A nabla^nu Phi^A + boundary/nonlocal terms",
        "if_fail": "q_loc is not owned by the parent variation",
    },
    {
        "contract_id": "MR514_3_Euler_silence",
        "requirement": "The fields Phi entering Gamma_eff obey source-free positive local equations in compact local vacuum.",
        "test": "E_A=0 and energy identity gives delta Phi=0 or bounded exponential hair",
        "if_fail": "q_loc is a physical local force residual",
    },
    {
        "contract_id": "MR514_4_fixed_point_subtraction",
        "requirement": "Any constant Gamma_eff(Phi0) is absorbed into Lambda0/background subtraction, leaving no local force.",
        "test": "nabla^nu Gamma_eff(Phi0)=0 and boundary variation of the constant piece is EH-compatible",
        "if_fail": "constant background contaminates local mass/source readout",
    },
    {
        "contract_id": "MR514_5_double_zero",
        "requirement": "First variations of the stress vanish at the local fixed point.",
        "test": "partial_A T_GK^{mu nu}(Phi0)=0, equivalent to F_1=0 for this sector",
        "if_fail": "linear PPN/fifth-force/source-normalization leakage remains",
    },
]

FIXED_POINT_GATE_ROWS = [
    {
        "gate_id": "FG514_0_local_vacuum",
        "gate": "Phi=Phi0 and E_A(Phi0)=0 in compact local exterior",
        "result_now": "not_matched",
        "blocks_if_missing": "q_loc_zero_derived_for_MTS",
    },
    {
        "gate_id": "FG514_1_positive_operator",
        "gate": "linearized operator around Phi0 is positive/self-adjoint after gauge fixing",
        "result_now": "not_matched",
        "blocks_if_missing": "no-hair/silence theorem",
    },
    {
        "gate_id": "FG514_2_metric_response_identity",
        "gate": "K_hat equals metric response of Gamma_eff",
        "result_now": "not_matched",
        "blocks_if_missing": "action derivation of q_loc",
    },
    {
        "gate_id": "FG514_3_double_zero",
        "gate": "T_GK and partial_A T_GK vanish or become constant background at Phi0",
        "result_now": "not_derived",
        "blocks_if_missing": "F_1=0/local_PPN_silence",
    },
    {
        "gate_id": "FG514_4_boundary_terms",
        "gate": "metric response and integrations by parts add no local boundary force/mass flux",
        "result_now": "open",
        "blocks_if_missing": "worldtube/source_measure",
    },
    {
        "gate_id": "FG514_5_Ploc",
        "gate": "P_loc is parent-owned and does not hide unprojected force components",
        "result_now": "open",
        "blocks_if_missing": "covariant local_GR claim",
    },
]

RESIDUAL_BOUND_ROWS = [
    {
        "residual_id": "GB514_0_Gamma_not_scalar",
        "if_candidate_fails": "Gamma_eff cannot be written as a covariant scalar action density",
        "bound_or_demote": "demote Gamma_eff to phenomenological/readout function and bound q_loc directly",
    },
    {
        "residual_id": "GB514_1_Khat_not_response",
        "if_candidate_fails": "K_hat is not the metric response of Gamma_eff",
        "bound_or_demote": "treat K_hat as independent boundary/closure tensor and require PPN/local-bound coefficient",
    },
    {
        "residual_id": "GB514_2_Euler_source",
        "if_candidate_fails": "Phi fields remain sourced in local vacuum",
        "bound_or_demote": "derive finite-range profile or score q_loc residual against fifth-force/PPN locks",
    },
    {
        "residual_id": "GB514_3_double_zero_missing",
        "if_candidate_fails": "linear stress variation survives",
        "bound_or_demote": "compute F_1 coefficient and PPN residual vector",
    },
    {
        "residual_id": "GB514_4_boundary_leak",
        "if_candidate_fails": "action variation creates boundary flux",
        "bound_or_demote": "carry boundary flux in M_eff radial/source-measure residual runner",
    },
]

GATE_TEST_ROWS = [
    {
        "gate_id": "G514_0_candidate_constructed",
        "gate": "an explicit S_GK candidate route is written",
        "result": "pass_conditional",
        "evidence": "GK514_A and GK514_B",
    },
    {
        "gate_id": "G514_1_metric_response_route",
        "gate": "K_hat can be interpreted as metric response of Gamma_eff",
        "result": "pass_as_contract",
        "evidence": "MR514_1 gives exact required identity",
    },
    {
        "gate_id": "G514_2_current_MTS_match",
        "gate": "current corpus proves Gamma_eff and K_hat satisfy the metric-response identity",
        "result": "fail_for_current_claim",
        "evidence": "FG514_2 not matched",
    },
    {
        "gate_id": "G514_3_q_loc_zero",
        "gate": "q_loc is derived zero for MTS",
        "result": "fail_blocked",
        "evidence": "requires FG514_0-FG514_5",
    },
    {
        "gate_id": "G514_4_residual_fallback",
        "gate": "if construction fails, residual-bound branch remains explicit",
        "result": "pass",
        "evidence": f"residual_rows={len(RESIDUAL_BOUND_ROWS)}",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D514_0",
        "decision": "best_candidate_is_metric_response_action",
        "meaning": "the cleanest route is S_GK=-integral sqrt(-g)Gamma_eff with K_hat as the metric response",
        "claim_status": "candidate_contract",
    },
    {
        "decision_id": "D514_1",
        "decision": "current_MTS_not_matched",
        "meaning": "Gamma_eff and K_hat have not yet been shown to satisfy the metric-response identity",
        "claim_status": "q_loc_zero_false",
    },
    {
        "decision_id": "D514_2",
        "decision": "this_is_progress_not_promotion",
        "meaning": "we now know exactly what has to be true for the local vacuum route to become derivable",
        "claim_status": "local_GR_claim_false",
    },
    {
        "decision_id": "D514_3",
        "decision": "next_step_match_real_symbols",
        "meaning": "try to identify the existing Gamma_eff and K_hat definitions with the metric response of a scalar density",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU514_0",
        "status": "S_GK_candidate_built",
        "update": "q_loc can be derived if Gamma_eff is a scalar action density and K_hat is its metric response",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU514_1",
        "status": "hard_match_required",
        "update": "the next checkpoint must match actual MTS definitions to the metric-response contract",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU514_2",
        "status": "residual_branch_kept",
        "update": "if the match fails, q_loc moves to direct residual bounds rather than hidden local-GR proof",
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
            "check_id": "V514_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V514_1_candidates_present",
            "result": "pass",
            "detail": f"candidate_rows={len(ACTION_CANDIDATE_ROWS)}",
        },
        {
            "check_id": "V514_2_metric_response_contract_present",
            "result": "pass",
            "detail": f"contract_rows={len(METRIC_RESPONSE_CONTRACT_ROWS)}",
        },
        {
            "check_id": "V514_3_residual_branch_present",
            "result": "pass",
            "detail": f"residual_rows={len(RESIDUAL_BOUND_ROWS)}",
        },
        {
            "check_id": "V514_4_no_overclaim",
            "result": "pass",
            "detail": "S_GK_matched_to_MTS=false; q_loc_zero_derived_for_MTS=false; local_GR_claim_allowed=false",
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
    return f"""# 514 - Construct GK Stress Action or Residual Bound

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

There is a concrete, non-cheat candidate for the `Gamma_eff / K_hat / q_loc` route:

```text
S_GK = - integral sqrt(-g) Gamma_eff
K_hat = metric response of Gamma_eff
T_GK^{{mu nu}} = Gamma_eff g^{{mu nu}} - K_hat^{{mu nu}}
q_loc^nu = P_loc nabla_mu T_GK^{{mu nu}}
```

This is promising because `Gamma_eff` and `K_hat` stop being independent knobs. They become one variational object.

But this is not promoted yet. Current MTS still has to prove that its actual `Gamma_eff` and `K_hat` satisfy the metric-response identity, the local fixed-point double zero, the positive/source-free Euler equations, and boundary no-flux.

So the honest status is:

```text
candidate action route constructed;
current symbol match not proven;
q_loc zero not derived yet;
residual branch retained.
```

## 2. Action Candidates

{markdown_table(ACTION_CANDIDATE_ROWS)}

## 3. Metric-Response Contract

{markdown_table(METRIC_RESPONSE_CONTRACT_ROWS)}

## 4. Local Fixed-Point Gates

{markdown_table(FIXED_POINT_GATE_ROWS)}

## 5. Residual-Bound Branch

{markdown_table(RESIDUAL_BOUND_ROWS)}

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
MTS has a concrete candidate action route for the Gamma/Khat/q_loc local-vacuum mechanism.
The route would derive q_loc^nu -> 0 if K_hat is the metric response of Gamma_eff and fixed-point gates pass.
```

Forbidden:

```text
MTS has matched existing Gamma_eff and K_hat to this action.
MTS has derived q_loc^nu -> 0.
MTS has derived local GR or PPN silence.
```

## 12. Next Target

`{NEXT_TARGET}`

Search the existing MTS definitions for a `Gamma_eff` scalar-density owner and check whether `K_hat` can be interpreted as its metric variation. If yes, the local route gets much stronger. If no, stop trying to derive local GR through this channel and carry q_loc as a bounded residual.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-construct-GK-stress-action-or-residual-bound"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (ACTION_CANDIDATES_PATH, ACTION_CANDIDATE_ROWS),
        (METRIC_RESPONSE_CONTRACT_PATH, METRIC_RESPONSE_CONTRACT_ROWS),
        (FIXED_POINT_GATES_PATH, FIXED_POINT_GATE_ROWS),
        (RESIDUAL_BOUND_BRANCH_PATH, RESIDUAL_BOUND_ROWS),
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
        "action_candidates": str(ROOT / ACTION_CANDIDATES_PATH),
        "metric_response_contract": str(ROOT / METRIC_RESPONSE_CONTRACT_PATH),
        "fixed_point_gates": str(ROOT / FIXED_POINT_GATES_PATH),
        "residual_bound_branch": str(ROOT / RESIDUAL_BOUND_BRANCH_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "S_GK_candidate_constructed": True,
        "best_candidate_metric_response_action": True,
        "S_GK_matched_to_MTS": False,
        "K_hat_metric_response_derived": False,
        "Gamma_eff_scalar_density_derived": False,
        "q_loc_zero_derived_for_MTS": False,
        "residual_branch_retained": True,
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
