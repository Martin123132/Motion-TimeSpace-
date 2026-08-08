from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "618-Y5-R10-no-pole-source-zero-certificate-after-finite-branch-demotion.md"
SCRIPT_REL = "scripts/Y5_R10_no_pole_source_zero_certificate_after_finite_branch_demotion.py"
STATUS = "Y5_R10_no_pole_source_zero_certificate_audited_one_direct_X_zero_closed_full_certificate_not_signed"
CLAIM_CEILING = "certificate_audit_and_route_discipline_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "619-Y5-R10-no-marker-minimal-quotient-theorem-or-qbarXT-residual-fill.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


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
        ("617-Y5-R10-field-space-normalization-beta-eigenvalue-owner-or-no-pole-return.md", "617 immediate handoff"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_617_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_617_NO_POLE_RETURN_GATE.csv", "no-pole/source-zero return decision"),
        ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "conditional no-pole theorem"),
        ("source-intake/mts_residuals/P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv", "no-pole certificate obligations"),
        ("582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md", "boundary and Dirac algebra gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv", "no-pole gate status"),
        ("583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md", "momentum-map owner failure and edge demotion"),
        ("590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md", "DCdagger/Omega-flat vertical map"),
        ("596-Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote.md", "quotient pullback lemma"),
        ("source-intake/mts_residuals/P8_Y5_R10_596_QUOTIENT_PULLBACK_LEMMA.csv", "vertical-blind q_loc pullback rows"),
        ("598-Y5-R10-fill-q_loc-residual-runner-or-derive-first-zero-row.md", "first direct-X zero row"),
        ("source-intake/mts_residuals/P8_Y5_R10_598_FIRST_ZERO_ROW_DERIVATION.csv", "closed direct-X smuggling row"),
        ("599-Y5-R10-parent-projector-boundary-zero-or-compact-shell-score.md", "projector/boundary residual status"),
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "matter selector source-zero attempt"),
        ("source-intake/mts_residuals/P8_Y5_R10_613_SELECTOR_CERTIFICATE_TEMPLATE.csv", "qbar_XT selector certificate"),
        ("source-intake/mts_residuals/P8_Y5_R10_617_NONCLAIM_SUMMARY.csv", "finite branch demotion after beta law"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_no_pole_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "NPC618_0_parent_projection",
            "required_clause": "construct pi: Conf_parent -> Q_obs with X vertical before variation",
            "mathematical_form": "d pi(v_X)=0",
            "current_status": "candidate_pi_exists_not_parent_universal",
            "evidence_source": "595/596",
            "certificate_result": "conditional_only",
            "if_missing": "X can remain a physical exchange direction",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "NPC618_1_bulk_action_factorization",
            "required_clause": "bulk action factors through observed quotient or a true gauge constraint",
            "mathematical_form": "S_bulk[Y]=S_red[pi(Y)] or C_X is a parent momentum map",
            "current_status": "not_signed",
            "evidence_source": "581/582/583/590",
            "certificate_result": "fail_current_claim",
            "if_missing": "regular or edge X pole can survive",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "NPC618_2_parent_Omega_DCX_vX",
            "required_clause": "DCdagger X is Omega-flat of a real vertical generator",
            "mathematical_form": "(DC_X)^dagger X = Omega_Y^flat(v_X), v_X=Omega_Y^-1[(DC_X)^dagger X]",
            "current_status": "map_derived_conditionally_parent_Omega_missing",
            "evidence_source": "590/591",
            "certificate_result": "blocked_current_claim",
            "if_missing": "no first-class no-pole bracket credit",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "NPC618_3_constraint_and_boundary",
            "required_clause": "first-class constraint algebra and zero boundary charge",
            "mathematical_form": "{G[epsilon],G[eta]}=G[[epsilon,eta]] and Q_X=K_boundary=0",
            "current_status": "boundary_not_silenced_bracket_not_computed",
            "evidence_source": "582/583",
            "certificate_result": "fail_current_claim",
            "if_missing": "edge hair or second-class remnant routes to finite residual",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "NPC618_4_direct_q_loc_X_smuggling",
            "required_clause": "direct representative-X source cannot enter Gamma/Khat/q_loc if all are Q_obs pullbacks",
            "mathematical_form": "Lie_vX(q_loc)=0",
            "current_status": "closed_under_quotient_contract",
            "evidence_source": "596/598",
            "certificate_result": "partial_zero_row_closed",
            "if_missing": "direct hidden-X source row reopens",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "NPC618_5_exact_q_loc_zero",
            "required_clause": "observed q_loc vanishes by reduced Ward identity",
            "mathematical_form": "q_loc=P_loc nabla_mu T_GK^{mu nu}=0 from reduced on-shell Euler equations and no boundary flux",
            "current_status": "not_derived_observed_residual_open",
            "evidence_source": "596/597/598/599",
            "certificate_result": "fail_current_claim",
            "if_missing": "q_loc remains observed residual, even if vertical-blind",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "NPC618_6_no_pole_promotion",
            "required_clause": "all no-pole clauses pass together",
            "mathematical_form": "NPC618_0..NPC618_5 jointly imply K_X=0 and inactive alpha_X(lambda)",
            "current_status": "not_passed",
            "evidence_source": "this_checkpoint",
            "certificate_result": "no_claim",
            "if_missing": "finite C_X / edge / q_loc residual branches remain live",
            "valid_for_claim": "false",
        },
    ]


