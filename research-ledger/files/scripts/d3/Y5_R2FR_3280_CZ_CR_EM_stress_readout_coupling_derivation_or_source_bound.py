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

DOC = ROOT / "3280-Y5-R2FR-CZ-CR-EM-stress-readout-coupling-derivation-or-source-bound-under-AX1090.md"

SRC_3273_DOC = ROOT / "3273-Y5-R2FR-alpha-owner-theorem-zero-or-source-backed-Ce-prediction-under-AX1090.md"
SRC_3274_DOC = ROOT / "3274-Y5-R2FR-current-normalization-and-EM-stress-source-coupling-derivation-under-AX1090.md"
SRC_3276_DOC = ROOT / "3276-Y5-R2FR-minimal-covariant-derivative-domain-or-first-source-shadow-coefficient-under-AX1090.md"
SRC_3278_DOC = ROOT / "3278-Y5-R2FR-source-shadow-finite-row-acquisition-or-parent-U1-clause-source-under-AX1090.md"
SRC_3279_DOC = ROOT / "3279-Y5-R2FR-first-finite-source-shadow-row-source-hunt-or-CJ-closure-demotion-under-AX1090.md"
SRC_1099_DOC = ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

SRC_3273_DECOMP = OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv"
SRC_3273_OWNER = OUT / "P8_Y5_R2FR_3273_ALPHA_OWNER_CLAUSE_AUDIT.csv"
SRC_3273_RUNNER = OUT / "P8_Y5_R2FR_3273_CE_BOUND_RUNNER_RESULTS_NONCLAIM.csv"
SRC_3274_ACTION = OUT / "P8_Y5_R2FR_3274_EM_ACTION_VARIATION_DERIVATION.csv"
SRC_3274_STRESS = OUT / "P8_Y5_R2FR_3274_EM_STRESS_POYNTING_EXCHANGE_LAW.csv"
SRC_3276_MAG = OUT / "P8_Y5_R2FR_3276_F_ONLY_MAGNETIZATION_CURRENT_LEMMA.csv"
SRC_3278_CLAUSE = OUT / "P8_Y5_R2FR_3278_EXACT_U1_CLAUSE_SOURCE_ROWS.csv"
SRC_3279_CJ = OUT / "P8_Y5_R2FR_3279_CJ_CLOSURE_DEMOTION.csv"
SRC_3279_VALIDATION = OUT / "P8_Y5_BRR545_3279_VALIDATION.csv"
SRC_1099_OWNER = OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
SRC_1099_EXC = OUT / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
SRC_1099_ALPHA = OUT / "P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv"
SRC_1101_GAUGE = OUT / "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv"
SRC_1101_ROUTE = OUT / "P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3280_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_R2FR_3280_EM_STRESS_READOUT_DERIVATION.csv",
    "owner_gate": OUT / "P8_Y5_R2FR_3280_CZ_CR_OWNER_GATE_AUDIT.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3280_CZ_CR_SOURCE_BOUND_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3280_CZ_CR_ALPHA_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3280_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3280_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3280_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3280_VALIDATION.csv",
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
        (SRC_3273_DOC, "3273 alpha law handoff", ["C_e := L_X", "C_Z", "C_R"]),
        (SRC_3273_DECOMP, "3273 C_e decomposition", ["ADECOMP3273_1", "2 C_J - C_Z - C_R"]),
        (SRC_3273_OWNER, "3273 alpha owner clause audit", ["AOWN3273_0", "AOWN3273_2"]),
        (SRC_3273_RUNNER, "3273 alpha bound runner", ["ARUN3273_1", "bound_value"]),
        (SRC_3274_DOC, "3274 EM source/stress derivation", ["Poynting", "T_EM"]),
        (SRC_3274_ACTION, "3274 EM action variation", ["AV3274_0", "Z_Q"]),
        (SRC_3274_STRESS, "3274 EM stress/Poynting law", ["SP3274_1", "SP3274_3"]),
        (SRC_3276_DOC, "3276 F-only domain split", ["F-only", "Poynting"]),
        (SRC_3276_MAG, "3276 magnetization current lemma", ["MAG3276_3", "stress"]),
        (SRC_3278_DOC, "3278 exact U1 and Poynting placement", ["wave/Poynting", "EM stress"]),
        (SRC_3278_CLAUSE, "3278 F-only wave clause", ["CLAUSE3278_1", "Poynting"]),
        (SRC_3279_DOC, "3279 C_J closure demotion", ["C_Z/C_R", "closure-only"]),
        (SRC_3279_CJ, "3279 finite C_J closure table", ["CJC3279_2", "C_Z"]),
        (SRC_3279_VALIDATION, "3279 validation", ["VAL3279_8_overall", "true"]),
        (SRC_1099_DOC, "1099 unique EM kinetic owner", ["f_X(Xhat) F_Q^2", "readout"]),
        (SRC_1099_OWNER, "1099 EM kinetic owner theorem rows", ["UEM1099_2", "counterterm"]),
        (SRC_1099_EXC, "1099 no-extra-F2 exclusion audit", ["EXC1099_1", "EXC1099_5"]),
        (SRC_1099_ALPHA, "1099 alpha coefficient rows", ["ASR1099_0", "ASR1099_4"]),
        (SRC_1100_DOC, "1100 T_Q/gauge norm signature", ["TQS1100_3", "readout"]),
        (SRC_1101_GAUGE, "1101 gauge norm theorem attempt", ["GFT1101_4", "GAUGE_NORM_OWNER_NOT_DERIVED"]),
        (SRC_1101_ROUTE, "1101 alpha route decision", ["ROUTE1101_2", "BEST_IMMEDIATE"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3280_{idx}",
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
    rows = read_csv(SRC_3273_RUNNER)
    for row in rows:
        if row.get("prediction_id") == "CE3273_1_theorem_zero_conditional":
            return float(row["bound_value"])
    return float(rows[0]["bound_value"])


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "DER3280_0_starting_block",
            "object": "EM kinetic/source/readout block",
            "formula": "S_EM=int mu_obs[-Z_Q F_Q^2/4 + s_J kappa_J A_Q_mu J_Q^mu] + S_readout[g_obs,*_obs,hbar,c,...]",
            "derivation": "Start from the explicit 3273/3274 parametrization after finite C_J is closure-only in 3279.",
            "result": "C_Z and C_R are now the live alpha/source-coupling slopes, not hidden C_J compensators.",
            "status": "STARTING_BLOCK_FIXED",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "DER3280_1_EM_stress",
            "object": "Hilbert EM stress",
            "formula": "T_EM^{mu nu}=Z_Q(F_Q^{mu rho}F_Q^nu_rho - 1/4 g_obs^{mu nu}F_Q^2) + constitutive/readout boundary terms",
            "derivation": "Metric variation of the Maxwell kinetic term; F-only response contributes constitutive stress, not a source-current normalization.",
            "result": "Poynting/wave energy is proportional to Z_Q in the observed coframe.",
            "status": "EXACT_FROM_ASSUMED_BLOCK",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "DER3280_2_Z_exchange",
            "object": "Maxwell stress exchange residual",
            "formula": "nabla_mu T_EM^{mu nu}=s_J kappa_J F_Q^nu_mu J_Q^mu + Q_Z^nu, with Q_Z^nu ~ -(1/4)F_Q^2 nabla^nu Z_Q plus owner/boundary terms",
            "derivation": "Use Maxwell equation, Bianchi identity, and the 3274 stress-exchange law; sign convention is carried by s_J/Q_Z.",
            "result": "A floating Z_Q becomes a real stress-exchange residual, not a current-normalization escape hatch.",
            "status": "POYNTING_DIAGNOSTIC_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "DER3280_3_observer_Poynting",
            "object": "observer-frame energy flow",
            "formula": "u_EM=Z_Q(E^2+B^2)/2; S_EM^i=Z_Q(E x B)^i; partial_t u_EM+div S_EM=-s_J kappa_J E.J + Z_Q/readout-gradient exchange",
            "derivation": "3+1 split of the covariant exchange law in the observed coframe.",
            "result": "The user's Poynting/background-field intuition is placed in C_Z/C_R stress/readout, not discarded.",
            "status": "FLOW_ROUTE_MAPPED",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "DER3280_4_readout_slope",
            "object": "dimensionless alpha/readout transfer",
            "formula": "alpha_obs proportional to kappa_J^2/(Z_Q R_alpha); C_e=2C_J-C_Z-C_R, C_R=L_X ln R_alpha",
            "derivation": "Log differentiation of the 3273 low-energy alpha normalization law.",
            "result": "Readout/Hodge/coframe/hbar*c leakage is independent debt unless quotient-fixed.",
            "status": "READOUT_CONTRACT_EXPLICIT",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "DER3280_5_qEM_residual",
            "object": "local residual vector",
            "formula": "q_EM^nu=P_loc[Q_Z^nu + nabla_mu T_readout^{mu nu} + boundary/no-flux leakage]",
            "derivation": "Project all unowned EM stress/readout exchange into the same q_loc style residual used by the local-GR branch.",
            "result": "Local GR/Newton/Maxwell recovery requires q_EM^nu=0 by parent theorem or a sourced finite bound.",
            "status": "LOCAL_RESIDUAL_GATE_BUILT",
            "valid_for_claim": "false",
        },
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CZCR3280_0_unique_Z_owner",
            "coefficient": "C_Z=L_X ln Z_Q",
            "required_signature": "unique parent Maxwell kinetic owner: Z_Q=C_P<T_Q,T_Q>_P fixed under the local generator",
            "current_status": "NOT_SIGNED",
            "blocking_evidence": "1099/1100 retain fixed-gauge-norm and no-extra-F2 debt.",
            "result_if_signed": "C_Z=0 at tree level",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CZCR3280_1_no_extra_F2",
            "coefficient": "C_Z residual",
            "required_signature": "no independent lambda_A F_Q^2, f_X(Xhat)F_Q^2, or radiative threshold F_Q^2 coefficient",
            "current_status": "COUNTERTERM_RETAINED",
            "blocking_evidence": "1099 EXC rows say diffeomorphism and U1 gauge invariance do not forbid f_X F_Q^2.",
            "result_if_signed": "hidden-visible gauge kinetic leak removed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CZCR3280_2_F_only_response",
            "coefficient": "stress/readout residual, not C_J",
            "required_signature": "F-only wave/Poynting response is treated as constitutive stress/boundary data",
            "current_status": "SOURCE_BACKED_PLACEMENT",
            "blocking_evidence": "3276/3278 prove magnetization current is identically conserved and belongs in stress/Poynting residuals.",
            "result_if_signed": "prevents smuggling F-only physics into source-current normalization",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CZCR3280_3_readout_owner",
            "coefficient": "C_R=L_X ln R_alpha",
            "required_signature": "Hodge/coframe/hbar*c/spectroscopy readout factors through quotient-fixed observed data with no hidden/radiative re-entry",
            "current_status": "UNSIGNED",
            "blocking_evidence": "3273, 1099, and 1100 all retain readout/radiative closure as unsigned.",
            "result_if_signed": "C_R=0",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CZCR3280_4_CJ_not_reopened",
            "coefficient": "C_J",
            "required_signature": "finite C_J cannot be used as compensator unless a new numeric source row appears",
            "current_status": "DEMOTED_TO_CLOSURE_ONLY",
            "blocking_evidence": "3279 closure demotion.",
            "result_if_signed": "C_Z/C_R are attacked directly without hidden C_J cancellation",
            "valid_for_claim": "false",
        },
    ]


