from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2953"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2953-Y5-R2FR-positive-physical-X-Hessian-source-pack-or-residual-demotion-under-AX1090.md"

SRC_2952_DOC = ROOT / "2952-Y5-R2FR-parent-X-no-pole-quotient-or-vertical-generator-proof-under-AX1090.md"
SRC_2952_NEXT = RESIDUALS / "P8_Y5_R2FR_2952_NEXT_TARGET.csv"
SRC_2952_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2952_PHYSICAL_X_DEMOTION_AND_SOURCE_PACK_ROUTE.csv"
SRC_2951_COEFF = RESIDUALS / "P8_Y5_R2FR_2951_ZX_MX2_SOURCE_ROW_ATTEMPT.csv"
SRC_564_HESSIAN = RESIDUALS / "P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv"
SRC_564_SOURCE_ZERO = RESIDUALS / "P8_Y5_R10_564_SOURCE_ZERO_THEOREM_ATTEMPT.csv"
SRC_614_CONTRACT = RESIDUALS / "P8_Y5_R10_614_PARENT_HESSIAN_CONTRACT.csv"
SRC_614_ATTEMPT = RESIDUALS / "P8_Y5_R10_614_HESSIAN_DERIVATION_ATTEMPT.csv"
SRC_615_XBLOCK = RESIDUALS / "P8_Y5_R10_615_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv"
SRC_616_XBLOCK = RESIDUALS / "P8_Y5_R10_616_PARENT_X_BLOCK_OWNER_CONTRACT.csv"
SRC_616_VACUUM = RESIDUALS / "P8_Y5_R10_616_VACUUM_OWNER_ATTEMPT.csv"
SRC_616_DEMOTION = RESIDUALS / "P8_Y5_R10_616_RANGE_CLOSURE_DEMOTION_GATE.csv"
SRC_1042_IDENTITY = RESIDUALS / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv"
SRC_1042_PREMISE = RESIDUALS / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv"
SRC_1042_SOURCE_ZERO = RESIDUALS / "P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv"
SRC_1042_BOUNDARY = RESIDUALS / "P8_Y5_R10_1042_BOUNDARY_FLUX_PRIOR_FIRST_FILL.csv"
SRC_ENERGY_IDENTITY = RESIDUALS / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2953_SOURCE_REGISTER.csv",
    "hessian": RESIDUALS / "P8_Y5_R2FR_2953_POSITIVE_X_HESSIAN_THEOREM_AUDIT.csv",
    "premises": RESIDUALS / "P8_Y5_R2FR_2953_NOHAIR_PREMISE_STATUS.csv",
    "beta": RESIDUALS / "P8_Y5_R2FR_2953_FIELD_SPACE_BETA_BLOCKER.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_2953_FINITE_RESIDUAL_SOURCE_PACK_QUEUE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2953_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2953_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2953_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2953_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2953_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hessian_copy": PARENT_ACTION / "positive_X_Hessian_theorem_audit_2953_NONCLAIM.csv",
    "source_pack_copy": LOCAL_BOUNDS / "finite_X_residual_source_pack_queue_2953_NONCLAIM.csv",
    "beta_copy": PARENT_ACTION / "field_space_beta_blocker_2953_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2953_FIELD_SPACE_BETA_OR_RESIDUAL_COEFFICIENT_INTAKE_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2953_00_2952_doc", SRC_2952_DOC, "NEXT2952_0_2953;Validation overall: `True`", "2952 physical-X handoff"),
        ("SRC2953_01_2952_next", SRC_2952_NEXT, "NEXT2952_0_2953", "machine-readable 2953 target"),
        ("SRC2953_02_2952_demotion", SRC_2952_DEMOTION, "DEM2952_0_physical_X_selected;DEM2952_4_next", "physical X route selected"),
        ("SRC2953_03_2951_coeff", SRC_2951_COEFF, "COEFF2951_0_ZX_formula;COEFF2951_5_candidate_row", "prior Z/M source row attempt"),
        ("SRC2953_04_564_hessian", SRC_564_HESSIAN, "H564_0_parent_expansion;H564_5_yukawa_or_zero_fork", "Hessian extraction formulas"),
        ("SRC2953_05_564_source_zero", SRC_564_SOURCE_ZERO, "SZ564_0_stationary_branch;SZ564_5_verdict", "source-zero theorem attempt"),
        ("SRC2953_06_614_contract", SRC_614_CONTRACT, "HC614_0_same_branch_Hessian;HC614_5_claim_wall", "parent Hessian contract"),
        ("SRC2953_07_614_attempt", SRC_614_ATTEMPT, "HA614_0_second_variation;HA614_3_numeric_ratio", "Hessian derivation attempt"),
        ("SRC2953_08_615_xblock", SRC_615_XBLOCK, "XB615_0_minimal_bridge_block;XB615_4_no_pole_escape", "explicit X-block bridge contract"),
        ("SRC2953_09_616_xblock", SRC_616_XBLOCK, "PC616_0_same_branch_second_variation;PC616_5_no_pole_fallback", "parent X-block owner contract"),
        ("SRC2953_10_616_vacuum", SRC_616_VACUUM, "VO616_0_vacuum_scale_definition;VO616_5_no_posthoc_gate", "vacuum/field-space owner attempt"),
        ("SRC2953_11_616_demotion", SRC_616_DEMOTION, "DG616_0_rho_vac_parent_owned;DG616_5_no_R10_promotion", "range-closure demotion gate"),
        ("SRC2953_12_1042_identity", SRC_1042_IDENTITY, "NH1042_1_energy_identity;NH1042_5_verdict", "positive no-hair identity"),
        ("SRC2953_13_1042_premise", SRC_1042_PREMISE, "NHP1042_0_LX_owner;NHP1042_6_verdict", "no-hair premise gates"),
        ("SRC2953_14_1042_source_zero", SRC_1042_SOURCE_ZERO, "SZ1042_0_matter_pullback;SZ1042_5_verdict", "source-zero channel audit"),
        ("SRC2953_15_1042_boundary", SRC_1042_BOUNDARY, "PBF1042_0_Phi_boundary_local_definition;PBF1042_2_numeric_prior_route", "boundary-flux prior fill"),
        ("SRC2953_16_energy_identity", SRC_ENERGY_IDENTITY, "E506_scalar_positive_operator;E506_boundary_topological_silence", "generic positive operator identities"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def hessian_rows() -> list[dict[str, Any]]:
    rows = [
        ("HX2953_0_parent_expansion", "parent quadratic expansion", "S_parent=S0+int E_X|0 deltaX + 1/2 int[H_grad nablaX nablaX - H_0 X^2]+...", "EXACT_DEFINITION_CONDITIONAL", "564 gives the correct extraction definition", True, False),
        ("HX2953_1_quadratic_operator", "positive physical X operator", "L_X=(-Z_X Delta + M_X^2) with source J_X", "FORMAL_OPERATOR_DERIVED", "564/614 derive the operator form but not parent coefficients", True, False),
        ("HX2953_2_ZX", "kinetic residue Z_X", "Z_X=(1/3)h_{mu nu}H_grad^{mu nu} or equivalent A_X^ij in local isotropic branch", "FORMULA_ONLY_NOT_PARENT_SIGNED", "2951 and 1042 keep sign and field normalization unsigned", True, False),
        ("HX2953_3_MX2", "mass curvature M_X^2", "M_X^2=H_0 in the sign convention E_X=(-Z_X Delta+M_X^2)X-J_X", "FORMULA_ONLY_NOT_PARENT_SIGNED", "2951 and 1042 keep gap, units and zero-mode policy unsigned", True, False),
        ("HX2953_4_lambda", "range law", "lambda_X=sqrt(Z_X/M_X^2)", "CONDITIONAL_LAW_DERIVED_RATIO_MISSING", "614 derives the law; Z/M ratio is not parent-owned", True, False),
        ("HX2953_5_vacuum_bridge", "vacuum-scale finite target", "M_X^2/Z_X=beta_eff/ell_vac^2; beta_eff~3..5 would give a short forgiving band", "PROMISING_BRIDGE_CLOSURE_ONLY", "615/616 show the scale scent but field-space normalization and beta eigenvalue are not signed", True, False),
        ("HX2953_6_positive_claim", "Z_X>0 and M_X^2>0", "same-branch second variation gives positive elliptic operator and positive gap", "SIGN_GATE_UNFILLED", "614/1042 mark positivity necessary but not evaluated", False, False),
        ("HX2953_7_verdict", "positive Hessian source pack", "parent L_X, field normalization, Z sign, M gap, range and source clauses all pass together", "HESSIAN_PACK_NOT_ACQUIRED", "conditional formulas are real; claim-grade parent payload is still missing", False, False),
    ]
    return [
        add_common(
            {
                "hessian_id": hessian_id,
                "object": obj,
                "formula_or_requirement": formula,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "accepted_for_scoring": accepted,
            }
        )
        for hessian_id, obj, formula, status, evidence, conditional, accepted in rows
    ]


def premise_rows() -> list[dict[str, Any]]:
    rows = [
        ("PREM2953_0_LX_owner", "parent L_X selected", "explicit S_X with field normalization and boundary class", "MISSING_PARENT_LX", "energy identity remains a template", False),
        ("PREM2953_1_branch_extremum", "E_X|0=0", "local branch is an extremum; no tadpole", "CONDITIONAL_NOT_PARENT_FILLED", "X has a local tadpole if not closed", False),
        ("PREM2953_2_Z_positive", "Z_X>0", "second variation fixes positive kinetic residue", "FORMULA_ONLY_NOT_PARENT_SIGNED", "ghost/anti-elliptic mode can evade no-hair", False),
        ("PREM2953_3_M_gap", "M_X^2>0", "same-branch Hessian gives positive mass gap and no flat zero mode", "FORMULA_ONLY_NOT_PARENT_SIGNED", "massless/topological/long-range X can remain", False),
        ("PREM2953_4_JX_zero", "J_X=0 channelwise", "matter, constants, boundary, projector, domain and memory source channels vanish by parent identity", "SOURCE_ZERO_NOT_DERIVED", "physical X is sourced and must be scored", False),
        ("PREM2953_5_Phi_boundary_zero", "Phi_boundary_local=0", "boundary flux, source worldtube, reference subtraction and corners vanish or are bounded", "BOUNDARY_FLUX_ZERO_NOT_DERIVED", "alpha3/R10 boundary residual remains active", False),
        ("PREM2953_6_no_kernel", "zero-mode/topology policy", "kernel is quotient/proper or fixed by boundary/reference data", "TOPOLOGY_KERNEL_GATE_OPEN", "positive norm may kill only nonzero modes", False),
        ("PREM2953_7_nohair_verdict", "positive physical X no-hair", "PREM2953_0 through PREM2953_6 all pass", "NOHAIR_NOT_PARENT_SIGNED", "finite residual branch remains live", False),
    ]
    return [
        add_common(
            {
                "premise_id": premise_id,
                "premise": premise,
                "required_test": required,
                "current_status": status,
                "if_missing": if_missing,
                "premise_pass": passed,
            }
        )
        for premise_id, premise, required, status, if_missing, passed in rows
    ]


def beta_rows() -> list[dict[str, Any]]:
    rows = [
        ("BETA2953_0_rho_vac", "rho_vac owner", "parent vacuum/cosmology action fixes rho_vac as a local Hessian scale before local bound comparison", "NOT_SIGNED", "rho_vac is a useful dimensional input but not yet a parent-owned local curvature"),
        ("BETA2953_1_field_metric", "field-space normalization", "Z_X f_X^2 or equivalent parent field metric fixes how a potential height becomes M_X^2/Z_X", "MISSING_HARD_BLOCKER", "without this, beta_eff can float by normalization"),
        ("BETA2953_2_beta_eigenvalue", "beta_eff owner", "beta_eff is an eigenvalue/trace/regularity index declared before R10", "CANDIDATE_NUMBERS_ONLY", "beta 3..5 is a target, not evidence"),
        ("BETA2953_3_lambda_prediction", "lambda_X prediction", "lambda_X=ell_vac/sqrt(beta_eff) after rho_vac, field metric and beta all close", "RANGE_CLOSURE_ONLY", "short-range bridge remains nonclaim"),
        ("BETA2953_4_verdict", "field-space/beta lock", "BETA2953_0 through BETA2953_2 close in one branch", "NOT_ACQUIRED", "finite short-range route cannot be promoted"),
    ]
    return [
        add_common(
            {
                "beta_id": beta_id,
                "object": obj,
                "required_owner": required,
                "current_status": status,
                "blocker": blocker,
                "owner_acquired": False,
            }
        )
        for beta_id, obj, required, status, blocker in rows
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("PACK2953_0_ZX", "Z_X / A_X^ij", "kinetic/operator normalization and sign certificate", "operator_or_action_units", "MISSING_PARENT_SIGNED_VALUE"),
        ("PACK2953_1_MX2", "M_X^2", "mass/gap/range term with zero-mode policy", "inverse_length_squared_or_action_units", "MISSING_PARENT_SIGNED_VALUE"),
        ("PACK2953_2_lambdaX", "lambda_X", "sqrt(Z_X/M_X^2) in one normalization", "length", "BLOCKED_BY_ZX_MX2"),
        ("PACK2953_3_KX", "K_X(lambda)", "Green-function/force-law kernel normalization", "force_normalization", "MISSING_ARENA_PROJECTION"),
        ("PACK2953_4_Qbar_XH", "Qbar_XH(lambda)", "source charge per positive same-frame M_H_ref", "dimensionless", "MISSING_SOURCE_CHARGE_AND_MHREF"),
        ("PACK2953_5_qbar_XT", "qbar_XT(lambda)", "test-body/material/clock charge under X", "dimensionless", "MISSING_TEST_CHARGE"),
        ("PACK2953_6_J_matter", "J_matter", "ordinary matter pullback source for X", "source_current", "MISSING_MATTER_PULLBACK_ZERO_OR_VALUE"),
        ("PACK2953_7_J_boundary", "J_boundary / Phi_boundary_local", "boundary/source-worldtube flux or theorem-zero", "charge_or_flux", "MISSING_BOUNDARY_ZERO_OR_VALUE"),
        ("PACK2953_8_J_projector_domain", "J_projector_domain", "projector/domain selector source current", "source_current", "MISSING_PROJECTOR_DOMAIN_ZERO_OR_VALUE"),
        ("PACK2953_9_J_memory", "J_memory", "memory/history kernel source current", "source_current", "MISSING_MEMORY_ZERO_OR_VALUE"),
        ("PACK2953_10_MHref", "M_H_ref", "positive same-frame source denominator", "mass_or_charge", "MISSING_STABLE_MH_REF"),
        ("PACK2953_11_alphaX", "alpha_X(lambda_X)", "K_X Qbar_XH qbar_XT plus absolute tails", "dimensionless", "NOT_SCORE_READY_COMPONENTS_MISSING"),
    ]
    return [
        add_common(
            {
                "pack_id": pack_id,
                "symbol": symbol,
                "required_payload": required,
                "units": units,
                "current_status": status,
                "numeric_or_theorem_value": "MISSING",
                "source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for pack_id, symbol, required, units, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2953_0_parent_LX", "parent L_X selected", False, "MISSING_PARENT_LX"),
        ("CG2953_1_ZM_positive", "Z_X>0 and M_X^2>0 parent-signed", False, "HESSIAN_SIGNS_UNSIGNED"),
        ("CG2953_2_JX_zero", "J_X=0 channelwise", False, "SOURCE_ZERO_NOT_DERIVED"),
        ("CG2953_3_boundary_zero", "Phi_boundary_local=0", False, "BOUNDARY_FLUX_ZERO_NOT_DERIVED"),
        ("CG2953_4_nohair", "positive physical X no-hair closes", False, "NOHAIR_NOT_PARENT_SIGNED"),
        ("CG2953_5_finite_residual", "finite residual source pack score-ready", False, "SOURCE_PACK_COMPONENTS_MISSING"),
        ("CG2953_6_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2953_7_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2953_0_result", "positive physical X Hessian route is conditional, not claimed", "the operator/no-hair mathematics is clean, but parent L_X, field normalization, signs, source-zero, boundary-zero and kernel gates remain unsigned", "keep all rows nonclaim"),
        ("DEC2953_1_best_gain", "the finite branch source-pack queue is now explicit", "if no-hair fails, the theory must carry real Z/M/K/Q/q/source/boundary/MHref values into empirical tests", "do not score placeholders"),
        ("DEC2953_2_key_blocker", "field-space normalization and beta owner are the next highest-leverage physical-X blockers", "rho_vac alone does not determine lambda_X; Z_X f_X^2 and beta_eff must be parent-owned", "attack the field-space/beta lock before R10 scoring"),
        ("DEC2953_3_local_GR_status", "local GR reduction still not derived", "finite-range survival or nice lambda pressure is not the same thing as proving GR/Newton recovery", "no local-GR, R10, WEP, PPN or public claim"),
        ("DEC2953_4_next", "build 2954 field-space normalization beta-eigenvalue or residual coefficient intake", "this either promotes the finite branch into a real parent range target or forces explicit empirical residual inputs", "derive/source Z_X f_X^2, U''(0), beta_eff, lambda_X and first component bounds"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2953_0_2954",
                "priority": "selected_primary",
                "next_doc": "2954-Y5-R2FR-field-space-normalization-beta-eigenvalue-or-residual-coefficient-intake-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_field_space_normalization_beta_eigenvalue_or_residual_coefficient_intake_under_AX1090_2954.py",
                "objective": "Try to derive or source the physical-X field-space normalization and beta_eff eigenvalue that would turn the vacuum-scale bridge into a parent-owned lambda_X. If this fails, convert the 2953 source-pack queue into explicit nonclaim coefficient-intake rows for empirical testing.",
                "include": "Z_X field metric;f_X or canonical normalization;U''(0);rho_vac owner;beta_eff;lambda_X;component coefficient-intake rows;no-cancellation policy;source paths;units",
                "exclude": "quotient/vertical no-pole rerun;claiming beta 3..5;direct lambda closure as prediction;alpha(lambda) scoring;I_X scoring;EH-only substitution;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("hessian_copy", OUTPUTS["hessian"], BRANCH_OUTPUTS["hessian_copy"]),
        ("source_pack_copy", OUTPUTS["source_pack"], BRANCH_OUTPUTS["source_pack_copy"]),
        ("beta_copy", OUTPUTS["beta"], BRANCH_OUTPUTS["beta_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2953_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2953_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2953_2_hessian_conditional", any(row["hessian_id"] == "HX2953_7_verdict" and row["accepted_for_scoring"] is False for row in all_rows["hessian"]), "Hessian audit is conditional and not score-ready", True),
        ("VAL2953_3_nohair_blocked", any(row["premise_id"] == "PREM2953_7_nohair_verdict" and row["premise_pass"] is False for row in all_rows["premises"]), "no-hair premise verdict is blocked", True),
        ("VAL2953_4_beta_blocker_emitted", any(row["beta_id"] == "BETA2953_4_verdict" and row["owner_acquired"] is False for row in all_rows["beta"]), "field-space/beta blocker is emitted", True),
        ("VAL2953_5_source_pack_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["source_pack"]), "finite residual source-pack queue remains nonclaim", True),
        ("VAL2953_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates are blocked", True),
        ("VAL2953_7_next_target_written", any(row["next_id"] == "NEXT2953_0_2954" for row in all_rows["next"]), "2954 next target selected", True),
        ("VAL2953_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2953_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2953_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2953_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2953 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2953_OVERALL",
                "passed": overall,
                "check": "2953 validation overall",
                "required": True,
            }
        )
    )
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2953 - Y5 R2FR: positive physical X Hessian source-pack or residual demotion under AX1090

Status: `Y5_R2FR_2953_positive_physical_X_conditional_nohair_not_parent_signed_finite_source_pack_queue_emitted`

Claim ceiling: `no_parent_LX_no_ZX_sign_no_MX2_gap_no_JX_zero_no_boundary_zero_no_nohair_no_lambda_prediction_no_alpha_score_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2953 treats `X` as physical until proven otherwise, as selected by 2952. The result is:

- The conditional physical-X mathematics is good: second variation gives the right operator form, `lambda_X=sqrt(Z_X/M_X^2)`, and the positive no-hair identity is clean.
- The theory still does not own the physical payload: parent `L_X`, field normalization, `Z_X>0`, `M_X^2>0`, `J_X=0`, `Phi_boundary=0`, and zero-mode policy remain unsigned.
- The vacuum-scale bridge remains a useful theorem target, not a prediction: `rho_vac` alone does not determine `lambda_X`; field-space normalization and `beta_eff` must be derived.
- The honest fallback is now explicit: if no-hair fails, MTS needs source-backed finite residual rows before any R10/WEP/PPN/clock/orbital scoring.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Positive X Hessian Theorem Audit

{md_table(all_rows["hessian"], ["hessian_id", "object", "current_status", "conditional_math_available", "accepted_for_scoring", "evidence_summary"])}

## No-Hair Premise Status

{md_table(all_rows["premises"], ["premise_id", "premise", "current_status", "premise_pass", "if_missing"])}

## Field-Space Beta Blocker

{md_table(all_rows["beta"], ["beta_id", "object", "current_status", "owner_acquired", "blocker"])}

## Finite Residual Source-Pack Queue

{md_table(all_rows["source_pack"], ["pack_id", "symbol", "current_status", "numeric_or_theorem_value", "units", "accepted_for_scoring"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "hessian": hessian_rows(),
        "premises": premise_rows(),
        "beta": beta_rows(),
        "source_pack": source_pack_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2953 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
