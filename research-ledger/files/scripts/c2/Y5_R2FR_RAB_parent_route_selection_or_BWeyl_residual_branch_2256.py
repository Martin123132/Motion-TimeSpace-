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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_ROUTE_SELECTION_2256"
DOC = ROOT / "2256-Y5-R2FR-RAB-parent-route-selection-or-BWeyl-residual-branch.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2256_00_2255_doc",
        "source_key": "2255_handoff",
        "source_path": ROOT / "2255-Y5-R2FR-RAB-field-content-and-no-spurion-certificate.md",
        "needles": ["DEC2255_3_next", "NEXT2255_0_primary"],
        "role": "selects parent route selection or B_Weyl residual branch",
    },
    {
        "source_id": "SRC2256_01_2255_validation",
        "source_key": "2255_validation",
        "source_path": OUT / "P8_Y5_BRR545_2255_VALIDATION.csv",
        "needles": ["VAL2255_OVERALL", "PASS"],
        "role": "confirms 2255 passed before 2256 starts",
    },
    {
        "source_id": "SRC2256_02_2255_field",
        "source_key": "2255_field",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2255_FIELD_CONTENT_CERTIFICATE_ATTEMPT.csv",
        "needles": ["FCC2255_0_route_selection", "FCC2255_5_verdict"],
        "role": "field-content certificate blocked by route selection",
    },
    {
        "source_id": "SRC2256_03_2255_fallback",
        "source_key": "2255_fallback",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2255_FALLBACK_RESIDUAL_ROWS.csv",
        "needles": ["FBR2255_0_BWeyl", "FBR2255_2_total"],
        "role": "B_Weyl fallback residual if route cannot close",
    },
    {
        "source_id": "SRC2256_04_2247_doc",
        "source_key": "2247_parent_R",
        "source_path": ROOT / "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md",
        "needles": ["RC2247_0_absent_quotient", "RC2247_2_positive_sourcefree_physical_R", "RC2247_3_sourced_residual"],
        "role": "parent R_AB route menu",
    },
    {
        "source_id": "SRC2256_05_2247_classifier",
        "source_key": "2247_classifier",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_PARENT_R_CANDIDATE_CLASSIFIER.csv",
        "needles": ["RC2247_0_absent_quotient", "RC2247_1_first_class_vertical_constraint", "RC2247_2_positive_sourcefree_physical_R"],
        "role": "machine-readable route candidates",
    },
    {
        "source_id": "SRC2256_06_2247_template",
        "source_key": "2247_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_PR_TEMPLATE_CONTRACT.csv",
        "needles": ["TPR2247_4_positive_RAB_example", "TPR2247_5_verdict"],
        "role": "positive R_AB example and owner verdict",
    },
    {
        "source_id": "SRC2256_07_2248_doc",
        "source_key": "2248_nohair",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["NH2248_3_zero_theorem", "RNH2248_5_verdict"],
        "role": "conditional no-hair identity for positive R_AB route",
    },
    {
        "source_id": "SRC2256_08_2248_validation",
        "source_key": "2248_validation",
        "source_path": OUT / "P8_Y5_BRR545_2248_VALIDATION.csv",
        "needles": ["VAL2248_OVERALL", "PASS"],
        "role": "confirms 2248 conditional identity passed",
    },
    {
        "source_id": "SRC2256_09_2253_residuals",
        "source_key": "2253_residuals",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2253_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
        "needles": ["CURV2253_0_BWeyl", "CURV2253_1_BRic"],
        "role": "curvature residuals carried into route choice",
    },
    {
        "source_id": "SRC2256_10_2254_weyl",
        "source_key": "2254_weyl",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2254_BWEYL_INDEX_ZERO_THEOREM_GATE.csv",
        "needles": ["WZ2254_0_conditional_theorem", "WZ2254_4_verdict"],
        "role": "conditional B_Weyl zero theorem remains inactive",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2256_SOURCE_REGISTER.csv",
    "route_matrix": OUT / "P8_Y5_PARENT_QLOC_2256_RAB_PARENT_ROUTE_MATRIX.csv",
    "working_selection": OUT / "P8_Y5_PARENT_QLOC_2256_WORKING_BRANCH_SELECTION.csv",
    "activation_vector": OUT / "P8_Y5_PARENT_QLOC_2256_POSITIVE_BRANCH_ACTIVATION_VECTOR.csv",
    "bweyl_policy": OUT / "P8_Y5_PARENT_QLOC_2256_BWEYL_RESIDUAL_POLICY.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2256_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2256_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2256_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2256_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2256_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2256_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_routes": QUEUE / "JR2256_RAB_ROUTE_SELECTION_NONCLAIM.csv",
    "queue_positive": QUEUE / "JR2256_POSITIVE_RAB_ACTIVATION_VECTOR_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_route_selection_BWeyl_policy_nonclaim_2256.csv",
    "beta_docs": BETA_DOCS / "RAB_ROUTE_SELECTION_2256_NONCLAIM.csv",
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
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
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
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def route_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ROUTE2256_0_absent_quotient",
            "R_AB absent/nonprimitive quotient artefact",
            "would kill R_AB before variation and make B_Weyl irrelevant",
            "best theorem outcome, but no source proves nonprimitive status",
            "NOT_PARENT_SIGNED",
            "MISSING_NONPRIMITIVE_QUOTIENT_PROOF",
            "held_best_if_proved",
        ),
        (
            "ROUTE2256_1_first_class_constraint",
            "R_AB first-class vertical gauge/constraint direction",
            "would remove physical R_AB Green function if Omega/momentum-map constraints close",
            "promising active route, but Omega, D C_R, bracket closure, degree count and matter descent missing",
            "NOT_PARENT_SIGNED",
            "MISSING_FIRST_CLASS_CONSTRAINT_PACKAGE",
            "held_high_value",
        ),
        (
            "ROUTE2256_2_positive_sourcefree_physical_R",
            "R_AB positive physical operator but source-free in local branch",
            "keeps a physical R_AB field but allows no-hair collapse if operator/source/boundary gates close",
            "most concrete derivation working branch because 2248 has a conditional energy/no-hair identity",
            "WORKING_BRANCH_SELECTED_NONCLAIM",
            "MISSING_OPERATOR_SOURCE_BOUNDARY_CURVATURE_PACKAGE",
            "selected_private_working_branch",
        ),
        (
            "ROUTE2256_3_sourced_residual",
            "R_AB physical sourced residual",
            "turns local branch into empirical residual/fifth-force framework",
            "valid fallback if source-free or constraint routes fail; not a local-GR derivation by itself",
            "FALLBACK_ONLY",
            "MISSING_NUMERIC_SOURCE_VECTOR_AND_ARENA_KERNELS",
            "held_empirical_fallback",
        ),
        (
            "ROUTE2256_4_universal_conformal",
            "matter sees exp(2 a R)g or R_AB-dependent frame",
            "creates fifth-force/shadow-frame countermodel unless a=0 is derived",
            "countermodel, not a solution to local GR",
            "REJECT_AS_GR_DERIVATION_ROUTE",
            "MISSING_A_ZERO_THEOREM",
            "not_selected",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "what_it_would_do": effect,
            "current_evidence": evidence,
            "selection_status": status,
            "missing_for_claim": missing,
            "policy": policy,
            "source_paths": src("2247_parent_R", "2247_classifier", "2247_template", "2248_nohair"),
            **false_flags(),
        }
        for route_id, route, effect, evidence, status, missing, policy in rows
    ]


