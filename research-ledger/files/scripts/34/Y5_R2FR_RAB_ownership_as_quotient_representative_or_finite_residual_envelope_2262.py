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

BRANCH_ID = "MTS_R2FR_RAB_OWNERSHIP_QUOTIENT_OR_FINITE_ENVELOPE_2262"
DOC = ROOT / "2262-Y5-R2FR-RAB-ownership-as-quotient-representative-or-finite-residual-envelope.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2262_00_2261_doc",
        "source_key": "2261_doc",
        "source_path": ROOT / "2261-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-residual-row.md",
        "needles": ["OBS2261_0_RAB_ownership", "LIVE2261_0_RAB_parent_ownership_gap", "NEXT2261_0_primary"],
        "role": "handoff: R_AB ownership isolated as the fatal blocker",
    },
    {
        "source_id": "SRC2262_01_2261_validation",
        "source_key": "2261_validation",
        "source_path": OUT / "P8_Y5_BRR545_2261_VALIDATION.csv",
        "needles": ["VAL2261_OVERALL", "PASS"],
        "role": "confirms 2261 passed before 2262 starts",
    },
    {
        "source_id": "SRC2262_02_2261_live_row",
        "source_key": "2261_live_row",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2261_FIRST_LIVE_NONCLAIM_ROW.csv",
        "needles": ["LIVE2261_0_RAB_parent_ownership_gap", "MISSING_PARENT_RAB_OWNERSHIP_SIGNATURE"],
        "role": "first source-backed nonclaim R_AB ownership gap row",
    },
    {
        "source_id": "SRC2262_03_02_local_gr",
        "source_key": "local_gr_02",
        "source_path": ROOT / "02-motion-load-local-GR-reduction.md",
        "needles": ["T^2 S = 1", "gamma = p", "parent origin of reciprocal routing = missing"],
        "role": "conditional local-GR reduction and missing reciprocal origin",
    },
    {
        "source_id": "SRC2262_04_06_charge",
        "source_key": "charge_06",
        "source_path": ROOT / "06-reciprocal-charge-source-neutrality.md",
        "needles": ["Q_R = -Pi_R", "|q_R| <= 1e-5", "reciprocity remains conditional"],
        "role": "reciprocal hair/source-neutrality and PPN residual danger",
    },
    {
        "source_id": "SRC2262_05_07_constraint",
        "source_key": "constraint_07",
        "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": ["S_constraint = integral lambda_R R_AB", "no R_AB kinetic term", "parent origin is still open"],
        "role": "clean nonpropagating constraint route and lambda-origin blocker",
    },
    {
        "source_id": "SRC2262_06_08_phase",
        "source_key": "phase_08",
        "source_path": ROOT / "08-phase-volume-reciprocity-origin.md",
        "needles": ["T sqrt(S) = 1", "radial t-r clock-routing cell preservation", "candidate principle, not a parent theorem"],
        "role": "phase-cell motivation but not derivation",
    },
    {
        "source_id": "SRC2262_07_09_hamiltonian",
        "source_key": "hamiltonian_09",
        "source_path": ROOT / "09-hamiltonian-radial-cell-derivation.md",
        "needles": ["generic symplectic or Liouville phase-volume preservation does not derive p=1", "why the radial observer cell is separately conserved"],
        "role": "Hamiltonian route rejects generic phase-volume derivation",
    },
    {
        "source_id": "SRC2262_08_10_observer",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "R_AB normalization and exact missing theorem",
    },
    {
        "source_id": "SRC2262_09_11_current",
        "source_key": "current_11",
        "source_path": ROOT / "11-cell-current-origin-attempt.md",
        "needles": ["W partial_r R_AB = Q_R", "Q_R = 0", "ordinary cell-current conservation does not close"],
        "role": "ordinary current conservation leaves reciprocal hair",
    },
    {
        "source_id": "SRC2262_10_12_noether",
        "source_key": "noether_12",
        "source_path": ROOT / "12-gauge-noether-origin-audit.md",
        "needles": ["cell-scale gauge", "first-class parent constraint", "closure-only"],
        "role": "coordinate/gauge/Noether routes rejected in current scaffold",
    },
    {
        "source_id": "SRC2262_11_13_benchmark",
        "source_key": "benchmark_13",
        "source_path": ROOT / "13-local-closure-PPN-benchmark.md",
        "needles": ["R_AB=0 and Q_R=0 are closure assumptions", "gamma = 1", "gamma approx 1 + q_R"],
        "role": "closure benchmark and finite q_R sensitivity",
    },
    {
        "source_id": "SRC2262_12_581_vertical_chain",
        "source_key": "vertical_581",
        "source_path": OUT / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
        "needles": ["QVT581_0_parent_projection", "QVT581_7_alpha_result", "valid_for_claim"],
        "role": "generic quotient/vertical theorem chain, premises unfilled",
    },
    {
        "source_id": "SRC2262_13_590_field_map",
        "source_key": "field_map_590",
        "source_path": OUT / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
        "needles": ["metric_or_coframe", "domain_memory_projector_fields", "matter_readout"],
        "role": "field-by-field vertical generator gaps",
    },
    {
        "source_id": "SRC2262_14_590_gate",
        "source_key": "gate_590",
        "source_path": OUT / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv",
        "needles": ["MCG590_0_parent_Omega", "MCG590_2_vertical_generator", "MCG590_6_matter_quotient"],
        "role": "vertical map closure gate remains blocked",
    },
    {
        "source_id": "SRC2262_15_670_no_pole",
        "source_key": "nopole_670",
        "source_path": OUT / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
        "needles": ["NQ670_8_no_pole_result", "not_passed", "finite/edge/source residual vector retained"],
        "role": "no-pole quotient proof chain not passed",
    },
    {
        "source_id": "SRC2262_16_same_coframe",
        "source_key": "same_coframe_519",
        "source_path": OUT / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "needles": ["UOC519_0_single_coframe_field", "UOC519_5_no_conformal_disformal_shadow_frame", "conditional_clause_written"],
        "role": "same-observed-coframe guardrails against frame cheating",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2262_SOURCE_REGISTER.csv",
    "ownership_fork": OUT / "P8_Y5_PARENT_QLOC_2262_RAB_OWNERSHIP_FORK.csv",
    "vertical_gate": OUT / "P8_Y5_PARENT_QLOC_2262_VERTICAL_REPRESENTATIVE_GATE.csv",
    "constraint_route": OUT / "P8_Y5_PARENT_QLOC_2262_NONPROPAGATING_CONSTRAINT_AUDIT.csv",
    "finite_envelope": OUT / "P8_Y5_PARENT_QLOC_2262_FINITE_RAB_RESIDUAL_ENVELOPE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2262_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2262_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2262_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2262_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2262_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2262_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_envelope": QUEUE / "JR2262_FINITE_RAB_RESIDUAL_ENVELOPE_NONCLAIM.csv",
    "queue_decision": QUEUE / "JR2262_RAB_OWNERSHIP_DECISION_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_ownership_refusal_and_qR_envelope_2262.csv",
    "beta_docs": BETA_DOCS / "RAB_OWNERSHIP_VERTICAL_OR_FINITE_AUDIT_2262_NONCLAIM.csv",
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
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


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


def ownership_fork_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fork_id": "OWN2262_0_physical_observer_strain",
            "candidate_ownership": "R_AB is physical observer-cell strain",
            "test": "changing T sqrt(S) changes clock/routing cell and gamma proxy",
            "current_status": "DEFAULT_CURRENT_SCAFFOLD",
            "evidence": "observer cell and PPN benchmark treat R_AB/q_R as observable unless constrained",
            "consequence": "finite q_R envelope required if no parent constraint closes",
            "source_path": source_refs("observer_10", "benchmark_13", "charge_06"),
        },
        {
            "fork_id": "OWN2262_1_coordinate_gauge",
            "candidate_ownership": "R_AB is coordinate gauge",
            "test": "use radial coordinate freedom to set T^2 S=1",
            "current_status": "REJECTED",
            "evidence": "areal radius already fixes r; importing AB=1 from Schwarzschild equations is forbidden",
            "consequence": "cannot claim quotient/gauge from coordinate choice",
            "source_path": source_refs("noether_12"),
        },
        {
            "fork_id": "OWN2262_2_cell_scale_gauge",
            "candidate_ownership": "R_AB is observer-splitting gauge",
            "test": "cell-scale transformation leaves physics unchanged",
            "current_status": "REJECTED_CURRENT_SCAFFOLD",
            "evidence": "cell-scale gauge changes T sqrt(S), which changes local observables unless a new matter map is supplied",
            "consequence": "not a harmless representative variable in current matter/readout map",
            "source_path": source_refs("noether_12", "same_coframe_519"),
        },
        {
            "fork_id": "OWN2262_3_quotient_vertical",
            "candidate_ownership": "R_AB is vertical representative in ker(Dq_R)",
            "test": "Dq_R[v_R]=0, action/matter/boundary descend, no physical pole/edge charge",
            "current_status": "CONDITIONAL_NOT_PROVED",
            "evidence": "quotient kernels exist, but parent Omega, v_R map, boundary charge, degree count, and matter descent are unfilled",
            "consequence": "best theorem-zero route remains possible but inactive",
            "source_path": source_refs("vertical_581", "field_map_590", "gate_590", "nopole_670"),
        },
        {
            "fork_id": "OWN2262_4_nonpropagating_constraint",
            "candidate_ownership": "R_AB is algebraic/nonpropagating constraint",
            "test": "S_constraint=int lambda_R R_AB, no kinetic R_AB, no Q_R hair",
            "current_status": "CLEAN_BUT_PARENT_ORIGIN_OPEN",
            "evidence": "constraint route gives p=1/gamma=1 cleanly but lambda_R origin remains open",
            "consequence": "strongest derivation route is now lambda-origin constrained parent action, not generic quotient",
            "source_path": source_refs("constraint_07", "phase_08", "observer_10"),
        },
        {
            "fork_id": "OWN2262_5_finite_residual",
            "candidate_ownership": "R_AB is finite local residual",
            "test": "R_AB=q_R L+O(L^2), gamma-1≈q_R, empirical bounds apply",
            "current_status": "HONEST_FALLBACK_SELECTED_IF_DERIVATION_FAILS",
            "evidence": "source-neutrality and benchmark files give q_R sensitivity and closure-vs-deviation split",
            "consequence": "no GR derivation claim, but testable local residual programme",
            "source_path": source_refs("charge_06", "benchmark_13"),
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **row, "valid_for_claim": False, "claim_allowed": False} for row in rows]


