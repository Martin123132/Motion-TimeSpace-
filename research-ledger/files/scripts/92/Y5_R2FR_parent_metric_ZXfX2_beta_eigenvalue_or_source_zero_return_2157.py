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


DOC = ROOT / "2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2156": ROOT / "2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
    "2156_next": OUT / "P8_Y5_PARENT_QLOC_2156_NEXT_TARGET.csv",
    "2156_validation": OUT / "P8_Y5_BRR545_2156_VALIDATION.csv",
    "1848": ROOT / "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "1848_validation": OUT / "P8_Y5_BRR545_1848_VALIDATION.csv",
    "1849": ROOT / "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
    "1849_validation": OUT / "P8_Y5_BRR545_1849_VALIDATION.csv",
    "1026": ROOT / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "210": ROOT / "210-GK-alphaK-parent-invariant-or-fixed-closure.md",
    "211": ROOT / "211-GK-parent-metric-Ward-identity-attempt.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2157_SOURCE_REGISTER.csv",
    "parent_metric_lock": OUT / "P8_Y5_PARENT_QLOC_2157_PARENT_METRIC_LOCK_ATTEMPT.csv",
    "trace_eigenvalue": OUT / "P8_Y5_PARENT_QLOC_2157_TRACE_EIGENVALUE_THEOREM_ATTEMPT.csv",
    "rescaling_audit": OUT / "P8_Y5_PARENT_QLOC_2157_RESCALING_DEGENERACY_AUDIT.csv",
    "finite_route": OUT / "P8_Y5_PARENT_QLOC_2157_FINITE_ROUTE_DECISION.csv",
    "source_zero": OUT / "P8_Y5_PARENT_QLOC_2157_SOURCE_ZERO_RETURN.csv",
    "bounded_handoff": OUT / "P8_Y5_PARENT_QLOC_2157_BOUNDED_COUPLING_HANDOFF.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2157_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2157_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2157_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2157_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2157_VALIDATION.csv",
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


