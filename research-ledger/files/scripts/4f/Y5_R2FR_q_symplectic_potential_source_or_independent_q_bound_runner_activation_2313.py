from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_Q_SYMPLECTIC_SOURCE_OR_BOUND_RUNNER_2313"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2313-Y5-R2FR-q-symplectic-potential-source-or-independent-q-bound-runner-activation.md"

PATHS = {
    "2312_doc": ROOT / "2312-Y5-R2FR-parent-q-Omega-momentum-map-generator-or-independent-q-bound-pack.md",
    "2312_validation": OUT / "P8_Y5_BRR545_2312_VALIDATION.csv",
    "2312_closure": OUT / "P8_Y5_PARENT_QLOC_2312_MOMENTUM_MAP_CLOSURE_GATES.csv",
    "2312_candidates": OUT / "P8_Y5_PARENT_QLOC_2312_Q_MOMENTUM_MAP_CANDIDATES.csv",
    "2312_bound": OUT / "P8_Y5_PARENT_QLOC_2312_INDEPENDENT_Q_BOUND_PACK_UPDATE.csv",
    "1008_doc": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
    "2308_normal": OUT / "P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv",
    "2308_dcoef": OUT / "P8_Y5_PARENT_QLOC_2308_DQWEYL2_PARENT_COEFFICIENT_AUDIT.csv",
    "2307_hunt": OUT / "P8_Y5_PARENT_QLOC_2307_PARENT_COEFFICIENT_SOURCE_HUNT.csv",
    "2306_weyl": OUT / "P8_Y5_PARENT_QLOC_2306_SCHWARZSCHILD_WEYL2_PROJECTION_LAW.csv",
    "2297_bounds": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_BOUND_TEMPLATE.csv",
    "2297_body": OUT / "P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
    "2311_fallback": OUT / "P8_Y5_PARENT_QLOC_2311_INDEPENDENT_HESSIAN_FALLBACK_PACK.csv",
}

