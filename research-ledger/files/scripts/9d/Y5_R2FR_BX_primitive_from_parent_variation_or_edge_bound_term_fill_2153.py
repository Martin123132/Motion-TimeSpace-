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


DOC = ROOT / "2153-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2152": ROOT / "2152-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
    "2152_validation": OUT / "P8_Y5_BRR545_2152_VALIDATION.csv",
    "2152_next": OUT / "P8_Y5_PARENT_QLOC_2152_NEXT_TARGET.csv",
    "1844": ROOT / "1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
    "1844_validation": OUT / "P8_Y5_BRR545_1844_VALIDATION.csv",
    "1845": ROOT / "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
    "1845_validation": OUT / "P8_Y5_BRR545_1845_VALIDATION.csv",
    "1845_next": OUT / "P8_Y5_PARENT_QLOC_1845_NEXT_TARGET.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2153_SOURCE_REGISTER.csv",
    "parent_variation": OUT / "P8_Y5_PARENT_QLOC_2153_PARENT_VARIATION_TEMPLATE.csv",
    "primitive_gates": OUT / "P8_Y5_PARENT_QLOC_2153_BX_PRIMITIVE_GATES.csv",
    "scalar_branch": OUT / "P8_Y5_PARENT_QLOC_2153_SCALAR_BRANCH_SEPARATION.csv",
    "edge_bound_fill": OUT / "P8_Y5_PARENT_QLOC_2153_EDGE_BOUND_FILL_SCHEMA.csv",
    "route_verdicts": OUT / "P8_Y5_PARENT_QLOC_2153_ROUTE_VERDICTS.csv",
    "gr_bridge": OUT / "P8_Y5_PARENT_QLOC_2153_GR_BRIDGE_STATUS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2153_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2153_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2153_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2153_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2153_VALIDATION.csv",
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


