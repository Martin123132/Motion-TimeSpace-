from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1697"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_SOURCE = MICROSCOPE / "branch_locked_wep" / "source"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1697-Y5-R2FR-owner-axiom-candidate-and-WEP-readout-source-pack.md"

SOURCE_FILES = {
    "1696_doc": ROOT / "1696-Y5-R2FR-parent-object-language-owner-or-tau-min-current-branch.md",
    "1696_validation": OUT / "P8_Y5_BRR545_1696_VALIDATION.csv",
    "1696_owner_stack": OUT / "P8_Y5_PARENT_QLOC_1696_PARENT_OBJECT_LANGUAGE_OWNER_STACK.csv",
    "1696_tau_min": OUT / "P8_Y5_PARENT_QLOC_1696_TAU_MIN_LOWER_BOUND_GATE.csv",
    "1696_next": OUT / "P8_Y5_PARENT_QLOC_1696_NEXT_TARGET.csv",
    "1450_label_forgetting": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1452_measure_current": OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv",
    "1464_connected_category": OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv",
    "1478_action_line": MICROSCOPE / "quarantine" / "1478" / "SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT_NONCLAIM.csv",
    "1479_typing": MICROSCOPE / "quarantine" / "1479" / "NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT_NONCLAIM.csv",
    "1480_hom": MICROSCOPE / "quarantine" / "1480" / "COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT_NONCLAIM.csv",
    "1482_tau_readiness": OUT / "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv",
    "1084_readout": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1225_tau": OUT / "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
    "1482_parser": BRANCH_SOURCE / "P_WEP_R_source_status_1482.csv",
}

