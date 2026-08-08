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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_REPRESENTATION_CERTIFICATE_2254"
DOC = ROOT / "2254-Y5-R2FR-RAB-representation-certificate-or-BWeyl-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2254_00_2253_doc",
        "source_key": "2253_handoff",
        "source_path": ROOT / "2253-Y5-R2FR-RAB-Ricci-Weyl-split-and-geometric-mixing-diagonalization.md",
        "needles": ["DEC2253_3_next", "NEXT2253_0_primary"],
        "role": "selects R_AB representation certificate or B_Weyl bound row",
    },
    {
        "source_id": "SRC2254_01_2253_validation",
        "source_key": "2253_validation",
        "source_path": OUT / "P8_Y5_BRR545_2253_VALIDATION.csv",
        "needles": ["VAL2253_OVERALL", "PASS"],
        "role": "confirms 2253 passed before 2254 starts",
    },
    {
        "source_id": "SRC2254_02_2253_rep_gate",
        "source_key": "2253_rep_gate",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2253_RAB_REPRESENTATION_TYPE_GATE.csv",
        "needles": ["REP2253_0_scalar_trace", "REP2253_4_verdict"],
        "role": "incoming representation gate and B_Weyl zero condition",
    },
    {
        "source_id": "SRC2254_03_2253_split",
        "source_key": "2253_split",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2253_RICCI_WEYL_SPLIT_ATTEMPT.csv",
        "needles": ["RWS2253_3_representation_escape", "EXACT_CONDITIONAL_INDEX_THEOREM"],
        "role": "conditional index theorem for Weyl-coupling zero",
    },
    {
        "source_id": "SRC2254_04_2253_residuals",
        "source_key": "2253_residuals",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2253_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
        "needles": ["CURV2253_0_BWeyl", "MISSING_REPRESENTATION_CERTIFICATE_OR_BOUND"],
        "role": "B_Weyl residual row to refine",
    },
    {
        "source_id": "SRC2254_05_2247_doc",
        "source_key": "2247_parent_R",
        "source_path": ROOT / "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md",
        "needles": ["TPR2247_4_positive_RAB_example", "TOG2247_1_field_content"],
        "role": "best current parent R-sector representation evidence and missing field-content gate",
    },
    {
        "source_id": "SRC2254_06_2247_classifier",
        "source_key": "2247_classifier",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_PARENT_R_CANDIDATE_CLASSIFIER.csv",
        "needles": ["RC2247_2_positive_sourcefree_physical_R", "RC2247_1_first_class_vertical_constraint"],
        "role": "candidate R_AB routes and owner status",
    },
    {
        "source_id": "SRC2254_07_2247_template",
        "source_key": "2247_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_PR_TEMPLATE_CONTRACT.csv",
        "needles": ["TPR2247_3_Noether_PR", "TPR2247_4_positive_RAB_example"],
        "role": "Theta_R/P_R template and positive tensor-residual example",
    },
    {
        "source_id": "SRC2254_08_2248_doc",
        "source_key": "2248_nohair",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["NH2248_0_candidate_sector", "NH2248_3_zero_theorem"],
        "role": "positive R_AB no-hair route with inner-product action",
    },
    {
        "source_id": "SRC2254_09_1761_doc",
        "source_key": "1761_spurion",
        "source_path": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
        "needles": ["DV1761_3_shadow_frame", "SP1761_4_hidden_frame"],
        "role": "hidden frame/spurion warning against premature Weyl-zero claim",
    },
    {
        "source_id": "SRC2254_10_1768_doc",
        "source_key": "1768_normal_form",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["SCL1768_2_nonminimal_coupling", "SCL1768_5_post_variation_projector"],
        "role": "normal-form warning for hidden projectors/nonminimal couplings",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2254_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_PARENT_QLOC_2254_REPRESENTATION_EVIDENCE_LEDGER.csv",
    "certificate": OUT / "P8_Y5_PARENT_QLOC_2254_RAB_REPRESENTATION_CERTIFICATE_ATTEMPT.csv",
    "weyl_index": OUT / "P8_Y5_PARENT_QLOC_2254_BWEYL_INDEX_ZERO_THEOREM_GATE.csv",
    "bound_row": OUT / "P8_Y5_PARENT_QLOC_2254_BWEYL_BOUND_ROW_NONCLAIM.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2254_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2254_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2254_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2254_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2254_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2254_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_certificate": QUEUE / "JR2254_RAB_REPRESENTATION_CERTIFICATE_NONCLAIM.csv",
    "queue_bweyl": QUEUE / "JR2254_BWEYL_BOUND_ROW_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_representation_BWeyl_nonclaim_2254.csv",
    "beta_docs": BETA_DOCS / "RAB_REPRESENTATION_BWEYL_2254_NONCLAIM.csv",
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


def evidence_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EVID2254_0_positive_tensor_residual",
            "2247 positive route calls the example a minimal positive tensor-residual and writes <R,L_R R>",
            "supports finite-sector/internal/tensor-residual reading rather than confirmed Weyl four-index reading",
            "SUPPORTS_NON_WEYL_CANDIDATE_NOT_CERTIFICATE",
            "source says example only and route not parent-selected",
            "2247_parent_R;2247_template;2248_nohair",
        ),
        (
            "EVID2254_1_AB_indices",
            "Theta/P templates use R_AB labels and P_R^{mu AB} generator coefficients",
            "AB appears as sector/generator labels, not certified spacetime Weyl indices",
            "INTERNAL_OR_VERTICAL_LABEL_PLAUSIBLE",
            "field action and tensor/density convention are explicitly incomplete",
            "2247_template;2247_parent_R",
        ),
        (
            "EVID2254_2_field_content_missing",
            "TOG2247_1 says field list/transformation law is incomplete",
            "blocks any representation certificate",
            "HARD_BLOCKER",
            "must declare Y_R^A, transformation law, bundle/rank, and index type",
            "2247_parent_R;2247_template",
        ),
        (
            "EVID2254_3_no_Weyl_type_source_found",
            "focused current-state search found no parent-selected Weyl/Riemann-type R_AB action in the cited R-sector chain",
            "absence of evidence helps triage but is not proof",
            "SEARCH_SUPPORT_ONLY",
            "need positive certificate, not just no hit",
            "2253_handoff;2247_parent_R;2248_nohair",
        ),
        (
            "EVID2254_4_hidden_spurion_warning",
            "1761/1768 keep hidden frame, projector and nonminimal coupling channels open",
            "even scalar/internal R_AB can acquire Weyl coupling through a hidden Weyl-type spurion unless forbidden",
            "NO_SPURION_NOT_CERTIFIED",
            "must prove no hidden Weyl projector/spurion in parent action",
            "1761_spurion;1768_normal_form",
        ),
        (
            "EVID2254_5_verdict",
            "current representation evidence",
            "best current reading favors non-Weyl finite-sector/tensor-residual route, but it is not parent-signed",
            "REPRESENTATION_CERTIFICATE_NOT_CLOSED",
            "B_Weyl zero remains conditional; bound row required as fallback",
            "2253_rep_gate;2253_split;2247_parent_R",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "evidence_id": evidence_id,
            "evidence": evidence,
            "interpretation": interpretation,
            "status": status,
            "limitation": limitation,
            "source_keys": source_keys,
            "source_paths": ";".join(src(key) for key in source_keys.split(";")),
            **false_flags(),
        }
        for evidence_id, evidence, interpretation, status, limitation, source_keys in rows
    ]


