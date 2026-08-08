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
QUARANTINE = MICROSCOPE / "quarantine" / "1656"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1656-Y5-R2FR-local-domain-selector-for-nablaPloc-MHref-source-acquisition.md"

SOURCE_FILES = {
    "1655_doc": ROOT / "1655-Y5-R2FR-nablaPloc-Icommutator-bound-row-or-MHref-denominator-fill.md",
    "1655_validation": OUT / "P8_Y5_BRR545_1655_VALIDATION.csv",
    "1655_next": OUT / "P8_Y5_PARENT_QLOC_1655_NEXT_TARGET.csv",
    "1655_readiness": OUT / "P8_Y5_PARENT_QLOC_1655_BOUND_ROW_READINESS_MATRIX.csv",
    "1655_nablaploc": OUT / "P8_Y5_PARENT_QLOC_1655_NABLAPLOC_CANDIDATE_ROW.csv",
    "1655_mhref": OUT / "P8_Y5_PARENT_QLOC_1655_MHREF_DENOMINATOR_CANDIDATE_ROW.csv",
    "1655_acquisition": OUT / "P8_Y5_PARENT_QLOC_1655_ACQUISITION_QUEUE.csv",
    "domain_scope_874": OUT / "P8_Y5_R10_874_DOMAIN_SCOPE_AUDIT.csv",
    "readout_tests_893": OUT / "P8_Y5_R10_893_READOUT_DOMAIN_TESTS.csv",
    "readout_cert_969": OUT / "P8_Y5_R10_969_READOUT_DOMAIN_CERTIFICATE.csv",
    "einstein_classifier_1195": OUT / "P8_Y5_R10_1195_EINSTEIN_DOMAIN_CLASSIFIER.csv",
    "fermi_domain_1209": OUT / "P8_Y5_R10_1209_FERMI_DOMAIN_DERIVATION.csv",
    "domain_motion_1209": OUT / "P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv",
    "typed_domain_1235": OUT / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
    "support_1547": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "nablaploc_row_1208": OUT / "P8_Y5_R10_1208_SOURCE_READY_NABLAPLOC_ROW.csv",
    "mhref_gate_1652": OUT / "P8_Y5_PARENT_QLOC_1652_MHREF_FIRST_ROW_GATE.csv",
    "queue_1655_acquisition": QUEUE / "JR1655_ACQUISITION_QUEUE_NONCLAIM.csv",
    "queue_1655_nablaploc": QUEUE / "JR1655_NABLAPLOC_CANDIDATE_ROW_NONCLAIM.csv",
}

