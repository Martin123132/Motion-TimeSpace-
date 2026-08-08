from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3836"
BRANCH = "MTS_R2FR_Y5_DIRECT_GAMMA_READOUT_EPS_SPATIAL_ZERO_OR_SOURCE_BOUND_3836"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3836-Y5-R2FR-direct-gamma-readout-eps-spatial-zero-or-source-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3835 = PCW / "3835-Y5-R2FR-integrated-gamma-no-slip-ledger-and-first-threshold-dashboard.md"
CSV_3835_LEDGER = OUT / "P8_Y5_R2FR_3835_GAMMA_NO_SLIP_LEDGER.csv"
CSV_3835_DASH = OUT / "P8_Y5_R2FR_3835_GAMMA_THRESHOLD_DASHBOARD.csv"
CSV_3835_VALIDATION = OUT / "P8_Y5_BRR545_3835_VALIDATION.csv"
CSV_3828_ANSATZ = OUT / "P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv"
CSV_3828_RESIDUAL = OUT / "P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv"
CSV_3828_GATES = OUT / "P8_Y5_R2FR_3828_LOCAL_GR_READOUT_CLAUSE_GATES.csv"
CSV_3827_PPN = OUT / "P8_Y5_R2FR_3827_PPN_READOUT_TAIL_FIRST_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3836_SOURCE_REGISTER.csv",
    "readout": OUT / "P8_Y5_R2FR_3836_DIRECT_GAMMA_READOUT_DECOMPOSITION.csv",
    "eps": OUT / "P8_Y5_R2FR_3836_EPS_SPATIAL_ZERO_OR_BOUND_ROWS.csv",
    "gamma_update": OUT / "P8_Y5_R2FR_3836_GAMMA_LEDGER_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3836_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3836_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3836_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3836_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3836_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3836_0_3835_doc", P_3835, "Integrated Gamma No-Slip Ledger And First Threshold Dashboard"),
    ("SRC3836_1_3835_ledger", CSV_3835_LEDGER, "GLED3835_3_readout_direct"),
    ("SRC3836_2_3835_dashboard", CSV_3835_DASH, "GDASH3835_2_pass_rule"),
    ("SRC3836_3_3835_validation", CSV_3835_VALIDATION, "VAL3835_5_next_gap"),
    ("SRC3836_4_3828_ansatz", CSV_3828_ANSATZ, "ANS3828_1_spatial_curvature"),
    ("SRC3836_5_3828_residual", CSV_3828_RESIDUAL, "RPPN3828_0_gamma"),
    ("SRC3836_6_3828_readout_gates", CSV_3828_GATES, "RGATE3828_0_gamma"),
    ("SRC3836_7_3827_ppn_first_rows", CSV_3827_PPN, "PPN3827_0_gamma_minus_one"),
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
                "role": "input_for_direct_gamma_readout_eps_spatial_zero_or_bound",
                "claim_use": "readout_tail_bound_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def readout_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "DGR3836_0_metric_projection",
            "component": "B_metric_projection",
            "definition": "mismatch between parent spatial metric perturbation and the PPN isotropic gamma projection",
            "zero_route": "single metric readout plus declared PPN gauge/projection maps h_ij -> 2 gamma Phi delta_ij without residual TF/scalar leakage",
            "bound_formula": "B_metric_projection <= norm(P_gamma_perp h_ij)/(abs(Phi))",
            "status": "PROJECTION_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "DGR3836_1_arena_readout_tail",
            "component": "B_arena_readout_tail",
            "definition": "arena-specific extraction, calibration, or fit-window tail that changes the gamma readout",
            "zero_route": "one fixed readout map before arena fitting; no post-fit gamma extraction coefficient",
            "bound_formula": "B_arena_readout_tail <= abs(R_gamma_arena_window)",
            "status": "ARENA_READOUT_SOURCE_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "DGR3836_2_clock_or_PPN_projection",
            "component": "B_clock_or_PPN_projection",
            "definition": "mismatch between clock/redshift, orbital, and PPN spatial readout projections when used together",
            "zero_route": "clock/orbital/PPN projections are all induced by the same metric source readout",
            "bound_formula": "B_clock_or_PPN_projection <= abs(C_tau/C_t-1) + abs(C_acc/C_t-1) projected into gamma channel",
            "status": "CROSS_READOUT_LOCK_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "DGR3836_3_total",
            "component": "B_gamma_readout",
            "definition": "direct gamma readout residual not already counted as matter, parent-extra, or boundary slip",
            "zero_route": "all direct readout projection tails vanish on the fixed local PPN map",
            "bound_formula": "B_gamma_readout <= B_metric_projection + B_arena_readout_tail + B_clock_or_PPN_projection",
            "status": "FIRST_DIRECT_GAMMA_READOUT_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def eps_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "EPS3836_0_higher_multipole",
            "component": "B_eps_multipole",
            "definition": "l>=2/tidal spatial metric residue not included in the scalar C_s Phi term",
            "zero_route": "monopole/local-isotropic projection or multipole term outside claimed PPN order",
            "bound_formula": "B_eps_multipole <= norm(h_ij^l>=2)/(abs(Phi))",
            "status": "MULTIPOLE_SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EPS3836_1_gauge_tail",
            "component": "B_eps_gauge",
            "definition": "coordinate/gauge residue in spatial metric after choosing the PPN readout gauge",
            "zero_route": "fixed PPN gauge and gauge-invariant gamma extraction",
            "bound_formula": "B_eps_gauge <= norm(L_xi g_ij)_scalar/abs(Phi)",
            "status": "GAUGE_FIX_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EPS3836_2_finite_domain",
            "component": "B_eps_domain",
            "definition": "finite-radius/exterior-domain correction in the spatial potential expansion",
            "zero_route": "asymptotic/local exterior domain limit or source-backed finite-domain correction",
            "bound_formula": "B_eps_domain <= abs(R_domain_spatial/Phi)",
            "status": "DOMAIN_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EPS3836_3_nonlinear_cross",
            "component": "B_eps_nonlinear",
            "definition": "higher-order potential or cross-sector term leaking into the linear gamma readout",
            "zero_route": "linear PPN order projection and higher-order terms assigned to beta/second-order branch",
            "bound_formula": "B_eps_nonlinear <= O(Phi) + cross_sector_tail",
            "status": "ORDER_SEPARATION_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "EPS3836_4_total",
            "component": "abs(eps_spatial/Phi)",
            "definition": "total residual spatial-metric readout tail outside C_s Phi",
            "zero_route": "all eps_spatial components vanish or are below gamma threshold budget",
            "bound_formula": "abs(eps_spatial/Phi) <= B_eps_multipole + B_eps_gauge + B_eps_domain + B_eps_nonlinear",
            "status": "FIRST_EPS_SPATIAL_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gamma_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "GUP3836_0_readout_update",
            "observable": "B_gamma_readout",
            "formula": "B_gamma_readout <= B_metric_projection + B_arena_readout_tail + B_clock_or_PPN_projection",
            "new_detail": "direct gamma readout placeholder from 3835 is now decomposed",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GUP3836_1_eps_update",
            "observable": "abs(eps_spatial/Phi)",
            "formula": "abs(eps_spatial/Phi) <= B_eps_multipole + B_eps_gauge + B_eps_domain + B_eps_nonlinear",
            "new_detail": "spatial residual placeholder from 3828/3835 is now decomposed",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GUP3836_2_gamma_total_update",
            "observable": "gamma-1",
            "formula": "abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)",
            "new_detail": "all five top-level gamma terms now have decomposition rows; numeric/source validity still missing",
            "status": "STRUCTURALLY_COMPLETE_NONCLAIM_GAMMA_LEDGER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3836_0_readout_decomposed",
            "gate": "direct gamma readout residual decomposed",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "B_gamma_readout now has metric, arena, and cross-readout components",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3836_1_eps_decomposed",
            "gate": "eps_spatial/Phi residual decomposed",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "eps_spatial now has multipole, gauge, domain, and nonlinear components",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3836_2_gamma_claim",
            "gate": "gamma/no-slip claim",
            "status": "BLOCKED_SOURCE_AND_THRESHOLD_REQUIRED",
            "claim_allowed": False,
            "reason": "gamma ledger is structurally complete but lacks source-backed numeric component values and threshold",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3836_3_local_GR_claim",
            "gate": "local GR claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "gamma is nonclaim and beta S_beta branch remains open",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3836_4_next_target",
            "gate": "next target returns to beta second-order vertex",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "gamma ledger is structurally complete; beta is the next major PPN/local-GR gap",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3836_0_gamma_formula_complete",
            "decision": "treat gamma/no-slip as structurally complete but numerically/source blocked",
            "basis": "all top-level terms now have decomposition or bound rows",
            "consequence": "do not add more gamma prose until source rows or threshold acquisition are attempted",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3836_1_no_gamma_claim",
            "decision": "do not claim gamma or local GR",
            "basis": "no component row is source-backed numeric and theta_gamma_local remains missing",
            "consequence": "gamma can be tested only as a blocked dashboard for now",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3836_2_return_to_beta",
            "decision": "return to beta/S_beta derivation next",
            "basis": "local GR needs both gamma and beta; gamma now has an integrated ledger while beta remains at the 3829 residual stage",
            "consequence": "3837 should attack the second-order EH vertex/self-coupling route",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3836_0",
            "next_checkpoint": "3837-Y5-R2FR-beta-second-order-vertex-Sbeta-zero-or-bound.md",
            "script": "scripts/Y5_R2FR_3837_beta_second_order_vertex_Sbeta_zero_or_bound.py",
            "objective": "derive or source-bound S_beta in B_t=C_t^2+S_beta, separating EH second-order vertex mismatch, extra scalar self-energy, boundary2, and readout2 terms",
            "reason": "3836 makes gamma structurally complete but nonclaim; beta is now the main undeveloped PPN/local-GR branch",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_DIRECT_GAMMA_READOUT_EPS_BOUND",
            "claim": "no gamma/no-slip/local-GR claim",
            "summary": "3836 decomposes direct gamma readout and eps_spatial residuals, making the gamma ledger structurally complete but still numeric/source blocked.",
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


