from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from curvature_projection_gate import evaluate_parent_scale_row, evaluate_projection_row, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4455"
CLAIM_ID = "L-297"
MARKER = "PPC4161_CR2_PARENT_SCALE_SIGNATURE_OR_ALPHA_LAMBDA_PROJECTION_4455"
PACKET_MARKER = "PPC4161_PACKET_CR2_PARENT_SCALE_SIGNATURE_OR_ALPHA_LAMBDA_PROJECTION_4455"
DECISION = "CR2_STANDARD_ALPHA_LAMBDA_PROJECTION_ROWS_WRITTEN_PARENT_SCALE_SIGNATURE_STAGED_FULL_CURVE_AND_MTS_COEFFICIENT_MAPPING_STILL_OPEN_NONCLAIM"
NEXT_TARGET = "4456-Y5-R2FR-alpha-lambda-curve-promotion-or-parent-MR-scale-value.md"

FORMAL_PATH = FORMAL / "471-PPC4161-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md"
DOC_PATH = POST / "4455-Y5-R2FR-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4455_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4455_SOURCE_REGISTER.csv"
PROJECTION_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4455_ALPHA_LAMBDA_PROJECTION_INPUT.csv"
PROJECTION_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4455_ALPHA_LAMBDA_PROJECTION_OUTPUT.csv"
SCALE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4455_PARENT_SCALE_SIGNATURE_INPUT.csv"
SCALE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4455_PARENT_SCALE_SIGNATURE_OUTPUT.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4455_DERIVATION_ROWS.csv"
FORMULA_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4455_FORMULA_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4455_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4455_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4455_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4455_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "curvature_projection_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4455_cR2_parent_scale_signature_or_alpha_lambda_projection_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4454 = SOURCE_DIR / "P8_Y5_R2FR_4454_NEXT_TARGET.csv"
STATUS_4454 = SOURCE_DIR / "P8_Y5_R2FR_4454_STATUS.csv"
MODE_4454 = SOURCE_DIR / "P8_Y5_R2FR_4454_CURVATURE_MODE_OUTPUT.csv"
BOUND_4454 = SOURCE_DIR / "P8_Y5_R2FR_4454_SHORT_RANGE_ORBITAL_BOUND_OUTPUT.csv"
FORMULA_4454 = SOURCE_DIR / "P8_Y5_R2FR_4454_FORMULA_ROWS.csv"
FORMAL_470 = FORMAL / "470-PPC4161-cR2-MR-parent-scale-or-short-range-orbital-bound.md"
FORMAL_201 = FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md"
WEB_HIGHER_DERIVATIVE = "https://arxiv.org/abs/gr-qc/0109005"
WEB_SINGULARITY_CANCEL = "https://arxiv.org/abs/1609.05432"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4455_00_next4454", "kind": "local", "ref": str(NEXT_4454), "needle": "4455-Y5-R2FR-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md", "role": "4454 selected cR2 projection target."},
        {"source_id": "SRC4455_01_status4454", "kind": "local", "ref": str(STATUS_4454), "needle": "anchor_ready_full_curve_projection_missing", "role": "4454 open projection status."},
        {"source_id": "SRC4455_02_mode4454", "kind": "local", "ref": str(MODE_4454), "needle": "CM4454_0_scalar_R2", "role": "4454 scalar/tensor mode rows."},
        {"source_id": "SRC4455_03_bound4454", "kind": "local", "ref": str(BOUND_4454), "needle": "BR4454_0_R10_alpha1_anchor", "role": "4454 short-range anchor."},
        {"source_id": "SRC4455_04_formula4454", "kind": "local", "ref": str(FORMULA_4454), "needle": "F4454_0_yukawa_potential", "role": "4454 formula rows."},
        {"source_id": "SRC4455_05_formal470", "kind": "local", "ref": str(FORMAL_470), "needle": "MTS still needs either a parent scale theorem", "role": "formal 4454 handoff."},
        {"source_id": "SRC4455_06_formal201", "kind": "local", "ref": str(FORMAL_201), "needle": "projection Jacobian/numerator", "role": "projection still required."},
        {"source_id": "SRC4455_07_web_higher_derivative", "kind": "web", "ref": WEB_HIGHER_DERIVATIVE, "needle": "Newtonian limit has Yukawa terms", "role": "external higher-derivative Newtonian-limit source."},
        {"source_id": "SRC4455_08_web_singularity", "kind": "web", "ref": WEB_SINGULARITY_CANCEL, "needle": "higher-derivative potentials and massive poles", "role": "external higher-derivative potential source."},
        {"source_id": "SRC4455_09_gate", "kind": "local", "ref": str(GATE_PATH), "needle": "def evaluate_projection_row", "role": "4455 projection gate."},
        {"source_id": "SRC4455_10_generator", "kind": "local", "ref": str(GENERATOR_PATH), "needle": 'CHECKPOINT = "4455"', "role": "4455 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        kind = str(spec["kind"])
        ref = str(spec["ref"])
        path = Path(ref) if kind == "local" else None
        line = line_of(path, str(spec["needle"])) if path else 0
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": spec["source_id"],
            "source_kind": kind,
            "source_ref": ref,
            "local_path_exists": bool(path and path.exists()),
            "web_source_recorded": kind == "web" and ref.startswith("https://"),
            "web_verified_in_session": kind == "web",
            "needle": spec["needle"],
            "needle_found": line > 0 if kind == "local" else True,
            "line_number": line,
            "role": spec["role"],
            "valid_for_claim": False,
        })
    return rows


