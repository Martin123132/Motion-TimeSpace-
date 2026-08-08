from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2560"
BRANCH_ID = "MTS_R2FR_GK_VACUUM_NO_HAIR_POSITIVITY_OR_STRESS_BOUND_2560"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2560-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2560_SOURCE_REGISTER.csv",
    "positivity_clauses": OUT / "P8_Y5_NO_SHADOW_2560_POSITIVITY_CLAUSES.csv",
    "parent_coefficient_ledger": OUT / "P8_Y5_NO_SHADOW_2560_PARENT_COEFFICIENT_LEDGER.csv",
    "nohair_proof_attempt": OUT / "P8_Y5_NO_SHADOW_2560_NOHAIR_PROOF_ATTEMPT.csv",
    "failure_modes": OUT / "P8_Y5_NO_SHADOW_2560_NOHAIR_FAILURE_MODES.csv",
    "stress_bound_fallback": OUT / "P8_Y5_NO_SHADOW_2560_STRESS_BOUND_FALLBACK.csv",
    "metric_implications": OUT / "P8_Y5_NO_SHADOW_2560_METRIC_IMPLICATIONS.csv",
    "promotion_verdict": OUT / "P8_Y5_NO_SHADOW_2560_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2560_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2560_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2560_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2560_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2560_VALIDATION.csv",
}

