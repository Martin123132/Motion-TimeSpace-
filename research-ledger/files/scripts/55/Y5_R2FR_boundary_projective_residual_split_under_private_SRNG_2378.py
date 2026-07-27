from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_BOUNDARY_PROJECTIVE_SPLIT_UNDER_PRIVATE_SRNG_2378"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2378-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


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
    sources = [
        ("SRC2378_2377_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2377_NEXT_TARGET.csv", "NEXT2377_0_selected", "2377 selected boundary/projective residual split"),
        ("SRC2378_2377_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2377_VALIDATION.csv", "VAL2377_OVERALL", "2377 validation"),
        ("SRC2378_2377_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2377_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv", "P4A2377_4_reduced_total", "2377 reduced residual status"),
        ("SRC2378_2337_split", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2337_RESIDUAL_SPLIT_LEDGER.csv", "RSL2337_4_verdict", "2337 residual split ledger"),
        ("SRC2378_2337_projective", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2337_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv", "PRJ2337_3_verdict", "2337 projective status"),
        ("SRC2378_2337_boundary", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2337_BOUNDARY_IMPROVEMENT_QUEUE.csv", "BND2337_4_priority", "2337 boundary queue"),
        ("SRC2378_2337_gate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2337_REDUCED_CONNECTION_GATE.csv", "RCG2337_2_boundary_live", "2337 reduced connection gate"),
        ("SRC2378_2337_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2337_NEXT_TARGET.csv", "NEXT2337_0", "2337 boundary no-flux next target"),
        ("SRC2378_2337_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2337_VALIDATION.csv", "VAL2337_OVERALL", "2337 validation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def residual_split_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "RSL2378_0_private_total",
            "Delta_abs_private_SRNG_branch",
            "Delta_source/clock/light/orbit zeroed by private SRNG/OFC",
            "not a public theorem",
            "split spin, boundary, projective",
        ),
        (
            "RSL2378_1_spin",
            "Delta_spin",
            "still live unless owned-coframe spin connection is parent-signed",
            "live",
            "spin/coframe-owned connection theorem or axial-torsion bound",
        ),
        (
            "RSL2378_2_boundary",
            "Delta_boundary + Delta_improvement",
            "still live; SRNG does not fix integration-boundary flux",
            "live",
            "derive B_zero_flux=0 / compact flux closure or fill boundary bound",
        ),
        (
            "RSL2378_3_projective_private",
            "Delta_projective",
            "zero inside private owned-coframe+SRNG branch by variable absence",
            "global affine fallback retained",
            "record private zero switch and keep affine fallback policy",
        ),
        (
            "RSL2378_4_verdict",
            "connection residual split",
            "projective reduced; boundary remains hard live channel; spin remains separate guard",
            "no local-GR/Newton claim",
            "boundary no-flux/Hilbert flux closure first",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
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
            "PRJ2378_0_candidate_zero",
            "private owned-coframe + SRNG/OFC",
            "0",
            "Gamma_ind is not a variable and source/readout exceptions are excluded by private SRNG",
            "ZERO_INSIDE_PRIVATE_BRANCH_ONLY",
        ),
        (
            "PRJ2378_1_public_global",
            "full current corpus",
            "not globally zero",
            "SRNG/OFC and owned-coframe are private working clauses, not public parent-signed theorems",
            "PUBLIC_CERTIFICATE_BLOCKED",
        ),
        (
            "PRJ2378_2_affine_fallback",
            "independent affine fallback",
            "P_projective[source,clock,WEP]",
            "if Gamma_ind is retained, projective trace needs an unobservable/gauge/fixed proof or numeric kernel",
            "FALLBACK_RETAINED",
        ),
        (
            "PRJ2378_3_verdict",
            "decision",
            "zero only in private branch",
            "private SRNG/owned-coframe collapses candidate-branch projective issue, not global affine branch",
            "PRIVATE_ZERO_PUBLIC_NONCLAIM",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
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
            "BND2378_0_B_zero_flux",
            "B_zero_flux",
            "exact/reference/boundary improvement flux through compact linked boundary",
            "MISSING_THEOREM_OR_VALUE",
            "GM_flux_or_dimensionless after source normalization",
            "boundary no-flux theorem, compact support/falloff, source path, no-cancellation guard",
        ),
        (
            "BND2378_1_worldtube_flux",
            "finite-annulus flux leakage",
            "M_eff^-1 int_A d(Pi_M J_H) or dln_Meff_dt / radial envelope",
            "MISSING_TIME_RADIAL_PROFILE_OR_THEOREM",
            "yr^-1 or dimensionless radial envelope",
            "worldtube glue, Pi_M ownership, same-frame M_H_ref, flux closure",
        ),
        (
            "BND2378_2_projector_commutator",
            "[d,Pi_M]J_H + R_eq",
            "projector/domain variation and topological-Hilbert mismatch",
            "MISSING_COMMUTATOR_OR_EQUALITY_THEOREM",
            "dimensionless or GM flux units",
            "Pi_M J_H = J_M_top + dB_zero, I_commutator, Delta_PiM",
        ),
        (
            "BND2378_3_improvement_representative",
            "improvement/superpotential representative",
            "choice of Hamiltonian representative and exact flux class",
            "MISSING_FIXED_REPRESENTATIVE",
            "source-current units",
            "fixed boundary/reference convention before readout",
        ),
        (
            "BND2378_4_priority",
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
            "branch_id": BRANCH_ID,
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
            "RCG2378_0_private_formula",
            "private SRNG reduced connection residual",
            "Delta_abs_private = Delta_spin + Delta_boundary + Delta_improvement + 0_projective_private",
            "PRIVATE_BRANCH_REDUCTION_ONLY",
            "narrows internal work; no public pass",
        ),
        (
            "RCG2378_1_projective_private_zero",
            "projective trace inside private branch",
            "Delta_projective_private=0 by no Gamma_ind variable and SRNG source/readout exclusion",
            "PRIVATE_ZERO_SWITCH",
            "projective no longer first priority inside private branch",
        ),
        (
            "RCG2378_2_boundary_live",
            "boundary/improvement closure",
            "Delta_boundary requires B_zero_flux/worldtube/commutator/improvement proof or bound",
            "PRIMARY_LIVE_BLOCKER",
            "Newton/GM/local-GR still blocked",
        ),
        (
            "RCG2378_3_public_gate",
            "public local GR/Newton bridge",
            "all private clauses must be derived/adopted in formal spine plus boundary/spin closed",
            "BLOCKED_NONCLAIM",
            "do not publish as evidence",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "formula": formula,
            "status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, formula, status, effect in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2378_0_projective_public_zero", "projective trace globally zero", "FAIL", "private branch only"),
        ("CG2378_1_boundary_zero", "boundary/improvement flux zero", "FAIL", "primary blocker"),
        ("CG2378_2_spin_zero", "spin/torsion hypermomentum zero", "FAIL", "separate guard"),
        ("CG2378_3_P4_score", "remaining residuals score-ready", "FAIL", "values/maps/bounds missing"),
        ("CG2378_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "boundary/spin/formal adoption still open"),
        ("CG2378_5_github", "safe public evidence update", "FAIL", "private checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "gate_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2378_0_projective_as_public", "projective trace is solved globally", "false", "zero is private owned-coframe+SRNG only; affine fallback retained"),
        ("REF2378_1_SRNG_solves_boundary", "SRNG solves boundary/improvement flux", "false", "boundary flux is an integration/source-normalization obstruction, not a readout Gamma slot"),
        ("REF2378_2_boundary_by_notation", "B_zero_flux=0 by choosing a reference", "false", "reference must be fixed before readout and sourced; no fitted cancellation"),
        ("REF2378_3_local_gr", "2378 proves local GR/Newton", "false", "2378 narrows residuals but leaves boundary, spin and formal private-clause adoption open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, allowed, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2378_0_selected",
            "2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md",
            "scripts/Y5_R2FR_boundary_no_flux_theorem_or_Bzero_first_bound_row_2379.py",
            "derive compact boundary no-flux / Hilbert flux closure theorem for B_zero_flux",
            "if theorem fails, emit first source-backed B_zero_flux bound row in GM-flux or dimensionless units",
        ),
        (
            "NEXT2378_1_parallel",
            "2379b-Y5-R2FR-spin-coframe-owned-connection-proof-or-axial-torsion-bound.md",
            "scripts/Y5_R2FR_spin_coframe_owned_connection_proof_or_axial_torsion_bound_2379b.py",
            "prove spin connection is coframe-owned or bound axial torsion source response",
            "retain E_spin residual if not closed",
        ),
        (
            "NEXT2378_2_fallback",
            "2379c-Y5-R2FR-affine-projective-kernel-if-private-branch-rejected.md",
            "scripts/Y5_R2FR_affine_projective_kernel_if_private_branch_rejected_2379c.py",
            "build projective trace residual kernel for global affine fallback",
            "keep nonclaim unless sourced and same-frame",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "next_file": file_name,
            "next_script": script_name,
            "success_condition": success,
            "fallback_condition": fallback,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, file_name, script_name, success, fallback in rows
    ]


def all_output_files() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_SOURCE_REGISTER.csv",
        "split_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_RESIDUAL_SPLIT_LEDGER.csv",
        "projective_status": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv",
        "boundary_queue": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_BOUNDARY_IMPROVEMENT_QUEUE.csv",
        "reduced_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_REDUCED_CONNECTION_GATE.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2378_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2378_VALIDATION.csv",
    }


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    sensitive = {
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    }
    positive_values = {"true", "pass", "passed", "ready", "yes", "1"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in sensitive and str(value).strip().lower() in positive_values:
                    return False
    return True


def validation_rows(outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(outputs["source_register"])
    generated_paths = [path for key, path in outputs.items() if key != "validation"]
    parsed_ok = True
    for path in generated_paths:
        try:
            parsed_ok = parsed_ok and bool(read_csv(path))
        except Exception:
            parsed_ok = False

    split = read_csv(outputs["split_ledger"])
    projective = read_csv(outputs["projective_status"])
    boundary = read_csv(outputs["boundary_queue"])
    gate = read_csv(outputs["reduced_gate"])
    claims = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        ("VAL2378_00_required_sources_exist", all(row["path_exists"] == "true" for row in source_rows), "all required source paths exist"),
        ("VAL2378_01_required_needles_found", all(row["needle_found"] == "true" for row in source_rows), "all source needles found"),
        ("VAL2378_02_outputs_exist", all(path.exists() for path in generated_paths), "all 2378 output files written"),
        ("VAL2378_03_csv_parse", parsed_ok, "all generated CSV files parse and contain rows"),
        (
            "VAL2378_04_split_verdict",
            any(row["row_id"] == "RSL2378_4_verdict" and "boundary" in row["next_action"].lower() for row in split),
            "residual split verdict recorded",
        ),
        (
            "VAL2378_05_projective_private_zero",
            any(row["row_id"] == "PRJ2378_0_candidate_zero" and row["status"] == "ZERO_INSIDE_PRIVATE_BRANCH_ONLY" for row in projective),
            "projective zero switch private only",
        ),
        (
            "VAL2378_06_projective_fallback_retained",
            any(row["row_id"] == "PRJ2378_2_affine_fallback" and row["status"] == "FALLBACK_RETAINED" for row in projective),
            "affine projective fallback retained",
        ),
        (
            "VAL2378_07_boundary_queue_live",
            any(row["row_id"] == "BND2378_0_B_zero_flux" and row["status"] == "MISSING_THEOREM_OR_VALUE" for row in boundary),
            "B_zero boundary row remains live",
        ),
        (
            "VAL2378_08_boundary_primary",
            any(row["row_id"] == "RCG2378_2_boundary_live" and row["status"] == "PRIMARY_LIVE_BLOCKER" for row in gate),
            "boundary selected as primary live blocker",
        ),
        (
            "VAL2378_09_local_claims_block",
            any(row["row_id"] == "CG2378_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in claims),
            "local GR/Newton claim gate remains false",
        ),
        (
            "VAL2378_10_next_boundary_no_flux",
            any(row["row_id"] == "NEXT2378_0_selected" for row in next_rows),
            "boundary no-flux target selected next",
        ),
        (
            "VAL2378_11_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2378_12_formalization_untouched",
            not any(FORMALIZATION_WORKBENCH in path.parents for path in generated_paths),
            "generator writes only under post-checkpoint-work",
        ),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2378_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2378 valid: residuals split under private SRNG, projective zero private only, affine fallback retained, boundary no-flux selected next"
            if overall_ok
            else "2378 validation failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    split = read_csv(outputs["split_ledger"])
    projective = read_csv(outputs["projective_status"])
    boundary = read_csv(outputs["boundary_queue"])
    gate = read_csv(outputs["reduced_gate"])
    claims = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]

    text = f"""# 2378 - Boundary / Projective Residual Split Under Private SRNG

## Result

Using the private `SRNG/OFC` branch, the connection residual now splits cleanly:

`Delta_abs_private = Delta_spin + Delta_boundary + Delta_improvement + 0_projective_private`.

Projective trace is zero only inside the private owned-coframe + SRNG branch, by variable absence.  This is not a public/global result; the affine/projective fallback remains retained.

Boundary/improvement flux is not solved by SRNG.  It is now the primary live blocker for the local Newton/GR source-normalization route:

`B_zero_flux` must either be derived zero by compact boundary/Hilbert flux closure, or filled as a finite source-backed bound row.

Spin/torsion remains a parallel guard.

## Residual Split Ledger

{md_table(split, ["row_id", "component", "private_SRNG_status", "public_status", "next_action"])}

## Projective Status Under Private SRNG

{md_table(projective, ["row_id", "branch", "projective_current", "status", "reason"])}

## Boundary Improvement Queue

{md_table(boundary, ["row_id", "boundary_object", "status", "needed_input"])}

## Reduced Connection Gate

{md_table(gate, ["row_id", "gate", "status", "claim_effect"])}

## Claim Gates

{md_table(claims, ["row_id", "gate", "gate_status", "claim_effect"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is a useful reduction.  The private SRNG branch removes the source/readout/projective clutter from the immediate internal path, but does not create a public claim.  The main blocker is now boundary/improvement flux: prove no-flux or quantify `B_zero_flux`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["split_ledger"], residual_split_ledger())
    write_csv(outputs["projective_status"], projective_status_under_private_srng())
    write_csv(outputs["boundary_queue"], boundary_improvement_queue())
    write_csv(outputs["reduced_gate"], reduced_connection_gate())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()
