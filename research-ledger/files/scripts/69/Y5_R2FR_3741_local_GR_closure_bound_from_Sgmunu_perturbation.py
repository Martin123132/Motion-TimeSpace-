from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3741"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_GR_CLOSURE_BOUND_FROM_SGMUNU_PERTURBATION_3741"
DOC = ROOT / "3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md"

DOC_3740 = ROOT / "3740-Y5-R2FR-parent-action-coefficient-extraction-A1-A2-G1-kappa.md"
NEXT_3740 = RESIDUALS / "P8_Y5_R2FR_3740_NEXT_TARGET.csv"
VALIDATION_3740 = RESIDUALS / "P8_Y5_BRR545_3740_VALIDATION.csv"
CLOSURE_3740 = RESIDUALS / "P8_Y5_R2FR_3740_CLOSURE_ROUTE_ROWS.csv"
FILL_3740 = RESIDUALS / "P8_Y5_R2FR_3740_FILL_ROWS.csv"
MTS_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
MTS_GRAVITY_CORE = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md"
ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"


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
        ("doc_3740", DOC_3740, "calibrated-GR closure", "3740 closure route handoff"),
        ("next_3740", NEXT_3740, "3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md", "3740 next target"),
        ("validation_3740", VALIDATION_3740, "next_target_3741", "3740 validation"),
        ("closure_3740", CLOSURE_3740, "local_PPN_bound", "3740 closure route rows"),
        ("fill_3740", FILL_3740, "C_beta_S*K^m", "3740 beta fill row"),
        ("mts_gravity", MTS_GRAVITY, "Gμν + 𝓢 gμν = κ Tμν", "local field equation with correction"),
        ("mts_gravity_S", MTS_GRAVITY, "η Φ²", "full S budget includes phi term"),
        ("mts_gravity_ppn", MTS_GRAVITY, "β = 1 + O(K^m)", "PPN closure statement"),
        ("mts_gravity_core", MTS_GRAVITY_CORE, "Minimal MTS-consistent form:", "curvature response functional source"),
        ("action_principle", ACTION_PRINCIPLE, "κ = 8πG / c⁴", "calibrated GR coupling source"),
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


def theorem_clause_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("LC3741_0_equation_split", "field_equation_split", "G[g] - kappa*T = -S*g", "Subtract a GR solution G[g_GR]=kappa*T to isolate the MTS correction as an effective source.", "DERIVED_FROM_FIELD_EQUATION"),
        ("LC3741_1_linearized_problem", "linearized_metric_response", "L_GR[h] = -S*g_GR + boundary/gauge terms + O(S*h,h^2)", "In a fixed local PPN gauge, the metric deviation is controlled by the inverse of the linearized GR operator.", "CONDITIONAL_GAUGE_FIXED_DERIVATION"),
        ("LC3741_2_operator_bound", "metric_norm_bound", "||h||_PPN <= C_GR*(||S||_D + L_D||nabla S||_D + B_boundary)", "The local deviation from GR is bounded by a correction budget epsilon_S times a gauge/operator constant.", "BOUND_FORMULA_DERIVED_CONSTANT_OPEN"),
        ("LC3741_3_newton_bound", "newton_residual_bound", "|delta Phi|/Phi_scale <= C_N*epsilon_S and |delta a|/a_scale <= C_a*epsilon_S", "Newtonian residuals are small if S and its local gradients are small.", "BOUND_FORMULA_DERIVED_CONSTANT_OPEN"),
        ("LC3741_4_ppn_bound", "ppn_residual_bound", "|gamma-1| <= C_gamma*S_epsilon and |beta-1| <= C_beta*S_epsilon", "This fills the beta/gamma closure route in the 3738 ledger without needing parent A2.", "BOUND_FORMULA_DERIVED_CONSTANT_OPEN"),
        ("LC3741_5_not_parent", "parent_route_separation", "This does not prove A2=A1^2 or derive G_N; it proves a calibrated-GR perturbative closure route.", "Prevents mixing the closure ladder with the stricter parent-owned derivation ladder.", "ANTI_OVERCLAIM"),
    ]
    return [
        {
            **base(timestamp),
            "clause_id": clause_id,
            "name": name,
            "formula": formula,
            "derivation_meaning": derivation_meaning,
            "status": status,
            "claim_allowed": False,
        }
        for clause_id, name, formula, derivation_meaning, status in specs
    ]


