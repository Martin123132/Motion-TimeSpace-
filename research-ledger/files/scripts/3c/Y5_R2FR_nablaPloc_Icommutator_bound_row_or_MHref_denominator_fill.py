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
QUARANTINE = MICROSCOPE / "quarantine" / "1655"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1655-Y5-R2FR-nablaPloc-Icommutator-bound-row-or-MHref-denominator-fill.md"

SOURCE_FILES = {
    "1654_doc": ROOT / "1654-Y5-R2FR-PiM-Ploc-commutator-owner-or-first-strict-source-row-fill.md",
    "1654_validation": OUT / "P8_Y5_BRR545_1654_VALIDATION.csv",
    "1654_next": OUT / "P8_Y5_PARENT_QLOC_1654_NEXT_TARGET.csv",
    "1654_commutator": OUT / "P8_Y5_PARENT_QLOC_1654_PROJECTOR_COMMUTATOR_DERIVATION.csv",
    "1654_owner_gate": OUT / "P8_Y5_PARENT_QLOC_1654_PIM_PLOC_OWNER_GATE.csv",
    "1654_bound_ledger": OUT / "P8_Y5_PARENT_QLOC_1654_PROJECTOR_BOUND_FORMULA_LEDGER.csv",
    "1654_first_fill": OUT / "P8_Y5_PARENT_QLOC_1654_FIRST_STRICT_SOURCE_ROW_FILL_RUNNER.csv",
    "1654_refusal": OUT / "P8_Y5_PARENT_QLOC_1654_COMMUTATOR_FIRST_ROW_REFUSAL_RUNNER.csv",
    "1653_first_rows": OUT / "P8_Y5_PARENT_QLOC_1653_FIRST_SOURCE_ROW_LEDGER.csv",
    "1652_mhref_gate": OUT / "P8_Y5_PARENT_QLOC_1652_MHREF_FIRST_ROW_GATE.csv",
    "1645_mhref_schema": OUT / "P8_Y5_PARENT_QLOC_1645_MHREF_SOURCE_ROW_SCHEMA.csv",
    "nablaploc_row": OUT / "P8_Y5_R10_1208_SOURCE_READY_NABLAPLOC_ROW.csv",
    "nablaploc_law": OUT / "P8_Y5_R10_1208_NABLAPLOC_BOUND_LAW.csv",
    "ploc_derivation": OUT / "P8_Y5_R10_1283_PLOC_PROJECTOR_OWNER_DERIVATION.csv",
    "projector_rows": OUT / "P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
    "projector_pack": OUT / "P8_Y5_R10_914_PROJECTOR_SOURCE_BOUND_PACK.csv",
    "stress_vector": OUT / "P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv",
    "queue_1654_bound": QUEUE / "JR1654_PROJECTOR_BOUND_FORMULA_LEDGER_NONCLAIM.csv",
    "queue_1654_fill": QUEUE / "JR1654_FIRST_STRICT_SOURCE_ROW_FILL_RUNNER_NONCLAIM.csv",
}

