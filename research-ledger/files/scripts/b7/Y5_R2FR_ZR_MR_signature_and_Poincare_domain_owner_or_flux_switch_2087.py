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


DOC = ROOT / "2087-Y5-R2FR-ZR-MR-signature-and-Poincare-domain-owner-or-flux-switch.md"
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


def formalization_has_2087_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2087-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2087*",
        "*Y5_R2FR_ZR_MR_signature_and_Poincare_domain_owner_or_flux_switch_2087*",
        "*AFRAME_ZR_MR_POINCARE_2087*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2087_00_2086_doc",
            ROOT / "2086-Y5-R2FR-parent-reciprocal-quadratic-form-extraction-or-PiR-flux-switch.md",
            ["NEXT2086_0_2087", "Z_R/M_R signature", "VAL2086_OVERALL"],
            "2086 handoff into Z_R/M_R/Poincare signature and flux-switch audit.",
        ),
        (
            "SRC2087_01_2086_validation",
            OUT / "P8_Y5_BRR545_2086_VALIDATION.csv",
            ["VAL2086_OVERALL", "Z_R/M_R/Poincare", "PASS"],
            "machine validation that 2086 selected this target without claims.",
        ),
        (
            "SRC2087_02_1256_coefficients",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["COEF1256_0_ZR", "COEF1256_1_MR2", "FORMAL_VARIATIONAL_CONTRACT_NOT_PARENT_SIGNED"],
            "formal H_R coefficients exist only as missing/unsigned coefficient requirements.",
        ),
        (
            "SRC2087_03_1257_selector",
            ROOT / "1257-Y5-R10-ZR-lambdaR-selector-from-parent-primitives.md",
            ["SEL1257_0_field_exclusion", "SEL1257_3_mass_gap_silence", "GATE1257_1_ZR_zero"],
            "older selector already separated zero, kinetic, and mass-gap routes.",
        ),
        (
            "SRC2087_04_1268_auxiliary",
            ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            ["CAC1268_1_constraint_action", "CAC1268_5_conditional_theorem", "VAR1268_4_operator_ban"],
            "second-class auxiliary compatibility gives the clean conditional Z_R=0 route.",
        ),
        (
            "SRC2087_05_1272_parent_contract",
            ROOT / "1272-Y5-R10-RAB-auxiliary-parent-necessity-from-radial-cell-variational-principle-or-finite-source-row.md",
            ["PNC1272_7_parent_signed_zero_theorem", "RCD1272_7_verdict", "NO_ACCEPTED_SOURCE_READY_ROWS"],
            "radial-cell parent-necessity contract remains exact but unsigned.",
        ),
        (
            "SRC2087_06_1273_hcore_no_go",
            ROOT / "1273-Y5-R10-RAB-parent-Hcore-radial-cell-owner-or-finite-residual-source-acquisition.md",
            ["HCO1273_5_unimodular_radial_cell", "NO_ORDINARY_HCORE_ZERO_OWNER", "NO_ACCEPTED_SOURCE_READY_ROWS"],
            "ordinary H_core zero route is rejected; unimodular cell is the exact-route target.",
        ),
        (
            "SRC2087_07_1172_trace_constant",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["C_trace(D,gamma)", "MISSING_TRACE_CONSTANT", "Hodge/Poincare"],
            "selected-domain trace/Poincare constants are still symbolic/missing.",
        ),
        (
            "SRC2087_08_2062_boundary_flux",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "MISSING_NORMALIZATION_CHAIN", "CONDITIONAL_SILENCE_FINITE_PIR_ROW_REQUIRED"],
            "finite Pi_R fallback exists but lacks orientation/normalization/source components.",
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


