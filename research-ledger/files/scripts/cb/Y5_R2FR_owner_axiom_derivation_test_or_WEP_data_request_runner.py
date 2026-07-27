from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1698"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_SOURCE = MICROSCOPE / "branch_locked_wep" / "source"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1698-Y5-R2FR-owner-axiom-derivation-test-or-WEP-data-request-runner.md"
DRY_RUN_SCRIPT = ROOT / "scripts" / "MICROSCOPE_WEP_public_source_download_dry_run.py"

SOURCE_FILES = {
    "1697_doc": ROOT / "1697-Y5-R2FR-owner-axiom-candidate-and-WEP-readout-source-pack.md",
    "1697_validation": OUT / "P8_Y5_BRR545_1697_VALIDATION.csv",
    "1697_owner_axiom": OUT / "P8_Y5_PARENT_QLOC_1697_MINIMAL_OWNER_AXIOM_CANDIDATE.csv",
    "1697_risk_audit": OUT / "P8_Y5_PARENT_QLOC_1697_AXIOM_RISK_AUDIT.csv",
    "1697_web_sources": OUT / "P8_Y5_PARENT_QLOC_1697_WEP_DATA_SOURCE_CANDIDATES.csv",
    "1697_acquisition_pack": OUT / "P8_Y5_PARENT_QLOC_1697_WEP_TAU_MIN_ACQUISITION_PACK.csv",
    "1697_runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1697_RUNNER_REFUSAL.csv",
    "1697_next_target": OUT / "P8_Y5_PARENT_QLOC_1697_NEXT_TARGET.csv",
    "1450_label_forgetting": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1452_measure_current": OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv",
    "1464_connected_category": OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv",
    "1478_action_line": MICROSCOPE / "quarantine" / "1478" / "SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT_NONCLAIM.csv",
    "1479_typing": MICROSCOPE / "quarantine" / "1479" / "NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT_NONCLAIM.csv",
    "1480_hom": MICROSCOPE / "quarantine" / "1480" / "COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT_NONCLAIM.csv",
    "1482_parser_status": BRANCH_SOURCE / "P_WEP_R_source_status_1482.csv",
}

