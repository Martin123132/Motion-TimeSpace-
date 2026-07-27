from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


RESIDUAL_TERMS = ["rho_top-rho_H", "rho_top-rho-H", "topological/Hilbert residual", "topological/Hilbert profile"]
DOUBLE_DIVERGENCE_TERMS = ["partial_i partial_j", "nabla_alpha nabla_beta", "S^{ij}", "U^{0i0j}", "U^{mu alpha nu beta}"]
ACTION_TERMS = ["dB_impr", "improvement action", "phi R", "Riemann", "Hilbert/Noether improvement", "S_U"]
OWNER_TERMS = ["parent-owned", "parent owner", "parent action", "parent-adopted", "birth certificate", "birth-certify"]
READOUT_TERMS = ["before readout", "pre-readout", "readout firewall", "cannot be recentered", "not post-readout"]
BOUNDARY_TERMS = ["boundary", "no-flux", "boundary_silent", "affine boundary", "boundary pairings", "zero pairings"]
BLOCKER_TERMS = [
    "MISSING",
    "NOT_SIGNED",
    "not sufficient",
    "fails",
    "FAILS",
    "BIRTH_CERTIFICATE_FAILS",
    "blocked",
    "unsigned",
    "nonclaim",
    "do_not_claim",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def contains_any(text: str, terms: Iterable[str]) -> bool:
    lower_text = text.lower()
    return any(term.lower() in lower_text for term in terms)


def matching_terms(text: str, terms: Iterable[str]) -> str:
    lower_text = text.lower()
    return ";".join(term for term in terms if term.lower() in lower_text)


def score_candidate(row: Mapping[str, str]) -> Dict[str, str]:
    path = Path(str(row["path"]))
    text = read_text(path)
    path_exists = path.exists()
    has_residual_identity = contains_any(text, RESIDUAL_TERMS) and contains_any(text, DOUBLE_DIVERGENCE_TERMS)
    has_action_birth_shape = contains_any(text, ACTION_TERMS) and contains_any(text, DOUBLE_DIVERGENCE_TERMS + ["dB_impr", "phi R"])
    has_parent_owner = contains_any(text, OWNER_TERMS)
    has_readout_lock = contains_any(text, READOUT_TERMS)
    has_boundary_silence = contains_any(text, BOUNDARY_TERMS)
    has_blocker = contains_any(text, BLOCKER_TERMS)
    certificate_pass = (
        path_exists
        and has_residual_identity
        and has_action_birth_shape
        and has_parent_owner
        and has_readout_lock
        and has_boundary_silence
        and not has_blocker
    )
    if certificate_pass:
        status = "BIRTH_CERTIFICATE_PASS_CANDIDATE"
    elif path_exists and has_residual_identity and has_action_birth_shape and has_blocker:
        status = "CANDIDATE_SHAPE_PRESENT_BUT_BLOCKED"
    elif path_exists and (has_residual_identity or has_action_birth_shape or has_parent_owner or has_boundary_silence):
        status = "PARTIAL_CANDIDATE_INSUFFICIENT"
    elif path_exists:
        status = "NO_RELEVANT_BIRTH_CERTIFICATE_TERMS"
    else:
        status = "PATH_MISSING"
    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "role": str(row.get("role", "")),
        "path": str(path),
        "path_exists": str(path_exists),
        "has_residual_identity": str(has_residual_identity),
        "has_action_birth_shape": str(has_action_birth_shape),
        "has_parent_owner": str(has_parent_owner),
        "has_readout_lock": str(has_readout_lock),
        "has_boundary_silence": str(has_boundary_silence),
        "has_blocker_terms": str(has_blocker),
        "matched_residual_terms": matching_terms(text, RESIDUAL_TERMS),
        "matched_double_divergence_terms": matching_terms(text, DOUBLE_DIVERGENCE_TERMS),
        "matched_action_terms": matching_terms(text, ACTION_TERMS),
        "matched_owner_terms": matching_terms(text, OWNER_TERMS),
        "matched_boundary_terms": matching_terms(text, BOUNDARY_TERMS),
        "matched_blockers": matching_terms(text, BLOCKER_TERMS),
        "certificate_pass": str(certificate_pass),
        "valid_for_claim": "False",
        "claim_allowed": "False",
        "status": status,
    }


def score_manifest(manifest_path: Path) -> List[Dict[str, str]]:
    return [score_candidate(row) for row in read_csv(manifest_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Score candidate sources for the U/S improvement birth certificate.")
    parser.add_argument("--manifest", required=True, type=Path, help="CSV with candidate_id,path,role.")
    parser.add_argument("--output", required=True, type=Path, help="Output source-hunt CSV.")
    args = parser.parse_args()
    write_csv(args.output, score_manifest(args.manifest))


if __name__ == "__main__":
    main()
