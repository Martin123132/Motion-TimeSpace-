from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_GK_VACUUM_NO_HAIR_POSITIVITY_OR_STRESS_BOUND_2470"
CHECKPOINT_ID = "2470"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GK_NOHAIR_2470_SOURCE_REGISTER.csv",
    "positivity_clauses": OUT / "P8_Y5_GK_NOHAIR_2470_POSITIVITY_CLAUSES.csv",
    "nohair_attempt": OUT / "P8_Y5_GK_NOHAIR_2470_NOHAIR_PROOF_ATTEMPT.csv",
    "failure_modes": OUT / "P8_Y5_GK_NOHAIR_2470_FAILURE_MODES.csv",
    "stress_bound": OUT / "P8_Y5_GK_NOHAIR_2470_STRESS_BOUND_FALLBACK.csv",
    "metric_reduction": OUT / "P8_Y5_GK_NOHAIR_2470_METRIC_REDUCTION_STATUS.csv",
    "promotion_verdict": OUT / "P8_Y5_GK_NOHAIR_2470_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_GK_NOHAIR_2470_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GK_NOHAIR_2470_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GK_NOHAIR_2470_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GK_NOHAIR_2470_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2470_VALIDATION.csv",
}

COPY_TARGETS = {
    "nohair_contract": LOCAL_BOUNDS / "GK_nohair_positivity_contract_2470_NONCLAIM.csv",
    "stress_bound": LOCAL_BOUNDS / "GK_stress_bound_fallback_2470_NONCLAIM.csv",
    "failure_modes": QUEUE / "JR2470_GK_NOHAIR_FAILURE_MODES_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2470_00_2469_doc",
        "source_path": ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
        "needles": ["STL2469_6_conditional_result", "MET2469_3_current_corpus", "NEXT2469_0_selected", "VAL2469_OVERALL"],
        "role": "handoff selecting GK no-hair/positivity gate",
    },
    {
        "source_id": "SRC2470_01_2469_stealth",
        "source_path": OUT / "P8_Y5_GK_STRESS_2469_STEALTH_BRANCH_CONDITIONS.csv",
        "needles": ["STL2469_4_positive_gap", "STL2469_5_boundary_no_hair", "CONDITIONAL_CONTRACT_ONLY"],
        "role": "stealth branch conditions to prove or bound",
    },
    {
        "source_id": "SRC2470_02_2469_ppn",
        "source_path": OUT / "P8_Y5_GK_STRESS_2469_PPN_RESIDUAL_LEDGER.csv",
        "needles": ["PPN2469_2_hair_bound", "BOUND_FORM_ONLY"],
        "role": "stress-bound fallback handoff",
    },
    {
        "source_id": "SRC2470_03_2464_candidate_action",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2464_A_vertical_generator_current_law", "L_K", "L_Gamma"],
        "role": "candidate action requiring positivity",
    },
    {
        "source_id": "SRC2470_04_2465_dimension",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2465_DIMENSION_AUDIT.csv",
        "needles": ["DIM2465_3_viable_branch", "DIM2465_4_Khat_dimension"],
        "role": "dimension branch for positive quadratic operators",
    },
    {
        "source_id": "SRC2470_05_2468_theorem",
        "source_path": OUT / "P8_Y5_STATIONARY_SOURCE_2468_PROOF_STEPS.csv",
        "needles": ["PRF2468_4_projected_q_zero", "PRF2468_6_not_full_GR"],
        "role": "stationary q_loc theorem and remaining nonclaim limit",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def positivity_clause_rows() -> list[dict[str, Any]]:
    rows = [
        ("POS2470_0_operator_field", "u=(A_nu, Gamma_eff-Gamma_0) on stationary exterior domain Omega", "defines no-hair variables", "CONDITIONAL_INPUT"),
        ("POS2470_1_quadratic_form", "E_GK[u] >= c_A||nabla A||^2+c_m||A||^2+c_G||nabla Gamma||^2+c_g||Gamma-Gamma_0||^2 - boundary", "coercive positive exterior energy", "REQUIRED_NOT_DERIVED"),
        ("POS2470_2_cross_term_bound", "A.nabla Gamma and other mixings obey |cross| <= eta E_positive with eta<1", "prevents tachyon/ghost hair from the A-Gamma coupling", "REQUIRED_NOT_DERIVED"),
        ("POS2470_3_vacuum_normalization", "L_Gamma(Gamma_0)=0 and dL_Gamma/dGamma|Gamma_0=0 or fixed Lambda subtraction is parent-signed", "removes vacuum energy stress", "REQUIRED_NOT_DERIVED"),
        ("POS2470_4_boundary_condition", "u=0, finite energy plus asymptotic vacuum, or no-flux boundary conditions select the trivial exterior mode", "boundary no-hair", "REQUIRED_NOT_DERIVED"),
        ("POS2470_5_no_topological_hair", "Omega carries no unsourced topological GK charge/harmonic mode", "excludes q_loc=0 but stressful harmonic sectors", "REQUIRED_NOT_DERIVED"),
        ("POS2470_6_parent_sign", "all positivity/sign choices come from parent action, not local test fitting", "anti-circularity", "REQUIRED_NOT_DERIVED"),
    ]
    return [{**base_row(), "positivity_id": i, "clause": c, "why_needed": why, "status": st} for i, c, why, st in rows]


def nohair_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        ("NH2470_0_stationary_domain", "Take stationary exterior Omega with J_M=0 and q_loc=0 from 2468.", "stationary local-source theorem", "PASS_CONDITIONAL_INPUT"),
        ("NH2470_1_euler_system", "Use A/Gamma Euler equations from ACT2464_A in Omega.", "source-free GK equations", "PASS_AS_FORMAL_INPUT"),
        ("NH2470_2_energy_identity", "Multiply Euler system by u and integrate by parts to get E_GK[u]=boundary_flux plus possible cross/topological terms.", "standard elliptic/no-hair method", "PASS_AS_METHOD"),
        ("NH2470_3_boundary_zero", "If boundary flux and topological terms vanish, E_GK[u]=0.", "POS2470_4 and POS2470_5", "CONDITIONAL"),
        ("NH2470_4_coercive_zero", "If E_GK is coercive positive, E_GK[u]=0 implies u=0.", "POS2470_1 and POS2470_2", "CONDITIONAL"),
        ("NH2470_5_stress_zero", "If u=0 and vacuum energy is normalized, T_GK^{mu nu}=0 or fixed Lambda.", "POS2470_3", "CONDITIONAL"),
        ("NH2470_6_current_status", "Current corpus lacks explicit L_K/L_Gamma signs, cross-term bound, parent scale and boundary no-hair proof.", "source audit", "NOT_PROMOTED"),
    ]
    return [{**base_row(), "nohair_id": i, "proof_step": step, "basis": basis, "status": st} for i, step, basis, st in rows]


