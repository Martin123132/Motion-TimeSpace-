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


DOC = ROOT / "2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2098 = ROOT / "2098-Y5-R2FR-parent-field-inventory-certificate-refresh-or-first-source-current-envelope-row.md"
SRC_1835 = ROOT / "1835-Y5-R2FR-DeltaGamma-component-map-to-P4-observables.md"
SRC_1836 = ROOT / "1836-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton.md"
CSV_1834_BASIS = OUT / "P8_Y5_PARENT_QLOC_1834_DELTAGAMMA_COMPONENT_BASIS.csv"
CSV_1835_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_1835_DELTAGAMMA_COMPONENT_OBSERVABLE_MAP.csv"
CSV_1835_ARENAS = OUT / "P8_Y5_PARENT_QLOC_1835_ARENA_PROJECTION_REQUIREMENTS.csv"
CSV_1835_BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_1835_SCORE_BLOCKER_LEDGER.csv"
CSV_1836_PROJECTIONS = OUT / "P8_Y5_PARENT_QLOC_1836_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON.csv"
CSV_1836_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1836_RESPONSE_OPERATOR_REQUIREMENTS.csv"
CSV_1836_DECISIONS = OUT / "P8_Y5_PARENT_QLOC_1836_DECISION_LEDGER.csv"
P4_TEMPLATE = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results" / "P4_R11_template_rows.csv"
P4_DEMOTIONS = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results" / "connection_operator_demotions.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2099_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2099-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2099*",
        "*Y5_R2FR_DeltaGamma_component_map_to_P4_WEP_PPN_clock_orbital_residuals_2099*",
        "*AFRAME_DELTAGAMMA_OBSERVABLE_MAP_2099*",
        "*JR2099_PWEP_RESPONSE_OPERATOR*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2099_00_2098_handoff",
            SRC_2098,
            ["NEXT2098_0_2099", "DELTAGAMMA_COMPONENT_TO_OBSERVABLE_MAP_NEXT", "VAL2098_OVERALL"],
            "2098 selects Delta_Gamma component-to-observable mapping as the next nonclaim step.",
        ),
        (
            "SRC2099_01_1835_map_doc",
            SRC_1835,
            ["DGOM1835_0_spin", "ARENA1835_1_WEP", "VAL1835_OVERALL"],
            "1835 provides the seven-component Delta_Gamma observable map.",
        ),
        (
            "SRC2099_02_1835_components_csv",
            CSV_1835_COMPONENTS,
            ["DGOM1835_0_spin", "DGOM1835_6_projective", "MAP_SKELETON_ONLY_MISSING_PROJECTION"],
            "machine-readable seven-component map to observable channels.",
        ),
        (
            "SRC2099_03_1835_arenas_csv",
            CSV_1835_ARENAS,
            ["ARENA1835_0_R10", "ARENA1835_5_ORBITAL", "MISSING_WEP_PROJECTION_MATRIX"],
            "arena projection requirements across R10/WEP/PPN/clock/lightcone/orbital.",
        ),
        (
            "SRC2099_04_1836_projection_doc",
            SRC_1836,
            ["P1836_WEP_0_eta_total", "DEC1836_2_best_next", "VAL1836_OVERALL"],
            "1836 advances the map into the first WEP/clock/lightcone projection skeleton.",
        ),
        (
            "SRC2099_05_1836_projection_csv",
            CSV_1836_PROJECTIONS,
            ["P1836_WEP_0_eta_total", "P1836_GUARD_0_cross_arena", "NO_LOCAL_GR_PROMOTION"],
            "machine-readable WEP/clock/lightcone projection skeleton.",
        ),
        (
            "SRC2099_06_1836_response_requirements",
            CSV_1836_REQUIREMENTS,
            ["ROR1836_1_P_WEP", "ROR1836_2_P_clock", "ROR1836_3_P_lightcone"],
            "response-operator requirements for the first local projection block.",
        ),
        (
            "SRC2099_07_1836_decisions",
            CSV_1836_DECISIONS,
            ["P_WEP_FROM_MATTER_FUNCTOR_NEXT", "RESPONSE_OPERATORS_NOT_DERIVED"],
            "1836 selects P_WEP from matter functor as the first response operator to derive.",
        ),
        (
            "SRC2099_08_1834_component_basis",
            CSV_1834_BASIS,
            ["DGC1834_0_spin", "DGC1834_6_projective", "MISSING_ZERO_OR_BOUND"],
            "component basis for retained Delta_Gamma currents.",
        ),
        (
            "SRC2099_09_P4_template",
            P4_TEMPLATE,
            ["independent_connection_hypermomentum", "fill_WEP_source_clock_spin_map"],
            "P4/R11 template anchors torsion/nonmetricity and hypermomentum observable vocabulary.",
        ),
        (
            "SRC2099_10_P4_demotions",
            P4_DEMOTIONS,
            ["torsion_nonmetricity_combined", "fill hypermomentum/source-charge row"],
            "P4 demotion ledger prevents silently deleting connection-current branches.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2099_DeltaGamma_component_observable_map",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2099=use,
                valid_for_claim=False,
            )
        )
    return rows


