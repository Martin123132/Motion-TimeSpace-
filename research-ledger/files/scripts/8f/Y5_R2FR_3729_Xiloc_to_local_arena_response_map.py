from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3729"
BRANCH_ID = "MTS_R2FR_Y5_XILOC_TO_LOCAL_ARENA_RESPONSE_MAP_3729"
DOC = ROOT / "3729-Y5-R2FR-Xiloc-to-local-arena-response-map.md"

DOC_3728 = ROOT / "3728-Y5-R2FR-combined-Xiloc-runner-and-refusal-gates.md"
NEXT_3728 = RESIDUALS / "P8_Y5_R2FR_3728_NEXT_TARGET.csv"
RUNNER_3728 = RESIDUALS / "P8_Y5_R2FR_3728_XILOC_RUNNER_STATUS.csv"
CLAIM_GATES_3728 = RESIDUALS / "P8_Y5_R2FR_3728_CLAIM_GATES.csv"
VALIDATION_3728 = RESIDUALS / "P8_Y5_BRR545_3728_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
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


def try_float(value: object) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3728", DOC_3728, "ADVANCE_TO_RESPONSE_ARENA_MAP", "3728 decision to route Xi_loc into arenas"),
        ("next_3728", NEXT_3728, "3729-Y5-R2FR-Xiloc-to-local-arena-response-map.md", "3728 handoff target"),
        ("runner_3728", RUNNER_3728, "Xi_loc=u_min^2", "3728 combined Xi_loc runner"),
        ("claim_gates_3728", CLAIM_GATES_3728, "positive Xi_loc mapped", "3728 arena claim gate"),
        ("validation_3728", VALIDATION_3728, "next_target_3729", "3728 validation record"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(ts),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def arena_specs() -> list[dict[str, str]]:
    formula = "residual_bound_A=beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A"
    pass_condition = "Xi_loc>ell_A and residual_bound_A<=bound_A"
    return [
        {
            "arena_id": "ARENA3729_0_R10",
            "arena": "R10_short_range",
            "observable_residual": "alpha(lambda) fifth-force residual",
            "baseline_limit": "Newton inverse-square laboratory torsion response",
            "required_bound_source": "R10 alpha(lambda) bound curve or source-backed anchors",
            "response_formula": formula,
            "pass_condition": pass_condition,
        },
        {
            "arena_id": "ARENA3729_1_PPN",
            "arena": "PPN_solar_system",
            "observable_residual": "PPN residual vector including gamma-1, beta-1, preferred-frame terms",
            "baseline_limit": "metric GR weak-field post-Newtonian limit",
            "required_bound_source": "PPN experimental bound table with units and assumptions",
            "response_formula": formula,
            "pass_condition": pass_condition,
        },
        {
            "arena_id": "ARENA3729_2_CLOCKS",
            "arena": "clock_redshift",
            "observable_residual": "fractional frequency/redshift residual",
            "baseline_limit": "GR proper-time and gravitational redshift limit",
            "required_bound_source": "clock/redshift bound table with source path",
            "response_formula": formula,
            "pass_condition": pass_condition,
        },
        {
            "arena_id": "ARENA3729_3_ORBITS",
            "arena": "orbital_dynamics",
            "observable_residual": "perihelion, range, timing, and acceleration residual vector",
            "baseline_limit": "Newtonian plus GR weak-field orbital dynamics",
            "required_bound_source": "orbital residual bounds and body/system assumptions",
            "response_formula": formula,
            "pass_condition": pass_condition,
        },
        {
            "arena_id": "ARENA3729_4_EM_Poynting",
            "arena": "EM_Poynting_waves",
            "observable_residual": "Maxwell stress, wave, and Poynting-balance residual",
            "baseline_limit": "Maxwell vacuum/material energy-flux balance",
            "required_bound_source": "EM wave/Poynting constraint or theorem-zero residual",
            "response_formula": formula,
            "pass_condition": pass_condition,
        },
        {
            "arena_id": "ARENA3729_5_NEWTON",
            "arena": "Newton_limit",
            "observable_residual": "local acceleration and Poisson-potential residual",
            "baseline_limit": "Newtonian mechanics recovered from the local weak-field branch",
            "required_bound_source": "Newton-limit theorem residual or precision bound",
            "response_formula": formula,
            "pass_condition": pass_condition,
        },
    ]


def arena_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            **spec,
            "status": "RESPONSE_CONTRACT_READY_CURRENTLY_BLOCKED",
            "claim_allowed": False,
        }
        for spec in arena_specs()
    ]


