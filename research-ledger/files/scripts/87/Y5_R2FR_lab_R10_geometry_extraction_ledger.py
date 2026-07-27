from __future__ import annotations

import csv
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
QUARANTINE = MICROSCOPE / "quarantine" / "1658"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1658-Y5-R2FR-lab-R10-geometry-extraction-ledger.md"

PRIMARY_PDF = LAB_R10 / "Lee_Adelberger_2020_arXiv_2002_11761.pdf"
PRIMARY_TEXT = LAB_R10 / "Lee_Adelberger_2020_arXiv_2002_11761.txt"

SOURCE_FILES = {
    "1657_doc": ROOT / "1657-Y5-R2FR-lab-R10-nablaPloc-MHref-source-pack.md",
    "1657_validation": OUT / "P8_Y5_BRR545_1657_VALIDATION.csv",
    "1657_next": OUT / "P8_Y5_PARENT_QLOC_1657_NEXT_TARGET.csv",
    "1657_web": OUT / "P8_Y5_PARENT_QLOC_1657_WEB_SOURCE_REGISTER.csv",
    "1657_source_pack": OUT / "P8_Y5_PARENT_QLOC_1657_LAB_R10_SOURCE_PACK.csv",
    "1657_nablaploc": OUT / "P8_Y5_PARENT_QLOC_1657_NABLAPLOC_SOURCE_ROW_CANDIDATE.csv",
    "1657_mhref": OUT / "P8_Y5_PARENT_QLOC_1657_MHREF_SOURCE_ROW_CANDIDATE.csv",
    "primary_pdf": PRIMARY_PDF,
    "primary_text": PRIMARY_TEXT,
}

NEEDLES = {
    "1657_doc": ["geometry extraction", "separation down to 52 um"],
    "1657_validation": ["VAL1657_OVERALL", "PASS"],
    "1657_next": ["1658-Y5-R2FR-lab-R10-geometry-extraction-ledger.md", "geometry fields"],
    "1657_web": ["WEB1657_1_aps_prl_2020", "PROVENANCE_ONLY_NOT_NUMERIC_ROW"],
    "1657_source_pack": ["PACK1657_0_geometry", "MISSING_FULL_APPARATUS_GEOMETRY_EXTRACTION"],
    "1657_nablaploc": ["NPLR1657_0_lab_R10_candidate", "52_um_separation_floor_from_EotWash_2020_not_equal_to_L_D"],
    "1657_mhref": ["MHR1657_0_lab_R10_denominator_candidate", "MISSING_HAMILTONIAN_DENOMINATOR"],
    "primary_pdf": [],
    "primary_text": ["separations between 52 µm and 3.0 mm", "The hole pattern diameter is 52 mm"],
}

