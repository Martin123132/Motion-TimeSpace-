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


DOC = ROOT / "2093-Y5-R2FR-radial-micro-kernel-axiom-review-or-finite-local-input-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_1572_CURVE = OUT / "P8_Y5_PARENT_QLOC_1572_R10_ALPHA_LAMBDA_REVIEWED_CANDIDATE.csv"
SRC_1573_TAU = OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv"
SRC_1577_FINITE = OUT / "P8_Y5_PARENT_QLOC_1577_FINITE_COMPONENT_BOUND_FILL_START.csv"
SRC_2092_INTAKE = OUT / "P8_Y5_PARENT_QLOC_2092_FINITE_INPUT_INTAKE.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid", "pass"}


def formalization_has_2093_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2093-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2093*",
        "*Y5_R2FR_radial_micro_kernel_axiom_review_or_finite_local_input_runner_2093*",
        "*AFRAME_RADIAL_MICRO_KERNEL_AXIOM_REVIEW_2093*",
        "*JR2093_FINITE_LOCAL_INPUT_PRIORITY*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def safe_read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def csv_true_count(rows: list[dict[str, str]], column: str) -> int:
    return sum(1 for csv_row in rows if truthy(csv_row.get(column, "")))


def csv_status_values(rows: list[dict[str, str]], column: str) -> str:
    values: list[str] = []
    for csv_row in rows:
        value = csv_row.get(column, "").strip()
        if value and value not in values:
            values.append(value)
    return "; ".join(values[:8])