def xi_from_3728() -> tuple[float | None, bool, str]:
    if not RUNNER_3728.exists():
        return None, False, "MISSING_3728_RUNNER"
    rows = parse_csv(RUNNER_3728)
    if not rows:
        return None, False, "EMPTY_3728_RUNNER"
    row = rows[0]
    xi_value = try_float(row.get("xi_loc", ""))
    executable = str(row.get("executable", "")) == "True"
    missing = str(row.get("missing_inputs", ""))
    sign_failures = str(row.get("sign_failures", ""))
    positive = str(row.get("positive_gap", "")) == "True"
    if xi_value is None:
        return None, False, str(row.get("status", "MISSING_XILOC_VALUE"))
    available = executable and not missing and not sign_failures and positive and xi_value > 0
    return xi_value, available, str(row.get("status", "UNKNOWN_3728_STATUS"))


def arena_input_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = [{
        **base(ts),
        "input_id": "AIN3729_GLOBAL_Xiloc",
        "arena": "GLOBAL",
        "quantity": "Xi_loc",
        "value": "MISSING_XILOC_FROM_3728",
        "required_sign": "positive",
        "units": "local_operator_gap_units",
        "meaning": "positive coercive local gap from 3728",
        "source_path": str(RUNNER_3728),
        "source_owned": False,
        "claim_allowed": False,
    }]
    quantity_specs = [
        ("sigma_A", "MISSING_SOURCE_NORM", "nonnegative", "arena_source_norm_units", "norm of the arena source/coupling residual"),
        ("beta_A", "MISSING_RESPONSE_NORM", "nonnegative", "observable_per_solution_norm", "operator norm from local solution perturbation to observable residual"),
        ("ell_A", "MISSING_NONLINEAR_LOSS", "nonnegative", "local_operator_gap_units", "arena nonlinear/Lipschitz loss subtracted from Xi_loc"),
        ("epsilon_A", "MISSING_PROJECTION_FLOOR", "nonnegative", "observable_residual_units", "projection/discretization/background residual floor"),
        ("bound_A", "MISSING_EMPIRICAL_BOUND", "positive", "observable_residual_units", "empirical or theorem bound for the arena residual"),
    ]
    for spec in arena_specs():
        arena = spec["arena"]
        safe = arena.upper().replace("-", "_")
        for quantity, value_prefix, required_sign, units, meaning in quantity_specs:
            rows.append({
                **base(ts),
                "input_id": f"AIN3729_{safe}_{quantity}",
                "arena": arena,
                "quantity": quantity,
                "value": f"{value_prefix}_{safe}",
                "required_sign": required_sign,
                "units": units,
                "meaning": meaning,
                "source_path": "MISSING_PARENT_OR_DATA_SOURCE_PATH",
                "source_owned": False,
                "claim_allowed": False,
            })
    return rows


