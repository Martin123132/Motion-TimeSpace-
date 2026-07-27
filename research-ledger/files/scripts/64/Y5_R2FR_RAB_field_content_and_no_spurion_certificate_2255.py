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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_FIELD_CONTENT_NO_SPURION_2255"
DOC = ROOT / "2255-Y5-R2FR-RAB-field-content-and-no-spurion-certificate.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2255_00_2254_doc",
        "source_key": "2254_handoff",
        "source_path": ROOT / "2254-Y5-R2FR-RAB-representation-certificate-or-BWeyl-bound-row.md",
        "needles": ["DEC2254_3_next", "NEXT2254_0_primary"],
        "role": "selects field-content and no-spurion certificate",
    },
    {
        "source_id": "SRC2255_01_2254_validation",
        "source_key": "2254_validation",
        "source_path": OUT / "P8_Y5_BRR545_2254_VALIDATION.csv",
        "needles": ["VAL2254_OVERALL", "PASS"],
        "role": "confirms 2254 passed before 2255 starts",
    },
    {
        "source_id": "SRC2255_02_2254_certificate",
        "source_key": "2254_certificate",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2254_RAB_REPRESENTATION_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CERT2254_1_field_bundle", "CERT2254_5_verdict"],
        "role": "incoming representation certificate blockers",
    },
    {
        "source_id": "SRC2255_03_2254_weyl",
        "source_key": "2254_weyl",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2254_BWEYL_INDEX_ZERO_THEOREM_GATE.csv",
        "needles": ["WZ2254_0_conditional_theorem", "WZ2254_4_verdict"],
        "role": "conditional B_Weyl index-zero theorem",
    },
    {
        "source_id": "SRC2255_04_2247_doc",
        "source_key": "2247_parent_R",
        "source_path": ROOT / "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md",
        "needles": ["TOG2247_1_field_content", "RC2247_2_positive_sourcefree_physical_R"],
        "role": "parent R route and field-content owner gate",
    },
    {
        "source_id": "SRC2255_05_2247_template",
        "source_key": "2247_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_PR_TEMPLATE_CONTRACT.csv",
        "needles": ["TPR2247_3_Noether_PR", "TPR2247_4_positive_RAB_example"],
        "role": "Theta_R/P_R template and candidate field variable",
    },
    {
        "source_id": "SRC2255_06_2247_classifier",
        "source_key": "2247_classifier",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_PARENT_R_CANDIDATE_CLASSIFIER.csv",
        "needles": ["RC2247_0_absent_quotient", "RC2247_2_positive_sourcefree_physical_R"],
        "role": "candidate route menu; no route selected",
    },
    {
        "source_id": "SRC2255_07_1761_spurion",
        "source_key": "1761_spurion",
        "source_path": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
        "needles": ["DV1761_3_shadow_frame", "SP1761_4_hidden_frame"],
        "role": "hidden frame/projector/spurion countermodel",
    },
    {
        "source_id": "SRC2255_08_1768_normal",
        "source_key": "1768_normal_form",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["SCL1768_2_nonminimal_coupling", "SCL1768_5_post_variation_projector"],
        "role": "normal-form ledger retaining nonminimal/projector channels",
    },
    {
        "source_id": "SRC2255_09_2248_nohair",
        "source_key": "2248_nohair",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["NH2248_0_candidate_sector", "RNH2248_5_verdict"],
        "role": "positive source-free route remains conditional",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2255_SOURCE_REGISTER.csv",
    "field_content": OUT / "P8_Y5_PARENT_QLOC_2255_FIELD_CONTENT_CERTIFICATE_ATTEMPT.csv",
    "no_spurion": OUT / "P8_Y5_PARENT_QLOC_2255_NO_WEYL_SPURION_AUDIT.csv",
    "activation": OUT / "P8_Y5_PARENT_QLOC_2255_BWEYL_ZERO_ACTIVATION_GATE.csv",
    "fallback": OUT / "P8_Y5_PARENT_QLOC_2255_FALLBACK_RESIDUAL_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2255_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2255_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2255_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2255_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2255_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2255_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_field": QUEUE / "JR2255_FIELD_CONTENT_NO_SPURION_CERTIFICATE_NONCLAIM.csv",
    "queue_fallback": QUEUE / "JR2255_BWEYL_FALLBACK_RESIDUAL_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_field_content_no_spurion_nonclaim_2255.csv",
    "beta_docs": BETA_DOCS / "RAB_FIELD_CONTENT_NO_SPURION_2255_NONCLAIM.csv",
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


def field_content_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FCC2255_0_route_selection",
            "select parent R_AB route before representation certificate",
            "one of absent quotient, first-class vertical constraint, positive source-free field, or sourced residual",
            "NOT_SELECTED",
            "MISSING_PARENT_ROUTE_SELECTION",
        ),
        (
            "FCC2255_1_candidate_bundle",
            "candidate non-Weyl finite-sector bundle",
            "if RC2247_2 is selected, take R_AB as Y_R^A in a finite internal/vertical bundle with spacetime scalar or trace/Ricci-type amplitude",
            "CANDIDATE_DECLARED_NOT_PARENT_SIGNED",
            "MISSING_PARENT_SELECTION_AND_BUNDLE_DECLARATION",
        ),
        (
            "FCC2255_2_indices",
            "AB labels are internal/sector/generator labels",
            "AB is treated as a vertical/generator label in P_R^{mu AB}, not as a spacetime Weyl/Riemann four-index pair",
            "PLAUSIBLE_FROM_TPR2247_NOT_CERTIFIED",
            "MISSING_INDEX_CONVENTION_CERTIFICATE",
        ),
        (
            "FCC2255_3_transform_law",
            "transformation law",
            "R_AB transforms as scalar/internal finite-sector variable or trace/Ricci-type object under spacetime diffeomorphisms",
            "NOT_DECLARED",
            "MISSING_DIFF_LORENTZ_INTERNAL_TRANSFORM_RULE",
        ),
        (
            "FCC2255_4_no_four_index_field",
            "no Weyl/Riemann-type four-index field content",
            "R_AB has no C_{mu nu rho sigma}-type representation and no four-index parent slot",
            "NOT_CERTIFIED",
            "MISSING_NO_WEYL_REPRESENTATION_CERTIFICATE",
        ),
        (
            "FCC2255_5_verdict",
            "field-content certificate",
            "FCC2255_0 through FCC2255_4 close together",
            "FAIL_CURRENT_CLAIM",
            "FIELD_CONTENT_CERTIFICATE_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "certificate_piece": piece,
            "required_statement": required,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("2247_parent_R", "2247_template", "2247_classifier", "2254_certificate"),
            **false_flags(),
        }
        for certificate_id, piece, required, status, missing in rows
    ]


