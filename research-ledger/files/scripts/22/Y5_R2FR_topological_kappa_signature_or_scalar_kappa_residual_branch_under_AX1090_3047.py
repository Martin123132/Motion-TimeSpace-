from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3047"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3047-Y5-R2FR-topological-kappa-signature-or-scalar-kappa-residual-branch-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3047_00_3046_doc": ROOT / "3046-Y5-R2FR-Gref-Geff-reference-lock-or-epsilon-A-bound-row-under-AX1090.md",
    "SRC3047_01_3046_lock": RESIDUALS / "P8_Y5_R2FR_3046_GREF_GEFF_REFERENCE_LOCK_ATTEMPT.csv",
    "SRC3047_02_3046_topological": RESIDUALS / "P8_Y5_R2FR_3046_TOPOLOGICAL_KAPPA_ROUTE_AUDIT.csv",
    "SRC3047_03_3046_epsilon": RESIDUALS / "P8_Y5_R2FR_3046_EPSILON_GREF_COMPONENT_ROW.csv",
    "SRC3047_04_3046_next": RESIDUALS / "P8_Y5_R2FR_3046_NEXT_TARGET.csv",
    "SRC3047_05_constant_kappa_sources": RESIDUALS / "P8_CONSTANT_KAPPA_SOURCE_REGISTER.csv",
    "SRC3047_06_constant_kappa_theorem": RESIDUALS / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
    "SRC3047_07_topological_clause": RESIDUALS / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
    "SRC3047_08_kappa_residual_map": RESIDUALS / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv",
    "SRC3047_09_kappa_route_update": RESIDUALS / "P8_CONSTANT_KAPPA_ROUTE_UPDATE.csv",
    "SRC3047_10_global_coupling": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
    "SRC3047_11_constant_kappa_contract": RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
    "SRC3047_12_constant_gm_gate": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
    "SRC3047_13_constant_gm_runner": RESIDUALS / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
    "SRC3047_14_min_parent": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3047_15_symbol_map": RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3047_SOURCE_REGISTER.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_3047_TOPOLOGICAL_KAPPA_SIGNATURE_ATTEMPT.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_3047_KAPPA_VARIATION_AUDIT.csv",
    "adoption": RESIDUALS / "P8_Y5_R2FR_3047_PARENT_ADOPTION_GATE.csv",
    "scalar_branch": RESIDUALS / "P8_Y5_R2FR_3047_SCALAR_KAPPA_RESIDUAL_BRANCH.csv",
    "runner_bridge": RESIDUALS / "P8_Y5_R2FR_3047_SCALAR_KAPPA_RUNNER_BRIDGE.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3047_COUNTERMODEL_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3047_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3047_PROMOTION_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3047_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3047_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3047_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "signature_copy": PARENT_ACTION / "topological_kappa_signature_attempt_3047_NOT_ADOPTED.csv",
    "variation_copy": PARENT_ACTION / "kappa_variation_audit_3047_CONDITIONAL_NONCLAIM.csv",
    "adoption_copy": PARENT_ACTION / "parent_adoption_gate_3047_FAILED_NONCLAIM.csv",
    "scalar_copy": LOCAL_BOUNDS / "scalar_kappa_residual_branch_3047_NONCLAIM.csv",
    "runner_copy": LOCAL_BOUNDS / "scalar_kappa_runner_bridge_3047_BLOCKED_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3047_SCALAR_KAPPA_RESIDUAL_INPUTS_OR_TOPOLOGICAL_ADOPTION_NEXT_NONCLAIM.csv",
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
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3047_00_3046_doc": "3046 handoff to topological kappa signature or scalar branch",
    "SRC3047_01_3046_lock": "G_ref/Geff lock attempt",
    "SRC3047_02_3046_topological": "topological kappa route audit",
    "SRC3047_03_3046_epsilon": "epsilon_Gref component rows",
    "SRC3047_04_3046_next": "3047 target selector",
    "SRC3047_05_constant_kappa_sources": "constant kappa source register",
    "SRC3047_06_constant_kappa_theorem": "constant kappa theorem attempt",
    "SRC3047_07_topological_clause": "zero-form/three-form topological clause",
    "SRC3047_08_kappa_residual_map": "scalar-kappa residual map",
    "SRC3047_09_kappa_route_update": "route update after 508",
    "SRC3047_10_global_coupling": "global coupling superselection contract",
    "SRC3047_11_constant_kappa_contract": "constant universal kappa/Geff contract",
    "SRC3047_12_constant_gm_gate": "constant GM derivative hair gate",
    "SRC3047_13_constant_gm_runner": "local residual runner inputs",
    "SRC3047_14_min_parent": "minimum parent action blocks",
    "SRC3047_15_symbol_map": "symbol/action map",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

