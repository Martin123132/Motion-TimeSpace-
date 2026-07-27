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


DOC = ROOT / "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2157": ROOT / "2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "2157_next": OUT / "P8_Y5_PARENT_QLOC_2157_NEXT_TARGET.csv",
    "2157_validation": OUT / "P8_Y5_BRR545_2157_VALIDATION.csv",
    "1849": ROOT / "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
    "1850": ROOT / "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
    "1850_validation": OUT / "P8_Y5_BRR545_1850_VALIDATION.csv",
    "1044": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
    "1044_validation": OUT / "P8_Y5_BRR545_1044_VALIDATION.csv",
    "1088": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "1088_validation": OUT / "P8_Y5_BRR545_1088_VALIDATION.csv",
    "1093": ROOT / "1093-Y5-R10-scalar-nohair-input-owner-or-balpha-tau-projection-source.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2158_SOURCE_REGISTER.csv",
    "source_zero_identity": OUT / "P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_IDENTITY.csv",
    "premise_gate": OUT / "P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_PREMISE_GATE.csv",
    "jx_decomposition": OUT / "P8_Y5_PARENT_QLOC_2158_JX_QBARXT_DECOMPOSITION.csv",
    "component_pack": OUT / "P8_Y5_PARENT_QLOC_2158_BOUNDED_COUPLING_COMPONENT_PACK.csv",
    "arena_projection": OUT / "P8_Y5_PARENT_QLOC_2158_ARENA_PROJECTION_ROWS.csv",
    "local_gr_gate": OUT / "P8_Y5_PARENT_QLOC_2158_LOCAL_GR_SOURCE_SILENCE_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2158_REFUSAL_RUNNER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2158_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2158_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2158_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2158_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2158_VALIDATION.csv",
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


