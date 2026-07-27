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


DOC = ROOT / "2054-Y5-R2FR-PPN-gamma-gauge-readout-tail-zero-or-qR-profile-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2054_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2054-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2054*",
            "*Y5_R2FR_PPN_gamma_gauge_readout_tail_zero_or_qR_profile_source_row_2054*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2054_00_2053_doc",
            ROOT / "2053-Y5-R2FR-PPN-gamma-map-from-RAB-profile-or-finite-qR-first-bound.md",
            ["NEXT2053_0_2054", "GUARD2053_0_same_frame_mass", "QB2053_0_areal_qR_conservative"],
            "2053 PPN-gamma map and guard handoff.",
        ),
        (
            "SRC2054_01_2053_next",
            OUT / "P8_Y5_PARENT_QLOC_2053_NEXT_TARGET.csv",
            ["NEXT2053_0_2054", "same-frame M_obs/r_s owner", "q_R profile/Pi_R source row"],
            "machine-readable 2054 target.",
        ),
        (
            "SRC2054_02_2053_guard",
            OUT / "P8_Y5_PARENT_QLOC_2053_GUARD_LEDGER.csv",
            ["GUARD2053_0_same_frame_mass", "MISSING_GAUGE_CONVERSION_PROOF", "MISSING_TAIL_ZERO_OR_BOUNDS"],
            "guard blockers from 2053.",
        ),
        (
            "SRC2054_03_2053_bound",
            OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv",
            ["QB2053_0_areal_qR_conservative", "6.7e-05"],
            "Cassini-backed q_R^PPN bound row.",
        ),
        (
            "SRC2054_04_source_mass_tail",
            OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
            ["NRB1639_1_same_frame_mass", "MISSING_PARENT_SOURCE_MASS_CALIBRATION"],
            "same-frame source-mass and tail blockers.",
        ),
        (
            "SRC2054_05_tail_runner",
            OUT / "P8_Y5_PARENT_QLOC_1583_CASSINI_TAIL_RUNNER.csv",
            ["CTR1583_1_finite_tail_bound", "NOT_RUN_COMPONENTS_MISSING"],
            "tail runner refusal.",
        ),
        (
            "SRC2054_06_tail_zero",
            OUT / "P8_Y5_PARENT_QLOC_2039_TAIL_ZERO_AUDIT.csv",
            ["TZ2039_5_verdict", "FAIL_CURRENT_CLAIM_TAIL_ZERO_NOT_DERIVED"],
            "latest tail-zero audit.",
        ),
        (
            "SRC2054_07_tail_bound_inputs",
            OUT / "P8_Y5_PARENT_QLOC_1872_ABSOLUTE_TAIL_BOUND_INPUTS_NONCLAIM.csv",
            ["ABI1872_1_PiR", "ABI1872_3_gamma_bound", "6.7e-05"],
            "absolute tail/source input ledger.",
        ),
        (
            "SRC2054_08_readout_descent",
            OUT / "P8_Y5_PARENT_QLOC_1675_SOURCE_READOUT_DESCENT_GATE.csv",
            ["SRD1675_5_verdict", "SOURCE_READOUT_DESCENT_NOT_CLOSED"],
            "source/readout descent blocker.",
        ),
        (
            "SRC2054_09_matter_readout",
            OUT / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv",
            ["MRT1802_7_verdict", "FAIL_CURRENT_CLAIM"],
            "matter/readout theorem gate.",
        ),
        (
            "SRC2054_10_variation_before_readout",
            OUT / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
            ["VBR1816_6_verdict", "source-worldtube"],
            "variation-before-readout conditional theorem.",
        ),
        (
            "SRC2054_11_coframe",
            ROOT / "2048-Y5-R2FR-motion-load-coframe-construction-or-CMTS-provenance.md",
            ["MLC2048_2_observed_coframe", "MLC2048_8_verdict"],
            "constructed observed coframe and its parent/readout limitation.",
        ),
        (
            "SRC2054_12_euler_difference",
            ROOT / "2049-Y5-R2FR-motion-load-parent-Euler-difference-or-RAB-finite-residual.md",
            ["ECO2049_4_difference_target", "COORDINATES_READY_EULER_PAIR_MISSING"],
            "parent Euler difference target.",
        ),
        (
            "SRC2054_13_motion_load_noGR",
            ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            ["MPD1859_6_best_surviving_route", "SELECT_PRIMARY"],
            "best noncircular local-GR route.",
        ),
        (
            "SRC2054_14_reciprocity_action",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["W R_AB' = Q_R.", "Asymptotic flatness alone does not kill `Q_R`."],
            "Q_R hair and asymptotic no-go.",
        ),
        (
            "SRC2054_15_source_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Q_R = -Pi_R.", "Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1."],
            "Pi_R boundary momentum conditional route.",
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
            }
        )
        rows.append(row)
    return rows


