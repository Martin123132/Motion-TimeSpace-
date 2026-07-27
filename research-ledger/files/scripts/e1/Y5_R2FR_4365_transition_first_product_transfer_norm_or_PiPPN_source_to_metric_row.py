from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4365"
CLAIM_ID = "L-206"
BRANCH = "MTS_R2FR_Y5_TRANSITION_FIRST_PRODUCT_TRANSFER_NORM_OR_PIPPN_SOURCE_TO_METRIC_ROW_4365"
MARKER = "PPC4161_TRANSITION_FIRST_PRODUCT_TRANSFER_NORM_OR_PIPPN_SOURCE_TO_METRIC_ROW_4365"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_FIRST_PRODUCT_TRANSFER_NORM_OR_PIPPN_SOURCE_TO_METRIC_ROW_4365"
DECISION = "PRODUCT_TRANSFER_CRITICAL_NORMS_DERIVED_PIPPN_ACTUAL_TRANSFER_STILL_MISSING_NONCLAIM"
NEXT_TARGET = "4366-Y5-R2FR-transition-preferred-frame-product-channel-zero-or-PiPPN-transfer-coefficient.md"

FORMAL_PATH = FORMAL / "381-PPC4161-transition-first-product-transfer-norm-or-PiPPN-source-to-metric-row.md"
DOC_PATH = POST / "4365-Y5-R2FR-transition-first-product-transfer-norm-or-PiPPN-source-to-metric-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4365_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

B_WEP_PRODUCT = 2.8e-15

BOUND_ROWS = [
    ("R3_gamma", "gamma_minus_1", "PPN_gamma", "dimensionless_per_product", "solar_light_propagation", "solar_compatible"),
    ("R4_beta", "beta_minus_1", "PPN_beta", "dimensionless_per_product", "orbital_second_order", "solar_compatible"),
    ("R5_alpha1", "alpha1", "PPN_preferred_frame_alpha1", "dimensionless_per_product", "preferred_frame", "solar_compatible"),
    ("R6_alpha2", "alpha2", "PPN_preferred_frame_alpha2", "dimensionless_per_product", "preferred_frame", "solar_compatible"),
    ("R7_alpha3", "alpha3", "PPN_momentum_preferred_frame_alpha3", "dimensionless_per_product", "momentum_preferred_frame", "full_table_strong_field_caveat"),
    ("R8_xi", "xi", "PPN_preferred_location_xi", "dimensionless_per_product", "preferred_location", "full_table_strong_field_caveat"),
    ("R9_Gdot", "Gdot_over_G", "local_Gdot", "yr^-1_per_product", "source_normalization_drift", "solar_compatible"),
    ("R2_clock_redshift", "alpha_clock_redshift", "clock_redshift", "dimensionless_per_product", "clock_transfer", "side_lane"),
]


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4365_00_4364_formal": (
        FORMAL / "380-PPC4161-transition-tau-WEP-lower-bound-or-product-only-local-route.md",
        "product-only transfer theorem",
        "4364 derives the product-only transfer law.",
    ),
    "SRC4365_01_4364_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4364_PRODUCT_TRANSFER_CONTRACT.csv",
        "TR4364_2_PPN",
        "4364 PPN/local transfer contract waiting for a transfer norm.",
    ),
    "SRC4365_02_4364_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4364_PRODUCT_ONLY_THEOREM_ROWS.csv",
        "TH4364_1_transfer_norm",
        "Exact product transfer theorem.",
    ),
    "SRC4365_03_4363_projection": (
        SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv",
        "PI4363_WEP_product",
        "WEP product source-backed bound row.",
    ),
    "SRC4365_04_local_bounds": (
        LOCAL_BOUNDS / "local_bound_claims.csv",
        "R7_alpha3",
        "Local bound table containing PPN, clock and Gdot comparators.",
    ),
    "SRC4365_05_1883_ppn_bounds": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1883_PPN_BOUND_ROWS.csv",
        "PBOUND1883_4_alpha3",
        "Prior PPN bound rows and use policy.",
    ),
    "SRC4365_06_1883_ppn_vector": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
        "PPNV1883_7_total_no_cancellation",
        "Existing PPN vector residual discipline and no-cancellation policy.",
    ),
    "SRC4365_07_4362_arena_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_ARENA_PROJECTION_CONTRACT.csv",
        "ARENA4362_1_PPN",
        "Earlier C_src arena projection contract.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def local_bounds_by_row_id() -> Dict[str, Dict[str, str]]:
    rows = read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    return {row["row_id"]: row for row in rows}


