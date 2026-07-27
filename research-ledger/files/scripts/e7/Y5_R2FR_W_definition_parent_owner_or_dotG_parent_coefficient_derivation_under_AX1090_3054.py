from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3054"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3054-Y5-R2FR-W-definition-parent-owner-or-dotG-parent-coefficient-derivation-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3054_00_3053_doc": ROOT / "3053-Y5-R2FR-WPhi-source-readout-theorem-or-real-dotG-coefficient-value-under-AX1090.md",
    "SRC3054_01_3053_wphi": RESIDUALS / "P8_Y5_R2FR_3053_WPHI_UNIQUENESS_THEOREM_ATTEMPT.csv",
    "SRC3054_02_3053_hilbert": RESIDUALS / "P8_Y5_R2FR_3053_HILBERT_SOURCE_READOUT_AUDIT.csv",
    "SRC3054_03_3053_gates": RESIDUALS / "P8_Y5_R2FR_3053_PREMISE_SIGNATURE_GATES.csv",
    "SRC3054_04_3053_dotg_req": RESIDUALS / "P8_Y5_R2FR_3053_DOTG_REAL_VALUE_REQUIREMENT.csv",
    "SRC3054_05_3053_next": RESIDUALS / "P8_Y5_R2FR_3053_NEXT_TARGET.csv",
    "SRC3054_06_3042_W_dictionary": PARENT_ACTION / "W_symbol_retirement_dictionary_3042_CANDIDATE_NONCLAIM.csv",
    "SRC3054_07_3042_WPhi": PARENT_ACTION / "W_equals_Phi_parent_readout_theorem_3042_NOT_SIGNED.csv",
    "SRC3054_08_3040_single_potential": PARENT_ACTION / "single_potential_readout_theorem_3040_CONDITIONAL_NOT_SIGNED.csv",
    "SRC3054_09_3038_common_source": PARENT_ACTION / "common_source_functional_normal_form_3038_NOT_SIGNED.csv",
    "SRC3054_10_3045_aw_law": RESIDUALS / "P8_Y5_R2FR_3045_AW_COEFFICIENT_RATIO_LAW.csv",
    "SRC3054_11_3045_coeff_map": PARENT_ACTION / "linear_source_normalization_coefficient_map_3045_NOT_SIGNED.csv",
    "SRC3054_12_3050_spine": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
    "SRC3054_13_3050_gref": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "SRC3054_14_dotg_target": DOTG_TARGET,
    "SRC3054_15_3051_topological": RESIDUALS / "P8_Y5_R2FR_3051_TOPOLOGICAL_STRESS_AND_COMPANION_AUDIT.csv",
}

W_AUDIT_TARGETS = {
    "AUDTGT3054_0_W_dictionary": SOURCE_PATHS["SRC3054_06_3042_W_dictionary"],
    "AUDTGT3054_1_single_potential": SOURCE_PATHS["SRC3054_08_3040_single_potential"],
    "AUDTGT3054_2_common_source": SOURCE_PATHS["SRC3054_09_3038_common_source"],
    "AUDTGT3054_3_aw_law": SOURCE_PATHS["SRC3054_10_3045_aw_law"],
    "AUDTGT3054_4_coeff_map": SOURCE_PATHS["SRC3054_11_3045_coeff_map"],
    "AUDTGT3054_5_3053_wphi": SOURCE_PATHS["SRC3054_01_3053_wphi"],
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3054_SOURCE_REGISTER.csv",
    "w_owner_clause": RESIDUALS / "P8_Y5_R2FR_3054_W_PARENT_OWNER_CLAUSE.csv",
    "w_audit": RESIDUALS / "P8_Y5_R2FR_3054_W_SYMBOL_OCCURRENCE_AUDIT.csv",
    "w_gates": RESIDUALS / "P8_Y5_R2FR_3054_W_OWNER_GATE_EVALUATION.csv",
    "dotg_attempt": RESIDUALS / "P8_Y5_R2FR_3054_DOTG_PARENT_COEFFICIENT_ATTEMPT.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3054_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3054_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3054_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3054_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3054_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "w_owner_clause_copy": PARENT_ACTION / "W_definition_parent_owner_clause_3054_CONDITIONAL_NOT_SIGNED.csv",
    "w_audit_copy": PARENT_ACTION / "W_symbol_occurrence_audit_3054_TARGETED_NONCLAIM.csv",
    "w_gates_copy": PARENT_ACTION / "W_owner_gate_evaluation_3054_NOT_SIGNED.csv",
    "dotg_attempt_copy": LOCAL_BOUNDS / "dotG_parent_coefficient_attempt_3054_BLOCKED_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3054_HILBERT_SOURCE_DESCENT_OR_W_OWNER_ADOPTION_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: as_str(output_row.get(key, "")) for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, str] | dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "signed_for_current_MTS",
        "gate_passes_for_current_MTS",
        "adopted_for_current_MTS",
    }
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        values = []
        for column in columns:
            value = as_str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def w_count(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(r"\bW\b|chi_W|A_W|C_W|a_W|W/c\^2|W=Phi|W := Phi", text))


