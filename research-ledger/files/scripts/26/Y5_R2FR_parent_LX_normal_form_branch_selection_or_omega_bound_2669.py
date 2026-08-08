from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2669"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2669-Y5-R2FR-parent-LX-normal-form-branch-selection-or-omega-bound.md"

CHECKPOINT = "2669"
BRANCH_ID = "Y5_R2FR_PARENT_LX_BRANCH_SELECTION_2669"
PREFIX = "P8_Y5_R2FR_LX_BRANCH_2669"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "RETAINED",
    "UNFILLED",
    "PLACEHOLDER",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "branch_audit": RESIDUALS / f"{PREFIX}_BRANCH_SELECTION_AUDIT.csv",
    "selector_template": RESIDUALS / f"{PREFIX}_SELECTOR_TEMPLATE_NONCLAIM.csv",
    "omega_bound_interface": RESIDUALS / f"{PREFIX}_OMEGA_BOUND_INTERFACE_NONCLAIM.csv",
    "branch_gate": RESIDUALS / f"{PREFIX}_BRANCH_GATE.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_BRANCH_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2669_PARENT_LX_BRANCH_SELECTION_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Parent_LX_branch_selection_2669_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "OMEGA_X_INTEGRAL_BOUND_INTERFACE_2669_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2669_LX_BRANCH_SELECTOR.csv",
    "quarantine": QUARANTINE / "P8_Y5_2669_BRANCH_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2668_doc": {
        "path": ROOT / "2668-Y5-R2FR-LX-Theta-omega-owner-or-Htau-curl-component-bound.md",
        "needles": ["LTO2668_1_absent_quotient", "LTO2668_8_verdict", "NEXT2668_0_selected"],
        "role": "immediate handoff selecting parent L_X branch selection as the next target",
    },
    "669_doc": {
        "path": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
        "needles": ["LX669_0_absent_quotient_variable", "LX669_5_memory_kernel_or_nonlocal", "EV669_1_best_route"],
        "role": "early minimal L_X branch menu and ranking",
    },
    "1018_doc": {
        "path": ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["LOC1018_0_LX_owner", "RT1018_0_absent_quotient", "RT1018_5_verdict"],
        "role": "sector-owner map and branch failure ledger",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["PO1019_2_symplectic_block", "DC1019_0_orthogonal_split", "V1019_9_claim_gates_blocked"],
        "role": "boundary exactness and no-cancellation guardrail",
    },
    "1022_doc": {
        "path": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
        "needles": ["VQC1022_7_verdict", "FBR1022_1_scalar_operator_pack", "R1022_1_scalar_fallback"],
        "role": "quotient/vertical no-pole failure and scalar fallback ledger",
    },
    "1023_doc": {
        "path": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
        "needles": ["QVC1023_8_verdict", "CDA1023_4_verdict", "DEM1023_1_scalar_operator"],
        "role": "single q/v/action descent certificate failure and demotion logic",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["SV1025_0_local_block", "SV1025_2_Hessian_signs", "BV1025_3_coupling_gap"],
        "role": "scalar operator signs and coupling gap localization",
    },
    "2618_doc": {
        "path": ROOT / "2618-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["ANF2618_6_current_verdict", "SMG2618_0_euler_equation_gate", "CM2618_3_gr_lhs_missing"],
        "role": "parent action normal-form signature and GR-limit warning",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def has_missing(row: dict[str, Any]) -> bool:
    joined = " ".join(str(value) for value in row.values())
    return any(token in joined for token in MISSING_TOKENS)


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2669_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def branch_selection_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "audit_id": "LXB2669_0_target",
            "branch": "single parent L_X normal form",
            "candidate_normal_form": "choose exactly one live local branch before any local fifth-force or GR-reduction statement",
            "closure_condition": "one branch has parent action signature, variation domain, boundary class, source map and exclusion matrix",
            "exclusion_condition": "all competing branches are theorem-zeroed, demoted, or carried as explicit residual rows",
            "current_status": "TARGET_EXACT",
            "blocker": "none; this is the contract",
            "next_action": "audit each branch without mixing them",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_1_absent_quotient",
            "branch": "absent quotient",
            "candidate_normal_form": "S_parent=S_red[q(Phi),Psi,theta] with no independent X before variation",
            "closure_condition": "q map, v_X in ker(Dq), matter descent, measure/coframe/connection descent and boundary silence all parent-signed",
            "exclusion_condition": "if closed, scalar, edge and nonlocal X rows are removed rather than tuned",
            "current_status": "BEST_GR_REDUCTION_ROUTE_NOT_DERIVED",
            "blocker": "q/v/action/matter/boundary certificate is still unsigned as a single object",
            "next_action": "attack absent-quotient erasure certificate first",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_2_vertical_constraint",
            "branch": "vertical first-class constraint",
            "candidate_normal_form": "X is generated by a first-class vertical constraint with differentiable zero charge",
            "closure_condition": "Dq[v_X]=0, Omega(delta Phi,v_X)=delta G_X, bracket closes, Q_X differentiable and boundary contribution zero",
            "exclusion_condition": "if closed, sourced scalar residuals are gauge artefacts not physical couplings",
            "current_status": "CONDITIONAL_ROUTE_UNSIGNED",
            "blocker": "vertical generator, charge differentiability, bracket and boundary silence are not parent-signed",
            "next_action": "keep as secondary route after quotient erasure attempt",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_3_scalar_sourcefree",
            "branch": "positive scalar source-free",
            "candidate_normal_form": "L_X=1/2 sqrt(h)(Z_X|grad X|^2+M_X^2 X^2) with J_X=0 and boundary_flux_X=0",
            "closure_condition": "Z_X>0, M_X^2>0, self-adjoint local domain, J_X=0 and boundary_flux_X=0 from parent action",
            "exclusion_condition": "if closed, finite local X amplitude vanishes by positive energy identity",
            "current_status": "CONDITIONAL_THEOREM_ONLY",
            "blocker": "operator ownership and source-zero clauses are values-missing and parent-unsigned",
            "next_action": "only use after quotient/vertical routes fail",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_4_scalar_sourced",
            "branch": "physical scalar sourced",
            "candidate_normal_form": "L_X=1/2 sqrt(h)(Z_X|grad X|^2+M_X^2 X^2)-sqrt(h)XJ_X plus finite matter coupling",
            "closure_condition": "source-backed Z_X, M_X^2, J_X, K_X, Qbar_XH, qbar_XT, lambda_X and bound curve",
            "exclusion_condition": "cannot be hidden by no-hair; must be scored against local tests",
            "current_status": "FINITE_RESIDUAL_ROUTE_NOT_CLAIM_READY",
            "blocker": "coupling/source normalization is still the live missing coefficient pack",
            "next_action": "retain as bound-input fallback if theorem-zero routes fail",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_5_edge_boundary",
            "branch": "edge or boundary charge",
            "candidate_normal_form": "X exists only through edge/boundary charge or exact boundary term",
            "closure_condition": "boundary exactness, projector orthogonality, edge coefficient signs and no double counting",
            "exclusion_condition": "if not exact-zero, edge residual must be bounded separately from bulk source",
            "current_status": "BOUNDARY_BRANCH_UNSIGNED",
            "blocker": "edge/projector orthogonality and boundary exactness remain unproven",
            "next_action": "keep no-cancellation rows live",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_6_nonlocal_kernel",
            "branch": "memory or nonlocal kernel",
            "candidate_normal_form": "X is a local face of a retarded memory kernel or auxiliary lift",
            "closure_condition": "kernel spectrum, causal domain, positive auxiliary lift and local-test projection are all owned",
            "exclusion_condition": "if kernel not reducible, local residual vector must carry nonlocal parameters explicitly",
            "current_status": "NONLOCAL_BRANCH_UNSIGNED",
            "blocker": "no parent kernel, spectrum, auxiliary lift or causality proof has been supplied",
            "next_action": "do not let memory language erase local residuals",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_7_countermodel",
            "branch": "universal conformal countermodel",
            "candidate_normal_form": "DeltaS=a_X X T_m demonstrates a source can appear unless descent forbids it",
            "closure_condition": "parent action forbids or reclassifies every X-matter coupling term",
            "exclusion_condition": "without this exclusion, qbar_XT and Qbar_XH cannot be set to zero",
            "current_status": "COUNTERMODEL_STILL_OPEN",
            "blocker": "source-zero has not been derived; it is exactly the coupling gap",
            "next_action": "use as the anti-cheat guardrail for all zero claims",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "audit_id": "LXB2669_8_verdict",
            "branch": "parent L_X branch selection",
            "candidate_normal_form": "one parent branch selects the local L_X normal form and excludes the others",
            "closure_condition": "LXB2669_1 or LXB2669_2 or LXB2669_3 closes, or LXB2669_4/5/6 becomes source-backed",
            "exclusion_condition": "no mixed symbolic owner and no cancellation of unknown components",
            "current_status": "PARENT_LX_BRANCH_SELECTION_NOT_DERIVED",
            "blocker": "every branch is still conditional, unsigned, or coefficient-missing",
            "next_action": "stage omega bound interface and derive absent-quotient erasure next",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def selector_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "SEL2669_0_branch_id",
            "branch_candidate": "single active branch",
            "required_inputs": "branch_id;normal_form;parent_action_signature;variation_domain;boundary_class;excluded_branches",
            "units_or_domain": "branch metadata",
            "source_path": "MISSING_SINGLE_BRANCH_SELECTION",
            "status": "MISSING_PARENT_LX_BRANCH_SELECTION",
            "use_if": "always required before local-GR, R10, PPN, clock or orbital claims",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SEL2669_1_absent_quotient_certificate",
            "branch_candidate": "absent quotient",
            "required_inputs": "q;Dq;v_X;S_red;S_matter_descent;measure_descent;connection_descent;boundary_silence",
            "units_or_domain": "parent geometric certificate",
            "source_path": "MISSING_Q_V_ACTION_DESCENT_CERTIFICATE",
            "status": "BEST_ROUTE_UNSIGNED",
            "use_if": "try first because it erases the pole rather than fitting it",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SEL2669_2_vertical_constraint_certificate",
            "branch_candidate": "vertical constraint",
            "required_inputs": "v_X;G_X;Omega;charge_differentiability;bracket_closure;boundary_charge_zero",
            "units_or_domain": "constraint algebra",
            "source_path": "MISSING_VERTICAL_GENERATOR_CERTIFICATE",
            "status": "UNSIGNED_FIRST_CLASS_ROUTE",
            "use_if": "second theorem-zero route if quotient erasure fails",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SEL2669_3_scalar_operator_pack",
            "branch_candidate": "positive scalar source-free",
            "required_inputs": "Z_X;M_X2;self_adjoint_domain;J_X=0;boundary_flux_X=0;lambda_X",
            "units_or_domain": "operator coefficients",
            "source_path": "MISSING_SCALAR_OPERATOR_PACK",
            "status": "CONDITIONAL_NOHAIR_VALUES_MISSING",
            "use_if": "fallback theorem route after quotient/vertical fail",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SEL2669_4_sourced_alpha_pack",
            "branch_candidate": "physical scalar sourced",
            "required_inputs": "K_X;Qbar_XH;qbar_XT;lambda_X;alpha_X(lambda);bound_curve",
            "units_or_domain": "local fifth-force alpha/lambda coefficients",
            "source_path": "MISSING_SOURCE_BACKED_ALPHA_PACK",
            "status": "FINITE_RESIDUAL_VALUES_MISSING",
            "use_if": "only if source-zero theorem fails",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SEL2669_5_edge_pack",
            "branch_candidate": "edge/boundary",
            "required_inputs": "boundary_exactness;projector_orthogonality;edge_coefficients;no_double_counting",
            "units_or_domain": "boundary charge coefficients",
            "source_path": "MISSING_EDGE_BOUNDARY_PACK",
            "status": "EDGE_BRANCH_VALUES_MISSING",
            "use_if": "only if X is boundary-localized rather than bulk",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SEL2669_6_nonlocal_kernel_pack",
            "branch_candidate": "memory/nonlocal kernel",
            "required_inputs": "kernel;retarded_domain;spectrum;auxiliary_lift;local_projection;causality",
            "units_or_domain": "kernel spectrum",
            "source_path": "MISSING_NONLOCAL_KERNEL_PACK",
            "status": "NONLOCAL_ROUTE_VALUES_MISSING",
            "use_if": "only if local scalar normal form is rejected",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SEL2669_7_exclusion_matrix",
            "branch_candidate": "no branch mixing",
            "required_inputs": "forbid_matrix;demotion_reason;residual_row_for_each_survivor;no_cancellation_certificate",
            "units_or_domain": "logic gate",
            "source_path": "MISSING_BRANCH_EXCLUSION_MATRIX",
            "status": "MIXING_FORBIDDEN_BUT_MATRIX_MISSING",
            "use_if": "required before any branch is treated as selected",
            "selected": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def omega_bound_interface_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "OBND2669_0_omega_X_integral_bound",
            "quantity": "abs(omega_X_integral)",
            "definition": "absolute upper envelope for int_S omega_X(delta_1 Phi,delta_2 Phi) over the local surface pair",
            "required_inputs": "Theta_X;surface_pair;tau_action;boundary_class;field_norm;excluded_branch_matrix",
            "units": "action variation / phase-space area",
            "status": "MISSING_PARENT_THETA_OMEGA_AND_BRANCH",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "fallback if no theorem-zero branch closes",
            "timestamp_utc": generated,
        },
        {
            "row_id": "OBND2669_1_surface_pair",
            "quantity": "S_inner,S_outer",
            "definition": "local annular or exterior surfaces used to compare boundary and bulk symplectic flux",
            "required_inputs": "surface_definition;orientation;falloff_class;lab_or_solar_system_scale",
            "units": "length^2",
            "status": "MISSING_SURFACE_PAIR",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "cannot bind omega without the surface pair",
            "timestamp_utc": generated,
        },
        {
            "row_id": "OBND2669_2_tau_action",
            "quantity": "tau action on X sector",
            "definition": "flow direction that transports the local surface charge or Hamiltonian comparison",
            "required_inputs": "xi_tau;Lie_derivative_on_X;Hamiltonian_generator;domain",
            "units": "1/time or dimensionless generator",
            "status": "MISSING_TAU_ACTION_ON_LX_BRANCH",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "prevents symbolic H_tau curl cancellation",
            "timestamp_utc": generated,
        },
        {
            "row_id": "OBND2669_3_boundary_exactness_or_bound",
            "quantity": "boundary_flux_X",
            "definition": "exact zero certificate or positive numeric envelope for local boundary injection",
            "required_inputs": "B_X;delta B_X;falloff;edge_modes;orthogonality",
            "units": "same as action boundary variation",
            "status": "MISSING_BOUNDARY_EXACTNESS_OR_BOUND",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "needed by scalar no-hair and omega bound routes",
            "timestamp_utc": generated,
        },
        {
            "row_id": "OBND2669_4_units_normalization",
            "quantity": "omega normalization",
            "definition": "field and Hamiltonian normalization connecting omega_X to M_H_ref and local residual rows",
            "required_inputs": "X_units;Theta_units;M_H_ref;field_rescaling;G_obs_normalization",
            "units": "dimension ledger",
            "status": "MISSING_UNITS_NORMALIZATION",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "prevents arbitrary coefficient hiding",
            "timestamp_utc": generated,
        },
        {
            "row_id": "OBND2669_5_absolute_envelope",
            "quantity": "omega_X_envelope_to_Htau",
            "definition": "non-cancelling positive bound feeding delta_H_tau_nonintegrable_over_MH",
            "required_inputs": "omega_bound;M_H_ref;surface_pair;tau_action;branch_id",
            "units": "dimensionless after M_H_ref normalization",
            "status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "unknown components may not cancel one another",
            "timestamp_utc": generated,
        },
        {
            "row_id": "OBND2669_6_Htau_feed",
            "quantity": "delta_H_tau_nonintegrable_over_MH contribution",
            "definition": "how the bounded omega_X component feeds the H_tau integrability curl ledger",
            "required_inputs": "omega_X_envelope_to_Htau;component_sign;component_projection;source_path",
            "units": "dimensionless",
            "status": "MISSING_HTAU_FEED_MAP",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "this is a ledger interface, not a pass claim",
            "timestamp_utc": generated,
        },
    ]
    return rows