SOURCES = [
    ("SRC2313_00_2312_doc", "2312_doc", PATHS["2312_doc"], ["DEC2312_4_next", "CLOSE2312_6_verdict"], "direct 2312 handoff"),
    ("SRC2313_01_2312_validation", "2312_validation", PATHS["2312_validation"], ["VAL2312_OVERALL", "PASS"], "2312 validation"),
    ("SRC2313_02_2312_closure", "2312_closure", PATHS["2312_closure"], ["CLOSE2312_0_Omega", "MISSING_PARENT_OMEGA_Q_BLOCK"], "q momentum-map closure gates"),
    ("SRC2313_03_2312_candidates", "2312_candidates", PATHS["2312_candidates"], ["GQ2312_5_verdict", "GQ_NOT_ACTIVATED_CURRENT"], "q generator candidates"),
    ("SRC2313_04_2312_bound", "2312_bound", PATHS["2312_bound"], ["BND2312_5_claim_gate", "CLAIM_BLOCKED"], "incoming independent-q bound pack"),
    ("SRC2313_05_1008_doc", "1008_doc", PATHS["1008_doc"], ["PVA1008_1_theta_MTS", "template_available_not_extracted"], "general parent theta extraction negative evidence"),
    ("SRC2313_06_2308_normal", "2308_normal", PATHS["2308_normal"], ["NF2308_0_minimal_action", "CONTRACT_WRITTEN_NOT_DERIVED"], "minimal q action contract"),
    ("SRC2313_07_2308_dcoef", "2308_dcoef", PATHS["2308_dcoef"], ["DCO2308_3_verdict", "COEFFICIENT_UNSOURCED"], "D_qWeyl2 coefficient audit"),
    ("SRC2313_08_2307_hunt", "2307_hunt", PATHS["2307_hunt"], ["HUNT2307_3_verdict", "BLOCKED"], "projection runner source hunt"),
    ("SRC2313_09_2306_weyl", "2306_weyl", PATHS["2306_weyl"], ["PROJ2306_0_schwarzschild_identity", "EXACT_BACKGROUND_IDENTITY"], "Weyl2 background kernel"),
    ("SRC2313_10_2297_bounds", "2297_bounds", PATHS["2297_bounds"], ["JBT2297_10_total_abs", "SCHEMA_READY_VALUES_MISSING"], "J_q absolute source envelope"),
    ("SRC2313_11_2297_body", "2297_body", PATHS["2297_body"], ["BCL2297_1_body_charge", "Q_q[body]"], "body/worldtube q charge source law"),
    ("SRC2313_12_2311_fallback", "2311_fallback", PATHS["2311_fallback"], ["FB2311_7_claim_gate", "CLAIM_BLOCKED"], "earlier independent Hessian fallback pack"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2313_SOURCE_REGISTER.csv",
    "source_hunt": OUT / "P8_Y5_PARENT_QLOC_2313_THETAQ_SOURCE_HUNT.csv",
    "route": OUT / "P8_Y5_PARENT_QLOC_2313_ROUTE_DECISION.csv",
    "runner": OUT / "P8_Y5_PARENT_QLOC_2313_INDEPENDENT_Q_BOUND_RUNNER_ACTIVATION.csv",
    "priority": OUT / "P8_Y5_PARENT_QLOC_2313_INPUT_PRIORITY_LEDGER.csv",
    "contract": OUT / "P8_Y5_PARENT_QLOC_2313_BOUND_RUNNER_CONTRACT.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2313_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2313_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2313_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2313_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2313_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2313_0_source_hunt", OUTPUTS["source_hunt"], BETA_DOCS / "Q_THETAQ_SOURCE_HUNT_2313_NONCLAIM.csv"),
    ("COPY2313_1_runner", OUTPUTS["runner"], MICRO_RESIDUALS / "q_bound_runner_activation_nonclaim_2313.csv"),
    ("COPY2313_2_priority", OUTPUTS["priority"], RAB_QUEUE / "JR2313_Q_BOUND_RUNNER_INPUT_PRIORITY_NONCLAIM.csv"),
    ("COPY2313_3_contract", OUTPUTS["contract"], BETA_DOCS / "Q_BOUND_RUNNER_CONTRACT_2313_NONCLAIM.csv"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_source_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "THQ2313_0_Thetaq",
            "target": "Theta_q or Omega_q parent q block",
            "hunt_result": "NOT_FOUND_AS_PARENT_SOURCE",
            "evidence": "2312 names Theta_q/Omega_q only as the missing object; 1008 keeps theta_MTS template_available_not_extracted",
            "route_effect": "no-pole momentum-map route paused",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THQ2313_1_piq",
            "target": "pi_q canonical momentum",
            "hunt_result": "NOT_FOUND_AS_PARENT_SOURCE",
            "evidence": "canonical shift generator formula is conditional only; no parent action variation supplies pi_q",
            "route_effect": "cannot promote G_q[epsilon]=-int epsilon pi_q+Q_q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THQ2313_2_constraint_action",
            "target": "explicit q constraint or Lagrange multiplier action",
            "hunt_result": "NOT_FOUND_AS_PARENT_SOURCE",
            "evidence": "2308 writes a minimal q action contract but marks it CONTRACT_WRITTEN_NOT_DERIVED",
            "route_effect": "Dirac/auxiliary q route remains unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THQ2313_3_operator_coefficients",
            "target": "Z_q, M_q^2, lambda_q, D_qWeyl2",
            "hunt_result": "PARTIAL_SYMBOLIC_CONTRACT_ONLY",
            "evidence": "2308 gives the formal q action and range formula; D_qWeyl2 remains coefficient-unsourced",
            "route_effect": "bound-runner can be activated as schema but not scored",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THQ2313_4_source_projection",
            "target": "J_q, Q_q[body], q source tails, arena projection",
            "hunt_result": "SCHEMA_READY_VALUES_MISSING",
            "evidence": "2297 provides component/source envelope and body charge law, all nonclaim/missing numeric or theorem-zero values",
            "route_effect": "componentwise source-bound pack is the honest next lane",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THQ2313_5_verdict",
            "target": "continue no-pole source hunt or activate bound runner",
            "hunt_result": "SYMPLECTIC_SOURCE_NEGATIVE_ACTIVATE_BOUND_RUNNER_NONCLAIM",
            "evidence": "no parent q symplectic potential, q momentum, or q constraint action is sourced in the current inspected chain",
            "route_effect": "independent-q bound-runner lane becomes active private fallback",
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ROUTE2313_0_no_pole",
            "route": "q no-pole/first-class route",
            "decision": "PAUSE_UNTIL_NEW_PARENT_SOURCE",
            "reason": "Theta_q/Omega_q, pi_q, C_q, Q_q, and q constraint action were not found as parent-owned objects",
            "claim_status": "no_claim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ROUTE2313_1_independent_q",
            "route": "independent q bound runner",
            "decision": "ACTIVATE_AS_NONCLAIM_DISCIPLINE_LANE",
            "reason": "once no-pole lacks its first brick, every retained q effect must be bounded with source-backed inputs",
            "claim_status": "schema_active_not_score_ready",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ROUTE2313_2_auxiliary_q",
            "route": "auxiliary/Schur q branch",
            "decision": "RETAIN_AS_SUBCASE_OF_BOUND_RUNNER",
            "reason": "if Z_q=0 or q is algebraic, contact/higher-curvature terms must still be bounded or zero-proved",
            "claim_status": "subcase_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ROUTE2313_3_verdict",
            "route": "current working route",
            "decision": "BOUND_RUNNER_ACTIVE_NO_PUBLIC_CLAIM",
            "reason": "this prevents another no-pole lap without new evidence while preserving the derivation route if a real Theta_q source appears later",
            "claim_status": "private_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def build_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2313_0_branch_predicate",
            "runner_input": "active branch predicate",
            "required_input": "CLOSE2312_6 not closed and THQ2313_5 source hunt negative",
            "current_status": "ACTIVE_NONCLAIM",
            "runner_effect": "use independent-q source/bound schema until a new parent no-pole source appears",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2313_1_operator",
            "runner_input": "Z_q, M_q^2, lambda_q, boundary/domain",
            "required_input": "source-backed q Hessian in one normalization; lambda_q=sqrt(Z_q/M_q^2) when massive",
            "current_status": "MISSING_PARENT_HESSIAN",
            "runner_effect": "no numeric response or range can be computed yet",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2313_2_curvature_source",
            "runner_input": "D_qWeyl2 and optional D_qWeylDual",
            "required_input": "parent action coefficient or theorem-zero; sign and units",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "runner_effect": "Weyl2 source branch remains symbolic only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2313_3_matter_body_tails",
            "runner_input": "J_q components, Q_q[body], Q_q_boundary, readout/history/projector/tails",
            "required_input": "componentwise zero theorem or absolute source-backed bound",
            "current_status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "runner_effect": "no exterior-vacuum-only shortcut allowed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2313_4_projection",
            "runner_input": "P_arena for R10/PPN/clocks/orbital/local-GR",
            "required_input": "map q profile/source vector into observables in the same normalization",
            "current_status": "MISSING_ARENA_PROJECTION",
            "runner_effect": "no empirical score can be run yet",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2313_5_background_kernel",
            "runner_input": "Schwarzschild Weyl2 kernel",
            "required_input": "C_abcd C^abcd=48 mu^2/r^6 and integral 64 pi mu^2/R^3 usable only after coefficient/operator/source conventions are filled",
            "current_status": "EXACT_BACKGROUND_KERNEL_READY_NONCLAIM",
            "runner_effect": "first local/orbital kernel can be reused later, not a claim now",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RUN2313_6_score_gate",
            "runner_input": "score permission",
            "required_input": "RUN2313_1 through RUN2313_4 all source-backed or theorem-zero",
            "current_status": "CLAIM_AND_SCORE_BLOCKED",
            "runner_effect": "activation means workflow lane, not numerical evidence",
            "valid_for_claim": "false",
        },
    ]