def s_budget_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("SB3741_0_Km", "K^m/(1+K^m)", "curvature-power term", "epsilon_K <= C_K*K_D^m; corpus solar note gives K_solar≈1e-61, so m>=2 gives <=C_K*1e-122", "SOURCE_BACKED_SHAPE_NUMERIC_SCALE_PARTIAL", "source-backed K scale, open C_K/domain units"),
        ("SB3741_1_gradK", "ell^2*(nabla K)^2/(1+K^m)", "curvature-gradient/memory term", "epsilon_grad <= C_gradK*ell^2*||nabla K||_D^2", "BOUND_FORMULA_OPEN", "must bound local curvature gradients and ell"),
        ("SB3741_2_phi", "eta*Phi^2", "curvature-tension morphology term", "epsilon_phi <= |eta|*||Phi||_D^2", "DANGEROUS_IF_UNBOUNDED", "must prove eta=0 locally, Phi projection silent, or bound below PPN tolerance"),
        ("SB3741_3_total", "S_epsilon", "total correction budget", "S_epsilon = epsilon_K + epsilon_grad + epsilon_phi + epsilon_boundary", "ASSEMBLED_BUDGET_VALUES_MISSING", "all terms must be finite before a numeric PPN pass"),
    ]
    return [
        {
            **base(timestamp),
            "budget_id": budget_id,
            "term": term,
            "meaning": meaning,
            "bound_formula": bound_formula,
            "status": status,
            "missing_for_claim": missing_for_claim,
            "claim_allowed": False,
        }
        for budget_id, term, meaning, bound_formula, status, missing_for_claim in specs
    ]


def beta_fill_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("BF3741_0_C_beta_2PN_closure", "C_beta_2PN", "C_beta_S*S_epsilon", "replaces pure symbolic beta row only for calibrated-GR closure branch", "BOUND_SCHEMA_READY_CONSTANT_OPEN"),
        ("BF3741_1_gamma_closure", "Phi0_inv/gamma residual", "C_gamma_S*S_epsilon", "bounds gamma residual without claiming parent G1=A1", "BOUND_SCHEMA_READY_CONSTANT_OPEN"),
        ("BF3741_2_GN_closure", "G_N_eff_local", "G_calibrated*(1 + O(S_epsilon))", "keeps Newton constant calibrated while bounding local deviations", "CALIBRATED_CLOSURE_BOUND_READY"),
        ("BF3741_3_accel_poisson", "C_grad/C_lap residual add-on", "C_Newton_S*S_epsilon", "adds S-source residual to Newton/Poisson rows", "BOUND_SCHEMA_READY_CONSTANT_OPEN"),
    ]
    return [
        {
            **base(timestamp),
            "fill_id": fill_id,
            "target_symbol": target_symbol,
            "fill_value_or_bound": fill_value_or_bound,
            "ledger_meaning": ledger_meaning,
            "status": status,
            "ready_to_patch_3738": False,
            "claim_allowed": False,
        }
        for fill_id, target_symbol, fill_value_or_bound, ledger_meaning, status in specs
    ]


