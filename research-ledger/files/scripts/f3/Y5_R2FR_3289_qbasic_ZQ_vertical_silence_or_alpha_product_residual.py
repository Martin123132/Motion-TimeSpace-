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

DOC = ROOT / "3289-Y5-R2FR-qbasic-ZQ-vertical-silence-or-alpha-product-residual-under-AX1090.md"

SRC_3288_DOC = ROOT / "3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md"
SRC_3288_NEXT = OUT / "P8_Y5_R2FR_3288_NEXT_TARGET.csv"
SRC_3288_ZQ = OUT / "P8_Y5_R2FR_3288_ZQ_IMPEDANCE_DECOMPOSITION.csv"
SRC_3288_LGR = OUT / "P8_Y5_R2FR_3288_LOCAL_GR_RELEVANCE_TABLE.csv"
SRC_3288_RUNNER = OUT / "P8_Y5_R2FR_3288_SPLIT_BOUND_RUNNER_NONCLAIM.csv"
SRC_3288_VALIDATION = OUT / "P8_Y5_BRR545_3288_VALIDATION.csv"
SRC_1050_DOC = ROOT / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
SRC_1051_DOC = ROOT / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"
SRC_1057_DOC = ROOT / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
SRC_1058_DOC = ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
SRC_1051_CLOCK_CHAIN = OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"
SRC_988_CLOCK_IMPORT = OUT / "P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3289_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3289_QBASIC_ZQ_THEOREM.csv",
    "pieces": OUT / "P8_Y5_R2FR_3289_ZQ_PIECE_VERTICAL_AUDIT.csv",
    "conditions": OUT / "P8_Y5_R2FR_3289_VERTICAL_SILENCE_CONDITION_VECTOR.csv",
    "products": OUT / "P8_Y5_R2FR_3289_ALPHA_ZQ_PRODUCT_RESIDUAL_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3289_ZQ_VERTICAL_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3289_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3289_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3289_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3289_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
DEFAULT_BOUND = 1.389797711495e-12


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 460) -> str:
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
            hits.append(f"L{idx}:{compact(line, 285)}")
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


def bound_from_3288() -> float:
    residual_path = OUT / "P8_Y5_R2FR_3288_FINITE_RESIDUAL_ROWS_NONCLAIM.csv"
    if not residual_path.exists():
        return DEFAULT_BOUND
    for row in read_csv(residual_path):
        if row.get("row_id") == "SPL3288_2_ZQ_drift_residual":
            try:
                return float(row["abs_bound"])
            except (KeyError, ValueError):
                return DEFAULT_BOUND
    return DEFAULT_BOUND


