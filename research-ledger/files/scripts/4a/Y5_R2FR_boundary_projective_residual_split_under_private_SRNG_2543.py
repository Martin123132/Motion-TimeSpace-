from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2543"
BRANCH_ID = "MTS_R2FR_BOUNDARY_PROJECTIVE_SPLIT_UNDER_PRIVATE_SRNG_2543"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2543-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2543_SOURCE_REGISTER.csv",
    "split": RESIDUALS / "P8_Y5_NO_SHADOW_2543_RESIDUAL_SPLIT_LEDGER.csv",
    "projective": RESIDUALS / "P8_Y5_NO_SHADOW_2543_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv",
    "boundary": RESIDUALS / "P8_Y5_NO_SHADOW_2543_BOUNDARY_IMPROVEMENT_QUEUE.csv",
    "gate": RESIDUALS / "P8_Y5_NO_SHADOW_2543_REDUCED_CONNECTION_GATE.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2543_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2543_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2543_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2543_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2543_VALIDATION.csv",
}

BRANCH_COPIES = {
    "split": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Residual_split_under_private_SRNG_2543_NONCLAIM.csv",
    "projective": POST_ROOT / "source-intake" / "local_bounds" / "Projective_status_private_SRNG_2543_NONCLAIM.csv",
    "boundary": POST_ROOT / "source-intake" / "local_bounds" / "Boundary_improvement_queue_2543_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "BZERO2543_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2543_0_2542_doc", "2542-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md", "NEXT2542_0_selected", "2542 selected boundary/projective residual split"),
    ("SRC2543_1_2542_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2542_VALIDATION.csv", "VAL2542_OVERALL,PASS", "2542 validation anchor"),
    ("SRC2543_2_2542_p4", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2542_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv", "P4A2542_4_reduced_total", "current reduced residual status"),
    ("SRC2543_3_2542_adoption", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2542_SRNG_ADOPTION_DECISION_MATRIX.csv", "ADM2542_3_decision", "private SRNG/OFC adoption input"),
    ("SRC2543_4_2378_doc", "2378-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md", "RSL2378_4_verdict", "older residual split precedent"),
    ("SRC2543_5_2378_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2378_VALIDATION.csv", "VAL2378_OVERALL", "2378 validation anchor"),
    ("SRC2543_6_2378_split", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_RESIDUAL_SPLIT_LEDGER.csv", "RSL2378_4_verdict", "residual split ledger precedent"),
    ("SRC2543_7_2378_projective", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv", "PRJ2378_3_verdict", "projective status precedent"),
    ("SRC2543_8_2378_boundary", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_BOUNDARY_IMPROVEMENT_QUEUE.csv", "BND2378_4_priority", "boundary queue precedent"),
    ("SRC2543_9_2378_gate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_REDUCED_CONNECTION_GATE.csv", "RCG2378_2_boundary_live", "reduced connection gate precedent"),
    ("SRC2543_10_2378_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_NEXT_TARGET.csv", "NEXT2378_0_selected", "boundary no-flux next target precedent"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "source_id": source_id,
                    "source_path": source_path,
                    "needle": needle,
                    "role": role,
                    "path_exists": str(path.exists()).lower(),
                    "needle_found": str(contains(path, needle)).lower(),
                    "status": "SOURCE_OK" if path.exists() and contains(path, needle) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def residual_split_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "RSL2543_0_private_total",
            "Delta_abs_private_SRNG_branch",
            "Delta_source/clock/light/orbit zeroed by private SRNG/OFC",
            "not a public theorem",
            "split spin, boundary, projective",
        ),
        (
            "RSL2543_1_spin",
            "Delta_spin",
            "still live unless owned-coframe spin connection is parent-signed",
            "live",
            "spin/coframe-owned connection theorem or axial-torsion bound",
        ),
        (
            "RSL2543_2_boundary",
            "Delta_boundary + Delta_improvement",
            "still live; SRNG does not fix integration-boundary flux",
            "live",
            "derive B_zero_flux=0 / compact flux closure or fill boundary bound",
        ),
        (
            "RSL2543_3_projective_private",
            "Delta_projective",
            "zero inside private owned-coframe+SRNG branch by variable absence",
            "global affine fallback retained",
            "record private zero switch and keep affine fallback policy",
        ),
        (
            "RSL2543_4_verdict",
            "connection residual split",
            "projective reduced; boundary remains hard live channel; spin remains separate guard",
            "no local-GR/Newton claim",
            "boundary no-flux/Hilbert flux closure first",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "component": component,
            "private_SRNG_status": private_status,
            "public_status": public_status,
            "next_action": next_action,
        }
        for row_id, component, private_status, public_status, next_action in rows
    ]


def projective_status_under_private_srng() -> list[dict[str, object]]:
    rows = [
        (
            "PRJ2543_0_candidate_zero",
            "private owned-coframe + SRNG/OFC",
            "0",
            "Gamma_ind is not a variable and source/readout exceptions are excluded by private SRNG",
            "ZERO_INSIDE_PRIVATE_BRANCH_ONLY",
        ),
        (
            "PRJ2543_1_public_global",
            "full current corpus",
            "not globally zero",
            "SRNG/OFC and owned-coframe are private working clauses, not public parent-signed theorems",
            "PUBLIC_CERTIFICATE_BLOCKED",
        ),
        (
            "PRJ2543_2_affine_fallback",
            "independent affine fallback",
            "P_projective[source,clock,WEP]",
            "if Gamma_ind is retained, projective trace needs an unobservable/gauge/fixed proof or numeric kernel",
            "FALLBACK_RETAINED",
        ),
        (
            "PRJ2543_3_verdict",
            "decision",
            "zero only in private branch",
            "private SRNG/owned-coframe collapses candidate-branch projective issue, not global affine branch",
            "PRIVATE_ZERO_PUBLIC_NONCLAIM",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "branch": branch,
            "projective_current": current,
            "reason": reason,
            "status": status,
        }
        for row_id, branch, current, reason, status in rows
    ]


def boundary_improvement_queue() -> list[dict[str, object]]:
    rows = [
        (
            "BND2543_0_B_zero_flux",
            "B_zero_flux",
            "exact/reference/boundary improvement flux through compact linked boundary",
            "MISSING_THEOREM_OR_VALUE",
            "GM_flux_or_dimensionless after source normalization",
            "boundary no-flux theorem, compact support/falloff, source path, no-cancellation guard",
        ),
        (
            "BND2543_1_worldtube_flux",
            "finite-annulus flux leakage",
            "M_eff^-1 int_A d(Pi_M J_H) or dln_Meff_dt / radial envelope",
            "MISSING_TIME_RADIAL_PROFILE_OR_THEOREM",
            "yr^-1 or dimensionless radial envelope",
            "worldtube glue, Pi_M ownership, same-frame M_H_ref, flux closure",
        ),
        (
            "BND2543_2_projector_commutator",
            "[d,Pi_M]J_H + R_eq",
            "projector/domain variation and topological-Hilbert mismatch",
            "MISSING_COMMUTATOR_OR_EQUALITY_THEOREM",
            "dimensionless or GM flux units",
            "Pi_M J_H = J_M_top + dB_zero, I_commutator, Delta_PiM",
        ),
        (
            "BND2543_3_improvement_representative",
            "improvement/superpotential representative",
            "choice of Hamiltonian representative and exact flux class",
            "MISSING_FIXED_REPRESENTATIVE",
            "source-current units",
            "fixed boundary/reference convention before readout",
        ),
        (
            "BND2543_4_priority",
            "boundary first target",
            "B_zero_flux=0 or finite source-backed B_zero_flux row",
            "SELECTED_NEXT",
            "GM_flux_or_dimensionless",
            "derive compact boundary no-flux theorem or build first bound row",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "boundary_object": obj,
            "definition": definition,
            "status": status,
            "units": units,
            "needed_input": needed,
        }
        for row_id, obj, definition, status, units, needed in rows
    ]


def reduced_connection_gate() -> list[dict[str, object]]:
    rows = [
        (
            "RCG2543_0_private_formula",
            "private SRNG reduced connection residual",
            "Delta_abs_private = Delta_spin + Delta_boundary + Delta_improvement + 0_projective_private",
            "PRIVATE_BRANCH_REDUCTION_ONLY",
            "narrows internal work; no public pass",
        ),
        (
            "RCG2543_1_projective_private_zero",
            "projective trace inside private branch",
            "Delta_projective_private=0 by no Gamma_ind variable and SRNG source/readout exclusion",
            "PRIVATE_ZERO_SWITCH",
            "projective no longer first priority inside private branch",
        ),
        (
            "RCG2543_2_boundary_live",
            "boundary/improvement closure",
            "Delta_boundary requires B_zero_flux/worldtube/commutator/improvement proof or bound",
            "PRIMARY_LIVE_BLOCKER",
            "Newton/GM/local-GR still blocked",
        ),
        (
            "RCG2543_3_public_gate",
            "public local GR/Newton bridge",
            "all private clauses must be derived/adopted in formal spine plus boundary/spin closed",
            "BLOCKED_NONCLAIM",
            "do not publish as evidence",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "gate": gate,
                "formula": formula,
                "status": status,
                "claim_effect": effect,
            }
        )
        for row_id, gate, formula, status, effect in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2543_0_projective_public_zero", "projective trace globally zero", "FAIL", "private branch only"),
        ("CG2543_1_boundary_zero", "boundary/improvement flux zero", "FAIL", "primary blocker"),
        ("CG2543_2_spin_zero", "spin/torsion hypermomentum zero", "FAIL", "separate guard"),
        ("CG2543_3_P4_score", "remaining residuals score-ready", "FAIL", "values/maps/bounds missing"),
        ("CG2543_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "boundary/spin/formal adoption still open"),
        ("CG2543_5_github", "safe public evidence update", "FAIL", "private checkpoint only"),
    ]
    return [stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}) for row_id, gate, status, effect in rows]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2543_0_projective_as_public", "projective trace is solved globally", "false", "zero is private owned-coframe+SRNG only; affine fallback retained"),
        ("REF2543_1_SRNG_solves_boundary", "SRNG solves boundary/improvement flux", "false", "boundary flux is an integration/source-normalization obstruction, not a readout Gamma slot"),
        ("REF2543_2_boundary_by_notation", "B_zero_flux=0 by choosing a reference", "false", "reference must be fixed before readout and sourced; no fitted cancellation"),
        ("REF2543_3_local_gr", "2543 proves local GR/Newton", "false", "2543 narrows residuals but leaves boundary, spin and formal private-clause adoption open"),
    ]
    return [stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason}) for row_id, claim, allowed, reason in rows]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2543_0_selected",
            "selected",
            "2544-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md",
            "scripts/Y5_R2FR_boundary_no_flux_theorem_or_Bzero_first_bound_row_2544.py",
            "derive compact boundary no-flux / Hilbert flux closure theorem for B_zero_flux",
            "if theorem fails, emit first source-backed B_zero_flux bound row in GM-flux or dimensionless units",
        ),
        (
            "NEXT2543_1_parallel",
            "parallel",
            "2544b-Y5-R2FR-spin-coframe-owned-connection-proof-or-axial-torsion-bound.md",
            "scripts/Y5_R2FR_spin_coframe_owned_connection_proof_or_axial_torsion_bound_2544b.py",
            "prove spin connection is coframe-owned or bound axial torsion source response",
            "retain E_spin residual if not closed",
        ),
        (
            "NEXT2543_2_fallback",
            "fallback",
            "2544c-Y5-R2FR-affine-projective-kernel-if-private-branch-rejected.md",
            "scripts/Y5_R2FR_affine_projective_kernel_if_private_branch_rejected_2544c.py",
            "build projective trace residual kernel for global affine fallback",
            "keep nonclaim unless sourced and same-frame",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "priority": priority,
                "next_file": next_file,
                "next_script": next_script,
                "success_condition": success,
                "fallback_condition": fallback,
            }
        )
        for row_id, priority, next_file, next_script, success, fallback in rows
    ]