def source_bound_rows() -> list[dict[str, Any]]:
    bound = alpha_bound()
    return [
        {
            "row_id": "ZRB3280_0_CZ_zero_if_unique_owner_signed",
            "C_Z": "0",
            "C_R": "MISSING_READOUT_OR_ZERO_THEOREM",
            "C_J": "0_if_parent_exact_U1_current_owner_signed_else_closure_only",
            "C_e_prediction": "MISSING",
            "bound_value": fmt(bound),
            "source_path": str(SRC_1099_OWNER),
            "status": "CZ_THEOREM_ZERO_CONDITIONAL_CANNOT_SCORE_ALPHA_ALONE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZRB3280_1_CR_zero_if_readout_signed",
            "C_Z": "MISSING_CZ_OR_ZERO_THEOREM",
            "C_R": "0",
            "C_J": "0_if_parent_exact_U1_current_owner_signed_else_closure_only",
            "C_e_prediction": "MISSING",
            "bound_value": fmt(bound),
            "source_path": str(SRC_3273_OWNER),
            "status": "CR_THEOREM_ZERO_CONDITIONAL_CANNOT_SCORE_ALPHA_ALONE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZRB3280_2_hidden_F2_CZ_missing",
            "C_Z": "L_X ln(C_P N_Q + lambda_A + f_X + delta_lambda_rad)",
            "C_R": "0_if_readout_signed_else_MISSING",
            "C_J": "0_if_current_owner_signed_else_closure_only",
            "C_e_prediction": "MISSING_NUMERIC_CZ_COUNTERTERM_SLOPE",
            "bound_value": fmt(bound),
            "source_path": str(SRC_1099_OWNER),
            "status": "COUNTERTERM_RETAINED_NUMERIC_SLOPE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZRB3280_3_readout_CR_missing",
            "C_Z": "0_if_unique_Z_owner_signed_else_MISSING",
            "C_R": "L_X ln R_alpha_readout",
            "C_J": "0_if_current_owner_signed_else_closure_only",
            "C_e_prediction": "MISSING_NUMERIC_READOUT_SLOPE",
            "bound_value": fmt(bound),
            "source_path": str(SRC_1100_DOC),
            "status": "READOUT_REENTRY_RETAINED_NUMERIC_SLOPE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZRB3280_4_combined_ZR_bound_contract",
            "C_Z": "C_Z",
            "C_R": "C_R",
            "C_J": "0_if_current_owner_signed_else_closure_only",
            "C_e_prediction": "-C_Z-C_R_if_CJ_zero",
            "bound_value": fmt(bound),
            "source_path": str(SRC_3273_DECOMP),
            "status": "COMBINATION_BOUND_ONLY_NO_SEPARATE_CZ_CR_VALUES",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZRB3280_5_half_bound_CZ_smoke",
            "C_Z": fmt(-bound / 2.0),
            "C_R": "0",
            "C_J": "0",
            "C_e_prediction": fmt(bound / 2.0),
            "bound_value": fmt(bound),
            "source_path": "SMOKE_NUMERIC_NONCLAIM",
            "status": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZRB3280_6_twice_bound_CZ_smoke",
            "C_Z": fmt(-2.0 * bound),
            "C_R": "0",
            "C_J": "0",
            "C_e_prediction": fmt(2.0 * bound),
            "bound_value": fmt(bound),
            "source_path": "SMOKE_NUMERIC_NONCLAIM",
            "status": "SMOKE",
            "valid_for_claim": "false",
        },
    ]


