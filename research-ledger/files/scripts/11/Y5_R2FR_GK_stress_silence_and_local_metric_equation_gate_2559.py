from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2559"
BRANCH_ID = "MTS_R2FR_GK_STRESS_SILENCE_AND_LOCAL_METRIC_EQUATION_GATE_2559"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2559-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2559_SOURCE_REGISTER.csv",
    "stress_exposure": OUT / "P8_Y5_NO_SHADOW_2559_STRESS_EXPOSURE.csv",
    "stealth_conditions": OUT / "P8_Y5_NO_SHADOW_2559_STEALTH_BRANCH_CONDITIONS.csv",
    "metric_gate": OUT / "P8_Y5_NO_SHADOW_2559_LOCAL_METRIC_EQUATION_GATE.csv",
    "ppn_residual": OUT / "P8_Y5_NO_SHADOW_2559_PPN_RESIDUAL_LEDGER.csv",
    "stress_bound": OUT / "P8_Y5_NO_SHADOW_2559_STRESS_BOUND_FORM.csv",
    "promotion_verdict": OUT / "P8_Y5_NO_SHADOW_2559_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2559_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2559_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2559_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2559_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2559_VALIDATION.csv",
}

COPY_TARGETS = {
    "stress_silence_contract": LOCAL_BOUNDS / "GK_stress_silence_contract_2559_NONCLAIM.csv",
    "ppn_residual_ledger": LOCAL_BOUNDS / "GK_PPN_residual_ledger_2559_NONCLAIM.csv",
    "stealth_branch_queue": QUEUE / "JR2559_GK_STEALTH_BRANCH_REQUIREMENTS_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2559_00_2558_doc",
        "source_path": ROOT / "2558-Y5-R2FR-parent-clock-exchange-current-or-stationary-source-theorem.md",
        "needles": ["PRF2558_4_projected_q_zero", "SCP2558_1_GK_stress", "NEXT2558_0_selected", "VAL2558_OVERALL"],
        "role": "active handoff proving conditional q_loc/F1 zero but retaining stress gate",
    },
    {
        "source_id": "SRC2559_01_2558_scope",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2558_SCOPE_LIMITS.csv",
        "needles": ["SCP2558_1_GK_stress", "q_loc=0 does not imply T_GK", "BLOCKED"],
        "role": "machine-readable stress blocker after stationary theorem",
    },
    {
        "source_id": "SRC2559_02_2558_proof",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2558_STATIONARY_PROOF_STEPS.csv",
        "needles": ["PRF2558_4_projected_q_zero", "PRF2558_5_F1_zero", "PASS_CONDITIONAL"],
        "role": "stationary exterior q_loc/F1 proof contract",
    },
    {
        "source_id": "SRC2559_03_2555_stress",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_STRESS_TENSOR_EXPOSURE.csv",
        "needles": ["STR2555_0_metric_variation_exists", "STR2555_1_vacuum_stealth_condition", "STR2555_4_GR_limit_gate"],
        "role": "GK stress tensor exposure and no q_loc-to-stress shortcut",
    },
    {
        "source_id": "SRC2559_04_2555_variation",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_VARIATION_AUDIT.csv",
        "needles": ["VAR2555_0_action_assumed", "VAR2555_2_delta_A_bulk", "VAR2555_4_delta_Gamma_bulk"],
        "role": "candidate action variation terms that can carry stress",
    },
    {
        "source_id": "SRC2559_05_2554_candidate_action",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2554_A_vertical_generator_current_law", "L_K(g,tau,nabla A)", "L_Gamma"],
        "role": "candidate GK action whose metric stress must be silenced",
    },
    {
        "source_id": "SRC2559_06_2469_precedent",
        "source_path": ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
        "needles": ["STR2469_6_key_lesson", "MET2469_3_current_corpus", "VAL2469_OVERALL"],
        "role": "earlier stress gate precedent, re-run against 2558 chain",
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


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def bool_text(value: bool) -> str:
    return "true" if value else "false"


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


def stress_exposure_rows() -> list[dict[str, Any]]:
    rows = [
        ("STR2559_0_definition", "T_GK^{mu nu}=-(2/sqrt(-g))delta S_GK/delta g_mu_nu", "metric variation of ACT2554_A", "stress object exists symbolically", "PASS_AS_FORMAL_DEFINITION"),
        ("STR2559_1_LK", "T_K from L_K(g,tau,nabla A)", "explicit metric contractions and covariant derivative dependence", "generically nonzero if nabla A or A modes persist", "EXPOSED_NONZERO_RISK"),
        ("STR2559_2_AGamma", "T_{A Gamma} from A_nu nabla^nu Gamma_eff", "metric raises derivative/index and sqrt(-g)", "generically nonzero if A or grad Gamma persists", "EXPOSED_NONZERO_RISK"),
        ("STR2559_3_AJ", "T_{AJ} from -A_nu J_M^nu", "source coupling and metric dependence of J_M", "zero in exterior only if J_M=0 and A does not enter hidden source readout", "CONDITIONAL_ZERO"),
        ("STR2559_4_LGamma", "T_Gamma from L_Gamma(Gamma_eff,g,tau)", "potential/gap/vacuum energy term", "acts like local cosmological/stress term unless vacuum value and derivative are fixed", "EXPOSED_VACUUM_ENERGY_RISK"),
        ("STR2559_5_tau_projector", "T_tau/P from tau and P_loc ownership", "clock/projector can carry metric dependence", "local GR needs those stresses fixed, zero, or absorbed consistently", "EXPOSED_SELECTOR_CLOCK_RISK"),
        ("STR2559_6_boundary_improvement", "boundary/improvement stress from integrations by parts", "well-posed variational principle", "can leak into local metric unless boundary terms fixed or bounded", "MISSING_BOUNDARY_STRESS"),
        ("STR2559_7_key_lesson", "q_loc=0 constrains Euler residual, not all field amplitudes", "homogeneous GK modes can carry stress", "stress silence needs vacuum/stealth/no-hair branch, not just current-law silence", "PASS_RED_TEAM"),
    ]
    return [
        {**base_row(), "stress_id": item, "stress_component": component, "basis": basis, "local_effect": effect, "status": status}
        for item, component, basis, effect, status in rows
    ]


def stealth_condition_rows() -> list[dict[str, Any]]:
    rows = [
        ("STL2559_0_stationary_source", "stationary exterior has J_M=0, q_loc=0 and F1=0", "2558 conditional theorem", "removes source current forcing", "CONDITIONAL_INPUT"),
        ("STL2559_1_positive_vacuum_branch", "L_K and L_Gamma have a positive/elliptic vacuum branch", "needed for no-hair or energy minimisation", "can force exterior modes to trivial vacuum", "REQUIRED_NOT_DERIVED"),
        ("STL2559_2_field_vacuum", "A_nu=0 or pure gauge, nabla_mu A_nu=0, Gamma_eff=Gamma_0 with nabla Gamma=0", "strong stealth/vacuum branch", "makes L_K and A.Gamma stress vanish", "REQUIRED_NOT_DERIVED"),
        ("STL2559_3_potential_minimum", "dL_Gamma/dGamma|Gamma_0=0 and L_Gamma(Gamma_0)=0 or absorbed into fixed Lambda", "avoid vacuum energy/local cosmological stress", "needed for metric silence", "REQUIRED_NOT_DERIVED"),
        ("STL2559_4_boundary_no_hair", "boundary data eliminate homogeneous GK hair in the local exterior", "finite-energy/no incoming hair condition", "prevents hidden PPN stress", "REQUIRED_NOT_DERIVED"),
        ("STL2559_5_tau_projector_silence", "tau/P_loc stresses are fixed background, pure gauge, or zero in the local collar", "clock/projector metric variation", "prevents source-free local metric deviations", "REQUIRED_NOT_DERIVED"),
        ("STL2559_6_conditional_result", "if STL2559_0-5 hold, T_GK^{mu nu}=0 or pure fixed Lambda in local exterior", "conditional stress-silence theorem", "would let metric equation reduce to GR locally", "CONDITIONAL_CONTRACT_ONLY"),
        ("STL2559_7_current_status", "current corpus has not derived STL2559_1-5 from a parent action", "source audit", "stress-silence theorem not promoted", "BLOCKED_CURRENT_CLAIM"),
    ]
    return [
        {**base_row(), "stealth_id": item, "condition": condition, "basis": basis, "effect": effect, "status": status}
        for item, condition, basis, effect, status in rows
    ]


def metric_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("MET2559_0_parent_metric_equation", "E_GR^{mu nu}=8piG T_matter^{mu nu}+T_GK^{mu nu}+T_tau/P^{mu nu}+T_boundary^{mu nu}", "generic local metric equation", "extra sector stress appears unless silenced", "FORMAL_GATE"),
        ("MET2559_1_stationary_exterior", "outside matter, T_matter=0 and q_loc=0", "2558 theorem", "metric still differs from GR if T_GK or projector/tau stress survives", "BLOCKED_UNTIL_STRESS_SILENCE"),
        ("MET2559_2_stealth_reduction", "if T_GK=0 and retained sector stresses vanish or reduce to fixed Lambda, local metric equation reduces to vacuum GR", "stealth branch", "conditional GR exterior route", "CONDITIONAL_CONTRACT_ONLY"),
        ("MET2559_3_current_corpus", "current corpus does not prove T_GK=0", "missing explicit L_K/L_Gamma/gap/boundary/no-hair theorem", "local GR/PPN not promoted", "BLOCKED_CURRENT_CLAIM"),
        ("MET2559_4_Newton_source_interior", "inside matter, metric source should be Hilbert T_matter plus controlled corrections", "GR/Newton source requirement", "requires ell_J/source normalisation and stress correction bounds", "BLOCKED_SOURCE_NORMALISATION"),
        ("MET2559_5_next_mathematical_target", "derive energy positivity/no-hair for GK exterior modes or build a stress-bound fallback", "needed to turn q_loc=0 into T_GK=0 or bounded", "next step must attack vacuum branch", "SELECT_NEXT"),
    ]
    return [
        {**base_row(), "metric_id": item, "gate": gate, "basis": basis, "result": result, "status": status}
        for item, gate, basis, result, status in rows
    ]


