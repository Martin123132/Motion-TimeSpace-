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


DOC = ROOT / "2129-Y5-R2FR-EH-operator-selection-or-nonEH-residual-vector.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2128_NEXT = OUT / "P8_Y5_PARENT_QLOC_2128_NEXT_TARGET.csv"
CSV_2128_VAL = OUT / "P8_Y5_BRR545_2128_VALIDATION.csv"
CSV_2128_GATES = OUT / "P8_Y5_PARENT_QLOC_2128_REMAINING_LOCAL_GR_GATE_MAP.csv"
CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"
CSV_1963_NO_GAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"
CSV_655_EH = OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv"
CSV_1670_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1670_ARENA_PROJECTION_UPDATE.csv"
CSV_LOCAL_TEMPLATE = OUT / "MTS_local_residual_predictions_TEMPLATE.csv"
CSV_2117_EXCEPTIONS = OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv"
CSV_2118_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_2041_NEF = SOURCE_WEIGHT_DOCS / "AFRAME_NO_EXTRA_FIELD_2041_NONCLAIM.csv"
DOC_2041 = ROOT / "2041-Y5-R2FR-second-order-no-extra-field-parent-clause-or-R11-priority-fill.md"
DOC_440 = ROOT / "440-metric-only-second-order-sector-reduction-attempt.md"
DOC_655 = ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2129_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2129-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2129*",
        "*Y5_R2FR_EH_operator_selection_or_nonEH_residual_vector_2129*",
        "*AFRAME_EH_OPERATOR_SELECTION_2129*",
        "*JR2129*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2129_00_2128_next", CSV_2128_NEXT, ["NEXT2128_0_2129", "EH-operator-selection"], "2128 handoff selects EH/operator selection or non-EH residual vector."),
        ("SRC2129_01_2128_validation", CSV_2128_VAL, ["VAL2128_OVERALL", "PASS"], "2128 validation passed."),
        ("SRC2129_02_2128_gate", CSV_2128_GATES, ["LGR2128_1_EH_operator_selection", "OPEN"], "EH/operator selection is the remaining left-hand GR gate."),
        ("SRC2129_03_1963_action", CSV_1963_ACTION, ["ACT1963_3_geometry_term", "GENERAL_LOCAL_OPERATOR_RETAINED"], "1963 action keeps a general local geometry operator."),
        ("SRC2129_04_1963_no_gamma", CSV_1963_NO_GAMMA, ["NGT1963_3_not_EH", "SCOPE_LIMIT_EXPLICIT"], "no-Gamma/LC branch does not select EH."),
        ("SRC2129_05_655_premises", CSV_655_EH, ["EHP655_P5_local_4D_metric_action", "EHP655_P6_second_order", "EHP655_P9_PPN_completion"], "EH-only premise audit remains unsigned."),
        ("SRC2129_06_2041_no_extra", CSV_2041_NEF, ["NEF2041_1_Lovelock_implication", "NEF2041_7_verdict"], "no-extra-field/Lovelock implication exists only conditionally."),
        ("SRC2129_07_2041_doc", DOC_2041, ["Lovelock/EH implication is clean only if", "current corpus does not yet sign those premises"], "2041 narrative blocks EH promotion from Lovelock alone."),
        ("SRC2129_08_440_doc", DOC_440, ["higher_curvature_metric_operators", "metric_only_second_order_derived"], "440 sector-reduction attempt leaves metric-only/second-order unclosed."),
        ("SRC2129_09_655_doc", DOC_655, ["EH-only theorem route remains unsigned", "R11 Retained Operator Vector Status"], "655 already framed EH-or-R11 fork."),
        ("SRC2129_10_1670_update", CSV_1670_UPDATE, ["MISSING_WEAK_FIELD_METRIC_RESPONSE", "MISSING_POST_NEWTONIAN_SECOND_ORDER_RESPONSE"], "R3/R4 weak-field response still missing."),
        ("SRC2129_11_local_template", CSV_LOCAL_TEMPLATE, ["R11_EH_operator_ledger", "non_EH_operator_coefficients"], "local residual template has R11 operator row."),
        ("SRC2129_12_2117_exceptions", CSV_2117_EXCEPTIONS, ["SEC2117_0_gravity_geometry", "SEC2117_9_verdict"], "sector exceptions block promotion."),
        ("SRC2129_13_2118_kernels", CSV_2118_KERNELS, ["KSR2118_2_clock_redshift_kernel", "KSR2118_7_total_no_cancellation"], "readout/source kernels remain retained."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    return rows


def eh_selector_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="EHS2129_0_target",
            statement="Select Einstein-Hilbert plus Lambda as the compact local exterior geometry operator.",
            math_form="S_loc[e]=int sqrt(-g) [(2 kappa)^-1 (R - 2 Lambda)] + boundary/topological terms",
            status="TARGET_NOT_CLAIM",
            implication="This is the GR/Newton left-hand target, not something the current parent action has earned.",
            blocker="ACT1963_3 still permits general L_loc(e,R,nabla R,Xi,nabla Xi,...).",
        ),
        row(
            theorem_id="EHS2129_1_diffeomorphism_ward",
            statement="Diffeomorphism invariance gives a conserved metric Euler tensor but does not uniquely select EH.",
            math_form="delta S_loc = 1/2 int sqrt(-g) E^{mu nu} delta g_{mu nu}; nabla_mu E^{mu nu}=0 on the reduced branch",
            status="CONDITIONAL_FORMAL_STEP",
            implication="Bianchi/Noether conservation is necessary for GR compatibility.",
            blocker="Conserved non-EH tensors from higher-curvature, scalar, vector, boundary or nonlocal sectors remain legal.",
        ),
        row(
            theorem_id="EHS2129_2_lovelock_selector",
            statement="If the compact exterior is 4D, local, metric-only, diffeomorphism invariant, and second order, then the local tensor is EH plus Lambda, up to topological/boundary normalization.",
            math_form="E^{mu nu}=a G^{mu nu}+b g^{mu nu}; in 4D the Gauss-Bonnet density is locally topological under the usual assumptions",
            status="CONDITIONAL_THEOREM_VALID",
            implication="This is the cleanest mathematical bridge from MTS local geometry to GR.",
            blocker="The bridge activates only after metric-only, no-extra-field, second-order and boundary-harmless premises are parent-signed.",
        ),
        row(
            theorem_id="EHS2129_3_parent_premise_status",
            statement="The current corpus does not parent-sign the Lovelock selector premises.",
            math_form="NEF2041_2..NEF2041_6 and EHP655_P3..P7 are unsigned/open; ACT1963_3 retains general operators.",
            status="PREMISES_UNSIGNED",
            implication="EH/operator selection is not derived in 2129.",
            blocker="No parent theorem forbids R^2, f(R), Ricci^2, Weyl^2, scalar/class, vector/domain, torsion/nonmetricity, nonlocal, boundary, source-normalization or projector operators.",
        ),
        row(
            theorem_id="EHS2129_4_countermodel_family",
            statement="Adding a small conserved non-EH operator is still compatible with covariance but changes PPN/local tests.",
            math_form="E^{mu nu}=G^{mu nu}+Lambda g^{mu nu}+sum_i c_i H_i^{mu nu}, with nabla_mu H_i^{mu nu}=0 for covariant operator families",
            status="COUNTERMODEL_RETAINED",
            implication="The theory can still be viable as a modified-gravity branch, but not as derived local GR until c_i=0/topological/bounded.",
            blocker="Need theorem-zero, topological no-hair, infinite-mass/decoupling, or executable coefficient rows for every c_i.",
        ),
        row(
            theorem_id="EHS2129_5_verdict",
            statement="2129 derives the exact EH-selection contract but rejects EH promotion from the current evidence.",
            math_form="EH_claim = Lovelock_selector and parent_signed(P_metric_only,P_no_extra,P_second_order,P_boundary); current value false",
            status="EH_SELECTION_NOT_DERIVED_R11_VECTOR_RETAINED",
            implication="This is progress: the wall is no longer vague; it is a finite premise/vector ledger.",
            blocker="Next work must attack second-order/no-extra selector or fill the first real non-EH coefficient path.",
        ),
    ]


