from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3284-Y5-R2FR-CR-readout-product-law-and-Poynting-wave-standard-or-zero-theorem-under-AX1090.md"

SRC_3283_DOC = ROOT / "3283-Y5-R2FR-first-numeric-CZ-input-source-pack-or-CR-readout-demotion-under-AX1090.md"
SRC_3283_CR_FORMULA = OUT / "P8_Y5_R2FR_3283_CR_READOUT_FORMULA_HANDOFF.csv"
SRC_3283_NEXT = OUT / "P8_Y5_R2FR_3283_NEXT_TARGET.csv"
SRC_3283_VALIDATION = OUT / "P8_Y5_BRR545_3283_VALIDATION.csv"
SRC_3280_ROWS = OUT / "P8_Y5_R2FR_3280_CZ_CR_SOURCE_BOUND_ROWS_NONCLAIM.csv"
SRC_3273_DECOMP = OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv"
SRC_2630_DECISION = OUT / "P8_Y5_CR_ZERO_ROLLFORWARD_2630_DECISION_LEDGER.csv"
SRC_2656_CONTRACT = OUT / "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_RESIDUAL_BOUND_INPUT_CONTRACT.csv"
SRC_3105_DOC = ROOT / "3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md"
SRC_3106_DOC = ROOT / "3106-Y5-R2FR-constitutive-Hodge-star-derivation-or-EM-medium-residual-under-AX1090.md"
SRC_1056_DOC = ROOT / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
SRC_1324_DOC = ROOT / "1324-Y5-R10-RAB-clock-direct-product-derivation-source-fill-or-waitstate.md"
SRC_2764_DOC = ROOT / "2764-Y5-R2FR-EM-vertical-generator-norm-or-MICROSCOPE-extraction-preflight-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3284_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3284_CR_PRODUCT_LAW_THEOREM.csv",
    "factors": OUT / "P8_Y5_R2FR_3284_CR_READOUT_FACTOR_LEDGER.csv",
    "poynting": OUT / "P8_Y5_R2FR_3284_POYNTING_STANDARD_BRANCH_TABLE.csv",
    "prediction": OUT / "P8_Y5_R2FR_3284_FIRST_CR_SLOPE_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3284_CR_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3284_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3284_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3284_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3284_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 360) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 240)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3283_DOC, "3283 branch cut", ["C_R", "Poynting"]),
        (SRC_3283_CR_FORMULA, "3283 C_R formula handoff", ["CRF3283_1", "Poynting"]),
        (SRC_3283_NEXT, "3283 next target", ["3284", "Poynting"]),
        (SRC_3283_VALIDATION, "3283 validation", ["VAL3283_11_overall", "true"]),
        (SRC_3280_ROWS, "3280 C_Z/C_R alpha row", ["ZRB3280_3", "L_X ln R_alpha"]),
        (SRC_3273_DECOMP, "3273 alpha coefficient law", ["2 C_J", "C_R"]),
        (SRC_2630_DECISION, "C_R zero rollforward", ["CR_ZERO_NOT_DERIVED", "RAB_REMAINS"]),
        (SRC_2656_CONTRACT, "readout/source empirical contract", ["tau_WEP", "MISSING_PARENT_COUPLING_OWNER"]),
        (SRC_3105_DOC, "Poynting public-geometry route", ["Double-Counting Guard", "Poynting"]),
        (SRC_3106_DOC, "constitutive Hodge route", ["H = Z_Q", "EM-Medium Residual"]),
        (SRC_1056_DOC, "alpha owner/readout route", ["observed alpha readout", "Hodge"]),
        (SRC_1100_DOC, "T_Q/readout radiative guard", ["readout_radiative_guard", "alpha readout"]),
        (SRC_1324_DOC, "clock direct product wait-state", ["direct product", "clock"]),
        (SRC_2764_DOC, "EM current/readout owner", ["current_readout_owner", "MICROSCOPE"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3284_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def alpha_bound() -> float:
    for row in read_csv(SRC_3280_ROWS):
        if row.get("row_id") == "ZRB3280_3_readout_CR_missing":
            return float(row["bound_value"])
    return 1.389797711495e-12


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CRPL3284_0_definition",
            "claim_piece": "define C_R as the vertical readout multiplier",
            "statement": "Let alpha_obs = alpha_field * R_alpha_readout^{-1}; define C_R := L_v ln R_alpha_readout. Then the alpha residual law is C_e = 2 C_J - C_Z - C_R.",
            "proof_status": "DEFINITION_PLUS_3273_DECOMPOSITION",
            "missing_for_claim": "C_J and C_Z zero/fixed routes are separate; R_alpha_readout must be parent-owned or finite-sourced.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CRPL3284_1_product_law",
            "claim_piece": "exact readout product law",
            "statement": "If R_alpha_readout = product_s R_s^{n_s}, then C_R = sum_s n_s L_v ln R_s.",
            "proof_status": "EXACT_LOG_DERIVATIVE_THEOREM",
            "missing_for_claim": "the actual standard factors and exponents must be parent-declared before scoring.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CRPL3284_2_qbasic_zero_theorem",
            "claim_piece": "readout-zero route",
            "statement": "If every readout factor R_s is q-basic, R_s=q^*Rbar_s, and v in ker(Dq), then C_R=0.",
            "proof_status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "missing_for_claim": "q-basic status for clocks/rods/action units, charge standards, Hodge/impedance, Poynting flux, and material detectors is unsigned.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CRPL3284_3_shift_zero_theorem",
            "claim_piece": "shift-protected readout route",
            "statement": "If an exact vertical shift/Ward identity gives L_v ln R_s=0 for every readout standard factor and is preserved by effective/readout reduction, then C_R=0.",
            "proof_status": "EXACT_CONDITIONAL_WARD_THEOREM",
            "missing_for_claim": "the action/effective/readout Ward identity is not parent-signed.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CRPL3284_4_poynting_no_double_count",
            "claim_piece": "Poynting placement rule",
            "statement": "Poynting energy flux is either the spatial flux of public T_EM or a separate named E_res flux, never both.",
            "proof_status": "ACCOUNTING_IDENTITY_AND_GUARD",
            "missing_for_claim": "parent must decide public Maxwell/Hodge branch versus independent background flux branch.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CRPL3284_5_current_verdict",
            "claim_piece": "C_R current status",
            "statement": "The exact product law and Poynting placement are derived, but C_R=0 and finite C_R are not claimable from current corpus.",
            "proof_status": "NOT_PROMOTED_CURRENT_CORPUS",
            "missing_for_claim": "parent-owned readout functor or numeric source-backed factor slopes.",
            "valid_for_claim": "false",
        },
    ]


