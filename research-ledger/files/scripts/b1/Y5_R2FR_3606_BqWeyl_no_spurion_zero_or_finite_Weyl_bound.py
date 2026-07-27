from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3606"
BRANCH_ID = "MTS_R2FR_Y5_BQWEYL_NO_SPURION_OR_BOUND_3606"
DOC = ROOT / "3606-Y5-R2FR-BqWeyl-no-spurion-zero-or-finite-Weyl-bound.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3605": (RESIDUALS / "P8_Y5_R2FR_3605_NEXT_TARGET.csv", "NEXT3605_0"),
        "status_3605": (RESIDUALS / "P8_Y5_R2FR_3605_STATUS.csv", "VQ_FIRST_CLASS_SOURCE_SILENCE"),
        "bounds_3605": (RESIDUALS / "P8_Y5_R2FR_3605_DQ_VQ_BOUND_ROWS.csv", "VQB3605_3_E_BqWeyl"),
        "first_dangerous": (RESIDUALS / "P8_Y5_NO_SHADOW_2529_FIRST_DANGEROUS_BQWEYL_ROW.csv", "FDQ2529_0_BqWeyl"),
        "linear_zero_audit": (RESIDUALS / "P8_Y5_NO_SHADOW_2530_LINEAR_BQWEYL_ZERO_AUDIT.csv", "LBZ2530_0_metric_trace"),
        "bqweyl_status": (RESIDUALS / "P8_Y5_NO_SHADOW_2530_BQWEYL_BOUND_ROW_STATUS.csv", "BQB2530_1_parent_coefficient"),
        "qap_status": (RESIDUALS / "P8_EM_quotient_action_derives_q_normal_form_status.csv", "STAT3520_2_BqWeyl"),
        "index_lemma": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv", "OLI2304_6_verdict"),
        "parent_signature_gate": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_PARENT_SIGNATURE_GATE.csv", "PTG2304_7_verdict"),
        "first_source_input": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_BQWEYL_FIRST_SOURCE_INPUT.csv", "BQI2304_1_BqWeyl_parent_coefficient"),
        "countermodels": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_CURVATURE_COUNTERMODEL_LEDGER.csv", "CM2304_0_weyl_spurion"),
        "claim_gates_2304": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_CLAIM_GATES.csv", "GATE2304_2_parent_signature"),
        "demotion_2305": (RESIDUALS / "P8_Y5_PARENT_QLOC_2305_LINEAR_BQWEYL_DEMOTION_LEDGER.csv", "DEM2305_0_linear_route_status"),
        "bound_nonclaim_2302": (RESIDUALS / "P8_Y5_PARENT_QLOC_2302_BQWEYL_BOUND_ROW_NONCLAIM.csv", "BQB2302_0_BqWeyl"),
        "dqweyl2_audit": (RESIDUALS / "P8_Y5_NO_SHADOW_2531_DQWEYL2_COEFFICIENT_AUDIT.csv", "DQC2531_1_zero_route"),
        "dqweyl2_zero": (RESIDUALS / "P8_Y5_PARENT_QLOC_2306_DQWEYL2_ZERO_THEOREM_ATTEMPT.csv", "ZERO2306_4_verdict"),
        "dqweyl2_inputs": (RESIDUALS / "P8_Y5_R2FR_2754_DQWEYL2_INPUT_CONTRACT.csv", "IN2754_0_DqWeyl2"),
        "linear_revival": (RESIDUALS / "P8_Y5_R2FR_2754_LINEAR_BQWEYL_REVIVAL_GATE.csv", "LIN2754_2_verdict"),
        "weyl2_projection": (RESIDUALS / "P8_Y5_R2FR_2754_SCHWARZSCHILD_WEYL2_PROJECTION_GATE.csv", "PROJ2754_0_schwarzschild_C2"),
        "ppn_kernel": (RESIDUALS / "P8_Y5_R2FR_2889_COMMON_WEYL_PPN_KERNEL_ROW_NONCLAIM.csv", "PPNK2889_0_common_weyl_gamma"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3606_SOURCE_REGISTER.csv",
        "bqweyl_theorem": RESIDUALS / "P8_Y5_R2FR_3606_BQWEYL_NO_SPURION_THEOREM.csv",
        "bqweyl_bound_rows": RESIDUALS / "P8_Y5_R2FR_3606_BQWEYL_BOUND_ROWS.csv",
        "countermodel_guards": RESIDUALS / "P8_Y5_R2FR_3606_BQWEYL_COUNTERMODEL_GUARDS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3606_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3606_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3606_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_BqWeyl_no_spurion_or_bound_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3606_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "BQW3606_0_target",
            "3606 target",
            "Prove B_qWeyl=0 from QAP plus no-Weyl-spurion/index theorem, or retain finite B_qWeyl rows.",
            "3605 selected B_qWeyl as the first dangerous v_q source-vector component because exterior vacuum does not kill Weyl curvature.",
            "TARGET_IMPORTED",
            "next_3605",
        ),
        (
            "BQW3606_1_metric_trace_index_lemma",
            "metric-only one-Weyl zero",
            "Any scalar linear in C_abcd formed only from metric contractions vanishes because the Weyl tensor is trace-free.",
            "Every candidate contraction reduces to a trace such as g^{ac}g^{bd}C_abcd=0.",
            "EXACT_INDEX_LEMMA",
            "index_lemma",
        ),
        (
            "BQW3606_2_epsilon_index_lemma",
            "epsilon-only one-Weyl zero",
            "epsilon^{abcd}C_abcd also vanishes for a single Weyl tensor; parity-odd curvature scalars begin at quadratic order C*Cdual.",
            "Weyl pair symmetries and the first Bianchi identity kill the fully antisymmetric one-Weyl scalar.",
            "EXACT_INDEX_LEMMA",
            "index_lemma",
        ),
        (
            "BQW3606_3_spurion_necessity",
            "linear Weyl needs a spurion",
            "A nonzero scalar linear in Weyl has form q P^{abcd} C_abcd, where P^{abcd} is a Weyl-type spurion/projector/readout tensor.",
            "So the zero theorem is equivalent to a typed parent grammar with no such P^{abcd} object.",
            "EXACT_CONDITIONAL_THEOREM",
            "index_lemma",
        ),
        (
            "BQW3606_4_QAP_no_spurion_route",
            "QAP plus no-spurion zero route",
            "If QAP removes q_private source dependence and the parent grammar admits q only as scalar/quotient/pure-density with no Weyl spurion, then B_qWeyl=0.",
            "QAP kills q_private dependence; the index theorem kills metric/epsilon-only one-Weyl terms.",
            "CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "qap_status",
        ),
        (
            "BQW3606_5_finite_bound_law",
            "finite BqWeyl bound law",
            "E_BqWeyl[arena] <= tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl|| plus boundary/source tails.",
            "If the no-spurion theorem is unsigned, the coefficient, q operator, Weyl profile, units and arena projection must be sourced.",
            "EXACT_BOUND_LAW_NONCLAIM",
            "bound_nonclaim_2302",
        ),
        (
            "BQW3606_6_quadratic_guard",
            "quadratic Weyl guard",
            "B_qWeyl(linear)=0 does not kill D_qWeyl2 q C_abcd C^abcd or q C*Cdual towers.",
            "The one-Weyl index theorem cannot erase higher-curvature residuals; those require a no-tower theorem or finite row.",
            "SEPARATE_RESIDUAL_GUARD",
            "dqweyl2_zero",
        ),
        (
            "BQW3606_7_current_MTS_verdict",
            "current corpus verdict",
            "The linear index theorem is solid, but parent typed grammar, q representation, no-spurion/projector/readout kernel and higher-curvature tower exclusions are not signed.",
            "So B_qWeyl=0 is not live and finite rows remain unfilled.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "parent_signature_gate",
        ),
        (
            "BQW3606_8_best_next_move",
            "next mathematical pressure point",
            "Either parent-sign the no-spurion grammar or fill the finite B_qWeyl row with B_qWeyl, G_q, C_Weyl profile, units and arena projections.",
            "This is the narrowest route to reducing epsilon_Dq_vq without pretending local vacuum kills Weyl.",
            "NEXT_TARGET_SELECTED",
            "first_source_input",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, statement, derivation, status, source_id in rows
    ]


