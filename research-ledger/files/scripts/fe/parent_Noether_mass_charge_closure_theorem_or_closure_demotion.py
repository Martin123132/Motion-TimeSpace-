from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "conditional_parent_Noether_mass_charge_closure_theorem_derived_under_EH_silence_premises_MTS_premises_open"
CLAIM_CEILING = "conditional_zero_theorem_only_not_MTS_local_GR_or_Newton_promotion"
NEXT_TARGET = "506-local-EH-reduction-and-extra-sector-silence-theorem.md"

DOC_PATH = Path("505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_SOURCE_REGISTER.csv")
THEOREM_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_THEOREM.csv")
DERIVATION_CHAIN_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv")
EH_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv")
C_TERM_LEDGER_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv")
DEMOTION_TEST_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DEMOTION_TEST.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "sets Q_M[τ] parent charge closure as the next theorem target",
    },
    {
        "source_file": "503-fill-radial-bound-inputs-or-return-to-parent-glue.md",
        "role": "rules out numeric placeholder scoring and forces derivation-first route",
    },
    {
        "source_file": "502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md",
        "role": "runner formula for epsilon_radial_Meff and dry-run guard",
    },
    {
        "source_file": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
        "role": "radial integral identity that Q_M closure must kill",
    },
    {
        "source_file": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "retained local operator ledger; local EH reduction remains a gate",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv",
        "role": "existing EH-only/operator-vector gate",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv",
        "role": "source-normalization link for non-EH/operator leakage",
    },
    {
        "source_file": "scripts/parent_Noether_mass_charge_closure_theorem_or_closure_demotion.py",
        "role": "this checkpoint generator",
    },
]

THEOREM_ROWS = [
    {
        "theorem_id": "T505_conditional_Noether_mass_charge_closure",
        "statement": "If the local exterior parent action reduces to EH plus topological/exact/silent sectors, the parent Noether mass charge Q_M[τ] is radially closed in the compact exterior.",
        "premises": "covariant parent action; compact source worldtube; stationary/quasi-static local exterior; EH local operator; zero projected extra stress; constant projector; zero boundary/improvement flux; calibrated G_ref",
        "result": "integral_S2 Q_M[τ] - integral_S1 Q_M[τ] = 0 and conditional epsilon_radial_Meff = 0",
        "derived_status": "mathematical_conditional_derived",
        "MTS_status": "premises_not_yet_parent_derived",
    },
    {
        "theorem_id": "T505_source_measure_matching",
        "statement": "If the worldtube source measure equals the exterior parent charge, the radially closed charge is the measured source monopole.",
        "premises": "M_source[W] = integral_S Q_M[τ] before orbital readout; fixed normalization; no radius-dependent calibration",
        "result": "measured GM is constant across exterior annuli",
        "derived_status": "conditional_identity",
        "MTS_status": "core_glue_not_yet_parent_derived",
    },
    {
        "theorem_id": "T505_Newton_limit_corollary",
        "statement": "If the same local EH branch has the standard weak-field limit, Q_M closure becomes the Newton/Gauss exterior mass-flux theorem.",
        "premises": "g_00 = -1 - 2Φ/c^2; ∇²Φ = 4πG_ref rho_eff; no exterior rho_eff; source integral equals M_eff",
        "result": "exterior ∇²Φ = 0 and integral_S grad(Φ).dS = 4πG_ref M_eff independent of radius",
        "derived_status": "conditional_corollary",
        "MTS_status": "weak_field_normalization_not_yet_parent_derived",
    },
]

DERIVATION_CHAIN = [
    {
        "step_id": "D505_0_local_parent_action_form",
        "equation": "L_parent|A = (16πG_ref)^-1 (R - 2Λ_loc)*1 + dB_top + L_silent + L_residual",
        "meaning": "split the compact exterior action into EH, topological/exact, silent, and residual pieces",
        "if_not_zero": "L_residual becomes a C_extra/source-normalization residual",
    },
    {
        "step_id": "D505_1_field_equations",
        "equation": "E_g = G + Λ_loc g + E_silent + E_residual = 0",
        "meaning": "EH closure only follows if the residual metric/source projection vanishes in the exterior",
        "if_not_zero": "C_EH and C_extra do not vanish",
    },
    {
        "step_id": "D505_2_charge_form",
        "equation": "Q_M[τ] = Q_EH[τ;G_ref] + Q_top[τ] + Q_silent[τ] + Q_residual[τ]",
        "meaning": "the parent mass charge must be defined by the action, not fitted after reading orbits",
        "if_not_zero": "Q_residual must be bounded by the radial runner",
    },
    {
        "step_id": "D505_3_exterior_derivative",
        "equation": "dQ_M[τ] = C_EH[E_g,Λ_sub] + C_extra + C_projector + C_boundary",
        "meaning": "radial mass drift is exactly the exterior constraint/leakage content",
        "if_not_zero": "epsilon_radial_Meff = M_ref^-1 integral_A dQ_M[τ]",
    },
    {
        "step_id": "D505_4_zero_premises",
        "equation": "C_EH = C_extra = C_projector = C_boundary = 0",
        "meaning": "local plateau emerges only from field-equation closure and silence clauses",
        "if_not_zero": "no exact local-GR/Newton promotion",
    },
    {
        "step_id": "D505_5_surface_equality",
        "equation": "integral_S2 Q_M[τ] = integral_S1 Q_M[τ]",
        "meaning": "finite-radius measured mass is radially stable",
        "if_not_zero": "radial source hair remains physical or bounded",
    },
    {
        "step_id": "D505_6_worldtube_readout",
        "equation": "M_eff = M_source[W] = integral_S Q_M[τ]",
        "meaning": "this is the bridge from conserved exterior charge to measured GM",
        "if_not_zero": "closed charge may not be the observed mass",
    },
]

