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

DOC_PATH = ROOT / "1974-Y5-R2FR-active-coefficient-dependence-on-Acurv-or-zero-projector.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1974_VALIDATION.csv"

SOURCES = {
    "1973_doc": {
        "path": ROOT / "1973-Y5-R2FR-XB-env-route-split-firewall-or-CXR-first-row.md",
        "needles": ["CXRROW1973_5_effective_vertex", "ACD1973_6_verdict", "NEXT1973_0_primary"],
    },
    "1973_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1973_VALIDATION.csv",
        "needles": ["VAL1973_OVERALL", "PASS"],
    },
    "85_XB_invariants": {
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": ["B_env =", "Pi_B =", "D_L(X_B) =", "m_L(X_B) =", "L_cg^-2 F_L(X_B)"],
    },
    "83_parent_equations": {
        "path": FORMALIZATION / "83-parent-equations-v1.md",
        "needles": ["gamma_B(X_B)", "lambda_R(X_B)", "F_L(X_B)", "R(m; X_B)", "E7 is effective open-system dynamics"],
    },
    "826_coefficients": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
        "needles": ["Z_m(X_B)", "R(m;X_B)", "F_L(X_B), a_F, L_cg(X_B)"],
    },
    "1306_XB_domain": {
        "path": ROOT / "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
        "needles": ["FRA1306_1_XB_dependent", "NO_PARENT_FUNCTION_FOUND_DEMOTE_TO_EXPLICIT_CLOSURE"],
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
                "purpose": "1974 active A_curv coefficient dependence or zero projector",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def zero_projector_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ZP1974_0_projector_theorem",
            "exact zero projector",
            "If every action-relevant coefficient c_i(X_B) factors as c_i=cbar_i(P_env X_B) and P_env annihilates A_curv/X_route, then partial_Acurv c_i=0.",
            "RELATIVE_THEOREM_CLEAN",
            "This is the exact way to quarantine curvature diagnostics from the EH action.",
        ),
        (
            "ZP1974_1_current_parent_form",
            "current parent equations use unsplit X_B",
            "83 writes gamma_B(X_B), lambda_R(X_B), R(m;X_B), F_L(X_B), m_L(X_B), and 85 writes D_L(X_B), S_cg(X_B), m_L(X_B), F_L(X_B).",
            "ZERO_PROJECTOR_NOT_SOURCE_SIGNED",
            "No source proves the active coefficient functions factor through P_env.",
        ),
        (
            "ZP1974_2_full_Acurv_zero",
            "partial_Acurv c_i=0 for the full current bundle",
            "False as a generic theorem: current X_B includes A_curv, and action-relevant symbols are functions of X_B unless split.",
            "FULL_BUNDLE_ZERO_REJECTED",
            "Do not claim EH/no-tower through full-X_B geometry blindness.",
        ),
        (
            "ZP1974_3_suppression_not_zero",
            "local logistic suppression",
            "Pi_B(A_curv) -> 1 and U_B -> 0 can suppress D_L-powered terms, but finite A_curv gives derivative leakage rather than exact zero.",
            "SUPPRESSION_ROUTE_IDENTIFIED",
            "This opens a bound route, not a theorem-zero route.",
        ),
        (
            "ZP1974_4_verdict",
            "1974 zero projector verdict",
            "Exact zero requires a new P_env dependency theorem. Current corpus only supports a possible local suppression law for D_L-powered closure terms.",
            "ZERO_PROJECTOR_FAILS_CURRENT_CORPUS",
            "Derive/bound suppression powers next, while retaining finite Schur rows for unsuppressed coefficients.",
        ),
    ]
    rows = []
    for row_id, gate, statement, status, implication in entries:
        row = base(row_id)
        row.update({"gate": gate, "statement": statement, "status": status, "implication": implication})
        rows.append(row)
    return rows