def build_source_zero_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "zero_id": "SZ618_0_qbar_XT_chain_rule",
            "target_zero": "qbar_XT=0",
            "mathematical_condition": "S_matter=S_matter[psi,e_obs(Q),omega(Q),theta_A] and Lie_vX(theta_A)=0",
            "current_status": "valid_conditional_theorem_not_parent_signed",
            "evidence_source": "613",
            "result": "not_promoted",
            "counterexample": "universal conformal frame or selector-dependent constants",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "SZ618_1_Qbar_XH_boundary",
            "target_zero": "Qbar_XH=0",
            "mathematical_condition": "boundary charge is zero/exact/proper-gauge and Pi_M^H projects no X edge charge",
            "current_status": "not_derived",
            "evidence_source": "581/582/583/599",
            "result": "not_promoted",
            "counterexample": "vertical edge mode with nonzero Hamiltonian charge",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "SZ618_2_KX_no_green_function",
            "target_zero": "K_X=0",
            "mathematical_condition": "no invertible physical X kinetic operator after first-class quotient and boundary audit",
            "current_status": "conditional_theorem_shape_only",
            "evidence_source": "581/582/590",
            "result": "not_promoted",
            "counterexample": "physical massive X block or second-class remnant",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "SZ618_3_direct_X_to_q_loc",
            "target_zero": "Lie_vX(q_loc)=0",
            "mathematical_condition": "Gamma_eff, K_hat, P_loc, connection, and boundary reference are Q_obs pullbacks",
            "current_status": "closed_under_quotient_contract",
            "evidence_source": "596/598",
            "result": "partial_zero_closed",
            "counterexample": "future symbols depending on representative fibre data reopen the row",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "SZ618_4_observed_q_loc_zero",
            "target_zero": "q_loc=0",
            "mathematical_condition": "reduced GK action, metric response identity, P_loc ownership, and boundary no-flux",
            "current_status": "not_derived",
            "evidence_source": "597/599",
            "result": "not_promoted",
            "counterexample": "nonzero vertical-blind tensor on Q_obs",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "SZ618_5_full_source_zero_certificate",
            "target_zero": "R10 source/test/edge all theorem-zero",
            "mathematical_condition": "qbar_XT=0 or Qbar_XH=0 or K_X=0 with no edge substitute",
            "current_status": "not_passed",
            "evidence_source": "this_checkpoint",
            "result": "finite_branch_retained",
            "counterexample": "any failed zero route keeps alpha=lambda residual row",
            "valid_for_claim": "false",
        },
    ]


def build_finite_branch_rows(summary_617: dict[str, str]) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "FB618_0_finite_branch_after_617",
            "status": "closure_sidecar_retained",
            "reason": "field-space metric and beta eigenvalue not parent-signed",
            "law": summary_617.get("field_space_law", "beta_eff=Upp0*rho_vac^(1/2)/(Z_X*f_X^2)"),
            "pressure_read": "beta3 theorem target remains useful but nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "FB618_1_p1_envelope",
            "status": "active_honest_fallback",
            "reason": "p=2/no-marker norm-square route not parent-owned; p=1 remains legal",
            "law": "alpha_X(lambda)=epsilon_shell*C_X(lambda)",
            "pressure_read": "requires source-backed C_X and lambda before any R10 scoring",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "FB618_2_direct_hidden_X_row",
            "status": "closed_conditional_row",
            "reason": "Q_obs pullback kills direct representative-X smuggling",
            "law": "Lie_vX(q_loc)=0 under pullback assumptions",
            "pressure_read": "shrinks residual runner but does not prove local GR",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "FB618_3_no_marker_repair",
            "status": "best_next_derivation_target",
            "reason": "qbar_XT=0 needs primitive-minimal/no-marker quotient proof",
            "law": "no nontrivial material marker extension or X-dependent constants",
            "pressure_read": "if it fails, fill qbar_XT residual instead of zeroing it",
            "valid_for_claim": "false",
        },
    ]


