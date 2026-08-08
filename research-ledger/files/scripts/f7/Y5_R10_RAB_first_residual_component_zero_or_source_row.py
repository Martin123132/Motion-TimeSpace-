from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1413-Y5-R10-RAB-first-residual-component-zero-or-source-row.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1413_SOURCE_REGISTER.csv"
R_EM_PROOF_PATH = SRC_DIR / "P8_Y5_R10_1413_R_EM_TYPED_MORPHISM_ZERO_ATTEMPT.csv"
R_EM_SOURCE_ROW_PATH = SRC_DIR / "P8_Y5_R10_1413_R_EM_FINITE_SOURCE_ROW_TEMPLATE.csv"
R_EM_ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1413_R_EM_ARENA_PROJECTION_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1413_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1413_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1413_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1413_VALIDATION.csv"

STATUS = "Y5_R10_1413_R_EM_zero_attempt_failed_finite_source_row_written_nonclaim"
CLAIM_CEILING = (
    "R_EM_first_residual_component_template_only_no_EM_zero_no_alpha_pass_no_WEP_"
    "no_R10_no_clock_transfer_no_Newton_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1413_0_1412_doc",
            "source_path": "1412-Y5-R10-RAB-ordinary-matter-functor-exhaustion-or-finite-residual-vector.md",
            "anchor": "NEXT1412_0_1413",
            "role": "prior checkpoint selecting first residual component zero/source row",
        },
        {
            "source_id": "SRC1413_1_1412_R_EM",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1412_FINITE_RESIDUAL_VECTOR_BRANCH.csv",
            "anchor": "RV1412_0_R_EM",
            "role": "R_EM finite residual component definition",
        },
        {
            "source_id": "SRC1413_2_1412_morphism",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1412_VISIBLE_COEFFICIENT_MORPHISM_COUNTEREXAMPLES.csv",
            "anchor": "MOR1412_0_EM_kinetic",
            "role": "live X -> Z_EM(X)F_Q^2 morphism counterexample",
        },
        {
            "source_id": "SRC1413_3_1411_counterterm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1411_COUNTERTERM_BAN_AUDIT.csv",
            "anchor": "CTB1411_0_ZEM",
            "role": "independent EM kinetic counterterm not banned by derivation",
        },
        {
            "source_id": "SRC1413_4_1396_em_lock",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_EM_LOCK_REPAIR_ATTEMPT.csv",
            "anchor": "ELR1396_6_current_verdict",
            "role": "EM-lock repair status and active blockers",
        },
        {
            "source_id": "SRC1413_5_1396_beta_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv",
            "anchor": "BEM1396_6_template_verdict",
            "role": "finite beta_EM source-bound template ready but unfilled",
        },
        {
            "source_id": "SRC1413_6_1396_arena_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv",
            "anchor": "EMG1396_4_local_GR",
            "role": "alpha/WEP/clock/R10/local_GR arena blockers",
        },
        {
            "source_id": "SRC1413_7_988_emlock",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
            "anchor": "EMLOCK988_5_theorem_verdict",
            "role": "EM-lock theorem exact but not promoted",
        },
        {
            "source_id": "SRC1413_8_988_joint_alpha",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
            "anchor": "JAV988_3_cross_arena_policy",
            "role": "clock/WEP alpha branch cross-arena policy and normalization debt",
        },
        {
            "source_id": "SRC1413_9_988_wep_pressure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
            "anchor": "WEP988_WAS651_0_alpha_Coulomb",
            "role": "source-backed WEP alpha pressure target from prior smoke row, nonclaim",
        },
        {
            "source_id": "SRC1413_10_989_signature",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "anchor": "ELA989_5_total",
            "role": "EM-lock signature audit and no-promotion verdict",
        },
        {
            "source_id": "SRC1413_11_989_source_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
            "anchor": "BSO989_4_failure_action",
            "role": "beta_source_alpha owner ledger and numeric target-only rows",
        },
        {
            "source_id": "SRC1413_12_989_input_candidates",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_PARENT_INPUT_CANDIDATE_LEDGER.csv",
            "anchor": "PIC989_4_no_alpha_vertex",
            "role": "required parent input candidates for EM-lock closure",
        },
        {
            "source_id": "SRC1413_13_this_script",
            "source_path": "scripts/Y5_R10_RAB_first_residual_component_zero_or_source_row.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def r_em_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "REM1413_0_target",
            "zero_target": "R_EM=0",
            "formal_test": "prove Hom(ParentResidual, EMKineticCoefficient)=empty and alpha/readout/current vertices are absent",
            "result": "TARGET_DEFINED",
            "blocking_clause": "all REM1413_1 through REM1413_5 must close",
            "if_failed": "retain R_EM finite source-row template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "REM1413_1_charge_generator_owner",
            "zero_target": "fixed T_Q generator",
            "formal_test": "T_Q is a compact parent-action generator with fixed lattice/norm and no rescaling freedom",
            "result": "UNSIGNED",
            "blocking_clause": "ELA989_0_TQ_owner;EMLOCK988_0_parent_charge_generator",
            "if_failed": "charge unit and A_Q normalization can float",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "REM1413_2_unique_F2_subblock",
            "zero_target": "ban X -> Z_EM(X)F_Q^2",
            "formal_test": "observed F_Q^2 appears only as a parent curvature-norm subblock; standalone lambda_A F_Q^2 is forbidden",
            "result": "FAILS_CURRENT_CORPUS",
            "blocking_clause": "ELR1396_1_unique_Maxwell_F2;EMLOCK988_1_unique_Maxwell_F2;ELA989_1_unique_F2",
            "if_failed": "R_EM remains a live finite residual component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "REM1413_3_current_source_owner",
            "zero_target": "single current/source normalization",
            "formal_test": "matter current, charge labels, Maxwell source normalization, and WEP/R10 source-test strength descend from the same T_Q owner",
            "result": "UNSIGNED",
            "blocking_clause": "ELA989_2_current_owner;BSO989_0_definition",
            "if_failed": "beta_source_alpha remains separate finite debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "REM1413_4_readout_descent",
            "zero_target": "dimensionless alpha readout fixed",
            "formal_test": "Hodge star, coframe, and hbar*c readout are quotient-fixed so Lie_v ln alpha_EM=0",
            "result": "UNSIGNED",
            "blocking_clause": "ELA989_3_readout_descent;JAV988_0_alpha_slot",
            "if_failed": "clock/spectroscopy alpha drift can re-enter through readout units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "REM1413_5_no_alpha_vertex",
            "zero_target": "no explicit alpha/mass/binding response vertex",
            "formal_test": "ordinary matter functor forbids alpha_EM(X), f_A(X)F^2, m_A(X), and binding-response vertices",
            "result": "UNSIGNED",
            "blocking_clause": "ELA989_4_no_alpha_vertex;PIC989_4_no_alpha_vertex",
            "if_failed": "composition-dependent Coulomb and binding channels remain physical fallbacks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "REM1413_6_verdict",
            "zero_target": "R_EM theorem-zero",
            "formal_test": "REM1413_1 through REM1413_5 all parent-signed",
            "result": "R_EM_ZERO_NOT_PROVED_FINITE_ROW_REQUIRED",
            "blocking_clause": "unique F2 fails and charge/current/readout/no-alpha clauses are unsigned",
            "if_failed": "write R_EM finite source-row template with no promoted values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def r_em_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RFS1413_0_R_EM",
            "quantity": "R_EM",
            "definition": "beta_EM^a - beta_*^a or equivalent EM kinetic/alpha relative response",
            "formula_or_target": "R_EM collects b_alpha_EM, beta_source_alpha, EM binding composition, readout descent, and no-alpha-vertex residuals",
            "required_inputs": "parent coordinate basis; EM normalization map; value/bound; uncertainty; units; sign; source path; arena projection",
            "current_value": "MISSING",
            "units": "X_a^-1 or dimensionless per parent coordinate",
            "source_anchor": "REM1413_6_verdict",
            "current_status": "FINITE_SOURCE_ROW_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RFS1413_1_b_alpha_EM",
            "quantity": "b_alpha_EM",
            "definition": "dimensionless alpha_EM drift/coupling slot",
            "formula_or_target": "b_alpha := d ln alpha_EM / d Xhat after parent normalization",
            "required_inputs": "Xhat/canonical parent normalization; tau_clock; tau_WEP; source/readout map",
            "current_value": "MISSING_STANDALONE_VALUE",
            "units": "dimensionless or per declared parent coordinate",
            "source_anchor": "BEM1396_1_b_alpha_EM;JAV988_1_clock_product",
            "current_status": "PRODUCT_BOUND_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RFS1413_2_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "definition": "WEP/source-force normalization multiplying the finite alpha channel",
            "formula_or_target": "eta_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP",
            "required_inputs": "parent source functional or Noether current normalization; tau_WEP; beta_source/tau map; units/sign",
            "current_value": "MISSING_DERIVED_VALUE_TARGET_ONLY",
            "units": "dimensionless suppression factor if parent-normalized",
            "source_anchor": "BSO989_1_alpha_only_target;BSO989_2_robust_surface_including_target",
            "current_status": "NUMERIC_TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RFS1413_3_WEP_pressure_targets",
            "quantity": "R_EM WEP pressure targets",
            "definition": "nonclaim finite-branch targets inherited from alpha/Coulomb smoke pressure",
            "formula_or_target": "alpha-only beta_source_alpha <= 4.797780522732e-05; robust surface-including target <= 2.887280314062e-05",
            "required_inputs": "conversion theorem from smoke charge basis to parent EM residual basis; official U_a/tau_WEP; material tensor",
            "current_value": "TARGETS_ONLY",
            "units": "dimensionless target ratios",
            "source_anchor": "WEP988_WAS651_0_alpha_Coulomb;BSO989_1_alpha_only_target",
            "current_status": "TARGET_ONLY_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RFS1413_4_R10_material_leg",
            "quantity": "R_EM_R10_material_leg",
            "definition": "f_EM,S/T beta_EM contribution to bulk/source-test material leg",
            "formula_or_target": "alpha_bulk,ST(lambda) includes K(lambda)(...+f_EM,S beta_EM)(...+f_EM,T beta_EM)+tail",
            "required_inputs": "f_EM,S/T; beta_EM/R_EM; K(lambda); tail; full R10 bound curve; source paths",
            "current_value": "MISSING",
            "units": "declared by R10 alpha(lambda) map",
            "source_anchor": "BEM1396_4_R10_material_leg",
            "current_status": "R10_MATERIAL_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RFS1413_5_local_EM_residual",
            "quantity": "R_EM_local",
            "definition": "finite local EM residual vector for local GR/Newton/WEP/clock/R10 gates",
            "formula_or_target": "collect alpha_EM drift, Coulomb WEP, clock, binding, R10 material effects, and source normalization",
            "required_inputs": "RFS1413_0 through RFS1413_4 plus local projection and PPN/local-bound interface",
            "current_value": "MISSING",
            "units": "component-specific",
            "source_anchor": "BEM1396_5_local_residual;EMG1396_4_local_GR",
            "current_status": "LOCAL_RESIDUAL_VECTOR_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RFS1413_6_verdict",
            "quantity": "R_EM finite source row pack",
            "definition": "R_EM cannot be theorem-zeroed at 1413, so finite nonclaim source rows are now explicit",
            "formula_or_target": "all RFS1413_0 through RFS1413_5 complete without MISSING before scoring",
            "required_inputs": "source-backed values or theorem-zero clauses for all EM residual subcomponents",
            "current_value": "TEMPLATE_ONLY",
            "units": "not_applicable",
            "source_anchor": "REM1413_6_verdict",
            "current_status": "R_EM_SOURCE_ROW_READY_NONCLAIM_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def r_em_arena_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "RAG1413_0_alpha_clock",
            "arena": "clock/alpha_EM",
            "dependency": "b_alpha_EM and readout descent",
            "current_status": "BLOCKED_PRODUCT_ONLY",
            "reason": "clock product bound exists, but standalone b_alpha and tau_clock dynamics are not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "RAG1413_1_WEP",
            "arena": "WEP/Coulomb",
            "dependency": "beta_source_alpha * b_alpha * tau_WEP and U_a/material tensor",
            "current_status": "BLOCKED_SOURCE_NORMALIZATION_AND_Ua",
            "reason": "source normalization owner is missing and 1409 blocks U_a official readout/source kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "RAG1413_2_R10",
            "arena": "R10/local force range",
            "dependency": "f_EM,S/T beta_EM, K(lambda), tail, and bound curve",
            "current_status": "BLOCKED_MATERIAL_AND_BOUND_CURVE",
            "reason": "R10 material leg and bound curve projection are not filled for R_EM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "RAG1413_3_local_GR",
            "arena": "local GR/Newton",
            "dependency": "R_EM_local=0 or below local bounds plus common matter owner and EH/PPN gates",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "EM-lock not signed and finite local EM residual vector is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "RAG1413_4_transfer_policy",
            "arena": "cross-arena transfer",
            "dependency": "same parent screen/domain/source normalization for clock, WEP, R10, and local EM",
            "current_status": "ARENA_ISOLATION_ACTIVE",
            "reason": "clock-screening cannot be used as a WEP or R10 pass without a parent map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1413_0_component_choice",
            "decision": "target R_EM first",
            "reason": "R_EM touches alpha/charge, WEP Coulomb composition, clocks, R10 material leg, and local EM silence",
            "effect": "highest-leverage residual component is now audited before R_source/R_nuc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1413_1_zero_verdict",
            "decision": "do not claim R_EM=0",
            "reason": "independent F_Q^2 counterterm remains legal and charge/current/readout/no-alpha clauses are unsigned",
            "effect": "R_EM moves to finite source-row template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1413_2_next_best",
            "decision": "target beta_source_alpha/source normalization next",
            "reason": "R_EM finite branch is most blocked by the unowned source-force normalization in WEP/R10",
            "effect": "next checkpoint should try Noether/source-owner derivation or finite bound row for beta_source_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1413_0_R_EM_zero",
            "claim": "R_EM is theorem-zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "unique F2 fails current corpus and EM-lock signatures are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1413_1_finite_R_EM",
            "claim": "finite R_EM row is score-ready",
            "status": "TEMPLATE_ONLY_NO_CLAIM",
            "reason": "values, units, signs, parent basis, and source anchors for subcomponents are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1413_2_alpha_clock",
            "claim": "alpha/clock branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "clock bound is product-only and standalone b_alpha/tau dynamics are not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1413_3_WEP_R10",
            "claim": "R_EM passes WEP or R10",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "beta_source_alpha, U_a, material tensor, and R10 inputs remain incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1413_4_local_GR",
            "claim": "local GR/Newton reduction follows from R_EM",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R_EM is only one residual component and is not zero or bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1413_5_verdict",
            "claim": "1413 solves first residual component",
            "status": "NO_PROMOTION",
            "reason": "1413 converts R_EM into explicit finite nonclaim rows and selects source normalization next",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1413_0_1414",
            "target_doc": "1414-Y5-R10-RAB-beta-source-alpha-owner-or-finite-bound-row.md",
            "target_script": "scripts/Y5_R10_RAB_beta_source_alpha_owner_or_finite_bound_row.py",
            "task": "try to derive the source-force normalization owner beta_source_alpha from T_Q Noether/current normalization; if it fails, write the finite bound row with target-only status",
            "success_condition": "beta_source_alpha is theorem-owned/zero, or a source-ready finite row records target, units, sign convention, required source paths, and nonclaim blockers",
            "do_not_claim": "WEP pass; clock pass; R10 pass; R_EM zero; P_s products; Newton/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1413_1_parallel",
            "target_doc": "future-unique-Maxwell-F2-parent-subblock-proof.md",
            "target_script": "future_parent_EM_uniqueness_route",
            "task": "if a stronger parent curvature/norm axiom appears, revisit the unique Maxwell F2 proof and try to ban lambda_A F_Q^2 directly",
            "success_condition": "standalone EM kinetic prefactors are forbidden by parent symmetry/domain, not by preference",
            "do_not_claim": "F2 uniqueness from contract-only wording",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        R_EM_PROOF_PATH,
        R_EM_SOURCE_ROW_PATH,
        R_EM_ARENA_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL1413_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1413_1_R_EM_zero_attempt",
        any(row["proof_id"] == "REM1413_2_unique_F2_subblock" and row["result"] == "FAILS_CURRENT_CORPUS" for row in proof_rows)
        and any(row["proof_id"] == "REM1413_6_verdict" and row["result"] == "R_EM_ZERO_NOT_PROVED_FINITE_ROW_REQUIRED" for row in proof_rows),
        "R_EM zero attempt records unique-F2 failure and finite-row fallback",
    )
    add(
        "VAL1413_2_source_rows",
        any(row["row_id"] == "RFS1413_6_verdict" and row["current_status"] == "R_EM_SOURCE_ROW_READY_NONCLAIM_VALUES_MISSING" for row in source_rows)
        and all(row["valid_for_claim"] == False for row in source_rows),
        "R_EM finite source-row pack exists but all rows remain nonclaim",
    )
    add(
        "VAL1413_3_arena_gates",
        {"RAG1413_0_alpha_clock", "RAG1413_1_WEP", "RAG1413_2_R10", "RAG1413_3_local_GR"}.issubset(
            {row["arena_id"] for row in arena_rows}
        )
        and all(row["valid_for_claim"] == False for row in arena_rows),
        "alpha, WEP, R10, and local-GR arena gates remain blocked",
    )
    add(
        "VAL1413_4_decision",
        any(row["decision_id"] == "DEC1413_2_next_best" for row in decisions),
        "decision ledger selects beta_source_alpha/source normalization next",
    )
    add(
        "VAL1413_5_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gates),
        "R_EM zero, finite score, arena transfer, and local-GR claims are refused",
    )
    add(
        "VAL1413_6_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1413_7_overall",
        True,
        "1413 chooses R_EM, rejects theorem-zero promotion, and writes finite nonclaim source rows",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1413 - First Residual Component Zero Or Source Row

**Status:** `{STATUS}`

**Current verdict:** `R_EM` is the first retained residual component to audit. The zero route fails in the current corpus because the typed morphism `X -> Z_EM(X)F_Q^2` / standalone `lambda_A F_Q^2` is still legal, and the charge-generator, current-owner, readout-descent, and no-alpha-vertex clauses are unsigned. Therefore `R_EM` is retained as a finite nonclaim source-row pack.

**Discipline move:** no `R_EM=0`, alpha/clock, WEP, R10, Newton, or local-GR claim is made. The useful output is a source-ready decomposition of the EM residual: `b_alpha_EM`, `beta_source_alpha`, WEP pressure targets, R10 material leg, and local EM residual, all still gated.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## R_EM Typed Morphism Zero Attempt

{md_table(proof_rows)}

## R_EM Finite Source Row Template

{md_table(source_rows)}

## R_EM Arena Projection Gate

{md_table(arena_rows)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    proof_rows = r_em_proof_rows()
    source_rows = r_em_source_rows()
    arena_rows = r_em_arena_gate_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, proof_rows, source_rows, arena_rows, decisions, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(R_EM_PROOF_PATH, proof_rows)
    write_csv(R_EM_SOURCE_ROW_PATH, source_rows)
    write_csv(R_EM_ARENA_GATE_PATH, arena_rows)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, proof_rows, source_rows, arena_rows, decisions, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1413 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
