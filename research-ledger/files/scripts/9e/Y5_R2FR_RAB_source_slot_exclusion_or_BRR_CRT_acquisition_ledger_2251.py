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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_SOURCE_SLOT_EXCLUSION_2251"
DOC = ROOT / "2251-Y5-R2FR-RAB-source-slot-exclusion-or-BRR-CRT-acquisition-ledger.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2251_00_2250_doc",
        "source_key": "2250_handoff",
        "source_path": ROOT / "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md",
        "needles": ["DEC2250_2_next", "NEXT2250_0_primary"],
        "role": "selects source-slot exclusion or B_RR/C_RT acquisition as 2251 target",
    },
    {
        "source_id": "SRC2251_01_2250_validation",
        "source_key": "2250_validation",
        "source_path": OUT / "P8_Y5_BRR545_2250_VALIDATION.csv",
        "needles": ["VAL2250_OVERALL", "PASS"],
        "role": "confirms 2250 passed before 2251 starts",
    },
    {
        "source_id": "SRC2251_02_2250_signature",
        "source_key": "2250_signature",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2250_RAB_SOURCE_SIGNATURE_ATTEMPT.csv",
        "needles": ["RSS2250_2_no_curvature_source_vertex", "MISSING_BRR_ZERO"],
        "role": "records the missing curvature/source vertex theorem",
    },
    {
        "source_id": "SRC2251_03_2250_acquisition",
        "source_key": "2250_acquisition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2250_BRR_CRT_QR_ACQUISITION_LEDGER.csv",
        "needles": ["ACQ2250_0_BRR", "ACQ2250_1_CRT", "ACQ2250_4_total"],
        "role": "source coefficient acquisition template to refine",
    },
    {
        "source_id": "SRC2251_04_1629_doc",
        "source_key": "1629_source_slot",
        "source_path": ROOT / "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md",
        "needles": ["RSE1629_7_verdict", "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS"],
        "role": "earlier R_AB source-slot exclusion failure and obstruction list",
    },
    {
        "source_id": "SRC2251_05_1629_validation",
        "source_key": "1629_validation",
        "source_path": OUT / "P8_Y5_BRR545_1629_VALIDATION.csv",
        "needles": ["VAL1629_OVERALL", "PASS"],
        "role": "confirms 1629 passed as nonclaim",
    },
    {
        "source_id": "SRC2251_06_1761_doc",
        "source_key": "1761_no_direct_vertex",
        "source_path": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
        "needles": ["NDV1761_4_current_verdict", "THEOREM_CONTRACT_READY_PARENT_UNSIGNED"],
        "role": "no-direct-matter-vertex grammar attempt and source-prefactor countermodels",
    },
    {
        "source_id": "SRC2251_07_1761_csv",
        "source_key": "1761_no_vertex_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
        "needles": ["NDV1761_0_target", "NDV1761_4_current_verdict"],
        "role": "machine-readable no-direct-vertex theorem status",
    },
    {
        "source_id": "SRC2251_08_1768_doc",
        "source_key": "1768_normal_form",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["ANF1768_6_current_verdict", "SCL1768_2_nonminimal_coupling"],
        "role": "action normal-form owner rule and nonminimal-source classification",
    },
    {
        "source_id": "SRC2251_09_1628_doc",
        "source_key": "1628_owner",
        "source_path": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
        "needles": ["SOC1628_6_verdict", "CE1628_1_direct_RAB_slot"],
        "role": "source-owner route fails direct R_AB slot and Pi_R clauses",
    },
    {
        "source_id": "SRC2251_10_1344_doc",
        "source_key": "1344_body_charge",
        "source_path": ROOT / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md",
        "needles": ["VERT1344_3_body_charge", "QX1344_2_zero_switch"],
        "role": "body charge warning and no-XR/source-charge precedent",
    },
    {
        "source_id": "SRC2251_11_1720_functor",
        "source_key": "1720_functor",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"],
        "role": "matter functor remains unsigned",
    },
    {
        "source_id": "SRC2251_12_1786_boundary",
        "source_key": "1786_boundary",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
        "needles": ["BMC1786_1_matter_interface", "BMC1786_5_verdict"],
        "role": "boundary/matter closure remains open",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2251_SOURCE_REGISTER.csv",
    "slot_exclusion": OUT / "P8_Y5_PARENT_QLOC_2251_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2251_COUNTERMODEL_LEDGER.csv",
    "acquisition": OUT / "P8_Y5_PARENT_QLOC_2251_BRR_CRT_QR_ACQUISITION_LEDGER.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2251_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2251_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2251_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2251_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2251_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2251_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_coeffs": QUEUE / "JR2251_BRR_CRT_QR_SOURCE_VECTOR_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_source_slot_BRR_CRT_QR_nonclaim_2251.csv",
    "beta_docs": BETA_DOCS / "RAB_SOURCE_SLOT_BRR_CRT_QR_2251_NONCLAIM.csv",
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


def slot_exclusion_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RSE2251_0_parent_object_language",
            "typed parent object language",
            "Allowed[S_parent] must decide before variation whether R_AB is an LHS operator variable, a constrained auxiliary, or a legal matter/source argument.",
            "NEEDED_EXACTLY",
            "current corpus has contracts but no complete signed parent syntax",
            "MISSING_PARENT_OBJECT_LANGUAGE_SIGNATURE",
        ),
        (
            "RSE2251_1_no_direct_RAB_matter_slot",
            "ordinary matter has no independent R_AB slot",
            "If S_matter = S_matter[Psi,e_obs(q(Phi)),theta] with no R_AB argument, then delta S_matter/delta R_AB=0 by chain rule.",
            "EXACT_CONDITIONAL_SUBTHEOREM",
            "works only after R_AB is excluded from hidden frames, support functions, measured constants, and readout masks",
            "MISSING_NO_DIRECT_RAB_SLOT_THEOREM",
        ),
        (
            "RSE2251_2_no_curvature_source_vertex",
            "curvature/source vertices vanish",
            "B_RR = delta^2 S_parent/(delta R_AB delta R_obs)=0 and C_RT = delta^2 S_parent/(delta R_AB delta T_H)=0 if no R_AB R_obs, R_AB T_H, or equivalent mixed source operator is legal.",
            "CONDITIONAL_VERTEX_ZERO",
            "normal-form owner rule classifies the term, but does not forbid it from the parent inventory",
            "MISSING_BRR_ZERO;MISSING_CRT_ZERO",
        ),
        (
            "RSE2251_3_no_source_only_scalar",
            "no inert reciprocal source scalar",
            "No sigma_source, w_A, W_source, domain marker, or active-source prefactor may multiply an R_AB source channel while staying absent from nongravitational readout.",
            "CONTRACT_READY_UNSIGNED",
            "source-only Hom/action-scale owner remains unsigned",
            "MISSING_SOURCE_ONLY_SCALAR_EXCLUSION",
        ),
        (
            "RSE2251_4_action_scale_measure_owner",
            "action scale and measure are universal or observable-owned",
            "Any overall matter action multiplier is either a common calibrated constant or a measured matter-sector parameter, never an independent R_AB source charge.",
            "NOT_PARENT_SIGNED",
            "classical field-normalization arguments do not remove action-scale/measure counterexamples",
            "MISSING_ACTION_SCALE_MEASURE_OWNER",
        ),
        (
            "RSE2251_5_boundary_worldtube_silence",
            "source-worldtube and boundary Pi_R slots are absent or bounded",
            "Q_R[body] and Pi_R vanish only if support, matching, boundary, and reference terms are all owned before variation or are separately bounded.",
            "NOT_PARENT_SIGNED",
            "exterior source-free proofs do not erase source-worldtube charge",
            "MISSING_QR_BODY_ZERO;MISSING_PIR_ZERO",
        ),
        (
            "RSE2251_6_hidden_readout_projector_silence",
            "hidden/readout/history/projector source tails are absent or bounded",
            "No post-variation readout, history kernel, projector commutator, or counterterm may reintroduce an R_AB source component.",
            "NOT_PARENT_SIGNED",
            "normal-form and boundary ledgers keep these channels open",
            "MISSING_TAIL_ZERO_OR_BOUND",
        ),
        (
            "RSE2251_7_verdict",
            "R_AB source-slot exclusion theorem",
            "RSE2251_0 through RSE2251_6 must close in the same parent branch before B_RR=C_RT=Q_R[body]=Pi_R=0 can be claimed.",
            "FAIL_CURRENT_CLAIM",
            "there is a simple covariant countermodel with B_RR, C_RT, or epsilon_RAB_source unless the object language forbids the slots",
            "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "status": status,
            "current_evidence": evidence,
            "gap": gap,
            "source_paths": src("2250_handoff", "1629_source_slot", "1761_no_direct_vertex", "1768_normal_form", "1628_owner"),
            **false_flags(),
        }
        for attempt_id, claim_piece, mathematical_form, status, evidence, gap in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CM2251_0_mixed_curvature_vertex",
            "Delta S = int sqrt(-g) (1/2 B_RR R_AB R_obs)",
            "generally covariant mixed curvature/source operator can exist unless parent syntax forbids R_AB R_obs",
            "B_RR remains a live acquisition coefficient",
            "parent no-mixed-curvature-vertex theorem or source-backed B_RR bound",
        ),
        (
            "CM2251_1_matter_trace_vertex",
            "Delta S = int sqrt(-g) C_RT R_AB T_H",
            "Hilbert source ownership alone does not forbid a pre-action mixed R_AB matter-trace vertex",
            "C_RT remains a live acquisition coefficient",
            "parent source-slot exclusion theorem or source-backed C_RT bound",
        ),
        (
            "CM2251_2_inert_source_scalar",
            "Delta S = int sqrt(-g) epsilon_RAB_source sigma_source R_AB",
            "a source-only scalar can be invisible to ordinary matter readout until the parent grammar excludes it",
            "epsilon_RAB_source remains a live prior/source width",
            "no-source-only Hom/action-scale theorem or sourced prior width",
        ),
        (
            "CM2251_3_body_charge_matching",
            "R_AB outside body = integral_body G_R rho_R dV + tails",
            "an exterior vacuum equation can still carry boundary data from Q_R[body]",
            "Q_R[body] remains a live local-GR/R10/PPN blocker",
            "body neutrality theorem or source-backed body-charge bound",
        ),
        (
            "CM2251_4_boundary_momentum",
            "Pi_R != 0 at source/support/boundary interface",
            "boundary/reference terms are not killed by ordinary-matter descent",
            "Pi_R remains a live boundary/acquisition coefficient",
            "Pi_R zero theorem or finite boundary momentum bound",
        ),
        (
            "CM2251_5_verdict",
            "covariance plus MOMS descent is insufficient",
            "all above countermodels survive unless a typed parent action explicitly excludes or bounds them",
            "source-slot proof rejected for current corpus",
            "move to explicit parent-action normal form or source-backed coefficient acquisition",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "why_survives": why_survives,
            "effect": effect,
            "what_kills_it": what_kills_it,
            "survives_current_constraints": True,
            **false_flags(),
        }
        for countermodel_id, countermodel, why_survives, effect, what_kills_it in rows
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACQ2251_0_BRR",
            "B_RR",
            "mixed R_AB-observed-curvature vertex coefficient",
            "|B_RR| <= theorem_zero_or_source_backed_bound",
            "parent Hessian delta^2 S_parent/(delta R_AB delta R_obs) and normalization to local arena basis",
            "MISSING_NO_VERTEX_THEOREM_OR_NUMERIC_BOUND",
            "R10;PPN;local_GR",
        ),
        (
            "ACQ2251_1_CRT",
            "C_RT",
            "mixed R_AB-Hilbert-source trace coefficient",
            "|C_RT| <= theorem_zero_or_source_backed_bound",
            "parent Hessian/source derivative delta^2 S_parent/(delta R_AB delta T_H) in same matter frame",
            "MISSING_SOURCE_SLOT_EXCLUSION_OR_NUMERIC_BOUND",
            "R10;WEP;PPN;orbital",
        ),
        (
            "ACQ2251_2_epsilon_RAB_source",
            "epsilon_RAB_source",
            "inert source-only reciprocal scalar/prior width",
            "|epsilon_RAB_source| <= theorem_zero_or_source_backed_prior_width",
            "source-only Hom/action-scale owner or explicit prior-width source",
            "MISSING_SOURCE_ONLY_SCALAR_ZERO_OR_WIDTH",
            "WEP;R10;PPN;clock",
        ),
        (
            "ACQ2251_3_QR_body",
            "Q_R_body",
            "body/source-worldtube reciprocal charge",
            "|Q_R[body]| <= int_body abs(W_R rho_R) dV + |Q_R_boundary|",
            "body model, W_R, rho_R source density, Green function normalization, boundary term",
            "MISSING_BODY_NEUTRALITY_OR_NUMERIC_BODY_CHARGE",
            "R10;PPN;orbital;local_GR",
        ),
        (
            "ACQ2251_4_PiR",
            "Pi_R",
            "boundary reciprocal momentum/source support term",
            "|Pi_R| <= theorem_zero_or_source_backed_boundary_bound",
            "boundary/support/reference variation and physical matching rule",
            "MISSING_PIR_ZERO_OR_BOUND",
            "boundary;R10;PPN;orbital",
        ),
        (
            "ACQ2251_5_tail_source_vector",
            "tail_R",
            "readout/history/projector/counterterm source-tail vector",
            "|tail_R| <= |C_readout_R| + ||K_history_R|| + ||Delta_projector_R|| + |C_counterterm_R|",
            "variation-before-readout theorem or finite tail coefficient rows",
            "MISSING_TAIL_ZERO_OR_BOUNDS",
            "clock;orbital;PPN;local_GR",
        ),
        (
            "ACQ2251_6_total_abs",
            "RAB_source_vector_abs",
            "absolute no-cancellation source vector",
            "S_R_abs = |B_RR|+|C_RT|+|epsilon_RAB_source|+|Q_R_body|+|Pi_R|+|tail_R|",
            "all component theorem-zero certificates or numeric/source-backed bounds in common units",
            "SCHEMA_READY_VALUES_MISSING",
            "all_local_arenas",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula_or_bound,
            "required_source": required_source,
            "current_status": current_status,
            "observable_link": observable_link,
            "units_status": "MISSING_COMMON_SOURCE_NORMALIZATION",
            "source_paths": src("2250_acquisition", "2249_bounds") if False else src("2250_acquisition", "1629_source_slot", "1768_normal_form", "1344_body_charge"),
            **false_flags(),
        }
        for acquisition_id, symbol, definition, formula_or_bound, required_source, current_status, observable_link in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2251_0_source_slot_theorem", "R_AB source-slot exclusion is derived", "BLOCKED", "RSE2251_7_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2251_1_BRR_CRT_zero", "B_RR=C_RT=0 by theorem", "BLOCKED", "mixed curvature/source vertex countermodels survive"),
        ("REF2251_2_source_vector_score", "RAB source vector is score-ready", "BLOCKED", "ACQ2251_6_total has missing component values and units"),
        ("REF2251_3_nohair_activation", "2248 no-hair source side activates", "BLOCKED", "Q_R[body], Pi_R, and tails remain open"),
        ("REF2251_4_local_empirical_claims", "R10/PPN/WEP/clock/orbital/local-GR comparisons are claimable", "BLOCKED", "no numeric source vector and no arena projection kernels"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": attempted_claim,
            "runner_result": runner_result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, attempted_claim, runner_result, blocked_by in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2251_0_source_slot", "parent source-slot exclusion theorem", "RSE2251_7 fails"),
        ("CG2251_1_BRR_CRT", "B_RR and C_RT theorem-zero or source-backed", "mixed vertex coefficients remain missing"),
        ("CG2251_2_body_boundary", "Q_R[body] and Pi_R theorem-zero or source-backed", "body/boundary rows remain symbolic"),
        ("CG2251_3_source_vector", "absolute R_AB source vector ready for arenas", "common units and component values missing"),
        ("CG2251_4_local_GR", "derived local GR/Newton branch", "source-slot, source-vector, operator, and projection gates blocked"),
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
            "decision_id": "DEC2251_0_theorem",
            "decision": "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED",
            "reason": "A clean theorem exists if the parent object language forbids R_AB source slots and mixed vertices, but current corpus does not sign that object language.",
            "next_action": "do not set B_RR=C_RT=Q_R[body]=Pi_R=0",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2251_1_countermodel",
            "decision": "MIXED_VERTEX_COUNTERMODEL_SURVIVES",
            "reason": "Delta S terms B_RR R_AB R_obs and C_RT R_AB T_H are not removed by covariance, Hilbert source ownership, or MOMS descent alone.",
            "next_action": "force these terms into parent-action normal form with owner/forbid/bound labels",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2251_2_acquisition",
            "decision": "BRR_CRT_QR_PIR_ACQUISITION_LEDGER_STAGED_NONCLAIM",
            "reason": "The fallback source vector now has explicit components and no-cancellation structure, but no numeric/source-backed values.",
            "next_action": "build explicit parent action normal-form slot inventory before attempting another zero proof",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2251_3_next",
            "decision": "MINIMAL_PARENT_ACTION_RAB_SOURCE_VECTOR_NORMAL_FORM_NEXT",
            "reason": "The least-circular next move is not another prose exclusion attempt; it is a concrete parent-action slot inventory that either forbids, owns, or bounds each source term.",
            "next_action": "2252-Y5-R2FR-minimal-parent-action-RAB-source-vector-normal-form-or-closure-declaration.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2251_0_primary",
            "next_target": "2252-Y5-R2FR-minimal-parent-action-RAB-source-vector-normal-form-or-closure-declaration.md",
            "script": "scripts/Y5_R2FR_minimal_parent_action_RAB_source_vector_normal_form_or_closure_declaration_2252.py",
            "objective": "write the minimal parent action slot inventory for R_AB and classify every source-looking term as forbidden by syntax, LHS operator-owned, boundary-owned, or finite residual; no zero claim unless the slot is actually absent in the same action.",
            "selection_status": "selected",
            "success_condition": "each of B_RR, C_RT, epsilon_RAB_source, Q_R[body], Pi_R, and tail_R has a signed owner/forbid/bound status without cancellation credit",
            "forbidden_shortcuts": "another MOMS-only proof; covariance-only exclusion; invented coefficient values; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2251_1_fallback",
            "next_target": "2252b-Y5-R2FR-BRR-CRT-source-vector-bound-runner.md",
            "script": "scripts/Y5_R2FR_BRR_CRT_source_vector_bound_runner_2252b.py",
            "objective": "if the parent action slot inventory cannot be signed, build a refusal runner for numeric/source-backed bounds on B_RR, C_RT, epsilon_RAB_source, Q_R[body], Pi_R, and tail_R",
            "selection_status": "held_fallback",
            "success_condition": "runner refuses all rows with MISSING values and accepts only numeric, sourced, unit-matched residual bounds",
            "forbidden_shortcuts": "setting priors to zero; tau=1 shortcuts; cancellation between source components",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_coeffs", OUTPUTS["acquisition"], COPY_TARGETS["queue_coeffs"], "R_AB source vector acquisition queue"),
        ("branch_wep", OUTPUTS["acquisition"], COPY_TARGETS["branch_wep"], "WEP branch locked R_AB source-slot coefficient copy"),
        ("beta_docs", OUTPUTS["acquisition"], COPY_TARGETS["beta_docs"], "beta-source docs R_AB source-slot coefficient copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2251_{copy_id}",
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
    slot = read_csv(OUTPUTS["slot_exclusion"])
    countermodels = read_csv(OUTPUTS["countermodels"])
    acquisition = read_csv(OUTPUTS["acquisition"])
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

    formalization_2251 = []
    if FORMALIZATION.exists():
        formalization_2251 = [path for path in FORMALIZATION.rglob("*2251*") if path.is_file()]

    all_rows = [row for path in paths for row in read_csv(path)]
    rows = [
        check("VAL2251_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2251_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2251_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2250 and 1629 validations pass where checked"),
        check("VAL2251_3_slot_theorem_refused", any(row["attempt_id"] == "RSE2251_7_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in slot), "source-slot exclusion theorem is not promoted"),
        check("VAL2251_4_countermodels_retained", all(row["survives_current_constraints"] == "True" for row in countermodels), "mixed/source countermodels remain active"),
        check("VAL2251_5_acquisition_values_missing", any(row["acquisition_id"] == "ACQ2251_6_total_abs" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in acquisition), "source vector acquisition ledger is not score-ready"),
        check("VAL2251_6_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2251_7_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2251_8_decision_next", any(row["decision_id"] == "DEC2251_3_next" and "MINIMAL_PARENT_ACTION" in row["decision"] for row in decisions), "decision selects parent-action slot inventory next"),
        check("VAL2251_9_next_selected", any(row["route_id"] == "NEXT2251_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2251_10_csv_parse", csv_parse_ok, "all generated 2251 CSVs parse"),
        check("VAL2251_11_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        check("VAL2251_12_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2251_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2251_14_formalization_no_2251", not formalization_2251, "formalization-workbench has no 2251 outputs"),
    ]
    rows.append(
        check(
            "VAL2251_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2251 rejects source-slot exclusion from current premises, preserves mixed-vertex countermodels, stages B_RR/C_RT/Q_R/Pi_R acquisition, and selects minimal parent-action slot inventory next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    slot: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
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
            "# 2251 - Y5/R2FR R_AB Source-Slot Exclusion Or B_RR/C_RT Acquisition Ledger",
            "## Verdict\n\n2251 takes the derivation-first route and tries to prove that the parent object language forbids independent `R_AB` source slots and mixed curvature/source vertices. The result is a useful rejection: the clean theorem is exact if the parent syntax is signed, but the current corpus does not sign it. A covariant parent action can still contain `B_RR R_AB R_obs`, `C_RT R_AB T_H`, an inert source scalar, or body/boundary source charge unless those slots are explicitly forbidden or bounded.\n\nSo this is not a local-GR/R10/PPN/WEP win. The gain is sharper: the coupling gap has been reduced to a concrete no-cancellation source vector, and the next non-circular move is to write the minimal parent-action slot inventory that either forbids, owns, or bounds each term.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Source-Slot Exclusion Attempt\n" + markdown_table(slot, ["attempt_id", "claim_piece", "mathematical_form", "status", "current_evidence", "gap", "valid_for_claim"]),
            "## Countermodel Ledger\n" + markdown_table(countermodels, ["countermodel_id", "countermodel", "why_survives", "effect", "what_kills_it", "survives_current_constraints", "valid_for_claim"]),
            "## B_RR/C_RT/Q_R Acquisition Ledger\n" + markdown_table(acquisition, ["acquisition_id", "symbol", "definition", "formula_or_bound", "required_source", "current_status", "observable_link", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis does move us forward. We did not prove the source-slot theorem, but we now know why we cannot honestly claim it: mixed `R_AB` source vertices are legal countermodels unless a typed parent action removes them. That is better than circling. The next checkpoint should write the actual slot inventory rather than trying to infer absence from nice words like covariance, descent, or Hilbert source owner. If the slot is absent in that inventory, we can derive zero; if it is present, it becomes a finite residual for tests.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    write_csv(OUTPUTS["source_register"], source_rows)

    slot = slot_exclusion_rows()
    countermodels = countermodel_rows()
    acquisition = acquisition_rows()
    refusals = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["slot_exclusion"], slot)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["acquisition"], acquisition)
    write_csv(OUTPUTS["runner_refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["slot_exclusion"],
        OUTPUTS["countermodels"],
        OUTPUTS["acquisition"],
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
        build_doc(source_rows, slot, countermodels, acquisition, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2251 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