NEEDLES = {
    "1654_doc": ["nabla P_loc", "I_commutator"],
    "1654_validation": ["VAL1654_OVERALL", "PASS"],
    "1654_next": ["1655-Y5-R2FR-nablaPloc-Icommutator-bound-row-or-MHref-denominator-fill.md", "nabla_Ploc or I_commutator"],
    "1654_commutator": ["PCD1654_0_product_rule", "PCD1654_5_verdict"],
    "1654_owner_gate": ["POG1654_5_MHref_join", "BLOCKED_BY_MHREF"],
    "1654_bound_ledger": ["PBL1654_1_nabla_Ploc", "PBL1654_0_I_commutator"],
    "1654_first_fill": ["FRF1654_3_nabla_Ploc_bound", "NO_FILL_ACCEPTED_STRICT_TEMPLATE_ONLY"],
    "1654_refusal": ["RUN1654_1_commutator_bound", "REFUSE_SCORING"],
    "1653_first_rows": ["FSR1653_1_MHref_source_row", "FSR1653_3_Bobs_numeric_bound"],
    "1652_mhref_gate": ["MHG1652_7_first_row_verdict", "FIRST_ROW_NOT_ACCEPTED"],
    "1645_mhref_schema": ["MHS1645_0_M_H_ref", "MISSING_STABLE_MH_REF"],
    "nablaploc_row": ["SRN1208_2_fermi_curvature_row", "BEST_SOURCE_ROW_FOR_NEXT_RUN_NONCLAIM"],
    "nablaploc_law": ["NPL1208_2_fermi_curvature_bound", "BEST_NUMERIC_ROUTE_SOURCE_READY_NOT_CLAIM"],
    "ploc_derivation": ["POD1283_2_finite_domain_bound", "BOUND_LAW_DERIVED_NUMERIC_INPUTS_MISSING"],
    "projector_rows": ["PSR913_4_projector_commutator", "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL"],
    "projector_pack": ["PSB914_4_I_commutator", "MISSING_CHAIN_MAP_DOMAIN_PROOF"],
    "stress_vector": ["TPS660_0_commutator_integral", "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL"],
    "queue_1654_bound": ["PBL1654_1_nabla_Ploc", "PBL1654_0_I_commutator"],
    "queue_1654_fill": ["FRF1654_3_nabla_Ploc_bound", "NO_FILL_ACCEPTED_STRICT_TEMPLATE_ONLY"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1655_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1655_INTAKE_SCAN.csv"
ROW_READINESS = OUT / "P8_Y5_PARENT_QLOC_1655_BOUND_ROW_READINESS_MATRIX.csv"
NABLAPLOC_ROW = OUT / "P8_Y5_PARENT_QLOC_1655_NABLAPLOC_CANDIDATE_ROW.csv"
ICOMM_ROW = OUT / "P8_Y5_PARENT_QLOC_1655_ICOMMUTATOR_CANDIDATE_ROW.csv"
MHREF_ROW = OUT / "P8_Y5_PARENT_QLOC_1655_MHREF_DENOMINATOR_CANDIDATE_ROW.csv"
JOINED_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1655_JOINED_BOUND_ROW_RUNNER.csv"
ACQUISITION_QUEUE = OUT / "P8_Y5_PARENT_QLOC_1655_ACQUISITION_QUEUE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1655_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1655_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1655_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1655_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    INTAKE_SCAN,
    ROW_READINESS,
    NABLAPLOC_ROW,
    ICOMM_ROW,
    MHREF_ROW,
    JOINED_RUNNER,
    ACQUISITION_QUEUE,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    ROW_READINESS,
    NABLAPLOC_ROW,
    ICOMM_ROW,
    MHREF_ROW,
    JOINED_RUNNER,
    ACQUISITION_QUEUE,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    ROW_READINESS: [
        QUARANTINE / "BOUND_ROW_READINESS_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_bound_row_readiness_matrix_nonclaim_1655.csv",
        QUEUE / "JR1655_BOUND_ROW_READINESS_MATRIX_NONCLAIM.csv",
    ],
    NABLAPLOC_ROW: [
        QUARANTINE / "NABLAPLOC_CANDIDATE_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_nablaPloc_candidate_row_nonclaim_1655.csv",
        QUEUE / "JR1655_NABLAPLOC_CANDIDATE_ROW_NONCLAIM.csv",
    ],
    ICOMM_ROW: [
        QUARANTINE / "ICOMMUTATOR_CANDIDATE_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Icommutator_candidate_row_nonclaim_1655.csv",
        QUEUE / "JR1655_ICOMMUTATOR_CANDIDATE_ROW_NONCLAIM.csv",
    ],
    MHREF_ROW: [
        QUARANTINE / "MHREF_DENOMINATOR_CANDIDATE_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_MHref_denominator_candidate_row_nonclaim_1655.csv",
        QUEUE / "JR1655_MHREF_DENOMINATOR_CANDIDATE_ROW_NONCLAIM.csv",
    ],
    ACQUISITION_QUEUE: [
        QUARANTINE / "ACQUISITION_QUEUE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_acquisition_queue_nonclaim_1655.csv",
        QUEUE / "JR1655_ACQUISITION_QUEUE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1655.csv",
        QUEUE / "JR1655_NEXT_TARGET_NONCLAIM.csv",
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
        "first_row_ready",
        "numeric_ready",
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
                "role": "1655 nabla_Ploc/I_commutator bound row or M_H_ref denominator fill",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1655_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1655_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1655_2_queue", QUEUE, "nonclaim_acquisition_queue"),
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


def readiness_rows() -> list[dict[str, object]]:
    rows = [
        ("READY1655_0_nabla_Ploc", "nabla_Ploc_Linf", "closest_to_fill", "formula source-ready from 1208/1283", "MISSING_DOMAIN;MISSING_LD;MISSING_CURVATURE_NORMS;MISSING_CONSTANTS;MISSING_SOURCE_PATH;MISSING_MHREF_JOIN"),
        ("READY1655_1_I_commutator", "I_commutator", "harder_owner_or_integral", "requires Pi_M chain-map zero or sourced commutator integral", "MISSING_CHAIN_MAP;MISSING_HILBERT_CURRENT_DOMAIN;MISSING_INTEGRAL;MISSING_MHREF"),
        ("READY1655_2_MHref", "M_H_ref", "hard_denominator", "needed by every normalized bound", "MISSING_HTAU;MISSING_HREF;MISSING_PARENT_CURRENT;MISSING_INTEGRABILITY;MISSING_POSITIVITY;NO_ORBITAL_GM_IMPORT"),
        ("READY1655_3_joined_total", "B_obs_projector_source_over_MH", "not_ready", "requires all numerator rows plus same-frame denominator and no-cancellation vector", "MISSING_COMPONENT_ROWS;MISSING_COEFFICIENTS;MISSING_MHREF;MISSING_UNITS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ready_id": ready_id,
            "quantity": quantity,
            "priority": priority,
            "why": why,
            "missing_fields": missing_fields,
            "numeric_ready": False,
            "first_row_ready": False,
            "valid_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ready_id, quantity, priority, why, missing_fields in rows
    ]


def nablaploc_candidate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPLR1655_0_fermi_curvature_candidate",
            "quantity": "nabla_Ploc_Linf",
            "domain_id": "MISSING_LOCAL_FERMI_DOMAIN",
            "norm_id": "MISSING_WEIGHTED_LINF_NORM",
            "formula": "C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm",
            "L_D": "MISSING",
            "Riemann_norm": "MISSING",
            "nabla_Riemann_norm": "MISSING",
            "C_Fermi": "MISSING",
            "C_Fermi2": "MISSING",
            "numeric_value": "MISSING",
            "units": "1/length",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "accepted_for_scoring": False,
            "numeric_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def icommutator_candidate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ICR1655_0_commutator_integral_candidate",
            "quantity": "I_commutator",
            "definition": "abs(integral_A [d,Pi_M]J_H)/M_H_ref",
            "annulus_or_domain": "MISSING_COMPACT_EXTERIOR_ANNULUS",
            "Pi_M_owner": "MISSING_CHAIN_MAP_OWNER",
            "J_H_domain": "MISSING_HILBERT_SOURCE_CURRENT_DOMAIN",
            "integral_value": "MISSING",
            "M_H_ref": "MISSING",
            "units": "dimensionless_after_M_H_ref_or_mass_flux_units",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL",
            "accepted_for_scoring": False,
            "numeric_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def mhref_candidate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR1655_0_same_frame_denominator_candidate",
            "quantity": "M_H_ref",
            "definition": "H_tau[S_outer] - H_ref",
            "tau_id": "MISSING_TAU_SOURCE",
            "surface_outer": "MISSING_SURFACE_OUTER",
            "H_tau": "MISSING",
            "H_ref": "MISSING",
            "M_H_ref": "MISSING",
            "units": "mass_or_energy_over_c2_equivalent",
            "reference_rule": "MISSING_FIXED_REFERENCE_RULE",
            "integrability_status": "MISSING_INTEGRABILITY",
            "positivity_status": "MISSING_POSITIVE_FINITE_PROOF",
            "source_path": "MISSING_SOURCE_PATH",
            "forbidden_substitution": "NO_ORBITAL_GM_IMPORT",
            "current_status": "MISSING_STABLE_MH_REF",
            "accepted_for_scoring": False,
            "numeric_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def joined_runner_rows() -> list[dict[str, object]]:
    rows = [
        ("JBR1655_0_nabla_only", "nabla_Ploc row without M_H_ref", "REFUSE", "cannot normalize projector/source leakage without denominator"),
        ("JBR1655_1_Icomm_only", "I_commutator row without M_H_ref", "REFUSE", "commutator integral is not dimensionless/scoreable without same-frame denominator"),
        ("JBR1655_2_MHref_only", "M_H_ref row without numerator rows", "REFUSE_LOCAL_SCORING", "denominator alone does not prove local-GR recovery"),
        ("JBR1655_3_joined_no_cancellation", "nabla_Ploc + I_commutator + B_P_flux + M_H_ref", "FUTURE_ACCEPTABLE_ROUTE", "requires sourced units, coefficients, no-cancellation vector, and valid_for_claim true on every component"),
        ("JBR1655_4_current_state", "current 1655 rows", "REFUSE_SCORING", "all candidates remain missing numeric/source fields"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": run_id,
            "case": case,
            "runner_decision": decision,
            "reason": reason,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for run_id, case, decision, reason in rows
    ]


def acquisition_rows() -> list[dict[str, object]]:
    rows = [
        ("ACQ1655_0_choose_local_domain", "domain_id;physical_system;L_D;boundary_rule;source_path", "needed before any finite-domain nabla_Ploc bound", "highest"),
        ("ACQ1655_1_curvature_norms", "Riemann_norm;nabla_Riemann_norm;units;source_path", "fills the closest source-ready row from 1208", "highest"),
        ("ACQ1655_2_projector_constants", "C_Fermi;C_Fermi2;remainder_control;source_path", "turns the symbolic bound into a numeric upper bound", "high"),
        ("ACQ1655_3_MHref_denominator", "H_tau;H_ref;M_H_ref;units;reference_rule;source_path", "normalizes every local source/projector bound", "highest"),
        ("ACQ1655_4_Icommutator_or_zero", "Pi_M_chain_map_proof or I_commutator integral;units;source_path", "closes or bounds mass-current commutator leakage", "medium"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "needed_fields": needed_fields,
            "why_needed": why_needed,
            "priority": priority,
            "status": "SOURCE_INPUT_REQUIRED",
            "accepted_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, needed_fields, why_needed, priority in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1655_0_nabla_Ploc", "nabla_Ploc bound row is numeric/source-backed", False, "BLOCKED", "finite-domain values and source path missing"),
        ("CG1655_1_Icommutator", "I_commutator zero or numeric bound is source-backed", False, "BLOCKED", "chain-map proof or integral missing"),
        ("CG1655_2_MHref", "M_H_ref denominator row is accepted", False, "BLOCKED", "H_tau/H_ref/source path and parent current missing"),
        ("CG1655_3_joined_bound", "joined no-cancellation local source/projector bound is scoreable", False, "BLOCKED", "component rows and denominator missing"),
        ("CG1655_4_local_GR", "local GR/Newton/PPN/R10/WEP follows from 1655", False, "NO_CLAIM", "1655 is data/source-row plumbing only"),
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
        ("DEC1655_0_best_row", "NABLAPLOC_BOUND_ROW_IS_CLOSEST", "the 1208/1283 law already supplies a formula and units; only finite-domain values/source path are missing", "prioritize a physical local domain and curvature data"),
        ("DEC1655_1_MHref", "MHREF_REMAINS_GLOBAL_DENOMINATOR_BLOCKER", "all normalized projector/source rows still need H_tau-H_ref", "keep M_H_ref acquisition tied to any local-data pass"),
        ("DEC1655_2_Icommutator", "ICOMMUTATOR_REMAINS_OWNER_OR_INTEGRAL_BLOCKER", "without Pi_M chain-map proof, the commutator needs a sourced integral", "do not claim source-measure zero"),
        ("DEC1655_3_next", "NEXT_1656_LOCAL_DOMAIN_SELECTOR", "a numeric row needs a named local domain before data can be sourced", "select local source/domain and unit convention for nabla_Ploc/MHref acquisition"),
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
            "next_target": "1656-Y5-R2FR-local-domain-selector-for-nablaPloc-MHref-source-acquisition.md",
            "script": "scripts/Y5_R2FR_local_domain_selector_for_nablaPloc_MHref_source_acquisition.py",
            "objective": "select the first physical local source/domain and unit convention for nabla_Ploc and M_H_ref source acquisition, without using orbital-GM as the denominator",
            "success_condition": "one local domain has explicit L_D/curvature/source requirements and M_H_ref normalization requirements, or all candidate domains are refused with exact blockers",
            "forbidden_shortcuts": "no orbital-GM denominator; no post-fit projector; no source-measure zero without owner proof; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, intake_rows, readiness, nablaploc, icomm, mhref, joined, acquisition, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1655_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1655 source paths exist and needles are present"),
        ("VAL1655_1_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1655_2_readiness_ranked", readiness[0]["quantity"] == "nabla_Ploc_Linf" and readiness[0]["priority"] == "closest_to_fill", "nabla_Ploc finite-domain row is ranked closest to fill"),
        ("VAL1655_3_nabla_row_nonclaim", nablaploc[0]["current_status"] == "SOURCE_READY_VALUES_MISSING" and nablaploc[0]["valid_for_claim"] is False, "nabla_Ploc candidate row remains nonclaim"),
        ("VAL1655_4_icomm_row_nonclaim", icomm[0]["current_status"] == "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL" and icomm[0]["valid_for_claim"] is False, "I_commutator candidate row remains nonclaim"),
        ("VAL1655_5_mhref_row_nonclaim", mhref[0]["current_status"] == "MISSING_STABLE_MH_REF" and mhref[0]["valid_for_claim"] is False, "M_H_ref candidate row remains nonclaim"),
        ("VAL1655_6_joined_runner_blocks", any(row["runner_decision"] == "REFUSE_SCORING" for row in joined), "joined runner refuses current scoring"),
        ("VAL1655_7_acquisition_queue_ready", len(acquisition) == 5 and acquisition[0]["priority"] == "highest", "source acquisition queue is explicit"),
        ("VAL1655_8_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1655_9_next_target_selected", next_targets[0]["next_target"] == "1656-Y5-R2FR-local-domain-selector-for-nablaPloc-MHref-source-acquisition.md", "next target selects local domain/source acquisition"),
        ("VAL1655_10_csv_parse", generated_csv_parse, "all generated 1655 CSVs parse"),
        ("VAL1655_11_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1655 generated rows keep MTS claim/no-score flags false"),
        ("VAL1655_12_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1655_13_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1655_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1655_15_formalization_untouched", not formalization_dirty, "no 1655 outputs found under formalization-workbench"),
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
            "check_id": "VAL1655_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1655 nabla_Ploc/I_commutator bound row or M_H_ref denominator fill validation",
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


def write_doc(source_rows, intake_rows, readiness, nablaploc, icomm, mhref, joined, acquisition, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1655 - nablaPloc Icommutator Bound Row Or MHref Denominator Fill

**Private status:** nonclaim source-row acquisition checkpoint. No `nabla_Ploc` bound, `I_commutator` bound, `M_H_ref`, joined local projector/source bound, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

`1655` tries to fill the first actual bound row after the commutator split:

```text
||nabla P_loc|| <= C_Fermi L_D ||Riemann|| + C_Fermi2 L_D^2 ||nabla Riemann||
I_commutator = |integral_A [d,Pi_M]J_H| / M_H_ref
M_H_ref = H_tau[S_outer] - H_ref
```

No row is accepted yet. The closest-to-fill row is `nabla_Ploc_Linf` because the formula and units already exist in the `1208/1283` chain; it needs a chosen local domain, curvature norms, constants, and a source path. `I_commutator` is harder because it still needs a `Pi_M` chain-map theorem or a sourced commutator integral. `M_H_ref` remains the denominator blocker because it needs `H_tau`, `H_ref`, integrability, positivity, and no orbital-`GM` import.

The useful result is a narrower data plan: pick a physical local domain first, then acquire `L_D`, curvature/norm data, and the same-frame denominator requirements.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## Bound Row Readiness Matrix

{markdown_table(readiness, ["ready_id", "quantity", "priority", "why", "missing_fields"])}

## nablaPloc Candidate Row

{markdown_table(nablaploc, ["row_id", "quantity", "formula", "L_D", "Riemann_norm", "nabla_Riemann_norm", "current_status"])}

## Icommutator Candidate Row

{markdown_table(icomm, ["row_id", "quantity", "definition", "Pi_M_owner", "integral_value", "M_H_ref", "current_status"])}

## MHref Denominator Candidate Row

{markdown_table(mhref, ["row_id", "quantity", "definition", "H_tau", "H_ref", "M_H_ref", "current_status"])}

## Joined Bound Runner

{markdown_table(joined, ["run_id", "case", "runner_decision", "reason"])}

## Acquisition Queue

{markdown_table(acquisition, ["acquisition_id", "needed_fields", "why_needed", "priority", "status"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is the bridge from derivation discipline into empirical plumbing. The most economical next test is not a full local-GR score; it is choosing a concrete local domain and seeing whether the finite-domain projector drift can be bounded with real source-backed numbers while the Hamiltonian denominator is kept noncircular.
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
    readiness = readiness_rows()
    nablaploc = nablaploc_candidate_rows()
    icomm = icommutator_candidate_rows()
    mhref = mhref_candidate_rows()
    joined = joined_runner_rows()
    acquisition = acquisition_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (INTAKE_SCAN, intake_rows),
        (ROW_READINESS, readiness),
        (NABLAPLOC_ROW, nablaploc),
        (ICOMM_ROW, icomm),
        (MHREF_ROW, mhref),
        (JOINED_RUNNER, joined),
        (ACQUISITION_QUEUE, acquisition),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, intake_rows, readiness, nablaploc, icomm, mhref, joined, acquisition, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, intake_rows, readiness, nablaploc, icomm, mhref, joined, acquisition, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1655 validation failed; see P8_Y5_BRR545_1655_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1655 validation PASS")


if __name__ == "__main__":
    main()
