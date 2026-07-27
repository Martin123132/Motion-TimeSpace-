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


DOC = ROOT / "2155-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2154": ROOT / "2154-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
    "2154_validation": OUT / "P8_Y5_BRR545_2154_VALIDATION.csv",
    "2154_next": OUT / "P8_Y5_PARENT_QLOC_2154_NEXT_TARGET.csv",
    "1846": ROOT / "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
    "1846_validation": OUT / "P8_Y5_BRR545_1846_VALIDATION.csv",
    "1847": ROOT / "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
    "1847_validation": OUT / "P8_Y5_BRR545_1847_VALIDATION.csv",
    "1847_next": OUT / "P8_Y5_PARENT_QLOC_1847_NEXT_TARGET.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2155_SOURCE_REGISTER.csv",
    "scalar_input_assessment": OUT / "P8_Y5_PARENT_QLOC_2155_SCALAR_INPUT_ASSESSMENT.csv",
    "positive_nohair_contract": OUT / "P8_Y5_PARENT_QLOC_2155_POSITIVE_NOHAIR_CONTRACT.csv",
    "parent_owner_audit": OUT / "P8_Y5_PARENT_QLOC_2155_PARENT_SCALAR_OWNER_AUDIT.csv",
    "operator_pack": OUT / "P8_Y5_PARENT_QLOC_2155_POSITIVE_OPERATOR_PACK.csv",
    "source_silence": OUT / "P8_Y5_PARENT_QLOC_2155_SOURCE_SILENCE_AUDIT.csv",
    "alpha_rows": OUT / "P8_Y5_PARENT_QLOC_2155_ALPHA_COEFFICIENT_ROWS.csv",
    "alpha_refusal": OUT / "P8_Y5_PARENT_QLOC_2155_ALPHA_RUNNER_REFUSAL.csv",
    "branch_verdicts": OUT / "P8_Y5_PARENT_QLOC_2155_BRANCH_VERDICTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2155_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2155_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2155_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2155_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2155_VALIDATION.csv",
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


