from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_GK_LAMBDA_SIGNATURE_OR_NONCOERCIVE_SWITCH_3588"
CHECKPOINT_ID = "3588"
DOC = ROOT / "3588-Y5-R2FR-GK-lambda-coefficient-signature-or-noncoercive-switch.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3587": RESIDUALS / "P8_Y5_R2FR_3587_NEXT_TARGET.csv",
        "status_3587": RESIDUALS / "P8_Y5_R2FR_3587_STATUS.csv",
        "owner_3587": RESIDUALS / "P8_Y5_R2FR_3587_GK_INPUT_OWNER_MATRIX.csv",
        "candidate_3587": RESIDUALS / "P8_Y5_R2FR_3587_GK_CANDIDATE_BOUND_INPUT_ROWS.csv",
        "readiness_3587": RESIDUALS / "P8_Y5_R2FR_3587_GK_RUNNER_READINESS.csv",
        "gates_3587": RESIDUALS / "P8_Y5_R2FR_3587_ACTIVATION_GATES.csv",
        "validation_3587": RESIDUALS / "P8_Y5_BRR545_3587_VALIDATION.csv",
        "gk_coercivity_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "gk_ghost_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_GHOST_TACHYON_CHECKS.csv",
        "gk_eligibility_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv",
        "gk_missing_coeff_2473": RESIDUALS / "P8_Y5_GK_STRESS_BOUND_2473_MISSING_COEFFICIENT_LEDGER.csv",
        "no_shadow_coercivity_2561": RESIDUALS / "P8_Y5_NO_SHADOW_2561_COERCIVITY_AUDIT.csv",
        "no_shadow_ghost_2561": RESIDUALS / "P8_Y5_NO_SHADOW_2561_GHOST_TACHYON_CHECKS.csv",
        "full_rank_1672": RESIDUALS / "P8_Y5_PARENT_QLOC_1672_FULL_RANK_COERCIVITY_GATE.csv",
        "activation_1800": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_POSITIVE_OPERATOR_ACTIVATION_AUDIT.csv",
        "positive_pack_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "coercivity_steps_1979": RESIDUALS / "P8_Y5_PARENT_QLOC_1979_COERCIVITY_PROOF_STEPS.csv",
        "noncoercive_2079": RESIDUALS / "P8_Y5_PARENT_QLOC_2079_FINITE_NONCOERCIVE_BRANCH.csv",
        "operator_gate_2095": RESIDUALS / "P8_Y5_PARENT_QLOC_2095_OPERATOR_SIGNATURE_GATE.csv",
        "operator_inputs_2095": RESIDUALS / "P8_Y5_PARENT_QLOC_2095_FINITE_OPERATOR_INPUT_ROWS.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3588_SOURCE_REGISTER.csv",
        "lambda_signature": RESIDUALS / "P8_Y5_R2FR_3588_LAMBDA_GK_SIGNATURE_ATTEMPT.csv",
        "clause_audit": RESIDUALS / "P8_Y5_R2FR_3588_COERCIVITY_CLAUSE_AUDIT.csv",
        "noncoercive_switch": RESIDUALS / "P8_Y5_R2FR_3588_NONCOERCIVE_SWITCH_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3588_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3588_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3588_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_GK_lambda_coefficient_signature_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3588_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3588 lambda_GK signature and noncoercive switch source",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def lambda_signature_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "LAMB3588_0_lower_bound_formula",
            "lambda_GK",
            "min(Z_A*lambda1_A + m_A2, Z_G*lambda1_G + m_G2) - abs(c_AG)*C_cross",
            "formal sufficient lower-bound coefficient for the Gamma/Khat channel u_GK=(A,gamma)",
            "EXACT_SUFFICIENT_FORM",
            "requires same norm, same domain, and same stationary energy convention for all terms",
            "owner_3587",
        ),
        (
            "LAMB3588_1_positive_blocks",
            "Z_A,Z_G,m_A2,m_G2",
            "Z_A>0, Z_G>0, m_A2>=0, m_G2>=0",
            "forbids ghost/tachyon signs and gives nonnegative diagonal energy blocks",
            "REQUIRED_NOT_PARENT_SIGNED",
            "2471/2561 state the signs as requirements, not parent-derived coefficients",
            "gk_coercivity_2471",
        ),
        (
            "LAMB3588_2_domain_floor",
            "lambda1_A,lambda1_G",
            "lambda1_A>0 and lambda1_G>0 after gauge/boundary/topology quotient, or mass gaps remove zero modes",
            "keeps constant, harmonic, gauge, and topology modes out of the kernel",
            "REQUIRED_NOT_PARENT_SIGNED",
            "domain constants and quotient kernel removal are not sourced as numeric/signed rows",
            "positive_pack_1846",
        ),
        (
            "LAMB3588_3_cross_term",
            "c_AG,C_cross",
            "abs(c_AG)*C_cross < min(Z_A*lambda1_A + m_A2, Z_G*lambda1_G + m_G2)",
            "Young/Schur smallness condition preventing A-gamma mixing from defeating positivity",
            "FORMAL_ONLY_NOT_PARENT_SIGNED",
            "completion-of-square exists, but c_AG and normalization constants are not parent-owned",
            "no_shadow_coercivity_2561",
        ),
        (
            "LAMB3588_4_lorentzian_stability",
            "full parent action",
            "stationary positive energy must come from a Lorentzian parent with no hidden higher-derivative ghost",
            "prevents a local exterior energy proof from hiding a dynamical instability",
            "MISSING_FULL_LORENTZIAN_CHECK",
            "2471 explicitly leaves full dynamical/Ostrogradsky safety missing",
            "gk_ghost_2471",
        ),
        (
            "LAMB3588_5_observable_lock",
            "physical residual control",
            "positive auxiliary norm must control measured local residuals after quotient/projection",
            "prevents a positive GK norm from missing physical PPN/R10/source/boundary channels",
            "MISSING_COERCIVE_PHYSICAL_LOCK",
            "1672 keeps full-rank/coercive physical lock open",
            "full_rank_1672",
        ),
        (
            "LAMB3588_6_verdict",
            "lambda_GK",
            "lambda_GK>0 is not claimable from current corpus",
            "parent-owned coefficient signs, domain constants, cross smallness, Lorentzian stability, and physical-lock rows are all incomplete",
            "UNSIGNED_POSITIVITY_SWITCH_REQUIRED",
            "therefore the coercive GK no-hair theorem and denominator bound cannot be spent",
            "status_3587",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula_or_condition": formula,
            "meaning": meaning,
            "status": status,
            "blocker_or_scope": blocker,
            "source_path": str(source_paths[source_key]),
            "parent_signed": False,
            "numeric_value_present": False,
            "lambda_positive_claimed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, meaning, status, blocker, source_key in rows
    ]


