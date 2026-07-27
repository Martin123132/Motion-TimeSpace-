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

DOC_PATH = ROOT / "1973-Y5-R2FR-XB-env-route-split-firewall-or-CXR-first-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1973_VALIDATION.csv"

SOURCES = {
    "1972_doc": {
        "path": ROOT / "1972-Y5-R2FR-minimal-XB-parent-ownership-clause-or-Schur-fill.md",
        "needles": ["XBI1972_0_current_XB_contains_curvature", "NEXT1972_0_primary"],
    },
    "1972_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1972_VALIDATION.csv",
        "needles": ["VAL1972_OVERALL", "PASS"],
    },
    "85_XB_invariants": {
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": ["Sector projections may use different functions of `X_B`", "A_curv", "Pi_B", "They are routing and eligibility variables."],
    },
    "83_parent_equations": {
        "path": FORMALIZATION / "83-parent-equations-v1.md",
        "needles": ["F_L(X_B)", "R(m; X_B)", "m_L(X_B)", "coarse-graining theorem for X_B"],
    },
    "1306_XB_domain": {
        "path": ROOT / "1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md",
        "needles": ["FRA1306_1_XB_dependent", "XDG1306_4_arena_rule"],
    },
    "826_coefficients": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_COEFFICIENT_LEDGER.csv",
        "needles": ["C826_0_Zm", "C826_1_R_potential", "C826_3_trace_coefficients"],
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
                "purpose": "1973 X_env/X_route split firewall or C_XR first row",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def firewall_rows() -> list[dict[str, object]]:
    entries = [
        (
            "FIRE1973_0_split_definition",
            "X_B split candidate",
            "X_B := (X_env, X_route), where X_env owns action coefficients and X_route owns routing/eligibility diagnostics such as A_curv and Pi_B.",
            "SPLIT_DEFINITION_WRITTEN",
            "This is the only route that can keep useful curvature diagnostics without injecting them into the EH action.",
        ),
        (
            "FIRE1973_1_action_firewall",
            "action coefficients ignore X_route",
            "Z_m,V_R,F_L,L_cg,m_L may depend on X_env but not on A_curv/X_route unless the induced Schur coefficient is retained.",
            "REQUIRED_NOT_SOURCE_SIGNED",
            "Current 83 writes these as functions of X_B, not X_env.",
        ),
        (
            "FIRE1973_2_route_owner",
            "routing diagnostics are Ward-safe",
            "Pi_B,U_B,D_L and routing projectors may use X_route only if they are readout-only after variation or have a Khat/source/boundary stress owner.",
            "REQUIRED_NOT_SOURCE_SIGNED",
            "85 names routing variables but says the theorem is not derived.",
        ),
        (
            "FIRE1973_3_same_parent_law",
            "no per-sector retuning",
            "X_env/X_route split must be one universal parent decomposition, not local-vs-galaxy relabelling after data.",
            "POLICY_PASS_THEOREM_MISSING",
            "83/85 already forbid arbitrary per-sector X_B, but do not derive the split.",
        ),
        (
            "FIRE1973_4_active_dependency_list",
            "active coefficient dependency list",
            "The parent must list which X_B components enter Z_m, V_R, F_L, L_cg, m_L, gamma_B, lambda_R, and source/bath terms.",
            "MISSING_ACTIVE_DEPENDENCY_LIST",
            "Without this, C_XR cannot be zeroed or scored.",
        ),
        (
            "FIRE1973_5_verdict",
            "split firewall status",
            "The split is a strong architecture repair, but it is not present as a current parent theorem.",
            "SPLIT_FIREWALL_FAILS_CURRENT_CORPUS",
            "Proceed to first C_XR row and active-coefficient derivative audit.",
        ),
    ]
    rows = []
    for row_id, gate, condition, status, implication in entries:
        row = base(row_id)
        row.update({"gate": gate, "condition": condition, "status": status, "implication": implication})
        rows.append(row)
    return rows


