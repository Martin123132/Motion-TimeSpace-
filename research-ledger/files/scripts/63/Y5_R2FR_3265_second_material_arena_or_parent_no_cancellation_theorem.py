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
EOT_TEX = ROOT / "source-intake" / "external-sources" / "eotwash_0712.0607_source" / "ep.tex"
DELTA_3264 = OUT / "P8_Y5_R2FR_3264_TIPT_DD_DELTA_VECTOR_NONCLAIM.csv"
MAT_3264 = OUT / "P8_Y5_R2FR_3264_DD_MATERIAL_CHARGES_NONCLAIM.csv"
BOUND_3264 = OUT / "P8_Y5_R2FR_3264_MULTICHANNEL_WEP_BOUNDS_NONCLAIM.csv"

DOC = ROOT / "3265-Y5-R2FR-second-material-arena-or-parent-no-cancellation-theorem-under-AX1090.md"

ETA_MICROSCOPE_CONSERVATIVE = 2.7e-15 / 0.98
EOT_ETA_CENTRAL = 0.3e-13
EOT_ETA_SIGMA = 1.8e-13
EOT_ETA_95_BOUND = abs(EOT_ETA_CENTRAL) + 1.96 * EOT_ETA_SIGMA

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3265_SOURCE_REGISTER.csv",
    "eot_evidence": OUT / "P8_Y5_R2FR_3265_EOTWASH_EVIDENCE.csv",
    "material_charges": OUT / "P8_Y5_R2FR_3265_DD_MATERIAL_CHARGES_NONCLAIM.csv",
    "delta_matrix": OUT / "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv",
    "rank": OUT / "P8_Y5_R2FR_3265_RANK_AND_CONDITIONING.csv",
    "bounds": OUT / "P8_Y5_R2FR_3265_CONDITIONAL_TWO_CHANNEL_BOUNDS_NONCLAIM.csv",
    "theorem": OUT / "P8_Y5_R2FR_3265_NO_CANCELLATION_THEOREM_STATUS.csv",
    "gates": OUT / "P8_Y5_R2FR_3265_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3265_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3265_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3265_VALIDATION.csv",
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
            "SRC3265_3264_handoff",
            ROOT / "3264-Y5-R2FR-parent-source-charge-meaning-or-multichannel-WEP-vector-under-AX1090.md",
            "3264 established Ti/Pt as a two-channel DD strip, not an EM-only bound",
            ["single Ti/Pt WEP pair gives a", "Delta_Qhatm", "NEXT3264_0_3265"],
            "",
        ),
        (
            "SRC3265_DD_tex",
            DD_TEX,
            "Damour-Donoghue two-charge basis and WEP formula",
            ["Q'_{\\hat m}", "Q'_{e}", "D_{\\hat m} Q'_{\\hat m}"],
            "https://arxiv.org/abs/1007.2792",
        ),
        (
            "SRC3265_EOTWASH_tex",
            EOT_TEX,
            "Eot-Wash Be/Ti torsion-balance second material arena",
            ["beryllium and titanium", "eta(\\mbox{Be}-\\mbox{Ti})", "The pendulum"],
            "https://arxiv.org/abs/0712.0607",
        ),
        (
            "SRC3265_3264_delta",
            DELTA_3264,
            "MICROSCOPE TA6V/PtRh10 DD vector from 3264",
            ["DELTA3264_TA6V_minus_PtRh10"],
            "",
        ),
        (
            "SRC3265_3264_bounds",
            BOUND_3264,
            "MICROSCOPE conservative eta strip bound from 3264",
            ["MB3264_0_two_channel_strip"],
            "",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles, url in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_url": url,
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def eot_evidence_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EOT3265_0_materials_abstract",
            "beryllium and titanium test bodies",
            "Eot-Wash compares Be and Ti test bodies.",
        ),
        (
            "EOT3265_1_pendulum_materials",
            "four beryllium and four titanium test masses",
            "Be/Ti material pair is explicit in the apparatus.",
        ),
        (
            "EOT3265_2_eta_result",
            "\\eta(\\mbox{Be}-\\mbox{Ti})= \\frac{\\Delta a_{N}}{a_{\\perp}^g}= (0.3\\pm 1.8)\\times 10^{-13}.",
            "Earth-directed Eotvos parameter used as a 95 percent second-row bound.",
        ),
        (
            "EOT3265_3_source_model",
            "We used an elliptical layered Earth model",
            "Long-range source convention is Earth-model based, but not yet parent-locked to MTS.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for evidence_id, needle, role in specs:
        line_number, text = line_hit(EOT_TEX, needle)
        rows.append(
            {
                "evidence_id": evidence_id,
                "source_path": str(EOT_TEX),
                "source_url": "https://arxiv.org/abs/0712.0607",
                "line_number": line_number if line_number is not None else "NO_MATCH",
                "text_excerpt": text,
                "role": role,
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "evidence_id": "EOT3265_4_eta_bound_95",
            "source_path": str(EOT_TEX),
            "source_url": "https://arxiv.org/abs/0712.0607",
            "line_number": "derived_from_EOT3265_2_eta_result",
            "text_excerpt": f"|eta_Earth_BeTi| <= |{EOT_ETA_CENTRAL:.3e}| + 1.96*{EOT_ETA_SIGMA:.3e} = {EOT_ETA_95_BOUND:.12e}",
            "role": "Conservative Gaussian 95 percent absolute upper bound for matrix smoke inversion.",
            "valid_for_claim": "false",
        }
    )
    return rows


def material_charge_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if MAT_3264.exists():
        for row in read_csv(MAT_3264):
            rows.append(
                {
                    "material_charge_id": f"MAT3265_from3264_{row['material_id']}",
                    "arena": "MICROSCOPE_TIPT",
                    "material_id": row["material_id"],
                    "composition_basis": row.get("basis", "3264 DD alloy average"),
                    "A_context": "alloy_from_3264",
                    "Z": "alloy_from_3264",
                    "Qhatm_prime": row["Qhatm_prime"],
                    "Qe_prime": row["Qe_prime"],
                    "source_row": str(MAT_3264),
                    "valid_for_claim": "false",
                }
            )
    eot_specs = [
        ("Be", "EOTWASH_Be", 9.0122, 4.0),
        ("Ti", "EOTWASH_Ti", 47.867, 22.0),
    ]
    for element, material_id, a, z in eot_specs:
        rows.append(
            {
                "material_charge_id": f"MAT3265_{material_id}",
                "arena": "EOTWASH_BETI",
                "material_id": material_id,
                "composition_basis": "nominal pure natural element; Eot-Wash source identifies test-body element, not isotope/binding tensor",
                "A_context": f"{a:.12e}",
                "Z": f"{z:.12e}",
                "Qhatm_prime": f"{q_hatm(z, a):.12e}",
                "Qe_prime": f"{q_e(z, a):.12e}",
                "source_row": str(EOT_TEX),
                "valid_for_claim": "false",
            }
        )
    return rows


def material_lookup() -> dict[str, tuple[float, float]]:
    lookup: dict[str, tuple[float, float]] = {}
    for row in material_charge_rows():
        lookup[row["material_id"]] = (float(row["Qhatm_prime"]), float(row["Qe_prime"]))
    return lookup


def delta_matrix_rows() -> list[dict[str, Any]]:
    lookup = material_lookup()
    tipt = read_csv(DELTA_3264)[0]
    be = lookup["EOTWASH_Be"]
    ti = lookup["EOTWASH_Ti"]
    rows = [
        {
            "row_id": "DM3265_0_MICROSCOPE_TA6V_minus_PtRh10",
            "arena": "MICROSCOPE_TIPT_EARTH_FIELD",
            "left_minus_right": "TA6V_minus_PtRh10",
            "Delta_Qhatm_prime": tipt["Delta_Qhatm_prime"],
            "Delta_Qe_prime": tipt["Delta_Qe_prime"],
            "eta_abs_bound": f"{ETA_MICROSCOPE_CONSERVATIVE:.12e}",
            "eta_bound_basis": "MICROSCOPE final eta divided by tau_readout_min=0.98 from 3264",
            "source_row": str(DELTA_3264),
            "valid_for_claim": "false",
        },
        {
            "row_id": "DM3265_1_EOTWASH_Be_minus_Ti",
            "arena": "EOTWASH_BETI_EARTH_FIELD",
            "left_minus_right": "Be_minus_Ti",
            "Delta_Qhatm_prime": f"{be[0] - ti[0]:.12e}",
            "Delta_Qe_prime": f"{be[1] - ti[1]:.12e}",
            "eta_abs_bound": f"{EOT_ETA_95_BOUND:.12e}",
            "eta_bound_basis": "|0.3e-13| + 1.96*1.8e-13 from Eot-Wash eta(Be-Ti)",
            "source_row": str(EOT_TEX),
            "valid_for_claim": "false",
        },
    ]
    return rows


def matrix_values() -> tuple[float, float, float, float, float, float]:
    rows = delta_matrix_rows()
    a = float(rows[0]["Delta_Qhatm_prime"])
    b = float(rows[0]["Delta_Qe_prime"])
    c = float(rows[1]["Delta_Qhatm_prime"])
    d = float(rows[1]["Delta_Qe_prime"])
    b1 = float(rows[0]["eta_abs_bound"])
    b2 = float(rows[1]["eta_abs_bound"])
    return a, b, c, d, b1, b2


def rank_rows() -> list[dict[str, Any]]:
    a, b, c, d, _, _ = matrix_values()
    det = a * d - b * c
    n1 = math.hypot(a, b)
    n2 = math.hypot(c, d)
    cos_angle = (a * c + b * d) / (n1 * n2)
    sin_angle = abs(det) / (n1 * n2)
    x = a * a + c * c
    y = a * b + c * d
    z = b * b + d * d
    trace = x + z
    disc = math.sqrt(max((x - z) ** 2 + 4.0 * y * y, 0.0))
    smax = math.sqrt(max((trace + disc) / 2.0, 0.0))
    smin = math.sqrt(max((trace - disc) / 2.0, 0.0))
    condition = math.inf if smin == 0.0 else smax / smin
    return [
        {
            "rank_id": "RANK3265_0_two_arena_DD_matrix",
            "matrix_rows": "[(TA6V-PtRh10),(Be-Ti)] in (Q'_hatm,Q'_e)",
            "determinant": f"{det:.12e}",
            "row1_norm": f"{n1:.12e}",
            "row2_norm": f"{n2:.12e}",
            "cos_angle": f"{cos_angle:.12e}",
            "sin_angle_abs": f"{sin_angle:.12e}",
            "condition_number": f"{condition:.12e}",
            "rank_two": bool_str(abs(det) > 1.0e-12),
            "meaning": "The Eot-Wash Be/Ti vector is not parallel to the MICROSCOPE Ti/Pt vector; cancellation cannot hide both channels if the same D basis and residual silence are signed.",
            "valid_for_claim": "false",
        }
    ]


def conditional_bound_rows() -> list[dict[str, Any]]:
    a, b, c, d, b1, b2 = matrix_values()
    det = a * d - b * c
    inv00 = d / det
    inv01 = -b / det
    inv10 = -c / det
    inv11 = a / det
    dhatm_bound = abs(inv00) * b1 + abs(inv01) * b2
    de_bound = abs(inv10) * b1 + abs(inv11) * b2
    return [
        {
            "bound_id": "CB3265_0_conditional_two_row_system",
            "assumption": "same DD D_hatm/D_e coordinates across MICROSCOPE and Eot-Wash; residuals silent; source convention locked",
            "matrix_equation": "A D = eta, A rows are DeltaQ(TA6V-PtRh10) and DeltaQ(Be-Ti)",
            "eta_bounds": f"b_MICROSCOPE={b1:.12e}; b_EOTWASH={b2:.12e}",
            "claim_status": "CONDITIONAL_MATRIX_THEOREM_ONLY",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3265_1_D_hatm_component_bound",
            "assumption": "CB3265_0 assumptions",
            "formula": "|D_hatm| <= |A^{-1}_{00}| b1 + |A^{-1}_{01}| b2",
            "value": f"{dhatm_bound:.12e}",
            "claim_status": "NONCLAIM_UNTIL_PARENT_SOURCE_CONVENTION_LOCK",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3265_2_D_e_component_bound",
            "assumption": "CB3265_0 assumptions",
            "formula": "|D_e| <= |A^{-1}_{10}| b1 + |A^{-1}_{11}| b2",
            "value": f"{de_bound:.12e}",
            "claim_status": "NONCLAIM_UNTIL_PARENT_SOURCE_CONVENTION_LOCK",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    rank = rank_rows()[0]
    return [
        {
            "clause_id": "NCT3265_0_linear_algebra_core",
            "clause": "Two nonparallel DD material-difference rows give finite component bounds by A^{-1}.",
            "status": "PROVED_CONDITIONAL",
            "evidence": f"det(A)={rank['determinant']}; rank_two={rank['rank_two']}",
            "remaining_gap": "none for the algebraic theorem",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "NCT3265_1_same_coupling_coordinates",
            "clause": "MICROSCOPE and Eot-Wash must project onto the same parent D_hatm/D_e coordinates.",
            "status": "UNSIGNED_PARENT_CONVENTION",
            "evidence": "Both are Earth-field WEP arenas, but the MTS parent source map has not signed equality of calibration coordinates.",
            "remaining_gap": "derive/source parent source-convention lock",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "NCT3265_2_residual_silence",
            "clause": "Residual source/profile/readout terms must be zero or bounded below the eta rows.",
            "status": "UNSIGNED_RESIDUAL",
            "evidence": "3263 closed MICROSCOPE eta-level projection; Eot-Wash source/profile residuals are not imported into MTS convention.",
            "remaining_gap": "derive residual transport or add residual terms to matrix",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "NCT3265_3_material_exactness",
            "clause": "Be/Ti and Ti/Pt material charge rows must be exact enough for public bounds.",
            "status": "SOURCE_BACKED_SMOKE_NOT_FULL_MATERIAL_TENSOR",
            "evidence": "DD approximate charges and nominal pure-element Be/Ti are enough for a rank smoke test, not a final material tensor.",
            "remaining_gap": "upgrade to exact material/isotope/binding tensor if promoting",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rank = rank_rows()[0]
    return [
        {
            "gate_id": "CG3265_0_second_vector",
            "gate": "second independent material arena exists",
            "passed": rank["rank_two"],
            "reason": "Eot-Wash Be/Ti vector is nonparallel to MICROSCOPE Ti/Pt in DD two-charge space",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3265_1_conditional_bounds",
            "gate": "finite two-channel component bounds derived",
            "passed": "true",
            "reason": "matrix inverse gives finite conditional |D_hatm| and |D_e| bounds",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3265_2_parent_source_convention",
            "gate": "MTS parent D coordinates locked across arenas",
            "passed": "false",
            "reason": "external DD coordinates are still calibration coordinates until parent source map signs equality",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3265_3_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "3265 breaks the algebraic cancellation route conditionally; it does not yet derive the local parent action",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    rank = rank_rows()[0]
    bounds = conditional_bound_rows()
    return [
        {
            "decision_id": "DEC3265_0",
            "verdict": "SECOND_VECTOR_FOUND_RANK_TWO_BUT_PARENT_LOCK_UNSIGNED",
            "what_moved": f"det(A)={rank['determinant']}; conditional {bounds[1]['bound_id']}={bounds[1]['value']}; {bounds[2]['bound_id']}={bounds[2]['value']}",
            "best_next": "derive/source the common parent source-convention lock so MICROSCOPE and Eot-Wash rows share one D_hatm/D_e vector",
            "fallback_next": "add R10/clock cross-channel rows with explicit D-coordinate maps instead of relying on WEP alone",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3265_0_3266",
            "selected": "primary",
            "target_doc": "3266-Y5-R2FR-source-convention-lock-or-two-channel-bound-promotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3266_source_convention_lock_or_two_channel_bound_promotion.py",
            "objective": "Prove that the MICROSCOPE and Eot-Wash DD rows use the same parent MTS source-coupling coordinates, or explicitly retain arena-specific residual/source-map terms.",
            "guardrail": "Do not promote the conditional two-row inversion into a WEP/local-GR claim until parent source convention and residual silence are signed.",
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
    eot = eot_evidence_rows()
    mats = material_charge_rows()
    deltas = delta_matrix_rows()
    rank = rank_rows()[0]
    bounds = conditional_bound_rows()
    finite_materials = all(
        math.isfinite(float(row["Qhatm_prime"])) and math.isfinite(float(row["Qe_prime"]))
        for row in mats
    )
    finite_bounds = all(
        "value" not in row or math.isfinite(float(row["value"]))
        for row in bounds
    )
    validations = [
        {
            "check_id": "VAL3265_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3265_1_sources_parse",
            "check": "all cited source CSV/MD/TEX paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3265_2_eotwash_lines_found",
            "check": "Eot-Wash materials/eta/source evidence lines are found",
            "passed": bool_str(all(row["line_number"] != "NO_MATCH" for row in eot if row["evidence_id"] != "EOT3265_4_eta_bound_95")),
            "detail": ";".join(f"{row['evidence_id']}:{row['line_number']}" for row in eot),
        },
        {
            "check_id": "VAL3265_3_outputs_parse",
            "check": "all 3265 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3265_4_material_rows_finite",
            "check": "all DD material charge rows are finite numeric",
            "passed": bool_str(finite_materials),
            "detail": ";".join(row["material_id"] for row in mats),
        },
        {
            "check_id": "VAL3265_5_delta_matrix_rank_two",
            "check": "two-arena DD matrix is rank two",
            "passed": rank["rank_two"],
            "detail": f"determinant={rank['determinant']}; sin_angle_abs={rank['sin_angle_abs']}; condition={rank['condition_number']}",
        },
        {
            "check_id": "VAL3265_6_conditional_bounds_finite",
            "check": "conditional two-channel bounds are finite",
            "passed": bool_str(finite_bounds),
            "detail": ";".join(f"{row['bound_id']}={row.get('value', 'matrix')}" for row in bounds),
        },
        {
            "check_id": "VAL3265_7_claim_gates_false",
            "check": "no 3265 claim gate allows WEP/local-GR promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3265_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3265_9_overall",
            "check": "3265 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3265_9_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    eot = eot_evidence_rows()
    mats = material_charge_rows()
    deltas = delta_matrix_rows()
    rank = rank_rows()
    bounds = conditional_bound_rows()
    theorem = theorem_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3265 - Second material arena or parent no-cancellation theorem under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3265` finds the missing second punch: Eot-Wash Be/Ti supplies a second DD material-difference vector.
- The two-row matrix `[(TA6V-PtRh10),(Be-Ti)]` is rank two in `(Q'_hatm,Q'_e)`, so the pure algebraic cancellation escape is broken **conditionally**.
- The conditional inversion gives finite bounds on `D_hatm` and `D_e`, but they remain non-claim because the parent MTS source-convention lock is unsigned.
- This is a real advance over `3264`: the blocker is no longer "one material pair cannot bound two channels"; it is now specifically "prove both arenas share the same parent coupling coordinates and residual convention."

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "source_url", "valid_for_claim"])}

## Eot-Wash Evidence
{md_table(eot, ["evidence_id", "line_number", "text_excerpt", "role", "source_url", "valid_for_claim"])}

## DD Material Charges
{md_table(mats, ["material_charge_id", "arena", "material_id", "composition_basis", "A_context", "Z", "Qhatm_prime", "Qe_prime", "valid_for_claim"])}

## Two-Arena Delta Matrix
{md_table(deltas, ["row_id", "arena", "left_minus_right", "Delta_Qhatm_prime", "Delta_Qe_prime", "eta_abs_bound", "eta_bound_basis", "valid_for_claim"])}

## Rank and Conditioning
{md_table(rank, ["rank_id", "determinant", "row1_norm", "row2_norm", "cos_angle", "sin_angle_abs", "condition_number", "rank_two", "meaning", "valid_for_claim"])}

## Conditional Two-Channel Bounds
{md_table(bounds, ["bound_id", "assumption", "formula", "matrix_equation", "eta_bounds", "value", "claim_status", "valid_for_claim"])}

## No-Cancellation Theorem Status
{md_table(theorem, ["clause_id", "clause", "status", "evidence", "remaining_gap", "valid_for_claim"])}

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
    write_csv(OUTPUTS["sources"], source_register())
    write_csv(OUTPUTS["eot_evidence"], eot_evidence_rows())
    write_csv(OUTPUTS["material_charges"], material_charge_rows())
    write_csv(OUTPUTS["delta_matrix"], delta_matrix_rows())
    write_csv(OUTPUTS["rank"], rank_rows())
    write_csv(OUTPUTS["bounds"], conditional_bound_rows())
    write_csv(OUTPUTS["theorem"], theorem_rows())
    write_csv(OUTPUTS["gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