def formalization_has_2155_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2155-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2155*",
        "*P8_Y5_BRR545_2155*",
        "*Y5_R2FR_scalar_nohair_input_pack_or_residual_alpha_coefficient_runner_2155*",
        "*AFRAME_SCALAR_NOHAIR_2155*",
        "*JR2155*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2155_00_2154_handoff", DOCS["2154"], [["NEXT2154_0_2155"], ["SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT"], ["VAL2154_OVERALL"]], "current 2154 selects scalar no-hair/residual alpha route."),
        ("SRC2155_01_2154_validation", DOCS["2154_validation"], [["VAL2154_OVERALL"], ["PASS"]], "current 2154 validation passed as nonclaim."),
        ("SRC2155_02_2154_next", DOCS["2154_next"], [["NEXT2154_0_2155"], ["scalar no-hair"], ["alpha coefficients"]], "machine-readable current scalar route target."),
        ("SRC2155_03_1846_nohair", DOCS["1846"], [["SIA1846_7_verdict"], ["NHC1846_2_zero_result"], ["RUN1846_6_verdict"]], "old 1846 supplies exact conditional no-hair contract and alpha refusal."),
        ("SRC2155_04_1846_validation", DOCS["1846_validation"], [["VAL1846_OVERALL"], ["PASS"]], "old 1846 validation passed as nonclaim."),
        ("SRC2155_05_1847_xhat", DOCS["1847"], [["PX1847_4_verdict"], ["SV1847_6_verdict"], ["PHA1847_8_verdict"]], "old 1847 shows parent Xhat/Hessian owner is next and still unsigned."),
        ("SRC2155_06_1847_validation", DOCS["1847_validation"], [["VAL1847_OVERALL"], ["PASS"]], "old 1847 validation passed as nonclaim."),
        ("SRC2155_07_1847_next", DOCS["1847_next"], [["NEXT1847_0_primary"], ["parent-metric"], ["source-zero"]], "old 1847 selects parent metric/eigenvalue or source-zero return after Xhat/Hessian failure."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def scalar_input_assessment_rows() -> list[dict[str, object]]:
    data = [
        ("SIA2155_0_operator_domain", "O_X self-adjoint positive operator", "O_X=-nabla_i(Z_X nabla^i)+M_X^2 on compact source-free exterior with owned local domain", "positive identity exists as mathematics; parent operator/domain not owned", "TEMPLATE_ONLY", "parent operator, field units, self-adjoint domain and boundary class"),
        ("SIA2155_1_parent_owner", "same Xhat owns visible coefficients and no-hair equation", "one parent-normalized Xhat controls dangerous coupling and obeys L_X Xhat=J_X", "owner audit finds closure-coordinate and theorem-target candidates only", "PARENT_OWNER_NOT_DERIVED", "identify Xhat as action-owned parent field rather than closure coordinate"),
        ("SIA2155_2_Z_X", "Z_X>0", "second variation fixes positive kinetic residue with normalization and units", "operator pack has formula language but no parent-signed Hessian", "MISSING_PARENT_INPUT", "parent Hessian, sign convention, field normalization and units"),
        ("SIA2155_3_M_X2_lambda", "M_X^2>0 and lambda_X", "mass gap is positive and lambda_X=sqrt(Z_X/M_X^2) has source-backed length units", "mass gap and range remain formula-only", "MISSING_PARENT_INPUT", "parent Hessian curvature, zero-mode handling and range units"),
        ("SIA2155_4_J_X_zero", "J_X=0", "ordinary matter plus hidden/source/domain terms are X-blind channel-by-channel", "source silence audit keeps ordinary matter, alpha, WEP, R10 and readout channels live", "MISSING_SOURCE_ZERO_PROOF", "matter quotient/no-marker theorem or explicit source-current bounds"),
        ("SIA2155_5_boundary_flux_zero", "boundary_flux_X=0", "boundary flux is zero/proper/exact or source-backed bounded", "boundary/projector/EDGEBOUND branch remains unsigned", "MISSING_BOUNDARY_LOCK", "boundary class, no-hair/projector silence or flux bound"),
        ("SIA2155_6_energy_identity", "positive energy identity", "int_A(Z_X|grad X|^2+M_X^2 X^2+positive_mix)=int_A XJ_X+Phi_boundary", "conditional no-hair math is valid", "CONDITIONAL_MATH_VALID", "SIA2155_0 through SIA2155_5 together"),
        ("SIA2155_7_verdict", "scalar no-hair theorem", "all scalar input rows parent-signed or source-bounded with zero RHS", "the theorem contract is exact, but every physical owner premise is unsigned", "FAIL_CURRENT_CLAIM", "operator, parent owner, Z_X, M_X^2, J_X=0, boundary_flux_X=0 and no zero-mode gate"),
    ]
    return [row(input_id=input_id, quantity=quantity, required_condition=required_condition, current_evidence=current_evidence, current_status=current_status, missing_for_claim=missing_for_claim) for input_id, quantity, required_condition, current_evidence, current_status, missing_for_claim in data]


def positive_nohair_contract_rows() -> list[dict[str, object]]:
    data = [
        ("NHC2155_0_operator_setup", "retained scalar mode equation", "Let Xhat be the parent-owned retained local mode on compact exterior A with L_X Xhat=J_X.", "CONDITIONAL_CONTRACT", "only applies if Xhat is the same parent field that controls visible coefficients"),
        ("NHC2155_1_energy_identity", "multiply by Xhat and integrate", "int_A[Z_X^{mu nu} nabla_mu Xhat nabla_nu Xhat+M_X^2 Xhat^2+positive_mix] = int_A Xhat J_X + Phi_boundary", "EXACT_CONDITIONAL_IDENTITY", "turns local silence into sign/source/boundary premises rather than a plateau axiom"),
        ("NHC2155_2_zero_result", "set RHS to zero with positive gap/no zero mode", "Z_X>=Z_min>0, M_X^2>=m_min^2>0, J_X=0, Phi_boundary=0 and no zero mode imply Xhat=0 on A.", "EXACT_CONDITIONAL_THEOREM", "would silence the scalar local branch and reopen local-GR route if parent-signed"),
        ("NHC2155_3_failure_branch", "any premise fails", "alpha_X(lambda_X)=K_X Qbar_XH qbar_XT plus edge and FB5540 absolute guard", "FINITE_RESIDUAL_BRANCH", "local tests score the residual instead of accepting a closure"),
        ("NHC2155_4_verdict", "MTS no-hair status", "positive no-hair theorem is derived as mathematics but not activated for MTS", "CONDITIONAL_THEOREM_NOT_MTS_CLAIM", "must derive parent owner/operator/source/boundary clauses first"),
    ]
    return [row(theorem_id=theorem_id, step=step, mathematical_statement=mathematical_statement, status=status, consequence=consequence) for theorem_id, step, mathematical_statement, status, consequence in data]


def parent_owner_audit_rows() -> list[dict[str, object]]:
    data = [
        ("OWN2155_0_target", "parent scalar Xhat/I controlling visible coefficients", "d ln(c_visible)=b_X dXhat and the same Xhat enters L_X Xhat=J_X", "TARGET_SHARP", "not yet identified as a parent field rather than a closure coordinate", "clock, WEP, R10 and local-GR residuals can share one normalization"),
        ("OWN2155_1_chiX", "chi_X finite alpha-pressure coordinate", "chi_X is a parent-owned local field with units and action normalization", "CLOSURE_COORDINATE_ONLY", "visible coefficient response is defined but not tied to parent state variation", "could feed no-hair operator and alpha/WEP projection"),
        ("OWN2155_2_vertical_norm", "parent vertical norm or quotient-fixed scalar", "visible scalar pressure equals a vertical-norm response or quotient-fixed observable", "NOT_DERIVED", "vertical quotient certificate failed in current branch", "could reopen quotient no-pole route rather than scalar no-hair"),
        ("OWN2155_3_clock_coframe", "clock/coframe scalar", "same signed scalar controls observed clock/redshift maps and local source equation", "THEOREM_TARGET_NOT_DERIVED", "clock scalar is not parent-derived and may be gauge/closure if not action-owned", "could connect clock and local no-hair routes"),
        ("OWN2155_4_verdict", "unique parent owner for dangerous scalar coefficient", "one parent-normalized Xhat controls visible coefficients and obeys the no-hair operator", "PARENT_OWNER_NOT_DERIVED", "all candidates are closure coordinates, conditional quotient targets, or unsigned theorem targets", "would unlock the positive no-hair identity as a local-GR route"),
    ]
    return [row(owner_id=owner_id, candidate_owner=candidate_owner, needed_identity=needed_identity, current_status=current_status, why_not_closed=why_not_closed, if_closed=if_closed) for owner_id, candidate_owner, needed_identity, current_status, why_not_closed, if_closed in data]


def operator_pack_rows() -> list[dict[str, object]]:
    data = [
        ("OP2155_0_LX_owner", "parent L_X selected from second variation", "defines the self-adjoint operator acting on the same Xhat that controls visible coefficients", "MISSING_PARENT_LX", "NHC2155_0_operator_setup;SIA2155_0_operator_domain"),
        ("OP2155_1_Z_positive", "Z_X positive kinetic matrix", "makes int Z_X |grad X|^2 nonnegative", "FORMULA_ONLY_NOT_PARENT_SIGNED", "SIA2155_2_Z_X"),
        ("OP2155_2_mass_gap", "M_X^2 positive gap or justified zero-mode handling", "removes long-range scalar zero mode from local exterior", "FORMULA_ONLY_NOT_PARENT_SIGNED", "SIA2155_3_M_X2_lambda"),
        ("OP2155_3_self_adjoint_domain", "self-adjoint local domain and boundary class", "permits integration by parts without hidden leakage", "MISSING_DOMAIN_SIGNATURE", "SIA2155_0_operator_domain;SIA2155_5_boundary_flux_zero"),
        ("OP2155_4_verdict", "positive operator pack", "operator, signs, units, domain and zero-mode handling all parent-owned", "OPERATOR_PACK_UNSIGNED", "blocks scalar no-hair claim and alpha range"),
    ]
    return [row(input_id=input_id, required_input=required_input, mathematical_role=mathematical_role, current_status=current_status, source_basis=source_basis, blocks_claim=True) for input_id, required_input, mathematical_role, current_status, source_basis in data]


def source_silence_rows() -> list[dict[str, object]]:
    data = [
        ("JX2155_0_matter", "ordinary matter/source current", "J_X^matter=0", "CONDITIONAL_ON_PARENT_MATTER_SIGNATURE", "ordinary matter signature/descent is not parent-signed in active branch", "J_X_bound source row"),
        ("JX2155_1_visible_coefficients", "alpha/EM/clock visible coefficient", "partial_X ln(c_visible)=0 or parent-owned coefficient with no local source", "NOT_DERIVED", "dangerous scalar owner and no-extra-coupling theorem remain unsigned", "b_visible or product source row"),
        ("JX2155_2_WEP_source", "composition/source dependence", "Delta qbar_XT=0 or bounded source charge", "NOT_DERIVED", "WEP/source-shadow pieces remain conditional", "direct WEP product source row"),
        ("JX2155_3_R10_source", "R10/Yukawa projection", "beta_s beta_t K_X/Z_X tau_R10=0 or bounded alpha(lambda)", "PROJECTION_NOT_DERIVED", "tau_R10, K_X/Z_X and lambda_X remain template rows", "alpha_X(lambda) source row"),
        ("JX2155_4_verdict", "source-free no-hair premise", "J_X=0 channelwise", "SOURCE_SILENCE_NOT_DERIVED", "ordinary matter, visible coefficients, WEP, R10, boundary and readout channels are not all parent-silenced", "residual coefficient/product runner"),
    ]
    return [row(silence_id=silence_id, channel=channel, needed_zero=needed_zero, current_status=current_status, obstruction=obstruction, finite_fallback=finite_fallback) for silence_id, channel, needed_zero, current_status, obstruction, finite_fallback in data]


def alpha_rows() -> list[dict[str, object]]:
    data = [
        ("ALPHA2155_0_bulk_operator", "Z_X;M_X2;lambda_X", "lambda_X=sqrt(Z_X/M_X2)", "system_id;field_id;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim", "MISSING_PARENT_INPUT"),
        ("ALPHA2155_1_source_current", "J_X or J_X_bound", "O_X X=J_X", "system_id;J_X;J_X_bound;source_channel;units;source_path;valid_for_claim", "MISSING_SOURCE_ZERO_PROOF"),
        ("ALPHA2155_2_boundary_flux", "boundary_flux_X or boundary_flux_bound", "Phi_boundary=int_boundary X Z_X n.grad X plus edge/projector terms", "system_id;boundary_flux_X;boundary_flux_bound;boundary_rule;units;source_path;valid_for_claim", "MISSING_BOUNDARY_LOCK"),
        ("ALPHA2155_3_bulk_R10_projection", "K_X;Qbar_XH;qbar_XT", "alpha_bulk(lambda_X)=K_X Qbar_XH qbar_XT", "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;normalization;units;source_path;valid_for_claim", "MISSING_ARENA_PROJECTION"),
        ("ALPHA2155_4_edge_projection", "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT", "alpha_edge(lambda_edge)=K_edge Qbar_edge_XH qbar_XT", "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim", "MISSING_EDGE_PROJECTION"),
        ("ALPHA2155_5_no_cancellation_guard", "alpha_total_guard", "abs_alpha_total=|alpha_bulk|+|alpha_edge|+|epsilon_FB5540|+|alpha_R11|", "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim", "NOT_COMPUTED_COMPONENTS_MISSING"),
    ]
    return [row(row_id=row_id, quantity=quantity, formula=formula, required_columns=required_columns, current_status=current_status) for row_id, quantity, formula, required_columns, current_status in data]


def alpha_refusal_rows(alpha: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in alpha:
        reasons = ["VALID_FOR_CLAIM_FALSE"]
        if "MISSING_PARENT_INPUT" in str(item["current_status"]):
            reasons.append("MISSING_OPERATOR_RANGE")
        if "SOURCE" in str(item["current_status"]):
            reasons.append("MISSING_SOURCE_SILENCE_OR_BOUND")
        if "BOUNDARY" in str(item["current_status"]):
            reasons.append("MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND")
        if "PROJECTION" in str(item["current_status"]):
            reasons.append("MISSING_ALPHA_PROJECTION_INPUTS")
        if "NOT_COMPUTED" in str(item["current_status"]):
            reasons.append("MISSING_NO_CANCELLATION_GUARD")
        rows.append(row(runner_id=str(item["row_id"]).replace("ALPHA", "RUN"), row_id=item["row_id"], computed_status="REFUSED_NO_CLAIM", failure_reasons=";".join(reasons)))
    rows.append(row(runner_id="RUN2155_6_verdict", row_id="ALPHA2155_ALL", computed_status="REFUSED_NO_CLAIM", failure_reasons="operator/range, source, projection, edge and total guard rows are missing"))
    return rows


def branch_verdict_rows() -> list[dict[str, object]]:
    data = [
        ("BV2155_0_scalar_zero", "scalar no-hair theorem", "FAIL_CURRENT_CLAIM", "parent owner, Z_X, M_X2, J_X=0, boundary_flux_X=0, zero-mode and units are not parent-signed", "positive energy identity is an exact conditional theorem target only", "try parent Xhat owner and Hessian/range extraction"),
        ("BV2155_1_residual_alpha", "residual alpha scorer", "SCHEMA_READY_RUNNER_REFUSES", "K_X, Qbar_XH, qbar_XT, lambda_X, edge terms and total guard are missing", "alpha rows are ready as nonclaim placeholders only", "fill first parent owner/Hessian/range row before alpha scoring"),
        ("BV2155_2_coupling_status", "coupling suspicion", "CONFIRMED_AS_LIVE_GAP", "J_X, qbar_XT, Qbar_XH and edge projection are exact coupling/source places where local tests bite", "coupling is now a concrete input class, not a vague objection", "after owner/Z/M, attack J_X=0 or source product with paths"),
        ("BV2155_3_next_target", "next target", "PARENT_OWNER_AND_HESSIAN_FIRST", "without a parent Xhat and Z_X/M_X2, neither no-hair nor alpha(lambda) can be normalized", "operator/range owner is the next least-fake derivation target", "2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"),
    ]
    return [row(verdict_id=verdict_id, branch=branch, status=status, because=because, allowed_statement=allowed_statement, next_action=next_action) for verdict_id, branch, status, because, allowed_statement, next_action in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2155_0_parent_owner", "same Xhat controls coefficient and no-hair equation", False, "OWN2155_4_verdict=PARENT_OWNER_NOT_DERIVED"),
        ("CG2155_1_operator_positive", "positive self-adjoint operator is parent-owned", False, "OP2155_4_verdict=OPERATOR_PACK_UNSIGNED"),
        ("CG2155_2_mass_gap_range", "M_X^2 and lambda_X are source-backed", False, "M_X^2/lambda_X remain formula-only"),
        ("CG2155_3_source_silence", "J_X=0 channelwise", False, "JX2155_4_verdict=SOURCE_SILENCE_NOT_DERIVED"),
        ("CG2155_4_boundary_flux_zero", "boundary_flux_X=0", False, "boundary class/no-hair/projector silence remains unsigned"),
        ("CG2155_5_scalar_nohair_claim", "scalar no-hair theorem closes local branch", False, "exact conditional theorem lacks parent owner/operator/source/boundary premises"),
        ("CG2155_6_alpha_runner_claim", "residual alpha row can be scored", False, "alpha runner refusal blocks all rows"),
        ("CG2155_7_local_GR_Newton", "local GR/Newton reduction follows", False, "scalar no-hair/residual score gates remain blocked"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2155_0_theorem_result", "The positive no-hair theorem is exact conditional math, not an active MTS claim.", "parent owner, positive operator, source silence and boundary silence are all unsigned.", "do not claim local plateau or GR reduction from this theorem yet"),
        ("DEC2155_1_runner_result", "Residual alpha runner is staged but refuses all claims.", "operator/range, source, projection, edge and total guard rows are missing.", "fill first parent owner/Hessian/range row before alpha scoring"),
        ("DEC2155_2_coupling", "The coupling gap is now concrete.", "J_X, qbar_XT, Qbar_XH and edge projection are the exact coupling/source places where local tests bite.", "after parent owner/Z_X/M_X2, attack J_X=0 or qbar_XT/product row with source paths"),
        ("DEC2155_3_next_target", "Next target is parent Xhat owner plus Hessian signs and range.", "without the same parent Xhat and Z_X/M_X2, neither no-hair nor alpha(lambda) can be normalized.", "2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2155_0_2156",
            next_target="2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            script="scripts/Y5_R2FR_parent_Xhat_owner_and_Hessian_ZX_MX2_range_or_alpha_source_row_2156.py",
            objective="Derive or source the parent Xhat owner, Hessian signs, field units, M_X^2, lambda_X and first fallback alpha/source row if the Hessian cannot be owned.",
            selection_status="selected",
            success_condition="one parent-owned scalar/operator row supplies Xhat, Z_X, M_X2 and lambda_X, or the branch is explicitly demoted to sourced residual coefficients",
        )
    ]


def write_branch_copies(contract: list[dict[str, object]], owner: list[dict[str, object]], alpha_refusal: list[dict[str, object]], verdicts: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2155_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_SCALAR_NOHAIR_2155_NONCLAIM.csv", contract + owner),
        ("COPY2155_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2155_SCALAR_NOHAIR_NONCLAIM.csv", alpha_refusal + verdicts),
        ("COPY2155_2_acquisition_queue", QUEUE / "JR2155_PARENT_XHAT_HESSIAN_QUEUE.csv", next_rows + owner),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    scalar: list[dict[str, object]],
    contract: list[dict[str, object]],
    owner: list[dict[str, object]],
    operator: list[dict[str, object]],
    source_silence: list[dict[str, object]],
    alpha: list[dict[str, object]],
    alpha_refusal: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    scalar_ok = any(item["input_id"] == "SIA2155_7_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM" for item in scalar)
    theorem_ok = any(item["theorem_id"] == "NHC2155_2_zero_result" and item["status"] == "EXACT_CONDITIONAL_THEOREM" for item in contract)
    owner_ok = any(item["owner_id"] == "OWN2155_4_verdict" and item["current_status"] == "PARENT_OWNER_NOT_DERIVED" for item in owner)
    operator_ok = any(item["input_id"] == "OP2155_4_verdict" and item["current_status"] == "OPERATOR_PACK_UNSIGNED" for item in operator)
    source_ok = any(item["silence_id"] == "JX2155_4_verdict" and item["current_status"] == "SOURCE_SILENCE_NOT_DERIVED" for item in source_silence)
    alpha_ok = {"ALPHA2155_0_bulk_operator", "ALPHA2155_3_bulk_R10_projection", "ALPHA2155_5_no_cancellation_guard"}.issubset({str(item["row_id"]) for item in alpha}) and all(not truthy(item.get("valid_for_claim", False)) for item in alpha)
    refusal_ok = any(item["runner_id"] == "RUN2155_6_verdict" and item["computed_status"] == "REFUSED_NO_CLAIM" for item in alpha_refusal)
    verdict_ok = any(item["verdict_id"] == "BV2155_3_next_target" and item["status"] == "PARENT_OWNER_AND_HESSIAN_FIRST" for item in verdicts)
    gates_ok = all(not truthy(item.get("gate_pass", False)) and not truthy(item.get("claim_allowed", False)) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2155_3_next_target" and "parent Xhat" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2155_0_2156" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for group in (scalar, alpha) for item in group if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, scalar, contract, owner, operator, source_silence, alpha, alpha_refusal, verdicts, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2155_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, scalar_ok, theorem_ok, owner_ok, operator_ok, source_ok, alpha_ok, refusal_ok, verdict_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2155_00_sources", sources_ok, "2154 handoff and old 1846/1847 frontier validate"),
        ("VAL2155_01_scalar_verdict_blocks_claim", scalar_ok, "scalar no-hair theorem remains nonclaim"),
        ("VAL2155_02_conditional_theorem", theorem_ok, "exact conditional no-hair theorem is written"),
        ("VAL2155_03_parent_owner_blocks", owner_ok, "parent scalar owner remains unsigned"),
        ("VAL2155_04_operator_pack_blocks", operator_ok, "positive operator pack remains unsigned"),
        ("VAL2155_05_source_silence_blocks", source_ok, "source silence remains unsigned"),
        ("VAL2155_06_alpha_rows_nonclaim", alpha_ok, "alpha coefficient rows exist and stay nonclaim"),
        ("VAL2155_07_alpha_runner_refuses", refusal_ok, "residual alpha runner refuses all claims"),
        ("VAL2155_08_branch_next", verdict_ok, "branch verdict selects parent owner/Hessian first"),
        ("VAL2155_09_claim_gates_blocked", gates_ok, "all claim gates remain blocked"),
        ("VAL2155_10_decision_next", decisions_ok, "decision ledger selects parent Xhat/Hessian target"),
        ("VAL2155_11_next", next_ok, "next target selected"),
        ("VAL2155_12_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2155_13_csv_parse", csv_ok, "all generated 2155 CSVs parse cleanly"),
        ("VAL2155_14_missing_not_ready", missing_not_ready, "MISSING_* rows stay nonclaim"),
        ("VAL2155_15_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2155_16_formalization_clean", formalization_clean, "formalization-workbench untouched by 2155"),
        ("VAL2155_17_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2155_OVERALL", all_ok, "2155 proves scalar no-hair only as a conditional contract and selects parent Xhat/Hessian next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    scalar: list[dict[str, object]],
    contract: list[dict[str, object]],
    owner: list[dict[str, object]],
    operator: list[dict[str, object]],
    source_silence: list[dict[str, object]],
    alpha: list[dict[str, object]],
    alpha_refusal: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2154, _ = find_line(DOCS["2154"], ["NEXT2154_0_2155"])
    line_1847, _ = find_line(DOCS["1847"], ["SV1847_6_verdict"])
    content = "\n\n".join(
        [
            "# 2155 - Y5/R2FR Scalar No-Hair Input Pack Or Residual Alpha Coefficient Runner",
            "## Current Verdict",
            "2155 does **not** prove scalar no-hair, residual alpha pass, R10/R11, PPN, local GR/Newton, or any public claim.",
            "The useful result is mathematical discipline: a parent-owned scalar with positive self-adjoint operator, source silence, boundary silence and no zero mode would vanish locally. Current MTS does not yet own the physical premises: parent `Xhat`, `Z_X`, `M_X^2`, `J_X=0`, `boundary_flux_X=0`, `lambda_X`, or alpha/product normalization.",
            f"This follows the current 2154 handoff at line {line_2154} and syncs to the old parent-Hessian contract at 1847 line {line_1847}. The next target is parent `Xhat` plus Hessian signs/range, not another re-derivation of the same energy identity.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Scalar Input Assessment",
            md_table(scalar, ["input_id", "quantity", "required_condition", "current_evidence", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## Positive No-Hair Contract",
            md_table(contract, ["theorem_id", "step", "mathematical_statement", "status", "consequence", "valid_for_claim"]),
            "## Parent Scalar Owner Audit",
            md_table(owner, ["owner_id", "candidate_owner", "needed_identity", "current_status", "why_not_closed", "if_closed", "valid_for_claim"]),
            "## Positive Operator Pack",
            md_table(operator, ["input_id", "required_input", "mathematical_role", "current_status", "source_basis", "blocks_claim", "valid_for_claim"]),
            "## Source Silence Audit",
            md_table(source_silence, ["silence_id", "channel", "needed_zero", "current_status", "obstruction", "finite_fallback", "valid_for_claim"]),
            "## Alpha Coefficient Rows",
            md_table(alpha, ["row_id", "quantity", "formula", "required_columns", "current_status", "valid_for_claim"]),
            "## Alpha Runner Refusal",
            md_table(alpha_refusal, ["runner_id", "row_id", "computed_status", "claim_allowed", "failure_reasons", "valid_for_claim"]),
            "## Branch Verdicts",
            md_table(verdicts, ["verdict_id", "branch", "status", "because", "allowed_statement", "next_action", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This is a good hard gate. The local-GR branch now has an exact mathematical contract instead of a plateau axiom: identify the parent scalar, prove the positive operator, prove source and boundary silence, and the local profile dies. If any premise fails, MTS must carry residual alpha/source rows and face local tests honestly.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    scalar = scalar_input_assessment_rows()
    contract = positive_nohair_contract_rows()
    owner = parent_owner_audit_rows()
    operator = operator_pack_rows()
    source_silence = source_silence_rows()
    alpha = alpha_rows()
    alpha_refusal = alpha_refusal_rows(alpha)
    verdicts = branch_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["scalar_input_assessment"], scalar)
    write_csv(OUTPUTS["positive_nohair_contract"], contract)
    write_csv(OUTPUTS["parent_owner_audit"], owner)
    write_csv(OUTPUTS["operator_pack"], operator)
    write_csv(OUTPUTS["source_silence"], source_silence)
    write_csv(OUTPUTS["alpha_rows"], alpha)
    write_csv(OUTPUTS["alpha_refusal"], alpha_refusal)
    write_csv(OUTPUTS["branch_verdicts"], verdicts)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(contract, owner, alpha_refusal, verdicts, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, scalar, contract, owner, operator, source_silence, alpha, alpha_refusal, verdicts, gates, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, scalar, contract, owner, operator, source_silence, alpha, alpha_refusal, verdicts, gates, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2155 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