def write_doc(sources, readout, eps, gamma_update, gates, decisions, timestamp: str) -> None:
    text = f"""# 3836 — Direct Gamma Readout eps_spatial Zero Or Source Bound

Private checkpoint. This decomposes the last placeholder gamma components from 3835. It does not claim `gamma=1`.

Generated: `{timestamp}`

## Result

The direct readout residual is now:

`B_gamma_readout <= B_metric_projection + B_arena_readout_tail + B_clock_or_PPN_projection`.

The residual spatial tail is now:

`abs(eps_spatial/Phi) <= B_eps_multipole + B_eps_gauge + B_eps_domain + B_eps_nonlinear`.

Therefore the gamma ledger is structurally complete:

`abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)`.

It is still not claimable because the component rows and the gamma threshold are not source-backed numeric rows.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Direct Gamma Readout Decomposition

{markdown_table(readout, ["component_id", "component", "definition", "zero_route", "status"])}

## eps_spatial Zero Or Bound Rows

{markdown_table(eps, ["component_id", "component", "definition", "zero_route", "status"])}

## Gamma Ledger Update

{markdown_table(gamma_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

Gamma is now in the best state it has been in: structurally complete, nonclaim, and ready for source-filling/threshold work. For local GR, the next mathematical gap is `beta`, specifically the second-order vertex residual `S_beta`.

Next target: `3837-Y5-R2FR-beta-second-order-vertex-Sbeta-zero-or-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3835", "Current State After 3836", 1)
    paragraph = (
        "`3836` decomposes the last placeholder gamma terms. "
        "`B_gamma_readout <= B_metric_projection+B_arena_readout_tail+B_clock_or_PPN_projection`, and "
        "`|eps_spatial/Phi| <= B_eps_multipole+B_eps_gauge+B_eps_domain+B_eps_nonlinear`. "
        "The gamma/no-slip ledger is now structurally complete but still nonclaim because no component bounds or local gamma threshold are source-backed numeric rows. The next major PPN gap is beta/`S_beta`.\n\n"
    )
    anchor = "`3835` integrates"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3836-Y5-R2FR-direct-gamma-readout-eps-spatial-zero-or-source-bound.md`

Target: derive or source-bound `B_gamma_readout` and `eps_spatial/Phi`, the remaining direct spatial/readout gamma residuals in the integrated no-slip ledger.

This is the best next move because 3835 integrates the gamma ledger and shows direct readout/`eps_spatial` rows are the least developed remaining gamma components."""
    new_gate = """`3837-Y5-R2FR-beta-second-order-vertex-Sbeta-zero-or-bound.md`

Target: derive or source-bound `S_beta` in `B_t=C_t^2+S_beta`, separating EH second-order vertex mismatch, extra scalar self-energy, boundary2, and readout2 terms.

This is the best next move because 3836 makes gamma structurally complete but nonclaim; beta is now the main undeveloped PPN/local-GR branch."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3836_DIRECT_GAMMA_READOUT_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3836_EPS_SPATIAL_ZERO_OR_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3836_GAMMA_LEDGER_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3836_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3836_DIRECT_GAMMA_READOUT_DECOMPOSITION.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3836 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3836 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, readout, eps, gamma_update, gates, timestamp: str):
    rows = []

    def add(check_id, check, passed, detail):
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in readout + eps + gamma_update + gates)
    add("VAL3836_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3836_1_readout_components", "direct gamma readout components are decomposed", all(token in all_text for token in ["B_metric_projection", "B_arena_readout_tail", "B_clock_or_PPN_projection", "B_gamma_readout"]), "direct readout tokens present")
    add("VAL3836_2_eps_components", "eps_spatial components are decomposed", all(token in all_text for token in ["B_eps_multipole", "B_eps_gauge", "B_eps_domain", "B_eps_nonlinear", "eps_spatial/Phi"]), "eps tokens present")
    add("VAL3836_3_nonclaim", "all 3836 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in readout + eps + gamma_update + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3836_4_gamma_blocked", "gamma claim remains blocked", any(row["gate_id"] == "GATE3836_2_gamma_claim" and row["status"].startswith("BLOCKED") for row in gates), "gamma gate blocked")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3836_5_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3836_6_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "S_beta" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3836*", "P8_Y5_BRR545_3836*", "*Y5_R2FR_3836*", "3836-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3836_7_formalization_clean", "formalization-workbench has no 3836 files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3836 file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3836_8_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    readout = readout_rows(timestamp)
    eps = eps_rows(timestamp)
    gamma_update = gamma_update_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["readout"], readout)
    write_csv(OUTPUTS["eps"], eps)
    write_csv(OUTPUTS["gamma_update"], gamma_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, readout, eps, gamma_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, readout, eps, gamma_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_DIRECT_GAMMA_READOUT_EPS_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