def build_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2313_0_operator_first",
            "priority": "P1",
            "input_to_fill": "Z_q, M_q^2, lambda_q, q units, q boundary/domain",
            "why_first": "without the q operator there is no range, Green function, response amplitude, or comparison to local tests",
            "source_candidate": "parent q action/Hessian or theorem-zero/auxiliary proof",
            "next_action": "attempt independent q Hessian operator source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2313_1_curvature_second",
            "priority": "P2",
            "input_to_fill": "D_qWeyl2 and D_qWeylDual",
            "why_first": "Schwarzschild Weyl2 kernel is ready but cannot drive a q profile without the coefficient",
            "source_candidate": "parent higher-curvature/q coupling term or zero theorem",
            "next_action": "fill after or alongside operator source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2313_2_source_vector",
            "priority": "P3",
            "input_to_fill": "J_q components and Q_q[body]/boundary/tails",
            "why_first": "body/worldtube and tails can source q even when exterior vacuum source is zero",
            "source_candidate": "2297 component-bound pack",
            "next_action": "fill componentwise zero/bound rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2313_3_projection",
            "priority": "P4",
            "input_to_fill": "tau_R10, tau_PPN, tau_clock, tau_orbital, qbar/Qbar/K",
            "why_first": "tests cannot be scored until q variables map to observables",
            "source_candidate": "arena-specific projection derivation",
            "next_action": "derive after operator/source convention is fixed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2313_4_verdict",
            "priority": "selected next",
            "input_to_fill": "independent q Hessian/operator source",
            "why_first": "operator ownership is the denominator for every bound",
            "source_candidate": "2314 target",
            "next_action": "2314-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill.md",
            "valid_for_claim": "false",
        },
    ]


