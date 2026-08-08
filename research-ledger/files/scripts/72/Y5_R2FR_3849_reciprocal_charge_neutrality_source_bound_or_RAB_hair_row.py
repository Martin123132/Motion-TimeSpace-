from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3849"
BRANCH = "MTS_R2FR_Y5_RECIPROCAL_CHARGE_NEUTRALITY_OR_RAB_HAIR_ROW_3849"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3849-Y5-R2FR-reciprocal-charge-neutrality-source-bound-or-RAB-hair-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3848 = PCW / "3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md"
P_06_NEUTRALITY = PCW / "06-reciprocal-charge-source-neutrality.md"
P_05_ATTEMPT = PCW / "05-reciprocity-theorem-attempt.md"
P_04_CONTRACT = PCW / "04-vacuum-reciprocity-action-contract.md"

CSV_3848_DYNAMICS = OUT / "P8_Y5_R2FR_3848_TS_DYNAMICS_DERIVATION.csv"
CSV_3848_LEMMA = OUT / "P8_Y5_R2FR_3848_RAB_ZERO_OR_HAIR_LEMMA.csv"
CSV_3848_WEAK = OUT / "P8_Y5_R2FR_3848_WEAK_FIELD_TS_MAP.csv"
CSV_3848_PPN = OUT / "P8_Y5_R2FR_3848_PPN_IMPACT_UPDATE.csv"
CSV_3848_VALIDATION = OUT / "P8_Y5_BRR545_3848_VALIDATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3849_SOURCE_REGISTER.csv",
    "neutrality": OUT / "P8_Y5_R2FR_3849_RECIPROCAL_NEUTRALITY_THEOREM.csv",
    "source_audit": OUT / "P8_Y5_R2FR_3849_QR_JR_SOURCE_AUDIT.csv",
    "hair_row": OUT / "P8_Y5_R2FR_3849_RAB_HAIR_SOURCE_ROW.csv",
    "ppn_queue": OUT / "P8_Y5_R2FR_3849_RAB_PPN_PROJECTION_QUEUE.csv",
    "gates": OUT / "P8_Y5_R2FR_3849_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3849_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3849_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3849_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3849_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3849_0_3848_doc", P_3848, "reciprocal charge/source pair"),
    ("SRC3849_1_3848_dynamics", CSV_3848_DYNAMICS, "TSD3848_2_flux"),
    ("SRC3849_2_3848_lemma", CSV_3848_LEMMA, "RZL3848_1_source_bound"),
    ("SRC3849_3_3848_weak", CSV_3848_WEAK, "WFM3848_3_gamma_lane"),
    ("SRC3849_4_3848_ppn", CSV_3848_PPN, "PPNU3848_0_RAB_component"),
    ("SRC3849_5_3848_validation", CSV_3848_VALIDATION, "PASS"),
    ("SRC3849_6_06_neutrality", P_06_NEUTRALITY, "Pi_R = source reciprocal momentum/charge."),
    ("SRC3849_7_05_attempt", P_05_ATTEMPT, "W R_AB' = Q_R"),
    ("SRC3849_8_04_contract", P_04_CONTRACT, "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R"),
]

