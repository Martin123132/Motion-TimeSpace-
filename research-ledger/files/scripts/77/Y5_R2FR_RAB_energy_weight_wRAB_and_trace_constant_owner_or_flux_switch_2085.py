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


DOC = ROOT / "2085-Y5-R2FR-RAB-energy-weight-wRAB-and-trace-constant-owner-or-flux-switch.md"
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


def formalization_has_2085_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2085-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2085*",
        "*Y5_R2FR_RAB_energy_weight_wRAB_and_trace_constant_owner_or_flux_switch_2085*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2085_00_2084_doc",
            ROOT / "2084-Y5-R2FR-RAB-component-projector-and-Ctrace-owner-or-flux-fallback.md",
            ["NEXT2084_0_2085", "w_RAB", "C_tr"],
            "2084 handoff: source w_RAB and C_tr or switch to Pi_R flux fallback.",
        ),
        (
            "SRC2085_01_2084_validation",
            OUT / "P8_Y5_BRR545_2084_VALIDATION.csv",
            ["VAL2084_OVERALL", "2085 w_RAB/C_tr target selected", "claim_allowed"],
            "2084 validation confirms P_RAB/C_trace owner contract is conditional only.",
        ),
        (
            "SRC2085_02_2084_lemmas",
            OUT / "P8_Y5_PARENT_QLOC_2084_PROJECTOR_TRACE_LEMMAS.csv",
            ["LEM2084_1_energy_slot_domination", "C_trace_out = C_tr", "w_RAB"],
            "2084 lemma CSV is the immediate formula source for the w_RAB/C_tr pair.",
        ),
        (
            "SRC2085_03_2083_cell",
            ROOT / "2083-Y5-R2FR-domain-surface-norm-selector-and-CQX-constant-source-pack.md",
            ["S_ext={r=r_ext}", "area_ext=4*pi*r_ext^2", "P_RAB"],
            "2083 supplies the round exterior extraction-cell schema.",
        ),
        (
            "SRC2085_04_1172_trace",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["HBP1172_2_trace_to_boundary", "C_trace(D,gamma)", "MISSING_TRACE_CONSTANT"],
            "1172 supplies trace theorem grammar but no selected-domain constant.",
        ),
        (
            "SRC2085_05_1206_normal_trace",
            ROOT / "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md",
            ["DRV1206_0_boundary_trace_lowering", "C_NT(D,gamma)", "MISSING_DOMAIN_GEOMETRY_CONSTANT"],
            "1206 supplies normal-trace fallback grammar and flags domain constants.",
        ),
        (
            "SRC2085_06_1256_exterior",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_1_spherical_exterior", "r^2 Z_R partial_r R_AB = Q_R", "Q_R = int_{S_r} Pi_R^n dS"],
            "1256 supplies the R_AB exterior and Pi_R flux shape.",
        ),
        (
            "SRC2085_07_2062_orientation",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "Pi_R^tot", "MISSING_ORIENTATION_CONVENTION"],
            "2062 keeps flux normalization/orientation unsigned.",
        ),
        (
            "SRC2085_08_2080_runner",
            ROOT / "2080-Y5-R2FR-finite-noncoercive-energy-bound-input-source-runner.md",
            ["MISSING_QRHAT_MAP", "MISSING_TRACE_CONSTANT", "K_qR"],
            "2080 finite runner remains blocked on trace and K_qR inputs.",
        ),
        (
            "SRC2085_09_1244_GM",
            OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            ["GM1244_0_qR_definition", "q_R_hat = Q_R c^2/(G M_source)", "weak-field map assumes areal-radial matching"],
            "1244 supplies q_R_hat convention only.",
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


def owner_hunt_rows() -> list[dict[str, object]]:
    return [
        row(
            hunt_id="HUNT2085_0_wRAB_explicit",
            target="w_RAB explicit source row",
            evidence="No current pre-2085 source supplies a parent-signed numerical or symbolic positive R_AB H1 slot weight.",
            current_status="OWNER_NOT_FOUND",
            consequence="trace route cannot score K_qR",
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2085_1_Ctr_explicit",
            target="C_tr(D_ext,S_ext,gamma) selected-domain trace constant",
            evidence="1172 and 1206 provide trace theorem grammar but mark selected-domain constants missing.",
            current_status="OWNER_NOT_FOUND",
            consequence="C_trace_out cannot become numeric/source-ready",
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2085_2_XE_norm_decomposition",
            target="X_E norm decomposition",
            evidence="2080 uses X_E only as an abstract finite reciprocal energy norm; no current row decomposes it into R_AB and orthogonal/nonnegative pieces.",
            current_status="OWNER_NOT_FOUND",
            consequence="w_RAB cannot be inferred by inspection",
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2085_3_flux_owner",
            target="Pi_R flux fallback constants",
            evidence="1256/2062 define the flux shape and orientation blockers, but no C_flux_out/C_flux_total row is sourced.",
            current_status="FALLBACK_OWNER_NOT_FOUND",
            consequence="flux switch can be prepared but not scored",
            claim_allowed=False,
        ),
    ]


def coercivity_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="THM2085_0_block_diagonal_weight",
            route="trace owner",
            statement="If X_E^2 contains int_D (a0 R_AB^2 + a1 |nabla R_AB|^2) dmu plus nonnegative rest terms, with a0>0 and a1>0, then w_RAB=min(a0,a1) for the H1 norm int_D(R_AB^2+|nabla R_AB|^2).",
            output="C_trace_out=C_tr/sqrt(min(a0,a1)); C_QX=C_tr/sqrt(4*pi*min(a0,a1)) in unit-Q_R normalization.",
            status="EXACT_IF_PARENT_BLOCK_DIAGONAL_SLOT_SIGNED",
            missing_inputs="a0;a1;H1_norm_convention;nonnegative_rest_terms;C_tr",
            claim_allowed=False,
        ),
        row(
            theorem_id="THM2085_1_weight_matrix_lower_bound",
            route="trace owner",
            statement="If the R_AB value/gradient pair has a positive 2x2 coefficient matrix A_RAB in the selected norm basis, then w_RAB=lambda_min(A_RAB) after unit matching.",
            output="C_trace_out=C_tr/sqrt(lambda_min(A_RAB)).",
            status="EXACT_IF_PARENT_MATRIX_SLOT_SIGNED",
            missing_inputs="A_RAB;unit_matching;lambda_min_positive;C_tr",
            claim_allowed=False,
        ),
        row(
            theorem_id="THM2085_2_cross_term_schur_bound",
            route="trace owner",
            statement="If R_AB mixes with other reciprocal variables y through quadratic block [[A,B],[B^T,C]], then R_AB is controlled only when A - B C^{-1} B^T >= w_RAB I with C positive; otherwise trace extraction may be noncoercive.",
            output="w_RAB=lambda_min(A - B C^{-1} B^T) when positive.",
            status="EXACT_IF_PARENT_SCHUR_COERCIVITY_SIGNED",
            missing_inputs="A;B;C;C_positive_inverse;Schur_lower_bound;no_negative_boundary_terms",
            claim_allowed=False,
        ),
        row(
            theorem_id="THM2085_3_trace_constant_contract",
            route="trace owner",
            statement="For the selected D_ext and S_ext, the trace theorem contributes ||R_AB||_L2(S_ext)<=C_tr(D_ext,S_ext,gamma)||R_AB||_H1(D_ext); C_tr must match the metric, measure, boundary regularity, and H1 convention.",
            output="C_tr is a geometric/theorem constant, not the older trace-coupling symbol C_tr(Phi).",
            status="CONTRACT_READY_CONSTANT_NOT_SOURCED",
            missing_inputs="domain geometry;metric regularity;boundary class;H1 convention;theorem/source path",
            claim_allowed=False,
        ),
        row(
            theorem_id="THM2085_4_trace_failure_switch_rule",
            route="flux switch",
            statement="If no positive R_AB H1 slot or equivalent coercive bound is parent-signed, trace extraction is invalid and the finite branch must switch to Pi_R flux ownership rather than score K_qR by trace.",
            output="switch_condition=NO_PARENT_SIGNED_RAB_H1_CONTROL; next required inputs are Pi_R density/total normalization and C_flux_out/C_flux_total.",
            status="SWITCH_RULE_READY_CURRENT_ABSENCE_NOT_PROVED",
            missing_inputs="parent verdict that R_AB H1 slot is absent, or completed search of parent quadratic form",
            claim_allowed=False,
        ),
    ]


