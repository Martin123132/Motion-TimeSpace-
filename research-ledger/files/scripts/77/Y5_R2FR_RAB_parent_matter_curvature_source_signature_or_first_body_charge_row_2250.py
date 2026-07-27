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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_SOURCE_SIGNATURE_2250"
DOC = ROOT / "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2250_00_2249_doc",
        "source_key": "2249_handoff",
        "source_path": ROOT / "2249-Y5-R2FR-RAB-JR-source-zero-or-component-bound-pack.md",
        "needles": ["DEC2249_2_next", "NEXT2249_0_primary"],
        "role": "selects R_AB parent source signature or first body-charge row",
    },
    {
        "source_id": "SRC2250_01_2249_validation",
        "source_key": "2249_validation",
        "source_path": OUT / "P8_Y5_BRR545_2249_VALIDATION.csv",
        "needles": ["VAL2249_OVERALL", "PASS"],
        "role": "confirms 2249 passed",
    },
    {
        "source_id": "SRC2250_02_2249_body",
        "source_key": "2249_body_law",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2249_BODY_CHARGE_SOURCE_LAW.csv",
        "needles": ["BCL2249_3_zero_switch", "ZERO_SWITCH_REJECTED_UNTIL_PARENT_SIGNED"],
        "role": "body charge zero switch to be tested",
    },
    {
        "source_id": "SRC2250_03_2249_bounds",
        "source_key": "2249_bounds",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2249_JR_COMPONENT_BOUND_TEMPLATE.csv",
        "needles": ["JBT2249_0_BRR", "JBT2249_1_CRT"],
        "role": "B_RR/C_RT/Q_R source coefficient templates",
    },
    {
        "source_id": "SRC2250_04_2159_doc",
        "source_key": "2159_moms",
        "source_path": ROOT / "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md",
        "needles": ["MOM2159_7_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "ordinary-matter MOMS attempt remains unsigned",
    },
    {
        "source_id": "SRC2250_05_2159_validation",
        "source_key": "2159_validation",
        "source_path": OUT / "P8_Y5_BRR545_2159_VALIDATION.csv",
        "needles": ["VAL2159_OVERALL", "PASS"],
        "role": "confirms 2159 passed as nonclaim",
    },
    {
        "source_id": "SRC2250_06_1088_moms",
        "source_key": "1088_moms",
        "source_path": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
        "needles": ["MOMS1088_7_verdict", "THM1088_5_conclusion"],
        "role": "minimal ordinary-matter signature theorem contract",
    },
    {
        "source_id": "SRC2250_07_1344_body_charge",
        "source_key": "1344_body_charge",
        "source_path": ROOT / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md",
        "needles": ["VERT1344_3_body_charge", "QX1344_2_zero_switch"],
        "role": "body charge and no-XR vertex warning",
    },
    {
        "source_id": "SRC2250_08_1627_jr",
        "source_key": "1627_jr",
        "source_path": ROOT / "1627-Y5-R2FR-JR-zero-source-theorem-or-first-finite-JR-row.md",
        "needles": ["JR1627_2_reciprocal_charge", "JR1627_4_boundary_momentum"],
        "role": "J_R=0 leaves Q_R unless boundary/source neutrality closes",
    },
    {
        "source_id": "SRC2250_09_1628_source_owner",
        "source_key": "1628_source_owner",
        "source_path": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
        "needles": ["SOC1628_6_verdict", "CE1628_1_direct_RAB_slot", "DEC1628_1_certificate"],
        "role": "source-owner route fails direct R_AB slot and Pi_R blockers",
    },
    {
        "source_id": "SRC2250_10_1768_normal_form",
        "source_key": "1768_normal_form",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["ANF1768_6_current_verdict", "SCL1768_2_nonminimal_coupling"],
        "role": "parent normal-form signature and nonminimal source classification",
    },
    {
        "source_id": "SRC2250_11_1430_cparent",
        "source_key": "1430_cparent",
        "source_path": ROOT / "1430-Y5-R10-RAB-C-parent-coupling-source-signature-or-refusal-ledger.md",
        "needles": ["CPC1430_0_product_law", "HUNT1430_5_verdict"],
        "role": "C_parent coupling vector remains placeholder/refusal",
    },
    {
        "source_id": "SRC2250_12_1720_functor",
        "source_key": "1720_functor",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"],
        "role": "matter functor signature remains unsigned",
    },
    {
        "source_id": "SRC2250_13_1761_no_vertex",
        "source_key": "1761_no_vertex",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
        "needles": ["NDV1761_0_target", "NDV1761_4_current_verdict"],
        "role": "no-direct-vertex grammar remains parent-unsigned",
    },
    {
        "source_id": "SRC2250_14_1786_boundary",
        "source_key": "1786_boundary",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
        "needles": ["BMC1786_1_matter_interface", "BMC1786_5_verdict"],
        "role": "boundary/matter closure remains open",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2250_SOURCE_REGISTER.csv",
    "signature_attempt": OUT / "P8_Y5_PARENT_QLOC_2250_RAB_SOURCE_SIGNATURE_ATTEMPT.csv",
    "no_source_theorem": OUT / "P8_Y5_PARENT_QLOC_2250_NO_SOURCE_THEOREM_GATE.csv",
    "first_body_charge_row": OUT / "P8_Y5_PARENT_QLOC_2250_FIRST_BODY_CHARGE_ROW.csv",
    "coefficient_acquisition": OUT / "P8_Y5_PARENT_QLOC_2250_BRR_CRT_QR_ACQUISITION_LEDGER.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2250_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2250_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2250_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2250_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2250_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2250_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_body": QUEUE / "JR2250_BODY_CHARGE_ROW_NONCLAIM.csv",
    "queue_coeffs": QUEUE / "JR2250_BRR_CRT_QR_ACQUISITION_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_source_signature_body_charge_nonclaim_2250.csv",
    "beta_docs": BETA_DOCS / "RAB_SOURCE_SIGNATURE_BODY_CHARGE_2250_NONCLAIM.csv",
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


def signature_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RSS2250_0_parent_action_owner",
            "one parent action owns geometry, R_AB, matter, boundary, and readout order before projection",
            "S_parent = S_geom[Phi,R_AB,...] + S_matter[Psi,E(q(Phi)),theta] + S_boundary, with no post-variation source map",
            "not supplied as a complete parent action in current corpus",
            "MISSING_PARENT_ACTION_OWNER",
        ),
        (
            "RSS2250_1_no_direct_RAB_matter_slot",
            "ordinary matter has no independent R_AB argument",
            "partial S_matter / partial R_AB = 0 because matter sees only quotient observed geometry and fixed constants",
            "exact conditional MOMS route exists but direct R_AB/source slots are not parent-excluded",
            "MISSING_NO_DIRECT_RAB_SOURCE_SLOT_THEOREM",
        ),
        (
            "RSS2250_2_no_curvature_source_vertex",
            "no R_AB-curvature/source vertex",
            "B_RR := delta^2 S_parent/(delta R_AB delta R_obs)=0 and C_RT := delta^2 S_parent/(delta R_AB delta T)=0",
            "no-vertex theorem for R_AB is not signed; nonminimal/source couplings remain legal countermodels",
            "MISSING_BRR_ZERO;MISSING_CRT_ZERO",
        ),
        (
            "RSS2250_3_source_worldtube_neutrality",
            "body/source-worldtube charge vanishes",
            "Q_R[body] = int_body sqrt(gamma) W_R rho_R + Q_R_boundary = 0",
            "exterior source silence does not prove this; Pi_R/boundary neutrality remains unsigned",
            "MISSING_QR_BODY_ZERO;MISSING_PIR_ZERO",
        ),
        (
            "RSS2250_4_boundary_reference_silence",
            "boundary/reference/counterterm source terms vanish or are bounded",
            "Q_R_boundary=0 and counterterm/reference variations are fixed before source extraction",
            "proper compact collar result does not cover physical source worldtubes",
            "MISSING_BOUNDARY_REFERENCE_SOURCE_RULE",
        ),
        (
            "RSS2250_5_verdict",
            "R_AB parent matter/curvature no-source signature",
            "RSS2250_0 through RSS2250_4 pass in the same parent branch",
            "current corpus does not sign the source signature; retain body-charge and coefficient rows",
            "RAB_SOURCE_SIGNATURE_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "clause": clause,
            "required_statement": statement,
            "current_evidence": evidence,
            "current_status": "EXACT_CONDITIONAL_ROUTE_UNSIGNED" if clause_id in {"RSS2250_1_no_direct_RAB_matter_slot"} else ("FAIL_CURRENT_CLAIM" if clause_id == "RSS2250_5_verdict" else "NOT_PARENT_SIGNED"),
            "missing_for_claim": missing,
            "source_paths": src("2249_handoff", "1088_moms", "1628_source_owner", "1768_normal_form", "1344_body_charge"),
            **false_flags(),
        }
        for clause_id, clause, statement, evidence, missing in rows
    ]


