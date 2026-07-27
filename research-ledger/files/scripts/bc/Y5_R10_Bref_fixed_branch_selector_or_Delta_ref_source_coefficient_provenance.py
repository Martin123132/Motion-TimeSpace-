from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md"
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
            "source_id": "998_doc",
            "path": "998-Y5-R10-Bref-source-blindness-theorem-or-Delta-ref-source-component-row.md",
            "role": "handoff selecting fixed-branch selector or source coefficient provenance",
            "needle": "999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md",
        },
        {
            "source_id": "998_theorem_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_998_BREF_SOURCE_BLIND_THEOREM_ATTEMPT.csv",
            "role": "source-blind theorem attempt",
            "needle": "SBT998_2_fixed_branch_selector",
        },
        {
            "source_id": "998_leakage",
            "path": "source-intake/mts_residuals/P8_Y5_R10_998_SOURCE_LEAKAGE_CHANNEL_AUDIT.csv",
            "role": "source leakage channels",
            "needle": "SLC998_3_source_dependent_surface",
        },
        {
            "source_id": "998_countermodels",
            "path": "source-intake/mts_residuals/P8_Y5_R10_998_COUNTERMODEL_LEDGER.csv",
            "role": "countermodels blocking notation-only proof",
            "needle": "CM998_1_GM_calibrated_reference",
        },
        {
            "source_id": "998_component_template",
            "path": "source-intake/mts_residuals/P8_Y5_R10_998_DELTA_REF_SOURCE_COMPONENT_TEMPLATE.csv",
            "role": "source component template",
            "needle": "DSC998_0_component_schema",
        },
        {
            "source_id": "998_refusal",
            "path": "source-intake/mts_residuals/P8_Y5_R10_998_STRICT_REFUSAL_LEDGER.csv",
            "role": "strict anti-cheat policy",
            "needle": "REF998_1_no_source_calibration",
        },
        {
            "source_id": "997_derivative_component",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "partial_source Delta_ref component audit",
            "needle": "DVC997_0_source",
        },
        {
            "source_id": "667_action_ansatz",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
            "role": "candidate B_ref and fixed branch scaffold",
            "needle": "PBA667_4_reference_rule",
        },
        {
            "source_id": "667_variation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv",
            "role": "reference derivative ledger",
            "needle": "VL667_5_reference_derivative",
        },
        {
            "source_id": "668_boundary_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
            "role": "fixed branch lock failure",
            "needle": "BCL668_1_reference_fixed_branch",
        },
        {
            "source_id": "950_source_countermodel",
            "path": "source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "role": "source/species countermodel warning",
            "needle": "SNL950_4_countermodel",
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


def selector_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "selector_id": "FBS999_0_selector_definition",
            "claim": "a fixed-branch selector Sigma_ref is defined before source/readout",
            "mathematical_form": "Sigma_ref(Phi_parent) -> (gamma_ref,tau_ref,C_top,B_ct,S0) and B_ref=B_ref[Sigma_ref]",
            "would_close": "turns B_ref into fixed branch data instead of a chosen subtraction",
            "current_evidence": "667 defines H_ref and B_ref scaffolds",
            "current_status": "definition_level_only",
            "missing_signature": "parent action/constraint that uniquely selects Sigma_ref",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "FBS999_1_parent_variational_owner",
            "claim": "Sigma_ref is selected by parent Euler/Ward/topological conditions",
            "mathematical_form": "delta S_parent/delta Sigma_ref=0 or C_top/topology/stationarity fixes Sigma_ref",
            "would_close": "prevents post-fit reference selection",
            "current_evidence": "668 marks B_ref fixed branch as fail_current_claim",
            "current_status": "not_signed",
            "missing_signature": "explicit selector equation and boundary condition from parent action",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "FBS999_2_source_independence",
            "claim": "selector is independent of matter/source labels and fitted source parameters",
            "mathematical_form": "D_source Sigma_ref=0; D_source gamma_ref=D_source tau_ref=D_source C_top=D_source B_ct=D_source S0=0",
            "would_close": "partial_source Delta_ref=0 by chain rule",
            "current_evidence": "998 records the source-blindness theorem as conditional only",
            "current_status": "not_signed",
            "missing_signature": "no source labels/material markers/GM calibration in selector inputs",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "FBS999_3_surface_domain_lock",
            "claim": "reference surface/domain is fixed independently of the source choice",
            "mathematical_form": "D_source S0=0 and linked surfaces are selected by the same parent domain rule",
            "would_close": "blocks source dependence through moving surfaces rather than B_ref integrand",
            "current_evidence": "998 leakage audit flags S0=S0[source] as unexcluded",
            "current_status": "not_signed",
            "missing_signature": "source-blind linking-surface/domain selector",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "FBS999_4_no_GM_calibration",
            "claim": "selector cannot use observed GM, fitted mass, or source-current normalization",
            "mathematical_form": "partial_{GM_obs,M_fit,kappa_A,M_H_ref} Sigma_ref=0",
            "would_close": "prevents reference subtraction from absorbing the source mass we need to derive",
            "current_evidence": "998 countermodel CM998_1 remains legal",
            "current_status": "not_signed",
            "missing_signature": "source-current equality/Gauss readout kept downstream of selector",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "FBS999_5_counterterm_convention",
            "claim": "counterterm convention is fixed before readout",
            "mathematical_form": "B_ct=B_ct[Sigma_ref] and D_source B_ct=0",
            "would_close": "prevents source-dependent counterterm cancellation",
            "current_evidence": "998 flags B_ct[source,fit,calibration] as unexcluded",
            "current_status": "not_signed",
            "missing_signature": "counterterm convention with source path and equation reference",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "FBS999_6_same_frame_denominator",
            "claim": "selector and denominator use same tau/coframe/frame",
            "mathematical_form": "tau_ref=tau_Q=tau_source and M_H_ref>0 in that same frame",
            "would_close": "makes Delta_ref_source_component_over_MH meaningful",
            "current_evidence": "997/998 keep M_H_ref missing and forbid orbital GM substitution",
            "current_status": "not_signed",
            "missing_signature": "same-frame Hamiltonian/source mass owner",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "FBS999_7_verdict",
            "claim": "fixed-branch selector makes B_ref source-blind for current MTS",
            "mathematical_form": "FBS999_0 through FBS999_6 all signed => partial_source Delta_ref=0",
            "would_close": "the source component of Delta_ref theorem-zero",
            "current_evidence": "all decisive selector clauses remain unsigned",
            "current_status": "fail_current_claim",
            "missing_signature": "parent-owned Sigma_ref and same-frame denominator",
            "valid_for_claim": "false",
        },
    ]


