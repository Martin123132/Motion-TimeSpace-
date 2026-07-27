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

CHECKPOINT = "3046"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3046-Y5-R2FR-Gref-Geff-reference-lock-or-epsilon-A-bound-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3046_00_3045_doc": ROOT / "3045-Y5-R2FR-linear-source-normalization-coefficient-map-or-AW-bound-row-under-AX1090.md",
    "SRC3046_01_3045_coefficient": RESIDUALS / "P8_Y5_R2FR_3045_LINEAR_SOURCE_NORMALIZATION_COEFFICIENT_MAP.csv",
    "SRC3046_02_3045_epsilon": RESIDUALS / "P8_Y5_R2FR_3045_EPSILON_A_COMPONENT_SCHEMA.csv",
    "SRC3046_03_3045_bound": RESIDUALS / "P8_Y5_R2FR_3045_DWPHI_FROM_LINEAR_COEFFICIENT_BOUND_SCHEMA.csv",
    "SRC3046_04_3045_next": RESIDUALS / "P8_Y5_R2FR_3045_NEXT_TARGET.csv",
    "SRC3046_05_global_coupling": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
    "SRC3046_06_constant_kappa": RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
    "SRC3046_07_calibration_lock": RESIDUALS / "P8_CALIBRATION_LOCK_ATTEMPT.csv",
    "SRC3046_08_constant_gm_zero": RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
    "SRC3046_09_constant_gm_hair": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
    "SRC3046_10_constant_gm_runner": RESIDUALS / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
    "SRC3046_11_min_parent": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3046_12_symbol_map": RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
    "SRC3046_13_pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "SRC3046_14_hilbert_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "SRC3046_15_mass_flux_contract": RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3046_SOURCE_REGISTER.csv",
    "lock": RESIDUALS / "P8_Y5_R2FR_3046_GREF_GEFF_REFERENCE_LOCK_ATTEMPT.csv",
    "topological": RESIDUALS / "P8_Y5_R2FR_3046_TOPOLOGICAL_KAPPA_ROUTE_AUDIT.csv",
    "epsilon_gref": RESIDUALS / "P8_Y5_R2FR_3046_EPSILON_GREF_COMPONENT_ROW.csv",
    "epsilon_a_update": RESIDUALS / "P8_Y5_R2FR_3046_EPSILON_A_BOUND_UPDATE.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3046_COUNTERMODEL_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3046_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3046_PROMOTION_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3046_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3046_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3046_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "lock_copy": PARENT_ACTION / "Gref_Geff_reference_lock_attempt_3046_NOT_SIGNED.csv",
    "topological_copy": PARENT_ACTION / "topological_kappa_route_audit_3046_CANDIDATE_NONCLAIM.csv",
    "epsilon_gref_copy": LOCAL_BOUNDS / "epsilon_Gref_component_row_3046_BLOCKED_NONCLAIM.csv",
    "epsilon_a_copy": LOCAL_BOUNDS / "epsilon_A_bound_update_3046_BLOCKED_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3046_TOPOLOGICAL_KAPPA_SIGNATURE_OR_SCALAR_KAPPA_RESIDUAL_NEXT_NONCLAIM.csv",
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
    "SRC3046_00_3045_doc": "3045 handoff to G_ref/G_eff lock",
    "SRC3046_01_3045_coefficient": "A_W ratio law and G_ref lock condition",
    "SRC3046_02_3045_epsilon": "epsilon_A component schema",
    "SRC3046_03_3045_bound": "D_WPhi component bound schema",
    "SRC3046_04_3045_next": "3046 target selector",
    "SRC3046_05_global_coupling": "global coupling superselection contract",
    "SRC3046_06_constant_kappa": "constant universal Geff/kappa contract",
    "SRC3046_07_calibration_lock": "calibration lock attempt",
    "SRC3046_08_constant_gm_zero": "constant GM theorem attempt",
    "SRC3046_09_constant_gm_hair": "derivative hair gate",
    "SRC3046_10_constant_gm_runner": "constant GM residual runner input",
    "SRC3046_11_min_parent": "minimum parent action blocks",
    "SRC3046_12_symbol_map": "symbol to local-GR action map",
    "SRC3046_13_pg_contract": "Poisson/Gauss coupling contract",
    "SRC3046_14_hilbert_contract": "Hilbert monopole coupling contract",
    "SRC3046_15_mass_flux_contract": "mass flux absolute calibration contract",
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