def bound_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("BQB3606_0_Z_linear", "Z_BqWeyl_linear", "B_qWeyl=0 if QAP plus typed no-Weyl-spurion grammar is parent-signed", "boolean", "FALSE_CONDITIONAL_NOT_PARENT_SIGNED", "parent typed object-language, q scalar/density representation, no P^{abcd}/projector/readout kernel", "index_lemma", "BOUND_REQUIRED_OR_ZERO_SWITCH"),
        ("BQB3606_1_BqWeyl", "B_qWeyl", "linear q-Weyl/tidal curvature mixing coefficient", "parent_normalized", "MISSING_PARENT_COEFFICIENT", "theorem-zero source or parent coefficient with sign, units, normalization and uncertainty", "first_source_input", "BOUND_REQUIRED_FIRST_DANGEROUS"),
        ("BQB3606_2_Gq", "G_q_or_Lq_inverse", "same-domain q Green/operator response", "operator_declared", "MISSING_Q_OPERATOR_NORMALIZATION", "q kinetic/operator normalization, domain, boundary condition and norm convention", "bqweyl_status", "BOUND_REQUIRED"),
        ("BQB3606_3_CWeyl", "C_Weyl_local_profile", "local Weyl/tidal curvature profile entering G_q C_Weyl", "length^-2_or_declared_norm", "MISSING_DOMAIN_PROFILE", "source geometry/interior cutoff/profile convention; no local-vacuum shortcut", "bqweyl_status", "BOUND_REQUIRED"),
        ("BQB3606_4_tau_arena", "tau_BqWeyl_arena", "projection from q-Weyl profile to R10/PPN/clock/orbital/local residuals", "arena_specific", "MISSING_ARENA_PROJECTION", "R10, PPN, clock, orbital and local-GR projection kernels and units", "first_source_input", "BOUND_REQUIRED"),
        ("BQB3606_5_Pspurion", "P_Weyl_spurion", "hidden P^{abcd}C_abcd/projector/readout kernel countermodel amplitude", "spurion_norm", "MISSING_NO_SPURION_SIGNATURE", "parent no-spurion signature or finite spurion amplitude bound", "countermodels", "BOUND_REQUIRED_IF_ZERO_ROUTE_FAILS"),
        ("BQB3606_6_DqWeyl2_guard", "D_qWeyl2", "quadratic Weyl/higher-curvature residual not killed by linear theorem", "length_squared_or_parent_normalized", "RETAIN_NONCLAIM_RESIDUAL", "no-higher-curvature/no-tower theorem or finite D_qWeyl2 coefficient/operator rows", "dqweyl2_inputs", "SEPARATE_GUARD_BOUND_REQUIRED"),
        ("BQB3606_7_ppn_kernel_bridge", "b_R_common_Weyl", "Cassini-style PPN gamma bridge for common Weyl/frame kernel", "dimensionless", "MISSING_b_R_VALUE", "b_R value, x_U profile, beta channel and no-other-channel proof", "ppn_kernel", "ARENA_KERNEL_NONCLAIM"),
        ("BQB3606_8_E_BqWeyl_total", "E_BqWeyl", "tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl|| + boundary/source tails", "q_source_vector_norm", "NOT_SCORE_READY_TOTAL", "all rows above zero/source-backed; no cancellation with C_qT/source/boundary/readout tails", "bounds_3605", "TOTAL_BOUND_BRANCH_ACTIVE"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": p[source_id],
            "score_status": score_status,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, current_value, required_inputs, source_id, score_status in rows
    ]


