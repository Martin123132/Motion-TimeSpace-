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


DOC = ROOT / "2098-Y5-R2FR-parent-field-inventory-certificate-refresh-or-first-source-current-envelope-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2097 = ROOT / "2097-Y5-R2FR-current-owner-nonHilbert-readout-silence-or-current-envelope.md"
SRC_1960 = ROOT / "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md"
SRC_1831 = ROOT / "1831-Y5-R2FR-parent-field-inventory-certificate-or-first-P4-numeric-row.md"
SRC_1832 = ROOT / "1832-Y5-R2FR-torsion-nonmetricity-zero-theorem-or-first-coefficient-source-row.md"
SRC_1833 = ROOT / "1833-Y5-R2FR-distortion-equation-owner-or-hypermomentum-source-row.md"
SRC_1834 = ROOT / "1834-Y5-R2FR-no-hypermomentum-matter-functor-or-DeltaGamma-bound-row.md"
CSV_1830_P4 = OUT / "P8_Y5_PARENT_QLOC_1830_P4_ROW_FILL_CONTRACT.csv"
CSV_1833_HYP = OUT / "P8_Y5_PARENT_QLOC_1833_HYPERMOMENTUM_SOURCE_ROW.csv"
CSV_1834_DG = OUT / "P8_Y5_PARENT_QLOC_1834_DELTAGAMMA_BOUND_ROW.csv"
CSV_1834_DEC = OUT / "P8_Y5_PARENT_QLOC_1834_DECISION_LEDGER.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2098_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2098-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2098*",
        "*Y5_R2FR_parent_field_inventory_certificate_refresh_or_first_source_current_envelope_row_2098*",
        "*AFRAME_DELTAGAMMA_CURRENT_ENVELOPE_2098*",
        "*JR2098_DELTAGAMMA_COMPONENT_MAP*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2098_00_2097_handoff",
            SRC_2097,
            ["NEXT2097_0_2098", "NO_INDEPENDENT_CONNECTION_HYPERMOMENTUM_FIRST", "VAL2097_OVERALL"],
            "2097 selects field inventory/no-hypermomentum or first current-envelope row.",
        ),
        (
            "SRC2098_01_1960_LC_no_hyper",
            SRC_1960,
            ["LC1960_0_target", "LC1960_6_verdict", "P4C1960_5_hypermomentum"],
            "1960 keeps the Levi-Civita/no-hypermomentum route exact but unsigned.",
        ),
        (
            "SRC2098_02_1831_inventory",
            SRC_1831,
            ["PARENT_FIELD_INVENTORY_CERTIFICATE_NOT_PROVEN", "FIRST_P4_NUMERIC_ROW_NOT_FILLED", "VAL1831_OVERALL"],
            "1831 already tried the field-inventory certificate and found the first P4 row template-only.",
        ),
        (
            "SRC2098_03_1832_TQ",
            SRC_1832,
            ["TQ1832_6_verdict", "COEF1832_0_c_T", "DEC1832_2_best_next", "VAL1832_OVERALL"],
            "1832 reduces the connection gap to a distortion/torsion-nonmetricity equation or coefficient row.",
        ),
        (
            "SRC2098_04_1833_hypermomentum",
            CSV_1833_HYP,
            ["HYP1833_0_Delta_Gamma_total", "SOURCE_ROW_STAGED_NONCLAIM", "MISSING_DELTA_GAMMA_TO_PPN_WEP_CLOCK_MAP"],
            "1833 stages Delta_Gamma_total as the first concrete hypermomentum/source/readout current row.",
        ),
        (
            "SRC2098_05_1834_DeltaGamma_bound",
            CSV_1834_DG,
            ["DGB1834_0_total", "BOUND_ROW_STAGED_NONCLAIM", "MISSING_DELTAGAMMA_TO_P4_WEP_PPN_CLOCK_MAP"],
            "1834 splits Delta_Gamma into bound components but keeps values, units and maps missing.",
        ),
        (
            "SRC2098_06_1834_decision",
            CSV_1834_DEC,
            ["NO_HYPERMOMENTUM_THEOREM_NOT_PROVEN", "DELTAGAMMA_COMPONENT_MAP_NEXT"],
            "1834 explicitly says the next useful step is the Delta_Gamma component-to-observable map.",
        ),
        (
            "SRC2098_07_1830_P4_contract",
            CSV_1830_P4,
            ["P4F1830_0_combined_TQ", "P4F1830_5_hypermomentum", "P4_ROW_FILL_CONTRACT_READY_NONCLAIM"],
            "1830 provides the P4 row-fill contract for torsion/nonmetricity and hypermomentum.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2098_field_inventory_to_DeltaGamma_bridge",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2098=use,
                valid_for_claim=False,
            )
        )
    return rows


