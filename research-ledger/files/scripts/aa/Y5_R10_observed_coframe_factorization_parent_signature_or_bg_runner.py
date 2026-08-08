from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md"
SCRIPT_REL = "scripts/Y5_R10_observed_coframe_factorization_parent_signature_or_bg_runner.py"
STATUS = "Y5_R10_observed_coframe_factorization_parent_signature_failed_bg_runner_blocks_claims"
CLAIM_CEILING = "private_parent_signature_and_bg_runner_only_no_bg_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md", "immediate handoff: factorization lemma and b_g prior"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_623_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv", "coframe factorization lemma"),
        ("source-intake/mts_residuals/P8_Y5_R10_623_FACTORIZATION_GATE.csv", "factorization gate rows"),
        ("source-intake/mts_residuals/P8_Y5_R10_623_BG_PRIOR_FILL.csv", "b_g prior rows"),
        ("source-intake/mts_residuals/P8_Y5_R10_623_ARENA_IMPACT.csv", "b_g arena impact"),
        ("622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md", "parent matter-sector contract"),
        ("source-intake/mts_residuals/P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv", "parent matter contract CSV"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "conditional coframe pullback theorem"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor attempt"),
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "selector theorem audit"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "no-extension and marker loopholes"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_signature_rows() -> list[dict[str, object]]:
    return [
        {
            "signature_id": "SIG624_0_parent_quotient",
            "signature_clause": "parent supplies q:Phi_parent -> Q_MTS before ordinary matter coupling",
            "required_source": "parent action or quotient construction",
            "current_status": "contract_only",
            "if_signed": "geometry factorization can be a parent statement",
            "if_unsigned": "X may be physical geometry data rather than vertical representative data",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG624_1_local_X_verticality",
            "signature_clause": "v_X is vertical to Q_MTS on the local matter branch: dq(v_X)=0",
            "required_source": "parent local branch definition",
            "current_status": "conditional_not_parent_signed",
            "if_signed": "Q-factorized coframes are blind to X",
            "if_unsigned": "common metric/coframe X response remains physical",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG624_2_matter_geometry_factorization",
            "signature_clause": "for all ordinary species A, e_A(Phi)=E_A(q(Phi))",
            "required_source": "parent matter action",
            "current_status": "not_signed",
            "if_signed": "Lie_vX e_A=0 for every ordinary species",
            "if_unsigned": "common_frame_log_derivative prior remains open",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG624_3_no_representative_Weyl",
            "signature_clause": "no matter-visible A_g(X) Weyl factor appears before quotient",
            "required_source": "parent no-representative-frame theorem",
            "current_status": "not_signed",
            "if_signed": "pure conformal c_g channel is absent",
            "if_unsigned": "c_g=d ln A_g/dXhat must be treated as a prior",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG624_4_no_representative_disformal",
            "signature_clause": "no matter-visible B_g(X) disformal/tensor frame appears before quotient",
            "required_source": "parent no-representative-frame theorem",
            "current_status": "not_signed",
            "if_signed": "disformal common-frame b_g channels are absent",
            "if_unsigned": "runner needs a disformal projection extension",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG624_5_gauge_classification",
            "signature_clause": "local Lorentz/tetrad gauge is separated from physical Weyl/disformal frame changes",
            "required_source": "matter gauge invariance and parent frame taxonomy",
            "current_status": "classification_rule_written_not_parent_signed",
            "if_signed": "pure tetrad rotations do not pollute b_g",
            "if_unsigned": "b_g runner must keep gauge/physical distinction explicit",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG624_6_species_universal_geometry",
            "signature_clause": "ordinary species either share the same E(q) or any E_A(q) differences are Q-only and X-blind",
            "required_source": "parent matter universality/representation theorem",
            "current_status": "not_signed",
            "if_signed": "species-dependent Q-only frames do not source b_g along v_X",
            "if_unsigned": "species-frame differences route into b_theta/b_kappa or a species geometry prior",
            "blocks_bg_zero": "false_for_vertical_bg_but_blocks_single_frame_claim",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG624_7_signature_verdict",
            "signature_clause": "SIG624_0..SIG624_5 jointly sign observed coframe factorization",
            "required_source": "full parent matter-sector action",
            "current_status": "not_signed",
            "if_signed": "b_g=0 for ordinary matter geometry coupling",
            "if_unsigned": "b_g runner remains active and all local arena claims stay blocked",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
    ]


def build_bg_runner_schema_rows() -> list[dict[str, object]]:
    return [
        {
            "field": "mode_id",
            "required": "true",
            "allowed_or_expected": "conformal_common,disformal_common,gauge_lorentz,Q_only_frame,marker_mixed",
            "claim_rule": "mode selects projection formula and zero/bound requirements",
        },
        {
            "field": "coefficient",
            "required": "true",
            "allowed_or_expected": "c_g,d_g,0,MISSING_PARENT_INPUT",
            "claim_rule": "claim-ready only when coefficient is zero-derived or numerically sourced",
        },
        {
            "field": "projection",
            "required": "true",
            "allowed_or_expected": "tau_g,Pi_disformal,0,MISSING_ARENA_PROJECTION",
            "claim_rule": "arena projection must be known before scoring",
        },
        {
            "field": "b_g_effective",
            "required": "true",
            "allowed_or_expected": "coefficient times projection, or zero for signed factorization/gauge",
            "claim_rule": "cannot be evaluated with MISSING markers",
        },
        {
            "field": "source_path",
            "required": "true",
            "allowed_or_expected": "local theorem path, local data path, or MISSING_PARENT_SOURCE",
            "claim_rule": "source path must exist for any claim-ready row",
        },
        {
            "field": "valid_for_claim",
            "required": "true",
            "allowed_or_expected": "false until coefficient, projection, and source gate pass",
            "claim_rule": "smoke rows never self-promote",
        },
    ]


def build_bg_smoke_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": "BGR624_0_conformal_common",
            "mode_id": "conformal_common",
            "coefficient": "MISSING_PARENT_INPUT",
            "projection": "MISSING_ARENA_PROJECTION",
            "b_g_effective": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "runner_result": "blocked_missing_parent_input",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BGR624_1_disformal_common",
            "mode_id": "disformal_common",
            "coefficient": "MISSING_PARENT_INPUT",
            "projection": "MISSING_ARENA_PROJECTION",
            "b_g_effective": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "runner_result": "blocked_missing_parent_input",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BGR624_2_gauge_lorentz",
            "mode_id": "gauge_lorentz",
            "coefficient": "0",
            "projection": "0",
            "b_g_effective": "0",
            "source_path": "MISSING_PARENT_SOURCE",
            "runner_result": "blocked_until_gauge_invariance_source_signed",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BGR624_3_Q_only_frame",
            "mode_id": "Q_only_frame",
            "coefficient": "0_along_vX_if_factorization_signed",
            "projection": "not_needed_for_vertical_bg",
            "b_g_effective": "0_conditional",
            "source_path": "MISSING_PARENT_SOURCE",
            "runner_result": "blocked_until_factorization_source_signed",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BGR624_4_marker_mixed",
            "mode_id": "marker_mixed",
            "coefficient": "MISSING_PARENT_INPUT",
            "projection": "MISSING_ARENA_PROJECTION",
            "b_g_effective": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "runner_result": "blocked_marker_and_geometry_mixed",
            "valid_for_claim": "false",
        },
    ]


