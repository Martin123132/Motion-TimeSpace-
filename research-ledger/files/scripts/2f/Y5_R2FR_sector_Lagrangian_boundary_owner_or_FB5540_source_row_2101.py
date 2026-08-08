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


DOC = ROOT / "2101-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2100 = ROOT / "2100-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md"
SRC_1842 = ROOT / "1842-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
SRC_1843 = ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md"
SRC_1844 = ROOT / "1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"
SRC_1845 = ROOT / "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
SRC_1846 = ROOT / "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
SRC_1847 = ROOT / "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"
SRC_1848 = ROOT / "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"
SRC_1849 = ROOT / "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md"

CSV_1842_OWNER = OUT / "P8_Y5_PARENT_QLOC_1842_OWNER_CLAUSES.csv"
CSV_1842_FSR = OUT / "P8_Y5_PARENT_QLOC_1842_FB5540_SOURCE_ROW_SCHEMA.csv"
CSV_1843_DEC = OUT / "P8_Y5_PARENT_QLOC_1843_DECISION_LEDGER.csv"
CSV_1844_DEC = OUT / "P8_Y5_PARENT_QLOC_1844_DECISION_LEDGER.csv"
CSV_1845_DEC = OUT / "P8_Y5_PARENT_QLOC_1845_DECISION_LEDGER.csv"
CSV_1846_ALPHA = OUT / "P8_Y5_PARENT_QLOC_1846_ALPHA_COEFFICIENT_ROWS.csv"
CSV_1847_DEC = OUT / "P8_Y5_PARENT_QLOC_1847_DECISION_LEDGER.csv"
CSV_1848_SOURCE_ZERO = OUT / "P8_Y5_PARENT_QLOC_1848_SOURCE_ZERO_RETURN.csv"
CSV_1849_DEC = OUT / "P8_Y5_PARENT_QLOC_1849_DECISION_LEDGER.csv"
CSV_1849_QBAR = OUT / "P8_Y5_PARENT_QLOC_1849_QBARXT_COMPONENT_ENVELOPE.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2101_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2101-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2101*",
        "*Y5_R2FR_sector_Lagrangian_boundary_owner_or_FB5540_source_row_2101*",
        "*AFRAME_SECTOR_OWNER_FB5540_2101*",
        "*JR2101_FRAME_MARKER_COUPLING*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2101_00_2100_handoff",
            SRC_2100,
            ["NEXT2100_0_2101", "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_NEXT", "VAL2100_OVERALL"],
            "2100 hands off from narrowed WEP to sector Lagrangian/boundary owner for GR/Newton reduction.",
        ),
        (
            "SRC2101_01_1842_owner",
            CSV_1842_OWNER,
            ["LOC1842_0_LX_owner", "LOC1842_7_MHref_owner", "LOC1842_8_verdict"],
            "1842 owner clauses define the Hamiltonian/source charge owner map.",
        ),
        (
            "SRC2101_02_1842_fb5540",
            CSV_1842_FSR,
            ["FSR1842_0_M_H_ref", "FSR1842_7_total_guard", "MISSING_STABLE_MH_REF"],
            "1842 FB5540 source schema lists required denominator and numerator rows.",
        ),
        (
            "SRC2101_03_1843_boundary_decision",
            CSV_1843_DEC,
            ["BOUNDARY_PROJECTOR_ROUTE_PRECISE_BUT_NOT_CLOSED", "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT"],
            "1843 says boundary/projector route needs an explicit B_X primitive or full source pack.",
        ),
        (
            "SRC2101_04_1844_bx_decision",
            CSV_1844_DEC,
            ["explicit B_X primitive", "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"],
            "1844 fails the B_X primitive and splits quotient/no-hair routes.",
        ),
        (
            "SRC2101_05_1845_quotient_decision",
            CSV_1845_DEC,
            ["q/v_X/action descent certificate does not close", "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"],
            "1845 demotes the active local branch to scalar no-hair/source-coefficient work.",
        ),
        (
            "SRC2101_06_1846_alpha_rows",
            CSV_1846_ALPHA,
            ["ALPHA1846_0_bulk_operator", "ALPHA1846_5_no_cancellation_guard", "MISSING_ARENA_PROJECTION"],
            "1846 stages scalar no-hair/residual-alpha rows but no values.",
        ),
        (
            "SRC2101_07_1847_hessian_decision",
            CSV_1847_DEC,
            ["exact parent Xhat/Hessian/range contract", "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"],
            "1847 derives the second-variation/range contract but does not own Xhat/Hessian.",
        ),
        (
            "SRC2101_08_1848_source_zero",
            CSV_1848_SOURCE_ZERO,
            ["SZR1848_2_qbar_XT", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW", "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md"],
            "1848 freezes finite metric/eigenvalue route and returns to qbar_XT/J_X source-zero or bounded coupling.",
        ),
        (
            "SRC2101_09_1849_decision",
            CSV_1849_DEC,
            ["qbar_XT=0/J_X=0 is an exact conditional theorem", "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"],
            "1849 narrows the coupling gap to frame/marker/no-marker theorem or bound input pack.",
        ),
        (
            "SRC2101_10_1849_qbar_components",
            CSV_1849_QBAR,
            ["QBC1849_0_qbar_geom", "QBC1849_5_total_abs_guard", "MISSING"],
            "1849 qbarXT component envelope provides current source-row decomposition.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2101_sector_owner_FB5540_GR_bridge",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2101=use,
                valid_for_claim=False,
            )
        )
    return rows


