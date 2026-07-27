from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAW = RAB_SECTOR / "raw"
ACCEPTED = RAB_SECTOR / "accepted"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1657"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1657-Y5-R2FR-lab-R10-nablaPloc-MHref-source-pack.md"

SOURCE_FILES = {
    "1656_doc": ROOT / "1656-Y5-R2FR-local-domain-selector-for-nablaPloc-MHref-source-acquisition.md",
    "1656_validation": OUT / "P8_Y5_BRR545_1656_VALIDATION.csv",
    "1656_next": OUT / "P8_Y5_PARENT_QLOC_1656_NEXT_TARGET.csv",
    "1656_domain": OUT / "P8_Y5_PARENT_QLOC_1656_DOMAIN_CANDIDATE_SELECTOR.csv",
    "1656_requirements": OUT / "P8_Y5_PARENT_QLOC_1656_SELECTED_DOMAIN_REQUIREMENTS.csv",
    "1656_units": OUT / "P8_Y5_PARENT_QLOC_1656_UNIT_CONVENTION.csv",
    "1656_nablaploc": OUT / "P8_Y5_PARENT_QLOC_1656_NABLAPLOC_SOURCE_TEMPLATE.csv",
    "1656_mhref": OUT / "P8_Y5_PARENT_QLOC_1656_MHREF_SOURCE_TEMPLATE.csv",
    "fermi_domain_1209": OUT / "P8_Y5_R10_1209_FERMI_DOMAIN_DERIVATION.csv",
    "domain_motion_1209": OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv",
    "source_pack_777": OUT / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv",
    "queue_1656_domain": QUEUE / "JR1656_SELECTED_DOMAIN_REQUIREMENTS_NONCLAIM.csv",
    "queue_1656_nablaploc": QUEUE / "JR1656_NABLAPLOC_SOURCE_TEMPLATE_NONCLAIM.csv",
    "queue_1656_mhref": QUEUE / "JR1656_MHREF_SOURCE_TEMPLATE_NONCLAIM.csv",
}

NEEDLES = {
    "1656_doc": ["lab_R10_compact_fermi_tube", "first empirical target"],
    "1656_validation": ["VAL1656_OVERALL", "PASS"],
    "1656_next": ["1657-Y5-R2FR-lab-R10-nablaPloc-MHref-source-pack.md", "lab_R10 source pack"],
    "1656_domain": ["DOM1656_0_lab_R10", "SELECT_FOR_ACQUISITION"],
    "1656_requirements": ["LDR1656_2_LD", "LDR1656_6_mhref"],
    "1656_units": ["UNIT1656_3_projector_gradient", "meter^-1"],
    "1656_nablaploc": ["NPLT1656_0_lab_R10_fermi_candidate", "DOMAIN_SELECTED_VALUES_MISSING"],
    "1656_mhref": ["MHRT1656_0_lab_R10_same_frame_candidate", "DENOMINATOR_DOMAIN_SELECTED_VALUES_MISSING"],
    "fermi_domain_1209": ["FDL1209_3_clean_freefall_fermi_bound", "BEST_NONCLAIM_NUMERIC_ROUTE"],
    "domain_motion_1209": ["DMP1209_1_non_geodesic_lab_bound", "BOUND_DERIVED_VALUES_MISSING"],
    "source_pack_777": ["BSM777_2_source_flux_value_input", "MISSING_SOURCE_FLUX_VALUE"],
    "queue_1656_domain": ["LDR1656_2_LD", "MISSING_NUMERIC_SOURCE"],
    "queue_1656_nablaploc": ["NPLT1656_0_lab_R10_fermi_candidate", "DOMAIN_SELECTED_VALUES_MISSING"],
    "queue_1656_mhref": ["MHRT1656_0_lab_R10_same_frame_candidate", "DENOMINATOR_DOMAIN_SELECTED_VALUES_MISSING"],
}

