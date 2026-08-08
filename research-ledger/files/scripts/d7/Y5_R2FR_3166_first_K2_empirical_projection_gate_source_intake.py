from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3166_INPUTS.csv"
SOURCES = OUT / "P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv"
GATE = OUT / "P8_Y5_R2FR_3166_K2_GAMMA_EMPIRICAL_GATE.csv"
PROJECTION = OUT / "P8_Y5_R2FR_3166_PI_GAMMA_PROJECTION_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3166_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3166_VALIDATION.csv"

CASSINI_GAMMA_MINUS_ONE_CENTRAL = 2.1e-5
CASSINI_GAMMA_MINUS_ONE_SIGMA = 2.3e-5


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        for row in rows:
            writer.writerow(row)


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def csv_value(path: Path, key: str, value: str, column: str) -> str:
    for row in read_csv(path):
        if row.get(key) == value:
            return row[column]
    raise KeyError(f"missing {key}={value} in {path}")


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md", "3165 K2 residual-vector gate"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv", "C_K2_unit value"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3165_PPN_CLOCK_ORBITAL_GATES.csv", "PPN gamma gate formula"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv", "internal K2 cap"),
    ]
    return [
        {
            "input_id": f"IN3166_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def source_rows() -> list[dict[str, object]]:
    now = stamp()
    abs_1sigma = abs(CASSINI_GAMMA_MINUS_ONE_CENTRAL) + CASSINI_GAMMA_MINUS_ONE_SIGMA
    abs_2sigma = abs(CASSINI_GAMMA_MINUS_ONE_CENTRAL) + 2.0 * CASSINI_GAMMA_MINUS_ONE_SIGMA
    return [
        {
            "source_id": "SRC3166_0_cassini_primary",
            "observable": "PPN_gamma_minus_one",
            "paper": "Bertotti, Iess, Tortora, A test of general relativity using radio links with the Cassini spacecraft",
            "journal": "Nature 425, 374-376 (2003)",
            "doi": "10.1038/nature01997",
            "source_url": "https://ilorentz.org/research/vanbaal/DECEASED/ART/gr-test.pdf",
            "source_line_ref": "PDF result equation for gamma_minus_one; PubMed DOI index records the same paper",
            "central_value": fmt(CASSINI_GAMMA_MINUS_ONE_CENTRAL),
            "one_sigma": fmt(CASSINI_GAMMA_MINUS_ONE_SIGMA),
            "abs_envelope_1sigma": fmt(abs_1sigma),
            "abs_envelope_2sigma": fmt(abs_2sigma),
            "use_in_3166": "default diagnostic uses abs_envelope_2sigma; all rows remain nonclaim until Pi_gamma_K2 is derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "source_id": "SRC3166_1_pubmed_index",
            "observable": "bibliographic_index",
            "paper": "A test of general relativity using radio links with the Cassini spacecraft",
            "journal": "Nature 425, 374-376 (2003)",
            "doi": "10.1038/nature01997",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "source_line_ref": "PubMed index/DOI; page may require browser check",
            "central_value": "not_applicable",
            "one_sigma": "not_applicable",
            "abs_envelope_1sigma": "not_applicable",
            "abs_envelope_2sigma": "not_applicable",
            "use_in_3166": "bibliographic provenance only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def values() -> dict[str, float]:
    unit = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv",
            "unit_id",
            "KU3165_0_definition",
            "value",
        )
    )
    internal_cap = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv",
            "quantity",
            "K_2",
            "required_bound_l2",
        )
    )
    return {
        "unit": unit,
        "internal_cap": internal_cap,
        "central": CASSINI_GAMMA_MINUS_ONE_CENTRAL,
        "sigma": CASSINI_GAMMA_MINUS_ONE_SIGMA,
        "abs_1sigma": abs(CASSINI_GAMMA_MINUS_ONE_CENTRAL) + CASSINI_GAMMA_MINUS_ONE_SIGMA,
        "abs_2sigma": abs(CASSINI_GAMMA_MINUS_ONE_CENTRAL) + 2.0 * CASSINI_GAMMA_MINUS_ONE_SIGMA,
    }


