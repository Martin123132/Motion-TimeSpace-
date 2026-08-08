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

DOC = ROOT / "3281-Y5-R2FR-unique-Maxwell-kinetic-owner-or-CZ-finite-bound-row-under-AX1090.md"

SRC_3271_DOC = ROOT / "3271-Y5-R2FR-hidden-visible-hom-typing-proof-or-coupling-coefficient-bound-pack-under-AX1090.md"
SRC_3280_DOC = ROOT / "3280-Y5-R2FR-CZ-CR-EM-stress-readout-coupling-derivation-or-source-bound-under-AX1090.md"
SRC_1049_DOC = ROOT / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md"
SRC_1051_DOC = ROOT / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"
SRC_1058_DOC = ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
SRC_1091_DOC = ROOT / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md"
SRC_1099_DOC = ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

SRC_3271_MATRIX = OUT / "P8_Y5_R2FR_3271_HIDDEN_VISIBLE_TYPING_PROOF_MATRIX.csv"
SRC_3273_DECOMP = OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv"
SRC_3273_RUNNER = OUT / "P8_Y5_R2FR_3273_CE_BOUND_RUNNER_RESULTS_NONCLAIM.csv"
SRC_3280_GATE = OUT / "P8_Y5_R2FR_3280_CZ_CR_OWNER_GATE_AUDIT.csv"
SRC_3280_ROWS = OUT / "P8_Y5_R2FR_3280_CZ_CR_SOURCE_BOUND_ROWS_NONCLAIM.csv"
SRC_3280_VALIDATION = OUT / "P8_Y5_BRR545_3280_VALIDATION.csv"
SRC_1057_THEOREM = OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"
SRC_1057_COUNTER = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
SRC_1099_OWNER = OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
SRC_1099_EXC = OUT / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
SRC_1101_GAUGE = OUT / "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv"
SRC_1236_META = OUT / "P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv"
SRC_1467_F2 = OUT / "P8_Y5_R10_1467_NO_HIDDEN_F2_OPERATOR_CLASSIFICATION.csv"
SRC_3118_GATE = OUT / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3281_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3281_MAXWELL_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
    "operator_audit": OUT / "P8_Y5_R2FR_3281_NO_EXTRA_F2_OPERATOR_AUDIT.csv",
    "lambda_split": OUT / "P8_Y5_R2FR_3281_LAMBDA_FX_RADIATIVE_SPLIT.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3281_CZ_FINITE_BOUND_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3281_CZ_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3281_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3281_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3281_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3281_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: str, limit: int = 300) -> str:
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
    hits: list[str] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 240)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3280_DOC, "3280 handoff", ["C_Z/C_R", "q_EM"]),
        (SRC_3280_GATE, "3280 C_Z/C_R owner gate", ["CZCR3280_0", "CZCR3280_1"]),
        (SRC_3280_ROWS, "3280 C_Z/C_R source-bound rows", ["ZRB3280_4", "ZRB3280_5"]),
        (SRC_3280_VALIDATION, "3280 validation", ["VAL3280_9_overall", "true"]),
        (SRC_3271_DOC, "3271 hidden-visible typing theorem", ["QFT3271_2", "ENV3271_0"]),
        (SRC_3271_MATRIX, "3271 typing proof matrix", ["RED3271_1", "RED3271_3"]),
        (SRC_3273_DECOMP, "3273 C_e law", ["ADECOMP3273_1", "2 C_J - C_Z - C_R"]),
        (SRC_3273_RUNNER, "3273 alpha bound runner", ["ARUN3273_1", "bound_value"]),
        (SRC_1049_DOC, "ordinary symmetries cannot ban f_X F2", ["SBT1049_1", "DOES_NOT_FORBID"]),
        (SRC_1051_DOC, "no-mixed morphism obstruction", ["NMM1051_2", "f_X F^2"]),
        (SRC_1057_THEOREM, "unique Maxwell subblock attempt", ["UMS1057_2", "UMS1057_5"]),
        (SRC_1057_COUNTER, "F2 counterterm ledger", ["CT1057_0", "CT1057_1"]),
        (SRC_1058_DOC, "visible operator exhaustion", ["VOE1058_5", "ACP1058_0"]),
        (SRC_1091_DOC, "no-hidden-visible hom theorem status", ["ODH1091_6", "OBS1091_0"]),
        (SRC_1099_DOC, "unique EM kinetic owner doc", ["UEM1099_2", "EXC1099_1"]),
        (SRC_1099_OWNER, "1099 EM kinetic owner rows", ["UEM1099_3", "NO_EXTRA_F2"]),
        (SRC_1099_EXC, "1099 no-extra-F2 audit", ["EXC1099_0", "EXC1099_5"]),
        (SRC_1100_DOC, "T_Q/gauge norm signature", ["TQS1100_3", "Z1100_4_total"]),
        (SRC_1101_GAUGE, "1101 gauge norm theorem attempt", ["GFT1101_4", "GAUGE_NORM_OWNER_NOT_DERIVED"]),
        (SRC_1236_META, "no-hidden-visible coefficient meta theorem", ["META1236_1", "unique_F2"]),
        (SRC_1467_F2, "no-hidden-F2 operator classification", ["NHF1467_1", "NHF1467_3"]),
        (SRC_3118_GATE, "R2FR no-hidden-visible hom gate", ["NHV3118_0", "NHV3118_1"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3281_{idx}",
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
    for row in read_csv(SRC_3273_RUNNER):
        if row.get("prediction_id") == "CE3273_1_theorem_zero_conditional":
            return float(row["bound_value"])
    return float(read_csv(SRC_3273_RUNNER)[0]["bound_value"])


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "MKO3281_0_parent_curvature_norm",
            "claim_piece": "parent curvature norm gives one candidate Maxwell coefficient",
            "statement": "If A_parent=A_Q T_Q+A_perp and S_parent contains -(C_P/4)int <F_parent,F_parent>_P, then the visible Q subblock gives Z_parent=C_P N_Q with N_Q=<T_Q,T_Q>_P.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "T_Q parent object, fixed nonrescalable fibre norm N_Q, and fixed C_P must be parent-signed.",
            "consequence": "the parent piece has L_v ln(C_P N_Q)=0 when C_P,N_Q are fixed representation/topological data.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MKO3281_1_vertical_zero_chain_rule",
            "claim_piece": "C_Z zero from descended coefficient",
            "statement": "If Z_Q=q^*Z_bar or Z_Q=C_P N_Q with fixed data and v in ker(Dq), then C_Z=L_v ln Z_Q=0.",
            "proof_status": "EXACT_CHAIN_RULE_THEOREM",
            "missing_for_claim": "current corpus has not signed that the full observed Z_Q is only the parent piece.",
            "consequence": "this is the mathematically clean C_Z theorem-zero route.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MKO3281_2_additive_counterterm_law",
            "claim_piece": "observed Maxwell coefficient decomposition",
            "statement": "Z_Q=Z_parent+lambda_A+f_X(I_hid)+delta_lambda_rad+delta_Z_readout; therefore C_Z=L_v ln Z_Q.",
            "proof_status": "COUNTERTERM_LEDGER_DERIVED",
            "missing_for_claim": "no-extra-F2, no-hidden-visible hom, and radiative/readout closure are unsigned.",
            "consequence": "hidden or radiative pieces can create a C_Z leak even when the parent curvature norm exists.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MKO3281_3_constant_lambda_split",
            "claim_piece": "constant lambda_A is alpha-value debt, not vertical C_Z drift",
            "statement": "If lambda_A is hidden-independent and L_v lambda_A=0, then it changes the absolute alpha value but contributes no local vertical C_Z.",
            "proof_status": "EXACT_LOCAL_DERIVATIVE_SPLIT",
            "missing_for_claim": "absolute alpha value remains unpredicted unless parent norm fixes the total constant coefficient.",
            "consequence": "do not confuse failure to predict alpha's value with a local GR/alpha-drift residual.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MKO3281_4_current_status",
            "claim_piece": "unique Maxwell kinetic owner promotion",
            "statement": "MKO3281_0..3 plus no hidden-visible F2 target and radiative/readout stability would close C_Z.",
            "proof_status": "NOT_PROMOTED_CURRENT_CORPUS",
            "missing_for_claim": "A_ord=q*A_Q plus A_fixed, no hidden scalar target, fixed gauge norm, and radiative/readout closure remain unsigned.",
            "consequence": "C_Z zero remains a good theorem route, but not a claim.",
            "valid_for_claim": "false",
        },
    ]


