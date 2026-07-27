from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_POSITIVE_ACTIVATION_VECTOR_2257"
DOC = ROOT / "2257-Y5-R2FR-positive-RAB-working-branch-activation-vector.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2257_00_2256_doc",
        "source_key": "2256_handoff",
        "source_path": ROOT / "2256-Y5-R2FR-RAB-parent-route-selection-or-BWeyl-residual-branch.md",
        "needles": ["ROUTE2256_2_positive_sourcefree_physical_R", "ACTV2256_0_operator", "NEXT2256_0_primary"],
        "role": "selects the private positive source-free R_AB working branch and hands off to activation",
    },
    {
        "source_id": "SRC2257_01_2256_validation",
        "source_key": "2256_validation",
        "source_path": OUT / "P8_Y5_BRR545_2256_VALIDATION.csv",
        "needles": ["VAL2256_OVERALL", "PASS"],
        "role": "confirms 2256 passed before 2257 starts",
    },
    {
        "source_id": "SRC2257_02_2256_activation",
        "source_key": "2256_activation",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2256_POSITIVE_BRANCH_ACTIVATION_VECTOR.csv",
        "needles": ["ACTV2256_0_operator", "ACTV2256_6_verdict", "POSITIVE_BRANCH_NOT_ACTIVATED"],
        "role": "machine-readable activation vector inherited from 2256",
    },
    {
        "source_id": "SRC2257_03_2248_doc",
        "source_key": "2248_nohair",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["NH2248_3_zero_theorem", "RNH2248_5_verdict"],
        "role": "conditional energy/no-hair identity to activate if positivity, source, and boundary clauses close",
    },
    {
        "source_id": "SRC2257_04_2248_validation",
        "source_key": "2248_validation",
        "source_path": OUT / "P8_Y5_BRR545_2248_VALIDATION.csv",
        "needles": ["VAL2248_OVERALL", "PASS"],
        "role": "confirms the conditional no-hair identity passed as nonclaim",
    },
    {
        "source_id": "SRC2257_05_2247_template",
        "source_key": "2247_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_PR_TEMPLATE_CONTRACT.csv",
        "needles": ["TPR2247_4_positive_RAB_example", "FAIL_CURRENT_CLAIM_THETAR_PR_NOT_PARENT_OWNED"],
        "role": "candidate positive R_AB action skeleton and owner gap",
    },
    {
        "source_id": "SRC2257_06_2253_residuals",
        "source_key": "2253_curvature",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2253_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
        "needles": ["CURV2253_0_BWeyl", "CURV2253_1_BRic"],
        "role": "curvature residual rows that must be zeroed, diagonalized, or bounded",
    },
    {
        "source_id": "SRC2257_07_2254_weyl",
        "source_key": "2254_weyl",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2254_BWEYL_INDEX_ZERO_THEOREM_GATE.csv",
        "needles": ["WZ2254_0_conditional_theorem", "WZ2254_4_verdict"],
        "role": "conditional B_Weyl index-zero theorem that remains premise-unsigned",
    },
    {
        "source_id": "SRC2257_08_2255_fallback",
        "source_key": "2255_fallback",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2255_FALLBACK_RESIDUAL_ROWS.csv",
        "needles": ["FBR2255_0_BWeyl", "FBR2255_2_total"],
        "role": "fallback residual rows if theorem-zero routes fail",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2257_SOURCE_REGISTER.csv",
    "activation_audit": OUT / "P8_Y5_PARENT_QLOC_2257_ACTIVATION_GATE_AUDIT.csv",
    "operator_rows": OUT / "P8_Y5_PARENT_QLOC_2257_OPERATOR_SIGN_GAP_ROWS.csv",
    "queue": OUT / "P8_Y5_PARENT_QLOC_2257_SOURCE_BOUNDARY_CURVATURE_PROJECTION_QUEUE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2257_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2257_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2257_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2257_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2257_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2257_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_operator": QUEUE / "JR2257_RAB_OPERATOR_SIGN_GAP_NONCLAIM.csv",
    "queue_activation": QUEUE / "JR2257_POSITIVE_BRANCH_ACTIVATION_QUEUE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_positive_activation_nonclaim_2257.csv",
    "beta_docs": BETA_DOCS / "RAB_POSITIVE_ACTIVATION_2257_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def activation_gate_audit_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "ACT2257_0_operator",
            "operator positivity and gap",
            "Z_R>0, M_R^2>0, Hessian_R positive on the quotient, zero modes removed, local domain fixed",
            "MISSING_ZR_MR2_HESSIAN_ZERO_MODE_CERTIFICATE",
            "highest",
            "2258 sign/gap certificate",
            src("2256_activation", "2248_nohair", "2247_template"),
        ),
        (
            "ACT2257_1_source",
            "source-free local branch",
            "J_R_res=0 or bounded componentwise for C_RT, epsilon_source, Q_R_body, Pi_R, and tail_R",
            "MISSING_JR_ZERO_OR_COMPONENT_BOUNDS",
            "high",
            "held after operator sign/gap",
            src("2248_nohair", "2255_fallback"),
        ),
        (
            "ACT2257_2_boundary",
            "boundary flux silence",
            "Phi_boundary_local=0 or finite sourced boundary coefficient with sign-controlled contribution",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "high",
            "held after operator sign/gap",
            src("2248_nohair", "2255_fallback"),
        ),
        (
            "ACT2257_3_BWeyl",
            "Weyl/tidal curvature driving",
            "B_Weyl=0 by representation/no-spurion route or B_Weyl_effective_abs is numeric and bounded",
            "MISSING_BWEYL_ZERO_OR_BOUND",
            "medium",
            "carry in queue",
            src("2254_weyl", "2255_fallback", "2253_curvature"),
        ),
        (
            "ACT2257_4_BRic",
            "Ricci geometric mixing",
            "B_Ric is absorbed into the positive LHS operator by Schur/norm control or retained as finite residual",
            "MISSING_BRIC_DIAGONALIZATION_OR_BOUND",
            "medium",
            "carry in queue",
            src("2253_curvature"),
        ),
        (
            "ACT2257_5_projection",
            "observable projection cleanup",
            "R_AB=0 implies q_loc, PPN, R10, clock, and orbital residual silence or finite arena bounds",
            "MISSING_QLOC_PPN_R10_CLOCK_ORBITAL_PROJECTION",
            "medium",
            "carry in queue",
            src("2256_activation", "2255_fallback"),
        ),
        (
            "ACT2257_6_verdict",
            "positive R_AB branch activation",
            "all activation clauses pass together before local-GR/Newton/R10/PPN claim",
            "POSITIVE_BRANCH_NOT_ACTIVATED",
            "summary",
            "select operator sign/gap first",
            src("2256_activation"),
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "activation_id": activation_id,
            "gate": gate,
            "required_statement": required,
            "current_status": status,
            "priority": priority,
            "first_action": action,
            "source_paths": source_paths,
            "gate_pass": False,
            **false_flags(),
        }
        for activation_id, gate, required, status, priority, action, source_paths in entries
    ]


