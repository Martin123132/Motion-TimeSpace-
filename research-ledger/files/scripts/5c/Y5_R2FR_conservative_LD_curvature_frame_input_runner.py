from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LAB_R10 = ROOT / "source-intake" / "lab-r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAW = RAB_SECTOR / "raw"
ACCEPTED = RAB_SECTOR / "accepted"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1660"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1660-Y5-R2FR-conservative-LD-curvature-frame-input-runner.md"

NIST_TEXT = LAB_R10 / "NIST_CODATA_2022_wall_chart.txt"
NIST_PDF = LAB_R10 / "NIST_CODATA_2022_wall_chart.pdf"
JPL_HTML = LAB_R10 / "JPL_planetary_physical_parameters.html"

SOURCE_FILES = {
    "1659_doc": ROOT / "1659-Y5-R2FR-LD-mapping-rule-or-conservative-geometry-bound.md",
    "1659_validation": OUT / "P8_Y5_BRR545_1659_VALIDATION.csv",
    "1659_ld_row": OUT / "P8_Y5_PARENT_QLOC_1659_CONSERVATIVE_LD_ROW.csv",
    "1659_nablaploc": OUT / "P8_Y5_PARENT_QLOC_1659_NABLAPLOC_READY_TEMPLATE.csv",
    "nist_pdf": NIST_PDF,
    "nist_text": NIST_TEXT,
    "jpl_html": JPL_HTML,
}

NEEDLES = {
    "1659_doc": ["L_D_upper = 52 mm / 2 = 2.6e-2 m", "Curvature norms, frame terms, constants, and `M_H_ref` remain missing"],
    "1659_validation": ["VAL1659_OVERALL", "PASS"],
    "1659_ld_row": ["CLD1659_0_full_support_upper_bound", "2.6e-2"],
    "1659_nablaploc": ["Riemann_norm_m2", "C_Fermi"],
    "nist_pdf": [],
    "nist_text": ["speed of light in vacuum c 299 792 458", "Newtonian constant of gravitation G 6. 674 30"],
    "jpl_html": ["<b>Earth</b>", "6371.0084", "5.97217"],
}

SOURCE_URLS = {
    "nist_pdf": "https://pml.nist.gov/cuu/pdf/wall_2022.pdf",
    "nist_text": "https://pml.nist.gov/cuu/pdf/wall_2022.pdf",
    "jpl_html": "https://ssd.jpl.nasa.gov/planets/phys_par.html",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1660_SOURCE_REGISTER.csv"
EARTH_MONOPOLE_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1660_EARTH_MONOPOLE_INPUTS.csv"
CURVATURE_PROXY = OUT / "P8_Y5_PARENT_QLOC_1660_CURVATURE_PROXY.csv"
FERMI_CONSTANT_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1660_FERMI_CONSTANT_LEDGER.csv"
FRAME_TERM_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1660_FRAME_TERM_LEDGER.csv"
NABLAPLOC_PARTIAL_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1660_NABLAPLOC_PARTIAL_TEMPLATE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1660_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1660_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1660_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1660_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    EARTH_MONOPOLE_INPUTS,
    CURVATURE_PROXY,
    FERMI_CONSTANT_LEDGER,
    FRAME_TERM_LEDGER,
    NABLAPLOC_PARTIAL_TEMPLATE,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    EARTH_MONOPOLE_INPUTS,
    CURVATURE_PROXY,
    FERMI_CONSTANT_LEDGER,
    FRAME_TERM_LEDGER,
    NABLAPLOC_PARTIAL_TEMPLATE,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    CURVATURE_PROXY: [
        QUARANTINE / "CURVATURE_PROXY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_curvature_proxy_nonclaim_1660.csv",
        QUEUE / "JR1660_CURVATURE_PROXY_NONCLAIM.csv",
    ],
    FERMI_CONSTANT_LEDGER: [
        QUARANTINE / "FERMI_CONSTANT_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_fermi_constant_ledger_nonclaim_1660.csv",
        QUEUE / "JR1660_FERMI_CONSTANT_LEDGER_NONCLAIM.csv",
    ],
    FRAME_TERM_LEDGER: [
        QUARANTINE / "FRAME_TERM_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_frame_term_ledger_nonclaim_1660.csv",
        QUEUE / "JR1660_FRAME_TERM_LEDGER_NONCLAIM.csv",
    ],
    NABLAPLOC_PARTIAL_TEMPLATE: [
        QUARANTINE / "NABLAPLOC_PARTIAL_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_nablaPloc_partial_template_nonclaim_1660.csv",
        QUEUE / "JR1660_NABLAPLOC_PARTIAL_TEMPLATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1660.csv",
        QUEUE / "JR1660_NEXT_TARGET_NONCLAIM.csv",
    ],
}

