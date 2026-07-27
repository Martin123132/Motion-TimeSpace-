from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "997-Y5-R10-Bref-derivative-vector-theorem-or-Delta-ref-source-row.md"
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
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "996_doc",
            "path": "996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md",
            "role": "handoff selecting B_ref derivative vector or Delta_ref source row",
            "needle": "997-Y5-R10-Bref-derivative-vector-theorem-or-Delta-ref-source-row.md",
        },
        {
            "source_id": "996_derivative_test",
            "path": "source-intake/mts_residuals/P8_Y5_R10_996_BREF_SUPERSELECTION_DERIVATIVE_TEST.csv",
            "role": "B_ref derivative-vector blocker",
            "needle": "BST996_5_Bref_vector_verdict",
        },
        {
            "source_id": "996_source_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_996_RC9940_SOURCE_BOUND_INPUT_PACK.csv",
            "role": "source-bound pack selecting Delta_ref_over_MH first",
            "needle": "SBI996_0_Delta_ref",
        },
        {
            "source_id": "995_bound_schema",
            "path": "source-intake/mts_residuals/P8_Y5_R10_995_RC9940_RESIDUAL_BOUND_ROW_SCHEMA.csv",
            "role": "older RC994_0 residual-bound schema",
            "needle": "BR995_0_Delta_ref",
        },
        {
            "source_id": "667_action_ansatz",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
            "role": "B_ref action scaffold and reference-rule row",
            "needle": "PBA667_4_reference_rule",
        },
        {
            "source_id": "667_variation_ledger",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv",
            "role": "reference derivative ledger",
            "needle": "VL667_5_reference_derivative",
        },
        {
            "source_id": "668_boundary_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
            "role": "failed fixed-branch boundary lock",
            "needle": "BCL668_1_reference_fixed_branch",
        },
        {
            "source_id": "545_contract",
            "path": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
            "role": "minimal reference-lock clause",
            "needle": "MAC545_2_reference_lock",
        },
        {
            "source_id": "552_clause_tests",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_CLAUSE_TESTS.csv",
            "role": "reference symplectic clause failure",
            "needle": "CT552_0_reference_symplectic",
        },
        {
            "source_id": "994_deltaH_envelope",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "no-cancellation envelope policy",
            "needle": "DHE994_1_no_cancellation",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "BDT997_0_define_reference_charge",
            "claim": "reference charge can be expressed as a boundary functional before readout",
            "mathematical_step": "H_ref[S,tau]=int_S B_ref[gamma_ref,tau_ref,C_top]; Delta_ref=H_ref[S,tau]-H_ref[S0,tau0]",
            "needed_premise": "B_ref, gamma_ref, tau_ref, C_top, and S0 are parent-selected fixed-branch data",
            "current_status": "definition_written",
            "why_not_claim": "667 gives the ledger definition but not a unique parent selector",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDT997_1_chain_rule_zero",
            "claim": "if fixed-branch data are superselected, derivatives of H_ref vanish",
            "mathematical_step": "D_a H_ref=int_S[(delta B_ref/delta gamma_ref)D_a gamma_ref+(delta B_ref/delta tau_ref)D_a tau_ref+(delta B_ref/delta C_top)D_a C_top]+surface_term_a",
            "needed_premise": "D_a gamma_ref=D_a tau_ref=D_a C_top=0 and surface_term_a=0 for a in {source,r,t,frame,lambda}",
            "current_status": "conditional_lemma",
            "why_not_claim": "superselection and surface terms are exactly the unsigned B_ref rule",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDT997_2_radius_surface_term",
            "claim": "radial/surface derivative can vanish by relative exactness",
            "mathematical_step": "partial_r H_ref=int_{partial A_r} B_ref = int_A dB_ref plus corner terms",
            "needed_premise": "dB_ref=0 or a parent-selected relative exact class with corner terms fixed",
            "current_status": "conditional_lemma",
            "why_not_claim": "relative boundary class remains unsigned and exact-looking terms may carry finite charge",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDT997_3_time_stationarity",
            "claim": "time derivative can vanish by reference stationarity",
            "mathematical_step": "partial_t H_ref=int_S L_tau B_ref=0",
            "needed_premise": "tau_ref is parent-owned and B_ref is stationary on the fixed branch",
            "current_status": "conditional_lemma",
            "why_not_claim": "tau/coframe owner is still missing and time-generator equality is downstream",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDT997_4_frame_covariance",
            "claim": "frame derivative can vanish by covariant reference functor",
            "mathematical_step": "partial_frame H_ref=0 if frame changes are proper gauge and B_ref is a scalar/covariant boundary form on fixed data",
            "needed_premise": "observed coframe functor and proper/improper charge split are parent-owned",
            "current_status": "conditional_lemma",
            "why_not_claim": "frame/coframe and proper-charge guards remain unsigned",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDT997_5_range_parameter",
            "claim": "range/lambda derivative can vanish if B_ref has no MTS range parameter dependence",
            "mathematical_step": "partial_lambda H_ref=0 when partial_lambda B_ref=0 and C_top is lambda-independent",
            "needed_premise": "B_ref normalization is universal and not tuned to R10/lambda/sector parameters",
            "current_status": "conditional_lemma",
            "why_not_claim": "B_ref rule is still named rather than derived from the parent branch",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDT997_6_verdict",
            "claim": "B_ref derivative-vector zero theorem is signed for current MTS",
            "mathematical_step": "D_ref Delta_ref=(partial_source,partial_r,partial_t,partial_frame,partial_lambda)Delta_ref=(0,0,0,0,0)",
            "needed_premise": "BDT997_0 through BDT997_5 accepted from parent-owned data",
            "current_status": "fail_current_claim",
            "why_not_claim": "the proof is a valid conditional lemma, not a current MTS theorem",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
    ]


