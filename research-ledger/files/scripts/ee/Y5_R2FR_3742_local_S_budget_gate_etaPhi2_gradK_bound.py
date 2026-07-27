from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3742"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_S_BUDGET_GATE_ETAPHI2_GRADK_BOUND_3742"
DOC = ROOT / "3742-Y5-R2FR-local-S-budget-gate-etaPhi2-gradK-bound.md"

DOC_3741 = ROOT / "3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md"
NEXT_3741 = RESIDUALS / "P8_Y5_R2FR_3741_NEXT_TARGET.csv"
VALIDATION_3741 = RESIDUALS / "P8_Y5_BRR545_3741_VALIDATION.csv"
S_BUDGET_3741 = RESIDUALS / "P8_Y5_R2FR_3741_S_BUDGET_ROWS.csv"
CLAIM_GATES_3741 = RESIDUALS / "P8_Y5_R2FR_3741_CLAIM_GATES.csv"
MTS_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
MTS_GRAVITY_CORE = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md"
TIME_RELATIVITY = REPO / "core-mts-framework" / "relativity" / "time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md"


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
        ("doc_3741", DOC_3741, "eta*Phi^2", "3741 local closure hazard handoff"),
        ("next_3741", NEXT_3741, "3742-Y5-R2FR-local-S-budget-gate-etaPhi2-gradK-bound.md", "3741 next target"),
        ("validation_3741", VALIDATION_3741, "phi_gate_blocks", "3741 validation"),
        ("s_budget_3741", S_BUDGET_3741, "DANGEROUS_IF_UNBOUNDED", "3741 S-budget rows"),
        ("claim_gates_3741", CLAIM_GATES_3741, "CG3741_4_phi_term", "3741 blocking gate"),
        ("gravity_phi_def", MTS_GRAVITY, "Φ  = |∇κ|", "S-functional Phi definition"),
        ("gravity_s_formula", MTS_GRAVITY, "+ η Φ²", "S-functional eta Phi term"),
        ("gravity_flrw_zero", MTS_GRAVITY, "Φ = 0", "homogeneous branch zero condition"),
        ("gravity_ppn", MTS_GRAVITY, "𝓢 ≈ K^m", "local PPN K suppression claim"),
        ("gravity_core_phi", MTS_GRAVITY_CORE, "Φ enters directly", "morphology Phi source"),
        ("relativity_phi", TIME_RELATIVITY, "where Φ is the Newtonian gravitational potential", "Newtonian Phi definition"),
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


def symbol_disambiguation_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("SYM3742_0_Phi_S", "Phi_S", "S-functional curvature-tension/morphology proxy", "Phi_S := |nabla kappa| or related curvature-tension proxy in S(K,nablaK,Phi)", "gravity_phi_def", "must not be identified with Newtonian potential without a map"),
        ("SYM3742_1_Phi_N", "Phi_N", "Newtonian gravitational potential", "Phi_N appears in weak-field metric and Gamma_kappa=-2 Phi_N/c^2", "relativity_phi", "distinct from Phi_S unless a parent theorem maps them"),
        ("SYM3742_2_eta", "eta", "coefficient of Phi_S^2 in S", "eta is present in the S ansatz but no local numeric/source-owned value was found", "gravity_s_formula", "eta=0 or eta*Phi_S^2 bound is required for local PPN closure"),
        ("SYM3742_3_ell", "ell", "length scale multiplying gradK term", "ell appears in ell^2(nablaK)^2 but is not locally normalized in the corpus source", "gravity_s_formula", "ell/L_K ratio must be bounded"),
        ("SYM3742_4_K", "K", "Kretschmann/invariant curvature input", "K_solar scale supports K^m suppression branch", "gravity_ppn", "K term alone cannot certify full S budget"),
    ]
    return [
        {
            **base(timestamp),
            "symbol_id": symbol_id,
            "symbol": symbol,
            "meaning": meaning,
            "definition_or_status": definition_or_status,
            "source_evidence": source_evidence,
            "gate": gate,
            "claim_allowed": False,
        }
        for symbol_id, symbol, meaning, definition_or_status, source_evidence, gate in specs
    ]


