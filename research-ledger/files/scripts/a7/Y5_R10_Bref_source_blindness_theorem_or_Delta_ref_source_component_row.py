from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "998-Y5-R10-Bref-source-blindness-theorem-or-Delta-ref-source-component-row.md"
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
            "source_id": "997_doc",
            "path": "997-Y5-R10-Bref-derivative-vector-theorem-or-Delta-ref-source-row.md",
            "role": "handoff selecting source-blind B_ref or source component row",
            "needle": "998-Y5-R10-Bref-source-blindness-theorem-or-Delta-ref-source-component-row.md",
        },
        {
            "source_id": "997_component_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "partial_source Delta_ref component blocker",
            "needle": "DVC997_0_source",
        },
        {
            "source_id": "997_source_template",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DELTA_REF_SOURCE_ROW_TEMPLATE.csv",
            "role": "Delta_ref source-row schema",
            "needle": "DRS997_2_derivative_vector_sidecar",
        },
        {
            "source_id": "667_action_ansatz",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
            "role": "candidate B_ref functional arguments",
            "needle": "PBA667_2_boundary_action",
        },
        {
            "source_id": "667_variation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv",
            "role": "reference derivative row",
            "needle": "VL667_5_reference_derivative",
        },
        {
            "source_id": "668_boundary_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
            "role": "reference fixed branch failure",
            "needle": "BCL668_1_reference_fixed_branch",
        },
        {
            "source_id": "668_owner_queue",
            "path": "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
            "role": "B_ref can absorb source calibration unless fixed",
            "needle": "reference can absorb source calibration unless fixed",
        },
        {
            "source_id": "950_doc",
            "path": "950-Y5-R10-source-normalization-species-blind-zero-lemma-or-first-finite-coefficient-smoke-run.md",
            "role": "source/species blind cautionary lemma and countermodel",
            "needle": "species-weighted source current",
        },
        {
            "source_id": "950_source_norm_lemma",
            "path": "source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "role": "source-normalization countermodel",
            "needle": "SNL950_4_countermodel",
        },
        {
            "source_id": "950_refusal",
            "path": "source-intake/mts_residuals/P8_Y5_R10_950_STRICT_REFUSAL_LEDGER.csv",
            "role": "strict no silent-zero/no invented coefficient policy",
            "needle": "REF950_1_no_silent_zero",
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


def source_blind_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "SBT998_0_target",
            "statement": "B_ref is source-blind before readout",
            "mathematical_form": "partial_source B_ref[gamma_ref,tau_ref,C_top,B_ct]=0",
            "proof_status": "target_defined",
            "needed_for": "partial_source Delta_ref=0",
            "blocker": "target definition is not a parent proof",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SBT998_1_argument_absence",
            "statement": "candidate notation has no explicit source argument",
            "mathematical_form": "B_ref=B_ref[gamma_ref,tau_ref,C_top]+B_ct[fixed_branch]",
            "proof_status": "useful_but_insufficient",
            "needed_for": "exclude explicit source fields in B_ref",
            "blocker": "absence of a source symbol in an ansatz does not prove the fixed branch is source-independent",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SBT998_2_fixed_branch_selector",
            "statement": "fixed branch data are selected without source labels or fitted mass/calibration",
            "mathematical_form": "D_source gamma_ref=D_source tau_ref=D_source C_top=D_source B_ct=0",
            "proof_status": "not_signed",
            "needed_for": "chain-rule zero of partial_source H_ref",
            "blocker": "667/668 mark the parent-selected reference branch as missing",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SBT998_3_no_material_marker",
            "statement": "B_ref contains no matter/material/species marker",
            "mathematical_form": "delta B_ref/delta m_A=delta B_ref/delta theta_A=delta B_ref/delta kappa_A=0",
            "proof_status": "not_signed",
            "needed_for": "prevent source-composition leakage into reference subtraction",
            "blocker": "950 shows species/source weights remain legal unless parent action forbids them",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SBT998_4_no_measured_GM_calibration",
            "statement": "B_ref cannot depend on measured GM, source amplitude, or post-fit calibration",
            "mathematical_form": "partial_{GM_obs,M_source,calibration} B_ref=0",
            "proof_status": "not_signed",
            "needed_for": "prevent the reference from absorbing source mass normalization",
            "blocker": "same-frame M_H_ref/source-current equality is still missing",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SBT998_5_counterterm_guard",
            "statement": "B_ct cannot hide source dependence",
            "mathematical_form": "B_ct=B_ct[fixed_branch] and D_source B_ct=0",
            "proof_status": "not_signed",
            "needed_for": "prevent a source-dependent counterterm from cancelling Delta_ref",
            "blocker": "counterterm convention/source path is not fixed",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "step_id": "SBT998_6_verdict",
            "statement": "partial_source Delta_ref=0 closes as a current MTS theorem",
            "mathematical_form": "partial_source Delta_ref=partial_source int_S B_ref-partial_source int_S0 B_ref=0",
            "proof_status": "fail_current_claim",
            "needed_for": "Delta_ref_source_component_over_MH theorem-zero",
            "blocker": "the fixed-branch selector, no-marker clause, no-GM-calibration clause, and counterterm rule are all unsigned",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
    ]


