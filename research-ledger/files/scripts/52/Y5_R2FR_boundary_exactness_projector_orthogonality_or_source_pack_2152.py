from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2152-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2151": ROOT / "2151-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
    "2151_validation": OUT / "P8_Y5_BRR545_2151_VALIDATION.csv",
    "2151_route": OUT / "P8_Y5_PARENT_QLOC_2151_ROUTE_TESTS.csv",
    "1843": ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
    "1843_validation": OUT / "P8_Y5_BRR545_1843_VALIDATION.csv",
    "1844": ROOT / "1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
    "1844_validation": OUT / "P8_Y5_BRR545_1844_VALIDATION.csv",
    "1844_next": OUT / "P8_Y5_PARENT_QLOC_1844_NEXT_TARGET.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2152_SOURCE_REGISTER.csv",
    "boundary_exactness": OUT / "P8_Y5_PARENT_QLOC_2152_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "projector_orthogonality": OUT / "P8_Y5_PARENT_QLOC_2152_PROJECTOR_ORTHOGONALITY_CLAUSES.csv",
    "domain_certificate": OUT / "P8_Y5_PARENT_QLOC_2152_BOUNDARY_DOMAIN_CERTIFICATE.csv",
    "weighted_stokes": OUT / "P8_Y5_PARENT_QLOC_2152_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
    "source_pack": OUT / "P8_Y5_PARENT_QLOC_2152_SOURCE_PACK_SCHEMA.csv",
    "route_verdicts": OUT / "P8_Y5_PARENT_QLOC_2152_ROUTE_VERDICTS.csv",
    "gr_bridge": OUT / "P8_Y5_PARENT_QLOC_2152_GR_BRIDGE_STATUS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2152_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2152_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2152_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2152_VALIDATION.csv",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2152_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2152-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2152*",
        "*P8_Y5_BRR545_2152*",
        "*Y5_R2FR_boundary_exactness_projector_orthogonality_or_source_pack_2152*",
        "*AFRAME_BOUNDARY_PROJECTOR_2152*",
        "*JR2152*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2152_00_2151_handoff",
            DOCS["2151"],
            [["NEXT2151_0_2152"], ["BOUNDARY_PROJECTOR_ROUTE_IS_BEST_NEXT"], ["VAL2151_OVERALL"]],
            "current 2151 handoff selects boundary exactness/projector orthogonality.",
        ),
        (
            "SRC2152_01_2151_validation",
            DOCS["2151_validation"],
            [["VAL2151_OVERALL"], ["PASS"]],
            "current 2151 validation passed as nonclaim.",
        ),
        (
            "SRC2152_02_2151_route_csv",
            DOCS["2151_route"],
            [["RT2151_4_boundary_projector_route"], ["NEXT_DERIVATION_ROUTE"]],
            "machine-readable current route split selects the boundary/projector path.",
        ),
        (
            "SRC2152_03_1843_boundary_projector",
            DOCS["1843"],
            [["ETB1843_5_verdict"], ["FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS"], ["NEXT1843_0_primary"]],
            "old 1843 gives boundary/projector exact conditions and finite fallback bound.",
        ),
        (
            "SRC2152_04_1843_validation",
            DOCS["1843_validation"],
            [["VAL1843_OVERALL"], ["PASS"]],
            "old 1843 validation passed as nonclaim.",
        ),
        (
            "SRC2152_05_1844_BX_primitive",
            DOCS["1844"],
            [["PVT1844_5_verdict"], ["BXG1844_5_verdict"], ["VAL1844_OVERALL"]],
            "old 1844 identifies B_X primitive as the next bottleneck.",
        ),
        (
            "SRC2152_06_1844_validation",
            DOCS["1844_validation"],
            [["VAL1844_OVERALL"], ["PASS"]],
            "old 1844 validation passed as nonclaim.",
        ),
        (
            "SRC2152_07_1844_next",
            DOCS["1844_next"],
            [["NEXT1844_0_primary"], ["vertical-quotient"], ["scalar-nohair"]],
            "old 1844 shows the post-primitive route split: vertical quotient first, scalar/source fallback second.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def boundary_exactness_rows() -> list[dict[str, object]]:
    data = [
        (
            "BE2152_0_domain",
            "edge integration domain has no untracked corner or domain dependence",
            "partial S_edge=empty, or every corner C carries explicit Q_C in source pack",
            "NOT_SIGNED",
            "parent boundary class fixes S_edge and corner terms before readout",
            "Stokes zero hides corner/domain charge",
        ),
        (
            "BE2152_1_exact_BX",
            "boundary momentum is exact on the certified boundary class",
            "B_X=d_S b_X with no residual r_X and no harmonic h_X",
            "NOT_DERIVED",
            "derive b_X from parent L_X/Theta_X/Q_X plus fixed counterterm",
            "Q_edge remains live or must be bounded",
        ),
        (
            "BE2152_2_harmonic_residual",
            "no harmonic or residual edge class survives",
            "B_X=d_S b_X+h_X+r_X with h_X=r_X=0",
            "NOT_SIGNED",
            "boundary cohomology/no-hair theorem or source-backed h_X/r_X bounds",
            "closed but wrong edge mode feeds R10/R11",
        ),
        (
            "BE2152_3_closed_weight",
            "weighted Stokes derivative term vanishes",
            "d_S(F_lambda epsilon_X)=0 on S_edge",
            "NOT_SIGNED",
            "kernel/gauge weight closure theorem or source-backed derivative norm",
            "exact B_X still leaves weighted derivative residual",
        ),
        (
            "BE2152_4_counterterm_reference",
            "boundary counterterm/reference cannot be tuned after readout",
            "B_ct,B_ref fixed once; partial_source Delta_ref=0",
            "NOT_SIGNED",
            "parent variational principle fixes counterterm and reference class",
            "reference absorbs source calibration or edge charge",
        ),
        (
            "BE2152_5_verdict",
            "boundary exactness kills edge branch",
            "BE2152_0 through BE2152_4 imply Q_edge^H(lambda)=0 and K_boundary=0",
            "FAIL_CURRENT_CLAIM",
            "all exactness clauses parent-signed in one boundary class",
            "retain source-pack fallback rows for Qbar_edge_XH and K_edge",
        ),
    ]
    return [
        row(clause_id=clause_id, claim=claim, mathematical_form=mathematical_form, current_status=current_status, what_would_close=what_would_close, failure_mode=failure_mode)
        for clause_id, claim, mathematical_form, current_status, what_would_close, failure_mode in data
    ]


def projector_orthogonality_rows() -> list[dict[str, object]]:
    data = [
        (
            "PO2152_0_projector_definition",
            "Pi_M^H is the fixed Hamiltonian source-mass projector",
            "Pi_M^H[J] = component of J paired with same-frame M_H_ref",
            "NOT_SIGNED",
            "M_H_ref and Pi_M^H defined from parent Hamiltonian charge before readout",
            "projector can select the wrong object",
        ),
        (
            "PO2152_1_edge_mass_independence",
            "edge charge has no same-frame source-mass dependence",
            "partial Q_edge^H(lambda)/partial M_H_ref |_{tau,reference,surface}=0",
            "NOT_DERIVED",
            "Q_edge depends only on fixed boundary cohomology/gauge data, not source worldtube data",
            "Qbar_edge_XH(lambda) remains live",
        ),
        (
            "PO2152_2_symplectic_block",
            "source and edge sectors are symplectically orthogonal",
            "Omega(delta_M Phi,delta_edge Phi)=0 and Pi_M^H[delta_edge Q]=0",
            "NOT_DERIVED",
            "block-diagonal reduced symplectic form or exact mixed term",
            "edge/source mixing feeds FB5540 or R10/R11",
        ),
        (
            "PO2152_3_reference_silence",
            "reference subtraction does not reroute edge charge into mass readout",
            "Pi_M^H[Delta_ref+Delta_symp+B_class]=0",
            "NOT_SIGNED",
            "B_ref derivative-silent theorem plus boundary class certificate",
            "projector orthogonality broken by reference movement",
        ),
        (
            "PO2152_4_conditional_zero",
            "projector clauses kill edge Hamiltonian source charge",
            "PO2152_0 through PO2152_3 imply Qbar_edge_XH(lambda)=0",
            "CONDITIONAL_THEOREM_ONLY",
            "parent-signed projector definition, mass-independence, block and reference lemmas",
            "cannot zero edge projection row",
        ),
        (
            "PO2152_5_verdict",
            "projector orthogonality kills edge source projection",
            "Pi_M^H[Q_edge]=0 with no reference, tau, or surface leakage",
            "FAIL_CURRENT_CLAIM",
            "PO2152_0 through PO2152_4 signed by same parent action/boundary class",
            "retain Qbar_edge_XH source-pack row",
        ),
    ]
    return [
        row(clause_id=clause_id, claim=claim, mathematical_form=mathematical_form, current_status=current_status, what_would_close=what_would_close, failure_mode=failure_mode)
        for clause_id, claim, mathematical_form, current_status, what_would_close, failure_mode in data
    ]


def domain_certificate_rows() -> list[dict[str, object]]:
    data = [
        (
            "BDC2152_0_surface_manifold",
            "edge surface S_edge",
            "compact oriented smooth codim-2 surface with no active corner boundary",
            "partial S_edge=empty or every corner C has explicit corner charge Q_C",
            "NOT_SIGNED",
            "Stokes zero can hide corner charge",
            "Q_edge_zero;corner_source_row",
        ),
        (
            "BDC2152_1_boundary_class",
            "allowed boundary class B_class",
            "same B_class used by L_X,Q_X,B_ref,Pi_M^H and R10/R11 readout",
            "delta B_class=0 along source variation and no retuning between source/test systems",
            "NOT_SIGNED",
            "reference or boundary class can absorb the signal",
            "FB5540;Qbar_edge_XH",
        ),
        (
            "BDC2152_2_relative_cohomology",
            "relative edge cohomology H_edge",
            "harmonic/non-exact edge class absent or separately measured as h_X",
            "B_X=d_S b_X+h_X with h_X=0, or norm(int_S F_lambda epsilon h_X) source-bounded",
            "NOT_SIGNED",
            "exactness misses a harmonic edge mode",
            "harmonic_edge_bound;Q_edge_zero",
        ),
        (
            "BDC2152_3_allowed_epsilon",
            "epsilon_X domain",
            "epsilon_X is a proper X-representative gauge while physical tau/mass/rotation generators remain admissible",
            "epsilon_X|S_edge=0 or d_S(F_lambda epsilon_X)=0 without constraining tau_source or ADM charges",
            "CLOSURE_ONLY",
            "proper-gauge zero may erase real physical charges",
            "Q_edge_zero;projector_definition",
        ),
        (
            "BDC2152_4_kernel_weight",
            "weighted-Stokes kernel",
            "F_lambda epsilon_X is closed or its derivative norm is source-bounded on S_edge",
            "d_S(F_lambda epsilon_X)=0 or norm_dS_Feps has units/source path",
            "NOT_SIGNED",
            "weighted derivative term survives",
            "edge_bound_terms",
        ),
        (
            "BDC2152_5_verdict",
            "boundary domain certificate",
            "BDC2152_0 through BDC2152_4 signed in one parent boundary class",
            "closed/corner-free plus cohomology plus epsilon/kernel conditions imply no untracked edge domain term",
            "FAIL_CURRENT_CLAIM",
            "Q_edge cannot be set to zero by Stokes alone",
            "B_X_primitive_or_edge_bound",
        ),
    ]
    return [
        row(certificate_id=certificate_id, object=object_name, required_certificate=required_certificate, mathematical_test=mathematical_test, current_status=current_status, failure_if_missing=failure_if_missing, feeds=feeds)
        for certificate_id, object_name, required_certificate, mathematical_test, current_status, failure_if_missing, feeds in data
    ]


def weighted_stokes_rows() -> list[dict[str, object]]:
    data = [
        (
            "ETB2152_0_decomposition",
            "boundary momentum decomposes into exact, harmonic and residual pieces",
            "B_X=d_S b_X+h_X+r_X",
            "FORMAL_DECOMPOSITION",
            "parent L_X/Theta_X/Q_X must prove r_X=0 and identify h_X",
            "norm(Q_edge) keeps norm(int_S F epsilon h_X)+norm(int_S F epsilon r_X)",
        ),
        (
            "ETB2152_1_weighted_identity",
            "weighted Stokes identity exposes the real residual",
            "int_S F epsilon d_S b_X = int_partialS F epsilon b_X - int_S d_S(F epsilon) wedge b_X",
            "EXACT_IDENTITY",
            "boundary/corner and kernel derivative conditions must be signed",
            "corner and derivative norm terms remain",
        ),
        (
            "ETB2152_2_zero_conditions",
            "genuine edge-zero theorem needs exactness, no harmonic/residual/corner terms, and closed weight",
            "partialS=empty, h_X=0, r_X=0, d_S(F epsilon)=0 => Q_edge^H(lambda)=0",
            "CONDITIONAL_THEOREM",
            "all hypotheses unsigned in current MTS",
            "use finite residual bound instead of zero",
        ),
        (
            "ETB2152_3_residual_bound",
            "if exact zero fails, edge charge has a finite source-pack bound",
            "norm(Q_edge(lambda)) <= C_corner + norm_dS_Feps norm_bX + harmonic_edge_abs + residual_edge_abs",
            "BOUND_LAW_STAGED",
            "numeric/source-backed norms for each term and units",
            "first nonclaim source row stores terms with valid_for_claim=false",
        ),
        (
            "ETB2152_4_projector_bound",
            "Hamiltonian/source projection is bounded after M_H_ref and Pi_M norm are owned",
            "norm(Qbar_edge_XH(lambda)) <= norm(Pi_M^H) norm(Q_edge(lambda)) / M_H_ref_min",
            "CONDITIONAL_BOUND",
            "Pi_M^H definition, M_H_ref_min and source-backed Q_edge bound",
            "Qbar_edge_XH remains MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
        ),
        (
            "ETB2152_5_verdict",
            "exact local condition and fallback bound are derived, but not the zero theorem",
            "Q_edge=0 conditional; Q_edge_bound schema-ready; no claim promoted",
            "FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS",
            "B_X primitive, h_X/r_X zero or bounds, kernel derivative bound, corner audit, M_H_ref/Pi_M",
            "move to B_X primitive or first source-bound term",
        ),
    ]
    return [
        row(theorem_id=theorem_id, statement=statement, formula=formula, current_result=current_result, missing_for_claim=missing_for_claim, bound_if_missing=bound_if_missing)
        for theorem_id, statement, formula, current_result, missing_for_claim, bound_if_missing in data
    ]


def source_pack_rows() -> list[dict[str, object]]:
    data = [
        ("SP2152_0_M_H_ref", "M_H_ref", "same-frame Hamiltonian source denominator", "system_id;tau_id;surface;Q_tau_integral;H_ref;M_H_ref;units;reference_rule;source_path;valid_for_claim", "MISSING_STABLE_MH_REF"),
        ("SP2152_1_FB5540_components", "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;symplectic_boundary_flux_over_MH", "componentwise FB5540 numerator rows normalized by M_H_ref", "system_id;component_id;value_abs;M_H_ref;units;source_path;assumptions;valid_for_claim", "MISSING_FB5540_COMPONENT_VALUES"),
        ("SP2152_2_edge_bound_terms", "C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs", "weighted-Stokes bound terms for Q_edge(lambda)", "system_id;lambda;C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim", "MISSING_EDGEBOUND_TERMS"),
        ("SP2152_3_projected_edge_bound", "Qbar_edge_XH_bound(lambda)", "projected edge bound after Pi_M^H norm and M_H_ref_min", "system_id;lambda;PiM_norm;Q_edge_bound;M_H_ref_min;Qbar_edge_XH_bound;units;source_path;valid_for_claim", "MISSING_PIM_NORM_OR_MHREF_MIN"),
        ("SP2152_4_bulk_coefficients", "lambda_X;K_X;Qbar_XH;qbar_XT;alpha_X(lambda)", "bulk residual amplitude if vertical/source-free theorem fails", "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_X;units;source_path;valid_for_claim", "MISSING_BULK_PROJECTION"),
        ("SP2152_5_edge_coefficients", "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge(lambda)", "edge residual amplitude if boundary/projector theorem fails", "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim", "MISSING_EDGE_PROJECTION"),
        ("SP2152_6_total_guard", "alpha_total_guard(lambda)", "absolute no-cancellation envelope across FB5540, bulk X, edge X and R11", "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim", "NOT_COMPUTED_COMPONENTS_MISSING"),
    ]
    return [row(pack_id=pack_id, quantity=quantity, definition=definition, required_columns=required_columns, current_status=current_status) for pack_id, quantity, definition, required_columns, current_status in data]


def route_verdict_rows() -> list[dict[str, object]]:
    data = [
        ("RVT2152_0_boundary_exactness", "derive Q_edge=0 from exact boundary form", "CONDITIONAL_NOT_PROMOTED", "BE2152 clauses plus BDC2152 certificates and ETB2152 zero conditions", "FAIL_CURRENT_CLAIM", "retain edge source-pack rows"),
        ("RVT2152_1_projector_orthogonality", "derive Qbar_edge_XH=0 from mass-projector orthogonality", "CONDITIONAL_NOT_PROMOTED", "PO2152 clauses plus M_H_ref/Pi_M^H owner", "FAIL_CURRENT_CLAIM", "source or bound Pi_M^H[Q_edge]"),
        ("RVT2152_2_weighted_stokes_bound", "finite edge residual bound from derivative/harmonic/corner terms", "BEST_CURRENT_FALLBACK", "C_corner,norm_dS_Feps,norm_bX,harmonic_edge_abs,residual_edge_abs,M_H_ref_min,PiM_norm", "SOURCE_PACK_SCHEMA_READY_NO_VALUES", "2153 B_X primitive or first edge-bound term"),
        ("RVT2152_3_no_double_count", "orthogonal source split prevents duplicate scoring", "GUARD_WRITTEN_NOT_DERIVED", "bulk/edge/FB5540/R11 projectors and source currents", "BLOCKS_CURRENT_CLAIM", "absolute no-cancellation envelope"),
        ("RVT2152_4_verdict", "2152 branch closure", "FAIL_CURRENT_CLAIM_BUT_NARROWS_GAP", "theorem-zero route or complete source pack", "no R10/R11/Newton/local-GR pass", "2153 explicit B_X primitive from parent variation or edge-bound term fill"),
    ]
    return [row(route_id=route_id, route=route_name, status=status, requires=requires, result=result, fallback=fallback) for route_id, route_name, status, requires, result, fallback in data]


def gr_bridge_rows() -> list[dict[str, object]]:
    data = [
        ("GB2152_0_boundary_zero", "boundary exactness route", "CONDITIONAL_NOT_PROMOTED", "BE2152;BDC2152;ETB2152", "B_X primitive, h_X/r_X zero, kernel and corner clauses unsigned"),
        ("GB2152_1_projector_zero", "edge-source projector orthogonality", "CONDITIONAL_NOT_PROMOTED", "PO2152", "Pi_M^H, M_H_ref, source/edge symplectic block and reference silence unsigned"),
        ("GB2152_2_source_pack", "FB5540/bulk/edge/R11 source pack", "SCHEMA_READY_NO_VALUES", "SP2152 rows", "all source-backed numeric/theorem-zero terms missing"),
        ("GB2152_3_Newton_GR", "Newton/local-GR bridge", "BLOCKED", "RVT2152_4", "edge/source leakage and M_H_ref normalization still open"),
        ("GB2152_4_next", "next derivation owner", "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT", "ETB2152_5;1844 B_X primitive audit", "derive explicit b_X primitive or fill first weighted-Stokes bound term"),
    ]
    return [row(status_id=status_id, bridge_piece=bridge_piece, current_status=current_status, evidence=evidence, remaining_gap=remaining_gap) for status_id, bridge_piece, current_status, evidence, remaining_gap in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2152_0_theorem_attempt", "BOUNDARY_PROJECTOR_ROUTE_PRECISE_BUT_NOT_CLOSED", "Stokes/projector arguments can kill edge leakage only after boundary domain, B_X primitive, cohomology, kernel and reference clauses are parent-signed", "derive explicit B_X primitive from parent variation or fill bound terms"),
        ("DEC2152_1_best_gain", "WEIGHTED_STOKES_BOUND_IS_REAL_PROGRESS", "the fallback is now a finite edge-bound law rather than a closure axiom", "stage EDGEBOUND terms if theorem route fails"),
        ("DEC2152_2_source_pack", "NO_CANCELLATION_SOURCE_PACK_REQUIRED_IF_THEOREM_FAILS", "edge, bulk, FB5540 and R11 components cannot cancel while inputs are unknown", "do not run comparators until source pack terms are real"),
        ("DEC2152_3_best_next", "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_NEXT", "without b_X, both the zero theorem and weighted-Stokes bound lack their central object", "2153 B_X primitive from parent variation or first edge-bound term"),
        ("DEC2152_4_claim_policy", "NO_QEDGE_OR_LOCAL_GR_CLAIM", "Q_edge, Qbar_edge_XH, Newton/local-GR, PPN and R10/R11 remain nonclaim", "continue private derivation/test discipline"),
    ]
    return [row(decision_id=decision_id, decision=decision, reason=reason, next_action=next_action) for decision_id, decision, reason, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2152_0_2153",
            next_target="2153-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
            script="scripts/Y5_R2FR_BX_primitive_from_parent_variation_or_edge_bound_term_fill_2153.py",
            objective="Derive the explicit B_X primitive from parent L_X/Theta_X/Q_X and boundary counterterm, or fill the first EDGEBOUND term with source-backed units.",
            forbidden_shortcuts="do not call B_X exact without b_X; do not merge scalar no-hair with Noether edge-charge exactness; do not claim Q_edge zero or local GR; no formalization-workbench edits; no GitHub action",
        )
    ]