def symbol_hygiene_rows() -> list[dict[str, object]]:
    return [
        row(
            symbol_id="SYM2085_0_C_tr_trace_constant",
            symbol="C_tr(D_ext,S_ext,gamma)",
            meaning="Sobolev/geometric trace theorem constant mapping H1(D_ext) to L2(S_ext)",
            must_not_confuse_with="C_tr(Phi) trace-sector coupling/leakage rows around 895-899",
            status="RENAMING_RECOMMENDED_AS_C_trace_geom",
            claim_allowed=False,
        ),
        row(
            symbol_id="SYM2085_1_C_trace_out",
            symbol="C_trace_out",
            meaning="compound extraction constant C_tr/sqrt(w_RAB) from X_E to boundary R_AB",
            must_not_confuse_with="generic C_trace(D,gamma) rows from 1172 before R_AB energy-slot ownership",
            status="COMPOUND_CONSTANT_FORMULA_ONLY",
            claim_allowed=False,
        ),
        row(
            symbol_id="SYM2085_2_w_RAB",
            symbol="w_RAB",
            meaning="positive lower-bound coefficient of the R_AB H1 slot inside X_E^2",
            must_not_confuse_with="Z_R kinetic normalization or fitted q_R coefficient",
            status="MISSING_OWNER",
            claim_allowed=False,
        ),
    ]