def source_leakage_channel_rows() -> list[dict[str, str]]:
    return [
        {
            "channel_id": "SLC998_0_explicit_source_fields",
            "source_leak_channel": "B_ref directly depends on matter/source fields",
            "forbidden_form": "B_ref[...,psi_A,T_A,J_source]",
            "current_status": "not_parent_excluded",
            "why_dangerous": "lets reference subtraction track the source distribution",
            "required_exit": "parent B_ref argument list and variation proving delta B_ref/delta psi_A=0",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "SLC998_1_material_species_labels",
            "source_leak_channel": "B_ref depends on material/species labels",
            "forbidden_form": "B_ref[...,m_A,theta_A,kappa_A,composition_A]",
            "current_status": "not_parent_excluded",
            "why_dangerous": "turns WEP/source-normalization markers into reference drift",
            "required_exit": "no-marker/source-universality clause signed by parent action",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "SLC998_2_measured_GM_or_mass_fit",
            "source_leak_channel": "B_ref depends on observed GM or fitted source mass",
            "forbidden_form": "B_ref[...,GM_obs,M_fit,M_H_ref]",
            "current_status": "not_parent_excluded",
            "why_dangerous": "reference term can absorb the mass normalization we are trying to derive",
            "required_exit": "source-current equality and Gauss/readout theorem before any GM input",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "SLC998_3_source_dependent_surface",
            "source_leak_channel": "the reference surface/fixed branch moves with source choice",
            "forbidden_form": "S0=S0[source] or gamma_ref=gamma_ref[source]",
            "current_status": "not_parent_excluded",
            "why_dangerous": "partial_source Delta_ref re-enters through the domain rather than the integrand",
            "required_exit": "fixed branch selector and linking-surface rule independent of source labels",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "SLC998_4_counterterm_calibration",
            "source_leak_channel": "counterterm normalization is chosen after source/readout",
            "forbidden_form": "B_ct=B_ct[source,fit,calibration]",
            "current_status": "not_parent_excluded",
            "why_dangerous": "can fake zero by subtraction while leaving the physics unowned",
            "required_exit": "counterterm convention fixed in the parent action with source path/equation reference",
            "valid_for_claim": "false",
        },
        {
            "channel_id": "SLC998_5_source_current_weight",
            "source_leak_channel": "species-weighted source current countermodel",
            "forbidden_form": "J_source=sum_A kappa_A(source) T_A with B_ref or M_H_ref tracking kappa_A",
            "current_status": "countermodel_retained",
            "why_dangerous": "950 shows metric/descent language alone does not exclude source weights",
            "required_exit": "parent source-current Ward/no-marker theorem",
            "valid_for_claim": "false",
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM998_0_source_weighted_reference",
            "construction": "B_ref = B_ref0[gamma_ref,tau_ref,C_top] + epsilon f(source_label) omega_S",
            "preserves": "formal boundary covariance and a fixed-looking reference expression",
            "violates": "source-blindness and partial_source Delta_ref=0",
            "why_allowed_now": "no parent rule forbids source labels in B_ref/counterterms",
            "blocks_theorem": "partial_source Delta_ref theorem-zero",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM998_1_GM_calibrated_reference",
            "construction": "H_ref[S]=H_ref0[S]+epsilon GM_obs(source)",
            "preserves": "same symbolic H_ref form if GM_obs is hidden as calibration data",
            "violates": "derivation of source mass from Q_tau",
            "why_allowed_now": "M_H_ref/source-current equality and no-orbital-import guard are not theorem-owned",
            "blocks_theorem": "Delta_ref_over_MH zero or bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM998_2_material_marker_counterterm",
            "construction": "B_ct = B_ct0 + epsilon theta_A b_ct on a material-labelled branch",
            "preserves": "local covariance if theta_A is treated as branch data",
            "violates": "no material/source marker rule",
            "why_allowed_now": "950 retains marker/source-weight countermodels",
            "blocks_theorem": "source-blind B_ref",
            "valid_for_claim": "false",
        },
    ]


