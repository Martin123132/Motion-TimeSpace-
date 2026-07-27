from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4019"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4019-Y5-R2FR-EH-only-R11-no-extra-operator-adoption-or-PPN-residual-scorer.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4019_SOURCE_REGISTER.csv",
    "adoption": SRC / "P8_Y5_R2FR_4019_EH_ONLY_R11_ADOPTION_CLAUSES.csv",
    "theorem": SRC / "P8_Y5_R2FR_4019_NO_EXTRA_OPERATOR_THEOREM.csv",
    "scorer": SRC / "P8_Y5_R2FR_4019_PPN_RESIDUAL_SCORER_ROWS.csv",
    "audit": SRC / "P8_Y5_R2FR_4019_EH_ONLY_R11_AUDIT.csv",
    "cases": SRC / "P8_Y5_R2FR_4019_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4019_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4019_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4019_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4019_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4019_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4019_VALIDATION.csv",
}

NEXT_DOC = "4020-Y5-R2FR-local-GR-conditional-rollup-or-first-executable-PPN-score.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4020_local_GR_conditional_rollup_or_first_executable_PPN_score.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4019_00_handoff", SRC / "P8_Y5_R2FR_4018_NEXT_TARGET.csv", "NEXT4018_0", "4018 handoff"),
        ("SRC4019_01_4018_gamma", SRC / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv", "PPN4018_1_gamma_EH_zero", "4018 gamma theorem"),
        ("SRC4019_02_4018_beta", SRC / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv", "PPN4018_3_beta_EH_zero", "4018 beta theorem"),
        ("SRC4019_03_4018_vector", SRC / "P8_Y5_R2FR_4018_GAMMA_BETA_SOURCE_RESIDUAL_ROWS.csv", "PPR4018_0_master", "4018 PPN vector"),
        ("SRC4019_04_3885_target", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_0_target", "3885 EH PPN target"),
        ("SRC4019_05_3885_verdict", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_5_verdict", "3885 nonclaim verdict"),
        ("SRC4019_06_3886_gamma", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_00_delta_gamma_R11", "R11 gamma coefficient"),
        ("SRC4019_07_3886_beta_R11", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_04_delta_beta_R11", "R11 beta coefficient"),
        ("SRC4019_08_3886_q_loc", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_05_delta_beta_q_loc", "q_loc beta coefficient"),
        ("SRC4019_09_3886_total", SRC / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv", "COEF3886_12_R11_total", "R11 total coefficient"),
        ("SRC4019_10_3887_gamma", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_1_gamma_R11", "gamma fill pivot"),
        ("SRC4019_11_3887_beta", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_2_beta_source", "beta fill pivot"),
        ("SRC4019_12_3887_projector", SRC / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv", "FILL3887_5_projector_stress", "projector stress fill"),
        ("SRC4019_13_3915_zero", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_8_total", "conditional PPN zero vector"),
        ("SRC4019_14_3915_res_total", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_8_total", "executable PPN vector"),
        ("SRC4019_15_3915_res_gamma", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_0_gamma", "executable gamma"),
        ("SRC4019_16_3915_res_beta", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_1_beta", "executable beta"),
        ("SRC4019_17_3933_rollup", SRC / "P8_Y5_R2FR_3933_PPN_ZERO_ROLLUP.csv", "PPN3933_8_total", "private PPN zero rollup"),
        ("SRC4019_18_3967_fixedGM", SRC / "P8_Y5_R2FR_3967_PPN_STABILITY_THEOREM_OR_BOUND.csv", "PPN3967_0_fixed_GM_convention", "fixed GM convention"),
        ("SRC4019_19_3967_beta", SRC / "P8_Y5_R2FR_3967_PPN_STABILITY_THEOREM_OR_BOUND.csv", "PPN3967_2_beta_AB_law", "beta A/B law"),
        ("SRC4019_20_3967_envelope", SRC / "P8_Y5_R2FR_3967_PPN_STABILITY_THEOREM_OR_BOUND.csv", "PPN3967_5_absolute_no_cancellation_envelope", "PPN no cancellation envelope"),
        ("SRC4019_21_3988_PPN", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_ORIGIN_AND_PPN_THEOREM.csv", "JPPN3988_3_PPN_envelope", "source-current PPN envelope"),
        ("SRC4019_22_3989_rest", SRC / "P8_Y5_R2FR_3989_DESCENT_PREFAC_PPN_BOUND_ROWS.csv", "NPB3989_4_ppn_rest", "PPN rest vector"),
        ("SRC4019_23_3989_fill", SRC / "P8_Y5_R2FR_3989_FIRST_PPN_SOURCE_WEIGHT_FILL.csv", "PPNF3989_2_ppn_rest", "PPN rest fill"),
        ("SRC4019_24_3624_EH", SRC / "P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv", "NPG3624_0_EH_dominance", "EH dominance gate"),
        ("SRC4019_25_3626_components", SRC / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv", "PCF3626_6_total", "old component fill total"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def adoption_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("EHA4019_0_action_domain", "local operator domain", "S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter+S_EM+dB_proper+S_topological", "only EH contributes to metric Euler equations through O(U^2)", "candidate_branch_not_final"),
        ("EHA4019_1_R11_absent", "R11/no-extra operator", "Allowed(O_R11^{<=2PN})={topological, exact, auxiliary-double-zero, Sigma_loc-selected-zero}", "delta E_R11^{(1)}=delta E_R11^{(2)}=0", "unsigned_for_final_claim"),
        ("EHA4019_2_q_loc_absent", "q_loc/local projection tail", "P_loc(nabla Gamma_eff - nabla Khat)=0 through PPN order or is orthogonal to PPN projectors", "delta_beta_q_loc=0 and no finite-range PPN tail", "unsigned_for_final_claim"),
        ("EHA4019_3_readout_frame", "same observed readout", "same e_obs/g_obs/tau/frame defines U, gamma, beta and source current", "no readout or frame correction to gamma/beta", "conditional"),
        ("EHA4019_4_source_slot", "source-current same branch", "4012/3988 Hilbert source current and 4017 K_G packet feed the same EH equation", "A_source fixed before beta and B_source=A_source^2 under EH nonlinear completion", "conditional"),
        ("EHA4019_5_status", "adoption status", "branch is coherent but not declared final corpus parent action", "use as conditional rollup or scorer interface only", "nonclaim"),
    ]
    return [
        {
            "clause_id": clause_id,
            "component": component,
            "mathematical_form": form,
            "ppn_effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, component, form, effect, status in rows
    ]


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("NOX4019_0_operator_domain_theorem", "no extra metric operator through O(U^2)", "If every non-EH local operator is topological, exact, auxiliary with double-zero stress, or Sigma_loc-selected zero before readout, then DeltaE_MTS^{(1)}=DeltaE_MTS^{(2)}=0", "delta_gamma_R11=delta_beta_R11=0 conditionally", "EXACT_CONDITIONAL_NO_EXTRA_OPERATOR_THEOREM"),
        ("NOX4019_1_q_loc_projector_zero", "q_loc PPN tail zero", "If q_loc lies in the kernel of all PPN projectors Pi_gamma, Pi_beta, Pi_alpha_i, Pi_xi, Pi_zeta through O(U^2), then q_loc_Khat and delta_beta_q_loc vanish", "bulk/local projection tails cannot affect gamma/beta in the adopted branch", "EXACT_CONDITIONAL_PROJECTOR_KERNEL_THEOREM"),
        ("NOX4019_2_EH_PPN_solution", "EH-only PPN solution", "EH field equation with fixed K_G, same Hilbert source, same readout and no R11/q_loc tail gives the standard weak-field solution: gamma=1 and beta=1", "turns 4018 conditional theorem into the precise EH-only adoption branch", "EXACT_CONDITIONAL_EH_PPN_THEOREM"),
        ("NOX4019_3_failure_to_scorer", "failure maps to scorer", "Any unsigned clause maps to PPN residual scorer rows: delta_gamma_R11, delta_beta_R11, delta_beta_q_loc, readout, source, boundary/domain, preferred-frame and conservation", "no hidden operator closure remains", "FINITE_SCORER_INTERFACE"),
        ("NOX4019_4_no_private_rollup_claim", "private zero rollup guard", "Rows such as ZERO_IN_PRIVATE_LOCAL_BRANCH may guide the branch but cannot become a claim unless adoption clauses are signed or scorer rows pass", "prevents closure-only local-GR promotion", "ANTI_OVERCLAIM_GUARD"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": form,
            "derived_result": result,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, claim_piece, form, result, status in rows
    ]


def scorer_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PPS4019_0_master", "Delta_PPN_abs_4019", "|delta_gamma_R11|+|delta_gamma_readout|+|delta_gamma_frame|+|delta_gamma_source|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary_domain|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|", "every term zero or independently bounded", "full local-GR scorer"),
        ("PPS4019_1_delta_gamma_R11", "delta_gamma_R11", "Pi_gamma[DeltaE_R11^{(1)}]", "abs(delta_gamma_R11)<=2.3e-05 or theorem-zero", "gamma scorer"),
        ("PPS4019_2_delta_beta_R11", "delta_beta_R11", "Pi_beta[DeltaE_R11^{(2)}]", "abs(delta_beta_R11)<=7.8e-05 or theorem-zero", "beta operator scorer"),
        ("PPS4019_3_delta_beta_q_loc", "delta_beta_q_loc", "Pi_beta[q_loc_Khat^{(2)}]", "zero by projector-kernel theorem or bounded", "q_loc beta scorer"),
        ("PPS4019_4_delta_beta_source", "delta_beta_source", "B_source/A_source^2 - 1 + epsilon_SN", "abs(delta_beta_source)<=7.8e-05 or B_source=A_source^2 theorem", "source beta scorer"),
        ("PPS4019_5_readout_frame", "delta_readout_frame", "gamma/beta readout + frame mismatch terms", "same-readout theorem-zero or bounded", "readout scorer"),
        ("PPS4019_6_preferred_frame", "alpha_i_xi", "alpha1+alpha2+alpha3+xi from vector/domain/coframe/memory selectors", "each component below its own lock or theorem-zero", "preferred-frame scorer"),
        ("PPS4019_7_conservation", "zeta_i", "non-Hilbert stress/nonconservation projection", "zeta_i=0 or bounded with total stress closure", "conservation scorer"),
        ("PPS4019_8_Gdot", "Gdot_over_G", "D_t lnG in local branch", "4017 K_G theorem-zero or Gdot bound", "coupling drift scorer"),
    ]
    return [
        {
            "scorer_id": scorer_id,
            "quantity": quantity,
            "formula": formula,
            "pass_rule": pass_rule,
            "role": role,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for scorer_id, quantity, formula, pass_rule, role in rows
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("EHAUD4019_0_candidate_packet", "EH-only/R11 packet coherence", "PASS_CONDITIONAL", "branch is coherent as a theorem target", "can feed conditional rollup"),
        ("EHAUD4019_1_final_adoption", "packet adopted by full parent action", "NOT_FINAL", "local-GR claim remains blocked", "roll into synthesis or scorer"),
        ("EHAUD4019_2_R11_family", "all R11 families absent/topological/auxiliary-zero", "UNSIGNED", "delta_gamma_R11 and delta_beta_R11 live", "prove no-extra operator or score rows"),
        ("EHAUD4019_3_q_loc", "q_loc in PPN projector kernel", "UNSIGNED", "delta_beta_q_loc and finite-range PPN tail live", "prove projector-kernel theorem or score rows"),
        ("EHAUD4019_4_source_readout", "same source/readout frame", "CONDITIONAL", "beta/source/readout mismatch live", "bind to 4012/3988/4017"),
        ("EHAUD4019_5_private_zero", "private zero rollup treated as public proof", "REJECTED", "closure-only claim", "use as branch guide only"),
    ]
    return [
        {
            "audit_id": audit_id,
            "clause": clause,
            "current_status": status,
            "risk_if_open": risk,
            "next_action": action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, clause, status, risk, action in rows
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    cases = [
        ("CASE4019_0_full_EH_only_adopted", True, True, True, True, True, False, False, "EH-only/R11 no-extra branch adopted through O(U^2)"),
        ("CASE4019_1_candidate_not_final", False, True, True, True, True, False, False, "candidate branch coherent but not adopted as final parent action"),
        ("CASE4019_2_R11_tail_survives", True, False, True, True, True, False, False, "non-EH R11 operator family survives"),
        ("CASE4019_3_q_loc_tail_survives", True, True, False, True, True, False, False, "q_loc/Khat tail survives PPN projection"),
        ("CASE4019_4_readout_source_open", True, True, True, False, True, False, False, "same source/readout frame not closed"),
        ("CASE4019_5_vector_conservation_open", True, True, True, True, False, False, False, "preferred-frame/conservation vector not closed"),
        ("CASE4019_6_private_zero_overclaim", False, True, True, True, True, True, False, "private zero rollup used as public proof"),
        ("CASE4019_7_cancellation_attempt", True, False, False, False, False, False, True, "tries to cancel scorer rows"),
        ("CASE4019_8_scorer_only", False, False, False, False, False, False, False, "use PPN scorer because adoption clauses unsigned"),
    ]
    return [
        {
            "case_id": case_id,
            "adopted": adopted,
            "R11_zero": r11_zero,
            "q_loc_zero": qloc_zero,
            "source_readout": source_readout,
            "vector_conservation": vector_conservation,
            "private_zero_overclaim": private_zero,
            "cancellation_attempt": cancellation,
            "description": description,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for case_id, adopted, r11_zero, qloc_zero, source_readout, vector_conservation, private_zero, cancellation, description in cases
    ]


def truthy(row: dict[str, Any], key: str) -> bool:
    return str(row[key]).lower() == "true" if isinstance(row[key], str) else bool(row[key])


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in cases:
        if truthy(row, "private_zero_overclaim"):
            owner = "PRIVATE_ZERO_ROLLUP_OVERCLAIM_REJECTED"
            residual = "adoption_or_scorer_required"
            claim = "NO_LOCAL_GR_CLAIM"
            action = "use private zero only as branch guide until adoption/scorer evidence exists"
        elif truthy(row, "cancellation_attempt"):
            owner = "PPN_SCORER_CANCELLATION_REJECTED"
            residual = "Delta_PPN_abs_no_cancellation"
            claim = "NO_PPN_PASS"
            action = "absolute-sum scorer rows"
        elif not truthy(row, "adopted"):
            owner = "EH_ONLY_BRANCH_NOT_ADOPTED"
            residual = "PPS4019_SCORER_REQUIRED"
            claim = "NO_LOCAL_GR_PROMOTION"
            action = "adopt parent branch explicitly or run scorer rows"
        elif not truthy(row, "R11_zero"):
            owner = "R11_OPERATOR_TAIL_BLOCKED"
            residual = "delta_gamma_R11+delta_beta_R11"
            claim = "NO_GAMMA_BETA_CLAIM"
            action = "prove no-extra R11 theorem or fill R11 scorer coefficients"
        elif not truthy(row, "q_loc_zero"):
            owner = "QLOC_PPN_TAIL_BLOCKED"
            residual = "delta_beta_q_loc+alpha_lambda"
            claim = "NO_BETA_R10_LOCAL_GR_CLAIM"
            action = "prove PPN-projector kernel or score q_loc tail"
        elif not truthy(row, "source_readout"):
            owner = "SOURCE_READOUT_BRANCH_BLOCKED"
            residual = "delta_beta_source+delta_readout_frame"
            claim = "NO_SOURCE_NORMALIZED_PPN_CLAIM"
            action = "bind same source/readout frame and Hilbert current origin"
        elif not truthy(row, "vector_conservation"):
            owner = "FULL_VECTOR_BLOCKED"
            residual = "alpha_i+xi+zeta_i"
            claim = "NO_FULL_LOCAL_GR_CLAIM"
            action = "close preferred-frame/conservation rows or score them"
        elif row["case_id"] == "CASE4019_0_full_EH_only_adopted":
            owner = "CONDITIONAL_EH_ONLY_LOCAL_GR_LOCK"
            residual = "R11_QLOC_READOUT_SOURCE_VECTOR_ZERO_IF_ADOPTED"
            claim = "LOCAL_GR_CONDITIONAL_ONLY_NOT_PUBLIC_CLAIM"
            action = "roll up conditional local-GR branch and identify remaining adoption evidence"
        else:
            owner = "PPN_SCORER_NONCLAIM"
            residual = "FULL_SCORER_VECTOR_REQUIRED"
            claim = "NO_CLAIM"
            action = "source theorem-zero or numeric rows"
        rows.append(
            {
                "case_id": row["case_id"],
                "owner_status": owner,
                "residual_result": residual,
                "claim_result": claim,
                "next_action": action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4019_0_constructive_gate", "write EH-only/R11 no-extra adoption clauses", "this is the exact parent-action condition needed by 4018", "conditional route becomes explicit"),
        ("DEC4019_1_no_final_adoption", "do not claim final parent adoption yet", "the branch is coherent but still conditional in the full corpus", "claim gates stay false"),
        ("DEC4019_2_scorer_interface", "emit PPN residual scorer rows", "any failed adoption clause becomes gamma/beta/q_loc/vector scorer input", "testability improves"),
        ("DEC4019_3_reject_private_zero_overclaim", "private zero rollup is not proof", "ZERO_IN_PRIVATE_LOCAL_BRANCH requires adoption/scorer evidence", "closure-only route blocked"),
        ("DEC4019_4_next", f"move to {NEXT_DOC}", "next step should roll up the conditional local-GR branch or perform first executable PPN score", "turns theorem stack into a decision dashboard"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "effect": effect,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, rationale, effect in rows
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CLAIM4019_0_EH_only", "EH-only/R11 branch adopted", False, "candidate clauses written but not final parent adoption"),
        ("CLAIM4019_1_gamma_beta", "gamma=beta=1", False, "conditional on R11/q_loc/source/readout closure"),
        ("CLAIM4019_2_full_PPN", "full PPN pass", False, "scorer rows are not theorem-zero/numeric scored"),
        ("CLAIM4019_3_local_GR", "local GR recovery", False, "requires 4020 rollup/scorer evidence"),
        ("CLAIM4019_4_private_zero", "private zero rollup as claim", False, "explicitly rejected"),
    ]
    return [
        {
            "claim_id": claim_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for claim_id, claim, allowed, reason in gates
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4019_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "roll up the conditional local-GR branch from 4015-4019 and either identify the exact remaining adoption evidence or perform the first executable PPN score from the scorer rows",
            "success_condition": "every local-GR gate is labelled theorem-zero, adopted-conditional, or executable residual with claim gates still false unless all evidence is actually complete",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "EH-only/R11 no-extra-operator adoption gate constructed and PPN residual scorer rows emitted; local-GR claim remains blocked pending final adoption or scorer evidence.",
            "claim_allowed": False,
            "next_doc": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["needle_found"])
    lines = [
        "# 4019 - EH-Only R11 No-Extra Operator Adoption Or PPN Residual Scorer",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "This checkpoint states the exact operator gate behind the 4018 PPN theorem.",
        "",
        "The candidate local branch is:",
        "",
        "`S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter+S_EM+dB_proper+S_topological`.",
        "",
        "The no-extra condition is:",
        "",
        "`Allowed(O_R11^{<=2PN})={topological, exact, auxiliary-double-zero, Sigma_loc-selected-zero}`.",
        "",
        "If signed, `DeltaE_MTS^{(1)}=DeltaE_MTS^{(2)}=0`, so `delta_gamma_R11=delta_beta_R11=0`.",
        "",
        "## PPN Scorer",
        "",
        "If any adoption clause fails, the branch falls into the scorer:",
        "",
        "`Delta_PPN_abs_4019 = |delta_gamma_R11|+|delta_gamma_readout|+|delta_gamma_frame|+|delta_gamma_source|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary_domain|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|`.",
        "",
        "Private zero rollups are explicitly not enough for a claim; they only guide the branch.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: owner=`{row['owner_status']}`, residual=`{row['residual_result']}`, claim=`{row['claim_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "The route is now concrete: local GR can be conditionally obtained if the parent action really has no non-EH R11/q_loc operator through second order. If not, the scorer catches the failure component by component. No closure magic, no fitted-GM repair job.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4019 - EH-Only R11 No-Extra Operator Gate"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: the exact 2PN operator gate is now explicit: `S_loc^{{<=2PN}}=S_EH[g_obs;kappa_*]+S_matter+S_EM+dB_proper+S_topological`.
- No-extra condition: `Allowed(O_R11^{{<=2PN}})={{topological, exact, auxiliary-double-zero, Sigma_loc-selected-zero}}`; if signed, `DeltaE_MTS^{{(1)}}=DeltaE_MTS^{{(2)}}=0`, so `delta_gamma_R11=delta_beta_R11=0`.
- q_loc condition: PPN projectors must annihilate `q_loc_Khat` through O(U^2), otherwise `delta_beta_q_loc` and finite-range tails stay live.
- Scorer fallback: `Delta_PPN_abs_4019 = |delta_gamma_R11|+|delta_gamma_readout|+|delta_gamma_frame|+|delta_gamma_source|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary_domain|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|`.
- Guard: private zero rollups are not public proof; branch adoption or scorer evidence is required.
- No claim: local GR remains conditional/nonclaim pending 4020 rollup or first executable score.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4019 - EH-Only R11 No-Extra Operator Gate" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    scorer: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4019_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4019_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, clause_id in enumerate(
        ["EHA4019_0_action_domain", "EHA4019_1_R11_absent", "EHA4019_2_q_loc_absent", "EHA4019_3_readout_frame", "EHA4019_4_source_slot", "EHA4019_5_status"],
        start=2,
    ):
        add(f"VAL4019_{idx:02d}_adoption", any(row["clause_id"] == clause_id for row in adoption), f"{clause_id} present")
    for idx, theorem_id in enumerate(
        ["NOX4019_0_operator_domain_theorem", "NOX4019_1_q_loc_projector_zero", "NOX4019_2_EH_PPN_solution", "NOX4019_3_failure_to_scorer", "NOX4019_4_no_private_rollup_claim"],
        start=8,
    ):
        add(f"VAL4019_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    for idx, scorer_id in enumerate(
        ["PPS4019_0_master", "PPS4019_1_delta_gamma_R11", "PPS4019_2_delta_beta_R11", "PPS4019_3_delta_beta_q_loc", "PPS4019_4_delta_beta_source", "PPS4019_6_preferred_frame", "PPS4019_7_conservation"],
        start=13,
    ):
        add(f"VAL4019_{idx:02d}_scorer", any(row["scorer_id"] == scorer_id for row in scorer), f"{scorer_id} present")
    for idx, audit_id in enumerate(
        ["EHAUD4019_1_final_adoption", "EHAUD4019_2_R11_family", "EHAUD4019_3_q_loc", "EHAUD4019_5_private_zero"],
        start=20,
    ):
        add(f"VAL4019_{idx:02d}_audit", any(row["audit_id"] == audit_id for row in audit), f"{audit_id} present")
    lookup = {row["case_id"]: row for row in results}
    add("VAL4019_24_full_case", lookup["CASE4019_0_full_EH_only_adopted"]["owner_status"] == "CONDITIONAL_EH_ONLY_LOCAL_GR_LOCK", "full EH-only case locks conditionally")
    add("VAL4019_25_not_final", lookup["CASE4019_1_candidate_not_final"]["owner_status"] == "EH_ONLY_BRANCH_NOT_ADOPTED", "candidate not-final remains blocked")
    add("VAL4019_26_R11_tail", "delta_gamma_R11" in lookup["CASE4019_2_R11_tail_survives"]["residual_result"], "R11 tail routed")
    add("VAL4019_27_qloc_tail", "delta_beta_q_loc" in lookup["CASE4019_3_q_loc_tail_survives"]["residual_result"], "q_loc tail routed")
    add("VAL4019_28_source_readout", "delta_beta_source" in lookup["CASE4019_4_readout_source_open"]["residual_result"], "source/readout failure routed")
    add("VAL4019_29_vector", "alpha_i" in lookup["CASE4019_5_vector_conservation_open"]["residual_result"], "vector/conservation failure routed")
    add("VAL4019_30_private_zero", lookup["CASE4019_6_private_zero_overclaim"]["owner_status"] == "PRIVATE_ZERO_ROLLUP_OVERCLAIM_REJECTED", "private zero overclaim rejected")
    add("VAL4019_31_cancellation", lookup["CASE4019_7_cancellation_attempt"]["owner_status"] == "PPN_SCORER_CANCELLATION_REJECTED", "cancellation rejected")
    add("VAL4019_32_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4019_33_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4019_34_doc_exists", DOC_PATH.exists() and "Allowed(O_R11" in read_text(DOC_PATH), "document written with no-extra operator gate")
    add("VAL4019_35_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4019_36_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4019_37_compile", compile_ok, "script compiles")
    add("VAL4019_38_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [
        sources,
        adoption,
        theorem,
        scorer,
        audit,
        results,
        read_csv(OUTPUTS["decision"]),
        read_csv(OUTPUTS["claim_gate"]),
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4019_39_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4019_40_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4019_41_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4019_42_scorer_formula", "Delta_PPN_abs_4019" in read_text(DOC_PATH), "scorer formula recorded")
    add("VAL4019_43_next_rollup", "conditional local-GR branch" in read_text(OUTPUTS["next"]), "rollup/scorer next target recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    adoption = adoption_rows(timestamp)
    theorem = theorem_rows(timestamp)
    scorer = scorer_rows(timestamp)
    audit = audit_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["adoption"], adoption)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["scorer"], scorer)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, adoption, theorem, scorer, audit, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4019 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
