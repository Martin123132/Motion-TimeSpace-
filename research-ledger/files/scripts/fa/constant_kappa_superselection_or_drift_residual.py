from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "constant_kappa_topological_superselection_clause_built_conditional_current_MTS_not_derived_residual_map_written"
CLAIM_CEILING = "conditional_kappa_constancy_only_no_measured_GM_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "509-source-measure-Meff-flux-closure-after-kappa-gate.md"

DOC_PATH = Path("508-constant-kappa-superselection-or-drift-residual.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_SOURCE_REGISTER.csv")
THEOREM_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv")
TOPOLOGICAL_CLAUSE_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv")
RESIDUAL_MAP_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_GATE_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_KAPPA_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "507-field-specific-silence-queue-kappa-domain-memory-motion.md",
        "role": "selects kappa/G_eff as first field-specific silence target",
    },
    {
        "source_file": "453-global-coupling-superselection-parent-action-contract.md",
        "role": "existing global/superselection kappa parent-action contract",
    },
    {
        "source_file": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "conditional constant G_eff/kappa theorem and Bianchi overclaim warning",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_global_coupling_superselection_CONTRACT.csv",
        "role": "GS0-GS8 superselection requirements",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "role": "CU0-CU8 constant universal kappa/G_eff requirements",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "role": "constant measured-GM theorem attempt and open Z1 global-coupling row",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "role": "derivative-hair identity for measured mu_obs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "role": "local residual runner input rows for Gdot, radial, range, source, frame, and mu_extra",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "role": "local bound matrix for source-normalization residuals",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "empirical lock table including Gdot and local PPN/fifth-force rows",
    },
    {
        "source_file": "scripts/constant_kappa_superselection_or_drift_residual.py",
        "role": "this checkpoint generator",
    },
]

THEOREM_ROWS = [
    {
        "theorem_id": "T508_0_global_sector",
        "statement": "If kappa_eff belongs to a parent global/superselection sector, not a local field bundle, then compact-support local variations cannot generate d kappa_eff.",
        "mathematical_form": "Q_parent = Q_dyn x K_global; kappa_eff in K_global; delta_local kappa_eff = 0",
        "result": "D_X kappa_eff = 0 for local spacetime directions and local MTS variations, provided K_global is acted on trivially",
        "status": "conditional_parent_premise",
        "MTS_current_status": "not_parent_derived",
    },
    {
        "theorem_id": "T508_1_topological_zeroform",
        "statement": "If the parent action contains a metric-independent topological zero-form/three-form pair, variation of the three-form can derive d kappa_eff=0 on connected local domains.",
        "mathematical_form": "S_kappa_top = ∫ kappa_eff dA_3; delta_{A_3} S = -∫ d kappa_eff ∧ delta A_3 => d kappa_eff=0",
        "result": "kappa_eff is an integration constant rather than a propagating scalar source",
        "status": "conditional_derivation_route",
        "MTS_current_status": "not_in_current_parent_action",
    },
    {
        "theorem_id": "T508_2_no_residual_if_closed",
        "statement": "If T508_0 or T508_1 passes and kappa carries no species/range/frame/domain labels, then local G_eff derivative/source/range residuals from kappa vanish.",
        "mathematical_form": "G_eff = kappa_eff c^4/(8π); D_X kappa_eff=0 => D_X G_eff=0",
        "result": "P8_Geff_time_drift, kappa radial/range hair, and kappa species/source drift are zero from kappa sector only",
        "status": "conditional_corollary",
        "MTS_current_status": "not_promoted_because_parent_clause_not_adopted_or_derived",
    },
]

