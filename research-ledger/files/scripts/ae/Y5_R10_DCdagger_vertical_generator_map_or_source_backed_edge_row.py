from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "727-Y5-R10-DCdagger-vertical-generator-map-or-source-backed-edge-row.md"
NEXT_TARGET = "728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "726_doc": {
        "path": POST_CHECKPOINT / "726-Y5-R10-Vdef-parent-owner-map-or-edge-coefficient-source-contract.md",
        "note": "immediate handoff: DCdagger map or source-backed edge row",
        "needles": ["727-Y5-R10-DCdagger-vertical-generator-map-or-source-backed-edge-row.md", "DCdagger-to-vertical-generator map", "lambda_um=608.0783"],
    },
    "726_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_726_VALIDATION.csv",
        "note": "prior validation gate",
        "needles": ["V726_9_next_target_selected", "pass", "V726_12_formalization_workbench_untouched"],
    },
    "726_parent_owner_map": {
        "path": RESIDUALS / "P8_Y5_R10_726_PARENT_OWNER_MAP.csv",
        "note": "current parent owner requirements",
        "needles": ["POM726_6_DCdagger_map", "not_mapped", "POM726_9_matter_quotient"],
    },
    "726_edge_contract": {
        "path": RESIDUALS / "P8_Y5_R10_726_EDGE_COEFFICIENT_SOURCE_CONTRACT.csv",
        "note": "current edge coefficient source contract",
        "needles": ["ECSC726_1_K_edge", "ECSC726_2_Qbar_edge_XH", "ECSC726_3_qbar_XT"],
    },
    "726_edge_template": {
        "path": RESIDUALS / "P8_Y5_R10_726_SOURCE_BACKED_EDGE_ROW_TEMPLATE.csv",
        "note": "current source-backed edge row template",
        "needles": ["SBER726_0_required_source_backed_row", "608.0783", "MISSING_SOURCE_BACKED_K_EDGE"],
    },
    "590_doc": {
        "path": POST_CHECKPOINT / "590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md",
        "note": "older precise map theorem",
        "needles": ["symplectic covector", "v_X=Omega_Y^-1[(DC_X)^dagger X]", "parent `theta/Omega`"],
    },
    "590_map": {
        "path": RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
        "note": "older DCdagger=Omega-flat map rows",
        "needles": ["DVM590_3_precise_map", "(DC_X)^dagger X = Omega_Y^flat(v_X[Y])", "conditional_map_theorem"],
    },
    "590_gr": {
        "path": RESIDUALS / "P8_Y5_R10_590_GR_ANALOGUE_CHECK.csv",
        "note": "GR analogy for momentum/diffeomorphism constraints",
        "needles": ["GRA590_0_ADM_momentum_constraint", "GRA590_1_covariant_phase_space", "false"],
    },
    "590_field_map": {
        "path": RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
        "note": "field-by-field vertical action targets",
        "needles": ["metric_or_coframe", "Gamma_Khat_qloc_sector", "boundary_edge"],
    },
    "590_closure": {
        "path": RESIDUALS / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv",
        "note": "closure gates for the precise map",
        "needles": ["MCG590_0_parent_Omega", "MCG590_6_matter_quotient", "true"],
    },
    "590_edge_status": {
        "path": RESIDUALS / "P8_Y5_R10_590_EDGE_ROW_SOURCE_STATUS.csv",
        "note": "older edge row source status",
        "needles": ["SBE589_0_required_source_backed_row", "missing_sources", "false"],
    },
    "589_doc": {
        "path": POST_CHECKPOINT / "589-Y5-R10-adjoint-zero-mode-certificate-or-source-backed-edge-product-row.md",
        "note": "older adjoint zero-mode certificate skeleton",
        "needles": ["DCdagger", "vertical generator", "source-backed edge-product row"],
    },
    "591_doc": {
        "path": POST_CHECKPOINT / "591-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md",
        "note": "older next target: parent Omega and DC operator fill",
        "needles": ["formal DC_X and DCdagger formulas", "P/J/Omega ownership", "Edge-source rows are still missing"],
    },
    "591_omega": {
        "path": RESIDUALS / "P8_Y5_R10_591_PARENT_OMEGA_CANDIDATE.csv",
        "note": "parent Omega candidate rows",
        "needles": ["OM591_0_covariant_variation_definition", "formal_definition_only", "false"],
    },
    "591_dc": {
        "path": RESIDUALS / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
        "note": "formal DC operator formula rows",
        "needles": ["DC591_1_linearization_tensor_convention", "formal_operator_formula", "DC591_2_densitized_variant"],
    },
    "591_dcadjoint": {
        "path": RESIDUALS / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv",
        "note": "formal DCdagger formula rows",
        "needles": ["DCA591_1_PJ_adjoint", "operator_shape_derived", "DCA591_4_compare_to_Omega_flat"],
    },
    "583_doc": {
        "path": POST_CHECKPOINT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md",
        "note": "momentum-map owner contract",
        "needles": ["i_{v_epsilon} Omega_Y = delta G[epsilon]", "Q_boundary[epsilon]=0", "P[Y], J_eff[Y]"],
    },
    "581_doc": {
        "path": POST_CHECKPOINT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "note": "quotient vertical theorem shape",
        "needles": ["v_X in ker(d pi)", "Q_X[epsilon]=0", "pi_X ~= 0"],
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def csv_contains(path: Path, *needles: str) -> bool:
    return text_contains(path, list(needles))


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def all_valid_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def make_source_register() -> list[dict[str, object]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    source_register = make_source_register()
    edge_template_726 = read_csv(SOURCES["726_edge_template"]["path"])

    dcdagger_vertical_map = [
        {
            "map_id": "DVM727_0_generator_functional",
            "statement": "G_X[X;Y]=int_Sigma X_nu C_X^nu[Y]+Q_X[X;Y]",
            "meaning": "the multiplier constraint must be the bulk density of a differentiable Hamiltonian generator",
            "map_result": "definition_contract",
            "current_MTS_status": "G_X_template_exists_but_Q_and_domain_not_derived",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_doc", "590_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "DVM727_1_variation_as_DCadjoint",
            "statement": "delta G_X[delta Y]=int_Sigma X_nu DC_X^nu[delta Y]+delta Q_X=<((DC_X)^dagger X),delta Y>+boundary_fixed",
            "meaning": "DCdagger X is a covector on parent field space",
            "map_result": "formal_adjoint_side",
            "current_MTS_status": "requires explicit DC, pairing, and boundary cancellation",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_map", "591_dcadjoint"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "DVM727_2_momentum_map_identity",
            "statement": "delta G_X[delta Y]=Omega_Y(delta Y,v_X[Y])",
            "meaning": "the same variation is the symplectic pairing with the vertical generator",
            "map_result": "momentum_map_side",
            "current_MTS_status": "requires parent theta_Y/Omega_Y and vertical action v_X",
            "valid_for_claim": "false",
            "source_paths": source_path_string("583_doc", "590_map", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "DVM727_3_precise_map",
            "statement": "(DC_X)^dagger X = Omega_Y^flat(v_X[Y])",
            "meaning": "DCdagger is the symplectic covector dual of the vertical generator; it is not literally the vector generator",
            "map_result": "conditional_map_theorem",
            "current_MTS_status": "mathematically_clean_but_parent_Omega_missing",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_doc", "590_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "DVM727_4_raise_index",
            "statement": "v_X[Y]=Omega_Y^{-1}[(DC_X)^dagger X] on the reduced nondegenerate phase space",
            "meaning": "the actual generator appears only after the parent symplectic form is known and inverted on the quotient",
            "map_result": "actual_generator_after_Omega_inverse",
            "current_MTS_status": "not_available_until_reduced_Omega_is_explicit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_doc", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "map_id": "DVM727_5_zero_mode_implication",
            "statement": "(DC_X)^dagger X=0 => Omega_Y(delta Y,v_X)=0 for all delta Y => v_X=0 modulo known degeneracies",
            "meaning": "the adjoint zero-mode certificate reduces to no proper vertical stabilizers only after Omega is reduced and nondegenerate",
            "map_result": "conditional_kernel_kill",
            "current_MTS_status": "needs nondegenerate reduced Omega and proper-boundary domain",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_map", "581_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    category_repair_note = [
        {
            "repair_id": "CRN727_0_old_shorthand",
            "old_wording": "DCdagger maps to the vertical generator",
            "corrected_wording": "DCdagger maps to Omega-flat of the vertical generator",
            "why_it_matters": "DCdagger is a field-space covector; v_X is a field-space vector",
            "claim_effect": "prevents a category error in the no-pole proof",
            "valid_for_claim": "false",
            "source_paths": source_path_string("589_doc", "590_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "repair_id": "CRN727_1_current_required_map",
            "old_wording": "prove DCdagger=v_X",
            "corrected_wording": "prove (DC_X)^dagger X=Omega_Y^flat(v_X[Y]) and then invert reduced Omega_Y",
            "why_it_matters": "without Omega, the adjoint can be changed by choosing a pairing",
            "claim_effect": "parent theta/Omega is now mandatory, not cosmetic",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_map", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    gr_analogue_check = [
        {
            "analogue_id": "GRA727_0_ADM_momentum_constraint",
            "object": "ADM momentum/diffeomorphism constraint",
            "canonical_form": "C_i=-2 h_{ij}D_k pi^{jk}+C_i^matter",
            "generator_variation": "G[xi]=int pi^{ij} L_xi h_{ij}+p_A L_xi Phi^A+boundary",
            "map_lesson": "functional derivatives of G give the diffeomorphism vector field on phase space",
            "MTS_transfer_status": "template_only_not_MTS_proof",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_gr"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "analogue_id": "GRA727_1_covariant_phase_space",
            "object": "covariant Hamiltonian charge",
            "canonical_form": "delta H_xi=Omega(delta phi,L_xi phi)",
            "generator_variation": "H_xi=int_S Q_xi-i_xi B plus constraints",
            "map_lesson": "differentiable charge variation is Omega-flat of the diffeomorphism generator",
            "MTS_transfer_status": "conditional_if_parent_theta_Q_exist",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_gr", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "analogue_id": "GRA727_2_current_MTS_CX",
            "object": "MTS C_X=-nabla_mu P^{mu nu}+J_eff^nu",
            "canonical_form": "candidate momentum-map density",
            "generator_variation": "G_X=int X_nu C_X^nu+Q_X",
            "map_lesson": "MTS matches the GR style only if P,J_eff,Q_X,theta,Omega are from one parent action",
            "MTS_transfer_status": "not_derived_P_J_theta_Omega_missing",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_gr", "726_parent_owner_map"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    field_by_field_vertical_action_map = [
        {
            "field_block": "metric_or_coframe",
            "candidate_vertical_action": "v_X[g]=L_X g or v_X[e]=L_X e plus local Lorentz compensation",
            "DCdagger_target": "metric/coframe component of Omega_Y^flat(v_X)",
            "status": "standard_candidate_not_parent_declared",
            "missing_input": "observed coframe/metric as parent field and symplectic potential",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_field_map", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "field_block": "canonical_momenta_or_boundary_charge",
            "candidate_vertical_action": "v_X[pi]=L_X pi plus density/boundary improvements",
            "DCdagger_target": "momentum component of Omega_Y^flat(v_X)",
            "status": "not_written_for_MTS",
            "missing_input": "canonical variables or covariant charge split",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_field_map", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "field_block": "Gamma_Khat_qloc_sector",
            "candidate_vertical_action": "v_X[T_GK]=L_X T_GK if T_GK is parent stress",
            "DCdagger_target": "Euler-Ward stress-divergence covector",
            "status": "conditional_from_513_not_integrated_with_CX",
            "missing_input": "S_GK and Helmholtz/integrability proof",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_field_map", "726_parent_owner_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "field_block": "domain_memory_projector_fields",
            "candidate_vertical_action": "v_X[Phi^A]=L_X Phi^A or quotient-vertical action",
            "DCdagger_target": "extra-sector components of Omega_Y^flat(v_X)",
            "status": "unmapped",
            "missing_input": "field transformation law for chi_D,Qcoh,memory,Pi_M/boundary variables",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_field_map", "726_parent_owner_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "field_block": "matter_readout",
            "candidate_vertical_action": "v_X matter=0 after quotient; v_X hat_g(q(Y))=0",
            "DCdagger_target": "no matter component in proper vertical generator",
            "status": "not_derived",
            "missing_input": "matter quotient functor and no-marker theorem",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_field_map", "726_parent_owner_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "field_block": "boundary_edge",
            "candidate_vertical_action": "proper X has zero boundary charge or exact primitive",
            "DCdagger_target": "no boundary covector remains after delta Q_X",
            "status": "not_derived",
            "missing_input": "Q_X differentiability, B_X exactness, Pi_M^H edge projection zero",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_field_map", "726_edge_contract"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    mapping_closure_gate = [
        {
            "gate_id": "MCG727_0_parent_Omega",
            "required_to_close": "explicit theta_Y and Omega_Y for parent variables",
            "current_status": "missing",
            "if_missing": "DCdagger remains an undefined covector up to arbitrary pairing",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_closure", "591_omega", "726_parent_owner_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "MCG727_1_DCX_operator",
            "required_to_close": "linearized DC_X from C_X=-nabla P+J_eff",
            "current_status": "formal_shape_only",
            "if_missing": "cannot compare DCdagger with Omega-flat vertical action",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_closure", "591_dc", "591_dcadjoint"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "MCG727_2_vertical_generator",
            "required_to_close": "v_X on every parent and boundary field",
            "current_status": "missing",
            "if_missing": "no actual generator to map to",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_closure", "581_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "MCG727_3_differentiable_boundary",
            "required_to_close": "Q_X cancels boundary variation and is zero/proper/exact on local branch",
            "current_status": "missing",
            "if_missing": "edge charge survives and no-pole fails",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_closure", "726_edge_contract"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "MCG727_4_reduced_nondegeneracy",
            "required_to_close": "Omega is nondegenerate after quotienting ordinary gauge degeneracies",
            "current_status": "not_checked",
            "if_missing": "DCdagger=0 may imply only a symplectic degeneracy, not X=0",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_closure", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "MCG727_5_no_proper_stabilizer",
            "required_to_close": "proper v_X[Y0]=0 implies X=0",
            "current_status": "not_proved",
            "if_missing": "adjoint zero modes can remain",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_closure", "581_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "MCG727_6_matter_quotient",
            "required_to_close": "ordinary matter sees only quotient variables",
            "current_status": "missing",
            "if_missing": "qbar_XT stays finite or must be bounded",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_closure", "726_parent_owner_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "MCG727_7_edge_sources",
            "required_to_close": "lambda_edge,K_edge,Qbar_edge_XH,qbar_XT,bound curve are source-backed if theorem route fails",
            "current_status": "missing",
            "if_missing": "fallback edge branch remains runner-smoke only",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "source_paths": source_path_string("726_edge_contract", "726_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    edge_row_source_status = [
        {
            "edge_row_id": row["row_id"],
            "lambda_um": row["lambda_um"],
            "alpha_edge_ceiling": row["alpha_edge_ceiling"],
            "alpha_edge_predicted": row["alpha_edge_predicted"],
            "source_status": "missing_sources" if "MISSING" in row["K_edge"] else "diagnostic_budget_or_smoke_not_source_backed",
            "required_next": row["source_required"],
            "valid_for_claim": "false",
            "source_paths": str(SOURCES["726_edge_template"]["path"]),
            "generated_utc": GENERATED_UTC,
        }
        for row in edge_template_726
    ]

    decision_matrix = [
        {
            "decision_id": "D727_0_precise_map_carried_forward",
            "decision": "DCdagger maps to Omega-flat of the vertical generator",
            "meaning": "the actual generator is v_X=Omega^{-1}(DCdagger X) only after parent Omega is supplied",
            "claim_status": "conditional_map_not_MTS_proof",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_doc", "590_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D727_1_category_error_prevented",
            "decision": "do not say DCdagger literally equals v_X",
            "meaning": "this avoids mixing field-space covectors and vectors",
            "claim_status": "rigour_improvement",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_doc", "591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D727_2_current_MTS_not_closed",
            "decision": "actual MTS map still lacks Omega, DC, v_X, boundary differentiability, and matter quotient",
            "meaning": "no no-pole/R10/local-GR promotion",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("726_parent_owner_map", "590_closure"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D727_3_edge_row_still_source_blocked",
            "decision": "source-backed edge row remains unfilled",
            "meaning": "fallback still needs K_edge, Qbar_edge_XH, qbar_XT, lambda support, and bound provenance",
            "claim_status": "fallback_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("726_edge_contract", "726_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    route_update = [
        {
            "route_id": "RU727_0_allowed",
            "allowed_after_727": "use DCdagger=Omega_flat(v_X) as the exact map theorem",
            "forbidden_after_727": "state DCdagger literally equals v_X without specifying the pairing/symplectic inverse",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("590_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "route_id": "RU727_1_allowed",
            "allowed_after_727": "try to fill parent theta/Omega and DC_X operator",
            "forbidden_after_727": "promote no-pole from the GR analogue alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_doc", "591_dc", "591_dcadjoint"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "route_id": "RU727_2_allowed",
            "allowed_after_727": "if Omega/DC cannot be filled, fill source-backed edge coefficients",
            "forbidden_after_727": "mark diagnostic edge rows valid_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("726_edge_contract", "726_edge_template"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_727_DCdagger_Omega_flat_vertical_map_written_edge_row_source_still_blocked_nonclaim",
            "claim_ceiling": "conditional_DCdagger_equals_Omega_flat_vX_map_only_no_R10_WEP_PPN_Newton_or_local_GR_pass",
            "main_result": "DCdagger is correctly categorized as Omega-flat of the vertical generator, not the generator itself",
            "hard_blocker": "parent Omega, explicit DC_X, vertical action on all fields, boundary differentiability, reduced nondegeneracy, no proper stabilizer, and matter quotient remain unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("726_doc", "590_doc", "591_doc"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_727_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "dcdagger_vertical_map": (
            RESIDUALS / "P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv",
            dcdagger_vertical_map,
            ["map_id", "statement", "meaning", "map_result", "current_MTS_status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "category_repair_note": (
            RESIDUALS / "P8_Y5_R10_727_CATEGORY_REPAIR_NOTE.csv",
            category_repair_note,
            ["repair_id", "old_wording", "corrected_wording", "why_it_matters", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "gr_analogue_check": (
            RESIDUALS / "P8_Y5_R10_727_GR_ANALOGUE_CHECK.csv",
            gr_analogue_check,
            ["analogue_id", "object", "canonical_form", "generator_variation", "map_lesson", "MTS_transfer_status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "field_by_field_vertical_action_map": (
            RESIDUALS / "P8_Y5_R10_727_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
            field_by_field_vertical_action_map,
            ["field_block", "candidate_vertical_action", "DCdagger_target", "status", "missing_input", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "mapping_closure_gate": (
            RESIDUALS / "P8_Y5_R10_727_MAPPING_CLOSURE_GATE.csv",
            mapping_closure_gate,
            ["gate_id", "required_to_close", "current_status", "if_missing", "claim_blocked", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "edge_row_source_status": (
            RESIDUALS / "P8_Y5_R10_727_EDGE_ROW_SOURCE_STATUS.csv",
            edge_row_source_status,
            ["edge_row_id", "lambda_um", "alpha_edge_ceiling", "alpha_edge_predicted", "source_status", "required_next", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "decision_matrix": (
            RESIDUALS / "P8_Y5_R10_727_DECISION_MATRIX.csv",
            decision_matrix,
            ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "route_update": (
            RESIDUALS / "P8_Y5_R10_727_ROUTE_UPDATE.csv",
            route_update,
            ["route_id", "allowed_after_727", "forbidden_after_727", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_727_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
    }

    for path, rows, fields in outputs.values():
        write_csv(path, rows, fields)

    generated_paths = [path for path, _, _ in outputs.values()]
    formalization_count = formalization_changed_after_cutoff()
    validations = [
        {
            "check_id": "V727_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V727_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V727_2_prior_726_clean",
            "result": "pass" if prior_validation_clean(SOURCES["726_validation"]["path"]) else "fail",
            "detail": "726 validation has no failures",
        },
        {
            "check_id": "V727_3_726_selected_727",
            "result": "pass" if csv_contains(SOURCES["726_doc"]["path"], "727-Y5-R10-DCdagger-vertical-generator-map-or-source-backed-edge-row.md") else "fail",
            "detail": "726 selected this checkpoint",
        },
        {
            "check_id": "V727_4_precise_map_written",
            "result": "pass"
            if any(row["statement"] == "(DC_X)^dagger X = Omega_Y^flat(v_X[Y])" for row in dcdagger_vertical_map)
            and any("Omega_Y^{-1}" in row["statement"] for row in dcdagger_vertical_map)
            else "fail",
            "detail": "requires DCdagger=Omega_flat(vX) and vX=Omega_inverse(DCdaggerX)",
        },
        {
            "check_id": "V727_5_category_repair_explicit",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in category_repair_note) and any("covector" in row["why_it_matters"] for row in category_repair_note) else "fail",
            "detail": "DCdagger-vX category distinction preserved",
        },
        {
            "check_id": "V727_6_GR_analogue_nonclaim",
            "result": "pass" if len(gr_analogue_check) == 3 and all(row["valid_for_claim"] == "false" for row in gr_analogue_check) else "fail",
            "detail": f"gr_rows={len(gr_analogue_check)}",
        },
        {
            "check_id": "V727_7_field_action_map_nonclaim",
            "result": "pass" if len(field_by_field_vertical_action_map) >= 6 and all(row["valid_for_claim"] == "false" for row in field_by_field_vertical_action_map) else "fail",
            "detail": f"field_rows={len(field_by_field_vertical_action_map)}",
        },
        {
            "check_id": "V727_8_closure_gates_block_claim",
            "result": "pass" if all(row["claim_blocked"] == "true" and row["valid_for_claim"] == "false" for row in mapping_closure_gate) else "fail",
            "detail": f"gate_rows={len(mapping_closure_gate)};all_block=True",
        },
        {
            "check_id": "V727_9_edge_rows_still_nonclaim",
            "result": "pass"
            if len(edge_row_source_status) == 3
            and all(row["valid_for_claim"] == "false" for row in edge_row_source_status)
            and any(row["lambda_um"] == "608.0783" and row["alpha_edge_ceiling"] == "0.00234471960478" for row in edge_row_source_status)
            else "fail",
            "detail": f"edge_rows={len(edge_row_source_status)}",
        },
        {
            "check_id": "V727_10_old_590_591_integrated",
            "result": "pass"
            if csv_contains(SOURCES["590_map"]["path"], "DVM590_3_precise_map")
            and csv_contains(SOURCES["591_dc"]["path"], "DC591_1_linearization_tensor_convention")
            else "fail",
            "detail": "old map and next Omega/DC target integrated",
        },
        {
            "check_id": "V727_11_next_target_selected",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in decision_matrix) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V727_12_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V727_13_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V727_14_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V727_15_no_local_arena_claim",
            "result": "pass" if "no_R10_WEP_PPN_Newton_or_local_GR_pass" in nonclaim_summary[0]["claim_ceiling"] else "fail",
            "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked",
        },
        {
            "check_id": "V727_16_source_register_written",
            "result": "pass" if len(source_register) >= 16 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V727_17_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_727_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 727 - Y5 R10 DCdagger Vertical Generator Map Or Source-Backed Edge Row

## Summary

This checkpoint repairs the operator language:

`(DC_X)^dagger X` is not literally the vertical generator. It is the **symplectic covector** of the vertical generator:

```text
(DC_X)^dagger X = Omega_Y^flat(v_X[Y])
v_X[Y] = Omega_Y^{{-1}}[(DC_X)^dagger X]
```

Current verdict: **conditional map only**. The category problem is fixed, but current MTS still lacks parent `theta/Omega`, explicit `DC_X`, field-by-field `v_X`, differentiable boundary charge, reduced nondegenerate phase space, no proper stabilizer proof, and matter quotient.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | private/nonclaim checkpoint |
| Next target | `{NEXT_TARGET}` |

## DCdagger Vertical Map

{markdown_table(dcdagger_vertical_map, ["map_id", "statement", "map_result", "current_MTS_status", "valid_for_claim"])}

## Category Repair Note

{markdown_table(category_repair_note, ["repair_id", "old_wording", "corrected_wording", "why_it_matters", "valid_for_claim"])}

## GR Analogue Check

{markdown_table(gr_analogue_check, ["analogue_id", "object", "map_lesson", "MTS_transfer_status", "valid_for_claim"])}

## Field-By-Field Vertical Action Map

{markdown_table(field_by_field_vertical_action_map, ["field_block", "candidate_vertical_action", "DCdagger_target", "status", "missing_input", "valid_for_claim"])}

## Mapping Closure Gate

{markdown_table(mapping_closure_gate, ["gate_id", "required_to_close", "current_status", "if_missing", "claim_blocked", "valid_for_claim"])}

## Edge Row Source Status

{markdown_table(edge_row_source_status, ["edge_row_id", "lambda_um", "alpha_edge_ceiling", "alpha_edge_predicted", "source_status", "required_next", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_matrix, ["decision_id", "decision", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_update, ["route_id", "allowed_after_727", "forbidden_after_727", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Practical Read

This is a real tightening. The theorem route is still alive, but now it has the right mathematical type: constraint variation covector to symplectic-dual generator. Closing it requires `Omega_Y` and `DC_X`, not just confidence. If those do not materialize, the edge row remains the honest fallback and still needs sourced coefficients.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
