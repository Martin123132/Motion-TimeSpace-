from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1226"
TITLE = "1226-Y5-R10-MICROSCOPE-readout-source-acquisition-ledger"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PORTAL_PROBE_PATH = OUT_DIR / f"{PACK_ID}_PUBLIC_PORTAL_PROBE.csv"
REQUIRED_OBJECTS_PATH = OUT_DIR / f"{PACK_ID}_REQUIRED_DATA_OBJECTS.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_ACQUISITION_BLOCKER_LEDGER.csv"
NO_SURROGATE_PATH = OUT_DIR / f"{PACK_ID}_NO_SURROGATE_POLICY.csv"
STAGING_MANIFEST_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_STAGING_MANIFEST.csv"
TAU_FEED_PATH = OUT_DIR / f"{PACK_ID}_TAU_WEP_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1226_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1226_0_1225_next",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1225_NEXT_TARGET.csv",
            "needle_or_evidence": "1226-Y5-R10-MICROSCOPE-readout-source-acquisition-ledger.md",
            "purpose": "1225 handoff to MICROSCOPE readout/source acquisition",
        },
        {
            "source_id": "SRC1226_1_1225_acquisition",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
            "needle_or_evidence": "ACQ1225_0_official_readout_arrays",
            "purpose": "tau_WEP required data objects",
        },
        {
            "source_id": "SRC1226_2_1225_formula",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
            "needle_or_evidence": "FORM1225_0_tau_WEP_functional",
            "purpose": "symbolic tau_WEP functional contract",
        },
        {
            "source_id": "SRC1226_3_1084_readout_gate",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle_or_evidence": "RIG1084_0_CMSM_arrays",
            "purpose": "existing readout import gate",
        },
        {
            "source_id": "SRC1226_4_1083_source_vector",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "needle_or_evidence": "SCG1083_0_profile_weighting",
            "purpose": "existing source worldtube/profile weighting gate",
        },
        {
            "source_id": "SRC1226_5_CMSM_portal",
            "source_type": "web",
            "location": "https://cmsm-ds.onera.fr/",
            "needle_or_evidence": "official MICROSCOPE data portal; web probe showed REGARDS OSS landing page, but no package enumeration captured in this run",
            "purpose": "primary public data portal for MICROSCOPE data/documentation",
        },
        {
            "source_id": "SRC1226_6_arxiv_ground_segment",
            "source_type": "web",
            "location": "https://arxiv.org/abs/2201.10841",
            "needle_or_evidence": "mission paper says CNES provided raw data and ONERA provided the Science Mission Centre of MICROSCOPE",
            "purpose": "provenance for CNES/ONERA/CMSM ground segment and data processing",
        },
        {
            "source_id": "SRC1226_7_CNES_project",
            "source_type": "web",
            "location": "https://cnes.fr/en/projects/microscope",
            "needle_or_evidence": "CNES project page identifies MICROSCOPE mission, partners, final results milestone, and Ti/Pt test masses",
            "purpose": "official mission/project provenance",
        },
        {
            "source_id": "SRC1226_8_CQG_result_data_availability",
            "source_type": "web",
            "location": "https://doi.org/10.1088/1361-6382/ac84be",
            "needle_or_evidence": "data availability statement points to https://cmsm-ds.onera.fr/ after embargo",
            "purpose": "published result data-availability provenance",
        },
        {
            "source_id": "SRC1226_9_Moriond_data_available",
            "source_type": "web",
            "location": "https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf",
            "needle_or_evidence": "slides state data and documentation are available at https://cmsm-ds.onera.fr/",
            "purpose": "secondary public pointer to data and documentation portal",
        },
    ]

    source_register = []
    for spec in source_specs:
        if spec["source_type"] == "local":
            path_exists, needle_found = exists_and_contains(spec["location"], spec["needle_or_evidence"])
            absolute_or_url = str(source_path(spec["location"]))
        else:
            path_exists = spec["location"].startswith("http")
            needle_found = bool(spec["needle_or_evidence"])
            absolute_or_url = spec["location"]
        source_register.append(
            {
                **spec,
                "absolute_path_or_url": absolute_or_url,
                "source_recorded": path_exists,
                "evidence_recorded": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    portal_probe = [
        {
            "probe_id": "PORT1226_0_CMSM_landing",
            "url": "https://cmsm-ds.onera.fr/",
            "probe_method": "web_open plus local PowerShell Invoke-WebRequest check",
            "observed_status": "WEB_OPENED_REGARDS_OSS; POWERSHELL_REMOTE_CONNECT_FAILED",
            "package_enumeration_status": "NOT_ENUMERATED",
            "download_status": "NO_DATA_DOWNLOADED",
            "interpretation": "portal exists as the right target, but this run did not obtain a machine-readable package list",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "PORT1226_1_public_literature",
            "url": "https://arxiv.org/abs/2201.10841; https://doi.org/10.1088/1361-6382/ac84be",
            "probe_method": "web search/open of public paper pages and snippets",
            "observed_status": "DATA_PORTAL_PROVENANCE_FOUND",
            "package_enumeration_status": "NO_ARRAY_FILE_NAMES_IDENTIFIED",
            "download_status": "NO_DATA_DOWNLOADED",
            "interpretation": "literature proves where data should be, not the exact file objects needed by tau_WEP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    required_objects = [
        {
            "object_id": "OBJ1226_0_official_CMSM_arrays",
            "tau_WEP_role": "K_eta readout kernel and measured acceleration channel",
            "required_content": "time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, attitude/orbit convention",
            "expected_source": "https://cmsm-ds.onera.fr/",
            "local_status": "NOT_PRESENT_IN_POST_CHECKPOINT_WORK",
            "acquisition_status": "MISSING_PACKAGE_ENUMERATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "object_id": "OBJ1226_1_eta_product_convention",
            "tau_WEP_role": "normalization N_eta from source/material/readout response to reported Eotvos eta",
            "required_content": "data dictionary or analysis documentation defining product normalization and reported eta_AB convention",
            "expected_source": "CMSM documentation or CQG data-analysis documentation",
            "local_status": "NOT_PRESENT_IN_POST_CHECKPOINT_WORK",
            "acquisition_status": "MISSING_DOCUMENT_OBJECT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "object_id": "OBJ1226_2_source_worldtube",
            "tau_WEP_role": "R_source and K_source Earth/source profile weighting",
            "required_content": "Earth/source stress/current profile and orbit-weighted source vector in observed local frame",
            "expected_source": "CMSM source/orbit products plus Earth model documentation",
            "local_status": "NOT_PRESENT_IN_POST_CHECKPOINT_WORK",
            "acquisition_status": "MISSING_SOURCE_PROFILE_OBJECT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "object_id": "OBJ1226_3_orbit_attitude_masks",
            "tau_WEP_role": "orbit/session average and mask operator",
            "required_content": "orbit, attitude, time/session ids, masks, and segment definitions matched to SUEP/SUREF sessions",
            "expected_source": "CMSM mission scenario/data products",
            "local_status": "NOT_PRESENT_IN_POST_CHECKPOINT_WORK",
            "acquisition_status": "MISSING_ORBIT_MASK_OBJECT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "object_id": "OBJ1226_4_TiPt_material_tensor",
            "tau_WEP_role": "R_material(TiPt) response to source-weight channel",
            "required_content": "TA6V minus PtRh10 source-weight response tensor, not only alpha/Coulomb delta-Q",
            "expected_source": "MICROSCOPE material docs plus MTS source-weight convention",
            "local_status": "MATERIAL_PAIR_ONLY",
            "acquisition_status": "MISSING_SOURCE_WEIGHT_TENSOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "object_id": "OBJ1226_5_Delta_w_prior",
            "tau_WEP_role": "finite source-weight amplitude multiplying tau_WEP",
            "required_content": "numeric Delta_w_TiPt prior width or parent theorem-zero proof, same convention as tau_WEP",
            "expected_source": "MTS parent coupling derivation or source-backed finite prior",
            "local_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "acquisition_status": "MISSING_THEORY_OR_PRIOR_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "object_id": "OBJ1226_6_reproducibility_metadata",
            "tau_WEP_role": "schema and provenance for future runner",
            "required_content": "license/access status, file checksums, version/date, units, columns, session coverage, and citation",
            "expected_source": "CMSM portal metadata or manually recorded data dictionary",
            "local_status": "NOT_PRESENT_IN_POST_CHECKPOINT_WORK",
            "acquisition_status": "MISSING_METADATA",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    blockers = [
        {
            "blocker_id": f"BLOCK1226_{index}_{row['object_id'].split('_')[-1]}",
            "object_id": row["object_id"],
            "blocker": row["acquisition_status"],
            "required_resolution": "acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows",
            "claim_effect": "tau_WEP remains SYMBOLIC_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, row in enumerate(required_objects)
        if row["acquisition_status"].startswith("MISSING")
    ]

    no_surrogate_policy = [
        {
            "policy_id": "SURR1226_0_official_arrays_only",
            "forbidden_substitute": "handmade gx/gz/Sxx/Sxz arrays or approximate orbital kernels",
            "allowed_use": "software smoke tests only, labelled surrogate and valid_for_claim=false",
            "claim_rule": "official CMSM/export arrays or exact equivalence proof required",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "policy_id": "SURR1226_1_no_literature_to_arrays",
            "forbidden_substitute": "using published eta result or paper equations as if they were time-series arrays",
            "allowed_use": "provenance, priors, and shape of analysis model",
            "claim_rule": "papers prove the target data exist, not the tau_WEP kernel",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "policy_id": "SURR1226_2_no_tau_unity",
            "forbidden_substitute": "setting tau_WEP=1",
            "allowed_use": "none for claims",
            "claim_rule": "tau_WEP must be evaluated from source/worldtube/readout or theorem-zero",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    staging_manifest = [
        {
            "staging_id": "STAGE1226_0_raw",
            "future_local_path": "source-intake/microscope/raw/",
            "contents": "unmodified official downloaded packages, checksums, and access notes",
            "current_status": "DIRECTORY_NOT_CREATED_NO_DATA_DOWNLOADED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "staging_id": "STAGE1226_1_docs",
            "future_local_path": "source-intake/microscope/docs/",
            "contents": "data dictionaries, CMSM documentation, readout convention notes, license/access metadata",
            "current_status": "DIRECTORY_NOT_CREATED_NO_DOCS_DOWNLOADED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "staging_id": "STAGE1226_2_derived",
            "future_local_path": "source-intake/microscope/derived/",
            "contents": "future tau_WEP derived products generated from raw official objects",
            "current_status": "DIRECTORY_NOT_CREATED_NO_DERIVED_PRODUCTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    tau_feed = [
        {
            "feed_id": "FEED1226_0_to_tau_WEP",
            "target": "FORM1225_0_tau_WEP_functional",
            "update": "public data portal and provenance identified, but no official array package enumerated or downloaded",
            "tau_WEP_status": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_prediction_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1226_1_to_source_weight_product",
            "target": "PROD1224_0_source_weight",
            "update": "source-weight product remains not scoreable because tau_WEP and Delta_w_TiPt are still missing",
            "tau_WEP_status": "NOT_NUMERIC",
            "valid_prediction_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1226_0_portal_found_not_claim",
            "decision": "record CMSM portal as the official acquisition target, not as acquired data",
            "because": "the run found public provenance but did not enumerate or download official packages",
            "next_action": "build a portal/package map or access-blocker probe",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1226_1_no_surrogate",
            "decision": "forbid surrogate arrays for tau_WEP claim",
            "because": "tau_WEP depends on official readout/source/orbit conventions",
            "next_action": "only use surrogate data for smoke tests with valid_for_claim=false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1226_2_data_plumbing_bottleneck",
            "decision": "treat readout/source acquisition as the next bottleneck",
            "because": "the local-GR source-weight branch is now theory-contracted but not empirically scoreable",
            "next_action": "attempt a safe package-map/download dry run into D-drive staging paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1226_0_sources",
            "gate": "local and web source register",
            "status": "PASS",
            "reason": "local sources and public provenance URLs are recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1226_1_portal_enumeration",
            "gate": "CMSM package enumeration",
            "status": "BLOCKED",
            "reason": "portal identified but package list not captured",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1226_2_required_objects",
            "gate": "official readout/source objects acquired",
            "status": "BLOCKED",
            "reason": "all required data objects remain missing/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1226_3_no_surrogate",
            "gate": "no surrogate-as-claim",
            "status": "PASS",
            "reason": "surrogate policy is active and blocks claim promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1226_4_tau_WEP",
            "gate": "tau_WEP numeric/source-backed",
            "status": "BLOCKED",
            "reason": "tau_WEP remains symbolic-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1226_5_local_GR_WEP",
            "gate": "local GR/WEP claim permission",
            "status": "BLOCKED",
            "reason": "1226 is acquisition plumbing only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1226_0_1227",
            "target_file": "1227-Y5-R10-MICROSCOPE-portal-package-map-or-access-blocker.md",
            "target_script": "scripts/Y5_R10_MICROSCOPE_portal_package_map_or_access_blocker.py",
            "task": "attempt a safe CMSM portal/package map and dry-run download plan; if machine access fails, record exact access blockers and manual acquisition instructions",
            "success_condition": "official package names/metadata are mapped or a hard blocker ledger explains why they could not be obtained, with no fabricated data rows",
            "do_not_do": "do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (PORTAL_PROBE_PATH, portal_probe),
        (REQUIRED_OBJECTS_PATH, required_objects),
        (BLOCKER_LEDGER_PATH, blockers),
        (NO_SURROGATE_PATH, no_surrogate_policy),
        (STAGING_MANIFEST_PATH, staging_manifest),
        (TAU_FEED_PATH, tau_feed),
        (DECISION_PATH, decision_rows),
        (CLAIM_GATES_PATH, claim_gates),
        (NEXT_PATH, next_rows),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    validation_rows = []
    local_sources = [row for row in source_register if row["source_type"] == "local"]
    web_sources = [row for row in source_register if row["source_type"] == "web"]
    validation_rows.append(
        validation_row(
            "VAL1226_0_local_sources_exist",
            "all cited local sources exist",
            all(parse_bool(row["source_recorded"]) for row in local_sources),
            f"{sum(1 for row in local_sources if parse_bool(row['source_recorded']))}/{len(local_sources)} local sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_1_local_needles_found",
            "all cited local needles found",
            all(parse_bool(row["evidence_recorded"]) for row in local_sources),
            f"{sum(1 for row in local_sources if parse_bool(row['evidence_recorded']))}/{len(local_sources)} local needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_2_web_sources_recorded",
            "web provenance URLs recorded",
            all(row["location"].startswith("http") and parse_bool(row["evidence_recorded"]) for row in web_sources),
            "; ".join(row["source_id"] for row in web_sources),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_3_required_objects_complete",
            "required tau_WEP objects are listed",
            len(required_objects) == 7,
            "; ".join(row["object_id"] for row in required_objects),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_4_no_fabricated_acquisition",
            "no official data object is falsely acquired",
            all(row["acquisition_status"].startswith("MISSING") for row in required_objects),
            "all required objects remain missing/package-unenumerated",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_5_blockers_materialized",
            "missing objects have blockers",
            len(blockers) == len(required_objects),
            f"blocker_rows={len(blockers)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_6_no_surrogate_policy",
            "surrogate-as-claim policy active",
            all(row["status"] == "ACTIVE" and is_false(row, "claim_allowed") for row in no_surrogate_policy),
            "; ".join(row["policy_id"] for row in no_surrogate_policy),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_7_tau_feed_nonclaim",
            "tau_WEP feed remains nonclaim",
            all(row["valid_prediction_rows_delta"] == 0 and is_false(row, "claim_allowed") for row in tau_feed),
            "valid_prediction_rows_delta=0 for tau/product feeds",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_8_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            any(row["status"] == "BLOCKED" for row in claim_gates) and all(is_false(row, "valid_for_claim") for row in claim_gates),
            "portal/object/tau/local claim gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_9_next_target_package_map",
            "next target stages package map/access blocker",
            next_rows[0]["target_file"] == "1227-Y5-R10-MICROSCOPE-portal-package-map-or-access-blocker.md",
            next_rows[0]["target_file"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1226_10_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
                for _, rows in generated_tables
                for row in rows
                if "valid_for_claim" in row and "claim_allowed" in row
            ),
            "valid_for_claim=false and claim_allowed=false throughout claim-bearing tables",
        )
    )

    csv_parse_details = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            parsed = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAIL:{exc}")
    validation_rows.append(
        validation_row(
            "VAL1226_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(csv_parse_details),
        )
    )

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if modified >= RUN_STARTED_UTC:
                    formalization_recent.append(path)
    validation_rows.append(
        validation_row(
            "VAL1226_12_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1226_13_overall",
            "overall 1226 validation",
            overall_before,
            "1226 identifies official MICROSCOPE acquisition targets and blocks tau_WEP claims until real packages are mapped/acquired",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1226 Y5/R10 MICROSCOPE Readout Source Acquisition Ledger

**Current verdict:** 1226 identifies the official MICROSCOPE/CMSM acquisition target and the exact objects needed for `tau_WEP`, but it does **not** acquire or enumerate official array packages. No data rows are fabricated.

**Main progress:** the bridge from symbolic `tau_WEP` to real data is now concrete: official CMSM arrays, eta product normalization, source worldtube/profile weighting, orbit/attitude/masks, Ti/Pt source-weight tensor, `Delta_w_TiPt`, and metadata are all listed as required objects.

**Practical consequence:** the next move is a safe portal/package map or access-blocker pass. Surrogates can be used only for smoke tests, never for WEP/local-GR claims.

## Source Register

{markdown_table(source_register, ["source_id", "source_type", "location", "needle_or_evidence", "purpose", "absolute_path_or_url", "source_recorded", "evidence_recorded", "valid_for_claim", "claim_allowed"])}

## Public Portal Probe

{markdown_table(portal_probe, ["probe_id", "url", "probe_method", "observed_status", "package_enumeration_status", "download_status", "interpretation", "valid_for_claim", "claim_allowed"])}

## Required Data Objects

{markdown_table(required_objects, ["object_id", "tau_WEP_role", "required_content", "expected_source", "local_status", "acquisition_status", "valid_for_claim", "claim_allowed"])}

## Acquisition Blocker Ledger

{markdown_table(blockers, ["blocker_id", "object_id", "blocker", "required_resolution", "claim_effect", "valid_for_claim", "claim_allowed"])}

## No Surrogate Policy

{markdown_table(no_surrogate_policy, ["policy_id", "forbidden_substitute", "allowed_use", "claim_rule", "status", "valid_for_claim", "claim_allowed"])}

## Local Staging Manifest

{markdown_table(staging_manifest, ["staging_id", "future_local_path", "contents", "current_status", "valid_for_claim", "claim_allowed"])}

## Tau WEP Feed Update

{markdown_table(tau_feed, ["feed_id", "target", "update", "tau_WEP_status", "valid_prediction_rows_delta", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_rows, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows, ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