def no_source_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NST2250_0_conditional_theorem",
            "theorem": "If the parent action has no direct R_AB matter slot, B_RR=C_RT=0, Q_R[body]=0, Q_R_boundary=0, and readout/history/projector tails vanish, then the source side of the 2248 no-hair theorem closes.",
            "status": "CONDITIONAL_THEOREM_WRITTEN_PREMISES_UNSIGNED",
            "what_it_would_unlock": "RNH2248_2_JR_zero and BCL2249_3_zero_switch would pass, allowing the positive no-hair route to be tested against operator/boundary gates.",
            "current_blocker": "RSS2250_5_verdict fails",
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NST2250_1_not_enough",
            "theorem": "MOMS ordinary-matter pullback alone does not kill B_RR, Q_R[body], Pi_R, boundary reference terms, or a nonminimal R_AB-curvature vertex.",
            "status": "REPAIR_RULE_RECORDED",
            "what_it_would_unlock": "prevents accidental promotion from ordinary-matter descent to full local-GR source neutrality",
            "current_blocker": "body/curvature source terms remain live",
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NST2250_2_verdict",
            "theorem": "No current R_AB no-source theorem is claim-active.",
            "status": "NO_SOURCE_THEOREM_NOT_ACTIVATED",
            "what_it_would_unlock": "none yet; use finite body-charge/source-coefficient rows",
            "current_blocker": "parent signature and source coefficients missing",
            **false_flags(),
        },
    ]