def formalization_has_2157_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2157-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2157*",
        "*P8_Y5_BRR545_2157*",
        "*Y5_R2FR_parent_metric_ZXfX2_beta_eigenvalue_or_source_zero_return_2157*",
        "*AFRAME_PARENT_METRIC_TRACE_2157*",
        "*JR2157*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2157_00_2156_handoff", DOCS["2156"], [["NEXT2156_0_2157"], ["FNL2156_1_canonical_metric"], ["FNL2156_2_beta_eigenvalue"]], "current 2156 selects parent metric/eigenvalue or source-zero return."),
        ("SRC2157_01_2156_next_csv", DOCS["2156_next"], [["NEXT2156_0_2157"], ["parent_metric_ZXfX2"], ["source-zero"]], "machine-readable current 2157 target."),
        ("SRC2157_02_2156_validation", DOCS["2156_validation"], [["VAL2156_OVERALL"], ["PASS"]], "current 2156 validation passed as nonclaim."),
        ("SRC2157_03_1848_metric_precedent", DOCS["1848"], [["PM1848_6_verdict"], ["BE1848_4_verdict"], ["SZR1848_5_verdict"]], "old active-branch metric/eigenvalue route fails and returns to qbar/source-zero."),
        ("SRC2157_04_1848_validation", DOCS["1848_validation"], [["VAL1848_OVERALL"], ["PASS"]], "old 1848 validation passed as nonclaim."),
        ("SRC2157_05_1849_source_zero", DOCS["1849"], [["QZ1849_6_verdict"], ["BQT1849_3_total_abs_guard"], ["NEXT1849_0_primary"]], "old 1849 supplies qbarXT/JX source-zero and bounded-coupling component handoff."),
        ("SRC2157_06_1849_validation", DOCS["1849_validation"], [["VAL1849_OVERALL"], ["PASS"]], "old 1849 validation passed as nonclaim."),
        ("SRC2157_07_1026_metric_precedent", DOCS["1026"], [["PM1026_6_verdict"], ["BE1026_4_verdict"], ["DEC1026_1_beta_result"]], "R10 predecessor already found parent metric/beta unowned."),
        ("SRC2157_08_210_metric_warning", DOCS["210"], [["M_AB"], ["field-space metric"], ["fail"]], "early GK checkpoint identifies M_AB as fixed closure rather than derived parent metric."),
        ("SRC2157_09_211_ward_attempt", DOCS["211"], [["Ward identity"], ["M_AB"], ["fail"]], "Ward/current-norm attempt does not derive the parent metric with stress/Bianchi ownership."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def parent_metric_lock_rows() -> list[dict[str, object]]:
    data = [
        (
            "PML2157_0_parent_metric_object",
            "field-space metric restricted to the Xhat direction",
            "G_X := M_AB e_X^A e_X^B",
            "This is the coordinate-invariant object needed before Z_X, f_X or beta can be physical.",
            "TARGET_DEFINED_NOT_OWNED",
            "parent M_AB, normalized e_X, field units, sign convention and stress/Bianchi variation",
        ),
        (
            "PML2157_1_dimensional_amplitude",
            "dimensionful local coordinate",
            "X_phys = f_X x and Z_x = G_X f_X^2 for the dimensionless coordinate x",
            "The relationship is exact once M_AB, e_X and f_X are parent-owned; it also shows why f_X cannot be chosen after local data.",
            "EXACT_RELATION_CONDITIONAL",
            "parent-owned f_X or equivalent clock/rod/readout normalization",
        ),
        (
            "PML2157_2_vacuum_metric_lock",
            "canonical finite-route lock",
            "Z_X f_X^2 = rho_vac^(1/2)",
            "This is a clean contract, but no current source signs the Ward/metric theorem that equates the X norm to the vacuum-density scale.",
            "CLEAN_CONTRACT_NOT_SIGNED",
            "parent Ward/current norm or defect metric theorem with units and no circular local-test calibration",
        ),
        (
            "PML2157_3_stress_bianchi_variation",
            "stress/Bianchi ownership",
            "delta_g(M_AB,e_X,f_X,V_eff) must enter the parent stress tensor consistently",
            "A metric lock is not just a number: it must survive variation of the coframe/metric or it breaks conservation accounting.",
            "MISSING_STRESS_BIANCHI_VARIATION",
            "parent stress variation and Bianchi-compatible conservation identity",
        ),
        (
            "PML2157_4_cross_block_guard",
            "single scalar truncation legality",
            "H_AB must block-diagonalize into Xhat plus positive orthogonal sectors, or the projected Schur complement must be used",
            "Without this, Z_X and M_X^2 are not a standalone physical scalar route.",
            "MISSING_BLOCK_DIAGONAL_OR_SCHUR_PROOF",
            "cross-Hessian matrix, projector/eigenbasis and positive orthogonal block",
        ),
        (
            "PML2157_5_verdict",
            "parent metric lock claim",
            "parent_signed(M_AB,e_X,f_X,V_eff,stress) -> Z_X f_X^2 = rho_vac^(1/2)",
            "The exact contract is now sharper, but the current corpus still does not sign all parent objects from one branch.",
            "FAIL_CURRENT_CLAIM",
            "one parent action clause owning M_AB, e_X, f_X, Hessian spectrum, units and stress variation",
        ),
    ]
    return [row(lock_id=lock_id, target=target, mathematical_statement=mathematical_statement, result=result, status=status, missing_for_claim=missing_for_claim) for lock_id, target, mathematical_statement, result, status, missing_for_claim in data]


def trace_eigenvalue_rows() -> list[dict[str, object]]:
    data = [
        (
            "TET2157_0_spectral_operator",
            "define beta as an eigenvalue, not a fitted number",
            "H^A_B := rho_vac^(-1/2) M^{AC} nabla_C nabla_B V_eff and beta_eff in Spec(H)",
            "This is the correct invariant target if M_AB and V_eff are parent-owned.",
            "CONDITIONAL_DEFINITION_ONLY",
            "parent M_AB, V_eff, covariant field-space Hessian, branch/eigenbasis and units",
        ),
        (
            "TET2157_1_common_amplitude_trace",
            "where beta=3 can appear",
            "For three equal spatial channels z_i=x and U=(k/2) sum_i z_i^2, U(x)=(3k/2)x^2 so U''(0)=3k.",
            "The familiar factor 3 is real only for the unnormalised common-amplitude coordinate x.",
            "CONDITIONAL_COORDINATE_RESULT",
            "parent proof that Xhat is exactly this unnormalised common spatial amplitude",
        ),
        (
            "TET2157_2_normalized_trace_eigenvector",
            "why mode-count beta=3 is not invariant",
            "For the normalized trace eigenvector x_tr=(z_1+z_2+z_3)/sqrt(3), the same quadratic potential gives U=(k/2)x_tr^2 and beta=k after normalization.",
            "The factor 3 evaporates under the parent-normalized eigenvector convention; raw mode counting is therefore not a physical beta prediction.",
            "DERIVED_REJECTION_OF_MODE_COUNT_CLAIM",
            "parent action must choose the coordinate and metric before beta is promoted",
        ),
        (
            "TET2157_3_time_weyl_constraint_leak",
            "extra directions can shift the spectrum",
            "time trace, Weyl, constraint, boundary or memory directions alter the Schur-complement eigenvalue unless projected out by parent algebra",
            "Even beta=1 or beta=3 is unsafe without the full constrained Hessian block.",
            "MISSING_CONSTRAINT_PROJECTION",
            "constraint algebra, gauge quotient, boundary class and positive Schur complement",
        ),
        (
            "TET2157_4_verdict",
            "beta eigenvalue ownership",
            "parent_signed(H spectrum and Xhat normalization) -> beta_eff and lambda_X=ell_vac/sqrt(beta_eff)",
            "Beta remains a good theorem target, but beta=3 from spatial mode counting is rejected as a claim because it is normalization-dependent.",
            "BETA3_MODE_COUNT_REJECTED_AS_CLAIM",
            "parent-normalized Hessian spectrum; not a post-hoc beta or raw dimension count",
        ),
    ]
    return [row(theorem_id=theorem_id, target=target, mathematical_statement=mathematical_statement, derived_result=derived_result, status=status, missing_for_claim=missing_for_claim) for theorem_id, target, mathematical_statement, derived_result, status, missing_for_claim in data]


def rescaling_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "RDA2157_0_field_rescale",
            "X -> a X",
            "Z_X -> Z_X/a^2, M_X^2 -> M_X^2/a^2, J_X -> J_X/a, b_X -> b_X/a",
            "lambda_X=sqrt(Z_X/M_X^2) survives, but amplitudes and beta/source products do not become physical until normalization is parent-fixed.",
            "GUARDRAIL_PASS",
        ),
        (
            "RDA2157_1_vacuum_lock_invariant",
            "f_X compensates coordinate rescaling",
            "if x -> a x then f_X -> f_X/a, so G_X f_X^2 is the invariant metric-amplitude lock",
            "This explains why Z_X f_X^2 is the right object and why neither Z_X nor f_X alone can be used as evidence.",
            "EXACT_RESCALING_LEDGER",
        ),
        (
            "RDA2157_2_beta_coordinate_trap",
            "raw U'' is coordinate-dependent",
            "U'' -> U''/a^2 unless the field-space metric transforms with it and beta is built from M^{-1} Hessian",
            "This is the mathematical reason beta=3 cannot be claimed from trace counting alone.",
            "POSTHOC_BETA_BLOCKED",
        ),
        (
            "RDA2157_3_alpha_product_trap",
            "range and source amplitude are linked",
            "alpha_X(lambda)=K_X Qbar_XH qbar_XT must use the same normalization that fixed Z_X,M_X^2,J_X,b_X",
            "The route cannot choose lambda from Hessian and source amplitude from a separate convention.",
            "ANTI_KNOB_CONSTRAINT_RESTATED",
        ),
        (
            "RDA2157_4_verdict",
            "finite route normalization",
            "only invariant rows survive rescaling: lambda_X plus fully linked source products, or theorem-zero source",
            "The finite route is mathematically disciplined but not claim-grade without parent metric/spectrum/source ownership.",
            "FINITE_ROUTE_NOT_PROMOTED",
        ),
    ]
    return [row(audit_id=audit_id, transformation=transformation, transformation_law=transformation_law, result=result, status=status) for audit_id, transformation, transformation_law, result, status in data]


