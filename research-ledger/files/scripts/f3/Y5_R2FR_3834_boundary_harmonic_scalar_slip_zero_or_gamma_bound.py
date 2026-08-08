from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3834"
BRANCH = "MTS_R2FR_Y5_BOUNDARY_HARMONIC_SCALAR_SLIP_ZERO_OR_GAMMA_BOUND_3834"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3833 = PCW / "3833-Y5-R2FR-parent-extra-scalar-slip-readout-naturality-or-bound.md"
CSV_3833_BOUNDS = OUT / "P8_Y5_R2FR_3833_PARENT_EXTRA_GAMMA_BOUND_ROWS.csv"
CSV_3833_VALIDATION = OUT / "P8_Y5_BRR545_3833_VALIDATION.csv"
CSV_3830_DECOMP = OUT / "P8_Y5_R2FR_3830_SLIP_SOURCE_DECOMPOSITION.csv"
CSV_3830_OPERATOR = OUT / "P8_Y5_R2FR_3830_NO_SLIP_OPERATOR_THEOREM.csv"
CSV_3825_BOUNDARY = OUT / "P8_Y5_R2FR_3825_BOUNDARY_REFERENCE_ZERO_THEOREM.csv"
CSV_3825_FIRST = OUT / "P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv"
CSV_3825_RESID = OUT / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3834_SOURCE_REGISTER.csv",
    "elliptic": OUT / "P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv",
    "components": OUT / "P8_Y5_R2FR_3834_BOUNDARY_SLIP_COMPONENTS.csv",
    "bounds": OUT / "P8_Y5_R2FR_3834_BOUNDARY_GAMMA_BOUND_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3834_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3834_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3834_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3834_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3834_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3834_0_3833_doc", P_3833, "Parent-Extra Scalar Slip Readout Naturality Or Bound"),
    ("SRC3834_1_3833_bounds", CSV_3833_BOUNDS, "PGB3833_1_gamma_total_update"),
    ("SRC3834_2_3833_validation", CSV_3833_VALIDATION, "VAL3833_2_components"),
    ("SRC3834_3_3830_decomp", CSV_3830_DECOMP, "SLIP3830_2_boundary_harmonic"),
    ("SRC3834_4_3830_operator", CSV_3830_OPERATOR, "NS3830_1_traceless_ij_operator"),
    ("SRC3834_5_3825_boundary", CSV_3825_BOUNDARY, "BRT3825_2_B_zero_flux_zero"),
    ("SRC3834_6_3825_first", CSV_3825_FIRST, "FSR3825_0_B_zero_flux"),
    ("SRC3834_7_3825_resid", CSV_3825_RESID, "R3825_4_total"),
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
                "role": "input_for_boundary_harmonic_scalar_slip_zero_or_gamma_bound",
                "claim_use": "elliptic_boundary_zero_and_bound_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def elliptic_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "BH3834_0_elliptic_uniqueness",
            "statement": "If the no-slip source vanishes and the scalar slip has silent boundary/harmonic data, elliptic uniqueness kills the homogeneous slip mode.",
            "formula": "D_TF[S]=0, S|boundary=0, H_l>=2=0 => S=0",
            "required_signature": "fixed exterior annulus; boundary/reference lock; no cohomological/harmonic scalar slip mode",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "BH3834_1_3825_specialization",
            "statement": "The 3825 B_zero_flux/Delta_symp route can support no-slip only if it applies to scalar slip boundary data, not just generic charge drift.",
            "formula": "Sigma_TF_boundary -> B_zero_flux^slip + Delta_symp^slip + H_slip",
            "required_signature": "scalar-slip-specific boundary row with source path and units",
            "status": "SPECIALIZATION_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "BH3834_2_bound_contract",
            "statement": "Without scalar-slip boundary signatures, boundary/harmonic slip is a finite gamma-bound component.",
            "formula": "B_gamma_boundary <= B_Dirichlet_slip + B_Neumann_slip + B_harmonic_l2 + B_Bzero_flux_slip + B_Delta_symp_slip",
            "required_signature": "source-backed boundary amplitudes or theorem-zero rows",
            "status": "FIRST_BOUND_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def component_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "BC3834_0_Dirichlet",
            "component": "B_Dirichlet_slip",
            "definition": "scalar slip value fixed on the exterior boundary/reference surface",
            "zero_route": "S|boundary=0 from reference lock",
            "bound_formula": "B_Dirichlet_slip <= sup_boundary abs(S/Phi)",
            "status": "SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BC3834_1_Neumann",
            "component": "B_Neumann_slip",
            "definition": "normal derivative or flux of scalar slip through the exterior boundary",
            "zero_route": "normal slip flux zero by Stokes/fixed boundary data",
            "bound_formula": "B_Neumann_slip <= sup_boundary abs(n.grad S/Phi)",
            "status": "SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BC3834_2_harmonic",
            "component": "B_harmonic_l2",
            "definition": "homogeneous l>=2 harmonic scalar slip mode on the exterior annulus",
            "zero_route": "cohomologically trivial/no harmonic scalar slip class",
            "bound_formula": "B_harmonic_l2 <= sum_l>=2 abs(a_lm^slip)/abs(Phi)",
            "status": "HARMONIC_CLASS_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BC3834_3_Bzero",
            "component": "B_Bzero_flux_slip",
            "definition": "scalar-slip specialization of 3825 B_zero_flux",
            "zero_route": "B_zero_flux=0 applies to scalar slip mode",
            "bound_formula": "B_Bzero_flux_slip <= abs(B_zero_flux^slip/Phi)",
            "status": "SPECIALIZED_3825_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "BC3834_4_Delta_symp",
            "component": "B_Delta_symp_slip",
            "definition": "scalar-slip reference/symplectic drift from fixed exterior projector",
            "zero_route": "Delta_symp=0 applies to scalar slip reference data",
            "bound_formula": "B_Delta_symp_slip <= abs(Delta_symp^slip/Phi)",
            "status": "SPECIALIZED_3825_ROW_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BGB3834_0_boundary",
            "observable": "B_gamma_boundary",
            "formula": "B_gamma_boundary <= B_Dirichlet_slip + B_Neumann_slip + B_harmonic_l2 + B_Bzero_flux_slip + B_Delta_symp_slip",
            "needed_for_claim": "scalar-slip-specific boundary/reference zero or numeric source-backed bounds",
            "status": "FIRST_BOUNDARY_GAMMA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BGB3834_1_gamma_total_update",
            "observable": "gamma-1",
            "formula": "abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)",
            "needed_for_claim": "matter/EM, parent-extra, boundary, readout, and eps_spatial rows",
            "status": "UPDATED_GAMMA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3834_0_elliptic_route",
            "gate": "elliptic boundary zero route",
            "status": "PASS_CONDITIONAL_ZERO_ROUTE",
            "claim_allowed": False,
            "reason": "D_TF[S]=0 plus silent boundary/harmonic data would kill scalar slip",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3834_1_boundary_zero",
            "gate": "Sigma_TF_boundary zero claim",
            "status": "BLOCKED_SPECIALIZED_BOUNDARY_ROW_REQUIRED",
            "claim_allowed": False,
            "reason": "3825 is generic boundary machinery; scalar-slip-specific boundary rows are not claim-valid",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3834_2_boundary_bound",
            "gate": "boundary gamma bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "boundary/harmonic gamma bound exists but lacks numeric/source-backed rows",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3834_3_gamma",
            "gate": "gamma/no-slip claim",
            "status": "BLOCKED_REFINED_LEDGER_ONLY",
            "claim_allowed": False,
            "reason": "gamma ledger is structured but not source/numeric closed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3834_4_next_target",
            "gate": "next target integrates gamma ledger",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "major gamma components now have bound rows; next step is an integrated threshold/dashboard gate",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3834_0_boundary_specialization_needed",
            "decision": "do not reuse generic 3825 boundary-zero as scalar no-slip proof without specialization",
            "basis": "gamma needs scalar-slip boundary/harmonic silence, not only generic boundary charge drift",
            "consequence": "boundary contributes a finite gamma-bound row until scalar-slip rows are signed",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3834_1_gamma_ledger_ready",
            "decision": "gamma ledger is now structurally ready for integration",
            "basis": "matter/EM, parent-extra, and boundary components all have explicit nonclaim bound rows",
            "consequence": "3835 can build a no-slip dashboard and first threshold placeholders",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3834_0",
            "next_checkpoint": "3835-Y5-R2FR-integrated-gamma-no-slip-ledger-and-first-threshold-dashboard.md",
            "script": "scripts/Y5_R2FR_3835_integrated_gamma_no_slip_ledger_and_first_threshold_dashboard.py",
            "objective": "integrate matter/EM, parent-extra, boundary, readout, and eps_spatial gamma rows into one no-slip ledger with source/numeric thresholds and claim-blocked local test status",
            "reason": "3834 gives the last major boundary/harmonic gamma bound component; the project needs one integrated gamma dashboard before more local tests",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_BOUNDARY_HARMONIC_SLIP_BOUND",
            "claim": "no gamma/no-slip/local-GR claim",
            "summary": "3834 specializes the 3825 boundary route to scalar slip, blocks generic reuse, and emits boundary/harmonic gamma-bound rows.",
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


