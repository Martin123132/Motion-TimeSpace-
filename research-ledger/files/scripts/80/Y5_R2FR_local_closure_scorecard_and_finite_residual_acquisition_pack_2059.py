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
    read_csv,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2059-Y5-R2FR-local-closure-scorecard-and-finite-residual-acquisition-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2059_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2059-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2059*",
            "*Y5_R2FR_local_closure_scorecard_and_finite_residual_acquisition_pack_2059*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def cassini_bound() -> float:
    rows = read_csv(OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv")
    for row in rows:
        if row.get("row_id") == "QB2053_0_areal_qR_conservative":
            return float(row["numeric_abs_bound"])
    raise RuntimeError("QB2053_0_areal_qR_conservative not found")


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2059_00_2058_doc",
            ROOT / "2058-Y5-R2FR-parent-radial-cell-owner-or-local-closure-baseline.md",
            ["NEXT2058_0_2059", "local_closure_baseline", "FAG2058_0_C_R_profile"],
            "2058 handoff into closure scorecard and finite acquisition pack.",
        ),
        (
            "SRC2059_01_2058_next",
            OUT / "P8_Y5_PARENT_QLOC_2058_NEXT_TARGET.csv",
            ["NEXT2058_0_2059", "closure branch flags", "finite residual rows from FAG2058"],
            "machine-readable 2059 target.",
        ),
        (
            "SRC2059_02_2058_closure",
            OUT / "P8_Y5_PARENT_QLOC_2058_LOCAL_CLOSURE_BASELINE.csv",
            ["LCB2058_0_branch", "local_closure_baseline", "derived_local_GR"],
            "closure branch flags and hard refusals.",
        ),
        (
            "SRC2059_03_2058_finite",
            OUT / "P8_Y5_PARENT_QLOC_2058_FINITE_ACQUISITION_GATES.csv",
            ["FAG2058_0_C_R_profile", "MISSING_PROFILE_OR_ZERO_THEOREM", "FAG2058_9_q_loc_profile"],
            "finite residual acquisition gates.",
        ),
        (
            "SRC2059_04_2058_runner",
            OUT / "P8_Y5_PARENT_QLOC_2058_BRANCH_RUNNER.csv",
            ["RUN2058_VERDICT", "PARENT_OWNER_NOT_DERIVED_CLOSURE_BASELINE_ONLY"],
            "2058 runner demotion to closure/control.",
        ),
        (
            "SRC2059_05_2053_qR_bound",
            OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv",
            ["QB2053_0_areal_qR_conservative", "6.7e-05", "CONDITIONAL_BOUND_ROW_NONCLAIM"],
            "Cassini-backed q_R^PPN bound row, still nonclaim.",
        ),
        (
            "SRC2059_06_2057_schema",
            OUT / "P8_Y5_PARENT_QLOC_2057_STRICT_FINITE_SOURCE_SCHEMA.csv",
            ["FSR2057_0_ZR_infty", "MISSING_Z_R_INFTY_OR_PARENT_ZERO_THEOREM", "FSR2057_8_q_loc_profile"],
            "strict finite source schema from 2057.",
        ),
        (
            "SRC2059_07_1278_firewall",
            ROOT / "1278-Y5-R10-RAB-explicit-local-closure-runner-and-A511-origin-priority-ladder.md",
            ["local_closure_baseline", "closure_only=true", "BR1278_0_local_closure_baseline"],
            "prior local closure firewall.",
        ),
        (
            "SRC2059_08_2049_finite",
            ROOT / "2049-Y5-R2FR-motion-load-parent-Euler-difference-or-RAB-finite-residual.md",
            ["RAB2049_VERDICT", "STAGED_NOT_SCOREABLE", "MISSING_ARENA_PROJECTIONS"],
            "R2FR finite R_AB residual schema and arena links.",
        ),
        (
            "SRC2059_09_2054_guards",
            ROOT / "2054-Y5-R2FR-PPN-gamma-gauge-readout-tail-zero-or-qR-profile-source-row.md",
            ["QRP2054_0_areal_profile", "QRP2054_1_PiR_boundary", "RUN2054"],
            "q_R/Pi_R guard closure and profile-row source state.",
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


def closure_scorecard_rows() -> list[dict[str, object]]:
    data = [
        (
            "CSC2059_0_branch_flags",
            "all_local_arenas",
            "local_closure_baseline",
            "closure_only=true; derived_local_GR=false; pass_for_claim=false",
            "READY_CONTROL_ONLY",
            "debug local pipeline and compare against GR-like zero residual",
            "using closure as theory evidence",
        ),
        (
            "CSC2059_1_PPN_gamma",
            "PPN_gamma",
            "q_R^PPN=0 by closure assumption",
            "gamma-1 control residual is zero",
            "CONTROL_ONLY_CASSINI_GUARDS_STILL_ACTIVE",
            "check sign/convention of q_R^PPN runner",
            "claiming Cassini pass for MTS",
        ),
        (
            "CSC2059_2_PPN_beta_Newton",
            "PPN_beta;Newton",
            "C_R=0 alone does not prove beta/Newton source normalization",
            "requires parent Euler/source-mass/source-balance gates",
            "CONTROL_ONLY_NOT_A_BETA_PROOF",
            "avoid gamma-only overclaim",
            "promoting p=1/gamma to full GR/Newton",
        ),
        (
            "CSC2059_3_R10",
            "R10_short_range",
            "closure sets local R_AB hair to zero in the benchmark branch",
            "R10 finite-residual branch disabled until source kernels exist",
            "CONTROL_ONLY_NO_ALPHA_SCORE",
            "debug R10 no-signal baseline",
            "treating no residual closure as R10 evidence",
        ),
        (
            "CSC2059_4_clock",
            "clock",
            "closure assumes no local clock/readout regeneration",
            "q_loc/tail/readout profile still missing for finite branch",
            "CONTROL_ONLY_READOUT_GUARD_OPEN",
            "debug clock residual plumbing",
            "claiming clock safety without readout theorem",
        ),
        (
            "CSC2059_5_orbital",
            "orbital",
            "closure assumes source/boundary/orbital readout tails vanish",
            "finite orbital tau kernel and source mass remain missing",
            "CONTROL_ONLY_ORBITAL_GUARD_OPEN",
            "debug orbital zero-residual baseline",
            "claiming orbital pass from closure",
        ),
        (
            "CSC2059_6_q_loc",
            "local_GR_response",
            "closure assumes epsilon_GK_q_loc=0",
            "Gamma/Khat metric-response identity/profile is not filled",
            "CONTROL_ONLY_QLOC_PROFILE_MISSING",
            "keep local response leak visible",
            "hiding q_loc inside closure",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, arena, branch, control_input, status, allowed_use, hard_refusal in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "arena": arena,
                "branch": branch,
                "control_input": control_input,
                "status": status,
                "allowed_use": allowed_use,
                "hard_refusal": hard_refusal,
                "closure_only": True,
                "derived_local_GR": False,
                "accepted_for_scoring": False,
                "pass_for_claim": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_priority_rows() -> list[dict[str, object]]:
    q_bound = cassini_bound()
    data = [
        (
            "PRI2059_0_qR_PiR_mass_tail",
            1,
            "q_R^PPN/Pi_R plus same-frame r_s and absolute tails",
            "PPN_gamma",
            f"first scoreable local finite row must target |q_R^PPN + tails| <= {q_bound:.2e}",
            "FAG2058_1_qR_PiR;FAG2058_5_boundary_tail;FAG2058_6_same_frame_mass;FAG2058_7_tail_budget",
            "MISSING_QR_OR_PIR_VALUE;MISSING_SAME_FRAME_SOURCE_MASS;MISSING_ABSOLUTE_TAIL_BUDGET",
        ),
        (
            "PRI2059_1_C_R_profile",
            2,
            "C_R(r) profile in observed areal gauge",
            "PPN;orbital;clock",
            "profile owns the residual directly and prevents convention drift",
            "FAG2058_0_C_R_profile",
            "MISSING_PROFILE_OR_ZERO_THEOREM",
        ),
        (
            "PRI2059_2_ZR_Nsphere",
            3,
            "Z_R_infty and N_sphere normalization",
            "PPN;R10;orbital",
            "needed to convert Pi_R to q_R^PPN without omega_W handwaving",
            "FAG2058_2_ZR_Nsphere;FSR2057_0_ZR_infty;FSR2057_1_N_sphere",
            "MISSING_Z_R_INFTY_OR_N_SPHERE",
        ),
        (
            "PRI2059_3_tau_PPN",
            4,
            "tau_PPN projection including beta/preferred-frame components",
            "PPN_beta;PPN_alpha",
            "gamma lane alone is not local GR/Newton",
            "FAG2058_8_tau_kernels;FSR2057_6_tau_PPN",
            "MISSING_PPN_PROJECTION",
        ),
        (
            "PRI2059_4_q_loc_profile",
            5,
            "epsilon_GK_q_loc/Gamma-Khat response profile",
            "local_GR;PPN;clock",
            "readout/EFT leakage must be theorem-zero or bounded",
            "FAG2058_9_q_loc_profile;FSR2057_8_q_loc_profile",
            "MISSING_Q_LOC_PROFILE_OR_ZERO",
        ),
        (
            "PRI2059_5_MR2_screening",
            6,
            "M_R^2 or ell_R screened branch",
            "R10;PPN;orbital",
            "only needed if finite kinetic branch is massive/suppressed",
            "FAG2058_3_MR2;FSR2057_2_MR2",
            "MISSING_M_R2_OR_ELL_R",
        ),
        (
            "PRI2059_6_R10_clock_orbital_kernels",
            7,
            "tau_R10/tau_clock/tau_orbital arena kernels",
            "R10;clock;orbital",
            "required before cross-arena tests can be treated as MTS predictions",
            "FAG2058_8_tau_kernels;FSR2057_7_tau_R10_clock_orbital",
            "MISSING_ARENA_PROJECTIONS",
        ),
        (
            "PRI2059_7_source_balance",
            8,
            "S_R[source] and source-balance/no-charge theorem",
            "Newton;WEP;orbital",
            "keeps local vacuum from hiding a source anisotropy",
            "FAG2058_4_source_balance",
            "MISSING_SOURCE_BALANCE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, priority, target, arenas, scoring_rule, source_gate_ids, current_blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "priority": priority,
                "target": target,
                "arenas": arenas,
                "scoring_rule": scoring_rule,
                "source_gate_ids": source_gate_ids,
                "current_blocker": current_blocker,
                "ready_for_scoring": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def no_cancellation_rows() -> list[dict[str, object]]:
    data = [
        ("NC2059_0_vector_norm", "score absolute residual vector components, not tuned sums", "ACTIVE", "all local arenas"),
        ("NC2059_1_qR_tails", "q_R cannot be cancelled by tail/gauge/readout/source terms unless a parent cancellation theorem exists", "ACTIVE", "PPN_gamma"),
        ("NC2059_2_closure_finite", "closure assumptions cannot be mixed with finite residual rows", "ACTIVE", "all local arenas"),
        ("NC2059_3_qRhat_converter", "legacy q_R_hat/s_R converters cannot be scored with areal q_R^PPN without signed convention map", "ACTIVE", "PPN_gamma"),
        ("NC2059_4_common_mode", "same-frame mass/source normalization cannot be absorbed into measured G without a source-mass certificate", "ACTIVE", "Newton;PPN"),
        ("NC2059_5_readout", "readout/EFT q_loc leakage must be independently zero or bounded", "ACTIVE", "local_GR;clock;PPN"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, rule, status, arenas in data:
        row = base_row()
        row.update({"row_id": row_id, "rule": rule, "status": status, "arenas": arenas, "claim_allowed": False})
        rows.append(row)
    return rows


def dry_run_rows(
    closure_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    no_cancel_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    blockers = ";".join(row["current_blocker"] for row in priority_rows)
    data = [
        (
            "DRY2059_0_closure_control",
            "local_closure_baseline",
            "ACCEPT_AS_CONTROL_ONLY",
            "closure rows are usable for internal pipeline debugging only",
            False,
        ),
        (
            "DRY2059_1_closure_claim",
            "closure_as_derived_local_GR",
            "REFUSE_PROMOTION",
            "closure_only branch has derived_local_GR=false and pass_for_claim=false",
            False,
        ),
        (
            "DRY2059_2_finite_score",
            "finite_residual_score",
            "REFUSE_MISSING_SOURCE_ROWS",
            blockers,
            False,
        ),
        (
            "DRY2059_3_cassini",
            "Cassini q_R bound",
            "BOUND_AVAILABLE_NONCLAIM",
            f"conservative |q_R^PPN + tails| <= {cassini_bound():.2e}, but q_R/tail/source-mass guards are open",
            False,
        ),
        (
            "DRY2059_4_no_cancellation",
            "no-cancellation guard",
            "ACTIVE",
            f"{len(no_cancel_rows)} absolute-residual rules active",
            False,
        ),
        (
            "DRY2059_VERDICT",
            "2059 local branch runner",
            "CLOSURE_CONTROL_READY_FINITE_SCORING_BLOCKED",
            "closure scorecard ready as nonclaim control; finite residual acquisition pack ready but unfilled",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict, reason, accepted_for_scoring in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_scoring": accepted_for_scoring,
                "closure_rows": len(closure_rows),
                "priority_rows": len(priority_rows),
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2059_0_closure_scorecard", "closure control scorecard exists", "PASS_NONCLAIM", "usable for debugging, not evidence"),
        ("GATE2059_1_finite_pack", "finite residual acquisition pack exists", "PASS_NONCLAIM", "prioritized source rows written, all nonclaim"),
        ("GATE2059_2_cassini_bound", "Cassini q_R bound connected", "PASS_NONCLAIM", "source-backed bound row referenced but guards remain open"),
        ("GATE2059_3_finite_scoring", "finite residual branch scoreable", "FAIL_BLOCKED", "no priority row is source-backed or ready"),
        ("GATE2059_4_derived_local_GR", "derived local GR/Newton claim", "FAIL_BLOCKED", "closure is not derivation and finite rows are missing"),
        ("GATE2059_5_branch_mixing", "branch mixing prevented", "PASS_NONCLAIM", "closure/finite/readout residual lanes separated"),
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
            "DEC2059_0_result",
            "The local branch is now operational as a control, not a claim.",
            "Closure can debug PPN/R10/clock/orbital/Newton pipelines while preserving derived_local_GR=false.",
        ),
        (
            "DEC2059_1_acquisition",
            "The finite residual acquisition path is concrete.",
            "The first serious source target is q_R/Pi_R plus same-frame mass and tail budget, because it directly interfaces with Cassini.",
        ),
        (
            "DEC2059_2_no_cancellation",
            "No-cancellation rules are active before any fit/test.",
            "This prevents a finite residual from being hidden under closure, source mass, gauge, readout, or tail conventions.",
        ),
        (
            "DEC2059_3_next",
            "Next work should fill the first finite residual source row or supply a new parent owner.",
            "Without one of those, further local derivation passes are likely circling rather than progress.",
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
            "target_id": "NEXT2059_0_2060",
            "target_doc": "2060-Y5-R2FR-first-finite-qR-PiR-source-row-or-parent-owner-reopen.md",
            "objective": "try to fill the first finite local residual source row for q_R^PPN/Pi_R with same-frame r_s and tail budget; alternatively reopen derivation only with a concrete parent L_core/H_core radial-cell owner",
            "must_include": "q_R/Pi_R source schema; same-frame source mass; absolute tail vector; Cassini guard; no-cancellation check; source-path validation; dry-run refusal if placeholders remain",
            "excluded": "claiming closure as derived GR; scoring Cassini without q_R prediction; using template rows; repeating AP1265/radial-cell owner without new parent action; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    closure_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    no_cancel_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2059_0_source_weight_acquisition",
            SOURCE_WEIGHT_DOCS / "AFRAME_LOCAL_FINITE_ACQUISITION_2059_NONCLAIM.csv",
            priority_rows,
        ),
        (
            "COPY2059_1_wep_closure_scorecard",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2059_LOCAL_CLOSURE_SCORECARD_NONCLAIM.csv",
            closure_rows,
        ),
        (
            "COPY2059_2_wep_no_cancellation",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2059_NO_CANCELLATION_VECTOR_NONCLAIM.csv",
            no_cancel_rows,
        ),
        (
            "COPY2059_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2059_DRY_RUNNER_NONCLAIM.csv",
            dry_rows,
        ),
        (
            "COPY2059_4_rab_next",
            QUEUE / "JR2059_FIRST_QR_PIR_SOURCE_ROW_NEXT_NONCLAIM.csv",
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
    closure_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    no_cancel_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    closure_ok = len(closure_rows) >= 6 and all(bool(row["closure_only"]) and not bool(row["derived_local_GR"]) and not bool(row["pass_for_claim"]) for row in closure_rows)
    priority_ok = len(priority_rows) >= 8 and priority_rows[0]["row_id"] == "PRI2059_0_qR_PiR_mass_tail"
    no_cancel_ok = len(no_cancel_rows) >= 6 and all(row["status"] == "ACTIVE" for row in no_cancel_rows)
    dry_verdict = next(row for row in dry_rows if row["run_id"] == "DRY2059_VERDICT")
    finite_gate = next(row for row in gates if row["row_id"] == "GATE2059_3_finite_scoring")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2059_4_derived_local_GR")
    no_score = all(not bool(row.get("accepted_for_scoring", False)) for row in dry_rows) and all(
        not bool(row.get("ready_for_scoring", False)) for row in priority_rows
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2059_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2059_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2059_02_closure_scorecard", closure_ok, "closure scorecard rows are nonclaim controls"))
    checks.append(("VAL2059_03_priority_order", priority_ok, "finite acquisition priorities start with q_R/Pi_R mass/tail row"))
    checks.append(("VAL2059_04_no_cancellation", no_cancel_ok, "no-cancellation vector is active"))
    checks.append(("VAL2059_05_dry_runner", dry_verdict["verdict"] == "CLOSURE_CONTROL_READY_FINITE_SCORING_BLOCKED", "dry runner refuses finite scoring"))
    checks.append(("VAL2059_06_no_score", no_score, "no dry-run or priority row is accepted for scoring"))
    checks.append(("VAL2059_07_finite_gate_blocked", finite_gate["status"] == "FAIL_BLOCKED", "finite residual scoring gate remains blocked"))
    checks.append(("VAL2059_08_local_GR_blocked", local_gate["status"] == "FAIL_BLOCKED", "derived local GR/Newton claim remains blocked"))
    checks.append(("VAL2059_09_next_selected", next_rows_[0]["target_id"] == "NEXT2059_0_2060", "2060 first q_R/Pi_R source-row target selected"))
    checks.append(("VAL2059_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2059_11_no_formalization_2059_artifacts", not formalization_has_2059_artifacts(), "no 2059 artifacts were written under formalization-workbench"))
    checks.append(("VAL2059_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2059_OVERALL", overall, "2059 builds closure control scorecard and finite residual acquisition pack while blocking all claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    priority_rows: list[dict[str, object]],
    no_cancel_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2059 Y5 R2FR Local Closure Scorecard And Finite Residual Acquisition Pack",
        "",
        "## Current Verdict",
        "",
        "2059 makes the local branch operational without overclaiming. The closure branch is now a nonclaim control scorecard across PPN, R10, clock, orbital, Newton and local-response arenas. It can debug pipelines, but every row keeps `closure_only=true`, `derived_local_GR=false`, and `pass_for_claim=false`.",
        "",
        "The finite residual path is now an acquisition programme rather than fog. The first priority is a source-backed `q_R^PPN/Pi_R` row with same-frame `r_s` and an absolute tail budget, because that is the shortest path into the Cassini guard. Other rows cover `C_R(r)`, `Z_R_infty/N_sphere`, `M_R^2`, `tau` kernels, source balance and `q_loc` readout leakage.",
        "",
        "No local-GR/Newton, PPN, R10, clock, orbital, closure, or finite-residual pass is claim-valid. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Closure Control Scorecard",
        md_table(closure_rows, ["row_id", "arena", "branch", "control_input", "status", "allowed_use", "hard_refusal", "closure_only", "derived_local_GR", "accepted_for_scoring", "pass_for_claim", "claim_allowed"]),
        "## Finite Residual Acquisition Priorities",
        md_table(priority_rows, ["row_id", "priority", "target", "arenas", "scoring_rule", "source_gate_ids", "current_blocker", "ready_for_scoring", "valid_for_claim", "claim_allowed"]),
        "## No-Cancellation Vector",
        md_table(no_cancel_rows, ["row_id", "rule", "status", "arenas", "claim_allowed"]),
        "## Dry-Run Runner",
        md_table(dry_rows, ["run_id", "target", "verdict", "reason", "accepted_for_scoring", "closure_rows", "priority_rows", "claim_allowed"]),
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
    closure_rows = closure_scorecard_rows()
    priority_rows = finite_priority_rows()
    no_cancel_rows = no_cancellation_rows()
    dry_rows = dry_run_rows(closure_rows, priority_rows, no_cancel_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2059_SOURCE_REGISTER.csv",
        "closure": OUT / "P8_Y5_PARENT_QLOC_2059_CLOSURE_SCORECARD.csv",
        "priorities": OUT / "P8_Y5_PARENT_QLOC_2059_FINITE_ACQUISITION_PRIORITIES.csv",
        "no_cancel": OUT / "P8_Y5_PARENT_QLOC_2059_NO_CANCELLATION_VECTOR.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2059_DRY_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2059_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2059_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2059_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2059_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2059_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["closure"], closure_rows)
    write_csv(paths["priorities"], priority_rows)
    write_csv(paths["no_cancel"], no_cancel_rows)
    write_csv(paths["dry"], dry_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(closure_rows, priority_rows, no_cancel_rows, dry_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, closure_rows, priority_rows, no_cancel_rows, dry_rows, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, closure_rows, priority_rows, no_cancel_rows, dry_rows, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, closure_rows, priority_rows, no_cancel_rows, dry_rows, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