def formalization_has_2158_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2158-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2158*",
        "*P8_Y5_BRR545_2158*",
        "*Y5_R2FR_JX_qbarXT_source_zero_or_bounded_coupling_component_pack_2158*",
        "*AFRAME_JX_QBARXT_2158*",
        "*JR2158*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2158_00_2157_handoff", DOCS["2157"], [["NEXT2157_0_2158"], ["J_X/qbar_XT"], ["VAL2157_OVERALL"]], "current 2157 selects source-zero/bounded coupling component pack."),
        ("SRC2158_01_2157_next_csv", DOCS["2157_next"], [["NEXT2157_0_2158"], ["source-zero"], ["bounded coupling"]], "machine-readable 2158 target."),
        ("SRC2158_02_2157_validation", DOCS["2157_validation"], [["VAL2157_OVERALL"], ["PASS"]], "2157 validation passed as nonclaim."),
        ("SRC2158_03_1849_source_zero", DOCS["1849"], [["QZ1849_6_verdict"], ["BQT1849_3_total_abs_guard"], ["DEC1849_2_coupling_status"]], "1849 writes qbarXT/JX source-zero theorem and bounded qbarXT schema."),
        ("SRC2158_04_1850_bound_pack", DOCS["1850"], [["NMT1850_6_verdict"], ["FMB1850_10_total_qbarXT_envelope"], ["VAL1850_OVERALL"]], "1850 identifies surviving frame/marker/source coupling families."),
        ("SRC2158_05_1850_validation", DOCS["1850_validation"], [["VAL1850_OVERALL"], ["PASS"]], "1850 validation passed as nonclaim."),
        ("SRC2158_06_1044_pullback", DOCS["1044"], [["MPD1044_7_exact_theorem_if_signed"], ["QBC1044_5_total_abs_guard"], ["CG1044_4_local_GR_reduction"]], "1044 gives exact conditional matter-pullback identity and fallback qbarXT envelope."),
        ("SRC2158_07_1044_validation", DOCS["1044_validation"], [["V1044_SUMMARY"], ["pass"]], "1044 validation passed as nonclaim."),
        ("SRC2158_08_1088_moms", DOCS["1088"], [["MOMS1088_7_verdict"], ["THM1088_5_conclusion"], ["CM1088_4_boundary_domain_marker"]], "1088 minimal ordinary-matter signature gives strongest conditional source-zero route."),
        ("SRC2158_09_1088_validation", DOCS["1088_validation"], [["V1088_SUMMARY"], ["pass"]], "1088 validation passed as nonclaim."),
        ("SRC2158_10_1093_nohair", DOCS["1093"], [["THM1093_2_zero_result"], ["JX1093_4_verdict"], ["DEC1093_0_nohair_contract"]], "1093 connects source silence to positive no-hair/local-GR route."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def source_zero_identity_rows() -> list[dict[str, object]]:
    data = [
        (
            "SZI2158_0_definition",
            "define local source/test response",
            "qbar_XT := M_T^-1 delta_{v_X} S_T and J_X is the bulk coefficient of delta Xhat in delta S_local",
            "This locks test-body response and bulk source current into one vertical-variation language.",
            "DEFINITION_ONLY",
            "parent-owned v_X/Xhat normalization and source measure",
        ),
        (
            "SZI2158_1_chain_rule",
            "ordinary matter variation",
            "delta_v S_T = 1/2 int sqrt(-g_m) T_T^{mu nu} Lie_v g^m_{mu nu} + sum_A int J_theta^A Lie_v theta_A + E_Psi[delta_v Psi] + Phi_boundary",
            "This is the exact conditional identity behind qbar_XT and J_matter.",
            "EXACT_CONDITIONAL_IDENTITY",
            "observed matter frame, constant sector, matter lift and boundary class must be parent-owned",
        ),
        (
            "SZI2158_2_zero_theorem",
            "source-zero theorem",
            "If Dq[v_X]=0, g_m/e_m descend through q, Lie_v theta_A=0, delta_v Psi is gauge/EOM/boundary, no source weights/shadow frames exist, and Phi_boundary=0, then delta_v S_T=0.",
            "Under these premises qbar_XT=0 and J_matter=0 for ordinary matter.",
            "EXACT_THEOREM_UNDER_UNSIGNED_PREMISES",
            "single parent ordinary-matter signature proving every premise together",
        ),
        (
            "SZI2158_3_not_enough",
            "why covariance/WEP alone cannot prove zero",
            "A common conformal frame, species-independent source weight, post-variation selector or boundary/support tail can be covariant and WEP-blind but still give J_X or qbar_XT nonzero.",
            "This blocks the cheap route: source silence must be parent-derived or bounded componentwise.",
            "COUNTEREXAMPLE_GUARD",
            "theorem-zero or source-backed numeric bounds for every surviving channel",
        ),
        (
            "SZI2158_4_verdict",
            "current MTS source-zero status",
            "SZI2158_0 through SZI2158_3 give the exact contract, but current corpus does not sign all premises in one parent branch.",
            "J_X=qbar_XT=0 is not a current claim; bounded component rows remain mandatory.",
            "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED",
            "parent ordinary-matter signature or bounded coupling rows",
        ),
    ]
    return [row(identity_id=identity_id, step=step, mathematical_statement=mathematical_statement, result=result, status=status, missing_for_claim=missing_for_claim) for identity_id, step, mathematical_statement, result, status, missing_for_claim in data]


def premise_gate_rows() -> list[dict[str, object]]:
    data = [
        ("SPG2158_0_vertical_kernel", "Dq[v_X]=0 for the same Xhat/vertical direction used in local source rows", "chain-rule geometry silence", "CONDITIONAL_ONLY", "source Dq matrix and Xhat owner are not closed together"),
        ("SPG2158_1_observed_matter_frame", "ordinary matter metric/coframe/gauge data are pulled back from q(Phi)", "qbar_geom=0", "NOT_PARENT_SIGNED", "common Weyl/disformal/shadow frame remains legal"),
        ("SPG2158_2_matter_lift", "delta_v Psi_A is zero, gauge, local-Lorentz, diffeomorphism, EOM or boundary-only", "bulk matter-field variation contributes no source current", "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR", "matter lift and domain class are unsigned"),
        ("SPG2158_3_constant_superselection", "Lie_v theta_A=0 for masses, charges, alpha_EM, clocks and representation labels", "qbar_constants=0", "CONSTANT_SUPERSELECTION_UNSIGNED", "constant/marker channels remain live"),
        ("SPG2158_4_no_species_weights", "no w_A(X) S_A, kappa_A(X), source-only prefactor or material-source multiplier exists before variation", "qbar_source_weight=0", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "source-current universality remains open"),
        ("SPG2158_5_variation_before_readout", "Hilbert/source current is extracted before empirical/material/readout projection", "post-readout selector cannot manufacture J_X", "CONDITIONAL_SUBTHEOREM_ONLY", "readout/source-normalization tail remains live"),
        ("SPG2158_6_boundary_domain_silence", "boundary charge, support shift, domain selector and non-Hilbert tail are zero or bounded", "qbar_nonH and boundary components vanish or score", "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND", "local projection can reintroduce source"),
        ("SPG2158_7_verdict", "all source-zero premises close together", "J_X=qbar_XT=0 claim", "FAIL_CURRENT_CLAIM", "premises are known but not parent-signed as one action signature"),
    ]
    return [row(gate_id=gate_id, premise=premise, needed_for=needed_for, current_status=current_status, if_missing=if_missing) for gate_id, premise, needed_for, current_status, if_missing in data]


def jx_decomposition_rows() -> list[dict[str, object]]:
    data = [
        ("JQD2158_0_geom", "J_geom/qbar_geom", "observed matter frame/coframe/geodesic coupling", "1/2 int T^{mu nu} Lie_v g^m_{mu nu}", "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND", "c_g;b_dis", "R10;PPN;clock;WEP_common_mode"),
        ("JQD2158_1_constants", "J_constants/qbar_constants", "masses, charges, alpha_EM, nuclear/clock constants", "sum_A int J_theta^A Lie_v theta_A", "MISSING_CONSTANT_SUPERSELECTION_OR_NUMERIC_BOUND", "b_A;b_alpha", "WEP;clock;EM;particle_mass;R10"),
        ("JQD2158_2_marker", "J_marker/qbar_marker", "material, preparation, isotope, source/readout class labels", "sum_marker sensitivity_marker * Lie_v marker", "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS", "b_marker", "WEP_source_charge;clock;R10;readout"),
        ("JQD2158_3_source_weight", "J_source_weight/qbar_source_weight", "source-only Hilbert/current prefactors and species weights", "delta_kappa_A or w_A'(X) S_A contribution", "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND", "delta_kappa_A", "WEP_source_charge;orbital;R10_source_mass"),
        ("JQD2158_4_nonHilbert", "J_nonH/qbar_nonH", "non-Hilbert, torsion/connection, memory, domain or support current", "q_nonH + Delta_W_support + q_domain", "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND", "q_nonH;Delta_W_support;q_domain", "R10;orbital;boundary;local_GR"),
        ("JQD2158_5_boundary", "J_boundary/qbar_boundary", "boundary/local projection flux and source-worldtube edge contribution", "Phi_boundary_X or q_boundary after local projection", "MISSING_BOUNDARY_FLUX_ZERO_OR_NUMERIC_BOUND", "q_boundary;Phi_boundary_X", "boundary;orbital;R10;local_GR"),
        ("JQD2158_6_readout", "J_readout/qbar_readout", "post-variation readout or measured-G/source-normalization selector", "C_readout[A] acting after variation", "MISSING_VARIATION_BEFORE_READOUT_OR_NUMERIC_BOUND", "C_readout;Delta_GM_absorption", "orbital;clock;WEP;R10"),
        ("JQD2158_7_total_abs_guard", "J_X_bound_abs/qbar_XT_bound_abs", "absolute no-cancellation envelope", "|total| <= |geom|+|constants|+|marker|+|source_weight|+|nonH|+|boundary|+|readout|", "SCHEMA_READY_VALUES_MISSING", "all component bounds", "R10;WEP;clock;PPN;orbital;local_GR"),
    ]
    return [row(component_id=component_id, component=component, definition=definition, formula_or_bound=formula_or_bound, current_status=current_status, required_symbols=required_symbols, observable_links=observable_links) for component_id, component, definition, formula_or_bound, current_status, required_symbols, observable_links in data]


def component_pack_rows() -> list[dict[str, object]]:
    data = [
        ("BCP2158_0_cg", "c_g", "common Weyl/conformal derivative d ln A_g/dXhat", "|c_g| <= theorem_zero_or_source_bound", "MISSING_CG_BOUND_OR_ZERO_THEOREM", "dimensionless_per_normalized_Xhat", str(OUT / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv"), "R10;PPN;clock;WEP_common_mode"),
        ("BCP2158_1_bdis", "b_dis", "disformal/profile-normalized matter frame derivative", "|b_dis| <= theorem_zero_or_source_bound", "MISSING_BDIS_BOUND_OR_ZERO_THEOREM", "dimensionless_or_declared_profile_units", str(OUT / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv"), "PPN;clock;orbital;R10"),
        ("BCP2158_2_bA", "b_A", "vertical derivative of material masses/species constants", "|b_A| <= theorem_zero_or_source_bound", "MISSING_BA_BOUND_OR_ZERO_THEOREM", "dimensionless_per_normalized_Xhat", str(OUT / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv"), "WEP;clock;R10;particle_mass"),
        ("BCP2158_3_balpha", "b_alpha", "vertical derivative of alpha_EM/gauge/binding/clock constants", "|b_alpha| <= theorem_zero_or_source_bound", "MISSING_BALPHA_BOUND_OR_ZERO_THEOREM", "dimensionless_per_normalized_Xhat", str(OUT / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv"), "clock;fine_structure;EM;R10"),
        ("BCP2158_4_bmarker", "b_marker", "vertical derivative of material/source/preparation/readout marker", "|b_marker| <= theorem_zero_or_source_bound", "MISSING_BMARKER_BOUND_OR_ZERO_THEOREM", "dimensionless", str(OUT / "P8_Y5_PARENT_QLOC_1850_SURVIVING_MARKER_FAMILY_AUDIT.csv"), "WEP_source_charge;R10;clock;readout"),
        ("BCP2158_5_delta_kappa_A", "delta_kappa_A", "relative source-only species/source current weight", "|delta_kappa_A| <= theorem_zero_or_source_bound", "MISSING_DELTA_KAPPA_A_BOUND_OR_ZERO_THEOREM", "dimensionless", str(OUT / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv"), "WEP_source_charge;orbital;R10_source_mass"),
        ("BCP2158_6_qnonH", "q_nonH", "non-Hilbert/source/domain/memory tail", "|q_nonH| <= theorem_zero_or_source_bound", "MISSING_QNONH_BOUND_OR_ZERO_THEOREM", "dimensionless_after_source_normalization", str(OUT / "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv"), "R10;orbital;source_normalization;boundary"),
        ("BCP2158_7_Delta_W_support", "Delta_W_support", "source worldtube/support shift under projection", "|Delta_W_support| <= theorem_zero_or_source_bound", "MISSING_SUPPORT_SHIFT_BOUND_OR_ZERO_THEOREM", "dimensionless_or_projection_declared", str(OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv"), "orbital;R10;boundary;local_GR"),
        ("BCP2158_8_qboundary", "q_boundary", "boundary/local projection flux contribution", "|q_boundary| <= theorem_zero_or_source_bound", "MISSING_QBOUNDARY_BOUND_OR_ZERO_THEOREM", "dimensionless_after_boundary_normalization", str(OUT / "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv"), "boundary;orbital;local_GR;R10"),
        ("BCP2158_9_Creadout", "C_readout", "post-variation source/readout selector or measured-G absorption tail", "|C_readout| <= theorem_zero_or_source_bound", "MISSING_READOUT_SELECTOR_ZERO_OR_NUMERIC_BOUND", "dimensionless_or_declared_projection_units", str(OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv"), "orbital;clock;WEP;R10"),
        ("BCP2158_10_total", "JX_qbarXT_abs_envelope", "absolute no-cancellation total source/test coupling", "sum_abs_components", "SCHEMA_READY_VALUES_MISSING", "declared_common_normalization_required", str(OUTPUTS["jx_decomposition"]), "all_local_arenas"),
    ]
    return [row(row_id=row_id, symbol=symbol, definition=definition, formula_or_bound=formula_or_bound, current_status=current_status, units=units, source_path=source_path, observable_link=observable_link) for row_id, symbol, definition, formula_or_bound, current_status, units, source_path, observable_link in data]


def arena_projection_rows() -> list[dict[str, object]]:
    data = [
        ("APR2158_0_R10", "R10 short-range fifth force", "alpha_R10(lambda)=K_X(lambda) Qbar_XH(lambda) qbar_XT_bound_abs tau_R10(lambda)", "K_X;Qbar_XH;lambda_X;qbar_XT_bound_abs;tau_R10;real alpha_bound(lambda)", "MISSING_ARENA_PROJECTION", "no R10 score"),
        ("APR2158_1_WEP", "WEP/source charge", "eta_AB <= tau_WEP dot abs(differential component vector_AB)", "material-pair sensitivities;component bounds;tau_WEP;source paths", "MISSING_ARENA_PROJECTION", "no MICROSCOPE/source-charge score"),
        ("APR2158_2_PPN", "PPN/preferred frame and weak field", "PPN_residual_vector <= tau_PPN dot absolute_component_vector", "tau_PPN;frame/disformal/source-tail projections", "MISSING_ARENA_PROJECTION", "no PPN pass"),
        ("APR2158_3_clock", "clock/redshift/fine-structure", "clock_residual <= tau_clock dot abs(c_g,b_A,b_alpha,b_marker,q_nonH,C_readout)", "clock sensitivities;constant derivatives;source paths", "MISSING_ARENA_PROJECTION", "no clock pass"),
        ("APR2158_4_orbital", "orbital/source-support systems", "orbital_residual <= tau_orbital dot abs(delta_kappa_A,q_nonH,Delta_W_support,q_boundary,C_readout)", "worldtube/support/source-normalization map", "MISSING_ARENA_PROJECTION", "no orbital/local-GM pass"),
        ("APR2158_5_local_GR", "local GR/Newton reduction", "requires source-zero theorem or all residual projections below local bounds with no-cancellation", "parent source-zero or source-backed component vector", "BLOCKED_PENDING_SOURCE_SILENCE_OR_BOUNDS", "no local-GR claim"),
    ]
    return [row(projection_id=projection_id, arena=arena, formula_or_contract=formula_or_contract, required_inputs=required_inputs, current_status=current_status, claim_effect=claim_effect) for projection_id, arena, formula_or_contract, required_inputs, current_status, claim_effect in data]


def local_gr_gate_rows() -> list[dict[str, object]]:
    data = [
        ("LGS2158_0_parent_owner", "same Xhat/vertical source variable is parent-owned", False, "2156/2157 keep owner/metric unsigned"),
        ("LGS2158_1_positive_operator", "positive self-adjoint local operator for Xhat", False, "Z_X/M_X^2/operator signs remain unsigned"),
        ("LGS2158_2_source_zero", "J_X=0 channel-by-channel", False, "2158 source-zero premises do not close together"),
        ("LGS2158_3_boundary_zero", "boundary/local projection flux zero or bounded to zero", False, "boundary/support/domain tails remain live"),
        ("LGS2158_4_no_zero_mode", "no topological/gauge zero mode leaks into local readout", False, "domain/kernel gate remains unsigned"),
        ("LGS2158_5_nohair_result", "positive energy identity forces Xhat=0 in local exterior", False, "only conditional if LGS2158_0 through LGS2158_4 pass"),
        ("LGS2158_6_GR_Newton_limit", "matter sees only GR/Newton observed fields locally", False, "source-zero/no-pole and bounded residual gates remain blocked"),
    ]
    return [row(gate_id=gate_id, requirement=requirement, gate_pass=gate_pass, reason=reason) for gate_id, requirement, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2158_0_JX_zero", "J_X=0", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED", "BLOCKED", "SPG2158_0 through SPG2158_7 do not all pass", False),
        ("REF2158_1_qbarXT_zero", "qbar_XT=0", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED", "BLOCKED", "matter functor/no-marker/source-tail premises unsigned", False),
        ("REF2158_2_component_values", "JX/qbarXT bounded component vector", "SCHEMA_READY_VALUES_MISSING", "BLOCKED", "BCP2158 components have MISSING_* values and no source-backed rows", False),
        ("REF2158_3_local_GR", "local GR/Newton recovered", "SOURCE_SILENCE_AND_NOHAIR_UNSIGNED", "BLOCKED", "local-GR source silence and positive-operator gates fail", False),
        ("REF2158_4_empirical_scores", "R10/WEP/clock/PPN/orbital pass", "ARENA_PROJECTIONS_MISSING", "BLOCKED", "tau/projection rows and source-backed components missing", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2158_0_sources_registered", "2158 source chain exists", False, "source chain supports audit continuity only"),
        ("CG2158_1_source_zero_identity", "J_X/qbar_XT zero theorem is claim-active", False, "identity is exact but premises are unsigned"),
        ("CG2158_2_component_pack_values", "bounded coupling component vector is source-backed", False, "all live component rows are values-missing"),
        ("CG2158_3_arena_projection", "R10/WEP/clock/PPN/orbital projections are score-ready", False, "projection tau maps and component values are missing"),
        ("CG2158_4_nohair_local_GR", "positive no-hair plus source silence gives local GR", False, "operator/source/boundary/domain gates are unsigned"),
        ("CG2158_5_public_claim", "public local-GR/Newton reduction claim is allowed", False, "no claim gate passes"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2158_0_exact_identity", "The source-zero identity is exact but conditional.", "The chain-rule variation makes qbar_XT/J_matter vanish if ordinary matter descends through quotient observables with X-trivial constants and no hidden tails.", "keep it as the parent action contract, not as a current claim"),
        ("DEC2158_1_live_components", "The coupling problem is now one source-current vector.", "Every surviving loophole is assigned to geometry, constants, marker, source-weight, non-Hilbert, boundary or readout components.", "source or theorem-zero components one by one"),
        ("DEC2158_2_local_GR_status", "Local GR/Newton is still blocked but better targeted.", "If source-zero plus positive no-hair closes, local scalar/readout residuals vanish; if not, bounded residual vectors must be scored.", "do not run public local tests until source-current rows are real"),
        ("DEC2158_3_next_target", "Next target is parent ordinary-matter signature or first coupling bound row.", "The cleanest derivation route is signing the MOMS-style matter action; the fallback is sourcing the first component bound without claiming a pass.", "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2158_0_2159",
            "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md",
            "scripts/Y5_R2FR_parent_ordinary_matter_signature_or_first_coupling_bound_row_2159.py",
            "try to parent-sign the ordinary-matter quotient signature that proves J_X=qbar_XT=0; if unsigned, source the first real c_g/b_A/b_alpha/delta_kappa/q_nonH/support bound row as nonclaim input",
            "selected",
            "MOMS-style signature closes from one parent action, or at least one coupling component becomes theorem-zero/source-backed while all local claims remain blocked",
        ),
        (
            "NEXT2158_1_parallel",
            "2159b-Y5-R2FR-positive-nohair-source-silence-assembly.md",
            "scripts/Y5_R2FR_positive_nohair_source_silence_assembly_2159b.py",
            "assemble parent owner, positive operator, J_X=0, boundary silence and no-zero-mode gates into one local-GR theorem checklist",
            "held",
            "only useful after source-zero or component bounds improve",
        ),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(identity: list[dict[str, object]], decomposition: list[dict[str, object]], components: list[dict[str, object]], projections: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2158_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_JX_QBARXT_2158_NONCLAIM.csv", identity + decomposition),
        ("COPY2158_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2158_COUPLING_COMPONENTS_NONCLAIM.csv", components + projections),
        ("COPY2158_2_acquisition_queue", QUEUE / "JR2158_PARENT_MATTER_SIGNATURE_OR_FIRST_BOUND_ROW_QUEUE.csv", next_rows + components),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    identity: list[dict[str, object]],
    premises: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    components: list[dict[str, object]],
    projections: list[dict[str, object]],
    local_gr: list[dict[str, object]],
    refusals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    identity_ok = any(item["identity_id"] == "SZI2158_4_verdict" and item["status"] == "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED" for item in identity)
    premise_ok = any(item["gate_id"] == "SPG2158_7_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM" for item in premises)
    decomposition_ok = any(item["component_id"] == "JQD2158_7_total_abs_guard" and item["current_status"] == "SCHEMA_READY_VALUES_MISSING" for item in decomposition)
    component_ok = any(item["row_id"] == "BCP2158_10_total" and item["current_status"] == "SCHEMA_READY_VALUES_MISSING" for item in components) and all(not truthy(item.get("valid_for_claim", False)) for item in components)
    projection_ok = any(item["projection_id"] == "APR2158_5_local_GR" and item["current_status"] == "BLOCKED_PENDING_SOURCE_SILENCE_OR_BOUNDS" for item in projections)
    local_gr_ok = all(not truthy(item.get("gate_pass", False)) for item in local_gr)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    gates_ok = all(not truthy(item.get("gate_pass", False)) and not truthy(item.get("claim_allowed", False)) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2158_3_next_target" and "ordinary-matter" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2158_0_2159" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for group in (premises, decomposition, components, projections) for item in group if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, identity, premises, decomposition, components, projections, local_gr, refusals, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2158_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, identity_ok, premise_ok, decomposition_ok, component_ok, projection_ok, local_gr_ok, refusal_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2158_00_sources", sources_ok, "2157 handoff and source-zero precedents validate"),
        ("VAL2158_01_identity", identity_ok, "source-zero identity is exact but nonclaim"),
        ("VAL2158_02_premise_gate", premise_ok, "premise gate blocks current source-zero claim"),
        ("VAL2158_03_decomposition", decomposition_ok, "JX/qbarXT decomposition includes total absolute guard"),
        ("VAL2158_04_component_pack", component_ok, "bounded coupling component pack remains values-missing and nonclaim"),
        ("VAL2158_05_arena_projection", projection_ok, "arena projections remain blocked pending real inputs"),
        ("VAL2158_06_local_gr_gate", local_gr_ok, "local-GR gates remain blocked"),
        ("VAL2158_07_refusals", refusal_ok, "refusal runner blocks zero, bounds, local-GR and empirical claims"),
        ("VAL2158_08_claim_gates", gates_ok, "all claim gates keep claim_allowed=false"),
        ("VAL2158_09_decision_next", decisions_ok, "decision ledger selects parent matter signature or first bound row"),
        ("VAL2158_10_next", next_ok, "2159 next target selected"),
        ("VAL2158_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2158_12_csv_parse", csv_ok, "all generated 2158 CSVs parse cleanly"),
        ("VAL2158_13_missing_not_ready", missing_not_ready, "MISSING_* rows stay nonclaim"),
        ("VAL2158_14_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2158_15_formalization_clean", formalization_clean, "formalization-workbench untouched by 2158"),
        ("VAL2158_16_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2158_OVERALL", all_ok, "2158 consolidates JX/qbarXT source-zero identity and bounded coupling component pack."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    identity: list[dict[str, object]],
    premises: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    components: list[dict[str, object]],
    projections: list[dict[str, object]],
    local_gr: list[dict[str, object]],
    refusals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2157, _ = find_line(DOCS["2157"], ["NEXT2157_0_2158"])
    line_1044, _ = find_line(DOCS["1044"], ["MPD1044_7_exact_theorem_if_signed"])
    line_1088, _ = find_line(DOCS["1088"], ["THM1088_5_conclusion"])
    content = "\n\n".join(
        [
            "# 2158 - Y5/R2FR JX/qbarXT Source-Zero Or Bounded Coupling Component Pack",
            "## Current Verdict",
            "2158 does **not** prove `J_X=0`, `qbar_XT=0`, local GR/Newton, R10/WEP/clock/PPN/orbital safety, or any public claim.",
            "It does consolidate the clean source-side theorem: the vertical variation of ordinary matter vanishes if the observed matter frame descends through `q`, constants are vertical-trivial, matter lifts are gauge/EOM/boundary only, no species/source weights or shadow frames exist, variation happens before readout, and boundary/domain tails are silent.",
            "That exact identity is useful because it says what must be true for MTS to reduce locally to GR without tuning. It also names every surviving loophole as a source-current component rather than letting coupling remain fog.",
            f"This follows the current 2157 handoff at line {line_2157}, the 1044 exact matter-pullback theorem at line {line_1044}, and the 1088 MOMS source-zero conclusion at line {line_1088}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Source-Zero Identity",
            md_table(identity, ["identity_id", "step", "mathematical_statement", "result", "status", "missing_for_claim", "valid_for_claim"]),
            "## Source-Zero Premise Gate",
            md_table(premises, ["gate_id", "premise", "needed_for", "current_status", "if_missing", "valid_for_claim"]),
            "## JX/qbarXT Decomposition",
            md_table(decomposition, ["component_id", "component", "definition", "formula_or_bound", "current_status", "required_symbols", "observable_links", "valid_for_claim"]),
            "## Bounded Coupling Component Pack",
            md_table(components, ["row_id", "symbol", "definition", "formula_or_bound", "current_status", "units", "source_path", "observable_link", "valid_for_claim"]),
            "## Arena Projection Rows",
            md_table(projections, ["projection_id", "arena", "formula_or_contract", "required_inputs", "current_status", "claim_effect", "valid_for_claim"]),
            "## Local GR Source Silence Gate",
            md_table(local_gr, ["gate_id", "requirement", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Refusal Runner",
            md_table(refusals, ["refusal_id", "attempted_claim", "input_status", "runner_result", "blocked_by", "score_eligible", "claim_allowed", "valid_for_claim"]),
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
            "This is a proper leap forward: source silence is no longer a slogan. The local-GR path is now a hard contract: either sign the ordinary-matter parent signature and kill `J_X/qbar_XT`, or source each surviving coupling component with an absolute no-cancellation bound. That is how we stop this branch being vibes with equations.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    identity = source_zero_identity_rows()
    premises = premise_gate_rows()
    decomposition = jx_decomposition_rows()
    components = component_pack_rows()
    projections = arena_projection_rows()
    local_gr = local_gr_gate_rows()
    refusals = refusal_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["source_zero_identity"], identity)
    write_csv(OUTPUTS["premise_gate"], premises)
    write_csv(OUTPUTS["jx_decomposition"], decomposition)
    write_csv(OUTPUTS["component_pack"], components)
    write_csv(OUTPUTS["arena_projection"], projections)
    write_csv(OUTPUTS["local_gr_gate"], local_gr)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(identity, decomposition, components, projections, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, identity, premises, decomposition, components, projections, local_gr, refusals, gates, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, identity, premises, decomposition, components, projections, local_gr, refusals, gates, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2158 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
