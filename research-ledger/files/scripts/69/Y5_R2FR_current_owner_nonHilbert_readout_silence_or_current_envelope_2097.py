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


DOC = ROOT / "2097-Y5-R2FR-current-owner-nonHilbert-readout-silence-or-current-envelope.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2096 = ROOT / "2096-Y5-R2FR-SR-JR-source-map-silence-or-finite-coupling-row.md"
SRC_1957 = ROOT / "1957-Y5-R2FR-source-map-signature-or-residual-current-bound.md"
SRC_1958 = ROOT / "1958-Y5-R2FR-current-owner-nonHilbert-silence-or-current-bound.md"
SRC_1959 = ROOT / "1959-Y5-R2FR-torsion-boundary-readout-current-silence-or-envelope.md"
SRC_1960 = ROOT / "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md"
SRC_1829 = ROOT / "1829-Y5-R2FR-metric-only-connection-theorem-or-P4-hinge-source-pack.md"
SRC_1830 = ROOT / "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md"
CSV_1594_AWT = OUT / "P8_Y5_PARENT_QLOC_1594_ACTION_WEIGHT_EXCLUSION_THEOREM_ATTEMPT.csv"
CSV_1594_CMC = OUT / "P8_Y5_PARENT_QLOC_1594_COMMON_MEASURE_CURRENT_AUDIT.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2097_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2097-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2097*",
        "*Y5_R2FR_current_owner_nonHilbert_readout_silence_or_current_envelope_2097*",
        "*AFRAME_CURRENT_OWNER_NONHILBERT_2097*",
        "*JR2097_LC_NOHYPERMOMENTUM_NEXT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2097_00_2096_handoff",
            SRC_2096,
            ["NEXT2096_0_2097", "ATTACK_CURRENT_OWNER_NONHILBERT_READOUT_SILENCE", "VAL2096_OVERALL"],
            "2096 sharpens the S_R/J_R gap into current-owner, non-Hilbert and readout clauses.",
        ),
        (
            "SRC2097_01_1957_source_map",
            SRC_1957,
            ["SM1957_3_current_owner", "SM1957_4_nonHilbert_silence", "CUR1957_3_DeltaT_readout"],
            "1957 names the residual current vector and keeps current/non-Hilbert/readout blockers live.",
        ),
        (
            "SRC2097_02_1958_current_owner",
            SRC_1958,
            ["OWN1958_0_target", "OWN1958_6_verdict", "VAL1958_OVERALL"],
            "1958 tries current ownership and exposes spin/torsion, boundary, readout and improvement bypasses.",
        ),
        (
            "SRC2097_03_1959_bypass_channels",
            SRC_1959,
            ["SIL1959_0_target", "SIL1959_6_verdict", "ENV1959_0_combined_nonHilbert"],
            "1959 decomposes the bypass current into torsion/nonmetricity, boundary, readout and improvement terms.",
        ),
        (
            "SRC2097_04_1960_LC_route",
            SRC_1960,
            ["LC1960_0_target", "LC1960_6_verdict", "P4C1960_5_hypermomentum"],
            "1960 shows the clean Levi-Civita/no-hypermomentum route is exact but unsigned, with P4 fallback rows.",
        ),
        (
            "SRC2097_05_1829_metric_only_lemma",
            SRC_1829,
            ["MOC1829_1_exact_lemma", "MOC1829_3_matter_no_hypermomentum", "DEC1829_0_theorem_result"],
            "1829 gives the exact metric-only connection lemma and identifies the missing no-hypermomentum premise.",
        ),
        (
            "SRC2097_06_1830_field_grammar",
            SRC_1830,
            ["NIC1830_0_target", "NIC1830_3_no_hypermomentum", "DEC1830_0_grammar_result"],
            "1830 tests no independent connection/hypermomentum at parent grammar level and keeps the route blocked.",
        ),
        (
            "SRC2097_07_1594_action_weight",
            CSV_1594_AWT,
            ["AWT1594_6_nonHilbert_bypass", "AWT1594_7_verdict", "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED"],
            "1594 keeps non-Hilbert bypass and action-weight exclusion as strict finite-row validator debts.",
        ),
        (
            "SRC2097_08_1594_common_current",
            CSV_1594_CMC,
            ["CMC1594_4_no_nonhilbert_current", "CMC1594_7_verdict", "COMMON_MEASURE_CURRENT_NOT_DERIVED"],
            "1594 common-measure/current audit keeps no-non-Hilbert-current unsigned.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2097_current_owner_nonHilbert_readout_gate",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2097=use,
                valid_for_claim=False,
            )
        )
    return rows


