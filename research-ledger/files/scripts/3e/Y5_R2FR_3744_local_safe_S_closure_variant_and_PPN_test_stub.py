from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3744"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_SAFE_S_CLOSURE_VARIANT_AND_PPN_STUB_3744"
DOC = ROOT / "3744-Y5-R2FR-local-safe-S-closure-variant-and-PPN-test-stub.md"

DOC_3741 = ROOT / "3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md"
DOC_3742 = ROOT / "3742-Y5-R2FR-local-S-budget-gate-etaPhi2-gradK-bound.md"
DOC_3743 = ROOT / "3743-Y5-R2FR-local-PhiS-projector-or-eta-zero-theorem.md"
VALIDATION_3743 = RESIDUALS / "P8_Y5_BRR545_3743_VALIDATION.csv"
LOCAL_SAFE_3743 = RESIDUALS / "P8_Y5_R2FR_3743_LOCAL_SAFE_S_OPTIONS.csv"
CLAIM_GATES_3743 = RESIDUALS / "P8_Y5_R2FR_3743_CLAIM_GATES.csv"
PPN_TOLERANCE_3742 = RESIDUALS / "P8_Y5_R2FR_3742_PPN_TOLERANCE_GATE_ROWS.csv"
CG_1029 = ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md"


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


def as_float(value: object) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3741_ppn_bound", DOC_3741, "|gamma-1| <= C_gamma*S_epsilon", "closure theorem PPN residual interface"),
        ("doc_3741_operator_constants", DOC_3741, "C_gamma_S", "operator norms remain open inputs"),
        ("doc_3742_budget", DOC_3742, "S_epsilon = epsilon_K + epsilon_grad + epsilon_phi + epsilon_boundary", "full local budget"),
        ("doc_3742_phi_split", DOC_3742, "`Phi_S`: Phi_S :=", "Phi_S/Phi_N symbol split"),
        ("doc_3742_tolerance", DOC_3742, "need S_epsilon <= tol_gamma/C_gamma_S", "symbolic PPN tolerance gate"),
        ("doc_3743_status", DOC_3743, "RAW_S_LOCAL_PPN_UNSAFE_REPAIR_CONTRACT_REQUIRED", "3743 handoff status"),
        ("local_safe_3743_projector", LOCAL_SAFE_3743, "P_loc P_nonloc=0", "projected local-safe closure option"),
        ("claim_gates_3743_block", CLAIM_GATES_3743, "CG3743_6_local_claim", "local claim remains blocked"),
        ("ppn_tolerance_3742_combined", PPN_TOLERANCE_3742, "PT3742_3_combined", "machine-readable symbolic tolerance gate"),
        ("cg_1029_ppn_placeholders", CG_1029, "2.3e-05", "older nonclaim PPN threshold placeholder reference"),
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


