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

DOC = ROOT / "2746-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2746_SOURCE_REGISTER.csv",
    "ppn_derivation": RESIDUALS / "P8_Y5_R2FR_2746_PPN_COEFFICIENT_DERIVATION.csv",
    "phenomenology": RESIDUALS / "P8_Y5_R2FR_2746_PHENOMENOLOGICAL_COEFFICIENT_MAP.csv",
    "rejections": RESIDUALS / "P8_Y5_R2FR_2746_COEFFICIENT_REJECTION_LEDGER.csv",
    "readiness": RESIDUALS / "P8_Y5_R2FR_2746_COEFFICIENT_READINESS_MATRIX.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2746_RUNNER_NONCLAIM.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2746_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2746_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2746_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2746_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2746_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ppn": LOCAL_BOUNDS / "qR_delta_beta_ppn_translation_2746_NONCLAIM.csv",
    "readiness": SOURCE_WEIGHT / "coefficient_readiness_matrix_2746_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2746_TWO_PARAMETER_PPN_CONTROL_NEXT.csv",
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


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2746_0_2745_doc",
            "description": "2745 selects response-coefficient source map.",
            "source_path": "2745-Y5-R2FR-closure-deviation-PPN-sensitivity-and-bound-budget-under-AX1090.md",
            "required_needles": "NEXT2745_0_2746;COEF2745_0_C_gamma_qR;VAL2745_OVERALL",
        },
        {
            "source_id": "SRC2746_1_2745_validation",
            "description": "2745 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2745_VALIDATION.csv",
            "required_needles": "VAL2745_OVERALL;True;response-coefficient sourcing next",
        },
        {
            "source_id": "SRC2746_2_2745_budget",
            "description": "live closure-deviation bound budget.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2745_BOUND_BUDGET_NONCLAIM.csv",
            "required_needles": "BUD2745_0_qR;MISSING_C_gamma_qR;CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION",
        },
        {
            "source_id": "SRC2746_3_2745_sensitivity",
            "description": "live sensitivity map.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2745_SENSITIVITY_MAP_NONCLAIM.csv",
            "required_needles": "SENS2745_0_qR_light_bending;SENS2745_3_delta_beta_mercury",
        },
        {
            "source_id": "SRC2746_4_2745_coefficient_queue",
            "description": "live response coefficient queue.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2745_RESPONSE_COEFFICIENT_SOURCE_QUEUE.csv",
            "required_needles": "COEF2745_0_C_gamma_qR;COEF2745_8_M_TF;MISSING_PARENT_RESPONSE_COEFFICIENT",
        },
        {
            "source_id": "SRC2746_5_1558_doc",
            "description": "prior coefficient source-map/rejection checkpoint.",
            "source_path": "1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md",
            "required_needles": "PPNC1558_0_qR_gamma;READY1558_0_qR_gamma;NEXT_1559_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT",
        },
        {
            "source_id": "SRC2746_6_14_deviation_doc",
            "description": "internal deviation sensitivity source text.",
            "source_path": "14-closure-deviation-PPN-sensitivity.md",
            "required_needles": "Mercury shift factor = (2 q_R - delta_beta)/3.;solar light bending vs q_R",
        },
        {
            "source_id": "SRC2746_7_13_closure_doc",
            "description": "local closure benchmark warning for q_R/gamma.",
            "source_path": "13-local-closure-PPN-benchmark.md",
            "required_needles": "R_AB approx q_R L;gamma approx 1 + q_R.",
        },
        {
            "source_id": "SRC2746_8_2745_queue",
            "description": "live queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2745_RESPONSE_COEFFICIENT_SOURCE_MAP_NEXT.csv",
            "required_needles": "NEXT2745_0_2746;response coefficients",
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


def ppn_derivation_rows() -> list[dict[str, Any]]:
    light_coeff = GR_LIGHT_BENDING_ARCSEC / 2
    shapiro_coeff = GR_SHAPIRO_MICROSECONDS / 2
    mercury_qr = 2 * GR_MERCURY_ARCSEC_CENTURY / 3
    mercury_beta = -GR_MERCURY_ARCSEC_CENTURY / 3
    specs = [
        ("PPNC2746_0_qR_gamma", "q_R", "gamma_minus_1", "1", "dimensionless per unit q_R", "DERIVED_PPN_DICTIONARY_NOT_PARENT_PREDICTION", "R_AB ~= (gamma-1)L and R_AB ~= q_R L imply gamma-1=q_R"),
        ("PPNC2746_1_qR_light_bending", "q_R", "solar_light_bending_residual", f"{light_coeff}", "arcsec per unit q_R", "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION", "light-bending gamma residual is half the GR limb-bending scale per unit gamma-1"),
        ("PPNC2746_2_qR_shapiro", "q_R", "solar_Shapiro_residual", f"{shapiro_coeff}", "microseconds per unit q_R", "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION", "Shapiro gamma residual is half the GR Shapiro scale per unit gamma-1"),
        ("PPNC2746_3_qR_mercury", "q_R", "Mercury_perihelion_residual", f"{mercury_qr}", "arcsec/century per unit q_R", "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION", "perihelion factor contains 2 q_R / 3"),
        ("PPNC2746_4_delta_beta_definition", "delta_beta", "beta_minus_1", "1", "dimensionless per unit delta_beta", "PPN_PARAMETER_DEFINITION_NOT_PARENT_COMPLETION", "delta_beta is defined as beta-1 for the control runner"),
        ("PPNC2746_5_delta_beta_mercury", "delta_beta", "Mercury_perihelion_residual", f"{mercury_beta}", "arcsec/century per unit delta_beta", "DERIVED_FROM_STANDARD_PPN_SCALING_NOT_PARENT_PREDICTION", "perihelion factor contains -delta_beta / 3"),
        ("PPNC2746_6_perihelion_degeneracy", "q_R; delta_beta", "Mercury_perihelion_residual", "(2 q_R - delta_beta)/3 times GR perihelion", "dimensionless factor", "DERIVED_PPN_DEGENERACY_STRUCTURE_NOT_PARENT_PREDICTION", "Mercury alone does not isolate q_R from beta drift"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "coefficient_id": cid,
                "leak_parameter": leak,
                "observable_response": response,
                "coefficient_value": value,
                "coefficient_units": units,
                "coefficient_status": status,
                "derivation_note": note,
            }
        )
        for cid, leak, response, value, units, status, note in specs
    ]


