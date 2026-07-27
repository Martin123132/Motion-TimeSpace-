from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3750"
BRANCH_ID = "MTS_R2FR_Y5_OPERATOR_NORM_SOURCE_OR_PARENT_PARALLEL_SPLIT_PROOF_3750"
DOC = ROOT / "3750-Y5-R2FR-operator-norm-source-or-parent-parallel-split-proof.md"

DOC_3748 = ROOT / "3748-Y5-R2FR-parent-bundle-split-construction-or-projector-leak-bound.md"
DOC_3749 = ROOT / "3749-Y5-R2FR-local-Fermi-domain-projector-leak-numeric-smoke.md"
RESULTS_3749 = RESIDUALS / "P8_Y5_R2FR_3749_FERMI_DOMAIN_RESULTS.csv"
GATES_3749 = RESIDUALS / "P8_Y5_R2FR_3749_CLAIM_GATES.csv"
NEXT_3749 = RESIDUALS / "P8_Y5_R2FR_3749_NEXT_TARGET.csv"
VALIDATION_3749 = RESIDUALS / "P8_Y5_BRR545_3749_VALIDATION.csv"
LOCAL_EH_OPERATOR_AUDIT = RESIDUALS / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv"
EH_DOMINANCE_PACK = RESIDUALS / "P8_Y5_EH_DOMINANCE_GATE_2620_OPERATOR_COEFFICIENT_PACK.csv"
PPN_INTERFACE_2636 = RESIDUALS / "P8_Y5_GENERATOR_EFFECTIVE_PACK_2636_PPN_INTERFACE_MAP.csv"
BETA_EVALUATOR = RESIDUALS / "P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv"
COMM_PROJECTOR_FILL = RESIDUALS / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv"


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
        ("doc_3749_status", DOC_3749, "FERMI_PROJECTOR_LEAK_NUMERIC_SMOKE_PASSES_NONCLAIM", "3749 smoke handoff"),
        ("doc_3749_gain", DOC_3749, "smallest hidden-operator gain-to-fail", "hidden operator cap handoff"),
        ("results_3749", RESULTS_3749, "hidden_operator_gain_to_fail_min_tol", "machine-readable smoke margins"),
        ("gates_3749_source_values", GATES_3749, "CG3749_4_source_values", "source values still missing"),
        ("next_3749", NEXT_3749, "3750-Y5-R2FR-operator-norm-source-or-parent-parallel-split-proof.md", "3749 next target"),
        ("validation_3749", VALIDATION_3749, "no_formalization_leak", "3749 clean validation"),
        ("doc_3748_offdiag", DOC_3748, "off-diagonal connection blocks", "parent parallel split obstruction"),
        ("local_eh_projector_stress", LOCAL_EH_OPERATOR_AUDIT, "projector_domain_stress", "operator audit: projector stress"),
        ("eh_dominance_projector", EH_DOMINANCE_PACK, "OPC2620_2_projector", "operator coefficient pack: projector residual"),
        ("ppn_interface_total", PPN_INTERFACE_2636, "PPNI2636_6_total_abs", "PPN interface absolute envelope"),
        ("beta_evaluator_bound", BETA_EVALUATOR, "7.8e-05", "beta placeholder comparator"),
        ("comm_projector_missing", COMM_PROJECTOR_FILL, "MISSING_GAMMA_COEFFICIENT", "commutator projector coefficient gap"),
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