def build_closed_zero_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": "CZR618_0",
            "closed_zero": "direct representative-X smuggling into Gamma/Khat/q_loc",
            "exact_statement": "If Gamma_eff, K_hat, P_loc, connection, and boundary reference factor through Q_obs, then Lie_vX(q_loc)=0.",
            "scope": "internal quotient-contract zero only",
            "not_closed": "observed q_loc, qbar_XT, Qbar_XH, K_X, boundary edge charge, PPN vector",
            "source": "596/598",
            "valid_for_claim": "false",
        }
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D618_0_main_verdict",
            "status": STATUS,
            "decision": "audit no-pole/source-zero certificate after finite range demotion",
            "meaning": "only the direct representative-X smuggling row is closed; the full no-pole/source-zero certificate is not signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D618_1_no_pole",
            "status": "no_pole_certificate_not_closed",
            "decision": "do not promote K_X=0",
            "meaning": "parent Omega/DC/v_X, first-class bracket closure, and boundary charge zero are still missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D618_2_source_zero",
            "status": "qbar_XT_zero_not_signed",
            "decision": "do not promote qbar_XT=0",
            "meaning": "the chain-rule selector theorem needs primitive-minimal no-marker and constant-triviality clauses",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D618_3_finite_sidecar",
            "status": "finite_p1_and_vacuum_range_sidecar_retained_nonclaim",
            "decision": "keep finite branch as the honest fallback",
            "meaning": "survivability can be pressure-tested later but is not local-GR reduction",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D618_4_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "this is certificate bookkeeping and one conditional zero row only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_update_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU618_0_allowed",
            "allowed_after_618": "cite Lie_vX(q_loc)=0 only under explicit Q_obs pullback assumptions",
            "forbidden_after_618": "call q_loc itself zero or local GR derived",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU618_1_allowed",
            "allowed_after_618": "try primitive-minimal no-marker quotient repair for qbar_XT",
            "forbidden_after_618": "set qbar_XT=0 without no-marker/constant-triviality certificate",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU618_2_allowed",
            "allowed_after_618": "keep finite p1/vacuum-range sidecar as nonclaim pressure route",
            "forbidden_after_618": "treat finite R10 survival as a GR-reduction proof",
            "next_action": "fill_qbarXT_or_edge_residual_if_no_marker_fails",
        },
    ]


