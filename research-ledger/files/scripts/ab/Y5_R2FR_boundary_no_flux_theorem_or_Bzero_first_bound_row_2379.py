from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_BOUNDARY_NO_FLUX_OR_BZERO_FIRST_BOUND_ROW_2379"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md"
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
        ("SRC2379_2378_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_NEXT_TARGET.csv", "NEXT2378_0_selected", "2378 selected boundary no-flux target"),
        ("SRC2379_2378_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2378_VALIDATION.csv", "VAL2378_OVERALL", "2378 validation"),
        ("SRC2379_2378_boundary", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_BOUNDARY_IMPROVEMENT_QUEUE.csv", "BND2378_0_B_zero_flux", "2378 boundary queue"),
        ("SRC2379_2378_gate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_REDUCED_CONNECTION_GATE.csv", "RCG2378_2_boundary_live", "2378 reduced gate"),
        ("SRC2379_2338_theorem", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2338_BZERO_NOFLUX_THEOREM_AUDIT.csv", "BZT2338_6_verdict", "2338 Bzero theorem audit"),
        ("SRC2379_2338_bound", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2338_BZERO_FIRST_BOUND_ROW.csv", "BZR2338_0_first_row", "2338 first Bzero row"),
        ("SRC2379_2338_deps", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2338_BOUNDARY_DENOMINATOR_DEPENDENCY.csv", "BDD2338_2_MHref", "2338 denominator dependencies"),
        ("SRC2379_2338_decision", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2338_DECISION_LEDGER.csv", "DEC2338_2_next", "2338 decision ledger"),
        ("SRC2379_2338_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2338_NEXT_TARGET.csv", "NEXT2338_0", "2338 theta/Qtau next target"),
        ("SRC2379_2338_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2338_VALIDATION.csv", "VAL2338_OVERALL", "2338 validation"),
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


def bzero_no_flux_theorem_audit() -> list[dict[str, object]]:
    rows = [
        (
            "BZT2379_0_target",
            "B_zero_flux theorem target",
            "B_zero_flux=0 for compact linked surfaces if the parent boundary/reference/improvement current is fixed, exact or carries zero compact flux before readout.",
            "TARGET_SHARPENED",
            "requires parent theta/Q_tau, fixed reference, boundary conditions, compact support/falloff, positive M_H_ref and no extra hidden charge",
            "stage B_zero_flux/M_H_ref absolute residual row",
        ),
        (
            "BZT2379_1_parent_symplectic",
            "parent theta/Q_tau extraction",
            "delta L_parent = E_A delta Phi^A + d theta_MTS and Q_tau^MTS exists for the same observed tau used by source, clocks and orbital readout.",
            "MISSING_PARENT_THETA_QTAU",
            "parent symplectic/Noether structure remains unsigned",
            "epsilon_HPiM_integrability_abs component",
        ),
        (
            "BZT2379_2_fixed_reference",
            "fixed reference/counterterm",
            "H_ref and boundary representative are chosen before source/readout and cannot be fitted to cancel B_zero_flux.",
            "MISSING_FIXED_REFERENCE",
            "reference/counterterm convention and selector source remain unowned",
            "B_zero_flux_over_MH absolute numerator",
        ),
        (
            "BZT2379_3_compact_support",
            "compact support/falloff",
            "The exterior annulus has no source support and linked surfaces carry no improvement flux through the caps/corners.",
            "CONDITIONAL_WORLDTUBE_NOT_SIGNED",
            "worldtube/source selector and linking surfaces are contract-ready but not current-MTS theorem",
            "Delta_worldtube_domain and B_zero_flux terms",
        ),
        (
            "BZT2379_4_Hilbert_topological_equality",
            "Hilbert/topological equality",
            "Pi_M J_H = J_M_top + dB_zero and integral_boundary dB_zero=0 in the linked compact exterior.",
            "MISSING_EQUALITY_THEOREM",
            "closed topological charge can be the wrong charge; projector algebra is not flux closure",
            "R_eq_integral + I_commutator + B_zero_flux",
        ),
        (
            "BZT2379_5_denominator",
            "positive same-frame denominator",
            "B_zero_flux is scoreable only after M_H_ref=H_tau-H_ref is positive, finite, same-frame and source-backed.",
            "MISSING_MHREF",
            "M_H_ref has no claim-valid theorem-zero or data row",
            "keep first B_zero row non-score-ready",
        ),
        (
            "BZT2379_6_verdict",
            "B_zero_flux=0 now",
            "BZT2379_1 through BZT2379_5 all parent-signed would imply B_zero_flux=0 or a scoreable normalized boundary residual.",
            "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW",
            "the zero theorem stack is exact but unsigned in the current corpus",
            "Bzero first bound row with valid_for_claim=false",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
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
            "BZR2379_0_first_row",
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
            "BZR2379_1_zero_switch",
            "B_zero_flux_zero",
            "theorem_zero=true iff parent-signed boundary no-flux theorem supplies BZT2379_1..5",
            "0 if theorem signed",
            "M_H_ref still recorded for units/audit",
            "boolean theorem switch plus dimensionless audit row",
            "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNATURE",
            "parent theta/Q_tau; fixed reference; compact support; Hilbert/topological equality; positive M_H_ref",
            "ZERO_SWITCH_BLOCKED",
        ),
        (
            "BZR2379_2_absolute_sum_guard",
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
            "branch_id": BRANCH_ID,
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
            "BDD2379_0_theta_Qtau",
            "theta_MTS and Q_tau^MTS",
            "defines the actual parent boundary charge rather than importing EH charge",
            "MISSING_PARENT_EXTRACTION",
            "B_zero theorem and H_tau integrability",
            "parent theta/Q_tau extraction or decomposition ledger",
        ),
        (
            "BDD2379_1_fixed_reference",
            "fixed H_ref/counterterm",
            "prevents fitted boundary cancellation",
            "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "B_zero numerator and M_H_ref denominator",
            "fixed reference selector source",
        ),
        (
            "BDD2379_2_MHref",
            "positive same-frame M_H_ref",
            "normalizes every B_zero/R_eq/I_commutator row",
            "MISSING_M_H_REF",
            "score-ready boundary row",
            "H_tau-H_ref first row or theorem",
        ),
        (
            "BDD2379_3_worldtube",
            "worldtube/linking-surface selector",
            "defines the compact boundary pair and exterior annulus before readout",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "compact no-flux theorem",
            "support selector and compactness/falloff proof",
        ),
        (
            "BDD2379_4_PiM_equality",
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
            "branch_id": BRANCH_ID,
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
            "DEC2379_0_theorem_result",
            "B_zero_flux zero theorem not derived",
            "theta/Q_tau, fixed reference, compact support, Hilbert/topological equality and M_H_ref are unsigned",
            "retain Bzero bound row",
            "ZERO_THEOREM_FAILED_CLEANLY",
        ),
        (
            "DEC2379_1_bound_row",
            "stage first Bzero bound row",
            "this gives the next executable object without claiming a value",
            "epsilon_Bzero_abs schema ready but non-score-ready",
            "FIRST_BOUND_ROW_STAGED_NONCLAIM",
        ),
        (
            "DEC2379_2_next",
            "attack parent theta/Qtau fixed-reference denominator next",
            "Bzero cannot be scored until the boundary charge and M_H_ref are owned",
            "next target moves to theta/Q_tau/H_ref/M_H_ref extraction",
            "SELECT_THETA_QTAU_FIXED_REFERENCE_NEXT",
        ),
        (
            "DEC2379_3_public_policy",
            "no GitHub evidence update",
            "boundary obstruction is still open and local-GR/Newton remains blocked",
            "private checkpoint only",
            "NO_GITHUB_EVIDENCE_UPDATE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, decision, reason, consequence, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2379_0_Bzero_zero", "B_zero_flux=0 theorem derived", "FAIL", "zero theorem blocked"),
        ("CG2379_1_Bzero_bound_score", "Bzero first row score-ready", "FAIL", "missing numerator and M_H_ref"),
        ("CG2379_2_fixed_reference", "fixed reference/counterterm signed", "FAIL", "fitted-reference guard remains live"),
        ("CG2379_3_MHref", "positive same-frame M_H_ref exists", "FAIL", "normalization blocked"),
        ("CG2379_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "boundary/source-normalization still blocks"),
        ("CG2379_5_github", "safe public evidence update", "FAIL", "private checkpoint only"),
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
        ("REF2379_0_reference_zero", "B_zero_flux=0 by choosing the reference", "false", "fixed reference must be parent-owned before readout; fitted cancellation is refused"),
        ("REF2379_1_EH_import", "use EH boundary charge as the MTS boundary charge", "false", "MTS theta/Q_tau must be extracted or EH reduction proven first"),
        ("REF2379_2_unnormalized_bound", "score B_zero_flux without M_H_ref", "false", "Bzero row needs positive same-frame denominator and units"),
        ("REF2379_3_local_gr", "2379 proves local GR/Newton", "false", "2379 stages a nonclaim boundary row and leaves source-normalization gates open"),
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
            "NEXT2379_0_selected",
            "2380-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md",
            "scripts/Y5_R2FR_parent_theta_Qtau_fixed_reference_or_MHref_first_row_2380.py",
            "own the parent boundary charge, fixed reference and positive same-frame M_H_ref denominator",
            "if theorem extraction fails, stage first M_H_ref/H_ref row as nonclaim",
        ),
        (
            "NEXT2379_1_parallel",
            "2380b-Y5-R2FR-Hilbert-topological-equality-or-Req-bound.md",
            "scripts/Y5_R2FR_Hilbert_topological_equality_or_Req_bound_2380b.py",
            "prove Pi_M J_H equals the measured/topological charge or produce R_eq",
            "retain R_eq/I_commutator if not closed",
        ),
        (
            "NEXT2379_2_fallback",
            "2380c-Y5-R2FR-Bzero-source-backed-numerator-acquisition.md",
            "scripts/Y5_R2FR_Bzero_source_backed_numerator_acquisition_2380c.py",
            "source finite B_zero numerator and units without claiming a pass",
            "keep nonclaim until denominator and fixed-reference certificate exist",
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
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_SOURCE_REGISTER.csv",
        "theorem_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_BZERO_NOFLUX_THEOREM_AUDIT.csv",
        "bound_row": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_BZERO_FIRST_BOUND_ROW.csv",
        "denominator_dependency": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_BOUNDARY_DENOMINATOR_DEPENDENCY.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_DECISION_LEDGER.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2379_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2379_VALIDATION.csv",
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

    theorem = read_csv(outputs["theorem_audit"])
    bound = read_csv(outputs["bound_row"])
    deps = read_csv(outputs["denominator_dependency"])
    decisions = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        ("VAL2379_00_required_sources_exist", all(row["path_exists"] == "true" for row in source_rows), "all required source paths exist"),
        ("VAL2379_01_required_needles_found", all(row["needle_found"] == "true" for row in source_rows), "all source needles found"),
        ("VAL2379_02_outputs_exist", all(path.exists() for path in generated_paths), "all 2379 output files written"),
        ("VAL2379_03_csv_parse", parsed_ok, "all generated CSV files parse and contain rows"),
        (
            "VAL2379_04_zero_theorem_not_derived",
            any(row["row_id"] == "BZT2379_6_verdict" and row["status"] == "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW" for row in theorem),
            "Bzero zero theorem not promoted",
        ),
        (
            "VAL2379_05_bound_row_staged",
            any(row["row_id"] == "BZR2379_0_first_row" and row["status"] == "SCHEMA_READY_VALUES_MISSING" for row in bound),
            "Bzero first bound row exists",
        ),
        (
            "VAL2379_06_dependencies_named",
            any(row["row_id"] == "BDD2379_0_theta_Qtau" for row in deps)
            and any(row["row_id"] == "BDD2379_2_MHref" for row in deps),
            "theta/Qtau, fixed reference and MHref dependencies named",
        ),
        (
            "VAL2379_07_next_selected",
            any(row["row_id"] == "DEC2379_2_next" and row["status"] == "SELECT_THETA_QTAU_FIXED_REFERENCE_NEXT" for row in decisions)
            and any(row["row_id"] == "NEXT2379_0_selected" for row in next_rows),
            "theta/Qtau fixed-reference next selected",
        ),
        (
            "VAL2379_08_local_claims_block",
            any(row["row_id"] == "CG2379_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
            "local GR/Newton claim gate remains false",
        ),
        (
            "VAL2379_09_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2379_10_formalization_untouched",
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
            "row_id": "VAL2379_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2379 valid: Bzero no-flux theorem not promoted, first nonclaim Bzero row staged, theta/Qtau fixed-reference/MHref selected next"
            if overall_ok
            else "2379 validation failed",
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
    theorem = read_csv(outputs["theorem_audit"])
    bound = read_csv(outputs["bound_row"])
    deps = read_csv(outputs["denominator_dependency"])
    decisions = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]

    text = f"""# 2379 - Boundary no-Flux Theorem Or Bzero First Bound Row

## Result

The boundary no-flux route is now explicit but not closed.

Target:

`B_zero_flux = 0`

for compact linked source boundaries, if the parent boundary/reference/improvement current is fixed, exact, or carries zero compact flux before readout.

The obstruction is not vague: the branch needs parent `theta_MTS/Q_tau^MTS`, a fixed reference/counterterm, compact support/falloff, Hilbert/topological equality, and a positive same-frame `M_H_ref`.

Because those are unsigned, the honest row is:

`epsilon_Bzero_abs := abs(B_zero_flux) / M_H_ref`.

It is schema-ready only, not score-ready.  Next target is parent theta/Qtau + fixed reference + `M_H_ref`.

## Bzero no-Flux Theorem Audit

{md_table(theorem, ["row_id", "clause", "status", "obstruction"])}

## Bzero First Bound Row

{md_table(bound, ["row_id", "quantity", "current_value", "status", "required_for_claim"])}

## Boundary Denominator Dependency

{md_table(deps, ["row_id", "dependency", "current_status", "blocks", "next_input"])}

## Decision Ledger

{md_table(decisions, ["row_id", "decision", "status", "consequence"])}

## Claim Gates

{md_table(gates, ["row_id", "gate", "gate_status", "claim_effect"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is the real boundary bottleneck in plain sight.  We are no longer saying "boundary term maybe"; we have a normalized residual object and the exact missing denominator/reference stack.  No local GR/Newton claim follows until that stack is owned.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["theorem_audit"], bzero_no_flux_theorem_audit())
    write_csv(outputs["bound_row"], bzero_first_bound_row())
    write_csv(outputs["denominator_dependency"], boundary_denominator_dependency())
    write_csv(outputs["decision_ledger"], decision_ledger())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()
