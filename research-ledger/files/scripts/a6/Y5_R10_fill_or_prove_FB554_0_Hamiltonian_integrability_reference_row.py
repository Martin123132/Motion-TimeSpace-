from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_FB554_0_attempted_no_theorem_zero_no_source_values_nonclaim"
CLAIM_CEILING = "FB554_0_integrability_reference_fill_gate_only_no_stable_Hamiltonian_source_charge_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "666-Y5-R10-parent-boundary-reference-lock-or-FB554-0-source-value-hunt.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "665-Y5-R10-fill-or-prove-FB554-0-Hamiltonian-integrability-reference-row.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "664_doc": ROOT / "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md",
    "664_validation": RESIDUALS / "P8_Y5_BRR545_664_VALIDATION.csv",
    "664_first_residual": RESIDUALS / "P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv",
    "664_integrability_attempt": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
    "664_obstruction": RESIDUALS / "P8_Y5_R10_664_OBSTRUCTION_LEDGER.csv",
    "554_doc": ROOT / "554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md",
    "554_validation": RESIDUALS / "P8_Y5_BRR545_554_VALIDATION.csv",
    "554_fill_rows": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv",
    "554_evaluator": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_EVALUATOR.csv",
    "554_integrability_attempt": RESIDUALS / "P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
    "548_doc": ROOT / "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md",
    "548_validation": RESIDUALS / "P8_Y5_BRR545_548_VALIDATION.csv",
    "545_doc": ROOT / "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
    "545_validation": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_545_VALIDATION.csv",
    "545_contract": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
    "545_parent_ownership": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv",
    "544_doc": ROOT / "544-Y5-boundary-reference-first-row-data-or-theorem-zero.md",
    "544_validation": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_544_VALIDATION.csv",
    "544_fill_pack": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv",
    "544_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "544_theorem_zero": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv",
    "544_data_source": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_DATA_SOURCE_AUDIT.csv",
    "543_doc": ROOT / "543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "664_doc": "fresh parent result selecting FB554_0 as first hard residual target",
        "664_validation": "prior 664 validation",
        "664_first_residual": "FB554_0 selection and formula",
        "664_integrability_attempt": "Hamiltonian integrability/reference/tau/boundary attempt rows",
        "664_obstruction": "fresh obstruction ledger for Hamiltonian PiM source charge",
        "554_doc": "Hamiltonian charge integrability/reference lock and source equality fill checkpoint",
        "554_validation": "prior 554 validation",
        "554_fill_rows": "current FB554_0 unfilled row with missing markers",
        "554_evaluator": "prior nonclaim evaluator for FB554 rows",
        "554_integrability_attempt": "prior Hamiltonian charge integrability/reference attempt",
        "548_doc": "reference-lock certificate attempt and first numeric-bound fill",
        "548_validation": "prior 548 validation",
        "545_doc": "minimal action clauses for boundary/reference zero",
        "545_validation": "prior 545 validation",
        "545_contract": "minimal parent clauses needed for boundary/reference zero",
        "545_parent_ownership": "ownership audit showing parent clauses are unsigned",
        "544_doc": "data-source and theorem-zero audit for boundary/reference first row",
        "544_validation": "prior 544 validation",
        "544_fill_pack": "boundary/reference first row fill pack",
        "544_status": "boundary/reference first row status",
        "544_theorem_zero": "theorem-zero rejection ledger",
        "544_data_source": "data-source rejection ledger",
        "543_doc": "boundary/reference theorem-or-fill predecessor",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def component_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "component_id": "FBC665_0_delta_H_tau_nonintegrable",
            "component": "delta_H_tau_nonintegrable_over_MH",
            "definition": "normalized obstruction to path-independent Hamiltonian variation for the local time generator",
            "zero_condition": "explicit parent theta and Q_tau exist; delta H_tau=int_S(delta Q_tau-i_tau theta); field-space curl delta_1 delta_2 H_tau - delta_2 delta_1 H_tau vanishes on the local branch",
            "source_or_parent_requirement": "derive theta_MTS, Q_tau_MTS, boundary term, and fixed tau from the parent action or provide a source-backed numerical bound",
            "current_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "why_blocked": "664 and 554 only define the target; current corpus does not provide the full parent symplectic current for all retained sectors",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability_attempt", "554_integrability_attempt", "554_fill_rows"),
            "generated_utc": now,
        },
        {
            "component_id": "FBC665_1_Delta_ref",
            "component": "Delta_ref_over_MH",
            "definition": "normalized reference-subtraction shift between the candidate Hamiltonian charge and its fixed reference branch",
            "zero_condition": "reference/background subtraction is parent-owned and independent of source, radius, time, frame, and readout changes",
            "source_or_parent_requirement": "derive B_ref/reference lock from the parent boundary structure or provide a source-backed numerical bound",
            "current_status": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "why_blocked": "548 did not sign the reference-lock certificate and 544 rejected reference-only zero rows as current-MTS evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "548_validation", "544_theorem_zero", "554_fill_rows"),
            "generated_utc": now,
        },
        {
            "component_id": "FBC665_2_symplectic_boundary_flux",
            "component": "symplectic_boundary_flux_over_MH",
            "definition": "normalized leakage from extra boundary/projector/non-EH terms in delta Q_tau - i_tau theta",
            "zero_condition": "all extra symplectic-boundary fluxes vanish or are fixed topological constants with no local source/readout variation",
            "source_or_parent_requirement": "derive boundary exactness, no vector/tensor hair, projector symplectic silence, and retained-sector flux zero or provide a source-backed numerical bound",
            "current_status": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "why_blocked": "545 parent ownership audit leaves boundary/projector clauses unsigned; 543/544 keep the fill row nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("545_parent_ownership", "545_contract", "544_fill_pack", "543_doc"),
            "generated_utc": now,
        },
        {
            "component_id": "FBC665_3_tau_lock",
            "component": "time_generator_lock",
            "definition": "certificate that source variation, Hamiltonian charge, clock/coframe, and observed readout use the same local time generator",
            "zero_condition": "tau_source=tau_charge=tau_clock=tau_readout and delta tau=0 on the local branch",
            "source_or_parent_requirement": "derive the observed-coframe/time-generator lock from parent matter coupling or provide a source-backed mismatch bound",
            "current_status": "MISSING_TAU_LOCK_CERTIFICATE",
            "why_blocked": "664 leaves same-observed-time/coframe branch open",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability_attempt", "664_obstruction"),
            "generated_utc": now,
        },
        {
            "component_id": "FBC665_4_M_H_ref",
            "component": "M_H_ref",
            "definition": "positive same-frame Hamiltonian reference mass used to normalize FB554_0 components",
            "zero_condition": "not a zero target; must be stable, positive, same-frame, and parent/source-backed",
            "source_or_parent_requirement": "derive or source a stable positive denominator before computing normalized residuals",
            "current_status": "MISSING_STABLE_MH_REF",
            "why_blocked": "544 first-row pack leaves M_H_ref missing for current MTS; reference-only M_H_ref=1 is rejected as claim evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("544_fill_pack", "544_data_source", "544_status"),
            "generated_utc": now,
        },
        {
            "component_id": "FBC665_5_FB5540_total",
            "component": "FB554_0_HPiM_integrability_reference_bound",
            "definition": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(symplectic_boundary_flux_over_MH)",
            "zero_condition": "all three normalized terms individually theorem-zero or source-backed numeric and bounded, with no cancellation credit",
            "source_or_parent_requirement": "complete FBC665_0 through FBC665_4",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "why_blocked": "the numerator terms, tau lock, and denominator are all unsigned or unsourced",
            "valid_for_claim": "false",
            "source_paths": source_list("664_first_residual", "554_fill_rows", "554_evaluator"),
            "generated_utc": now,
        },
    ]


