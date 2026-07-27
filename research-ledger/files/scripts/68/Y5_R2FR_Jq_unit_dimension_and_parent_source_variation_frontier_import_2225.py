from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2225-Y5-R2FR-Jq-unit-dimension-and-parent-source-variation-frontier-import.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_JQ_QNORM_FRONTIER_2225"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2224_doc": ROOT / "2224-Y5-R2FR-source-norm-and-direct-memory-residual-frontier-import.md",
    "2224_validation": OUT / "P8_Y5_BRR545_2224_VALIDATION.csv",
    "2224_unit": OUT / "P8_Y5_PARENT_QLOC_2224_JQ_UNIT_SOURCE_VARIATION_GATE.csv",
    "2224_next": OUT / "P8_Y5_PARENT_QLOC_2224_NEXT_TARGET.csv",
    "1549_doc": ROOT / "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
    "1549_validation": OUT / "P8_Y5_BRR545_1549_VALIDATION.csv",
    "1549_variational": OUT / "P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv",
    "1549_units": OUT / "P8_Y5_PARENT_QLOC_1549_UNIT_PAIRING_THEOREM_CONDITIONAL.csv",
    "1549_cqm": OUT / "P8_Y5_PARENT_QLOC_1549_CQM_PAIRING_REQUIREMENTS.csv",
    "1550_doc": ROOT / "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md",
    "1550_validation": OUT / "P8_Y5_BRR545_1550_VALIDATION.csv",
    "1550_dual": OUT / "P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv",
    "1550_unit": OUT / "P8_Y5_PARENT_QLOC_1550_SCG_ENVELOPE_UNIT_GATE.csv",
    "1551_doc": ROOT / "1551-Y5-parent-qnorm-source-or-local-closure-demotion.md",
    "1551_validation": OUT / "P8_Y5_BRR545_1551_VALIDATION.csv",
    "1551_hunt": OUT / "P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_SOURCE_HUNT.csv",
    "1551_reentry": OUT / "P8_Y5_PARENT_QLOC_1551_QNORM_REENTRY_CONDITIONS.csv",
    "1552_doc": ROOT / "1552-Y5-parent-q-sector-action-norm-extraction-template.md",
    "1552_validation": OUT / "P8_Y5_BRR545_1552_VALIDATION.csv",
    "1552_template": OUT / "P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv",
    "1552_algorithm": OUT / "P8_Y5_PARENT_QLOC_1552_QNORM_EXTRACTION_ALGORITHM.csv",
    "1552_runner": OUT / "P8_Y5_PARENT_QLOC_1552_REENTRY_RUNNER_NONCLAIM.csv",
    "1552_next": OUT / "P8_Y5_PARENT_QLOC_1552_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2225_SOURCE_REGISTER.csv"