def field_inventory_refresh_rows() -> list[dict[str, object]]:
    return [
        row(
            refresh_id="FIR2098_0_target",
            clause="parent field-inventory certificate",
            status="TARGET_ALREADY_TESTED_NOT_SIGNED",
            statement="To close Levi-Civita/current-owner source silence, MTS must prove the parent configuration has no independent Gamma/C/hypermomentum slot.",
            evidence="1960, 1831, 1832, 1833 and 1834 all keep this exact route unsigned.",
            consequence="do not spend another broad pass re-auditing the same certificate unless new parent-action text is supplied",
            valid_for_claim=False,
        ),
        row(
            refresh_id="FIR2098_1_metric_only_conditional",
            clause="metric/coframe-only lemma",
            status="EXACT_CONDITIONAL_ONLY",
            statement="If all geometry is e_obs/g_obs and omega[e_obs], torsion/nonmetricity vanish kinematically.",
            evidence="1829/1831/1960 conditional route",
            consequence="clean derivation path, but premise is not current evidence",
            valid_for_claim=False,
        ),
        row(
            refresh_id="FIR2098_2_failed_parent_certificate",
            clause="no independent connection/hypermomentum",
            status="NOT_PARENT_SIGNED_CURRENT_CORPUS",
            statement="Candidate visible-geometry language exists, but no parent field-inventory theorem excludes C^lambda_{mu nu}, projective residue or hypermomentum.",
            evidence="1831 certificate result and 1834 no-hypermomentum theorem result",
            consequence="retain Delta_Gamma_total as a finite current-envelope object",
            valid_for_claim=False,
        ),
        row(
            refresh_id="FIR2098_3_no_broad_circling_rule",
            clause="progress discipline",
            status="ACTIVE_DECISION_RULE",
            statement="After 2097/1831/1834, the next useful step is not another broad source audit; it is one row becoming theorem-zero or numerically bounded.",
            evidence="2097 DEC2097_2 and 1834 DEC1834_2",
            consequence="select Delta_Gamma component-to-observable map next",
            valid_for_claim=False,
        ),
    ]