def source_component_template_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "DSC998_0_component_schema",
            "target": "Delta_ref_source_component_over_MH",
            "formula": "abs(partial_source Delta_ref * Delta_source_scale)/M_H_ref",
            "required_columns": "system_id;source_parameter;Delta_source_scale;partial_source_Delta_ref;Delta_ref_units;M_H_ref;M_H_ref_units;B_ref_rule;fixed_branch_id;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "numeric finite same-frame ratio or theorem_zero=true; source path exists; no MISSING markers",
            "current_fill": "SCHEMA_ONLY_MISSING_VALUES",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DSC998_1_theorem_zero_switch",
            "target": "partial_source Delta_ref",
            "formula": "partial_source Delta_ref=0",
            "required_columns": "B_ref_source_blind_theorem;fixed_branch_selector;no_marker_clause;no_GM_calibration;counterterm_rule;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "all source-blindness theorem clauses parent-signed true",
            "current_fill": "MISSING_PARENT_BREF_SOURCE_BLIND_THEOREM",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DSC998_2_finite_bound_row",
            "target": "partial_source Delta_ref finite bound",
            "formula": "abs(partial_source Delta_ref)<=bound_source_ref",
            "required_columns": "derivative_value;bound;units;source_parameter;source_path;equation_ref;extraction_method;valid_for_claim",
            "acceptance_rule": "sourced derivative or bounded finite-difference profile with units",
            "current_fill": "MISSING_NUMERIC_DERIVATIVE_AND_BOUND",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DSC998_3_denominator_sidecar",
            "target": "M_H_ref for source component",
            "formula": "M_H_ref>0 in same frame as Delta_ref",
            "required_columns": "M_H_ref;units;tau_id;frame_id;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "same-frame positive Hamiltonian denominator; no orbital GM substitution",
            "current_fill": "MISSING_SAME_FRAME_MHREF",
            "source_path": "MISSING_SOURCE_FILE",
            "valid_for_claim": "false",
        },
    ]


