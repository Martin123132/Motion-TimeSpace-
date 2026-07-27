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
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1661"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1661-Y5-R2FR-Fermi-projector-constant-theorem-or-frame-silence.md"

NIST_TEXT = LAB_R10 / "NIST_CODATA_2022_wall_chart.txt"
JPL_HTML = LAB_R10 / "JPL_planetary_physical_parameters.html"
FERMI_SOURCE = LAB_R10 / "OSTI_Manasse_Misner_Fermi_Normal_Coordinates.html"

SOURCE_FILES = {
    "1660_doc": ROOT / "1660-Y5-R2FR-conservative-LD-curvature-frame-input-runner.md",
    "1660_validation": OUT / "P8_Y5_BRR545_1660_VALIDATION.csv",
    "1660_nablaploc": OUT / "P8_Y5_PARENT_QLOC_1660_NABLAPLOC_PARTIAL_TEMPLATE.csv",
    "1660_curvature": OUT / "P8_Y5_PARENT_QLOC_1660_CURVATURE_PROXY.csv",
    "fermi_source": FERMI_SOURCE,
    "nist_text": NIST_TEXT,
    "jpl_html": JPL_HTML,
}

NEEDLES = {
    "1660_doc": ["It is blocked by the local projector theorem itself", "Fermi/projector constant theorem"],
    "1660_validation": ["VAL1660_OVERALL", "PASS"],
    "1660_nablaploc": ["PARTIAL_NUMERIC_PROXY_BLOCKED_BY_CONSTANTS_AND_FRAME_TERMS", "LD_times_Riemann_m1"],
    "1660_curvature": ["CURV1660_0_earth_monopole_proxy", "1.18820825e-22"],
    "fermi_source": ["metric is rectangular and has vanishing first derivatives", "second-order terms are explicitly computed in terms of the curvature tensor", "10.1063/1.1724316"],
    "nist_text": ["speed of light in vacuum c 299 792 458"],
    "jpl_html": ["0.99726968", "9.80", "Equatorial Gravity"],
}

SOURCE_URLS = {
    "fermi_source": "https://www.osti.gov/biblio/4672491",
    "nist_text": "https://pml.nist.gov/cuu/pdf/wall_2022.pdf",
    "jpl_html": "https://ssd.jpl.nasa.gov/planets/phys_par.html",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1661_SOURCE_REGISTER.csv"
NORM_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1661_NORM_CONTRACT.csv"
FERMI_THEOREM_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1661_FERMI_THEOREM_LEDGER.csv"
PROJECTOR_BOUND = OUT / "P8_Y5_PARENT_QLOC_1661_PROJECTOR_BOUND.csv"
FRAME_SCALE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1661_FRAME_SCALE_LEDGER.csv"
FRAME_SILENCE_GATE = OUT / "P8_Y5_PARENT_QLOC_1661_FRAME_SILENCE_GATE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1661_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1661_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1661_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1661_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    NORM_CONTRACT,
    FERMI_THEOREM_LEDGER,
    PROJECTOR_BOUND,
    FRAME_SCALE_LEDGER,
    FRAME_SILENCE_GATE,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    NORM_CONTRACT,
    FERMI_THEOREM_LEDGER,
    PROJECTOR_BOUND,
    FRAME_SCALE_LEDGER,
    FRAME_SILENCE_GATE,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    NORM_CONTRACT: [
        QUARANTINE / "NORM_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_norm_contract_nonclaim_1661.csv",
        QUEUE / "JR1661_NORM_CONTRACT_NONCLAIM.csv",
    ],
    PROJECTOR_BOUND: [
        QUARANTINE / "PROJECTOR_BOUND_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_projector_bound_nonclaim_1661.csv",
        QUEUE / "JR1661_PROJECTOR_BOUND_NONCLAIM.csv",
    ],
    FRAME_SCALE_LEDGER: [
        QUARANTINE / "FRAME_SCALE_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_frame_scale_ledger_nonclaim_1661.csv",
        QUEUE / "JR1661_FRAME_SCALE_LEDGER_NONCLAIM.csv",
    ],
    FRAME_SILENCE_GATE: [
        QUARANTINE / "FRAME_SILENCE_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_frame_silence_gate_nonclaim_1661.csv",
        QUEUE / "JR1661_FRAME_SILENCE_GATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1661.csv",
        QUEUE / "JR1661_NEXT_TARGET_NONCLAIM.csv",
    ],
}

SPEED_OF_LIGHT_M_PER_S = 299_792_458.0
EARTH_GRAVITY_M_PER_S2 = 9.80
EARTH_ROTATION_PERIOD_DAYS = 0.99726968
SECONDS_PER_DAY = 86_400.0
LD_M = 2.6e-2
RIEMANN_NORM_M2 = 1.18820825e-22
NABLA_RIEMANN_NORM_M3 = 5.59507152e-29
C_FERMI = 4.0
C_FERMI2 = 8.0


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
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


