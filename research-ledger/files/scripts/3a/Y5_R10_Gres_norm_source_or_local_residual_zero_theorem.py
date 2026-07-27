from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1211"
TITLE = "1211-Y5-R10-Gres-norm-source-or-local-residual-zero-theorem"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DEFINITION_PATH = OUT_DIR / f"{PACK_ID}_GRES_DEFINITION_AND_DECOMPOSITION.csv"
ZERO_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_GRES_ZERO_THEOREM_AUDIT.csv"
BOUND_PATH = OUT_DIR / f"{PACK_ID}_GRES_BOUND_DECOMPOSITION.csv"
SOURCE_READY_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_READY_GRES_ROWS.csv"
PRESSURE_BRIDGE_PATH = OUT_DIR / f"{PACK_ID}_CP_GRES_PRESSURE_BRIDGE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1211_VALIDATION.csv"


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
        if value == 0:
            return "0"
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
            "source_id": "SRC1211_0_1210_next",
            "local_path": "1210-Y5-R10-first-local-curvature-scale-and-Gres-bracket-smoke.md",
            "needle": "NEXT1210_0_1211",
            "purpose": "handoff to G_res norm source or local residual zero theorem",
        },
        {
            "source_id": "SRC1211_1_1210_gres_gap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1210_SOURCE_GAPS.csv",
            "needle": "GAP1210_1_Gres",
            "purpose": "G_res_norm identified as pressure bottleneck",
        },
        {
            "source_id": "SRC1211_2_1210_grid",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1210_FERMI_BRACKET_GRID.csv",
            "needle": "allowed_CpGres_product",
            "purpose": "allowed C_P*G_res product range from clean Fermi bracket",
        },
        {
            "source_id": "SRC1211_3_1193_Gres_definition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1193_VECTOR_TENSOR_COMPENSATOR_CONTRACT.csv",
            "needle": "VTC1193_0_residual_source_split",
            "purpose": "original G_res definition after scalar branch split",
        },
        {
            "source_id": "SRC1211_4_1193_ricci_exact",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
            "needle": "RES1193_5_matter_domain_failure",
            "purpose": "generic matter scalar exactness failure and Ricci-curl residual",
        },
        {
            "source_id": "SRC1211_5_1194_scalar_classifier",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1194_EINSTEIN_SCALAR_BOUND_FORMS.csv",
            "needle": "ESB1194_4_domain_classifier",
            "purpose": "Einstein/Ricci-flat scalar branch classifier",
        },
        {
            "source_id": "SRC1211_6_1195_range",
            "local_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_3_exact_range_condition",
            "purpose": "G_res range/cokernel condition for D_T",
        },
        {
            "source_id": "SRC1211_7_1199_profile_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1199_GRES_PROFILE_SCHEMA.csv",
            "needle": "GRP1199_0_G_res_profile",
            "purpose": "G_res profile source schema",
        },
        {
            "source_id": "SRC1211_8_956_source_spine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
            "needle": "SSG956_5_source_side_verdict",
            "purpose": "source-side GR/Newton hidden/species residual spine",
        },
        {
            "source_id": "SRC1211_9_1206_Gres_input",
            "local_path": "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            "needle": "IN1206_3_Gres_norm",
            "purpose": "G_res_norm same-domain input for boundary and projector routes",
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

    grid_rows_in = load_csv(OUT_DIR / "P8_Y5_R10_1210_FERMI_BRACKET_GRID.csv")
    allowed_products = [float(row["allowed_CpGres_product"]) for row in grid_rows_in]
    targets = {float(row["target"]) for row in grid_rows_in}
    target = next(iter(targets))
    allowed_min = min(allowed_products)
    allowed_max = max(allowed_products)

    definition_rows = [
        {
            "definition_id": "GDEF1211_0_live_object",
            "object": "G_res^nu",
            "definition": "local vector residual entering D_T K_T = G_res after the scalar/EH/Newton branch has removed everything it can remove",
            "formula": "G_res := P_loc(nabla Gamma_eff - D_T K_scalar) or the equivalent non-exact Ricci/source residual left by M[phi]",
            "source_anchor": "P8_Y5_R10_1193_VECTOR_TENSOR_COMPENSATOR_CONTRACT.csv::VTC1193_0_residual_source_split",
            "current_status": "DEFINED_NOT_SOURCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "definition_id": "GDEF1211_1_decomposition",
            "object": "G_res budget",
            "definition": "split G_res into independently auditable leftovers rather than treating it as a free parameter",
            "formula": "G_res = P_loc(G_scalar_exactness + G_source_side + G_parent_LHS + G_boundary_harmonic + G_profile_remainder)",
            "source_anchor": "1193/1194 scalar branch; 956 source-side spine; 1195 D_T range condition",
            "current_status": "DECOMPOSITION_DEFINED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "definition_id": "GDEF1211_2_norm",
            "object": "G_res_norm",
            "definition": "weighted norm of G_res in exactly the same local domain, coframe, gauge, and norm convention as the D_T and projector estimates",
            "formula": "G_res_norm := ||G_res||_{D_L,w,norm}",
            "source_anchor": "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md::IN1206_3_Gres_norm",
            "current_status": "NORM_REQUIREMENT_DEFINED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "definition_id": "GDEF1211_3_product_link",
            "object": "C_P*G_res_norm",
            "definition": "the clean Fermi projector branch scores only through the product C_P*G_res_norm",
            "formula": "C_P*G_res_norm <= allowed_CpGres_product from 1210 clean branch rows",
            "source_anchor": "P8_Y5_R10_1210_FERMI_BRACKET_GRID.csv::allowed_CpGres_product",
            "current_status": "PRODUCT_LINK_READY_CP_AND_GRES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zero_audit = [
        {
            "audit_id": "ZG1211_0_scalar_exact_zero",
            "component": "G_scalar_exactness",
            "zero_condition": "domain is Ricci-flat/Einstein with constant Lambda_E, scalar Helmholtz equation is solved with parent source and boundary/no-flux conditions",
            "missing_for_claim": "domain classifier; Lambda_E; Gamma_eff profile; Green inverse; boundary condition; parent scalar source",
            "current_status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZG1211_1_generic_matter_residual",
            "component": "G_scalar_exactness",
            "zero_condition": "generic Ricci matter term satisfies exactness/alignment theorem or its curl/Hodge residual is bounded below target",
            "missing_for_claim": "Ricci anisotropy norm; Hessian-gradient alignment; Hodge constant; boundary/harmonic control",
            "current_status": "GENERIC_ZERO_REJECTED_BOUND_ROUTE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZG1211_2_source_side_zero",
            "component": "G_source_side",
            "zero_condition": "ordinary source is exactly kappa_univ*T_total and DeltaJ_hidden=DeltaJ_species=0 in the same public metric/coframe",
            "missing_for_claim": "single-public-metric/source functor parent signature; hidden residual zero; species residual zero; measured-G calibration",
            "current_status": "CONDITIONAL_FROM_SOURCE_SPINE_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZG1211_3_parent_LHS_zero",
            "component": "G_parent_LHS",
            "zero_condition": "left-hand parent field equation reduces to Einstein/Newton operator in the selected local branch, with retained higher terms zero or bounded",
            "missing_for_claim": "EH/Newton left-hand limit; Bianchi/Ward compatibility; higher-operator residual bound",
            "current_status": "LEFT_HAND_GR_LIMIT_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZG1211_4_boundary_harmonic_zero",
            "component": "G_boundary_harmonic",
            "zero_condition": "boundary flux, harmonic representatives, and cokernel projection are killed or quotient-gauge in the same domain",
            "missing_for_claim": "boundary/no-flux certificate; harmonic-free domain; cokernel basis/projection; quotient-gauge proof",
            "current_status": "BOUNDARY_HARMONIC_ZERO_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ZG1211_5_total_Gres_zero",
            "component": "G_res_norm",
            "zero_condition": "all components ZG1211_0 through ZG1211_4 close in one common domain/norm",
            "missing_for_claim": "scalar/source/LHS/boundary conditions simultaneously signed",
            "current_status": "TOTAL_ZERO_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_rows = [
        {
            "bound_id": "GBD1211_0_absolute_budget",
            "quantity": "G_res_norm",
            "bound_formula": "||G_res|| <= ||P_loc||*(||G_scalar_exactness|| + ||G_source_side|| + ||G_parent_LHS|| + ||G_boundary_harmonic|| + ||G_profile_remainder||)",
            "derivation_basis": "triangle inequality applied to the 1211 decomposition; no signed cancellation allowed",
            "required_inputs": "P_loc_norm;component_norms;domain_id;norm_id;source_paths",
            "current_status": "BOUND_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "GBD1211_1_hodge_curl_route",
            "quantity": "G_scalar_exactness",
            "bound_formula": "||G_scalar_exactness|| <= C_Hodge*(||curl M[phi]|| + ||div_defect|| + ||boundary_trace|| + ||harmonic_part||)",
            "derivation_basis": "if only the Ricci-curl obstruction is accessible, a Hodge/Poincare estimate can convert curl/div/boundary control into a vector residual norm",
            "required_inputs": "C_Hodge;curl_M_phi_norm;div_defect_norm;boundary_trace_norm;harmonic_part_norm;domain_topology",
            "current_status": "BOUND_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "GBD1211_2_Einstein_classifier_defect",
            "quantity": "G_scalar_exactness",
            "bound_formula": "||G_scalar_exactness|| <= C_E*(epsilon_E*(||nabla phi||+||nabla^2 phi||) + ||d Lambda_E wedge d phi|| + boundary_phi)",
            "derivation_basis": "1193/1194 show scalar exactness closes in Einstein/Ricci-flat domains and fails by Ricci anisotropy or variable-Lambda wedge terms outside that branch",
            "required_inputs": "epsilon_E;C_E;nabla_phi_norm;hessian_phi_norm;dLambda_wedge_dphi_norm;boundary_phi",
            "current_status": "BOUND_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "GBD1211_3_source_side_residual",
            "quantity": "G_source_side",
            "bound_formula": "||G_source_side|| <= ||DeltaJ_hidden|| + ||DeltaJ_species|| + ||Delta_kappa_calibration||",
            "derivation_basis": "956 source-side spine says standard GR source is kappa_univ*T_total plus hidden/species residuals until parent source functor and measured-G chain close",
            "required_inputs": "DeltaJ_hidden_norm;DeltaJ_species_norm;Delta_kappa_norm;source_functor_path;measured_G_calibration_path",
            "current_status": "BOUND_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "GBD1211_4_parent_left_hand_residual",
            "quantity": "G_parent_LHS",
            "bound_formula": "||G_parent_LHS|| <= ||E_parent - E_EH/Newton|| + ||Bianchi_Ward_residual|| + ||higher_operator_tail||",
            "derivation_basis": "local GR requires both source side and left-hand field equation to reduce, not only matter coupling",
            "required_inputs": "parent_field_equation;EH_limit_residual_norm;Bianchi_Ward_residual_norm;higher_operator_tail_norm",
            "current_status": "BOUND_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "GBD1211_5_product_budget_for_1210",
            "quantity": "C_P*G_res_norm",
            "bound_formula": "C_P*G_res_norm <= C_P*Gres_bound and must be <= allowed_CpGres_product for each 1210 bracket row",
            "derivation_basis": "links the residual decomposition to the clean Fermi projector pressure map",
            "required_inputs": "C_P;Gres_bound;1210 bracket row;domain/norm compatibility",
            "current_status": "PRODUCT_BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_ready = [
        {
            "row_id": "SGR1211_0_direct_Gres_profile",
            "component": "G_res_profile",
            "definition": "direct grid/formula for G_res^nu(x) in the selected local domain",
            "required_columns": "domain_id;coframe;gauge;units;profile_grid_or_formula;norm_value;norm_type;source_path;equation_ref",
            "current_value": "MISSING",
            "current_status": "MISSING_DIRECT_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SGR1211_1_scalar_exactness_defect",
            "component": "G_scalar_exactness",
            "definition": "Ricci exactness / variable-Lambda / scalar branch defect after trying the Einstein/Ricci-flat branch",
            "required_columns": "domain_id;epsilon_E;Lambda_E;curl_M_phi_norm;dLambda_wedge_dphi_norm;C_Hodge;boundary_harmonic_norm;source_path",
            "current_value": "MISSING",
            "current_status": "MISSING_SCALAR_DEFECT_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SGR1211_2_source_side_residual",
            "component": "G_source_side",
            "definition": "hidden/species/source-normalization residual after standard kappa_univ*T_total source term is extracted",
            "required_columns": "DeltaJ_hidden_norm;DeltaJ_species_norm;Delta_kappa_norm;source_functor_path;measured_G_path;source_path",
            "current_value": "MISSING",
            "current_status": "MISSING_SOURCE_SIDE_RESIDUALS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SGR1211_3_parent_LHS_residual",
            "component": "G_parent_LHS",
            "definition": "left-hand field-equation residual after subtracting the Einstein/Newton operator in the local branch",
            "required_columns": "parent_equation_path;EH_limit_residual_norm;Newton_limit_residual_norm;Bianchi_Ward_residual_norm;higher_tail_norm;source_path",
            "current_value": "MISSING",
            "current_status": "MISSING_PARENT_LHS_LIMIT_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SGR1211_4_boundary_harmonic_residual",
            "component": "G_boundary_harmonic",
            "definition": "boundary, harmonic representative, and cokernel projection pieces not captured by the bulk profile",
            "required_columns": "boundary_trace_norm;harmonic_part_norm;cokernel_projection_norm;domain_topology;boundary_condition_source_path",
            "current_value": "MISSING",
            "current_status": "MISSING_BOUNDARY_HARMONIC_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SGR1211_5_CP_link",
            "component": "C_P",
            "definition": "same-norm operator constant needed to turn G_res_norm into projector pressure",
            "required_columns": "C_P;norm_id;domain_id;operator_estimate_path;D_T_adjoint_source_path;valid_for_claim",
            "current_value": "MISSING",
            "current_status": "MISSING_CP_OPERATOR_CONSTANT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    pressure_bridge = [
        {
            "bridge_id": "CPG1211_0_1210_range",
            "quantity": "allowed_CpGres_product",
            "formula": "S_allowed = target/(C_eff*L_D*Riemann_norm)",
            "value_or_range": f"[{fmt(allowed_min)}, {fmt(allowed_max)}]",
            "interpretation": "1210 clean branch can only be evaluated once C_P*G_res_norm has units/norm-compatible value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "CPG1211_1_if_CP_sourced",
            "quantity": "G_res_norm_allowed",
            "formula": "G_res_norm <= S_allowed/C_P",
            "value_or_range": "symbolic_until_C_P_sourced",
            "interpretation": "C_P source row turns the 1210 bracket into an allowed G_res_norm envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "CPG1211_2_if_Gres_sourced",
            "quantity": "C_P_allowed",
            "formula": "C_P <= S_allowed/G_res_norm",
            "value_or_range": "symbolic_until_G_res_norm_sourced",
            "interpretation": "G_res source row turns the 1210 bracket into an operator-constant target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "CPG1211_3_units_guard",
            "quantity": "claim policy",
            "formula": "valid_for_claim=false unless C_P and G_res_norm share the exact same D_L,w,norm convention as the projector bracket",
            "value_or_range": "guard_active",
            "interpretation": "large allowed-product values in 1210 are not evidence until units/norms are locked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1211_0_verdict",
            "condition": "Can G_res_norm be set to zero now?",
            "decision": "No. A zero theorem would require scalar exactness, source-side GR, parent left-hand EH/Newton reduction, and boundary/harmonic silence in one domain.",
            "result": "G_res_norm is decomposed into source-ready rows rather than left as a primitive missing number.",
            "next_action": "attack source-side/LHS residual zero, or fill the first direct G_res profile row.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1211_1_best_next",
            "condition": "What is the best next derivation target?",
            "decision": "Try the source-side plus parent-left-hand residual-zero route before numeric profiling, because proving G_res=0 would bypass C_P pressure entirely.",
            "result": "1212 should target source-side/EH-limit residual zero or build the first Gres_bound profile row if the proof fails.",
            "next_action": "1212 local residual zero/source-side EH limit or first profile row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1211_0_Gres_zero",
            "gate": "G_res_norm=0",
            "status": "BLOCKED",
            "reason": "all residual components are only conditional or missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1211_1_Gres_numeric",
            "gate": "numeric G_res_norm source row",
            "status": "BLOCKED",
            "reason": "no direct profile or component norm is sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1211_2_CP_Gres_product",
            "gate": "C_P*G_res_norm pressure product",
            "status": "BLOCKED",
            "reason": "both C_P and G_res_norm lack same-norm source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1211_3_local_GR_R10",
            "gate": "local-GR/R10 pass",
            "status": "BLOCKED",
            "reason": "1211 is a residual decomposition/source-pack checkpoint only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1211_0_1212",
            "target_file": "1212-Y5-R10-Gres-zero-source-side-EH-limit-or-first-profile-row.md",
            "target_script": "scripts/Y5_R10_Gres_zero_source_side_EH_limit_or_first_profile_row.py",
            "task": "attempt the G_res=0 theorem by closing source-side hidden/species residuals and the parent left-hand EH/Newton residual; if it fails, produce the first direct G_res_bound profile schema row",
            "success_condition": "G_res_norm is theorem-zero in one parent-owned local domain, or the first same-norm nonclaim Gres_bound row exists and feeds the 1210 C_P*G_res product map",
            "do_not_do": "do not call C_P*G_res bracket rows evidence; do not hide scalar/source/LHS/boundary residual components; do not edit formalization-workbench; do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    definition_fields = ["definition_id", "object", "definition", "formula", "source_anchor", "current_status", "valid_for_claim", "claim_allowed"]
    zero_fields = ["audit_id", "component", "zero_condition", "missing_for_claim", "current_status", "valid_for_claim", "claim_allowed"]
    bound_fields = ["bound_id", "quantity", "bound_formula", "derivation_basis", "required_inputs", "current_status", "valid_for_claim", "claim_allowed"]
    source_ready_fields = ["row_id", "component", "definition", "required_columns", "current_value", "current_status", "valid_for_claim", "claim_allowed"]
    bridge_fields = ["bridge_id", "quantity", "formula", "value_or_range", "interpretation", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(DEFINITION_PATH, definition_rows, definition_fields)
    write_csv(ZERO_AUDIT_PATH, zero_audit, zero_fields)
    write_csv(BOUND_PATH, bound_rows, bound_fields)
    write_csv(SOURCE_READY_PATH, source_ready, source_ready_fields)
    write_csv(PRESSURE_BRIDGE_PATH, pressure_bridge, bridge_fields)
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
        DEFINITION_PATH,
        ZERO_AUDIT_PATH,
        BOUND_PATH,
        SOURCE_READY_PATH,
        PRESSURE_BRIDGE_PATH,
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
    definition_present = any(row["definition_id"] == "GDEF1211_0_live_object" for row in definition_rows)
    decomposition_present = any(row["definition_id"] == "GDEF1211_1_decomposition" for row in definition_rows)
    total_zero_blocked = any(row["audit_id"] == "ZG1211_5_total_Gres_zero" and row["current_status"] == "TOTAL_ZERO_BLOCKED" for row in zero_audit)
    bound_components_present = {"G_scalar_exactness", "G_source_side", "G_parent_LHS", "G_boundary_harmonic"}.issubset({row["component"] for row in source_ready})
    pressure_bridge_present = any(row["bridge_id"] == "CPG1211_0_1210_range" for row in pressure_bridge)
    allowed_range_positive = allowed_min > 0 and allowed_max >= allowed_min
    target_preserved = abs(target - 1.17233215026e-05) < 1e-16
    no_missing_claim_rows = all(not (row["valid_for_claim"] and "MISSING" in row["current_value"]) for row in source_ready)
    no_claim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in definition_rows + zero_audit + bound_rows + source_ready + pressure_bridge + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1212 = next_rows[0]["target_file"].startswith("1212-")

    validation_rows = [
        validation_row("VAL1211_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1211_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1211_2_definition_present", "G_res live object is defined", definition_present, "GDEF1211_0 present"),
        validation_row("VAL1211_3_decomposition_present", "G_res decomposition is present", decomposition_present, "GDEF1211_1 present"),
        validation_row("VAL1211_4_total_zero_blocked", "G_res zero is not overclaimed", total_zero_blocked, "ZG1211_5 total zero blocked"),
        validation_row("VAL1211_5_component_rows", "source-ready component rows are staged", bound_components_present, ",".join(row["component"] for row in source_ready)),
        validation_row("VAL1211_6_pressure_bridge", "1210 C_P*G_res product bridge is staged", pressure_bridge_present and allowed_range_positive, f"allowed=[{fmt(allowed_min)}, {fmt(allowed_max)}]"),
        validation_row("VAL1211_7_target_preserved", "1210 projector target is preserved", target_preserved, f"target={fmt(target)}"),
        validation_row("VAL1211_8_no_missing_claim_rows", "no row with MISSING is valid for claim", no_missing_claim_rows, "all source-ready rows nonclaim"),
        validation_row("VAL1211_9_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1211_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1211_11_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1211_12_next_target", "next target is staged", next_1212, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1211_13_overall",
            "overall 1211 validation",
            validation_pass,
            "1211 G_res decomposition/source pack is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1211 Y5/R10 Gres Norm Source Or Local Residual Zero Theorem

**Current verdict:** 1211 does **not** prove `G_res_norm=0` and does **not** source a numeric `G_res_norm`. It does the needed cleanup: `G_res` is no longer a black-box missing number, but a sum of named residual debts.

**Main progress:** `G_res = P_loc(G_scalar_exactness + G_source_side + G_parent_LHS + G_boundary_harmonic + G_profile_remainder)`. A local-GR reduction needs these to vanish or be bounded in one common domain/coframe/norm. This connects the local projector route back to the GR/Newton spine rather than treating `G_res_norm` as a tunable knob.

**1210 pressure link:** clean Fermi rows allow `C_P*G_res_norm` in the range `{fmt(allowed_min)}` to `{fmt(allowed_max)}` across the private bracket grid, but that is not evidence until `C_P`, units, and the `G_res` norm are sourced.

## Source Register

{markdown_table(source_rows, source_fields)}

## G_res Definition And Decomposition

{markdown_table(definition_rows, definition_fields)}

## G_res Zero Theorem Audit

{markdown_table(zero_audit, zero_fields)}

## G_res Bound Decomposition

{markdown_table(bound_rows, bound_fields)}

## Source-Ready G_res Rows

{markdown_table(source_ready, source_ready_fields)}

## C_P G_res Pressure Bridge

{markdown_table(pressure_bridge, bridge_fields)}

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
    print(f"target={fmt(target)}")
    print(f"allowed_CpGres_min={fmt(allowed_min)}")
    print(f"allowed_CpGres_max={fmt(allowed_max)}")
    print("G_res_zero_claimed=false")


if __name__ == "__main__":
    main()