def best_clock_product_bound() -> tuple[str, str, str]:
    if not SRC_1051_CLOCK_CHAIN.exists():
        return ("MISSING_CLOCK_PRODUCT", "MISSING", "MISSING")
    best: dict[str, str] | None = None
    for row in read_csv(SRC_1051_CLOCK_CHAIN):
        try:
            value = float(row.get("product_bound_1sigma_yr_inv", "nan"))
        except ValueError:
            continue
        if not math.isfinite(value):
            continue
        if best is None or value < float(best["product_bound_1sigma_yr_inv"]):
            best = row
    if best is None:
        return ("MISSING_CLOCK_PRODUCT", "MISSING", "MISSING")
    return (
        best.get("clock_pair", "UNKNOWN"),
        best.get("product_bound_1sigma_yr_inv", "MISSING"),
        best.get("product_bound_2sigma_yr_inv", "MISSING"),
    )


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3288_DOC, "3288 handoff", ["L_v Z_Q", "calibrated constants"]),
        (SRC_3288_NEXT, "3288 next target", ["L_v Z_Q=0", "alpha/Z_Q"]),
        (SRC_3288_ZQ, "Z_Q piece split", ["Z_Q = C_P", "f_X"]),
        (SRC_3288_LGR, "local GR fair standard", ["empirical G", "L_v Z_Q"]),
        (SRC_3288_RUNNER, "3288 residual runner", ["ZQ_drift", "REFUSE"]),
        (SRC_3288_VALIDATION, "3288 validation", ["VAL3288_11_overall", "true"]),
        (SRC_1057_DOC, "unique Maxwell subblock/no-extra-F2", ["lambda_A", "f(Xhat)F_Q^2"]),
        (SRC_1058_DOC, "operator-domain exhaustion/counterterm prior", ["Z_A", "counterterm"]),
        (SRC_1100_DOC, "T_Q/gauge-norm signature and Z_A decomposition", ["Z_A", "radiative"]),
        (SRC_1050_DOC, "visible-hidden product functor", ["product functor", "f_X"]),
        (SRC_1051_DOC, "no-mixed morphism and alpha product chain", ["b_alpha", "clock product"]),
        (SRC_1051_CLOCK_CHAIN, "source-backed b_alpha clock product chain", ["BAP1051_2_best_current_product", "2.1e-18"]),
        (SRC_988_CLOCK_IMPORT, "raw imported clock product rows", ["YbE3E2", "2.1e-18"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3289_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "QZ3289_0_decomposition",
            "claim_piece": "separate calibrated constants from drift",
            "statement": "Write Z_Q = Z_cal + Z_drift with Z_cal=C_P N_Q + lambda_A0 and Z_drift=f_X(I_hid)+delta_lambda_rad+delta_readout.",
            "derivation": "3288 already split parent, constant, hidden, radiative, and readout pieces; 3289 promotes that split to the vertical derivative test.",
            "status": "EXACT_DECOMPOSITION_CONTRACT",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QZ3289_1_vertical_derivative",
            "claim_piece": "q-basic Z_Q condition",
            "statement": "L_v ln Z_Q = Z_Q^{-1}[L_v(C_P N_Q)+L_v lambda_A0+L_v f_X+L_v delta_lambda_rad+L_v delta_readout].",
            "derivation": "direct chain rule; constant calibrated pieces have zero vertical derivative, while hidden/radiative/readout pieces must be zeroed or bounded.",
            "status": "EXACT_CHAIN_RULE_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QZ3289_2_constant_allowed",
            "claim_piece": "calibrated constant is not a local-GR failure",
            "statement": "A universal constant lambda_A0 can change the calibrated value of Z_Q without creating L_v Z_Q, so it weakens alpha prediction but does not by itself violate local Maxwell/GR reduction.",
            "derivation": "L_v lambda_A0=0; this parallels empirical G in GR and preserves the 3288 fair standard.",
            "status": "DERIVED_FAIR_STANDARD",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QZ3289_3_no_cancellation",
            "claim_piece": "no cancellation proof discipline",
            "statement": "L_v Z_Q=0 is claim-grade only if each nonparent drift channel is absent, q-basic, or independently bounded; cancellation between unrelated hidden/radiative/readout pieces is not a theorem.",
            "derivation": "without shared parent owner, cancellations are unstable under domain/readout/data splits and would smuggle closure assumptions.",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QZ3289_4_alpha_relation",
            "claim_piece": "relation to measured alpha branch",
            "statement": "In the selected readout convention alpha_EM proportional 1/(hbar c Z_Q), so b_alpha = L_v ln alpha_EM = -L_v ln Z_Q - L_v ln(hbar c) plus readout convention terms.",
            "derivation": "if hbar c/readout is q-basic, alpha vertical drift is exactly the negative Z_Q vertical drift; otherwise readout belongs in delta_readout.",
            "status": "EXACT_CONDITIONAL_READOUT_RELATION",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QZ3289_5_current_verdict",
            "claim_piece": "current proof status",
            "statement": "The current corpus does not prove L_v Z_Q=0 because hidden scalar, radiative/readout, no-extra-F2, and gauge-norm owner clauses remain unsigned; the clock product branch remains the strongest sourced nonclaim residual.",
            "derivation": "1057/1058/1100 retain legal counterterms; 1051 supplies source-backed b_alpha*tau_clock products but not standalone b_alpha.",
            "status": "NOT_PROMOTED_RETAIN_PRODUCT_RESIDUAL",
            "valid_for_claim": "false",
        },
    ]


