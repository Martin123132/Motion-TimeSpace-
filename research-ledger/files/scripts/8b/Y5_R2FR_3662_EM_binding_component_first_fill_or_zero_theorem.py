from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3662"
BRANCH_ID = "MTS_R2FR_Y5_EM_BINDING_COMPONENT_FIRST_FILL_OR_ZERO_THEOREM_3662"
DOC = ROOT / "3662-Y5-R2FR-EM-binding-component-first-fill-or-zero-theorem.md"

A_C_MEV = 0.711
U_MEV = 931.49410242
SEMF_SOURCE = "semi_empirical_mass_formula_convention; a_C≈0.711 MeV; see https://en.wikipedia.org/wiki/Semi-empirical_mass_formula"
ATOMIC_WEIGHT_SOURCE = "CIAAW/IUPAC standard atomic weights; https://www.ciaaw.org/atomic-weights.htm"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def em_binding_fraction(z: int, atomic_weight: float) -> tuple[float, float, float]:
    e_c_mev = A_C_MEV * z * (z - 1) * atomic_weight ** (-1.0 / 3.0)
    mass_energy_mev = atomic_weight * U_MEV
    return e_c_mev, mass_energy_mev, e_c_mev / mass_energy_mev


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3661", RESIDUALS / "P8_Y5_R2FR_3661_NEXT_TARGET.csv", "EM-binding", "3661 selected EM-binding first fill"),
        ("basis_3661", RESIDUALS / "P8_Y5_R2FR_3661_QX_COMPONENT_BASIS_ROWS.csv", "QXB3661_1_EM_binding", "QX EM binding basis row"),
        ("envelope_3661", RESIDUALS / "P8_Y5_R2FR_3661_QX_NO_CANCELLATION_ENVELOPE_ROWS.csv", "B_source_EM*f_EM", "no-cancellation envelope"),
        ("arenas_3661", RESIDUALS / "P8_Y5_R2FR_3661_SHARED_BOUND_ARENA_ROWS.csv", "SBA3661_0_WEP", "shared WEP/R10/gamma arena map"),
        ("material_3651", RESIDUALS / "P8_Y5_R2FR_3651_MATERIAL_SENSITIVITY_ROWS.csv", "MSR3651_1_BAEM", "B_A_EM symbolic row"),
        ("matter_theorem_3651", RESIDUALS / "P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv", "EM_BINDING_FORMULA_DERIVED_SYMBOLICALLY", "EM Coulomb binding derivation"),
        ("local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local shared bound anchors"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    rows.extend(
        [
            {
                **base(ts),
                "source_id": "external_atomic_weights",
                "path": ATOMIC_WEIGHT_SOURCE,
                "exists": True,
                "needle": "Ti=47.867; Pt=195.084",
                "needle_found": True,
                "role": "standard atomic weight provenance for Ti/Pt nonclaim fill",
            },
            {
                **base(ts),
                "source_id": "external_SEMF_aC",
                "path": SEMF_SOURCE,
                "exists": True,
                "needle": "a_C≈0.711 MeV",
                "needle_found": True,
                "role": "Coulomb coefficient convention for first nonclaim SEMF fill",
            },
        ]
    )
    return rows


def em_zero_theorem_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "theorem_id": "EMZ3662_0_component_definition",
            "object": "EM-binding QX component",
            "statement": "The EM-binding component of Q_X is the source-weighted Coulomb binding sensitivity times the EM coupling slot.",
            "formula": "Q_X^EM = B_source_EM*f_EM; B_source_EM=sum_i w_i B_i^EM",
            "theorem_status": "COMPONENT_DEFINITION_DERIVED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "EMZ3662_1_Coulomb_binding_formula",
            "object": "Coulomb binding sensitivity",
            "statement": "The leading SEMF EM sensitivity is the Coulomb binding fraction.",
            "formula": "B_A^EM ~= E_C/(M_A c^2); E_C=a_C Z(Z-1)A^(-1/3)",
            "theorem_status": "SEMF_FORMULA_READY",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "EMZ3662_2_zero_route",
            "object": "EM-binding zero theorem",
            "statement": "This component is zero only if f_EM=0, or the parent action proves EM binding cannot couple to X, or every relevant source has zero Coulomb fraction.",
            "formula": "f_EM=0 or B_source_EM=0 or parent_no_EM_binding_X_coupling => Q_X^EM=0",
            "theorem_status": "CONDITIONAL_ZERO_THEOREM_PREMISES_UNSIGNED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "EMZ3662_3_countermodel",
            "object": "live EM countermodel",
            "statement": "Ordinary nuclei have nonzero Coulomb binding, so if f_EM is live this component is generically nonzero.",
            "formula": "Z>1 and f_EM!=0 => B_A^EM*f_EM can contribute to Q_X",
            "theorem_status": "NONZERO_EM_BINDING_BRANCH_LIVE",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
    ]