def closure_variant_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "LS3744_0_raw_S",
            "raw current S",
            "S_eff = epsilon_K + epsilon_grad + epsilon_phi_raw + epsilon_boundary",
            "epsilon_phi_raw = |eta| Phi_S,D^2",
            "unsafe control: requires eta/Phi_S numeric source or theorem zero",
            "LOCAL_PPN_UNSAFE_RETAINS_3743_DEMOTION",
            "This is carried only as a blocked baseline.",
        ),
        (
            "LS3744_1_projected_S",
            "projected local-safe closure",
            "S_eff = epsilon_K + epsilon_grad + sigma_phi_local*epsilon_phi_raw + epsilon_boundary",
            "sigma_phi_local = ||P_loc Phi_S||_D^2 / ||Phi_S||_D^2",
            "requires parent-derived sigma_phi_local=0 or source-backed sigma_phi_local bound",
            "PREFERRED_REPAIR_CANDIDATE_NONCLAIM",
            "This is the cleanest repair because it quarantines morphology locally without deleting it globally.",
        ),
        (
            "LS3744_2_eta_zero_S",
            "eta-zero local closure",
            "S_eff = epsilon_K + epsilon_grad + epsilon_boundary",
            "eta_local = 0 by parent theorem or explicit closure clause",
            "requires eta_local zero theorem/source path",
            "SECOND_REPAIR_CANDIDATE_NONCLAIM",
            "This is simpler but more fragile because it risks looking like term deletion unless parent-signed.",
        ),
        (
            "LS3744_3_numeric_bound_S",
            "numeric-bound raw closure",
            "S_eff = epsilon_K + epsilon_grad + epsilon_phi_raw + epsilon_boundary",
            "epsilon_phi_raw supplied from source-owned eta and Phi_S norm",
            "requires eta, Phi_S norm, operator constants, and tolerances",
            "EMPIRICAL_REPAIR_CANDIDATE_NONCLAIM",
            "This is a useful fallback once real local profiles exist.",
        ),
    ]
    return [
        {
            **base(timestamp),
            "variant_id": variant_id,
            "route": route,
            "formula": formula,
            "phi_handling": phi_handling,
            "required_inputs": required_inputs,
            "status": status,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for variant_id, route, formula, phi_handling, required_inputs, status, meaning in specs
    ]


def input_template_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "input_id": "TPL3744_0_fill_for_real_run",
            "variant_id": "LS3744_1_projected_S|LS3744_2_eta_zero_S|LS3744_3_numeric_bound_S",
            "epsilon_K": "MISSING_K_POWER_BUDGET",
            "epsilon_grad": "MISSING_GRADK_BUDGET",
            "epsilon_phi_raw": "MISSING_ETA_PHIS_BUDGET_OR_ZERO",
            "sigma_phi_local": "MISSING_PROJECTOR_KERNEL_OR_BOUND",
            "epsilon_boundary": "MISSING_BOUNDARY_BUDGET",
            "C_gamma_S": "MISSING_PPN_OPERATOR_NORM",
            "C_beta_S": "MISSING_2PN_OPERATOR_NORM",
            "C_Newton_S": "MISSING_NEWTON_OPERATOR_NORM",
            "tol_gamma": "MISSING_SOURCE_TOL_GAMMA",
            "tol_beta": "MISSING_SOURCE_TOL_BETA",
            "tol_Newton": "MISSING_SOURCE_TOL_NEWTON",
            "source_paths": "MISSING_PARENT_AND_DATA_SOURCES",
            "claim_allowed": False,
        }
    ]


def dry_run_input_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DRY3744_0_raw_hazard", "LS3744_0_raw_S", 1e-20, 1e-20, 1e-3, 1.0, 0.0, 1.0, 1.0, 1.0, 2.3e-5, 7.8e-5, 1e-5, False, False, False, "demo only: shows raw Phi_S term can dominate"),
        ("DRY3744_1_projected_zero", "LS3744_1_projected_S", 1e-20, 1e-20, 1e-3, 0.0, 0.0, 1.0, 1.0, 1.0, 2.3e-5, 7.8e-5, 1e-5, False, False, False, "demo only: shows a true projector zero would pass the arithmetic"),
        ("DRY3744_2_eta_zero", "LS3744_2_eta_zero_S", 1e-20, 1e-20, 1e-3, 1.0, 0.0, 1.0, 1.0, 1.0, 2.3e-5, 7.8e-5, 1e-5, False, False, False, "demo only: eta-zero arithmetic without source cannot claim"),
        ("DRY3744_3_numeric_bound", "LS3744_3_numeric_bound_S", 1e-20, 1e-20, 1e-8, 1.0, 0.0, 1.0, 1.0, 1.0, 2.3e-5, 7.8e-5, 1e-5, False, False, False, "demo only: small sourced epsilon_phi would pass, but this row is not sourced"),
    ]
    return [
        {
            **base(timestamp),
            "input_id": input_id,
            "variant_id": variant_id,
            "epsilon_K": epsilon_K,
            "epsilon_grad": epsilon_grad,
            "epsilon_phi_raw": epsilon_phi_raw,
            "sigma_phi_local": sigma_phi_local,
            "epsilon_boundary": epsilon_boundary,
            "C_gamma_S": C_gamma_S,
            "C_beta_S": C_beta_S,
            "C_Newton_S": C_Newton_S,
            "tol_gamma": tol_gamma,
            "tol_beta": tol_beta,
            "tol_Newton": tol_Newton,
            "has_parent_projector_source": has_parent_projector_source,
            "has_eta_zero_source": has_eta_zero_source,
            "has_numeric_phi_source": has_numeric_phi_source,
            "source_paths": "DEMO_NONCLAIM",
            "notes": notes,
            "claim_allowed": False,
        }
        for (
            input_id,
            variant_id,
            epsilon_K,
            epsilon_grad,
            epsilon_phi_raw,
            sigma_phi_local,
            epsilon_boundary,
            C_gamma_S,
            C_beta_S,
            C_Newton_S,
            tol_gamma,
            tol_beta,
            tol_Newton,
            has_parent_projector_source,
            has_eta_zero_source,
            has_numeric_phi_source,
            notes,
        ) in specs
    ]