def piece_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece_id": "ZQP3289_0_parent_norm",
            "piece": "C_P N_Q",
            "vertical_derivative": "L_v(C_P N_Q)",
            "zero_condition": "C_P and N_Q are parent-fixed/q-basic",
            "current_status": "CONDITIONAL_UNSIGNED",
            "local_limit_effect": "acceptable calibrated universal coupling if silent",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "ZQP3289_1_constant_lambda",
            "piece": "lambda_A0",
            "vertical_derivative": "0 if constant and universal",
            "zero_condition": "lambda_A0 is fixed before readout and source/species blind",
            "current_status": "ALLOWED_NOT_PREDICTIVE",
            "local_limit_effect": "not fatal to local Maxwell/GR, but blocks derived alpha value",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "ZQP3289_2_hidden_scalar",
            "piece": "f_X(I_hid)",
            "vertical_derivative": "f_X'(I_hid) L_v I_hid",
            "zero_condition": "hidden invariant absent, f_X constant, or product/no-mixed functor forbids the coefficient",
            "current_status": "LIVE_DANGEROUS_RESIDUAL",
            "local_limit_effect": "opens alpha/source fifth-force and clock pressure",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "ZQP3289_3_radiative",
            "piece": "delta_lambda_rad(mu,I_hid)",
            "vertical_derivative": "L_v delta_lambda_rad",
            "zero_condition": "radiative/effective action remains in the parent-generated q-basic operator algebra",
            "current_status": "UNSIGNED_READOUT_EFT_CLOSURE",
            "local_limit_effect": "tree-level silence can fail after thresholds/loops",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "ZQP3289_4_readout",
            "piece": "delta_readout from Hodge/hbar*c/spectroscopy convention",
            "vertical_derivative": "L_v delta_readout",
            "zero_condition": "observed readout functor and hbar*c/Hodge conventions are q-basic or fixed representation data",
            "current_status": "UNSIGNED_READOUT_FUNCTOR",
            "local_limit_effect": "measured alpha drift can appear even if abstract gauge norm is silent",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "ZQP3289_5_source_current",
            "piece": "source/current normalization linked to Z_Q",
            "vertical_derivative": "L_v source alpha charge or current weight",
            "zero_condition": "same T_Q/current owner and source-label forgetting are parent-signed",
            "current_status": "UNSIGNED_SOURCE_UNIVERSALITY",
            "local_limit_effect": "WEP/R10 source-charge residual can survive even if Z_Q is constant",
            "valid_for_claim": "false",
        },
    ]


def condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "ZQC3289_0_value_not_required",
            "condition": "Do not require numerical alpha/Z_Q derivation for first local GR/Maxwell reduction",
            "why": "a calibrated universal constant is acceptable at the GR-like stage",
            "current_status": "ADOPT_AS_FAIR_STANDARD",
            "claim_effect": "keeps route alive without pretending alpha value is predicted",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "ZQC3289_1_vertical_silence_required",
            "condition": "Require L_v Z_Q=0 or explicit bounded residual",
            "why": "hidden/environment drift creates local fifth-force/clock/WEP pressure",
            "current_status": "THEOREM_SHAPE_DERIVED_NOT_SIGNED",
            "claim_effect": "blocks local claim until drift channels are closed or bounded",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "ZQC3289_2_universality_required",
            "condition": "Require source/species/readout universality, not only constant lab alpha",
            "why": "source/test charge weights can violate WEP/R10 even with constant Z_Q",
            "current_status": "UNSIGNED_SOURCE_CURRENT_OWNER",
            "claim_effect": "keeps beta_source_alpha and WEP/R10 projections live",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "ZQC3289_3_no_cancellation_required",
            "condition": "Each nonparent drift term must be zero or bounded separately",
            "why": "cancellation between unrelated sectors is not robust or derived",
            "current_status": "GUARD_ACTIVE",
            "claim_effect": "prevents smuggled closure",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "ZQC3289_4_product_residual_allowed",
            "condition": "If L_v Z_Q is not derived zero, retain product constraints such as b_alpha*tau_clock",
            "why": "current evidence has source-backed products but no standalone b_alpha/tau separation",
            "current_status": "SOURCE_BACKED_NONCLAIM_PRODUCT_AVAILABLE",
            "claim_effect": "keeps empirical pressure without overstating it",
            "valid_for_claim": "false",
        },
    ]