def budget_bound_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "BG3742_0_K_power",
            "epsilon_K",
            "K^m/(1+K^m)",
            "epsilon_K <= K_D^m for K_D^m>=0; with K_D≈1e-61 and m>=2 gives <=1e-122 before operator constants",
            "SOURCE_BACKED_SOLAR_SCALE_PARTIAL_PASS",
            "K_solar and m>=2 source text exist; units/operator constants still open",
            True,
        ),
        (
            "BG3742_1_gradK_length",
            "epsilon_grad",
            "ell^2*(nabla K)^2/(1+K^m)",
            "if ||nabla K||_D <= K_D/L_K then epsilon_grad <= (ell/L_K)^2*K_D^2/(1+K_D^m)",
            "CONDITIONAL_LENGTH_SCALE_BOUND",
            "requires source-owned ell and local variation length L_K; likely tiny only when ell<<L_K or at least ell/L_K finite",
            False,
        ),
        (
            "BG3742_2_phi_direct",
            "epsilon_phi",
            "eta*Phi_S^2",
            "epsilon_phi <= |eta|*Phi_S,D^2; if Phi_S=|nabla kappa| and ||nabla kappa||<=kappa_D/L_kappa then <= |eta|*(kappa_D/L_kappa)^2",
            "UNRESOLVED_DOMINANT_LOCAL_GATE",
            "must prove eta=0, Phi_S=0, local projector silence, or numeric bound below PPN tolerance",
            False,
        ),
        (
            "BG3742_3_boundary",
            "epsilon_boundary",
            "local boundary/support residual",
            "epsilon_boundary <= B_boundary from domain choice and support projection",
            "BOUNDARY_GATE_OPEN",
            "must select local domain/gauge and bound support terms",
            False,
        ),
        (
            "BG3742_4_total",
            "S_epsilon",
            "total local correction budget",
            "S_epsilon = epsilon_K + epsilon_grad + epsilon_phi + epsilon_boundary",
            "ASSEMBLED_BUT_NOT_NUMERIC",
            "full local PPN closure is blocked until all four terms satisfy the target tolerance",
            False,
        ),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "budget_symbol": budget_symbol,
            "term": term,
            "bound_formula": bound_formula,
            "status": status,
            "claim_blocker": claim_blocker,
            "partial_pass": partial_pass,
            "claim_allowed": False,
        }
        for bound_id, budget_symbol, term, bound_formula, status, claim_blocker, partial_pass in specs
    ]