def gate_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    unit = v["unit"]
    internal_cap = v["internal_cap"]
    bounds = [
        ("KG3166_0_sigma_sensitivity", "one_sigma_uncertainty", v["sigma"], "strict sensitivity diagnostic; ignores central offset"),
        ("KG3166_1_abs_1sigma", "abs_central_plus_1sigma", v["abs_1sigma"], "absolute one-sigma envelope diagnostic"),
        ("KG3166_2_abs_2sigma_default", "abs_central_plus_2sigma", v["abs_2sigma"], "default conservative nonclaim diagnostic"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, bound_name, bound, use in bounds:
        k2_unit_pi = bound / unit
        rows.append(
            {
                "gate_id": gate_id,
                "observable": "PPN_gamma_minus_one_Cassini_Shapiro",
                "bound_name": bound_name,
                "gamma_abs_bound": fmt(bound),
                "C_K2_unit": fmt(unit),
                "Pi_gamma_K2": "1.0_DIAGNOSTIC_NOT_DERIVED",
                "K2_bound_unit_projection": fmt(k2_unit_pi),
                "ratio_to_internal_AX1090_K2_cap": fmt(k2_unit_pi / internal_cap),
                "formula": "K2 <= gamma_abs_bound/(|Pi_gamma_K2|*C_K2_unit)",
                "use": use,
                "status": "source_backed_bound_unit_projection_nonclaim",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    projection_owner_residual = unit
    rows.append(
        {
            "gate_id": "KG3166_3_projection_owner_K2_equals_1",
            "observable": "PPN_gamma_minus_one_Cassini_Shapiro",
            "bound_name": "projection_owner_smoke",
            "gamma_abs_bound": fmt(v["abs_2sigma"]),
            "C_K2_unit": fmt(unit),
            "Pi_gamma_K2": "1.0_DIAGNOSTIC_NOT_DERIVED",
            "K2_bound_unit_projection": "not_applicable",
            "ratio_to_internal_AX1090_K2_cap": "not_applicable",
            "residual_if_K2_equals_1": fmt(projection_owner_residual),
            "ratio_to_default_abs_2sigma_bound": fmt(projection_owner_residual / v["abs_2sigma"]),
            "formula": "Delta_gamma_K2 = C_K2_unit if K2=Pi_gamma_K2=1",
            "use": "natural projection-owner smoke case; nonclaim until parent Wbar/M_Lambda and Pi_gamma_K2 close",
            "status": "projection_owner_smoke_safe_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    )
    return rows


def projection_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "projection_id": "PG3166_0_general_gate",
            "quantity": "Pi_gamma_K2",
            "definition": "projection/readout kernel mapping K2 l=2 residual coefficient into PPN gamma_minus_1 in the Cassini/Shapiro convention",
            "current_value": "MISSING_DERIVED_KERNEL",
            "gate_formula": "K2 <= gamma_abs_bound/(|Pi_gamma_K2|*C_K2_unit)",
            "default_gamma_bound": fmt(v["abs_2sigma"]),
            "default_C_K2_unit": fmt(v["unit"]),
            "status": "kernel_missing_claim_blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "PG3166_1_unit_projection_diagnostic",
            "quantity": "Pi_gamma_K2_unit_diagnostic",
            "definition": "diagnostic assumption Pi_gamma_K2=1 used only to size the gate",
            "current_value": "1.0_DIAGNOSTIC",
            "gate_formula": "K2 <= gamma_abs_bound/C_K2_unit",
            "default_gamma_bound": fmt(v["abs_2sigma"]),
            "default_C_K2_unit": fmt(v["unit"]),
            "status": "diagnostic_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "PG3166_2_claim_requirement",
            "quantity": "Cassini_K2_gamma_claim_requirements",
            "definition": "requirements before any gamma/Shapiro empirical pass can be claimed",
            "current_value": "UNSATISFIED",
            "gate_formula": "derive Pi_gamma_K2; source empirical bound; choose confidence envelope; verify K2 lane is the only active gamma residual or combine no-cancellation vector",
            "default_gamma_bound": fmt(v["abs_2sigma"]),
            "default_C_K2_unit": fmt(v["unit"]),
            "status": "claim_blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    default_k2 = v["abs_2sigma"] / v["unit"]
    return [
        {
            "decision_id": "D3166_0_first_empirical_gate",
            "decision": "Cassini/Shapiro gamma gives the first source-backed empirical K2 gate",
            "evidence": "gamma-1=(2.1 +/- 2.3)e-5 from Bertotti/Iess/Tortora 2003; default abs+2sigma envelope used",
            "effect": f"unit-projection diagnostic gives K2 <= {fmt(default_k2)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3166_1_tighter_than_internal",
            "decision": "the unit-projection Cassini diagnostic is tighter than the internal AX1090 cap",
            "evidence": f"ratio_to_internal_cap={fmt(default_k2 / v['internal_cap'])}",
            "effect": "gamma/Shapiro should be the first empirical local gate once Pi_gamma_K2 is derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3166_2_next_attack",
            "decision": "derive Pi_gamma_K2 or explicitly keep the Cassini gate as a unit-projection smoke row",
            "evidence": "PG3166_0 marks Pi_gamma_K2 missing",
            "effect": "next checkpoint should attempt the gamma/Shapiro projection kernel from the public metric l=2 lane",
            "next_action": "3167-Y5-R2FR-Pi-gamma-K2-Shapiro-projection-kernel-or-unit-smoke-only-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    sources: list[dict[str, object]],
    gates: list[dict[str, object]],
    projections: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    source_ok = any(row["source_id"] == "SRC3166_0_cassini_primary" and row["doi"] == "10.1038/nature01997" for row in sources)
    bounds_positive = all(
        row["gate_id"] == "KG3166_3_projection_owner_K2_equals_1"
        or float(str(row["gamma_abs_bound"])) > 0.0 and float(str(row["K2_bound_unit_projection"])) > 0.0
        for row in gates
    )
    default_gate = next(row for row in gates if row["gate_id"] == "KG3166_2_abs_2sigma_default")
    default_tighter = float(str(default_gate["ratio_to_internal_AX1090_K2_cap"])) < 1.0
    claim_block = any(row["status"] == "kernel_missing_claim_blocked" for row in projections)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, sources, gates, projections, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3166_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3166_1_cassini_source_recorded",
            "status": "pass" if source_ok else "fail",
            "detail": "Cassini DOI/source row present",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3166_2_bounds_positive",
            "status": "pass" if bounds_positive else "fail",
            "detail": "gamma bounds and unit-projection K2 limits positive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3166_3_default_tighter_than_internal",
            "status": "pass" if default_tighter else "fail",
            "detail": "default abs+2sigma Cassini diagnostic tighter than internal AX1090 cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3166_4_claim_block_retained",
            "status": "pass" if claim_block else "fail",
            "detail": "Pi_gamma_K2 missing claim block retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3166_5_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3166 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    v = values()
    inputs = input_rows()
    sources = source_rows()
    gates = gate_rows(v)
    projections = projection_rows(v)
    decisions = decision_rows(v)
    validations = validation_rows(inputs, sources, gates, projections, decisions)
    write_csv(INPUTS, inputs)
    write_csv(SOURCES, sources)
    write_csv(GATE, gates)
    write_csv(PROJECTION, projections)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3166 validation failed: {failures}")


if __name__ == "__main__":
    main()
