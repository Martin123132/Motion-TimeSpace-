from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1209"
TITLE = "1209-Y5-R10-local-Fermi-domain-curvature-source-pack-or-domain-motion-lock"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FERMI_DERIVATION_PATH = OUT_DIR / f"{PACK_ID}_FERMI_DOMAIN_DERIVATION.csv"
DOMAIN_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv"
SOURCE_PACK_PATH = OUT_DIR / f"{PACK_ID}_UNIFIED_SOURCE_PACK.csv"
PRESSURE_PATH = OUT_DIR / f"{PACK_ID}_PRESSURE_SMOKE_SCHEMA.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1209_VALIDATION.csv"


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
            "source_id": "SRC1209_0_1208_next",
            "local_path": "1208-Y5-R10-Ploc-parallel-projector-or-nablaPloc-bound.md",
            "needle": "NEXT1208_0_1209",
            "purpose": "handoff to local Fermi-domain curvature source pack",
        },
        {
            "source_id": "SRC1209_1_1208_fermi_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1208_NABLAPLOC_BOUND_LAW.csv",
            "needle": "NPL1208_2_fermi_curvature_bound",
            "purpose": "finite-domain Fermi curvature bound for nabla_P_loc",
        },
        {
            "source_id": "SRC1209_2_1208_fermi_row",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1208_SOURCE_READY_NABLAPLOC_ROW.csv",
            "needle": "SRN1208_2_fermi_curvature_row",
            "purpose": "source-ready Fermi projector row to refine",
        },
        {
            "source_id": "SRC1209_3_1208_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1208_PRESSURE_COMPARISON.csv",
            "needle": "CMP1208_2_fermi_curvature_requirement",
            "purpose": "Fermi curvature pressure requirement",
        },
        {
            "source_id": "SRC1209_4_1207_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1207_PRESSURE_AND_ABSORPTION_GATE.csv",
            "needle": "PGA1207_0_total_formula",
            "purpose": "epsilon_geom target and absorption gate",
        },
        {
            "source_id": "SRC1209_5_1206_lowering",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1206_LOWERED_COMPONENT_DERIVATIONS.csv",
            "needle": "DRV1206_1_projector_leakage_lowering",
            "purpose": "q_projector lowered to epsilon_geom*G_res_norm",
        },
        {
            "source_id": "SRC1209_6_1195_adjoint",
            "local_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_1_formal_adjoint",
            "purpose": "D_T adjoint shows derivative projector term to be bounded",
        },
        {
            "source_id": "SRC1209_7_1196_absorption",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_3_projector_perturbation_bound",
            "purpose": "operator absorption gate for projector leakage",
        },
        {
            "source_id": "SRC1209_8_1003_frame_verdict",
            "local_path": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
            "needle": "CFA1003_6_theorem_verdict",
            "purpose": "frame/coframe parent theorem still unsigned",
        },
        {
            "source_id": "SRC1209_9_1207_coframe_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1207_EPSILON_GEOM_ZERO_AUDIT.csv",
            "needle": "ZEA1207_0_chain_rule_coframe",
            "purpose": "coframe chain-rule zero is conditional and carried forward",
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

    pressure_in = load_csv(OUT_DIR / "P8_Y5_R10_1208_PRESSURE_COMPARISON.csv")
    target = float(next(row for row in pressure_in if row["comparison_id"] == "CMP1208_0_preserved_projector_target")["target"])

    fermi_derivation = [
        {
            "derivation_id": "FDL1209_0_local_tube_setup",
            "object": "D_L local Fermi tube",
            "derived_law": "Choose a central timelike curve gamma, Fermi/Fermi-Walker transported tetrad e_A, and finite radius L_D. Pointwise local inertial silence is not enough; the finite tube carries connection drift.",
            "clean_zero_condition": "L_D=0, or flat/parallel geometry over the entire tube with fixed projector components.",
            "new_lower_inputs": "central_worldline;Fermi_chart_source;L_D;transport_rule;support_weight",
            "status": "DOMAIN_SETUP_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "FDL1209_1_connection_drift",
            "object": "connection scale",
            "derived_law": "||Gamma||_Linf(D_L) <= C_Gamma1*L_D*||Riemann||_Linf + C_Gamma2*L_D^2*||nabla Riemann||_Linf + C_acc*||a|| + C_rot*||omega||",
            "clean_zero_condition": "geodesic/Fermi-Walker branch with a=0, omega=0 and curvature-domain terms negligible or zero.",
            "new_lower_inputs": "C_Gamma1;C_Gamma2;L_D;Riemann_norm;nabla_Riemann_norm;acceleration_norm;rotation_norm",
            "status": "FINITE_DOMAIN_CONNECTION_BOUND_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "FDL1209_2_projector_components",
            "object": "P_loc components in Fermi frame",
            "derived_law": "If P_loc has fixed components in the Fermi tetrad, ||nabla P_loc|| <= C_Ploc*||Gamma||. If P components vary by readout/source choice, add ||partial_Fermi P_loc||.",
            "clean_zero_condition": "fixed projector components and zero connection drift throughout D_L.",
            "new_lower_inputs": "C_Ploc;partial_Fermi_P_norm;projector_definition_path;connection_path",
            "status": "PROJECTOR_DRIFT_LOWERED_TO_CONNECTION_AND_COMPONENT_DRIFT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "FDL1209_3_clean_freefall_fermi_bound",
            "object": "nabla_P_loc_Linf",
            "derived_law": "clean branch: ||nabla P_loc||_Linf(D_L) <= C_Fermi*L_D*||Riemann||_Linf(D_L) + C_Fermi2*L_D^2*||nabla Riemann||_Linf(D_L)",
            "clean_zero_condition": "free-fall Fermi frame, fixed P components, no domain/readout variation, and exact flat/parallel finite domain.",
            "new_lower_inputs": "C_Fermi;C_Fermi2;L_D;Riemann_norm;nabla_Riemann_norm;remainder_control",
            "status": "BEST_NONCLAIM_NUMERIC_ROUTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "FDL1209_4_pressure_insert",
            "object": "q_projector",
            "derived_law": "q_projector <= C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)*G_res_norm",
            "clean_zero_condition": "all bracket terms theorem-zero or sourced below target/(C_P*G_res_norm).",
            "new_lower_inputs": "C_P;G_res_norm;coframe_lock_Linf;domain_motion_Linf;projector_stress_Linf",
            "status": "PRESSURE_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    domain_audit = [
        {
            "audit_id": "DMP1209_0_domain_motion_zero_branch",
            "component": "domain_motion_Linf",
            "zero_or_bound_law": "domain_motion_Linf=0 if the support tube, boundary, time normal, and weight are fixed by the same Fermi/parent readout map.",
            "failure_mode": "moving lab/support, changing readout weight, non-geodesic frame, or unmatched boundary transport",
            "source_columns_needed": "domain_id;central_worldline;support_map;boundary_transport;weight_function;domain_motion_norm;source_path",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DMP1209_1_non_geodesic_lab_bound",
            "component": "domain_motion_Linf",
            "zero_or_bound_law": "non-geodesic branch: domain_motion_Linf <= C_D*(acceleration_norm + rotation_norm + L_D*Riemann_norm + L_D^2*nabla_Riemann_norm)",
            "failure_mode": "Earth/lab frame acceleration or rotation can be small but cannot be silently set to zero",
            "source_columns_needed": "C_D;acceleration_norm;rotation_norm;L_D;Riemann_norm;nabla_Riemann_norm;source_path",
            "current_status": "BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DMP1209_2_projector_stress_zero_branch",
            "component": "projector_stress_Linf",
            "zero_or_bound_law": "projector_stress_Linf=0 if P_loc definition, readout channel, and support weights are not varied independently of q and the Fermi domain.",
            "failure_mode": "hidden readout/source dependence changes P_loc even when coframe vertical variation is silent",
            "source_columns_needed": "P_loc_definition_path;readout_channel_path;support_weight_path;projector_stress_norm;source_path",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DMP1209_3_projector_stress_bound",
            "component": "projector_stress_Linf",
            "zero_or_bound_law": "projector_stress_Linf <= C_stress*(partial_readout_P_norm + partial_weight_P_norm + connection_mismatch_norm)",
            "failure_mode": "projector stress becomes a finite source row instead of a theorem zero",
            "source_columns_needed": "C_stress;partial_readout_P_norm;partial_weight_P_norm;connection_mismatch_norm;source_path",
            "current_status": "BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DMP1209_4_total_epsilon_status",
            "component": "epsilon_geom",
            "zero_or_bound_law": "epsilon_geom=C_P*(fermi_curvature_projector_drift + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)",
            "failure_mode": "even if Fermi projector drift is tiny, domain/stress/C_P/G_res can still block the local-GR/R10 pass",
            "source_columns_needed": "C_P;G_res_norm;all component bounds;C_CK;target",
            "current_status": "LOWERED_NOT_NUMERIC",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_pack = [
        {
            "input_id": "USP1209_0_domain",
            "symbol": "D_L",
            "definition": "finite local Fermi test tube/domain used for the projector leakage bound",
            "formula_role": "sets finite radius and support for all norms",
            "units": "domain metadata",
            "required_source": "central_worldline;support_radius;boundary_transport;weight_function",
            "current_value": "MISSING",
            "current_status": "MISSING_LOCAL_DOMAIN_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_1_LD",
            "symbol": "L_D",
            "definition": "radius/diameter scale of the finite Fermi domain",
            "formula_role": "multiplies curvature in nabla_P_loc bound",
            "units": "length",
            "required_source": "domain radius in same coordinates/norm as curvature",
            "current_value": "MISSING",
            "current_status": "MISSING_LENGTH_SCALE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_2_Riemann",
            "symbol": "Riemann_norm",
            "definition": "supremum norm of local curvature over D_L",
            "formula_role": "first finite-domain projector drift term",
            "units": "1/length^2",
            "required_source": "GR/MTS local metric or curvature profile source",
            "current_value": "MISSING",
            "current_status": "MISSING_CURVATURE_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_3_nablaR",
            "symbol": "nabla_Riemann_norm",
            "definition": "supremum norm of curvature gradient over D_L",
            "formula_role": "second-order/remainder projector drift term",
            "units": "1/length^3",
            "required_source": "curvature-gradient profile or conservative upper bound",
            "current_value": "MISSING",
            "current_status": "MISSING_CURVATURE_GRADIENT_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_4_CFermi",
            "symbol": "C_Fermi;C_Fermi2",
            "definition": "coordinate/norm constants for the Fermi connection and projector drift estimates",
            "formula_role": "converts curvature-domain scale into nabla_P_loc_Linf",
            "units": "dimensionless",
            "required_source": "norm convention and Fermi expansion theorem/source path",
            "current_value": "MISSING",
            "current_status": "MISSING_OPERATOR_CONSTANTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_5_accelrot",
            "symbol": "acceleration_norm;rotation_norm",
            "definition": "non-geodesic lab-frame corrections if the domain is not ideal free-fall/Fermi-Walker",
            "formula_role": "domain_motion and connection drift correction",
            "units": "1/length",
            "required_source": "lab frame/source trajectory or free-fall theorem-zero clause",
            "current_value": "MISSING_OR_ZERO_BRANCH_UNSIGNED",
            "current_status": "MISSING_NON_GEODESIC_FRAME_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_6_CP",
            "symbol": "C_P",
            "definition": "operator constant converting geometry leakage terms into epsilon_geom",
            "formula_role": "epsilon_geom multiplier",
            "units": "dimensionless_or_norm_defined",
            "required_source": "same-norm operator estimate from D_T adjoint/projector leakage",
            "current_value": "MISSING",
            "current_status": "MISSING_OPERATOR_CONSTANT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_7_Gres",
            "symbol": "G_res_norm",
            "definition": "local residual source norm in the same domain/norm",
            "formula_role": "q_projector = epsilon_geom*G_res_norm scoring factor",
            "units": "same as local residual norm",
            "required_source": "parent GR-reduction residual profile or theorem-zero source",
            "current_value": "MISSING",
            "current_status": "MISSING_G_RES_PROFILE_NORM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_8_domain_motion",
            "symbol": "domain_motion_Linf",
            "definition": "finite support/boundary/readout-domain drift term",
            "formula_role": "epsilon_geom additive component",
            "units": "1/length_or_norm_defined",
            "required_source": "domain lock theorem or non-geodesic/domain bound",
            "current_value": "MISSING",
            "current_status": "MISSING_DOMAIN_LOCK_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_9_projector_stress",
            "symbol": "projector_stress_Linf",
            "definition": "variation of P_loc from readout/source/support changes not captured by Fermi curvature drift",
            "formula_role": "epsilon_geom additive component",
            "units": "1/length_or_norm_defined",
            "required_source": "projector definition lock or finite stress bound",
            "current_value": "MISSING",
            "current_status": "MISSING_PROJECTOR_STRESS_LOCK_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "USP1209_10_CCK",
            "symbol": "C_CK",
            "definition": "conformal-Killing/Korn absorption constant",
            "formula_role": "requires C_CK*epsilon_geom < 1",
            "units": "norm_defined",
            "required_source": "same-domain CK/Korn estimate",
            "current_value": "MISSING",
            "current_status": "MISSING_ABSORPTION_CONSTANT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    pressure_rows = [
        {
            "pressure_id": "PSC1209_0_clean_fermi_projector",
            "formula": "q_projector <= C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm)*G_res_norm",
            "target": target,
            "claim_rule": "valid only if coframe/domain/projector-stress are theorem-zero in the same domain",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PSC1209_1_full_projector_budget",
            "formula": "q_projector <= C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)*G_res_norm",
            "target": target,
            "claim_rule": "all terms must be numeric/sourced or theorem-zero; any MISSING keeps branch blocked",
            "current_status": "FULL_SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PSC1209_2_absorption_budget",
            "formula": "C_CK*C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf) < 1",
            "target": "<1",
            "claim_rule": "same source rows must pass the operator absorption condition",
            "current_status": "ABSORPTION_SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PSC1209_3_radius_requirement_clean_branch",
            "formula": "if nabla_Riemann term is negligible, L_D <= target/(C_P*C_Fermi*Riemann_norm*G_res_norm)",
            "target": target,
            "claim_rule": "only an algebraic design inequality until C_P, C_Fermi, Riemann_norm, and G_res_norm are sourced",
            "current_status": "DESIGN_INEQUALITY_NOT_NUMERIC",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "PSC1209_4_blocker_policy",
            "formula": "if any of C_P,G_res_norm,L_D,Riemann_norm,nabla_Riemann_norm,domain_motion,projector_stress are missing, q_projector claim_allowed=false",
            "target": "no missing claim inputs",
            "claim_rule": "missing source rows block claim even if formula looks small by intuition",
            "current_status": "BLOCK_POLICY_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1209_0_verdict",
            "condition": "Can finite-domain Fermi geometry close q_projector now?",
            "decision": "No numeric close yet. It lowers nabla_P_loc and domain drift to sourceable curvature/domain constants, but C_P, G_res_norm, and local domain constants are missing.",
            "result": "projector branch is stronger and more GR-like, but remains nonclaim.",
            "next_action": "build a first nonclaim local-curvature/G_res bracket smoke runner.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1209_1_best_route",
            "condition": "What should be sourced first?",
            "decision": "Source or bracket G_res_norm and C_P alongside a conservative local curvature/domain scale; curvature alone cannot score q_projector.",
            "result": "next checkpoint should produce a feasibility map, not a pass/fail claim.",
            "next_action": "1210 first local curvature scale plus G_res/C_P bracket smoke.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1209_0_projector_zero",
            "gate": "nabla_P_loc_Linf=0",
            "status": "BLOCKED",
            "reason": "Fermi pointwise silence does not prove finite-domain projector silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1209_1_projector_numeric",
            "gate": "q_projector numeric target",
            "status": "BLOCKED",
            "reason": "C_P, G_res_norm, curvature/domain constants, and domain/stress terms are unsourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1209_2_domain_motion_zero",
            "gate": "domain_motion_Linf=0",
            "status": "BLOCKED",
            "reason": "requires parent-signed fixed Fermi support/boundary/readout map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1209_3_local_GR_R10_pass",
            "gate": "local-GR/R10 pass",
            "status": "BLOCKED",
            "reason": "1209 is a source-pack and derivation checkpoint only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1209_0_1210",
            "target_file": "1210-Y5-R10-first-local-curvature-scale-and-Gres-bracket-smoke.md",
            "target_script": "scripts/Y5_R10_first_local_curvature_scale_and_Gres_bracket_smoke.py",
            "task": "create a nonclaim feasibility/bracket runner for the clean Fermi projector budget using conservative ranges for L_D, Riemann_norm, C_Fermi, C_P, and G_res_norm, while keeping domain_motion/projector_stress as explicit blockers unless theorem-zero",
            "success_condition": "produce a pressure map showing what C_P*G_res_norm or domain radius would be required, without claiming local-GR/R10 pass",
            "do_not_do": "do not use hand-picked optimistic values as evidence, do not hide missing domain/stress terms, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    fermi_fields = ["derivation_id", "object", "derived_law", "clean_zero_condition", "new_lower_inputs", "status", "valid_for_claim", "claim_allowed"]
    domain_fields = ["audit_id", "component", "zero_or_bound_law", "failure_mode", "source_columns_needed", "current_status", "valid_for_claim", "claim_allowed"]
    pack_fields = ["input_id", "symbol", "definition", "formula_role", "units", "required_source", "current_value", "current_status", "valid_for_claim", "claim_allowed"]
    pressure_fields = ["pressure_id", "formula", "target", "claim_rule", "current_status", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(FERMI_DERIVATION_PATH, fermi_derivation, fermi_fields)
    write_csv(DOMAIN_AUDIT_PATH, domain_audit, domain_fields)
    write_csv(SOURCE_PACK_PATH, source_pack, pack_fields)
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
        FERMI_DERIVATION_PATH,
        DOMAIN_AUDIT_PATH,
        SOURCE_PACK_PATH,
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
    fermi_law_present = any(row["derivation_id"] == "FDL1209_3_clean_freefall_fermi_bound" for row in fermi_derivation)
    pressure_insert_present = any(row["derivation_id"] == "FDL1209_4_pressure_insert" for row in fermi_derivation)
    domain_audit_present = {"domain_motion_Linf", "projector_stress_Linf", "epsilon_geom"}.issubset({row["component"] for row in domain_audit})
    source_pack_complete = {"L_D", "Riemann_norm", "nabla_Riemann_norm", "C_Fermi;C_Fermi2", "C_P", "G_res_norm", "domain_motion_Linf", "projector_stress_Linf", "C_CK"}.issubset({row["symbol"] for row in source_pack})
    pressure_preserved = abs(target - 1.17233215026e-05) < 1e-16
    blocker_policy_present = any(row["pressure_id"] == "PSC1209_4_blocker_policy" for row in pressure_rows)
    no_missing_claim_rows = all(not (row["valid_for_claim"] and "MISSING" in row["current_value"]) for row in source_pack)
    no_claim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in fermi_derivation + domain_audit + source_pack + pressure_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1210 = next_rows[0]["target_file"].startswith("1210-")

    validation_rows = [
        validation_row("VAL1209_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1209_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1209_2_fermi_law_present", "clean Fermi finite-domain law is recorded", fermi_law_present, "FDL1209_3 present"),
        validation_row("VAL1209_3_pressure_insert", "projector pressure insert is recorded", pressure_insert_present, "FDL1209_4 present"),
        validation_row("VAL1209_4_domain_audit", "domain motion and projector stress are audited", domain_audit_present, ",".join(row["component"] for row in domain_audit)),
        validation_row("VAL1209_5_source_pack_complete", "unified source pack lists required constants", source_pack_complete, ",".join(row["symbol"] for row in source_pack)),
        validation_row("VAL1209_6_pressure_preserved", "1208 projector target is preserved", pressure_preserved, f"target={fmt(target)}"),
        validation_row("VAL1209_7_blocker_policy", "missing source rows block claims", blocker_policy_present, "PSC1209_4 present"),
        validation_row("VAL1209_8_no_missing_claim_rows", "no row with MISSING is valid for claim", no_missing_claim_rows, "all source pack rows nonclaim"),
        validation_row("VAL1209_9_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1209_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1209_11_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1209_12_next_target", "next target is staged", next_1210, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1209_13_overall",
            "overall 1209 validation",
            validation_pass,
            "1209 local Fermi-domain source pack is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1209 Y5/R10 Local Fermi Domain Curvature Source Pack Or Domain Motion Lock

**Current verdict:** 1209 does **not** close the local-GR/R10 projector gate. It does convert the finite-domain projector problem into a cleaner GR-style source problem: local curvature, curvature gradient, finite domain size, frame acceleration/rotation, and the same-norm operator constants.

**Main progress:** the live clean branch is now `||nabla P_loc||_Linf(D_L) <= C_Fermi L_D||Riemann||_Linf + C_Fermi2 L_D^2||nabla Riemann||_Linf`. If the lab/domain is not an ideal free-fall Fermi tube, acceleration, rotation, domain-motion, and projector-stress rows must be added rather than hidden.

**Pressure kept honest:** the harsh target remains `q_projector <= {fmt(target)}` via `q_projector <= C_P*(fermi_curvature_projector_drift + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)*G_res_norm`. This is a source-pack checkpoint, not a pass.

## Source Register

{markdown_table(source_rows, source_fields)}

## Fermi Domain Derivation

{markdown_table(fermi_derivation, fermi_fields)}

## Domain Motion And Projector Stress Audit

{markdown_table(domain_audit, domain_fields)}

## Unified Source Pack

{markdown_table(source_pack, pack_fields)}

## Pressure Smoke Schema

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
    print("local_GR_R10_claimed=false")


if __name__ == "__main__":
    main()
