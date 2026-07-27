from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3712"
BRANCH_ID = "MTS_R2FR_Y5_JEFF_ZERO_OR_FINITE_BOUND_HORIZONTAL_SOURCE_AMPLITUDE_3712"
DOC = ROOT / "3712-Y5-R2FR-Jeff-zero-or-finite-bound-horizontal-source-amplitude.md"

DOC_3711 = ROOT / "3711-Y5-R2FR-PN-factor-decomposition-KN-rho-CH-Jeff-source-bound.md"
PRIORITY_3711 = RESIDUALS / "P8_Y5_R2FR_3711_FACTOR_PRIORITY_ROWS.csv"
BUDGET_3711 = RESIDUALS / "P8_Y5_R2FR_3711_FACTOR_BUDGET_ROWS.csv"
THEOREM_3711 = RESIDUALS / "P8_Y5_R2FR_3711_THEOREM_ATTEMPT_ROWS.csv"
LOCAL_SUPPRESSION_3693 = RESIDUALS / "P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv"
RESIDUAL_TENSOR_3700 = RESIDUALS / "P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv"
DOC_1055 = ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md"
DOC_1038 = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"
DOC_1012 = ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"
DOC_1015 = ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"
DESIGN_3709 = RESIDUALS / "P8_Y5_R2FR_3709_DESIGN_INEQUALITY_ROWS.csv"


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


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3711", DOC_3711, "J_y+B_y=0", "3711 selected J_eff zero-or-bound route"),
        ("priority_3711", PRIORITY_3711, "PRI3711_0_Jeff", "J_eff rank-1 factor target"),
        ("budget_3711", BUDGET_3711, "FB3711_0_FB3710_0_private_tightest", "J_eff budget rows"),
        ("theorem_3711", THEOREM_3711, "THM3711_1_Jeff_exact_zero", "J_eff exact zero theorem statement"),
        ("local_suppression_3693", LOCAL_SUPPRESSION_3693, "SPL3693_0_exact_silence", "original exact horizontal silence law"),
        ("residual_tensor_3700", RESIDUAL_TENSOR_3700, "RT3700_3_amplitude_bound", "second-order source residual amplitude gate"),
        ("doc_1055", DOC_1055, "PAC1055_4_source_label_forgetting", "matter functor source-label forgetting candidate"),
        ("doc_1038", DOC_1038, "MISSING_DCX_OPERATOR", "DCX obstruction to vertical generator/no-pole proof"),
        ("doc_1012", DOC_1012, "Y5O1012_3_flux_closure", "source/current flux closure obstruction"),
        ("doc_1015", DOC_1015, "Pi_M J_H = J_M_top", "topological-Hilbert same-object condition"),
        ("design_3709", DESIGN_3709, "DI3709_3_PN_factor_budget", "P_N factor budget inequality"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "needle": needle,
            "exists": exists,
            "needle_found": needle in text if exists else False,
            "claim_allowed": False,
        })
    return rows