signature_rows = [
    base(
        {
            "signature_id": "KSIG3047_0_field_content",
            "object": "topological zero-form/three-form kappa sector",
            "statement": "Introduce kappa_eff as a zero-form and A_3 as a metric-independent three-form in a global/topological sector.",
            "math_form": "S_kappa_top = integral_M kappa_eff dA_3",
            "result": "SIGNATURE_CANDIDATE_EXACT",
            "missing_for_claim": "MISSING_PARENT_ADOPTION; MISSING_BOUNDARY_CONDITIONS_FOR_A3",
        }
    ),
    base(
        {
            "signature_id": "KSIG3047_1_variation_A3",
            "object": "A_3 variation",
            "statement": "Varying A_3 gives the zero-gradient equation.",
            "math_form": "delta_A3 S = - integral_M d kappa_eff wedge delta A_3 + boundary, so d kappa_eff=0 when delta A_3 is admissible",
            "result": "LOCAL_CONSTANCY_DERIVED_IF_SECTOR_ADOPTED",
            "missing_for_claim": "MISSING_PARENT_ADOPTION; MISSING_FIXED_OR_TOPOLOGICAL_A3_BOUNDARY_VARIATION",
        }
    ),
    base(
        {
            "signature_id": "KSIG3047_2_variation_kappa",
            "object": "kappa_eff variation",
            "statement": "Varying kappa_eff gives the companion topological equation and must not reintroduce a local scalar force.",
            "math_form": "delta_kappa S gives dA_3 plus any EH/source normalization companion equation",
            "result": "COMPANION_EQUATION_OPEN",
            "missing_for_claim": "MISSING_COMPANION_CONSTRAINT_SIGNATURE; MISSING_NO_LOCAL_SCALAR_STRESS_PROOF",
        }
    ),
    base(
        {
            "signature_id": "KSIG3047_3_metric_stress",
            "object": "metric stress of topological sector",
            "statement": "The topological sector must be metric-independent or boundary/topological-silent in the local exterior.",
            "math_form": "delta_g S_kappa_top = 0 in compact local variations",
            "result": "CONDITIONAL_STRESS_SILENCE",
            "missing_for_claim": "MISSING_BOUNDARY_NO_FLUX; MISSING_NO_MEASURED_MASS_CHANNEL_LEAK",
        }
    ),
    base(
        {
            "signature_id": "KSIG3047_4_Gref_owner",
            "object": "reference normalization",
            "statement": "Even if d kappa_eff=0, A_W needs W's denominator G_ref to be the same parent EH coupling reference.",
            "math_form": "G_ref = kappa_eff c^4/(8*pi)",
            "result": "REFERENCE_OWNER_NOT_SIGNED",
            "missing_for_claim": "MISSING_PARENT_DECLARATION_THAT_W_DENOMINATOR_USES_G_EH",
        }
    ),
    base(
        {
            "signature_id": "KSIG3047_5_verdict",
            "object": "current topological kappa proof",
            "statement": "The derivation is mathematically valid as a parent-action option, but current corpus rows do not adopt it as the active parent signature.",
            "math_form": "candidate != current parent proof",
            "result": "TOPOLOGICAL_KAPPA_NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_PARENT_ADOPTION_OR_EXPLICIT_USER_DECISION; MISSING_GREF_OWNER",
        }
    ),
]

