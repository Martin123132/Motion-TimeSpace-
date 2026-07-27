from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2747-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt-under-AX1090.md"
LOCAL_BOUND_CLAIMS = LOCAL_BOUNDS / "local_bound_claims.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2747_SOURCE_REGISTER.csv",
    "model": RESIDUALS / "P8_Y5_R2FR_2747_TWO_PARAMETER_MODEL.csv",
    "bound_box": RESIDUALS / "P8_Y5_R2FR_2747_PARAMETER_BOUND_BOX_NONCLAIM.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2747_TWO_PARAMETER_CONTROL_RUNNER_NONCLAIM.csv",
    "zero_hunt": RESIDUALS / "P8_Y5_R2FR_2747_PARENT_ZERO_CONDITION_HUNT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2747_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2747_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2747_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2747_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2747_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "runner": LOCAL_BOUNDS / "qR_delta_beta_control_runner_2747_NONCLAIM.csv",
    "zero_hunt": SOURCE_WEIGHT / "parent_zero_condition_hunt_2747_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2747_PARENT_WEAK_FIELD_ZERO_CONDITION_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GR_LIGHT_BENDING_ARCSEC = 1.7512432813682448
GR_SHAPIRO_MICROSECONDS = 119.4750358485562
GR_MERCURY_ARCSEC_CENTURY = 42.98201260912118


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def local_bound_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(LOCAL_BOUND_CLAIMS)
    return {row["row_id"]: row for row in rows}


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2747_0_2746_doc",
            "description": "2746 selects q_R/delta_beta two-parameter PPN control runner.",
            "source_path": "2746-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection-under-AX1090.md",
            "required_needles": "NEXT2746_0_2747;PPNC2746_0_qR_gamma;VAL2746_OVERALL",
        },
        {
            "source_id": "SRC2747_1_2746_validation",
            "description": "2746 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2746_VALIDATION.csv",
            "required_needles": "VAL2746_OVERALL;True;two-parameter runner next",
        },
        {
            "source_id": "SRC2747_2_2746_ppn",
            "description": "live q_R/delta_beta PPN coefficient translation.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2746_PPN_COEFFICIENT_DERIVATION.csv",
            "required_needles": "PPNC2746_0_qR_gamma;PPNC2746_6_perihelion_degeneracy",
        },
        {
            "source_id": "SRC2747_3_2746_readiness",
            "description": "live coefficient readiness matrix.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2746_COEFFICIENT_READINESS_MATRIX.csv",
            "required_needles": "READY2746_0_qR_gamma;TRANSLATION_ONLY",
        },
        {
            "source_id": "SRC2747_4_2745_budget",
            "description": "live q_R and beta bound budget rows.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2745_BOUND_BUDGET_NONCLAIM.csv",
            "required_needles": "BUD2745_0_qR;BUD2745_1_delta_beta",
        },
        {
            "source_id": "SRC2747_5_local_bounds",
            "description": "local Cassini gamma and beta bound source rows.",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "required_needles": "R3_gamma;R4_beta;Cassini_Shapiro_gamma_2003",
        },
        {
            "source_id": "SRC2747_6_1559_doc",
            "description": "prior two-parameter runner and zero-condition hunt.",
            "source_path": "1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md",
            "required_needles": "ZERO1559_0_qR_linear;GATE1559_2_GR_origin;NEXT_1560_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION",
        },
        {
            "source_id": "SRC2747_7_14_deviation_doc",
            "description": "deviation sensitivity source text.",
            "source_path": "14-closure-deviation-PPN-sensitivity.md",
            "required_needles": "Mercury shift factor = (2 q_R - delta_beta)/3.;Light bending and Shapiro isolate the gamma-like side",
        },
        {
            "source_id": "SRC2747_8_10_observer_contract",
            "description": "observer-map contract and zero-condition warning.",
            "source_path": "10-observer-map-symplectic-contract.md",
            "required_needles": "derive R_AB=0 from the parent theory;beta - 1 = 0",
        },
        {
            "source_id": "SRC2747_9_2746_queue",
            "description": "live queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2746_TWO_PARAMETER_PPN_CONTROL_NEXT.csv",
            "required_needles": "NEXT2746_0_2747;two-parameter local control runner",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def model_rows() -> list[dict[str, Any]]:
    specs = [
        ("MODEL2747_0_gamma", "gamma_minus_1", "q_R", "1", "dimensionless", "linear PPN dictionary"),
        ("MODEL2747_1_beta", "beta_minus_1", "delta_beta", "1", "dimensionless", "definition of nonlinear beta drift"),
        ("MODEL2747_2_light", "solar_light_bending_residual_arcsec", "q_R", f"{GR_LIGHT_BENDING_ARCSEC / 2}", "arcsec", "theta_GR q_R/2"),
        ("MODEL2747_3_shapiro", "solar_Shapiro_residual_microseconds", "q_R", f"{GR_SHAPIRO_MICROSECONDS / 2}", "microseconds", "delay_GR q_R/2"),
        ("MODEL2747_4_mercury_qR", "Mercury_perihelion_residual_arcsec_per_century", "q_R", f"{2 * GR_MERCURY_ARCSEC_CENTURY / 3}", "arcsec/century", "GR_perihelion 2 q_R/3"),
        ("MODEL2747_5_mercury_beta", "Mercury_perihelion_residual_arcsec_per_century", "delta_beta", f"{-GR_MERCURY_ARCSEC_CENTURY / 3}", "arcsec/century", "-GR_perihelion delta_beta/3"),
        ("MODEL2747_6_mercury_combo", "Mercury_perihelion_fractional_factor", "q_R; delta_beta", "(2 q_R - delta_beta)/3", "dimensionless", "perihelion degeneracy line"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "model_id": mid,
                "observable_response": response,
                "leak_parameter": leak,
                "coefficient": coeff,
                "units": units,
                "derivation_note": note,
                "model_status": "PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R2FR_2746_PPN_COEFFICIENT_DERIVATION.csv; 14-closure-deviation-PPN-sensitivity.md",
            }
        )
        for mid, response, leak, coeff, units, note in specs
    ]


