from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1527-Y5-phi-owner-and-current-Khat-symbol-match-source-hunt.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "route_contract": ROOT / "01-motion-load-route-contract.md",
    "local_gr_reduction": ROOT / "02-motion-load-local-GR-reduction.md",
    "lambda_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "lambda_origin": ROOT / "08-phase-volume-reciprocity-origin.md",
    "1009_doc": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1526_doc": ROOT / "1526-Y5-tracefree-Hessian-improvement-action-coefficient-and-symbol-match.md",
    "1526_validation": OUT / "P8_Y5_BRR545_1526_VALIDATION.csv",
    "1526_variation": OUT / "P8_Y5_PARENT_QLOC_1526_VARIATION_DERIVATION.csv",
    "1526_contract": OUT / "P8_Y5_PARENT_QLOC_1526_COEFFICIENT_SIGN_CONTRACT.csv",
    "1526_symbol": OUT / "P8_Y5_PARENT_QLOC_1526_SYMBOL_MATCH_AUDIT.csv",
    "1526_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1526_CLAIM_GATE.csv",
    "1526_next": OUT / "P8_Y5_PARENT_QLOC_1526_NEXT_TARGET.csv",
    "1287_khat": OUT / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
    "1287_deltak": OUT / "P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "gk_evidence": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "gk_candidates": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
    "gk_gates": OUT / "P8_GK_STRESS_ACTION_GATE_TESTS.csv",
    "gamma_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1527_SOURCE_REGISTER.csv"
PHI_SOURCE_HUNT = OUT / "P8_Y5_PARENT_QLOC_1527_PHI_OWNER_SOURCE_HUNT.csv"
AUX_ACTION = OUT / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv"
MULTIPLIER_GATE = OUT / "P8_Y5_PARENT_QLOC_1527_MULTIPLIER_STRESS_SILENCE_GATE.csv"
KHAT_ADOPTION = OUT / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv"
NONLOCALITY_GUARD = OUT / "P8_Y5_PARENT_QLOC_1527_NONLOCALITY_GUARD.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1527_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1527_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1527_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1527_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1527_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1527_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1527"
QUAR_HUNT = QUARANTINE / "PHI_OWNER_SOURCE_HUNT_NONCLAIM.csv"
QUAR_AUX = QUARANTINE / "LOCAL_AUXILIARY_ACTION_CONTRACT_NONCLAIM.csv"
QUAR_KHAT = QUARANTINE / "KHAT_ADOPTION_ROW_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_HUNT = BRANCH_RESIDUALS / "phi_owner_source_hunt_nonclaim_1527.csv"
BRANCH_AUX = BRANCH_RESIDUALS / "local_auxiliary_phi_action_contract_nonclaim_1527.csv"
BRANCH_KHAT = BRANCH_RESIDUALS / "khat_adoption_row_nonclaim_1527.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "phi_owner_decision_nonclaim_1527.csv"