lock_rows = [
    base(
        {
            "lock_id": "GLOCK3046_0_reference_identity",
            "claim_piece": "G_ref/Geff reference identity",
            "statement": "If the parent EH/source normal form defines G_EH := kappa_eff c^4/(8*pi) and defines W with G_ref=G_EH before orbital fitting, then epsilon_Gref=0.",
            "derived_relation": "epsilon_Gref = kappa_eff c^4/(8*pi*G_ref)-1",
            "result": "EXACT_LOCK_CONDITION_DERIVED",
            "missing_for_claim": "MISSING_PARENT_DECLARATION_THAT_G_REF_IS_G_EH; MISSING_NO_POSTFIT_GM_IMPORT",
            "claim_effect": "turns A_W unity into a parent reference-normalization question",
        }
    ),
    base(
        {
            "lock_id": "GLOCK3046_1_topological_constancy",
            "claim_piece": "constant/global kappa",
            "statement": "A topological/global coupling sector can make d kappa_eff=0 on connected local domains.",
            "derived_relation": "delta_{A_3} S_kappa_top -> d kappa_eff=0",
            "result": "CANDIDATE_ROUTE_EXISTS_NOT_ADOPTED",
            "missing_for_claim": "MISSING_PARENT_ADOPTION_OF_A3_OR_SUPERSELECTION_SECTOR; MISSING_PROOF_KAPPA_NOT_LOCAL_FIELD",
            "claim_effect": "would suppress Gdot/radial/range kappa drift, not automatically absolute G_ref",
        }
    ),
    base(
        {
            "lock_id": "GLOCK3046_2_absolute_normalization_warning",
            "claim_piece": "absolute numerical G is not predicted by naming",
            "statement": "A constant offset in kappa/G can be calibration-only unless the parent action fixes the absolute unit/reference convention independently.",
            "derived_relation": "constant_global delta kappa/kappa is harmless only for derivative/source tests, not an absolute-G prediction",
            "result": "CONSTANT_OFFSET_POLICY_RETAINED",
            "missing_for_claim": "MISSING_ABSOLUTE_COUPLING_NORMALIZATION_THEOREM",
            "claim_effect": "no claim that MTS predicts numerical G; local tests care about derivative/source/range residuals",
        }
    ),
    base(
        {
            "lock_id": "GLOCK3046_3_current_status",
            "claim_piece": "current G_ref lock status",
            "statement": "Existing coupling rows say the constant/global route is conditional or not parent-derived.",
            "derived_relation": "G_ref=G_EH remains a contract, not current theorem",
            "result": "G_REF_LOCK_NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_GLOBAL_COUPLING_SUPERSELECTION; MISSING_SOURCE_REFERENCE_OWNER; MISSING_DERIVATIVE_HAIR_ZERO",
            "claim_effect": "epsilon_Gref remains active",
        }
    ),
]