def signature_audit_rows() -> list[dict[str, object]]:
    return [
        row(
            signature_id="SIG2087_0_formal_HR_present",
            target="H_R reciprocal quadratic form",
            condition="H_R contains Z_R |D R_AB|^2, M_R^2 R_AB^2, lambda_R R_AB, J_R R_AB, and boundary B_R",
            current_evidence="1256/2086 extract the formal density but explicitly mark it not parent-signed.",
            derived_consequence="trace route remains live as a formal branch, not as evidence",
            status="FORMAL_ONLY_NOT_PARENT_SIGNED",
            missing="parent origin of every coefficient; coefficient-variation terms; matter descent",
            claim_allowed=False,
        ),
        row(
            signature_id="SIG2087_1_positive_ZR_needed",
            target="Z_R lower bound",
            condition="Z_R(x) >= Z_min > 0 on D_ext in the selected normalization",
            current_evidence="no source-backed row or theorem-zero/positive theorem found in the cited corpus",
            derived_consequence="gradient coercivity would control ||D R_AB||_L2 but not ||R_AB||_L2 without mass or Poincare/reference",
            status="MISSING_PARENT_SIGNED_ZMIN",
            missing="Z_min value/theorem; units; normalization; source path; coefficient variation policy",
            claim_allowed=False,
        ),
        row(
            signature_id="SIG2087_2_positive_MR_needed",
            target="M_R^2 lower bound",
            condition="M_R^2(x) >= M_min^2 > 0 on D_ext in the same frame as Z_R",
            current_evidence="1256/1273 keep mass-gap route conceptual; no accepted finite coefficient row exists",
            derived_consequence="with Z_min and M_min^2, bulk H1 control gives w_RAB=min(Z_min,M_min^2) up to norm/unit matching",
            status="MISSING_PARENT_SIGNED_MMIN",
            missing="M_min^2 source; Hessian around local branch; units; scale separation; source silence",
            claim_allowed=False,
        ),
        row(
            signature_id="SIG2087_3_massless_reference_route",
            target="M_R=0 kinetic branch",
            condition="Z_R>=Z_min>0, M_R=0, and a reference/Dirichlet/zero-mean condition gives ||R_AB||_L2^2 <= C_P,RAB^2 ||D R_AB||_L2^2",
            current_evidence="2086 writes the route; 1172 shows analogous Hodge/Poincare constants are symbolic, not sourced",
            derived_consequence="w_RAB=Z_min/(1+C_P,RAB^2) for the H1 norm",
            status="MISSING_POINCARE_REFERENCE_OWNER",
            missing="C_P,RAB; domain D_ext; reference selector; boundary condition; C_tr; GM_source",
            claim_allowed=False,
        ),
        row(
            signature_id="SIG2087_4_auxiliary_zero_route",
            target="Z_R=0 exact branch",
            condition="R_AB is parent auxiliary/compatibility data; no derivative operator is legal; lambda/Lambda block is parent-owned; matter/boundary/readout sources are silent",
            current_evidence="1268 gives exact conditional mechanism; 1272/1273 show parent necessity/unimodular-cell owner remains unsigned",
            derived_consequence="if fully signed, Z_R=J_R=B_R=0 and no finite trace/flux score is needed for this channel",
            status="BEST_EXACT_ROUTE_CONDITIONAL_NOT_CLOSED",
            missing="parent sort; no-derivative grammar; Lambda_R origin; Dirac preservation; matter descent; boundary/readout silence",
            claim_allowed=False,
        ),
        row(
            signature_id="SIG2087_5_negative_or_indefinite_route",
            target="bad-sign quadratic branch",
            condition="Z_R<=0, M_R^2<0, unbounded boundary terms, or uncontrolled coefficient-variation terms",
            current_evidence="no current source selects a bad sign, but no positive signature excludes it either",
            derived_consequence="trace coercivity fails; branch must be rejected or converted to a finite residual/stability problem",
            status="COUNTERCASE_NOT_EXCLUDED",
            missing="positive Hessian/coercivity proof or explicit demotion",
            claim_allowed=False,
        ),
    ]