def failure_mode_rows() -> list[dict[str, Any]]:
    rows = [
        ("FAIL2470_0_ghost_or_tachyon", "quadratic form not positive", "homogeneous stressful modes survive", "blocks GR/PPN"),
        ("FAIL2470_1_A_Gamma_cross_instability", "A.nabla Gamma cross term overwhelms positive terms", "q_loc=0 can coexist with hair", "requires coefficient bound"),
        ("FAIL2470_2_vacuum_energy", "L_Gamma(Gamma_0) not zero or not fixed", "local cosmological/stress offset remains", "requires parent subtraction or cosmological accounting"),
        ("FAIL2470_3_boundary_hair", "boundary data sources stationary GK modes", "external T_GK nonzero despite J_M=0", "requires no-hair boundary condition or bound"),
        ("FAIL2470_4_topological_hair", "harmonic/topological sector survives", "PPN residual possible", "requires topology ledger"),
        ("FAIL2470_5_projector_hiding", "P_loc hides nonprojected residual components", "q_loc=0 not full field silence", "requires parent-owned projector/full residual audit"),
    ]
    return [{**base_row(), "failure_id": i, "failure_mode": mode, "effect": effect, "required_fix": fix} for i, mode, effect, fix in rows]


def stress_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND2470_0_energy_to_stress", "||T_GK||_Omega <= C_T E_GK[u] + C_Lambda |L_vac|", "stress controlled by exterior energy plus vacuum offset", "BOUND_FORM_ONLY"),
        ("BND2470_1_energy_bound", "E_GK[u] <= C_B boundary_flux + C_S source_tail + C_X negative_mode_defect", "if no exact no-hair, residual bound route", "BOUND_FORM_ONLY"),
        ("BND2470_2_metric_bound", "||delta g_PPN|| <= C_metric ||T_GK+T_tau/P+boundary||", "linearized local metric response", "BOUND_FORM_ONLY"),
        ("BND2470_3_claim_requirement", "numeric PPN/R10/clock/orbital comparison requires C_T,C_B,C_metric and source-tail coefficients", "future empirical gate", "MISSING_NUMERIC_COEFFICIENTS"),
        ("BND2470_4_nonclaim", "bound form does not pass local GR until coefficients are sourced and below arena limits", "claim discipline", "NONCLAIM"),
    ]
    return [{**base_row(), "bound_id": i, "bound": bound, "basis": basis, "status": st} for i, bound, basis, st in rows]


