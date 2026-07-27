from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2748-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2748_SOURCE_REGISTER.csv",
    "attempt": RESIDUALS / "P8_Y5_R2FR_2748_WEAK_FIELD_DERIVATION_ATTEMPT.csv",
    "qr_routes": RESIDUALS / "P8_Y5_R2FR_2748_QR_ZERO_ROUTE_AUDIT.csv",
    "beta_routes": RESIDUALS / "P8_Y5_R2FR_2748_BETA_ZERO_ROUTE_AUDIT.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2748_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2748_BOUNDED_CLOSURE_DEMOTION.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2748_RUNNER_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2748_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2748_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2748_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2748_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2748_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract": SOURCE_WEIGHT / "weak_field_zero_contract_2748_NONCLAIM.csv",
    "demotion": LOCAL_BOUNDS / "bounded_closure_demotion_2748_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2748_MINIMAL_PARENT_WEAK_FIELD_ACTION_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2748_0_2747_doc",
            "description": "2747 selects parent weak-field zero-condition derivation or demotion.",
            "source_path": "2747-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt-under-AX1090.md",
            "required_needles": "NEXT2747_0_2748;ZERO2747_0_qR_linear;VAL2747_OVERALL",
        },
        {
            "source_id": "SRC2748_1_2747_validation",
            "description": "2747 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2747_VALIDATION.csv",
            "required_needles": "VAL2747_OVERALL;True;zero-condition derivation next",
        },
        {
            "source_id": "SRC2748_2_2747_zero",
            "description": "live parent zero-condition hunt ledger.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2747_PARENT_ZERO_CONDITION_HUNT.csv",
            "required_needles": "ZERO2747_0_qR_linear;MISSING_SECOND_ORDER_PARENT_COMPLETION;MISSING_MODE_DECOUPLING_THEOREM",
        },
        {
            "source_id": "SRC2748_3_2747_model",
            "description": "live q_R/delta_beta two-parameter model.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2747_TWO_PARAMETER_MODEL.csv",
            "required_needles": "MODEL2747_0_gamma;MODEL2747_6_mercury_combo",
        },
        {
            "source_id": "SRC2748_4_1560_doc",
            "description": "prior parent weak-field zero derivation/demotion checkpoint.",
            "source_path": "1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md",
            "required_needles": "WF1560_6_verdict;COND1560_7_consequence;NEXT_1561_MINIMAL_PARENT_WEAK_FIELD_ACTION_ANSATZ",
        },
        {
            "source_id": "SRC2748_5_observer_contract",
            "description": "observer-map symplectic contract.",
            "source_path": "10-observer-map-symplectic-contract.md",
            "required_needles": "A future parent action may pass only if it produces;R_AB = ln(T^2 S) = 0",
        },
        {
            "source_id": "SRC2748_6_local_closure",
            "description": "local closure benchmark status.",
            "source_path": "13-local-closure-PPN-benchmark.md",
            "required_needles": "valid local GR control baseline;not a parent derivation",
        },
        {
            "source_id": "SRC2748_7_vacuum_reciprocity",
            "description": "vacuum reciprocity action contract.",
            "source_path": "04-vacuum-reciprocity-action-contract.md",
            "required_needles": "vacuum_reciprocity_action_contract_locked_not_satisfied;d/dr [ W(r,L,fields) dR_AB/dr ] = J_R",
        },
        {
            "source_id": "SRC2748_8_reciprocity_attempt",
            "description": "reciprocity theorem attempt and Q_R obstruction.",
            "source_path": "05-reciprocity-theorem-attempt.md",
            "required_needles": "W R_AB' = Q_R.;The missing theorem is source matching",
        },
        {
            "source_id": "SRC2748_9_constraint_doc",
            "description": "nonpropagating reciprocity constraint source.",
            "source_path": "07-nonpropagating-reciprocity-constraint.md",
            "required_needles": "S_constraint = integral lambda_R R_AB.;why does the parent motion-load action contain lambda_R",
        },
        {
            "source_id": "SRC2748_10_parent_skeleton",
            "description": "constrained parent action skeleton.",
            "source_path": "19-constrained-parent-action-skeleton.md",
            "required_needles": "closure_term.;beta=1, still open",
        },
        {
            "source_id": "SRC2748_11_euler_ward",
            "description": "minimal parent action Euler/Ward test.",
            "source_path": "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
            "required_needles": "conditional_Euler_Ward_chain_only_no_PiM;DAT537_4",
        },
        {
            "source_id": "SRC2748_12_current_chain",
            "description": "parent theta/current-chain extraction attempt.",
            "source_path": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "required_needles": "parent `theta_MTS` and `Q_tau^MTS` extraction attempted;missing_explicit_current_chain",
        },
        {
            "source_id": "SRC2748_13_2747_queue",
            "description": "live queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2747_PARENT_WEAK_FIELD_ZERO_CONDITION_NEXT.csv",
            "required_needles": "NEXT2747_0_2748;parent weak-field field-equation/action structure",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def attempt_rows() -> list[dict[str, Any]]:
    specs = [
        ("WF2748_0_translation", "weak-field dictionary", "R_AB ~= q_R L and q_R = gamma-1", "first-order local PPN translation already derived", "DERIVED_TRANSLATION_ONLY", "does not prove q_R=0; it only shows what must vanish"),
        ("WF2748_1_qR_target", "first-order zero condition", "parent equations must force R_AB=O(L^2)", "then q_R=0 and gamma=1 at first PPN order", "TARGET_THEOREM_NOT_SIGNED", "requires field equation, boundary condition, zero charge, and matter readout"),
        ("WF2748_2_kinetic_route", "reciprocal-strain kinetic variation", "d/dr(W R_AB')=J_R gives W R_AB'=Q_R in vacuum", "allows reciprocal hair unless Q_R=0 is separately proven", "REJECTED_AS_CURRENT_ZERO_PROOF", "kinetic route converts the problem into a zero-charge theorem"),
        ("WF2748_3_constraint_route", "auxiliary multiplier constraint", "delta lambda_R -> R_AB=0", "would prove q_R=0 if lambda_R R_AB is parent-owned and not an inserted closure", "CONDITIONAL_UNSIGNED", "current skeleton labels this a closure term"),
        ("WF2748_4_EH_Ward_route", "EH plus silent exterior route", "covariant variation and Noether/Ward chain can conditionally recover GR-like weak field", "conditional chain fails current source/PiM/current-chain ownership", "CONDITIONAL_NOT_MTS_PARENT_DERIVATION", "EH reference cannot be used as the whole MTS parent action"),
        ("WF2748_5_beta_target", "second-order beta zero condition", "parent equations must fix beta-1=delta_beta=0 at O(U^2)", "requires nonlinear self-coupling, source normalization, Bianchi/Ward identity, and gauge/readout map", "MISSING_SECOND_ORDER_PARENT_COMPLETION", "closure benchmark uses beta=1 but does not derive it"),
        ("WF2748_6_verdict", "current derivation status", "no current parent weak-field action derives both q_R=0 and delta_beta=0", "local branch remains useful as a bounded closure control lane", "DERIVATION_FAILED_DEMOTE_TO_BOUNDED_CLOSURE", "next route must build/test a minimal parent weak-field action ansatz"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "attempt_id": aid,
                "route": route,
                "equation_or_condition": equation,
                "consequence": consequence,
                "status": status,
                "limitation": limitation,
                "source_paths": "source-intake/mts_residuals/P8_Y5_R2FR_2747_PARENT_ZERO_CONDITION_HUNT.csv; 04-vacuum-reciprocity-action-contract.md; 05-reciprocity-theorem-attempt.md; 07-nonpropagating-reciprocity-constraint.md; 19-constrained-parent-action-skeleton.md; 538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md; 1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            }
        )
        for aid, route, equation, consequence, status, limitation in specs
    ]


def qr_route_rows() -> list[dict[str, Any]]:
    specs = [
        ("QR2748_0_kinetic", "kinetic reciprocal-strain equation", "d/dr(W R_AB')=0", "R_AB can carry Q_R hair", "FAILS_CURRENT_ZERO_PROOF", "needs independent Q_R=0 theorem"),
        ("QR2748_1_boundary", "asymptotic/local boundary condition", "R_AB(infinity)=0 plus regularity", "kills integration constant but not necessarily Q_R source/boundary hair", "INSUFFICIENT", "must prove no source boundary charge"),
        ("QR2748_2_multiplier", "lambda_R auxiliary constraint", "delta lambda_R -> R_AB=0", "would close q_R=0 exactly", "CONDITIONAL_UNSIGNED", "lambda_R term is currently closure_term, not parent-derived"),
        ("QR2748_3_first_class", "first-class constraint/no-charge generator", "C_R=R_AB with zero/proper boundary charge", "would make reciprocal strain gauge/constrained rather than propagating", "POSSIBLE_NOT_PRESENT", "generator, bracket closure, degree count, and boundary charge not supplied"),
        ("QR2748_4_EH_import", "Einstein exterior equations", "AB=1 in Schwarzschild/vacuum GR", "would give q_R=0 by importing GR", "FORBIDDEN_AS_MTS_DERIVATION", "not allowed to smuggle in the target theorem"),
        ("QR2748_5_current", "accepted current route", "none", "q_R=0 is not parent-derived at 2748", "NO_ACCEPTED_PARENT_ZERO_ROUTE", "bounded closure lane retained"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "route_id": rid, "route": route, "test_equation": eq, "result": result, "status": status, "missing_or_forbidden": missing}) for rid, route, eq, result, status, missing in specs]