def delta_gamma_envelope_rows() -> list[dict[str, object]]:
    return [
        row(
            envelope_id="DGE2098_0_total",
            selected_first_row=True,
            quantity="Delta_Gamma_total",
            definition="delta(S_matter + S_source + S_readout)/delta Gamma in the retained independent-connection branch",
            envelope_formula="||Delta_Gamma_total|| <= ||Delta_spin|| + ||Delta_source_readout|| + ||Delta_projective|| + ||Delta_boundary||",
            current_source_path=str(CSV_1833_HYP),
            bound_source_path=str(CSV_1834_DG),
            source_exists=CSV_1833_HYP.exists() and CSV_1834_DG.exists(),
            numeric_value="MISSING_COMPONENT_VALUES",
            units="MISSING_COMMON_DUAL_CONNECTION_UNITS",
            normalization="MISSING_CONNECTION_VARIATION_NORMALIZATION",
            observable_map="MISSING_DELTAGAMMA_TO_P4_WEP_PPN_CLOCK_MAP",
            status="FIRST_CURRENT_ENVELOPE_ROW_SELECTED_NONCLAIM",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="DGE2098_1_spin",
            selected_first_row=False,
            quantity="Delta_spin",
            definition="spinor/tetrad matter connection charge beyond omega[e_obs]",
            envelope_formula="||Delta_spin|| in same dual connection norm as Delta_Gamma_total",
            current_source_path=str(CSV_1833_HYP),
            bound_source_path=str(CSV_1834_DG),
            source_exists=CSV_1833_HYP.exists() and CSV_1834_DG.exists(),
            numeric_value="MISSING_SPIN_BOUND",
            units="MISSING_SPIN_CURRENT_UNITS",
            normalization="MISSING_SPIN_CONNECTION_NORMALIZATION",
            observable_map="MISSING_SPIN_TO_CLOCK_LIGHTCONE_MAP",
            status="COMPONENT_ROW_STAGED_NONCLAIM",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="DGE2098_2_source_readout",
            selected_first_row=False,
            quantity="Delta_source_readout",
            definition="source support plus readout connection-current norm",
            envelope_formula="||Delta_source|| + ||Delta_readout|| in same dual connection norm",
            current_source_path=str(CSV_1833_HYP),
            bound_source_path=str(CSV_1834_DG),
            source_exists=CSV_1833_HYP.exists() and CSV_1834_DG.exists(),
            numeric_value="MISSING_SOURCE_READOUT_BOUND",
            units="MISSING_SOURCE_READOUT_UNITS",
            normalization="MISSING_SOURCE_BRANCH_NORMALIZATION",
            observable_map="MISSING_R10_PPN_ORBITAL_MAP",
            status="COMPONENT_ROW_STAGED_NONCLAIM",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            envelope_id="DGE2098_3_projective_boundary",
            selected_first_row=False,
            quantity="Delta_projective_boundary",
            definition="projective trace and boundary/improvement connection-current leakage",
            envelope_formula="||Delta_projective|| + ||Delta_boundary|| after quotient/readout projection",
            current_source_path=str(CSV_1833_HYP),
            bound_source_path=str(CSV_1834_DG),
            source_exists=CSV_1833_HYP.exists() and CSV_1834_DG.exists(),
            numeric_value="MISSING_PROJECTIVE_BOUNDARY_BOUND",
            units="MISSING_PROJECTIVE_BOUNDARY_UNITS",
            normalization="MISSING_PROJECTIVE_BOUNDARY_NORMALIZATION",
            observable_map="MISSING_PROJECTIVE_BOUNDARY_TO_PPN_MAP",
            status="COMPONENT_ROW_STAGED_NONCLAIM",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        ),
    ]


