from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1645"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md"

SOURCE_FILES = {
    "1644_doc": ROOT / "1644-Y5-R2FR-Mstar-same-frame-source-mass-owner-or-noncircular-denominator-blocker.md",
    "1644_validation": OUT / "P8_Y5_BRR545_1644_VALIDATION.csv",
    "1644_next": OUT / "P8_Y5_PARENT_QLOC_1644_NEXT_TARGET.csv",
    "1644_theorem": OUT / "P8_Y5_PARENT_QLOC_1644_MSTAR_THEOREM_ATTEMPT.csv",
    "1644_clause": OUT / "P8_Y5_PARENT_QLOC_1644_SAME_FRAME_DENOMINATOR_CLAUSE_MAP.csv",
    "1007_doc": ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
    "1007_audit": OUT / "P8_Y5_R10_1007_HTAU_INTEGRABILITY_THEOREM_AUDIT.csv",
    "770_doc": ROOT / "770-Y5-R10-Hamiltonian-integrability-parent-action-clause-or-FB5540-component-fill.md",
    "770_curl": OUT / "P8_Y5_R10_770_INTEGRABILITY_CURL_TEST.csv",
    "1017_doc": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    "1017_lock": OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
    "664_integrability": OUT / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
    "hsm_contract": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "boundary_status": OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "tau_contract": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
    "frame_contract": OUT / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
    "ham_charge_contract": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
}

