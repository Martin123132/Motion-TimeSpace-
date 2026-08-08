from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "987-Y5-R10-Coulomb-to-alphaEM-normal-form-or-parent-zero-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "986_doc",
            "path": "986-Y5-R10-Ci-to-MTS-slot-map-or-parent-zero-theorem.md",
            "role": "handoff selecting Coulomb-to-alphaEM normal form",
            "needle": "DEC986_2_best_next",
        },
        {
            "source_id": "986_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_986_CI_TO_MTS_SLOT_MAP.csv",
            "role": "C_C to b_theta_alpha route",
            "needle": "CIMAP986_0_C_C_to_btheta_alpha",
        },
        {
            "source_id": "986_obligations",
            "path": "source-intake/mts_residuals/P8_Y5_R10_986_PROOF_OBLIGATIONS.csv",
            "role": "EM normal-form proof obligation",
            "needle": "OB986_0_EM_normal_form",
        },
        {
            "source_id": "984_imported_basis",
            "path": "source-intake/mts_residuals/P8_Y5_R10_984_IMPORTED_PHENOMENOLOGICAL_BASIS.csv",
            "role": "imported Coulomb charge basis",
            "needle": "IMP984_2_electromagnetic_Coulomb",
        },
        {
            "source_id": "983_delta",
            "path": "source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv",
            "role": "MICROSCOPE Coulomb proxy contrast",
            "needle": "DEL983_coulomb_proxy",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "b_theta alpha_EM slot and parent matter contract",
            "needle": "d_ln_alpha_EM_dXhat",
        },
        {
            "source_id": "448_doc",
            "path": "448-constant-sector-universality-theorem-attempt.md",
            "role": "constant-sector hazard and forbidden alpha_EM(Z) vertices",
            "needle": "alpha_EM(Z)",
        },
        {
            "source_id": "240_doc",
            "path": "240-universal-coupling-parent-contract-or-local-bound-data-runner.md",
            "role": "older alpha_EM(Z) direct memory-probe hazard",
            "needle": "alpha_EM(Z)",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def em_normal_form_rows() -> list[dict[str, str]]:
    return [
        {
            "form_id": "EMNF987_0_parent_zero_constant_EM",
            "normal_form": "EM sector is part of ordinary matter with constant representation data",
            "action_shape": "S_EM=-1/4 int sqrt(-g_obs) Z_F(theta_EM) F_mn F^mn with L_X theta_EM=0",
            "Coulomb_effect": "C_C=0 for local MTS X direction",
            "MTS_slot": "none; parent-zero branch",
            "status": "RELATIVE_ZERO_THEOREM",
            "missing_for_claim": "parent-signed constant-sector trivial action and no marker/source-weight term",
            "valid_for_claim": "false",
        },
        {
            "form_id": "EMNF987_1_finite_alphaEM_X",
            "normal_form": "EM coupling depends on local MTS branch",
            "action_shape": "Z_F=Z_F(Xhat), alpha_EM(Xhat)=alpha_0/Z_F(Xhat)",
            "Coulomb_effect": "C_C = P_C_alpha * b_alpha * profile_X",
            "MTS_slot": "b_theta_alpha_EM",
            "status": "FINITE_ROUTE_IDENTIFIED_NOT_DERIVED",
            "missing_for_claim": "parent EM coupling term, P_C_alpha sensitivity, profile_X normalization",
            "valid_for_claim": "false",
        },
        {
            "form_id": "EMNF987_2_marker_dependent_alpha",
            "normal_form": "EM coupling depends on quotient/material marker",
            "action_shape": "alpha_EM=alpha_EM(I_Q,m,readout_projector)",
            "Coulomb_effect": "C_C may be nonzero but belongs to marker/closure branch",
            "MTS_slot": "b_m or forbidden post-readout branch",
            "status": "FORBIDDEN_OR_RETAINED_MARKER_ROUTE",
            "missing_for_claim": "marker taxonomy/no-extension theorem or explicit finite b_m bound",
            "valid_for_claim": "false",
        },
        {
            "form_id": "EMNF987_3_emergent_EM_geometry_locked",
            "normal_form": "EM is emergent/geometry-locked with no independent alpha_EM X-variation",
            "action_shape": "A_mu and alpha_EM are derived observables of the same parent geometry/readout, with D_X alpha_EM=0 in local branch",
            "Coulomb_effect": "C_C=0 if the emergent EM map is parent-signed",
            "MTS_slot": "parent-zero or derived EM-lock branch",
            "status": "PROMISING_BUT_NOT_PARENT_SIGNED",
            "missing_for_claim": "actual emergent EM parent map plus Maxwell/fine-structure limit",
            "valid_for_claim": "false",
        },
        {
            "form_id": "EMNF987_4_verdict",
            "normal_form": "Coulomb-to-alphaEM status",
            "action_shape": "only EMNF987_1 gives finite C_C; EMNF987_0/3 kill it; EMNF987_2 demotes it to marker",
            "Coulomb_effect": "finite WEP Coulomb channel is b_theta_alpha_EM, not b_kappa",
            "MTS_slot": "b_theta_alpha_EM first",
            "status": "CLEAN_FINITE_ROUTE_BUT_PARENT_UNSIGNED",
            "missing_for_claim": "EM normal form and profile normalization",
            "valid_for_claim": "false",
        },
    ]


def coulomb_projection_rows() -> list[dict[str, str]]:
    return [
        {
            "projection_id": "CPROJ987_0_symbolic_map",
            "formula": "eta_Coulomb = DeltaQ_C * P_C_alpha * b_alpha * profile_X",
            "known_from_983": "DeltaQ_C = -2.574514671e+00 for TiAlloy - PtRh10 proxy",
            "known_from_986": "C_C routes to b_theta_alpha_EM",
            "missing_inputs": "P_C_alpha,b_alpha,profile_X",
            "claim_status": "not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "CPROJ987_1_identity_debug_link",
            "formula": "if P_C_alpha*profile_X=1, then |b_alpha| <= 2.715851682e-15",
            "known_from_983": "IB983_coulomb_proxy identity debug bound",
            "known_from_986": "identity assumption is not an MTS map",
            "missing_inputs": "proof P_C_alpha*profile_X=1 or actual value",
            "claim_status": "debug_only",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "CPROJ987_2_clock_EM_link",
            "formula": "same b_alpha should also face clock/fine-structure tests: d ln alpha_EM/dXhat",
            "known_from_622": "d_ln_alpha_EM_dXhat is an existing b_theta prior slot",
            "known_from_986": "WEP Coulomb and clocks must not be scored independently if they share b_alpha",
            "missing_inputs": "clock sensitivity matrix and local Xhat environment profile",
            "claim_status": "cross_arena_coupling_needed",
            "valid_for_claim": "false",
        },
    ]


def parent_zero_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PZG987_0_constant_EM",
            "condition": "alpha_EM is representation data with trivial local MTS action",
            "math_form": "L_X alpha_EM=0",
            "result_if_signed": "C_C=0",
            "current_status": "not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PZG987_1_no_direct_vertex",
            "condition": "parent matter action has no alpha_EM(X), alpha_EM(I_Q), or alpha_EM(m) vertex",
            "math_form": "partial_X Z_F = partial_IQ Z_F = partial_m Z_F = 0",
            "result_if_signed": "no direct EM WEP/clock source",
            "current_status": "forbidden_policy_only",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PZG987_2_emergent_EM_lock",
            "condition": "if EM is emergent, its fine-structure readout is local-X silent",
            "math_form": "D alpha_EM[Dq(X)] = 0",
            "result_if_signed": "C_C=0 without separately postulating constant alpha",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PZG987_3_verdict",
            "condition": "parent-zero branch for Coulomb WEP channel",
            "math_form": "EMNF987_0 or EMNF987_3 plus source-universality gates",
            "result_if_signed": "C_C theorem-zero",
            "current_status": "relative_only",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE987_0_route",
            "claim": "Coulomb route maps to b_theta_alpha_EM rather than b_kappa",
            "gate_pass": "route_identified",
            "claim_allowed": "false",
            "why_not": "route identity is not a numeric coefficient bound",
        },
        {
            "gate_id": "CGATE987_1_btheta_bound",
            "claim": "MICROSCOPE bounds b_theta_alpha_EM",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "P_C_alpha and profile_X are missing",
        },
        {
            "gate_id": "CGATE987_2_parent_zero",
            "claim": "C_C is theorem-zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "constant/emergent EM lock is not parent-signed",
        },
        {
            "gate_id": "CGATE987_3_WEP_clock_combined",
            "claim": "WEP+clock alpha_EM branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "clock sensitivity/environment profile not connected",
        },
        {
            "gate_id": "CGATE987_4_local_GR",
            "claim": "local-GR branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "EM route is a finite/nonclaim map audit",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC987_0_route",
            "topic": "Coulomb WEP channel",
            "result": "routes_to_btheta_alpha_not_bkappa",
            "reason": "Coulomb binding is an EM/fine-structure matter-constant sensitivity",
            "next_action": "connect this slot to clock/fine-structure constraints before numeric scoring",
        },
        {
            "decision_id": "DEC987_1_zero",
            "topic": "parent-zero branch",
            "result": "possible_but_unsigned",
            "reason": "constant/emergent EM lock could set C_C=0, but the parent EM map is missing",
            "next_action": "derive EM-lock theorem or retain finite b_theta_alpha placeholder",
        },
        {
            "decision_id": "DEC987_2_best_next",
            "topic": "next checkpoint",
            "result": "alphaEM_clock_WEP_joint_prior_or_EM_lock_theorem",
            "reason": "the same b_alpha should be constrained by WEP Coulomb and clock/fine-structure arenas, so the next move is cross-arena tying",
            "next_action": "write 988 alpha_EM WEP-clock joint-prior skeleton or EM-lock theorem attempt",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
            "objective": "tie the Coulomb WEP b_theta_alpha route to clock/fine-structure constraints, or derive an EM-lock theorem that sets local alpha_EM variation to zero",
            "include": "WEP Coulomb proxy, d_ln_alpha_EM_dXhat prior slot, clock sensitivity placeholders, EM-lock parent gate",
            "exclude": "WEP pass, clock pass, invented sensitivity coefficients, b_kappa claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    normal_forms: list[dict[str, str]],
    projections: list[dict[str, str]],
    parent_zero: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    verdict_ok = any(row["form_id"] == "EMNF987_4_verdict" and row["status"] == "CLEAN_FINITE_ROUTE_BUT_PARENT_UNSIGNED" for row in normal_forms)
    projections_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in projections)
    parent_zero_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in parent_zero)
    claims_safe_ok = all(row["claim_allowed"] == "false" for row in claims)
    next_decision_ok = any(row["decision_id"] == "DEC987_2_best_next" and row["result"] == "alphaEM_clock_WEP_joint_prior_or_EM_lock_theorem" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V987_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all source files exist and needles are found"},
        {"check_id": "V987_1_normal_form_verdict", "result": "pass" if verdict_ok else "fail", "detail": "Coulomb route verdict is finite but parent-unsigned"},
        {"check_id": "V987_2_projection_nonclaim", "result": "pass" if projections_nonclaim_ok else "fail", "detail": "projection rows remain nonclaim"},
        {"check_id": "V987_3_parent_zero_nonclaim", "result": "pass" if parent_zero_nonclaim_ok else "fail", "detail": "parent-zero gate remains nonclaim"},
        {"check_id": "V987_4_claim_gates_safe", "result": "pass" if claims_safe_ok else "fail", "detail": "claim gates block WEP/clock/local-GR claims"},
        {"check_id": "V987_5_next_decision", "result": "pass" if next_decision_ok else "fail", "detail": "988 alphaEM WEP-clock/EM-lock target selected"},
        {"check_id": "V987_6_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V987_7_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {"check_id": "V987_READY", "result": "pass" if ready else "fail", "detail": "987 checkpoint pack validation summary", "generated_utc": stamp()}
    ]


def write_doc(
    sources: list[dict[str, str]],
    normal_forms: list[dict[str, str]],
    projections: list[dict[str, str]],
    parent_zero: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 987 Y5 R10: Coulomb To AlphaEM Normal Form Or Parent Zero Gate",
        "",
        "Status: `Y5_R10_987_Coulomb_WEP_routes_to_btheta_alphaEM_not_bkappa_finite_route_parent_unsigned`",
        "",
        "Claim ceiling: no WEP pass, no clock pass, no `b_theta_alpha_EM` bound, no `b_kappa` bound, no local-GR claim.",
        "",
        "## Readout",
        "",
        "987 classifies the cleanest finite WEP route. The Coulomb proxy is an EM/fine-structure sensitivity. It should route first to `b_theta_alpha_EM`, not to `b_kappa`. Universal `kappa` remains invisible to differential WEP unless it becomes composition dependent.",
        "",
        "There are three honest branches: constant/locked EM gives `C_C=0` if parent-signed; finite `alpha_EM(X)` gives a `b_theta_alpha_EM` channel; marker-dependent `alpha_EM(I_Q,m)` is forbidden or retained as `b_m` closure. No branch is claim-ready yet.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## EM Normal Forms",
        "",
        md_table(normal_forms, ["form_id", "normal_form", "Coulomb_effect", "MTS_slot", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Coulomb Projection",
        "",
        md_table(projections, ["projection_id", "formula", "known_from_983", "known_from_986", "missing_inputs", "claim_status", "valid_for_claim"]),
        "",
        "## Parent-Zero Gate",
        "",
        md_table(parent_zero, ["gate_id", "condition", "math_form", "result_if_signed", "current_status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    normal_forms = em_normal_form_rows()
    projections = coulomb_projection_rows()
    parent_zero = parent_zero_gate_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, normal_forms, projections, parent_zero, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_987_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_987_EM_NORMAL_FORMS.csv", normal_forms)
    write_csv(OUT / "P8_Y5_R10_987_COULOMB_PROJECTION.csv", projections)
    write_csv(OUT / "P8_Y5_R10_987_PARENT_ZERO_GATE.csv", parent_zero)
    write_csv(OUT / "P8_Y5_R10_987_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_987_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_987_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_987_VALIDATION.csv", validation)
    write_doc(sources, normal_forms, projections, parent_zero, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
