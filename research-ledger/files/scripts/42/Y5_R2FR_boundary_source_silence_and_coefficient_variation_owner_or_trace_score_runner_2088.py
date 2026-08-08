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


DOC = ROOT / "2088-Y5-R2FR-boundary-source-silence-and-coefficient-variation-owner-or-trace-score-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
Q_R_HAT_POLICY_CEILING = 4.6e-05


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid"}


def formalization_has_2088_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2088-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2088*",
        "*Y5_R2FR_boundary_source_silence_and_coefficient_variation_owner_or_trace_score_runner_2088*",
        "*AFRAME_TRACE_SCORE_SOURCE_BOUNDARY_2088*",
        "*JR2088_PARENT_EULER_SOURCE_MAP*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2088_00_2087_doc",
            ROOT / "2087-Y5-R2FR-ZR-MR-signature-and-Poincare-domain-owner-or-flux-switch.md",
            ["NEXT2087_0_2088", "BS2087_3_coefficient_variation", "VAL2087_OVERALL"],
            "2087 handoff selecting source/boundary/coefficient cleanup before any trace score.",
        ),
        (
            "SRC2088_01_2087_validation",
            OUT / "P8_Y5_BRR545_2087_VALIDATION.csv",
            ["VAL2087_OVERALL", "source/boundary/coefficient cleanup", "PASS"],
            "machine validation that 2087 refused scoring and selected this target.",
        ),
        (
            "SRC2088_02_1256_hcore",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_0_minimal_density", "COEF1256_3_JR", "COEF1256_4_BR"],
            "formal reciprocal H_R density and coefficient blockers J_R/B_R.",
        ),
        (
            "SRC2088_03_1268_auxiliary",
            ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            ["VAR1268_1_E_R", "CAC1268_5_conditional_theorem", "VAR1268_4_operator_ban"],
            "auxiliary exact route and source/boundary/readout clauses that must vanish.",
        ),
        (
            "SRC2088_04_2063_boundary",
            ROOT / "2063-Y5-R2FR-boundary-object-exhaustion-or-PiR-component-bound-intake.md",
            ["BOE2063_5_verdict", "PCI2063_5_qR_Cassini_join", "COUNTERMODEL_OPEN"],
            "boundary object-exhaustion theorem shape plus countermodels and finite Pi_R intake needs.",
        ),
        (
            "SRC2088_05_2074_robin",
            ROOT / "2074-Y5-R2FR-Robin-Bmix-positivity-and-boundary-silence-or-finite-residual-fill.md",
            ["ROBIN_ACTIVATION_BLOCKED_USE_FINITE_RESIDUAL_FILL", "BSA2074_4_residue", "FRF2074_5_deltaR_bound"],
            "Robin/small-boundary absorption route and finite residual fallback.",
        ),
        (
            "SRC2088_06_2080_runner",
            ROOT / "2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md",
            ["PRESS2080_0_full_inequality", "RUN2080_0_current_inputs", "VAL2080_00_local_sources_exist"],
            "finite noncoercive pressure inequality runner and missing input status.",
        ),
        (
            "SRC2088_07_1087_matter",
            ROOT / "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md",
            ["PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED", "ZCC1087_0_object_language", "V1087_SUMMARY"],
            "matter descent zero-current chain that would silence ordinary-matter sourcing.",
        ),
        (
            "SRC2088_08_1275_equation",
            ROOT / "1275-Y5-R10-RAB-GR-style-radial-field-equation-difference-or-local-closure-baseline.md",
            ["EDA1275_0_contract_form", "MPE1275_0_Lcore", "VAL1275_12_overall"],
            "GR-style equation-difference route that needs parent Euler/source maps.",
        ),
        (
            "SRC2088_09_1276_contract",
            ROOT / "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
            ["ESC1276_4_difference_operator", "ESC1276_5_source_map", "VAL1276_11_overall"],
            "parent Euler/source-map contract turning the less-scrutinized exact route into certificate rows.",
        ),
        (
            "SRC2088_10_06_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Q_R = -Pi_R.", "Pi_R = 0 -> Q_R = 0", "Q_R neutrality is the missing source theorem."],
            "early neutral-charge argument showing boundary flux silence is not optional.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                exists=path.exists(),
                needle_count=len(needles),
                missing_needles=";".join(missing),
                status="EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                note=note,
                claim_allowed=False,
            )
        )
    return rows