def ppn_residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("PPN2559_0_residual_source", "delta G^{mu nu}=T_GK^{mu nu}+T_tau/P^{mu nu}+T_boundary^{mu nu}+stress corrections", "local metric residual source", "PPN deviations source", "FORMAL_LEDGER"),
        ("PPN2559_1_q_zero_not_enough", "q_loc=0 removes current residual but not homogeneous stress", "stationary q theorem", "PPN residual can remain", "BLOCKED"),
        ("PPN2559_2_hair_bound", "||delta g_PPN|| <= C_metric ||T_GK+T_tau/P+T_boundary||", "linearized metric response", "requires stress norm and Green function scale", "BOUND_FORM_ONLY"),
        ("PPN2559_3_stealth_pass", "if stealth branch gives T_GK=0 and other sector stresses zero/bounded below arena limits, PPN residual passes conditionally", "conditional exterior branch", "not current claim", "CONDITIONAL_ONLY"),
        ("PPN2559_4_empirical_needed_later", "R10/PPN/clocks/orbital tests need numeric stress residual coefficients", "future empirical gate", "not ready until L_K/L_Gamma fixed", "DEFER_NUMERIC_TEST"),
        ("PPN2559_5_baseline_comparison", "when tested, GR baseline and MTS residual pipeline must be checked side by side", "pipeline discipline", "prevents false failure from code/baseline artefacts", "FUTURE_TEST_GUARDRAIL"),
    ]
    return [
        {**base_row(), "ppn_id": item, "ledger": ledger, "basis": basis, "effect": effect, "status": status}
        for item, ledger, basis, effect, status in rows
    ]