def product_bound() -> float:
    rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv")
    match = [row for row in rows if row.get("projection_id") == "PI4363_WEP_product"]
    if len(match) != 1:
        raise ValueError("expected one PI4363_WEP_product row")
    return float(match[0]["source_bound_value"])


def threshold_rows(bounds: Dict[str, Dict[str, str]], b_wep: float) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row_id, observable, lane, transfer_units, channel_class, policy in BOUND_ROWS:
        bound = bounds[row_id]
        upper_bound = float(bound["upper_bound"])
        critical_norm = upper_bound / b_wep
        rows.append(
            {
                "threshold_id": f"CT4365_{row_id}",
                "source_row_id": row_id,
                "observable": observable,
                "lane": lane,
                "channel_class": channel_class,
                "upper_bound": f"{upper_bound:.16g}",
                "upper_bound_units": bound["units"],
                "B_WEP_product": f"{b_wep:.16g}",
                "critical_transfer_norm": f"{critical_norm:.16g}",
                "critical_transfer_units": transfer_units,
                "formula": "A_crit = upper_bound / B_WEP_product",
                "source_reference": bound["reference_path_or_url"],
                "use_policy": policy,
                "actual_transfer_norm_present": "False",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def ppn_summary_rows(thresholds: List[Dict[str, str]]) -> List[Dict[str, str]]:
    ppn_rows = [row for row in thresholds if row["lane"].startswith("PPN_")]
    full_min = min(ppn_rows, key=lambda row: float(row["critical_transfer_norm"]))
    solar_rows = [row for row in ppn_rows if row["use_policy"] == "solar_compatible"]
    solar_min = min(solar_rows, key=lambda row: float(row["critical_transfer_norm"]))
    gamma = next(row for row in thresholds if row["source_row_id"] == "R3_gamma")
    beta = next(row for row in thresholds if row["source_row_id"] == "R4_beta")
    return [
        {
            "summary_id": "SUM4365_0_full_PPN_table",
            "scope": "full PPN table including strong-field caveat rows",
            "weighted_norm_gate": "max_j |T_j|/Acrit_j <= 1",
            "dominant_observable": full_min["observable"],
            "dominant_critical_norm": full_min["critical_transfer_norm"],
            "interpretation": "alpha3 dominates the full-table critical norm; any product coupling into momentum/preferred-frame channels must be theorem-zero or extremely suppressed",
            "actual_transfer_norm_present": "False",
            "claim_allowed": "False",
        },
        {
            "summary_id": "SUM4365_1_solar_compatible_subset",
            "scope": "solar-compatible PPN subset in current local bounds table",
            "weighted_norm_gate": "max_solar |T_j|/Acrit_j <= 1",
            "dominant_observable": solar_min["observable"],
            "dominant_critical_norm": solar_min["critical_transfer_norm"],
            "interpretation": "alpha2 dominates the solar-compatible preferred-frame gate; gamma and beta are loose compared with the product bound",
            "actual_transfer_norm_present": "False",
            "claim_allowed": "False",
        },
        {
            "summary_id": "SUM4365_2_gamma_beta_headroom",
            "scope": "classic gamma/beta weak-field lanes",
            "weighted_norm_gate": "T_gamma <= Acrit_gamma and T_beta <= Acrit_beta",
            "dominant_observable": "gamma_beta_pair",
            "dominant_critical_norm": min(gamma["critical_transfer_norm"], beta["critical_transfer_norm"], key=float),
            "interpretation": "gamma/beta allow transfer norms of order 1e10, so the product row is not the bottleneck there; factorization and preferred-frame silence are the real bottlenecks",
            "actual_transfer_norm_present": "False",
            "claim_allowed": "False",
        },
    ]


def requirement_rows(thresholds: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        {
            "requirement_id": "REQ4365_0_factorization",
            "required_object": "product factorization theorem",
            "requirement": "R_j must be proved to depend on p_WEP_TiPt rather than Delta_w_TiPt separately",
            "why": "4364 small-tau countermodel defeats nonfactorized residuals",
            "current_status": "MISSING_FOR_PPN_GR",
            "next_action": "derive Pi_PPN product channel from parent source-to-metric map",
            "claim_allowed": "False",
        },
        {
            "requirement_id": "REQ4365_1_transfer_coefficients",
            "required_object": "T_j product-transfer coefficients",
            "requirement": "one coefficient per observable, fixed before scoring",
            "why": "critical thresholds are pass/fail limits, not MTS predictions",
            "current_status": "MISSING",
            "next_action": "fill or prove zero for gamma,beta,alpha1,alpha2,alpha3,xi,Gdot",
            "claim_allowed": "False",
        },
        {
            "requirement_id": "REQ4365_2_preferred_frame_zero",
            "required_object": "preferred-frame/momentum product-channel silence",
            "requirement": "T_alpha3=0 or |T_alpha3|<=1.428571e-5 for full-table row",
            "why": "alpha3 is the severe bottleneck in the source-backed critical table",
            "current_status": "MISSING",
            "next_action": "derive scalar/source-normalization-only coupling or retain alpha3 as lethal gate",
            "claim_allowed": "False",
        },
        {
            "requirement_id": "REQ4365_3_conservation",
            "required_object": "Bianchi/conservation-compatible source-to-metric transfer",
            "requirement": "Pi_GR/Pi_PPN product transfer must preserve local conservation and not generate hidden stress",
            "why": "local GR reduction needs conserved source stress, not just small PPN numbers",
            "current_status": "MISSING",
            "next_action": "derive product channel as scalar calibrated source normalization or prove it is absent from metric stress",
            "claim_allowed": "False",
        },
    ]


def danger_rows(thresholds: List[Dict[str, str]]) -> List[Dict[str, str]]:
    sorted_rows = sorted(thresholds, key=lambda row: float(row["critical_transfer_norm"]))
    out: List[Dict[str, str]] = []
    for rank, row in enumerate(sorted_rows, start=1):
        out.append(
            {
                "rank": str(rank),
                "observable": row["observable"],
                "lane": row["lane"],
                "critical_transfer_norm": row["critical_transfer_norm"],
                "danger_interpretation": (
                    "hardest; theorem-zero likely needed"
                    if rank == 1
                    else "tight preferred-frame/source-drift gate"
                    if rank <= 4
                    else "large headroom if factorization holds"
                ),
                "use_policy": row["use_policy"],
                "claim_allowed": "False",
            }
        )
    return out


def runner_rows(summary: List[Dict[str, str]], requirements: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        {
            "run_id": "RUN4365_0_thresholds",
            "operation": "compute Acrit_j=bound_j/B_WEP",
            "result": "CRITICAL_THRESHOLDS_READY",
            "detail": "all selected source-backed numeric bounds converted to transfer-norm thresholds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4365_1_weighted_norm",
            "operation": "define weighted PPN norm gate",
            "result": "GATE_READY_NO_ACTUAL_T",
            "detail": summary[0]["weighted_norm_gate"],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4365_2_preferred_frame",
            "operation": "identify bottleneck",
            "result": "ALPHA3_FULL_TABLE_ALPHA2_SOLAR_SUBSET_DOMINATE",
            "detail": "preferred-frame/momentum channels, not gamma/beta, are the dangerous transfer lanes",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4365_3_claim",
            "operation": "score current MTS product-to-PPN transfer",
            "result": "NOT_SCORED",
            "detail": "actual product-transfer coefficients are missing: " + "; ".join(row["requirement_id"] for row in requirements[:3]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4365_0_thresholds",
            "gate": "critical transfer thresholds",
            "requirement": "source-backed local bounds and B_WEP product bound",
            "current_result": "PASS_NONCLAIM_NUMERIC_THRESHOLDS",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4365_1_actual_PiPPN",
            "gate": "actual Pi_PPN product transfer row",
            "requirement": "parent-derived or source-backed T_j coefficients fixed before scoring",
            "current_result": "MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4365_2_preferred_frame",
            "gate": "preferred-frame product silence",
            "requirement": "T_alpha3=0 or <= alpha3 critical threshold; T_alpha2 below solar subset threshold",
            "current_result": "MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4365_3_public_claim",
            "gate": "claim PPN/Newton/local-GR pass",
            "requirement": "factorization plus actual transfer coefficients plus conservation/Bianchi closure",
            "current_result": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4365_0",
            "decision": DECISION,
            "rationale": "4365 converts the 4364 product-only theorem into hard numeric transfer thresholds. The WEP product bound is so tight that gamma and beta have enormous headroom if a product-only transfer exists, but preferred-frame/momentum rows dominate the real risk: alpha3 in the full table and alpha2 in the solar-compatible subset. No actual Pi_PPN transfer is claimed; the next derivation must either prove the product channel has no preferred-frame component or supply source-backed transfer coefficients below these thresholds.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4365_0",
            "item": "critical thresholds",
            "status": "DERIVED",
            "detail": "Acrit_j=bound_j/2.8e-15 for selected PPN/clock/Gdot lanes.",
        },
        {
            "status_id": "STAT4365_1",
            "item": "Pi_PPN actual transfer",
            "status": "MISSING",
            "detail": "No MTS T_j product-transfer coefficients are present yet.",
        },
        {
            "status_id": "STAT4365_2",
            "item": "bottleneck",
            "status": "PREFERRED_FRAME_CHANNELS",
            "detail": "alpha3 full-table and alpha2 solar-compatible thresholds dominate.",
        },
        {
            "status_id": "STAT4365_3",
            "item": "next target",
            "status": "PREFERRED_FRAME_ZERO_OR_TRANSFER_COEFFICIENT",
            "detail": NEXT_TARGET,
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "target_id": "NT4365_0",
            "next_target": NEXT_TARGET,
            "question": "Can the WEP product channel be proved scalar/source-normalization-only with no preferred-frame transfer, or can T_alpha3/T_alpha2 be bounded below the critical thresholds?",
            "preferred_route": "derive T_alpha3=T_alpha2=0 from covariance/isotropy/scalar source-normalization of the product channel",
            "alternate_route": "derive actual Pi_PPN product-transfer coefficients and compare to Acrit rows",
            "fallback_route": "demote product-to-PPN transfer to closure-only and move to Pi_GR conserved source-stress row",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: List[Dict[str, str]],
    thresholds: List[Dict[str, str]],
    summary: List[Dict[str, str]],
    requirements: List[Dict[str, str]],
    dangers: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "check": check,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    by_obs = {row["observable"]: row for row in thresholds}
    add("VAL4365_00_sources_exist", "all cited local source paths exist", all(row["path_exists"] == "True" for row in sources), "source register path_exists flags")
    add("VAL4365_01_needles_found", "all cited local source needles found", all(row["needle_found"] == "True" for row in sources), "source register needle_found flags")
    add("VAL4365_02_product_bound", "product bound equals 2.8e-15", product_bound() == B_WEP_PRODUCT, str(product_bound()))
    add("VAL4365_03_threshold_count", "selected threshold rows present", len(thresholds) == len(BOUND_ROWS), f"rows={len(thresholds)}")
    add("VAL4365_04_gamma_threshold", "gamma critical threshold computed", abs(float(by_obs["gamma_minus_1"]["critical_transfer_norm"]) - (2.3e-5 / B_WEP_PRODUCT)) < 1e-6, by_obs["gamma_minus_1"]["critical_transfer_norm"])
    add("VAL4365_05_alpha3_bottleneck", "alpha3 is full-table bottleneck", summary[0]["dominant_observable"] == "alpha3", summary[0]["dominant_critical_norm"])
    add("VAL4365_06_alpha2_solar_bottleneck", "alpha2 is solar-compatible bottleneck", summary[1]["dominant_observable"] == "alpha2", summary[1]["dominant_critical_norm"])
    add("VAL4365_07_no_actual_transfer", "actual transfer coefficients remain missing", all(row["actual_transfer_norm_present"] == "False" for row in thresholds + summary), "actual_transfer_norm_present flags")
    add("VAL4365_08_requirements_include_preferred_frame", "preferred-frame zero requirement present", any(row["requirement_id"] == "REQ4365_2_preferred_frame_zero" for row in requirements), "REQ4365_2")
    add("VAL4365_09_danger_sorted", "danger ranking sorted by increasing critical threshold", dangers[0]["observable"] == "alpha3" and float(dangers[0]["critical_transfer_norm"]) <= float(dangers[1]["critical_transfer_norm"]), "rank1=" + dangers[0]["observable"])
    add("VAL4365_10_runner_nonclaim", "runner rows remain nonclaim", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in runner), "runner flags")
    add("VAL4365_11_claim_forbidden", "public claim forbidden", any(row["gate_id"] == "GATE4365_3_public_claim" and row["current_result"] == "FORBIDDEN" for row in gates), "claim gate")
    add("VAL4365_12_decision_nonclaim", "decision is nonclaim", decisions[0]["decision"] == DECISION and decisions[0]["claim_allowed"] == "False", DECISION)
    add("VAL4365_13_next_selected", "next target selected", next_targets[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4365_14_formal_marker", "formal marker written", MARKER in read_text(FORMAL_PATH), str(FORMAL_PATH))
    add("VAL4365_15_post_doc_marker", "post doc marker written", MARKER in read_text(DOC_PATH), str(DOC_PATH))
    add("VAL4365_16_spine_marker", "spine marker appended", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4365_17_packet_marker", "packet marker appended", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4365_18_claim_register", "claim register updated", f"\n{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    return rows


def write_docs(
    sources: List[Dict[str, str]],
    thresholds: List[Dict[str, str]],
    summary: List[Dict[str, str]],
    requirements: List[Dict[str, str]],
    dangers: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    formal = f"""# PPC4161 transition: first product transfer norm or PiPPN source-to-metric row

Marker: `{MARKER}`

Generated: {STAMP}

## Purpose

4364 gave the legal product-only transfer law. 4365 turns it into hard numeric thresholds:

`Acrit_j = bound_j / B_WEP`, with `B_WEP = {B_WEP_PRODUCT}`.

If a future source-to-metric product channel gives `R_j = T_j p`, then the product channel passes observable `j` only if `|T_j| <= Acrit_j`. These are pass/fail thresholds, not MTS predictions.

## Critical transfer thresholds

{md_table(thresholds, ["threshold_id", "observable", "lane", "upper_bound", "B_WEP_product", "critical_transfer_norm", "critical_transfer_units", "use_policy", "actual_transfer_norm_present", "claim_allowed"])}

## PPN vector summary

{md_table(summary, ["summary_id", "scope", "weighted_norm_gate", "dominant_observable", "dominant_critical_norm", "interpretation", "actual_transfer_norm_present", "claim_allowed"])}

## Requirements before scoring

{md_table(requirements, ["requirement_id", "required_object", "requirement", "why", "current_status", "next_action", "claim_allowed"])}

## Danger ranking

{md_table(dangers, ["rank", "observable", "lane", "critical_transfer_norm", "danger_interpretation", "use_policy", "claim_allowed"])}

## Runner

{md_table(runner, ["run_id", "operation", "result", "detail", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "requirement", "current_result", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "rationale", "next_target", "claim_allowed"])}

## Status

{md_table(statuses, ["status_id", "item", "status", "detail"])}

## Next target

{md_table(next_targets, ["target_id", "next_target", "question", "preferred_route", "alternate_route", "fallback_route", "claim_allowed"])}

## Source register

{md_table(sources, ["source_id", "path_exists", "needle_found", "line_number", "role"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")

    post_doc = f"""# 4365 - first product transfer norm or PiPPN source-to-metric row

Marker: `{MARKER}`

Generated: {STAMP}

## Result

- Derived numeric critical transfer thresholds from `B_WEP=2.8e-15`.
- Gamma/beta have huge headroom if factorization holds.
- Preferred-frame/momentum channels dominate: `alpha3` for the full table, `alpha2` for the solar-compatible subset.
- No actual `Pi_PPN` transfer coefficient is claimed yet.

## Why this matters

The next derivation no longer just says "PPN transfer missing". It says exactly what the transfer has to beat, and shows where the dragon is: preferred-frame silence.

## Files

- Formal checkpoint: `{FORMAL_PATH}`
- Thresholds: `{SOURCE_DIR / "P8_Y5_R2FR_4365_CRITICAL_TRANSFER_THRESHOLDS.csv"}`
- PPN summary: `{SOURCE_DIR / "P8_Y5_R2FR_4365_PPN_VECTOR_THRESHOLD_SUMMARY.csv"}`
- Validation: `{VALIDATION_PATH}`

## Next

{NEXT_TARGET}
"""
    DOC_PATH.write_text(post_doc, encoding="utf-8")


def update_rollups(summary: List[Dict[str, str]]) -> None:
    spine_block = f"""

## 4365 Transition first product transfer norm thresholds

Marker: `{MARKER}`

4365 converts the WEP product-only theorem into numeric transfer thresholds. For any product-channel residual `R_j=T_j p` with `|p|<=2.8e-15`, the critical transfer norm is `Acrit_j=bound_j/2.8e-15`. Gamma and beta have large headroom if product factorization holds, but the preferred-frame/momentum lanes dominate: `{summary[0]["dominant_observable"]}` is the full-table bottleneck with `Acrit={summary[0]["dominant_critical_norm"]}`, and `{summary[1]["dominant_observable"]}` is the solar-compatible subset bottleneck with `Acrit={summary[1]["dominant_critical_norm"]}`.

No actual `Pi_PPN` product-transfer coefficient is claimed. The next target is to prove the product channel is scalar/source-normalization-only with no preferred-frame transfer, or to fill source-backed `T_j` coefficients below the critical thresholds. Next target: `{NEXT_TARGET}`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""

## 4365 packet update: product transfer thresholds

Marker: `{PACKET_MARKER}`

Packet update: the product-only WEP lane now has numeric PPN/local threshold gates. A future `Pi_PPN` or `Pi_GR` product row must satisfy the weighted norm gate `max_j |T_j|/Acrit_j <= 1`. Gamma/beta are not the main danger; preferred-frame/momentum transfer is. The immediate derivation target is `T_alpha3=0`/`T_alpha2=0` from covariance/isotropy/source-normalization, or explicit sourced coefficients below the thresholds.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)

    append_claim_once(
        FORMAL / "02-claims-register.csv",
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4365 converts the WEP product-only transfer law into source-backed critical transfer thresholds for PPN/clock/Gdot lanes. For each observable j, Acrit_j=bound_j/2.8e-15 is the maximum allowed product-transfer coefficient if R_j=T_j p and p=Delta_w_TiPt*tau_WEP. Gamma and beta have large headroom, while preferred-frame/momentum rows dominate: alpha3 in the full table and alpha2 in the solar-compatible subset. No actual Pi_PPN or Pi_GR transfer coefficient is claimed; local-GR/Newton/PPN claims remain blocked until factorization, source-backed T_j coefficients, and conservation/Bianchi closure are supplied.",
            "4365 source register, critical transfer thresholds, PPN vector summary, transfer requirements, danger ranking, runner, claim gates, decision, status, next target and validation CSV.",
            "product_transfer_critical_norms_derived_actual_PiPPN_missing_nonclaim",
            "Prove preferred-frame product-channel silence or fill actual Pi_PPN/Pi_GR product-transfer coefficients below the thresholds.",
            "Treating critical thresholds as predictions; ignoring alpha3/alpha2 preferred-frame bottlenecks; using gamma/beta headroom as full PPN or local-GR proof.",
        ],
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    b_wep = product_bound()
    if b_wep != B_WEP_PRODUCT:
        raise SystemExit(f"unexpected B_WEP product bound {b_wep}")

    sources = source_rows()
    thresholds = threshold_rows(local_bounds_by_row_id(), b_wep)
    summary = ppn_summary_rows(thresholds)
    requirements = requirement_rows(thresholds)
    dangers = danger_rows(thresholds)
    runner = runner_rows(summary, requirements)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_SOURCE_REGISTER.csv", sources)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_CRITICAL_TRANSFER_THRESHOLDS.csv", thresholds)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_PPN_VECTOR_THRESHOLD_SUMMARY.csv", summary)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_TRANSFER_NORM_REQUIREMENTS.csv", requirements)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_DANGER_RANKING.csv", dangers)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_RUNNER.csv", runner)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_CLAIM_GATES.csv", gates)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_DECISION.csv", decisions)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_STATUS.csv", statuses)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_NEXT_TARGET.csv", next_targets)

    write_docs(sources, thresholds, summary, requirements, dangers, runner, gates, decisions, statuses, next_targets)
    update_rollups(summary)

    validations = validation_rows(sources, thresholds, summary, requirements, dangers, runner, gates, decisions, statuses, next_targets)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"4365 validation failed: {details}")

    print(f"{CHECKPOINT} generated: {DECISION}")
    print(f"formal={FORMAL_PATH}")
    print(f"validation={VALIDATION_PATH}")


if __name__ == "__main__":
    main()