def parent_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "FBC999_0_selector_function",
            "future_parent_action_must_supply": "a named selector function Sigma_ref",
            "minimum_form": "Sigma_ref: boundary/topology/stationarity data -> gamma_ref,tau_ref,C_top,B_ct,S0",
            "acceptance_test": "selector inputs contain no source/material/GM/calibration labels",
            "current_fill": "MISSING_PARENT_SELECTOR",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FBC999_1_variation_or_constraint",
            "future_parent_action_must_supply": "variation/constraint equation fixing Sigma_ref",
            "minimum_form": "E_Sigma=0, Ward condition, topological class, or stationarity condition",
            "acceptance_test": "equation is written in parent variables with source path/equation reference",
            "current_fill": "MISSING_SELECTOR_EQUATION",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FBC999_2_source_blind_derivatives",
            "future_parent_action_must_supply": "componentwise derivative-zero certificate",
            "minimum_form": "D_source gamma_ref=D_source tau_ref=D_source C_top=D_source B_ct=D_source S0=0",
            "acceptance_test": "each component is theorem-zero or source-backed bounded",
            "current_fill": "MISSING_SOURCE_BLIND_COMPONENT_CERTIFICATE",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FBC999_3_no_marker_clause",
            "future_parent_action_must_supply": "no material/source marker clause",
            "minimum_form": "delta Sigma_ref/delta(m_A,theta_A,kappa_A,composition_A)=0",
            "acceptance_test": "excludes 950/998 source-weight countermodels",
            "current_fill": "MISSING_NO_MARKER_SELECTOR_CLAUSE",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FBC999_4_no_GM_calibration",
            "future_parent_action_must_supply": "no measured-GM/fitted-source calibration in selector",
            "minimum_form": "partial_{GM_obs,M_fit,M_H_ref} Sigma_ref=0 before source-current equality",
            "acceptance_test": "no orbital/observed GM appears in B_ref or B_ct provenance",
            "current_fill": "MISSING_NO_GM_CALIBRATION_CERTIFICATE",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FBC999_5_counterterm_provenance",
            "future_parent_action_must_supply": "counterterm convention fixed before readout",
            "minimum_form": "B_ct formula, units, boundary convention, source path, equation reference",
            "acceptance_test": "D_source B_ct=0 or finite sourced source-component residual",
            "current_fill": "MISSING_COUNTERTERM_CONVENTION",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FBC999_6_MHref_sidecar",
            "future_parent_action_must_supply": "same-frame positive M_H_ref sidecar",
            "minimum_form": "M_H_ref;units;tau_id;frame_id;source_path;equation_ref",
            "acceptance_test": "positive Hamiltonian denominator; no orbital GM substitution",
            "current_fill": "MISSING_SAME_FRAME_MHREF",
            "valid_for_claim": "false",
        },
    ]


