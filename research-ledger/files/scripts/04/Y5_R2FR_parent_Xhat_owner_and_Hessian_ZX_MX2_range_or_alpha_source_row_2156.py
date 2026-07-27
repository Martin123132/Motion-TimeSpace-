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


DOC = ROOT / "2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2155": ROOT / "2155-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
    "2155_validation": OUT / "P8_Y5_BRR545_2155_VALIDATION.csv",
    "2155_next": OUT / "P8_Y5_PARENT_QLOC_2155_NEXT_TARGET.csv",
    "1847": ROOT / "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
    "1847_validation": OUT / "P8_Y5_BRR545_1847_VALIDATION.csv",
    "1848": ROOT / "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "1848_validation": OUT / "P8_Y5_BRR545_1848_VALIDATION.csv",
    "1848_next": OUT / "P8_Y5_PARENT_QLOC_1848_NEXT_TARGET.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2156_SOURCE_REGISTER.csv",
    "parent_xhat_action": OUT / "P8_Y5_PARENT_QLOC_2156_PARENT_XHAT_ACTION_CLAUSE.csv",
    "second_variation": OUT / "P8_Y5_PARENT_QLOC_2156_SECOND_VARIATION_DERIVATION.csv",
    "parent_hessian": OUT / "P8_Y5_PARENT_QLOC_2156_PARENT_HESSIAN_AUDIT.csv",
    "normalization_locks": OUT / "P8_Y5_PARENT_QLOC_2156_FIELD_NORMALIZATION_LOCKS.csv",
    "alpha_template": OUT / "P8_Y5_PARENT_QLOC_2156_ALPHA_SOURCE_ROW_TEMPLATE.csv",
    "direct_product": OUT / "P8_Y5_PARENT_QLOC_2156_DIRECT_PRODUCT_BRIDGE.csv",
    "branch_verdicts": OUT / "P8_Y5_PARENT_QLOC_2156_BRANCH_VERDICTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2156_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2156_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2156_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2156_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2156_VALIDATION.csv",
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