def certificate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CERT2254_0_parent_route",
            "R_AB route selected before variation",
            "absent quotient, first-class constraint, positive source-free physical field, or sourced residual",
            "NOT_SELECTED",
            "MISSING_PARENT_ROUTE_SELECTION",
        ),
        (
            "CERT2254_1_field_bundle",
            "field bundle and rank",
            "Y_R^A with declared spacetime/internal indices, density convention, and gauge/constraint quotient",
            "NOT_DECLARED",
            "MISSING_FIELD_BUNDLE_AND_RANK",
        ),
        (
            "CERT2254_2_transform_law",
            "transformation law",
            "how R_AB transforms under diffeomorphisms/local Lorentz/internal vertical generator",
            "NOT_DECLARED",
            "MISSING_TRANSFORMATION_LAW",
        ),
        (
            "CERT2254_3_non_weyl_type",
            "non-Weyl representation",
            "R_AB is scalar/trace/Ricci-type/internal finite-sector variable, not a Weyl/Riemann four-index tensor",
            "PLAUSIBLE_NOT_CERTIFIED",
            "MISSING_NON_WEYL_TYPE_PROOF",
        ),
        (
            "CERT2254_4_no_spurion",
            "no hidden Weyl-type spurion/projector",
            "no background/projector/history/readout object supplies Weyl indices to a scalar/internal R_AB",
            "NOT_CERTIFIED",
            "MISSING_NO_SPURION_THEOREM",
        ),
        (
            "CERT2254_5_verdict",
            "R_AB representation certificate",
            "CERT2254_0 through CERT2254_4 must close in one parent branch",
            "FAIL_CURRENT_CLAIM",
            "RAB_REPRESENTATION_CERTIFICATE_NOT_PARENT_SIGNED",
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
            "source_paths": src("2247_parent_R", "2247_template", "2253_rep_gate", "1761_spurion", "1768_normal_form"),
            **false_flags(),
        }
        for certificate_id, piece, required, status, missing in rows
    ]