def write_doc(sources, elliptic, components, bounds, gates, decisions, timestamp: str) -> None:
    text = f"""# 3834 — Boundary/Harmonic Scalar Slip Zero Or Gamma Bound

Private checkpoint. This specializes the 3825 boundary/reference route to scalar no-slip. It does not claim `gamma=1`.

Generated: `{timestamp}`

## Result

3834 says exactly when the boundary route can kill scalar slip:

`D_TF[S]=0, S|boundary=0, H_l>=2=0 => S=0`.

But the current corpus does not yet contain scalar-slip-specific boundary rows. Therefore the boundary contribution is:

`B_gamma_boundary <= B_Dirichlet_slip + B_Neumann_slip + B_harmonic_l2 + B_Bzero_flux_slip + B_Delta_symp_slip`.

This blocks a bad shortcut: generic `B_zero_flux=0` is not automatically a no-slip proof.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Elliptic Boundary Zero Theorem

{markdown_table(elliptic, ["theorem_id", "statement", "formula", "status"])}

## Boundary Slip Components

{markdown_table(components, ["component_id", "component", "definition", "zero_route", "status"])}

## Boundary Gamma Bounds

{markdown_table(bounds, ["bound_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

The gamma/no-slip branch now has its boundary component in the right form. This is not victory yet, but it is a clean engineering drawing: every major gamma leak has a named zero route or a bound row.

Next target: `3835-Y5-R2FR-integrated-gamma-no-slip-ledger-and-first-threshold-dashboard.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3833", "Current State After 3834", 1)
    paragraph = (
        "`3834` specializes the 3825 boundary/reference route to scalar no-slip. The elliptic route is "
        "`D_TF[S]=0, S|boundary=0, H_l>=2=0 => S=0`, but generic `B_zero_flux=0` is not automatically a scalar-slip proof. "
        "The emitted nonclaim bound is `B_gamma_boundary <= B_Dirichlet_slip+B_Neumann_slip+B_harmonic_l2+B_Bzero_flux_slip+B_Delta_symp_slip`.\n\n"
    )
    anchor = "`3833` converts"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md`

Target: try to prove `Sigma_TF_boundary=0` for scalar slip using the 3825 boundary/reference route and elliptic uniqueness, or emit a boundary/harmonic gamma bound row.

This is the best next move because 3833 formulates parent-extra/readout slip; the next remaining no-slip source is boundary/harmonic scalar slip."""
    new_gate = """`3835-Y5-R2FR-integrated-gamma-no-slip-ledger-and-first-threshold-dashboard.md`

Target: integrate matter/EM, parent-extra, boundary, readout, and `eps_spatial` gamma rows into one no-slip ledger with source/numeric thresholds and claim-blocked local test status.

This is the best next move because 3834 gives the last major boundary/harmonic gamma bound component; the project needs one integrated gamma dashboard before more local tests."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3834_BOUNDARY_HARMONIC_ELLIPTIC_ZERO_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3834_BOUNDARY_SLIP_COMPONENTS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3834_BOUNDARY_GAMMA_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3834_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3834_BOUNDARY_GAMMA_BOUND_ROWS.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3834 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3834 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, elliptic, components, bounds, gates, timestamp: str):
    rows = []

    def add(check_id, check, passed, detail):
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in elliptic + components + bounds + gates)
    add("VAL3834_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3834_1_elliptic", "elliptic scalar-slip boundary zero route is present", all(token in all_text for token in ["D_TF[S]=0", "H_l>=2", "S=0"]), "elliptic zero tokens present")
    add("VAL3834_2_components", "boundary gamma components are decomposed", all(token in all_text for token in ["B_Dirichlet_slip", "B_Neumann_slip", "B_harmonic_l2", "B_Bzero_flux_slip", "B_Delta_symp_slip"]), "five boundary components present")
    add("VAL3834_3_nonclaim", "all 3834 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in elliptic + components + bounds + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3834_4_zero_blocked", "boundary zero claim remains blocked", any(row["gate_id"] == "GATE3834_1_boundary_zero" and row["status"].startswith("BLOCKED") for row in gates), "boundary zero blocked")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3834_5_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3834_6_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "B_gamma_boundary" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3834*", "P8_Y5_BRR545_3834*", "*Y5_R2FR_3834*", "3834-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3834_7_formalization_clean", "formalization-workbench has no 3834 files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3834 file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3834_8_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    elliptic = elliptic_rows(timestamp)
    components = component_rows(timestamp)
    bounds = bound_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["elliptic"], elliptic)
    write_csv(OUTPUTS["components"], components)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, elliptic, components, bounds, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, elliptic, components, bounds, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_BOUNDARY_HARMONIC_SLIP_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