def component_map_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DGM2099_0_spin",
            "spin_hypermomentum",
            "axial_torsion_spin_coupling",
            "spin_torsion_residual;clock_residual;lightcone_residual;eta_WEP;operator_ledger",
            "P_spin_to_axial_torsion;P_spin_to_clock;P_spin_to_lightcone;P_spin_to_WEP",
            "spin current norm; spin connection normalization; species/spin basis; source path",
            "dual-connection spin-current units or normalized torsion response",
            "WEP_CLOCK_LIGHTCONE_PRIMARY",
        ),
        (
            "DGM2099_1_material",
            "material_marker_connection_current",
            "species_source_charge",
            "eta_source_AB;eta_WEP;clock_redshift;operator_ledger",
            "P_material_to_composition;P_material_to_clock;P_material_to_source_charge",
            "material tensor; marker derivative; same-frame source basis; no hidden species theorem or bound",
            "dimensionless material/source charge after projection; input current units missing",
            "WEP_CLOCK_PRIMARY",
        ),
        (
            "DGM2099_2_source_support",
            "source_support_connection_current",
            "source_normalization_operator",
            "source_charge_residual;alpha(lambda);gamma_minus_1;beta_minus_1;orbital_GM;operator_ledger",
            "P_source_support_to_GM;P_source_support_to_R10;P_source_support_to_PPN",
            "worldtube support; source current norm; radial profile; range scale; GM transfer convention",
            "source-current density or normalized source-charge residual",
            "R10_PPN_ORBITAL_SECONDARY",
        ),
        (
            "DGM2099_3_clock_rods",
            "clock_rod_nonmetric_connection_current",
            "nonmetricity_weyl_trace",
            "clock_residual;rod_residual;redshift_fractional_deviation;eta_WEP;operator_ledger",
            "P_nonmetricity_to_clock;P_nonmetricity_to_rods;P_clock_to_WEP",
            "clock functional; rod calibration functional; Q_trace normalization; redshift bound source",
            "inverse length or normalized Weyl-nonmetricity response",
            "WEP_CLOCK_PRIMARY",
        ),
        (
            "DGM2099_4_photon_lightcone",
            "photon_lightcone_connection_current",
            "nonmetricity_shear_lightcone",
            "lightcone_residual;gamma_minus_1;clock_residual;eta_WEP;operator_ledger",
            "P_shearQ_to_lightcone;P_lightcone_to_gamma;P_lightcone_to_clock",
            "lightcone response operator; trace-free Q normalization; gauge choice; photon/readout branch",
            "inverse length or normalized shear-nonmetricity response",
            "LIGHTCONE_PPN_PRIMARY",
        ),
        (
            "DGM2099_5_orbital_readout",
            "orbital_readout_connection_current",
            "source_readout_connection_current",
            "orbital_GM;Gdot_over_G;alpha(lambda);beta_minus_1;gamma_minus_1;operator_ledger",
            "P_orbital_readout_to_GM;P_orbital_readout_to_Gdot;P_orbital_readout_to_fifth_force",
            "test-body readout action; inverse-square split; time/range law; no fitted-G absorption guard",
            "normalized orbital/source-readout current",
            "R10_PPN_ORBITAL_SECONDARY",
        ),
        (
            "DGM2099_6_projective",
            "projective_trace_current",
            "torsion_trace_projective_mode",
            "eta_WEP;source_charge_residual;clock_residual;projective_invariance_certificate;operator_ledger",
            "P_projective_to_source;P_projective_to_clock;P_projective_invariance_all_sectors",
            "projective gauge rule; all-sector invariance proof; source/readout trace coupling bound",
            "projective trace normalization or all-sector gauge-invariant zero",
            "COMMON_GUARD_PRIMARY",
        ),
    ]
    return [
        row(
            map_id=map_id,
            DeltaGamma_component=component,
            connection_channel=channel,
            primary_observables=observables,
            projection_required=projection,
            needed_inputs=inputs,
            unit_normalization_target=unit_target,
            priority_bucket=priority,
            current_status="MAP_REGISTERED_PROJECTION_MISSING",
            source_backed=False,
            map_ready=False,
            score_ready=False,
            valid_for_claim=False,
        )
        for map_id, component, channel, observables, projection, inputs, unit_target, priority in specs
    ]


