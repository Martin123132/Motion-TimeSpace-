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


DOC = ROOT / "2055-Y5-R2FR-PiR-boundary-momentum-or-WR-asymptotic-normalization.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2055_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2055-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2055*",
            "*Y5_R2FR_PiR_boundary_momentum_or_WR_asymptotic_normalization_2055*",
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
            "SRC2055_00_2054_doc",
            ROOT / "2054-Y5-R2FR-PPN-gamma-gauge-readout-tail-zero-or-qR-profile-source-row.md",
            ["NEXT2054_0_2055", "QRP2054_1_PiR_boundary", "QRP2054_2_WR_normalization"],
            "2054 handoff into Pi_R/W_R normalization.",
        ),
        (
            "SRC2055_01_2054_next",
            OUT / "P8_Y5_PARENT_QLOC_2054_NEXT_TARGET.csv",
            ["NEXT2054_0_2055", "Q_R=-Pi_R sign and units", "W_R partial_r C_R=Q_R asymptotics"],
            "machine-readable 2055 target.",
        ),
        (
            "SRC2055_02_2054_profiles",
            OUT / "P8_Y5_PARENT_QLOC_2054_QR_PROFILE_SOURCE_ROWS_NONCLAIM.csv",
            ["QRP2054_1_PiR_boundary", "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM", "QRP2054_2_WR_normalization"],
            "q_R/Pi_R source-row contract to update.",
        ),
        (
            "SRC2055_03_2053_bound",
            OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv",
            ["QB2053_0_areal_qR_conservative", "6.7e-05"],
            "Cassini q_R^PPN nonclaim bound.",
        ),
        (
            "SRC2055_04_reciprocity_action",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].", "W R_AB' = Q_R.", "R_AB ~ Q_R/r."],
            "reciprocal current and W_R equation.",
        ),
        (
            "SRC2055_05_source_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["delta S_boundary = [W R_AB' + Pi_R] delta R_AB|_surface.", "Q_R = -Pi_R."],
            "boundary variation sign convention source.",
        ),
        (
            "SRC2055_06_Hcore_boundary",
            ROOT / "1253-Y5-R10-reciprocal-Hcore-boundary-charge-derivation-attempt.md",
            ["BCA1253_0_QR_current_constant", "for W=r^2", "MISSING_BOUNDARY_CHARGE_CLASS"],
            "prior boundary-charge and W=r^2 analogy audit.",
        ),
        (
            "SRC2055_07_qRhat_template",
            ROOT / "1254-Y5-R10-boundary-flux-source-template-or-phenomenological-qRhat-row.md",
        ["q_R_hat = Q_R c^2/(G M_source)", "BFC1254_1_raw_boundary_flux", "TEMPLATE_ONLY_NO_ROW"],
            "older q_Rhat flux intake template and source-mass warning.",
        ),
        (
            "SRC2055_08_source_mass_tail",
            OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
            ["NRB1639_0_tail_normalization", "NRB1639_1_same_frame_mass", "MISSING_PARENT_SOURCE_MASS_CALIBRATION"],
            "tail normalization and same-frame source mass blockers.",
        ),
        (
            "SRC2055_09_tail_inputs",
            OUT / "P8_Y5_PARENT_QLOC_1872_ABSOLUTE_TAIL_BOUND_INPUTS_NONCLAIM.csv",
            ["ABI1872_1_PiR", "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM", "ABI1872_3_gamma_bound"],
            "absolute tail/Pi_R input blocker rows.",
        ),
        (
            "SRC2055_10_wr_contract",
            OUT / "P8_Y5_PARENT_QLOC_1886_FINITE_WR_BETAW_ROW_CONTRACT.csv",
            ["FWR1886_1_wR", "numeric source/action weight coefficient or theorem-zero", "tau_PPN"],
            "finite weight-row contract; no symbolic unity shortcuts.",
        ),
        (
            "SRC2055_11_wr_template",
            OUT / "P8_Y5_PARENT_QLOC_1886_WR_BETAW_CANDIDATE_TEMPLATE_NONCLAIM.csv",
            ["WR1886_TEMPLATE_FINITE_SOURCE_WEIGHT", "MISSING_NUMERIC_SOURCE_WEIGHT"],
            "finite W-like source-weight template remains placeholder.",
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


def conversion_derivation_rows() -> list[dict[str, object]]:
    q_bound = cassini_bound()
    data = [
        (
            "CONV2055_0_profile",
            "areal profile",
            "C_R(r)=q_R^PPN r_s/r + o(1/r), so partial_r C_R=-q_R^PPN r_s/r^2 + o(1/r^2)",
            "EXACT_ASYMPTOTIC_IF_PROFILE_DEFINED",
            "defines the coefficient Cassini bounds",
            "profile remains unfilled numerically",
        ),
        (
            "CONV2055_1_weight",
            "asymptotic W_R coefficient",
            "omega_W := lim_{r->infinity} W_R(r)/r^2, requiring 0<omega_W<infinity",
            "REQUIRED_NORMALIZATION_NOT_PARENT_SIGNED",
            "separates actual radial measure/weight from a hidden W_R=r^2 assumption",
            "omega_W is missing from current corpus",
        ),
        (
            "CONV2055_2_current",
            "current asymptotics",
            "Q_R := W_R partial_r C_R = -omega_W q_R^PPN r_s + o(1)",
            "FORMAL_DERIVATION",
            "maps areal q_R into the conserved reciprocal current once omega_W exists",
            "sign depends on outward/inward convention only through the boundary definition",
        ),
        (
            "CONV2055_3_boundary",
            "boundary momentum convention",
            "delta S_boundary=[W_R partial_r C_R + Pi_R] delta C_R|boundary gives Q_R=-Pi_R",
            "FORMAL_FROM_06_CONVENTION",
            "fixes the 06 sign if the same boundary orientation is parent-owned",
            "worldtube/reference/corner class is still unsigned",
        ),
        (
            "CONV2055_4_combine",
            "Pi_R to q_R^PPN conversion",
            "Pi_R = omega_W q_R^PPN r_s, hence q_R^PPN=Pi_R/(omega_W r_s); equivalently q_R^PPN=k_W Pi_R/r_s with k_W=1/omega_W",
            "CONDITIONAL_CONVERSION_DERIVED_NONCLAIM",
            "repairs the 2054 k_W shorthand by defining the inverse-weight convention",
            "cannot score until Pi_R, omega_W, r_s owner and tails are supplied",
        ),
        (
            "CONV2055_5_Cassini",
            "Cassini symbolic Pi_R bound",
            f"|Pi_R| <= omega_W r_s max(0,{q_bound:.2e}-B_tail) after all tail/gauge/readout/source budgets are absolute-bounded",
            "SYMBOLIC_BOUND_DERIVED_NONCLAIM",
            "turns the q_R Cassini lane into a Pi_R boundary-momentum lane",
            "omega_W, r_s and B_tail are not source-backed values",
        ),
        (
            "CONV2055_6_verdict",
            "2055 conversion result",
            "the Pi_R-to-q_R^PPN algebra is conditionally derived, but W_R asymptotics, Pi_R value, source mass and tails are still missing",
            "CONVERSION_DERIVED_CONDITIONAL_RUNNER_BLOCKED",
            "real progress: the boundary row is now dimensionally/sign explicit",
            "no PPN/local-GR score",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, item, formula, status, meaning, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "formula": formula,
                "status": status,
                "meaning": meaning,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def normalization_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "NORM2055_0_W_equals_r2",
            "W_R=r^2 shortcut",
            "1253 records W=r^2 as an illustrative case where R_AB=R_inf-Q_R/r.",
            "REJECT_AS_PARENT_NORMALIZATION",
            "would set omega_W=1",
            "not parent-signed; cannot use by taste",
        ),
        (
            "NORM2055_1_omegaW",
            "omega_W finite positive",
            "Need lim W_R/r^2 = omega_W from parent radial action/measure.",
            "MISSING_PARENT_SIGN_AND_NORMALIZATION",
            "would make q_R^PPN=Pi_R/(omega_W r_s)",
            "no source path currently supplies omega_W",
        ),
        (
            "NORM2055_2_orientation",
            "Q_R=-Pi_R orientation",
            "06 supplies this sign for the written boundary variation.",
            "CONDITIONAL_SIGN_CONVENTION_AVAILABLE",
            "absolute Cassini bound is sign-insensitive",
            "source-worldtube orientation and reference subtraction still unsigned",
        ),
        (
            "NORM2055_3_same_frame_rs",
            "same-frame r_s owner",
            "r_s=2G M_obs/c^2 must be the same source mass/readout used by the photon metric.",
            "MISSING_PARENT_SOURCE_MASS_CALIBRATION",
            "dimensionless q_R bound can be written; Pi_R bound cannot score",
            "same source-mass circularity as 1639/2054",
        ),
        (
            "NORM2055_4_tail_budget",
            "absolute tail budget",
            "B_tail=|delta_tail|+|delta_gauge|+|delta_readout|+|delta_source| must be zero or bounded before subtracting from Cassini.",
            "MISSING_TAIL_ZERO_OR_BOUNDS",
            "prevents hiding q_R by cancellation",
            "tail components remain missing",
        ),
        (
            "NORM2055_5_verdict",
            "normalization audit",
            "only the formal conversion closes; no numeric/source-backed Pi_R or omega_W row exists.",
            "SYMBOLIC_NONCLAIM_ONLY",
            "keep profile row blocked but sharper",
            "next target should derive omega_W from parent radial measure or write a finite omega_W prior row",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, topic, evidence, status, effect_if_signed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "topic": topic,
                "evidence": evidence,
                "status": status,
                "effect_if_signed": effect_if_signed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def updated_profile_rows() -> list[dict[str, object]]:
    q_bound = cassini_bound()
    data = [
        (
            "UPR2055_0_qR_profile",
            "q_R^PPN",
            "C_R=q_R^PPN r_s/r + o(1/r)",
            f"|q_R^PPN + B_tail_signed| <= {q_bound:.2e}",
            "dimensionless",
            "CONDITIONAL_BOUND_ROW_NONCLAIM",
            "needs q_R prediction/theorem-zero or bounded tails before score",
        ),
        (
            "UPR2055_1_PiR_conversion",
            "Pi_R",
            "Pi_R=omega_W q_R^PPN r_s",
            f"|Pi_R| <= omega_W r_s max(0,{q_bound:.2e}-B_tail_abs)",
            "boundary-current units",
            "SYMBOLIC_BOUND_ROW_NONCLAIM",
            "needs Pi_R value/bound, omega_W, r_s owner and tail budget",
        ),
        (
            "UPR2055_2_kW_converter",
            "k_W",
            "k_W:=1/omega_W so q_R^PPN=k_W Pi_R/r_s",
            "2054 k_W formula is valid only with this inverse-weight definition",
            "inverse strain-weight coefficient",
            "CONVENTION_REPAIRED_NONCLAIM",
            "prevents future k_W/omega_W inversion errors",
        ),
        (
            "UPR2055_3_zero_theorem_lane",
            "Pi_R=0 or q_R^PPN=0",
            "if Pi_R=0 and tails vanish, q_R^PPN=0; with C_R(infinity)=0 the reciprocal current branch gives C_R=0",
            "exact local-GR gamma lane only after source neutrality/boundary no-charge is parent-signed",
            "theorem",
            "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "no-charge theorem remains unsigned",
        ),
        (
            "UPR2055_4_runner_status",
            "profile row score state",
            "conversion is algebraically sharpened but all live value/theorem slots are still missing",
            "do not score",
            "nonclaim",
            "RUNNER_BLOCKED_NONCLAIM",
            "source-ready, not evidence",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, bound_or_rule, units, status, missing_for_score in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "bound_or_rule": bound_or_rule,
                "units": units,
                "status": status,
                "missing_for_score": missing_for_score,
                "source_ready_schema": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows(profile_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blockers = "MISSING_PIR_VALUE;MISSING_OMEGA_W;MISSING_SAME_FRAME_RS;MISSING_TAIL_BUDGET"
    rows: list[dict[str, object]] = []
    for profile_row in profile_rows:
        row = base_row()
        row.update(
            {
                "run_id": "RUN_" + str(profile_row["row_id"]),
                "quantity": profile_row["quantity"],
                "source_ready_schema": profile_row["source_ready_schema"],
                "accepted_for_scoring": False,
                "verdict": "SYMBOLIC_CONVERSION_ROW_NONCLAIM",
                "reason": blockers,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2055_VERDICT",
            "quantity": "Pi_R_to_q_R_PPN_conversion",
            "source_ready_schema": True,
            "accepted_for_scoring": False,
            "verdict": "CONVERSION_DERIVED_SYMBOLIC_BOUND_BLOCKED_NONCLAIM",
            "reason": "Pi_R-to-q_R^PPN conversion is explicit, but omega_W, Pi_R, r_s owner and tail budget are missing",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2055_0_conversion", "Pi_R to q_R^PPN conversion derived", "PASS_NONCLAIM", "q_R^PPN=Pi_R/(omega_W r_s) under declared orientation and omega_W definition"),
        ("GATE2055_1_kW_repaired", "2054 k_W convention repaired", "PASS_NONCLAIM", "k_W is explicitly inverse omega_W"),
        ("GATE2055_2_symbolic_bound", "Cassini symbolic Pi_R bound written", "PASS_NONCLAIM", "bound remains symbolic in omega_W, r_s and tail budget"),
        ("GATE2055_3_omegaW_numeric", "omega_W parent value supplied", "FAIL_BLOCKED", "W_R asymptotic normalization is not parent-signed"),
        ("GATE2055_4_PiR_score", "Pi_R/q_R row scoreable", "FAIL_BLOCKED", "Pi_R numeric/theorem-zero and tail budget missing"),
        ("GATE2055_5_local_GR", "q_R=0/local GR/Newton claimed", "FAIL_BLOCKED", "no no-charge theorem, source mass owner, beta or Newton proof"),
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
            "DEC2055_0_result",
            "2055 derives the Pi_R-to-q_R conversion conditionally.",
            "With C_R=q_R^PPN r_s/r, omega_W=lim W_R/r^2 and Q_R=-Pi_R, the clean relation is q_R^PPN=Pi_R/(omega_W r_s).",
        ),
        (
            "DEC2055_1_not_scoreable",
            "The conversion is not yet a score.",
            "omega_W, Pi_R, same-frame r_s ownership and absolute tail budget are still missing or unsigned.",
        ),
        (
            "DEC2055_2_next",
            "Next best move is W_R radial measure ownership.",
            "If omega_W is derived, the profile row becomes much closer to a real bounded local-GR residual; if not, keep symbolic and move to source mass.",
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
            "target_id": "NEXT2055_0_2056",
            "target_doc": "2056-Y5-R2FR-WR-radial-measure-owner-or-omegaW-symbolic-runner.md",
            "objective": "derive omega_W=lim W_R/r^2 from the parent radial action/measure/coframe reduction, or keep omega_W symbolic and move to same-frame source mass calibration",
            "must_include": "radial reduced action measure; W_R positivity; asymptotic r^2 coefficient; no W_R=r^2 by taste; omega_W source row; updated Pi_R/q_R runner; source-mass fallback",
            "excluded": "assuming omega_W=1 without parent derivation; scoring Pi_R while omega_W symbolic; hiding source mass circularity; claiming local GR/Newton; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    conversion: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2055_0_source_weight_conversion",
            SOURCE_WEIGHT_DOCS / "AFRAME_PIR_QR_CONVERSION_2055_NONCLAIM.csv",
            conversion,
        ),
        (
            "COPY2055_1_wep_profile_update",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2055_QR_PROFILE_UPDATE_NONCLAIM.csv",
            profile_rows,
        ),
        (
            "COPY2055_2_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2055_PIR_WR_RUNNER_NONCLAIM.csv",
            runner,
        ),
        (
            "COPY2055_3_rab_next",
            QUEUE / "JR2055_WR_RADIAL_MEASURE_OWNER_NEXT_NONCLAIM.csv",
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
    conversion: list[dict[str, object]],
    normalization: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    conv_verdict = next(row for row in conversion if row["row_id"] == "CONV2055_6_verdict")
    combine_row = next(row for row in conversion if row["row_id"] == "CONV2055_4_combine")
    norm_verdict = next(row for row in normalization if row["row_id"] == "NORM2055_5_verdict")
    k_row = next(row for row in profile_rows if row["row_id"] == "UPR2055_2_kW_converter")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2055_VERDICT")
    omega_gate = next(row for row in gates if row["row_id"] == "GATE2055_3_omegaW_numeric")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2055_5_local_GR")
    no_score = all(not bool(row.get("ready_for_scoring", False)) for row in profile_rows) and all(
        not bool(row.get("accepted_for_scoring", False)) for row in runner
    )
    profile_coverage = {"UPR2055_0_qR_profile", "UPR2055_1_PiR_conversion", "UPR2055_2_kW_converter"}.issubset(
        {str(row["row_id"]) for row in profile_rows}
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2055_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2055_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2055_02_conversion_derived", conv_verdict["status"] == "CONVERSION_DERIVED_CONDITIONAL_RUNNER_BLOCKED", "Pi_R-to-q_R conversion derived conditionally"))
    checks.append(("VAL2055_03_formula_contains_omegaW", "omega_W" in str(combine_row["formula"]) and "Pi_R/(omega_W r_s)" in str(combine_row["formula"]), "conversion formula explicitly uses omega_W"))
    checks.append(("VAL2055_04_normalization_symbolic", norm_verdict["status"] == "SYMBOLIC_NONCLAIM_ONLY", "normalization remains symbolic/nonclaim"))
    checks.append(("VAL2055_05_kW_inverse_declared", "k_W:=1/omega_W" in str(k_row["formula"]), "k_W inverse convention declared"))
    checks.append(("VAL2055_06_profile_coverage", profile_coverage, "q_R, Pi_R and k_W profile update rows are present"))
    checks.append(("VAL2055_07_runner_blocked", runner_verdict["verdict"] == "CONVERSION_DERIVED_SYMBOLIC_BOUND_BLOCKED_NONCLAIM", "runner blocks scoring while preserving symbolic bound"))
    checks.append(("VAL2055_08_no_score", no_score, "no symbolic profile row is accepted for scoring"))
    checks.append(("VAL2055_09_omega_gate_blocked", omega_gate["status"] == "FAIL_BLOCKED", "omega_W numeric gate remains blocked"))
    checks.append(("VAL2055_10_local_GR_blocked", local_gate["status"] == "FAIL_BLOCKED", "local GR/Newton claim remains blocked"))
    checks.append(("VAL2055_11_next_selected", next_rows_[0]["target_id"] == "NEXT2055_0_2056", "2056 W_R radial measure owner target selected"))
    checks.append(("VAL2055_12_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2055_13_no_formalization_2055_artifacts", not formalization_has_2055_artifacts(), "no 2055 artifacts were written under formalization-workbench"))
    checks.append(("VAL2055_14_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2055_OVERALL", overall, "2055 derives symbolic Pi_R/q_R conversion, blocks scoring and selects W_R radial measure ownership next"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    conversion: list[dict[str, object]],
    normalization: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2055 Y5 R2FR Pi_R Boundary Momentum Or W_R Asymptotic Normalization",
        "",
        "## Current Verdict",
        "",
        "2055 derives the conditional boundary conversion cleanly. In the areal PPN profile `C_R=q_R^PPN r_s/r`, define `omega_W=lim_{r->infinity} W_R/r^2`. Then `W_R partial_r C_R=Q_R` gives `Q_R=-omega_W q_R^PPN r_s`, and the 06 boundary convention `Q_R=-Pi_R` gives `q_R^PPN=Pi_R/(omega_W r_s)`. Equivalently the 2054 shorthand `q_R^PPN=k_W Pi_R/r_s` is valid only if `k_W=1/omega_W`.",
        "",
        "This is progress, not a pass. `omega_W`, `Pi_R`, same-frame `r_s`, and the absolute tail budget are still missing or unsigned. The Cassini lane is therefore a symbolic nonclaim bound, not an MTS prediction score.",
        "",
        "No `Pi_R=0`, `q_R=0`, `R_AB=0`, local-GR, Newton, PPN pass, GitHub action, or `formalization-workbench` edit is claimed.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Conversion Derivation",
        md_table(conversion, ["row_id", "item", "formula", "status", "meaning", "blocker", "claim_allowed"]),
        "## Normalization Audit",
        md_table(normalization, ["row_id", "topic", "evidence", "status", "effect_if_signed", "blocker", "claim_allowed"]),
        "## Updated q_R/Pi_R Profile Rows",
        md_table(profile_rows, ["row_id", "quantity", "formula", "bound_or_rule", "units", "status", "missing_for_score", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
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
    conversion = conversion_derivation_rows()
    normalization = normalization_audit_rows()
    profile_rows = updated_profile_rows()
    runner = runner_rows(profile_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2055_SOURCE_REGISTER.csv",
        "conversion": OUT / "P8_Y5_PARENT_QLOC_2055_PIR_QR_CONVERSION_DERIVATION.csv",
        "normalization": OUT / "P8_Y5_PARENT_QLOC_2055_WR_NORMALIZATION_AUDIT.csv",
        "profiles": OUT / "P8_Y5_PARENT_QLOC_2055_QR_PROFILE_UPDATE_NONCLAIM.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2055_PIR_WR_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2055_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2055_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2055_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2055_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2055_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["conversion"], conversion)
    write_csv(paths["normalization"], normalization)
    write_csv(paths["profiles"], profile_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(conversion, profile_rows, runner, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, conversion, normalization, profile_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, conversion, normalization, profile_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, conversion, normalization, profile_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