def trace_score_clause_rows() -> list[dict[str, object]]:
    return [
        row(
            clause_id="TSC2088_0_parent_quadratic_signature",
            target="bulk R_AB quadratic operator",
            required_contract="Z_R>=Z_min>0 and either M_R^2>=M_min^2>0 or a parent-owned Poincare/reference condition; all in the same selected domain and normalization",
            current_evidence="2087 found only formal H_R notation, no parent-signed Z_min/M_min/C_P,RAB owner.",
            status="BLOCKED_MISSING_BULK_SIGNATURE",
            trace_score_effect="no positive trace score denominator exists",
            next_action="do not evaluate K_qR until sign/source/domain rows exist",
            claim_allowed=False,
        ),
        row(
            clause_id="TSC2088_1_linear_source_policy",
            target="linear source in R_AB equation",
            required_contract="S_total := J_R + lambda_R + coefficient_variation_source is theorem-zero, auxiliary-eliminated, or norm-bounded with an arena projection",
            current_evidence="1256/1268/1087 keep J_R, lambda_R, matter descent, and readout-regeneration unsigned.",
            status="BLOCKED_MISSING_SOURCE_ZERO_OR_BOUND",
            trace_score_effect="positive bulk terms would control a sourced profile, not prove local GR",
            next_action="derive matter descent/source map or create finite source-norm intake rows",
            claim_allowed=False,
        ),
        row(
            clause_id="TSC2088_2_boundary_policy",
            target="B_R / Pi_R / boundary-corner terms",
            required_contract="B_R is absent, nonnegative, trace-small, or componentized into signed absolute Pi_R rows with orientation and normalization",
            current_evidence="2063 leaves countermodels open; 2074 supplies only conditional Robin absorption and finite residual schemas.",
            status="BLOCKED_MISSING_BOUNDARY_SILENCE_OR_BOUND",
            trace_score_effect="boundary hair can beat the bulk energy or become Q_R flux",
            next_action="prove boundary object-exhaustion or source finite Pi_R components",
            claim_allowed=False,
        ),
        row(
            clause_id="TSC2088_3_coefficient_variation_schur",
            target="parent Hessian/cross terms",
            required_contract="after integrating out other parent fields Y, the effective operator A_eff=A_RR-A_RY A_YY^{-1} A_YR is nonnegative/coercive or explicitly residualized",
            current_evidence="2087 marks coefficient variation policy missing; 1256 warns E_R includes coefficient-variation terms.",
            status="BLOCKED_MISSING_PARENT_SECOND_VARIATION",
            trace_score_effect="formal Z_R/M_R notation may not be the actual linearized operator",
            next_action="extract the parent second-variation block before any local residual score",
            claim_allowed=False,
        ),
        row(
            clause_id="TSC2088_4_domain_normalization",
            target="D_ext/S_ext/C_tr/C_P/GM_source/readout",
            required_contract="selected exterior domain, trace constant, Poincare/reference constant, mass normalization, and q_R_hat readout are source-backed",
            current_evidence="1172/2080/2087 keep these constants symbolic or missing.",
            status="BLOCKED_MISSING_DOMAIN_AND_ARENA_PROJECTION",
            trace_score_effect="even a valid energy estimate cannot be compared to Cassini/R10/PPN without K_qR",
            next_action="source domain constants only after the parent route is selected",
            claim_allowed=False,
        ),
        row(
            clause_id="TSC2088_5_no_cancellation_absolute_envelope",
            target="multi-source residual join",
            required_contract="use an absolute envelope q_R_hat <= q_bulk + q_source + q_boundary + q_coeff + q_readout; do not cancel unknown signs",
            current_evidence="2071/2074 already require no-cancellation guards; no accepted numeric rows exist.",
            status="SCHEMA_GUARD_INSTALLED_NONCLAIM",
            trace_score_effect="prevents accidental wins from sign choices or hand-tuned cancellation",
            next_action="future runner must fail closed unless every term is signed or bounded absolutely",
            claim_allowed=False,
        ),
    ]