def arena_projection_rows() -> list[dict[str, object]]:
    specs = [
        (
            "APM2099_0_R10",
            "R10_short_range_inverse_square",
            "alpha(lambda)",
            "source_support_connection_current;orbital_readout_connection_current",
            "P_DeltaGamma_to_alpha_lambda",
            "source geometry, range/profile convention, torque/readout projection, full bound curve",
            "SECONDARY_AFTER_LOCAL_COUPLING_BLOCK",
        ),
        (
            "APM2099_1_WEP",
            "WEP_MICROSCOPE",
            "eta_AB",
            "spin_hypermomentum;material_marker_connection_current;clock_rod_nonmetric_connection_current;projective_trace_current",
            "P_WEP_eta_AB",
            "composition tensor, material/source basis, no measured-G absorption, common DeltaGamma units",
            "PRIMARY_FIRST_RESPONSE_OPERATOR",
        ),
        (
            "APM2099_2_PPN",
            "PPN",
            "gamma_minus_1;beta_minus_1;alpha1;alpha2;alpha3;xi",
            "source_support_connection_current;photon_lightcone_connection_current;orbital_readout_connection_current",
            "P_DeltaGamma_to_metric_PPN",
            "weak-field Green operator, gauge, trace reversal, source-normalization split",
            "SECONDARY_AFTER_WEP_LIGHTCONE",
        ),
        (
            "APM2099_3_CLOCK",
            "clock_redshift",
            "redshift_fractional_deviation;clock_residual",
            "clock_rod_nonmetric_connection_current;spin_hypermomentum;material_marker_connection_current;projective_trace_current",
            "P_clock",
            "clock species functional, rod calibration, coframe lock, Q_trace normalization",
            "PRIMARY_AFTER_PWEP",
        ),
        (
            "APM2099_4_LIGHTCONE",
            "lightcone_photon",
            "lightcone_residual;gamma_minus_1",
            "photon_lightcone_connection_current;clock_rod_nonmetric_connection_current;spin_hypermomentum",
            "P_lightcone",
            "photon eikonal branch, gauge rule, trace-free Q normalization, metric-lightcone theorem or bound",
            "PRIMARY_AFTER_PWEP",
        ),
        (
            "APM2099_5_ORBITAL",
            "orbital_Newton_source_normalization",
            "orbital_GM;Gdot_over_G;anomalous_radial_acceleration",
            "orbital_readout_connection_current;source_support_connection_current;projective_trace_current",
            "P_DeltaGamma_to_orbital_readout",
            "inverse-square split, no fitted-G shortcut, time/range law, source-worldtube projection",
            "SECONDARY_AFTER_SOURCE_NORMALIZATION",
        ),
    ]
    return [
        row(
            arena_projection_id=arena_id,
            arena=arena,
            observable=observable,
            DeltaGamma_components=components,
            projection_matrix=projection,
            missing_inputs=missing,
            priority=priority,
            projection_status="MISSING_PROJECTION_MATRIX",
            source_backed=False,
            map_ready=False,
            score_ready=False,
            valid_for_claim=False,
        )
        for arena_id, arena, observable, components, projection, missing, priority in specs
    ]


