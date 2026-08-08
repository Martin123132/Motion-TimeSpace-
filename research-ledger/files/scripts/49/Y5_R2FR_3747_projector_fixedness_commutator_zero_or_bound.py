from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3747"
BRANCH_ID = "MTS_R2FR_Y5_PROJECTOR_FIXEDNESS_COMMUTATOR_ZERO_OR_BOUND_3747"
DOC = ROOT / "3747-Y5-R2FR-projector-fixedness-commutator-zero-or-bound.md"

DOC_3745 = ROOT / "3745-Y5-R2FR-parent-legitimacy-of-local-safe-S-closure.md"
DOC_3746 = ROOT / "3746-Y5-R2FR-explicit-parent-action-ansatz-and-variation-test.md"
RESIDUALS_3746 = RESIDUALS / "P8_Y5_R2FR_3746_RESIDUAL_VECTOR.csv"
BOUNDS_3746 = RESIDUALS / "P8_Y5_R2FR_3746_PPN_BOUND_INTERFACE.csv"
GATES_3746 = RESIDUALS / "P8_Y5_R2FR_3746_CLAIM_GATES.csv"
VALIDATION_3746 = RESIDUALS / "P8_Y5_BRR545_3746_VALIDATION.csv"
RED_TEAM = FORMALIZATION / "06-consistency-red-team.md"
SPINE = FORMALIZATION / "07-unification-spine.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def read_lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def find_line(path: Path, needle: str) -> tuple[int, str]:
    for line_number, line in enumerate(read_lines(path), start=1):
        if needle in line:
            return line_number, line.strip()
    return 0, ""


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3745_projector_domain", DOC_3745, "P_L^2=P_L, P_M^2=P_M, P_L P_M=0", "parent projector contract"),
        ("doc_3745_commutator", DOC_3745, "[nabla,P_L] terms are zero or budgeted", "commutator clause"),
        ("doc_3746_status", DOC_3746, "VARIATION_IDENTITY_AND_CONDITIONAL_ZERO_DERIVED_RESIDUALS_REMAIN", "3746 variation handoff"),
        ("doc_3746_residual_vector", DOC_3746, "R_deltaP", "projector fixedness residual"),
        ("residuals_3746_deltaP", RESIDUALS_3746, "R_deltaP", "machine-readable delta-projector residual"),
        ("bounds_3746_comm", BOUNDS_3746, "epsilon_comm", "machine-readable commutator bound slot"),
        ("gates_3746_block", GATES_3746, "CG3746_6_local_claim", "local claim remains blocked"),
        ("validation_3746_clean", VALIDATION_3746, "no_formalization_leak", "3746 validation clean"),
        ("redteam_projector_switch", RED_TEAM, "P_loc, P_gal, and P_cos could become arbitrary sector switches.", "anti-switch warning"),
        ("redteam_projector_toy", RED_TEAM, "P_loc = Pi_B + (1 - Pi_B)(1 - C_cos)(1 - T_gal)", "field/arena-like toy projector"),
        ("spine_projector_route", SPINE, "exact cancellation/projector theorem", "projector route in spine"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        line_number, line_text = find_line(path, needle) if exists else (0, "")
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "line_number": line_number,
            "line_text": line_text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def projector_case_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "PC3747_0_structural_parallel",
            "structural parallel projector",
            "P_M is a parent bundle/quotient endomorphism fixed by the theory, with nabla P_M=0",
            "delta_L P_M=0 and [nabla,P_M]P_L=0",
            "ZERO_THEOREM_IF_PARENT_SIGNED",
            "This is the clean route: geometry, not arena switching.",
        ),
        (
            "PC3747_1_field_dependent_switch",
            "field-dependent switch projector",
            "P_M=P_M[Phi,K,C_cos,T_gal,Pi_B] depends on local/cosmological/galaxy markers",
            "delta_L P_M != 0 and [nabla,P_M] generally nonzero",
            "FAILS_ZERO_REQUIRES_BOUND",
            "This behaves like a closure switch unless residuals are bounded.",
        ),
        (
            "PC3747_2_transition_partition",
            "smooth transition partition",
            "P_M is a smooth partition of unity across local/nonlocal sectors",
            "delta_L P_M and nabla P_M live near transition regions",
            "BOUND_ROUTE_ONLY",
            "May be empirically controllable but is not an exact local zero.",
        ),
        (
            "PC3747_3_algebraic_projection_after_variation",
            "post-variation algebraic projection",
            "field equations are varied first, then local observable map applies P_L",
            "P_L R_M may vanish even if delta_L S_M is not zero",
            "OBSERVABLE_SILENCE_ROUTE_NEEDS_MAP",
            "Could save local observables but no longer proves action-level silence.",
        ),
    ]
    return [
        {
            **base(timestamp),
            "case_id": case_id,
            "case": case,
            "definition": definition,
            "variation_result": variation_result,
            "verdict": verdict,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for case_id, case, definition, variation_result, verdict, meaning in specs
    ]


def zero_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("ZT3747_0_bundle_split", "E = E_L direct-sum E_M with P_L and P_M the canonical projections", "P_M P_L=0", "hypothesis"),
        ("ZT3747_1_structural_fixedness", "P_M is independent of dynamical local fields", "delta_L P_M=0", "deduction"),
        ("ZT3747_2_parallel_connection", "the parent connection preserves the split: nabla(E_L) subset E_L and nabla(E_M) subset E_M", "nabla P_M=0", "hypothesis"),
        ("ZT3747_3_commutator_zero", "for any local variation delta_L Phi in E_L, [nabla,P_M]P_L delta Phi=(nabla P_M)P_L delta Phi=0", "R_comm=0", "deduction"),
        ("ZT3747_4_deltaP_zero", "delta_L(P_M Phi_S)=P_M P_L delta Phi_S+(delta_L P_M)Phi_S=0", "R_deltaP=0", "deduction"),
        ("ZT3747_5_result", "structural parallel projector implies the two sharp 3746 leakage terms vanish", "R_deltaP=R_comm=0", "conditional_theorem"),
        ("ZT3747_6_claim_limit", "the current corpus has not signed E=E_L direct-sum E_M or nabla P_M=0 as parent geometry", "no local claim", "anti_overclaim"),
    ]
    return [
        {
            **base(timestamp),
            "theorem_step_id": step_id,
            "condition_or_step": condition,
            "result": result,
            "step_type": step_type,
            "signed_in_current_corpus": False,
            "claim_allowed": False,
        }
        for step_id, condition, result, step_type in specs
    ]


