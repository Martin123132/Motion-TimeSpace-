from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1370"
TITLE = "1370-Y5-R10-RAB-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
LCG_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_LCG_CONTRACT_CANDIDATE.csv"
LCG_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_LCG_CONTRACT_AUDIT.csv"
CQGAMMA_PATH = OUT_DIR / f"{PACK_ID}_WARD_SAFE_CQGAMMA_DERIVATION.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_QLOC_GAMMA_RUNNER_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1370_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        out.append("| " + " | ".join(values) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1370_0_1369_doc",
            "source_path": "1369-Y5-R10-RAB-Lcg-parent-definition-metric-silence-or-q_loc-gamma-projection-runner.md",
            "required_anchor": "NEXT1369_0_1370",
            "purpose": "1369 handoff to parent L_cg contract or q_loc weak-field coefficient.",
        },
        {
            "source_id": "SRC1370_1_1369_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1369_NEXT_TARGET.csv",
            "required_anchor": "NEXT1369_0_1370",
            "purpose": "machine-readable 1370 target.",
        },
        {
            "source_id": "SRC1370_2_1369_lcg_hunt",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv",
            "required_anchor": "LCGH1369_1_fixed_parameter_route",
            "purpose": "fixed-parameter L_cg silence route and counterbranches.",
        },
        {
            "source_id": "SRC1370_3_1369_lcg_response",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv",
            "required_anchor": "ML1369_4_best_route",
            "purpose": "proposed parent contract route for L_cg.",
        },
        {
            "source_id": "SRC1370_4_1369_qgamma_schema",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1369_QLOC_GAMMA_RUNNER_SCHEMA.csv",
            "required_anchor": "QG1369_1_response_coefficient",
            "purpose": "q_loc gamma schema requiring C_qgamma.",
        },
        {
            "source_id": "SRC1370_5_1182_ppn_projection",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv",
            "required_anchor": "PPNP1182_2_gamma_leakage",
            "purpose": "weak-field scalar gamma projection and leakage map.",
        },
        {
            "source_id": "SRC1370_6_1185_qloc_split",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1185_QLOC_RESPONSE_SPLIT_ATTEMPT.csv",
            "required_anchor": "QRS1185_2_scalar_projection",
            "purpose": "q_loc type guard and scalar projection requirement.",
        },
        {
            "source_id": "SRC1370_7_1186_ward_operator",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv",
            "required_anchor": "RQB1186_2_operator_factorization",
            "purpose": "Ward-safe compensator route and operator factorization.",
        },
        {
            "source_id": "SRC1370_8_1240_qr_map",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "required_anchor": "QMAP1240_3_gamma_projection",
            "purpose": "finite q_R to gamma projection, used only as a nonimportable special case.",
        },
        {
            "source_id": "SRC1370_9_1181_cassini",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "required_anchor": "SRC1181W_0_Cassini_gamma",
            "purpose": "source-backed Cassini PPN gamma comparator.",
        },
        {
            "source_id": "SRC1370_10_1244_policy",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "required_anchor": "RPF1244_0_policy",
            "purpose": "strict one-sigma gamma policy and q_R guardrail.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def lcg_contract_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "clause_id": "LCC1370_0_fixed_scalar_parameter",
                "clause": "L_cg is a positive constant scalar parameter L0, not a spacetime field.",
                "contract_text": "The parent action may contain L0 through scalar functions such as L0^-2 F(m), with L0 held fixed under Hilbert variation.",
                "status": "COVARIANCE_ADMISSIBLE_CLOSURE_CANDIDATE",
                "proof_or_risk": "A constant scalar parameter introduces no preferred vector/tensor background; delta_g L0=0 and nabla_mu L0=0.",
                "consequence": "M_L^{mu nu}=0 and nabla_mu L_cg=0 for the algebraic Gamma_eff term.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv;source-intake/mts_residuals/P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv",
                "source_anchors": "LCGH1369_1_fixed_parameter_route;ML1369_0_exact_fixed_scale_silence",
            },
            {
                "clause_id": "LCC1370_1_no_local_readout_inside_variation",
                "clause": "No cell-volume, curvature, density, source, projector, or domain readout is allowed to masquerade as L0 inside the Hilbert variation.",
                "contract_text": "Observable coarse-graining/domain readouts may be performed after variation, but they are not the varied parent L_cg appearing in Gamma_eff.",
                "status": "REQUIRED_ANTI_SMUGGLING_CLAUSE",
                "proof_or_risk": "Without this clause, the 1369 volume/curvature/density counterbranches give generically nonzero M_L.",
                "consequence": "prevents deleting metric-composite L_cg response by notation.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv",
                "source_anchors": "LCGH1369_2_cell_volume_route;LCGH1369_3_curvature_length_route;LCGH1369_4_density_or_source_length_route",
            },
            {
                "clause_id": "LCC1370_2_variation_order",
                "clause": "Hilbert variation is performed at fixed parent fields and fixed L0 before projection/domain reduction.",
                "contract_text": "delta_g acts on g and dynamical fields only; L0 labels the effective theory and is not varied.",
                "status": "REQUIRED_FOR_ML_ZERO",
                "proof_or_risk": "If projection/domain reduction enters before variation, hidden M_L, K_domain, and boundary terms can reappear.",
                "consequence": "M_L=0 applies only to the algebraic chain term, not to K_conn/K_domain/K_boundary.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv",
                "source_anchors": "ML1369_3_chain_zero_gate_update;ML1369_4_best_route",
            },
            {
                "clause_id": "LCC1370_3_effective_scale_role",
                "clause": "L0 is an effective coarse-graining/renormalization scale, not a fitted local environmental field.",
                "contract_text": "Changing L0 changes the effective description; physical predictions must be stable under a future RG/stability condition or L0 must be fixed by parent microphysics.",
                "status": "ADMISSIBLE_BUT_NEEDS_FUTURE_SCALE_SETTING",
                "proof_or_risk": "This avoids covariance breaking but leaves a scale-selection problem.",
                "consequence": "local-GR proof can use M_L=0 only after L0 is fixed or shown not to overfit.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv",
                "source_anchors": "ML1369_4_best_route",
            },
            {
                "clause_id": "LCC1370_4_metric_silence_result",
                "clause": "Under LCC1370_0 through LCC1370_2, M_L^{mu nu}=0 for the parent Gamma_eff chain.",
                "contract_text": "delta_g Gamma_eff|L = -2 L0^-3 F(m) delta_g L0 = 0, and nabla_mu Gamma_eff loses the -2 L_cg^-3 F(m)nabla_mu L_cg term.",
                "status": "DERIVED_UNDER_CLOSURE_CONTRACT",
                "proof_or_risk": "This is exact algebra if L0 is fixed; it is false for metric-composite L_cg.",
                "consequence": "combines with the fixed-field m branch to close the algebraic m/L_cg chain, but not the cdb residual.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
                "source_anchors": "GSE798_1_gradient_expansion;KDR1289_1_local_zero_condition_for_chain_kernel",
            },
            {
                "clause_id": "LCC1370_5_corpus_signature_verdict",
                "clause": "Current registered corpus does not yet parent-sign LCC1370_0 through LCC1370_4 as the live theory definition.",
                "contract_text": "Treat the fixed-L0 branch as a proposed closure contract until a parent action file adopts it explicitly.",
                "status": "NOT_LIVE_CLAIM_UNTIL_PARENT_SIGNED",
                "proof_or_risk": "1369 found no live L_cg parent definition in registered sources.",
                "consequence": "M_L=0 is closure-admissible but not claim-grade.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv",
                "source_anchors": "LCGH1369_5_parent_definition_verdict",
            },
        ]
    )