FRONTIER_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2225_JQ_UNIT_FRONTIER_IMPORT.csv"
VARIATIONAL_GATE = OUT / "P8_Y5_PARENT_QLOC_2225_VARIATIONAL_SOURCE_CURRENT_GATE.csv"
QNORM_GATE = OUT / "P8_Y5_PARENT_QLOC_2225_QNORM_DUAL_PAIRING_GATE.csv"
CLOSURE_GATE = OUT / "P8_Y5_PARENT_QLOC_2225_CLOSURE_DEMOTION_GATE.csv"
REENTRY_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2225_PARENT_QSECTOR_REENTRY_TEMPLATE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2225_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2225_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2225_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2225_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2225_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2225_JQ_QNORM_FRONTIER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "Jq_qnorm_frontier_nonclaim_2225.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_JQ_QNORM_FRONTIER_2225_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    FRONTIER_IMPORT,
    VARIATIONAL_GATE,
    QNORM_GATE,
    CLOSURE_GATE,
    REENTRY_TEMPLATE,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "theorem_zero_adopted": False,
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


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "theorem_zero_adopted",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2225_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2225" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        if key.startswith("2224"):
            role = "current source-residual handoff into J_q unit closure"
        elif key.startswith("1549"):
            role = "variational source-current and unit-pairing frontier"
        elif key.startswith("1550"):
            role = "same-norm C_qm/T_source dual-pairing contract"
        elif key.startswith("1551"):
            role = "parent q-norm source hunt and closure demotion"
        elif key.startswith("1552"):
            role = "parent q-sector action/norm extraction template"
        else:
            role = "input evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2225_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def frontier_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "FRONT2225_0_1549",
            "1549 J_q source-current law",
            "delta S_matter = int_W J_A delta q^A dV_e + boundary defines J_q only if the parent action owns q",
            "IMPORT_AS_CONDITIONAL_VARIATIONAL_LAW",
            "S_matter[q], q(Phi), dim(q_loc), coupling projector and boundary terms not supplied",
        ),
        (
            "FRONT2225_1_1550",
            "1550 same-norm dual pairing",
            "|<J_q,Dq[v_m]>| <= T_source_norm*C_qm is a clean Holder/Cauchy bound in one parent-owned E norm",
            "IMPORT_AS_UNIT_LEGAL_PAIRING",
            "E, J_q and Dq[v_m] are not all parent-derived in the same norm",
        ),
        (
            "FRONT2225_2_1551",
            "1551 closure demotion",
            "no accepted parent q norm was found; finite local q-norm route is closure-only until reentry conditions close",
            "IMPORT_AS_NONCLAIM_DEMOTION",
            "q field, norm, variation domain, J_q, Dq[v_m], boundary residuals and arena kernels missing",
        ),
        (
            "FRONT2225_3_1552",
            "1552 parent q-sector template",
            "the exact action slots and q-norm extraction algorithm are written, but the template is not a supplied action",
            "IMPORT_AS_REENTRY_CONTRACT",
            "minimal parent q-sector ansatz must be attempted or rejected without local-data tuning",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "frontier_id": frontier_id,
            "checkpoint": checkpoint,
            "imported_result": result,
            "current_2225_use": use,
            "remaining_blocker": blocker,
            **flags(),
        }
        for frontier_id, checkpoint, result, use, blocker in entries
    ]


def variational_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "VAR2225_0_definition",
            "J_q^A",
            "delta S_matter|_{psi,e_obs}=int_W dV_e J_A delta q^A + boundary",
            "CONDITIONAL_THEOREM_IMPORTED",
            "parent S_matter must explicitly depend on q or q(Phi) in the same observed frame",
            "if supplied, J_q is not an empirical fit but the source current dual to q",
        ),
        (
            "VAR2225_1_chain_rule",
            "q(Phi) chain rule",
            "delta S_matter/delta Phi^I includes (delta q^A/delta Phi^I)J_A",
            "MISSING_PARENT_Q_MAP",
            "q(Phi), Dq and vertical generator relation must be signed",
            "C_qm remains formal until Dq[v_m] is owned",
        ),
        (
            "VAR2225_2_hilbert_proxy",
            "Hilbert stress proxy",
            "J_A=P_A^{mu_nu}T_{mu_nu} only if parent action derives P_A^{mu_nu}",
            "MISSING_COUPLING_PROJECTOR",
            "do not reuse GR/WEP Hilbert stress as q-source without a projector",
            "prevents smuggling GR conservation into MTS coupling",
        ),
        (
            "VAR2225_3_no_readout",
            "forbidden source definition",
            "J_q != fitted GM, alpha(lambda), gamma-1, beta-1, clock or orbital residual",
            "PASS_GUARD_NONCLAIM",
            "source current must be prior to arena projection",
            "keeps this as field theory rather than patchwork readout fitting",
        ),
        (
            "VAR2225_4_verdict",
            "J_q status",
            "source-current unit law exists conditionally; parent-specific J_q remains absent",
            "NOT_SCORE_READY",
            "q dimension, matter q-dependence, norm and boundary terms missing",
            "local branch remains blocked",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "law_id": law_id,
            "object": obj,
            "formula": formula,
            "status": status,
            "required_parent_input": required,
            "current_result": result,
            **flags(),
        }
        for law_id, obj, formula, status, required, result in entries
    ]


