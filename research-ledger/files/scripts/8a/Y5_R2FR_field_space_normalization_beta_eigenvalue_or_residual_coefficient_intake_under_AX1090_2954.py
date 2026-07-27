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

CHECKPOINT = "2954"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2954-Y5-R2FR-field-space-normalization-beta-eigenvalue-or-residual-coefficient-intake-under-AX1090.md"

SRC_2953_DOC = ROOT / "2953-Y5-R2FR-positive-physical-X-Hessian-source-pack-or-residual-demotion-under-AX1090.md"
SRC_2953_NEXT = RESIDUALS / "P8_Y5_R2FR_2953_NEXT_TARGET.csv"
SRC_2953_BETA = RESIDUALS / "P8_Y5_R2FR_2953_FIELD_SPACE_BETA_BLOCKER.csv"
SRC_2953_PACK = RESIDUALS / "P8_Y5_R2FR_2953_FINITE_RESIDUAL_SOURCE_PACK_QUEUE.csv"
SRC_617_DOC = ROOT / "617-Y5-R10-field-space-normalization-beta-eigenvalue-owner-or-no-pole-return.md"
SRC_617_FS = RESIDUALS / "P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv"
SRC_617_BETA = RESIDUALS / "P8_Y5_R10_617_BETA_EIGENVALUE_CANDIDATE_LEDGER.csv"
SRC_617_NOPOLE = RESIDUALS / "P8_Y5_R10_617_NO_POLE_RETURN_GATE.csv"
SRC_617_SUMMARY = RESIDUALS / "P8_Y5_R10_617_NONCLAIM_SUMMARY.csv"
SRC_616_XBLOCK = RESIDUALS / "P8_Y5_R10_616_PARENT_X_BLOCK_OWNER_CONTRACT.csv"
SRC_616_VACUUM = RESIDUALS / "P8_Y5_R10_616_VACUUM_OWNER_ATTEMPT.csv"
SRC_616_DEMOTION = RESIDUALS / "P8_Y5_R10_616_RANGE_CLOSURE_DEMOTION_GATE.csv"
SRC_614_CONTRACT = RESIDUALS / "P8_Y5_R10_614_PARENT_HESSIAN_CONTRACT.csv"
SRC_564_HESSIAN = RESIDUALS / "P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv"
SRC_1042_SOURCE_ZERO = RESIDUALS / "P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2954_SOURCE_REGISTER.csv",
    "law": RESIDUALS / "P8_Y5_R2FR_2954_FIELD_SPACE_LAW_AUDIT.csv",
    "beta": RESIDUALS / "P8_Y5_R2FR_2954_BETA_EIGENVALUE_TARGET_LEDGER.csv",
    "intake": RESIDUALS / "P8_Y5_R2FR_2954_RESIDUAL_COEFFICIENT_INTAKE_ROWS.csv",
    "route": RESIDUALS / "P8_Y5_R2FR_2954_ROUTE_SELECTION_AFTER_BETA_FAILURE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2954_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2954_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2954_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2954_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2954_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "law_copy": PARENT_ACTION / "field_space_law_audit_2954_NONCLAIM.csv",
    "beta_copy": PARENT_ACTION / "beta_eigenvalue_target_ledger_2954_NONCLAIM.csv",
    "intake_copy": LOCAL_BOUNDS / "residual_coefficient_intake_rows_2954_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2954_SOURCE_ZERO_OR_FIRST_RESIDUAL_COEFFICIENT_ROW_NEXT_NONCLAIM.csv",
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
        ("SRC2954_00_2953_doc", SRC_2953_DOC, "NEXT2953_0_2954;Validation overall: `True`", "2953 handoff"),
        ("SRC2954_01_2953_next", SRC_2953_NEXT, "NEXT2953_0_2954", "machine-readable 2954 target"),
        ("SRC2954_02_2953_beta", SRC_2953_BETA, "BETA2953_1_field_metric;BETA2953_4_verdict", "2953 beta blocker"),
        ("SRC2954_03_2953_pack", SRC_2953_PACK, "PACK2953_0_ZX;PACK2953_11_alphaX", "2953 residual source-pack queue"),
        ("SRC2954_04_617_doc", SRC_617_DOC, "Status: `Y5_R10_field_space_normalization_law_derived_conditionally;beta_eff = U''(0) rho_vac^(1/2)/(Z_X f_X^2)`", "617 field-space derivation"),
        ("SRC2954_05_617_fs", SRC_617_FS, "FS617_0_exact_second_variation;FS617_5_finite_branch_ceiling", "field-space normalization attempt"),
        ("SRC2954_06_617_beta", SRC_617_BETA, "BS617_1_beta3;BS617_5_direct_38p6_backsolve", "beta eigenvalue targets"),
        ("SRC2954_07_617_nopole", SRC_617_NOPOLE, "NP617_0_finite_branch_status;NP617_3_residual_bound_fallback", "post-beta route gate"),
        ("SRC2954_08_617_summary", SRC_617_SUMMARY, "Y5_R10_field_space_normalization_law_derived_conditionally;no_pole_or_source_zero_certificate", "617 nonclaim summary"),
        ("SRC2954_09_616_xblock", SRC_616_XBLOCK, "PC616_2_field_space_metric_lock;PC616_3_beta_spectrum_lock", "field-space/beta owner contract"),
        ("SRC2954_10_616_vacuum", SRC_616_VACUUM, "VO616_3_field_space_normalization_blocker;VO616_4_beta_eff_invariant", "vacuum bridge blocker"),
        ("SRC2954_11_616_demotion", SRC_616_DEMOTION, "DG616_2_field_space_normalization_signed;DG616_5_no_R10_promotion", "range demotion gate"),
        ("SRC2954_12_614_contract", SRC_614_CONTRACT, "HC614_0_same_branch_Hessian;HC614_5_claim_wall", "Hessian source contract"),
        ("SRC2954_13_564_hessian", SRC_564_HESSIAN, "H564_1_ZX_extraction;H564_5_yukawa_or_zero_fork", "operator/range formula"),
        ("SRC2954_14_1042_source_zero", SRC_1042_SOURCE_ZERO, "SZ1042_0_matter_pullback;SZ1042_5_verdict", "source-zero channel audit"),
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


