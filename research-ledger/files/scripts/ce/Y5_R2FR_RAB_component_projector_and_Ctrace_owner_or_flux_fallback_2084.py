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


DOC = ROOT / "2084-Y5-R2FR-RAB-component-projector-and-Ctrace-owner-or-flux-fallback.md"
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


def formalization_has_2084_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2084-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2084*",
        "*Y5_R2FR_RAB_component_projector_and_Ctrace_owner_or_flux_fallback_2084*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2084_00_2083_doc",
            ROOT / "2083-Y5-R2FR-domain-surface-norm-selector-and-CQX-constant-source-pack.md",
            ["NEXT2083_0_2084", "P_RAB", "C_trace_out"],
            "2083 handoff: derive/source P_RAB and C_trace_out owner for the round extraction cell.",
        ),
        (
            "SRC2084_01_2083_validation",
            OUT / "P8_Y5_BRR545_2083_VALIDATION.csv",
            ["VAL2083_OVERALL", "2084 P_RAB/C_trace target selected", "claim_allowed"],
            "2083 validation confirms trace route is least-scrutiny but unscored.",
        ),
        (
            "SRC2084_02_1172_trace",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["HBP1172_2_trace_to_boundary", "C_trace(D,gamma)", "MISSING_TRACE_CONSTANT"],
            "1172 supplies the trace inequality grammar and flags the domain constant as missing.",
        ),
        (
            "SRC2084_03_2080_runner",
            ROOT / "2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md",
            ["MISSING_QRHAT_MAP", "K_qR", "MISSING_TRACE_CONSTANT"],
            "2080 finite runner still awaits trace constant and K_qR map.",
        ),
        (
            "SRC2084_04_1256_exterior",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_1_spherical_exterior", "r^2 Z_R partial_r R_AB = Q_R", "Q_R = int_{S_r} Pi_R^n dS"],
            "1256 supplies the exterior R_AB/Q_R convention and flux fallback grammar.",
        ),
        (
            "SRC2084_05_1206_normal_trace",
            ROOT / "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            ["DRV1206_0_boundary_trace_lowering", "C_NT(D,gamma)", "LOWERED_TO_GEOMETRIC_TRACE_CONTRACT_NONCLAIM"],
            "1206 supplies normal-trace fallback grammar.",
        ),
        (
            "SRC2084_06_2062_orientation",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "MISSING_ORIENTATION_CONVENTION", "CONDITIONAL_PROOF_ONLY"],
            "2062 keeps finite orientation and normalization unsigned.",
        ),
        (
            "SRC2084_07_1521_bridge",
            ROOT / "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md",
            ["QBRG1521_3_same_normalization", "QLOC_TO_QR_BRIDGE_NOT_PROVED", "retained-channel silence"],
            "1521 blocks local-test promotion until same-normalization and retained-channel silence are proved.",
        ),
        (
            "SRC2084_08_1045_gauge",
            ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            ["MFS1045_0_parent_field_quotient", "Dq_loc[v_X]=0", "shadow frame"],
            "1045 records the general rule: representative/gauge silence must be parent-signed, not assumed.",
        ),
        (
            "SRC2084_09_1244_GM",
            OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            ["GM1244_0_qR_definition", "q_R_hat = Q_R c^2/(G M_source)", "weak-field map assumes areal-radial matching"],
            "1244 supplies the q_R_hat convention but not an MTS Q_R prediction.",
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
            )
        )
    return rows


