from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1559_doc": ROOT / "1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md",
    "1559_validation": OUT / "P8_Y5_BRR545_1559_VALIDATION.csv",
    "1559_next": OUT / "P8_Y5_PARENT_QLOC_1559_NEXT_TARGET.csv",
    "1559_zero": OUT / "P8_Y5_PARENT_QLOC_1559_PARENT_ZERO_CONDITION_HUNT.csv",
    "1559_model": OUT / "P8_Y5_PARENT_QLOC_1559_TWO_PARAMETER_MODEL.csv",
    "10_doc": ROOT / "10-observer-map-symplectic-contract.md",
    "13_doc": ROOT / "13-local-closure-PPN-benchmark.md",
    "04_doc": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_doc": ROOT / "05-reciprocity-theorem-attempt.md",
    "07_doc": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "19_doc": ROOT / "19-constrained-parent-action-skeleton.md",
    "538_doc": ROOT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
    "1008_doc": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
}

NEEDLES = {
    "1559_doc": ["CONTROL_RUNNER_READY_ZERO_THEOREM_MISSING", "Parent Zero-Condition Hunt"],
    "1559_validation": ["VAL1559_OVERALL", "PASS"],
    "1559_next": ["1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md"],
    "1559_zero": ["ZERO1559_0_qR_linear", "MISSING_SECOND_ORDER_PARENT_COMPLETION"],
    "1559_model": ["MODEL1559_0_gamma", "MODEL1559_6_mercury_combo"],
    "10_doc": ["A future parent action may pass only if it produces", "R_AB = ln(T^2 S) = 0"],
    "13_doc": ["valid local GR control baseline", "not a parent derivation"],
    "04_doc": ["vacuum_reciprocity_action_contract_locked_not_satisfied", "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R"],
    "05_doc": ["W R_AB' = Q_R.", "The missing theorem is source matching"],
    "07_doc": ["S_constraint = integral lambda_R R_AB.", "why does the parent motion-load action contain lambda_R"],
    "19_doc": ["closure_term.", "beta=1, still open"],
    "538_doc": ["conditional_Euler_Ward_chain_only_no_PiM", "DAT537_4"],
    "1008_doc": ["parent `theta_MTS` and `Q_tau^MTS` extraction attempted; not closed", "missing_explicit_current_chain"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1560_SOURCE_REGISTER.csv"
WEAK_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1560_WEAK_FIELD_DERIVATION_ATTEMPT.csv"
QR_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1560_QR_ZERO_ROUTE_AUDIT.csv"
BETA_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1560_BETA_ZERO_ROUTE_AUDIT.csv"
CONDITIONAL_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1560_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv"
CLOSURE_DEMOTION = OUT / "P8_Y5_PARENT_QLOC_1560_BOUNDED_CLOSURE_DEMOTION.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1560_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1560_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1560_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1560_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1560_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1560"
QUAR_WEAK = QUARANTINE / "WEAK_FIELD_DERIVATION_ATTEMPT_NONCLAIM.csv"
QUAR_QR = QUARANTINE / "QR_ZERO_ROUTE_AUDIT_NONCLAIM.csv"
QUAR_BETA = QUARANTINE / "BETA_ZERO_ROUTE_AUDIT_NONCLAIM.csv"
QUAR_CONTRACT = QUARANTINE / "CONDITIONAL_ZERO_THEOREM_CONTRACT_NONCLAIM.csv"
QUAR_DEMOTION = QUARANTINE / "BOUNDED_CLOSURE_DEMOTION_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_WEAK = BRANCH_RESIDUALS / "weak_field_derivation_attempt_nonclaim_1560.csv"
BRANCH_QR = BRANCH_RESIDUALS / "qR_zero_route_audit_nonclaim_1560.csv"
BRANCH_BETA = BRANCH_RESIDUALS / "beta_zero_route_audit_nonclaim_1560.csv"
BRANCH_CONTRACT = BRANCH_RESIDUALS / "conditional_zero_theorem_contract_nonclaim_1560.csv"
BRANCH_DEMOTION = BRANCH_RESIDUALS / "bounded_closure_demotion_nonclaim_1560.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "weak_field_zero_runner_nonclaim_1560.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "weak_field_zero_decision_nonclaim_1560.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1560_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for parent weak-field q_R/beta zero-condition derivation attempt",
                **flags(),
            }
        )
    return rows


