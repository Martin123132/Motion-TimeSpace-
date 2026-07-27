from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1283"
TITLE = "1283-Y5-R10-RAB-q_loc-profile-source-fill-or-P_loc-projector-owner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PROFILE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_QLOC_PROFILE_SOURCE_FILL_AUDIT.csv"
PLOC_DERIVATION_PATH = OUT_DIR / f"{PACK_ID}_PLOC_PROJECTOR_OWNER_DERIVATION.csv"
THEOREM_ZERO_PATH = OUT_DIR / f"{PACK_ID}_THEOREM_ZERO_SWITCH_AUDIT.csv"
LIVE_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_MINIMUM_LIVE_PROFILE_SCHEMA.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1283_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        PROFILE_AUDIT_PATH,
        PLOC_DERIVATION_PATH,
        THEOREM_ZERO_PATH,
        LIVE_SCHEMA_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1283_0_1282_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1282_NEXT_TARGET.csv",
            "needle": "NEXT1282_0_1283",
            "role": "handoff into q_loc profile source-fill or P_loc owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_1_1187_source_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1187_GAMMA_KHAT_PLOC_QNORM_SOURCE_ROWS.csv",
            "needle": "GKP1187_2_P_loc",
            "role": "prior source rows for Gamma_eff, K_hat, P_loc, q_loc, qnorm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_2_Ploc_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1208_PLOC_PARALLEL_PROJECTOR_AUDIT.csv",
            "needle": "PPA1208_5_zero_verdict",
            "role": "projector identity and finite-domain zero/bound audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_3_input_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_792_GAMMA_KHAT_INPUT_REQUIREMENTS.csv",
            "needle": "GKI792_2_Ploc_definition",
            "role": "minimum Gamma/Khat/Ploc/boundary/response inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_4_first_variation",
            "local_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            "needle": "GK513_4_projector_ownership",
            "role": "action/Helmholtz/Euler/double-zero/projector/boundary clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_5_metric_response",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "MR514_1_Khat_metric_response",
            "role": "Gamma_eff and K_hat metric-response requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_6_1281_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1281_EPSILON_GK_QLOC_PROFILE_TEMPLATE_NONCLAIM.csv",
            "needle": "GKQ1281_TEMPLATE_DO_NOT_SCORE",
            "role": "current invalid q_loc profile template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_7_1282_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1282_QLOC_PROFILE_FILL_REQUIREMENTS.csv",
            "needle": "QPF1282_3_P_loc",
            "role": "profile fill requirements from 1282",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_8_bound_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1280_EPSILON_GK_QLOC_BOUND_CONTRACT.csv",
            "needle": "BND1280_0_definition",
            "role": "epsilon_GK_q_loc bound contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_9_qnorm_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_NORM_SOURCE_ROWS.csv",
            "needle": "QNR1186_0_formula_row",
            "role": "q_loc formula and norm rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_10_bound_runner",
            "local_path": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
            "needle": "QB516_0_compact_shell_budget",
            "role": "fallback bound-runner quantities and missing mappings",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_11_component_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1189_QLOC_COMPONENT_RESIDUAL_INPUT_PACK.csv",
            "needle": "QPACK1189_0_PPN_component_template",
            "role": "component profile input pack remains template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1283_12_component_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
            "needle": "QIN750_3_q_loc_components",
            "role": "component input schema for future numeric profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    profile_audit = [
        {
            "audit_id": "QPF1283_0_formula_shell",
            "object": "q_loc^nu",
            "current_formula": "q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "source_status": "FORMULA_SHELL_PRESENT",
            "blocking_gap": "MISSING_ACTUAL_PROFILE_VALUES_AND_DOMAIN",
            "what_was_gained": "the residual is now tied to a concrete vector V^nu before projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QPF1283_1_Gamma_eff",
            "object": "Gamma_eff",
            "current_formula": "MISSING_GAMMA_EFF_FORMULA",
            "source_status": "MISSING_PROFILE_AND_UNITS",
            "blocking_gap": "no sourced scalar/density equation, units, background subtraction, or local branch profile",
            "what_was_gained": "identified as first live owner, because nabla Gamma_eff drives q_loc directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QPF1283_2_K_hat",
            "object": "K_hat^{mu nu}",
            "current_formula": "MISSING_K_HAT_FORMULA;MISSING_DELTA_K_COMPARISON",
            "source_status": "MISSING_PROFILE_AND_METRIC_RESPONSE_MATCH",
            "blocking_gap": "no sourced tensor equation and no Delta_K=K_hat-K_metric ledger",
            "what_was_gained": "identified as second live owner; if Delta_K survives it becomes an explicit local residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QPF1283_3_P_loc",
            "object": "P_loc",
            "current_formula": "projector structure partially derived; parent owner still missing",
            "source_status": "DERIVED_PROJECTOR_IDENTITIES_NOT_PARENT_ZERO",
            "blocking_gap": "parallel splitting/domain/readout/boundary package not parent-signed",
            "what_was_gained": "P_loc is no longer just a word; the exact zero condition is covariant-parallel splitting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QPF1283_4_units_norm",
            "object": "||q_loc||_local or A_loc",
            "current_formula": "MISSING_Q_LOC_UNITS;MISSING_LOCAL_NORM_DEFINITION;MISSING_A_REF_OR_DIMENSIONLESS_GATE",
            "source_status": "MISSING_NORM_AND_UNITS",
            "blocking_gap": "Gamma/Khat units and local measure/frame are absent",
            "what_was_gained": "norm cannot be chosen independently of the sourced Gamma/Khat/P_loc domain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QPF1283_5_arena_bounds",
            "object": "PPN/clock/orbital/local-GR/R10 thresholds",
            "current_formula": "MISSING_ARENA_BOUND_THRESHOLD;MISSING_BOUND_UNITS",
            "source_status": "MAPPING_MISSING",
            "blocking_gap": "no q_loc-to-observable response coefficients",
            "what_was_gained": "bound branch is refused until profile and response map are both source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "QPF1283_6_verdict",
            "object": "epsilon_GK_q_loc live row",
            "current_formula": "GKQ1281_TEMPLATE_DO_NOT_SCORE",
            "source_status": "TEMPLATE_REMAINS_INVALID",
            "blocking_gap": "Gamma_eff, K_hat, P_loc, units, norm, and response bounds are not filled",
            "what_was_gained": "the next derivation target is narrowed to Gamma_eff/K_hat owner extraction plus Delta_K",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ploc_derivation = [
        {
            "derivation_id": "POD1283_0_projector_identity",
            "statement": "For any smooth projector P with P^2=P, nabla(P^2)=nablaP gives P(nablaP)P=0 and (I-P)(nablaP)(I-P)=0.",
            "consequence": "projector drift is purely off-diagonal between image and kernel",
            "zero_condition": "nablaP=0 requires no image/kernel mixing",
            "current_status": "DERIVED_IDENTITY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "POD1283_1_parallel_splitting",
            "statement": "For an orthogonal projector onto E, nablaP is controlled by second fundamental forms of E and E_perp.",
            "consequence": "P_loc is covariantly silent only if the selected local split is parallel under the same connection",
            "zero_condition": "II_E=0 and II_Eperp=0 with no connection mismatch",
            "current_status": "CONDITIONAL_ZERO_REDUCED_TO_PARALLEL_SPLITTING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "POD1283_2_finite_domain_bound",
            "statement": "A Fermi/local-inertial choice can zero connection coefficients at a point but over finite L gives ||nablaP|| <= C_Fermi L ||Riemann|| + O(L^2||nablaRiemann||).",
            "consequence": "finite local domains generically need a curvature/domain bound, not a projector-zero axiom",
            "zero_condition": "point limit, flat/parallel parent geometry, or source-backed smallness bound",
            "current_status": "BOUND_LAW_DERIVED_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "POD1283_3_quotient_chain_rule",
            "statement": "If P_loc=Pi(q(Phi)), then nablaP_loc=D_Pi(q)nablaq; vertical silence along ker(Dq) does not erase spacetime gradients.",
            "consequence": "quotient invariance alone cannot prove finite-domain P_loc silence",
            "zero_condition": "D_Pi=0 on branch or q is covariantly constant in the observed domain",
            "current_status": "VERTICAL_ZERO_NOT_ENOUGH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "POD1283_4_norm_bound",
            "statement": "With V^nu=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}, an orthogonal P_loc gives ||q_loc|| <= ||V||; nonparallel projector effects enter any commuted/integrated response through ||nablaP_loc|| terms.",
            "consequence": "P_loc can be handled honestly as a bound factor once Gamma_eff and K_hat profiles exist",
            "zero_condition": "V=0 plus no projector/boundary leakage, or finite source-backed ||V|| and ||nablaP|| bounds",
            "current_status": "SYMBOLIC_BOUND_READY_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "POD1283_5_verdict",
            "statement": "P_loc has a real mathematical owner route, but not a parent-signed local-zero theorem in the current corpus.",
            "consequence": "projector uncertainty is demoted from mystery to explicit parallel-splitting/curvature/domain input debt",
            "zero_condition": "parallel splitting + fixed connection + fixed readout projector + boundary silence",
            "current_status": "PLOC_OWNER_NOT_CLOSED_BUT_BOUNDABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_zero = [
        {
            "gate_id": "TZ1283_0_action_existence",
            "required_clause": "local diffeo-invariant S_GK exists",
            "current_status": "NOT_SUPPLIED",
            "source_anchor": "GK513_0_action_existence",
            "effect": "Gamma/Khat remain non-variational if absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TZ1283_1_metric_response",
            "required_clause": "K_hat equals metric response of sqrt(-g) Gamma_eff",
            "current_status": "NOT_MATCHED",
            "source_anchor": "MR514_1_Khat_metric_response",
            "effect": "Delta_K enters q_loc if nonzero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TZ1283_2_Euler_closure",
            "required_clause": "fields building Gamma/Khat obey source-free local Euler equations",
            "current_status": "NOT_DERIVED",
            "source_anchor": "GK513_2_Euler_closure",
            "effect": "stress divergence remains physical force/source-exchange residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TZ1283_3_double_zero",
            "required_clause": "T_GK and first variation vanish at local fixed point",
            "current_status": "NOT_MATCHED_TO_PHYSICAL_QLOC",
            "source_anchor": "GK513_3_double_zero; FZ1282_5_verdict",
            "effect": "formal double-zero cannot claim local PPN silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TZ1283_4_projector_boundary",
            "required_clause": "P_loc parent-owned and boundary/symplectic flux zero",
            "current_status": "PLOC_BOUNDABLE_BUT_NOT_ZERO;BOUNDARY_OPEN",
            "source_anchor": "POD1283_5_verdict; GK513_5_boundary_no_flux",
            "effect": "projection and boundary terms remain explicit residual gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TZ1283_5_verdict",
            "required_clause": "all theorem-zero gates close",
            "current_status": "THEOREM_ZERO_FALSE",
            "source_anchor": "BND1280_1_theorem_zero_switch",
            "effect": "epsilon_GK_q_loc remains nonclaim retained residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    live_schema = [
        {
            "field_id": "LQS1283_0_source_identity",
            "required_column": "source_path;source_anchor;equation_ref",
            "acceptance_rule": "source exists and anchor/equation is found in the cited file",
            "current_status": "MISSING_FOR_LIVE_QLOC_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "LQS1283_1_domain_frame",
            "required_column": "domain_id;boundary_condition;frame_convention;P_loc_definition",
            "acceptance_rule": "same local domain/frame used in q_loc, PPN, clock, and orbital projections",
            "current_status": "MISSING_FOR_LIVE_QLOC_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "LQS1283_2_profiles",
            "required_column": "Gamma_eff_formula;K_hat_formula;Delta_K_status;q_loc_profile_formula",
            "acceptance_rule": "Gamma/Khat profiles are explicit and Delta_K is zero or separately bounded",
            "current_status": "MISSING_FOR_LIVE_QLOC_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "LQS1283_3_units_norm",
            "required_column": "q_loc_units;norm_definition;normalization_reference;weight_measure",
            "acceptance_rule": "dimensionless A_loc or arena-specific norm can be reproduced",
            "current_status": "MISSING_FOR_LIVE_QLOC_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "LQS1283_4_observable_map",
            "required_column": "arena;response_operator_id;arena_bound_threshold;bound_units",
            "acceptance_rule": "q_loc-to-observable map is sourced before any comparison to PPN/clock/orbital/R10",
            "current_status": "MISSING_FOR_LIVE_QLOC_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_id": "LQS1283_5_claim_flags",
            "required_column": "valid_for_claim;claim_allowed;no_cancellation_guard",
            "acceptance_rule": "claim flags can only change after all prior fields close and no cancellation is used",
            "current_status": "FORCED_FALSE_IN_PRIVATE_CHECKPOINT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1283_0_projector_progress",
            "decision": "Keep the P_loc route alive as a boundable geometric object.",
            "because": "projector identities and finite-domain drift bounds are real, but exact zero requires parallel splitting plus boundary/readout ownership",
            "next_action": "do not spend the next step on P_loc alone unless Gamma/Khat profiles exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1283_1_primary_blocker",
            "decision": "Move the next derivation target to Gamma_eff/K_hat owner extraction and Delta_K.",
            "because": "P_loc can only project/bound the vector V; the vector itself is undefined until Gamma_eff and K_hat are sourced",
            "next_action": "attempt a Gamma_eff/K_hat candidate extraction from existing action/field files or write an explicit no-source blocker ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1283_2_nonclaim_stance",
            "decision": "Keep epsilon_GK_q_loc retained and unscoreable.",
            "because": "theorem-zero is false and the live profile schema still has missing source, profile, unit, norm, and response fields",
            "next_action": "no local-GR/PPN claim until theorem-zero or finite profile gates close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1283_0_1284",
            "target_file": "1284-Y5-R10-RAB-Gamma-eff-Khat-owner-extraction-or-DeltaK-residual-ledger.md",
            "target_script": "scripts/Y5_R10_RAB_Gamma_eff_Khat_owner_extraction_or_DeltaK_residual_ledger.py",
            "task": "attempt to extract sourced Gamma_eff and K_hat formulas from existing candidate action/field files and decide whether Delta_K=K_hat-K_metric can be zeroed, bounded, or must become a separate retained residual",
            "success_condition": "Gamma_eff and K_hat acquire source-backed formula rows with units and variation convention, or Delta_K/Gamma/Khat remain explicit blocker rows with no live q_loc claim",
            "do_not": "do not use P_loc identities to hide missing Gamma/Khat profiles and do not claim q_loc zero from a formula shell",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PROFILE_AUDIT_PATH, profile_audit)
    write_csv(PLOC_DERIVATION_PATH, ploc_derivation)
    write_csv(THEOREM_ZERO_PATH, theorem_zero)
    write_csv(LIVE_SCHEMA_PATH, live_schema)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1283_0_sources_exist",
            "all cited local sources exist",
            all(bool(row["exists"]) for row in source_register),
            f"{sum(bool(row['exists']) for row in source_register)}/{len(source_register)} sources exist",
        )
    )
    validations.append(
        validation_row(
            "VAL1283_1_needles_found",
            "all cited local needles found",
            all(bool(row["needle_found"]) for row in source_register),
            f"{sum(bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        )
    )
    ploc_verdict = next(row for row in ploc_derivation if row["derivation_id"] == "POD1283_5_verdict")
    validations.append(
        validation_row(
            "VAL1283_2_Ploc_boundable_not_zero",
            "P_loc owner route is sharpened but not claimed zero",
            ploc_verdict["current_status"] == "PLOC_OWNER_NOT_CLOSED_BUT_BOUNDABLE" and is_false(ploc_verdict["valid_for_claim"]),
            "POD1283_5_verdict=PLOC_OWNER_NOT_CLOSED_BUT_BOUNDABLE",
        )
    )
    profile_verdict = next(row for row in profile_audit if row["audit_id"] == "QPF1283_6_verdict")
    validations.append(
        validation_row(
            "VAL1283_3_profile_template_invalid",
            "q_loc live profile remains invalid",
            profile_verdict["source_status"] == "TEMPLATE_REMAINS_INVALID" and is_false(profile_verdict["claim_allowed"]),
            "QPF1283_6_verdict=TEMPLATE_REMAINS_INVALID",
        )
    )
    theorem_verdict = next(row for row in theorem_zero if row["gate_id"] == "TZ1283_5_verdict")
    validations.append(
        validation_row(
            "VAL1283_4_theorem_zero_false",
            "theorem-zero switch remains false",
            theorem_verdict["current_status"] == "THEOREM_ZERO_FALSE" and is_false(theorem_verdict["valid_for_claim"]),
            "TZ1283_5_verdict=THEOREM_ZERO_FALSE",
        )
    )
    validations.append(
        validation_row(
            "VAL1283_5_live_schema_blocks_claim",
            "minimum live q_loc schema blocks claim until all fields are sourced",
            all("MISSING" in str(row["current_status"]) or "FORCED_FALSE" in str(row["current_status"]) for row in live_schema)
            and all(is_false(row["claim_allowed"]) for row in live_schema),
            f"live_schema_rows={len(live_schema)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        PROFILE_AUDIT_PATH,
        PLOC_DERIVATION_PATH,
        THEOREM_ZERO_PATH,
        LIVE_SCHEMA_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(
        validation_row(
            "VAL1283_6_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parse_details),
        )
    )
    validations.append(
        validation_row(
            "VAL1283_7_next_target_1284",
            "next target routes to Gamma_eff/Khat owner extraction or DeltaK residual ledger",
            next_target[0]["next_id"] == "NEXT1283_0_1284" and "Delta_K" in str(next_target[0]["task"]),
            str(next_target[0]["target_file"]),
        )
    )
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1283_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1283_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
                for rows in [source_register, profile_audit, ploc_derivation, theorem_zero, live_schema, decision, next_target]
                for row in rows
            ),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1283_10_overall",
            "overall 1283 validation",
            overall_pass,
            "1283 derives the projector-zero condition/bound route, keeps q_loc profile invalid, and routes to Gamma_eff/Khat/DeltaK owner extraction next",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1283 Y5 R10 RAB q_loc profile source fill or P_loc projector owner

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1283 makes real progress on `P_loc`, but still does not produce a live `q_loc` profile or theorem-zero. `P_loc` is boundable and has exact projector identities; it is not parent-signed as zero on the finite local branch.

**Main progress:** the local projector gap is now less grim: for `P^2=P`, projector drift is off-diagonal, and finite-domain projector leakage is controlled by parallel splitting/curvature/domain data. That means the projector problem can be bounded honestly. The sharper blocker is now `Gamma_eff`, `K_hat`, and `Delta_K=K_hat-K_metric`.

**Next derivation target:** extract or reject concrete `Gamma_eff` and `K_hat` owners. Without those, `q_loc=P_loc(nabla Gamma_eff-div K_hat)` is only a formula shell.

## Minimal Derivation

Let `V^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}}`, so `q_loc^nu=P_loc V^nu`.

For a projector `P^2=P`, differentiating gives `(nabla P)P + P(nabla P)=nabla P`. Multiplying on both sides by `P` gives `P(nabla P)P=0`; similarly `(I-P)(nabla P)(I-P)=0`. So nonparallel projector drift only mixes image and kernel. Exact projector silence requires the image and kernel splitting to be parallel in the same local connection. In a finite local/Fermi domain this is generically a curvature/domain bound, not a free zero.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## q_loc Profile Source Fill Audit

{markdown_table(profile_audit, ["audit_id", "object", "current_formula", "source_status", "blocking_gap", "what_was_gained", "valid_for_claim", "claim_allowed"])}

## P_loc Projector Owner Derivation

{markdown_table(ploc_derivation, ["derivation_id", "statement", "consequence", "zero_condition", "current_status", "valid_for_claim", "claim_allowed"])}

## Theorem-Zero Switch Audit

{markdown_table(theorem_zero, ["gate_id", "required_clause", "current_status", "source_anchor", "effect", "valid_for_claim", "claim_allowed"])}

## Minimum Live Profile Schema

{markdown_table(live_schema, ["field_id", "required_column", "acceptance_rule", "current_status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