def operator_sign_gap_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "OPR2257_0_ZR",
            "Z_R",
            "kinetic sign",
            "parent quadratic R_AB sector has positive kinetic coefficient on the physical quotient",
            "MISSING_PARENT_ZR_VALUE_OR_THEOREM",
            "operator positivity",
        ),
        (
            "OPR2257_1_MR2",
            "M_R^2",
            "mass/gap sign",
            "parent Hessian gives nonnegative or positive local R_AB gap after gauge and zero-mode quotient",
            "MISSING_PARENT_MR2_VALUE_OR_GAP_THEOREM",
            "operator coercivity",
        ),
        (
            "OPR2257_2_Hessian_R",
            "Hessian_R",
            "second variation signature",
            "second variation of the parent route is positive on allowed compact-support perturbations",
            "MISSING_SECOND_VARIATION_SIGNATURE",
            "operator coercivity",
        ),
        (
            "OPR2257_3_zero_mode_rule",
            "zero_mode_rule",
            "kernel handling",
            "constant, gauge, topological, and boundary zero modes are removed or explicitly projected out",
            "MISSING_ZERO_MODE_AND_GAUGE_KERNEL_RULE",
            "no-hair activation",
        ),
        (
            "OPR2257_4_domain_gauge_quotient",
            "domain_gauge_quotient",
            "functional domain",
            "local vacuum domain, gauge slice, quotient map, and boundary conditions are fixed before integration by parts",
            "MISSING_DOMAIN_GAUGE_QUOTIENT_CERTIFICATE",
            "no-hair activation",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "operator_component": component,
            "role": role,
            "required_statement": required,
            "current_status": status,
            "target_gate": target_gate,
            "source_requirement": "parent route/action or explicit signed theorem, not phenomenological insertion",
            "source_paths": src("2248_nohair", "2247_template", "2256_activation"),
            "next_action": "2258-Y5-R2FR-RAB-ZR-MR2-sign-gap-and-zero-mode-certificate.md",
            **false_flags(),
        }
        for row_id, component, role, required, status, target_gate in entries
    ]


