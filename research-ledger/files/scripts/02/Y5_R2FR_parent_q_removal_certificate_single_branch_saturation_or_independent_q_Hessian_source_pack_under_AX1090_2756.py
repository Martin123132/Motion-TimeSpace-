from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2756-Y5-R2FR-parent-q-removal-certificate-single-branch-saturation-or-independent-q-Hessian-source-pack-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_Q_REMOVAL_OR_Q_HESSIAN_2756"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2756_SOURCE_REGISTER.csv",
    "saturation": RESIDUALS / "P8_Y5_R2FR_2756_SINGLE_BRANCH_Q_REMOVAL_SATURATION.csv",
    "theta_hunt": RESIDUALS / "P8_Y5_R2FR_2756_THETAQ_OMEGAQ_SOURCE_HUNT_CROSSCHECK.csv",
    "fallback": RESIDUALS / "P8_Y5_R2FR_2756_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2756_BOUND_RUNNER_ACTIVATION_STATUS.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2756_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2756_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2756_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2756_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2756_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2756_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "saturation_beta": BETA_DOCS / "Q_REMOVAL_SINGLE_BRANCH_SATURATION_2756_NONCLAIM.csv",
    "fallback_local": LOCAL_BOUNDS / "q_independent_hessian_source_pack_2756_NONCLAIM.csv",
    "theta_source_weight": SOURCE_WEIGHT / "Q_THETAQ_OMEGAQ_NEGATIVE_SOURCE_HUNT_2756_NONCLAIM.csv",
    "next_queue": QUEUE / "JR2756_INDEPENDENT_Q_HESSIAN_OPERATOR_SOURCE_NEXT.csv",
}


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
            "source_id": "SRC2756_0_2755_doc",
            "description": "AX1090 q-operator branch decision handoff.",
            "source_path": "2755-Y5-R2FR-q-operator-identity-bridge-or-independent-Hessian-under-AX1090.md",
            "required_needles": "NEXT2755_0_2756;NP2755_5_activation_verdict;IQH2755_5_claim_gate;VAL2755_OVERALL",
        },
        {
            "source_id": "SRC2756_1_2755_validation",
            "description": "2755 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2755_VALIDATION.csv",
            "required_needles": "VAL2755_OVERALL;True",
        },
        {
            "source_id": "SRC2756_2_2311_doc",
            "description": "prior parent q-removal certificate audit.",
            "source_path": "2311-Y5-R2FR-parent-q-removal-certificate-degree-count-boundary-neutrality-or-independent-Hessian-source-pack.md",
            "required_needles": "QRC2311_8_verdict;CERTIFICATE_NOT_CLOSED_CURRENT;FB2311_7_claim_gate;VAL2311_OVERALL",
        },
        {
            "source_id": "SRC2756_3_2311_validation",
            "description": "2311 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2311_VALIDATION.csv",
            "required_needles": "VAL2311_OVERALL;PASS",
        },
        {
            "source_id": "SRC2756_4_2312_doc",
            "description": "prior q Omega/momentum-map source attempt.",
            "source_path": "2312-Y5-R2FR-parent-q-Omega-momentum-map-generator-or-independent-q-bound-pack.md",
            "required_needles": "GQ2312_5_verdict;GQ_NOT_ACTIVATED_CURRENT;SHIFT2312_4_verdict;VAL2312_OVERALL",
        },
        {
            "source_id": "SRC2756_5_2312_validation",
            "description": "2312 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2312_VALIDATION.csv",
            "required_needles": "VAL2312_OVERALL;PASS",
        },
        {
            "source_id": "SRC2756_6_2313_doc",
            "description": "prior Theta_q source hunt and independent bound-runner activation.",
            "source_path": "2313-Y5-R2FR-q-symplectic-potential-source-or-independent-q-bound-runner-activation.md",
            "required_needles": "THQ2313_5_verdict;SYMPLECTIC_SOURCE_NEGATIVE_ACTIVATE_BOUND_RUNNER_NONCLAIM;RUN2313_6_score_gate;VAL2313_OVERALL",
        },
        {
            "source_id": "SRC2756_7_2313_validation",
            "description": "2313 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2313_VALIDATION.csv",
            "required_needles": "VAL2313_OVERALL;PASS",
        },
        {
            "source_id": "SRC2756_8_2308_doc",
            "description": "minimal q action contract and unsourced q operator verdict.",
            "source_path": "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
            "required_needles": "QOP2308_4_verdict;Q_OPERATOR_UNSOURCED;NF2308_0_minimal_action",
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


def saturation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SAT2756_0_parent_quotient",
            "parent quotient object",
            "q or pi:Y->Y_red is defined before variation with units/domain",
            "NOT_PARENT_SIGNED",
            "1157/2311 keep parent q-map/null-generator unsigned",
        ),
        (
            "SAT2756_1_actual_vertical_generator",
            "actual local vertical generator",
            "v_q acts on geometry, matter, readouts, and boundary fields and lies in ker(Dpi)",
            "CONDITIONAL_ONLY",
            "637 gives a conditional kernel; 1023/1157 keep the actual local direction open",
        ),
        (
            "SAT2756_2_theta_omega_q",
            "Theta_q/Omega_q q block",
            "parent symplectic potential or presymplectic q block exists",
            "MISSING_PARENT_THETAQ_OMEGAQ",
            "2312/2313 find only template shape, not q-specific parent data",
        ),
        (
            "SAT2756_3_generator_constraint",
            "momentum map/constraint generator",
            "i_v Omega = delta G_q with differentiable G_q=int epsilon C_q+Q_q",
            "MISSING_CQ_QQ_GENERATOR",
            "C_q, Q_q, allowed epsilon domain, and differentiability are unsourced",
        ),
        (
            "SAT2756_4_bracket_degree",
            "first-class closure and degree count",
            "brackets close without anomaly and rank(G_q)=N_q removes the q canonical pair",
            "MISSING_BRACKET_AND_DEGREE_COUNT",
            "2311 degree theorem is exact conditional but not parent-signed",
        ),
        (
            "SAT2756_5_descent",
            "action/matter/readout descent",
            "S, S_matter, clocks/constants/readouts all factor through the same quotient branch",
            "MISSING_DESCENT_CERTIFICATE",
            "1023/2311 keep matter/readout descent conditional or missing",
        ),
        (
            "SAT2756_6_boundary_source_neutrality",
            "boundary and source neutrality",
            "Q_q[body], boundary/corner/readout/history/projector tails vanish or are bounded as proper gauge",
            "MISSING_BOUNDARY_SOURCE_NEUTRALITY",
            "2297/2311 show exterior vacuum silence is insufficient",
        ),
        (
            "SAT2756_7_single_branch_verdict",
            "single-branch q-removal certificate",
            "all clauses SAT2756_0 through SAT2756_6 close in the same parent branch",
            "CERTIFICATE_NOT_CLOSED_CURRENT",
            "no-pole theorem remains exact-conditional; fallback lane activates as nonclaim",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "saturation_id": row_id,
                "clause": clause,
                "requirement": requirement,
                "current_status": status,
                "evidence_summary": evidence,
                "single_branch_signed": False,
            }
        )
        for row_id, clause, requirement, status, evidence in specs
    ]


