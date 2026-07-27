from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2656"
CMSM_DROP = ROOT / "source-intake" / "microscope_cmsm"
WEP_SOURCE_CACHE = ROOT / "source-intake" / "wep-sources" / "1899"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2656-Y5-R2FR-official-MICROSCOPE-readout-data-dry-run-or-source-worldtube-residual-bound.md"

CHECKPOINT = "2656"
BRANCH_ID = "Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656"
PREFIX = "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656"

OFFICIAL_EXTENSIONS = {".csv", ".tsv", ".txt", ".dat", ".nc", ".h5", ".hdf5", ".fits", ".fit", ".parquet", ".json"}
HELPER_PREFIXES = ("README", "TEMPLATE")

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "web_probe": RESIDUALS / f"{PREFIX}_WEB_ACQUISITION_PROBE_NONCLAIM.csv",
    "local_inventory": RESIDUALS / f"{PREFIX}_LOCAL_CMSM_DROP_INVENTORY.csv",
    "official_dryrun": RESIDUALS / f"{PREFIX}_OFFICIAL_READOUT_DATA_DRYRUN.csv",
    "residual_bound_attempt": RESIDUALS / f"{PREFIX}_SOURCE_WORLDTUBE_RESIDUAL_BOUND_ATTEMPT.csv",
    "bound_input_contract": RESIDUALS / f"{PREFIX}_SOURCE_RESIDUAL_BOUND_INPUT_CONTRACT.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_READOUT_BOUND_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_READOUT_BOUND_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2656_MICROSCOPE_READOUT_BOUND_INPUT_CONTRACT_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "WEP_source_worldtube_residual_bound_2656_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "WEP_SOURCE_RESIDUAL_BOUND_2656_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2656_MICROSCOPE_READOUT_DRYRUN.csv",
    "quarantine": QUARANTINE / "P8_Y5_2656_READOUT_BOUND_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2655_doc": {
        "path": ROOT / "2655-Y5-R2FR-WEP-source-worldtube-point-source-reduction-or-official-readout-data-runner.md",
        "needles": ["PSR2655_6_verdict", "ODT2655_3_official_arrays", "NEXT2655_0_selected", "VAL2655_OVERALL"],
        "role": "immediate handoff selecting readout dry-run/source residual bound",
    },
    "1901_doc": {
        "path": ROOT / "1901-Y5-R2FR-measured-G-common-mode-guard-or-source-vector-fill.md",
        "needles": ["GMG1901_5_verdict", "SVF1901_6_verdict", "VAL1901_OVERALL"],
        "role": "measured-G anti-hiding guard and source-vector fallback",
    },
    "1071_doc": {
        "path": ROOT / "1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md",
        "needles": ["KER1071_6_verdict", "TAU1071_3_verdict", "SUEP1071_210"],
        "role": "kernel skeleton, SUEP segment table and numeric tau gap",
    },
    "1075_doc": {
        "path": ROOT / "1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md",
        "needles": ["DMROW1075_000", "TAUSHAPE1075_2_physics_tau", "RG1075_0_official_arrays"],
        "role": "surrogate design matrix and surrogate-as-official refusal",
    },
    "1084_doc": {
        "path": ROOT / "1084-Y5-R10-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate.md",
        "needles": ["RIG1084_0_CMSM_arrays", "RIG1084_2_surrogate_limit", "NEXT1084_0_1085"],
        "role": "readout import gate and profile weighting gap",
    },
    "1424_doc": {
        "path": ROOT / "1424-Y5-R10-RAB-parent-TiPt-source-vector-map-or-official-CMSM-import-lock.md",
        "needles": ["LOCK1424_0_CMSM_schema", "SRCMAP1424_3_K_CMSM", "WEX1424_4_product"],
        "role": "official CMSM import lock and parent-map caveat",
    },
}

