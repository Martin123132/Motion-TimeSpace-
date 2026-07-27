from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BOUNDARY_PROJECTIVE_SPLIT_UNDER_PRIVATE_SRNG_2337"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2337-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md"

PATHS = {
    "2336_doc": ROOT / "2336-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
    "2336_validation": OUT / "P8_Y5_BRR545_2336_VALIDATION.csv",
    "2336_next": OUT / "P8_Y5_PARENT_QLOC_2336_NEXT_TARGET.csv",
    "2336_p4": OUT / "P8_Y5_PARENT_QLOC_2336_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv",
    "2119_projective_cert": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_CERTIFICATE.csv",
    "2119_projective_policy": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_RESIDUAL_POLICY.csv",
    "2332_audit": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_TRIDENT_SILENCE_AUDIT.csv",
    "2332_envelopes": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_RESIDUAL_ENVELOPES.csv",
    "2331_nonhilbert": OUT / "P8_Y5_PARENT_QLOC_2331_NONHILBERT_RESIDUAL_ROW.csv",
    "1013_flux": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "1014_commutator": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1963_action": OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv",
}

SOURCES = [
    ("SRC2337_00_2336_doc", "2336_doc", PATHS["2336_doc"], ["NEXT2336_0", "P4A2336_4_reduced_total"], "2336 handoff"),
    ("SRC2337_01_2336_validation", "2336_validation", PATHS["2336_validation"], ["VAL2336_OVERALL", "PASS"], "2336 validation"),
    ("SRC2337_02_2336_next", "2336_next", PATHS["2336_next"], ["NEXT2336_0", "boundary-projective"], "machine-readable 2337 target"),
    ("SRC2337_03_2336_p4", "2336_p4", PATHS["2336_p4"], ["P4A2336_2_boundary", "P4A2336_3_projective"], "reduced residual status"),
    ("SRC2337_04_2119_projective_cert", "2119_projective_cert", PATHS["2119_projective_cert"], ["PJC2119_5_verdict", "PROJECTIVE_ZERO_INSIDE_CANDIDATE"], "projective certificate"),
    ("SRC2337_05_2119_projective_policy", "2119_projective_policy", PATHS["2119_projective_policy"], ["PRP2119_0_candidate_branch", "PRP2119_1_global_corpus"], "projective policy"),
    ("SRC2337_06_2332_audit", "2332_audit", PATHS["2332_audit"], ["NHT2332_2_boundary_improvement", "NOT_ZERO_DERIVED"], "boundary/improvement trident"),
    ("SRC2337_07_2332_envelopes", "2332_envelopes", PATHS["2332_envelopes"], ["NHE2332_2_boundary", "MISSING_ZERO_OR_ENVELOPE"], "boundary residual envelope"),
    ("SRC2337_08_2331_nonhilbert", "2331_nonhilbert", PATHS["2331_nonhilbert"], ["NHR2331_2_boundary_worldtube", "MISSING_ZERO_OR_ENVELOPE"], "non-Hilbert boundary row"),
    ("SRC2337_09_1013_flux", "1013_flux", PATHS["1013_flux"], ["OBS1013_4_boundary_zero_flux", "MISSING_B_ZERO_FLUX"], "measured-GM boundary flux obstruction"),
    ("SRC2337_10_1014_commutator", "1014_commutator", PATHS["1014_commutator"], ["PCC1014_2_B_zero_flux", "MISSING_B_ZERO_FLUX"], "PiM boundary flux obstruction"),
    ("SRC2337_11_1963_action", "1963_action", PATHS["1963_action"], ["ACT1963_5_no_independent_Gamma_clause", "NO_GAMMA_BY_VARIABLE_SIGNATURE"], "owned-coframe no-Gamma branch"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2337_SOURCE_REGISTER.csv",
    "split": OUT / "P8_Y5_PARENT_QLOC_2337_RESIDUAL_SPLIT_LEDGER.csv",
    "projective": OUT / "P8_Y5_PARENT_QLOC_2337_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv",
    "boundary": OUT / "P8_Y5_PARENT_QLOC_2337_BOUNDARY_IMPROVEMENT_QUEUE.csv",
    "reduced": OUT / "P8_Y5_PARENT_QLOC_2337_REDUCED_CONNECTION_GATE.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2337_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2337_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2337_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2337_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2337_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2337_0_split", OUTPUTS["split"], BETA_DOCS / "BOUNDARY_PROJECTIVE_RESIDUAL_SPLIT_2337_NONCLAIM.csv"),
    ("COPY2337_1_boundary", OUTPUTS["boundary"], MICRO_RESIDUALS / "boundary_improvement_queue_2337_nonclaim.csv"),
    ("COPY2337_2_decision", OUTPUTS["reduced"], RAB_QUEUE / "JR2337_REDUCED_CONNECTION_GATE_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_split_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "RSL2337_0_private_total", "component": "Delta_abs_private_SRNG_branch", "private_SRNG_status": "Delta_source/clock/light/orbit zeroed by private SRNG/OFC", "public_status": "not a public theorem", "next_action": "split spin, boundary, projective", "claim_allowed": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "RSL2337_1_spin", "component": "Delta_spin", "private_SRNG_status": "still live unless owned-coframe spin connection is parent-signed", "public_status": "live", "next_action": "spin/coframe-owned connection theorem or axial-torsion bound", "claim_allowed": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "RSL2337_2_boundary", "component": "Delta_boundary + Delta_improvement", "private_SRNG_status": "still live; SRNG does not fix integration-boundary flux", "public_status": "live", "next_action": "derive B_zero_flux=0 / compact flux closure or fill boundary bound", "claim_allowed": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "RSL2337_3_projective_private", "component": "Delta_projective", "private_SRNG_status": "zero inside private owned-coframe+SRNG branch by variable absence", "public_status": "global affine fallback retained", "next_action": "record private zero switch and keep affine fallback policy", "claim_allowed": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "RSL2337_4_verdict", "component": "connection residual split", "private_SRNG_status": "projective reduced; boundary remains the hard live channel; spin remains a separate guard", "public_status": "no local-GR/Newton claim", "next_action": "boundary no-flux/Hilbert flux closure first", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def build_projective_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "PRJ2337_0_candidate_zero", "branch": "private owned-coframe + SRNG/OFC", "projective_current": "0", "reason": "Gamma_ind is not a variable and source/readout exceptions are excluded by private SRNG", "status": "ZERO_INSIDE_PRIVATE_BRANCH_ONLY", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "PRJ2337_1_public_global", "branch": "full current corpus", "projective_current": "not globally zero", "reason": "SRNG/OFC and owned-coframe are private working clauses, not public parent-signed theorems", "status": "PUBLIC_CERTIFICATE_BLOCKED", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "PRJ2337_2_affine_fallback", "branch": "independent affine fallback", "projective_current": "P_projective[source,clock,WEP]", "reason": "if Gamma_ind is retained, projective trace needs an unobservable/gauge/fixed proof or a numeric kernel", "status": "FALLBACK_RETAINED", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "PRJ2337_3_verdict", "branch": "decision", "projective_current": "zero only in private branch", "reason": "2119 plus 2336 collapses the candidate-branch projective issue, not the global affine branch", "status": "PRIVATE_ZERO_PUBLIC_NONCLAIM", "score_ready": "false", "valid_for_claim": "false"},
    ]


def build_boundary_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "BND2337_0_B_zero_flux", "boundary_object": "B_zero_flux", "definition": "exact/reference/boundary improvement flux through compact linked boundary", "status": "MISSING_THEOREM_OR_VALUE", "units": "GM_flux_or_dimensionless after source normalization", "needed_input": "boundary no-flux theorem, compact support/falloff, source path, no-cancellation guard", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BND2337_1_worldtube_flux", "boundary_object": "finite-annulus flux leakage", "definition": "M_eff^-1 int_A d(Pi_M J_H) or dln_Meff_dt / radial envelope", "status": "MISSING_TIME_RADIAL_PROFILE_OR_THEOREM", "units": "yr^-1 or dimensionless radial envelope", "needed_input": "worldtube glue, Pi_M ownership, same-frame M_H_ref, flux closure", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BND2337_2_projector_commutator", "boundary_object": "[d,Pi_M]J_H + R_eq", "definition": "projector/domain variation and topological-Hilbert mismatch", "status": "MISSING_COMMUTATOR_OR_EQUALITY_THEOREM", "units": "dimensionless or GM flux units", "needed_input": "Pi_M J_H = J_M_top + dB_zero, I_commutator, Delta_PiM", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BND2337_3_improvement_representative", "boundary_object": "improvement/superpotential representative", "definition": "choice of Hamiltonian representative and exact flux class", "status": "MISSING_FIXED_REPRESENTATIVE", "units": "source-current units", "needed_input": "fixed boundary/reference convention before readout", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BND2337_4_priority", "boundary_object": "boundary first target", "definition": "B_zero_flux=0 or finite source-backed B_zero_flux row", "status": "SELECTED_NEXT", "units": "GM_flux_or_dimensionless", "needed_input": "derive compact boundary no-flux theorem or build first bound row", "score_ready": "false", "valid_for_claim": "false"},
    ]


