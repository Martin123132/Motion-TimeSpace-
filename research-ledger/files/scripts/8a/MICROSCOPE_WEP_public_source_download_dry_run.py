from __future__ import annotations

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