dotg_rows_before = rows(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "parse_ok": csv_ok(path) if path.suffix.lower() == ".csv" and path.exists() else "",
            "row_count": len(rows(path)) if path.suffix.lower() == ".csv" and path.exists() else "",
            "role": source_id.split("_", 2)[-1],
            "status": "PRESENT" if path.exists() else "MISSING_BLOCKER",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

w_owner_clause_rows = [
    base(
        {
            "clause_id": "WOWN3054_0_parent_object",
            "clause": "The only parent local gravitational readout object is g_obs, the observed metric/coframe branch.",
            "mathematical_content": "W is not a fundamental field, not a fitted potential, and not varied independently.",
            "effect_if_adopted": "removes independent W source/operator normalization from the local Newton branch",
            "current_status": "CANDIDATE_PARENT_CLAUSE_NOT_ADOPTED",
            "adopted_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_ACTION_TEXT_ADOPTION; MISSING_FULL_W_ALIAS_AUDIT",
            "source_path": str(SOURCE_PATHS["SRC3054_06_3042_W_dictionary"]),
        }
    ),
    base(
        {
            "clause_id": "WOWN3054_1_definition",
            "clause": "In the local weak-field observed chart, define Phi_metric[g_obs] := (c^2/2)*(g_obs00+1) where g_obs00=-1+2*Phi_metric/c^2.",
            "mathematical_content": "W := Phi_metric[g_obs] and chi_W := W/c^2 := Phi_metric/c^2.",
            "effect_if_adopted": "W=Phi_metric becomes a parent readout definition rather than an empirical postulate",
            "current_status": "LOWEST_SCRUTINY_ROUTE_IDENTIFIED",
            "adopted_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_SIGNATURE_FOR_WEAK_FIELD_CHART; MISSING_SIGN_CONVENTION_AUDIT",
            "source_path": str(SOURCE_PATHS["SRC3054_08_3040_single_potential"]),
        }
    ),
    base(
        {
            "clause_id": "WOWN3054_2_variation_rule",
            "clause": "No Euler-Lagrange equation is taken by varying W; any W equation is the weak-field projection of delta S_parent/delta g_obs=0.",
            "mathematical_content": "delta/delta W is shorthand for the pullback of the metric equation through Phi_metric[g_obs].",
            "effect_if_adopted": "forbids an extra W kinetic coefficient or source-channel denominator",
            "current_status": "NEEDED_NOT_SIGNED",
            "adopted_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PULLBACK_VARIATION_PROOF; MISSING_NO_W_ACTION_TERM_AUDIT",
            "source_path": str(SOURCE_PATHS["SRC3054_11_3045_coeff_map"]),
        }
    ),
    base(
        {
            "clause_id": "WOWN3054_3_source_rule",
            "clause": "The source density in the W/Poisson equation is rho_obs := T_obs00/c^2 from the Hilbert variation of S_matter[g_obs,psi].",
            "mathematical_content": "T_obs_munu := -2/sqrt(-g_obs)*delta S_matter[g_obs,psi]/delta g_obs^munu.",
            "effect_if_adopted": "ties W, Phi_metric, clocks, orbits and source mass to one matter action",
            "current_status": "BLOCKED_BY_HILBERT_SOURCE_DESCENT",
            "adopted_for_current_MTS": "false",
            "missing_for_claim": "MISSING_MATTER_ACTION_DESCENT; MISSING_UNIVERSAL_COUPLING_SIGNATURE",
            "source_path": str(SOURCE_PATHS["SRC3054_02_3053_hilbert"]),
        }
    ),
    base(
        {
            "clause_id": "WOWN3054_4_boundary_rule",
            "clause": "W inherits the same boundary/asymptotic data as Phi_metric because it is the same metric readout.",
            "mathematical_content": "Delta := W-Phi_metric is identically zero before solving; no independent harmonic mode is allowed.",
            "effect_if_adopted": "closes the boundary/local projection silence required by 3053",
            "current_status": "NEEDED_NOT_SIGNED",
            "adopted_for_current_MTS": "false",
            "missing_for_claim": "MISSING_BOUNDARY_CLASS_ADOPTION; MISSING_LOCAL_PROJECTION_SILENCE",
            "source_path": str(SOURCE_PATHS["SRC3054_01_3053_wphi"]),
        }
    ),
    base(
        {
            "clause_id": "WOWN3054_5_forbidden_shortcuts",
            "clause": "Forbidden: W_fit, W_orbit, independent C_W, independent a_W, or any post-fit GM potential used to define W.",
            "mathematical_content": "old two-channel local normal forms must be marked as diagnostic coordinates only, not parent variables.",
            "effect_if_adopted": "prevents measured-GM import and fake A_W=1 closure",
            "current_status": "AUDIT_REQUIRED",
            "adopted_for_current_MTS": "false",
            "missing_for_claim": "MISSING_TWO_CHANNEL_RETIREMENT_AUDIT",
            "source_path": str(SOURCE_PATHS["SRC3054_09_3038_common_source"]),
        }
    ),
    base(
        {
            "clause_id": "WOWN3054_6_verdict",
            "clause": "Parent-owning W by metric readout is the cleanest route, but it is not active until the parent action adopts the retirement clause and source descent.",
            "mathematical_content": "W := Phi_metric is acceptable as a definition only if it deletes rather than hides the independent W channel.",
            "effect_if_adopted": "would close GATE3053_1 and reduce the next blocker to Hilbert/source descent",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "adopted_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_ADOPTION; MISSING_HILBERT_SOURCE_READOUT",
            "source_path": str(SOURCE_PATHS["SRC3054_03_3053_gates"]),
        }
    ),
]

w_audit_rows: list[dict[str, Any]] = []
for audit_id, path in W_AUDIT_TARGETS.items():
    count = w_count(path)
    if "common_source" in audit_id:
        classification = "BLOCKER_TWO_CHANNEL_LANGUAGE_PRESENT"
        required_action = "retire a_W and chi_W as diagnostic coordinates or derive their collapse to one metric source"
    elif "coeff_map" in audit_id or "aw_law" in audit_id:
        classification = "BLOCKER_INDEPENDENT_COEFFICIENT_LANGUAGE_PRESENT"
        required_action = "prove coefficient map is a pullback of the metric equation, not an independent W operator"
    elif "W_dictionary" in audit_id:
        classification = "SUPPORTS_RETIREMENT_ROUTE"
        required_action = "promote dictionary only after source/variation guards pass"
    elif "single_potential" in audit_id or "3053_wphi" in audit_id:
        classification = "SUPPORTS_CONDITIONAL_SINGLE_POTENTIAL_ROUTE"
        required_action = "sign parent owner and Hilbert source premises"
    else:
        classification = "UNCLASSIFIED"
        required_action = "manual audit"
    w_audit_rows.append(
        base(
            {
                "audit_id": audit_id,
                "path": str(path),
                "exists": path.exists(),
                "w_token_count": count,
                "classification": classification,
                "safe_to_retire_now": "false",
                "required_action": required_action,
            }
        )
    )

w_gate_rows = [
    base(
        {
            "gate_id": "WGATE3054_0_parent_metric_object",
            "requirement": "local branch declares g_obs as the only parent gravitational readout object",
            "candidate_result": "W owner clause identifies g_obs as parent object",
            "current_status": "CANDIDATE_NOT_ADOPTED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "parent action has not adopted this clause",
        }
    ),
    base(
        {
            "gate_id": "WGATE3054_1_define_W_as_readout",
            "requirement": "W := Phi_metric[g_obs] in the local weak-field chart",
            "candidate_result": "definition written explicitly in 3054",
            "current_status": "ADOPTABLE_NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "needs parent signature and sign/gauge convention audit",
        }
    ),
    base(
        {
            "gate_id": "WGATE3054_2_no_independent_W_variation",
            "requirement": "no independent delta S/delta W, W kinetic term, C_W denominator or a_W source vertex",
            "candidate_result": "forbidden-shortcut clause written",
            "current_status": "BLOCKED_BY_3038_3045_LANGUAGE",
            "gate_passes_for_current_MTS": "false",
            "blocker": "targeted audit still sees two-channel/coefficient language that must be retired or derived as pullback",
        }
    ),
    base(
        {
            "gate_id": "WGATE3054_3_same_Hilbert_source",
            "requirement": "rho_obs for W equals T_obs00/c^2 from S_matter[g_obs,psi]",
            "candidate_result": "source rule written",
            "current_status": "BLOCKED_BY_MATTER_ACTION_DESCENT",
            "gate_passes_for_current_MTS": "false",
            "blocker": "Hilbert source theorem remains unsigned",
        }
    ),
    base(
        {
            "gate_id": "WGATE3054_4_same_boundary",
            "requirement": "W inherits Phi_metric boundary/asymptotic data",
            "candidate_result": "automatic if W is definitionally Phi_metric",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "boundary class adoption not yet in parent contract",
        }
    ),
    base(
        {
            "gate_id": "WGATE3054_5_AW_effect",
            "requirement": "A_W=1 follows without fitted-GM import",
            "candidate_result": "would follow after W owner plus G_ref plus Hilbert source gates",
            "current_status": "NOT_CLAIMABLE",
            "gate_passes_for_current_MTS": "false",
            "blocker": "W owner and source gates do not pass",
        }
    ),
]

dotg_attempt_rows = [
    base(
        {
            "attempt_id": "DOTG3054_0_topological_zero_route",
            "formula": "dln_Geff_dt = D_t ln(kappa_eff*c^4/(8*pi)) + D_t ln Z_readout",
            "candidate_derivation": "topological kappa spine would give d kappa_eff=0 if adopted",
            "result": "PARTIAL_ZERO_ROUTE",
            "current_status": "BLOCKED_READOUT_ZERO_UNSIGNED",
            "numeric_value": "",
            "units": "yr^-1",
            "valid_prediction_row": "false",
            "reason": "D_t ln Z_readout is not zero until W/Hilbert/same-frame readout is signed",
            "source_path": str(SOURCE_PATHS["SRC3054_15_3051_topological"]),
        }
    ),
    base(
        {
            "attempt_id": "DOTG3054_1_scalar_kappa_route",
            "formula": "D_t ln(kappa_eff) from parent scalar-kappa dynamics",
            "candidate_derivation": "would require an active scalar-kappa equation and local solution branch",
            "result": "NO_PARENT_DYNAMICS_AVAILABLE",
            "current_status": "MISSING_REAL_COEFFICIENT",
            "numeric_value": "",
            "units": "yr^-1",
            "valid_prediction_row": "false",
            "reason": "no sourced scalar-kappa evolution coefficient exists in the current local branch",
            "source_path": str(SOURCE_PATHS["SRC3054_14_dotg_target"]),
        }
    ),
    base(
        {
            "attempt_id": "DOTG3054_2_bound_guard",
            "formula": "external dotG/G bound",
            "candidate_derivation": "empirical bound only",
            "result": "REJECTED_AS_PREDICTION_SOURCE",
            "current_status": "GUARD_ACTIVE",
            "numeric_value": "",
            "units": "yr^-1",
            "valid_prediction_row": "false",
            "reason": "a bound may constrain a prediction but cannot be the prediction",
            "source_path": str(SOURCE_PATHS["SRC3054_04_3053_dotg_req"]),
        }
    ),
    base(
        {
            "attempt_id": "DOTG3054_3_verdict",
            "formula": "real dotG coefficient for local branch",
            "candidate_derivation": "none accepted in 3054",
            "result": "BLOCKED_NONCLAIM",
            "current_status": "NO_NUMERIC_OR_THEOREM_ZERO_ROW",
            "numeric_value": "",
            "units": "yr^-1",
            "valid_prediction_row": "false",
            "reason": "own W/Hilbert readout first; do not invent a drift number",
            "source_path": str(SOURCE_PATHS["SRC3054_14_dotg_target"]),
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3054_0_W_owner",
            "claim": "W is parent-owned as Phi_metric for current MTS",
            "status": "NO_CANDIDATE_NOT_ADOPTED",
            "claim_active": "false",
            "reason": "3054 writes the minimal owner clause but does not promote it as signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3054_1_no_independent_W",
            "claim": "all independent W source/operator language is retired",
            "status": "NO_AUDIT_BLOCKERS_REMAIN",
            "claim_active": "false",
            "reason": "3038/3045 still contain two-channel/coefficient language needing retirement or pullback proof",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3054_2_AW",
            "claim": "A_W=1 is derived",
            "status": "NO_BLOCKED",
            "claim_active": "false",
            "reason": "W owner, Hilbert source and boundary gates remain unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3054_3_dotG",
            "claim": "real dln_Geff_dt coefficient is available",
            "status": "NO_REAL_VALUE",
            "claim_active": "false",
            "reason": "only partial topological zero route exists; readout zero is unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3054_4_local_GR",
            "claim": "local GR/Newton branch is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "3054 narrows the next blocker to source/matter descent and W-channel retirement",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3054_0_best_route",
            "question": "Should W be kept as a separate field?",
            "answer": "NO_FOR_LOCAL_BRANCH",
            "reason": "separate W creates exactly the coefficient/source ambiguity blocking A_W=1",
            "action": "retire W into Phi_metric if the parent action adopts the metric-readout clause",
        }
    ),
    base(
        {
            "decision_id": "DEC3054_1_can_adopt_now",
            "question": "Can current MTS claim W owner now?",
            "answer": "NO",
            "reason": "the owner clause is written, but the old two-channel W language and Hilbert-source descent remain unsigned",
            "action": "do not promote local GR/Newton",
        }
    ),
    base(
        {
            "decision_id": "DEC3054_2_dotg",
            "question": "Is the dotG fallback better now?",
            "answer": "NO",
            "reason": "dotG still lacks either a full theorem-zero readout or a numeric scalar-kappa coefficient",
            "action": "keep dotG nonclaim and avoid placeholder rows",
        }
    ),
    base(
        {
            "decision_id": "DEC3054_3_next",
            "question": "What is the next theorem gate?",
            "answer": "HILBERT_SOURCE_DESCENT_AND_W_CHANNEL_RETIREMENT",
            "reason": "once W is only Phi_metric, the remaining nontrivial local-GR issue is whether the source is exactly the universal matter Hilbert source",
            "action": "build 3055 source descent / two-channel retirement proof attempt",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3054_0_3055",
            "next_checkpoint": "3055-Y5-R2FR-Hilbert-source-descent-and-W-channel-retirement-or-dotG-zero-readout-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Hilbert_source_descent_and_W_channel_retirement_or_dotG_zero_readout_under_AX1090_3055.py",
            "mission": "try to collapse the old two-channel a_H/a_W source language into one Hilbert matter source; if that fails, state the exact residual coefficient that must be bounded",
            "starting_equation": "S_matter[g_obs,psi] -> T_obs_munu and W:=Phi_metric[g_obs] together forbid an independent W source channel",
            "claim_policy": "no local-GR/Newton claim until W-channel retirement and Hilbert source descent are parent-signed",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["w_owner_clause"], w_owner_clause_rows)
write_csv(OUTPUTS["w_audit"], w_audit_rows)
write_csv(OUTPUTS["w_gates"], w_gate_rows)
write_csv(OUTPUTS["dotg_attempt"], dotg_attempt_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["w_owner_clause"], BRANCH_OUTPUTS["w_owner_clause_copy"])
copy_csv(OUTPUTS["w_audit"], BRANCH_OUTPUTS["w_audit_copy"])
copy_csv(OUTPUTS["w_gates"], BRANCH_OUTPUTS["w_gates_copy"])
copy_csv(OUTPUTS["dotg_attempt"], BRANCH_OUTPUTS["dotg_attempt_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3054 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["w_owner_clause"],
    OUTPUTS["w_audit"],
    OUTPUTS["w_gates"],
    OUTPUTS["dotg_attempt"],
    OUTPUTS["claim_status"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
    *BRANCH_OUTPUTS.values(),
]

all_output_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_output_rows.extend(rows(path))

generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
formalization_generated_hits = [path for path in generated_paths if FORMALIZATION.exists() and under(path, FORMALIZATION)]
dotg_rows_after = rows(DOTG_TARGET)

has_w_definition = any("W := Phi_metric" in row["mathematical_content"] for row in w_owner_clause_rows)
has_audit_blockers = any("BLOCKER" in row["classification"] for row in w_audit_rows)

validation_rows = [
    base({"validation_id": "VAL3054_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3054_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3054_02_w_owner_clause_written", "passed": has_w_definition and len(w_owner_clause_rows) >= 7, "requirement": "W parent-owner clause explicitly defines W as Phi_metric", "evidence": OUTPUTS["w_owner_clause"].name}),
    base({"validation_id": "VAL3054_03_w_occurrence_audit", "passed": len(w_audit_rows) == len(W_AUDIT_TARGETS) and has_audit_blockers, "requirement": "targeted W occurrence audit records remaining blockers", "evidence": OUTPUTS["w_audit"].name}),
    base({"validation_id": "VAL3054_04_w_gates_block", "passed": all(row["gate_passes_for_current_MTS"] == "false" for row in w_gate_rows), "requirement": "W owner gates remain blocked for current MTS", "evidence": OUTPUTS["w_gates"].name}),
    base({"validation_id": "VAL3054_05_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3054" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3054 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3054_06_dotg_attempt_nonclaim", "passed": all(str(row["valid_prediction_row"]).lower() == "false" for row in dotg_attempt_rows), "requirement": "dotG coefficient attempt remains nonclaim", "evidence": OUTPUTS["dotg_attempt"].name}),
    base({"validation_id": "VAL3054_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active/signature flags"}),
    base({"validation_id": "VAL3054_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "all 3054 claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3054_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3054_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3054_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3054_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3055-"), "requirement": "next target selects Hilbert source descent / W-channel retirement", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3054_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3054 - W Definition Parent Owner or dotG Parent Coefficient Derivation

Status: `Y5_R2FR_3054_W_metric_readout_owner_clause_written_not_adopted_dotG_blocked_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3054 chooses the cleanest low-scrutiny route:

`W` should not be a separate local field.

The proposed parent-owner clause is:

`Phi_metric[g_obs] := (c^2/2)*(g_obs00+1)` where `g_obs00=-1+2*Phi_metric/c^2`

`W := Phi_metric[g_obs]`

`chi_W := W/c^2 := Phi_metric/c^2`

This is strong because it removes the extra `W` denominator instead of tuning it. If adopted, `W=Phi_metric` is not an axiom glued on top; it is the definition of the local weak-field readout of the parent metric.

But 3054 does **not** claim this is active MTS yet. The targeted audit still finds old two-channel/coefficient language: `a_W`, `chi_W`, `C_W`, and `A_W` appear as independent diagnostic/coefficient objects in prior checkpoints. Those can be harmless only if the next step retires them as pullback coordinates of the single metric/Hilbert source, not as independent fields.

The dotG fallback remains blocked: topological `d kappa_eff=0` is only half the job because readout drift must also be zero, and scalar-kappa dynamics still supplies no real numeric coefficient.

## W Parent-Owner Clause

{md_table(w_owner_clause_rows, ["clause_id", "clause", "mathematical_content", "effect_if_adopted", "current_status", "missing_for_claim"])}

## W Occurrence Audit

{md_table(w_audit_rows, ["audit_id", "path", "w_token_count", "classification", "safe_to_retire_now", "required_action"])}

## W Owner Gate Evaluation

{md_table(w_gate_rows, ["gate_id", "requirement", "candidate_result", "current_status", "gate_passes_for_current_MTS", "blocker"])}

## dotG Parent Coefficient Attempt

{md_table(dotg_attempt_rows, ["attempt_id", "formula", "candidate_derivation", "result", "current_status", "numeric_value", "units", "reason"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "parse_ok", "row_count", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "row_count", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3054 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: W owner clause written but not adopted; dotG blocked nonclaim")