def build_reduced_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "RCG2337_0_private_formula", "gate": "private SRNG reduced connection residual", "formula": "Delta_abs_private = Delta_spin + Delta_boundary + Delta_improvement + 0_projective_private", "status": "PRIVATE_BRANCH_REDUCTION_ONLY", "claim_effect": "narrows internal work; no public pass", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "RCG2337_1_projective_private_zero", "gate": "projective trace inside private branch", "formula": "Delta_projective_private=0 by no Gamma_ind variable and SRNG source/readout exclusion", "status": "PRIVATE_ZERO_SWITCH", "claim_effect": "projective no longer first priority inside private branch", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "RCG2337_2_boundary_live", "gate": "boundary/improvement closure", "formula": "Delta_boundary requires B_zero_flux/worldtube/commutator/improvement proof or bound", "status": "PRIMARY_LIVE_BLOCKER", "claim_effect": "Newton/GM/local-GR still blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "RCG2337_3_public_gate", "gate": "public local GR/Newton bridge", "formula": "all private clauses must be derived/adopted in formal spine plus boundary/spin closed", "status": "BLOCKED_NONCLAIM", "claim_effect": "do not publish as evidence", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2337_0_projective_public_zero", "gate": "projective trace globally zero", "passed": "false", "claim_effect": "private branch only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2337_1_boundary_zero", "gate": "boundary/improvement flux zero", "passed": "false", "claim_effect": "primary blocker", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2337_2_spin_zero", "gate": "spin/torsion hypermomentum zero", "passed": "false", "claim_effect": "separate guard", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2337_3_P4_score", "gate": "remaining residuals score-ready", "passed": "false", "claim_effect": "values/maps/bounds missing", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2337_4_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "boundary/spin/formal adoption still open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2337_5_github", "gate": "safe public evidence update", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2337_0_projective_as_public", "claim": "projective trace is solved globally", "allowed": "false", "reason": "zero is private owned-coframe+SRNG only; affine fallback retained", "blocking_rows": "PRJ2337_1_public_global;PRJ2337_2_affine_fallback", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2337_1_SRNG_solves_boundary", "claim": "SRNG solves boundary/improvement flux", "allowed": "false", "reason": "boundary flux is an integration/source-normalization obstruction, not a readout Gamma slot", "blocking_rows": "BND2337_0_B_zero_flux;RCG2337_2_boundary_live", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2337_2_boundary_by_notation", "claim": "B_zero_flux=0 by choosing a reference", "allowed": "false", "reason": "reference must be fixed before readout and sourced; no fitted cancellation", "blocking_rows": "BND2337_0_B_zero_flux;BND2337_3_improvement_representative", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2337_3_local_gr", "claim": "2337 proves local GR/Newton", "allowed": "false", "reason": "2337 narrows residuals but leaves boundary, spin and formal private-clause adoption open", "blocking_rows": "CG2337_4_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2337_0", "next_target": "2338-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md", "why": "boundary/improvement is now the primary live connection/source-normalization blocker under private SRNG.", "claim_status": "private_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2337_1", "next_target": "2338b-Y5-R2FR-spin-coframe-owned-connection-proof-or-axial-torsion-bound.md", "why": "spin/torsion remains the parallel connection guard after source/readout/projective private reductions.", "claim_status": "parallel_nonclaim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2337_2", "next_target": "2338c-Y5-R2FR-affine-projective-kernel-if-private-branch-rejected.md", "why": "if the private owned-coframe branch is rejected, projective trace needs an empirical/theorem residual kernel.", "claim_status": "fallback_nonclaim", "valid_for_claim": "false"},
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    required_sources = [row for row in source_rows if row["required"] == "true"]

    add("VAL2337_00_required_sources_exist", all(row["exists"] == "true" for row in required_sources), "every required source path exists")
    add("VAL2337_01_required_needles_found", all(row["needles_found"] == "true" for row in required_sources), "all required source needles were found")
    split_rows = read_csv_rows(OUTPUTS["split"])
    add("VAL2337_02_split_verdict", any(row.get("row_id") == "RSL2337_4_verdict" and "boundary remains" in row.get("private_SRNG_status", "") for row in split_rows), "residual split verdict recorded")
    projective_rows = read_csv_rows(OUTPUTS["projective"])
    add("VAL2337_03_projective_private_zero", any(row.get("row_id") == "PRJ2337_0_candidate_zero" and row.get("status") == "ZERO_INSIDE_PRIVATE_BRANCH_ONLY" for row in projective_rows), "projective zero switch private only")
    add("VAL2337_04_projective_fallback_retained", any(row.get("row_id") == "PRJ2337_2_affine_fallback" and row.get("status") == "FALLBACK_RETAINED" for row in projective_rows), "affine projective fallback retained")
    boundary_rows = read_csv_rows(OUTPUTS["boundary"])
    add("VAL2337_05_boundary_queue_live", any(row.get("row_id") == "BND2337_0_B_zero_flux" and row.get("status") == "MISSING_THEOREM_OR_VALUE" for row in boundary_rows), "B_zero boundary row remains live")
    reduced_rows = read_csv_rows(OUTPUTS["reduced"])
    add("VAL2337_06_boundary_primary", any(row.get("row_id") == "RCG2337_2_boundary_live" and row.get("status") == "PRIMARY_LIVE_BLOCKER" for row in reduced_rows), "boundary selected as primary live blocker")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2337_07_local_claims_block", any(row.get("row_id") == "CG2337_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2337_08_github_blocked", any(row.get("row_id") == "CG2337_5_github" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended from 2337")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2337_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    next_rows = read_csv_rows(OUTPUTS["next"])
    add("VAL2337_10_next_boundary_no_flux", any(row.get("row_id") == "NEXT2337_0" and "boundary-no-flux" in row.get("next_target", "") for row in next_rows), "boundary no-flux target selected next")
    add("VAL2337_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")

    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2337_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2337*.csv", "*2337*.md", "*BOUNDARY_PROJECTIVE*2337*", "*Bzero*2337*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2337_13_formalization_untouched_by_2337", not formalization_hits, "no 2337 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2337_OVERALL", all(row["status"] == "PASS" for row in rows), "2337 splits the remaining private-SRNG connection residuals, records projective trace as zero only inside the private owned-coframe branch, keeps affine fallback public/nonclaim, and selects boundary no-flux/B_zero as the next primary blocker.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    split_rows: list[dict[str, Any]],
    projective_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    reduced_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2337 - boundary/projective residual split under private SRNG