def law_rows() -> list[dict[str, Any]]:
    rows = [
        ("LAW2954_0_exact_second_variation", "finite-X range law", "S_X=int sqrt(h)[1/2 Z_X |grad X|^2 + rho_vac U(X/f_X)] -> M_X^2/Z_X=rho_vac U''(0)/(Z_X f_X^2)", "DERIVED_CONDITIONALLY", "617 derives the correct invariant law", True, False),
        ("LAW2954_1_beta_invariant", "beta_eff", "beta_eff=ell_vac^2 M_X^2/Z_X=U''(0) rho_vac^(1/2)/(Z_X f_X^2)", "INVARIANT_IDENTIFIED", "beta_eff is the only meaningful range selector", True, False),
        ("LAW2954_2_canonical_metric_contract", "Z_X f_X^2=rho_vac^(1/2)", "canonical vacuum field-space metric would make beta_eff=U''(0)", "CLEAN_CONTRACT_NOT_SIGNED", "no parent Ward/metric theorem fixes this product", True, False),
        ("LAW2954_3_rescaling_guard", "normalization guard", "X rescaling cannot change the physical product Z_X f_X^2 if the parent metric is real", "GUARDRAIL_PASS", "prevents fake beta wins from coordinate choice", True, False),
        ("LAW2954_4_existing_corpus_check", "existing metric owner", "parent M_AB/DeWitt/defect metric restricted to X direction", "NOT_FOUND", "nearby trace/flow pieces do not own the full X metric or cross-term policy", False, False),
        ("LAW2954_5_Upp0_owner", "U''(0) eigenvalue", "dimensionless Hessian eigenvalue is fixed before R10 comparison", "NOT_SIGNED", "beta=3 is a good target, not a derived number", False, False),
        ("LAW2954_6_verdict", "parent-owned lambda_X", "Z_X f_X^2 and U''(0) both parent-signed in the same branch", "LAMBDA_NOT_PARENT_OWNED", "finite short-range route remains closure-only", False, False),
    ]
    return [
        add_common(
            {
                "law_id": law_id,
                "object": obj,
                "formula_or_test": formula,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "owner_acquired": acquired,
            }
        )
        for law_id, obj, formula, status, evidence, conditional, acquired in rows
    ]


