from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1975-Y5-R2FR-Ub-suppression-bound-envelope-and-unsuppressed-coefficient-rows.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1975_VALIDATION.csv"

SOURCES = {
    "1974_doc": {
        "path": ROOT / "1974-Y5-R2FR-active-coefficient-dependence-on-Acurv-or-zero-projector.md",
        "needles": ["LOG1974_7_verdict", "ACT1974_7_verdict", "NEXT1974_0_primary"],
    },
    "1974_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1974_VALIDATION.csv",
        "needles": ["VAL1974_OVERALL", "PASS"],
    },
    "1974_logistic_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_LOGISTIC_DERIVATIVE_SUPPRESSION.csv",
        "needles": ["LOG1974_1_Pi_derivative", "LOG1974_6_trace_derivative"],
    },
    "1974_active_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_ACTIVE_ACURV_DEPENDENCY_STATUS.csv",
        "needles": ["ACT1974_0_Zm", "ACT1974_7_verdict"],
    },
    "85_XB_invariants": {
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": ["D_L(X_B) =", "S_cg(X_B) =", "m_L(X_B) =", "L_cg^-2 F_L(X_B)"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1975 U_B suppression bound envelope and unsuppressed coefficient rows",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def bound_constant_rows() -> list[dict[str, object]]:
    entries = [
        ("CONST1975_0_Amin", "A_min", "lower bound A_curv >= A_min over the local tested exterior", "MISSING_LOCAL_RANGE", "needed because leakage scales with 1/(1+A_min)"),
        ("CONST1975_1_Umax", "epsilon_U", "upper bound U_B <= epsilon_U over the local tested exterior", "MISSING_LOCAL_RANGE", "sets local screening strength"),
        ("CONST1975_2_Delta", "Delta_min", "strict lower bound Delta_B >= Delta_min > 0", "MISSING_PARENT_VALUE", "prevents logistic derivative blow-up"),
        ("CONST1975_3_H", "H0,H1A", "|H_L|<=H0 and |(1+A) partial_A H_L|<=H1A", "MISSING_FUNCTION_BOUND", "needed for D_L derivative envelope"),
        ("CONST1975_4_S", "S10,S11A", "|S_1|<=S10 and |(1+A) partial_A S_1|<=S11A", "MISSING_FUNCTION_BOUND", "needed for source envelope"),
        ("CONST1975_5_m2", "M20,M21A", "|m_2|<=M20 and |(1+A) partial_A m_2|<=M21A", "MISSING_FUNCTION_BOUND", "needed for m_L envelope"),
        ("CONST1975_6_F2", "F20,F21A", "|F_2|<=F20 and |(1+A) partial_A F_2|<=F21A", "MISSING_FUNCTION_BOUND", "needed for trace baseline envelope"),
        ("CONST1975_7_domain", "D_loc and norm convention", "compact local exterior, coframe, and curvature-norm regularization", "MISSING_DOMAIN_AND_REGULARIZATION", "needed before any R11 comparison"),
    ]
    rows = []
    for row_id, symbol, definition, status, use in entries:
        row = base(row_id)
        row.update({"symbol": symbol, "definition": definition, "status": status, "use": use})
        rows.append(row)
    return rows


def envelope_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ENV1975_0_U_derivative",
            "U_B derivative",
            "|partial_A U_B| <= epsilon_U/[Delta_min(1+A_min)]",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "uses U_B<=epsilon_U and 1-U_B<=1",
        ),
        (
            "ENV1975_1_DL_amplitude",
            "D_L amplitude",
            "|D_L| <= epsilon_U H0",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "direct from D_L=U_B H_L",
        ),
        (
            "ENV1975_2_DL_derivative",
            "D_L derivative",
            "|partial_A D_L| <= epsilon_U[H0/Delta_min + H1A]/(1+A_min)",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "first local fixed-point derivative envelope",
        ),
        (
            "ENV1975_3_source_amplitude",
            "U_B S_cg amplitude",
            "|U_B S_cg| <= epsilon_U^2 H0 S10",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "source drive is double-suppressed if S_cg=D_L S_1",
        ),
        (
            "ENV1975_4_source_derivative",
            "U_B S_cg derivative",
            "|partial_A(U_B S_cg)| <= epsilon_U^2[2H0S10/Delta_min + H1A S10 + H0 S11A]/(1+A_min)",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "local source derivative leakage envelope",
        ),
        (
            "ENV1975_5_mL_amplitude",
            "m_L-m_* amplitude",
            "|m_L-m_*| <= epsilon_U^2 H0^2 M20",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "local attractor displacement is double-suppressed",
        ),
        (
            "ENV1975_6_mL_derivative",
            "m_L derivative",
            "|partial_A m_L| <= epsilon_U^2[2H0M20(H0/Delta_min+H1A)+H0^2 M21A]/(1+A_min)",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "moving-extremum leakage envelope",
        ),
        (
            "ENV1975_7_trace_amplitude",
            "Gamma_L-Lambda_loc amplitude",
            "|Gamma_L-Lambda_loc| <= epsilon_U^2 H0^2 F20",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "trace baseline displacement is double-suppressed",
        ),
        (
            "ENV1975_8_trace_derivative",
            "Gamma_L derivative",
            "|partial_A Gamma_L| <= epsilon_U^2[2H0F20(H0/Delta_min+H1A)+H0^2 F21A]/(1+A_min)",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "candidate local R2/q_loc leakage envelope for D_L-powered trace terms",
        ),
        (
            "ENV1975_9_verdict",
            "suppression envelope",
            "all envelope rows remain nonclaim until constants, domain, regularization, and source paths are filled",
            "ENVELOPE_READY_INPUTS_MISSING",
            "ready for later numeric/theorem sourcing",
        ),
    ]
    rows = []
    for row_id, object_name, bound, status, implication in entries:
        row = base(row_id)
        row.update({"object": object_name, "bound": bound, "status": status, "implication": implication})
        rows.append(row)
    return rows


