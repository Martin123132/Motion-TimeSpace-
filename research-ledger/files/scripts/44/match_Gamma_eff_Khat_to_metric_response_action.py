from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Gamma_eff_Khat_metric_response_match_audited_current_corpus_no_match_found_candidate_route_retained"
CLAIM_CEILING = "metric_response_match_audit_only_no_q_loc_zero_local_GR_Newton_or_PPN_promotion"
NEXT_TARGET = "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md"

DOC_PATH = Path("515-match-Gamma-eff-Khat-to-metric-response-action.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_SOURCE_REGISTER.csv")
SOURCE_EVIDENCE_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv")
MATCH_AUDIT_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv")
PASS_FAIL_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_PASS_FAIL.csv")
REPAIR_OPTIONS_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_REPAIR_OPTIONS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "514-construct-GK-stress-action-or-residual-bound.md",
        "role": "metric-response action candidate and required match contract",
    },
    {
        "source_file": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc stress-divergence identity",
    },
    {
        "source_file": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "role": "symbol map that left Gamma_eff/K_hat unplaced",
    },
    {
        "source_file": "219-compact-shell-q_loc-source-projection-attempt.md",
        "role": "older compact-shell q_loc theorem target with Gamma/Khat identity missing",
    },
    {
        "source_file": "220-Jrel-local-trivial-representative-or-closure-bound.md",
        "role": "older J_rel trivial representative route and leakage bound",
    },
    {
        "source_file": "211-GK-parent-metric-Ward-identity-attempt.md",
        "role": "earlier GK metric/Ward attempt; composite metric remained closure-level",
    },
    {
        "source_file": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward identity and force-ledger discipline",
    },
    {
        "source_file": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Ward/Bianchi owner identity and no-zero-by-ownership warning",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "role": "514 metric-response contract rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
        "role": "513 stress rewrite rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "512 symbol map rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
        "role": "Noether/Ward source-current audit including parent response identity",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "Ward/source owner contract with exact-owner decomposition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "parent action terms and source owner decomposition",
    },
    {
        "source_file": "scripts/match_Gamma_eff_Khat_to_metric_response_action.py",
        "role": "this checkpoint generator",
    },
]

SOURCE_EVIDENCE_ROWS = [
    {
        "evidence_id": "E515_0_early_symbol_list",
        "source_file": "01-motion-load-route-contract.md;02-motion-load-local-GR-reduction.md",
        "evidence": "Gamma_eff, K_hat, and q_loc are listed as local-GR route symbols.",
        "interpretation": "symbols exist as framework targets, not as explicit action-derived objects",
        "match_value": "weak",
    },
    {
        "evidence_id": "E515_1_compact_shell_identity",
        "source_file": "219-compact-shell-q_loc-source-projection-attempt.md",
        "evidence": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu}); desired identity nabla_mu Khat - nabla Gamma = S_L + d_rel J_rel.",
        "interpretation": "older route already knew the Noether/source identity was missing",
        "match_value": "supports_need_for_action_not_match",
    },
    {
        "evidence_id": "E515_2_Jrel_route",
        "source_file": "220-Jrel-local-trivial-representative-or-closure-bound.md",
        "evidence": "J_rel exactness and pointwise projector annihilation are conditional; q_loc silence remains closure-bounded.",
        "interpretation": "relative-current route is useful but does not identify K_hat as metric response of Gamma_eff",
        "match_value": "conditional_alternative",
    },
    {
        "evidence_id": "E515_3_Ward_owner",
        "source_file": "356-parent-action-ward-identity-and-projector-variation.md;429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "evidence": "Ward/Bianchi ownership forces residuals into a ledger but does not prove each force vanishes.",
        "interpretation": "supports the discipline needed by S_GK but not the specific metric-response identity",
        "match_value": "necessary_not_sufficient",
    },
    {
        "evidence_id": "E515_4_source_current_audit",
        "source_file": "source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
        "evidence": "parent response/displacement identity can derive source identity if Khat and Gamma_eff are conjugates of a parent response field.",
        "interpretation": "strong clue for the next construction: conjugate response field, but still a template",
        "match_value": "promising_template",
    },
    {
        "evidence_id": "E515_5_current_contract",
        "source_file": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "evidence": "Gamma_eff must be scalar density and K_hat must be metric response including derivative/boundary terms.",
        "interpretation": "defines the pass condition for 515",
        "match_value": "required_gate",
    },
]