def poincare_contract_rows() -> list[dict[str, object]]:
    return [
        row(
            contract_id="PC2087_0_massive_trace_law",
            route="massive coercive trace",
            premise="E_RAB >= int_D_ext [Z_min |D R_AB|^2 + M_min^2 R_AB^2] dmu",
            derived_law="||R_AB||_H1(D_ext)^2 <= E_RAB / min(Z_min,M_min^2)",
            trace_law="||R_AB||_L2(S_ext) <= C_tr(D_ext,S_ext,gamma) sqrt(E_RAB/min(Z_min,M_min^2))",
            score_law="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*min(Z_min,M_min^2))",
            status="EXACT_IF_INPUTS_SIGNED",
            blocker="Z_min;M_min^2;C_tr;GM_source;source/boundary/coefficient silence",
            claim_allowed=False,
        ),
        row(
            contract_id="PC2087_1_massless_poincare_law",
            route="massless kinetic trace",
            premise="E_RAB >= int_D_ext Z_min |D R_AB|^2 dmu and ||R_AB||_L2^2 <= C_P,RAB^2 ||D R_AB||_L2^2",
            derived_law="||R_AB||_H1(D_ext)^2 <= ((1+C_P,RAB^2)/Z_min) E_RAB",
            trace_law="||R_AB||_L2(S_ext) <= C_tr sqrt((1+C_P,RAB^2)/Z_min) sqrt(E_RAB)",
            score_law="K_qR=(c^2/(G*M_source))*C_tr*sqrt(1+C_P,RAB^2)/sqrt(4*pi*Z_min)",
            status="EXACT_IF_REFERENCE_SIGNED",
            blocker="Z_min;C_P,RAB;reference/Dirichlet/zero-mean condition;C_tr;GM_source",
            claim_allowed=False,
        ),
        row(
            contract_id="PC2087_2_small_robin_absorption",
            route="boundary-term absorbed trace",
            premise="bulk coercivity w0 minus boundary penalty beta_R ||R_AB||_L2(S_ext)^2",
            derived_law="coercivity survives if w0 > beta_R C_tr^2 in the chosen trace convention",
            trace_law="effective w_RAB >= w0 - beta_R C_tr^2",
            score_law="use w_eff only after beta_R, sign convention, and C_tr are source-backed",
            status="DERIVED_GUARDRAIL_NOT_ACTIVATED",
            blocker="boundary coefficient beta_R; sign; trace convention; no-cancellation guard",
            claim_allowed=False,
        ),
        row(
            contract_id="PC2087_3_source_shift_warning",
            route="linear J_R/lambda_R source terms",
            premise="E includes linear source int (lambda_R+J_R) R_AB",
            derived_law="positive M_R^2 can bound a shifted profile, but not prove zero; massless branch needs source orthogonality/zero",
            trace_law="source contribution must be bounded separately in the same norm before any K_qR score",
            score_law="no score until source norm or source-zero theorem exists",
            status="SOURCE_TERMS_BLOCK_TRACE_CLAIM",
            blocker="J_R/lambda_R zero, shift, or norm bound; matter descent; coefficient variation terms",
            claim_allowed=False,
        ),
    ]


def boundary_source_rows() -> list[dict[str, object]]:
    return [
        row(
            clause_id="BS2087_0_JR_source_silence",
            object="J_R",
            required_clause="J_R=0 in local vacuum, or ||J_R|| source norm is bounded and projected to the arena",
            current_status="MISSING_MATTER_DESCENT_OR_SOURCE_BOUND",
            effect_if_missing="finite R_AB profile can be sourced even with positive Z_R/M_R^2",
            next_action="derive matter descent for R_AB or create source-backed J_R rows",
            claim_allowed=False,
        ),
        row(
            clause_id="BS2087_1_lambda_policy",
            object="lambda_R / Lambda_R",
            required_clause="lambda_R is either a parent-owned auxiliary multiplier eliminating R_AB, or a bounded/shifted source term",
            current_status="AUXILIARY_ROUTE_CONDITIONAL_NOT_PARENT_SIGNED",
            effect_if_missing="closure-like local GR route remains unsigned",
            next_action="prove parent multiplier necessity or keep finite branch unscored",
            claim_allowed=False,
        ),
        row(
            clause_id="BS2087_2_BR_boundary",
            object="B_R",
            required_clause="B_R absent/nonnegative/trace-small in the selected boundary class, or Pi_R component rows are sourced",
            current_status="MISSING_BOUNDARY_POSITIVITY_OR_SILENCE",
            effect_if_missing="boundary hair can defeat bulk coercivity or become Q_R flux",
            next_action="derive boundary object-exhaustion or fill finite Pi_R component rows",
            claim_allowed=False,
        ),
        row(
            clause_id="BS2087_3_coefficient_variation",
            object="delta Z_R, delta M_R^2, delta B_R under parent-field variation",
            required_clause="coefficient variations are frozen, higher order, or bounded as explicit sources",
            current_status="MISSING_COEFFICIENT_VARIATION_POLICY",
            effect_if_missing="formal quadratic form is not the actual linearized operator controlling R_AB",
            next_action="extract parent second variation/Hessian block including cross terms",
            claim_allowed=False,
        ),
        row(
            clause_id="BS2087_4_trace_domain",
            object="D_ext,S_ext,gamma,C_tr,C_P,RAB",
            required_clause="selected exterior domain, boundary condition, trace theorem, and Poincare/reference constant are fixed before readout",
            current_status="MISSING_DOMAIN_CONSTANTS",
            effect_if_missing="K_qR can be algebraically written but not evaluated or compared",
            next_action="source domain geometry constants after parent sign route is selected",
            claim_allowed=False,
        ),
    ]