def weak_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WF1560_0_translation",
            "weak-field dictionary",
            "R_AB ~= q_R L and q_R = gamma-1",
            "first-order local PPN translation already derived",
            "DERIVED_TRANSLATION_ONLY",
            "does not prove q_R=0; it only shows what must vanish",
        ),
        (
            "WF1560_1_qR_target",
            "first-order zero condition",
            "parent equations must force R_AB=O(L^2)",
            "then q_R=0 and gamma=1 at first PPN order",
            "TARGET_THEOREM_NOT_SIGNED",
            "requires field equation, boundary condition, zero charge, and matter readout",
        ),
        (
            "WF1560_2_kinetic_route",
            "reciprocal-strain kinetic variation",
            "d/dr(W R_AB')=J_R gives W R_AB'=Q_R in vacuum",
            "allows reciprocal hair unless Q_R=0 is separately proven",
            "REJECTED_AS_CURRENT_ZERO_PROOF",
            "kinetic route converts the problem into a zero-charge theorem",
        ),
        (
            "WF1560_3_constraint_route",
            "auxiliary multiplier constraint",
            "delta lambda_R -> R_AB=0",
            "would prove q_R=0 if lambda_R R_AB is parent-owned and not an inserted closure",
            "CONDITIONAL_UNSIGNED",
            "current skeleton labels this a closure term",
        ),
        (
            "WF1560_4_EH_Ward_route",
            "EH plus silent exterior route",
            "covariant variation and Noether/Ward chain can conditionally recover GR-like weak field",
            "conditional chain fails current source/PiM/current-chain ownership",
            "CONDITIONAL_NOT_MTS_PARENT_DERIVATION",
            "EH reference cannot be used as the whole MTS parent action",
        ),
        (
            "WF1560_5_beta_target",
            "second-order beta zero condition",
            "parent equations must fix beta-1=delta_beta=0 at O(U^2)",
            "requires nonlinear self-coupling, source normalization, Bianchi/Ward identity, and gauge/readout map",
            "MISSING_SECOND_ORDER_PARENT_COMPLETION",
            "closure benchmark uses beta=1 but does not derive it",
        ),
        (
            "WF1560_6_verdict",
            "current derivation status",
            "no current parent weak-field action derives both q_R=0 and delta_beta=0",
            "local branch remains useful as a bounded closure control lane",
            "DERIVATION_FAILED_DEMOTE_TO_BOUNDED_CLOSURE",
            "next route must build/test a minimal parent weak-field action ansatz",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "route": route,
            "equation_or_condition": equation_or_condition,
            "consequence": consequence,
            "status": status,
            "limitation": limitation,
            "source_paths": source_list("1559_zero", "04_doc", "05_doc", "07_doc", "19_doc", "538_doc", "1008_doc"),
            **flags(),
        }
        for attempt_id, route, equation_or_condition, consequence, status, limitation in rows
    ]


