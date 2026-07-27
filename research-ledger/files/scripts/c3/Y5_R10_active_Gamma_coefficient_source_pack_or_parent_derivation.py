from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "838-Y5-R10-active-Gamma-coefficient-source-pack-or-parent-derivation.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_838_SOURCE_REGISTER.csv"
SYMBOL_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_838_SYMBOL_LEDGER.csv"
PARENT_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_838_PARENT_DERIVATION_CONTRACT.csv"
COEFFICIENT_LAW_PATH = RESIDUALS / "P8_Y5_R10_838_COEFFICIENT_BOUND_LAW.csv"
NUMERIC_READINESS_PATH = RESIDUALS / "P8_Y5_R10_838_NUMERIC_READINESS.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_838_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_838_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_838_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_838_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_838_VALIDATION.csv"

STATUS = "Y5_R10_838_conditional_active_Gamma_coefficient_law_derived_numeric_inputs_missing_nonclaim"
CLAIM_CEILING = "conditional_coefficient_derivation_schema_only_no_numeric_Cgamma_no_local_GR_pass"
NEXT_TARGET = "839-Y5-R10-F2-bound-DL-transfer-and-q-gradient-source-pack.md"

SOURCE_SPECS = [
    {
        "source_id": "837_doc",
        "path": POST_CHECKPOINT / "837-Y5-R10-source-active-Gamma-coefficients-or-local-branch-closure-label.md",
        "needles": [
            "closure_input_acquisition_not_derived_local_GR",
            "CH837_0_C_D",
            "838-Y5-R10-active-Gamma-coefficient-source-pack-or-parent-derivation.md",
        ],
        "role": "immediate coefficient-hunt handoff",
    },
    {
        "source_id": "837_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_837_VALIDATION.csv",
        "needles": [
            "V837_2_coefficients_remain_unsourced,pass",
            "V837_7_next_target_selected,pass",
            "V837_8_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "836_doc",
        "path": POST_CHECKPOINT / "836-Y5-R10-fill-active-Gamma-bound-from-source-support-or-demote-local-branch.md",
        "needles": [
            "source-support fills useful form and proxy small-parameter values",
            "DG836_1_coefficients",
            "DG836_2_response",
        ],
        "role": "proxy suppression and missing coefficient record",
    },
    {
        "source_id": "800_double_zero_warning",
        "path": POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": [
            "pL=2 is not derived by Pi_B",
            "pT=2 is not derived by Pi_B",
            "not_derived_as_parent_theorem",
        ],
        "role": "warning that quadratic support cannot be obtained from the switch alone",
    },
    {
        "source_id": "equation_register_local_terms",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "L_cg^-2 F_L = Lambda_loc + D_L^2 F_2",
            "0 <= H_L <= C_D",
            "partial_m Gamma_eff|m_L = 0",
            "D_L derivation overclaim",
        ],
        "role": "formalization equations used to derive the conditional coefficient law",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def symbol_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "symbol_id": "SL838_0_alias_collision",
            "symbol": "C_D",
            "canonical_role": "ambiguous_do_not_use_unqualified",
            "current_usage": "837 uses C_D as active-Gamma/D_L^2 coefficient while the equation register also uses C_D as the D_L<=C_D U_B transfer bound",
            "replacement": "use C_gamma_D for active-Gamma coefficient and C_DU for D_L-to-U_B transfer",
            "status": "alias_collision_resolved_for_new_rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "symbol_id": "SL838_1_CgammaD",
            "symbol": "C_gamma_D",
            "canonical_role": "bound in |Gamma_eff-Lambda_loc| <= C_gamma_D D_L^2",
            "current_usage": "not numeric; derived conditionally from F2_bound and L_cg normalization",
            "replacement": "C_gamma_D <= L_cg^-2(F2_bound + R3_bound delta_D)",
            "status": "conditional_formula_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "symbol_id": "SL838_2_CDU",
            "symbol": "C_DU",
            "canonical_role": "bound in D_L <= C_DU U_B",
            "current_usage": "equation register gives 0<=H_L<=C_D and D_L<=C_D U_B, but C_D value/source is not numeric",
            "replacement": "source or derive numeric/symbolic upper bound C_DU from parent local branch",
            "status": "not_sourced_numeric",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "symbol_id": "SL838_3_CgammaU",
            "symbol": "C_gamma_U",
            "canonical_role": "bound in |Gamma_eff-Lambda_loc| <= C_gamma_U U_B^2",
            "current_usage": "induced only if C_gamma_D and C_DU are sourced",
            "replacement": "C_gamma_U <= C_gamma_D C_DU^2",
            "status": "conditional_formula_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "PC838_0_fixed_point_stationarity",
            "requirement": "F_1=partial_D Gamma_eff|D_L=0 = 0",
            "why_needed": "without stationarity the active residual is O(D_L) or O(U_B), not quadratic",
            "current_support": "equation register contains partial_m Gamma_eff|m_L=0 under projection locking",
            "missing_piece": "prove D_L is the parent fixed-point coordinate and not an inserted closure coordinate",
            "status": "conditional_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PC838_1_quadratic_coefficient_bound",
            "requirement": "source |F_2|<=F2_bound on the local branch",
            "why_needed": "C_gamma_D is controlled by the size of the quadratic coefficient",
            "current_support": "equation register has L_cg^-2 F_L = Lambda_loc + D_L^2 F_2",
            "missing_piece": "numeric or theorem-level F2_bound with source path and domain",
            "status": "missing_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PC838_2_remainder_control",
            "requirement": "bound O(D_L^3) remainder by R3_bound delta_D D_L^2",
            "why_needed": "a local Taylor law cannot be used outside its controlled neighbourhood",
            "current_support": "none beyond formal smooth expansion language",
            "missing_piece": "Taylor domain delta_D and third-derivative/remainder bound",
            "status": "missing_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PC838_3_D_to_U_transfer",
            "requirement": "D_L <= C_DU U_B",
            "why_needed": "turns the D_L^2 coefficient into a U_B^2 local-screening coefficient",
            "current_support": "equation register states 0<=H_L<=C_D and D_L<=C_D U_B but labels D_L derivation overclaim",
            "missing_piece": "derive or source C_DU from the parent local branch",
            "status": "missing_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PC838_4_scale_normalization",
            "requirement": "local L_cg normalization and dimensions must be fixed",
            "why_needed": "Gamma_eff has units L^-2 and coefficient comparisons need a concrete scale convention",
            "current_support": "equation register uses L_cg^-2 F_L but does not provide a claim-ready local coefficient normalization",
            "missing_piece": "source L_cg or keep coefficient symbolic with units",
            "status": "missing_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coefficient_law_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "CLAW838_0_Taylor_zero",
            "input_assumptions": "Gamma_eff(D_L,Y) is C2 near D_L=0; Gamma_eff(0,Y)=Lambda_loc; partial_D Gamma_eff(0,Y)=0",
            "derived_law": "Gamma_eff-Lambda_loc = D_L^2 F_2(D_L,Y)",
            "coefficient_bound": "|Gamma_eff-Lambda_loc| <= L_cg^-2 F2_bound D_L^2",
            "missing_for_claim": "parent proof of stationarity plus F2_bound and L_cg normalization",
            "status": "conditional_derivation_schema",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "CLAW838_1_remainder_safe_D_bound",
            "input_assumptions": "|F_2|<=F2_bound; |O(D_L^3)|<=R3_bound delta_D D_L^2 within |D_L|<=delta_D",
            "derived_law": "|Gamma_eff-Lambda_loc| <= C_gamma_D D_L^2",
            "coefficient_bound": "C_gamma_D <= L_cg^-2(F2_bound + R3_bound delta_D)",
            "missing_for_claim": "F2_bound, R3_bound, delta_D, and L_cg are not sourced",
            "status": "conditional_bound_formula",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "CLAW838_2_U_B_transfer",
            "input_assumptions": "D_L <= C_DU U_B and C_gamma_D bound exists",
            "derived_law": "|Gamma_eff-Lambda_loc| <= C_gamma_U U_B^2",
            "coefficient_bound": "C_gamma_U <= C_gamma_D C_DU^2",
            "missing_for_claim": "C_DU is not parent-derived or numeric",
            "status": "conditional_bound_formula",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "CLAW838_3_q_gradient_warning",
            "input_assumptions": "q_loc depends on nabla Gamma_eff, not just the amplitude of Gamma_eff-Lambda_loc",
            "derived_law": "|nabla gamma_act| <= 2 C_gamma_U U_B |nabla U_B| + |nabla C_gamma_U| U_B^2",
            "coefficient_bound": "with |nabla U_B|<=C_B U_B/L_B, first term is <=2 C_gamma_U C_B U_B^2/L_B",
            "missing_for_claim": "C_B, L_B, nabla C_gamma_U, and Khat divergence response are not sourced",
            "status": "q_bound_not_closed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def numeric_readiness_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "input_id": "NR838_0_F2_bound",
            "input_name": "F2_bound",
            "needed_for": "C_gamma_D",
            "current_value": "MISSING",
            "source_status": "not_sourced",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NR838_1_CDU",
            "input_name": "C_DU",
            "needed_for": "C_gamma_U",
            "current_value": "MISSING",
            "source_status": "equation form exists but numeric/theorem bound missing",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NR838_2_Lcg",
            "input_name": "L_cg_local_normalization",
            "needed_for": "units and coefficient scale",
            "current_value": "MISSING",
            "source_status": "symbolic only",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NR838_3_remainder_domain",
            "input_name": "R3_bound_and_delta_D",
            "needed_for": "finite Taylor domain",
            "current_value": "MISSING",
            "source_status": "not_sourced",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NR838_4_q_gradient_inputs",
            "input_name": "C_B_L_B_grad_Cgamma",
            "needed_for": "q_loc suppression rather than amplitude-only suppression",
            "current_value": "MISSING",
            "source_status": "not_sourced",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG838_0_no_Cgamma_claim",
            "claim": "C_gamma_D or C_gamma_U is sourced",
            "status": "forbidden",
            "reason": "838 derives the algebraic coefficient law but does not source F2_bound, C_DU, L_cg, or remainder bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG838_1_no_local_GR_claim",
            "claim": "MTS reduces to GR/Newton locally",
            "status": "forbidden",
            "reason": "q-gradient, Khat divergence, matter descent, and arena response remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG838_2_allowed_private_result",
            "claim": "active-Gamma coefficient has a conditional parent-contract law",
            "status": "allowed_private_nonclaim",
            "reason": "if stationarity, F2_bound, transfer, and remainder clauses are parent-signed, C_gamma_U follows as C_gamma_D C_DU^2",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D838_0",
            "finding": "active-Gamma coefficient law derived conditionally",
            "reason": "stationarity/F1=0 plus bounded quadratic term gives C_gamma_D; D_L<=C_DU U_B gives C_gamma_U",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D838_1",
            "finding": "numeric coefficient claim remains blocked",
            "reason": "F2_bound, C_DU, L_cg normalization, Taylor domain, and q-gradient inputs are missing",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D838_2",
            "finding": "C_D symbol collision resolved for future work",
            "reason": "separating C_gamma_D from C_DU prevents mixing active residual strength with D_L-to-U_B transfer",
            "status": "notation_cleaned_for_future_runner_rows",
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "source or derive F2_bound, C_DU, L_cg normalization, Taylor-domain control, and q-gradient inputs",
            "include": "F2_bound source pack, D_L<=C_DU U_B proof, L_cg units, C_B/L_B logistic-gradient constants, nonclaim runner update",
            "exclude": "local-GR claim, proxy-only pass, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "derived the conditional coefficient law and cleaned C_D notation",
            "what_is_not_claimed": "numeric C_gamma_D/C_gamma_U, q_loc suppression, local GR/Newton, PPN/R10/WEP pass",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    symbol_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_837_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    alias_resolved = any(row["symbol_id"] == "SL838_0_alias_collision" for row in symbol_rows)
    stationarity_recorded = any(row["contract_id"] == "PC838_0_fixed_point_stationarity" for row in parent_rows)
    coefficient_formula = any(row["law_id"] == "CLAW838_2_U_B_transfer" for row in coefficient_rows)
    q_warning = any(row["law_id"] == "CLAW838_3_q_gradient_warning" for row in coefficient_rows)
    readiness_blocked = all(row["ready"] == "false" for row in readiness_rows)
    guards_forbid = {"CG838_0_no_Cgamma_claim", "CG838_1_no_local_GR_claim"}.issubset(
        {row["guard_id"] for row in guard_rows if row["status"] == "forbidden"}
    )
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, symbol_rows, parent_rows, coefficient_rows, readiness_rows, guard_rows, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V838_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V838_1_prior_837_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V838_2_C_D_alias_resolved",
            "result": "pass" if alias_resolved else "fail",
            "detail": "C_D split into C_gamma_D and C_DU for future rows",
        },
        {
            "check_id": "V838_3_stationarity_clause_recorded",
            "result": "pass" if stationarity_recorded else "fail",
            "detail": "F1=0 is conditional on parent fixed-point stationarity",
        },
        {
            "check_id": "V838_4_coefficient_law_derived",
            "result": "pass" if coefficient_formula else "fail",
            "detail": "C_gamma_U <= C_gamma_D C_DU^2 recorded",
        },
        {
            "check_id": "V838_5_q_gradient_not_forgotten",
            "result": "pass" if q_warning else "fail",
            "detail": "q_loc needs gradient inputs, not amplitude-only coefficient",
        },
        {
            "check_id": "V838_6_numeric_inputs_block_claim",
            "result": "pass" if readiness_blocked else "fail",
            "detail": "all numeric readiness rows remain blocked",
        },
        {
            "check_id": "V838_7_claim_guards_forbid_overclaim",
            "result": "pass" if guards_forbid and no_claim else "fail",
            "detail": "C_gamma and local-GR claims remain forbidden",
        },
        {
            "check_id": "V838_8_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V838_9_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V838_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V838_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    symbol_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 838 - Y5 R10 Active-Gamma Coefficient Source Pack Or Parent Derivation",
        "",
        "Current result: **we derived the conditional active-Gamma coefficient law, but not the numeric coefficient**. If the parent local branch proves the fixed-point/stationarity clause `F_1=0`, bounds `F_2`, controls the Taylor remainder, and derives `D_L <= C_DU U_B`, then `|Gamma_eff-Lambda_loc| <= C_gamma_U U_B^2` with `C_gamma_U <= C_gamma_D C_DU^2`. The route is sharper, but still non-claim until those inputs are sourced.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Symbol Ledger",
        "",
        csv_table(symbol_rows, ["symbol_id", "symbol", "canonical_role", "current_usage", "replacement", "status", "valid_for_claim"]),
        "",
        "## Parent Derivation Contract",
        "",
        csv_table(parent_rows, ["contract_id", "requirement", "why_needed", "current_support", "missing_piece", "status", "valid_for_claim"]),
        "",
        "## Coefficient Bound Law",
        "",
        csv_table(coefficient_rows, ["law_id", "input_assumptions", "derived_law", "coefficient_bound", "missing_for_claim", "status", "valid_for_claim"]),
        "",
        "## Numeric Readiness",
        "",
        csv_table(readiness_rows, ["input_id", "input_name", "needed_for", "current_value", "source_status", "ready", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    symbol_rows = symbol_ledger_rows(generated_utc)
    parent_rows = parent_contract_rows(generated_utc)
    coefficient_rows = coefficient_law_rows(generated_utc)
    readiness_rows = numeric_readiness_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        symbol_rows,
        parent_rows,
        coefficient_rows,
        readiness_rows,
        guard_rows,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SYMBOL_LEDGER_PATH, symbol_rows, ["symbol_id", "symbol", "canonical_role", "current_usage", "replacement", "status", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_CONTRACT_PATH, parent_rows, ["contract_id", "requirement", "why_needed", "current_support", "missing_piece", "status", "valid_for_claim", "generated_utc"])
    write_csv(COEFFICIENT_LAW_PATH, coefficient_rows, ["law_id", "input_assumptions", "derived_law", "coefficient_bound", "missing_for_claim", "status", "valid_for_claim", "generated_utc"])
    write_csv(NUMERIC_READINESS_PATH, readiness_rows, ["input_id", "input_name", "needed_for", "current_value", "source_status", "ready", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, symbol_rows, parent_rows, coefficient_rows, readiness_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