def formalization_has_2153_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2153-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2153*",
        "*P8_Y5_BRR545_2153*",
        "*Y5_R2FR_BX_primitive_from_parent_variation_or_edge_bound_term_fill_2153*",
        "*AFRAME_BX_PRIMITIVE_2153*",
        "*JR2153*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2153_00_2152_handoff",
            DOCS["2152"],
            [["NEXT2152_0_2153"], ["ETB2152_5_verdict"], ["VAL2152_OVERALL"]],
            "current 2152 selects B_X primitive or edge-bound fill.",
        ),
        (
            "SRC2153_01_2152_validation",
            DOCS["2152_validation"],
            [["VAL2152_OVERALL"], ["PASS"]],
            "current 2152 validation passed as nonclaim.",
        ),
        (
            "SRC2153_02_2152_next",
            DOCS["2152_next"],
            [["NEXT2152_0_2153"], ["B_X primitive"]],
            "machine-readable current next target.",
        ),
        (
            "SRC2153_03_1844_BX",
            DOCS["1844"],
            [["PVT1844_5_verdict"], ["BXG1844_5_verdict"], ["R1844_3_verdict"]],
            "old 1844 supplies the parent-variation/primitive gate and failure mode.",
        ),
        (
            "SRC2153_04_1844_validation",
            DOCS["1844_validation"],
            [["VAL1844_OVERALL"], ["PASS"]],
            "old 1844 validation passed as nonclaim.",
        ),
        (
            "SRC2153_05_1845_branch_choice",
            DOCS["1845"],
            [["QVC1845_8_verdict"], ["DEC1845_3_next_target"], ["VAL1845_OVERALL"]],
            "old 1845 shows quotient route fails current files and scalar/source pack becomes next executable target.",
        ),
        (
            "SRC2153_06_1845_validation",
            DOCS["1845_validation"],
            [["VAL1845_OVERALL"], ["PASS"]],
            "old 1845 validation passed as nonclaim.",
        ),
        (
            "SRC2153_07_1845_next",
            DOCS["1845_next"],
            [["NEXT1845_0_primary"], ["scalar-nohair"], ["residual-alpha"]],
            "old 1845 selects scalar no-hair input pack/residual alpha runner after quotient demotion.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def parent_variation_rows() -> list[dict[str, object]]:
    data = [
        (
            "PVT2153_0_parent_first_variation",
            "parent X-sector first variation",
            "delta L_X = E_A^X delta X^A + d Theta_X(Phi,delta X)",
            "L_X, field normalization, source coupling, and boundary terms are all parent-signed before local readout",
            "FORMULA_TRANSFERRED_NOT_PARENT_SIGNED",
            "variation algebra is available but not a derivation of the MTS edge primitive",
        ),
        (
            "PVT2153_1_vertical_Noether_route",
            "vertical/gauge branch",
            "delta_epsilon X^A=R_i^A epsilon^i+R_i^{A mu} nabla_mu epsilon^i; J_epsilon=Theta_X(delta_epsilon X)-mu_epsilon=dQ_epsilon+epsilon C_X",
            "vertical generator is actual parent gauge direction and not a fitted local closure",
            "VERTICAL_GENERATOR_UNSIGNED",
            "Noether edge silence cannot be claimed yet",
        ),
        (
            "PVT2153_2_boundary_covector",
            "boundary adjoint covector",
            "B_DC[X,deltaY]=-int_S n_mu X_nu delta P^{mu nu}+delta Q_X+density/reference terms",
            "delta Q_X cancels every boundary covector or remaining covectors are explicitly bounded",
            "COVECTOR_OWNER_MISSING",
            "edge source cannot be zeroed by exactness words without a primitive",
        ),
        (
            "PVT2153_3_BX_definition",
            "edge boundary momentum",
            "B_X := i_S^*(n_mu P_X^{mu nu} epsilon_nu + B_ct[epsilon]) as a surface top form",
            "P_X and B_ct are fixed by the same parent action and reference principle",
            "DEFINITION_WRITTEN_PRIMITIVE_NOT_DERIVED",
            "B_X is the immediate derivation bottleneck",
        ),
        (
            "PVT2153_4_hodge_decomposition",
            "surface decomposition",
            "B_X=d_S b_X+h_X+r_X on S_edge",
            "derive b_X and show h_X=r_X=0, or source-bound all three terms",
            "DECOMPOSITION_CONTRACT_READY",
            "weighted-Stokes bound has a precise algebraic slot but no numeric/source-backed payload",
        ),
        (
            "PVT2153_5_verdict",
            "parent variation to primitive map",
            "parent L_X/Theta_X/Q_X -> P_X,B_ct -> B_X -> d_S b_X+h_X+r_X -> Q_edge bound",
            "every arrow is parent-signed or theorem-zero, with no missing edge-bound term",
            "MAP_WRITTEN_NOT_CLOSED",
            "B_X primitive is not derived in current MTS",
        ),
    ]
    return [row(template_id=template_id, object=object_name, formula=formula, closure_test=closure_test, current_status=current_status, implication=implication) for template_id, object_name, formula, closure_test, current_status, implication in data]


def primitive_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "BXG2153_0_same_parent_origin",
            "P_X, J_X, Theta_X, Q_X, Omega_X, and B_ct all come from one parent L_X",
            "compare adjoint operator, Noether current, symplectic form, and counterterm from the same action",
            "FAIL_CURRENT_CLAIM",
            "single signed parent sector action with source normalization and boundary reference",
            "B_X can be an assembled closure rather than a derived primitive",
        ),
        (
            "BXG2153_1_counterterm_owner",
            "B_ct is fixed before readout",
            "delta(Q_X+B_ct)-i_epsilon Theta_X has no uncancelled boundary covector",
            "NOT_DERIVED",
            "differentiability/reference principle for the X-sector boundary class",
            "reference/counterterm can accidentally absorb source calibration",
        ),
        (
            "BXG2153_2_exact_surface_pullback",
            "i_S^*B_X-h_X is exact on S_edge",
            "construct b_X with B_X-h_X=d_S b_X and verify patch overlap compatibility",
            "NOT_DERIVED",
            "explicit b_X primitive or theorem bounding norm_bX",
            "weighted-Stokes exact route remains conditional",
        ),
        (
            "BXG2153_3_harmonic_zero",
            "harmonic/cohomology edge class vanishes or is bounded",
            "Pi_Hedge[B_X]=0, or h_X coefficient bound is source-backed",
            "MISSING_COHOMOLOGY_PROOF_OR_BOUND",
            "boundary cohomology certificate plus source-backed harmonic bound",
            "closed edge classes can feed R10/R11",
        ),
        (
            "BXG2153_4_kernel_norm",
            "d_S(F_lambda epsilon_X) is zero or bounded",
            "closed weight on S_edge, or source-backed norm_dS_Feps",
            "MISSING_KERNEL_DERIVATIVE_BOUND",
            "edge geometry, lambda support, allowed epsilon_X domain",
            "even exact B_X leaves a weighted derivative residual",
        ),
        (
            "BXG2153_5_verdict",
            "B_X primitive closure",
            "BXG2153_0 through BXG2153_4 close together",
            "FAIL_CURRENT_CLAIM",
            "parent-signed primitive or source-backed edge-bound pack",
            "move to vertical quotient construction or scalar/source coefficient fallback",
        ),
    ]
    return [row(gate_id=gate_id, primitive_requirement=primitive_requirement, test=test, current_result=current_result, missing_for_claim=missing_for_claim, if_missing=if_missing) for gate_id, primitive_requirement, test, current_result, missing_for_claim, if_missing in data]