def factor_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor_id": "CRFCT3284_0_phase_action_clock",
            "readout_factor": "R_phase_action_clock",
            "slope_symbol": "C_phase := L_v ln R_phase_action_clock",
            "role": "clock/action/frequency unit used to make alpha dimensionless",
            "if_qbasic": "C_phase=0",
            "current_status": "CLOCK_DIRECT_PRODUCT_WAITSTATE",
            "source_path": str(SRC_1324_DOC),
            "valid_for_claim": "false",
        },
        {
            "factor_id": "CRFCT3284_1_lightcone_rods",
            "readout_factor": "R_light_rods",
            "slope_symbol": "C_light := L_v ln R_light_rods",
            "role": "speed-of-light/rod/time conversion from public coframe",
            "if_qbasic": "C_light=0",
            "current_status": "SAME_PUBLIC_METRIC_UNSIGNED",
            "source_path": str(SRC_3106_DOC),
            "valid_for_claim": "false",
        },
        {
            "factor_id": "CRFCT3284_2_hodge_impedance",
            "readout_factor": "R_Hodge_impedance",
            "slope_symbol": "C_H := L_v ln R_Hodge_impedance",
            "role": "Hodge star/impedance standard converting field amplitudes to energy and spectra",
            "if_qbasic": "C_H=0",
            "current_status": "CONSTITUTIVE_HODGE_ROUTE_OPEN",
            "source_path": str(SRC_3106_DOC),
            "valid_for_claim": "false",
        },
        {
            "factor_id": "CRFCT3284_3_poynting_flux_standard",
            "readout_factor": "R_Poynting_flux",
            "slope_symbol": "C_S := L_v ln R_Poynting_flux",
            "role": "EM energy-flux/radiation-pressure calibration from T_EM^{0i}",
            "if_qbasic": "C_S=0 and flux belongs to public T_EM",
            "current_status": "PLACEMENT_RULE_DERIVED_OWNER_UNSIGNED",
            "source_path": str(SRC_3105_DOC),
            "valid_for_claim": "false",
        },
        {
            "factor_id": "CRFCT3284_4_material_detector",
            "readout_factor": "R_material_detector",
            "slope_symbol": "C_mat := L_v ln R_material_detector",
            "role": "detector/material/spectroscopy response to alpha or EM stress",
            "if_qbasic": "C_mat=0",
            "current_status": "MATERIAL_TENSOR_MISSING",
            "source_path": str(SRC_2656_CONTRACT),
            "valid_for_claim": "false",
        },
        {
            "factor_id": "CRFCT3284_5_charge_calibration_guard",
            "readout_factor": "R_charge_standard",
            "slope_symbol": "C_Qread := L_v ln R_charge_standard",
            "role": "charge/current calibration if it is not already the C_J owner",
            "if_qbasic": "C_Qread=0 or route to C_J",
            "current_status": "DO_NOT_DOUBLE_COUNT_WITH_CJ",
            "source_path": str(SRC_1100_DOC),
            "valid_for_claim": "false",
        },
        {
            "factor_id": "CRFCT3284_6_instrument_projection",
            "readout_factor": "R_projection_kernel",
            "slope_symbol": "C_inst := L_v ln R_projection_kernel",
            "role": "experiment/orbit/sampling/kernel conversion from physical residual to observable",
            "if_qbasic": "C_inst=0",
            "current_status": "KERNEL_AND_TAU_NOT_SCORE_READY",
            "source_path": str(SRC_2656_CONTRACT),
            "valid_for_claim": "false",
        },
    ]