def owner_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("OWN2101_0_LX", "L_X owner", "parent-owned extra-sector Lagrangian with operator, source term, normalization and boundary conditions", "NOT_SIGNED", "Theta_X/Q_X, R10/R11 and local scaling cannot be computed"),
        ("OWN2101_1_Theta_Q", "Theta_X/Q_X owner", "delta L_X=E_X delta X+dTheta_X and J_tau^X=dQ_tau^X+C_tau^X", "FORMULA_WRITTEN_NOT_OWNED", "Hamiltonian integrability remains schematic"),
        ("OWN2101_2_Bref", "B_ref owner", "reference boundary functional selected before readout and derivative-silent under source/range/frame changes", "NOT_SIGNED", "reference can absorb source calibration"),
        ("OWN2101_3_Bclass", "boundary class/no-hair/projector silence", "B_class plus exact/proper-gauge/no-vector-tensor-hair conditions", "NOT_SIGNED", "symplectic boundary flux and edge charge remain live"),
        ("OWN2101_4_tau", "tau/source/clock/readout lock", "same generator for source, charge, clocks and readout up to sourced mismatch bound", "NOT_SIGNED", "Hamiltonian source charge and empirical readout can drift apart"),
        ("OWN2101_5_MHref", "M_H_ref same-frame denominator", "M_H_ref=H_tau[S_outer]-H_ref positive and fixed before orbital readout", "MISSING_STABLE_MH_REF", "FB5540/source-normalization rows are unnormalized"),
        ("OWN2101_6_verdict", "sector owner map closure", "all owner clauses close together in one parent action and boundary class", "OWNER_MAP_SHARP_BUT_NOT_CLOSED", "no FB5540/R10/R11/Newton/local-GR promotion"),
    ]
    return [
        row(
            owner_id=owner_id,
            owner=owner,
            required_statement=statement,
            current_status=status,
            failure_if_missing=failure,
            source_backed=False,
            theorem_zero_signed=False,
            valid_for_claim=False,
        )
        for owner_id, owner, statement, status, failure in specs
    ]