def projector_curvature_bound_m1() -> float:
    return C_FERMI * LD_M * RIEMANN_NORM_M2 + C_FERMI2 * (LD_M**2) * NABLA_RIEMANN_NORM_M3


def acceleration_frame_m1() -> float:
    return EARTH_GRAVITY_M_PER_S2 / (SPEED_OF_LIGHT_M_PER_S**2)


def rotation_frame_m1() -> float:
    omega = 2.0 * math.pi / (EARTH_ROTATION_PERIOD_DAYS * SECONDS_PER_DAY)
    return omega / SPEED_OF_LIGHT_M_PER_S


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
                "needles": "; ".join(needles),
                "role": "1661 Fermi projector constant theorem or frame silence",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def norm_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NORM1661_0_component_sup_orthonormal_Fermi",
            "norm_name": "component_sup_norm_in_orthonormal_Fermi_frame",
            "definition": "||T||_inf = max_abs_component(T) on the compact Fermi tube using the transported orthonormal tetrad",
            "why_selected": "avoids hidden tensor-norm factors and makes finite 4D component counting explicit",
            "dimension": "4D_spacetime",
            "parent_status": "METHOD_CONTRACT_SELECTED_NONCLAIM",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def fermi_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "FERMIT1661_0_geodesic_Fermi_connection_bound",
            "assumptions": "central worldline geodesic; Fermi-Walker/parallel tetrad; compact tube radius L_D; bounded curvature and first derivative; component sup norm",
            "input_expansion": "Gamma = O(x*Riemann) + O(x^2*nabla_Riemann) + higher_order_terms",
            "derived_bound": "||Gamma||_inf <= 4*L_D*||Riemann||_inf + 8*L_D^2*||nabla_Riemann||_inf + higher_order_guard",
            "C_Fermi": C_FERMI,
            "C_Fermi2": C_FERMI2,
            "source_basis": "Manasse_Misner_Fermi_normal_coordinates_second_order_curvature_expansion",
            "source_path": str(FERMI_SOURCE),
            "source_line": find_line(FERMI_SOURCE, "second-order terms are explicitly computed in terms of the curvature tensor"),
            "theorem_status": "CONDITIONAL_DERIVATION_ACCEPTED_FOR_PRIVATE_LEDGER",
            "gap": "higher-order guard and parent projection map still need explicit signing before claims",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def projector_bound_rows() -> list[dict[str, object]]:
    curvature_bound = projector_curvature_bound_m1()
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PB1661_0_conditional_geodesic_Fermi_projector_bound",
            "domain_id": "lab_R10_compact_fermi_tube",
            "LD_m": format_scientific(LD_M),
            "Riemann_norm_m2": format_scientific(RIEMANN_NORM_M2),
            "nabla_Riemann_norm_m3": format_scientific(NABLA_RIEMANN_NORM_M3),
            "C_Fermi": format_scientific(C_FERMI),
            "C_Fermi2": format_scientific(C_FERMI2),
            "bound_formula": "4*LD*R + 8*LD^2*nablaR",
            "conditional_projector_bound_m1": format_scientific(curvature_bound),
            "bound_status": "NUMERIC_CONDITIONAL_GEODESIC_FERMI_ONLY",
            "limitation": "not accepted for lab scoring until frame terms are silenced or bounded and parent projection map is signed",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def frame_scale_rows() -> list[dict[str, object]]:
    curvature_bound = projector_curvature_bound_m1()
    acceleration_scale = acceleration_frame_m1()
    rotation_scale = rotation_frame_m1()
    rows = [
        ("FRAME1661_0_surface_acceleration", "a_earth/c^2", acceleration_scale, "m^-1", "JPL equatorial gravity with NIST c", find_line(JPL_HTML, "9.80"), acceleration_scale / curvature_bound),
        ("FRAME1661_1_earth_rotation", "Omega_earth/c", rotation_scale, "m^-1", "JPL sidereal rotation period with NIST c", find_line(JPL_HTML, "0.99726968"), rotation_scale / curvature_bound),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "scale_value": format_scientific(scale_value),
            "units": units,
            "source": source,
            "source_line": source_line,
            "ratio_to_conditional_curvature_bound": format_scientific(ratio),
            "status": "FRAME_SCALE_DWARFS_CURVATURE_IF_UNSILENCED",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, quantity, scale_value, units, source, source_line, ratio in rows
    ]


