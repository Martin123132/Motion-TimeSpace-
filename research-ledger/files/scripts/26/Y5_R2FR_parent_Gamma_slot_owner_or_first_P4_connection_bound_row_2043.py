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


DOC = ROOT / "2043-Y5-R2FR-parent-Gamma-slot-owner-or-first-P4-connection-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2043_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        artifact_patterns = (
            "*2043-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2043*",
            "*Y5_R2FR_parent_Gamma_slot_owner_or_first_P4_connection_bound_row_2043*",
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
    specs = [
        (
            "SRC2043_00_2042_doc",
            ROOT / "2042-Y5-R2FR-Levi-Civita-no-hypermomentum-parent-clause-or-P4-connection-row.md",
            ["NEXT2042_0_2043", "GSA2042_7_verdict", "VAL2042_OVERALL"],
            "2042 handoff: hunt Gamma-slot owner or build first P4 connection row.",
        ),
        (
            "SRC2043_01_2042_next",
            OUT / "P8_Y5_PARENT_QLOC_2042_NEXT_TARGET.csv",
            ["NEXT2042_0_2043", "Gamma-slot owner"],
            "machine-readable 2043 target.",
        ),
        (
            "SRC2043_02_2042_gamma",
            OUT / "P8_Y5_PARENT_QLOC_2042_GAMMA_SLOT_AUDIT.csv",
            ["GSA2042_1_ordinary_matter", "GSA2042_7_verdict"],
            "Gamma-slot audit requiring all ordinary slots to close.",
        ),
        (
            "SRC2043_03_2042_p4",
            OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv",
            ["P4C1960_1_axial_torsion", "P4C1960_5_hypermomentum"],
            "P4 connection interface selected for finite fallback rows.",
        ),
        (
            "SRC2043_04_1045_matter_functor",
            ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            ["MFS1045_1_observed_coframe_functor", "QG1045_2_connection_stack", "V1045_SUMMARY"],
            "matter functor descent and independent connection caveat.",
        ),
        (
            "SRC2043_05_1065_parent_grammar",
            ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
            ["PGG1065_0_parent_language", "PGG1065_4_measure_coframe_descent", "AAG1065_6_nonHilbert_current"],
            "ordinary matter object language and non-Hilbert current caveat.",
        ),
        (
            "SRC2043_06_1309_matter_descent",
            ROOT / "1309-Y5-R10-RAB-matter-descent-constant-marker-theorem-or-qc-residual.md",
            ["QZT1309_1_chain_rule", "MCG1309_0_observed_coframe", "VAL1309_6_csv_parse"],
            "ordinary matter descent through observed coframe/spin connection, conditional only.",
        ),
        (
            "SRC2043_07_1339_left_hand",
            ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
            ["EHGate1339_3_Levi_Civita", "R11V1339_1_torsion_nonmetricity", "VAL1339_12_overall"],
            "left-hand GR gate map: Levi-Civita remains not parent-derived.",
        ),
        (
            "SRC2043_08_1340_R11_interface",
            ROOT / "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
            ["EH1340_3_connection_obstruction", "R11SCHEMA1340_2_connection", "VAL1340_11_overall"],
            "strict R11 connection residual interface already exists and rejects placeholders.",
        ),
        (
            "SRC2043_09_1960_p4",
            OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
            ["P4C1960_1_axial_torsion", "P4C1960_5_hypermomentum"],
            "current P4 subrow ledger.",
        ),
        (
            "SRC2043_10_R11_vector",
            OUT / "R11_nonEH_operator_vector_executable.csv",
            ["torsion_nonmetricity", "MISSING_WEP_CLOCK_LIGHTCONE_SPIN_SOURCE_MAP"],
            "global torsion/nonmetricity R11 vector row.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def gamma_slot_owner_rows() -> list[dict[str, object]]:
    data = [
        (
            "GSO2043_0_target",
            "parent ordinary-action Gamma-slot owner",
            "S_ord must be a local functional of e_obs(q), g_obs(q), omega_LC[e_obs(q)], ordinary fields, gauge connections and constants, with no independent affine Gamma argument.",
            "TARGET_EXACT",
            "would make delta S_ord/delta Gamma=0 and activate 2042 no-hypermomentum theorem",
            "target is a future parent-action signature, not current proof",
            False,
        ),
        (
            "GSO2043_1_chain_rule",
            "if every ordinary slot factors through e_obs/g_obs and LC[e_obs], Gamma variation is absent",
            "delta_Gamma S_ord = 0 because Gamma is not an independent argument; variations route through delta e_obs/delta g_obs instead and are Hilbert stress, not hypermomentum.",
            "EXACT_CONDITIONAL_THEOREM",
            "separates GR/coframe matter from metric-affine matter",
            "requires parent object-language exhaustion across matter/source/readout",
            "conditional_only",
        ),
        (
            "GSO2043_2_no_extra_connection_counterterm",
            "forbid independent connection operators",
            "No T^2, Q^2, R(Gamma)^2, Gamma-source, spin-torsion, clock-nonmetricity or boundary/non-Hilbert connection term appears unless retained as P4.",
            "UNSIGNED",
            "prevents connection leakage from bypassing the matter no-Gamma clause",
            "1340/2042 keep torsion_nonmetricity family live",
            False,
        ),
        (
            "GSO2043_3_source_readout_closure",
            "source, clock, lightcone and orbital readout also use only g_obs/LC",
            "Worldline/source/readout actions depend on proper time, null cones and orbital geometry from g_obs, with no separate Gamma current.",
            "UNSIGNED",
            "needed for WEP, clock, Shapiro, orbital and Newton measured-GM safety",
            "readout and source action arguments are not parent-signed",
            False,
        ),
        (
            "GSO2043_4_spin_guard",
            "spin connection is coframe-owned",
            "Spinors use omega[e_obs] and do not couple to independent torsion; otherwise axial torsion is a real residual.",
            "UNSIGNED",
            "needed to suppress the P4 axial torsion row",
            "spin/torsion guard remains a specific missing clause",
            False,
        ),
        (
            "GSO2043_5_projective_boundary_guard",
            "projective and boundary/non-Hilbert connection currents are silent",
            "Projective trace is gauge/unobservable, and boundary or support-shift connection currents vanish or are retained as P4 residuals.",
            "UNSIGNED",
            "needed before Palatini can be promoted to LC in local observables",
            "projective and non-Hilbert current caveats remain open",
            False,
        ),
        (
            "GSO2043_6_verdict",
            "Gamma-slot owner theorem",
            "GSO2043_0 through GSO2043_5 parent-signed in one action language.",
            "NOT_PARENT_DERIVED_CURRENT_CORPUS",
            "would close no-hypermomentum/LC connection gate",
            "current evidence gives exact contract and conditional theorem, not the parent signature",
            False,
        ),
    ]
    rows = []
    for row_id, clause, mathematical_statement, status, would_close, blocker, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "mathematical_statement": mathematical_statement,
                "status": status,
                "would_close": would_close,
                "blocker": blocker,
                "parent_signed": parent_signed,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def action_argument_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "ARG2043_0_geometry",
            "geometry",
            "e_obs(q), g_obs(q), omega_LC[e_obs(q)]",
            "allowed_required",
            "ordinary GR geometry slot",
            "parent q/e_obs functor still conditional",
        ),
        (
            "ARG2043_1_matter_fields",
            "ordinary matter fields",
            "Psi_A in bundles over e_obs/g_obs with representation constants theta_A",
            "allowed_required",
            "needed for matter descent",
            "matter category not fully parent-constructed",
        ),
        (
            "ARG2043_2_gauge_connections",
            "gauge connections",
            "A_Q and other internal gauge connections owned by charge/lattice representation, not affine Gamma",
            "allowed_with_owner",
            "keeps EM/internal gauge separate from spacetime connection",
            "gauge norm/charge owner still separate open gate",
        ),
        (
            "ARG2043_3_affine_Gamma",
            "independent affine Gamma",
            "Gamma^lambda_{mu nu} as separate matter/source/readout argument",
            "forbidden_or_retained_P4",
            "the core slot under audit",
            "not parent-forbidden yet",
        ),
        (
            "ARG2043_4_spin_torsion",
            "torsionful spin connection",
            "omega_ind[e,Gamma] or axial torsion coupling",
            "forbidden_or_retained_P4",
            "must be blocked for axial torsion zero",
            "spin guard unsigned",
        ),
        (
            "ARG2043_5_nonmetricity_clock",
            "nonmetricity clock/rod connection",
            "Q_rho mu nu, Weyl trace, shear nonmetricity in readout",
            "forbidden_or_retained_P4",
            "must be blocked for clock/lightcone safety",
            "clock/light readout Gamma slots unsigned",
        ),
        (
            "ARG2043_6_source_worldtube",
            "source/worldtube connection current",
            "source charge depends on independent Gamma, boundary torsion, support shift or non-Hilbert current",
            "forbidden_or_retained_P4",
            "must be blocked for Newton measured-GM and WEP source",
            "source action argument not parent-signed",
        ),
        (
            "ARG2043_7_verdict",
            "ordinary action object language",
            "allowed slots are exhausted and forbidden slots are parent-excluded or P4-retained",
            "FAIL_CURRENT_CORPUS",
            "would convert closure into derivation",
            "several forbidden slots remain unsigned",
        ),
    ]
    rows = []
    for row_id, slot, argument_form, status, why_needed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "slot": slot,
                "argument_form": argument_form,
                "status": status,
                "why_needed": why_needed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def spin_projective_guard_rows() -> list[dict[str, object]]:
    data = [
        (
            "SPG2043_0_spin_guard",
            "axial torsion",
            "omega_spin = omega_LC[e_obs] and no independent contorsion K_{abc} couples to spin current",
            "UNSIGNED",
            "if false, axial torsion P4 row is first priority",
            "P4C1960_1_axial_torsion",
        ),
        (
            "SPG2043_1_projective_guard",
            "projective trace",
            "Gamma projective trace is gauge/unobservable in matter/source/readout or explicitly gauge-fixed",
            "UNSIGNED",
            "if false, projective trace P4 row is retained",
            "P4C1960_2_projective_trace",
        ),
        (
            "SPG2043_2_weyl_clock_guard",
            "Weyl nonmetricity",
            "Q_trace does not alter rods, clocks, masses or source normalization except through bounded residuals",
            "UNSIGNED",
            "if false, clock/source P4 row is retained",
            "P4C1960_3_weyl_nonmetricity",
        ),
        (
            "SPG2043_3_shear_light_guard",
            "shear nonmetricity",
            "null cones and optical readout are metric g_obs readouts, not shear-nonmetric connection readouts",
            "UNSIGNED",
            "if false, lightcone P4 row is retained",
            "P4C1960_4_shear_nonmetricity",
        ),
        (
            "SPG2043_4_hypermomentum_guard",
            "hypermomentum",
            "delta S_ord/delta Gamma=0 across matter, source, clock, light and orbital readout",
            "UNSIGNED",
            "if false, hypermomentum P4 row is first broad fallback",
            "P4C1960_5_hypermomentum",
        ),
        (
            "SPG2043_5_verdict",
            "spin/projective/nonmetricity guards",
            "all guard rows are parent-signed or bounded",
            "FAIL_CURRENT_CORPUS",
            "guards are now exact but not proven",
            "prioritize hypermomentum and axial torsion P4 templates",
        ),
    ]
    rows = []
    for row_id, guard, required_clause, status, fallback_if_false, p4_row in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "guard": guard,
                "required_clause": required_clause,
                "status": status,
                "fallback_if_false": fallback_if_false,
                "p4_row": p4_row,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def first_p4_bound_rows() -> list[dict[str, object]]:
    data = [
        (
            "P4B2043_0_hypermomentum",
            "independent_connection_hypermomentum",
            "c_Delta_or_Delta_lambda_munu",
            "Delta_abs := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary||",
            "hypermomentum units or normalized dimensionless envelope",
            "WEP;clock;source_charge;orbital;PPN;local_GR",
            "MISSING_DELTA_COMPONENT_VALUES",
            "MISSING_HYPERMOMENTUM_TO_OBSERVABLE_KERNELS",
            "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv::NH2042_5_verdict;P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv::P4C1960_5_hypermomentum",
            "first broad P4 fallback if Gamma-slot owner fails",
        ),
        (
            "P4B2043_1_axial_torsion",
            "axial_torsion_spin_coupling",
            "c_A_or_S_mu",
            "S_axial_abs := ||c_A S_mu J5^mu|| or normalized spin-torsion response envelope",
            "spin-current units or normalized dimensionless envelope",
            "spin_transport;clock;WEP;source_charge",
            "MISSING_SPIN_TORSION_COEFFICIENT",
            "MISSING_SPIN_TORSION_TO_OBSERVABLE_KERNELS",
            "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv::P4C1960_1_axial_torsion",
            "first narrow P4 fallback if spin guard fails",
        ),
    ]
    rows = []
    for (
        row_id,
        channel,
        coefficient,
        residual_formula,
        units,
        affected_tests,
        current_value,
        missing_map,
        source_anchor,
        role,
    ) in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "channel": channel,
                "coefficient": coefficient,
                "residual_formula": residual_formula,
                "units": units,
                "affected_tests": affected_tests,
                "current_value": current_value,
                "weak_field_map": missing_map,
                "bound_source": "MISSING_SOURCE_BACKED_BOUND",
                "source_anchor": source_anchor,
                "role": role,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def p4_runner_rows(p4_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for index, source in enumerate(p4_rows):
        missing = [
            field
            for field in ("current_value", "weak_field_map", "bound_source")
            if str(source.get(field, "")).startswith("MISSING")
        ]
        row = base_row()
        row.update(
            {
                "run_id": f"P4RUN2043_{index}",
                "input_id": source["row_id"],
                "channel": source["channel"],
                "accepted_for_scoring": False,
                "verdict": "REJECTED_MISSING_EXECUTABLE_INPUTS",
                "missing_fields": ";".join(missing),
                "reason": "strict P4 interface: no score without coefficient/value, units, weak-field map, source-backed bound and no-cancellation guard",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "P4RUN2043_VERDICT",
            "input_id": "all_P4_connection_rows",
            "channel": "hypermomentum;axial_torsion",
            "accepted_for_scoring": False,
            "verdict": "P4_CONNECTION_BRANCH_BLOCKED_NONCLAIM",
            "missing_fields": "parent_zero_signature_or_complete_numeric_bound_inputs",
            "reason": "first P4 rows are now concrete acquisition rows but not claim-valid",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2043_0_gamma_slot_owner", "parent Gamma-slot owner theorem", "FAIL_BLOCKED", "ordinary action object language not parent-derived"),
        ("GATE2043_1_no_hypermomentum", "Delta_lambda^{mu nu}=0", "FAIL_BLOCKED", "conditional theorem cannot promote without Gamma-slot owner"),
        ("GATE2043_2_Levi_Civita", "Gamma=LC(g_obs)", "FAIL_BLOCKED", "needs zero hypermomentum, EH-only connection action and projective silence"),
        ("GATE2043_3_P4_score", "first P4 connection row scoreable", "FAIL_BLOCKED", "hypermomentum/axial rows lack coefficient values, maps and source-backed bounds"),
        ("GATE2043_4_WEP_clock_orbital", "WEP/clock/orbital safety from connection sector", "FAIL_BLOCKED", "connection residual branch not zeroed or bounded"),
        ("GATE2043_5_local_GR", "derived local GR/Newton branch", "FAIL_BLOCKED", "connection gate is still one unresolved gate among EH, beta, conservation, matter and GM transfer"),
        ("GATE2043_6_public_claim", "public local-GR/PPN/R10/WEP claim", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
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
            "DEC2043_0_theorem_result",
            "The parent Gamma-slot theorem is exact as a contract but not derived.",
            "If the ordinary action language excludes independent Gamma, 2042 closes; current files do not prove the exclusion.",
        ),
        (
            "DEC2043_1_p4_result",
            "The first P4 fallback rows are now concrete acquisition rows.",
            "Hypermomentum is the broad coupling fallback; axial torsion is the sharp spin fallback. Both remain nonclaim until maps and bounds exist.",
        ),
        (
            "DEC2043_2_best_next",
            "Next best route is to split the Gamma-slot owner by sector.",
            "Trying one universal proof keeps failing; sector-by-sector source/matter/clock/orbit audit can either sign the owner or identify the first real P4 coefficient target.",
        ),
        (
            "DEC2043_3_project_status",
            "This is a forward leap, not another loop.",
            "We moved from 'coupling is suspicious' to a variational target: delta S_ord/delta Gamma, with named fallback residuals.",
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
            "target_id": "NEXT2043_0_2044",
            "target_doc": "2044-Y5-R2FR-sector-Gamma-slot-audit-or-first-numeric-P4-source.md",
            "objective": "audit matter, spin, source/worldtube, clock/lightcone and orbital readout sectors one by one for independent Gamma arguments; if any sector remains unsigned, choose hypermomentum or axial torsion and source the first numeric bound/mapping row",
            "must_include": "sector action arguments; deltaS/deltaGamma status; spin/coframe guard; source/worldtube guard; clock/lightcone guard; orbital readout guard; P4 coefficient/map/bound acquisition choice; no-claim gates",
            "excluded": "single-line universal closure; claiming Levi-Civita from GR notation; invented torsion/nonmetricity coefficients; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    gamma_rows: list[dict[str, object]],
    p4_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2043_0_source_weight_gamma_owner",
            SOURCE_WEIGHT_DOCS / "AFRAME_GAMMA_SLOT_OWNER_2043_NONCLAIM.csv",
            gamma_rows,
        ),
        (
            "COPY2043_1_wep_first_p4_rows",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2043_FIRST_P4_CONNECTION_ROWS_NONCLAIM.csv",
            p4_rows,
        ),
        (
            "COPY2043_2_rab_next",
            QUEUE / "JR2043_SECTOR_GAMMA_SLOT_AUDIT_NEXT_NONCLAIM.csv",
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
    source_rows: list[dict[str, object]],
    gamma_rows: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    p4_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    gamma_verdict = next(row for row in gamma_rows if row["row_id"] == "GSO2043_6_verdict")
    action_verdict = next(row for row in action_rows if row["row_id"] == "ARG2043_7_verdict")
    guard_verdict = next(row for row in guard_rows if row["row_id"] == "SPG2043_5_verdict")
    p4_verdict = next(row for row in runner_rows if row["run_id"] == "P4RUN2043_VERDICT")
    local_gate = next(row for row in gate_rows if row["row_id"] == "GATE2043_5_local_GR")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2043_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited local source paths and needles exist"))
    checks.append(("VAL2043_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2043_02_gamma_owner_not_promoted", gamma_verdict["status"] == "NOT_PARENT_DERIVED_CURRENT_CORPUS", "Gamma-slot owner theorem is not promoted"))
    checks.append(("VAL2043_03_action_language_not_closed", action_verdict["status"] == "FAIL_CURRENT_CORPUS", "ordinary action object language remains unsigned"))
    checks.append(("VAL2043_04_guards_not_closed", guard_verdict["status"] == "FAIL_CURRENT_CORPUS", "spin/projective/nonmetricity guards remain unsigned"))
    checks.append(("VAL2043_05_first_p4_rows_nonclaim", all(not bool(row.get("ready_for_scoring")) for row in p4_rows), "first P4 rows are concrete but nonclaim"))
    checks.append(("VAL2043_06_runner_rejects", p4_verdict["verdict"] == "P4_CONNECTION_BRANCH_BLOCKED_NONCLAIM", "P4 runner rejects missing executable inputs"))
    checks.append(("VAL2043_07_claim_gates_closed", local_gate["status"] == "FAIL_BLOCKED", "local-GR claim gate remains closed"))
    checks.append(("VAL2043_08_next_selected", next_rows_[0]["target_id"] == "NEXT2043_0_2044", "2044 sector Gamma-slot audit target selected"))
    checks.append(("VAL2043_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2043_10_no_formalization_2043_artifacts", not formalization_has_2043_artifacts(), "no 2043 artifacts were written under formalization-workbench"))
    checks.append(("VAL2043_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2043_OVERALL", overall_ok, "2043 writes the Gamma-slot owner contract and first P4 rows without promoting claims"))
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
    source_rows: list[dict[str, object]],
    gamma_rows: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    p4_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2043 Y5 R2FR Parent Gamma-Slot Owner Or First P4 Connection Bound Row",
        "",
        "## Current Verdict",
        "",
        "2043 does not close the connection theorem, but it turns the missing coupling into an exact action-language problem. The future parent action must exhaust the ordinary slots: matter, source, clocks, lightcones and orbital readout may use `e_obs`, `g_obs`, `omega_LC[e_obs]`, gauge connections and constants, but not an independent affine `Gamma` unless that dependence is retained as a P4 residual.",
        "",
        "That is the cleanest route to `Delta_lambda^{mu nu}=0` and then `Gamma=LC(g_obs)`. Current evidence still does not parent-sign the exclusion, so the first P4 fallback rows are staged for hypermomentum and axial torsion. They are concrete acquisition rows, not score rows. No local-GR, EH, WEP, clock, orbital, PPN, R10, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Gamma-Slot Owner Theorem Attempt",
        md_table(gamma_rows, ["row_id", "clause", "mathematical_statement", "status", "would_close", "blocker", "parent_signed", "claim_allowed"]),
        "## Ordinary Action Argument Audit",
        md_table(action_rows, ["row_id", "slot", "argument_form", "status", "why_needed", "blocker", "claim_allowed"]),
        "## Spin / Projective Guard",
        md_table(guard_rows, ["row_id", "guard", "required_clause", "status", "fallback_if_false", "p4_row", "claim_allowed"]),
        "## First P4 Bound Rows",
        md_table(p4_rows, ["row_id", "channel", "coefficient", "residual_formula", "units", "affected_tests", "current_value", "weak_field_map", "bound_source", "role", "ready_for_scoring", "claim_allowed"]),
        "## P4 Runner Dry Run",
        md_table(runner_rows, ["run_id", "input_id", "channel", "accepted_for_scoring", "verdict", "missing_fields", "reason", "claim_allowed"]),
        "## Claim Gate",
        md_table(gate_rows, ["row_id", "gate", "status", "detail", "claim_allowed"]),
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
    source_rows = source_register_rows()
    gamma_rows = gamma_slot_owner_rows()
    action_rows = action_argument_audit_rows()
    guard_rows = spin_projective_guard_rows()
    p4_rows = first_p4_bound_rows()
    runner_rows = p4_runner_rows(p4_rows)
    gate_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2043_SOURCE_REGISTER.csv",
        "gamma": OUT / "P8_Y5_PARENT_QLOC_2043_GAMMA_SLOT_OWNER_THEOREM_ATTEMPT.csv",
        "action": OUT / "P8_Y5_PARENT_QLOC_2043_ORDINARY_ACTION_ARGUMENT_AUDIT.csv",
        "guards": OUT / "P8_Y5_PARENT_QLOC_2043_SPIN_PROJECTIVE_GUARD.csv",
        "p4": OUT / "P8_Y5_PARENT_QLOC_2043_FIRST_P4_BOUND_ROWS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2043_P4_RUNNER_DRYRUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2043_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2043_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2043_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2043_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2043_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["gamma"], gamma_rows)
    write_csv(paths["action"], action_rows)
    write_csv(paths["guards"], guard_rows)
    write_csv(paths["p4"], p4_rows)
    write_csv(paths["runner"], runner_rows)
    write_csv(paths["gates"], gate_rows)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(gamma_rows, p4_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, gamma_rows, action_rows, guard_rows, p4_rows, runner_rows, gate_rows, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(source_rows, gamma_rows, action_rows, guard_rows, p4_rows, runner_rows, gate_rows, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(source_rows, gamma_rows, action_rows, guard_rows, p4_rows, runner_rows, gate_rows, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