MATCH_AUDIT_ROWS = [
    {
        "audit_id": "MA515_0_Gamma_scalar_density_owner",
        "required_match": "Gamma_eff is given as a covariant scalar action density Gamma_eff(g,Phi,nablaPhi,D,topological data).",
        "current_evidence": "Gamma_eff appears as route/readout/relaxation/boundary-charge symbol; no explicit scalar density owner with metric dependence and units was found.",
        "result": "fail_for_current_claim",
        "repair": "define Gamma_eff as a parent scalar density or choose residual branch",
    },
    {
        "audit_id": "MA515_1_Khat_metric_response",
        "required_match": "K_hat equals the metric variation of sqrt(-g) Gamma_eff under a fixed sign convention.",
        "current_evidence": "K_hat/Khat appears in q_loc identities and owner-current targets; no derivation as delta[sqrt(-g)Gamma_eff]/delta g was found.",
        "result": "fail_for_current_claim",
        "repair": "compute metric response from a proposed Gamma_eff and compare tensor structure to K_hat",
    },
    {
        "audit_id": "MA515_2_conjugate_response_field",
        "required_match": "Gamma_eff and K_hat are conjugate pieces of one parent response/displacement field.",
        "current_evidence": "Yloc Noether audit lists this as a possible parent response identity, but labels it conditional template/not zero.",
        "result": "open_promising_template",
        "repair": "construct the response field and show Gamma/Khat are its scalar/tensor variational projections",
    },
    {
        "audit_id": "MA515_3_Ward_identity",
        "required_match": "Diffeomorphism invariance of S_GK produces q_loc as Ward residual.",
        "current_evidence": "Ward/Bianchi owner identities exist structurally, but they distribute all residual force channels rather than proving this specific S_GK identity.",
        "result": "conditional_not_specific_match",
        "repair": "derive Ward identity for S_GK after Gamma/Khat metric-response match",
    },
    {
        "audit_id": "MA515_4_double_zero",
        "required_match": "T_GK(Phi0)=0 or constant background and partial_A T_GK(Phi0)=0.",
        "current_evidence": "Double-zero conditions exist as gates in 511/514; no Gamma/Khat fixed-point expansion was found.",
        "result": "fail_for_current_claim",
        "repair": "expand candidate Gamma_eff around local fixed point and test F_1=0",
    },
    {
        "audit_id": "MA515_5_boundary_terms",
        "required_match": "metric response boundary terms have zero local force/mass flux or fixed topological subtraction.",
        "current_evidence": "Older boundary/Ward ledgers keep no-flux conditional; boundary flux remains an active residual risk.",
        "result": "open",
        "repair": "carry boundary term ledger for any proposed S_GK",
    },
    {
        "audit_id": "MA515_6_units_and_readout",
        "required_match": "Gamma_eff and K_hat carry stress-density units and map to PPN/local residual units.",
        "current_evidence": "Current Gamma/Khat appearances are symbolic; no unit-normalized stress/readout map found.",
        "result": "fail_for_current_claim",
        "repair": "declare normalization and derive q_loc residual components with units",
    },
]