def component_observable_rows() -> list[dict[str, object]]:
    return [
        row(
            map_id="COM2098_0_P4_operator",
            component="Delta_Gamma_total",
            observable_channel="P4 torsion/nonmetricity residual vector",
            required_map="C = M_C^{-1}(Delta_Gamma + B_boundary + Pi_projective) and irreducible T/Q split",
            missing_input="MISSING_M_C_INVERSE;MISSING_TQ_IRREP_MAP;MISSING_UNITS",
            next_test_use="feeds WEP, PPN, clock, lightcone and orbital residuals",
            map_ready=False,
            valid_for_claim=False,
        ),
        row(
            map_id="COM2098_1_PPN",
            component="Delta_source_readout",
            observable_channel="PPN gamma/beta/preferred-frame source residual",
            required_map="weak-field Green operator from connection current to metric/readout potentials",
            missing_input="MISSING_WEAK_FIELD_CONNECTION_GREEN;MISSING_SOURCE_NORMALIZATION",
            next_test_use="Cassini/PPN gate only after no-cancellation and q_R/Z_R rows are compatible",
            map_ready=False,
            valid_for_claim=False,
        ),
        row(
            map_id="COM2098_2_clock_light",
            component="Delta_spin",
            observable_channel="clock/lightcone/spin transport residual",
            required_map="spin/torsion/nonmetricity transport equation in observed frame",
            missing_input="MISSING_SPIN_TRANSPORT_RULE;MISSING_CLOCK_LIGHTCONE_READOUT",
            next_test_use="clock/light tests and spin-coupling sanity checks",
            map_ready=False,
            valid_for_claim=False,
        ),
        row(
            map_id="COM2098_3_R10_orbital",
            component="Delta_projective_boundary",
            observable_channel="R10/orbital/source-worldtube residual",
            required_map="projective and boundary terms through local exterior projection",
            missing_input="MISSING_PROJECTIVE_GAUGE_FIX;MISSING_BOUNDARY_FALLOFF;MISSING_ORBITAL_PROJECTION",
            next_test_use="short-range and orbital residual bounds once source-normalized",
            map_ready=False,
            valid_for_claim=False,
        ),
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2098_0_field_inventory", "parent excludes independent connection/hypermomentum", "FAIL_ALREADY_TESTED_UNSIGNED", "1831/1834 leave field inventory and no-hypermomentum unsigned"),
        ("GATE2098_1_DeltaGamma_zero", "Delta_Gamma_total is theorem-zero", "FAIL_BLOCKED", "no matter/source/readout Gamma-current zero theorem"),
        ("GATE2098_2_DeltaGamma_bound", "Delta_Gamma_total has finite scored bound", "FAIL_MISSING_VALUES", "component values, units, normalization and observable maps missing"),
        ("GATE2098_3_component_map", "Delta_Gamma components map to observables", "FAIL_MISSING_MAP", "P4/WEP/PPN/clock/orbital maps not built"),
        ("GATE2098_4_local_GR", "local GR/Newton source-current branch is derived", "FAIL_BLOCKED", "Levi-Civita, no-hypermomentum and current-owner gates remain unsigned"),
    ]
    return [
        row(gate_id=gate_id, claim=claim, status=status, reason=reason, valid_for_claim=False)
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2098_0_certificate_refresh",
            decision="FIELD_INVENTORY_CERTIFICATE_STILL_UNSIGNED_DO_NOT_RECIRCLE",
            basis="2097 asked for a refresh, but 1831 and 1834 already tested the same route and did not close it.",
            consequence="carry the exact conditional theorem as a target, not evidence.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2098_1_first_row",
            decision="DELTAGAMMA_TOTAL_SELECTED_AS_FIRST_CURRENT_ENVELOPE_ROW",
            basis="1833/1834 stage Delta_Gamma_total and split its components; this is the first concrete source-side object rather than another broad audit.",
            consequence="next progress means theorem-zero or bound/map for Delta_Gamma components.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2098_2_best_next",
            decision="DELTAGAMMA_COMPONENT_TO_OBSERVABLE_MAP_NEXT",
            basis="No numeric score can happen until each retained component maps to P4/WEP/PPN/clock/orbital residuals in one normalization.",
            consequence="2099 should build the component map and keep all rows nonclaim until values/units/maps exist.",
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2098_0_2099",
            target_doc="2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md",
            target_script="scripts/Y5_R2FR_DeltaGamma_component_map_to_P4_WEP_PPN_clock_orbital_residuals_2099.py",
            objective="build the first explicit component-to-observable map for Delta_Gamma_total: spin, source/readout, projective and boundary terms into P4/WEP/PPN/clock/orbital residual channels",
            success_condition="each retained component has a declared normalization, units target, projection operator, observable channel and missing-input ledger; no score or local-GR claim unless theorem-zero or sourced numeric values exist",
            forbidden_shortcuts="another broad field-inventory audit; WEP-only silence; GR import; cancellation between Delta_Gamma components; source-free coefficients; GitHub; formalization-workbench edits",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    refresh: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    maps: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_DELTAGAMMA_CURRENT_ENVELOPE_2098_NONCLAIM.csv",
            refresh + envelopes + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2098_DELTAGAMMA_GATE_NONCLAIM.csv",
            envelopes + maps,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2098_DELTAGAMMA_COMPONENT_MAP_NEXT_QUEUE.csv",
            maps + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2098_{len(rows)}",
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
    refresh: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    maps: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    no_recircle_ok = any(
        r["refresh_id"] == "FIR2098_3_no_broad_circling_rule" and r["status"] == "ACTIVE_DECISION_RULE"
        for r in refresh
    )
    first_row_ok = any(
        r["envelope_id"] == "DGE2098_0_total"
        and truthy(r["selected_first_row"])
        and r["status"] == "FIRST_CURRENT_ENVELOPE_ROW_SELECTED_NONCLAIM"
        for r in envelopes
    )
    envelopes_blocked = all(not truthy(r["source_backed"]) and not truthy(r["score_ready"]) for r in envelopes)
    maps_blocked = all(not truthy(r["map_ready"]) for r in maps)
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and all(str(r["status"]).startswith("FAIL") for r in gates)
    decision_ok = any(r["decision_id"] == "DEC2098_2_best_next" and r["decision"] == "DELTAGAMMA_COMPONENT_TO_OBSERVABLE_MAP_NEXT" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2098_0_2099"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, refresh, envelopes, maps, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2098_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2098_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2098_01_no_recircle", no_recircle_ok, "field-inventory refresh avoids broad recircling"),
        ("VAL2098_02_first_row", first_row_ok, "Delta_Gamma_total selected as first current-envelope row"),
        ("VAL2098_03_envelopes_blocked", envelopes_blocked, "Delta_Gamma envelope rows remain non-source-backed and not score-ready"),
        ("VAL2098_04_maps_blocked", maps_blocked, "component-to-observable maps are explicit but missing"),
        ("VAL2098_05_claim_gates", gates_safe, "claim gates block local-GR/PPN/R10 promotion"),
        ("VAL2098_06_decision", decision_ok, "decision selects Delta_Gamma component-to-observable map next"),
        ("VAL2098_07_next", next_ok, "next target is 2099 Delta_Gamma component map"),
        ("VAL2098_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2098_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2098_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2098_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2098"),
        ("VAL2098_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2098_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2098 stops the field-inventory recircle, selects Delta_Gamma_total as the first current-envelope object, and routes next to component-to-observable mapping" if overall else "one or more 2098 validation gates failed",
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    refresh: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    maps: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2098 - Y5/R2FR Parent Field-Inventory Certificate Refresh Or First Source-Current Envelope Row",
            "## Current Verdict\n\n2098 is the point where we stop circling the same gate. The field-inventory/no-hypermomentum certificate remains the clean route to Levi-Civita and local GR, but 1831 and 1834 already tested it and did not close it. Without new parent-action text, another broad certificate pass would be theater.\n\nSo the branch moves to the first concrete current-envelope object: `Delta_Gamma_total = delta(S_matter + S_source + S_readout)/delta Gamma`. This is still nonclaim. It has no numeric value, no common units, no connection-variation normalization, and no P4/WEP/PPN/clock/orbital map. But it is the right object. The next derivable move is to map its components, not to say local GR loudly.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2098", "claim_allowed", "valid_for_claim"]),
            "## Field-Inventory Refresh",
            md_table(refresh, ["refresh_id", "clause", "status", "statement", "evidence", "consequence", "claim_allowed", "valid_for_claim"]),
            "## Delta_Gamma Current Envelope",
            md_table(envelopes, ["envelope_id", "selected_first_row", "quantity", "definition", "envelope_formula", "numeric_value", "units", "normalization", "observable_map", "status", "source_backed", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## Component-To-Observable Requirements",
            md_table(maps, ["map_id", "component", "observable_channel", "required_map", "missing_input", "next_test_use", "map_ready", "claim_allowed", "valid_for_claim"]),
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
    refresh = field_inventory_refresh_rows()
    envelopes = delta_gamma_envelope_rows()
    maps = component_observable_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2098_SOURCE_REGISTER.csv",
        "refresh": OUT / "P8_Y5_PARENT_QLOC_2098_FIELD_INVENTORY_REFRESH.csv",
        "envelopes": OUT / "P8_Y5_PARENT_QLOC_2098_DELTAGAMMA_ENVELOPE_BRIDGE.csv",
        "maps": OUT / "P8_Y5_PARENT_QLOC_2098_COMPONENT_TO_OBSERVABLE_REQUIREMENTS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2098_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2098_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2098_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2098_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2098_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["refresh"], refresh)
    write_csv(paths["envelopes"], envelopes)
    write_csv(paths["maps"], maps)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(refresh, envelopes, maps, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, refresh, envelopes, maps, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, refresh, envelopes, maps, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