NEUTRALITY_FORMULA = "delta S_boundary=[W_R R_AB' + Pi_R] delta R_AB|Sigma"
HAIR_FORMULA = "R_AB(r)=-int_r^infty [Q_R + int_{r_in}^rho J_R(s)ds]/W_R(rho) d rho + R_boundary"
STRICT_BOUND = "B_RAB <= C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|)"


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
                "role": "input_for_reciprocal_charge_neutrality_or_RAB_hair_row",
                "claim_use": "nonclaim_neutrality_theorem_and_hair_row_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def neutrality_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "RNT3849_0_boundary_variation",
            "claim_piece": "boundary reciprocal charge",
            "formula": NEUTRALITY_FORMULA,
            "derivation": "vary reciprocal strain action with a source boundary term; natural boundary stationarity sets W_R R_AB' + Pi_R=0",
            "result": "Q_R=-Pi_R at the source boundary",
            "status": "EXACT_CONDITIONAL_BOUNDARY_RELATION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "RNT3849_1_bulk_neutrality",
            "claim_piece": "bulk source neutrality",
            "formula": "J_R=delta S_src/delta R_AB|visible_source_data",
            "derivation": "if ordinary source action depends on observed clock potential/source data but has no independent R_AB argument, then the exterior reciprocal bulk source vanishes",
            "result": "J_R=0 is exact if no independent reciprocal source slot exists",
            "status": "EXACT_CONDITIONAL_BULK_NEUTRALITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "RNT3849_2_zero_chain",
            "claim_piece": "R_AB zero from source neutrality",
            "formula": "Pi_R=0 and J_R=0 => Q_R=0 => R_AB=0 => T^2 S=1",
            "derivation": "combine RNT3849_0 with the 3848 no-hair lemma",
            "result": "reciprocal routing is derived if parent source/boundary neutrality is signed",
            "status": "EXACT_CONDITIONAL_NEUTRALITY_CHAIN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "RNT3849_3_current_verdict",
            "claim_piece": "current MTS reciprocal neutrality",
            "formula": "parent_signed(no independent Pi_R,J_R source slot) is required",
            "derivation": "06 gives the route but states source neutrality is not parent-derived",
            "result": "Q_R/J_R zero is not claimed for current corpus",
            "status": "NEUTRALITY_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "QJA3849_0_PiR_slot",
            "object": "Pi_R",
            "required_zero_clause": "source/boundary action has no independent reciprocal momentum conjugate to R_AB",
            "current_status": "UNSIGNED",
            "if_unsigned": "retain |Pi_R| in B_RAB",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "QJA3849_1_JR_slot",
            "object": "J_R",
            "required_zero_clause": "bulk ordinary matter/exterior action has no independent R_AB source channel",
            "current_status": "UNSIGNED",
            "if_unsigned": "retain int|J_R|dr in B_RAB",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "QJA3849_2_boundary_counterterm",
            "object": "Pi_R_ct",
            "required_zero_clause": "allowed boundary/reference counterterms are fixed before readout and have no reciprocal momentum",
            "current_status": "COUNTERTERM_POLICY_REQUIRED",
            "if_unsigned": "retain |Pi_R_ct| in B_RAB",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "QJA3849_3_W_positive",
            "object": "W_R",
            "required_zero_clause": "W_R>0 and nondegenerate on exterior branch",
            "current_status": "POSITIVE_WEIGHT_SOURCE_REQUIRED",
            "if_unsigned": "retain |Delta_W| and no no-hair promotion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "QJA3849_4_verdict",
            "object": "Q_R,J_R neutrality",
            "required_zero_clause": "QJA3849_0 through QJA3849_3 all parent-signed",
            "current_status": "FAIL_CURRENT_CLAIM_SOURCE_AUDIT_READY",
            "if_unsigned": "use strict R_AB hair row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def hair_row_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "hair_id": "RHAIR3849_0_strict_row",
            "quantity": "R_AB_hair_envelope",
            "formula": STRICT_BOUND,
            "required_columns": "system_id;r_in;r_out;W_R_min;Pi_R;Pi_R_units;Pi_R_ct;JR_L1;Delta_R_boundary;Delta_W;C_W;RAB_bound;source_path;equation_ref;valid_for_claim",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "projection_use": "feeds B_gamma_RAB and static-spherical readout residual only after values/source paths exist",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "hair_id": "RHAIR3849_1_zero_switch",
            "quantity": "R_AB_zero_theorem_switch",
            "formula": "theorem_zero=true iff Pi_R_zero_authority and J_R_zero_authority are PARENT_SIGNED_TRUE and W_R_positive_source exists",
            "required_columns": "Pi_R_zero_authority;J_R_zero_authority;W_R_positive_source;boundary_reference_source;equation_ref;valid_for_claim",
            "current_status": "ZERO_SWITCH_BLOCKED",
            "projection_use": "prevents closure-only AB=1 promotion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ppn_queue_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "queue_id": "RPPN3849_0_gamma",
            "target": "gamma/readout projection",
            "needed_input": "RAB_bound plus gauge/domain map from static spherical areal branch to PPN readout",
            "current_status": "PROJECTION_MATRIX_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "RPPN3849_1_Newton",
            "target": "Newton/source normalization",
            "needed_input": "T-potential Poisson/source owner plus R_AB hair separation",
            "current_status": "SOURCE_NORMALIZATION_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "RPPN3849_2_beta",
            "target": "beta",
            "needed_input": "second-order temporal self-coupling/EH2 ledger; R_AB hair is not a beta substitute",
            "current_status": "BETA_SEPARATE_GATE",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3849_0_boundary_relation",
            "gate": "Q_R=-Pi_R relation",
            "status": "PASS_EXACT_CONDITIONAL_RELATION",
            "claim_allowed": False,
            "reason": "source-boundary variation gives W_R R_AB' + Pi_R=0",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3849_1_neutrality_claim",
            "gate": "Q_R=J_R=0 for current MTS",
            "status": "BLOCKED_PARENT_SOURCE_NEUTRALITY_REQUIRED",
            "claim_allowed": False,
            "reason": "no parent-signed no-Pi_R/no-J_R source action clause exists yet",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3849_2_hair_row",
            "gate": "finite R_AB hair row exists",
            "status": "PASS_SCHEMA_READY_NONCLAIM",
            "claim_allowed": False,
            "reason": "strict source row schema exists but values and source paths are missing",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3849_3_ppn_projection",
            "gate": "R_AB hair PPN projection",
            "status": "BLOCKED_PROJECTION_MATRIX_REQUIRED",
            "claim_allowed": False,
            "reason": "B_gamma_RAB needs gauge/domain map before comparison to local bounds",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3849_4_next_action",
            "gate": "next target selected",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "next derive/source the R_AB hair-to-PPN response matrix or parent-sign neutrality",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3849_0",
            "decision": "neutrality route is exact but not parent-signed",
            "consequence": "do not claim T^2S=1 yet",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3849_1",
            "decision": "retain R_AB hair as a strict row rather than a vague closure",
            "consequence": "future PPN/gamma tests can bound it if neutrality does not close",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3849_2",
            "decision": "beta remains untouched by reciprocal neutrality",
            "consequence": "continue EH2/beta branch separately",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3849_0",
            "next_checkpoint": "3850-Y5-R2FR-RAB-hair-PPN-response-or-neutrality-parent-signature.md",
            "script": "scripts/Y5_R2FR_3850_RAB_hair_PPN_response_or_neutrality_parent_signature.py",
            "objective": "derive the response map from finite R_AB hair into gamma/readout bounds, or parent-sign the no-Pi_R/no-J_R neutrality clause",
            "reason": "3849 makes the zero route exact but unsigned and creates the strict hair row; the next useful step is projection or parent signature",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_RECIPROCAL_NEUTRALITY_OR_RAB_HAIR_ROW",
            "claim": "no R_AB zero, gamma, Newton, beta, local-GR, or PPN claim",
            "next": "3850 R_AB hair PPN response or neutrality parent signature",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        vals = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, object]],
    neutrality: list[dict[str, object]],
    source_audit: list[dict[str, object]],
    hair_row: list[dict[str, object]],
    ppn_queue: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3849 - Reciprocal Charge Neutrality Source Bound Or R_AB Hair Row