def bound_box_rows() -> list[dict[str, Any]]:
    lookup = local_bound_lookup()
    gamma = lookup["R3_gamma"]
    beta = lookup["R4_beta"]
    specs = [
        ("BOX2747_0_qR", "q_R", "R3_gamma", gamma["measured_value"], gamma["one_sigma"], gamma["upper_bound"], "q_R = gamma-1 in the PPN translation map"),
        ("BOX2747_1_delta_beta", "delta_beta", "R4_beta", beta["measured_value"], beta["one_sigma"], beta["upper_bound"], "delta_beta = beta-1 by PPN parameter definition; beta row carries its original gamma-prior caveat"),
        ("BOX2747_2_perihelion_combo", "2 q_R - delta_beta", "R3_gamma; R4_beta", "not_independently_fit_here", "not_independently_fit_here", "derived_combination_only", "perihelion constrains the combination through (2 q_R-delta_beta)/3, but no independent Mercury covariance is reconstructed here"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "bound_id": bid,
                "parameter_or_combo": param,
                "local_bound_rows": rows,
                "measured_or_central": central,
                "one_sigma": sigma,
                "control_bound": bound,
                "interpretation": interpretation,
            }
        )
        for bid, param, rows, central, sigma, bound, interpretation in specs
    ]


def runner_case(q_r: float, delta_beta: float) -> tuple[float, float, float]:
    gamma_minus_1 = q_r
    beta_minus_1 = delta_beta
    mercury = GR_MERCURY_ARCSEC_CENTURY * (2 * q_r - delta_beta) / 3
    return gamma_minus_1, beta_minus_1, mercury