def build_arena_runner_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "AGR624_0_R10",
            "arena": "R10 inverse-square",
            "bg_inputs_needed": "mode_id, coefficient, projection, K_X, Qbar_XH, lambda_X, bound_curve",
            "runner_status": "blocked",
            "block_reason": "b_g_effective and R10 kernel inputs contain MISSING markers",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AGR624_1_PPN",
            "arena": "PPN/local gravity",
            "bg_inputs_needed": "coefficient, range/profile suppression, PPN projection matrix",
            "runner_status": "blocked",
            "block_reason": "common-frame coefficient and projection are not sourced",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AGR624_2_clock_redshift",
            "arena": "clock/redshift",
            "bg_inputs_needed": "coefficient, environment profile, clock sensitivity to common frame",
            "runner_status": "blocked",
            "block_reason": "environment and coefficient priors are placeholders",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AGR624_3_orbital",
            "arena": "orbital/binary",
            "bg_inputs_needed": "coefficient, lambda_X, source profile, orbital projection",
            "runner_status": "blocked",
            "block_reason": "range/profile and b_g coefficient are placeholders",
            "claim_allowed": "false",
        },
    ]


def build_repair_target_rows() -> list[dict[str, object]]:
    return [
        {
            "target_id": "RT624_0_no_representative_Weyl",
            "repair_target": "prove no A_g(X)^2 representative Weyl factor can appear in ordinary matter geometry",
            "why_first": "pure conformal common-frame coupling is the simplest b_g leakage and touches all local gravity arenas",
            "success_output": "c_g=0 theorem row",
            "failure_output": "numeric/symbolic c_g prior remains",
            "next_target": NEXT_TARGET,
        },
        {
            "target_id": "RT624_1_no_representative_disformal",
            "repair_target": "prove no B_g(X) disformal/tensor representative geometry appears",
            "why_first": "needed after Weyl if conformal channel closes",
            "success_output": "disformal projection row zero",
            "failure_output": "disformal prior schema extension",
            "next_target": "after_Weyl_gate_if_needed",
        },
        {
            "target_id": "RT624_2_gauge_source",
            "repair_target": "source local Lorentz gauge invariance row",
            "why_first": "prevents pure tetrad rotations from being miscounted as physical b_g",
            "success_output": "gauge_lorentz runner row can be claim-safe as zero within branch",
            "failure_output": "keep gauge row nonclaim",
            "next_target": "parallel_supporting_gate",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D624_0_main_verdict",
            "status": STATUS,
            "decision": "observed coframe factorization parent signature not signed",
            "meaning": "the 623 lemma remains conditional; b_g cannot be zeroed from the current parent corpus",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D624_1_bg_runner",
            "status": "bg_runner_blocks_all_smoke_rows",
            "decision": "create b_g runner with conformal, disformal, gauge, Q-only, and marker-mixed modes",
            "meaning": "the geometry prior is now executable bookkeeping rather than prose",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D624_2_best_next_derivation",
            "status": "no_representative_Weyl_first",
            "decision": "attack representative Weyl coupling before broader local claims",
            "meaning": "killing c_g is the fastest way to shrink R10/PPN/clock/orbital exposure",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D624_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no b_g/R10/WEP/PPN/local-GR pass",
            "meaning": "all signature and runner rows are nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU624_0_allowed",
            "allowed_after_624": "use the signature audit as the required checklist for b_g=0",
            "forbidden_after_624": "promote b_g=0 without SIG624_0..SIG624_5",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU624_1_allowed",
            "allowed_after_624": "use b_g runner rows to block/scaffold future scoring",
            "forbidden_after_624": "score R10/PPN/clocks/orbits while runner rows contain MISSING markers",
            "next_action": "derive or source c_g first",
        },
        {
            "route_id": "RU624_2_allowed",
            "allowed_after_624": "target no-representative-Weyl theorem first",
            "forbidden_after_624": "jump to total local-GR recovery before c_g channel is resolved",
            "next_action": NEXT_TARGET,
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "signature_audit_written": "true",
            "parent_factorization_signed": "false",
            "bg_runner_written": "true",
            "bg_runner_blocks_claims": "true",
            "b_g_zero_promoted": "false",
            "c_g_zero_promoted": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    repair_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_623_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]

    required_signature_ids = {
        "SIG624_0_parent_quotient",
        "SIG624_1_local_X_verticality",
        "SIG624_2_matter_geometry_factorization",
        "SIG624_3_no_representative_Weyl",
        "SIG624_4_no_representative_disformal",
        "SIG624_5_gauge_classification",
        "SIG624_7_signature_verdict",
    }
    signature_ids = {row["signature_id"] for row in signature_rows}
    signature_complete = required_signature_ids.issubset(signature_ids)
    signature_not_signed = any(row["signature_id"] == "SIG624_7_signature_verdict" and row["current_status"] == "not_signed" for row in signature_rows)
    schema_complete = {"mode_id", "coefficient", "projection", "b_g_effective", "source_path", "valid_for_claim"}.issubset({row["field"] for row in schema_rows})
    smoke_nonclaim = all(not parse_bool(row["valid_for_claim"]) for row in smoke_rows)
    smoke_blocks = any(row["runner_result"].startswith("blocked") for row in smoke_rows) and any(has_missing_marker(row) for row in smoke_rows)
    arena_blocks = all(row["runner_status"] == "blocked" and row["claim_allowed"] == "false" for row in arena_rows)
    repair_next = any(row["target_id"] == "RT624_0_no_representative_Weyl" and row["next_target"] == NEXT_TARGET for row in repair_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in signature_rows + smoke_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V624_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V624_1_prior_623_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V624_2_signature_complete_not_signed",
            "result": "pass" if signature_complete and signature_not_signed else "fail",
            "detail": f"signature_complete={signature_complete};signature_not_signed={signature_not_signed}",
        },
        {
            "check_id": "V624_3_bg_runner_schema_complete",
            "result": "pass" if schema_complete else "fail",
            "detail": f"schema_complete={schema_complete}",
        },
        {
            "check_id": "V624_4_smoke_rows_block_nonclaim",
            "result": "pass" if smoke_nonclaim and smoke_blocks else "fail",
            "detail": f"smoke_nonclaim={smoke_nonclaim};smoke_blocks={smoke_blocks}",
        },
        {
            "check_id": "V624_5_arenas_blocked",
            "result": "pass" if arena_blocks else "fail",
            "detail": f"arena_rows={len(arena_rows)};arena_blocks={arena_blocks}",
        },
        {
            "check_id": "V624_6_repair_next_target_set",
            "result": "pass" if repair_next else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V624_7_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V624_8_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["b_g_zero_promoted"] == "false"
            else "fail",
            "detail": "b_g_zero=false;R10=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    source_register: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    repair_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 624 Y5 R10 observed coframe factorization parent signature or bg runner

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- 624 asks the exact parent-signature question for the 623 factorization lemma.
- Current result: the signature is not closed. The parent has not yet signed quotient ownership, local `X` verticality, all-species matter geometry factorization, no representative Weyl/disformal frame, or full gauge/physical-frame classification.
- Therefore `b_g=0` is still not promoted.
- The useful output is the first `b_g` runner: conformal, disformal, gauge, Q-only, and marker-mixed geometry modes are separated, and every local arena remains blocked while the rows contain `MISSING_PARENT_INPUT` or `MISSING_ARENA_PROJECTION`.

## Signature Target
The zero route is:

```text
q: Phi_parent -> Q_MTS
dq(v_X)=0
for all ordinary matter species A: e_A(Phi)=E_A(q(Phi))
no representative Weyl/disformal frame before q
```

Then:

```text
Lie_vX e_A = 0
b_g = 0
```

The current corpus has the conditional math, not the parent signature.

## Source Register
{md_table(source_register)}

## Parent Signature Audit
{md_table(signature_rows)}

## b_g Runner Schema
{md_table(schema_rows)}

## b_g Smoke Rows
{md_table(smoke_rows)}

## Arena Runner Status
{md_table(arena_rows)}

## Repair Targets
{md_table(repair_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This checkpoint does not win the local-GR round, but it keeps our guard up. The geometry problem is now split into concrete mode rows. The best next derivation is the simplest dangerous one: prove there is no representative-dependent Weyl factor `A_g(X)^2` in ordinary matter geometry, or admit `c_g=d ln A_g/dXhat` as the first real common-frame prior.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    signature_rows = build_signature_rows()
    schema_rows = build_bg_runner_schema_rows()
    smoke_rows = build_bg_smoke_rows()
    arena_rows = build_arena_runner_rows()
    repair_rows = build_repair_target_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        signature_rows,
        schema_rows,
        smoke_rows,
        arena_rows,
        repair_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_624_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_624_PARENT_SIGNATURE_AUDIT.csv", signature_rows),
        ("P8_Y5_R10_624_BG_RUNNER_SCHEMA.csv", schema_rows),
        ("P8_Y5_R10_624_BG_SMOKE_ROWS.csv", smoke_rows),
        ("P8_Y5_R10_624_ARENA_RUNNER_STATUS.csv", arena_rows),
        ("P8_Y5_R10_624_REPAIR_TARGETS.csv", repair_rows),
        ("P8_Y5_BRR545_624_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_624_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_624_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_624_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        signature_rows,
        schema_rows,
        smoke_rows,
        arena_rows,
        repair_rows,
        decision_rows,
        route_rows,
        nonclaim_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
