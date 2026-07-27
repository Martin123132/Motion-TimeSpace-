from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_boundary_reference_lock_attempt_failed_current_claim_FB5540_source_value_hunt_staged_nonclaim"
CLAIM_CEILING = "parent_boundary_reference_lock_and_FB5540_source_hunt_only_no_stable_Hamiltonian_source_charge_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "666-Y5-R10-parent-boundary-reference-lock-or-FB554-0-source-value-hunt.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "665_doc": ROOT / "665-Y5-R10-fill-or-prove-FB554-0-Hamiltonian-integrability-reference-row.md",
    "665_validation": RESIDUALS / "P8_Y5_BRR545_665_VALIDATION.csv",
    "665_component_audit": RESIDUALS / "P8_Y5_R10_665_FB5540_COMPONENT_AUDIT.csv",
    "665_theorem_zero": RESIDUALS / "P8_Y5_R10_665_THEOREM_ZERO_ATTEMPT.csv",
    "665_fill_row": RESIDUALS / "P8_Y5_R10_665_FIRST_FILL_ROW_STAGED.csv",
    "664_validation": RESIDUALS / "P8_Y5_BRR545_664_VALIDATION.csv",
    "664_integrability_attempt": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
    "664_obstruction": RESIDUALS / "P8_Y5_R10_664_OBSTRUCTION_LEDGER.csv",
    "554_doc": ROOT / "554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md",
    "554_validation": RESIDUALS / "P8_Y5_BRR545_554_VALIDATION.csv",
    "554_fill_rows": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv",
    "553_doc": ROOT / "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md",
    "553_validation": RESIDUALS / "P8_Y5_BRR545_553_VALIDATION.csv",
    "552_doc": ROOT / "552-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt.md",
    "552_validation": RESIDUALS / "P8_Y5_BRR545_552_VALIDATION.csv",
    "552_zero_contract": RESIDUALS / "P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
    "552_repair_attempt": RESIDUALS / "P8_Y5_BRR545_FIRST_REPAIR_ATTEMPT.csv",
    "550_doc": ROOT / "550-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill.md",
    "550_validation": RESIDUALS / "P8_Y5_BRR545_550_VALIDATION.csv",
    "549_doc": ROOT / "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
    "549_validation": RESIDUALS / "P8_Y5_BRR545_549_VALIDATION.csv",
    "548_doc": ROOT / "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md",
    "548_validation": RESIDUALS / "P8_Y5_BRR545_548_VALIDATION.csv",
    "545_contract": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
    "545_ownership": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv",
    "544_fill_pack": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_FILL_PACK.csv",
    "544_theorem_zero": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv",
    "544_data_source": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_DATA_SOURCE_AUDIT.csv",
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
        "665_doc": "immediate predecessor selecting parent boundary/reference lock or source-value hunt",
        "665_validation": "prior 665 validation",
        "665_component_audit": "FB554_0 component gaps",
        "665_theorem_zero": "failed theorem-zero attempt for FB554_0",
        "665_fill_row": "staged missing FB554_0 inputs",
        "664_validation": "prior 664 validation",
        "664_integrability_attempt": "Hamiltonian integrability/reference/tau/boundary attempt",
        "664_obstruction": "Hamiltonian PiM obstruction ledger",
        "554_doc": "Hamiltonian charge integrability/reference lock attempt",
        "554_validation": "prior 554 validation",
        "554_fill_rows": "FB554_0 original unfilled row",
        "553_doc": "Hamiltonian PiM repair failure and residual decomposition",
        "553_validation": "prior 553 validation",
        "552_doc": "BRR545 parent-action zero-theorem contract and first repair candidate",
        "552_validation": "prior 552 validation",
        "552_zero_contract": "explicit BRR545 parent action zero-theorem clauses",
        "552_repair_attempt": "Hamiltonian PiM first repair rows",
        "550_doc": "projector symplectic silence failure",
        "550_validation": "prior 550 validation",
        "549_doc": "boundary cohomology/no-hair failure",
        "549_validation": "prior 549 validation",
        "548_doc": "reference-lock certificate failure",
        "548_validation": "prior 548 validation",
        "545_contract": "minimal action clauses for boundary/reference zero",
        "545_ownership": "parent ownership audit for minimal clauses",
        "544_fill_pack": "boundary/reference first row fill pack",
        "544_theorem_zero": "theorem-zero rejection ledger",
        "544_data_source": "data-source rejection ledger",
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