def route_ladder_rows() -> list[dict[str, object]]:
    specs = [
        ("LAD2101_0_1842_owner", "sector owner map", "sharp owner map but not closed", "FB5540 source row schema staged", "boundary exactness/projector route"),
        ("LAD2101_1_1843_boundary", "boundary exactness/projector orthogonality", "precise but not closed", "weighted Stokes/source pack required", "B_X primitive"),
        ("LAD2101_2_1844_BX", "B_X primitive", "not derivable from current parent variation", "EDGEBOUND terms retained", "vertical quotient or scalar no-hair choice"),
        ("LAD2101_3_1845_quotient", "vertical quotient/no-pole", "q/v_X/action descent certificate fails current branch", "quotient route can reopen only with one parent certificate", "scalar no-hair/input pack"),
        ("LAD2101_4_1846_scalar", "scalar no-hair", "exact conditional but all owner/sign/source/boundary inputs missing", "alpha/source rows staged nonclaim", "parent Xhat/Hessian owner"),
        ("LAD2101_5_1847_Xhat", "parent Xhat/Hessian/range", "second-variation/range law exact but not owned", "alpha/source row remains empty", "parent metric/eigenvalue or source-zero return"),
        ("LAD2101_6_1848_metric", "parent metric/beta eigenvalue", "M_AB and beta route unowned; finite route demoted", "source-zero/bounded coupling selected", "qbar_XT/J_X source-zero"),
        ("LAD2101_7_1849_qbar", "qbar_XT/J_X source-zero", "exact conditional theorem but not current result", "qbar component envelope staged", "frame/marker no-marker theorem or bound inputs"),
    ]
    return [
        row(
            ladder_id=ladder_id,
            route=route,
            current_result=result,
            retained_fallback=fallback,
            next_pressure_point=next_point,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for ladder_id, route, result, fallback, next_point in specs
    ]


def fb5540_source_rows() -> list[dict[str, object]]:
    specs = [
        ("FSR2101_0_M_H_ref", "M_H_ref", "same-frame Hamiltonian source denominator", "MISSING_STABLE_MH_REF"),
        ("FSR2101_1_delta_H_tau", "delta_H_tau_nonintegrable_over_MH", "field-space curl of Hamiltonian variation normalized by M_H_ref", "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO"),
        ("FSR2101_2_Delta_ref", "Delta_ref_over_MH", "reference shift/derivative profile normalized by M_H_ref", "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO"),
        ("FSR2101_3_boundary_flux", "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp", "boundary/projector/non-EH linked flux normalized by M_H_ref", "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO"),
        ("FSR2101_4_LX_bulk", "Z_X;M_X2;J_X;lambda_X", "bulk X-sector coefficients if no theorem-zero route closes", "MISSING_PARENT_INPUT"),
        ("FSR2101_5_R10_projection", "K_X;Qbar_XH;qbar_XT", "R10 residual amplitude factors for active X exchange", "MISSING_ARENA_PROJECTION"),
        ("FSR2101_6_edge_projection", "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT", "edge/boundary residual amplitude factors if boundary theorem fails", "MISSING_EDGE_COEFFICIENTS"),
        ("FSR2101_7_total_guard", "FB5540_alpha_R11_total_guard", "absolute no-cancellation envelope across FB5540, bulk X, edge X and R11 coefficients", "NOT_COMPUTED_COMPONENTS_MISSING"),
    ]
    return [
        row(
            source_row_id=row_id,
            quantity=quantity,
            definition=definition,
            current_status=status,
            required_evidence="theorem-zero or source-backed nonclaim row with units, signs, source path and no-cancellation bookkeeping",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        )
        for row_id, quantity, definition, status in specs
    ]


def qbar_coupling_rows() -> list[dict[str, object]]:
    specs = [
        ("QBR2101_0_geom", "qbar_geom", "ordinary test-body X charge from observed metric/coframe leakage", "MISSING_GEOMETRY_PULLBACK_ZERO_OR_BOUND"),
        ("QBR2101_1_constants", "qbar_constants", "ordinary test-body X charge from masses, charges, alpha_EM, clocks or representation constants", "MISSING_CONSTANT_DESCENT_ZERO_OR_BOUND"),
        ("QBR2101_2_marker", "qbar_marker", "source/test charge from material markers, hidden frames or direct matter-X response", "MISSING_NO_MARKER_THEOREM_OR_BOUND"),
        ("QBR2101_3_source_weight", "qbar_source_weight", "relative species/class source-only weight in the source map", "MISSING_SOURCE_WEIGHT_ZERO_OR_BOUND"),
        ("QBR2101_4_nonH", "qbar_nonH", "non-Hilbert, boundary, connection, domain or support-shift contribution", "MISSING_NONHILBERT_TAIL_ZERO_OR_BOUND"),
        ("QBR2101_5_total_guard", "qbar_XT_bound_abs", "absolute no-cancellation envelope for ordinary test-body X charge", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        row(
            coupling_id=coupling_id,
            quantity=quantity,
            definition=definition,
            current_status=status,
            required_evidence="parent theorem-zero or numeric bound row with units, source path, arena link and no-cancellation guard",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        )
        for coupling_id, quantity, definition, status in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2101_0_owner_map", "sector Lagrangian/boundary owner map is closed", "FAIL_UNSIGNED_OWNER_MAP", "L_X, Theta/Q, B_ref, B_class, tau and M_H_ref remain unsigned"),
        ("GATE2101_1_FB5540", "FB5540 source row can be scored", "FAIL_MISSING_VALUES", "M_H_ref and numerator/source components are missing"),
        ("GATE2101_2_boundary_projector", "boundary/projector theorem kills edge/source leakage", "FAIL_UNSIGNED_BOUNDARY_PROJECTOR", "B_X primitive, cohomology, kernel and reference clauses are not signed"),
        ("GATE2101_3_quotient_no_pole", "vertical quotient removes X before variation", "FAIL_UNSIGNED_QVX_CERTIFICATE", "q, v_X, action descent, matter descent, boundary silence and degree count do not close together"),
        ("GATE2101_4_scalar_finite", "scalar finite-range branch is predictive", "FAIL_MISSING_XHAT_HESSIAN_VALUES", "Xhat, Z_X, M_X2, lambda_X, K_X and source projections remain missing"),
        ("GATE2101_5_qbar_zero_bound", "qbar_XT/J_X is zero or bounded", "FAIL_NEXT_INPUT_MISSING", "frame/marker/no-marker theorem or component bound inputs are missing"),
        ("GATE2101_6_local_GR_Newton", "local GR/Newton recovery is derived", "FAIL_BLOCKED", "source owner, coupling and left-hand operator gates remain incomplete"),
    ]
    return [
        row(gate_id=gate_id, claim=claim, status=status, reason=reason, valid_for_claim=False)
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2101_0_owner_result",
            decision="SECTOR_OWNER_MAP_EXPLICIT_BUT_NOT_CLOSED",
            basis="1842 writes the right owner clauses, but none close as current MTS evidence.",
            consequence="do not claim FB5540, R10/R11, Newton or local GR from symbolic sector machinery.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2101_1_ladder_result",
            decision="ZERO_ROUTES_TESTED_AND_DEMOTED_TO_SOURCE_ROWS",
            basis="1843-1848 test boundary/projector, B_X, quotient/no-pole, scalar no-hair, Xhat/Hessian and metric/beta routes; each remains conditional or missing values.",
            consequence="retain theorem targets, but stop reusing them as proof.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2101_2_coupling_result",
            decision="QBARXT_COUPLING_IS_NOW_COMPONENT_ROW_PROBLEM",
            basis="1849 shows qbar_XT=0 is exact conditional but not current; the fallback component envelope is explicit.",
            consequence="next progress means no-marker theorem or real frame/marker/coupling bound inputs.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2101_3_best_next",
            decision="FRAME_MARKER_COUPLING_BOUND_INPUT_PACK_OR_NO_MARKER_THEOREM_NEXT",
            basis="1849 identifies frame/marker source coupling as the live ordinary-matter/source-zero blocker.",
            consequence="2102 should attack no-marker/constant descent or fill c_g, b_dis, b_A, b_alpha, q_nonH and support-shift rows.",
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2101_0_2102",
            target_doc="2102-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            target_script="scripts/Y5_R2FR_frame_marker_coupling_bound_input_pack_or_no_marker_theorem_2102.py",
            objective="derive the no-marker/constant-descent theorem for ordinary matter, or build claim-blocked c_g, b_dis, b_A, b_alpha, q_nonH and support-shift bound rows with units, source paths and observable links",
            success_condition="no-marker theorem closes, or frame/marker/source bound input pack is complete, source-backed where numeric, and valid_for_claim=false until all gates pass",
            forbidden_shortcuts="local-GR claim; qbar_XT=0 promotion; cancellation between components; source-free coefficient values; measured-G absorption; GitHub; formalization-workbench edits",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    owners: list[dict[str, object]],
    ladder: list[dict[str, object]],
    fb_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_SECTOR_OWNER_FB5540_2101_NONCLAIM.csv",
            owners + ladder + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2101_GR_SOURCE_OWNER_GATE_NONCLAIM.csv",
            fb_rows + qbar_rows,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2101_FRAME_MARKER_COUPLING_NEXT_QUEUE.csv",
            qbar_rows + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2101_{len(rows)}",
                copy_kind=copy_kind,
                path=str(path),
                rows=len(data_rows),
                parses=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    owners: list[dict[str, object]],
    ladder: list[dict[str, object]],
    fb_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    owner_ok = len(owners) == 7 and any(r["owner_id"] == "OWN2101_6_verdict" and r["current_status"] == "OWNER_MAP_SHARP_BUT_NOT_CLOSED" for r in owners)
    ladder_ok = len(ladder) == 8 and ladder[-1]["next_pressure_point"] == "frame/marker no-marker theorem or bound inputs"
    fb_blocked = len(fb_rows) == 8 and all(not truthy(r["source_backed"]) and not truthy(r["score_ready"]) for r in fb_rows)
    qbar_blocked = len(qbar_rows) == 6 and all(not truthy(r["source_backed"]) and not truthy(r["score_ready"]) for r in qbar_rows)
    gates_safe = all(not truthy(r["claim_allowed"]) and str(r["status"]).startswith("FAIL") for r in gates)
    decision_ok = any(r["decision_id"] == "DEC2101_3_best_next" and r["decision"] == "FRAME_MARKER_COUPLING_BOUND_INPUT_PACK_OR_NO_MARKER_THEOREM_NEXT" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2101_0_2102"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, owners, ladder, fb_rows, qbar_rows, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2101_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2101_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2101_01_owner_map", owner_ok, "sector owner map is explicit but not closed"),
        ("VAL2101_02_ladder", ladder_ok, "route ladder reaches frame/marker coupling as current pressure point"),
        ("VAL2101_03_FB5540_rows", fb_blocked, "FB5540/source-normalization rows remain nonclaim and not score-ready"),
        ("VAL2101_04_qbar_rows", qbar_blocked, "qbarXT coupling rows remain nonclaim and not score-ready"),
        ("VAL2101_05_claim_gates", gates_safe, "all claim gates block local-GR/Newton promotion"),
        ("VAL2101_06_decision", decision_ok, "decision selects frame/marker no-marker theorem or bound input pack"),
        ("VAL2101_07_next", next_ok, "next target is 2102 frame/marker coupling"),
        ("VAL2101_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2101_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2101_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2101_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2101"),
        ("VAL2101_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2101_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2101 consolidates the sector owner/FB5540 ladder, blocks local-GR promotion, and selects frame-marker coupling/no-marker theorem next" if overall else "one or more 2101 validation gates failed",
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    owners: list[dict[str, object]],
    ladder: list[dict[str, object]],
    fb_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2101 - Y5/R2FR Sector Lagrangian Boundary Owner Or FB5540 Source Row",
            "## Current Verdict\n\n2101 consolidates the GR/Newton source-owner ladder rather than restarting it. The correct objects are now named: `L_X`, `Theta_X`, `Q_X`, `B_ref`, boundary class, tau lock, and same-frame `M_H_ref`. That owner map is sharp, but it is not closed for current MTS.\n\nThe older 1842-1849 chain already tested the obvious theorem-zero exits: boundary/projector exactness, `B_X` primitive, vertical quotient/no-pole, scalar no-hair, parent `Xhat` Hessian, parent metric/beta, and finally `qbar_XT/J_X` source-zero. Each route is useful as a theorem target, but none is current evidence. The live next pressure point is now the frame/marker coupling/no-marker theorem or explicit bounded component rows.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2101", "claim_allowed", "valid_for_claim"]),
            "## Sector Owner Gate",
            md_table(owners, ["owner_id", "owner", "required_statement", "current_status", "failure_if_missing", "source_backed", "theorem_zero_signed", "claim_allowed", "valid_for_claim"]),
            "## Route Ladder",
            md_table(ladder, ["ladder_id", "route", "current_result", "retained_fallback", "next_pressure_point", "claim_allowed", "valid_for_claim"]),
            "## FB5540 Source Rows",
            md_table(fb_rows, ["source_row_id", "quantity", "definition", "current_status", "required_evidence", "source_backed", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## qbarXT Coupling Rows",
            md_table(qbar_rows, ["coupling_id", "quantity", "definition", "current_status", "required_evidence", "source_backed", "score_ready", "claim_allowed", "valid_for_claim"]),
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
    owners = owner_gate_rows()
    ladder = route_ladder_rows()
    fb_rows = fb5540_source_rows()
    qbar_rows = qbar_coupling_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2101_SOURCE_REGISTER.csv",
        "owners": OUT / "P8_Y5_PARENT_QLOC_2101_SECTOR_OWNER_GATE.csv",
        "ladder": OUT / "P8_Y5_PARENT_QLOC_2101_ROUTE_LADDER.csv",
        "fb_rows": OUT / "P8_Y5_PARENT_QLOC_2101_FB5540_SOURCE_ROWS.csv",
        "qbar_rows": OUT / "P8_Y5_PARENT_QLOC_2101_QBARXT_COUPLING_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2101_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2101_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2101_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2101_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2101_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["owners"], owners)
    write_csv(paths["ladder"], ladder)
    write_csv(paths["fb_rows"], fb_rows)
    write_csv(paths["qbar_rows"], qbar_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(owners, ladder, fb_rows, qbar_rows, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, owners, ladder, fb_rows, qbar_rows, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, owners, ladder, fb_rows, qbar_rows, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
