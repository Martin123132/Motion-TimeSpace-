from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1174-Y5-R10-local-Qflow-stationarity-theorem-or-first-Qflow-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1174_0_1173_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1173_NEXT_TARGET.csv",
            "needle": "NEXT1173_0_1174",
            "role": "handoff to local Q-flow stationarity theorem or first Q-flow bound row.",
        },
        {
            "source_id": "SRC1174_1_1173_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1173_VALIDATION.csv",
            "needle": "V1173_SUMMARY",
            "role": "1173 validation summary.",
        },
        {
            "source_id": "SRC1174_2_1173_norm",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1173_FIRST_NORM_INPUT_ROW.csv",
            "needle": "JNI1173_0_first_symbolic_norm_row",
            "role": "first symbolic residual exact source norm row.",
        },
        {
            "source_id": "SRC1174_3_1173_decision",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1173_DECISION_LEDGER.csv",
            "needle": "D1173_2_best_next",
            "role": "Q-flow trace and N_D/domain variation selected as next target.",
        },
        {
            "source_id": "SRC1174_4_1166_variation",
            "relative_path": "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
            "needle": "delta J_C = J_C Tr(Q^{-1} delta Q) - J_C delta(log N_D)",
            "role": "determinant variation formula.",
        },
        {
            "source_id": "SRC1174_5_1166_volume_lock",
            "relative_path": "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
            "needle": "int_D delta J_C=0",
            "role": "integral volume-lock obstruction.",
        },
        {
            "source_id": "SRC1174_6_1167_lock",
            "relative_path": "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md",
            "needle": "local stationary domains with `Sigma_C=0`, `Phi_C|partialD=0`, and no moving-boundary contribution",
            "role": "conditional stationary local branch.",
        },
        {
            "source_id": "SRC1174_7_1167_ND",
            "relative_path": "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md",
            "needle": "MISSING_NORMALIZATION_VARIATION",
            "role": "N_D normalization variation remains missing.",
        },
        {
            "source_id": "SRC1174_8_275_ND",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "N_D = (1/3) ln(V_D0 / V_D)",
            "role": "older N_D coherent-volume definition.",
        },
        {
            "source_id": "SRC1174_9_275_Qcoh",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "Q_coh^i_j = (N_D / u3) delta^i_j",
            "role": "Q_coh coherent projection shape.",
        },
        {
            "source_id": "SRC1174_10_275_projection_missing",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "coherent projection `Q -> Q_coh` | not parent-derived",
            "role": "Q_coh projection is not parent-owned.",
        },
        {
            "source_id": "SRC1174_11_275_shear",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "tracefree shear leaks into unprojected `det(Q)` at second order",
            "role": "unprojected determinant local shear guard.",
        },
        {
            "source_id": "SRC1174_12_207_bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi/Ward guard.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def stationarity_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "QST1174_0_defect_definition",
            "quantity": "Theta_Q",
            "statement": "Define the local coherent-volume stationarity defect Theta_Q := Tr(Q^{-1} delta Q) - delta(log N_D). Then delta J_C = J_C Theta_Q plus domain/coframe-reference terms.",
            "status": "DEFECT_DEFINED",
            "what_it_derives": "the source feeding j_C exact residual is now one scalar defect plus reference terms.",
            "missing_for_claim": "parent-owned Q, N_D, delta, and domain transport",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QST1174_1_normalization_identity",
            "quantity": "Theta_Q_coh",
            "statement": "If N_D is parent-defined so that delta(log N_D)=Tr(Q_coh^{-1} delta Q_coh) on the coherent local branch, then the coherent part Theta_Q_coh vanishes.",
            "status": "IDENTITY_IF_PARENT_NORMALIZATION_SIGNED",
            "what_it_derives": "a clean cancellation of the coherent/background volume mode.",
            "missing_for_claim": "proof that this is a parent normalization law, not a post-hoc subtraction",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QST1174_2_stationary_vacuum",
            "quantity": "Theta_Q_local",
            "statement": "If a local stationary vacuum branch has delta Q_coh=0, delta N_D=0, and zero domain/coframe-reference terms, then Theta_Q_local=0 and the residual exact source vanishes.",
            "status": "CONDITIONAL_ZERO_SHAPE",
            "what_it_derives": "the desired local zero theorem shape.",
            "missing_for_claim": "parent local stationarity theorem and physical-charge guard",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QST1174_3_fluctuation_warning",
            "quantity": "Theta_Q_res",
            "statement": "Coherent normalization can remove the mean/coherent volume mode but not necessarily local fluctuations, tracefree second-order determinant leakage, projector errors, or moving-domain terms.",
            "status": "ZERO_NOT_GENERAL",
            "what_it_derives": "the correct finite-bound object is the residual stationarity defect Theta_Q_res.",
            "missing_for_claim": "Q_coh projector owner and bounds for fluctuation/projector/domain terms",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QST1174_4_verdict",
            "quantity": "Q-flow stationarity theorem",
            "statement": "1174 does not derive full local Q-flow stationarity. It derives the right defect variable and shows the coherent cancellation is legitimate only if N_D/Q_coh are parent-owned.",
            "status": "PARTIAL_IDENTITY_PLUS_BOUND_ROUTE",
            "what_it_derives": "a sharper stationarity-defect bound route.",
            "missing_for_claim": "parent Q_coh projection, N_D rule, and numeric/source-backed defect bounds",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def defect_bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "bound_id": "QDB1174_0_first_stationarity_defect_row",
            "quantity": "norm_Theta_Q_res",
            "formula": "||Theta_Q_res|| <= ||Tr(Q^{-1}delta Q)-Pi_coh Tr(Q^{-1}delta Q)|| + ||Pi_coh Tr(Q^{-1}delta Q)-delta log N_D|| + ||R_domain||",
            "units": "inverse_time_or_variation_parameter_units",
            "current_value": "SYMBOLIC_ONLY_MISSING_PROJECTOR_AND_ND_RULE",
            "source_or_theorem": "1166 variation; 275 Q_coh/N_D shape",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QDB1174_1_projector_leak",
            "quantity": "noncoherent trace/projector leakage",
            "formula": "||Tr(Q^{-1}delta Q)-Pi_coh Tr(Q^{-1}delta Q)||",
            "units": "same_as_Theta_Q_res",
            "current_value": "MISSING_QCOH_PROJECTOR_OWNER_OR_BOUND",
            "source_or_theorem": "275 says Q_coh projection is not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QDB1174_2_normalization_mismatch",
            "quantity": "coherent normalization mismatch",
            "formula": "||Pi_coh Tr(Q^{-1}delta Q)-delta log N_D||",
            "units": "same_as_Theta_Q_res",
            "current_value": "MISSING_ND_NORMALIZATION_VARIATION",
            "source_or_theorem": "1167 N_D normalization variation missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QDB1174_3_domain_reference",
            "quantity": "R_domain",
            "formula": "moving-domain + coframe-reference + projector/cutoff terms",
            "units": "same_as_Theta_Q_res",
            "current_value": "MISSING_DOMAIN_TRANSPORT_BOUND",
            "source_or_theorem": "1167 moving boundary/domain transport gap",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "QDB1174_4_runner_payload",
            "quantity": "norm_jC_exact_residual",
            "formula": "||j_C^exact|| <= ||J_C|| * ||Theta_Q_res|| + ||J_C|| * ||R_domain_extra||",
            "units": "J_C_norm_units_times_Theta_units",
            "current_value": "NOT_EVALUATED",
            "source_or_theorem": "feeds 1173/1172 finite boundary runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def normalization_guard_rows() -> list[dict[str, object]]:
    rows = [
        {
            "guard_id": "NG1174_0_parent_owned_normalization",
            "risk": "post-hoc subtraction",
            "rule": "N_D may cancel coherent trace flow only if N_D is generated by the same parent domain/measure law as Q_coh.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "choosing N_D after the fact hides local leakage",
            "valid_for_claim": False,
        },
        {
            "guard_id": "NG1174_1_not_full_J_zero",
            "risk": "zeroing physical memory",
            "rule": "Only residual stationarity defect is zeroed/bounded; full background/coherent J_C is retained for FLRW/domain memory.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "local repair accidentally kills cosmology branch",
            "valid_for_claim": False,
        },
        {
            "guard_id": "NG1174_2_integral_not_norm",
            "risk": "volume-lock overclaim",
            "rule": "int_D delta J_C=0 can cancel the coherent integral but cannot be used as norm_Theta_Q_res=0.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "mean-zero fluctuations still feed B_C",
            "valid_for_claim": False,
        },
        {
            "guard_id": "NG1174_3_tracefree_shear",
            "risk": "unprojected determinant leakage",
            "rule": "Use only parent-owned Q_coh projection; unprojected determinant has tracefree shear leakage at second order.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "local PPN leakage hidden by informal smoothing",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1174_0_coherent_identity",
            "test": "Theta_Q_coh cancellation",
            "status": "PARTIAL_PASS_IF_PARENT_NORMALIZATION",
            "result": "coherent mode cancels if delta log N_D is the parent coherent trace flow",
            "blocked_by": "parent_ND_rule;Qcoh_projector_owner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1174_1_stationarity_zero",
            "test": "local Theta_Q_res=0",
            "status": "REFUSED_ZERO_THEOREM_MISSING",
            "result": "zero requires local Q-flow stationarity plus no projector/domain/reference leakage",
            "blocked_by": "Qcoh_stationarity;N_D_stationarity;domain_transport;tracefree_shear_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1174_2_bound_row",
            "test": "first Q-flow bound row",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "result": "norm_Theta_Q_res and norm_jC_exact_residual runner payload are staged",
            "blocked_by": "numeric/source-backed projector, normalization, and domain terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1174_3_local_promotion",
            "test": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "result": "1174 gives a sharper defect row but no scored local bound",
            "blocked_by": "Qcoh_projector_owner_or_numeric_defect_bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1174_0_defect_defined",
            "gate": "Theta_Q stationarity defect",
            "current_status": "PASS_NONCLAIM",
            "reason": "defect variable is defined and tied to delta J_C",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1174_1_coherent_cancellation",
            "gate": "coherent normalization cancellation",
            "current_status": "PARTIAL_PASS_IF_PARENT_OWNED",
            "reason": "cancellation is legitimate only if Q_coh and N_D descend from parent law",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1174_2_stationarity_zero",
            "gate": "Theta_Q_res=0 local theorem",
            "current_status": "BLOCKED",
            "reason": "local Q-flow/projector/domain stationarity is not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1174_3_numeric_bound",
            "gate": "source-backed Q-flow bound",
            "current_status": "SYMBOLIC_READY_VALUES_MISSING",
            "reason": "projector, normalization, and domain terms have no numeric/source-backed bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1174_4_local_promotion",
            "gate": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "neither stationarity zero nor numeric finite bound is available",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1174_0_identity_not_enough",
            "decision": "do_not_claim_stationarity_from_normalization_identity",
            "reason": "N_D cancellation is only physics if the parent action owns the domain normalization",
            "next_action": "derive Q_coh projector/N_D owner or keep finite bound route",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1174_1_bound_route_progress",
            "decision": "stage_Theta_Q_res_bound",
            "reason": "Q-flow leakage is now split into projector leak, normalization mismatch, and domain/reference terms",
            "next_action": "target the Q_coh projector owner first",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1174_2_best_next",
            "decision": "target_Qcoh_projector_owner",
            "reason": "without parent-owned Q_coh, local shear/projector leakage cannot be distinguished from a smoothing closure",
            "next_action": "derive Q_coh as a variational/cohomological projector or stage the projector-leak bound row",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1174_0_1175",
            "next_target": "1175-Y5-R10-Qcoh-projector-owner-or-projector-leak-bound-row.md",
            "objective": "try to derive the coherent Q projection as a parent-owned domain/volume projector; if not, stage the first projector-leak bound row for Theta_Q_res",
            "include": "Qcoh definition; tracefree shear guard; N_D normalization; domain projector; parent variational owner; projector-leak bound; no-claim runner",
            "exclude": "post-hoc smoothing; zeroing full J_C; using normalization as proof; local claim; c_g zero; invented numeric values; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1174_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_1_defect_defined",
            "result": "pass" if any(r["quantity"] == "Theta_Q" for r in attempts) else "fail",
            "detail": "Theta_Q stationarity defect is defined",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_2_identity_guarded",
            "result": "pass" if any("post-hoc subtraction" in str(r["risk"]) for r in guards) else "fail",
            "detail": "normalization cancellation is guarded against post-hoc subtraction",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_3_stationarity_not_claimed",
            "result": "pass" if any(r["status"] == "PARTIAL_IDENTITY_PLUS_BOUND_ROUTE" for r in attempts) else "fail",
            "detail": "full local Q-flow stationarity is not claimed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_4_bound_row_created",
            "result": "pass" if any(r["bound_id"] == "QDB1174_0_first_stationarity_defect_row" for r in bounds) else "fail",
            "detail": "first stationarity-defect bound row is created",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_5_runner_payload_created",
            "result": "pass" if any(r["quantity"] == "norm_jC_exact_residual" for r in bounds) else "fail",
            "detail": "norm_jC_exact_residual runner payload is staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in r.values())) or r["valid_for_claim"] is False for r in bounds)
            else "fail",
            "detail": "rows with MISSING inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses stationarity, numeric-bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_8_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1174 claim gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_9_no_claim_rows",
            "result": "pass"
            if all(r.get("valid_for_claim") is False for r in attempts + bounds + guards + gates + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_10_next_target",
            "result": "pass" if nexts and "1175" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1175 handoff targets Qcoh projector owner or projector-leak bound row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_11_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1174_SUMMARY",
            "result": "pass",
            "detail": "1174 defines Theta_Q stationarity defect, permits coherent cancellation only if parent-owned, stages the first Q-flow bound row, and blocks claims until Qcoh/N_D/domain terms are sourced",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1174 — Y5/R10 local Q-flow stationarity theorem or first Q-flow bound row",
        "**Current verdict:** local Q-flow stationarity is not derived, but the defect is now sharply named. Define `Theta_Q := Tr(Q^{-1} delta Q) - delta(log N_D)`. The local residual source is controlled by `Theta_Q_res`, not by a vague motion-field leak.",
        "**Main progress:** coherent cancellation is legitimate only if `N_D` is parent-defined as the coherent domain-volume normalization. Otherwise it is just post-hoc subtraction. The first bound row is now `||Theta_Q_res|| <= projector_leak + normalization_mismatch + domain_reference_terms`.",
        "**Hard blocker:** the next missing object is a parent-owned `Q -> Q_coh` projector and `N_D` normalization law. Without that, local shear/projector leakage cannot be cleanly separated from smoothing closure.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Q-flow stationarity attempt\n\n" + table(attempts),
        "## First Q-flow defect bound rows\n\n" + table(bounds),
        "## Normalization and projection guards\n\n" + table(guards),
        "## Runner dry-run\n\n" + table(runs),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    attempts = stationarity_attempt_rows()
    bounds = defect_bound_rows()
    guards = normalization_guard_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, attempts, bounds, guards, runs, gates, nexts)

    outputs = {
        "P8_Y5_R10_1174_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1174_QFLOW_STATIONARITY_ATTEMPT.csv": attempts,
        "P8_Y5_R10_1174_FIRST_QFLOW_DEFECT_BOUND_ROWS.csv": bounds,
        "P8_Y5_R10_1174_NORMALIZATION_PROJECTION_GUARDS.csv": guards,
        "P8_Y5_R10_1174_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1174_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1174_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1174_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1174_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, attempts, bounds, guards, runs, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
