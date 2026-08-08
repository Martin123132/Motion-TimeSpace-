from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md"
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


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "S1007_0_handoff_doc",
            "path": "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
            "role": "1006 handoff selecting H_tau integrability and fixed-reference target",
            "needle": "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
        },
        {
            "source_id": "S1007_1_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1006_NEXT_TARGET.csv",
            "role": "machine-readable 1007 target",
            "needle": "delta H_tau",
        },
        {
            "source_id": "S1007_2_integrability_664",
            "path": "source-intake/mts_residuals/P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
            "role": "Hamiltonian charge integrability attempt",
            "needle": "HCI664_6_integrability_verdict",
        },
        {
            "source_id": "S1007_3_source_measure_contract",
            "path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "role": "Hamiltonian source measure contract",
            "needle": "HSM541_1_integrable_charge",
        },
        {
            "source_id": "S1007_4_integrability_reference",
            "path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
            "role": "original integrability/fixed-reference attempt",
            "needle": "HCI554_6_integrability_verdict",
        },
        {
            "source_id": "S1007_5_residual_decomposition",
            "path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv",
            "role": "epsilon_HPiM integrability residual decomposition",
            "needle": "HPRD553_0_integrability",
        },
        {
            "source_id": "S1007_6_noether_chain",
            "path": "source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "role": "parent Noether charge derivation chain",
            "needle": "D505_2_charge_form",
        },
        {
            "source_id": "S1007_7_boundary_charge_contract",
            "path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
            "role": "Hamiltonian boundary charge contract",
            "needle": "HC2_differentiable_integrable_Hxi",
        },
        {
            "source_id": "S1007_8_boundary_status",
            "path": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
            "role": "Delta_symp and B_zero_flux status",
            "needle": "Delta_symp",
        },
        {
            "source_id": "S1007_9_Qtau_decomposition",
            "path": "source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
            "role": "Q_tau^MTS piece ledger",
            "needle": "QDEC993_5_total",
        },
        {
            "source_id": "S1007_10_MHref_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1006_CLAIM_GATE.csv",
            "role": "M_H_ref denominator gate requiring H_tau",
            "needle": "CG1006_0_MHref_positive_same_frame",
        },
        {
            "source_id": "S1007_11_prior_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_1006_VALIDATION.csv",
            "role": "1006 validation pass",
            "needle": "V1006_SUMMARY",
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
                "valid_for_claim": "false",
            }
        )
    return rows


def integrability_theorem_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "HTA1007_0_target",
            "object": "delta H_tau",
            "needed_for_claim": "delta H_tau = int_S(delta Q_tau - i_tau theta) is finite, differentiable, and path-independent",
            "current_evidence": "664 defines this target but does not derive MTS theta/Q_tau",
            "status": "definition_only",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HTA1007_1_parent_theta_Qtau",
            "object": "theta_MTS and Q_tau^MTS",
            "needed_for_claim": "parent MTS action supplies explicit symplectic potential and Noether charge for all local sectors",
            "current_evidence": "993 says only Q_EH is conditional; boundary/extra/projector/matter pieces are not extracted",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HTA1007_2_EH_import_guard",
            "object": "EH covariant phase space",
            "needed_for_claim": "EH charge formalism can be used only after MTS reduces to EH plus signed silent/topological sectors",
            "current_evidence": "664 marks EH as a known conditional reference, not an MTS parent derivation",
            "status": "guardrail_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HTA1007_3_fixed_reference",
            "object": "H_ref and B_ref",
            "needed_for_claim": "reference/counterterm is fixed once and cannot absorb source, radius, time, frame, lambda, or readout changes",
            "current_evidence": "664 reference lock failed; 1000-1005 show Delta_ref components are guarded but unfilled",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HTA1007_4_tau_lock",
            "object": "tau",
            "needed_for_claim": "same observed tau is used in source variation, Hamiltonian charge, boundary reference, clocks, and readout",
            "current_evidence": "685 and 1002 keep stationary tau lock unsigned",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HTA1007_5_symplectic_boundary_flux",
            "object": "Delta_symp and B_zero_flux",
            "needed_for_claim": "extra symplectic/boundary flux vanishes, is fixed topological data, or is source-bounded",
            "current_evidence": "boundary first-row status has zero claim-valid Delta_symp/B_zero_flux rows",
            "status": "fallback_required",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "HTA1007_6_integrability_verdict",
            "object": "integrable H_tau with fixed H_ref",
            "needed_for_claim": "theta_MTS, Q_tau^MTS, fixed reference, tau lock, boundary conditions, zero extra flux, and source/equation paths all parent-signed",
            "current_evidence": "not enough parent symplectic/Noether structure to promote H_tau",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]