def effective_phi(row: dict[str, object]) -> tuple[float | None, str]:
    epsilon_phi_raw = as_float(row.get("epsilon_phi_raw"))
    sigma_phi_local = as_float(row.get("sigma_phi_local"))
    variant_id = str(row.get("variant_id", ""))
    if epsilon_phi_raw is None:
        return None, "missing epsilon_phi_raw"
    if variant_id == "LS3744_1_projected_S":
        if sigma_phi_local is None:
            return None, "missing sigma_phi_local"
        return sigma_phi_local * epsilon_phi_raw, "projected_phi = sigma_phi_local*epsilon_phi_raw"
    if variant_id == "LS3744_2_eta_zero_S":
        return 0.0, "eta_zero_closure_phi = 0"
    return epsilon_phi_raw, "raw_or_numeric_phi retained"


def evaluate_input(row: dict[str, object], timestamp: str) -> dict[str, object]:
    numbers = {
        key: as_float(row.get(key))
        for key in [
            "epsilon_K",
            "epsilon_grad",
            "epsilon_boundary",
            "C_gamma_S",
            "C_beta_S",
            "C_Newton_S",
            "tol_gamma",
            "tol_beta",
            "tol_Newton",
        ]
    }
    phi_value, phi_rule = effective_phi(row)
    missing = [key for key, value in numbers.items() if value is None]
    if phi_value is None:
        missing.append("effective_phi")
    if missing:
        return {
            **base(timestamp),
            "result_id": str(row["input_id"]).replace("DRY", "RES"),
            "input_id": row["input_id"],
            "variant_id": row["variant_id"],
            "S_eff": "MISSING_INPUT",
            "gamma_residual_bound": "MISSING_INPUT",
            "beta_residual_bound": "MISSING_INPUT",
            "newton_residual_bound": "MISSING_INPUT",
            "numeric_pass": False,
            "claim_allowed": False,
            "failure_mode": ";".join(missing),
            "phi_rule": phi_rule,
        }
    S_eff = numbers["epsilon_K"] + numbers["epsilon_grad"] + phi_value + numbers["epsilon_boundary"]
    gamma_residual = numbers["C_gamma_S"] * S_eff
    beta_residual = numbers["C_beta_S"] * S_eff
    newton_residual = numbers["C_Newton_S"] * S_eff
    numeric_pass = (
        gamma_residual <= numbers["tol_gamma"]
        and beta_residual <= numbers["tol_beta"]
        and newton_residual <= numbers["tol_Newton"]
    )
    row_valid = str(row.get("valid_for_claim", "False")) == "True"
    claim_allowed = False
    if row["variant_id"] == "LS3744_1_projected_S":
        claim_allowed = numeric_pass and row_valid and str(row.get("has_parent_projector_source")) == "True"
    elif row["variant_id"] == "LS3744_2_eta_zero_S":
        claim_allowed = numeric_pass and row_valid and str(row.get("has_eta_zero_source")) == "True"
    elif row["variant_id"] == "LS3744_3_numeric_bound_S":
        claim_allowed = numeric_pass and row_valid and str(row.get("has_numeric_phi_source")) == "True"
    return {
        **base(timestamp),
        "result_id": str(row["input_id"]).replace("DRY", "RES"),
        "input_id": row["input_id"],
        "variant_id": row["variant_id"],
        "S_eff": f"{S_eff:.12e}",
        "gamma_residual_bound": f"{gamma_residual:.12e}",
        "beta_residual_bound": f"{beta_residual:.12e}",
        "newton_residual_bound": f"{newton_residual:.12e}",
        "numeric_pass": numeric_pass,
        "claim_allowed": claim_allowed,
        "failure_mode": "none_numeric_only" if numeric_pass else "exceeds_tolerance",
        "phi_rule": phi_rule,
    }


