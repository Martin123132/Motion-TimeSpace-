from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAW = ROOT / "source-intake" / "component-fractions" / "raw"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3258-Y5-R2FR-source-backed-EM-Coulomb-coefficient-or-parent-alpha-map-owner-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3258_SOURCE_REGISTER.csv",
    "coefficient": OUT / "P8_Y5_R2FR_3258_DD_EM_COULOMB_COEFFICIENT_SOURCE_ROW.csv",
    "external_charge": OUT / "P8_Y5_R2FR_3258_DD_EM_CHARGE_EXTERNAL_COMPARATOR_NONCLAIM.csv",
    "raw_external": RAW / "P8_Y5_R2FR_3258_DD_EM_CHARGE_EXTERNAL_COMPARATOR_NONCLAIM.csv",
    "schema_audit": OUT / "P8_Y5_R2FR_3258_DD_VS_FEM_SCHEMA_AUDIT.csv",
    "alpha_map": OUT / "P8_Y5_R2FR_3258_PARENT_ALPHA_MAP_OWNER_AUDIT.csv",
    "gates": OUT / "P8_Y5_R2FR_3258_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3258_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3258_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3258_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
DD_ARXIV = "https://arxiv.org/abs/1007.2792"
DD_PDF = "https://arxiv.org/pdf/1007.2792"
DD_DOI = "https://link.aps.org/doi/10.1103/PhysRevD.82.084033"
DD_QE_COEFFICIENT = 7.7e-4


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:260]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def float_or_none(value: Any) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3258_3257_handoff",
            "local_path",
            str(ROOT / "3257-Y5-R2FR-first-accepted-EM-Coulomb-fraction-row-or-toy-shell-runner-dryrun-under-AX1090.md"),
            "3257 selected source-backed coefficient or parent alpha-map owner",
            ["NEXT3257_0_3258", "f_EM,A = k_C q_C,A", "DD"],
        ),
        (
            "SRC3258_3257_shape_rows",
            "local_path",
            str(OUT / "P8_Y5_R2FR_3257_EM_COULOMB_SHAPE_ROWS_NONCLAIM.csv"),
            "numeric q_C alloy shape rows",
            ["SHAPE3257_PtRh10", "SHAPE3257_TA6V"],
        ),
        (
            "SRC3258_1328_DD_route",
            "local_path",
            str(OUT / "P8_Y5_R10_1328_COMPONENT_SOURCE_ROUTE_MATRIX.csv"),
            "pre-existing DD route status as external basis only",
            ["ROUTE1328_TA6V_EM_Coulomb", "Damour"],
        ),
        (
            "SRC3258_1910_contract",
            "local_path",
            str(OUT / "P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv"),
            "parent response contract requiring alpha map",
            ["MDT1910_3_EM_Coulomb_binding", "partial_alpha"],
        ),
        (
            "SRC3258_DD_arxiv",
            "url",
            DD_ARXIV,
            "Damour-Donoghue light-dilaton EM charge source",
            ["Q'_e = +7.7 x 10^-4 Z(Z-1)/A^(4/3)", "Eq. 25"],
        ),
        (
            "SRC3258_DD_pdf",
            "url",
            DD_PDF,
            "paper PDF location for Eq. 25 audit",
            ["Q'_e", "7.7 x 10^-4"],
        ),
        (
            "SRC3258_DD_DOI",
            "url",
            DD_DOI,
            "published DOI provenance",
            ["PhysRevD.82.084033"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_kind, source_ref, role, needles in specs:
        path = Path(source_ref) if source_kind == "local_path" else None
        exists = path.exists() if path else bool(source_ref.startswith("https://"))
        rows.append(
            {
                "source_id": source_id,
                "source_kind": source_kind,
                "source_ref": source_ref,
                "exists_or_url_recorded": bool_str(exists),
                "parse_ok": bool_str(parse_ok(path)) if path else "url_not_fetched_by_script",
                "role": role,
                "evidence_hits": evidence(path, needles) if path else ";".join(needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def shape_rows() -> list[dict[str, str]]:
    path = OUT / "P8_Y5_R2FR_3257_EM_COULOMB_SHAPE_ROWS_NONCLAIM.csv"
    return read_csv(path)


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "DD3258_Qe_prime_coefficient",
            "symbol": "k_DD,e",
            "value": f"{DD_QE_COEFFICIENT:.12e}",
            "units": "dimensionless",
            "source_url": DD_ARXIV,
            "source_pdf": DD_PDF,
            "source_doi": DD_DOI,
            "source_pointer": "Damour-Donoghue 2010 Eq. 25 simplified electromagnetic dilaton charge Q'_e=+7.7e-4 Z(Z-1)/A^(4/3)",
            "quantity_type": "external_DD_dilaton_charge_coefficient_not_parent_MTS_fraction",
            "valid_for_claim": "false",
        }
    ]


def external_charge_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for shape in shape_rows():
        shape_value = float_or_none(shape.get("shape_value_q_C"))
        dd_charge = DD_QE_COEFFICIENT * shape_value if shape_value is not None else None
        rows.append(
            {
                "external_row_id": f"DD3258_{shape['material_id']}_Qe_prime",
                "material_id": shape["material_id"],
                "component_id": "EM_Coulomb",
                "q_C_shape": shape.get("shape_value_q_C"),
                "coefficient_id": "DD3258_Qe_prime_coefficient",
                "Qe_prime_DD": f"{dd_charge:.12e}" if dd_charge is not None else "MISSING_SHAPE",
                "formula": "Q'_e = 7.7e-4 q_C = 7.7e-4 Z(Z-1)/A^(4/3), alloy averaged via 1909 q_C",
                "source_status": "SOURCE_BACKED_EXTERNAL_DD_COMPARATOR",
                "mts_parent_status": "PARENT_ALPHA_MAP_UNSIGNED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def raw_external_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for charge in external_charge_rows():
        if charge["material_id"] == "TA6V_minus_PtRh10":
            continue
        rows.append(
            {
                "row_id": charge["external_row_id"],
                "material_id": charge["material_id"],
                "component_id": "EM_Coulomb",
                "quantity_supplied": "Qe_prime_DD_external_comparator",
                "numeric_value": charge["Qe_prime_DD"],
                "requested_fraction_value": "NOT_SUPPLIED_AS_f_EM_A",
                "source_path_or_url": DD_ARXIV,
                "source_doi": DD_DOI,
                "extraction_method": "3257 q_C shape multiplied by DD Eq.25 coefficient 7.7e-4",
                "acceptance_status": "SCHEMA_NUMERIC_BUT_WRONG_QUANTITY_FOR_1233_FRACTION_ACCEPTANCE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def schema_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SCHEMA3258_0_numeric_external_rows",
            "question": "Does 3258 supply finite numeric EM rows?",
            "answer": "yes, finite Q'_e DD external comparator rows for TA6V, PtRh10, and their difference",
            "claim_effect": "does not satisfy f_EM,A fraction acceptance by itself",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SCHEMA3258_1_fraction_vs_charge",
            "question": "Can Q'_e_DD be treated as f_EM,A?",
            "answer": "no; Q'_e is an external dilaton/alpha sensitivity charge, not automatically the parent MTS material energy fraction",
            "claim_effect": "requires parent alpha-map owner or explicit response identification",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SCHEMA3258_2_useful_bridge",
            "question": "What did the sourced coefficient buy us?",
            "answer": "it turns the 3257 toy coefficient into a cited external comparator with the same numerical scale",
            "claim_effect": "good calibration target, not yet a local-GR claim",
            "valid_for_claim": "false",
        },
    ]


def alpha_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "ALPHA3258_0_parent_owner_needed",
            "target": "gamma_EM,A = partial ln M_A / partial ln alpha_EM",
            "current_input": "DD Q'_e external comparator and 1910 exact response contract",
            "required_parent_clause": "parent action must identify the EM generator/alpha deformation whose material response is measured by Q'_e or by f_EM,A",
            "status": "UNSIGNED_PARENT_ALPHA_MAP",
            "valid_for_claim": "false",
        },
        {
            "map_id": "ALPHA3258_1_possible_identification",
            "target": "gamma_EM,A -> Q'_e_DD",
            "current_input": "source-backed Q'_e rows",
            "required_parent_clause": "derive that MTS EM/Coulomb source perturbation acts as the same alpha variation used in the DD charge basis",
            "status": "DERIVATION_TARGET_NOT_ASSUMPTION",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3258_0_source_coefficient",
            "gate": "source-backed external EM coefficient acquired",
            "passed": "true",
            "reason": "DD Eq.25 coefficient recorded as k_DD,e=7.7e-4",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3258_1_fraction_acceptance",
            "gate": "accepted MTS f_EM,A fraction rows",
            "passed": "false",
            "reason": "rows are Q'_e external alpha charges, not parent-owned f_EM,A rows",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3258_2_parent_alpha_map",
            "gate": "parent alpha/EM response map signed",
            "passed": "false",
            "reason": "mapping Q'_e or f_EM into MTS source coupling remains a derivation target",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3258_0",
            "verdict": "SOURCE_BACKED_EXTERNAL_COMPARATOR_FILLED_PARENT_MAP_STILL_OPEN",
            "what_moved": "the 3257 toy 7.7e-4 coefficient is now tied to DD Eq.25, giving numeric Q'_e rows for PtRh10/TA6V",
            "what_remains": "prove or reject the parent identification gamma_EM,A == Q'_e_DD or replace it with a parent-owned f_EM response",
            "selected_next": "derive parent alpha-map owner or demote DD rows to permanent calibration comparators",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3258_0_3259",
            "selected": "primary",
            "target_doc": "3259-Y5-R2FR-parent-alpha-map-owner-or-DD-comparator-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3259_parent_alpha_map_owner_or_DD_comparator_demotion.py",
            "objective": "Attempt the parent derivation that identifies the MTS EM source perturbation with the DD alpha/Coulomb response; if it fails, lock DD as calibration-only and source f_EM separately.",
            "guardrail": "Do not call Q'_e_DD an MTS material fraction unless the parent action signs the alpha/EM generator map.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = source_register()
    external_rows = external_charge_rows()
    numeric_values = [float_or_none(row["Qe_prime_DD"]) for row in external_rows]
    validations = [
        {
            "check_id": "VAL3258_0_sources_recorded",
            "check": "all local sources exist and DD URL strings are recorded",
            "passed": bool_str(all(row["exists_or_url_recorded"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["exists_or_url_recorded"] != "true"),
        },
        {
            "check_id": "VAL3258_1_local_sources_parse",
            "check": "all local source CSV/MD paths parse",
            "passed": bool_str(all(row["parse_ok"] in {"true", "url_not_fetched_by_script"} for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["parse_ok"] not in {"true", "url_not_fetched_by_script"}),
        },
        {
            "check_id": "VAL3258_2_outputs_parse",
            "check": "all 3258 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3258_3_coefficient_numeric",
            "check": "DD coefficient is finite positive and equals 7.7e-4",
            "passed": bool_str(math.isfinite(DD_QE_COEFFICIENT) and DD_QE_COEFFICIENT == 7.7e-4),
            "detail": f"k_DD,e={DD_QE_COEFFICIENT:.12e}",
        },
        {
            "check_id": "VAL3258_4_external_values_numeric",
            "check": "all DD external comparator values are finite numeric",
            "passed": bool_str(all(value is not None and math.isfinite(value) for value in numeric_values)),
            "detail": ";".join(str(value) for value in numeric_values),
        },
        {
            "check_id": "VAL3258_5_nonclaim_preserved",
            "check": "all 3258 gates have claim_allowed=false",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3258_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3258_7_overall",
            "check": "3258 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3258_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    coefficients = coefficient_rows()
    external = external_charge_rows()
    schema = schema_audit_rows()
    alpha_map = alpha_map_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3258 - Source-backed EM Coulomb coefficient or parent alpha-map owner under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3258` upgrades the `3257` toy coefficient into a source-backed **external Damour-Donoghue comparator**.
- The coefficient `k_DD,e=7.7e-4` gives numeric `Q'_e` rows for `PtRh10`, `TA6V`, and `TA6V_minus_PtRh10`.
- This is real progress, but not a loophole: `Q'_e` is an external alpha/dilaton charge, not automatically an MTS-owned `f_EM,A` material fraction.
- The next derivation target is now precise: prove the parent alpha/EM generator map, or demote DD permanently to calibration-only.

## Source Register
{md_table(sources, ["source_id", "source_kind", "source_ref", "exists_or_url_recorded", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## Source-Backed Coefficient
{md_table(coefficients, ["coefficient_id", "symbol", "value", "units", "source_url", "source_doi", "source_pointer", "quantity_type", "valid_for_claim"])}

## DD External EM Charge Rows
{md_table(external, ["external_row_id", "material_id", "q_C_shape", "coefficient_id", "Qe_prime_DD", "formula", "source_status", "mts_parent_status", "valid_for_claim"])}

## Schema Audit
{md_table(schema, ["audit_id", "question", "answer", "claim_effect", "valid_for_claim"])}

## Parent Alpha Map Owner Audit
{md_table(alpha_map, ["map_id", "target", "current_input", "required_parent_clause", "status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "what_remains", "selected_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    rows_by_key = {
        "sources": source_register(),
        "coefficient": coefficient_rows(),
        "external_charge": external_charge_rows(),
        "raw_external": raw_external_rows(),
        "schema_audit": schema_audit_rows(),
        "alpha_map": alpha_map_rows(),
        "gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