def symplectic_residual_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "SRS1007_0_integrability_formula",
            "target": "epsilon_HPiM_integrability_abs",
            "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(B_zero_flux_over_MH)+abs(Delta_symp_over_MH)",
            "required_columns": "system_id;delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;B_zero_flux_over_MH;Delta_symp_over_MH;M_H_ref;theta_source;Q_tau_source;H_ref_source;boundary_condition_source;equation_ref;valid_for_claim",
            "acceptance_rule": "finite numeric same-frame absolute terms, positive sourced M_H_ref, parent theta/Q_tau, fixed reference, no MISSING markers",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SRS1007_1_parent_integrability_zero_switch",
            "target": "epsilon_HPiM_integrability_abs_zero",
            "formula": "theorem_zero=true iff integrability_zero_authority=PARENT_SIGNED_HTAU_INTEGRABILITY_TRUE",
            "required_columns": "theta_MTS_certificate;Q_tau_MTS_certificate;fixed_reference_certificate;tau_lock_certificate;boundary_condition_certificate;symplectic_flux_certificate;source_path;equation_ref",
            "acceptance_rule": "EH import, fitted reference, and assumed boundary silence are rejected",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SRS1007_2_EH_import_guard",
            "target": "EH reference use",
            "formula": "EH theta/Q_tau can be a reference pattern but not a claim source unless MTS parent reduction is signed",
            "required_columns": "MTS_parent_theta_source;MTS_parent_Qtau_source;EH_reduction_certificate;silent_sector_certificate;topological_sector_certificate",
            "acceptance_rule": "known GR formalism alone is not MTS H_tau evidence",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "SRS1007_3_no_fitted_reference",
            "target": "fixed H_ref",
            "formula": "H_ref fixed before source/readout and never fitted to cancel residuals",
            "required_columns": "reference_selector_source;counterterm_convention;pre_readout_timestamp_or_derivation;no_cancellation_guard",
            "acceptance_rule": "fitted reference/counterterm rows are refused",
            "valid_for_claim": "false",
        },
    ]