def countermodel_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("BQG3606_0_weyl_spurion", "q P^{abcd} C_abcd", "legal unless parent object-language forbids Weyl-type spurion/projector/readout tensors", "blocks linear BqWeyl zero", "countermodels"),
        ("BQG3606_1_projector_source_map", "post-variation curvature/readout source map", "legal unless action normal form rejects readout re-entry before source variation", "blocks variational local-GR reduction", "countermodels"),
        ("BQG3606_2_hidden_frame", "hidden conformal/disformal/readout frame", "legal unless matter/source/readout descent and hidden-frame absence are signed", "shifts effect into clocks, matter constants or PPN", "countermodels"),
        ("BQG3606_3_quadratic_weyl", "q C_abcd C^abcd or q C*Cdual", "not removed by one-Weyl index theorem", "requires no-tower theorem or finite D_qWeyl2 row", "countermodels"),
        ("BQG3606_4_hidden_curvature_coefficient", "F(I_hid)R or F(I_hid)C^2", "legal if hidden scalar invariant survives", "feeds curvature coefficients despite linear zero", "countermodels"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "guard_id": guard_id,
            "countermodel": countermodel,
            "why_it_survives": why,
            "failure_if_open": failure,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for guard_id, countermodel, why, failure, source_id in rows
    ]


