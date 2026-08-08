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

DOC = ROOT / "3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md"

SRC_3287_DOC = ROOT / "3287-Y5-R2FR-chi-to-metric-Hodge-premise-proof-or-DeltaChi-slope-source-row-under-AX1090.md"
SRC_3287_NEXT = OUT / "P8_Y5_R2FR_3287_NEXT_TARGET.csv"
SRC_3287_RECON = OUT / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv"
SRC_3287_RESID = OUT / "P8_Y5_R2FR_3287_DELTA_CHI_RESIDUAL_DECOMPOSITION.csv"
SRC_3287_DECISION = OUT / "P8_Y5_R2FR_3287_DECISION_LEDGER.csv"
SRC_3287_VALIDATION = OUT / "P8_Y5_BRR545_3287_VALIDATION.csv"
SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_1012_DOC = ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"
SRC_1016_DOC = ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
SRC_1057_DOC = ROOT / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
SRC_1058_DOC = ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3288_SOURCE_REGISTER.csv",
    "metric": OUT / "P8_Y5_R2FR_3288_METRIC_IDENTIFICATION_SPLIT.csv",
    "zq": OUT / "P8_Y5_R2FR_3288_ZQ_IMPEDANCE_DECOMPOSITION.csv",
    "gr": OUT / "P8_Y5_R2FR_3288_LOCAL_GR_RELEVANCE_TABLE.csv",
    "residual": OUT / "P8_Y5_R2FR_3288_FINITE_RESIDUAL_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3288_SPLIT_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3288_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3288_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3288_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3288_VALIDATION.csv",
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