def vertical_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("VRG2262_0_qR_map", "parent quotient map q_R", "q_R: Conf_parent -> Q_obs with Dq_R[v_R]=0", "CONDITIONAL_MATH_ONLY", "actual R_AB direction not identified with parent quotient fibre", "OWN2262_3_quotient_vertical"),
        ("VRG2262_1_vR_generator", "field-by-field v_R", "v_R on coframe, momenta, memory/projector, matter/readout, boundary", "MISSING_FIELD_MAP", "590 lists unmapped extra sectors and matter/readout gaps", "OWN2262_3_quotient_vertical"),
        ("VRG2262_2_action_descent", "bulk action descent", "S_bulk=S_red[q_R(Phi)] plus safe boundary terms", "CONDITIONAL_NOT_PARENT_SIGNED", "legacy action does not factor through q_R with R_AB removed", "OWN2262_3_quotient_vertical"),
        ("VRG2262_3_matter_descent", "matter/readout descent", "S_matter=Sbar[Obs(q_R(Phi)),Psi,theta] and no marker extension", "CONDITIONAL_NOT_PARENT_SIGNED", "same-coframe is a guardrail; it does not prove R_AB blindness", "OWN2262_3_quotient_vertical"),
        ("VRG2262_4_boundary_charge", "boundary/edge silence", "Q_R or Q_boundary[v_R]=0/proper/exact", "MISSING_BOUNDARY_ZERO", "current conservation leaves Q_R hair unless zero-charge theorem exists", "OWN2262_3_quotient_vertical"),
        ("VRG2262_5_degree_count", "first-class/constraint degree count", "constraints remove the R_AB pair before local inversion", "MISSING_PARENT_CONSTRAINT_ALGEBRA", "Noether identity alone does not create lambda_R constraint", "OWN2262_4_nonpropagating_constraint"),
        ("VRG2262_6_verdict", "vertical representative theorem", "all prior gates jointly close before matter/readout", "NOT_PROVED_CURRENT_CORPUS", "R_AB cannot be claimed vertical; finite envelope remains active", "OWN2262_5_finite_residual"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "required_statement": required,
            "current_status": status,
            "missing_or_failure": missing,
            "route_effect": effect,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, required, status, missing, effect in rows
    ]