def metric_reduction_rows() -> list[dict[str, Any]]:
    rows = [
        ("MET2470_0_if_nohair", "If no-hair proof closes, stationary exterior metric equation reduces to GR plus fixed Lambda.", "T_GK=0 and other retained stresses silent", "CONDITIONAL_ROUTE"),
        ("MET2470_1_current", "Current corpus does not close no-hair/positivity.", "missing POS2470 clauses", "BLOCKED_CURRENT_CLAIM"),
        ("MET2470_2_bound_route", "If no-hair fails but stress bound is finite, local tests become residual-bound problem.", "BND2470 ledger", "FALLBACK_ROUTE"),
        ("MET2470_3_needed_next", "Need explicit quadratic L_K/L_Gamma ansatz and sign/cross-term audit.", "to decide no-hair vs bound", "SELECT_NEXT"),
    ]
    return [{**base_row(), "metric_id": i, "statement": s, "basis": b, "status": st} for i, s, b, st in rows]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2470_0_nohair_method", "Is there a valid no-hair proof method?", "YES_CONDITIONAL", "energy identity plus coercivity would prove trivial exterior GK fields", "contract only"),
        ("PV2470_1_current_nohair", "Does current corpus prove no-hair?", "NO", "positivity/cross-term/boundary/topology clauses are unsigned", "blocked"),
        ("PV2470_2_stress_bound", "Is there a fallback if no-hair fails?", "YES_FORMAL_BOUND", "stress-to-metric residual bound written", "nonclaim fallback"),
        ("PV2470_3_GR_status", "Does local GR/PPN pass?", "NO", "no-hair and numeric residual bounds are not closed", "no claim"),
        ("PV2470_4_overall", "Overall 2470 verdict", "NOHAIR_CONTRACT_WRITTEN_NOT_PROVED_BOUND_FALLBACK_READY", "next target is explicit quadratic operator/sign audit", "continue"),
    ]
    return [{**base_row(), "verdict_id": i, "question": q, "result": r, "evidence": e, "effect": eff} for i, q, r, e, eff in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2470_0_nohair_contract", "No-hair positivity proof route is written.", "PASS_AS_CONTRACT", "energy identity/coercivity steps explicit", True, False),
        ("GATE2470_1_nohair_proved", "Current corpus proves no-hair.", "BLOCKED", "positivity and boundary clauses unsigned", False, False),
        ("GATE2470_2_stress_bound", "Stress-bound fallback is available as a form.", "PASS_AS_BOUND_FORM", "residual inequality ledger written", True, False),
        ("GATE2470_3_local_GR_PPN", "local GR/PPN branch passes.", "BLOCKED", "no-hair not proved and bound coefficients missing", False, False),
        ("GATE2470_4_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2470_0_nohair_not_proved", "Do not promote the no-hair theorem.", "key positivity and boundary clauses are not parent-signed", "local GR remains blocked"),
        ("DEC2470_1_best_next", "Attack explicit quadratic GK operator signs next.", "without L_K/L_Gamma signs we cannot choose no-hair or bound route", "2471 selected"),
        ("DEC2470_2_keep_bound", "Keep stress-bound fallback ready.", "if no-hair fails, empirical local tests can still discipline residuals", "future bound runner path preserved"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2470_0_selected",
            "selection_status": "selected",
            "target_file": "2471-Y5-R2FR-explicit-GK-quadratic-operator-sign-audit.md",
            "target_script": "scripts/Y5_R2FR_explicit_GK_quadratic_operator_sign_audit_2471.py",
            "task": "write the minimal quadratic L_K/L_Gamma operator, audit signs/cross-term coercivity, and decide whether no-hair is plausible or the branch must go to stress-bound only",
            "acceptance_target": "operator ansatz, dimension/sign table, cross-term bound, ghost/tachyon checks, no-hair eligibility, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["nohair_attempt"], COPY_TARGETS["nohair_contract"])
    shutil.copyfile(OUTPUTS["stress_bound"], COPY_TARGETS["stress_bound"])
    shutil.copyfile(OUTPUTS["failure_modes"], COPY_TARGETS["failure_modes"])
    source_map = {
        "nohair_contract": OUTPUTS["nohair_attempt"],
        "stress_bound": OUTPUTS["stress_bound"],
        "failure_modes": OUTPUTS["failure_modes"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2470_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2470_01_positivity_clauses", len(data["positivity"]) >= 7 and all(row["status"] in {"CONDITIONAL_INPUT", "REQUIRED_NOT_DERIVED"} for row in data["positivity"]), "positivity/no-hair clauses explicit")
    add("VAL2470_02_nohair_method", any(row["nohair_id"] == "NH2470_5_stress_zero" and row["status"] == "CONDITIONAL" for row in data["nohair"]), "conditional stress-zero proof step written")
    add("VAL2470_03_current_not_promoted", any(row["nohair_id"] == "NH2470_6_current_status" and row["status"] == "NOT_PROMOTED" for row in data["nohair"]), "current no-hair theorem not promoted")
    add("VAL2470_04_failure_modes", len(data["failures"]) >= 6, "failure modes recorded")
    add("VAL2470_05_bound_fallback", any(row["bound_id"] == "BND2470_2_metric_bound" for row in data["bounds"]), "stress-to-metric bound fallback written")
    add("VAL2470_06_metric_blocked", any(row["metric_id"] == "MET2470_1_current" and row["status"] == "BLOCKED_CURRENT_CLAIM" for row in data["metric"]), "current local metric claim blocked")
    add("VAL2470_07_overall_nonclaim", any(row["verdict_id"] == "PV2470_4_overall" and row["result"] == "NOHAIR_CONTRACT_WRITTEN_NOT_PROVED_BOUND_FALLBACK_READY" for row in data["verdicts"]), "overall verdict is nonclaim")
    add("VAL2470_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/PPN claim")
    add("VAL2470_09_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2470_0_selected", "2471 operator sign audit selected")
    add("VAL2470_10_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2470-Y5", "P8_Y5_GK_NOHAIR_2470", "P8_Y5_BRR545_2470", "JR2470")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2470_11_no_formalization_artifacts", not formal_hits, "no 2470 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2470_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2470_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2470_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2470_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2470_OVERALL", all(row["status"] == "PASS" for row in rows), "2470 writes GK no-hair positivity contract, refuses promotion, and prepares stress-bound fallback")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2470 Y5 R2FR GK Vacuum No-hair Positivity Or Stress Bound",
        "",
        "**Status:** no-hair route formalized, not proved. The right theorem shape is now clear: if the stationary exterior GK quadratic energy is coercive, cross-terms are controlled, boundary/topological hair is absent, and vacuum energy is parent-normalized, then the only finite-energy exterior solution is the trivial GK vacuum and `T_GK` is locally silent.",
        "",
        "**Reality check:** current MTS does not yet supply the explicit `L_K/L_Gamma` signs, cross-term bound, no-hair boundary theorem, or parent vacuum normalization. So this checkpoint improves the derivation path but does not pass GR/PPN. If no-hair fails, the fallback is a stress-bound-to-PPN residual runner.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Positivity Clauses",
        markdown_table(data["positivity"], ["positivity_id", "clause", "why_needed", "status"]),
        "",
        "## No-hair Proof Attempt",
        markdown_table(data["nohair"], ["nohair_id", "proof_step", "basis", "status"]),
        "",
        "## Failure Modes",
        markdown_table(data["failures"], ["failure_id", "failure_mode", "effect", "required_fix"]),
        "",
        "## Stress Bound Fallback",
        markdown_table(data["bounds"], ["bound_id", "bound", "basis", "status"]),
        "",
        "## Metric Reduction Status",
        markdown_table(data["metric"], ["metric_id", "statement", "basis", "status"]),
        "",
        "## Promotion Verdict",
        markdown_table(data["verdicts"], ["verdict_id", "question", "result", "evidence", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register(),
        "positivity": positivity_clause_rows(),
        "nohair": nohair_attempt_rows(),
        "failures": failure_mode_rows(),
        "bounds": stress_bound_rows(),
        "metric": metric_reduction_rows(),
        "verdicts": promotion_verdict_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["positivity_clauses"], data["positivity"])
    write_csv(OUTPUTS["nohair_attempt"], data["nohair"])
    write_csv(OUTPUTS["failure_modes"], data["failures"])
    write_csv(OUTPUTS["stress_bound"], data["bounds"])
    write_csv(OUTPUTS["metric_reduction"], data["metric"])
    write_csv(OUTPUTS["promotion_verdict"], data["verdicts"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