def projector_trace_lemma_rows() -> list[dict[str, object]]:
    return [
        row(
            lemma_id="LEM2084_0_RAB_component_projector_contract",
            object="P_RAB",
            statement="Let the reciprocal local field bundle split as E_R = span(e_RAB) plus E_perp in a parent-signed weak-field basis. Define P_RAB Phi_R := <Phi_R,e_RAB>_h e_RAB and scalar R_AB := pi_RAB(Phi_R).",
            consequence="P_RAB is legal only if the field basis, inner product h, gauge/representative fixing, and reference subtraction are parent-signed.",
            status="CONDITIONAL_EXACT_PROJECTOR_DEFINITION",
            missing_inputs="field_basis;bundle_inner_product;gauge_representative_silence;R_AB_reference_subtraction",
            claim_allowed=False,
        ),
        row(
            lemma_id="LEM2084_1_energy_slot_domination",
            object="X_E to R_AB bound",
            statement="If X_E^2 >= w_RAB * ||R_AB||_{H1(D_ext)}^2 with w_RAB>0 and all other slots nonnegative, then ||R_AB||_{H1(D_ext)} <= X_E/sqrt(w_RAB).",
            consequence="This is the cleanest route from finite energy to the exact exterior scalar component.",
            status="EXACT_IF_POSITIVE_RAB_ENERGY_SLOT_SIGNED",
            missing_inputs="w_RAB;X_E_norm_definition;nonnegative_rest_terms;same_domain_D_ext",
            claim_allowed=False,
        ),
        row(
            lemma_id="LEM2084_2_trace_owner",
            object="C_trace_out",
            statement="For the chosen Lipschitz/round exterior domain, ||R_AB||_{L2(S_ext)} <= C_tr(D_ext,S_ext,gamma) * ||R_AB||_{H1(D_ext)}.",
            consequence="Combined with LEM2084_1, C_trace_out = C_tr(D_ext,S_ext,gamma)/sqrt(w_RAB).",
            status="TRACE_THEOREM_CONDITIONAL_CONSTANT_MISSING",
            missing_inputs="C_tr(D_ext,S_ext,gamma);boundary_regular;metric_regular;w_RAB",
            claim_allowed=False,
        ),
        row(
            lemma_id="LEM2084_3_round_trace_to_CQX_unit",
            object="C_QX trace unit-Q_R",
            statement="With S_ext round areal and R_AB=-Q_R/r, C_QX = C_trace_out/sqrt(4*pi) = C_tr/(sqrt(4*pi*w_RAB)).",
            consequence="K_qR = (c^2/(G*M_source))*C_tr/(sqrt(4*pi*w_RAB)) if the unit-Q_R convention is parent-signed.",
            status="FORMULA_READY_INPUTS_MISSING",
            missing_inputs="C_tr;w_RAB;GM_source;unit_QR_convention;P_RAB",
            claim_allowed=False,
        ),
        row(
            lemma_id="LEM2084_4_round_trace_to_CQX_ZR",
            object="C_QX trace kinetic-Z_R",
            statement="With R_AB=-Q_R/(Z_R*r), C_QX = abs(Z_R)*C_trace_out/sqrt(4*pi) = abs(Z_R)*C_tr/(sqrt(4*pi*w_RAB)).",
            consequence="K_qR = (c^2/(G*M_source))*abs(Z_R)*C_tr/(sqrt(4*pi*w_RAB)) if kinetic normalization is parent-signed.",
            status="FORMULA_READY_INPUTS_MISSING",
            missing_inputs="Z_R;C_tr;w_RAB;GM_source;P_RAB",
            claim_allowed=False,
        ),
    ]


def trace_owner_audit_rows() -> list[dict[str, object]]:
    specs = [
        (
            "AUD2084_0_field_basis",
            "field basis and scalar slot",
            "R_AB must be a named scalar component of the local reciprocal weak-field variables, not a notational alias introduced after readout.",
            "MISSING_PARENT_FIELD_BASIS",
        ),
        (
            "AUD2084_1_projector",
            "P_RAB projector",
            "The map from Phi_R to R_AB must be linear/idempotent in the chosen branch and invariant under allowed representative/gauge changes.",
            "MISSING_PROJECTOR_CERTIFICATE",
        ),
        (
            "AUD2084_2_energy_weight",
            "w_RAB positive slot",
            "The finite energy norm must contain a positive R_AB H1 slot or an equivalent coercive bound.",
            "MISSING_POSITIVE_RAB_ENERGY_WEIGHT",
        ),
        (
            "AUD2084_3_rest_nonnegative",
            "nonnegative rest terms",
            "Other reciprocal variables cannot subtract from X_E or hide cancellation against R_AB.",
            "MISSING_NONNEGATIVE_NORM_DECOMPOSITION",
        ),
        (
            "AUD2084_4_trace_constant",
            "C_tr(D_ext,S_ext,gamma)",
            "A concrete trace constant or accepted theorem reference must match the selected domain, metric regularity, and H1 norm convention.",
            "MISSING_TRACE_CONSTANT",
        ),
        (
            "AUD2084_5_reference_subtraction",
            "R_AB reference subtraction",
            "The offset removal must preserve the 1/r monopole and cannot enforce Q_R=0 by boundary convention.",
            "MISSING_REFERENCE_SUBTRACTION_CERTIFICATE",
        ),
        (
            "AUD2084_6_GM_normalization",
            "GM/source-body binding",
            "Raw Q_R still requires source_body and measured GM_source or a directly dimensionless q_R_hat row.",
            "MISSING_SOURCE_BODY_GM_ROW",
        ),
        (
            "AUD2084_7_local_bridge",
            "q_loc to q_R bridge",
            "Even a scored q_R map is not a local-GR claim until q_loc projection, same normalization, and retained-channel silence are proved.",
            "QLOC_TO_QR_BRIDGE_NOT_PROVED",
        ),
    ]
    return [
        row(
            audit_id=audit_id,
            clause=clause,
            requirement=requirement,
            current_status=status,
            blocks_score=status != "QLOC_TO_QR_BRIDGE_NOT_PROVED",
            blocks_claim=True,
            claim_allowed=False,
        )
        for audit_id, clause, requirement, status in specs
    ]