def source_boundary_queue_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "Q2257_0_JR",
            "J_R_res",
            "source vector",
            "prove local J_R_res=0 or retain componentwise bounds for C_RT, epsilon_source, Q_R_body, Pi_R, tail_R",
            "MISSING_SOURCE_VECTOR_ZERO_OR_BOUNDS",
            "source/local_GR/PPN/R10",
            src("2248_nohair", "2255_fallback"),
        ),
        (
            "Q2257_1_boundary",
            "Phi_boundary_local",
            "boundary flux",
            "prove boundary term vanishes under local vacuum support and asymptotic/compact boundary conditions",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "boundary/local_GR",
            src("2248_nohair"),
        ),
        (
            "Q2257_2_BWeyl",
            "B_Weyl_effective_abs",
            "Weyl curvature residual",
            "activate representation/no-spurion zero theorem or source numeric B_Weyl bound row",
            "MISSING_BWEYL_ZERO_OR_BOUND",
            "curvature/PPN/orbital/R10",
            src("2254_weyl", "2255_fallback", "2253_curvature"),
        ),
        (
            "Q2257_3_BRic",
            "B_Ric",
            "Ricci mixing residual",
            "diagonalize into positive LHS operator or retain finite residual bound",
            "MISSING_BRIC_DIAGONALIZATION_OR_BOUND",
            "curvature/local_GR/R10",
            src("2253_curvature"),
        ),
        (
            "Q2257_4_projection",
            "P_loc(R_AB residual)",
            "observable projection",
            "map any retained R_AB residual into q_loc, PPN, R10, clocks, and orbital observables",
            "MISSING_ARENA_PROJECTION_KERNELS",
            "q_loc/PPN/R10/clock/orbital",
            src("2256_activation", "2255_fallback"),
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "queue_id": queue_id,
            "object": object_name,
            "queue_type": queue_type,
            "required_statement": required,
            "current_status": status,
            "arena": arena,
            "source_paths": source_paths,
            "selected_now": queue_id == "Q2257_0_JR" and False,
            **false_flags(),
        }
        for queue_id, object_name, queue_type, required, status, arena, source_paths in entries
    ]