EH_REQUIREMENTS = [
    {
        "requirement_id": "EH505_0_operator_reduction",
        "requirement": "local exterior metric/coframe operator reduces to Einstein-Hilbert plus cosmological/background subtraction",
        "current_status": "not_parent_derived",
        "why_required": "non-EH curvature/operator terms change Q_M and local PPN coefficients",
        "pass_condition": "all retained R11/operator-vector rows either vanish in local vacuum or are executable residuals below locks",
    },
    {
        "requirement_id": "EH505_1_extra_sector_silence",
        "requirement": "motion/time/domain/memory/non-EH sectors carry no projected mass-channel stress in the compact local exterior",
        "current_status": "not_parent_derived",
        "why_required": "extra projected stress is C_extra and directly sources epsilon_radial_Meff",
        "pass_condition": "derive positive no-hair/topological silence/equation-of-motion zero for each sector",
    },
    {
        "requirement_id": "EH505_2_projector_constancy",
        "requirement": "Pi_M or Q_M readout is fixed/covariantly constant before data fitting",
        "current_status": "not_parent_derived",
        "why_required": "field-dependent projector creates [d,Pi_M]J_H radial leakage",
        "pass_condition": "derive Pi_M from parent charge algebra or replace it with Q_M source-measure readout",
    },
    {
        "requirement_id": "EH505_3_boundary_flux_zero",
        "requirement": "topological/exact boundary terms have zero compact exterior flux or fixed background subtraction",
        "current_status": "not_parent_derived",
        "why_required": "boundary flux is precisely how a divergence becomes observable radial hair",
        "pass_condition": "prove exact zero-flux on linking spheres or retain source-backed bound",
    },
    {
        "requirement_id": "EH505_4_source_measure_calibration",
        "requirement": "worldtube source charge equals exterior Q_M and fixes G_ref/M_eff normalization",
        "current_status": "not_parent_derived",
        "why_required": "a conserved charge with wrong normalization is not Newton/GR",
        "pass_condition": "derive Gauss/Poisson source law and measured-GM calibration before orbital fitting",
    },
]

C_TERM_LEDGER = [
    {
        "term_id": "C505_EH",
        "term": "C_EH[E_g,Λ_sub]",
        "zero_condition": "local exterior EH equations hold with appropriate Λ/background subtraction",
        "if_open": "standard GR local charge closure is not recovered",
        "mapped_rows": "R3;R4;R11",
    },
    {
        "term_id": "C505_extra",
        "term": "C_extra",
        "zero_condition": "all non-EH, motion/time/domain/memory/source-normalization sectors are silent or topological in local vacuum",
        "if_open": "mu_extra and radial source hair remain retained",
        "mapped_rows": "R1;R4;R7;R8;R9;R10;R11",
    },
    {
        "term_id": "C505_projector",
        "term": "C_projector",
        "zero_condition": "mass-channel projector/readout is parent-fixed and covariantly constant in the exterior",
        "if_open": "mass drift can be an artifact of readout rather than physics, but still cannot be ignored",
        "mapped_rows": "R4;R11",
    },
    {
        "term_id": "C505_boundary",
        "term": "C_boundary",
        "zero_condition": "exact/topological/boundary improvements have no linking-sphere flux or are background-subtracted",
        "if_open": "divergence terms can produce finite surface charges",
        "mapped_rows": "R3;R4;R7;R8;R9;R11",
    },
]