def decision_matrix_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DM2087_0_positive_signature_found",
            question="Did 2087 find parent-signed positive Z_R/M_R^2?",
            answer="NO",
            evidence="1256, 1257, 1268, 1272, and 1273 all keep coefficient signs/source rows unsigned or missing.",
            consequence="no trace score and no local-GR/PPN/R10 claim",
            claim_allowed=False,
        ),
        row(
            decision_id="DM2087_1_auxiliary_zero_status",
            question="Did 2087 close Z_R=0 as theorem?",
            answer="NO_BUT_BEST_EXACT_ROUTE_IDENTIFIED",
            evidence="1268 gives exact conditional auxiliary mechanism; 1273 says unimodular radial-cell grammar is the honest parent-origin target.",
            consequence="exact GR route should keep attacking parent cell/auxiliary ownership, not pretend finite signs exist",
            claim_allowed=False,
        ),
        row(
            decision_id="DM2087_2_poincare_owner",
            question="Can the massless trace route score now?",
            answer="NO",
            evidence="C_P,RAB, reference condition, C_tr, and source/domain constants are not source-backed.",
            consequence="massless trace law remains a useful formula-only branch",
            claim_allowed=False,
        ),
        row(
            decision_id="DM2087_3_flux_switch",
            question="Should Pi_R flux be activated?",
            answer="NO_TRACE_SIGNATURE_MISSING_FLUX_SWITCH_NOT_ACTIVATED",
            evidence="missing signs are not a theorem that the trace slot is absent; 2062 flux fallback also lacks normalization/component rows.",
            consequence="keep flux fallback staged but inactive until trace failure is proved or finite component rows are sourced",
            claim_allowed=False,
        ),
    ]


