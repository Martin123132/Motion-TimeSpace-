from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3833"
BRANCH = "MTS_R2FR_Y5_PARENT_EXTRA_SCALAR_SLIP_READOUT_NATURALITY_OR_BOUND_3833"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3833-Y5-R2FR-parent-extra-scalar-slip-readout-naturality-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3832 = PCW / "3832-Y5-R2FR-tensor-virial-TF-stress-and-EM-Poynting-separation-or-bound.md"
CSV_3832_GAMMA = OUT / "P8_Y5_R2FR_3832_GAMMA_BOUND_UPDATE.csv"
CSV_3832_VALIDATION = OUT / "P8_Y5_BRR545_3832_VALIDATION.csv"
CSV_3830_DECOMP = OUT / "P8_Y5_R2FR_3830_SLIP_SOURCE_DECOMPOSITION.csv"
CSV_3808_OBSREP = OUT / "P8_Y5_R2FR_3808_OBSREP_TYPE_SYSTEM_THEOREM.csv"
CSV_3810_CONTRACT = OUT / "P8_Y5_R2FR_3810_PARENT_OWNED_ZQEFF_READOUT_CONTRACT.csv"
CSV_3811_MORPHISM = OUT / "P8_Y5_R2FR_3811_MORPHISM_BAN_DERIVATION_AUDIT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3833_SOURCE_REGISTER.csv",
    "naturality": OUT / "P8_Y5_R2FR_3833_READOUT_NATURALITY_THEOREM.csv",
    "parent_extra": OUT / "P8_Y5_R2FR_3833_PARENT_EXTRA_SLIP_DECOMPOSITION.csv",
    "bounds": OUT / "P8_Y5_R2FR_3833_PARENT_EXTRA_GAMMA_BOUND_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3833_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3833_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3833_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3833_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3833_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3833_0_3832_doc", P_3832, "Tensor-Virial TF Stress And EM/Poynting Separation Or Bound"),
    ("SRC3833_1_3832_gamma", CSV_3832_GAMMA, "GUP3832_1_gamma_total"),
    ("SRC3833_2_3832_validation", CSV_3832_VALIDATION, "VAL3832_1_separation"),
    ("SRC3833_3_3830_decomp", CSV_3830_DECOMP, "SLIP3830_1_parent_extra_scalar"),
    ("SRC3833_4_3808_obsrep", CSV_3808_OBSREP, "ORT3808_2_chain_rule"),
    ("SRC3833_5_3810_contract", CSV_3810_CONTRACT, "POC3810_3_no_hidden_visible_coefficients"),
    ("SRC3833_6_3811_morphism", CSV_3811_MORPHISM, "MB3811_2_scalar_countermodel"),
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
    rows: list[dict[str, object]] = []
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
                "role": "input_for_parent_extra_scalar_slip_readout_naturality_or_bound",
                "claim_use": "type_theorem_and_bound_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def naturality_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "RN3833_0_chain_rule_zero",
            "statement": "If the observed metric readout descends through the same q_obs-owned ObsRep data, vertical hidden variations cannot change the scalar readout coefficients.",
            "formula": "D_v g_obs = D gbar_obs[D_v ObsRep] = 0 for v in ker(Dq_obs)",
            "zero_condition": "D_v ObsRep=0 and no hidden-visible coefficient/readout morphism",
            "status": "EXACT_CONDITIONAL_FROM_3808_3811",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "RN3833_1_single_metric_scalar_lock",
            "statement": "A single parent metric/readout with no extra scalar morphism gives one scalar potential in the local exterior metric.",
            "formula": "g00=-1+2 C_t Phi+... and gij=delta_ij(1+2 C_s Phi)+... with C_s-C_t sourced only by nonnatural readout/morphism terms",
            "zero_condition": "single metric readout; no Weyl/disformal representative coefficient; no hidden scalar slot in C_s or C_t",
            "status": "CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "RN3833_2_countermodel_retained",
            "statement": "If a hidden scalar can enter visible metric/readout coefficients, parent-extra slip is legal and gamma is not protected.",
            "formula": "C_s-C_t = a_dis I_hid + a_rep I_hid + ...",
            "zero_condition": "hidden invariant algebra is typed out of visible scalar/readout coefficient slots",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "RN3833_3_bound_contract",
            "statement": "Absent a parent signature, Sigma_TF_parent_extra is a finite gamma-bound component.",
            "formula": "B_gamma_parent_extra <= B_disformal_slip + B_hidden_coeff_slip + B_readout_rep_slip + B_parent_metric_nonuniqueness",
            "zero_condition": "all four bound components vanish or are source-bounded below threshold",
            "status": "FIRST_PARENT_EXTRA_BOUND_CONTRACT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def parent_extra_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "PEX3833_0_disformal_Weyl_slip",
            "component": "B_disformal_slip",
            "definition": "differential spatial/temporal scalar coefficient induced by Weyl/disformal representative choice",
            "zero_route": "no representative Weyl/disformal coefficient or coefficient is fixed q_obs/superselection data",
            "bound_formula": "B_disformal_slip <= abs(delta C_disformal/C_t)",
            "status": "MISSING_REPRESENTATIVE_COEFFICIENT_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "PEX3833_1_hidden_visible_coeff",
            "component": "B_hidden_coeff_slip",
            "definition": "hidden scalar invariant feeding C_s or C_t through a visible coefficient slot",
            "zero_route": "Hom(A_hid,Coeff_vis) has no nonconstant vertical component",
            "bound_formula": "B_hidden_coeff_slip <= sup |D_v(C_s-C_t)|/abs(C_t)",
            "status": "MORPHISM_BAN_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "PEX3833_2_readout_rep",
            "component": "B_readout_rep_slip",
            "definition": "readout map sends the same parent scalar into different temporal/spatial ordinary coefficients",
            "zero_route": "readout naturality before arena projection locks scalar coefficients",
            "bound_formula": "B_readout_rep_slip <= abs(R_readout_scalar_naturality)",
            "status": "READOUT_NATURALITY_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "PEX3833_3_parent_metric_nonuniqueness",
            "component": "B_parent_metric_nonuniqueness",
            "definition": "more than one visible metric/readout branch survives in the local exterior sector",
            "zero_route": "unique ordinary metric branch selected by parent action plus equivalence relation",
            "bound_formula": "B_parent_metric_nonuniqueness <= norm(g_obs_branch1-g_obs_branch2)_scalar/abs(Phi)",
            "status": "UNIQUE_METRIC_BRANCH_NOT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "PEX3833_4_total",
            "component": "B_gamma_parent_extra",
            "definition": "total parent/readout-generated scalar slip bound",
            "zero_route": "all parent-extra components above vanish on the same compact exterior readout",
            "bound_formula": "B_gamma_parent_extra <= B_disformal_slip + B_hidden_coeff_slip + B_readout_rep_slip + B_parent_metric_nonuniqueness",
            "status": "INTEGRATED_PARENT_EXTRA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "PGB3833_0_parent_extra",
            "observable": "B_gamma_parent_extra",
            "formula": "B_gamma_parent_extra <= B_disformal_slip + B_hidden_coeff_slip + B_readout_rep_slip + B_parent_metric_nonuniqueness",
            "needed_for_claim": "parent signed single-metric readout/naturality or numeric source-backed bounds for all components",
            "status": "FIRST_PARENT_EXTRA_GAMMA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PGB3833_1_gamma_total_update",
            "observable": "gamma-1",
            "formula": "abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)",
            "needed_for_claim": "3832 matter/EM rows, 3833 parent-extra row, boundary/readout rows, and eps_spatial row",
            "status": "UPDATED_GAMMA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3833_0_type_theorem",
            "gate": "type/chain-rule theorem exists",
            "status": "PASS_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "reason": "3808/3811 prove the theorem shape, not the parent signature",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3833_1_parent_extra_zero",
            "gate": "Sigma_TF_parent_extra zero claim",
            "status": "BLOCKED_PARENT_SIGNATURE_REQUIRED",
            "claim_allowed": False,
            "reason": "single-metric readout, no morphism, and no representative scalar coefficient are not parent-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3833_2_parent_extra_bound",
            "gate": "parent-extra gamma bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "bound components are explicit but not numeric/source-backed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3833_3_local_GR_gamma",
            "gate": "gamma/no-slip claim",
            "status": "BLOCKED_REFINED_BOUND_ONLY",
            "claim_allowed": False,
            "reason": "matter, parent-extra, boundary, readout, and eps_spatial components remain open",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3833_4_next_target",
            "gate": "next target attacks boundary/harmonic slip",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "parent-extra/readout source is formulated; remaining gamma ledger needs boundary/harmonic slip treatment",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3833_0_do_not_rehunt_theorem",
            "decision": "do not keep re-hunting the morphism-ban theorem",
            "basis": "3808/3811 already provide the exact conditional theorem and countermodel",
            "consequence": "future work must supply parent signatures or finite bounds, not another theorem restatement",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3833_1_parent_extra_as_gamma_bound",
            "decision": "treat unsigned parent-extra scalar slip as a gamma-bound row",
            "basis": "without single-metric readout/naturality, C_s-C_t can be legally sourced by hidden-visible scalar morphisms",
            "consequence": "the local-GR path remains honest and test-ready",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3833_2_boundary_next",
            "decision": "move next to boundary/harmonic scalar slip",
            "basis": "matter/EM and parent-extra components now have explicit ledgers",
            "consequence": "3834 should target Sigma_TF_boundary before closing the gamma dashboard",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3833_0",
            "next_checkpoint": "3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md",
            "script": "scripts/Y5_R2FR_3834_boundary_harmonic_scalar_slip_zero_or_gamma_bound.py",
            "objective": "try to prove Sigma_TF_boundary=0 for scalar slip using the 3825 boundary/reference route and elliptic uniqueness, or emit a boundary/harmonic gamma bound row",
            "reason": "3833 formulates parent-extra/readout slip; the next remaining no-slip source is boundary/harmonic scalar slip",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_PARENT_EXTRA_SLIP_BOUND",
            "claim": "no gamma/no-slip/local-GR claim",
            "summary": "3833 converts parent-extra/readout scalar slip into explicit zero conditions and a nonclaim gamma-bound row.",
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