def definition_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEF3712_0_linearized_action",
            "local horizontal expansion",
            "S_loc[y]=S_0 + <J_y+B_y,y> + 1/2 <y,L_H y> + O(||y||^3)",
            "The source amplitude is the linear coefficient of the horizontal field around the local GR/Newton branch.",
            "definition",
        ),
        (
            "DEF3712_1_Jeff",
            "effective source norm",
            "J_eff:=||J_y+B_y||_{H*}",
            "This is the only factor in P_N that can be made exactly zero by a source-silence theorem.",
            "definition",
        ),
        (
            "DEF3712_2_source_split",
            "three-piece source split",
            "J_y+B_y = J_geom + J_matter + B_boundary",
            "The proof target is not mystical: kill or bound the geometric residual, matter horizontal pullback, and boundary term.",
            "derived_split",
        ),
        (
            "DEF3712_3_norm_bound",
            "triangle bound",
            "J_eff <= ||J_geom|| + ||J_matter|| + ||B_boundary||",
            "This gives a fallback finite bound if exact silence does not close.",
            "derived_bound",
        ),
    ]
    return [
        {
            **base(timestamp),
            "definition_id": row_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, obj, formula, meaning, status in specs
    ]


def zero_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZERO3712_0_geometric_extremum",
            "J_geom=0",
            "local GR/Newton background is a stationary point of the parent geometric sector in horizontal directions",
            "P_H delta S_geom|_0=0",
            "CONDITION_REQUIRED",
            "not signed without parent L_H/domain/extremum certificate",
        ),
        (
            "ZERO3712_1_matter_H_silence",
            "J_matter=0",
            "matter action descends through observed quotient data and the horizontal direction is invisible to that data",
            "S_matter=bar S_matter[q_obs(Phi),psi] and Dq_obs[P_H delta Phi]=0 at the local branch",
            "CONDITION_REQUIRED",
            "1055 gives a constructible source-label-forgetting contract, not a parent derivation",
        ),
        (
            "ZERO3712_2_boundary_silence",
            "B_boundary=0",
            "local boundary/reference term has no horizontal flux in the compact exterior or is cancelled by the fixed reference",
            "delta_y S_boundary|_0=0",
            "CONDITION_REQUIRED",
            "1012/1015 flux and same-source boundary closure remain unsigned",
        ),
        (
            "ZERO3712_3_zero_theorem",
            "J_eff=0 => P_N=0",
            "if ZERO3712_0 through ZERO3712_2 all hold, then J_y+B_y=0, J_eff=0, and P_N=K_N*rho_Newton*C_H^2*J_eff^2=0 for finite remaining factors",
            "J_geom=J_matter=B_boundary=0 => J_y+B_y=0",
            "THEOREM_CONDITIONAL_NOT_CLAIMED",
            "conditions are exact but not parent-signed for current MTS",
        ),
    ]
    return [
        {
            **base(timestamp),
            "zero_id": row_id,
            "target": target,
            "condition": condition,
            "formal_condition": formal,
            "status": status,
            "remaining_gap": gap,
            "claim_allowed": False,
        }
        for row_id, target, condition, formal, status, gap in specs
    ]


def finite_bound_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "BND3712_0_matter_pullback",
            "||J_matter|| <= T_matter * epsilon_qH",
            "T_matter:=||delta bar S_matter/delta q_obs||, epsilon_qH:=||Dq_obs P_H||",
            "matter term vanishes if epsilon_qH=0; otherwise it is a controlled quotient-leakage row",
            "NONCLAIM_BOUND_TEMPLATE",
        ),
        (
            "BND3712_1_geometry_residual",
            "||J_geom|| <= epsilon_geom",
            "epsilon_geom:=||P_H delta S_geom|_0||",
            "measures failure of the local background to be a horizontal extremum",
            "NONCLAIM_BOUND_TEMPLATE",
        ),
        (
            "BND3712_2_boundary_residual",
            "||B_boundary|| <= epsilon_boundary",
            "epsilon_boundary:=sup_{||y||=1}|delta_y S_boundary|_0|",
            "measures retained local/reference/boundary flux",
            "NONCLAIM_BOUND_TEMPLATE",
        ),
        (
            "BND3712_3_master_Jeff_bound",
            "J_eff <= epsilon_geom + T_matter*epsilon_qH + epsilon_boundary",
            "combine BND3712_0 through BND3712_2",
            "feeds the 3711 R10/Newton source-product budgets without pretending exact zero",
            "DERIVED_FINITE_BOUND",
        ),
        (
            "BND3712_4_R10_budget_match",
            "epsilon_geom + T_matter*epsilon_qH + epsilon_boundary <= sqrt(P_N_max/(K_N*rho_Newton*C_H^2))",
            "substitute the master J_eff bound into the factor budget",
            "this is the executable local-source criterion for the next runner",
            "DERIVED_PASS_CRITERION_NONCLAIM",
        ),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": row_id,
            "bound": bound,
            "definitions": definitions,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, bound, definitions, use, status in specs
    ]


