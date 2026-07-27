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

DOC = ROOT / "3282-Y5-R2FR-hidden-F2-coefficient-slot-ban-or-first-CZ-prediction-row-under-AX1090.md"

SRC_3271_DOC = ROOT / "3271-Y5-R2FR-hidden-visible-hom-typing-proof-or-coupling-coefficient-bound-pack-under-AX1090.md"
SRC_3280_DOC = ROOT / "3280-Y5-R2FR-CZ-CR-EM-stress-readout-coupling-derivation-or-source-bound-under-AX1090.md"
SRC_3281_DOC = ROOT / "3281-Y5-R2FR-unique-Maxwell-kinetic-owner-or-CZ-finite-bound-row-under-AX1090.md"
SRC_1049_DOC = ROOT / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md"
SRC_1051_DOC = ROOT / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"
SRC_1058_DOC = ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
SRC_1091_DOC = ROOT / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md"
SRC_1099_DOC = ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

SRC_3271_MATRIX = OUT / "P8_Y5_R2FR_3271_HIDDEN_VISIBLE_TYPING_PROOF_MATRIX.csv"
SRC_3273_DECOMP = OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv"
SRC_3273_RUNNER = OUT / "P8_Y5_R2FR_3273_CE_BOUND_RUNNER_RESULTS_NONCLAIM.csv"
SRC_3281_THEOREM = OUT / "P8_Y5_R2FR_3281_MAXWELL_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
SRC_3281_BOUND = OUT / "P8_Y5_R2FR_3281_CZ_FINITE_BOUND_ROWS_NONCLAIM.csv"
SRC_3281_VALIDATION = OUT / "P8_Y5_BRR545_3281_VALIDATION.csv"
SRC_1057_COUNTER = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
SRC_1099_EXC = OUT / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
SRC_1236_META = OUT / "P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv"
SRC_1467_F2 = OUT / "P8_Y5_R10_1467_NO_HIDDEN_F2_OPERATOR_CLASSIFICATION.csv"
SRC_3118_GATE = OUT / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3282_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3282_HIDDEN_F2_SLOT_THEOREM_ATTEMPT.csv",
    "audit": OUT / "P8_Y5_R2FR_3282_QBASIC_SHIFT_RADIATIVE_AUDIT.csv",
    "formula": OUT / "P8_Y5_R2FR_3282_CZ_RESIDUAL_FORMULA_ROWS.csv",
    "prediction": OUT / "P8_Y5_R2FR_3282_FIRST_CZ_PREDICTION_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3282_CZ_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3282_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3282_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3282_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3282_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 320) -> str:
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
        (SRC_3281_DOC, "3281 immediate handoff", ["hidden/radiative/readout", "C_Z Finite Bound Rows"]),
        (SRC_3281_THEOREM, "3281 Maxwell kinetic owner rows", ["MKO3281_2", "additive"]),
        (SRC_3281_BOUND, "3281 pure C_Z bound contract", ["CZB3281_0", "1.389797711495e-12"]),
        (SRC_3281_VALIDATION, "3281 validation", ["VAL3281_9_overall", "true"]),
        (SRC_3280_DOC, "3280 C_Z/C_R residual context", ["q_EM", "C_Z"]),
        (SRC_3271_DOC, "3271 hidden-visible typing theorem", ["QFT3271_2", "QFT3271_3"]),
        (SRC_3271_MATRIX, "3271 typing proof matrix", ["RED3271_1", "RED3271_3"]),
        (SRC_3273_DECOMP, "3273 alpha coefficient law", ["2 C_J - C_Z - C_R", "C_e"]),
        (SRC_3273_RUNNER, "3273 alpha bound runner", ["bound_value", "CE3273_1"]),
        (SRC_1049_DOC, "symmetry ban audit", ["SBT1049", "DOES_NOT_FORBID"]),
        (SRC_1051_DOC, "hidden-visible morphism obstruction", ["NMM1051_2", "counterexample"]),
        (SRC_1057_COUNTER, "F2 counterterm ledger", ["CT1057_1", "f(I_hid)"]),
        (SRC_1058_DOC, "visible operator domain exhaustion", ["ACP1058_0", "Z_A"]),
        (SRC_1091_DOC, "no-hidden-visible hom theorem status", ["ODH1091_6", "not derived"]),
        (SRC_1099_DOC, "unique EM kinetic owner doc", ["UEM1099_2", "f_X"]),
        (SRC_1099_EXC, "no-extra-F2 exclusion audit", ["EXC1099_0", "EXC1099_5"]),
        (SRC_1100_DOC, "T_Q/gauge norm signature", ["TQS1100_3", "Z1100_4"]),
        (SRC_1236_META, "no-hidden-visible coefficient meta theorem", ["META1236_1", "unique_F2"]),
        (SRC_1467_F2, "no-hidden-F2 operator classification", ["NHF1467_1", "NHF1467_3"]),
        (SRC_3118_GATE, "R2FR no-hidden-visible hom gate", ["NHV3118_0", "NHV3118_1"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3282_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def pure_cz_bound() -> float:
    for row in read_csv(SRC_3281_BOUND):
        if row.get("row_id") == "CZB3281_0_pure_CZ_bound_contract":
            return float(row["C_Z_abs_bound"])
    for row in read_csv(SRC_3273_RUNNER):
        if row.get("prediction_id") == "CE3273_1_theorem_zero_conditional":
            return float(row["bound_value"])
    raise RuntimeError("could not locate pure C_Z bound")


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HFT3282_0_qbasic_visible_coefficient_slot_ban",
            "claim_piece": "ban hidden F2 coefficient by q-basic visible algebra",
            "statement": "Let S_EM=-(1/4) int mu_Q Z_Q(Phi) F_Q^2 and q:P->B. If the ordinary EM kinetic coefficient algebra is q-basic, Z_Q=q^*Zbar_Q, then every vertical v in ker(Dq) obeys L_v Z_Q=0 and therefore C_Z=L_v ln Z_Q=0.",
            "proof_sketch": "Chain rule: D(q^*Zbar_Q)[v]=DZbar_Q[Dq(v)]=0. A term f_X(I_hid)F_Q^2 is not an admissible ordinary coefficient unless f_X(I_hid) is q-basic.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "parent has not signed A_ord=q^*A_Q tensor A_fixed plus q-basic readout/effective action.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HFT3282_1_exact_hidden_shift_slot_ban",
            "claim_piece": "ban non-derivative hidden F2 coefficient by exact hidden shift",
            "statement": "If I_hid shifts along the local vertical generator and F_Q^2 is shift-neutral, exact invariance of the parent and effective action forces L_v f_X(I_hid)=0; any surviving constant is lambda_A0 and gives no C_Z.",
            "proof_sketch": "For arbitrary shift parameter epsilon, delta[f_X(I_hid)F_Q^2]=(epsilon L_v f_X)F_Q^2. Invariance for arbitrary F_Q^2 gives L_v f_X=0; on a connected fibre f_X is constant.",
            "proof_status": "EXACT_CONDITIONAL_WARD_THEOREM",
            "missing_for_claim": "exact hidden shift, anomaly/radiative preservation, boundary silence, and readout preservation are unsigned.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HFT3282_2_trivial_hidden_invariant_algebra",
            "claim_piece": "ban hidden F2 coefficient by no surviving scalar invariant",
            "statement": "If the fibre-local hidden invariant algebra feeding ordinary coefficients is only constants, O(C_hid)^inv=R, then f_X(I_hid) is constant and cannot create local C_Z drift.",
            "proof_sketch": "The only allowed scalar coefficient is lambda_A0; L_v lambda_A0=0.",
            "proof_status": "EXACT_CONDITIONAL_ALGEBRA_THEOREM",
            "missing_for_claim": "current corpus still retains scalar obstruction/counterexample rows.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HFT3282_3_hidden_scalar_countermodel",
            "claim_piece": "show exactly why ordinary covariance/U1 are insufficient",
            "statement": "If a non-q-basic scalar I_hid survives and the coefficient slot accepts scalar functions, Z_Q=Z_0+epsilon I_hid is legal under ordinary covariance and visible U1, with C_Z=epsilon L_v I_hid/(Z_0+epsilon I_hid).",
            "proof_sketch": "The operator sqrt(-g) I_hid F_Q^2 is a scalar density and is visible-U1 invariant; only the stronger q-basic/shift/algebra gates remove it.",
            "proof_status": "EXACT_COUNTERMODEL",
            "missing_for_claim": "none as a countermodel; it blocks promotion unless a stronger parent gate is signed.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HFT3282_4_current_verdict",
            "claim_piece": "hidden F2 slot status after 3282",
            "statement": "3282 proves the exact zero routes and the exact residual law, but current MTS does not yet sign the parent condition needed to claim C_Z=0.",
            "proof_sketch": "The q-basic, shift, and trivial-invariant routes are sufficient; none is currently parent-owned across action, radiative corrections, and readout.",
            "proof_status": "NOT_PROMOTED_CURRENT_CORPUS",
            "missing_for_claim": "choose and sign one route, or source numeric f'_X, L_v I_hid, Z_Q, radiative, and readout slopes.",
            "valid_for_claim": "false",
        },
    ]


def audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "QSR3282_0_ordinary_covariance",
            "gate": "ordinary covariance",
            "status": "INSUFFICIENT",
            "reason": "sqrt(-g) f_X(I_hid) F_Q^2 is a scalar density.",
            "moves_forward_by": "do not revisit this as a ban; it is already a negative result.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "QSR3282_1_visible_U1",
            "gate": "visible U1 gauge invariance",
            "status": "INSUFFICIENT",
            "reason": "F_Q^2 is gauge invariant, so scalar coefficient functions are allowed.",
            "moves_forward_by": "use unique parent gauge norm plus q-basic coefficient algebra, not gauge invariance alone.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "QSR3282_2_qbasic_visible_algebra",
            "gate": "ordinary coefficient algebra descends through q",
            "status": "SUFFICIENT_IF_PARENT_SIGNED",
            "reason": "q-basic coefficients have zero vertical derivative, so hidden scalar F2 slots vanish as local drift sources.",
            "moves_forward_by": "prove A_ord=q^*A_Q tensor A_fixed and no hidden-to-visible coefficient hom.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "QSR3282_3_exact_hidden_shift",
            "gate": "exact hidden shift/Ward identity",
            "status": "SUFFICIENT_IF_PARENT_AND_EFFECTIVE_SIGNED",
            "reason": "non-derivative f_X(I_hid)F_Q^2 breaks the shift unless f_X is constant.",
            "moves_forward_by": "source or derive the actual vertical generator action and anomaly-free effective Ward identity.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "QSR3282_4_radiative_reentry",
            "gate": "integrating out hidden sector",
            "status": "LIVE_RISK",
            "reason": "even if tree-level f_X is absent, delta_lambda_rad(mu,I_hid) can re-enter unless the effective action remains q-basic/shift-protected.",
            "moves_forward_by": "derive q-basic effective action or source a numeric radiative slope.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "QSR3282_5_readout_reentry",
            "gate": "observed alpha/readout map",
            "status": "LIVE_RISK",
            "reason": "bare Z_Q can be stable while the observed readout R_alpha drifts.",
            "moves_forward_by": "move C_R to its own owner proof or finite source-bound row after C_Z input attempt.",
            "valid_for_claim": "false",
        },
    ]