def obstruction_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("OBS3747_0_marker_dependence", "P_M depends on C_cos/T_gal/Pi_B or similar markers", "delta_L P_M includes derivatives of marker functions", "R_deltaP survives"),
        ("OBS3747_1_transition_gradients", "P_M changes across a local/nonlocal boundary", "nabla P_M supported on transition region", "R_comm and R_boundary survive"),
        ("OBS3747_2_connection_mixing", "connection has off-diagonal E_L/E_M components", "nabla P_M != 0", "R_comm survives"),
        ("OBS3747_3_metric_dependence", "projector is defined by local metric/curvature scalars", "delta_L g or delta_L K changes P_M", "R_deltaP survives"),
        ("OBS3747_4_posthoc_observable_projection", "P_L is applied only to final observable equations", "action-level zero not proved", "requires separate observable response map"),
    ]
    return [
        {
            **base(timestamp),
            "obstruction_id": obstruction_id,
            "obstruction": obstruction,
            "mechanism": mechanism,
            "residual_effect": residual_effect,
            "claim_allowed": False,
        }
        for obstruction_id, obstruction, mechanism, residual_effect in specs
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("B3747_0_epsilon_deltaP", "epsilon_deltaP", "||<E_M,(delta_L P_M)Phi_S>||_D", "local profile/operator norm", "feeds S_eff_3746", "MISSING_PROFILE_AND_OPERATOR_NORM"),
        ("B3747_1_epsilon_comm", "epsilon_comm", "||<E_M^nabla,[nabla,P_M]P_L delta Phi_S>||_D", "local derivative/operator norm", "feeds S_eff_3746", "MISSING_CONNECTION_SPLIT_OR_BOUND"),
        ("B3747_2_transition_width", "ell_transition", "length scale over which P_M changes", "length", "controls nabla P_M ~ 1/ell_transition", "MISSING_TRANSITION_GEOMETRY"),
        ("B3747_3_mixing_norm", "Omega_LM", "off-diagonal connection/projector mixing norm", "inverse_length_or_dimensionless", "bounds commutator leakage", "MISSING_PARENT_CONNECTION"),
        ("B3747_4_marker_sensitivity", "dP_dI", "projector derivative with respect to marker invariants", "inverse_marker_units", "bounds delta_L P_M", "MISSING_MARKER_DEFINITION"),
        ("B3747_5_total_addon", "epsilon_proj_leak", "epsilon_deltaP+epsilon_comm", "dimensionless_after_normalization", "add to 3746 S_eff_3746 and 3744 PPN/Newton gate", "BOUND_SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "quantity": quantity,
            "definition": definition,
            "units": units,
            "observable_link": observable_link,
            "status": status,
            "claim_allowed": False,
        }
        for bound_id, quantity, definition, units, observable_link, status in specs
    ]


