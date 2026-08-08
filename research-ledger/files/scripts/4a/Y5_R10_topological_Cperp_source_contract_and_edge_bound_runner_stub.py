from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1163-Y5-R10-topological-Cperp-source-contract-and-edge-bound-runner-stub.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def local_path(relative_path: str) -> Path:
    return ROOT / relative_path


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def is_missing(value: object) -> bool:
    text = str(value).strip()
    return (
        text == ""
        or "MISSING" in text
        or "BLOCKED" in text
        or "NOT_SOURCED" in text
        or "NOT_DERIVED" in text
        or "SOURCE_ANCHOR_ONLY" in text
        or "NONCLAIM" in text
        or "NOT_ADOPTED" in text
        or "SHAPE_SUPPORT_ONLY" in text
    )


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1163_0_1162_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1162_NEXT_TARGET.csv",
            "needle": "NEXT1162_0_1163",
            "role": "handoff requiring strict Cperp source contract and no-claim runner stub.",
        },
        {
            "source_id": "SRC1163_1_1162_candidate_choice",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv",
            "needle": "CAND1162_0_topological_projector_residual",
            "role": "single selected acquisition candidate C_perp=(I-P_D)C.",
        },
        {
            "source_id": "SRC1163_2_1162_edge_fill",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1162_EDGE_BOUND_FIRST_SOURCE_FILL.csv",
            "needle": "EFS1162_0_C_corner",
            "role": "first edge-bound source-fill row set imported into the runner stub.",
        },
        {
            "source_id": "SRC1163_3_1161_source_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
            "needle": "CDSRC1161_0_Cperp_definition",
            "role": "older explicit missing-source pack for Cperp, P_D, d_rel, closedness, and selector.",
        },
        {
            "source_id": "SRC1163_4_272_quotient",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "[C] = C / ker(P_D).",
            "role": "quotient route supporting the candidate contract shape.",
        },
        {
            "source_id": "SRC1163_5_272_relative_exactness",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "Cperp residuals are relative-exact representatives",
            "role": "conditional exactness route and its open burden.",
        },
        {
            "source_id": "SRC1163_6_1020_weighted_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "edge-bound formula source for corner and surface derivative terms.",
        },
        {
            "source_id": "SRC1163_7_1020_BC_primitive",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BXP1020_2_exact_primitive",
            "role": "primitive row showing the exact primitive remains not derived.",
        },
        {
            "source_id": "SRC1163_8_1020_cohomology",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_2_relative_cohomology",
            "role": "harmonic edge mode zero-or-bound requirement.",
        },
        {
            "source_id": "SRC1163_9_1019_projector",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "SP1019_6_projector_zero_or_bound",
            "role": "projector source bound requirement for Qbar_CXH.",
        },
        {
            "source_id": "SRC1163_10_1040_QX",
            "relative_path": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "needle": "BX1040_2_candidate_QX",
            "role": "boundary charge formula contract tied to edge readout.",
        },
        {
            "source_id": "SRC1163_11_1040_cocycle",
            "relative_path": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "needle": "KBC1040_0_contract",
            "role": "boundary cocycle source-contract row.",
        },
        {
            "source_id": "SRC1163_12_1144_selector",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv",
            "needle": "RC1144_2_same_parent_law",
            "role": "local-trivial/FLRW-active branch selector remains a missing parent-law requirement.",
        },
        {
            "source_id": "SRC1163_13_1146_no_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
            "needle": "NF1146_6_verdict",
            "role": "epsilon no-flux sibling gate remains blocked.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in sources:
        path = local_path(str(row["relative_path"]))
        text = read_text(path)
        checked.append(
            {
                **row,
                "exists": path.exists(),
                "needle_found": str(row["needle"]) in text,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return checked


def contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "CTC1163_0_candidate_lock",
            "clause": "single C_perp candidate",
            "strict_requirement": "Carry only C_perp=(I-P_D)C or equivalent topological/projector residual; no candidate switching.",
            "candidate_value": "C_perp=(I-P_D)C",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv",
            "source_needle": "CAND1162_0_topological_projector_residual",
            "current_status": "ACQUISITION_CANDIDATE_ONLY",
            "missing_piece": "parent-signed definition not yet supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_1_parent_C_object",
            "clause": "parent C object",
            "strict_requirement": "Define C as a specific parent field/cochain/form with bundle, degree, orientation, units, and variation rule.",
            "candidate_value": "C is the object projected by P_D",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
            "source_needle": "CDSRC1161_0_Cperp_definition",
            "current_status": "MISSING_PARENT_C_OBJECT",
            "missing_piece": "actual C variable owner and degree",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_2_PD_owner",
            "clause": "P_D projector ownership",
            "strict_requirement": "Source P_D as an idempotent, metric-independent or explicitly metric-dependent projector with delta P_D rule.",
            "candidate_value": "P_D from quotient/topological projector route",
            "source_anchor": "272-quotient-configuration-principle-from-topological-projector.md",
            "source_needle": "[C] = C / ker(P_D).",
            "current_status": "PARTIAL_SHAPE_SUPPORT_ONLY",
            "missing_piece": "projector definition, domain rule, idempotence proof, and variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_3_Cperp_definition",
            "clause": "C_perp definition",
            "strict_requirement": "After C and P_D are sourced, define C_perp=(I-P_D)C and state whether it is bulk, boundary, or relative-pair valued.",
            "candidate_value": "C_perp=(I-P_D)C",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv",
            "source_needle": "CAND1162_0_topological_projector_residual",
            "current_status": "FORMULA_STUB_NOT_DEFINITION",
            "missing_piece": "C and P_D must be parent-owned first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_4_form_degree_units",
            "clause": "form degree and units",
            "strict_requirement": "Give form degree k, boundary degree k-1, dimensions, normalization, and integration measure.",
            "candidate_value": "unspecified",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
            "source_needle": "CDSRC1161_0_Cperp_definition",
            "current_status": "MISSING_FORM_DEGREE_AND_UNITS",
            "missing_piece": "degree, units, and normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_5_relative_pair",
            "clause": "relative domain pair",
            "strict_requirement": "Specify local domain U, boundary S, pullback i_star, boundary class, support/collar conditions, and allowed variations.",
            "candidate_value": "(U,S) relative pair",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BDC1020_2_relative_cohomology",
            "current_status": "PARTIAL_BOUNDARY_SHAPE_SUPPORT",
            "missing_piece": "C-sector relative pair and allowed boundary class",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_6_drel_complex",
            "clause": "d_rel operator",
            "strict_requirement": "Instantiate d_rel on Omega_C^k(U,S), including signs, nilpotency, boundary pullback, and source terms.",
            "candidate_value": "standard relative differential shape only",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
            "source_needle": "CDSRC1161_2_drel_operator",
            "current_status": "MISSING_DREL_OPERATOR_FOR_C_SECTOR",
            "missing_piece": "actual complexes and sign convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_7_closedness_identity",
            "clause": "relative closedness",
            "strict_requirement": "Prove d_rel C_perp=0 or identify nonzero source/support terms to bound.",
            "candidate_value": "d_rel C_perp=0 desired",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
            "source_needle": "CDSRC1161_3_closedness_identity",
            "current_status": "MISSING_CPERP_CLOSEDNESS_PROOF",
            "missing_piece": "Noether/Bianchi/Euler identity with boundary/source terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_8_exactness_or_harmonic_bound",
            "clause": "relative exactness or harmonic bound",
            "strict_requirement": "Either source C_perp=d_rel B_C with h_C=0, or supply h_C and residual bounds.",
            "candidate_value": "Cperp residuals are relative-exact representatives",
            "source_anchor": "272-quotient-configuration-principle-from-topological-projector.md",
            "source_needle": "Cperp residuals are relative-exact representatives",
            "current_status": "CONDITIONAL_ROUTE_OPEN",
            "missing_piece": "B_C primitive and H_rel certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_9_BC_primitive",
            "clause": "B_C primitive",
            "strict_requirement": "Write B_C or b_C explicitly and define the norm used in the weighted-Stokes edge bound.",
            "candidate_value": "B_C primitive placeholder",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BXP1020_2_exact_primitive",
            "current_status": "NOT_DERIVED",
            "missing_piece": "primitive formula and norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_10_edge_readout",
            "clause": "edge readout formula",
            "strict_requirement": "Use weighted Stokes to compute or bound corner, derivative-weight, primitive, harmonic, residual, and cocycle terms.",
            "candidate_value": "|Q_C| <= |C_corner| + ||d_S(F eps)|| ||B_C|| + |h_C| + |r_C| + |K_boundary Qbar_CXH|",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_1_weighted_Stokes_identity",
            "current_status": "FORMULA_STUB_ONLY",
            "missing_piece": "all numeric/theorem-zero edge inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_11_branch_selector",
            "clause": "local trivial / FLRW active selector",
            "strict_requirement": "Prove from one parent law when local branch has trivial C_perp while FLRW/domain branch is active.",
            "candidate_value": "same-parent-law selector required",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv",
            "source_needle": "RC1144_2_same_parent_law",
            "current_status": "MISSING_PARENT_BRANCH_SELECTION_LAW",
            "missing_piece": "no hand-switch theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_12_no_frame_shortcut",
            "clause": "no hidden c_g/frame shortcut",
            "strict_requirement": "Do not rename frame/A_g/Xhat residual as C_perp unless a no-shadow matter quotient theorem is independently sourced.",
            "candidate_value": "frame residual excluded from C_perp definition",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv",
            "source_needle": "CAND1162_2_frame_conformal_residual",
            "current_status": "GUARD_ACTIVE",
            "missing_piece": "no-shadow theorem still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "CTC1163_13_claim_promotion",
            "clause": "claim promotion gate",
            "strict_requirement": "Only promote after C, P_D, d_rel, closedness/exactness, B_C, edge terms, selector, and no-shadow gates close.",
            "candidate_value": "promotion blocked",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1162_CLAIM_GATES.csv",
            "source_needle": "G1162_4_claim_promotion",
            "current_status": "BLOCKED",
            "missing_piece": "multiple parent and edge inputs missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


EDGE_REQUIREMENTS = {
    "C_corner": "zero_theorem_or_nonnegative_abs_numeric_bound",
    "norm_dS_Feps": "closed_weight_zero_theorem_or_nonnegative_dual_surface_norm",
    "norm_bC": "explicit_BC_primitive_norm_or_zero_certificate",
    "harmonic_edge_abs": "H_rel_zero_theorem_or_nonnegative_abs_bound",
    "residual_edge_abs": "residual_zero_theorem_or_nonnegative_abs_bound",
    "K_boundary": "cocycle_zero_theorem_or_nonnegative_operator_bound",
    "Qbar_CXH": "projector_zero_theorem_or_nonnegative_abs_source_bound",
    "local_trivial_FLRW_active_selector": "parent_branch_function_or_boolean_theorem",
    "epsilon_domain_flux_zero_or_bound": "epsilon_no_flux_theorem_or_nonnegative_profile_bound",
}


def edge_schema_rows(edge_fill_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for input_row in edge_fill_rows:
        quantity = input_row["quantity"]
        rows.append(
            {
                "input_id": input_row["fill_id"].replace("EFS1162", "EIS1163"),
                "quantity": quantity,
                "source_anchor": input_row["source_anchor"],
                "source_needle": input_row["source_needle"],
                "required_kind": EDGE_REQUIREMENTS.get(quantity, "explicit_source_backed_value_or_theorem"),
                "units_requirement": input_row["units"],
                "current_input_status": input_row["status"],
                "numeric_value": "MISSING_NUMERIC_VALUE",
                "theorem_zero_certificate": "MISSING_THEOREM_ZERO_CERTIFICATE",
                "runner_role": runner_role(quantity),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_role(quantity: str) -> str:
    roles = {
        "C_corner": "additive_edge_bound_term",
        "norm_dS_Feps": "multiplicative_weight_derivative_factor",
        "norm_bC": "multiplicative_primitive_norm_factor",
        "harmonic_edge_abs": "additive_harmonic_bound_term",
        "residual_edge_abs": "additive_residual_bound_term",
        "K_boundary": "multiplicative_cocycle_operator_factor",
        "Qbar_CXH": "multiplicative_projected_source_factor",
        "local_trivial_FLRW_active_selector": "branch_gate_not_numeric_term",
        "epsilon_domain_flux_zero_or_bound": "sibling_flux_gate",
    }
    return roles.get(quantity, "unclassified_required_input")


def formula_rows() -> list[dict[str, object]]:
    return [
        {
            "formula_id": "EBF1163_0_edge_bound_formula",
            "formula": "|Q_C| <= |C_corner| + ||d_S(F eps)||_* ||B_C||_* + |h_C| + |r_C| + |K_boundary Qbar_CXH| + epsilon_flux_sibling",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_1_weighted_Stokes_identity",
            "status": "FORMULA_STUB_ONLY_INPUTS_MISSING",
            "evaluation": "not_evaluated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "EBF1163_1_zero_route",
            "formula": "Q_C=0 only if corner=0, d_S(F eps)=0 or B_C=0, h_C=0, r_C=0, K_boundary Qbar_CXH=0, selector local-trivial, and epsilon flux gate closes",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_2_zero_conditions",
            "status": "CONDITIONAL_ONLY_NOT_MET",
            "evaluation": "blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "EBF1163_2_finite_bound_route",
            "formula": "Finite local residual may be bounded only after every additive/multiplicative term has sourced units and values",
            "source_anchor": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "source_needle": "SP1019_6_projector_zero_or_bound",
            "status": "INPUT_SCHEMA_READY_VALUES_MISSING",
            "evaluation": "blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def run_edge_stub(schema_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked_inputs = [
        str(row["quantity"])
        for row in schema_rows
        if is_missing(row["numeric_value"])
        and is_missing(row["theorem_zero_certificate"])
    ]
    numeric_inputs = [
        str(row["quantity"])
        for row in schema_rows
        if not is_missing(row["numeric_value"])
    ]
    theorem_zero_inputs = [
        str(row["quantity"])
        for row in schema_rows
        if not is_missing(row["theorem_zero_certificate"])
    ]
    all_inputs_ready = not blocked_inputs and len(schema_rows) > 0
    return [
        {
            "run_id": "RUN1163_0_load_edge_schema",
            "test": "load 1162 edge-fill rows into strict runner schema",
            "input_rows": len(schema_rows),
            "blocked_inputs": ";".join(blocked_inputs),
            "numeric_inputs": ";".join(numeric_inputs),
            "theorem_zero_inputs": ";".join(theorem_zero_inputs),
            "status": "SCHEMA_LOADED_INPUTS_MISSING",
            "claim_allowed": False,
            "detail": "schema is usable but every edge quantity still needs a numeric bound or theorem-zero certificate",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1163_1_claim_refusal",
            "test": "refuse Cperp/local claim when required inputs are missing",
            "input_rows": len(schema_rows),
            "blocked_inputs": ";".join(blocked_inputs),
            "numeric_inputs": ";".join(numeric_inputs),
            "theorem_zero_inputs": ";".join(theorem_zero_inputs),
            "status": "PASS_REFUSED_CLAIM_AS_DESIGNED",
            "claim_allowed": all_inputs_ready,
            "detail": "claim_allowed remains false because no required edge input is sourced",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1163_2_formula_evaluation",
            "test": "evaluate edge-bound formula only if all inputs are sourced",
            "input_rows": len(schema_rows),
            "blocked_inputs": ";".join(blocked_inputs),
            "numeric_inputs": ";".join(numeric_inputs),
            "theorem_zero_inputs": ";".join(theorem_zero_inputs),
            "status": "NOT_EVALUATED_BY_GATE",
            "claim_allowed": False,
            "detail": "runner intentionally does not compute a numeric residual from placeholder rows",
            "valid_for_claim": False,
        },
    ]


def guard_rows() -> list[dict[str, object]]:
    return [
        {
            "guard_id": "GUA1163_0_no_candidate_switching",
            "guard": "Only the topological/projector C_perp candidate may be carried into this branch.",
            "failure_mode_prevented": "mixing J_rel/domain current or frame residual definitions into one symbol",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "GUA1163_1_no_frame_cg_renaming",
            "guard": "Frame/A_g/Xhat residuals cannot be relabelled as C_perp without a separate no-shadow theorem.",
            "failure_mode_prevented": "hiding the common-frame coupling problem inside notation",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "GUA1163_2_no_numeric_placeholders",
            "guard": "MISSING, anchor-only, symbolic, or nonclaim rows cannot enter a numeric edge-bound result.",
            "failure_mode_prevented": "accidental fake local/R10 pass",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "GUA1163_3_no_zero_by_exactness_alone",
            "guard": "Exactness does not zero the edge charge unless corner, weight derivative, harmonic, residual, and cocycle terms also close.",
            "failure_mode_prevented": "Stokes theorem misuse",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "GUA1163_4_no_local_claim",
            "guard": "No local GR/Newton/R10/PPN/WEP/clock/orbital claim follows from this stub.",
            "failure_mode_prevented": "overclaiming from a runner harness",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CG1163_0_candidate_source_contract",
            "gate": "C, P_D, C_perp, form degree, units, variation rule, and d_rel are parent-sourced",
            "required_evidence": "CTC1163_1 through CTC1163_7 closed with valid source paths",
            "current_status": "BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1163_1_exactness_or_bound",
            "gate": "C_perp exactness, B_C primitive, H_rel/harmonic, residual, and boundary terms are zeroed or bounded",
            "required_evidence": "CTC1163_8 through CTC1163_10 plus EIS1163 rows sourced",
            "current_status": "BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1163_2_runner_claim_allowed",
            "gate": "edge-bound runner returns claim_allowed=true",
            "required_evidence": "all schema rows have numeric values or theorem-zero certificates",
            "current_status": "BLOCKED_RUNNER_REFUSES_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1163_3_branch_and_no_shadow",
            "gate": "same-parent branch selector and no hidden c_g/frame shortcut theorem close",
            "required_evidence": "CTC1163_11 and CTC1163_12 closed",
            "current_status": "BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1163_4_local_claim_promotion",
            "gate": "local GR/Newton/R10/PPN/WEP/clock/orbital promotion",
            "required_evidence": "all previous gates pass plus arena projections",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1163_0_contract_status",
            "decision": "strict_source_contract_written_but_not_satisfied",
            "reason": "the topological/projector candidate is now legally specified as an acquisition branch, but C, P_D, d_rel, closedness, and B_C remain source-missing",
            "next_action": "source or derive one hard parent clause rather than broaden the branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1163_1_runner_status",
            "decision": "edge_bound_runner_stub_refuses_claim",
            "reason": "every edge input is schema-visible but still lacks a numeric bound or theorem-zero certificate",
            "next_action": "fill first edge term or prove a zero condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1163_2_best_next",
            "decision": "target_parent_C_PD_drel_source_hunt_or_first_edge_zero_certificate",
            "reason": "this is the narrowest route that can turn the candidate from a scaffold into either a theorem branch or a finite bound",
            "next_action": "1164 should attempt C/P_D/d_rel source closure first; if it fails, attack C_corner or d_S(F eps) zero/bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1163_0_1164",
            "next_target": "1164-Y5-R10-parent-C-PD-drel-source-hunt-or-first-edge-zero-certificate.md",
            "objective": "try to source or derive the parent C object, P_D projector ownership, and C-sector d_rel complex; if not closed, fill the first edge-bound zero/bound certificate such as C_corner or d_S(F epsilon)",
            "include": "C object; P_D owner; form degree; d_rel signs; closedness/source terms; C_corner theorem/bound; dS_Feps theorem/bound; runner dry-run",
            "exclude": "candidate switching; invented edge numbers; frame residual renaming; c_g zero claim; local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    schema: list[dict[str, object]],
    runner: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    required_contract = {
        "single C_perp candidate",
        "parent C object",
        "P_D projector ownership",
        "C_perp definition",
        "form degree and units",
        "relative domain pair",
        "d_rel operator",
        "relative closedness",
        "relative exactness or harmonic bound",
        "B_C primitive",
        "edge readout formula",
        "local trivial / FLRW active selector",
        "no hidden c_g/frame shortcut",
        "claim promotion gate",
    }
    contract_clauses = {str(row["clause"]) for row in contract}
    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    schema_quantities = {str(row["quantity"]) for row in schema}
    edge_expected = set(EDGE_REQUIREMENTS)
    runner_refuses = all(is_false(row["claim_allowed"]) for row in runner)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for table in (sources, contract, schema, runner, guards, gates, next_rows)
        for row in table
    )
    no_values = all(
        str(row["numeric_value"]) == "MISSING_NUMERIC_VALUE"
        and str(row["theorem_zero_certificate"]) == "MISSING_THEOREM_ZERO_CERTIFICATE"
        for row in schema
    )
    csv_parse = True
    parse_detail = "all 1163 CSV outputs parse cleanly"
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - validation report
            csv_parse = False
            parse_detail = f"{path.name}: {exc}"
            break
    generated_under_post = all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in csv_paths + [DOC])
    rows = [
        {
            "check_id": "V1163_0_sources_exist",
            "result": "pass" if source_ok else "fail",
            "detail": "all cited local source paths exist and needles are found" if source_ok else "source path or needle missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_1_contract_complete_shape",
            "result": "pass" if required_contract <= contract_clauses else "fail",
            "detail": "strict source contract includes all required Cperp clauses",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_2_contract_not_satisfied",
            "result": "pass" if any("MISSING" in str(row["current_status"]) or "NOT_DERIVED" in str(row["current_status"]) for row in contract) else "fail",
            "detail": "contract remains intentionally unsatisfied/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_3_edge_schema_complete",
            "result": "pass" if schema_quantities == edge_expected else "fail",
            "detail": "edge schema has one row for every 1162 edge-fill quantity",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_4_no_invented_edge_values",
            "result": "pass" if no_values else "fail",
            "detail": "runner stub contains no numeric values or theorem-zero certificates",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_5_runner_refuses_claim",
            "result": "pass" if runner_refuses else "fail",
            "detail": "runner refuses edge/local claim while inputs are missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_6_guards_active",
            "result": "pass" if all(str(row["status"]) == "ACTIVE" for row in guards) else "fail",
            "detail": "candidate, frame-shortcut, placeholder, exactness, and local-claim guards are active",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_7_claim_gates_blocked",
            "result": "pass" if all(is_false(row["claim_allowed"]) for row in gates) else "fail",
            "detail": "all claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_8_no_claim_rows",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_9_next_target",
            "result": "pass" if next_rows and "1164" in str(next_rows[0]["next_target"]) else "fail",
            "detail": "1164 handoff targets parent C/P_D/d_rel source hunt or first edge zero certificate",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_10_generated_under_post_checkpoint",
            "result": "pass" if generated_under_post else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_11_csv_parse",
            "result": "pass" if csv_parse else "fail",
            "detail": parse_detail,
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1163_SUMMARY",
            "result": "pass" if source_ok and runner_refuses and all_nonclaim else "fail",
            "detail": "1163 converts the selected topological/projector Cperp branch into a strict source contract and no-claim edge-bound runner stub",
            "claim_allowed": False,
        },
    ]
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| "
        + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    schema: list[dict[str, object]],
    formulas: list[dict[str, object]],
    runner: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1163 — Y5/R10 topological Cperp source contract and edge-bound runner stub

**Current verdict:** the topological/projector branch is now executable as a strict acquisition contract, but it is still not a claim. `C_perp=(I-P_D)C` is only a candidate until the parent `C` object, `P_D`, `d_rel`, relative closedness, and `B_C` primitive are sourced.

**Main progress:** the edge-bound runner stub now has a hard input schema and refuses to evaluate or claim while the 1162 rows remain source-anchor-only. This is good discipline: we have a machine gate that prevents us from accidentally turning placeholders into a local/R10 result.

**Best next target:** source or derive the parent `C/P_D/d_rel` trio first. If that stalls, attack the first edge theorem/bound directly, starting with `C_corner=0` or `d_S(F epsilon)=0/bounded`.

## Source register

{md_table(sources, ["source_id", "relative_path", "needle", "exists", "needle_found", "role"])}

## Strict Cperp source contract

{md_table(contract, ["contract_id", "clause", "strict_requirement", "candidate_value", "current_status", "missing_piece", "valid_for_claim"])}

## Edge-bound input schema

{md_table(schema, ["input_id", "quantity", "required_kind", "units_requirement", "current_input_status", "numeric_value", "theorem_zero_certificate", "runner_role", "valid_for_claim"])}

## Edge-bound formula stubs

{md_table(formulas, ["formula_id", "formula", "status", "evaluation", "valid_for_claim"])}

## Runner stub results

{md_table(runner, ["run_id", "test", "input_rows", "status", "claim_allowed", "detail"])}

## No-cheat guards

{md_table(guards, ["guard_id", "guard", "failure_mode_prevented", "status", "valid_for_claim"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "required_evidence", "current_status", "claim_allowed"])}

## Decision ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "claim_allowed"])}

## Next target

{md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = stamp(source_rows())
    edge_fill_path = OUT / "P8_Y5_R10_1162_EDGE_BOUND_FIRST_SOURCE_FILL.csv"
    edge_fill_rows = read_csv(edge_fill_path)
    contract = stamp(contract_rows())
    schema = stamp(edge_schema_rows(edge_fill_rows))
    formulas = stamp(formula_rows())
    runner = stamp(run_edge_stub(schema))
    guards = stamp(guard_rows())
    gates = stamp(claim_gate_rows())
    decisions = stamp(decision_rows())
    next_rows = stamp(next_target_rows())

    outputs = {
        "P8_Y5_R10_1163_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1163_TOPOLOGICAL_CPERP_SOURCE_CONTRACT.csv": contract,
        "P8_Y5_R10_1163_EDGE_BOUND_INPUT_SCHEMA.csv": schema,
        "P8_Y5_R10_1163_EDGE_BOUND_FORMULA_STUBS.csv": formulas,
        "P8_Y5_R10_1163_EDGE_BOUND_RUNNER_STUB_RESULTS.csv": runner,
        "P8_Y5_R10_1163_NO_CHEAT_GUARDS.csv": guards,
        "P8_Y5_R10_1163_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1163_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1163_NEXT_TARGET.csv": next_rows,
    }
    csv_paths: list[Path] = []
    for name, rows in outputs.items():
        path = OUT / name
        write_csv(path, rows)
        csv_paths.append(path)

    validation = stamp(validate(sources, contract, schema, runner, guards, gates, next_rows, csv_paths))
    validation_path = OUT / "P8_Y5_BRR545_1163_VALIDATION.csv"
    write_csv(validation_path, validation)
    csv_paths.append(validation_path)
    write_doc(sources, contract, schema, formulas, runner, guards, gates, decisions, next_rows, validation)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