def write_branch_copies(weighted: list[dict[str, object]], source_pack: list[dict[str, object]], bridge: list[dict[str, object]], decisions: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2152_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_BOUNDARY_PROJECTOR_2152_NONCLAIM.csv", weighted + source_pack + decisions),
        ("COPY2152_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2152_BOUNDARY_PROJECTOR_NONCLAIM.csv", weighted + bridge),
        ("COPY2152_2_acquisition_queue", QUEUE / "JR2152_BX_PRIMITIVE_OR_EDGEBOUND_QUEUE.csv", next_rows + source_pack),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    projector: list[dict[str, object]],
    domain: list[dict[str, object]],
    stokes: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    routes: list[dict[str, object]],
    bridge: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    boundary_ok = any(item["clause_id"] == "BE2152_5_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM" for item in boundary)
    projector_ok = any(item["clause_id"] == "PO2152_5_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM" for item in projector)
    domain_ok = {"BDC2152_0_surface_manifold", "BDC2152_2_relative_cohomology", "BDC2152_4_kernel_weight", "BDC2152_5_verdict"}.issubset({str(item["certificate_id"]) for item in domain})
    stokes_ok = any(item["theorem_id"] == "ETB2152_5_verdict" and item["current_result"] == "FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS" for item in stokes)
    source_pack_ok = {"SP2152_0_M_H_ref", "SP2152_2_edge_bound_terms", "SP2152_6_total_guard"}.issubset({str(item["pack_id"]) for item in source_pack}) and all(not truthy(item.get("valid_for_claim", False)) for item in source_pack)
    routes_ok = any(item["route_id"] == "RVT2152_4_verdict" and item["result"] == "no R10/R11/Newton/local-GR pass" for item in routes)
    bridge_ok = any(item["status_id"] == "GB2152_4_next" and item["current_status"] == "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT" for item in bridge)
    decisions_ok = any(item["decision"] == "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_NEXT" for item in decisions) and any(item["decision"] == "NO_QEDGE_OR_LOCAL_GR_CLAIM" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2152_0_2153" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for item in source_pack if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, boundary, projector, domain, stokes, source_pack, routes, bridge, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2152_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, boundary_ok, projector_ok, domain_ok, stokes_ok, source_pack_ok, routes_ok, bridge_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2152_00_sources", sources_ok, "2151 handoff and old 1843/1844 frontier validate"),
        ("VAL2152_01_boundary_blocks_claim", boundary_ok, "boundary exactness remains nonclaim"),
        ("VAL2152_02_projector_blocks_claim", projector_ok, "projector orthogonality remains nonclaim"),
        ("VAL2152_03_domain_certificate", domain_ok, "domain certificate covers surface, cohomology, kernel and verdict"),
        ("VAL2152_04_weighted_stokes", stokes_ok, "weighted-Stokes theorem and fallback bound are written"),
        ("VAL2152_05_source_pack_nonclaim", source_pack_ok, "source pack rows are explicit and nonclaim"),
        ("VAL2152_06_route_verdicts", routes_ok, "route verdict blocks R10/R11/Newton/local-GR pass"),
        ("VAL2152_07_bridge", bridge_ok, "bridge selects B_X primitive/edge-bound next"),
        ("VAL2152_08_decisions", decisions_ok, "decisions select B_X primitive and block local claims"),
        ("VAL2152_09_next", next_ok, "next target is 2153 B_X primitive or edge-bound fill"),
        ("VAL2152_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2152_11_csv_parse", csv_ok, "all generated 2152 CSVs parse cleanly"),
        ("VAL2152_12_missing_not_ready", missing_not_ready, "no MISSING_* source-pack row is ready"),
        ("VAL2152_13_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2152_14_formalization_clean", formalization_clean, "formalization-workbench untouched by 2152"),
        ("VAL2152_15_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2152_OVERALL", all_ok, "2152 boundary/projector theorem route is exact but nonclaim; B_X primitive is next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    projector: list[dict[str, object]],
    domain: list[dict[str, object]],
    stokes: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    routes: list[dict[str, object]],
    bridge: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2151, _ = find_line(DOCS["2151"], ["NEXT2151_0_2152"])
    line_1844, _ = find_line(DOCS["1844"], ["PVT1844_5_verdict"])
    content = "\n\n".join(
        [
            "# 2152 - Y5/R2FR Boundary Exactness Projector Orthogonality Or Source Pack",
            "## Current Verdict",
            "2152 does **not** prove `Q_edge=0`, `Qbar_edge_XH=0`, R10/R11, Newton, local GR, PPN, edge-source cancellation, or any public claim.",
            "The useful gain is exact narrowing: boundary leakage is now a weighted-Stokes/projector problem. A zero theorem needs a certified boundary domain, an explicit `B_X=d_S b_X+h_X+r_X` primitive/decomposition, closed kernel weight, source-mass projector ownership, and no reference/tau leakage.",
            f"This follows the current 2151 handoff at line {line_2151} and syncs to the old B_X primitive bottleneck at 1844 line {line_1844}. The next missing object is not rhetoric; it is the actual `b_X` primitive or a complete EDGEBOUND source row.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Boundary Exactness Clauses",
            md_table(boundary, ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode", "valid_for_claim"]),
            "## Projector Orthogonality Clauses",
            md_table(projector, ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode", "valid_for_claim"]),
            "## Boundary Domain Certificate",
            md_table(domain, ["certificate_id", "object", "required_certificate", "mathematical_test", "current_status", "failure_if_missing", "feeds", "valid_for_claim"]),
            "## Weighted Stokes Theorem And Bound",
            md_table(stokes, ["theorem_id", "statement", "formula", "current_result", "missing_for_claim", "bound_if_missing", "valid_for_claim"]),
            "## Source Pack Schema",
            md_table(source_pack, ["pack_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"]),
            "## Route Verdicts",
            md_table(routes, ["route_id", "route", "status", "requires", "result", "fallback", "valid_for_claim"]),
            "## GR Bridge Status",
            md_table(bridge, ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This is a real step toward a derivable local-GR branch because the edge sector is no longer a fog bank. It is a precise weighted-Stokes and source-projector contract. The next hard target is `B_X`/`b_X`; if it cannot be derived, the theory must carry bounded residual edge rows instead of claiming silence.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    boundary = boundary_exactness_rows()
    projector = projector_orthogonality_rows()
    domain = domain_certificate_rows()
    stokes = weighted_stokes_rows()
    source_pack = source_pack_rows()
    routes = route_verdict_rows()
    bridge = gr_bridge_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["boundary_exactness"], boundary)
    write_csv(OUTPUTS["projector_orthogonality"], projector)
    write_csv(OUTPUTS["domain_certificate"], domain)
    write_csv(OUTPUTS["weighted_stokes"], stokes)
    write_csv(OUTPUTS["source_pack"], source_pack)
    write_csv(OUTPUTS["route_verdicts"], routes)
    write_csv(OUTPUTS["gr_bridge"], bridge)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(stokes, source_pack, bridge, decisions, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, boundary, projector, domain, stokes, source_pack, routes, bridge, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, boundary, projector, domain, stokes, source_pack, routes, bridge, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2152 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
