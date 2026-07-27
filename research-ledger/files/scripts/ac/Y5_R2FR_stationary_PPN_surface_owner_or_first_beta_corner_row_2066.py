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


DOC = ROOT / "2066-Y5-R2FR-stationary-PPN-surface-owner-or-first-beta-corner-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2066_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2066-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2066*",
            "*Y5_R2FR_stationary_PPN_surface_owner_or_first_beta_corner_row_2066*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2066_00_2065_doc",
            ROOT / "2065-Y5-R2FR-actual-worldtube-surface-class-or-regulator-joint-ledger.md",
            ["NEXT2065_0_2066", "stationary spatial annulus", "beta_corner_i"],
            "2065 handoff into stationary PPN surface owner or first beta_corner row.",
        ),
        (
            "SRC2066_01_2065_next",
            OUT / "P8_Y5_PARENT_QLOC_2065_NEXT_TARGET.csv",
            ["NEXT2065_0_2066", "D_stat", "first beta_corner row"],
            "machine-readable 2066 target.",
        ),
        (
            "SRC2066_02_2065_requirements",
            OUT / "P8_Y5_PARENT_QLOC_2065_ACTUAL_SURFACE_REQUIREMENTS.csv",
            ["ASR2065_2_source_selector", "ASR2065_4_stationary_slice", "MISSING_STATIONARY_SLICE_THEOREM"],
            "actual surface owner requirements from 2065.",
        ),
        (
            "SRC2066_03_2065_joint_ledger",
            OUT / "P8_Y5_PARENT_QLOC_2065_REGULATOR_JOINT_LEDGER_SCHEMA.csv",
            ["RJL2065_2_time_caps", "RJL2065_3_source_worldtube_endpoints", "RJL2065_7_reference_readout_join"],
            "joint families that block the annulus proof.",
        ),
        (
            "SRC2066_04_2065_beta_rows",
            OUT / "P8_Y5_PARENT_QLOC_2065_BETA_CORNER_PLACEHOLDER_ROWS.csv",
            ["BCP2065_1_beta_time_caps", "BCP2065_6_no_cancellation_join", "MISSING_STATIONARY_SLICE_THEOREM_OR_CAP_BETA"],
            "beta_corner placeholder rows to refine in 2066.",
        ),
        (
            "SRC2066_05_1016_worldtube_selector",
            ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            ["PSC1016_3_support_selector", "PST1016_0_selector_lemma", "PST1016_5_verdict"],
            "conditional source-worldtube selector and current failure.",
        ),
        (
            "SRC2066_06_worldtube_glue",
            OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            ["W504_0_worldtube_setup", "W504_4_worldtube_source_measure_glue", "W504_5_calibration_and_limits"],
            "worldtube/exterior-annulus setup and measured-mass glue debt.",
        ),
        (
            "SRC2066_07_1002_stationary_tau_doc",
            ROOT / "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md",
            ["STA1002_2_stationary_generator", "TPS1002_1_stationary_tau_zero_switch", "DEC1002_0_theorem_not_closed"],
            "stationary tau theorem attempt and guardrail against stationary-by-assumption.",
        ),
        (
            "SRC2066_08_tau_contract",
            OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            ["TGC685_1_Killing_stationary_route", "TGC685_6_verdict", "blocked_nonclaim"],
            "tau generator contract: same tau across source, charge, clock, boundary and orbit remains blocked.",
        ),
        (
            "SRC2066_09_selector_to_tau",
            OUT / "P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv",
            ["STT687_3_Killing_upgrade", "STT687_5_verdict", "failed_for_claim"],
            "domain selector does not yet force a stationary Killing generator.",
        ),
        (
            "SRC2066_10_1001_surface_doc",
            ROOT / "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
            ["RSA1001_1_surface_class", "MISSING_CLOSED_BREF_AND_CORNER_CERTIFICATE", "zero-by-boundary-silence and zero-by-fixed-radius are rejected"],
            "fixed-radius/surface shortcut guardrail.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def stationary_surface_owner_rows() -> list[dict[str, object]]:
    data = [
        (
            "SSO2066_0_surface_id",
            "SURF_PPN_STAT_ANNULUS_2066",
            "defined candidate",
            "the PPN/local residual is evaluated on a stationary spatial annulus rather than a finite-time slab",
            "DEFINED_CANDIDATE_NOT_PARENT_SIGNED",
            "naming the surface is useful but does not prove action/readout/source ownership",
            False,
        ),
        (
            "SSO2066_1_domain_Dstat",
            "D_stat",
            "D_stat := Sigma_tau intersect (exterior(W_source)) intersect {R_in <= r <= R_out}",
            "boundary S = S_out union (-S_in) when Sigma_tau is stationary and W_source is compact",
            "CONDITIONAL_DEFINITION_AVAILABLE",
            "this is the clean annulus object to ask the parent theory to own",
            False,
        ),
        (
            "SSO2066_2_outer_surface",
            "S_out",
            "readout/linking surface at R_out in the same observed frame",
            "smooth closed two-sphere if parent readout fixes R_out before fitting",
            "MISSING_READOUT_SURFACE_OWNER",
            "outer geometry is easy; readout ownership remains unsigned",
            False,
        ),
        (
            "SSO2066_3_inner_source_surface",
            "S_in",
            "source-linking surface around W_source = closure(supp J_H[tau])",
            "smooth closed component if source support is compact/regular and parent-owned",
            "MISSING_PARENT_SOURCE_WORLDTUBE_OWNER",
            "inherits PSC1016/W504 source-measure debt",
            False,
        ),
        (
            "SSO2066_4_stationary_slice",
            "Sigma_tau",
            "observed stationary hypersurface with L_tau g_obs = 0 and tau fixed across source/charge/readout",
            "removes finite time caps if parent-signed",
            "MISSING_STATIONARY_TAU_KILLING_OWNER",
            "1002/685/687 block stationary-by-assumption",
            False,
        ),
        (
            "SSO2066_5_no_caps",
            "C_time_caps",
            "no finite-time cap faces are present in a true stationary spatial-annulus calculation",
            "beta_corner_time_caps=0 follows only after SSO2066_4",
            "CONDITIONAL_ZERO_WAITING_ON_STATIONARY_OWNER",
            "this is the nearest almost-win in the surface branch",
            False,
        ),
        (
            "SSO2066_6_no_regulator_seams",
            "C_regulator",
            "no cutoff, excision, smoothing, patch, or reference seam changes the boundary class",
            "if any seam exists, it needs an R_AB-silent theorem or beta_corner_i row",
            "MISSING_REGULATOR_SEAM_CERTIFICATE",
            "no ledger row proves absence yet",
            False,
        ),
        (
            "SSO2066_7_action_readout_source_equivalence",
            "same surface object",
            "the annulus used in the variational boundary term is the same object used in q_R/PPN readout and source normalization",
            "prevents proving a theorem for the wrong surface",
            "MISSING_ACTION_READOUT_SOURCE_EQUIVALENCE",
            "essential before local-GR promotion",
            False,
        ),
        (
            "SSO2066_8_verdict",
            "stationary PPN surface owner",
            "SSO2066_0 through SSO2066_7 must be parent-signed to set Pi_R^corner=0",
            "current MTS has the best candidate surface but not the owner theorem",
            "FAIL_CURRENT_CLAIM_SURFACE_OWNER_UNSIGNED",
            "move to stationary tau/Killing owner or beta_time_caps source row",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, definition, implication, status, note, accepted in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "definition": definition,
                "implication": implication,
                "status": status,
                "note": note,
                "parent_signed": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def time_cap_zero_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "TCZ2066_0_geometry_lemma",
            "finite-time cap absence",
            "If the local branch is formulated directly on a stationary spatial hypersurface Sigma_tau, D_stat has no initial/final time faces.",
            "beta_corner_time_caps=0 as a geometry theorem",
            "EXACT_IF_STATIONARY_SPATIAL_REDUCTION_PARENT_SIGNED",
            "mathematically clean",
            False,
        ),
        (
            "TCZ2066_1_stationary_tau",
            "L_tau g_obs=0",
            "tau must be the parent-owned observed Killing generator, not a clock/gauge choice or selector label.",
            "attaches spatial annulus to actual PPN branch",
            "MISSING_STATIONARY_TAU_KILLING_OWNER",
            "1002/685/687 reject stationarity-by-assumption",
            False,
        ),
        (
            "TCZ2066_2_same_tau",
            "same tau across sectors",
            "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs.",
            "prevents removing caps in one frame while scoring in another",
            "MISSING_SAME_TAU_LOCK",
            "TGC685_6 verdict remains blocked",
            False,
        ),
        (
            "TCZ2066_3_source_endpoint",
            "source-worldtube endpoints",
            "even if time caps are absent, source boundary/endpoints must not re-enter through finite source-worldtube slabs.",
            "keeps C_source_caps separate from C_time_caps",
            "MISSING_SOURCE_ENDPOINT_LEDGER",
            "source support remains conditional",
            False,
        ),
        (
            "TCZ2066_4_verdict",
            "beta_time_caps zero",
            "beta_time_caps=0 is available only as a conditional theorem.",
            "do not score Pi_R^corner yet",
            "CONDITIONAL_ZERO_NOT_ARENA_CERTIFIED",
            "first beta row must stay nonclaim",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, target, statement, implication, status, note, accepted in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "target": target,
                "statement": statement,
                "implication": implication,
                "status": status,
                "note": note,
                "accepted_as_zero": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def first_beta_corner_rows() -> list[dict[str, object]]:
    data = [
        (
            "FBC2066_0_beta_time_caps_zero_switch",
            "beta_corner_time_caps_zero",
            "theorem_zero=true iff stationary_spatial_reduction_owner=true and same_tau_lock=true",
            "boolean theorem gate",
            "stationary tau/Killing owner; same tau lock; no finite-time slab usage",
            "MISSING_STATIONARY_TAU_KILLING_OWNER",
            False,
        ),
        (
            "FBC2066_1_beta_time_caps_abs",
            "beta_corner_time_caps_abs",
            "abs(beta_corner_time_caps) * W_time_caps",
            "boundary-current units",
            "numeric beta_corner_time_caps bound/value or theorem-zero plus source path and weight",
            "MISSING_BETA_TIME_CAPS_NUMERIC_OR_ZERO_THEOREM",
            False,
        ),
        (
            "FBC2066_2_epsilon_tau_bridge",
            "epsilon_nonstationary_tau_to_beta_time_caps",
            "beta_corner_time_caps_abs <= C_cap * epsilon_nonstationary_tau if C_cap, epsilon, and W_time_caps are sourced",
            "boundary-current units",
            "epsilon_nonstationary_tau; C_cap; W_time_caps; same-frame units; source path",
            "MISSING_C_CAP_AND_EPSILON_TAU_NORMALIZATION",
            False,
        ),
        (
            "FBC2066_3_source_endpoint_separation",
            "beta_corner_source_caps_separate",
            "source-worldtube endpoint terms are not folded into beta_time_caps",
            "boundary-current units",
            "source endpoint ledger and separate beta/source-zero theorem",
            "MISSING_SOURCE_ENDPOINT_LEDGER",
            False,
        ),
        (
            "FBC2066_4_no_cancellation_join",
            "Pi_R_corner_abs_total",
            "Pi_R^corner_abs = beta_time_caps_abs + sum_other abs(beta_corner_i) W_i",
            "boundary-current units",
            "all active/unknown corner families zeroed or bounded by absolute values",
            "MISSING_OTHER_BETA_CORNER_ROWS",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, units, required_input, blocker, ready_for_scoring in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "units": units,
                "required_input": required_input,
                "blocker": blocker,
                "source_ready_schema": True,
                "ready_for_scoring": ready_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows(
    owners: list[dict[str, object]],
    cap_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    owner_verdict = next(row for row in owners if row["row_id"] == "SSO2066_8_verdict")
    cap_verdict = next(row for row in cap_rows if row["row_id"] == "TCZ2066_4_verdict")
    rows_data = [
        (
            "RUN2066_0_surface_definition",
            "SURF_PPN_STAT_ANNULUS_2066",
            "CANDIDATE_DEFINED",
            "surface_id and D_stat candidate are explicit",
            False,
        ),
        (
            "RUN2066_1_owner_attempt",
            "stationary PPN surface owner",
            "REFUSED_OWNER_UNSIGNED",
            str(owner_verdict["status"]),
            False,
        ),
        (
            "RUN2066_2_time_cap_zero",
            "beta_time_caps=0",
            "CONDITIONAL_ZERO_NOT_SCORABLE",
            str(cap_verdict["status"]),
            False,
        ),
        (
            "RUN2066_3_first_beta_row",
            "beta_time_caps source row",
            "SCHEMA_WRITTEN_VALUES_MISSING",
            f"rows={len(beta_rows)}; no numeric/theorem-zero row accepted",
            False,
        ),
        (
            "RUN2066_VERDICT",
            "stationary PPN surface owner or first beta_corner row",
            "SURFACE_OWNER_FAILS_FIRST_BETA_ROW_STAGED_NONCLAIM",
            "2067 should attack stationary tau/Killing ownership or source epsilon_tau -> beta_time_caps",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict, reason, accepted in rows_data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_scoring": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2066_0_surface_owner",
            "stationary annulus is actual parent-owned PPN surface",
            "FAIL_BLOCKED",
            "candidate surface is defined but source/tau/readout/action ownership is unsigned",
        ),
        (
            "GATE2066_1_stationary_tau",
            "L_tau g_obs=0 and same tau lock",
            "FAIL_BLOCKED",
            "1002/685/687 block stationary-by-assumption and selector-to-Killing jump",
        ),
        (
            "GATE2066_2_time_caps",
            "beta_time_caps=0",
            "FAIL_BLOCKED",
            "conditional on stationary spatial reduction owner",
        ),
        (
            "GATE2066_3_beta_time_caps",
            "finite beta_time_caps row score",
            "FAIL_BLOCKED",
            "no numeric coefficient, no C_cap epsilon_tau bridge, no source-backed weight",
        ),
        (
            "GATE2066_4_source_endpoint",
            "source-worldtube endpoints separated or zeroed",
            "FAIL_BLOCKED",
            "source endpoint ledger remains missing",
        ),
        (
            "GATE2066_5_PiRtot_qR",
            "Pi_R^tot_abs and q_R PPN score",
            "FAIL_BLOCKED",
            "other beta_corner rows, Pi_R components, and normalization are incomplete",
        ),
        (
            "GATE2066_6_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "no formalization-workbench edit is made",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2066_0_result",
            "SURFACE_ID_AND_DSTAT_NOW_EXACT_CANDIDATES",
            "The branch now has a precise annulus object to ask the parent action to own.",
        ),
        (
            "DEC2066_1_best_news",
            "TIME_CAPS_HAVE_A_CLEAN_CONDITIONAL_ZERO",
            "If stationary spatial reduction is parent-owned, beta_time_caps disappears without a fitted cancellation.",
        ),
        (
            "DEC2066_2_hard_block",
            "STATIONARY_TAU_KILLING_OWNER_IS_THE_NEXT BOTTLENECK",
            "The existing corpus explicitly says selector silence and tau labels do not prove L_tau g_obs=0.",
        ),
        (
            "DEC2066_3_no_claim",
            "DO_NOT_CLAIM_CORNER_ZERO_OR_LOCAL_GR",
            "The current result is a route map and first beta row schema, not a scored theorem.",
        ),
        (
            "DEC2066_4_next",
            "ATTACK_STATIONARY_TAU_OR_SOURCE_EPSILON_TAU_BETA_ROW",
            "2067 should either derive the Killing/same-tau owner or fill the epsilon_nonstationary_tau to beta_time_caps bound.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2066_0_2067",
            "target_doc": "2067-Y5-R2FR-stationary-tau-Killing-owner-or-beta-time-caps-bound.md",
            "objective": "derive the parent-owned stationary tau/Killing generator and same-tau lock needed to remove time caps, or source the first epsilon_nonstationary_tau to beta_time_caps finite bound",
            "must_include": "tau_obs owner; L_tau g_obs=0; same tau source/charge/clock/boundary/orbit lock; selector-to-Killing failure modes; epsilon_nonstationary_tau bridge; C_cap and W_time_caps units; no-cancellation Pi_Rcorner join",
            "excluded": "stationary-by-assumption; clock/lapse gauge shortcut; selector silence as Killing proof; fitted cancellation; local-GR/PPN scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    owners: list[dict[str, object]],
    cap_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2066_0_source_weight_surface_owner",
            SOURCE_WEIGHT_DOCS / "AFRAME_STATIONARY_PPN_SURFACE_OWNER_2066_CONDITIONAL_NONCLAIM.csv",
            owners,
        ),
        (
            "COPY2066_1_source_weight_time_caps",
            SOURCE_WEIGHT_DOCS / "AFRAME_TIME_CAP_ZERO_2066_CONDITIONAL_NONCLAIM.csv",
            cap_rows,
        ),
        (
            "COPY2066_2_source_weight_beta_time_caps",
            SOURCE_WEIGHT_DOCS / "AFRAME_BETA_TIME_CAPS_2066_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            beta_rows,
        ),
        (
            "COPY2066_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2066_STATIONARY_SURFACE_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2066_4_queue_next",
            QUEUE / "JR2066_STATIONARY_TAU_OR_BETA_TIME_CAPS_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY", "claim_allowed": False})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    owners: list[dict[str, object]],
    cap_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    owner_verdict = next(row for row in owners if row["row_id"] == "SSO2066_8_verdict")
    owner_ok = (
        any(row["row_id"] == "SSO2066_0_surface_id" for row in owners)
        and any(row["row_id"] == "SSO2066_1_domain_Dstat" for row in owners)
        and owner_verdict["status"] == "FAIL_CURRENT_CLAIM_SURFACE_OWNER_UNSIGNED"
        and all(not bool(row["parent_signed"]) for row in owners)
    )
    cap_verdict = next(row for row in cap_rows if row["row_id"] == "TCZ2066_4_verdict")
    cap_ok = (
        any(row["row_id"] == "TCZ2066_0_geometry_lemma" for row in cap_rows)
        and cap_verdict["status"] == "CONDITIONAL_ZERO_NOT_ARENA_CERTIFIED"
        and all(not bool(row["accepted_as_zero"]) for row in cap_rows)
    )
    beta_ok = len(beta_rows) >= 5 and all(bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in beta_rows)
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2066_VERDICT")
    dry_ok = dry_verdict["verdict"] == "SURFACE_OWNER_FAILS_FIRST_BETA_ROW_STAGED_NONCLAIM"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2066_0_2067"
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, owners, cap_rows, beta_rows, dry_rows_, gates, next_rows_]
        for row in group
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2066_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2066_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2066_02_surface_owner", owner_ok, "surface_id and D_stat are defined but owner theorem fails"))
    checks.append(("VAL2066_03_time_cap_zero", cap_ok, "time-cap zero lemma is conditional and not arena-certified"))
    checks.append(("VAL2066_04_first_beta_row", beta_ok, "first beta_time_caps rows are source-ready but unscored"))
    checks.append(("VAL2066_05_dry_verdict", dry_ok, "dry run stages beta row and refuses local/PPN claim"))
    checks.append(("VAL2066_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2066_07_next_selected", next_ok, "2067 stationary tau/Killing owner or beta_time_caps bound target selected"))
    checks.append(("VAL2066_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2066_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2066_10_no_formalization_artifacts", not formalization_has_2066_artifacts(), "no 2066 artifacts were written under formalization-workbench"))
    checks.append(("VAL2066_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2066_OVERALL", overall, "2066 defines the stationary surface candidate and stages first beta_time_caps rows without claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    owners: list[dict[str, object]],
    cap_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2066 Y5 R2FR Stationary PPN Surface Owner Or First Beta Corner Row",
        "",
        "## Current Verdict",
        "",
        "2066 makes the low-scrutiny local route sharper. The exact candidate surface is now `SURF_PPN_STAT_ANNULUS_2066`: a stationary spatial annulus `D_stat = Sigma_tau intersect exterior(W_source) intersect {R_in <= r <= R_out}` with boundary `S_out union (-S_in)`.",
        "",
        "The good news is that finite-time caps have a clean conditional zero. If the parent theory owns the stationary spatial reduction and the same `tau_obs` controls source, charge, clocks, boundary, and readout, then the annulus has no initial/final time faces and `beta_corner_time_caps=0` follows geometrically.",
        "",
        "The bad-but-useful news is that current MTS does not yet sign that owner theorem. Existing source rows already say selector silence is weaker than a Killing generator, and tau labels do not fix clock/Hamiltonian/readout normalization. So the stationary annulus is a precise candidate, not a local-GR/PPN claim.",
        "",
        "The fallback is now concrete: the first `beta_corner` family is `beta_corner_time_caps`, with a zero switch and an `epsilon_nonstationary_tau -> beta_time_caps` bound slot. It is source-ready but not scoreable because `C_cap`, `epsilon_tau`, `W_time_caps`, units, and theorem-zero authority are still missing.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, corner-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Stationary Surface Owner Attempt",
        md_table(owners, ["row_id", "object_id", "definition", "implication", "status", "note", "parent_signed", "claim_allowed"]),
        "## Time-Cap Zero Attempt",
        md_table(cap_rows, ["row_id", "target", "statement", "implication", "status", "note", "accepted_as_zero", "claim_allowed"]),
        "## First Beta Corner Rows",
        md_table(beta_rows, ["row_id", "quantity", "formula", "units", "required_input", "blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Dry Run",
        md_table(dry_rows_, ["run_id", "target", "verdict", "reason", "accepted_for_scoring", "claim_allowed"]),
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
    owners = stationary_surface_owner_rows()
    cap_rows = time_cap_zero_attempt_rows()
    beta_rows = first_beta_corner_rows()
    dry_rows_ = dry_run_rows(owners, cap_rows, beta_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2066_SOURCE_REGISTER.csv",
        "owners": OUT / "P8_Y5_PARENT_QLOC_2066_STATIONARY_SURFACE_OWNER_ATTEMPT.csv",
        "caps": OUT / "P8_Y5_PARENT_QLOC_2066_TIME_CAP_ZERO_ATTEMPT.csv",
        "beta": OUT / "P8_Y5_PARENT_QLOC_2066_FIRST_BETA_CORNER_ROWS.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2066_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2066_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2066_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2066_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2066_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2066_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["owners"], owners)
    write_csv(paths["caps"], cap_rows)
    write_csv(paths["beta"], beta_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(owners, cap_rows, beta_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, owners, cap_rows, beta_rows, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, owners, cap_rows, beta_rows, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, owners, cap_rows, beta_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
