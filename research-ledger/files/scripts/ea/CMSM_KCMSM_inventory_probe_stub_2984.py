from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENDPOINTS = [
    "https://cmsm-ds.onera.fr/",
    "https://cmsm-ds.onera.fr/user/microscope",
    "https://cmsm-ds.onera.fr/user/microscope/modules/7",
    "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
]


def fetch(url: str, timeout: float) -> dict[str, object]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MTS-CMSM-inventory-probe/2984"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            return {
                "url": url,
                "status": f"HTTP_{response.status}",
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type", ""),
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                "body": body.decode("utf-8", errors="replace"),
            }
    except urllib.error.HTTPError as exc:
        return {
            "url": url,
            "status": f"HTTP_ERROR_{exc.code}",
            "final_url": getattr(exc, "url", url),
            "content_type": "",
            "bytes": 0,
            "sha256": "",
            "body": "",
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "url": url,
            "status": "REQUEST_FAILED",
            "final_url": url,
            "content_type": "",
            "bytes": 0,
            "sha256": "",
            "body": "",
            "error": str(exc),
        }


def link_candidates(body: str, source_url: str) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    for match in re.finditer(r"""href=["']([^"']+)["']""", body, flags=re.IGNORECASE):
        href = match.group(1).strip()
        low = href.lower()
        if any(token in low for token in ("microscope", "cmsm", "suep", "suref", "csv", "zip", "tar", "dat", "h5", "npz", "pkl", "fits")):
            candidates.append({"source_url": source_url, "href": href, "reason": "keyword_or_data_extension"})
    return candidates


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Nonclaim CMSM inventory probe stub for MTS WEP K_CMSM acquisition.")
    parser.add_argument("--out", type=Path, default=None, help="Output run directory. Defaults to post-checkpoint-work/runs/<timestamp>.")
    parser.add_argument("--timeout", type=float, default=8.0, help="Per-request timeout in seconds.")
    parser.add_argument("--endpoint", action="append", default=[], help="Additional endpoint to probe.")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = args.out or (ROOT / "runs" / f"{stamp}_CMSM_KCMSM_inventory_probe_2984")
    run_dir.mkdir(parents=True, exist_ok=True)

    endpoints = [*DEFAULT_ENDPOINTS, *args.endpoint]
    probe_rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, str]] = []
    log_lines = [
        "CMSM K_CMSM inventory probe stub 2984",
        "NONCLAIM: this script does not create P_WEP_K_CMSM_readout.csv.",
        f"run_utc={datetime.now(timezone.utc).isoformat()}",
    ]
    for endpoint in endpoints:
        result = fetch(endpoint, args.timeout)
        body = str(result.pop("body", ""))
        probe_rows.append(result)
        candidate_rows.extend(link_candidates(body, str(result.get("final_url", endpoint))))
        log_lines.append(f"{endpoint} -> {result.get('status')} bytes={result.get('bytes')} sha256={result.get('sha256')}")

    write_csv(run_dir / "cmsm_endpoint_probe.csv", probe_rows)
    write_csv(run_dir / "inventory_link_candidates.csv", candidate_rows)
    status = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint_count": len(endpoints),
        "candidate_count": len(candidate_rows),
        "claim_allowed": False,
        "valid_for_claim": False,
        "live_target_written": False,
        "live_target": str(ROOT / "source-intake" / "microscope" / "official_readout" / "P_WEP_K_CMSM_readout.csv"),
        "next_required_step": "Manually review candidates, then build a source-specific downloader/checksummer before any live readout file is written.",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(run_dir)


if __name__ == "__main__":
    main()