def beta_rows() -> list[dict[str, Any]]:
    rows = [
        ("B2954_0_beta1", "1", "single canonical X mode", "U''(0)=1", "88.078", "CONDITIONAL_NOT_SIGNED", "natural transition-band target"),
        ("B2954_1_beta3", "3", "spatial trace eigenvalue", "three equal spatial curvature channels", "50.852", "BEST_LOW_SCRUTINY_TARGET_NOT_SIGNED", "best finite theorem target if spatial trace owner closes"),
        ("B2954_2_beta4", "4", "four-block trace eigenvalue", "3+1 equal block if time participates", "44.039", "CONDITIONAL_NOT_SIGNED", "needs time-channel owner"),
        ("B2954_3_beta5", "5", "trace plus auxiliary stiffness", "trace block plus one/two auxiliary contributions", "39.390", "CANDIDATE_NOT_SIGNED", "numerically excellent but less clean than beta=3"),
        ("B2954_4_beta_direct", "5.206677", "direct 38.6um backsolve", "beta chosen to hit lambda=38.6um", "38.600", "FORBIDDEN_AS_DERIVATION", "closure-only unless independently reproduced"),
        ("B2954_5_verdict", "beta_eff", "parent eigenvalue/spectrum", "U''(0) or equivalent trace eigenvalue fixed before comparison", "MISSING", "BETA_EIGENVALUE_NOT_OWNED", "do not promote lambda_X prediction"),
    ]
    return [
        add_common(
            {
                "beta_id": beta_id,
                "beta_eff": beta,
                "candidate_owner_route": route,
                "eigenvalue_contract": contract,
                "lambda_um": lambda_um,
                "current_status": status,
                "interpretation": interpretation,
                "owner_acquired": False,
            }
        )
        for beta_id, beta, route, contract, lambda_um, status, interpretation in rows
    ]


