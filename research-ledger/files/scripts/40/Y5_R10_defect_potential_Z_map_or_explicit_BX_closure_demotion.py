from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_defect_potential_Z_map_partial_flow_only_BX_demoted_to_explicit_closure_nonclaim"
CLAIM_CEILING = "partial_Z_Vdef_candidate_and_BX_closure_demotion_only_no_BX_claim_no_Qbar_no_alpha_edge_no_R10_no_PPN_no_local_GR_claim"
NEXT_TARGET = "682-Y5-R10-Qbar-numerator-denominator-source-pack-or-BX-closure-runner.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "681-Y5-R10-defect-potential-Z-map-or-explicit-BX-closure-demotion.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "210_doc": ROOT / "210-GK-alphaK-parent-invariant-or-fixed-closure.md",
    "211_doc": ROOT / "211-GK-parent-metric-Ward-identity-attempt.md",
    "222_doc": ROOT / "222-parent-X-sector-degree-count-and-boundary-action.md",
    "223_doc": ROOT / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "668_validation": RESIDUALS / "P8_Y5_BRR545_668_VALIDATION.csv",
    "668_boundary_lock": RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "673_validation": RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv",
    "673_acquisition": RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "675_validation": RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
    "675_blockers": RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
    "676_validation": RESIDUALS / "P8_Y5_BRR545_676_VALIDATION.csv",
    "677_validation": RESIDUALS / "P8_Y5_BRR545_677_VALIDATION.csv",
    "677_bx": RESIDUALS / "P8_Y5_R10_677_BX_EXACTNESS_OR_SOURCE_ROW.csv",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "678_silence": RESIDUALS / "P8_Y5_R10_678_SILENCE_STACK_AUDIT.csv",
    "679_validation": RESIDUALS / "P8_Y5_BRR545_679_VALIDATION.csv",
    "679_acquisition": RESIDUALS / "P8_Y5_R10_679_ACQUISITION_LEDGER.csv",
    "680_doc": ROOT / "680-Y5-R10-parent-P-constitutive-owner-or-Qbar-numeric-denominator-source.md",
    "680_validation": RESIDUALS / "P8_Y5_BRR545_680_VALIDATION.csv",
    "680_p_owner": RESIDUALS / "P8_Y5_R10_680_P_CONSTITUTIVE_OWNER_ATTEMPT.csv",
    "680_bx": RESIDUALS / "P8_Y5_R10_680_BX_CLAIM_ROW_CANDIDATE.csv",
    "680_qbar_gate": RESIDUALS / "P8_Y5_R10_680_QBAR_DENOMINATOR_SOURCE_GATE.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "210_doc": "coherence-defect vector and parent metric missing source",
        "211_doc": "partial flow-block metric and full composite metric closure source",
        "222_doc": "boundary momentum contract source",
        "223_doc": "P=dV_def/dZ contract and fail condition source",
        "235_doc": "projector stress/nohair source",
        "667_validation": "667 validation gate",
        "667_variation": "boundary flux ledger",
        "668_validation": "668 validation gate",
        "668_boundary_lock": "boundary/projector lock rows",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "673_validation": "673 validation gate",
        "673_acquisition": "Qbar acquisition ledger",
        "674_validation": "674 validation gate",
        "674_requirements": "edge coefficient requirements",
        "675_validation": "675 validation gate",
        "675_blockers": "edge blocker matrix",
        "676_validation": "676 validation gate",
        "677_validation": "677 validation gate",
        "677_bx": "BX exactness/source rows",
        "678_validation": "678 validation gate",
        "678_silence": "silence stack audit",
        "679_validation": "679 validation gate",
        "679_acquisition": "source acquisition ledger",
        "680_doc": "immediate predecessor checkpoint",
        "680_validation": "680 validation gate",
        "680_p_owner": "P constitutive owner attempt",
        "680_bx": "BX claim-row candidate",
        "680_qbar_gate": "Qbar denominator source gate",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def z_map_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "map_id": "ZMA681_0_flow_symmetric_block",
            "candidate_component": "Z_flow_mu_nu",
            "candidate_map": "Z_flow_mu_nu = sigma_mu_nu + (1/3) h_mu_nu delta_theta",
            "what_is_owned": "flow dispersion/shear block has partial ADM/DeWitt-style geometric ownership",
            "what_fails": "trace convention/sign and full stress variation are still not parent-signed",
            "verdict": "partial_candidate",
            "valid_for_claim": "false",
            "source_paths": source_list("211_doc", "210_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "ZMA681_1_vorticity_sector_mismatch",
            "candidate_component": "omega_mu_nu",
            "candidate_map": "vorticity is antisymmetric and belongs to a two-form/connection sector, not directly to symmetric P_mu_nu",
            "what_is_owned": "vorticity appears in Xi_D as a coherence-breaking component",
            "what_fails": "no parent map embeds it into the symmetric boundary momentum without adding a chosen projection",
            "verdict": "separate_sector_required",
            "valid_for_claim": "false",
            "source_paths": source_list("210_doc", "211_doc", "223_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "ZMA681_2_Weyl_projection",
            "candidate_component": "Z_W_mu_nu",
            "candidate_map": "Z_W_mu_nu = ell_W E_mu_nu[u_D] or scalar W_D times a selected STF direction",
            "what_is_owned": "W_D=(C_abcd C^abcd)^1/4 is a natural inverse-length scalar",
            "what_fails": "parent-normalized tensor projection, scale ell_W, and coefficient are not derived",
            "verdict": "closure_projection",
            "valid_for_claim": "false",
            "source_paths": source_list("210_doc", "211_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "ZMA681_3_Jrel_Q_projection",
            "candidate_component": "Z_JQ_mu_nu",
            "candidate_map": "relative current and load anisotropy require Hodge/response projections into a rank-2 tensor",
            "what_is_owned": "J_rel and delta Q enter Xi_D as named coherence-defect blocks",
            "what_fails": "representatives, normalization, and tensor embedding are missing",
            "verdict": "closure_projection",
            "valid_for_claim": "false",
            "source_paths": source_list("210_doc", "211_doc", "223_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "ZMA681_4_cross_terms",
            "candidate_component": "M_AB cross terms",
            "candidate_map": "M_AB block diagonal with flow/Weyl/Jrel/Q weights",
            "what_is_owned": "unit diagonal closure was declared safe only as predeclared closure",
            "what_fails": "single Ward identity for M_AB and cross-term vanish theorem fail",
            "verdict": "closure_metric",
            "valid_for_claim": "false",
            "source_paths": source_list("211_doc", "210_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "ZMA681_5_defect_potential",
            "candidate_component": "V_def",
            "candidate_map": "V_def = 1/2 integral sqrt(-g) Z_A M^{AB} Z_B",
            "what_is_owned": "quadratic potential is the mathematically minimal way to generate P_A=M_AB Z_B",
            "what_fails": "Z_A, full M_AB, stress variation, and cross terms are not parent-derived",
            "verdict": "formal_candidate_only",
            "valid_for_claim": "false",
            "source_paths": source_list("223_doc", "210_doc", "211_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "ZMA681_6_BX_pullback",
            "candidate_component": "B_X^nu",
            "candidate_map": "B_X^nu = n_mu M^{mu nu|A} Z_A + B_ct^nu",
            "what_is_owned": "boundary equation exists and P=dV/dZ would make the pullback meaningful",
            "what_fails": "B_ct, shell/domain, units, and boundary class remain missing",
            "verdict": "not_claim_ready",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "223_doc", "235_doc", "680_bx"),
            "generated_utc": now,
        },
        {
            "map_id": "ZMA681_7_verdict",
            "candidate_component": "full Z_mu_nu/V_def route",
            "candidate_map": "derive one parent response tensor Z_mu_nu from all coherence-defect variables",
            "what_is_owned": "flow block and algebraic trace/traceless projection are useful partial structure",
            "what_fails": "full tensor map would still be chosen to make B_X work unless new parent action supplies it",
            "verdict": "partial_flow_only_not_parent_derived",
            "valid_for_claim": "false",
            "source_paths": source_list("210_doc", "211_doc", "223_doc", "680_p_owner"),
            "generated_utc": now,
        },
    ]


def closure_demotion_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "closure_id": "BCD681_0_BX_status",
            "object": "B_X_boundary_momentum",
            "demotion": "explicit_closure_support",
            "reason": "no parent-derived full Z_mu_nu/V_def/M_AB map exists; using B_X as a claim row would smuggle choices",
            "allowed_use": "private model-building scaffold or nonclaim source-row template",
            "forbidden_use": "R10/PPN/local-GR evidence or theorem-zero",
            "valid_for_claim": "false",
            "source_paths": source_list("680_bx", "678_silence", "679_acquisition"),
            "generated_utc": now,
        },
        {
            "closure_id": "BCD681_1_flow_block_status",
            "object": "flow/shear/expansion piece",
            "demotion": "partial_parent_owned_subsector",
            "reason": "211 gives real geometric motivation but not full P tensor or boundary current",
            "allowed_use": "seed future Z map and local-suppression intuition",
            "forbidden_use": "standalone B_X normalization",
            "valid_for_claim": "false",
            "source_paths": source_list("211_doc", "210_doc"),
            "generated_utc": now,
        },
        {
            "closure_id": "BCD681_2_Weyl_Jrel_Q_status",
            "object": "Weyl/J_rel/Q pieces",
            "demotion": "closure_projection_required",
            "reason": "each needs a tensor representative and normalization not supplied by the parent action",
            "allowed_use": "explicitly labelled closure block",
            "forbidden_use": "hidden metric weights inside M_AB",
            "valid_for_claim": "false",
            "source_paths": source_list("210_doc", "211_doc", "223_doc"),
            "generated_utc": now,
        },
        {
            "closure_id": "BCD681_3_Qbar_fallback",
            "object": "Qbar_edge_XH(lambda)",
            "demotion": "next_source_route",
            "reason": "if B_X is closure, the honest empirical route is to source Q_edge/M_H_ref directly",
            "allowed_use": "build numerator/denominator source pack",
            "forbidden_use": "infer Qbar from closure B_X without units/frame/source",
            "valid_for_claim": "false",
            "source_paths": source_list("680_qbar_gate", "673_acquisition", "674_requirements"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D681_0_Z_map",
            "target": "concrete Z_mu_nu/V_def construction",
            "result": "partial_flow_only",
            "reason": "flow block is partially owned, but Weyl/current/load projections, full M_AB, and cross terms are closure",
            "next_action": "do not promote B_X from this route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D681_1_BX",
            "target": "B_X_boundary_momentum",
            "result": "demote_to_explicit_closure",
            "reason": "B_X cannot be a claim row unless a future parent action derives the full response tensor and boundary counterterm",
            "next_action": "treat B_X as nonclaim scaffold only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D681_2_next",
            "target": "Qbar fallback",
            "result": "selected",
            "reason": "with B_X demoted, the next honest measurable path is Q_edge numerator and M_H_ref denominator sourcing",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    z_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    z_claim = any(row["valid_for_claim"] == "true" for row in z_rows)
    closure_claim = any(row["valid_for_claim"] == "true" for row in closure_rows)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision)
    return [
        {
            "evaluator_id": "EV681_0_Z_map_attempt",
            "target": "derive full Z_mu_nu map",
            "status": "fail_nonclaim",
            "reason": f"z_claim={bool_text(z_claim)}; only flow block has partial ownership",
            "claim_effect": "P=dV/dZ remains unpromoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV681_1_BX_demotion",
            "target": "demote B_X if Z map is closure",
            "status": "pass_nonclaim",
            "reason": f"closure_claim={bool_text(closure_claim)}; B_X explicitly demoted to nonclaim closure support",
            "claim_effect": "no B_X claim row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV681_2_next_route",
            "target": "select next measurable route",
            "status": "selected_nonclaim",
            "reason": f"next_selected={bool_text(next_selected)}; Qbar numerator/denominator pack selected",
            "claim_effect": "next private checkpoint only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV681_3_claim_guardrail",
            "target": "prevent R10/local promotion",
            "status": "pass",
            "reason": "all generated 681 rows remain valid_for_claim=false",
            "claim_effect": "no R10/R11/PPN/local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS681_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "concrete Z/Vdef attempt yields partial flow ownership only; B_X demoted to explicit nonclaim closure",
            "blocked_claims": "P_owner;B_X_claim;Qedge_zero;Qbar_edge_XH;alpha_edge;R10;R11;PPN;clock;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_register: list[dict[str, str]],
    z_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_register if row["exists"] != "true"]
    rows.append({"check_id": "V681_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources), "generated_utc": now})

    validation_ids = ["667_validation", "668_validation", "671_validation", "673_validation", "674_validation", "675_validation", "676_validation", "677_validation", "678_validation", "679_validation", "680_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({"check_id": "V681_1_prior_validations_clean", "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail", "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()), "generated_utc": now})

    rows.append({"check_id": "V681_2_Z_map_attempt_coverage", "result": "pass" if len(z_rows) >= 8 else "fail", "detail": f"z_rows={len(z_rows)}", "generated_utc": now})

    verdict = [row for row in z_rows if row["map_id"] == "ZMA681_7_verdict"]
    rows.append({"check_id": "V681_3_Z_map_not_promoted", "result": "pass" if verdict and verdict[0]["verdict"] == "partial_flow_only_not_parent_derived" and all(row["valid_for_claim"] == "false" for row in z_rows) else "fail", "detail": "Z/Vdef route remains nonclaim", "generated_utc": now})

    bx_demotion = [row for row in closure_rows if row["object"] == "B_X_boundary_momentum" and row["demotion"] == "explicit_closure_support"]
    rows.append({"check_id": "V681_4_BX_demoted_to_closure", "result": "pass" if bx_demotion and all(row["valid_for_claim"] == "false" for row in closure_rows) else "fail", "detail": f"closure_rows={len(closure_rows)}", "generated_utc": now})

    selected = [row for row in decision if row["next_action"] == NEXT_TARGET]
    rows.append({"check_id": "V681_5_next_target_selected", "result": "pass" if selected else "fail", "detail": NEXT_TARGET, "generated_utc": now})

    generated = z_rows + closure_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append({"check_id": "V681_6_no_claim_rows_promoted", "result": "pass" if not claim_rows else "fail", "detail": "all generated 681 rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}", "generated_utc": now})

    output_paths = [
        RESIDUALS / "P8_Y5_R10_681_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_681_Z_MAP_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_681_BX_CLOSURE_DEMOTION.csv",
        RESIDUALS / "P8_Y5_R10_681_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_681_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_681_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_681_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({"check_id": "V681_7_generated_outputs_scoped", "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail", "detail": "all 681 outputs target post-checkpoint-work", "generated_utc": now})

    changed_count = formalization_changed_count()
    rows.append({"check_id": "V681_8_formalization_workbench_untouched", "result": "pass" if changed_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed_count}", "generated_utc": now})

    rows.append({"check_id": "V681_9_status_nonclaim", "result": "pass" if "no_BX_claim" in CLAIM_CEILING and "no_Qbar" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail", "detail": CLAIM_CEILING, "generated_utc": now})

    missing_or_closure = [row for row in z_rows + closure_rows if any(token in ";".join(str(value).lower() for value in row.values()) for token in ["missing", "closure", "not_parent_derived"])]
    rows.append({"check_id": "V681_10_missing_or_closure_blocks_claims", "result": "pass" if missing_or_closure and not claim_rows else "fail", "detail": f"blocking_rows={len(missing_or_closure)};claim_rows={len(claim_rows)}", "generated_utc": now})

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    z_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 681 - Y5 R10 Defect Potential Z Map Or Explicit BX Closure Demotion

## Verdict

681 tried the concrete `Z_mu_nu / V_def` construction.

The strongest honest candidate is:

```text
Z_flow_mu_nu = sigma_mu_nu + (1/3) h_mu_nu delta_theta
V_def = 1/2 integral sqrt(-g) Z_A M^AB Z_B
P_A = partial V_def / partial Z_A = M_AB Z_B
B_X^nu = n_mu P^{{mu nu}} + B_ct^nu
```

This is useful, but it only owns the flow/shear/expansion block partially. Vorticity is a two-form sector, Weyl needs a parent-normalized tensor projection, `J_rel` and `Q` need representatives, cross terms are still closure, and `B_ct/C_top` are missing.

So the result is decisive: `B_X` is demoted to explicit nonclaim closure support unless a future parent action derives the full `Z_mu_nu`, `V_def`, and `M_AB` stack. The next honest route is to source `Qbar_edge_XH(lambda)` by its numerator/denominator instead of pretending `B_X` has been derived.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Z Map Attempt

{markdown_table(z_rows, ["map_id", "candidate_component", "candidate_map", "what_is_owned", "what_fails", "verdict", "valid_for_claim"])}

## BX Closure Demotion

{markdown_table(closure_rows, ["closure_id", "object", "demotion", "reason", "allowed_use", "forbidden_use", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: build the `Qbar_edge_XH(lambda)` source pack directly: `Q_edge` numerator, `M_H_ref` denominator, lambda/support, units, reference, and frame convention. `B_X` can stay as labelled closure support, not evidence.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    z_rows = z_map_attempt_rows()
    closure_rows = closure_demotion_rows()
    decision = decision_rows()
    evaluator = evaluator_rows(z_rows, closure_rows, decision)
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, z_rows, closure_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_681_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_681_Z_MAP_ATTEMPT.csv", z_rows, ["map_id", "candidate_component", "candidate_map", "what_is_owned", "what_fails", "verdict", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_681_BX_CLOSURE_DEMOTION.csv", closure_rows, ["closure_id", "object", "demotion", "reason", "allowed_use", "forbidden_use", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_681_EVALUATOR.csv", evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_681_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_681_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_681_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, z_rows, closure_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"z_rows={len(z_rows)}")
    print(f"closure_rows={len(closure_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