def qnorm_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "QN2225_0_variation_space",
            "E",
            "allowed compact/local q-variation class with boundary and quotient/gauge class fixed",
            "MISSING_PARENT_VARIATION_DOMAIN",
            "cannot choose an arena-convenience norm",
        ),
        (
            "QN2225_1_source_dual",
            "T_source_norm",
            "T_source_norm := sup_{||delta q||_E<=1}|int_W J_A delta q^A dV_e|",
            "CONDITIONAL_REQUIRES_E_AND_JQ",
            "dual source norm is legal only after E and J_q are parent supplied",
        ),
        (
            "QN2225_2_cqm_primal",
            "C_qm",
            "C_qm := ||Dq[v_m]||_E in the same q-norm used by T_source_norm",
            "CONDITIONAL_REQUIRES_DQVM_AND_E",
            "norm switch would invalidate the product bound",
        ),
        (
            "QN2225_3_holder_bound",
            "source leakage bound",
            "|int_W J_A Dq[v_m]^A dV_e| <= T_source_norm*C_qm",
            "CONDITIONAL_THEOREM_IMPORTED",
            "mathematically clean but not computable until parent inputs exist",
        ),
        (
            "QN2225_4_envelope",
            "S_cg source term",
            "S_geom_m <= 1/2*T_source_norm*C_qm",
            "UNIT_ROUTABLE_NOT_SCORE_READY",
            "fits the envelope only with same E, same observed frame, and retained boundary terms",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "pairing_id": pairing_id,
            "object": obj,
            "contract": contract,
            "status": status,
            "blocker": blocker,
            **flags(),
        }
        for pairing_id, obj, contract, status, blocker in entries
    ]


def closure_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "CLOSE2225_0_q_field",
            "parent q/q_loc field definition",
            "field dimension and observed-frame descent are explicit",
            "MISSING",
        ),
        (
            "CLOSE2225_1_norm",
            "parent-owned q-norm E",
            "kinetic/operator metric, Hessian, or regulator norm is sourced and positive/coercive",
            "MISSING",
        ),
        (
            "CLOSE2225_2_variation_domain",
            "allowed variation class",
            "compact support, boundary, quotient/gauge, and regularity domain are declared",
            "MISSING",
        ),
        (
            "CLOSE2225_3_Jq",
            "source current J_q",
            "delta S_matter/delta q is parent-derived in the same frame",
            "MISSING",
        ),
        (
            "CLOSE2225_4_Dqvm",
            "C_qm in same norm",
            "Dq[v_m] is computed in E with no norm switch",
            "MISSING",
        ),
        (
            "CLOSE2225_5_boundary",
            "boundary/source residuals",
            "boundary terms are zero-proved or included in S_boundary_m",
            "MISSING",
        ),
        (
            "CLOSE2225_6_arenas",
            "local arena kernels",
            "Pi_R10/Pi_PPN/Pi_clock/Pi_orbital/Pi_local map the same source norm to observables",
            "MISSING",
        ),
        (
            "CLOSE2225_7_policy",
            "claim policy",
            "no local claim until all previous conditions pass",
            "PASS_GUARD_NONCLAIM",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "closure_id": closure_id,
            "needed_input": needed,
            "acceptance_requirement": requirement,
            "current_status": status,
            **flags(),
        }
        for closure_id, needed, requirement, status in entries
    ]