def clause_audit_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "CLAUSE3588_0_source_handoff",
            "3587 lambda_GK candidate is the correct input to attack first",
            "PASS_HANDOFF",
            "GIB3587_0_lambda_GK_candidate supplies exact missing coefficient/domain list",
            "candidate_3587",
        ),
        (
            "CLAUSE3588_1_diagonal_signs",
            "Z_A>0, Z_G>0, m_A2>=0, m_G2>=0",
            "FAIL_CURRENT_CLAIM",
            "required signs are written as conditions but not parent-signed values or inequalities",
            "gk_coercivity_2471",
        ),
        (
            "CLAUSE3588_2_completed_square",
            "if m_A2>0 then 0.5*m_A2|A|^2 + c_AG A.Dgamma + 0.5*Z_G|Dgamma|^2 has Schur remainder",
            "PASS_FORMAL_INEQUALITY_ONLY",
            "algebraic square completion is useful, but it still depends on unsigned c_AG,m_A2,Z_G",
            "no_shadow_coercivity_2561",
        ),
        (
            "CLAUSE3588_3_zero_modes",
            "massless gamma/A modes require boundary, gauge, topology, and reference removal",
            "FAIL_CURRENT_CLAIM",
            "local kernel and topology removal are not parent-signed",
            "gk_eligibility_2471",
        ),
        (
            "CLAUSE3588_4_domain_constants",
            "lambda1_A, lambda1_G, C_cross exist for the selected self-adjoint domain",
            "FAIL_CURRENT_CLAIM",
            "self-adjoint domain and boundary class remain missing/signature-only",
            "positive_pack_1846",
        ),
        (
            "CLAUSE3588_5_negative_defect_coefficients",
            "if coercivity fails, negative-mode/projector/topology defect coefficients must be finite rows",
            "FAIL_CURRENT_SCORE",
            "2473 still marks C_X, C_H, C_P and boundary/source coefficients missing",
            "gk_missing_coeff_2473",
        ),
        (
            "CLAUSE3588_6_operator_signature_pattern",
            "generic positive operator route requires signed kinetic/mass/source/boundary inputs",
            "FAIL_CURRENT_CLAIM",
            "2095 shows the same exact gap: template exists, signed values do not",
            "operator_gate_2095",
        ),
        (
            "CLAUSE3588_7_lambda_verdict",
            "lambda_GK cannot be used as a positive denominator in epsilon_GK_hair",
            "BLOCKED_COERCIVE_ROUTE",
            "using it would be a hidden axiom, not a derivation",
            "readiness_3587",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "criterion": criterion,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "blocks_lambda_positive_claim": status.startswith("FAIL") or status.startswith("BLOCKED"),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, criterion, status, detail, source_key in rows
    ]


