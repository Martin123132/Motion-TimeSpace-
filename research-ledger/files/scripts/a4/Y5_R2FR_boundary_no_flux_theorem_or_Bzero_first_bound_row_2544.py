from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2544"
BRANCH_ID = "MTS_R2FR_BOUNDARY_NO_FLUX_OR_BZERO_FIRST_BOUND_ROW_2544"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2544-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2544_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_NO_SHADOW_2544_BZERO_NOFLUX_THEOREM_AUDIT.csv",
    "bound": RESIDUALS / "P8_Y5_NO_SHADOW_2544_BZERO_FIRST_BOUND_ROW.csv",
    "dependencies": RESIDUALS / "P8_Y5_NO_SHADOW_2544_BOUNDARY_DENOMINATOR_DEPENDENCY.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2544_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2544_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2544_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2544_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2544_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2544_VALIDATION.csv",
}

BRANCH_COPIES = {
    "theorem": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Bzero_no_flux_theorem_audit_2544_NONCLAIM.csv",
    "bound": POST_ROOT / "source-intake" / "local_bounds" / "Bzero_first_bound_row_2544_NONCLAIM.csv",
    "dependencies": POST_ROOT / "source-intake" / "local_bounds" / "Boundary_denominator_dependency_2544_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "THETA_QTAU_MHREF2544_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2544_0_2543_doc", "2543-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md", "NEXT2543_0_selected", "2543 selected boundary no-flux target"),
    ("SRC2544_1_2543_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2543_VALIDATION.csv", "VAL2543_OVERALL,PASS", "2543 validation anchor"),
    ("SRC2544_2_2543_boundary", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_BOUNDARY_IMPROVEMENT_QUEUE.csv", "BND2543_0_B_zero_flux", "current boundary queue"),
    ("SRC2544_3_2543_gate", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_REDUCED_CONNECTION_GATE.csv", "RCG2543_2_boundary_live", "current reduced gate"),
    ("SRC2544_4_2379_doc", "2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md", "BZT2379_6_verdict", "older Bzero theorem precedent"),
    ("SRC2544_5_2379_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2379_VALIDATION.csv", "VAL2379_OVERALL", "2379 validation anchor"),
    ("SRC2544_6_2379_theorem", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2379_BZERO_NOFLUX_THEOREM_AUDIT.csv", "BZT2379_6_verdict", "Bzero no-flux theorem audit precedent"),
    ("SRC2544_7_2379_bound", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2379_BZERO_FIRST_BOUND_ROW.csv", "BZR2379_0_first_row", "Bzero first bound row precedent"),
    ("SRC2544_8_2379_dependencies", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2379_BOUNDARY_DENOMINATOR_DEPENDENCY.csv", "BDD2379_2_MHref", "boundary denominator dependencies precedent"),
    ("SRC2544_9_2379_decision", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2379_DECISION_LEDGER.csv", "DEC2379_2_next", "decision precedent"),
    ("SRC2544_10_2379_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2379_NEXT_TARGET.csv", "NEXT2379_0_selected", "theta/Qtau/MHref next target precedent"),
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


def bzero_no_flux_theorem_audit() -> list[dict[str, object]]:
    rows = [
        (
            "BZT2544_0_target",
            "B_zero_flux theorem target",
            "B_zero_flux=0 for compact linked surfaces if the parent boundary/reference/improvement current is fixed, exact or carries zero compact flux before readout.",
            "TARGET_SHARPENED",
            "requires parent theta/Q_tau, fixed reference, boundary conditions, compact support/falloff, positive M_H_ref and no extra hidden charge",
            "stage B_zero_flux/M_H_ref absolute residual row",
        ),
        (
            "BZT2544_1_parent_symplectic",
            "parent theta/Q_tau extraction",
            "delta L_parent = E_A delta Phi^A + d theta_MTS and Q_tau^MTS exists for the same observed tau used by source, clocks and orbital readout.",
            "MISSING_PARENT_THETA_QTAU",
            "parent symplectic/Noether structure remains unsigned",
            "epsilon_HPiM_integrability_abs component",
        ),
        (
            "BZT2544_2_fixed_reference",
            "fixed reference/counterterm",
            "H_ref and boundary representative are chosen before source/readout and cannot be fitted to cancel B_zero_flux.",
            "MISSING_FIXED_REFERENCE",
            "reference/counterterm convention and selector source remain unowned",
            "B_zero_flux_over_MH absolute numerator",
        ),
        (
            "BZT2544_3_compact_support",
            "compact support/falloff",
            "The exterior annulus has no source support and linked surfaces carry no improvement flux through the caps/corners.",
            "CONDITIONAL_WORLDTUBE_NOT_SIGNED",
            "worldtube/source selector and linking surfaces are contract-ready but not current-MTS theorem",
            "Delta_worldtube_domain and B_zero_flux terms",
        ),
        (
            "BZT2544_4_Hilbert_topological_equality",
            "Hilbert/topological equality",
            "Pi_M J_H = J_M_top + dB_zero and integral_boundary dB_zero=0 in the linked compact exterior.",
            "MISSING_EQUALITY_THEOREM",
            "closed topological charge can be the wrong charge; projector algebra is not flux closure",
            "R_eq_integral + I_commutator + B_zero_flux",
        ),
        (
            "BZT2544_5_denominator",
            "positive same-frame denominator",
            "B_zero_flux is scoreable only after M_H_ref=H_tau-H_ref is positive, finite, same-frame and source-backed.",
            "MISSING_MHREF",
            "M_H_ref has no claim-valid theorem-zero or data row",
            "keep first B_zero row non-score-ready",
        ),
        (
            "BZT2544_6_verdict",
            "B_zero_flux=0 now",
            "BZT2544_1 through BZT2544_5 all parent-signed would imply B_zero_flux=0 or a scoreable normalized boundary residual.",
            "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW",
            "the zero theorem stack is exact but unsigned in the current corpus",
            "Bzero first bound row with valid_for_claim=false",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "clause": clause,
            "mathematical_statement": statement,
            "status": status,
            "obstruction": obstruction,
            "fallback": fallback,
        }
        for row_id, clause, statement, status, obstruction, fallback in rows
    ]


def bzero_first_bound_row() -> list[dict[str, object]]:
    rows = [
        (
            "BZR2544_0_first_row",
            "epsilon_Bzero_abs",
            "epsilon_Bzero_abs := abs(B_zero_flux) / M_H_ref",
            "B_zero_flux",
            "M_H_ref",
            "dimensionless after GM/source normalization",
            "MISSING_B_ZERO_FLUX;MISSING_M_H_REF",
            "finite B_zero_flux; positive same-frame M_H_ref; source path; equation ref; fixed-reference certificate; no-cancellation guard",
            "SCHEMA_READY_VALUES_MISSING",
        ),
        (
            "BZR2544_1_zero_switch",
            "B_zero_flux_zero",
            "theorem_zero=true iff parent-signed boundary no-flux theorem supplies BZT2544_1..5",
            "0 if theorem signed",
            "M_H_ref still recorded for units/audit",
            "boolean theorem switch plus dimensionless audit row",
            "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNATURE",
            "parent theta/Q_tau; fixed reference; compact support; Hilbert/topological equality; positive M_H_ref",
            "ZERO_SWITCH_BLOCKED",
        ),
        (
            "BZR2544_2_absolute_sum_guard",
            "epsilon_boundary_abs",
            "epsilon_boundary_abs >= abs(B_zero_flux)/M_H_ref + abs(Delta_symp)/M_H_ref + abs(Delta_worldtube_domain) + abs(I_commutator)/M_H_ref",
            "B_zero_flux;Delta_symp;Delta_worldtube_domain;I_commutator",
            "M_H_ref or dimensionless component normalization",
            "dimensionless absolute envelope",
            "MISSING_COMPONENT_INPUTS",
            "all components finite, sourced, same-frame and absolute-summed",
            "NO_CANCELLATION_GUARD_READY_VALUES_MISSING",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "numerator": numerator,
            "denominator": denominator,
            "units": units,
            "current_value": value,
            "required_for_claim": required,
            "status": status,
        }
        for row_id, quantity, formula, numerator, denominator, units, value, required, status in rows
    ]


def boundary_denominator_dependency() -> list[dict[str, object]]:
    rows = [
        (
            "BDD2544_0_theta_Qtau",
            "theta_MTS and Q_tau^MTS",
            "defines the actual parent boundary charge rather than importing EH charge",
            "MISSING_PARENT_EXTRACTION",
            "B_zero theorem and H_tau integrability",
            "parent theta/Q_tau extraction or decomposition ledger",
        ),
        (
            "BDD2544_1_fixed_reference",
            "fixed H_ref/counterterm",
            "prevents fitted boundary cancellation",
            "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "B_zero numerator and M_H_ref denominator",
            "fixed reference selector source",
        ),
        (
            "BDD2544_2_MHref",
            "positive same-frame M_H_ref",
            "normalizes every B_zero/R_eq/I_commutator row",
            "MISSING_M_H_REF",
            "score-ready boundary row",
            "H_tau-H_ref first row or theorem",
        ),
        (
            "BDD2544_3_worldtube",
            "worldtube/linking-surface selector",
            "defines the compact boundary pair and exterior annulus before readout",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "compact no-flux theorem",
            "support selector and compactness/falloff proof",
        ),
        (
            "BDD2544_4_PiM_equality",
            "Pi_M J_H = J_M_top + dB_zero",
            "prevents conserved-wrong-object error",
            "MISSING_EQUALITY_THEOREM",
            "Newton/source-normalization claim",
            "Hilbert/topological equality or R_eq bound",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "dependency": dep,
            "why_needed": why,
            "current_status": status,
            "blocks": blocks,
            "next_input": next_input,
        }
        for row_id, dep, why, status, blocks, next_input in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "DEC2544_0_theorem_result",
            "B_zero_flux zero theorem not derived",
            "theta/Q_tau, fixed reference, compact support, Hilbert/topological equality and M_H_ref are unsigned",
            "retain Bzero bound row",
            "ZERO_THEOREM_FAILED_CLEANLY",
        ),
        (
            "DEC2544_1_bound_row",
            "stage first Bzero bound row",
            "this gives the next executable object without claiming a value",
            "epsilon_Bzero_abs schema ready but non-score-ready",
            "FIRST_BOUND_ROW_STAGED_NONCLAIM",
        ),
        (
            "DEC2544_2_next",
            "attack parent theta/Qtau fixed-reference denominator next",
            "Bzero cannot be scored until the boundary charge and M_H_ref are owned",
            "next target moves to theta/Q_tau/H_ref/M_H_ref extraction",
            "SELECT_THETA_QTAU_FIXED_REFERENCE_NEXT",
        ),
        (
            "DEC2544_3_public_policy",
            "no GitHub evidence update",
            "boundary obstruction is still open and local-GR/Newton remains blocked",
            "private checkpoint only",
            "NO_GITHUB_EVIDENCE_UPDATE",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "decision": decision,
                "reason": reason,
                "consequence": consequence,
                "status": status,
            }
        )
        for row_id, decision, reason, consequence, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2544_0_Bzero_zero", "B_zero_flux=0 theorem derived", "FAIL", "zero theorem blocked"),
        ("CG2544_1_Bzero_bound_score", "Bzero first row score-ready", "FAIL", "missing numerator and M_H_ref"),
        ("CG2544_2_fixed_reference", "fixed reference/counterterm signed", "FAIL", "fitted-reference guard remains live"),
        ("CG2544_3_MHref", "positive same-frame M_H_ref exists", "FAIL", "normalization blocked"),
        ("CG2544_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "boundary/source-normalization still blocks"),
        ("CG2544_5_github", "safe public evidence update", "FAIL", "private checkpoint only"),
    ]
    return [stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}) for row_id, gate, status, effect in rows]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2544_0_reference_zero", "B_zero_flux=0 by choosing the reference", "false", "fixed reference must be parent-owned before readout; fitted cancellation is refused"),
        ("REF2544_1_EH_import", "use EH boundary charge as the MTS boundary charge", "false", "MTS theta/Q_tau must be extracted or EH reduction proven first"),
        ("REF2544_2_unnormalized_bound", "score B_zero_flux without M_H_ref", "false", "Bzero row needs positive same-frame denominator and units"),
        ("REF2544_3_local_gr", "2544 proves local GR/Newton", "false", "2544 stages a nonclaim boundary row and leaves source-normalization gates open"),
    ]
    return [stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason}) for row_id, claim, allowed, reason in rows]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2544_0_selected",
            "selected",
            "2545-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md",
            "scripts/Y5_R2FR_parent_theta_Qtau_fixed_reference_or_MHref_first_row_2545.py",
            "own the parent boundary charge, fixed reference and positive same-frame M_H_ref denominator",
            "if theorem extraction fails, stage first M_H_ref/H_ref row as nonclaim",
        ),
        (
            "NEXT2544_1_parallel",
            "parallel",
            "2545b-Y5-R2FR-Hilbert-topological-equality-or-Req-bound.md",
            "scripts/Y5_R2FR_Hilbert_topological_equality_or_Req_bound_2545b.py",
            "prove Pi_M J_H equals the measured/topological charge or produce R_eq",
            "retain R_eq/I_commutator if not closed",
        ),
        (
            "NEXT2544_2_fallback",
            "fallback",
            "2545c-Y5-R2FR-Bzero-source-backed-numerator-acquisition.md",
            "scripts/Y5_R2FR_Bzero_source_backed_numerator_acquisition_2545c.py",
            "source finite B_zero numerator and units without claiming a pass",
            "keep nonclaim until denominator and fixed-reference certificate exist",
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
    add("VAL2544_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2544_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2544_02_outputs_exist", all(path.exists() for path in generated), "all 2544 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2544_03_csv_parse", parse_ok, parse_detail)

    theorem = read_csv(outputs["theorem"])
    bound = read_csv(outputs["bound"])
    deps = read_csv(outputs["dependencies"])
    decisions = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])

    add(
        "VAL2544_04_zero_theorem_not_derived",
        any(row["row_id"] == "BZT2544_6_verdict" and row["status"] == "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW" for row in theorem),
        "Bzero zero theorem not promoted",
    )
    add(
        "VAL2544_05_bound_row_staged",
        any(row["row_id"] == "BZR2544_0_first_row" and row["status"] == "SCHEMA_READY_VALUES_MISSING" for row in bound),
        "Bzero first bound row exists",
    )
    add(
        "VAL2544_06_dependencies_named",
        any(row["row_id"] == "BDD2544_0_theta_Qtau" for row in deps)
        and any(row["row_id"] == "BDD2544_2_MHref" for row in deps),
        "theta/Qtau, fixed reference and MHref dependencies named",
    )
    add(
        "VAL2544_07_next_selected",
        any(row["row_id"] == "DEC2544_2_next" and row["status"] == "SELECT_THETA_QTAU_FIXED_REFERENCE_NEXT" for row in decisions)
        and any(row["row_id"] == "NEXT2544_0_selected" for row in next_rows),
        "theta/Qtau fixed-reference next selected",
    )
    add(
        "VAL2544_08_local_claims_block",
        any(row["row_id"] == "CG2544_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
        "local GR/Newton claim gate remains false",
    )
    add(
        "VAL2544_09_github_blocked",
        any(row["row_id"] == "CG2544_5_github" and row["gate_status"] == "FAIL" for row in gates),
        "public GitHub evidence update remains blocked",
    )

    copy_rows = read_csv(outputs["copies"])
    add("VAL2544_10_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2544_11_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2544_12_formalization_untouched", formal_ok, formal_detail)
    add("VAL2544_13_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2544_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2544 valid: Bzero no-flux theorem not promoted, first nonclaim Bzero row staged, theta/Qtau fixed-reference/MHref selected next" if overall else "one or more validation gates failed",
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
    theorem = read_csv(outputs["theorem"])
    bound = read_csv(outputs["bound"])
    deps = read_csv(outputs["dependencies"])
    decisions = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2544 - Boundary no-Flux Theorem Or Bzero First Bound Row

## Result

The boundary no-flux route is now explicit but not closed.

Target:

`B_zero_flux = 0`

for compact linked source boundaries, if the parent boundary/reference/improvement current is fixed, exact, or carries zero compact flux before readout.

The obstruction is not vague: the branch needs parent `theta_MTS/Q_tau^MTS`, a fixed reference/counterterm, compact support/falloff, Hilbert/topological equality, and a positive same-frame `M_H_ref`.

Because those are unsigned, the honest row is:

`epsilon_Bzero_abs := abs(B_zero_flux) / M_H_ref`.

It is schema-ready only, not score-ready. Next target is parent theta/Qtau + fixed reference + `M_H_ref`.

## Bzero no-Flux Theorem Audit

{table(["row_id", "clause", "status", "obstruction"], theorem)}

## Bzero First Bound Row

{table(["row_id", "quantity", "current_value", "status", "required_for_claim"], bound)}

## Boundary Denominator Dependency

{table(["row_id", "dependency", "current_status", "blocks", "next_input"], deps)}

## Decision Ledger

{table(["row_id", "decision", "status", "consequence"], decisions)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], gates)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["theorem"])}`
- `{rel(outputs["bound"])}`
- `{rel(outputs["dependencies"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is the real boundary bottleneck in plain sight. We are no longer saying "boundary term maybe"; we have a normalized residual object and the exact missing denominator/reference stack. No local GR/Newton claim follows until that stack is owned.
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
    write_csv(OUTPUTS["theorem"], bzero_no_flux_theorem_audit())
    write_csv(OUTPUTS["bound"], bzero_first_bound_row())
    write_csv(OUTPUTS["dependencies"], boundary_denominator_dependency())
    write_csv(OUTPUTS["decision"], decision_ledger())
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