topological_rows = [
    base(
        {
            "route_id": "KTOP3046_0_action_block",
            "candidate": "S_kappa_top = integral kappa_eff dA_3",
            "would_prove": "d kappa_eff=0 on connected local domains",
            "current_status": "CANDIDATE_IN_MIN_PARENT_BLOCKS_NOT_ADOPTED",
            "source_anchor": "A511_1 and symbol-map kappa_eff/A_3 rows",
            "failure_if_missing": "G_eff/kappa can drift as a local scalar/source-normalization field",
        }
    ),
    base(
        {
            "route_id": "KTOP3046_1_configuration_factorization",
            "candidate": "Q_parent=Q_dyn x K_global with kappa_eff in K_global",
            "would_prove": "compact local variations cannot vary kappa_eff",
            "current_status": "NOT_PARENT_DERIVED",
            "source_anchor": "GS0/GS1",
            "failure_if_missing": "scalar-kappa branch and fifth-force/PPN locks remain active",
        }
    ),
    base(
        {
            "route_id": "KTOP3046_2_marker_blindness",
            "candidate": "partial_Z/A/lambda/frame kappa_eff=0 from superselection/source-blindness",
            "would_prove": "no source/species/range/radial/time coupling hair",
            "current_status": "NOT_PARENT_DERIVED",
            "source_anchor": "GS2-GS4/CU2-CU4",
            "failure_if_missing": "Gdot, WEP source-charge, R10 and radial residual rows stay active",
        }
    ),
    base(
        {
            "route_id": "KTOP3046_3_Bianchi_guard",
            "candidate": "Bianchi only closes kappa if same-frame conserved arbitrary-source conditions hold",
            "would_prove": "no hidden T_obs nabla kappa exchange term",
            "current_status": "CONDITIONAL_ONLY",
            "source_anchor": "GS5/CU5",
            "failure_if_missing": "delta_kappa_source remains in q_loc/source-normalization residual ledger",
        }
    ),
    base(
        {
            "route_id": "KTOP3046_4_reference_lock_limit",
            "candidate": "topological constancy plus parent definition G_ref=G_EH",
            "would_prove": "epsilon_Gref=0 only if both constancy and reference definition are accepted",
            "current_status": "REFERENCE_DEFINITION_NOT_SIGNED",
            "source_anchor": "3045 ratio law plus CU6/GS6",
            "failure_if_missing": "constant mismatch can be calibration-only but not a derived A_W=1 theorem",
        }
    ),
]

epsilon_gref_rows = [
    base(
        {
            "component_id": "EGREF3046_0_static_offset",
            "quantity": "epsilon_Gref",
            "definition": "kappa_eff c^4/(8*pi*G_ref)-1",
            "status": "FORMULA_READY_VALUE_MISSING",
            "units": "dimensionless",
            "missing_input": "parent G_ref=G_EH theorem or numeric prior/bound on constant mismatch",
            "observable_link": "A_W; D_WPhi; Newton source normalization",
        }
    ),
    base(
        {
            "component_id": "EGREF3046_1_time_drift",
            "quantity": "D_t ln G_eff",
            "definition": "time derivative of the local coupling/reference normalization",
            "status": "MISSING_DERIVED_ZERO_OR_NUMERIC_GDOT_ROW",
            "units": "yr^-1 or declared time unit",
            "missing_input": "dln_Geff_dt theorem-zero or bound row",
            "observable_link": "Gdot; clocks; orbital timing",
        }
    ),
    base(
        {
            "component_id": "EGREF3046_2_source_species",
            "quantity": "Delta_A ln G_eff",
            "definition": "source/species/material dependence of active gravitational coupling",
            "status": "MISSING_SOURCE_BLINDNESS_OR_ETA_ROW",
            "units": "dimensionless",
            "missing_input": "source-blind kappa theorem or eta_source_AB row",
            "observable_link": "WEP; source-charge tests",
        }
    ),
    base(
        {
            "component_id": "EGREF3046_3_range_radial",
            "quantity": "partial_r/partial_lambda ln G_eff",
            "definition": "radial or finite-range coupling hair",
            "status": "MISSING_RANGE_RADIAL_ZERO_OR_ALPHA_CURVE",
            "units": "inverse length or dimensionless curve",
            "missing_input": "R10 alpha(lambda), radial source profile, or no-range theorem",
            "observable_link": "R10; orbital; inverse-square tests",
        }
    ),
    base(
        {
            "component_id": "EGREF3046_4_frame_domain",
            "quantity": "Delta_frame/domain ln G_eff",
            "definition": "frame/domain/projector dependence of the coupling branch",
            "status": "MISSING_FRAME_DOMAIN_SUPERSELECTION",
            "units": "dimensionless",
            "missing_input": "same-frame and domain-blind kappa proof",
            "observable_link": "PPN; local-GR; clock/source frame",
        }
    ),
]