def current_owner_attempt_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="CUR2097_0_target",
            clause="active current owner",
            statement="Prove J_active = J_Hilbert[S_matter,e_obs] and P2[J_NH]=0 before using S_R/J_R as a local-GR source silence.",
            status="TARGET_SHARP",
            missing_for_zero="parent variation owner; no independent connection/hypermomentum; boundary and readout silence",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="CUR2097_1_hilbert_owner_identity",
            clause="Hilbert owner identity",
            statement="If matter couples only through the observed coframe/metric and variation is taken before readout, the source is the Hilbert/coframe current.",
            status="EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            missing_for_zero="single matter action, common measure/current and variation-before-readout certificate",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="CUR2097_2_nonHilbert_split",
            clause="non-Hilbert split",
            statement="J_active = J_Hilbert + J_spin/torsion + J_boundary + J_readout + J_improvement + J_shadow_connection.",
            status="DECOMPOSITION_FOR_AUDIT_NONCLAIM",
            missing_for_zero="each non-Hilbert term must be theorem-zero, projected silent, or bounded without cancellation",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="CUR2097_3_connection_hypermomentum",
            clause="spin/torsion/nonmetricity channel",
            statement="If an independent connection or hypermomentum slot exists, spin/torsion/nonmetricity can source local residual current even when metric WEP language looks clean.",
            status="LIVE_ESCAPE_ROUTE",
            missing_for_zero="Levi-Civita/no-hypermomentum parent field-inventory certificate or P4 envelope rows",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="CUR2097_4_boundary_worldtube",
            clause="boundary/source-worldtube current",
            statement="Canonical-to-Hilbert improvement terms and source-worldtube fluxes must vanish under the local projection or be bounded.",
            status="LIVE_ESCAPE_ROUTE",
            missing_for_zero="boundary condition, compact support, falloff and projection silence theorem",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="CUR2097_5_readout_reentry",
            clause="readout no-reentry",
            statement="Post-variation readout cannot reintroduce species/source/hidden marker dependence into the projected source current.",
            status="LIVE_ESCAPE_ROUTE",
            missing_for_zero="readout kernel, marker null theorem and variation-before-readout commutation row",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="CUR2097_6_no_cancellation",
            clause="no source-channel cancellation",
            statement="A local pass cannot rely on J_spin/torsion + J_boundary + J_readout cancelling numerically unless the parent action forces the cancellation identity.",
            status="SAFETY_RULE_ACTIVE",
            missing_for_zero="independent zero or bound for each channel",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="CUR2097_7_verdict",
            clause="current owner/non-Hilbert/readout silence",
            statement="The zero proof fails in the current corpus: the route is exact as a contract, but current-owner, non-Hilbert and readout silence are not parent-signed.",
            status="CURRENT_OWNER_NONHILBERT_READOUT_ZERO_FAILED_CLEANLY",
            missing_for_zero="field-inventory/no-hypermomentum certificate, boundary/readout silence, or source-backed finite envelope rows",
            theorem_zero_signed=False,
            valid_for_claim=False,
        ),
    ]


