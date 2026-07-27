from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3850"
BRANCH = "MTS_R2FR_Y5_RAB_HAIR_PPN_RESPONSE_OR_NEUTRALITY_PARENT_SIGNATURE_3850"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3850-Y5-R2FR-RAB-hair-PPN-response-or-neutrality-parent-signature.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3848 = PCW / "3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md"
P_3849 = PCW / "3849-Y5-R2FR-reciprocal-charge-neutrality-source-bound-or-RAB-hair-row.md"
CSV_3848_WEAK = OUT / "P8_Y5_R2FR_3848_WEAK_FIELD_TS_MAP.csv"
CSV_3849_NEUTRALITY = OUT / "P8_Y5_R2FR_3849_RECIPROCAL_NEUTRALITY_THEOREM.csv"
CSV_3849_AUDIT = OUT / "P8_Y5_R2FR_3849_QR_JR_SOURCE_AUDIT.csv"
CSV_3849_HAIR = OUT / "P8_Y5_R2FR_3849_RAB_HAIR_SOURCE_ROW.csv"
CSV_3849_PPN = OUT / "P8_Y5_R2FR_3849_RAB_PPN_PROJECTION_QUEUE.csv"
CSV_3849_VALIDATION = OUT / "P8_Y5_BRR545_3849_VALIDATION.csv"
CSV_LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds" / "local_bound_claims.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3850_SOURCE_REGISTER.csv",
    "response": OUT / "P8_Y5_R2FR_3850_RAB_TO_GAMMA_RESPONSE_DERIVATION.csv",
    "bound_contract": OUT / "P8_Y5_R2FR_3850_GAMMA_BOUND_CONTRACT.csv",
    "neutrality_audit": OUT / "P8_Y5_R2FR_3850_NEUTRALITY_SIGNATURE_AUDIT.csv",
    "projection_row": OUT / "P8_Y5_R2FR_3850_PPN_PROJECTION_INPUT_ROW.csv",
    "gates": OUT / "P8_Y5_R2FR_3850_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3850_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3850_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3850_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3850_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3850_0_3848_doc", P_3848, "S=exp(R_AB)/T^2"),
    ("SRC3850_1_3848_weak_map", CSV_3848_WEAK, "WFM3848_1_RAB_to_spatial"),
    ("SRC3850_2_3849_doc", P_3849, "Q_R=-Pi_R"),
    ("SRC3850_3_3849_neutrality", CSV_3849_NEUTRALITY, "RNT3849_2_zero_chain"),
    ("SRC3850_4_3849_audit", CSV_3849_AUDIT, "QJA3849_4_verdict"),
    ("SRC3850_5_3849_hair", CSV_3849_HAIR, "R_AB_hair_envelope"),
    ("SRC3850_6_3849_ppn_queue", CSV_3849_PPN, "PROJECTION_MATRIX_REQUIRED"),
    ("SRC3850_7_3849_validation", CSV_3849_VALIDATION, "PASS"),
    ("SRC3850_8_local_gamma_bound", CSV_LOCAL_BOUNDS, "Cassini_Shapiro_gamma_2003"),
]

PHI_DEF = "phi_T=U_T/c_*^2=(1-T^2)/2"
S_EXACT = "S=exp(R_AB)/T^2=exp(R_AB)/(1-2phi_T)"
GAMMA_LINEAR = "delta_gamma_RAB=R_AB/(2phi_T)+O(phi_T,R_AB,gauge,domain,normalization)"
GAMMA_SAFE_BOUND = "B_delta_gamma_RAB <= (exp(B_RAB)-1)/(2*phi_floor*T2_floor)+B_areal_to_PPN+B_domain+B_norm+B_higher_order"


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