def parent_lock_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "PLA666_0_target",
            "target": "parent boundary/reference lock sufficient for FB554_0 theorem-zero",
            "mathematical_form": "S_parent=int_M L_MTS + int_boundary B_ref; delta L=E_A delta Phi^A+dTheta; delta H_tau=int_S(delta Q_tau-i_tau Theta)-delta H_ref",
            "required_ownership": "L_MTS, Theta, Q_tau, B_ref, tau, boundary class, Pi_M^H, and M_H_ref fixed before readout",
            "current_result": "target_defined",
            "why_not_signed": "a sufficient target is not yet a parent-action derivation",
            "activated_FB5540_input": "all",
            "valid_for_claim": "false",
            "source_paths": source_list("665_theorem_zero", "552_zero_contract", "545_contract"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PLA666_1_fixed_B_ref",
            "target": "reference subtraction is parent-owned and source/readout independent",
            "mathematical_form": "partial_{source,r,t,frame,lambda} Delta_ref = 0; B_ref=B_ref[boundary_class,tau_ref,g_ref] only",
            "required_ownership": "explicit B_ref variation ledger and fixed reference branch",
            "current_result": "fail_current_claim",
            "why_not_signed": "548 and 545 leave reference lock as a contract, not a current parent result",
            "activated_FB5540_input": "Delta_ref_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "548_validation", "545_ownership"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PLA666_2_integrable_theta_Qtau",
            "target": "Hamiltonian charge variation is integrable",
            "mathematical_form": "delta_1 delta_2 H_tau - delta_2 delta_1 H_tau = int_S omega(Phi;delta_1 Phi,delta_2 Phi,L_tau Phi)=0",
            "required_ownership": "explicit Theta_MTS and Q_tau_MTS for every retained local sector",
            "current_result": "fail_current_claim",
            "why_not_signed": "664/554 do not provide the fully varied parent symplectic current",
            "activated_FB5540_input": "delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability_attempt", "554_fill_rows", "553_doc"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PLA666_3_boundary_class",
            "target": "exact/improvement boundary flux vanishes on the compact linked exterior",
            "mathematical_form": "B_imp=dC with int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0",
            "required_ownership": "parent-selected trivial relative boundary class, not a post-readout choice",
            "current_result": "fail_current_claim",
            "why_not_signed": "549 found the cohomology route conditional but not parent-selected",
            "activated_FB5540_input": "symplectic_boundary_flux_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "549_validation", "545_ownership"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PLA666_4_no_vector_tensor_hair",
            "target": "boundary stress has no vector, trace-free tensor, shear, marker, or derivative hair",
            "mathematical_form": "T_B^TF=0; T_B^vector=0; n_mu P_loc_nu T_B^{mu nu}=0; partial_{t,r,frame}T_B=0",
            "required_ownership": "homogeneous scalar marker-free boundary action derived from parent dynamics",
            "current_result": "fail_current_claim",
            "why_not_signed": "scalar/volume no-flux is not enough to remove vector/tensor boundary flux",
            "activated_FB5540_input": "symplectic_boundary_flux_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "545_contract", "544_theorem_zero"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PLA666_5_projector_silence",
            "target": "Pi_M^H or any remaining mass projector is symplectically silent",
            "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H; [d,Pi_M]J_H=0; delta Pi_M=0 or exact zero-flux",
            "required_ownership": "parent-fixed charge functional/domain and same-frame Hilbert-source equality",
            "current_result": "fail_current_claim",
            "why_not_signed": "550 and 553 demote independent Pi_M proof credit; Hamiltonian PiM is a candidate but not signed",
            "activated_FB5540_input": "symplectic_boundary_flux_over_MH;delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": "false",
            "source_paths": source_list("550_doc", "550_validation", "553_doc"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PLA666_6_tau_and_denominator",
            "target": "same local time generator and positive denominator are locked",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_readout; delta tau=0; M_H_ref>0 and GM_orbit=G_ref M_H_ref",
            "required_ownership": "same observed coframe and source-normalized Gauss/orbital readout",
            "current_result": "fail_current_claim",
            "why_not_signed": "tau lock, M_H_ref, and measured-GM calibration remain downstream",
            "activated_FB5540_input": "time_generator_lock;M_H_ref",
            "valid_for_claim": "false",
            "source_paths": source_list("665_component_audit", "664_obstruction", "544_data_source"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PLA666_7_verdict",
            "target": "parent boundary/reference lock closes FB554_0",
            "mathematical_form": "FB554_0=0 componentwise",
            "required_ownership": "PLA666_1 through PLA666_6 all signed",
            "current_result": "fail_current_claim",
            "why_not_signed": "every hard clause is either conditional, retained, or missing source-backed values",
            "activated_FB5540_input": "FB554_0_HPiM_integrability_reference_bound",
            "valid_for_claim": "false",
            "source_paths": source_list("665_theorem_zero", "554_fill_rows", "552_zero_contract"),
            "generated_utc": now,
        },
    ]


def clause_test_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "CL666_0_reference_lock",
            "needed_for": "Delta_ref_over_MH",
            "pass_condition": "B_ref and Delta_ref are fixed by parent data and have zero source/surface/time/frame/range derivatives",
            "current_result": "fail_current_claim",
            "missing": "explicit parent B_ref and reference-branch variation ledger",
            "repair_or_source_fallback": "write B_ref ansatz and vary it, or source Delta_ref_over_MH plus profiles",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CL666_1_integrability",
            "needed_for": "delta_H_tau_nonintegrable_over_MH",
            "pass_condition": "field-space curl of delta H_tau vanishes for retained MTS sectors",
            "current_result": "fail_current_claim",
            "missing": "Theta_MTS, Q_tau_MTS, and sector-by-sector symplectic current",
            "repair_or_source_fallback": "derive explicit parent variation ledger, or source bound on nonintegrable Hamiltonian leakage",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CL666_2_boundary_flux",
            "needed_for": "symplectic_boundary_flux_over_MH",
            "pass_condition": "boundary exact/cohomology terms and no-hair terms produce zero compact linked-surface flux",
            "current_result": "fail_current_claim",
            "missing": "parent-selected relative class and vector/tensor hair exclusion",
            "repair_or_source_fallback": "derive boundary action/nohair, or source B_zero_flux_over_MH and derivative profiles",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CL666_3_projector_silence",
            "needed_for": "symplectic_boundary_flux_over_MH;delta_H_tau_nonintegrable_over_MH",
            "pass_condition": "mass channel is Hamiltonian charge data with no independent Hodge/projector stress",
            "current_result": "repair_candidate_open_but_unsigned",
            "missing": "Pi_M^H integrability and same-frame Hilbert/source equality",
            "repair_or_source_fallback": "continue Hamiltonian PiM repair, or source commutator/projector-stress envelope",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CL666_4_tau_lock",
            "needed_for": "time_generator_lock",
            "pass_condition": "one observed local time generator is used by clocks, source variation, charge, and readout",
            "current_result": "fail_current_claim",
            "missing": "parent matter/coframe functor tying tau to observed clocks and source current",
            "repair_or_source_fallback": "derive tau/coframe lock, or source a mismatch bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CL666_5_denominator",
            "needed_for": "M_H_ref",
            "pass_condition": "M_H_ref is positive, same-frame, and calibrated to measured GM without circular substitution",
            "current_result": "fail_current_claim",
            "missing": "same-frame source-measure theorem and Poisson/Gauss/orbital readout",
            "repair_or_source_fallback": "derive measured-GM denominator, or keep M_H_ref unsourced",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CL666_6_source_hunt_readiness",
            "needed_for": "FB554_0_source_value_hunt",
            "pass_condition": "each missing quantity has a source-ready row, units, arena links, and valid_for_claim=false until real values exist",
            "current_result": "pass_nonclaim",
            "missing": "real source-backed values or theorem-zero certificates",
            "repair_or_source_fallback": "use the 666 hunt ledger only after parent-action route fails again",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def source_value_hunt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "hunt_id": "SVH666_0_delta_H_tau",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "parent_or_source_requirement": "field-space curl of delta H_tau, normalized by M_H_ref, from explicit MTS theta/Q_tau variation",
            "acceptable_source_kind": "parent variation ledger or finite-shell symbolic/numeric calculation",
            "units": "dimensionless",
            "arena_links": "R3_gamma;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
            "value_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_PARENT_THETA_QTAU_AND_FIELD_SPACE_CURL_ZERO",
            "valid_for_claim": "false",
            "source_paths": source_list("665_fill_row", "664_integrability_attempt", "554_fill_rows"),
            "generated_utc": now,
        },
        {
            "hunt_id": "SVH666_1_Delta_ref",
            "quantity": "Delta_ref_over_MH",
            "parent_or_source_requirement": "fixed reference subtraction shift and derivative profiles, normalized by M_H_ref",
            "acceptable_source_kind": "B_ref theorem-zero certificate or source-backed Delta_ref value/profile table",
            "units": "dimensionless",
            "arena_links": "R3_gamma;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
            "value_status": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_PARENT_REFERENCE_LOCK",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "545_ownership", "544_theorem_zero"),
            "generated_utc": now,
        },
        {
            "hunt_id": "SVH666_2_symplectic_boundary_flux",
            "quantity": "symplectic_boundary_flux_over_MH",
            "parent_or_source_requirement": "extra symplectic/boundary/projector leakage through linked surfaces, normalized by M_H_ref",
            "acceptable_source_kind": "boundary/projector theorem-zero certificate or source-backed flux integral/profile",
            "units": "dimensionless",
            "arena_links": "R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
            "value_status": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_BOUNDARY_PROJECTOR_FLUX_ZERO",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "550_doc", "545_ownership"),
            "generated_utc": now,
        },
        {
            "hunt_id": "SVH666_3_tau_lock",
            "quantity": "time_generator_lock",
            "parent_or_source_requirement": "same observed time generator for source variation, charge, clocks, and readout",
            "acceptable_source_kind": "parent matter/coframe functor theorem or source-backed mismatch bound",
            "units": "certificate_or_dimensionless_mismatch",
            "arena_links": "R1_WEP_source_charge;R9_Gdot;clock;orbital",
            "value_status": "MISSING_TAU_LOCK_CERTIFICATE",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_SAME_OBSERVED_TIME_GENERATOR",
            "valid_for_claim": "false",
            "source_paths": source_list("665_component_audit", "664_obstruction"),
            "generated_utc": now,
        },
        {
            "hunt_id": "SVH666_4_M_H_ref",
            "quantity": "M_H_ref",
            "parent_or_source_requirement": "positive same-frame Hamiltonian/source denominator tied to measured GM without circular substitution",
            "acceptable_source_kind": "source-measure plus Poisson/Gauss/orbital derivation or source-backed denominator row",
            "units": "mass_or_GM_declared",
            "arena_links": "R1_WEP_source_charge;R3_gamma;R9_Gdot;orbital;PPN",
            "value_status": "MISSING_STABLE_MH_REF",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_POSITIVE_SAME_FRAME_DENOMINATOR",
            "valid_for_claim": "false",
            "source_paths": source_list("544_fill_pack", "544_data_source", "553_doc"),
            "generated_utc": now,
        },
        {
            "hunt_id": "SVH666_5_B_zero_flux",
            "quantity": "B_zero_flux_over_MH",
            "parent_or_source_requirement": "exact/improvement boundary flux through compact linked surface pair",
            "acceptable_source_kind": "relative cohomology/no-hair theorem-zero or source-backed boundary flux value/profile",
            "units": "dimensionless",
            "arena_links": "R4_beta;R7_alpha3;R8_xi;R9_Gdot;R11_EH_operator_ledger",
            "value_status": "MISSING_B_ZERO_FLUX_NUMERIC_OR_THEOREM_ZERO",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_BOUNDARY_EXACT_COHOMOLOGY_ZERO_AND_NO_VECTOR_TENSOR_HAIR",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "544_fill_pack", "545_contract"),
            "generated_utc": now,
        },
        {
            "hunt_id": "SVH666_6_Delta_symp",
            "quantity": "Delta_symp_over_MH",
            "parent_or_source_requirement": "reference plus exterior symplectic/projector transfer obstruction",
            "acceptable_source_kind": "reference/projector theorem-zero or source-backed Delta_symp value/profile",
            "units": "dimensionless",
            "arena_links": "R3_gamma;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
            "value_status": "MISSING_DELTA_SYMP_NUMERIC_OR_THEOREM_ZERO",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_REFERENCE_LOCK_AND_PROJECTOR_SYMPLECTIC_SILENCE",
            "valid_for_claim": "false",
            "source_paths": source_list("548_doc", "550_doc", "544_fill_pack"),
            "generated_utc": now,
        },
        {
            "hunt_id": "SVH666_7_commutator_projector",
            "quantity": "commutator_projector_stress_over_MH",
            "parent_or_source_requirement": "integrals of [d,Pi_M]J_H and (delta Pi_M)J_H if any non-Hamiltonian projector remains",
            "acceptable_source_kind": "old PiM demotion/equality theorem or source-backed commutator/projector-stress bound",
            "units": "dimensionless",
            "arena_links": "R1_WEP_source_charge;R3_gamma;R4_beta;R7_alpha3;R8_xi;R10_fifth_force;R11_EH_operator_ledger",
            "value_status": "MISSING_COMMUTATOR_PROJECTOR_NUMERIC_OR_THEOREM_ZERO",
            "source_file": "MISSING_SOURCE_FILE",
            "blocker": "MISSING_PROJECTOR_SYMPLECTIC_SILENCE",
            "valid_for_claim": "false",
            "source_paths": source_list("550_doc", "553_doc", "552_repair_attempt"),
            "generated_utc": now,
        },
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "evaluator_id": "EV666_0_parent_lock",
            "target": "parent_boundary_reference_lock",
            "numeric_status": "not_numeric",
            "pass_status": "not_claimable",
            "reason": "reference lock, integrability, boundary class/nohair, projector silence, tau lock, and M_H_ref are not parent-owned",
            "claim_effect": "FB554_0 remains open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV666_1_source_value_hunt",
            "target": "FB554_0_source_value_hunt",
            "numeric_status": "source_ready_nonclaim",
            "pass_status": "guardrail",
            "reason": "source rows now state exactly what counts, but every row still has MISSING_SOURCE_FILE and valid_for_claim=false",
            "claim_effect": "data plumbing only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV666_2_best_next_route",
            "target": "next_derivation_step",
            "numeric_status": "not_numeric",
            "pass_status": "derive_first",
            "reason": "a numeric hunt for abstract Hamiltonian leakage would be weak unless the parent boundary action is first written and varied",
            "claim_effect": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "G666_0_sources_exist",
            "gate": "every cited source path exists",
            "result": "pass",
            "detail": "checked by validation",
            "claim_effect": "evidence plumbing only",
            "generated_utc": now,
        },
        {
            "gate_id": "G666_1_prior_validations_clean",
            "gate": "prior 665/664/554/553/552/550/549/548 validations are clean",
            "result": "pass",
            "detail": "checked by validation",
            "claim_effect": "checkpoint chain usable",
            "generated_utc": now,
        },
        {
            "gate_id": "G666_2_parent_lock_attempt_complete",
            "gate": "parent boundary/reference lock was attempted clause-by-clause",
            "result": "blocked_as_expected",
            "detail": "all hard clauses remain conditional or unsigned",
            "claim_effect": "no FB554_0 theorem-zero",
            "generated_utc": now,
        },
        {
            "gate_id": "G666_3_source_hunt_staged",
            "gate": "FB554_0 source-value hunt rows are staged",
            "result": "pass_nonclaim",
            "detail": "all rows are source-ready but have missing markers and valid_for_claim=false",
            "claim_effect": "no numeric pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G666_4_no_substitution_shortcut",
            "gate": "orbital GM/reference-only zeros cannot substitute for parent source charge",
            "result": "pass",
            "detail": "M_H_ref and reference-only rows stay rejected as claim evidence",
            "claim_effect": "prevents circular win",
            "generated_utc": now,
        },
        {
            "gate_id": "G666_5_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": "pass",
            "detail": CLAIM_CEILING,
            "claim_effect": "private derivation audit only",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D666_0_parent_lock",
            "status": "not_signed",
            "meaning": "the desired parent boundary/reference lock is a valid sufficient theorem shape but is not owned by the current corpus",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D666_1_source_hunt",
            "status": "staged_nonclaim",
            "meaning": "source-value rows now identify the exact quantities needed if derivation fails again",
            "claim_status": "false",
            "next_action": "use only after explicit parent boundary action/variation route fails",
            "generated_utc": now,
        },
        {
            "decision_id": "D666_2_best_route",
            "status": "derive_first",
            "meaning": "the least-scrutiny route is to write an explicit parent boundary action ansatz and variation ledger, not to invent numerical leakage priors",
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
    parent_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    hunt_rows: list[dict[str, str]],
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
    add("V666_0_sources_exist", not missing_sources, "missing=" + ";".join(missing_sources))

    prior_ids = ["665_validation", "664_validation", "554_validation", "553_validation", "552_validation", "550_validation", "549_validation", "548_validation"]
    flat_prior_failures = [
        f"{source_id}:{failure}"
        for source_id in prior_ids
        for failure in prior_validation_failures(source_id)
    ]
    add("V666_1_prior_validations_clean", not flat_prior_failures, "prior_failures=" + ";".join(flat_prior_failures))

    parent_ids = {row["attempt_id"] for row in parent_rows}
    required_parent = {f"PLA666_{index}_{suffix}" for index, suffix in [
        (0, "target"),
        (1, "fixed_B_ref"),
        (2, "integrable_theta_Qtau"),
        (3, "boundary_class"),
        (4, "no_vector_tensor_hair"),
        (5, "projector_silence"),
        (6, "tau_and_denominator"),
        (7, "verdict"),
    ]}
    add("V666_2_parent_lock_attempt_coverage", required_parent.issubset(parent_ids), "attempt_ids=" + ";".join(sorted(parent_ids)))

    verdict_rows = [row for row in parent_rows if row["attempt_id"] == "PLA666_7_verdict" and row["current_result"] == "fail_current_claim"]
    add("V666_3_parent_lock_not_signed", len(verdict_rows) == 1, "verdict_rows=" + str(len(verdict_rows)))

    clause_ids = {row["clause_id"] for row in clause_rows}
    required_clauses = {"CL666_0_reference_lock", "CL666_1_integrability", "CL666_2_boundary_flux", "CL666_3_projector_silence", "CL666_4_tau_lock", "CL666_5_denominator", "CL666_6_source_hunt_readiness"}
    add("V666_4_clause_test_coverage", required_clauses.issubset(clause_ids), "clause_ids=" + ";".join(sorted(clause_ids)))

    hunt_ids = {row["hunt_id"] for row in hunt_rows}
    required_hunt_ids = {"SVH666_0_delta_H_tau", "SVH666_1_Delta_ref", "SVH666_2_symplectic_boundary_flux", "SVH666_3_tau_lock", "SVH666_4_M_H_ref", "SVH666_5_B_zero_flux", "SVH666_6_Delta_symp", "SVH666_7_commutator_projector"}
    add("V666_5_source_hunt_coverage", required_hunt_ids.issubset(hunt_ids), "hunt_ids=" + ";".join(sorted(hunt_ids)))

    missing_hunt_rows = [row for row in hunt_rows if "MISSING" in row["value_status"] and row["source_file"] == "MISSING_SOURCE_FILE"]
    add("V666_6_hunt_rows_remain_unfilled", len(missing_hunt_rows) == len(hunt_rows), "missing_rows=" + str(len(missing_hunt_rows)))

    all_valid_flags = [
        row.get("valid_for_claim")
        for row_group in (parent_rows, clause_rows, hunt_rows, evaluator_data)
        for row in row_group
    ]
    add("V666_7_no_generated_claim_rows", all(flag == "false" for flag in all_valid_flags), "valid_for_claim_flags=" + ";".join(sorted(set(all_valid_flags))))

    evaluator_claims = [row for row in evaluator_data if row["valid_for_claim"] != "false" or row["pass_status"] not in {"not_claimable", "guardrail", "derive_first"}]
    add("V666_8_evaluator_nonclaim", not evaluator_claims, "claimlike_evaluator_rows=" + str(len(evaluator_claims)))

    blocked_gates = {row["gate_id"] for row in gate_rows if row["result"] == "blocked_as_expected"}
    add("V666_9_blocked_gate_present", "G666_2_parent_lock_attempt_complete" in blocked_gates, "blocked_gates=" + ";".join(sorted(blocked_gates)))

    next_target_rows = [row for row in decision if row["next_action"] == NEXT_TARGET]
    add("V666_10_next_target_selected", bool(next_target_rows), NEXT_TARGET)

    changed = formalization_changed_after_cutoff()
    add("V666_11_formalization_workbench_untouched", changed == 0, "formalization_changed_after_cutoff=" + str(changed))

    add("V666_12_status_nonclaim", STATUS.endswith("nonclaim") and "no_stable_Hamiltonian_source_charge" in CLAIM_CEILING, STATUS)

    return rows


def nonclaim_summary_rows(
    parent_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    hunt_rows: list[dict[str, str]],
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
            "parent_lock_attempt_rows": str(len(parent_rows)),
            "clause_test_rows": str(len(clause_rows)),
            "source_hunt_rows": str(len(hunt_rows)),
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
    parent_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    hunt_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 666 - Y5 R10 Parent Boundary Reference Lock Or FB554-0 Source Value Hunt

## Verdict

666 tried the clean route: sign the parent boundary/reference lock that would make the first Hamiltonian leakage row vanish.

The sufficient theorem shape is now sharp:

```text
S_parent = int_M L_MTS + int_boundary B_ref
delta H_tau = int_S(delta Q_tau - i_tau Theta) - delta H_ref
FB554_0 = |delta_H_tau_nonintegrable|/M_H_ref
        + |Delta_ref|/M_H_ref
        + |symplectic_boundary_flux|/M_H_ref
```

This route would work only if `B_ref`, `Theta`, `Q_tau`, the boundary class/no-hair condition, projector silence, the local time generator, and `M_H_ref` are all parent-owned before readout.

Current verdict: not signed. The source-value hunt is staged, but every row remains nonclaim and missing real source files.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Parent Lock Attempt

{markdown_table(parent_rows, ["attempt_id", "target", "mathematical_form", "current_result", "why_not_signed", "activated_FB5540_input", "valid_for_claim"])}

## Clause Tests

{markdown_table(clause_rows, ["clause_id", "needed_for", "pass_condition", "current_result", "missing", "repair_or_source_fallback", "valid_for_claim"])}

## Source Value Hunt

{markdown_table(hunt_rows, ["hunt_id", "quantity", "parent_or_source_requirement", "acceptable_source_kind", "units", "arena_links", "value_status", "source_file", "blocker", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "target", "numeric_status", "pass_status", "reason", "claim_effect", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "detail", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "parent_lock_attempt_rows", "clause_test_rows", "source_hunt_rows", "evaluator_rows", "blocked_or_nonclaim_gates", "validation_failures", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is the right failure mode. We are not stuck because the route is vague; we are stuck because it is too sharp to cheat. The next mathematically serious move is to write the explicit parent boundary action ansatz and variation ledger. If that still fails, the 666 source-value hunt tells us exactly which rows would need real source-backed numbers.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    parent_rows = parent_lock_attempt_rows()
    clause_rows = clause_test_rows()
    hunt_rows = source_value_hunt_rows()
    evaluator_data = evaluator_rows()
    gate_rows = scoreability_gate_rows()
    decision = decision_rows()
    validation = validation_rows(source_rows, parent_rows, clause_rows, hunt_rows, evaluator_data, gate_rows, decision)
    summary_rows = nonclaim_summary_rows(parent_rows, clause_rows, hunt_rows, evaluator_data, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_666_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_666_PARENT_LOCK_ATTEMPT.csv",
        parent_rows,
        [
            "attempt_id",
            "target",
            "mathematical_form",
            "required_ownership",
            "current_result",
            "why_not_signed",
            "activated_FB5540_input",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_666_BOUNDARY_REFERENCE_CLAUSE_TEST.csv",
        clause_rows,
        ["clause_id", "needed_for", "pass_condition", "current_result", "missing", "repair_or_source_fallback", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
        hunt_rows,
        [
            "hunt_id",
            "quantity",
            "parent_or_source_requirement",
            "acceptable_source_kind",
            "units",
            "arena_links",
            "value_status",
            "source_file",
            "blocker",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_666_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "target", "numeric_status", "pass_status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_666_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_666_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_666_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "parent_lock_attempt_rows",
            "clause_test_rows",
            "source_hunt_rows",
            "evaluator_rows",
            "blocked_or_nonclaim_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_666_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(source_rows, parent_rows, clause_rows, hunt_rows, evaluator_data, gate_rows, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"parent_lock_attempt_rows={len(parent_rows)}")
    print(f"clause_test_rows={len(clause_rows)}")
    print(f"source_hunt_rows={len(hunt_rows)}")
    print(f"evaluator_rows={len(evaluator_data)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