def poynting_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "POY3284_0_public_metric_Maxwell",
            "branch": "public Maxwell stress",
            "condition": "H=Z_Q *_{g_pub}F and Z_Q/readout factors are q-basic or parent-fixed",
            "C_R_effect": "C_S=0; Poynting is T_EM^{0i} in the same public geometry",
            "source_side_effect": "include T_EM in T_total once",
            "blocked_by": "Hodge/impedance/readout parent ownership unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "POY3284_1_constitutive_medium",
            "branch": "background constitutive chi",
            "condition": "chi is local, reciprocal, positive, nonbirefringent, nondispersive and reduces to metric Hodge",
            "C_R_effect": "if chi is q-basic, C_H=C_S=0; otherwise finite EM-medium/readout slopes remain",
            "source_side_effect": "derive public cone/Hodge but not EH operator",
            "blocked_by": "chi-to-Hodge theorem not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "POY3284_2_independent_background_flux",
            "branch": "non-EM MTS background energy flow",
            "condition": "flux is not the Maxwell Poynting vector and has its own stress/residual variable",
            "C_R_effect": "not a readout rescue; it belongs in E_res_munu or a named residual stress",
            "source_side_effect": "may source gravity only as explicit E_res/T_res component",
            "blocked_by": "needs separate field, stress, conservation and no-double-counting certificate",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "POY3284_3_forbidden_double_count",
            "branch": "Poynting counted as both T_EM and hidden background flux",
            "condition": "same EM energy flux used twice",
            "C_R_effect": "invalid",
            "source_side_effect": "forbidden by energy accounting",
            "blocked_by": "route rejected, not retained",
            "valid_for_claim": "false",
        },
    ]