NEEDLES = {
    "1655_doc": ["closest-to-fill row is `nabla_Ploc_Linf`", "pick a physical local domain"],
    "1655_validation": ["VAL1655_OVERALL", "PASS"],
    "1655_next": ["1656-Y5-R2FR-local-domain-selector-for-nablaPloc-MHref-source-acquisition.md", "local domain"],
    "1655_readiness": ["READY1655_0_nabla_Ploc", "closest_to_fill"],
    "1655_nablaploc": ["NPLR1655_0_fermi_curvature_candidate", "SOURCE_READY_VALUES_MISSING"],
    "1655_mhref": ["MHR1655_0_same_frame_denominator_candidate", "MISSING_STABLE_MH_REF"],
    "1655_acquisition": ["ACQ1655_0_choose_local_domain", "ACQ1655_3_MHref_denominator"],
    "domain_scope_874": ["DS874_0_lab_R10", "DS874_1_solar_system_PPN"],
    "readout_tests_893": ["RDT893_1_compact_local_domain", "not_parent_locked"],
    "readout_cert_969": ["RDC969_5_verdict", "CERTIFIED_CLOSURE_NOT_DERIVATION"],
    "einstein_classifier_1195": ["EDC1195_2_generic_matter", "DEFAULT_SAFE_CLASS_FOR_LAB_MATTER_UNTIL_SOURCED"],
    "fermi_domain_1209": ["FDL1209_3_clean_freefall_fermi_bound", "BEST_NONCLAIM_NUMERIC_ROUTE"],
    "domain_motion_1209": ["DMP1209_1_non_geodesic_lab_bound", "BOUND_DERIVED_VALUES_MISSING"],
    "typed_domain_1235": ["TREQ1235_0_parent_object_language", "MISSING_PARENT_SIGNATURE"],
    "support_1547": ["SUP1547_1_compact_support", "MISSING_SOURCE_PROFILE"],
    "nablaploc_row_1208": ["SRN1208_2_fermi_curvature_row", "BEST_SOURCE_ROW_FOR_NEXT_RUN_NONCLAIM"],
    "mhref_gate_1652": ["MHG1652_7_first_row_verdict", "FIRST_ROW_NOT_ACCEPTED"],
    "queue_1655_acquisition": ["ACQ1655_0_choose_local_domain", "SOURCE_INPUT_REQUIRED"],
    "queue_1655_nablaploc": ["NPLR1655_0_fermi_curvature_candidate", "SOURCE_READY_VALUES_MISSING"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1656_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1656_INTAKE_SCAN.csv"
DOMAIN_CANDIDATES = OUT / "P8_Y5_PARENT_QLOC_1656_DOMAIN_CANDIDATE_SELECTOR.csv"
SELECTED_DOMAIN = OUT / "P8_Y5_PARENT_QLOC_1656_SELECTED_DOMAIN_REQUIREMENTS.csv"
UNIT_CONVENTION = OUT / "P8_Y5_PARENT_QLOC_1656_UNIT_CONVENTION.csv"
NABLAPLOC_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1656_NABLAPLOC_SOURCE_TEMPLATE.csv"
MHREF_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1656_MHREF_SOURCE_TEMPLATE.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1656_DOMAIN_REFUSAL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1656_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1656_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1656_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1656_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    INTAKE_SCAN,
    DOMAIN_CANDIDATES,
    SELECTED_DOMAIN,
    UNIT_CONVENTION,
    NABLAPLOC_TEMPLATE,
    MHREF_TEMPLATE,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    DOMAIN_CANDIDATES,
    SELECTED_DOMAIN,
    UNIT_CONVENTION,
    NABLAPLOC_TEMPLATE,
    MHREF_TEMPLATE,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    DOMAIN_CANDIDATES: [
        QUARANTINE / "DOMAIN_CANDIDATE_SELECTOR_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_domain_candidate_selector_nonclaim_1656.csv",
        QUEUE / "JR1656_DOMAIN_CANDIDATE_SELECTOR_NONCLAIM.csv",
    ],
    SELECTED_DOMAIN: [
        QUARANTINE / "SELECTED_DOMAIN_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_selected_domain_requirements_nonclaim_1656.csv",
        QUEUE / "JR1656_SELECTED_DOMAIN_REQUIREMENTS_NONCLAIM.csv",
    ],
    UNIT_CONVENTION: [
        QUARANTINE / "UNIT_CONVENTION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_unit_convention_nonclaim_1656.csv",
        QUEUE / "JR1656_UNIT_CONVENTION_NONCLAIM.csv",
    ],
    NABLAPLOC_TEMPLATE: [
        QUARANTINE / "NABLAPLOC_SOURCE_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_nablaPloc_source_template_nonclaim_1656.csv",
        QUEUE / "JR1656_NABLAPLOC_SOURCE_TEMPLATE_NONCLAIM.csv",
    ],
    MHREF_TEMPLATE: [
        QUARANTINE / "MHREF_SOURCE_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_MHref_source_template_nonclaim_1656.csv",
        QUEUE / "JR1656_MHREF_SOURCE_TEMPLATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1656.csv",
        QUEUE / "JR1656_NEXT_TARGET_NONCLAIM.csv",
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
        "domain_claim_ready",
        "prediction_ready",
        "score_allowed",
        "score_ready",
        "source_ready",
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
    rows: list[dict[str, object]] = []
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
                "role": "1656 local domain selector for nabla_Ploc/M_H_ref source acquisition",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1656_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1656_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1656_2_queue", QUEUE, "nonclaim_acquisition_queue"),
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


def domain_candidate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DOM1656_0_lab_R10",
            "compact lab/R10 finite-range source-test domain",
            "SELECT_FOR_ACQUISITION",
            "finite local tube, direct short-range arena, independent apparatus geometry, no orbital GM needed for first acquisition template",
            "MISSING_SOURCE_PROFILE;MISSING_FERMI_DOMAIN;MISSING_CURVATURE_NORMS;MISSING_MHREF_DENOMINATOR",
        ),
        (
            "DOM1656_1_solar_system_PPN",
            "solar-system weak-field exterior domain",
            "DEFER",
            "excellent PPN relevance but source mass is easily contaminated by orbital-GM calibration",
            "NO_ORBITAL_GM_IMPORT;MISSING_PARENT_MHREF;MISSING_DOMAIN_BOUNDARY_LOCK",
        ),
        (
            "DOM1656_2_clock_WEP",
            "local clock/material-species domain",
            "DEFER",
            "good readout/coupling relevance but species response introduces extra matter/EM coefficients before projector row is filled",
            "MISSING_READOUT_RESPONSE;MISSING_SPECIES_CHARGE;MISSING_PARENT_DOMAIN",
        ),
        (
            "DOM1656_3_orbital_sources",
            "orbital/binary source-normalization domain",
            "REJECT_FOR_FIRST_ROW",
            "too close to forbidden orbital-GM denominator shortcut",
            "NO_ORBITAL_GM_IMPORT",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "domain_id": domain_id,
            "physical_domain": physical_domain,
            "selection": selection,
            "reason": reason,
            "blockers": blockers,
            "selected_for_acquisition": selection == "SELECT_FOR_ACQUISITION",
            "domain_claim_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for domain_id, physical_domain, selection, reason, blockers in rows
    ]


def selected_domain_rows() -> list[dict[str, object]]:
    rows = [
        ("LDR1656_0_domain_id", "domain_id", "lab_R10_compact_fermi_tube", "fixed label for first local finite-domain acquisition", "CHOSEN_TEMPLATE_LABEL"),
        ("LDR1656_1_physical_system", "physical_system", "short-range laboratory source/test apparatus exterior tube", "matches R10/local finite-source arena without orbital-GM import", "SOURCE_DETAILS_MISSING"),
        ("LDR1656_2_LD", "L_D", "MISSING_VALUE_METERS", "tube radius/diameter scale entering finite-domain Fermi bound", "MISSING_NUMERIC_SOURCE"),
        ("LDR1656_3_boundary_rule", "boundary_rule", "compact tube with source support excised and fixed support weight", "needed to keep boundary/domain motion explicit", "MISSING_PARENT_OR_APPARATUS_SOURCE"),
        ("LDR1656_4_curvature", "Riemann_norm;nabla_Riemann_norm", "MISSING_VALUES_IN_m^-2_AND_m^-3", "fills nabla_Ploc Fermi-curvature row", "MISSING_CURVATURE_SOURCE"),
        ("LDR1656_5_frame", "central_worldline;transport_rule", "free-fall/Fermi-Walker idealization or non-geodesic lab correction", "decides whether acceleration/rotation terms enter", "MISSING_FRAME_SOURCE"),
        ("LDR1656_6_mhref", "M_H_ref", "MISSING_HAMILTONIAN_DENOMINATOR", "normalizes projector/source leakage without orbital GM", "MISSING_HTAU_HREF_PARENT_ROW"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "field": field,
            "selected_requirement": selected_requirement,
            "why_needed": why_needed,
            "status": status,
            "source_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for requirement_id, field, selected_requirement, why_needed, status in rows
    ]


def unit_convention_rows() -> list[dict[str, object]]:
    rows = [
        ("UNIT1656_0_length", "L_D", "meter", "SI length for local tube size", "numeric value required"),
        ("UNIT1656_1_curvature", "Riemann_norm", "meter^-2", "curvature norm in local domain", "numeric value required"),
        ("UNIT1656_2_curvature_derivative", "nabla_Riemann_norm", "meter^-3", "first curvature derivative norm", "numeric value required"),
        ("UNIT1656_3_projector_gradient", "nabla_Ploc_Linf", "meter^-1", "finite-domain projector drift bound", "computed only after lower inputs"),
        ("UNIT1656_4_mass_denominator", "M_H_ref", "kg or J/c^2 with explicit conversion", "same-frame Hamiltonian source mass denominator", "must not be orbital GM"),
        ("UNIT1656_5_joined_bound", "B_obs_projector_source_over_MH", "dimensionless", "all local source/projector residuals normalized by M_H_ref", "requires no-cancellation components"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "unit_id": unit_id,
            "quantity": quantity,
            "unit": unit,
            "role": role,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for unit_id, quantity, unit, role, status in rows
    ]


def nablaploc_template_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPLT1656_0_lab_R10_fermi_candidate",
            "domain_id": "lab_R10_compact_fermi_tube",
            "formula": "nabla_Ploc_Linf <= C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + non_geodesic_terms",
            "L_D_m": "MISSING",
            "Riemann_norm_m2": "MISSING",
            "nabla_Riemann_norm_m3": "MISSING",
            "C_Fermi": "MISSING",
            "C_Fermi2": "MISSING",
            "acceleration_rotation_terms": "MISSING_OR_DECLARED_ZERO_WITH_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "DOMAIN_SELECTED_VALUES_MISSING",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def mhref_template_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHRT1656_0_lab_R10_same_frame_candidate",
            "domain_id": "lab_R10_compact_fermi_tube",
            "definition": "M_H_ref = H_tau[S_outer] - H_ref",
            "allowed_source_mass_proxy": "ordinary apparatus/source mass may be recorded only as an input to be matched to H_tau, not as proof of M_H_ref",
            "forbidden_source_mass_proxy": "orbital GM or post-fit Newtonian source mass",
            "H_tau": "MISSING",
            "H_ref": "MISSING",
            "M_H_ref": "MISSING",
            "units": "kg_or_J_over_c2",
            "reference_rule": "MISSING_FIXED_REFERENCE_RULE",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "DENOMINATOR_DOMAIN_SELECTED_VALUES_MISSING",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1656_0_domain_selection", "lab_R10 compact Fermi tube", "SELECTED_FOR_ACQUISITION_NOT_CLAIM", "domain chosen only as first source-row target; no parent domain theorem"),
        ("RUN1656_1_nabla_Ploc", "nabla_Ploc_Linf row", "REFUSE_SCORING", "MISSING_LD;MISSING_CURVATURE_NORMS;MISSING_CONSTANTS;MISSING_SOURCE_PATH"),
        ("RUN1656_2_MHref", "M_H_ref denominator row", "REFUSE_SCORING", "MISSING_HTAU;MISSING_HREF;MISSING_REFERENCE_RULE;MISSING_PARENT_CURRENT;NO_ORBITAL_GM_IMPORT"),
        ("RUN1656_3_joined_local", "local_GR_Newton_PPN_R10_WEP", "REFUSE_SCORING", "DOMAIN_SELECTED_ONLY;NABLAPLOC_VALUES_MISSING;MHREF_MISSING;NO_LOCAL_CLAIM"),
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
        ("CG1656_0_domain", "lab_R10 compact Fermi tube is selected for acquisition", "INTERNAL_SELECTION_ONLY", "NONCLAIM", "selection is not a domain theorem"),
        ("CG1656_1_nabla_Ploc", "nabla_Ploc bound row is source-backed", False, "BLOCKED", "values and source path missing"),
        ("CG1656_2_MHref", "M_H_ref denominator is source-backed", False, "BLOCKED", "Hamiltonian charge/reference row missing"),
        ("CG1656_3_local_GR", "local GR/Newton/PPN/R10/WEP follows from 1656", False, "NO_CLAIM", "1656 chooses an acquisition domain only"),
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
        ("DEC1656_0_select_lab_R10", "SELECT_LAB_R10_COMPACT_FERMI_TUBE_FOR_ACQUISITION", "it is the cleanest finite local domain for the first nabla_Ploc source row and avoids orbital-GM as first denominator input", "build a lab_R10 source pack for L_D, curvature norms, frame terms, and M_H_ref requirements"),
        ("DEC1656_1_defer_solar", "DEFER_SOLAR_SYSTEM_PPN_DOMAIN", "high value but too easy to contaminate the denominator with orbital GM", "return after M_H_ref discipline is source-backed"),
        ("DEC1656_2_unit_convention", "USE_SI_LENGTH_AND_MASS_WITH_DIMENSIONLESS_JOINED_BOUND", "keeps nabla_Ploc in m^-1 and normalized leakage dimensionless", "future data rows must declare conversions and no-cancellation normalization"),
        ("DEC1656_3_next", "NEXT_1657_LAB_R10_SOURCE_PACK", "selected domain now needs actual sourced lower inputs", "create lab_R10 finite-domain source pack for L_D/curvature/frame/M_H_ref"),
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
            "next_target": "1657-Y5-R2FR-lab-R10-nablaPloc-MHref-source-pack.md",
            "script": "scripts/Y5_R2FR_lab_R10_nablaPloc_MHref_source_pack.py",
            "objective": "build the lab_R10 source pack for L_D, curvature norms, frame terms, projector constants, and same-frame M_H_ref requirements; no scoring unless real source-backed rows exist",
            "success_condition": "either a lab_R10 source row gets numeric source-backed fields without orbital-GM import, or every field remains explicit MISSING_* with valid_for_claim=false",
            "forbidden_shortcuts": "no orbital-GM denominator; no post-fit projector; no source-measure zero without owner proof; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, intake_rows, domain_candidates, selected_domain, unit_convention, nablaploc, mhref, refusal, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1656_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1656 source paths exist and needles are present"),
        ("VAL1656_1_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1656_2_domain_selected", any(row["domain_id"] == "DOM1656_0_lab_R10" and row["selected_for_acquisition"] is True for row in domain_candidates), "lab_R10 compact Fermi tube selected for acquisition"),
        ("VAL1656_3_selected_requirements_complete", len(selected_domain) == 7 and any(row["field"] == "M_H_ref" for row in selected_domain), "selected domain requirements include geometry and M_H_ref fields"),
        ("VAL1656_4_unit_convention_complete", len(unit_convention) == 6 and any(row["quantity"] == "nabla_Ploc_Linf" and row["unit"] == "meter^-1" for row in unit_convention), "unit convention fixes nabla_Ploc and normalized bound units"),
        ("VAL1656_5_templates_nonclaim", nablaploc[0]["current_status"] == "DOMAIN_SELECTED_VALUES_MISSING" and mhref[0]["current_status"] == "DENOMINATOR_DOMAIN_SELECTED_VALUES_MISSING", "source templates are selected but remain value-missing"),
        ("VAL1656_6_refusal_runner_blocks", len(refusal) == 4 and any(row["runner_decision"] == "REFUSE_SCORING" for row in refusal), "refusal runner blocks scoring"),
        ("VAL1656_7_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1656_8_next_target_selected", next_targets[0]["next_target"] == "1657-Y5-R2FR-lab-R10-nablaPloc-MHref-source-pack.md", "next target selects lab_R10 source pack"),
        ("VAL1656_9_csv_parse", generated_csv_parse, "all generated 1656 CSVs parse"),
        ("VAL1656_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1656 generated rows keep MTS claim/no-score flags false"),
        ("VAL1656_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1656_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1656_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1656_14_formalization_untouched", not formalization_dirty, "no 1656 outputs found under formalization-workbench"),
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
            "check_id": "VAL1656_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1656 local domain selector for nabla_Ploc/M_H_ref source acquisition validation",
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


def write_doc(source_rows, intake_rows, domain_candidates, selected_domain, unit_convention, nablaploc, mhref, refusal, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1656 - Local Domain Selector For nablaPloc MHref Source Acquisition

**Private status:** nonclaim domain-selection checkpoint. No local domain theorem, `nabla_Ploc` bound, `M_H_ref`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`1656` selects the first acquisition domain, not a proof domain:

```text
selected domain: lab_R10_compact_fermi_tube
||nabla P_loc|| <= C_Fermi L_D ||Riemann|| + C_Fermi2 L_D^2 ||nabla Riemann|| + non-geodesic lab terms
M_H_ref = H_tau[S_outer] - H_ref
```

The lab/R10 compact Fermi tube is selected because it is the cleanest finite local arena for the first `nabla_Ploc` source row and avoids using orbital `GM` as the first denominator. Solar-system PPN is deferred because it is too easy to smuggle orbital calibration into `M_H_ref`; clocks/WEP are deferred because readout/species responses add extra coupling coefficients first.

This is not a pass. The selected domain still lacks `L_D`, curvature norms, frame/acceleration terms, source profile, and the same-frame Hamiltonian denominator. It is just the first disciplined ring to fight in.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## Domain Candidate Selector

{markdown_table(domain_candidates, ["domain_id", "physical_domain", "selection", "reason", "blockers"])}

## Selected Domain Requirements

{markdown_table(selected_domain, ["requirement_id", "field", "selected_requirement", "why_needed", "status"])}

## Unit Convention

{markdown_table(unit_convention, ["unit_id", "quantity", "unit", "role", "status"])}

## nablaPloc Source Template

{markdown_table(nablaploc, ["row_id", "domain_id", "formula", "L_D_m", "Riemann_norm_m2", "nabla_Riemann_norm_m3", "current_status"])}

## MHref Source Template

{markdown_table(mhref, ["row_id", "domain_id", "definition", "allowed_source_mass_proxy", "forbidden_source_mass_proxy", "current_status"])}

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

The local branch now has a concrete first empirical target: a lab/R10 compact Fermi tube source pack. If that pack can source `L_D`, curvature/frame terms, and a noncircular `M_H_ref`, we can finally start testing whether the projector leakage is small rather than merely assumed zero.
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
    intake_rows = intake_scan_rows()
    domain_candidates = domain_candidate_rows()
    selected_domain = selected_domain_rows()
    unit_convention = unit_convention_rows()
    nablaploc = nablaploc_template_rows()
    mhref = mhref_template_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (INTAKE_SCAN, intake_rows),
        (DOMAIN_CANDIDATES, domain_candidates),
        (SELECTED_DOMAIN, selected_domain),
        (UNIT_CONVENTION, unit_convention),
        (NABLAPLOC_TEMPLATE, nablaploc),
        (MHREF_TEMPLATE, mhref),
        (REFUSAL_RUNNER, refusal),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, intake_rows, domain_candidates, selected_domain, unit_convention, nablaploc, mhref, refusal, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, intake_rows, domain_candidates, selected_domain, unit_convention, nablaploc, mhref, refusal, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1656 validation failed; see P8_Y5_BRR545_1656_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1656 validation PASS")


if __name__ == "__main__":
    main()