def operator_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "F2AUD3281_0_diffeomorphism",
            "operator": "f_X(I_hid) F_Q^2",
            "test": "diffeomorphism covariance",
            "result": "DOES_NOT_FORBID",
            "reason": "a scalar coefficient times F_Q^2 is a scalar density.",
            "repair": "operator-domain exhaustion, product/sequester functor, exact shift, or trivial hidden invariant algebra.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "F2AUD3281_1_U1_gauge",
            "operator": "f_X(I_hid) F_Q^2",
            "test": "visible U1 gauge invariance",
            "result": "DOES_NOT_FORBID",
            "reason": "F_Q^2 is gauge invariant; U1 alone controls A/J structure, not the scalar kinetic coefficient.",
            "repair": "unique parent gauge norm plus no-extra-F2 domain theorem.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "F2AUD3281_2_compact_U1",
            "operator": "continuous Z_Q coefficient",
            "test": "compact charge lattice",
            "result": "INSUFFICIENT",
            "reason": "compact U1 can quantize labels but does not by itself fix g_EM^{-2}.",
            "repair": "fixed fibre norm/level/index/monopole source plus readout closure.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "F2AUD3281_3_typed_visible_algebra",
            "operator": "hidden-to-visible coefficient hom",
            "test": "A_ord=q*A_Q tensor A_fixed",
            "result": "WOULD_FORBID_IF_PARENT_SIGNED",
            "reason": "if visible coefficients have no hidden argument slot, L_v Z_Q=0 by quotient descent.",
            "repair": "derive the parent ordinary visible coefficient algebra rather than adopting it as closure.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "F2AUD3281_4_radiative_readout",
            "operator": "delta_lambda_rad(mu,Xhat)F_Q^2 or readout alpha_X",
            "test": "effective/readout stability",
            "result": "UNSIGNED_REQUIRED_GATE",
            "reason": "a tree-level ban is insufficient if loops or readout regenerate hidden-dependent Z_Q.",
            "repair": "q-basic effective action/readout theorem or finite product/source-bound row.",
            "valid_for_claim": "false",
        },
    ]


