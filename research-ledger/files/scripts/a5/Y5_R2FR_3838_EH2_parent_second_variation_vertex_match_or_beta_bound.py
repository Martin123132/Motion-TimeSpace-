from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3838"
BRANCH = "MTS_R2FR_Y5_EH2_PARENT_SECOND_VARIATION_VERTEX_MATCH_OR_BETA_BOUND_3838"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3837 = PCW / "3837-Y5-R2FR-beta-second-order-vertex-Sbeta-zero-or-bound.md"
CSV_3837_DECOMP = OUT / "P8_Y5_R2FR_3837_SBETA_DECOMPOSITION.csv"
CSV_3837_COND = OUT / "P8_Y5_R2FR_3837_EH2_VERTEX_MATCH_CONDITIONS.csv"
CSV_3837_BETA = OUT / "P8_Y5_R2FR_3837_BETA_BOUND_ROWS.csv"
CSV_3837_VALIDATION = OUT / "P8_Y5_BRR545_3837_VALIDATION.csv"
CSV_3829_LOCK = OUT / "P8_Y5_R2FR_3829_SCALAR_LOCK_CONDITIONAL_THEOREM.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3818_RESID = OUT / "P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv"
CSV_3824_REQ = OUT / "P8_Y5_R2FR_3824_R_EQ_BOUNDARY_RESIDUAL_ROWS.csv"
CSV_3825_BOUNDARY = OUT / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3838_SOURCE_REGISTER.csv",
    "vertex_audit": OUT / "P8_Y5_R2FR_3838_EH2_VERTEX_MATCH_AUDIT.csv",
    "mismatch": OUT / "P8_Y5_R2FR_3838_EH2_MISMATCH_DECOMPOSITION.csv",
    "beta_update": OUT / "P8_Y5_R2FR_3838_BETA_BOUND_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3838_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3838_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3838_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3838_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3838_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3838_0_3837_doc", P_3837, "Beta Second-Order Vertex Sbeta Zero Or Bound"),
    ("SRC3838_1_3837_decomp", CSV_3837_DECOMP, "SB3837_0_EH2_vertex"),
    ("SRC3838_2_3837_conditions", CSV_3837_COND, "EH2C3837_0_same_parent_action"),
    ("SRC3838_3_3837_beta", CSV_3837_BETA, "BB3837_1_beta"),
    ("SRC3838_4_3837_validation", CSV_3837_VALIDATION, "VAL3837_1_sbeta_components"),
    ("SRC3838_5_3829_lock", CSV_3829_LOCK, "LOCK3829_2_beta_EH2_vertex"),
    ("SRC3838_6_3818_Poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
    ("SRC3838_7_3818_residuals", CSV_3818_RESID, "R3818_5_total"),
    ("SRC3838_8_3824_Req", CSV_3824_REQ, "R3824_5_total"),
    ("SRC3838_9_3825_boundary", CSV_3825_BOUNDARY, "R3825_4_total"),
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
                "role": "input_for_EH2_parent_second_variation_vertex_match_or_beta_bound",
                "claim_use": "second_variation_audit_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def vertex_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "EH2A3838_0_first_order_not_enough",
            "requirement": "first-order Poisson/EH bridge cannot be promoted to beta",
            "test": "3818 only proves the linear 00/Poisson bridge and source normalization route",
            "current_status": "PASS_GUARD",
            "if_failed": "beta would be smuggled from Newtonian normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EH2A3838_1_parent_second_variation",
            "requirement": "parent second variation projected to visible metric equals EH second variation",
            "test": "P_vis delta^2 S_parent P_vis = delta^2 S_EH + boundary/gauge-zero terms",
            "current_status": "MISSING_PARENT_SECOND_VARIATION",
            "if_failed": "retain B_L2_operator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EH2A3838_2_same_source_measure",
            "requirement": "quadratic gravitational self-energy couples to the same source measure as the first-order Poisson branch",
            "test": "Bianchi/conservation plus Pi_M/R_eq/source measure consistency through 3824/3825",
            "current_status": "NOT_SIGNED_AT_SECOND_ORDER",
            "if_failed": "retain B_grav_energy_source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EH2A3838_3_field_redefinition_gauge",
            "requirement": "field redefinitions/gauge choices do not move the quadratic vertex into readout coefficients",
            "test": "fixed PPN gauge/readout and no hidden nonlinear representative coefficient",
            "current_status": "UNSIGNED",
            "if_failed": "retain B_field_redef_gauge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EH2A3838_4_no_nonEH_operator",
            "requirement": "no non-EH local operator contributes at the beta order",
            "test": "no R^2/scalar/disformal/vector-tensor quadratic temporal source in visible g00",
            "current_status": "UNSIGNED",
            "if_failed": "retain B_nonEH2_operator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def mismatch_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "EH2M3838_0_L2_operator",
            "component": "B_L2_operator",
            "definition": "operator-level mismatch between parent second variation and EH quadratic visible metric vertex",
            "zero_route": "parent local metric sector action is EH to second order after quotient/projection",
            "bound_formula": "B_L2_operator <= ||P_vis(delta^2S_parent-delta^2S_EH)P_vis||/||delta^2S_EH||",
            "status": "PARENT_SECOND_VARIATION_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EH2M3838_1_grav_energy_source",
            "component": "B_grav_energy_source",
            "definition": "mismatch in how gravitational field self-energy sources the second-order 00 equation",
            "zero_route": "Bianchi/conservation and same compact source measure fix nonlinear self-coupling",
            "bound_formula": "B_grav_energy_source <= abs(R_second_order_source_measure/C_t^2)",
            "status": "SECOND_ORDER_SOURCE_MEASURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EH2M3838_2_field_redef_gauge",
            "component": "B_field_redef_gauge",
            "definition": "nonlinear field redefinition or gauge/readout shift that changes B_t without changing C_t",
            "zero_route": "fixed PPN readout gauge and field variable before fitting beta",
            "bound_formula": "B_field_redef_gauge <= abs(R_field_redef_beta)",
            "status": "GAUGE_FIELD_REDEF_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EH2M3838_3_nonEH2_operator",
            "component": "B_nonEH2_operator",
            "definition": "quadratic contribution from non-EH operators or extra fields in visible g00",
            "zero_route": "no visible R^2/scalar/disformal/vector-tensor beta-order operator survives",
            "bound_formula": "B_nonEH2_operator <= abs(R_nonEH2/C_t^2)",
            "status": "NON_EH_OPERATOR_EXCLUSION_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EH2M3838_4_total",
            "component": "B_EH2_vertex",
            "definition": "total beta contribution from parent/EH second-order vertex mismatch",
            "zero_route": "all EH2 mismatch components vanish on the same compact exterior branch",
            "bound_formula": "B_EH2_vertex <= B_L2_operator + B_grav_energy_source + B_field_redef_gauge + B_nonEH2_operator",
            "status": "FIRST_EH2_VERTEX_MISMATCH_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "BUP3838_0_EH2_update",
            "observable": "B_EH2_vertex",
            "formula": "B_EH2_vertex <= B_L2_operator + B_grav_energy_source + B_field_redef_gauge + B_nonEH2_operator",
            "new_detail": "core S_beta term now has second-variation audit components",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BUP3838_1_beta_total",
            "observable": "beta-1",
            "formula": "abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)",
            "new_detail": "beta total remains blocked because EH2 vertex match is not parent-signed",
            "status": "NONCLAIM_BETA_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3838_0_first_order_guard",
            "gate": "first-order Poisson not promoted to beta",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "3818 remains first-order only; beta requires second variation",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3838_1_EH2_match",
            "gate": "EH2 parent second-variation match",
            "status": "BLOCKED_PARENT_SECOND_VARIATION_REQUIRED",
            "claim_allowed": False,
            "reason": "no parent action second-variation artifact proves the EH quadratic vertex",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3838_2_EH2_bound",
            "gate": "EH2 mismatch bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "B_EH2_vertex bound formula exists but no numeric/source-backed rows exist",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3838_3_beta_claim",
            "gate": "beta/local PPN claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "EH2, extra scalar2, boundary2, readout2, and eps_temporal4 rows are not source-backed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3838_4_next_target",
            "gate": "next target attacks extra scalar2",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "EH2 mismatch is formulated; next S_beta component is extra scalar quadratic self-energy",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3838_0_no_first_order_smuggle",
            "decision": "do not infer beta from the first-order EH/Poisson bridge",
            "basis": "3818 proves linear Poisson normalization only",
            "consequence": "MTS needs an actual second-order parent action or a finite beta bound",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3838_1_EH2_not_closed",
            "decision": "retain B_EH2_vertex as formula-only nonclaim",
            "basis": "no parent second variation artifact currently signs the EH quadratic vertex",
            "consequence": "beta remains blocked but now has an actionable second-variation ledger",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3838_2_next_Sbeta_component",
            "decision": "move next to extra scalar quadratic self-energy",
            "basis": "S_EH2_mismatch has a ledger; S_extra_scalar2 is the next unresolved S_beta component",
            "consequence": "3839 should try to exclude or bound extra scalar2 in visible g00",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3838_0",
            "next_checkpoint": "3839-Y5-R2FR-extra-scalar-quadratic-self-energy-zero-or-beta-bound.md",
            "script": "scripts/Y5_R2FR_3839_extra_scalar_quadratic_self_energy_zero_or_beta_bound.py",
            "objective": "try to prove no extra scalar quadratic self-energy contributes to visible g00 at beta order, or retain/source-bound S_extra_scalar2",
            "reason": "3838 formulates the EH2 vertex mismatch ledger; the next S_beta component is extra scalar2",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EH2_VERTEX_MISMATCH_BOUND",
            "claim": "no beta/local-GR claim",
            "summary": "3838 guards against first-order-to-beta smuggling and decomposes the EH2 parent second-variation mismatch into source-bound components.",
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


def write_doc(sources, vertex_audit, mismatch, beta_update, gates, decisions, timestamp: str) -> None:
    text = f"""# 3838 — EH2 Parent Second Variation Vertex Match Or Beta Bound

Private checkpoint. This tests the core beta question: whether the parent action really supplies the GR/EH second-order 00 vertex. It does not claim `beta=1`.

Generated: `{timestamp}`

## Result

3838 blocks the bad shortcut:

`first-order Poisson normalization != second-order beta self-coupling`.

The EH2 mismatch is now:

`B_EH2_vertex <= B_L2_operator + B_grav_energy_source + B_field_redef_gauge + B_nonEH2_operator`.

Therefore:

`abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + abs(eps_temporal4/Phi^2)`.

Current result: the EH2 route is formulated, not closed. A parent second-variation artifact is still required.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## EH2 Vertex Match Audit

{markdown_table(vertex_audit, ["audit_id", "requirement", "test", "current_status", "if_failed"])}

## EH2 Mismatch Decomposition

{markdown_table(mismatch, ["component_id", "component", "definition", "zero_route", "status"])}

## Beta Bound Update

{markdown_table(beta_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is the right kind of discipline: beta cannot be inherited from Newton. MTS must either show the parent second variation really reproduces the EH quadratic vertex, or carry `B_EH2_vertex` as a beta residual.

Next target: `3839-Y5-R2FR-extra-scalar-quadratic-self-energy-zero-or-beta-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3837", "Current State After 3838", 1)
    paragraph = (
        "`3838` blocks first-order-to-beta smuggling: the 3818 Poisson bridge is linear only. "
        "The EH2 mismatch is now `B_EH2_vertex <= B_L2_operator+B_grav_energy_source+B_field_redef_gauge+B_nonEH2_operator`, "
        "so `|beta-1| <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+|eps_temporal4/Phi^2|`. "
        "No beta claim is made because no parent second-variation artifact currently signs the EH quadratic vertex.\n\n"
    )
    anchor = "`3837` starts"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md`

Target: test whether the parent second variation matches the GR/EH quadratic 00 vertex after Poisson normalization, or retain/source-bound `S_EH2_mismatch`.

This is the best next move because 3837 decomposes `S_beta` and shows `S_EH2_mismatch` is the core beta/local-GR derivation target."""
    new_gate = """`3839-Y5-R2FR-extra-scalar-quadratic-self-energy-zero-or-beta-bound.md`

Target: try to prove no extra scalar quadratic self-energy contributes to visible `g00` at beta order, or retain/source-bound `S_extra_scalar2`.

This is the best next move because 3838 formulates the EH2 vertex mismatch ledger; the next `S_beta` component is extra scalar2."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3838_EH2_VERTEX_MATCH_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3838_EH2_MISMATCH_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3838_BETA_BOUND_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3838_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3838_EH2_VERTEX_MATCH_AUDIT.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3838 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3838 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, vertex_audit, mismatch, beta_update, gates, timestamp: str):
    rows = []

    def add(check_id, check, passed, detail):
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in vertex_audit + mismatch + beta_update + gates)
    add("VAL3838_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3838_1_first_order_guard", "first-order Poisson is not promoted to beta", "first-order Poisson/EH bridge cannot be promoted to beta" in all_text and any(row["gate_id"] == "GATE3838_0_first_order_guard" for row in gates), "first-order guard present")
    add("VAL3838_2_mismatch_components", "EH2 mismatch components are decomposed", all(token in all_text for token in ["B_L2_operator", "B_grav_energy_source", "B_field_redef_gauge", "B_nonEH2_operator", "B_EH2_vertex"]), "EH2 component tokens present")
    add("VAL3838_3_nonclaim", "all 3838 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in vertex_audit + mismatch + beta_update + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3838_4_EH2_blocked", "EH2 match remains blocked", any(row["gate_id"] == "GATE3838_1_EH2_match" and row["status"].startswith("BLOCKED") for row in gates), "EH2 gate blocked")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3838_5_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3838_6_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "first-order Poisson normalization" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3838*", "P8_Y5_BRR545_3838*", "*Y5_R2FR_3838*", "3838-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3838_7_formalization_clean", "formalization-workbench has no 3838 files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3838 file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3838_8_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    vertex_audit = vertex_audit_rows(timestamp)
    mismatch = mismatch_rows(timestamp)
    beta_update = beta_update_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["vertex_audit"], vertex_audit)
    write_csv(OUTPUTS["mismatch"], mismatch)
    write_csv(OUTPUTS["beta_update"], beta_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, vertex_audit, mismatch, beta_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, vertex_audit, mismatch, beta_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_EH2_VERTEX_MISMATCH_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