WEB_PROBES = [
    {
        "probe_id": "WEBP2656_0_arxiv_data_processing",
        "source_url": "https://arxiv.org/abs/2201.10841",
        "source_label": "MICROSCOPE Mission scenario, ground segment and data processing",
        "observed_role": "mission/data-processing paper and CMSM provenance",
        "machine_readable_arrays_found": False,
        "status": "PUBLIC_DOC_SOURCE_ONLY_NOT_ARRAYS",
    },
    {
        "probe_id": "WEBP2656_1_final_results_arxiv",
        "source_url": "https://arxiv.org/abs/2209.15487",
        "source_label": "MICROSCOPE mission final WEP result",
        "observed_role": "final-result/bound provenance",
        "machine_readable_arrays_found": False,
        "status": "BOUND_PROVENANCE_ONLY_NOT_READOUT_ARRAYS",
    },
    {
        "probe_id": "WEBP2656_2_HAL_processing",
        "source_url": "https://hal.science/hal-03564498/document",
        "source_label": "HAL mirror of data-processing paper",
        "observed_role": "candidate PDF source; local cached fetch is bot-check HTML",
        "machine_readable_arrays_found": False,
        "status": "PUBLIC_DOC_OR_BOTCHECK_NOT_ARRAY_EXPORT",
    },
    {
        "probe_id": "WEBP2656_3_CNES_project_page",
        "source_url": "https://cnes.fr/en/projects/microscope",
        "source_label": "CNES MICROSCOPE project page",
        "observed_role": "mission overview/provenance",
        "machine_readable_arrays_found": False,
        "status": "MISSION_PAGE_NOT_ARRAY_EXPORT",
    },
    {
        "probe_id": "WEBP2656_4_ONERA_press_page",
        "source_url": "https://onera.fr/en/presse/communiques-presse/final-results-of-microscope-mission-achieve-record-levels-of-precision",
        "source_label": "ONERA final-results press page",
        "observed_role": "public final-result context",
        "machine_readable_arrays_found": False,
        "status": "PRESS_PAGE_NOT_ARRAY_EXPORT",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH, CMSM_DROP]:
        path.parent.mkdir(parents=True, exist_ok=True)
    CMSM_DROP.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def file_magic(path: Path, size: int = 8) -> str:
    if not path.exists() or not path.is_file():
        return ""
    with path.open("rb") as handle:
        return handle.read(size).decode("latin1", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2656_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def web_probe_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            **row,
            "claim_use": "source/provenance ledger only",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in WEB_PROBES
    ]


def classify_cmsm_file(path: Path) -> str:
    name_upper = path.name.upper()
    if any(name_upper.startswith(prefix) for prefix in HELPER_PREFIXES):
        return "HELPER_OR_TEMPLATE_NOT_DATA"
    if path.suffix.lower() not in OFFICIAL_EXTENSIONS:
        return "UNRECOGNIZED_EXTENSION_NOT_ACCEPTED_FOR_DRYRUN"
    return "CANDIDATE_ARRAY_FILE_REQUIRES_SCHEMA_VALIDATION"


def local_inventory_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    files = sorted(CMSM_DROP.rglob("*")) if CMSM_DROP.exists() else []
    for path in files:
        if not path.is_file():
            continue
        status = classify_cmsm_file(path)
        rows.append(
            {
                "inventory_id": f"LCI2656_{len(rows):03d}",
                "path": str(path),
                "name": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "file_magic": file_magic(path),
                "classification": status,
                "candidate_official_array": status == "CANDIDATE_ARRAY_FILE_REQUIRES_SCHEMA_VALIDATION",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    if not rows:
        rows.append(
            {
                "inventory_id": "LCI2656_EMPTY",
                "path": str(CMSM_DROP),
                "name": "NO_FILES",
                "extension": "",
                "size_bytes": 0,
                "file_magic": "",
                "classification": "DROP_FOLDER_EMPTY",
                "candidate_official_array": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def official_array_candidates(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in inventory if row["candidate_official_array"]]


def official_dryrun_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidate_count = len(official_array_candidates(inventory))
    return [
        {
            "dryrun_id": "ODR2656_0_schema_contract",
            "object": "official MICROSCOPE CMSM/readout export",
            "required_content": "time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, orbit/attitude convention, units and checksum/manifest",
            "current_evidence": "1424/1084/1071 contracts plus local drop-folder template",
            "current_status": "SCHEMA_CONTRACT_STAGED",
            "blocks_claim": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "ODR2656_1_local_inventory",
            "object": "local CMSM drop folder",
            "required_content": "at least one candidate official array file with recognized data extension and non-template name",
            "current_evidence": f"candidate_array_files={candidate_count}; folder={CMSM_DROP}",
            "current_status": "NO_OFFICIAL_ARRAY_CANDIDATES_FOUND" if candidate_count == 0 else "CANDIDATE_FILES_REQUIRE_SCHEMA_VALIDATION",
            "blocks_claim": candidate_count == 0,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "ODR2656_2_web_probe",
            "object": "web-facing MICROSCOPE sources",
            "required_content": "machine-readable arrays or official archive/schema, not only papers/pages",
            "current_evidence": "arXiv/HAL/CNES/ONERA sources provide papers/mission context; no machine-readable array export identified in this pass",
            "current_status": "PUBLIC_DOCS_FOUND_ARRAY_EXPORT_NOT_FOUND",
            "blocks_claim": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "ODR2656_3_surrogate_lock",
            "object": "surrogate design matrix",
            "required_content": "proof of equivalence to official arrays before any physical tau_WEP use",
            "current_evidence": "1075 surrogate matrix exists but is explicitly SURROGATE_ONLY",
            "current_status": "SURROGATE_AVAILABLE_NONCLAIM_NOT_OFFICIAL",
            "blocks_claim": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "ODR2656_4_botcheck_lock",
            "object": "HAL/local cached candidate PDFs",
            "required_content": "valid PDF/data magic; bot-check HTML cannot be data",
            "current_evidence": "2655/2654 caches include bot-check HTML for HAL candidates",
            "current_status": "BOTCHECK_HTML_REJECTED_AS_DATA",
            "blocks_claim": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "ODR2656_5_verdict",
            "object": "official readout data dry-run",
            "required_content": "complete array/schema/manifest pack or validated exact reconstruction",
            "current_evidence": "local folder has helper/template files only and web probe did not identify an array export",
            "current_status": "OFFICIAL_MICROSCOPE_READOUT_DRYRUN_BLOCKED_NONCLAIM",
            "blocks_claim": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def residual_bound_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "SRB2656_0_target",
            "claim_piece": "finite source-worldtube residual bound",
            "formal_statement": "Replace the point-source shortcut by an inequality bounding eta_res from the difference between the true source/readout worldtube kernel and the calibrated common-mode monopole kernel.",
            "status": "TARGET_SHARP",
            "derivation_or_gap": "this is the mathematically honest way to approach local GR/Newton reduction without pretending Earth/source structure vanishes",
            "source_anchor": "2655:PSL2655_6_acceptance;1901:GMG1901_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "SRB2656_1_operator_decomposition",
            "claim_piece": "kernel residual decomposition",
            "formal_statement": "Let K_true = K_CM + deltaK_source + deltaK_multipole + deltaK_readout + deltaK_frame. Then |eta_res| <= ||DeltaR_TiPt|| ||C_parent|| ||R_source|| ||deltaK_total|| plus declared tau_WEP normalization error.",
            "status": "FORMAL_INEQUALITY_DERIVED",
            "derivation_or_gap": "triangle inequality and operator norm bookkeeping are valid, but every norm must be parent/data sourced before scoring",
            "source_anchor": "1424:SRCMAP1424_0_R_source through SRCMAP1424_4_calibration_guard;1071:KER1071_6_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "SRB2656_2_common_mode_limit",
            "claim_piece": "Newton/GR common-mode limit",
            "formal_statement": "If C_parent has no relative matter/source component and deltaK_total is universal/common-mode, the residual contributes no differential WEP signal after the measured-G guard.",
            "status": "EXACT_CONDITIONAL_ZERO",
            "derivation_or_gap": "this is a clean GR-like reduction condition; MTS still lacks parent-signed no relative component/source-label forgetting",
            "source_anchor": "1901:GMG1901_1_algebraic_absorption;1450 common-mode guard",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "SRB2656_3_shell_point_source_warning",
            "claim_piece": "spherical/point-source shortcut limit",
            "formal_statement": "A shell/Gauss point-source theorem is exact only for the universal exterior monopole; non-spherical, profile-weighted or composition-relative source charges must be bounded, not erased.",
            "status": "POINT_SOURCE_SHORTCUT_REJECTED_FOR_RELATIVE_CHANNELS",
            "derivation_or_gap": "MICROSCOPE altitude is not a magic small-parameter proof; source composition, multipoles, masks and readout frame still matter",
            "source_anchor": "2655:PSR2655_3_source_composition_profile;1071:EXT1071_7_suep_segment_table",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "SRB2656_4_bound_target",
            "claim_piece": "WEP tolerance target",
            "formal_statement": "|eta_res| must be below the MICROSCOPE Ti/Pt bound envelope only after the residual product is expressed in dimensionless eta units with source, material, parent coupling, readout and tau_WEP factors.",
            "status": "BOUND_TARGET_DECLARED_NOT_NUMERIC",
            "derivation_or_gap": "the 2.8e-15 bound is a target; it is not a prediction and cannot close missing C_parent/R_source/R_material/K_CMSM/tau_WEP",
            "source_anchor": "1080:BOUND1080_0_MICROSCOPE_WEP_source_charge;2655:ODT2655_0_bound_pdf",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "SRB2656_5_verdict",
            "claim_piece": "source-worldtube residual bound closes point-source branch",
            "formal_statement": "Current MTS corpus supplies a numeric or theorem-zero finite source-worldtube residual bound strong enough to legalize the point-source WEP branch.",
            "status": "SOURCE_WORLDTUBE_RESIDUAL_BOUND_NOT_NUMERICALLY_CLOSED",
            "derivation_or_gap": "the operator inequality is useful, but C_parent, source vector/profile, material tensor, K_CMSM, tau_WEP and numeric residual norms remain missing or nonclaim",
            "source_anchor": "SRB2656_0_target through SRB2656_4_bound_target",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def bound_input_contract_rows() -> list[dict[str, Any]]:
    return [
        {"input_id": "BIC2656_0_eta_bound", "input": "MICROSCOPE Ti/Pt eta bound", "required_form": "dimensionless bound/provenance only", "current_artifact": str(WEP_SOURCE_CACHE / "MICROSCOPE_final_results_arxiv_2209_15487.pdf"), "current_status": "SOURCE_PDF_CACHED_BOUND_ANCHOR_ONLY", "units": "dimensionless eta", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"input_id": "BIC2656_1_C_parent", "input": "parent coupling/operator coefficient", "required_form": "parent-owned C_parent or theorem-zero relative coupling", "current_artifact": "MISSING", "current_status": "MISSING_PARENT_COUPLING_OWNER", "units": "declared parent/source units", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"input_id": "BIC2656_2_R_source", "input": "Earth/source vector and profile", "required_form": "profile/worldtube-weighted source vector in same parent basis, or common-mode zero theorem", "current_artifact": "MISSING", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "units": "dimensionless source vector or normalized kernel", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"input_id": "BIC2656_3_R_material", "input": "TA6V-PtRh10 material response tensor", "required_form": "full material response tensor to parent residual basis", "current_artifact": "MISSING", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "units": "dimensionless sensitivities per basis component", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"input_id": "BIC2656_4_K_CMSM", "input": "official MICROSCOPE readout kernel", "required_form": "official arrays or validated exact reconstruction with masks/orbit/attitude/units", "current_artifact": str(CMSM_DROP), "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "units": "time, m s^-2, s^-2 and dimensionless kernel columns", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"input_id": "BIC2656_5_deltaK_norms", "input": "finite source/readout residual norms", "required_form": "numeric operator norm bounds for source profile, multipoles, readout frame and masks", "current_artifact": "MISSING", "current_status": "MISSING_RESIDUAL_NORM_BOUNDS", "units": "dimensionless eta contribution or declared kernel norm", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"input_id": "BIC2656_6_tau_WEP", "input": "tau_WEP projection/contraction normalization", "required_form": "derived/sourced tau_WEP or retained nuisance prior; tau=1 shortcut forbidden", "current_artifact": "MISSING", "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED", "units": "dimensionless", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
        {"input_id": "BIC2656_7_acceptance", "input": "source-worldtube residual bound product", "required_form": "all factors sourced/zeroed and no-cancellation absolute envelope below eta bound", "current_artifact": "NONCLAIM_CONTRACT_ONLY", "current_status": "RESIDUAL_BOUND_PRODUCT_NOT_EXECUTABLE", "units": "dimensionless eta envelope", "blocks_claim": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY2656_0_no_official_arrays", "official_arrays": False, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": False, "source_vector": False, "material_tensor": False, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_OFFICIAL_ARRAYS_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2656_1_template_only", "official_arrays": False, "template_only": True, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": False, "source_vector": False, "material_tensor": False, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_TEMPLATE_ONLY_NOT_DATA", "valid_for_claim": False},
        {"case_id": "DRY2656_2_surrogate", "official_arrays": False, "template_only": False, "surrogate_as_official": True, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": False, "source_vector": False, "material_tensor": False, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_SURROGATE_AS_OFFICIAL", "valid_for_claim": False},
        {"case_id": "DRY2656_3_botcheck", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": True, "bound_inequality_only": False, "c_parent": False, "source_vector": False, "material_tensor": False, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_BOTCHECK_HTML_AS_DATA", "valid_for_claim": False},
        {"case_id": "DRY2656_4_inequality_only", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": True, "c_parent": False, "source_vector": False, "material_tensor": False, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_INEQUALITY_ONLY_MISSING_NUMERIC_FACTORS", "valid_for_claim": False},
        {"case_id": "DRY2656_5_parent_coupling", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": False, "source_vector": True, "material_tensor": True, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_PARENT_COUPLING_OWNER_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2656_6_source_vector", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": True, "source_vector": False, "material_tensor": True, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_SOURCE_VECTOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2656_7_material_tensor", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": True, "source_vector": True, "material_tensor": False, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "REFUSED_MATERIAL_TENSOR_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2656_8_tau_unity", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": True, "source_vector": True, "material_tensor": True, "tau_wep_unity": True, "uses_cancellation": False, "expected_status": "REFUSED_TAU_WEP_UNITY_SHORTCUT", "valid_for_claim": False},
        {"case_id": "DRY2656_9_cancellation", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": True, "source_vector": True, "material_tensor": True, "tau_wep_unity": False, "uses_cancellation": True, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
        {"case_id": "DRY2656_10_counterfactual", "official_arrays": True, "template_only": False, "surrogate_as_official": False, "botcheck_as_data": False, "bound_inequality_only": False, "c_parent": True, "source_vector": True, "material_tensor": True, "tau_wep_unity": False, "uses_cancellation": False, "expected_status": "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM", "valid_for_claim": False},
    ]


def evaluate_dryrun(row: dict[str, Any]) -> str:
    if row["template_only"]:
        return "REFUSED_TEMPLATE_ONLY_NOT_DATA"
    if row["surrogate_as_official"]:
        return "REFUSED_SURROGATE_AS_OFFICIAL"
    if not row["official_arrays"]:
        return "REFUSED_OFFICIAL_ARRAYS_MISSING"
    if row["botcheck_as_data"]:
        return "REFUSED_BOTCHECK_HTML_AS_DATA"
    if row["bound_inequality_only"]:
        return "REFUSED_INEQUALITY_ONLY_MISSING_NUMERIC_FACTORS"
    if not row["c_parent"]:
        return "REFUSED_PARENT_COUPLING_OWNER_MISSING"
    if not row["source_vector"]:
        return "REFUSED_SOURCE_VECTOR_MISSING"
    if not row["material_tensor"]:
        return "REFUSED_MATERIAL_TENSOR_MISSING"
    if row["tau_wep_unity"]:
        return "REFUSED_TAU_WEP_UNITY_SHORTCUT"
    if row["uses_cancellation"]:
        return "REFUSED_CANCELLATION_ONLY"
    return "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "case_id": row["case_id"],
            "computed_status": evaluate_dryrun(row),
            "expected_status": row["expected_status"],
            "status_match": evaluate_dryrun(row) == row["expected_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2656_0_official_arrays", "condition": "official MICROSCOPE readout arrays are locally available and schema-validated", "current_status": "FAIL_OFFICIAL_ARRAYS_NOT_IMPORTED", "source_anchor": f"{OUTPUTS['official_dryrun'].name}:ODR2656_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2656_1_residual_bound", "condition": "source-worldtube residual inequality has numeric/theorem-zero factors", "current_status": "FAIL_SOURCE_WORLDTUBE_RESIDUAL_BOUND_NOT_NUMERICALLY_CLOSED", "source_anchor": f"{OUTPUTS['residual_bound_attempt'].name}:SRB2656_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2656_2_bound_inputs", "condition": "C_parent, source vector, material tensor, K_CMSM, deltaK norms and tau_WEP are filled or theorem-zero", "current_status": "FAIL_RESIDUAL_BOUND_PRODUCT_NOT_EXECUTABLE", "source_anchor": f"{OUTPUTS['bound_input_contract'].name}:BIC2656_7_acceptance", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2656_3_no_shortcuts", "condition": "template-only, surrogate, bot-check, inequality-only, tau=1 and cancellation shortcuts are refused", "current_status": "PASS_GUARDS_ENFORCED_BUT_NONCLAIM", "source_anchor": OUTPUTS["dryrun_results"].name, "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2656_4_verdict", "condition": "WEP source-worldtube residual branch can support local-GR/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG2656_0_official_arrays through CG2656_3_no_shortcuts", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2656_0_data", "decision": "DO_NOT_RUN_OFFICIAL_READOUT_SCORE", "reason": "local CMSM drop folder has helper/template files only; web-facing public sources found in this pass are documents/pages, not machine-readable arrays", "status": "OFFICIAL_DATA_ROUTE_BLOCKED_NONCLAIM", "next_dependency": "user-supplied official CMSM export or independently validated reconstruction", "valid_for_claim": False},
        {"decision_id": "DEC2656_1_bound", "decision": "KEEP_SOURCE_RESIDUAL_BOUND_AS_FORMAL_CONTRACT", "reason": "the operator-norm inequality is valid as a contract, but no numeric residual envelope exists without C_parent/source/material/K_CMSM/tau inputs", "status": "RESIDUAL_BOUND_CONTRACT_STAGED_NONCLAIM", "next_dependency": "parent coupling/material/source contraction theorem or source-backed coefficient pack", "valid_for_claim": False},
        {"decision_id": "DEC2656_2_next", "decision": "SELECT_2657_PARENT_COUPLING_SOURCE_CONTRACTION_THEOREM", "reason": "official data cannot create a prediction; the leap forward is to derive or bound the parent coupling/source/material contraction that would make any readout meaningful", "status": "NEXT_TARGET_SELECTED", "next_dependency": "2657 parent coupling/source contraction zero theorem or finite coefficient pack", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2656_0_selected",
            "status": "selected",
            "next_doc": "2657-Y5-R2FR-parent-coupling-source-material-contraction-zero-or-finite-WEP-coefficient-pack.md",
            "next_script": "scripts/Y5_R2FR_parent_coupling_source_material_contraction_zero_or_finite_WEP_coefficient_pack_2657.py",
            "target": "Try to derive the parent coupling/source/material contraction zero theorem that would make WEP local-GR reduction legal; if it fails, stage finite WEP coefficient rows with explicit units and no claim.",
            "must_include": "C_parent owner; source vector/profile; material tensor; K_CMSM side gate; tau_WEP dependency; no measured-G hiding; no cancellation; finite coefficient pack if theorem fails",
            "must_exclude": "GitHub action, formalization-workbench edits, official arrays as parent ontology, tau_WEP=1, bound-only WEP claim, surrogate readout as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT2656_0_data", "area": "MICROSCOPE official readout", "summary": "the local drop folder contains only helper/template files, and public web sources found are documents rather than array exports", "risk_level": "DATA_ROUTE_BLOCKED_UNTIL_EXPORT", "project_meaning": "we cannot accidentally score the WEP branch from fake arrays or a paper PDF", "next_action": "wait for official export or validated reconstruction; keep deriving meanwhile", "valid_for_claim": False},
        {"status_id": "STAT2656_1_theory", "area": "source-worldtube residual bound", "summary": "a real operator-norm contract is now staged: eta_res is bounded by parent coupling, source, material, readout and tau factors", "risk_level": "FORMAL_CONTRACT_PROGRESS_INPUTS_MISSING", "project_meaning": "this turns the point-source argument from handwave into an auditable theorem target", "next_action": "derive the parent coupling/source/material contraction theorem", "valid_for_claim": False},
        {"status_id": "STAT2656_2_project_overview", "area": "GR/Newton reduction bridge", "summary": "the branch has moved away from data-polishing and back to the right derivation choke point: parent coupling/source/material contraction", "risk_level": "GOOD_HARD_PROBLEM", "project_meaning": "the path is still alive, but the next win must be a theorem or a finite coefficient pack, not another surrogate run", "next_action": "2657 parent coupling contraction zero or finite WEP coefficient pack", "valid_for_claim": False},
    ]


def branch_copy_rows(dryrun_rows_out: list[dict[str, Any]], bound_rows: list[dict[str, Any]], input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], input_rows)
    write_csv(BRANCH_COPIES["local_bounds"], bound_rows)
    write_csv(BRANCH_COPIES["source_weight"], input_rows)
    write_csv(BRANCH_COPIES["microscope"], dryrun_rows_out)
    write_csv(BRANCH_COPIES["quarantine"], dryrun_rows_out)
    return [
        {"copy_id": copy_id, "path": str(path), "exists": path.exists(), "parseable_csv": path.exists() and len(csv_rows(path)) >= 1, "purpose": "2656 official readout/source residual bound nonclaim handoff", "valid_for_claim": False}
        for copy_id, path in BRANCH_COPIES.items()
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    inventory = local_inventory_rows()
    official = official_dryrun_rows(inventory)
    bound = residual_bound_attempt_rows()
    inputs = bound_input_contract_rows()
    dry_cases = dryrun_case_rows()
    dry = dryrun_result_rows(dry_cases)
    rows = {
        "source_register": source_register_rows(),
        "web_probe": web_probe_rows(),
        "local_inventory": inventory,
        "official_dryrun": official,
        "residual_bound_attempt": bound,
        "bound_input_contract": inputs,
        "dryrun_cases": dry_cases,
        "dryrun_results": dry,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["branch_copies"] = branch_copy_rows(official, bound, inputs)
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2656-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2656*",
        "*Y5_R2FR_official_MICROSCOPE_readout_data_dry_run_or_source_worldtube_residual_bound_2656*",
        "*JR2656*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    web_ok = len(rows["web_probe"]) >= 5 and all(not row["machine_readable_arrays_found"] and not row["valid_for_claim"] for row in rows["web_probe"])
    inventory_ok = len(rows["local_inventory"]) >= 1 and all(not row["valid_for_claim"] for row in rows["local_inventory"])
    no_candidates = len(official_array_candidates(rows["local_inventory"])) == 0
    official_ok = any(row["dryrun_id"] == "ODR2656_5_verdict" and row["current_status"] == "OFFICIAL_MICROSCOPE_READOUT_DRYRUN_BLOCKED_NONCLAIM" for row in rows["official_dryrun"])
    bound_ok = any(row["attempt_id"] == "SRB2656_5_verdict" and row["status"] == "SOURCE_WORLDTUBE_RESIDUAL_BOUND_NOT_NUMERICALLY_CLOSED" for row in rows["residual_bound_attempt"])
    input_ok = any(row["input_id"] == "BIC2656_7_acceptance" and row["current_status"] == "RESIDUAL_BOUND_PRODUCT_NOT_EXECUTABLE" for row in rows["bound_input_contract"]) and all(not row["score_ready"] and not row["valid_prediction_row"] for row in rows["bound_input_contract"])
    dry_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2656_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] for row in rows["claim_gates"])
    next_ok = any("2657-Y5-R2FR-parent-coupling-source-material-contraction" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2656_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2656_01_web_probe", web_ok, "web probe rows record public docs/pages only, not array exports"),
        ("VAL2656_02_local_inventory", inventory_ok and no_candidates, "local CMSM drop folder has no candidate official array files"),
        ("VAL2656_03_official_dryrun", official_ok, "official readout dry-run remains blocked/nonclaim"),
        ("VAL2656_04_residual_bound", bound_ok, "source-worldtube residual inequality is staged but not numerically closed"),
        ("VAL2656_05_bound_inputs", input_ok, "residual-bound input contract is nonclaim/not score-ready"),
        ("VAL2656_06_dryrun", dry_ok, "dry-run refuses missing arrays, template-only, surrogate, bot-check, inequality-only, missing factors, tau=1 and cancellation"),
        ("VAL2656_07_claim_gates_false", claim_ok, "claim remains blocked"),
        ("VAL2656_08_next_target", next_ok, "2657 parent coupling/source/material contraction target is recorded"),
        ("VAL2656_09_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2656_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2656_11_formalization_untouched", formal_ok, "no 2656 outputs are written under formalization-workbench"),
        ("VAL2656_12_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": validation_id, "status": "PASS" if passed else "FAIL", "detail": detail}
        for validation_id, passed, detail in checks
    ]
    out.append(
        {"timestamp_utc": generated, "checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "valid_for_claim": False, "claim_allowed": False, "validation_id": "VAL2656_OVERALL", "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL", "detail": "2656 blocks official-data scoring, stages source-worldtube residual bound contract, and selects parent coupling/source/material contraction next"}
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2656 - Official MICROSCOPE Readout Data Dry-Run Or Source-Worldtube Residual Bound

## Purpose

This checkpoint tests the fork selected by 2655. It checks whether official MICROSCOPE readout data are locally available or web-visible as machine-readable arrays; if not, it derives the exact residual-bound contract that would make the point-source source-worldtube branch legitimate without smuggling in a shortcut.

## Result

- No official MICROSCOPE CMSM/readout arrays are present in the local drop folder; only helper/template files are present.
- Public web-facing sources found in this pass are papers, mission pages, or press/provenance pages, not machine-readable gx/gz/Sxx/Sxz arrays.
- A useful formal inequality is now staged: the source-worldtube residual must be bounded by parent coupling, source vector/profile, material tensor, readout kernel and tau_WEP factors.
- The inequality is not a claim: C_parent, R_source, R_material, K_CMSM, residual norm bounds and tau_WEP remain missing or unsigned.
- The next target is 2657: parent coupling/source/material contraction zero theorem, or a finite WEP coefficient pack.

## Source Register

{markdown_table(rows["source_register"])}

## Web Acquisition Probe

{markdown_table(rows["web_probe"])}

## Local CMSM Drop Inventory

{markdown_table(rows["local_inventory"])}

## Official Readout Data Dry-Run

{markdown_table(rows["official_dryrun"])}

## Source-Worldtube Residual Bound Attempt

{markdown_table(rows["residual_bound_attempt"])}

## Residual Bound Input Contract

{markdown_table(rows["bound_input_contract"])}

## Dry-Run Cases

{markdown_table(rows["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows["dryrun_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
