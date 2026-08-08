from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1294"
TITLE = "1294-Y5-R10-RAB-chain-kernel-response-operator-or-input-pack-acquisition"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INPUT_PRIORITY_PATH = OUT_DIR / f"{PACK_ID}_INPUT_PRIORITY_AUDIT.csv"
C_SIGN_CANDIDATE_PATH = OUT_DIR / f"{PACK_ID}_C_SIGN_CONVENTION_CANDIDATE.csv"
PATCH_PREVIEW_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_PATCH_PREVIEW_NONCLAIM.csv"
RESPONSE_BLOCKERS_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_OPERATOR_BLOCKERS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1294_VALIDATION.csv"

INPUT_PATH = OUT_DIR / "P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv"


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
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def missing_tokens(value: str) -> list[str]:
    return [token for token in split_semicolon(value) if token.startswith("MISSING")]


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        INPUT_PRIORITY_PATH,
        C_SIGN_CANDIDATE_PATH,
        PATCH_PREVIEW_PATH,
        RESPONSE_BLOCKERS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def preview_required_inputs(required_inputs: str) -> tuple[str, bool, list[str]]:
    tokens = split_semicolon(required_inputs)
    applied = "MISSING_C_SIGN" in tokens
    preview_tokens = ["C_SIGN_GK514_CANDIDATE_NONCLAIM" if token == "MISSING_C_SIGN" else token for token in tokens]
    remaining = [token for token in preview_tokens if token.startswith("MISSING")]
    return ";".join(preview_tokens), applied, remaining


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    runner_rows = read_csv(INPUT_PATH)

    source_register = [
        {
            "source_id": "SRC1294_0_1293_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1293_NEXT_TARGET.csv",
            "needle": "NEXT1293_0_1294",
            "role": "handoff requesting first response operator/input pack acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_1_1292_runner_input",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "needle": "MISSING_C_SIGN",
            "role": "runner input templates containing the first replaceable missing sign token",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_2_GK_action",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
            "needle": "T_GK^{mu nu} = Gamma_eff g^{mu nu} - K_metric^{mu nu}",
            "role": "source-backed stress/action convention candidate for C_sign",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_3_GK_contract",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "fixed sign convention",
            "role": "contract saying K_hat/K_metric requires a fixed sign convention before claim use",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_4_Kgamma_volume",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "fixed sign/volume convention matching 514/733",
            "role": "volume-piece ledger proving sign/volume convention is still a claim blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_5_Kmetric_volume",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
            "needle": "up to sign/convention",
            "role": "current volume row remains convention-qualified and nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_6_derivative_chain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "needle": "C_sign fixed by Hilbert-stress convention",
            "role": "derivative-chain row where C_sign is explicitly missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_7_response_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "needle": "MISSING_FULL_RESPONSE_MATRIX",
            "role": "response operator matrix remains missing after sign candidate acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1294_8_1293_rejection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1293_REJECTION_SMOKE_RESULTS.csv",
            "needle": "REJECTED_NONCLAIM_NO_SCORE",
            "role": "prior runner rejection state to preserve after patch preview",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    input_priority = [
        {
            "audit_id": "IPA1294_0_C_sign",
            "input_name": "C_sign",
            "missing_token": "MISSING_C_SIGN",
            "priority": "BEST_FIRST_ACQUISITION",
            "candidate_status": "SOURCE_BACKED_CONVENTION_CANDIDATE_ACQUIRED_NOT_PROMOTED",
            "source_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv;source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "blocks_before_runner_use": "SIGN_CONVENTION_LOCK;VOLUME_DERIVATIVE_SPLIT;KHAT_KMETRIC_MATCH;RESPONSE_OPERATOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "IPA1294_1_response_operator",
            "input_name": "local response operators",
            "missing_token": "MISSING_RESPONSE_OPERATOR;MISSING_OBSERVABLE_RESPONSE_MATRIX;MISSING_LOCAL_RESPONSE_LIMITS",
            "priority": "NEXT_HIGHEST",
            "candidate_status": "MISSING_SOURCE_BACKED_OPERATOR_ROWS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "blocks_before_runner_use": "NEWTON_PPN_CLOCK_ORBITAL_R10_WEP_RESPONSE_MAPS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "IPA1294_2_m_profile",
            "input_name": "m profile and F/F_prime bounds",
            "missing_token": "MISSING_m_PROFILE;MISSING_F_BOUND;MISSING_F_PRIME_BOUND",
            "priority": "HIGH",
            "candidate_status": "MISSING_PROFILE_AND_BOUND_ROWS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "blocks_before_runner_use": "M_PROFILE_SOURCE;F_BOUND_SOURCE;F_PRIME_BOUND_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "IPA1294_3_Lcg_bound",
            "input_name": "L_cg value/lower bound",
            "missing_token": "MISSING_L_cg_VALUE;MISSING_LCG_LOWER_BOUND",
            "priority": "HIGH",
            "candidate_status": "MISSING_LOCAL_LENGTH_BOUND_ROWS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "blocks_before_runner_use": "L_CG_VALUE_OR_LOWER_BOUND;UNITS_LEDGER",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "IPA1294_4_metric_kernels",
            "input_name": "metric response kernels",
            "missing_token": "MISSING_M_m_00_BOUND;MISSING_M_L_00_BOUND;MISSING_M_m_00_KERNEL;MISSING_M_L_00_KERNEL",
            "priority": "HIGH",
            "candidate_status": "MISSING_KERNEL_BOUND_ROWS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "blocks_before_runner_use": "M_m_00_KERNEL;M_L_00_KERNEL;KERNEL_UNITS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "IPA1294_5_connection_domain_boundary",
            "input_name": "connection/domain/boundary pieces",
            "missing_token": "MISSING_K_CONN_BOUND;MISSING_K_DOMAIN_BOUND;MISSING_K_BOUNDARY_BOUND;MISSING_NO_FLUX_SOURCE",
            "priority": "MEDIUM",
            "candidate_status": "MISSING_CDB_AND_NO_FLUX_ROWS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1292_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv",
            "blocks_before_runner_use": "CONNECTION_BOUND;DOMAIN_BOUND;BOUNDARY_NO_FLUX",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    c_sign_candidate = [
        {
            "candidate_id": "CS1294_0_GK514_derivative_chain_sign",
            "input_name": "C_sign",
            "candidate_value": "+1_relative_to_K_metric_derivative_kernel",
            "convention_formula": "under S_GK=-int sqrt(-g) Gamma_eff and T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}, define Kmetric_chain with C_sign=+1 relative to the K_metric derivative response; the observable stress contribution carries the explicit minus sign in T_GK",
            "runner_interpretation": "can replace MISSING_C_SIGN only as C_SIGN_GK514_CANDIDATE_NONCLAIM in preview rows",
            "source_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv;source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "source_anchor": "GK514_A_metric_response_scalar_density;MR514_1_Khat_metric_response;KGL776_0_volume_piece",
            "required_before_promotion": "fix covariant/contravariant Hilbert variation convention; lock volume subtraction; prove K_hat=K_metric including derivative/boundary terms; attach response operator",
            "current_status": "SOURCE_BACKED_CONVENTION_CANDIDATE_NOT_PROMOTED",
            "replaces_missing_token": "MISSING_C_SIGN",
            "usable_in_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    patch_preview = []
    for row in runner_rows:
        preview_inputs, applied, remaining = preview_required_inputs(row.get("required_inputs", ""))
        response_missing = any(token in remaining for token in ["MISSING_RESPONSE_OPERATOR", "MISSING_OBSERVABLE_RESPONSE_MATRIX", "MISSING_LOCAL_RESPONSE_LIMITS"])
        patch_preview.append(
            {
                "preview_id": f"RPP1294_{len(patch_preview)}",
                "runner_id": row.get("runner_id", ""),
                "residual_component": row.get("residual_component", ""),
                "c_sign_candidate_applied": applied,
                "replaced_tokens": "MISSING_C_SIGN -> C_SIGN_GK514_CANDIDATE_NONCLAIM" if applied else "NONE",
                "required_inputs_original": row.get("required_inputs", ""),
                "required_inputs_preview": preview_inputs,
                "remaining_missing_count": len(remaining),
                "remaining_missing_tokens": ";".join(remaining) if remaining else "NONE",
                "response_operator_missing": response_missing,
                "runner_status": "PREVIEW_REJECTED_NONCLAIM_NO_SCORE" if remaining or response_missing else "PREVIEW_STILL_NONCLAIM_NOT_SCORED",
                "score_emitted": False,
                "score_value": "",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    response_blockers = [
        {
            "blocker_id": "ROB1294_0_Newton_source",
            "arena": "Newton/source normalization",
            "missing_operator": "R_Newton_chain or K00/source-normalization map",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "RMR1288_0_Newton_source",
            "current_status": "MISSING_KBAR_L_LOC_00_AND_SOURCE_MODEL",
            "blocks_runner_rows": "RRI1292_0_m_chain;RRI1292_1_Lcg_chain;RRI1292_3_chain_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ROB1294_1_PPN",
            "arena": "PPN gamma/beta/preferred-frame",
            "missing_operator": "R_PPN_chain and preferred-frame/projector maps",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "RMR1288_1_PPN_gamma_beta",
            "current_status": "MISSING_RESPONSE_MATRIX",
            "blocks_runner_rows": "all RRI1292 rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ROB1294_2_clock_orbital",
            "arena": "clock/orbital",
            "missing_operator": "R_clock_chain and R_orbital_chain with source/domain normalization",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "RMR1288_3_clock_readout;RMR1288_4_orbital_projection",
            "current_status": "MISSING_CLOCK_READOUT_COEFFICIENTS;MISSING_ORBITAL_FORCE_KERNEL",
            "blocks_runner_rows": "all RRI1292 rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ROB1294_3_R10",
            "arena": "R10 short-range/fifth-force",
            "missing_operator": "R_R10(lambda) plus range/source profile",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "RMR1288_5_R10_short_range",
            "current_status": "MISSING_R10_PROJECTION",
            "blocks_runner_rows": "RRI1292_0_m_chain_if_finite_range;RRI1292_3_chain_vector_if_finite_range",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "ROB1294_4_WEP_all_local",
            "arena": "WEP/all-local",
            "missing_operator": "matter descent theorem and full local response matrix",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "RMR1288_6_WEP_readout;RMR1288_7_response_verdict",
            "current_status": "MISSING_MATTER_DESCENT_PROOF;NONCLAIM_TEMPLATE_ONLY",
            "blocks_runner_rows": "all local claim rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1294_0_source_backed_input_candidate",
            "claim": "private C_sign source-backed convention candidate exists",
            "current_status": "SATISFIED_FOR_NONCLAIM_INPUT_PACK",
            "reason": "GK514/MR514/KGL776 provide a convention branch for C_sign but also demand fixed sign/volume/Khat closure before promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1294_1_Csign_runner_promotion",
            "claim": "C_sign can be used in scoring runner rows",
            "current_status": "BLOCKED_NOT_PROMOTED",
            "reason": "volume subtraction, covariant/contravariant variation convention, K_hat=K_metric, and derivative/boundary terms remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1294_2_response_operator",
            "claim": "local response operators exist for Newton/PPN/clock/orbital/R10/WEP",
            "current_status": "BLOCKED_MISSING_RESPONSE_OPERATOR",
            "reason": "1288 keeps the full response matrix and arena maps missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1294_3_runner_score",
            "claim": "chain-kernel residual rows can emit a numeric score",
            "current_status": "BLOCKED_REJECTED_NONCLAIM_NO_SCORE",
            "reason": "patch preview only replaces C_sign as nonclaim; all runner rows still contain MISSING tokens and nonclaim flags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1294_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "no response score, no promoted C_sign, no source-backed m/Lcg/kernel/boundary input pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1294_0_choose_Csign_first",
            "decision": "acquire C_sign as the first source-backed input candidate",
            "because": "C_sign is explicitly missing in RRI1292 m/Lcg rows and GK514 provides the closest source-backed convention branch",
            "next_action": "try to promote C_sign by locking Hilbert sign, volume subtraction, and K_hat/K_metric equality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1294_1_do_not_promote",
            "decision": "keep C_sign out of live scoring",
            "because": "the same sources that suggest the convention also state that fixed sign/volume/Khat matching is required before claims",
            "next_action": "build a promotion test or switch to response-operator sourcing if sign lock fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1294_2_runner_stays_rejected",
            "decision": "leave chain residual runner in rejection/no-score state",
            "because": "preview rows retain missing m, L_cg, kernel, CDB, and response inputs",
            "next_action": "fill missing input packs one at a time without weakening claim gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1294_0_1295",
            "target_file": "1295-Y5-R10-RAB-Csign-promotion-test-or-first-response-operator-source.md",
            "target_script": "scripts/Y5_R10_RAB_Csign_promotion_test_or_first_response_operator_source.py",
            "task": "try to lock the sign/volume/Khat convention enough to promote C_sign; if promotion fails, acquire the first source-backed local response operator row",
            "success_condition": "C_sign becomes usable_in_runner=true with source-backed sign lock, or one response operator becomes a source-backed nonclaim row",
            "do_not": "do not score chain residuals or claim local GR until runner rows have no MISSING inputs and response operators are sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(INPUT_PRIORITY_PATH, input_priority)
    write_csv(C_SIGN_CANDIDATE_PATH, c_sign_candidate)
    write_csv(PATCH_PREVIEW_PATH, patch_preview)
    write_csv(RESPONSE_BLOCKERS_PATH, response_blockers)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1294_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1294_1_Csign_candidate_acquired",
            "C_sign candidate exists as source-backed nonclaim row",
            len(c_sign_candidate) == 1
            and c_sign_candidate[0]["candidate_id"] == "CS1294_0_GK514_derivative_chain_sign"
            and c_sign_candidate[0]["candidate_value"].startswith("+1")
            and is_false(c_sign_candidate[0]["valid_for_claim"]),
            str(c_sign_candidate[0]["current_status"]),
        )
    )
    validations.append(
        validation_row(
            "VAL1294_2_Csign_not_promoted",
            "C_sign remains unusable in live scoring until sign/volume/Khat gates close",
            is_false(c_sign_candidate[0]["usable_in_runner"]) and "NOT_PROMOTED" in str(c_sign_candidate[0]["current_status"]),
            str(c_sign_candidate[0]["required_before_promotion"]),
        )
    )
    csign_preview_rows = [row for row in patch_preview if row["c_sign_candidate_applied"] is True]
    validations.append(
        validation_row(
            "VAL1294_3_patch_preview_replaces_Csign_only",
            "patch preview replaces MISSING_C_SIGN only in m/Lcg rows",
            len(csign_preview_rows) == 2 and all("C_SIGN_GK514_CANDIDATE_NONCLAIM" in row["required_inputs_preview"] for row in csign_preview_rows),
            ";".join(row["runner_id"] for row in csign_preview_rows),
        )
    )
    validations.append(
        validation_row(
            "VAL1294_4_preview_rows_still_rejected",
            "all preview rows remain rejected/nonclaim/no-score",
            all("REJECTED" in row["runner_status"] and int(row["remaining_missing_count"]) > 0 for row in patch_preview),
            ";".join(f"{row['runner_id']}={row['remaining_missing_count']}" for row in patch_preview),
        )
    )
    validations.append(
        validation_row(
            "VAL1294_5_no_score_emitted",
            "no residual or local-GR score is emitted",
            all(is_false(row["score_emitted"]) and not row["score_value"] for row in patch_preview),
            "score_value blank and score_emitted=false for every preview row",
        )
    )
    validations.append(
        validation_row(
            "VAL1294_6_response_blockers_remain",
            "response operator blockers remain explicit",
            len(response_blockers) == 5 and all("MISSING" in row["current_status"] or "NONCLAIM" in row["current_status"] for row in response_blockers),
            f"response_blocker_rows={len(response_blockers)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        INPUT_PRIORITY_PATH,
        C_SIGN_CANDIDATE_PATH,
        PATCH_PREVIEW_PATH,
        RESPONSE_BLOCKERS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1294_7_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1294_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1294_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, input_priority, c_sign_candidate, patch_preview, response_blockers, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1294_10_next_target_1295",
            "next target routes to Csign promotion test or response-operator sourcing",
            next_target[0]["next_id"] == "NEXT1294_0_1295" and "Csign" in next_target[0]["target_file"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1294_11_overall",
            "overall 1294 validation",
            overall_pass,
            "1294 acquires a source-backed C_sign convention candidate, keeps it nonclaim/unpromoted, preserves runner rejection, and routes to promotion/response sourcing",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1294 Y5 R10 RAB chain-kernel response-operator or input-pack acquisition

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1294 acquires the first real input-pack candidate: `C_sign` has a source-backed GK514 convention branch, but it is **not promoted** into live scoring. The chain-kernel runner still rejects all rows because response operators, `m`, `L_cg`, kernel, and boundary inputs remain missing.

**Main progress:** `MISSING_C_SIGN` is no longer a vague blank in the private ledger; it is now a concrete nonclaim convention candidate tied to `S_GK=-∫sqrt(-g)Γ_eff` and `T_GK=Γ_eff g-K_metric`. The same source chain also says why this is not yet enough: sign/volume convention, `K_hat=K_metric`, derivative terms, and boundary terms still need a parent lock.

**Next derivation target:** try the sign-promotion proof first. If `C_sign` cannot be promoted cleanly, switch to sourcing the first local response operator row, because without response operators the runner cannot score even a fully specified residual amplitude.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Input Priority Audit

{markdown_table(input_priority, ["audit_id", "input_name", "missing_token", "priority", "candidate_status", "source_path", "blocks_before_runner_use", "valid_for_claim", "claim_allowed"])}

## C Sign Convention Candidate

{markdown_table(c_sign_candidate, ["candidate_id", "input_name", "candidate_value", "convention_formula", "runner_interpretation", "source_path", "source_anchor", "required_before_promotion", "current_status", "replaces_missing_token", "usable_in_runner", "valid_for_claim", "claim_allowed"])}

## Runner Patch Preview

{markdown_table(patch_preview, ["preview_id", "runner_id", "residual_component", "c_sign_candidate_applied", "replaced_tokens", "required_inputs_preview", "remaining_missing_count", "remaining_missing_tokens", "response_operator_missing", "runner_status", "score_emitted", "score_value", "valid_for_claim", "claim_allowed"])}

## Response Operator Blockers

{markdown_table(response_blockers, ["blocker_id", "arena", "missing_operator", "source_path", "source_anchor", "current_status", "blocks_runner_rows", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

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