def lambda_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "LS3281_0_parent_piece",
            "term": "Z_parent=C_P N_Q",
            "vertical_slope": "0_if_C_P_and_N_Q_parent_fixed",
            "alpha_value_effect": "sets part or all of alpha normalization",
            "status": "CONDITIONAL_PARENT_OWNER",
            "valid_for_claim": "false",
        },
        {
            "split_id": "LS3281_1_constant_lambda",
            "term": "lambda_A0 F_Q^2",
            "vertical_slope": "0_if_lambda_A0_hidden_independent",
            "alpha_value_effect": "changes absolute alpha value; not a local vertical drift",
            "status": "VALUE_DEBT_NOT_LOCAL_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "split_id": "LS3281_2_hidden_scalar",
            "term": "f_X(I_hid)F_Q^2",
            "vertical_slope": "L_v ln(Z_parent+f_X)",
            "alpha_value_effect": "creates local alpha/EM stress drift and WEP/clock/R10 pressure",
            "status": "RETAINED_CZ_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "split_id": "LS3281_3_radiative",
            "term": "delta_lambda_rad(mu,Xhat)F_Q^2",
            "vertical_slope": "L_v ln(Z_parent+delta_lambda_rad)",
            "alpha_value_effect": "re-enters after tree-level descent unless effective/readout closure is signed",
            "status": "RETAINED_CZ_CR_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "split_id": "LS3281_4_readout",
            "term": "R_alpha_readout",
            "vertical_slope": "C_R=L_v ln R_alpha",
            "alpha_value_effect": "dimensionless observed alpha conversion can drift independently of bare Z_Q",
            "status": "RETAINED_CR_RESIDUAL",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    bound = alpha_bound()
    return [
        {
            "row_id": "CZB3281_0_pure_CZ_bound_contract",
            "case": "pure C_Z leak; C_J=0 and C_R=0 signed separately; no cancellation",
            "C_Z_prediction": "MISSING_SOURCE_BACKED_CZ_VALUE",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "MISSING",
            "side_conditions": "C_J theorem-zero signed; C_R readout-zero signed; C_Z is only nonzero alpha/EM slope",
            "source_path": str(SRC_3273_DECOMP),
            "result": "FINITE_BOUND_CONTRACT_READY_PREDICTION_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZB3281_1_CZ_theorem_zero_conditional",
            "case": "unique Maxwell kinetic owner and no-extra-F2 signed",
            "C_Z_prediction": "0",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "0_if_CJ_CR_zero_else_MISSING",
            "side_conditions": "fixed C_P N_Q; no hidden/radiative/readout F2 re-entry",
            "source_path": str(SRC_1099_OWNER),
            "result": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZB3281_2_constant_lambda_value_debt",
            "case": "constant lambda_A0 F_Q^2",
            "C_Z_prediction": "0_if_lambda_A0_hidden_independent",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "0_if_CJ_CR_zero_else_MISSING",
            "side_conditions": "constant lambda has no vertical derivative but alpha value remains unpredicted",
            "source_path": str(SRC_1057_COUNTER),
            "result": "VALUE_DEBT_NOT_LOCAL_CZ_DRIFT",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZB3281_3_hidden_F2_missing",
            "case": "hidden scalar f_X(I_hid)F_Q^2",
            "C_Z_prediction": "MISSING_NUMERIC_LV_LN_ZQ_SLOPE",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "MISSING_NUMERIC_CZ_COUNTERTERM_SLOPE",
            "side_conditions": "no cancellation with C_J/C_R allowed",
            "source_path": str(SRC_1057_COUNTER),
            "result": "RETAINED_RESIDUAL_NUMERIC_SLOPE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZB3281_4_radiative_readout_missing",
            "case": "radiative/readout F2 re-entry",
            "C_Z_prediction": "MISSING_DELTA_LAMBDA_RAD_OR_READOUT_SLOPE",
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": "MISSING",
            "side_conditions": "effective action/readout closure unsigned",
            "source_path": str(SRC_1058_DOC),
            "result": "RETAINED_RESIDUAL_NUMERIC_SLOPE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZB3281_5_half_bound_smoke",
            "case": "numeric smoke C_Z inside pure-CZ envelope",
            "C_Z_prediction": fmt(bound / 2.0),
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": fmt(-bound / 2.0),
            "side_conditions": "SMOKE_NUMERIC_NONCLAIM",
            "source_path": "SMOKE_NUMERIC_NONCLAIM",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CZB3281_6_twice_bound_smoke",
            "case": "numeric smoke C_Z outside pure-CZ envelope",
            "C_Z_prediction": fmt(2.0 * bound),
            "C_Z_abs_bound": fmt(bound),
            "C_e_prediction": fmt(-2.0 * bound),
            "side_conditions": "SMOKE_NUMERIC_NONCLAIM",
            "source_path": "SMOKE_NUMERIC_NONCLAIM",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
    ]


def runner_result(row: dict[str, Any]) -> tuple[str, str, str, str]:
    prediction = str(row["C_Z_prediction"])
    bound = float(row["C_Z_abs_bound"])
    if "MISSING" in prediction:
        return ("MISSING", "false", "REFUSE_OR_FAIL", "REFUSE_OR_FAIL")
    if "if_" in prediction:
        return ("N/A", "N/A", "CONDITIONAL_NONNUMERIC_NONCLAIM", "CONDITIONAL_NONNUMERIC_NONCLAIM")
    numeric = float(prediction)
    ratio = abs(numeric) / bound if bound else math.inf
    result = "PASS_NUMERIC_NONCLAIM" if abs(numeric) <= bound else "FAIL_BOUND"
    expected = {
        "CZB3281_5_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "CZB3281_6_twice_bound_smoke": "FAIL_BOUND",
    }.get(str(row["row_id"]), result)
    return (fmt(ratio), bool_str(abs(numeric) <= bound), result, expected)


def runner_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in bound_rows():
        ratio, pass_bound, result, expected = runner_result(row)
        rows.append(
            {
                "row_id": row["row_id"],
                "C_Z_prediction": row["C_Z_prediction"],
                "C_Z_abs_bound": row["C_Z_abs_bound"],
                "prediction_over_bound": ratio,
                "pass_bound": pass_bound,
                "result": result,
                "expected": expected,
                "expectation_met": bool_str(result == expected),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    theorem = theorem_rows()
    runner = runner_rows()
    return [
        {
            "gate_id": "GATE3281_0_parent_piece_theorem",
            "gate": "parent curvature norm theorem stated",
            "passed": bool_str(any(row["theorem_id"] == "MKO3281_0_parent_curvature_norm" for row in theorem)),
            "claim_allowed": "false",
            "detail": "exact conditional parent piece exists but fixed norm is not parent-signed.",
        },
        {
            "gate_id": "GATE3281_1_no_extra_F2_signed",
            "gate": "no independent/hidden/radiative F_Q^2 counterterm signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "ordinary covariance/U1 do not forbid f_X F_Q^2; typed visible algebra remains unsigned.",
        },
        {
            "gate_id": "GATE3281_2_constant_lambda_split",
            "gate": "constant lambda is separated from local C_Z drift",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "constant alpha-value debt is not treated as local vertical residual.",
        },
        {
            "gate_id": "GATE3281_3_finite_CZ_bound_contract",
            "gate": "pure C_Z no-cancellation bound contract exists",
            "passed": bool_str(alpha_bound() > 0),
            "claim_allowed": "false",
            "detail": f"|C_Z| <= {fmt(alpha_bound())} only if C_J=0, C_R=0, and C_Z is the only alpha/EM slope.",
        },
        {
            "gate_id": "GATE3281_4_runner_expectations",
            "gate": "C_Z runner refuses missing rows and scores smoke rows",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "claim_allowed": "false",
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "gate_id": "GATE3281_5_no_claim",
            "gate": "no alpha/Maxwell/local-GR claim promoted",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3281 is a theorem-audit plus finite bound contract checkpoint.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3281_0_theorem_result",
            "decision": "Unique Maxwell kinetic owner is an exact conditional theorem, not yet a current MTS derivation.",
            "why_it_moves_forward": "the needed signatures are now minimal and explicit: fixed parent gauge norm plus no independent/hidden/radiative F_Q^2 target.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3281_1_counterterm_result",
            "decision": "The live C_Z failure is not vague: it is f_X(I_hid)F_Q^2 or radiative/readout re-entry.",
            "why_it_moves_forward": "future work can attack one operator slot rather than the whole alpha problem.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3281_2_constant_lambda_result",
            "decision": "A hidden-independent constant lambda_A is separated as alpha-value debt, not local drift.",
            "why_it_moves_forward": "this prevents over-penalizing MTS for not deriving the absolute value of alpha while still policing local variations.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3281_3_bound_result",
            "decision": "A finite pure-C_Z no-cancellation bound is now executable: |C_Z| <= 1.389797711495e-12 under signed C_J=C_R=0 side conditions.",
            "why_it_moves_forward": "if MTS later predicts a single hidden EM kinetic leak, it can be scored immediately without cancellation games.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3281_0_3282",
            "target_doc": "3282-Y5-R2FR-hidden-F2-coefficient-slot-ban-or-first-CZ-prediction-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3282_hidden_F2_coefficient_slot_ban_or_first_CZ_prediction_row.py",
            "objective": "Attack the remaining live C_Z slot directly: prove f_X(I_hid)F_Q^2/radiative F_Q^2 has no parent target via q-basic visible algebra or exact hidden shift, or source the first numeric C_Z prediction row for the pure-C_Z bound.",
            "guardrail": "Do not use compact U1, covariance, gauge invariance, or constant lambda_A as a no-drift proof; no claim unless hidden/radiative F2 target is forbidden or a numeric C_Z row is sourced and scored nonclaim.",
            "valid_for_claim": "false",
        }
    ]


def output_csvs_parse() -> bool:
    return all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    sources = source_register_rows()
    theorem = theorem_rows()
    split = lambda_split_rows()
    bounds = bound_rows()
    runner = runner_rows()
    gates = promotion_gate_rows()
    validations = [
        {
            "check_id": "VAL3281_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3281_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3281_2_outputs_parse",
            "check": "all 3281 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3281_3_exact_theorem_present",
            "check": "parent curvature norm and vertical zero theorem rows exist",
            "passed": bool_str(any(row["theorem_id"] == "MKO3281_0_parent_curvature_norm" for row in theorem) and any(row["theorem_id"] == "MKO3281_1_vertical_zero_chain_rule" for row in theorem)),
            "detail": "MKO3281_0;MKO3281_1",
        },
        {
            "check_id": "VAL3281_4_constant_lambda_split",
            "check": "constant lambda value debt is separated from C_Z drift",
            "passed": bool_str(any(row["split_id"] == "LS3281_1_constant_lambda" and row["status"] == "VALUE_DEBT_NOT_LOCAL_RESIDUAL" for row in split)),
            "detail": "LS3281_1_constant_lambda",
        },
        {
            "check_id": "VAL3281_5_pure_CZ_bound_positive",
            "check": "pure C_Z bound contract has positive numeric bound and remains nonclaim",
            "passed": bool_str(any(row["row_id"] == "CZB3281_0_pure_CZ_bound_contract" and float(row["C_Z_abs_bound"]) > 0 and row["valid_for_claim"] == "false" for row in bounds)),
            "detail": f"bound={fmt(alpha_bound())}",
        },
        {
            "check_id": "VAL3281_6_runner_expectations",
            "check": "C_Z runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3281_7_claim_gates_false",
            "check": "no 3281 gate allows alpha/Maxwell/local-GR claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3281_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3281_9_overall",
            "check": "3281 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3281_9_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(compact(str(row.get(col, "")), 180).replace("|", "\\|") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc() -> None:
    theorem = read_csv(OUTPUTS["theorem"])
    audit = read_csv(OUTPUTS["operator_audit"])
    split = read_csv(OUTPUTS["lambda_split"])
    bounds = read_csv(OUTPUTS["bound_rows"])
    runner = read_csv(OUTPUTS["runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 3281 - Unique Maxwell kinetic owner or C_Z finite bound row under AX1090

## Summary

3281 attacks `C_Z` directly. The clean theorem is real but conditional: if the visible Maxwell kinetic coefficient is only the parent curvature norm

`Z_Q = C_P <T_Q,T_Q>_P`,

with `C_P` and `<T_Q,T_Q>_P` fixed parent/representation data and no independent `F_Q^2` counterterm target, then `C_Z=L_v ln Z_Q=0` for vertical `v in ker(Dq)`.

The current corpus still does **not** sign the no-extra-`F_Q^2` slot. Ordinary covariance and visible U(1) allow `f_X(I_hid)F_Q^2`; compact U(1) fixes charge labels, not the continuous kinetic coefficient. But 3281 makes one useful split: a hidden-independent constant `lambda_A F_Q^2` is alpha-value debt, not local vertical drift. The real local `C_Z` danger is hidden/radiative/readout dependence.

## Maxwell Kinetic Owner Theorem Attempt
{md_table(theorem, ["theorem_id", "claim_piece", "proof_status", "missing_for_claim", "consequence"])}

## No-Extra-F2 Operator Audit
{md_table(audit, ["audit_id", "operator", "test", "result", "repair"])}

## Lambda / Hidden / Radiative Split
{md_table(split, ["split_id", "term", "vertical_slope", "alpha_value_effect", "status"])}

## C_Z Finite Bound Rows
{md_table(bounds, ["row_id", "case", "C_Z_prediction", "C_Z_abs_bound", "result", "valid_for_claim"])}

## C_Z Runner
{md_table(runner, ["row_id", "C_Z_prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(gates, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decisions, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_rows, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validation, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_key = {
        "sources": source_register_rows(),
        "theorem": theorem_rows(),
        "operator_audit": operator_audit_rows(),
        "lambda_split": lambda_split_rows(),
        "bound_rows": bound_rows(),
        "runner": runner_rows(),
        "promotion": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
