from __future__ import annotations

import csv
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


DOC = ROOT / "2044-Y5-R2FR-sector-Gamma-slot-audit-or-first-numeric-P4-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2044_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        artifact_patterns = (
            "*2044-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2044*",
            "*Y5_R2FR_sector_Gamma_slot_audit_or_first_numeric_P4_source_2044*",
        )
        return any(path.is_file() for pattern in artifact_patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def source_register_rows() -> list[dict[str, object]]:
    local_specs = [
        (
            "SRC2044_00_2043_doc",
            ROOT / "2043-Y5-R2FR-parent-Gamma-slot-owner-or-first-P4-connection-bound-row.md",
            ["NEXT2043_0_2044", "GSO2043_6_verdict", "VAL2043_OVERALL"],
            "2043 handoff: sector Gamma-slot audit or first numeric P4 source.",
        ),
        (
            "SRC2044_01_2043_next",
            OUT / "P8_Y5_PARENT_QLOC_2043_NEXT_TARGET.csv",
            ["NEXT2043_0_2044", "independent Gamma arguments"],
            "machine-readable 2044 target.",
        ),
        (
            "SRC2044_02_2043_p4",
            OUT / "P8_Y5_PARENT_QLOC_2043_FIRST_P4_BOUND_ROWS.csv",
            ["P4B2043_0_hypermomentum", "P4B2043_1_axial_torsion"],
            "first broad/narrow P4 connection fallback rows.",
        ),
        (
            "SRC2044_03_1045_matter_functor",
            ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            ["MFS1045_1_observed_coframe_functor", "QG1045_2_connection_stack", "V1045_SUMMARY"],
            "matter functor descent with connection caveat.",
        ),
        (
            "SRC2044_04_1065_parent_grammar",
            ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
            ["PGG1065_0_parent_language", "PGG1065_4_measure_coframe_descent", "AAG1065_6_nonHilbert_current"],
            "ordinary matter parent-language and non-Hilbert-current caveat.",
        ),
        (
            "SRC2044_05_1309_matter_descent",
            ROOT / "1309-Y5-R10-RAB-matter-descent-constant-marker-theorem-or-qc-residual.md",
            ["QZT1309_1_chain_rule", "MCG1309_0_observed_coframe", "VAL1309_6_csv_parse"],
            "matter descent chain-rule and coframe premise.",
        ),
        (
            "SRC2044_06_1339_left_hand",
            ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
            ["EHGate1339_3_Levi_Civita", "R11V1339_1_torsion_nonmetricity", "VAL1339_12_overall"],
            "left-hand local-GR gate map.",
        ),
        (
            "SRC2044_07_1340_R11_interface",
            ROOT / "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
            ["R11SCHEMA1340_2_connection", "R11RUN1340_2_connection_prediction_required", "VAL1340_11_overall"],
            "strict R11 connection interface.",
        ),
        (
            "SRC2044_08_1778_source_measure",
            ROOT / "1778-Y5-R2FR-adopted-PiM-source-measure-glue-or-RPiH-first-row.md",
            ["ASM1778_4_gauss_downstream", "DHS1778_1_Delta_frame_source", "CG1778_2_Newton_Gauss_orbit"],
            "source/worldtube/orbital readout is downstream and frame-sensitive.",
        ),
        (
            "SRC2044_09_1960_p4",
            OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
            ["P4C1960_1_axial_torsion", "P4C1960_5_hypermomentum"],
            "P4 connection envelope ledger.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in local_specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(path),
                "source_url": "",
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    external_specs = [
        (
            "SRC2044_EXT_00_KRT2008_torsion",
            "https://arxiv.org/abs/0712.4393",
            "https://doi.org/10.1103/PhysRevLett.100.111102",
            "Kostelecky/Russell/Tasson torsion constraints: 19 of 24 torsion components constrained down to order 1e-31 GeV via Lorentz-violation searches.",
        ),
        (
            "SRC2044_EXT_01_Terrano2015_spin",
            "https://arxiv.org/abs/1508.02463",
            "https://doi.org/10.1103/PhysRevLett.115.201801",
            "Terrano/Adelberger/Lee/Heckel short-range electron spin-dependent torsion-pendulum source candidate; useful spin-sector context, not a direct MTS torsion map.",
        ),
    ]
    for source_id, source_url, doi, note in external_specs:
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "external_web_record",
                "source_path": "",
                "source_url": source_url,
                "status": "SOURCE_STRING_RECORDED_NONCLAIM",
                "needles": doi,
                "note": note,
            }
        )
        rows.append(row)
    return rows


def sector_gamma_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "SECG2044_0_matter",
            "ordinary matter",
            "S_matter[Psi_A,e_obs(q),omega_LC[e_obs(q)],A_Q,theta_A]",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "delta S_matter/delta Gamma=0 if no independent Gamma argument",
            "MFS1045/MCG1309 are contracts, not parent action signatures",
            "keep theorem conditional",
        ),
        (
            "SECG2044_1_spin",
            "spinor/spin transport",
            "omega_spin = omega_LC[e_obs] only; no independent contorsion K_{abc}",
            "UNSIGNED_HIGHEST_P4_RISK",
            "would kill axial torsion P4 row",
            "spin/coframe-owned connection guard not parent-signed",
            "choose axial torsion source row as first numeric P4 anchor",
        ),
        (
            "SECG2044_2_source_worldtube",
            "source/worldtube",
            "S_source[W,e_obs,tau_obs] with no Gamma-source or boundary torsion current",
            "UNSIGNED",
            "needed for measured-GM and WEP/source charge",
            "worldtube/source owner and no post-readout support shift remain open",
            "retain hypermomentum/source component",
        ),
        (
            "SECG2044_3_clock_lightcone",
            "clocks, rods and lightcones",
            "readout uses metric proper time and null cones from g_obs only",
            "UNSIGNED",
            "needed for clock, Shapiro and lightcone safety",
            "nonmetricity clock/rod/shear rows remain live",
            "retain Weyl/shear nonmetricity rows",
        ),
        (
            "SECG2044_4_orbital",
            "orbital readout",
            "orbits are downstream functors of source-measure -> Poisson/Gauss -> g_obs, not Gamma readout inputs",
            "UNSIGNED_DOWNSTREAM",
            "needed to avoid using fitted GM to prove the source/connection branch",
            "1778 explicitly keeps orbital/Gauss downstream",
            "retain orbital Gamma component in hypermomentum envelope",
        ),
        (
            "SECG2044_5_boundary_nonHilbert",
            "boundary/non-Hilbert current",
            "boundary torsion/nonmetricity/support currents vanish, are gauge, or become explicit residuals",
            "UNSIGNED",
            "needed for conservation/source equality",
            "non-Hilbert current caveats remain open",
            "retain boundary Gamma component",
        ),
        (
            "SECG2044_6_verdict",
            "all sector Gamma slots",
            "every sector above is parent-signed Gamma-free or bounded as P4",
            "FAIL_CURRENT_CORPUS",
            "would activate 2042 no-hypermomentum and LC route",
            "no sector audit closes enough for a claim",
            "source first axial torsion numeric anchor and keep hypermomentum broad row",
        ),
    ]
    rows = []
    for row_id, sector, action_argument_form, status, if_signed, blocker, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "sector": sector,
                "action_argument_form": action_argument_form,
                "status": status,
                "if_signed": if_signed,
                "blocker": blocker,
                "next_action": next_action,
                "deltaS_deltaGamma_zero_claim_allowed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def sector_delta_rows() -> list[dict[str, object]]:
    data = [
        ("DELTA2044_0_matter", "Delta_matter", "||delta S_matter/delta Gamma||", "MISSING_PARENT_NO_GAMMA_SIGNATURE_OR_COMPONENT_BOUND", "matter;WEP;R10;local_GR"),
        ("DELTA2044_1_spin", "Delta_spin_axial", "||delta S_spin/delta K_axial||", "MISSING_SPIN_CONNECTION_LC_THEOREM_OR_TORSION_BOUND", "spin;clock;WEP;source_charge"),
        ("DELTA2044_2_source", "Delta_source", "||delta S_source/delta Gamma||", "MISSING_SOURCE_WORLDTUBE_GAMMA_OWNER_OR_BOUND", "source_charge;Newton_GM;WEP"),
        ("DELTA2044_3_clock_light", "Delta_clock_light", "||delta S_clock/light/delta Gamma||", "MISSING_CLOCK_LIGHTCONE_NONMETRICITY_MAP_OR_BOUND", "clock;Shapiro;PPN"),
        ("DELTA2044_4_orbit", "Delta_orbit", "||delta S_orbit/readout/delta Gamma||", "MISSING_ORBITAL_READOUT_GAMMA_SILENCE_OR_BOUND", "orbital;PPN;Newton_GM"),
        ("DELTA2044_5_boundary", "Delta_boundary", "||delta S_boundary/nonH/delta Gamma||", "MISSING_BOUNDARY_NONHILBERT_GAMMA_ZERO_OR_BOUND", "conservation;source_charge;local_GR"),
        ("DELTA2044_6_total_abs", "Delta_Gamma_abs", "sum_i abs(Delta_i) no-cancellation", "NOT_RUN_COMPONENTS_MISSING", "all_connection_tests"),
    ]
    rows = []
    for row_id, symbol, formula, status, observables in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "status": status,
                "units": "hypermomentum_or_normalized_dimensionless_units_required",
                "observable_links": observables,
                "value": "MISSING_COMPONENT_VALUES",
                "no_cancellation": True,
                "score_ready": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def numeric_p4_source_rows() -> list[dict[str, object]]:
    data = [
        (
            "P4SRC2044_0_KRT2008_axial_torsion_anchor",
            "axial_torsion_spin_coupling",
            "c_A_or_S_mu",
            "torsion_component_bound_order",
            1.0e-31,
            "GeV",
            "order_of_magnitude_from_abstract",
            "https://arxiv.org/abs/0712.4393",
            "PhysRevLett.100.111102",
            "constraints involving 19 of 24 torsion components down to order 1e-31 GeV",
            "SOURCE_BACKED_ANCHOR_NOT_MTS_MAP",
            "needs map from MTS axial torsion/hypermomentum variable to KRT torsion irreducible-component basis and lab-frame convention",
            "nonclaim_numeric_anchor",
        ),
        (
            "P4SRC2044_1_Terrano2015_spin_context",
            "axial_torsion_spin_context",
            "spin_dependent_electron_interaction",
            "symmetry_breaking_scale_context",
            70.0,
            "TeV",
            "abstract_context_not_torsion_component_bound",
            "https://arxiv.org/abs/1508.02463",
            "PhysRevLett.115.201801",
            "spin-polarized torsion pendulum source candidate; highest symmetry-breaking scales up to 70 TeV in stated context",
            "SOURCE_BACKED_CONTEXT_NOT_DIRECT_P4_BOUND",
            "not a direct c_A/S_mu torsion coefficient until interaction-basis map is derived",
            "context_only",
        ),
    ]
    rows = []
    for (
        row_id,
        channel,
        coefficient,
        bound_quantity,
        bound_value,
        bound_units,
        extraction_method,
        source_url,
        source_ref,
        source_anchor,
        provenance_status,
        missing_for_claim,
        runner_role,
    ) in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "channel": channel,
                "coefficient": coefficient,
                "bound_quantity": bound_quantity,
                "bound_value": bound_value,
                "bound_units": bound_units,
                "extraction_method": extraction_method,
                "source_url": source_url,
                "source_ref": source_ref,
                "source_anchor": source_anchor,
                "provenance_status": provenance_status,
                "missing_for_claim": missing_for_claim,
                "runner_role": runner_role,
                "valid_numeric_anchor": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def p4_mapping_requirements_rows() -> list[dict[str, object]]:
    data = [
        ("MAP2044_0_component_basis", "map MTS c_A/S_mu/Delta_lambda to torsion irreducible components", "MISSING_BASIS_MAP", "KRT source cannot be used as bound without component projection"),
        ("MAP2044_1_units", "convert MTS coefficient units to GeV torsion-component units or normalized dimensionless envelope", "MISSING_UNIT_NORMALIZATION", "prevents apples-to-oranges bound comparison"),
        ("MAP2044_2_lab_frame", "lab/Sun-centered frame convention and orientation/time dependence", "MISSING_FRAME_CONVENTION", "torsion/LV bounds are component-frame dependent"),
        ("MAP2044_3_observable_kernel", "kernel from torsion component to WEP/clock/source/orbit residual", "MISSING_OBSERVABLE_KERNEL", "needed before P4 runner can compare prediction to bound"),
        ("MAP2044_4_no_cancellation", "absolute envelope over all connection components", "ENFORCED_SCHEMA", "no signed cancellation between unknown components"),
        ("MAP2044_5_claim_rule", "claim allowed iff zero theorem signed OR numeric MTS component map and source-backed bound both exist", "CLAIM_BLOCKED_CURRENTLY", "keeps source row useful but private/nonclaim"),
    ]
    rows = []
    for row_id, requirement, status, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "requirement": requirement,
                "status": status,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows(source_rows: list[dict[str, object]], mapping_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    missing = [row["row_id"] for row in mapping_rows if str(row["status"]).startswith("MISSING") or str(row["status"]).startswith("CLAIM_BLOCKED")]
    rows = []
    for source in source_rows:
        row = base_row()
        row.update(
            {
                "run_id": f"RUN2044_{source['row_id']}",
                "input_id": source["row_id"],
                "channel": source["channel"],
                "numeric_anchor_present": bool(source["valid_numeric_anchor"]),
                "accepted_for_scoring": False,
                "verdict": "REJECTED_MAPPING_MISSING",
                "missing_requirements": ";".join(missing),
                "reason": "source-backed numeric/context row exists, but MTS-to-torsion component map, units, frame and observable kernels are missing",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2044_VERDICT",
            "input_id": "all_numeric_P4_sources",
            "channel": "axial_torsion_spin_coupling",
            "numeric_anchor_present": True,
            "accepted_for_scoring": False,
            "verdict": "P4_NUMERIC_SOURCE_STAGED_NONCLAIM_NO_SCORE",
            "missing_requirements": ";".join(missing),
            "reason": "first numeric source is acquired as an anchor only; no MTS P4 pass is possible yet",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2044_0_sector_gamma", "all sector Gamma slots are parent-signed Gamma-free", "FAIL_BLOCKED", "sector audit has unsigned spin/source/clock/orbit/boundary clauses"),
        ("GATE2044_1_no_hypermomentum", "Delta_Gamma_abs=0", "FAIL_BLOCKED", "component zero theorem not signed and component values missing"),
        ("GATE2044_2_numeric_P4", "first P4 numeric source row is scoreable", "FAIL_BLOCKED", "numeric torsion anchor exists but MTS basis/unit/kernel map is missing"),
        ("GATE2044_3_Levi_Civita", "Gamma=LC(g_obs)", "FAIL_BLOCKED", "requires zero hypermomentum, projective silence and EH-only connection action"),
        ("GATE2044_4_WEP_clock_orbit", "WEP/clock/orbital connection safety", "FAIL_BLOCKED", "P4 residual rows not zeroed or bounded"),
        ("GATE2044_5_local_GR_Newton", "derived local GR/Newton branch", "FAIL_BLOCKED", "connection gate and other EH/GM/PPN gates remain unresolved"),
        ("GATE2044_6_public_claim", "public local-GR/PPN/R10/WEP claim", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "status": status,
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2044_0_sector_audit",
            "The universal Gamma-slot proof still does not close sector-by-sector.",
            "Matter is conditional; spin, source/worldtube, clock/light, orbital and boundary sectors remain unsigned or downstream.",
        ),
        (
            "DEC2044_1_numeric_source",
            "The first numeric P4 source anchor is staged from torsion bounds.",
            "Kostelecky/Russell/Tasson gives a real torsion-component order-of-magnitude bound, but MTS cannot score it until the component-basis/unit/kernel map exists.",
        ),
        (
            "DEC2044_2_best_next",
            "Next target should derive the MTS-to-torsion component map for the axial row.",
            "That is more useful than gathering more bounds: without the map, every source stays decorative.",
        ),
        (
            "DEC2044_3_project_status",
            "The connection/coupling route is now test-plumbed.",
            "We have an exact theorem target, sector blockers, and the first external numeric anchor. The missing bridge is the projection map.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2044_0_2045",
            "target_doc": "2045-Y5-R2FR-MTS-axial-torsion-component-map-or-P4-bound-runner.md",
            "objective": "derive or stage the map from MTS axial torsion/hypermomentum variables to the KRT torsion-component basis and units; if the map fails, write the exact missing projection ledger for c_A/S_mu before any P4 score",
            "must_include": "MTS c_A/S_mu definition; torsion irreducible component basis; units GeV conversion or dimensionless normalization; lab-frame convention; observable kernel to WEP/clock/source/orbit; no-cancellation runner refusal",
            "excluded": "claiming torsion pass from 1e-31 GeV anchor alone; using spin-pendulum context as direct MTS coefficient; invented c_A/c_Q values; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    sector_rows: list[dict[str, object]],
    numeric_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2044_0_source_weight_sector_gamma",
            SOURCE_WEIGHT_DOCS / "AFRAME_SECTOR_GAMMA_AUDIT_2044_NONCLAIM.csv",
            sector_rows,
        ),
        (
            "COPY2044_1_wep_numeric_p4_anchor",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2044_NUMERIC_P4_SOURCE_ANCHOR_NONCLAIM.csv",
            numeric_rows,
        ),
        (
            "COPY2044_2_rab_next",
            QUEUE / "JR2044_AXIAL_TORSION_COMPONENT_MAP_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    sector: list[dict[str, object]],
    delta: list[dict[str, object]],
    numeric: list[dict[str, object]],
    mapping: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    local_sources_ok = all(
        row["status"] == "EXISTS_NEEDLES_CONFIRMED"
        for row in sources
        if row["source_kind"] == "local"
    )
    external_sources_ok = all(
        str(row["source_url"]).startswith("https://") and row["status"] == "SOURCE_STRING_RECORDED_NONCLAIM"
        for row in sources
        if row["source_kind"] == "external_web_record"
    )
    sector_verdict = next(row for row in sector if row["row_id"] == "SECG2044_6_verdict")
    delta_total = next(row for row in delta if row["row_id"] == "DELTA2044_6_total_abs")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2044_VERDICT")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2044_5_local_GR_Newton")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2044_00_local_sources_exist", local_sources_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2044_01_external_sources_recorded", external_sources_ok, "external source URLs/DOIs recorded as nonclaim provenance"))
    checks.append(("VAL2044_02_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2044_03_sector_audit_blocks", sector_verdict["status"] == "FAIL_CURRENT_CORPUS", "sector Gamma audit remains blocked"))
    checks.append(("VAL2044_04_delta_total_not_run", delta_total["status"] == "NOT_RUN_COMPONENTS_MISSING", "total hypermomentum envelope refuses scoring"))
    checks.append(("VAL2044_05_numeric_anchor_positive", all(float(row["bound_value"]) > 0 for row in numeric), "numeric source anchors have positive values"))
    checks.append(("VAL2044_06_mapping_missing", any(str(row["status"]).startswith("MISSING") for row in mapping), "mapping requirements remain missing"))
    checks.append(("VAL2044_07_runner_rejects", runner_verdict["verdict"] == "P4_NUMERIC_SOURCE_STAGED_NONCLAIM_NO_SCORE", "runner rejects source anchor as nonclaim/no-score"))
    checks.append(("VAL2044_08_claim_gates_closed", local_gate["status"] == "FAIL_BLOCKED", "local-GR/Newton claim gate remains closed"))
    checks.append(("VAL2044_09_next_selected", next_rows_[0]["target_id"] == "NEXT2044_0_2045", "2045 axial torsion component-map target selected"))
    checks.append(("VAL2044_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2044_11_no_formalization_2044_artifacts", not formalization_has_2044_artifacts(), "no 2044 artifacts were written under formalization-workbench"))
    checks.append(("VAL2044_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2044_OVERALL", overall_ok, "2044 audits sector Gamma slots and stages first numeric P4 source without scoring claims"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    sector: list[dict[str, object]],
    delta: list[dict[str, object]],
    numeric: list[dict[str, object]],
    mapping: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2044 Y5 R2FR Sector Gamma-Slot Audit Or First Numeric P4 Source",
        "",
        "## Current Verdict",
        "",
        "2044 splits the `Gamma`-slot problem sector by sector. The universal closure still does not close: matter is only conditional, while spin, source/worldtube, clock/lightcone, orbital readout, and boundary/non-Hilbert sectors remain unsigned or downstream.",
        "",
        "The useful forward move is that the first numeric P4 source anchor is now staged. Kostelecky/Russell/Tasson provides a real torsion-component bound at order `1e-31 GeV`, but it is **not** an MTS pass because the MTS `c_A/S_mu` or hypermomentum variable has not been mapped to their torsion-component basis, units, lab-frame convention, or observable kernels. No local-GR, Newton, WEP, clock, orbital, PPN, R10, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "source_url", "status", "note", "valid_for_claim"]),
        "## Sector Gamma-Slot Audit",
        md_table(sector, ["row_id", "sector", "action_argument_form", "status", "if_signed", "blocker", "next_action", "claim_allowed"]),
        "## Delta Gamma Component Envelope",
        md_table(delta, ["row_id", "symbol", "formula", "status", "units", "observable_links", "value", "no_cancellation", "score_ready", "claim_allowed"]),
        "## Numeric P4 Source Anchors",
        md_table(numeric, ["row_id", "channel", "coefficient", "bound_quantity", "bound_value", "bound_units", "extraction_method", "source_url", "source_ref", "provenance_status", "missing_for_claim", "ready_for_scoring", "claim_allowed"]),
        "## P4 Mapping Requirements",
        md_table(mapping, ["row_id", "requirement", "status", "rationale", "claim_allowed"]),
        "## Runner Dry Run",
        md_table(runner, ["run_id", "input_id", "channel", "numeric_anchor_present", "accepted_for_scoring", "verdict", "missing_requirements", "reason", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    sector = sector_gamma_audit_rows()
    delta = sector_delta_rows()
    numeric = numeric_p4_source_rows()
    mapping = p4_mapping_requirements_rows()
    runner = runner_rows(numeric, mapping)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2044_SOURCE_REGISTER.csv",
        "sector": OUT / "P8_Y5_PARENT_QLOC_2044_SECTOR_GAMMA_AUDIT.csv",
        "delta": OUT / "P8_Y5_PARENT_QLOC_2044_DELTA_GAMMA_COMPONENT_ENVELOPE.csv",
        "numeric": OUT / "P8_Y5_PARENT_QLOC_2044_NUMERIC_P4_SOURCE_ANCHORS.csv",
        "mapping": OUT / "P8_Y5_PARENT_QLOC_2044_P4_MAPPING_REQUIREMENTS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2044_RUNNER_DRYRUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2044_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2044_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2044_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2044_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2044_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["sector"], sector)
    write_csv(paths["delta"], delta)
    write_csv(paths["numeric"], numeric)
    write_csv(paths["mapping"], mapping)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(sector, numeric, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, sector, delta, numeric, mapping, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, sector, delta, numeric, mapping, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, sector, delta, numeric, mapping, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