def coefficient_provenance_rows() -> list[dict[str, str]]:
    return [
        {
            "provenance_id": "DCP999_0_partial_source_derivative",
            "coefficient": "partial_source_Delta_ref",
            "target_row": "Delta_ref_source_component_over_MH",
            "required_provenance": "source_parameter;derivative_value;units;source_path;equation_ref;extraction_method;valid_for_claim",
            "acceptance_rule": "numeric derivative or theorem_zero=true with parent-signed selector",
            "current_value": "MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "provenance_id": "DCP999_1_source_scale",
            "coefficient": "Delta_source_scale",
            "target_row": "Delta_ref_source_component_over_MH",
            "required_provenance": "definition of source variation scale; units; source_path;equation_ref",
            "acceptance_rule": "source parameter must be physically defined, not chosen to shrink the residual",
            "current_value": "MISSING_SOURCE_SCALE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "provenance_id": "DCP999_2_Bref_rule",
            "coefficient": "B_ref_rule",
            "target_row": "Delta_ref_source_component_over_MH",
            "required_provenance": "B_ref formula; boundary convention; counterterm convention; source_path;equation_ref",
            "acceptance_rule": "formula must be fixed before source/readout and contain no hidden GM/source labels",
            "current_value": "MISSING_PARENT_BREF_RULE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "provenance_id": "DCP999_3_MHref",
            "coefficient": "M_H_ref",
            "target_row": "Delta_ref_source_component_over_MH",
            "required_provenance": "positive same-frame Hamiltonian source mass; units; tau/frame ids; source_path;equation_ref",
            "acceptance_rule": "same-frame and not orbital GM imported before Gauss/source-current proof",
            "current_value": "MISSING_SAME_FRAME_MHREF",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "provenance_id": "DCP999_4_component_bound",
            "coefficient": "Delta_ref_source_component_over_MH",
            "target_row": "Delta_ref_source_component_over_MH",
            "required_provenance": "partial_source_Delta_ref;Delta_source_scale;M_H_ref;absolute-value rule;source_path;valid_for_claim",
            "acceptance_rule": "abs(partial_source_Delta_ref*Delta_source_scale)/M_H_ref with no cancellation credit",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def coefficient_runner_readiness_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "DCR999_0_schema_ready",
            "object": "Delta_ref source-component finite row",
            "ready": "true",
            "reason": "required fields and absolute-value rule are specified",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "DCR999_1_values_ready",
            "object": "numeric/theorem-zero inputs",
            "ready": "false",
            "reason": "partial_source_Delta_ref, source scale, B_ref rule, and M_H_ref are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "DCR999_2_no_silent_zero",
            "object": "zero-theorem switch",
            "ready": "false",
            "reason": "selector theorem not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "DCR999_3_no_downstream_score",
            "object": "Delta_ref/RC994_0/local-GR score",
            "ready": "false",
            "reason": "this is one source-component row only and the denominator/source-current route remains open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG999_0_fixed_branch_selector",
            "claim": "B_ref fixed-branch selector is parent-owned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "selector equation, no-marker clause, no-GM calibration, counterterm convention, and M_H_ref sidecar are missing",
        },
        {
            "gate_id": "CG999_1_source_blind_Bref",
            "claim": "B_ref is source-blind",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source-blindness depends on the unsigned selector",
        },
        {
            "gate_id": "CG999_2_source_component_score",
            "claim": "Delta_ref_source_component_over_MH is score-ready",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "coefficient provenance rows are MISSING and score_ready=false",
        },
        {
            "gate_id": "CG999_3_downstream",
            "claim": "Delta_ref, RC994_0, deltaH, FB554_0, Newton/PPN/R10/local-GR pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "999 only locks selector/provenance requirements and does not close the residual",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC999_0_selector_attempt",
            "decision": "do not promote the fixed-branch selector theorem",
            "reason": "the current corpus has a useful B_ref scaffold but not the parent selector equation or no-marker/GM/counterterm sidecars",
            "effect": "B_ref source-blindness and partial_source Delta_ref remain unclaimed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC999_1_provenance_gate",
            "decision": "stage finite source-component provenance requirements",
            "reason": "if the selector cannot be signed, the source component must be bounded from sourced inputs",
            "effect": "future numeric row cannot be scored without exact provenance",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC999_2_next_target",
            "decision": "move to a runnable strict provenance checker",
            "reason": "the schema is now explicit enough to refuse bad rows automatically",
            "effect": "1000 can build the refusal/validation runner for any proposed Delta_ref source coefficient",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1000-Y5-R10-Delta-ref-source-coefficient-strict-provenance-runner.md",
            "objective": "build a strict runner that refuses Delta_ref_source_component rows unless selector theorem or finite coefficient provenance is complete",
            "include": "partial_source_Delta_ref, Delta_source_scale, B_ref rule, M_H_ref, units, equation/source paths, theorem-zero switch, no-cancellation guard",
            "exclude": "invented coefficients, zero-by-closure, Delta_ref pass, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action, formalization-workbench edits",
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
    selector: list[dict[str, str]],
    contract: list[dict[str, str]],
    provenance: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    selector_ok = (
        len(selector) >= 8
        and any(row["selector_id"] == "FBS999_7_verdict" and row["current_status"] == "fail_current_claim" for row in selector)
        and all(row["valid_for_claim"] == "false" for row in selector)
    )
    contract_ok = (
        len(contract) >= 7
        and all(row["valid_for_claim"] == "false" and "MISSING" in row["current_fill"] for row in contract)
    )
    provenance_ok = (
        len(provenance) >= 5
        and all(row["valid_for_claim"] == "false" and row["score_ready"] == "false" for row in provenance)
        and all("MISSING" in row["current_value"] for row in provenance)
    )
    runner_ok = (
        len(runner) >= 4
        and any(row["runner_id"] == "DCR999_0_schema_ready" and row["ready"] == "true" for row in runner)
        and all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in runner)
    )
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC999_2_next_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V999_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V999_1_selector_attempt_fail_closed", "result": "pass" if selector_ok else "fail", "detail": "fixed-branch selector theorem is attempted but not promoted"},
        {"check_id": "V999_2_parent_contract_missing", "result": "pass" if contract_ok else "fail", "detail": "future parent-action selector contract is explicit and missing-marked"},
        {"check_id": "V999_3_provenance_missing", "result": "pass" if provenance_ok else "fail", "detail": "finite source-component provenance rows are missing and score_ready=false"},
        {"check_id": "V999_4_runner_readiness_safe", "result": "pass" if runner_ok else "fail", "detail": "schema is ready but values/claims are refused"},
        {"check_id": "V999_5_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "selector, source-blindness, source component score, and downstream claims are blocked"},
        {"check_id": "V999_6_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "strict provenance runner selected next"},
        {"check_id": "V999_7_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1000 target row is present and nonclaim"},
        {"check_id": "V999_8_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V999_READY",
            "result": "pass" if ready else "fail",
            "detail": "999 B_ref fixed-branch selector/provenance validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    selector: list[dict[str, str]],
    contract: list[dict[str, str]],
    provenance: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 999 Y5 R10: B_ref Fixed-Branch Selector or Delta_ref Source-Coefficient Provenance",
        "",
        "Status: `Y5_R10_999_Bref_fixed_branch_selector_not_signed_source_component_provenance_gate_staged_nonclaim`",
        "",
        "Claim ceiling: no parent-owned `B_ref` fixed-branch selector, no `B_ref` source-blindness theorem, no `partial_source Delta_ref=0`, no score-ready `Delta_ref_source_component_over_MH`, no `Delta_ref` pass, no `RC994_0=0`, no `deltaH` curl closure, no `FB554_0=0`, no Newton/PPN/R10/R11/orbit/local-GR pass.",
        "",
        "## Readout",
        "",
        "999 asks the right selector question: what parent rule forces the reference branch before source/readout exists? The current corpus has a useful `B_ref` scaffold, but not a selector equation. That means source-blindness is still a conditional route, not a current theorem.",
        "",
        "The gain is concrete: any future finite `Delta_ref_source_component_over_MH` row now needs exact provenance for `partial_source_Delta_ref`, source scale, `B_ref` rule, and same-frame `M_H_ref`. No magic pocket, no calibration rabbit.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Fixed-Branch Selector Attempt",
        "",
        md_table(selector, ["selector_id", "claim", "mathematical_form", "would_close", "current_evidence", "current_status", "missing_signature", "valid_for_claim"]),
        "",
        "## Future Parent-Action Selector Contract",
        "",
        md_table(contract, ["contract_id", "future_parent_action_must_supply", "minimum_form", "acceptance_test", "current_fill", "valid_for_claim"]),
        "",
        "## Delta_ref Source-Coefficient Provenance Gate",
        "",
        md_table(provenance, ["provenance_id", "coefficient", "target_row", "required_provenance", "acceptance_rule", "current_value", "score_ready", "valid_for_claim"]),
        "",
        "## Runner Readiness",
        "",
        md_table(runner, ["runner_id", "object", "ready", "reason", "claim_allowed", "valid_for_claim"]),
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
    selector = selector_attempt_rows()
    contract = parent_contract_rows()
    provenance = coefficient_provenance_rows()
    runner = coefficient_runner_readiness_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, selector, contract, provenance, runner, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_999_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv", selector)
    write_csv(OUT / "P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv", contract)
    write_csv(OUT / "P8_Y5_R10_999_DELTA_REF_SOURCE_COEFFICIENT_PROVENANCE.csv", provenance)
    write_csv(OUT / "P8_Y5_R10_999_COEFFICIENT_RUNNER_READINESS.csv", runner)
    write_csv(OUT / "P8_Y5_R10_999_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_999_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_999_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_999_VALIDATION.csv", validation)
    write_doc(sources, selector, contract, provenance, runner, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
