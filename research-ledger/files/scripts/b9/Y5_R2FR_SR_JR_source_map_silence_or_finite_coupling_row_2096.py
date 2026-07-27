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
    read_csv,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2096-Y5-R2FR-SR-JR-source-map-silence-or-finite-coupling-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2095 = ROOT / "2095-Y5-R2FR-ZR-MR2-operator-signature-source-row.md"
SRC_2089 = ROOT / "2089-Y5-R2FR-parent-Euler-source-map-contract-integration-or-finite-trace-input-lock.md"
SRC_2034 = ROOT / "2034-Y5-R2FR-Lcore-theta-current-fill-or-first-finite-Z-source.md"
SRC_1957 = ROOT / "1957-Y5-R2FR-source-map-signature-or-residual-current-bound.md"
SRC_1955 = ROOT / "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md"
SRC_1461 = ROOT / "1461-Y5-R10-RAB-parent-source-factorization-no-relative-source-label-proof-or-CMSM-inventory.md"
SRC_1577 = ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md"
CSV_1573_TAU = OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv"
CSV_2092_INTAKE = OUT / "P8_Y5_PARENT_QLOC_2092_FINITE_INPUT_INTAKE.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def safe_read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def csv_rows_with_missing(rows: list[dict[str, str]]) -> str:
    values: list[str] = []
    for csv_row in rows:
        for value in csv_row.values():
            text = str(value)
            if ("MISSING_" in text or "SOURCE_BACKED_ROW_MISSING" in text or "REVIEWED_CANDIDATE_NOT_ACCEPTED" in text) and text not in values:
                values.append(text)
    return "; ".join(values[:12])