def constraint_route_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "constraint_id": "NPR2262_0_algebraic_lock",
            "statement": "If S_constraint=int lambda_R R_AB is parent-derived, then variation gives R_AB=0.",
            "status": "EXACT_CONDITIONAL",
            "why_not_claimed": "lambda_R origin not derived from motion/time/space primitives",
            "source_path": source_refs("constraint_07", "observer_10"),
        },
        {
            "constraint_id": "NPR2262_1_no_hair",
            "statement": "No R_AB kinetic term means no Q_R=W R_AB' exterior hair.",
            "status": "EXACT_WITHIN_CONSTRAINT_ROUTE",
            "why_not_claimed": "only applies after nonpropagating route is parent-signed",
            "source_path": source_refs("constraint_07", "current_11"),
        },
        {
            "constraint_id": "NPR2262_2_phase_motivation",
            "statement": "T sqrt(S)=1 is the specific radial t-r cell rule that selects p=1.",
            "status": "MOTIVATED_NOT_DERIVED",
            "why_not_claimed": "Hamiltonian/Liouville arguments reject generic phase-volume derivation",
            "source_path": source_refs("phase_08", "hamiltonian_09"),
        },
        {
            "constraint_id": "NPR2262_3_best_derivation_route",
            "statement": "The least-posthoc route is a constrained parent action whose first-class/algebraic origin makes R_AB nonpropagating.",
            "status": "SELECTED_NEXT_ATTEMPT",
            "why_not_claimed": "needs lambda-origin construction and constraint algebra before any local-GR claim",
            "source_path": source_refs("noether_12", "constraint_07", "2261_doc"),
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **row, "valid_for_claim": False, "claim_allowed": False} for row in rows]


