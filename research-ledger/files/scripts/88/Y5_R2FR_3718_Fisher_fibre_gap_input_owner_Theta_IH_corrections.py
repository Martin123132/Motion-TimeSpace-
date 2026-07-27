from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3718"
BRANCH_ID = "MTS_R2FR_Y5_FISHER_FIBRE_GAP_INPUT_OWNER_THETA_IH_CORRECTIONS_3718"
DOC = ROOT / "3718-Y5-R2FR-Fisher-fibre-gap-input-owner-Theta-IH-corrections.md"

DOC_3717 = ROOT / "3717-Y5-R2FR-fibre-normal-form-F1-zero-and-BQK-mixed-Hessian-owner.md"
NEXT_3717 = RESIDUALS / "P8_Y5_R2FR_3717_NEXT_TARGET.csv"
FISHER_3717 = RESIDUALS / "P8_Y5_R2FR_3717_FISHER_KL_CORE_ROWS.csv"
PACK_3717 = RESIDUALS / "P8_Y5_R2FR_3717_COEFFICIENT_PACK_ROWS.csv"
CORR_3717 = RESIDUALS / "P8_Y5_R2FR_3717_RETAINED_CORRECTION_ROWS.csv"
FILL_3709 = RESIDUALS / "P8_Y5_R2FR_3709_PARENT_FILL_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
ANCHOR_3708 = RESIDUALS / "P8_Y5_R2FR_3708_OFFICIAL_ANCHOR_FISHER_GAP_ROWS.csv"
DOC_3716 = ROOT / "3716-Y5-R2FR-LH-block-diagonal-from-quotient-action-or-epsilon-LP-source-row.md"


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(stamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": stamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


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


def source_register(stamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3717", DOC_3717, "F1_BQK_REDUCED_TO_ZERO_SECTION_FAMILY_AND_FISHER_KL_CORE_NONCLAIM", "3717 result"),
        ("next_3717", NEXT_3717, "Theta_H, I_H", "3717 declared 3718 target"),
        ("fisher_3717", FISHER_3717, "M_K,core(q)=Theta_H(q) I_AB(q)", "Fisher/KL core rows"),
        ("pack_3717", PACK_3717, "PACK3717_2_MK_core", "coefficient pack requiring Theta_H and I_H"),
        ("corr_3717", CORR_3717, "R_odd,BQK", "retained correction rows"),
        ("fill_3709", FILL_3709, "Theta_H*iota_H - R_loss", "prior symbolic Xi_H contract"),
        ("fisher_3708", FISHER_3708, "D_KL(p_z||p_0)=0.5", "Fisher gap derivation input"),
        ("anchor_3708", ANCHOR_3708, "Xi_H", "R10 anchor budget only"),
        ("doc_3716", DOC_3716, "epsilon_LP", "dynamic leakage target"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base_row(stamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def owner_clause_rows(stamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    clauses = [
        (
            "OWN3718_0_bath_family",
            "p_z(xi|X_B,q)",
            "parent-owned smooth bath family over the local observed patch U",
            "needed so the Fisher matrix is not an invented closure",
            "MISSING_PARENT_BATH_FAMILY",
        ),
        (
            "OWN3718_1_measure",
            "mu_H(xi;q)",
            "parent-owned measure/coframe normalization for bath averages",
            "sets the units of I_H and prevents arbitrary rescaling",
            "MISSING_MEASURE_NORMALIZATION",
        ),
        (
            "OWN3718_2_scale",
            "Theta_H(q)>0",
            "positive parent scale multiplying the KL fibre potential",
            "converts dimensionless KL curvature into local Hessian/operator units",
            "MISSING_THETA_H_SOURCE",
        ),
        (
            "OWN3718_3_fisher_floor",
            "iota_H:=lambda_min(I_H)",
            "strict lower eigenvalue bound on the Fisher matrix in the active kernel sector",
            "keeps a real fibre mass gap rather than a flat closure direction",
            "MISSING_IH_EIGENVALUE_BOUND",
        ),
        (
            "OWN3718_4_correction_loss",
            "R_M_loss",
            "operator norm budget for even/correction Hessian pieces that can reduce the gap",
            "lets the gap theorem survive non-ideal parent terms",
            "MISSING_CORRECTION_OPERATOR_BOUND",
        ),
        (
            "OWN3718_5_unit_map",
            "U_H",
            "same-basis unit map from fibre Hessian to the local screening operator",
            "connects M_K to Xi_H in m^-2 without unit sleight of hand",
            "MISSING_UNIT_BASIS_MAP",
        ),
    ]
    for clause_id, symbol, required_clause, reason, status in clauses:
        rows.append({
            **base_row(stamp),
            "clause_id": clause_id,
            "symbol": symbol,
            "required_clause": required_clause,
            "reason": reason,
            "status": status,
            "claim_allowed": False,
        })
    return rows


def gap_law_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "GAP3718_0_core_hessian",
            "M_K,core(q)=Theta_H(q) I_H(q)",
            "second z-variation of Theta_H D_KL at z=0",
            "DERIVED_FROM_3717_CORE",
        ),
        (
            "GAP3718_1_total_hessian",
            "M_K,total=M_K,core+Delta M_even+Delta M_boundary",
            "keeps all non-core curvature pieces visible",
            "DERIVED_DECOMPOSITION",
        ),
        (
            "GAP3718_2_weyl_floor",
            "lambda_min(M_K,total) >= Theta_min*iota_H - R_M_loss",
            "Weyl bound with R_M_loss>=||Delta M_even+Delta M_boundary||",
            "DERIVED_BOUND",
        ),
        (
            "GAP3718_3_gap_condition",
            "Xi_H:=Theta_min*iota_H - R_M_loss > 0",
            "positive screening/operator gap condition",
            "DERIVED_PASS_CONDITION_NOT_SATISFIED",
        ),
        (
            "GAP3718_4_screening_length",
            "ell_H <= Xi_H^(-1/2)",
            "local transition length if Xi_H is in m^-2",
            "DERIVED_IF_UNIT_MAP_OWNED",
        ),
        (
            "GAP3718_5_anchor_warning",
            "Xi_H_min_for_R10_anchor is a required lower bound, not a parent prediction",
            "anchor budgets can test but cannot source Theta_H or I_H",
            "ANTI_SMUGGLING_GUARD",
        ),
    ]
    return [
        {
            **base_row(stamp),
            "gap_id": gap_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for gap_id, formula, meaning, status in entries
    ]


def correction_budget_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "CORRB3718_0_force_loss",
            "F_loss:=||R_odd,F1||+||B_boundary,F1||",
            "||F_1,total|| <= F_loss",
            "source or theorem-zero required before local force silence",
        ),
        (
            "CORRB3718_1_mixed_loss",
            "QK_loss:=||R_odd,BQK||+||B_boundary,QK||",
            "||B_QK,total|| <= QK_loss",
            "feeds epsilon_LP and dynamic leakage",
        ),
        (
            "CORRB3718_2_reciprocal_loss",
            "KQ_loss:=||B_KQ,total||",
            "needed if Hessian/operator is not self-adjoint in the chosen pairing",
            "prevents hiding asymmetric mixed leakage",
        ),
        (
            "CORRB3718_3_dynamic_leak",
            "epsilon_LP <= QK_loss + KQ_loss + ||B_boundary,QK||",
            "safe leakage row inherited from 3716/3717",
            "local arenas stay blocked until finite values exist",
        ),
        (
            "CORRB3718_4_exact_symmetry_route",
            "R_odd=0 and boundary fibre-stationary over U => F_loss=QK_loss=0",
            "clean theorem route if parent action has a z -> -z fibre symmetry plus silent boundary",
            "DERIVED_EXACT_IF_PARENT_SYMMETRY_SIGNED",
        ),
    ]
    return [
        {
            **base_row(stamp),
            "correction_id": correction_id,
            "quantity": quantity,
            "bound_or_clause": bound_or_clause,
            "impact": impact,
            "status": "MISSING_ZERO_OR_SOURCE_BOUND" if correction_id != "CORRB3718_4_exact_symmetry_route" else "CONDITIONAL_EXACT_ROUTE",
            "claim_allowed": False,
        }
        for correction_id, quantity, bound_or_clause, impact in entries
    ]


def executable_input_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "INPUT3718_0_Theta_min",
            "Theta_min",
            "lower bound of Theta_H over local patch U",
            "operator scale compatible with Xi_H units",
            "MISSING_NUMERIC_PARENT_VALUE",
        ),
        (
            "INPUT3718_1_iota_H",
            "iota_H",
            "minimum positive eigenvalue of I_H in active kernel sector",
            "inverse fibre-coordinate squared after unit map",
            "MISSING_NUMERIC_PARENT_VALUE",
        ),
        (
            "INPUT3718_2_R_M_loss",
            "R_M_loss",
            "operator norm loss from even and boundary Hessian corrections",
            "same operator units as Theta_H*iota_H",
            "MISSING_NUMERIC_PARENT_VALUE",
        ),
        (
            "INPUT3718_3_Xi_H",
            "Xi_H",
            "Theta_min*iota_H - R_M_loss",
            "m^-2 only after U_H unit map is fixed",
            "SYMBOLIC_DERIVED_NOT_NUMERIC",
        ),
        (
            "INPUT3718_4_F_loss",
            "F_loss",
            "||R_odd,F1||+||B_boundary,F1||",
            "action per fibre coordinate",
            "MISSING_NUMERIC_PARENT_VALUE",
        ),
        (
            "INPUT3718_5_QK_loss",
            "QK_loss",
            "||R_odd,BQK||+||B_boundary,QK||",
            "local Hessian/operator units",
            "MISSING_NUMERIC_PARENT_VALUE",
        ),
        (
            "INPUT3718_6_R10_anchor",
            "Xi_H_min_for_alpha1_anchor",
            "6.711589572874e+08 from 3709 anchor requirement",
            "m^-2 requirement, not MTS prediction",
            "TEST_REQUIREMENT_ONLY",
        ),
    ]
    return [
        {
            **base_row(stamp),
            "input_id": input_id,
            "quantity": quantity,
            "formula_or_value": formula_or_value,
            "units": units,
            "status": status,
            "claim_allowed": False,
        }
        for input_id, quantity, formula_or_value, units, status in entries
    ]


