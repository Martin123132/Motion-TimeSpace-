from __future__ import annotations

import csv
import socket
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


PACK_ID = "P8_Y5_R10_1227"
TITLE = "1227-Y5-R10-MICROSCOPE-portal-package-map-or-access-blocker"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
NETWORK_PROBE_PATH = OUT_DIR / f"{PACK_ID}_NETWORK_PROBE.csv"
ENDPOINT_CANDIDATES_PATH = OUT_DIR / f"{PACK_ID}_REGARDS_ENDPOINT_CANDIDATES.csv"
PACKAGE_MAP_PATH = OUT_DIR / f"{PACK_ID}_PACKAGE_MAP_STATUS.csv"
ACCESS_BLOCKER_PATH = OUT_DIR / f"{PACK_ID}_ACCESS_BLOCKER_LEDGER.csv"
DOWNLOAD_DRY_RUN_PATH = OUT_DIR / f"{PACK_ID}_DOWNLOAD_DRY_RUN_PLAN.csv"
MANUAL_ACQUISITION_PATH = OUT_DIR / f"{PACK_ID}_MANUAL_ACQUISITION_INSTRUCTIONS.csv"
PARSER_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_FUTURE_PARSER_CONTRACT.csv"
TAU_FEED_PATH = OUT_DIR / f"{PACK_ID}_TAU_WEP_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1227_VALIDATION.csv"


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