def weyl_index_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WZ2254_0_conditional_theorem",
            "If R_AB is scalar/trace/Ricci-type or internal finite-sector and no Weyl-type spurion/projector exists, then a linear scalar action term R_AB C_munuab is index-forbidden.",
            "B_Weyl=0",
            "EXACT_CONDITIONAL_THEOREM",
            "premises unsigned",
        ),
        (
            "WZ2254_1_scalar_case",
            "A scalar/internal R_AB cannot by itself contract the trace-free four-index Weyl tensor to a scalar density.",
            "linear Weyl mixing absent",
            "CONDITIONAL_ON_FIELD_TYPE",
            "R_AB scalar/internal type not certified",
        ),
        (
            "WZ2254_2_two_tensor_case",
            "A symmetric two-tensor R_AB can couple naturally to Ricci/Einstein-type tensors; a direct linear Weyl scalar needs extra projectors/derivatives.",
            "B_Weyl becomes higher-derivative/projector residual if not absent",
            "CONDITIONAL_ON_BASIS",
            "projector/derivative basis not certified",
        ),
        (
            "WZ2254_3_spurion_countermodel",
            "A hidden four-index projector or background tensor can make scalar/internal R_AB couple linearly to Weyl.",
            "B_Weyl remains live",
            "COUNTERMODEL_SURVIVES",
            "no-spurion theorem missing",
        ),
        (
            "WZ2254_4_verdict",
            "B_Weyl zero theorem",
            "Conditional index theorem is ready, but not activated without representation and no-spurion certificates.",
            "ZERO_THEOREM_NOT_ACTIVATED",
            "MISSING_RAB_REPRESENTATION_CERTIFICATE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "effect": effect,
            "current_status": status,
            "blocker": blocker,
            "source_paths": src("2253_split", "2253_rep_gate", "2247_template", "1768_normal_form"),
            **false_flags(),
        }
        for theorem_id, statement, effect, status, blocker in rows
    ]


