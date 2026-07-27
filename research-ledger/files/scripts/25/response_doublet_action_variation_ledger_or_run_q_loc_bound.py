from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "response_doublet_variation_ledger_written_double_zero_formal_Y5_Y6_blockers_active_q_loc_bound_branch_triggered_if_no_owner"
CLAIM_CEILING = "variation_ledger_and_bound_trigger_only_no_q_loc_zero_local_GR_Newton_or_PPN_promotion"
NEXT_TARGET = "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"

DOC_PATH = Path("517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_VARIATION_SOURCE_REGISTER.csv")
ACTION_VARIATION_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv")
METRIC_RESPONSE_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv")
EULER_SOURCE_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv")
OBSTRUCTION_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv")
BOUND_TRIGGER_PATH = Path("source-intake/mts_residuals/P8_QLOC_BOUND_TRIGGER_LEDGER.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_VARIATION_GATE_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_VARIATION_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_VARIATION_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_VARIATION_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
        "role": "response-doublet owner candidate and q_loc bound-runner spec",
    },
    {
        "source_file": "515-match-Gamma-eff-Khat-to-metric-response-action.md",
        "role": "current corpus match audit and repair options",
    },
    {
        "source_file": "514-construct-GK-stress-action-or-residual-bound.md",
        "role": "S_GK metric-response action candidate",
    },
    {
        "source_file": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc as projected stress divergence",
    },
    {
        "source_file": "494-exchange-doublet-component-map-or-coefficient-branch.md",
        "role": "component map identifying Y5 and Y6 hard rows",
    },
    {
        "source_file": "495-source-normalization-even-scalar-theorem-or-coefficient-fill.md",
        "role": "source-normalization even scalar follow-up for Y5",
    },
    {
        "source_file": "219-compact-shell-q_loc-source-projection-attempt.md",
        "role": "compact-shell q_loc leakage budget origin",
    },
    {
        "source_file": "220-Jrel-local-trivial-representative-or-closure-bound.md",
        "role": "worst compact q_loc leakage bound",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "role": "516 response-doublet contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "role": "516 q_loc bound runner spec",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "role": "516 owner candidate rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_YLOC_EULER_SYSTEM.csv",
        "role": "Yloc component list",
    },
    {
        "source_file": "scripts/response_doublet_action_variation_ledger_or_run_q_loc_bound.py",
        "role": "this checkpoint generator",
    },
]

ACTION_VARIATION_ROWS = [
    {
        "step_id": "AV517_0_define_doublet",
        "variation_object": "R_+^A,R_-^A,Z^A,R_even^A",
        "equation": "Z^A=(R_+^A-R_-^A)/2; R_even^A=(R_+^A+R_-^A)/2",
        "derived_if": "exchange symmetry E:R_+<->R_- is a parent symmetry",
        "current_status": "conditional_not_component_derived",
    },
    {
        "step_id": "AV517_1_scalar_density",
        "variation_object": "Gamma_eff",
        "equation": "Gamma_eff = Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)",
        "derived_if": "M_AB is parent-owned, covariant, and positive on local components",
        "current_status": "candidate_written_not_matched",
    },
    {
        "step_id": "AV517_2_first_variation_Z",
        "variation_object": "delta_Z Gamma_eff",
        "equation": "delta Gamma_eff/delta Z^A = M_AB Z^B + O(Z^3)",
        "derived_if": "no linear source term J_A Z^A or boundary B_A Z^A is present",
        "current_status": "formal_double_zero_at_Z0",
    },
    {
        "step_id": "AV517_3_double_zero",
        "variation_object": "F_1",
        "equation": "at Z=0: Gamma_eff-Gamma0=0 and partial_A Gamma_eff=0",
        "derived_if": "Z=0 is the physical local residual state and Gamma0 is subtracted/constant",
        "current_status": "conditional_pass_not_MTS_promotion",
    },
    {
        "step_id": "AV517_4_Euler_equation",
        "variation_object": "Z Euler equation",
        "equation": "L_AB Z^B = J_A + boundary/source terms",
        "derived_if": "L_AB positive and J_A=B_A=0",
        "current_status": "blocked_by_source_current_rows",
    },
    {
        "step_id": "AV517_5_positive_theorem",
        "variation_object": "energy identity",
        "equation": "integral_A Z^A L_AB Z^B = boundary_flux + source_work",
        "derived_if": "positive operator plus zero source/boundary flux",
        "current_status": "conditional_only",
    },
]