def operator_source_audit_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("OSA3750_0_projector_stress", "c_projector_domain_stress", "0 only if parent owns metric-independent topological projector; otherwise missing coefficient", "CONDITIONAL_ZERO_NOT_PARENT_OWNED", "blocks claim; supports target H_op cap"),
        ("OSA3750_1_projector_operator", "c_projector", "E_projector or [d,Pi_M]J_H", "MISSING_PROJECTOR_ACTION_VARIATION_OR_BOUND", "matches epsilon_comm_Fermi source gap"),
        ("OSA3750_2_total_ppn_abs", "Delta_PPN_abs", "absolute envelope across all generator components", "SCHEMA_READY_VALUES_MISSING", "requires no-cancellation total, not gamma-only pass"),
        ("OSA3750_3_beta_reference", "beta_bound", "7.8e-05 reference-only comparator", "REFERENCE_ONLY_NOT_CLAIM", "usable as smoke threshold only"),
        ("OSA3750_4_comm_projector", "c_projector_to_gamma/beta", "missing gamma/beta/alpha3/xi coefficients for commutator projector", "MISSING_RESPONSE_COEFFICIENTS", "operator norms not source-backed"),
        ("OSA3750_5_verdict", "H_op", "hidden product C_pair*C_Fermi*operator_norms*PPN_response", "NOT_SOURCED", "must be below cap or theorem-zero"),
    ]
    return [
        {
            **base(timestamp),
            "audit_id": audit_id,
            "quantity": quantity,
            "source_readout": source_readout,
            "status": status,
            "use_in_3750": use_in_3750,
            "claim_allowed": False,
        }
        for audit_id, quantity, source_readout, status, use_in_3750 in specs
    ]


def parent_parallel_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PPA3750_0_target", "prove A_ML=0 and A_LM=0", "connection preserves E_L direct-sum E_M", "WOULD_THEOREM_ZERO_EPSILON_COMM", "not sourced"),
        ("PPA3750_1_metric_independence", "P_M independent of local metric/coframe variations", "delta_L P_M=0", "WOULD_THEOREM_ZERO_EPSILON_DELTAP", "not sourced"),
        ("PPA3750_2_topological_candidate", "projector is topological/cohomological before readout", "metric variation of projector stress vanishes", "PLAUSIBLE_ROUTE", "older audits call this conditional only"),
        ("PPA3750_3_countermodel", "P_M depends on domain/marker/transition variables", "A_ML or deltaP generally nonzero", "COUNTERMODEL_ACTIVE", "requires finite bound"),
        ("PPA3750_4_current_verdict", "parent parallel split proof", "A_ML=0 cannot be promoted from current corpus", "UNSIGNED", "use norm cap route"),
    ]
    return [
        {
            **base(timestamp),
            "attempt_id": attempt_id,
            "target": target,
            "mathematical_condition": condition,
            "would_do": would_do,
            "current_status": current_status,
            "claim_allowed": False,
        }
        for attempt_id, target, condition, would_do, current_status in specs
    ]


