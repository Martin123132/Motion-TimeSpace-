from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3226-Y5-R2FR-CD-coefficient-package-or-clock-product-saturation-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3226_INPUTS.csv"
PACKAGE = OUT / "P8_Y5_R2FR_3226_CD_COEFFICIENT_PACKAGE.csv"
SATURATION = OUT / "P8_Y5_R2FR_3226_PRODUCT_SATURATION_BOUNDS.csv"
INVERSION = OUT / "P8_Y5_R2FR_3226_PROJECTION_INVERSION_TABLE.csv"
ACQUISITION = OUT / "P8_Y5_R2FR_3226_CD_ACQUISITION_TARGETS.csv"
DECISION = OUT / "P8_Y5_R2FR_3226_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3226_VALIDATION.csv"

PRODUCT_3225 = OUT / "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def maybe_float(value: object) -> float | None:
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or text.lower().startswith("missing") or text.lower() in {"not_applicable", "none", "nan"}:
            return None
        number = float(text)
        if not math.isfinite(number):
            return None
        return number
    except Exception:
        return None


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:200]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3226_00_3225_doc",
        "location": "post_checkpoint",
        "relative_path": "3225-Y5-R2FR-first-real-alpha-input-acquisition-balpha-zero-or-lambdaD-DRQ-Zmin-under-AX1090.md",
        "role": "3225 handoff and product constraints",
        "terms": ["C_D", "2.1e-18", "1.407170e-12", "3226"],
    },
    {
        "input_id": "SRC3226_01_3225_products",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv",
        "role": "clock/WEP product constraints",
        "terms": ["PC3225_0_clock_1sigma", "PC3225_2_WEP_alpha", "PC3225_3_WEP_unit_source_beta_anchor"],
    },
    {
        "input_id": "SRC3226_02_3225_finite",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3225_FINITE_INPUT_ACQUISITION_AUDIT.csv",
        "role": "missing finite input package",
        "terms": ["FI3225_0_C_D", "Delta m", "Z_min"],
    },
    {
        "input_id": "SRC3226_03_3223_formula",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv",
        "role": "finite alpha formula source",
        "terms": ["FORM3223_1_offroot_bound", "FORM3223_3_hessian_guard"],
    },
    {
        "input_id": "SRC3226_04_3224_blockers",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv",
        "role": "projection blockers",
        "terms": ["BLK3224_0_first_MTS_scalar", "BLK3224_1_clock_projection", "BLK3224_2_WEP_projection"],
    },
    {
        "input_id": "SRC3226_05_3210_amp",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "local amplitude law candidate",
        "terms": ["Y_X", "source/boundary leakage", "||X||_H1"],
    },
    {
        "input_id": "SRC3226_06_3219_hessian",
        "location": "post_checkpoint",
        "relative_path": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md",
        "role": "Hessian/coercivity guard",
        "terms": ["G_eff", "HES3219_1_coercivity_floor", "ORB3219_0_balpha_offroot"],
    },
]


PROJECTION_TIERS = [1.0, 1e-3, 1e-6, 1e-9, 1e-12, 1e-15]
CD_TIERS = [1.0, 1e-3, 1e-6, 1e-9, 1e-12, 1e-15]