def noncoercive_switch_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "NCS3588_0_branch_decision",
            "GK channel route",
            "Because lambda_GK is unsigned, demote GIB3587_0 from coercive-positive denominator input to finite noncoercive input pack.",
            "ACTIVE_NONCLAIM_SWITCH",
            "status_3587",
        ),
        (
            "NCS3588_1_finite_branch_law",
            "X_GK finite envelope",
            "a_GK := C_Poincare_GK*J_GK_norm + C_trace_GK*abs(Phi_boundary_GK) + C_top_GK*abs(Q_top_GK); X_GK <= 0.5*(a_GK + sqrt(a_GK^2 + 4*F_outer_GK_abs)); epsilon_GK_hair <= K_GK*X_GK",
            "SYMBOLIC_ONLY_FROM_2079_PATTERN",
            "noncoercive_2079",
        ),
        (
            "NCS3588_2_required_inputs",
            "finite noncoercive inputs",
            "C_Poincare_GK;C_trace_GK;C_top_GK;J_GK_norm;Phi_boundary_GK;Q_top_GK;F_outer_GK_abs;K_GK;domain_id;norm_id;source_paths;units",
            "MISSING_INPUT_PACK",
            "operator_inputs_2095",
        ),
        (
            "NCS3588_3_no_denominator_rule",
            "lambda_GK policy",
            "Do not use 1/lambda_GK, lambda_GK>0, or the 3586 coercive no-hair theorem until parent signatures close.",
            "PASS_GUARD",
            "gk_ghost_2471",
        ),
        (
            "NCS3588_4_r10_policy",
            "R10/PPN/local scoring",
            "No R10, PPN, clock, orbital, or local-GR score may run from this branch until finite input rows are numeric/sourced and all MISSING markers clear.",
            "BLOCKED_CURRENT_SCORE",
            "readiness_3587",
        ),
        (
            "NCS3588_5_next_work",
            "3589 target",
            "Build the GK noncoercive input pack or first finite epsilon_GK_hair row; if the input pack is still empty, keep the channel explicitly nonclaim.",
            "NEXT_TARGET_SELECTED",
            "gk_missing_coeff_2473",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "switch_id": switch_id,
            "quantity": quantity,
            "formula_or_rule": formula,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "uses_positive_lambda_denominator": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for switch_id, quantity, formula, status, source_key in rows
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3588_0_sources", "PASS", "all source paths and selected anchors exist", "next_3587"),
        ("GATE3588_1_lambda_formula", "PASS_FORMAL", "lambda_GK sufficient lower-bound formula is exact as a conditional inequality", "owner_3587"),
        ("GATE3588_2_parent_signature", "FAIL_CURRENT_CLAIM", "Z_A,Z_G,m_A2,m_G2,c_AG,lambda1_A,lambda1_G,C_cross are not parent-signed", "gk_coercivity_2471"),
        ("GATE3588_3_coercive_theorem_spend", "FAIL_CURRENT_CLAIM", "positive-denominator GK no-hair theorem cannot be used", "readiness_3587"),
        ("GATE3588_4_noncoercive_switch", "PASS_NONCLAIM", "finite noncoercive branch is the lawful route while lambda_GK is unsigned", "noncoercive_2079"),
        ("GATE3588_5_no_bound_inversion", "PASS_GUARD", "external/local bounds are not used to define missing MTS coefficients", "gates_3587"),
        ("GATE3588_6_local_GR", "FAIL_CURRENT_CLAIM", "lambda switch alone does not prove local GR, PPN silence, or R10 pass", "full_rank_1672"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "LAMBDA_GK_UNSIGNED_NONCOERCIVE_SWITCH_ACTIVE",
            "strongest_result": "3588 proves the exact conditional lambda_GK gate: positivity would follow from signed diagonal blocks, domain floors, cross-term smallness, zero-mode removal, Lorentzian stability, and physical residual lock. The corpus has those as requirements and formal inequalities, not parent-owned coefficients, so the coercive GK no-hair route is demoted.",
            "decision": "switch GK to the finite noncoercive branch as a nonclaim route; do not use lambda_GK as a positive denominator",
            "still_missing": "Z_A,Z_G,m_A2,m_G2,c_AG; lambda1_A,lambda1_G,C_cross; zero-mode/gauge/topology removal; Lorentzian stability; physical residual lock; finite noncoercive constants C_Poincare_GK,C_trace_GK,C_top_GK,F_outer_GK_abs,K_GK and source/boundary norms",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3587"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3588_0",
            "target_doc": "3589-Y5-R2FR-GK-noncoercive-input-pack-or-first-finite-epsilon-row.md",
            "target_script": "scripts/Y5_R2FR_3589_GK_noncoercive_input_pack_or_first_finite_epsilon_row.py",
            "objective": "source or construct the finite noncoercive GK input pack C_Poincare_GK,C_trace_GK,C_top_GK,J_GK_norm,Phi_boundary_GK,Q_top_GK,F_outer_GK_abs,K_GK, or keep epsilon_GK_hair blocked as nonclaim",
            "success_gate": "a finite epsilon_GK_hair expression has all symbolic inputs named with source/unit owners, or the branch remains explicitly blocked with no hidden lambda_GK positivity",
            "reason": "this is the only lawful way forward unless the parent action later signs lambda_GK>0",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    lambdas: list[dict[str, object]],
    clauses: list[dict[str, object]],
    switches: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3587": "NEXT3587_0",
        "status_3587": "GK_INPUTS_STAGED_NOT_SIGNED_OR_NUMERIC",
        "owner_3587": "GIO3587_0_lambda_GK",
        "candidate_3587": "GIB3587_0_lambda_GK_candidate",
        "readiness_3587": "GRR3587_0_theorem_zero_route",
        "gates_3587": "GATE3587_5_no_bound_inversion",
        "validation_3587": "VAL3587_12_formalization_workbench_untouched",
        "gk_coercivity_2471": "COER2471_5_current_status",
        "gk_ghost_2471": "GT2471_5_higher_derivative",
        "gk_eligibility_2471": "NHG2471_5_eligibility",
        "gk_missing_coeff_2473": "MISS2473_2_CX",
        "no_shadow_coercivity_2561": "COER2561_3_completed_square",
        "no_shadow_ghost_2561": "GHOST2561_4_cross_instability",
        "full_rank_1672": "RG1672_3_coercivity",
        "activation_1800": "XPA1800_1_operator_sign_gap",
        "positive_pack_1846": "OP1846_3_self_adjoint_domain",
        "coercivity_steps_1979": "PRF1979_4_coercivity",
        "noncoercive_2079": "FIN2079_0_branch_law",
        "operator_gate_2095": "OP2095_4_positive_nohair",
        "operator_inputs_2095": "ZRI2095_0_ZRR",
    }
    validations.append(("VAL3588_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3588 source paths exist"))
    validations.append(("VAL3588_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3588 anchors found"))
    validations.append(("VAL3588_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3588 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3588_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3588_4_lambda_not_claimed", any(row["row_id"] == "LAMB3588_6_verdict" and row["status"] == "UNSIGNED_POSITIVITY_SWITCH_REQUIRED" for row in lambdas), "lambda_GK positivity remains unclaimed"))
    validations.append(("VAL3588_5_required_clauses_present", {"CLAUSE3588_1_diagonal_signs", "CLAUSE3588_2_completed_square", "CLAUSE3588_3_zero_modes", "CLAUSE3588_4_domain_constants", "CLAUSE3588_7_lambda_verdict"}.issubset({str(row["clause_id"]) for row in clauses}), "all main lambda clauses are audited"))
    validations.append(("VAL3588_6_noncoercive_switch_active", any(row["switch_id"] == "NCS3588_0_branch_decision" and row["status"] == "ACTIVE_NONCLAIM_SWITCH" for row in switches), "GK branch switched to finite noncoercive nonclaim route"))
    validations.append(("VAL3588_7_no_positive_denominator_use", all(str(row.get("uses_positive_lambda_denominator", False)).lower() == "false" for row in switches), "noncoercive switch rows do not use positive lambda_GK denominator"))
    validations.append(("VAL3588_8_coercive_route_blocked", any(row["gate_id"] == "GATE3588_3_coercive_theorem_spend" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "coercive theorem spending remains blocked"))
    generated_rows = lambdas + clauses + switches + gates + status + next_target
    validations.append(("VAL3588_9_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" and str(row.get("claim_allowed", False)).lower() == "false" for row in generated_rows), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3588_10_next_target_selected", any(row["next_id"] == "NEXT3588_0" for row in next_target), "3589 finite noncoercive input pack target selected"))
    validations.append(("VAL3588_11_generated_source_paths_exist", all(Path(str(row["source_path"])).exists() for row in lambdas + clauses + switches + gates + status), "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3588*")) or any(FORMALIZATION.rglob("3588-Y5-R2FR*"))
    validations.append(("VAL3588_12_formalization_workbench_untouched", not formalization_touched, "no 3588 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    lambdas: list[dict[str, object]],
    clauses: list[dict[str, object]],
    switches: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3588 - GK lambda coefficient signature or noncoercive switch",
        "",
        "## Verdict",
        "3588 attacks `lambda_GK` directly.  The lower-bound formula is clean, but the current corpus still does not parent-sign the coefficients, domain constants, cross-term smallness, zero-mode removal, Lorentzian stability, or physical residual lock.",
        "",
        "So the coercive GK no-hair route is not legally spendable.  The correct move is to switch the GK channel to the finite noncoercive branch as a nonclaim route.",
        "",
        "## Lambda signature attempt",
    ]
    for row in lambdas:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['status']} - {row['formula_or_condition']}")
    lines.extend(["", "## Coercivity clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}`: {row['status']} - {row['criterion']}")
    lines.extend(["", "## Noncoercive switch"])
    for row in switches:
        lines.append(f"- `{row['switch_id']}` `{row['quantity']}`: {row['status']} - {row['formula_or_rule']}")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    lambdas = lambda_signature_rows(source_paths)
    clauses = clause_audit_rows(source_paths)
    switches = noncoercive_switch_rows(source_paths)
    gates = gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "lambda_signature": lambdas,
        "clause_audit": clauses,
        "noncoercive_switch": switches,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, lambdas, clauses, switches, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(lambdas, clauses, switches, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3588 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