def zero_or_bound_conditions(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("ZB3742_0_eta_zero", "eta=0 local theorem", "epsilon_phi=0", "Would close the dangerous morphology term, but no corpus source currently proves eta=0.", "NOT_PROVED"),
        ("ZB3742_1_phi_zero", "Phi_S=0 symmetry/plateau theorem", "epsilon_phi=0", "FLRW source has Phi=0, but solar/local non-homogeneous branch does not inherit this automatically.", "NOT_PROVED_FOR_LOCAL"),
        ("ZB3742_2_projector_silence", "P_loc Phi_S=0", "epsilon_phi projected out of local PPN observables", "Viable route if the parent projector kills morphology terms in local vacuum without killing galaxy/cosmology behavior.", "OPEN_THEOREM_TARGET"),
        ("ZB3742_3_numeric_bound", "|eta| Phi_S,D^2 <= epsilon_PPN/(C_beta+C_gamma+C_N)", "epsilon_phi below PPN tolerance", "Viable empirical/phenomenological route if eta and Phi_S norms are source-owned.", "OPEN_NUMERIC_TARGET"),
        ("ZB3742_4_modify_S", "replace S ansatz by local-safe S = K^m + gradK terms only in PPN branch", "epsilon_phi removed by theory design", "This is a possible repair but must be explicit; otherwise the old S ansatz remains the blocker.", "CLOSURE_REPAIR_OPTION"),
    ]
    return [
        {
            **base(timestamp),
            "condition_id": condition_id,
            "condition": condition,
            "effect_on_phi_gate": effect_on_phi_gate,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for condition_id, condition, effect_on_phi_gate, rationale, status in specs
    ]


def ppn_tolerance_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PT3742_0_gamma", "gamma", "|gamma-1| <= C_gamma_S*S_epsilon", "need S_epsilon <= tol_gamma/C_gamma_S", "tol_gamma not sourced here; leave symbolic until PPN data gate"),
        ("PT3742_1_beta", "beta", "|beta-1| <= C_beta_S*S_epsilon", "need S_epsilon <= tol_beta/C_beta_S", "tol_beta not sourced here; leave symbolic until PPN data gate"),
        ("PT3742_2_newton", "Newton/Poisson", "|delta a|/a <= C_Newton_S*S_epsilon", "need S_epsilon <= tol_Newton/C_Newton_S", "tol_Newton not sourced here; leave symbolic until local data gate"),
        ("PT3742_3_combined", "combined local closure", "S_epsilon <= min(tol_gamma/C_gamma_S, tol_beta/C_beta_S, tol_Newton/C_Newton_S)", "single acceptance gate for calibrated-GR closure branch", "symbolic acceptance gate ready"),
    ]
    return [
        {
            **base(timestamp),
            "tolerance_id": tolerance_id,
            "observable": observable,
            "residual_formula": residual_formula,
            "required_budget": required_budget,
            "status": status,
            "claim_allowed": False,
        }
        for tolerance_id, observable, residual_formula, required_budget, status in specs
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("THM3742_0_symbol_split", "SYMBOL_COLLISION_RESOLVED", "The S-functional Phi must be treated as Phi_S, distinct from Newtonian Phi_N, until a parent map is proved.", "This blocks a common false local-GR shortcut."),
        ("THM3742_1_grad_bound", "DERIVED_CONDITIONAL_BOUND", "If ||nabla K||<=K_D/L_K, then the gradK term is bounded by (ell/L_K)^2 K_D^2/(1+K_D^m).", "This makes gradK a length-scale gate, not vague doom."),
        ("THM3742_2_phi_gate", "DOMINANT_OPEN_GATE", "The eta Phi_S^2 term is the dominant unresolved local closure blocker because it is not automatically suppressed by K^m.", "The K_solar argument is not enough by itself."),
        ("THM3742_3_demotion", "OVERBROAD_CLOSURE_DEMOTED", "The statement 'local PPN passes because S≈K^m' is demoted to 'local PPN is conditionally safe if the full S_epsilon budget is below tolerance'.", "This is a correction, not a retreat."),
        ("THM3742_4_claim_gate", "ANTI_OVERCLAIM", "No local-GR/Newton/PPN pass is claimable until eta Phi_S^2, gradK, boundary, and operator constants are closed.", "Keeps the route serious."),
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
        ("CG3742_0_sources", "S-budget source evidence registered", True, "gravity and relativity source rows found"),
        ("CG3742_1_symbol_split", "Phi_S/Phi_N symbol split enforced", True, "symbol-disambiguation rows emitted"),
        ("CG3742_2_K_term", "K^m solar-scale suppression partially source-backed", True, "K_solar and m>=2 branch recorded"),
        ("CG3742_3_gradK", "gradK bounded by source-owned ell/L_K", False, "formula derived but ell and L_K not source-owned"),
        ("CG3742_4_phi", "eta*Phi_S^2 killed or bounded", False, "no eta=0, Phi_S=0, projector silence, or numeric bound proved"),
        ("CG3742_5_boundary", "boundary/support residual bounded", False, "domain/gauge boundary still open"),
        ("CG3742_6_tolerance", "S_epsilon below PPN/Newton tolerance", False, "tolerances/operator constants remain symbolic"),
        ("CG3742_7_local_claim", "local GR/Newton/PPN pass claim allowed", False, "full S budget not closed"),
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
        ("DEC3742_0_progress", "FULL_S_BUDGET_GATE_FORMALIZED", "The local closure branch now has explicit K, gradK, Phi_S, and boundary budget terms."),
        ("DEC3742_1_demote", "OVERBROAD_KM_LOCAL_PASS_DEMOTED", "The old shorthand S≈K^m is not valid unless gradK and Phi_S terms vanish or are bounded."),
        ("DEC3742_2_best_route", "BEST_NEXT_ROUTE_PROJECTOR_OR_ETA_ZERO", "The least-circular next leap is to derive P_loc Phi_S=0 or eta=0 in local weak-field/vacuum, rather than fitting eta small."),
        ("DEC3742_3_fallback", "FALLBACK_MODIFY_S_FUNCTIONAL", "If the Phi_S gate cannot be derived, the local closure branch needs an explicitly local-safe S functional or remains closure-only."),
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
        "status_id": "STATUS3742_0",
        "status": "FULL_S_BUDGET_GATE_FORMALIZED_PHI_AND_GRADK_OPEN",
        "summary": "3742 formalizes the full local S_epsilon budget and demotes the overbroad S≈K^m local pass; K^m is tiny, gradK is conditionally length-scale bounded, and eta*Phi_S^2 remains the dominant open gate.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3742_0",
        "target_doc": "3743-Y5-R2FR-local-PhiS-projector-or-eta-zero-theorem.md",
        "target_script": "scripts/Y5_R2FR_3743_local_PhiS_projector_or_eta_zero_theorem.py",
        "objective": "try to prove P_loc Phi_S=0 or eta=0 for the local weak-field/vacuum branch; if not, declare the current S functional local-PPN unsafe without an added projector/modification",
        "success_gate": "eta*Phi_S^2 is either theorem-killed, bounded below symbolic PPN tolerance, or explicitly marked as requiring a modified local-safe S functional",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3742 - Local S-Budget Gate: eta Phi_S^2 and gradK Bound",
        "",
        "## Status",
        "- `FULL_S_BUDGET_GATE_FORMALIZED_PHI_AND_GRADK_OPEN`",
        "- The overbroad shorthand `S ≈ K^m` is demoted: the local branch only survives if the full `S_epsilon` budget is small.",
        "- `Phi_S` in the `S` functional is not automatically Newtonian `Phi_N`; the symbol collision is now an explicit gate.",
        "",
        "## Symbol Disambiguation",
    ]
    for row in grouped["symbols"]:
        lines.append(f"- `{row['symbol']}`: {row['definition_or_status']} | gate: {row['gate']}")
    lines.extend(["", "## Budget Bounds"])
    for row in grouped["budget_bounds"]:
        lines.append(f"- `{row['budget_symbol']}` `{row['status']}`: {row['bound_formula']} | blocker: {row['claim_blocker']}")
    lines.extend(["", "## Phi_S Zero-or-Bound Routes"])
    for row in grouped["zero_or_bound"]:
        lines.append(f"- `{row['condition_id']}` `{row['status']}`: {row['condition']} -> {row['effect_on_phi_gate']} | {row['rationale']}")
    lines.extend(["", "## PPN Acceptance Gate"])
    for row in grouped["ppn_tolerances"]:
        lines.append(f"- `{row['observable']}`: {row['required_budget']} | {row['status']}")
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
    symbols = parse_csv(paths["symbols"])
    budget_bounds = parse_csv(paths["budget_bounds"])
    zero_or_bound = parse_csv(paths["zero_or_bound"])
    ppn_tolerances = parse_csv(paths["ppn_tolerances"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3742*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("symbol_split", "Phi_S/Phi_N split recorded", len(symbols) == 5 and all(token in read_text(paths["symbols"]) for token in ["Phi_S", "Phi_N", "eta"])),
        ("budget_bounds", "five budget bounds present", len(budget_bounds) == 5 and all(token in read_text(paths["budget_bounds"]) for token in ["epsilon_K", "epsilon_grad", "epsilon_phi", "S_epsilon"])),
        ("zero_or_bound", "Phi zero-or-bound routes present", len(zero_or_bound) == 5 and any(row["status"] == "OPEN_THEOREM_TARGET" for row in zero_or_bound)),
        ("ppn_tolerance_gate", "symbolic PPN tolerance gate present", len(ppn_tolerances) == 4 and "min(tol_gamma" in read_text(paths["ppn_tolerances"])),
        ("phi_gate_blocks", "eta Phi gate blocks claim", any(row["gate_id"] == "CG3742_4_phi" and row["passed"] == "False" for row in claim_gates)),
        ("demotion_recorded", "overbroad K^m pass demoted", "OVERBROAD_KM_LOCAL_PASS_DEMOTED" in read_text(paths["decisions"]) and "OVERBROAD_CLOSURE_DEMOTED" in read_text(paths["theorems"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3743", "next target is Phi_S projector/eta theorem", next_target[0]["target_doc"] == "3743-Y5-R2FR-local-PhiS-projector-or-eta-zero-theorem.md"),
        ("doc_core_terms", "doc contains S budget and symbol collision", all(token in read_text(paths["doc"]) for token in ["Phi_S", "Phi_N", "S_epsilon", "eta*Phi_S^2", "demoted"])),
        ("no_formalization_leak", "no 3742 files in formalization-workbench", len(formalization_leaks) == 0),
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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3742_SOURCE_REGISTER.csv",
        "symbols": RESIDUALS / "P8_Y5_R2FR_3742_SYMBOL_DISAMBIGUATION_ROWS.csv",
        "budget_bounds": RESIDUALS / "P8_Y5_R2FR_3742_BUDGET_BOUND_ROWS.csv",
        "zero_or_bound": RESIDUALS / "P8_Y5_R2FR_3742_PhiS_ZERO_OR_BOUND_CONDITIONS.csv",
        "ppn_tolerances": RESIDUALS / "P8_Y5_R2FR_3742_PPN_TOLERANCE_GATE_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3742_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3742_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3742_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3742_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3742_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3742_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "symbols": symbol_disambiguation_rows(timestamp),
        "budget_bounds": budget_bound_rows(timestamp),
        "zero_or_bound": zero_or_bound_conditions(timestamp),
        "ppn_tolerances": ppn_tolerance_rows(timestamp),
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
        raise SystemExit(f"3742 validation failed: {failures}")
    print("wrote 3742 checkpoint: full S budget gate formalized; Phi_S and gradK remain open")


if __name__ == "__main__":
    main()