variation_rows = [
    base({"variation_id": "VAR3047_0_A3", "variation": "delta A_3", "equation": "d kappa_eff=0", "status": "DERIVED_IF_TOPOLOGICAL_SECTOR_ADOPTED", "claim_effect": "would kill local kappa gradients"}),
    base({"variation_id": "VAR3047_1_kappa", "variation": "delta kappa_eff", "equation": "dA_3 plus EH/source companion constraint", "status": "COMPANION_CONSTRAINT_OPEN", "claim_effect": "can become Lagrange multiplier patch if unowned"}),
    base({"variation_id": "VAR3047_2_metric", "variation": "delta g_obs", "equation": "delta_g S_kappa_top=0 only for metric-independent/topological sector", "status": "CONDITIONAL_STRESS_SILENCE", "claim_effect": "must not add non-EH local stress"}),
    base({"variation_id": "VAR3047_3_matter_source", "variation": "delta matter/source fields", "equation": "partial_matter kappa_eff=0 and no source labels", "status": "NOT_PARENT_DERIVED", "claim_effect": "blocks source-charge/WEP closure"}),
    base({"variation_id": "VAR3047_4_boundary", "variation": "boundary/reference variations", "equation": "fixed A3 boundary or topological boundary term with no mass flux", "status": "MISSING_BOUNDARY_NO_FLUX", "claim_effect": "blocks measured-GM promotion"}),
]

adoption_rows = [
    base({"gate_id": "ADOPT3047_0_explicit_parent_clause", "requirement": "S_kappa_top is explicitly part of the active parent action", "current_status": "FAILED_CANDIDATE_NOT_ADOPTED", "evidence": "symbol map says conditional/not adopted; 508 says not in current parent action", "claim_effect": "no d kappa theorem claim"}),
    base({"gate_id": "ADOPT3047_1_global_sector", "requirement": "kappa_eff belongs to K_global, not a local scalar bundle", "current_status": "FAILED_NOT_PARENT_DERIVED", "evidence": "GS0/GS1 and CU1", "claim_effect": "scalar-kappa residual branch remains"}),
    base({"gate_id": "ADOPT3047_2_marker_blindness", "requirement": "kappa_eff has no memory/domain/source/species/range/frame dependence", "current_status": "FAILED_NOT_PARENT_DERIVED", "evidence": "GS2-GS4/CU2-CU4", "claim_effect": "Gdot/R10/WEP residuals remain"}),
    base({"gate_id": "ADOPT3047_3_boundary_stress_silence", "requirement": "topological sector has no local stress or boundary mass-channel flux", "current_status": "FAILED_BOUNDARY_OPEN", "evidence": "topological clause K508_3 and boundary ledgers", "claim_effect": "no measured-GM/local-GR promotion"}),
    base({"gate_id": "ADOPT3047_4_Gref_owner", "requirement": "W denominator G_ref is parent-owned as kappa_eff c^4/(8*pi)", "current_status": "FAILED_REFERENCE_NOT_SIGNED", "evidence": "3046 reference lock", "claim_effect": "epsilon_Gref remains"}),
]

scalar_branch_rows = [
    base({"residual_id": "SKR3047_0_static_reference", "quantity": "epsilon_Gref", "formula": "kappa_eff c^4/(8*pi*G_ref)-1", "units": "dimensionless", "status": "FORMULA_READY_VALUE_MISSING", "needed_input": "parent reference lock or numeric prior/bound", "observable_link": "A_W; D_WPhi; Newton"}),
    base({"residual_id": "SKR3047_1_time_drift", "quantity": "dln_Geff_dt", "formula": "D_t ln G_eff", "units": "yr^-1", "status": "RUNNER_TEMPLATE_EXISTS_VALUE_MISSING", "needed_input": "Gdot theorem-zero or numeric bound row", "observable_link": "Gdot; orbital timing; clocks"}),
    base({"residual_id": "SKR3047_2_source_species", "quantity": "eta_source_AB / partial_A ln G_eff", "formula": "Delta_AB ln G_eff or active source-charge contrast", "units": "dimensionless", "status": "RUNNER_TEMPLATE_EXISTS_VALUE_MISSING", "needed_input": "source-blindness theorem or material/source coefficient", "observable_link": "WEP; source-charge"}),
    base({"residual_id": "SKR3047_3_range", "quantity": "alpha(lambda)", "formula": "finite-range scalar-kappa source-normalization response", "units": "dimensionless curve", "status": "CURVE_REQUIRED_VALUE_MISSING", "needed_input": "alpha(lambda) prediction curve or no-range theorem", "observable_link": "R10; inverse-square"}),
    base({"residual_id": "SKR3047_4_radial", "quantity": "partial_r ln G_eff", "formula": "radial coupling hair outside compact support", "units": "inverse length or dimensionless profile", "status": "PROFILE_REQUIRED_VALUE_MISSING", "needed_input": "radial no-hair theorem or profile envelope", "observable_link": "orbital; PPN; inverse-square"}),
    base({"residual_id": "SKR3047_5_frame_domain", "quantity": "delta_frame_source / D_domain ln G_eff", "formula": "source-frame/domain coupling split", "units": "dimensionless", "status": "RUNNER_TEMPLATE_EXISTS_VALUE_MISSING", "needed_input": "same-frame/domain-blind theorem or residual coefficient", "observable_link": "clock; WEP; PPN"}),
    base({"residual_id": "SKR3047_6_Bianchi_exchange", "quantity": "delta_kappa_source", "formula": "kappa_eff^-1 P_loc[T_obs grad kappa_eff]", "units": "declared source-normalization units", "status": "EXCHANGE_ROW_REQUIRED", "needed_input": "same-frame arbitrary-source conservation theorem or exchange coefficient", "observable_link": "q_loc; PPN; R10"}),
]