def write_doc(sources, naturality, parent_extra, bounds, gates, decisions, timestamp: str) -> None:
    text = f"""# 3833 — Parent-Extra Scalar Slip Readout Naturality Or Bound

Private checkpoint. This attacks `Sigma_TF_parent_extra`, the parent/readout-generated scalar slip source. It does not claim no-slip or local GR.

Generated: `{timestamp}`

## Result

3833 uses the existing 3808/3810/3811 type-system results correctly:

- the chain-rule/type theorem exists;
- the countermodel also exists;
- the missing object is the parent signature proving single-metric readout/naturality.

So the parent-extra gamma contribution is:

`B_gamma_parent_extra <= B_disformal_slip + B_hidden_coeff_slip + B_readout_rep_slip + B_parent_metric_nonuniqueness`.

If all four vanish by parent signature, `Sigma_TF_parent_extra=0`. Current corpus has the theorem shape, not the signature, so this remains nonclaim.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Readout Naturality Theorem

{markdown_table(naturality, ["theorem_id", "statement", "formula", "status"])}

## Parent-Extra Slip Decomposition

{markdown_table(parent_extra, ["component_id", "component", "definition", "zero_route", "status"])}

## Parent-Extra Gamma Bounds

{markdown_table(bounds, ["bound_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This stops a loop: the morphism/type theorem is not the missing part anymore. The missing part is a parent action/readout signature proving the ordinary metric branch has no hidden-visible scalar coefficient path. Until then, parent-extra slip is a finite gamma-bound contribution.

Next target: `3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3832", "Current State After 3833", 1)
    paragraph = (
        "`3833` converts parent-extra/readout scalar slip into a precise nonclaim ledger. The 3808/3810/3811 type-system rows already give the chain-rule theorem and countermodel; "
        "the missing object is the parent signature proving single-metric readout/naturality. The new bound is "
        "`B_gamma_parent_extra <= B_disformal_slip+B_hidden_coeff_slip+B_readout_rep_slip+B_parent_metric_nonuniqueness`, "
        "so unsigned parent-extra slip is now a finite gamma-bound component rather than another vague morphism hunt.\n\n"
    )
    anchor = "`3832` separates"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3833-Y5-R2FR-parent-extra-scalar-slip-readout-naturality-or-bound.md`

Target: try to prove `Sigma_TF_parent_extra=0` from single-metric readout/naturality and no representative scalar morphism, or emit a parent-extra gamma bound row.

This is the best next move because 3832 separates matter/EM/Poynting TF stress; the next no-slip source is parent/readout-generated scalar slip."""
    new_gate = """`3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md`

Target: try to prove `Sigma_TF_boundary=0` for scalar slip using the 3825 boundary/reference route and elliptic uniqueness, or emit a boundary/harmonic gamma bound row.

This is the best next move because 3833 formulates parent-extra/readout slip; the next remaining no-slip source is boundary/harmonic scalar slip."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3833_READOUT_NATURALITY_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3833_PARENT_EXTRA_SLIP_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3833_PARENT_EXTRA_GAMMA_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3833_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3833_READOUT_NATURALITY_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3833 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3833 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, naturality, parent_extra, bounds, gates, timestamp: str):
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in naturality + parent_extra + bounds + gates)
    add("VAL3833_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3833_1_chain_rule", "chain-rule/type theorem and countermodel are represented", all(token in all_text for token in ["chain-rule", "countermodel", "D_v ObsRep"]), "theorem/countermodel tokens present")
    add("VAL3833_2_components", "parent-extra bound components are decomposed", all(token in all_text for token in ["B_disformal_slip", "B_hidden_coeff_slip", "B_readout_rep_slip", "B_parent_metric_nonuniqueness"]), "four parent-extra components present")
    add("VAL3833_3_nonclaim", "all 3833 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in naturality + parent_extra + bounds + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3833_4_zero_blocked", "parent-extra zero claim remains blocked", any(row["gate_id"] == "GATE3833_1_parent_extra_zero" and row["status"].startswith("BLOCKED") for row in gates), "parent-extra zero blocked")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3833_5_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3833_6_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "B_gamma_parent_extra" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3833*", "P8_Y5_BRR545_3833*", "*Y5_R2FR_3833*", "3833-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3833_7_formalization_clean", "formalization-workbench has no 3833 files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3833 file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3833_8_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    naturality = naturality_rows(timestamp)
    parent_extra = parent_extra_rows(timestamp)
    bounds = bound_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["naturality"], naturality)
    write_csv(OUTPUTS["parent_extra"], parent_extra)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, naturality, parent_extra, bounds, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, naturality, parent_extra, bounds, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_PARENT_EXTRA_SLIP_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