def first_body_charge_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BCR2250_0_density",
            "rho_R",
            "rho_R = B_RR R_obs + C_RT T + J_R_matter_bulk + J_R_readout + J_R_history + J_R_projector + J_R_counterterm",
            "source_density_units_required",
            "MISSING_BRR;MISSING_CRT;MISSING_COMPONENTS",
            "R10;PPN;WEP;clock;orbital;local_GR",
        ),
        (
            "BCR2250_1_body_charge",
            "Q_R_body",
            "Q_R[body] = int_body sqrt(gamma) W_R rho_R + Q_R_boundary",
            "R_AB_charge_units_required",
            "MISSING_BODY_MODEL;MISSING_WR;MISSING_QR_BOUNDARY",
            "R10;PPN;orbital;local_GR",
        ),
        (
            "BCR2250_2_exterior_profile",
            "R_AB_profile",
            "R_AB(x) = integral_body G_R(x,x') rho_R(x') dV' + boundary/history tails",
            "dimensionless_RAB_after_normalization",
            "MISSING_GREEN_FUNCTION;MISSING_ZR;MISSING_MR2;MISSING_DOMAIN",
            "R10;PPN;clock;orbital",
        ),
        (
            "BCR2250_3_zero_switch",
            "Q_R_body_zero",
            "Q_R[body]=0 iff B_RR=C_RT=J_R_components=Q_R_boundary=0 in the same signed parent branch",
            "theorem_zero_or_abs_bound",
            "MISSING_PARENT_SIGNATURE",
            "local_GR",
        ),
        (
            "BCR2250_4_verdict",
            "first_body_charge_row",
            "first body-charge row is staged as source-ready schema only; no numeric/source-backed value exists",
            "not_scoreable",
            "SOURCE_CHARGE_ROW_NONCLAIM_VALUES_MISSING",
            "all_local_arenas",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_status": "NONCLAIM_SCHEMA_READY_VALUES_MISSING" if row_id != "BCR2250_3_zero_switch" else "ZERO_SWITCH_REJECTED_UNTIL_PARENT_SIGNED",
            "missing_inputs": missing,
            "observable_link": observable,
            "source_paths": src("2249_body_law", "1344_body_charge", "1627_jr", "1628_source_owner"),
            **false_flags(),
        }
        for row_id, symbol, formula, units, missing, observable in rows
    ]