def dry_run_result_rows(timestamp: str, inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    return [evaluate_input(row, timestamp) for row in inputs]


def claim_gate_rows(timestamp: str, results: list[dict[str, object]]) -> list[dict[str, object]]:
    raw_blocked = any(row["variant_id"] == "LS3744_0_raw_S" and row["numeric_pass"] is False for row in results)
    repair_numeric_passes = [row for row in results if row["variant_id"] != "LS3744_0_raw_S" and row["numeric_pass"] is True]
    specs = [
        ("CG3744_0_sources", "3741-3743 handoff sources registered", True, "source needles found for budget, tolerance, and repair contract"),
        ("CG3744_1_raw_blocked", "raw S branch remains blocked", raw_blocked, "raw demo fails because epsilon_phi_raw dominates"),
        ("CG3744_2_projected_arithmetic", "projected closure arithmetic works as a stub", any(row["variant_id"] == "LS3744_1_projected_S" and row["numeric_pass"] is True for row in results), "sigma_phi_local=0 kills the local Phi_S term in dry-run arithmetic"),
        ("CG3744_3_eta_zero_arithmetic", "eta-zero closure arithmetic works as a stub", any(row["variant_id"] == "LS3744_2_eta_zero_S" and row["numeric_pass"] is True for row in results), "eta-zero branch kills the local Phi_S term in dry-run arithmetic"),
        ("CG3744_4_numeric_bound_arithmetic", "numeric-bound closure arithmetic works as a stub", any(row["variant_id"] == "LS3744_3_numeric_bound_S" and row["numeric_pass"] is True for row in results), "small supplied epsilon_phi_raw passes the tolerance dry run"),
        ("CG3744_5_no_repair_claim", "repair rows do not claim a pass", all(row["claim_allowed"] is False for row in repair_numeric_passes), "dry-run arithmetic is not a sourced theorem or data result"),
        ("CG3744_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "parent projector/eta-zero/numeric local profile sources remain absent"),
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
        ("DEC3744_0_progress", "RUNNABLE_LOCAL_SAFE_S_GATE_BUILT", "The local branch is now an executable budget gate, not just prose."),
        ("DEC3744_1_best_route", "PROJECTED_LOCAL_SAFE_S_IS_PREFERRED_REPAIR", "It preserves galaxy/cosmology morphology while letting the local PPN projection be silent if a real parent projector exists."),
        ("DEC3744_2_eta_zero_fallback", "ETA_ZERO_IS_SECOND_BEST", "It is algebraically clean but needs stronger parent legitimacy because it removes a term outright."),
        ("DEC3744_3_no_claim", "NO_LOCAL_GR_CLAIM_FROM_DRY_RUN", "Dry-run arithmetic passing is not a theorem and not evidence."),
        ("DEC3744_4_next", "NEXT_PARENT_LEGITIMACY_GATE", "The next leap is to derive or reject the parent legitimacy of the projected local-safe S closure."),
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
        "status_id": "STATUS3744_0",
        "status": "LOCAL_SAFE_S_STUB_BUILT_NONCLAIM_PARENT_LEGITIMACY_REQUIRED",
        "summary": "3744 turns the 3743 repair contract into an explicit local-safe S closure variant and PPN/Newton tolerance dry-run stub; raw S remains blocked and no local pass is claimed.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3744_0",
        "target_doc": "3745-Y5-R2FR-parent-legitimacy-of-local-safe-S-closure.md",
        "target_script": "scripts/Y5_R2FR_3745_parent_legitimacy_of_local_safe_S_closure.py",
        "objective": "derive or reject whether the projected local-safe S closure follows from a parent action/quotient projector rather than being an explicit closure patch",
        "success_gate": "either a parent-owned projector/eta-zero theorem is signed, or the closure route is permanently labeled phenomenological before data testing",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3744 - Local-Safe S Closure Variant and PPN Test Stub",
        "",
        "## Status",
        "- `LOCAL_SAFE_S_STUB_BUILT_NONCLAIM_PARENT_LEGITIMACY_REQUIRED`",
        "- This is a forward step: the 3743 repair contract is now an executable local budget gate.",
        "- The raw `S` branch remains demoted; no local GR/Newton/PPN pass is claimed from dry-run arithmetic.",
        "",
        "## Closure Variants",
    ]
    for row in grouped["closure_variants"]:
        lines.append(f"- `{row['variant_id']}` `{row['status']}`: {row['formula']} | {row['meaning']}")
    lines.extend(["", "## PPN/Newton Stub Rule"])
    lines.append("- `gamma`: pass arithmetic only if `C_gamma_S*S_eff <= tol_gamma`.")
    lines.append("- `beta`: pass arithmetic only if `C_beta_S*S_eff <= tol_beta`.")
    lines.append("- `Newton`: pass arithmetic only if `C_Newton_S*S_eff <= tol_Newton`.")
    lines.append("- `claim_allowed`: remains false unless the input row is sourced and the relevant projector/eta/numeric branch is parent-owned.")
    lines.extend(["", "## Dry-Run Results"])
    for row in grouped["dry_run_results"]:
        lines.append(f"- `{row['result_id']}` `{row['variant_id']}`: S_eff={row['S_eff']} gamma={row['gamma_residual_bound']} beta={row['beta_residual_bound']} numeric_pass={row['numeric_pass']} claim_allowed={row['claim_allowed']} | {row['failure_mode']}")
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
    variants = parse_csv(paths["closure_variants"])
    template = parse_csv(paths["input_template"])
    dry_inputs = parse_csv(paths["dry_run_inputs"])
    dry_results = parse_csv(paths["dry_run_results"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3744*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("variants_complete", "raw/projected/eta-zero/numeric variants present", len(variants) == 4 and all(token in read_text(paths["closure_variants"]) for token in ["LS3744_0_raw_S", "LS3744_1_projected_S", "LS3744_2_eta_zero_S", "LS3744_3_numeric_bound_S"])),
        ("projector_formula", "projected closure uses sigma_phi_local", "sigma_phi_local*epsilon_phi_raw" in read_text(paths["closure_variants"])),
        ("template_blocks_claim", "real-run template has missing markers and no claim", len(template) == 1 and "MISSING_" in read_text(paths["input_template"]) and all(row["claim_allowed"] == "False" for row in template)),
        ("dry_run_inputs", "four dry-run inputs present", len(dry_inputs) == 4 and all(row["source_paths"] == "DEMO_NONCLAIM" for row in dry_inputs)),
        ("dry_run_raw_fails", "raw branch fails tolerance in dry run", any(row["variant_id"] == "LS3744_0_raw_S" and row["numeric_pass"] == "False" for row in dry_results)),
        ("dry_run_repairs_pass_arithmetic", "repair branches pass arithmetic but not claim", sum(1 for row in dry_results if row["variant_id"] != "LS3744_0_raw_S" and row["numeric_pass"] == "True") == 3),
        ("dry_run_claims_blocked", "all dry-run rows keep claim_allowed false", all(row["claim_allowed"] == "False" for row in dry_results)),
        ("claim_gates_block", "local claim gate remains blocked", any(row["gate_id"] == "CG3744_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("doc_core_terms", "doc records stub and nonclaim status", all(token in read_text(paths["doc"]) for token in ["executable local budget gate", "raw `S` branch remains demoted", "claim_allowed"])),
        ("next_target_3745", "next target is parent legitimacy gate", next_target[0]["target_doc"] == "3745-Y5-R2FR-parent-legitimacy-of-local-safe-S-closure.md"),
        ("no_formalization_leak", "no 3744 files in formalization-workbench", len(formalization_leaks) == 0),
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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3744_SOURCE_REGISTER.csv",
        "closure_variants": RESIDUALS / "P8_Y5_R2FR_3744_CLOSURE_VARIANTS.csv",
        "input_template": RESIDUALS / "P8_Y5_R2FR_3744_PPN_INPUT_TEMPLATE.csv",
        "dry_run_inputs": RESIDUALS / "P8_Y5_R2FR_3744_PPN_DRY_RUN_INPUTS.csv",
        "dry_run_results": RESIDUALS / "P8_Y5_R2FR_3744_PPN_DRY_RUN_RESULTS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3744_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3744_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3744_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3744_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3744_VALIDATION.csv",
        "doc": DOC,
    }
    dry_inputs = dry_run_input_rows(timestamp)
    dry_results = dry_run_result_rows(timestamp, dry_inputs)
    grouped = {
        "source_register": source_register(timestamp),
        "closure_variants": closure_variant_rows(timestamp),
        "input_template": input_template_rows(timestamp),
        "dry_run_inputs": dry_inputs,
        "dry_run_results": dry_results,
        "claim_gates": claim_gate_rows(timestamp, dry_results),
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
        raise SystemExit(f"3744 validation failed: {failures}")
    print("wrote 3744 checkpoint: local-safe S closure variant and PPN/Newton test stub built; no claim promoted")


if __name__ == "__main__":
    main()
