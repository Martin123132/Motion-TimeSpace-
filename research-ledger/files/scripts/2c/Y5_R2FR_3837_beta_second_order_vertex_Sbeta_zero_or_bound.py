from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3837"
BRANCH = "MTS_R2FR_Y5_BETA_SECOND_ORDER_VERTEX_SBETA_ZERO_OR_BOUND_3837"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3837-Y5-R2FR-beta-second-order-vertex-Sbeta-zero-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3836 = PCW / "3836-Y5-R2FR-direct-gamma-readout-eps-spatial-zero-or-source-bound.md"
CSV_3836_GAMMA = OUT / "P8_Y5_R2FR_3836_GAMMA_LEDGER_UPDATE.csv"
CSV_3836_VALIDATION = OUT / "P8_Y5_BRR545_3836_VALIDATION.csv"
CSV_3829_OWNER = OUT / "P8_Y5_R2FR_3829_SCALAR_COEFFICIENT_OWNER_MAP.csv"
CSV_3829_LOCK = OUT / "P8_Y5_R2FR_3829_SCALAR_LOCK_CONDITIONAL_THEOREM.csv"
CSV_3829_BOUNDS = OUT / "P8_Y5_R2FR_3829_GAMMA_BETA_COEFFICIENT_BOUND_ROWS.csv"
CSV_3829_BUDGET = OUT / "P8_Y5_R2FR_3829_SCALAR_RESIDUAL_BUDGET.csv"
CSV_3828_RESIDUAL = OUT / "P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv"
CSV_3828_ANSATZ = OUT / "P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3837_SOURCE_REGISTER.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3837_SBETA_DECOMPOSITION.csv",
    "vertex_conditions": OUT / "P8_Y5_R2FR_3837_EH2_VERTEX_MATCH_CONDITIONS.csv",
    "eps_temporal": OUT / "P8_Y5_R2FR_3837_EPS_TEMPORAL4_BOUND_ROWS.csv",
    "beta_bounds": OUT / "P8_Y5_R2FR_3837_BETA_BOUND_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3837_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3837_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3837_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3837_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3837_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3837_0_3836_doc", P_3836, "Direct Gamma Readout eps_spatial Zero Or Source Bound"),
    ("SRC3837_1_3836_gamma", CSV_3836_GAMMA, "GUP3836_2_gamma_total_update"),
    ("SRC3837_2_3836_validation", CSV_3836_VALIDATION, "VAL3836_4_gamma_blocked"),
    ("SRC3837_3_3829_owner", CSV_3829_OWNER, "COEFF3829_4_S_beta"),
    ("SRC3837_4_3829_lock", CSV_3829_LOCK, "LOCK3829_2_beta_EH2_vertex"),
    ("SRC3837_5_3829_beta_bound", CSV_3829_BOUNDS, "BND3829_2_beta"),
    ("SRC3837_6_3829_budget", CSV_3829_BUDGET, "RB3829_3_beta_EH2"),
    ("SRC3837_7_3828_residual", CSV_3828_RESIDUAL, "RPPN3828_1_beta"),
    ("SRC3837_8_3828_ansatz", CSV_3828_ANSATZ, "ANS3828_0_Newtonian_temporal"),
    ("SRC3837_9_3818_Poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_beta_second_order_vertex_Sbeta_zero_or_bound",
                "claim_use": "second_order_vertex_bound_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "SB3837_0_EH2_vertex",
            "component": "S_EH2_mismatch",
            "definition": "difference between parent second variation in the local metric sector and the GR/EH quadratic 00 vertex",
            "zero_route": "parent action second variation equals EH quadratic vertex after the 3818 Poisson normalization and same source measure",
            "bound_formula": "B_EH2_vertex <= abs(S_EH2_mismatch/C_t^2)",
            "status": "PARENT_SECOND_VARIATION_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SB3837_1_extra_scalar2",
            "component": "S_extra_scalar2",
            "definition": "extra scalar quadratic self-energy or independent nonlinear visible potential not present in GR beta",
            "zero_route": "no independent scalar self-energy in ordinary visible metric readout",
            "bound_formula": "B_extra_scalar2 <= abs(S_extra_scalar2/C_t^2)",
            "status": "EXTRA_SCALAR_SELF_ENERGY_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SB3837_2_boundary2",
            "component": "S_boundary2",
            "definition": "second-order boundary/reference contribution to the temporal metric coefficient",
            "zero_route": "boundary/reference zero route extends to second-order temporal self-coupling",
            "bound_formula": "B_boundary2 <= abs(S_boundary2/C_t^2)",
            "status": "SECOND_ORDER_BOUNDARY_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SB3837_3_readout2",
            "component": "S_readout2",
            "definition": "second-order temporal readout/projection mismatch after Newtonian C_t calibration",
            "zero_route": "same metric readout fixes both first-order C_t and second-order B_t before arena projection",
            "bound_formula": "B_readout2 <= abs(S_readout2/C_t^2)",
            "status": "SECOND_ORDER_READOUT_NATURALITY_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SB3837_4_total",
            "component": "S_beta",
            "definition": "total second-order beta/self-coupling residual in B_t=C_t^2+S_beta",
            "zero_route": "all four S_beta components vanish on the same compact exterior source/readout branch",
            "bound_formula": "abs(S_beta/C_t^2) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2",
            "status": "FIRST_SBETA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def vertex_condition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "condition_id": "EH2C3837_0_same_parent_action",
            "condition": "first- and second-order temporal terms come from the same parent action expansion",
            "why_needed": "prevents fitting C_t from Newtonian limit and choosing B_t independently",
            "current_status": "UNSIGNED",
            "if_unsigned": "retain S_EH2_mismatch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "EH2C3837_1_Bianchi_conservation",
            "condition": "Bianchi/conservation identity fixes the nonlinear source self-coupling after Poisson normalization",
            "why_needed": "GR beta is a nonlinear consistency condition, not a new independent coefficient",
            "current_status": "NOT_YET_PARENT_SIGNED_FOR_MTS",
            "if_unsigned": "retain S_EH2_mismatch + S_extra_scalar2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "EH2C3837_2_no_extra_scalar_energy",
            "condition": "no extra scalar quadratic energy contributes to visible g00 at the beta order",
            "why_needed": "extra scalar self-energy would shift beta while leaving gamma apparently healthy",
            "current_status": "UNSIGNED",
            "if_unsigned": "retain S_extra_scalar2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "EH2C3837_3_same_boundary_readout_order",
            "condition": "boundary/reference and readout naturality extend from first-order gamma branch to second-order beta branch",
            "why_needed": "second-order boundary/readout tails can mimic beta deviations",
            "current_status": "UNSIGNED",
            "if_unsigned": "retain S_boundary2 + S_readout2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def eps_temporal_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "ET43837_0_higher_order",
            "component": "B_eps_temporal_higher",
            "definition": "temporal metric terms beyond the beta-order Phi^2 truncation",
            "zero_route": "strict PPN order separation",
            "bound_formula": "B_eps_temporal_higher <= abs(R_g00_O(Phi^3)/Phi^2)",
            "status": "ORDER_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET43837_1_gauge",
            "component": "B_eps_temporal_gauge",
            "definition": "gauge/coordinate contribution to g00 at fourth order",
            "zero_route": "fixed PPN gauge and gauge-invariant beta extraction",
            "bound_formula": "B_eps_temporal_gauge <= abs((L_xi g00)_4/Phi^2)",
            "status": "GAUGE_FIX_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET43837_2_domain",
            "component": "B_eps_temporal_domain",
            "definition": "finite-domain/exterior cutoff correction in temporal self-coupling",
            "zero_route": "asymptotic/local exterior limit or source-backed finite-domain row",
            "bound_formula": "B_eps_temporal_domain <= abs(R_domain_g00_4/Phi^2)",
            "status": "DOMAIN_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET43837_3_total",
            "component": "abs(eps_temporal4/Phi^2)",
            "definition": "temporal fourth-order residual outside B_t Phi^2",
            "zero_route": "all temporal residual terms vanish or are below beta threshold budget",
            "bound_formula": "abs(eps_temporal4/Phi^2) <= B_eps_temporal_higher + B_eps_temporal_gauge + B_eps_temporal_domain",
            "status": "FIRST_EPS_TEMPORAL4_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BB3837_0_Sbeta",
            "observable": "S_beta",
            "formula": "abs(S_beta/C_t^2) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2",
            "needed_for_claim": "parent second variation, no extra scalar2, second-order boundary, and readout2 rows",
            "status": "FIRST_SBETA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BB3837_1_beta",
            "observable": "beta-1",
            "formula": "abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)",
            "needed_for_claim": "S_beta component bounds plus eps_temporal4 bound below sourced beta threshold",
            "status": "FIRST_INTEGRATED_BETA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BB3837_2_beta_zero",
            "observable": "beta zero route",
            "formula": "if S_EH2_mismatch=S_extra_scalar2=S_boundary2=S_readout2=eps_temporal4=0 then beta-1=0",
            "needed_for_claim": "all beta zero conditions parent/source signed on the same compact exterior branch",
            "status": "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3837_0_Sbeta_decomposed",
            "gate": "S_beta decomposed",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "S_beta now has EH2, extra scalar2, boundary2, and readout2 components",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3837_1_beta_bound",
            "gate": "beta bound emitted",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "integrated beta formula exists but no numeric/source-backed component rows exist",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3837_2_beta_claim",
            "gate": "beta/local PPN claim",
            "status": "BLOCKED_PARENT_SECOND_VARIATION_REQUIRED",
            "claim_allowed": False,
            "reason": "EH2 vertex match and second-order readout/boundary clauses are unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3837_3_local_GR_claim",
            "gate": "local GR claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "gamma and beta ledgers are structural/nonclaim; numeric/source thresholds absent",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3837_4_next_target",
            "gate": "next target attacks EH2 vertex match",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "S_EH2_mismatch is the core beta term and least avoidable derivation target",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3837_0_beta_not_free_parameter",
            "decision": "do not treat beta as an adjustable second PPN coefficient",
            "basis": "B_t must be tied to C_t by the same parent action expansion or retained as S_beta",
            "consequence": "local GR remains blocked until second-order self-coupling is derived or bounded",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3837_1_EH2_first",
            "decision": "attack EH2 vertex match before weaker beta source-filling",
            "basis": "S_EH2_mismatch is the core theoretical term; source-filling without it would look post-hoc",
            "consequence": "3838 should test parent second variation against the EH quadratic vertex",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3837_2_gamma_status",
            "decision": "keep gamma structurally complete but nonclaim while beta is developed",
            "basis": "3836 completed gamma's formula ledger but not numeric/source thresholds",
            "consequence": "the next derivation work belongs to beta, not more gamma prose",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3837_0",
            "next_checkpoint": "3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md",
            "script": "scripts/Y5_R2FR_3838_EH2_parent_second_variation_vertex_match_or_beta_bound.py",
            "objective": "test whether the parent second variation matches the GR/EH quadratic 00 vertex after Poisson normalization, or retain/source-bound S_EH2_mismatch",
            "reason": "3837 decomposes S_beta and shows S_EH2_mismatch is the core beta/local-GR derivation target",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_BETA_SBETA_BOUND_FORM",
            "claim": "no beta/local-GR claim",
            "summary": "3837 decomposes S_beta and emits first integrated beta bound rows, selecting EH2 vertex match as the next derivation target.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(sources, decomposition, vertex_conditions, eps_temporal, beta_bounds, gates, decisions, timestamp: str) -> None:
    text = f"""# 3837 — Beta Second-Order Vertex Sbeta Zero Or Bound

Private checkpoint. This starts the beta branch after the gamma ledger became structurally complete. It does not claim `beta=1`.

Generated: `{timestamp}`

## Result

The beta residual is now decomposed:

`B_t = C_t^2 + S_beta`

`S_beta = S_EH2_mismatch + S_extra_scalar2 + S_boundary2 + S_readout2`.

So

`abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)`.

This blocks a dangerous shortcut: `C_t` being Newtonian-normalized does not automatically fix the second-order self-coupling.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## S_beta Decomposition

{markdown_table(decomposition, ["component_id", "component", "definition", "zero_route", "status"])}

## EH2 Vertex Match Conditions

{markdown_table(vertex_conditions, ["condition_id", "condition", "why_needed", "current_status", "if_unsigned"])}

## eps_temporal4 Bound Rows

{markdown_table(eps_temporal, ["component_id", "component", "definition", "zero_route", "status"])}

## Beta Bound Rows

{markdown_table(beta_bounds, ["bound_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

Gamma is structurally mapped; beta is now the live mathematical problem. The next clean derivation target is the parent second variation: does it actually produce the EH quadratic 00 vertex after the Poisson/Newton normalization, or does `S_EH2_mismatch` survive as a beta residual?

Next target: `3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3836", "Current State After 3837", 1)
    paragraph = (
        "`3837` starts the beta branch. `B_t=C_t^2+S_beta` with "
        "`S_beta=S_EH2_mismatch+S_extra_scalar2+S_boundary2+S_readout2`, so "
        "`|beta-1| <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+|eps_temporal4/Phi^2|`. "
        "This keeps beta from becoming a free post-Newtonian knob and selects the parent second-variation/EH2 vertex match as the next proof target.\n\n"
    )
    anchor = "`3836` decomposes"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3837-Y5-R2FR-beta-second-order-vertex-Sbeta-zero-or-bound.md`

Target: derive or source-bound `S_beta` in `B_t=C_t^2+S_beta`, separating EH second-order vertex mismatch, extra scalar self-energy, boundary2, and readout2 terms.

This is the best next move because 3836 makes gamma structurally complete but nonclaim; beta is now the main undeveloped PPN/local-GR branch."""
    new_gate = """`3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md`

Target: test whether the parent second variation matches the GR/EH quadratic 00 vertex after Poisson normalization, or retain/source-bound `S_EH2_mismatch`.

This is the best next move because 3837 decomposes `S_beta` and shows `S_EH2_mismatch` is the core beta/local-GR derivation target."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3837_SBETA_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3837_EH2_VERTEX_MATCH_CONDITIONS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3837_EPS_TEMPORAL4_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3837_BETA_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3837_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3837_SBETA_DECOMPOSITION.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3837 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3837 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, decomposition, vertex_conditions, eps_temporal, beta_bounds, gates, timestamp: str):
    rows = []

    def add(check_id, check, passed, detail):
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in decomposition + vertex_conditions + eps_temporal + beta_bounds + gates)
    add("VAL3837_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3837_1_sbeta_components", "S_beta components are decomposed", all(token in all_text for token in ["S_EH2_mismatch", "S_extra_scalar2", "S_boundary2", "S_readout2", "S_beta"]), "S_beta tokens present")
    add("VAL3837_2_beta_bound", "integrated beta bound row exists", any(row["bound_id"] == "BB3837_1_beta" for row in beta_bounds), f"{len(beta_bounds)} beta bound rows")
    add("VAL3837_3_eps_temporal", "eps_temporal4 is decomposed", all(token in all_text for token in ["B_eps_temporal_higher", "B_eps_temporal_gauge", "B_eps_temporal_domain", "eps_temporal4/Phi^2"]), "eps temporal tokens present")
    add("VAL3837_4_nonclaim", "all 3837 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in decomposition + vertex_conditions + eps_temporal + beta_bounds + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3837_5_beta_blocked", "beta claim remains blocked", any(row["gate_id"] == "GATE3837_2_beta_claim" and row["status"].startswith("BLOCKED") for row in gates), "beta gate blocked")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3837_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3837_7_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "S_EH2_mismatch" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3837*", "P8_Y5_BRR545_3837*", "*Y5_R2FR_3837*", "3837-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3837_8_formalization_clean", "formalization-workbench has no 3837 files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3837 file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3837_9_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    decomposition = decomposition_rows(timestamp)
    vertex_conditions = vertex_condition_rows(timestamp)
    eps_temporal = eps_temporal_rows(timestamp)
    beta_bounds = beta_bound_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["decomposition"], decomposition)
    write_csv(OUTPUTS["vertex_conditions"], vertex_conditions)
    write_csv(OUTPUTS["eps_temporal"], eps_temporal)
    write_csv(OUTPUTS["beta_bounds"], beta_bounds)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, decomposition, vertex_conditions, eps_temporal, beta_bounds, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, decomposition, vertex_conditions, eps_temporal, beta_bounds, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_BETA_SBETA_BOUND_FORM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