def beta_route_rows() -> list[dict[str, Any]]:
    specs = [
        ("BETA2748_0_closure_completion", "exact Schwarzschild-equivalent completion", "beta=1 in the closure control lane", "works as benchmark, not parent derivation", "CLOSURE_ONLY", "requires parent origin for the second-order metric/coframe terms"),
        ("BETA2748_1_EH_plus_silent", "minimal EH plus silent-sector parent", "standard nonlinear GR self-coupling gives beta=1", "conditional if the observed metric/source charge is parent-owned", "CONDITIONAL_NOT_CURRENT_MTS", "Pi_M/source-charge/current-chain ownership remains open"),
        ("BETA2748_2_second_order_action", "MTS second-order weak-field action", "delta_e S_parent fixes O(U^2) coefficient", "not available as an explicit MTS variation", "MISSING_PARENT_VARIATION", "write and vary the actual local parent Lagrangian"),
        ("BETA2748_3_Bianchi_Ward", "Bianchi/Ward identity", "conservation fixes nonlinear source and gauge consistency", "identity contract exists, but sector-by-sector parent action is not extracted", "MISSING_PARENT_IDENTITY", "derive dJ or nabla E identity with all retained sectors"),
        ("BETA2748_4_extra_modes", "extra local modes", "silent/decoupled sectors leave beta unchanged", "no general silence theorem for all retained local residuals", "MISSING_MODE_DECOUPLING", "prove no scalar/tracefree/fifth-force local hair or keep residual bounds"),
        ("BETA2748_5_current", "accepted current route", "none", "delta_beta=0 is not parent-derived at 2748", "NO_ACCEPTED_PARENT_BETA_ROUTE", "bounded closure lane retained"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "route_id": rid, "route": route, "test_equation": eq, "result": result, "status": status, "missing_or_forbidden": missing}) for rid, route, eq, result, status, missing in specs]


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("COND2748_0_L_parent", "explicit parent weak-field action", "L_parent with fields, variations, retained sectors, and boundary terms", "without this, no Euler equation is owned", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND2748_1_R_constraint", "reciprocal zero mechanism", "R_AB auxiliary/first-class constraint or kinetic route plus proven Q_R=0", "needed to force R_AB=O(L^2)", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND2748_2_source", "Newton/source normalization", "T^2=1-2U/c^2 and measured GM are derived from the same parent charge", "otherwise beta/gamma can be calibrated after the fact", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND2748_3_matter", "universal matter/coframe descent", "matter, clocks, and photons read the same observed coframe", "otherwise local bounds do not test one geometry", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND2748_4_second_order", "second-order weak-field completion", "O(U^2) metric/coframe equation yields beta=1", "needed for delta_beta=0", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND2748_5_identity", "Bianchi/Ward identity", "parent equations imply the conservation identity tying source and field equations", "prevents inconsistent source normalization and beta drift", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND2748_6_silence", "no extra local hair", "scalar/vector/tracefree/fifth-force sectors vanish, decouple, or are explicitly bounded", "needed before local GR is exact rather than residual-bounded", "UNSIGNED_REQUIRED_PREMISE"),
        ("COND2748_7_consequence", "conditional theorem consequence", "if COND2748_0 through COND2748_6 hold, then q_R=0 and delta_beta=0 in the local branch", "conditional theorem shape is clear", "CONDITIONAL_THEOREM_UNSIGNED"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "contract_id": cid, "premise": premise, "required_statement": statement, "why_needed": why, "status": status}) for cid, premise, statement, why, status in specs]


