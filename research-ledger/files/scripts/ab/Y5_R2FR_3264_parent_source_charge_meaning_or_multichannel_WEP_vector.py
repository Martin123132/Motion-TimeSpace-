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
PYCACHE = ROOT / "scripts" / "__pycache__"
DD_TEX = ROOT / "source-intake" / "external-sources" / "damour_donoghue_1007.2792_source" / "DamourDonoghueEPfinal.tex"
COMPOSITION = OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_COMPOSITION_SOURCE_BACKED_NONCLAIM.csv"

DOC = ROOT / "3264-Y5-R2FR-parent-source-charge-meaning-or-multichannel-WEP-vector-under-AX1090.md"

ETA_REPORTED = 2.7e-15
TAU_READOUT_MIN = 0.98
ETA_CONSERVATIVE = ETA_REPORTED / TAU_READOUT_MIN

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3264_SOURCE_REGISTER.csv",
    "dd_evidence": OUT / "P8_Y5_R2FR_3264_DD_MULTICHANNEL_EVIDENCE.csv",
    "element_charges": OUT / "P8_Y5_R2FR_3264_DD_ELEMENT_CHARGES_NONCLAIM.csv",
    "material_charges": OUT / "P8_Y5_R2FR_3264_DD_MATERIAL_CHARGES_NONCLAIM.csv",
    "delta_vector": OUT / "P8_Y5_R2FR_3264_TIPT_DD_DELTA_VECTOR_NONCLAIM.csv",
    "bounds": OUT / "P8_Y5_R2FR_3264_MULTICHANNEL_WEP_BOUNDS_NONCLAIM.csv",
    "degeneracy": OUT / "P8_Y5_R2FR_3264_TWO_CHANNEL_DEGENERACY_GUARD.csv",
    "gates": OUT / "P8_Y5_R2FR_3264_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3264_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3264_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3264_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


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
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def line_hit(path: Path, needle: str) -> tuple[int | None, str]:
    if not path.exists():
        return None, "MISSING_SOURCE"
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            if needle in line:
                return line_number, " ".join(line.strip().split())
    return None, "NO_MATCH"


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


def q_c_shape(z: float, a: float) -> float:
    return z * (z - 1.0) / (a ** (4.0 / 3.0))


def q_e(z: float, a: float) -> float:
    return 7.7e-4 * q_c_shape(z, a)