def intake_rows() -> list[dict[str, Any]]:
    rows = [
        ("INT2954_0_ZX_metric", "Z_X", "parent field-space metric / kinetic residue", "operator_or_action_units", "parent-action", "MISSING_PARENT_METRIC"),
        ("INT2954_1_fX", "f_X", "field amplitude/decay scale or canonical normalization", "field_units", "parent-action", "MISSING_FIELD_SCALE"),
        ("INT2954_2_Zf_product", "Z_X f_X^2", "normalization-invariant product", "energy_density_sqrt_or_action_units", "parent-action", "MISSING_CANONICAL_METRIC_CONTRACT"),
        ("INT2954_3_Upp0", "U''(0)", "dimensionless potential/Hessian eigenvalue", "dimensionless", "parent-action", "MISSING_BETA_EIGENVALUE"),
        ("INT2954_4_rho_vac", "rho_vac", "parent-owned local vacuum extremum scale", "energy_density", "cosmology-parent", "NOT_PARENT_SIGNED_FOR_LOCAL_HESSIAN"),
        ("INT2954_5_beta_eff", "beta_eff", "U''(0) rho_vac^(1/2)/(Z_X f_X^2)", "dimensionless", "derived-after-inputs", "BLOCKED_BY_COMPONENTS"),
        ("INT2954_6_lambdaX", "lambda_X", "ell_vac/sqrt(beta_eff)", "length", "derived-after-inputs", "BLOCKED_BY_BETA_EFF"),
        ("INT2954_7_KX", "K_X(lambda)", "force-law Green kernel normalization", "force_normalization", "arena-projection", "MISSING_ARENA_PROJECTION"),
        ("INT2954_8_Qbar_XH", "Qbar_XH(lambda)", "source charge per same-frame M_H_ref", "dimensionless", "source-normalization", "MISSING_SOURCE_CHARGE_AND_MHREF"),
        ("INT2954_9_qbar_XT", "qbar_XT(lambda)", "test/material/clock charge", "dimensionless", "matter-test", "MISSING_TEST_CHARGE"),
        ("INT2954_10_tail_abs", "absolute source/boundary tails", "J_boundary + J_projector + J_memory + Phi_boundary + PiM tails", "dimensionless_after_normalization", "residual-tail", "MISSING_ABSOLUTE_TAIL_BOUNDS"),
        ("INT2954_11_alphaX", "alpha_X(lambda)", "K_X Qbar_XH qbar_XT plus no-cancellation tails", "dimensionless", "derived-after-inputs", "NOT_SCORE_READY"),
    ]
    return [
        add_common(
            {
                "intake_id": intake_id,
                "symbol": symbol,
                "required_payload": payload,
                "units": units,
                "source_family": family,
                "current_status": status,
                "numeric_or_theorem_value": "MISSING",
                "source_path": "MISSING",
                "source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for intake_id, symbol, payload, units, family, status in rows
    ]


def route_rows() -> list[dict[str, Any]]:
    rows = [
        ("ROUTE2954_0_field_space", "field-space/beta derivation", "best finite prediction route if Z_X f_X^2 and U''(0) become parent-signed", "FAILED_CURRENT_OWNER", "keep as theorem target, not claim"),
        ("ROUTE2954_1_source_zero", "positive source-zero no-hair", "best physical-X local-GR route if source/boundary channels vanish", "SELECT_NEXT_DERIVATION_ROUTE", "attack J_X/Phi zeros before empirical scoring"),
        ("ROUTE2954_2_coefficient_intake", "finite empirical residual", "fallback if source-zero fails; use 2954 intake rows", "READY_AS_NONCLAIM_QUEUE", "fill real source-backed rows before tests"),
        ("ROUTE2954_3_no_pole", "quotient/vertical no-pole", "still strongest if new parent q/v certificate appears", "NOT_RERUN_NOW", "do not circle the same failed certificate"),
        ("ROUTE2954_4_verdict", "route selection", "beta owner failed; next try source-zero channel proof, with coefficient intake as fallback", "SOURCE_ZERO_NEXT", "advance GR reduction before scoring"),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "route": route,
                "role": role,
                "current_status": status,
                "next_action": action,
            }
        )
        for route_id, route, role, status, action in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2954_0_field_metric", "Z_X f_X^2 parent-owned", False, "FIELD_SPACE_METRIC_NOT_SIGNED"),
        ("CG2954_1_beta", "U''(0)/beta_eff parent-owned", False, "BETA_EIGENVALUE_NOT_SIGNED"),
        ("CG2954_2_lambda", "lambda_X predicted", False, "LAMBDA_CLOSURE_ONLY"),
        ("CG2954_3_residual_rows", "finite residual coefficient rows score-ready", False, "INTAKE_ROWS_MISSING_VALUES"),
        ("CG2954_4_source_zero", "source-zero/no-hair closes", False, "SOURCE_ZERO_NOT_DERIVED"),
        ("CG2954_5_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2954_6_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
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
        ("DEC2954_0_result", "field-space law derived conditionally but not parent-owned", "617 supplies the exact invariant formula, but no source fixes Z_X f_X^2 or U''(0)", "keep lambda_X nonclaim"),
        ("DEC2954_1_beta3", "beta=3 remains the best low-scrutiny finite theorem target", "it could follow from a spatial trace eigenvalue and gives lambda_X around 50.85 um", "do not call beta=3 derived"),
        ("DEC2954_2_intake", "convert residual fallback into explicit coefficient-intake rows", "if source-zero fails, empirical tests need Z, f, beta, lambda, K, Qbar, qbar and tail inputs with units and source paths", "fill rows only from real parent/source evidence"),
        ("DEC2954_3_route", "next attack should be source-zero channel proof, not R10 scoring", "local-GR reduction wants X silent, not merely short-ranged by closure", "build 2955 J_X/Phi/source-zero proof or first bounded coefficient row"),
        ("DEC2954_4_claim_ceiling", "no local-GR/R10/WEP/PPN/public claim", "all decisive payloads are still missing or conditional", "private framework discipline only"),
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
                "next_id": "NEXT2954_0_2955",
                "priority": "selected_primary",
                "next_doc": "2955-Y5-R2FR-JX-Phi-source-zero-proof-or-first-residual-coefficient-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_JX_Phi_source_zero_proof_or_first_residual_coefficient_row_under_AX1090_2955.py",
                "objective": "Try to prove the physical-X source-zero/right-hand-side-zero condition channelwise: J_matter, boundary/Phi, projector/domain, memory/history, source normalization and PiM tails. If any channel remains open, fill the first nonclaim residual coefficient row from the 2954 intake queue with real units and source path.",
                "include": "J_X channel split;matter pullback;Phi_boundary_local;projector/domain source;memory source;source normalization;PiM tail;absolute no-cancellation row;units;source paths",
                "exclude": "quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;EH-only substitution;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("law_copy", OUTPUTS["law"], BRANCH_OUTPUTS["law_copy"]),
        ("beta_copy", OUTPUTS["beta"], BRANCH_OUTPUTS["beta_copy"]),
        ("intake_copy", OUTPUTS["intake"], BRANCH_OUTPUTS["intake_copy"]),
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
        ("VAL2954_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2954_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2954_2_law_conditional", any(row["law_id"] == "LAW2954_6_verdict" and row["owner_acquired"] is False for row in all_rows["law"]), "field-space law verdict is conditional/not owned", True),
        ("VAL2954_3_beta_not_claimed", all(row["owner_acquired"] is False for row in all_rows["beta"]), "beta target rows remain nonclaim", True),
        ("VAL2954_4_intake_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["intake"]), "residual coefficient intake rows remain nonclaim", True),
        ("VAL2954_5_source_zero_next", any(row["route_id"] == "ROUTE2954_4_verdict" and row["current_status"] == "SOURCE_ZERO_NEXT" for row in all_rows["route"]), "source-zero route selected next", True),
        ("VAL2954_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates are blocked", True),
        ("VAL2954_7_next_target_written", any(row["next_id"] == "NEXT2954_0_2955" for row in all_rows["next"]), "2955 next target selected", True),
        ("VAL2954_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2954_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2954_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2954_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2954 outputs were written to formalization-workbench", True),
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
                "validation_id": "VAL2954_OVERALL",
                "passed": overall,
                "check": "2954 validation overall",
                "required": True,
            }
        )
    )
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2954 - Y5 R2FR: field-space normalization beta eigenvalue or residual coefficient intake under AX1090