def finite_route_rows() -> list[dict[str, object]]:
    data = [
        (
            "FRD2157_0_exact_part",
            "second variation and range relation",
            "lambda_X=sqrt(Z_X/M_X^2) remains exact if Z_X and M_X^2 are from one parent-owned Xhat block",
            "RETAIN_AS_CONDITIONAL_MATH",
            "2156 exact contract remains useful.",
            "claim finite range from current corpus",
        ),
        (
            "FRD2157_1_metric_lock",
            "Z_X f_X^2=rho_vac^(1/2)",
            "not parent-signed; no Ward/metric/stress theorem closes",
            "FREEZE_AS_THEOREM_TARGET",
            "future parent metric source can reopen this route.",
            "use rho_vac alone as a range prediction",
        ),
        (
            "FRD2157_2_beta",
            "beta=3 trace route",
            "mode-count beta=3 is convention-dependent unless the parent action chooses the unnormalised spatial common-amplitude coordinate",
            "DEMOTE_TO_CONDITIONAL_NOT_CLAIM",
            "trace route is a possible theorem target, not an active prediction.",
            "score beta=3 as derived",
        ),
        (
            "FRD2157_3_alpha",
            "alpha product",
            "K_X, Qbar_XH, qbar_XT and lambda_X remain missing or normalization-linked",
            "SCHEMA_ONLY_VALUES_MISSING",
            "keep alpha rows ready but nonclaim.",
            "run local tests as if alpha row is sourced",
        ),
        (
            "FRD2157_4_verdict",
            "finite scalar route",
            "finite route is frozen until one parent source signs metric, spectrum, source and boundary normalization together",
            "FINITE_ROUTE_FROZEN_NONCLAIM",
            "return to source-zero/bounded coupling as the lower-scrutiny local-GR path.",
            "local GR/Newton or R10/PPN pass",
        ),
    ]
    return [row(decision_id=decision_id, object=object_name, current_evidence=current_evidence, status=status, allowed_use=allowed_use, forbidden_use=forbidden_use) for decision_id, object_name, current_evidence, status, allowed_use, forbidden_use in data]