def scalar_branch_rows() -> list[dict[str, object]]:
    data = [
        (
            "SB2153_0_scalar_like_LX",
            "L_X=1/2 sqrt(h)(Z_X |grad X|^2+M_X^2 X^2)-sqrt(h) X J_X",
            "positive operator plus J_X=0 can silence X under selected boundary conditions",
            "this is not a Noether edge-charge primitive unless X is also a gauge/vertical direction",
            "CONDITIONAL_ROUTE_ONLY",
        ),
        (
            "SB2153_1_scalar_boundary_condition",
            "delta X|_S=0 or n.grad X|_S=0 plus positive operator and J_X=0",
            "boundary flux can vanish for a specified boundary-value problem",
            "the parent theory must select these conditions; they cannot be imposed after local data are seen",
            "NOT_PROMOTED",
        ),
        (
            "SB2153_2_scalar_source_route",
            "(-Z_X Delta+M_X^2)X=J_X with Z_X>0 and M_X^2>=0",
            "if J_X=0 and boundary data vanish, X=0 by positive-energy/no-hair argument",
            "requires actual Z_X, M_X^2, J_X and boundary condition from the parent action",
            "MISSING_SOURCE_COEFFICIENTS",
        ),
        (
            "SB2153_3_scalar_verdict",
            "scalar no-hair can be a fallback theorem, not the B_X primitive theorem",
            "separates_routes",
            "do not mix scalar silence with Noether edge-charge exactness",
            "ROUTE_SPLIT_RETAINED",
        ),
    ]
    return [row(branch=branch, formula=formula, boundary_result=boundary_result, warning=warning, status=status) for branch, formula, boundary_result, warning, status in data]