def bound_row_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "BWB2254_0_BWeyl",
            "symbol": "B_Weyl",
            "definition": "linear Weyl/tidal curvature mixing coefficient in the R_AB Euler source vector",
            "formula_or_bound": "|B_Weyl| <= theorem_zero_from_WZ2254_or_source_backed_bound",
            "units_status": "MISSING_COMMON_OPERATOR_NORMALIZATION",
            "required_sources": "R_AB representation certificate; no-spurion theorem; or numeric/source-backed local curvature residual bound",
            "current_status": "MISSING_REPRESENTATION_CERTIFICATE_OR_NUMERIC_BOUND",
            "observable_link": "PPN;orbital;local_GR;R10",
            "source_paths": src("2253_residuals", "2253_split", "2253_rep_gate"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "BWB2254_1_BWeyl_projection",
            "symbol": "tau_Weyl_local",
            "definition": "projection from B_Weyl C_Weyl to local PPN/orbital/R10 residual vector",
            "formula_or_bound": "residual_local <= tau_Weyl_local |B_Weyl| |C_Weyl|",
            "units_status": "MISSING_ARENA_PROJECTION_KERNEL",
            "required_sources": "local curvature scale; body/source geometry; PPN/orbital projection kernel; R10 mapping if applicable",
            "current_status": "MISSING_ARENA_PROJECTION",
            "observable_link": "PPN;orbital;local_GR",
            "source_paths": src("2253_residuals", "2248_nohair"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "BWB2254_2_total",
            "symbol": "B_Weyl_claim_status",
            "definition": "claim status for B_Weyl branch",
            "formula_or_bound": "claim allowed only if WZ2254 theorem-zero activates or BWB2254_0/1 are numeric, sourced, unit-matched, and within arena bounds",
            "units_status": "status",
            "required_sources": "all above",
            "current_status": "NONCLAIM_BOUND_ROW_STAGED",
            "observable_link": "all_local_arenas",
            "source_paths": src("2253_residuals", "2253_validation"),
            **false_flags(),
        },
    ]
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2254_0_rep_certificate", "R_AB representation certificate closes", "BLOCKED", "CERT2254_5_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2254_1_BWeyl_zero", "B_Weyl=0 by index theorem", "BLOCKED", "WZ2254_4_verdict=ZERO_THEOREM_NOT_ACTIVATED"),
        ("REF2254_2_BWeyl_bound", "B_Weyl finite bound is score-ready", "BLOCKED", "BWB2254 rows have missing units/projection/numeric bound"),
        ("REF2254_3_local_vacuum", "local vacuum source silence", "BLOCKED", "B_Weyl and body/boundary/tail gates remain open"),
        ("REF2254_4_local_GR", "derived local GR/Newton branch", "BLOCKED", "representation/source/operator gates remain open"),
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
        ("CG2254_0_representation", "R_AB representation certificate is parent-signed", "field bundle/rank/transformation/no-spurion clauses missing"),
        ("CG2254_1_BWeyl_zero", "B_Weyl theorem-zero", "conditional theorem premises unsigned"),
        ("CG2254_2_BWeyl_bound", "B_Weyl bound row score-ready", "numeric bound, units, and arena projection missing"),
        ("CG2254_3_nohair", "2248 no-hair source leg can ignore Weyl driving", "B_Weyl not zero/bounded"),
        ("CG2254_4_local_GR_Newton", "derived local GR/Newton recovery", "representation/source/operator/boundary gates remain blocked"),
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
            "decision_id": "DEC2254_0_evidence",
            "decision": "CURRENT_EVIDENCE_FAVORS_NON_WEYL_BUT_DOES_NOT_CERTIFY",
            "reason": "2247/2248 treat R_AB through a finite-sector inner-product quadratic block and positive tensor-residual example, but field content and transformation law remain incomplete.",
            "next_action": "do not claim B_Weyl=0 yet",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2254_1_theorem",
            "decision": "BWEYL_INDEX_ZERO_THEOREM_READY_CONDITIONAL",
            "reason": "If R_AB is scalar/internal/trace/Ricci-type and no Weyl spurion exists, a linear Weyl term is index-forbidden.",
            "next_action": "turn field-content/no-spurion certificate into the next proof target",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2254_2_fallback",
            "decision": "BWEYL_BOUND_ROW_STAGED_NONCLAIM",
            "reason": "If representation or no-spurion certification fails, B_Weyl is a real local residual and must be bounded empirically.",
            "next_action": "do not delete B_Weyl; carry bound row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2254_3_next",
            "decision": "RAB_FIELD_CONTENT_NO_SPURION_CERTIFICATE_NEXT",
            "reason": "The fastest derivation route is to close TOG2247_1: declare R_AB bundle/rank/transformation and prove no hidden Weyl projector/spurion.",
            "next_action": "2255-Y5-R2FR-RAB-field-content-and-no-spurion-certificate.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2254_0_primary",
            "next_target": "2255-Y5-R2FR-RAB-field-content-and-no-spurion-certificate.md",
            "script": "scripts/Y5_R2FR_RAB_field_content_and_no_spurion_certificate_2255.py",
            "objective": "close the concrete field-content gate: declare R_AB bundle/rank/transformation law and prove no hidden Weyl-type projector/spurion; if successful activate the conditional B_Weyl=0 theorem, otherwise retain B_Weyl bound row",
            "selection_status": "selected",
            "success_condition": "field-content plus no-spurion certificate activates WZ2254, or B_Weyl bound row remains explicit and nonclaim",
            "forbidden_shortcuts": "assuming scalar/internal type from notation; using absence of search hits as proof; ignoring hidden projectors; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2254_1_fallback",
            "next_target": "2255b-Y5-R2FR-BWeyl-local-bound-acquisition-runner.md",
            "script": "scripts/Y5_R2FR_BWeyl_local_bound_acquisition_runner_2255b.py",
            "objective": "build numeric/source-backed acquisition requirements and refusal runner for B_Weyl and tau_Weyl_local if the representation certificate fails",
            "selection_status": "held_fallback",
            "success_condition": "runner refuses MISSING rows and accepts only numeric, sourced, unit-matched B_Weyl local residual bounds",
            "forbidden_shortcuts": "setting B_Weyl=0 by taste; tau=1; cancellation with B_Ric or C_RT",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_certificate", OUTPUTS["certificate"], COPY_TARGETS["queue_certificate"], "R_AB representation certificate nonclaim queue"),
        ("queue_bweyl", OUTPUTS["bound_row"], COPY_TARGETS["queue_bweyl"], "B_Weyl bound row nonclaim queue"),
        ("branch_wep", OUTPUTS["bound_row"], COPY_TARGETS["branch_wep"], "WEP branch locked B_Weyl residual copy"),
        ("beta_docs", OUTPUTS["certificate"], COPY_TARGETS["beta_docs"], "beta-source docs R_AB representation certificate copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2254_{copy_id}",
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
    evidence = read_csv(OUTPUTS["evidence"])
    cert = read_csv(OUTPUTS["certificate"])
    weyl = read_csv(OUTPUTS["weyl_index"])
    bounds = read_csv(OUTPUTS["bound_row"])
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

    formalization_2254 = []
    if FORMALIZATION.exists():
        formalization_2254 = [path for path in FORMALIZATION.rglob("*2254*") if path.is_file()]

    all_rows = [row for path in paths for row in read_csv(path)]
    rows = [
        check("VAL2254_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2254_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2254_2_prior_validation", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2253 validation passes where checked"),
        check("VAL2254_3_evidence_nonclaim", any(row["evidence_id"] == "EVID2254_5_verdict" and row["status"] == "REPRESENTATION_CERTIFICATE_NOT_CLOSED" for row in evidence), "representation evidence is audited without promotion"),
        check("VAL2254_4_certificate_blocks", any(row["certificate_id"] == "CERT2254_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in cert), "representation certificate remains blocked"),
        check("VAL2254_5_weyl_theorem_conditional", any(row["theorem_id"] == "WZ2254_0_conditional_theorem" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in weyl), "conditional B_Weyl index theorem is recorded"),
        check("VAL2254_6_weyl_zero_not_activated", any(row["theorem_id"] == "WZ2254_4_verdict" and row["current_status"] == "ZERO_THEOREM_NOT_ACTIVATED" for row in weyl), "B_Weyl zero theorem is not activated"),
        check("VAL2254_7_bound_row_nonclaim", any(row["bound_id"] == "BWB2254_0_BWeyl" and row["current_status"] == "MISSING_REPRESENTATION_CERTIFICATE_OR_NUMERIC_BOUND" for row in bounds), "B_Weyl bound row remains nonclaim"),
        check("VAL2254_8_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2254_9_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2254_10_decision_next", any(row["decision_id"] == "DEC2254_3_next" and "FIELD_CONTENT" in row["decision"] for row in decisions), "decision selects field-content/no-spurion certificate next"),
        check("VAL2254_11_next_selected", any(row["route_id"] == "NEXT2254_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2254_12_csv_parse", csv_parse_ok, "all generated 2254 CSVs parse"),
        check("VAL2254_13_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        check("VAL2254_14_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2254_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2254_16_formalization_no_2254", not formalization_2254, "formalization-workbench has no 2254 outputs"),
    ]
    rows.append(
        check(
            "VAL2254_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2254 audits R_AB representation evidence, keeps B_Weyl zero conditional, stages B_Weyl bound row, and selects field-content/no-spurion certificate next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    cert: list[dict[str, Any]],
    weyl: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2254 - Y5/R2FR R_AB Representation Certificate Or B_Weyl Bound Row",
            "## Verdict\n\n2254 finds a promising but not claim-grade route. The current R-sector chain most strongly supports treating `R_AB` as a finite-sector/internal or tensor-residual amplitude governed by an inner-product quadratic block, not as a certified Weyl/Riemann four-index field. That makes the `B_Weyl=0` index theorem plausible.\n\nBut plausible is not enough. `2247` also says the field content and transformation law are incomplete, and the hidden projector/spurion channel is still open. Therefore `B_Weyl=0` remains a conditional theorem only. The fallback `B_Weyl` bound row is staged as nonclaim, and the next target is the concrete field-content/no-spurion certificate.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Representation Evidence Ledger\n" + markdown_table(evidence, ["evidence_id", "evidence", "interpretation", "status", "limitation", "valid_for_claim"]),
            "## R_AB Representation Certificate Attempt\n" + markdown_table(cert, ["certificate_id", "certificate_piece", "required_statement", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## B_Weyl Index-Zero Theorem Gate\n" + markdown_table(weyl, ["theorem_id", "statement", "effect", "current_status", "blocker", "valid_for_claim"]),
            "## B_Weyl Bound Row\n" + markdown_table(bounds, ["bound_id", "symbol", "definition", "formula_or_bound", "units_status", "current_status", "observable_link", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is a decent little opening, chume. We may be able to kill the Weyl/tidal coupling cleanly, but only by proving what `R_AB` actually is. The theory now needs a field-content certificate: bundle/rank/index type, transformation law, and no hidden Weyl spurion. If that closes, `B_Weyl` can go to zero by index structure rather than wishful thinking. If it does not close, the bound row is already waiting.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    write_csv(OUTPUTS["source_register"], source_rows)

    evidence = evidence_rows()
    cert = certificate_rows()
    weyl = weyl_index_rows()
    bounds = bound_row_rows()
    refusals = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["evidence"], evidence)
    write_csv(OUTPUTS["certificate"], cert)
    write_csv(OUTPUTS["weyl_index"], weyl)
    write_csv(OUTPUTS["bound_row"], bounds)
    write_csv(OUTPUTS["runner_refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["evidence"],
        OUTPUTS["certificate"],
        OUTPUTS["weyl_index"],
        OUTPUTS["bound_row"],
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
        build_doc(source_rows, evidence, cert, weyl, bounds, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2254 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
