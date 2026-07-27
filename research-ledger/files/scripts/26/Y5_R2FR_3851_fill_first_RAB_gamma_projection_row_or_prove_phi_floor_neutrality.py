from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 50

CHECKPOINT = "3851"
BRANCH = "MTS_R2FR_Y5_FILL_FIRST_RAB_GAMMA_PROJECTION_ROW_OR_PROVE_PHI_FLOOR_NEUTRALITY_3851"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3851-Y5-R2FR-fill-first-RAB-gamma-projection-row-or-prove-phi-floor-neutrality.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3850_RESPONSE = OUT / "P8_Y5_R2FR_3850_RAB_TO_GAMMA_RESPONSE_DERIVATION.csv"
CSV_3850_CONTRACT = OUT / "P8_Y5_R2FR_3850_GAMMA_BOUND_CONTRACT.csv"
CSV_3850_INPUT = OUT / "P8_Y5_R2FR_3850_PPN_PROJECTION_INPUT_ROW.csv"
CSV_3850_VALIDATION = OUT / "P8_Y5_BRR545_3850_VALIDATION.csv"
CSV_3849_HAIR = OUT / "P8_Y5_R2FR_3849_RAB_HAIR_SOURCE_ROW.csv"
CSV_3849_NEUTRALITY = OUT / "P8_Y5_R2FR_3849_RECIPROCAL_NEUTRALITY_THEOREM.csv"
CSV_LOCAL_BOUNDS = PCW / "source-intake" / "local_bounds" / "local_bound_claims.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3851_SOURCE_REGISTER.csv",
    "constants": OUT / "P8_Y5_R2FR_3851_CASSINI_GEOMETRY_CONSTANTS.csv",
    "projection": OUT / "P8_Y5_R2FR_3851_FIRST_RAB_GAMMA_NUMERIC_PROJECTION_ROW.csv",
    "budget": OUT / "P8_Y5_R2FR_3851_RAB_BUDGET_FROM_CASSINI_NEAR_LIMB.csv",
    "neutrality": OUT / "P8_Y5_R2FR_3851_NEUTRALITY_VS_FINITE_HAIR_DECISION.csv",
    "gates": OUT / "P8_Y5_R2FR_3851_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3851_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3851_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3851_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3851_VALIDATION.csv",
}

LOCAL_SOURCE_SPECS = [
    ("SRC3851_L0_3850_response", CSV_3850_RESPONSE, "RGR3850_3_safe_bound"),
    ("SRC3851_L1_3850_contract", CSV_3850_CONTRACT, "GBC3850_0_threshold_source"),
    ("SRC3851_L2_3850_input", CSV_3850_INPUT, "MISSING_B_RAB"),
    ("SRC3851_L3_3850_validation", CSV_3850_VALIDATION, "PASS"),
    ("SRC3851_L4_3849_hair", CSV_3849_HAIR, "R_AB_hair_envelope"),
    ("SRC3851_L5_3849_neutrality", CSV_3849_NEUTRALITY, "RNT3849_2_zero_chain"),
    ("SRC3851_L6_local_gamma_bound", CSV_LOCAL_BOUNDS, "Cassini_Shapiro_gamma_2003"),
]

WEB_SOURCE_SPECS = [
    (
        "SRC3851_W0_Cassini_bmin",
        "https://pds-geosciences.wustl.edu/radiosciencedocs/urn-nasa-pds-radiosci_documentation/DOCUMENT/asmar.2014.pdf",
        "Cassini Radio Science Users Guide reports the 2002 conjunction minimum impact parameter as 1.6 solar radii.",
    ),
    (
        "SRC3851_W1_Cassini_gamma",
        "https://www.nature.com/articles/nature01997",
        "Bertotti, Iess, and Tortora Nature 2003/Cassini gamma measurement; local row stores gamma-1=(2.1 +/- 2.3)e-5.",
    ),
    (
        "SRC3851_W2_IAU_2015_B3",
        "https://www.iau.org/common/Uploaded%20files/IAUGA2015-Resolution-B3-recommended-nominal-conversion.pdf",
        "IAU Resolution B3 nominal solar radius 6.957e8 m and nominal solar mass parameter 1.3271244e20 m^3 s^-2.",
    ),
    (
        "SRC3851_W3_BIPM_c",
        "https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf",
        "SI Brochure fixes the speed of light in vacuum at c=299792458 m/s.",
    ),
]