def flags() -> dict[str, bool]:
    return {
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


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


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


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1527_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for phi owner and current Khat symbol-match source hunt",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def phi_source_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PHH1527_0_box_phi_source",
            "Box phi=(2/3)(Gamma_eff+C)",
            "formal source relation exists in the K_L candidate row",
            "SOURCE_RELATION_EXISTS",
            "relation alone does not say whether phi is local, auxiliary, or inverse-Box",
            source_list("1287_khat", "1526_variation"),
        ),
        (
            "PHH1527_1_existing_phi_owner",
            "live phi parent action",
            "source hunt found no existing row that makes phi a parent-owned auxiliary field",
            "MISSING_LIVE_PHI_OWNER",
            "cannot promote local field-theory route without an owner",
            source_list("route_contract", "local_gr_reduction", "gamma_owner"),
        ),
        (
            "PHH1527_2_constraint_precedent",
            "lambda-style constraint precedent",
            "older corpus contains lambda_R/constraint-style parent discussions, useful as a pattern but not a phi proof",
            "PRECEDENT_ONLY",
            "lambda_R precedent cannot be imported as phi ownership",
            source_list("lambda_constraint", "lambda_origin"),
        ),
        (
            "PHH1527_3_nonlocal_risk",
            "inverse-Box phi",
            "taking phi=Box^{-1}[2/3(Gamma_eff+C)] without an auxiliary action would make the route nonlocal",
            "NONLOCAL_RISK_IDENTIFIED",
            "must be marked nonlocal/closure-only or replaced by local auxiliary action",
            source_list("1526_contract", "1526_claim_gate"),
        ),
        (
            "PHH1527_4_verdict",
            "phi owner source hunt",
            "no existing live phi owner found; construct a local auxiliary contract as nonclaim candidate",
            "SOURCE_HUNT_FAILS_CONTRACT_STAGED",
            "candidate contract still needs parent adoption and multiplier-stress silence",
            source_list("1526_next", "gk_gates"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "hunt_id": hunt_id,
            "target": target,
            "finding": finding,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for hunt_id, target, finding, status, missing, sources in rows
    ]


def auxiliary_action_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AUX1527_0_local_action_candidate",
            "local auxiliary phi owner",
            "S_phiK=int sqrt(-g)[c_I phi R - nabla_mu lambda_phi nabla^mu phi - lambda_phi S_Gamma]+B_phiK, with S_Gamma=(2/3)(Gamma_eff+C)",
            "LOCAL_ACTION_CONTRACT_WRITTEN",
            "not a live parent action until adopted and sign/boundary conventions are fixed",
        ),
        (
            "AUX1527_1_lambda_variation",
            "delta lambda_phi equation",
            "delta_{lambda_phi} S_phiK=0 gives Box phi=S_Gamma, assuming the boundary term kills the integration-by-parts flux",
            "PHI_CONSTRAINT_LOCALIZED",
            "boundary/no-flux condition not signed",
        ),
        (
            "AUX1527_2_phi_variation",
            "delta phi equation",
            "delta_phi S_phiK=0 gives Box lambda_phi=-c_I R plus convention/boundary terms",
            "MULTIPLIER_EQUATION_WRITTEN",
            "lambda_phi must be shown silent in the local Ricci-flat compact branch",
        ),
        (
            "AUX1527_3_metric_response",
            "metric variation",
            "phi R supplies the K_L trace-free response; lambda_phi sector supplies extra stress unless lambda_phi=nabla lambda_phi=0 or is bounded",
            "EXTRA_STRESS_IDENTIFIED",
            "cannot claim K_hat match until multiplier stress is silent or retained",
        ),
        (
            "AUX1527_4_coefficient_link",
            "Khat coefficient",
            "same 1526 coefficient law required: sigma_resp*c_I=1",
            "COEFFICIENT_CONTRACT_INHERITED",
            "live sign convention still missing",
        ),
        (
            "AUX1527_5_verdict",
            "auxiliary phi owner",
            "local auxiliary route avoids inverse-Box nonlocality in form, but introduces lambda_phi stress and adoption obligations",
            "CONDITIONAL_LOCAL_ROUTE_NOT_PROMOTED",
            "needs boundary/no-flux, Ricci-flat lambda silence, and current Khat adoption",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "aux_id": aux_id,
            "object": obj,
            "formula_or_statement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1526_variation", "1526_contract", "gk_contract"),
            **flags(),
        }
        for aux_id, obj, formula, status, missing in rows
    ]


def multiplier_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MLT1527_0_Ricci_flat_lambda_equation",
            "Box lambda_phi=-c_I R",
            "in exact local Ricci-flat vacuum R=0, lambda_phi is harmonic",
            "CONDITIONAL_HARMONIC_ROUTE",
            "requires local Ricci-flat condition from the same parent branch",
        ),
        (
            "MLT1527_1_boundary_silence",
            "lambda_phi boundary/no-flux",
            "lambda_phi=0 or no-flux boundary data would imply lambda_phi=0 for compact positive elliptic branch",
            "BOUNDARY_SILENCE_UNSIGNED",
            "boundary data not parent-signed",
        ),
        (
            "MLT1527_2_extra_stress",
            "T_lambda_phi^{mu nu}",
            "if lambda_phi or nabla lambda_phi is nonzero, its metric response enters S_total/q_loc and must be bounded",
            "RETAIN_IF_NOT_ZERO",
            "no numeric/theorem bound exists",
        ),
        (
            "MLT1527_3_gamma_metric_dependence",
            "lambda_phi S_Gamma response",
            "metric dependence of Gamma_eff in the constraint term vanishes only if lambda_phi=0; otherwise it reopens Kmetric kernels",
            "DEPENDENT_ON_LAMBDA_SILENCE",
            "cannot ignore this term",
        ),
        (
            "MLT1527_4_verdict",
            "multiplier silence",
            "lambda_phi silence is plausible under Ricci-flat plus zero boundary, but not parent-signed",
            "SILENCE_NOT_PROVED",
            "local route remains nonclaim",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "multiplier_id": multiplier_id,
            "object": obj,
            "condition_or_statement": condition,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1010_doc", "1526_claim_gate", "1526_symbol"),
            **flags(),
        }
        for multiplier_id, obj, condition, status, missing in rows
    ]