epsilon_a_update = [
    base(
        {
            "bound_id": "EAU3046_0_epsA_split",
            "quantity": "epsilon_A",
            "expression": "epsilon_A = epsilon_Gref + epsilon_frame + epsilon_operator + epsilon_source_current + epsilon_mu_extra + epsilon_boundary + epsilon_range_radial + epsilon_readout",
            "status": "COMPONENT_SPLIT_RETAINED",
            "blocking_issue": "epsilon_Gref still formula-only; other 3045 components remain missing",
            "valid_bound_row_created": False,
        }
    ),
    base(
        {
            "bound_id": "EAU3046_1_epsGref",
            "quantity": "epsilon_Gref",
            "expression": "epsilon_Gref = kappa_eff c^4/(8*pi*G_ref)-1",
            "status": "FIRST_COMPONENT_FORMULA_READY_VALUE_MISSING",
            "blocking_issue": "MISSING_PARENT_REFERENCE_LOCK_OR_NUMERIC_BOUND",
            "valid_bound_row_created": False,
        }
    ),
    base(
        {
            "bound_id": "EAU3046_2_DWPhi",
            "quantity": "D_WPhi_total_abs",
            "expression": "|D_WPhi| <= Delta_A/(1-Delta_A) for Delta_A<1",
            "status": "NO_VALID_BOUND_ROW_CREATED",
            "blocking_issue": "MISSING_DELTA_A_COMPONENT_VALUES",
            "valid_bound_row_created": False,
        }
    ),
]

countermodels = [
    base({"countermodel_id": "CM3046_0_constant_mismatch", "case": "kappa_eff is constant but G_ref is chosen independently", "why_it_blocks": "no drift appears, but A_W is a constant not derived to one", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3046_1_local_scalar_kappa", "case": "kappa_eff is a local scalar depending on time/radius/range/source markers", "why_it_blocks": "Gdot, R10, WEP source-charge and q_loc exchange residuals remain", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3046_2_topological_but_unowned_W", "case": "kappa is topological, but W is still defined by fitted G_ref", "why_it_blocks": "topological constancy alone does not prove W denominator is parent-normalized", "status": "LIVE_BLOCKER"}),
    base({"countermodel_id": "CM3046_3_same_G_but_extra_mass", "case": "G_ref=G_EH but mu_extra/source-current residual shifts measured GM", "why_it_blocks": "A_W/Newton can still hide extra monopole or source-current leakage", "status": "LIVE_BLOCKER"}),
]

decision_rows = [
    base({"decision_id": "DEC3046_0_exact_lock", "question": "is the exact G_ref/G_eff lock condition known?", "answer": "YES", "reason": "G_ref must equal kappa_eff c^4/(8*pi) before measured-GM fitting", "action": "record reference-lock theorem contract"}),
    base({"decision_id": "DEC3046_1_current_claim", "question": "is the lock parent-signed in the current corpus?", "answer": "NO", "reason": "global coupling/superselection and topological kappa rows are candidate/conditional/not-parent-derived", "action": "keep epsilon_Gref active"}),
    base({"decision_id": "DEC3046_2_bound", "question": "can an epsilon_A numeric bound be created now?", "answer": "NO", "reason": "epsilon_Gref and sibling epsilon_A components have no theorem-zero or numeric source-backed values", "action": "stage component rows only"}),
    base({"decision_id": "DEC3046_3_next", "question": "what is the least-smuggly next target?", "answer": "topological kappa signature or scalar-kappa residual branch", "reason": "the coupling route must be adopted/derived or made executable as data-bound residuals", "action": "3047 should decide the parent topological clause or build scalar-kappa residual rows"}),
]