WEB_SOURCES = [
    {
        "web_id": "WEB1657_0_eotwash_group",
        "title": "Eot-Wash Group laboratory tests page",
        "url": "https://www.npl.washington.edu/eotwash/node/1",
        "role": "lab short-range gravity provenance and 2020 PRL context",
        "extractable_hint": "New Test of the Gravitational 1/r2 Law at separations down to 52 um; PRL 124 101101 (2020)",
        "usable_as_numeric_row": False,
        "why_not_numeric": "separation floor is not the same as L_D, curvature norm, or M_H_ref",
    },
    {
        "web_id": "WEB1657_1_aps_prl_2020",
        "title": "Phys. Rev. Lett. 124, 101101",
        "url": "https://link.aps.org/doi/10.1103/PhysRevLett.124.101101",
        "role": "primary paper landing page for the 2020 Eot-Wash short-range inverse-square-law test",
        "extractable_hint": "DOI 10.1103/PhysRevLett.124.101101",
        "usable_as_numeric_row": False,
        "why_not_numeric": "landing page/abstract is provenance; apparatus geometry must be extracted from full source tables/figures before scoring",
    },
    {
        "web_id": "WEB1657_2_arxiv_levitated",
        "title": "arXiv 2102.06848 levitated microsphere short-range gravity",
        "url": "https://arxiv.org/abs/2102.06848",
        "role": "alternative lab short-range source/test mass arena for later cross-checks",
        "extractable_hint": "characteristic scale around 10 um reported in abstract",
        "usable_as_numeric_row": False,
        "why_not_numeric": "not the selected Eot-Wash torsion lab domain and no same-frame M_H_ref row",
    },
]

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1657_SOURCE_REGISTER.csv"
WEB_SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1657_WEB_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1657_INTAKE_SCAN.csv"
LAB_R10_SOURCE_PACK = OUT / "P8_Y5_PARENT_QLOC_1657_LAB_R10_SOURCE_PACK.csv"
NABLAPLOC_ROW = OUT / "P8_Y5_PARENT_QLOC_1657_NABLAPLOC_SOURCE_ROW_CANDIDATE.csv"
FRAME_ROW = OUT / "P8_Y5_PARENT_QLOC_1657_FRAME_TERMS_SOURCE_ROW_CANDIDATE.csv"
MHREF_ROW = OUT / "P8_Y5_PARENT_QLOC_1657_MHREF_SOURCE_ROW_CANDIDATE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1657_SOURCE_PACK_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1657_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1657_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1657_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1657_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    WEB_SOURCE_REGISTER,
    INTAKE_SCAN,
    LAB_R10_SOURCE_PACK,
    NABLAPLOC_ROW,
    FRAME_ROW,
    MHREF_ROW,
    RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    WEB_SOURCE_REGISTER,
    LAB_R10_SOURCE_PACK,
    NABLAPLOC_ROW,
    FRAME_ROW,
    MHREF_ROW,
    RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    WEB_SOURCE_REGISTER: [
        QUARANTINE / "WEB_SOURCE_REGISTER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_web_source_register_nonclaim_1657.csv",
        QUEUE / "JR1657_WEB_SOURCE_REGISTER_NONCLAIM.csv",
    ],
    LAB_R10_SOURCE_PACK: [
        QUARANTINE / "LAB_R10_SOURCE_PACK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_lab_R10_source_pack_nonclaim_1657.csv",
        QUEUE / "JR1657_LAB_R10_SOURCE_PACK_NONCLAIM.csv",
    ],
    NABLAPLOC_ROW: [
        QUARANTINE / "NABLAPLOC_SOURCE_ROW_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_nablaPloc_source_row_candidate_nonclaim_1657.csv",
        QUEUE / "JR1657_NABLAPLOC_SOURCE_ROW_CANDIDATE_NONCLAIM.csv",
    ],
    MHREF_ROW: [
        QUARANTINE / "MHREF_SOURCE_ROW_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_MHref_source_row_candidate_nonclaim_1657.csv",
        QUEUE / "JR1657_MHREF_SOURCE_ROW_CANDIDATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1657.csv",
        QUEUE / "JR1657_NEXT_TARGET_NONCLAIM.csv",
    ],
}


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
        "numeric_ready",
        "score_allowed",
        "score_ready",
        "source_ready",
        "usable_as_numeric_row",
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
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1657 lab_R10 nabla_Ploc/M_H_ref source pack",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def web_source_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            **source,
            "source_status": "PROVENANCE_ONLY_NOT_NUMERIC_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source in WEB_SOURCES
    ]


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1657_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1657_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1657_2_queue", QUEUE, "nonclaim_acquisition_queue"),
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