def branch_copy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for copy_id, destination in BRANCH_COPIES.items():
        source = OUTPUTS[copy_id]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": rel(source),
                    "destination_path": rel(destination),
                    "destination_exists": str(destination.exists()).lower(),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        if not changed:
            return True, "git modified-file count for formalization-workbench is 0"
        return False, f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or row.get("copy_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() in {"true", "pass", "passed", "ready", "yes", "1"}:
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2543_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2543_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2543_02_outputs_exist", all(path.exists() for path in generated), "all 2543 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2543_03_csv_parse", parse_ok, parse_detail)

    split = read_csv(outputs["split"])
    projective = read_csv(outputs["projective"])
    boundary = read_csv(outputs["boundary"])
    gate = read_csv(outputs["gate"])
    claims = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])

    add(
        "VAL2543_04_split_verdict",
        any(row["row_id"] == "RSL2543_4_verdict" and "boundary" in row["next_action"].lower() for row in split),
        "residual split verdict recorded",
    )
    add(
        "VAL2543_05_projective_private_zero",
        any(row["row_id"] == "PRJ2543_0_candidate_zero" and row["status"] == "ZERO_INSIDE_PRIVATE_BRANCH_ONLY" for row in projective),
        "projective zero switch private only",
    )
    add(
        "VAL2543_06_projective_fallback_retained",
        any(row["row_id"] == "PRJ2543_2_affine_fallback" and row["status"] == "FALLBACK_RETAINED" for row in projective),
        "affine projective fallback retained",
    )
    add(
        "VAL2543_07_boundary_queue_live",
        any(row["row_id"] == "BND2543_0_B_zero_flux" and row["status"] == "MISSING_THEOREM_OR_VALUE" for row in boundary),
        "B_zero boundary row remains live",
    )
    add(
        "VAL2543_08_boundary_primary",
        any(row["row_id"] == "RCG2543_2_boundary_live" and row["status"] == "PRIMARY_LIVE_BLOCKER" for row in gate),
        "boundary selected as primary live blocker",
    )
    add(
        "VAL2543_09_local_claims_block",
        any(row["row_id"] == "CG2543_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in claims),
        "local GR/Newton claim gate remains false",
    )
    add(
        "VAL2543_10_next_boundary_no_flux",
        any(row["row_id"] == "NEXT2543_0_selected" for row in next_rows),
        "boundary no-flux target selected next",
    )
    add(
        "VAL2543_11_github_blocked",
        any(row["row_id"] == "CG2543_5_github" and row["gate_status"] == "FAIL" for row in claims),
        "public GitHub evidence update remains blocked",
    )

    copy_rows = read_csv(outputs["copies"])
    add("VAL2543_12_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2543_13_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2543_14_formalization_untouched", formal_ok, formal_detail)
    add("VAL2543_15_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2543_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2543 valid: residuals split under private SRNG, projective zero private only, affine fallback retained, boundary no-flux selected next" if overall else "one or more validation gates failed",
            }
        )
    )
    return rows


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    split = read_csv(outputs["split"])
    projective = read_csv(outputs["projective"])
    boundary = read_csv(outputs["boundary"])
    gate = read_csv(outputs["gate"])
    claims = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2543 - Boundary / Projective Residual Split Under Private SRNG