runner_bridge = [
    base({"bridge_id": "BR3047_0_Gdot", "target_file": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "existing_component": "P8_Geff_time_drift", "new_scalar_quantity": "dln_Geff_dt", "current_runner_state": "not_scoreable_prediction_missing", "next_fill": "P8_time_drift_residual_or_zero.csv"}),
    base({"bridge_id": "BR3047_1_R10", "target_file": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "existing_component": "P8_range_dependence", "new_scalar_quantity": "alpha(lambda)", "current_runner_state": "not_scoreable_curve_missing", "next_fill": "R10_alpha_lambda_curve_MTS_source_normalization.csv"}),
    base({"bridge_id": "BR3047_2_WEP", "target_file": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "existing_component": "P8_species_source_charge", "new_scalar_quantity": "eta_source_AB", "current_runner_state": "not_scoreable_prediction_missing", "next_fill": "P8_species_source_charge_residual_or_zero.csv"}),
    base({"bridge_id": "BR3047_3_radial", "target_file": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "existing_component": "P8_radial_source_hair", "new_scalar_quantity": "partial_r_ln_mu_obs or partial_r ln G_eff", "current_runner_state": "not_scoreable_prediction_missing", "next_fill": "P8_radial_mu_profile_or_zero.csv"}),
    base({"bridge_id": "BR3047_4_frame", "target_file": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "existing_component": "P8_frame_calibration_split", "new_scalar_quantity": "delta_frame_source", "current_runner_state": "not_scoreable_prediction_missing", "next_fill": "P8_frame_source_split_residual_or_zero.csv"}),
]