def projection_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "projection_id": "AP4455_0_scalar",
            "mode": "scalar_R2_standard_branch",
            "source_path": str(MODE_4454),
            "alpha_standard": 1.0 / 3.0,
            "lambda_symbol": "lambda_0 = 1/M_0",
            "mass_symbol": "M_0",
            "projection_formula": "Phi_0/Phi_N = +(1/3) exp(-M_0 r)",
            "standard_projection_written": True,
            "mts_coefficient_mapped": False,
            "full_curve_available": False,
            "parent_scale_signed": False,
            "no_cancellation_guard": True,
            "public_claim_false": True,
        },
        {
            "projection_id": "AP4455_1_spin2",
            "mode": "massive_spin2_standard_branch",
            "source_path": str(MODE_4454),
            "alpha_standard": -4.0 / 3.0,
            "lambda_symbol": "lambda_2 = 1/M_2",
            "mass_symbol": "M_2",
            "projection_formula": "Phi_2/Phi_N = -(4/3) exp(-M_2 r)",
            "standard_projection_written": True,
            "mts_coefficient_mapped": False,
            "full_curve_available": False,
            "parent_scale_signed": False,
            "no_cancellation_guard": True,
            "public_claim_false": True,
        },
        {
            "projection_id": "AP4455_2_parent_heavy",
            "mode": "parent_heavy_scale_route",
            "source_path": str(FORMULA_4454),
            "alpha_standard": 1.0,
            "lambda_symbol": "lambda_R <= 1/M_parent,IR",
            "mass_symbol": "M_parent,IR",
            "projection_formula": "M_parent,IR L_test >> 1 => exp(-M_parent,IR r) suppressed",
            "standard_projection_written": True,
            "mts_coefficient_mapped": False,
            "full_curve_available": False,
            "parent_scale_signed": False,
            "no_cancellation_guard": True,
            "public_claim_false": True,
        },
    ]


def scale_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "scale_id": "PS4455_0_parent_zero",
            "scale_route": "coefficient_zero_selection",
            "source_path": str(FORMAL_470),
            "scale_contract": "c_R2=0 or curvature-square invariant forbidden by parent selector",
            "hierarchy_written": True,
            "numeric_parent_value": False,
            "exceeds_anchor_mass": False,
            "coefficient_zero": False,
            "public_claim_false": True,
        },
        {
            "scale_id": "PS4455_1_parent_heavy",
            "scale_route": "heavy_parent_scale",
            "source_path": str(FORMULA_4454),
            "scale_contract": "M_parent,IR > 0.0051120979 eV for alpha≈1 anchor, stronger condition requires alpha(lambda)",
            "hierarchy_written": True,
            "numeric_parent_value": False,
            "exceeds_anchor_mass": False,
            "coefficient_zero": False,
            "public_claim_false": True,
        },
        {
            "scale_id": "PS4455_2_full_curve_projection",
            "scale_route": "empirical_alpha_lambda_projection",
            "source_path": str(BOUND_4454),
            "scale_contract": "abs(alpha_i) <= alpha_bound(lambda_i) for each scalar/tensor mode without cancellation",
            "hierarchy_written": True,
            "numeric_parent_value": False,
            "exceeds_anchor_mass": False,
            "coefficient_zero": False,
            "public_claim_false": True,
        },
    ]