def cxr_first_row() -> list[dict[str, object]]:
    entries = [
        (
            "CXRROW1973_0_Acurv_definition",
            "A_curv",
            "A_curv = (c L_cg/H_bg)(w_C C_abs + w_R R_abs)",
            "SOURCE_BACKED_SYMBOLIC",
            "dimensionless curvature diagnostic in current X_B candidate",
        ),
        (
            "CXRROW1973_1_variation_formula",
            "delta A_curv",
            "delta A_curv = (c L_cg/H_bg)[w_C <C,delta C>/C_abs + w_R <Ric,delta Ric>/R_abs] + A_curv delta ln(L_cg/H_bg), away from norm-zero points",
            "DERIVED_SYMBOLIC_NONCLAIM",
            "this is the first explicit C_XR shape; it is direction-dependent, not a scalar number yet",
        ),
        (
            "CXRROW1973_2_scalar_projection",
            "projection to delta R_geom",
            "C_XR[A_curv] requires a map from scalar Ricci variation to delta Ricci/Weyl norm directions on the selected local branch",
            "MISSING_PROJECTION_MAP",
            "cannot score R2/fR until weak-field projection convention is fixed",
        ),
        (
            "CXRROW1973_3_norm_regularization",
            "norm-zero/cusp guard",
            "C_abs=sqrt(C^2), R_abs=sqrt(Ric^2) have derivative singularities at zero norm unless smoothed or branch-bounded away from zero",
            "MISSING_REGULARIZATION_OR_BRANCH_BOUND",
            "important for vacuum/asymptotic local systems",
        ),
        (
            "CXRROW1973_4_units",
            "units",
            "[C_XR] = [A_curv]/[R_geom] = L^2 for dimensionless A_curv and R_geom with units L^-2",
            "UNITS_FORMULA_READY",
            "numeric comparison still needs normalization and active coefficient derivative",
        ),
        (
            "CXRROW1973_5_effective_vertex",
            "effective curvature vertex",
            "B_XR^eff = sum_A (partial coefficient/partial X_B^A) C_XR^A; for A=A_curv this needs partial_Acurv Z_m,V_R,F_L,L_cg,m_L,...",
            "MISSING_ACTIVE_COEFFICIENT_DERIVATIVES",
            "the next root input is not just C_XR, but which coefficients actually depend on A_curv",
        ),
        (
            "CXRROW1973_6_claim_status",
            "first C_XR row",
            "symbolic shape exists but no numeric/theorem value, projection map, regularization, or coefficient derivative is supplied",
            "FIRST_ROW_STAGED_NONCLAIM",
            "valid_for_claim remains false",
        ),
    ]
    rows = []
    for row_id, object_name, formula, status, requirement in entries:
        row = base(row_id)
        row.update({"object": object_name, "formula": formula, "status": status, "requirement": requirement})
        rows.append(row)
    return rows