def source_boundary_clause_rows() -> list[dict[str, object]]:
    return [
        row(
            source_id="SBC2088_0_JR_matter_descent",
            object="J_R",
            exact_zero_clause="ordinary matter descends through q/g_obs and has no first variation along R_AB/vertical reciprocal direction",
            finite_clause="rho_R_norm := ||J_R||_{H^-1 or L2} with arena projection and source path",
            current_status="MISSING_MATTER_DESCENT_OR_RHO_R_NORM",
            blocks="local-vacuum plateau; trace score; PPN residual pass",
            claim_allowed=False,
        ),
        row(
            source_id="SBC2088_1_lambda_policy",
            object="lambda_R / Lambda_R",
            exact_zero_clause="Lambda_R is parent multiplier enforcing C_R=R_AB=0 before readout, with Dirac preservation and no source regeneration",
            finite_clause="lambda_R is included as a source/shift term in the absolute envelope",
            current_status="AUXILIARY_MULTIPLIER_CONDITIONAL_NOT_PARENT_SIGNED",
            blocks="exact local-GR branch unless promoted; finite branch unless bounded",
            claim_allowed=False,
        ),
        row(
            source_id="SBC2088_2_BR_boundary",
            object="B_R",
            exact_zero_clause="allowed boundary/corner functional has no R_AB argument or its R_AB variation vanishes in the selected boundary class",
            finite_clause="b_C_norm and Pi_R component rows with orientation, density/total convention, and same-frame normalization",
            current_status="COUNTERMODELS_OPEN_MISSING_BOUNDARY_OBJECT_EXHAUSTION",
            blocks="Q_R=0; no-hair; finite trace absorption",
            claim_allowed=False,
        ),
        row(
            source_id="SBC2088_3_PiR_flux",
            object="Pi_R^tot",
            exact_zero_clause="Pi_R^tot=0 follows from boundary object exhaustion plus reference subtraction, not fixed by hand",
            finite_clause="Pi_R^tot_abs <= sum_i |Pi_R_i| with no cancellation, source paths, and arena conversion",
            current_status="FLUX_FALLBACK_STAGED_NOT_ACTIVATED",
            blocks="R10/PPN/local-GR claim if used without components",
            claim_allowed=False,
        ),
        row(
            source_id="SBC2088_4_readout_regeneration",
            object="readout_regen_terms",
            exact_zero_clause="eliminating R_AB does not regenerate first-order q_R_hat, g_obs, clock, or matter-source variation",
            finite_clause="DObs/Dq finite leak rows are included in absolute envelope",
            current_status="MISSING_READOUT_STABILITY_FOR_RAB_ROUTE",
            blocks="turning auxiliary elimination into observed local GR",
            claim_allowed=False,
        ),
    ]