def phenomenology_rows() -> list[dict[str, Any]]:
    specs = [
        ("PHEN2746_0_alpha_clock_redshift", "alpha_clock", "alpha_clock_redshift", "1", "PHENOMENOLOGICAL_PARAMETER_DEFINITION_ONLY", "alpha_clock can be used as observed redshift-deviation parameter, but MTS clock/load map is not parent-derived"),
        ("PHEN2746_1_epsilon_matter_eta", "epsilon_matter", "eta_WEP_proxy", "1", "PHENOMENOLOGICAL_PROXY_ONLY", "epsilon_matter measures matter-coupling spread, but universal matter-action descent is not derived"),
        ("PHEN2746_2_sigma_Gdot", "sigma_Gdot", "Gdot_over_G", "MISSING", "REJECTED_FOR_NOW_MISSING_PARENT_SOURCE_NORMALIZATION", "requires measured-GM/source-normalization theorem before Gdot bound can be applied to MTS"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "phenomenology_id": pid,
                "leak_parameter": leak,
                "observable_response": response,
                "coefficient_value": value,
                "coefficient_status": status,
                "limitation": limitation,
            }
        )
        for pid, leak, response, value, status, limitation in specs
    ]


def rejection_rows() -> list[dict[str, Any]]:
    specs = [
        ("REJ2746_0_source_normalization", "sigma_Gdot", "Gdot_over_G", "MISSING_C_Gdot", "no parent measured-GM/source-normalization theorem; cannot decide whether source drift maps to measured Gdot", "derive source-normalization theorem or leave as external bound only"),
        ("REJ2746_1_preferred_frame_alpha1", "epsilon_frame_1", "alpha1", "MISSING_C_alpha1", "no frame/coframe descent coefficient from parent observer split", "derive frame-descent response or keep alpha1 as no-claim diagnostic"),
        ("REJ2746_2_preferred_frame_alpha2", "epsilon_frame_2", "alpha2", "MISSING_C_alpha2", "spin/anisotropic coframe leakage lacks a response map", "derive spin/coframe response or keep alpha2 as no-claim diagnostic"),
        ("REJ2746_3_flux_alpha3_xi", "epsilon_flux", "alpha3; xi", "MISSING_C_alpha3_AND_C_xi", "boundary silence and momentum/source-flux conservation are not parent-derived", "derive boundary/no-charge theorem before using ultra-tight alpha3/xi bounds"),
        ("REJ2746_4_R10_range_curve", "alpha_R10(lambda)", "Yukawa alpha(lambda)", "MISSING_C_R10_lambda_AND_DIGITIZED_CURVE", "R10 bound remains symbolic curve-only and parent range map is absent", "acquire real alpha(lambda) curve and derive lambda/residual-hair map"),
        ("REJ2746_5_tracefree_transfer", "h_TF_residual", "PPN residual vector", "MISSING_M_TF_RESPONSE_MATRIX", "scalar R_AB closure does not define tensor/vector transfer", "derive tensor/coframe response matrix before vector/tensor PPN scoring"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "rejection_id": rid,
                "leak_parameter": leak,
                "observable_response": response,
                "missing_input": missing,
                "reason": reason,
                "reentry_condition": reentry,
                "status": "REJECTED_FOR_SCORING_AT_2746",
            }
        )
        for rid, leak, response, missing, reason, reentry in specs
    ]