Status: `Y5_R2FR_2954_field_space_law_conditional_beta_not_owned_residual_intake_rows_emitted_source_zero_next`

Claim ceiling: `no_field_metric_owner_no_beta_eigenvalue_no_lambda_prediction_no_residual_score_no_source_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2954 asks whether the finite physical-`X` range can be promoted from a closure target to a parent-owned prediction. The answer is disciplined:

- The exact field-space law is already derived conditionally: `beta_eff=U''(0) rho_vac^(1/2)/(Z_X f_X^2)`.
- The promotion fails because current MTS does not parent-own `Z_X f_X^2` or the eigenvalue `U''(0)`.
- `beta=3` remains the cleanest low-scrutiny theorem target, but not evidence; direct `38.6 um` backsolving remains closure-only.
- The finite residual fallback is now an explicit intake queue, not a score: every row still needs numeric/theorem value, units, source path, and no-cancellation provenance.
- The next derivation should attack physical-`X` source-zero/right-hand-side-zero channelwise before any R10/PPN scoring.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Field-Space Law Audit

{md_table(all_rows["law"], ["law_id", "object", "current_status", "conditional_math_available", "owner_acquired", "evidence_summary"])}

## Beta Eigenvalue Target Ledger

{md_table(all_rows["beta"], ["beta_id", "beta_eff", "candidate_owner_route", "lambda_um", "current_status", "owner_acquired"])}

## Residual Coefficient Intake Rows

{md_table(all_rows["intake"], ["intake_id", "symbol", "current_status", "numeric_or_theorem_value", "units", "accepted_for_scoring"])}

## Route Selection After Beta Failure

{md_table(all_rows["route"], ["route_id", "route", "current_status", "next_action"])}

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
        "law": law_rows(),
        "beta": beta_rows(),
        "intake": intake_rows(),
        "route": route_rows(),
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

    print(f"2954 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