def refusal_rows() -> list[dict[str, Any]]:
    entries = [
        ("REF2257_0_positive_branch", "positive R_AB working branch activates", "BLOCKED", "ACT2257_6_verdict=POSITIVE_BRANCH_NOT_ACTIVATED"),
        ("REF2257_1_nohair", "local R_AB no-hair theorem is usable as theorem-zero", "BLOCKED", "operator/source/boundary clauses remain unsigned"),
        ("REF2257_2_local_GR", "derived local GR/Newton recovery", "BLOCKED", "no-hair plus projection cleanup not closed"),
        ("REF2257_3_BWeyl_zero", "B_Weyl=0", "BLOCKED", "representation/no-spurion premises remain unsigned"),
        ("REF2257_4_empirical_pass", "R10/PPN/clock/orbital pass", "BLOCKED", "numeric residual rows and arena kernels missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            **false_flags(),
        }
        for refusal_id, claim, result, blocked_by in entries
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2257_0_operator", "coercive R_AB operator", "Z_R/M_R^2/Hessian/zero-mode/domain package missing"),
        ("CG2257_1_source", "source-free local R_AB branch", "J_R_res zero theorem or component bounds missing"),
        ("CG2257_2_boundary", "boundary flux silence", "Phi_boundary_local zero or finite bound missing"),
        ("CG2257_3_curvature", "curvature residual cleanup", "B_Weyl and B_Ric zero/bound clauses missing"),
        ("CG2257_4_projection", "observable silence", "q_loc/PPN/R10/clock/orbital kernels missing"),
        ("CG2257_5_local_GR_Newton", "derived local GR/Newton recovery", "upstream activation vector remains blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            **false_flags(),
        }
        for claim_id, claim, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2257_0_status",
            "POSITIVE_RAB_BRANCH_NOT_ACTIVATED",
            "2257 ranks the activation vector but does not close any theorem-zero gate.",
            "keep branch private and nonclaim",
        ),
        (
            "DEC2257_1_first_gate",
            "OPERATOR_SIGN_GAP_FIRST",
            "the 2248 energy identity cannot be used until the quadratic form is coercive on the quotient.",
            "build Z_R/M_R^2/Hessian/zero-mode/domain certificate",
        ),
        (
            "DEC2257_2_queue",
            "SOURCE_BOUNDARY_CURVATURE_PROJECTION_QUEUE_RETAINED",
            "source, boundary, B_Weyl, B_Ric, and projection gates remain necessary but should not be attacked before positivity.",
            "carry nonclaim rows forward",
        ),
        (
            "DEC2257_3_next",
            "SIGN_GAP_AND_ZERO_MODE_CERTIFICATE_NEXT",
            "this is the least circular next proof target and the one most likely to turn the existing identity into a real theorem.",
            "2258-Y5-R2FR-RAB-ZR-MR2-sign-gap-and-zero-mode-certificate.md",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in entries
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2257_0_primary",
            "next_target": "2258-Y5-R2FR-RAB-ZR-MR2-sign-gap-and-zero-mode-certificate.md",
            "script": "scripts/Y5_R2FR_RAB_ZR_MR2_sign_gap_and_zero_mode_certificate_2258.py",
            "objective": "try to parent-sign Z_R, M_R^2, Hessian_R positivity, zero-mode removal, and the local quotient/domain needed by the 2248 no-hair identity",
            "selection_status": "selected",
            "success_condition": "operator coercivity becomes parent-signed, or the positive R_AB local-GR route is demoted to residual-only without a GR claim",
            "forbidden_claims": "local-GR/Newton/R10/PPN/WEP/clock/orbital pass; B_Weyl=0; source-free branch activation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2257_1_fallback",
            "next_target": "2258b-Y5-R2FR-positive-RAB-source-boundary-residual-runner.md",
            "script": "scripts/Y5_R2FR_positive_RAB_source_boundary_residual_runner_2258b.py",
            "objective": "if sign/gap cannot close, turn source, boundary, curvature, and projection queues into finite residual rows",
            "selection_status": "held_fallback",
            "success_condition": "all retained residuals have sourced numeric rows and explicit arena projection kernels",
            "forbidden_claims": "theorem-zero by placeholder; cancellation between residual channels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("operator", OUTPUTS["operator_rows"], COPY_TARGETS["queue_operator"], "operator sign/gap rows for the next proof target"),
        ("activation", OUTPUTS["queue"], COPY_TARGETS["queue_activation"], "positive branch source/boundary/curvature/projection nonclaim queue"),
        ("branch_wep", OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"], "branch-locked WEP/local residual claim refusal state"),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], "portable decision ledger for beta-source docs"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in copies:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2257_{copy_id}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_rows(paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    activation = read_csv(OUTPUTS["activation_audit"])
    operator_rows = read_csv(OUTPUTS["operator_rows"])
    queue = read_csv(OUTPUTS["queue"])
    refusals = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}

    csv_parse_ok = True
    for path in paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    formalization_2257 = []
    if FORMALIZATION.exists():
        formalization_2257 = [path for path in FORMALIZATION.rglob("*2257*") if path.is_file()]

    activation_ids = {row["activation_id"] for row in activation}
    operator_components = {row["operator_component"] for row in operator_rows}
    all_rows = [row for path in paths for row in read_csv(path)]

    rows = [
        check("VAL2257_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2257_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2257_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2248 and 2256 validations pass where checked"),
        check("VAL2257_3_activation_coverage", {"ACT2257_0_operator", "ACT2257_1_source", "ACT2257_2_boundary", "ACT2257_3_BWeyl", "ACT2257_4_BRic", "ACT2257_5_projection", "ACT2257_6_verdict"}.issubset(activation_ids), "activation audit covers operator/source/boundary/BWeyl/BRic/projection/verdict"),
        check("VAL2257_4_operator_rows_complete", {"Z_R", "M_R^2", "Hessian_R", "zero_mode_rule", "domain_gauge_quotient"}.issubset(operator_components), "operator sign/gap rows include all required first-gate components"),
        check("VAL2257_5_no_activation_passes", all(row["gate_pass"] == "False" for row in activation), "no positive branch activation gate is marked passed"),
        check("VAL2257_6_queue_retained", len(queue) == 5 and all(row["valid_for_claim"] == "False" for row in queue), "source/boundary/curvature/projection queue retained as nonclaim"),
        check("VAL2257_7_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2257_8_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2257_9_decision_first_gate", any(row["decision_id"] == "DEC2257_1_first_gate" and row["decision"] == "OPERATOR_SIGN_GAP_FIRST" for row in decisions), "decision selects operator sign/gap as first gate"),
        check("VAL2257_10_next_selected", any(row["route_id"] == "NEXT2257_0_primary" and row["selection_status"] == "selected" and "sign-gap" in row["script"].lower().replace("_", "-") for row in next_targets), "next target selected as sign/gap certificate"),
        check("VAL2257_11_csv_parse", csv_parse_ok, "all generated 2257 CSVs parse"),
        check("VAL2257_12_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        check("VAL2257_13_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2257_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2257_15_formalization_no_2257", not formalization_2257, "formalization-workbench has no 2257 outputs"),
    ]
    rows.append(
        check(
            "VAL2257_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2257 ranks the positive R_AB activation vector, refuses all local-GR/no-hair/observable claims, and selects Z_R/M_R^2 sign-gap plus zero-mode certificate next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    activation: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2257 - Y5/R2FR Positive R_AB Working Branch Activation Vector",
            "## Verdict\n\n2257 does not activate the local positive `R_AB` branch. It turns the 2256 route choice into a ranked activation vector and selects the least circular first attack: the operator sign/gap certificate for `Z_R`, `M_R^2`, the second-variation Hessian, zero-mode removal, and the local gauge/domain quotient.\n\nThis keeps the branch alive without smuggling in the plateau/no-hair conclusion. The 2248 energy identity is useful, but only after the quadratic form is parent-signed as coercive. Until then, source silence, boundary silence, `B_Weyl`, `B_Ric`, and observable projections remain explicit nonclaim queues.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Activation Gate Audit\n" + markdown_table(activation, ["activation_id", "gate", "required_statement", "current_status", "priority", "first_action", "gate_pass", "valid_for_claim"]),
            "## Operator Sign/Gap Rows\n" + markdown_table(operator_rows, ["row_id", "operator_component", "role", "required_statement", "current_status", "target_gate", "next_action", "valid_for_claim"]),
            "## Source/Boundary/Curvature/Projection Queue\n" + markdown_table(queue, ["queue_id", "object", "queue_type", "required_statement", "current_status", "arena", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is a forward move, not another circle. We are not saying `R_AB` vanishes; we are identifying the one clause that must be true before the no-hair identity can do honest work. If 2258 signs the operator package, the branch becomes a serious local-GR derivation route. If 2258 fails, we demote cleanly into a residual/bound programme instead of pretending the plateau was proved.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    activation = activation_gate_audit_rows()
    operator_rows = operator_sign_gap_rows()
    queue = source_boundary_queue_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["activation_audit"], activation)
    write_csv(OUTPUTS["operator_rows"], operator_rows)
    write_csv(OUTPUTS["queue"], queue)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["activation_audit"],
        OUTPUTS["operator_rows"],
        OUTPUTS["queue"],
        OUTPUTS["refusal"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]

    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)

    DOC.write_text(
        build_doc(source_rows, activation, operator_rows, queue, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2257 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