countermodels = [
    base({"countermodel_id": "CM3047_0_candidate_not_action", "case": "topological clause exists as candidate but not in active parent action", "why_it_blocks": "a possible repair is not a derivation of current MTS", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3047_1_kappa_constant_Gref_free", "case": "d kappa_eff=0 but G_ref is an independently chosen W denominator", "why_it_blocks": "A_W remains a constant reference mismatch", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3047_2_boundary_flux", "case": "topological sector has boundary/reference variation carrying mass-channel flux", "why_it_blocks": "local gradients vanish but measured-GM shifts", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3047_3_scalar_kappa_hair", "case": "kappa_eff depends on source/range/frame/domain variables", "why_it_blocks": "Gdot/R10/WEP/q_loc residuals become physical", "status": "LIVE_BLOCKER"}),
]

decision_rows = [
    base({"decision_id": "DEC3047_0_derivation", "question": "does the topological route mathematically derive d kappa_eff=0?", "answer": "YES_IF_ADOPTED", "reason": "delta A_3 variation gives d kappa_eff=0", "action": "record as conditional parent-signature route"}),
    base({"decision_id": "DEC3047_1_adoption", "question": "is the route adopted/signed by current corpus?", "answer": "NO", "reason": "source rows repeatedly say candidate, not adopted, not parent-derived", "action": "do not claim constant kappa"}),
    base({"decision_id": "DEC3047_2_residual", "question": "what happens if not adopted?", "answer": "SCALAR_KAPPA_RESIDUAL_BRANCH_ACTIVE", "reason": "Gdot/R10/WEP/radial/frame rows already exist as missing runner inputs", "action": "stage scalar-kappa residual branch rows"}),
    base({"decision_id": "DEC3047_3_next", "question": "what is the least-smuggly next target?", "answer": "fill first scalar-kappa residual inputs or explicitly adopt parent clause", "reason": "we need either a real parent action decision or empirical residual rows", "action": "3048 should create first source-backed scalar-kappa input rows"}),
]

gates = [
    base({"gate_id": "GATE3047_0_sources_exist", "gate": "all cited source paths exist", "passed": all(boolish(row["exists"]) for row in source_register), "claim_effect": "source-backed checkpoint"}),
    base({"gate_id": "GATE3047_1_variation_derives_constancy", "gate": "delta A_3 derivation of d kappa_eff=0 is written", "passed": True, "claim_effect": "conditional theorem route"}),
    base({"gate_id": "GATE3047_2_parent_adoption", "gate": "topological kappa sector is active parent action", "passed": False, "claim_effect": "blocks constant-kappa claim"}),
    base({"gate_id": "GATE3047_3_Gref_owner", "gate": "G_ref ownership is signed", "passed": False, "claim_effect": "blocks epsilon_Gref=0"}),
    base({"gate_id": "GATE3047_4_boundary_stress", "gate": "boundary/stress silence is signed", "passed": False, "claim_effect": "blocks measured-GM promotion"}),
    base({"gate_id": "GATE3047_5_scalar_branch", "gate": "scalar-kappa residual branch rows are staged", "passed": True, "claim_effect": "testable fallback"}),
    base({"gate_id": "GATE3047_6_runner_bridge", "gate": "runner bridge rows map to Gdot/R10/WEP/radial/frame tests", "passed": True, "claim_effect": "empirical path"}),
    base({"gate_id": "GATE3047_7_no_claim_rows", "gate": "no generated 3047 row is valid for claim", "passed": True, "claim_effect": "private nonclaim checkpoint"}),
    base({"gate_id": "GATE3047_8_next_target", "gate": "next target selects scalar-kappa input rows or explicit adoption", "passed": True, "claim_effect": "no circling"}),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3047_0_3048",
            "next_checkpoint": "3048-Y5-R2FR-scalar-kappa-residual-inputs-or-topological-adoption-decision-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_scalar_kappa_residual_inputs_or_topological_adoption_decision_under_AX1090_3048.py",
            "mission": "either explicitly promote the topological kappa clause into the parent-action spine with G_ref ownership, or build first source-backed scalar-kappa residual input rows for Gdot, R10 alpha(lambda), source-charge WEP, radial hair, and frame split",
            "starting_equation": "d kappa_eff=0 only if S_kappa_top is parent-owned; otherwise retain dln_Geff_dt, alpha(lambda), eta_source_AB, partial_r ln G_eff, delta_frame_source and delta_kappa_source",
            "do_not_repeat": "do not treat candidate topological infrastructure as current proof",
            "claim_policy": "no A_W/Newton/PPN/local-GR claim until parent adoption or residual rows are valid",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["signature"], signature_rows)
write_csv(OUTPUTS["variation"], variation_rows)
write_csv(OUTPUTS["adoption"], adoption_rows)
write_csv(OUTPUTS["scalar_branch"], scalar_branch_rows)
write_csv(OUTPUTS["runner_bridge"], runner_bridge)
write_csv(OUTPUTS["countermodels"], countermodels)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["gates"], gates)
write_csv(OUTPUTS["next"], next_rows)

branch_map = [
    ("signature_copy", OUTPUTS["signature"], BRANCH_OUTPUTS["signature_copy"], "topological kappa signature attempt copy"),
    ("variation_copy", OUTPUTS["variation"], BRANCH_OUTPUTS["variation_copy"], "kappa variation audit copy"),
    ("adoption_copy", OUTPUTS["adoption"], BRANCH_OUTPUTS["adoption_copy"], "parent adoption gate copy"),
    ("scalar_copy", OUTPUTS["scalar_branch"], BRANCH_OUTPUTS["scalar_copy"], "scalar-kappa residual branch copy"),
    ("runner_copy", OUTPUTS["runner_bridge"], BRANCH_OUTPUTS["runner_copy"], "runner bridge copy"),
    ("queue_copy", OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"], "3048 acquisition queue copy"),
]
branch_rows: list[dict[str, Any]] = []
for copy_id, source, destination, description in branch_map:
    shutil.copyfile(source, destination)
    branch_rows.append(
        base(
            {
                "copy_id": copy_id,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "description": description,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
non_validation_csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
formalization_hits = list(FORMALIZATION.rglob("*3047*")) if FORMALIZATION.exists() else []

all_non_validation_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_non_validation_rows.extend(rows(path))

validation_rows = [
    base({"validation_id": "VAL3047_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3047_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated non-validation CSV and branch-copy rows parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3047_02_variation_route", "passed": any(row["signature_id"] == "KSIG3047_1_variation_A3" and row["result"] == "LOCAL_CONSTANCY_DERIVED_IF_SECTOR_ADOPTED" for row in signature_rows), "requirement": "delta A3 route derives local constancy conditionally", "evidence": OUTPUTS["signature"].name}),
    base({"validation_id": "VAL3047_03_not_adopted", "passed": any(row["signature_id"] == "KSIG3047_5_verdict" and row["result"] == "TOPOLOGICAL_KAPPA_NOT_PARENT_SIGNED" for row in signature_rows), "requirement": "topological route is not promoted as current proof", "evidence": OUTPUTS["signature"].name}),
    base({"validation_id": "VAL3047_04_adoption_gates_fail", "passed": any(row["gate_id"] == "ADOPT3047_0_explicit_parent_clause" and row["current_status"].startswith("FAILED") for row in adoption_rows), "requirement": "parent adoption gate records failure", "evidence": OUTPUTS["adoption"].name}),
    base({"validation_id": "VAL3047_05_scalar_branch_rows", "passed": len(scalar_branch_rows) >= 7, "requirement": "scalar-kappa residual rows are staged", "evidence": OUTPUTS["scalar_branch"].name}),
    base({"validation_id": "VAL3047_06_runner_bridge", "passed": len(runner_bridge) >= 5, "requirement": "runner bridge covers Gdot, R10, WEP, radial and frame tests", "evidence": OUTPUTS["runner_bridge"].name}),
    base({"validation_id": "VAL3047_07_no_claim_rows", "passed": not any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) or boolish(row.get("valid_prediction_row")) for row in all_non_validation_rows), "requirement": "no 3047 row is valid for claim", "evidence": "generated rows"}),
    base({"validation_id": "VAL3047_08_countermodels_live", "passed": len(countermodels) >= 4 and all(row["status"] == "LIVE_BLOCKER" for row in countermodels), "requirement": "shortcut countermodels remain live", "evidence": OUTPUTS["countermodels"].name}),
    base({"validation_id": "VAL3047_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3047_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3047_11_formalization_untouched", "passed": len(formalization_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"formalization 3047 hits={len(formalization_hits)}"}),
    base({"validation_id": "VAL3047_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3048-"), "requirement": "next target selects scalar-kappa inputs or explicit adoption", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3047_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3047 - Topological Kappa Signature or Scalar-Kappa Residual Branch

Status: `Y5_R2FR_3047_topological_kappa_conditional_scalar_branch_active`

Generated: `{RUN_UTC}`

## Verdict

3047 tries the derivation route first.

The topological route is mathematically clean:

`S_kappa_top = integral_M kappa_eff dA_3`

and varying `A_3` gives

`d kappa_eff = 0`

on connected local domains, assuming admissible/fixed/topological boundary variation.

But this is still a candidate parent-action clause, not a signed current-MTS theorem. The existing source rows say `A_3` is new infrastructure, the route is conditional/not adopted, and the active parent still lacks `G_ref` ownership plus boundary/stress silence. Therefore 3047 does not claim constant kappa, `epsilon_Gref=0`, `A_W=1`, Newton, PPN, or local GR.

The fallback is now explicit: scalar-kappa residual rows for `dln_Geff_dt`, `alpha(lambda)`, source-charge/WEP, radial hair, frame/domain split, and Bianchi exchange.

## Topological Signature Attempt

{md_table(signature_rows, ["signature_id", "object", "math_form", "result", "missing_for_claim"])}

## Variation Audit

{md_table(variation_rows, ["variation_id", "variation", "equation", "status", "claim_effect"])}

## Parent Adoption Gate

{md_table(adoption_rows, ["gate_id", "requirement", "current_status", "claim_effect"])}

## Scalar-Kappa Residual Branch

{md_table(scalar_branch_rows, ["residual_id", "quantity", "formula", "status", "needed_input", "observable_link"])}

## Runner Bridge

{md_table(runner_bridge, ["bridge_id", "existing_component", "new_scalar_quantity", "current_runner_state", "next_fill"])}

## Countermodels

{md_table(countermodels, ["countermodel_id", "case", "why_it_blocks", "status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "passed", "claim_effect"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3047 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: topological kappa conditional; scalar-kappa residual branch active")