def candidate_symplectic_rows() -> list[dict[str, str]]:
    base = {
        "system_id": "R10_local_reference_branch",
        "delta_H_tau_nonintegrable_over_MH": "MISSING_DELTA_H_TAU_NONINTEGRABLE_OVER_MH",
        "Delta_ref_over_MH": "MISSING_DELTA_REF_OVER_MH",
        "B_zero_flux_over_MH": "MISSING_B_ZERO_FLUX_OVER_MH",
        "Delta_symp_over_MH": "MISSING_DELTA_SYMP_OVER_MH",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "theta_source": "MISSING_THETA_SOURCE",
        "Q_tau_source": "MISSING_Q_TAU_SOURCE",
        "H_ref_source": "MISSING_H_REF_SOURCE",
        "boundary_condition_source": "MISSING_BOUNDARY_CONDITION_SOURCE",
        "theta_MTS_certificate": "MISSING_THETA_MTS_CERTIFICATE",
        "Q_tau_MTS_certificate": "MISSING_Q_TAU_MTS_CERTIFICATE",
        "fixed_reference_certificate": "MISSING_FIXED_REFERENCE_CERTIFICATE",
        "tau_lock_certificate": "MISSING_TAU_LOCK_CERTIFICATE",
        "boundary_condition_certificate": "MISSING_BOUNDARY_CONDITION_CERTIFICATE",
        "symplectic_flux_certificate": "MISSING_SYMPLECTIC_FLUX_CERTIFICATE",
        "EH_reduction_certificate": "MISSING_EH_REDUCTION_CERTIFICATE",
        "silent_sector_certificate": "MISSING_SILENT_SECTOR_CERTIFICATE",
        "topological_sector_certificate": "MISSING_TOPOLOGICAL_SECTOR_CERTIFICATE",
        "reference_selector_source": "MISSING_REFERENCE_SELECTOR_SOURCE",
        "counterterm_convention": "MISSING_COUNTERTERM_CONVENTION",
        "equation_ref": "MISSING_EQUATION_REF",
        "source_path": "MISSING_SOURCE_PATH",
        "theorem_zero": "false",
        "integrability_zero_authority": "MISSING_PARENT_INTEGRABILITY_SIGNATURE",
        "denominator_source_method": "MISSING_DENOMINATOR_SOURCE_METHOD",
        "no_cancellation_guard": "MISSING_ABS_SUM_GUARD",
        "valid_for_claim": "false",
    }
    variants = [
        ("SRC1007_0_missing_theta_Qtau", "MTS theta/Q_tau sources are missing"),
        ("SRC1007_1_missing_fixed_reference", "fixed H_ref/counterterm convention is missing"),
        ("SRC1007_2_EH_import_only", "EH charge formalism is imported without MTS parent theta/Q_tau"),
        ("SRC1007_3_fitted_reference_attempt", "reference/counterterm is used as a fit/cancellation knob"),
        ("SRC1007_4_missing_MHref", "positive same-frame M_H_ref denominator is missing"),
        ("SRC1007_5_zero_switch_unsigned", "theorem-zero switch is requested without parent-signed integrability"),
        ("SRC1007_6_live_placeholder", "live symplectic residual row is schema-only and cannot be scored"),
    ]
    rows: list[dict[str, str]] = []
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "target": "epsilon_HPiM_integrability_abs", "purpose": purpose}
        if row_id == "SRC1007_2_EH_import_only":
            row["theta_source"] = "EH_REFERENCE_ONLY"
            row["Q_tau_source"] = "EH_REFERENCE_ONLY"
            row["EH_reduction_certificate"] = "MISSING_MTS_PARENT_REDUCTION"
        if row_id == "SRC1007_3_fitted_reference_attempt":
            row["reference_selector_source"] = "POST_READOUT_FITTED_REFERENCE"
            row["counterterm_convention"] = "FITTED_COUNTERTERM"
            row["no_cancellation_guard"] = "FITTED_REFERENCE_CANCELLATION_ATTEMPT"
        if row_id == "SRC1007_5_zero_switch_unsigned":
            row["theorem_zero"] = "true"
            row["integrability_zero_authority"] = "MISSING_PARENT_INTEGRABILITY_SIGNATURE"
        rows.append(row)
    return rows


def is_missing(value: str) -> bool:
    stripped = str(value).strip()
    return not stripped or stripped.upper().startswith("MISSING") or stripped.upper().startswith("SCHEMA_ONLY")


def finite_float(value: str) -> tuple[bool, float | None]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


def path_list_exists(value: str) -> bool:
    if is_missing(value) or value in {"EH_REFERENCE_ONLY", "POST_READOUT_FITTED_REFERENCE", "FITTED_COUNTERTERM"}:
        return False
    paths = [item.strip() for item in value.split(";") if item.strip()]
    if not paths:
        return False
    for item in paths:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / item
        if not path.exists():
            return False
    return True