def theorem_zero_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "theorem_id": "TZ665_0_sufficient_contract",
            "target": "FB554_0=0",
            "attempted_route": "if the parent action supplies differentiable covariant phase-space data, a fixed tau, a fixed reference B_ref, and zero extra boundary flux, then FB554_0 vanishes componentwise",
            "required_clauses": "theta_MTS;Q_tau_MTS;delta^2H_tau=0;fixed_B_ref;fixed_tau;zero_extra_symplectic_boundary_flux;positive_MH_ref",
            "current_result": "conditional_theorem_only",
            "failure_or_gap": "sufficient clauses are known, but not owned by the current parent action",
            "survives_as": "contract_for_future_parent_action",
            "valid_for_claim": "false",
            "source_paths": source_list("545_contract", "664_integrability_attempt"),
            "generated_utc": now,
        },
        {
            "theorem_id": "TZ665_1_integrability_zero",
            "target": "delta_H_tau_nonintegrable_over_MH=0",
            "attempted_route": "use covariant Hamiltonian identity delta H_tau=int_S(delta Q_tau-i_tau theta) and require field-space curl zero",
            "required_clauses": "explicit theta_MTS;explicit Q_tau_MTS;annulus constraints;no sector-dependent curl",
            "current_result": "fail_current_claim",
            "failure_or_gap": "theta_MTS and Q_tau_MTS are not fully specified for all retained local sectors",
            "survives_as": "first numerator proof target",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability_attempt", "554_integrability_attempt"),
            "generated_utc": now,
        },
        {
            "theorem_id": "TZ665_2_reference_zero",
            "target": "Delta_ref_over_MH=0",
            "attempted_route": "declare the reference subtraction fixed and source-independent",
            "required_clauses": "parent-owned reference branch;no source/radius/time/frame/readout dependence;no hidden calibration absorption",
            "current_result": "fail_current_claim",
            "failure_or_gap": "reference-only zero rows were rejected and 548 did not sign the reference lock",
            "survives_as": "reference-lock proof or numeric-bound target",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "548_validation", "544_theorem_zero"),
            "generated_utc": now,
        },
        {
            "theorem_id": "TZ665_3_boundary_flux_zero",
            "target": "symplectic_boundary_flux_over_MH=0",
            "attempted_route": "make boundary/projector/non-EH symplectic contributions exact, topological, or silent",
            "required_clauses": "boundary exact cohomology zero;no vector/tensor hair;projector symplectic silence;retained sector flux zero",
            "current_result": "fail_current_claim",
            "failure_or_gap": "545 parent-ownership rows are false for boundary and projector clauses",
            "survives_as": "boundary-flux proof or numeric-bound target",
            "valid_for_claim": "false",
            "source_paths": source_list("545_parent_ownership", "545_contract", "544_fill_pack"),
            "generated_utc": now,
        },
        {
            "theorem_id": "TZ665_4_tau_denominator_guard",
            "target": "well-defined normalized FB554_0",
            "attempted_route": "lock tau and normalize by a positive same-frame M_H_ref",
            "required_clauses": "same observed time generator;positive stable M_H_ref;same-frame source/readout branch",
            "current_result": "fail_current_claim",
            "failure_or_gap": "tau lock and M_H_ref are both missing as claim-valid current-MTS inputs",
            "survives_as": "normalization and clock/coframe guardrail",
            "valid_for_claim": "false",
            "source_paths": source_list("664_obstruction", "544_fill_pack", "544_data_source"),
            "generated_utc": now,
        },
        {
            "theorem_id": "TZ665_5_verdict",
            "target": "FB554_0 theorem-zero",
            "attempted_route": "combine integrability zero, reference zero, boundary flux zero, tau lock, and positive M_H_ref",
            "required_clauses": "TZ665_1;TZ665_2;TZ665_3;TZ665_4",
            "current_result": "fail_current_claim",
            "failure_or_gap": "at least one required clause is unsigned; in fact all numerator clauses remain unsigned or unsourced",
            "survives_as": "closure-only unless 666 signs parent reference/boundary clauses or sources numeric inputs",
            "valid_for_claim": "false",
            "source_paths": source_list("664_first_residual", "554_fill_rows", "554_evaluator"),
            "generated_utc": now,
        },
    ]