METRIC_RESPONSE_ROWS = [
    {
        "response_id": "MR517_0_volume_term",
        "metric_piece": "variation of sqrt(-g)",
        "equation": "delta(sqrt(-g)Gamma_eff) includes -1/2 sqrt(-g) Gamma_eff g^{mu nu} delta g_{mu nu}",
        "Khat_role": "sets the volume convention in T_GK=Gamma g-K_hat",
        "current_status": "formal",
    },
    {
        "response_id": "MR517_1_MAB_metric_dependence",
        "metric_piece": "delta_g M_AB",
        "equation": "K_hat contains Z^A Z^B delta_g M_AB plus index/measure terms",
        "Khat_role": "quadratic in Z if M_AB has no singular local dependence",
        "current_status": "conditional",
    },
    {
        "response_id": "MR517_2_Z_metric_lock",
        "metric_piece": "delta_g Z^A",
        "equation": "K_hat contains M_AB Z^A delta_g Z^B if Z depends on metric/readout/projector",
        "Khat_role": "linear leakage can reappear unless delta_g Z^A is finite and multiplied by Z^A",
        "current_status": "PPN_lock_open",
    },
    {
        "response_id": "MR517_3_boundary_terms",
        "metric_piece": "integrations by parts and domain/boundary variations",
        "equation": "K_hat receives boundary/collar/domain terms if M_AB or Z uses derivatives, projectors, or domains",
        "Khat_role": "can source alpha3/source-measure leakage unless zero-flux theorem passes",
        "current_status": "open",
    },
    {
        "response_id": "MR517_4_fixed_point_stress",
        "metric_piece": "T_GK at Z=0",
        "equation": "T_GK(Phi0)=Gamma0 g^{mu nu}-K_Gamma0^{mu nu}",
        "Khat_role": "must be cosmological/background subtraction only, not local source mass",
        "current_status": "conditional_background_subtraction",
    },
]

EULER_SOURCE_ROWS = [
    {
        "component_id": "Y0_trace_expansion",
        "source_problem": "matter trace can be exchange-even and source scalar response",
        "variation_status": "not_zeroed",
        "required_theorem": "matter sees only even quotient and trace residual is truly odd parent variable",
        "fallback": "trace-load/source-current residual",
    },
    {
        "component_id": "Y1_coherent_projector",
        "source_problem": "projector stress/ownership and trace-STF split are open",
        "variation_status": "not_zeroed",
        "required_theorem": "topological/projector parent ownership and metric-stress accounting",
        "fallback": "retained projector stress ledger",
    },
    {
        "component_id": "Y2_boundary_flux",
        "source_problem": "boundary/collar odd charge can survive",
        "variation_status": "conditional_route",
        "required_theorem": "local compact boundary odd charge zero and no-flux boundary response",
        "fallback": "W_boundary_alpha3_epsilon_boundary_flux",
    },
    {
        "component_id": "Y3_domain_vector",
        "source_problem": "domain vector can be covariant and still PPN-visible",
        "variation_status": "conditional_best",
        "required_theorem": "scalar/topological domain selector and local odd vector class zero",
        "fallback": "W_domain_alpha1/alpha2/alpha3 products",
    },
    {
        "component_id": "Y4_domain_STF_stress",
        "source_problem": "STF/tidal stress can be conserved and nonzero",
        "variation_status": "not_zeroed",
        "required_theorem": "topological/isotropic invisible STF stress theorem",
        "fallback": "W_domain_xi_epsilon_domain_anisotropy plus T_extra",
    },
    {
        "component_id": "Y5_source_normalization",
        "source_problem": "measured GM/source normalization is naturally exchange-even",
        "variation_status": "hard_fail_current",
        "required_theorem": "even EH source only plus all non-EH normalization offsets odd/local-zero or coefficient-bounded",
        "fallback": "c_domain_source_normalization_operator or measured-GM residual vector",
    },
    {
        "component_id": "Y6_stress_Bianchi",
        "source_problem": "Bianchi-owned extra stress can be exchange-even and nonzero",
        "variation_status": "retained_debt",
        "required_theorem": "extra stress topological/invisible or explicitly below PPN bounds",
        "fallback": "retained T_extra residual vector",
    },
]

OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "OB517_0_Y5_even_scalar",
        "obstruction": "source normalization is an observed even scalar, so exchange-odd quadratic Gamma cannot automatically kill it",
        "effect": "Newton/source-normalized GR remains blocked",
        "next_action": "attack Y5 owner theorem before claiming local Newton",
    },
    {
        "obstruction_id": "OB517_1_Y6_even_stress",
        "obstruction": "extra stress may be exchange-even and conserved, so Ward/Bianchi plus doublet parity does not erase it",
        "effect": "EH-only local exterior remains blocked",
        "next_action": "topological/invisible stress theorem or residual score",
    },
    {
        "obstruction_id": "OB517_2_PPN_lock",
        "obstruction": "Z=0 must mean the actual beta/gamma/alpha_i/xi/Gdot/R11 residual vector is zero",
        "effect": "the theorem can zero auxiliary shadows without zeroing physical residuals",
        "next_action": "component lock ledger through PPN order",
    },
    {
        "obstruction_id": "OB517_3_boundary_metric_response",
        "obstruction": "metric variation of domain/projector/boundary pieces can generate local force or mass flux",
        "effect": "q_loc bulk silence may not imply source-measure closure",
        "next_action": "boundary no-flux theorem or q_loc bound row",
    },
]

BOUND_TRIGGER_ROWS = [
    {
        "trigger_id": "BT517_0_owner_match_fails",
        "condition": "Gamma_eff owner or K_hat metric-response identity cannot be constructed",
        "bound_action": "run q_loc residual-bound branch using P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "priority": "immediate",
    },
    {
        "trigger_id": "BT517_1_Y5_unsolved",
        "condition": "source-normalization even scalar theorem fails",
        "bound_action": "fill c_domain_source_normalization_operator / measured-GM residual vector",
        "priority": "high",
    },
    {
        "trigger_id": "BT517_2_Y6_unsolved",
        "condition": "extra stress invisibility theorem fails",
        "bound_action": "retain T_extra residual vector and score PPN/operator rows",
        "priority": "high",
    },
    {
        "trigger_id": "BT517_3_boundary_no_flux_fails",
        "condition": "boundary/domain metric-response flux survives",
        "bound_action": "use compact-shell worst budget 7.432631961576971e-06 plus alpha3/PPN mapping",
        "priority": "high",
    },
    {
        "trigger_id": "BT517_4_PPN_lock_missing",
        "condition": "Z variables cannot be proven equal to physical residual vector",
        "bound_action": "do not use response-doublet theorem for local GR; score residual components directly",
        "priority": "gate",
    },
]

