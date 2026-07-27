from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1208"
TITLE = "1208-Y5-R10-Ploc-parallel-projector-or-nablaPloc-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PLOC_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_PLOC_PARALLEL_PROJECTOR_AUDIT.csv"
BOUND_LAW_PATH = OUT_DIR / f"{PACK_ID}_NABLAPLOC_BOUND_LAW.csv"
SOURCE_READY_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_READY_NABLAPLOC_ROW.csv"
PRESSURE_PATH = OUT_DIR / f"{PACK_ID}_PRESSURE_COMPARISON.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1208_VALIDATION.csv"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    return fmt(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1208_0_1207_next",
            "local_path": "1207-Y5-R10-quotient-coframe-lock-or-epsilon-geom-source-pack.md",
            "needle": "NEXT1207_0_1208",
            "purpose": "handoff to P_loc parallel-projector or nabla_P_loc bound",
        },
        {
            "source_id": "SRC1208_1_1207_nabla_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1207_EPSILON_GEOM_COMPONENT_SOURCE_PACK.csv",
            "needle": "EGP1207_0_nabla_P_loc",
            "purpose": "nabla_P_loc source-pack row and missing columns",
        },
        {
            "source_id": "SRC1208_2_1207_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1207_PRESSURE_AND_ABSORPTION_GATE.csv",
            "needle": "PGA1207_0_total_formula",
            "purpose": "epsilon_geom pressure target and absorption gate",
        },
        {
            "source_id": "SRC1208_3_1206_projector_lowering",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1206_LOWERED_COMPONENT_DERIVATIONS.csv",
            "needle": "DRV1206_1_projector_leakage_lowering",
            "purpose": "projector leakage lowered to epsilon_geom",
        },
        {
            "source_id": "SRC1208_4_1195_adjoint",
            "local_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_1_formal_adjoint",
            "purpose": "formal adjoint contains derivative projector terms",
        },
        {
            "source_id": "SRC1208_5_1196_projector",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_3_projector_perturbation_bound",
            "purpose": "projector perturbation absorption condition",
        },
        {
            "source_id": "SRC1208_6_1196_boundary_projector",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "BP1196_2_projector_boundary_leakage",
            "purpose": "Delta_P includes nabla P_loc, boundary pullback, domain/coframe variation",
        },
        {
            "source_id": "SRC1208_7_1019_projector_verdict",
            "local_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "PO1019_5_verdict",
            "purpose": "projector orthogonality/silence not yet closed",
        },
        {
            "source_id": "SRC1208_8_1003_frame_verdict",
            "local_path": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
            "needle": "CFA1003_6_theorem_verdict",
            "purpose": "coframe/frame theorem remains unsigned for total zero",
        },
        {
            "source_id": "SRC1208_9_1029_shadow_frame",
            "local_path": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
            "needle": "NST1029_1_chain_rule_zero",
            "purpose": "no-shadow-frame chain-rule zero is vertical/readout, not spatial nabla P_loc",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    pressure_in = load_csv(OUT_DIR / "P8_Y5_R10_1207_PRESSURE_AND_ABSORPTION_GATE.csv")
    target = float(next(row for row in pressure_in if row["pressure_id"] == "PGA1207_0_total_formula")["target"])

    ploc_audit = [
        {
            "audit_id": "PPA1208_0_projector_identity",
            "object": "P_loc",
            "derivation": "P_loc^2=P_loc implies nabla(P_loc^2)=nabla P_loc, hence P(nablaP)P=0 and (I-P)(nablaP)(I-P)=0; derivative leakage is purely off-diagonal between image and kernel.",
            "zero_condition": "nabla P_loc=0 iff the image and kernel splitting are both parallel under the same local connection.",
            "required_parent_inputs": "P_loc_definition;connection;image_subbundle;kernel_subbundle;domain_id;norm_id",
            "current_status": "DERIVED_IDENTITY_NOT_ZERO",
            "source_anchor": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md::DTA1195_1_formal_adjoint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PPA1208_1_parallel_splitting_iff",
            "object": "nabla_P_loc_Linf",
            "derivation": "For an orthogonal projector onto E, nablaP is controlled by the second fundamental forms of E and E_perp. If both second fundamental forms vanish, the projector is covariantly parallel; if either is live, nablaP is live.",
            "zero_condition": "II_E=0 and II_Eperp=0 with no connection mismatch in the same observed domain.",
            "required_parent_inputs": "E_definition;Eperp_definition;Levi_Civita_or_parent_connection;II_E_norm;II_Eperp_norm;connection_mismatch_norm",
            "current_status": "CONDITIONAL_ZERO_REDUCED_TO_PARALLEL_SPLITTING",
            "source_anchor": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md::CKZ1196_3_projector_perturbation_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PPA1208_2_unit_normal_projector",
            "object": "P_loc=g-sigma u_otimes_u",
            "derivation": "Metric compatibility gives nablaP= -sigma[(nabla u) otimes u + u otimes (nabla u)], so ||nablaP|| <= 2||nabla u|| for a unit normal/tangent projector.",
            "zero_condition": "the selected normal/tangent field u is covariantly constant across the local domain.",
            "required_parent_inputs": "u_field_source;normalization;connection_path;nabla_u_norm;domain_radius;boundary_conditions",
            "current_status": "DERIVED_BOUND_NOT_NUMERIC",
            "source_anchor": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md::BP1196_2_projector_boundary_leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PPA1208_3_fermi_local_domain",
            "object": "local Fermi/readout projector",
            "derivation": "A Fermi or local-inertial frame can set the connection coefficients to zero at the central worldline/point, but over a finite domain the projector drift is curvature-controlled: ||nablaP||_Linf(D_L) <= C_Fermi L_D||Riemann||_Linf + O(L_D^2||nabla Riemann||).",
            "zero_condition": "exact point limit L_D=0, or flat/parallel parent geometry over the whole observed domain.",
            "required_parent_inputs": "Fermi_frame_source;L_D;Riemann_norm;nabla_Riemann_norm;C_Fermi;remainder_bound",
            "current_status": "FINITE_DOMAIN_BOUND_REDUCED_TO_CURVATURE_NOT_ZERO",
            "source_anchor": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md::CFA1003_6_theorem_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PPA1208_4_quotient_chain_rule_limit",
            "object": "P_loc=Pi(q(Phi)) route",
            "derivation": "If P_loc factors through q, then nablaP_loc=D_Pi(q)nablaq for spacetime derivatives. Vertical chain-rule silence only kills variations along ker(Dq); it does not kill ordinary spacetime gradients unless D_Pi=0 or nablaq=0.",
            "zero_condition": "D_Pi=0 on the local branch, or q is covariantly constant in the observed spacetime domain.",
            "required_parent_inputs": "q_map;Pi_definition;D_Pi_norm;nabla_q_norm;vertical_vs_spacetime_derivative_split",
            "current_status": "QUOTIENT_VERTICAL_ZERO_NOT_ENOUGH",
            "source_anchor": "1207-Y5-R10-quotient-coframe-lock-or-epsilon-geom-source-pack.md::ZEA1207_2_parallel_projector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PPA1208_5_zero_verdict",
            "object": "nabla_P_loc_Linf=0",
            "derivation": "The parent corpus currently gives a conditional route to projector silence, but it has not signed the stronger parallel-splitting/coframe/domain/connection package needed to set nabla_P_loc_Linf=0.",
            "zero_condition": "one parent action/domain proves parallel splitting, fixed connection, fixed readout projector, and boundary silence together.",
            "required_parent_inputs": "parent_action_clause;domain_clause;connection_clause;P_loc_parallel_clause;boundary_projection_clause",
            "current_status": "ZERO_NOT_CLAIMED_BOUND_ROUTE_SELECTED",
            "source_anchor": "1207-Y5-R10-quotient-coframe-lock-or-epsilon-geom-source-pack.md::PGA1207_2_total_zero_condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_laws = [
        {
            "law_id": "NPL1208_0_parallel_splitting_bound",
            "quantity": "nabla_P_loc_Linf",
            "bound_formula": "||nabla P_loc||_Linf <= C_split*(||II_E||_Linf + ||II_Eperp||_Linf + ||A_conn||_Linf)",
            "derivation_basis": "P=P^2 makes nablaP off-diagonal; off-diagonal connection components are exactly the second-fundamental/splitting-drift terms plus connection mismatch.",
            "required_inputs": "C_split;II_E_norm;II_Eperp_norm;A_conn_norm;domain_id;norm_id;source_path",
            "status": "DERIVED_SYMBOLIC_LOWERING_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "NPL1208_1_unit_vector_bound",
            "quantity": "nabla_P_loc_Linf",
            "bound_formula": "for P=g-sigma u⊗u, ||nabla P||_Linf <= 2||nabla u||_Linf",
            "derivation_basis": "metric compatibility and unit-field projector differentiation.",
            "required_inputs": "u_definition;connection_path;nabla_u_norm;domain_id;norm_id;source_path",
            "status": "DERIVED_SYMBOLIC_LOWERING_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "NPL1208_2_fermi_curvature_bound",
            "quantity": "nabla_P_loc_Linf",
            "bound_formula": "||nabla P_loc||_Linf(D_L) <= C_Fermi*L_D*||Riemann||_Linf(D_L) + C_Fermi2*L_D^2*||nabla Riemann||_Linf(D_L)",
            "derivation_basis": "Fermi/local-inertial transport freezes the projector at the central readout point; finite-domain drift is controlled by curvature and its first derivative.",
            "required_inputs": "Fermi_chart_source;L_D;Riemann_norm;nabla_Riemann_norm;C_Fermi;C_Fermi2;remainder_control;source_path",
            "status": "BEST_NUMERIC_ROUTE_SOURCE_READY_NOT_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "NPL1208_3_quotient_projector_bound",
            "quantity": "nabla_P_loc_Linf",
            "bound_formula": "if P_loc=Pi(q(Phi)), ||nabla P_loc||_Linf <= ||D Pi||_Linf*||nabla q||_Linf",
            "derivation_basis": "ordinary spacetime chain rule, not vertical variational chain rule.",
            "required_inputs": "Pi_definition;D_Pi_norm;nabla_q_norm;branch_domain;source_path",
            "status": "DERIVED_SYMBOLIC_LOWERING_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "NPL1208_4_projector_pressure_insert",
            "quantity": "q_projector",
            "bound_formula": "q_projector <= C_P*(nabla_P_loc_Linf + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)*G_res_norm",
            "derivation_basis": "1206/1207 epsilon_geom lowering with nabla_P_loc now reducible to splitting/curvature/quotient constants.",
            "required_inputs": "C_P;G_res_norm;nabla_P_loc_bound;coframe_lock_bound;domain_motion_bound;projector_stress_bound",
            "status": "PRESSURE_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_ready = [
        {
            "row_id": "SRN1208_0_parallel_splitting_row",
            "domain_id": "MISSING_DOMAIN",
            "norm_id": "MISSING_NORM",
            "P_loc_definition_path": "MISSING_P_LOC_DEFINITION_PATH",
            "connection_path": "MISSING_CONNECTION_PATH",
            "projector_family": "orthogonal_subbundle_projector",
            "lower_bound_formula": "C_split*(II_E_norm+II_Eperp_norm+A_conn_norm)",
            "lower_level_constants": "C_split;II_E_norm;II_Eperp_norm;A_conn_norm",
            "numeric_value": "MISSING",
            "units": "1/length",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SRN1208_1_unit_vector_row",
            "domain_id": "MISSING_DOMAIN",
            "norm_id": "MISSING_NORM",
            "P_loc_definition_path": "MISSING_UNIT_FIELD_PROJECTOR_PATH",
            "connection_path": "MISSING_CONNECTION_PATH",
            "projector_family": "unit_normal_or_tangent_projector",
            "lower_bound_formula": "2*nabla_u_norm",
            "lower_level_constants": "nabla_u_norm",
            "numeric_value": "MISSING",
            "units": "1/length",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SRN1208_2_fermi_curvature_row",
            "domain_id": "MISSING_LOCAL_FERMI_DOMAIN",
            "norm_id": "MISSING_WEIGHTED_LINF_NORM",
            "P_loc_definition_path": "MISSING_FERMI_PROJECTOR_PATH",
            "connection_path": "MISSING_PARENT_CONNECTION_PATH",
            "projector_family": "Fermi_local_readout_projector",
            "lower_bound_formula": "C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm",
            "lower_level_constants": "C_Fermi;C_Fermi2;L_D;Riemann_norm;nabla_Riemann_norm",
            "numeric_value": "MISSING",
            "units": "1/length",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "BEST_SOURCE_ROW_FOR_NEXT_RUN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SRN1208_3_quotient_projector_row",
            "domain_id": "MISSING_BRANCH_DOMAIN",
            "norm_id": "MISSING_NORM",
            "P_loc_definition_path": "MISSING_PI_OF_Q_PROJECTOR_PATH",
            "connection_path": "MISSING_CONNECTION_PATH",
            "projector_family": "quotient_projector_Pi_of_q",
            "lower_bound_formula": "D_Pi_norm*nabla_q_norm",
            "lower_level_constants": "D_Pi_norm;nabla_q_norm",
            "numeric_value": "MISSING",
            "units": "1/length",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    pressure_rows = [
        {
            "comparison_id": "CMP1208_0_preserved_projector_target",
            "object": "q_projector",
            "formula": "epsilon_geom*G_res_norm <= target",
            "target": target,
            "derived_requirement": "target preserved from 1207",
            "current_status": "TARGET_PRESERVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1208_1_isolated_nabla_requirement",
            "object": "nabla_P_loc_Linf",
            "formula": "if coframe/domain/stress terms vanish, C_P*nabla_P_loc_Linf*G_res_norm <= target",
            "target": target,
            "derived_requirement": "nabla_P_loc_Linf <= target/(C_P*G_res_norm)",
            "current_status": "SYMBOLIC_REQUIREMENT_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1208_2_fermi_curvature_requirement",
            "object": "Fermi curvature smallness",
            "formula": "C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm)*G_res_norm <= target",
            "target": target,
            "derived_requirement": "local domain radius and curvature must make projector drift below R10 harsh split",
            "current_status": "BEST_NEXT_NUMERIC_GATE_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1208_3_absorption_requirement",
            "object": "projector perturbation absorption",
            "formula": "C_CK*C_P*(nabla_P_loc_Linf + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf) < 1",
            "target": "<1",
            "derived_requirement": "same geometry source rows must also satisfy the CK absorption gate",
            "current_status": "SYMBOLIC_REQUIREMENT_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1208_0_verdict",
            "condition": "Can quotient/coframe descent alone prove nabla_P_loc=0?",
            "decision": "No. It kills vertical/readout variation, not spatial derivative of the projector.",
            "result": "parallel-projector zero remains conditional; bound route selected.",
            "next_action": "source or derive local Fermi-domain curvature constants and domain-motion/projector-stress locks.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1208_1_best_route",
            "condition": "Which lowered law is least ugly for local GR?",
            "decision": "Use the Fermi/local-domain curvature bound first, because it ties projector drift to ordinary local curvature and domain size instead of inventing a new MTS parameter.",
            "result": "nabla_P_loc is no longer a primitive blocker; it is a curvature/domain/source-row problem.",
            "next_action": "build 1209 around L_D, Riemann_norm, C_Fermi, C_P, G_res_norm, and domain_motion in one common norm.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1208_0_parallel_projector_zero",
            "gate": "nabla_P_loc_Linf=0",
            "status": "BLOCKED",
            "reason": "parallel splitting, fixed connection, and fixed projector are not parent-signed in one local domain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1208_1_nabla_bound_numeric",
            "gate": "numeric nabla_P_loc_Linf bound",
            "status": "BLOCKED",
            "reason": "lower formulas exist but constants are still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1208_2_projector_pressure",
            "gate": "q_projector <= target",
            "status": "BLOCKED",
            "reason": "C_P, G_res_norm, and finite geometry constants remain unsourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1208_3_local_GR_or_R10_pass",
            "gate": "local-GR/R10 pass",
            "status": "BLOCKED",
            "reason": "1208 lowers one component only; no local-GR or R10 claim is allowed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1208_0_1209",
            "target_file": "1209-Y5-R10-local-Fermi-domain-curvature-source-pack-or-domain-motion-lock.md",
            "target_script": "scripts/Y5_R10_local_Fermi_domain_curvature_source_pack_or_domain_motion_lock.py",
            "task": "fill the Fermi-domain source row for L_D, Riemann_norm, nabla_Riemann_norm, C_Fermi, C_P, G_res_norm, and domain_motion/projector_stress in one norm; otherwise keep q_projector blocked",
            "success_condition": "projector pressure can be evaluated as a nonclaim numeric smoke row, or domain-motion/projector-stress are theorem-zero in the same parent local domain",
            "do_not_do": "do not claim nabla_P_loc=0 from pointwise local inertial coordinates; do not edit formalization-workbench; do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    audit_fields = ["audit_id", "object", "derivation", "zero_condition", "required_parent_inputs", "current_status", "source_anchor", "valid_for_claim", "claim_allowed"]
    bound_fields = ["law_id", "quantity", "bound_formula", "derivation_basis", "required_inputs", "status", "valid_for_claim", "claim_allowed"]
    source_ready_fields = ["row_id", "domain_id", "norm_id", "P_loc_definition_path", "connection_path", "projector_family", "lower_bound_formula", "lower_level_constants", "numeric_value", "units", "source_path", "current_status", "valid_for_claim", "claim_allowed"]
    pressure_fields = ["comparison_id", "object", "formula", "target", "derived_requirement", "current_status", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(PLOC_AUDIT_PATH, ploc_audit, audit_fields)
    write_csv(BOUND_LAW_PATH, bound_laws, bound_fields)
    write_csv(SOURCE_READY_PATH, source_ready, source_ready_fields)
    write_csv(PRESSURE_PATH, pressure_rows, pressure_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        PLOC_AUDIT_PATH,
        BOUND_LAW_PATH,
        SOURCE_READY_PATH,
        PRESSURE_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    projector_identity_present = any(row["audit_id"] == "PPA1208_0_projector_identity" for row in ploc_audit)
    quotient_not_enough = any(row["current_status"] == "QUOTIENT_VERTICAL_ZERO_NOT_ENOUGH" for row in ploc_audit)
    zero_not_claimed = any(row["current_status"] == "ZERO_NOT_CLAIMED_BOUND_ROUTE_SELECTED" for row in ploc_audit)
    lower_bound_present = {"NPL1208_0_parallel_splitting_bound", "NPL1208_1_unit_vector_bound", "NPL1208_2_fermi_curvature_bound", "NPL1208_3_quotient_projector_bound"}.issubset({row["law_id"] for row in bound_laws})
    source_ready_complete = {"SRN1208_0_parallel_splitting_row", "SRN1208_1_unit_vector_row", "SRN1208_2_fermi_curvature_row", "SRN1208_3_quotient_projector_row"}.issubset({row["row_id"] for row in source_ready})
    pressure_preserved = abs(target - 1.17233215026e-05) < 1e-16
    fermi_route_selected = any(row["decision_id"] == "DEC1208_1_best_route" and "Fermi" in row["decision"] for row in decisions)
    no_claim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in ploc_audit + bound_laws + source_ready + pressure_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1209 = next_rows[0]["target_file"].startswith("1209-")

    validation_rows = [
        validation_row("VAL1208_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1208_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1208_2_projector_identity", "projector derivative identity is recorded", projector_identity_present, "PPA1208_0 present"),
        validation_row("VAL1208_3_quotient_not_enough", "vertical quotient silence is not overclaimed", quotient_not_enough, "PPA1208_4 blocks spatial nabla_P_loc zero"),
        validation_row("VAL1208_4_zero_not_claimed", "nabla_P_loc zero is not claimed", zero_not_claimed, "PPA1208_5 selects bound route"),
        validation_row("VAL1208_5_lower_bound_laws", "nabla_P_loc is reduced to lower geometry constants", lower_bound_present, ",".join(row["law_id"] for row in bound_laws)),
        validation_row("VAL1208_6_source_ready_rows", "source-ready nabla_P_loc rows are staged", source_ready_complete, ",".join(row["row_id"] for row in source_ready)),
        validation_row("VAL1208_7_pressure_preserved", "1207 projector pressure target is preserved", pressure_preserved, f"target={fmt(target)}"),
        validation_row("VAL1208_8_fermi_route_selected", "Fermi curvature/domain route is selected for next numeric gate", fermi_route_selected, "DEC1208_1 present"),
        validation_row("VAL1208_9_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1208_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1208_11_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1208_12_next_target", "next target is staged", next_1209, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1208_13_overall",
            "overall 1208 validation",
            validation_pass,
            "1208 P_loc parallel-projector audit is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1208 Y5/R10 P_loc Parallel Projector Or Nabla P_loc Bound

**Current verdict:** 1208 does **not** prove `nabla_P_loc_Linf=0`. It proves the sharper local geometry statement: a projector is silent only when the image/kernel splitting is covariantly parallel under the same connection and domain. Quotient/coframe descent by itself is vertical/readout silence, not spatial projector silence.

**Main progress:** `nabla_P_loc_Linf` is no longer a primitive mystery constant. It is reduced to lower geometry rows: second-fundamental/splitting drift, unit-field drift, Fermi curvature/domain drift, or quotient-projector chain-rule drift. The least ugly next route is the finite-domain Fermi bound `||nabla P_loc||_Linf <= C_Fermi L_D||Riemann|| + C_Fermi2 L_D^2||nabla Riemann||`.

**Pressure kept alive:** the harsh projector target remains `epsilon_geom*G_res_norm <= {fmt(target)}`. If the other epsilon components are zero or separately bounded, the isolated pressure is `nabla_P_loc_Linf <= target/(C_P*G_res_norm)`. This is not yet numeric because `C_P` and `G_res_norm` are still unsourced.

## Source Register

{markdown_table(source_rows, source_fields)}

## P_loc Parallel Projector Audit

{markdown_table(ploc_audit, audit_fields)}

## Nabla P_loc Bound Law

{markdown_table(bound_laws, bound_fields)}

## Source-Ready Nabla P_loc Rows

{markdown_table(source_ready, source_ready_fields)}

## Pressure Comparison

{markdown_table(pressure_rows, pressure_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print(f"projector_target={fmt(target)}")
    print("nabla_P_loc_zero_claimed=false")


if __name__ == "__main__":
    main()