SPEED_OF_LIGHT_M_PER_S = 299_792_458.0
NEWTON_G_SI = 6.67430e-11
EARTH_MASS_KG = 5.97217e24
EARTH_MEAN_RADIUS_M = 6.3710084e6
LD_UPPER_M = 2.6e-2


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, RAW, ACCEPTED, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def find_line(path: Path, pattern: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if pattern in line:
            return index
    return -1


def format_scientific(value: float) -> str:
    return f"{value:.8e}"


def curvature_values() -> dict[str, float]:
    schwarzschild_length_m = NEWTON_G_SI * EARTH_MASS_KG / (SPEED_OF_LIGHT_M_PER_S**2)
    base_curvature_m2 = schwarzschild_length_m / (EARTH_MEAN_RADIUS_M**3)
    kretschmann_sqrt_proxy_m2 = math.sqrt(48.0) * base_curvature_m2
    radial_gradient_proxy_m3 = 3.0 * kretschmann_sqrt_proxy_m2 / EARTH_MEAN_RADIUS_M
    first_order_projector_term_m1 = LD_UPPER_M * kretschmann_sqrt_proxy_m2
    second_order_projector_term_m1 = (LD_UPPER_M**2) * radial_gradient_proxy_m3
    return {
        "schwarzschild_length_m": schwarzschild_length_m,
        "base_curvature_m2": base_curvature_m2,
        "kretschmann_sqrt_proxy_m2": kretschmann_sqrt_proxy_m2,
        "radial_gradient_proxy_m3": radial_gradient_proxy_m3,
        "first_order_projector_term_m1": first_order_projector_term_m1,
        "second_order_projector_term_m1": second_order_projector_term_m1,
    }


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "source_url": SOURCE_URLS.get(source_id, "local_prior_checkpoint"),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles) if needles else "binary/source presence only",
                "role": "1660 conservative-LD curvature/frame input runner",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def earth_input_rows() -> list[dict[str, object]]:
    rows = [
        ("CONST1660_0_c", "speed_of_light", SPEED_OF_LIGHT_M_PER_S, "m s^-1", "NIST_CODATA_2022_wall_chart", str(NIST_TEXT), find_line(NIST_TEXT, "speed of light in vacuum c 299 792 458"), "exact"),
        ("CONST1660_1_G", "Newtonian_constant_of_gravitation", NEWTON_G_SI, "m^3 kg^-1 s^-2", "NIST_CODATA_2022_wall_chart", str(NIST_TEXT), find_line(NIST_TEXT, "Newtonian constant of gravitation G 6. 674 30"), "CODATA_2022"),
        ("CONST1660_2_Mearth", "Earth_mass", EARTH_MASS_KG, "kg", "JPL_planetary_physical_parameters", str(JPL_HTML), find_line(JPL_HTML, "5.97217"), "planetary_parameter"),
        ("CONST1660_3_Rearth_mean", "Earth_mean_radius", EARTH_MEAN_RADIUS_M, "m", "JPL_planetary_physical_parameters", str(JPL_HTML), find_line(JPL_HTML, "6371.0084"), "planetary_parameter"),
        ("CONST1660_4_LD_upper", "conservative_LD_upper", LD_UPPER_M, "m", "1659_conservative_LD_row", str(OUT / "P8_Y5_PARENT_QLOC_1659_CONSERVATIVE_LD_ROW.csv"), 2, "internal_nonclaim_method"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "value": format_scientific(float(value)),
            "units": units,
            "source": source,
            "source_path": source_path,
            "source_line": source_line,
            "source_status": source_status,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, quantity, value, units, source, source_path, source_line, source_status in rows
    ]


def curvature_proxy_rows() -> list[dict[str, object]]:
    values = curvature_values()
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CURV1660_0_earth_monopole_proxy",
            "domain_id": "lab_R10_compact_fermi_tube",
            "metric_background": "weak_field_Earth_monopole_proxy",
            "formula_Riemann_norm": "sqrt(48)*G*M_E/(c^2*R_E^3)",
            "formula_nabla_Riemann_norm": "3*Riemann_norm/R_E",
            "Riemann_norm_m2": format_scientific(values["kretschmann_sqrt_proxy_m2"]),
            "nabla_Riemann_norm_m3": format_scientific(values["radial_gradient_proxy_m3"]),
            "LD_times_Riemann_m1": format_scientific(values["first_order_projector_term_m1"]),
            "LD2_times_nabla_Riemann_m1": format_scientific(values["second_order_projector_term_m1"]),
            "source_status": "SOURCE_BACKED_EARTH_MONOPOLE_PROXY_NONCLAIM",
            "limitations": "not full laboratory curvature model; ignores local masses, multipoles, apparatus frame motion, and parent projector constants",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def fermi_constant_rows() -> list[dict[str, object]]:
    rows = [
        ("FERMI1660_0_C_Fermi", "C_Fermi", "MISSING_PARENT_PROJECTOR_THEOREM", "needs explicit local projector/Fermi-coordinate norm inequality"),
        ("FERMI1660_1_C_Fermi2", "C_Fermi2", "MISSING_PARENT_PROJECTOR_THEOREM", "needs second-order projector drift theorem or conservative analytic bound"),
        ("FERMI1660_2_norm_choice", "operator_norm_choice", "MISSING_NORM_CONTRACT", "must specify tensor/operator norm used in nabla_Ploc_Linf"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "value": "MISSING",
            "units": "dimensionless" if quantity.startswith("C_") else "method_contract",
            "status": status,
            "blocker": blocker,
            "source_path": "MISSING_PARENT_DERIVATION",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, quantity, status, blocker in rows
    ]


def frame_term_rows() -> list[dict[str, object]]:
    rows = [
        ("FRAME1660_0_lab_motion", "lab_frame_acceleration_rotation_terms", "MISSING_FRAME_CONTRACT", "must decide whether Earth rotation, suspension turntable, and local acceleration enter q_loc residual"),
        ("FRAME1660_1_apparatus_orientation", "apparatus_orientation_projection", "MISSING_ARENA_PROJECTION", "Lee-Adelberger geometry source does not by itself define MTS projector orientation terms"),
        ("FRAME1660_2_local_masses", "nearby_mass_curvature_terms", "MISSING_LOCAL_MASS_MODEL", "near-apparatus density/multipole contribution not source-modelled"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "value": "MISSING",
            "units": "m^-1 contribution or projection coefficient",
            "status": status,
            "blocker": blocker,
            "source_path": "MISSING_ARENA_SOURCE_OR_PARENT_SILENCE_THEOREM",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, quantity, status, blocker in rows
    ]


def nablaploc_partial_rows() -> list[dict[str, object]]:
    values = curvature_values()
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPLR1660_0_partial_conservative_LD_bound",
            "domain_id": "lab_R10_compact_fermi_tube",
            "partial_formula": "nabla_Ploc_Linf <= C_Fermi*LD*Riemann_norm + C_Fermi2*LD^2*nabla_Riemann_norm + frame_terms",
            "LD_m": format_scientific(LD_UPPER_M),
            "Riemann_norm_m2": format_scientific(values["kretschmann_sqrt_proxy_m2"]),
            "nabla_Riemann_norm_m3": format_scientific(values["radial_gradient_proxy_m3"]),
            "LD_times_Riemann_m1": format_scientific(values["first_order_projector_term_m1"]),
            "LD2_times_nabla_Riemann_m1": format_scientific(values["second_order_projector_term_m1"]),
            "C_Fermi": "MISSING",
            "C_Fermi2": "MISSING",
            "frame_terms": "MISSING",
            "current_status": "PARTIAL_NUMERIC_PROXY_BLOCKED_BY_CONSTANTS_AND_FRAME_TERMS",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1660_0_curvature_proxy", "Earth-monopole curvature proxy is numeric", "INTERNAL_SOURCE_PROXY_ONLY", "NONCLAIM", "not full lab curvature model"),
        ("CG1660_1_fermi_constants", "C_Fermi and C_Fermi2 are source-backed", False, "BLOCKED", "parent projector theorem missing"),
        ("CG1660_2_frame_terms", "frame terms are zero or bounded", False, "BLOCKED", "frame contract/silence theorem missing"),
        ("CG1660_3_nabla_Ploc", "nabla_Ploc_Linf numeric bound is accepted", False, "BLOCKED", "constants and frame terms missing"),
        ("CG1660_4_local", "local GR/Newton/PPN/R10/WEP follows", False, "NO_CLAIM", "no normalized residual vector or M_H_ref denominator"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1660_0_curvature", "ACCEPT_EARTH_MONOPOLE_PROXY_NONCLAIM", "sourced constants give a concrete curvature scale", "carry as proxy input, not as local-GR evidence"),
        ("DEC1660_1_constants", "BLOCK_ON_FERMI_PROJECTOR_CONSTANTS", "C_Fermi, C_Fermi2, and norm contract control the actual bound", "derive a projector/Fermi norm theorem next"),
        ("DEC1660_2_frame", "BLOCK_ON_FRAME_TERMS_OR_SILENCE_THEOREM", "lab rotation/projection terms may dominate if not silenced", "derive frame silence or source apparatus frame model"),
        ("DEC1660_3_next", "NEXT_1661_FERMI_PROJECTOR_CONSTANT_THEOREM", "the curvature proxy is no longer the main blocker", "attempt analytic constants before more data plumbing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1661-Y5-R2FR-Fermi-projector-constant-theorem-or-frame-silence.md",
            "script": "scripts/Y5_R2FR_Fermi_projector_constant_theorem_or_frame_silence.py",
            "objective": "derive or bound C_Fermi, C_Fermi2, the norm contract, and frame-term silence for the finite-domain local projector residual",
            "success_condition": "constants/frame terms become theorem-backed or the local projector route stays explicitly closure-only",
            "forbidden_shortcuts": "no setting C_Fermi=1 without proof; no dropping frame terms by assumption; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, earth_inputs, curvature, fermi, frame, nablaploc, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any(FORMALIZATION.rglob("*1660*")) if FORMALIZATION.exists() else False
    curvature_numeric = float(curvature[0]["Riemann_norm_m2"]) > 0 and float(curvature[0]["nabla_Riemann_norm_m3"]) > 0
    constants_blocked = all(row["value"] == "MISSING" and row["valid_for_claim"] is False for row in fermi)
    frame_blocked = all(row["value"] == "MISSING" and row["valid_for_claim"] is False for row in frame)

    checks = [
        ("VAL1660_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1660 source paths exist and needles are present"),
        ("VAL1660_1_1659_passed", any(row["source_id"] == "1659_validation" and row["needles_found"] for row in source_rows), "1659 validation is source-registered as PASS"),
        ("VAL1660_2_earth_inputs_positive", all(float(row["value"]) > 0 and int(row["source_line"]) != -1 for row in earth_inputs), "Earth constants and L_D input are positive and source-lined"),
        ("VAL1660_3_curvature_proxy_numeric", curvature_numeric, "Earth-monopole curvature and gradient proxy are positive"),
        ("VAL1660_4_constants_block_scoring", constants_blocked, "Fermi constants and norm contract remain explicit blockers"),
        ("VAL1660_5_frame_terms_block_scoring", frame_blocked, "frame terms remain explicit blockers"),
        ("VAL1660_6_nablaploc_partial_nonclaim", nablaploc[0]["current_status"] == "PARTIAL_NUMERIC_PROXY_BLOCKED_BY_CONSTANTS_AND_FRAME_TERMS", "nabla_Ploc template is partial and nonclaim"),
        ("VAL1660_7_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1660_8_next_target_selected", next_targets[0]["next_target"] == "1661-Y5-R2FR-Fermi-projector-constant-theorem-or-frame-silence.md", "next target selects Fermi/projector constant theorem"),
        ("VAL1660_9_csv_parse", generated_csv_parse, "all generated 1660 CSVs parse"),
        ("VAL1660_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1660 generated rows keep MTS claim/no-score flags false"),
        ("VAL1660_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1660_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1660_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1660_14_formalization_untouched", not formalization_dirty, "no 1660 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1660_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1660 conservative-LD curvature/frame input validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(source_rows, earth_inputs, curvature, fermi, frame, nablaploc, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1660 - Conservative L_D Curvature Frame Input Runner

**Private status:** nonclaim lower-input checkpoint. No `nabla_Ploc` bound, R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1660` gets one real numerical foothold and then stops exactly where it should:

```text
L_D_upper = 2.6e-2 m
Riemann_norm proxy = {curvature[0]["Riemann_norm_m2"]} m^-2
nabla_Riemann_norm proxy = {curvature[0]["nabla_Riemann_norm_m3"]} m^-3
LD*Riemann proxy = {curvature[0]["LD_times_Riemann_m1"]} m^-1
```

That is not a local-GR win. It is only an Earth-monopole curvature proxy built from source-backed constants. The actual finite-domain projector residual is still blocked by `C_Fermi`, `C_Fermi2`, the norm contract, and lab-frame/projection terms.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "source_url", "path_exists", "needles_found", "role"])}

## Earth Monopole Inputs

{markdown_table(earth_inputs, ["row_id", "quantity", "value", "units", "source", "source_line", "source_status"])}

## Curvature Proxy

{markdown_table(curvature, ["row_id", "formula_Riemann_norm", "formula_nabla_Riemann_norm", "Riemann_norm_m2", "nabla_Riemann_norm_m3", "LD_times_Riemann_m1", "LD2_times_nabla_Riemann_m1", "limitations"])}

## Fermi Constant Ledger

{markdown_table(fermi, ["row_id", "quantity", "value", "status", "blocker"])}

## Frame Term Ledger

{markdown_table(frame, ["row_id", "quantity", "value", "status", "blocker"])}

## nablaPloc Partial Template

{markdown_table(nablaploc, ["row_id", "partial_formula", "LD_m", "Riemann_norm_m2", "nabla_Riemann_norm_m3", "C_Fermi", "C_Fermi2", "frame_terms", "current_status"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

The geometry branch is no longer blocked by not knowing any curvature scale. It is blocked by the local projector theorem itself. The next proof attempt should therefore target the constants/frame silence, not more R10 geometry.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    earth_inputs = earth_input_rows()
    curvature = curvature_proxy_rows()
    fermi = fermi_constant_rows()
    frame = frame_term_rows()
    nablaploc = nablaploc_partial_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (EARTH_MONOPOLE_INPUTS, earth_inputs),
        (CURVATURE_PROXY, curvature),
        (FERMI_CONSTANT_LEDGER, fermi),
        (FRAME_TERM_LEDGER, frame),
        (NABLAPLOC_PARTIAL_TEMPLATE, nablaploc),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, earth_inputs, curvature, fermi, frame, nablaploc, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, earth_inputs, curvature, fermi, frame, nablaploc, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1660 validation failed; see P8_Y5_BRR545_1660_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1660 validation PASS")


if __name__ == "__main__":
    main()