def qR_route_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QR1560_0_kinetic",
            "kinetic reciprocal-strain equation",
            "d/dr(W R_AB')=0",
            "R_AB can carry Q_R hair",
            "FAILS_CURRENT_ZERO_PROOF",
            "needs independent Q_R=0 theorem",
        ),
        (
            "QR1560_1_boundary",
            "asymptotic/local boundary condition",
            "R_AB(infinity)=0 plus regularity",
            "kills integration constant but not necessarily Q_R source/boundary hair",
            "INSUFFICIENT",
            "must prove no source boundary charge",
        ),
        (
            "QR1560_2_multiplier",
            "lambda_R auxiliary constraint",
            "delta lambda_R -> R_AB=0",
            "would close q_R=0 exactly",
            "CONDITIONAL_UNSIGNED",
            "lambda_R term is currently closure_term, not parent-derived",
        ),
        (
            "QR1560_3_first_class",
            "first-class constraint/no-charge generator",
            "C_R=R_AB with zero/proper boundary charge",
            "would make reciprocal strain gauge/constrained rather than propagating",
            "POSSIBLE_NOT_PRESENT",
            "generator, bracket closure, degree count, and boundary charge not supplied",
        ),
        (
            "QR1560_4_EH_import",
            "Einstein exterior equations",
            "AB=1 in Schwarzschild/vacuum GR",
            "would give q_R=0 by importing GR",
            "FORBIDDEN_AS_MTS_DERIVATION",
            "not allowed to smuggle in the target theorem",
        ),
        (
            "QR1560_5_current",
            "accepted current route",
            "none",
            "q_R=0 is not parent-derived at 1560",
            "NO_ACCEPTED_PARENT_ZERO_ROUTE",
            "bounded closure lane retained",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "test_equation": test_equation,
            "result": result,
            "status": status,
            "missing_or_forbidden": missing_or_forbidden,
            "source_paths": source_list("04_doc", "05_doc", "07_doc", "10_doc", "13_doc", "1559_zero"),
            **flags(),
        }
        for route_id, route, test_equation, result, status, missing_or_forbidden in rows
    ]


def beta_route_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BETA1560_0_closure_completion",
            "exact Schwarzschild-equivalent completion",
            "beta=1 in the closure control lane",
            "works as benchmark, not parent derivation",
            "CLOSURE_ONLY",
            "requires parent origin for the second-order metric/coframe terms",
        ),
        (
            "BETA1560_1_EH_plus_silent",
            "minimal EH plus silent-sector parent",
            "standard nonlinear GR self-coupling gives beta=1",
            "conditional if the observed metric/source charge is parent-owned",
            "CONDITIONAL_NOT_CURRENT_MTS",
            "Pi_M/source-charge/current-chain ownership remains open",
        ),
        (
            "BETA1560_2_second_order_action",
            "MTS second-order weak-field action",
            "delta_e S_parent fixes O(U^2) coefficient",
            "not available as an explicit MTS variation",
            "MISSING_PARENT_VARIATION",
            "write and vary the actual local parent Lagrangian",
        ),
        (
            "BETA1560_3_Bianchi_Ward",
            "Bianchi/Ward identity",
            "conservation fixes nonlinear source and gauge consistency",
            "identity contract exists, but sector-by-sector parent action is not extracted",
            "MISSING_PARENT_IDENTITY",
            "derive dJ or nabla E identity with all retained sectors",
        ),
        (
            "BETA1560_4_extra_modes",
            "extra local modes",
            "silent/decoupled sectors leave beta unchanged",
            "no general silence theorem for all retained local residuals",
            "MISSING_MODE_DECOUPLING",
            "prove no scalar/tracefree/fifth-force local hair or keep residual bounds",
        ),
        (
            "BETA1560_5_current",
            "accepted current route",
            "none",
            "delta_beta=0 is not parent-derived at 1560",
            "NO_ACCEPTED_PARENT_BETA_ROUTE",
            "bounded closure lane retained",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "test_equation": test_equation,
            "result": result,
            "status": status,
            "missing_or_forbidden": missing_or_forbidden,
            "source_paths": source_list("10_doc", "13_doc", "19_doc", "538_doc", "1008_doc", "1559_zero"),
            **flags(),
        }
        for route_id, route, test_equation, result, status, missing_or_forbidden in rows
    ]