def local_projection_block_rows() -> list[dict[str, object]]:
    return [
        row(
            block_id="LPB2099_0_WEP_total",
            projection="eta_AB = P_WEP_eta_AB · DeltaGamma_WEP",
            input_components="spin_hypermomentum;material_marker_connection_current;clock_rod_nonmetric_connection_current;projective_trace_current",
            output="eta_AB dimensionless differential acceleration",
            status="P_WEP_MISSING",
            missing_for_derivation="parent matter functor; material/source basis; component units; no measured-G absorption guard",
            selected_first=True,
            valid_for_claim=False,
        ),
        row(
            block_id="LPB2099_1_clock_total",
            projection="delta_nu_over_nu = P_clock · DeltaGamma_clock",
            input_components="clock_rod_nonmetric_connection_current;spin_hypermomentum;material_marker_connection_current;projective_trace_current",
            output="fractional clock/redshift residual",
            status="P_CLOCK_MISSING",
            missing_for_derivation="clock functional; rod calibration; Q_trace normalization; clock bound source",
            selected_first=False,
            valid_for_claim=False,
        ),
        row(
            block_id="LPB2099_2_lightcone_total",
            projection="delta_null = P_lightcone · DeltaGamma_light",
            input_components="photon_lightcone_connection_current;clock_rod_nonmetric_connection_current;spin_hypermomentum",
            output="lightcone residual and PPN gamma leakage",
            status="P_LIGHTCONE_MISSING",
            missing_for_derivation="photon branch; gauge rule; Q_shear normalization; metric-lightcone theorem or bound",
            selected_first=False,
            valid_for_claim=False,
        ),
        row(
            block_id="LPB2099_3_common_guard",
            projection="R_local = (P_WEP, P_clock, P_lightcone, P_projective) · DeltaGamma_local",
            input_components="all local DeltaGamma components in common units",
            output="combined local residual vector",
            status="LOCAL_GR_PROMOTION_FORBIDDEN",
            missing_for_derivation="common units; component values or zero theorems; no-cancellation identity",
            selected_first=False,
            valid_for_claim=False,
        ),
    ]