def theta_hunt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TH2756_0_Thetaq",
            "Theta_q or Omega_q q-block",
            "NOT_FOUND_AS_PARENT_SOURCE",
            "2312 gives template transfer and conditional q-shift formula; 2313 source hunt is negative",
            "no-pole momentum-map route cannot activate",
        ),
        (
            "TH2756_1_piq",
            "pi_q or conjugate q momentum",
            "NOT_FOUND_AS_PARENT_SOURCE",
            "canonical shift generator G_q=-int epsilon pi_q+Q_q is exact only if pi_q is sourced",
            "degree count and generator ownership remain unsigned",
        ),
        (
            "TH2756_2_constraint_action",
            "explicit q constraint/Lagrange multiplier action",
            "NOT_FOUND_AS_PARENT_SOURCE",
            "2308 writes a normal form contract but not a parent-derived constraint action",
            "Dirac first-class or auxiliary route remains unsigned",
        ),
        (
            "TH2756_3_current_policy",
            "new source requirement",
            "REQUIRE_NEW_PARENT_TEXT_BEFORE_NO_POLE_RETRY",
            "2311-2313 already exhausted the current inspected q-removal chain",
            "do not run more no-pole laps without Theta_q/Omega_q/C_q/Q_q evidence",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "hunt_id": row_id,
                "target": target,
                "hunt_result": result,
                "evidence": evidence,
                "route_effect": effect,
            }
        )
        for row_id, target, result, evidence, effect in specs
    ]


