from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md"
SCRIPT_REL = "scripts/Y5_R10_quotient_invariant_matter_action_signature_or_cg_bound_input.py"
STATUS = "Y5_R10_quotient_invariant_matter_action_signature_not_signed_cg_bound_input_blocks_claims"
CLAIM_CEILING = "private_quotient_matter_signature_and_cg_bound_schema_only_no_cg_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md"


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
        ("625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md", "immediate handoff: c_g prior retained"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_625_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_625_WEYL_DISFORMAL_EXCLUSION_ATTEMPT.csv", "representative frame exclusion attempt"),
        ("source-intake/mts_residuals/P8_Y5_R10_625_CG_PRIOR_TEMPLATE.csv", "c_g prior template"),
        ("source-intake/mts_residuals/P8_Y5_R10_625_DISFORMAL_PRIOR_TEMPLATE.csv", "disformal prior template"),
        ("source-intake/mts_residuals/P8_Y5_R10_625_ARENA_BLOCKS.csv", "local arena blockers"),
        ("624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md", "b_g runner"),
        ("623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md", "coframe factorization lemma"),
        ("622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md", "parent matter contract"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "coframe pullback theorem"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor attempt"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "no-extension loophole audit"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_signature_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "QIM626_0_descent_equivalence",
            "target": "matter action descends to Q_MTS",
            "mathematical_statement": "S_matter descends to Sbar_matter on Q_MTS iff Lie_v S_matter=0 for every vertical v in ker(Dq), up to owned gauge/boundary terms.",
            "proof_status": "valid_conditional_descent_criterion",
            "parent_status": "not_signed",
            "if_signed": "representative Weyl/disformal frame factors with nonzero vertical derivative are forbidden",
            "if_unsigned": "c_g and disformal priors remain active",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "QIM626_1_parent_matter_domain",
            "target": "ordinary matter variables and their vertical transformation law are specified",
            "mathematical_statement": "For vertical v_X, either Psi is fixed and only Phi changes, or a lifted vertical action on Psi is specified and leaves observables invariant.",
            "proof_status": "signature_clause_identified",
            "parent_status": "not_signed",
            "if_signed": "vertical derivative test is well-defined",
            "if_unsigned": "cannot evaluate quotient invariance of S_matter",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "QIM626_2_measure_and_connection_descent",
            "target": "matter volume form, coframe, connection, and derivative operator descend to Q_MTS",
            "mathematical_statement": "det(e_m), e_m, omega[e_m], and D[e_m] must be functions of q(Phi) rather than representative fibre data.",
            "proof_status": "signature_clause_identified",
            "parent_status": "not_signed",
            "if_signed": "representative common-frame metric contribution is excluded",
            "if_unsigned": "A_g(X) can still enter through measure or connection",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "QIM626_3_no_representative_coefficients",
            "target": "matter coefficients contain no representative X labels",
            "mathematical_statement": "theta_A, frame factors, and source couplings must be Q_MTS data, representation data, or retained fields; not unvaried fibre functions.",
            "proof_status": "signature_clause_identified",
            "parent_status": "not_signed",
            "if_signed": "fixed c_g spurion is excluded",
            "if_unsigned": "constant and frame priors remain mixed",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "QIM626_4_boundary_terms",
            "target": "vertical variation produces no local/boundary source remnant",
            "mathematical_statement": "Lie_v S_matter may vanish only up to boundary/exact terms if those terms have zero local projection and zero relevant flux.",
            "proof_status": "signature_clause_identified",
            "parent_status": "not_signed",
            "if_signed": "descent criterion is not spoiled by edge current",
            "if_unsigned": "boundary/non-Hilbert residual remains open",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "QIM626_5_signature_verdict",
            "target": "sign quotient-invariant matter action",
            "mathematical_statement": "QIM626_0..QIM626_4 jointly sign S_matter=Sbar_matter[q(Phi),Psi,theta] and c_g=0 for representative Weyl frames.",
            "proof_status": "not_closed",
            "parent_status": "not_signed",
            "if_signed": "c_g zero certificate can be written",
            "if_unsigned": "c_g bound input is required before local scoring",
            "promote_cg_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def build_signature_ledger_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "QMS626_0_q_object",
            "signature_clause": "q:Phi_parent -> Q_MTS is defined before matter coupling",
            "current_status": "contract_only",
            "required_source": "parent quotient construction",
            "blocks": "descent criterion",
            "next_action": "source parent q map or keep closure-only",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "QMS626_1_vertical_kernel",
            "signature_clause": "v_X belongs to ker(Dq) on the local matter branch",
            "current_status": "conditional_not_signed",
            "required_source": "local branch parent theorem",
            "blocks": "representative-frame exclusion",
            "next_action": "prove local X verticality or retain c_g",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "QMS626_2_matter_descent",
            "signature_clause": "S_matter = Sbar_matter[q(Phi),Psi,theta]",
            "current_status": "not_signed",
            "required_source": "parent matter action",
            "blocks": "c_g zero",
            "next_action": "derive matter descent or use c_g bound inputs",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "QMS626_3_no_fixed_representative_frame",
            "signature_clause": "no fixed A_g(X), B_g(X), U_a(X) enters matter geometry",
            "current_status": "not_signed",
            "required_source": "no representative frame theorem",
            "blocks": "Weyl/disformal zero",
            "next_action": "classify as absent/gauge/auxiliary/retained or prior",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "QMS626_4_boundary_projection",
            "signature_clause": "vertical boundary/exact terms have zero local projection",
            "current_status": "not_signed",
            "required_source": "boundary/current certificate",
            "blocks": "clean local matter zero",
            "next_action": "route edge term to non-Hilbert residual if unsigned",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "QMS626_5_total_signature",
            "signature_clause": "all quotient-invariant matter clauses signed",
            "current_status": "not_signed",
            "required_source": "full parent matter action",
            "blocks": "local geometry zero claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_cg_bound_input_rows() -> list[dict[str, object]]:
    return [
        {
            "input_id": "CGB626_0_zero_certificate",
            "parameter": "Z_cg",
            "definition": "Z_cg=true iff quotient-invariant matter action is parent-signed",
            "units": "boolean",
            "value": "false",
            "source_path": "this_checkpoint",
            "status": "not_signed",
            "claim_gate": "blocks_cg_zero",
            "valid_for_claim": "false",
        },
        {
            "input_id": "CGB626_1_cg_value",
            "parameter": "c_g",
            "definition": "c_g=d ln A_g/dXhat for representative Weyl common frame",
            "units": "dimensionless",
            "value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "status": "required_for_bound_if_not_zero",
            "claim_gate": "blocks_all_local_scoring_until_numeric_or_zero",
            "valid_for_claim": "false",
        },
        {
            "input_id": "CGB626_2_tau_R10",
            "parameter": "tau_R10",
            "definition": "R10 material/source-test projection of stress trace/common-frame response",
            "units": "dimensionless",
            "value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "status": "required_for_R10_bound",
            "claim_gate": "blocks_R10",
            "valid_for_claim": "false",
        },
        {
            "input_id": "CGB626_3_tau_PPN",
            "parameter": "tau_PPN",
            "definition": "PPN/local-gravity projection of common-frame response",
            "units": "dimensionless",
            "value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "status": "required_for_PPN_bound",
            "claim_gate": "blocks_PPN",
            "valid_for_claim": "false",
        },
        {
            "input_id": "CGB626_4_tau_clock",
            "parameter": "tau_clock",
            "definition": "clock/redshift/environment projection of common-frame response",
            "units": "dimensionless",
            "value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "status": "required_for_clock_bound",
            "claim_gate": "blocks_clock_scoring",
            "valid_for_claim": "false",
        },
        {
            "input_id": "CGB626_5_tau_orbital",
            "parameter": "tau_orbital",
            "definition": "orbital/binary projection of common-frame response",
            "units": "dimensionless",
            "value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "status": "required_for_orbital_bound",
            "claim_gate": "blocks_orbital_scoring",
            "valid_for_claim": "false",
        },
        {
            "input_id": "CGB626_6_disformal_bound_stub",
            "parameter": "d_g_Pi_disformal",
            "definition": "combined representative disformal coefficient and arena projection, pending fuller schema",
            "units": "dimensionless_after_schema_fix",
            "value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "status": "stub_blocks_disformal_scoring",
            "claim_gate": "blocks_disformal_claims",
            "valid_for_claim": "false",
        },
    ]


def build_arena_equation_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "CGE626_0_R10",
            "equation": "b_g_R10 = tau_R10*c_g; alpha_bg(lambda)=K_X(lambda)*Qbar_XH*b_g_R10",
            "inputs_required": "c_g,tau_R10,K_X,Qbar_XH,lambda_X,alpha_bound(lambda)",
            "claim_status": "blocked_missing_inputs",
            "failure_mode": "cannot compare alpha_bg to R10 bound",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "CGE626_1_PPN",
            "equation": "r_PPN_bg = M_PPN(lambda_X,profile)*tau_PPN*c_g",
            "inputs_required": "c_g,tau_PPN,lambda_X,profile,M_PPN",
            "claim_status": "blocked_missing_inputs",
            "failure_mode": "cannot claim PPN/local-GR recovery",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "CGE626_2_clock",
            "equation": "r_clock_bg = S_clock(environment)*tau_clock*c_g",
            "inputs_required": "c_g,tau_clock,environment_profile,clock_sensitivity",
            "claim_status": "blocked_missing_inputs",
            "failure_mode": "cannot score clock/redshift branch",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "CGE626_3_orbital",
            "equation": "r_orbital_bg = M_orbital(lambda_X,source_profile)*tau_orbital*c_g",
            "inputs_required": "c_g,tau_orbital,lambda_X,source_profile,orbital_projection",
            "claim_status": "blocked_missing_inputs",
            "failure_mode": "cannot score orbital/binary branch",
            "valid_for_claim": "false",
        },
    ]