def product_bound(constraint_id: str) -> float:
    for row in read_csv(PRODUCT_3225):
        if row.get("constraint_id") == constraint_id:
            value = maybe_float(row.get("numeric_bound"))
            if value is None:
                raise ValueError(f"missing numeric bound for {constraint_id}")
            return value
    raise ValueError(f"missing constraint row {constraint_id}")


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    clock_1sigma = product_bound("PC3225_0_clock_1sigma")
    clock_2sigma = product_bound("PC3225_1_clock_2sigma")
    wep_alpha = product_bound("PC3225_2_WEP_alpha")
    wep_beta = product_bound("PC3225_3_WEP_unit_source_beta_anchor")

    package_rows = [
        {
            "package_id": "CD3226_0_definition",
            "quantity": "C_D",
            "definition": "C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min",
            "units": "1/[m] after chosen memory normalization, or inverse of Delta m units",
            "role": "compact finite coefficient controlling |b_alpha_m| <= C_D |Delta m|",
            "source_status": "definition_exact_inputs_missing",
            "missing_for_claim": "lambda_D; D_m R_Q norm; Z_min; units; source paths",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "package_id": "CD3226_1_clock_product",
            "quantity": "Pi_clock := |Delta m tau_clock_time|",
            "definition": "clock product projection multiplying C_D in |dot alpha/alpha| <= C_D Pi_clock",
            "units": "clock-time convention units",
            "role": "projection factor that must not be set to one",
            "source_status": "not_derived",
            "missing_for_claim": "EM-attached Delta m and tau_clock_time",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "package_id": "CD3226_2_WEP_product",
            "quantity": "Pi_WEP := |Delta m tau_WEP beta_source_alpha|",
            "definition": "WEP projection factor multiplying C_D in the alpha/Coulomb channel",
            "units": "selected WEP projection convention",
            "role": "source/test projection factor that must not inherit clock tau",
            "source_status": "not_derived",
            "missing_for_claim": "EM-attached Delta m, tau_WEP, beta_source_alpha",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "package_id": "CD3226_3_hessian",
            "quantity": "eta_D",
            "definition": "defect-norm Hessian correction tied to C_D plus field/support norms",
            "units": "memory operator correction units",
            "role": "keeps alpha finite branch from smuggling local-GR/Maxwell stress safety",
            "source_status": "not_derived",
            "missing_for_claim": "G_mem floor, ||F_Q^2|| support norm, stress/readout bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    saturation_rows: list[dict[str, object]] = []
    for product in PROJECTION_TIERS:
        saturation_rows.append(
            {
                "sat_id": f"SAT3226_clock1_pi_{product:.0e}",
                "arena": "clock",
                "bound_source": "ACB1052_2_1sigma",
                "assumed_projection_product": f"{product:.1e}",
                "saturation_formula": "C_D_max = clock_bound_1sigma / Pi_clock",
                "C_D_max": f"{clock_1sigma / product:.6e}",
                "units": "yr^-1 divided by Pi_clock units",
                "interpretation": "diagnostic target curve only; Pi_clock is not assumed",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
        saturation_rows.append(
            {
                "sat_id": f"SAT3226_clock2_pi_{product:.0e}",
                "arena": "clock",
                "bound_source": "ACB1052_2_2sigma",
                "assumed_projection_product": f"{product:.1e}",
                "saturation_formula": "C_D_max = clock_bound_2sigma / Pi_clock",
                "C_D_max": f"{clock_2sigma / product:.6e}",
                "units": "yr^-1 divided by Pi_clock units",
                "interpretation": "diagnostic target curve only; Pi_clock is not assumed",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
        saturation_rows.append(
            {
                "sat_id": f"SAT3226_WEP_pi_{product:.0e}",
                "arena": "MICROSCOPE_WEP",
                "bound_source": "AWP1052_0_alpha_Coulomb",
                "assumed_projection_product": f"{product:.1e}",
                "saturation_formula": "C_D_max = (eta_bound/delta_Q_alpha) / Pi_WEP",
                "C_D_max": f"{wep_alpha / product:.6e}",
                "units": "dimensionless divided by Pi_WEP units",
                "interpretation": "diagnostic target curve only; Pi_WEP is not assumed",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    inversion_rows: list[dict[str, object]] = []
    for cd in CD_TIERS:
        inversion_rows.append(
            {
                "inv_id": f"INV3226_clock1_CD_{cd:.0e}",
                "arena": "clock",
                "assumed_C_D": f"{cd:.1e}",
                "max_projection_product": f"{clock_1sigma / cd:.6e}",
                "formula": "Pi_clock_max = clock_bound_1sigma / C_D",
                "units": "Pi_clock units",
                "interpretation": "if C_D is this large, Pi_clock must be no larger than this target",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
        inversion_rows.append(
            {
                "inv_id": f"INV3226_WEP_CD_{cd:.0e}",
                "arena": "MICROSCOPE_WEP",
                "assumed_C_D": f"{cd:.1e}",
                "max_projection_product": f"{wep_alpha / cd:.6e}",
                "formula": "Pi_WEP_max = (eta_bound/delta_Q_alpha) / C_D",
                "units": "Pi_WEP units",
                "interpretation": "if C_D is this large, Pi_WEP must be no larger than this target",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    acquisition_rows = [
        {
            "target_id": "ACQ3226_0_direct_CD",
            "target": "direct C_D package",
            "required_row": "C_D numeric value with units and source path",
            "why_first": "one compact row can feed clock/WEP/R10 propagators once projection products are available",
            "current_status": "MISSING",
            "claim_gate": "valid_for_claim remains false until C_D and at least one projection product are source-backed",
            "next_action": "derive/source lambda_D, D_m R_Q, Z_min or source C_D directly",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "target_id": "ACQ3226_1_clock_projection",
            "target": "Pi_clock = |Delta m tau_clock_time|",
            "required_row": "clock projection product with units/source",
            "why_first": "clock gives the tightest numeric product anchor",
            "current_status": "MISSING",
            "claim_gate": "do not set Pi_clock to unity",
            "next_action": "derive clock readout/local memory normalization",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "target_id": "ACQ3226_2_WEP_projection",
            "target": "Pi_WEP = |Delta m tau_WEP beta_source_alpha|",
            "required_row": "WEP source/test projection product with units/source",
            "why_first": "WEP provides an independent alpha/Coulomb material-channel target",
            "current_status": "MISSING",
            "claim_gate": "do not transfer clock tau into WEP",
            "next_action": "derive/source beta_source_alpha and tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "target_id": "ACQ3226_3_unit_source_beta",
            "target": "beta_source_alpha under unit-source convention",
            "required_row": f"|beta_source_alpha| <= {wep_beta:.6e} if the 1052 unit-source convention is used",
            "why_first": "gives a concrete beta target, but only under the named convention",
            "current_status": "NUMERIC_TARGET_NONCLAIM",
            "claim_gate": "requires tau_WEP and convention match before use",
            "next_action": "decide whether 1052 unit-source convention is the live WEP projection convention",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3226_0_result",
            "decision": "CD_PACKAGE_DEFINED_SATURATION_BOUNDS_DERIVED_NO_COEFFICIENT_CLAIM",
            "because": "C_D packages the finite alpha coupling and product anchors define saturation curves, but no C_D or projection product is source-backed",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM",
            "next_action": "acquire either direct C_D or the tightest projection product Pi_clock; keep all saturation rows diagnostic",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3226_1_next_target",
            "decision": "3227-Y5-R2FR-Pi-clock-or-CD-source-row-acquisition-under-AX1090",
            "because": "the product curves show that a C_D claim is impossible without at least one projection product; clock is the tightest first projection target",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "try to derive Pi_clock=|Delta m tau_clock_time| from local memory/readout normalization; fallback to direct C_D source row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, package_rows, saturation_rows, inversion_rows, acquisition_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    package_rows: list[dict[str, object]],
    saturation_rows: list[dict[str, object]],
    inversion_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, PACKAGE, SATURATION, INVERSION, ACQUISITION, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    package_defined = any(row["package_id"] == "CD3226_0_definition" for row in package_rows)
    saturation_numeric = sum(maybe_float(row["C_D_max"]) is not None for row in saturation_rows)
    inversion_numeric = sum(maybe_float(row["max_projection_product"]) is not None for row in inversion_rows)
    claims_allowed = sum(row["claim_allowed"] == "true" for row in saturation_rows + inversion_rows)
    claim_true_count = 0
    for rows in [input_rows, package_rows, saturation_rows, inversion_rows, acquisition_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])

    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3226_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3226_01_CD_package_defined", "pass": b(package_defined), "detail": "C_D := 2|lambda_D|||D_mR_Q||^2/Z_min", "generated_utc": now},
        {"check_id": "VAL3226_02_saturation_numeric", "pass": b(saturation_numeric >= 18), "detail": f"saturation_numeric={saturation_numeric}", "generated_utc": now},
        {"check_id": "VAL3226_03_inversion_numeric", "pass": b(inversion_numeric >= 12), "detail": f"inversion_numeric={inversion_numeric}", "generated_utc": now},
        {"check_id": "VAL3226_04_diagnostic_only", "pass": b(claims_allowed == 0), "detail": f"claim_allowed_rows={claims_allowed}", "generated_utc": now},
        {"check_id": "VAL3226_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3226_06_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3226_07_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3226_08_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3227-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    package_rows: list[dict[str, object]],
    saturation_rows: list[dict[str, object]],
    inversion_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3226 - C_D Coefficient Package Or Clock Product Saturation Bound under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3226 packages the finite alpha branch into one coefficient:

```text
C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min
|b_alpha_m| <= C_D |Delta m|.
```

Then the real data anchors become saturation conditions:

```text
C_D <= B_clock / Pi_clock
Pi_clock := |Delta m tau_clock_time|

C_D <= B_WEP / Pi_WEP
Pi_WEP := |Delta m tau_WEP beta_source_alpha|.
```

No projection product is assumed to be one. The saturation tables are diagnostic target curves only.

The key practical readout:

```text
If Pi_clock = 1e-6, then C_D must be <= 2.1e-12 in the clock 1sigma convention.
If Pi_WEP = 1e-6, then C_D must be <= 1.407170e-6 in the MICROSCOPE alpha/Coulomb convention.
```

So the clock product is the sharper first pressure test unless `Pi_clock` is extremely suppressed relative to `Pi_WEP`.

Current verdict: `CD_PACKAGE_DEFINED_SATURATION_BOUNDS_DERIVED_NO_COEFFICIENT_CLAIM`.

## C_D Coefficient Package

{md_table(package_rows, ["package_id", "quantity", "definition", "units", "role", "source_status", "missing_for_claim", "valid_for_claim"])}

## Product Saturation Bounds

{md_table(saturation_rows, ["sat_id", "arena", "bound_source", "assumed_projection_product", "saturation_formula", "C_D_max", "units", "interpretation", "claim_allowed", "valid_for_claim"])}

## Projection Inversion Table

{md_table(inversion_rows, ["inv_id", "arena", "assumed_C_D", "max_projection_product", "formula", "units", "interpretation", "claim_allowed", "valid_for_claim"])}

## C_D Acquisition Targets

{md_table(acquisition_rows, ["target_id", "target", "required_row", "why_first", "current_status", "claim_gate", "next_action", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_CD_COEFFICIENT_PACKAGE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_PRODUCT_SATURATION_BOUNDS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_PROJECTION_INVERSION_TABLE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_CD_ACQUISITION_TARGETS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3226_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, package_rows, saturation_rows, inversion_rows, acquisition_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (PACKAGE, package_rows),
        (SATURATION, saturation_rows),
        (INVERSION, inversion_rows),
        (ACQUISITION, acquisition_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, package_rows, saturation_rows, inversion_rows, acquisition_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, package_rows, saturation_rows, inversion_rows, acquisition_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