def current_envelope_rows() -> list[dict[str, object]]:
    return [
        row(
            envelope_id="ENV2097_0_DeltaT_current_total",
            quantity="DeltaT_current_total",
            formula="||P2[J_active-J_Hilbert]|| <= DeltaT_w + DeltaT_NH + DeltaT_boundary + DeltaT_readout + DeltaT_improvement + DeltaT_shadow",
            required_evidence="same projection norm, operator normalization, source path and arena weak-field map for each term",
            current_status="MISSING_COMPONENT_BOUNDS",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="ENV2097_1_DeltaT_w",
            quantity="DeltaT_w",
            formula="relative source/action weight current residual",
            required_evidence="source-weight theorem zero or coefficient with units and weak-field map",
            current_status="MISSING_SOURCE_WEIGHT_ZERO_OR_BOUND",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="ENV2097_2_DeltaT_NH",
            quantity="DeltaT_NH",
            formula="spin/torsion/nonmetricity/non-Hilbert source current envelope",
            required_evidence="Levi-Civita/no-hypermomentum theorem or P4 source-backed coefficients",
            current_status="MISSING_P4_CURRENT_INPUTS",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="ENV2097_3_DeltaT_boundary",
            quantity="DeltaT_boundary",
            formula="projected boundary and source-worldtube current flux",
            required_evidence="compact-support/falloff theorem or bounded surface term with units",
            current_status="MISSING_BOUNDARY_FLUX_INPUT",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="ENV2097_4_DeltaT_readout",
            quantity="DeltaT_readout",
            formula="readout/source-marker reentry current residual",
            required_evidence="readout commutation theorem or marker sensitivity coefficient",
            current_status="MISSING_READOUT_REENTRY_INPUT",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="ENV2097_5_DeltaT_improvement",
            quantity="DeltaT_improvement",
            formula="canonical-to-Hilbert improvement flux after projection",
            required_evidence="superpotential divergence projected silent or finite surface-flux row",
            current_status="MISSING_IMPROVEMENT_FLUX_INPUT",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="ENV2097_6_DeltaT_shadow",
            quantity="DeltaT_shadow",
            formula="hidden/shadow connection or representative current feedthrough",
            required_evidence="single geometry-stack theorem or explicit shadow-current coefficient",
            current_status="MISSING_SHADOW_CONNECTION_INPUT",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="ENV2097_7_projection_norm",
            quantity="K_P2_current",
            formula="operator norm sending current residuals into local q_R/Q_R/PPN/R10 observables",
            required_evidence="projection kernel, units, arena map and baseline normalization",
            current_status="MISSING_ARENA_PROJECTION_NORM",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
    ]


def countermodel_rows() -> list[dict[str, object]]:
    return [
        row(
            countermodel_id="CM2097_0_relative_source_weight",
            countermodel="S_matter=sum_A w_A S_A with identical matter equations but different source variation",
            effect="Hilbert current normalization shifts while test dynamics look ordinary",
            blocked_by="action-weight exclusion plus common current owner",
            status="RETAIN_LIVE_NONCLAIM",
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2097_1_spin_torsion_hypermomentum",
            countermodel="ordinary matter carries spin/connection charge in an independent connection branch",
            effect="non-Hilbert current survives metric-only WEP wording",
            blocked_by="Levi-Civita/no-hypermomentum parent certificate",
            status="RETAIN_LIVE_NONCLAIM",
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2097_2_boundary_worldtube_flux",
            countermodel="localized source has nonzero projected boundary or improvement flux",
            effect="source current leaks into the local exterior residual",
            blocked_by="compact support/falloff/projected-boundary theorem",
            status="RETAIN_LIVE_NONCLAIM",
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2097_3_readout_selector_reentry",
            countermodel="readout kernel removes labels in motion equations but reintroduces them in source projection",
            effect="DeltaT_readout remains finite",
            blocked_by="variation-before-readout and marker-null theorem",
            status="RETAIN_LIVE_NONCLAIM",
            valid_for_claim=False,
        ),
        row(
            countermodel_id="CM2097_4_shadow_connection",
            countermodel="Gamma_eff/K_hat is not fully reconciled with omega[e_obs]",
            effect="connection current can hide outside the Hilbert metric current",
            blocked_by="single geometry-stack and Gamma/K_hat compatibility certificate",
            status="RETAIN_LIVE_NONCLAIM",
            valid_for_claim=False,
        ),
    ]


def triage_rows() -> list[dict[str, object]]:
    return [
        row(
            triage_id="TRI2097_0_no_independent_connection",
            next_action="PARENT_FIELD_INVENTORY_NO_INDEPENDENT_CONNECTION_OR_HYPERMOMENTUM",
            priority=1,
            reason="This kills the largest non-Hilbert bypass at the source and connection level if it closes.",
            reuse_sources="1960, 1829, 1830",
            if_fails="fill P4 hypermomentum/torsion/nonmetricity current envelope rows",
            selected=True,
            valid_for_claim=False,
        ),
        row(
            triage_id="TRI2097_1_boundary_flux",
            next_action="BOUNDARY_SOURCE_WORLDTUBE_CURRENT_ZERO_OR_BOUND",
            priority=2,
            reason="Boundary/improvement flux is the next clean current-owner bypass.",
            reuse_sources="1958, 1959",
            if_fails="fill DeltaT_boundary and DeltaT_improvement source rows",
            selected=False,
            valid_for_claim=False,
        ),
        row(
            triage_id="TRI2097_2_readout_reentry",
            next_action="VARIATION_BEFORE_READOUT_MARKER_NULL_THEOREM_OR_BOUND",
            priority=3,
            reason="Readout can make a source look silent in equations but not in projected currents.",
            reuse_sources="1957, 1958, 2096",
            if_fails="fill DeltaT_readout marker-sensitivity row",
            selected=False,
            valid_for_claim=False,
        ),
        row(
            triage_id="TRI2097_3_source_weight",
            next_action="ACTION_WEIGHT_COMMON_CURRENT_EXCLUSION_OR_DELTAW_BOUND",
            priority=4,
            reason="Source weights are already well-audited in 1594; use strict rows, not another broad audit.",
            reuse_sources="1594",
            if_fails="fill DeltaT_w with finite source-weight coefficient",
            selected=False,
            valid_for_claim=False,
        ),
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2097_0_current_owner", "active source current is Hilbert/coframe current", "FAIL_BLOCKED", "variation owner and common current stack are not parent-signed"),
        ("GATE2097_1_nonHilbert_silence", "non-Hilbert current is zero or projected silent", "FAIL_BLOCKED", "spin/torsion/hypermomentum, boundary, readout and improvement channels remain live"),
        ("GATE2097_2_readout_no_reentry", "readout cannot recreate source current", "FAIL_BLOCKED", "readout commutation and marker-null rows are missing"),
        ("GATE2097_3_finite_envelope", "finite current envelope is score-ready", "FAIL_MISSING_VALUES", "DeltaT rows, projection norm and arena maps are missing"),
        ("GATE2097_4_R10_PPN", "R10/PPN local source-side score is allowed", "FAIL_BLOCKED", "source current envelope and q_R/Q_R/Z_R rows are not score-ready"),
        ("GATE2097_5_local_GR", "local GR/Newton source side is derived", "FAIL_BLOCKED", "current-owner plus Levi-Civita/no-hypermomentum premises remain unsigned"),
    ]
    return [
        row(gate_id=gate_id, claim=claim, status=status, reason=reason, valid_for_claim=False)
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2097_0_zero_status",
            decision="CURRENT_OWNER_NONHILBERT_READOUT_ZERO_NOT_DERIVED",
            basis="1957-1960 and 2096 agree: the conditional route is exact, but non-Hilbert and readout clauses are not signed by the parent action.",
            consequence="do not claim S_R/J_R=0, local-GR source closure, R10 pass, PPN pass, or WEP-only silence.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2097_1_best_route",
            decision="NO_INDEPENDENT_CONNECTION_HYPERMOMENTUM_FIRST",
            basis="Connection/hypermomentum is the largest upstream bypass: if it closes, torsion/nonmetricity non-Hilbert current collapses cleanly; if not, P4 rows are mandatory.",
            consequence="next work should target the parent field-inventory certificate or first source-backed P4 current envelope row.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2097_2_no_more_broad_circling",
            decision="STOP_BROAD_SOURCE_AUDITS_UNTIL_ONE_INPUT_CLOSES",
            basis="The blocker is now specific: current owner plus non-Hilbert/readout silence, not another naming pass.",
            consequence="advance by proving a parent clause or filling one finite row with units, source path and weak-field map.",
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2097_0_2098",
            target_doc="2098-Y5-R2FR-parent-field-inventory-certificate-refresh-or-first-source-current-envelope-row.md",
            target_script="scripts/Y5_R2FR_parent_field_inventory_certificate_refresh_or_first_source_current_envelope_row_2098.py",
            objective="reopen the 1960/1829/1830 connection route only as a decisive field-inventory certificate attempt; if it fails, fill the first source-backed P4 or current-envelope row",
            success_condition="parent field inventory excludes independent connection/hypermomentum, or at least one finite current-envelope row has numeric/source-backed coefficient, units, weak-field map and valid_for_claim=false until all gates pass",
            forbidden_shortcuts="repeat broad audits; WEP-only silence; GR source equation import; cancellation between current channels; source-free coefficients; GitHub; formalization-workbench edits",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    attempt: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    counters: list[dict[str, object]],
    triage: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_CURRENT_OWNER_NONHILBERT_2097_NONCLAIM.csv",
            attempt + counters + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2097_CURRENT_OWNER_GATE_NONCLAIM.csv",
            attempt + envelopes + triage,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2097_LC_NOHYPERMOMENTUM_NEXT_QUEUE.csv",
            envelopes + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2097_{len(rows)}",
                copy_kind=copy_kind,
                path=str(path),
                rows=len(data_rows),
                parses=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    attempt: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    counters: list[dict[str, object]],
    triage: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    target_ok = any(r["theorem_id"] == "CUR2097_0_target" and r["status"] == "TARGET_SHARP" for r in attempt)
    zero_fail_ok = any(
        r["theorem_id"] == "CUR2097_7_verdict" and r["status"] == "CURRENT_OWNER_NONHILBERT_READOUT_ZERO_FAILED_CLEANLY"
        for r in attempt
    )
    envelopes_blocked = all(not truthy(r["source_backed"]) and not truthy(r["score_ready"]) for r in envelopes)
    counters_live = len(counters) >= 5 and all(r["status"] == "RETAIN_LIVE_NONCLAIM" for r in counters)
    triage_selected = any(
        r["triage_id"] == "TRI2097_0_no_independent_connection" and truthy(r["selected"])
        for r in triage
    )
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and all(str(r["status"]).startswith("FAIL") for r in gates)
    decisions_ok = any(r["decision_id"] == "DEC2097_2_no_more_broad_circling" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2097_0_2098"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, attempt, envelopes, counters, triage, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2097_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2097_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2097_01_target", target_ok, "current-owner theorem target recorded"),
        ("VAL2097_02_zero_fail", zero_fail_ok, "current-owner/non-Hilbert/readout zero proof fails cleanly"),
        ("VAL2097_03_envelopes_blocked", envelopes_blocked, "current envelope rows remain non-source-backed and not score-ready"),
        ("VAL2097_04_countermodels", counters_live, "current bypass countermodels remain live"),
        ("VAL2097_05_triage", triage_selected, "no-independent-connection/no-hypermomentum selected first"),
        ("VAL2097_06_claim_gates", gates_safe, "all claim gates block R10/PPN/local-GR promotion"),
        ("VAL2097_07_decision", decisions_ok, "decision forbids more broad circling before one input closes"),
        ("VAL2097_08_next", next_ok, "next target is 2098 parent field-inventory or first current-envelope row"),
        ("VAL2097_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2097_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2097_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2097_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2097"),
        ("VAL2097_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2097_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2097 consolidates the source-current coupling gate: zero proof fails cleanly, finite envelope rows are explicit, and the next decisive target is no-independent-connection/no-hypermomentum or a first finite row" if overall else "one or more 2097 validation gates failed",
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    attempt: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    counters: list[dict[str, object]],
    triage: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2097 - Y5/R2FR Current Owner Non-Hilbert Readout Silence Or Current Envelope",
            "## Current Verdict\n\n2097 is the coupling-lock checkpoint. It does not prove local GR, but it removes fog from the blocker: `S_R/J_R` cannot be set to zero until the active source current is owned by the same Hilbert/coframe variation and the non-Hilbert/readout bypass channels are either parent-zero or finitely bounded.\n\nThe zero route is exact as a contract, not as a current result. The live obstruction is now small enough to attack directly: prove no independent connection/hypermomentum and no readout/boundary re-entry, or fill `DeltaT_w`, `DeltaT_NH`, `DeltaT_boundary`, `DeltaT_readout`, `DeltaT_improvement`, and projection-norm rows with sourced finite inputs. This is not a failure of the programme; it is the right throat of the maze.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2097", "claim_allowed", "valid_for_claim"]),
            "## Current Owner / Non-Hilbert / Readout Theorem Attempt",
            md_table(attempt, ["theorem_id", "clause", "statement", "status", "missing_for_zero", "theorem_zero_signed", "claim_allowed", "valid_for_claim"]),
            "## Current Envelope Rows",
            md_table(envelopes, ["envelope_id", "quantity", "formula", "required_evidence", "current_status", "source_backed", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## Live Countermodels",
            md_table(counters, ["countermodel_id", "countermodel", "effect", "blocked_by", "status", "claim_allowed", "valid_for_claim"]),
            "## Attack Triage",
            md_table(triage, ["triage_id", "next_action", "priority", "reason", "reuse_sources", "if_fails", "selected", "claim_allowed", "valid_for_claim"]),
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
    attempt = current_owner_attempt_rows()
    envelopes = current_envelope_rows()
    counters = countermodel_rows()
    triage = triage_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2097_SOURCE_REGISTER.csv",
        "attempt": OUT / "P8_Y5_PARENT_QLOC_2097_CURRENT_OWNER_ATTEMPT.csv",
        "envelopes": OUT / "P8_Y5_PARENT_QLOC_2097_CURRENT_ENVELOPE_ROWS.csv",
        "counters": OUT / "P8_Y5_PARENT_QLOC_2097_COUNTERMODELS.csv",
        "triage": OUT / "P8_Y5_PARENT_QLOC_2097_ATTACK_TRIAGE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2097_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2097_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2097_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2097_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2097_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["attempt"], attempt)
    write_csv(paths["envelopes"], envelopes)
    write_csv(paths["counters"], counters)
    write_csv(paths["triage"], triage)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(attempt, envelopes, counters, triage, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, attempt, envelopes, counters, triage, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, attempt, envelopes, counters, triage, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