def formalization_has_2156_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2156-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2156*",
        "*P8_Y5_BRR545_2156*",
        "*Y5_R2FR_parent_Xhat_owner_and_Hessian_ZX_MX2_range_or_alpha_source_row_2156*",
        "*AFRAME_PARENT_XHAT_HESSIAN_2156*",
        "*JR2156*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2156_00_2155_handoff", DOCS["2155"], [["NEXT2155_0_2156"], ["PARENT_OWNER_AND_HESSIAN_FIRST"], ["VAL2155_OVERALL"]], "current 2155 selects parent Xhat/Hessian/range gate."),
        ("SRC2156_01_2155_validation", DOCS["2155_validation"], [["VAL2155_OVERALL"], ["PASS"]], "current 2155 validation passed as nonclaim."),
        ("SRC2156_02_2155_next", DOCS["2155_next"], [["NEXT2155_0_2156"], ["Xhat"], ["Hessian"]], "machine-readable current next target."),
        ("SRC2156_03_1847_xhat_hessian", DOCS["1847"], [["PX1847_4_verdict"], ["SV1847_6_verdict"], ["PHA1847_8_verdict"]], "old 1847 supplies exact Xhat/Hessian/range contract and failure mode."),
        ("SRC2156_04_1847_validation", DOCS["1847_validation"], [["VAL1847_OVERALL"], ["PASS"]], "old 1847 validation passed as nonclaim."),
        ("SRC2156_05_1848_metric_return", DOCS["1848"], [["PM1848_6_verdict"], ["BE1848_4_verdict"], ["SZR1848_5_verdict"]], "old 1848 shows parent metric/eigenvalue remains unsigned and source-zero return is next."),
        ("SRC2156_06_1848_validation", DOCS["1848_validation"], [["VAL1848_OVERALL"], ["PASS"]], "old 1848 validation passed as nonclaim."),
        ("SRC2156_07_1848_next", DOCS["1848_next"], [["NEXT1848_0_primary"], ["qbarXT"], ["bounded-coupling"]], "old 1848 selects qbar_XT/J_X source-zero or bounded coupling next."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def parent_xhat_action_rows() -> list[dict[str, object]]:
    data = [
        ("PX2156_0_field_owner", "S_parent contains a normalized scalar/vertical mode Xhat with a declared quotient or physical-residual role", "Xhat is not chi_X closure notation; it is the field varied in the parent action and used in the Hessian", "NOT_SIGNED", "connects no-hair operator, range, alpha/WEP products and local residual rows"),
        ("PX2156_1_same_variable_lock", "visible coefficient response and no-hair equation use the same Xhat", "d ln(c_visible)=b_X dXhat and delta_X S_parent gives L_X Xhat=J_X with one normalization", "NOT_DERIVED", "prevents separate knobs for clocks, WEP, R10 range and source amplitude"),
        ("PX2156_2_matter_response", "ordinary matter response is from same Xhat or zero", "delta_X S_matter=J_X^matter delta Xhat with source units, or matter descends through q and J_X^matter=0", "CONDITIONAL_ONLY", "would decide qbar_XT/J_X source-zero versus finite residual"),
        ("PX2156_3_observed_frame_lock", "observed clock/coframe/readout uses same Xhat normalization", "no hidden conformal/disformal/readout channel rescales Xhat after the Hessian is fixed", "NOT_SIGNED", "prevents alpha and local clock/WEP channels from using independent normalizations"),
        ("PX2156_4_verdict", "parent Xhat action clause sufficient for Hessian and product scoring", "field owner + same-variable lock + matter response + readout/frame + no-rescale rule", "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED", "2156 Hessian and alpha/product rows can become real prediction rows"),
    ]
    return [row(clause_id=clause_id, parent_action_clause=parent_action_clause, must_satisfy=must_satisfy, current_status=current_status, if_signed=if_signed) for clause_id, parent_action_clause, must_satisfy, current_status, if_signed in data]


def second_variation_rows() -> list[dict[str, object]]:
    data = [
        ("SV2156_0_local_block", "write minimal parent-owned local Xhat block", "S_X=int_A sqrt(h)[1/2 Z_X h^{ij} partial_i Xhat partial_j Xhat + 1/2 M_X^2 Xhat^2 - J_X Xhat] + boundary", "smallest scalar block whose second variation can define local finite-range channel", "CONDITIONAL_ANSATZ_ONLY", "same parent action must produce Xhat, h_ij, Z_X, M_X^2, J_X and boundary terms"),
        ("SV2156_1_euler_operator", "vary Xhat once", "delta_X S_X -> O_X Xhat = J_X with O_X=-nabla_i(Z_X nabla^i)+M_X^2", "local operator is fixed once parent block and boundary convention are owned", "CONDITIONAL_OPERATOR_DERIVED", "parent Euler expression, self-adjoint domain and source split"),
        ("SV2156_2_Hessian_signs", "vary Xhat twice", "delta_X^2 S_X=int_A sqrt(h)[Z_X |grad delta Xhat|^2+M_X^2(delta Xhat)^2]+boundary Hessian terms", "Z_X>0 and M_X^2>0 are exact local stability requirements", "EXACT_CONDITION_DERIVED_VALUES_MISSING", "parent Hessian signs, mixed-sector Hessian control and units"),
        ("SV2156_3_range_relation", "canonicalize static operator", "mu_X^2=M_X^2/Z_X and lambda_X=sqrt(Z_X/M_X^2)", "lambda_X is exact if Z_X and M_X^2 are positive and come from the same normalized parent branch", "EXACT_RELATION_DERIVED_NOT_OWNED", "same-branch Z_X/M_X^2 with length units"),
        ("SV2156_4_field_rescaling_guard", "block fake normalization wins", "Xhat->aXhat rescales Z_X, M_X^2, J_X and b_X in linked ways; invariant rows are lambda_X and coupled products", "field rescaling cannot choose beta, lambda or alpha after seeing local data", "GUARDRAIL_PASS", "parent field-space metric or Ward identity fixing invariant normalization"),
        ("SV2156_5_sourcefree_nohair", "connect Hessian to local silence", "int_A[Z_X|grad Xhat|^2+M_X^2 Xhat^2]=int_A Xhat J_X+boundary_flux_X", "if Z_X>0, M_X^2>0, J_X=0 and boundary_flux_X=0, then Xhat=0 on local exterior", "CONDITIONAL_THEOREM_ONLY", "J_X=0, boundary flux zero and parent-signed positivity together"),
        ("SV2156_6_verdict", "decide whether 2156 owns the Hessian", "parent_signed(delta_X^2 S_parent) -> Xhat,Z_X,M_X^2,lambda_X,alpha/source row", "2156 derives the exact contract but does not find parent-signed Xhat/Hessian ownership in current corpus", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED", "explicit parent second variation, Xhat owner and normalization ledger"),
    ]
    return [row(derivation_id=derivation_id, step=step, mathematical_statement=mathematical_statement, derived_result=derived_result, status=status, missing_for_claim=missing_for_claim) for derivation_id, step, mathematical_statement, derived_result, status, missing_for_claim in data]


def parent_hessian_rows() -> list[dict[str, object]]:
    data = [
        ("PHA2156_0_branch_extremum", "F_1=E_Xhat|_{Xhat=0}", "parent Euler expression vanishes on local branch before readout", "scalar branch remains nonclaim; no parent Xhat action clause is signed", "MISSING_PARENT_EULER_ZERO", "Xhat=0 is not proven stationary local vacuum"),
        ("PHA2156_1_ZX_positive", "Z_X>0", "positive gradient Hessian residue with field units and sign convention", "operator pack remains unsigned; parent sign missing", "MISSING_PARENT_HESSIAN_SIGN", "ghost, anti-elliptic or indefinite local residual must be retained"),
        ("PHA2156_2_MX2_positive", "M_X^2>0", "positive local curvature Hessian in same Xhat normalization", "mass gap/range remain formula-only; beta eigenvalue not signed", "MISSING_PARENT_MASS_GAP", "massless, tachyonic or long-range branch remains possible"),
        ("PHA2156_3_lambda_units", "lambda_X=sqrt(Z_X/M_X^2)", "same-branch Z_X and M_X^2 with compatible units yielding meters", "range relation exact but values/units missing; alpha runner refuses", "RELATION_ONLY_VALUES_MISSING", "R10/local interpolation cannot be claim-grade"),
        ("PHA2156_4_cross_Hessian", "mixed Xhat-sector Hessian terms", "cross terms with metric, trace, projector, boundary and matter variables vanish or form positive block", "no full parent metric/cross-term policy in active branch", "MISSING_BLOCK_DIAGONAL_OR_POSITIVE_MATRIX_PROOF", "single-scalar Z_X/M_X^2 truncation may be invalid"),
        ("PHA2156_5_source_current", "J_X=0 or bound", "ordinary matter, hidden channels and readout tails give zero source or bounded source current", "source-zero route remains conditional", "MISSING_SOURCE_ZERO_OR_BOUND", "positive no-hair cannot conclude; residual alpha/product row needed"),
        ("PHA2156_6_boundary_flux", "boundary_flux_X=0 or bound", "self-adjoint boundary class, exact/proper gauge edge or explicit flux bound", "boundary/EDGEBOUND/projector branch unsigned", "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND", "positive no-hair identity cannot conclude Xhat=0"),
        ("PHA2156_7_prefactor", "K_X=s_X/(4*pi*Z_X*G_obs)", "normalization convention, sign s_X, G_obs frame and source/test charges", "alpha source rows remain schema-ready values-missing", "MISSING_ALPHA_NORMALIZATION", "alpha(lambda) row remains smoke-only"),
        ("PHA2156_8_verdict", "parent Xhat/Hessian ownership", "PX2156 and PHA2156_0 through PHA2156_7 close from one parent branch", "none of the parent-owned owner/value/sign/source rows close", "FAIL_CURRENT_CLAIM", "move to parent metric/eigenvalue theorem or source-zero/bounded coupling row"),
    ]
    return [row(audit_id=audit_id, object=object_name, required_evidence=required_evidence, current_evidence=current_evidence, status=status, if_missing=if_missing) for audit_id, object_name, required_evidence, current_evidence, status, if_missing in data]


def normalization_lock_rows() -> list[dict[str, object]]:
    data = [
        ("FNL2156_0_invariant", "identify physical finite-range invariant", "beta_eff=ell_vac^2 M_X^2/Z_X or an equivalent parent-normalized Hessian eigenvalue", "CONDITIONAL_INVARIANT_IDENTIFIED", "theorem target and normalization guard", "claim that rho_vac alone predicts lambda_X"),
        ("FNL2156_1_canonical_metric", "make vacuum density set the field-space metric", "Z_X f_X^2=rho_vac^(1/2)", "CLEAN_CONTRACT_NOT_SIGNED", "parent Ward/metric theorem target", "normalization chosen after R10 pressure"),
        ("FNL2156_2_beta_eigenvalue", "make beta a parent spectrum value", "beta_eff is eigenvalue of normalized Hessian H_X", "SPECTRAL_TARGET_NOT_SIGNED", "finite theorem target for 2157", "model-chosen beta from desired local range"),
        ("FNL2156_3_direct_range", "direct range backsolve", "choose beta/lambda after seeing local bound pressure", "CLOSURE_ONLY_FORBIDDEN_AS_DERIVATION", "sanity check only", "evidence or prediction"),
        ("FNL2156_4_CX_tie", "tie range normalization to source amplitude", "same parent normalization fixes lambda_X and C_X/K_X/qbar_XT/Qbar_XH", "MISSING_COUPLING_NORMALIZATION_LEDGER", "next source-row schema", "choose range and amplitude independently"),
    ]
    return [row(lock_id=lock_id, target=target, condition=condition, current_status=current_status, allowed_use=allowed_use, forbidden_use=forbidden_use) for lock_id, target, condition, current_status, allowed_use, forbidden_use in data]


def alpha_template_rows() -> list[dict[str, object]]:
    data = [
        ("ASR2156_0_bulk_Hessian", "Xhat;Z_X;M_X2;lambda_X", "lambda_X=sqrt(Z_X/M_X2)", "system_id;field_id;branch_id;Xhat_owner;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim", "MISSING_PARENT_INPUT", str(OUTPUTS["parent_hessian"])),
        ("ASR2156_1_field_metric_beta", "Z_X f_X^2;Upp0;beta_eff", "beta_eff=Upp0*rho_vac^(1/2)/(Z_X*f_X^2)", "system_id;branch_id;ZX_fX2;Upp0;beta_eff;metric_units;source_path;valid_for_claim", "MISSING_PARENT_METRIC_AND_EIGENVALUE", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2157_PARENT_METRIC_ATTEMPT.csv"),
        ("ASR2156_2_source_zero", "J_X;qbar_XT", "J_X=0 or qbar_XT=0 theorem/row", "system_id;source_channel;J_X;J_X_bound;qbar_XT;qbar_bound;units;source_path;valid_for_claim", "MISSING_SOURCE_ZERO_OR_BOUND", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2157_SOURCE_ZERO_RETURN.csv"),
        ("ASR2156_3_boundary_flux", "boundary_flux_X", "boundary_flux_X=0 or bounded EDGEBOUND", "system_id;boundary_channel;boundary_flux_X;bound;units;source_path;valid_for_claim", "MISSING_BOUNDARY_LOCK", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2152_SOURCE_PACK_SCHEMA.csv"),
        ("ASR2156_4_green_prefactor", "K_X", "K_X=s_X/(4*pi*Z_X*G_obs)", "system_id;K_X;s_X;Z_X;G_obs;normalization;units;source_path;valid_for_claim", "MISSING_ALPHA_NORMALIZATION", str(OUTPUTS["normalization_locks"])),
        ("ASR2156_5_candidate_alpha", "alpha_bulk(lambda_X)", "alpha_bulk(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT", "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;alpha_bound;source_paths;valid_for_claim", "SCHEMA_READY_VALUES_MISSING", str(OUTPUTS["alpha_template"])),
    ]
    return [row(row_id=row_id, quantity=quantity, formula=formula, required_columns=required_columns, current_status=current_status, source_path=source_path) for row_id, quantity, formula, required_columns, current_status, source_path in data]


def direct_product_rows() -> list[dict[str, object]]:
    data = [
        ("DPB2156_0_WEP_threshold", "P_WEP_alpha_direct bound", "NUMERIC_THRESHOLD_NONCLAIM_EXISTS", "4.797780522732e-05", "dimensionless", "private WEP product threshold can score a future direct MTS product row"),
        ("DPB2156_1_MTS_prediction", "MTS direct WEP/R10 product prediction", "MISSING_MTS_DIRECT_PRODUCT", "MISSING", "dimensionless", "requires parent Xhat action/matter response or explicit source-backed product"),
        ("DPB2156_2_verdict", "direct product bridge", "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING", "MISSING", "dimensionless", "threshold is useful only after prediction-side parent product exists"),
    ]
    return [row(bridge_id=bridge_id, object=object_name, status=status, value=value, units=units, meaning=meaning) for bridge_id, object_name, status, value, units, meaning in data]


def branch_verdict_rows() -> list[dict[str, object]]:
    data = [
        ("BV2156_0_Xhat_owner", "parent Xhat owner", "PARENT_ACTION_CLAUSE_NOT_DERIVED", "no source makes Xhat the field varied in the parent action and the same variable controlling visible coefficients", "MTS has an exact parent-owner contract", "chi_X/Xhat is already the physical scalar", "try parent metric/eigenvalue theorem or direct source product row"),
        ("BV2156_1_Hessian_formula", "parent Hessian route", "CONTRACT_DERIVED_NOT_OWNED", "second variation/range law is exact, but current files do not supply parent-signed Xhat, Z_X, M_X^2 or units", "MTS has a precise Hessian contract for local scalar route", "MTS predicts lambda_X or passes local tests from this route", "derive parent field-space metric and Hessian eigenvalue"),
        ("BV2156_2_alpha_source_row", "residual alpha/source fallback", "SCHEMA_READY_VALUES_MISSING", "K_X, Qbar_XH, qbar_XT, Z_X, Xhat owner and lambda_X remain missing or unsigned", "fallback alpha rows are ready to receive sourced values", "fallback alpha row is evidence", "fill only after parent metric/eigenvalue or source-current coefficients exist"),
        ("BV2156_3_direct_product", "direct WEP/R10 product", "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING", "WEP product threshold exists but MTS has no parent-projected product prediction", "direct product scoring avoids fake factor splitting if prediction row is sourced", "threshold alone supports MTS", "use only after parent Xhat matter-response clause or numeric product row exists"),
        ("BV2156_4_next_target", "next target", "PARENT_METRIC_OR_SOURCE_ZERO_RETURN", "Xhat owner/Hessian row failed; the least fake next options are parent metric/eigenvalue or qbar_XT/J_X source-zero", "finite route is a private theorem target; source-zero remains cleaner for local GR", "finite lambda or local-GR claim", "2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"),
    ]
    return [row(verdict_id=verdict_id, branch=branch, status=status, because=because, allowed_statement=allowed_statement, forbidden_statement=forbidden_statement, next_action=next_action) for verdict_id, branch, status, because, allowed_statement, forbidden_statement, next_action in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2156_0_sources_registered", "2156 source chain exists", False, "sources prove audit continuity only, not parent Xhat ownership"),
        ("CG2156_1_parent_Xhat_owner", "same Xhat is parent-owned scalar/operator field", False, "PX2156_4_verdict=PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED"),
        ("CG2156_2_parent_block_owned", "single parent action owns Xhat block", False, "local block is conditional ansatz only"),
        ("CG2156_3_ZX_positive", "Z_X>0 is parent-signed", False, "kinetic Hessian sign and units are missing"),
        ("CG2156_4_MX2_positive", "M_X^2>0 is parent-signed", False, "mass-gap/eigenvalue theorem is missing"),
        ("CG2156_5_alpha_source_claim", "alpha(lambda) row is claim-grade", False, "K_X, Qbar_XH, qbar_XT and bound comparison inputs are missing"),
        ("CG2156_6_local_GR_claim", "local GR/Newton reduction is derived", False, "Xhat/Hessian/source/boundary/no-pole routes remain unsigned"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2156_0_exact_contract", "The exact parent Xhat/Hessian/range contract is now written in the active branch.", "second variation gives O_X, positivity conditions and lambda_X=sqrt(Z_X/M_X^2), while the parent Xhat clause states the owner requirement.", "do not re-derive the same formula; hunt parent metric/eigenvalue or source-zero owner"),
        ("DEC2156_1_no_claim", "Current MTS still does not own Xhat, Z_X, M_X^2, lambda_X or alpha.", "required values, signs, units, cross-term controls, matter response and source coefficients are missing or conditional.", "keep local R10/PPN/local-GR claims blocked"),
        ("DEC2156_2_product_bridge", "Direct WEP product scoring is useful but prediction-side empty.", "the bound-side product threshold exists, but no parent Xhat matter response yields an MTS product row.", "derive parent matter-response clause or source a direct product row later"),
        ("DEC2156_3_next_target", "Next target is parent metric/eigenvalue or source-zero return.", "without parent field-space metric/eigenvalue, the finite Hessian route cannot be promoted; source-zero is cleaner for local GR if it can be signed.", "2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2156_0_2157",
            next_target="2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            script="scripts/Y5_R2FR_parent_metric_ZXfX2_beta_eigenvalue_or_source_zero_return_2157.py",
            objective="Try to derive parent field-space metric lock Z_X f_X^2=rho_vac^(1/2) and beta eigenvalue; if unsigned, return to J_X/qbar_XT source-zero or bounded coupling rows.",
            selection_status="selected",
            success_condition="parent M_AB/e_X/H_X spectrum signs the finite route, or finite route is frozen and source-zero/bounded coupling becomes primary",
        ),
        row(
            route_id="NEXT2156_1_parallel",
            next_target="2157b-Y5-R2FR-direct-WEP-R10-product-prediction-row.md",
            script="scripts/Y5_R2FR_direct_WEP_R10_product_prediction_row_2157b.py",
            objective="Stage direct product prediction rows only if parent Xhat matter-response or numeric source kernels are available.",
            selection_status="held",
            success_condition="no standalone beta/tau division, no tau=1 shortcut, no threshold-only claim",
        ),
    ]


def write_branch_copies(parent: list[dict[str, object]], hessian: list[dict[str, object]], alpha: list[dict[str, object]], verdicts: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2156_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_XHAT_HESSIAN_2156_NONCLAIM.csv", parent + hessian),
        ("COPY2156_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2156_XHAT_HESSIAN_NONCLAIM.csv", alpha + verdicts),
        ("COPY2156_2_acquisition_queue", QUEUE / "JR2156_PARENT_METRIC_OR_SOURCE_ZERO_QUEUE.csv", next_rows + hessian),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    parent: list[dict[str, object]],
    second: list[dict[str, object]],
    hessian: list[dict[str, object]],
    locks: list[dict[str, object]],
    alpha: list[dict[str, object]],
    product: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    parent_ok = any(item["clause_id"] == "PX2156_4_verdict" and item["current_status"] == "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED" for item in parent)
    second_ok = any(item["derivation_id"] == "SV2156_6_verdict" and item["status"] == "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED" for item in second)
    hessian_ok = any(item["audit_id"] == "PHA2156_8_verdict" and item["status"] == "FAIL_CURRENT_CLAIM" for item in hessian)
    locks_ok = any(item["lock_id"] == "FNL2156_1_canonical_metric" and item["current_status"] == "CLEAN_CONTRACT_NOT_SIGNED" for item in locks) and all(not truthy(item.get("valid_for_claim", False)) for item in locks)
    alpha_ok = any(item["row_id"] == "ASR2156_5_candidate_alpha" and item["current_status"] == "SCHEMA_READY_VALUES_MISSING" for item in alpha) and all(not truthy(item.get("valid_for_claim", False)) for item in alpha)
    product_ok = any(item["bridge_id"] == "DPB2156_2_verdict" and item["status"] == "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING" for item in product)
    verdict_ok = any(item["verdict_id"] == "BV2156_4_next_target" and item["status"] == "PARENT_METRIC_OR_SOURCE_ZERO_RETURN" for item in verdicts)
    gates_ok = all(not truthy(item.get("gate_pass", False)) and not truthy(item.get("claim_allowed", False)) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2156_3_next_target" and "parent metric" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2156_0_2157" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for group in (hessian, alpha) for item in group if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, parent, second, hessian, locks, alpha, product, verdicts, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2156_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, parent_ok, second_ok, hessian_ok, locks_ok, alpha_ok, product_ok, verdict_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2156_00_sources", sources_ok, "2155 handoff and old 1847/1848 frontier validate"),
        ("VAL2156_01_parent_xhat_blocks", parent_ok, "parent Xhat action clause remains unsigned"),
        ("VAL2156_02_second_variation", second_ok, "second variation/range contract written but nonclaim"),
        ("VAL2156_03_hessian_audit_blocks", hessian_ok, "parent Hessian ownership remains blocked"),
        ("VAL2156_04_normalization_locks", locks_ok, "normalization locks are explicit and nonclaim"),
        ("VAL2156_05_alpha_schema", alpha_ok, "alpha source row schema is complete and nonclaim"),
        ("VAL2156_06_direct_product", product_ok, "direct product bridge remains prediction-side missing"),
        ("VAL2156_07_branch_next", verdict_ok, "branch verdict selects parent metric/source-zero next"),
        ("VAL2156_08_claim_gates", gates_ok, "all claim gates remain blocked"),
        ("VAL2156_09_decision_next", decisions_ok, "decision ledger selects parent metric/source-zero target"),
        ("VAL2156_10_next", next_ok, "next target selected"),
        ("VAL2156_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2156_12_csv_parse", csv_ok, "all generated 2156 CSVs parse cleanly"),
        ("VAL2156_13_missing_not_ready", missing_not_ready, "MISSING_* rows stay nonclaim"),
        ("VAL2156_14_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2156_15_formalization_clean", formalization_clean, "formalization-workbench untouched by 2156"),
        ("VAL2156_16_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2156_OVERALL", all_ok, "2156 writes the parent Xhat/Hessian anti-knob contract and selects parent metric/source-zero next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    parent: list[dict[str, object]],
    second: list[dict[str, object]],
    hessian: list[dict[str, object]],
    locks: list[dict[str, object]],
    alpha: list[dict[str, object]],
    product: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2155, _ = find_line(DOCS["2155"], ["NEXT2155_0_2156"])
    line_1848, _ = find_line(DOCS["1848"], ["SZR1848_5_verdict"])
    content = "\n\n".join(
        [
            "# 2156 - Y5/R2FR Parent Xhat Owner And Hessian ZX/MX2 Range Or Alpha Source Row",
            "## Current Verdict",
            "2156 does **not** prove parent `Xhat`, finite-range prediction, alpha/product pass, R10/R11, PPN, local GR/Newton, or any public claim.",
            "The exact second-variation/range law is written: if one parent-owned `Xhat` supplies `Z_X`, `M_X^2`, source current, boundary flux, units and readout normalization, then `lambda_X=sqrt(Z_X/M_X^2)` is meaningful. Current MTS does not yet own those premises.",
            f"This follows the current 2155 handoff at line {line_2155} and syncs to the old source-zero return at 1848 line {line_1848}. The next fair attack is parent metric/eigenvalue ownership or source-zero/bounded coupling, not another range backsolve.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Parent Xhat Action Clause",
            md_table(parent, ["clause_id", "parent_action_clause", "must_satisfy", "current_status", "if_signed", "valid_for_claim"]),
            "## Second Variation Derivation",
            md_table(second, ["derivation_id", "step", "mathematical_statement", "derived_result", "status", "missing_for_claim", "valid_for_claim"]),
            "## Parent Hessian Audit",
            md_table(hessian, ["audit_id", "object", "required_evidence", "current_evidence", "status", "if_missing", "valid_for_claim"]),
            "## Field Normalization Locks",
            md_table(locks, ["lock_id", "target", "condition", "current_status", "allowed_use", "forbidden_use", "valid_for_claim"]),
            "## Alpha Source Row Template",
            md_table(alpha, ["row_id", "quantity", "formula", "required_columns", "current_status", "source_path", "valid_for_claim"]),
            "## Direct Product Bridge",
            md_table(product, ["bridge_id", "object", "status", "value", "units", "meaning", "valid_for_claim"]),
            "## Branch Verdicts",
            md_table(verdicts, ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
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
            "The finite scalar path is now disciplined: same parent field, same Hessian, same source normalization, same observed-frame readout. No more choosing range here and amplitude there. Since the owner row still fails, the next fair attack is either parent metric/eigenvalue ownership or source-zero/bounded coupling.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    parent = parent_xhat_action_rows()
    second = second_variation_rows()
    hessian = parent_hessian_rows()
    locks = normalization_lock_rows()
    alpha = alpha_template_rows()
    product = direct_product_rows()
    verdicts = branch_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_xhat_action"], parent)
    write_csv(OUTPUTS["second_variation"], second)
    write_csv(OUTPUTS["parent_hessian"], hessian)
    write_csv(OUTPUTS["normalization_locks"], locks)
    write_csv(OUTPUTS["alpha_template"], alpha)
    write_csv(OUTPUTS["direct_product"], product)
    write_csv(OUTPUTS["branch_verdicts"], verdicts)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(parent, hessian, alpha, verdicts, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, parent, second, hessian, locks, alpha, product, verdicts, gates, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, parent, second, hessian, locks, alpha, product, verdicts, gates, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2156 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
