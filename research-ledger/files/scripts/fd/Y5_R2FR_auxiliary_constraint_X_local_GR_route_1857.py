from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1857"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1857-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_SOURCE_REGISTER.csv",
    "conditional_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_CONSTRAINT_LOCAL_GR_CONDITIONAL_THEOREM.csv",
    "gate_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_CONSTRAINT_GATE_AUDIT.csv",
    "route_comparison": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_AUXILIARY_CONSTRAINT_ROUTE_COMPARISON.csv",
    "local_gr_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_LOCAL_GR_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1857_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1857_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1857_0_1856_handoff",
            "source_path": source_path("1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md"),
            "needle": "NEXT1856_0_primary",
            "use": "selected auxiliary/constraint local-GR route",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1857_1_first_class_contract",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv"),
            "needle": "FCC1555_7_no_GR_import",
            "use": "first-class constraint acceptance requirements",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1857_2_constraint_class",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv"),
            "needle": "CLASS1562_5_second_class",
            "use": "first-class vs second-class constraint class gate",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1857_3_constraint_action",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1668_CONSTRAINT_FIRST_ACTION_ATTEMPT.csv"),
            "needle": "CFA1668_8_verdict",
            "use": "constraint-first action attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1857_4_descent_theorem",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv"),
            "needle": "constraint_first_DqZ_zero_descent_theorem",
            "use": "conditional descent theorem attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1857_5_exclusion_gate",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1783_CONSTRAINT_FIRST_EXCLUSION_GATE.csv"),
            "needle": "CFE1783_7_verdict",
            "use": "constraint-first exclusion gate",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1857_6_nonprop_constraint",
            "source_path": source_path("07-nonpropagating-reciprocity-constraint.md"),
            "needle": "best route = hard constraint or phase-volume balance",
            "use": "nonpropagating reciprocity route",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1857_7_qmap_guard",
            "source_path": source_path("1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md"),
            "needle": "no local physical X mode",
            "use": "quotient/null guard for no physical scalar",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    theorem_rows = [
        {
            "theorem_id": "CLG1857_0_setup",
            "statement": "Let parent phase space P contain a residual coordinate Z/X and a constraint C_X(Phi)=0.",
            "mathematical_role": "defines the candidate nonpropagating local residual",
            "proof_status": "SETUP",
            "current_mts_status": "NEEDS_PARENT_PHASE_SPACE",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CLG1857_1_elimination_before_readout",
            "statement": "If C_X eliminates Z/X before physical phase space and before ordinary matter/readout functors are defined, then Dq(v_X)=0 for the eliminated direction.",
            "mathematical_role": "turns X from physical scalar hair into a null/removed representative",
            "proof_status": "CONDITIONAL_THEOREM_VALID",
            "current_mts_status": "NEEDS_CONSTRAINT_AND_Q_MAP",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CLG1857_2_first_class_case",
            "statement": "If G_X[epsilon] is differentiable, has zero/proper boundary charge, and closes first-class, then P_red=C_X^{-1}(0)/Gauge_X contains no physical X pair.",
            "mathematical_role": "removes local scalar degree by gauge quotient",
            "proof_status": "CONDITIONAL_THEOREM_VALID",
            "current_mts_status": "NEEDS_GENERATOR_BRACKET_BOUNDARY_DEGREE_COUNT",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CLG1857_3_second_class_auxiliary_case",
            "statement": "If X and its multiplier form an algebraic second-class auxiliary pair, solve them before phase space and substitute back into the action.",
            "mathematical_role": "removes local scalar degree by elimination rather than gauge",
            "proof_status": "CONDITIONAL_THEOREM_VALID",
            "current_mts_status": "NEEDS_ALGEBRAIC_SOLVE_AND_NO_NONLOCAL_TAIL",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CLG1857_4_matter_descent",
            "statement": "If S_matter and observed coframe depend only on reduced variables q(Phi), ordinary test bodies cannot source the eliminated X direction.",
            "mathematical_role": "prevents fifth-force/source charge return after elimination",
            "proof_status": "CONDITIONAL_THEOREM_VALID",
            "current_mts_status": "NEEDS_MATTER_READOUT_DESCENT",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CLG1857_5_local_GR_consequence",
            "statement": "If CLG1857_0 through CLG1857_4 all close, local GR/Newton can be the reduced branch without physical X scalar hair.",
            "mathematical_role": "local-GR theorem target",
            "proof_status": "EXACT_CONDITIONAL_TARGET",
            "current_mts_status": "FAIL_CURRENT_CLAIM_PREMISES_UNSIGNED",
            "valid_for_claim": False,
        },
    ]

    gate_rows = [
        {
            "gate_id": "CGA1857_0_parent_phase_space",
            "needed_gate": "parent phase space and symplectic form",
            "acceptance": "fields, symplectic/current form and constraints are declared without importing GR as conclusion",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CGA1857_1_constraint_equation",
            "needed_gate": "constraint equation C_X=0",
            "acceptance": "constraint follows from MTS parent action/motion-load/phase-volume law",
            "current_status": "PARENT_ORIGIN_OPEN",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CGA1857_2_generator",
            "needed_gate": "differentiable generator or algebraic auxiliary solve",
            "acceptance": "delta G_X is well-defined, or auxiliary equations solve locally without nonlocal tail",
            "current_status": "NOT_DERIVED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CGA1857_3_boundary_charge",
            "needed_gate": "zero/proper boundary charge",
            "acceptance": "Q_X is zero, exact, fixed, or retained as explicit boundary residual",
            "current_status": "BOUNDARY_SILENCE_UNSIGNED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CGA1857_4_bracket_degree",
            "needed_gate": "constraint class and degree count",
            "acceptance": "first-class pair removes two phase-space dimensions, or second-class auxiliary pair is eliminated",
            "current_status": "DEGREE_COUNT_NOT_CLOSED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CGA1857_5_matter_readout_descent",
            "needed_gate": "ordinary matter/readout descends after elimination",
            "acceptance": "S_matter=Sbar[q(Phi),Psi,theta] and no hidden marker/source tail returns",
            "current_status": "MATTER_DESCENT_UNSIGNED",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CGA1857_6_physical_component_lock",
            "needed_gate": "removed variable is exactly the dangerous local X/c_g direction",
            "acceptance": "physical-component lock maps the eliminated residual to the PPN/R10/local coupling direction",
            "current_status": "PHYSICAL_COMPONENT_LOCK_MISSING",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CGA1857_7_verdict",
            "needed_gate": "all constraint-first gates close",
            "acceptance": "CGA1857_0 through CGA1857_6 pass from one parent branch",
            "current_status": "FAIL_CURRENT_CLAIM",
            "blocks_local_gr_claim": True,
            "valid_for_claim": False,
        },
    ]

    route_rows = [
        {
            "route_id": "ACR1857_0_first_class",
            "route": "first-class quotient constraint",
            "strength": "best if generator/boundary/brackets close; clean no-hair by quotient",
            "weakness": "hardest algebra and boundary proof",
            "current_status": "CONDITIONAL_NOT_CLOSED",
            "next_requirement": "parent phase-space/generator/bracket package",
            "valid_for_claim": False,
        },
        {
            "route_id": "ACR1857_1_second_class_auxiliary",
            "route": "second-class algebraic auxiliary elimination",
            "strength": "simpler elimination if equations solve locally",
            "weakness": "can leave nonlocal tails or hidden source/readout terms",
            "current_status": "CONDITIONAL_NOT_CLOSED",
            "next_requirement": "local algebraic solve plus no-tail proof",
            "valid_for_claim": False,
        },
        {
            "route_id": "ACR1857_2_nonprop_reciprocity",
            "route": "hard nonpropagating reciprocity constraint",
            "strength": "closest to prior local metric reciprocity work",
            "weakness": "parent origin/multiplier still open",
            "current_status": "PROMISING_PARENT_ORIGIN_OPEN",
            "next_requirement": "derive from motion-load/phase-volume law",
            "valid_for_claim": False,
        },
        {
            "route_id": "ACR1857_3_current_selection",
            "route": "constraint-first proof package",
            "strength": "least dangerous route to derived local GR",
            "weakness": "still many unsigned gates",
            "current_status": "SELECT_FOR_NEXT_GATE_BUILD",
            "next_requirement": "build parent constraint package with no GR import",
            "valid_for_claim": False,
        },
    ]

    status_rows = [
        {
            "status_id": "LGS1857_0_physical_scalar",
            "branch": "physical scalar",
            "local_gr_status": "DEMOTED_TO_EFT_CLOSURE",
            "reason": "1856 rejected primitive derivation",
            "valid_for_claim": False,
        },
        {
            "status_id": "LGS1857_1_constraint",
            "branch": "constraint/auxiliary",
            "local_gr_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "reason": "1857 theorem is clean but gates fail current claim",
            "valid_for_claim": False,
        },
        {
            "status_id": "LGS1857_2_project",
            "branch": "overall local-GR route",
            "local_gr_status": "NARROWED_TO_CONSTRAINT_PACKAGE",
            "reason": "we now know the proof package required instead of chasing scalar coefficients",
            "valid_for_claim": False,
        },
    ]

    claim_rows = [
        {
            "gate_id": "CG1857_0_conditional_theorem",
            "claim": "constraint/auxiliary route has a valid conditional theorem shape",
            "gate_pass": True,
            "reason": "reduced phase space or algebraic elimination would remove physical X hair before readout",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1857_1_parent_constraint",
            "claim": "MTS parent action supplies the constraint",
            "gate_pass": False,
            "reason": "parent origin and no-GR-import proof remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1857_2_boundary_degree_matter",
            "claim": "boundary charge, degree count and matter descent all close",
            "gate_pass": False,
            "reason": "CGA1857 gates remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1857_3_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "gate_pass": False,
            "reason": "constraint theorem is conditional only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1857_0_theorem_status",
            "decision": "Constraint-first local GR is an exact conditional theorem target.",
            "because": "if X is eliminated before physical phase space and matter readout, there is no physical scalar hair to test locally.",
            "next_action": "build the parent constraint package rather than returning to physical scalar coefficients",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1857_1_current_block",
            "decision": "The route is not yet a local-GR derivation.",
            "because": "parent origin, generator/boundary/bracket/degree/matter descent and physical-component lock are unsigned.",
            "next_action": "derive or reject the parent constraint package",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1857_2_next",
            "decision": "Next target is the parent constraint package with no GR import.",
            "because": "that package is the bottleneck that decides whether the selected route is real MTS or another closure.",
            "next_action": "1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "route_id": "NEXT1857_0_primary",
            "next_target": "1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md",
            "script": "scripts/Y5_R2FR_parent_constraint_package_no_GR_import_gate_1858.py",
            "objective": "derive or reject the parent constraint package: phase space, constraint, generator/auxiliary solve, bracket/degree count, boundary charge, matter descent and no-GR-import proof",
            "selection_status": "selected",
            "success_condition": "constraint package closes from MTS primitives, or the constraint route is demoted to closure-only",
        },
        {
            "route_id": "NEXT1857_1_parallel",
            "next_target": "1858b-Y5-R2FR-motion-load-phase-volume-parent-origin.md",
            "script": "scripts/Y5_R2FR_motion_load_phase_volume_parent_origin_1858b.py",
            "objective": "derive the nonpropagating reciprocity constraint from motion-load/phase-volume balance",
            "selection_status": "held",
            "success_condition": "constraint multiplier/origin is derived without importing GR reciprocity as an axiom",
        },
    ]

    return {
        "source_register": source_rows,
        "conditional_theorem": theorem_rows,
        "gate_audit": gate_rows,
        "route_comparison": route_rows,
        "local_gr_status": status_rows,
        "claim_gate": claim_rows,
        "decision": decision_rows,
        "next_target": next_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1857_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1857 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1857_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1857_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1857_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1857_2_conditional_theorem",
            any(row["theorem_id"] == "CLG1857_5_local_GR_consequence" and row["proof_status"] == "EXACT_CONDITIONAL_TARGET" for row in rows_map["conditional_theorem"]),
            "local-GR conditional theorem target is present",
        )
    )
    checks.append(
        (
            "VAL1857_3_gate_audit_blocks",
            any(row["gate_id"] == "CGA1857_7_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["gate_audit"])
            and all(boolish(row["blocks_local_gr_claim"]) for row in rows_map["gate_audit"]),
            "all constraint gates block local-GR claim until signed",
        )
    )
    checks.append(
        (
            "VAL1857_4_route_selected",
            any(row["route_id"] == "ACR1857_3_current_selection" and row["current_status"] == "SELECT_FOR_NEXT_GATE_BUILD" for row in rows_map["route_comparison"]),
            "constraint-first proof package remains selected",
        )
    )
    checks.append(
        (
            "VAL1857_5_local_status_nonclaim",
            any(row["status_id"] == "LGS1857_1_constraint" and row["local_gr_status"] == "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED" for row in rows_map["local_gr_status"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["local_gr_status"]),
            "local-GR status remains conditional and nonclaim",
        )
    )
    checks.append(
        (
            "VAL1857_6_claim_gates_safe",
            any(row["gate_id"] == "CG1857_0_conditional_theorem" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1857_3_local_GR" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "conditional theorem gate passes but local-GR claim does not",
        )
    )
    checks.append(
        (
            "VAL1857_7_next_target_selected",
            any(row["route_id"] == "NEXT1857_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1857_8_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1857_9_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1857_10_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1857_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs = list(FORMALIZATION.rglob("*1857*")) if FORMALIZATION.exists() else []
    checks.append(("VAL1857_12_formalization_untouched", not formalization_outputs, "no 1857 outputs found under formalization-workbench"))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1857_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1857 auxiliary constraint X local-GR route",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1857: Auxiliary/Constraint X Local-GR Route",
            "",
            "**Current verdict:** the constraint/auxiliary route has a clean conditional theorem: if the residual is eliminated before physical phase space and ordinary matter readout, local scalar hair is absent and GR/Newton can be the reduced local branch. But the route is not yet proven for MTS: parent phase space, constraint origin, generator or auxiliary solve, boundary charge, degree count, matter descent and physical-component lock remain unsigned.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## Constraint Local-GR Conditional Theorem",
            markdown_table(rows_map["conditional_theorem"], ["theorem_id", "statement", "mathematical_role", "proof_status", "current_mts_status", "valid_for_claim"]),
            "",
            "## Constraint Gate Audit",
            markdown_table(rows_map["gate_audit"], ["gate_id", "needed_gate", "acceptance", "current_status", "blocks_local_gr_claim", "valid_for_claim"]),
            "",
            "## Auxiliary/Constraint Route Comparison",
            markdown_table(rows_map["route_comparison"], ["route_id", "route", "strength", "weakness", "current_status", "next_requirement", "valid_for_claim"]),
            "",
            "## Local-GR Status",
            markdown_table(rows_map["local_gr_status"], ["status_id", "branch", "local_gr_status", "reason", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the route we wanted: no fifth-force scalar to hide. But it is only earned if the constraint package is real. The next checkpoint should try to build that package without importing GR as the answer.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1857 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