def khat_adoption_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KAD1527_0_adoption_contract",
            "current K_hat definition",
            "K_hat^{mu nu}:=TF[sigma_resp c_I metric response of int sqrt(-g)phi R] with sigma_resp*c_I=1",
            "ADOPTION_ROW_STAGED_NONCLAIM",
            "not live in main corpus; must be explicitly adopted or sourced",
        ),
        (
            "KAD1527_1_phi_owner_dependency",
            "phi owner dependency",
            "adoption requires S_phiK or an equivalent local parent sector, not inverse-Box shorthand",
            "DEPENDS_ON_AUX_ROUTE",
            "phi owner unresolved",
        ),
        (
            "KAD1527_2_multiplier_dependency",
            "lambda_phi stress dependency",
            "adoption gives clean K_L only if lambda_phi stress is theorem-zero or retained outside K_hat",
            "DEPENDS_ON_MULTIPLIER_GATE",
            "lambda silence not proved",
        ),
        (
            "KAD1527_3_symbol_status",
            "current MTS symbol status",
            "existing sources require K_hat metric response but do not yet make this adoption live",
            "NOT_LIVE",
            "do not use for PPN/local-GR scoring",
        ),
        (
            "KAD1527_4_verdict",
            "Khat adoption",
            "a precise adoption row now exists, but it is staged/nonclaim until signed into the parent action",
            "STAGED_NOT_PROMOTED",
            "current K_hat match remains blocked",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "adoption_id": adoption_id,
            "target": target,
            "contract_or_status": contract,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1526_symbol", "gk_contract", "gk_evidence"),
            **flags(),
        }
        for adoption_id, target, contract, status, missing in rows
    ]