def premise_audit_rows() -> list[dict[str, object]]:
    return [
        row(premise_id="P2129_0_owned_coframe_LC", premise="observed coframe/LC candidate branch exists", needed_for="metric variable definition", current_status="CONDITIONAL_SUPPORT", evidence="ACT1963_1; ACT1963_5; NGT1963_0", closes_EH_selector=False, next_action="carry as branch support only"),
        row(premise_id="P2129_1_local_4D_metric_only", premise="surviving compact exterior depends only on g_obs/e_obs", needed_for="Lovelock selector", current_status="UNSIGNED", evidence="EHP655_P5; NEF2041_2", closes_EH_selector=False, next_action="prove all extra sectors absent/gauge/topological/no-haired or retain them"),
        row(premise_id="P2129_2_no_extra_fields", premise="no scalar/vector/bulk/domain/memory/source-marker field contributes to local compact tests", needed_for="metric-only and no fifth-force leakage", current_status="UNSIGNED", evidence="EHP655_P3; NEF2041_4; SEC2117", closes_EH_selector=False, next_action="sector-by-sector no-hair or coefficient vector"),
        row(premise_id="P2129_3_second_order", premise="local metric equations are second order through tested scales", needed_for="exclude higher-curvature/nonlocal conserved tensors", current_status="CENTRAL_UNSIGNED_BLOCKER", evidence="EHP655_P6; NEF2041_3; 440 sector reduction", closes_EH_selector=False, next_action="derive second-order selector or retain R2/fR/Ricci/Weyl/nonlocal rows"),
        row(premise_id="P2129_4_boundary_topological_harmless", premise="boundary/topological/projector/domain terms do not source compact local observables", needed_for="prevent bypass of EH tensor", current_status="UNSIGNED", evidence="EHP655_P7; NEF2041_6; SEC2117_7", closes_EH_selector=False, next_action="prove boundary collar/topological silence or bound residuals"),
        row(premise_id="P2129_5_source_normalization", premise="kappa/G_eff/M_eff/measured GM are universal and range independent", needed_for="Newton and PPN interpretation after EH", current_status="OPEN_DOWNSTREAM", evidence="EHP655_P8; LGR2128_2", closes_EH_selector=False, next_action="keep separate from EH operator; do not use it as EH proof"),
        row(premise_id="P2129_6_PPN_completion", premise="weak-field solution gives gamma=beta=1 and no preferred-frame/location tails in observed frame", needed_for="local GR claim", current_status="OPEN_DOWNSTREAM", evidence="EHP655_P9; 1670 update", closes_EH_selector=False, next_action="derive only after EH/operator and source normalization gates"),
        row(premise_id="P2129_7_selector_activation", premise="all Lovelock selector premises parent-signed", needed_for="EH operator promotion", current_status="FALSE_CURRENT_CORPUS", evidence="2129 audit", closes_EH_selector=False, next_action="no EH/Newton/PPN/local-GR claim"),
    ]


