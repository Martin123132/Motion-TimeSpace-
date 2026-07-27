from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md"
SCRIPT_REL = "scripts/Y5_R10_no_representative_Weyl_disformal_coupling_or_cg_prior.py"
STATUS = "Y5_R10_no_representative_Weyl_disformal_exclusion_conditional_only_cg_prior_retained"
CLAIM_CEILING = "private_representative_frame_gate_only_no_cg_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md"


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
        ("624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md", "immediate handoff: no representative Weyl/disformal first"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_624_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_624_PARENT_SIGNATURE_AUDIT.csv", "parent signature audit"),
        ("source-intake/mts_residuals/P8_Y5_R10_624_BG_SMOKE_ROWS.csv", "b_g smoke runner rows"),
        ("source-intake/mts_residuals/P8_Y5_R10_624_REPAIR_TARGETS.csv", "repair target selection"),
        ("623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md", "factorization lemma and c_g prior"),
        ("source-intake/mts_residuals/P8_Y5_R10_623_BG_PRIOR_FILL.csv", "b_g/c_g prior template"),
        ("622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md", "parent matter-sector contract"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "conditional coframe pullback theorem"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor attempt"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "no-extension loophole audit"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_exclusion_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "NWD625_0_quotient_invariance_lemma",
            "target": "exclude representative-dependent Weyl/disformal geometry",
            "mathematical_statement": "If S_matter is a well-defined function on Q_MTS, then replacing Phi by another representative in the same fibre cannot change e_matter; therefore A_g(X) or B_g(X) with Lie_vX != 0 is forbidden.",
            "proof_status": "valid_conditional_lemma",
            "parent_status": "quotient_invariant_matter_action_not_signed",
            "if_parent_signed": "c_g=0 and representative disformal coefficients vanish",
            "if_not_signed": "representative frame priors remain active",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NWD625_1_fixed_representative_Weyl",
            "target": "exclude fixed A_g(X)^2 matter frame",
            "mathematical_statement": "hat_g_ab=A_g(X)^2 g_ab is not quotient-invariant if X is fibre data and d ln A_g/dXhat != 0.",
            "proof_status": "excluded_only_under_strict_quotient_matter_contract",
            "parent_status": "strict_contract_not_signed",
            "if_parent_signed": "fixed representative Weyl spurion is forbidden",
            "if_not_signed": "c_g=d ln A_g/dXhat is a prior",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NWD625_2_dynamical_Weyl_scalar",
            "target": "classify varied A_g as physical field rather than hidden representative factor",
            "mathematical_statement": "If A_g is varied/propagating, it is not a disposable representative spurion; it is a retained scalar/conformal mode with its own equation and residual channel.",
            "proof_status": "classification_rule",
            "parent_status": "field_taxonomy_not_signed",
            "if_parent_signed": "route to retained field branch or prove auxiliary/gauge",
            "if_not_signed": "do not zero c_g; retain scalar-frame prior",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NWD625_3_Q_only_Weyl_factor",
            "target": "separate Q-only conformal frame from representative Weyl leakage",
            "mathematical_statement": "If A_g=A(Q_MTS), then Lie_vX A_g=0 even if A_g is not constant on Q_MTS.",
            "proof_status": "valid_conditional_clarification",
            "parent_status": "allowed_if_factorization_signed",
            "if_parent_signed": "no b_g source along v_X; interpretation may still require frame convention",
            "if_not_signed": "does not exclude representative A_g(X)",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NWD625_4_representative_disformal",
            "target": "exclude representative-dependent disformal geometry",
            "mathematical_statement": "hat_g_ab=A(Q)^2 g_ab + B_g(X) U_a U_b is not quotient-invariant if B_g or U_a contain fibre data.",
            "proof_status": "excluded_only_under_strict_quotient_matter_contract",
            "parent_status": "no_vector_tensor_marker_theorem_not_signed",
            "if_parent_signed": "representative disformal coefficients vanish",
            "if_not_signed": "disformal projection prior is required",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NWD625_5_gauge_Lorentz",
            "target": "avoid confusing tetrad gauge with physical Weyl/disformal frame",
            "mathematical_statement": "e'_a=Lambda_a^b e_b with Lambda in local Lorentz gauge gives no physical b_g contribution if matter action is gauge-invariant.",
            "proof_status": "standard_conditional_gauge_rule",
            "parent_status": "source_path_not_signed_in_this_branch",
            "if_parent_signed": "gauge_lorentz runner row can be zero-certified",
            "if_not_signed": "keep gauge row nonclaim but not a physical c_g prior",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NWD625_6_verdict",
            "target": "promote c_g=0",
            "mathematical_statement": "c_g=0 requires parent-signed quotient-invariant matter action or a direct no-Weyl theorem.",
            "proof_status": "not_closed",
            "parent_status": "not_signed",
            "if_parent_signed": "b_g conformal common-frame channel closes",
            "if_not_signed": "c_g prior remains and local arenas stay blocked",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def build_frame_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "RFG625_0_matter_action_on_quotient",
            "gate": "S_matter descends to Q_MTS before ordinary matter coupling",
            "status": "not_parent_signed",
            "kills_if_pass": "all representative-only Weyl/disformal factors",
            "fallback_if_fail": "c_g and disformal priors",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RFG625_1_no_fixed_frame_spurion",
            "gate": "no nondynamical A_g(X), B_g(X), U_a(X) frame objects",
            "status": "not_parent_signed",
            "kills_if_pass": "fixed representative frame leakage",
            "fallback_if_fail": "fixed-spurion prior or closure-only exclusion",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RFG625_2_varied_field_taxonomy",
            "gate": "any A_g/B_g/U_a is absent, gauge, auxiliary, or retained as a field",
            "status": "not_parent_signed",
            "kills_if_pass": "hidden scalar/vector frame cheating",
            "fallback_if_fail": "retained scalar/disformal residual",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RFG625_3_Q_only_frame_allowed",
            "gate": "Q-only frames are vertical-blind but need frame convention for public interpretation",
            "status": "conditional_safe",
            "kills_if_pass": "b_g along v_X for Q-only frames",
            "fallback_if_fail": "not a failure if Q-only; only interpretive convention remains",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RFG625_4_disformal_marker_exclusion",
            "gate": "no representative vector/tensor/material marker enters matter metric",
            "status": "not_parent_signed",
            "kills_if_pass": "disformal b_g leakage",
            "fallback_if_fail": "disformal_projection prior and marker-mixed route",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "RFG625_5_total",
            "gate": "RFG625_0..RFG625_4 all signed",
            "status": "not_passed",
            "kills_if_pass": "c_g and representative disformal priors can be zero-certified",
            "fallback_if_fail": "run c_g/disformal prior branch",
            "valid_for_claim": "false",
        },
    ]


