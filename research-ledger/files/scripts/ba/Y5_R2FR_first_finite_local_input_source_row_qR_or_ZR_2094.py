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


DOC = ROOT / "2094-Y5-R2FR-first-finite-local-input-source-row-qR-or-ZR.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

QRHAT_1255 = ROOT / "source-intake" / "qr-hat" / "raw" / "QRHAT1255_CASSINI_GAMMA_PHENOMENOLOGICAL_BOUND_NONCLAIM.csv"
PPN_1181 = OUT / "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv"
PPN_1691 = ROOT / "1691-Y5-R2FR-PPN-residual-vector-or-qRhat-source-row.md"
FINITE_1577 = ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md"
NEUTRALITY_06 = ROOT / "06-reciprocal-charge-source-neutrality.md"
CELL_CURRENT_11 = ROOT / "11-cell-current-origin-attempt.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def safe_read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def formalization_has_2094_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2094-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2094*",
        "*Y5_R2FR_first_finite_local_input_source_row_qR_or_ZR_2094*",
        "*AFRAME_QRHAT_FIRST_FINITE_INPUT_2094*",
        "*JR2094_QRHAT_OR_ZR_NEXT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2094_00_2093_handoff",
            ROOT / "2093-Y5-R2FR-radial-micro-kernel-axiom-review-or-finite-local-input-runner.md",
            ["NEXT2093_0_2094", "PRI2093_0_qR_QR_no_charge", "VAL2093_OVERALL"],
            "2093 selects Q_R/q_R_hat no-charge or bound as the first finite local input target.",
        ),
        (
            "SRC2094_01_1577_current_gate",
            FINITE_1577,
            ["NCA1577_4_verdict", "FCF1577_0_qRhat", "VAL1577_OVERALL"],
            "1577 records that radial current conservation gives Q_R constant but no Q_R=0 theorem.",
        ),
        (
            "SRC2094_02_06_neutrality",
            NEUTRALITY_06,
            ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "Q_R neutrality is the missing source theorem"],
            "06 gives the sufficient source-neutrality route and flags it as the missing theorem.",
        ),
        (
            "SRC2094_03_11_cell_current",
            CELL_CURRENT_11,
            ["cell_current_origin_no_charge_obstruction", "Q_R = constant.", "generically carries Q_R hair"],
            "11 proves ordinary cell current preserves reciprocal hair unless Q_R=0 is separately proven.",
        ),
        (
            "SRC2094_04_1691_ppn_bridge",
            PPN_1691,
            ["PPNV1691_2_qRhat_definition", "PPNV1691_4_current_hair_projection", "VAL1691_OVERALL"],
            "1691 defines q_R_hat and its conditional current-hair bridge to Q_R/(G*M).",
        ),
        (
            "SRC2094_05_1255_qrhat_bound",
            QRHAT_1255,
            ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "4.6e-05", "https://pubmed.ncbi.nlm.nih.gov/14508481/"],
            "1255 provides a nonclaim Cassini q_R_hat comparator ceiling.",
        ),
        (
            "SRC2094_06_1181_ppn_source",
            PPN_1181,
            ["SRC1181W_0_Cassini_gamma", "gamma = 1 + (2.1 +/- 2.3) x 10^-5", "source_backed_from_pubmed_abstract"],
            "1181 records the external Cassini gamma comparator provenance.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2094_qRhat_first_finite_input_source",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2094=note,
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return rows


def nocharge_theorem_rows() -> list[dict[str, object]]:
    return [
        row(
            attempt_id="QZ2094_0_current_equation",
            clause="radial current equation",
            statement="partial_r(W_R partial_r R_AB)=0 implies W_R partial_r R_AB=Q_R.",
            result="DERIVES_CONSTANT_CHARGE_ONLY",
            missing_for_zero="a separate source/boundary/constraint theorem setting Q_R=0",
            zero_theorem_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            attempt_id="QZ2094_1_outer_normalization",
            clause="asymptotic/exterior normalization",
            statement="R_AB(infinity)=0 fixes the additive mode but allows R_AB approximately -Q_R/r if Q_R is nonzero.",
            result="DOES_NOT_KILL_HAIR",
            missing_for_zero="boundary no-charge or source neutrality, not just falloff",
            zero_theorem_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            attempt_id="QZ2094_2_source_neutrality",
            clause="source reciprocal neutrality",
            statement="Pi_R=0 is sufficient: Q_R=-Pi_R, so Pi_R=0 implies Q_R=0 and then R_AB=0.",
            result="SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            missing_for_zero="parent matter/source action must prove Pi_R=0 for the protected local source class",
            zero_theorem_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            attempt_id="QZ2094_3_auxiliary_constraint",
            clause="auxiliary/nonpropagating route",
            statement="A parent-owned algebraic compatibility constraint could remove the Q_R integration mode before the current forms.",
            result="POSSIBLE_ROUTE_NOT_AVAILABLE",
            missing_for_zero="parent action, constraint algebra, boundary term and readout silence",
            zero_theorem_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            attempt_id="QZ2094_4_readout_tail_silence",
            clause="gauge/source/boundary/readout tails",
            statement="Even if q_R_hat is zeroed, gamma residual scoring needs all tails theorem-zero or absolutely bounded.",
            result="TAIL_GATE_OPEN",
            missing_for_zero="delta_gauge, delta_source, delta_boundary, delta_readout and O(U_N) envelope",
            zero_theorem_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            attempt_id="QZ2094_5_verdict",
            clause="Q_R zero theorem",
            statement="No current source provides a noncircular parent-signed theorem that Q_R=0.",
            result="ZERO_THEOREM_FAIL_CURRENT_CORPUS",
            missing_for_zero="source-neutral boundary theorem or parent constraint that removes reciprocal hair",
            zero_theorem_signed=False,
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def qrhat_bound_review_rows() -> list[dict[str, object]]:
    raw_rows = safe_read_csv(QRHAT_1255)
    if not raw_rows:
        return [
            row(
                review_id="QRB2094_0_missing_raw",
                candidate_id="MISSING_QRHAT1255",
                route_type="missing",
                q_R_hat_bound="MISSING",
                units="MISSING",
                source_path=str(QRHAT_1255),
                external_source_url="MISSING",
                comparator_source_backed=False,
                mts_prediction_present=False,
                result="BOUND_ROW_MISSING",
                score_ready=False,
                claim_allowed=False,
                valid_for_claim=False,
            )
        ]
    reviewed: list[dict[str, object]] = []
    for idx, raw in enumerate(raw_rows):
        q_bound = raw.get("q_R_hat", "")
        source_path = raw.get("source_path", "")
        source_exists = (ROOT / source_path).exists() if source_path and not Path(source_path).is_absolute() else Path(source_path).exists()
        reviewed.append(
            row(
                review_id=f"QRB2094_{idx}_cassini_bound",
                candidate_id=raw.get("candidate_id", ""),
                route_type=raw.get("route_type", ""),
                q_R_hat_bound=q_bound,
                units=raw.get("q_R_hat_units", ""),
                source_path=source_path,
                source_path_exists=source_exists,
                external_source_url=raw.get("external_source_url", ""),
                comparator_source_backed=source_exists and "pubmed" in raw.get("external_source_url", "").lower(),
                mts_prediction_present=False,
                zero_theorem_statement=raw.get("zero_theorem_statement", ""),
                input_kind=raw.get("input_kind", ""),
                bound_direction=raw.get("bound_direction", ""),
                result="COMPARATOR_BOUND_SOURCED_NONCLAIM_MTS_PREDICTION_MISSING",
                score_ready=False,
                claim_allowed=False,
                valid_for_claim=False,
            )
        )
    return reviewed


def first_input_rows() -> list[dict[str, object]]:
    return [
        row(
            input_id="QRI2094_0_qRhat_definition",
            quantity="q_R_hat",
            definition="q_R_hat:=R_AB^(1)/(2*U_N)",
            source="1691 PPN residual vector",
            current_value="MISSING_MTS_VALUE",
            units="dimensionless",
            source_backed=False,
            theorem_zero=False,
            score_ready=False,
            current_status="FORMAL_DEFINITION_VALUE_MISSING",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            input_id="QRI2094_1_current_hair_projection",
            quantity="Q_R/(kappa_W*G*M)",
            definition="if W=kappa_W*r^2 then q_R_hat=-Q_R/(2*kappa_W*G*M)+tails+O(GM/r)",
            source="1691 conditional current-hair bridge",
            current_value="MISSING_Q_R_KAPPA_W_GM_AND_TAILS",
            units="dimensionless after source normalization",
            source_backed=False,
            theorem_zero=False,
            score_ready=False,
            current_status="FORMAL_BRIDGE_DENOMINATOR_MISSING",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            input_id="QRI2094_2_Cassini_ceiling",
            quantity="abs(q_R_hat)_ceiling",
            definition="phenomenological comparator ceiling from Cassini gamma row",
            source=str(QRHAT_1255),
            current_value="4.6e-05",
            units="dimensionless",
            source_backed=True,
            theorem_zero=False,
            score_ready=False,
            current_status="COMPARATOR_ONLY_NOT_THEORY_INPUT",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            input_id="QRI2094_3_tail_envelope",
            quantity="delta_gauge+delta_source+delta_boundary+delta_readout+O(U_N)",
            definition="absolute envelope required before comparing q_R_hat to gamma",
            source="1691 residual vector and 1577 finite-component rows",
            current_value="MISSING_COMPONENT_VALUES",
            units="dimensionless",
            source_backed=False,
            theorem_zero=False,
            score_ready=False,
            current_status="TAIL_VALUES_MISSING",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            input_id="QRI2094_4_first_input_verdict",
            quantity="first finite local q_R_hat input",
            definition="a source-backed MTS q_R_hat value/theorem-zero or bound-ready prediction row",
            source="combined qR/nocharge/PPN bridge audit",
            current_value="BLOCKED",
            units="dimensionless",
            source_backed=False,
            theorem_zero=False,
            score_ready=False,
            current_status="MTS_QRHAT_INPUT_ROW_BLOCKED_EXACT_MISSING_PARENT_INPUTS",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        (
            "GATE2094_0_QR_zero",
            "Q_R=0 is parent-derived",
            "FAIL_BLOCKED",
            "ordinary current gives Q_R constant; Pi_R=0/source neutrality is sufficient but unsigned",
        ),
        (
            "GATE2094_1_qRhat_bound",
            "q_R_hat has a source-backed external comparator bound",
            "PASS_COMPARATOR_ONLY",
            "Cassini-derived ceiling exists as nonclaim comparator, not as MTS prediction",
        ),
        (
            "GATE2094_2_qRhat_prediction",
            "MTS has a q_R_hat prediction row",
            "FAIL_BLOCKED",
            "Q_R, kappa_W, same-frame GM and tails are missing",
        ),
        (
            "GATE2094_3_gamma_score",
            "PPN gamma/Cassini score is allowed",
            "FAIL_BLOCKED",
            "score requires q_R_hat prediction plus absolute tails, not only comparator data",
        ),
        (
            "GATE2094_4_local_GR",
            "local GR/Newton is derived from q_R_hat branch",
            "FAIL_BLOCKED",
            "gamma alone is insufficient and beta/conservation/matter/source-normalized Newton remain open",
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
            decision_id="DEC2094_0_nocharge",
            decision="Q_R_ZERO_THEOREM_NOT_DERIVED",
            basis="current conservation preserves Q_R hair; source-neutral Pi_R=0 would kill it but is not parent-signed.",
            consequence="do not set q_R_hat=0 by closure or asymptotic flatness.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2094_1_bound",
            decision="CASSINI_QRHAT_CEILING_AVAILABLE_COMPARATOR_ONLY",
            basis="QRHAT1255 records abs(q_R_hat)<=4.6e-05 from the source-backed Cassini gamma comparator.",
            consequence="use it as a pressure-test ceiling once MTS supplies Q_R/kappa_W/GM/tails; no score now.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2094_2_first_input",
            decision="FIRST_QRHAT_INPUT_ROW_BLOCKED_WITH_EXACT_MISSING_PARENT_INPUTS",
            basis="MTS q_R_hat value needs Q_R or no-charge theorem, kappa_W, source-normalized GM and tail envelope.",
            consequence="2094 is a clean fail/acquire step, not a proof failure of the whole programme.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2094_3_next",
            decision="MOVE_TO_ZR_MR2_OPERATOR_SIGNATURE",
            basis="continuing to ask current conservation to kill Q_R would circle the same obstruction.",
            consequence="next attack should test whether the radial residual is an auxiliary/no-pole branch or a finite operator with Z_R/M_R^2.",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2094_0_2095",
            target_doc="2095-Y5-R2FR-ZR-MR2-operator-signature-source-row.md",
            target_script="scripts/Y5_R2FR_ZR_MR2_operator_signature_source_row_2095.py",
            objective="derive, source, or explicitly fail the Z_R/M_R^2 radial operator signature: theorem-zero/no-pole, positive finite operator, or missing parent Hessian/kinetic block",
            success_condition="operator row becomes parent-signed theorem-zero/source-backed finite input, or is blocked with exact missing parent action terms; no local-test score unless q_R/Q_R, source, boundary and arena rows also close",
            forbidden_shortcuts="invented Z_R or M_R^2; treating positive range as no coupling; importing GR; cancellation between unknown tails; GitHub; formalization-workbench edits",
            claim_allowed=False,
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    nocharge: list[dict[str, object]],
    bounds: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_QRHAT_FIRST_FINITE_INPUT_2094_NONCLAIM.csv",
            nocharge + bounds + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2094_QRHAT_GATE_NONCLAIM.csv",
            nocharge + inputs + gates,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2094_QRHAT_OR_ZR_NEXT_QUEUE.csv",
            inputs + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2094_{len(rows)}",
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
    nocharge: list[dict[str, object]],
    bounds: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    nocharge_fail_ok = any(
        r["attempt_id"] == "QZ2094_5_verdict" and r["result"] == "ZERO_THEOREM_FAIL_CURRENT_CORPUS"
        for r in nocharge
    ) and all(not truthy(r["zero_theorem_signed"]) for r in nocharge)
    comparator_ok = any(
        r["review_id"].startswith("QRB2094_") and r["q_R_hat_bound"] == "4.6e-05" and truthy(r["comparator_source_backed"])
        for r in bounds
    )
    first_input_blocked = any(
        r["input_id"] == "QRI2094_4_first_input_verdict"
        and r["current_status"] == "MTS_QRHAT_INPUT_ROW_BLOCKED_EXACT_MISSING_PARENT_INPUTS"
        for r in inputs
    )
    no_score_ready = all(not truthy(r.get("score_ready")) for r in bounds + inputs)
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and any(
        r["gate_id"] == "GATE2094_2_qRhat_prediction" and r["status"] == "FAIL_BLOCKED" for r in gates
    )
    decision_ok = any(r["decision_id"] == "DEC2094_3_next" and r["decision"] == "MOVE_TO_ZR_MR2_OPERATOR_SIGNATURE" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2094_0_2095"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, nocharge, bounds, inputs, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2094_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2094_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2094_01_nocharge_fail", nocharge_fail_ok, "Q_R zero theorem fails current corpus and is not promoted"),
        ("VAL2094_02_comparator_bound", comparator_ok, "Cassini q_R_hat comparator ceiling is present and sourced"),
        ("VAL2094_03_first_input_blocked", first_input_blocked, "MTS q_R_hat input row is blocked with exact missing parent inputs"),
        ("VAL2094_04_no_score_ready", no_score_ready, "no q_R_hat row is score-ready or claim-ready"),
        ("VAL2094_05_claim_gates", gates_safe, "claim gates block q_R_hat prediction, PPN score and local-GR claim"),
        ("VAL2094_06_decision", decision_ok, "decision moves next to Z_R/M_R^2 operator signature"),
        ("VAL2094_07_next", next_ok, "next target is 2095 Z_R/M_R^2 operator signature"),
        ("VAL2094_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2094_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2094_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2094_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2094"),
        ("VAL2094_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, claim_allowed=False, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2094_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2094 fails Q_R theorem-zero honestly, preserves Cassini q_R_hat as comparator-only, and pivots to Z_R/M_R^2 operator signature" if overall else "one or more 2094 validation gates failed",
            claim_allowed=False,
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    nocharge: list[dict[str, object]],
    bounds: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2094 - Y5/R2FR First Finite Local Input Source Row: qR Or ZR",
            "## Current Verdict\n\n2094 takes the first finite local input target seriously. The `Q_R/q_R_hat` branch does **not** close as a theorem-zero: ordinary radial current conservation gives a constant reciprocal charge, not `Q_R=0`. The source-neutral route `Pi_R=0 -> Q_R=0` remains sufficient but unsigned by the parent matter/source action.\n\nThe useful progress is that the PPN-facing comparator side is real enough for pressure testing later: the existing Cassini scaffold gives `abs(q_R_hat)<=4.6e-05` as a source-backed **comparator-only** ceiling. But MTS still lacks the theory-side prediction row: `Q_R`, `kappa_W`, same-frame `G*M`, and gauge/source/boundary/readout tails are missing. So 2094 blocks scoring and moves the next attack to the radial operator signature `Z_R/M_R^2`, rather than circling the same no-charge obstruction.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2094", "claim_allowed", "valid_for_claim"]),
            "## Q_R No-Charge Theorem Attempt",
            md_table(nocharge, ["attempt_id", "clause", "statement", "result", "missing_for_zero", "zero_theorem_signed", "claim_allowed", "valid_for_claim"]),
            "## q_R_hat Comparator Bound Review",
            md_table(bounds, ["review_id", "candidate_id", "route_type", "q_R_hat_bound", "units", "source_path", "source_path_exists", "external_source_url", "comparator_source_backed", "mts_prediction_present", "result", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## First Finite Input Rows",
            md_table(inputs, ["input_id", "quantity", "definition", "source", "current_value", "units", "source_backed", "theorem_zero", "score_ready", "current_status", "claim_allowed", "valid_for_claim"]),
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
    nocharge = nocharge_theorem_rows()
    bounds = qrhat_bound_review_rows()
    inputs = first_input_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2094_SOURCE_REGISTER.csv",
        "nocharge": OUT / "P8_Y5_PARENT_QLOC_2094_QR_NOCHARGE_THEOREM_ATTEMPT.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2094_QRHAT_COMPARATOR_BOUND_REVIEW.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2094_FIRST_FINITE_QRHAT_INPUT_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2094_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2094_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2094_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2094_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2094_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["nocharge"], nocharge)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["inputs"], inputs)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(nocharge, bounds, inputs, gates, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, nocharge, bounds, inputs, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, nocharge, bounds, inputs, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