def source_zero_rows() -> list[dict[str, object]]:
    data = [
        (
            "SZR2157_0_route_trigger",
            "finite metric/eigenvalue route",
            "NOT_PROMOTED",
            "M_AB/e_X/f_X/stress and beta spectrum are not parent-signed; beta=3 mode count is not invariant.",
            "return to source-zero/no-pole or bounded coupling before empirical alpha claims",
        ),
        (
            "SZR2157_1_qbarXT_JX_zero",
            "matter source-zero theorem",
            "STILL_STRONGEST_IF_PARENT_SIGNED",
            "If matter sees only quotient observables and all constants/markers/tails are vertical-trivial, then qbar_XT=0 and J_matter=0 by chain rule.",
            "attack parent q-kernel, observed coframe, matter functor, no-marker constants and hidden-tail silence together",
        ),
        (
            "SZR2157_2_no_pole",
            "quotient/no-pole theorem",
            "STRONGER_THAN_SMALL_COUPLING_IF_CLOSED",
            "No physical X Green function would make K_X=0 instead of merely bounded.",
            "requires first-class quotient, boundary charge zero and readout/projector silence",
        ),
        (
            "SZR2157_3_bounded_fallback",
            "bounded coupling component envelope",
            "MANDATORY_IF_ZERO_UNSIGNED",
            "Surviving source channels must be rows with units, source paths, observable links and no-cancellation policy.",
            "fill c_g, b_dis, b_A, b_alpha, q_nonH, source-weight and boundary/support rows",
        ),
        (
            "SZR2157_4_verdict",
            "next route",
            "SOURCE_ZERO_OR_BOUNDED_COUPLING_SELECTED",
            "The finite route is not dead, but source-zero/bounded coupling is now the cleaner local-GR branch.",
            "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
        ),
    ]
    return [row(return_id=return_id, route=route, current_status=current_status, because=because, next_use=next_use) for return_id, route, current_status, because, next_use in data]