def branch_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "gate_id": "LXG2669_0_single_branch",
            "requirement": "exactly one parent L_X branch is selected",
            "current_status": "FAIL_BRANCH_SELECTION_MISSING",
            "source_row": "SEL2669_0_branch_id",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_1_absent_quotient",
            "requirement": "q/v/action/matter/boundary descent erases X before variation",
            "current_status": "FAIL_QUOTIENT_CERTIFICATE_MISSING",
            "source_row": "SEL2669_1_absent_quotient_certificate",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_2_vertical_constraint",
            "requirement": "vertical generator is first-class with zero differentiable boundary charge",
            "current_status": "FAIL_VERTICAL_CERTIFICATE_MISSING",
            "source_row": "SEL2669_2_vertical_constraint_certificate",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_3_scalar_nohair",
            "requirement": "Z_X>0, M_X^2>0, J_X=0 and boundary_flux_X=0 are parent-derived",
            "current_status": "FAIL_SCALAR_OPERATOR_VALUES_MISSING",
            "source_row": "SEL2669_3_scalar_operator_pack",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_4_sourced_residual",
            "requirement": "finite coupling pack is numeric, sourced and compared to bounds",
            "current_status": "FAIL_SOURCE_ALPHA_PACK_MISSING",
            "source_row": "SEL2669_4_sourced_alpha_pack",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_5_edge_nonlocal",
            "requirement": "edge and nonlocal branches are either excluded or source-bounded",
            "current_status": "FAIL_EDGE_NONLOCAL_BRANCHES_UNRESOLVED",
            "source_row": "SEL2669_5_edge_pack;SEL2669_6_nonlocal_kernel_pack",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_6_omega_bound",
            "requirement": "omega_X_integral has theorem zero or absolute non-cancelling bound",
            "current_status": "FAIL_OMEGA_BOUND_INTERFACE_MISSING_VALUES",
            "source_row": "OBND2669_0_omega_X_integral_bound",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_7_no_mixing",
            "requirement": "unknown branches are not mixed or cancelled against one another",
            "current_status": "FAIL_BRANCH_EXCLUSION_MATRIX_MISSING",
            "source_row": "SEL2669_7_exclusion_matrix",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "LXG2669_8_verdict",
            "requirement": "local L_X normal form is parent-selected and all surviving residuals are explicit",
            "current_status": "LX_BRANCH_SELECTION_NOT_CLAIM_READY",
            "source_row": "LXB2669_8_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def runner_results_rows(
    branch_audit: list[dict[str, Any]],
    selector_template: list[dict[str, Any]],
    omega_bound_interface: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in branch_audit:
        rows.append(
            {
                "run_id": f"RUN2669_{row['audit_id']}",
                "input_id": row["audit_id"],
                "input_type": "branch_audit",
                "has_missing_marker": has_missing(row),
                "selected": row["selected"],
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_PARENT_LX_BRANCH_NOT_DERIVED",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for row in selector_template:
        rows.append(
            {
                "run_id": f"RUN2669_{row['row_id']}",
                "input_id": row["row_id"],
                "input_type": "selector_template",
                "has_missing_marker": has_missing(row),
                "selected": row["selected"],
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_BRANCH_SELECTOR_INPUTS_MISSING",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for row in omega_bound_interface:
        rows.append(
            {
                "run_id": f"RUN2669_{row['row_id']}",
                "input_id": row["row_id"],
                "input_type": "omega_bound_interface",
                "has_missing_marker": has_missing(row),
                "selected": False,
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_OMEGA_BOUND_INPUTS_MISSING",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "gate_id": "CG2669_0_R10",
            "claim": "R10 alpha/lambda local bound pass",
            "current_status": "FAIL_LX_BRANCH_AND_ALPHA_PACK_UNSIGNED",
            "blocking_rows": "SEL2669_0_branch_id;SEL2669_4_sourced_alpha_pack;OBND2669_0_omega_X_integral_bound",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2669_1_PPN",
            "claim": "PPN residual vector locally silent",
            "current_status": "FAIL_LX_BRANCH_NOT_SELECTED",
            "blocking_rows": "LXB2669_8_verdict;LXG2669_8_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2669_2_clock_or_EM",
            "claim": "clock or EM coupling branch is silent",
            "current_status": "FAIL_SOURCE_DESCENT_AND_COUPLING_ZERO_UNSIGNED",
            "blocking_rows": "LXB2669_7_countermodel;SEL2669_1_absent_quotient_certificate",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2669_3_orbital",
            "claim": "orbital residuals reduce to GR/Newton local branch",
            "current_status": "FAIL_BRANCH_AND_OMEGA_BOUND_MISSING",
            "blocking_rows": "OBND2669_5_absolute_envelope;OBND2669_6_Htau_feed",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2669_4_local_GR",
            "claim": "local GR branch is derived rather than closed by axiom",
            "current_status": "FAIL_PARENT_LX_BRANCH_SELECTION_UNSIGNED",
            "blocking_rows": "LXB2669_1_absent_quotient;LXB2669_8_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2669_5_verdict",
            "claim": "any local-GR/R10/PPN/clock/orbital pass",
            "current_status": "CLAIM_BLOCKED",
            "blocking_rows": "LXG2669_8_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2669_0_result",
            "question": "Can 2669 select the parent L_X branch now?",
            "answer": "No. The branch menu is now exact, but every route remains unsigned or coefficient-missing.",
            "consequence": "no local-GR, R10, PPN, clock or orbital claim may be promoted",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2669_1_best_route",
            "question": "Which branch should be attacked first?",
            "answer": "Absent quotient, because it is the cleanest GR-like route: if X is absent before variation, the local pole is erased rather than tuned.",
            "consequence": "derive q/v/action/matter/boundary descent as one certificate or demote the quotient route",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2669_2_guardrail",
            "question": "What is forbidden after this checkpoint?",
            "answer": "No branch mixing, no symbolic L_X owner, no assumed boundary silence, and no cancellation of unknown components.",
            "consequence": "every surviving branch needs either theorem-zero or explicit residual rows",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2669_3_fallback",
            "question": "What happens if absent quotient fails?",
            "answer": "Move to vertical constraint; if that also fails, use positive scalar no-hair before accepting sourced alpha rows.",
            "consequence": "derivation-first route remains alive without pretending the coupling vanished",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "target_id": "NEXT2669_0_selected",
            "status": "selected",
            "next_doc": "2670-Y5-R2FR-absent-quotient-LX-erasure-certificate-or-branch-demotion.md",
            "next_script": "scripts/Y5_R2FR_absent_quotient_LX_erasure_certificate_or_branch_demotion_2670.py",
            "purpose": "prove X is absent from the physical tangent before variation, or demote the quotient branch",
            "acceptance_gate": "q, v_X, action, matter, measure/coframe/connection and boundary descent close together; otherwise quotient route is explicitly demoted",
            "forbidden": "assuming q erases X after variation, treating matter descent as obvious, hiding boundary charges, local-GR/R10 pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "status_id": "PS2669_0_local_GR",
            "area": "local GR reduction",
            "state": "alive_but_not_derived",
            "why": "best route is absent quotient; branch selection has not closed",
            "next_needed": "2670 absent-quotient erasure certificate",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2669_1_coupling",
            "area": "coupling/source gap",
            "state": "localized",
            "why": "countermodel shows X-matter source cannot be assumed zero",
            "next_needed": "derive descent zero or source K_X/Qbar_XH/qbar_XT",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2669_2_empirical",
            "area": "R10/PPN/clock/orbital tests",
            "state": "blocked_as_claim_ready_evidence",
            "why": "branch and omega bound interfaces are nonclaim",
            "next_needed": "theorem-zero branch or source-backed residual vector",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["selector_template"], BRANCH_COPIES["queue"], "branch selector queue copy"),
        "local_bounds": (OUTPUTS["selector_template"], BRANCH_COPIES["local_bounds"], "local-bound branch selection nonclaim copy"),
        "source_weight": (OUTPUTS["omega_bound_interface"], BRANCH_COPIES["source_weight"], "omega bound interface nonclaim copy"),
        "microscope": (OUTPUTS["selector_template"], BRANCH_COPIES["microscope"], "microscope branch selector copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "branch runner refusal results"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                read_csv(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2669_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2669-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2669*",
        "*Y5_R2FR_parent_LX_normal_form_branch_selection_or_omega_bound_2669*",
        "*JR2669*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    branch_ok = any(
        row["audit_id"] == "LXB2669_8_verdict"
        and row["current_status"] == "PARENT_LX_BRANCH_SELECTION_NOT_DERIVED"
        for row in rows["branch_audit"]
    ) and all(not row["selected"] and not row["score_ready"] and not row["valid_for_claim"] for row in rows["branch_audit"])
    selector_ok = all(
        required in {row["row_id"] for row in rows["selector_template"]}
        for required in (
            "SEL2669_0_branch_id",
            "SEL2669_1_absent_quotient_certificate",
            "SEL2669_7_exclusion_matrix",
        )
    ) and all(not row["selected"] and not row["score_ready"] and not row["valid_for_claim"] for row in rows["selector_template"])
    omega_ok = any(row["row_id"] == "OBND2669_0_omega_X_integral_bound" for row in rows["omega_bound_interface"]) and any(
        row["row_id"] == "OBND2669_5_absolute_envelope" for row in rows["omega_bound_interface"]
    ) and all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["omega_bound_interface"])
    gate_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["branch_gate"]) and any(
        row["gate_id"] == "LXG2669_8_verdict" and row["current_status"] == "LX_BRANCH_SELECTION_NOT_CLAIM_READY"
        for row in rows["branch_gate"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["branch_audit"]) + len(rows["selector_template"]) + len(rows["omega_bound_interface"]) and all(
        row["runner_status"]
        in {
            "REJECTED_PARENT_LX_BRANCH_NOT_DERIVED",
            "REJECTED_BRANCH_SELECTOR_INPUTS_MISSING",
            "REJECTED_OMEGA_BOUND_INPUTS_MISSING",
        }
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2669_5_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    decision_ok = any(
        row["decision_id"] == "DEC2669_1_best_route" and "Absent quotient" in row["answer"] for row in rows["decision"]
    )
    next_ok = any("2670-Y5-R2FR-absent-quotient" in row["next_doc"] for row in rows["next_target"])
    copies_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2669_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2669_01_branch_audit", branch_ok, "parent L_X branch menu is written and not promoted"),
        ("VAL2669_02_selector_template", selector_ok, "branch selector template keeps every branch nonclaim"),
        ("VAL2669_03_omega_interface", omega_ok, "omega bound interface includes omega integral and absolute envelope"),
        ("VAL2669_04_branch_gate", gate_ok, "branch gates block claim promotion"),
        ("VAL2669_05_runner_refuses", runner_ok, "runner rejects unsigned branch and missing omega inputs"),
        ("VAL2669_06_claim_gates_blocked", claim_ok, "R10/PPN/clock/orbital/local-GR claims remain blocked"),
        ("VAL2669_07_decision", decision_ok, "absent quotient selected as next derivation-first route"),
        ("VAL2669_08_next_target", next_ok, "2670 absent-quotient erasure target selected"),
        ("VAL2669_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2669_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2669_11_formalization_untouched", formal_ok, "no 2669 outputs are written under formalization-workbench"),
        ("VAL2669_12_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2669_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2669 rejects parent L_X branch selection as unsigned, stages omega bound interface, and selects absent-quotient erasure next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2669 - Parent LX Normal Form Branch Selection Or Omega Bound

## Purpose

This checkpoint asks which parent `L_X` branch is actually allowed for the local sector. The goal is not to win a claim; it is to prevent branch mixing. A local-GR/R10/PPN/clock/orbital statement needs either a theorem-zero branch or an explicit residual branch with source-backed coefficients.

## Result

- No parent `L_X` branch is selected yet.
- The absent-quotient route remains the best derivation-first path because it erases `X` before variation rather than tuning the local force away.
- Scalar source-free, scalar sourced, edge/boundary, and nonlocal kernel routes stay live only as nonclaim branches.
- `omega_X_integral` is staged as an absolute bound interface so unknown symplectic pieces cannot be cancelled by hand.
- The next target is `2670`: prove the absent-quotient erasure certificate, or demote that branch.

## Source Register

{markdown_table(rows["source_register"])}

## Branch Selection Audit

{markdown_table(rows["branch_audit"])}

## Branch Selector Template

{markdown_table(rows["selector_template"])}

## Omega Bound Interface

{markdown_table(rows["omega_bound_interface"])}

## Branch Gate

{markdown_table(rows["branch_gate"])}

## Runner Results

{markdown_table(rows["runner_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "branch_audit": branch_selection_audit_rows(),
        "selector_template": selector_template_rows(),
        "omega_bound_interface": omega_bound_interface_rows(),
        "branch_gate": branch_gate_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["branch_audit"], rows["selector_template"], rows["omega_bound_interface"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