GATE_TEST_ROWS = [
    {
        "gate_id": "G517_0_variation_ledger",
        "gate": "response-doublet action variation is written through first variation and metric response",
        "result": "pass",
        "evidence": "AV517 and MR517 rows",
    },
    {
        "gate_id": "G517_1_formal_double_zero",
        "gate": "quadratic Gamma_eff gives formal F_1=0 at Z=0",
        "result": "pass_conditional",
        "evidence": "AV517_2/AV517_3",
    },
    {
        "gate_id": "G517_2_current_MTS_derivation",
        "gate": "current MTS derives response-doublet owner and Z=physical residual lock",
        "result": "fail_for_current_claim",
        "evidence": "Y5/Y6, PPN lock, and boundary response open",
    },
    {
        "gate_id": "G517_3_bound_triggers",
        "gate": "fallback q_loc bound conditions are explicit",
        "result": "pass",
        "evidence": f"bound_trigger_rows={len(BOUND_TRIGGER_ROWS)}",
    },
    {
        "gate_id": "G517_4_local_GR_claim",
        "gate": "local GR/Newton/PPN is promoted",
        "result": "fail_blocked",
        "evidence": "variation ledger is not a full derivation and bound runner is not scored",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D517_0",
        "decision": "formal_double_zero_route_survives",
        "meaning": "the quadratic response-doublet density really can provide F_1=0 if Z=0 is physical",
        "claim_status": "conditional",
    },
    {
        "decision_id": "D517_1",
        "decision": "current_MTS_not_promoted",
        "meaning": "Y5/Y6, PPN lock, metric response, and boundary terms remain active blockers",
        "claim_status": "local_GR_claim_false",
    },
    {
        "decision_id": "D517_2",
        "decision": "Y5_is_next_derivation_pressure",
        "meaning": "source-normalization even scalar blocks Newton recovery more directly than q_loc algebra",
        "claim_status": NEXT_TARGET,
    },
    {
        "decision_id": "D517_3",
        "decision": "bound_branch_ready_if_owner_fails",
        "meaning": "if Y5/Y6 cannot be derived, q_loc must be scored as retained residual",
        "claim_status": "residual_bound_branch",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU517_0",
        "status": "variation_ledger_written",
        "update": "response-doublet quadratic density gives a formal double-zero route",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU517_1",
        "status": "Y5_Y6_blockers_active",
        "update": "source normalization and extra stress prevent local Newton/GR promotion",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU517_2",
        "status": "bound_runner_triggered_if_owner_fails",
        "update": "q_loc bound runner becomes mandatory if the owner/lock/boundary gates fail",
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
            "check_id": "V517_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V517_1_variation_rows_present",
            "result": "pass",
            "detail": f"action_rows={len(ACTION_VARIATION_ROWS)}; metric_rows={len(METRIC_RESPONSE_ROWS)}",
        },
        {
            "check_id": "V517_2_component_coverage",
            "result": "pass",
            "detail": f"component_rows={len(EULER_SOURCE_ROWS)}",
        },
        {
            "check_id": "V517_3_bound_triggers_present",
            "result": "pass",
            "detail": f"bound_triggers={len(BOUND_TRIGGER_ROWS)}",
        },
        {
            "check_id": "V517_4_no_overclaim",
            "result": "pass",
            "detail": "response_doublet_owner_derived_for_MTS=false; q_loc_bound_runner_scored=false; local_GR_claim_allowed=false",
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
    return f"""# 517 - Response-Doublet Action Variation Ledger or Run q_loc Bound

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The response-doublet route survives the first-variation check as a **formal** mechanism:

```text
Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)
```

does give:

```text
partial_A Gamma_eff|Z=0 = 0.
```

So the route can produce the desired `F_1=0` without a plateau axiom.

But that is still not enough for MTS local GR. The physical lock remains the hard part:

```text
Z^A must equal the actual local residual vector through PPN/source-normalization order.
```

The active blockers are still `Y5_source_normalization`, `Y6_stress_Bianchi`, boundary metric-response flux, and the full PPN lock.

## 2. Action Variation

{markdown_table(ACTION_VARIATION_ROWS)}

## 3. Metric Response

{markdown_table(METRIC_RESPONSE_ROWS)}

## 4. Euler Source Ledger

{markdown_table(EULER_SOURCE_ROWS)}

## 5. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

## 6. q_loc Bound Trigger

{markdown_table(BOUND_TRIGGER_ROWS)}

## 7. Gate Tests

{markdown_table(GATE_TEST_ROWS)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Source Register

{markdown_table(sources)}

## 10. Validation

{markdown_table(validations)}

## 11. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 12. Claim Ceiling

Allowed:

```text
MTS has a formal response-doublet variation route that can derive F_1=0 conditionally.
MTS has identified the exact components that still block local GR/Newton/PPN.
MTS has explicit triggers for switching to q_loc residual-bound scoring.
```

Forbidden:

```text
MTS has derived q_loc^nu -> 0.
MTS has derived the response-doublet owner for current MTS.
MTS has solved source-normalized Newton recovery.
MTS has derived local GR or PPN silence.
```

## 13. Next Target

`{NEXT_TARGET}`

Attack `Y5_source_normalization` directly. If the even scalar source-normalization theorem fails, implement the q_loc/source-normalization bound runner rather than claiming local Newton.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-response-doublet-action-variation-ledger-or-run-q_loc-bound"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (ACTION_VARIATION_PATH, ACTION_VARIATION_ROWS),
        (METRIC_RESPONSE_PATH, METRIC_RESPONSE_ROWS),
        (EULER_SOURCE_PATH, EULER_SOURCE_ROWS),
        (OBSTRUCTION_PATH, OBSTRUCTION_ROWS),
        (BOUND_TRIGGER_PATH, BOUND_TRIGGER_ROWS),
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
        "action_variation": str(ROOT / ACTION_VARIATION_PATH),
        "metric_response": str(ROOT / METRIC_RESPONSE_PATH),
        "euler_source": str(ROOT / EULER_SOURCE_PATH),
        "obstruction": str(ROOT / OBSTRUCTION_PATH),
        "bound_trigger": str(ROOT / BOUND_TRIGGER_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "formal_double_zero_from_quadratic_Gamma": True,
        "response_doublet_owner_derived_for_MTS": False,
        "Z_equals_physical_residual_vector_derived": False,
        "Y5_source_normalization_solved": False,
        "Y6_extra_stress_solved": False,
        "q_loc_bound_runner_triggered_if_owner_fails": True,
        "q_loc_bound_runner_scored": False,
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