def stress_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND2559_0_norm_contract", "epsilon_GK(R)=sup_{collar R} ||T_GK+T_tau/P+T_boundary||/||T_matter||_source", "dimensionless local stress residual", "defines the local non-GR stress amplitude to bound", "BOUND_FORM_ONLY"),
        ("BND2559_1_metric_response", "||delta g||_PPN <= C_R epsilon_GK", "linearized local Green response", "requires arena-specific C_R", "BOUND_FORM_ONLY"),
        ("BND2559_2_exact_branch", "epsilon_GK=0 if stealth/no-hair branch is proven", "vacuum uniqueness", "would close stress gate conditionally", "CONDITIONAL_ONLY"),
        ("BND2559_3_empirical_branch", "epsilon_GK must be below R10/PPN/clock/orbital thresholds if exact branch fails", "fallback evidence path", "future numeric local tests", "FALLBACK_NOT_GR_PROOF"),
        ("BND2559_4_current_status", "no numeric epsilon_GK exists because L_K/L_Gamma coefficients are not fixed", "source audit", "cannot run local metric claims yet", "MISSING_PARENT_COEFFICIENTS"),
    ]
    return [
        {**base_row(), "bound_id": item, "bound_or_clause": bound, "basis": basis, "effect": effect, "status": status}
        for item, bound, basis, effect, status in rows
    ]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2559_0_stress_exposed", "Is the GK stress gate now explicit?", "YES", "stress components and risks listed", "progress"),
        ("PV2559_1_q_zero_to_stress_zero", "Does q_loc=0 imply T_GK=0?", "NO", "homogeneous GK modes and vacuum energy can carry stress", "do not overclaim"),
        ("PV2559_2_conditional_stealth", "Is there a clean conditional stress-silence route?", "YES_CONDITIONAL", "trivial/gapped vacuum branch plus no-hair boundary would silence T_GK", "contract only"),
        ("PV2559_3_current_local_GR", "Does current MTS pass local GR/PPN?", "NO", "stealth/no-hair/gap and explicit stress tensor not derived", "blocked"),
        ("PV2559_4_overall", "Overall 2559 verdict", "STRESS_GATE_SHARPENED_STEALTH_CONTRACT_WRITTEN_NOT_PROMOTED", "next target is GK vacuum/no-hair positivity or stress bound", "continue derivation"),
    ]
    return [
        {**base_row(), "verdict_id": item, "question": question, "result": result, "evidence": evidence, "effect": effect}
        for item, question, result, evidence, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2559_0_stress_exposure", "GK stress tensor exposure is written.", "PASS_AS_AUDIT", "symbolic stress components identified", "true", "false"),
        ("GATE2559_1_conditional_stealth", "A conditional stress-silence branch is stated.", "PASS_AS_CONTRACT", "requires vacuum/gap/no-hair hypotheses", "true", "false"),
        ("GATE2559_2_current_stress_silence", "Current corpus proves T_GK=0 in local exterior.", "BLOCKED", "explicit stress/no-hair/gap branch missing", "false", "false"),
        ("GATE2559_3_PPN_GR", "PPN/local GR branch passes.", "BLOCKED", "stress residual not yet zero or bounded numerically", "false", "false"),
        ("GATE2559_4_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [
        {**base_row(), "gate_id": item, "claim": claim, "gate_status": status, "reason": reason, "gate_pass": gate_pass, "claim_promoted": promoted}
        for item, claim, status, reason, gate_pass, promoted in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2559_0_no_q_to_stress_shortcut", "Reject q_loc=0 => T_GK=0 as a shortcut.", "Euler residual silence is weaker than stress silence", "keeps local GR route honest"),
        ("DEC2559_1_keep_stealth_contract", "Keep the stealth/no-hair branch as the right next contract.", "it is the least-scrutiny path to local GR: source exterior plus vacuum uniqueness", "next work targets no-hair/positivity"),
        ("DEC2559_2_build_bound_fallback", "If no-hair cannot be proved, build an explicit stress-bound fallback.", "PPN/clocks/orbits need residual coefficients", "prepares empirical gate without claiming GR"),
        ("DEC2559_3_no_claim", "Do not claim local GR/PPN.", "current corpus lacks explicit stress tensor and no-hair proof", "private nonclaim status retained"),
    ]
    return [
        {**base_row(), "decision_id": item, "decision": decision, "reason": reason, "effect": effect}
        for item, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2559_0_selected",
            "selection_status": "selected",
            "target_file": "2560-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
            "target_script": "scripts/Y5_R2FR_GK_vacuum_no_hair_positivity_or_stress_bound_2560.py",
            "task": "derive or reject a GK vacuum/no-hair positivity theorem showing stationary exterior q_loc=0 selects trivial stress, or else build the stress-bound fallback",
            "acceptance_target": "candidate L_K/L_Gamma positivity clauses, boundary no-hair proof attempt, stress residual bound form, parent-coefficient ledger, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    copy_sources = {
        "stress_silence_contract": OUTPUTS["stealth_conditions"],
        "ppn_residual_ledger": OUTPUTS["ppn_residual"],
        "stealth_branch_queue": OUTPUTS["stealth_conditions"],
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
    return len(outside_formalization) == len(touched_paths), f"declared_2559_paths_outside_formalization={len(outside_formalization)}/{len(touched_paths)}"


def validation_rows(
    sources: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    stealth: list[dict[str, Any]],
    metric: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail})

    add("VAL2559_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present")
    add("VAL2559_01_stress_exposed", any(row["stress_id"] == "STR2559_0_definition" and row["status"] == "PASS_AS_FORMAL_DEFINITION" for row in stress), "GK stress definition exposed")
    add("VAL2559_02_q_not_stress", any(row["stress_id"] == "STR2559_7_key_lesson" and row["status"] == "PASS_RED_TEAM" for row in stress), "q_loc zero not treated as stress zero")
    add("VAL2559_03_stealth_conditions", any(row["stealth_id"] == "STL2559_6_conditional_result" and row["status"] == "CONDITIONAL_CONTRACT_ONLY" for row in stealth), "conditional stress-silence branch written")
    add("VAL2559_04_current_stress_blocked", any(row["stealth_id"] == "STL2559_7_current_status" and row["status"] == "BLOCKED_CURRENT_CLAIM" for row in stealth), "current corpus does not prove stress silence")
    add("VAL2559_05_metric_gate", any(row["metric_id"] == "MET2559_3_current_corpus" and row["status"] == "BLOCKED_CURRENT_CLAIM" for row in metric), "local metric equation remains blocked")
    add("VAL2559_06_ppn_ledger", any(row["ppn_id"] == "PPN2559_2_hair_bound" and row["status"] == "BOUND_FORM_ONLY" for row in ppn), "PPN residual bound form recorded")
    add("VAL2559_07_stress_bound_form", any(row["bound_id"] == "BND2559_0_norm_contract" and row["status"] == "BOUND_FORM_ONLY" for row in bounds), "stress residual norm contract recorded")
    add("VAL2559_08_overall_verdict", any(row["verdict_id"] == "PV2559_4_overall" and row["result"] == "STRESS_GATE_SHARPENED_STEALTH_CONTRACT_WRITTEN_NOT_PROMOTED" for row in verdicts), "overall verdict selects no-hair/positivity next")
    add("VAL2559_09_claim_gates_safe", all(row["claim_promoted"] == "false" for row in gates), "no claim gate promotes local-GR/Newton claims")
    add("VAL2559_10_next_target_written", any(row["route_id"] == "NEXT2559_0_selected" and row["selection_status"] == "selected" for row in next_rows), "2560 no-hair/positivity target selected")
    add("VAL2559_11_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_copies), "nonclaim branch copies exist")

    output_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]
    add("VAL2559_12_all_outputs_inside_post_checkpoint", all(is_relative_to(path, ROOT) for path in output_paths), "all 2559 outputs stay inside post-checkpoint-work")
    formalization_ok, formalization_detail = formalization_status_detail()
    add("VAL2559_13_formalization_workbench_not_targeted", formalization_ok, "declared 2559 outputs do not target formalization-workbench", formalization_detail)

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        add(f"VAL2559_OUTPUT_{key}", path.exists() and csv_row_count(path) > 0, f"{key} output exists and has rows", str(path))

    for copy_id, path in COPY_TARGETS.items():
        add(f"VAL2559_COPY_{copy_id}", path.exists() and csv_row_count(path) > 0, f"{copy_id} copy exists and has rows", str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2559_OVERALL", overall, "2559 exposes GK stress, writes conditional stealth/stress-bound contracts, and keeps local GR blocked pending no-hair/positivity")
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
    stress: list[dict[str, Any]],
    stealth: list[dict[str, Any]],
    metric: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
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
                "# 2559 Y5 R2FR GK Stress Silence And Local Metric Equation Gate",
                "**Status:** stress gate sharpened, not closed. The 2558 stationary source theorem gives exterior `q_loc=0` and `F1=0`, but that only silences a current residual. It does not automatically silence stress carried by `A`, `Gamma_eff`, `K_hat`, clock/projector structures, boundary terms, or vacuum energy.",
                "**Main result:** the least-scrutiny path is now clear: prove a GK stealth/no-hair branch where the local exterior selects `A=0` or pure gauge, `Gamma_eff=Gamma_0`, zero gradients, zero/fixed vacuum energy, and silent boundaries. If that branch is derived, the local metric equation can reduce to GR conditionally. If not, the fallback is an explicit stress residual bound for PPN/clocks/orbits. No local-GR or PPN pass is claimed here.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
                "## Stress Exposure",
                markdown_table(stress, ["stress_id", "stress_component", "basis", "local_effect", "status"]),
                "## Stealth Branch Conditions",
                markdown_table(stealth, ["stealth_id", "condition", "basis", "effect", "status"]),
                "## Local Metric Equation Gate",
                markdown_table(metric, ["metric_id", "gate", "basis", "result", "status"]),
                "## PPN Residual Ledger",
                markdown_table(ppn, ["ppn_id", "ledger", "basis", "effect", "status"]),
                "## Stress Bound Form",
                markdown_table(bounds, ["bound_id", "bound_or_clause", "basis", "effect", "status"]),
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
    stress = stress_exposure_rows()
    stealth = stealth_condition_rows()
    metric = metric_gate_rows()
    ppn = ppn_residual_rows()
    bounds = stress_bound_rows()
    verdicts = promotion_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["stress_exposure"], stress)
    write_csv(OUTPUTS["stealth_conditions"], stealth)
    write_csv(OUTPUTS["metric_gate"], metric)
    write_csv(OUTPUTS["ppn_residual"], ppn)
    write_csv(OUTPUTS["stress_bound"], bounds)
    write_csv(OUTPUTS["promotion_verdict"], verdicts)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_copies = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validations = validation_rows(sources, stress, stealth, metric, ppn, bounds, verdicts, gates, decisions, next_rows, branch_copies)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, stress, stealth, metric, ppn, bounds, verdicts, gates, decisions, next_rows, branch_copies, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