def evaluate_symplectic(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    component_fields = [
        "delta_H_tau_nonintegrable_over_MH",
        "Delta_ref_over_MH",
        "B_zero_flux_over_MH",
        "Delta_symp_over_MH",
    ]
    component_values: list[float] = []
    for field in component_fields:
        ok, value = finite_float(row.get(field, ""))
        if not ok or value is None:
            reasons.append(f"MISSING_SYMPLECTIC_COMPONENT_{field.upper()}")
        elif value < 0:
            reasons.append(f"NEGATIVE_SYMPLECTIC_COMPONENT_{field.upper()}")
        else:
            component_values.append(value)
    mh_ok, mh_value = finite_float(row.get("M_H_ref", ""))
    if not mh_ok or mh_value is None or mh_value <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    for field in ["M_H_ref_units", "counterterm_convention", "equation_ref"]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    for path_field in ["theta_source", "Q_tau_source", "H_ref_source", "boundary_condition_source", "source_path", "reference_selector_source"]:
        if not path_list_exists(row.get(path_field, "")):
            reasons.append(f"MISSING_EXISTING_{path_field.upper()}")
    certificate_fields = [
        "theta_MTS_certificate",
        "Q_tau_MTS_certificate",
        "fixed_reference_certificate",
        "tau_lock_certificate",
        "boundary_condition_certificate",
        "symplectic_flux_certificate",
    ]
    for field in certificate_fields:
        value = row.get(field, "")
        if is_missing(value):
            reasons.append(f"MISSING_{field.upper()}")
        elif not value.startswith("PARENT_SIGNED_"):
            reasons.append(f"UNSIGNED_{field.upper()}")
    theorem_zero = row.get("theorem_zero", "").strip().lower() == "true"
    parent_signed_zero = theorem_zero and row.get("integrability_zero_authority") == "PARENT_SIGNED_HTAU_INTEGRABILITY_TRUE"
    if theorem_zero and not parent_signed_zero:
        reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_HTAU_INTEGRABILITY")
    if row.get("theta_source") == "EH_REFERENCE_ONLY" or row.get("Q_tau_source") == "EH_REFERENCE_ONLY":
        reasons.append("EH_IMPORT_WITHOUT_MTS_PARENT_THETA_QTAU_REJECTED")
    if row.get("reference_selector_source") == "POST_READOUT_FITTED_REFERENCE" or row.get("counterterm_convention") == "FITTED_COUNTERTERM":
        reasons.append("FITTED_REFERENCE_REJECTED")
    if row.get("denominator_source_method") != "M_H_REF_PARENT_SIGNED":
        reasons.append("M_H_REF_DENOMINATOR_NOT_PARENT_SIGNED")
    if row.get("no_cancellation_guard") != "ABS_SUM_NO_SYMPLECTIC_CANCELLATION":
        reasons.append("MISSING_ABS_SUM_NO_SYMPLECTIC_CANCELLATION_GUARD")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    computed = "NOT_SCORED"
    if not reasons:
        computed = f"{sum(abs(value) for value in component_values):.16e}"
    verdict = "ACCEPT_INTEGRABILITY_OR_SOURCE_BOUND" if not reasons else "REFUSED_MISSING_HTAU_INTEGRABILITY_PROVENANCE"
    return {
        "runner_id": row["candidate_id"].replace("SRC", "SRR"),
        "candidate_id": row["candidate_id"],
        "target": row["target"],
        "verdict": verdict,
        "score_ready": flag(not reasons),
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "computed_epsilon_HPiM_integrability_abs": computed,
        "failure_reasons": ";".join(reasons) if reasons else "none",
        "generated_utc": stamp(),
    }


def symplectic_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_symplectic(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": row["runner_id"].replace("SRR", "SFR"),
            "candidate_id": row["candidate_id"],
            "refusal": row["verdict"],
            "why": row["failure_reasons"],
            "required_exit": "parent MTS theta/Q_tau, fixed reference, tau lock, boundary conditions, positive M_H_ref, source paths, and ABS_SUM_NO_SYMPLECTIC_CANCELLATION",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for row in runner
    ]


def claim_gate_rows(runner: list[dict[str, str]], theorem: list[dict[str, str]]) -> list[dict[str, str]]:
    runner_refuses = all(row["verdict"] == "REFUSED_MISSING_HTAU_INTEGRABILITY_PROVENANCE" for row in runner)
    theorem_fails = any(row["audit_id"] == "HTA1007_6_integrability_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    return [
        {
            "gate_id": "CG1007_0_Htau_integrability",
            "claim": "H_tau is integrable with fixed H_ref",
            "gate_pass": "false",
            "reason": "MTS theta/Q_tau, fixed reference, tau lock, boundary conditions, and symplectic flux theorem are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1007_1_EH_import_guard",
            "claim": "EH covariant phase space alone proves MTS H_tau",
            "gate_pass": "false",
            "reason": "EH is a reference pattern only until the MTS parent theta/Q_tau and reduction are signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1007_2_fitted_reference_guard",
            "claim": "H_ref may be fitted after readout",
            "gate_pass": "false",
            "reason": "post-readout reference/counterterm fitting is rejected",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1007_3_MHref",
            "claim": "M_H_ref denominator can now pass",
            "gate_pass": "false",
            "reason": "H_tau integrability/fixed reference remains blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1007_4_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "symplectic/reference and denominator remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1007_5_FB554_0_local_GR",
            "claim": "FB554_0/local-GR branch passes",
            "gate_pass": "false",
            "reason": "parent Hamiltonian charge is not integrable/source-backed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1007_6_guardrail",
            "claim": "H_tau integrability guardrail is installed",
            "gate_pass": flag(runner_refuses and theorem_fails),
            "reason": "theorem is not promoted and all placeholder/shortcut rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1007_0_integrability_not_claimed",
            "decision": "do not claim integrable H_tau or fixed H_ref",
            "reason": "the parent MTS symplectic potential and Noether charge are not extracted",
            "effect": "M_H_ref, vector norm, RC994_0, and local-GR remain blocked",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1007_1_EH_reference_only",
            "decision": "keep EH charge formalism as a reference pattern only",
            "reason": "importing EH theta/Q without MTS sector reduction would smuggle GR into the proof",
            "effect": "future proof must extract MTS theta/Q_tau or prove exact EH reduction",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1007_2_next_theta_Qtau_target",
            "decision": "move to parent theta/Q_tau extraction",
            "reason": "this is the first missing object in the integrability chain",
            "effect": "1008 should extract or refuse the MTS Noether charge decomposition pieces",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "objective": "extract parent MTS theta and Q_tau pieces, or stage strict nonclaim charge-decomposition residual rows",
            "include": "L_parent, theta_MTS, Q_tau^EH, Q_tau^boundary, Q_tau^extra, Q_tau^projector, matter/source constraint pieces, source/equation paths",
            "exclude": "EH-only import, unowned extra-sector silence, fitted reference, H_tau pass, M_H_ref pass, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
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
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_ok = any(row["audit_id"] == "HTA1007_6_integrability_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem)
    schema_ok = any(row["schema_id"] == "SRS1007_0_integrability_formula" for row in schema) and any(row["schema_id"] == "SRS1007_2_EH_import_guard" for row in schema)
    candidates_ok = len(candidates) >= 7 and all(row["valid_for_claim"] == "false" for row in candidates)
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_HTAU_INTEGRABILITY_PROVENANCE" and row["score_ready"] == "false" for row in runner)
    eh_guard_ok = any(
        row["candidate_id"] == "SRC1007_2_EH_import_only"
        and "EH_IMPORT_WITHOUT_MTS_PARENT_THETA_QTAU_REJECTED" in row["failure_reasons"]
        for row in runner
    )
    fitted_ref_ok = any(
        row["candidate_id"] == "SRC1007_3_fitted_reference_attempt"
        and "FITTED_REFERENCE_REJECTED" in row["failure_reasons"]
        for row in runner
    )
    zero_switch_ok = any(
        row["candidate_id"] == "SRC1007_5_zero_switch_unsigned"
        and "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_HTAU_INTEGRABILITY" in row["failure_reasons"]
        for row in runner
    )
    refusals_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    hta_gate_ok = any(row["gate_id"] == "CG1007_0_Htau_integrability" and row["gate_pass"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1007_2_next_theta_Qtau_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1007_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1007_1_theorem_audit_nonclaim", "result": "pass" if theorem_ok else "fail", "detail": "H_tau integrability theorem remains blocked rather than promoted"},
        {"check_id": "V1007_2_schema_ready", "result": "pass" if schema_ok else "fail", "detail": "symplectic residual, parent-zero, EH guard, and fixed-reference schema rows are present"},
        {"check_id": "V1007_3_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate symplectic rows remain valid_for_claim=false"},
        {"check_id": "V1007_4_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current integrability placeholder/shortcut row"},
        {"check_id": "V1007_5_EH_import_guard", "result": "pass" if eh_guard_ok else "fail", "detail": "EH-only import is refused without MTS parent theta/Q_tau"},
        {"check_id": "V1007_6_fitted_reference_guard", "result": "pass" if fitted_ref_ok else "fail", "detail": "post-readout fitted reference is refused"},
        {"check_id": "V1007_7_zero_switch_guard", "result": "pass" if zero_switch_ok else "fail", "detail": "theorem_zero=true is refused without PARENT_SIGNED_HTAU_INTEGRABILITY_TRUE"},
        {"check_id": "V1007_8_refusal_ledger_nonclaim", "result": "pass" if refusals_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1007_9_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "H_tau, M_H_ref, RC994_0, and local-GR claims stay blocked"},
        {"check_id": "V1007_10_Htau_gate_written", "result": "pass" if hta_gate_ok else "fail", "detail": "H_tau integrability gate is present and blocked"},
        {"check_id": "V1007_11_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "parent theta/Q_tau extraction target decision is written"},
        {"check_id": "V1007_12_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1008 target row is present and nonclaim"},
        {"check_id": "V1007_13_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1007_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1007 H_tau integrability fixed-reference validation summary",
            "generated_utc": stamp(),
        }
    )
    for row in checks:
        row.setdefault("generated_utc", stamp())
    return checks


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 1007 Y5 R10 Htau Integrability Fixed-Reference Theorem Or Symplectic Residual Row",
        "",
        "**Status:** H_tau integrability/fixed-reference theorem attempted, not closed; strict symplectic residual row staged as nonclaim.",
        "",
        "**Claim ceiling:** this checkpoint does not claim integrable H_tau, M_H_ref, vector norm, RC994_0, FB554_0, R10, PPN, WEP, clock, orbital, or local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## Htau Integrability Theorem Audit",
        "",
        md_table(theorem, ["audit_id", "object", "needed_for_claim", "current_evidence", "status", "valid_for_claim"]),
        "",
        "## Symplectic Residual Schema",
        "",
        md_table(schema, ["schema_id", "target", "formula", "required_columns", "acceptance_rule", "valid_for_claim"]),
        "",
        "## Candidate Symplectic Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "theta_source", "Q_tau_source", "H_ref_source", "reference_selector_source", "theorem_zero", "integrability_zero_authority", "valid_for_claim"]),
        "",
        "## Symplectic Runner",
        "",
        md_table(runner, ["runner_id", "candidate_id", "verdict", "score_ready", "claim_allowed", "computed_epsilon_HPiM_integrability_abs", "failure_reasons", "generated_utc"]),
        "",
        "## Refusal Ledger",
        "",
        md_table(refusals, ["refusal_id", "candidate_id", "refusal", "why", "required_exit", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
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
    sources = source_register_rows()
    theorem = integrability_theorem_audit_rows()
    schema = symplectic_residual_schema_rows()
    candidates = candidate_symplectic_rows()
    runner = symplectic_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(runner, theorem)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1007_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1007_HTAU_INTEGRABILITY_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1007_SYMPLECTIC_RESIDUAL_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1007_CANDIDATE_SYMPLECTIC_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1007_SYMPLECTIC_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1007_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1007_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1007_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1007_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1007_VALIDATION.csv", validation)
    write_doc(sources, theorem, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