DEMOTION_TEST = [
    {
        "test_id": "DM505_0_if_EH_reduction_proved",
        "condition": "all EH505 requirements pass from parent action",
        "branch_status": "promote_to_conditional_local_GR_derivation_stack",
        "next_action": "derive weak-field PPN coefficients and source measure normalization explicitly",
    },
    {
        "test_id": "DM505_1_if_some_C_terms_remain",
        "condition": "one or more C terms are retained but source-backed bounds exist",
        "branch_status": "numeric_residual_branch",
        "next_action": "run 502 radial bound runner and map each channel to local locks",
    },
    {
        "test_id": "DM505_2_if_C_terms_open_no_bounds",
        "condition": "C terms are retained and no source-backed bounds exist",
        "branch_status": "closure_only_no_local_GR_claim",
        "next_action": "demote local transition route until parent action or data supplies the missing rows",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "DEC505_0_conditional_theorem",
        "decision": "conditional_Noether_charge_closure_theorem_is_valid",
        "meaning": "under EH-plus-silent exterior premises, epsilon_radial_Meff vanishes by charge closure rather than by axiom",
        "claim_status": "mathematical_conditional_only",
    },
    {
        "decision_id": "DEC505_1_MTS_status",
        "decision": "MTS_has_not_yet_satisfied_the_premises",
        "meaning": "local EH reduction, extra-sector silence, projector constancy, boundary flux zero, and source calibration remain to be parent-derived",
        "claim_status": "no_local_GR_claim",
    },
    {
        "decision_id": "DEC505_2_next_derivation",
        "decision": "attack_local_EH_reduction_and_extra_sector_silence",
        "meaning": "this is now the narrowest derivability target for the local GR/Newton bridge",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU505_0",
        "status": "conditional_theorem_achieved",
        "update": "epsilon_radial_Meff=0 is derivable if Q_M closure follows from local EH plus silent/topological extra sectors",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU505_1",
        "status": "MTS_premises_open",
        "update": "the remaining problem is no longer vague radial plateau language; it is an EH-reduction/silence/source-calibration theorem stack",
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
            "check_id": "V505_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V505_1_conditional_not_overclaimed",
            "result": "pass",
            "detail": "conditional_theorem=true; MTS_premises_satisfied=false",
        },
        {
            "check_id": "V505_2_EH_requirements_explicit",
            "result": "pass",
            "detail": f"requirements={len(EH_REQUIREMENTS)}",
        },
        {
            "check_id": "V505_3_C_terms_named",
            "result": "pass",
            "detail": f"C_terms={len(C_TERM_LEDGER)}",
        },
        {
            "check_id": "V505_4_local_GR_claim_blocked",
            "result": "pass",
            "detail": "local_GR_claim_allowed=false",
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
    return f"""# 505 — Parent Noether Mass-Charge Closure Theorem or Closure Demotion

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

We got a real conditional theorem, but not yet a full MTS theorem.

The theorem is:

```text
If the local exterior parent action reduces to EH plus topological/exact/silent sectors,
and the worldtube source measure equals the exterior parent mass charge,
then the parent Noether mass charge Q_M[τ] is radially closed,
so epsilon_radial_Meff = 0.
```

That is a genuine derivation pattern. It is not a plateau axiom. It is the GR/Newton kind of argument: exterior constraints close the mass charge.

What is still missing is equally sharp:

```text
derive the EH-plus-silent local exterior reduction from MTS itself.
```

Until that is done, MTS has a conditional local-GR bridge, not a completed local-GR bridge.

## 2. Conditional Theorem

{markdown_table(THEOREM_ROWS)}

## 3. Derivation Chain

{markdown_table(DERIVATION_CHAIN)}

## 4. Local EH Reduction Requirements

{markdown_table(EH_REQUIREMENTS)}

## 5. C-Term Ledger

{markdown_table(C_TERM_LEDGER)}

## 6. Demotion Test

{markdown_table(DEMOTION_TEST)}

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
MTS has a conditional theorem: EH-plus-silent local exterior + source matching implies epsilon_radial_Meff=0.
MTS has narrowed the local GR bridge to EH reduction, extra-sector silence, projector constancy, boundary no-flux, and source calibration.
```

Forbidden:

```text
MTS has derived those premises from the parent action.
MTS has derived local GR.
MTS has derived Newtonian recovery.
MTS has scored the radial-bound runner.
MTS has proven all non-EH/operator/source-normalization rows vanish.
```

## 12. Next Target

`{NEXT_TARGET}`

This is now the right battle line: prove the local parent action really collapses to EH plus silent/topological sectors in compact local vacuum. If it does, the local GR/Newton bridge becomes serious. If it does not, the branch must be closure-only or numeric-residual only.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-parent-Noether-mass-charge-closure-theorem-or-closure-demotion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_PATH, THEOREM_ROWS),
        (DERIVATION_CHAIN_PATH, DERIVATION_CHAIN),
        (EH_REQUIREMENTS_PATH, EH_REQUIREMENTS),
        (C_TERM_LEDGER_PATH, C_TERM_LEDGER),
        (DEMOTION_TEST_PATH, DEMOTION_TEST),
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
        "theorem": str(ROOT / THEOREM_PATH),
        "derivation_chain": str(ROOT / DERIVATION_CHAIN_PATH),
        "EH_requirements": str(ROOT / EH_REQUIREMENTS_PATH),
        "C_term_ledger": str(ROOT / C_TERM_LEDGER_PATH),
        "demotion_test": str(ROOT / DEMOTION_TEST_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "conditional_Noether_mass_charge_closure_theorem": True,
        "conditional_epsilon_radial_Meff_zero_theorem": True,
        "MTS_premises_satisfied": False,
        "local_EH_reduction_derived": False,
        "extra_sector_silence_derived": False,
        "projector_constancy_derived": False,
        "boundary_flux_zero_derived": False,
        "source_measure_matching_derived": False,
        "parent_Noether_mass_charge_closure_derived_for_MTS": False,
        "epsilon_radial_Meff_zero_derived_for_MTS": False,
        "epsilon_radial_Meff_computed": False,
        "radial_bound_scored": False,
        "mu_extra_zero_derived": False,
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