NEEDLES = {
    "1644_doc": ["M_* := M_H_ref", "owned J_H[tau]"],
    "1644_validation": ["VAL1644_OVERALL", "PASS"],
    "1644_next": ["1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md"],
    "1644_theorem": ["MST1644_2_integrability", "FAIL_CURRENT_CLAIM"],
    "1644_clause": ["MDC1644_4_integrability_reference", "NOT_DERIVED"],
    "1007_doc": ["H_tau integrability", "parent theta/Q_tau extraction"],
    "1007_audit": ["HTA1007_6_integrability_verdict", "fail_current_claim"],
    "770_doc": ["field-space curl of `delta H_tau`", "theta_total and Q_tau^MTS"],
    "770_curl": ["ICT770_1_curl_identity", "exact_test_written_not_evaluated"],
    "1017_doc": ["Reference-lock law", "field-space curl of delta H_tau vanishes"],
    "1017_lock": ["HRL1017_1_integrability_curl", "fail_current_claim"],
    "664_integrability": ["HCI664_6_integrability_verdict", "missing explicit theta/Q_tau"],
    "hsm_contract": ["HSM541_1_integrable_charge", "not_derived_for_current_MTS"],
    "boundary_status": ["M_H_ref", "claim_valid_data_rows"],
    "tau_contract": ["TGC685_2_Hamiltonian_boundary_route", "not_derived_for_current_MTS"],
    "frame_contract": ["FLC684_6_verdict", "blocked_nonclaim"],
    "ham_charge_contract": ["HC2_differentiable_integrable_Hxi", "not_parent_derived"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1645_SOURCE_REGISTER.csv"
THEOREM = OUT / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv"
CURL = OUT / "P8_Y5_PARENT_QLOC_1645_FIELD_SPACE_CURL_OBSTRUCTION.csv"
SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1645_MHREF_SOURCE_ROW_SCHEMA.csv"
INPUT_STATUS = OUT / "P8_Y5_PARENT_QLOC_1645_MSTAR_INPUT_STATUS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1645_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1645_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1645_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1645_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    THEOREM,
    CURL,
    SCHEMA,
    INPUT_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    THEOREM,
    CURL,
    SCHEMA,
    INPUT_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {"valid_for_claim", "valid_for_mts_claim", "claim_allowed", "score_allowed"}
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1645 Htau/MHref integrability-reference lock audit",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HTM1645_0_phase_space_one_form",
            "statement": "on a fixed local branch, define the Hamiltonian one-form alpha_tau on field space",
            "mathematical_form": "alpha_tau[delta Phi] = integral_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref",
            "proof_status": "FORMAL_DEFINITION_AVAILABLE",
            "missing_for_current_claim": "Theta_total, Q_tau^MTS, tau, S, and H_ref are not all parent-owned before readout",
            "source_paths": ";".join([str(SOURCE_FILES["770_curl"]), str(SOURCE_FILES["1017_lock"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HTM1645_1_integrability_criterion",
            "statement": "H_tau exists iff alpha_tau is closed on the allowed branch phase space",
            "mathematical_form": "d_field alpha_tau(delta1,delta2)=0",
            "proof_status": "CONDITIONAL_THEOREM_WRITTEN",
            "missing_for_current_claim": "the field-space curl is not evaluated from an explicit parent current",
            "source_paths": ";".join([str(SOURCE_FILES["1007_doc"]), str(SOURCE_FILES["770_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HTM1645_2_curl_decomposition",
            "statement": "the obstruction splits into EH, retained-sector, reference, tau, surface, and boundary pieces",
            "mathematical_form": "d alpha_tau = I_EH + I_X + I_projector + I_boundary + I_ref + I_tau + I_surface",
            "proof_status": "OBSTRUCTION_DECOMPOSED_NOT_ZERO",
            "missing_for_current_claim": "I_X, I_projector, I_boundary, I_ref, I_tau, and I_surface are not parent-signed zero or source-bounded",
            "source_paths": ";".join([str(SOURCE_FILES["770_curl"]), str(SOURCE_FILES["1017_lock"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HTM1645_3_fixed_reference_law",
            "statement": "H_ref must be selected once and derivative-silent under source/radius/time/frame/readout changes",
            "mathematical_form": "partial_{source,r,t,frame,lambda} Delta_ref = 0 and curl(delta H_ref)=0",
            "proof_status": "FAIL_CURRENT_CLAIM",
            "missing_for_current_claim": "B_ref/H_ref is named but not selected by a current parent principle",
            "source_paths": ";".join([str(SOURCE_FILES["1017_lock"]), str(SOURCE_FILES["boundary_status"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HTM1645_4_MHref_denominator_law",
            "statement": "if the one-form is closed, the legal denominator is the positive same-frame charge M_H_ref",
            "mathematical_form": "M_H_ref = H_tau[S_outer] - H_ref > 0 and M_* = M_H_ref",
            "proof_status": "CONDITIONAL_ONLY",
            "missing_for_current_claim": "integrability, fixed reference, positivity, source equality, and Poisson/Gauss readout are unsigned",
            "source_paths": ";".join([str(SOURCE_FILES["1644_theorem"]), str(SOURCE_FILES["1017_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HTM1645_5_verdict",
            "statement": "current MTS proves an integrable fixed-reference H_tau and hence Mstar",
            "mathematical_form": "d alpha_tau=0; delta H_ref fixed; M_H_ref positive; no orbital-GM import",
            "proof_status": "FAIL_CURRENT_CLAIM",
            "missing_for_current_claim": "parent theta/Q_tau extraction and the curl-zero certificates are absent",
            "source_paths": ";".join(
                [
                    str(SOURCE_FILES["1007_audit"]),
                    str(SOURCE_FILES["770_curl"]),
                    str(SOURCE_FILES["1017_lock"]),
                    str(SOURCE_FILES["664_integrability"]),
                ]
            ),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def curl_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "ICO1645_0_EH_core",
            "component": "I_EH",
            "mathematical_form": "integral_S i_tau omega_EH(delta1,delta2)",
            "zero_condition": "local exterior is genuinely EH with fixed stationary boundary data",
            "current_status": "CONDITIONAL_REFERENCE_ONLY",
            "activated_residual": "delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "ICO1645_1_retained_sector",
            "component": "I_X",
            "mathematical_form": "integral_S i_tau omega_X + C_X",
            "zero_condition": "X sector absent from tangent space, proper gauge, no-pole source-free, or explicitly bounded",
            "current_status": "NOT_PARENT_SIGNED",
            "activated_residual": "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "ICO1645_2_projector_boundary",
            "component": "I_projector + I_boundary",
            "mathematical_form": "integral_boundary(delta Q_tau^extra - i_tau Theta_extra)+delta B_class+projector_terms",
            "zero_condition": "boundary class/no-hair/projector silence is parent-owned",
            "current_status": "NOT_PARENT_SIGNED",
            "activated_residual": "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "ICO1645_3_reference",
            "component": "I_ref",
            "mathematical_form": "curl(delta H_ref)+Delta_ref derivatives",
            "zero_condition": "H_ref is fixed once by parent branch/topology and derivative-silent",
            "current_status": "NOT_PARENT_SIGNED",
            "activated_residual": "Delta_ref_over_MH;H_ref_shift",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "ICO1645_4_tau_surface",
            "component": "I_tau + I_surface",
            "mathematical_form": "terms from delta tau and delta S_outer/domain",
            "zero_condition": "tau and linking surface are fixed by the same observed source branch",
            "current_status": "NOT_PARENT_SIGNED",
            "activated_residual": "time_generator_lock;worldtube_domain_shift",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "ICO1645_5_curl_verdict",
            "component": "d_field alpha_tau",
            "mathematical_form": "I_EH + I_X + I_projector + I_boundary + I_ref + I_tau + I_surface",
            "zero_condition": "all components vanish jointly as theorem-zero or are source-bounded with absolute no-cancellation accounting",
            "current_status": "NOT_PROVED_ZERO",
            "activated_residual": "FB5540_delta_H_tau_source_row_required_if_certificate_fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def schema_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHS1645_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "positive same-frame Hamiltonian source denominator",
            "required_columns": "system_id;tau_id;surface_outer;Q_tau_integral;H_tau;H_ref;M_H_ref;units;reference_rule;source_path;valid_for_claim",
            "current_status": "MISSING_STABLE_MH_REF",
            "acceptance_gate": "finite positive parent-owned H_tau-H_ref with no orbital-GM import",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHS1645_1_delta_H_tau_nonintegrable",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "absolute field-space curl obstruction normalized by M_H_ref",
            "required_columns": "system_id;surface;field_variation_pair;curl_value;M_H_ref;units;theta_source;Q_tau_source;valid_for_claim",
            "current_status": "MISSING_PARENT_THETA_QTAU_OR_NUMERIC_CURL",
            "acceptance_gate": "theorem-zero from parent current or source-backed numeric absolute bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHS1645_2_Delta_ref",
            "quantity": "Delta_ref_over_MH;H_ref_shift",
            "definition": "reference subtraction shift and derivative profile normalized by M_H_ref",
            "required_columns": "system_id;reference_branch;Delta_ref;H_ref_shift;derivative_profile;M_H_ref;source_path;valid_for_claim",
            "current_status": "MISSING_REFERENCE_LOCK_OR_NUMERIC_PROFILE",
            "acceptance_gate": "reference derivative silence or source-backed derivative profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHS1645_3_symplectic_boundary_flux",
            "quantity": "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
            "definition": "extra-sector/projector/boundary symplectic leakage normalized by M_H_ref",
            "required_columns": "system_id;boundary_class;flux_integral;projector_terms;edge_terms;M_H_ref;source_path;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_EDGE_PROJECTOR_ZERO_OR_NUMERIC_FLUX",
            "acceptance_gate": "boundary/edge theorem-zero or explicit source-backed flux bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHS1645_4_tau_surface_lock",
            "quantity": "time_generator_lock;worldtube_domain_shift",
            "definition": "same tau/source surface controls source, charge, clocks, boundary, orbit, and PPN readout",
            "required_columns": "system_id;tau_source;tau_charge;tau_clock;tau_orbit;surface_rule;mismatch_bound;source_path;valid_for_claim",
            "current_status": "MISSING_TAU_SURFACE_LOCK_CERTIFICATE",
            "acceptance_gate": "one observed tau/surface theorem or bounded mismatch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHS1645_5_FB5540_total",
            "quantity": "epsilon_HPiM_integrability_abs",
            "definition": "absolute no-cancellation total for integrability/reference/boundary/tau residuals",
            "required_columns": "system_id;component_sum_abs;M_H_ref;normalization;component_sources;source_path;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "acceptance_gate": "all numerator and denominator pieces real; no cancellation between unknowns",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def input_status_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1645_0_Mstar_same_frame",
            "quantity": "M_star_same_frame",
            "current_value": "MISSING_STABLE_MH_REF",
            "status": "BLOCKED_BY_HTAU_INTEGRABILITY_REFERENCE_LOCK",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1645_1_parent_theta_Qtau",
            "quantity": "Theta_total;Q_tau^MTS",
            "current_value": "MISSING_PARENT_CURRENT_OWNER",
            "status": "FIRST_UPSTREAM_BLOCKER",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1645_2_delta_H_tau_nonintegrable",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "current_value": "MISSING_THEOREM_ZERO_OR_SOURCE_BOUND",
            "status": "FB5540_COMPONENT_ROW_REQUIRED_IF_PROOF_FAILS",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1645_3_Delta_ref_boundary_tau",
            "quantity": "Delta_ref_over_MH;symplectic_boundary_flux_over_MH;time_generator_lock",
            "current_value": "MISSING_COMPONENTS",
            "status": "NO_CANCELLATION_VECTOR_INCOMPLETE",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1645_0_conditional_theorem_retained",
            "decision": "retain the covariant-phase-space integrability theorem as the legal route",
            "reason": "alpha_tau closed on field space is the exact condition for H_tau and hence M_H_ref",
            "effect": "the next proof target is sharp rather than rhetorical",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1645_1_no_current_MHref_claim",
            "decision": "do not claim M_H_ref or M_star_same_frame",
            "reason": "current corpus has not extracted parent Theta_total/Q_tau^MTS or closed the curl/reference pieces",
            "effect": "normalized PPN/local-GR branch remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1645_2_no_EH_or_orbital_shortcut",
            "decision": "reject EH-only import and orbital-GM denominator shortcuts",
            "reason": "either shortcut would smuggle GR/Newton into the derivation",
            "effect": "only parent current extraction or source-backed residual rows can move the gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1645_3_next_theta_Qtau",
            "decision": "move next to Theta_total/Q_tau^MTS current ownership",
            "reason": "without these objects the curl cannot be evaluated and the theorem cannot become a proof",
            "effect": "1646 should extract the parent current owner or stage delta_H source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1645_0_Htau_integrability",
            "claim": "H_tau is integrable on the current MTS local branch",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_PARENT_THETA_QTAU_AND_CURL_ZERO_CERTIFICATES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1645_1_reference_lock",
            "claim": "H_ref is fixed and derivative-silent",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_PARENT_REFERENCE_SELECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1645_2_MHref_Mstar",
            "claim": "M_H_ref supplies Mstar same-frame denominator",
            "gate_pass": False,
            "status": "NOT_SCORED",
            "blocker": "HTAU_INTEGRABILITY_REFERENCE_LOCK_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1645_3_local_GR_PPN_R10",
            "claim": "local GR, PPN, or R10 pass follows from 1645",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "source-charge denominator and no-cancellation residual vector remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1645_4_guardrail",
            "claim": "integrability-reference theorem gate is now explicit",
            "gate_pass": True,
            "status": "PASS_AS_INTERNAL_GUARDRAIL_ONLY",
            "blocker": "guardrail is not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1646-Y5-R2FR-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
            "script": "scripts/Y5_R2FR_theta_Qtau_current_owner_or_deltaH_component_source_row.py",
            "objective": "extract parent Theta_total and Q_tau^MTS/current decomposition for the local branch, or stage source-ready delta_H_tau_nonintegrable component rows",
            "success_condition": "Theta_total, Q_tau^MTS, sector constraints, reference terms, tau/surface variations, and source paths are parent-owned enough to evaluate d_field alpha_tau",
            "guardrails": "no EH-only import; no orbital-GM denominator; no fitted reference; no PPN/local-GR/R10 claim; score no placeholders",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for path in GENERATED + [VALIDATION]:
        if path.exists():
            shutil.copy2(path, QUARANTINE / path.name)
            shutil.copy2(path, BRANCH_RESIDUALS / path.name)
    shutil.copy2(THEOREM, QUEUE / "JR1645_HTAU_INTEGRABILITY_THEOREM_NONCLAIM.csv")
    shutil.copy2(SCHEMA, QUEUE / "JR1645_MHREF_SOURCE_ROW_SCHEMA_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1645_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    sources = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM)
    curl = csv_rows(CURL)
    schema = csv_rows(SCHEMA)
    inputs = csv_rows(INPUT_STATUS)
    gates = csv_rows(CLAIM_GATE)
    decisions = csv_rows(DECISION)
    next_targets = csv_rows(NEXT_TARGET)
    checks = [
        (
            "VAL1645_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" and bool_string(row["needles_found"]) == "true" for row in sources),
            "all cited 1645 source paths exist and needles are present",
        ),
        (
            "VAL1645_1_integrability_theorem_written",
            any(row["theorem_id"] == "HTM1645_1_integrability_criterion" for row in theorem),
            "alpha_tau closure criterion is written",
        ),
        (
            "VAL1645_2_verdict_blocks_claim",
            any(row["theorem_id"] == "HTM1645_5_verdict" and row["proof_status"] == "FAIL_CURRENT_CLAIM" for row in theorem),
            "theorem attempt refuses to promote H_tau/MHref",
        ),
        (
            "VAL1645_3_curl_components_split",
            len(curl) >= 6 and any(row["component_id"] == "ICO1645_5_curl_verdict" for row in curl),
            "field-space curl obstruction is decomposed",
        ),
        (
            "VAL1645_4_schema_source_ready_nonclaim",
            len(schema) >= 6 and all(bool_string(row["valid_for_claim"]) == "false" for row in schema),
            "MHref/source-row schema is staged as nonclaim",
        ),
        (
            "VAL1645_5_mstar_still_blocked",
            any(row["quantity"] == "M_star_same_frame" and row["status"] == "BLOCKED_BY_HTAU_INTEGRABILITY_REFERENCE_LOCK" for row in inputs),
            "Mstar remains blocked by Htau/reference lock",
        ),
        (
            "VAL1645_6_no_shortcuts",
            any(row["decision_id"] == "DEC1645_2_no_EH_or_orbital_shortcut" for row in decisions),
            "EH-only and orbital-GM shortcuts are rejected",
        ),
        (
            "VAL1645_7_claim_gates_safe",
            any(row["gate_id"] == "CG1645_4_guardrail" and row["status"] == "PASS_AS_INTERNAL_GUARDRAIL_ONLY" for row in gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in gates),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1645_8_next_target_selected",
            next_targets[0]["next_target"] == "1646-Y5-R2FR-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
            "next target selects Theta/Q_tau current ownership",
        ),
        (
            "VAL1645_9_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1645 CSVs parse",
        ),
        (
            "VAL1645_10_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1645 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1645_11_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1645_12_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1645_HTAU_INTEGRABILITY_THEOREM_NONCLAIM.csv",
                    QUEUE / "JR1645_MHREF_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
                    QUEUE / "JR1645_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1645_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1645_14_formalization_untouched",
            not any(FORMALIZATION.rglob("*1645*")) if FORMALIZATION.exists() else True,
            "no 1645 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1645_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1645 Htau/MHref integrability-reference lock validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    sources = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM)
    curl = csv_rows(CURL)
    schema = csv_rows(SCHEMA)
    inputs = csv_rows(INPUT_STATUS)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)
    content = f"""# 1645 - Htau MHref Integrability Reference Lock Or Mstar Source Row

**Private status:** nonclaim checkpoint. No stable Hamiltonian source charge, `M_H_ref`, `M_*`, PPN pass, local-GR pass, Newton pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

The exact local denominator route is now written as a field-space integrability theorem:

```text
alpha_tau[delta Phi] = integral_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref
H_tau exists on the branch iff d_field alpha_tau = 0
M_* = M_H_ref = H_tau[S_outer] - H_ref
```

This is the correct mathematical route, but the current corpus does **not** yet prove it. The obstruction is not vague anymore:

```text
d alpha_tau = I_EH + I_X + I_projector + I_boundary + I_ref + I_tau + I_surface
```

Only the EH-like piece has a known conditional reference route. The retained-sector, projector/boundary, reference, tau, and surface terms are not parent-signed zero or source-bounded. So `M_H_ref` remains unavailable as `M_*`. The next root target is therefore `Theta_total/Q_tau^MTS` current ownership: without those, the curl cannot be evaluated.

## Source Register

{markdown_table(sources, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Htau Integrability Theorem

{markdown_table(theorem, ["theorem_id", "statement", "mathematical_form", "proof_status", "missing_for_current_claim"])}

## Field-Space Curl Obstruction

{markdown_table(curl, ["component_id", "component", "mathematical_form", "zero_condition", "current_status", "activated_residual"])}

## MHref Source Row Schema

{markdown_table(schema, ["row_id", "quantity", "definition", "current_status", "acceptance_gate"])}

## Mstar Input Status

{markdown_table(inputs, ["input_id", "quantity", "current_value", "status", "valid_for_runner"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "effect"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        THEOREM: theorem_rows(),
        CURL: curl_rows(),
        SCHEMA: schema_rows(),
        INPUT_STATUS: input_status_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)
    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