def formula_rows() -> List[Dict[str, object]]:
    return [
        {"formula_id": "F4455_0_standard_potential", "formula": "Phi/Phi_N = 1 + (1/3) exp(-M_0 r) - (4/3) exp(-M_2 r)", "meaning": "standard local quadratic-gravity projection template; MTS coefficients must still map to M0/M2", "valid_for_claim": False},
        {"formula_id": "F4455_1_scalar_projection", "formula": "alpha_0=+1/3, lambda_0=1/M_0", "meaning": "scalar cR2 projection row", "valid_for_claim": False},
        {"formula_id": "F4455_2_spin2_projection", "formula": "alpha_2=-4/3, lambda_2=1/M_2", "meaning": "massive spin-2 projection row", "valid_for_claim": False},
        {"formula_id": "F4455_3_score_rule", "formula": "for each i: abs(alpha_i) <= alpha_bound(lambda_i)", "meaning": "R10 scoring rule; no scalar/tensor cancellation unless parent-derived", "valid_for_claim": False},
        {"formula_id": "F4455_4_anchor_warning", "formula": "alpha=1 anchor at lambda=38.6um is not a substitute for alpha_bound(lambda)", "meaning": "claim firewall for 4454 anchor", "valid_for_claim": False},
    ]


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "D4455_0_projection_template",
            "claim": "The standard local quadratic-gravity weak-field template gives fixed scalar/spin-2 Yukawa amplitudes.",
            "derivation": "For the ordinary fourth-order metric branch, the Newtonian potential can be written as the GR potential plus a scalar Yukawa term with alpha_0=+1/3 and a massive spin-2 Yukawa term with alpha_2=-4/3. This is used only as a projection template; MTS still has to map its parent coefficients to M_0 and M_2 or prove the modes absent.",
            "consequence": "c_R2/M_R now has explicit alpha_i, lambda_i placeholders instead of generic alpha.",
            "status": "STANDARD_ALPHA_LAMBDA_TEMPLATE_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4455_1_anchor_firewall",
            "claim": "The alpha=1 Eot-Wash anchor is not enough for the scalar/spin-2 projection.",
            "derivation": "The scalar template has |alpha_0|=1/3 and the spin-2 template has |alpha_2|=4/3. Neither is exactly the alpha=1 anchor row. A full alpha(lambda) curve or a parent heavy-scale theorem is required before scoring either mode.",
            "consequence": "No R10/local-GR claim can be made from the 38.6um anchor alone.",
            "status": "ANCHOR_NOT_FULL_CURVE_GUARD_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4455_2_parent_scale_signature",
            "claim": "The parent route is a scale or zero signature.",
            "derivation": "The parent action must either set the curvature-square coefficients to zero or give a mass hierarchy M_0,M_2 >= M_parent,IR with M_parent,IR L_test >> 1. The alpha≈1 anchor gives a smoke mass floor only; the public route needs an MTS-owned numeric scale or a full alpha(lambda) projection.",
            "consequence": "4456 should either promote the alpha(lambda) curve or source a parent M_R scale value.",
            "status": "PARENT_SCALE_SIGNATURE_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4455_3_no_cancellation",
            "claim": "Scalar/tensor cancellation cannot be used unless the parent action derives it.",
            "derivation": "The standard template contains opposite-sign Yukawa pieces. Public scoring must test each channel separately or carry a parent-derived cancellation theorem. Otherwise a local fifth-force failure could be hidden by accidental cancellation.",
            "consequence": "R10/orbital projection rows must be channelwise.",
            "status": "CHANNELWISE_SCORING_REQUIRED",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "standard_projection_rows_written": True,
        "alpha_scalar": "1/3",
        "alpha_spin2": "-4/3",
        "parent_scale_signature_written": True,
        "full_alpha_lambda_curve_ready": False,
        "MTS_coefficient_map_ready": False,
        "public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def status_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "projection_status": "alpha0=1/3_alpha2=-4/3_template_written",
        "parent_scale_status": "signature_staged_numeric_MR_missing",
        "short_range_status": "full_alpha_lambda_curve_or_projection_missing",
        "local_GR_public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def next_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4455_0",
        "target": NEXT_TARGET,
        "objective": "Make the cR2 branch scoreable by either promoting alpha(lambda) curve data or sourcing an MTS-owned parent M_R value.",
        "derive_first": "derive or identify parent M_0/M_2 scale values from the MTS IR hierarchy",
        "fallback": "digitize/promote alpha(lambda) curve and map alpha_0=1/3, alpha_2=-4/3 channelwise",
        "risk": "treating the standard projection template as an MTS coefficient derivation",
        "valid_for_claim": False,
    }]