def finite_envelope_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ENV2262_0_qR_local_residual",
            "from_row": "LIVE2261_0_RAB_parent_ownership_gap",
            "quantity": "q_R",
            "definition": "first-order reciprocal strain amplitude R_AB = q_R L + O(L^2), L=2GM/(rc^2)",
            "units": "dimensionless",
            "observable_link": "gamma - 1 approximately q_R in the internal weak-field sensitivity model",
            "internal_bound_anchor": "|q_R| <= 1e-5 conservative local PPN danger threshold",
            "source_paths": source_refs("charge_06", "benchmark_13", "local_gr_02"),
            "current_value": "MISSING_PARENT_VALUE_OR_BOUND",
            "normalization_status": "SCHEMA_NORMALIZED_BY_L",
            "arena_projection": "PPN;R10;WEP;clock;orbital",
            "status": "FINITE_ENVELOPE_SCHEMA_READY_NONCLAIM",
            "score_ready": False,
            "accepted_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ENV2262_1_QR_boundary_hair",
            "from_row": "ACQ2260_4_BR",
            "quantity": "Q_R_or_Pi_R",
            "definition": "reciprocal boundary/source charge with Q_R=-Pi_R in the source matching audit",
            "units": "dimensionless_or_model_normalized_boundary_charge",
            "observable_link": "nonzero Q_R sources exterior R_AB hair and therefore q_R residual",
            "internal_bound_anchor": "must be zero by theorem or bounded by q_R envelope",
            "source_paths": source_refs("charge_06", "current_11"),
            "current_value": "MISSING_ZERO_CHARGE_THEOREM_OR_NUMERIC_BOUND",
            "normalization_status": "BOUNDARY_NORMALIZATION_NOT_COMPLETE",
            "arena_projection": "PPN;R10;orbital",
            "status": "FINITE_BOUNDARY_ENVELOPE_NONCLAIM",
            "score_ready": False,
            "accepted_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2262_0_RAB_vertical", "R_AB is proven vertical representative", "BLOCKED", "VRG2262_6_verdict=NOT_PROVED_CURRENT_CORPUS"),
        ("REF2262_1_coordinate_gauge", "R_AB=0 by coordinate gauge", "REJECTED", "areal radial scaffold forbids hiding AB=1 as gauge"),
        ("REF2262_2_noether", "Noether identity alone sets R_AB=0", "REJECTED", "Noether identity relates equations; it does not create lambda_R equation"),
        ("REF2262_3_constraint_claim", "nonpropagating constraint is parent-derived", "BLOCKED", "lambda_R origin and constraint algebra missing"),
        ("REF2262_4_qR_score", "finite q_R residual can be scored now", "BLOCKED", "missing parent coefficient/value/bound and arena projection kernels"),
        ("REF2262_5_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED", "neither parent constraint nor finite envelope bound closes"),
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
        ("CG2262_0_vertical_RAB", "R_AB quotient-vertical theorem", False, "field-by-field generator/action/matter/boundary/degree gates missing"),
        ("CG2262_1_nonprop_constraint", "parent-signed nonpropagating R_AB constraint", False, "lambda_R origin missing"),
        ("CG2262_2_QR_zero", "Q_R/Pi_R zero theorem", False, "current conservation leaves charge; source neutrality conditional"),
        ("CG2262_3_finite_envelope", "finite q_R residual score", False, "envelope schema has no parent value/bound"),
        ("CG2262_4_local_GR_Newton", "derived local GR/Newton/PPN safety", False, "only closure benchmark currently passes"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2262_0_ownership",
            "decision": "RAB_PHYSICAL_BY_DEFAULT_CURRENTLY",
            "reason": "in the current scaffold R_AB changes clock/routing observables unless a new parent constraint/quotient proof removes it first",
            "next_action": "do not claim zero; keep finite q_R envelope active",
        },
        {
            "decision_id": "DEC2262_1_quotient_route",
            "decision": "QUOTIENT_VERTICAL_ROUTE_NOT_CLOSED",
            "reason": "conditional quotient math exists but the actual R_AB vertical generator, parent Omega, boundary silence, and matter descent are unfilled",
            "next_action": "do not use quotient language as proof",
        },
        {
            "decision_id": "DEC2262_2_derivation_route",
            "decision": "CONSTRAINED_PARENT_ACTION_IS_BEST_NEXT_DERIVATION_ROUTE",
            "reason": "nonpropagating constraint cleanly kills Q_R hair and gives p=1 if lambda_R has a parent origin",
            "next_action": "try to derive lambda_R from motion-capacity/radial-cell principle",
        },
        {
            "decision_id": "DEC2262_3_fallback",
            "decision": "FINITE_QR_ENVELOPE_RETAINED",
            "reason": "if lambda origin fails, q_R is the honest local residual and must be bounded",
            "next_action": "carry ENV2262 rows as nonclaim acquisition inputs",
        },
        {
            "decision_id": "DEC2262_4_next",
            "decision": "LAMBDA_ORIGIN_OR_QR_ENVELOPE_RUNNER_NEXT",
            "reason": "the next step should either supply the missing parent constraint origin or begin quantitative residual bounding",
            "next_action": "2263-Y5-R2FR-RAB-constrained-parent-action-lambda-origin-or-qR-envelope-runner.md",
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **row, "valid_for_claim": False, "claim_allowed": False} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2262_0_primary",
            "next_target": "2263-Y5-R2FR-RAB-constrained-parent-action-lambda-origin-or-qR-envelope-runner.md",
            "script": "scripts/Y5_R2FR_RAB_constrained_parent_action_lambda_origin_or_qR_envelope_runner_2263.py",
            "objective": "attempt to derive the lambda_R R_AB nonpropagating constraint from motion-capacity/radial-cell primitives; if it fails, convert q_R/Q_R into a quantitative nonclaim PPN/R10 residual envelope runner",
            "selection_status": "selected",
            "success_condition": "lambda_R gains parent origin and constraint algebra, or q_R/Q_R rows gain complete value/bound/projection schemas while remaining nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2262_1_parallel",
            "next_target": "2263b-Y5-R2FR-RAB-ParentGenerate-operator-grammar-and-ZR-row.md",
            "script": "scripts/Y5_R2FR_RAB_ParentGenerate_operator_grammar_and_ZR_row_2263b.py",
            "objective": "formalize derivative-constructor exclusion for A_R and create finite Z_R/M_R^2 rows if exclusion fails",
            "selection_status": "held_parallel",
            "success_condition": "operator grammar proves no D R_AB or produces source-ready Z_R/M_R^2 placeholders",
            "valid_for_claim": False,
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2262_envelope",
            "source_path": rel(OUTPUTS["finite_envelope"]),
            "target_path": rel(COPY_TARGETS["queue_envelope"]),
            "target_exists": COPY_TARGETS["queue_envelope"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_envelope"]) if COPY_TARGETS["queue_envelope"].exists() else False,
            "reason": "finite q_R/Q_R envelope nonclaim acquisition copy",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2262_decision",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["queue_decision"]),
            "target_exists": COPY_TARGETS["queue_decision"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_decision"]) if COPY_TARGETS["queue_decision"].exists() else False,
            "reason": "portable ownership decision ledger",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2262_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]) if COPY_TARGETS["branch_wep"].exists() else False,
            "reason": "branch-locked local/WEP refusal gates",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2262_beta_docs",
            "source_path": rel(OUTPUTS["ownership_fork"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]) if COPY_TARGETS["beta_docs"].exists() else False,
            "reason": "portable ownership fork audit",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    ownership = read_csv(OUTPUTS["ownership_fork"])
    vertical = read_csv(OUTPUTS["vertical_gate"])
    constraint = read_csv(OUTPUTS["constraint_route"])
    envelope = read_csv(OUTPUTS["finite_envelope"])
    refusal = read_csv(OUTPUTS["refusal"])
    gates = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2262_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2262_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2262_2_prior_validation",
            any(row["source_key"] == "2261_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2261 validation passes",
        ),
        (
            "VAL2262_3_ownership_fork_complete",
            {row["fork_id"] for row in ownership}
            >= {
                "OWN2262_0_physical_observer_strain",
                "OWN2262_1_coordinate_gauge",
                "OWN2262_2_cell_scale_gauge",
                "OWN2262_3_quotient_vertical",
                "OWN2262_4_nonpropagating_constraint",
                "OWN2262_5_finite_residual",
            },
            "ownership fork covers physical, gauge, quotient, constraint, and finite routes",
        ),
        (
            "VAL2262_4_vertical_not_proved",
            any(row["gate_id"] == "VRG2262_6_verdict" and row["current_status"] == "NOT_PROVED_CURRENT_CORPUS" for row in vertical),
            "vertical representative route is not falsely promoted",
        ),
        (
            "VAL2262_5_constraint_route_selected",
            any(row["constraint_id"] == "NPR2262_3_best_derivation_route" and row["status"] == "SELECTED_NEXT_ATTEMPT" for row in constraint),
            "nonpropagating constrained parent action selected as next derivation attempt",
        ),
        (
            "VAL2262_6_finite_envelope_present",
            any(row["row_id"] == "ENV2262_0_qR_local_residual" and row["status"] == "FINITE_ENVELOPE_SCHEMA_READY_NONCLAIM" for row in envelope),
            "finite q_R local residual envelope present",
        ),
        (
            "VAL2262_7_envelope_nonclaim",
            all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in envelope),
            "finite envelope rows remain nonclaim and unscored",
        ),
        (
            "VAL2262_8_refusal_runner_blocks",
            all(row["claim_allowed"].lower() == "false" and row["score_eligible"].lower() == "false" for row in refusal),
            "refusal runner blocks all current claims",
        ),
        (
            "VAL2262_9_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in gates),
            "claim gates remain blocked",
        ),
        (
            "VAL2262_10_next_selected",
            any(row["route_id"] == "NEXT2262_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2263 lambda-origin or q_R-envelope target selected",
        ),
        ("VAL2262_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2262 CSVs parse"),
        (
            "VAL2262_12_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("accepted_ready", "score_ready", "valid_for_claim", "claim_allowed")
            ),
            "no generated score/claim flags are true",
        ),
        (
            "VAL2262_13_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2262_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2262_15_formalization_no_2262",
            not any(path.is_file() and "2262" in path.name for path in FORMALIZATION.rglob("*")),
            "formalization-workbench has no 2262 output files",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2262_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2262 rejects current R_AB vertical/gauge proof, keeps the nonpropagating constraint as the best derivation route, writes finite q_R envelope rows, and selects 2263",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    ownership = read_csv(OUTPUTS["ownership_fork"])
    vertical = read_csv(OUTPUTS["vertical_gate"])
    constraint = read_csv(OUTPUTS["constraint_route"])
    envelope = read_csv(OUTPUTS["finite_envelope"])
    refusal = read_csv(OUTPUTS["refusal"])
    gates = read_csv(OUTPUTS["claim_gates"])
    decision = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2262 - Y5/R2FR R_AB Ownership As Quotient Representative Or Finite Residual Envelope",
        "",
        "## Verdict",
        "",
        "`R_AB` is **physical-by-default** in the current scaffold: it changes the clock/routing observer cell and maps directly into the local `gamma-1` residual unless a parent constraint or quotient proof removes it before matter/readout.",
        "",
        "The coordinate-gauge and ordinary Noether/current routes are rejected by prior local audits. The quotient-vertical route remains a mathematically clean conditional, but it is not proved for the actual `R_AB` direction because the parent `Omega`, field-by-field vertical generator, boundary charge, degree count, and matter/no-marker descent are still unsigned.",
        "",
        "The best derivation route is therefore the nonpropagating constrained parent action: derive a real parent origin for `lambda_R R_AB`. If that fails, `R_AB` becomes a finite residual envelope with `R_AB = q_R L + O(L^2)` and `gamma-1 approximately q_R`.",
        "",
        "No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or `q_R` pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## R_AB Ownership Fork",
        table(["fork_id", "candidate_ownership", "current_status", "evidence", "consequence", "source_path", "valid_for_claim"], ownership),
        "",
        "## Vertical Representative Gate",
        table(["gate_id", "gate", "required_statement", "current_status", "missing_or_failure", "route_effect", "valid_for_claim"], vertical),
        "",
        "## Nonpropagating Constraint Route",
        table(["constraint_id", "statement", "status", "why_not_claimed", "source_path", "valid_for_claim"], constraint),
        "",
        "## Finite R_AB Residual Envelope",
        table(["row_id", "quantity", "definition", "units", "observable_link", "internal_bound_anchor", "current_value", "normalization_status", "arena_projection", "status", "score_ready", "valid_for_claim"], envelope),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], gates),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decision),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is the clean fork. If we want a derived GR lane, we now stop trying to make `R_AB` vanish by calling it gauge. The viable leap is narrower and better: derive the nonpropagating `lambda_R R_AB` constraint from motion-capacity/radial-cell primitives. If that cannot be done, the honest theory is not dead; it becomes a finite local residual theory with `q_R` bounded hard by PPN/clock/orbital/R10 channels.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["ownership_fork"], ownership_fork_rows())
    write_csv(OUTPUTS["vertical_gate"], vertical_gate_rows())
    write_csv(OUTPUTS["constraint_route"], constraint_route_rows())
    write_csv(OUTPUTS["finite_envelope"], finite_envelope_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["finite_envelope"], COPY_TARGETS["queue_envelope"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["queue_decision"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["ownership_fork"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