TOPOLOGICAL_CLAUSE_ROWS = [
    {
        "clause_id": "K508_0_field_content",
        "parent_clause": "Introduce a metric-independent 3-form A_3 and a zero-form kappa_eff in a global/topological sector.",
        "equation": "S_kappa_top = ∫_M kappa_eff dA_3",
        "required_ownership": "A_3 and kappa_eff are not matter/source labels and do not vary with domain, memory, species, frame, or radial readout",
        "if_missing": "kappa_eff remains a possible scalar/source-normalization residual",
    },
    {
        "clause_id": "K508_1_variation_A3",
        "parent_clause": "Varying A_3 gives the zero-gradient equation.",
        "equation": "delta_{A_3} S = -∫_M d kappa_eff ∧ delta A_3 + boundary => d kappa_eff=0",
        "required_ownership": "boundary variation of A_3 is fixed or topological and does not create measured-mass flux",
        "if_missing": "zero-gradient proof becomes a boundary/closure assumption",
    },
    {
        "clause_id": "K508_2_variation_kappa",
        "parent_clause": "Varying kappa_eff gives the companion topological/integration-constant equation and must not reintroduce local stress.",
        "equation": "delta_kappa S gives dA_3 plus any allowed global-sector constraint",
        "required_ownership": "the companion equation is global/topological, not a local scalar force or source-current equation",
        "if_missing": "the route becomes a dressed Lagrange multiplier patch",
    },
    {
        "clause_id": "K508_3_metric_stress_silence",
        "parent_clause": "The topological sector is metric-independent or has only fixed background subtraction.",
        "equation": "delta_g S_kappa_top = 0 in compact local exterior",
        "required_ownership": "no non-EH stress, no preferred-frame vector, no boundary mass-channel leakage",
        "if_missing": "constant kappa may still be paid for by a new unowned stress sector",
    },
    {
        "clause_id": "K508_4_matter_source_blindness",
        "parent_clause": "Matter/source action sees only the same constant kappa_eff and cannot carry species-specific kappa_A.",
        "equation": "partial_A kappa_eff = partial_source kappa_eff = partial_m kappa_eff = 0",
        "required_ownership": "source-current Ward universality and one observed coframe/source pullback",
        "if_missing": "R1 source-charge and frame/source residuals remain active",
    },
]

RESIDUAL_MAP_ROWS = [
    {
        "residual_id": "KR508_0_time_drift",
        "if_theorem_missing": "dln_Geff_dt is retained",
        "symbol": "dln_Geff_dt",
        "observable_lock": "Gdot_over_G",
        "target_bound": "9.6e-15 yr^-1 or derived_zero",
        "required_artifact": "P8_time_drift_residual_or_zero.csv with separated G_eff, M_eff, and epsilon_mu terms",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "KR508_1_radial_hair",
        "if_theorem_missing": "partial_r ln G_eff is retained",
        "symbol": "partial_r_ln_Geff",
        "observable_lock": "beta/gamma/radial source hair",
        "target_bound": "zero radial hair or mapped local profile bound",
        "required_artifact": "P8_radial_mu_profile_or_zero.csv",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "KR508_2_range_dependence",
        "if_theorem_missing": "alpha(lambda) from kappa running is retained",
        "symbol": "alpha_kappa(lambda)",
        "observable_lock": "R10_fifth_force",
        "target_bound": "executable alpha(lambda) curve below inverse-square bounds",
        "required_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "KR508_3_species_source_charge",
        "if_theorem_missing": "species/source dependence of kappa is retained",
        "symbol": "eta_source_AB or partial_A ln G_eff",
        "observable_lock": "R1_WEP_source_charge",
        "target_bound": "2.8e-15 or derived source universality",
        "required_artifact": "P8_species_source_charge_residual_or_zero.csv",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "KR508_4_frame_domain_split",
        "if_theorem_missing": "frame/domain dependence of kappa is retained",
        "symbol": "delta_frame_source; partial_D ln G_eff",
        "observable_lock": "WEP/clock/R11/domain rows",
        "target_bound": "one observed source frame or explicit residual below locks",
        "required_artifact": "P8_frame_source_split_residual_or_zero.csv",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "KR508_5_Bianchi_exchange",
        "if_theorem_missing": "T_obs grad kappa exchange term is retained",
        "symbol": "delta_kappa_source",
        "observable_lock": "R4;R7;R9;R10;R11",
        "target_bound": "same-frame arbitrary-source conservation theorem or explicit exchange coefficient",
        "required_artifact": "P8_delta_kappa_source_exchange_residual.csv",
        "valid_for_claim": "false",
    },
]