def verdict_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("VER3747_0_conditional_success", "PARALLEL_STRUCTURAL_PROJECTOR_WOULD_CLOSE_RDELTAP_RCOMM", "If P_M is a fixed parent bundle projector preserved by the connection, then delta_L P_M=0 and [nabla,P_M]P_L=0."),
        ("VER3747_1_current_unsigned", "CURRENT_CORPUS_DOES_NOT_SIGN_PARALLEL_PROJECTOR", "Existing projector evidence is toy/contract/red-team level, not a parent geometric construction."),
        ("VER3747_2_switch_warning", "FIELD_DEPENDENT_SWITCH_ROUTE_IS_NOT_A_DERIVATION", "If P_M depends on markers like C_cos/T_gal/Pi_B, the exact zero generally fails."),
        ("VER3747_3_next", "NEXT_BUILD_PARENT_BUNDLE_SPLIT_OR_BOUND_EPSILON_PROJ_LEAK", "Either construct the bundle split and parallel connection, or feed epsilon_deltaP/epsilon_comm into the PPN budget."),
    ]
    return [
        {
            **base(timestamp),
            "verdict_id": verdict_id,
            "verdict": verdict,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for verdict_id, verdict, rationale in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3747_0_sources", "3747 source handoff complete", True, "source paths and needles found"),
        ("CG3747_1_zero_theorem", "parallel-projector zero theorem derived conditionally", True, "structural fixedness plus parallel connection kills R_deltaP and R_comm"),
        ("CG3747_2_parent_bundle_signed", "parent bundle split signed", False, "not found in current corpus"),
        ("CG3747_3_parallel_connection_signed", "nabla P_M=0 signed", False, "not found in current corpus"),
        ("CG3747_4_switch_obstruction_recorded", "field-dependent switch obstruction recorded", True, "toy/marker projector route cannot be treated as exact zero"),
        ("CG3747_5_bounds_filled", "epsilon_deltaP and epsilon_comm numeric/source bounds filled", False, "bound rows are schema only"),
        ("CG3747_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "zero theorem remains conditional and bounds are missing"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, rationale in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3747_0_progress", "SHARP_ZERO_CONDITION_FOUND", "The correct mathematical object is a structural parallel projector, not a dataset/sector switch."),
        ("DEC3747_1_best_route", "TRY_PARENT_BUNDLE_SPLIT_NEXT", "A signed E_L direct-sum E_M split with nabla P_M=0 would close two major 3746 residuals cleanly."),
        ("DEC3747_2_fallback", "BOUND_PROJECTOR_LEAK_IF_SPLIT_FAILS", "If the projector is marker/transition based, epsilon_deltaP and epsilon_comm must be bounded before PPN testing."),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "status_id": "STATUS3747_0",
        "status": "PARALLEL_PROJECTOR_ZERO_THEOREM_CONDITIONAL_SWITCH_ROUTE_BLOCKED",
        "summary": "3747 derives that R_deltaP and R_comm vanish if the local/nonlocal projector is a structural parent bundle projector preserved by the connection; current corpus does not sign that structure, and field-dependent switch projectors require bounds.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3747_0",
        "target_doc": "3748-Y5-R2FR-parent-bundle-split-construction-or-projector-leak-bound.md",
        "target_script": "scripts/Y5_R2FR_3748_parent_bundle_split_construction_or_projector_leak_bound.py",
        "objective": "attempt to construct a parent E_L direct-sum E_M bundle split with a parallel projector; if that cannot be sourced, instantiate epsilon_deltaP and epsilon_comm bound rows for local PPN/Newton testing",
        "success_gate": "either P_M is parent-signed as structural and parallel, or the projector leak becomes a numeric/source-bound input rather than a hidden closure assumption",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3747 - Projector Fixedness and Commutator Zero-or-Bound",
        "",
        "## Status",
        "- `PARALLEL_PROJECTOR_ZERO_THEOREM_CONDITIONAL_SWITCH_ROUTE_BLOCKED`",
        "- The exact zero route is now clear: `P_M` must be a structural parent projector preserved by the connection.",
        "- If `P_M` is a field/marker/arena switch, `R_deltaP` and `R_comm` generally survive and must be bounded.",
        "",
        "## Projector Cases",
    ]
    for row in grouped["cases"]:
        lines.append(f"- `{row['case_id']}` `{row['verdict']}`: {row['case']} | {row['meaning']}")
    lines.extend(["", "## Conditional Zero Theorem"])
    for row in grouped["zero_theorem"]:
        lines.append(f"- `{row['theorem_step_id']}` `{row['step_type']}`: {row['condition_or_step']} -> {row['result']}")
    lines.extend(["", "## Obstructions"])
    for row in grouped["obstructions"]:
        lines.append(f"- `{row['obstruction_id']}`: {row['obstruction']} | {row['residual_effect']}")
    lines.extend(["", "## Bound Rows"])
    for row in grouped["bounds"]:
        lines.append(f"- `{row['bound_id']}` `{row['quantity']}` `{row['status']}`: {row['definition']}")
    lines.extend(["", "## Verdicts"])
    for row in grouped["verdicts"]:
        lines.append(f"- `{row['verdict_id']}` `{row['verdict']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` passed={row['passed']} claim_allowed={row['claim_allowed']} | {row['gate']}: {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    cases = parse_csv(paths["cases"])
    zero_theorem = parse_csv(paths["zero_theorem"])
    obstructions = parse_csv(paths["obstructions"])
    bounds = parse_csv(paths["bounds"])
    verdicts = parse_csv(paths["verdicts"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3747*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("cases_complete", "four projector cases emitted", len(cases) == 4 and all(token in read_text(paths["cases"]) for token in ["structural parallel projector", "field-dependent switch projector"])),
        ("zero_theorem", "parallel projector zero theorem emitted", len(zero_theorem) == 7 and all(token in read_text(paths["zero_theorem"]) for token in ["delta_L P_M=0", "nabla P_M=0", "R_deltaP=R_comm=0"])),
        ("obstructions", "switch/transition/connection obstructions emitted", len(obstructions) == 5 and all(token in read_text(paths["obstructions"]) for token in ["transition", "off-diagonal", "metric"])),
        ("bounds", "epsilon_deltaP and epsilon_comm bound schema emitted", len(bounds) == 6 and all(token in read_text(paths["bounds"]) for token in ["epsilon_deltaP", "epsilon_comm", "epsilon_proj_leak"])),
        ("verdicts", "conditional success and current unsigned verdicts emitted", all(token in read_text(paths["verdicts"]) for token in ["PARALLEL_STRUCTURAL_PROJECTOR_WOULD_CLOSE_RDELTAP_RCOMM", "CURRENT_CORPUS_DOES_NOT_SIGN_PARALLEL_PROJECTOR"])),
        ("claim_gates_block", "local claim gate remains blocked", any(row["gate_id"] == "CG3747_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("claim_allowed_false", "all gate rows keep claim_allowed false", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("doc_core_terms", "doc records structural projector route and switch warning", all(token in read_text(paths["doc"]) for token in ["structural parent projector", "field/marker/arena switch", "Conditional Zero Theorem"])),
        ("next_target_3748", "next target is parent bundle split or leak bound", next_target[0]["target_doc"] == "3748-Y5-R2FR-parent-bundle-split-construction-or-projector-leak-bound.md"),
        ("no_formalization_leak", "no 3747 files in formalization-workbench", len(formalization_leaks) == 0),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def main() -> None:
    timestamp = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3747_SOURCE_REGISTER.csv",
        "cases": RESIDUALS / "P8_Y5_R2FR_3747_PROJECTOR_CASES.csv",
        "zero_theorem": RESIDUALS / "P8_Y5_R2FR_3747_PARALLEL_PROJECTOR_ZERO_THEOREM.csv",
        "obstructions": RESIDUALS / "P8_Y5_R2FR_3747_SWITCH_OBSTRUCTIONS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3747_PROJECTOR_LEAK_BOUND_ROWS.csv",
        "verdicts": RESIDUALS / "P8_Y5_R2FR_3747_VERDICT_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3747_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3747_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3747_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3747_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3747_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "cases": projector_case_rows(timestamp),
        "zero_theorem": zero_theorem_rows(timestamp),
        "obstructions": obstruction_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "verdicts": verdict_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "status": status_rows(timestamp),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3747 validation failed: {failures}")
    print("wrote 3747 checkpoint: parallel-projector zero theorem conditional; switch route blocked unless bounded")


if __name__ == "__main__":
    main()
