from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1187-Y5-R10-compensator-divergence-inverse-or-Gamma-Khat-qnorm-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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
            "source_id": "SRC1187_0_1186_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1186_NEXT_TARGET.csv",
            "needle": "NEXT1186_0_1187",
            "role": "handoff to compensator divergence inverse or Gamma/Khat qnorm source.",
        },
        {
            "source_id": "SRC1187_1_1186_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1186_VALIDATION.csv",
            "needle": "V1186_SUMMARY",
            "role": "1186 validation summary.",
        },
        {
            "source_id": "SRC1187_2_1186_factor",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv",
            "needle": "RQB1186_2_operator_factorization",
            "role": "Ward-safe response factorization.",
        },
        {
            "source_id": "SRC1187_3_1186_div",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1186_WARD_SAFE_OPERATOR_INPUT_LEDGER.csv",
            "needle": "RQI1186_0_div_inverse",
            "role": "Div inverse norm missing.",
        },
        {
            "source_id": "SRC1187_4_1186_boundary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1186_WARD_SAFE_OPERATOR_INPUT_LEDGER.csv",
            "needle": "RQI1186_4_boundary_flux",
            "role": "boundary flux missing.",
        },
        {
            "source_id": "SRC1187_5_1186_qformula",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_NORM_SOURCE_ROWS.csv",
            "needle": "QNR1186_0_formula_row",
            "role": "q_loc formula row.",
        },
        {
            "source_id": "SRC1187_6_1010_metric",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_1_metric_response_identity",
            "role": "metric response identity missing.",
        },
        {
            "source_id": "SRC1187_7_1010_projector_boundary",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_5_projector_boundary",
            "role": "P_loc/boundary ownership missing.",
        },
        {
            "source_id": "SRC1187_8_207_hidden_force",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "That would hide an external force and fake conservation.",
            "role": "fake-conservation guard.",
        },
        {
            "source_id": "SRC1187_9_symbol_map",
            "relative_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "q_loc^nu = P_loc",
            "role": "q_loc formula and demotion requirement.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def compensator_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "CDI1187_0_parent_owner",
            "object": "C_q compensator sector",
            "statement": "A compensator is legitimate only if it is parent-owned or an explicitly retained auxiliary stress with metric variation included.",
            "result": "not parent-owned in current source chain",
            "status": "COMPENSATOR_NOT_PARENT_OWNED",
            "missing_for_claim": "S_comp or parent field equation for C_q",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CDI1187_1_divergence_inverse_condition",
            "object": "Div^{-1}",
            "statement": "On a compact domain, a right-inverse of divergence exists only after source compatibility and boundary conditions are specified.",
            "result": "conditional bound form: ||C_q|| <= C_D ||q_loc|| + B_boundary",
            "status": "CONDITIONAL_BOUND_FORM",
            "missing_for_claim": "domain geometry, gauge, boundary flux/no-flux, C_D source",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CDI1187_2_boundary_guard",
            "object": "boundary flux",
            "statement": "If bulk q_loc is compensated but boundary/symplectic flux remains, the local source-measure closure is still residual.",
            "result": "boundary term must be carried as B_q_boundary, not dropped",
            "status": "BOUNDARY_RESIDUAL_RETAINED",
            "missing_for_claim": "boundary no-flux theorem or radial/source-measure bound",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CDI1187_3_no_fake_conservation",
            "object": "Bianchi/Ward ledger",
            "statement": "A chosen compensator that merely cancels q_loc after readout would hide an external force and fake conservation.",
            "result": "compensator route remains nonclaim unless parent-selected before readout",
            "status": "FAKE_CONSERVATION_GUARD_ACTIVE",
            "missing_for_claim": "parent selection before fit/readout",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CDI1187_4_verdict",
            "object": "compensator/divergence inverse verdict",
            "statement": "1187 derives conditional compensator bounds but does not source a parent-owned compensator or divergence inverse.",
            "result": "route falls back to explicit q_loc norm source rows",
            "status": "COMPENSATOR_BOUND_NONCLAIM_QNORM_ROUTE_ACTIVE",
            "missing_for_claim": "S_comp, C_D, B_boundary, q_loc profile",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def qnorm_profile_rows() -> list[dict[str, object]]:
    rows = [
        {
            "profile_id": "GKP1187_0_Gamma_eff",
            "symbol": "Gamma_eff",
            "needed_profile": "Gamma_eff(Phi,g,boundary) on the PPN/local domain",
            "needed_units": "stress-density or compatible scalar-response units",
            "derivative_needed": "nabla^nu Gamma_eff",
            "current_status": "MISSING_PROFILE_AND_UNITS",
            "source_needed": "parent field definition or source-backed closure file",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "profile_id": "GKP1187_1_K_hat",
            "symbol": "K_hat^{mu nu}",
            "needed_profile": "K_hat^{mu nu}(Phi,g,boundary) on the PPN/local domain",
            "needed_units": "stress-tensor units compatible with Gamma_eff g^{mu nu}",
            "derivative_needed": "nabla_mu K_hat^{mu nu}",
            "current_status": "MISSING_PROFILE_AND_UNITS",
            "source_needed": "metric response or boundary/symplectic tensor source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "profile_id": "GKP1187_2_P_loc",
            "symbol": "P_loc",
            "needed_profile": "parent-owned local projector/domain representative",
            "needed_units": "projection operator",
            "derivative_needed": "commutation with derivative/readout or correction term",
            "current_status": "MISSING_PARENT_PROJECTOR_DOMAIN",
            "source_needed": "P_loc parent algebra, domain selector, boundary no-flux",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "profile_id": "GKP1187_3_q_loc_formula",
            "symbol": "q_loc^nu",
            "needed_profile": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "needed_units": "force/source-exchange residual units mapped to PPN arena",
            "derivative_needed": "all above derivatives and projector corrections",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "source_needed": "Gamma_eff, K_hat, P_loc rows complete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "profile_id": "GKP1187_4_qnorm",
            "symbol": "||q_loc||_PPN",
            "needed_profile": "PPN-domain norm, uncertainty, and source path",
            "needed_units": "arena-specific residual norm units",
            "derivative_needed": "not applicable after profile row",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "source_needed": "q_loc profile or theorem bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def bound_update_rows() -> list[dict[str, object]]:
    rows = [
        {
            "bound_id": "BUP1187_0_compensator_stress",
            "component": "C_q",
            "formula": "||C_q||_D <= C_D ||q_loc||_D + B_q_boundary",
            "closed_by_1187": "conditional bound structure",
            "still_missing": "C_D; B_q_boundary; ||q_loc||_D; parent owner",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BUP1187_1_scalar_response",
            "component": "q_trace",
            "formula": "|q_trace| <= ||P_scalar G_EH|| (C_D ||q_loc|| + B_q_boundary)",
            "closed_by_1187": "Ward-safe scalar response bound form",
            "still_missing": "P_scalar G_EH norm; C_D; ||q_loc||; B_q_boundary",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BUP1187_2_STF_response",
            "component": "q_TF",
            "formula": "||q_TF|| <= ||P_TF G_EH|| (C_D ||q_loc|| + B_q_boundary)",
            "closed_by_1187": "Ward-safe STF response bound form",
            "still_missing": "P_TF G_EH norm; C_D; ||q_loc||; B_q_boundary",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1187_0_compensator_owner",
            "claim": "C_q is parent-owned",
            "status": "BLOCKED_PARENT_COMPENSATOR_MISSING",
            "why": "no S_comp or parent auxiliary stress source exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1187_1_div_inverse_bound",
            "claim": "Div^{-1} bound is numeric/source-backed",
            "status": "BLOCKED_DOMAIN_BOUNDARY_OPERATOR_MISSING",
            "why": "domain geometry, boundary condition, and operator norm are absent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1187_2_boundary_no_flux",
            "claim": "q_loc boundary/symplectic flux is silent",
            "status": "BLOCKED_BOUNDARY_NO_FLUX_MISSING",
            "why": "bulk compensation does not eliminate boundary leakage",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1187_3_Gamma_Khat_profiles",
            "claim": "Gamma_eff/K_hat/P_loc profiles are sufficient for qnorm",
            "status": "BLOCKED_PROFILE_ROWS_MISSING_VALUES",
            "why": "profile rows are staged but not filled with formulas, units, domains, or source paths",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1187_4_PPN_local",
            "claim": "PPN/local-GR score is allowed",
            "status": "BLOCKED_NO_LOCAL_CLAIM",
            "why": "compensator and qnorm routes are not scoreable",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1187_0_compensator_status",
            "decision": "conditional_compensator_bound_only",
            "reason": "right-inverse/divergence logic is valid only with domain and parent ownership; current corpus lacks both.",
            "next_action": "do not use compensator for claims until S_comp or operator norm is sourced.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1187_1_qnorm_status",
            "decision": "Gamma_Khat_Ploc_profile_rows_are_next_practical_route",
            "reason": "q_loc norm can be staged directly from its defining profiles if those are sourced.",
            "next_action": "hunt/source Gamma_eff formula, K_hat formula, and P_loc domain/projection files.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1187_2_best_next",
            "decision": "source_Gamma_eff_Khat_Ploc_before_more_operator_math",
            "reason": "without profiles, operator bounds multiply an unknown q_loc norm.",
            "next_action": "1188 should build the Gamma/Khat/P_loc profile source ledger or demote q_loc to explicit empirical residual row.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1187_0_1188",
            "next_target": "1188-Y5-R10-Gamma-Khat-Ploc-profile-source-ledger-or-q_loc-demotion-row.md",
            "objective": "source Gamma_eff, K_hat, and P_loc profiles/units/domains needed for q_loc norm; if unavailable, demote q_loc to an explicit empirical residual row for PPN/R10/clock/orbital tests",
            "include": "Gamma_eff formula; K_hat formula; P_loc/domain; derivative conventions; units; q_loc norm row; no-claim validation",
            "exclude": "q_loc zero claim; parent compensator claim; invented profiles; PPN pass; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    compensator: list[dict[str, object]],
    profiles: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1187_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_1_compensator_nonclaim",
            "result": "pass" if any(r["status"] == "COMPENSATOR_NOT_PARENT_OWNED" for r in compensator) else "fail",
            "detail": "parent-owned compensator is not claimed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_2_div_bound_form",
            "result": "pass" if any(r["status"] == "CONDITIONAL_BOUND_FORM" for r in compensator) else "fail",
            "detail": "conditional divergence-inverse bound form is recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_3_profile_rows_complete_set",
            "result": "pass"
            if {r["symbol"] for r in profiles} >= {"Gamma_eff", "K_hat^{mu nu}", "P_loc", "q_loc^nu", "||q_loc||_PPN"}
            else "fail",
            "detail": "Gamma_eff, K_hat, P_loc, q_loc, and qnorm source rows are staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_4_bounds_nonclaim",
            "result": "pass" if len(bounds) >= 3 and all(r["claim_allowed"] is False for r in bounds) else "fail",
            "detail": "compensator/scalar/STF bound rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_5_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in profiles + bounds)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_6_gates_nonclaim",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_7_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in compensator + profiles + bounds + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_8_next_target",
            "result": "pass" if nexts and "1188" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1188 handoff targets Gamma/Khat/P_loc profile sourcing or q_loc demotion",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_9_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1187_SUMMARY",
            "result": "pass",
            "detail": "1187 derives conditional compensator/divergence-inverse bounds, refuses parent compensator and no-flux claims, stages Gamma_eff/K_hat/P_loc qnorm source rows, and hands off to profile sourcing or q_loc demotion",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    compensator: list[dict[str, object]],
    profiles: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1187 - Y5/R10 compensator divergence inverse or Gamma/Khat qnorm source",
        "**Current verdict:** the compensator route has a valid conditional bound shape, but it is not parent-owned and cannot be used for claims. The practical route is now sourcing `Gamma_eff`, `K_hat`, and `P_loc` profiles for an explicit `q_loc` norm.",
        "**Main progress:** the conditional bound `||C_q|| <= C_D ||q_loc|| + B_q_boundary` and its scalar/STF responses are written, with boundary flux retained rather than hidden.",
        "**Hard blocker:** no `S_comp`, no `Div^{-1}` norm, no boundary no-flux theorem, and no filled `Gamma_eff/K_hat/P_loc` profile rows exist.",
        "**No claim:** no q_loc zero, local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Compensator/divergence-inverse attempt\n\n" + table(compensator),
        "## Gamma/Khat/P_loc qnorm source rows\n\n" + table(profiles),
        "## Bound update rows\n\n" + table(bounds),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    compensator = compensator_rows()
    profiles = qnorm_profile_rows()
    bounds = bound_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, compensator, profiles, bounds, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1187_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1187_COMPENSATOR_DIVERGENCE_INVERSE_ATTEMPT.csv": compensator,
        "P8_Y5_R10_1187_GAMMA_KHAT_PLOC_QNORM_SOURCE_ROWS.csv": profiles,
        "P8_Y5_R10_1187_BOUND_UPDATE_ROWS.csv": bounds,
        "P8_Y5_R10_1187_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1187_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1187_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1187_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, compensator, profiles, bounds, gates, decisions, validations, nexts)

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