def no_spurion_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NSP2255_0_hidden_frame",
            "hidden conformal/disformal frame with Weyl-sensitive projector",
            "1761 keeps hidden frame channel live",
            "COUNTERMODEL_SURVIVES",
            "MISSING_NO_HIDDEN_FRAME_THEOREM",
        ),
        (
            "NSP2255_1_post_variation_projector",
            "post-variation material/geometric projector supplies Weyl indices",
            "1768 keeps post-variation projector forbidden by contract but unsigned",
            "COUNTERMODEL_SURVIVES",
            "MISSING_PROJECTOR_IDENTITY_THEOREM",
        ),
        (
            "NSP2255_2_history_kernel",
            "history/readout kernel carries tidal/Weyl tensor support",
            "tail_R channel from 2252/2253 remains open",
            "COUNTERMODEL_SURVIVES",
            "MISSING_HISTORY_READOUT_NO_SPURION",
        ),
        (
            "NSP2255_3_boundary_support",
            "boundary/source support imports Weyl-type normal/tidal data",
            "physical boundary and source-worldtube support are not signed silent",
            "COUNTERMODEL_SURVIVES",
            "MISSING_BOUNDARY_NO_SPURION",
        ),
        (
            "NSP2255_4_verdict",
            "no Weyl-type spurion/projector theorem",
            "all hidden frame/projector/history/boundary channels must be excluded in the same parent branch",
            "FAIL_CURRENT_CLAIM",
            "NO_SPURION_CERTIFICATE_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "spurion_id": spurion_id,
            "channel": channel,
            "evidence": evidence,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("1761_spurion", "1768_normal_form", "2254_certificate", "2254_weyl"),
            **false_flags(),
        }
        for spurion_id, channel, evidence, status, missing in rows
    ]