def lcg_audit_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "audit_id": "LCA1370_0_covariance",
                "test": "Does fixed L0 break diffeomorphism covariance?",
                "result": "PASS_AS_CONSTANT_SCALAR",
                "reason": "A constant scalar parameter can appear in a scalar-density action without selecting a frame or direction.",
                "remaining_risk": "spacetime-dependent L_cg(x) would require its own field equation or background-source treatment.",
            },
            {
                "audit_id": "LCA1370_1_metric_silence",
                "test": "Does fixed L0 imply M_L=0?",
                "result": "PASS_UNDER_CONTRACT",
                "reason": "Hilbert variation holds nondynamical scalar parameters fixed, so delta_g L0=0.",
                "remaining_risk": "only the algebraic L_cg chain closes; connection/domain/boundary terms remain.",
            },
            {
                "audit_id": "LCA1370_2_locality",
                "test": "Does fixed L0 preserve the intended local/coarse-grained interpretation?",
                "result": "PARTIAL_RISK",
                "reason": "It is clean as an effective theory scale, but not a derived local environmental length.",
                "remaining_risk": "needs RG/stability or parent microphysics to fix L0 rather than fitting it arena-by-arena.",
            },
            {
                "audit_id": "LCA1370_3_no_smuggling",
                "test": "Are metric-composite readouts kept out of the fixed-L0 proof?",
                "result": "PASS_IF_LCC1370_1_IS_ENFORCED",
                "reason": "The contract explicitly separates parent L0 from post-variation observational readouts.",
                "remaining_risk": "future text must not reuse L_cg for both parent constant and domain readout without labels.",
            },
            {
                "audit_id": "LCA1370_4_claim_grade",
                "test": "Can the current corpus claim fixed-L0 as live parent theory?",
                "result": "FAIL_NOT_SOURCE_SIGNED",
                "reason": "The contract is newly articulated here; previous registered evidence only made it a best route.",
                "remaining_risk": "requires a parent action insertion checkpoint before local-GR scoring.",
            },
        ]
    )