def working_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "selection_id": "SEL2256_0_claim_grade",
            "selected_route": "none",
            "selection_type": "claim_grade_parent_route",
            "selection_status": "NO_ROUTE_PARENT_SIGNED",
            "reason": "all 2247 route candidates still miss parent owner gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "selection_id": "SEL2256_1_working_branch",
            "selected_route": "ROUTE2256_2_positive_sourcefree_physical_R",
            "selection_type": "private_derivation_working_branch",
            "selection_status": "SELECTED_NONCLAIM",
            "reason": "it is the only route with an already written conditional energy/no-hair identity and an explicit activation vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "selection_id": "SEL2256_2_empirical_fallback",
            "selected_route": "ROUTE2256_3_sourced_residual",
            "selection_type": "fallback_if_positive_branch_fails",
            "selection_status": "HELD_FALLBACK_NONCLAIM",
            "reason": "if no theorem route closes, B_Weyl/source-vector residuals become empirical rows rather than a GR derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def activation_vector_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACTV2256_0_operator",
            "positive/coercive R_AB operator",
            "Z_R>0, M_R^2>0, zero modes removed, gauge/quotient domain fixed",
            "MISSING_ZR_MR2_SIGN_GAP_AND_ZERO_MODE_RULE",
        ),
        (
            "ACTV2256_1_source",
            "source-free local branch",
            "J_R_res=0 including C_RT, epsilon_source, Q_R_body, Pi_R, tail_R",
            "MISSING_SOURCE_VECTOR_ZERO_OR_BOUNDS",
        ),
        (
            "ACTV2256_2_boundary",
            "boundary flux silence",
            "Phi_boundary_local=0 or sourced finite boundary coefficient",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
        ),
        (
            "ACTV2256_3_BWeyl",
            "Weyl/tidal curvature driving removed or bounded",
            "B_Weyl=0 by route/type/no-spurion theorem, or B_Weyl_effective_abs is bounded",
            "MISSING_BWEYL_ZERO_OR_BOUND",
        ),
        (
            "ACTV2256_4_BRic",
            "Ricci geometric mixing diagonalized",
            "B_Ric is positive LHS operator deformation by Schur/norm condition or residual-bounded",
            "MISSING_BRIC_DIAGONALIZATION_OR_BOUND",
        ),
        (
            "ACTV2256_5_projection",
            "R_AB=0 projects to local observable silence",
            "q_loc/PPN/R10/clock/orbital projection tails vanish or are bounded",
            "MISSING_OBSERVABLE_PROJECTION_CLEANUP",
        ),
        (
            "ACTV2256_6_verdict",
            "positive R_AB working branch activation",
            "all activation rows pass together before no-hair/local-GR claim",
            "POSITIVE_BRANCH_NOT_ACTIVATED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "activation_id": activation_id,
            "gate": gate,
            "required_statement": required,
            "current_status": status,
            "gate_pass": False,
            "source_paths": src("2248_nohair", "2255_fallback", "2253_residuals", "2254_weyl"),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for activation_id, gate, required, status in rows
    ]