def source_pack_rows() -> list[dict[str, object]]:
    specs = [
        ("PACK2087_0_Zmin", "Z_min", "positive lower bound or theorem-zero for Z_R", "MISSING_PARENT_SIGNED_VALUE"),
        ("PACK2087_1_Mmin", "M_min^2", "positive local Hessian/mass gap for R_AB/u", "MISSING_PARENT_HESSIAN"),
        ("PACK2087_2_CP_RAB", "C_P,RAB", "Poincare/reference constant for massless route", "MISSING_DOMAIN_REFERENCE_ROW"),
        ("PACK2087_3_Ctr", "C_tr(D_ext,S_ext,gamma)", "selected-domain trace constant", "MISSING_TRACE_CONSTANT"),
        ("PACK2087_4_JR", "J_R", "matter/source coupling zero or finite norm", "MISSING_MATTER_DESCENT_OR_BOUND"),
        ("PACK2087_5_BR", "B_R/Pi_R", "boundary silence/positivity or finite component flux", "MISSING_BOUNDARY_COMPONENTS"),
        ("PACK2087_6_cross_terms", "Hessian cross block", "Schur complement/coefficient variation policy", "MISSING_PARENT_SECOND_VARIATION"),
        ("PACK2087_7_GM", "GM_source and normalization", "convert R_AB trace to q_R/K_qR arena residual", "MISSING_ARENA_NORMALIZATION"),
    ]
    return [
        row(
            pack_id=pack_id,
            required_input=required_input,
            purpose=purpose,
            current_status=current_status,
            source_ready=False,
            score_ready=False,
            claim_allowed=False,
        )
        for pack_id, required_input, purpose, current_status in specs
    ]


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2087_0_massive_trace",
            attempted_route="positive Z_R/M_R^2 trace score",
            formula="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*min(Z_min,M_min^2))",
            input_status="REFUSED_MISSING_ZMIN_MMIN_CTR_SOURCE_BOUNDARY_GM",
            missing_inputs="Z_min;M_min^2;C_tr;J_R/lambda policy;B_R positivity;GM_source",
            result="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2087_1_massless_poincare",
            attempted_route="positive Z_R plus Poincare/reference trace score",
            formula="K_qR=(c^2/(G*M_source))*C_tr*sqrt(1+C_P,RAB^2)/sqrt(4*pi*Z_min)",
            input_status="REFUSED_MISSING_ZMIN_CP_REFERENCE_CTR_GM",
            missing_inputs="Z_min;C_P,RAB;reference/Dirichlet/zero-mean condition;C_tr;GM_source",
            result="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2087_2_auxiliary_zero",
            attempted_route="Z_R=J_R=B_R=0 via auxiliary/unimodular cell",
            formula="R_AB eliminated before readout if parent sort + Lambda_R C_R + no derivative/source/boundary/readout clauses are signed",
            input_status="REFUSED_PARENT_NECESSITY_NOT_DERIVED",
            missing_inputs="unimodular radial-cell grammar; Lambda_R origin; Dirac preservation; matter/boundary/readout silence",
            result="EXACT_CONDITIONAL_ONLY",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_CLAIM",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2087_3_flux_fallback",
            attempted_route="Pi_R flux score after trace failure",
            formula="K_qR=(c^2/(G*M_source))*C_flux with density/total normalization fixed",
            input_status="REFUSED_TRACE_FAILURE_NOT_PROVED_AND_FLUX_INPUTS_MISSING",
            missing_inputs="proof coercive trace route fails;Pi_R component rows;orientation;normalization;GM_source",
            result="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2087_0_sources", "all cited source paths and needles exist", "PASS_SOURCE_ONLY", "source audit is complete for this checkpoint"),
        ("GATE2087_1_positive_signature", "parent-signed positive Z_R/M_R^2 exists", "FAIL_BLOCKED", "no source-backed sign/lower-bound rows exist"),
        ("GATE2087_2_massless_poincare", "massless Poincare/reference branch can score", "FAIL_BLOCKED", "C_P,RAB/reference/C_tr/GM are missing"),
        ("GATE2087_3_auxiliary_zero", "Z_R=0 exact local branch is proved", "FAIL_BLOCKED", "auxiliary/unimodular route is exact conditional but not parent-derived"),
        ("GATE2087_4_flux_switch", "Pi_R flux fallback is activated", "FAIL_BLOCKED", "trace failure is not proved and flux component rows are missing"),
        ("GATE2087_5_local_tests", "local GR/Newton/R10/PPN/clock/orbital pass", "FAIL_BLOCKED", "neither theorem-zero nor finite score branch is claim-valid"),
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
            decision_id="DEC2087_0_trace_route_alive_but_unsigned",
            decision="Keep the trace route alive only as formula-only scaffolding.",
            because="formal H_R exists, but Z_R/M_R signs, source terms, boundary terms, and domain constants are not parent-signed.",
            next_action="do not score K_qR until coefficient/sign/source/domain rows are real",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2087_1_exact_route_priority",
            decision="The exact local-GR route is still auxiliary/unimodular-cell ownership, not positive finite hair.",
            because="1268/1273 show the clean route is eliminating R_AB before readout; ordinary H_core either gives no equation, finite residuals, or hair.",
            next_action="continue deriving parent cell grammar or explicitly demote it to closure",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2087_2_flux_not_now",
            decision="Do not activate Pi_R flux fallback yet.",
            because="missing Z/M rows are not proof of trace failure, and 2062 says flux normalization/components remain missing.",
            next_action="activate flux only after trace failure theorem or source-backed component rows",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2087_3_next_target",
            decision="Next target is boundary/source/coefficient-variation ownership before any trace score.",
            because="even positive Z/M would not score unless J_R, lambda_R, B_R, cross terms, C_tr, and GM are controlled.",
            next_action="build 2088 boundary-source-silence-and-coefficient-variation-owner-or-trace-score-runner.md",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2087_0_2088",
            target_doc="2088-Y5-R2FR-boundary-source-silence-and-coefficient-variation-owner-or-trace-score-runner.md",
            objective="derive or source the missing J_R/lambda_R/B_R/coefficient-variation clauses that prevent the formal Z_R/M_R trace formulas from becoming a local residual score; retain exact auxiliary/unimodular route as theorem target and keep flux fallback inactive unless trace failure is proved",
            must_include="J_R source-zero or norm bound; lambda_R policy; B_R positivity/silence or Pi_R component rows; coefficient variation/Schur complement; C_tr/C_P domain constants; no-cancellation guard; nonclaim dry runs",
            exclusions="claiming positive Z_R/M_R from formal notation; using missing rows as trace failure proof; activating flux without component normalization; closure q_R=0; local GR/Newton/PPN/R10 claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    signatures: list[dict[str, object]],
    contracts: list[dict[str, object]],
    boundary: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2087_0_source_weight_signature",
            SOURCE_WEIGHT_DOCS / "AFRAME_ZR_MR_POINCARE_2087_NONCLAIM.csv",
            signatures + contracts + boundary + dry,
        ),
        (
            "COPY2087_1_wep_signature",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2087_ZR_MR_POINCARE_NONCLAIM.csv",
            signatures + contracts + dry,
        ),
        (
            "COPY2087_2_queue_2088",
            QUEUE / "JR2087_BOUNDARY_SOURCE_SILENCE_OR_TRACE_SCORE_QUEUE.csv",
            pack + boundary + next_rows_,
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
    signatures: list[dict[str, object]],
    contracts: list[dict[str, object]],
    boundary: list[dict[str, object]],
    matrix: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    positive_missing = any(r["signature_id"] == "SIG2087_1_positive_ZR_needed" and r["status"] == "MISSING_PARENT_SIGNED_ZMIN" for r in signatures) and any(
        r["signature_id"] == "SIG2087_2_positive_MR_needed" and r["status"] == "MISSING_PARENT_SIGNED_MMIN" for r in signatures
    )
    auxiliary_conditional = any(
        r["signature_id"] == "SIG2087_4_auxiliary_zero_route" and r["status"] == "BEST_EXACT_ROUTE_CONDITIONAL_NOT_CLOSED"
        for r in signatures
    )
    massive_formula = any("min(Z_min,M_min^2)" in str(r["score_law"]) for r in contracts)
    massless_formula = any("sqrt(1+C_P,RAB^2)" in str(r["score_law"]) for r in contracts)
    robin_guard = any(r["contract_id"] == "PC2087_2_small_robin_absorption" for r in contracts)
    boundary_blockers = all(str(r["current_status"]).startswith("MISSING") or "CONDITIONAL" in str(r["current_status"]) for r in boundary)
    no_flux_switch = any("FLUX_SWITCH_NOT_ACTIVATED" in str(r["answer"]) for r in matrix)
    pack_nonclaim = all(not truthy(r.get("source_ready")) and not truthy(r.get("score_ready")) for r in pack)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in dry)
    gates_safe = all(not truthy(r.get("claim_allowed")) for r in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2087_0_2088"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [signatures, contracts, boundary, matrix, pack, dry, gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2087_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2087_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2087_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2087_02_positive_signature_missing", positive_missing, "Z_R/M_R positive signatures remain missing/nonclaim"),
        ("VAL2087_03_auxiliary_conditional", auxiliary_conditional, "auxiliary/unimodular exact route remains conditional not closed"),
        ("VAL2087_04_massive_formula", massive_formula, "massive trace formula is written but not scored"),
        ("VAL2087_05_massless_formula", massless_formula, "massless Poincare trace formula is written but not scored"),
        ("VAL2087_06_robin_guard", robin_guard, "boundary absorption guardrail is written"),
        ("VAL2087_07_boundary_blockers", boundary_blockers, "source/boundary/coefficient blockers remain explicit"),
        ("VAL2087_08_no_flux_switch", no_flux_switch, "flux fallback is not activated"),
        ("VAL2087_09_pack_nonclaim", pack_nonclaim, "source pack rows remain nonclaim/unscored"),
        ("VAL2087_10_dry_refusal", dry_refused, "all dry-run branches refuse missing inputs"),
        ("VAL2087_11_claim_gates_safe", gates_safe, "claim gates allow no claims"),
        ("VAL2087_12_next_selected", next_ok, "2088 boundary/source/coefficient target selected"),
        ("VAL2087_13_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2087_14_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2087_15_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2087_16_no_formalization_artifacts", no_formalization_artifacts, "no 2087 artifacts were written under formalization-workbench"),
        ("VAL2087_17_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(
        (
            "VAL2087_OVERALL",
            overall,
            "2087 finds no parent-signed positive Z_R/M_R/Poincare owner, keeps auxiliary zero route conditional, refuses scoring, and selects source/boundary/coefficient cleanup",
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
    signatures: list[dict[str, object]],
    contracts: list[dict[str, object]],
    boundary: list[dict[str, object]],
    matrix: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2087 Y5 R2FR Z_R/M_R Signature And Poincare Domain Owner Or Flux Switch",
        "",
        "## Current Verdict",
        "",
        "2087 does not find a parent-signed positive `Z_R` or `M_R^2` owner, and it does not find the `C_P,RAB`/reference data needed for the massless Poincare trace branch. The formal `H_R` engine from 2086 is still useful, but it is not evidence until its signs, sources, boundary terms, and coefficient variations are owned by the parent action.",
        "",
        "The best exact-GR route is still the auxiliary/unimodular-cell route: eliminate `R_AB` before observed readout so `Z_R=J_R=B_R=0` rather than trying to tune finite hair small. That route is mathematically coherent, but still conditional because the parent cell grammar, multiplier origin, Dirac preservation, matter descent, boundary silence, and readout stability are not jointly signed.",
        "",
        "The finite trace laws are now exact contracts rather than claims. Massive branch: `w_RAB=min(Z_min,M_min^2)`. Massless branch with reference/Poincare: `w_RAB=Z_min/(1+C_P,RAB^2)`. Boundary penalties can be absorbed only under a small-Robin guard such as `w0 > beta_R C_tr^2` in a declared convention.",
        "",
        "`Pi_R` flux is not activated. Missing `Z_R/M_R` evidence is not a theorem that the trace slot fails, and the flux fallback still lacks component, orientation, normalization, and arena projection rows.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "claim_allowed", "valid_for_claim"]),
        "## Signature Audit",
        md_table(signatures, ["signature_id", "target", "condition", "current_evidence", "derived_consequence", "status", "missing", "claim_allowed", "valid_for_claim"]),
        "## Poincare Trace Contracts",
        md_table(contracts, ["contract_id", "route", "premise", "derived_law", "trace_law", "score_law", "status", "blocker", "claim_allowed", "valid_for_claim"]),
        "## Boundary Source Clauses",
        md_table(boundary, ["clause_id", "object", "required_clause", "current_status", "effect_if_missing", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Decision Matrix",
        md_table(matrix, ["decision_id", "question", "answer", "evidence", "consequence", "claim_allowed", "valid_for_claim"]),
        "## Source Pack",
        md_table(pack, ["pack_id", "required_input", "purpose", "current_status", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry, ["run_id", "attempted_route", "formula", "input_status", "missing_inputs", "result", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "condition", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "exclusions", "claim_allowed", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows_written", "status", "claim_allowed", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    signatures = signature_audit_rows()
    contracts = poincare_contract_rows()
    boundary = boundary_source_rows()
    matrix = decision_matrix_rows()
    pack = source_pack_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2087_SOURCE_REGISTER.csv",
        "signatures": OUT / "P8_Y5_PARENT_QLOC_2087_SIGNATURE_AUDIT.csv",
        "contracts": OUT / "P8_Y5_PARENT_QLOC_2087_POINCARE_TRACE_CONTRACT.csv",
        "boundary": OUT / "P8_Y5_PARENT_QLOC_2087_BOUNDARY_SOURCE_CLAUSES.csv",
        "matrix": OUT / "P8_Y5_PARENT_QLOC_2087_DECISION_MATRIX.csv",
        "pack": OUT / "P8_Y5_PARENT_QLOC_2087_SOURCE_PACK.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2087_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2087_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2087_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2087_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2087_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2087_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["signatures"], signatures)
    write_csv(paths["contracts"], contracts)
    write_csv(paths["boundary"], boundary)
    write_csv(paths["matrix"], matrix)
    write_csv(paths["pack"], pack)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(signatures, contracts, boundary, pack, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, signatures, contracts, boundary, matrix, pack, dry, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, signatures, contracts, boundary, matrix, pack, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