def promotion_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PROM3606_0_index_lemma", "one-Weyl index lemma", "PASS_EXACT_LEMMA", "metric/epsilon-only scalar linear in Weyl vanishes", "index_lemma"),
        ("PROM3606_1_spurion_theorem", "linear Weyl needs spurion theorem", "PASS_CONDITIONAL_THEOREM", "nonzero B_qWeyl requires P^{abcd}C_abcd or equivalent projector/readout object", "index_lemma"),
        ("PROM3606_2_current_zero_claim", "current B_qWeyl=0 claim", "FAIL_CURRENT_CLAIM", "parent typed grammar/q representation/no-spurion clauses are not signed", "parent_signature_gate"),
        ("PROM3606_3_current_finite_bound", "current finite B_qWeyl bound", "FAIL_CURRENT_CLAIM", "B_qWeyl coefficient, q operator, Weyl profile and arena projections are missing", "first_source_input"),
        ("PROM3606_4_quadratic_guard", "quadratic Weyl guard", "PASS_GUARD", "linear B_qWeyl zero does not remove D_qWeyl2", "dqweyl2_zero"),
        ("PROM3606_5_local_vacuum_guard", "no local-vacuum shortcut", "PASS_GUARD", "Weyl/tidal curvature survives exterior vacuum", "first_dangerous"),
        ("PROM3606_6_no_Newton_GR_claim", "Newton/PPN/local-GR promotion", "FAIL_CURRENT_CLAIM", "E_BqWeyl is not zero or source-backed finite", "status_3605"),
        ("PROM3606_7_bound_pack", "BqWeyl bound pack complete", "PASS_NONCLAIM", "zero switch and finite input rows are source-ready but not score-ready", "bounds_3605"),
        ("PROM3606_8_next_target", "next target selected", "PASS_ROUTE_SELECTED", "parent-sign no-spurion grammar or fill finite BqWeyl row", "first_source_input"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "BQWEYL_INDEX_THEOREM_STRONG_PARENT_SIGNATURE_UNSIGNED",
            "strongest_result": "3606 proves the useful algebra: metric/epsilon-only one-Weyl scalars vanish, so a nonzero linear B_qWeyl needs a Weyl-type spurion/projector/readout tensor. The live corpus does not parent-sign no-spurion grammar, so the zero theorem is conditional and the finite row remains missing.",
            "decision": "retain Z_BqWeyl_linear as a conditional zero switch, keep B_qWeyl/G_q/C_Weyl/tau_arena/spurion/D_qWeyl2 rows nonclaim, and next either parent-sign the no-spurion grammar or fill finite BqWeyl inputs",
            "still_missing": "parent typed object-language, q scalar/density representation, object-language exhaustion, no P^{abcd}/projector/readout kernel, hidden-frame exclusion, B_qWeyl coefficient, q operator normalization, Weyl profile, arena projections and D_qWeyl2 no-tower guard",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["index_lemma"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3606_0",
            "target_doc": "3607-Y5-R2FR-BqWeyl-parent-signature-or-finite-row-acquisition.md",
            "target_script": "scripts/Y5_R2FR_3607_BqWeyl_parent_signature_or_finite_row_acquisition.py",
            "objective": "try to parent-sign the no-Weyl-spurion grammar; if that fails, stage finite B_qWeyl acquisition rows for B_qWeyl, G_q, C_Weyl profile, tau_arena projections, units and D_qWeyl2 guard",
            "success_gate": "E_BqWeyl can only leave epsilon_Dq_vq if Z_BqWeyl_linear is parent-signed or all finite BqWeyl inputs are source-backed and arena-projected",
            "reason": "3606 shows the index theorem is strong but not activated; the live gap is parent signature or finite source-backed inputs",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3606_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3606 source paths exist"))
    validations.append(("VAL3606_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3606 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3606_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3606 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3606_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3606_4_index_lemmas_present", {"BQW3606_1_metric_trace_index_lemma", "BQW3606_2_epsilon_index_lemma", "BQW3606_3_spurion_necessity"}.issubset({str(row["theorem_id"]) for row in theorem}), "index and spurion necessity rows present"))
    validations.append(("VAL3606_5_bound_rows_present", {"Z_BqWeyl_linear", "B_qWeyl", "G_q_or_Lq_inverse", "C_Weyl_local_profile", "tau_BqWeyl_arena", "D_qWeyl2", "E_BqWeyl"}.issubset({str(row["symbol"]) for row in bounds}), "critical BqWeyl bound rows present"))
    validations.append(("VAL3606_6_countermodels_present", {"q P^{abcd} C_abcd", "q C_abcd C^abcd or q C*Cdual"}.issubset({str(row["countermodel"]) for row in guards}), "Weyl spurion and quadratic Weyl guards present"))
    validations.append(("VAL3606_7_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3606_2_current_zero_claim", "PROM3606_3_current_finite_bound", "PROM3606_6_no_Newton_GR_claim"]), "BqWeyl zero/finite/local-GR claims are blocked"))
    validations.append(("VAL3606_8_quadratic_guard", any(row["gate_id"] == "PROM3606_4_quadratic_guard" and row["status"] == "PASS_GUARD" for row in gates), "DqWeyl2 guard present"))
    validations.append(("VAL3606_9_next_target_selected", any(row["next_id"] == "NEXT3606_0" for row in next_target), "3607 BqWeyl parent-signature/finite-row target selected"))
    validations.append(("VAL3606_10_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, bounds, guards, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, bounds, guards, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3606_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3606*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3606-") or path.name.startswith("Y5_R2FR_3606") or "P8_Y5_R2FR_3606" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3606_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3606 checkpoint output appears in formalization-workbench outside package/venv noise"))
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(theorem, bounds, guards, gates, status, next_target, validation) -> None:
    lines = [
        "# 3606 - BqWeyl no-spurion zero or finite Weyl bound",
        "",
        "## Verdict",
        "3606 proves the useful algebraic fact: a metric/epsilon-only scalar linear in one Weyl tensor vanishes.  So a nonzero `B_qWeyl` requires a Weyl-type spurion/projector/readout tensor `P^{abcd}`.",
        "",
        "That is a good theorem route, but not a live claim: current MTS has not parent-signed the typed no-spurion grammar or q representation.  Therefore `B_qWeyl=0` stays conditional and `E_BqWeyl` remains a finite-row problem.",
        "",
        "The finite law is `E_BqWeyl[arena] <= tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl||` plus boundary/source tails.  Quadratic Weyl `D_qWeyl2` is a separate guard, not killed by the linear index theorem.",
        "",
        "## BqWeyl Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## BqWeyl Bound Rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` / `{row['symbol']}`: {row['score_status']} - {row['formula']}")
    lines.extend(["", "## Countermodel Guards"])
    for row in guards:
        lines.append(f"- `{row['guard_id']}` / `{row['countermodel']}`: {row['failure_if_open']} - {row['why_it_survives']}")
    lines.extend(["", "## Promotion Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_map = sources()
    out_paths = outputs()
    register = source_register_rows(source_map)
    theorem = theorem_rows(source_map)
    bounds = bound_rows(source_map)
    guards = countermodel_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["bqweyl_theorem"], theorem)
    write_csv(out_paths["bqweyl_bound_rows"], bounds)
    write_csv(out_paths["countermodel_guards"], guards)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, theorem, bounds, guards, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, bounds, guards, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