def build_cg_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "prior_id": "CG625_0_conformal_log_derivative",
            "parameter": "c_g",
            "definition": "c_g := d ln A_g/dXhat",
            "mode": "representative_Weyl",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "zero_certificate": "false",
            "runner_status": "blocked_missing_parent_input",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CG625_1_conformal_projection",
            "parameter": "tau_g",
            "definition": "tau_g := arena projection of the stress trace/common-frame response",
            "mode": "arena_projection",
            "units": "dimensionless",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "zero_certificate": "false",
            "runner_status": "blocked_missing_arena_projection",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CG625_2_effective_conformal_bg",
            "parameter": "b_g_conformal",
            "definition": "b_g_conformal := tau_g*c_g",
            "mode": "representative_Weyl",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "zero_certificate": "false",
            "runner_status": "blocked_until_cg_and_tau_g",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CG625_3_zero_certificate",
            "parameter": "Z_cg",
            "definition": "true only if quotient-invariant matter action or no-representative-Weyl theorem is parent-signed",
            "mode": "zero_certificate",
            "units": "boolean",
            "current_value": "false",
            "source_path": "this_checkpoint",
            "zero_certificate": "false",
            "runner_status": "not_signed",
            "valid_for_claim": "false",
        },
    ]


def build_disformal_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "prior_id": "DG625_0_disformal_coefficient",
            "parameter": "d_g",
            "definition": "representative disformal coefficient, e.g. d_g := dB_g/dXhat after normalization",
            "mode": "representative_disformal",
            "units": "dimensionless_after_schema_fix",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "runner_status": "blocked_missing_parent_input",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "DG625_1_disformal_projection",
            "parameter": "Pi_disformal",
            "definition": "arena projection of U_a U_b or tensor-frame response",
            "mode": "arena_projection",
            "units": "dimensionless_or_schema_defined",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "runner_status": "blocked_missing_arena_projection",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "DG625_2_effective_disformal_bg",
            "parameter": "b_g_disformal",
            "definition": "b_g_disformal := Pi_disformal*d_g",
            "mode": "representative_disformal",
            "units": "dimensionless_after_schema_fix",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "runner_status": "blocked_until_dg_and_projection",
            "valid_for_claim": "false",
        },
    ]