def activation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACT2255_0_field_content",
            "FCC2255_5 passes",
            "would certify R_AB is non-Weyl finite-sector/trace/Ricci-type",
            "FAIL",
        ),
        (
            "ACT2255_1_no_spurion",
            "NSP2255_4 passes",
            "would remove hidden Weyl projector escape",
            "FAIL",
        ),
        (
            "ACT2255_2_index_theorem",
            "WZ2254_0 activates",
            "would set B_Weyl=0 by index/representation mismatch",
            "NOT_ACTIVATED",
        ),
        (
            "ACT2255_3_local_vacuum",
            "B_Weyl removed from local source vector",
            "would leave B_Ric diagonalization plus C_RT/body/boundary/tail gates",
            "NOT_ACTIVATED",
        ),
        (
            "ACT2255_4_verdict",
            "B_Weyl theorem-zero activation",
            "blocked by field-content and no-spurion certificate failures",
            "FAIL_CURRENT_CLAIM",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "activation_id": activation_id,
            "required_gate": gate,
            "effect_if_passed": effect,
            "current_status": status,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for activation_id, gate, effect, status in rows
    ]


def fallback_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FBR2255_0_BWeyl",
            "B_Weyl",
            "Weyl/tidal curvature residual after failed certificate",
            "|B_Weyl| <= theorem_zero_or_numeric_bound",
            "MISSING_FIELD_CERTIFICATE_OR_BOUND",
            "PPN;orbital;local_GR;R10",
        ),
        (
            "FBR2255_1_no_spurion_width",
            "epsilon_spurion_W",
            "hidden Weyl projector/spurion width",
            "|epsilon_spurion_W| <= theorem_zero_or_numeric_bound",
            "MISSING_NO_SPURION_THEOREM_OR_BOUND",
            "PPN;orbital;clock",
        ),
        (
            "FBR2255_2_total",
            "B_Weyl_effective_abs",
            "absolute Weyl residual including hidden spurion leakage",
            "|B_Weyl| + |epsilon_spurion_W|",
            "SCHEMA_READY_VALUES_MISSING",
            "all_local_arenas",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "fallback_id": fallback_id,
            "symbol": symbol,
            "meaning": meaning,
            "formula_or_bound": formula,
            "current_status": status,
            "observable_link": observable,
            "units_status": "MISSING_COMMON_OPERATOR_NORMALIZATION",
            "source_paths": src("2254_weyl", "2254_certificate", "1761_spurion", "1768_normal_form"),
            **false_flags(),
        }
        for fallback_id, symbol, meaning, formula, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2255_0_field_content", "R_AB field-content certificate closes", "BLOCKED", "FCC2255_5_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2255_1_no_spurion", "no Weyl spurion theorem closes", "BLOCKED", "NSP2255_4_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2255_2_BWeyl_zero", "B_Weyl=0 theorem activates", "BLOCKED", "ACT2255_4_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2255_3_BWeyl_bound", "B_Weyl fallback row is score-ready", "BLOCKED", "FBR2255 rows contain MISSING bounds/units"),
        ("REF2255_4_local_GR", "derived local GR/Newton branch", "BLOCKED", "B_Weyl, B_Ric, C_RT, body/boundary/tail gates remain open"),
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
        ("CG2255_0_field_content", "R_AB field content/rank/transform law is parent-signed", "route selection, bundle/rank, index convention, and transform law missing"),
        ("CG2255_1_no_spurion", "no hidden Weyl projector/spurion", "hidden frame/projector/history/boundary channels survive"),
        ("CG2255_2_BWeyl_zero", "B_Weyl theorem-zero", "activation gate fails"),
        ("CG2255_3_BWeyl_bound", "B_Weyl finite residual score-ready", "numeric/source-backed bound and units missing"),
        ("CG2255_4_local_GR_Newton", "derived local GR/Newton recovery", "curvature/source/operator/boundary gates remain blocked"),
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
            "decision_id": "DEC2255_0_candidate",
            "decision": "NON_WEYL_FIELD_CONTENT_IS_CANDIDATE_NOT_CERTIFICATE",
            "reason": "The finite-sector/tensor-residual reading is plausible from 2247, but the parent route and transformation law are not selected.",
            "next_action": "do not activate B_Weyl zero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2255_1_no_spurion",
            "decision": "NO_SPURION_THEOREM_IS_REQUIRED",
            "reason": "Even a scalar/internal R_AB can couple to Weyl if a hidden projector, frame, history kernel, or boundary support tensor supplies the Weyl indices.",
            "next_action": "treat hidden Weyl projector as first-class residual if not excluded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2255_2_route",
            "decision": "PARENT_ROUTE_SELECTION_IS_NOW_UPSTREAM_BLOCKER",
            "reason": "Field content cannot be certified until the branch chooses absent quotient, first-class constraint, positive physical R, or sourced residual.",
            "next_action": "attack parent route selection rather than another representation audit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2255_3_next",
            "decision": "RAB_PARENT_ROUTE_SELECTION_OR_BWEYL_RESIDUAL_BRANCH_NEXT",
            "reason": "The least circular next move is to select/prove the R_AB route from 2247; if no route can be signed, stop chasing zero and run B_Weyl as a residual.",
            "next_action": "2256-Y5-R2FR-RAB-parent-route-selection-or-BWeyl-residual-branch.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2255_0_primary",
            "next_target": "2256-Y5-R2FR-RAB-parent-route-selection-or-BWeyl-residual-branch.md",
            "script": "scripts/Y5_R2FR_RAB_parent_route_selection_or_BWeyl_residual_branch_2256.py",
            "objective": "decide the upstream R_AB route from the 2247 menu: absent quotient, first-class constraint, positive source-free physical field, or sourced residual; this determines whether B_Weyl can be killed by representation or must be bounded",
            "selection_status": "selected",
            "success_condition": "one route becomes parent-signed or the B_Weyl residual branch is explicitly retained with no local-GR claim",
            "forbidden_shortcuts": "choosing the easiest route without proof; declaring no-spurion by preference; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2255_1_fallback",
            "next_target": "2256b-Y5-R2FR-BWeyl-effective-bound-runner.md",
            "script": "scripts/Y5_R2FR_BWeyl_effective_bound_runner_2256b.py",
            "objective": "build executable refusal runner for B_Weyl_effective_abs and arena projections if parent route selection remains unsigned",
            "selection_status": "held_fallback",
            "success_condition": "runner refuses MISSING rows and accepts only numeric, sourced, unit-matched B_Weyl residual bounds",
            "forbidden_shortcuts": "zero priors; tau=1; cancellation with Ricci/matter/source terms",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_field", OUTPUTS["field_content"], COPY_TARGETS["queue_field"], "field-content/no-spurion certificate queue"),
        ("queue_fallback", OUTPUTS["fallback"], COPY_TARGETS["queue_fallback"], "B_Weyl fallback residual queue"),
        ("branch_wep", OUTPUTS["fallback"], COPY_TARGETS["branch_wep"], "WEP branch locked B_Weyl effective residual copy"),
        ("beta_docs", OUTPUTS["field_content"], COPY_TARGETS["beta_docs"], "beta-source docs field-content/no-spurion copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2255_{copy_id}",
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
    field = read_csv(OUTPUTS["field_content"])
    spurion = read_csv(OUTPUTS["no_spurion"])
    activation = read_csv(OUTPUTS["activation"])
    fallback = read_csv(OUTPUTS["fallback"])
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

    formalization_2255 = []
    if FORMALIZATION.exists():
        formalization_2255 = [path for path in FORMALIZATION.rglob("*2255*") if path.is_file()]

    all_rows = [row for path in paths for row in read_csv(path)]
    rows = [
        check("VAL2255_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2255_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2255_2_prior_validation", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2254 validation passes where checked"),
        check("VAL2255_3_field_certificate_blocks", any(row["certificate_id"] == "FCC2255_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in field), "field-content certificate remains blocked"),
        check("VAL2255_4_no_spurion_blocks", any(row["spurion_id"] == "NSP2255_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in spurion), "no-spurion theorem remains blocked"),
        check("VAL2255_5_activation_fails", any(row["activation_id"] == "ACT2255_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in activation), "B_Weyl zero activation is refused"),
        check("VAL2255_6_fallback_rows", any(row["fallback_id"] == "FBR2255_2_total" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in fallback), "B_Weyl effective fallback row is staged"),
        check("VAL2255_7_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2255_8_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2255_9_decision_next", any(row["decision_id"] == "DEC2255_3_next" and "PARENT_ROUTE" in row["decision"] for row in decisions), "decision selects parent route selection next"),
        check("VAL2255_10_next_selected", any(row["route_id"] == "NEXT2255_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2255_11_csv_parse", csv_parse_ok, "all generated 2255 CSVs parse"),
        check("VAL2255_12_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        check("VAL2255_13_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2255_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2255_15_formalization_no_2255", not formalization_2255, "formalization-workbench has no 2255 outputs"),
    ]
    rows.append(
        check(
            "VAL2255_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2255 attempts field-content/no-spurion certificate, refuses B_Weyl zero activation, stages effective B_Weyl residual, and selects parent route selection next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    field: list[dict[str, Any]],
    spurion: list[dict[str, Any]],
    activation: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2255 - Y5/R2FR R_AB Field-Content And No-Spurion Certificate",
            "## Verdict\n\n2255 tries to activate the conditional `B_Weyl=0` theorem by certifying the field content of `R_AB` and excluding hidden Weyl-type projectors/spurions. It does not close. The non-Weyl finite-sector reading is still the best candidate, but the parent route is not selected, the bundle/rank/transformation law is not declared, and hidden frame/projector/history/boundary channels remain legal countermodels.\n\nThis is still progress because the failure is now upstream and explicit: route selection comes before representation certification. Until the parent selects absent quotient, first-class constraint, positive source-free field, or sourced residual, `B_Weyl` remains a conditional-zero or finite-residual object, not a claimed zero.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Field-Content Certificate Attempt\n" + markdown_table(field, ["certificate_id", "certificate_piece", "required_statement", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## No Weyl-Spurion Audit\n" + markdown_table(spurion, ["spurion_id", "channel", "evidence", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## B_Weyl Zero Activation Gate\n" + markdown_table(activation, ["activation_id", "required_gate", "effect_if_passed", "current_status", "gate_pass", "valid_for_claim"]),
            "## Fallback Residual Rows\n" + markdown_table(fallback, ["fallback_id", "symbol", "meaning", "formula_or_bound", "current_status", "observable_link", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is a useful correction of direction. We should not keep circling representation language until the route is chosen. The next real move is to attack the 2247 menu directly. If `R_AB` is absent/quotient or first-class constraint, local GR gets a clean route. If it is a positive physical residual, no-hair can still work but needs source/boundary/operator gates. If it is sourced residual, we stop pretending it is derived local GR and test it.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    write_csv(OUTPUTS["source_register"], source_rows)

    field = field_content_rows()
    spurion = no_spurion_rows()
    activation = activation_rows()
    fallback = fallback_rows()
    refusals = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["field_content"], field)
    write_csv(OUTPUTS["no_spurion"], spurion)
    write_csv(OUTPUTS["activation"], activation)
    write_csv(OUTPUTS["fallback"], fallback)
    write_csv(OUTPUTS["runner_refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["field_content"],
        OUTPUTS["no_spurion"],
        OUTPUTS["activation"],
        OUTPUTS["fallback"],
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
        build_doc(source_rows, field, spurion, activation, fallback, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2255 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