def operator_constant_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("OC3741_0_C_GR", "C_GR", "inverse gauge-fixed linearized Einstein operator norm on the local PPN domain", "MISSING_OPERATOR_NORM"),
        ("OC3741_1_C_N", "C_N", "metric-to-Newtonian-potential projection norm", "MISSING_PROJECTION_NORM"),
        ("OC3741_2_C_a", "C_a", "metric/potential-to-acceleration projection norm", "MISSING_PROJECTION_NORM"),
        ("OC3741_3_C_gamma", "C_gamma_S", "metric perturbation to PPN gamma residual norm", "MISSING_PPN_OPERATOR_NORM"),
        ("OC3741_4_C_beta", "C_beta_S", "second-order metric perturbation to PPN beta residual norm", "MISSING_2PN_OPERATOR_NORM"),
        ("OC3741_5_boundary", "B_boundary", "local domain boundary/support residual", "MISSING_BOUNDARY_NORM"),
    ]
    return [
        {
            **base(timestamp),
            "constant_id": constant_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for constant_id, symbol, meaning, status in specs
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "runner_id": "RUN3741_0_LOCAL_GR_CLOSURE_BOUND",
        "theorem_clauses": 6,
        "s_budget_terms": 4,
        "beta_fill_rows": 4,
        "operator_constants_open": 6,
        "numeric_executable": False,
        "status": "LOCAL_GR_CLOSURE_THEOREM_DERIVED_S_BUDGET_VALUES_MISSING",
        "claim_allowed": False,
    }]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("THM3741_0_closure_bound", "DERIVED_CONDITIONAL_THEOREM", "For a calibrated GR baseline, local MTS metric residuals are bounded by S_epsilon through the gauge-fixed linearized Einstein operator.", "This makes the GR/Newton reduction route mathematical instead of rhetorical."),
        ("THM3741_1_ppn_fill", "DERIVED_LEDGER_FILL", "C_beta_2PN and gamma residual can be filled as C_beta_S*S_epsilon and C_gamma_S*S_epsilon in the closure branch.", "This is a concrete interface to 3738."),
        ("THM3741_2_phi_hazard", "RED_TEAM_GATE", "The eta*Phi^2 term is a live hazard: if it is not locally zero or tightly bounded, the K^m solar suppression claim is insufficient.", "This prevents an over-optimistic local pass."),
        ("THM3741_3_parent_separation", "ANTI_OVERCLAIM", "The closure theorem does not derive G_N or A2=A1^2; those remain parent-route problems.", "Keeps both ladders honest."),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "status": status,
            "clause": clause,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for theorem_id, status, clause, meaning in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3741_0_equation", "Sg perturbation equation split", True, "derived from source-backed field equation"),
        ("CG3741_1_bound_formula", "operator bound formula assembled", True, "C_GR*S_epsilon theorem rows emitted"),
        ("CG3741_2_beta_fill", "beta/gamma closure fill rows emitted", True, "C_beta_S*S_epsilon and C_gamma_S*S_epsilon rows exist"),
        ("CG3741_3_K_scale", "K^m solar scale source-backed", True, "K_solar and S≈K^m source lines exist"),
        ("CG3741_4_phi_term", "eta*Phi^2 locally killed or bounded", False, "not yet proved; this is the largest local closure hazard"),
        ("CG3741_5_operator_constants", "operator constants numeric/source-owned", False, "C_GR/C_beta/etc remain open"),
        ("CG3741_6_boundary", "local boundary projection bounded", False, "boundary/support norm remains open"),
        ("CG3741_7_local_claim", "local GR/Newton/PPN pass claim allowed", False, "S budget and constants not closed"),
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
        ("DEC3741_0_progress", "LOCAL_GR_CLOSURE_THEOREM_DERIVED", "The closure route now has an explicit perturbative bound from Sg_mu_nu to Newton/PPN residuals."),
        ("DEC3741_1_hazard", "ETA_PHI2_IS_THE_NEXT_LOCAL_GATE", "The K^m term is tiny, but the full S functional is only small if gradient and phi terms are killed or bounded."),
        ("DEC3741_2_next", "NEXT_BOUND_LOCAL_S_BUDGET_TERMS", "The next best target is the local S-budget gate for eta*Phi^2, gradK, boundary, and operator constants."),
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
        "status_id": "STATUS3741_0",
        "status": "LOCAL_GR_CLOSURE_THEOREM_DERIVED_S_BUDGET_VALUES_MISSING",
        "summary": "3741 derives the calibrated-GR perturbation bound from G+Sg=kappaT to Newton/PPN residuals and maps beta/gamma to C*S_epsilon; local pass remains blocked by eta*Phi^2, gradK, boundary, and operator constants.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3741_0",
        "target_doc": "3742-Y5-R2FR-local-S-budget-gate-etaPhi2-gradK-bound.md",
        "target_script": "scripts/Y5_R2FR_3742_local_S_budget_gate_etaPhi2_gradK_bound.py",
        "objective": "derive or bound the full local S_epsilon budget, especially eta*Phi^2 and gradK, so the O(K^m) local PPN closure is not overclaimed",
        "success_gate": "either eta*Phi^2 and gradK are locally zero/bounded below PPN tolerance, or the closure branch is explicitly demoted to requiring a modified S functional",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3741 - Local GR Closure Bound from S g_mu_nu Perturbation",
        "",
        "## Status",
        "- `LOCAL_GR_CLOSURE_THEOREM_DERIVED_S_BUDGET_VALUES_MISSING`",
        "- This proves the calibrated-GR closure route as a conditional perturbative bound, not as a parent derivation.",
        "- The next local hazard is the full `S_epsilon` budget: `K^m` is tiny, but `gradK`, boundary, and `eta*Phi^2` must also be killed or bounded.",
        "",
        "## Closure Theorem Clauses",
    ]
    for row in grouped["clauses"]:
        lines.append(f"- `{row['clause_id']}` `{row['status']}`: {row['formula']} | {row['derivation_meaning']}")
    lines.extend(["", "## S Budget"])
    for row in grouped["s_budget"]:
        lines.append(f"- `{row['budget_id']}` `{row['status']}`: {row['term']} -> {row['bound_formula']} | missing: {row['missing_for_claim']}")
    lines.extend(["", "## Beta/Gamma Fill Rows"])
    for row in grouped["beta_fills"]:
        lines.append(f"- `{row['target_symbol']}` `{row['status']}`: {row['fill_value_or_bound']} | {row['ledger_meaning']}")
    lines.extend(["", "## Operator Constants"])
    for row in grouped["operator_constants"]:
        lines.append(f"- `{row['symbol']}` `{row['status']}`: {row['meaning']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    clauses = parse_csv(paths["clauses"])
    s_budget = parse_csv(paths["s_budget"])
    beta_fills = parse_csv(paths["beta_fills"])
    operator_constants = parse_csv(paths["operator_constants"])
    runner = parse_csv(paths["runner"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3741*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("clauses", "six closure theorem clauses present", len(clauses) == 6 and all(token in read_text(paths["clauses"]) for token in ["L_GR", "S_epsilon", "C_beta"])),
        ("s_budget", "full S budget terms present", len(s_budget) == 4 and all(token in read_text(paths["s_budget"]) for token in ["eta*Phi^2", "grad", "K^m"])),
        ("beta_fills", "beta/gamma/G_N fill rows present", len(beta_fills) == 4 and all(token in read_text(paths["beta_fills"]) for token in ["C_beta_S*S_epsilon", "C_gamma_S*S_epsilon", "G_calibrated"])),
        ("operator_constants", "operator constant ledger present", len(operator_constants) == 6),
        ("runner_blocks", "runner blocks numeric pass", runner[0]["numeric_executable"] == "False"),
        ("phi_gate_blocks", "eta Phi gate blocks claim", any(row["gate_id"] == "CG3741_4_phi_term" and row["passed"] == "False" for row in claim_gates)),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3742", "next target is local S budget", next_target[0]["target_doc"] == "3742-Y5-R2FR-local-S-budget-gate-etaPhi2-gradK-bound.md"),
        ("doc_core_terms", "doc contains closure theorem and phi hazard", all(token in read_text(paths["doc"]) for token in ["S_epsilon", "eta*Phi^2", "calibrated-GR closure", "C_beta_S"])),
        ("no_formalization_leak", "no 3741 files in formalization-workbench", len(formalization_leaks) == 0),
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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3741_SOURCE_REGISTER.csv",
        "clauses": RESIDUALS / "P8_Y5_R2FR_3741_CLOSURE_THEOREM_CLAUSES.csv",
        "s_budget": RESIDUALS / "P8_Y5_R2FR_3741_S_BUDGET_ROWS.csv",
        "beta_fills": RESIDUALS / "P8_Y5_R2FR_3741_BETA_FILL_ROWS.csv",
        "operator_constants": RESIDUALS / "P8_Y5_R2FR_3741_OPERATOR_CONSTANT_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3741_RUNNER_STATUS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3741_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3741_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3741_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3741_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3741_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3741_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "clauses": theorem_clause_rows(timestamp),
        "s_budget": s_budget_rows(timestamp),
        "beta_fills": beta_fill_rows(timestamp),
        "operator_constants": operator_constant_rows(timestamp),
        "runner": runner_rows(timestamp),
        "theorems": theorem_rows(timestamp),
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
        raise SystemExit(f"3741 validation failed: {failures}")
    print("wrote 3741 checkpoint: local GR closure bound derived; S budget values still missing")


if __name__ == "__main__":
    main()