## Summary

2337 uses the private SRNG/OFC branch from 2336 to split the remaining connection residuals.

Result:

1. Source/readout Gamma leakage is zero only inside the private branch.
2. Projective trace is also zero inside the private owned-coframe+SRNG branch by variable absence.
3. The affine/projective fallback remains retained for public/global work.
4. Boundary/improvement flux is not solved by SRNG and becomes the primary live blocker.
5. Spin/torsion remains a parallel guard.

No public local-GR/Newton claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Residual Split Ledger

{markdown_table(split_rows, ["row_id", "component", "private_SRNG_status", "public_status", "next_action", "claim_allowed", "valid_for_claim"])}

## Projective Status Under Private SRNG

{markdown_table(projective_rows, ["row_id", "branch", "projective_current", "reason", "status", "score_ready", "valid_for_claim"])}

## Boundary Improvement Queue

{markdown_table(boundary_rows, ["row_id", "boundary_object", "definition", "status", "units", "needed_input", "score_ready", "valid_for_claim"])}

## Reduced Connection Gate

{markdown_table(reduced_rows, ["row_id", "gate", "formula", "status", "claim_effect", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "split": build_split_rows(),
        "projective": build_projective_rows(),
        "boundary": build_boundary_rows(),
        "reduced": build_reduced_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["split"],
        rows_by_output["projective"],
        rows_by_output["boundary"],
        rows_by_output["reduced"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2337 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