def fallback_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FB2756_0_trigger",
            "fallback branch predicate",
            "SAT2756_7 != CERTIFICATE_CLOSED and q-X bridge remains inactive",
            "TRIGGER_ACTIVE_NONCLAIM",
            "boolean",
            "2755;2311;2313",
        ),
        (
            "FB2756_1_Zq",
            "Z_q",
            "signed q kinetic Hessian/operator normalization",
            "MISSING_PARENT_HESSIAN",
            "action_density_normalization_dependent",
            "MISSING_PARENT_SOURCE",
        ),
        (
            "FB2756_2_Mq2_lambda",
            "M_q^2/lambda_q",
            "q mass/gap and range in same normalization as Z_q",
            "MISSING_PARENT_HESSIAN_OR_RANGE",
            "Z_q/length^2 and length",
            "MISSING_PARENT_SOURCE",
        ),
        (
            "FB2756_3_DqWeyl2",
            "D_qWeyl2",
            "coefficient of q C_abcd C^abcd or theorem-zero/no-tower proof",
            "MISSING_PARENT_COEFFICIENT",
            "q-action convention dependent",
            "MISSING_PARENT_SOURCE",
        ),
        (
            "FB2756_4_DqWeylDual",
            "D_qWeylDual",
            "parity-odd q C_abcd *C^abcd coefficient or zero theorem",
            "MISSING_PARENT_COEFFICIENT_OR_STATIC_ZERO_SCOPE",
            "q-action convention dependent",
            "MISSING_PARENT_SOURCE",
        ),
        (
            "FB2756_5_Jq_components",
            "J_q component vector",
            "matter/body/boundary/readout/history/projector/counterterm/constants source rows",
            "MISSING_COMPONENT_ZERO_OR_BOUNDS",
            "q Euler-source units",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_BOUND_TEMPLATE.csv",
        ),
        (
            "FB2756_6_body_boundary_tails",
            "Q_q[body], Q_q_boundary, Pi_q/tail envelope",
            "absolute zero theorem or source-backed bound without sign cancellation",
            "MISSING_ZERO_THEOREM_OR_BOUND",
            "source/boundary charge",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
        ),
        (
            "FB2756_7_Parena",
            "P_arena[q]",
            "R10/PPN/clock/orbital/local-GR projection from q into observables",
            "MISSING_ARENA_PROJECTION",
            "arena dependent",
            "MISSING_ARENA_SOURCE",
        ),
        (
            "FB2756_8_score_gate",
            "independent q score permission",
            "FB2756_1 through FB2756_7 all source-backed or theorem-zero",
            "CLAIM_AND_SCORE_BLOCKED",
            "boolean",
            "FB2756_1;FB2756_2;FB2756_3;FB2756_4;FB2756_5;FB2756_6;FB2756_7",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "fallback_id": row_id,
                "input": input_name,
                "required_value": required,
                "current_status": status,
                "units": units,
                "source_path": source,
            }
        )
        for row_id, input_name, required, status, units, source in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RUN2756_0_route",
            "working route",
            "INDEPENDENT_Q_BOUND_RUNNER_ACTIVE_AS_NONCLAIM_LANE",
            "no-pole certificate and q-X bridge are both inactive under current evidence",
        ),
        (
            "RUN2756_1_score",
            "numerical scoring",
            "BLOCKED",
            "Z_q, M_q^2/lambda_q, D coefficients, source vector, boundary tails, and P_arena are missing",
        ),
        (
            "RUN2756_2_kernel",
            "Schwarzschild Weyl2 kernel",
            "BACKGROUND_KERNEL_READY_NONCLAIM",
            "C^2 shape can be used after q operator/coefficient/source conventions are owned",
        ),
        (
            "RUN2756_3_policy",
            "no-cancellation policy",
            "ABSOLUTE_ENVELOPE_REQUIRED",
            "unknown source channels cannot cancel each other in a claim-grade bound",
        ),
        (
            "RUN2756_4_local_GR",
            "derived local GR/Newton",
            "BLOCKED_NO_CLAIM",
            "q branch has not been deleted by proof and cannot yet be bounded numerically",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "runner_id": row_id,
                "target": target,
                "current_status": status,
                "reason": reason,
            }
        )
        for row_id, target, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2756_0_no_pole",
            "single-branch q-removal certificate",
            "NOT_CLOSED_CURRENT",
            "exact theorem exists, but parent quotient/vertical/Omega/generator/degree/descent/boundary package is unsigned",
        ),
        (
            "DEC2756_1_new_source_rule",
            "future no-pole retry condition",
            "REQUIRE_THETAQ_OMEGAQ_OR_EXPLICIT_Q_CONSTRAINT",
            "2311-2313 already tested the current no-pole trail; more laps need genuinely new parent source text",
        ),
        (
            "DEC2756_2_fallback",
            "independent-q bound runner",
            "ACTIVATE_AS_NONCLAIM_WORKFLOW_LANE",
            "retained q residuals must now be source-bounded rather than rhetorically suppressed",
        ),
        (
            "DEC2756_3_first_fill",
            "first fallback input",
            "Z_Q_MQ2_LAMBDAQ_OPERATOR_SOURCE_FIRST",
            "operator ownership is the denominator for every q response or local empirical score",
        ),
        (
            "DEC2756_4_next",
            "next target",
            "NEXT_2757_INDEPENDENT_Q_HESSIAN_OPERATOR_SOURCE_OR_BOUND_RUNNER_FIRST_FILL",
            "try to source Z_q/M_q^2/lambda_q/q units/domain; if absent, write the explicit blocker rather than scoring",
        ),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "decision_id": row_id, "decision": decision, "result": result, "reason": reason}) for row_id, decision, result, reason in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2756_0_sources", "all source paths/needles valid", "PASS_NONCLAIM", "checkpoint is reproducible"),
        ("GATE2756_1_no_pole", "single-branch no-pole activation", "BLOCKED_NO_CLAIM", "Theta_q/Omega_q/G_q/degree/descent/boundary missing"),
        ("GATE2756_2_bound_lane", "independent q bound lane active", "PASS_NONCLAIM", "workflow lane active, not score-ready"),
        ("GATE2756_3_score", "independent q numerical score", "BLOCKED_NO_CLAIM", "operator/coefficient/source/projection inputs missing"),
        ("GATE2756_4_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "q not deleted or bounded"),
        ("GATE2756_5_public", "public/GitHub update", "BLOCKED_NO_CLAIM", "private derivability checkpoint only"),
    ]
    return [nonclaim({"claim_gate_id": row_id, "claim_gate": gate, "status": status, "reason": reason}) for row_id, gate, status, reason in specs]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2756_0_delete_q", "delete q/DqWeyl2 rows as no-pole", "BLOCKED", "single-branch certificate is not closed"),
        ("REF2756_1_retry_no_pole_lap", "rerun no-pole route without new parent source", "BLOCKED", "Theta_q/Omega_q or explicit q constraint action is required first"),
        ("REF2756_2_score_bound_runner", "score independent q bound runner now", "BLOCKED", "operator/coefficient/source/projection rows are missing"),
        ("REF2756_3_claim_local_GR", "claim derived local GR/Newton", "BLOCKED", "q residual route is active but not resolved"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row_id,
                "attempted_claim": claim,
                "status": status,
                "reason": reason,
                "runner_allows_claim": False,
            }
        )
        for row_id, claim, status, reason in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2756_0_2757",
                "status": "selected_primary",
                "target_doc": "2757-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_independent_q_Hessian_operator_source_or_bound_runner_first_fill_under_AX1090_2757.py",
                "mission": "source or reject the q operator first: Z_q, M_q^2/lambda_q, q units, q boundary/domain, and no-pole/auxiliary alternatives; do not score curvature/source projections until the operator denominator is owned",
                "acceptance": "either parent-sourced q Hessian/operator rows or an explicit blocker ledger showing the independent-q bound runner cannot score; all rows remain nonclaim unless sourced",
                "forbidden": "do not claim local GR/Newton, do not borrow X operator values, do not score D_qWeyl2, do not edit formalization-workbench, no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2756_0_saturation_beta", "source_table": rel(OUTPUTS["saturation"]), "copy_path": rel(BRANCH_OUTPUTS["saturation_beta"]), "purpose": "single-branch q-removal saturation handoff", "exists": BRANCH_OUTPUTS["saturation_beta"].exists()}),
        nonclaim({"copy_id": "BR2756_1_fallback_local", "source_table": rel(OUTPUTS["fallback"]), "copy_path": rel(BRANCH_OUTPUTS["fallback_local"]), "purpose": "local-bound independent q Hessian source pack", "exists": BRANCH_OUTPUTS["fallback_local"].exists()}),
        nonclaim({"copy_id": "BR2756_2_theta_source_weight", "source_table": rel(OUTPUTS["theta_hunt"]), "copy_path": rel(BRANCH_OUTPUTS["theta_source_weight"]), "purpose": "Theta_q/Omega_q negative source-hunt handoff", "exists": BRANCH_OUTPUTS["theta_source_weight"].exists()}),
        nonclaim({"copy_id": "BR2756_3_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB queue for independent-q operator source", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    saturation: list[dict[str, Any]],
    theta_hunt: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    saturation_ok = any(row["saturation_id"] == "SAT2756_7_single_branch_verdict" and row["current_status"] == "CERTIFICATE_NOT_CLOSED_CURRENT" for row in saturation)
    theta_ok = any(row["hunt_id"] == "TH2756_3_current_policy" and row["hunt_result"] == "REQUIRE_NEW_PARENT_TEXT_BEFORE_NO_POLE_RETRY" for row in theta_hunt)
    fallback_ok = {"Z_q", "M_q^2/lambda_q", "D_qWeyl2", "J_q component vector", "Q_q[body], Q_q_boundary, Pi_q/tail envelope", "P_arena[q]"}.issubset({row["input"] for row in fallback})
    runner_ok = any(row["runner_id"] == "RUN2756_0_route" and row["current_status"] == "INDEPENDENT_Q_BOUND_RUNNER_ACTIVE_AS_NONCLAIM_LANE" for row in runner) and any(row["runner_id"] == "RUN2756_1_score" and row["current_status"] == "BLOCKED" for row in runner)
    decision_ok = any(row["decision_id"] == "DEC2756_4_next" and row["result"] == "NEXT_2757_INDEPENDENT_Q_HESSIAN_OPERATOR_SOURCE_OR_BOUND_RUNNER_FIRST_FILL" for row in decisions)
    gates_ok = any(row["claim_gate_id"] == "GATE2756_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    refusal_ok = all(row["runner_allows_claim"] is False for row in refusal)
    next_ok = next_target[0]["selected"] is True and "2757" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [saturation, theta_hunt, fallback, runner, decisions, gates, refusal, next_target]
        for row in block
    )
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
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
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    rows = [
        {"validation_id": "VAL2756_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_1_saturation_failed_honestly", "passed": saturation_ok, "detail": "single-branch q-removal certificate remains unsigned", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_2_theta_policy", "passed": theta_ok, "detail": "future no-pole retry requires new Theta_q/Omega_q or q constraint source", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_3_fallback_pack", "passed": fallback_ok, "detail": "independent q Hessian/source/projection fallback pack is complete and nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_4_runner_lane", "passed": runner_ok, "detail": "independent-q bound runner lane active but score blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_5_next", "passed": decision_ok and next_ok, "detail": "2757 q Hessian/operator source first-fill selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_6_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "local GR/Newton and all claim gates remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_7_refusal_runner", "passed": refusal_ok, "detail": "refusal runner blocks delete/retry/score/local-GR claims", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2756_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2756_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2756_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2756 rejects current activation of the single-branch q-removal certificate, requires new Theta_q/Omega_q or q constraint evidence before no-pole retries, activates the independent-q bound-runner lane as nonclaim, and selects q Hessian/operator source first-fill.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2756 - Y5 R2/f(R): Parent q-Removal Certificate Single-Branch Saturation Or Independent q Hessian Source Pack Under AX1090

Status: `Y5_R2FR_2756_q_removal_not_closed_bound_runner_lane_active_nonclaim`

## Private Verdict

2756 is the no more mist checkpoint.

The q no-pole route is mathematically real: if the parent theory owns a quotient, a first-class generator, a correct degree count, descent of action/matter/readouts, and boundary/source neutrality in one branch, then the physical reduced Green operator has no q column and no local q pole.

Current MTS evidence does not sign that single branch. The exact missing first object is now sharper than before: `Theta_q/Omega_q`, `pi_q`, or an explicit q constraint action. Without one of those, the q-removal route is paused rather than rerun.

So the active private lane becomes the independent-q bound runner, still nonclaim. It cannot score yet: `Z_q`, `M_q^2/lambda_q`, `D_qWeyl2`, source tails, body/boundary charges, and `P_arena[q]` are missing. But from here the next useful move is not another proof lap. It is operator ownership first.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Single-Branch q-Removal Saturation

{markdown_table(data["saturation"], ["saturation_id", "clause", "requirement", "current_status", "evidence_summary", "single_branch_signed", "valid_for_claim"])}

## Thetaq/Omegaq Source-Hunt Crosscheck

{markdown_table(data["theta_hunt"], ["hunt_id", "target", "hunt_result", "evidence", "route_effect", "valid_for_claim"])}

## Independent q Hessian Source Pack

{markdown_table(data["fallback"], ["fallback_id", "input", "required_value", "current_status", "units", "source_path", "valid_for_claim"])}

## Bound Runner Activation Status

{markdown_table(data["runner"], ["runner_id", "target", "current_status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Refusal Runner

{markdown_table(data["refusal"], ["refusal_id", "attempted_claim", "status", "reason", "runner_allows_claim", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the leap forward we needed, even though it is not the glamorous answer. The no-pole theorem is no longer vague; it has a precise missing key. Unless a real `Theta_q/Omega_q` or q-constraint action appears, we stop trying to delete q by elegance and start bounding q honestly. First denominator: `Z_q`, `M_q^2`, range, units, and boundary/domain.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    saturation = saturation_rows()
    theta_hunt = theta_hunt_rows()
    fallback = fallback_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    refusal = refusal_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["saturation"], saturation)
    write_csv(OUTPUTS["theta_hunt"], theta_hunt)
    write_csv(OUTPUTS["fallback"], fallback)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["saturation_beta"], saturation)
    write_csv(BRANCH_OUTPUTS["fallback_local"], fallback)
    write_csv(BRANCH_OUTPUTS["theta_source_weight"], theta_hunt)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, saturation, theta_hunt, fallback, runner, decisions, gates, refusal, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "saturation": saturation,
        "theta_hunt": theta_hunt,
        "fallback": fallback,
        "runner": runner,
        "decisions": decisions,
        "gates": gates,
        "refusal": refusal,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2756 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