def coefficient_variation_rows() -> list[dict[str, object]]:
    return [
        row(
            coeff_id="CV2088_0_background_freeze",
            coefficient_object="Z_R(phi), M_R^2(phi), B_R(phi)",
            safe_if="R_AB=0, D R_AB=0, and coefficient variations multiply at least quadratic R_AB terms after auxiliary elimination",
            unsafe_if="delta Z_R, delta M_R^2, or delta B_R produces linear source terms in the local branch",
            current_status="MISSING_VARIATION_ORDER_PROOF",
            required_output="parent variation order lemma or finite source row",
            claim_allowed=False,
        ),
        row(
            coeff_id="CV2088_1_schur_complement",
            coefficient_object="mixed Hessian between R_AB and other parent fields Y",
            safe_if="A_YY is invertible/coercive and A_eff=A_RR-A_RY A_YY^{-1}A_YR keeps the needed sign",
            unsafe_if="cross terms generate a negative mode or an unsourced linear residual",
            current_status="MISSING_HESSIAN_BLOCK",
            required_output="source-backed second-variation matrix or closure-only demotion",
            claim_allowed=False,
        ),
        row(
            coeff_id="CV2088_2_robin_absorption",
            coefficient_object="boundary Robin/mixed terms",
            safe_if="w_eff=w_bulk-beta_plus*C_tr^2 > 0 in declared convention",
            unsafe_if="beta_plus*C_tr^2 >= w_bulk or beta sign/orientation is unknown",
            current_status="DERIVED_GUARD_NOT_ACTIVATED",
            required_output="beta_plus, C_tr, w_bulk, and orientation rows; otherwise finite noncoercive runner only",
            claim_allowed=False,
        ),
        row(
            coeff_id="CV2088_3_Bmix_cap",
            coefficient_object="mixed cap/source-reference split",
            safe_if="same parent functional proves source/reference cap split and no hidden R_AB boundary variation",
            unsafe_if="B_mix_cap is assumed from notation or fitted as a cancellation knob",
            current_status="MISSING_PARENT_FUNCTIONAL_FOR_BMIX_CAP",
            required_output="parent boundary functional or absolute cap residual row",
            claim_allowed=False,
        ),
        row(
            coeff_id="CV2088_4_no_cancellation_join",
            coefficient_object="all residual channels",
            safe_if="q_R_hat_total <= sum_abs(q_i) and every q_i has source path, units, and arena projection",
            unsafe_if="unknown signs are combined algebraically to reduce the residual",
            current_status="ABSOLUTE_JOIN_POLICY_INSTALLED",
            required_output="future runner refuses any MISSING_* q_i term",
            claim_allowed=False,
        ),
    ]