def coefficient_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ2250_0_BRR", "B_RR", "curvature-source vertex coefficient", "derive zero by parent no-vertex theorem or source bound from parent action Hessian", "MISSING_NO_VERTEX_THEOREM_OR_NUMERIC_BOUND", "R10;PPN;local_GR"),
        ("ACQ2250_1_CRT", "C_RT", "matter trace/source vertex coefficient", "derive zero by source-slot exclusion or source-backed bound in same matter frame", "MISSING_SOURCE_SLOT_EXCLUSION_OR_NUMERIC_BOUND", "R10;WEP;PPN;orbital"),
        ("ACQ2250_2_QR_body", "Q_R_body", "source-worldtube/body reciprocal charge", "derive zero by body neutrality or source-backed body integral", "MISSING_BODY_NEUTRALITY_OR_NUMERIC_BODY_CHARGE", "R10;PPN;orbital;local_GR"),
        ("ACQ2250_3_PiR", "Pi_R", "boundary reciprocal momentum", "derive Pi_R=0 natural boundary condition or bound finite boundary momentum", "MISSING_PIR_ZERO_OR_BOUND", "boundary;R10;PPN"),
        ("ACQ2250_4_total", "RAB_source_vector_abs", "absolute source coefficient vector", "sum_abs(B_RR,C_RT,Q_R_body,Pi_R,readout,history,projector,counterterm)", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "symbol": symbol,
            "definition": definition,
            "acquisition_rule": rule,
            "current_status": status,
            "observable_link": observable,
            "source_paths": src("2249_bounds", "1628_source_owner", "1430_cparent", "1768_normal_form"),
            **false_flags(),
        }
        for acquisition_id, symbol, definition, rule, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2250_0_source_signature", "R_AB no-source signature is derived", "BLOCKED", "RSS2250_5_verdict=FAIL_CURRENT_CLAIM", False),
        ("REF2250_1_QR_body_zero", "Q_R[body]=0 theorem", "BLOCKED", "BCR2250_3_zero_switch remains unsigned", False),
        ("REF2250_2_first_body_row", "first body-charge row scoreable", "BLOCKED", "BCR2250_4 has missing values and no source-backed coefficient", False),
        ("REF2250_3_local_GR", "2248 no-hair activates local GR/Newton", "BLOCKED", "operator/source/boundary/projection gates still not closed", False),
        ("REF2250_4_empirical_scores", "R10/PPN/WEP/clock/orbital scores runnable", "BLOCKED", "arena projections have no numeric source vector", False),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": score_eligible,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, claim, result, blocked_by, score_eligible in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2250_0_signature", "parent R_AB no-source signature", "RSS2250_5 fails"),
        ("CG2250_1_body_charge", "Q_R[body]=0 or source-backed finite value", "BCR2250 rows are symbolic/nonclaim"),
        ("CG2250_2_source_vector", "B_RR/C_RT/Q_R/Pi_R source vector score-ready", "ACQ2250_4 values missing"),
        ("CG2250_3_nohair", "2248 no-hair source leg closes", "2250 no-source theorem not activated"),
        ("CG2250_4_local_GR", "local GR/Newton reduction", "source, operator, boundary, and projection gates blocked"),
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
            "decision_id": "DEC2250_0_signature",
            "decision": "RAB_SOURCE_SIGNATURE_NOT_PARENT_SIGNED",
            "reason": "MOMS-style matter descent is useful but does not exclude R_AB curvature vertices, body charge, Pi_R, or boundary/source slots",
            "next_action": "do not activate 2248 no-hair",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2250_1_first_row",
            "decision": "FIRST_BODY_CHARGE_ROW_STAGED_NONCLAIM",
            "reason": "Q_R[body], B_RR, C_RT and Pi_R are now explicit acquisition targets with units/arena links, but no values",
            "next_action": "try source-slot exclusion before hunting arbitrary coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2250_2_next",
            "decision": "RAB_SOURCE_SLOT_EXCLUSION_OR_BRR_CRT_ACQUISITION_NEXT",
            "reason": "the least-scrutiny route is a parent grammar theorem forbidding direct R_AB/source-only slots; fallback is source-backed B_RR/C_RT/Q_R/Pi_R acquisition",
            "next_action": "2251-Y5-R2FR-RAB-source-slot-exclusion-or-BRR-CRT-acquisition-ledger.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2250_0_primary",
            "next_target": "2251-Y5-R2FR-RAB-source-slot-exclusion-or-BRR-CRT-acquisition-ledger.md",
            "script": "scripts/Y5_R2FR_RAB_source_slot_exclusion_or_BRR_CRT_acquisition_ledger_2251.py",
            "objective": "try to derive a parent object-language rule forbidding independent R_AB matter/source slots and curvature-source vertices; if unsigned, build BRR/CRT/QR/PiR acquisition ledger rows without scoring",
            "selection_status": "selected",
            "success_condition": "source-slot exclusion theorem closes or first coefficient/source-charge acquisition ledger is source-ready and claim-blocked",
            "forbidden_shortcuts": "MOMS-only promotion; exterior-vacuum proof; invented coefficients; source cancellation; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2250_1_parallel_boundary",
            "next_target": "2251b-Y5-R2FR-RAB-PiR-boundary-neutrality-or-QR-bound-row.md",
            "script": "scripts/Y5_R2FR_RAB_PiR_boundary_neutrality_or_QR_bound_row_2251b.py",
            "objective": "derive Pi_R=0 boundary/source neutrality or stage finite Q_R/Pi_R boundary-charge rows",
            "selection_status": "held_parallel",
            "success_condition": "Pi_R theorem-zero or source-backed finite boundary momentum row",
            "forbidden_shortcuts": "asymptotic flatness as source neutrality; compact-collar proof on physical source worldtubes",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_body", OUTPUTS["first_body_charge_row"], COPY_TARGETS["queue_body"], "first R_AB body-charge row nonclaim queue"),
        ("queue_coeffs", OUTPUTS["coefficient_acquisition"], COPY_TARGETS["queue_coeffs"], "B_RR/C_RT/Q_R/Pi_R acquisition nonclaim queue"),
        ("branch_wep", OUTPUTS["coefficient_acquisition"], COPY_TARGETS["branch_wep"], "WEP branch locked R_AB source coefficient copy"),
        ("beta_docs", OUTPUTS["coefficient_acquisition"], COPY_TARGETS["beta_docs"], "beta-source docs R_AB source coefficient copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2250_{copy_id}",
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
    signature = read_csv(OUTPUTS["signature_attempt"])
    theorem = read_csv(OUTPUTS["no_source_theorem"])
    body = read_csv(OUTPUTS["first_body_charge_row"])
    acquisition = read_csv(OUTPUTS["coefficient_acquisition"])
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

    formalization_2250 = []
    if FORMALIZATION.exists():
        formalization_2250 = [path for path in FORMALIZATION.rglob("*2250*") if path.is_file()]

    all_rows = [row for path in paths for row in read_csv(path)]
    rows = [
        check("VAL2250_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2250_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2250_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2249 and precedent validations pass where checked"),
        check("VAL2250_3_signature_refused", any(row["clause_id"] == "RSS2250_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in signature), "parent R_AB source signature is not promoted"),
        check("VAL2250_4_no_source_not_activated", any(row["theorem_id"] == "NST2250_2_verdict" and row["status"] == "NO_SOURCE_THEOREM_NOT_ACTIVATED" for row in theorem), "no-source theorem remains inactive"),
        check("VAL2250_5_body_row_nonclaim", any(row["row_id"] == "BCR2250_4_verdict" and row["current_status"] == "NONCLAIM_SCHEMA_READY_VALUES_MISSING" for row in body), "first body-charge row is schema-only nonclaim"),
        check("VAL2250_6_acquisition_values_missing", any(row["acquisition_id"] == "ACQ2250_4_total" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in acquisition), "source coefficient acquisition ledger is not score-ready"),
        check("VAL2250_7_refusals_block", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks signature/body/local claims"),
        check("VAL2250_8_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2250_9_decision_next", any(row["decision_id"] == "DEC2250_2_next" and "RAB_SOURCE_SLOT_EXCLUSION" in row["decision"] for row in decisions), "decision selects source-slot exclusion or acquisition next"),
        check("VAL2250_10_next_selected", any(row["route_id"] == "NEXT2250_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2250_11_csv_parse", csv_parse_ok, "all generated 2250 CSVs parse"),
        check("VAL2250_12_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" for row in all_rows), "no generated theorem/score/claim flags are true"),
        check("VAL2250_13_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2250_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2250_15_formalization_no_2250", not formalization_2250, "formalization-workbench has no 2250 outputs"),
    ]
    rows.append(
        check(
            "VAL2250_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2250 refuses the R_AB source signature, stages first body-charge/source-coefficient rows, and selects source-slot exclusion or acquisition next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    body: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2250 - Y5/R2FR R_AB Parent Matter/Curvature Source Signature Or First Body-Charge Row",
            "## Verdict\n\n2250 tries the clean derivation first. The result is negative but useful: the ordinary-matter MOMS pullback is not enough to sign the full `R_AB` source side. A complete parent source signature would also need no direct `R_AB` matter slot, no `B_RR R_AB R_obs` or `C_RT R_AB T` vertex, `Q_R[body]=0`, `Pi_R=0`, and boundary/reference silence in the same parent branch.\n\nThose clauses are not signed, so the source side remains nonclaim. The win is that the first body-charge/source-coefficient row is now explicit rather than fog: `rho_R`, `Q_R[body]`, `B_RR`, `C_RT`, `Pi_R`, and the absolute source vector are acquisition targets.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Source Signature Attempt\n" + markdown_table(signature, ["clause_id", "clause", "required_statement", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## No-Source Theorem Gate\n" + markdown_table(theorem, ["theorem_id", "theorem", "status", "current_blocker", "valid_for_claim"]),
            "## First Body-Charge Row\n" + markdown_table(body, ["row_id", "symbol", "formula", "current_status", "missing_inputs", "observable_link", "valid_for_claim"]),
            "## Coefficient Acquisition Ledger\n" + markdown_table(acquisition, ["acquisition_id", "symbol", "definition", "current_status", "observable_link", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is a useful failure. We now know the source side cannot be closed by saying 'ordinary matter descends' and walking away. The parent must also forbid the `R_AB` source slot and curvature/source vertices, or the theory must carry a finite body-charge vector into tests. Next we attack the source-slot exclusion theorem directly.",
        ]
    ) + "\n"


def main() -> None:
    source_rows = source_register_rows()
    signature = signature_attempt_rows()
    theorem = no_source_theorem_rows()
    body = first_body_charge_rows()
    acquisition = coefficient_acquisition_rows()
    refusals = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["signature_attempt"], signature)
    write_csv(OUTPUTS["no_source_theorem"], theorem)
    write_csv(OUTPUTS["first_body_charge_row"], body)
    write_csv(OUTPUTS["coefficient_acquisition"], acquisition)
    write_csv(OUTPUTS["runner_refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()

    DOC.write_text(
        build_doc(source_rows, signature, theorem, body, acquisition, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not validation_pass(OUTPUTS["validation"]):
        raise SystemExit(f"2250 validation failed: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