WEB_SOURCES = [
    {
        "web_id": "WEB1658_0_arxiv_abs",
        "url": "https://arxiv.org/abs/2002.11761",
        "role": "primary abstract page with detector-attractor separation range and arXiv identity",
        "status": "PRIMARY_PROVENANCE",
    },
    {
        "web_id": "WEB1658_1_arxiv_pdf",
        "url": "https://arxiv.org/pdf/2002.11761",
        "role": "primary PDF cached locally for geometry extraction",
        "status": "PRIMARY_PDF_CACHED",
    },
    {
        "web_id": "WEB1658_2_aps_doi",
        "url": "https://link.aps.org/doi/10.1103/PhysRevLett.124.101101",
        "role": "journal DOI landing page",
        "status": "JOURNAL_PROVENANCE",
    },
]

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1658_SOURCE_REGISTER.csv"
WEB_SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1658_WEB_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1658_INTAKE_SCAN.csv"
GEOMETRY_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1658_LAB_R10_GEOMETRY_EXTRACTION_LEDGER.csv"
LD_GATE = OUT / "P8_Y5_PARENT_QLOC_1658_LD_CANDIDATE_GATE.csv"
NABLAPLOC_GEOMETRY_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1658_NABLAPLOC_GEOMETRY_TEMPLATE.csv"
MHREF_GEOMETRY_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1658_MHREF_GEOMETRY_LEDGER.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1658_GEOMETRY_REFUSAL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1658_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1658_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1658_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1658_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    WEB_SOURCE_REGISTER,
    INTAKE_SCAN,
    GEOMETRY_LEDGER,
    LD_GATE,
    NABLAPLOC_GEOMETRY_TEMPLATE,
    MHREF_GEOMETRY_LEDGER,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    WEB_SOURCE_REGISTER,
    GEOMETRY_LEDGER,
    LD_GATE,
    NABLAPLOC_GEOMETRY_TEMPLATE,
    MHREF_GEOMETRY_LEDGER,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    GEOMETRY_LEDGER: [
        QUARANTINE / "LAB_R10_GEOMETRY_EXTRACTION_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_lab_R10_geometry_extraction_ledger_nonclaim_1658.csv",
        QUEUE / "JR1658_LAB_R10_GEOMETRY_EXTRACTION_LEDGER_NONCLAIM.csv",
    ],
    LD_GATE: [
        QUARANTINE / "LD_CANDIDATE_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_LD_candidate_gate_nonclaim_1658.csv",
        QUEUE / "JR1658_LD_CANDIDATE_GATE_NONCLAIM.csv",
    ],
    NABLAPLOC_GEOMETRY_TEMPLATE: [
        QUARANTINE / "NABLAPLOC_GEOMETRY_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_nablaPloc_geometry_template_nonclaim_1658.csv",
        QUEUE / "JR1658_NABLAPLOC_GEOMETRY_TEMPLATE_NONCLAIM.csv",
    ],
    MHREF_GEOMETRY_LEDGER: [
        QUARANTINE / "MHREF_GEOMETRY_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_MHref_geometry_ledger_nonclaim_1658.csv",
        QUEUE / "JR1658_MHREF_GEOMETRY_LEDGER_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1658.csv",
        QUEUE / "JR1658_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, LAB_R10, QUARANTINE, BRANCH_RESIDUALS, RAW, ACCEPTED, QUEUE]:
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
        "geometry_claim_ready",
        "ld_selected_for_runner",
        "score_allowed",
        "score_ready",
        "source_ready",
        "use_as_LD",
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


def find_line(pattern: str) -> int:
    text = read_text(PRIMARY_TEXT)
    for index, line in enumerate(text.splitlines(), start=1):
        if pattern in line:
            return index
    return -1


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
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles) if needles else path.exists(),
                "needles": "; ".join(needles),
                "role": "1658 lab_R10 geometry extraction ledger",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def web_source_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "cached_pdf": str(PRIMARY_PDF),
            "cached_text": str(PRIMARY_TEXT),
            "usable_as_numeric_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row in WEB_SOURCES
    ]


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1658_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1658_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1658_2_queue", QUEUE, "nonclaim_acquisition_queue"),
    ]
    rows = []
    for scan_id, folder, role in scans:
        csv_count = len(list(folder.glob("*.csv"))) if folder.exists() else 0
        if folder == RAW and csv_count == 0:
            status = "NO_RAW_LIVE_ROWS"
        elif folder == ACCEPTED and csv_count == 0:
            status = "NO_ACCEPTED_LIVE_ROWS"
        elif folder == QUEUE and csv_count:
            status = "QUEUE_PRESENT_NONCLAIM"
        else:
            status = "LIVE_ROWS_REQUIRE_REVIEW"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "scan_id": scan_id,
                "folder_role": role,
                "folder_path": str(folder),
                "csv_count": csv_count,
                "status": status,
                "source_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def geometry_rows() -> list[dict[str, object]]:
    rows = [
        ("GEO1658_0_separation_range", "detector_attractor_separation_s", "52 µm to 3.0 mm", "5.2e-5 to 3.0e-3", "m", "separations between 52 µm and 3.0 mm", "SOURCE_BACKED_SCALE_HINT_NOT_LD", False, "measured facing-surface separation range, not a finite Fermi tube/support radius"),
        ("GEO1658_1_separation_definition", "s_definition", "s is separation between facing detector/attractor surfaces", "not_numeric", "definition", "between the facing surfaces", "SOURCE_BACKED_DEFINITION", False, "defines s but not the MTS compact domain radius"),
        ("GEO1658_2_hole_pattern_diameter", "hole_pattern_diameter", "52 mm", "5.2e-2", "m", "The hole pattern diameter is 52 mm", "SOURCE_BACKED_APPARATUS_SCALE_NOT_LD", False, "pattern radius 26 mm is an apparatus extent, not automatically L_D"),
        ("GEO1658_3_azimuthal_symmetry", "test_body_symmetries", "18-fold and 120-fold", "not_numeric", "dimensionless", "18-fold and 120-fold azimuthal symmetries", "SOURCE_BACKED_GEOMETRY_STRUCTURE", False, "geometry mode structure only"),
        ("GEO1658_4_test_body_thicknesses", "detector_attractor_thickness", "54 µm and 99 µm", "5.4e-5 and 9.9e-5", "m", "detector and attractor thicknesses of 54 and 99 µm", "SOURCE_BACKED_MATERIAL_THICKNESS_NOT_LD", False, "material thicknesses are not the finite tube/domain rule"),
        ("GEO1658_5_isolation_foil", "isolation_foil_thickness", "10 µm", "1.0e-5", "m", "10 µm-thick isolation foil", "SOURCE_BACKED_BOUNDARY_COMPONENT_NOT_DOMAIN_RULE", False, "shield component, not MTS compact boundary rule"),
        ("GEO1658_6_calibration_geometry", "calibration_sphere_geometry", "1.137 kg external spheres; 0.4816 g detector spheres; 16.48 mm and 19.05 cm radius circles", "mixed", "mixed", "Three 1.137 kg spheres", "SOURCE_BACKED_CALIBRATION_NOT_MHREF", False, "calibration geometry cannot supply the Hamiltonian denominator"),
        ("GEO1658_7_centering_offsets", "x0_y0_centering", "x0=(-102±2)µm; y0=(-2121±2)µm", "mixed", "m", "x0=(−102±2)µm", "SOURCE_BACKED_ALIGNMENT_NOT_DOMAIN_RULE", False, "alignment fit data, not source/support radius"),
        ("GEO1658_8_geometry_verdict", "L_D_extraction_verdict", "no extracted field is accepted as L_D", "MISSING_LD_RULE", "not_applicable", "L_D requires separate rule", "BLOCKED_BY_LD_SELECTION_RULE", False, "need a rule mapping apparatus geometry to finite Fermi tube radius/support"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "geometry_id": geometry_id,
            "field": field,
            "extracted_value": extracted_value,
            "si_value_or_range": si_value,
            "units": units,
            "source_phrase": source_phrase,
            "source_line": find_line(source_phrase) if source_phrase != "L_D requires separate rule" else -1,
            "extraction_status": status,
            "use_as_LD": use_as_ld,
            "blocker_or_note": note,
            "source_file": str(PRIMARY_TEXT),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for geometry_id, field, extracted_value, si_value, units, source_phrase, status, use_as_ld, note in rows
    ]


def ld_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("LDG1658_0_min_separation", "52 µm minimum separation", "REJECT_AS_LD", "separation floor is not support radius/tube size"),
        ("LDG1658_1_max_separation", "3.0 mm maximum separation", "REJECT_AS_LD", "measurement scan range is not domain radius"),
        ("LDG1658_2_pattern_radius", "26 mm inferred pattern radius from 52 mm diameter", "REJECT_AS_LD_PENDING_RULE", "apparatus extent needs a domain/support rule before becoming L_D"),
        ("LDG1658_3_test_body_thickness", "54/99 µm material thickness", "REJECT_AS_LD_PENDING_RULE", "thickness is not the compact exterior tube radius"),
        ("LDG1658_4_foil_thickness", "10 µm isolation foil", "REJECT_AS_LD", "shield thickness is a boundary component, not L_D"),
        ("LDG1658_5_selection_verdict", "accepted L_D", "NOT_SELECTED", "no noncircular mapping rule from extracted geometry to L_D exists yet"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "candidate": candidate,
            "decision": decision,
            "reason": reason,
            "ld_selected_for_runner": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, candidate, decision, reason in rows
    ]


def nablaploc_template_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPLG1658_0_geometry_backed_template",
            "domain_id": "lab_R10_compact_fermi_tube",
            "formula": "C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + frame_terms",
            "source_test_separation_range_m": "5.2e-5_to_3.0e-3",
            "hole_pattern_radius_m": "2.6e-2",
            "detector_thickness_m": "5.4e-5",
            "attractor_thickness_m": "9.9e-5",
            "selected_L_D_m": "MISSING_LD_SELECTION_RULE",
            "Riemann_norm_m2": "MISSING",
            "nabla_Riemann_norm_m3": "MISSING",
            "current_status": "GEOMETRY_EXTRACTED_LD_NOT_SELECTED",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def mhref_geometry_rows() -> list[dict[str, object]]:
    rows = [
        ("MHRG1658_0_calibration_spheres", "calibration sphere masses and circle radii are source-backed", "SOURCE_BACKED_CALIBRATION_ONLY", "calibration masses/geometry cannot be substituted for H_tau-H_ref"),
        ("MHRG1658_1_science_test_bodies", "platinum test-body thicknesses are source-backed", "SOURCE_BACKED_GEOMETRY_ONLY", "test-body material geometry is not the Hamiltonian source denominator"),
        ("MHRG1658_2_mhref_verdict", "M_H_ref remains missing", "MISSING_HAMILTONIAN_DENOMINATOR", "no H_tau/H_ref/reference rule extracted from geometry paper"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "extracted_or_needed": extracted_or_needed,
            "status": status,
            "blocker": blocker,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, extracted_or_needed, status, blocker in rows
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1658_0_geometry", "lab_R10 geometry extraction", "PARTIAL_PASS_NONCLAIM", "separation range, pattern diameter, thicknesses, shield thickness, and calibration geometry extracted"),
        ("RUN1658_1_LD", "L_D selection", "REFUSE_SCORING", "no rule maps extracted apparatus geometry to finite Fermi tube radius"),
        ("RUN1658_2_nabla_Ploc", "nabla_Ploc numeric row", "REFUSE_SCORING", "L_D, curvature norms, constants, and frame terms remain missing"),
        ("RUN1658_3_MHref", "M_H_ref row", "REFUSE_SCORING", "geometry paper does not supply H_tau-H_ref denominator"),
        ("RUN1658_4_local", "local_GR_Newton_PPN_R10_WEP", "REFUSE_SCORING", "geometry extraction is nonclaim and no normalized local residual bound exists"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": run_id,
            "quantity": quantity,
            "runner_decision": decision,
            "reason": reason,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for run_id, quantity, decision, reason in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1658_0_geometry", "lab/R10 geometry fields are extracted", "PARTIAL_INTERNAL_ONLY", "NONCLAIM", "several fields are source-backed but not score-ready"),
        ("CG1658_1_LD", "L_D is selected", False, "BLOCKED", "mapping rule missing"),
        ("CG1658_2_nabla", "nabla_Ploc numeric/source row is accepted", False, "BLOCKED", "L_D and curvature inputs missing"),
        ("CG1658_3_MHref", "M_H_ref is accepted", False, "BLOCKED", "H_tau/H_ref missing"),
        ("CG1658_4_local", "local GR/Newton/PPN/R10/WEP follows", False, "NO_CLAIM", "geometry extraction does not imply theory reduction"),
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
        ("DEC1658_0_geometry", "GEOMETRY_PARTIALLY_EXTRACTED", "primary arXiv text supports separation range, pattern diameter, thicknesses, shield thickness, and calibration geometry", "keep extracted fields as source-backed but nonclaim"),
        ("DEC1658_1_LD", "LD_NOT_SELECTED", "no field is automatically the finite Fermi tube/support radius", "derive or choose a conservative L_D mapping rule next"),
        ("DEC1658_2_MHref", "MHREF_NOT_FILLED_BY_GEOMETRY", "calibration/test masses do not supply H_tau-H_ref", "keep denominator acquisition separate"),
        ("DEC1658_3_next", "NEXT_1659_LD_RULE_OR_CONSERVATIVE_BOUND", "nabla_Ploc cannot compute until L_D rule is declared", "build L_D mapping-rule gate from extracted geometry"),
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
            "next_target": "1659-Y5-R2FR-LD-mapping-rule-or-conservative-geometry-bound.md",
            "script": "scripts/Y5_R2FR_LD_mapping_rule_or_conservative_geometry_bound.py",
            "objective": "derive or choose a conservative rule mapping extracted lab_R10 geometry to L_D for the finite-domain nabla_Ploc bound, or refuse L_D with exact blockers",
            "success_condition": "L_D rule is source/method-backed and noncircular, or L_D remains unselected and all scoring stays blocked",
            "forbidden_shortcuts": "do not equate 52 um separation with L_D by default; no orbital-GM denominator; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, web_rows, intake_rows, geometry, ld_gate, nablaploc, mhref, refusal, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1658_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1658 source paths exist and needles are present"),
        ("VAL1658_1_web_sources_recorded", len(web_rows) == 3 and all(row["usable_as_numeric_claim"] is False for row in web_rows), "web sources recorded as provenance/nonclaim"),
        ("VAL1658_2_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1658_3_geometry_extracted", len(geometry) == 9 and any(row["geometry_id"] == "GEO1658_0_separation_range" and row["source_line"] > 0 for row in geometry), "primary text backs extracted geometry rows"),
        ("VAL1658_4_ld_not_selected", all(row["ld_selected_for_runner"] is False for row in ld_gate) and any(row["decision"] == "NOT_SELECTED" for row in ld_gate), "L_D is not selected by shortcut"),
        ("VAL1658_5_nabla_template_blocked", nablaploc[0]["current_status"] == "GEOMETRY_EXTRACTED_LD_NOT_SELECTED" and nablaploc[0]["valid_for_claim"] is False, "nabla_Ploc template remains blocked by L_D rule"),
        ("VAL1658_6_mhref_blocked", any(row["status"] == "MISSING_HAMILTONIAN_DENOMINATOR" for row in mhref), "M_H_ref remains blocked"),
        ("VAL1658_7_refusal_runner_blocks", any(row["runner_decision"] == "REFUSE_SCORING" for row in refusal), "refusal runner blocks scoring"),
        ("VAL1658_8_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1658_9_next_target_selected", next_targets[0]["next_target"] == "1659-Y5-R2FR-LD-mapping-rule-or-conservative-geometry-bound.md", "next target selects L_D mapping rule"),
        ("VAL1658_10_csv_parse", generated_csv_parse, "all generated 1658 CSVs parse"),
        ("VAL1658_11_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1658 generated rows keep MTS claim/no-score flags false"),
        ("VAL1658_12_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1658_13_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1658_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1658_15_formalization_untouched", not formalization_dirty, "no 1658 outputs found under formalization-workbench"),
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
            "check_id": "VAL1658_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1658 lab_R10 geometry extraction ledger validation",
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


def write_doc(source_rows, web_rows, intake_rows, geometry, ld_gate, nablaploc, mhref, refusal, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1658 - lab R10 Geometry Extraction Ledger

**Private status:** nonclaim geometry extraction checkpoint. No `L_D`, `nabla_Ploc` numeric bound, `M_H_ref`, R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1658` extracts actual geometry fields from the cached arXiv primary text:

```text
detector-attractor separation range: 52 µm to 3.0 mm
hole-pattern diameter: 52 mm
detector/attractor thicknesses: 54 µm and 99 µm
isolation foil thickness: 10 µm
```

But it refuses the tempting shortcut: none of those fields is automatically the finite-domain `L_D` in the Fermi projector bound. The separation range is a source-backed scale hint; the hole-pattern radius is an apparatus extent; the test-body thicknesses are material geometry; the foil is a boundary component. A rule mapping extracted apparatus geometry to the compact Fermi tube radius is still missing.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Web Source Register

{markdown_table(web_rows, ["web_id", "url", "role", "status"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## Geometry Extraction Ledger

{markdown_table(geometry, ["geometry_id", "field", "extracted_value", "si_value_or_range", "units", "source_line", "extraction_status", "use_as_LD"])}

## L_D Candidate Gate

{markdown_table(ld_gate, ["gate_id", "candidate", "decision", "reason"])}

## nablaPloc Geometry Template

{markdown_table(nablaploc, ["row_id", "source_test_separation_range_m", "hole_pattern_radius_m", "detector_thickness_m", "attractor_thickness_m", "selected_L_D_m", "current_status"])}

## MHref Geometry Ledger

{markdown_table(mhref, ["row_id", "extracted_or_needed", "status", "blocker"])}

## Refusal Runner

{markdown_table(refusal, ["run_id", "quantity", "runner_decision", "reason"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

We now have source-backed lab/R10 geometry, but not a domain radius. That is still progress: the next mathematical question is no longer vague source acquisition; it is whether MTS can define a conservative, noncircular `L_D` mapping rule from the extracted apparatus geometry.
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
    web_rows = web_source_rows()
    intake_rows = intake_scan_rows()
    geometry = geometry_rows()
    ld_gate = ld_gate_rows()
    nablaploc = nablaploc_template_rows()
    mhref = mhref_geometry_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (WEB_SOURCE_REGISTER, web_rows),
        (INTAKE_SCAN, intake_rows),
        (GEOMETRY_LEDGER, geometry),
        (LD_GATE, ld_gate),
        (NABLAPLOC_GEOMETRY_TEMPLATE, nablaploc),
        (MHREF_GEOMETRY_LEDGER, mhref),
        (REFUSAL_RUNNER, refusal),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, web_rows, intake_rows, geometry, ld_gate, nablaploc, mhref, refusal, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, web_rows, intake_rows, geometry, ld_gate, nablaploc, mhref, refusal, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1658 validation failed; see P8_Y5_BRR545_1658_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1658 validation PASS")


if __name__ == "__main__":
    main()