def runner_rows(ts: str, inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    xi_value, xi_available, xi_status = xi_from_3728()
    rows: list[dict[str, object]] = []
    by_arena: dict[str, dict[str, dict[str, object]]] = {}
    for row in inputs:
        arena = str(row["arena"])
        by_arena.setdefault(arena, {})[str(row["quantity"])] = row
    for spec in arena_specs():
        arena = spec["arena"]
        missing: list[str] = []
        sign_failures: list[str] = []
        values: dict[str, float] = {}
        if not xi_available:
            missing.append("Xi_loc")
        for quantity in ["sigma_A", "beta_A", "ell_A", "epsilon_A", "bound_A"]:
            input_row = by_arena.get(arena, {}).get(quantity)
            if input_row is None:
                missing.append(quantity)
                continue
            parsed = try_float(input_row["value"])
            if parsed is None or str(input_row["source_owned"]) != "True":
                missing.append(quantity)
                continue
            if input_row["required_sign"] == "positive" and parsed <= 0:
                sign_failures.append(quantity)
            if input_row["required_sign"] == "nonnegative" and parsed < 0:
                sign_failures.append(quantity)
            values[quantity] = parsed
        executable = not missing and not sign_failures and xi_value is not None
        denominator: float | str = ""
        residual_bound: float | str = ""
        arena_pass = False
        status = "BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS"
        if executable:
            denominator_value = xi_value - values["ell_A"]
            denominator = denominator_value
            if denominator_value <= 0:
                status = "BLOCKED_NONPOSITIVE_RESPONSE_DENOMINATOR"
            else:
                residual_value = values["beta_A"] * values["sigma_A"] / denominator_value + values["epsilon_A"]
                residual_bound = residual_value
                arena_pass = residual_value <= values["bound_A"]
                status = "EXECUTABLE_PASS_NONCLAIM" if arena_pass else "EXECUTABLE_FAIL_OR_TOO_LARGE"
        rows.append({
            **base(ts),
            "runner_id": f"RUN3729_{arena}",
            "arena": arena,
            "input_xiloc_status": xi_status,
            "formula": spec["response_formula"],
            "executable": executable,
            "missing_inputs": ";".join(missing),
            "sign_failures": ";".join(sign_failures),
            "denominator_Xi_minus_ell": denominator,
            "predicted_residual_bound": residual_bound,
            "arena_pass_nonclaim": arena_pass,
            "status": status,
            "claim_allowed": False,
        })
    return rows


def refusal_rows(ts: str, runner: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in runner:
        arena = str(row["arena"])
        for quantity in [item for item in str(row["missing_inputs"]).split(";") if item]:
            rows.append({
                **base(ts),
                "refusal_id": f"REF3729_{arena}_{quantity}",
                "arena": arena,
                "quantity": quantity,
                "reason": "missing numeric source-owned response input",
                "required_fix": f"derive or source {quantity} for {arena} before using the response inequality",
                "claim_allowed": False,
            })
        for quantity in [item for item in str(row["sign_failures"]).split(";") if item]:
            rows.append({
                **base(ts),
                "refusal_id": f"REF3729_{arena}_sign_{quantity}",
                "arena": arena,
                "quantity": quantity,
                "reason": "input sign violates response-map gate",
                "required_fix": f"repair or reject {quantity} for {arena}",
                "claim_allowed": False,
            })
        if row["status"] == "BLOCKED_NONPOSITIVE_RESPONSE_DENOMINATOR":
            rows.append({
                **base(ts),
                "refusal_id": f"REF3729_{arena}_denominator",
                "arena": arena,
                "quantity": "Xi_loc-ell_A",
                "reason": "response denominator is nonpositive",
                "required_fix": "prove Xi_loc exceeds arena nonlinear loss ell_A",
                "claim_allowed": False,
            })
    if not rows:
        rows.append({
            **base(ts),
            "refusal_id": "REF3729_none",
            "arena": "all",
            "quantity": "none",
            "reason": "all arena response inputs present; claim still withheld until independent review",
            "required_fix": "compare executable nonclaim residuals against sourced experimental bounds",
            "claim_allowed": False,
        })
    return rows


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3729_0_coercive_response_bound",
            "If <h,Lh> >= Xi_loc||h||^2 and ||N_A(h)|| <= ell_A||h|| with ell_A < Xi_loc, then ||h_A|| <= sigma_A/(Xi_loc-ell_A).",
            "Local coercivity converts source/coupling residual into a bounded local perturbation.",
            "DERIVED_CONTRACT",
        ),
        (
            "THM3729_1_observable_pushforward",
            "If ||B_A|| <= beta_A, then residual_bound_A=beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A.",
            "Each empirical arena needs its own response norm and residual floor.",
            "DERIVED_CONTRACT",
        ),
        (
            "THM3729_2_no_claim_from_Xi_alone",
            "Xi_loc>0 is not an arena pass without sigma_A, beta_A, ell_A, epsilon_A, and bound_A.",
            "Stops a positive local gap from being smuggled into R10/PPN/clock/orbit/EM/Newton claims.",
            "ANTI_OVERCLAIM",
        ),
        (
            "THM3729_3_EM_Poynting_is_an_arena",
            "The Poynting/wave route enters as EM_Poynting_waves with the same response inequality, not as an assumed Maxwell recovery.",
            "Keeps the user's background-field/Poynting idea alive but gateable.",
            "ROUTE_OPEN_BLOCKED",
        ),
        (
            "THM3729_4_GR_Newton_bridge_is_residual_based",
            "Derived local GR/Newton recovery means bounded PPN/orbital/Newton residuals, not a declaration that the branch is GR.",
            "Turns the GR reduction target into measurable residual inequalities.",
            "DISCIPLINE_GATE",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, clause, meaning, status in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3729_0_response_map_ready",
            "RESPONSE_MAP_CONTRACT_READY",
            "A future positive Xi_loc now has a concrete path into R10, PPN, clocks, orbits, EM/Poynting, and Newton residual bounds.",
        ),
        (
            "DEC3729_1_current_blocked",
            "CURRENT_ARENAS_BLOCKED_BY_MISSING_XILOC_AND_COUPLINGS",
            "The runner refuses every arena because Xi_loc and arena coupling/source response rows are not numeric/source-owned.",
        ),
        (
            "DEC3729_2_next",
            "NEXT_ATTACK_COUPLING_SOURCE_NORMS",
            "The highest-leverage derivation is sigma_A and beta_A from matter coupling/descent, because those feed every local arena.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in rows
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3729_0_Xi", "BLOCKED", "3728 produces positive numeric Xi_loc with no missing factors"),
        ("CG3729_1_source", "BLOCKED", "each arena has source/coupling norm sigma_A"),
        ("CG3729_2_response", "BLOCKED", "each arena has observable response norm beta_A"),
        ("CG3729_3_loss", "BLOCKED", "each arena proves ell_A < Xi_loc"),
        ("CG3729_4_floor", "BLOCKED", "each arena has projection floor epsilon_A"),
        ("CG3729_5_bound", "BLOCKED", "each arena has sourced empirical or theorem bound_A"),
        ("CG3729_6_runner", "BLOCKED", "response runner predicts residual_bound_A <= bound_A"),
        ("CG3729_7_claim", "BLOCKED", "local-GR/Newton/EM arena claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": gate_status,
            "required_before_claim": required_before_claim,
            "claim_allowed": False,
        }
        for gate_id, gate_status, required_before_claim in gates
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3729_0",
        "status": "RESPONSE_MAP_READY_CURRENTLY_BLOCKED_BY_XILOC_AND_ARENA_INPUTS",
        "summary": "3729 converts a future positive Xi_loc into arena residual inequalities. Current rows are placeholders, so no R10, PPN, clock, orbital, EM/Poynting, Newton, local-GR, or local-Newton claim is allowed.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3729_0",
        "target_doc": "3730-Y5-R2FR-coupling-source-norm-derivation-hunt.md",
        "target_script": "scripts/Y5_R2FR_3730_coupling_source_norm_derivation_hunt.py",
        "objective": "derive or source sigma_A and beta_A from matter coupling/descent so the response map stops being a formal shell",
        "success_gate": "at least one arena has a parent-owned sigma_A/beta_A derivation route or a theorem-blocker with exact missing axiom",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3729*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    runner = parse_csv(paths["runner"])
    arenas = parse_csv(paths["arenas"])
    claim_gates = parse_csv(paths["claim_gates"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("arena_schema", "six local response arenas present", len(arenas) == 6),
        ("input_schema", "global Xi plus five inputs per arena present", len(parse_csv(paths["inputs"])) == 31),
        ("runner_blocks_placeholders", "runner blocks placeholders", all(row["status"] == "BLOCKED_MISSING_XILOC_OR_ARENA_INPUTS" for row in runner)),
        ("formula_contract", "response formula is present", all("beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A" in row["formula"] for row in runner)),
        ("em_poynting_included", "EM/Poynting arena included", any(row["arena"] == "EM_Poynting_waves" for row in arenas)),
        ("refusal_rows", "refusal rows exist for blocked arenas", len(parse_csv(paths["refusals"])) >= 30),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3730", "next target is coupling derivation", all(token in read_text(paths["next_target"]) for token in ["3730", "coupling", "sigma_A", "beta_A"])),
        ("doc_core_terms", "doc contains response-map status", all(token in read_text(paths["doc"]) for token in ["RESPONSE_MAP_CONTRACT_READY", "Xi_loc-ell_A", "EM_Poynting_waves"])),
        ("no_formalization_leak", "no 3729 files in formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3729 - Xi_loc to Local Arena Response Map",
        "",
        "## Status",
        "- `RESPONSE_MAP_READY_CURRENTLY_BLOCKED_BY_XILOC_AND_ARENA_INPUTS`",
        "- Main response law: `residual_bound_A=beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A`.",
        "- Pass condition: `Xi_loc>ell_A` and `residual_bound_A<=bound_A`.",
        "- This is a bridge from local coercivity to measurable arenas, not a claim that local GR/Newton/Maxwell has been recovered.",
        "",
        "## Derived Contract",
        "- Coercive local branch: `<h,Lh> >= Xi_loc||h||^2`.",
        "- Arena nonlinear loss: `||N_A(h)|| <= ell_A||h||`.",
        "- Source/coupling norm: `||source_A|| <= sigma_A`.",
        "- Observable map norm: `||B_A|| <= beta_A`.",
        "- Therefore `||residual_A|| <= beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A`, if `ell_A < Xi_loc`.",
        "",
        "## Arena Rows",
    ]
    for row in grouped["arenas"]:
        lines.append(f"- `{row['arena']}`: {row['observable_residual']} | baseline: {row['baseline_limit']} | status `{row['status']}`")
    lines.extend(["", "## Runner Rows"])
    for row in grouped["runner"]:
        lines.append(f"- `{row['arena']}` `{row['status']}` missing=`{row['missing_inputs']}` predicted=`{row['predicted_residual_bound']}`")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Refusals"])
    lines.append("- Every arena is blocked until `Xi_loc`, `sigma_A`, `beta_A`, `ell_A`, `epsilon_A`, and `bound_A` are numeric/source-owned.")
    lines.append("- The EM/Poynting route is retained as a proper response arena rather than being discarded or assumed.")
    lines.extend(["", "## Next Target"])
    lines.append("- `3730-Y5-R2FR-coupling-source-norm-derivation-hunt.md`")
    lines.append("- Objective: derive or source `sigma_A` and `beta_A` from matter coupling/descent, because that is the common bottleneck for R10/PPN/clocks/orbits/EM/Newton.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3729_SOURCE_REGISTER.csv",
        "arenas": RESIDUALS / "P8_Y5_R2FR_3729_RESPONSE_ARENA_ROWS.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3729_ARENA_INPUT_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3729_RESPONSE_RUNNER_STATUS.csv",
        "refusals": RESIDUALS / "P8_Y5_R2FR_3729_REFUSAL_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3729_THEOREM_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3729_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3729_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3729_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3729_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3729_VALIDATION.csv",
        "doc": DOC,
    }
    inputs = arena_input_rows(ts)
    runner = runner_rows(ts, inputs)
    grouped = {
        "source_register": source_register(ts),
        "arenas": arena_rows(ts),
        "inputs": inputs,
        "runner": runner,
        "refusals": refusal_rows(ts, runner),
        "theorems": theorem_rows(ts),
        "decisions": decision_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3729 validation failed: {failures}")
    print("wrote 3729 checkpoint: Xi_loc response map ready and all arenas blocked by missing source/coupling inputs")


if __name__ == "__main__":
    main()