def build_summary_rows(summary_617: dict[str, str]) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "direct_X_smuggling_zero_closed": "true",
            "q_loc_zero_promoted": "false",
            "K_X_zero_promoted": "false",
            "qbar_XT_zero_promoted": "false",
            "Qbar_XH_zero_promoted": "false",
            "finite_branch_retained": "true",
            "finite_field_space_law": summary_617.get("field_space_law", "beta_eff=Upp0*rho_vac^(1/2)/(Z_X*f_X^2)"),
            "selected_next_route": "no_marker_minimal_quotient_or_qbarXT_residual_fill",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    no_pole_rows: list[dict[str, object]],
    source_zero_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    closed_zero_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row for row in source_register if not parse_bool(row["exists"])]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    no_claim_rows = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for table in [no_pole_rows, source_zero_rows, finite_rows, closed_zero_rows, decision_rows, summary_rows]
        for row in table
    )
    direct_zero_closed = summary_rows[0]["direct_X_smuggling_zero_closed"] == "true"
    full_no_pole_not_promoted = summary_rows[0]["K_X_zero_promoted"] == "false"
    qbar_not_promoted = summary_rows[0]["qbar_XT_zero_promoted"] == "false"
    finite_retained = summary_rows[0]["finite_branch_retained"] == "true"
    no_marker_next = summary_rows[0]["selected_next_route"] == "no_marker_minimal_quotient_or_qbarXT_residual_fill"
    return [
        {"check_id": "V618_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": f"missing={len(missing_sources)}"},
        {"check_id": "V618_1_prior_617_clean", "result": "pass" if not prior_failures else "fail", "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}"},
        {"check_id": "V618_2_direct_zero_row_retained", "result": "pass" if direct_zero_closed else "fail", "detail": "Lie_vX(q_loc)=0 under pullback contract"},
        {"check_id": "V618_3_no_full_nopole_promotion", "result": "pass" if full_no_pole_not_promoted else "fail", "detail": "K_X=0 not promoted"},
        {"check_id": "V618_4_no_qbarXT_promotion", "result": "pass" if qbar_not_promoted else "fail", "detail": "qbar_XT=0 not parent-signed"},
        {"check_id": "V618_5_finite_branch_retained", "result": "pass" if finite_retained else "fail", "detail": "finite p1/vacuum-range sidecar retained"},
        {"check_id": "V618_6_next_route_set", "result": "pass" if no_marker_next else "fail", "detail": NEXT_TARGET},
        {"check_id": "V618_7_no_claim_rows", "result": "pass" if no_claim_rows else "fail", "detail": f"all_valid_for_claim_false={no_claim_rows}"},
        {"check_id": "V618_8_next_target_set", "result": "pass" if decision_rows[0]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V618_9_no_R10_or_local_GR_claim", "result": "pass", "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false"},
    ]


def write_doc(
    generated: str,
    source_register: list[dict[str, object]],
    no_pole_rows: list[dict[str, object]],
    source_zero_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    closed_zero_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 618 Y5 R10 no-pole source-zero certificate after finite branch demotion

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- After the finite vacuum-range branch was demoted, I re-audited the clean no-pole/source-zero route.
- One real internal zero row survives: under the explicit `Q_obs` pullback contract, `Lie_vX(q_loc)=0`, so direct representative-`X` smuggling through `Gamma_eff/K_hat/q_loc` is closed.
- That is not `q_loc=0`, not `K_X=0`, not `qbar_XT=0`, and not local GR.
- The full no-pole certificate still lacks parent `Omega/DC_X/v_X`, first-class bracket closure, and zero boundary charge.
- The source-zero certificate still lacks primitive-minimal no-marker, constant-triviality, and matter-factorization clauses. Next we attack that exact missing no-marker quotient clause or fill `qbar_XT` as a residual.

## Exact Boundary
Allowed:

```text
Lie_vX(q_loc)=0 under Q_obs pullback assumptions.
```

Forbidden:

```text
q_loc=0
K_X=0
qbar_XT=0
Qbar_XH=0
R10/local-GR pass
```

This keeps the route honest: one boxer is definitely not in the ring, but the observed residuals still need either theorem-zero or scoring.

## Source Register
{md_table(source_register)}

## No-Pole Certificate Audit
{md_table(no_pole_rows)}

## Source-Zero Certificate Audit
{md_table(source_zero_rows)}

## Finite Branch Demotion Status
{md_table(finite_rows)}

## Closed Zero Rows
{md_table(closed_zero_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(summary_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is a useful checkpoint because it stops two mistakes at once. We do not throw away the real conditional zero row, but we also do not let it impersonate full local GR. The next best derivation is narrow: prove a primitive-minimal/no-marker quotient for ordinary matter and constants. If that fails, `qbar_XT` must become a sourced residual row rather than a theorem-zero.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated = utc_now()
    source_register = build_source_register()
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_617_VALIDATION.csv")
    summary_617 = read_csv(OUT / "P8_Y5_R10_617_NONCLAIM_SUMMARY.csv")[0]

    no_pole_rows = build_no_pole_audit_rows()
    source_zero_rows = build_source_zero_audit_rows()
    finite_rows = build_finite_branch_rows(summary_617)
    closed_zero_rows = build_closed_zero_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_update_rows()
    summary_rows = build_summary_rows(summary_617)
    validation_rows = build_validation_rows(
        source_register,
        prior_validation,
        no_pole_rows,
        source_zero_rows,
        finite_rows,
        closed_zero_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(OUT / "P8_Y5_R10_618_SOURCE_REGISTER.csv", source_register)
    write_csv(OUT / "P8_Y5_R10_618_NO_POLE_CERTIFICATE_AUDIT.csv", no_pole_rows)
    write_csv(OUT / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", source_zero_rows)
    write_csv(OUT / "P8_Y5_R10_618_FINITE_BRANCH_DEMOTION_STATUS.csv", finite_rows)
    write_csv(OUT / "P8_Y5_R10_618_CLOSED_ZERO_ROWS.csv", closed_zero_rows)
    write_csv(OUT / "P8_Y5_BRR545_618_DECISION.csv", decision_rows)
    write_csv(OUT / "P8_Y5_BRR545_618_ROUTE_UPDATE.csv", route_rows)
    write_csv(OUT / "P8_Y5_R10_618_NONCLAIM_SUMMARY.csv", summary_rows)
    write_csv(OUT / "P8_Y5_BRR545_618_VALIDATION.csv", validation_rows)

    write_doc(
        generated,
        source_register,
        no_pole_rows,
        source_zero_rows,
        finite_rows,
        closed_zero_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC),
        "validation": rel(OUT / "P8_Y5_BRR545_618_VALIDATION.csv"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