def conditional_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("COND1560_0_L_parent", "explicit parent weak-field action", "L_parent with fields, variations, retained sectors, and boundary terms", "without this, no Euler equation is owned", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND1560_1_R_constraint", "reciprocal zero mechanism", "R_AB auxiliary/first-class constraint or kinetic route plus proven Q_R=0", "needed to force R_AB=O(L^2)", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND1560_2_source", "Newton/source normalization", "T^2=1-2U/c^2 and measured GM are derived from the same parent charge", "otherwise beta/gamma can be calibrated after the fact", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND1560_3_matter", "universal matter/coframe descent", "matter, clocks, and photons read the same observed coframe", "otherwise local bounds do not test one geometry", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND1560_4_second_order", "second-order weak-field completion", "O(U^2) metric/coframe equation yields beta=1", "needed for delta_beta=0", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND1560_5_identity", "Bianchi/Ward identity", "parent equations imply the conservation identity tying source and field equations", "prevents inconsistent source normalization and beta drift", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND1560_6_silence", "no extra local hair", "scalar/vector/tracefree/fifth-force sectors vanish, decouple, or are explicitly bounded", "needed before local GR is exact rather than residual-bounded", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND1560_7_consequence", "conditional theorem consequence", "if COND1560_0 through COND1560_6 hold, then q_R=0 and delta_beta=0 in the local branch", "conditional theorem shape is clear", "CONDITIONAL_THEOREM_UNSIGNED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "premise": premise,
            "required_statement": required_statement,
            "why_needed": why_needed,
            "status": status,
            "source_paths": source_list("10_doc", "19_doc", "538_doc", "1008_doc", "1559_zero"),
            **flags(),
        }
        for contract_id, premise, required_statement, why_needed, status in rows
    ]