def runner_rows() -> list[dict[str, Any]]:
    lookup = local_bound_lookup()
    q_bound = float(lookup["R3_gamma"]["upper_bound"])
    beta_bound = float(lookup["R4_beta"]["upper_bound"])
    cases = [
        ("CASE2747_0_GR_origin", "GR/null closure origin", 0.0, 0.0, "baseline origin of q_R/delta_beta plane"),
        ("CASE2747_1_Cassini_q_edge", "positive q_R bound edge", q_bound, 0.0, "Cassini gamma-edge control point"),
        ("CASE2747_2_beta_edge", "positive delta_beta bound edge", 0.0, beta_bound, "beta edge control point"),
        ("CASE2747_3_perihelion_degeneracy", "perihelion degeneracy line", 2e-05, 4e-05, "2 q_R - delta_beta = 0 while gamma/beta bounds still matter"),
        ("CASE2747_4_q_fail", "q_R too large", 5e-05, 0.0, "shows Cassini/gamma clamp"),
        ("CASE2747_5_beta_fail", "delta_beta too large", 0.0, 0.00012, "shows beta clamp"),
    ]
    rows: list[dict[str, Any]] = []
    for cid, label, q_r, delta_beta, purpose in cases:
        gamma_minus_1, beta_minus_1, mercury = runner_case(q_r, delta_beta)
        pass_box = abs(q_r) <= q_bound and abs(delta_beta) <= beta_bound
        rows.append(
            nonclaim(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "case_id": cid,
                    "label": label,
                    "q_R_input": f"{q_r:.12g}",
                    "delta_beta_input": f"{delta_beta:.12g}",
                    "gamma_minus_1": f"{gamma_minus_1:.12g}",
                    "beta_minus_1": f"{beta_minus_1:.12g}",
                    "mercury_residual_arcsec_per_century": f"{mercury:.12g}",
                    "control_status": "PASS_CONTROL_BOX" if pass_box else "FAIL_CONTROL_BOX",
                    "purpose": purpose,
                }
            )
        )
    return rows