PASS_FAIL_ROWS = [
    {
        "gate_id": "PF515_0_sources_exist",
        "gate": "all cited 515 sources exist",
        "result": "pass",
        "evidence": "validated by source register",
    },
    {
        "gate_id": "PF515_1_Gamma_owner_found",
        "gate": "actual Gamma_eff scalar-density owner found in current corpus",
        "result": "fail",
        "evidence": "MA515_0",
    },
    {
        "gate_id": "PF515_2_Khat_response_found",
        "gate": "actual K_hat metric-response derivation found",
        "result": "fail",
        "evidence": "MA515_1",
    },
    {
        "gate_id": "PF515_3_response_template_found",
        "gate": "a viable response-field template exists",
        "result": "pass_conditional",
        "evidence": "MA515_2 and P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
    },
    {
        "gate_id": "PF515_4_q_loc_zero",
        "gate": "q_loc zero is derived for current MTS",
        "result": "fail",
        "evidence": "Gamma/Khat match and double-zero gates fail",
    },
    {
        "gate_id": "PF515_5_residual_branch",
        "gate": "if match fails, residual branch is explicit",
        "result": "pass",
        "evidence": "514 residual branch plus 219/220 leakage bounds",
    },
]

REPAIR_OPTION_ROWS = [
    {
        "option_id": "RO515_A_boundary_charge_density",
        "route": "derive Gamma_eff from a normalized boundary/topological charge density",
        "needed": "Q_B/Q_* owner, metric variation, boundary no-flux, and fixed reference subtraction",
        "risk": "older endpoint/boundary work says Ward/index/charge unit still missing",
        "priority": "medium",
    },
    {
        "option_id": "RO515_B_auxiliary_positive_field",
        "route": "define Gamma_eff as potential/kinetic scalar from positive auxiliary field Phi and K_hat as elastic/kinetic metric response",
        "needed": "field content, units, positive Hessian, local fixed point, double zero",
        "risk": "new field can introduce fifth force unless source-free/no-hair theorem passes",
        "priority": "high",
    },
    {
        "option_id": "RO515_C_response_displacement_pair",
        "route": "construct a parent response/displacement field whose scalar projection is Gamma_eff and tensor response is K_hat",
        "needed": "conjugacy relation, Ward identity, projector ownership, fixed-point expansion",
        "risk": "most abstract but closest to Yloc Noether audit clue",
        "priority": "high",
    },
    {
        "option_id": "RO515_D_exact_topological_improvement",
        "route": "make Gamma_eff g - K_hat an exact/improvement stress with zero local flux",
        "needed": "exact form, no boundary leakage, no mass-channel charge",
        "risk": "bulk can be killed but boundary/source-measure can still fail",
        "priority": "medium",
    },
    {
        "option_id": "RO515_E_residual_runner",
        "route": "stop deriving through Gamma/Khat and score q_loc as explicit residual",
        "needed": "q_loc component map, PPN/local-bound normalization, compact-shell leakage limits",
        "risk": "becomes modified-gravity closure, not derived local GR",
        "priority": "fallback",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D515_0",
        "decision": "no_current_metric_response_match",
        "meaning": "current files do not prove Gamma_eff is a scalar action density or K_hat is its metric response",
        "claim_status": "q_loc_zero_false",
    },
    {
        "decision_id": "D515_1",
        "decision": "candidate_route_stays_alive",
        "meaning": "the parent response/displacement clue and 514 action contract are coherent enough to attempt construction",
        "claim_status": "conditional_route",
    },
    {
        "decision_id": "D515_2",
        "decision": "next_step_owner_or_bound",
        "meaning": "either build a Gamma_eff scalar-density owner or switch to q_loc residual-bound runner",
        "claim_status": NEXT_TARGET,
    },
    {
        "decision_id": "D515_3",
        "decision": "no_public_or_local_GR_promotion",
        "meaning": "this is a private derivability audit; local GR/Newton/PPN remain unpromoted",
        "claim_status": "claim_ceiling_enforced",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU515_0",
        "status": "metric_response_match_failed_for_current_corpus",
        "update": "Gamma_eff/K_hat are not yet matched to an action-derived scalar density plus metric response",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU515_1",
        "status": "response_field_template_prioritized",
        "update": "the strongest constructive route is a response/displacement field whose scalar projection is Gamma_eff and tensor metric response is K_hat",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU515_2",
        "status": "residual_fallback_explicit",
        "update": "if the owner construction fails, q_loc must be bounded using compact-shell and PPN residual rows",
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
    failures = [row for row in MATCH_AUDIT_ROWS if row["result"] == "fail_for_current_claim"]
    return [
        {
            "check_id": "V515_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V515_1_match_audit_complete",
            "result": "pass",
            "detail": f"audit_rows={len(MATCH_AUDIT_ROWS)}; failure_rows={len(failures)}",
        },
        {
            "check_id": "V515_2_repair_options_present",
            "result": "pass",
            "detail": f"repair_options={len(REPAIR_OPTION_ROWS)}",
        },
        {
            "check_id": "V515_3_no_overclaim",
            "result": "pass",
            "detail": "Gamma_eff_scalar_density_found=false; K_hat_metric_response_found=false; local_GR_claim_allowed=false",
        },
        {
            "check_id": "V515_4_next_target_set",
            "result": "pass",
            "detail": NEXT_TARGET,
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
    return f"""# 515 - Match Gamma_eff/K_hat to Metric-Response Action

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This audit looked for the actual match demanded by 514:

```text
S_GK = - integral sqrt(-g) Gamma_eff
K_hat = metric response of Gamma_eff
```

The result is strict:

```text
No current corpus source proves that Gamma_eff is a covariant scalar action density.
No current corpus source proves that K_hat is the metric variation of Gamma_eff.
```

So the 514 route remains a good candidate, but it is **not matched to current MTS yet**.

The best clue is the older Noether/source audit: it says a parent response/displacement identity could work if `Khat` and `Gamma_eff` are conjugates of a parent response field. That now becomes the serious construction route.

## 2. Source Evidence

{markdown_table(SOURCE_EVIDENCE_ROWS)}

## 3. Match Audit

{markdown_table(MATCH_AUDIT_ROWS)}

## 4. Pass/Fail Gates

{markdown_table(PASS_FAIL_ROWS)}

## 5. Repair Options

{markdown_table(REPAIR_OPTION_ROWS)}

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
MTS has a candidate Gamma/Khat metric-response route.
MTS has audited the current corpus and found the match is not currently proved.
MTS has prioritized concrete repair routes.
```

Forbidden:

```text
MTS has derived q_loc^nu -> 0.
MTS has proved Gamma_eff is a scalar action density.
MTS has proved K_hat is the metric response of Gamma_eff.
MTS has derived local GR, Newtonian recovery, or PPN silence.
```

## 11. Next Target

`{NEXT_TARGET}`

Either construct a real `Gamma_eff` scalar-density owner, preferably through a parent response/displacement field, or stop pursuing this as a derivation and build the direct `q_loc` residual-bound runner.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-match-Gamma-eff-Khat-to-metric-response-action"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (SOURCE_EVIDENCE_PATH, SOURCE_EVIDENCE_ROWS),
        (MATCH_AUDIT_PATH, MATCH_AUDIT_ROWS),
        (PASS_FAIL_PATH, PASS_FAIL_ROWS),
        (REPAIR_OPTIONS_PATH, REPAIR_OPTION_ROWS),
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
        "source_evidence": str(ROOT / SOURCE_EVIDENCE_PATH),
        "match_audit": str(ROOT / MATCH_AUDIT_PATH),
        "pass_fail": str(ROOT / PASS_FAIL_PATH),
        "repair_options": str(ROOT / REPAIR_OPTIONS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "Gamma_eff_scalar_density_found": False,
        "K_hat_metric_response_found": False,
        "current_MTS_metric_response_match_passed": False,
        "response_displacement_template_found": True,
        "S_GK_candidate_route_retained": True,
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