def unsuppressed_rows() -> list[dict[str, object]]:
    entries = [
        ("UNSUP1975_0_Zm", "partial_Acurv Z_m", "zero theorem or finite derivative bound", "MISSING_ZERO_OR_BOUND", "kinetic metric-response leakage"),
        ("UNSUP1975_1_Rpotential", "partial_Acurv partial_m R / V_mA", "zero theorem or finite mixed-Hessian bound", "MISSING_ZERO_OR_BOUND", "direct memory-environment Schur vertex"),
        ("UNSUP1975_2_gamma", "partial_Acurv gamma_B", "zero theorem or finite derivative bound", "MISSING_ZERO_OR_BOUND", "open-system relaxation coefficient leakage"),
        ("UNSUP1975_3_lambda", "partial_Acurv lambda_R", "zero theorem or finite derivative bound", "MISSING_ZERO_OR_BOUND", "memory mass/relaxation leakage"),
        ("UNSUP1975_4_Lcg", "partial_Acurv L_cg separate from Gamma_L", "zero theorem or finite scale-response bound", "MISSING_ZERO_OR_BOUND", "scale response feeds A_curv and Gamma_eff"),
        ("UNSUP1975_5_source_bath", "partial_Acurv source/bath vertices", "closed bath action or finite response bound", "MISSING_ZERO_OR_BOUND", "Ward-safe completion blocker"),
        ("UNSUP1975_6_boundary", "partial_Acurv boundary/counterterm vertices", "boundary silence theorem or finite surface response", "MISSING_ZERO_OR_BOUND", "local exterior boundary blocker"),
        ("UNSUP1975_7_verdict", "unsuppressed active derivatives", "all rows above need source-backed zero/bound values", "UNSUPPRESSED_ROWS_BLOCK_CLAIM", "cannot promote envelope to EH/local-GR claim"),
    ]
    rows = []
    for row_id, coefficient_derivative, required_input, status, risk in entries:
        row = base(row_id)
        row.update(
            {
                "coefficient_derivative": coefficient_derivative,
                "required_input": required_input,
                "status": status,
                "risk": risk,
            }
        )
        rows.append(row)
    return rows