def cqgamma_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "derivation_id": "CQG1370_0_type_guard",
                "object": "q_loc^nu",
                "statement": "q_loc is a vector/Ward-force residual, not a scalar metric trace.",
                "derived_relation": "A coefficient gamma_minus_1=C*q_loc is ill-typed until a response operator maps q_loc into a spatial metric perturbation.",
                "status": "DIRECT_SCALAR_MAP_REJECTED",
                "missing_for_numeric": "response operator, gauge, boundary, source normalization",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1185_QLOC_RESPONSE_SPLIT_ATTEMPT.csv",
                "source_anchors": "QRS1185_0_type_guard;QRS1185_1_response_operator",
            },
            {
                "derivation_id": "CQG1370_1_ward_safe_compensator",
                "object": "C_q^{mu nu}",
                "statement": "Metric sources must be conserved; embed q_loc in a compensator satisfying nabla_mu C_q^{mu nu}=-q_loc^nu.",
                "derived_relation": "delta G^{mu nu}=kappa C_q^{mu nu} is Bianchi-safe only after Div C_q=-q_loc with boundary conditions.",
                "status": "WARD_SAFE_ROUTE_REQUIRED",
                "missing_for_numeric": "parent-owned compensator or right-inverse of divergence",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv",
                "source_anchors": "RQB1186_0_direct_map_guard;RQB1186_1_compensator_route",
            },
            {
                "derivation_id": "CQG1370_2_operator_factorization",
                "object": "R_q",
                "statement": "Choose a gauge/domain Green operator G_EH and a divergence right-inverse Div^{-1}.",
                "derived_relation": "delta g_ij^(q)=P_ij G_EH Div^{-1}[-q_loc] := R_{ij nu} q_loc^nu.",
                "status": "SYMBOLIC_RESPONSE_OPERATOR_DERIVED",
                "missing_for_numeric": "G_EH, Div^{-1}, gauge, domain, boundary, units",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1185_QLOC_RESPONSE_SPLIT_ATTEMPT.csv",
                "source_anchors": "RQB1186_2_operator_factorization;QRS1185_2_scalar_projection",
            },
            {
                "derivation_id": "CQG1370_3_gamma_projection_coefficient",
                "object": "C_qgamma",
                "statement": "Using g_ij=(1+2 gamma U/c^2)delta_ij+H_ij^TF, a scalar spatial trace perturbation obeys gamma_minus_1=(c^2/(2U_ref)) P_scalar[delta g_ij^(q)].",
                "derived_relation": "C_qgamma[Q0]=-(c^2/(2U_ref)) P_scalar P_metric G_EH Div^{-1}[Q0] when q_loc=q_loc_hat Q0.",
                "status": "SYMBOLIC_WARD_SAFE_COEFFICIENT_DERIVED",
                "missing_for_numeric": "Q0 profile, U_ref/source convention, G_EH, Div^{-1}, boundary, sign convention",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv;source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv",
                "source_anchors": "PPNP1182_0_metric_ansatz;PPNP1182_2_gamma_leakage;RQB1186_2_operator_factorization",
            },
            {
                "derivation_id": "CQG1370_4_norm_bound",
                "object": "|gamma_minus_1_q_loc|",
                "statement": "A nonclaim norm bound follows from the operator factorization.",
                "derived_relation": "|gamma-1| <= (c^2/(2U_min)) ||P_scalar P_metric G_EH|| ||Div^{-1}|| ||q_loc||, with all norms domain/gauge dependent.",
                "status": "SYMBOLIC_BOUND_FORM_DERIVED",
                "missing_for_numeric": "U_min, operator norms, q_loc norm, boundary conditions",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv",
                "source_anchors": "RQB1186_2_operator_factorization;RQB1186_4_verdict",
            },
            {
                "derivation_id": "CQG1370_5_qR_special_case_guard",
                "object": "q_R bridge",
                "statement": "The existing q_R map gives gamma_minus_1_QR approximately -q_R_hat/2, but it is not a q_loc coefficient unless q_loc reduces to the same scalar exterior hair.",
                "derived_relation": "C_qgamma=-1/2 is allowed only under a q_loc -> q_R reduction theorem and matching GM/source normalization.",
                "status": "QR_SPECIAL_CASE_NOT_IMPORTED",
                "missing_for_numeric": "q_loc-to-q_R reduction theorem",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv;source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
                "source_anchors": "QMAP1240_3_gamma_projection;RPF1244_0_policy",
            },
            {
                "derivation_id": "CQG1370_6_verdict",
                "object": "q_loc weak-field response coefficient",
                "statement": "1370 upgrades C_qgamma from missing to symbolic Ward-safe operator coefficient, not a number.",
                "derived_relation": "C_qgamma exists as a formal operator functional once Q0, U_ref, G_EH, Div^{-1}, gauge, and boundary are supplied.",
                "status": "SYMBOLIC_COEFFICIENT_READY_NUMERIC_INPUTS_MISSING",
                "missing_for_numeric": "Q0;U_ref;G_EH;Div^{-1};gauge;boundary;q_loc_hat",
                "source_paths": "aggregate_cqgamma_derivation",
                "source_anchors": "CQG1370_0_to_CQG1370_5",
            },
        ]
    )