def build_arena_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "ARE625_0_R10",
            "arena": "R10 inverse-square",
            "needed_for_scoring": "c_g,tau_g,d_g,Pi_disformal,K_X,Qbar_XH,lambda_X,bound_curve",
            "status": "blocked",
            "reason": "representative-frame coefficients and projections are placeholders",
            "claim_allowed": "false",
        },
        {
            "arena_id": "ARE625_1_PPN",
            "arena": "PPN/local gravity",
            "needed_for_scoring": "c_g or zero certificate; disformal projection; range/profile suppression",
            "status": "blocked",
            "reason": "no c_g zero certificate or numeric coefficient",
            "claim_allowed": "false",
        },
        {
            "arena_id": "ARE625_2_clocks",
            "arena": "clock/redshift",
            "needed_for_scoring": "c_g,tau_g,environment profile,clock sensitivity",
            "status": "blocked",
            "reason": "c_g and arena projection are missing",
            "claim_allowed": "false",
        },
        {
            "arena_id": "ARE625_3_orbital",
            "arena": "orbital/binary",
            "needed_for_scoring": "c_g,d_g,range/profile,orbital projection",
            "status": "blocked",
            "reason": "representative-frame coefficient and range/profile are missing",
            "claim_allowed": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D625_0_main_verdict",
            "status": STATUS,
            "decision": "no-representative Weyl/disformal exclusion remains conditional",
            "meaning": "quotient-invariant matter action would kill representative frame couplings, but it is not parent-signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D625_1_cg_prior",
            "status": "c_g_prior_retained",
            "decision": "retain c_g=d ln A_g/dXhat as the first common-frame prior",
            "meaning": "representative Weyl coupling is the simplest dangerous b_g leakage",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D625_2_disformal",
            "status": "disformal_extension_template_written",
            "decision": "track representative disformal leakage separately from pure conformal c_g",
            "meaning": "disformal channels need their own projection schema before scoring",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D625_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no local claim",
            "meaning": "c_g=0 is not signed and all local arena rows remain blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU625_0_allowed",
            "allowed_after_625": "cite representative-frame exclusion only under quotient-invariant matter action",
            "forbidden_after_625": "claim c_g=0 without parent-signed quotient-invariant matter action",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU625_1_allowed",
            "allowed_after_625": "use c_g and tau_g as blocked prior rows",
            "forbidden_after_625": "score R10/PPN/clocks/orbits while c_g or tau_g has MISSING markers",
            "next_action": "derive quotient-invariant matter action or source c_g bound",
        },
        {
            "route_id": "RU625_2_allowed",
            "allowed_after_625": "keep dynamical Weyl/disformal fields as retained-field residuals, not hidden closures",
            "forbidden_after_625": "zero a varied scalar/vector/tensor frame without gauge/auxiliary proof",
            "next_action": NEXT_TARGET,
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "quotient_invariance_lemma_written": "true",
            "quotient_invariant_matter_action_signed": "false",
            "no_representative_Weyl_signed": "false",
            "no_representative_disformal_signed": "false",
            "c_g_zero_promoted": "false",
            "c_g_prior_retained": "true",
            "disformal_prior_retained": "true",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    exclusion_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    cg_rows: list[dict[str, object]],
    disformal_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_624_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]
    lemma_present = any(row["attempt_id"] == "NWD625_0_quotient_invariance_lemma" for row in exclusion_rows)
    no_cg_zero = all(not parse_bool(row["promote_cg_zero"]) for row in exclusion_rows)
    total_gate = [row for row in gate_rows if row["gate_id"] == "RFG625_5_total"]
    total_gate_blocks = bool(total_gate) and total_gate[0]["status"] == "not_passed"
    cg_safe = all(not parse_bool(row["valid_for_claim"]) for row in cg_rows) and any(has_missing_marker(row) for row in cg_rows)
    disformal_safe = all(not parse_bool(row["valid_for_claim"]) for row in disformal_rows) and any(has_missing_marker(row) for row in disformal_rows)
    arenas_blocked = all(row["status"] == "blocked" and row["claim_allowed"] == "false" for row in arena_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in exclusion_rows + gate_rows + cg_rows + disformal_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V625_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V625_1_prior_624_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V625_2_quotient_invariance_lemma_present",
            "result": "pass" if lemma_present else "fail",
            "detail": "representative frame excluded only if matter action descends to Q_MTS",
        },
        {
            "check_id": "V625_3_no_cg_zero_promotion",
            "result": "pass" if no_cg_zero else "fail",
            "detail": f"no_cg_zero_promoted={no_cg_zero}",
        },
        {
            "check_id": "V625_4_total_gate_blocks",
            "result": "pass" if total_gate_blocks else "fail",
            "detail": f"total_gate_blocks={total_gate_blocks}",
        },
        {
            "check_id": "V625_5_cg_priors_safe",
            "result": "pass" if cg_safe else "fail",
            "detail": f"cg_rows={len(cg_rows)};nonclaim_with_missing={cg_safe}",
        },
        {
            "check_id": "V625_6_disformal_priors_safe",
            "result": "pass" if disformal_safe else "fail",
            "detail": f"disformal_rows={len(disformal_rows)};nonclaim_with_missing={disformal_safe}",
        },
        {
            "check_id": "V625_7_arenas_blocked",
            "result": "pass" if arenas_blocked else "fail",
            "detail": f"arena_rows={len(arena_rows)};arenas_blocked={arenas_blocked}",
        },
        {
            "check_id": "V625_8_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V625_9_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["c_g_zero_promoted"] == "false"
            else "fail",
            "detail": "c_g_zero=false;R10=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    source_register: list[dict[str, object]],
    exclusion_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    cg_rows: list[dict[str, object]],
    disformal_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 625 Y5 R10 no representative Weyl disformal coupling or cg prior

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- I tried to kill the representative Weyl/disformal common-frame channel.
- The clean lemma is real: if the ordinary matter action is a well-defined function on the quotient `Q_MTS`, then representative-dependent frames like `A_g(X)^2 g_ab` or `B_g(X)U_aU_b` are not allowed.
- The current parent action has not signed that quotient-invariant matter-action premise. So `c_g=0` is not promoted.
- Result: `c_g=d ln A_g/dXhat` remains the first common-frame prior, and disformal leakage gets its own extension template instead of being hidden inside `b_g`.

## Conditional Exclusion Lemma

```text
S_matter = Sbar_matter[q(Phi), Psi, theta]
Phi ~ Phi' when q(Phi)=q(Phi')
```

Then:

```text
S_matter[Phi] = S_matter[Phi']
```

so a matter metric containing representative fibre data,

```text
hat_g_ab = A_g(X)^2 g_ab
c_g = d ln A_g/dXhat != 0
```

cannot appear in the parent-signed ordinary matter branch. The same logic applies to representative disformal/tensor factors. But this is only as strong as the parent quotient-invariance premise.

## Source Register
{md_table(source_register)}

## Weyl/Disformal Exclusion Attempt
{md_table(exclusion_rows)}

## Representative Frame Gate
{md_table(gate_rows)}

## c_g Prior Template
{md_table(cg_rows)}

## Disformal Prior Template
{md_table(disformal_rows)}

## Arena Blocks
{md_table(arena_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is another clean narrowing. We now know that the dangerous Weyl/disformal geometry channel is not a mysterious new beast: it is exactly the failure of quotient-invariant matter action. If 626 can sign that parent premise, `c_g` dies. If not, `c_g` must become a sourced prior before any local test is scored.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    exclusion_rows = build_exclusion_attempt_rows()
    gate_rows = build_frame_gate_rows()
    cg_rows = build_cg_prior_rows()
    disformal_rows = build_disformal_prior_rows()
    arena_rows = build_arena_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        exclusion_rows,
        gate_rows,
        cg_rows,
        disformal_rows,
        arena_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_625_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_625_WEYL_DISFORMAL_EXCLUSION_ATTEMPT.csv", exclusion_rows),
        ("P8_Y5_R10_625_REPRESENTATIVE_FRAME_GATE.csv", gate_rows),
        ("P8_Y5_R10_625_CG_PRIOR_TEMPLATE.csv", cg_rows),
        ("P8_Y5_R10_625_DISFORMAL_PRIOR_TEMPLATE.csv", disformal_rows),
        ("P8_Y5_R10_625_ARENA_BLOCKS.csv", arena_rows),
        ("P8_Y5_BRR545_625_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_625_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_625_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_625_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        exclusion_rows,
        gate_rows,
        cg_rows,
        disformal_rows,
        arena_rows,
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