NEEDLES = {
    "1697_doc": ["NEXT1697_0_primary", "Owner Axiom Candidate"],
    "1697_validation": ["VAL1697_OVERALL", "PASS"],
    "1697_owner_axiom": ["AX1697_7_verdict", "OWNER_AXIOM_CANDIDATE_READY_NOT_DERIVED"],
    "1697_risk_audit": ["RISK1697_5_verdict", "all risks remain open"],
    "1697_web_sources": ["https://arxiv.org/abs/2209.15487", "https://arxiv.org/abs/2201.10841"],
    "1697_acquisition_pack": ["P_WEP_K_CMSM_readout.csv", "P_WEP_tau_parser_manifest.json"],
    "1697_runner_refusal": ["RUN1697_5_local_gr", "BLOCKED_NO_CLAIM"],
    "1697_next_target": ["NEXT1697_0_primary", "owner-axiom-derivation-test"],
    "1450_label_forgetting": ["HT1450_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1452_measure_current": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1464_connected_category": ["CON1464_5_verdict", "PROOF_NOT_CLOSED"],
    "1478_action_line": ["SAL1478_4_verdict", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"],
    "1479_typing": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    "1480_hom": ["CDH1480_5_verdict", "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED"],
    "1482_parser_status": ["ACCEPT1482_5_overall_parser_permission", "BLOCKED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1698_SOURCE_REGISTER.csv"
DERIVATION_TEST = OUT / "P8_Y5_PARENT_QLOC_1698_AXIOM_DERIVATION_TEST.csv"
COUNTERMODEL = OUT / "P8_Y5_PARENT_QLOC_1698_AXIOM_MINIMALITY_COUNTERMODEL.csv"
WEP_REQUEST = OUT / "P8_Y5_PARENT_QLOC_1698_WEP_DATA_REQUEST_DRY_RUN.csv"
DOWNLOAD_MANIFEST = OUT / "P8_Y5_PARENT_QLOC_1698_DOWNLOAD_SCRIPT_MANIFEST.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1698_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1698_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1698_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1698_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    DERIVATION_TEST,
    COUNTERMODEL,
    WEP_REQUEST,
    DOWNLOAD_MANIFEST,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    DERIVATION_TEST,
    COUNTERMODEL,
    WEP_REQUEST,
    DOWNLOAD_MANIFEST,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    DERIVATION_TEST: [
        QUARANTINE / "AXIOM_DERIVATION_TEST.csv",
        BRANCH_RESIDUALS / "R2FR_owner_axiom_derivation_test_1698.csv",
        QUEUE / "JR1698_OWNER_AXIOM_DERIVATION_TEST.csv",
    ],
    COUNTERMODEL: [
        QUARANTINE / "AXIOM_MINIMALITY_COUNTERMODEL.csv",
        BRANCH_RESIDUALS / "R2FR_axiom_minimality_countermodel_1698.csv",
        QUEUE / "JR1698_AXIOM_MINIMALITY_COUNTERMODEL.csv",
    ],
    WEP_REQUEST: [
        QUARANTINE / "WEP_DATA_REQUEST_DRY_RUN.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_data_request_dry_run_1698.csv",
        QUEUE / "JR1698_WEP_DATA_REQUEST_DRY_RUN.csv",
    ],
    DOWNLOAD_MANIFEST: [
        QUARANTINE / "DOWNLOAD_SCRIPT_MANIFEST.csv",
        BRANCH_RESIDUALS / "R2FR_download_script_manifest_1698.csv",
        QUEUE / "JR1698_DOWNLOAD_SCRIPT_MANIFEST.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1698.csv",
        QUEUE / "JR1698_NEXT_TARGET.csv",
    ],
}


DRY_RUN_SCRIPT_BODY = '''from __future__ import annotations

import argparse
import json
from pathlib import Path


DRY_RUN_DEFAULT = True

SOURCES = [
    {
        "source_id": "MICROSCOPE_FINAL_RESULT_2022",
        "url": "https://arxiv.org/abs/2209.15487",
        "doi": "https://doi.org/10.1103/PhysRevLett.129.121102",
        "use": "eta_TiPt result provenance only; not machine-readable CMSM arrays",
    },
    {
        "source_id": "MICROSCOPE_GROUND_SEGMENT_2022",
        "url": "https://arxiv.org/abs/2201.10841",
        "doi": "https://doi.org/10.1088/1361-6382/ac4b9a",
        "use": "mission sessions, CNES/ONERA/CMSM data-flow provenance",
    },
    {
        "source_id": "HAL_GROUND_SEGMENT_PDF",
        "url": "https://hal.science/hal-03564498/document",
        "doi": "not_recorded",
        "use": "open PDF mirror for data-processing paper",
    },
    {
        "source_id": "CNES_ONERA_CMSM_REQUEST_ROUTE",
        "url": "not_found_as_public_machine_readable_URL_in_current_search",
        "doi": "not_applicable",
        "use": "manual/archive request route for official arrays",
    },
]

ARTIFACTS = [
    "P_WEP_K_CMSM_readout.csv",
    "P_WEP_R_source_Earth_worldtube.csv",
    "P_WEP_TiPt_material_response_tensor.csv",
    "P_WEP_eta_product_convention.csv",
    "P_WEP_tau_min_lower_bound.csv",
    "P_WEP_tau_parser_manifest.json",
]


def build_plan(destination: Path, execute_downloads: bool) -> dict[str, object]:
    return {
        "dry_run": not execute_downloads,
        "claim_allowed": False,
        "valid_for_claim": False,
        "destination": str(destination),
        "sources": SOURCES,
        "artifacts_required_before_scoring": [
            {"artifact": artifact, "status": "not_downloaded", "valid_for_claim": False}
            for artifact in ARTIFACTS
        ],
        "rule": "Do not claim WEP/local-GR/R10 pass from this script; it only prints a source/request plan.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="MICROSCOPE WEP public-source download/request dry-run.")
    parser.add_argument("--destination", default="source-intake/microscope/branch_locked_wep/source")
    parser.add_argument("--execute-downloads", action="store_true", help="Reserved; still refuses without manually sourced array URLs.")
    parser.add_argument("--write-plan-json", default="")
    args = parser.parse_args()

    plan = build_plan(Path(args.destination), bool(args.execute_downloads))
    print(json.dumps(plan, indent=2, sort_keys=True))
    if args.write_plan_json:
        Path(args.write_plan_json).write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    if args.execute_downloads:
        raise SystemExit("No executable public machine-readable CMSM array URL is registered; refusing download.")


if __name__ == "__main__":
    main()
'''


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
                "use_in_1698": "AX1697 derivation test, minimality countermodel, and WEP source request dry-run",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def derivation_test_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DER1698_0_domain_exhaustion",
            "OrdinaryMatterObjectLanguage",
            "parent grammar proves all ordinary matter source slots are observed geometry, dynamical fields, gauge/current data, representation constants, or universal constants",
            "1450 label forgetting plus 1697 AX1697_0",
            "not_closed",
            "missing parent grammar theorem excluding source-only coefficient objects",
            "add inert scalar source coefficient w_A to Arg(S_ord) without affecting kinematics",
        ),
        (
            "DER1698_1_active_source_target_absence",
            "NoSourceOnlyPrefactor",
            "Coeff_active_source is not an object/target of the parent language except one common constant calibration",
            "1479 typing theorem attempt and 1480 Hom exclusion attempt",
            "not_closed",
            "missing signed Hom exclusion at parent level",
            "define Hom(species_label,Coeff_active_source) nontrivially and recover independent w_A",
        ),
        (
            "DER1698_2_single_density_owner",
            "SingleActionDensityLine",
            "one action-density, measure, hbar, and source-normalization owner covers ordinary matter",
            "1478 action-line attempt plus 1452 common measure/current attempt",
            "not_closed",
            "missing component-vector/action-line proof",
            "use separate component action lines S_A with independent weights while keeping local field equations rescaled",
        ),
        (
            "DER1698_3_variation_before_readout",
            "VariationBeforeReadout",
            "parent stress/source is varied before material, instrument, orbit, or readout selectors are applied",
            "1697 explicit axiom candidate and 1482 parser blocker",
            "not_closed",
            "missing parent ordering theorem for readout maps",
            "let a readout selector multiply source residuals after variation and mimic Delta_w",
        ),
        (
            "DER1698_4_connected_naturality",
            "ConnectedOrdinaryMatterNaturality",
            "ordinary matter source-normalization graph is connected and natural scalars collapse to one common mode",
            "1464 connected matter category proof attempt",
            "not_closed",
            "missing connected category certificate",
            "split ordinary matter into disconnected components with independent natural weights",
        ),
        (
            "DER1698_5_no_reentry",
            "NoHiddenReadoutReentry",
            "effective action, boundary, measure, hidden invariant, and readout maps preserve source-coefficient exclusion",
            "1697 risk audit",
            "not_closed",
            "missing EFT/readout no-reentry theorem",
            "introduce hidden invariant I_hid and coefficient c(I_hid) multiplying the active source",
        ),
        (
            "DER1698_6_result",
            "DeltaWZeroConsequence",
            "Delta_w_A=0 follows only if DER1698_0 through DER1698_5 close as parent theorems",
            "1697 AX1697_6 conditional consequence",
            "blocked_no_claim",
            "at least six parent clauses are unsigned",
            "set common calibration aside but leave species/source weights live",
        ),
        (
            "DER1698_7_verdict",
            "OwnerAxiomDerivationStatus",
            "AX1697 remains a minimal derivation target, not a theorem",
            "1698 derivation audit",
            "AXIOM_NOT_DERIVED_COUNTERMODELS_PRESENT",
            "derive parent grammar/Hom/action/readout/connectivity/no-reentry stack or keep finite WEP route",
            "all weakened routes reopen w_A or hidden source coefficient",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": test_id,
            "clause": clause,
            "required_parent_statement": statement,
            "prior_evidence": evidence,
            "current_result": result,
            "missing_parent_input": missing,
            "countermodel_if_missing": countermodel,
            "parent_derived": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for test_id, clause, statement, evidence, result, missing, countermodel in rows
    ]


def countermodel_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CM1698_0_remove_domain",
            "remove ordinary-matter object-language exhaustion",
            "admit inert source-only scalar slot w_A in the parent action language",
            "species/source weights are legal objects and local GR reduction is not forced",
            "clause appears necessary at current proof level",
        ),
        (
            "CM1698_1_remove_no_source_prefactor",
            "remove NoSourceOnlyPrefactor",
            "S_matter = sum_A w_A integral dmu L_A with w_A constant per species/source",
            "field equations can be rescaled while active source normalization differs",
            "clause appears necessary at current proof level",
        ),
        (
            "CM1698_2_remove_single_action_line",
            "remove single action-density/measure owner",
            "use separate component measures or hbar/action normalizations",
            "source weights hide in component Jacobians or quantum/action units",
            "clause appears necessary at current proof level",
        ),
        (
            "CM1698_3_remove_variation_order",
            "remove variation-before-readout",
            "let instrument/material/readout selector multiply the already-varied source",
            "Delta_w returns as a readout-side source coefficient",
            "clause appears necessary at current proof level",
        ),
        (
            "CM1698_4_remove_connected_naturality",
            "remove connected ordinary matter graph",
            "ordinary matter decomposes into disconnected sectors with separate natural scalars",
            "one common calibration no longer propagates across Ti/Pt or other sectors",
            "clause appears necessary at current proof level",
        ),
        (
            "CM1698_5_remove_no_reentry",
            "remove hidden/effective no-reentry",
            "effective coefficient c(I_hid), boundary term, or disformal readout factor multiplies source",
            "bare exclusion is bypassed after projection/EFT/readout",
            "clause appears necessary at current proof level",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": cid,
            "weakened_clause": weakened,
            "countermodel_construction": construction,
            "failure_reopened": failure,
            "minimality_status": status,
            "clause_needed": True,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, weakened, construction, failure, status in rows
    ]


def wep_request_rows() -> list[dict[str, object]]:
    rows = [
        (
            "REQ1698_0_final_result",
            "MICROSCOPE final WEP result",
            "https://arxiv.org/abs/2209.15487",
            "https://doi.org/10.1103/PhysRevLett.129.121102",
            "eta_TiPt anchor/provenance",
            "source_anchor_only",
            "no raw CMSM/readout arrays in recorded route",
        ),
        (
            "REQ1698_1_ground_segment",
            "MICROSCOPE mission scenario, ground segment and data processing",
            "https://arxiv.org/abs/2201.10841",
            "https://doi.org/10.1088/1361-6382/ac4b9a",
            "CNES/ONERA/CMSM data-flow context",
            "source_anchor_only",
            "method paper, not machine-readable tau inputs",
        ),
        (
            "REQ1698_2_HAL_pdf",
            "HAL PDF mirror",
            "https://hal.science/hal-03564498/document",
            "not_recorded",
            "open PDF source candidate",
            "source_anchor_only",
            "may help provenance but not an array endpoint",
        ),
        (
            "REQ1698_3_CNES_ONERA_request",
            "CNES/ONERA/CMSM archive or contact route",
            "not_found_as_public_machine_readable_URL_in_current_search",
            "not_applicable",
            "official array request route",
            "manual_request_needed",
            "external state blocker remains",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "request_id": request_id,
            "source_name": name,
            "url": url,
            "doi_or_related": doi,
            "target_use": target,
            "dry_run_status": status,
            "blocker": blocker,
            "downloaded": False,
            "data_acquired": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for request_id, name, url, doi, target, status, blocker in rows
    ]


def download_manifest_rows() -> list[dict[str, object]]:
    artifacts = [
        ("DL1698_0_script", str(DRY_RUN_SCRIPT), "dry-run source/request script", "generated", "script defaults to dry-run and refuses execute mode without public array URL"),
        ("DL1698_1_readout_matrix", "P_WEP_K_CMSM_readout.csv", "official CMSM/export readout matrix", "not_downloaded", "required before tau scoring"),
        ("DL1698_2_source_worldtube", "P_WEP_R_source_Earth_worldtube.csv", "Earth source worldtube/profile", "not_downloaded", "requires source model and MTS source-weight convention"),
        ("DL1698_3_material_tensor", "P_WEP_TiPt_material_response_tensor.csv", "TA6V/PtRh10 material response tensor", "not_downloaded", "requires official composition/material model or parent matter derivation"),
        ("DL1698_4_product_convention", "P_WEP_eta_product_convention.csv", "eta product convention", "not_downloaded", "must be derived from MICROSCOPE eta convention and branch residual convention"),
        ("DL1698_5_tau_min", "P_WEP_tau_min_lower_bound.csv", "positive tau lower bound", "not_downloaded", "must be computed/proved from sourced inputs"),
        ("DL1698_6_parser_manifest", "P_WEP_tau_parser_manifest.json", "parser manifest", "not_written", "cannot be live until inputs exist"),
        ("DL1698_7_verdict", "MICROSCOPE WEP data acquisition", "dry-run only", "DATA_NOT_ACQUIRED", "no WEP/local-GR claim allowed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "manifest_id": mid,
            "artifact_or_path": artifact,
            "purpose": purpose,
            "status": status,
            "notes": notes,
            "dry_run_default": True,
            "downloaded": False,
            "data_acquired": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for mid, artifact, purpose, status, notes in artifacts
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1698_0_axiom_derivation", "promote AX1697 to theorem", "REJECT_AXIOM_DERIVATION", "each required parent clause still has an explicit countermodel"),
        ("RUN1698_1_delta_w_zero", "set Delta_w_A=0", "REJECT_DELTA_W_ZERO", "owner axiom is not derived"),
        ("RUN1698_2_tau_min", "claim tau_WEP lower bound", "REJECT_TAU_MIN", "official readout/source/material/product arrays are missing"),
        ("RUN1698_3_download_claim", "claim MICROSCOPE data acquired", "REJECT_DATA_ACQUIRED", "1698 only creates a dry-run request/download plan"),
        ("RUN1698_4_wep_score", "score WEP source branch", "REJECT_WEP_SCORE", "parser manifest and tau inputs absent"),
        ("RUN1698_5_local_gr", "claim local GR/Newton reduction", "BLOCKED_NO_CLAIM", "source-weight coupling route remains open"),
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
            "NEXT1698_0_primary",
            "1699-Y5-R2FR-parent-source-owner-grammar-or-finite-WEP-request-pack.md",
            "scripts/Y5_R2FR_parent_source_owner_grammar_or_finite_WEP_request_pack.py",
            "try the least-axiomatic parent grammar proof for source-owner exclusion; if still unsigned, build the manual MICROSCOPE request pack from 1698",
            "selected",
        ),
        (
            "NEXT1698_1_theory_route",
            "1699a-Y5-R2FR-source-owner-grammar-Hom-exclusion-proof.md",
            "scripts/Y5_R2FR_source_owner_grammar_Hom_exclusion_proof.py",
            "attack the active-source coefficient target directly with parent grammar and Hom exclusion",
            "held_fallback",
        ),
        (
            "NEXT1698_2_data_route",
            "1699b-Y5-R2FR-MICROSCOPE-manual-request-and-tau-parser-skeleton.md",
            "scripts/Y5_R2FR_MICROSCOPE_manual_request_and_tau_parser_skeleton.py",
            "turn dry-run source list into an email/archive request ledger plus parser skeleton",
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
        ("CG1698_0_owner_axiom", "AX1697 derived theorem", "BLOCKED_NO_CLAIM", "countermodels remain for every clause"),
        ("CG1698_1_delta_w_zero", "Delta_w theorem-zero", "BLOCKED_NO_CLAIM", "source-owner exclusion not derived"),
        ("CG1698_2_WEP_data", "MICROSCOPE WEP arrays acquired", "BLOCKED_NO_CLAIM", "dry-run only; no arrays acquired"),
        ("CG1698_3_tau_min", "tau_WEP positive lower bound", "BLOCKED_NO_CLAIM", "missing readout/source/material/product arrays"),
        ("CG1698_4_R10_WEP_PPN_clock_orbital", "local arena pass", "BLOCKED_NO_CLAIM", "coupling/source branch remains unsolved"),
        ("CG1698_5_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "must derive parent source owner or finite bound branch"),
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


def write_dry_run_script() -> None:
    DRY_RUN_SCRIPT.write_text(DRY_RUN_SCRIPT_BODY, encoding="utf-8")


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in (
                "can_score",
                "accepted_for_scoring",
                "score_ready",
                "valid_prediction_row",
                "valid_for_claim",
                "claim_allowed",
                "downloaded",
                "data_acquired",
            ):
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


def validate(
    source_rows_: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    countermodel_rows_: list[dict[str, object]],
    wep_rows: list[dict[str, object]],
    manifest_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows_)
    all_six_clauses_tested = {
        "OrdinaryMatterObjectLanguage",
        "NoSourceOnlyPrefactor",
        "SingleActionDensityLine",
        "VariationBeforeReadout",
        "ConnectedOrdinaryMatterNaturality",
        "NoHiddenReadoutReentry",
    }.issubset({str(row["clause"]) for row in derivation_rows})
    derivation_blocked = any(
        row["test_id"] == "DER1698_7_verdict" and row["current_result"] == "AXIOM_NOT_DERIVED_COUNTERMODELS_PRESENT"
        for row in derivation_rows
    )
    every_derivation_unsigned = all(not bool_cell(row["parent_derived"]) for row in derivation_rows)
    countermodels_complete = len(countermodel_rows_) >= 6 and all(str(row["countermodel_construction"]) for row in countermodel_rows_)
    every_clause_needed = all(bool_cell(row["clause_needed"]) for row in countermodel_rows_)
    wep_sources_recorded = {"https://arxiv.org/abs/2209.15487", "https://arxiv.org/abs/2201.10841"}.issubset({str(row["url"]) for row in wep_rows})
    no_data_downloaded = all(not bool_cell(row["downloaded"]) and not bool_cell(row["data_acquired"]) for row in wep_rows + manifest_rows)
    dry_run_script_exists = DRY_RUN_SCRIPT.exists() and "DRY_RUN_DEFAULT = True" in read_text(DRY_RUN_SCRIPT)
    dry_run_manifest_safe = all(bool_cell(row["dry_run_default"]) and not bool_cell(row["claim_allowed"]) for row in manifest_rows)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1698_0_primary" and row["selection_status"] == "selected" for row in next_rows)
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
    formalization_untouched = len(list(FORMALIZATION.rglob("*1698*"))) == 0 if FORMALIZATION.exists() else True
    checks = [
        ("VAL1698_0_sources_exist", sources_ok, "all cited local source paths exist and required needles are present"),
        ("VAL1698_1_all_clauses_tested", all_six_clauses_tested, "all six AX1697 parent clauses are tested"),
        ("VAL1698_2_derivation_blocked", derivation_blocked, "AX1697 is not promoted; countermodels remain"),
        ("VAL1698_3_every_derivation_unsigned", every_derivation_unsigned, "no parent-derived flags are set true"),
        ("VAL1698_4_countermodels_complete", countermodels_complete, "every weakened clause has an explicit countermodel"),
        ("VAL1698_5_every_clause_needed", every_clause_needed, "minimality table marks each clause needed at current proof level"),
        ("VAL1698_6_wep_sources_recorded", wep_sources_recorded, "MICROSCOPE WEP source anchors are recorded"),
        ("VAL1698_7_no_data_downloaded", no_data_downloaded, "1698 remains dry-run only; no arrays are marked acquired"),
        ("VAL1698_8_dry_run_script_exists", dry_run_script_exists, "dry-run request/download helper exists and defaults safe"),
        ("VAL1698_9_dry_run_manifest_safe", dry_run_manifest_safe, "download manifest keeps claim flags false"),
        ("VAL1698_10_runner_blocks", runner_blocks, "runner blocks axiom, tau, WEP and local-GR claims"),
        ("VAL1698_11_next_selected", next_selected, "next target selects parent grammar proof or finite WEP request pack"),
        ("VAL1698_12_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1698_13_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1698_14_csv_parse", csv_parse, "all generated 1698 CSVs parse"),
        ("VAL1698_15_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1698_16_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1698_17_formalization_untouched", formalization_untouched, "no 1698 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": cid,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1698_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1698 owner axiom derivation test and WEP data request dry-run validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows_: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    countermodel_rows_: list[dict[str, object]],
    wep_rows: list[dict[str, object]],
    manifest_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1698 - Owner Axiom Derivation Test Or WEP Data Request Runner

## Verdict

1698 takes the honest shot at deriving the AX1697 owner axiom and does **not** close it. Every clause now has a clear parent-theorem target, but every weakened clause also has a countermodel that reopens `w_A`, a hidden source coefficient, or readout-side source rescaling.

So the result is useful but not glamorous: AX1697 is now a minimal derivation target rather than a vague wish. The theory branch still needs a parent source-owner grammar/Hom exclusion proof before `Delta_w_A=0` can be claimed.

The empirical branch is also made safer. 1698 generates a dry-run MICROSCOPE WEP source/request helper and manifest, but it marks no CMSM/readout arrays as downloaded and makes no WEP, R10, PPN, clock, orbital, local-GR, or Newton claim.

## Source Register

{markdown_table(source_rows_, ["source_key", "source_path", "exists", "needles_present", "use_in_1698"])}

## AX1697 Derivation Test

{markdown_table(derivation_rows, ["test_id", "clause", "current_result", "missing_parent_input"])}

## Minimality Countermodels

{markdown_table(countermodel_rows_, ["countermodel_id", "weakened_clause", "failure_reopened", "minimality_status"])}

## WEP Data Request Dry-Run

{markdown_table(wep_rows, ["request_id", "source_name", "url", "dry_run_status", "blocker"])}

## Download Script Manifest

{markdown_table(manifest_rows, ["manifest_id", "artifact_or_path", "purpose", "status", "notes"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

The coupling/source-owner gap is now sharply localized. We either prove the parent language has no source-only coefficient target, or we stop trying to magic it away and run the finite WEP request/tau parser route. That is frustrating, but it is clean: no smuggled plateau, no fake `tau_WEP=1`, and no claim until the coupling is owned.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    write_dry_run_script()
    source_rows_ = source_register_rows()
    derivation_rows = derivation_test_rows()
    countermodel_rows_ = countermodel_rows()
    wep_rows = wep_request_rows()
    manifest_rows = download_manifest_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()
    write_csv(SOURCE_REGISTER, source_rows_, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1698", "valid_for_claim", "claim_allowed"])
    write_csv(DERIVATION_TEST, derivation_rows, ["branch_id", "test_id", "clause", "required_parent_statement", "prior_evidence", "current_result", "missing_parent_input", "countermodel_if_missing", "parent_derived", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(COUNTERMODEL, countermodel_rows_, ["branch_id", "countermodel_id", "weakened_clause", "countermodel_construction", "failure_reopened", "minimality_status", "clause_needed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(WEP_REQUEST, wep_rows, ["branch_id", "request_id", "source_name", "url", "doi_or_related", "target_use", "dry_run_status", "blocker", "downloaded", "data_acquired", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DOWNLOAD_MANIFEST, manifest_rows, ["branch_id", "manifest_id", "artifact_or_path", "purpose", "status", "notes", "dry_run_default", "downloaded", "data_acquired", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])
    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows_, derivation_rows, countermodel_rows_, wep_rows, manifest_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows_, derivation_rows, countermodel_rows_, wep_rows, manifest_rows, runner_rows_, next_rows, claim_rows, validation_rows)
    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {DRY_RUN_SCRIPT}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1698 validation PASS")


if __name__ == "__main__":
    main()