def active_coefficient_rows() -> list[dict[str, object]]:
    entries = [
        ("ACD1973_0_Zm", "Z_m(X_B)", "partial_Acurv Z_m", "MISSING_PARENT_FUNCTION", "if nonzero, kinetic normalization contributes metric-response residuals"),
        ("ACD1973_1_VR", "V_R(m;X_B)", "partial_Acurv partial_m V_R or mixed Hessian V_mA", "MISSING_PARENT_FUNCTION", "if nonzero, memory scalar mediates a curvature-induced Schur term"),
        ("ACD1973_2_FL", "F_L(X_B)", "partial_Acurv F_L", "MISSING_PARENT_FUNCTION", "if nonzero, local trace baseline has curvature dependence beyond EH"),
        ("ACD1973_3_Lcg", "L_cg(X_B)", "partial_Acurv L_cg", "MISSING_PARENT_FUNCTION", "if nonzero, scale response feeds both q_loc and C_XR rows"),
        ("ACD1973_4_mL", "m_L(X_B)", "partial_Acurv m_L", "MISSING_PARENT_FUNCTION", "moving extremum can move with curvature and feed the two-field block"),
        ("ACD1973_5_source_bath", "source/bath terms", "partial_Acurv source/bath vertices", "MISSING_ACTION", "open-system terms must not bypass the firewall"),
        ("ACD1973_6_verdict", "active dependency map", "all active coefficient derivatives with respect to A_curv", "MISSING_DEPENDENCY_MAP", "next target should zero these or keep finite Schur rows"),
    ]
    rows = []
    for row_id, coefficient, needed_derivative, status, implication in entries:
        row = base(row_id)
        row.update(
            {
                "coefficient": coefficient,
                "needed_derivative": needed_derivative,
                "status": status,
                "implication": implication,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("RUN1973_0_split_definition", "FIRE1973_0_split_definition", "PASS_ARCHITECTURE_CANDIDATE", "split route is well-formed"),
        ("RUN1973_1_firewall", "FIRE1973_5_verdict", "REJECTED_NOT_SOURCE_SIGNED", "current corpus does not prove action coefficients ignore X_route"),
        ("RUN1973_2_CXR_shape", "CXRROW1973_1_variation_formula", "PASS_SYMBOLIC_NONCLAIM", "first C_XR derivative shape written"),
        ("RUN1973_3_CXR_score", "CXRROW1973_2..5", "REJECTED_MISSING_PROJECTION_AND_DERIVATIVES", "projection, regularization, and active derivatives missing"),
        ("RUN1973_VERDICT", "all_rows", "SPLIT_FIREWALL_UNSIGNED_FIRST_CXR_ROW_STAGED_NONCLAIM", "next gate is active coefficient dependence on A_curv"),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update({"input_row": input_row, "runner_status": runner_status, "reason": reason, "accepted_for_claim": False})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1973_0_split_firewall", "X_env/X_route split firewall derived", "FAIL_BLOCKED", "architecture candidate only"),
        ("CG1973_1_CXR_numeric", "C_XR[A_curv] is numeric/theorem-sourced", "FAIL_BLOCKED", "projection and regularization missing"),
        ("CG1973_2_active_derivatives_zero", "active coefficient derivatives wrt A_curv vanish", "FAIL_BLOCKED", "dependency map missing"),
        ("CG1973_3_schur_score", "Schur R2/fR coefficient scoreable", "FAIL_BLOCKED", "B_YR/H_Y incomplete"),
        ("CG1973_4_EH_second_order", "EH second-order local action derived", "FAIL_BLOCKED", "R2/fR gate open"),
        ("CG1973_5_local_GR_Newton", "local GR/Newton follows", "FAIL_BLOCKED", "EH plus matter/PPN gates remain"),
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
            "DEC1973_0_result",
            "SPLIT_FIREWALL_NOT_DERIVED",
            "The split is the right architecture but the current parent equations still use unsplit X_B in action-relevant coefficients.",
            "do not claim the split until active dependencies are rewritten and Ward-owned",
        ),
        (
            "DEC1973_1_first_row",
            "CXR_ACURV_FIRST_ROW_STAGED",
            "The first symbolic C_XR[A_curv] derivative is written; the missing pieces are projection, regularization, and active coefficient derivatives.",
            "audit whether coefficients actually depend on A_curv; zero them or keep Schur rows",
        ),
        (
            "DEC1973_2_best_next",
            "ACTIVE_COEFFICIENT_DEPENDENCE_ON_ACURV",
            "If partial_Acurv Z_m,V_R,F_L,L_cg,m_L all vanish by architecture, the curvature diagnostic can be quarantined; if not, the Schur route is mandatory.",
            "target active coefficient dependency map next",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1973_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1974-Y5-R2FR-active-coefficient-dependence-on-Acurv-or-zero-projector.md",
            "target_script": "scripts/Y5_R2FR_active_coefficient_dependence_on_Acurv_or_zero_projector_1974.py",
            "objective": "prove action-relevant coefficients have zero derivative with respect to A_curv, or promote A_curv to an explicit Schur/R2 coefficient source",
            "acceptance_output": "active dependency zero map or finite derivative rows for Z_m,V_R,F_L,L_cg,m_L and source/bath terms",
            "nonclaim_rule": "no EH/local-GR claim while active A_curv coefficient dependence is unknown",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1973_0_project_position")
    row.update(
        {
            "strongest_result": "The split architecture is identified, and the first symbolic C_XR[A_curv] derivative row exists.",
            "what_improved": "The bottleneck moved from vague coupling language to active coefficient derivatives with respect to A_curv.",
            "still_missing": "active dependency map, projection from scalar curvature variation to curvature norms, norm regularization, H_Y/B_YR values, source/bath/boundary owner",
            "claim_status": "private nonclaim; split firewall unsigned and first C_XR row unscoreable",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_SOURCE_REGISTER.csv",
    "firewall": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_XENV_XROUTE_FIREWALL_TEST.csv",
    "cxr_first": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_CXR_ACURV_FIRST_ROW.csv",
    "active_coefficients": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_ACTIVE_COEFFICIENT_DEPENDENCY_MAP.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1973_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "XB_SPLIT_OR_CXR_1973_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1973_ACTIVE_ACURV_DEPENDENCY_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1973_0_nonclaim_weight"),
            "artifact": "1973 X_env/X_route split firewall or C_XR first row",
            "weight": "SPLIT_ARCHITECTURE_IDENTIFIED_FIRST_CXR_ROW_STAGED",
            "reason": "firewall is not current-source-signed; A_curv derivative row staged as nonclaim",
        }
    ]
    queue = [
        {
            **base("AQ1973_0_active_Acurv_dependency"),
            "target": "active coefficient derivative map",
            "needed_inputs": "partial_Acurv Z_m,V_R,F_L,L_cg,m_L,gamma_B,lambda_R,source/bath terms; source paths; zero theorem or finite values",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1973_1_projection_regularization"),
            "target": "C_XR projection and norm regularization",
            "needed_inputs": "weak-field projection from delta R_geom to Ricci/Weyl norms; smoothing or branch lower bounds for zero norm",
            "priority": "HIGH_IF_DERIVATIVES_NONZERO",
        },
    ]
    return {
        "source_register": source_register(),
        "firewall": firewall_rows(),
        "cxr_first": cxr_first_row(),
        "active_coefficients": active_coefficient_rows(),
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
    patterns = ("1973-", "*_1973_*", "*Y5*1973*", "*VAL1973*", "*P8*1973*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1973_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    split_ok = any(row["row_id"] == "FIRE1973_0_split_definition" and row["status"] == "SPLIT_DEFINITION_WRITTEN" for row in tables["firewall"])
    fail_ok = any(row["row_id"] == "FIRE1973_5_verdict" and row["status"] == "SPLIT_FIREWALL_FAILS_CURRENT_CORPUS" for row in tables["firewall"])
    rows.append(validation_row("VAL1973_01_firewall", "PASS" if split_ok and fail_ok else "FAIL", "split firewall defined but not source-signed"))

    cxr_ok = any(row["row_id"] == "CXRROW1973_1_variation_formula" and row["status"] == "DERIVED_SYMBOLIC_NONCLAIM" for row in tables["cxr_first"])
    guard_ok = any(row["row_id"] == "CXRROW1973_3_norm_regularization" and row["status"] == "MISSING_REGULARIZATION_OR_BRANCH_BOUND" for row in tables["cxr_first"])
    rows.append(validation_row("VAL1973_02_cxr_first_row", "PASS" if cxr_ok and guard_ok else "FAIL", "first symbolic C_XR[A_curv] row and norm guard recorded"))

    dep_ok = any(row["row_id"] == "ACD1973_6_verdict" and row["status"] == "MISSING_DEPENDENCY_MAP" for row in tables["active_coefficients"])
    rows.append(validation_row("VAL1973_03_active_coefficients", "PASS" if dep_ok else "FAIL", "active A_curv coefficient dependency map remains missing"))

    runner_ok = any(row["row_id"] == "RUN1973_VERDICT" and row["runner_status"] == "SPLIT_FIREWALL_UNSIGNED_FIRST_CXR_ROW_STAGED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1973_04_runner", "PASS" if runner_ok else "FAIL", "runner blocks split/CXR claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1973_4_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1973_05_claim_gates", "PASS" if gate_ok else "FAIL", "all claim gates blocked"))

    decision_ok = any(row["decision"] == "ACTIVE_COEFFICIENT_DEPENDENCE_ON_ACURV" for row in tables["decision"])
    rows.append(validation_row("VAL1973_06_decision", "PASS" if decision_ok else "FAIL", "decision selects active A_curv dependency next"))

    next_ok = tables["next"][0]["target_doc"] == "1974-Y5-R2FR-active-coefficient-dependence-on-Acurv-or-zero-projector.md"
    rows.append(validation_row("VAL1973_07_next_target", "PASS" if next_ok else "FAIL", "1974 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1973_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1973_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1973_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1973_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1973_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1973_OVERALL", overall, "1973 X_env/X_route split firewall or C_XR first row"))
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
        ("X_env/X_route Firewall Test", tables["firewall"]),
        ("C_XR A_curv First Row", tables["cxr_first"]),
        ("Active Coefficient Dependency Map", tables["active_coefficients"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1973 Y5 R2FR: X_env/X_route Split Firewall Or C_XR First Row",
        "",
        "Private checkpoint. This tests the architecture repair selected in 1972: keep curvature diagnostics as routing/readout data while preventing them from entering action coefficients that would generate an `R2/fR` scalar tower.",
        "",
        "Verdict: the `X_env/X_route` split is the right repair shape but is not source-signed in the current parent equations, which still write action-relevant coefficients as functions of unsplit `X_B`. The first symbolic `C_XR[A_curv]` row is now staged, with projection, norm-regularization, and active coefficient derivatives left explicit.",
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
    print(f"VAL1973_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