def switch_ledger_rows() -> list[dict[str, object]]:
    return [
        row(
            switch_id="SW2085_0_trace_status",
            branch="trace",
            condition="w_RAB and C_tr are parent-signed",
            current_status="NOT_SATISFIED",
            action="do not score K_qR by trace",
            claim_allowed=False,
        ),
        row(
            switch_id="SW2085_1_absence_status",
            branch="trace-to-flux",
            condition="parent quadratic-form audit proves no R_AB H1/equivalent coercive slot exists",
            current_status="NOT_PROVED",
            action="do not claim trace absent; prepare flux switch but first audit parent quadratic form",
            claim_allowed=False,
        ),
        row(
            switch_id="SW2085_2_flux_status",
            branch="flux",
            condition="Pi_R density/total normalization and C_flux_out/C_flux_total are parent-signed",
            current_status="NOT_SATISFIED",
            action="flux fallback not scorable yet",
            claim_allowed=False,
        ),
        row(
            switch_id="SW2085_3_best_next",
            branch="parent quadratic form",
            condition="extract or reject the R_AB H1 slot directly from the parent reciprocal quadratic form",
            current_status="SELECTED_NEXT",
            action="build 2086 parent reciprocal quadratic-form extraction or flux switch",
            claim_allowed=False,
        ),
    ]


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2085_0_block_diagonal_trace",
            attempted_route="block diagonal R_AB H1 slot",
            formula="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*min(a0,a1))",
            input_status="REFUSED_MISSING_A0_A1_CTR_GM",
            missing_inputs="a0;a1;C_tr;GM_source;X_E_norm_definition;nonnegative_rest_terms",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2085_1_schur_trace",
            attempted_route="cross-term Schur coercivity",
            formula="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*lambda_min(A-B C^-1 B^T))",
            input_status="REFUSED_MISSING_QUADRATIC_BLOCKS",
            missing_inputs="A;B;C;C_positive_inverse;Schur_lower_bound;C_tr;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2085_2_flux_switch",
            attempted_route="Pi_R flux fallback",
            formula="K_qR=(c^2/(G*M_source))*sqrt(4*pi)*r_ext*C_flux_out or (c^2/(G*M_source))*C_flux_total",
            input_status="REFUSED_MISSING_FLUX_OWNER",
            missing_inputs="Pi_R normalization;C_flux_out;C_flux_total;r_ext;orientation;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2085_0_wRAB_formulae", "w_RAB formulae are derived conditionally", "PASS_CONDITIONAL", "block-diagonal, matrix, and Schur coercivity routes are written"),
        ("GATE2085_1_wRAB_owner", "w_RAB is parent-signed/source-backed", "FAIL_BLOCKED", "no parent reciprocal quadratic form supplies the positive R_AB slot"),
        ("GATE2085_2_Ctr_owner", "C_tr is source-backed for D_ext/S_ext", "FAIL_BLOCKED", "trace theorem constant remains selected-domain missing"),
        ("GATE2085_3_trace_score", "K_qR trace route can score", "FAIL_REFUSED", "w_RAB, C_tr, GM, and norm decomposition are missing"),
        ("GATE2085_4_flux_switch", "flux fallback can score", "FAIL_REFUSED", "Pi_R flux normalization and constants are missing"),
        ("GATE2085_5_local_claim", "local GR/Newton/PPN claim", "FAIL_BLOCKED", "q_loc bridge and retained-channel silence are still not proved"),
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
            decision_id="DEC2085_0_wRAB_not_found",
            decision="No source-backed w_RAB owner is present in the current corpus.",
            because="current rows define the needed coefficient but do not extract the parent reciprocal quadratic form.",
            next_action="do not score trace route",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2085_1_Ctr_not_found",
            decision="No selected-domain C_tr owner is present.",
            because="1172/1206 supply theorem grammar but not the round exterior domain constant and convention.",
            next_action="keep C_tr formula-only",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2085_2_trace_absence_not_proved",
            decision="Trace route is blocked, not disproved.",
            because="absence of a sourced w_RAB row is not the same as a proof that the parent action has no R_AB slot.",
            next_action="audit parent reciprocal quadratic form before activating flux switch",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2085_3_best_next",
            decision="Next target is parent reciprocal quadratic-form extraction.",
            because="it can either produce w_RAB/C_tr ownership or justify switching to Pi_R flux fallback cleanly.",
            next_action="build 2086 parent H_R/X_E quadratic-form extraction or flux switch",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2085_0_2086",
            target_doc="2086-Y5-R2FR-parent-reciprocal-quadratic-form-extraction-or-PiR-flux-switch.md",
            objective="extract the parent reciprocal quadratic form defining X_E/H_R and decide whether it contains a positive R_AB H1 slot; if it does, fill w_RAB/C_tr owner rows; if it provably does not, switch finite branch to Pi_R flux ownership",
            must_include="parent H_R or X_E definition; R_AB scalar slot; a0/a1 or A/B/C quadratic blocks; positivity/nonnegative rest terms; domain/norm convention; C_tr source route; Pi_R fallback constants if trace fails",
            exclusions="scoring K_qR without w_RAB/C_tr or flux constants; assuming no R_AB slot from silence; using Cassini ceiling as prediction; closure q_R=0; local GR/Newton/PPN claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    hunt: list[dict[str, object]],
    theorems: list[dict[str, object]],
    switches: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2085_0_source_weight_wRAB",
            SOURCE_WEIGHT_DOCS / "AFRAME_WRAB_CTR_OWNER_OR_FLUX_SWITCH_2085_NONCLAIM.csv",
            hunt + theorems + dry,
        ),
        (
            "COPY2085_1_wep_wRAB",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2085_WRAB_CTR_NONCLAIM.csv",
            theorems + switches + dry,
        ),
        (
            "COPY2085_2_queue_2086",
            QUEUE / "JR2085_PARENT_QUADRATIC_FORM_OR_PIR_FLUX_SWITCH_QUEUE.csv",
            switches + next_rows_,
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
    hunt: list[dict[str, object]],
    theorems: list[dict[str, object]],
    symbols: list[dict[str, object]],
    switches: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    hunt_missing_ok = all("OWNER_NOT_FOUND" in str(r["current_status"]) or "FALLBACK_OWNER_NOT_FOUND" in str(r["current_status"]) for r in hunt)
    block_diag_ok = any(r["theorem_id"] == "THM2085_0_block_diagonal_weight" and "min(a0,a1)" in str(r["output"]) for r in theorems)
    schur_ok = any(
        r["theorem_id"] == "THM2085_2_cross_term_schur_bound"
        and "A - B C^{-1} B^T" in str(r["statement"])
        for r in theorems
    )
    trace_contract_ok = any(r["theorem_id"] == "THM2085_3_trace_constant_contract" for r in theorems)
    switch_rule_ok = any(r["theorem_id"] == "THM2085_4_trace_failure_switch_rule" for r in theorems)
    symbol_ok = any(r["symbol_id"] == "SYM2085_0_C_tr_trace_constant" for r in symbols)
    switch_prepared = any(r["switch_id"] == "SW2085_3_best_next" and r["current_status"] == "SELECTED_NEXT" for r in switches)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in dry)
    gates_blocked = all(not truthy(r.get("claim_allowed")) for r in gates)
    absence_not_proved = any(r["decision_id"] == "DEC2085_2_trace_absence_not_proved" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2085_0_2086"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [hunt, theorems, symbols, switches, dry, gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2085_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2085_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2085_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2085_02_owner_hunt_missing", hunt_missing_ok, "w_RAB/C_tr/flux owners are not found and not fabricated"),
        ("VAL2085_03_block_diagonal_formula", block_diag_ok, "block diagonal w_RAB=min(a0,a1) formula is written"),
        ("VAL2085_04_schur_formula", schur_ok, "cross-term Schur coercivity formula is written"),
        ("VAL2085_05_trace_contract", trace_contract_ok, "C_tr trace constant contract is written"),
        ("VAL2085_06_switch_rule", switch_rule_ok, "trace failure switch rule is written"),
        ("VAL2085_07_symbol_hygiene", symbol_ok, "C_tr symbol collision is guarded"),
        ("VAL2085_08_switch_prepared", switch_prepared, "flux switch is prepared but not activated without absence proof"),
        ("VAL2085_09_dry_refusal", dry_refused, "all dry-run branches refuse missing inputs"),
        ("VAL2085_10_claim_gates_blocked", gates_blocked, "claim gates remain blocked"),
        ("VAL2085_11_absence_not_proved", absence_not_proved, "trace absence is not claimed from missing source rows"),
        ("VAL2085_12_next_selected", next_ok, "2086 parent quadratic-form/flux switch target selected"),
        ("VAL2085_13_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2085_14_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2085_15_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2085_16_no_formalization_artifacts", no_formalization_artifacts, "no 2085 artifacts were written under formalization-workbench"),
        ("VAL2085_17_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2085_OVERALL", overall, "2085 derives w_RAB/C_tr owner formulae, refuses scoring, and selects parent quadratic-form extraction or Pi_R flux switch"))
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
    hunt: list[dict[str, object]],
    theorems: list[dict[str, object]],
    symbols: list[dict[str, object]],
    switches: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2085 Y5 R2FR R_AB Energy Weight w_RAB And Trace Constant Owner Or Flux Switch",
        "",
        "## Current Verdict",
        "",
        "2085 does not find a source-backed `w_RAB` or selected-domain `C_tr(D_ext,S_ext,gamma)` owner in the current corpus. That blocks the trace route from scoring, but it is not yet a proof that the trace route is absent.",
        "",
        "The useful derivation is now exact. If the parent finite norm has a block-diagonal `R_AB` slot, `X_E^2 >= int_D (a0 R_AB^2 + a1 |nabla R_AB|^2) dmu`, then `w_RAB=min(a0,a1)` and `K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*min(a0,a1))` in the unit-`Q_R` convention.",
        "",
        "If there are cross terms with other reciprocal variables, the safe owner is the Schur complement: `w_RAB=lambda_min(A - B C^{-1} B^T)`, provided the complementary block `C` is positive and the lower bound is positive. If this lower bound is not positive or not parent-signed, trace extraction is noncoercive.",
        "",
        "The flux switch is prepared but not activated. Missing `w_RAB` is not the same as proving there is no `R_AB` energy slot. The next step has to inspect the parent reciprocal quadratic form directly; only then can we either fill `w_RAB/C_tr` or cleanly switch to `Pi_R` flux ownership.",
        "",
        "Symbol hygiene: `C_tr(D_ext,S_ext,gamma)` here is a Sobolev trace constant, not the older trace-sector coupling `C_tr(Phi)` used around the trace-action/double-zero work.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## Owner Hunt",
        md_table(hunt, ["hunt_id", "target", "evidence", "current_status", "consequence", "claim_allowed", "valid_for_claim"]),
        "## Coercivity And Trace Theorems",
        md_table(theorems, ["theorem_id", "route", "statement", "output", "status", "missing_inputs", "claim_allowed", "valid_for_claim"]),
        "## Symbol Hygiene",
        md_table(symbols, ["symbol_id", "symbol", "meaning", "must_not_confuse_with", "status", "claim_allowed", "valid_for_claim"]),
        "## Switch Ledger",
        md_table(switches, ["switch_id", "branch", "condition", "current_status", "action", "claim_allowed", "valid_for_claim"]),
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
    hunt = owner_hunt_rows()
    theorems = coercivity_theorem_rows()
    symbols = symbol_hygiene_rows()
    switches = switch_ledger_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2085_SOURCE_REGISTER.csv",
        "hunt": OUT / "P8_Y5_PARENT_QLOC_2085_OWNER_HUNT.csv",
        "theorems": OUT / "P8_Y5_PARENT_QLOC_2085_COERCIVITY_TRACE_THEOREMS.csv",
        "symbols": OUT / "P8_Y5_PARENT_QLOC_2085_SYMBOL_HYGIENE.csv",
        "switches": OUT / "P8_Y5_PARENT_QLOC_2085_SWITCH_LEDGER.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2085_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2085_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2085_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2085_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2085_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2085_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["hunt"], hunt)
    write_csv(paths["theorems"], theorems)
    write_csv(paths["symbols"], symbols)
    write_csv(paths["switches"], switches)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(hunt, theorems, switches, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, hunt, theorems, symbols, switches, dry, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, hunt, theorems, symbols, switches, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
