from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_900_trace_residual_priority_stack_built_combined_zero_theorem_conditional_parent_owner_missing_nonclaim"
CLAIM_CEILING = "priority_and_conditional_zero_theorem_only_no_trace_silence_no_numeric_source_rows_no_R10_PPN_WEP_clock_orbital_or_local_GR_claim"
NEXT_TARGET = "901-Y5-R10-trace-owner-local-rank-zero-certificate-or-finite-carrier-fill.md"

COMBINED_THEOREM = (
    "If ell_tr, K_parent, v_tr, and P_tr are parent-owned; q_loc[U] is a compact local quotient; "
    "rank(P_loc P_tr P_loc^dagger)=0 or Dq_loc[U][v_tr]=0; ordinary matter descends through q_loc with no trace markers; "
    "and boundary/readout tails are silent, then the local trace branch has no source-coupled pole and no local source-cokernel: "
    "lambda_tr is absent locally and Q_tr^A=J_tr=0 for compact local tests."
)

SOURCE_SPECS = [
    {
        "source_id": "899_doc",
        "path": ROOT / "899-Y5-R10-trace-residual-vector-source-pack-and-local-bound-interface.md",
        "needle": "trace residual vector is now wired",
        "role": "immediate source-pack handoff",
    },
    {
        "source_id": "899_validation",
        "path": OUT / "P8_Y5_BRR545_899_VALIDATION.csv",
        "needle": "V899_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "899_source_pack",
        "path": OUT / "P8_Y5_R10_899_TRACE_RESIDUAL_SOURCE_PACK.csv",
        "needle": "RSP899_0",
        "role": "residual quantity/source requirement rows",
    },
    {
        "source_id": "899_zero_gate",
        "path": OUT / "P8_Y5_R10_899_THEOREM_ZERO_REOPEN_GATE.csv",
        "needle": "TZR899_0_vertical_generator",
        "role": "theorem-zero reopen clauses",
    },
    {
        "source_id": "886_zero_pole",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "Zero-Pole Implication Theorem",
        "role": "rank-zero/no-pole/source-cokernel theorem",
    },
    {
        "source_id": "886_validation",
        "path": OUT / "P8_Y5_BRR545_886_VALIDATION.csv",
        "needle": "V886_12_validation_rows_ready",
        "role": "zero-pole checkpoint validation",
    },
    {
        "source_id": "879_covector_pairing",
        "path": ROOT / "879-Y5-R10-parent-trace-covector-and-pairing-source-or-closure.md",
        "needle": "P_tr` is demoted to closure-only",
        "role": "current parent-owner blocker for P_tr",
    },
    {
        "source_id": "878_projector",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "A real trace projector requires",
        "role": "formal P_tr/v_tr construction",
    },
    {
        "source_id": "876_trace_hessian",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "parent-Hessian problem",
        "role": "Z_tr/lambda_tr extraction contract",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "Dq_loc[U][v_T]=0",
        "role": "local quotient verticality lemma",
    },
    {
        "source_id": "873_trace_charge_zero",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "chain-rule zero theorem",
        "role": "matter trace-charge zero theorem",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "ranked the trace residual blockers and wrote the combined local trace silence theorem as a conditional target",
            "best_partial_result": "Z_tr, lambda_tr, and Q_tr are now controlled by one theorem-zero stack if parent ownership, local rank-zero, matter descent, and no-tail clauses close",
            "hard_blockers": "ell_tr/Q_trace/Q_star/K_parent/P_tr are still not parent-owned; q_loc support/no-tail and matter descent/no-marker remain unsigned",
            "what_is_not_claimed": "trace zero, no local pole, Q_tr=0, R10/PPN/WEP/clock/orbital pass, or local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def priority_stack_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "PRI900_0_parent_trace_owner",
            1,
            "parent-own ell_tr/K_parent/v_tr/P_tr",
            "without a real P_tr the no-pole, source-cokernel, H_tr, Z_tr, and lambda_tr tests cannot even be evaluated",
            10,
            9,
            "not_owned_closure_only",
            "derive trace owner/local rank-zero certificate or concede finite carrier fill",
        ),
        (
            "PRI900_1_no_pole_rank_zero",
            2,
            "prove rank(P_loc P_tr P_loc^dagger)=0 or no local source-coupled pole",
            "this kills Z_tr/lambda_tr as local finite-carrier rows instead of sourcing them",
            10,
            8,
            "conditional_theorem_valid_parent_unsigned",
            "use only after parent trace owner exists",
        ),
        (
            "PRI900_2_source_cokernel_Qtr",
            3,
            "prove J_tr=P_tr^dagger J_parent=0 and Q_tr^A=0",
            "this kills the R10/orbital matter amplitude and WEP/clock source charges",
            10,
            7,
            "conditional_chain_rule_valid_parent_unsigned",
            "requires q_loc verticality plus matter descent/no-marker",
        ),
        (
            "PRI900_3_boundary_no_tail",
            4,
            "prove compact local projection silence for boundary/exact trace currents",
            "without no-tail, a nominally global trace endpoint can leak into local tests",
            8,
            6,
            "open",
            "certify support/no-tail or carry B_tr_tail",
        ),
        (
            "PRI900_4_finite_carrier_fill",
            5,
            "source Z_tr, lambda_tr, Q_tr/m, and alpha_tr(lambda) if theorem-zero fails",
            "this is the honest empirical branch, but not the least-scrutiny route",
            9,
            4,
            "retained_nonclaim",
            "fill parent numeric rows only after a parent action supplies them",
        ),
        (
            "PRI900_5_metric_clock_response",
            6,
            "derive C_tr PPN, clock/EM, and source-normalization responses",
            "needed if trace amplitude survives or if double-zero theorem does not close",
            7,
            5,
            "missing_response_operator",
            "defer until trace owner/amplitude route is decided",
        ),
    ]
    return [
        {
            "priority_id": priority_id,
            "rank": rank,
            "target": target,
            "why_this_order": why_this_order,
            "local_GR_impact_0_10": impact,
            "dependency_weight_0_10": dependency,
            "current_status": current_status,
            "next_action": next_action,
            "selected_now": rank == 1,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for priority_id, rank, target, why_this_order, impact, dependency, current_status, next_action in rows
    ]


def combined_zero_theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CZT900_0_statement",
            "claim": "combined local trace silence theorem",
            "statement": COMBINED_THEOREM,
            "proof_status": "conditional_theorem_target",
            "parent_status": "not_parent_signed",
            "what_it_would_buy": "Z_tr/lambda_tr become absent locally and Q_tr/J_tr vanish without fitting a tiny coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT900_1_parent_projector",
            "claim": "P_tr is a real parent object",
            "statement": "ell_tr=DQ_trace, v_tr=K_parent^{-1}ell_tr/<ell_tr,K_parent^{-1}ell_tr>, P_tr=v_tr otimes ell_tr",
            "proof_status": "formula_valid",
            "parent_status": "blocked_by_Qtrace_Qstar_Kparent",
            "what_it_would_buy": "rank, source-cokernel, and H_tr tests become meaningful",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT900_2_rank_zero_to_no_pole",
            "claim": "rank-zero removes the local trace pole",
            "statement": "if rank(P_loc P_tr P_loc^dagger)=0, compact local sources have no physical trace image and the reduced Green function has no source-coupled scalar pole",
            "proof_status": "conditional_implication_valid_from_886",
            "parent_status": "rank_zero_unsigned",
            "what_it_would_buy": "lambda_tr is not a local physical range and no R10 finite-range trace force exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT900_3_matter_descent_to_Qzero",
            "claim": "matter descent kills Q_tr",
            "statement": "if S_matter=Sbar[q_loc(Phi),Psi,theta], Dq_loc[v_tr]=0, and Lie_vtr theta=0, then partial_vtr S_matter=0 and Q_tr^A=0",
            "proof_status": "conditional_chain_rule_valid_from_873",
            "parent_status": "matter_descent_no_marker_unsigned",
            "what_it_would_buy": "R10/WEP/clock/orbital trace source amplitudes vanish by structure",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT900_4_no_tail_stability",
            "claim": "boundary/readout tails do not reintroduce the local source",
            "statement": "if P_loc dB_trace|_U=0 and no post-readout EFT trace spurion enters S_parent, the rank-zero/source-cokernel result is stable under integration by parts and readout",
            "proof_status": "necessary_stability_clause",
            "parent_status": "no_tail_unsigned",
            "what_it_would_buy": "prevents a fake zero caused by throwing boundary terms away",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT900_5_verdict",
            "claim": "the theorem shape is strong but not promoted",
            "statement": "the combined theorem is the least-scrutiny route, but current evidence fails at parent trace ownership before the rank and source-cokernel tests can be promoted",
            "proof_status": "conditional_valid_not_promoted",
            "parent_status": "parent_owner_missing_first_blocker",
            "what_it_would_buy": "selects 901: trace-owner local rank-zero certificate or finite carrier fill",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def parent_signature_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "signature_id": "PST900_0_Qtrace_Qstar",
            "required_signature": "Q_trace and Q_star are parent variables/readouts with fixed normalization",
            "current_evidence": "879 records ell_tr formula but Q_star and endpoint covectors remain missing",
            "test_result": "fail_for_claim",
            "if_failed": "ell_tr cannot be claimed and P_tr remains closure-only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "PST900_1_Kparent_pairing",
            "required_signature": "K_parent or constrained pseudo-inverse raises ell_tr into v_tr",
            "current_evidence": "879 finds charge metric, endpoint potential, symplectic, and Hessian pairings non-computable for trace",
            "test_result": "fail_for_claim",
            "if_failed": "v_tr normalization and rank tests are arbitrary",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "PST900_2_Ptr_parent_owner",
            "required_signature": "P_tr=v_tr otimes ell_tr is parent-owned before local testing",
            "current_evidence": "878 gives the formal construction; 879 demotes current P_tr to closure-only",
            "test_result": "fail_for_claim",
            "if_failed": "H_tr, Z_tr, lambda_tr, and no-pole cannot be promoted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "PST900_3_qloc_support_rank",
            "required_signature": "q_loc[U] is a parent compact local quotient and v_tr has zero/gauge local jet support",
            "current_evidence": "874 proves the restriction lemma only conditionally",
            "test_result": "fail_for_claim",
            "if_failed": "trace may be a real local scalar/conformal carrier",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "PST900_4_matter_descent_no_marker",
            "required_signature": "matter stack and constants descend through q_loc with no trace marker",
            "current_evidence": "873 gives chain-rule zero only if descent/no-marker premises close",
            "test_result": "fail_for_claim",
            "if_failed": "Q_tr/m and species/clock response rows must be sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "PST900_5_boundary_no_tail",
            "required_signature": "boundary/exact trace current has no compact local tail and readout remains source-at-zero",
            "current_evidence": "886 and 899 keep no-tail unsigned",
            "test_result": "fail_for_claim",
            "if_failed": "B_tr_tail/K_perp_trace remain active contamination guards",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "PST900_6_verdict",
            "required_signature": "PST900_0 through PST900_5 jointly pass",
            "current_evidence": "first three parent-owner clauses already fail for claim",
            "test_result": "not_signed",
            "if_failed": "do not claim trace silence; select 901 parent-owner certificate or finite fill",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def source_acquisition_plan_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "SAP900_0_Ztr",
            "Z_tr",
            "principal symbol of H_tr=P_tr^dagger Hess(S_parent) P_tr on local scalar trace subspace",
            "needed only if no-pole/rank-zero fails",
            "MISSING_PARENT_TRACE_OWNER_AND_HESSIAN",
            "do not estimate from data; derive from parent action or keep invalid",
        ),
        (
            "SAP900_1_lambdatr",
            "lambda_tr",
            "lambda_tr=sqrt(Z_tr/mu_tr^2) or hbar/(m_tr c) after parent mass gap is known",
            "needed only if finite trace carrier has a physical pole",
            "MISSING_MASS_GAP_OR_NOPOLE",
            "derive mu_tr^2 from parent Hessian or mark absent_by_theorem",
        ),
        (
            "SAP900_2_Qtr_universal",
            "Q_tr_over_m_universal",
            "source-cokernel or matter charge projection partial_vtr S_A divided by inertial mass",
            "controls R10/orbital common-force amplitude",
            "MISSING_SOURCE_COKERNEL_OR_QZERO_THEOREM",
            "prove Q_tr=0 by descent or derive body-source functional",
        ),
        (
            "SAP900_3_alpha_tr",
            "alpha_tr_AB(lambda_tr)",
            "Q_tr^A Q_tr^B/(4*pi*Z_tr*G_obs*m_A*m_B)",
            "first numeric R10/orbital prediction row",
            "MISSING_Z_LAMBDA_Q_INPUTS",
            "only compute after SAP900_0..2 are sourced and units are fixed",
        ),
        (
            "SAP900_4_bound_curve",
            "R10 alpha_bound(lambda)",
            "claim-grade digitized or machine-readable bound curve with positive numeric rows",
            "external comparison only after MTS row exists",
            "CURRENT_BOUND_FILE_PLACEHOLDER_NONCLAIM",
            "do not use anchor/placeholder rows for claims",
        ),
    ]
    return [
        {
            "source_plan_id": source_plan_id,
            "quantity": quantity,
            "definition": definition,
            "needed_if": needed_if,
            "current_status": current_status,
            "next_action": next_action,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for source_plan_id, quantity, definition, needed_if, current_status, next_action in rows
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD900_0_theorem_zero",
            "branch": "combined local trace silence theorem",
            "status": "best_route_but_not_entered",
            "reason": "conditional theorem is strong, but parent trace owner/P_tr/K_parent is missing",
            "decision": "not_promoted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD900_1_finite_carrier_source",
            "branch": "finite trace carrier/source acquisition",
            "status": "retained_nonclaim",
            "reason": "if parent-owner/rank-zero fails, Z_tr/lambda_tr/Q_tr must be sourced before data tests",
            "decision": "not_executable_yet",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD900_2_selected_next",
            "branch": "trace-owner local rank-zero certificate or finite fill",
            "status": "selected",
            "reason": "the first blocker is parent ownership; solve that before R10 or PPN claims",
            "decision": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE900_0_trace_zero",
            "claim": "local trace branch zero-returns",
            "claim_allowed": False,
            "blocker": "combined theorem premises not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CGATE900_1_no_pole",
            "claim": "no local source-coupled trace pole",
            "claim_allowed": False,
            "blocker": "P_tr/H_tr/rank-zero not parent-owned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CGATE900_2_Qtr_zero",
            "claim": "Q_tr^A and J_tr vanish",
            "claim_allowed": False,
            "blocker": "matter descent/no-marker and source-cokernel premises unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CGATE900_3_R10_PPN_local",
            "claim": "R10/PPN/WEP/clock/orbital/local-GR pass",
            "claim_allowed": False,
            "blocker": "no numeric trace prediction and no theorem-zero promotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to parent-sign the trace owner/local rank-zero certificate; if it fails, fill the finite carrier source rows without claiming a pass",
            "include": "Q_trace/Q_star/K_parent, ell_tr, v_tr, P_tr, q_loc support rank, no-tail certificate, finite Z_tr/lambda_tr/Q_tr fallback",
            "exclude": "data claims, fitted tiny couplings, placeholder alpha rows, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_899_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_899_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    priority_rows_: list[dict[str, object]],
    theorem_rows_: list[dict[str, object]],
    signature_rows_: list[dict[str, object]],
    source_plan_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        priority_rows_,
        theorem_rows_,
        signature_rows_,
        source_plan_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V900_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V900_1_prior_899_clean",
            "result": "pass" if prior_899_clean() else "fail",
            "detail": "P8_Y5_BRR545_899_VALIDATION.csv clean",
        },
        {
            "check_id": "V900_2_priority_selects_parent_owner",
            "result": "pass"
            if priority_rows_[0]["priority_id"] == "PRI900_0_parent_trace_owner" and priority_rows_[0]["selected_now"] is True
            else "fail",
            "detail": "parent trace ownership selected as first blocker",
        },
        {
            "check_id": "V900_3_combined_theorem_written_nonclaim",
            "result": "pass"
            if any(row["theorem_id"] == "CZT900_5_verdict" and row["proof_status"] == "conditional_valid_not_promoted" for row in theorem_rows_)
            else "fail",
            "detail": "combined local trace silence theorem remains conditional",
        },
        {
            "check_id": "V900_4_parent_signature_tests_fail_for_claim",
            "result": "pass"
            if all(row["valid_for_claim"] is False for row in signature_rows_)
            and any(row["signature_id"] == "PST900_6_verdict" and row["test_result"] == "not_signed" for row in signature_rows_)
            else "fail",
            "detail": "parent signature stack is not signed",
        },
        {
            "check_id": "V900_5_source_plan_retained_missing_nonclaim",
            "result": "pass"
            if all("MISSING" in stringify(row["current_status"]) or "PLACEHOLDER" in stringify(row["current_status"]) for row in source_plan_rows_)
            else "fail",
            "detail": "finite carrier source plan remains missing/nonclaim",
        },
        {
            "check_id": "V900_6_branch_selected_next",
            "result": "pass"
            if any(row["branch_id"] == "BD900_2_selected_next" and row["decision"] == NEXT_TARGET for row in branch_rows_)
            else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V900_7_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all trace/local claims remain blocked",
        },
        {
            "check_id": "V900_8_all_generated_rows_nonclaim",
            "result": "pass" if generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V900_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V900_10_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V900_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows_: list[dict[str, object]],
    source_rows_: list[dict[str, object]],
    priority_rows_: list[dict[str, object]],
    theorem_rows_: list[dict[str, object]],
    signature_rows_: list[dict[str, object]],
    source_plan_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 900 - Y5/R10 Trace Residual Vector Priority Source Acquisition Or Theorem-Zero Reopen

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the best next move is not data yet; it is parent trace ownership**. The combined local trace silence theorem is now written as the least-scrutiny route: if the parent action owns `ell_tr/K_parent/v_tr/P_tr`, the compact-local rank is zero, matter descends through `q_loc`, and boundary tails are silent, then `Z_tr/lambda_tr` are absent locally and `Q_tr/J_tr` vanish. But this route fails for claim immediately because `P_tr` is still closure-only in the current corpus.

## Exact 900 Finding
The trace branch has one clean theoretical escape hatch: prove the parent trace direction is a boundary/readout-only local-rank-zero direction. That would remove the finite local scalar pole and its matter source-cokernel together, which is exactly the kind of derivation needed for MTS to reduce to GR/Newton rather than behave like a tuned fifth-force model. The present documents do not sign the first ownership clauses, so 900 selects a precise next fork: parent-sign the trace-owner/local-rank-zero certificate, or stop trying to zero it and fill `Z_tr`, `lambda_tr`, and `Q_tr/m` as finite-carrier source rows.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Priority Stack
{md_table(priority_rows_)}

## Combined Theorem-Zero Attempt
{md_table(theorem_rows_)}

## Parent Signature Test
{md_table(signature_rows_)}

## Source Acquisition Plan
{md_table(source_plan_rows_)}

## Branch Decision
{md_table(branch_rows_)}

## Claim Gate
{md_table(claim_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    priority_rows_ = priority_stack_rows(generated_utc)
    theorem_rows_ = combined_zero_theorem_rows(generated_utc)
    signature_rows_ = parent_signature_test_rows(generated_utc)
    source_plan_rows_ = source_acquisition_plan_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        priority_rows_,
        theorem_rows_,
        signature_rows_,
        source_plan_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_900_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_900_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_900_PRIORITY_STACK.csv": priority_rows_,
        "P8_Y5_R10_900_COMBINED_THEOREM_ZERO_ATTEMPT.csv": theorem_rows_,
        "P8_Y5_R10_900_PARENT_SIGNATURE_TEST.csv": signature_rows_,
        "P8_Y5_R10_900_SOURCE_ACQUISITION_PLAN.csv": source_plan_rows_,
        "P8_Y5_R10_900_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_900_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_900_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_900_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "900-Y5-R10-trace-residual-vector-priority-source-acquisition-or-theorem-zero-reopen.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        priority_rows_,
        theorem_rows_,
        signature_rows_,
        source_plan_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_900_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