def probe_host(url: str, timeout_seconds: float = 5.0) -> dict[str, object]:
    parsed = urlparse(url)
    host = parsed.hostname or url
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        addresses = sorted({info[4][0] for info in infos})
        dns_status = "RESOLVED"
    except OSError as exc:
        return {
            "host": host,
            "port": port,
            "dns_status": "DNS_FAILED",
            "addresses": "",
            "tcp_status": "NOT_ATTEMPTED",
            "error": repr(exc),
        }

    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            tcp_status = "CONNECTED"
            error = ""
    except OSError as exc:
        tcp_status = "CONNECT_FAILED"
        error = repr(exc)

    return {
        "host": host,
        "port": port,
        "dns_status": dns_status,
        "addresses": ";".join(addresses),
        "tcp_status": tcp_status,
        "error": error,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1227_0_1226_next",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1226_NEXT_TARGET.csv",
            "needle_or_evidence": "1227-Y5-R10-MICROSCOPE-portal-package-map-or-access-blocker.md",
            "purpose": "1226 handoff to CMSM package-map/access-blocker target",
        },
        {
            "source_id": "SRC1227_1_1226_required_objects",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1226_REQUIRED_DATA_OBJECTS.csv",
            "needle_or_evidence": "OBJ1226_0_official_CMSM_arrays",
            "purpose": "required official MICROSCOPE/tau_WEP data objects",
        },
        {
            "source_id": "SRC1227_2_1226_portal_probe",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1226_PUBLIC_PORTAL_PROBE.csv",
            "needle_or_evidence": "PORT1226_0_CMSM_landing",
            "purpose": "previous CMSM portal probe result",
        },
        {
            "source_id": "SRC1227_3_1226_no_surrogate",
            "source_type": "local",
            "location": "source-intake/mts_residuals/P8_Y5_R10_1226_NO_SURROGATE_POLICY.csv",
            "needle_or_evidence": "SURR1226_0_official_arrays_only",
            "purpose": "no surrogate-as-claim policy",
        },
        {
            "source_id": "SRC1227_4_REGARDS_overview",
            "source_type": "web",
            "location": "https://regardsoss.github.io/",
            "needle_or_evidence": "REGARDS provides OpenSearch/GeoJSON/STAC discovery and HTTP serving of files",
            "purpose": "REGARDS platform behavior and expected portal capabilities",
        },
        {
            "source_id": "SRC1227_5_REGARDS_catalog_api",
            "source_type": "web",
            "location": "https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/api-swagger",
            "needle_or_evidence": "catalog API includes complex search, engine searches, downloads, and OAuth2 authorization",
            "purpose": "candidate API route and auth expectations",
        },
        {
            "source_id": "SRC1227_6_REGARDS_services",
            "source_type": "web",
            "location": "https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/service-plugins",
            "needle_or_evidence": "catalog service plugin endpoint /api/v1/rs-catalog/services/{serviceId}/apply",
            "purpose": "candidate bulk download/service route",
        },
        {
            "source_id": "SRC1227_7_CMSM_portal",
            "source_type": "web",
            "location": "https://cmsm-ds.onera.fr/",
            "needle_or_evidence": "official CMSM data portal target from 1226 provenance",
            "purpose": "target portal for package enumeration",
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

    host_probe = probe_host("https://cmsm-ds.onera.fr/")
    network_probe = [
        {
            "probe_id": "NET1227_0_CMSM_tcp",
            "target": "https://cmsm-ds.onera.fr/",
            "method": "socket.getaddrinfo plus socket.create_connection timeout=5s",
            "dns_status": host_probe["dns_status"],
            "addresses": host_probe["addresses"],
            "tcp_status": host_probe["tcp_status"],
            "error": host_probe["error"],
            "package_map_effect": "BLOCK_PACKAGE_ENUMERATION" if host_probe["tcp_status"] != "CONNECTED" else "CAN_ATTEMPT_ENDPOINTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "probe_id": "NET1227_1_prior_curl_probe",
            "target": "https://cmsm-ds.onera.fr/* candidate routes",
            "method": "PowerShell curl.exe -I -L --max-time 15",
            "dns_status": "NOT_RECORDED_SEPARATELY",
            "addresses": "",
            "tcp_status": "CONNECT_FAILED",
            "error": "curl: (7) Failed to connect to cmsm-ds.onera.fr port 443 after about 2.2s",
            "package_map_effect": "BLOCK_PACKAGE_ENUMERATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    endpoint_templates = [
        ("END1227_0_landing", "https://cmsm-ds.onera.fr/", "portal landing page", "landing"),
        ("END1227_1_user_project", "https://cmsm-ds.onera.fr/user/microscope", "possible REGARDS project UI route noted in external references", "ui"),
        ("END1227_2_complex_search", "https://cmsm-ds.onera.fr/api/v1/rs-catalog/complex/search", "REGARDS complex search endpoint", "api_post"),
        ("END1227_3_opensearch_datasets", "https://cmsm-ds.onera.fr/api/v1/rs-catalog/engines/opensearch/datasets/search", "REGARDS engine dataset search", "api_get"),
        ("END1227_4_opensearch_dataobjects", "https://cmsm-ds.onera.fr/api/v1/rs-catalog/engines/opensearch/dataobjects/search", "REGARDS engine dataobject search", "api_get"),
        ("END1227_5_stac_collections", "https://cmsm-ds.onera.fr/api/v1/rs-catalog/engines/stac/collections/search", "REGARDS STAC-style collections search candidate", "api_get"),
        ("END1227_6_api_docs", "https://cmsm-ds.onera.fr/api/v1/rs-catalog/v3/api-docs", "possible instance OpenAPI docs", "api_get"),
        ("END1227_7_service_apply", "https://cmsm-ds.onera.fr/api/v1/rs-catalog/services/{serviceId}/apply", "REGARDS catalog service plugin route for bulk operations", "api_post_template"),
        ("END1227_8_download_file", "https://cmsm-ds.onera.fr/api/v1/rs-catalog/downloads/{aip_id}/files/{checksum}", "REGARDS file download route once AIP/checksum are known", "download_template"),
    ]

    endpoint_candidates = []
    for endpoint_id, url, purpose, route_type in endpoint_templates:
        endpoint_candidates.append(
            {
                "endpoint_id": endpoint_id,
                "url_or_template": url,
                "route_type": route_type,
                "purpose": purpose,
                "auth_expectation": "REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT" if "api/v1" in url else "PUBLIC_UI_OR_REDIRECT",
                "probe_status": "NOT_PROBED_CONNECT_BLOCKED" if host_probe["tcp_status"] != "CONNECTED" else "READY_FOR_NEXT_PROBE",
                "map_result": "NO_PACKAGE_NAMES",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    package_map = [
        {
            "package_id": "PKG1227_0_official_arrays",
            "needed_for": "OBJ1226_0_official_CMSM_arrays",
            "expected_name_patterns": "SUEP;SUREF;science sessions;accelerometer;gx;gz;Sxx;Sxz;masks;calibration",
            "mapped_package_name": "MISSING_PACKAGE_NAME",
            "mapped_url": "MISSING_PACKAGE_URL",
            "metadata_status": "MISSING_METADATA",
            "download_status": "NOT_DOWNLOADED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "package_id": "PKG1227_1_documentation",
            "needed_for": "OBJ1226_1_eta_product_convention;OBJ1226_6_reproducibility_metadata",
            "expected_name_patterns": "documentation;data dictionary;product convention;eta;readme;license",
            "mapped_package_name": "MISSING_PACKAGE_NAME",
            "mapped_url": "MISSING_PACKAGE_URL",
            "metadata_status": "MISSING_METADATA",
            "download_status": "NOT_DOWNLOADED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "package_id": "PKG1227_2_orbit_attitude",
            "needed_for": "OBJ1226_2_source_worldtube;OBJ1226_3_orbit_attitude_masks",
            "expected_name_patterns": "orbit;attitude;session;segment;masks;time",
            "mapped_package_name": "MISSING_PACKAGE_NAME",
            "mapped_url": "MISSING_PACKAGE_URL",
            "metadata_status": "MISSING_METADATA",
            "download_status": "NOT_DOWNLOADED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "package_id": "PKG1227_3_material_response",
            "needed_for": "OBJ1226_4_TiPt_material_tensor;OBJ1226_5_Delta_w_prior",
            "expected_name_patterns": "material;Ti;PtRh;source-weight;composition;test mass",
            "mapped_package_name": "MISSING_PACKAGE_NAME",
            "mapped_url": "MISSING_PACKAGE_URL",
            "metadata_status": "MISSING_METADATA",
            "download_status": "NOT_DOWNLOADED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    access_blockers = [
        {
            "blocker_id": "ABLOCK1227_0_local_tcp",
            "blocker": "LOCAL_MACHINE_CANNOT_CONNECT_TO_CMSM_HTTPS",
            "evidence": "NET1227_0_CMSM_tcp plus prior curl probe",
            "impact": "cannot enumerate or download official packages from this run",
            "resolution": "retry from browser/user network, VPN-free network, or user-assisted portal download",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ABLOCK1227_1_api_auth_unknown",
            "blocker": "REGARDS_API_AUTH_OR_PUBLIC_ROLE_UNKNOWN",
            "evidence": "REGARDS catalog API docs list REGARDS_OAUTH2 for catalog/search/download endpoints",
            "impact": "even with connectivity, API may require browser session/public-role token",
            "resolution": "inspect portal UI session/network calls or use public UI export/download if available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ABLOCK1227_2_no_package_identifiers",
            "blocker": "NO_AIP_ID_CHECKSUM_OR_PACKAGE_URL",
            "evidence": "package map rows all MISSING_PACKAGE_NAME/MISSING_PACKAGE_URL",
            "impact": "download route cannot be constructed safely",
            "resolution": "obtain package metadata before any download attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ABLOCK1227_3_no_data_dictionary",
            "blocker": "NO_DATA_DICTIONARY_OR_COLUMN_SCHEMA",
            "evidence": "OBJ1226 required object metadata remains missing",
            "impact": "parser/tau_WEP runner cannot interpret arrays even if files appear",
            "resolution": "download documentation/readme/data dictionary with the raw packages",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    download_dry_run = [
        {
            "step_id": "DRY1227_0_do_not_execute",
            "action": "download",
            "condition_to_execute": "mapped_package_url and license/access status are known",
            "future_destination": "source-intake/microscope/raw/",
            "current_status": "BLOCKED_NO_PACKAGE_URL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "DRY1227_1_checksum",
            "action": "compute checksums",
            "condition_to_execute": "official files exist locally",
            "future_destination": "source-intake/microscope/metadata/checksums.csv",
            "current_status": "BLOCKED_NO_FILES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "DRY1227_2_manifest",
            "action": "write package manifest",
            "condition_to_execute": "package metadata and local file paths exist",
            "future_destination": "source-intake/microscope/metadata/package_manifest.csv",
            "current_status": "BLOCKED_NO_METADATA",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    manual_acquisition = [
        {
            "manual_step_id": "MAN1227_0_open_portal",
            "instruction": "Open https://cmsm-ds.onera.fr/ in a normal browser and enter the MICROSCOPE project area.",
            "success_evidence": "screenshot or copied package list showing CMSM/MICROSCOPE package names",
            "do_not_do": "do not rename or reinterpret files before provenance is recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "manual_step_id": "MAN1227_1_search_terms",
            "instruction": "Search for SUEP, SUREF, science sessions, accelerometer, readout, documentation, orbit, attitude, masks, gx, gz, Sxx, and Sxz.",
            "success_evidence": "package names, metadata fields, access/license status, and any data dictionary URLs",
            "do_not_do": "do not substitute paper equations for arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "manual_step_id": "MAN1227_2_download_raw",
            "instruction": "If official downloads are available, save unmodified packages under source-intake/microscope/raw/ and docs under source-intake/microscope/docs/.",
            "success_evidence": "local file paths plus checksums and source URLs",
            "do_not_do": "do not mark valid_for_claim=true until parser verifies schema/units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "manual_step_id": "MAN1227_3_report_blocker",
            "instruction": "If login/manual acceptance is required, record the exact screen text and whether account/request access is needed.",
            "success_evidence": "access-blocker note or portal export instructions",
            "do_not_do": "do not bypass access controls",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parser_contract = [
        {
            "parser_id": "PARSE1227_0_required_columns",
            "future_input": "official readout array files",
            "required_fields": "time;session_id;segment_id;instrument/SU;gx;gz;Sxx;Sxz;masks;calibration_flags;attitude/orbit convention",
            "first_validation": "columns exist, units documented, sampling rate/session coverage recorded",
            "current_status": "WAITING_FOR_OFFICIAL_FILES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "parser_id": "PARSE1227_1_metadata",
            "future_input": "CMSM data dictionary/readme",
            "required_fields": "license/access status;citation;version/date;file checksums;units;coordinate frames;product convention",
            "first_validation": "metadata links every parsed column to official documentation",
            "current_status": "WAITING_FOR_DOCUMENTATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "parser_id": "PARSE1227_2_tau_output",
            "future_input": "parsed official arrays and source/orbit/material products",
            "required_fields": "tau_WEP_value_or_distribution;normalization;uncertainty;masking;session coverage;nonclaim flag until reviewed",
            "first_validation": "tau_WEP product remains nonclaim until source-weight runner passes all gates",
            "current_status": "WAITING_FOR_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    tau_feed = [
        {
            "feed_id": "FEED1227_0_to_1225",
            "target": "ACQ1225_0_official_readout_arrays",
            "update": "package map attempted, but connectivity/package identifiers are blocked",
            "tau_WEP_status": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_prediction_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1227_1_to_1226",
            "target": "OBJ1226 required data objects",
            "update": "required objects remain missing; manual acquisition instructions and parser contract staged",
            "tau_WEP_status": "NO_OFFICIAL_ARRAYS_LOCAL",
            "valid_prediction_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1227_0_no_package_map",
            "decision": "do not claim a CMSM package map",
            "because": "local machine cannot connect to CMSM and no package identifiers were obtained",
            "next_action": "user-assisted/browser portal package list or retry from a network that can reach CMSM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1227_1_no_download",
            "decision": "do not download or create raw data rows",
            "because": "there is no mapped package URL, AIP id, checksum, or license/access state",
            "next_action": "only execute dry-run download plan after package metadata exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1227_2_parser_ready",
            "decision": "stage parser contract rather than parser code",
            "because": "without official files, parser code would be speculative and risk accepting wrong columns",
            "next_action": "build parser only after package docs reveal schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1227_0_sources",
            "gate": "local and web source register",
            "status": "PASS",
            "reason": "local handoff sources and web/API documentation sources are recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1227_1_connectivity",
            "gate": "local machine can reach CMSM portal",
            "status": "BLOCKED" if host_probe["tcp_status"] != "CONNECTED" else "PASS",
            "reason": f"tcp_status={host_probe['tcp_status']}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1227_2_package_map",
            "gate": "official package map",
            "status": "BLOCKED",
            "reason": "package names/URLs/AIP ids/checksums are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1227_3_download",
            "gate": "official package download",
            "status": "BLOCKED",
            "reason": "download dry run is blocked until package URL and license/access are known",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1227_4_parser",
            "gate": "readout parser implementation",
            "status": "BLOCKED",
            "reason": "schema/data dictionary not acquired",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1227_5_tau_WEP_claim",
            "gate": "tau_WEP/local-GR/WEP claim permission",
            "status": "BLOCKED",
            "reason": "no official data objects are mapped or local",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1227_0_1228",
            "target_file": "1228-Y5-R10-MICROSCOPE-user-assisted-package-intake-contract.md",
            "target_script": "scripts/Y5_R10_MICROSCOPE_user_assisted_package_intake_contract.py",
            "task": "prepare a strict intake contract for user-assisted CMSM package files: allowed paths, required checksums, metadata fields, and parser refusal gates",
            "success_condition": "if files appear under source-intake/microscope, the runner can verify provenance/schema or refuse them without claims",
            "do_not_do": "do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (NETWORK_PROBE_PATH, network_probe),
        (ENDPOINT_CANDIDATES_PATH, endpoint_candidates),
        (PACKAGE_MAP_PATH, package_map),
        (ACCESS_BLOCKER_PATH, access_blockers),
        (DOWNLOAD_DRY_RUN_PATH, download_dry_run),
        (MANUAL_ACQUISITION_PATH, manual_acquisition),
        (PARSER_CONTRACT_PATH, parser_contract),
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
            "VAL1227_0_local_sources_exist",
            "all cited local sources exist",
            all(parse_bool(row["source_recorded"]) for row in local_sources),
            f"{sum(1 for row in local_sources if parse_bool(row['source_recorded']))}/{len(local_sources)} local sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_1_local_needles_found",
            "all cited local needles found",
            all(parse_bool(row["evidence_recorded"]) for row in local_sources),
            f"{sum(1 for row in local_sources if parse_bool(row['evidence_recorded']))}/{len(local_sources)} local needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_2_web_sources_recorded",
            "web/API documentation sources recorded",
            all(row["location"].startswith("http") and parse_bool(row["evidence_recorded"]) for row in web_sources),
            "; ".join(row["source_id"] for row in web_sources),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_3_endpoint_candidates_staged",
            "REGARDS endpoint candidates are staged",
            len(endpoint_candidates) >= 8,
            "; ".join(row["endpoint_id"] for row in endpoint_candidates),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_4_no_package_names_claimed",
            "no package names or URLs are fabricated",
            all(row["mapped_package_name"].startswith("MISSING") and row["mapped_url"].startswith("MISSING") for row in package_map),
            "all package rows remain MISSING_PACKAGE_NAME/MISSING_PACKAGE_URL",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_5_downloads_blocked",
            "download plan is dry-run only",
            all(row["current_status"].startswith("BLOCKED") and is_false(row, "claim_allowed") for row in download_dry_run),
            "; ".join(row["step_id"] for row in download_dry_run),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_6_blockers_recorded",
            "access blockers are recorded",
            len(access_blockers) >= 4,
            "; ".join(row["blocker_id"] for row in access_blockers),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_7_parser_contract_nonclaim",
            "future parser contract remains nonclaim",
            all(is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") for row in parser_contract),
            "; ".join(row["parser_id"] for row in parser_contract),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_8_tau_feed_nonclaim",
            "tau_WEP feed remains nonclaim",
            all(row["valid_prediction_rows_delta"] == 0 and is_false(row, "claim_allowed") for row in tau_feed),
            "valid_prediction_rows_delta=0 for tau feeds",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_9_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            any(row["status"] == "BLOCKED" for row in claim_gates) and all(is_false(row, "valid_for_claim") for row in claim_gates),
            "connectivity/package/download/parser/tau claim gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_10_next_target_intake",
            "next target stages user-assisted intake contract",
            next_rows[0]["target_file"] == "1228-Y5-R10-MICROSCOPE-user-assisted-package-intake-contract.md",
            next_rows[0]["target_file"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1227_11_nonclaim_policy",
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
            "VAL1227_12_csv_parse",
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
            "VAL1227_13_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1227_14_overall",
            "overall 1227 validation",
            overall_before,
            "1227 maps REGARDS/CMSM route candidates, records access blockers, and refuses fabricated package rows",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1227 Y5/R10 MICROSCOPE Portal Package Map Or Access Blocker

**Current verdict:** 1227 does **not** obtain a package map. It identifies the likely REGARDS/CMSM endpoint family, but local machine access to `cmsm-ds.onera.fr:443` is blocked, so no package names, URLs, AIP ids, checksums, or arrays are claimed.

**Main progress:** the acquisition route is now exact: candidate REGARDS endpoints are listed, package rows are deliberately left missing, access blockers are explicit, and a no-surrogate parser/intake contract is staged for future official files.

**Practical consequence:** `tau_WEP` remains symbolic-only. The next safe move is user-assisted package intake or a retry from a network/browser session that can reach CMSM.

## Source Register

{markdown_table(source_register, ["source_id", "source_type", "location", "needle_or_evidence", "purpose", "absolute_path_or_url", "source_recorded", "evidence_recorded", "valid_for_claim", "claim_allowed"])}

## Network Probe

{markdown_table(network_probe, ["probe_id", "target", "method", "dns_status", "addresses", "tcp_status", "error", "package_map_effect", "valid_for_claim", "claim_allowed"])}

## REGARDS Endpoint Candidates

{markdown_table(endpoint_candidates, ["endpoint_id", "url_or_template", "route_type", "purpose", "auth_expectation", "probe_status", "map_result", "valid_for_claim", "claim_allowed"])}

## Package Map Status

{markdown_table(package_map, ["package_id", "needed_for", "expected_name_patterns", "mapped_package_name", "mapped_url", "metadata_status", "download_status", "valid_for_claim", "claim_allowed"])}

## Access Blocker Ledger

{markdown_table(access_blockers, ["blocker_id", "blocker", "evidence", "impact", "resolution", "valid_for_claim", "claim_allowed"])}

## Download Dry-Run Plan

{markdown_table(download_dry_run, ["step_id", "action", "condition_to_execute", "future_destination", "current_status", "valid_for_claim", "claim_allowed"])}

## Manual Acquisition Instructions

{markdown_table(manual_acquisition, ["manual_step_id", "instruction", "success_evidence", "do_not_do", "valid_for_claim", "claim_allowed"])}

## Future Parser Contract

{markdown_table(parser_contract, ["parser_id", "future_input", "required_fields", "first_validation", "current_status", "valid_for_claim", "claim_allowed"])}

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