def elemental_em_rows(ts: str) -> list[dict[str, object]]:
    elements = [
        ("Ti", 22, 47.867, "MICROSCOPE_test_body_Ti_proxy"),
        ("Pt", 78, 195.084, "MICROSCOPE_test_body_Pt_proxy"),
    ]
    rows = []
    for symbol, z, atomic_weight, role in elements:
        e_c, mass_e, fraction = em_binding_fraction(z, atomic_weight)
        rows.append(
            {
                **base(ts),
                "element_id": f"EME3662_{symbol}",
                "element": symbol,
                "Z": z,
                "A_effective_atomic_weight": atomic_weight,
                "a_C_MeV": A_C_MEV,
                "E_C_MeV": round(e_c, 9),
                "mass_energy_MeV": round(mass_e, 9),
                "B_A_EM": round(fraction, 12),
                "role": role,
                "atomic_weight_source": ATOMIC_WEIGHT_SOURCE,
                "semf_source": SEMF_SOURCE,
                "current_status": "SOURCE_BACKED_NUMERIC_NONCLAIM_NATURAL_ELEMENT_APPROX",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    ti = rows[0]["B_A_EM"]
    pt = rows[1]["B_A_EM"]
    rows.append(
        {
            **base(ts),
            "element_id": "EME3662_TiPt_delta",
            "element": "Ti_minus_Pt_proxy",
            "Z": "mixed",
            "A_effective_atomic_weight": "mixed",
            "a_C_MeV": A_C_MEV,
            "E_C_MeV": "computed_per_element",
            "mass_energy_MeV": "computed_per_element",
            "B_A_EM": round(float(ti) - float(pt), 12),
            "role": "MICROSCOPE_Ti_minus_Pt_proxy_delta",
            "atomic_weight_source": ATOMIC_WEIGHT_SOURCE,
            "semf_source": SEMF_SOURCE,
            "current_status": "DELTA_B_EM_NUMERIC_NONCLAIM_SOURCE_COMPOSITION_STILL_REQUIRED",
            "score_ready": False,
            "claim_allowed": False,
        }
    )
    return rows


def source_body_schema_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("EMS3662_0_source_body_generic", "source_body_S", "B_source_EM=sum_i w_i B_i^EM", "source material composition weights w_i; element/isotope Z,A; source path", "SOURCE_BODY_COMPOSITION_REQUIRED"),
        ("EMS3662_1_Cassini_Sun", "solar_source_for_gamma", "B_Sun_EM=sum_i w_i B_i^EM", "solar composition model; H/He/metals mass fractions; convention for ionized plasma mass", "SOLAR_COMPOSITION_REQUIRED_FOR_GAMMA"),
        ("EMS3662_2_Earth_WEP", "Earth_source_for_WEP", "B_Earth_EM=sum_i w_i B_i^EM", "Earth composition model; layer weighting; lab/source geometry", "EARTH_COMPOSITION_REQUIRED_FOR_WEP"),
        ("EMS3662_3_lab_R10", "lab_source_for_R10", "B_lab_EM=sum_i w_i B_i^EM", "attractor/test material composition; range geometry; alpha(lambda) curve", "LAB_SOURCE_COMPOSITION_REQUIRED_FOR_R10"),
    ]
    return [
        {
            **base(ts),
            "schema_id": schema_id,
            "object": obj,
            "formula": formula,
            "required_columns": required,
            "current_status": status,
            "score_ready": False,
            "placeholder_refused_as_claim": True,
            "claim_allowed": False,
        }
        for schema_id, obj, formula, required, status in specs
    ]


def shared_component_rows(ts: str, element_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    delta = next(row for row in element_rows if row["element_id"] == "EME3662_TiPt_delta")["B_A_EM"]
    bounds = {row["row_id"]: row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv")}
    return [
        {
            **base(ts),
            "shared_id": "ESC3662_0_WEP_TiPt_EM_piece",
            "arena": "WEP/MICROSCOPE",
            "formula": "eta_TiPt_EM ~= (B_Ti_EM-B_Pt_EM)*f_EM*Q_source_X*tau_WEP",
            "numeric_piece": delta,
            "missing_inputs": "f_EM;Q_source_X;tau_WEP;Earth/source composition",
            "bound_row": "R1_WEP_source_charge",
            "bound_value": bounds["R1_WEP_source_charge"]["upper_bound"],
            "current_status": "TEST_PAIR_NUMERIC_SOURCE_SIDE_MISSING_NONCLAIM",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "shared_id": "ESC3662_1_R10_EM_piece",
            "arena": "R10/fifth-force",
            "formula": "alpha_EM_component(lambda)=K_X*(B_source_EM*f_EM)*(B_test_EM*f_EM)/(4*pi*Z_X*G_obs)",
            "numeric_piece": "Ti/Pt B_EM available; source/test material still branch-dependent",
            "missing_inputs": "K_X;Z_X;lambda_X;source/test material composition;alpha_bound(lambda)",
            "bound_row": "R10_fifth_force",
            "bound_value": bounds["R10_fifth_force"]["upper_bound"],
            "current_status": "SYMBOLIC_CURVE_AND_SOURCE_TEST_PRODUCT_MISSING_NONCLAIM",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "shared_id": "ESC3662_2_gamma_EM_piece",
            "arena": "Cassini/PPN gamma",
            "formula": "Q_X^EM=B_source_EM*f_EM enters A_X~=Q_X/(4*pi*Z_X) and gamma profile envelope",
            "numeric_piece": "no source-body B_source_EM yet",
            "missing_inputs": "solar/source B_source_EM;f_EM;Z_X;lambda_X;k_H;k_G;gamma kernel",
            "bound_row": "R3_gamma",
            "bound_value": bounds["R3_gamma"]["upper_bound"],
            "current_status": "GAMMA_SOURCE_SIDE_MISSING_NONCLAIM",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3662_0_zero_attempt", "EM-binding zero theorem attempted", "PASSED_AUDIT", "zero requires f_EM=0 or parent no-EM-coupling theorem; not signed"),
        ("CG3662_1_numeric_TiPt", "Ti/Pt EM binding fractions computed", "PASSED_NUMERIC_FILL_NONCLAIM", "natural-element SEMF proxies filled with provenance"),
        ("CG3662_2_source_schema", "source-body schemas written", "PASSED_SCHEMA_GATE", "Sun/Earth/lab source compositions remain required"),
        ("CG3662_3_shared_use", "shared WEP/R10/gamma mapping written", "PASSED_MAPPING_GATE", "same EM component feeds all arenas"),
        ("CG3662_4_no_claim", "no WEP/R10/gamma/local-GR pass claimed", "ACTIVE_GUARD", "source composition and f_EM/Z_X/profile inputs remain missing"),
        ("CG3662_5_next", "next step sources source-body composition or derives f_EM=0", "SOURCE_COMPOSITION_OR_fEM_ZERO_NEXT", "this makes the first numeric component scoreable"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "EM_BINDING_ZERO_UNSIGNED_TIPT_NUMERIC_NONCLAIM_FILL_READY",
            "summary": "3662 refuses the unsigned EM-binding zero theorem, computes source-backed nonclaim Ti/Pt SEMF Coulomb binding fractions, and writes the source-body schemas needed before WEP/R10/gamma can score the shared EM component.",
            "claim_ceiling": "no EM-binding zero, WEP, R10, gamma, local-GR, PPN, Newtonian, source-calibration, clock/orbital, or EH-dominance pass is claimed",
            "useful_result": "The easiest Q_X component now has real numeric test-body proxies; the remaining hard input is source-body composition plus f_EM/Z_X/profile ownership.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3662_0",
            "target_doc": "3663-Y5-R2FR-EM-source-composition-fill-or-fEM-zero-theorem.md",
            "target_script": "scripts/Y5_R2FR_3663_EM_source_composition_fill_or_fEM_zero_theorem.py",
            "objective": "try to derive f_EM=0 from parent EM normalization/no-extra-F2 ownership; if not, source Sun/Earth/lab EM composition rows for B_source_EM and keep all claims nonclaim",
            "success_gate": "EM component has either parent f_EM zero or source-body B_source_EM rows with provenance placeholders refused as claims",
        }
    ]


def write_doc(sources, theorem, elements, schemas, shared, gates, status_rows_, next_target) -> None:
    lines = [
        "# 3662 - EM-binding component first fill or zero theorem",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The EM-binding component cannot be zero-claimed yet. It would vanish only if `f_EM=0`, if the parent action forbids EM binding from coupling to `X`, or if the relevant source has no Coulomb binding. Ordinary Ti/Pt nuclei do have Coulomb binding, so the nonzero branch is live.",
        "",
        "The first numeric nonclaim fill is now in place:",
        "",
        "`B_A^EM ~= E_C/(M_A c^2)`, with `E_C=a_C Z(Z-1)A^(-1/3)` and `a_C=0.711 MeV`.",
        "",
        "Ti/Pt are filled as natural-element SEMF proxies, but WEP/R10/gamma still cannot score until the attractor/source composition and `f_EM`, `Z_X`, `lambda_X`, `k_H`, `k_G` inputs are owned.",
        "",
        "## EM zero theorem attempt",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['theorem_status']} - `{row['formula']}`")
    lines.extend(["", "## Elemental EM rows"])
    for row in elements:
        lines.append(f"- `{row['element_id']}`: `{row['element']}` B_A_EM=`{row['B_A_EM']}` - {row['current_status']}")
    lines.extend(["", "## Source-body schemas"])
    for row in schemas:
        lines.append(f"- `{row['schema_id']}`: `{row['object']}` - {row['current_status']}")
    lines.extend(["", "## Shared component rows"])
    for row in shared:
        lines.append(f"- `{row['shared_id']}`: `{row['arena']}` - {row['current_status']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(ts, output_paths, sources, theorem, elements, schemas, shared, gates, status_rows_, next_target) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3662_0_sources_exist", all(row["exists"] for row in sources), "every cited local/external source marker exists")
    add("VAL3662_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found or externally declared")
    add("VAL3662_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3662 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3662_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3662_4_zero_not_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in theorem), "EM zero theorem not accepted")
    add("VAL3662_5_numeric_elements", {"Ti", "Pt"}.issubset({row["element"] for row in elements}) and all(parse_float(row["B_A_EM"]) is not None for row in elements if row["element"] in {"Ti", "Pt"}), "Ti/Pt numeric EM fractions present")
    add("VAL3662_6_delta_present", any(row["element_id"] == "EME3662_TiPt_delta" for row in elements), "Ti-Pt delta EM fraction present")
    add("VAL3662_7_schemas_present", {"solar_source_for_gamma", "Earth_source_for_WEP", "lab_source_for_R10"}.issubset({row["object"] for row in schemas}), "source-body schemas present")
    add("VAL3662_8_schemas_nonclaim", all(str(row["placeholder_refused_as_claim"]).lower() == "true" and str(row["score_ready"]).lower() == "false" for row in schemas), "source schemas remain nonclaim")
    add("VAL3662_9_shared_rows", {"WEP/MICROSCOPE", "R10/fifth-force", "Cassini/PPN gamma"}.issubset({row["arena"] for row in shared}), "shared arena rows present")
    add("VAL3662_10_claim_gates_present", {"CG3662_0_zero_attempt", "CG3662_1_numeric_TiPt", "CG3662_2_source_schema", "CG3662_3_shared_use", "CG3662_4_no_claim", "CG3662_5_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + theorem + elements + schemas + shared + gates + status_rows_ + next_target
    add("VAL3662_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3662_12_no_element_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in elements), "element rows are numeric but not score-ready")
    doc_text = read_text(DOC)
    add("VAL3662_13_doc_written", "B_A^EM" in doc_text and "Ti/Pt" in doc_text and "cannot score" in doc_text, "doc records EM fill and nonclaim status")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3662*", "3662-Y5-R2FR-*", "Y5_R2FR_3662_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3662_14_no_formalization_leak", not leaks, "no 3662 checkpoint files in formalization-workbench")
    add("VAL3662_15_next_target", next_target[0]["target_doc"].startswith("3663-") and "source-composition" in next_target[0]["target_doc"], "3663 source-composition/fEM target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = em_zero_theorem_rows(ts)
    elements = elemental_em_rows(ts)
    schemas = source_body_schema_rows(ts)
    shared = shared_component_rows(ts, elements)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3662_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3662_EM_ZERO_THEOREM_ATTEMPT.csv",
        "elements": RESIDUALS / "P8_Y5_R2FR_3662_ELEMENTAL_EM_BINDING_ROWS.csv",
        "schemas": RESIDUALS / "P8_Y5_R2FR_3662_SOURCE_BODY_SCHEMA_ROWS.csv",
        "shared": RESIDUALS / "P8_Y5_R2FR_3662_SHARED_COMPONENT_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3662_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3662_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3662_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3662_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["elements"], elements)
    write_csv(outputs["schemas"], schemas)
    write_csv(outputs["shared"], shared)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, elements, schemas, shared, gates, status_rows_, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, elements, schemas, shared, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3662 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3662 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