def gamma_bound_row() -> dict[str, str]:
    if not CSV_LOCAL_BOUNDS.exists():
        return {}
    for row in read_csv_rows(CSV_LOCAL_BOUNDS):
        if row.get("row_id") == "R3_gamma" or row.get("observable") == "gamma_minus_1":
            return row
    return {}


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
                "role": "input_for_RAB_hair_to_gamma_response_or_neutrality_signature",
                "claim_use": "nonclaim_projection_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def response_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "derivation_id": "RGR3850_0_define_phi",
            "step": "clock-potential normalization",
            "formula": PHI_DEF,
            "assumptions": "use the 3848 weak-field TS map and the 3847 static spherical coframe",
            "result": "T^2=1-2phi_T exactly in this normalization",
            "status": "PASS_EXACT_DEFINITION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RGR3850_1_exact_spatial_factor",
            "step": "retain finite reciprocal hair",
            "formula": S_EXACT,
            "assumptions": "R_AB=ln(T^2 S) and T^2>0 on the local exterior domain",
            "result": "finite R_AB hair is a multiplicative radial-spatial readout factor",
            "status": "PASS_EXACT_REARRANGEMENT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RGR3850_2_linear_response",
            "step": "linear gamma response",
            "formula": "S=1+2phi_T+R_AB+O(phi_T^2,phi_T*R_AB,R_AB^2)",
            "assumptions": "weak field, small R_AB, same static areal readout, no hidden gauge/domain shift",
            "result": GAMMA_LINEAR,
            "status": "PASS_CONDITIONAL_LINEAR_RESPONSE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RGR3850_3_safe_bound",
            "step": "nonzero-denominator bound",
            "formula": GAMMA_SAFE_BOUND,
            "assumptions": "abs(R_AB)<=B_RAB, abs(phi_T)>=phi_floor>0, T^2>=T2_floor>0 on the comparison domain",
            "result": "finite R_AB hair can be compared to local gamma only after B_RAB, phi_floor, T2_floor, gauge/domain/normalization rows are sourced",
            "status": "PASS_BOUND_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RGR3850_4_zero_limit",
            "step": "neutrality zero limit",
            "formula": "Pi_R=0 and J_R=0 and W_R>0 => B_RAB=0 => delta_gamma_RAB=0",
            "assumptions": "the 3849 no-Pi_R/no-J_R parent source/boundary signature is actually signed",
            "result": "R_AB contributes no gamma hair on this branch, but full gamma still needs the existing no-slip/readout gates",
            "status": "PASS_EXACT_CONDITIONAL_ZERO_LIMIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_contract_rows(timestamp: str) -> list[dict[str, object]]:
    gamma = gamma_bound_row()
    theta_gamma = gamma.get("upper_bound", "MISSING_THETA_GAMMA")
    theta_units = gamma.get("units", "MISSING_UNITS")
    theta_source = gamma.get("reference_path_or_url", "MISSING_REFERENCE")
    return [
        {
            "contract_id": "GBC3850_0_threshold_source",
            "observable": "gamma_minus_1",
            "threshold_value": theta_gamma,
            "threshold_units": theta_units,
            "source_path_or_url": theta_source,
            "source_row": gamma.get("row_id", "MISSING_R3_gamma"),
            "status": "SOURCE_BACKED_THRESHOLD_ROW" if gamma else "MISSING_THRESHOLD_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "GBC3850_1_acceptance_inequality",
            "observable": "R_AB_contribution_to_gamma",
            "threshold_value": theta_gamma,
            "threshold_units": theta_units,
            "source_path_or_url": rel(CSV_LOCAL_BOUNDS),
            "source_row": "R3_gamma",
            "status": "PASS_IF_BOUND_LE_THRESHOLD_AND_ALL_INPUTS_VALID",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "GBC3850_2_required_inputs",
            "observable": "R_AB_contribution_to_gamma",
            "threshold_value": "B_RAB;phi_floor;T2_floor;B_areal_to_PPN;B_domain;B_norm;B_higher_order",
            "threshold_units": "mixed_input_contract",
            "source_path_or_url": rel(CSV_3849_HAIR),
            "source_row": "RHAIR3849_0_strict_row",
            "status": "BLOCKED_REQUIRED_INPUTS_NOT_FILLED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def neutrality_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "NSA3850_0_no_boundary_charge",
            "clause": "parent action has no independent Pi_R boundary/source momentum",
            "current_status": "UNSIGNED_FROM_3849",
            "consequence": "must retain |Pi_R| inside B_RAB",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "NSA3850_1_no_bulk_source",
            "clause": "ordinary/source action has no independent J_R bulk reciprocal source channel",
            "current_status": "UNSIGNED_FROM_3849",
            "consequence": "must retain int|J_R|dr inside B_RAB",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "NSA3850_2_boundary_counterterm",
            "clause": "reference/boundary counterterms do not carry R_AB momentum",
            "current_status": "COUNTERTERM_POLICY_REQUIRED",
            "consequence": "must retain |Pi_R_ct| inside B_RAB",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "NSA3850_3_positive_weight",
            "clause": "W_R positive and nondegenerate on the local exterior branch",
            "current_status": "POSITIVE_WEIGHT_SOURCE_REQUIRED",
            "consequence": "must retain T2_floor/W_R/domain guard rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "NSA3850_4_verdict",
            "clause": "parent-signed reciprocal neutrality",
            "current_status": "FAIL_CURRENT_CORPUS_USE_GAMMA_RESPONSE_CONTRACT",
            "consequence": "do not claim R_AB=0; project or bound finite hair",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def projection_row_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "projection_id": "PPR3850_0_gamma_RAB_input_row",
            "system_id": "MISSING_SYSTEM_DOMAIN",
            "phi_floor": "MISSING_phi_floor",
            "T2_floor": "MISSING_T2_floor",
            "B_RAB": "MISSING_B_RAB",
            "B_areal_to_PPN": "MISSING_B_areal_to_PPN",
            "B_domain": "MISSING_B_domain",
            "B_norm": "MISSING_B_norm",
            "B_higher_order": "MISSING_B_higher_order",
            "delta_gamma_RAB_bound": GAMMA_SAFE_BOUND,
            "theta_gamma_source": rel(CSV_LOCAL_BOUNDS),
            "source_path": rel(CSV_3849_HAIR),
            "status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "projection_id": "PPR3850_1_zero_switch",
            "system_id": "local_exterior_neutrality_branch",
            "phi_floor": "not_needed_if_B_RAB_zero",
            "T2_floor": "positive_branch_required",
            "B_RAB": "0 only if Pi_R=J_R=Pi_R_ct=Delta_R_boundary=Delta_W=0 parent-signed",
            "B_areal_to_PPN": "still_required_for_full_gamma_claim",
            "B_domain": "still_required_for_full_gamma_claim",
            "B_norm": "still_required_for_full_gamma_claim",
            "B_higher_order": "still_required_for_full_gamma_claim",
            "delta_gamma_RAB_bound": "0 contribution from R_AB hair only",
            "theta_gamma_source": rel(CSV_LOCAL_BOUNDS),
            "source_path": rel(CSV_3849_NEUTRALITY),
            "status": "ZERO_SWITCH_BLOCKED_UNTIL_PARENT_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3850_0_response_map",
            "gate": "R_AB to gamma response derived",
            "status": "PASS_CONDITIONAL_RESPONSE_MAP",
            "claim_allowed": False,
            "reason": "S=exp(R_AB)/T^2 gives a direct finite-hair gamma/readout residual",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3850_1_threshold",
            "gate": "local gamma threshold sourced",
            "status": "PASS_SOURCE_ROW_PRESENT_NONCLAIM",
            "claim_allowed": False,
            "reason": "Cassini R3_gamma row is available, but this checkpoint has not filled the MTS numerator/projection inputs",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3850_2_numeric_inputs",
            "gate": "B_RAB and projection inputs filled",
            "status": "BLOCKED_MISSING_B_RAB_phi_floor_T2_floor_gauge_domain_norm",
            "claim_allowed": False,
            "reason": "projection row is schema-ready but contains explicit MISSING_* values",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3850_3_neutrality_signature",
            "gate": "parent-signed Pi_R/J_R neutrality",
            "status": "BLOCKED_PARENT_SIGNATURE_REQUIRED",
            "claim_allowed": False,
            "reason": "3849 zero theorem remains exact but unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3850_4_scope_guard",
            "gate": "full PPN/local-GR claim",
            "status": "BLOCKED_GAMMA_COMPONENT_ONLY_BETA_NEWTON_SEPARATE",
            "claim_allowed": False,
            "reason": "this only maps R_AB hair into gamma; it does not close beta, Newton/source normalization, or full no-slip/readout",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3850_0",
            "decision": "finite R_AB hair is now test-facing rather than a vague missing term",
            "consequence": "the next row to fill is a concrete gamma contribution bound",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3850_1",
            "decision": "do not use Cassini/gamma threshold as a claim yet",
            "consequence": "threshold exists, but MTS numerator and projection coefficients are missing",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3850_2",
            "decision": "neutrality proof remains best route if parent source action can sign it",
            "consequence": "zeroing Pi_R and J_R beats fitting B_RAB, but cannot be assumed",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3850_0",
            "next_checkpoint": "3851-Y5-R2FR-fill-first-RAB-gamma-projection-row-or-prove-phi-floor-neutrality.md",
            "script": "scripts/Y5_R2FR_3851_fill_first_RAB_gamma_projection_row_or_prove_phi_floor_neutrality.py",
            "objective": "fill the first claim-gated R_AB-to-gamma projection row with B_RAB, phi_floor, T2_floor, gauge/domain/normalization bounds, or prove the parent neutrality zero route",
            "reason": "3850 derived the response map; the next real advance is a filled numerator/projection row or the no-hair zero signature",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_RAB_HAIR_TO_GAMMA_RESPONSE_CONTRACT",
            "claim": "no gamma, PPN, Newton, beta, R_AB zero, or local-GR claim",
            "next": "3851 fill first R_AB-gamma projection row or prove phi-floor/neutrality route",
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
    response: list[dict[str, object]],
    bound_contract: list[dict[str, object]],
    neutrality_audit: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3850 - R_AB Hair PPN Response Or Neutrality Parent Signature

Private checkpoint. This turns the finite `R_AB` hair left by 3849 into an explicit gamma/readout response contract. It does not claim local GR or a PPN pass.

Generated: `{timestamp}`

## Result

Define the dimensionless clock potential:

`{PHI_DEF}`.

The exact radial spatial factor from 3848 is:

`{S_EXACT}`.

Therefore, in the weak static areal readout branch:

`S=1+2phi_T+R_AB+O(phi_T^2,phi_T*R_AB,R_AB^2)`.

The first-order R_AB contribution to the gamma-like readout is:

`{GAMMA_LINEAR}`.

The safer nonzero-denominator contract is:

`{GAMMA_SAFE_BOUND}`.

This is the useful step: `R_AB` hair is no longer just "missing"; it has an explicit route into a local gamma comparison. The branch remains nonclaim because `B_RAB`, `phi_floor`, `T2_floor`, gauge/domain/normalization rows, and the parent neutrality signature are still missing.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Response Derivation

{markdown_table(response, ["derivation_id", "step", "formula", "status", "result"])}

## Gamma Bound Contract

{markdown_table(bound_contract, ["contract_id", "observable", "threshold_value", "source_row", "status"])}

## Neutrality Signature Audit

{markdown_table(neutrality_audit, ["audit_id", "clause", "current_status", "consequence"])}

## Projection Input Rows

{markdown_table(projection_rows, ["projection_id", "system_id", "B_RAB", "delta_gamma_RAB_bound", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3850 is a genuine forward move, not another circular audit: it derives the actual response law from reciprocal hair to the gamma/readout lane. The price is also clear. Either prove the 3849 parent neutrality route and set `B_RAB=0`, or fill the first projection row with real `B_RAB`, `phi_floor`, `T2_floor`, gauge/domain/normalization inputs.

Next target: `3851-Y5-R2FR-fill-first-RAB-gamma-projection-row-or-prove-phi-floor-neutrality.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3849", "Current State After 3850", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3850 at ")
    )
    paragraph = (
        "`3850` derives the finite `R_AB` hair response into the local gamma/readout lane. "
        "With `phi_T=U_T/c_*^2=(1-T^2)/2` and `S=exp(R_AB)/T^2`, the weak static areal branch gives `S=1+2phi_T+R_AB+O(phi_T^2,phi_T*R_AB,R_AB^2)`, hence `delta_gamma_RAB=R_AB/(2phi_T)+O(phi_T,R_AB,gauge,domain,normalization)`. "
        "The safe nonclaim contract is `B_delta_gamma_RAB <= (exp(B_RAB)-1)/(2*phi_floor*T2_floor)+B_areal_to_PPN+B_domain+B_norm+B_higher_order`. "
        "The Cassini `R3_gamma` threshold row is source-backed, but no claim opens because `B_RAB`, `phi_floor`, `T2_floor`, gauge/domain/normalization, and parent neutrality signatures are missing. "
        "The next target is to fill the first R_AB-to-gamma projection row or prove the 3849 neutrality zero route.\n\n"
    )
    anchor = "`3849` attacks"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3850-Y5-R2FR-RAB-hair-PPN-response-or-neutrality-parent-signature.md`

Target: derive the response map from finite `R_AB` hair into gamma/readout bounds, or parent-sign the no-`Pi_R`/no-`J_R` neutrality clause.

This is the best next move because 3849 makes the zero route exact but unsigned and creates the strict hair row."""
    new_gate = """`3851-Y5-R2FR-fill-first-RAB-gamma-projection-row-or-prove-phi-floor-neutrality.md`

Target: fill the first claim-gated R_AB-to-gamma projection row with `B_RAB`, `phi_floor`, `T2_floor`, gauge/domain/normalization bounds, or prove the parent neutrality zero route.

This is the best next move because 3850 has derived the response law; now the numerator/projection row or no-hair signature must be supplied."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3850_RAB_TO_GAMMA_RESPONSE_DERIVATION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3850_GAMMA_BOUND_CONTRACT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3850_PPN_PROJECTION_INPUT_ROW.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3850_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3850_RAB_TO_GAMMA_RESPONSE_DERIVATION.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3850 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    response: list[dict[str, object]],
    bound_contract: list[dict[str, object]],
    neutrality_audit: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in response + bound_contract + neutrality_audit + projection_rows + gates)
    add(
        "VAL3850_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add("VAL3850_1_exact_map", "exact S=exp(R_AB)/T^2 map is present", S_EXACT in all_text or S_EXACT in read_text(DOC_PATH), "exact map present")
    add("VAL3850_2_linear_response", "linear gamma response is present", "delta_gamma_RAB=R_AB/(2phi_T)" in all_text, "linear response present")
    add("VAL3850_3_safe_bound", "safe finite-hair bound is present", GAMMA_SAFE_BOUND in all_text, "safe bound present")
    add("VAL3850_4_threshold", "local gamma threshold row is sourced", any(row.get("source_row") == "R3_gamma" and row.get("status") == "SOURCE_BACKED_THRESHOLD_ROW" for row in bound_contract), "R3_gamma threshold found")
    add("VAL3850_5_missing_inputs_block_claim", "projection row remains blocked by explicit missing inputs", any("MISSING_B_RAB" in str(row) and row.get("valid_for_claim") is False for row in projection_rows), "MISSING_* blockers retained")
    add("VAL3850_6_neutrality_unsigned", "neutrality route remains unsigned", any("UNSIGNED" in str(row.get("current_status")) for row in neutrality_audit), "unsigned parent clauses retained")
    add("VAL3850_7_nonclaim", "all 3850 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in response + bound_contract + neutrality_audit + projection_rows + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3850_8_next", "next target is 3851", DOC_PATH.exists() and "3851-Y5-R2FR-fill-first-RAB-gamma-projection-row-or-prove-phi-floor-neutrality" in read_text(DOC_PATH), "3851 target visible")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3850_9_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3850_10_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "hair is no longer just" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3850*", "P8_Y5_BRR545_3850*", "*Y5_R2FR_3850*", "3850-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3850_11_formalization_clean", "formalization-workbench has no generated 3850 project files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3850 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3850_12_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    response = response_rows(timestamp)
    bound_contract = bound_contract_rows(timestamp)
    neutrality_audit = neutrality_audit_rows(timestamp)
    projection_rows = projection_row_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["response"], response)
    write_csv(OUTPUTS["bound_contract"], bound_contract)
    write_csv(OUTPUTS["neutrality_audit"], neutrality_audit)
    write_csv(OUTPUTS["projection_row"], projection_rows)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, response, bound_contract, neutrality_audit, projection_rows, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, response, bound_contract, neutrality_audit, projection_rows, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_RAB_HAIR_TO_GAMMA_RESPONSE_CONTRACT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