gates = [
    base({"gate_id": "GATE3046_0_sources_exist", "gate": "all cited source paths exist", "passed": all(boolish(row["exists"]) for row in source_register), "claim_effect": "source-backed checkpoint"}),
    base({"gate_id": "GATE3046_1_exact_lock", "gate": "G_ref=G_EH exact condition is written", "passed": True, "claim_effect": "real derivation contract"}),
    base({"gate_id": "GATE3046_2_topological_route", "gate": "topological kappa route is audited", "passed": True, "claim_effect": "route identified"}),
    base({"gate_id": "GATE3046_3_parent_adoption", "gate": "parent action currently adopts/signs topological kappa or superselection", "passed": False, "claim_effect": "blocks epsilon_Gref=0"}),
    base({"gate_id": "GATE3046_4_reference_owner", "gate": "W denominator G_ref is parent-owned as G_EH before orbital fitting", "passed": False, "claim_effect": "blocks A_W=1"}),
    base({"gate_id": "GATE3046_5_derivative_hair", "gate": "Gdot/source/range/frame coupling hair is zero or bounded", "passed": False, "claim_effect": "blocks Newton/PPN/local-GR promotion"}),
    base({"gate_id": "GATE3046_6_bound_values", "gate": "epsilon_Gref has numeric or theorem-zero value", "passed": False, "claim_effect": "blocks executable epsilon_A bound"}),
    base({"gate_id": "GATE3046_7_no_claim_rows", "gate": "no generated 3046 row is valid for claim", "passed": True, "claim_effect": "private nonclaim checkpoint"}),
    base({"gate_id": "GATE3046_8_next_target", "gate": "next target selects topological kappa signature or scalar-kappa residual branch", "passed": True, "claim_effect": "does not circle A_W notation"}),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3046_0_3047",
            "next_checkpoint": "3047-Y5-R2FR-topological-kappa-signature-or-scalar-kappa-residual-branch-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_topological_kappa_signature_or_scalar_kappa_residual_branch_under_AX1090_3047.py",
            "mission": "either parent-sign the topological/global kappa sector including G_ref=G_EH ownership, or demote kappa_eff to scalar/residual rows for Gdot, R10, WEP source-charge and frame/radial tests",
            "starting_equation": "epsilon_Gref=kappa_eff c^4/(8*pi*G_ref)-1; d kappa_eff=0 only if superselection/topological sector is parent-owned",
            "do_not_repeat": "do not treat a fitted constant G or naming convention as a derivation",
            "claim_policy": "no A_W/Newton/PPN/local-GR claim until kappa is parent-global and G_ref is owned, or epsilon_Gref is bounded",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["lock"], lock_rows)
write_csv(OUTPUTS["topological"], topological_rows)
write_csv(OUTPUTS["epsilon_gref"], epsilon_gref_rows)
write_csv(OUTPUTS["epsilon_a_update"], epsilon_a_update)
write_csv(OUTPUTS["countermodels"], countermodels)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["gates"], gates)
write_csv(OUTPUTS["next"], next_rows)