COPY_TARGETS = {
    "nohair_contract": LOCAL_BOUNDS / "GK_nohair_positivity_contract_2560_NONCLAIM.csv",
    "stress_bound_fallback": LOCAL_BOUNDS / "GK_stress_bound_fallback_2560_NONCLAIM.csv",
    "operator_sign_queue": QUEUE / "JR2560_GK_QUADRATIC_OPERATOR_SIGN_AUDIT_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2560_00_2559_doc",
        "source_path": ROOT / "2559-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
        "needles": ["NEXT2559_0_selected", "STL2559_1_positive_vacuum_branch", "BND2559_4_current_status", "VAL2559_OVERALL"],
        "role": "active handoff selecting no-hair/positivity or stress-bound fallback",
    },
    {
        "source_id": "SRC2560_01_2559_stealth",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2559_STEALTH_BRANCH_CONDITIONS.csv",
        "needles": ["STL2559_1_positive_vacuum_branch", "STL2559_6_conditional_result", "BLOCKED_CURRENT_CLAIM"],
        "role": "machine-readable stealth branch requirements",
    },
    {
        "source_id": "SRC2560_02_2559_stress_bound",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2559_STRESS_BOUND_FORM.csv",
        "needles": ["BND2559_0_norm_contract", "BND2559_4_current_status", "MISSING_PARENT_COEFFICIENTS"],
        "role": "stress residual fallback and missing parent coefficients",
    },
    {
        "source_id": "SRC2560_03_2559_metric_gate",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2559_LOCAL_METRIC_EQUATION_GATE.csv",
        "needles": ["MET2559_2_stealth_reduction", "MET2559_3_current_corpus", "BLOCKED_CURRENT_CLAIM"],
        "role": "local metric implication gate",
    },
    {
        "source_id": "SRC2560_04_2559_stress_exposure",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2559_STRESS_EXPOSURE.csv",
        "needles": ["STR2559_1_LK", "STR2559_4_LGamma", "STR2559_7_key_lesson"],
        "role": "GK stress components that no-hair must silence",
    },
    {
        "source_id": "SRC2560_05_2554_candidate_action",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2554_A_vertical_generator_current_law", "L_K(g,tau,nabla A)", "L_Gamma"],
        "role": "candidate action requiring explicit signs and coefficients",
    },
    {
        "source_id": "SRC2560_06_2555_variation",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_VARIATION_AUDIT.csv",
        "needles": ["VAR2555_2_delta_A_bulk", "VAR2555_4_delta_Gamma_bulk", "VAR2555_6_not_theorem"],
        "role": "Euler equations used by no-hair proof attempt",
    },
    {
        "source_id": "SRC2560_07_2470_precedent",
        "source_path": ROOT / "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
        "needles": ["POS2470_1_quadratic_form", "NH2470_6_current_status", "VAL2470_OVERALL"],
        "role": "earlier no-hair positivity precedent, re-run against 2559 chain",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for spec in SOURCE_SPECS:
        path = Path(spec["source_path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        exists = path.exists()
        rows.append(
            {
                **base_row(),
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "missing_needles": ";".join(missing),
                "source_pass": bool_text(exists and not missing),
                "role": spec["role"],
            }
        )
    return rows


def positivity_clause_rows() -> list[dict[str, Any]]:
    rows = [
        ("POS2560_0_operator_field", "u=(A_nu, Gamma_eff-Gamma_0) on stationary exterior domain Omega", "defines no-hair variables", "CONDITIONAL_INPUT"),
        ("POS2560_1_quadratic_form", "E_GK[u] >= c_A||nabla A||^2+c_m||A||^2+c_G||nabla Gamma||^2+c_g||Gamma-Gamma_0||^2 - boundary", "coercive positive exterior energy", "REQUIRED_NOT_DERIVED"),
        ("POS2560_2_cross_term_bound", "A.nabla Gamma and other mixings obey |cross| <= eta E_positive with eta<1", "prevents tachyon/ghost hair from A-Gamma coupling", "REQUIRED_NOT_DERIVED"),
        ("POS2560_3_vacuum_normalization", "L_Gamma(Gamma_0)=0 and dL_Gamma/dGamma|Gamma_0=0 or fixed Lambda subtraction is parent-signed", "removes vacuum energy stress", "REQUIRED_NOT_DERIVED"),
        ("POS2560_4_boundary_condition", "u=0, finite energy plus asymptotic vacuum, or no-flux boundary conditions select the trivial exterior mode", "boundary no-hair", "REQUIRED_NOT_DERIVED"),
        ("POS2560_5_no_topological_hair", "Omega carries no unsourced topological GK charge or harmonic mode", "excludes q_loc=0 but stressful harmonic sectors", "REQUIRED_NOT_DERIVED"),
        ("POS2560_6_tau_projector_silence", "tau/P_loc are fixed, pure gauge, or parent-silent in the local exterior", "prevents selector/clock stress from surviving", "REQUIRED_NOT_DERIVED"),
        ("POS2560_7_parent_sign", "all positivity/sign choices come from parent action, not local test fitting", "anti-circularity", "REQUIRED_NOT_DERIVED"),
    ]
    return [
        {**base_row(), "positivity_id": item, "clause": clause, "why_needed": why, "status": status}
        for item, clause, why, status in rows
    ]


def parent_coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        ("COEF2560_0_c_A", "c_A", "coefficient of ||nabla A||^2 in L_K", "must be positive for gradient coercivity", "MISSING_PARENT_VALUE"),
        ("COEF2560_1_c_m", "c_m", "mass/gap coefficient for A modes", "positive gap suppresses homogeneous vector hair", "MISSING_PARENT_VALUE"),
        ("COEF2560_2_c_G", "c_G", "coefficient of ||nabla Gamma||^2 or effective Gamma gradient term", "positive gradient cost for scalar memory/hair", "MISSING_PARENT_VALUE"),
        ("COEF2560_3_c_g", "c_g", "curvature of L_Gamma at Gamma_0", "positive potential minimum prevents tachyonic Gamma hair", "MISSING_PARENT_VALUE"),
        ("COEF2560_4_eta_cross", "eta", "relative A-Gamma cross-term strength", "must satisfy eta<1 after Cauchy/Young bound", "MISSING_PARENT_BOUND"),
        ("COEF2560_5_Lambda_sub", "Lambda_GK", "vacuum value L_Gamma(Gamma_0) or subtraction constant", "must be zero or fixed independent cosmological term", "MISSING_PARENT_NORMALISATION"),
        ("COEF2560_6_boundary_coeff", "C_boundary", "boundary/no-flux coefficient for exterior hair", "needed for no-hair or residual stress bound", "MISSING_BOUNDARY_CONTRACT"),
    ]
    return [
        {**base_row(), "coefficient_id": item, "symbol": symbol, "meaning": meaning, "required_role": role, "status": status}
        for item, symbol, meaning, role, status in rows
    ]


def nohair_proof_rows() -> list[dict[str, Any]]:
    rows = [
        ("NH2560_0_stationary_exterior", "Use 2558/2559 stationary exterior: J_M=0, q_loc=0, F1=0.", "source residual silence", "CONDITIONAL_INPUT"),
        ("NH2560_1_Euler_system", "Use ACT2554_A Euler equations for A and Gamma in exterior.", "VAR2555_2 and VAR2555_4", "CONDITIONAL_INPUT"),
        ("NH2560_2_energy_identity", "Multiply Euler system by u and integrate by parts to get E_GK[u]=boundary_flux+cross/topological terms.", "standard elliptic/no-hair method", "PASS_AS_METHOD"),
        ("NH2560_3_boundary_zero", "If boundary flux and topological terms vanish, E_GK[u]=0.", "POS2560_4 and POS2560_5", "CONDITIONAL"),
        ("NH2560_4_coercive_zero", "If E_GK is coercive positive, E_GK[u]=0 implies u=0.", "POS2560_1 and POS2560_2", "CONDITIONAL"),
        ("NH2560_5_stress_zero", "If u=0 and vacuum energy is normalized, T_GK^{mu nu}=0 or fixed Lambda.", "POS2560_3 and POS2560_6", "CONDITIONAL"),
        ("NH2560_6_current_status", "Current corpus lacks explicit L_K/L_Gamma signs, cross-term bound, parent scale and boundary no-hair proof.", "source audit", "NOT_PROMOTED"),
        ("NH2560_7_theorem_status", "No-hair is a viable theorem shape, not a proven theorem.", "all REQUIRED_NOT_DERIVED clauses remain unsigned", "CONTRACT_ONLY"),
    ]
    return [
        {**base_row(), "proof_id": item, "proof_step": step, "basis": basis, "status": status}
        for item, step, basis, status in rows
    ]


def failure_mode_rows() -> list[dict[str, Any]]:
    rows = [
        ("FAIL2560_0_negative_mode", "L_K or L_Gamma has wrong sign/ghost/tachyon", "stationary exterior hair grows or carries stress", "requires operator sign audit"),
        ("FAIL2560_1_cross_term_too_large", "A.nabla Gamma cross term overwhelms positive terms", "coercivity fails", "requires eta<1 bound or field redefinition"),
        ("FAIL2560_2_vacuum_energy", "L_Gamma(Gamma_0) not zero or fixed", "local cosmological/stress offset remains", "requires parent vacuum normalisation"),
        ("FAIL2560_3_boundary_hair", "boundary data source stationary GK modes", "external T_GK nonzero despite J_M=0", "requires no-hair boundary condition or bound"),
        ("FAIL2560_4_topological_hair", "harmonic/topological sector survives q_loc=0", "stressful but source-free local mode", "requires topology ledger"),
        ("FAIL2560_5_tau_projector_stress", "clock/projector variation carries stress", "metric differs from GR even with GK field vacuum", "requires tau/P stress silence"),
    ]
    return [
        {**base_row(), "failure_id": item, "failure_mode": mode, "effect": effect, "required_fix": fix}
        for item, mode, effect, fix in rows
    ]


def stress_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND2560_0_if_nohair", "epsilon_GK=0 if NH2560_0-5 close", "exact stealth/no-hair route", "CONDITIONAL_ROUTE"),
        ("BND2560_1_energy_bound", "E_GK[u] <= C_B boundary_flux + C_S source_tail + C_X negative_mode_defect + C_T tau_projector_defect", "if no exact no-hair, residual bound route", "BOUND_FORM_ONLY"),
        ("BND2560_2_stress_bound", "||T_GK+T_tau/P+T_boundary|| <= C_E E_GK[u] + C_L |L_Gamma(Gamma_0)|", "stress from energy density", "BOUND_FORM_ONLY"),
        ("BND2560_3_metric_bound", "||delta g_PPN|| <= C_metric ||T_GK+T_tau/P+T_boundary||", "local linearized metric response", "BOUND_FORM_ONLY"),
        ("BND2560_4_empirical_fallback", "compare epsilon_GK against R10/PPN/clock/orbital thresholds if exact no-hair fails", "future local tests", "FALLBACK_NOT_GR_PROOF"),
        ("BND2560_5_current_status", "bound cannot be numerical until c_A,c_m,c_G,c_g,eta and boundary constants are parent-sourced", "coefficient ledger", "MISSING_PARENT_COEFFICIENTS"),
    ]
    return [
        {**base_row(), "bound_id": item, "bound_or_clause": bound, "basis": basis, "status": status}
        for item, bound, basis, status in rows
    ]


def metric_implication_rows() -> list[dict[str, Any]]:
    rows = [
        ("MET2560_0_if_nohair", "If no-hair proof closes, stationary exterior metric equation reduces to GR plus fixed Lambda.", "T_GK=0 and other retained stresses silent", "CONDITIONAL_ROUTE"),
        ("MET2560_1_current", "Current corpus does not close no-hair/positivity.", "missing POS2560 clauses and coefficients", "BLOCKED_CURRENT_CLAIM"),
        ("MET2560_2_bound_route", "If no-hair fails but stress bound is finite, local tests become residual-bound problem.", "BND2560 ledger", "FALLBACK_ROUTE"),
        ("MET2560_3_Newton_status", "Newton source still needs ell_J/source normalisation and interior correction bounds.", "Hilbert source bridge still nonnumeric", "BLOCKED_SOURCE_NORMALISATION"),
        ("MET2560_4_needed_next", "Need explicit quadratic L_K/L_Gamma ansatz and sign/cross-term audit.", "to decide no-hair vs bound", "SELECT_NEXT"),
    ]
    return [
        {**base_row(), "metric_id": item, "implication": implication, "basis": basis, "status": status}
        for item, implication, basis, status in rows
    ]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2560_0_nohair_method", "Is there a valid no-hair proof method?", "YES_CONDITIONAL", "energy identity plus coercivity would prove trivial exterior GK fields", "contract only"),
        ("PV2560_1_current_nohair", "Does current corpus prove no-hair?", "NO", "positivity/cross-term/boundary/topology/tau clauses are unsigned", "blocked"),
        ("PV2560_2_stress_bound", "Is there a fallback if no-hair fails?", "YES_FORMAL_BOUND", "stress-to-metric residual bound written", "nonclaim fallback"),
        ("PV2560_3_GR_status", "Does local GR/PPN pass?", "NO", "no-hair and numeric residual bounds are not closed", "no claim"),
        ("PV2560_4_overall", "Overall 2560 verdict", "NOHAIR_CONTRACT_WRITTEN_NOT_PROVED_BOUND_FALLBACK_READY", "next target is explicit quadratic operator/sign audit", "continue"),
    ]
    return [
        {**base_row(), "verdict_id": item, "question": question, "result": result, "evidence": evidence, "effect": effect}
        for item, question, result, evidence, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2560_0_nohair_contract", "No-hair positivity proof route is written.", "PASS_AS_CONTRACT", "energy identity/coercivity steps explicit", "true", "false"),
        ("GATE2560_1_nohair_proved", "Current corpus proves no-hair.", "BLOCKED", "positivity and boundary clauses unsigned", "false", "false"),
        ("GATE2560_2_stress_bound", "Stress residual fallback is written.", "PASS_AS_FALLBACK", "bound forms and missing coefficients listed", "true", "false"),
        ("GATE2560_3_local_GR_PPN", "Local GR/PPN branch passes.", "BLOCKED", "no-hair not proved and bound coefficients missing", "false", "false"),
        ("GATE2560_4_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [
        {**base_row(), "gate_id": item, "claim": claim, "gate_status": status, "reason": reason, "gate_pass": gate_pass, "claim_promoted": promoted}
        for item, claim, status, reason, gate_pass, promoted in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2560_0_nohair_not_proved", "Do not promote the no-hair theorem.", "key positivity, coefficient and boundary clauses are not parent-signed", "local GR remains blocked"),
        ("DEC2560_1_best_next", "Attack explicit quadratic GK operator signs next.", "without L_K/L_Gamma signs we cannot choose no-hair or bound route", "2561 selected"),
        ("DEC2560_2_keep_bound", "Keep stress-bound fallback ready.", "if no-hair fails, empirical local tests can still discipline residuals", "future bound runner path preserved"),
        ("DEC2560_3_no_claim", "Do not claim local GR/PPN.", "this checkpoint is a theorem-shape and bound-contract audit", "private nonclaim status retained"),
    ]
    return [
        {**base_row(), "decision_id": item, "decision": decision, "reason": reason, "effect": effect}
        for item, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2560_0_selected",
            "selection_status": "selected",
            "target_file": "2561-Y5-R2FR-explicit-GK-quadratic-operator-sign-audit.md",
            "target_script": "scripts/Y5_R2FR_explicit_GK_quadratic_operator_sign_audit_2561.py",
            "task": "write the minimal quadratic L_K/L_Gamma operator, audit signs/cross-term coercivity, and decide whether no-hair is plausible or the branch must go stress-bound only",
            "acceptance_target": "operator ansatz, dimension/sign table, cross-term bound, ghost/tachyon checks, no-hair eligibility, parent coefficient ledger, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    copy_sources = {
        "nohair_contract": OUTPUTS["nohair_proof_attempt"],
        "stress_bound_fallback": OUTPUTS["stress_bound_fallback"],
        "operator_sign_queue": OUTPUTS["parent_coefficient_ledger"],
    }
    rows = []
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        shutil.copyfile(source, target)
        rows.append(
            {
                **base_row(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": bool_text(source.exists()),
                "target_exists": bool_text(target.exists()),
            }
        )
    return rows


def csv_row_count(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    with path.open(newline="", encoding="utf-8") as handle:
        return max(sum(1 for _ in csv.DictReader(handle)), 0)


def formalization_status_detail() -> tuple[bool, str]:
    touched_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC, Path(__file__).resolve()]
    outside_formalization = [path for path in touched_paths if not is_relative_to(path, FORMALIZATION)]
    return len(outside_formalization) == len(touched_paths), f"declared_2560_paths_outside_formalization={len(outside_formalization)}/{len(touched_paths)}"


def validation_rows(
    sources: list[dict[str, Any]],
    positivity: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    nohair: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail})

    add("VAL2560_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present")
    add("VAL2560_01_positivity_clauses", any(row["positivity_id"] == "POS2560_1_quadratic_form" for row in positivity), "positivity/no-hair clauses explicit")
    add("VAL2560_02_parent_coefficients_missing", any(row["coefficient_id"] == "COEF2560_0_c_A" and row["status"] == "MISSING_PARENT_VALUE" for row in coefficients), "parent coefficient ledger records missing signs")
    add("VAL2560_03_nohair_method", any(row["proof_id"] == "NH2560_2_energy_identity" and row["status"] == "PASS_AS_METHOD" for row in nohair), "energy/no-hair method recorded")
    add("VAL2560_04_current_not_promoted", any(row["proof_id"] == "NH2560_6_current_status" and row["status"] == "NOT_PROMOTED" for row in nohair), "current no-hair theorem not promoted")
    add("VAL2560_05_failure_modes", len(failures) >= 6 and any(row["failure_id"] == "FAIL2560_0_negative_mode" for row in failures), "failure modes listed")
    add("VAL2560_06_bound_fallback", any(row["bound_id"] == "BND2560_1_energy_bound" and row["status"] == "BOUND_FORM_ONLY" for row in bounds), "stress-bound fallback written")
    add("VAL2560_07_metric_status", any(row["metric_id"] == "MET2560_1_current" and row["status"] == "BLOCKED_CURRENT_CLAIM" for row in metrics), "local GR/metric claim blocked")
    add("VAL2560_08_overall_verdict", any(row["verdict_id"] == "PV2560_4_overall" and row["result"] == "NOHAIR_CONTRACT_WRITTEN_NOT_PROVED_BOUND_FALLBACK_READY" for row in verdicts), "overall verdict preserves nonclaim status")
    add("VAL2560_09_claim_gates_safe", all(row["claim_promoted"] == "false" for row in gates), "no claim gate promotes local-GR/Newton claims")
    add("VAL2560_10_next_target_written", any(row["route_id"] == "NEXT2560_0_selected" and row["selection_status"] == "selected" for row in next_rows), "2561 operator sign audit selected")
    add("VAL2560_11_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_copies), "nonclaim branch copies exist")

    output_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]
    add("VAL2560_12_all_outputs_inside_post_checkpoint", all(is_relative_to(path, ROOT) for path in output_paths), "all 2560 outputs stay inside post-checkpoint-work")
    formalization_ok, formalization_detail = formalization_status_detail()
    add("VAL2560_13_formalization_workbench_not_targeted", formalization_ok, "declared 2560 outputs do not target formalization-workbench", formalization_detail)

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        add(f"VAL2560_OUTPUT_{key}", path.exists() and csv_row_count(path) > 0, f"{key} output exists and has rows", str(path))

    for copy_id, path in COPY_TARGETS.items():
        add(f"VAL2560_COPY_{copy_id}", path.exists() and csv_row_count(path) > 0, f"{copy_id} copy exists and has rows", str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2560_OVERALL", overall, "2560 writes GK no-hair positivity contract, refuses promotion, and prepares stress-bound fallback")
    return rows


def escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(escape_md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    positivity: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    nohair: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2560 Y5 R2FR GK Vacuum No-hair Positivity Or Stress Bound",
                "**Status:** no-hair route formalized, not proved. The right theorem shape is now clear: if the stationary exterior GK quadratic energy is coercive, cross-terms are controlled, boundary/topological hair is absent, clock/projector stress is silent, and vacuum energy is parent-normalized, then the only finite-energy exterior solution is the trivial GK vacuum and `T_GK` is locally silent.",
                "**Reality check:** current MTS still does not supply the explicit `L_K/L_Gamma` signs, parent coefficients, cross-term bound, no-hair boundary theorem, topology ledger, or parent vacuum normalization. So this checkpoint improves the derivation path but does not pass GR/PPN. If no-hair fails, the fallback is a stress-bound-to-PPN residual route.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
                "## Positivity Clauses",
                markdown_table(positivity, ["positivity_id", "clause", "why_needed", "status"]),
                "## Parent Coefficient Ledger",
                markdown_table(coefficients, ["coefficient_id", "symbol", "meaning", "required_role", "status"]),
                "## No-hair Proof Attempt",
                markdown_table(nohair, ["proof_id", "proof_step", "basis", "status"]),
                "## No-hair Failure Modes",
                markdown_table(failures, ["failure_id", "failure_mode", "effect", "required_fix"]),
                "## Stress Bound Fallback",
                markdown_table(bounds, ["bound_id", "bound_or_clause", "basis", "status"]),
                "## Metric Implications",
                markdown_table(metrics, ["metric_id", "implication", "basis", "status"]),
                "## Promotion Verdict",
                markdown_table(verdicts, ["verdict_id", "question", "result", "evidence", "effect"]),
                "## Claim Gates",
                markdown_table(gates, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_promoted"]),
                "## Decision Ledger",
                markdown_table(decisions, ["decision_id", "decision", "reason", "effect"]),
                "## Next Target",
                markdown_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
                "## Branch Copies",
                markdown_table(branch_copies, ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
                "## Validation",
                markdown_table(validations, ["check_id", "status", "notes", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    positivity = positivity_clause_rows()
    coefficients = parent_coefficient_rows()
    nohair = nohair_proof_rows()
    failures = failure_mode_rows()
    bounds = stress_bound_rows()
    metrics = metric_implication_rows()
    verdicts = promotion_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["positivity_clauses"], positivity)
    write_csv(OUTPUTS["parent_coefficient_ledger"], coefficients)
    write_csv(OUTPUTS["nohair_proof_attempt"], nohair)
    write_csv(OUTPUTS["failure_modes"], failures)
    write_csv(OUTPUTS["stress_bound_fallback"], bounds)
    write_csv(OUTPUTS["metric_implications"], metrics)
    write_csv(OUTPUTS["promotion_verdict"], verdicts)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_copies = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validations = validation_rows(sources, positivity, coefficients, nohair, failures, bounds, metrics, verdicts, gates, decisions, next_rows, branch_copies)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, positivity, coefficients, nohair, failures, bounds, metrics, verdicts, gates, decisions, next_rows, branch_copies, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