def frame_silence_rows() -> list[dict[str, object]]:
    rows = [
        ("FS1661_0_geodesic_freefall_frame", "choose a local freely-falling nonrotating Fermi frame", "CONDITIONAL_SILENCE", "inertial acceleration/rotation terms are coordinate/frame artifacts in the geodesic Fermi construction"),
        ("FS1661_1_earth_fixed_lab_frame", "use the Earth-fixed R10 apparatus frame directly", "FAILS_SILENCE", "a/c^2 and Omega/c scales are sourced and larger than the conditional curvature projector bound"),
        ("FS1661_2_parent_projection_covariance", "prove q_loc is a covariant quotient residual independent of observer-frame inertial connection", "MISSING_PARENT_PROOF", "needed before freefall frame silence can be applied to Earth-fixed measurements"),
        ("FS1661_3_apparatus_transfer_map", "map Earth-fixed apparatus observables into the freefall Fermi residual without reintroducing frame terms", "MISSING_ARENA_PROJECTION", "needed for R10/WEP scoring"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "silence_route": route,
            "status": status,
            "reason": reason,
            "frame_silenced_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, route, status, reason in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1661_0_norm_contract", "norm contract selected", "INTERNAL_METHOD_ONLY", "NONCLAIM", "component sup norm needs parent adoption"),
        ("CG1661_1_C_constants", "C_Fermi and C_Fermi2 are derived", "CONDITIONAL_ONLY", "NONCLAIM", "valid only in geodesic Fermi setting with higher-order guard"),
        ("CG1661_2_projector_bound", "nabla_Ploc curvature part is numerically bounded", "CONDITIONAL_ONLY", "NONCLAIM", "frame/projection terms not silenced"),
        ("CG1661_3_frame_silence", "frame terms are zero or bounded for R10 lab", False, "BLOCKED", "Earth-fixed lab frame terms dwarf curvature unless parent covariance/projection removes them"),
        ("CG1661_4_local", "local GR/Newton/PPN/R10/WEP follows", False, "NO_CLAIM", "no signed frame silence, apparatus transfer map, or M_H_ref denominator"),
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
        ("DEC1661_0_constants", "ACCEPT_CONDITIONAL_CFERMI_BOUND_PRIVATE", "C_Fermi=4 and C_Fermi2=8 give a conservative geodesic-Fermi component-sup bound", "carry as conditional theorem row only"),
        ("DEC1661_1_frame", "FRAME_SILENCE_NOT_PROVED_FOR_EARTH_FIXED_LAB", "a/c^2 and Omega/c are source-backed and exceed curvature-bound scale if unsilenced", "derive parent covariance/projection silence before local claims"),
        ("DEC1661_2_route", "LOCAL_BRANCH_NOT_DEAD_BUT_NOW_COVARIANCE_GATED", "freefall Fermi silence is plausible but not yet connected to apparatus observables", "attack the q_loc covariance and apparatus transfer map"),
        ("DEC1661_3_next", "NEXT_1662_QLOC_COVARIANCE_APPARATUS_TRANSFER", "this is the least smuggly route to GR/Newton reduction", "prove observer-frame inertial terms are gauge/projection artifacts or keep closure-only"),
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
            "next_target": "1662-Y5-R2FR-q_loc-covariance-and-apparatus-transfer-map.md",
            "script": "scripts/Y5_R2FR_q_loc_covariance_and_apparatus_transfer_map.py",
            "objective": "prove q_loc is observer-frame covariant and Earth-fixed apparatus inertial terms are projected out or explicitly transferred into the freefall Fermi residual",
            "success_condition": "frame silence becomes parent-signed for local observables, or the local GR/Newton route is demoted to closure-only",
            "forbidden_shortcuts": "no dropping a/c^2 or Omega/c by assumption; no R10/PPN/WEP/local-GR claim without signed transfer map",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, norm_contract, theorem, projector_bound, frame_scales, frame_silence, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any(FORMALIZATION.rglob("*1661*")) if FORMALIZATION.exists() else False
    curvature_bound = float(projector_bound[0]["conditional_projector_bound_m1"])
    acceleration_ratio = float(frame_scales[0]["ratio_to_conditional_curvature_bound"])
    rotation_ratio = float(frame_scales[1]["ratio_to_conditional_curvature_bound"])
    frame_gate_blocks = any(row["status"] == "FAILS_SILENCE" for row in frame_silence) and any(row["status"].startswith("MISSING") for row in frame_silence)

    checks = [
        ("VAL1661_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1661 source paths exist and needles are present"),
        ("VAL1661_1_1660_passed", any(row["source_id"] == "1660_validation" and row["needles_found"] for row in source_rows), "1660 validation is source-registered as PASS"),
        ("VAL1661_2_norm_contract_selected", norm_contract[0]["norm_name"] == "component_sup_norm_in_orthonormal_Fermi_frame", "component sup norm contract is selected"),
        ("VAL1661_3_conditional_constants_positive", float(theorem[0]["C_Fermi"]) > 0 and float(theorem[0]["C_Fermi2"]) > 0, "conditional Fermi constants are positive"),
        ("VAL1661_4_projector_bound_numeric", curvature_bound > 0, "conditional geodesic-Fermi projector bound is numeric"),
        ("VAL1661_5_frame_scales_dominate_if_unsilenced", acceleration_ratio > 1 and rotation_ratio > 1, "sourced frame scales exceed curvature bound if unsilenced"),
        ("VAL1661_6_frame_silence_blocks_claim", frame_gate_blocks, "frame silence gate remains blocked for Earth-fixed lab claims"),
        ("VAL1661_7_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1661_8_next_target_selected", next_targets[0]["next_target"] == "1662-Y5-R2FR-q_loc-covariance-and-apparatus-transfer-map.md", "next target selects q_loc covariance and apparatus transfer"),
        ("VAL1661_9_csv_parse", generated_csv_parse, "all generated 1661 CSVs parse"),
        ("VAL1661_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1661 generated rows keep MTS claim/no-score flags false"),
        ("VAL1661_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1661_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1661_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1661_14_formalization_untouched", not formalization_dirty, "no 1661 outputs found under formalization-workbench"),
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
            "check_id": "VAL1661_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1661 Fermi projector constant theorem/frame silence validation",
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


def write_doc(source_rows, norm_contract, theorem, projector_bound, frame_scales, frame_silence, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1661 - Fermi Projector Constant Theorem Or Frame Silence

**Private status:** conditional theorem checkpoint. No R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1661` partially succeeds and then finds the real local-GR gate.

The geodesic Fermi-coordinate part can be given a conservative private bound:

```text
||Gamma||_inf <= 4 L_D ||Riemann||_inf + 8 L_D^2 ||nabla Riemann||_inf
conditional curvature-only bound = {projector_bound[0]["conditional_projector_bound_m1"]} m^-1
```

But the Earth-fixed laboratory frame cannot be silently identified with the geodesic freefall frame. The sourced frame scales are:

```text
a_earth/c^2 = {frame_scales[0]["scale_value"]} m^-1
Omega_earth/c = {frame_scales[1]["scale_value"]} m^-1
```

Those are much larger than the curvature-only bound if they enter `q_loc`. So the branch is not dead, but it is now covariance-gated: MTS must prove that `q_loc` is an observer-frame covariant quotient residual and that Earth-fixed apparatus inertial terms are projected out or transferred correctly.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "source_url", "path_exists", "needles_found", "role"])}

## Norm Contract

{markdown_table(norm_contract, ["contract_id", "norm_name", "definition", "why_selected", "parent_status"])}

## Fermi Theorem Ledger

{markdown_table(theorem, ["theorem_id", "assumptions", "input_expansion", "derived_bound", "C_Fermi", "C_Fermi2", "theorem_status", "gap"])}

## Projector Bound

{markdown_table(projector_bound, ["row_id", "LD_m", "Riemann_norm_m2", "nabla_Riemann_norm_m3", "C_Fermi", "C_Fermi2", "conditional_projector_bound_m1", "bound_status", "limitation"])}

## Frame Scale Ledger

{markdown_table(frame_scales, ["row_id", "quantity", "scale_value", "units", "source", "source_line", "ratio_to_conditional_curvature_bound", "status"])}

## Frame Silence Gate

{markdown_table(frame_silence, ["gate_id", "silence_route", "status", "reason"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is progress, not doom. The local branch has moved from "we have no constants" to "we have a conditional geodesic-Fermi bound, but frame covariance must be proven." If MTS can make `q_loc` genuinely tensorial/quotient-covariant, the large Earth-frame inertial scales become gauge or transfer-map terms rather than physical residuals. If it cannot, the local GR/Newton route stays closure-only.
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
    norm_contract = norm_contract_rows()
    theorem = fermi_theorem_rows()
    projector_bound = projector_bound_rows()
    frame_scales = frame_scale_rows()
    frame_silence = frame_silence_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (NORM_CONTRACT, norm_contract),
        (FERMI_THEOREM_LEDGER, theorem),
        (PROJECTOR_BOUND, projector_bound),
        (FRAME_SCALE_LEDGER, frame_scales),
        (FRAME_SILENCE_GATE, frame_silence),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, norm_contract, theorem, projector_bound, frame_scales, frame_silence, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, norm_contract, theorem, projector_bound, frame_scales, frame_silence, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1661 validation failed; see P8_Y5_BRR545_1661_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1661 validation PASS")


if __name__ == "__main__":
    main()