C_LIGHT = Decimal("299792458")
MU_SUN_N = Decimal("1.3271244e20")
R_SUN_N = Decimal("6.957e8")
BMIN_SOLAR_RADII = Decimal("1.6")
THETA_GAMMA = Decimal("2.3e-5")

PHI_FORMULA = "phi_b=GM_sun_N/(c^2*b_min), b_min=1.6*R_sun_N"
BUDGET_FORMULA = "B_RAB_budget_zero_other=ln(1+2*phi_b*T2_b*theta_gamma)"
CLAIM_FORMULA = "claim requires B_RAB <= ln(1+2*phi_floor*T2_floor*(theta_gamma-B_other)) with B_other>=0 and theta_gamma>B_other"


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


def fmt_decimal(value: Decimal, digits: int = 15) -> str:
    return f"{float(value):.{digits}e}"


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
    for row in read_csv_rows(CSV_LOCAL_BOUNDS):
        if row.get("row_id") == "R3_gamma":
            return row
    raise RuntimeError("R3_gamma row missing")


def computed_values() -> dict[str, Decimal]:
    b_min_m = BMIN_SOLAR_RADII * R_SUN_N
    phi_b = MU_SUN_N / (C_LIGHT * C_LIGHT * b_min_m)
    t2_b = Decimal(1) - Decimal(2) * phi_b
    linear_budget = Decimal(2) * phi_b * t2_b * THETA_GAMMA
    exact_budget = Decimal(str(math.log1p(float(linear_budget))))
    return {
        "b_min_m": b_min_m,
        "phi_b": phi_b,
        "T2_b": t2_b,
        "linear_budget": linear_budget,
        "exact_budget": exact_budget,
    }


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle in LOCAL_SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local",
                "path_or_url": rel(path),
                "exists_or_url_recorded": exists,
                "needle_or_extraction_note": needle,
                "needle_found": needle in text,
                "role": "input_for_first_RAB_gamma_projection_row",
                "claim_use": "nonclaim_numeric_denominator_and_budget_only",
                "timestamp_utc": timestamp,
            }
        )
    for source_id, url, note in WEB_SOURCE_SPECS:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "web",
                "path_or_url": url,
                "exists_or_url_recorded": url.startswith("https://"),
                "needle_or_extraction_note": note,
                "needle_found": True,
                "role": "external_provenance_for_constants_or_Cassini_geometry",
                "claim_use": "source_string_recorded_not_full_kernel_claim",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def constants_rows(timestamp: str) -> list[dict[str, object]]:
    values = computed_values()
    return [
        {
            "constant_id": "CGC3851_0_bmin_factor",
            "symbol": "b_min/R_sun_N",
            "value": str(BMIN_SOLAR_RADII),
            "units": "dimensionless",
            "formula": "Cassini 2002 conjunction minimum impact parameter",
            "source_id": "SRC3851_W0_Cassini_bmin",
            "status": "SOURCE_BACKED_CASSINI_GEOMETRY_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constant_id": "CGC3851_1_Rsun_nominal",
            "symbol": "R_sun_N",
            "value": fmt_decimal(R_SUN_N),
            "units": "m",
            "formula": "IAU nominal solar radius",
            "source_id": "SRC3851_W2_IAU_2015_B3",
            "status": "SOURCE_BACKED_NOMINAL_CONVERSION_CONSTANT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constant_id": "CGC3851_2_mu_sun_nominal",
            "symbol": "GM_sun_N",
            "value": fmt_decimal(MU_SUN_N),
            "units": "m^3 s^-2",
            "formula": "IAU nominal solar mass parameter",
            "source_id": "SRC3851_W2_IAU_2015_B3",
            "status": "SOURCE_BACKED_NOMINAL_CONVERSION_CONSTANT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constant_id": "CGC3851_3_c",
            "symbol": "c",
            "value": str(C_LIGHT),
            "units": "m s^-1",
            "formula": "SI exact speed of light",
            "source_id": "SRC3851_W3_BIPM_c",
            "status": "SOURCE_BACKED_EXACT_SI_CONSTANT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constant_id": "CGC3851_4_bmin_m",
            "symbol": "b_min",
            "value": fmt_decimal(values["b_min_m"]),
            "units": "m",
            "formula": "b_min=1.6*R_sun_N",
            "source_id": "CGC3851_0_bmin_factor;CGC3851_1_Rsun_nominal",
            "status": "DERIVED_GEOMETRY_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constant_id": "CGC3851_5_phi_b",
            "symbol": "phi_b",
            "value": fmt_decimal(values["phi_b"]),
            "units": "dimensionless",
            "formula": PHI_FORMULA,
            "source_id": "CGC3851_2_mu_sun_nominal;CGC3851_3_c;CGC3851_4_bmin_m",
            "status": "DERIVED_NEAR_LIMB_DENOMINATOR_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constant_id": "CGC3851_6_T2_b",
            "symbol": "T2_b",
            "value": fmt_decimal(values["T2_b"]),
            "units": "dimensionless",
            "formula": "T2_b=1-2*phi_b",
            "source_id": "CGC3851_5_phi_b",
            "status": "DERIVED_NEAR_LIMB_BRANCH_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def projection_rows(timestamp: str) -> list[dict[str, object]]:
    gamma = gamma_bound_row()
    values = computed_values()
    return [
        {
            "projection_id": "PPR3851_0_Cassini_near_limb_RAB_row",
            "arena": "Cassini_Shapiro_gamma_2003_near_limb_scalar_proxy",
            "phi_floor": fmt_decimal(values["phi_b"]),
            "T2_floor": fmt_decimal(values["T2_b"]),
            "theta_gamma": gamma["upper_bound"],
            "B_other": "MISSING_B_areal_to_PPN+B_domain+B_norm+B_higher_order+kernel_error",
            "B_RAB_budget_if_B_other_zero": fmt_decimal(values["exact_budget"]),
            "acceptance_formula": CLAIM_FORMULA,
            "source_path": rel(CSV_3849_HAIR),
            "geometry_source": "SRC3851_W0_Cassini_bmin;SRC3851_W2_IAU_2015_B3;SRC3851_W3_BIPM_c",
            "status": "PARTIAL_NUMERIC_DENOMINATOR_FILLED_B_RAB_AND_KERNEL_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "projection_id": "PPR3851_1_parent_neutrality_zero_route",
            "arena": "local_exterior_neutrality_branch",
            "phi_floor": "not_needed_if_B_RAB_zero",
            "T2_floor": fmt_decimal(values["T2_b"]),
            "theta_gamma": gamma["upper_bound"],
            "B_other": "still needs full no-slip/readout for full gamma claim",
            "B_RAB_budget_if_B_other_zero": "0 contribution if Pi_R=J_R=Pi_R_ct=Delta_R_boundary=Delta_W=0",
            "acceptance_formula": "parent-signed neutrality => B_RAB=0; then R_AB hair contribution passes automatically",
            "source_path": rel(CSV_3849_NEUTRALITY),
            "geometry_source": "not_required_for_zero_contribution",
            "status": "BEST_ROUTE_BUT_PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def budget_rows(timestamp: str) -> list[dict[str, object]]:
    values = computed_values()
    return [
        {
            "budget_id": "RBC3851_0_near_limb_scalar_budget",
            "formula": BUDGET_FORMULA,
            "input_phi_b": fmt_decimal(values["phi_b"]),
            "input_T2_b": fmt_decimal(values["T2_b"]),
            "input_theta_gamma": str(THETA_GAMMA),
            "linear_small_bound": fmt_decimal(values["linear_budget"]),
            "exact_log_bound": fmt_decimal(values["exact_budget"]),
            "interpretation": "if all other projection/gauge/domain/kernel terms were zero, Cassini near-limb scalar comparison would require B_RAB below about 6.1e-11",
            "status": "NUMERIC_PRESSURE_RESULT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "budget_id": "RBC3851_1_with_other_terms",
            "formula": "B_RAB <= ln(1+2*phi_b*T2_b*(theta_gamma-B_other))",
            "input_phi_b": fmt_decimal(values["phi_b"]),
            "input_T2_b": fmt_decimal(values["T2_b"]),
            "input_theta_gamma": str(THETA_GAMMA),
            "linear_small_bound": "2*phi_b*T2_b*(theta_gamma-B_other)",
            "exact_log_bound": "requires theta_gamma>B_other",
            "interpretation": "any nonzero gauge/domain/kernel/no-slip budget makes the allowed R_AB hair even smaller",
            "status": "STRICTER_IF_OTHER_TERMS_NONZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def neutrality_rows(timestamp: str) -> list[dict[str, object]]:
    values = computed_values()
    return [
        {
            "decision_id": "NFD3851_0_finite_hair_pressure",
            "route": "finite R_AB hair",
            "required_new_input": "source-backed B_RAB <= " + fmt_decimal(values["exact_budget"]) + " plus full Cassini kernel/gauge/domain terms",
            "current_status": "NOT_FILLED",
            "route_score": "hard_but_now_quantified",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "NFD3851_1_neutrality_zero_pressure",
            "route": "parent reciprocal neutrality",
            "required_new_input": "prove Pi_R=J_R=Pi_R_ct=Delta_R_boundary=Delta_W=0 on the exterior source branch",
            "current_status": "UNSIGNED_BUT_BEST_ROUTE",
            "route_score": "mathematically_preferred_after_6e-11_budget",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3851_0_geometry_constants",
            "gate": "Cassini near-limb geometry constants",
            "status": "PASS_SOURCE_STRINGS_AND_DERIVED_VALUES_RECORDED",
            "claim_allowed": False,
            "reason": "b_min, R_sun_N, GM_sun_N, c, phi_b, and T2_b are recorded with provenance",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3851_1_numeric_RAB_budget",
            "gate": "first R_AB gamma numeric budget",
            "status": "PASS_NONCLAIM_NUMERIC_PRESSURE_ROW",
            "claim_allowed": False,
            "reason": "zero-other-term near-limb budget is about 6.1e-11",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3851_2_B_RAB_source",
            "gate": "B_RAB value or theorem zero",
            "status": "BLOCKED_MISSING_B_RAB_OR_PARENT_NEUTRALITY",
            "claim_allowed": False,
            "reason": "3849 hair row still has no source-backed numeric B_RAB and no parent zero signature",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3851_3_Cassini_kernel",
            "gate": "full Cassini Shapiro/radio kernel projection",
            "status": "BLOCKED_NEAR_LIMB_PROXY_NOT_FULL_KERNEL",
            "claim_allowed": False,
            "reason": "a claim needs the path-integrated Shapiro/radio observable, not only a near-limb scalar denominator",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3851_4_scope_guard",
            "gate": "full local GR/PPN claim",
            "status": "BLOCKED_GAMMA_COMPONENT_ONLY",
            "claim_allowed": False,
            "reason": "Newton/source normalization, beta, no-slip/readout, and EM/source coupling remain separate gates",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3851_0",
            "decision": "finite R_AB hair is numerically under severe Cassini pressure",
            "consequence": "without a theorem zero, the source row must deliver B_RAB at roughly 1e-10 or below before other residuals",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3851_1",
            "decision": "the best physics route is now the parent neutrality/no-hair proof",
            "consequence": "trying to carry finite reciprocal hair through PPN is possible but likely ugly and very constrained",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3851_2",
            "decision": "do not overclaim the numeric row",
            "consequence": "near-limb scalar denominator is a budget scout; full Cassini kernel projection remains a later empirical gate",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3851_0",
            "next_checkpoint": "3852-Y5-R2FR-parent-neutrality-signature-for-RAB-zero-or-finite-hair-source-row.md",
            "script": "scripts/Y5_R2FR_3852_parent_neutrality_signature_for_RAB_zero_or_finite_hair_source_row.py",
            "objective": "derive the parent action/signature that sets Pi_R=J_R=0 for the reciprocal exterior branch, or source a finite B_RAB row tight enough for the 3851 Cassini pressure budget",
            "reason": "3851 shows finite R_AB hair must be extremely small in the solar gamma lane; proving R_AB=0 is now the cleanest route",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    values = computed_values()
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_FIRST_RAB_GAMMA_NUMERIC_PRESSURE_ROW",
            "claim": "no Cassini, gamma, PPN, Newton, beta, R_AB zero, or local-GR claim",
            "numeric_pressure": "B_RAB_zero_other_budget=" + fmt_decimal(values["exact_budget"]),
            "next": "3852 parent neutrality signature or finite B_RAB source row",
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
    constants: list[dict[str, object]],
    projection: list[dict[str, object]],
    budget: list[dict[str, object]],
    neutrality: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    values = computed_values()
    text = f"""# 3851 - Fill First R_AB Gamma Projection Row Or Prove Phi-Floor Neutrality

Private checkpoint. This fills the first actual denominator/budget row for the 3850 `R_AB -> gamma` response, using the Cassini near-limb geometry as a nonclaim scalar proxy.

Generated: `{timestamp}`

## Result

Using the Cassini 2002 conjunction near-limb geometry:

`b_min = 1.6 R_sun_N = {fmt_decimal(values["b_min_m"])} m`.

With IAU nominal `GM_sun_N`, IAU nominal `R_sun_N`, and exact SI `c`:

`{PHI_FORMULA} = {fmt_decimal(values["phi_b"])}`.

The local branch value is:

`T2_b = 1 - 2 phi_b = {fmt_decimal(values["T2_b"])}`.

If all other gauge/domain/readout/kernel terms were zero, the Cassini `theta_gamma=2.3e-5` row would require:

`{BUDGET_FORMULA} = {fmt_decimal(values["exact_budget"])}`.

So the practical message is sharp: finite `R_AB` hair is under roughly `6.1e-11` pressure in this near-limb gamma lane before any other residuals are paid. That makes the parent neutrality/no-hair proof the clean route; the finite-hair route now has a real number to beat.

This is not a claim. It is a sourced budget scout. A public or internal pass still needs real `B_RAB`, a full Cassini path-integrated Shapiro/radio kernel, and gauge/domain/normalization/no-slip/readout residual rows.

## Source Register

{markdown_table(sources, ["source_id", "source_type", "path_or_url", "exists_or_url_recorded", "needle_found", "role"])}

## Geometry Constants

{markdown_table(constants, ["constant_id", "symbol", "value", "units", "formula", "status"])}

## First Projection Rows

{markdown_table(projection, ["projection_id", "arena", "phi_floor", "T2_floor", "B_RAB_budget_if_B_other_zero", "status"])}

## R_AB Budget

{markdown_table(budget, ["budget_id", "formula", "input_phi_b", "input_T2_b", "exact_log_bound", "status"])}

## Neutrality Versus Finite Hair

{markdown_table(neutrality, ["decision_id", "route", "required_new_input", "current_status", "route_score"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This checkpoint stops the circling and puts a number on the local gamma throat. If MTS keeps finite reciprocal hair, it must be tiny in the solar-system lane. The better route is to derive the `R_AB=0` exterior neutrality result from the parent action, then use finite rows only as fallback.

Next target: `3852-Y5-R2FR-parent-neutrality-signature-for-RAB-zero-or-finite-hair-source-row.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    values = computed_values()
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3850", "Current State After 3851", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3851 at ")
    )
    paragraph = (
        "`3851` fills the first numeric denominator/budget row for the `R_AB -> gamma` response. "
        f"Using Cassini's near-limb `b_min=1.6R_sun`, IAU nominal solar constants, and exact SI `c`, it gets `phi_b={fmt_decimal(values['phi_b'])}` and `T2_b={fmt_decimal(values['T2_b'])}`. "
        f"With the existing Cassini `theta_gamma=2.3e-5` row, the zero-other-residual near-limb scalar budget is `B_RAB <= {fmt_decimal(values['exact_budget'])}`. "
        "This is a nonclaim budget scout, not a full Cassini kernel projection, but it strongly pressures the branch toward proving parent reciprocal neutrality/no-hair rather than carrying finite R_AB hair through PPN.\n\n"
    )
    anchor = "`3850` derives"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3851-Y5-R2FR-fill-first-RAB-gamma-projection-row-or-prove-phi-floor-neutrality.md`

Target: fill the first claim-gated R_AB-to-gamma projection row with `B_RAB`, `phi_floor`, `T2_floor`, gauge/domain/normalization bounds, or prove the parent neutrality zero route.

This is the best next move because 3850 has derived the response law; now the numerator/projection row or no-hair signature must be supplied."""
    new_gate = """`3852-Y5-R2FR-parent-neutrality-signature-for-RAB-zero-or-finite-hair-source-row.md`

Target: derive the parent action/signature that sets `Pi_R=J_R=0` for the reciprocal exterior branch, or source a finite `B_RAB` row tight enough for the 3851 Cassini pressure budget.

This is the best next move because 3851 makes the finite-hair route quantitatively severe; no-hair neutrality is the clean path."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3851_CASSINI_GEOMETRY_CONSTANTS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3851_FIRST_RAB_GAMMA_NUMERIC_PROJECTION_ROW.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3851_RAB_BUDGET_FROM_CASSINI_NEAR_LIMB.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3851_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3851_CASSINI_GEOMETRY_CONSTANTS.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3851 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    constants: list[dict[str, object]],
    projection: list[dict[str, object]],
    budget: list[dict[str, object]],
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

    values = computed_values()
    all_text = " ".join(str(row) for row in constants + projection + budget + gates)
    local_sources = [row for row in sources if row["source_type"] == "local"]
    web_sources = [row for row in sources if row["source_type"] == "web"]
    add(
        "VAL3851_0_local_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists_or_url_recorded"] and row["needle_found"] for row in local_sources),
        f"{sum(1 for row in local_sources if row['exists_or_url_recorded'] and row['needle_found'])}/{len(local_sources)} local sources resolved",
    )
    add(
        "VAL3851_1_web_sources",
        "all web source strings are recorded",
        all(str(row["path_or_url"]).startswith("https://") and row["needle_or_extraction_note"] for row in web_sources),
        f"{len(web_sources)} web source strings recorded",
    )
    add("VAL3851_2_phi_numeric", "phi_b numeric value is present and positive", fmt_decimal(values["phi_b"]) in all_text and values["phi_b"] > 0, fmt_decimal(values["phi_b"]))
    add("VAL3851_3_T2_numeric", "T2_b numeric value is present and positive", fmt_decimal(values["T2_b"]) in all_text and values["T2_b"] > 0, fmt_decimal(values["T2_b"]))
    add("VAL3851_4_budget_numeric", "R_AB budget is present and very small", fmt_decimal(values["exact_budget"]) in all_text and values["exact_budget"] < Decimal("1e-9"), fmt_decimal(values["exact_budget"]))
    add("VAL3851_5_missing_BRAB", "B_RAB claim remains blocked", "B_RAB_AND_KERNEL_MISSING" in all_text or "MISSING_B_areal_to_PPN" in all_text, "missing B_RAB/kernel blockers retained")
    add("VAL3851_6_nonclaim", "all 3851 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in constants + projection + budget + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3851_7_next", "next target is 3852", DOC_PATH.exists() and "3852-Y5-R2FR-parent-neutrality-signature-for-RAB-zero-or-finite-hair-source-row" in read_text(DOC_PATH), "3852 target visible")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3851_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3851_9_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "roughly `6.1e-11` pressure" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3851*", "P8_Y5_BRR545_3851*", "*Y5_R2FR_3851*", "3851-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3851_10_formalization_clean", "formalization-workbench has no generated 3851 project files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3851 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3851_11_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    constants = constants_rows(timestamp)
    projection = projection_rows(timestamp)
    budget = budget_rows(timestamp)
    neutrality = neutrality_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["constants"], constants)
    write_csv(OUTPUTS["projection"], projection)
    write_csv(OUTPUTS["budget"], budget)
    write_csv(OUTPUTS["neutrality"], neutrality)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, constants, projection, budget, neutrality, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, constants, projection, budget, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_FIRST_RAB_GAMMA_NUMERIC_PRESSURE_ROW")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