def budget_match_rows(timestamp: str, budgets_3711: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    master_left = "epsilon_geom + T_matter*epsilon_qH + epsilon_boundary"
    for index, budget in enumerate(budgets_3711):
        rows.append({
            **base(timestamp),
            "match_id": f"BM3712_{index}_{budget['source_budget_id']}",
            "budget_role": budget["budget_role"],
            "lambda_um": budget["lambda_um"],
            "P_N_max_eta10_m4": budget["P_N_max_eta10_m4"],
            "left_side": master_left,
            "right_side": budget["J_eff_bound_formula"].replace("J_eff <= ", ""),
            "pass_condition": f"{master_left} <= {budget['J_eff_bound_formula'].replace('J_eff <= ', '')}",
            "status": "NONCLAIM_EXECUTABLE_INEQUALITY",
            "claim_allowed": False,
        })
    return rows


def obstruction_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("OBS3712_0_DqH", "epsilon_qH", "need Dq_obs P_H=0 or a norm bound", "without it quotient descent does not silence horizontal matter coupling"),
        ("OBS3712_1_Tmatter", "T_matter", "need same-frame stress/source norm", "without it the bound is symbolic"),
        ("OBS3712_2_boundary", "epsilon_boundary", "need boundary/reference horizontal flux zero or finite row", "without it exact silence fails even if matter descends"),
        ("OBS3712_3_geometry", "epsilon_geom", "need parent local horizontal extremum certificate", "without it the local branch is not proved stationary"),
        ("OBS3712_4_DCX", "parent D C_X/Omega map", "need vertical/horizontal generator owner", "without it no-pole/gauge-zero language remains unproved"),
    ]
    return [
        {
            **base(timestamp),
            "obstruction_id": row_id,
            "missing_object": obj,
            "required_fill": fill,
            "failure_mode": failure,
            "claim_allowed": False,
        }
        for row_id, obj, fill, failure in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3712_0_zero_theorem_written", "The exact J_eff zero theorem has a clean three-clause form: geometric extremum, matter H-silence, and boundary silence.", "This is a real derivation target, not a plateau axiom.", "CONDITIONAL_ZERO_THEOREM_WRITTEN"),
        ("DEC3712_1_bound_written", "If exact zero fails, J_eff is bounded by epsilon_geom + T_matter*epsilon_qH + epsilon_boundary.", "This gives a finite source-amplitude route that can be tested against 3711 budgets.", "FINITE_BOUND_ROUTE_DERIVED"),
        ("DEC3712_2_not_claimed", "The current corpus does not yet sign epsilon_qH=0, epsilon_boundary=0, or epsilon_geom=0.", "So R10/local-GR remains nonclaim, but the next missing objects are now exact coefficients rather than vague coupling doubt.", "NO_CLAIM_PROMOTION"),
        ("DEC3712_3_next", "Next target should fill or zero epsilon_qH first.", "It is the highest-leverage clause: if Dq_obs P_H=0, matter stops sourcing the horizontal local mode.", "ADVANCE_TO_DQH_CERTIFICATE"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3712_0_geometric", "epsilon_geom=0 or source-backed finite epsilon_geom row"),
        ("CG3712_1_matter", "epsilon_qH=0 or source-backed finite epsilon_qH and T_matter rows"),
        ("CG3712_2_boundary", "epsilon_boundary=0 or source-backed finite epsilon_boundary row"),
        ("CG3712_3_budget", "master J_eff bound is below an official/reviewed R10/local arena budget"),
        ("CG3712_4_denominator", "K_N*rho_Newton and C_H are parent-owned in the same units"),
        ("CG3712_5_public", "local GR/Newton/R10 claim allowed"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": "BLOCKED",
            "claim_allowed": False,
        }
        for gate_id, requirement in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3712_0",
            "status": "JEFF_ZERO_THEOREM_CONDITIONAL_AND_FINITE_BOUND_DERIVED_NONCLAIM",
            "summary": (
                "3712 derives the local horizontal-source criterion: J_y+B_y splits into J_geom, J_matter, and B_boundary. "
                "Exact silence follows if geometric extremum, matter H-silence, and boundary silence all hold; otherwise J_eff is bounded by "
                "epsilon_geom + T_matter*epsilon_qH + epsilon_boundary and can be compared to the 3711 budgets."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3712_0",
            "target_doc": "3713-Y5-R2FR-DqH-matter-horizontal-silence-certificate-or-epsilon-qH-row.md",
            "target_script": "scripts/Y5_R2FR_3713_DqH_matter_horizontal_silence_certificate_or_epsilon_qH_row.py",
            "objective": "try to prove Dq_obs P_H=0 for the local branch, or write the finite epsilon_qH row with units/source path so J_matter <= T_matter*epsilon_qH becomes executable",
            "success_gate": "matter horizontal source either vanishes by quotient descent or is represented by a nonclaim epsilon_qH/T_matter product bound row",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    definitions: list[dict[str, object]],
    zeros: list[dict[str, object]],
    bounds: list[dict[str, object]],
    budget_matches: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3712 Y5 R2FR J_eff Zero Or Finite Bound Horizontal Source Amplitude",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- Write the local horizontal expansion as `S_loc[y]=S_0 + <J_y+B_y,y> + 1/2 <y,L_H y> + O(||y||^3)`.",
        "- Split the dangerous source as `J_y+B_y = J_geom + J_matter + B_boundary`.",
        "- Exact local silence follows from three clauses: `J_geom=0`, `J_matter=0`, and `B_boundary=0`.",
        "- If exact silence fails, the derived bound is `J_eff <= epsilon_geom + T_matter*epsilon_qH + epsilon_boundary`.",
        "- The pass criterion becomes `epsilon_geom + T_matter*epsilon_qH + epsilon_boundary <= sqrt(P_N_max/(K_N*rho_Newton*C_H^2))`.",
        "- `valid_for_claim=false`: the theorem form is clean, but the three zero/bound coefficients are not parent-signed yet.",
        "",
        "## Definitions",
        "",
    ]
    for row in definitions:
        lines.append(f"- `{row['definition_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Zero Theorem Clauses", ""])
    for row in zeros:
        lines.append(f"- `{row['zero_id']}` `{row['status']}`: {row['target']} via `{row['formal_condition']}` | gap: {row['remaining_gap']}")
    lines.extend(["", "## Finite Bound Route", ""])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` `{row['status']}`: `{row['bound']}` | {row['use']}")
    lines.extend(["", "## Budget Match", ""])
    for row in budget_matches:
        lines.append(f"- `{row['match_id']}` `{row['budget_role']}`: `{row['pass_condition']}`")
    lines.extend(["", "## Obstructions", ""])
    for row in obstructions:
        lines.append(f"- `{row['obstruction_id']}` `{row['missing_object']}`: {row['required_fill']} | {row['failure_mode']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    definitions: list[dict[str, object]],
    zeros: list[dict[str, object]],
    bounds: list[dict[str, object]],
    budget_matches: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    definition_text = "\n".join(str(row["formula"]) for row in definitions)
    checks.append(("source_split", "J_y+B_y three-piece split is written", "J_geom + J_matter + B_boundary" in definition_text, ""))
    zero_targets = {row["target"] for row in zeros}
    checks.append(("zero_clauses", "geometric, matter, and boundary zero clauses are represented", {"J_geom=0", "J_matter=0", "B_boundary=0"} <= zero_targets, ""))
    bound_text = "\n".join(str(row["bound"]) for row in bounds)
    checks.append(("master_bound", "master finite J_eff bound is derived", "epsilon_geom + T_matter*epsilon_qH + epsilon_boundary" in bound_text, ""))
    checks.append(("budget_match", "three 3711 budget rows receive pass inequalities", len(budget_matches) == 3 and all(row["status"] == "NONCLAIM_EXECUTABLE_INEQUALITY" for row in budget_matches), ""))
    obs_objects = {row["missing_object"] for row in obstructions}
    checks.append(("obstructions_exact", "next coefficient obstructions are exact named objects", {"epsilon_qH", "T_matter", "epsilon_boundary", "epsilon_geom"} <= obs_objects, ""))
    checks.append(("next_dqh", "next target advances to DqH/epsilon_qH", str(next_target[0]["target_doc"]).startswith("3713-") and "DqH" in str(next_target[0]["target_doc"]), ""))
    checks.append(("nonclaim_decisions", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3712 terms", all(term in doc_text for term in ["J_y+B_y = J_geom", "epsilon_qH", "sqrt(P_N_max", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3712*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3712 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    budgets_3711 = parse_csv(BUDGET_3711)
    sources = source_register(timestamp)
    definitions = definition_rows(timestamp)
    zeros = zero_theorem_rows(timestamp)
    bounds = finite_bound_rows(timestamp)
    budget_matches = budget_match_rows(timestamp, budgets_3711)
    obstructions = obstruction_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3712_SOURCE_REGISTER.csv",
        "definitions": RESIDUALS / "P8_Y5_R2FR_3712_HORIZONTAL_SOURCE_DEFINITION_ROWS.csv",
        "zeros": RESIDUALS / "P8_Y5_R2FR_3712_ZERO_THEOREM_ATTEMPT_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3712_FINITE_BOUND_ROWS.csv",
        "budget_match": RESIDUALS / "P8_Y5_R2FR_3712_BUDGET_MATCH_ROWS.csv",
        "obstructions": RESIDUALS / "P8_Y5_R2FR_3712_OBSTRUCTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3712_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3712_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3712_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3712_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3712_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["definitions"], definitions)
    write_csv(outputs["zeros"], zeros)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["budget_match"], budget_matches)
    write_csv(outputs["obstructions"], obstructions)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, definitions, zeros, bounds, budget_matches, obstructions, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, definitions, zeros, bounds, budget_matches, obstructions, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3712 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3712 checkpoint: J_eff zero theorem and finite bound route derived")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