def nonlocality_guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("NLG1527_0_inverse_box", "phi=Box^{-1}S_Gamma", "REJECT_FOR_LOCAL_FIELD_THEORY_CLAIM", "allowed only as explicitly nonlocal/closure branch"),
        ("NLG1527_1_auxiliary_route", "local lambda_phi constraint", "PREFERRED_NONCLAIM_ROUTE", "keeps the theory local in form but adds multiplier stress obligations"),
        ("NLG1527_2_boundary_guard", "Green function/boundary choice", "MUST_BE_PARENT_OWNED", "otherwise phi solution is tuned by external boundary conditions"),
        ("NLG1527_3_verdict", "locality status", "LOCALITY_NOT_PROMOTED", "auxiliary route is staged; inverse-Box shortcut rejected"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "object": obj,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1526_contract", "1526_variation"),
            **flags(),
        }
        for guard_id, obj, status, reason in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1527_0_inverse_box_shortcut", "define phi by inverse Box and call it local", "REJECTED", "nonlocal Green operator/boundary choice is not a local field-theory derivation"),
        ("REJ1527_1_lambda_precedent_import", "use lambda_R precedent as proof of phi owner", "REJECTED", "precedent is not a source path for this field/equation"),
        ("REJ1527_2_ignore_multiplier_stress", "drop lambda_phi stress after adding the constraint", "REJECTED", "new auxiliary fields add metric response unless theorem-zero/bounded"),
        ("REJ1527_3_adopt_Khat_silently", "quietly redefine K_hat as K_L", "REJECTED", "must be explicit parent adoption/source row"),
        ("REJ1527_4_score_local_GR", "score local GR/PPN from staged adoption", "REJECTED", "q_loc_hat/DeltaK/C_op remain blocked"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1527_0_phi_source_hunt", "existing phi owner found", "BLOCKED", "no live phi owner source found"),
        ("GATE1527_1_aux_contract", "local auxiliary phi action contract exists", "PASS_NONCLAIM", "S_phiK contract localizes Box phi relation in form"),
        ("GATE1527_2_multiplier_silence", "lambda_phi stress is zero or bounded", "BLOCKED", "Ricci-flat/boundary silence not parent-signed"),
        ("GATE1527_3_Khat_adoption", "current K_hat adoption is live", "BLOCKED", "adoption row staged only"),
        ("GATE1527_4_DeltaK", "DeltaK zero/compute route can reopen", "BLOCKED", "Khat adoption and Kmetric kernels still unresolved"),
        ("GATE1527_5_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "no q_loc/local branch claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1527_0_source_hunt",
            "No existing live phi owner was found.",
            "SOURCE_HUNT_FAIL",
            "the corpus has the Box phi relation and lambda-style precedents, but not this parent field owner.",
        ),
        (
            "DEC1527_1_best_route",
            "Stage the local auxiliary S_phiK contract as the best nonclaim route.",
            "AUXILIARY_ROUTE_STAGED",
            "it avoids inverse-Box nonlocality in form and exposes the exact multiplier-stress obligation.",
        ),
        (
            "DEC1527_2_adoption_status",
            "Stage but do not promote the current K_hat adoption row.",
            "KHAT_ADOPTION_STAGED_NONCLAIM",
            "this keeps the derivation route explicit without silently changing the theory.",
        ),
        (
            "DEC1527_3_next",
            "Next target is lambda_phi silence/no-flux or retained multiplier-stress bound.",
            "NEXT_1528_MULTIPLIER_SILENCE_OR_BOUND",
            "without lambda silence, the auxiliary fix creates a new local residual.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1527_0_phi_owner", "phi owner", "CONTRACT_STAGED_NONCLAIM", "local auxiliary action written but not parent-adopted"),
        ("LOCAL1527_1_nonlocality", "inverse-Box risk", "GUARDED", "nonlocal shortcut rejected for local field-theory claim"),
        ("LOCAL1527_2_multiplier", "lambda_phi stress", "BLOCKED", "silence/no-flux not proved"),
        ("LOCAL1527_3_Khat", "current K_hat", "ADOPTION_STAGED_NOT_LIVE", "source/adoption row not promoted"),
        ("LOCAL1527_4_GR", "derived local GR/Newton", "NOT_CLAIMED", "DeltaK/q_loc/C_op still downstream"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1527_0_1528",
            "next_target": "1528-Y5-lambda-phi-silence-no-flux-or-multiplier-stress-bound.md",
            "script": "scripts/Y5_lambda_phi_silence_no_flux_or_multiplier_stress_bound.py",
            "objective": "prove lambda_phi=0 from Ricci-flat local equation plus parent boundary/no-flux conditions, or retain/source a multiplier-stress bound before any Khat/DeltaK/local-GR promotion",
            "do_not": "do not ignore lambda_phi stress; do not promote staged Khat adoption; do not score local GR/PPN; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (PHI_SOURCE_HUNT, QUAR_HUNT),
        (AUX_ACTION, QUAR_AUX),
        (KHAT_ADOPTION, QUAR_KHAT),
        (DECISION, QUAR_DECISION),
        (PHI_SOURCE_HUNT, BRANCH_HUNT),
        (AUX_ACTION, BRANCH_AUX),
        (KHAT_ADOPTION, BRANCH_KHAT),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    hunt = read_csv(PHI_SOURCE_HUNT)
    aux = read_csv(AUX_ACTION)
    multiplier = read_csv(MULTIPLIER_GATE)
    khat = read_csv(KHAT_ADOPTION)
    guards = read_csv(NONLOCALITY_GUARD)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1527_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1527 input source paths exist"),
        ("VAL1527_1_source_hunt_fail", any(row["hunt_id"] == "PHH1527_4_verdict" and row["status"] == "SOURCE_HUNT_FAILS_CONTRACT_STAGED" for row in hunt), "phi source hunt failure is explicit"),
        ("VAL1527_2_aux_contract", any(row["aux_id"] == "AUX1527_0_local_action_candidate" and row["status"] == "LOCAL_ACTION_CONTRACT_WRITTEN" for row in aux), "local auxiliary S_phiK contract is written"),
        ("VAL1527_3_phi_constraint", any(row["aux_id"] == "AUX1527_1_lambda_variation" and row["status"] == "PHI_CONSTRAINT_LOCALIZED" for row in aux), "lambda variation localizes Box phi relation"),
        ("VAL1527_4_multiplier_not_silent", any(row["multiplier_id"] == "MLT1527_4_verdict" and row["status"] == "SILENCE_NOT_PROVED" for row in multiplier), "lambda_phi silence remains unproved"),
        ("VAL1527_5_Khat_not_live", any(row["adoption_id"] == "KAD1527_4_verdict" and row["status"] == "STAGED_NOT_PROMOTED" for row in khat), "Khat adoption remains staged/nonclaim"),
        ("VAL1527_6_nonlocal_rejected", any(row["guard_id"] == "NLG1527_0_inverse_box" and row["status"] == "REJECT_FOR_LOCAL_FIELD_THEORY_CLAIM" for row in guards), "inverse-Box shortcut rejected for local field-theory claim"),
        ("VAL1527_7_rejections_guardrails", len(rejections) >= 5 and all(row["status"] == "REJECTED" for row in rejections), "unsafe shortcuts rejected"),
        ("VAL1527_8_claim_gates_block", any(row["gate_id"] == "GATE1527_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1527_9_decision_next", any(row["result"] == "NEXT_1528_MULTIPLIER_SILENCE_OR_BOUND" for row in decisions), "decision selects multiplier silence/bound next"),
        ("VAL1527_10_next_target", any("1528-Y5-lambda-phi" in row["next_target"] for row in next_rows), "next target is lambda_phi silence/no-flux or stress bound"),
        ("VAL1527_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1527 CSVs parse cleanly"),
        ("VAL1527_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1527_13_branch_copies", all(path.exists() for path in [QUAR_HUNT, QUAR_AUX, QUAR_KHAT, QUAR_DECISION, BRANCH_HUNT, BRANCH_AUX, BRANCH_KHAT, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1527_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1527_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1527_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1527 stages a local auxiliary phi-owner contract, rejects inverse-Box promotion, keeps Khat/local-GR nonclaim, and selects lambda_phi silence or bound next"
            if overall
            else "1527 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    hunt: list[dict[str, Any]],
    aux: list[dict[str, Any]],
    multiplier: list[dict[str, Any]],
    khat: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1527 - Phi Owner and Current Khat Symbol-Match Source Hunt",
                "",
                "## Verdict",
                "- Source hunt result: no existing live parent-owned `phi` sector was found; the old `lambda_R` material is only a constraint precedent.",
                "- Best route staged: `S_phiK=int sqrt(-g)[c_I phi R - nabla_mu lambda_phi nabla^mu phi - lambda_phi S_Gamma]+B_phiK`, with `S_Gamma=(2/3)(Gamma_eff+C)`.",
                "- This localizes `Box phi=S_Gamma` without using a naked inverse-Box, but it introduces a new `lambda_phi` multiplier-stress gate.",
                "- Current `K_hat := K_L` adoption is now written as a precise staged row, but it is not live and not scoreable.",
                "- No local-GR/Newton/PPN claim is promoted from 1527.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Phi Owner Source Hunt",
                md_table(hunt, ["hunt_id", "target", "finding", "status", "missing_to_promote"]),
                "",
                "## Local Auxiliary Action Contract",
                md_table(aux, ["aux_id", "object", "formula_or_statement", "status", "missing_to_promote"]),
                "",
                "## Multiplier Stress Silence Gate",
                md_table(multiplier, ["multiplier_id", "object", "condition_or_statement", "status", "missing_to_promote"]),
                "",
                "## Khat Adoption Row",
                md_table(khat, ["adoption_id", "target", "contract_or_status", "status", "missing_to_promote"]),
                "",
                "## Nonlocality Guard",
                md_table(guards, ["guard_id", "object", "status", "reason"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    hunt = phi_source_hunt_rows()
    aux = auxiliary_action_rows()
    multiplier = multiplier_gate_rows()
    khat = khat_adoption_rows()
    guards = nonlocality_guard_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PHI_SOURCE_HUNT, hunt)
    write_csv(AUX_ACTION, aux)
    write_csv(MULTIPLIER_GATE, multiplier)
    write_csv(KHAT_ADOPTION, khat)
    write_csv(NONLOCALITY_GUARD, guards)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PHI_SOURCE_HUNT,
        AUX_ACTION,
        MULTIPLIER_GATE,
        KHAT_ADOPTION,
        NONLOCALITY_GUARD,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, hunt, aux, multiplier, khat, guards, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