Private checkpoint. This attacks the `Q_R,J_R` obstruction isolated by 3848. It does not claim reciprocal routing or local GR.

Generated: `{timestamp}`

## Result

The source-boundary variation gives:

`{NEUTRALITY_FORMULA}`.

Therefore the boundary reciprocal charge is:

`Q_R=-Pi_R`.

So the clean zero chain is:

`Pi_R=0 and J_R=0 => Q_R=0 => R_AB=0 => T^2S=1`.

Current MTS still has not parent-signed the no-`Pi_R`/no-`J_R` source clause. The honest fallback is now strict:

`{STRICT_BOUND}`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Neutrality Theorem

{markdown_table(neutrality, ["theorem_id", "claim_piece", "formula", "status", "result"])}

## Q_R/J_R Source Audit

{markdown_table(source_audit, ["audit_id", "object", "current_status", "if_unsigned"])}

## R_AB Hair Row

{markdown_table(hair_row, ["hair_id", "quantity", "formula", "current_status", "projection_use"])}

## PPN Projection Queue

{markdown_table(ppn_queue, ["queue_id", "target", "needed_input", "current_status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is another useful narrowing. `R_AB=0` is not assumed; it follows if the parent source/boundary action is reciprocal-neutral. If that cannot be signed, the theory now carries a strict `R_AB_hair_envelope` row into PPN/gamma projection instead of smuggling `AB=1`.

Next target: `3850-Y5-R2FR-RAB-hair-PPN-response-or-neutrality-parent-signature.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3848", "Current State After 3849", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3849 at ")
    )
    paragraph = (
        "`3849` attacks the exact reciprocal neutrality obstruction. "
        "Boundary variation gives `delta S_boundary=[W_R R_AB'+Pi_R]delta R_AB|Sigma`, hence `Q_R=-Pi_R`; with `Pi_R=0` and `J_R=0`, the 3848 no-hair lemma gives `R_AB=0` and `T^2S=1`. "
        "Current MTS still does not parent-sign the no-`Pi_R`/no-`J_R` source clause, so no reciprocal-routing/local-GR claim is made. "
        "The fallback is now strict: `B_RAB <= C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|)`, with a machine row ready for PPN/gamma projection once values or theorem-zero certificates exist.\n\n"
    )
    anchor = "`3848` derives"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3849-Y5-R2FR-reciprocal-charge-neutrality-source-bound-or-RAB-hair-row.md`

Target: prove `Q_R=0` and `J_R=0` from parent source/boundary neutrality, or emit a strict finite `R_AB` hair/source row for PPN projection.

This is the best next move because 3848 shows `R_AB=0` follows exactly from reciprocal neutrality, making `Q_R,J_R` the real obstruction."""
    new_gate = """`3850-Y5-R2FR-RAB-hair-PPN-response-or-neutrality-parent-signature.md`

Target: derive the response map from finite `R_AB` hair into gamma/readout bounds, or parent-sign the no-`Pi_R`/no-`J_R` neutrality clause.

This is the best next move because 3849 makes the zero route exact but unsigned and creates the strict hair row."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3849_RECIPROCAL_NEUTRALITY_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3849_QR_JR_SOURCE_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3849_RAB_HAIR_SOURCE_ROW.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3849_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3849_RECIPROCAL_NEUTRALITY_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3849 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    neutrality: list[dict[str, object]],
    source_audit: list[dict[str, object]],
    hair_row: list[dict[str, object]],
    ppn_queue: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in neutrality + source_audit + hair_row + ppn_queue + gates)
    add("VAL3849_0_sources", "all cited local source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3849_1_boundary_relation", "Q_R=-Pi_R relation is present", NEUTRALITY_FORMULA in all_text and "Q_R=-Pi_R" in all_text, "boundary relation present")
    add("VAL3849_2_zero_chain", "neutrality zero chain is present", "Pi_R=0 and J_R=0 => Q_R=0 => R_AB=0 => T^2 S=1" in all_text or "Pi_R=0 and J_R=0 => Q_R=0 => R_AB=0 => T^2S=1" in read_text(DOC_PATH), "zero chain present")
    add("VAL3849_3_hair_row", "strict R_AB hair row is present", STRICT_BOUND in all_text and "R_AB_hair_envelope" in all_text, "hair row present")
    add("VAL3849_4_projection_queue", "PPN projection queue is present", "PROJECTION_MATRIX_REQUIRED" in all_text and "BETA_SEPARATE_GATE" in all_text, "projection queue present")
    add("VAL3849_5_nonclaim", "all 3849 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in neutrality + source_audit + hair_row + ppn_queue + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3849_6_next", "next target is 3850", DOC_PATH.exists() and "3850-Y5-R2FR-RAB-hair-PPN-response-or-neutrality-parent-signature" in read_text(DOC_PATH), "3850 target visible")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3849_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3849_8_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "source-boundary variation" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3849*", "P8_Y5_BRR545_3849*", "*Y5_R2FR_3849*", "3849-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3849_9_formalization_clean", "formalization-workbench has no generated 3849 project files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3849 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3849_10_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    neutrality = neutrality_rows(timestamp)
    source_audit = source_audit_rows(timestamp)
    hair_row = hair_row_rows(timestamp)
    ppn_queue = ppn_queue_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["neutrality"], neutrality)
    write_csv(OUTPUTS["source_audit"], source_audit)
    write_csv(OUTPUTS["hair_row"], hair_row)
    write_csv(OUTPUTS["ppn_queue"], ppn_queue)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, neutrality, source_audit, hair_row, ppn_queue, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, neutrality, source_audit, hair_row, ppn_queue, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_RECIPROCAL_NEUTRALITY_OR_RAB_HAIR_ROW")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