def logistic_derivative_rows() -> list[dict[str, object]]:
    entries = [
        (
            "LOG1974_0_Benv",
            "B_env(A_curv,E_theta)",
            "B_env = ln(1+A_curv) - w_theta ln(1+E_theta)",
            "SOURCE_BACKED_SYMBOLIC",
            "A_curv enters the routing scalar explicitly.",
        ),
        (
            "LOG1974_1_Pi_derivative",
            "partial_Acurv Pi_B",
            "partial_A Pi_B = Pi_B(1-Pi_B)/(Delta_B(1+A_curv)) when E_theta and constants are held fixed",
            "DERIVED_SYMBOLIC",
            "Pi_B derivative is suppressed in the local Pi_B -> 1 limit but not identically zero.",
        ),
        (
            "LOG1974_2_U_derivative",
            "partial_Acurv U_B",
            "partial_A U_B = -Pi_B(1-Pi_B)/(Delta_B(1+A_curv)) = -U_B(1-U_B)/(Delta_B(1+A_curv))",
            "DERIVED_SYMBOLIC",
            "U_B-powered local leakage scales with U_B for screened systems.",
        ),
        (
            "LOG1974_3_DL_derivative",
            "D_L=U_B H_L",
            "partial_A D_L = H_L partial_A U_B + U_B partial_A H_L = O(U_B/(1+A_curv)) if H_L and partial_A H_L are bounded",
            "CONDITIONAL_SUPPRESSION_LAW",
            "Requires bounded H_L and no hidden singular branch dependence.",
        ),
        (
            "LOG1974_4_source_derivative",
            "U_B S_cg with S_cg=D_L S_1",
            "U_B S_cg = U_B^2 H_L S_1; partial_A(U_B S_cg)=O(U_B^2/(1+A_curv)) under bounded H_L,S_1 derivatives",
            "CONDITIONAL_DOUBLE_SUPPRESSION",
            "Promising for local source silence, not a proof without bounds.",
        ),
        (
            "LOG1974_5_mL_derivative",
            "m_L=m_*+D_L^2 m_2",
            "partial_A m_L = 2 D_L partial_A D_L m_2 + D_L^2 partial_A m_2 = O(U_B^2/(1+A_curv)) under bounded m_2,H_L derivatives",
            "CONDITIONAL_DOUBLE_SUPPRESSION",
            "This is a real derivative/amplitude law, but still nonclaim.",
        ),
        (
            "LOG1974_6_trace_derivative",
            "Gamma_L=L_cg^-2 F_L=Lambda_loc+D_L^2 F_2",
            "partial_A Gamma_L = 2 D_L partial_A D_L F_2 + D_L^2 partial_A F_2 = O(U_B^2/(1+A_curv)) under bounded F_2,H_L derivatives",
            "CONDITIONAL_DOUBLE_SUPPRESSION",
            "This could bound trace drift/R2 leakage if F_2 is the only active A_curv route.",
        ),
        (
            "LOG1974_7_verdict",
            "local suppression law",
            "D_L-powered closure laws give U_B or U_B^2 derivative suppression, but exact C_XR zero is not obtained.",
            "SUPPRESSION_LAW_READY_INPUTS_UNSIGNED",
            "Next target should bind H_L,S_1,m_2,F_2 derivatives and separate unsuppressed coefficients.",
        ),
    ]
    rows = []
    for row_id, object_name, formula, status, implication in entries:
        row = base(row_id)
        row.update({"object": object_name, "formula": formula, "status": status, "implication": implication})
        rows.append(row)
    return rows