branch_map = [
    ("lock_copy", OUTPUTS["lock"], BRANCH_OUTPUTS["lock_copy"], "G_ref/G_eff lock attempt copy"),
    ("topological_copy", OUTPUTS["topological"], BRANCH_OUTPUTS["topological_copy"], "topological kappa route audit copy"),
    ("epsilon_gref_copy", OUTPUTS["epsilon_gref"], BRANCH_OUTPUTS["epsilon_gref_copy"], "epsilon_Gref component rows copy"),
    ("epsilon_a_copy", OUTPUTS["epsilon_a_update"], BRANCH_OUTPUTS["epsilon_a_copy"], "epsilon_A bound update copy"),
    ("queue_copy", OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"], "3047 acquisition queue copy"),
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
formalization_hits = list(FORMALIZATION.rglob("*3046*")) if FORMALIZATION.exists() else []

all_non_validation_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_non_validation_rows.extend(rows(path))

validation_rows = [
    base({"validation_id": "VAL3046_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3046_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated non-validation CSV and branch-copy rows parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3046_02_exact_lock", "passed": any(row["lock_id"] == "GLOCK3046_0_reference_identity" and row["result"] == "EXACT_LOCK_CONDITION_DERIVED" for row in lock_rows), "requirement": "G_ref/G_eff exact lock condition is recorded", "evidence": OUTPUTS["lock"].name}),
    base({"validation_id": "VAL3046_03_lock_not_promoted", "passed": any(row["lock_id"] == "GLOCK3046_3_current_status" and row["result"] == "G_REF_LOCK_NOT_PARENT_SIGNED" for row in lock_rows), "requirement": "G_ref lock is not claimed", "evidence": OUTPUTS["lock"].name}),
    base({"validation_id": "VAL3046_04_topological_route_audited", "passed": len(topological_rows) >= 5, "requirement": "topological kappa route audit exists", "evidence": OUTPUTS["topological"].name}),
    base({"validation_id": "VAL3046_05_epsilon_gref_blocked", "passed": any(row["component_id"] == "EGREF3046_0_static_offset" and row["status"] == "FORMULA_READY_VALUE_MISSING" for row in epsilon_gref_rows), "requirement": "epsilon_Gref remains formula-only without value", "evidence": OUTPUTS["epsilon_gref"].name}),
    base({"validation_id": "VAL3046_06_bound_fail_closed", "passed": any(row["bound_id"] == "EAU3046_2_DWPhi" and row["status"] == "NO_VALID_BOUND_ROW_CREATED" for row in epsilon_a_update), "requirement": "D_WPhi/A_W bound remains blocked", "evidence": OUTPUTS["epsilon_a_update"].name}),
    base({"validation_id": "VAL3046_07_no_claim_rows", "passed": not any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) or boolish(row.get("valid_prediction_row")) for row in all_non_validation_rows), "requirement": "no 3046 row is valid for claim", "evidence": "generated rows"}),
    base({"validation_id": "VAL3046_08_countermodels_live", "passed": len(countermodels) >= 4 and all(row["status"] == "LIVE_BLOCKER" for row in countermodels), "requirement": "shortcut countermodels remain live", "evidence": OUTPUTS["countermodels"].name}),
    base({"validation_id": "VAL3046_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3046_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3046_11_formalization_untouched", "passed": len(formalization_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"formalization 3046 hits={len(formalization_hits)}"}),
    base({"validation_id": "VAL3046_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3047-"), "requirement": "next target selects topological kappa signature or scalar-kappa residual branch", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3046_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3046 - Gref/Geff Reference Lock or Epsilon_A Bound Row

Status: `Y5_R2FR_3046_Gref_lock_exact_but_parent_unsigned`

Generated: `{RUN_UTC}`

## Verdict

3046 isolates the coupling/reference issue cleanly.

The exact lock condition is:

`epsilon_Gref = kappa_eff c^4/(8*pi*G_ref) - 1`.

Therefore `epsilon_Gref=0` only if the parent theory owns

`G_ref = kappa_eff c^4/(8*pi)`

before measured-orbital-`GM` fitting.

The current corpus has a plausible route: a topological/global kappa sector can make `d kappa_eff=0`. But the relevant rows still say this route is candidate, conditional, or not parent-derived. Topological constancy also does not by itself prove that the `W` denominator uses the same parent reference `G_ref`.

So 3046 does not claim `A_W=1`, `D_WPhi=0`, Newton, PPN, or local GR. It converts the coupling gap into an explicit `epsilon_Gref` component and selects the next target: parent-sign the topological kappa sector or demote kappa to executable scalar/residual rows.

## Reference Lock Attempt

{md_table(lock_rows, ["lock_id", "claim_piece", "derived_relation", "result", "missing_for_claim"])}

## Topological Kappa Route Audit

{md_table(topological_rows, ["route_id", "candidate", "would_prove", "current_status", "failure_if_missing"])}

## Epsilon_Gref Components

{md_table(epsilon_gref_rows, ["component_id", "quantity", "definition", "status", "missing_input", "observable_link"])}

## Epsilon_A Bound Update

{md_table(epsilon_a_update, ["bound_id", "quantity", "expression", "status", "blocking_issue"])}

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
    raise SystemExit(f"3046 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: G_ref lock exact but parent-unsigned; epsilon_Gref retained")