def score_blocker_rows() -> list[dict[str, object]]:
    blockers = [
        ("SBL2099_0_component_values", "all arenas", "component numeric values or parent zero certificates", "BLOCKS_SCORE"),
        ("SBL2099_1_common_units", "DeltaGamma total norm", "common dual-connection units and normalization across components", "BLOCKS_SCORE"),
        ("SBL2099_2_projection_matrices", "observable maps", "P_R10, P_WEP, P_PPN, P_clock, P_lightcone, P_orbital", "BLOCKS_SCORE"),
        ("SBL2099_3_response_operators", "WEP/clock/lightcone primary block", "P_WEP, P_clock, P_lightcone and P_projective_all", "BLOCKS_SCORE"),
        ("SBL2099_4_no_cancellation", "combined local residual pass", "individual component pass or parent cancellation identity", "GUARD_ACTIVE"),
    ]
    return [
        row(blocker_id=blocker_id, blocks=blocks, missing=missing, status=status, valid_for_claim=False)
        for blocker_id, blocks, missing, status in blockers
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2099_0_component_map", "all DeltaGamma components are mapped", "PASS_NONCLAIM_MAP_ONLY", "map exists but no projection matrices or values are sourced"),
        ("GATE2099_1_WEP", "WEP can be scored", "FAIL_MISSING_PWEP", "P_WEP, component values, units and material/source basis are missing"),
        ("GATE2099_2_clock", "clock/redshift can be scored", "FAIL_MISSING_PCLOCK", "clock functional, rod calibration and Q_trace normalization are missing"),
        ("GATE2099_3_lightcone_PPN_gamma", "lightcone/PPN gamma can be scored", "FAIL_MISSING_PLIGHTCONE", "photon branch, gauge and Q_shear normalization are missing"),
        ("GATE2099_4_R10_PPN_orbital", "R10/PPN/orbital can be scored", "FAIL_SECONDARY_PROJECTIONS_MISSING", "source/orbital/PPN response operators and theory-side values are missing"),
        ("GATE2099_5_local_GR", "local GR/Newton recovery is derived", "FAIL_BLOCKED", "component values/zeroes, projection matrices and no-cancellation guard are not closed"),
    ]
    return [
        row(gate_id=gate_id, claim=claim, status=status, reason=reason, valid_for_claim=False)
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2099_0_map_status",
            decision="DELTAGAMMA_COMPONENT_MAP_CONSOLIDATED_NONCLAIM",
            basis="2098, 1835 and 1836 now agree on the component vector and its observable channels.",
            consequence="Delta_Gamma is test-facing, but no arena is score-ready.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2099_1_primary_gap",
            decision="RESPONSE_OPERATORS_AND_PROJECTION_MATRICES_MISSING",
            basis="P_WEP, P_clock, P_lightcone, P_R10, P_PPN and P_orbital remain unsourced.",
            consequence="no WEP/clock/lightcone/R10/PPN/orbital scoring or local-GR promotion.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2099_2_best_next",
            decision="P_WEP_FROM_MATTER_FUNCTOR_NEXT",
            basis="WEP is the harshest local-coupling test and shares the same matter-functor machinery needed by clocks and source charge.",
            consequence="2100 should try to derive P_WEP; if it fails, stage nonclaim eta_AB component-bound rows.",
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2099_0_2100",
            target_doc="2100-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md",
            target_script="scripts/Y5_R2FR_PWEP_response_operator_from_matter_functor_or_component_bound_row_2100.py",
            objective="derive P_WEP from the parent matter functor and same-frame source/readout basis, or stage eta_AB component-bound rows for spin/material/clock/projective DeltaGamma components",
            success_condition="P_WEP has signed parent assumptions and units, or WEP remains blocked with explicit component-bound inputs; no WEP/local-GR claim from placeholders",
            forbidden_shortcuts="WEP pass claim; measured-G absorption; cancellation between DeltaGamma components; GR import; source-free coefficients; GitHub; formalization-workbench edits",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    components: list[dict[str, object]],
    arenas: list[dict[str, object]],
    local_block: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_DELTAGAMMA_OBSERVABLE_MAP_2099_NONCLAIM.csv",
            components + arenas + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2099_WEP_CLOCK_LIGHTCONE_GATE_NONCLAIM.csv",
            local_block + blockers,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2099_PWEP_RESPONSE_OPERATOR_NEXT_QUEUE.csv",
            local_block + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2099_{len(rows)}",
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
    components: list[dict[str, object]],
    arenas: list[dict[str, object]],
    local_block: list[dict[str, object]],
    blockers: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    component_ok = len(components) == 7 and all(r["current_status"] == "MAP_REGISTERED_PROJECTION_MISSING" for r in components)
    arena_ok = len(arenas) == 6 and all(r["projection_status"] == "MISSING_PROJECTION_MATRIX" for r in arenas)
    local_block_ok = any(r["block_id"] == "LPB2099_0_WEP_total" and truthy(r["selected_first"]) for r in local_block)
    blockers_ok = len(blockers) >= 5 and any(r["blocker_id"] == "SBL2099_4_no_cancellation" for r in blockers)
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and all(
        str(r["status"]).startswith("FAIL") or r["status"] == "PASS_NONCLAIM_MAP_ONLY" for r in gates
    )
    decision_ok = any(r["decision_id"] == "DEC2099_2_best_next" and r["decision"] == "P_WEP_FROM_MATTER_FUNCTOR_NEXT" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2099_0_2100"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, components, arenas, local_block, blockers, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2099_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2099_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2099_01_components", component_ok, "seven DeltaGamma component map rows are registered and nonclaim"),
        ("VAL2099_02_arenas", arena_ok, "six arena projection matrix rows are registered and missing"),
        ("VAL2099_03_local_block", local_block_ok, "WEP/clock/lightcone block selects P_WEP first"),
        ("VAL2099_04_blockers", blockers_ok, "score blockers and no-cancellation guard are active"),
        ("VAL2099_05_claim_gates", gates_safe, "claim gates block all scoring/local-GR promotion"),
        ("VAL2099_06_decision", decision_ok, "decision selects P_WEP from matter functor next"),
        ("VAL2099_07_next", next_ok, "next target is 2100 P_WEP response operator"),
        ("VAL2099_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2099_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2099_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2099_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2099"),
        ("VAL2099_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2099_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2099 consolidates the Delta_Gamma observable map, keeps all arenas nonclaim, and selects P_WEP from matter functor as the next derivation target" if overall else "one or more 2099 validation gates failed",
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    components: list[dict[str, object]],
    arenas: list[dict[str, object]],
    local_block: list[dict[str, object]],
    blockers: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2099 - Y5/R2FR DeltaGamma Component Map To P4 WEP PPN Clock Orbital Residuals",
            "## Current Verdict\n\n2099 makes the coupling problem test-facing without pretending it is solved. `Delta_Gamma_total` is now a seven-component local current vector with named channels into R10, WEP, PPN, clock, lightcone and orbital observables. This is a serious improvement over a vague coupling gap.\n\nBut nothing is score-ready. The missing objects are response operators and projection matrices, not slogans: `P_WEP`, `P_clock`, `P_lightcone`, `P_R10`, `P_PPN`, and `P_orbital`, all in one common `Delta_Gamma` normalization. The first derivation target is `P_WEP` from the parent matter functor because it is the harshest local-coupling gate and it also teaches the clock/source-charge branches how to behave.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2099", "claim_allowed", "valid_for_claim"]),
            "## DeltaGamma Component Map",
            md_table(components, ["map_id", "DeltaGamma_component", "connection_channel", "primary_observables", "projection_required", "needed_inputs", "unit_normalization_target", "priority_bucket", "current_status", "source_backed", "map_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## Arena Projection Matrix Register",
            md_table(arenas, ["arena_projection_id", "arena", "observable", "DeltaGamma_components", "projection_matrix", "missing_inputs", "priority", "projection_status", "source_backed", "map_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## WEP Clock Lightcone Local Block",
            md_table(local_block, ["block_id", "projection", "input_components", "output", "status", "missing_for_derivation", "selected_first", "claim_allowed", "valid_for_claim"]),
            "## Score Blockers",
            md_table(blockers, ["blocker_id", "blocks", "missing", "status", "claim_allowed", "valid_for_claim"]),
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
    components = component_map_rows()
    arenas = arena_projection_rows()
    local_block = local_projection_block_rows()
    blockers = score_blocker_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2099_SOURCE_REGISTER.csv",
        "components": OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv",
        "arenas": OUT / "P8_Y5_PARENT_QLOC_2099_ARENA_PROJECTION_MATRIX_REGISTER.csv",
        "local_block": OUT / "P8_Y5_PARENT_QLOC_2099_WEP_CLOCK_LIGHTCONE_LOCAL_BLOCK.csv",
        "blockers": OUT / "P8_Y5_PARENT_QLOC_2099_SCORE_BLOCKERS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2099_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2099_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2099_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2099_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2099_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["components"], components)
    write_csv(paths["arenas"], arenas)
    write_csv(paths["local_block"], local_block)
    write_csv(paths["blockers"], blockers)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(components, arenas, local_block, blockers, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, components, arenas, local_block, blockers, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, components, arenas, local_block, blockers, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