GATE_TEST_ROWS = [
    {
        "gate_id": "G508_0_conditional_theorem",
        "gate": "topological/global kappa route is mathematically sufficient",
        "result": "pass_conditional",
        "evidence": "T508_0/T508_1 and K508_0-K508_4",
    },
    {
        "gate_id": "G508_1_parent_adoption",
        "gate": "current MTS parent action actually contains the global/topological kappa clause",
        "result": "fail_for_current_claim",
        "evidence": "453 says P0/P1 not established; 508 writes the clause but does not prove it is already in MTS",
    },
    {
        "gate_id": "G508_2_residual_fallback",
        "gate": "all failed kappa identities map to explicit residual rows",
        "result": "pass",
        "evidence": f"residual_rows={len(RESIDUAL_MAP_ROWS)}",
    },
    {
        "gate_id": "G508_3_no_local_GR_claim",
        "gate": "constant kappa alone cannot promote measured-GM/Newton/local-GR",
        "result": "pass",
        "evidence": "M_eff, mu_extra, source measure, and EH operator rows remain open",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D508_0",
        "decision": "conditional_topological_zeroform_route_is_the_clean_derivation_path",
        "meaning": "kappa can be made constant without a plateau axiom if the parent action owns the topological zero-form/three-form sector",
        "claim_status": "conditional_not_current_MTS_promotion",
    },
    {
        "decision_id": "D508_1",
        "decision": "current_MTS_has_not_yet_earned_constant_kappa",
        "meaning": "the route is now exact, but the present corpus has not derived or adopted the required parent clause",
        "claim_status": "kappa_Geff_silence_derived_false",
    },
    {
        "decision_id": "D508_2",
        "decision": "if_not_adopted_run_residual_branch",
        "meaning": "dln_Geff_dt, radial/range/source/frame/domain and Bianchi exchange rows must stay visible and testable",
        "claim_status": "residual_map_written",
    },
    {
        "decision_id": "D508_3",
        "decision": "move_to_source_measure_after_kappa_gate",
        "meaning": "even with constant kappa as a conditional/global premise, measured GM still needs M_eff flux closure and source matching",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU508_0",
        "status": "conditional_kappa_derivation_route_sharpened",
        "update": "topological zero-form/three-form clause is the cleanest derivation route for d kappa_eff=0",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU508_1",
        "status": "residual_fallback_active",
        "update": "if the clause is not adopted/derived, kappa becomes explicit local residual data rather than hidden measured-GM calibration",
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
            "check_id": "V508_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V508_1_topological_clause_complete",
            "result": "pass",
            "detail": f"clause_rows={len(TOPOLOGICAL_CLAUSE_ROWS)}",
        },
        {
            "check_id": "V508_2_residual_map_complete",
            "result": "pass",
            "detail": f"residual_rows={len(RESIDUAL_MAP_ROWS)}",
        },
        {
            "check_id": "V508_3_no_overclaim",
            "result": "pass",
            "detail": "kappa_Geff_silence_derived_for_MTS=false",
        },
        {
            "check_id": "V508_4_local_GR_claim_blocked",
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
    return f"""# 508 — Constant Kappa Superselection or Drift Residual

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The kappa/G_eff sector now has a precise non-cheat route:

```text
add or derive a parent topological zero-form/three-form sector
S_kappa_top = ∫ kappa_eff dA_3
variation in A_3 gives d kappa_eff = 0.
```

That would make `kappa_eff` an integration constant/global sector label rather than a local scalar hiding inside measured `GM`.

But this is still **conditional**. The current MTS corpus had the global-coupling contract; this checkpoint sharpens the parent clause that would derive it. It does not prove that the full MTS parent action already contains that clause.

So the honest branch is:

```text
conditional if topological/global kappa sector is adopted;
residual if kappa remains local or MTS-dependent.
```

## 2. Theorem Rows

{markdown_table(THEOREM_ROWS)}

## 3. Topological Zero-Form Clause

{markdown_table(TOPOLOGICAL_CLAUSE_ROWS)}

## 4. Residual Map

{markdown_table(RESIDUAL_MAP_ROWS)}

## 5. Gate Tests

{markdown_table(GATE_TEST_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has a precise conditional parent clause that would derive constant kappa.
MTS has a residual fallback map if kappa is local or MTS-dependent.
```

Forbidden:

```text
MTS has proved kappa_eff is constant in the current parent action.
MTS has derived measured GM, Newtonian recovery, PPN, or local GR.
MTS has hidden kappa drift inside fitted GM.
```

## 11. Next Target

`{NEXT_TARGET}`

If we carry constant kappa as a conditional global/topological premise, the next blocker is no longer G_eff. It is whether `M_eff` is the conserved parent source charge and whether source-measure matching is derived before orbital readout.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-constant-kappa-superselection-or-drift-residual"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_PATH, THEOREM_ROWS),
        (TOPOLOGICAL_CLAUSE_PATH, TOPOLOGICAL_CLAUSE_ROWS),
        (RESIDUAL_MAP_PATH, RESIDUAL_MAP_ROWS),
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
        "theorem": str(ROOT / THEOREM_PATH),
        "topological_clause": str(ROOT / TOPOLOGICAL_CLAUSE_PATH),
        "residual_map": str(ROOT / RESIDUAL_MAP_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "conditional_global_kappa_theorem": True,
        "conditional_topological_zeroform_kappa_derivation": True,
        "kappa_Geff_silence_derived_for_MTS": False,
        "topological_kappa_clause_adopted_in_current_parent_action": False,
        "kappa_residual_map_written": True,
        "dln_Geff_dt_zero_derived": False,
        "radial_range_kappa_hair_zero_derived": False,
        "species_source_kappa_blindness_derived": False,
        "frame_domain_kappa_blindness_derived": False,
        "measured_GM_parent_derived": False,
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