def guard_closure_rows() -> list[dict[str, object]]:
    data = [
        (
            "GCA2054_0_same_frame_mass",
            "same-frame M_obs/r_s owner",
            "2048 defines L=2GM/(r c^2), but 1639 and orbital ledgers say using observed GM to prove Newton/GR is circular unless the parent source mass is derived.",
            "NOT_CLOSED_SOURCE_MASS_OWNER_MISSING",
            "retain M_obs/r_s as a convention only",
            "derive parent source measure or keep q_R bound symbolic in r_s units",
        ),
        (
            "GCA2054_1_gauge",
            "areal-to-PPN gauge/readout coordinate guard",
            "2053 selected observed areal gauge and 2048 constructs the coframe, but there is no parent theorem that all MTS variables enter Cassini readout through this gauge.",
            "PARTIAL_CONVENTION_NOT_PARENT_CONVERTED",
            "tau_PPN_R=1 remains conditional",
            "prove observed coframe is the public photon/readout metric or add a gauge tail row",
        ),
        (
            "GCA2054_2_readout",
            "photon/ordinary matter readout stability",
            "1675 and 1802 keep matter/readout descent unsigned; 1816 helps only after pure readout typing and no source-only slots are signed.",
            "NOT_CLOSED_READOUT_DESCENT_MISSING",
            "delta_readout cannot be set to zero",
            "derive readout descent or bound delta_readout independently",
        ),
        (
            "GCA2054_3_tail",
            "delta_tail/source/boundary zero-or-bound",
            "2039 and 1583 say tail-zero is conditional and finite tail bound components are missing.",
            "NOT_CLOSED_TAIL_ZERO_OR_BOUND_MISSING",
            "delta_tail stays in the Cassini q_R bound",
            "source Pi_R/W_R/boundary rows or prove no-charge/source neutrality",
        ),
        (
            "GCA2054_4_no_cancellation",
            "absolute residual vector",
            "no-cancellation is already policy-active in 2053 and 1872.",
            "POLICY_ACTIVE",
            "no opposite-sign cancellation credit is allowed",
            "keep each residual component separate in runner rows",
        ),
        (
            "GCA2054_5_verdict",
            "2054 guard closure attempt",
            "No guard closes as a parent-signed theorem in the current corpus; the honest move is source-ready q_R/Pi_R profile rows.",
            "GUARDS_NOT_CLOSED_PROFILE_ROW_REQUIRED",
            "local-GR score remains blocked",
            "write q_R^PPN profile and Pi_R source-row contracts",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, guard, evidence, status, consequence, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "guard": guard,
                "evidence": evidence,
                "status": status,
                "consequence": consequence,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def qR_profile_rows() -> list[dict[str, object]]:
    data = [
        (
            "QRP2054_0_areal_profile",
            "q_R^PPN profile",
            "C_R(r)=q_R^PPN r_s/r + O(r_s^2/r^2) + delta_tail(r)",
            "q_R^PPN numeric value, theorem-zero, or parent source equation; r_s owner; tail budget",
            "MISSING_QR_VALUE_OR_ZERO_THEOREM",
            "6.7e-5",
            "dimensionless",
            "first source-ready profile row for Cassini gamma lane",
        ),
        (
            "QRP2054_1_PiR_boundary",
            "Pi_R boundary momentum",
            "q_R^PPN = k_W Pi_R/r_s + delta_W_sign_units under signed W_R/boundary convention",
            "Pi_R source/bound, W_R asymptotic normalization, boundary orientation, same-frame r_s",
            "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM",
            "|Pi_R| <= (r_s/|k_W|)*(6.7e-5 - residual_budget) if k_W and guards are signed",
            "boundary-current units",
            "connects 06 boundary relation to a bounded PPN amplitude",
        ),
        (
            "QRP2054_2_WR_normalization",
            "W_R/k_W asymptotic normalization",
            "W_R partial_r C_R=Q_R with C_R~q_R^PPN r_s/r fixes the Pi_R-to-q_R conversion only after W_R asymptotics are owned",
            "parent W_R sign, units, asymptotic radial weight, and Q_R=-Pi_R orientation",
            "MISSING_PARENT_SIGN_AND_NORMALIZATION",
            "required before Pi_R row can score",
            "strain-weight units",
            "prevents factor/sign/units mistakes",
        ),
        (
            "QRP2054_3_tail_budget",
            "absolute gamma-tail budget",
            "|delta_tail|+|delta_gauge|+|delta_readout|+|delta_source| <= remaining Cassini envelope",
            "individual theorem-zero or numeric bounds for each tail component",
            "MISSING_TAIL_ZERO_OR_BOUNDS",
            "residual_budget must be subtracted from 6.7e-5 before q_R scoring",
            "dimensionless",
            "enforces no-cancellation policy",
        ),
        (
            "QRP2054_4_same_frame_source_mass",
            "same-frame r_s owner",
            "r_s=2G M_obs/c^2 must come from the same parent source/readout used by the photon metric",
            "parent source-mass calibration or source-normalized Newton proof",
            "MISSING_PARENT_SOURCE_MASS_CALIBRATION",
            "q_R can be bounded dimensionlessly but Pi_R/Mstar conversion cannot score",
            "mass/length",
            "keeps Newton reduction honest",
        ),
        (
            "QRP2054_5_verdict",
            "q_R/Pi_R source-row contract",
            "profile and boundary rows are now source-ready but remain nonclaim and unscored",
            "all missing numeric/theorem-zero inputs are explicit",
            "SOURCE_READY_PROFILE_ROWS_WRITTEN_NONCLAIM",
            "nonclaim",
            "dimensionless/profile/boundary",
            "next target should attack Pi_R/W_R normalization or source mass owner",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, required_inputs, status, bound_or_rule, units, role in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "required_inputs": required_inputs,
                "status": status,
                "bound_or_rule": bound_or_rule,
                "units": units,
                "role": role,
                "source_ready_schema": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows(guard_rows: list[dict[str, object]], profile_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    blocking_guards = [
        row["row_id"]
        for row in guard_rows
        if str(row["status"]).startswith("NOT_CLOSED") or str(row["status"]).startswith("PARTIAL")
    ]
    for profile_row in profile_rows:
        row = base_row()
        row.update(
            {
                "run_id": "RUN_" + str(profile_row["row_id"]),
                "quantity": profile_row["quantity"],
                "source_ready_schema": profile_row["source_ready_schema"],
                "accepted_for_scoring": False,
                "verdict": "SOURCE_ROW_WRITTEN_NONCLAIM" if profile_row["row_id"] != "QRP2054_5_verdict" else "PROFILE_CONTRACT_READY_NONCLAIM",
                "reason": "guard blockers remain: " + ";".join(str(blocker) for blocker in blocking_guards),
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2054_VERDICT",
            "quantity": "PPN_gamma_guard_closure_or_qR_profile",
            "source_ready_schema": True,
            "accepted_for_scoring": False,
            "verdict": "GUARD_CLOSURE_FAILED_QR_PROFILE_ROWS_CREATED_NONCLAIM",
            "reason": "same-frame mass, gauge/readout and tail zero did not close; q_R^PPN/Pi_R source-ready rows created for the next derivation/fill target",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2054_0_guard_audit", "same-frame/gauge/readout/tail guards audited", "PASS_NONCLAIM", "all blockers have source-backed status rows"),
        ("GATE2054_1_profile_rows", "q_R^PPN/Pi_R profile source rows written", "PASS_NONCLAIM", "source-ready schema exists but is not scored"),
        ("GATE2054_2_no_cancellation", "absolute no-cancellation policy retained", "PASS_NONCLAIM", "tail/gauge/readout/source residuals remain separate"),
        ("GATE2054_3_guard_closure", "guards parent-signed and closed", "FAIL_BLOCKED", "source mass, readout and tail zero remain unsigned"),
        ("GATE2054_4_score_qR", "finite q_R prediction scored against Cassini", "FAIL_BLOCKED", "q_R/Pi_R numeric or theorem-zero input missing"),
        ("GATE2054_5_local_GR", "local GR/Newton/beta claimed", "FAIL_BLOCKED", "gamma-bound scaffolding is not a local-GR derivation"),
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
            "DEC2054_0_result",
            "The guard-closure attempt failed, but usefully.",
            "The missing pieces are now not vague: source mass owner, gauge/readout descent, tail/source/boundary zero-or-bound, and Pi_R/W_R normalization.",
        ),
        (
            "DEC2054_1_profile_row",
            "A source-ready q_R^PPN/Pi_R profile contract now exists.",
            "This is what lets future work either derive a zero theorem or fill a numeric/theorem-bound row without changing the scoring rules.",
        ),
        (
            "DEC2054_2_best_next",
            "Attack Pi_R/W_R normalization next.",
            "That is the shortest route from the boundary/no-charge work to an actual q_R amplitude, while source mass/readout stays as a visible guard.",
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
            "target_id": "NEXT2054_0_2055",
            "target_doc": "2055-Y5-R2FR-PiR-boundary-momentum-or-WR-asymptotic-normalization.md",
            "objective": "derive the Pi_R-to-q_R^PPN conversion by fixing boundary orientation, W_R asymptotic normalization and same-frame r_s ownership, or keep the profile row blocked with a symbolic nonclaim bound",
            "must_include": "Q_R=-Pi_R sign and units; W_R partial_r C_R=Q_R asymptotics; k_W normalization; r_s=2GM_obs/c^2 owner; q_R^PPN profile row update; Cassini bound runner refusal/pass logic",
            "excluded": "assuming W_R=r^2 by taste; hiding source mass circularity; scoring symbolic Pi_R; claiming q_R=0/local GR/Newton; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    guard_rows: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2054_0_source_weight_guard_audit",
            SOURCE_WEIGHT_DOCS / "AFRAME_PPN_GAMMA_GUARD_AUDIT_2054_NONCLAIM.csv",
            guard_rows,
        ),
        (
            "COPY2054_1_wep_qR_profile_rows",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2054_QR_PROFILE_SOURCE_ROWS_NONCLAIM.csv",
            profile_rows,
        ),
        (
            "COPY2054_2_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2054_GUARD_PROFILE_RUNNER_NONCLAIM.csv",
            runner,
        ),
        (
            "COPY2054_3_rab_next",
            QUEUE / "JR2054_PIR_WR_NORMALIZATION_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY"})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    guard_verdict = next(row for row in guard_rows if row["row_id"] == "GCA2054_5_verdict")
    profile_verdict = next(row for row in profile_rows if row["row_id"] == "QRP2054_5_verdict")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2054_VERDICT")
    guard_gate = next(row for row in gates if row["row_id"] == "GATE2054_3_guard_closure")
    score_gate = next(row for row in gates if row["row_id"] == "GATE2054_4_score_qR")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2054_5_local_GR")
    no_profile_scored = all(not bool(row.get("ready_for_scoring", False)) for row in profile_rows) and all(
        not bool(row.get("accepted_for_scoring", False)) for row in runner
    )
    required_profile_rows = {"QRP2054_0_areal_profile", "QRP2054_1_PiR_boundary", "QRP2054_2_WR_normalization", "QRP2054_3_tail_budget"}
    profile_coverage = required_profile_rows.issubset({str(row["row_id"]) for row in profile_rows})
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2054_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2054_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2054_02_guards_not_closed", guard_verdict["status"] == "GUARDS_NOT_CLOSED_PROFILE_ROW_REQUIRED", "guard closure correctly fails into profile-row route"))
    checks.append(("VAL2054_03_profile_rows_written", profile_verdict["status"] == "SOURCE_READY_PROFILE_ROWS_WRITTEN_NONCLAIM", "q_R/Pi_R source-ready profile rows written"))
    checks.append(("VAL2054_04_profile_coverage", profile_coverage, "profile, Pi_R, W_R and tail budget rows are present"))
    checks.append(("VAL2054_05_runner_nonclaim", runner_verdict["verdict"] == "GUARD_CLOSURE_FAILED_QR_PROFILE_ROWS_CREATED_NONCLAIM", "runner creates rows but does not score"))
    checks.append(("VAL2054_06_no_profile_scored", no_profile_scored, "no source-ready row is accepted for scoring"))
    checks.append(("VAL2054_07_guard_gate_blocked", guard_gate["status"] == "FAIL_BLOCKED", "guard closure gate remains blocked"))
    checks.append(("VAL2054_08_score_gate_blocked", score_gate["status"] == "FAIL_BLOCKED", "q_R score gate remains blocked"))
    checks.append(("VAL2054_09_local_GR_blocked", local_gate["status"] == "FAIL_BLOCKED", "local GR/Newton claim remains blocked"))
    checks.append(("VAL2054_10_next_selected", next_rows_[0]["target_id"] == "NEXT2054_0_2055", "2055 Pi_R/W_R normalization target selected"))
    checks.append(("VAL2054_11_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2054_12_no_formalization_2054_artifacts", not formalization_has_2054_artifacts(), "no 2054 artifacts were written under formalization-workbench"))
    checks.append(("VAL2054_13_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2054_OVERALL", overall, "2054 audits PPN gamma guards, writes q_R/Pi_R profile rows, and selects Pi_R/W_R normalization next"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2054 Y5 R2FR PPN Gamma Gauge Readout Tail Zero Or q_R Profile Source Row",
        "",
        "## Current Verdict",
        "",
        "2054 tries the honest guard-closure route for the PPN-gamma bridge. It does not close. The observed coframe/gamma map exists, but same-frame source mass ownership, areal-to-PPN readout/gauge descent, and tail/source/boundary zero-or-bound remain unsigned in the current corpus.",
        "",
        "That is not a dead end: the checkpoint converts the failure into source-ready finite rows. We now have a `q_R^PPN` profile contract, a `Pi_R` boundary-momentum contract, a `W_R/k_W` normalization contract, and a tail-budget row tied to the Cassini envelope. These rows are deliberately nonclaim and unscored.",
        "",
        "No `q_R=0`, `R_AB=0`, `p=1`, `beta=1`, local-GR, Newton, PPN pass, GitHub action, or `formalization-workbench` edit is claimed.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Guard Closure Audit",
        md_table(guard_rows, ["row_id", "guard", "evidence", "status", "consequence", "next_action", "claim_allowed"]),
        "## q_R Profile And Pi_R Source Rows",
        md_table(profile_rows, ["row_id", "quantity", "formula", "required_inputs", "status", "bound_or_rule", "units", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Runner",
        md_table(runner, ["run_id", "quantity", "source_ready_schema", "accepted_for_scoring", "verdict", "reason", "claim_allowed"]),
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
    guard_rows = guard_closure_rows()
    profile_rows = qR_profile_rows()
    runner = runner_rows(guard_rows, profile_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2054_SOURCE_REGISTER.csv",
        "guards": OUT / "P8_Y5_PARENT_QLOC_2054_GUARD_CLOSURE_AUDIT.csv",
        "profiles": OUT / "P8_Y5_PARENT_QLOC_2054_QR_PROFILE_SOURCE_ROWS_NONCLAIM.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2054_GUARD_PROFILE_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2054_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2054_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2054_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2054_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2054_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["guards"], guard_rows)
    write_csv(paths["profiles"], profile_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(guard_rows, profile_rows, runner, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, guard_rows, profile_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, guard_rows, profile_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, guard_rows, profile_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