def product_rows(bound: float) -> list[dict[str, Any]]:
    clock_pair, bound_1sigma, bound_2sigma = best_clock_product_bound()
    return [
        {
            "row_id": "AZQ3289_0_qbasic_ZQ_zero_conditional",
            "observable_or_gate": "local Maxwell/GR Z_Q vertical silence",
            "prediction": "0",
            "abs_bound": fmt(bound),
            "source_status": "THEOREM_CONDITIONAL_IF_PIECEWISE_SILENCE_SIGNED",
            "result": "PASS_NUMERIC_NONCLAIM",
            "missing_for_claim": "parent C_P N_Q owner; no hidden f_X; radiative/readout closure; source/current universality",
            "valid_for_claim": "false",
        },
        {
            "row_id": "AZQ3289_1_constant_calibrated_lambda",
            "observable_or_gate": "constant universal lambda_A0",
            "prediction": "0 vertical drift, value unpredicted",
            "abs_bound": fmt(bound),
            "source_status": "ALLOWED_CALIBRATED_CONSTANT_NONPREDICTIVE",
            "result": "PASS_VERTICAL_SILENCE_NONCLAIM_VALUE_NOT_PREDICTED",
            "missing_for_claim": "numerical alpha prediction or parent origin of lambda_A0",
            "valid_for_claim": "false",
        },
        {
            "row_id": "AZQ3289_2_hidden_ZQ_drift",
            "observable_or_gate": "hidden scalar alpha/Z_Q drift",
            "prediction": "Z_Q^{-1} L_v f_X(I_hid)",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_HIDDEN_DRIFT_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "source-backed f_X derivative, hidden state normalization, and arena projection",
            "valid_for_claim": "false",
        },
        {
            "row_id": "AZQ3289_3_radiative_readout_ZQ_drift",
            "observable_or_gate": "radiative/readout alpha/Z_Q drift",
            "prediction": "Z_Q^{-1} L_v(delta_lambda_rad + delta_readout)",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_RADIOUT_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "effective-action/readout closure or source-backed residual projection",
            "valid_for_claim": "false",
        },
        {
            "row_id": "AZQ3289_4_best_clock_product",
            "observable_or_gate": f"clock product: {clock_pair}",
            "prediction": f"|b_alpha*tau_clock_time| <= {bound_1sigma} yr^-1 at 1sigma; {bound_2sigma} yr^-1 at 2sigma",
            "abs_bound": bound_1sigma,
            "source_status": "SOURCE_BACKED_PRODUCT_NONCLAIM",
            "result": "PRODUCT_BOUND_AVAILABLE_STANDALONE_BLOCKED",
            "missing_for_claim": "tau_clock_time from MTS, Xhat/Z_Q normalization, and separation from other constants",
            "valid_for_claim": "false",
        },
        {
            "row_id": "AZQ3289_5_WEP_R10_projection_placeholder",
            "observable_or_gate": "WEP/R10 alpha/source projection",
            "prediction": "beta_source_alpha*b_alpha*tau_arena or K_X beta_s beta_t",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_SOURCE_TEST_ALPHA_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "beta_source_alpha, tau_WEP/tau_R10, lambda_X, source/test charge vectors, promoted bound curve",
            "valid_for_claim": "false",
        },
        {
            "row_id": "AZQ3289_6_half_bound_smoke",
            "observable_or_gate": "numeric smoke inside envelope",
            "prediction": fmt(0.5 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "missing_for_claim": "none; schema test only",
            "valid_for_claim": "false",
        },
        {
            "row_id": "AZQ3289_7_twice_bound_smoke",
            "observable_or_gate": "numeric smoke outside envelope",
            "prediction": fmt(2.0 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "missing_for_claim": "none; schema test only",
            "valid_for_claim": "false",
        },
    ]


def is_number(text: str) -> bool:
    try:
        value = float(text)
    except ValueError:
        return False
    return math.isfinite(value)


def runner_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = {
        "AZQ3289_0_qbasic_ZQ_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "AZQ3289_1_constant_calibrated_lambda": "PASS_VERTICAL_SILENCE_NONCLAIM_VALUE_NOT_PREDICTED",
        "AZQ3289_2_hidden_ZQ_drift": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "AZQ3289_3_radiative_readout_ZQ_drift": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "AZQ3289_4_best_clock_product": "PRODUCT_BOUND_AVAILABLE_STANDALONE_BLOCKED",
        "AZQ3289_5_WEP_R10_projection_placeholder": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "AZQ3289_6_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "AZQ3289_7_twice_bound_smoke": "FAIL_BOUND",
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        prediction = str(row["prediction"])
        source_status = str(row["source_status"])
        if row["row_id"] == "AZQ3289_1_constant_calibrated_lambda":
            result = "PASS_VERTICAL_SILENCE_NONCLAIM_VALUE_NOT_PREDICTED"
            ratio = "N/A"
        elif source_status == "SOURCE_BACKED_PRODUCT_NONCLAIM":
            result = "PRODUCT_BOUND_AVAILABLE_STANDALONE_BLOCKED"
            ratio = "N/A"
        elif source_status.startswith("MISSING"):
            result = "REFUSE_MISSING_SOURCE_NONCLAIM"
            ratio = "N/A"
        elif is_number(prediction):
            bound = float(row["abs_bound"])
            value = abs(float(prediction))
            ratio = fmt(value / bound)
            result = "PASS_NUMERIC_NONCLAIM" if value <= bound else "FAIL_BOUND"
        else:
            result = "SYMBOLIC_NONNUMERIC_NONCLAIM"
            ratio = "N/A"
        output.append(
            {
                "row_id": row["row_id"],
                "prediction": prediction,
                "prediction_over_bound": ratio,
                "result": result,
                "expected_result": expected[row["row_id"]],
                "expectation_met": bool_str(result == expected[row["row_id"]]),
                "valid_for_claim": "false",
            }
        )
    return output


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3289_0_chain_rule_ZQ",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "L_v ln Z_Q decomposition is explicit and separates calibrated constants from drift.",
        },
        {
            "gate_id": "GATE3289_1_constant_value_allowed",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "constant universal lambda_A0 is allowed as calibrated value, not alpha prediction.",
        },
        {
            "gate_id": "GATE3289_2_piecewise_silence_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "hidden f_X, radiative/readout, no-extra-F2, gauge norm, and source/current universality are not all signed.",
        },
        {
            "gate_id": "GATE3289_3_no_cancellation",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "cancellation between unrelated Z_Q pieces is forbidden as proof.",
        },
        {
            "gate_id": "GATE3289_4_product_residual_ready",
            "passed": "true_nonclaim_only",
            "claim_allowed": "false",
            "detail": "clock b_alpha*tau_clock product is source-backed but standalone b_alpha and arena transfers remain blocked.",
        },
        {
            "gate_id": "GATE3289_5_no_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "no local-GR/Maxwell/alpha/WEP/R10/clock claim is allowed from 3289.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3289_0_actual_progress",
            "decision": "The coupling bottleneck is now L_v Z_Q and universality, not immediate alpha-value prediction.",
            "why_it_moves_forward": "this makes the local GR/Maxwell reduction fairer and sharper: calibrated constants are allowed, hidden drift is not.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3289_1_current_failure",
            "decision": "The current corpus does not prove q-basic Z_Q.",
            "why_it_moves_forward": "the exact remaining blockers are hidden scalar coefficients, radiative/readout closure, no-extra-F2, gauge norm, and source/current universality.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3289_2_empirical_fallback",
            "decision": "Retain source-backed alpha clock product bounds as nonclaim residual pressure.",
            "why_it_moves_forward": "we keep data contact without pretending a standalone b_alpha or WEP/R10 alpha prediction exists.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3289_3_next_work",
            "decision": "Next best route is source/current universality or no-hidden-visible coefficient morphism, with q-basic Z_Q as the target.",
            "why_it_moves_forward": "constant lambda can be tolerated; the dangerous pieces are hidden/source/readout drift.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3289_0_3290",
            "target_doc": "3290-Y5-R2FR-no-hidden-ZQ-coefficient-or-source-current-universality-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3290_no_hidden_ZQ_coefficient_or_source_current_universality.py",
            "objective": "Attack the dangerous nonconstant pieces of Z_Q: prove hidden-to-visible Z_Q coefficient morphisms are absent/constant and source-current alpha weights are universal, or retain separate hidden-Z_Q and beta_source_alpha residual rows.",
            "guardrail": "Do not demand numerical alpha prediction; do not allow cancellation, species/source dependence, hidden f_X drift, radiative/readout leakage, or transfer of clock product bounds to WEP/R10 without projection maps.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    pieces: list[dict[str, Any]],
    conditions: list[dict[str, Any]],
    products: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    non_validation_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(fw_before, snapshot_tree(FW))
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": compact(detail, 680),
            }
        )

    add("VAL3289_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3289_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add(
        "VAL3289_2_outputs_parse",
        "all 3289 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3289_3_chain_rule_theorem_present",
        "theorem includes L_v ln Z_Q decomposition",
        any("L_v ln Z_Q" in row["statement"] and "L_v f_X" in row["statement"] for row in theorem),
    )
    add(
        "VAL3289_4_constant_not_fatal_present",
        "constant calibrated lambda is allowed but nonpredictive",
        any(row["theorem_id"] == "QZ3289_2_constant_allowed" and "not by itself violate" in row["statement"] for row in theorem)
        and any(row["piece_id"] == "ZQP3289_1_constant_lambda" and "not fatal" in row["local_limit_effect"] for row in pieces),
    )
    add(
        "VAL3289_5_danger_pieces_present",
        "hidden, radiative, readout, and source/current danger pieces are represented",
        all(piece_id in {row["piece_id"] for row in pieces} for piece_id in ["ZQP3289_2_hidden_scalar", "ZQP3289_3_radiative", "ZQP3289_4_readout", "ZQP3289_5_source_current"]),
    )
    add(
        "VAL3289_6_no_cancellation_guard_present",
        "no-cancellation discipline is explicit",
        any(row["theorem_id"] == "QZ3289_3_no_cancellation" for row in theorem)
        and any(row["condition_id"] == "ZQC3289_3_no_cancellation_required" for row in conditions),
    )
    add(
        "VAL3289_7_product_residual_present",
        "source-backed clock product is retained but standalone blocked",
        any(
            row["source_status"] == "SOURCE_BACKED_PRODUCT_NONCLAIM"
            and row["result"] == "PRODUCT_BOUND_AVAILABLE_STANDALONE_BLOCKED"
            and "tau_clock_time" in row["missing_for_claim"]
            for row in products
        ),
    )
    add(
        "VAL3289_8_runner_expectations",
        "Z_Q vertical runner expectations all match",
        all(row["expectation_met"] == "true" for row in runner),
        ";".join(f"{row['row_id']}={row['result']}" for row in runner),
    )
    add(
        "VAL3289_9_claim_gates_false",
        "no 3289 gate allows local-GR/alpha/Maxwell/WEP/R10 claim",
        all(row["claim_allowed"] == "false" for row in promotion)
        and all(row["valid_for_claim"] == "false" for row in products),
    )
    add(
        "VAL3289_10_next_target_focused",
        "next target focuses hidden Z_Q coefficient and source-current universality",
        any("no-hidden-ZQ" in row["target_doc"] and "source-current" in row["target_doc"] for row in next_target),
    )
    add(
        "VAL3289_11_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3289_12_overall",
        "3289 validation overall",
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
    pieces: list[dict[str, Any]],
    conditions: list[dict[str, Any]],
    products: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3289 - q-basic Z_Q vertical silence or alpha product residual under AX1090

## Summary

3289 attacks the coupling throat directly.

The fair local-GR/Maxwell standard is:

- MTS does **not** need to derive the exact numerical value of `alpha_EM` or `Z_Q` at the first local-limit stage.
- MTS **does** need `Z_Q` to be universal and vertical-silent: `L_v Z_Q=0`, with no hidden/source/radiative/readout drift.

The exact split is:

`Z_Q = Z_cal + Z_drift`

with

`Z_cal = C_P N_Q + lambda_A0`

and

`Z_drift = f_X(I_hid) + delta_lambda_rad + delta_readout`.

Then

`L_v ln Z_Q = Z_Q^-1 [L_v(C_P N_Q) + L_v lambda_A0 + L_v f_X + L_v delta_lambda_rad + L_v delta_readout]`.

Constant calibrated pieces such as `lambda_A0` can be tolerated like empirical `G` in GR: they weaken prediction of the value but do not create fifth-force/clock/WEP drift. The dangerous pieces are nonconstant hidden coefficients, source/current nonuniversality, radiative threshold terms, and readout terms.

Current verdict: `L_v Z_Q=0` is **not** proved in the corpus. The best empirical fallback remains source-backed product pressure, especially the clock product `|b_alpha tau_clock_time| <= 2.1e-18 yr^-1`, but standalone `b_alpha` and WEP/R10 transfer remain blocked.

Selected residual envelope remains:

`|residual| <= {fmt(bound)}`.

## q-Basic Z_Q Theorem
{md_table(theorem, ["theorem_id", "claim_piece", "status", "statement"])}

## Z_Q Piece Vertical Audit
{md_table(pieces, ["piece_id", "piece", "vertical_derivative", "zero_condition", "current_status", "local_limit_effect"])}

## Vertical Silence Condition Vector
{md_table(conditions, ["condition_id", "condition", "current_status", "claim_effect"])}

## Alpha/Z_Q Product Residual Rows
{md_table(products, ["row_id", "observable_or_gate", "prediction", "source_status", "result", "valid_for_claim"])}

## Z_Q Vertical Runner
{md_table(runner, ["row_id", "prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

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
    bound = bound_from_3288()
    sources = source_register_rows()
    theorem = theorem_rows()
    pieces = piece_rows()
    conditions = condition_rows()
    products = product_rows(bound)
    runner = runner_rows(products)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["pieces"], pieces)
    write_csv(OUTPUTS["conditions"], conditions)
    write_csv(OUTPUTS["products"], products)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, theorem, pieces, conditions, products, runner, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(bound, theorem, pieces, conditions, products, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