def norm_cap_rows(timestamp: str, results: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    min_row: dict[str, str] | None = None
    min_cap = float("inf")
    for result in results:
        cap = float(result["hidden_operator_gain_to_fail_min_tol"])
        if cap < min_cap:
            min_cap = cap
            min_row = result
        rows.append({
            **base(timestamp),
            "cap_id": result["result_id"].replace("RES", "CAP"),
            "scenario_id": result["scenario_id"],
            "epsilon_unit_norm": result["epsilon_comm_Fermi"],
            "H_op_max_to_pass_placeholder_tol": f"{cap:.12e}",
            "status": "CAP_FROM_NONCLAIM_SMOKE",
            "meaning": "if hidden operator product H_op is below this cap, this scenario passes placeholder tolerances",
            "claim_allowed": False,
        })
    if min_row is None:
        raise ValueError("no 3749 result rows")
    rows.append({
        **base(timestamp),
        "cap_id": "CAP3750_GLOBAL_MIN",
        "scenario_id": min_row["scenario_id"],
        "epsilon_unit_norm": min_row["epsilon_comm_Fermi"],
        "H_op_max_to_pass_placeholder_tol": f"{min_cap:.12e}",
        "status": "GLOBAL_CAP_FROM_WORST_SMOKE_SCENARIO",
        "meaning": "all 3749 smoke scenarios pass placeholder tolerances if H_op is below this global cap",
        "claim_allowed": False,
    })
    return rows


def sensitivity_rows(timestamp: str, results: list[dict[str, str]]) -> list[dict[str, object]]:
    gains = [1.0, 1.0e6, 1.0e9, 1.0e12, 5.0e12, 1.0e13]
    rows: list[dict[str, object]] = []
    for gain in gains:
        worst_ratio = 0.0
        failing: list[str] = []
        for result in results:
            cap = float(result["hidden_operator_gain_to_fail_min_tol"])
            ratio = gain / cap
            worst_ratio = max(worst_ratio, ratio)
            if ratio > 1.0:
                failing.append(result["scenario_id"])
        rows.append({
            **base(timestamp),
            "sensitivity_id": f"SENS3750_H_{gain:.0e}",
            "H_op_test_value": f"{gain:.12e}",
            "worst_fraction_of_cap": f"{worst_ratio:.12e}",
            "all_scenarios_pass_placeholder_tol": len(failing) == 0,
            "failing_scenarios": ";".join(failing),
            "status": "NONCLAIM_SENSITIVITY",
            "claim_allowed": False,
        })
    return rows


def bound_contract_rows(timestamp: str, caps: list[dict[str, object]]) -> list[dict[str, object]]:
    global_row = next(row for row in caps if row["cap_id"] == "CAP3750_GLOBAL_MIN")
    global_cap = global_row["H_op_max_to_pass_placeholder_tol"]
    specs = [
        ("BC3750_0_define_Hop", "H_op := C_pair * ||E_M^nabla||_D * ||deltaPhi_L||_D * PPN_response_norm", "dimensionless hidden gain multiplying epsilon_comm_Fermi", "definition ready"),
        ("BC3750_1_required_cap", f"H_op <= {global_cap}", "global nonclaim smoke cap from worst 3749 scenario", "target bound"),
        ("BC3750_2_parent_zero_option", "A_ML=0 and delta_L P_M=0", "theorem-zero alternative to bounding H_op", "unsigned"),
        ("BC3750_3_no_cancellation", "epsilon_proj_leak_abs added to S_eff, not canceled against other residuals", "absolute-envelope policy", "guard"),
        ("BC3750_4_claim_status", "claim_allowed=false", "operator norm source and parent zero both missing", "nonclaim"),
    ]
    return [
        {
            **base(timestamp),
            "contract_id": contract_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for contract_id, condition, meaning, status in specs
    ]


def decision_rows(timestamp: str, caps: list[dict[str, object]], sensitivities: list[dict[str, object]]) -> list[dict[str, object]]:
    global_cap = next(row for row in caps if row["cap_id"] == "CAP3750_GLOBAL_MIN")["H_op_max_to_pass_placeholder_tol"]
    first_fail = next((row for row in sensitivities if row["all_scenarios_pass_placeholder_tol"] is False), None)
    first_fail_text = first_fail["H_op_test_value"] if first_fail else "none_tested"
    specs = [
        ("DEC3750_0_operator_source", "NO_SOURCED_OPERATOR_NORM_FOUND", "existing operator tables still mark projector/PPN response coefficients missing or conditional"),
        ("DEC3750_1_cap", "HIDDEN_OPERATOR_CAP_DERIVED_FROM_SMOKE", f"all smoke scenarios require H_op <= {global_cap} using placeholder tolerances"),
        ("DEC3750_2_sensitivity", "SENSITIVITY_BRACKETED", f"tested gains pass through 5e12 and first fail at {first_fail_text}"),
        ("DEC3750_3_parent", "PARENT_PARALLEL_SPLIT_UNSIGNED", "A_ML=0 remains the clean proof route but is not sourced"),
        ("DEC3750_4_next", "NEXT_SOURCE_HOP_OR_SHARPEN_PARENT_ZERO", "either bound H_op from operator theory, or construct the topological/parallel projector proof"),
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


def claim_gate_rows(timestamp: str, sensitivities: list[dict[str, object]]) -> list[dict[str, object]]:
    pass_1e12 = any(row["H_op_test_value"] == f"{1.0e12:.12e}" and row["all_scenarios_pass_placeholder_tol"] is True for row in sensitivities)
    fail_1e13 = any(row["H_op_test_value"] == f"{1.0e13:.12e}" and row["all_scenarios_pass_placeholder_tol"] is False for row in sensitivities)
    specs = [
        ("CG3750_0_sources", "3750 source sweep complete", True, "registered local source paths and anchors found"),
        ("CG3750_1_operator_audit", "operator norm source audit completed", True, "existing rows inspected and recorded"),
        ("CG3750_2_parent_zero", "A_ML=0 parent proof achieved", False, "parent parallel split remains unsigned"),
        ("CG3750_3_cap_extracted", "hidden operator cap extracted", True, "global H_op cap from 3749 worst scenario emitted"),
        ("CG3750_4_sensitivity", "sensitivity bracket computed", pass_1e12 and fail_1e13, "1e12 passes and 1e13 fails placeholder smoke envelope"),
        ("CG3750_5_source_backed_bound", "H_op bound is source-backed", False, "H_op remains a target cap, not a sourced value"),
        ("CG3750_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "nonclaim cap and unsigned parent proof only"),
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


def status_rows(timestamp: str, caps: list[dict[str, object]]) -> list[dict[str, object]]:
    global_cap = next(row for row in caps if row["cap_id"] == "CAP3750_GLOBAL_MIN")["H_op_max_to_pass_placeholder_tol"]
    return [{
        **base(timestamp),
        "status_id": "STATUS3750_0",
        "status": "HIDDEN_OPERATOR_CAP_DERIVED_PARENT_ZERO_UNSIGNED",
        "summary": f"3750 finds no sourced operator norm or parent A_ML=0 proof; it converts the 3749 smoke margin into a nonclaim global target H_op <= {global_cap}.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3750_0",
        "target_doc": "3751-Y5-R2FR-Hop-operator-norm-decomposition-or-topological-projector-proof.md",
        "target_script": "scripts/Y5_R2FR_3751_Hop_operator_norm_decomposition_or_topological_projector_proof.py",
        "objective": "decompose H_op into C_pair, morphology Euler norm, local variation norm, and PPN response norm, or prove the projector is topological/parallel so H_op is irrelevant",
        "success_gate": "either each H_op factor gets a sourced/theorem cap below the 3750 global bound, or A_ML=delta_L P_M=0 is parent-signed",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3750 - Operator Norm Source or Parent Parallel Split Proof",
        "",
        "## Status",
        f"- `{grouped['status'][0]['status']}`",
        f"- {grouped['status'][0]['summary']}",
        "- This is a target-bound checkpoint: it does not claim local GR/PPN.",
        "",
        "## Operator Source Audit",
    ]
    for row in grouped["operator_audit"]:
        lines.append(f"- `{row['audit_id']}` `{row['status']}`: {row['quantity']} | {row['use_in_3750']}")
    lines.extend(["", "## Parent Parallel Attempt"])
    for row in grouped["parent_attempt"]:
        lines.append(f"- `{row['attempt_id']}` `{row['current_status']}`: {row['target']} | {row['mathematical_condition']}")
    lines.extend(["", "## Hidden Operator Caps"])
    for row in grouped["caps"]:
        if row["cap_id"] == "CAP3750_GLOBAL_MIN":
            lines.append(f"- `{row['cap_id']}`: H_op <= {row['H_op_max_to_pass_placeholder_tol']} from `{row['scenario_id']}`.")
    lines.extend(["", "## Sensitivity"])
    for row in grouped["sensitivity"]:
        lines.append(f"- `{row['sensitivity_id']}` pass={row['all_scenarios_pass_placeholder_tol']} worst_fraction={row['worst_fraction_of_cap']} failing={row['failing_scenarios']}")
    lines.extend(["", "## Bound Contract"])
    for row in grouped["bound_contract"]:
        lines.append(f"- `{row['contract_id']}` `{row['status']}`: {row['condition']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
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
    operator_audit = parse_csv(paths["operator_audit"])
    parent_attempt = parse_csv(paths["parent_attempt"])
    caps = parse_csv(paths["caps"])
    sensitivity = parse_csv(paths["sensitivity"])
    bound_contract = parse_csv(paths["bound_contract"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3750*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("operator_audit", "operator audit records missing sourced norms", len(operator_audit) == 6 and all(token in read_text(paths["operator_audit"]) for token in ["MISSING_RESPONSE_COEFFICIENTS", "NOT_SOURCED"])),
        ("parent_attempt", "parent zero proof remains unsigned", len(parent_attempt) == 5 and any(row["would_do"] == "UNSIGNED" for row in parent_attempt)),
        ("global_cap", "global H_op cap emitted", any(row["cap_id"] == "CAP3750_GLOBAL_MIN" and row["scenario_id"] == "SC3749_6_solar_1AU_large_domain" for row in caps)),
        ("sensitivity_bracket", "sensitivity has 1e12 pass and 1e13 fail", any(row["H_op_test_value"] == f"{1.0e12:.12e}" and row["all_scenarios_pass_placeholder_tol"] == "True" for row in sensitivity) and any(row["H_op_test_value"] == f"{1.0e13:.12e}" and row["all_scenarios_pass_placeholder_tol"] == "False" for row in sensitivity)),
        ("bound_contract", "bound contract includes H_op definition and cap", len(bound_contract) == 5 and all(token in read_text(paths["bound_contract"]) for token in ["H_op :=", "H_op <=", "A_ML=0"])),
        ("claim_gates_block", "local claim gate remains blocked", any(row["gate_id"] == "CG3750_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("claim_allowed_false", "all gate rows keep claim_allowed false", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("doc_core_terms", "doc records cap and nonclaim status", all(token in read_text(paths["doc"]) for token in ["H_op <=", "target-bound checkpoint", "Sensitivity"])),
        ("next_target_3751", "next target decomposes H_op or proves topological projector", next_target[0]["target_doc"] == "3751-Y5-R2FR-HOp-operator-norm-decomposition-or-topological-projector-proof.md" or next_target[0]["target_doc"] == "3751-Y5-R2FR-Hop-operator-norm-decomposition-or-topological-projector-proof.md"),
        ("no_formalization_leak", "no 3750 files in formalization-workbench", len(formalization_leaks) == 0),
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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3750_SOURCE_REGISTER.csv",
        "operator_audit": RESIDUALS / "P8_Y5_R2FR_3750_OPERATOR_SOURCE_AUDIT.csv",
        "parent_attempt": RESIDUALS / "P8_Y5_R2FR_3750_PARENT_PARALLEL_ATTEMPT.csv",
        "caps": RESIDUALS / "P8_Y5_R2FR_3750_HIDDEN_OPERATOR_NORM_CAPS.csv",
        "sensitivity": RESIDUALS / "P8_Y5_R2FR_3750_HOP_SENSITIVITY_ROWS.csv",
        "bound_contract": RESIDUALS / "P8_Y5_R2FR_3750_BOUND_CONTRACT_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3750_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3750_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3750_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3750_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3750_VALIDATION.csv",
        "doc": DOC,
    }
    results = parse_csv(RESULTS_3749)
    caps = norm_cap_rows(timestamp, results)
    sensitivities = sensitivity_rows(timestamp, results)
    grouped = {
        "source_register": source_register(timestamp),
        "operator_audit": operator_source_audit_rows(timestamp),
        "parent_attempt": parent_parallel_attempt_rows(timestamp),
        "caps": caps,
        "sensitivity": sensitivities,
        "bound_contract": bound_contract_rows(timestamp, caps),
        "claim_gates": claim_gate_rows(timestamp, sensitivities),
        "decisions": decision_rows(timestamp, caps, sensitivities),
        "status": status_rows(timestamp, caps),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3750 validation failed: {failures}")
    print("wrote 3750 checkpoint: hidden operator cap derived; parent zero remains unsigned")


if __name__ == "__main__":
    main()