def demotion_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEM2748_0_local_GR_branch", "local GR/Newton branch", "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED", "q_R=0 and delta_beta=0 are not parent-signed", "use 2747 runner as control harness; do not claim derived GR"),
        ("DEM2748_1_qR", "q_R local spatial reciprocal hair", "BOUNDED_PARAMETER", "Cassini/gamma clamps any nonzero q_R through q_R=gamma-1", "retain q_R bound box unless zero theorem closes"),
        ("DEM2748_2_delta_beta", "delta_beta nonlinear drift", "BOUNDED_PARAMETER", "beta/ephemeris row clamps beta drift; Mercury has q_R degeneracy", "retain two-parameter PPN control runner"),
        ("DEM2748_3_parent_program", "parent field theory route", "ACTIVE_DERIVATION_TARGET", "conditional theorem shows exactly what the parent action must provide", "next build minimal ansatz and run Euler/Ward/PPN gates"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "demotion_id": did, "object": obj, "new_status": status, "reason": reason, "allowed_use": use}) for did, obj, status, reason, use in specs]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2748_0_sources", "all derivation source contracts loaded", "PASS", "source register covers 2747, local closure, reciprocity action, constrained action skeleton, Euler/Ward, and parent current-chain audit"),
        ("RUN2748_1_qR_derivation", "derive q_R=0", "FAILED_CURRENT_PARENT_DERIVATION", "kinetic route leaves Q_R hair; multiplier route is closure unless parent-owned; first-class route is absent"),
        ("RUN2748_2_beta_derivation", "derive delta_beta=0", "FAILED_CURRENT_PARENT_DERIVATION", "second-order MTS parent variation and Bianchi/source identity are not supplied"),
        ("RUN2748_3_conditional_theorem", "conditional zero theorem shape", "PASS_CONDITIONAL_UNSIGNED", "the theorem can be stated if explicit parent action, reciprocal zero mechanism, source normalization, matter descent, beta completion, Ward identity, and no-extra-mode premises are supplied"),
        ("RUN2748_4_demotion", "local branch status", "DERIVATION_FAILED_DEMOTED_TO_BOUNDED_CLOSURE", "2747 control runner remains valid as a nonclaim local residual harness"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "runner_id": rid, "test": test, "current_status": status, "detail": detail}) for rid, test, status, detail in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2748_0_qR_zero", "q_R=0 parent theorem", "BLOCKED_NO_CLAIM", "no accepted current parent zero route"),
        ("GATE2748_1_beta_zero", "delta_beta=0 parent theorem", "BLOCKED_NO_CLAIM", "second-order parent completion missing"),
        ("GATE2748_2_constraint", "lambda_R constraint as derivation", "BLOCKED_NO_CLAIM", "lambda_R term currently functions as closure unless parent origin is supplied"),
        ("GATE2748_3_EH_reference", "EH route as MTS derivation", "BLOCKED_NO_CLAIM", "EH/Noether route is conditional/reference only without MTS current-chain ownership"),
        ("GATE2748_4_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "bounded closure control lane only"),
        ("GATE2748_5_empirical_score", "local PPN empirical success claim", "BLOCKED_NO_CLAIM", "control runner scores hypothetical leak vectors, not a parent-predicted vector"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2748_0_verdict", "parent weak-field zero theorem", "CURRENT_DERIVATION_FAILS_CONDITIONAL_THEOREM_WRITTEN", "the required theorem shape is clear, but the current corpus lacks the explicit parent action/variation and zero-charge/second-order completion needed to sign it"),
        ("DEC2748_1_branch_status", "local GR branch status", "DEMOTE_TO_BOUNDED_CLOSURE_CONTROL_LANE", "2747 PPN runner remains useful, but local GR/Newton is not parent-derived"),
        ("DEC2748_2_next", "next target", "NEXT_2749_MINIMAL_PARENT_WEAK_FIELD_ACTION_ANSATZ", "the most direct repair is to write a minimal parent weak-field ansatz and run Euler/Ward/PPN zero gates against it"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2748_0_2749",
                "status": "selected_primary",
                "target_doc": "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_minimal_parent_weak_field_action_ansatz_and_Euler_Ward_PPN_gate_under_AX1090_2749.py",
                "mission": "construct a minimal parent weak-field action ansatz with explicit R_AB auxiliary/constraint sector, source normalization, universal coframe matter coupling, and second-order beta terms; vary/gate it to see whether q_R=0 and delta_beta=0 can be parent-signed or must remain bounded closure",
                "acceptance": "write the ansatz, Euler/Ward/PPN gate rows, and either a signed zero theorem or precise rejection/demotion blockers",
                "forbidden": "do not promote a closure multiplier to derivation without parent-origin and zero-stress proof; do not claim local GR/Newton reduction; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2748_0_contract", "source_table": rel(OUTPUTS["contract"]), "copy_path": rel(BRANCH_OUTPUTS["contract"]), "purpose": "source-weight weak-field zero theorem contract", "exists": BRANCH_OUTPUTS["contract"].exists()}),
        nonclaim({"copy_id": "BR2748_1_demotion", "source_table": rel(OUTPUTS["demotion"]), "copy_path": rel(BRANCH_OUTPUTS["demotion"]), "purpose": "local-bound bounded closure demotion ledger", "exists": BRANCH_OUTPUTS["demotion"].exists()}),
        nonclaim({"copy_id": "BR2748_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for minimal parent weak-field action ansatz", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    attempt: list[dict[str, Any]],
    qr_routes: list[dict[str, Any]],
    beta_routes: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    attempt_ok = any(row["attempt_id"] == "WF2748_6_verdict" and row["status"] == "DERIVATION_FAILED_DEMOTE_TO_BOUNDED_CLOSURE" for row in attempt)
    qr_ok = any(row["route_id"] == "QR2748_5_current" and row["status"] == "NO_ACCEPTED_PARENT_ZERO_ROUTE" for row in qr_routes)
    beta_ok = any(row["route_id"] == "BETA2748_5_current" and row["status"] == "NO_ACCEPTED_PARENT_BETA_ROUTE" for row in beta_routes)
    contract_ok = len(contract) == 8 and any(row["contract_id"] == "COND2748_7_consequence" and row["status"] == "CONDITIONAL_THEOREM_UNSIGNED" for row in contract)
    demotion_ok = any(row["demotion_id"] == "DEM2748_0_local_GR_branch" and row["new_status"] == "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED" for row in demotion)
    runner_ok = any(row["runner_id"] == "RUN2748_4_demotion" and row["current_status"] == "DERIVATION_FAILED_DEMOTED_TO_BOUNDED_CLOSURE" for row in runner)
    gates_ok = len(gates) == 6 and all(row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [attempt, qr_routes, beta_routes, contract, demotion, runner, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2749" in next_target[0]["target_doc"] and "weak-field-action" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2748_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_1_weak_verdict", "passed": attempt_ok, "detail": "weak-field derivation verdict is explicit", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_2_qR_no_route", "passed": qr_ok, "detail": "q_R has no accepted parent zero route", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_3_beta_no_route", "passed": beta_ok, "detail": "delta_beta has no accepted parent route", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_4_contract_complete", "passed": contract_ok, "detail": "conditional zero theorem contract written", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_5_demotion", "passed": demotion_ok and runner_ok, "detail": "local GR branch demoted to bounded closure control", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_6_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "all claim gates remain blocked and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_7_next_target", "passed": next_ok, "detail": "next target is minimal parent weak-field action ansatz", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2748_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2748_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2748_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2748 attempts parent weak-field zero-condition derivation, demotes local GR to bounded closure, and selects minimal parent weak-field action ansatz next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2748 - Y5 R2/f(R): Parent Weak-Field Zero-Condition Derivation Or Demotion Under AX1090

Status: `Y5_R2FR_2748_parent_zero_derivation_failed_bounded_closure_control_lane`

## Private Verdict

2748 attacks the actual missing theorem.

To get derived local GR, the parent weak-field theory must force:

`R_AB=O(L^2)` so `q_R=0`,

and

`beta=1` so `delta_beta=0`.

Current result: not derived. The kinetic route leaves `Q_R` hair unless a zero-charge theorem exists. The multiplier route works only if `lambda_R R_AB` is parent-owned, not inserted as closure. The EH/Ward route is only conditional unless the MTS parent current/source chain owns the observed metric and source normalization. The second-order beta route is missing the explicit parent variation, Bianchi/Ward identity, and source normalization.

So the local GR branch is demoted to bounded closure control for now. That is not a dead end; it tells us exactly what the minimal parent weak-field action ansatz must supply next.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Weak-Field Derivation Attempt

{markdown_table(data["attempt"], ["attempt_id", "route", "equation_or_condition", "consequence", "status", "limitation", "valid_for_claim"])}

## q_R Zero Route Audit

{markdown_table(data["qr_routes"], ["route_id", "route", "test_equation", "result", "status", "missing_or_forbidden", "valid_for_claim"])}

## Beta Zero Route Audit

{markdown_table(data["beta_routes"], ["route_id", "route", "test_equation", "result", "status", "missing_or_forbidden", "valid_for_claim"])}

## Conditional Zero Theorem Contract

{markdown_table(data["contract"], ["contract_id", "premise", "required_statement", "why_needed", "status", "valid_for_claim"])}

## Bounded Closure Demotion

{markdown_table(data["demotion"], ["demotion_id", "object", "new_status", "reason", "allowed_use", "valid_for_claim"])}

## Runner

{markdown_table(data["runner"], ["runner_id", "test", "current_status", "detail", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the hard but useful answer: the local runner is now sharp, but the parent theorem is not signed. The next productive move is not more rhetoric around `R_AB=0`; it is a minimal parent weak-field action ansatz with explicit variation, source normalization, matter descent, and second-order beta gates.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    attempt = attempt_rows()
    qr_routes = qr_route_rows()
    beta_routes = beta_route_rows()
    contract = contract_rows()
    demotion = demotion_rows()
    runner = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["attempt"], attempt)
    write_csv(OUTPUTS["qr_routes"], qr_routes)
    write_csv(OUTPUTS["beta_routes"], beta_routes)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["demotion"], demotion)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["contract"], contract)
    write_csv(BRANCH_OUTPUTS["demotion"], demotion)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, attempt, qr_routes, beta_routes, contract, demotion, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "attempt": attempt,
        "qr_routes": qr_routes,
        "beta_routes": beta_routes,
        "contract": contract,
        "demotion": demotion,
        "runner": runner,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2748 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