def prediction_rows(bound: float) -> list[dict[str, Any]]:
    half = bound / 2.0
    twice = bound * 2.0
    return [
        {
            "row_id": "CRP3284_0_product_formula_ready_missing",
            "case": "general C_R product law",
            "C_R_prediction": "MISSING_NUMERIC_SUM_NS_CS",
            "C_R_abs_bound": fmt(bound),
            "C_e_prediction": "MISSING",
            "required_inputs": "factor list; exponents n_s; numeric slopes C_s; source paths; no double counting with C_J/C_Z",
            "result": "FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRP3284_1_qbasic_readout_zero_conditional",
            "case": "all readout factors q-basic",
            "C_R_prediction": "0",
            "C_R_abs_bound": fmt(bound),
            "C_e_prediction": "0_if_CJ_CZ_zero_else_MISSING",
            "required_inputs": "parent-signed q-basic readout functor for clocks/charge/Hodge/Poynting/material/kernel",
            "result": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRP3284_2_poynting_public_stress_conditional",
            "case": "Poynting is public T_EM flux",
            "C_R_prediction": "0_if_public_Hodge_and_flux_standard_qbasic",
            "C_R_abs_bound": fmt(bound),
            "C_e_prediction": "0_if_CJ_CZ_zero_else_MISSING",
            "required_inputs": "metric Hodge/impedance route plus public flux standard",
            "result": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRP3284_3_constitutive_medium_symbolic",
            "case": "nonmetric constitutive or impedance readout",
            "C_R_prediction": "n_H*C_H + n_S*C_S + n_mat*C_mat + ...",
            "C_R_abs_bound": fmt(bound),
            "C_e_prediction": "-C_R_if_CJ_CZ_zero_else_MISSING",
            "required_inputs": "Delta_chi/impedance/Poynting/material slopes",
            "result": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRP3284_4_clock_direct_product_waitstate",
            "case": "clock/spectroscopy alpha readout",
            "C_R_prediction": "MISSING_DIRECT_P_CLOCK_ALPHA_OR_FACTOR_SLOPES",
            "C_R_abs_bound": fmt(bound),
            "C_e_prediction": "MISSING",
            "required_inputs": "clock sensitivity plus MTS local alpha/readout slope in same units",
            "result": "REFUSE_OR_FAIL",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRP3284_5_half_bound_smoke",
            "case": "numeric smoke C_R inside pure-readout envelope",
            "C_R_prediction": fmt(half),
            "C_R_abs_bound": fmt(bound),
            "C_e_prediction": fmt(-half),
            "required_inputs": "SMOKE_NUMERIC_NONCLAIM",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRP3284_6_twice_bound_smoke",
            "case": "numeric smoke C_R outside pure-readout envelope",
            "C_R_prediction": fmt(twice),
            "C_R_abs_bound": fmt(bound),
            "C_e_prediction": fmt(-twice),
            "required_inputs": "SMOKE_NUMERIC_NONCLAIM",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
    ]


def try_float(value: str) -> float | None:
    try:
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    except Exception:
        return None


def runner_rows(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = {
        "CRP3284_0_product_formula_ready_missing": "REFUSE_OR_FAIL",
        "CRP3284_1_qbasic_readout_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "CRP3284_2_poynting_public_stress_conditional": "CONDITIONAL_NONNUMERIC_NONCLAIM",
        "CRP3284_3_constitutive_medium_symbolic": "SYMBOLIC_NONNUMERIC_NONCLAIM",
        "CRP3284_4_clock_direct_product_waitstate": "REFUSE_OR_FAIL",
        "CRP3284_5_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "CRP3284_6_twice_bound_smoke": "FAIL_BOUND",
    }
    rows: list[dict[str, Any]] = []
    for row in predictions:
        pred = str(row["C_R_prediction"])
        bound = float(row["C_R_abs_bound"])
        numeric = try_float(pred)
        if pred.startswith("MISSING"):
            result = "REFUSE_OR_FAIL"
            ratio = "MISSING"
        elif numeric is None and pred.startswith("0_if"):
            result = "CONDITIONAL_NONNUMERIC_NONCLAIM"
            ratio = "N/A"
        elif numeric is None:
            result = "SYMBOLIC_NONNUMERIC_NONCLAIM"
            ratio = "N/A"
        else:
            ratio_float = abs(numeric) / bound if bound > 0 else math.inf
            ratio = fmt(ratio_float)
            result = "PASS_NUMERIC_NONCLAIM" if ratio_float <= 1.0 else "FAIL_BOUND"
        expectation = expected[row["row_id"]]
        rows.append(
            {
                "row_id": row["row_id"],
                "C_R_prediction": pred,
                "prediction_over_bound": ratio,
                "result": result,
                "expected_result": expectation,
                "expectation_met": bool_str(result == expectation),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3284_0_product_law_derived",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "C_R=sum_s n_s L_v ln R_s is exact once readout factors are declared.",
        },
        {
            "gate_id": "GATE3284_1_qbasic_zero_theorem",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "if every factor descends through q, C_R=0; parent ownership is unsigned.",
        },
        {
            "gate_id": "GATE3284_2_poynting_placement_guard",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "Poynting is public T_EM flux or independent E_res flux, never both.",
        },
        {
            "gate_id": "GATE3284_3_finite_CR_slope_sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no numeric source-backed C_R factor slopes are supplied in 3284.",
        },
        {
            "gate_id": "GATE3284_4_no_empirical_shortcut",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "clock/MICROSCOPE/PPN bounds are not scored without a parent readout coefficient or zero theorem.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3284_0_product_law",
            "decision": "C_R is now a factorized readout product, not a vague readout leak.",
            "why_it_moves_forward": "future work can attack a named factor slope or prove all factors q-basic.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3284_1_poynting",
            "decision": "Poynting is admitted as a serious route to public Hodge/stress, but not as double-counted hidden energy.",
            "why_it_moves_forward": "this keeps the user's Poynting intuition while enforcing conservation/accounting.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3284_2_zero_route",
            "decision": "The best zero route is a parent q-basic readout functor across clocks, charge standards, Hodge/impedance, Poynting flux, material response and kernels.",
            "why_it_moves_forward": "this is one proof target, not seven disconnected missing ledgers.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3284_3_next_work",
            "decision": "Next should try to prove the public readout functor theorem or source the first finite factor slope.",
            "why_it_moves_forward": "forces a derivation/source fork instead of data-only testing.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3284_0_3285",
            "target_doc": "3285-Y5-R2FR-public-readout-functor-zero-proof-or-first-CR-factor-slope-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3285_public_readout_functor_zero_proof_or_first_CR_factor_slope.py",
            "objective": "Try to prove one parent public-readout functor theorem: clocks/rods/action units, charge standards, Hodge/impedance, Poynting flux, material detector response, and projection kernels all factor through q; if that fails, source the first finite C_R factor slope row using the 3284 product law.",
            "guardrail": "Do not score clock/MICROSCOPE/PPN data or claim C_R=0 unless the factor map is parent-owned; do not double-count Poynting as both T_EM and background E_res.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    factors: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    non_validation_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_after = snapshot_tree(FW)
    fw_changed = changed_count(fw_before, fw_after)
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": compact(detail, 520),
            }
        )

    add("VAL3284_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3284_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add(
        "VAL3284_2_outputs_parse",
        "all 3284 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3284_3_product_law_present",
        "exact product law theorem row is present",
        any(row["theorem_id"] == "CRPL3284_1_product_law" and "sum_s" in row["statement"] for row in theorem),
    )
    add(
        "VAL3284_4_factor_coverage",
        "readout factors include clock Hodge Poynting material charge kernel",
        all(
            any(token in row["factor_id"] or token in row["readout_factor"] for row in factors)
            for token in ["phase", "Hodge", "Poynting", "material", "charge", "projection"]
        ),
    )
    add(
        "VAL3284_5_poynting_no_double_count",
        "Poynting branch table includes forbidden double-count row",
        any(row["branch_id"] == "POY3284_3_forbidden_double_count" and row["C_R_effect"] == "invalid" for row in poynting),
    )
    add(
        "VAL3284_6_prediction_rows_nonclaim",
        "all C_R prediction rows remain nonclaim",
        all(row["valid_for_claim"] == "false" for row in predictions),
    )
    add(
        "VAL3284_7_runner_expectations",
        "C_R runner expectations all match",
        all(row["expectation_met"] == "true" for row in runner),
        ";".join(f"{row['row_id']}={row['result']}" for row in runner),
    )
    add(
        "VAL3284_8_claim_gates_false",
        "no 3284 gate allows local-GR/alpha/Maxwell claim",
        all(row["claim_allowed"] == "false" for row in promotion),
    )
    add(
        "VAL3284_9_next_target_public_readout",
        "next target is public readout functor or finite factor slope",
        any("public-readout" in row["target_doc"] and "Poynting" in row["guardrail"] for row in next_target),
    )
    add(
        "VAL3284_10_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3284_11_overall",
        "3284 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def write_doc(
    bound: float,
    theorem: list[dict[str, Any]],
    factors: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3284 - C_R readout product law and Poynting wave standard or zero theorem under AX1090

## Summary

3284 turns the readout branch into an exact algebraic object:

`R_alpha_readout = product_s R_s^{{n_s}}`

so

`C_R = L_v ln R_alpha_readout = sum_s n_s L_v ln R_s`.

This means `C_R=0` is not a wish. It follows if every readout factor is q-basic, or shift-protected, across the same parent public-readout functor. The factors are now named: clock/action standards, light-cone/rod standards, Hodge/impedance, Poynting flux, detector/material response, charge-calibration guard, and projection kernels.

The Poynting result is sharper than before: Poynting is allowed, but it has one legal home. It is either the public Maxwell stress flux `T_EM^{{0i}}`, or it is a separate named background residual in `E_res_munu`. It cannot be counted in both.

Pure readout bound inherited from the alpha row:

`|C_R| <= {fmt(bound)}` if `C_J=0`, `C_Z=0`, and `C_R` is the only live alpha/readout slope.

## C_R Product Law Theorem
{md_table(theorem, ["theorem_id", "claim_piece", "proof_status", "missing_for_claim"])}

## Readout Factor Ledger
{md_table(factors, ["factor_id", "readout_factor", "slope_symbol", "role", "current_status"])}

## Poynting Standard Branch Table
{md_table(poynting, ["branch_id", "branch", "condition", "C_R_effect", "source_side_effect", "blocked_by"])}

## First C_R Slope Rows
{md_table(predictions, ["row_id", "case", "C_R_prediction", "C_R_abs_bound", "result", "valid_for_claim"])}

## C_R Bound Runner
{md_table(runner, ["row_id", "C_R_prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(promotion, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decision, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_target, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validation, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    fw_before = snapshot_tree(FW)
    bound = alpha_bound()
    sources = source_register_rows()
    theorem = theorem_rows()
    factors = factor_rows()
    poynting = poynting_rows()
    predictions = prediction_rows(bound)
    runner = runner_rows(predictions)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["factors"], factors)
    write_csv(OUTPUTS["poynting"], poynting)
    write_csv(OUTPUTS["prediction"], predictions)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, theorem, factors, poynting, predictions, runner, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(bound, theorem, factors, poynting, predictions, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