def source_pack_rows() -> list[dict[str, object]]:
    rows = [
        ("PACK1657_0_geometry", "L_D;source-test separation;apparatus support radius;boundary rule", "WEB1657_0_eotwash_group;WEB1657_1_aps_prl_2020", "MISSING_FULL_APPARATUS_GEOMETRY_EXTRACTION"),
        ("PACK1657_1_curvature", "Riemann_norm;nabla_Riemann_norm;norm convention;Earth/lab background model", "MISSING_SOURCE", "MISSING_CURVATURE_NORM_SOURCE"),
        ("PACK1657_2_frame", "central_worldline;acceleration_norm;rotation_norm;transport_rule", "MISSING_SOURCE", "MISSING_LAB_FRAME_SOURCE"),
        ("PACK1657_3_projector_constants", "C_Fermi;C_Fermi2;C_acc;C_rot;remainder_control", "MISSING_SOURCE", "MISSING_BOUND_CONSTANTS"),
        ("PACK1657_4_MHref", "H_tau;H_ref;M_H_ref;reference_rule;apparatus/source mass bridge", "MISSING_SOURCE", "MISSING_HAMILTONIAN_DENOMINATOR"),
        ("PACK1657_5_no_cancellation", "component list;absolute sum;coefficient units;source paths", "MISSING_SOURCE", "MISSING_NO_CANCELLATION_VECTOR"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "needed_fields": needed_fields,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "source_ready": False,
            "accepted_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pack_id, needed_fields, source_anchor, current_status in rows
    ]


def nablaploc_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPLR1657_0_lab_R10_candidate",
            "formula": "C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + C_acc*acceleration_norm + C_rot*rotation_norm",
            "scale_hint": "52_um_separation_floor_from_EotWash_2020_not_equal_to_L_D",
            "L_D_m": "MISSING_FULL_GEOMETRY_EXTRACTION",
            "Riemann_norm_m2": "MISSING",
            "nabla_Riemann_norm_m3": "MISSING",
            "acceleration_norm": "MISSING_OR_DECLARED_FREEFALL",
            "rotation_norm": "MISSING_OR_DECLARED_ZERO",
            "numeric_value_m1": "MISSING",
            "source_path_or_url": "MISSING_NUMERIC_SOURCE_PATH",
            "current_status": "PROVENANCE_ANCHORED_VALUES_MISSING",
            "accepted_for_scoring": False,
            "numeric_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def frame_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FTR1657_0_lab_non_geodesic_terms",
            "quantity": "domain_motion_or_frame_terms",
            "formula": "C_D*(acceleration_norm + rotation_norm + L_D*Riemann_norm + L_D^2*nabla_Riemann_norm)",
            "frame_choice": "MISSING_FREEFALL_OR_LAB_FRAME_DECISION",
            "acceleration_norm": "MISSING",
            "rotation_norm": "MISSING",
            "source_path_or_url": "MISSING_SOURCE_PATH",
            "current_status": "FRAME_TERMS_VALUES_MISSING",
            "accepted_for_scoring": False,
            "numeric_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def mhref_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR1657_0_lab_R10_denominator_candidate",
            "definition": "M_H_ref = H_tau[S_outer] - H_ref",
            "apparatus_mass_hint": "may be recorded from lab source only as matter/source input, not as proof of Hamiltonian M_H_ref",
            "H_tau": "MISSING",
            "H_ref": "MISSING",
            "M_H_ref": "MISSING",
            "units": "kg_or_J_over_c2",
            "source_path_or_url": "MISSING_SOURCE_PATH",
            "forbidden_substitution": "NO_ORBITAL_GM_IMPORT",
            "current_status": "MISSING_HAMILTONIAN_DENOMINATOR",
            "accepted_for_scoring": False,
            "numeric_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1657_0_web_anchors", "external lab/R10 provenance anchors", "PASS_PROVENANCE_ONLY", "URLs identify candidate sources but no numeric row is accepted"),
        ("RUN1657_1_nabla_Ploc", "nabla_Ploc lab/R10 bound", "REFUSE_SCORING", "scale hint is not L_D; curvature/frame/constants missing"),
        ("RUN1657_2_MHref", "same-frame M_H_ref", "REFUSE_SCORING", "H_tau/H_ref/reference missing; apparatus mass is not Hamiltonian denominator"),
        ("RUN1657_3_joined_bound", "joined local source/projector bound", "REFUSE_SCORING", "nabla_Ploc, frame, I_commutator, B_P_flux, and M_H_ref rows not numeric/source-backed"),
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
        ("CG1657_0_sources", "lab/R10 source anchors are recorded", "INTERNAL_PROVENANCE_ONLY", "NONCLAIM", "anchors are not numeric source rows"),
        ("CG1657_1_nabla", "nabla_Ploc row is source-backed", False, "BLOCKED", "values missing"),
        ("CG1657_2_mhref", "M_H_ref denominator is source-backed", False, "BLOCKED", "Hamiltonian denominator missing"),
        ("CG1657_3_local", "local GR/Newton/PPN/R10/WEP follows from 1657", False, "NO_CLAIM", "1657 is source-pack plumbing only"),
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
        ("DEC1657_0_anchor", "WEB_PROVENANCE_RECORDED_NOT_SCORING", "Eot-Wash/APS sources anchor the selected lab domain but do not fill L_D or M_H_ref", "extract full apparatus geometry before any numeric row"),
        ("DEC1657_1_scale_hint", "DO_NOT_EQUATE_52UM_WITH_LD", "minimum separation is a useful scale hint but not automatically the Fermi tube radius/support diameter", "treat geometry extraction as a separate source row"),
        ("DEC1657_2_mhref", "APPARATUS_MASS_NOT_MHREF", "ordinary source mass can be a matter input but not the Hamiltonian denominator until H_tau-H_ref is derived or sourced", "keep denominator gate active"),
        ("DEC1657_3_next", "NEXT_1658_R10_GEOMETRY_EXTRACTION", "the next real progress is extracting geometry fields from primary source figures/tables", "build geometry extraction ledger for L_D/source-test separation/support radius/boundary rule"),
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
            "next_target": "1658-Y5-R2FR-lab-R10-geometry-extraction-ledger.md",
            "script": "scripts/Y5_R2FR_lab_R10_geometry_extraction_ledger.py",
            "objective": "extract or block the actual lab_R10 geometry fields needed for L_D/source-test separation/support radius/boundary rule from primary source material",
            "success_condition": "geometry rows are source-backed with units and extraction notes, or each remains MISSING_* with exact provenance blockers",
            "forbidden_shortcuts": "do not use separation floor as L_D without geometry definition; no orbital-GM denominator; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, web_rows, intake_rows, source_pack, nablaploc, frame_terms, mhref, runner, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1657_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1657 local source paths exist and needles are present"),
        ("VAL1657_1_web_sources_recorded", len(web_rows) == 3 and all(row["usable_as_numeric_row"] is False for row in web_rows), "web source anchors are recorded as provenance-only"),
        ("VAL1657_2_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1657_3_source_pack_complete", len(source_pack) == 6 and any(row["pack_id"] == "PACK1657_0_geometry" for row in source_pack), "lab_R10 source pack fields are enumerated"),
        ("VAL1657_4_nabla_nonclaim", nablaploc[0]["current_status"] == "PROVENANCE_ANCHORED_VALUES_MISSING" and nablaploc[0]["valid_for_claim"] is False, "nabla_Ploc candidate remains nonclaim"),
        ("VAL1657_5_frame_nonclaim", frame_terms[0]["current_status"] == "FRAME_TERMS_VALUES_MISSING" and frame_terms[0]["valid_for_claim"] is False, "frame/domain-motion candidate remains nonclaim"),
        ("VAL1657_6_mhref_nonclaim", mhref[0]["current_status"] == "MISSING_HAMILTONIAN_DENOMINATOR" and mhref[0]["valid_for_claim"] is False, "M_H_ref candidate remains nonclaim"),
        ("VAL1657_7_runner_blocks", any(row["runner_decision"] == "REFUSE_SCORING" for row in runner), "runner blocks scoring"),
        ("VAL1657_8_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1657_9_next_target_selected", next_targets[0]["next_target"] == "1658-Y5-R2FR-lab-R10-geometry-extraction-ledger.md", "next target selects R10 geometry extraction ledger"),
        ("VAL1657_10_csv_parse", generated_csv_parse, "all generated 1657 CSVs parse"),
        ("VAL1657_11_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1657 generated rows keep MTS claim/no-score flags false"),
        ("VAL1657_12_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1657_13_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1657_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1657_15_formalization_untouched", not formalization_dirty, "no 1657 outputs found under formalization-workbench"),
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
            "check_id": "VAL1657_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1657 lab_R10 nabla_Ploc/M_H_ref source pack validation",
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