## Result

Using the private `SRNG/OFC` branch, the connection residual now splits cleanly:

`Delta_abs_private = Delta_spin + Delta_boundary + Delta_improvement + 0_projective_private`.

Projective trace is zero only inside the private owned-coframe + SRNG branch, by variable absence. This is not a public/global result; the affine/projective fallback remains retained.

Boundary/improvement flux is not solved by SRNG. It is now the primary live blocker for the local Newton/GR source-normalization route:

`B_zero_flux` must either be derived zero by compact boundary/Hilbert flux closure, or filled as a finite source-backed bound row.

Spin/torsion remains a parallel guard.

## Residual Split Ledger

{table(["row_id", "component", "private_SRNG_status", "public_status", "next_action"], split)}

## Projective Status Under Private SRNG

{table(["row_id", "branch", "projective_current", "status", "reason"], projective)}

## Boundary Improvement Queue

{table(["row_id", "boundary_object", "status", "needed_input"], boundary)}

## Reduced Connection Gate

{table(["row_id", "gate", "status", "claim_effect"], gate)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], claims)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["split"])}`
- `{rel(outputs["projective"])}`
- `{rel(outputs["boundary"])}`
- `{rel(outputs["gate"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a useful reduction. The private SRNG branch removes the source/readout/projective clutter from the immediate internal path, but does not create a public claim. The main blocker is now boundary/improvement flux: prove no-flux or quantify `B_zero_flux`.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["split"], residual_split_ledger())
    write_csv(OUTPUTS["projective"], projective_status_under_private_srng())
    write_csv(OUTPUTS["boundary"], boundary_improvement_queue())
    write_csv(OUTPUTS["gate"], reduced_connection_gate())
    write_csv(OUTPUTS["claims"], claim_gates())
    write_csv(OUTPUTS["refusal"], refusal_runner())
    write_csv(OUTPUTS["next"], next_target())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