def csv_missing_values(rows: list[dict[str, str]]) -> str:
    values: list[str] = []
    for csv_row in rows:
        for column, value in csv_row.items():
            text = str(value)
            if ("MISSING_" in text or "NOT_ACCEPTED" in text or "SOURCE_BACKED_ROW_MISSING" in text) and text not in values:
                values.append(text)
    return "; ".join(values[:12])


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2093_00_2092_handoff",
            ROOT / "2092-Y5-R2FR-minimal-radial-parent-micro-kernel-or-finite-input-intake.md",
            ["NEXT2092_0_2093", "MK2092_5_status", "VAL2092_OVERALL"],
            "2092 constructs the micro-kernel but records formal-pass/parent-derivation-fail.",
        ),
        (
            "SRC2093_01_2091_source_hunt",
            ROOT / "2091-Y5-R2FR-radial-canonical-pair-source-hunt-or-finite-residual-lock.md",
            ["LOCK2091_0_selector_status", "DEC2091_0_source_hunt_result", "VAL2091_OVERALL"],
            "2091 failed to find a current parent source for theta_R/H_R.",
        ),
        (
            "SRC2093_02_1572_R10_curve",
            SRC_1572_CURVE,
            ["REVIEWED_QA_CANDIDATE_NONCLAIM", "accepted_for_scoring", "passes_for_claim"],
            "R10 curve exists as internal reviewed candidate only, not accepted scoring evidence.",
        ),
        (
            "SRC2093_03_1573_tau_inputs",
            SRC_1573_TAU,
            ["REQ1573_0_ZR", "MISSING_ZR", "REQ1573_4_Xi"],
            "tau_R10 still lacks Z_R, M_R^2, source/test charges, readout, and boundary tail.",
        ),
        (
            "SRC2093_04_1577_finite_components",
            SRC_1577_FINITE,
            ["FCF1577_0_qRhat", "MISSING_QR_VALUE_OR_ZERO_THEOREM", "FCF1577_4_arena_projection"],
            "finite local component rows remain missing for q_R/Q_R, operator, source, boundary and arenas.",
        ),
        (
            "SRC2093_05_2092_intake",
            SRC_2092_INTAKE,
            ["INT2092_0_ZR_MR2", "SOURCE_BACKED_ROW_MISSING", "INT2092_8_no_cancellation"],
            "2092 finite intake explicitly left all source-backed local rows missing.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2093_axiom_review_and_finite_input_gate",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2093=note,
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return rows


def axiom_review_rows() -> list[dict[str, object]]:
    return [
        row(
            review_id="AXR2093_0_minimality",
            question="Is the radial micro-kernel the smallest known block that closes the selector?",
            answer="yes, conditionally",
            evidence="2092 gives S_micro=int P_R(C_R'-S_R)dr+B_R and delta_{P_R} gives C_R'=S_R.",
            risk="minimality is within the current reduced radial grammar, not a theorem over every possible parent action.",
            verdict="PASS_CONDITIONAL_MINIMAL_ENGINE",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            review_id="AXR2093_1_derivation",
            question="Is the micro-kernel derived from deeper MTS primitives already in the corpus?",
            answer="no",
            evidence="2091 source hunt and 2092 parent necessity gate do not source theta_R=P_R delta C_R or H_R=P_R S_R.",
            risk="publicly calling it derived would overclaim the local-GR branch.",
            verdict="FAIL_CURRENT_PARENT_DERIVATION",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            review_id="AXR2093_2_testability",
            question="Does the unresolved axiom cost map to finite tests rather than vague handwaving?",
            answer="yes, conditionally",
            evidence="Z_R/M_R2, J_R/S_R, Q_R/q_R_hat, boundary tails and arena projections are explicit intake rows.",
            risk="no numerical score exists until those rows are source-backed or theorem-zero.",
            verdict="PASS_CONDITIONAL_TESTABLE_DEFECTS",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            review_id="AXR2093_3_scrutiny",
            question="Would this survive scrutiny if presented as final derived local GR?",
            answer="no",
            evidence="countermodels with extra V_R terms, kinetic C_R, nonzero S_R, boundary hair, or readout reentry remain open.",
            risk="a critic can accept the algebra and still reject the parent origin.",
            verdict="HIGH_RISK_IF_PUBLIC_AS_DERIVED",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            review_id="AXR2093_4_recommendation",
            question="What should the programme do with the micro-kernel now?",
            answer="keep it as a private working parent-axiom candidate, not as a claim.",
            evidence="it is mathematically clean, local, finite-input-testable, and directly targets the coupling gap.",
            risk="the theory still needs either a deeper derivation or source-backed finite residual bounds.",
            verdict="PRIVATE_WORKING_AXIOM_PLUS_FINITE_INPUT_PIVOT",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def adoption_option_rows() -> list[dict[str, object]]:
    return [
        row(
            option_id="OPT2093_A_deeper_derivation",
            option="derive micro-kernel from object-language/constraint grammar",
            upside="highest purity; preserves the ambition that the local-GR branch is not an inserted plateau",
            downside="current corpus has not supplied the parent theta/H_R source",
            present_status="OPEN_BUT_NOT_READY",
            selected=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            option_id="OPT2093_B_explicit_axiom",
            option="adopt S_micro as an explicit parent radial compatibility axiom",
            upside="clean, minimal and honest; makes the missing coupling visible instead of hidden",
            downside="adds a foundational postulate that must be labelled and defended",
            present_status="PRIVATE_WORKING_BRANCH_ONLY",
            selected=True,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            option_id="OPT2093_C_finite_input_pivot",
            option="start source-backed local finite input acquisition",
            upside="turns the open clauses into R10/PPN/clock/orbital pass-fail rows",
            downside="cannot score until parent coefficients and arena kernels are sourced",
            present_status="SELECTED_NEXT_OPERATION",
            selected=True,
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def finite_runner_rows() -> list[dict[str, object]]:
    curve_rows = safe_read_csv(SRC_1572_CURVE)
    tau_rows = safe_read_csv(SRC_1573_TAU)
    finite_rows = safe_read_csv(SRC_1577_FINITE)
    intake_rows = safe_read_csv(SRC_2092_INTAKE)
    return [
        row(
            run_id="FIN2093_0_R10_bound_curve",
            source_path=str(SRC_1572_CURVE),
            rows_read=len(curve_rows),
            observed_status=csv_status_values(curve_rows, "review_status"),
            accepted_for_scoring_count=csv_true_count(curve_rows, "accepted_for_scoring"),
            score_ready_count=csv_true_count(curve_rows, "score_ready"),
            passes_for_claim_count=csv_true_count(curve_rows, "passes_for_claim"),
            result="REFUSED_BOUND_CURVE_NONCLAIM_NOT_ACCEPTED",
            next_action="promote only after independent/manual curve QA or source-backed machine table",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="FIN2093_1_tau_R10_inputs",
            source_path=str(SRC_1573_TAU),
            rows_read=len(tau_rows),
            observed_status=csv_status_values(tau_rows, "current_status"),
            missing_or_blocked=csv_missing_values(tau_rows),
            score_ready_count=csv_true_count(tau_rows, "score_ready"),
            result="REFUSED_ZR_MR2_CHARGES_READOUT_BOUNDARY_MISSING",
            next_action="source Z_R, M_R^2, beta_S^R, beta_T^R, Xi_R10 and boundary tail in same parent frame",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="FIN2093_2_finite_components",
            source_path=str(SRC_1577_FINITE),
            rows_read=len(finite_rows),
            observed_status=csv_status_values(finite_rows, "current_status"),
            missing_or_blocked=csv_missing_values(finite_rows),
            score_ready_count=csv_true_count(finite_rows, "score_ready"),
            result="REFUSED_QR_OPERATOR_SOURCE_BOUNDARY_ARENA_MISSING",
            next_action="fill one source-backed component row at a time; no cancellation between siblings",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="FIN2093_3_2092_intake",
            source_path=str(SRC_2092_INTAKE),
            rows_read=len(intake_rows),
            observed_status=csv_status_values(intake_rows, "current_status"),
            missing_or_blocked=csv_missing_values(intake_rows),
            score_ready_count=csv_true_count(intake_rows, "score_ready"),
            result="REFUSED_ALL_2092_INTAKE_ROWS_SOURCE_BACKED_MISSING",
            next_action="choose the first finite local input target rather than looping derivation language",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="FIN2093_4_scoring_decision",
            source_path="combined 1572/1573/1577/2092",
            rows_read=len(curve_rows) + len(tau_rows) + len(finite_rows) + len(intake_rows),
            observed_status="nonclaim curve plus missing finite parent inputs",
            score_ready_count=0,
            result="NO_LOCAL_R10_PPN_CLOCK_OR_ORBITAL_SCORE_ALLOWED",
            next_action="2094 should acquire or reject the first finite local input row",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def priority_queue_rows() -> list[dict[str, object]]:
    return [
        row(
            priority_id="PRI2093_0_qR_QR_no_charge",
            target_quantity="Q_R or q_R_hat",
            why_first="a no-charge theorem or same-frame bound would immediately kill or quantify exterior reciprocal hair",
            acceptable_evidence="parent boundary/no-charge theorem, or numeric q_R_hat/Q_R bound with source path, units, GM convention and no-cancellation policy",
            failure_mode="MISSING_QR_VALUE_OR_ZERO_THEOREM",
            next_action="attempt theorem-zero first; if it fails, create finite bound row",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            priority_id="PRI2093_1_ZR_MR2_operator",
            target_quantity="Z_R and M_R^2",
            why_first="these decide whether the radial residual is no-pole/theorem-zero or finite-range Yukawa-like",
            acceptable_evidence="parent kinetic/Hessian block with normalization, sign, units and vacuum point",
            failure_mode="MISSING_OPERATOR_SIGNATURE",
            next_action="hunt parent action terms before assigning numerical lambda_R",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            priority_id="PRI2093_2_SR_JR_source_map",
            target_quantity="S_R, J_R, beta_S^R, beta_T^R",
            why_first="C_R'=S_R only reduces to local reciprocity if the source side is zero or bounded",
            acceptable_evidence="matter descent/source-map theorem or finite material charge coefficients",
            failure_mode="MISSING_SOURCE_CHARGE_RESOLUTION",
            next_action="split source and test legs; forbid linear-c_g shortcut",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            priority_id="PRI2093_3_boundary_tail",
            target_quantity="B_R, Pi_R, alpha_boundary_tail",
            why_first="boundary hair can survive even if the bulk equation is clean",
            acceptable_evidence="proper/exact boundary class theorem or absolute finite envelope",
            failure_mode="MISSING_BOUNDARY_RESOLUTION",
            next_action="make boundary charge either theorem-zero or separately bounded",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            priority_id="PRI2093_4_arena_projections",
            target_quantity="tau_R10, tau_PPN, tau_clock, tau_orbital",
            why_first="arena kernels translate the finite residual into observable tests",
            acceptable_evidence="separate same-frame projection kernels with units and readout convention",
            failure_mode="MISSING_ARENA_PROJECTIONS",
            next_action="do not transfer a pass from one arena to another",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    gates = [
        (
            "GATE2093_0_public_local_GR",
            "MTS has derived local GR/Newton from the parent action",
            "FAIL_BLOCKED",
            "micro-kernel is not parent-derived and finite source/boundary gates remain open",
        ),
        (
            "GATE2093_1_micro_kernel_as_axiom",
            "S_micro can be used as a private working axiom candidate",
            "PASS_PRIVATE_WORKING_ONLY",
            "allowed for internal branch development if labelled; not claim evidence",
        ),
        (
            "GATE2093_2_R10_score",
            "R10 local residual can be scored",
            "FAIL_BLOCKED",
            "bound curve not accepted for scoring and parent finite inputs are missing",
        ),
        (
            "GATE2093_3_PPN_clock_orbital",
            "PPN/clock/orbital branches can be scored",
            "FAIL_BLOCKED",
            "arena projections and residual amplitudes are not source-backed",
        ),
        (
            "GATE2093_4_github_public",
            "this branch is safe as a public local-GR proof",
            "FAIL_BLOCKED",
            "acceptable as private checkpoint only; public prose would need postulate labeling and caveats",
        ),
    ]
    return [
        row(
            gate_id=gate_id,
            claim=claim,
            status=status,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2093_0_result",
            decision="PRIVATE_WORKING_AXIOM_PLUS_FINITE_INPUT_PIVOT",
            basis="2092 micro-kernel is the cleanest known local coupling engine, but current corpus does not derive it from deeper primitives.",
            consequence="use it privately as a labelled working branch while forcing every open term into finite source-backed rows.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2093_1_no_public_derivation",
            decision="DO_NOT_CALL_LOCAL_GR_DERIVED",
            basis="extra V_R terms, Z_R/M_R2 residuals, S_R sources, Q_R hair, boundary terms and readout reentry remain logically open.",
            consequence="any public-facing statement must say postulate candidate or closure template, not proof.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2093_2_next_operation",
            decision="START_FIRST_FINITE_LOCAL_INPUT_ROW",
            basis="another derivation pass without a new object-language source risks circling the same joint.",
            consequence="2094 should attack Q_R/q_R_hat no-charge or bound first, then Z_R/M_R2 and source/boundary/arena rows.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2093_0_2094",
            target_doc="2094-Y5-R2FR-first-finite-local-input-source-row-qR-or-ZR.md",
            target_script="scripts/Y5_R2FR_first_finite_local_input_source_row_qR_or_ZR_2094.py",
            objective="acquire, derive, or explicitly fail the first source-backed finite local input row, prioritizing Q_R/q_R_hat no-charge or bound before Z_R/M_R2 if the no-charge theorem is reachable",
            success_condition="one strict row becomes theorem-zero/source-backed, or the row is blocked with exact missing parent input; no local-test score unless all dependent rows are ready",
            forbidden_shortcuts="placeholder coefficients; cancellation between siblings; using R10 candidate curve as accepted evidence; importing Schwarzschild/GR as proof; GitHub; formalization-workbench edits",
            claim_allowed=False,
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    axiom_review: list[dict[str, object]],
    options: list[dict[str, object]],
    finite: list[dict[str, object]],
    priority: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_RADIAL_MICRO_KERNEL_AXIOM_REVIEW_2093_NONCLAIM.csv",
            axiom_review + options + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2093_AXIOM_REVIEW_NONCLAIM.csv",
            axiom_review + finite + decisions,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2093_FINITE_LOCAL_INPUT_PRIORITY_QUEUE.csv",
            priority + finite + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2093_{len(rows)}",
                copy_kind=copy_kind,
                path=str(path),
                rows=len(data_rows),
                parses=csv_rows_parse(path),
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    axiom_review: list[dict[str, object]],
    options: list[dict[str, object]],
    finite: list[dict[str, object]],
    priority: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    axiom_review_ok = any(
        r["review_id"] == "AXR2093_1_derivation" and r["verdict"] == "FAIL_CURRENT_PARENT_DERIVATION"
        for r in axiom_review
    ) and any(
        r["review_id"] == "AXR2093_4_recommendation" and r["verdict"] == "PRIVATE_WORKING_AXIOM_PLUS_FINITE_INPUT_PIVOT"
        for r in axiom_review
    )
    options_ok = any(r["option_id"] == "OPT2093_B_explicit_axiom" and truthy(r["selected"]) for r in options) and any(
        r["option_id"] == "OPT2093_C_finite_input_pivot" and truthy(r["selected"]) for r in options
    )
    finite_refuses = all(str(r["result"]).startswith(("REFUSED", "NO_LOCAL")) for r in finite)
    finite_no_score = all(csv_true_count(safe_read_csv(Path(str(r["source_path"]))), "score_ready") == 0 for r in finite if Path(str(r["source_path"])).exists())
    priority_ok = priority[0]["priority_id"] == "PRI2093_0_qR_QR_no_charge" and len(priority) >= 5
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and any(
        r["gate_id"] == "GATE2093_0_public_local_GR" and r["status"] == "FAIL_BLOCKED" for r in gates
    )
    decisions_ok = any(r["decision_id"] == "DEC2093_0_result" for r in decisions) and any(
        r["decision_id"] == "DEC2093_2_next_operation" for r in decisions
    )
    next_ok = next_rows_[0]["target_id"] == "NEXT2093_0_2094"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, axiom_review, options, finite, priority, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2093_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2093_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2093_01_axiom_review", axiom_review_ok, "axiom review records derivation failure and private working pivot"),
        ("VAL2093_02_options", options_ok, "selected path is explicit axiom candidate plus finite-input pivot"),
        ("VAL2093_03_finite_refusal", finite_refuses, "finite runner refuses all non-source-backed scores"),
        ("VAL2093_04_finite_no_score", finite_no_score, "source CSVs contain no score-ready local finite rows"),
        ("VAL2093_05_priority", priority_ok, "priority queue starts with Q_R/q_R_hat no-charge or bound"),
        ("VAL2093_06_claim_gates", gates_safe, "claim gates block public local-GR/R10/PPN/clock/orbital claims"),
        ("VAL2093_07_decisions", decisions_ok, "decision ledger selects finite local input acquisition"),
        ("VAL2093_08_next", next_ok, "next target is 2094 first finite local input source row"),
        ("VAL2093_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2093_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2093_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2093_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2093"),
        ("VAL2093_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, claim_allowed=False, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2093_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2093 keeps the radial micro-kernel as a private working axiom candidate and pivots to strict finite local input acquisition" if overall else "one or more 2093 validation gates failed",
            claim_allowed=False,
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    axiom_review: list[dict[str, object]],
    options: list[dict[str, object]],
    finite: list[dict[str, object]],
    priority: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2093 - Y5/R2FR Radial Micro-Kernel Axiom Review Or Finite Local Input Runner",
            "## Current Verdict\n\n2093 makes the night-shift decision explicit: the radial micro-kernel is still one of the best-looking local routes, because it cleanly owns the missing selector coupling, but it is not yet derived from deeper MTS primitives. The honest working stance is therefore `PRIVATE_WORKING_AXIOM_PLUS_FINITE_INPUT_PIVOT`: keep the micro-kernel as a labelled private parent-axiom candidate, refuse public local-GR/R10/PPN claims, and start acquiring strict finite local input rows.\n\nThis is not a dead end. It is the joint in the machine. Either a future parent action derives this block, or the finite residual programme bounds every open term hard enough that the branch becomes empirically disciplined.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2093", "claim_allowed", "valid_for_claim"]),
            "## Axiom Review",
            md_table(axiom_review, ["review_id", "question", "answer", "evidence", "risk", "verdict", "claim_allowed", "valid_for_claim"]),
            "## Adoption Options",
            md_table(options, ["option_id", "option", "upside", "downside", "present_status", "selected", "claim_allowed", "valid_for_claim"]),
            "## Finite Input Runner",
            md_table(finite, ["run_id", "source_path", "rows_read", "observed_status", "missing_or_blocked", "accepted_for_scoring_count", "score_ready_count", "passes_for_claim_count", "result", "next_action", "claim_allowed", "valid_for_claim"]),
            "## Priority Queue",
            md_table(priority, ["priority_id", "target_quantity", "why_first", "acceptable_evidence", "failure_mode", "next_action", "claim_allowed", "valid_for_claim"]),
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
    axiom_review = axiom_review_rows()
    options = adoption_option_rows()
    finite = finite_runner_rows()
    priority = priority_queue_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2093_SOURCE_REGISTER.csv",
        "axiom": OUT / "P8_Y5_PARENT_QLOC_2093_AXIOM_REVIEW.csv",
        "options": OUT / "P8_Y5_PARENT_QLOC_2093_ADOPTION_OPTIONS.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2093_FINITE_INPUT_RUNNER.csv",
        "priority": OUT / "P8_Y5_PARENT_QLOC_2093_FINITE_LOCAL_PRIORITY_QUEUE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2093_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2093_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2093_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2093_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2093_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["axiom"], axiom_review)
    write_csv(paths["options"], options)
    write_csv(paths["finite"], finite)
    write_csv(paths["priority"], priority)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(axiom_review, options, finite, priority, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, axiom_review, options, finite, priority, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, axiom_review, options, finite, priority, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