def claim_gate_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    projections = rows_from(PROJECTION_OUTPUT)
    scales = rows_from(SCALE_OUTPUT)
    return [
        {"gate_id": "CG4455_0_local_sources_exist", "claim": "all cited local source paths exist", "passed": all(row["local_path_exists"] == "True" for row in sources if row["source_kind"] == "local"), "valid_for_claim": False, "detail": "Local source register path-backed."},
        {"gate_id": "CG4455_1_local_needles_found", "claim": "all cited local needles found", "passed": all(row["needle_found"] == "True" for row in sources if row["source_kind"] == "local"), "valid_for_claim": False, "detail": "Local projection chain is sourced."},
        {"gate_id": "CG4455_2_web_sources_recorded", "claim": "external projection source URLs recorded", "passed": all(row["web_source_recorded"] == "True" and row["web_verified_in_session"] == "True" for row in sources if row["source_kind"] == "web"), "valid_for_claim": False, "detail": "Web rows support context, not public MTS claim."},
        {"gate_id": "CG4455_3_projection_rows_written", "claim": "standard alpha(lambda) projection rows written", "passed": all(row["current_status"] == "STANDARD_ALPHA_LAMBDA_PROJECTION_WRITTEN_MTS_OR_CURVE_MISSING" for row in projections), "valid_for_claim": False, "detail": "Scalar/spin2/heavy rows written."},
        {"gate_id": "CG4455_4_parent_scale_signature_staged", "claim": "parent scale routes staged", "passed": all(row["current_status"] == "PARENT_SCALE_SIGNATURE_WRITTEN_NUMERIC_VALUE_OR_ZERO_MISSING" for row in scales), "valid_for_claim": False, "detail": "Zero/heavy/full curve routes staged."},
        {"gate_id": "CG4455_5_no_public_claim", "claim": "no cR2/local-GR public claim emitted", "passed": all(row["claim_allowed"] == "False" for row in projections) and all(row["claim_allowed"] == "False" for row in scales), "valid_for_claim": False, "detail": "MTS coefficient map/full curve/parent scale missing."},
        {"gate_id": "CG4455_6_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def build_doc() -> str:
    return f"""# 471 PPC4161 cR2 parent scale signature or alpha lambda projection row

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4455 makes the `c_R2/M_R` branch score-shaped:

```text
Phi/Phi_N = 1 + (1/3) exp(-M_0 r) - (4/3) exp(-M_2 r)
alpha_0 = +1/3, lambda_0 = 1/M_0
alpha_2 = -4/3, lambda_2 = 1/M_2
```

This is not yet an MTS coefficient derivation. It is a standard projection template for the finite-range curvature branch. Public scoring still needs:

```text
1. MTS coefficient map -> M_0, M_2 and alpha_i; or
2. parent scale/zero theorem; or
3. full alpha(lambda) curve and channelwise projection rows.
```

The alpha=1 short-range anchor from 4454 remains useful but not sufficient for `+1/3` and `-4/3` channels.

## Source Register

{table(rows_from(SOURCE_REGISTER))}

## Alpha Lambda Projection Gate

{table(rows_from(PROJECTION_OUTPUT))}

## Parent Scale Signature Gate

{table(rows_from(SCALE_OUTPUT))}

## Formula Rows

{table(rows_from(FORMULA_ROWS))}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Claim Gates

{table(rows_from(CLAIM_GATES))}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4455 Y5 R2FR cR2 parent scale signature or alpha lambda projection row

Private checkpoint generated at `{STAMP}`.

Summary:
- Wrote standard scalar/spin-2 projection rows: `alpha_0=+1/3`, `alpha_2=-4/3`.
- Converted cR2 scoring into channelwise `abs(alpha_i) <= alpha_bound(lambda_i)`.
- Staged parent scale/zero routes separately from empirical curve routes.
- Kept the branch nonclaim because MTS coefficient mapping, parent M_R value, and full alpha(lambda) curve are still missing.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    row = {field: "" for field in fieldnames}
    payload = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "4455 writes c_R2/M_R alpha(lambda) projection rows for standard scalar and massive spin-2 finite-range curvature modes, while keeping parent scale and full-curve requirements open.",
        "current_evidence": "4455 source register, alpha-lambda projection gate, parent scale signature gate, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "cR2_alpha_lambda_projection_template_ready_MTS_mapping_parent_scale_full_curve_open_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the standard projection template as an MTS coefficient derivation or using the alpha=1 anchor as a full curve.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4455 source register, alpha-lambda projection gate, parent scale signature gate, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Treating the standard projection template as an MTS coefficient derivation or using the alpha=1 anchor as a full curve.",
    }
    for key, value in payload.items():
        if key in row:
            row[key] = value
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Parent-Derivation Update - cR2 Alpha Lambda Projection

Marker: `{MARKER}`  
Source checkpoint: `4455-Y5-R2FR-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md`  
Claim register row: `{CLAIM_ID}`

The curvature-square survivor now has channelwise projection rows: scalar `alpha_0=+1/3`, massive spin-2 `alpha_2=-4/3`, with `lambda_i=1/M_i`. The branch remains nonclaim until MTS maps its coefficients to these modes, derives a parent scale/zero theorem, or promotes a full `alpha(lambda)` curve.
"""
    packet_section = f"""## PPC4161 Packet Addendum - cR2 Alpha Lambda Projection

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4455-Y5-R2FR-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md`

The packet now carries the scalar/spin-2 channel projection and no-cancellation rule. Next packet target: full curve promotion or parent `M_R` scale value.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    projections = rows_from(PROJECTION_OUTPUT)
    scales = rows_from(SCALE_OUTPUT)
    gates = rows_from(CLAIM_GATES)
    checks = [
        ("VAL4455_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in sources if row["source_kind"] == "local"), "every cited local source path exists"),
        ("VAL4455_1_local_needles_found", all(row["needle_found"] == "True" for row in sources if row["source_kind"] == "local"), "every cited local source needle is present"),
        ("VAL4455_2_web_sources_recorded", all(row["web_source_recorded"] == "True" and row["web_verified_in_session"] == "True" for row in sources if row["source_kind"] == "web"), "web source URLs recorded"),
        ("VAL4455_3_projection_rows", all(row["current_status"] == "STANDARD_ALPHA_LAMBDA_PROJECTION_WRITTEN_MTS_OR_CURVE_MISSING" for row in projections), "projection rows written"),
        ("VAL4455_4_scale_rows", all(row["current_status"] == "PARENT_SCALE_SIGNATURE_WRITTEN_NUMERIC_VALUE_OR_ZERO_MISSING" for row in scales), "parent scale rows staged"),
        ("VAL4455_5_formula_rows", FORMULA_ROWS.exists() and "alpha_2=-4/3" in text(FORMULA_ROWS), "formula rows include spin2 projection"),
        ("VAL4455_6_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4455_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-297"),
        ("VAL4455_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4455_9_post_doc", DOC_PATH.exists() and "Private checkpoint" in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4455_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4455_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4455_12_next_target", NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4455_13_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(PROJECTION_INPUT, projection_input_rows())
    write_csv(PROJECTION_OUTPUT, [evaluate_projection_row(row) for row in rows_from(PROJECTION_INPUT)])
    write_csv(SCALE_INPUT, scale_input_rows())
    write_csv(SCALE_OUTPUT, [evaluate_parent_scale_row(row) for row in rows_from(SCALE_INPUT)])
    write_csv(FORMULA_ROWS, formula_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_csv(CLAIM_GATES, claim_gate_rows())
    write_text(FORMAL_PATH, build_doc())
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