def r11_interface_rows() -> list[dict[str, object]]:
    entries = [
        (
            "R11IF1975_0_suppressed_vertex",
            "suppressed effective B_YR component",
            "B_supp <= K_geom * epsilon_U^2 * C_env/(1+A_min) for D_L^2 trace/source terms, after projection and units are fixed",
            "INTERFACE_FORMULA_ONLY",
            "K_geom, C_env, and projection map are not supplied",
        ),
        (
            "R11IF1975_1_schur_bound",
            "suppressed Delta c_R2 envelope",
            "|Delta c_R2_supp| <= 1/2 ||H_Y^{-1}|| B_supp^2 plus bare/measure/boundary terms",
            "FORMULA_READY_VALUES_MISSING",
            "needs H_Y lower bound and all unsuppressed rows",
        ),
        (
            "R11IF1975_2_claim_gate",
            "R11 comparison",
            "Compare |Delta c_R2_total| to R11 bound only after suppressed and unsuppressed components are both source-backed",
            "R11_COMPARISON_BLOCKED",
            "no local EH/no-tower claim yet",
        ),
    ]
    rows = []
    for row_id, interface, formula, status, blocker in entries:
        row = base(row_id)
        row.update({"interface": interface, "formula": formula, "status": status, "blocker": blocker})
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1975_0_envelope", "ENV1975_0..9", "PASS_FORMULA_NONCLAIM", "suppression envelope formulas are staged"),
        ("RUN1975_1_constants", "CONST1975_0..7", "REJECTED_MISSING_CONSTANTS", "no numeric/theorem constants supplied"),
        ("RUN1975_2_unsuppressed", "UNSUP1975_0..7", "REJECTED_UNSUPPRESSED_ROWS_OPEN", "active coefficients still require zero or bounds"),
        ("RUN1975_3_R11", "R11IF1975_0..2", "REJECTED_R11_INTERFACE_INCOMPLETE", "H_Y/projection/total coefficient missing"),
        ("RUN1975_VERDICT", "all_rows", "BOUND_ENVELOPE_READY_CLAIM_BLOCKED_NONCLAIM", "next gate is sourcing constants or zeroing unsuppressed derivatives"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update({"input_row": input_row, "runner_status": runner_status, "reason": reason, "accepted_for_claim": False})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1975_0_bound_constants", "all envelope constants are source-backed", "FAIL_BLOCKED", "local range/domain/function bounds missing"),
        ("CG1975_1_unsuppressed_derivatives", "unsuppressed derivatives are zero or bounded", "FAIL_BLOCKED", "Z_m/R/gamma/lambda/Lcg/source/boundary rows open"),
        ("CG1975_2_R11_total", "total Delta c_R2 compared to R11", "FAIL_BLOCKED", "projection and H_Y missing"),
        ("CG1975_3_EH_second_order", "EH second-order local action derived", "FAIL_BLOCKED", "R2/fR bound not passed"),
        ("CG1975_4_local_GR_Newton", "local GR/Newton follows", "FAIL_BLOCKED", "EH plus matter/PPN gates remain"),
    ]
    rows = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1975_0_main_result",
            "BOUND_ENVELOPE_WRITTEN",
            "The D_L-powered route now has explicit nonclaim inequalities instead of handwavy smallness.",
            "use these as acceptance formulas for future local/R11 scoring",
        ),
        (
            "DEC1975_1_limitation",
            "UNSUPPRESSED_ROWS_DOMINATE_RISK",
            "The envelope only helps if Z_m,R,gamma,lambda,Lcg,source/boundary A_curv derivatives are zero or bounded.",
            "prioritize unsuppressed coefficient derivative zero/bound rows",
        ),
        (
            "DEC1975_2_best_next",
            "UNSUPPRESSED_ZM_R_GATE_FIRST",
            "The cleanest next attack is Z_m and R/V_R because they are closest to the actual action/Hessian Schur coefficient.",
            "try to zero or bound partial_Acurv Z_m and V_mA before gamma/lambda/source rows",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1975_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1976-Y5-R2FR-Zm-and-VR-Acurv-dependence-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_Zm_and_VR_Acurv_dependence_zero_or_bound_1976.py",
            "objective": "try to prove partial_Acurv Z_m=0 and V_mA=0 from the action coefficient firewall, or retain finite Schur derivative rows",
            "acceptance_output": "zero theorem checklist or nonclaim derivative/bound rows for Z_m and R/V_R",
            "nonclaim_rule": "no EH/local-GR claim while Z_m and R/V_R A_curv dependence is unsourced",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1975_0_project_position")
    row.update(
        {
            "strongest_result": "D_L-powered local leakage now has explicit U_B^2 bound formulas.",
            "what_improved": "Smallness has become a sourceable envelope with named constants rather than an intuition.",
            "still_missing": "numeric/theorem constants, D_loc, norm regularization, projection map, H_Y lower bound, and unsuppressed Z_m/R/gamma/lambda/Lcg/source/boundary derivative rows",
            "claim_status": "private nonclaim; bound route prepared but not scored",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_SOURCE_REGISTER.csv",
    "bound_constants": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_BOUND_CONSTANT_REQUIREMENTS.csv",
    "envelope": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_UB_SUPPRESSION_BOUND_ENVELOPE.csv",
    "unsuppressed": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_UNSUPPRESSED_ACURV_COEFFICIENT_ROWS.csv",
    "r11_interface": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_R11_INTERFACE_ROWS.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1975_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "UB_SUPPRESSION_BOUND_1975_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1975_ZM_VR_ACURV_DERIVATIVE_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1975_0_nonclaim_weight"),
            "artifact": "1975 U_B suppression bound envelope and unsuppressed coefficient rows",
            "weight": "BOUND_ENVELOPE_READY_INPUTS_MISSING",
            "reason": "D_L-powered leakage has formulas, but constants and unsuppressed coefficient derivatives are not sourced",
        }
    ]
    queue = [
        {
            **base("AQ1975_0_Zm_VR"),
            "target": "Z_m and R/V_R A_curv derivatives",
            "needed_inputs": "zero theorem or finite derivative bounds for partial_Acurv Z_m and V_mA; units; source paths",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1975_1_envelope_constants"),
            "target": "U_B envelope constants",
            "needed_inputs": "A_min;epsilon_U;Delta_min;H0/H1A;S10/S11A;M20/M21A;F20/F21A;D_loc",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "bound_constants": bound_constant_rows(),
        "envelope": envelope_rows(),
        "unsuppressed": unsuppressed_rows(),
        "r11_interface": r11_interface_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1975-", "*_1975_*", "*Y5*1975*", "*VAL1975*", "*P8*1975*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1975_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    const_ok = any(row["row_id"] == "CONST1975_0_Amin" and row["status"] == "MISSING_LOCAL_RANGE" for row in tables["bound_constants"])
    rows.append(validation_row("VAL1975_01_constants", "PASS" if const_ok else "FAIL", "bound constants are explicitly missing"))

    env_ok = any(row["row_id"] == "ENV1975_8_trace_derivative" and row["status"] == "BOUND_FORMULA_READY_VALUES_MISSING" for row in tables["envelope"])
    verdict_ok = any(row["row_id"] == "ENV1975_9_verdict" and row["status"] == "ENVELOPE_READY_INPUTS_MISSING" for row in tables["envelope"])
    rows.append(validation_row("VAL1975_02_envelope", "PASS" if env_ok and verdict_ok else "FAIL", "U_B suppression envelope rows staged"))

    unsup_ok = any(row["row_id"] == "UNSUP1975_7_verdict" and row["status"] == "UNSUPPRESSED_ROWS_BLOCK_CLAIM" for row in tables["unsuppressed"])
    rows.append(validation_row("VAL1975_03_unsuppressed", "PASS" if unsup_ok else "FAIL", "unsuppressed coefficient rows block claim"))

    r11_ok = any(row["row_id"] == "R11IF1975_2_claim_gate" and row["status"] == "R11_COMPARISON_BLOCKED" for row in tables["r11_interface"])
    rows.append(validation_row("VAL1975_04_r11_interface", "PASS" if r11_ok else "FAIL", "R11 comparison remains blocked until total coefficient exists"))

    runner_ok = any(row["row_id"] == "RUN1975_VERDICT" and row["runner_status"] == "BOUND_ENVELOPE_READY_CLAIM_BLOCKED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1975_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1975_3_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1975_06_claim_gates", "PASS" if gate_ok else "FAIL", "all claim gates blocked"))

    decision_ok = any(row["decision"] == "UNSUPPRESSED_ZM_R_GATE_FIRST" for row in tables["decision"])
    rows.append(validation_row("VAL1975_07_decision", "PASS" if decision_ok else "FAIL", "decision selects Z_m/R gate next"))

    next_ok = tables["next"][0]["target_doc"] == "1976-Y5-R2FR-Zm-and-VR-Acurv-dependence-zero-or-bound.md"
    rows.append(validation_row("VAL1975_08_next_target", "PASS" if next_ok else "FAIL", "1976 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1975_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1975_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1975_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1975_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1975_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1975_OVERALL", overall, "1975 U_B suppression bound envelope and unsuppressed coefficient rows"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Bound Constant Requirements", tables["bound_constants"]),
        ("U_B Suppression Bound Envelope", tables["envelope"]),
        ("Unsuppressed A_curv Coefficient Rows", tables["unsuppressed"]),
        ("R11 Interface Rows", tables["r11_interface"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1975 Y5 R2FR: U_B Suppression Bound Envelope And Unsuppressed Coefficient Rows",
        "",
        "Private checkpoint. This converts the 1974 symbolic suppression law into explicit sourceable bound formulas.",
        "",
        "Verdict: D_L-powered local leakage now has concrete nonclaim inequalities, including U_B^2 bounds for the source, moving extremum, and trace baseline derivatives. This is a real bounded-leakage route, but it is not claimable until the constants are sourced and the unsuppressed A_curv derivatives of Z_m, R/V_R, gamma_B, lambda_R, L_cg, source/bath, and boundary terms are zeroed or bounded.",
        "",
        "No EH/Newton/local-GR claim follows from this checkpoint.",
        "",
    ]
    for title, table_rows in sections:
        lines.extend([f"## {title}", "", markdown_table(table_rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1975_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