def derivative_component_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "DVC997_0_source",
            "component": "partial_source Delta_ref",
            "zero_condition": "B_ref contains no source fields, material labels, fitted source amplitudes, or post-readout calibration constants",
            "current_value": "MISSING_PARENT_BREF_RULE",
            "failure_if_open": "reference subtraction can absorb source calibration",
            "source_row_if_fail": "Delta_ref_source_component_over_MH",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC997_1_radius",
            "component": "partial_r Delta_ref",
            "zero_condition": "surface deformation term vanishes by dB_ref=0, fixed corners, or source-backed finite radial profile",
            "current_value": "MISSING_SURFACE_CLASS_OR_RADIAL_PROFILE",
            "failure_if_open": "reference charge changes between linked surfaces",
            "source_row_if_fail": "Delta_ref_radial_profile_over_MH",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC997_2_time",
            "component": "partial_t Delta_ref",
            "zero_condition": "L_tau B_ref=0 under the same tau used by charge, clocks, and readout",
            "current_value": "MISSING_STATIONARY_TAU_BREF_RULE",
            "failure_if_open": "reference drift can mimic Gdot/clock leakage",
            "source_row_if_fail": "Delta_ref_time_profile_over_MH",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC997_3_frame",
            "component": "partial_frame Delta_ref",
            "zero_condition": "frame changes are proper gauge for B_ref and do not change the physical Hamiltonian reference",
            "current_value": "MISSING_COVARIANT_COFRAME_REFERENCE_RULE",
            "failure_if_open": "preferred-frame/reference leakage enters PPN and source normalization",
            "source_row_if_fail": "Delta_ref_frame_profile_over_MH",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC997_4_lambda",
            "component": "partial_lambda Delta_ref",
            "zero_condition": "B_ref is independent of R10 range/memory/domain/sector scale parameters",
            "current_value": "MISSING_RANGE_INDEPENDENCE_RULE",
            "failure_if_open": "reference subtraction can track R10/local-bound parameters",
            "source_row_if_fail": "Delta_ref_lambda_profile_over_MH",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DVC997_5_vector_norm",
            "component": "||D_ref Delta_ref||_1/M_H_ref",
            "zero_condition": "all five derivative components theorem-zero or sourced and bounded; M_H_ref positive same-frame",
            "current_value": "MISSING_ALL_COMPONENTS_AND_MHREF",
            "failure_if_open": "Delta_ref_over_MH cannot be used as a stable residual row",
            "source_row_if_fail": "Delta_ref_derivative_vector_norm_over_MH",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]