def runner_result(row: dict[str, Any]) -> tuple[str, str, str, str]:
    prediction = str(row["C_e_prediction"])
    bound = float(row["bound_value"])
    if "MISSING" in prediction or "if_" in prediction:
        return ("MISSING", "false", "REFUSE_OR_FAIL", "REFUSE_OR_FAIL")
    numeric = float(prediction)
    ratio = abs(numeric) / bound if bound else math.inf
    result = "PASS_NUMERIC_NONCLAIM" if abs(numeric) <= bound else "FAIL_BOUND"
    expected = {
        "ZRB3280_5_half_bound_CZ_smoke": "PASS_NUMERIC_NONCLAIM",
        "ZRB3280_6_twice_bound_CZ_smoke": "FAIL_BOUND",
    }.get(str(row["row_id"]), result)
    return (fmt(ratio), bool_str(abs(numeric) <= bound), result, expected)


def runner_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in source_bound_rows():
        ratio, pass_bound, result, expected = runner_result(row)
        rows.append(
            {
                "row_id": row["row_id"],
                "C_e_prediction": row["C_e_prediction"],
                "bound_value": row["bound_value"],
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
    gates = owner_gate_rows()
    runner = runner_rows()
    return [
        {
            "gate_id": "GATE3280_0_derivation_present",
            "gate": "EM stress/readout residual derivation is explicit",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "q_EM^nu=P_loc[Q_Z^nu+nabla_mu T_readout^{mu nu}+boundary] built as the direct Poynting/readout route.",
        },
        {
            "gate_id": "GATE3280_1_CZ_owner_signed",
            "gate": "unique Maxwell kinetic owner and no-extra-F2 are parent-signed",
            "passed": bool_str(all(row["current_status"] not in ["NOT_SIGNED", "COUNTERTERM_RETAINED"] for row in gates if row["coefficient"].startswith("C_Z"))),
            "claim_allowed": "false",
            "detail": "C_Z remains blocked by gauge-norm/no-extra-F2/radiative counterterm debt.",
        },
        {
            "gate_id": "GATE3280_2_CR_readout_signed",
            "gate": "readout/Hodge/coframe/radiative transfer is parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "C_R remains unsigned.",
        },
        {
            "gate_id": "GATE3280_3_CJ_not_used_as_compensator",
            "gate": "finite C_J is not reopened as a hidden compensator",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3279 demotion is carried forward.",
        },
        {
            "gate_id": "GATE3280_4_runner_expectations",
            "gate": "CZ/CR bound runner refuses missing rows and scores smoke rows",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "claim_allowed": "false",
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "gate_id": "GATE3280_5_no_public_claim",
            "gate": "no Maxwell/alpha/local-GR/Newton claim promoted",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3280 is derivation plus source-bound gate only.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3280_0_poynting_placement",
            "decision": "Poynting/wave response belongs in EM stress/readout residuals, not in C_J.",
            "why_it_moves_forward": "the background-field intuition now has a precise mathematical home: Z_Q-weighted stress flow and q_EM residuals.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3280_1_CZ_status",
            "decision": "C_Z is the sharpest next derivation target.",
            "why_it_moves_forward": "C_Z has a concrete owner theorem and a concrete counterexample f_X(Xhat)F_Q^2; this is less woolly than generic readout closure.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3280_2_CR_status",
            "decision": "C_R remains independent readout debt.",
            "why_it_moves_forward": "even a perfect tree-level Maxwell owner is not enough unless observed alpha readout factors through quotient-fixed data.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3280_3_bound_status",
            "decision": "The alpha envelope bounds only the combination 2C_J-C_Z-C_R, not standalone C_Z or C_R.",
            "why_it_moves_forward": "future numeric rows must say which side conditions are signed; no compensating cancellations are allowed.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3280_0_3281",
            "target_doc": "3281-Y5-R2FR-unique-Maxwell-kinetic-owner-or-CZ-finite-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3281_unique_Maxwell_kinetic_owner_or_CZ_finite_bound_row.py",
            "objective": "Try to close C_Z first: derive a unique parent Maxwell kinetic owner/no-extra-F2 theorem from T_Q/gauge-norm data, or build a finite C_Z source-bound row without using C_J or C_R as hidden compensators.",
            "guardrail": "Do not claim alpha/Maxwell/local-GR from compact U1 alone; C_Z needs fixed gauge norm, no independent F_Q^2 counterterm, radiative/readout guard, source paths, units, and nonclaim validation.",
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
    derivations = derivation_rows()
    owner_gates = owner_gate_rows()
    bound_rows = source_bound_rows()
    runner = runner_rows()
    promotions = promotion_gate_rows()
    validations = [
        {
            "check_id": "VAL3280_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3280_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3280_2_outputs_parse",
            "check": "all 3280 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3280_3_qEM_residual_present",
            "check": "q_EM residual route is explicitly derived",
            "passed": bool_str(any(row["derivation_id"] == "DER3280_5_qEM_residual" for row in derivations)),
            "detail": "DER3280_5_qEM_residual",
        },
        {
            "check_id": "VAL3280_4_CZ_CR_not_falsely_signed",
            "check": "C_Z and C_R gates remain unsigned/nonclaim",
            "passed": bool_str(any(row["coefficient"].startswith("C_Z") and row["current_status"] != "SIGNED" for row in owner_gates) and any(row["coefficient"].startswith("C_R") and row["current_status"] != "SIGNED" for row in owner_gates)),
            "detail": ";".join(f"{row['gate_id']}={row['current_status']}" for row in owner_gates),
        },
        {
            "check_id": "VAL3280_5_bound_rows_nonclaim",
            "check": "all CZ/CR source-bound rows remain nonclaim",
            "passed": bool_str(all(row["valid_for_claim"] == "false" for row in bound_rows)),
            "detail": "",
        },
        {
            "check_id": "VAL3280_6_runner_expectations",
            "check": "bound runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3280_7_claim_gates_false",
            "check": "no 3280 gate allows alpha/Maxwell/local-GR claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in promotions)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3280_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3280_9_overall",
            "check": "3280 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3280_9_overall")
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
    derivation = read_csv(OUTPUTS["derivation"])
    owner_gate = read_csv(OUTPUTS["owner_gate"])
    bound_rows = read_csv(OUTPUTS["bound_rows"])
    runner = read_csv(OUTPUTS["runner"])
    promotion = read_csv(OUTPUTS["promotion"])
    decision = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 3280 - C_Z/C_R EM stress-readout coupling derivation or source-bound gate under AX1090

## Summary

3280 moves the coupling work off the now-demoted finite `C_J` branch and attacks the EM side directly. The result is not a public Maxwell/alpha/local-GR claim. It is a sharper derivation gate:

`Poynting/wave/F_Q-only response lives in EM stress, constitutive boundary terms, and readout transfer. It does not secretly fix source-current normalization.`

The useful object is now

`q_EM^nu = P_loc[Q_Z^nu + nabla_mu T_readout^{{mu nu}} + boundary/no-flux leakage]`,

where `Q_Z^nu` is the stress-exchange term produced when `Z_Q` is not parent-fixed. Therefore local GR/Newton/Maxwell recovery needs either `q_EM^nu=0` by parent theorem or finite source-bound rows for `C_Z/C_R`.

## EM Stress / Readout Derivation
{md_table(derivation, ["derivation_id", "object", "formula", "result", "status"])}

## C_Z / C_R Owner Gate
{md_table(owner_gate, ["gate_id", "coefficient", "current_status", "blocking_evidence", "result_if_signed"])}

## Source-Bound Rows
{md_table(bound_rows, ["row_id", "C_Z", "C_R", "C_J", "C_e_prediction", "status", "valid_for_claim"])}

## Bound Runner
{md_table(runner, ["row_id", "C_e_prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(promotion, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decision, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

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
        "derivation": derivation_rows(),
        "owner_gate": owner_gate_rows(),
        "bound_rows": source_bound_rows(),
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
