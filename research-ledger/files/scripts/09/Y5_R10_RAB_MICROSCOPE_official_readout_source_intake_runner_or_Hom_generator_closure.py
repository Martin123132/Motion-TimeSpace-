from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "1482-Y5-R10-RAB-MICROSCOPE-official-readout-source-intake-runner-or-Hom-generator-closure.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1481_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1481_VALIDATION.csv"
PREV_TAU = OUT / "P8_Y5_R10_1481_WEP_TAU_SOURCE_READOUT_PACK.csv"
PREV_REJECTION = OUT / "P8_Y5_R10_1481_REJECTION_LEDGER.csv"
PREV_HOM = OUT / "P8_Y5_R10_1481_HOM_PARENT_GENERATOR_PROOF_SHARPENING.csv"
PREV_CONTRACT = OUT / "P8_Y5_R10_1481_SAME_BRANCH_WEP_PRODUCT_CONTRACT.csv"

WAIT_1335 = OUT / "P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv"
MANIFEST_1335 = OUT / "P8_Y5_R10_1335_OFFICIAL_INPUT_REQUEST_MANIFEST.csv"
PRODUCT_1335 = OUT / "P8_Y5_R10_1335_ELECTRON_WEP_PRODUCT_NORMALIZATION_CONTRACT.csv"
INTAKE_1228 = OUT / "P8_Y5_R10_1228_INTAKE_DIRECTORY_CONTRACT.csv"
ACCEPT_1228 = OUT / "P8_Y5_R10_1228_ACCEPTANCE_GATE_MATRIX.csv"
FEED_1228 = OUT / "P8_Y5_R10_1228_TAU_WEP_FEED_UPDATE.csv"

META_1336 = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_LOCAL_MICROSCOPE_INTAKE_AUDIT.csv"
WEB_1336 = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_WEB_SOURCE_CANDIDATE_REGISTER.csv"
READOUT_SCHEMA_1336 = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_OFFICIAL_READOUT_SCHEMA.csv"
SOURCE_SCHEMA_1336 = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_SOURCE_WORLDTUBE_SCHEMA.csv"
PRODUCT_SCHEMA_1336 = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
BRANCH_SCHEMA_1336 = MICROSCOPE / "metadata" / "P8_Y5_R10_1336_BRANCH_CLASSIFIER_SCHEMA.csv"

DOC_1443 = ROOT / "1443-Y5-R10-RAB-branch-product-first-fill-or-C-parent-source-search-plan.md"
DOC_1444 = ROOT / "1444-Y5-R10-RAB-product-convention-official-extraction-or-C-parent-theorem-source-search.md"
DOC_1445 = ROOT / "1445-Y5-R10-RAB-K-CMSM-readout-extraction-or-C-parent-coupling-theorem.md"

PRODUCT_LIVE = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
BRANCH_LIVE = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"
READOUT_REQUIREMENTS = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout_REQUIREMENTS.csv"
READOUT_LIVE = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
SOURCE_WORLDTUBE_LIVE = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
FULL_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
C_PARENT_IMPORT = MICROSCOPE / "branch_locked_wep" / "coefficients" / "C_parent_WEP_slot_import.csv"
C_PARENT_SCHEMA = MICROSCOPE / "branch_locked_wep" / "coefficients" / "C_parent_import_schema.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1482_SOURCE_REGISTER.csv"
WEB_CANDIDATES = OUT / "P8_Y5_R10_1482_OFFICIAL_WEB_SOURCE_CANDIDATES.csv"
DIRECTORY_STATUS = OUT / "P8_Y5_R10_1482_MICROSCOPE_INTAKE_DIRECTORY_STATUS.csv"
OFFICIAL_MANIFEST_UPDATE = OUT / "P8_Y5_R10_1482_OFFICIAL_INPUT_MANIFEST_UPDATE.csv"
ACCEPTANCE_GATE_UPDATE = OUT / "P8_Y5_R10_1482_INTAKE_ACCEPTANCE_GATE_UPDATE.csv"
PARSER_PRECHECK = OUT / "P8_Y5_R10_1482_PARSER_PRECHECK.csv"
TAU_READINESS = OUT / "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv"
HOM_CLOSURE = OUT / "P8_Y5_R10_1482_HOM_PARENT_GENERATOR_CLOSURE_ATTEMPT.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1482_REJECTION_LEDGER.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1482_REDUCTION_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1482_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1482_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1482_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1482"
QUAR_SOURCE_PACK = QUARANTINE / "source_pack_status_nonclaim.csv"
QUAR_TAU = QUARANTINE / "tau_WEP_readiness_nonclaim.csv"
BRANCH_READOUT_STATUS = MICROSCOPE / "branch_locked_wep" / "readout" / "P_WEP_K_CMSM_readout_status_1482.csv"
BRANCH_SOURCE_STATUS = MICROSCOPE / "branch_locked_wep" / "source" / "P_WEP_R_source_status_1482.csv"
BRANCH_PRODUCT_STATUS = MICROSCOPE / "branch_locked_wep" / "product" / "P_WEP_eta_product_status_1482.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def text_contains_blocker(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8", errors="replace").upper()
    blockers = ["MISSING", "PENDING", "NOT_FILLED", "ABSENT", "NONCLAIM", "FALSE"]
    return any(blocker in text for blocker in blockers)