def decision_rows(stamp: str) -> list[dict[str, object]]:
    decisions = [
        (
            "DEC3718_0_gap_law",
            "FISHER_GAP_LAW_DERIVED",
            "The local gap is no longer just a placeholder: Xi_H >= Theta_min*iota_H - R_M_loss.",
        ),
        (
            "DEC3718_1_anchor_guard",
            "ANCHOR_IS_TEST_NOT_SOURCE",
            "The R10 anchor supplies a target Xi_H floor but cannot be used as a parent-owned MTS coefficient.",
        ),
        (
            "DEC3718_2_correction_guard",
            "ODD_AND_BOUNDARY_TERMS_RETAINED",
            "The clean route requires z-parity/boundary silence; otherwise F_loss and QK_loss remain finite inputs.",
        ),
        (
            "DEC3718_3_next",
            "ADVANCE_TO_PARENT_BATH_NORMALIZATION_OR_PARITY_PROOF",
            "Next target should try to derive p_z, mu_H, Theta_H, and z-parity from the parent action, before numeric fitting.",
        ),
    ]
    return [
        {
            **base_row(stamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in decisions
    ]


def claim_gate_rows(stamp: str) -> list[dict[str, object]]:
    gates = [
        ("CG3718_0_bath", "BLOCKED", "p_z and mu_H parent-owned and normalized"),
        ("CG3718_1_scale", "BLOCKED", "Theta_min positive with units"),
        ("CG3718_2_fisher_floor", "BLOCKED", "iota_H positive in the active kernel sector"),
        ("CG3718_3_corrections", "BLOCKED", "R_M_loss, F_loss, and QK_loss theorem-zero or finite sourced"),
        ("CG3718_4_gap", "BLOCKED", "Xi_H=Theta_min*iota_H-R_M_loss positive in m^-2"),
        ("CG3718_5_local_claim", "BLOCKED", "R10/PPN/clock/orbital pass may be stated"),
    ]
    return [
        {
            **base_row(stamp),
            "gate_id": gate_id,
            "gate_status": gate_status,
            "required_before_claim": required_before_claim,
            "claim_allowed": False,
        }
        for gate_id, gate_status, required_before_claim in gates
    ]


def status_rows(stamp: str) -> list[dict[str, object]]:
    return [
        {
            **base_row(stamp),
            "status_id": "STATUS3718_0",
            "status": "GAP_LAW_DERIVED_INPUTS_STILL_NONCLAIM",
            "summary": "3718 converts the Fisher/KL core into an executable gap inequality Xi_H>=Theta_min*iota_H-R_M_loss, while keeping Theta_H, I_H, unit map, and correction rows blocked until parent-owned.",
            "claim_allowed": False,
        }
    ]


def next_target_rows(stamp: str) -> list[dict[str, object]]:
    return [
        {
            **base_row(stamp),
            "next_id": "NEXT3718_0",
            "target_doc": "3719-Y5-R2FR-parent-bath-normalization-and-z-parity-proof.md",
            "target_script": "scripts/Y5_R2FR_3719_parent_bath_normalization_and_z_parity_proof.py",
            "objective": "try to derive the bath family, measure normalization, positive Theta_H scale, and z-parity/boundary silence from the parent action so the Fisher gap inputs stop being external coefficient rows",
            "success_gate": "p_z, mu_H, Theta_H, U_H, and R_odd/boundary silence are parent-owned, or finite nonclaim rows remain with units and arena impact",
            "claim_allowed": False,
        }
    ]


def validation_rows(stamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_checkpoint_files = list(FORMALIZATION.rglob("*3718*")) if FORMALIZATION.exists() else []
    formalization_checkpoint_files = [path for path in formalization_checkpoint_files if path.is_file()]
    validations = [
        (
            "sources_exist",
            "all cited local sources exist",
            all(row["exists"] == "True" for row in sources),
            "",
        ),
        (
            "needles_found",
            "all source needles found",
            all(row["needle_found"] == "True" for row in sources),
            "",
        ),
        (
            "outputs_exist",
            "all generated output paths exist",
            all(path.exists() for path in generated_paths),
            "",
        ),
        (
            "csv_parse",
            "all generated CSV files parse and are nonempty",
            all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists()),
            "",
        ),
        (
            "owner_clauses",
            "Theta_H, I_H, measure, correction, and unit-map owner rows exist",
            all(token in read_text(paths["owner_clauses"]) for token in ["Theta_H(q)>0", "iota_H:=lambda_min(I_H)", "U_H"]),
            "",
        ),
        (
            "gap_law",
            "Weyl lower-bound gap law exists",
            "lambda_min(M_K,total) >= Theta_min*iota_H - R_M_loss" in read_text(paths["gap_laws"]),
            "",
        ),
        (
            "anchor_guard",
            "anchor is treated as test requirement not parent source",
            "required lower bound, not a parent prediction" in read_text(paths["gap_laws"]),
            "",
        ),
        (
            "correction_budget",
            "F_loss and QK_loss rows are retained",
            all(token in read_text(paths["correction_budget"]) for token in ["F_loss", "QK_loss", "z -> -z"]),
            "",
        ),
        (
            "executable_inputs",
            "Theta_min, iota_H, R_M_loss, Xi_H, and anchor rows exist",
            all(token in read_text(paths["executable_inputs"]) for token in ["Theta_min", "iota_H", "R_M_loss", "Xi_H_min_for_alpha1_anchor"]),
            "",
        ),
        (
            "claim_gates_blocked",
            "all claim gates remain blocked",
            all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"])),
            "",
        ),
        (
            "next_target_3719",
            "next target advances to parent bath normalization and z parity",
            "3719" in read_text(paths["next_target"]),
            "",
        ),
        (
            "doc_core_terms",
            "markdown contains core laws",
            all(token in read_text(paths["doc"]) for token in ["Xi_H:=Theta_min*iota_H-R_M_loss", "ell_H <= Xi_H^(-1/2)", "Anchor is not source"]),
            "",
        ),
        (
            "no_formalization_leak",
            "no 3718 files written to formalization-workbench",
            len(formalization_checkpoint_files) == 0,
            "",
        ),
    ]
    return [
        {
            **base_row(stamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": details,
        }
        for validation_id, description, result, details in validations
    ]


def write_doc(paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3718 — Fisher Fibre Gap Input Owner: Theta_H, I_H, Corrections",
        "",
        "## Status",
        "- `GAP_LAW_DERIVED_INPUTS_STILL_NONCLAIM`",
        "- 3718 pushes the framework forward: the Fisher/KL core now gives an explicit local gap law, not just a named missing coefficient.",
        "- `valid_for_claim=false`: the parent still has to own the bath family, scale, units, and correction bounds before R10/PPN/local-GR claims.",
        "",
        "## Main Result",
        "- From 3717, the Fisher core gives `M_K,core(q)=Theta_H(q) I_H(q)` while keeping `F_1,core=0` and `B_QK,core=0`.",
        "- Including even and boundary Hessian corrections, `M_K,total=M_K,core+Delta M_even+Delta M_boundary`.",
        "- Weyl bound: `lambda_min(M_K,total) >= Theta_min*iota_H - R_M_loss`.",
        "- Define `Xi_H:=Theta_min*iota_H-R_M_loss`; if `Xi_H>0` and the unit map is fixed, the local screening length obeys `ell_H <= Xi_H^(-1/2)`.",
        "- Anchor is not source: the R10 anchor budget is a required target floor for `Xi_H`, not a parent-owned MTS prediction.",
        "",
        "## Owner Clauses",
    ]
    for row in rows_by_name["owner_clauses"]:
        lines.append(f"- `{row['clause_id']}` `{row['symbol']}`: {row['required_clause']} | {row['status']}")
    lines.extend(["", "## Gap Laws"])
    for row in rows_by_name["gap_laws"]:
        lines.append(f"- `{row['gap_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Correction Budget"])
    for row in rows_by_name["correction_budget"]:
        lines.append(f"- `{row['correction_id']}` `{row['quantity']}`: `{row['bound_or_clause']}` | {row['impact']}")
    lines.extend(["", "## Executable Inputs"])
    for row in rows_by_name["executable_inputs"]:
        lines.append(f"- `{row['input_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['units']} | {row['status']}")
    lines.extend(["", "## Decisions"])
    for row in rows_by_name["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in rows_by_name["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Source Register"])
    for row in rows_by_name["source_register"]:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend([
        "",
        "## Next Target",
        "- `3719-Y5-R2FR-parent-bath-normalization-and-z-parity-proof.md`",
        "- Objective: derive the bath family, measure normalization, positive `Theta_H`, unit map, and `z -> -z`/boundary silence from the parent action, or keep finite nonclaim rows.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    stamp = timestamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3718_SOURCE_REGISTER.csv",
        "owner_clauses": RESIDUALS / "P8_Y5_R2FR_3718_OWNER_CLAUSE_ROWS.csv",
        "gap_laws": RESIDUALS / "P8_Y5_R2FR_3718_GAP_LAW_ROWS.csv",
        "correction_budget": RESIDUALS / "P8_Y5_R2FR_3718_CORRECTION_BUDGET_ROWS.csv",
        "executable_inputs": RESIDUALS / "P8_Y5_R2FR_3718_EXECUTABLE_INPUT_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3718_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3718_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3718_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3718_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3718_VALIDATION.csv",
        "doc": DOC,
    }
    rows_by_name = {
        "source_register": source_register(stamp),
        "owner_clauses": owner_clause_rows(stamp),
        "gap_laws": gap_law_rows(stamp),
        "correction_budget": correction_budget_rows(stamp),
        "executable_inputs": executable_input_rows(stamp),
        "decisions": decision_rows(stamp),
        "claim_gates": claim_gate_rows(stamp),
        "status": status_rows(stamp),
        "next_target": next_target_rows(stamp),
    }
    for name, rows in rows_by_name.items():
        write_csv(paths[name], rows)
    write_doc(paths, rows_by_name)
    write_csv(paths["validation"], validation_rows(stamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3718 validation failed: {failures}")
    print("wrote 3718 checkpoint: Fisher gap law derived with nonclaim parent input rows")


if __name__ == "__main__":
    main()
