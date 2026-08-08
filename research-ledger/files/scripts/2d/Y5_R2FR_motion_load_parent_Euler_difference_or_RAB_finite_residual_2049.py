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


DOC = ROOT / "2049-Y5-R2FR-motion-load-parent-Euler-difference-or-RAB-finite-residual.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2049_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2049-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2049*",
            "*Y5_R2FR_motion_load_parent_Euler_difference_or_RAB_finite_residual_2049*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2049_00_2048_doc",
            ROOT / "2048-Y5-R2FR-motion-load-coframe-construction-or-CMTS-provenance.md",
            ["NEXT2048_0_2049", "MLC2048_6_radial_cell_condition", "VAL2048_OVERALL"],
            "2048 handoff into parent Euler difference for R_AB=0.",
        ),
        (
            "SRC2049_01_2048_next",
            OUT / "P8_Y5_PARENT_QLOC_2048_NEXT_TARGET.csv",
            ["NEXT2048_0_2049", "E_time", "finite R_AB fallback"],
            "machine-readable 2049 target.",
        ),
        (
            "SRC2049_02_1859_noGR",
            ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            ["MPD1859_6_best_surviving_route", "FRS1859_2_parent_Euler_difference", "VAL1859_OVERALL"],
            "no-GR-import audit selecting parent Euler/source-map route.",
        ),
        (
            "SRC2049_03_1275_difference",
            ROOT / "1275-Y5-R10-RAB-GR-style-radial-field-equation-difference-or-local-closure-baseline.md",
            ["EDA1275_0_contract_form", "MPE1275_1_Euler_pair", "VAL1275_12_overall"],
            "GR-style radial equation-difference guard and missing parent Euler pair.",
        ),
        (
            "SRC2049_04_1276_contract",
            ROOT / "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
            ["ESC1276_2_E_time", "ESC1276_9_verdict", "VAL1276_11_overall"],
            "parent Euler/source-map executable contract.",
        ),
        (
            "SRC2049_05_1279_extra_silence",
            ROOT / "1279-Y5-R10-RAB-A511-extra-sector-silence-double-zero-or-residual-vector.md",
            ["XSL1279_1_Gamma_Khat_q_loc", "DZS1279_7_verdict", "VAL1279_12_overall"],
            "extra-sector residual blocker for EH/Euler inheritance.",
        ),
        (
            "SRC2049_06_1577_current_fallback",
            ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            ["RCC1577_4_verdict", "FCF1577_0_qRhat", "VAL1577_OVERALL"],
            "radial current/no-charge failure and finite component fallback.",
        ),
        (
            "SRC2049_07_2048_coframe_csv",
            OUT / "P8_Y5_PARENT_QLOC_2048_MOTION_LOAD_COFRAME_CONSTRUCTION.csv",
            ["MLC2048_2_observed_coframe", "MLC2048_6_radial_cell_condition"],
            "machine-readable coframe and R_AB identity rows.",
        ),
        (
            "SRC2049_08_2047_cmts",
            OUT / "P8_Y5_PARENT_QLOC_2047_CMTS_FIRST_COEFFICIENT_CHAIN.csv",
            ["CMTS2047_0_C_tensor", "CMTS2047_VERDICT"],
            "connection fallback row retained in parallel.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def euler_coordinate_rows() -> list[dict[str, object]]:
    data = [
        (
            "ECO2049_0_log_variables",
            "x=ln(T), y=ln(sqrt(S))",
            "C_R := ln(T^2 S)=2(x+y); J_q=T sqrt(S)=exp(x+y).",
            "EXACT_VARIABLE_DEFINITION",
            "motion-load coframe variables",
            "none at identity level",
        ),
        (
            "ECO2049_1_parent_action_needed",
            "S_parent^rad[x,y,psi,extras,boundary]",
            "A parent local radial action must be supplied before E_time:=delta S/delta x and E_radial:=delta S/delta y are MTS equations.",
            "MISSING_PARENT_ACTION",
            "would make the Euler pair real rather than benchmark language",
            "current corpus has contracts and scaffolds, not the parent action",
        ),
        (
            "ECO2049_2_E_time",
            "E_time",
            "E_time := delta S_parent^rad / delta x, including matter/source/readout/extra/boundary terms in the 2048 coframe.",
            "DEFINED_AS_REQUIRED_VARIATION_NOT_EXTRACTED",
            "time/lapse Euler equation",
            "no source path for full S_parent^rad",
        ),
        (
            "ECO2049_3_E_radial",
            "E_radial",
            "E_radial := delta S_parent^rad / delta y, including radial routing/source/extra/boundary terms in the 2048 coframe.",
            "DEFINED_AS_REQUIRED_VARIATION_NOT_EXTRACTED",
            "radial routing Euler equation",
            "no source path for full S_parent^rad",
        ),
        (
            "ECO2049_4_difference_target",
            "D_R[MTS]",
            "D_R[MTS] must be an algebraic consequence of E_time and E_radial, with target form D_R=partial_r C_R-S_R[source,residual,boundary]=0 or equivalent positive second-order current equation.",
            "TARGET_FORM_NOT_DERIVED",
            "would make R_AB=0 a dynamical theorem when S_R and charge vanish",
            "E_time/E_radial not extracted",
        ),
        (
            "ECO2049_5_verdict",
            "Euler coordinate setup",
            "The variables and target combination are exact; the parent Euler equations are still missing.",
            "COORDINATES_READY_EULER_PAIR_MISSING",
            "sets up the next derivation cleanly",
            "no GR/Newton promotion",
        ),
    ]
    rows = []
    for row_id, object_name, formula, status, if_closed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": object_name,
                "formula": formula,
                "status": status,
                "if_closed": if_closed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def derivation_route_rows() -> list[dict[str, object]]:
    data = [
        (
            "DER2049_0_direct_constraint",
            "direct algebraic constraint",
            "A parent multiplier term int lambda_R C_R would give C_R=0 by variation of lambda_R.",
            "CLOSURE_CANDIDATE_NOT_PARENT_ORIGIN",
            "would derive p=1 immediately",
            "lambda_R origin and constraint class are not parent-signed",
        ),
        (
            "DER2049_1_first_order_difference",
            "first-order Euler difference",
            "If E_time-E_radial yields partial_r C_R=S_R and local vacuum/source-balanced branch proves S_R=0, then C_R=constant and C_R(infinity)=0 gives C_R=0.",
            "VALID_CONDITIONAL_ROUTE",
            "noncircular if E_time/E_radial and S_R are MTS-derived",
            "Euler pair and source map missing",
        ),
        (
            "DER2049_2_second_order_current",
            "positive current equation",
            "If parent action gives partial_r(W_R partial_r C_R)=J_R with W_R>0, J_R=0, Q_R=0 and C_R(infinity)=0, then C_R=0.",
            "VALID_CONDITIONAL_ROUTE",
            "matches reciprocal-strain/current contracts",
            "W_R positivity, J_R=0 and Q_R=0 are unsigned",
        ),
        (
            "DER2049_3_EH_inheritance",
            "derived EH fixed-point inheritance",
            "If MTS first derives EH+matter as the local fixed point and all extras are silent, GR's time-radial difference can be inherited without smuggling.",
            "VALID_BUT_BLOCKED_ROUTE",
            "least ad-hoc route once A511 blocks close",
            "extra-sector silence and source/readout gates remain open",
        ),
        (
            "DER2049_4_rejected_shortcuts",
            "direct phase-volume/Liouville/null/current shortcut",
            "1859 and 1577 reject these as selectors because they either work for any p or leave Q_R hair.",
            "REJECTED_AS_PARENT_DERIVATION",
            "prevents false progress",
            "none; keep rejected",
        ),
        (
            "DER2049_5_verdict",
            "R_AB=0 derivation attempt",
            "2049 cannot close R_AB=0 from current evidence; it narrows the proof to parent Euler pair plus source/no-charge certificates, or finite residual fallback.",
            "NOT_DERIVED_CURRENT_CORPUS",
            "honest next gate",
            "parent Euler/source/no-charge certificates absent",
        ),
    ]
    rows = []
    for row_id, route, statement, status, if_closed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "route": route,
                "statement": statement,
                "status": status,
                "if_closed": if_closed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def source_map_certificate_rows() -> list[dict[str, object]]:
    data = [
        (
            "SRCMAP2049_0_S_R_source",
            "S_R[source]",
            "time-minus-radial matter/source anisotropy in the 2048 coframe",
            "MISSING_SOURCE_MAP",
            "vacuum/source-balance theorem or finite source anisotropy row",
        ),
        (
            "SRCMAP2049_1_S_R_extra",
            "S_R[extra]",
            "Gamma_eff/K_hat/q_loc, memory, range, curvature-coupling and projector stress projected into D_R",
            "MISSING_EXTRA_SECTOR_SILENCE_OR_BOUND",
            "close A511_3 or use residual vector",
        ),
        (
            "SRCMAP2049_2_S_R_boundary",
            "S_R[boundary]",
            "boundary, support, symplectic and reference terms entering radial equation or integration constant",
            "MISSING_BOUNDARY_NO_CHARGE",
            "Q_R=0 and boundary normalization certificate",
        ),
        (
            "SRCMAP2049_3_S_R_readout",
            "S_R[readout]",
            "clock/orbital/source-measure readout regeneration of C_R after variation",
            "MISSING_READOUT_STABILITY",
            "same coframe/source readout theorem",
        ),
        (
            "SRCMAP2049_4_W_positive",
            "W_R",
            "positive operator/weight in second-order current route",
            "MISSING_OPERATOR_SIGN",
            "parent Hessian/ghost-free certificate",
        ),
        (
            "SRCMAP2049_5_verdict",
            "full source map",
            "all S_R and W_R certificates needed for R_AB=0",
            "SOURCE_MAP_NOT_DERIVED",
            "derive or source finite rows",
        ),
    ]
    rows = []
    for row_id, component, definition, status, needed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "component": component,
                "definition": definition,
                "status": status,
                "needed_next": needed,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_residual_rows() -> list[dict[str, object]]:
    data = [
        (
            "RAB2049_0_C_R_profile",
            "C_R(r)=ln(T^2S)",
            "dimensionless",
            "finite radial-cell strain profile if R_AB=0 is not derived",
            "MISSING_PROFILE_OR_ZERO_THEOREM",
            "PPN_gamma;PPN_beta;light_bending;Shapiro;orbital;R10;clock",
            "no score without profile, source path, normalization and no-cancellation guard",
        ),
        (
            "RAB2049_1_q_R_charge",
            "Q_R or q_R_hat",
            "dimensionless_or_declared_current_units",
            "integrated reciprocal hair from W_R partial_r C_R",
            "MISSING_QR_VALUE_OR_NO_CHARGE_THEOREM",
            "PPN;orbital;R10;local_GR",
            "inherits 1577 finite-component requirement",
        ),
        (
            "RAB2049_2_S_R_source",
            "S_R[source]",
            "source_anisotropy_units_or_dimensionless_envelope",
            "time-radial source imbalance in D_R",
            "MISSING_SOURCE_BALANCE_OR_NUMERIC_ROW",
            "Newton_GM;PPN_beta;WEP_source;orbital",
            "must not be hidden under local vacuum label",
        ),
        (
            "RAB2049_3_boundary_tail",
            "B_R/Pi_R",
            "boundary_current_units_or_dimensionless_envelope",
            "boundary/no-charge tail that can preserve R_AB hair",
            "MISSING_BOUNDARY_CLASS_OR_NUMERIC_BOUND",
            "orbital;clock;source_normalization;PPN",
            "absolute no-cancellation with source and bulk rows",
        ),
        (
            "RAB2049_4_tau_PPN",
            "tau_PPN^R",
            "dimensionless response matrix",
            "projection from C_R/q_R into gamma,beta and preferred-frame PPN residuals",
            "MISSING_PPN_PROJECTION",
            "PPN",
            "gamma=1 conditional cannot be used as beta proof",
        ),
        (
            "RAB2049_5_tau_R10_clock_orbit",
            "tau_R10^R;tau_clock^R;tau_orbital^R",
            "arena-specific kernels",
            "projection from finite R_AB residual to short-range, clock and orbital arenas",
            "MISSING_ARENA_PROJECTIONS",
            "R10;clock;orbital",
            "no cross-arena transfer without source-backed kernels",
        ),
        (
            "RAB2049_VERDICT",
            "finite R_AB residual branch",
            "nonclaim schema",
            "strict fallback if parent Euler/no-charge route remains unsigned",
            "STAGED_NOT_SCOREABLE",
            "all_local_arenas",
            "all rows remain invalid for claim until theorem-zero or numeric/source-backed inputs exist",
        ),
    ]
    rows = []
    for row_id, symbol, units, definition, status, observable_links, claim_rule in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "units": units,
                "definition": definition,
                "status": status,
                "observable_links": observable_links,
                "claim_rule": claim_rule,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2049_0_Euler_pair",
            "ECO2049_5_verdict",
            "claim E_time/E_radial extracted",
            "REJECTED_PARENT_EULER_PAIR_MISSING",
            "variables are ready, but parent action variation is absent",
        ),
        (
            "RUN2049_1_RAB_zero",
            "DER2049_5_verdict",
            "claim C_R=0 or T^2S=1",
            "REJECTED_PARENT_ORIGIN_MISSING",
            "valid conditional routes exist, but no route is parent-signed",
        ),
        (
            "RUN2049_2_source_map",
            "SRCMAP2049_5_verdict",
            "claim local source/residual side vanishes",
            "REJECTED_SOURCE_MAP_MISSING",
            "S_R components and Q_R/no-charge certificates remain unsigned",
        ),
        (
            "RUN2049_3_finite_score",
            "RAB2049_VERDICT",
            "score finite R_AB against local arenas",
            "REJECTED_PLACEHOLDER_RESIDUALS",
            "finite rows are strict schemas only, with no numeric/source-backed values",
        ),
        (
            "RUN2049_VERDICT",
            "all_2049_rows",
            "derive or score local GR route",
            "RAB_EULER_GATE_BLOCKED_NONCLAIM",
            "2049 narrows the proof to parent Euler/source/no-charge certificates and stages finite residual rows",
        ),
    ]
    rows = []
    for run_id, input_id, attempted, verdict, reason in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "input_id": input_id,
                "attempted": attempted,
                "verdict": verdict,
                "reason": reason,
                "score_attempted": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2049_0_variables", "x,y,C_R,J_q variables defined", "PASS_NONCLAIM", "exact coordinate identities only"),
        ("GATE2049_1_parent_Euler_pair", "E_time and E_radial extracted from MTS parent action", "FAIL_BLOCKED", "parent action variation missing"),
        ("GATE2049_2_D_R_equation", "D_R[MTS]=partial_r C_R-S_R derived", "FAIL_BLOCKED", "difference operator remains target form"),
        ("GATE2049_3_source_nocharge", "S_R=0 and Q_R=0 local branch", "FAIL_BLOCKED", "source, extra, boundary and readout certificates missing"),
        ("GATE2049_4_RAB_zero", "R_AB=0 / p=1 parent-derived", "FAIL_BLOCKED", "valid conditional route, no parent signature"),
        ("GATE2049_5_finite_residual_score", "finite R_AB branch scoreable", "FAIL_BLOCKED", "numeric/source-backed residual rows and arena projections missing"),
        ("GATE2049_6_local_GR_Newton", "derived local GR/Newton branch", "FAIL_BLOCKED", "beta/Euler/source/conservation gates remain open"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2049_0_real_gain",
            "The proof target is now variationally phrased in the motion-load variables.",
            "Using x=ln T and y=ln sqrt(S), the exact GR-lock variable is C_R=2(x+y); any serious parent action must control this Euler combination.",
        ),
        (
            "DEC2049_1_no_derivation_yet",
            "Do not claim R_AB=0 from current evidence.",
            "All available successful routes require parent Euler/source/no-charge certificates that are absent.",
        ),
        (
            "DEC2049_2_next_best_route",
            "Go after the minimal radial parent action/Euler pair next.",
            "That is the shortest route to either deriving D_R or proving the branch is closure-only and must be tested as finite residual.",
        ),
        (
            "DEC2049_3_testability",
            "Finite R_AB residual rows are now named and arena-linked.",
            "If the derivation fails, the project can still test the deviation instead of smuggling GR.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2049_0_2050",
            "target_doc": "2050-Y5-R2FR-minimal-motion-load-radial-action-or-RAB-residual-runner.md",
            "objective": "try to construct the minimal no-GR-import radial parent action in variables x=lnT and y=lnsqrtS whose Euler pair yields D_R[MTS]; if no parent action can be justified, build a strict finite R_AB residual runner",
            "must_include": "candidate S_rad; variations delta_x and delta_y; D_R combination; source map S_R; W_R positivity or constraint class; boundary/no-charge certificate; finite residual runner refusal",
            "excluded": "Einstein equation import; declaring lambda_R C_R as parent without origin; fitting p=1; claiming beta=1 from gamma alone; invented residual values; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    euler_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2049_0_source_weight_euler_contract",
            SOURCE_WEIGHT_DOCS / "AFRAME_MOTION_LOAD_EULER_DIFFERENCE_2049_NONCLAIM.csv",
            euler_rows,
        ),
        (
            "COPY2049_1_wep_RAB_finite_residuals",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2049_RAB_FINITE_RESIDUAL_ROWS_NONCLAIM.csv",
            finite_rows,
        ),
        (
            "COPY2049_2_rab_next",
            QUEUE / "JR2049_MINIMAL_RADIAL_ACTION_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY"})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    euler_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    euler_verdict = next(row for row in euler_rows if row["row_id"] == "ECO2049_5_verdict")
    derivation_verdict = next(row for row in derivation_rows if row["row_id"] == "DER2049_5_verdict")
    source_verdict = next(row for row in source_rows if row["row_id"] == "SRCMAP2049_5_verdict")
    finite_verdict = next(row for row in finite_rows if row["row_id"] == "RAB2049_VERDICT")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2049_VERDICT")
    variable_gate = next(row for row in gates if row["row_id"] == "GATE2049_0_variables")
    gr_gate = next(row for row in gates if row["row_id"] == "GATE2049_6_local_GR_Newton")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2049_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2049_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2049_02_coordinates_ready", euler_verdict["status"] == "COORDINATES_READY_EULER_PAIR_MISSING", "Euler variables are ready but parent pair missing"))
    checks.append(("VAL2049_03_RAB_not_derived", derivation_verdict["status"] == "NOT_DERIVED_CURRENT_CORPUS", "R_AB=0 is not promoted"))
    checks.append(("VAL2049_04_source_map_missing", source_verdict["status"] == "SOURCE_MAP_NOT_DERIVED", "source/no-charge map remains missing"))
    checks.append(("VAL2049_05_finite_rows_nonclaim", finite_verdict["status"] == "STAGED_NOT_SCOREABLE", "finite R_AB rows staged but not scoreable"))
    checks.append(("VAL2049_06_runner_rejects", runner_verdict["verdict"] == "RAB_EULER_GATE_BLOCKED_NONCLAIM", "runner rejects derivation and score claims"))
    checks.append(("VAL2049_07_only_identity_gate_passes", variable_gate["status"] == "PASS_NONCLAIM", "only exact variable identity passes, nonclaim"))
    checks.append(("VAL2049_08_local_GR_blocked", gr_gate["status"] == "FAIL_BLOCKED", "local-GR/Newton gate remains blocked"))
    checks.append(("VAL2049_09_next_selected", next_rows_[0]["target_id"] == "NEXT2049_0_2050", "2050 minimal radial action target selected"))
    checks.append(("VAL2049_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2049_11_no_formalization_2049_artifacts", not formalization_has_2049_artifacts(), "no 2049 artifacts were written under formalization-workbench"))
    checks.append(("VAL2049_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2049_OVERALL", overall_ok, "2049 builds the Euler-difference contract and finite R_AB residual fallback without promoting local GR"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    euler_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2049 Y5 R2FR Motion-Load Parent Euler Difference Or R_AB Finite Residual",
        "",
        "## Current Verdict",
        "",
        "2049 does not derive `R_AB=0`, but it converts the missing theorem into the exact parent-Euler object we now need. In the motion-load coframe use `x=ln(T)` and `y=ln(sqrt(S))`; then `C_R=ln(T^2S)=2(x+y)` and `J_q=T sqrt(S)`. A serious GR reduction must make the Euler pair for `x` and `y` force this combination, not merely impose `T^2S=1`.",
        "",
        "The current corpus still lacks the parent radial action and source/no-charge certificates. Therefore `R_AB=0`, `p=1`, `beta=1`, and local GR/Newton remain unclaimed. The fallback finite `R_AB` residual branch is now staged with source, boundary, PPN, R10, clock and orbital slots, but it is not scoreable until theorem-zero or numeric/source-backed rows exist.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Euler Coordinate Setup",
        md_table(euler_rows, ["row_id", "object", "formula", "status", "if_closed", "blocker", "claim_allowed"]),
        "## R_AB Derivation Routes",
        md_table(derivation_rows, ["row_id", "route", "statement", "status", "if_closed", "blocker", "claim_allowed"]),
        "## Source Map Certificates",
        md_table(source_rows, ["row_id", "component", "definition", "status", "needed_next", "claim_allowed"]),
        "## Finite R_AB Residual Fallback",
        md_table(finite_rows, ["row_id", "symbol", "units", "definition", "status", "observable_links", "claim_rule", "ready_for_scoring", "claim_allowed"]),
        "## Runner Refusals",
        md_table(runner, ["run_id", "input_id", "attempted", "verdict", "reason", "score_attempted", "claim_allowed"]),
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
    euler_rows = euler_coordinate_rows()
    derivation_rows = derivation_route_rows()
    source_rows = source_map_certificate_rows()
    finite_rows = finite_residual_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2049_SOURCE_REGISTER.csv",
        "euler": OUT / "P8_Y5_PARENT_QLOC_2049_EULER_COORDINATE_SETUP.csv",
        "derivation": OUT / "P8_Y5_PARENT_QLOC_2049_RAB_DERIVATION_ROUTES.csv",
        "source": OUT / "P8_Y5_PARENT_QLOC_2049_SOURCE_MAP_CERTIFICATES.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2049_FINITE_RAB_RESIDUAL_ROWS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2049_RUNNER_REFUSALS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2049_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2049_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2049_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2049_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2049_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["euler"], euler_rows)
    write_csv(paths["derivation"], derivation_rows)
    write_csv(paths["source"], source_rows)
    write_csv(paths["finite"], finite_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(euler_rows, finite_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, euler_rows, derivation_rows, source_rows, finite_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, euler_rows, derivation_rows, source_rows, finite_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, euler_rows, derivation_rows, source_rows, finite_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