def non_eh_operator_rows() -> list[dict[str, object]]:
    return [
        row(vector_id="NEH2129_0_R2_fR_scalar", operator_family="R2/f(R) scalar mode", coefficient_symbol="c_R2, f_RR", operator_form="sqrt(-g)(c_R2 R^2 + f_extra(R))", units_or_normalization="length^2 after EH normalization or equivalent scalar mass map", why_retained="second-order restriction not parent-signed", affected_rows="R3;R4;R10;R11", weak_field_signature="scalar slip, beta tail, Yukawa/fifth-force if finite mass/coupling", minimum_to_clear="prove c_R2=f_RR=0/topological/decoupled or source coefficient plus alpha(lambda) map", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_1_Ricci_Weyl_squared", operator_family="Ricci^2/Weyl^2 curvature", coefficient_symbol="c_Ricci2, c_Weyl2", operator_form="sqrt(-g)(c_Ricci2 R_mn R^mn + c_Weyl2 C_mnrs C^mnrs)", units_or_normalization="length^2 after EH normalization", why_retained="higher-curvature tensors remain covariant and conserved", affected_rows="R3;R4;R8;R11", weak_field_signature="metric slip, tidal/preferred-location response, higher-derivative exterior corrections", minimum_to_clear="topological combination, coefficient-zero theorem, or weak-field residual map", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_2_scalar_class_metric", operator_family="scalar/class metric coupling", coefficient_symbol="c_phiR, c_CR", operator_form="sqrt(-g)(F(phi,C)R - kinetic - V)", units_or_normalization="dimensionless F shift plus scalar mass/range", why_retained="quotient-invariant class scalar/marker silence not parent-signed", affected_rows="R2;R3;R4;R9;R10;R11", weak_field_signature="clock drift, gamma/beta shift, Gdot, finite-range force", minimum_to_clear="prove scalar constant universal with zero stress/source charge or map residuals", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_3_vector_domain", operator_family="vector/domain preferred frame", coefficient_symbol="c_VR, c_domain", operator_form="V_mu V_nu R^mu nu, domain-normal/projector-vector stress", units_or_normalization="dimensionless or length^0 after vector normalization", why_retained="domain/projector/vector no-hair not parent-signed", affected_rows="R5;R6;R7;R8;R11", weak_field_signature="alpha1, alpha2, alpha3, preferred-location xi", minimum_to_clear="prove absent/gauge/aligned stress-free vector or map preferred-frame coefficients", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_4_torsion_nonmetricity", operator_family="torsion/nonmetricity connection", coefficient_symbol="c_T, c_Q", operator_form="T^2, Q^2, independent connection or nonmetricity couplings", units_or_normalization="connection-scale normalized coefficient", why_retained="no-independent-connection branch is conditional, not globally canonical", affected_rows="R0;R1;R2;R11", weak_field_signature="WEP geometry/source slip, clock/light/spin readout deviations", minimum_to_clear="parent LC theorem in every readout/source sector or P4 coefficient maps", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_5_bulk_X_force", operator_family="bulk-X/load finite-range force", coefficient_symbol="c_X, m_X, alpha_X", operator_form="source-coupled massive/bulk auxiliary sector", units_or_normalization="mass/range lambda_X plus source charge normalization", why_retained="positive source-free no-hair not parent-signed", affected_rows="R1;R3;R4;R10;R11", weak_field_signature="composition/source leakage and Yukawa-like short-range force", minimum_to_clear="source-free no-hair or source-backed alpha_X(lambda_X) map", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_6_nonlocal_memory", operator_family="nonlocal/memory kernel", coefficient_symbol="c_NL, K(x,x')", operator_form="R Box^-1 R or history/domain kernel", units_or_normalization="kernel norm with length/time support", why_retained="compact-local kernel silence not parent-signed", affected_rows="R7;R9;R10;R11", weak_field_signature="momentum nonconservation, Gdot, fifth-force/range tails", minimum_to_clear="prove compact-local screening/silence or bound kernel norm", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_7_boundary_hair", operator_family="boundary/topological hair", coefficient_symbol="c_B, c_ref", operator_form="boundary/reference/domain collar terms not purely topological-harmless", units_or_normalization="surface/collar normalized coefficient", why_retained="boundary projection silence remains unsigned", affected_rows="R3;R4;R7;R8;R9;R11", weak_field_signature="radial/shear/preferred-location/source-calibration leakage", minimum_to_clear="GHY/reference/topological no-hair proof or boundary coefficient map", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_8_source_normalization", operator_family="source-normalization operator", coefficient_symbol="delta_kappa, delta_mu, c_source", operator_form="G_eff M_eff, Pi_M J_H, mu_extra or range/time/source charge operator", units_or_normalization="dimensionless, yr^-1, or range-dependent after measured-G quotient", why_retained="EH equation does not by itself prove measured Newtonian GM", affected_rows="R1;R4;R9;R10;R11", weak_field_signature="source WEP, beta calibration, Gdot, range-dependent G", minimum_to_clear="constant universal measured-GM theorem or source residual coefficient rows", status="RETAINED_NONCLAIM"),
        row(vector_id="NEH2129_9_projector_domain_stress", operator_family="projector/domain stress", coefficient_symbol="c_Pi, c_D", operator_form="projector stress, moving-domain support, representative-selection stress", units_or_normalization="dimensionless stress norm or domain length normalization", why_retained="selector/domain stress accounting remains open", affected_rows="R5;R6;R7;R8;R11", weak_field_signature="preferred-frame/location and nonconservation residuals", minimum_to_clear="show projector metric-independent/topological or map stress residuals", status="RETAINED_NONCLAIM"),
    ]