def build_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRC2313_0_equation",
            "contract_item": "q equation",
            "formula": "(-Z_q Box + M_q^2) q = -D_qWeyl2 C^2 - D_qWeylDual CstarC - J_q - boundary_tail",
            "acceptance_rule": "all symbols must be source-backed in one normalization before scoring",
            "status": "FORMAL_CONTRACT_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRC2313_1_absolute_source",
            "contract_item": "absolute source envelope",
            "formula": "||source_q|| <= |D_qWeyl2| ||C^2|| + |D_qWeylDual| ||CstarC|| + sum_i ||J_q_i|| + ||boundary_tail||",
            "acceptance_rule": "no cancellation between unknown source channels",
            "status": "ABS_ENVELOPE_SCHEMA",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRC2313_2_response",
            "contract_item": "q response bound",
            "formula": "||q||_arena <= ||G_q||_arena ||source_q|| with massive/Yukawa or massless domain chosen explicitly",
            "acceptance_rule": "G_q requires Z_q, M_q^2, boundary/domain and units",
            "status": "OPERATOR_DEPENDENT_SCHEMA",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRC2313_3_observable",
            "contract_item": "observable projection",
            "formula": "observable_residual <= tau_arena dot abs(q_operator, q_source, q_projection_tail)",
            "acceptance_rule": "R10/PPN/clock/orbital/local-GR each needs its own tau/P_arena",
            "status": "PROJECTION_SCHEMA",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BRC2313_4_claim_policy",
            "contract_item": "claim policy",
            "formula": "claim_allowed = all required inputs numeric/source-backed or theorem-zero and residual <= bound",
            "acceptance_rule": "placeholder, fitted cancellation, or template-only rows refuse scoring",
            "status": "RUNNER_POLICY_ACTIVE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2313_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit is reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2313_1_thetaq_source", "gate": "Theta_q/Omega_q parent source found", "passed": "false", "claim_effect": "no-pole remains paused", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2313_2_bound_runner_active", "gate": "bound-runner lane activated as nonclaim workflow", "passed": "true", "claim_effect": "workflow moves forward", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2313_3_operator_ready", "gate": "q operator/Hessian source-backed", "passed": "false", "claim_effect": "cannot score q response", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2313_4_source_projection_ready", "gate": "source vector and arena projection source-backed", "passed": "false", "claim_effect": "cannot score local tests", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2313_5_local_GR_Newton", "gate": "derived local GR/Newton recovery allowed", "passed": "false", "claim_effect": "still a target", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2313_0_no_pole", "claim": "q no-pole is proven", "allowed": "false", "reason": "Theta_q/Omega_q and q constraint action are not sourced", "blocking_rows": "THQ2313_5_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2313_1_score_runner", "claim": "score independent q bound runner now", "allowed": "false", "reason": "operator, coefficient, source vector, and projection inputs are missing", "blocking_rows": "RUN2313_6_score_gate", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2313_2_use_weyl_kernel_as_claim", "claim": "Schwarzschild Weyl2 kernel proves or rules out local branch", "allowed": "false", "reason": "kernel is background source shape only; q coefficient/operator/projection are missing", "blocking_rows": "RUN2313_5_background_kernel", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2313_3_public_push", "claim": "publish as local-GR proof", "allowed": "false", "reason": "this checkpoint is a private route pivot and nonclaim runner activation", "blocking_rows": "CG2313_5_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2313_0",
            "next_target": "2314-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill.md",
            "why": "operator ownership is the first denominator for every independent-q bound; without Z_q/M_q^2/lambda_q no local empirical score can be meaningful",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    priority_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, hunt_rows, route_rows, runner_rows, priority_rows, contract_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    formalization_output_markers = (
        "2313-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2313",
        "P8_Y5_BRR545_2313",
        "Q_THETAQ_SOURCE_HUNT_2313",
        "JR2313_",
        "q_bound_runner_activation_nonclaim_2313",
        "Y5_R2FR_q_symplectic_potential_source_or_independent_q_bound_runner_activation_2313",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2313_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2313_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2313_02_symplectic_hunt_negative", any(row["row_id"] == "THQ2313_5_verdict" and row["hunt_result"] == "SYMPLECTIC_SOURCE_NEGATIVE_ACTIVATE_BOUND_RUNNER_NONCLAIM" for row in hunt_rows), "Theta_q/Omega_q source hunt verdict is negative"))
    checks.append(("VAL2313_03_bound_runner_active", any(row["row_id"] == "ROUTE2313_1_independent_q" and row["decision"] == "ACTIVATE_AS_NONCLAIM_DISCIPLINE_LANE" for row in route_rows), "bound-runner lane activated as nonclaim workflow"))
    checks.append(("VAL2313_04_runner_score_blocked", any(row["row_id"] == "RUN2313_6_score_gate" and row["current_status"] == "CLAIM_AND_SCORE_BLOCKED" for row in runner_rows), "runner scoring remains blocked"))
    checks.append(("VAL2313_05_priority_selected", any(row["row_id"] == "PRI2313_4_verdict" and "2314-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill.md" in row["next_action"] for row in priority_rows), "operator first-fill selected"))
    checks.append(("VAL2313_06_contract_written", {"BRC2313_0_equation", "BRC2313_1_absolute_source", "BRC2313_2_response", "BRC2313_3_observable"}.issubset({row["row_id"] for row in contract_rows}), "bound-runner contract is written"))
    checks.append(("VAL2313_07_claims_blocked", any(row["row_id"] == "CG2313_5_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2313_08_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2313_09_next_target", any(row["row_id"] == "NEXT2313_0" and "2314-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill.md" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2313_10_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2313_11_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2313_12_formalization_untouched_by_2313", len(formalization_hits) == 0, "no 2313 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2313_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2313 finds no parent Theta_q/Omega_q or q constraint source, pauses the no-pole route until new evidence, activates the independent-q bound-runner lane as nonclaim, and selects q Hessian/operator ownership as the next first-fill target.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    priority_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2313 — q Symplectic Potential Source Or Independent q Bound-Runner Activation",
        "",
        "## Summary",
        "",
        "2313 makes the fork explicit. The inspected corpus does not currently contain a parent-owned `Theta_q/Omega_q`, `pi_q`, or explicit q constraint action. The no-pole route remains mathematically alive, but it is paused until a genuinely new parent source appears.",
        "",
        "The active private lane is now the independent-q bound runner. This is not a claim and not a numerical score. It is the disciplined fallback: source the q operator first, then q curvature/source coefficients, then body/boundary/tails, then arena projections. The Schwarzschild Weyl2 kernel is ready as a background source shape, but cannot be used as evidence until the q operator and coefficients are owned.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Theta_q Source Hunt",
        "",
        md_table(hunt_rows, ["row_id", "target", "hunt_result", "evidence", "route_effect", "valid_for_claim"]),
        "",
        "## Route Decision",
        "",
        md_table(route_rows, ["row_id", "route", "decision", "reason", "claim_status", "valid_for_claim"]),
        "",
        "## Independent q Bound-Runner Activation",
        "",
        md_table(runner_rows, ["row_id", "runner_input", "required_input", "current_status", "runner_effect", "valid_for_claim"]),
        "",
        "## Input Priority Ledger",
        "",
        md_table(priority_rows, ["row_id", "priority", "input_to_fill", "why_first", "source_candidate", "next_action", "valid_for_claim"]),
        "",
        "## Bound-Runner Contract",
        "",
        md_table(contract_rows, ["row_id", "contract_item", "formula", "acceptance_rule", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = build_sources()
    hunt_rows = build_source_hunt_rows()
    route_rows = build_route_rows()
    runner_rows = build_runner_rows()
    priority_rows = build_priority_rows()
    contract_rows = build_contract_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["source_hunt"], hunt_rows)
    write_csv(OUTPUTS["route"], route_rows)
    write_csv(OUTPUTS["runner"], runner_rows)
    write_csv(OUTPUTS["priority"], priority_rows)
    write_csv(OUTPUTS["contract"], contract_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        hunt_rows,
        route_rows,
        runner_rows,
        priority_rows,
        contract_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        hunt_rows,
        route_rows,
        runner_rows,
        priority_rows,
        contract_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2313_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