def fallback_rows() -> list[dict[str, object]]:
    return [
        row(
            fallback_id="FB2084_0_identity_trace_if_XE_is_RAB_H1",
            route="trace",
            condition="If X_E is already the H1(D_ext) norm of R_AB after reference subtraction, set w_RAB=1 and P_RAB=id on the scalar slot.",
            result="C_trace_out=C_tr and C_QX=C_tr/sqrt(4*pi) in unit-Q_R normalization.",
            status="BEST_CASE_CONDITIONAL_NOT_SOURCED",
            missing_inputs="source row proving X_E == ||R_AB||_H1;C_tr;GM_source",
            claim_allowed=False,
        ),
        row(
            fallback_id="FB2084_1_weighted_trace_if_XE_contains_RAB",
            route="trace",
            condition="If X_E contains w_RAB ||R_AB||_H1^2 plus nonnegative rest terms, use the weighted projector lemma.",
            result="C_trace_out=C_tr/sqrt(w_RAB) and C_QX=C_tr/sqrt(4*pi*w_RAB).",
            status="PRIMARY_TRACE_CONTRACT_UNSIGNED",
            missing_inputs="w_RAB;nonnegative decomposition;C_tr;P_RAB",
            claim_allowed=False,
        ),
        row(
            fallback_id="FB2084_2_no_RAB_slot_then_trace_fails",
            route="trace",
            condition="If X_E does not control R_AB in H1 or equivalent trace norm, trace extraction cannot bind Q_R.",
            result="Do not score K_qR by trace; move to flux/Pi_R bound or parent zero theorem.",
            status="DEMOTION_RULE",
            missing_inputs="R_AB control absent",
            claim_allowed=False,
        ),
        row(
            fallback_id="FB2084_3_flux_fallback",
            route="flux",
            condition="If parent supplies Pi_R^n density or total-flux bound but not R_AB H1 control, use flux rows from 2083.",
            result="C_QX=sqrt(4*pi)*r_ext*C_flux_out for density, or C_QX=C_flux_total for total-charge normalized flux.",
            status="FALLBACK_MORE_NORMALIZATION_DEBT",
            missing_inputs="Pi_R normalization;C_flux_out or C_flux_total;orientation;absolute tails",
            claim_allowed=False,
        ),
    ]


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2084_0_projector_trace_best_case",
            attempted_route="identity R_AB H1 slot",
            formula="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi)",
            input_status="REFUSED_MISSING_XE_EQUALS_RAB_H1_AND_CTR",
            missing_inputs="X_E_equals_RAB_H1_source;C_tr;GM_source;reference_subtraction",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2084_1_projector_trace_weighted",
            attempted_route="weighted R_AB H1 slot",
            formula="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*w_RAB)",
            input_status="REFUSED_MISSING_WRAB_CTR_GM",
            missing_inputs="w_RAB;C_tr;GM_source;P_RAB;nonnegative norm decomposition",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2084_2_projector_trace_ZR",
            attempted_route="kinetic Z_R weighted trace",
            formula="K_qR=(c^2/(G*M_source))*abs(Z_R)*C_tr/sqrt(4*pi*w_RAB)",
            input_status="REFUSED_MISSING_ZR_WRAB_CTR_GM",
            missing_inputs="Z_R;w_RAB;C_tr;GM_source;P_RAB",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2084_3_flux_fallback",
            attempted_route="flux fallback",
            formula="K_qR=(c^2/(G*M_source))*sqrt(4*pi)*r_ext*C_flux_out or (c^2/(G*M_source))*C_flux_total",
            input_status="REFUSED_MISSING_PIR_FLUX_NORMALIZATION",
            missing_inputs="Pi_R density/total flag;C_flux_out;C_flux_total;r_ext;orientation;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2084_0_projector_contract", "P_RAB projector contract is explicit", "PASS_CONDITIONAL", "field split and idempotent scalar projection contract are written"),
        ("GATE2084_1_energy_bound", "X_E controls R_AB H1", "FAIL_BLOCKED", "w_RAB or identity R_AB H1 norm source row is missing"),
        ("GATE2084_2_trace_constant", "C_tr/C_trace_out is source-backed", "FAIL_BLOCKED", "trace constant is symbolic only"),
        ("GATE2084_3_CQX_score", "C_QX can be evaluated", "FAIL_REFUSED", "P_RAB, w_RAB, C_tr, and GM inputs are missing"),
        ("GATE2084_4_flux_fallback", "flux fallback can be evaluated", "FAIL_REFUSED", "Pi_R normalization and C_flux inputs are missing"),
        ("GATE2084_5_local_claim", "local GR/Newton/PPN claim", "FAIL_BLOCKED", "q_loc bridge and retained-channel silence remain missing"),
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
            decision_id="DEC2084_0_projector_contract_derived",
            decision="P_RAB is now a precise conditional projector contract.",
            because="if the parent weak-field reciprocal bundle contains a signed scalar R_AB slot, the projection is a standard idempotent component map.",
            next_action="source the parent field basis and R_AB slot instead of re-arguing the whole local branch",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2084_1_trace_owner_reduced",
            decision="C_trace_out reduces to C_tr/sqrt(w_RAB).",
            because="energy-slot domination plus the trace theorem gives the exact norm chain from X_E to boundary R_AB.",
            next_action="hunt w_RAB and C_tr as the next hard input pair",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2084_2_trace_remains_best_route",
            decision="Trace remains the least-scrutiny route if w_RAB and C_tr can be sourced.",
            because="it avoids Pi_R density-vs-total normalization and only needs a scalar H1 trace theorem.",
            next_action="build 2085 w_RAB/C_tr owner-or-numeric-bound checkpoint",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2084_3_flux_fallback_retained",
            decision="Flux fallback remains live but second choice.",
            because="flux still needs Pi_R normalization, orientation, density-vs-total convention, and absolute tail control.",
            next_action="only switch to flux if R_AB H1 energy-slot ownership fails",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2084_0_2085",
            target_doc="2085-Y5-R2FR-RAB-energy-weight-wRAB-and-trace-constant-owner-or-flux-switch.md",
            objective="derive/source w_RAB and C_tr(D_ext,S_ext,gamma) for the R_AB H1 slot in the round exterior cell; if no R_AB energy slot exists, explicitly switch the finite branch to Pi_R flux fallback",
            must_include="parent weak-field reciprocal basis; X_E norm decomposition; positive w_RAB; nonnegative rest terms; trace theorem/source row; reference subtraction; GM/source-body row remains nonclaim",
            exclusions="scoring K_qR without w_RAB and C_tr; using Cassini ceiling as prediction; closure q_R=0; local GR/Newton/PPN claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    lemmas: list[dict[str, object]],
    audit: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2084_0_source_weight_projector",
            SOURCE_WEIGHT_DOCS / "AFRAME_RAB_PROJECTOR_CTRACE_OWNER_2084_NONCLAIM.csv",
            lemmas + audit + dry,
        ),
        (
            "COPY2084_1_wep_projector",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2084_RAB_PROJECTOR_CTRACE_NONCLAIM.csv",
            lemmas + fallbacks + dry,
        ),
        (
            "COPY2084_2_queue_2085",
            QUEUE / "JR2084_WRAB_CTRACE_OWNER_QUEUE.csv",
            fallbacks + next_rows_,
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
    lemmas: list[dict[str, object]],
    audit: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    projector_ok = any(r["lemma_id"] == "LEM2084_0_RAB_component_projector_contract" for r in lemmas)
    domination_ok = any("X_E^2 >= w_RAB" in str(r["statement"]) for r in lemmas)
    ctrace_ok = any("C_trace_out = C_tr" in str(r["consequence"]) for r in lemmas)
    kq_unit_ok = any("sqrt(4*pi*w_RAB)" in str(r["statement"]) and "unit" in str(r["object"]) for r in lemmas)
    audit_blocks = all(truthy(r.get("blocks_claim")) and not truthy(r.get("claim_allowed")) for r in audit)
    trace_fallback_ok = any(r["fallback_id"] == "FB2084_1_weighted_trace_if_XE_contains_RAB" for r in fallbacks)
    flux_fallback_ok = any(r["fallback_id"] == "FB2084_3_flux_fallback" for r in fallbacks)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in dry)
    gates_blocked = all(not truthy(r.get("claim_allowed")) for r in gates)
    next_pair_ok = any(r["decision_id"] == "DEC2084_1_trace_owner_reduced" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2084_0_2085"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [lemmas, audit, fallbacks, dry, gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2084_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2084_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2084_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2084_02_projector_contract", projector_ok, "P_RAB projector contract is explicit"),
        ("VAL2084_03_energy_domination", domination_ok, "X_E to R_AB domination lemma is written"),
        ("VAL2084_04_Ctrace_owner", ctrace_ok, "C_trace_out reduces to C_tr/sqrt(w_RAB)"),
        ("VAL2084_05_KqR_unit_formula", kq_unit_ok, "unit-Q_R K_qR formula includes sqrt(4*pi*w_RAB)"),
        ("VAL2084_06_audit_blocks", audit_blocks, "all missing clauses block claims"),
        ("VAL2084_07_trace_fallback", trace_fallback_ok, "weighted trace fallback row exists"),
        ("VAL2084_08_flux_fallback", flux_fallback_ok, "flux fallback row remains available"),
        ("VAL2084_09_dry_refusal", dry_refused, "all dry-run branches refuse missing inputs"),
        ("VAL2084_10_claim_gates_blocked", gates_blocked, "claim gates remain blocked"),
        ("VAL2084_11_next_pair", next_pair_ok, "w_RAB/C_tr pair selected as next input pair"),
        ("VAL2084_12_next_selected", next_ok, "2085 w_RAB/C_tr target selected"),
        ("VAL2084_13_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2084_14_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2084_15_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2084_16_no_formalization_artifacts", no_formalization_artifacts, "no 2084 artifacts were written under formalization-workbench"),
        ("VAL2084_17_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2084_OVERALL", overall, "2084 derives the conditional P_RAB/C_trace owner contract, refuses scoring, and selects w_RAB/C_tr"))
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
    lemmas: list[dict[str, object]],
    audit: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2084 Y5 R2FR R_AB Component Projector And C_trace Owner Or Flux Fallback",
        "",
        "## Current Verdict",
        "",
        "2084 derives the exact conditional trace-owner contract. If the parent weak-field reciprocal bundle has a signed scalar `R_AB` slot and the finite norm contains a positive slot `w_RAB ||R_AB||_{H1(D_ext)}^2`, then the projector and trace route are no longer vague.",
        "",
        "The core bound is `||R_AB||_{H1(D_ext)} <= X_E/sqrt(w_RAB)`. The trace theorem then gives `C_trace_out = C_tr(D_ext,S_ext,gamma)/sqrt(w_RAB)`. On the round areal surface from 2083, the unit-`Q_R` route becomes `C_QX=C_tr/sqrt(4*pi*w_RAB)` and `K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*w_RAB)`.",
        "",
        "For kinetic normalization, the same route becomes `C_QX=|Z_R|*C_tr/sqrt(4*pi*w_RAB)`. This is still conditional because `Z_R`, `w_RAB`, `C_tr`, `P_RAB`, and the GM/source row are not parent-signed.",
        "",
        "Flux remains the fallback, not the first choice. If `X_E` does not control `R_AB` in `H1`, trace extraction is invalid and the branch must switch to a `Pi_R` density/total-flux bound with explicit orientation and normalization.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## Projector And Trace Lemmas",
        md_table(lemmas, ["lemma_id", "object", "statement", "consequence", "status", "missing_inputs", "claim_allowed", "valid_for_claim"]),
        "## Trace Owner Audit",
        md_table(audit, ["audit_id", "clause", "requirement", "current_status", "blocks_score", "blocks_claim", "claim_allowed", "valid_for_claim"]),
        "## Fallback Rows",
        md_table(fallbacks, ["fallback_id", "route", "condition", "result", "status", "missing_inputs", "claim_allowed", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry, ["run_id", "attempted_route", "formula", "input_status", "missing_inputs", "K_qR_value", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
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
    lemmas = projector_trace_lemma_rows()
    audit = trace_owner_audit_rows()
    fallbacks = fallback_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2084_SOURCE_REGISTER.csv",
        "lemmas": OUT / "P8_Y5_PARENT_QLOC_2084_PROJECTOR_TRACE_LEMMAS.csv",
        "audit": OUT / "P8_Y5_PARENT_QLOC_2084_TRACE_OWNER_AUDIT.csv",
        "fallbacks": OUT / "P8_Y5_PARENT_QLOC_2084_FALLBACK_ROWS.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2084_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2084_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2084_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2084_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2084_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2084_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["lemmas"], lemmas)
    write_csv(paths["audit"], audit)
    write_csv(paths["fallbacks"], fallbacks)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(lemmas, audit, fallbacks, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, lemmas, audit, fallbacks, dry, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, lemmas, audit, fallbacks, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