def q_hatm(z: float, a: float) -> float:
    return -0.036 / (a ** (1.0 / 3.0)) - 1.4e-4 * q_c_shape(z, a)


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3264_3263_handoff",
            ROOT / "3263-Y5-R2FR-source-profile-channel-projection-or-parent-domain-lock-under-AX1090.md",
            "3263 selected parent source-charge meaning or multichannel WEP vector",
            ["NEXT3263_0_3264", "eta-level", "multichannel"],
        ),
        (
            "SRC3264_DD_tex",
            DD_TEX,
            "Damour-Donoghue source formulas for Q'_hatm and Q'_e",
            ["Q'_{\\hat m}", "Q'_{e}", "D_{\\hat m}"],
        ),
        (
            "SRC3264_1909_composition",
            COMPOSITION,
            "TA6V/PtRh10 alloy composition inputs",
            ["AC1909_TA6V_Ti", "AC1909_PtRh10_Pt"],
        ),
        (
            "SRC3264_3263_bounds",
            OUT / "P8_Y5_R2FR_3263_CONVENTION_BOUND_OUTPUT_NONCLAIM.csv",
            "eta-level and conservative readout-corrected bound",
            ["CB3263_1_eta_level_readout_conservative"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def dd_evidence_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DDE3264_0_alpha_two_channel",
            "\\left( \\frac{\\Delta a}{a} \\right)_{BC} = (\\alpha_B- \\alpha_C)\\alpha_E =  \\left[D_{\\hat m} Q'_{\\hat m} + D_e Q'_e \\right]_{BC}",
            "DD two-dominant-channel WEP form.",
        ),
        (
            "DDE3264_1_qhatm",
            "Q'_{\\hat m} = -\\frac{0.036}{A^{1/3}} - 1.4 \\times 10^{-4} \\, \\frac{Z(Z-1)}{A^{4/3}}",
            "DD reduced light-quark/nuclear-mass charge.",
        ),
        (
            "DDE3264_2_qe",
            "Q'_{e} =  + 7.7 \\times 10^{-4} \\frac{Z(Z-1)}{A^{4/3}}",
            "DD electromagnetic charge.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for evidence_id, needle, role in specs:
        line_number, text = line_hit(DD_TEX, needle)
        rows.append(
            {
                "evidence_id": evidence_id,
                "source_path": str(DD_TEX),
                "line_number": line_number if line_number is not None else "NO_MATCH",
                "text_excerpt": text,
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def composition_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(COMPOSITION):
        material = row["material_id"]
        element = row["element"]
        mass_fraction = float(row["mass_fraction"])
        a = float(row["A_context"])
        z = float(row["Z"])
        rows.append(
            {
                "element_charge_id": f"EL3264_{material}_{element}",
                "material_id": material,
                "element": element,
                "mass_fraction": f"{mass_fraction:.12e}",
                "A_context": f"{a:.12e}",
                "Z": f"{z:.12e}",
                "Qhatm_prime_element": f"{q_hatm(z, a):.12e}",
                "Qe_prime_element": f"{q_e(z, a):.12e}",
                "extraction_method": "DD formulas applied to 1909 alloy element context, mass-fraction averaged",
                "valid_for_claim": "false",
            }
        )
    return rows


def material_charge_rows() -> list[dict[str, Any]]:
    accum: dict[str, dict[str, float]] = {}
    for row in composition_rows():
        material = row["material_id"]
        accum.setdefault(material, {"Qhatm": 0.0, "Qe": 0.0, "mass_fraction_sum": 0.0})
        weight = float(row["mass_fraction"])
        accum[material]["Qhatm"] += weight * float(row["Qhatm_prime_element"])
        accum[material]["Qe"] += weight * float(row["Qe_prime_element"])
        accum[material]["mass_fraction_sum"] += weight
    rows: list[dict[str, Any]] = []
    for material, values in sorted(accum.items()):
        rows.append(
            {
                "material_charge_id": f"MAT3264_{material}",
                "material_id": material,
                "Qhatm_prime": f"{values['Qhatm']:.12e}",
                "Qe_prime": f"{values['Qe']:.12e}",
                "mass_fraction_sum": f"{values['mass_fraction_sum']:.12e}",
                "basis": "DD approximate two-charge basis; mass-fraction alloy average",
                "valid_for_claim": "false",
            }
        )
    return rows


def delta_vector_rows() -> list[dict[str, Any]]:
    mats = {row["material_id"]: row for row in material_charge_rows()}
    delta_qhatm = float(mats["TA6V"]["Qhatm_prime"]) - float(mats["PtRh10"]["Qhatm_prime"])
    delta_qe = float(mats["TA6V"]["Qe_prime"]) - float(mats["PtRh10"]["Qe_prime"])
    norm = math.sqrt(delta_qhatm**2 + delta_qe**2)
    return [
        {
            "delta_id": "DELTA3264_TA6V_minus_PtRh10",
            "left_minus_right": "TA6V_minus_PtRh10",
            "Delta_Qhatm_prime": f"{delta_qhatm:.12e}",
            "Delta_Qe_prime": f"{delta_qe:.12e}",
            "delta_vector_norm": f"{norm:.12e}",
            "eta_formula": "eta_TiPt = Delta_Qhatm_prime*D_hatm + Delta_Qe_prime*D_e + residual",
            "valid_for_claim": "false",
        }
    ]


def bound_rows() -> list[dict[str, Any]]:
    delta = delta_vector_rows()[0]
    dqhat = abs(float(delta["Delta_Qhatm_prime"]))
    dqe = abs(float(delta["Delta_Qe_prime"]))
    dnorm = float(delta["delta_vector_norm"])
    return [
        {
            "bound_id": "MB3264_0_two_channel_strip",
            "assumption": "two DD channels retained; conservative eta bound; no residual",
            "formula": "|Delta_Qhatm*D_hatm + Delta_Qe*D_e| <= eta_bound",
            "value": f"{ETA_CONSERVATIVE:.12e}",
            "interpretation": "one Ti/Pt WEP pair gives a strip, not separate D_hatm/D_e bounds",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "MB3264_1_qhatm_single_channel",
            "assumption": "D_e=0 and residual=0",
            "formula": "|D_hatm| <= eta_bound/|Delta_Qhatm|",
            "value": f"{ETA_CONSERVATIVE / dqhat:.12e}",
            "interpretation": "single-channel smoke bound only",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "MB3264_2_qe_single_channel",
            "assumption": "D_hatm=0 and residual=0",
            "formula": "|D_e| <= eta_bound/|Delta_Qe|",
            "value": f"{ETA_CONSERVATIVE / dqe:.12e}",
            "interpretation": "matches the EM-only conservative scale",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "MB3264_3_parallel_min_norm",
            "assumption": "coupling vector parallel to Ti/Pt DD vector",
            "formula": "|D_parallel| <= eta_bound/||Delta_Q||",
            "value": f"{ETA_CONSERVATIVE / dnorm:.12e}",
            "interpretation": "minimum-norm aligned bound, not a general two-parameter bound",
            "valid_for_claim": "false",
        },
    ]


def degeneracy_rows() -> list[dict[str, Any]]:
    delta = delta_vector_rows()[0]
    dqhat = float(delta["Delta_Qhatm_prime"])
    dqe = float(delta["Delta_Qe_prime"])
    return [
        {
            "guard_id": "DEG3264_0_orthogonal_flat_direction",
            "statement": "A single Ti/Pt WEP pair cannot bound the coupling component orthogonal to its DD charge-difference vector.",
            "orthogonal_direction": f"(D_hatm,D_e) proportional to ({dqe:.12e},{-dqhat:.12e})",
            "math": "Delta_Qhatm*D_hatm + Delta_Qe*D_e = 0 along this direction",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "DEG3264_1_no_cancellation_guard",
            "statement": "The EM-only bound is not a full WEP pass because D_hatm and D_e can cancel in this material pair.",
            "orthogonal_direction": "requires another material pair, clock/R10 cross-channel, or parent no-cancellation theorem",
            "math": "do not infer both |D_hatm| and |D_e| are small from one scalar eta",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3264_0_multichannel_vector",
            "gate": "two-channel DD Ti/Pt vector computed",
            "passed": "true",
            "reason": "Q'_hatm and Q'_e are sourced and alloy-averaged from local composition rows",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3264_1_individual_channel_bounds",
            "gate": "individual D_hatm and D_e bounded without assumptions",
            "passed": "false",
            "reason": "one WEP pair gives a strip; single-channel bounds require assumptions",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3264_2_parent_source_meaning",
            "gate": "D_hatm/D_e identified with MTS parent source factors",
            "passed": "false",
            "reason": "external DD coefficients are calibration coordinates until parent source-charge map is signed",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3264_3_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "multichannel vector is evidence plumbing, not a fixed-EM or full-source theorem",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    delta = delta_vector_rows()[0]
    return [
        {
            "decision_id": "DEC3264_0",
            "verdict": "MULTICHANNEL_WEP_VECTOR_BUILT_SINGLE_PAIR_DEGENERATE",
            "what_moved": f"Ti/Pt now has Delta_Qhatm={delta['Delta_Qhatm_prime']} and Delta_Qe={delta['Delta_Qe_prime']}",
            "best_next": "add another material/test arena or derive parent no-cancellation/source map",
            "fallback_next": "use single-channel bounds only as clearly marked smoke diagnostics",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3264_0_3265",
            "selected": "primary",
            "target_doc": "3265-Y5-R2FR-second-material-arena-or-parent-no-cancellation-theorem-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3265_second_material_arena_or_parent_no_cancellation_theorem.py",
            "objective": "Either add a second independent material/test vector to break the DD two-channel degeneracy, or derive the parent no-cancellation/source map that lets one channel be isolated.",
            "guardrail": "Do not treat EM-only or qhatm-only bounds as full WEP/local-GR evidence.",
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
    sources = source_register()
    evidence_rows = dd_evidence_rows()
    mats = material_charge_rows()
    deltas = delta_vector_rows()
    delta = deltas[0]
    validations = [
        {
            "check_id": "VAL3264_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3264_1_sources_parse",
            "check": "all cited source CSV/MD/TEX paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3264_2_DD_lines_found",
            "check": "DD multichannel evidence lines are found",
            "passed": bool_str(all(row["line_number"] != "NO_MATCH" for row in evidence_rows)),
            "detail": ";".join(f"{row['evidence_id']}:{row['line_number']}" for row in evidence_rows),
        },
        {
            "check_id": "VAL3264_3_outputs_parse",
            "check": "all 3264 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3264_4_material_rows",
            "check": "TA6V and PtRh10 material charges exist",
            "passed": bool_str({row["material_id"] for row in mats} == {"PtRh10", "TA6V"}),
            "detail": ";".join(row["material_id"] for row in mats),
        },
        {
            "check_id": "VAL3264_5_delta_numeric",
            "check": "Delta vector entries are finite numeric",
            "passed": bool_str(all(math.isfinite(float(delta[key])) for key in ["Delta_Qhatm_prime", "Delta_Qe_prime", "delta_vector_norm"])),
            "detail": f"{delta['Delta_Qhatm_prime']};{delta['Delta_Qe_prime']}",
        },
        {
            "check_id": "VAL3264_6_claim_gates_false",
            "check": "no 3264 claim gate allows local-GR/WEP/Maxwell promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3264_7_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3264_8_overall",
            "check": "3264 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3264_8_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    dd_evidence = dd_evidence_rows()
    element_charges = composition_rows()
    material_charges = material_charge_rows()
    delta = delta_vector_rows()
    bounds = bound_rows()
    degeneracy = degeneracy_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3264 - Parent source-charge meaning or multichannel WEP vector under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3264` adds the second dominant DD channel, `Q'_hatm`, so the Ti/Pt WEP branch is no longer EM-only.
- The source-backed two-channel form is `eta_TiPt = Delta_Qhatm D_hatm + Delta_Qe D_e + residual`.
- A single Ti/Pt WEP pair gives a **strip**, not independent bounds on `D_hatm` and `D_e`; cancellation directions remain.
- This is progress because it tells us exactly what extra evidence is needed: a second material/test vector or a parent no-cancellation/source map.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## DD Multichannel Evidence
{md_table(dd_evidence, ["evidence_id", "line_number", "text_excerpt", "role", "valid_for_claim"])}

## Element Charges
{md_table(element_charges, ["element_charge_id", "material_id", "element", "mass_fraction", "A_context", "Z", "Qhatm_prime_element", "Qe_prime_element", "valid_for_claim"])}

## Material Charges
{md_table(material_charges, ["material_charge_id", "material_id", "Qhatm_prime", "Qe_prime", "mass_fraction_sum", "basis", "valid_for_claim"])}

## Ti/Pt DD Delta Vector
{md_table(delta, ["delta_id", "left_minus_right", "Delta_Qhatm_prime", "Delta_Qe_prime", "delta_vector_norm", "eta_formula", "valid_for_claim"])}

## Multichannel WEP Bounds
{md_table(bounds, ["bound_id", "assumption", "formula", "value", "interpretation", "valid_for_claim"])}

## Two-Channel Degeneracy Guard
{md_table(degeneracy, ["guard_id", "statement", "orthogonal_direction", "math", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_key = {
        "sources": source_register(),
        "dd_evidence": dd_evidence_rows(),
        "element_charges": composition_rows(),
        "material_charges": material_charge_rows(),
        "delta_vector": delta_vector_rows(),
        "bounds": bound_rows(),
        "degeneracy": degeneracy_rows(),
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
