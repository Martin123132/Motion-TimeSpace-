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


DOC = ROOT / "2154-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2153": ROOT / "2153-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
    "2153_validation": OUT / "P8_Y5_BRR545_2153_VALIDATION.csv",
    "2153_next": OUT / "P8_Y5_PARENT_QLOC_2153_NEXT_TARGET.csv",
    "1845": ROOT / "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
    "1845_validation": OUT / "P8_Y5_BRR545_1845_VALIDATION.csv",
    "1846": ROOT / "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
    "1846_validation": OUT / "P8_Y5_BRR545_1846_VALIDATION.csv",
    "1846_next": OUT / "P8_Y5_PARENT_QLOC_1846_NEXT_TARGET.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2154_SOURCE_REGISTER.csv",
    "branch_matrix": OUT / "P8_Y5_PARENT_QLOC_2154_BRANCH_DECISION_MATRIX.csv",
    "qvx_certificate": OUT / "P8_Y5_PARENT_QLOC_2154_QVX_ACTION_DESCENT_CERTIFICATE.csv",
    "coupling_audit": OUT / "P8_Y5_PARENT_QLOC_2154_COUPLING_DESCENT_AUDIT.csv",
    "scalar_input_pack": OUT / "P8_Y5_PARENT_QLOC_2154_SCALAR_NOHAIR_INPUT_PACK.csv",
    "fallback_source_rows": OUT / "P8_Y5_PARENT_QLOC_2154_FALLBACK_SOURCE_ROWS.csv",
    "demotion": OUT / "P8_Y5_PARENT_QLOC_2154_DEMOTION_LEDGER.csv",
    "gr_bridge": OUT / "P8_Y5_PARENT_QLOC_2154_GR_BRIDGE_STATUS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2154_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2154_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2154_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2154_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2154_VALIDATION.csv",
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