def bounded_handoff_rows() -> list[dict[str, object]]:
    data = [
        (
            "BCH2157_0_visible_geometry",
            "qbar_geom",
            "|qbar_geom| <= |tau_R10 c_g| + |tau_dis b_dis|",
            "R10;PPN;clock;WEP",
            "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "ordinary matter can see a common Weyl/disformal frame even when WEP spread is small",
        ),
        (
            "BCH2157_1_constants_markers",
            "qbar_marker",
            "|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|",
            "WEP;clock;fine_structure;composition;R10",
            "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "masses, charges, alpha_EM, clock species and material labels can carry X-dependence",
        ),
        (
            "BCH2157_2_source_weight",
            "qbar_source_weight",
            "|qbar_source_weight| <= max_A |kappa_A/kappa_univ - 1| + measured-GM calibration tail",
            "WEP_source_charge;orbital;R10_source_mass",
            "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND",
            "source-only weights can hide in gravitational mass normalization",
        ),
        (
            "BCH2157_3_nonHilbert_tail",
            "qbar_nonH",
            "|qbar_nonH| <= |q_nonH| + |Delta_W_support| + |q_domain| + |q_boundary|",
            "R10;orbital;boundary;source_normalization;local_GR",
            "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "boundary, support, domain and non-Hilbert tails can reintroduce source current",
        ),
        (
            "BCH2157_4_total_abs_guard",
            "qbar_XT_bound_abs",
            "|qbar_XT| <= |qbar_geom| + |qbar_marker| + |qbar_source_weight| + |qbar_nonH|",
            "R10;WEP;clock;PPN;orbital;local_GR",
            "SCHEMA_READY_VALUES_MISSING",
            "no-cancellation envelope prevents accidental smallness from being treated as a theorem",
        ),
    ]
    return [row(handoff_id=handoff_id, component=component, bound_formula=bound_formula, observable_links=observable_links, current_status=current_status, reason_retained=reason_retained) for handoff_id, component, bound_formula, observable_links, current_status, reason_retained in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2157_0_sources_registered", "2157 source chain exists", False, "source chain supports audit continuity only"),
        ("CG2157_1_parent_metric_lock", "Z_X f_X^2=rho_vac^(1/2) is parent-signed", False, "M_AB/e_X/f_X/stress variation are missing"),
        ("CG2157_2_beta_eigenvalue", "beta_eff or beta=3 is parent-signed", False, "mode-count beta=3 is normalization-dependent and no spectrum theorem exists"),
        ("CG2157_3_finite_lambda_claim", "lambda_X is a finite prediction", False, "metric/eigenvalue lock remains unsigned"),
        ("CG2157_4_alpha_product_claim", "alpha(lambda) row can be scored", False, "K_X, Qbar_XH, qbar_XT and source normalization are missing"),
        ("CG2157_5_source_zero_claim", "J_X/qbar_XT source-zero is parent-signed", False, "matter/coframe/no-marker/hidden-tail clauses remain unsigned"),
        ("CG2157_6_local_GR_claim", "local GR/Newton reduction is derived", False, "finite route and source-zero/no-pole route are still unsigned"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2157_0_metric_result",
            "The parent metric lock has a sharper exact contract but is still not owned.",
            "The invariant object is G_X f_X^2, with G_X=M_AB e_X e_X. Current files do not derive M_AB, e_X, f_X and stress/Bianchi variation from one parent action.",
            "keep Z_X f_X^2=rho_vac^(1/2) as theorem target only",
        ),
        (
            "DEC2157_1_beta_result",
            "Beta=3 from spatial mode counting is rejected as a claim.",
            "Three equal channels give U''=3 only in an unnormalised common-amplitude coordinate; a normalized trace eigenvector removes the factor 3.",
            "require a parent-normalized Hessian spectrum before any beta prediction",
        ),
        (
            "DEC2157_2_finite_route",
            "The finite route is frozen, not deleted.",
            "The second-variation/range law remains exact, but range, beta and source amplitude are not tied by one parent normalization ledger.",
            "use finite route only as private closure/pressure testing until parent metric+spectrum+source rows exist",
        ),
        (
            "DEC2157_3_next_target",
            "Next target is J_X/qbar_XT source-zero or bounded coupling component pack.",
            "This is the lower-scrutiny path to local GR: either the source coupling vanishes by parent descent, or every survivor becomes a bounded residual vector.",
            "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
        ),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2157_0_2158",
            "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
            "scripts/Y5_R2FR_JX_qbarXT_source_zero_or_bounded_coupling_component_pack_2158.py",
            "derive J_X=0/qbar_XT=0 from parent matter/coframe/no-marker/hidden-tail descent, or build claim-blocked bounded coupling component rows with units, source paths, observable links and no-cancellation envelope",
            "selected",
            "source-zero closes from one parent branch, or every live coupling component is staged as nonclaim source input",
        ),
        (
            "NEXT2157_1_future_reopen",
            "2158b-Y5-R2FR-parent-metric-spectrum-reopen.md",
            "scripts/Y5_R2FR_parent_metric_spectrum_reopen_2158b.py",
            "reopen finite route only if a source supplies parent M_AB, e_X, f_X, Hessian spectrum, units and stress/Bianchi variation",
            "held",
            "one parent metric/spectrum source replaces the conditional metric/eigenvalue ledger",
        ),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(metric: list[dict[str, object]], trace: list[dict[str, object]], source_zero: list[dict[str, object]], bounded: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2157_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_METRIC_TRACE_2157_NONCLAIM.csv", metric + trace),
        ("COPY2157_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2157_SOURCE_ZERO_HANDOFF_NONCLAIM.csv", source_zero + bounded),
        ("COPY2157_2_acquisition_queue", QUEUE / "JR2157_SOURCE_ZERO_OR_BOUNDED_COUPLING_QUEUE.csv", next_rows + bounded),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    metric: list[dict[str, object]],
    trace: list[dict[str, object]],
    rescale: list[dict[str, object]],
    finite: list[dict[str, object]],
    source_zero: list[dict[str, object]],
    bounded: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    metric_ok = any(item["lock_id"] == "PML2157_5_verdict" and item["status"] == "FAIL_CURRENT_CLAIM" for item in metric)
    trace_ok = any(item["theorem_id"] == "TET2157_2_normalized_trace_eigenvector" and item["status"] == "DERIVED_REJECTION_OF_MODE_COUNT_CLAIM" for item in trace) and any(item["theorem_id"] == "TET2157_4_verdict" and item["status"] == "BETA3_MODE_COUNT_REJECTED_AS_CLAIM" for item in trace)
    rescale_ok = any(item["audit_id"] == "RDA2157_4_verdict" and item["status"] == "FINITE_ROUTE_NOT_PROMOTED" for item in rescale)
    finite_ok = any(item["decision_id"] == "FRD2157_4_verdict" and item["status"] == "FINITE_ROUTE_FROZEN_NONCLAIM" for item in finite)
    source_ok = any(item["return_id"] == "SZR2157_4_verdict" and item["current_status"] == "SOURCE_ZERO_OR_BOUNDED_COUPLING_SELECTED" for item in source_zero)
    bounded_ok = any(item["handoff_id"] == "BCH2157_4_total_abs_guard" and item["current_status"] == "SCHEMA_READY_VALUES_MISSING" for item in bounded) and all(not truthy(item.get("valid_for_claim", False)) for item in bounded)
    gates_ok = all(not truthy(item.get("gate_pass", False)) and not truthy(item.get("claim_allowed", False)) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2157_3_next_target" and "source-zero" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2157_0_2158" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for group in (metric, trace, finite, source_zero, bounded) for item in group if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, metric, trace, rescale, finite, source_zero, bounded, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2157_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, metric_ok, trace_ok, rescale_ok, finite_ok, source_ok, bounded_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2157_00_sources", sources_ok, "2156 handoff and prior metric/source-zero frontiers validate"),
        ("VAL2157_01_metric_lock_blocks", metric_ok, "parent metric lock remains unsigned"),
        ("VAL2157_02_trace_beta_rejection", trace_ok, "beta=3 mode-count claim is rejected by normalization audit"),
        ("VAL2157_03_rescaling_guard", rescale_ok, "field-rescaling degeneracy keeps finite route nonclaim"),
        ("VAL2157_04_finite_frozen", finite_ok, "finite route frozen as theorem target only"),
        ("VAL2157_05_source_zero_selected", source_ok, "source-zero/bounded coupling route selected"),
        ("VAL2157_06_bounded_handoff", bounded_ok, "bounded coupling handoff rows are schema-ready and nonclaim"),
        ("VAL2157_07_claim_gates", gates_ok, "all claim gates remain blocked"),
        ("VAL2157_08_decision_next", decisions_ok, "decision ledger selects source-zero/bounded coupling target"),
        ("VAL2157_09_next", next_ok, "2158 next target selected"),
        ("VAL2157_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2157_11_csv_parse", csv_ok, "all generated 2157 CSVs parse cleanly"),
        ("VAL2157_12_missing_not_ready", missing_not_ready, "MISSING_* rows stay nonclaim"),
        ("VAL2157_13_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2157_14_formalization_clean", formalization_clean, "formalization-workbench untouched by 2157"),
        ("VAL2157_15_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2157_OVERALL", all_ok, "2157 sharpens parent metric/beta normalization and selects source-zero/bounded coupling next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    metric: list[dict[str, object]],
    trace: list[dict[str, object]],
    rescale: list[dict[str, object]],
    finite: list[dict[str, object]],
    source_zero: list[dict[str, object]],
    bounded: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2156, _ = find_line(DOCS["2156"], ["NEXT2156_0_2157"])
    line_1849, _ = find_line(DOCS["1849"], ["QZ1849_6_verdict"])
    content = "\n\n".join(
        [
            "# 2157 - Y5/R2FR Parent Metric ZXfX2 Beta Eigenvalue Or Source-Zero Return",
            "## Current Verdict",
            "2157 does **not** prove the parent metric lock, beta prediction, finite lambda, alpha/product pass, R10/PPN/local-GR pass, or any public claim.",
            "It does make a sharper mathematical cut: `Z_X f_X^2=rho_vac^(1/2)` is the right finite-route contract only if one parent action owns `M_AB`, `e_X`, `f_X`, the Hessian spectrum, units, and stress/Bianchi variation before local tests.",
            "The beta route is also tightened: three equal spatial channels give `U''(0)=3` only for an unnormalised common-amplitude coordinate. In the normalized trace eigenvector, the factor 3 is absorbed by the metric normalization. So beta=3 from mode counting is rejected as a claim.",
            f"This follows the current 2156 handoff at line {line_2156} and returns to the source-zero/bounded coupling route sharpened at 1849 line {line_1849}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Parent Metric Lock Attempt",
            md_table(metric, ["lock_id", "target", "mathematical_statement", "result", "status", "missing_for_claim", "valid_for_claim"]),
            "## Trace Eigenvalue Theorem Attempt",
            md_table(trace, ["theorem_id", "target", "mathematical_statement", "derived_result", "status", "missing_for_claim", "valid_for_claim"]),
            "## Rescaling Degeneracy Audit",
            md_table(rescale, ["audit_id", "transformation", "transformation_law", "result", "status", "valid_for_claim"]),
            "## Finite Route Decision",
            md_table(finite, ["decision_id", "object", "current_evidence", "status", "allowed_use", "forbidden_use", "valid_for_claim"]),
            "## Source-Zero Return",
            md_table(source_zero, ["return_id", "route", "current_status", "because", "next_use", "valid_for_claim"]),
            "## Bounded Coupling Handoff",
            md_table(bounded, ["handoff_id", "component", "bound_formula", "observable_links", "current_status", "reason_retained", "valid_for_claim"]),
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
            "This is not circling; it removes a fake shortcut. The finite route is now frozen unless a parent metric/spectrum source appears. The next serious local-GR route is coupling silence: prove `J_X=qbar_XT=0` from parent descent, or score every surviving coupling as a bounded residual component. Chume, that is the cleaner fight.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    metric = parent_metric_lock_rows()
    trace = trace_eigenvalue_rows()
    rescale = rescaling_audit_rows()
    finite = finite_route_rows()
    source_zero = source_zero_rows()
    bounded = bounded_handoff_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_metric_lock"], metric)
    write_csv(OUTPUTS["trace_eigenvalue"], trace)
    write_csv(OUTPUTS["rescaling_audit"], rescale)
    write_csv(OUTPUTS["finite_route"], finite)
    write_csv(OUTPUTS["source_zero"], source_zero)
    write_csv(OUTPUTS["bounded_handoff"], bounded)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(metric, trace, source_zero, bounded, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, metric, trace, rescale, finite, source_zero, bounded, gates, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, metric, trace, rescale, finite, source_zero, bounded, gates, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2157 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