def formula_rows(bound: float) -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "FORM3282_0_ZQ_decomposition",
            "object": "observed Maxwell kinetic coefficient",
            "formula": "Z_Q = Z_0 + lambda_A0 + sum_a f_a(I^a_hid) + delta_lambda_rad(mu,I_hid) + delta_Z_readout",
            "derivation_status": "DECOMPOSITION_FROM_3281_COUNTERTERM_LEDGER",
            "claim_use": "identifies every place hidden/radiative/readout drift can enter",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FORM3282_1_general_CZ_law",
            "object": "local Maxwell kinetic residual",
            "formula": "C_Z = L_v ln Z_Q = [sum_a f_a,_b L_v I^b_hid + L_v delta_lambda_rad + L_v delta_Z_readout] / Z_Q",
            "derivation_status": "EXACT_VERTICAL_DERIVATIVE",
            "claim_use": "turns the vague missing coupling into concrete numeric inputs",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FORM3282_2_single_hidden_scalar_law",
            "object": "single scalar hidden F2 leak",
            "formula": "C_Z = f'_X(I_hid) L_v I_hid / [Z_0 + lambda_A0 + f_X(I_hid)]",
            "derivation_status": "EXACT_SPECIAL_CASE",
            "claim_use": "first numeric C_Z row needs f'_X, L_v I_hid, and denominator Z_Q",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FORM3282_3_qbasic_zero_limit",
            "object": "q-basic visible coefficient",
            "formula": "Z_Q=q^*Zbar_Q and v in ker(Dq) => C_Z=0",
            "derivation_status": "EXACT_ZERO_LIMIT",
            "claim_use": "cleanest local-GR route if parent signs q-basic action/readout",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FORM3282_4_exact_shift_zero_limit",
            "object": "exact hidden shift",
            "formula": "L_v f_X=0 and L_v delta_lambda_rad=0 => C_Z=0 up to constant alpha-value debt",
            "derivation_status": "EXACT_ZERO_LIMIT_IF_WARD_PRESERVED",
            "claim_use": "second clean route if the vertical generator is an exact symmetry",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FORM3282_5_pure_CZ_bound_map",
            "object": "alpha residual under signed C_J=C_R=0",
            "formula": f"C_e = -C_Z and |C_Z| <= {fmt(bound)}",
            "derivation_status": "BOUND_MAP_FROM_3273_AND_3281",
            "claim_use": "scores any future single C_Z prediction without cancellation games",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FORM3282_6_numeric_input_contract",
            "object": "first real prediction row requirements",
            "formula": "required: source-backed Z_Q, f_a,_b, L_v I^b_hid, L_v delta_lambda_rad, L_v delta_Z_readout, units/normalization, and source paths",
            "derivation_status": "FINITE_ROW_CONTRACT",
            "claim_use": "prevents symbolic placeholders from being scored as evidence",
            "valid_for_claim": "false",
        },
    ]