NEEDLES = {
    "1696_doc": ["NEXT1696_0_primary", "owner axiom candidate"],
    "1696_validation": ["VAL1696_OVERALL", "PASS"],
    "1696_owner_stack": ["OBJ1696_7_verdict", "PARENT_OBJECT_LANGUAGE_OWNER_NOT_DERIVED_TAU_MIN_ROUTE_RETAINED"],
    "1696_tau_min": ["TAUMIN1696_8_verdict", "TAU_MIN_NOT_DERIVED_OR_SOURCED"],
    "1696_next": ["NEXT1696_0_primary", "WEP-readout-source-pack"],
    "1450_label_forgetting": ["HT1450_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1452_measure_current": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1464_connected_category": ["CON1464_5_verdict", "PROOF_NOT_CLOSED"],
    "1478_action_line": ["SAL1478_4_verdict", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"],
    "1479_typing": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    "1480_hom": ["CDH1480_5_verdict", "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED"],
    "1482_tau_readiness": ["TAU1482_0_formula", "MISSING_LIVE_READOUT_MATRIX"],
    "1084_readout": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1225_tau": ["TAU1225_6_verdict", "TAU_WEP_PROJECTION_NOT_DERIVED"],
    "1482_parser": ["ACCEPT1482_5_overall_parser_permission", "BLOCKED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1697_SOURCE_REGISTER.csv"
OWNER_AXIOM = OUT / "P8_Y5_PARENT_QLOC_1697_MINIMAL_OWNER_AXIOM_CANDIDATE.csv"
AXIOM_RISK = OUT / "P8_Y5_PARENT_QLOC_1697_AXIOM_RISK_AUDIT.csv"
WEB_SOURCES = OUT / "P8_Y5_PARENT_QLOC_1697_WEP_DATA_SOURCE_CANDIDATES.csv"
ACQUISITION_PACK = OUT / "P8_Y5_PARENT_QLOC_1697_WEP_TAU_MIN_ACQUISITION_PACK.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1697_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1697_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1697_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1697_VALIDATION.csv"

GENERATED = [SOURCE_REGISTER, OWNER_AXIOM, AXIOM_RISK, WEB_SOURCES, ACQUISITION_PACK, RUNNER, NEXT_TARGET, CLAIM_GATE]
CLAIM_CHECKED = [OWNER_AXIOM, AXIOM_RISK, WEB_SOURCES, ACQUISITION_PACK, RUNNER, NEXT_TARGET, CLAIM_GATE]

COPY_TARGETS = {
    OWNER_AXIOM: [
        QUARANTINE / "MINIMAL_OWNER_AXIOM_CANDIDATE.csv",
        BRANCH_RESIDUALS / "R2FR_minimal_owner_axiom_candidate_1697.csv",
        QUEUE / "JR1697_MINIMAL_OWNER_AXIOM_CANDIDATE.csv",
    ],
    WEB_SOURCES: [
        QUARANTINE / "WEP_DATA_SOURCE_CANDIDATES.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_data_source_candidates_1697.csv",
        QUEUE / "JR1697_WEP_DATA_SOURCE_CANDIDATES.csv",
    ],
    ACQUISITION_PACK: [
        QUARANTINE / "WEP_TAU_MIN_ACQUISITION_PACK.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_tau_min_acquisition_pack_1697.csv",
        QUEUE / "JR1697_WEP_TAU_MIN_ACQUISITION_PACK.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1697.csv",
        QUEUE / "JR1697_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1697": "owner axiom candidate and WEP tau_min acquisition pack",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def owner_axiom_rows() -> list[dict[str, object]]:
    rows = [
        (
            "AX1697_0_domain",
            "OrdinaryMatterObjectLanguage",
            "Arg(S_ord) := {e_obs(q), connection_obs(q), Psi_A, gauge/current fields, theta_A^rep, universal constants}",
            "candidate_parent_axiom",
            "source-only coefficient targets are absent from the parent domain",
        ),
        (
            "AX1697_1_no_source_prefactor",
            "NoSourceOnlyPrefactor",
            "Hom(species_label or hidden_marker, Coeff_active_source) = Const_common or 0",
            "candidate_parent_axiom",
            "forbids independent w_A, kappa_A, c_A, zeta_A as active-source multipliers",
        ),
        (
            "AX1697_2_single_action_line",
            "SingleActionDensityLine",
            "S_ord = integral dmu_parent L_ord(Psi_A, gauge, theta_A, e_obs)/hbar_parent with one measure/action scale",
            "candidate_parent_axiom",
            "collapses action weights to common calibration or measured matter parameters",
        ),
        (
            "AX1697_3_variation_before_readout",
            "VariationBeforeReadout",
            "T_H := delta S_ord/delta e_obs is formed before material, instrument, orbit, or readout selectors",
            "candidate_parent_axiom",
            "post-readout selectors cannot redefine the parent source",
        ),
        (
            "AX1697_4_connected_naturality",
            "ConnectedOrdinaryMatterNaturality",
            "source-relevant ordinary sectors form one parent-owned connected action-density/source-normalization graph",
            "candidate_parent_axiom",
            "natural scalar weights propagate to one common mode w_*",
        ),
        (
            "AX1697_5_no_reentry",
            "NoHiddenReadoutReentry",
            "effective action, boundary, measure, hidden invariant, and readout maps preserve source-coefficient exclusion",
            "candidate_parent_axiom",
            "prevents w_A from returning through hidden/source marker channels",
        ),
        (
            "AX1697_6_result_if_signed",
            "DeltaWZeroConsequence",
            "If AX1697_0 through AX1697_5 are parent-derived, then Delta_w_A=0 and beta_w,A=0 modulo common constant calibration",
            "conditional_consequence_not_claim",
            "would clear the source-weight leg of local GR/WEP branch",
        ),
        (
            "AX1697_7_verdict",
            "OwnerAxiomCandidateStatus",
            "This is a minimal axiom candidate, not a derived theorem in current MTS corpus",
            "OWNER_AXIOM_CANDIDATE_READY_NOT_DERIVED",
            "usable as a target for derivation; not usable as a physics claim",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "axiom_id": axiom_id,
            "clause": clause,
            "formal_statement": statement,
            "status": status,
            "effect_if_derived": effect,
            "parent_derived": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for axiom_id, clause, statement, status, effect in rows
    ]


def axiom_risk_rows() -> list[dict[str, object]]:
    rows = [
        ("RISK1697_0_axiom_smuggling", "axiom adopted instead of derived", "would be closure-only, not GR reduction", "derive from MTS quotient/category primitives or label as closure"),
        ("RISK1697_1_scalar_invariant", "hidden invariant feeds source coefficient", "reopens w_A through c(I_hid)", "prove trivial invariant algebra or forbidden target"),
        ("RISK1697_2_disconnected_matter", "ordinary matter graph decomposes", "independent component weights survive", "parent-owned connected graph certificate"),
        ("RISK1697_3_radiative_readout", "bare exclusion fails in effective/readout maps", "source weights re-enter after variation", "EFT/readout no-reentry theorem"),
        ("RISK1697_4_field_normalization", "field rescaling hides physical weight", "moves w_A into interactions or quantum measure", "interaction/measure owner proof"),
        ("RISK1697_5_verdict", "owner axiom risk status", "all risks remain open", "keep axiom nonclaim and keep finite tau route"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "risk_id": risk_id,
            "risk": risk,
            "failure_mode": failure_mode,
            "required_closure": closure,
            "risk_closed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for risk_id, risk, failure_mode, closure in rows
    ]


def web_source_rows() -> list[dict[str, object]]:
    rows = [
        (
            "WEB1697_0_final_result",
            "MICROSCOPE final WEP result",
            "https://arxiv.org/abs/2209.15487",
            "https://doi.org/10.1103/PhysRevLett.129.121102",
            "final eta_TiPt bound and mission result provenance",
            "source anchor only; no raw CMSM arrays",
            "source_candidate_recorded",
        ),
        (
            "WEB1697_1_ground_segment",
            "MICROSCOPE mission scenario, ground segment and data processing",
            "https://arxiv.org/abs/2201.10841",
            "https://doi.org/10.1088/1361-6382/ac4b9a",
            "data flow, CNES/ONERA/CMSM roles, sessions and processing context",
            "method/provenance source; not a machine-readable readout matrix",
            "source_candidate_recorded",
        ),
        (
            "WEB1697_2_HAL_ground_segment_pdf",
            "HAL PDF mirror for mission scenario/data processing",
            "https://hal.science/hal-03564498/document",
            "unknown",
            "open PDF source candidate for data-processing paper",
            "may need manual download/inspection; not an array source",
            "source_candidate_recorded",
        ),
        (
            "WEB1697_3_CNES_ONERA_CMSM_request",
            "CNES/ONERA/CMSM data request route",
            "not_found_as_public_machine_readable_URL_in_current_search",
            "not_applicable",
            "likely route for official CMSM/export arrays if public archive is unavailable",
            "requires manual contact/archive request before claim",
            "external_state_blocker_recorded",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "web_id": web_id,
            "source_name": source_name,
            "url": url,
            "doi_or_related": doi,
            "use_for": use_for,
            "claim_limit": limit,
            "status": status,
            "downloaded": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for web_id, source_name, url, doi, use_for, limit, status in rows
    ]


def acquisition_pack_rows() -> list[dict[str, object]]:
    rows = [
        ("ACQ1697_0_readout_matrix", "P_WEP_K_CMSM_readout.csv", "official CMSM/export arrays", "time;session_id;segment_id;gx;gz;Sxx;Sxz;masks;calibration_flags;attitude_orbit_convention;units", "CNES/ONERA/CMSM or validated exact equivalent", "missing"),
        ("ACQ1697_1_source_worldtube", "P_WEP_R_source_Earth_worldtube.csv", "Earth source profile weighted in observed frame", "radius_or_shell;density_or_stress_proxy;composition;orbit_kernel;source_weight_convention;units", "geophysical Earth model plus MTS source-weight convention", "missing"),
        ("ACQ1697_2_material_tensor", "P_WEP_TiPt_material_response_tensor.csv", "TA6V/PtRh10 material response tensor", "material_id;composition;response_component;uncertainty;source_weight_convention;provenance", "official material/composition model or parent matter calculation", "missing"),
        ("ACQ1697_3_product_convention", "P_WEP_eta_product_convention.csv", "eta product normalization", "formula;sign;absolute_value_policy;unit_map;normalization;no_cancellation_guard", "derive from MICROSCOPE eta definition and branch residual convention", "missing"),
        ("ACQ1697_4_tau_min", "P_WEP_tau_min_lower_bound.csv", "strictly positive lower bound", "tau_min;confidence;derivation_or_source;assumptions;valid_range", "prove nonvanishing or compute from sourced arrays", "missing"),
        ("ACQ1697_5_parser_manifest", "P_WEP_tau_parser_manifest.json", "machine-readable ingestion manifest", "all input paths;hashes;units;schema_version;validation_rules;claim_flags_false", "local dry-run only until sources acquired", "missing"),
        ("ACQ1697_6_verdict", "WEP tau_min acquisition pack", "source checklist ready", "all rows above must be present before tau scoring", "do not score from checklist", "ready_nonclaim_checklist"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acq_id": acq_id,
            "needed_artifact": artifact,
            "object": obj,
            "required_fields": fields,
            "source_route": route,
            "current_status": status,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acq_id, artifact, obj, fields, route, status in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1697_0_axiom_claim", "claim owner axiom as theorem", "REJECT_AXIOM_AS_DERIVATION", "candidate is written but not derived"),
        ("RUN1697_1_delta_w_zero", "set Delta_w_A=0 from axiom candidate", "REJECT_DELTA_W_ZERO", "candidate clauses remain unsigned"),
        ("RUN1697_2_data_claim", "claim WEP data acquired", "REJECT_DATA_ACQUIRED", "source candidates recorded but no arrays downloaded/validated"),
        ("RUN1697_3_tau_min", "claim tau_min>0", "REJECT_TAU_MIN_CLAIM", "no readout/source/material/product arrays exist"),
        ("RUN1697_4_wep_score", "run WEP source score", "REJECT_WEP_SCORE", "parser manifest and inputs missing"),
        ("RUN1697_5_local_gr", "claim local GR/Newton", "BLOCKED_NO_CLAIM", "owner axiom and empirical finite route not closed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1697_0_primary",
            "1698-Y5-R2FR-owner-axiom-derivation-test-or-WEP-data-request-runner.md",
            "scripts/Y5_R2FR_owner_axiom_derivation_test_or_WEP_data_request_runner.py",
            "try to derive AX1697 from MTS quotient/category primitives; in parallel generate a dry-run data-request/download script for MICROSCOPE WEP arrays without claiming data acquired",
            "selected",
        ),
        (
            "NEXT1697_1_axiom_only",
            "1698a-Y5-R2FR-owner-axiom-minimality-and-countermodel-test.md",
            "scripts/Y5_R2FR_owner_axiom_minimality_and_countermodel_test.py",
            "test whether any AX1697 clause can be weakened without reopening the w_A countermodel",
            "held_fallback",
        ),
        (
            "NEXT1697_2_data_only",
            "1698b-Y5-R2FR-MICROSCOPE-public-source-hunt-and-download-dry-run.md",
            "scripts/Y5_R2FR_MICROSCOPE_public_source_hunt_and_download_dry_run.py",
            "search/download dry-run for public machine-readable MICROSCOPE arrays or create a request ledger if unavailable",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1697_0_owner_axiom", "AX1697 derived theorem", "BLOCKED_NO_CLAIM", "candidate only"),
        ("CG1697_1_delta_w_zero", "Delta_w theorem-zero", "BLOCKED_NO_CLAIM", "owner axiom not derived"),
        ("CG1697_2_data_acquired", "MICROSCOPE arrays acquired", "BLOCKED_NO_CLAIM", "source candidates only"),
        ("CG1697_3_tau_min", "tau_min positive lower bound", "BLOCKED_NO_CLAIM", "missing arrays and proof"),
        ("CG1697_4_WEP_score", "WEP source-weight score", "BLOCKED_NO_CLAIM", "parser inputs missing"),
        ("CG1697_5_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "source-side route still open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(source_rows, axiom_rows, risk_rows, web_rows, acq_rows, runner_rows_, next_rows, claim_rows):
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    axiom_complete = {"OrdinaryMatterObjectLanguage", "NoSourceOnlyPrefactor", "SingleActionDensityLine", "VariationBeforeReadout", "ConnectedOrdinaryMatterNaturality", "NoHiddenReadoutReentry"}.issubset({str(row["clause"]) for row in axiom_rows})
    axiom_not_derived = any(row["axiom_id"] == "AX1697_7_verdict" and row["status"] == "OWNER_AXIOM_CANDIDATE_READY_NOT_DERIVED" for row in axiom_rows)
    risks_open = all(not bool_cell(row["risk_closed"]) for row in risk_rows)
    web_sources_recorded = {"https://arxiv.org/abs/2209.15487", "https://arxiv.org/abs/2201.10841"}.issubset({str(row["url"]) for row in web_rows})
    no_downloads = all(not bool_cell(row["downloaded"]) for row in web_rows)
    acquisition_complete = {"P_WEP_K_CMSM_readout.csv", "P_WEP_R_source_Earth_worldtube.csv", "P_WEP_TiPt_material_response_tensor.csv", "P_WEP_eta_product_convention.csv", "P_WEP_tau_min_lower_bound.csv", "P_WEP_tau_parser_manifest.json"}.issubset({str(row["needed_artifact"]) for row in acq_rows})
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1697_0_primary" and row["selection_status"] == "selected" for row in next_rows)
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1697*"))) == 0 if FORMALIZATION.exists() else True
    checks = [
        ("VAL1697_0_sources_exist", sources_ok, "all cited local source paths exist and required needles are present"),
        ("VAL1697_1_axiom_complete", axiom_complete, "minimal owner axiom candidate includes all six required clauses"),
        ("VAL1697_2_axiom_not_derived", axiom_not_derived, "owner axiom remains a candidate, not a theorem"),
        ("VAL1697_3_risks_open", risks_open, "axiom risks remain open and nonclaim"),
        ("VAL1697_4_web_sources_recorded", web_sources_recorded, "external WEP source candidates are recorded"),
        ("VAL1697_5_no_downloads", no_downloads, "no external arrays are falsely marked downloaded"),
        ("VAL1697_6_acquisition_complete", acquisition_complete, "WEP tau_min acquisition checklist includes all required artifacts"),
        ("VAL1697_7_runner_blocks", runner_blocks, "runner blocks axiom, data, tau, WEP and local-GR claims"),
        ("VAL1697_8_next_selected", next_selected, "next target selects derivation test or data-request runner"),
        ("VAL1697_9_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1697_10_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1697_11_csv_parse", csv_parse, "all generated 1697 CSVs parse"),
        ("VAL1697_12_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1697_13_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1697_14_formalization_untouched", formalization_untouched, "no 1697 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"check_id": cid, "result": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False} for cid, passed, detail in checks]
    rows.append({"check_id": "VAL1697_OVERALL", "result": "PASS" if overall else "FAIL", "detail": "1697 owner axiom candidate and WEP readout/source pack validation", "valid_for_claim": False, "claim_allowed": False})
    return rows


def write_doc(source_rows, axiom_rows, risk_rows, web_rows, acq_rows, runner_rows_, next_rows, claim_rows, validation_rows):
    body = f"""# 1697 - Owner Axiom Candidate And WEP Readout Source Pack

## Verdict

1697 writes the first explicit minimal parent-owner axiom candidate. If derived, it would forbid source-only `w_A` by making active-source coefficients non-objects of the parent ordinary-matter language except for a common constant calibration mode.

This is **not** promoted as a theorem. It is a target contract: useful because every clause is now visible, risky because adopting it without derivation would be a closure axiom rather than a GR reduction.

The finite WEP route is also made concrete. The required artifacts are named: official CMSM/readout arrays, Earth source worldtube, Ti/Pt material tensor, eta product convention, tau-min lower bound, and a parser manifest. External source candidates are recorded, but no arrays are marked acquired.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1697"])}

## Minimal Owner Axiom Candidate

{markdown_table(axiom_rows, ["axiom_id", "clause", "status", "effect_if_derived"])}

## Axiom Risk Audit

{markdown_table(risk_rows, ["risk_id", "risk", "failure_mode", "required_closure"])}

## WEP Data Source Candidates

{markdown_table(web_rows, ["web_id", "source_name", "url", "use_for", "status"])}

## WEP Tau-Min Acquisition Pack

{markdown_table(acq_rows, ["acq_id", "needed_artifact", "object", "current_status", "source_route"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is useful because it gives us two honest levers. The theory lever is now an explicit axiom candidate to derive or reject. The empirical lever is now a named data pack instead of vague “get MICROSCOPE data”. No claim is made from either lever yet.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    axiom_rows = owner_axiom_rows()
    risk_rows = axiom_risk_rows()
    web_rows = web_source_rows()
    acq_rows = acquisition_pack_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()
    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1697", "valid_for_claim", "claim_allowed"])
    write_csv(OWNER_AXIOM, axiom_rows, ["branch_id", "axiom_id", "clause", "formal_statement", "status", "effect_if_derived", "parent_derived", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(AXIOM_RISK, risk_rows, ["branch_id", "risk_id", "risk", "failure_mode", "required_closure", "risk_closed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(WEB_SOURCES, web_rows, ["branch_id", "web_id", "source_name", "url", "doi_or_related", "use_for", "claim_limit", "status", "downloaded", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(ACQUISITION_PACK, acq_rows, ["branch_id", "acq_id", "needed_artifact", "object", "required_fields", "source_route", "current_status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])
    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, axiom_rows, risk_rows, web_rows, acq_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, axiom_rows, risk_rows, web_rows, acq_rows, runner_rows_, next_rows, claim_rows, validation_rows)
    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1697 validation PASS")


if __name__ == "__main__":
    main()