def delta_ref_source_row_template() -> list[dict[str, str]]:
    return [
        {
            "row_id": "DRS997_0_claim_ready_schema",
            "target": "Delta_ref_over_MH",
            "formula": "abs(Delta_ref)/M_H_ref",
            "required_columns": "system_id;surface_pair;Delta_ref;Delta_ref_units;M_H_ref;M_H_ref_units;B_ref_rule;derivative_vector;source_path;equation_ref;theorem_zero;valid_for_claim",
            "acceptance_rule": "numeric finite same-frame ratio or theorem_zero=true; source path exists; no MISSING markers; derivative vector componentwise zero/bounded",
            "current_fill": "schema_only",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DRS997_1_current_candidate",
            "target": "Delta_ref_over_MH",
            "formula": "abs(H_ref[S,tau]-H_ref[fixed_branch])/M_H_ref",
            "required_columns": "H_ref_rule;fixed_branch_id;surface_pair;tau_id;M_H_ref;source_path;equation_ref",
            "acceptance_rule": "B_ref and fixed branch derived before readout, denominator positive and same-frame",
            "current_fill": "MISSING_BREF_RULE_MISSING_DELTA_REF_VALUE_MISSING_MHREF",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DRS997_2_derivative_vector_sidecar",
            "target": "D_ref_Delta_ref",
            "formula": "(partial_source,partial_r,partial_t,partial_frame,partial_lambda)Delta_ref",
            "required_columns": "component;value;units;zero_theorem;bound;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "each derivative component is theorem-zero or source-backed bounded with no MISSING markers",
            "current_fill": "MISSING_PARENT_BREF_RULE_FOR_ALL_COMPONENTS",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DRS997_3_no_cancellation_guard",
            "target": "Delta_ref acceptance",
            "formula": "abs(Delta_ref)/M_H_ref and sum_abs derivative sidecar; no sign cancellation credit",
            "required_columns": "component_abs_values;M_H_ref;source_path;valid_for_claim",
            "acceptance_rule": "componentwise theorem-zero/source-bound only",
            "current_fill": "GUARD_ACTIVE_NO_VALUES",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
    ]


def mhref_guard_rows() -> list[dict[str, str]]:
    return [
        {
            "guard_id": "MHG997_0_positive_denominator",
            "denominator_requirement": "M_H_ref>0",
            "why_needed": "Delta_ref_over_MH is meaningless or cheat-prone without a positive denominator",
            "current_status": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "MHG997_1_same_frame",
            "denominator_requirement": "M_H_ref uses the same tau/coframe/frame as H_ref and Q_tau",
            "why_needed": "prevents mixing a reference subtraction from one frame with a measured mass from another",
            "current_status": "MISSING_TAU_COFRAME_SOURCE_OWNER",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "MHG997_2_not_orbital_import",
            "denominator_requirement": "GM_orbit is not substituted for M_H_ref before source-current equality and Gauss/readout",
            "why_needed": "prevents circular Newton/local-GR proof",
            "current_status": "POLICY_PASS_DENOMINATOR_STILL_MISSING",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG997_0_Bref_derivative_zero",
            "claim": "B_ref derivative vector vanishes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "conditional chain-rule proof needs a parent-owned B_ref rule and fixed-branch data",
        },
        {
            "gate_id": "CG997_1_Delta_ref_zero",
            "claim": "Delta_ref_over_MH=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "Delta_ref value, B_ref rule, derivative vector, and M_H_ref are not sourced or theorem-zero",
        },
        {
            "gate_id": "CG997_2_Delta_ref_bound",
            "claim": "Delta_ref_over_MH has a source-backed bound",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source row is a template with MISSING_SOURCE_FILE and MISSING values",
        },
        {
            "gate_id": "CG997_3_downstream_claims",
            "claim": "RC994_0, deltaH, FB554_0, Newton/PPN/R10/local-GR pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "997 only narrows the first component of RC994_0 and does not supply source-current equality",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC997_0_derivation_attempt",
            "decision": "do not promote the B_ref derivative-vector zero theorem",
            "reason": "the proof is conditionally valid by chain rule, but its superselection premises are exactly the missing parent B_ref rule",
            "effect": "Delta_ref_over_MH remains retained",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC997_1_useful_derivation",
            "decision": "keep the chain-rule theorem as a future parent-action contract",
            "reason": "it shows precisely how source/radius/time/frame/lambda silence would follow if B_ref is truly fixed branch data",
            "effect": "future work can sign component derivatives one by one",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC997_2_next_component",
            "decision": "target the source derivative first",
            "reason": "partial_source Delta_ref is the most dangerous channel because it can absorb source calibration",
            "effect": "998 should either prove source-blind B_ref or fill Delta_ref_source_component_over_MH",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "998-Y5-R10-Bref-source-blindness-theorem-or-Delta-ref-source-component-row.md",
            "objective": "prove B_ref is source-blind before readout, or fill the source-derivative component of Delta_ref_over_MH",
            "include": "partial_source Delta_ref, no material/source labels in B_ref, fixed branch selector, same-frame M_H_ref, equation/source path",
            "exclude": "Delta_ref pass, RC994_0 pass, FB554_0 pass, Newton/PPN/R10/local-GR pass, orbital GM substitution, hidden EH import, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    components: list[dict[str, str]],
    source_template: list[dict[str, str]],
    mhref: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_ok = (
        len(theorem) >= 7
        and any(row["step_id"] == "BDT997_6_verdict" and row["current_status"] == "fail_current_claim" for row in theorem)
        and all(row["accepted_for_claim"] == "false" and row["valid_for_claim"] == "false" for row in theorem)
    )
    components_ok = (
        len(components) >= 6
        and any(row["component_id"] == "DVC997_5_vector_norm" and row["status"] == "fail_current_claim" for row in components)
        and all(row["valid_for_claim"] == "false" and ("MISSING" in row["current_value"]) for row in components)
    )
    source_ok = (
        len(source_template) >= 4
        and all(row["valid_for_claim"] == "false" for row in source_template)
        and any("MISSING" in row["current_fill"] for row in source_template)
        and any(row["row_id"] == "DRS997_3_no_cancellation_guard" for row in source_template)
    )
    mhref_ok = all(row["valid_for_claim"] == "false" and row["accepted_for_claim"] == "false" for row in mhref)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC997_2_next_component" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V997_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V997_1_theorem_attempt_fail_closed", "result": "pass" if theorem_ok else "fail", "detail": "B_ref derivative-vector theorem is conditional and not promoted"},
        {"check_id": "V997_2_component_vector_blocked", "result": "pass" if components_ok else "fail", "detail": "all derivative components remain MISSING and nonclaim"},
        {"check_id": "V997_3_source_row_template_safe", "result": "pass" if source_ok else "fail", "detail": "Delta_ref source row is schema-only with no-cancellation guard"},
        {"check_id": "V997_4_MHref_guard_safe", "result": "pass" if mhref_ok else "fail", "detail": "M_H_ref denominator remains guarded and nonclaim"},
        {"check_id": "V997_5_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "B_ref, Delta_ref, RC994_0, and local-GR claims are blocked"},
        {"check_id": "V997_6_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "source-derivative next component decision is recorded"},
        {"check_id": "V997_7_next_target_written", "result": "pass" if next_ok else "fail", "detail": "998 target row is present and nonclaim"},
        {"check_id": "V997_8_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V997_READY",
            "result": "pass" if ready else "fail",
            "detail": "997 B_ref derivative-vector validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    components: list[dict[str, str]],
    source_template: list[dict[str, str]],
    mhref: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 997 Y5 R10: B_ref Derivative-Vector Theorem or Delta_ref Source Row",
        "",
        "Status: `Y5_R10_997_Bref_derivative_vector_theorem_conditional_not_signed_Delta_ref_source_row_staged_nonclaim`",
        "",
        "Claim ceiling: no `B_ref` derivative-vector zero theorem, no `Delta_ref_over_MH=0`, no source-backed `Delta_ref` bound, no `RC994_0=0`, no `deltaH` curl closure, no `FB554_0=0`, no Newton/PPN/R10/R11/orbit/local-GR pass.",
        "",
        "## Readout",
        "",
        "997 gives the exact shape of the missing proof. If `B_ref` is genuinely fixed-branch data, the chain rule kills source, radius, time, frame, and range derivatives. That is the good news: the theorem is mathematically clean.",
        "",
        "The bad-but-useful news is that current MTS has not parent-signed the fixed-branch selector. So this is not a local-GR win yet; it is a precise target. The nastiest component is `partial_source Delta_ref`, because a source-dependent reference could fake mass calibration. That is where 998 should bite.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## B_ref Derivative-Vector Theorem Attempt",
        "",
        md_table(theorem, ["step_id", "claim", "mathematical_step", "needed_premise", "current_status", "why_not_claim", "accepted_for_claim", "valid_for_claim"]),
        "",
        "## Derivative Component Audit",
        "",
        md_table(components, ["component_id", "component", "zero_condition", "current_value", "failure_if_open", "source_row_if_fail", "status", "valid_for_claim"]),
        "",
        "## Delta_ref Source Row Template",
        "",
        md_table(source_template, ["row_id", "target", "formula", "required_columns", "acceptance_rule", "current_fill", "source_path", "valid_for_claim"]),
        "",
        "## M_H_ref Denominator Guard",
        "",
        md_table(mhref, ["guard_id", "denominator_requirement", "why_needed", "current_status", "accepted_for_claim", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
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
    theorem = theorem_attempt_rows()
    components = derivative_component_rows()
    source_template = delta_ref_source_row_template()
    mhref = mhref_guard_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, components, source_template, mhref, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_997_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_997_BREF_DERIVATIVE_ZERO_THEOREM_ATTEMPT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv", components)
    write_csv(OUT / "P8_Y5_R10_997_DELTA_REF_SOURCE_ROW_TEMPLATE.csv", source_template)
    write_csv(OUT / "P8_Y5_R10_997_MHREF_DENOMINATOR_GUARD.csv", mhref)
    write_csv(OUT / "P8_Y5_R10_997_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_997_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_997_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_997_VALIDATION.csv", validation)
    write_doc(sources, theorem, components, source_template, mhref, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