def formalization_has_2096_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2096-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2096*",
        "*Y5_R2FR_SR_JR_source_map_silence_or_finite_coupling_row_2096*",
        "*AFRAME_SR_JR_SOURCE_MAP_2096*",
        "*JR2096_CURRENT_OWNER_NONHILBERT_NEXT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2096_00_2095_handoff",
            SRC_2095,
            ["NEXT2095_0_2096", "MOVE_TO_SR_JR_SOURCE_MAP_SILENCE_OR_FINITE_COUPLING_ROW", "VAL2095_OVERALL"],
            "2095 selects S_R/J_R source-map coupling after q_R and Z_R/M_R^2 remain blocked.",
        ),
        (
            "SRC2096_01_2089_source_residuals",
            SRC_2089,
            ["PEG2089_2_source_map_SR", "SRI2089_1_JR_lambda", "SRI2089_7_readout_projector"],
            "2089 names the S_R residual components and keeps source/readout slots nonclaim.",
        ),
        (
            "SRC2096_02_2034_JR_formula",
            SRC_2034,
            ["HESS2034_4_source_formula", "FZ2034_3_JR", "GATE2034_4_matter_boundary"],
            "2034 gives the exact J_R source formula from parent variation.",
        ),
        (
            "SRC2096_03_1957_source_map",
            SRC_1957,
            ["SM1957_6_verdict", "CUR1957_0_DeltaT_source_bound", "VAL1957_OVERALL"],
            "1957 reduces source-map zero to current-owner, non-Hilbert silence and readout no-reentry.",
        ),
        (
            "SRC2096_04_1955_same_source",
            SRC_1955,
            ["EH1955_2_same_source_map", "EH1955_6_zero_verdict", "VAL1955_OVERALL"],
            "1955 gives the EH same-source contract and blocks local-GR claims until source clauses sign.",
        ),
        (
            "SRC2096_05_1461_source_factorization",
            SRC_1461,
            ["NRS1461_0_source_functor_domain", "NRS1461_5_delta_q_zero_decision", "VAL1461_14_overall"],
            "1461 reduces source-label forgetting to exact parent clauses but leaves countermodels live.",
        ),
        (
            "SRC2096_06_1577_bulk_source",
            SRC_1577,
            ["FCF1577_2_bulk_source", "ARI1577_1_R10", "VAL1577_OVERALL"],
            "1577 keeps J_R/beta source-test coupling as missing finite component rows.",
        ),
        (
            "SRC2096_07_1573_tau_inputs",
            CSV_1573_TAU,
            ["REQ1573_2_beta_source", "MISSING_SOURCE_CHARGE", "REQ1573_3_beta_test"],
            "1573 records R10 source/test charge inputs as missing.",
        ),
        (
            "SRC2096_08_2092_intake",
            CSV_2092_INTAKE,
            ["INT2092_1_JR_SR", "SOURCE_BACKED_ROW_MISSING", "INT2092_8_no_cancellation"],
            "2092 finite intake records J_R/S_R source-backed rows as missing.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2096_SR_JR_source_map_coupling_gate",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2096=note,
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return rows


def source_map_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="SRJ2096_0_target",
            clause="source-map target",
            statement="For the micro-kernel C_R'=S_R, local reciprocity needs S_R=0 or a source-backed finite envelope in protected local exterior.",
            status="TARGET_SHARP",
            missing_for_zero="parent matter/source/readout/boundary descent signatures",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="SRJ2096_1_parent_variation_formula",
            clause="J_R source formula",
            statement="J_R=[partial L/partial u - nabla_mu(partial L/partial(D_mu u))]_0 with u=R_AB or C_R-compatible reciprocal variable.",
            status="FORMULA_EXACT_NONNUMERIC",
            missing_for_zero="parent Lagrangian/source action evaluated in the u row",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="SRJ2096_2_factorisation_zero",
            clause="quotient/factorisation silence",
            statement="If L_phys, S_matter and readout/boundary maps factor through quotient observables and not u or D_mu u, then the u-source row vanishes.",
            status="EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            missing_for_zero="parent-domain/generator certificate and readout-after-variation stability",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="SRJ2096_3_matter_descent",
            clause="ordinary matter descent",
            statement="S_matter must couple to the same observed coframe/source measure without hidden reciprocal/source-label slots.",
            status="CONDITIONAL_NOT_PARENT_SIGNED",
            missing_for_zero="common measure/current, no source-only weights, and no hidden marker/source hom",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="SRJ2096_4_current_owner",
            clause="Hilbert current owner",
            statement="The active source current must be the Hilbert/coframe variation of the same parent matter action.",
            status="CURRENT_OWNER_NOT_SIGNED",
            missing_for_zero="Noether/Hilbert/readout current ownership stack",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="SRJ2096_5_nonHilbert_silence",
            clause="non-Hilbert bypass",
            statement="Spin/torsion/boundary/non-Hilbert current bypasses must be absent, exact/projected-silent, or source-bounded.",
            status="OPEN_PARALLEL_GATE",
            missing_for_zero="J_NH zero/exact/projected-silent theorem or finite residual envelope",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="SRJ2096_6_readout_no_reentry",
            clause="readout no-reentry",
            statement="Readout/source-worldtube kernels cannot recreate source/material/hidden labels after variation.",
            status="CONDITIONAL_NOT_PARENT_SIGNED",
            missing_for_zero="variation-before-readout theorem and official/readout kernel source rows",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="SRJ2096_7_verdict",
            clause="S_R/J_R source silence",
            statement="S_R/J_R source silence is not derived in the current corpus; the coupling gap is a finite residual-current problem unless current-owner and silence clauses sign.",
            status="SOURCE_SILENCE_ZERO_PROOF_FAILED_CLEANLY",
            missing_for_zero="current owner, non-Hilbert silence, readout no-reentry, and source-backed residual envelopes",
            theorem_zero_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def finite_coupling_rows() -> list[dict[str, object]]:
    tau_rows = safe_read_csv(CSV_1573_TAU)
    intake_rows = safe_read_csv(CSV_2092_INTAKE)
    return [
        row(
            coupling_id="CPL2096_0_JR_SR",
            quantity="J_R or S_R",
            role="source side of C_R'=S_R",
            required_evidence="parent variation row or theorem-zero with units and source path",
            current_status="SOURCE_BACKED_ROW_MISSING",
            evidence_hint="2092 intake: " + csv_rows_with_missing(intake_rows),
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            coupling_id="CPL2096_1_beta_source",
            quantity="beta_S^R",
            role="R10/source-body reciprocal charge",
            required_evidence="partial ln m_source / partial u or source-material theorem-zero",
            current_status="MISSING_SOURCE_CHARGE",
            evidence_hint="1573 tau inputs",
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            coupling_id="CPL2096_2_beta_test",
            quantity="beta_T^R",
            role="R10/test-body reciprocal charge",
            required_evidence="partial ln m_test / partial u or test-material theorem-zero",
            current_status="MISSING_TEST_CHARGE",
            evidence_hint="1573 tau inputs: " + csv_rows_with_missing(tau_rows),
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            coupling_id="CPL2096_3_deltaT_source",
            quantity="DeltaT_source",
            role="ordinary matter/source-map residual after GR baseline subtraction",
            required_evidence="DeltaT_w, DeltaT_NH, DeltaT_readout theorem-zero or finite norms",
            current_status="MISSING_RESIDUAL_CURRENT_ENVELOPES",
            evidence_hint="1957 residual current ledger",
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            coupling_id="CPL2096_4_q_loc_feedthrough",
            quantity="epsilon_GK_q_loc into S_R",
            role="extra-sector force residual contamination of Euler/source map",
            required_evidence="q_loc parent-zero theorem or source-backed bound",
            current_status="QLOC_RETAINED_NONCLAIM",
            evidence_hint="2089 S_R residual integration",
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            coupling_id="CPL2096_5_readout_marker",
            quantity="Delta_readout or source-worldtube marker residual",
            role="post-variation source/readout re-entry",
            required_evidence="readout no-reentry theorem or finite calibration/source-worldtube envelope",
            current_status="MISSING_READOUT_NO_REENTRY_OR_BOUND",
            evidence_hint="1957/1461 readout no-reentry gates",
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            coupling_id="CPL2096_6_no_cancellation",
            quantity="absolute source envelope",
            role="forbid cancellation between source, q_loc, boundary, operator and readout pieces",
            required_evidence="component-by-component zero theorem or absolute bound",
            current_status="NO_CANCELLATION_REQUIRED_NOT_SATISFIED",
            evidence_hint="2092 no-cancellation intake row",
            source_backed=False,
            score_ready=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def countermodel_rows() -> list[dict[str, object]]:
    return [
        row(
            countermodel_id="CM2096_0_relative_source_weight",
            countermodel="S_matter=sum_A w_A S_A",
            effect="species/source labels become real coupling coefficients and J_R can survive",
            blocked_by="parent source-label forgetting plus common current normalization",
            status="RETAIN_LIVE_NONCLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2096_1_species_jacobian",
            countermodel="species-dependent measure/current normalization J_A",
            effect="Hilbert total-source uniqueness is bypassed",
            blocked_by="common measure/current parent theorem",
            status="RETAIN_LIVE_NONCLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2096_2_hidden_marker_source",
            countermodel="source coefficient depends on hidden marker/material slot",
            effect="matter can be WEP-looking while still sourcing u through a marker channel",
            blocked_by="no-hidden-visible-hom and no-marker extension theorem",
            status="RETAIN_LIVE_NONCLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2096_3_nonHilbert_current",
            countermodel="J_src=kappa T_Hilbert + J_NH",
            effect="extra current survives without appearing as ordinary stress",
            blocked_by="J_NH=0/exact/projected-silent theorem or finite envelope",
            status="RETAIN_LIVE_NONCLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2096_4_readout_selector_reentry",
            countermodel="readout/source-worldtube kernel selects material/source profile after variation",
            effect="variation-stage source silence can be undone by measurement/readout",
            blocked_by="readout no-reentry theorem and official kernel/source rows",
            status="RETAIN_LIVE_NONCLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def arena_consequence_rows() -> list[dict[str, object]]:
    return [
        row(
            arena_id="ARENA2096_0_R10",
            observable="alpha_MTS(lambda_R)",
            source_formula="Xi_R10[beta_S^R beta_T^R/(4 pi G Z_R)+alpha_boundary_tail]",
            current_status="BLOCKED_BETA_ZR_BOUNDARY_CURVE_MISSING",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            arena_id="ARENA2096_1_PPN",
            observable="gamma/beta/source residual vector",
            source_formula="Delta_source enters q_R_hat/tail envelope and same-source local-EH map",
            current_status="BLOCKED_SOURCE_CURRENT_AND_TAIL_ENVELOPES_MISSING",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            arena_id="ARENA2096_2_WEP_MICROSCOPE",
            observable="composition/source-label residual",
            source_formula="delta_q(x) or source-label coefficient rows",
            current_status="BLOCKED_SOURCE_LABEL_FORGETTING_UNSIGNED",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            arena_id="ARENA2096_3_clock_orbital",
            observable="clock/orbital material and source-map tails",
            source_formula="tau_clock/tau_orbital times source/material sensitivity components",
            current_status="BLOCKED_NO_SAME_FRAME_SOURCE_MAP",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2096_0_SR_zero", "S_R/J_R source silence is parent-derived", "FAIL_BLOCKED", "current-owner, non-Hilbert, source-label and readout clauses are unsigned"),
        ("GATE2096_1_matter_descent", "ordinary matter descent removes u/source-label dependence", "FAIL_BLOCKED", "source functor/common measure/current and no hidden marker are not parent-signed"),
        ("GATE2096_2_finite_coupling", "finite source/coupling rows are score-ready", "FAIL_MISSING_VALUES", "J_R, beta_S^R, beta_T^R, DeltaT and readout envelopes are missing"),
        ("GATE2096_3_R10_PPN", "R10/PPN source-side score is allowed", "FAIL_BLOCKED", "source rows plus q_R/Q_R, Z_R/M_R2, boundary and arena projections remain incomplete"),
        ("GATE2096_4_local_GR", "local GR/Newton source side is derived", "FAIL_BLOCKED", "same-source theorem exact but unsigned; finite fallback not scoreable"),
    ]
    return [
        row(gate_id=gate_id, claim=claim, status=status, reason=reason, claim_allowed=False, valid_for_claim=False)
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2096_0_source_silence",
            decision="SR_JR_ZERO_THEOREM_NOT_DERIVED",
            basis="J_R has an exact parent-variation formula, but matter descent/current-owner/non-Hilbert/readout clauses are not parent-signed.",
            consequence="do not set S_R=0 by vacuum wording or WEP intuition.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2096_1_finite_rows",
            decision="FINITE_COUPLING_ROWS_NOT_SCORE_READY",
            basis="J_R/S_R, beta_S^R, beta_T^R, DeltaT_source, q_loc feedthrough and readout rows are missing or nonclaim.",
            consequence="no R10/PPN/clock/orbital score can use source-side cancellation or placeholder charges.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2096_2_best_next",
            decision="ATTACK_CURRENT_OWNER_NONHILBERT_READOUT_SILENCE",
            basis="1957 identifies current-owner and non-Hilbert/readout silence as the hard source-side blockers; they are more direct than another broad source audit.",
            consequence="2097 should try to prove those clauses or emit first residual-current envelope rows.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2096_0_2097",
            target_doc="2097-Y5-R2FR-current-owner-nonHilbert-readout-silence-or-current-envelope.md",
            target_script="scripts/Y5_R2FR_current_owner_nonHilbert_readout_silence_or_current_envelope_2097.py",
            objective="prove Hilbert current ownership plus non-Hilbert/readout silence for the S_R/J_R source side, or emit first source-backed residual current envelope rows",
            success_condition="current-owner/non-Hilbert/readout clauses become parent-signed zeroes, or DeltaT_w/DeltaT_NH/DeltaT_readout rows are source-backed finite inputs; no source-side/local-GR claim otherwise",
            forbidden_shortcuts="WEP-only source silence; source-free by assertion; cancellation between source channels; post-variation readout relabeling; GR source equation import; GitHub; formalization-workbench edits",
            claim_allowed=False,
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    theorem: list[dict[str, object]],
    finite: list[dict[str, object]],
    counters: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_SR_JR_SOURCE_MAP_2096_NONCLAIM.csv",
            theorem + counters + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2096_SR_JR_COUPLING_GATE_NONCLAIM.csv",
            theorem + finite + arenas,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2096_CURRENT_OWNER_NONHILBERT_NEXT_QUEUE.csv",
            finite + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2096_{len(rows)}",
                copy_kind=copy_kind,
                path=str(path),
                rows=len(data_rows),
                parses=csv_rows_parse(path),
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    finite: list[dict[str, object]],
    counters: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    formula_ok = any(r["theorem_id"] == "SRJ2096_1_parent_variation_formula" and r["status"] == "FORMULA_EXACT_NONNUMERIC" for r in theorem)
    zero_fail_ok = any(r["theorem_id"] == "SRJ2096_7_verdict" and r["status"] == "SOURCE_SILENCE_ZERO_PROOF_FAILED_CLEANLY" for r in theorem)
    finite_blocked = all(not truthy(r["source_backed"]) and not truthy(r["score_ready"]) for r in finite)
    counters_live = len(counters) >= 5 and all(r["status"] == "RETAIN_LIVE_NONCLAIM" for r in counters)
    arenas_blocked = all(str(r["current_status"]).startswith("BLOCKED") for r in arenas)
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and any(r["gate_id"] == "GATE2096_0_SR_zero" and r["status"] == "FAIL_BLOCKED" for r in gates)
    decision_ok = any(r["decision_id"] == "DEC2096_2_best_next" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2096_0_2097"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, theorem, finite, counters, arenas, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2096_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2096_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2096_01_formula", formula_ok, "J_R parent-variation formula is recorded"),
        ("VAL2096_02_zero_fail", zero_fail_ok, "S_R/J_R zero proof fails cleanly without promotion"),
        ("VAL2096_03_finite_blocked", finite_blocked, "finite coupling rows are not source-backed or score-ready"),
        ("VAL2096_04_countermodels", counters_live, "source-side countermodels remain live and nonclaim"),
        ("VAL2096_05_arenas", arenas_blocked, "R10/PPN/WEP/clock/orbital arenas remain blocked"),
        ("VAL2096_06_claim_gates", gates_safe, "claim gates block source-side/local-GR claims"),
        ("VAL2096_07_decision", decision_ok, "decision selects current-owner/non-Hilbert/readout next"),
        ("VAL2096_08_next", next_ok, "next target is 2097 current-owner/non-Hilbert/readout silence"),
        ("VAL2096_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2096_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2096_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2096_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2096"),
        ("VAL2096_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, claim_allowed=False, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2096_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2096 records S_R/J_R as a precise source-map coupling gate, fails source silence cleanly, and selects current-owner/non-Hilbert/readout silence next" if overall else "one or more 2096 validation gates failed",
            claim_allowed=False,
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    finite: list[dict[str, object]],
    counters: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2096 - Y5/R2FR S_R/J_R Source-Map Silence Or Finite Coupling Row",
            "## Current Verdict\n\n2096 names the coupling problem without mist. In the micro-kernel branch, `C_R'=S_R` only gives local reciprocity if the source side is zero or bounded. The exact source formula exists: `J_R=[partial L/partial u - nabla_mu(partial L/partial(D_mu u))]_0`. But the current corpus does not parent-sign the clauses that make it vanish: matter descent, common current normalization, Hilbert-current ownership, non-Hilbert silence, and readout no-reentry.\n\nSo the source side is not dead, but it is not free. `S_R/J_R` is now a precise finite residual-current problem: either prove current-owner/non-Hilbert/readout silence, or source finite `DeltaT_w`, `DeltaT_NH`, `DeltaT_readout`, `beta_S^R`, and `beta_T^R` rows. No R10/PPN/clock/orbital/local-GR claim is allowed from source-side intuition alone.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2096", "claim_allowed", "valid_for_claim"]),
            "## S_R/J_R Source-Map Theorem Attempt",
            md_table(theorem, ["theorem_id", "clause", "statement", "status", "missing_for_zero", "theorem_zero_signed", "claim_allowed", "valid_for_claim"]),
            "## Finite Coupling Rows",
            md_table(finite, ["coupling_id", "quantity", "role", "required_evidence", "current_status", "evidence_hint", "source_backed", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## Source-Side Countermodels",
            md_table(counters, ["countermodel_id", "countermodel", "effect", "blocked_by", "status", "claim_allowed", "valid_for_claim"]),
            "## Arena Consequences",
            md_table(arenas, ["arena_id", "observable", "source_formula", "current_status", "claim_allowed", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "status", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows_, ["target_id", "target_doc", "target_script", "objective", "success_condition", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "copy_kind", "path", "rows", "parses", "claim_allowed", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    theorem = source_map_theorem_rows()
    finite = finite_coupling_rows()
    counters = countermodel_rows()
    arenas = arena_consequence_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2096_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2096_SR_JR_THEOREM_ATTEMPT.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2096_FINITE_COUPLING_ROWS.csv",
        "counters": OUT / "P8_Y5_PARENT_QLOC_2096_SOURCE_COUNTERMODELS.csv",
        "arenas": OUT / "P8_Y5_PARENT_QLOC_2096_ARENA_CONSEQUENCES.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2096_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2096_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2096_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2096_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2096_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["finite"], finite)
    write_csv(paths["counters"], counters)
    write_csv(paths["arenas"], arenas)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(theorem, finite, counters, arenas, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, theorem, finite, counters, arenas, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem, finite, counters, arenas, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