def zero_hunt_rows() -> list[dict[str, Any]]:
    specs = [
        ("ZERO2747_0_qR_linear", "q_R=0", "parent equations must force R_AB=O(L^2), not R_AB=q_R L", "linear reciprocal strain coefficient vanishes", "MISSING_PARENT_FIELD_EQUATION", "derive first-order observer-sector equation whose regular/local-vacuum solution has T^2 S=1+O(L^2)"),
        ("ZERO2747_1_qR_charge", "q_R=0", "no reciprocal boundary/current charge may source R_AB at O(L)", "Q_R local charge is zero or pure gauge with proper boundary term", "MISSING_ZERO_CHARGE_THEOREM", "supply first-class constraint/no-boundary-charge proof rather than closure axiom"),
        ("ZERO2747_2_qR_matter", "q_R observed by matter", "matter and photons must read the same T,S coframe, otherwise gamma translation is not universal", "universal coframe descent", "MISSING_MATTER_DESCENT", "derive matter action descent through the same observer map"),
        ("ZERO2747_3_beta_second_order", "delta_beta=0", "second-order weak-field completion must match beta=1 in a valid PPN gauge", "nonlinear source self-coupling equals GR control lane", "MISSING_SECOND_ORDER_PARENT_COMPLETION", "derive O(U^2) metric/coframe field equation and coordinate/gauge map"),
        ("ZERO2747_4_beta_conservation", "delta_beta=0", "Bianchi/conservation identity must fix the nonlinear potential terms consistently", "local conservation closes source normalization and beta completion", "MISSING_BIANCHI_SOURCE_IDENTITY", "derive the parent identity linking field equations to matter conservation"),
        ("ZERO2747_5_no_extra_modes", "q_R=0 and delta_beta=0", "extra finite-range/scalar/tracefree modes must decouple or be suppressed locally", "no surviving local hair in the PPN residual vector", "MISSING_MODE_DECOUPLING_THEOREM", "derive decoupling/suppression or keep local branch as bounded closure"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "zero_id": zid,
                "target_zero": target,
                "required_statement": statement,
                "mathematical_content": content,
                "status": status,
                "next_derivation_step": step,
                "source_paths": "10-observer-map-symplectic-contract.md; 13-local-closure-PPN-benchmark.md; source-intake/mts_residuals/P8_Y5_R2FR_2746_PPN_COEFFICIENT_DERIVATION.csv",
            }
        )
        for zid, target, statement, content, status, step in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2747_0_control_runner", "two-parameter PPN control runner", "PASS_NONCLAIM_CONTROL", "control-plane arithmetic works and can reject trial leak vectors"),
        ("GATE2747_1_parent_prediction", "MTS predicts q_R and delta_beta", "BLOCKED_NO_CLAIM", "no parent equations produce q_R/delta_beta values"),
        ("GATE2747_2_GR_origin", "MTS derives local GR origin q_R=0, delta_beta=0", "BLOCKED_NO_CLAIM", "zero-condition ledger remains unsigned"),
        ("GATE2747_3_matter_universal", "local bounds apply to all matter/photons", "BLOCKED_NO_CLAIM", "matter/coframe descent still missing"),
        ("GATE2747_4_empirical_score", "empirical MTS local-bound score", "BLOCKED_NO_CLAIM", "runner can score hypothetical vectors, not the theory"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2747_0_verdict", "two-parameter local control status", "CONTROL_RUNNER_READY_ZERO_THEOREM_MISSING", "q_R/delta_beta local residuals are now test-shaped, but the parent theory has not derived the GR origin"),
        ("DEC2747_1_first_parent_target", "first zero target should be q_R linear", "Q_R_LINEAR_FIRST", "without R_AB=O(L^2), Cassini kills any generic O(L) reciprocal hair"),
        ("DEC2747_2_beta_target", "second zero target is beta completion", "DELTA_BETA_SECOND_ORDER", "beta only becomes meaningful after second-order weak-field/source-normalization closure"),
        ("DEC2747_3_next", "next target", "NEXT_2748_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION", "attack the parent equations needed for q_R=0 and delta_beta=0, or demote local GR to bounded closure"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2747_0_2748",
                "status": "selected_primary",
                "target_doc": "2748-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_weak_field_zero_condition_derivation_or_demotion_under_AX1090_2748.py",
                "mission": "attempt to derive the first-order q_R=0 condition and second-order delta_beta=0 condition from a parent weak-field field-equation/action structure; if this fails, demote the local GR branch to an explicit bounded-closure control lane",
                "acceptance": "derive parent first-order R_AB=O(L^2) and second-order beta=1 conditions, or write exact missing field-equation/action clauses and demotion language",
                "forbidden": "do not use the PPN control runner as a parent derivation; do not claim local GR/Newton reduction; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2747_0_runner", "source_table": rel(OUTPUTS["runner"]), "copy_path": rel(BRANCH_OUTPUTS["runner"]), "purpose": "local-bound two-parameter qR/delta-beta control runner", "exists": BRANCH_OUTPUTS["runner"].exists()}),
        nonclaim({"copy_id": "BR2747_1_zero_hunt", "source_table": rel(OUTPUTS["zero_hunt"]), "copy_path": rel(BRANCH_OUTPUTS["zero_hunt"]), "purpose": "source-weight parent zero-condition hunt", "exists": BRANCH_OUTPUTS["zero_hunt"].exists()}),
        nonclaim({"copy_id": "BR2747_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for parent weak-field zero-condition derivation", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    model: list[dict[str, Any]],
    bound_box: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    zero_hunt: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    model_ok = any(row["model_id"] == "MODEL2747_0_gamma" and row["coefficient"] == "1" for row in model) and any(row["model_id"] == "MODEL2747_6_mercury_combo" for row in model)
    bound_ok = any(row["bound_id"] == "BOX2747_0_qR" and row["control_bound"] == "2.3e-05" for row in bound_box) and any(row["bound_id"] == "BOX2747_1_delta_beta" and row["control_bound"] == "7.8e-05" for row in bound_box)
    gr_ok = any(row["case_id"] == "CASE2747_0_GR_origin" and row["control_status"] == "PASS_CONTROL_BOX" for row in runner)
    q_fail_ok = any(row["case_id"] == "CASE2747_4_q_fail" and row["control_status"] == "FAIL_CONTROL_BOX" for row in runner)
    degeneracy_ok = any(row["case_id"] == "CASE2747_3_perihelion_degeneracy" and abs(float(row["mercury_residual_arcsec_per_century"])) < 1e-18 for row in runner)
    zero_ok = any(row["zero_id"] == "ZERO2747_0_qR_linear" for row in zero_hunt) and any(row["zero_id"] == "ZERO2747_3_beta_second_order" for row in zero_hunt)
    gates_ok = any(row["claim_gate_id"] == "GATE2747_0_control_runner" and row["status"] == "PASS_NONCLAIM_CONTROL" for row in gates) and any(row["claim_gate_id"] == "GATE2747_2_GR_origin" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [model, bound_box, runner, zero_hunt, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2748" in next_target[0]["target_doc"] and "zero-condition" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2747_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_1_model_q_beta", "passed": model_ok, "detail": "q_R and delta_beta unit translation rows present", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_2_bound_box", "passed": bound_ok, "detail": "q_R and delta_beta bound box written", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_3_GR_origin_passes", "passed": gr_ok, "detail": "GR origin passes control box", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_4_q_fail_fails", "passed": q_fail_ok, "detail": "oversized q_R fails Cassini/gamma bound", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_5_degeneracy_line", "passed": degeneracy_ok, "detail": "perihelion degeneracy example has zero Mercury residual", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_6_zero_conditions", "passed": zero_ok, "detail": "parent zero-condition hunt ledger written", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_7_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "local GR derivation remains blocked and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_8_next_target", "passed": next_ok, "detail": "next target is parent weak-field zero-condition derivation or demotion", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_9_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_10_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2747_11_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2747_12_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2747_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2747 builds the q_R/delta_beta two-parameter PPN control runner and selects parent weak-field zero-condition derivation next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2747 - Y5 R2/f(R): q_R/delta_beta Two-Parameter PPN Control Runner And Zero-Condition Hunt Under AX1090

Status: `Y5_R2FR_2747_two_parameter_control_runner_ready_parent_zero_theorem_missing`

## Private Verdict

2747 makes the local residual branch properly test-shaped.

The control plane is now:

`gamma-1 = q_R`

`beta-1 = delta_beta`

`Delta Mercury / Delta Mercury_GR = (2 q_R - delta_beta)/3`.

This runner can reject trial leak vectors. It cannot score MTS as a prediction, because the parent action still has not produced `q_R`, `delta_beta`, or the zero theorem `q_R=delta_beta=0`.

So the next target is exactly the leap that matters: derive first-order `R_AB=O(L^2)` and second-order `beta=1` from a parent weak-field structure, or demote local GR to bounded closure.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Two-Parameter Model

{markdown_table(data["model"], ["model_id", "observable_response", "leak_parameter", "coefficient", "units", "derivation_note", "model_status", "valid_for_claim"])}

## Parameter Bound Box

{markdown_table(data["bound_box"], ["bound_id", "parameter_or_combo", "local_bound_rows", "measured_or_central", "one_sigma", "control_bound", "interpretation", "valid_for_claim"])}

## Control Runner

{markdown_table(data["runner"], ["case_id", "label", "q_R_input", "delta_beta_input", "gamma_minus_1", "beta_minus_1", "mercury_residual_arcsec_per_century", "control_status", "purpose", "valid_for_claim"])}

## Parent Zero-Condition Hunt

{markdown_table(data["zero_hunt"], ["zero_id", "target_zero", "required_statement", "mathematical_content", "status", "next_derivation_step", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the good kind of constraint. We now have a local control runner that can say exactly how much `q_R` and `delta_beta` are allowed, and it exposes the Mercury degeneracy rather than hiding it. But the theory still has to earn the origin: the parent weak-field equations must kill the linear reciprocal hair and fix the second-order beta term. That is the next serious derivation target.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    model = model_rows()
    bound_box = bound_box_rows()
    runner = runner_rows()
    zero_hunt = zero_hunt_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["model"], model)
    write_csv(OUTPUTS["bound_box"], bound_box)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["zero_hunt"], zero_hunt)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["runner"], runner)
    write_csv(BRANCH_OUTPUTS["zero_hunt"], zero_hunt)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, model, bound_box, runner, zero_hunt, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "model": model,
        "bound_box": bound_box,
        "runner": runner,
        "zero_hunt": zero_hunt,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2747 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