def edge_bound_fill_rows() -> list[dict[str, object]]:
    data = [
        ("EBF2153_0_norm_bX", "norm_bX", "dual norm of the primitive b_X entering |int_S d_S(F epsilon) wedge b_X|", "explicit b_X from P_X/B_ct or a theorem-bound on b_X", "MISSING_BX_PRIMITIVE_OR_BOUND", "edge_charge_units", "MISSING_SOURCE_PATH"),
        ("EBF2153_1_harmonic_edge_abs", "harmonic_edge_abs", "absolute harmonic/cohomology contribution |int_S F epsilon h_X|", "H_edge projection of B_X or no-hair/cohomology theorem", "MISSING_H_EDGE_ZERO_OR_BOUND", "edge_charge_units", "MISSING_SOURCE_PATH"),
        ("EBF2153_2_residual_edge_abs", "residual_edge_abs", "absolute residual/non-exact contribution |int_S F epsilon r_X|", "parent variation residual r_X or source-backed bound", "MISSING_RESIDUAL_ZERO_OR_BOUND", "edge_charge_units", "MISSING_SOURCE_PATH"),
        ("EBF2153_3_norm_dS_Feps", "norm_dS_Feps", "weighted-kernel derivative norm on S_edge", "edge support, lambda kernel and allowed epsilon_X domain", "MISSING_KERNEL_DERIVATIVE_BOUND", "inverse_length_or_surface_units", "MISSING_SOURCE_PATH"),
        ("EBF2153_4_C_corner", "C_corner", "corner/domain contribution in weighted Stokes formula", "corner audit for S_edge or explicit Q_C rows", "MISSING_CORNER_AUDIT_OR_BOUND", "edge_charge_units", "MISSING_SOURCE_PATH"),
        ("EBF2153_5_verdict", "EDGEBOUND fillability", "first executable edge-bound row requires all EBF2153_0 through EBF2153_4", "primitive or numeric/source-backed bound for every term", "NOT_FILLABLE_CURRENTLY", "mixed_missing_units", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2153_EDGE_BOUND_FILL_SCHEMA.csv"),
    ]
    return [row(fill_id=fill_id, quantity=quantity, definition=definition, required_source=required_source, current_status=current_status, units=units, source_path=source_path) for fill_id, quantity, definition, required_source, current_status, units, source_path in data]


def route_verdict_rows() -> list[dict[str, object]]:
    data = [
        ("R2153_0_vertical_gauge_primitive", "derive B_X as a Noether/vertical primitive", "BEST_CLEAN_ROUTE_NOT_CLOSED", "if X is a genuine vertical redundancy, local source poles can disappear before fitting", "construct q, v_X, action descent, matter descent, boundary silence and degree count"),
        ("R2153_1_scalar_nohair_route", "positive scalar/source-free no-hair", "FALLBACK_SEPARATE_ROUTE", "can yield X=0 under signed positivity and source-free boundary data, but it is not an edge primitive", "source Z_X, M_X^2, J_X, boundary conditions and no-hair theorem if quotient route fails"),
        ("R2153_2_edge_bound_fill", "finite edge-bound residual", "FALLBACK_SCHEMA_READY", "weighted-Stokes gives a finite bound once b_X, harmonic, residual, kernel and corner terms are sourced", "fill EDGEBOUND rows as nonclaim source-backed inputs"),
        ("R2153_3_verdict", "B_X primitive checkpoint", "FAIL_CURRENT_CLAIM_BUT_SPLITS_ROUTES", "the primitive map is exact enough to audit but not parent-signed enough to claim", "move to vertical quotient construction or scalar no-hair branch choice"),
    ]
    return [row(route_id=route_id, route=route_name, status=status, because=because, next_step=next_step) for route_id, route_name, status, because, next_step in data]


def gr_bridge_rows() -> list[dict[str, object]]:
    data = [
        ("GB2153_0_BX_primitive", "edge primitive needed for local GR silence", "BLOCKED_NOT_PARENT_SIGNED", "PVT2153_5_verdict;BXG2153_5_verdict", "derive b_X from parent L_X/Theta_X/Q_X/B_ct or source-bound the edge terms"),
        ("GB2153_1_scalar_branch", "positive scalar no-hair local silence", "SEPARATE_FALLBACK_NOT_EDGE_PROOF", "SB2153_3_scalar_verdict", "source Z_X/M_X2/J_X and parent-selected boundary conditions"),
        ("GB2153_2_edge_bound", "finite weighted-Stokes edge residual", "SCHEMA_READY_NO_VALUES", "EBF2153_5_verdict", "source norm_bX, harmonic/residual, kernel and corner bounds"),
        ("GB2153_3_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED", "nonzero or unbounded edge/local source branch still possible", "quotient no-pole theorem or bounded residual small enough for local tests"),
        ("GB2153_4_next", "next derivation owner", "VERTICAL_QUOTIENT_OR_SCALAR_NOHAIR_BRANCH_CHOICE_IS_NEXT", "DEC2153_2_best_next;NEXT2153_0_primary", "choose/test least-scrutiny local branch without mixing routes"),
    ]
    return [row(status_id=status_id, bridge_piece=bridge_piece, current_status=current_status, evidence=evidence, remaining_gap=remaining_gap) for status_id, bridge_piece, current_status, evidence, remaining_gap in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2153_0_sources_registered", "2153 source chain exists", False, "sources exist for audit only; they do not make parent primitive signed"),
        ("CG2153_1_BX_primitive_derived", "B_X=d_S b_X is derived", False, "PVT2153_5 and BXG2153_5 remain fail-current-claim"),
        ("CG2153_2_Qedge_zero", "Q_edge(lambda)=0", False, "exactness, harmonic zero, kernel closure and corner silence are not parent-signed"),
        ("CG2153_3_scalar_nohair", "scalar no-hair local silence", False, "scalar branch is separated and missing Z_X/M_X2/J_X/boundary inputs"),
        ("CG2153_4_edge_bound_executable", "first edge-bound row is executable", False, "EDGEBOUND terms have missing source paths and units"),
        ("CG2153_5_local_GR_Newton", "local GR/Newton reduction follows", False, "extra local branch is neither quotient-removed nor source-bounded"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2153_0_primitive_result", "The explicit B_X primitive is still not derivable from current files.", "The parent L_X/Theta_X/Q_X/P_X/B_ct chain is an audit contract, not a signed parent variation.", "do not claim Q_edge zero; attack the branch-choice theorem directly"),
        ("DEC2153_1_route_split", "Keep gauge-edge and scalar no-hair routes separate.", "Scalar positivity can silence an X field under source-free conditions, but it does not automatically supply a Noether edge primitive.", "test the quotient/vertical construction first, scalar no-hair second"),
        ("DEC2153_2_best_next", "The least-scrutiny route is the vertical quotient construction if it can be built.", "Removing X before variation is cleaner than bounding a leftover local coupling after the fact.", "2154-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"),
        ("DEC2153_3_fallback", "If no quotient/vertical construction closes, fill EDGEBOUND and scalar source coefficients.", "Then MTS survives or fails as a bounded residual theory rather than a theorem-zero local-GR branch.", "fill EBF2153 terms plus Z_X/M_X2/J_X/K_X/Qbar/qbar rows"),
    ]
    return [row(decision_id=decision_id, decision=decision, reason=reason, next_action=next_action) for decision_id, decision, reason, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2153_0_2154",
            next_target="2154-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
            script="scripts/Y5_R2FR_vertical_quotient_LX_construction_or_scalar_nohair_branch_choice_2154.py",
            objective="Choose and test the least-scrutiny local branch: construct X as absent/vertical quotient before variation, or demote to scalar positive no-hair/source-coefficient route.",
            selection_status="selected",
            success_condition="q, v_X, action descent, matter descent, boundary silence and degree count close together, or scalar/source branch is explicitly demoted to nonclaim coefficients",
        )
    ]


def write_branch_copies(parent: list[dict[str, object]], primitive: list[dict[str, object]], edge: list[dict[str, object]], bridge: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2153_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_BX_PRIMITIVE_2153_NONCLAIM.csv", parent + primitive),
        ("COPY2153_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2153_BX_PRIMITIVE_NONCLAIM.csv", primitive + bridge),
        ("COPY2153_2_acquisition_queue", QUEUE / "JR2153_VERTICAL_OR_SCALAR_BRANCH_QUEUE.csv", next_rows + edge),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    parent: list[dict[str, object]],
    primitive: list[dict[str, object]],
    scalar: list[dict[str, object]],
    edge: list[dict[str, object]],
    routes: list[dict[str, object]],
    bridge: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    parent_ok = any(item["template_id"] == "PVT2153_5_verdict" and item["current_status"] == "MAP_WRITTEN_NOT_CLOSED" for item in parent)
    primitive_ok = any(item["gate_id"] == "BXG2153_5_verdict" and item["current_result"] == "FAIL_CURRENT_CLAIM" for item in primitive)
    scalar_ok = any(item["branch"] == "SB2153_3_scalar_verdict" and item["boundary_result"] == "separates_routes" for item in scalar)
    edge_ok = any(item["fill_id"] == "EBF2153_5_verdict" and item["current_status"] == "NOT_FILLABLE_CURRENTLY" for item in edge)
    routes_ok = any(item["route_id"] == "R2153_3_verdict" and item["status"] == "FAIL_CURRENT_CLAIM_BUT_SPLITS_ROUTES" for item in routes)
    bridge_ok = any(item["status_id"] == "GB2153_4_next" and item["current_status"] == "VERTICAL_QUOTIENT_OR_SCALAR_NOHAIR_BRANCH_CHOICE_IS_NEXT" for item in bridge)
    gates_ok = all(not truthy(item.get("gate_pass", False)) and not truthy(item.get("claim_allowed", False)) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2153_2_best_next" and "vertical quotient" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2153_0_2154" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for item in edge if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, parent, primitive, scalar, edge, routes, bridge, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2153_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, parent_ok, primitive_ok, scalar_ok, edge_ok, routes_ok, bridge_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2153_00_sources", sources_ok, "2152 handoff and old 1844/1845 frontier validate"),
        ("VAL2153_01_parent_map_blocks_claim", parent_ok, "parent variation to primitive map remains nonclaim"),
        ("VAL2153_02_primitive_gates_block_claim", primitive_ok, "B_X primitive closure gates remain nonclaim"),
        ("VAL2153_03_scalar_branch_separated", scalar_ok, "scalar no-hair route is separated from Noether primitive route"),
        ("VAL2153_04_edge_bound_not_fillable", edge_ok, "edge-bound first row remains not fillable"),
        ("VAL2153_05_route_verdict", routes_ok, "route verdict splits theorem routes without claim promotion"),
        ("VAL2153_06_bridge_next", bridge_ok, "bridge selects vertical quotient/scalar branch choice next"),
        ("VAL2153_07_claim_gates_blocked", gates_ok, "all claim gates remain blocked"),
        ("VAL2153_08_decision_best_next", decisions_ok, "decision selects least-scrutiny vertical quotient route first"),
        ("VAL2153_09_next", next_ok, "next target is 2154 vertical quotient/scalar branch choice"),
        ("VAL2153_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2153_11_csv_parse", csv_ok, "all generated 2153 CSVs parse cleanly"),
        ("VAL2153_12_missing_not_ready", missing_not_ready, "MISSING_* edge rows stay nonclaim"),
        ("VAL2153_13_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2153_14_formalization_clean", formalization_clean, "formalization-workbench untouched by 2153"),
        ("VAL2153_15_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2153_OVERALL", all_ok, "2153 B_X primitive audit does not close; vertical quotient/scalar branch choice is next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    parent: list[dict[str, object]],
    primitive: list[dict[str, object]],
    scalar: list[dict[str, object]],
    edge: list[dict[str, object]],
    routes: list[dict[str, object]],
    bridge: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2152, _ = find_line(DOCS["2152"], ["NEXT2152_0_2153"])
    line_1845, _ = find_line(DOCS["1845"], ["QVC1845_8_verdict"])
    content = "\n\n".join(
        [
            "# 2153 - Y5/R2FR B_X Primitive From Parent Variation Or Edge-Bound Term Fill",
            "## Current Verdict",
            "2153 does **not** prove `B_X=d_S b_X`, `Q_edge=0`, scalar no-hair local silence, R10/R11, PPN, local GR/Newton, or any public claim.",
            "`B_X` is still not derivable from the current parent files. The checkpoint turns edge leakage into a clean branch choice: vertical quotient removal before variation, scalar no-hair fallback with real inputs, or sourced EDGEBOUND residual rows.",
            f"This follows the current 2152 handoff at line {line_2152} and syncs to the old quotient certificate failure at 1845 line {line_1845}. The least post-hoc path is still quotient/vertical removal, but current MTS cannot spend that credit yet.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Parent Variation Template",
            md_table(parent, ["template_id", "object", "formula", "closure_test", "current_status", "implication", "valid_for_claim"]),
            "## B_X Primitive Gates",
            md_table(primitive, ["gate_id", "primitive_requirement", "test", "current_result", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "## Scalar Branch Separation",
            md_table(scalar, ["branch", "formula", "boundary_result", "warning", "status", "valid_for_claim"]),
            "## Edge Bound Fill Schema",
            md_table(edge, ["fill_id", "quantity", "definition", "required_source", "current_status", "units", "source_path", "valid_for_claim"]),
            "## Route Verdicts",
            md_table(routes, ["route_id", "route", "status", "because", "next_step", "claim_allowed", "valid_for_claim"]),
            "## GR Bridge Status",
            md_table(bridge, ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This is a useful narrowing, not a retreat. The cleanest path to local GR remains removing the extra local branch before variation by proving it is quotient/vertical. Since the primitive is not parent-signed, the next move is to test that quotient route explicitly; if it fails, scalar no-hair or finite residual scoring becomes the honest branch.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    parent = parent_variation_rows()
    primitive = primitive_gate_rows()
    scalar = scalar_branch_rows()
    edge = edge_bound_fill_rows()
    routes = route_verdict_rows()
    bridge = gr_bridge_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_variation"], parent)
    write_csv(OUTPUTS["primitive_gates"], primitive)
    write_csv(OUTPUTS["scalar_branch"], scalar)
    write_csv(OUTPUTS["edge_bound_fill"], edge)
    write_csv(OUTPUTS["route_verdicts"], routes)
    write_csv(OUTPUTS["gr_bridge"], bridge)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(parent, primitive, edge, bridge, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, parent, primitive, scalar, edge, routes, bridge, gates, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, parent, primitive, scalar, edge, routes, bridge, gates, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2153 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