def first_fill_row_staged_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "input_id": "FB5540_input_delta_H_tau_nonintegrable",
            "fb_row": "FB554_0_HPiM_integrability_reference_bound",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "value": "",
            "value_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_after_dividing_by_M_H_ref",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "MISSING_PARENT_THETA_QTAU_AND_FIELD_SPACE_CURL_ZERO",
            "valid_for_claim": "false",
            "source_paths": source_list("554_fill_rows", "664_integrability_attempt"),
            "generated_utc": now,
        },
        {
            "input_id": "FB5540_input_Delta_ref",
            "fb_row": "FB554_0_HPiM_integrability_reference_bound",
            "quantity": "Delta_ref_over_MH",
            "value": "",
            "value_status": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_after_dividing_by_M_H_ref",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "MISSING_PARENT_REFERENCE_LOCK",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "544_theorem_zero", "554_fill_rows"),
            "generated_utc": now,
        },
        {
            "input_id": "FB5540_input_symplectic_boundary_flux",
            "fb_row": "FB554_0_HPiM_integrability_reference_bound",
            "quantity": "symplectic_boundary_flux_over_MH",
            "value": "",
            "value_status": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_after_dividing_by_M_H_ref",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "MISSING_BOUNDARY_PROJECTOR_FLUX_ZERO",
            "valid_for_claim": "false",
            "source_paths": source_list("545_parent_ownership", "544_fill_pack", "554_fill_rows"),
            "generated_utc": now,
        },
        {
            "input_id": "FB5540_input_tau_lock",
            "fb_row": "FB554_0_HPiM_integrability_reference_bound",
            "quantity": "time_generator_lock",
            "value": "",
            "value_status": "MISSING_TAU_LOCK_CERTIFICATE",
            "units": "certificate",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "MISSING_SAME_OBSERVED_TIME_GENERATOR",
            "valid_for_claim": "false",
            "source_paths": source_list("664_obstruction", "664_integrability_attempt"),
            "generated_utc": now,
        },
        {
            "input_id": "FB5540_input_M_H_ref",
            "fb_row": "FB554_0_HPiM_integrability_reference_bound",
            "quantity": "M_H_ref",
            "value": "",
            "value_status": "MISSING_STABLE_MH_REF",
            "units": "same_units_as_Hamiltonian_charge",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "MISSING_POSITIVE_SAME_FRAME_DENOMINATOR",
            "valid_for_claim": "false",
            "source_paths": source_list("544_fill_pack", "544_data_source"),
            "generated_utc": now,
        },
        {
            "input_id": "FB5540_total",
            "fb_row": "FB554_0_HPiM_integrability_reference_bound",
            "quantity": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(symplectic_boundary_flux_over_MH)",
            "value": "",
            "value_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "units": "dimensionless",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "NO_CANCELLATION_CREDIT_ALL_COMPONENTS_MUST_PASS",
            "valid_for_claim": "false",
            "source_paths": source_list("554_fill_rows", "554_evaluator", "664_first_residual"),
            "generated_utc": now,
        },
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "evaluator_id": "EV665_0_FB5540_scoreability",
            "row": "FB554_0_HPiM_integrability_reference_bound",
            "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(symplectic_boundary_flux_over_MH)",
            "numeric_status": "not_computed_missing_theorem_zero_or_source_backed_values",
            "pass_status": "not_claimable",
            "reason": "delta_H_tau_nonintegrable_over_MH, Delta_ref_over_MH, symplectic_boundary_flux_over_MH, tau lock, and M_H_ref remain missing or unsigned",
            "claim_effect": "no stable Hamiltonian source charge",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV665_1_no_cancellation_credit",
            "row": "FB554_0_HPiM_integrability_reference_bound",
            "formula": "componentwise nonnegative absolute-value sum",
            "numeric_status": "policy_pass",
            "pass_status": "guardrail",
            "reason": "a future small total cannot be produced by cancellation; every component must be zero/bounded individually",
            "claim_effect": "prevents fake win",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV665_2_current_theory_state",
            "row": "Hamiltonian_PiM_local_branch",
            "formula": "Pi_M^H candidate charge plus FB554_0 gate",
            "numeric_status": "theory_gate_open",
            "pass_status": "blocked_current_claim",
            "reason": "Pi_M^H is still the clean repair notation, but not yet a source-mass operator",
            "claim_effect": "Newton/GR/PPN/R10/R11 remain downstream",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G665_0_sources_exist",
            "gate": "every cited source path exists",
            "result": "pass",
            "detail": "checked by validation source register",
            "claim_effect": "evidence plumbing only",
            "generated_utc": now,
        },
        {
            "gate_id": "G665_1_prior_validations_clean",
            "gate": "prior 664/554/548/545/544 validations are clean",
            "result": "pass",
            "detail": "checked by validation rows",
            "claim_effect": "checkpoint chain usable",
            "generated_utc": now,
        },
        {
            "gate_id": "G665_2_component_audit_complete",
            "gate": "all FB554_0 components audited",
            "result": "pass_nonclaim",
            "detail": "integrability, reference, boundary flux, tau lock, M_H_ref, and total rows written",
            "claim_effect": "scoreability scaffold only",
            "generated_utc": now,
        },
        {
            "gate_id": "G665_3_theorem_zero_failed",
            "gate": "FB554_0 theorem-zero attempted",
            "result": "blocked_as_expected",
            "detail": "sufficient parent contract exists but current MTS has not signed the clauses",
            "claim_effect": "no theorem-zero pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G665_4_fill_row_staged",
            "gate": "first fill row staged with explicit missing markers",
            "result": "pass_nonclaim",
            "detail": "candidate inputs written but valid_for_claim=false",
            "claim_effect": "no numeric pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G665_5_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": "pass",
            "detail": CLAIM_CEILING,
            "claim_effect": "private derivation discipline",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D665_0_theorem_zero",
            "status": "not_proved",
            "meaning": "FB554_0=0 is conditionally possible but not parent-signed in the current corpus",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D665_1_source_values",
            "status": "not_filled",
            "meaning": "no source-backed numeric values exist for the three normalized numerator terms or M_H_ref",
            "claim_status": "false",
            "next_action": "hunt source values only if 666 cannot sign the parent boundary/reference lock",
            "generated_utc": now,
        },
        {
            "decision_id": "D665_2_route",
            "status": "derive_first",
            "meaning": "best route is still derivation-first because numeric bounds on abstract Hamiltonian leakage would face heavier scrutiny",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def prior_validation_failures(source_id: str) -> list[str]:
    rows = read_csv(SOURCE_PATHS[source_id])
    return [row.get("check_id", row.get("validation_id", "?")) for row in rows if row.get("result") != "pass"]


def validation_rows(
    source_rows: list[dict[str, str]],
    component_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": now,
            }
        )

    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    add("V665_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    prior_ids = ["664_validation", "554_validation", "548_validation", "545_validation", "544_validation"]
    prior_failures = {source_id: prior_validation_failures(source_id) for source_id in prior_ids}
    flat_prior_failures = [f"{source_id}:{failure}" for source_id, failures in prior_failures.items() for failure in failures]
    add("V665_1_prior_validations_clean", not flat_prior_failures, "prior_failures=" + ";".join(flat_prior_failures))

    component_ids = {row["component_id"] for row in component_rows}
    required_components = {
        "FBC665_0_delta_H_tau_nonintegrable",
        "FBC665_1_Delta_ref",
        "FBC665_2_symplectic_boundary_flux",
        "FBC665_3_tau_lock",
        "FBC665_4_M_H_ref",
        "FBC665_5_FB5540_total",
    }
    add("V665_2_component_coverage", required_components.issubset(component_ids), "component_ids=" + ";".join(sorted(component_ids)))

    component_statuses = [row["current_status"] for row in component_rows]
    add("V665_3_components_unfilled", all(("MISSING" in status or status.startswith("NOT_COMPUTED")) for status in component_statuses), "statuses=" + ";".join(sorted(set(component_statuses))))

    theorem_ids = {row["theorem_id"] for row in theorem_rows}
    required_theorems = {"TZ665_0_sufficient_contract", "TZ665_1_integrability_zero", "TZ665_2_reference_zero", "TZ665_3_boundary_flux_zero", "TZ665_4_tau_denominator_guard", "TZ665_5_verdict"}
    add("V665_4_theorem_zero_attempt_coverage", required_theorems.issubset(theorem_ids), "theorem_ids=" + ";".join(sorted(theorem_ids)))

    theorem_verdicts = [row for row in theorem_rows if row["theorem_id"] == "TZ665_5_verdict" and row["current_result"] == "fail_current_claim"]
    add("V665_5_theorem_zero_not_claimed", len(theorem_verdicts) == 1, "verdict_rows=" + str(len(theorem_verdicts)))

    fill_ids = {row["input_id"] for row in fill_rows}
    required_fill_ids = {
        "FB5540_input_delta_H_tau_nonintegrable",
        "FB5540_input_Delta_ref",
        "FB5540_input_symplectic_boundary_flux",
        "FB5540_input_tau_lock",
        "FB5540_input_M_H_ref",
        "FB5540_total",
    }
    add("V665_6_fill_row_coverage", required_fill_ids.issubset(fill_ids), "input_ids=" + ";".join(sorted(fill_ids)))

    missing_markers = [row["value_status"] for row in fill_rows if "MISSING" in row["value_status"] or row["value_status"].startswith("NOT_COMPUTED")]
    add("V665_7_fill_rows_explicitly_missing", len(missing_markers) == len(fill_rows), "missing_or_not_computed_rows=" + str(len(missing_markers)))

    evaluator_claims = [row for row in evaluator_data if row["valid_for_claim"] != "false" or row["pass_status"] not in {"not_claimable", "guardrail", "blocked_current_claim"}]
    add("V665_8_evaluator_nonclaim", not evaluator_claims, "claimlike_evaluator_rows=" + str(len(evaluator_claims)))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (component_rows, theorem_rows, fill_rows, evaluator_data)
        for row in row_group
    ]
    add("V665_9_no_generated_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    blocked_gates = {row["gate_id"] for row in gate_rows if row["result"] == "blocked_as_expected"}
    add("V665_10_blocked_gate_present", "G665_3_theorem_zero_failed" in blocked_gates, "blocked_gates=" + ";".join(sorted(blocked_gates)))

    next_targets = [row for row in decision if row["next_action"] == NEXT_TARGET]
    add("V665_11_next_target_selected", bool(next_targets), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V665_12_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V665_13_status_nonclaim", STATUS.endswith("nonclaim") and "no_stable_Hamiltonian_source_charge" in CLAIM_CEILING, STATUS)

    return rows


def nonclaim_summary_rows(
    component_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    blocked_gates = [row["gate_id"] for row in gate_rows if row["result"] in {"blocked_as_expected", "pass_nonclaim"}]
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "component_rows": str(len(component_rows)),
            "theorem_zero_rows": str(len(theorem_rows)),
            "fill_rows": str(len(fill_rows)),
            "evaluator_rows": str(len(evaluator_data)),
            "blocked_or_nonclaim_gates": ";".join(blocked_gates),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    component_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 665 - Y5 R10 Fill Or Prove FB554-0 Hamiltonian Integrability Reference Row

## Verdict

665 tried the right thing first: prove the local Hamiltonian leakage row away before reaching for numeric duct tape.

The conditional route is real:

```text
FB554_0 = abs(delta_H_tau_nonintegrable_over_MH)
        + abs(Delta_ref_over_MH)
        + abs(symplectic_boundary_flux_over_MH)
```

would vanish if the parent action supplies an integrable `H_tau`, a parent-owned fixed reference, a fixed local time generator, zero extra symplectic/boundary flux, and a positive same-frame `M_H_ref`.

But the current corpus does not yet sign those clauses. So `FB554_0` is not proved zero and is not numerically filled. It remains a scored, explicit closure gate.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Component Audit

{markdown_table(component_rows, ["component_id", "component", "definition", "zero_condition", "current_status", "why_blocked", "valid_for_claim"])}

## Theorem-Zero Attempt

{markdown_table(theorem_rows, ["theorem_id", "target", "attempted_route", "required_clauses", "current_result", "failure_or_gap", "survives_as", "valid_for_claim"])}

## First Fill Row

{markdown_table(fill_rows, ["input_id", "fb_row", "quantity", "value_status", "units", "source_file", "assumptions", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "row", "formula", "numeric_status", "pass_status", "reason", "claim_effect", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "component_rows", "theorem_zero_rows", "fill_rows", "evaluator_rows", "blocked_or_nonclaim_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is not a defeat; it is the right kind of locked door. The theory now knows exactly what it must own before `Pi_M^H` can be treated as a stable source-mass operator: integrability, reference lock, boundary silence, tau lock, and denominator normalization. Until then there is no local-GR, PPN, R10, R11, or Newton-source claim from this branch.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    component_rows = component_audit_rows()
    theorem_rows = theorem_zero_attempt_rows()
    fill_rows = first_fill_row_staged_rows()
    evaluator_data = evaluator_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, component_rows, theorem_rows, fill_rows, evaluator_data, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(component_rows, theorem_rows, fill_rows, evaluator_data, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_665_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_665_FB5540_COMPONENT_AUDIT.csv",
        component_rows,
        [
            "component_id",
            "component",
            "definition",
            "zero_condition",
            "source_or_parent_requirement",
            "current_status",
            "why_blocked",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_665_THEOREM_ZERO_ATTEMPT.csv",
        theorem_rows,
        [
            "theorem_id",
            "target",
            "attempted_route",
            "required_clauses",
            "current_result",
            "failure_or_gap",
            "survives_as",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_665_FIRST_FILL_ROW_STAGED.csv",
        fill_rows,
        [
            "input_id",
            "fb_row",
            "quantity",
            "value",
            "value_status",
            "units",
            "source_file",
            "assumptions",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_665_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "row", "formula", "numeric_status", "pass_status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_665_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_665_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_665_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "component_rows",
            "theorem_zero_rows",
            "fill_rows",
            "evaluator_rows",
            "blocked_or_nonclaim_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_665_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(source_rows, component_rows, theorem_rows, fill_rows, evaluator_data, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"component_rows={len(component_rows)}")
    print(f"theorem_zero_rows={len(theorem_rows)}")
    print(f"fill_rows={len(fill_rows)}")
    print(f"evaluator_rows={len(evaluator_data)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