def formalization_has_2154_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2154-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2154*",
        "*P8_Y5_BRR545_2154*",
        "*Y5_R2FR_vertical_quotient_LX_construction_or_scalar_nohair_branch_choice_2154*",
        "*AFRAME_VERTICAL_SCALAR_BRANCH_2154*",
        "*JR2154*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2154_00_2153_handoff", DOCS["2153"], [["NEXT2153_0_2154"], ["VERTICAL_QUOTIENT_OR_SCALAR_NOHAIR_BRANCH_CHOICE_IS_NEXT"], ["VAL2153_OVERALL"]], "current 2153 selects quotient-vs-scalar branch choice."),
        ("SRC2154_01_2153_validation", DOCS["2153_validation"], [["VAL2153_OVERALL"], ["PASS"]], "current 2153 validation passed as nonclaim."),
        ("SRC2154_02_2153_next", DOCS["2153_next"], [["NEXT2153_0_2154"], ["vertical quotient"], ["scalar"]], "machine-readable current next target."),
        ("SRC2154_03_1845_branch_choice", DOCS["1845"], [["QVC1845_8_verdict"], ["CDA1845_4_verdict"], ["VAL1845_OVERALL"]], "old 1845 supplies quotient certificate failure and scalar fallback demotion."),
        ("SRC2154_04_1845_validation", DOCS["1845_validation"], [["VAL1845_OVERALL"], ["PASS"]], "old 1845 validation passed as nonclaim."),
        ("SRC2154_05_1846_scalar_pack", DOCS["1846"], [["SIA1846_7_verdict"], ["DEC1846_3_next_target"], ["VAL1846_OVERALL"]], "old 1846 gives scalar no-hair input pack and residual alpha runner refusal."),
        ("SRC2154_06_1846_validation", DOCS["1846_validation"], [["VAL1846_OVERALL"], ["PASS"]], "old 1846 validation passed as nonclaim."),
        ("SRC2154_07_1846_next", DOCS["1846_next"], [["NEXT1846_0_primary"], ["Xhat"], ["Hessian"]], "old 1846 selects parent Xhat/Hessian/range owner as the next scalar route."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def branch_matrix_rows() -> list[dict[str, object]]:
    data = [
        ("BDM2154_0_vertical_quotient", "quotient/vertical removal before variation", "q, v_X, action descent, matter descent, boundary silence and degree count close together", "least_post_hoc_if_successful", "TESTED_NOT_CLOSED", "single parent certificate for field-by-field vertical action and descended matter/boundary terms", "demote current local branch; keep quotient route as future parent-action theorem target"),
        ("BDM2154_1_scalar_nohair", "positive scalar no-hair/source-free local silence", "Z_X>0, M_X^2>=0, J_X=0 and boundary_flux_X=0 imply X=0 in compact exterior", "honest_fallback_if_coefficients_are_real", "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM", "Z_X, M_X2, J_X, boundary flux and lambda_X source rows", "attempt next because it is executable after quotient certificate failure"),
        ("BDM2154_2_finite_residual", "bounded residual coupling/source branch", "K_X, Qbar_XH, qbar_XT, EDGEBOUND, FB5540 and R11 rows form no-cancellation envelope", "empirical_score_route", "FALLBACK_IF_NOHAIR_FAILS", "source-backed coefficient rows and local arena projection", "score residual instead of asserting local silence"),
    ]
    return [row(matrix_id=matrix_id, candidate=candidate, core_test=core_test, scrutiny_level=scrutiny_level, current_status=current_status, missing=missing, decision=decision) for matrix_id, candidate, core_test, scrutiny_level, current_status, missing, decision in data]


def qvx_certificate_rows() -> list[dict[str, object]]:
    data = [
        ("QVC2154_0_parent_q", "parent quotient map q", "q is canonical parent reduction, not post-readout projection; Dq[v_X]=0 for actual local X direction", "prior quotient pieces are conditional and do not identify actual local MTS X variations with the null generator", "PARTIAL_CONDITIONAL", "prove actual local Xhat variations equal the parent null/relative-exact generator", "X is representative data, not a physical local field"),
        ("QVC2154_1_vertical_generator", "field-by-field v_X", "v_X acts on every retained field and coefficient with known degree/signature", "candidate vertical directions exist, but not a current complete action on all fields", "MISSING_FIELD_BY_FIELD_ACTION", "vertical action table for metric, coframe, matter labels, clocks, EM markers and boundary fields", "K_X=qbar_XT=0 can be theorem-owned"),
        ("QVC2154_2_action_descent", "parent action descent", "S_parent[Phi]=Sbar[q(Phi)] plus boundary/reference terms descend", "action descent is conditional and boundary/reference terms remain live", "CONDITIONAL_THEOREM_ONLY", "same parent action supplies L_X, Theta_X, Q_X, B_ct and reference silence", "X has no independent Euler-Lagrange pole"),
        ("QVC2154_3_matter_descent", "ordinary matter quotient functor", "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] and L_vX theta_A=0 for constants/material markers", "metric/frame chain rule can pass conditionally, but constants, EM labels and material markers are not parent-owned", "CONDITIONAL_THEOREM_ONLY", "no-marker constants, EM/material labels, hidden conformal/disformal channel exclusion", "qbar_XT=0 and no ordinary matter X source"),
        ("QVC2154_4_boundary_silence", "boundary/projector descent", "B_X, Pi_M^H[Q_edge], reference shifts and tau readout descend through q or vanish as proper gauge", "2152/2153 leave B_X, Pi_M^H and EDGEBOUND terms unsigned", "NOT_DERIVED", "B_X primitive or complete edge-bound source pack", "Qbar_edge_XH=0 or source-bounded"),
        ("QVC2154_5_momentum_map", "differentiable first-class generator", "delta G_X=Omega(delta Phi,v_X), G_X=int epsilon C_X+Q_X, and bracket closes without active K_boundary", "parent theta/Omega/DC_X/Q_X and edge differentiability remain unsigned", "NOT_DERIVED", "parent symplectic potential, DC_X, Q_X differentiability and algebra closure", "X is constraint/gauge, not physical source field"),
        ("QVC2154_6_degree_count", "degree count/no lost physical data", "quotient removes only representative redundancy and keeps observed metric/source data complete", "no complete parent degree-count table exists", "NOT_DERIVED", "rank/kernel/cokernel table for local fields and observables", "quotient is not over-aggressive closure"),
        ("QVC2154_7_readout_commutation", "local readout commutes with quotient", "Obs(Phi)=Obsbar(q(Phi)) for clocks, rods, EM labels, source mass and local tests", "observed metric chain rule is conditional; EM/clock/material labels remain open", "PARTIAL_CONDITIONAL", "readout functor certificate for all local arenas", "no hidden X readout channel"),
        ("QVC2154_8_verdict", "single q/v_X/action descent certificate", "QVC2154_0 through QVC2154_7 all parent-signed together", "conditional pieces exist, but no single parent certificate closes in active PARENT_QLOC branch", "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH", "q, v_X, action, matter, boundary and degree certificates in one source-backed row", "K_X=qbar_XT=Qbar_XH=0 and local X alpha inactive"),
    ]
    return [row(certificate_id=certificate_id, required_object=required_object, pass_condition=pass_condition, current_evidence=current_evidence, current_status=current_status, missing_for_claim=missing_for_claim, claim_effect_if_signed=claim_effect_if_signed) for certificate_id, required_object, pass_condition, current_evidence, current_status, missing_for_claim, claim_effect_if_signed in data]


def coupling_audit_rows() -> list[dict[str, object]]:
    data = [
        ("CDA2154_0_metric_frame", "observed metric/coframe", "CONDITIONAL_PASS_SHAPE", "if Obs factors through q then metric/coframe response can be vertical-silent", "needs parent readout functor", "do not claim full quotient from metric-only chain rule"),
        ("CDA2154_1_constants_markers", "theta_A constants/material labels", "NOT_CLOSED", "L_vX theta_A is not parent-owned for EM, clocks, masses or material labels", "constant/material marker X-dependence", "retain clock/EM/WEP source rows"),
        ("CDA2154_2_hidden_frame", "hidden conformal/disformal X channel", "COUNTEREXAMPLE_FILTER_ONLY", "hidden X-frame dependence is observable unless it factors through q or is finite-coupled", "F_X prime or disformal coefficient if present", "source/coefficient pack required"),
        ("CDA2154_3_projector_boundary", "projector/boundary coupling", "OPEN", "B_X, Pi_M^H[Q_edge], K_boundary and source split remain unsigned", "edge/source projection into measured Hamiltonian mass", "retain EDGEBOUND and Qbar_edge rows"),
        ("CDA2154_4_verdict", "coupling descent verdict", "COUPLING_NOT_THEOREM_ZERO", "matter descent and boundary/projector descent are conditional, not parent-signed", "qbar_XT;Qbar_XH;edge terms;clock/WEP channels", "move to scalar no-hair/source coefficient input pack"),
    ]
    return [row(audit_id=audit_id, object=object_name, result=result, reason=reason, remaining_coupling=remaining_coupling, demotion_effect=demotion_effect) for audit_id, object_name, result, reason, remaining_coupling, demotion_effect in data]


def scalar_input_pack_rows() -> list[dict[str, object]]:
    data = [
        ("SNH2154_0_Z_X", "Z_X", "positive kinetic term", "parent Hessian second variation with field units", "MISSING_PARENT_INPUT", "no scalar no-hair theorem; score residual"),
        ("SNH2154_1_M_X2", "M_X^2", "positive mass gap/no zero mode", "parent Hessian curvature and zero-mode handling", "MISSING_PARENT_INPUT", "long-range scalar/residual alpha remains"),
        ("SNH2154_2_J_X_zero", "J_X=0", "source-free exterior equation", "matter/hidden/source variation proof or sourced current bound", "MISSING_SOURCE_ZERO_PROOF", "qbar_XT/source coupling row required"),
        ("SNH2154_3_boundary_flux_zero", "boundary_flux_X=0", "positive energy identity RHS", "parent boundary condition or EDGEBOUND zero/bound row", "MISSING_BOUNDARY_LOCK", "edge residual rows required"),
        ("SNH2154_4_lambda_X", "lambda_X=sqrt(Z_X/M_X^2)", "range for local tests", "Z_X/M_X2 units and normalization", "MISSING_RANGE_OWNER", "no R10/R11 alpha range"),
        ("SNH2154_5_alpha_coefficients", "K_X;Qbar_XH;qbar_XT;lambda_X", "R10/R11 residual scoring if no-hair fails", "source-normalized coefficient rows with units and no-cancellation envelope", "MISSING_ARENA_PROJECTION", "no local empirical pass"),
    ]
    return [row(input_id=input_id, quantity=quantity, needed_for=needed_for, required_source=required_source, current_status=current_status, if_missing=if_missing) for input_id, quantity, needed_for, required_source, current_status, if_missing in data]


def fallback_source_rows() -> list[dict[str, object]]:
    data = [
        ("FBR2154_0_quotient_certificate", "q_vX_action_matter_boundary_certificate", "q_id;vX_id;action_descent;matter_descent;boundary_silence;degree_count;source_path;valid_for_claim", "MISSING_CERTIFICATE", "quotient/vertical route is reopened"),
        ("FBR2154_1_scalar_operator_pack", "Z_X;M_X2;J_X;boundary_flux_X;lambda_X", "system_id;Z_X;M_X2;J_X;boundary_flux_X;lambda_X;units;source_path;valid_for_claim", "MISSING_PARENT_INPUT", "scalar no-hair route selected next"),
        ("FBR2154_2_sourced_alpha_pack", "K_X;Qbar_XH;qbar_XT;alpha_X(lambda)", "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_X;units;source_path;valid_for_claim", "MISSING_ARENA_PROJECTION", "scalar/source route remains nonzero"),
        ("FBR2154_3_edge_bound_pack", "EDGEBOUND terms", "C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim", "MISSING_EDGE_BOUND_TERMS", "boundary/edge charge route remains live"),
        ("FBR2154_4_total_guard", "absolute no-cancellation envelope", "abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_R11;component_sum_abs;source_path;valid_for_claim", "NOT_COMPUTED_COMPONENTS_MISSING", "any finite residual scoring"),
    ]
    return [row(row_id=row_id, quantity=quantity, required_columns=required_columns, current_status=current_status, used_if=used_if) for row_id, quantity, required_columns, current_status, used_if in data]


def demotion_rows() -> list[dict[str, object]]:
    data = [
        ("DEM2154_0_scope", "current quotient/vertical no-pole route", "DEMOTED_TO_CONDITIONAL_ONLY_FOR_CURRENT_MTS", "the single certificate fails at field-by-field v_X, action descent, matter/no-marker descent, boundary silence and degree count", "conditional theorem target for a future parent action"),
        ("DEM2154_1_scalar_operator", "scalar no-hair fallback", "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM", "it is now the honest executable route after the quotient certificate fails in current files", "positive energy identity if Z_X, M_X2, J_X and boundary flux are sourced"),
        ("DEM2154_2_sourced_residual", "finite coupling/source branch", "RETAINED_AS_SCOREABLE_IF_SCALAR_NOHAIR_FAILS", "nonzero J_X or matter coupling must be tested rather than hidden", "R10/R11 alpha/source-bound runner"),
        ("DEM2154_3_claim_ceiling", "local-GR/R10/R11 local silence", "BLOCKED", "no theorem-zero branch or valid source-bound branch closes", "discipline: no public/local claim from this branch yet"),
    ]
    return [row(demotion_id=demotion_id, demoted_object=demoted_object, demotion=demotion, reason=reason, what_survives=what_survives) for demotion_id, demoted_object, demotion, reason, what_survives in data]


def gr_bridge_rows() -> list[dict[str, object]]:
    data = [
        ("GB2154_0_quotient_no_pole", "remove local X before variation", "CERTIFICATE_FAILS_CURRENT_BRANCH", "QVC2154_8_verdict", "single parent q/v_X/action/matter/boundary/degree certificate"),
        ("GB2154_1_matter_coupling", "ordinary matter/marker descent", "COUPLING_NOT_ZERO", "CDA2154_4_verdict", "constants, EM/material labels and hidden frame channels"),
        ("GB2154_2_scalar_nohair", "positive scalar no-hair fallback", "NEXT_INPUT_TARGET_NOT_CLAIM", "SNH2154_0_Z_X through SNH2154_5_alpha_coefficients", "Z_X, M_X2, J_X, boundary_flux_X, lambda_X and alpha rows"),
        ("GB2154_3_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED", "no quotient no-pole theorem and no scalar no-hair theorem", "derive theorem-zero branch or score bounded residual against local tests"),
        ("GB2154_4_next", "next derivation owner", "SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT", "DEC2154_3_next_target;NEXT2154_0_primary", "try positive energy/no-hair route with real inputs; otherwise score residual"),
    ]
    return [row(status_id=status_id, bridge_piece=bridge_piece, current_status=current_status, evidence=evidence, remaining_gap=remaining_gap) for status_id, bridge_piece, current_status, evidence, remaining_gap in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2154_0_sources_registered", "2154 source chain exists", False, "sources prove audit continuity only, not quotient closure"),
        ("CG2154_1_quotient_no_pole", "X is quotient/vertical and absent before variation", False, "QVC2154_8 fails because action, matter, boundary and degree clauses are unsigned"),
        ("CG2154_2_coupling_zero", "local coupling/source projection is zero", False, "CDA2154_4 keeps qbar_XT/Qbar_XH/edge channels live"),
        ("CG2154_3_scalar_nohair", "scalar no-hair local silence", False, "scalar input pack lacks Z_X, M_X2, J_X and boundary flux proof"),
        ("CG2154_4_residual_score", "bounded residual passes local tests", False, "fallback source rows and arena projections are missing"),
        ("CG2154_5_local_GR_Newton", "local GR/Newton reduction follows", False, "no theorem-zero branch or valid source-bound branch closes"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2154_0_certificate_result", "The q/v_X/action descent certificate does not close for the active PARENT_QLOC branch.", "conditional quotient pieces exist, but no field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence or degree count is signed.", "do not spend no-pole credit from quotient route"),
        ("DEC2154_1_demotion", "Demote the current local branch to scalar no-hair/source-coefficient work.", "this is the honest executable route after the quotient certificate fails in current files.", "try to fill or reject Z_X, M_X2, J_X=0, boundary_flux_X=0 and alpha coefficients"),
        ("DEC2154_2_future_reopen", "The quotient route can be reopened only by a real parent action certificate.", "future q/v_X proof would still be the cleanest local-GR route if it supplies all missing clauses together.", "require q, v_X, action descent, matter descent, boundary silence and degree count in one source-backed row"),
        ("DEC2154_3_next_target", "Next target is scalar no-hair input pack or residual alpha coefficient runner.", "Z_X, M_X2, J_X=0, boundary_flux_X=0, lambda_X and alpha coefficients are now the executable local branch inputs.", "2155-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, reason=reason, next_action=next_action) for decision_id, decision, reason, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2154_0_2155",
            next_target="2155-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
            script="scripts/Y5_R2FR_scalar_nohair_input_pack_or_residual_alpha_coefficient_runner_2155.py",
            objective="Fill or reject the scalar no-hair input pack: Z_X, M_X^2, J_X=0, boundary_flux_X=0, lambda_X and fallback alpha coefficients with units and source paths.",
            selection_status="selected",
            success_condition="positive no-hair theorem is sourced without post-hoc boundary choices, or scalar branch is demoted to explicit residual alpha rows",
        ),
        row(
            route_id="NEXT2154_1_future_reopen",
            next_target="2155b-Y5-R2FR-parent-action-q-vX-certificate-reopen.md",
            script="scripts/Y5_R2FR_parent_action_q_vX_certificate_reopen_2155b.py",
            objective="Reopen quotient route only if a single parent action supplies q, v_X, action descent, matter descent, boundary silence and degree count.",
            selection_status="held",
            success_condition="one parent certificate replaces the conditional quotient ledger",
        ),
    ]


def write_branch_copies(matrix: list[dict[str, object]], qvx: list[dict[str, object]], scalar: list[dict[str, object]], bridge: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2154_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_VERTICAL_SCALAR_BRANCH_2154_NONCLAIM.csv", matrix + qvx),
        ("COPY2154_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2154_VERTICAL_SCALAR_NONCLAIM.csv", qvx + bridge),
        ("COPY2154_2_acquisition_queue", QUEUE / "JR2154_SCALAR_NOHAIR_OR_QVX_REOPEN_QUEUE.csv", next_rows + scalar),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    matrix: list[dict[str, object]],
    qvx: list[dict[str, object]],
    coupling: list[dict[str, object]],
    scalar: list[dict[str, object]],
    fallback: list[dict[str, object]],
    demotion: list[dict[str, object]],
    bridge: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    matrix_ok = any(item["matrix_id"] == "BDM2154_0_vertical_quotient" and item["current_status"] == "TESTED_NOT_CLOSED" for item in matrix)
    qvx_ok = any(item["certificate_id"] == "QVC2154_8_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH" for item in qvx)
    coupling_ok = any(item["audit_id"] == "CDA2154_4_verdict" and item["result"] == "COUPLING_NOT_THEOREM_ZERO" for item in coupling)
    scalar_ok = {"SNH2154_0_Z_X", "SNH2154_1_M_X2", "SNH2154_2_J_X_zero", "SNH2154_3_boundary_flux_zero"}.issubset({str(item["input_id"]) for item in scalar}) and all(not truthy(item.get("valid_for_claim", False)) for item in scalar)
    fallback_ok = {"FBR2154_0_quotient_certificate", "FBR2154_1_scalar_operator_pack", "FBR2154_4_total_guard"}.issubset({str(item["row_id"]) for item in fallback}) and all(not truthy(item.get("valid_for_claim", False)) for item in fallback)
    demotion_ok = any(item["demotion_id"] == "DEM2154_0_scope" and item["demotion"] == "DEMOTED_TO_CONDITIONAL_ONLY_FOR_CURRENT_MTS" for item in demotion) and any(item["demotion_id"] == "DEM2154_1_scalar_operator" and item["demotion"] == "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM" for item in demotion)
    bridge_ok = any(item["status_id"] == "GB2154_4_next" and item["current_status"] == "SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT" for item in bridge)
    gates_ok = all(not truthy(item.get("gate_pass", False)) and not truthy(item.get("claim_allowed", False)) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2154_3_next_target" and "scalar no-hair" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2154_0_2155" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for group in (scalar, fallback) for item in group if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, matrix, qvx, coupling, scalar, fallback, demotion, bridge, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2154_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, matrix_ok, qvx_ok, coupling_ok, scalar_ok, fallback_ok, demotion_ok, bridge_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2154_00_sources", sources_ok, "2153 handoff and old 1845/1846 frontier validate"),
        ("VAL2154_01_branch_matrix_demotes", matrix_ok, "branch matrix tests quotient first but does not claim it"),
        ("VAL2154_02_qvx_certificate_blocks_claim", qvx_ok, "q/v_X/action certificate fails current claim"),
        ("VAL2154_03_coupling_not_theorem_zero", coupling_ok, "coupling descent remains nonzero/nonclaim"),
        ("VAL2154_04_scalar_pack_nonclaim", scalar_ok, "scalar no-hair input pack exists and remains nonclaim"),
        ("VAL2154_05_fallback_rows_nonclaim", fallback_ok, "fallback source rows are explicit and nonclaim"),
        ("VAL2154_06_demotion_complete", demotion_ok, "demotion ledger covers quotient and scalar fallback"),
        ("VAL2154_07_bridge_next", bridge_ok, "bridge status selects scalar no-hair/residual runner next"),
        ("VAL2154_08_claim_gates_blocked", gates_ok, "all claim gates remain blocked"),
        ("VAL2154_09_decision_next", decisions_ok, "decision ledger selects scalar no-hair input pack next"),
        ("VAL2154_10_next", next_ok, "next target selected"),
        ("VAL2154_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2154_12_csv_parse", csv_ok, "all generated 2154 CSVs parse cleanly"),
        ("VAL2154_13_missing_not_ready", missing_not_ready, "MISSING_* rows stay nonclaim"),
        ("VAL2154_14_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2154_15_formalization_clean", formalization_clean, "formalization-workbench untouched by 2154"),
        ("VAL2154_16_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2154_OVERALL", all_ok, "2154 demotes quotient route for current files and selects scalar no-hair/residual alpha next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    matrix: list[dict[str, object]],
    qvx: list[dict[str, object]],
    coupling: list[dict[str, object]],
    scalar: list[dict[str, object]],
    fallback: list[dict[str, object]],
    demotion: list[dict[str, object]],
    bridge: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2153, _ = find_line(DOCS["2153"], ["NEXT2153_0_2154"])
    line_1846, _ = find_line(DOCS["1846"], ["SIA1846_7_verdict"])
    content = "\n\n".join(
        [
            "# 2154 - Y5/R2FR Vertical Quotient L_X Construction Or Scalar No-Hair Branch Choice",
            "## Current Verdict",
            "2154 does **not** prove quotient no-pole, coupling-zero, scalar no-hair, R10/R11, PPN, local GR/Newton, or any public claim.",
            "The clean quotient move is tested first because it is the least post-hoc route: remove the local `X` branch before variation. Current files do not close the single `q/v_X/action/matter/boundary/degree` certificate, so that credit cannot be spent.",
            f"This follows the current 2153 handoff at line {line_2153} and syncs to the old scalar input failure at 1846 line {line_1846}. The executable next branch is scalar no-hair with real `Z_X`, `M_X^2`, `J_X=0`, boundary flux and alpha rows.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Branch Decision Matrix",
            md_table(matrix, ["matrix_id", "candidate", "core_test", "scrutiny_level", "current_status", "missing", "decision", "valid_for_claim"]),
            "## q/v_X Action Descent Certificate",
            md_table(qvx, ["certificate_id", "required_object", "pass_condition", "current_evidence", "current_status", "missing_for_claim", "claim_effect_if_signed", "valid_for_claim"]),
            "## Coupling Descent Audit",
            md_table(coupling, ["audit_id", "object", "result", "reason", "remaining_coupling", "demotion_effect", "valid_for_claim"]),
            "## Scalar No-Hair Input Pack",
            md_table(scalar, ["input_id", "quantity", "needed_for", "required_source", "current_status", "if_missing", "valid_for_claim"]),
            "## Fallback Source Rows",
            md_table(fallback, ["row_id", "quantity", "required_columns", "current_status", "used_if", "valid_for_claim"]),
            "## Demotion Ledger",
            md_table(demotion, ["demotion_id", "demoted_object", "demotion", "reason", "what_survives", "valid_for_claim"]),
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
            "This is the least flattering but most useful answer: the clean quotient move remains the best theoretical route, but current MTS cannot spend that credit yet. So the next honest derivation is the positive-energy/no-hair branch: prove the scalar operator is positive and source-free, or admit a residual coupling and score it. That is how we avoid smuggling GR in through a hidden closure axiom.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    matrix = branch_matrix_rows()
    qvx = qvx_certificate_rows()
    coupling = coupling_audit_rows()
    scalar = scalar_input_pack_rows()
    fallback = fallback_source_rows()
    demotion = demotion_rows()
    bridge = gr_bridge_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["branch_matrix"], matrix)
    write_csv(OUTPUTS["qvx_certificate"], qvx)
    write_csv(OUTPUTS["coupling_audit"], coupling)
    write_csv(OUTPUTS["scalar_input_pack"], scalar)
    write_csv(OUTPUTS["fallback_source_rows"], fallback)
    write_csv(OUTPUTS["demotion"], demotion)
    write_csv(OUTPUTS["gr_bridge"], bridge)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(matrix, qvx, scalar, bridge, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, matrix, qvx, coupling, scalar, fallback, demotion, bridge, gates, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, matrix, qvx, coupling, scalar, fallback, demotion, bridge, gates, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2154 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