def demotion_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEM1560_0_local_GR_branch",
            "local GR/Newton branch",
            "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED",
            "q_R=0 and delta_beta=0 are not parent-signed",
            "use 1559 runner as control harness; do not claim derived GR",
        ),
        (
            "DEM1560_1_qR",
            "q_R local spatial reciprocal hair",
            "BOUNDED_PARAMETER",
            "Cassini/gamma clamps any nonzero q_R through q_R=gamma-1",
            "retain q_R bound box unless zero theorem closes",
        ),
        (
            "DEM1560_2_delta_beta",
            "delta_beta nonlinear drift",
            "BOUNDED_PARAMETER",
            "beta/ephemeris row clamps beta drift; Mercury has q_R degeneracy",
            "retain two-parameter PPN control runner",
        ),
        (
            "DEM1560_3_parent_program",
            "parent field theory route",
            "ACTIVE_DERIVATION_TARGET",
            "conditional theorem shows exactly what the parent action must provide",
            "next build minimal ansatz and run Euler/Ward/PPN gates",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": demotion_id,
            "object": obj,
            "new_status": new_status,
            "reason": reason,
            "allowed_use": allowed_use,
            "source_paths": source_list("1559_model", "1559_zero", "13_doc", "538_doc"),
            **flags(),
        }
        for demotion_id, obj, new_status, reason, allowed_use in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1560_0_sources",
            "test": "all derivation source contracts loaded",
            "current_status": "PASS",
            "detail": "source register covers 1559, local closure, reciprocity action, constrained action skeleton, Euler/Ward, and parent current-chain audit",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1560_1_qR_derivation",
            "test": "derive q_R=0",
            "current_status": "FAILED_CURRENT_PARENT_DERIVATION",
            "detail": "kinetic route leaves Q_R hair; multiplier route is closure unless parent-owned; first-class route is absent",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1560_2_beta_derivation",
            "test": "derive delta_beta=0",
            "current_status": "FAILED_CURRENT_PARENT_DERIVATION",
            "detail": "second-order MTS parent variation and Bianchi/source identity are not supplied",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1560_3_conditional_theorem",
            "test": "conditional zero theorem shape",
            "current_status": "PASS_CONDITIONAL_UNSIGNED",
            "detail": "the theorem can be stated if explicit parent action, reciprocal zero mechanism, source normalization, matter descent, beta completion, Ward identity, and no-extra-mode premises are supplied",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1560_4_demotion",
            "test": "local branch status",
            "current_status": "DERIVATION_FAILED_DEMOTED_TO_BOUNDED_CLOSURE",
            "detail": "1559 control runner remains valid as a nonclaim local residual harness",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1560_0_qR_zero", "q_R=0 parent theorem", "BLOCKED_NO_CLAIM", "no accepted current parent zero route"),
        ("GATE1560_1_beta_zero", "delta_beta=0 parent theorem", "BLOCKED_NO_CLAIM", "second-order parent completion missing"),
        ("GATE1560_2_constraint", "lambda_R constraint as derivation", "BLOCKED_NO_CLAIM", "lambda_R term currently functions as closure unless parent origin is supplied"),
        ("GATE1560_3_EH_reference", "EH route as MTS derivation", "BLOCKED_NO_CLAIM", "EH/Noether route is conditional/reference only without MTS current-chain ownership"),
        ("GATE1560_4_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "bounded closure control lane only"),
        ("GATE1560_5_empirical_score", "local PPN empirical success claim", "BLOCKED_NO_CLAIM", "control runner scores hypothetical leak vectors, not a parent-predicted vector"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1559_zero", "10_doc", "19_doc", "538_doc", "1008_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1560_0_verdict",
            "decision": "parent weak-field zero theorem",
            "result": "CURRENT_DERIVATION_FAILS_CONDITIONAL_THEOREM_WRITTEN",
            "reason": "the required theorem shape is clear, but the current corpus lacks the explicit parent action/variation and zero-charge/second-order completion needed to sign it",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1560_1_branch_status",
            "decision": "local GR branch status",
            "result": "DEMOTE_TO_BOUNDED_CLOSURE_CONTROL_LANE",
            "reason": "1559 PPN runner remains useful, but local GR/Newton is not parent-derived",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1560_2_next",
            "decision": "next target",
            "result": "NEXT_1561_MINIMAL_PARENT_WEAK_FIELD_ACTION_ANSATZ",
            "reason": "the most direct repair is to write a minimal parent weak-field ansatz and run Euler/Ward/PPN zero gates against it",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1560_0_1561",
            "next_target": "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
            "script": "scripts/Y5_minimal_parent_weak_field_action_ansatz_and_Euler_Ward_PPN_gate.py",
            "objective": "construct a minimal parent weak-field action ansatz with explicit R_AB auxiliary/constraint sector, source normalization, universal coframe matter coupling, and second-order beta terms; vary/gate it to see whether q_R=0 and delta_beta=0 can be parent-signed or must remain bounded closure",
            "do_not": "do not promote a closure multiplier to derivation without parent-origin and zero-stress proof; do not claim local GR/Newton reduction; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (WEAK_ATTEMPT, QUAR_WEAK),
        (QR_AUDIT, QUAR_QR),
        (BETA_AUDIT, QUAR_BETA),
        (CONDITIONAL_CONTRACT, QUAR_CONTRACT),
        (CLOSURE_DEMOTION, QUAR_DEMOTION),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (WEAK_ATTEMPT, BRANCH_WEAK),
        (QR_AUDIT, BRANCH_QR),
        (BETA_AUDIT, BRANCH_BETA),
        (CONDITIONAL_CONTRACT, BRANCH_CONTRACT),
        (CLOSURE_DEMOTION, BRANCH_DEMOTION),
        (RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    weak = read_csv(WEAK_ATTEMPT)
    qr = read_csv(QR_AUDIT)
    beta = read_csv(BETA_AUDIT)
    contract = read_csv(CONDITIONAL_CONTRACT)
    demotion = read_csv(CLOSURE_DEMOTION)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1560_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1560 source paths exist"),
        ("VAL1560_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1560_2_weak_verdict", any(row["attempt_id"] == "WF1560_6_verdict" and row["status"] == "DERIVATION_FAILED_DEMOTE_TO_BOUNDED_CLOSURE" for row in weak), "weak-field derivation verdict is explicit"),
        ("VAL1560_3_qR_no_route", any(row["route_id"] == "QR1560_5_current" and row["status"] == "NO_ACCEPTED_PARENT_ZERO_ROUTE" for row in qr), "q_R has no accepted parent zero route"),
        ("VAL1560_4_beta_no_route", any(row["route_id"] == "BETA1560_5_current" and row["status"] == "NO_ACCEPTED_PARENT_BETA_ROUTE" for row in beta), "delta_beta has no accepted parent route"),
        ("VAL1560_5_contract_complete", len(contract) >= 8 and any(row["contract_id"] == "COND1560_7_consequence" and row["status"] == "CONDITIONAL_THEOREM_UNSIGNED" for row in contract), "conditional zero theorem contract written"),
        ("VAL1560_6_demotion", any(row["demotion_id"] == "DEM1560_0_local_GR_branch" and row["new_status"] == "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED" for row in demotion), "local GR branch demoted to bounded closure control"),
        ("VAL1560_7_runner_demotion", any(row["runner_id"] == "RUN1560_4_demotion" and row["current_status"] == "DERIVATION_FAILED_DEMOTED_TO_BOUNDED_CLOSURE" for row in run_rows), "runner records derivation failure and demotion"),
        ("VAL1560_8_claim_gates", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL1560_9_decision_next", any(row["result"] == "NEXT_1561_MINIMAL_PARENT_WEAK_FIELD_ACTION_ANSATZ" for row in decision_items), "decision selects minimal parent weak-field action ansatz next"),
        ("VAL1560_10_next_target", any("1561-Y5-minimal-parent-weak-field-action" in row["next_target"] for row in next_rows), "next target is minimal parent weak-field action ansatz"),
        ("VAL1560_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1560 CSVs parse cleanly"),
        ("VAL1560_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1560_13_branch_copies", all(path.exists() for path in [QUAR_WEAK, QUAR_QR, QUAR_BETA, QUAR_CONTRACT, QUAR_DEMOTION, QUAR_RUNNER, QUAR_DECISION, BRANCH_WEAK, BRANCH_QR, BRANCH_BETA, BRANCH_CONTRACT, BRANCH_DEMOTION, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1560_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1560_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1560_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1560 parent weak-field zero-condition derivation or demotion validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    weak: list[dict[str, Any]],
    qr: list[dict[str, Any]],
    beta: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1560 - Parent Weak-Field Zero-Condition Derivation or Demotion",
                "",
                "## Verdict",
                "- The parent weak-field zero theorem was attempted directly.",
                "- `q_R=0` would follow if the parent theory supplied an owned auxiliary/first-class reciprocal constraint, or a kinetic route plus a real `Q_R=0` theorem.",
                "- `delta_beta=0` would follow if the parent weak-field variation supplied the second-order GR-like completion with source normalization and Bianchi/Ward conservation.",
                "- The current corpus has contracts and conditional EH/Noether/Ward machinery, but not an explicit signed MTS parent variation that proves both zeros.",
                "- Therefore the local GR branch is demoted, for now, to a bounded closure control lane; the 1559 runner remains useful but nonclaim.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Weak-Field Derivation Attempt",
                md_table(weak, ["attempt_id", "route", "equation_or_condition", "consequence", "status", "limitation"]),
                "",
                "## q_R Zero Route Audit",
                md_table(qr, ["route_id", "route", "test_equation", "result", "status", "missing_or_forbidden"]),
                "",
                "## Beta Zero Route Audit",
                md_table(beta, ["route_id", "route", "test_equation", "result", "status", "missing_or_forbidden"]),
                "",
                "## Conditional Zero Theorem Contract",
                md_table(contract, ["contract_id", "premise", "required_statement", "why_needed", "status"]),
                "",
                "## Bounded Closure Demotion",
                md_table(demotion, ["demotion_id", "object", "new_status", "reason", "allowed_use"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    weak = weak_attempt_rows()
    qr = qR_route_rows()
    beta = beta_route_rows()
    contract = conditional_contract_rows()
    demotion = demotion_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(WEAK_ATTEMPT, weak)
    write_csv(QR_AUDIT, qr)
    write_csv(BETA_AUDIT, beta)
    write_csv(CONDITIONAL_CONTRACT, contract)
    write_csv(CLOSURE_DEMOTION, demotion)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        WEAK_ATTEMPT,
        QR_AUDIT,
        BETA_AUDIT,
        CONDITIONAL_CONTRACT,
        CLOSURE_DEMOTION,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, weak, qr, beta, contract, demotion, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