def file_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1482_0_prev_next", PREV_NEXT, "1481 handoff selecting MICROSCOPE intake or Hom closure"),
        ("SRC1482_1_prev_validation", PREV_VALIDATION, "1481 validation baseline"),
        ("SRC1482_2_prev_tau", PREV_TAU, "1481 tau/source/readout blocked pack"),
        ("SRC1482_3_prev_rejection", PREV_REJECTION, "1481 rejection ledger"),
        ("SRC1482_4_prev_Hom", PREV_HOM, "1481 Hom parent-generator sharpening"),
        ("SRC1482_5_prev_contract", PREV_CONTRACT, "1481 same-branch WEP product contract"),
        ("SRC1482_6_wait1335", WAIT_1335, "readout/source waitstate"),
        ("SRC1482_7_manifest1335", MANIFEST_1335, "official input request manifest"),
        ("SRC1482_8_product1335", PRODUCT_1335, "tau/product normalization contract"),
        ("SRC1482_9_intake1228", INTAKE_1228, "intake directory contract"),
        ("SRC1482_10_accept1228", ACCEPT_1228, "acceptance gate baseline"),
        ("SRC1482_11_feed1228", FEED_1228, "tau_WEP feed baseline"),
        ("SRC1482_12_meta1336", META_1336, "local MICROSCOPE intake audit"),
        ("SRC1482_13_web1336", WEB_1336, "web source candidate register"),
        ("SRC1482_14_readout_schema", READOUT_SCHEMA_1336, "readout schema"),
        ("SRC1482_15_source_schema", SOURCE_SCHEMA_1336, "source-worldtube schema"),
        ("SRC1482_16_product_schema", PRODUCT_SCHEMA_1336, "product convention schema"),
        ("SRC1482_17_branch_schema", BRANCH_SCHEMA_1336, "branch classifier schema"),
        ("SRC1482_18_doc1443", DOC_1443, "branch/product first-fill context"),
        ("SRC1482_19_doc1444", DOC_1444, "official product extraction context"),
        ("SRC1482_20_doc1445", DOC_1445, "K_CMSM readout requirements context"),
        ("SRC1482_21_product_live", PRODUCT_LIVE, "live nonclaim product convention row"),
        ("SRC1482_22_branch_live", BRANCH_LIVE, "live nonclaim branch guard"),
        ("SRC1482_23_readout_requirements", READOUT_REQUIREMENTS, "readout requirements-only file"),
        ("SRC1482_24_C_parent_schema", C_PARENT_SCHEMA, "C_parent import schema"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, usage in local_sources:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": source_id,
                "path_or_url": rel(source_path),
                "source_kind": "local_file",
                "exists_or_resolved": source_path.exists(),
                "usage": usage,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def web_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "candidate_id": "WEB1482_0_CNES_project",
            "url": "https://cnes.fr/en/projects/microscope",
            "source_kind": "official_mission_page",
            "relevant_fact": "mission context: completed MICROSCOPE mission, 10^-15 target precision, Ti/Pt and PtRh test masses",
            "usable_as_array_source": False,
            "current_status": "SOURCE_FACTS_ONLY_NO_ARRAY_PACKAGE",
            "next_action": "keep as provenance context; do not parse as K_CMSM arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "candidate_id": "WEB1482_1_CQG_arxiv",
            "url": "https://arxiv.org/abs/2209.15488",
            "source_kind": "primary_analysis_paper",
            "relevant_fact": "MICROSCOPE final WEP-analysis paper with eta formula, 19 segments, X-axis model, masks/systematics discussion",
            "usable_as_array_source": False,
            "current_status": "MODEL_STRUCTURE_AND_FACTS_ONLY_NO_MACHINE_ARRAYS",
            "next_action": "use for schema anchors; still need official local arrays/design matrix",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "candidate_id": "WEB1482_2_PRL_arxiv",
            "url": "https://arxiv.org/abs/2209.15487",
            "source_kind": "primary_result_paper",
            "relevant_fact": "final eta(Ti,Pt) result and mission summary",
            "usable_as_array_source": False,
            "current_status": "BOUND_RESULT_ONLY_NOT_READOUT_KERNEL",
            "next_action": "use as bound/provenance source only; never invert into C_parent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "candidate_id": "WEB1482_3_CQG_pdf",
            "url": "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf",
            "source_kind": "primary_analysis_pdf",
            "relevant_fact": "paper states measured accelerations, attitude timestamps, satellite position/velocity, glitches, model terms",
            "usable_as_array_source": False,
            "current_status": "PAPER_TEXT_ONLY_NO_LOCAL_CMSM_EXPORT",
            "next_action": "extract schema/requirements only unless an official data package appears",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def directory_rows() -> list[dict[str, Any]]:
    directories = [
        ("DIR1482_0_root", MICROSCOPE, "MICROSCOPE intake root"),
        ("DIR1482_1_raw", MICROSCOPE / "raw", "unmodified official download package files"),
        ("DIR1482_2_docs", MICROSCOPE / "docs", "official manuals/data dictionaries/licence notes"),
        ("DIR1482_3_metadata", MICROSCOPE / "metadata", "schemas/provenance/validation outputs"),
        ("DIR1482_4_derived", MICROSCOPE / "derived", "future reproducible derived products"),
        ("DIR1482_5_quarantine", MICROSCOPE / "quarantine", "local files not accepted for claim"),
        ("DIR1482_6_official_readout", MICROSCOPE / "official_readout", "K_CMSM/readout arrays or requirements"),
        ("DIR1482_7_source_worldtube", MICROSCOPE / "source_worldtube", "Earth/source profile weighting"),
        ("DIR1482_8_product_convention", MICROSCOPE / "product_convention", "eta/product/readout convention"),
        ("DIR1482_9_branch_classifier", MICROSCOPE / "branch_classifier", "same-branch guard"),
        ("DIR1482_10_branch_readout", MICROSCOPE / "branch_locked_wep" / "readout", "branch-locked readout status rows"),
        ("DIR1482_11_branch_source", MICROSCOPE / "branch_locked_wep" / "source", "branch-locked source status rows"),
        ("DIR1482_12_branch_product", MICROSCOPE / "branch_locked_wep" / "product", "branch-locked product status rows"),
        ("DIR1482_13_branch_coefficients", MICROSCOPE / "branch_locked_wep" / "coefficients", "C_parent import/schema rows"),
    ]
    rows: list[dict[str, Any]] = []
    for directory_id, directory_path, purpose in directories:
        directory_path.mkdir(parents=True, exist_ok=True)
        count = file_count(directory_path)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "directory_id": directory_id,
                "absolute_path": str(directory_path),
                "purpose": purpose,
                "exists": directory_path.exists(),
                "file_count": count,
                "claim_usable_file_count": 0,
                "current_status": "DIRECTORY_READY_REQUIREMENTS_OR_GUARDS_ONLY" if count else "DIRECTORY_READY_FILES_PENDING",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def manifest_rows() -> list[dict[str, Any]]:
    targets = [
        (
            "MAN1482_0_live_readout",
            "official_readout",
            READOUT_LIVE,
            "P_WEP_K_CMSM_readout.csv",
            "official/exported or reproducibly generated K_CMSM/readout matrix with time, session, orbit, axis, gx/gz/Sxx/Sxz, masks, units, source path",
            READOUT_LIVE.exists(),
            "MISSING_REQUIRED_LIVE_FILE",
            "K_CMSM/tau_WEP readout kernel",
        ),
        (
            "MAN1482_1_readout_requirements",
            "official_readout_requirements",
            READOUT_REQUIREMENTS,
            "P_WEP_K_CMSM_readout_REQUIREMENTS.csv",
            "requirements-only scaffold; not a readout matrix",
            READOUT_REQUIREMENTS.exists(),
            "EXISTS_REQUIREMENTS_ONLY_NONCLAIM",
            "schema/provenance gate only",
        ),
        (
            "MAN1482_2_source_worldtube",
            "source_worldtube",
            SOURCE_WORLDTUBE_LIVE,
            "P_WEP_R_source_Earth_worldtube.csv",
            "Earth/source stress profile and orbit shell weighting in observed local frame",
            SOURCE_WORLDTUBE_LIVE.exists(),
            "MISSING_REQUIRED_LIVE_FILE",
            "R_source source leg",
        ),
        (
            "MAN1482_3_product_convention",
            "product_convention",
            PRODUCT_LIVE,
            "P_WEP_eta_product_convention.csv",
            "eta/product convention with official sign, units, source/readout/orbit average rule",
            PRODUCT_LIVE.exists(),
            "EXISTS_PARTIAL_PENDING_NONCLAIM",
            "tau_eff convention and sign",
        ),
        (
            "MAN1482_4_branch_classifier",
            "branch_classifier",
            BRANCH_LIVE,
            "P_WEP_same_parent_branch_lock.csv",
            "same-parent-branch anti-mixing guard",
            BRANCH_LIVE.exists(),
            "EXISTS_GUARD_NONCLAIM",
            "anti-branch-mixing gate",
        ),
        (
            "MAN1482_5_full_material_tensor",
            "material_tensor",
            FULL_MATERIAL_TENSOR,
            "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
            "full MTS material response tensor in same branch",
            FULL_MATERIAL_TENSOR.exists(),
            "MISSING_REQUIRED_LIVE_FILE",
            "R_material tensor",
        ),
        (
            "MAN1482_6_C_parent_import",
            "C_parent",
            C_PARENT_IMPORT,
            "C_parent_WEP_slot_import.csv",
            "parent action/theorem-signed WEP coefficient or DERIVED_ZERO proof",
            C_PARENT_IMPORT.exists(),
            "MISSING_REQUIRED_LIVE_FILE",
            "C_parent coupling slot",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for manifest_id, pack_item, target_path, file_name, expectation, exists, status, used_for in targets:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "manifest_id": manifest_id,
                "pack_item": pack_item,
                "target_path": str(target_path),
                "expected_file": file_name,
                "file_expectation": expectation,
                "target_exists": exists,
                "current_status": status,
                "used_for": used_for,
                "promotion_allowed_now": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def acceptance_gate_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    live_readout_ready = any(row["manifest_id"] == "MAN1482_0_live_readout" and row["target_exists"] for row in manifest)
    source_ready = any(row["manifest_id"] == "MAN1482_2_source_worldtube" and row["target_exists"] for row in manifest)
    product_ready = PRODUCT_LIVE.exists() and not text_contains_blocker(PRODUCT_LIVE)
    branch_ready = BRANCH_LIVE.exists() and not text_contains_blocker(BRANCH_LIVE)
    c_parent_ready = C_PARENT_IMPORT.exists() and not text_contains_blocker(C_PARENT_IMPORT)
    gates = [
        ("ACCEPT1482_0_official_arrays", live_readout_ready, "requires live P_WEP_K_CMSM_readout.csv, not requirements-only rows"),
        ("ACCEPT1482_1_source_worldtube", source_ready, "requires live P_WEP_R_source_Earth_worldtube.csv"),
        ("ACCEPT1482_2_product_convention", product_ready, "product row still has pending sign/units/orbit/source fields"),
        ("ACCEPT1482_3_branch_classifier", branch_ready, "branch guard exists but is nonclaim and not a prediction"),
        ("ACCEPT1482_4_C_parent", c_parent_ready, "requires theorem-zero or sourced finite parent coefficient import"),
    ]
    rows: list[dict[str, Any]] = []
    for gate_id, gate_pass, reason in gates:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "gate_id": gate_id,
                "gate_status": "PASS" if gate_pass else "BLOCKED",
                "reason": "accepted" if gate_pass else reason,
                "score_permission": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "ACCEPT1482_5_overall_parser_permission",
            "gate_status": "BLOCKED",
            "reason": "parser cannot evaluate tau_WEP until live readout, source worldtube, product convention, C_parent, material tensor, and branch rows all pass",
            "score_permission": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def parser_precheck_rows() -> list[dict[str, Any]]:
    targets = [
        ("PDR1482_0_live_readout", READOUT_LIVE, "live K_CMSM/readout matrix"),
        ("PDR1482_1_readout_requirements", READOUT_REQUIREMENTS, "requirements scaffold"),
        ("PDR1482_2_source_worldtube", SOURCE_WORLDTUBE_LIVE, "source worldtube matrix"),
        ("PDR1482_3_product_convention", PRODUCT_LIVE, "product convention"),
        ("PDR1482_4_branch_classifier", BRANCH_LIVE, "branch guard"),
        ("PDR1482_5_C_parent_import", C_PARENT_IMPORT, "parent coefficient import"),
        ("PDR1482_6_full_material_tensor", FULL_MATERIAL_TENSOR, "full material tensor"),
    ]
    rows: list[dict[str, Any]] = []
    for dryrun_id, target_path, target_role in targets:
        exists = target_path.exists()
        blocker = text_contains_blocker(target_path)
        if not exists:
            parser_status = "REFUSED_TARGET_ABSENT"
            refusal_reason = "required live target does not exist"
        elif blocker:
            parser_status = "REFUSED_PENDING_OR_NONCLAIM_FIELDS"
            refusal_reason = "target exists but contains pending/missing/nonclaim markers or claim flags false"
        else:
            parser_status = "PASS_STRUCTURE_ONLY_SCORE_STILL_DISABLED"
            refusal_reason = "structure parse only; cross-factor product gates still disabled"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "dryrun_id": dryrun_id,
                "target_role": target_role,
                "target_path": str(target_path),
                "target_exists": exists,
                "parser_status": parser_status,
                "refusal_reason": refusal_reason,
                "score_permission": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def tau_readiness_rows() -> list[dict[str, Any]]:
    components = [
        ("TAU1482_0_formula", "tau_eff_e := branch_locked_orbit_average(K_CMSM * R_source * readout_mask)", "SYMBOLIC_FORMULA_ONLY", "K_CMSM/readout matrix; R_source; masks; orbit weights; units/sign"),
        ("TAU1482_1_K_CMSM", "official readout/design matrix", "MISSING_LIVE_READOUT_MATRIX", "P_WEP_K_CMSM_readout.csv"),
        ("TAU1482_2_source_worldtube", "Earth/source worldtube", "MISSING_SOURCE_WORLDTUBE", "P_WEP_R_source_Earth_worldtube.csv"),
        ("TAU1482_3_product_convention", "eta product convention", "PARTIAL_PENDING_NONCLAIM", "positive axis sign; readout/source units; orbit average rule"),
        ("TAU1482_4_branch_guard", "same-parent branch guard", "GUARD_EXISTS_NONCLAIM", "parent-owned branch proof and all factors in same branch"),
        ("TAU1482_5_C_parent", "parent coupling slot", "MISSING_C_PARENT_IMPORT", "theorem-zero or sourced finite coefficient"),
        ("TAU1482_6_material_tensor", "full material response tensor", "MISSING_FULL_MATERIAL_TENSOR", "not just alloy/proxy rows"),
        ("TAU1482_7_numeric_tau", "tau_eff_e numeric value", "NOT_EVALUATED", "all above factors"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "tau_id": tau_id,
            "object": object_name,
            "current_status": status,
            "missing_for_claim": missing,
            "tau_eff_e_value": "NOT_EVALUATED",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for tau_id, object_name, status, missing in components
    ]


def hom_closure_rows() -> list[dict[str, Any]]:
    clauses = [
        ("HGC1482_0_parent_generate_functor", "ParentGenerate must map parent action data to all admissible source/readout coefficients", "CONTRACT_STATED_NOT_CONSTRUCTED", "construct functor and image/exhaustion proof"),
        ("HGC1482_1_vertical_kernel", "WEP/source vertical generators must lie in the quotient kernel or be parent-signed zero", "UNSIGNED_FOR_WEP_SLOT", "derive V_WEP from parent geometry, not material proxy basis"),
        ("HGC1482_2_no_hidden_source_generator", "there must be no source-only invariant that survives as a hidden Hom coefficient", "BLOCKED_BY_SCALAR_INVARIANT_OBSTRUCTION", "prove target exclusion or admit finite C_parent route"),
        ("HGC1482_3_no_species_prefactor", "species/material prefactors must descend from one source-blind action density line", "CONDITIONAL_TYPING_ONLY", "source-sign the no-source-only prefactor theorem"),
        ("HGC1482_4_readout_closure", "readout/source projection must be silent under quotient-preserving gauge choices", "BLOCKED_BY_MISSING_TAU_READOUT_SOURCE", "derive tau functional or import official source/readout rows"),
        ("HGC1482_5_C_parent_zero", "C_parent_WEP=0 requires a theorem-zero, not a closure preference", "NOT_PROVEN", "do not create zero import"),
        ("HGC1482_6_verdict", "Hom generator closure status", "NOT_CLOSED", "keep finite source coefficient route open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "closure_id": closure_id,
            "clause": clause,
            "current_status": status,
            "claim_effect": "blocks WEP/local-GR promotion",
            "next_action": next_action,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for closure_id, clause, status, next_action in clauses
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rejections = [
        ("REJ1482_0_official_arrays", "MISSING_LIVE_READOUT_MATRIX", "official K_CMSM/readout arrays/design matrix are not locally accepted"),
        ("REJ1482_1_source_worldtube", "MISSING_SOURCE_WORLDTUBE", "Earth/source stress profile and observed-frame weighting are absent"),
        ("REJ1482_2_product", "PENDING_PRODUCT_SIGN_UNITS_ORBIT", "product convention is partial and nonclaim"),
        ("REJ1482_3_tau", "TAU_EFF_NOT_EVALUATED", "tau_eff_e remains symbolic"),
        ("REJ1482_4_C_parent", "MISSING_C_PARENT_IMPORT", "no theorem-zero or finite parent coefficient row exists"),
        ("REJ1482_5_material", "MISSING_FULL_PARENT_MATERIAL_TENSOR", "material context is not a full MTS response tensor"),
        ("REJ1482_6_Hom", "HOM_PARENT_GENERATOR_NOT_CLOSED", "Hom/source coefficient exclusion is not parent-signed"),
        ("REJ1482_7_no_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton claim can be made from 1482"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rejections
    ]


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE1482_0_sources_exist", True, "local source paths and web source strings are recorded"),
        ("GATE1482_1_live_readout_blocked", not READOUT_LIVE.exists(), "live K_CMSM readout target absent"),
        ("GATE1482_2_source_worldtube_blocked", not SOURCE_WORLDTUBE_LIVE.exists(), "live source worldtube target absent"),
        ("GATE1482_3_product_nonclaim", PRODUCT_LIVE.exists() and text_contains_blocker(PRODUCT_LIVE), "product row exists but remains partial/nonclaim"),
        ("GATE1482_4_C_parent_absent", not C_PARENT_IMPORT.exists(), "C_parent import absent"),
        ("GATE1482_5_tau_symbolic", True, "tau_eff_e not evaluated"),
        ("GATE1482_6_Hom_open", True, "Hom generator closure not proven"),
        ("GATE1482_7_claim_false", True, "all generated rows keep claim flags false"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate_pass": gate_pass,
            "detail": detail,
            "claim_effect": "blocks claim" if gate_pass and gate_id != "GATE1482_0_sources_exist" else "provenance-only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate_pass, detail in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1482_0_no_array_fabrication", "do not create live K_CMSM or source-worldtube arrays", "paper/model facts exist but machine arrays/design matrix are not locally sourced", "write requirements/status only"),
        ("DEC1482_1_keep_product_partial", "keep product convention nonclaim", "sign/units/orbit weighting remain pending", "parser refuses WEP score"),
        ("DEC1482_2_keep_Hom_open", "do not close Hom/source coefficient route", "scalar/source generators and C_parent WEP slot are not parent-signed zero", "finite C_parent route remains needed unless proof appears"),
        ("DEC1482_3_next_tau_lock", "next target should lock the symbolic tau functional or acquire real source files", "tau_eff_e is the immediate bridge between MICROSCOPE data and the local branch", "1483 should make the tau functional contract parse-ready without claiming"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "why": why,
            "consequence": consequence,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, why, consequence in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1482_0_1483",
            "next_target": "1483-Y5-R10-RAB-MICROSCOPE-source-file-acquisition-ledger-or-symbolic-tau-functional-lock.md",
            "script": "scripts/Y5_R10_RAB_MICROSCOPE_source_file_acquisition_ledger_or_symbolic_tau_functional_lock.py",
            "objective": "either find/import a real official MICROSCOPE source-file package with provenance, or lock the symbolic tau_eff functional contract tightly enough that future data can drop in without changing theory",
            "include": "source-file acquisition ledger; official package checklist; tau functional columns; readout/source/product/orbit units; no-claim parser precheck; C_parent interaction points",
            "exclude": "GitHub action; formalization-workbench edits; WEP/local-GR claim promotion; fabricated arrays; bound-inverted C_parent",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def all_claim_flags_false(groups: list[list[dict[str, Any]]]) -> bool:
    for group in groups:
        for row in group:
            if str(row.get("valid_for_claim", "False")) != "False":
                return False
            if str(row.get("claim_allowed", "False")) != "False":
                return False
            if str(row.get("valid_prediction_row", "False")) == "True":
                return False
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    web_candidates: list[dict[str, Any]],
    directories: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    hom: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        WEB_CANDIDATES,
        DIRECTORY_STATUS,
        OFFICIAL_MANIFEST_UPDATE,
        ACCEPTANCE_GATE_UPDATE,
        PARSER_PRECHECK,
        TAU_READINESS,
        HOM_CLOSURE,
        REJECTION_LEDGER,
        REDUCTION_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    local_sources_exist = all(row["exists_or_resolved"] for row in sources if row["source_kind"] == "local_file")
    web_sources_recorded = all(row["url"].startswith("https://") for row in web_candidates)
    directories_exist = all(row["exists"] for row in directories)
    live_targets_blocked = all(
        row["current_status"] != "CLAIM_READY"
        and not row["promotion_allowed_now"]
        and not row["valid_for_claim"]
        for row in manifest
    )
    parser_blocked = all(not row["score_permission"] and not row["valid_for_claim"] for row in parser)
    tau_blocked = all(not row["score_ready"] and not row["valid_for_claim"] for row in tau)
    hom_open = any(row["closure_id"] == "HGC1482_6_verdict" and row["current_status"] == "NOT_CLOSED" for row in hom)
    rejection_blocks = len(rejection) >= 8 and all(not row["claim_allowed"] for row in rejection)
    gate_status = all(row["gate_pass"] for row in gates)
    claim_flags_false = all_claim_flags_false([sources, web_candidates, directories, manifest, acceptance, parser, tau, hom, rejection, gates])
    csv_parse_ok = all(path.exists() and parse_csv(path) for path in generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_SOURCE_PACK, QUAR_TAU, BRANCH_READOUT_STATUS, BRANCH_SOURCE_STATUS, BRANCH_PRODUCT_STATUS])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = (
        not any(file_path.stat().st_mtime >= START_TS for file_path in FORMALIZATION.rglob("*") if file_path.is_file())
        if FORMALIZATION.exists()
        else True
    )
    checks = [
        ("VAL1482_0_local_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1482_1_web_sources", web_sources_recorded, "official web source strings recorded"),
        ("VAL1482_2_directories", directories_exist, "MICROSCOPE intake directories exist"),
        ("VAL1482_3_live_targets_blocked", live_targets_blocked, "no live target is claim-ready"),
        ("VAL1482_4_acceptance_blocked", all(row["gate_status"] == "BLOCKED" for row in acceptance if row["gate_id"] != "ACCEPT1482_3_branch_classifier"), "acceptance gates block score paths"),
        ("VAL1482_5_parser_blocked", parser_blocked, "parser precheck refuses WEP score"),
        ("VAL1482_6_tau_blocked", tau_blocked, "tau_eff_e remains symbolic/nonclaim"),
        ("VAL1482_7_Hom_open", hom_open, "Hom parent-generator closure remains open"),
        ("VAL1482_8_rejection_blocks", rejection_blocks, "rejection ledger blocks claim"),
        ("VAL1482_9_reduction_gates", gate_status, "reduction gates encode blockers"),
        ("VAL1482_10_claim_flags_false", claim_flags_false, "all generated prediction/claim flags false"),
        ("VAL1482_11_csv_parse", csv_parse_ok, "all generated 1482 CSVs parse cleanly"),
        ("VAL1482_12_branch_copies", branch_copies, "nonclaim branch/quarantine copies written"),
        ("VAL1482_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1482_14_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1482_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1482 stages MICROSCOPE intake/readout/source gates as nonclaim and keeps Hom closure open",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


def write_doc(
    sources: list[dict[str, Any]],
    web_candidates: list[dict[str, Any]],
    directories: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    hom: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = [
        "# 1482 - MICROSCOPE Official Readout/Source Intake Runner Or Hom Generator Closure",
        "",
        "## Verdict",
        "- The MICROSCOPE branch now has an explicit intake/readout/source gate refresh, but no live `P_WEP_K_CMSM_readout.csv` or `P_WEP_R_source_Earth_worldtube.csv` is claim-ready.",
        "- Product and branch guard rows exist, but they remain nonclaim scaffolds: sign, units, orbit weighting, `C_parent`, source worldtube, and full material tensor are still missing.",
        "- The Hom-generator closure route remains open rather than proven; the local WEP/local-GR branch is still blocked, not dead.",
        "",
        "## Intake Directory Status",
    ]
    lines.extend(markdown_table(directories, ["directory_id", "file_count", "claim_usable_file_count", "current_status"]))
    lines.extend(["", "## Official Manifest Update"])
    lines.extend(markdown_table(manifest, ["manifest_id", "pack_item", "target_exists", "current_status", "used_for"]))
    lines.extend(["", "## Acceptance Gates"])
    lines.extend(markdown_table(acceptance, ["gate_id", "gate_status", "reason", "score_permission"]))
    lines.extend(["", "## Parser Precheck"])
    lines.extend(markdown_table(parser, ["dryrun_id", "target_exists", "parser_status", "refusal_reason"]))
    lines.extend(["", "## Tau Readiness"])
    lines.extend(markdown_table(tau, ["tau_id", "current_status", "missing_for_claim", "tau_eff_e_value"]))
    lines.extend(["", "## Hom Closure Attempt"])
    lines.extend(markdown_table(hom, ["closure_id", "current_status", "next_action"]))
    lines.extend(["", "## Rejection Ledger"])
    lines.extend(markdown_table(rejection, ["rejection_id", "blocking_marker", "reason"]))
    lines.extend(["", "## Reduction Gates"])
    lines.extend(markdown_table(gates, ["gate_id", "gate_pass", "detail", "claim_effect"]))
    lines.extend(["", "## Decision Ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.extend(["", "## Validation"])
    lines.extend(markdown_table(validation, ["check_id", "result", "detail"]))
    lines.extend(["", "## Official Web Source Candidates"])
    lines.extend(markdown_table(web_candidates, ["candidate_id", "url", "current_status", "next_action"]))
    lines.extend(["", "## Source Register"])
    lines.extend(markdown_table(sources, ["source_id", "exists_or_resolved", "path_or_url", "usage"]))
    lines.extend(["", "## Next Target"])
    lines.extend(markdown_table(next_target, ["next_id", "next_target", "script", "objective"]))
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_status_files() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OFFICIAL_MANIFEST_UPDATE, QUAR_SOURCE_PACK)
    shutil.copyfile(TAU_READINESS, QUAR_TAU)
    shutil.copyfile(PARSER_PRECHECK, BRANCH_READOUT_STATUS)
    shutil.copyfile(ACCEPTANCE_GATE_UPDATE, BRANCH_SOURCE_STATUS)
    shutil.copyfile(OFFICIAL_MANIFEST_UPDATE, BRANCH_PRODUCT_STATUS)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    web_candidates = web_candidate_rows()
    directories = directory_rows()
    manifest = manifest_rows()
    acceptance = acceptance_gate_rows(manifest)
    parser = parser_precheck_rows()
    tau = tau_readiness_rows()
    hom = hom_closure_rows()
    rejection = rejection_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(WEB_CANDIDATES, web_candidates)
    write_csv(DIRECTORY_STATUS, directories)
    write_csv(OFFICIAL_MANIFEST_UPDATE, manifest)
    write_csv(ACCEPTANCE_GATE_UPDATE, acceptance)
    write_csv(PARSER_PRECHECK, parser)
    write_csv(TAU_READINESS, tau)
    write_csv(HOM_CLOSURE, hom)
    write_csv(REJECTION_LEDGER, rejection)
    write_csv(REDUCTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)
    copy_status_files()
    validation = validation_rows(sources, web_candidates, directories, manifest, acceptance, parser, tau, hom, rejection, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, web_candidates, directories, manifest, acceptance, parser, tau, hom, rejection, gates, decisions, validation, next_target)
    print("Y5_R10_1482_MICROSCOPE_intake_gated_nonclaim_Hom_open")


if __name__ == "__main__":
    main()
