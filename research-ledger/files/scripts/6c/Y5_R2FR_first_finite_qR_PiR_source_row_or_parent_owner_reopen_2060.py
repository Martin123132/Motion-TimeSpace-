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


DOC = ROOT / "2060-Y5-R2FR-first-finite-qR-PiR-source-row-or-parent-owner-reopen.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"


def path_in(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def formalization_has_2060_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2060-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2060*",
            "*Y5_R2FR_first_finite_qR_PiR_source_row_or_parent_owner_reopen_2060*",
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
            "SRC2060_00_2059_doc",
            ROOT / "2059-Y5-R2FR-local-closure-scorecard-and-finite-residual-acquisition-pack.md",
            ["PRI2059_0_qR_PiR_mass_tail", "NEXT2059_0_2060", "CLOSURE_CONTROL_READY_FINITE_SCORING_BLOCKED"],
            "2059 handoff selects the first finite q_R/Pi_R row and refuses closure-as-GR.",
        ),
        (
            "SRC2060_01_2059_next",
            OUT / "P8_Y5_PARENT_QLOC_2059_NEXT_TARGET.csv",
            ["NEXT2059_0_2060", "q_R/Pi_R source schema", "same-frame source mass"],
            "machine-readable 2060 target.",
        ),
        (
            "SRC2060_02_2059_priority",
            OUT / "P8_Y5_PARENT_QLOC_2059_FINITE_ACQUISITION_PRIORITIES.csv",
            ["PRI2059_0_qR_PiR_mass_tail", "MISSING_QR_OR_PIR_VALUE", "MISSING_ABSOLUTE_TAIL_BUDGET"],
            "finite acquisition priority ladder.",
        ),
        (
            "SRC2060_03_2054_source_rows",
            OUT / "P8_Y5_PARENT_QLOC_2054_QR_PROFILE_SOURCE_ROWS_NONCLAIM.csv",
            ["QRP2054_0_areal_profile", "QRP2054_1_PiR_boundary", "QRP2054_4_same_frame_source_mass"],
            "q_R/Pi_R profile source-row contract.",
        ),
        (
            "SRC2060_04_2055_runner",
            OUT / "P8_Y5_PARENT_QLOC_2055_PIR_WR_RUNNER.csv",
            ["RUN2055_VERDICT", "MISSING_PIR_VALUE", "MISSING_OMEGA_W"],
            "Pi_R-to-q_R symbolic conversion runner.",
        ),
        (
            "SRC2060_05_2056_refined",
            OUT / "P8_Y5_PARENT_QLOC_2056_PROFILE_UPDATE_NONCLAIM.csv",
            ["OPR2056_1_qR_refined", "q_R^PPN=Pi_R/(N_sphere Z_R_infty r_s)", "MISSING_TAIL_BUDGET"],
            "refined finite kinetic conversion row.",
        ),
        (
            "SRC2060_06_2053_bound",
            OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv",
            ["QB2053_0_areal_qR_conservative", "6.7e-05", "CONDITIONAL_BOUND_ROW_NONCLAIM"],
            "Cassini-backed external q_R guard, not an MTS prediction.",
        ),
        (
            "SRC2060_07_2058_gates",
            OUT / "P8_Y5_PARENT_QLOC_2058_FINITE_ACQUISITION_GATES.csv",
            ["FAG2058_1_qR_PiR", "FAG2058_6_same_frame_mass", "FAG2058_7_tail_budget"],
            "strict finite acquisition gates.",
        ),
        (
            "SRC2060_08_1639_blockers",
            OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
            ["NRB1639_1_same_frame_mass", "MISSING_PARENT_SOURCE_MASS_CALIBRATION", "NRB1639_4_no_cancellation_budget"],
            "older source-mass and tail blocker ledger.",
        ),
        (
            "SRC2060_09_1872_abs_tail",
            OUT / "P8_Y5_PARENT_QLOC_1872_ABSOLUTE_TAIL_BOUND_INPUTS_NONCLAIM.csv",
            ["ABI1872_1_PiR", "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM", "ABI1872_4_no_cancellation"],
            "absolute local residual inputs and tail guard.",
        ),
        (
            "SRC2060_10_06_boundary",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Q_R = -Pi_R", "Pi_R = source reciprocal momentum/charge", "Pi_R = 0 -> Q_R = 0"],
            "original reciprocal charge boundary relation.",
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


def classify_path(path: Path) -> str:
    if path_in(path, OUT):
        return "mts_residuals_generated"
    if path_in(path, SOURCE_WEIGHT_DOCS):
        return "source_weight_docs"
    if path_in(path, BRANCH_WEP):
        return "wep_branch_copy"
    if path_in(path, QUEUE):
        return "rab_acquisition_queue"
    for name in ["accepted", "raw", "docs", "external"]:
        directory = RAB_SECTOR / name
        if path_in(path, directory):
            return f"rab_{name}"
    if path_in(path, RAB_SECTOR):
        return "rab_other"
    return "other"


def row_identifier(row: dict[str, str]) -> str:
    for key in ["row_id", "run_id", "target_id", "input_id", "blocker_id", "check_id", "copy_id", "source_id", "template_id"]:
        value = str(row.get(key, "")).strip()
        if value:
            return value
    return "MISSING_ROW_ID"


def row_blob(row: dict[str, object]) -> str:
    return " | ".join(str(value) for value in row.values())


def has_missing_marker(row: dict[str, object]) -> bool:
    return "MISSING_" in row_blob(row)


def truthy(row: dict[str, object], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"true", "1", "yes", "pass", "ready"}


def has_source_path(row: dict[str, object]) -> bool:
    for key in ["source_path", "local_path", "file_path", "source"]:
        value = str(row.get(key, "")).strip()
        if not value or value.startswith("MISSING_"):
            continue
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        if candidate.exists():
            return True
    return False


def relevant_scan_row(row: dict[str, str]) -> bool:
    blob = row_blob(row).lower()
    tokens = [
        "q_r",
        "q_r^ppn",
        "pir",
        "pi_r",
        "same-frame",
        "same_frame",
        "r_s",
        "tail_budget",
        "b_tail",
        "c_r",
        "cassini",
    ]
    return any(token in blob for token in tokens)


def validate_candidate_row(path: Path, row: dict[str, str]) -> dict[str, object]:
    intake_class = classify_path(path)
    row_id = row_identifier(row)
    blob = row_blob(row)
    lower_blob = blob.lower()
    missing = has_missing_marker(row)
    ready_flag = truthy(row, "ready_for_scoring") or truthy(row, "accepted_for_scoring") or truthy(row, "valid_prediction_row")
    source_path_exists = has_source_path(row)
    has_qr = "q_r" in lower_blob or "q_r^ppn" in lower_blob or "q_r_hat" in lower_blob
    has_pir = "pi_r" in lower_blob or "pir" in lower_blob
    has_mass = "same-frame" in lower_blob or "same_frame" in lower_blob or "r_s" in lower_blob
    has_tail = "tail" in lower_blob or "b_tail" in lower_blob
    live_intake = intake_class in {"rab_accepted", "rab_raw"}
    reasons: list[str] = []
    if not live_intake:
        reasons.append("SOURCE_CLASS_NOT_LIVE_ACCEPTED_INTAKE")
    if intake_class.endswith("docs") or intake_class == "source_weight_docs":
        reasons.append("TEMPLATE_OR_DOCS_ROW")
    if missing:
        reasons.append("MISSING_MARKER_PRESENT")
    if not source_path_exists:
        reasons.append("SOURCE_PATH_NOT_CONFIRMED_FOR_ROW")
    if not ready_flag:
        reasons.append("READY_OR_ACCEPTED_FLAG_FALSE_OR_ABSENT")
    if not (has_qr or has_pir):
        reasons.append("NO_QR_OR_PIR_SYMBOL")
    if not has_mass:
        reasons.append("SAME_FRAME_RS_NOT_PRESENT")
    if not has_tail:
        reasons.append("TAIL_BUDGET_NOT_PRESENT")
    status = "ACCEPT_NONCLAIM_REVIEW" if not reasons else "REJECT"
    row_out = base_row()
    row_out.update(
        {
            "scan_id": f"SCAN2060_{intake_class}_{path.stem}_{row_id}"[:220],
            "intake_class": intake_class,
            "file_path": str(path),
            "row_id": row_id,
            "status": status,
            "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_READY_WITH_SOURCE_PATH",
            "has_qR": has_qr,
            "has_PiR": has_pir,
            "has_same_frame_rs": has_mass,
            "has_tail_budget": has_tail,
            "source_path_exists": source_path_exists,
            "ready_flag": ready_flag,
            "accepted_for_scoring": status == "ACCEPT_NONCLAIM_REVIEW",
            "claim_allowed": False,
        }
    )
    return row_out


def live_row_scan_rows() -> list[dict[str, object]]:
    seed_paths = [
        OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv",
        OUT / "P8_Y5_PARENT_QLOC_2054_QR_PROFILE_SOURCE_ROWS_NONCLAIM.csv",
        OUT / "P8_Y5_PARENT_QLOC_2055_PIR_WR_RUNNER.csv",
        OUT / "P8_Y5_PARENT_QLOC_2056_PROFILE_UPDATE_NONCLAIM.csv",
        OUT / "P8_Y5_PARENT_QLOC_2057_STRICT_FINITE_SOURCE_SCHEMA.csv",
        OUT / "P8_Y5_PARENT_QLOC_2058_FINITE_ACQUISITION_GATES.csv",
        OUT / "P8_Y5_PARENT_QLOC_2059_FINITE_ACQUISITION_PRIORITIES.csv",
        OUT / "P8_Y5_PARENT_QLOC_2059_DRY_RUNNER.csv",
        OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1872_ABSOLUTE_TAIL_BOUND_INPUTS_NONCLAIM.csv",
    ]
    scan_dirs = [RAB_SECTOR / "docs", RAB_SECTOR / "raw", RAB_SECTOR / "accepted"]
    paths: list[Path] = [path for path in seed_paths if path.exists()]
    for directory in scan_dirs:
        if directory.exists():
            paths.extend(sorted(directory.glob("*.csv")))
    results: list[dict[str, object]] = []
    for path in sorted(set(paths), key=lambda item: str(item).lower()):
        if "2060" in path.name:
            continue
        try:
            rows = read_csv(path)
        except Exception:
            continue
        for row in rows:
            if relevant_scan_row(row):
                results.append(validate_candidate_row(path, row))
    if not results:
        row = base_row()
        row.update(
            {
                "scan_id": "SCAN2060_NO_RELEVANT_ROWS",
                "intake_class": "all_scan_dirs",
                "file_path": ";".join(str(path) for path in seed_paths + scan_dirs),
                "row_id": "none",
                "status": "NO_RELEVANT_ROWS_FOUND",
                "reasons": "no q_R/Pi_R/same-frame/tail rows found in scan dirs",
                "accepted_for_scoring": False,
                "claim_allowed": False,
            }
        )
        return [row]
    accepted = [row for row in results if row["status"] == "ACCEPT_NONCLAIM_REVIEW"]
    summary = base_row()
    summary.update(
        {
            "scan_id": "SCAN2060_SUMMARY",
            "intake_class": "summary",
            "file_path": ";".join(str(path) for path in seed_paths + scan_dirs),
            "row_id": "summary",
            "status": "NO_ACCEPTED_FINITE_QR_PIR_ROW" if not accepted else "ACCEPTED_ROWS_REQUIRE_REVIEW",
            "reasons": "representative rejects retained; full row count captured in candidate_rows_scanned",
            "has_qR": True,
            "has_PiR": True,
            "has_same_frame_rs": True,
            "has_tail_budget": True,
            "source_path_exists": any(bool(row.get("source_path_exists", False)) for row in results),
            "ready_flag": any(bool(row.get("ready_flag", False)) for row in results),
            "candidate_rows_scanned": len(results),
            "accepted_candidate_rows": len(accepted),
            "accepted_for_scoring": False,
            "claim_allowed": False,
        }
    )
    rejected_examples = [row for row in results if row["status"] != "ACCEPT_NONCLAIM_REVIEW"][:200]
    return [summary] + accepted + rejected_examples


def source_row_schema_rows() -> list[dict[str, object]]:
    data = [
        (
            "SRCROW2060_0_direct_qR",
            "direct_q_R_PPN",
            "q_R^PPN",
            "dimensionless",
            "q_R^PPN numeric value or theorem-zero certificate; source path; equation anchor; same observed-frame convention",
            "score variable is q_R^PPN itself",
            "MISSING_QR_VALUE_OR_ZERO_THEOREM",
        ),
        (
            "SRCROW2060_1_PiR_chain",
            "Pi_R_boundary_chain",
            "Pi_R;N_sphere;Z_R_infty;r_s",
            "boundary-current units plus dimensionless normalizations and length r_s",
            "Pi_R source/bound or zero theorem; N_sphere; Z_R_infty; same-frame r_s=2GM_obs/c^2; sign/orientation convention",
            "q_R^PPN = Pi_R/(N_sphere Z_R_infty r_s)",
            "MISSING_PIR_VALUE_OR_ZERO_THEOREM;MISSING_Z_R_INFTY;MISSING_N_SPHERE;MISSING_SAME_FRAME_RS",
        ),
        (
            "SRCROW2060_2_same_frame_rs",
            "same_frame_mass",
            "r_s",
            "length",
            "source mass calibration from the same parent coframe/readout used by photons and local clocks",
            "r_s cannot be borrowed from observed Newtonian GM to prove Newtonian/GR reduction",
            "MISSING_PARENT_SOURCE_MASS_CALIBRATION",
        ),
        (
            "SRCROW2060_3_absolute_tail",
            "absolute_tail_budget",
            "B_tail_abs",
            "dimensionless",
            "|delta_tail|+|delta_gauge|+|delta_readout|+|delta_source| component theorem-zero or numeric bounds",
            "subtract B_tail_abs from the Cassini envelope before accepting q_R/Pi_R",
            "MISSING_ABSOLUTE_TAIL_BUDGET",
        ),
        (
            "SRCROW2060_4_no_cancellation",
            "no_cancellation_vector",
            "q_R^PPN;B_tail_abs",
            "dimensionless",
            "evaluate |q_R^PPN| + B_tail_abs, or prove orthogonal zero components; never use signed cancellation",
            "guard condition: |q_R^PPN| + B_tail_abs <= 6.70e-05",
            "MISSING_ABSOLUTE_PRODUCT_GUARD",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, row_type, symbols, units, required_inputs, scoring_formula, current_blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "row_type": row_type,
                "symbols": symbols,
                "units": units,
                "required_inputs": required_inputs,
                "scoring_formula": scoring_formula,
                "current_blocker": current_blocker,
                "source_ready_schema": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def candidate_review_rows(scan_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    accepted = [row for row in scan_rows if row["status"] == "ACCEPT_NONCLAIM_REVIEW"]
    summary = next((row for row in scan_rows if row.get("scan_id") == "SCAN2060_SUMMARY"), {})
    scanned_count = int(summary.get("candidate_rows_scanned", len(scan_rows)))
    accepted_count = int(summary.get("accepted_candidate_rows", len(accepted)))
    rows: list[dict[str, object]] = []
    row = base_row()
    row.update(
        {
            "review_id": "REVIEW2060_0_live_scan_summary",
            "candidate_rows_scanned": scanned_count,
            "accepted_candidate_rows": accepted_count,
            "status": "NO_ACCEPTED_FINITE_QR_PIR_ROW" if accepted_count == 0 else "ACCEPTED_ROWS_REQUIRE_HUMAN_REVIEW",
            "dominant_rejection": "generated/templates/missing markers/source path or ready flag absent",
            "claim_allowed": False,
        }
    )
    rows.append(row)
    blockers = [
        ("REVIEW2060_1_qR", "q_R^PPN", "no accepted direct q_R^PPN value or theorem-zero row found"),
        ("REVIEW2060_2_PiR", "Pi_R", "no accepted Pi_R value/bound/zero theorem with N_sphere Z_R_infty r_s chain found"),
        ("REVIEW2060_3_mass", "same-frame r_s", "same-frame parent source mass remains missing"),
        ("REVIEW2060_4_tail", "absolute tail budget", "component zero/bounds remain missing"),
    ]
    for review_id, quantity, finding in blockers:
        row = base_row()
        row.update(
            {
                "review_id": review_id,
                "candidate_rows_scanned": scanned_count,
                "accepted_candidate_rows": len([scan for scan in accepted if quantity.lower() in row_blob(scan).lower()]),
                "status": "BLOCKED",
                "quantity": quantity,
                "finding": finding,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def cassini_dry_run_rows(scan_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    bound = cassini_bound()
    accepted = [row for row in scan_rows if row["status"] == "ACCEPT_NONCLAIM_REVIEW"]
    missing_inputs = [
        "MISSING_QR_OR_PIR_VALUE",
        "MISSING_Z_R_INFTY_OR_N_SPHERE_IF_PIR_CHAIN",
        "MISSING_SAME_FRAME_RS",
        "MISSING_ABSOLUTE_TAIL_BUDGET",
        "MISSING_NO_CANCELLATION_VECTOR_VALUE",
    ]
    data = [
        (
            "RUN2060_0_external_bound_loaded",
            "Cassini q_R guard",
            "|q_R^PPN| + B_tail_abs <= 6.70e-05",
            "BOUND_AVAILABLE_NONCLAIM",
            "external bound exists but is not an MTS prediction",
            False,
        ),
        (
            "RUN2060_1_direct_qR",
            "direct q_R^PPN score",
            "|q_R^PPN| + B_tail_abs <= 6.70e-05",
            "REFUSED_MISSING_QR",
            "no accepted direct q_R^PPN source row or zero theorem found",
            False,
        ),
        (
            "RUN2060_2_PiR_chain",
            "Pi_R conversion score",
            "|Pi_R/(N_sphere Z_R_infty r_s)| + B_tail_abs <= 6.70e-05",
            "REFUSED_MISSING_PIR_CHAIN",
            "Pi_R/N_sphere/Z_R_infty/same-frame r_s chain is not filled",
            False,
        ),
        (
            "RUN2060_3_tail_guard",
            "tail/readout/gauge/source residual guard",
            "absolute component sum only; no signed cancellation credit",
            "REFUSED_MISSING_TAIL_BUDGET",
            "absolute tail vector is missing",
            False,
        ),
        (
            "RUN2060_VERDICT",
            "first finite q_R/Pi_R row",
            "score only after all source inputs are numeric or theorem-zero and sourced",
            "FIRST_FINITE_QR_PIR_ROW_NOT_SCOREABLE",
            "no accepted live source row was found; closure remains a control, not a derived-GR claim",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, formula, verdict, reason, accepted_for_scoring in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "formula": formula,
                "cassini_abs_bound": bound,
                "accepted_live_rows": len(accepted),
                "missing_inputs": ";".join(missing_inputs),
                "verdict": verdict,
                "reason": reason,
                "accepted_for_scoring": accepted_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def parent_owner_reopen_gate_rows(scan_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    owner_candidates = [
        row
        for row in scan_rows
        if ("l_core" in row_blob(row).lower() or "h_core" in row_blob(row).lower())
        and row["status"] == "ACCEPT_NONCLAIM_REVIEW"
    ]
    data = [
        (
            "POG2060_0_new_parent_input",
            "concrete parent L_core/H_core radial-cell owner supplied after 2059",
            "REQUIRED_FOR_REOPEN",
            "BLOCKED",
            "no accepted live row contains a concrete sourced L_core/H_core owner",
        ),
        (
            "POG2060_1_no_repeat_AP1265",
            "do not repeat AP1265/radial-cell owner without new parent action input",
            "POLICY_GUARD",
            "PASS_GUARD_ACTIVE",
            "2060 does not use the closure branch as a parent proof",
        ),
        (
            "POG2060_2_owner_candidate_count",
            "accepted owner candidate count",
            "SCAN_RESULT",
            "BLOCKED" if not owner_candidates else "REVIEW_REQUIRED",
            f"accepted_owner_candidates={len(owner_candidates)}",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, role, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "role": role,
                "status": status,
                "detail": detail,
                "parent_reopen_allowed": False if status.startswith("BLOCKED") or "GUARD" in status else False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2060_0_source_row", "finite q_R/Pi_R source row exists", "FAIL_BLOCKED", "no accepted live q_R/Pi_R row was found"),
        ("GATE2060_1_Cassini_score", "Cassini score allowed", "FAIL_BLOCKED", "bound exists but q_R/Pi_R prediction and tails are missing"),
        ("GATE2060_2_parent_reopen", "parent owner route reopened", "FAIL_BLOCKED", "no concrete new L_core/H_core radial-cell owner input"),
        ("GATE2060_3_local_GR", "derived local GR/Newton claim", "FAIL_BLOCKED", "closure remains a control and finite residual row remains unfilled"),
        ("GATE2060_4_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "no formalization-workbench edit is needed or made"),
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
            "DEC2060_0_live_row",
            "NO_LIVE_SOURCE_ROW_FOUND",
            "The scan finds generated contracts/templates and blocker rows, not an accepted finite q_R/Pi_R input.",
        ),
        (
            "DEC2060_1_scoring",
            "CASSINI_DRY_RUN_REFUSED",
            "The Cassini guard is usable only after q_R or Pi_R-chain, same-frame r_s, and absolute tails are sourced.",
        ),
        (
            "DEC2060_2_parent_reopen",
            "PARENT_OWNER_REOPEN_DENIED",
            "No new concrete L_core/H_core radial-cell owner was supplied, so the derivation route cannot be reopened by repetition.",
        ),
        (
            "DEC2060_3_next",
            "DERIVATION_FIRST_NEXT",
            "The least-scrutiny route is now a Pi_R/Q_R boundary-current zero theorem, with finite source-row acquisition as fallback.",
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
            "target_id": "NEXT2060_0_2061",
            "target_doc": "2061-Y5-R2FR-PiR-boundary-current-zero-theorem-or-CR-profile-first-row.md",
            "objective": "try to derive Pi_R=0/Q_R=0 from the parent boundary-current grammar; if that fails, produce the first finite C_R/q_R profile source row with same-frame r_s and absolute tails",
            "must_include": "boundary variation; worldtube orientation; no boundary/corner R_AB functional; Q_R=-Pi_R sign and units; no-cancellation vector; Cassini dry-run refusal until source inputs close",
            "excluded": "claiming Cassini/local-GR pass; using template rows; borrowing observed GM as proof of same-frame source mass; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    schema_rows: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2060_0_source_weight_schema",
            SOURCE_WEIGHT_DOCS / "AFRAME_QR_PIR_2060_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            schema_rows,
        ),
        (
            "COPY2060_1_wep_live_scan",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2060_LIVE_ROW_SCAN_NONCLAIM.csv",
            scan_rows,
        ),
        (
            "COPY2060_2_wep_cassini_dry",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2060_CASSINI_DRY_RUN_NONCLAIM.csv",
            dry_rows,
        ),
        (
            "COPY2060_3_queue_next",
            QUEUE / "JR2060_PIR_ZERO_THEOREM_OR_FIRST_PROFILE_ROW_NEXT_NONCLAIM.csv",
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
    scan_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    review_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    scan_ok = len(scan_rows) > 0 and all(not bool(row.get("accepted_for_scoring", False)) for row in scan_rows)
    schema_ok = all(not bool(row.get("ready_for_scoring", False)) for row in schema_rows) and {
        "SRCROW2060_0_direct_qR",
        "SRCROW2060_1_PiR_chain",
        "SRCROW2060_2_same_frame_rs",
        "SRCROW2060_3_absolute_tail",
        "SRCROW2060_4_no_cancellation",
    }.issubset({str(row["row_id"]) for row in schema_rows})
    review_ok = review_rows[0]["status"] == "NO_ACCEPTED_FINITE_QR_PIR_ROW"
    verdict = next(row for row in dry_rows if row["run_id"] == "RUN2060_VERDICT")
    dry_ok = verdict["verdict"] == "FIRST_FINITE_QR_PIR_ROW_NOT_SCOREABLE" and not bool(verdict["accepted_for_scoring"])
    parent_ok = all(not bool(row.get("parent_reopen_allowed", False)) for row in parent_rows)
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2060_0_2061"
    no_claim = all(not bool(row.get("claim_allowed", False)) for group in [sources, scan_rows, schema_rows, review_rows, dry_rows, parent_rows, gates, next_rows_] for row in group)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2060_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2060_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2060_02_live_scan_nonclaim", scan_ok, "live row scan ran and accepted no source row for scoring"))
    checks.append(("VAL2060_03_source_schema", schema_ok, "q_R/Pi_R same-frame r_s tail and no-cancellation contract exists"))
    checks.append(("VAL2060_04_candidate_review", review_ok, "candidate review records no accepted finite q_R/Pi_R row"))
    checks.append(("VAL2060_05_cassini_dry_refusal", dry_ok, "Cassini dry run refuses scoring"))
    checks.append(("VAL2060_06_parent_reopen_blocked", parent_ok, "parent L_core/H_core reopen remains blocked"))
    checks.append(("VAL2060_07_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2060_08_next_selected", next_ok, "2061 Pi_R boundary-current theorem target selected"))
    checks.append(("VAL2060_09_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2060_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2060_11_no_formalization_artifacts", not formalization_has_2060_artifacts(), "no 2060 artifacts were written under formalization-workbench"))
    checks.append(("VAL2060_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2060_OVERALL", overall, "2060 installs the first finite q_R/Pi_R source-row contract and keeps all local claims blocked"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    review_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2060 Y5 R2FR First Finite q_R/Pi_R Source Row Or Parent Owner Reopen",
        "",
        "## Current Verdict",
        "",
        "2060 does not find a live, accepted finite `q_R^PPN` or `Pi_R` source row. The corpus contains useful symbolic contracts, Cassini guard rows, and blocker ledgers, but the first scoreable local residual is still missing.",
        "",
        "The first finite source-row contract is now explicit: either source `q_R^PPN` directly, or source `Pi_R`, `N_sphere`, `Z_R_infty`, and same-frame `r_s` so that `q_R^PPN = Pi_R/(N_sphere Z_R_infty r_s)`. In both lanes an absolute tail/readout/gauge/source budget must be supplied, and scoring uses no signed cancellation credit.",
        "",
        "The parent-owner route is not reopened. No new concrete parent `L_core/H_core` radial-cell owner is present, so repeating the closure/radial-cell story would be circular. Closure remains a control branch, not derived local GR/Newton.",
        "",
        "No local-GR/Newton, PPN, Cassini, R10, clock, orbital, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Live Row Scan",
        md_table(scan_rows, ["scan_id", "intake_class", "file_path", "row_id", "status", "reasons", "has_qR", "has_PiR", "has_same_frame_rs", "has_tail_budget", "source_path_exists", "ready_flag", "accepted_for_scoring"]),
        "## q_R/Pi_R Source Row Schema",
        md_table(schema_rows, ["row_id", "row_type", "symbols", "units", "required_inputs", "scoring_formula", "current_blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Candidate Review",
        md_table(review_rows, ["review_id", "quantity", "candidate_rows_scanned", "accepted_candidate_rows", "status", "finding", "dominant_rejection", "claim_allowed"]),
        "## Cassini Dry Run",
        md_table(dry_rows, ["run_id", "target", "formula", "cassini_abs_bound", "accepted_live_rows", "missing_inputs", "verdict", "reason", "accepted_for_scoring", "claim_allowed"]),
        "## Parent Owner Reopen Gate",
        md_table(parent_rows, ["row_id", "clause", "role", "status", "detail", "parent_reopen_allowed", "claim_allowed"]),
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
    scan_rows = live_row_scan_rows()
    schema_rows = source_row_schema_rows()
    review_rows = candidate_review_rows(scan_rows)
    dry_rows = cassini_dry_run_rows(scan_rows)
    parent_rows = parent_owner_reopen_gate_rows(scan_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2060_SOURCE_REGISTER.csv",
        "scan": OUT / "P8_Y5_PARENT_QLOC_2060_LIVE_ROW_SCAN.csv",
        "schema": OUT / "P8_Y5_PARENT_QLOC_2060_QR_PIR_SOURCE_ROW_SCHEMA.csv",
        "review": OUT / "P8_Y5_PARENT_QLOC_2060_CANDIDATE_ROW_REVIEW.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2060_CASSINI_DRY_RUN.csv",
        "parent": OUT / "P8_Y5_PARENT_QLOC_2060_PARENT_OWNER_REOPEN_GATE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2060_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2060_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2060_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2060_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2060_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["scan"], scan_rows)
    write_csv(paths["schema"], schema_rows)
    write_csv(paths["review"], review_rows)
    write_csv(paths["dry"], dry_rows)
    write_csv(paths["parent"], parent_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(schema_rows, scan_rows, dry_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, scan_rows, schema_rows, review_rows, dry_rows, parent_rows, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, scan_rows, schema_rows, review_rows, dry_rows, parent_rows, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, scan_rows, schema_rows, review_rows, dry_rows, parent_rows, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