def bweyl_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "policy_id": "BWP2256_0_zero_route",
            "object": "B_Weyl",
            "policy": "zero only if absent/constraint route signs nonphysical R_AB, or positive branch signs field-content/no-spurion/index theorem",
            "current_status": "ZERO_NOT_ACTIVATED",
            "next_requirement": "parent route selection plus type/no-spurion certificate",
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "BWP2256_1_bound_route",
            "object": "B_Weyl_effective_abs",
            "policy": "if theorem route fails, carry |B_Weyl|+|epsilon_spurion_W| as empirical residual with arena projections",
            "current_status": "RESIDUAL_BRANCH_STAGED_NONCLAIM",
            "next_requirement": "numeric/source-backed bound and tau_Weyl_local kernel",
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "BWP2256_2_no_cancellation",
            "object": "curvature_source_residual_abs",
            "policy": "no cancellation credit between B_Ric, B_Weyl, C_RT, body, boundary, or tail channels",
            "current_status": "GUARD_ACTIVE",
            "next_requirement": "absolute component bounds or theorem-zero certificates",
            **false_flags(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2256_0_claim_route", "claim-grade R_AB parent route selected", "BLOCKED", "SEL2256_0_claim_grade=NO_ROUTE_PARENT_SIGNED"),
        ("REF2256_1_positive_activation", "positive no-hair branch activates", "BLOCKED", "ACTV2256_6_verdict=POSITIVE_BRANCH_NOT_ACTIVATED"),
        ("REF2256_2_BWeyl_zero", "B_Weyl=0 theorem active", "BLOCKED", "BWP2256_0_zero_route=ZERO_NOT_ACTIVATED"),
        ("REF2256_3_empirical_residual", "B_Weyl residual score-ready", "BLOCKED", "numeric/source-backed bound and arena kernels missing"),
        ("REF2256_4_local_GR", "derived local GR/Newton branch", "BLOCKED", "route/operator/source/boundary/curvature/projection gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, claim, result, blocked_by in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2256_0_route", "claim-grade R_AB parent route", "no route is parent-signed"),
        ("CG2256_1_positive_branch", "positive source-free R_AB branch activated", "operator/source/boundary/curvature/projection vector incomplete"),
        ("CG2256_2_BWeyl", "B_Weyl zero or bound-ready", "zero theorem inactive and numeric bound missing"),
        ("CG2256_3_local_nohair", "local R_AB no-hair activates", "2248 premises not all signed"),
        ("CG2256_4_local_GR_Newton", "derived local GR/Newton recovery", "no-hair and projection cleanup remain blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2256_0_no_public_route",
            "decision": "NO_RAB_PARENT_ROUTE_CLAIM_SELECTED",
            "reason": "2247 route candidates are informative but none passes parent owner gates.",
            "next_action": "keep local-GR/R10/PPN claims blocked",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2256_1_working_branch",
            "decision": "POSITIVE_SOURCEFREE_RAB_SELECTED_AS_PRIVATE_WORKING_BRANCH",
            "reason": "it is the only route with a concrete conditional energy/no-hair identity already written; this is movement toward derivable GR without claiming success.",
            "next_action": "attack activation vector row by row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2256_2_BWeyl",
            "decision": "BWEYL_REMAINS_ZERO_OR_BOUND_FORK",
            "reason": "positive branch still needs B_Weyl zero by type/no-spurion theorem or a finite residual bound.",
            "next_action": "carry B_Weyl_effective_abs in activation vector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2256_3_next",
            "decision": "POSITIVE_BRANCH_ACTIVATION_VECTOR_NEXT",
            "reason": "with the working route chosen, the least circular next step is to attack the activation vector rather than re-audit the route menu.",
            "next_action": "2257-Y5-R2FR-positive-RAB-working-branch-activation-vector.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2256_0_primary",
            "next_target": "2257-Y5-R2FR-positive-RAB-working-branch-activation-vector.md",
            "script": "scripts/Y5_R2FR_positive_RAB_working_branch_activation_vector_2257.py",
            "objective": "attack the positive source-free R_AB working branch activation vector: operator positivity, source silence, boundary flux, B_Weyl zero/bound, B_Ric diagonalization, and observable projection cleanup",
            "selection_status": "selected",
            "success_condition": "at least one activation component becomes theorem-zero/source-backed, or the finite residual row is explicitly retained without local-GR claim",
            "forbidden_shortcuts": "claim-grade route selection; assuming B_Weyl zero; deleting body/boundary tails; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2256_1_fallback",
            "next_target": "2257b-Y5-R2FR-BWeyl-effective-bound-runner.md",
            "script": "scripts/Y5_R2FR_BWeyl_effective_bound_runner_2257b.py",
            "objective": "if activation stalls, build executable B_Weyl_effective_abs refusal/bound runner",
            "selection_status": "held_fallback",
            "success_condition": "runner refuses missing rows and accepts only numeric, sourced, unit-matched residual bounds",
            "forbidden_shortcuts": "zero priors; tau=1; residual cancellation",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_routes", OUTPUTS["route_matrix"], COPY_TARGETS["queue_routes"], "R_AB route selection nonclaim queue"),
        ("queue_positive", OUTPUTS["activation_vector"], COPY_TARGETS["queue_positive"], "positive branch activation vector nonclaim queue"),
        ("branch_wep", OUTPUTS["bweyl_policy"], COPY_TARGETS["branch_wep"], "WEP branch locked B_Weyl policy copy"),
        ("beta_docs", OUTPUTS["route_matrix"], COPY_TARGETS["beta_docs"], "beta-source docs route selection copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2256_{copy_id}",
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
    routes = read_csv(OUTPUTS["route_matrix"])
    selections = read_csv(OUTPUTS["working_selection"])
    activation = read_csv(OUTPUTS["activation_vector"])
    bweyl = read_csv(OUTPUTS["bweyl_policy"])
    refusals = read_csv(OUTPUTS["runner_refusal"])
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

    formalization_2256 = []
    if FORMALIZATION.exists():
        formalization_2256 = [path for path in FORMALIZATION.rglob("*2256*") if path.is_file()]

    all_rows = [row for path in paths for row in read_csv(path)]
    rows = [
        check("VAL2256_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2256_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2256_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2255 and 2248 validations pass where checked"),
        check("VAL2256_3_route_menu_complete", len(routes) == 5 and any(row["route_id"] == "ROUTE2256_2_positive_sourcefree_physical_R" for row in routes), "all 2247 route candidates represented"),
        check("VAL2256_4_no_claim_route", any(row["selection_id"] == "SEL2256_0_claim_grade" and row["selection_status"] == "NO_ROUTE_PARENT_SIGNED" for row in selections), "no claim-grade route selected"),
        check("VAL2256_5_working_branch_selected", any(row["selection_id"] == "SEL2256_1_working_branch" and row["selection_status"] == "SELECTED_NONCLAIM" for row in selections), "positive source-free R_AB selected as nonclaim working branch"),
        check("VAL2256_6_activation_vector_blocks", any(row["activation_id"] == "ACTV2256_6_verdict" and row["current_status"] == "POSITIVE_BRANCH_NOT_ACTIVATED" for row in activation), "positive branch activation vector remains blocked"),
        check("VAL2256_7_bweyl_policy", any(row["policy_id"] == "BWP2256_0_zero_route" and row["current_status"] == "ZERO_NOT_ACTIVATED" for row in bweyl), "B_Weyl zero policy remains inactive"),
        check("VAL2256_8_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2256_9_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2256_10_decision_next", any(row["decision_id"] == "DEC2256_3_next" and "POSITIVE_BRANCH" in row["decision"] for row in decisions), "decision selects positive branch activation vector next"),
        check("VAL2256_11_next_selected", any(row["route_id"] == "NEXT2256_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2256_12_csv_parse", csv_parse_ok, "all generated 2256 CSVs parse"),
        check("VAL2256_13_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        check("VAL2256_14_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2256_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2256_16_formalization_no_2256", not formalization_2256, "formalization-workbench has no 2256 outputs"),
    ]
    rows.append(
        check(
            "VAL2256_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2256 refuses claim-grade R_AB route selection, selects positive source-free R_AB as private working branch, keeps B_Weyl zero/bound fork, and selects activation vector next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    selections: list[dict[str, Any]],
    activation: list[dict[str, Any]],
    bweyl: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2256 - Y5/R2FR R_AB Parent Route Selection Or B_Weyl Residual Branch",
            "## Verdict\n\n2256 does not select a claim-grade parent route. The 2247 menu still has no fully signed route: absent quotient is best if proved, first-class constraint is powerful but missing its symplectic package, positive source-free physical `R_AB` has the strongest concrete no-hair machinery, and sourced residual is empirical fallback only.\n\nThe useful decision is private and disciplined: select the positive source-free physical `R_AB` route as the working derivation branch, not as a claim. That lets the project move forward into an activation vector: operator positivity, source silence, boundary flux, `B_Weyl` zero/bound, `B_Ric` diagonalization, and projection cleanup. If that activation vector fails, the residual branch is already explicit.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## R_AB Parent Route Matrix\n" + markdown_table(routes, ["route_id", "route", "what_it_would_do", "current_evidence", "selection_status", "missing_for_claim", "policy", "valid_for_claim"]),
            "## Working Branch Selection\n" + markdown_table(selections, ["selection_id", "selected_route", "selection_type", "selection_status", "reason", "valid_for_claim"]),
            "## Positive Branch Activation Vector\n" + markdown_table(activation, ["activation_id", "gate", "required_statement", "current_status", "gate_pass", "valid_for_claim"]),
            "## B_Weyl Residual Policy\n" + markdown_table(bweyl, ["policy_id", "object", "policy", "current_status", "next_requirement", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is the right kind of leap, not a circle. We have not proved local GR, but we have stopped hovering over the route menu. The positive no-hair branch is now the private workbench route because it has a real energy identity. The next proof attempt should attack one activation component at a time. If one component closes, the branch gets sharper; if none close, the same document tells us exactly how to demote to a bounded residual theory.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    write_csv(OUTPUTS["source_register"], source_rows)

    routes = route_matrix_rows()
    selections = working_selection_rows()
    activation = activation_vector_rows()
    bweyl = bweyl_policy_rows()
    refusals = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["route_matrix"], routes)
    write_csv(OUTPUTS["working_selection"], selections)
    write_csv(OUTPUTS["activation_vector"], activation)
    write_csv(OUTPUTS["bweyl_policy"], bweyl)
    write_csv(OUTPUTS["runner_refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["route_matrix"],
        OUTPUTS["working_selection"],
        OUTPUTS["activation_vector"],
        OUTPUTS["bweyl_policy"],
        OUTPUTS["runner_refusal"],
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
        build_doc(source_rows, routes, selections, activation, bweyl, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2256 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