def strict_refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF998_0_notation_not_proof",
            "rule": "do not treat absence of source arguments in B_ref notation as theorem-zero",
            "enforced_by": "SBT998_1 is useful_but_insufficient and claim gates remain false",
            "status": "enforced",
            "valid_for_claim": "false",
        },
        {
            "refusal_id": "REF998_1_no_source_calibration",
            "rule": "do not allow B_ref, B_ct, or fixed branch to depend on GM_obs/M_fit/source labels unless sourced as a residual",
            "enforced_by": "source leakage channel and countermodel ledgers",
            "status": "enforced",
            "valid_for_claim": "false",
        },
        {
            "refusal_id": "REF998_2_no_downstream_claim",
            "rule": "do not claim Delta_ref, RC994_0, deltaH, FB554_0, or local GR from this component audit",
            "enforced_by": "claim gate rows all claim_allowed=false",
            "status": "enforced",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG998_0_Bref_source_blind",
            "claim": "B_ref is source-blind",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "fixed-branch selector, no-marker clause, no-GM-calibration clause, and counterterm rule are unsigned",
        },
        {
            "gate_id": "CG998_1_partial_source_Delta_ref_zero",
            "claim": "partial_source Delta_ref=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source-blindness theorem is conditional only",
        },
        {
            "gate_id": "CG998_2_Delta_ref_source_component_bound",
            "claim": "Delta_ref_source_component_over_MH has a source-backed bound",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "component row is schema-only with MISSING values/source path/M_H_ref",
        },
        {
            "gate_id": "CG998_3_downstream",
            "claim": "Delta_ref, RC994_0, deltaH, FB554_0, Newton/PPN/R10/local-GR pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "998 covers one derivative component only and does not supply Hamiltonian source-current equality",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC998_0_source_blind_theorem",
            "decision": "do not promote B_ref source-blindness",
            "reason": "the theorem is conditional on a parent-owned fixed-branch/no-marker/counterterm rule that is not present",
            "effect": "partial_source Delta_ref remains retained",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC998_1_countermodel",
            "decision": "retain source-weighted reference countermodels",
            "reason": "they show notation-level source absence is not enough",
            "effect": "future proof must explicitly forbid source labels and GM calibration in B_ref/B_ct/fixed branch",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC998_2_next_route",
            "decision": "target fixed-branch selector or source-coefficient provenance next",
            "reason": "without the selector, every derivative component remains an imposed reference condition",
            "effect": "999 should either sign the selector or prepare a finite source-component input",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md",
            "objective": "derive the fixed-branch selector that makes B_ref source-blind, or require provenance for the finite source component of Delta_ref",
            "include": "fixed branch data, no material/source labels, no GM calibration, counterterm convention, same-frame M_H_ref, source path/equation ref",
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
    leakage: list[dict[str, str]],
    countermodels: list[dict[str, str]],
    component_template: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_ok = (
        len(theorem) >= 7
        and any(row["step_id"] == "SBT998_6_verdict" and row["proof_status"] == "fail_current_claim" for row in theorem)
        and all(row["accepted_for_claim"] == "false" and row["valid_for_claim"] == "false" for row in theorem)
    )
    leakage_ok = len(leakage) >= 6 and all(row["valid_for_claim"] == "false" and row["required_exit"] for row in leakage)
    counter_ok = len(countermodels) >= 3 and all(row["valid_for_claim"] == "false" and row["blocks_theorem"] for row in countermodels)
    template_ok = (
        len(component_template) >= 4
        and all(row["valid_for_claim"] == "false" for row in component_template)
        and all("MISSING" in row["current_fill"] or row["current_fill"].startswith("SCHEMA_ONLY") for row in component_template)
    )
    refusals_ok = all(row["status"] == "enforced" and row["valid_for_claim"] == "false" for row in refusals)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC998_2_next_route" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V998_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V998_1_source_blind_theorem_fail_closed", "result": "pass" if theorem_ok else "fail", "detail": "B_ref source-blind theorem is attempted but not promoted"},
        {"check_id": "V998_2_leakage_channels_covered", "result": "pass" if leakage_ok else "fail", "detail": "source/material/GM/surface/counterterm/source-current leakage channels are recorded"},
        {"check_id": "V998_3_countermodels_retained", "result": "pass" if counter_ok else "fail", "detail": "source-dependent reference countermodels block notation-only proof"},
        {"check_id": "V998_4_component_template_fail_closed", "result": "pass" if template_ok else "fail", "detail": "Delta_ref source component row is source-ready but missing and nonclaim"},
        {"check_id": "V998_5_refusal_policy_enforced", "result": "pass" if refusals_ok else "fail", "detail": "notation-not-proof and no-source-calibration guards enforced"},
        {"check_id": "V998_6_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "B_ref, partial_source Delta_ref, Delta_ref component, and downstream claims are blocked"},
        {"check_id": "V998_7_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "fixed-branch/source-provenance next route recorded"},
        {"check_id": "V998_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "999 target row is present and nonclaim"},
        {"check_id": "V998_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V998_READY",
            "result": "pass" if ready else "fail",
            "detail": "998 B_ref source-blindness gate validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    leakage: list[dict[str, str]],
    countermodels: list[dict[str, str]],
    component_template: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 998 Y5 R10: B_ref Source-Blindness Theorem or Delta_ref Source Component Row",
        "",
        "Status: `Y5_R10_998_Bref_source_blindness_theorem_rejected_current_claim_source_component_row_staged_nonclaim`",
        "",
        "Claim ceiling: no `B_ref` source-blindness theorem, no `partial_source Delta_ref=0`, no source-backed `Delta_ref_source_component_over_MH`, no `Delta_ref` pass, no `RC994_0=0`, no `deltaH` curl closure, no `FB554_0=0`, no Newton/PPN/R10/R11/orbit/local-GR pass.",
        "",
        "## Readout",
        "",
        "998 closes one loophole in our own thinking: writing `B_ref[gamma_ref,tau_ref,C_top]` is not enough. Source-blindness requires a parent-owned fixed-branch selector, no material/source markers, no measured-GM calibration, and a counterterm convention fixed before readout.",
        "",
        "Current MTS does not sign that stack, so `partial_source Delta_ref=0` is not a claim. The source component is now isolated as a finite/provenance row. This is not a loss; it is the theory refusing to let a reference term become a magic pocket.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## B_ref Source-Blindness Theorem Attempt",
        "",
        md_table(theorem, ["step_id", "statement", "mathematical_form", "proof_status", "needed_for", "blocker", "accepted_for_claim", "valid_for_claim"]),
        "",
        "## Source Leakage Channel Audit",
        "",
        md_table(leakage, ["channel_id", "source_leak_channel", "forbidden_form", "current_status", "why_dangerous", "required_exit", "valid_for_claim"]),
        "",
        "## Countermodel Ledger",
        "",
        md_table(countermodels, ["countermodel_id", "construction", "preserves", "violates", "why_allowed_now", "blocks_theorem", "valid_for_claim"]),
        "",
        "## Delta_ref Source Component Template",
        "",
        md_table(component_template, ["row_id", "target", "formula", "required_columns", "acceptance_rule", "current_fill", "source_path", "valid_for_claim"]),
        "",
        "## Strict Refusal Ledger",
        "",
        md_table(refusals, ["refusal_id", "rule", "enforced_by", "status", "valid_for_claim"]),
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
    theorem = source_blind_theorem_rows()
    leakage = source_leakage_channel_rows()
    countermodels = countermodel_rows()
    component_template = source_component_template_rows()
    refusals = strict_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, leakage, countermodels, component_template, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_998_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_998_BREF_SOURCE_BLIND_THEOREM_ATTEMPT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_998_SOURCE_LEAKAGE_CHANNEL_AUDIT.csv", leakage)
    write_csv(OUT / "P8_Y5_R10_998_COUNTERMODEL_LEDGER.csv", countermodels)
    write_csv(OUT / "P8_Y5_R10_998_DELTA_REF_SOURCE_COMPONENT_TEMPLATE.csv", component_template)
    write_csv(OUT / "P8_Y5_R10_998_STRICT_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_998_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_998_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_998_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_998_VALIDATION.csv", validation)
    write_doc(sources, theorem, leakage, countermodels, component_template, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
