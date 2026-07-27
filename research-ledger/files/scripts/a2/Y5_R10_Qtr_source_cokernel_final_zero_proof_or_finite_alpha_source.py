from __future__ import annotations

import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_903_Qtr_source_cokernel_final_zero_proof_attempted_unsigned_finite_alpha_source_rows_staged_nonclaim"
CLAIM_CEILING = "Qtr_zero_final_attempt_and_finite_alpha_source_contract_only_no_Qtr_zero_no_numeric_alpha_no_R10_or_local_GR_claim"
NEXT_TARGET = "904-Y5-R10-finite-alpha-source-provenance-and-real-bound-curve-gate.md"
ALPHA_TR_FORMULA = "alpha_tr_AB=(Q_tr^A/m_A)*(Q_tr^B/m_B)/(4*pi*Z_tr*G_obs)"

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]

SOURCE_SPECS = [
    {
        "source_id": "902_doc",
        "path": ROOT / "902-Y5-R10-finite-trace-carrier-minimum-source-runner-or-Qtr-zero-proof.md",
        "needle": "source-cokernel/matter descent",
        "role": "immediate handoff to final Q_tr zero attempt",
    },
    {
        "source_id": "902_validation",
        "path": OUT / "P8_Y5_BRR545_902_VALIDATION.csv",
        "needle": "V902_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "902_qtr_escape",
        "path": OUT / "P8_Y5_R10_902_QTR_ZERO_ESCAPE_HATCH.csv",
        "needle": "QZE902_5_verdict",
        "role": "Q_tr zero escape hatch",
    },
    {
        "source_id": "897_source_cokernel",
        "path": OUT / "P8_Y5_R10_897_SOURCE_COKERNEL_PROOF_ATTEMPT.csv",
        "needle": "SCA897_4_verdict",
        "role": "source-cokernel theorem attempt",
    },
    {
        "source_id": "898_pairing",
        "path": OUT / "P8_Y5_R10_898_SOURCE_COKERNEL_PAIRING.csv",
        "needle": "SCP898_4_verdict",
        "role": "trace coupling source-cokernel pairing",
    },
    {
        "source_id": "898_vertical_generator",
        "path": OUT / "P8_Y5_R10_898_TRACE_VERTICAL_GENERATOR_SIGNATURE.csv",
        "needle": "VGS898_6_verdict",
        "role": "vertical generator ownership audit",
    },
    {
        "source_id": "898_matter_descent",
        "path": OUT / "P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv",
        "needle": "MDS898_5_verdict",
        "role": "matter descent signature audit",
    },
    {
        "source_id": "873_trace_charge_zero",
        "path": OUT / "P8_Y5_R10_873_LOCAL_TRACE_CHARGE_ZERO_THEOREM.csv",
        "needle": "QTZ873_1_chain_rule_zero",
        "role": "local trace matter charge zero theorem",
    },
    {
        "source_id": "874_verticality",
        "path": OUT / "P8_Y5_R10_874_VERTICALITY_DERIVATION_ATTEMPT.csv",
        "needle": "VD874_4_verdict",
        "role": "q_loc verticality derivation attempt",
    },
    {
        "source_id": "901_finite_fill",
        "path": OUT / "P8_Y5_R10_901_FINITE_CARRIER_FILL_ROWS.csv",
        "needle": "FCF901_3_Qtr_universal",
        "role": "finite alpha source fallback inputs",
    },
    {
        "source_id": "902_minimum_schema",
        "path": OUT / "P8_Y5_R10_902_MINIMUM_FINITE_INPUT_SCHEMA.csv",
        "needle": "FTI902_3",
        "role": "minimum finite trace runner schema",
    },
    {
        "source_id": "r10_runner",
        "path": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
        "needle": "MTS_REQUIRED_COLUMNS",
        "role": "existing alpha(lambda) comparator",
    },
    {
        "source_id": "r10_bound_placeholder",
        "path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needle": "R10_BOUND_PLACEHOLDER_0",
        "role": "current R10 bound file remains placeholder",
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
            "what_changed": "made the final clean Q_tr source-cokernel proof attempt and staged finite-alpha source rows as the fallback",
            "best_partial_result": "the theorem has an exact chain-rule/source-cokernel form; if the parent signs the premises, local trace matter coupling vanishes structurally",
            "hard_blockers": "P_tr/v_tr parent ownership, q_loc verticality, matter-stack descent, no-marker constants, no-pole/source-cokernel rank, and boundary no-tail remain unsigned",
            "what_is_not_claimed": "Q_tr=0, alpha_tr=0, a finite trace alpha value, R10/PPN/WEP/clock/orbital pass, or local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def qtr_zero_proof_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "QZP903_0_definition",
            "local trace charge",
            "Q_tr^A := partial_{v_tr}S_A = <v_tr,J_A> or body integral of J_tr",
            "definition_ready",
            "does not decide zero/nonzero",
            "sets the exact coupling target",
        ),
        (
            "QZP903_1_parent_vertical_generator",
            "v_tr ownership",
            "ell_tr=DQ_trace, v_tr=K_parent^{-1}ell_tr/<ell_tr,K_parent^{-1}ell_tr>, P_tr=v_tr otimes ell_tr",
            "unsigned",
            "MISSING_ELLTR_KPARENT_PTR_PARENT_OWNERSHIP",
            "makes Dq_loc[v_tr] and source pairing computable",
        ),
        (
            "QZP903_2_quotient_verticality",
            "Dq_loc[v_tr]=0 on compact local U",
            "q_loc is a local restriction/jet quotient and v_tr has no compact local support or is exact/gauge-zero",
            "unsigned",
            "MISSING_QLOC_SUPPORT_OR_EXACT_CURRENT_CERTIFICATE",
            "kills the direct matter derivative by chain rule",
        ),
        (
            "QZP903_3_matter_descent",
            "S_matter descends through q_loc",
            "S_A[Phi,Psi]=Sbar_A[q_loc(Phi),Psi_A,theta_A]",
            "unsigned",
            "MISSING_PARENT_MATTER_FUNCTOR_AND_GEOMETRY_STACK_DESCENT",
            "forces ordinary matter to see only quotient variables",
        ),
        (
            "QZP903_4_no_marker_constants",
            "Lie_vtr theta_A=0",
            "species, clock, EM, binding, and mass-ratio constants carry no independent trace marker",
            "unsigned",
            "MISSING_NO_MARKER_SUPERSELECTION_THEOREM",
            "removes WEP/clock/species re-entry",
        ),
        (
            "QZP903_5_source_cokernel_or_no_pole",
            "local source-cokernel/no-pole",
            "rank(P_loc P_tr P_loc^dagger)=0 or <u_tr,J_parent>=0 for every compact physical local test mode",
            "unsigned",
            "MISSING_PTR_HTR_RANK_ZERO_OR_EXPLICIT_COKERNEL_PAIRING",
            "removes source-coupled local trace carrier",
        ),
        (
            "QZP903_6_boundary_no_tail",
            "boundary/readout tail silence",
            "P_loc J_trace=0 and P_loc dB_trace=0 for compact local tests",
            "unsigned",
            "MISSING_BOUNDARY_SUPPORT_OR_RELATIVE_COHOMOLOGY_CERTIFICATE",
            "prevents endpoint/readout currents from leaking back locally",
        ),
        (
            "QZP903_7_theorem_verdict",
            "Q_tr=0",
            "Q_tr^A=0 follows from QZP903_1 through QZP903_6 by chain rule and source-cokernel projection",
            "not_promoted",
            "one or more required parent signatures remain unsigned",
            "would close the local R10/orbital matter-amplitude branch if signed",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "target": target,
            "mathematical_statement": statement,
            "current_status": status,
            "blocker_or_condition": blocker,
            "what_it_would_buy": buy,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for clause_id, target, statement, status, blocker, buy in rows
    ]


def source_cokernel_pairing_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "SCP903_0_pairing_identity",
            "Q_tr^A=<v_tr,J_A>",
            "with v_tr parent-owned, the matter coupling is the contraction of the trace vertical generator with the local source current",
            "definition_ready_but_parent_generator_unsigned",
            "MISSING_VTR_PARENT_OWNERSHIP",
            "finite Q_tr_over_m source row",
        ),
        (
            "SCP903_1_chain_rule_cokernel",
            "J_A in Range(Dq_loc)^* and v_tr in ker(Dq_loc)",
            "then <v_tr,J_A>=<Dq_loc[v_tr],dSbar/dq_loc>=0",
            "conditional_theorem_valid",
            "MISSING_QLOC_VERTICALITY_AND_MATTER_DESCENT",
            "Q_tr=0 for ordinary compact local matter",
        ),
        (
            "SCP903_2_rank_zero_cokernel",
            "P_loc P_tr P_loc^dagger=0",
            "compact local physical modes have no trace image and no source-coupled trace pole",
            "conditional_theorem_valid",
            "MISSING_PTR_HTR_RANK_ZERO",
            "lambda_tr absent locally or alpha_tr structurally zero",
        ),
        (
            "SCP903_3_tail_counterterm_watch",
            "local boundary/readout re-entry",
            "exact or endpoint currents must have zero compact local projection after integration by parts",
            "not_proved",
            "MISSING_BOUNDARY_NO_TAIL",
            "boundary/EFT residual remains active",
        ),
        (
            "SCP903_4_legal_counterbranch",
            "representative matter coupling",
            "if matter couples to a representative Weyl/disformal/coframe/connection coefficient outside q_loc, then Q_tr need not vanish",
            "legal_counterbranch",
            "current parent action does not exclude this branch",
            "finite alpha/source-response ledger becomes mandatory",
        ),
        (
            "SCP903_5_verdict",
            "source-cokernel final zero proof",
            "the proof is exact as a conditional theorem but cannot be promoted from the current corpus",
            "not_parent_signed",
            "same six signature debts remain open",
            "selects finite-alpha source provenance and real bound curve gate",
        ),
    ]
    return [
        {
            "pairing_id": pairing_id,
            "object": obj,
            "proof_step": proof_step,
            "current_status": status,
            "blocker": blocker,
            "fallback_quantity": fallback,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for pairing_id, obj, proof_step, status, blocker, fallback in rows
    ]


def finite_alpha_source_rows(generated_utc: str) -> list[dict[str, object]]:
    schema_rows = read_csv(OUT / "P8_Y5_R10_902_MINIMUM_FINITE_INPUT_SCHEMA.csv")
    parent_sources = {
        "P_tr,H_tr": "parent trace projector and Hessian after gauge/constraint reduction",
        "Z_tr": "principal symbol of the trace Hessian on observed local metric background",
        "lambda_tr": "parent mass gap or no-pole certificate",
        "Q_tr_over_m_universal": "body-source functional or source-cokernel zero theorem",
        "Delta_AB_Q_tr_over_m,C_tr_clock_i,C_tr_alphaEM": "species/clock/EM no-marker theorem or sourced response coefficients",
        "C_tr_gamma,C_tr_beta,C_tr_source,Gdot_tr": "weak-field response and measured-GM/source-normalization split",
        "alpha_tr_AB(lambda_tr)": "derived Z_tr, lambda_tr, Q_tr/m plus claim-grade R10 bound curve",
        "B_tr_tail,K_perp_trace": "boundary support/no-tail certificate or explicit residual bound",
    }
    rows: list[dict[str, object]] = []
    for index, row in enumerate(schema_rows):
        quantity = row["quantity"]
        rows.append(
            {
                "source_row_id": f"FAS903_{index}",
                "quantity": quantity,
                "role": row["runner_role"],
                "required_parent_input": parent_sources.get(quantity, row["source_required"]),
                "current_value": row["current_value"],
                "current_status": "MISSING_OR_UNSIGNED",
                "formula_or_definition": row["definition"],
                "units_or_normalization": "source_defined_required",
                "source_path_required": "MISSING_PARENT_SOURCE_PATH_OR_ZERO_THEOREM",
                "claim_rule": "valid_for_claim false until numeric/source-backed or theorem-zero",
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def r10_alpha_dry_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_trace_Qtr_final_zero_attempt",
            "branch_id": "Qtr_source_cokernel_unsigned",
            "curve_id": "FT903_R10_0_Qtr_zero_not_signed",
            "lambda_value": "MISSING_NO_LOCAL_POLE_OR_LAMBDA_TR",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_QTR_ZERO_NOT_PARENT_SIGNED",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "alpha_tr=0 only if Q_tr=0 or no source-coupled local pole is parent-signed",
            "derivation_status": "QTR_SOURCE_COKERNEL_UNSIGNED_NONCLAIM",
            "formula_reference": "Q_tr^A=0 if matter descends through q_loc and v_tr is local-vertical/source-cokernel",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_903_QTR_ZERO_PROOF_CLAUSES.csv",
            "assumptions": "final zero proof attempt only; theorem not promoted",
            "valid_for_claim": False,
            "notes": "runner must reject this row because the zero theorem is unsigned",
            "generated_utc": generated_utc,
        },
        {
            "model_id": "MTS_trace_finite_alpha_source_contract",
            "branch_id": "finite_alpha_missing_parent_sources",
            "curve_id": "FT903_R10_1_finite_alpha_source_required",
            "lambda_value": "MISSING_LAMBDA_TR",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ZTR_QTR_SOURCE_INPUTS",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "Yukawa alpha_tr_AB exp(-r/lambda_tr)",
            "derivation_status": "FINITE_ALPHA_SOURCE_CONTRACT_NONCLAIM",
            "formula_reference": ALPHA_TR_FORMULA,
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_903_FINITE_ALPHA_SOURCE_ROWS.csv",
            "assumptions": "no numeric parent coefficients and no claim-grade bound curve",
            "valid_for_claim": False,
            "notes": "finite branch is now an input acquisition problem, not evidence",
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD903_0_Qtr_zero",
            "branch": "prove Q_tr=0 by source-cokernel/matter descent",
            "decision": "not_promoted",
            "reason": "exact proof shape exists but parent signatures are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD903_1_finite_alpha",
            "branch": "finite trace alpha source rows",
            "decision": "staged_nonclaim",
            "reason": "zero proof failed to promote, so every finite local test now needs source-backed Z_tr, lambda_tr, Q_tr/m, response operators, and real bound curves",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD903_2_selected_next",
            "branch": "finite-alpha provenance and real bound curve",
            "decision": NEXT_TARGET,
            "reason": "the coupling theorem route is exhausted until new parent signatures exist; next useful move is source provenance and real bound data plumbing",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE903_0_Qtr_zero", "Q_tr=0", "source-cokernel theorem not parent-signed"),
        ("CGATE903_1_alpha_zero", "alpha_tr=0", "depends on Q_tr zero or no local source-coupled trace pole"),
        ("CGATE903_2_finite_alpha", "numeric alpha_tr(lambda_tr)", "Z_tr/lambda_tr/Q_tr/m and response normalization missing"),
        ("CGATE903_3_R10", "R10 comparison pass", "MTS alpha rows invalid and bound curve placeholder"),
        ("CGATE903_4_local_GR", "local GR/Newton reduction", "trace coupling branch remains open as residual/source-acquisition problem"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "claim_allowed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, claim, blocker in gates
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "convert finite trace coupling from placeholder rows into a source-provenance and real-bound-curve acquisition gate, still with no claims",
            "include": "Z_tr, lambda_tr, Q_tr/m, response coefficients, source paths, R10 bound curve status, runner refusal modes",
            "exclude": "fitted tiny alpha, public claim, local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
    return True


def prior_902_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_902_VALIDATION.csv")
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def bound_curve_still_placeholder() -> bool:
    rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv")
    return bool(rows) and all(row.get("valid_for_claim", "").lower() == "false" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF:
            count += 1
    return count


def import_r10_runner() -> Any:
    runner_path = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
    spec = importlib.util.spec_from_file_location("r10_runner_903", runner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {runner_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_r10_dry_runner() -> dict[str, Any]:
    module = import_r10_runner()
    result = module.run_runner(
        OUT / "P8_Y5_R10_903_R10_ALPHA_DRY_ROWS.csv",
        LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        OUT / "P8_Y5_R10_903_R10_DRY_RUNNER_RESULTS",
    )
    return result["status"]


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    proof_rows_: list[dict[str, object]],
    pairing_rows_: list[dict[str, object]],
    finite_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    runner_status: dict[str, Any],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        proof_rows_,
        pairing_rows_,
        finite_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
    ]
    missing_schema_columns = [column for column in MTS_REQUIRED_COLUMNS if column not in dry_rows_[0]]
    checks = [
        {
            "check_id": "V903_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V903_1_prior_902_clean",
            "result": "pass" if prior_902_clean() else "fail",
            "detail": "P8_Y5_BRR545_902_VALIDATION.csv clean",
        },
        {
            "check_id": "V903_2_Qtr_zero_not_promoted",
            "result": "pass"
            if any(row["clause_id"] == "QZP903_7_theorem_verdict" and row["current_status"] == "not_promoted" for row in proof_rows_)
            else "fail",
            "detail": "final Q_tr zero proof remains conditional/not promoted",
        },
        {
            "check_id": "V903_3_pairing_verdict_unsigned",
            "result": "pass"
            if any(row["pairing_id"] == "SCP903_5_verdict" and row["current_status"] == "not_parent_signed" for row in pairing_rows_)
            else "fail",
            "detail": "source-cokernel pairing remains unsigned",
        },
        {
            "check_id": "V903_4_finite_alpha_rows_blocked",
            "result": "pass"
            if len(finite_rows_) == 8 and all(row["current_status"] == "MISSING_OR_UNSIGNED" for row in finite_rows_)
            else "fail",
            "detail": f"finite_alpha_rows={len(finite_rows_)}",
        },
        {
            "check_id": "V903_5_R10_dry_rows_match_schema",
            "result": "pass" if not missing_schema_columns else "fail",
            "detail": "schema ok" if not missing_schema_columns else "missing=" + ",".join(missing_schema_columns),
        },
        {
            "check_id": "V903_6_R10_dry_runner_blocks_claim",
            "result": "pass"
            if runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
            else "fail",
            "detail": json.dumps(
                {
                    "claim_allowed": runner_status.get("claim_allowed"),
                    "valid_mts_rows": runner_status.get("valid_mts_rows"),
                    "blocked_or_failed_rows": runner_status.get("blocked_or_failed_rows"),
                },
                sort_keys=True,
            ),
        },
        {
            "check_id": "V903_7_bound_curve_placeholder_nonclaim",
            "result": "pass" if bound_curve_still_placeholder() else "fail",
            "detail": "R10_alpha_lambda_bound_curve_DIGITIZED.csv remains invalid placeholder",
        },
        {
            "check_id": "V903_8_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all Q_tr/alpha/local claims blocked",
        },
        {
            "check_id": "V903_9_all_generated_rows_nonclaim",
            "result": "pass" if generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V903_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V903_11_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V903_12_validation_rows_ready",
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
    proof_rows_: list[dict[str, object]],
    pairing_rows_: list[dict[str, object]],
    finite_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 903 - Y5/R10 Qtr Source-Cokernel Final Zero Proof Or Finite Alpha Source

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the clean `Q_tr=0` route is now written as an exact conditional theorem, but it still cannot be promoted from the current parent corpus**. The theorem is not wrong; it is unsigned. If the parent later owns `v_tr/P_tr`, compact-local `q_loc` verticality, matter-stack descent, no-marker constants, no local trace pole/source-cokernel rank, and boundary no-tail, then `Q_tr^A=0` follows by chain rule and source-cokernel pairing. Until that happens, the honest route is finite-alpha source acquisition, not a hidden tiny fitted coupling.

## Exact 903 Finding
This is the end of the derivation-first attempt for the local trace coupling unless new parent signatures are introduced. We have a sharp theorem contract:

`Q_tr^A = partial_{{v_tr}} S_A = <v_tr,J_A> = 0`

provided matter descends through `q_loc`, `v_tr in ker(Dq_loc)`, no ordinary constants carry a trace marker, no compact local trace pole exists, and boundary/readout tails are silent. The current files do not sign those premises, so the local branch remains blocked rather than passed.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Qtr Zero Proof Clauses
{md_table(proof_rows_)}

## Source-Cokernel Pairing Test
{md_table(pairing_rows_)}

## Finite Alpha Source Rows
{md_table(finite_rows_)}

## R10 Alpha Dry Rows
{md_table(dry_rows_)}

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
    proof_rows_ = qtr_zero_proof_clause_rows(generated_utc)
    pairing_rows_ = source_cokernel_pairing_rows(generated_utc)
    finite_rows_ = finite_alpha_source_rows(generated_utc)
    dry_rows_ = r10_alpha_dry_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)

    initial_outputs = {
        "P8_Y5_R10_903_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_903_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_903_QTR_ZERO_PROOF_CLAUSES.csv": proof_rows_,
        "P8_Y5_R10_903_SOURCE_COKERNEL_PAIRING_TEST.csv": pairing_rows_,
        "P8_Y5_R10_903_FINITE_ALPHA_SOURCE_ROWS.csv": finite_rows_,
        "P8_Y5_R10_903_R10_ALPHA_DRY_ROWS.csv": dry_rows_,
        "P8_Y5_R10_903_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_903_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_903_NEXT_TARGET.csv": next_rows_,
    }
    for filename, rows in initial_outputs.items():
        write_csv(OUT / filename, rows)

    runner_status = run_r10_dry_runner()
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        proof_rows_,
        pairing_rows_,
        finite_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        runner_status,
    )
    write_csv(OUT / "P8_Y5_BRR545_903_VALIDATION.csv", validation_rows_)

    doc_path = ROOT / "903-Y5-R10-Qtr-source-cokernel-final-zero-proof-or-finite-alpha-source.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        proof_rows_,
        pairing_rows_,
        finite_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_903_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