def build_smoke_rows(cg_inputs: list[dict[str, object]], arena_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in cg_inputs:
        missing = has_missing_marker(row)
        rows.append(
            {
                "smoke_id": "SMK_" + str(row["input_id"]),
                "object_type": "input",
                "object_id": row["input_id"],
                "missing_marker_present": str(missing).lower(),
                "runner_result": "blocked_missing_input" if missing else "nonclaim_zero_certificate_or_stub",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    for row in arena_rows:
        rows.append(
            {
                "smoke_id": "SMK_" + str(row["arena_id"]),
                "object_type": "arena_equation",
                "object_id": row["arena_id"],
                "missing_marker_present": "true",
                "runner_result": row["claim_status"],
                "claim_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D626_0_main_verdict",
            "status": STATUS,
            "decision": "quotient-invariant matter action signature not signed",
            "meaning": "the descent criterion is written, but current parent action does not yet prove S_matter descends to Q_MTS",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D626_1_cg_bound_input",
            "status": "cg_bound_input_schema_written",
            "decision": "create c_g bound input rows for R10, PPN, clocks, and orbital arenas",
            "meaning": "if c_g cannot be zero-derived, it must be numerically sourced before scoring",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D626_2_next_route",
            "status": "source_or_zero_cg_next",
            "decision": "next target is either acquire/source c_g bound inputs or prove local geometry zero",
            "meaning": "this is the first point where data-facing local scoring can be prepared, but not claimed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D626_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no c_g/R10/WEP/PPN/local-GR pass",
            "meaning": "all local arena rows remain blocked by MISSING_PARENT_INPUT or MISSING_ARENA_PROJECTION",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU626_0_allowed",
            "allowed_after_626": "cite descent criterion as the parent signature target",
            "forbidden_after_626": "claim S_matter descends to Q_MTS from current corpus",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU626_1_allowed",
            "allowed_after_626": "prepare c_g bound rows with explicit missing-input blockers",
            "forbidden_after_626": "score R10/PPN/clocks/orbits before c_g and tau_A are sourced",
            "next_action": "source c_g/tau_A or prove Z_cg=true",
        },
        {
            "route_id": "RU626_2_allowed",
            "allowed_after_626": "keep disformal channel as separate blocked stub",
            "forbidden_after_626": "hide disformal leakage inside conformal c_g",
            "next_action": "expand disformal schema only if needed after c_g",
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "descent_criterion_written": "true",
            "quotient_invariant_matter_action_signed": "false",
            "c_g_zero_promoted": "false",
            "c_g_bound_inputs_written": "true",
            "bound_inputs_sourced": "false",
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
    ledger_rows: list[dict[str, object]],
    cg_inputs: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_625_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]
    descent_present = any(row["attempt_id"] == "QIM626_0_descent_equivalence" for row in signature_rows)
    no_cg_zero = all(not parse_bool(row["promote_cg_zero"]) for row in signature_rows)
    signature_not_signed = any(row["clause_id"] == "QMS626_5_total_signature" and row["current_status"] == "not_signed" for row in ledger_rows)
    cg_input_params = {row["parameter"] for row in cg_inputs}
    required_params = {"Z_cg", "c_g", "tau_R10", "tau_PPN", "tau_clock", "tau_orbital", "d_g_Pi_disformal"}
    cg_inputs_safe = required_params.issubset(cg_input_params) and all(not parse_bool(row["valid_for_claim"]) for row in cg_inputs) and any(has_missing_marker(row) for row in cg_inputs)
    arenas_blocked = all(row["claim_status"] == "blocked_missing_inputs" and row["valid_for_claim"] == "false" for row in arena_rows)
    smoke_blocks = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in smoke_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in signature_rows + ledger_rows + cg_inputs + arena_rows + smoke_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V626_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V626_1_prior_625_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V626_2_descent_criterion_present",
            "result": "pass" if descent_present else "fail",
            "detail": "S_matter descends iff vertical derivatives vanish up to owned gauge/boundary terms",
        },
        {
            "check_id": "V626_3_no_cg_zero_promotion",
            "result": "pass" if no_cg_zero and signature_not_signed else "fail",
            "detail": f"no_cg_zero={no_cg_zero};signature_not_signed={signature_not_signed}",
        },
        {
            "check_id": "V626_4_cg_bound_inputs_safe",
            "result": "pass" if cg_inputs_safe else "fail",
            "detail": f"params={','.join(sorted(cg_input_params))};safe={cg_inputs_safe}",
        },
        {
            "check_id": "V626_5_arena_equations_blocked",
            "result": "pass" if arenas_blocked else "fail",
            "detail": f"arena_rows={len(arena_rows)};blocked={arenas_blocked}",
        },
        {
            "check_id": "V626_6_smoke_blocks_claims",
            "result": "pass" if smoke_blocks else "fail",
            "detail": f"smoke_rows={len(smoke_rows)};blocks={smoke_blocks}",
        },
        {
            "check_id": "V626_7_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V626_8_no_local_claim",
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
    signature_rows: list[dict[str, object]],
    ledger_rows: list[dict[str, object]],
    cg_inputs: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 626 Y5 R10 quotient invariant matter action signature or cg bound input

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- 626 attacks the parent premise that would kill `c_g`: ordinary matter must descend to the quotient `Q_MTS`.
- The descent criterion is clean: `S_matter` is quotient-invariant iff every vertical representative variation has zero matter-action variation, up to owned gauge/boundary terms.
- Current result: the signature is not parent-signed. We still lack the parent matter action, vertical matter-domain rule, measure/connection descent, no representative coefficients, and boundary projection certificate.
- Therefore `c_g=0` is not promoted. Instead, 626 writes the bound-input schema needed before R10/PPN/clock/orbital scoring can even begin.

## Descent Criterion

```text
q: Phi_parent -> Q_MTS
v in ker(Dq)
S_matter[Phi,Psi] = Sbar_matter[q(Phi),Psi,theta]
```

implies:

```text
Lie_v S_matter = 0
```

and forbids a representative Weyl frame:

```text
hat_g_ab = A_g(X)^2 g_ab
c_g = d ln A_g/dXhat != 0
```

inside the parent-signed ordinary matter branch. Without the signed descent, `c_g` must be bounded or left blocked.

## Source Register
{md_table(source_register)}

## Quotient-Invariant Signature Attempt
{md_table(signature_rows)}

## Signature Ledger
{md_table(ledger_rows)}

## c_g Bound Input Template
{md_table(cg_inputs)}

## Arena Bound Equations
{md_table(arena_rows)}

## Smoke Results
{md_table(smoke_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is the exact fork we wanted. If the parent action signs matter descent to `Q_MTS`, the representative Weyl channel dies cleanly. If it cannot, then `c_g`, `tau_R10`, `tau_PPN`, `tau_clock`, and `tau_orbital` are the first bound inputs needed before local testing. No placeholders get to cosplay as GR recovery.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    signature_rows = build_signature_attempt_rows()
    ledger_rows = build_signature_ledger_rows()
    cg_inputs = build_cg_bound_input_rows()
    arena_rows = build_arena_equation_rows()
    smoke_rows = build_smoke_rows(cg_inputs, arena_rows)
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        signature_rows,
        ledger_rows,
        cg_inputs,
        arena_rows,
        smoke_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_626_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv", signature_rows),
        ("P8_Y5_R10_626_SIGNATURE_LEDGER.csv", ledger_rows),
        ("P8_Y5_R10_626_CG_BOUND_INPUT_TEMPLATE.csv", cg_inputs),
        ("P8_Y5_R10_626_ARENA_BOUND_EQUATIONS.csv", arena_rows),
        ("P8_Y5_R10_626_SMOKE_RESULTS.csv", smoke_rows),
        ("P8_Y5_BRR545_626_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_626_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_626_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_626_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        signature_rows,
        ledger_rows,
        cg_inputs,
        arena_rows,
        smoke_rows,
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