def write_doc(source_rows, web_rows, intake_rows, source_pack, nablaploc, frame_terms, mhref, runner, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1657 - lab R10 nablaPloc MHref Source Pack

**Private status:** nonclaim source-pack checkpoint. No numeric `nabla_Ploc` bound, `M_H_ref`, R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1657` records external lab/R10 provenance and turns the selected domain into a source-pack ledger. The Eot-Wash/APS anchors are useful, but they are **not** enough to score:

```text
separation down to 52 um = scale/provenance hint
L_D = finite Fermi tube/support size still needs definition and extraction
M_H_ref = H_tau[S_outer] - H_ref still missing
```

So the pack refuses scoring. The next real step is geometry extraction: source-test separation, support radius/tube size, boundary rule, frame terms, and extraction notes from primary source material.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Web Source Register

{markdown_table(web_rows, ["web_id", "title", "url", "role", "extractable_hint", "usable_as_numeric_row"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## Lab R10 Source Pack

{markdown_table(source_pack, ["pack_id", "needed_fields", "source_anchor", "current_status"])}

## nablaPloc Candidate Row

{markdown_table(nablaploc, ["row_id", "formula", "scale_hint", "L_D_m", "Riemann_norm_m2", "current_status"])}

## Frame Terms Candidate Row

{markdown_table(frame_terms, ["row_id", "quantity", "formula", "frame_choice", "current_status"])}

## MHref Candidate Row

{markdown_table(mhref, ["row_id", "definition", "apparatus_mass_hint", "forbidden_substitution", "current_status"])}

## Source Pack Runner

{markdown_table(runner, ["run_id", "quantity", "runner_decision", "reason"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

We now have the right empirical bottleneck for the local projector branch: not a broad PPN run, but a source-backed geometry extraction for the lab/R10 domain. If geometry extraction succeeds, `nabla_Ploc` can become the first real finite-domain bound row. If it fails, the local branch remains explicitly source-blocked rather than vaguely speculative.
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
    source_pack = source_pack_rows()
    nablaploc = nablaploc_rows()
    frame_terms = frame_rows()
    mhref = mhref_rows()
    runner = runner_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (WEB_SOURCE_REGISTER, web_rows),
        (INTAKE_SCAN, intake_rows),
        (LAB_R10_SOURCE_PACK, source_pack),
        (NABLAPLOC_ROW, nablaploc),
        (FRAME_ROW, frame_terms),
        (MHREF_ROW, mhref),
        (RUNNER, runner),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, web_rows, intake_rows, source_pack, nablaploc, frame_terms, mhref, runner, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, web_rows, intake_rows, source_pack, nablaploc, frame_terms, mhref, runner, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1657 validation failed; see P8_Y5_BRR545_1657_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1657 validation PASS")


if __name__ == "__main__":
    main()