def trace_runner_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2088_0_exact_auxiliary",
            branch="exact auxiliary/unimodular elimination",
            formula_or_contract="R_AB,Lambda_R eliminated before readout; Z_R=J_R=B_R=0 if parent sort, multiplier origin, source silence, boundary silence, and readout stability are signed",
            input_status="REFUSED_PARENT_SIGNATURES_NOT_SIGNED",
            missing_inputs="parent sort; no-derivative grammar; Lambda_R origin; Dirac preservation; matter descent; boundary/readout silence",
            result="EXACT_CONDITIONAL_ONLY",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_CLAIM",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2088_1_massive_trace_score",
            branch="positive Z_R/M_R^2 trace score",
            formula_or_contract="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*min(Z_min,M_min^2)) plus absolute source/boundary/coefficient terms",
            input_status="REFUSED_MISSING_ZMIN_MMIN_SOURCE_BOUNDARY_COEFF_DOMAIN",
            missing_inputs="Z_min;M_min^2;J_R/lambda policy;B_R/Pi_R;Schur complement;C_tr;GM_source",
            result="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2088_2_massless_poincare_score",
            branch="positive Z_R plus Poincare/reference trace score",
            formula_or_contract="K_qR=(c^2/(G*M_source))*C_tr*sqrt(1+C_P,RAB^2)/sqrt(4*pi*Z_min) plus absolute source/boundary/coefficient terms",
            input_status="REFUSED_MISSING_ZMIN_CP_REFERENCE_SOURCE_BOUNDARY_COEFF_DOMAIN",
            missing_inputs="Z_min;C_P,RAB;reference/Dirichlet/zero-mean condition;J_R;B_R;Schur complement;C_tr;GM_source",
            result="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2088_3_finite_noncoercive_pressure",
            branch="2080 finite noncoercive pressure inequality",
            formula_or_contract="K_qR*0.5*(a + sqrt(a^2 + 4*F_outer_abs)) <= 4.6e-05, a=C_Poincare*rho_R_norm + C_trace*b_C_norm",
            input_status="REFUSED_MISSING_RHO_BC_FOUTER_CTRACE_CP_KQR",
            missing_inputs="rho_R_norm;b_C_norm;F_outer_abs;C_trace;C_Poincare;K_qR;source paths",
            result="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2088_4_GR_style_equation_difference",
            branch="parent Euler/source-map route",
            formula_or_contract="D_R[MTS] := E_time - E_radial = partial_r C_R - S_R[source,residual,boundary] = 0",
            input_status="REFUSED_CURRENT_CORPUS_LACKS_PARENT_EULER_PAIR_AND_SOURCE_MAP",
            missing_inputs="S_parent local EH fixed point;E_time;E_radial;source map;boundary no-charge;EH import guard",
            result="BEST_NEXT_DERIVATION_ROUTE_NOT_TRACE_SCORE",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="ROUTE_SELECTED_NO_CLAIM",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2088_0_sources", "all cited sources and needles exist", "PASS_SOURCE_ONLY", "source audit complete for this checkpoint"),
        ("GATE2088_1_trace_score", "trace score is allowed", "FAIL_BLOCKED", "source, boundary, coefficient, and domain blockers remain"),
        ("GATE2088_2_exact_auxiliary", "auxiliary route proves local GR", "FAIL_BLOCKED", "exact route is coherent but parent signatures remain unsigned"),
        ("GATE2088_3_finite_noncoercive", "finite inequality can be evaluated", "FAIL_BLOCKED", "2080 inputs are missing"),
        ("GATE2088_4_GR_style_difference", "D_R[MTS] equation difference is derived", "FAIL_BLOCKED", "parent Euler pair and source map are not yet extracted"),
        ("GATE2088_5_local_tests", "R10/PPN/Newton/local-GR pass", "FAIL_BLOCKED", "no theorem-zero or finite residual branch is claim-valid"),
    ]
    return [
        row(
            gate_id=gate_id,
            condition=condition,
            status=status,
            reason=reason,
            claim_allowed=False,
        )
        for gate_id, condition, status, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2088_0_trace_score_blocked",
            decision="Do not score the formal trace branch yet.",
            because="even if Z_R/M_R were later signed, J_R/lambda_R/B_R/coefficient variation/domain normalization still block claim-valid scoring.",
            next_action="keep trace score as a contract-only branch until every poison-pill term is signed or source-bounded",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2088_1_exact_vs_finite_separated",
            decision="Keep exact local-GR derivation separate from finite residual testing.",
            because="auxiliary/GR-style equation-difference routes are theorem routes, while 2080/trace-score routes are finite-inequality routes.",
            next_action="label closure baseline explicitly and forbid using closure rows as proof",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2088_2_boundary_flux_inactive",
            decision="Keep Pi_R flux fallback staged but inactive.",
            because="boundary flux is a fallback after trace failure or component sourcing, not a free escape hatch from missing Z/M signs.",
            next_action="activate only after finite component rows or a trace-failure theorem",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2088_3_next_target",
            decision="Move the next derivation attempt to parent Euler/source-map integration.",
            because="1275/1276 already identified the less-scrutinized route: derive D_R[MTS]=E_time-E_radial from a parent local EH fixed point/source map instead of imposing a plateau axiom.",
            next_action="build 2089 parent Euler/source-map integration or finite trace input lock",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2088_0_2089",
            target_doc="2089-Y5-R2FR-parent-Euler-source-map-contract-integration-or-finite-trace-input-lock.md",
            target_script="scripts/Y5_R2FR_parent_Euler_source_map_contract_integration_or_finite_trace_input_lock_2089.py",
            objective="assemble and attempt the parent D_R[MTS]=E_time-E_radial source-map derivation using the 1275/1276 GR-style route while importing the 2088 J_R/B_R/coefficient-variation gates; if no parent Euler/source pieces exist, lock local GR as closure-only and finite trace as source-input-only",
            success_condition="explicit parent Euler pair/source map or a clean refusal that lists exact missing action blocks without scoring local tests",
            exclusions="plateau axiom; closure q_R=0 as proof; trace score with missing sources; Pi_R flux switch without components; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    trace_clauses: list[dict[str, object]],
    source_boundary: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    runs: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2088_0_source_weight_trace_gate",
            SOURCE_WEIGHT_DOCS / "AFRAME_TRACE_SCORE_SOURCE_BOUNDARY_2088_NONCLAIM.csv",
            trace_clauses + source_boundary + coeffs + runs,
        ),
        (
            "COPY2088_1_wep_trace_gate",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2088_TRACE_SCORE_NONCLAIM.csv",
            trace_clauses + source_boundary + runs,
        ),
        (
            "COPY2088_2_queue_2089",
            QUEUE / "JR2088_PARENT_EULER_SOURCE_MAP_OR_TRACE_INPUT_LOCK_QUEUE.csv",
            source_boundary + coeffs + runs + next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data_rows in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=copy_id,
                path=str(path),
                rows_written=len(data_rows),
                status="WRITTEN_NONCLAIM_COPY",
                claim_allowed=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    trace_clauses: list[dict[str, object]],
    source_boundary: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    trace_blocked = any(str(r["status"]).startswith("BLOCKED") for r in trace_clauses) and any(
        r["clause_id"] == "TSC2088_5_no_cancellation_absolute_envelope" for r in trace_clauses
    )
    source_blockers = all(
        "MISSING" in str(r["current_status"]) or "CONDITIONAL" in str(r["current_status"]) or "STAGED" in str(r["current_status"])
        for r in source_boundary
    )
    schur_present = any(r["clause_id"] == "TSC2088_3_coefficient_variation_schur" for r in trace_clauses) and any(
        "A_eff=A_RR-A_RY" in str(r["required_contract"]) for r in trace_clauses
    )
    robin_present = any(r["coeff_id"] == "CV2088_2_robin_absorption" and "w_eff" in str(r["safe_if"]) for r in coeffs)
    no_cancellation_present = any("sum_abs" in str(r.get("safe_if", "")) or "absolute envelope" in str(r.get("required_contract", "")) for r in coeffs + trace_clauses)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in runs)
    gr_route_selected = any(
        r["run_id"] == "RUN2088_4_GR_style_equation_difference" and r["result"] == "BEST_NEXT_DERIVATION_ROUTE_NOT_TRACE_SCORE"
        for r in runs
    )
    gates_safe = all(not truthy(r.get("claim_allowed")) and str(r["status"]) != "PASS_CLAIM" for r in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2088_0_2089"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [trace_clauses, source_boundary, coeffs, runs, gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2088_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2088_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2088_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2088_02_trace_score_blocked", trace_blocked, "trace score remains blocked by explicit source/boundary/coefficient/domain clauses"),
        ("VAL2088_03_source_boundary_blockers", source_blockers, "J_R/lambda_R/B_R/Pi_R/readout blockers remain explicit"),
        ("VAL2088_04_schur_contract", schur_present, "Schur complement coefficient-variation contract is present"),
        ("VAL2088_05_robin_guard", robin_present, "Robin/trace absorption guard remains conditional"),
        ("VAL2088_06_no_cancellation", no_cancellation_present, "absolute no-cancellation envelope is installed"),
        ("VAL2088_07_dry_refusal", dry_refused, "all runner branches refuse missing inputs"),
        ("VAL2088_08_gr_route_selected", gr_route_selected, "GR-style parent Euler/source-map route selected as next derivation target"),
        ("VAL2088_09_claim_gates_safe", gates_safe, "claim gates allow no local-GR/R10/PPN claim"),
        ("VAL2088_10_next_selected", next_ok, "2089 parent Euler/source-map integration target selected"),
        ("VAL2088_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2088_12_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2088_13_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2088_14_no_formalization_artifacts", no_formalization_artifacts, "no 2088 artifacts were written under formalization-workbench"),
        ("VAL2088_15_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(
        (
            "VAL2088_OVERALL",
            overall,
            "2088 blocks trace scoring on unsigned source/boundary/coefficient clauses, keeps exact and finite routes separated, and selects parent Euler/source-map integration",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if status else "FAIL",
            detail=detail,
            claim_allowed=False,
        )
        for check_id, status, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    trace_clauses: list[dict[str, object]],
    source_boundary: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2088 Y5 R2FR Boundary Source Silence And Coefficient Variation Owner Or Trace Score Runner",
        "",
        "## Current Verdict",
        "",
        "2088 says the local branch is not dying, but the trace-score route is still blocked. The problem is sharper now: even a future positive `Z_R/M_R^2` signature would not be enough unless `J_R`, `lambda_R/Lambda_R`, `B_R/Pi_R`, coefficient variations, domain constants, and readout normalization are all signed or source-bounded.",
        "",
        "The exact branch and finite branch are now cleanly separated. Exact branch: prove auxiliary/unimodular elimination or a GR-style parent Euler/source-map relation before observed readout. Finite branch: use absolute, no-cancellation envelopes with sourced rows for every residual term. Closure rows remain useful internal controls, not proof.",
        "",
        "The strongest next route is not another trace-score loop. It is the 1275/1276 route: derive `D_R[MTS] := E_time - E_radial = partial_r C_R - S_R[source,residual,boundary] = 0` from the parent local action/source map, while importing the 2088 source, boundary, and coefficient gates.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "claim_allowed", "valid_for_claim"]),
        "## Trace Score Clause Audit",
        md_table(trace_clauses, ["clause_id", "target", "required_contract", "current_evidence", "status", "trace_score_effect", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Source Boundary Clauses",
        md_table(source_boundary, ["source_id", "object", "exact_zero_clause", "finite_clause", "current_status", "blocks", "claim_allowed", "valid_for_claim"]),
        "## Coefficient Variation Audit",
        md_table(coeffs, ["coeff_id", "coefficient_object", "safe_if", "unsafe_if", "current_status", "required_output", "claim_allowed", "valid_for_claim"]),
        "## Trace Runner Dry Runs",
        md_table(runs, ["run_id", "branch", "formula_or_contract", "input_status", "missing_inputs", "result", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "condition", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "target_script", "objective", "success_condition", "exclusions", "claim_allowed", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows_written", "status", "claim_allowed", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    trace_clauses = trace_score_clause_rows()
    source_boundary = source_boundary_clause_rows()
    coeffs = coefficient_variation_rows()
    runs = trace_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2088_SOURCE_REGISTER.csv",
        "trace_clauses": OUT / "P8_Y5_PARENT_QLOC_2088_TRACE_SCORE_CLAUSE_AUDIT.csv",
        "source_boundary": OUT / "P8_Y5_PARENT_QLOC_2088_SOURCE_BOUNDARY_CLAUSES.csv",
        "coeffs": OUT / "P8_Y5_PARENT_QLOC_2088_COEFFICIENT_VARIATION_AUDIT.csv",
        "runs": OUT / "P8_Y5_PARENT_QLOC_2088_TRACE_RUNNER_DRY_RUNS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2088_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2088_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2088_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2088_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2088_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["trace_clauses"], trace_clauses)
    write_csv(paths["source_boundary"], source_boundary)
    write_csv(paths["coeffs"], coeffs)
    write_csv(paths["runs"], runs)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(trace_clauses, source_boundary, coeffs, runs, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, trace_clauses, source_boundary, coeffs, runs, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, trace_clauses, source_boundary, coeffs, runs, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