def prediction_rows(bound: float) -> list[dict[str, Any]]:
    half = bound / 2.0
    twice = bound * 2.0
    return [
        {
            "row_id": "CZP3282_0_formula_ready_prediction_missing",
            "case": "general hidden/radiative/readout C_Z formula",
            "C_Z_prediction": "MISSING_NUMERIC_FPRIME_LVI_OVER_Z",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "MISSING",
            "required_inputs": "Z_Q; f_a,_b; L_v I^b_hid; L_v delta_lambda_rad; L_v delta_Z_readout; units; source paths",
            "source_path": str(SRC_3281_BOUND),
            "result": "FINITE_FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZP3282_1_qbasic_theorem_zero_conditional",
            "case": "q-basic visible coefficient algebra signed",
            "C_Z_prediction": "0",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "0_if_CJ_CR_zero_else_MISSING",
            "required_inputs": "parent-signed q-basic ordinary coefficient algebra; q-basic effective action; q-basic readout",
            "source_path": str(SRC_3271_MATRIX),
            "result": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZP3282_2_exact_shift_theorem_zero_conditional",
            "case": "exact hidden shift/Ward identity signed",
            "C_Z_prediction": "0_if_exact_shift_and_Ward_signed",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "0_if_CJ_CR_zero_else_MISSING",
            "required_inputs": "vertical generator; exact hidden shift; anomaly-free radiative closure; boundary/readout preservation",
            "source_path": str(SRC_1099_EXC),
            "result": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZP3282_3_single_hidden_scalar_symbolic",
            "case": "one hidden scalar F2 leak",
            "C_Z_prediction": "f'_X(I_hid)*L_v(I_hid)/Z_Q",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "-f'_X(I_hid)*L_v(I_hid)/Z_Q_if_CJ_CR_zero",
            "required_inputs": "numeric f'_X; numeric L_v I_hid; numeric Z_Q",
            "source_path": str(SRC_1057_COUNTER),
            "result": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZP3282_4_radiative_readout_symbolic",
            "case": "radiative/readout re-entry",
            "C_Z_prediction": "(L_v delta_lambda_rad + L_v delta_Z_readout)/Z_Q",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "-C_Z_if_CJ_CR_zero_else_MISSING",
            "required_inputs": "numeric effective radiative slope; numeric readout slope; denominator Z_Q",
            "source_path": str(SRC_1058_DOC),
            "result": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZP3282_5_half_bound_smoke",
            "case": "numeric smoke C_Z inside pure-CZ envelope",
            "C_Z_prediction": fmt(half),
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": fmt(-half),
            "required_inputs": "SMOKE_NUMERIC_NONCLAIM",
            "source_path": "SMOKE_NUMERIC_NONCLAIM",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZP3282_6_twice_bound_smoke",
            "case": "numeric smoke C_Z outside pure-CZ envelope",
            "C_Z_prediction": fmt(twice),
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": fmt(-twice),
            "required_inputs": "SMOKE_NUMERIC_NONCLAIM",
            "source_path": "SMOKE_NUMERIC_NONCLAIM",
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
        "CZP3282_0_formula_ready_prediction_missing": "REFUSE_OR_FAIL",
        "CZP3282_1_qbasic_theorem_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "CZP3282_2_exact_shift_theorem_zero_conditional": "CONDITIONAL_NONNUMERIC_NONCLAIM",
        "CZP3282_3_single_hidden_scalar_symbolic": "SYMBOLIC_NONNUMERIC_NONCLAIM",
        "CZP3282_4_radiative_readout_symbolic": "SYMBOLIC_NONNUMERIC_NONCLAIM",
        "CZP3282_5_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "CZP3282_6_twice_bound_smoke": "FAIL_BOUND",
    }
    rows: list[dict[str, Any]] = []
    for row in predictions:
        pred = str(row["C_Z_prediction"])
        bound = float(row["C_Z_abs_bound"])
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
                "C_Z_prediction": pred,
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
            "gate_id": "GATE3282_0_residual_formula_derived",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "C_Z residual law is exact: vertical derivative of ln Z_Q with hidden, radiative, and readout terms separated.",
        },
        {
            "gate_id": "GATE3282_1_qbasic_slot_ban_theorem",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "q-basic visible coefficient theorem is exact but parent q-basic action/readout is unsigned.",
        },
        {
            "gate_id": "GATE3282_2_exact_shift_slot_ban_theorem",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "exact hidden shift theorem is exact but parent symmetry, radiative Ward identity, and readout preservation are unsigned.",
        },
        {
            "gate_id": "GATE3282_3_countermodel_retained",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "ordinary covariance and visible U1 still allow a non-q-basic scalar coefficient countermodel.",
        },
        {
            "gate_id": "GATE3282_4_numeric_CZ_prediction_sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no source-backed numeric f'_X, L_v I_hid, Z_Q, radiative slope, or readout slope is present.",
        },
        {
            "gate_id": "GATE3282_5_no_local_GR_alpha_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3282 is a derivation and scoring contract checkpoint, not an R10/local-GR pass.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3282_0_derivation_result",
            "decision": "The hidden F2 problem is now an explicit residual formula, not a vague missing coupling.",
            "why_it_moves_forward": "future rows must provide f'_X, L_v I_hid, Z_Q, and radiative/readout slopes or select a zero theorem route.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3282_1_zero_route_result",
            "decision": "Two clean zero routes exist: q-basic visible coefficient algebra or exact hidden shift/Ward protection.",
            "why_it_moves_forward": "the local-GR route can now target parent signatures instead of circling ordinary covariance/U1.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3282_2_countermodel_result",
            "decision": "Without those stronger parent signatures, the scalar countermodel Z_Q=Z_0+epsilon I_hid remains legal.",
            "why_it_moves_forward": "this prevents smuggling the plateau/closure axiom into the EM coupling.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3282_3_next_work_result",
            "decision": "Next work should either source a numeric C_Z input pack or demote finite C_Z to closure-only and move to C_R readout.",
            "why_it_moves_forward": "the next checkpoint must force a fork instead of re-arguing the same theorem gates.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3282_0_3283",
            "target_doc": "3283-Y5-R2FR-first-numeric-CZ-input-source-pack-or-CR-readout-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3283_first_numeric_CZ_input_source_pack_or_CR_readout_demotion.py",
            "objective": "Use the 3282 formula to source a real numeric C_Z input pack (Z_Q, f'_X, L_v I_hid, radiative/readout slopes, units, and source paths) or explicitly demote finite C_Z to closure-only and move to the C_R readout owner proof/bound.",
            "guardrail": "Do not restate covariance/U1/q-basic/shift audits unless a new parent source signs them; 3283 must either produce numeric source-backed inputs or force the C_R branch.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    formula: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
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
                "detail": compact(detail, 500),
            }
        )

    add(
        "VAL3282_0_sources_exist",
        "all cited source paths exist",
        all(row["exists"] == "true" for row in sources),
    )
    add(
        "VAL3282_1_sources_parse",
        "all cited source paths parse",
        all(row["parse_ok"] == "true" for row in sources),
    )
    add(
        "VAL3282_2_outputs_parse",
        "all 3282 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3282_3_qbasic_shift_theorems_present",
        "q-basic and exact shift zero theorem rows exist",
        any(row["theorem_id"] == "HFT3282_0_qbasic_visible_coefficient_slot_ban" for row in theorem)
        and any(row["theorem_id"] == "HFT3282_1_exact_hidden_shift_slot_ban" for row in theorem),
    )
    add(
        "VAL3282_4_countermodel_retained",
        "hidden scalar countermodel row remains explicit",
        any(row["theorem_id"] == "HFT3282_3_hidden_scalar_countermodel" for row in theorem),
    )
    add(
        "VAL3282_5_residual_formula_present",
        "general C_Z residual formula has required derivative inputs",
        any(
            row["formula_id"] == "FORM3282_1_general_CZ_law"
            and "sum_a" in row["formula"]
            and "L_v delta_lambda_rad" in row["formula"]
            for row in formula
        ),
    )
    add(
        "VAL3282_6_prediction_rows_nonclaim",
        "all C_Z prediction rows remain nonclaim",
        all(row["valid_for_claim"] == "false" for row in predictions),
    )
    add(
        "VAL3282_7_runner_expectations",
        "C_Z runner expectations all match",
        all(row["expectation_met"] == "true" for row in runner),
        ";".join(f"{row['row_id']}={row['result']}" for row in runner),
    )
    add(
        "VAL3282_8_claim_gates_false",
        "no 3282 gate allows local-GR/alpha/Maxwell claim",
        all(row["claim_allowed"] == "false" for row in promotion),
    )
    add(
        "VAL3282_9_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3282_10_overall",
        "3282 validation overall",
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
    audit: list[dict[str, Any]],
    formula: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3282 - Hidden F2 coefficient slot ban or first C_Z prediction row under AX1090

## Summary

3282 does the derivation step the 3281 handoff demanded. The hidden/radiative `F_Q^2` slot is now reduced to a precise local residual:

`C_Z = L_v ln Z_Q = [sum_a f_a,_b L_v I^b_hid + L_v delta_lambda_rad + L_v delta_Z_readout] / Z_Q`.

So the issue is no longer just "the coupling is missing". Either the parent action signs a q-basic visible coefficient algebra or exact hidden shift/Ward protection, in which case `C_Z=0`; or the theory must supply numeric source-backed inputs for `f'_X`, `L_v I_hid`, `Z_Q`, radiative slope, and readout slope. Ordinary covariance and visible U(1) still do not ban `f_X(I_hid)F_Q^2`.

The pure no-cancellation bound inherited from 3281 remains:

`|C_Z| <= {fmt(bound)}` when `C_J=0`, `C_R=0`, and `C_Z` is the only live alpha/EM slope.

## Hidden F2 Slot Theorem Attempt
{md_table(theorem, ["theorem_id", "claim_piece", "proof_status", "missing_for_claim"])}

## q-Basic / Shift / Radiative Audit
{md_table(audit, ["audit_id", "gate", "status", "reason", "moves_forward_by"])}

## C_Z Residual Formula Rows
{md_table(formula, ["formula_id", "object", "formula", "derivation_status", "claim_use"])}

## First C_Z Prediction Rows
{md_table(predictions, ["row_id", "case", "C_Z_prediction", "C_Z_abs_bound", "result", "valid_for_claim"])}

## C_Z Bound Runner
{md_table(runner, ["row_id", "C_Z_prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

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
    bound = pure_cz_bound()
    sources = source_register_rows()
    theorem = theorem_rows()
    audit = audit_rows()
    formula = formula_rows(bound)
    predictions = prediction_rows(bound)
    runner = runner_rows(predictions)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["formula"], formula)
    write_csv(OUTPUTS["prediction"], predictions)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, theorem, formula, predictions, runner, promotion)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(bound, theorem, audit, formula, predictions, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