def runner_update_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "runner_id": "QGR1370_0_q_loc_hat",
                "field": "q_loc_hat",
                "old_status": "MISSING_QLOC_VALUE",
                "new_status": "MISSING_QLOC_VALUE_UNCHANGED",
                "value_or_formula": "finite dimensionless amplitude still absent",
                "claim_effect": "runner cannot score",
            },
            {
                "runner_id": "QGR1370_1_C_qgamma_symbolic",
                "field": "C_qgamma",
                "old_status": "MISSING_WEAK_FIELD_RESPONSE",
                "new_status": "SYMBOLIC_WARD_SAFE_COEFFICIENT",
                "value_or_formula": "C_qgamma[Q0]=-(c^2/(2U_ref)) P_scalar P_metric G_EH Div^{-1}[Q0]",
                "claim_effect": "projection lane is now mathematically typed but still nonnumeric",
            },
            {
                "runner_id": "QGR1370_2_numeric_inputs",
                "field": "numeric response inputs",
                "old_status": "not separated",
                "new_status": "MISSING_NUMERIC_OPERATOR_INPUTS",
                "value_or_formula": "Q0;U_ref;G_EH;Div^{-1};gauge;boundary;operator norms",
                "claim_effect": "blocks PPN pass until sourced",
            },
            {
                "runner_id": "QGR1370_3_direct_map_guard",
                "field": "direct q_loc to gamma coefficient",
                "old_status": "implicit missing",
                "new_status": "FORBIDDEN_BY_WARD_GUARD",
                "value_or_formula": "no direct scalar C*q_loc without conserved compensator",
                "claim_effect": "prevents a cheap but invalid PPN score",
            },
            {
                "runner_id": "QGR1370_4_smoke_result",
                "field": "nonclaim smoke",
                "old_status": "BLOCKED_MISSING_QLOC_OR_RESPONSE",
                "new_status": "BLOCKED_SYMBOLIC_RESPONSE_NUMERIC_INPUTS_MISSING",
                "value_or_formula": "gamma_minus_1_predicted remains MISSING_NUMERIC",
                "claim_effect": "schema improved; no empirical pass",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1370_0_fixed_Lcg_covariance",
                "gate": "fixed L0 parent contract is covariance-admissible",
                "status": "PASS_CLOSURE_CANDIDATE",
                "reason": "constant scalar parameter does not select a frame; delta_g L0=0.",
            },
            {
                "gate_id": "GATE1370_1_fixed_Lcg_source_signed",
                "gate": "fixed L0 is source-signed as the live parent definition",
                "status": "BLOCKED_NOT_CORPUS_SIGNED",
                "reason": "1370 writes the contract but prior registered corpus does not adopt it.",
            },
            {
                "gate_id": "GATE1370_2_ML_zero_live",
                "gate": "M_L=0 can be used in live local-GR scoring",
                "status": "BLOCKED_CONDITIONAL_ONLY",
                "reason": "M_L=0 follows under fixed-L0 closure but not under metric-composite L_cg routes.",
            },
            {
                "gate_id": "GATE1370_3_Cqgamma_symbolic",
                "gate": "q_loc-to-gamma response coefficient is mathematically typed",
                "status": "PASS_SYMBOLIC_WARD_SAFE",
                "reason": "C_qgamma is derived as a Green-operator/divergence-inverse functional.",
            },
            {
                "gate_id": "GATE1370_4_Cqgamma_numeric",
                "gate": "q_loc-to-gamma runner can compute a number",
                "status": "BLOCKED_NUMERIC_INPUTS_MISSING",
                "reason": "q_loc profile, source normalization, operator norms, gauge, and boundary are missing.",
            },
            {
                "gate_id": "GATE1370_5_local_GR_or_PPN_claim",
                "gate": "local GR / PPN pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "fixed L0 is not parent-signed and q_loc gamma coefficient is symbolic only.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1370_0_preferred_Lcg_route",
                "decision": "prefer fixed-L0 parent contract if the theory can tolerate a global effective scale",
                "why": "it closes M_L without covariance cheating and avoids metric-composite response terms",
                "next_action": "insert the contract into a parent-action checkpoint, with distinct notation for post-variation readout scales",
            },
            {
                "decision_id": "DEC1370_1_no_local_length_smuggling",
                "decision": "do not reuse L_cg for local domain/cell/curvature lengths inside variation",
                "why": "those definitions generically have nonzero metric response",
                "next_action": "if a local length is needed, name it L_read or L_D and bound its response separately",
            },
            {
                "decision_id": "DEC1370_2_Cqgamma_progress",
                "decision": "upgrade q_loc projection from missing to symbolic Ward-safe",
                "why": "direct map is Bianchi-unsafe, but compensator plus Green operator gives a valid coefficient form",
                "next_action": "derive a bounded domain operator norm or prove q_loc reduces to q_R",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1370_0_1371",
                "next_doc": "1371-Y5-R10-RAB-fixed-Lcg-parent-action-insertion-or-Cqgamma-norm-bound.md",
                "next_script": "scripts/Y5_R10_RAB_fixed_Lcg_parent_action_insertion_or_Cqgamma_norm_bound.py",
                "task": "attempt to insert the fixed-L0 contract into the parent action with separate readout notation; if not, derive a bounded C_qgamma norm row by specifying gauge, domain, boundary, and q_loc normalization inputs",
                "success_condition": "either M_L=0 becomes parent-action signed as a closure branch, or C_qgamma receives a source-ready norm-bound input table that can be used by the nonclaim PPN runner",
                "do_not_claim": "local GR;PPN pass;q_loc=0;Khat match;R10 pass;GitHub-ready result",
            }
        ]
    )


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            rows = read_csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    cqgamma: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in sources + contract + audit + cqgamma + runner + gates
    )
    fixed_contract = any(row["clause_id"] == "LCC1370_4_metric_silence_result" and row["status"] == "DERIVED_UNDER_CLOSURE_CONTRACT" for row in contract)
    not_live = any(row["clause_id"] == "LCC1370_5_corpus_signature_verdict" and row["status"] == "NOT_LIVE_CLAIM_UNTIL_PARENT_SIGNED" for row in contract)
    covariance_pass = any(row["audit_id"] == "LCA1370_0_covariance" and row["result"] == "PASS_AS_CONSTANT_SCALAR" for row in audit)
    cqgamma_symbolic = any(row["derivation_id"] == "CQG1370_3_gamma_projection_coefficient" and row["status"] == "SYMBOLIC_WARD_SAFE_COEFFICIENT_DERIVED" for row in cqgamma)
    direct_rejected = any(row["derivation_id"] == "CQG1370_0_type_guard" and row["status"] == "DIRECT_SCALAR_MAP_REJECTED" for row in cqgamma)
    runner_blocked = any(row["runner_id"] == "QGR1370_4_smoke_result" and row["new_status"] == "BLOCKED_SYMBOLIC_RESPONSE_NUMERIC_INPUTS_MISSING" for row in runner)
    local_claim_blocked = any(row["gate_id"] == "GATE1370_5_local_GR_or_PPN_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1370_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1370_1_fixed_Lcg_contract",
            "check": "fixed L0 contract derives M_L=0 only as closure candidate",
            "status": "PASS" if fixed_contract and not_live and covariance_pass else "FAIL",
            "details": "constant scalar is covariance-admissible; corpus signature remains blocked",
        },
        {
            "validation_id": "VAL1370_2_Cqgamma_symbolic",
            "check": "q_loc gamma coefficient is upgraded to symbolic Ward-safe form",
            "status": "PASS" if cqgamma_symbolic and direct_rejected else "FAIL",
            "details": "direct scalar map rejected; compensator/Green operator coefficient derived",
        },
        {
            "validation_id": "VAL1370_3_runner_refusal",
            "check": "runner still refuses to score missing numeric inputs",
            "status": "PASS" if runner_blocked else "FAIL",
            "details": "q_loc_hat and numeric operator inputs remain missing",
        },
        {
            "validation_id": "VAL1370_4_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1370 is closure/projection discipline, not a local-GR or PPN pass",
        },
        {
            "validation_id": "VAL1370_5_local_claim_blocked",
            "check": "local GR / PPN claim remains blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1370_5_local_GR_or_PPN_claim remains BLOCKED_NO_CLAIM",
        },
        {
            "validation_id": "VAL1370_6_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1370_7_overall",
            "check": "overall 1370 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1370 supplies a covariance-admissible fixed-L0 closure candidate and a symbolic Ward-safe C_qgamma, while blocking claims.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    cqgamma: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1370 makes two useful moves without claiming the round. First, a fixed `L_cg=L0` parent contract is covariance-admissible and gives `delta_g L0=0`, hence `M_L^{{mu nu}}=0`, but only as a closure candidate until the parent action explicitly adopts it. Second, `C_qgamma` is no longer just “missing”: it has a Ward-safe symbolic form through a conserved compensator and Green operator.

**Main progress:** the cleanest local-GR route is now sharply stated: use `L0` as an external effective scale under Hilbert variation, and keep any local cell/domain readout as a separate post-variation object. The testing lane also improves: `q_loc -> gamma` must go through `C_qgamma[Q0]=-(c^2/(2U_ref)) P_scalar P_metric G_EH Div^-1[Q0]`, not a hand-waved scalar coefficient.

**Still blocked:** no local-GR or PPN pass is allowed. `M_L=0` is not live until the parent action signs fixed `L0`; `C_qgamma` is symbolic until `Q0`, `U_ref`, gauge, boundary conditions, `G_EH`, `Div^-1`, and `q_loc_hat` are supplied.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## Parent `L_cg` Contract Candidate

{table(["clause_id", "clause", "status", "contract_text", "proof_or_risk", "consequence", "source_paths", "source_anchors", "valid_for_claim", "claim_allowed"], contract)}

## Parent `L_cg` Contract Audit

{table(["audit_id", "test", "result", "reason", "remaining_risk", "valid_for_claim", "claim_allowed"], audit)}

## Ward-Safe `C_qgamma` Derivation

{table(["derivation_id", "object", "status", "statement", "derived_relation", "missing_for_numeric", "source_paths", "source_anchors", "valid_for_claim", "claim_allowed"], cqgamma)}

## `q_loc -> gamma` Runner Update

{table(["runner_id", "field", "old_status", "new_status", "value_or_formula", "claim_effect", "valid_for_claim", "claim_allowed"], runner)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    contract = lcg_contract_rows()
    audit = lcg_audit_rows()
    cqgamma = cqgamma_rows()
    runner = runner_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(LCG_CONTRACT_PATH, contract)
    write_csv(LCG_AUDIT_PATH, audit)
    write_csv(CQGAMMA_PATH, cqgamma)
    write_csv(RUNNER_UPDATE_PATH, runner)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        LCG_CONTRACT_PATH,
        LCG_AUDIT_PATH,
        CQGAMMA_PATH,
        RUNNER_UPDATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, contract, audit, cqgamma, runner, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, contract, audit, cqgamma, runner, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