def readiness_rows() -> list[dict[str, Any]]:
    specs = [
        ("READY2746_0_qR_gamma", "q_R", "gamma_minus_1/light/Shapiro/perihelion", True, False, False, "PPN translation is derived; parent still must predict q_R", "TRANSLATION_ONLY"),
        ("READY2746_1_delta_beta", "delta_beta", "beta_minus_1/perihelion", True, False, False, "PPN translation is derived; parent still must supply beta completion", "TRANSLATION_ONLY"),
        ("READY2746_2_alpha_clock", "alpha_clock", "redshift/clocks", True, False, False, "phenomenological clock parameter usable; parent clock/load response missing", "TRANSLATION_ONLY"),
        ("READY2746_3_epsilon_matter", "epsilon_matter", "WEP/Eotvos", True, False, False, "proxy parameter usable; parent matter descent missing", "TRANSLATION_ONLY"),
        ("READY2746_4_sigma_Gdot", "sigma_Gdot", "Gdot/G", False, False, False, "source-normalization coefficient missing", "REJECTED_PENDING_INPUTS"),
        ("READY2746_5_frame", "epsilon_frame_1; epsilon_frame_2", "alpha1/alpha2", False, False, False, "frame/coframe descent coefficients missing", "REJECTED_PENDING_INPUTS"),
        ("READY2746_6_flux", "epsilon_flux", "alpha3/xi", False, False, False, "boundary/source-flux coefficients missing", "REJECTED_PENDING_INPUTS"),
        ("READY2746_7_R10", "alpha_R10(lambda)", "Yukawa alpha(lambda)", False, False, False, "digitized curve and parent range map missing", "REJECTED_PENDING_INPUTS"),
        ("READY2746_8_tracefree", "h_TF_residual", "PPN residual vector", False, False, False, "tensor response matrix missing", "REJECTED_PENDING_INPUTS"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "readiness_id": rid,
                "leak_parameter": leak,
                "observable_response": response,
                "translation_ready": trans,
                "parent_prediction_ready": parent_ready,
                "score_ready_status": score_ready,
                "reason": reason,
                "status": status,
            }
        )
        for rid, leak, response, trans, parent_ready, score_ready, reason, status in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2746_0_sources", "2745 handoff and coefficient sources exist", "PASS", "all coefficient source files exist and evidence needles are present"),
        ("RUN2746_1_qR_beta_ppn", "derive q_R and delta_beta PPN translation coefficients", "PASS_TRANSLATION_ONLY", "q_R maps to gamma-1; light/Shapiro/perihelion and beta perihelion coefficients are derived from standard PPN scaling"),
        ("RUN2746_2_clock_matter", "classify clock and matter coefficients", "PASS_PHENOMENOLOGICAL_ONLY", "clock and WEP parameters can be used as proxy observables but not parent-derived MTS predictions"),
        ("RUN2746_3_rejections", "reject unsupported coefficients", "PASS_REJECTION_LEDGER", "Gdot, preferred-frame, flux, R10, and tracefree coefficients remain blocked"),
        ("RUN2746_4_scoring", "local-bound scoring", "REFUSED_NO_PARENT_PREDICTIONS", "translation coefficients do not produce a claim until the parent action predicts q_R, delta_beta, clock/matter drift, or their zeros"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "runner_id": rid, "test": test, "current_status": status, "detail": detail}) for rid, test, status, detail in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2746_0_qR_translation", "q_R PPN translation", "OPEN_TRANSLATION_ONLY", "coefficient map exists, but parent q_R prediction is missing"),
        ("GATE2746_1_beta_translation", "delta_beta PPN translation", "OPEN_TRANSLATION_ONLY", "coefficient map exists, but parent beta completion is missing"),
        ("GATE2746_2_clock", "clock coefficient", "BLOCKED_NO_CLAIM", "phenomenological redshift parameter only"),
        ("GATE2746_3_matter", "matter/WEP coefficient", "BLOCKED_NO_CLAIM", "phenomenological WEP proxy only"),
        ("GATE2746_4_Gdot", "source normalization", "BLOCKED_NO_CLAIM", "source-normalization theorem missing"),
        ("GATE2746_5_frame_flux_tracefree_R10", "remaining local residual vector", "BLOCKED_NO_CLAIM", "response matrix/range/boundary coefficients missing"),
        ("GATE2746_6_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "translation map is not a parent derivation of R_AB=0, Q_R=0, or beta=1"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2746_0_verdict", "coefficient source-map status", "Q_R_AND_DELTA_BETA_TRANSLATION_DERIVED_PARENT_PREDICTIONS_MISSING", "the q_R/beta PPN observable map is now mathematically sharp, but MTS still needs parent equations that set or predict the leak parameters"),
        ("DEC2746_1_first_runner", "two-parameter q_R/delta_beta runner is now justified", "NEXT_TWO_PARAMETER_CONTROL", "translation is ready even though parent predictions are not"),
        ("DEC2746_2_zero_hunt", "zero-condition hunt must run beside the control runner", "PARENT_ZERO_CONDITIONS_REQUIRED", "a fit to q_R=0/delta_beta=0 is not a derivation; parent theorem still needed"),
        ("DEC2746_3_next", "next target", "NEXT_2747_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT", "use derived translations to build a nonclaim runner and isolate the exact zero conditions"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2746_0_2747",
                "status": "selected_primary",
                "target_doc": "2747-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_qR_delta_beta_two_parameter_PPN_control_runner_and_zero_condition_hunt_under_AX1090_2747.py",
                "mission": "use the derived q_R and delta_beta PPN translation coefficients to build a nonclaim two-parameter local control runner, then identify the exact parent zero conditions needed to promote q_R=0 and delta_beta=0 from closure to derivation",
                "acceptance": "produce a q_R/delta_beta control runner with local bounds and a separate parent-zero-condition ledger; no MTS scoring without parent-predicted leak parameters",
                "forbidden": "do not score MTS predictions without parent-predicted leak parameters; do not claim local GR derivation; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2746_0_ppn", "source_table": rel(OUTPUTS["ppn_derivation"]), "copy_path": rel(BRANCH_OUTPUTS["ppn"]), "purpose": "local-bound qR/delta-beta PPN translation", "exists": BRANCH_OUTPUTS["ppn"].exists()}),
        nonclaim({"copy_id": "BR2746_1_readiness", "source_table": rel(OUTPUTS["readiness"]), "copy_path": rel(BRANCH_OUTPUTS["readiness"]), "purpose": "source-weight coefficient readiness matrix", "exists": BRANCH_OUTPUTS["readiness"].exists()}),
        nonclaim({"copy_id": "BR2746_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for two-parameter PPN control runner", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
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
    ppn: list[dict[str, Any]],
    phenomenology: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    qgamma_ok = any(row["coefficient_id"] == "PPNC2746_0_qR_gamma" and row["coefficient_value"] == "1" for row in ppn)
    light_ok = any(row["coefficient_id"] == "PPNC2746_1_qR_light_bending" and abs(float(row["coefficient_value"]) - GR_LIGHT_BENDING_ARCSEC / 2) < 1e-12 for row in ppn)
    shapiro_ok = any(row["coefficient_id"] == "PPNC2746_2_qR_shapiro" and abs(float(row["coefficient_value"]) - GR_SHAPIRO_MICROSECONDS / 2) < 1e-12 for row in ppn)
    peri_ok = any(row["coefficient_id"] == "PPNC2746_3_qR_mercury" and abs(float(row["coefficient_value"]) - 2 * GR_MERCURY_ARCSEC_CENTURY / 3) < 1e-12 for row in ppn) and any(row["coefficient_id"] == "PPNC2746_5_delta_beta_mercury" and abs(float(row["coefficient_value"]) + GR_MERCURY_ARCSEC_CENTURY / 3) < 1e-12 for row in ppn)
    phen_ok = any(row["phenomenology_id"] == "PHEN2746_0_alpha_clock_redshift" for row in phenomenology) and any(row["phenomenology_id"] == "PHEN2746_1_epsilon_matter_eta" for row in phenomenology)
    rejection_ok = len(rejections) == 6 and all(row["status"] == "REJECTED_FOR_SCORING_AT_2746" for row in rejections)
    readiness_ok = any(row["readiness_id"] == "READY2746_0_qR_gamma" and row["translation_ready"] is True and row["parent_prediction_ready"] is False for row in readiness) and all(row["score_ready_status"] is False for row in readiness)
    runner_ok = any(row["runner_id"] == "RUN2746_4_scoring" and "REFUSED" in row["current_status"] for row in runner)
    gate_ok = any(row["claim_gate_id"] == "GATE2746_0_qR_translation" and row["status"] == "OPEN_TRANSLATION_ONLY" for row in gates) and any(row["claim_gate_id"] == "GATE2746_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [ppn, phenomenology, rejections, readiness, runner, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2747" in next_target[0]["target_doc"] and "two-parameter" in next_target[0]["target_doc"]
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
        {"validation_id": "VAL2746_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_1_qR_gamma", "passed": qgamma_ok, "detail": "q_R to gamma-minus-one coefficient derived as translation", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_2_light_coefficient", "passed": light_ok, "detail": "light-bending q_R coefficient equals GR/2", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_3_shapiro_coefficient", "passed": shapiro_ok, "detail": "Shapiro q_R coefficient equals GR/2", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_4_perihelion_coefficients", "passed": peri_ok, "detail": "perihelion coefficients match (2 q_R - delta_beta)/3", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_5_clock_matter_nonparent", "passed": phen_ok, "detail": "clock/matter rows remain phenomenological and non-parent predictions", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_6_rejection_ledger", "passed": rejection_ok, "detail": "unsupported coefficients rejected for scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_7_readiness_translation_only", "passed": readiness_ok, "detail": "q_R row is translation-ready but not score-ready", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_8_runner_refuses_scoring", "passed": runner_ok, "detail": "runner refuses local-bound scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_9_claim_gates", "passed": gate_ok and no_claim_flags_ok, "detail": "translation gates open but local GR claim remains blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_10_next_target", "passed": next_ok, "detail": "next target is q_R/delta_beta two-parameter PPN control runner", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_11_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_12_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2746_13_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2746_14_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2746_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2746 derives q_R/delta_beta PPN translation coefficients, rejects unsupported response coefficients, and selects a nonclaim two-parameter runner next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2746 - Y5 R2/f(R): q_R/Beta/Matter/Clock Coefficient Source Map Or Rejection Under AX1090

Status: `Y5_R2FR_2746_qR_delta_beta_translation_ready_parent_prediction_missing`

## Private Verdict

2746 gets one proper win, with the guardrails still on.

`q_R` now has a derived PPN translation: at first weak-field order,

`R_AB ~= (gamma-1)L` and `R_AB ~= q_R L`, so `gamma-1=q_R`.

That makes the light-bending, Shapiro, and Mercury `q_R` coefficients usable in a local control runner. `delta_beta` also has a clean PPN definition, and Mercury carries the degeneracy `(2 q_R - delta_beta)/3`.

This is not a parent prediction. MTS still has to prove or predict `q_R=0`, `delta_beta=0`, or a nonzero leakage law from the parent equations. Clock and WEP coefficients remain phenomenological proxies; Gdot, preferred-frame, R10, and tracefree response coefficients are still rejected for scoring.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## PPN Coefficient Derivation

{markdown_table(data["ppn_derivation"], ["coefficient_id", "leak_parameter", "observable_response", "coefficient_value", "coefficient_units", "coefficient_status", "derivation_note", "valid_for_claim"])}

## Phenomenological Coefficient Map

{markdown_table(data["phenomenology"], ["phenomenology_id", "leak_parameter", "observable_response", "coefficient_value", "coefficient_status", "limitation", "valid_for_claim"])}

## Rejection Ledger

{markdown_table(data["rejections"], ["rejection_id", "leak_parameter", "observable_response", "missing_input", "reason", "reentry_condition", "status", "valid_for_claim"])}

## Readiness Matrix

{markdown_table(data["readiness"], ["readiness_id", "leak_parameter", "observable_response", "translation_ready", "parent_prediction_ready", "score_ready_status", "reason", "status", "valid_for_claim"])}

## Runner

{markdown_table(data["runner"], ["runner_id", "test", "current_status", "detail", "valid_for_claim"])}

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

This is a better position than pure closure. We still do not have derived local GR, but we now have a sharp local residual language: `q_R` is the gamma-like leak, and `delta_beta` is the nonlinear/orbital leak. Next we can build the two-parameter runner and hunt the actual parent zero conditions instead of waving at them.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    ppn_derivation = ppn_derivation_rows()
    phenomenology = phenomenology_rows()
    rejections = rejection_rows()
    readiness = readiness_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["ppn_derivation"], ppn_derivation)
    write_csv(OUTPUTS["phenomenology"], phenomenology)
    write_csv(OUTPUTS["rejections"], rejections)
    write_csv(OUTPUTS["readiness"], readiness)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["ppn"], ppn_derivation)
    write_csv(BRANCH_OUTPUTS["readiness"], readiness)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, ppn_derivation, phenomenology, rejections, readiness, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "ppn_derivation": ppn_derivation,
        "phenomenology": phenomenology,
        "rejections": rejections,
        "readiness": readiness,
        "runner": runner,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2746 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