def bound_from_3287() -> float:
    slope_path = OUT / "P8_Y5_R2FR_3287_DELTA_CHI_SLOPE_ROWS_NONCLAIM.csv"
    if not slope_path.exists():
        return DEFAULT_BOUND
    for row in read_csv(slope_path):
        if row.get("row_id") == "DCS3287_2_impedance_metric_readout_residual":
            try:
                return float(row["abs_bound"])
            except (KeyError, ValueError):
                return DEFAULT_BOUND
    return DEFAULT_BOUND


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3287_DOC, "3287 handoff", ["Z_Q", "g_EM"]),
        (SRC_3287_NEXT, "3287 next target", ["same-public-metric", "ZQ"]),
        (SRC_3287_RECON, "Hodge reconstruction theorem", ["g_EM", "Z_Q"]),
        (SRC_3287_RESID, "Delta chi residual split", ["Delta_Z_Q", "metric_split"]),
        (SRC_3287_DECISION, "coupling and same-metric decisions", ["coupling", "same metric"]),
        (SRC_3287_VALIDATION, "3287 validation", ["VAL3287_11_overall", "true"]),
        (SRC_1009_DOC, "parent current chain / same observed metric", ["same observed metric", "S_matter"]),
        (SRC_1012_DOC, "same-frame source normalization", ["same_frame", "one observed coframe"]),
        (SRC_1016_DOC, "worldtube/source coframe", ["single_observed_coframe", "coframe"]),
        (SRC_1057_DOC, "unique Maxwell subblock", ["no independent", "F_Q^2"]),
        (SRC_1058_DOC, "visible operator-domain exhaustion", ["Z_A", "operator-domain"]),
        (SRC_1100_DOC, "T_Q/gauge norm signature", ["g_EM", "radiative"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3288_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def metric_rows() -> list[dict[str, Any]]:
    return [
        {
            "metric_gate_id": "MGS3288_0_conformal_cone",
            "object": "EM cone metric",
            "statement": "3287 reconstructs only [g_EM] from nonbirefringent EM propagation; this is a conformal light-cone statement, not full matter metric ownership.",
            "theory_move": "separate cone equality from clock/rod scale equality",
            "status": "DERIVED_SPLIT",
            "valid_for_claim": "false",
        },
        {
            "metric_gate_id": "MGS3288_1_4D_Hodge_conformal_invariance",
            "object": "Hodge star on 2-forms",
            "statement": "In four spacetime dimensions, the Hodge star acting on 2-forms is conformally invariant, so EM Hodge data can match the public cone without fixing the clock/rod conformal scale.",
            "theory_move": "do not overclaim scale from EM alone",
            "status": "DERIVED_STANDARD_GEOMETRIC_FACT",
            "valid_for_claim": "false",
        },
        {
            "metric_gate_id": "MGS3288_2_public_metric_identity",
            "object": "same public metric",
            "statement": "To use EM stress in the local GR source equation, require [g_EM]=[g_pub] plus the matter/clock/source coframe e_obs fixes the representative scale used in S_matter, clocks, rods, and Hilbert stress.",
            "theory_move": "local GR needs one coframe, not merely a light cone",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "metric_gate_id": "MGS3288_3_bimetric_escape",
            "object": "metric split residual",
            "statement": "If [g_EM] differs from [g_pub] or the scale/coframe is not shared, the branch becomes an optical-metric/source-frame residual rather than a local-GR pass.",
            "theory_move": "route failure to finite residual instead of closure",
            "status": "LIVE_RESIDUAL_ROUTE",
            "valid_for_claim": "false",
        },
    ]


def zq_rows() -> list[dict[str, Any]]:
    return [
        {
            "zq_id": "ZQS3288_0_parent_piece",
            "piece": "C_P N_Q",
            "vertical_status": "q-basic if C_P and N_Q are parent-fixed",
            "local_GR_role": "acceptable calibrated coupling if universal and vertical-silent",
            "prediction_role": "does not by itself predict alpha value unless C_P,N_Q are derived numerically",
            "status": "CONDITIONAL_SUPPORT",
            "valid_for_claim": "false",
        },
        {
            "zq_id": "ZQS3288_1_constant_lambda",
            "piece": "lambda_A0 F_Q^2",
            "vertical_status": "vertical-silent if truly constant and universal",
            "local_GR_role": "can be absorbed into empirical Z_Q like GR absorbs empirical G; not fatal to local Maxwell/GR reduction",
            "prediction_role": "blocks a derived alpha value and weakens unification claim",
            "status": "ALLOWED_BUT_NOT_PREDICTIVE",
            "valid_for_claim": "false",
        },
        {
            "zq_id": "ZQS3288_2_hidden_scalar",
            "piece": "f_X(I_hid) F_Q^2",
            "vertical_status": "not vertical-silent unless f_X is absent or constant on vertical fibres",
            "local_GR_role": "dangerous: creates alpha/source fifth-force and readout drift",
            "prediction_role": "requires product-bound/source projection rows",
            "status": "LIVE_DANGEROUS_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "zq_id": "ZQS3288_3_radiative_readout",
            "piece": "delta_lambda_rad + readout Hodge/hbar*c terms",
            "vertical_status": "not vertical-silent unless effective/readout functor is parent-closed",
            "local_GR_role": "dangerous for measured clocks/spectra even if tree-level block is quiet",
            "prediction_role": "requires radiative/readout closure or empirical product bounds",
            "status": "LIVE_READOUT_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "zq_id": "ZQS3288_4_total",
            "piece": "Z_Q = C_P N_Q + lambda_A0 + f_X + delta_lambda_rad + readout",
            "vertical_status": "q-basic iff L_v Z_Q=0 for the whole sum without cancellation games",
            "local_GR_role": "only q-basic universal Z_Q belongs in clean local Maxwell/GR limit",
            "prediction_role": "numeric value can be calibrated initially, but drift/universality cannot be assumed",
            "status": "SPLIT_CONTRACT",
            "valid_for_claim": "false",
        },
    ]


def gr_relevance_rows() -> list[dict[str, Any]]:
    return [
        {
            "criterion_id": "LGR3288_0_value_vs_silence",
            "question": "must MTS derive the numerical value of Z_Q immediately?",
            "answer": "no for local GR/Maxwell reduction; yes eventually for a stronger unification/prediction claim",
            "reason": "GR uses empirical G, but local tests require constants to be universal and not hidden/environment drifting.",
            "status": "FAIR_CLAIM_STANDARD",
            "valid_for_claim": "false",
        },
        {
            "criterion_id": "LGR3288_1_metric_requirement",
            "question": "what metric condition is minimally needed?",
            "answer": "[g_EM]=[g_pub] for light cones plus shared matter/clock/source coframe for the observed representative",
            "reason": "EM nonbirefringence gives the cone; clocks/rods/matter fix the public scale used by source stress.",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "criterion_id": "LGR3288_2_coupling_requirement",
            "question": "what Z_Q condition is minimally needed?",
            "answer": "L_v Z_Q=0 and universal source/readout convention; numerical Z_Q may be calibrated at first pass",
            "reason": "drifting or species/source-dependent Z_Q creates fifth-force/clock/WEP pressure; a constant empirical coupling does not.",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "criterion_id": "LGR3288_3_no_cancellation",
            "question": "can hidden/radiative terms cancel to make L_v Z_Q=0?",
            "answer": "not as a theorem; each nonparent term must be absent, q-basic, or separately bounded",
            "reason": "cancellation between unrelated sectors would be a closure assumption and not robust under data splits.",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": "false",
        },
    ]


def residual_rows(bound: float) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SPL3288_0_clean_local_limit_conditional",
            "prediction": "0",
            "abs_bound": fmt(bound),
            "source_status": "THEOREM_CONDITIONAL_IF_SAME_CONE_COFRAME_AND_LVZQ_ZERO",
            "result": "PASS_NUMERIC_NONCLAIM",
            "needed": "[g_EM]=[g_pub], shared e_obs, L_v Z_Q=0, no hidden/radiative/readout drift",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SPL3288_1_metric_split_residual",
            "prediction": "Pi_g[L_v([g_EM]-[g_pub]) + L_v(scale/coframe)]/N_g",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_METRIC_SPLIT_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "needed": "same-cone/coframe theorem or optical-metric residual source map",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SPL3288_2_ZQ_drift_residual",
            "prediction": "L_v ln Z_Q = L_v ln(C_P N_Q + lambda_A0 + f_X + delta_lambda_rad + readout)",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_ZQ_DRIFT_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "needed": "q-basic Z_Q theorem or source-backed alpha/readout product rows",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SPL3288_3_half_bound_smoke",
            "prediction": fmt(0.5 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "needed": "none; schema test only",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SPL3288_4_twice_bound_smoke",
            "prediction": fmt(2.0 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "needed": "none; schema test only",
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
        "SPL3288_0_clean_local_limit_conditional": "PASS_NUMERIC_NONCLAIM",
        "SPL3288_1_metric_split_residual": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "SPL3288_2_ZQ_drift_residual": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "SPL3288_3_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "SPL3288_4_twice_bound_smoke": "FAIL_BOUND",
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        prediction = str(row["prediction"])
        bound = float(row["abs_bound"])
        if row["source_status"].startswith("MISSING"):
            result = "REFUSE_MISSING_SOURCE_NONCLAIM"
            ratio = "N/A"
        elif is_number(prediction):
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
            "gate_id": "GATE3288_0_metric_split_derived",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "same-public-metric split is refined into EM cone equality plus clock/matter coframe scale.",
        },
        {
            "gate_id": "GATE3288_1_ZQ_value_vs_silence_split",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "constant calibrated Z_Q is separated from dangerous hidden/radiative/readout drift.",
        },
        {
            "gate_id": "GATE3288_2_same_cone_coframe_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "same cone/coframe theorem remains conditional in 1009/1012/1016.",
        },
        {
            "gate_id": "GATE3288_3_LvZQ_zero_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "Z_Q q-basic theorem remains unsigned because no-extra-F2/operator-domain/readout closure are not derived.",
        },
        {
            "gate_id": "GATE3288_4_numeric_residual_sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no numeric metric-split or Z_Q-drift projection row exists.",
        },
        {
            "gate_id": "GATE3288_5_no_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "no local-GR/Maxwell/alpha/PPN/clock claim is allowed from this split.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3288_0_fair_constant_standard",
            "decision": "A calibrated constant Z_Q is not fatal to local GR/Maxwell reduction.",
            "why_it_moves_forward": "this matches how GR handles G: the first requirement is universality and vertical silence, not immediate numerical derivation.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3288_1_real_coupling_danger",
            "decision": "Hidden/radiative/readout drift in Z_Q remains fatal unless derived zero or bounded.",
            "why_it_moves_forward": "the coupling bottleneck is now precise: L_v Z_Q and source/readout universality, not aesthetic dislike of constants.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3288_2_metric_path",
            "decision": "EM Hodge reconstruction only fixes the cone; local GR needs shared coframe/scale with matter and clocks.",
            "why_it_moves_forward": "prevents overclaiming from EM waves while preserving the useful Poynting/Hodge route.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3288_3_next_work",
            "decision": "Next target should try the q-basic Z_Q theorem as vertical silence, not alpha-value derivation.",
            "why_it_moves_forward": "it is the least costly coupling win: prove no drift/universality first, leave exact alpha value as later stronger target.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3288_0_3289",
            "target_doc": "3289-Y5-R2FR-qbasic-ZQ-vertical-silence-or-alpha-product-residual-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3289_qbasic_ZQ_vertical_silence_or_alpha_product_residual.py",
            "objective": "Try to prove L_v Z_Q=0 as a universality/vertical-silence theorem without deriving the numerical alpha value: separate constant calibrated pieces from hidden, source-dependent, radiative, and readout pieces; if the theorem fails, retain a source-ready alpha/Z_Q product residual.",
            "guardrail": "Do not require numerical alpha derivation for local-GR reduction, but do not allow hidden drift, species/source dependence, radiative readout leakage, or cancellation between pieces.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    metric: list[dict[str, Any]],
    zq: list[dict[str, Any]],
    gr: list[dict[str, Any]],
    residual: list[dict[str, Any]],
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
                "detail": compact(detail, 660),
            }
        )

    add("VAL3288_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3288_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add(
        "VAL3288_2_outputs_parse",
        "all 3288 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3288_3_metric_conformal_split_present",
        "metric table separates conformal cone and coframe scale",
        any("[g_EM]" in row["statement"] and "conformal" in row["statement"] for row in metric)
        and any("coframe" in row["statement"] and "scale" in row["statement"] for row in metric),
    )
    add(
        "VAL3288_4_ZQ_value_vs_drift_present",
        "Z_Q table separates calibrated constants from dangerous drift",
        any(row["zq_id"] == "ZQS3288_1_constant_lambda" and "not fatal" in row["local_GR_role"] for row in zq)
        and any(row["zq_id"] == "ZQS3288_2_hidden_scalar" and "dangerous" in row["local_GR_role"] for row in zq),
    )
    add(
        "VAL3288_5_local_GR_fair_standard_present",
        "local GR relevance table allows calibrated value but requires silence",
        any("empirical G" in row["reason"] for row in gr)
        and any("L_v Z_Q=0" in row["answer"] for row in gr),
    )
    add(
        "VAL3288_6_residual_rows_refuse_missing_sources",
        "metric split and Z_Q drift residual rows refuse missing numeric projections",
        any(row["row_id"] == "SPL3288_1_metric_split_residual" and row["result"] == "REFUSE_MISSING_SOURCE_NONCLAIM" for row in residual)
        and any(row["row_id"] == "SPL3288_2_ZQ_drift_residual" and row["result"] == "REFUSE_MISSING_SOURCE_NONCLAIM" for row in residual),
    )
    add(
        "VAL3288_7_runner_expectations",
        "split runner expectations all match",
        all(row["expectation_met"] == "true" for row in runner),
        ";".join(f"{row['row_id']}={row['result']}" for row in runner),
    )
    add(
        "VAL3288_8_claim_gates_false",
        "no 3288 gate allows local-GR/alpha/Maxwell claim",
        all(row["claim_allowed"] == "false" for row in promotion)
        and all(row["valid_for_claim"] == "false" for row in residual),
    )
    add(
        "VAL3288_9_next_target_focused",
        "next target focuses q-basic Z_Q vertical silence",
        any("qbasic-ZQ" in row["target_doc"] and "L_v Z_Q=0" in row["objective"] for row in next_target),
    )
    add(
        "VAL3288_10_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3288_11_overall",
        "3288 validation overall",
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
    metric: list[dict[str, Any]],
    zq: list[dict[str, Any]],
    gr: list[dict[str, Any]],
    residual: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3288 - Same-public-metric or ZQ impedance owner split under AX1090

## Summary

3288 separates two things that were getting tangled:

1. **Metric identification:** EM nonbirefringence/Hodge closure gives a conformal cone `[g_EM]`. It does **not** by itself prove the matter/clock/source metric `g_pub`.
2. **Scalar coupling:** the Maxwell impedance `Z_Q` does not need its numerical value derived immediately for local Maxwell/GR reduction, but it must be universal and vertical-silent: `L_v Z_Q=0`.

This is the fair standard. GR uses an empirical `G`; a first serious MTS local limit may also use calibrated constants. What it cannot do is let those constants drift with hidden variables, source composition, readout convention, or radiative threshold choices.

In four dimensions, the Hodge star on 2-forms is conformally invariant, so EM can fix the light cone while matter/clocks/rods fix the public coframe scale. Therefore the same-metric gate becomes:

`[g_EM]=[g_pub]` plus shared observed coframe `e_obs` for matter, clocks, rods, source current, and EM stress.

The scalar coupling gate becomes:

`Z_Q = C_P N_Q + lambda_A0 + f_X + delta_lambda_rad + readout`

with no cancellation games. Constant calibrated pieces are weaker than derivation but not fatal; hidden/radiative/readout drift is fatal unless derived zero or bounded.

Selected residual envelope remains:

`|residual| <= {fmt(bound)}`.

## Metric Identification Split
{md_table(metric, ["metric_gate_id", "object", "statement", "status"])}

## Z_Q Impedance Decomposition
{md_table(zq, ["zq_id", "piece", "vertical_status", "local_GR_role", "prediction_role", "status"])}

## Local GR Relevance Table
{md_table(gr, ["criterion_id", "question", "answer", "reason", "status"])}

## Finite Residual Rows
{md_table(residual, ["row_id", "prediction", "abs_bound", "source_status", "result", "valid_for_claim"])}

## Split Bound Runner
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
    bound = bound_from_3287()
    sources = source_register_rows()
    metric = metric_rows()
    zq = zq_rows()
    gr = gr_relevance_rows()
    residual = residual_rows(bound)
    runner = runner_rows(residual)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["metric"], metric)
    write_csv(OUTPUTS["zq"], zq)
    write_csv(OUTPUTS["gr"], gr)
    write_csv(OUTPUTS["residual"], residual)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, metric, zq, gr, residual, runner, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(bound, metric, zq, gr, residual, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