def reentry_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "RE2225_0_q_field",
            "q-sector field definition",
            "q^A or q^A(Phi) with dim(q^A), observed-frame descent and variation class declared",
            "REQUIRED_NOT_SUPPLIED",
            "q is defined before readout and not selected by local test fits",
        ),
        (
            "RE2225_1_quadratic_form",
            "positive parent quadratic form",
            "delta^2 S_q = 1/2 int_W delta q^A G_AB delta q^B dV_e + boundary",
            "REQUIRED_NOT_SUPPLIED",
            "G_AB defines one parent-owned E used by both T_source_norm and C_qm",
        ),
        (
            "RE2225_2_derivative_operator",
            "kinetic/operator terms",
            "int_W 1/2 Z_AB^{mu nu} nabla_mu q^A nabla_nu q^B dV_e",
            "OPTIONAL_ROUTE_NOT_SUPPLIED",
            "operator must produce a positive local norm or be quotient/gauge removed",
        ),
        (
            "RE2225_3_regulator",
            "worldtube regulator/excision",
            "E_epsilon[delta q;W_src] with support and matching surface",
            "OPTIONAL_ROUTE_NOT_SUPPLIED",
            "same regulator enters source norm, C_qm and arena projections",
        ),
        (
            "RE2225_4_matter_coupling",
            "matter source variation",
            "delta S_matter = int_W J_A delta q^A dV_e + boundary",
            "REQUIRED_NOT_SUPPLIED",
            "J_q is parent-derived and not a readout-defined source",
        ),
        (
            "RE2225_5_boundary",
            "boundary and domain terms",
            "delta S_boundary plus integration-by-parts boundary terms",
            "REQUIRED_NOT_SUPPLIED",
            "no boundary term is silently dropped before S_cg scoring",
        ),
        (
            "RE2225_6_no_hair",
            "local exterior silence",
            "q-sector perturbations must not generate exterior reciprocal hair or fitted local tails",
            "REQUIRED_NOT_SUPPLIED",
            "minimal ansatz must pass local silence before empirical scoring",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "slot_id": slot_id,
            "action_slot": slot,
            "template_formula": formula,
            "current_status": status,
            "acceptance_test": acceptance,
            **flags(),
        }
        for slot_id, slot, formula, status, acceptance in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "CG2225_0_import",
            "1549-1552 J_q/q-norm frontier imported",
            "PASS_NONCLAIM",
            "conditional variational law, same-norm pairing, demotion and reentry template are connected to current R2FR numbering",
        ),
        (
            "CG2225_1_Jq",
            "parent source current J_q supplied",
            "BLOCKED_NONCLAIM",
            "no parent S_matter[q] or q(Phi) coupling projector has been supplied",
        ),
        (
            "CG2225_2_qnorm",
            "parent-owned q-norm E supplied",
            "BLOCKED_NONCLAIM",
            "positive/coercive kinetic, Hessian or regulator norm remains absent",
        ),
        (
            "CG2225_3_Cqm_pairing",
            "C_qm and T_source_norm paired in same E",
            "BLOCKED_NONCLAIM",
            "Dq[v_m] is not norm-evaluated in parent E",
        ),
        (
            "CG2225_4_envelope",
            "S_cg finite source envelope computable",
            "BLOCKED_NO_CLAIM",
            "E, J_q, Dq[v_m], direct/source-extra/boundary terms and arena kernels remain missing",
        ),
        (
            "CG2225_5_local_GR",
            "derived local GR/Newton/PPN recovery",
            "BLOCKED_NO_CLAIM",
            "local branch is closure-only until parent q-sector ansatz closes or is rejected",
        ),
        (
            "CG2225_6_GitHub",
            "public/GitHub update",
            "BLOCKED_NONCLAIM",
            "private proof line remains mid-derivation and should not be promoted",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2225_0_import",
            "Import 1549-1552 as the current J_q/q-norm frontier.",
            "FRONTIER_CONNECTED",
            "the unit law and same-norm product bound are now connected to the current R2FR line",
        ),
        (
            "DEC2225_1_clean_math",
            "Keep the variational source-current and Holder pairing as conditional wins.",
            "CONDITIONAL_STRUCTURE_ACCEPTED",
            "the mathematics is not the problem; the absent parent q-sector is the problem",
        ),
        (
            "DEC2225_2_no_claim",
            "Do not reopen local claims.",
            "PARENT_QSECTOR_NOT_SUPPLIED",
            "J_q, E and Dq[v_m] are not simultaneously parent-owned",
        ),
        (
            "DEC2225_3_next",
            "Move to a minimal parent q-sector action ansatz attempt or rejection.",
            "NEXT_2226_MINIMAL_QSECTOR_ACTION",
            "this is the least patchwork route: derive a parent E/J_q/Dq package before any local data scoring",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in entries
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2225_0_2226",
            "target_file": "2226-Y5-R2FR-minimal-parent-q-sector-action-ansatz-or-rejection.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_q_sector_action_ansatz_or_rejection_2226.py",
            "objective": "attempt the least-assumption parent q-sector action that supplies q, E, J_q and Dq[v_m] without exterior hair or local-data tuning, or reject the route explicitly",
            "success_condition": "a parent q-sector ansatz passes positivity, quotient/gauge, boundary and no-hair filters, or the local finite branch is demoted to closure-only with exact missing theorem clauses",
            "do_not": "do not choose coefficients from R10/PPN/clock/orbital fits; do not mix norms; do not claim GR/Newton reduction from an ansatz template",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(CLOSURE_GATE, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(CLOSURE_GATE),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    frontier: list[dict[str, Any]],
    variational: list[dict[str, Any]],
    qnorm: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    reentry: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2225 - Y5/R2FR J_q Unit Dimension And Parent Source Variation Frontier Import",
            "## Verdict\n"
            "- 2225 imports the `1549-1552` J_q/q-norm frontier into the current R2FR line.\n"
            "- The useful win is conditional but real: `J_q` has a clean variational definition, and `T_source_norm*C_qm` is unit/legal only as a same-norm dual pairing.\n"
            "- The blocking fact is also now clean: parent-specific `S_matter[q]`, `dim(q_loc)`, the parent q-norm `E`, and `Dq[v_m]` in that same norm are not supplied.\n"
            "- Therefore the finite local branch remains closure-only; no local GR/Newton/R10/PPN/clock/orbital claim is reopened.\n"
            "- Next move is not another arena test; it is the minimal parent q-sector action ansatz or rejection.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## J_q Unit Frontier Import\n"
            + md_table(frontier, ["frontier_id", "checkpoint", "imported_result", "current_2225_use", "remaining_blocker"]),
            "## Variational Source Current Gate\n"
            + md_table(variational, ["law_id", "object", "formula", "status", "required_parent_input", "current_result"]),
            "## q-norm Dual Pairing Gate\n"
            + md_table(qnorm, ["pairing_id", "object", "contract", "status", "blocker"]),
            "## Closure Demotion Gate\n"
            + md_table(closure, ["closure_id", "needed_input", "acceptance_requirement", "current_status"]),
            "## Parent q-sector Reentry Template\n"
            + md_table(reentry, ["slot_id", "action_slot", "template_formula", "current_status", "acceptance_test"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "rationale"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "target_file", "target_script", "objective", "success_condition", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is the coupling gate in its sharpest current form. The branch has found a legitimate mathematical shape for the local source term, but it has not yet earned the physical coupling. The parent theory must now either supply a q-sector action whose second variation gives a positive/coercive local norm and whose matter variation gives `J_q`, or admit that the local finite branch is a closure device rather than a derived GR/Newton limit.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    prior_validations = [
        SOURCE_FILES["2224_validation"],
        SOURCE_FILES["1549_validation"],
        SOURCE_FILES["1550_validation"],
        SOURCE_FILES["1551_validation"],
        SOURCE_FILES["1552_validation"],
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2225 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_01_prior_validations",
            "result": "PASS" if all(validation_pass(path) for path in prior_validations) else "FAIL",
            "detail": "all imported validation files pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_02_frontier_import",
            "result": "PASS" if len(read_csv(FRONTIER_IMPORT)) == 4 else "FAIL",
            "detail": "1549-1552 frontier imported",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_03_variational_law",
            "result": "PASS" if any(row["status"] == "CONDITIONAL_THEOREM_IMPORTED" for row in read_csv(VARIATIONAL_GATE)) else "FAIL",
            "detail": "J_q variational law retained as conditional theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_04_same_norm_pairing",
            "result": "PASS" if any("same q-norm" in row["contract"] for row in read_csv(QNORM_GATE)) else "FAIL",
            "detail": "T_source_norm and C_qm same-norm contract recorded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_05_closure_blockers",
            "result": "PASS" if sum(row["current_status"] == "MISSING" for row in read_csv(CLOSURE_GATE)) >= 6 else "FAIL",
            "detail": "parent q/action/norm inputs remain explicit blockers",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_06_reentry_template",
            "result": "PASS" if len(read_csv(REENTRY_TEMPLATE)) >= 6 else "FAIL",
            "detail": "parent q-sector reentry template written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_07_claims_blocked",
            "result": "PASS" if all("BLOCKED" in row["status"] or row["status"].startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "local GR and empirical claims remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_08_decision_next",
            "result": "PASS" if any(row["result"] == "NEXT_2226_MINIMAL_QSECTOR_ACTION" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects minimal parent q-sector action next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_09_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["target_file"].startswith("2226-Y5-R2FR-minimal-parent-q-sector-action") else "FAIL",
            "detail": "next target is current-numbered minimal parent q-sector action attempt or rejection",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_10_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2225 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_11_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_12_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_13_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_14_formalization_no_2225",
            "result": "PASS" if formalization_2225_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no 2225 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_15_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2225 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2225_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2225 imports the J_q/unit/q-norm frontier, accepts the conditional variational/same-norm structure, keeps local claims blocked, and selects minimal parent q-sector action ansatz or rejection next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    frontier = frontier_rows()
    variational = variational_rows()
    qnorm = qnorm_rows()
    closure = closure_rows()
    reentry = reentry_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(FRONTIER_IMPORT, frontier)
    write_csv(VARIATIONAL_GATE, variational)
    write_csv(QNORM_GATE, qnorm)
    write_csv(CLOSURE_GATE, closure)
    write_csv(REENTRY_TEMPLATE, reentry)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            frontier,
            variational,
            qnorm,
            closure,
            reentry,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2225 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