def observable_impact_rows() -> list[dict[str, object]]:
    return [
        row(impact_id="IMP2129_R3_gamma", row_id="R3_gamma", observable="gamma_minus_1", controlling_families="NEH2129_0;NEH2129_1;NEH2129_2;NEH2129_5", status="NOT_SCORE_READY", reason="weak-field spatial metric response not derived; non-EH coefficients symbolic"),
        row(impact_id="IMP2129_R4_beta", row_id="R4_beta", observable="beta_minus_1", controlling_families="NEH2129_0;NEH2129_1;NEH2129_2;NEH2129_8", status="NOT_SCORE_READY", reason="second-order temporal response and source normalization unresolved"),
        row(impact_id="IMP2129_R5_alpha1_R6_alpha2", row_id="R5_R6", observable="alpha1_alpha2", controlling_families="NEH2129_3;NEH2129_9", status="NOT_SCORE_READY", reason="preferred-frame vector/domain response map missing"),
        row(impact_id="IMP2129_R7_alpha3", row_id="R7_alpha3", observable="alpha3", controlling_families="NEH2129_3;NEH2129_6;NEH2129_7;NEH2129_9", status="NOT_SCORE_READY", reason="momentum/domain/boundary exchange cannot be cancelled by assumption"),
        row(impact_id="IMP2129_R8_xi", row_id="R8_xi", observable="xi", controlling_families="NEH2129_1;NEH2129_3;NEH2129_7;NEH2129_9", status="NOT_SCORE_READY", reason="preferred-location/tidal/domain response unresolved"),
        row(impact_id="IMP2129_R9_Gdot", row_id="R9_Gdot", observable="Gdot_over_G", controlling_families="NEH2129_2;NEH2129_6;NEH2129_7;NEH2129_8", status="NOT_SCORE_READY", reason="time-varying source/memory/kernel normalization unresolved"),
        row(impact_id="IMP2129_R10_fifth_force", row_id="R10_fifth_force", observable="alpha(lambda)_or_delta_G", controlling_families="NEH2129_0;NEH2129_2;NEH2129_5;NEH2129_6;NEH2129_8", status="NOT_SCORE_READY", reason="range/mass/coupling map and bound curve chain still missing"),
        row(impact_id="IMP2129_R11_operator", row_id="R11_EH_operator_ledger", observable="non_EH_operator_coefficients", controlling_families="all_NEH2129", status="VECTOR_RETAINED_NONCLAIM", reason="R11 is now explicit for this branch but not executable without coefficients/units/source maps"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2129_0_sources", gate="source evidence loaded", gate_pass=True, rationale="2128/1963/655/2041/440/1670/2117/2118 sources exist and are referenced"),
        row(gate_id="GATE2129_1_conditional_EH_selector", gate="conditional Lovelock/EH selector written", gate_pass=True, rationale="metric-only 4D local second-order route gives EH+Lambda if parent premises are signed"),
        row(gate_id="GATE2129_2_parent_premises_signed", gate="parent signs metric-only/no-extra/second-order/boundary premises", gate_pass=False, rationale="ACT1963 general local operator and NEF2041/EHP655 unsigned premise rows block activation"),
        row(gate_id="GATE2129_3_EH_operator_selection", gate="EH operator selected by MTS parent", gate_pass=False, rationale="conditional theorem exists but MTS premises are not derived"),
        row(gate_id="GATE2129_4_nonEH_vector_retained", gate="non-EH residual vector retained", gate_pass=True, rationale="all main legal operator families are carried as nonclaim R11 rows"),
        row(gate_id="GATE2129_5_Newton_PPN_completion", gate="Newton/PPN completion", gate_pass=False, rationale="source normalization, gamma, beta, readout and empirical gates remain open"),
        row(gate_id="GATE2129_6_local_GR_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="EH selector is inactive and residual vector is symbolic/nonclaim"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2129_0", decision="CONDITIONAL_EH_THEOREM_WRITTEN", because="the Lovelock-style selector is the right mathematical contract for local GR", next_action="do not treat it as evidence until parent premises are signed"),
        row(decision_id="DEC2129_1", decision="EH_PROMOTION_REJECTED_CURRENTLY", because="general local operator and extra-sector/higher-curvature countermodels remain legal", next_action="retain R11 non-EH operator vector"),
        row(decision_id="DEC2129_2", decision="NEXT_ATTACK_SECOND_ORDER_NO_EXTRA_SELECTOR", because="second-order/no-extra is the largest blocker left of PPN/source-normalization", next_action="try to derive parent second-order/no-extra-sector silence; if it fails, start real coefficient acquisition with R2/fR scalar mode"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2129_0_2130",
            next_target="2130-Y5-R2FR-second-order-no-extra-selector-or-R11-coefficient-priority-fill.md",
            script="scripts/Y5_R2FR_second_order_no_extra_selector_or_R11_coefficient_priority_fill_2130.py",
            objective="Try to parent-derive why the compact local exterior is metric-only and second order after all MTS fields are varied; if not derivable, choose the highest-priority non-EH family, likely R2/f(R) scalar mode, and build the first coefficient/bound acquisition row.",
            forbidden_shortcuts="claiming EH from Lovelock without premises; calling covariance conservation enough; ignoring higher-curvature/nonlocal operators; claiming Newton/PPN/local-GR; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    theorem: list[dict[str, object]],
    premises: list[dict[str, object]],
    vector: list[dict[str, object]],
    impacts: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    high_priority = [item for item in vector if item["vector_id"] in {"NEH2129_0_R2_fR_scalar", "NEH2129_1_Ricci_Weyl_squared", "NEH2129_2_scalar_class_metric", "NEH2129_8_source_normalization"}]
    copies = [
        ("COPY2129_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_EH_OPERATOR_SELECTION_2129_NONCLAIM.csv", theorem + premises + gates),
        ("COPY2129_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2129_NONEH_OPERATOR_VECTOR_NONCLAIM.csv", vector + impacts),
        ("COPY2129_2_acquisition_queue", QUEUE / "JR2129_SECOND_ORDER_OR_NONEH_VECTOR_QUEUE.csv", next_rows + high_priority),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    premises: list[dict[str, object]],
    vector: list[dict[str, object]],
    impacts: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    theorem_ok = any(item["theorem_id"] == "EHS2129_2_lovelock_selector" and item["status"] == "CONDITIONAL_THEOREM_VALID" for item in theorem) and any(item["theorem_id"] == "EHS2129_5_verdict" and "NOT_DERIVED" in str(item["status"]) for item in theorem)
    premises_ok = any(item["premise_id"] == "P2129_3_second_order" and not truthy(item["closes_EH_selector"]) for item in premises) and any(item["premise_id"] == "P2129_7_selector_activation" and item["current_status"] == "FALSE_CURRENT_CORPUS" for item in premises)
    vector_ok = len(vector) >= 10 and all(str(item["status"]).startswith("RETAINED") for item in vector) and any(item["vector_id"] == "NEH2129_0_R2_fR_scalar" for item in vector)
    impacts_ok = {item["row_id"] for item in impacts} >= {"R3_gamma", "R4_beta", "R10_fifth_force", "R11_EH_operator_ledger"}
    gates_ok = any(item["gate_id"] == "GATE2129_1_conditional_EH_selector" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2129_6_local_GR_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2129_2" and "SECOND_ORDER_NO_EXTRA" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2129_0_2130" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, theorem, premises, vector, impacts, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2129_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, theorem_ok, premises_ok, vector_ok, impacts_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2129_00_sources", sources_ok, "all cited EH/operator sources exist and contain expected needles"),
        ("VAL2129_01_theorem", theorem_ok, "conditional Lovelock/EH selector is written but verdict blocks promotion"),
        ("VAL2129_02_premises", premises_ok, "second-order/no-extra/selector premises remain unsigned"),
        ("VAL2129_03_nonEH_vector", vector_ok, "retained non-EH operator vector has at least ten nonclaim families"),
        ("VAL2129_04_impacts", impacts_ok, "R3, R4, R10 and R11 observable impacts are mapped"),
        ("VAL2129_05_gates", gates_ok, "conditional selector gate passes while local-GR claim gate fails"),
        ("VAL2129_06_decisions", decisions_ok, "decision ledger selects second-order/no-extra or coefficient fill next"),
        ("VAL2129_07_next", next_ok, "next target is 2130 second-order/no-extra selector or R11 coefficient fill"),
        ("VAL2129_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2129_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2129_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2129_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2129"),
        ("VAL2129_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2129_OVERALL", all_ok, "2129 derives the conditional EH-selection contract, rejects current EH promotion, and retains a nonclaim R11 operator vector."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    premises: list[dict[str, object]],
    vector: list[dict[str, object]],
    impacts: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2129 - Y5/R2FR EH Operator Selection Or Non-EH Residual Vector",
            "## Current Verdict",
            "2129 makes the GR-left-hand wall explicit. The EH route is mathematically clean as a conditional theorem: if the compact local exterior is 4D, local, metric-only, diffeomorphism invariant, second order, and boundary/topological harmless, the surviving geometry operator is EH plus Lambda up to normalization. That is the right contract.",
            "But the current MTS parent branch does not yet sign those premises. The 1963 action still retains a general local operator, 2041 keeps metric-only/no-extra/second-order clauses unsigned, and 655 keeps PPN/source-normalization gates open. Therefore EH, Newton, PPN and local-GR promotion remain false. The honest branch is now: prove the second-order/no-extra selector, or carry the non-EH R11 operator vector.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## EH Selector Theorem Attempt",
            md_table(theorem, ["theorem_id", "statement", "math_form", "status", "implication", "blocker", "valid_for_claim"]),
            "## Premise Audit",
            md_table(premises, ["premise_id", "premise", "needed_for", "current_status", "evidence", "closes_EH_selector", "next_action", "valid_for_claim"]),
            "## Retained Non-EH Operator Vector",
            md_table(vector, ["vector_id", "operator_family", "coefficient_symbol", "operator_form", "units_or_normalization", "why_retained", "affected_rows", "weak_field_signature", "minimum_to_clear", "status", "valid_for_claim"]),
            "## Observable Impact Map",
            md_table(impacts, ["impact_id", "row_id", "observable", "controlling_families", "status", "reason", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    theorem = eh_selector_theorem_rows()
    premises = premise_audit_rows()
    vector = non_eh_operator_rows()
    impacts = observable_impact_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2129_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2129_EH_SELECTOR_THEOREM_ATTEMPT.csv",
        "premises": OUT / "P8_Y5_PARENT_QLOC_2129_PREMISE_AUDIT.csv",
        "vector": OUT / "P8_Y5_PARENT_QLOC_2129_NONEH_OPERATOR_VECTOR.csv",
        "impacts": OUT / "P8_Y5_PARENT_QLOC_2129_OBSERVABLE_IMPACT_MAP.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2129_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2129_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2129_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2129_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2129_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["premises"], premises)
    write_csv(paths["vector"], vector)
    write_csv(paths["impacts"], impacts)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(theorem, premises, vector, impacts, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, theorem, premises, vector, impacts, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem, premises, vector, impacts, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