def active_dependency_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ACT1974_0_Zm",
            "Z_m(X_B)",
            "826/1306 name Z_m(X_B) but no parent function or P_env factorization exists",
            "UNSUPPRESSED_DEPENDENCE_UNKNOWN",
            "If partial_Acurv Z_m != 0, kinetic metric response is a live residual.",
        ),
        (
            "ACT1974_1_Rpotential",
            "R(m;X_B) / V_R(m;X_B)",
            "83/826 use R(m;X_B); no parent function or D_L-only factorization is supplied",
            "UNSUPPRESSED_DEPENDENCE_UNKNOWN",
            "If partial_Acurv partial_m R or V_mA is nonzero, the Schur block is mandatory.",
        ),
        (
            "ACT1974_2_gamma_lambda",
            "gamma_B(X_B), lambda_R(X_B)",
            "83 uses gamma_B and lambda_R as active open-system coefficients",
            "UNSUPPRESSED_DEPENDENCE_UNKNOWN",
            "These can bypass the D_L suppression law unless bounded/factored.",
        ),
        (
            "ACT1974_3_source",
            "U_B S_cg with S_cg=D_L S_1",
            "85 gives a D_L-powered form, producing conditional U_B^2 suppression",
            "SUPPRESSED_IF_BOUNDS_HOLD",
            "Needs bounded H_L,S_1 and derivative bounds before local claim.",
        ),
        (
            "ACT1974_4_mL",
            "m_L(X_B)",
            "85 gives m_L=m_*+D_L^2 m_2",
            "SUPPRESSED_IF_BOUNDS_HOLD",
            "Derivative is O(U_B^2/(1+A)) if m_2/H_L are bounded.",
        ),
        (
            "ACT1974_5_trace_baseline",
            "L_cg^-2 F_L(X_B)",
            "85 gives L_cg^-2 F_L=Lambda_loc+D_L^2 F_2",
            "SUPPRESSED_IF_BOUNDS_HOLD",
            "The combined baseline can be suppressed even if F_L and L_cg separately are not controlled.",
        ),
        (
            "ACT1974_6_Lcg_separate",
            "L_cg(X_B) separately",
            "85 includes L_cg in X_B and 83 uses L_cg in Gamma_eff; separate L_cg response is not bounded by the combined baseline law",
            "SEPARATE_SCALE_RESPONSE_OPEN",
            "Potential circularity: A_curv contains L_cg while L_cg may depend on X_B.",
        ),
        (
            "ACT1974_7_verdict",
            "active A_curv dependency status",
            "Some closure-combination derivatives are conditionally suppressed, but core functions Z_m,R,gamma,lambda,L_cg remain unsuppressed/unknown.",
            "ACTIVE_DEPENDENCY_NOT_CLOSED",
            "Local EH cannot be claimed; split coefficients or fill finite Schur rows.",
        ),
    ]
    rows = []
    for row_id, coefficient, evidence, status, implication in entries:
        row = base(row_id)
        row.update({"coefficient": coefficient, "evidence": evidence, "status": status, "implication": implication})
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1974_0_zero_projector", "ZP1974_0_projector_theorem", "PASS_RELATIVE_THEOREM", "exact zero projector theorem is clean if P_env is supplied"),
        ("RUN1974_1_current_zero", "ZP1974_4_verdict", "REJECTED_UNSIGNED", "current corpus does not supply P_env factorization"),
        ("RUN1974_2_suppression_law", "LOG1974_7_verdict", "PASS_CONDITIONAL_NONCLAIM", "D_L-powered terms have symbolic U_B suppression"),
        ("RUN1974_3_unsuppressed_coefficients", "ACT1974_7_verdict", "REJECTED_ACTIVE_DEPENDENCY_OPEN", "Z_m/R/gamma/lambda/Lcg remain active unknowns"),
        ("RUN1974_VERDICT", "all_rows", "ZERO_PROJECTOR_FAILS_SUPPRESSION_LAW_PARTIAL_NONCLAIM", "next gate is derivative bounds plus unsuppressed coefficient split/fill"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update({"input_row": input_row, "runner_status": runner_status, "reason": reason, "accepted_for_claim": False})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1974_0_zero_projector", "P_env zero projector is parent-signed", "FAIL_BLOCKED", "relative theorem only"),
        ("CG1974_1_full_Acurv_zero", "full current A_curv dependence vanishes", "FAIL_REJECTED", "current unsplit X_B dependence remains"),
        ("CG1974_2_suppression_bound", "U_B suppression has numeric/theorem bound", "FAIL_BLOCKED", "H_L,S_1,m_2,F_2 derivative bounds missing"),
        ("CG1974_3_unsuppressed_coefficients", "Z_m/R/gamma/lambda/Lcg A_curv derivatives are zero or bounded", "FAIL_BLOCKED", "active dependency map open"),
        ("CG1974_4_EH_second_order", "EH second-order local action derived", "FAIL_BLOCKED", "R2/fR coefficient not zeroed or bounded"),
        ("CG1974_5_local_GR_Newton", "local GR/Newton follows", "FAIL_BLOCKED", "EH plus matter/PPN gates remain"),
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
            "DEC1974_0_main_result",
            "SUPPRESSION_NOT_EXACT_ZERO",
            "The logistic/D_L structure gives U_B and U_B^2 suppression laws for closure terms, but it does not prove exact A_curv independence.",
            "treat this as a bound route, not a theorem-zero route",
        ),
        (
            "DEC1974_1_live_problem",
            "UNSUPPRESSED_COEFFICIENTS_REMAIN",
            "Z_m, R/V_R, gamma_B, lambda_R, source/bath terms, and separate L_cg response can still depend on A_curv unless a P_env split is signed.",
            "audit/zero these active derivatives or put them in the Schur coefficient pack",
        ),
        (
            "DEC1974_2_best_next",
            "DERIVATIVE_BOUND_ENVELOPE",
            "The best non-circular route is to turn the U_B suppression law into a local R11 envelope while separately retaining unsuppressed coefficient rows.",
            "derive bounded H_L,S_1,m_2,F_2 derivative constants and first finite rows for unknown coefficients",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1974_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1975-Y5-R2FR-Ub-suppression-bound-envelope-and-unsuppressed-coefficient-rows.md",
            "target_script": "scripts/Y5_R2FR_Ub_suppression_bound_envelope_and_unsuppressed_coefficient_rows_1975.py",
            "objective": "convert the symbolic U_B suppression law into a local bound envelope and retain first explicit rows for unsuppressed A_curv derivatives",
            "acceptance_output": "bounded derivative envelope for D_L-powered terms plus nonclaim coefficient rows for Z_m,R,gamma,lambda,Lcg",
            "nonclaim_rule": "no EH/local-GR claim until suppression envelope and unsuppressed coefficient rows are source-backed",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1974_0_project_position")
    row.update(
        {
            "strongest_result": "A mathematically clean U_B suppression law exists for D_L-powered local closure terms.",
            "what_improved": "The coupling problem split into suppressed closure derivatives versus unsuppressed core coefficient derivatives.",
            "still_missing": "P_env zero projector, H_L/S_1/m_2/F_2 derivative bounds, Z_m/R/gamma/lambda/Lcg A_curv derivative zeros or finite values, R11 comparison",
            "claim_status": "private nonclaim; suppression route promising but not claimable",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_SOURCE_REGISTER.csv",
    "zero_projector": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_ZERO_PROJECTOR_GATE.csv",
    "logistic_derivatives": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_LOGISTIC_DERIVATIVE_SUPPRESSION.csv",
    "active_dependencies": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_ACTIVE_ACURV_DEPENDENCY_STATUS.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1974_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "ACTIVE_ACURV_DEPENDENCE_1974_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1974_UB_SUPPRESSION_AND_ACURV_COEFFICIENT_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1974_0_nonclaim_weight"),
            "artifact": "1974 active coefficient dependence on Acurv or zero projector",
            "weight": "SUPPRESSION_LAW_PARTIAL_ACTIVE_DEPENDENCIES_OPEN",
            "reason": "D_L-powered terms suppress with U_B, but exact zero projector and unsuppressed coefficients remain open",
        }
    ]
    queue = [
        {
            **base("AQ1974_0_derivative_bounds"),
            "target": "bounded H_L,S_1,m_2,F_2 derivative constants",
            "needed_inputs": "bounds over D_loc; A_curv range; Delta_B; H_L/S_1/m_2/F_2 norms; source paths",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1974_1_unsuppressed_coefficients"),
            "target": "A_curv derivative rows for Z_m,R,gamma,lambda,Lcg",
            "needed_inputs": "zero theorem or finite derivative values; units; active coefficient dependency source",
            "priority": "HIGHEST",
        },
    ]
    return {
        "source_register": source_register(),
        "zero_projector": zero_projector_rows(),
        "logistic_derivatives": logistic_derivative_rows(),
        "active_dependencies": active_dependency_rows(),
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
    patterns = ("1974-", "*_1974_*", "*Y5*1974*", "*VAL1974*", "*P8*1974*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1974_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    zp_ok = any(row["row_id"] == "ZP1974_0_projector_theorem" and row["status"] == "RELATIVE_THEOREM_CLEAN" for row in tables["zero_projector"])
    zp_fail = any(row["row_id"] == "ZP1974_4_verdict" and row["status"] == "ZERO_PROJECTOR_FAILS_CURRENT_CORPUS" for row in tables["zero_projector"])
    rows.append(validation_row("VAL1974_01_zero_projector", "PASS" if zp_ok and zp_fail else "FAIL", "zero projector theorem relative but unsigned"))

    pi_ok = any(row["row_id"] == "LOG1974_1_Pi_derivative" and row["status"] == "DERIVED_SYMBOLIC" for row in tables["logistic_derivatives"])
    dl_ok = any(row["row_id"] == "LOG1974_3_DL_derivative" and row["status"] == "CONDITIONAL_SUPPRESSION_LAW" for row in tables["logistic_derivatives"])
    dbl_ok = any(row["row_id"] == "LOG1974_6_trace_derivative" and row["status"] == "CONDITIONAL_DOUBLE_SUPPRESSION" for row in tables["logistic_derivatives"])
    rows.append(validation_row("VAL1974_02_logistic_suppression", "PASS" if pi_ok and dl_ok and dbl_ok else "FAIL", "Pi/U/D_L derivative suppression laws recorded"))

    active_ok = any(row["row_id"] == "ACT1974_7_verdict" and row["status"] == "ACTIVE_DEPENDENCY_NOT_CLOSED" for row in tables["active_dependencies"])
    unsup_ok = any(row["row_id"] == "ACT1974_0_Zm" and row["status"] == "UNSUPPRESSED_DEPENDENCE_UNKNOWN" for row in tables["active_dependencies"])
    rows.append(validation_row("VAL1974_03_active_dependencies", "PASS" if active_ok and unsup_ok else "FAIL", "active unsuppressed coefficients remain open"))

    runner_ok = any(row["row_id"] == "RUN1974_VERDICT" and row["runner_status"] == "ZERO_PROJECTOR_FAILS_SUPPRESSION_LAW_PARTIAL_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1974_04_runner", "PASS" if runner_ok else "FAIL", "runner blocks exact-zero/EH claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1974_4_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1974_05_claim_gates", "PASS" if gate_ok else "FAIL", "all claim gates blocked or rejected"))

    decision_ok = any(row["decision"] == "DERIVATIVE_BOUND_ENVELOPE" for row in tables["decision"])
    rows.append(validation_row("VAL1974_06_decision", "PASS" if decision_ok else "FAIL", "decision selects derivative bound envelope next"))

    next_ok = tables["next"][0]["target_doc"] == "1975-Y5-R2FR-Ub-suppression-bound-envelope-and-unsuppressed-coefficient-rows.md"
    rows.append(validation_row("VAL1974_07_next_target", "PASS" if next_ok else "FAIL", "1975 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1974_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1974_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1974_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1974_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1974_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1974_OVERALL", overall, "1974 active Acurv coefficient dependence or zero projector"))
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
        ("Zero Projector Gate", tables["zero_projector"]),
        ("Logistic Derivative Suppression", tables["logistic_derivatives"]),
        ("Active A_curv Dependency Status", tables["active_dependencies"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1974 Y5 R2FR: Active Coefficient Dependence On A_curv Or Zero Projector",
        "",
        "Private checkpoint. This tests whether the `A_curv` route can be exactly projected out of action coefficients, or whether it survives as a finite Schur/R2 source.",
        "",
        "Verdict: exact zero requires a parent-signed `P_env` projector/factorization theorem, which the current corpus does not supply. However, the logistic/local-distance branch gives a concrete suppression law: `partial_A Pi_B`, `partial_A U_B`, and D_L-powered derivatives are suppressed by powers of `U_B/(1+A_curv)`. That is promising for a bound route, but not a local-GR theorem because `Z_m`, `R/V_R`, `gamma_B`, `lambda_R`, source/bath terms, and separate `L_cg` response remain unsuppressed or unknown.",
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
    print(f"VAL1974_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
