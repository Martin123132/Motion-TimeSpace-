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


DOC = ROOT / "2051-Y5-R2FR-lambdaR-origin-or-QR-nocharge-certificate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2051_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2051-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2051*",
            "*Y5_R2FR_lambdaR_origin_or_QR_nocharge_certificate_2051*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2051_00_2050_doc",
            ROOT / "2050-Y5-R2FR-minimal-motion-load-radial-action-or-RAB-residual-runner.md",
            ["NEXT2050_0_2051", "lambda_R", "Q_R no-charge"],
            "2050 handoff into lambda_R origin or Q_R no-charge certificate.",
        ),
        (
            "SRC2051_01_2050_next",
            OUT / "P8_Y5_PARENT_QLOC_2050_NEXT_TARGET.csv",
            ["NEXT2050_0_2051", "lambda_R constraint class", "finite residual source acquisition queue"],
            "machine-readable 2051 target.",
        ),
        (
            "SRC2051_02_nonprop_constraint",
            ROOT / "07-nonpropagating-reciprocity-constraint.md",
            ["S_constraint = integral lambda_R R_AB.", "T^2 S = 1", "why does the parent motion-load action contain lambda_R"],
            "nonpropagating constraint route and parent-origin gap.",
        ),
        (
            "SRC2051_03_cell_current",
            ROOT / "11-cell-current-origin-attempt.md",
            ["cell_current_origin_no_charge_obstruction", "Q_R = constant.", "Therefore the branch either needs a true gauge/Noether origin"],
            "ordinary cell-current route and Q_R hair obstruction.",
        ),
        (
            "SRC2051_04_gauge_noether",
            ROOT / "12-gauge-noether-origin-audit.md",
            ["gauge_noether_origin_not_derived_closure_only", "Noether structure can explain a constraint only after the parent action has"],
            "gauge/Noether route cannot conjure the constraint.",
        ),
        (
            "SRC2051_05_reciprocity",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["W R_AB' = Q_R.", "Asymptotic flatness alone does not kill `Q_R`."],
            "reciprocity theorem and asymptotic-flatness no-go.",
        ),
        (
            "SRC2051_06_source_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "Q_R neutrality is the missing source theorem"],
            "boundary momentum/source-neutrality conditional route.",
        ),
        (
            "SRC2051_07_first_class",
            ROOT / "1267-Y5-R10-first-class-RAB-parent-constraint-synthesis-or-finite-ZR-source-acquisition.md",
            ["FIRST_CLASS_ROUTE_NOT_CONSTRUCTED", "SECOND_CLASS_OR_HOLONOMIC_NOT_FIRST_CLASS"],
            "first-class route failure and second-class/auxiliary refocus.",
        ),
        (
            "SRC2051_08_second_class",
            ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            ["CAC1268_5_conditional_theorem", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
            "best conditional auxiliary-compatibility mechanism.",
        ),
        (
            "SRC2051_09_finite_fallback",
            ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            ["RCC1577_4_verdict", "NCA1577_4_verdict", "FCF1577_0_qRhat"],
            "finite residual fallback scaffold and no-charge failure.",
        ),
        (
            "SRC2051_10_no_gr_import",
            ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            ["NG1859_4_ordinary_current", "FRS1859_2_parent_Euler_difference", "VAL1859_OVERALL"],
            "no-GR-import guard and parent Euler difference route.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        needles_confirmed = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if needles_confirmed else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def lambda_origin_rows() -> list[dict[str, object]]:
    data = [
        (
            "LAM2051_0_direct_multiplier",
            "S_lambda=int dr lambda_R C_R",
            "delta_lambda S gives C_R=0 exactly",
            "FORMAL_CLOSURE_ONLY",
            "forces the answer if lambda_R is admitted",
            "parent source/class of lambda_R is not derived; declaring it by taste is rejected",
        ),
        (
            "LAM2051_1_first_class_gauge",
            "treat C_R as gauge-fixed coordinate",
            "would need a generator G_R/Pi_C, invariant matter, invariant readout, and bracket closure",
            "NOT_CONSTRUCTED",
            "would make C_R=0 a gauge choice rather than a new physical equation",
            "12 and 1267 do not supply the generator or invariant readout",
        ),
        (
            "LAM2051_2_second_class_auxiliary",
            "algebraic/second-class compatibility block",
            "E_Lambda enforces R_AB-C_AB=0; E_R kills Lambda_R only if no matter, boundary, derivative, or readout source exists",
            "BEST_CONDITIONAL_ROUTE",
            "cleanest non-GR-import mechanism if parent-signed",
            "1268 leaves parent sort, no-derivative grammar, matter descent, boundary silence and readout stability unsigned",
        ),
        (
            "LAM2051_3_nonpropagating_constraint",
            "nonpropagating reciprocity constraint",
            "lambda_R R_AB removes Q_R hair by not allowing a propagating R_AB current",
            "CLEAN_CLOSURE_NOT_PARENT_ORIGIN",
            "good closure benchmark",
            "07 explicitly asks why the parent motion-load action contains lambda_R ln(T^2S)",
        ),
        (
            "LAM2051_4_first_order_muR",
            "S_mu=int dr mu_R(partial_r C_R-S_R)",
            "can impose first-order radial balance if mu_R and S_R are parent-owned",
            "REJECT_IF_UNOWNED",
            "could express a parent Euler-difference equation",
            "currently shifts the gap from lambda_R to mu_R/S_R",
        ),
        (
            "LAM2051_5_no_gr_import_guard",
            "use EH/GR radial equations as shortcut",
            "would reproduce p=1 but imports the target theory unless MTS parent Euler equations are already derived",
            "REJECT_AS_GR_IMPORT_FOR_THIS_GATE",
            "keeps the route honest",
            "1859 keeps parent Euler difference as primary but unsigned",
        ),
        (
            "LAM2051_6_verdict",
            "lambda_R parent origin certificate",
            "no current source proves lambda_R is forced by MTS rather than inserted as a closure variable",
            "NO_LAMBDAR_PARENT_ORIGIN_CURRENT_CORPUS",
            "do not claim R_AB=0 from lambda_R yet",
            "best retained route is conditional second-class auxiliary compatibility plus finite residual fallback",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, candidate, derivation_status, status, if_closed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "candidate": candidate,
                "derivation_status": derivation_status,
                "status": status,
                "if_closed": if_closed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def qr_nocharge_rows() -> list[dict[str, object]]:
    data = [
        (
            "QR2051_0_current_equation",
            "partial_r(W_R partial_r C_R)+source terms = 0",
            "vacuum/source-free branch integrates to W_R partial_r C_R=Q_R",
            "DERIVES_CONSTANT_ONLY",
            "gives a measurable finite-hair branch",
            "does not set Q_R=0",
        ),
        (
            "QR2051_1_asymptotic_flatness",
            "C_R(infinity)=0",
            "permits C_R ~ -Q_R/r in the exterior",
            "REJECT_ZERO_PROOF",
            "normalizes the constant mode",
            "does not eliminate the reciprocal charge",
        ),
        (
            "QR2051_2_boundary_momentum",
            "delta B_R gives Q_R=-Pi_R",
            "Pi_R=0 would imply Q_R=0 -> C_R=0 -> AB=1",
            "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "strongest no-charge boundary theorem if source class is signed",
            "Pi_R=0 is not derived from the parent matter/boundary action",
        ),
        (
            "QR2051_3_source_neutrality",
            "source couples to public A/L variables but not independent R_AB",
            "J_R=0 and source reciprocal momentum zero would kill the charge",
            "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "could derive local reciprocity without fitting p=1",
            "source descent/matter coupling theorem is missing",
        ),
        (
            "QR2051_4_auxiliary_elimination",
            "eliminate R_AB before current formation",
            "second-class auxiliary branch has no physical Pi_R/Q_R if all 1268 protections hold",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "bypasses Q_R rather than proving Q_R=0 dynamically",
            "parent protections remain unsigned",
        ),
        (
            "QR2051_5_WR_positivity",
            "W_R>0",
            "positive strain weight makes C_R constant when Q_R=0",
            "NECESSARY_NOT_SUFFICIENT",
            "prevents sign tricks and ghosty zero proofs",
            "positivity alone still allows nonzero Q_R hair",
        ),
        (
            "QR2051_6_verdict",
            "Q_R no-charge certificate",
            "the corpus supplies conditional routes but no parent-signed theorem setting Q_R=0",
            "NO_QR_NOCHARGE_THEOREM_CURRENT_CORPUS",
            "finite residual branch must be filled if exact derivation remains unsigned",
            "do not use asymptotic flatness or ordinary conservation as no-charge proof",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, route, derivation_status, status, if_closed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "route": route,
                "derivation_status": derivation_status,
                "status": status,
                "if_closed": if_closed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_acquisition_rows() -> list[dict[str, object]]:
    data = [
        (
            "FACQ2051_0_C_R_profile",
            "C_R(r)=ln(T^2S)",
            "dimensionless profile or theorem-zero",
            "PPN;light_bending;Shapiro;orbital;clock",
            "MISSING_PROFILE_OR_THEOREM_ZERO",
            "source a parent equation/profile, not a fitted p=1 closure",
        ),
        (
            "FACQ2051_1_q_R_hat",
            "q_R_hat or Q_R",
            "dimensionless amplitude or current with convention",
            "PPN;R10;clock;orbital",
            "MISSING_QR_VALUE_OR_ZERO_THEOREM",
            "carry source path, units, GM convention and no-cancellation policy",
        ),
        (
            "FACQ2051_2_J_R_source",
            "J_R/S_R source balance",
            "declared source units",
            "Newtonian_limit;PPN;matter_coupling",
            "MISSING_PARENT_SOURCE_MAP",
            "derive or source how matter loads the reciprocal branch",
        ),
        (
            "FACQ2051_3_Pi_R_boundary",
            "Pi_R or B_R boundary momentum",
            "boundary/current units",
            "orbital;clock;R10",
            "MISSING_BOUNDARY_VARIATION_CLASS",
            "prove free/source-neutral boundary or give bounded nonzero tail",
        ),
        (
            "FACQ2051_4_W_R_positive",
            "W_R strain weight",
            "positive function with units",
            "stability;current_equation",
            "MISSING_PARENT_SIGN_AND_NORMALIZATION",
            "derive W_R>0 and its normalization from motion-load variables",
        ),
        (
            "FACQ2051_5_tau_PPN",
            "tau_PPN_R",
            "dimensionless response kernel",
            "Cassini;PPN_gamma_beta",
            "MISSING_PPN_PROJECTION",
            "map C_R/q_R into gamma-1, beta-1 and timing observables",
        ),
        (
            "FACQ2051_6_tau_R10",
            "tau_R10_R",
            "short-range response kernel",
            "R10;inverse_square",
            "MISSING_R10_PROJECTION",
            "map finite reciprocal component into alpha(lambda) convention",
        ),
        (
            "FACQ2051_7_tau_clock",
            "tau_clock_R",
            "clock/redshift response kernel",
            "clock;redshift;time",
            "MISSING_CLOCK_PROJECTION",
            "map reciprocal residual into clock comparison observables",
        ),
        (
            "FACQ2051_8_tau_orbital",
            "tau_orbital_R",
            "orbital response kernel",
            "perihelion;binary;ephemeris",
            "MISSING_ORBITAL_PROJECTION",
            "map residual profile into orbital precession/timing bounds",
        ),
        (
            "FACQ2051_9_no_cancellation_policy",
            "finite-branch scoring rule",
            "no hidden cancellation between missing sectors",
            "all_local_arenas",
            "MISSING_POLICY_LOCK",
            "runner must refuse rows without source path, units, convention, and arena projection",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, required_input, observable_links, status, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "required_input": required_input,
                "observable_links": observable_links,
                "current_status": status,
                "next_action": next_action,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_decision_rows(acquisition_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for input_row in acquisition_rows:
        decision = base_row()
        decision.update(
            {
                "run_id": "RUN_" + str(input_row["row_id"]),
                "input_id": input_row["row_id"],
                "quantity": input_row["quantity"],
                "accepted_for_scoring": False,
                "verdict": "SOURCE_ACQUISITION_REQUIRED_NONCLAIM",
                "reason": "missing theorem-zero or source-backed numeric/projection input with units and source path",
                "claim_allowed": False,
            }
        )
        rows.append(decision)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2051_VERDICT",
            "input_id": "all_finite_RAB_rows",
            "quantity": "finite_R_AB_residual_source_acquisition",
            "accepted_for_scoring": False,
            "verdict": "FINITE_RAB_ACQUISITION_SELECTED_NONCLAIM",
            "reason": "lambda_R parent origin and Q_R no-charge proofs did not close; move from proof-looping to source/acquisition runner",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2051_0_formal_algebra", "lambda_R and Q_R algebra is internally understood", "PASS_NONCLAIM", "constraint/current equations are clear but not parent-signed"),
        ("GATE2051_1_lambda_parent", "lambda_R has parent origin/class", "FAIL_BLOCKED", "direct multiplier and nonpropagating routes remain closure unless parent-owned"),
        ("GATE2051_2_QR_nocharge", "Q_R=0 follows from parent source/boundary theorem", "FAIL_BLOCKED", "Pi_R/source neutrality/auxiliary elimination remain conditional"),
        ("GATE2051_3_no_GR_import", "no-GR-import derivation of local reciprocity", "FAIL_BLOCKED", "parent Euler difference/source map still unsigned"),
        ("GATE2051_4_RAB_zero", "R_AB=0/p=1/beta=1 local branch", "FAIL_BLOCKED", "zero theorem not derived"),
        ("GATE2051_5_finite_acquisition", "finite residual source-acquisition mode", "PASS_NONCLAIM", "next route is to fill source-backed residual/projection rows"),
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
            "DEC2051_0_proof_attempt_result",
            "The proof-first route was attempted and did not close.",
            "lambda_R can force C_R=0 formally, and Pi_R=0 can kill Q_R conditionally, but neither is parent-signed in the current corpus.",
        ),
        (
            "DEC2051_1_best_derivation_lane",
            "Keep the second-class auxiliary mechanism as the best exact lane.",
            "It is cleaner than first-class gauge language and avoids pretending ordinary current conservation kills Q_R.",
        ),
        (
            "DEC2051_2_stop_circling_rule",
            "Do not keep restating the same lambda_R/Q_R obstruction without new parent input.",
            "The next productive step is finite residual source acquisition and bound-running, while the exact lane waits for a new parent block.",
        ),
        (
            "DEC2051_3_project_status",
            "This is a narrowing, not a collapse.",
            "The local route now has a precise missing theorem and a testable fallback rather than a vague GR analogy.",
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
            "target_id": "NEXT2051_0_2052",
            "target_doc": "2052-Y5-R2FR-finite-RAB-residual-source-acquisition-and-bound-runner.md",
            "objective": "build the source-backed finite R_AB residual acquisition pack and bound runner for PPN, R10, clock and orbital arenas; only reopen lambda_R/Q_R zero proof if a new parent action/source theorem is introduced",
            "must_include": "C_R/q_R/Q_R row schema; W_R sign/normalization; J_R/Pi_R source path requirements; tau_PPN; tau_R10; tau_clock; tau_orbital; no-cancellation policy; live runner refusal/pass logic",
            "excluded": "another closure-only lambda_R proof loop; asymptotic-flatness no-charge claims; invented finite residual values; beta/local-GR claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    lambda_rows: list[dict[str, object]],
    qr_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2051_0_source_weight_lambda_origin",
            SOURCE_WEIGHT_DOCS / "AFRAME_LAMBDAR_ORIGIN_2051_NONCLAIM.csv",
            lambda_rows,
        ),
        (
            "COPY2051_1_source_weight_qr_nocharge",
            SOURCE_WEIGHT_DOCS / "AFRAME_QR_NOCHARGE_2051_NONCLAIM.csv",
            qr_rows,
        ),
        (
            "COPY2051_2_wep_finite_acquisition",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2051_FINITE_RAB_ACQUISITION_NONCLAIM.csv",
            acquisition_rows,
        ),
        (
            "COPY2051_3_rab_next",
            QUEUE / "JR2051_FINITE_RAB_SOURCE_ACQUISITION_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, copy_path, data in copies:
        write_csv(copy_path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(copy_path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY"})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    lambda_rows: list[dict[str, object]],
    qr_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_paths_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_parse_ok = all(csv_rows_parse(csv_path) for csv_path in csv_paths)
    lambda_verdict = next(row for row in lambda_rows if row["row_id"] == "LAM2051_6_verdict")
    qr_verdict = next(row for row in qr_rows if row["row_id"] == "QR2051_6_verdict")
    asymptotic_row = next(row for row in qr_rows if row["row_id"] == "QR2051_1_asymptotic_flatness")
    runner_verdict = next(row for row in runner_rows_ if row["run_id"] == "RUN2051_VERDICT")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2051_4_RAB_zero")
    finite_gate = next(row for row in gates if row["row_id"] == "GATE2051_5_finite_acquisition")
    all_nonclaim = (
        all(not bool(row.get("claim_allowed", False)) for row in lambda_rows)
        and all(not bool(row.get("claim_allowed", False)) for row in qr_rows)
        and all(not bool(row.get("ready_for_scoring", False)) for row in acquisition_rows)
        and all(not bool(row.get("claim_allowed", False)) for row in runner_rows_)
    )
    required_arena_fragments = ["tau_PPN", "tau_R10", "tau_clock", "tau_orbital"]
    arena_rows_present = all(
        any(fragment in str(row["quantity"]) for row in acquisition_rows)
        for fragment in required_arena_fragments
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2051_00_local_sources_exist", source_paths_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2051_01_csv_parse", csv_parse_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2051_02_lambda_not_parent_signed", lambda_verdict["status"] == "NO_LAMBDAR_PARENT_ORIGIN_CURRENT_CORPUS", "lambda_R origin not promoted"))
    checks.append(("VAL2051_03_qr_nocharge_not_signed", qr_verdict["status"] == "NO_QR_NOCHARGE_THEOREM_CURRENT_CORPUS", "Q_R no-charge theorem not promoted"))
    checks.append(("VAL2051_04_asymptotic_flatness_rejected", asymptotic_row["status"] == "REJECT_ZERO_PROOF", "asymptotic flatness is not used as no-charge proof"))
    checks.append(("VAL2051_05_acquisition_rows_nonclaim", all_nonclaim, "finite residual rows remain nonclaim/not ready for scoring"))
    checks.append(("VAL2051_06_local_arenas_present", arena_rows_present, "PPN, R10, clock and orbital acquisition rows are present"))
    checks.append(("VAL2051_07_runner_selects_acquisition", runner_verdict["verdict"] == "FINITE_RAB_ACQUISITION_SELECTED_NONCLAIM", "runner moves to source acquisition nonclaim"))
    checks.append(("VAL2051_08_RAB_zero_blocked", local_gate["status"] == "FAIL_BLOCKED", "R_AB=0/local branch remains blocked"))
    checks.append(("VAL2051_09_finite_gate_nonclaim_pass", finite_gate["status"] == "PASS_NONCLAIM", "finite acquisition gate opens without claim"))
    checks.append(("VAL2051_10_next_selected", next_rows_[0]["target_id"] == "NEXT2051_0_2052", "2052 finite residual source-acquisition target selected"))
    checks.append(("VAL2051_11_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2051_12_no_formalization_2051_artifacts", not formalization_has_2051_artifacts(), "no 2051 artifacts were written under formalization-workbench"))
    checks.append(("VAL2051_13_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_pass = all(check_passed for _, check_passed, _ in checks)
    checks.append(("VAL2051_OVERALL", overall_pass, "2051 tried lambda_R/Q_R proof first, blocked claims, and selected finite residual acquisition"))
    rows: list[dict[str, object]] = []
    for check_id, check_passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if check_passed else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    lambda_rows: list[dict[str, object]],
    qr_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2051 Y5 R2FR lambda_R Origin Or Q_R No-Charge Certificate",
        "",
        "## Current Verdict",
        "",
        "2051 takes the proof-first route seriously. The result is sharp but not celebratory: `lambda_R C_R` and the nonpropagating constraint force `C_R=ln(T^2S)=0` formally, while `Pi_R=0` would kill `Q_R` conditionally. But the current corpus still does not parent-sign either the `lambda_R` origin/class or the `Q_R` no-charge/source-neutrality theorem.",
        "",
        "So this is the anti-circle checkpoint: do not keep proving the same closure in new words. The exact local-GR lane remains alive as a conditional second-class auxiliary mechanism, but the next productive route is a finite `R_AB` residual source-acquisition and bound runner. No `R_AB=0`, `p=1`, `beta=1`, PPN/R10/clock/orbital pass, GitHub action, or `formalization-workbench` edit is claimed.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## lambda_R Origin Audit",
        md_table(lambda_rows, ["row_id", "candidate", "derivation_status", "status", "if_closed", "blocker", "claim_allowed"]),
        "## Q_R No-Charge Audit",
        md_table(qr_rows, ["row_id", "route", "derivation_status", "status", "if_closed", "blocker", "claim_allowed"]),
        "## Finite Residual Acquisition Queue",
        md_table(acquisition_rows, ["row_id", "quantity", "required_input", "observable_links", "current_status", "next_action", "ready_for_scoring", "claim_allowed"]),
        "## Runner Decision",
        md_table(runner_rows_, ["run_id", "input_id", "quantity", "accepted_for_scoring", "verdict", "reason", "claim_allowed"]),
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
    lambda_rows = lambda_origin_rows()
    qr_rows = qr_nocharge_rows()
    acquisition_rows = finite_acquisition_rows()
    runner_rows_ = runner_decision_rows(acquisition_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2051_SOURCE_REGISTER.csv",
        "lambda": OUT / "P8_Y5_PARENT_QLOC_2051_LAMBDAR_ORIGIN_AUDIT.csv",
        "qr": OUT / "P8_Y5_PARENT_QLOC_2051_QR_NOCHARGE_AUDIT.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2051_FINITE_RESIDUAL_ACQUISITION_QUEUE.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2051_RUNNER_DECISION.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2051_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2051_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2051_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2051_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2051_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["lambda"], lambda_rows)
    write_csv(paths["qr"], qr_rows)
    write_csv(paths["acquisition"], acquisition_rows)
    write_csv(paths["runner"], runner_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(lambda_rows, qr_rows, acquisition_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, lambda_rows, qr_rows, acquisition_rows, runner_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, lambda_rows, qr_rows, acquisition_rows, runner_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, lambda_rows, qr_rows, acquisition_rows, runner_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
