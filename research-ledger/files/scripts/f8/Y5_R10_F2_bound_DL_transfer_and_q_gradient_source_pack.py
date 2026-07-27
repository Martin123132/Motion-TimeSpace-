from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "839-Y5-R10-F2-bound-DL-transfer-and-q-gradient-source-pack.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_839_SOURCE_REGISTER.csv"
F2_SOURCE_PACK_PATH = RESIDUALS / "P8_Y5_R10_839_F2_SOURCE_PACK.csv"
DL_TRANSFER_PACK_PATH = RESIDUALS / "P8_Y5_R10_839_DL_TRANSFER_PACK.csv"
GRADIENT_PACK_PATH = RESIDUALS / "P8_Y5_R10_839_Q_GRADIENT_PACK.csv"
SMOKE_ROWS_PATH = RESIDUALS / "P8_Y5_R10_839_CGAMMA_SMOKE_ROWS.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_839_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_839_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_839_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_839_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_839_VALIDATION.csv"

STATUS = "Y5_R10_839_source_pack_fills_closure_smoke_coefficients_parent_theorem_missing_nonclaim"
CLAIM_CEILING = "closure_smoke_coefficient_pack_only_no_parent_F2_CDU_or_transition_shell_pass"
NEXT_TARGET = "840-Y5-R10-parent-sign-F2-CDU-or-transition-quarantine-contract.md"

WINDOW43_U_B = 3.7965595357794454e-7
POINT_MASS_U_B = math.sqrt(9.458639468826237e-27)
DELTA_B_CLOSURE = 0.5
C_B_CLOSURE = 1.0 / DELTA_B_CLOSURE
F2_BOUND_CLOSURE = 1.0
C_DU_CLOSURE = 1.0
C_GAMMA_DIMLESS_CLOSURE = F2_BOUND_CLOSURE * C_DU_CLOSURE**2

SOURCE_SPECS = [
    {
        "source_id": "838_doc",
        "path": POST_CHECKPOINT / "838-Y5-R10-active-Gamma-coefficient-source-pack-or-parent-derivation.md",
        "needles": [
            "conditional active-Gamma coefficient law",
            "C_gamma_U <= C_gamma_D C_DU^2",
            "839-Y5-R10-F2-bound-DL-transfer-and-q-gradient-source-pack.md",
        ],
        "role": "immediate coefficient-law handoff",
    },
    {
        "source_id": "838_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_838_VALIDATION.csv",
        "needles": [
            "V838_4_coefficient_law_derived,pass",
            "V838_6_numeric_inputs_block_claim,pass",
            "V838_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "parent_DL_fixed_point_silence",
        "path": FORMALIZATION / "122-parent-DL-fixed-point-silence.md",
        "needles": [
            "F_1=0",
            "D_L = U_B H_L(X_B).",
            "H_L is not derived",
        ],
        "role": "partial F1 silence and conditional D_L transfer",
    },
    {
        "source_id": "local_leakage_vector_invariant",
        "path": FORMALIZATION / "125-local-leakage-vector-invariant.md",
        "needles": [
            "D_L <= U_B",
            "H_L and G_AB = not parent-derived",
            "U_B = 3.7965595357794454e-7",
        ],
        "role": "candidate algebraic C_DU=1 transfer and proxy U_B",
    },
    {
        "source_id": "trace_coupling_gate",
        "path": POST_CHECKPOINT / "95-trace-coupling-aF-normalization-gate.md",
        "needles": [
            "F_2 = a_F lambda_R.",
            "a_F = 1 is locally plausible if lambda_R is order-one or smaller",
            "a_F=1 remains an explicit closure convention",
        ],
        "role": "F2 coefficient factorization and closure warning",
    },
    {
        "source_id": "dimensional_ledger",
        "path": FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
        "needles": [
            "[L_cg] = L",
            "[F_2] = 1",
            "F_2 = a_F lambda_R",
        ],
        "role": "units for L_cg, F2, a_F, and lambda_R",
    },
    {
        "source_id": "equation_register_gradient",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "Delta_B = 0.5",
            "|nabla U_B| <= C_U U_B/L_B.",
            "D_L derivation overclaim",
        ],
        "role": "logistic-gradient source and overclaim guard",
    },
    {
        "source_id": "transition_shell_projector_gate",
        "path": FORMALIZATION / "133-exact-transition-cancellation-or-projector-theorem.md",
        "needles": [
            "exact_Khat_cancellation_parent_derived = false",
            "P_metric_projector_suppression_parent_derived = false",
            "conservation_owned_quarantine_only = true",
        ],
        "role": "transition-shell blocker for full local-GR claim",
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


def f2_source_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "item_id": "F2839_0_formula",
            "input_name": "F2_relation",
            "value_or_formula": "F_2 = a_F lambda_R",
            "source_status": "source_backed_formula",
            "claim_status": "formula_only_not_numeric_bound",
            "missing_to_promote": "derive or source a_F and lambda_R bounds from the parent action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "F2839_1_aF",
            "input_name": "a_F",
            "value_or_formula": "a_F=1",
            "source_status": "canonical_closure_convention",
            "claim_status": "not_parent_derived",
            "missing_to_promote": "trace-projection Ward identity or normalization theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "F2839_2_lambdaR",
            "input_name": "lambda_R",
            "value_or_formula": "lambda_R<=1 preferred for local safety; order-one grid explored",
            "source_status": "toy_guard_not_theorem",
            "claim_status": "not_parent_derived",
            "missing_to_promote": "parent potential curvature or mobility relation fixing lambda_R",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "F2839_3_F2_bound_smoke",
            "input_name": "F2_bound",
            "value_or_formula": f"{F2_BOUND_CLOSURE:.12g}",
            "source_status": "closure_smoke_from_aF1_lambdaR_le_1",
            "claim_status": "usable_for_plumbing_only",
            "missing_to_promote": "replace with parent-signed F2_bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def dl_transfer_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "item_id": "DL839_0_fixed_point",
            "input_name": "F1_silence",
            "value_or_formula": "F_1=0 from projection-locking partial_m Gamma_eff|m_L=0",
            "source_status": "partial_parent_support",
            "claim_status": "not_full_local_GR",
            "missing_to_promote": "prove D_L is the parent fixed-point coordinate for every tested local branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "DL839_1_transfer_formula",
            "input_name": "D_L_transfer",
            "value_or_formula": "D_L = U_B H_L(X_B); if 0<=H_L<=C_D then D_L<=C_D U_B",
            "source_status": "conditional_formula",
            "claim_status": "H_L_not_parent_derived",
            "missing_to_promote": "derive bounded H_L from parent invariant bundle",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "DL839_2_ZL_algebraic_transfer",
            "input_name": "C_DU",
            "value_or_formula": f"{C_DU_CLOSURE:.12g}",
            "source_status": "candidate_algebraic_bound_if_HL_components_bounded_and_G_normalized",
            "claim_status": "closure_smoke_only",
            "missing_to_promote": "parent-sign H_L components and G_AB normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gradient_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "item_id": "GR839_0_logistic_gradient",
            "input_name": "C_B",
            "value_or_formula": f"C_B=1/Delta_B={C_B_CLOSURE:.12g} for Delta_B={DELTA_B_CLOSURE:.12g}",
            "source_status": "source_backed_logistic_closure",
            "claim_status": "far_local_only",
            "missing_to_promote": "parent-sign universal Delta_B and L_B domain for tested systems",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "GR839_1_far_local_q_gradient",
            "input_name": "far_local_q_gradient",
            "value_or_formula": "|nabla gamma_act| <= 2 C_gamma_U C_B U_B^2/L_B plus coefficient/L_cg gradients",
            "source_status": "conditional_far_local_bound",
            "claim_status": "not_transition_shell_safe",
            "missing_to_promote": "bound nabla C_gamma_U, nabla L_cg, Khat divergence, and metric response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "item_id": "GR839_2_transition_shell",
            "input_name": "transition_shell",
            "value_or_formula": "U_B=O(1) in shell; exact cancellation/projector not parent-derived",
            "source_status": "blocker_source_backed",
            "claim_status": "blocks_full_local_GR",
            "missing_to_promote": "derive exact projector/cancellation or conservation-owned quarantine equations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def smoke_rows(generated_utc: str) -> list[dict[str, object]]:
    cases = [
        ("SM839_0_window43_far_local", WINDOW43_U_B, "window43_U_B from local leakage invariant/source-support"),
        ("SM839_1_point_mass_far_local", POINT_MASS_U_B, "point-mass U_B from 836 proxy"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, u_b, provenance in cases:
        amplitude = C_GAMMA_DIMLESS_CLOSURE * u_b**2
        gradient_prefactor = 2.0 * C_B_CLOSURE * C_GAMMA_DIMLESS_CLOSURE * u_b**2
        rows.append(
            {
                "row_id": row_id,
                "U_B": f"{u_b:.16e}",
                "F2_bound": f"{F2_BOUND_CLOSURE:.12g}",
                "C_DU": f"{C_DU_CLOSURE:.12g}",
                "C_B": f"{C_B_CLOSURE:.12g}",
                "dimensionless_gamma_bound": f"{amplitude:.16e}",
                "dimensionless_gradient_prefactor": f"{gradient_prefactor:.16e}",
                "provenance": provenance,
                "claim_status": "closure_smoke_only_missing_parent_theorem_and_response",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG839_0_no_numeric_Cgamma_claim",
            "claim": "C_gamma_U is now source-backed",
            "status": "forbidden",
            "reason": "F2_bound=1 and C_DU=1 are closure-smoke values, not parent-signed bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG839_1_no_transition_shell_claim",
            "claim": "far-local U_B^2 gradient suppression proves local GR",
            "status": "forbidden",
            "reason": "transition shell still has U_B=O(1) and lacks exact projector/cancellation theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG839_2_allowed_private_result",
            "claim": "closure-smoke source pack can test runner plumbing",
            "status": "allowed_private_nonclaim",
            "reason": "all smoke rows are explicitly nonclaim and identify parent inputs needed for promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D839_0",
            "finding": "F2 source formula found",
            "reason": "F_2=a_F lambda_R with a_F=1 and lambda_R<=1 only as closure-smoke guard",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D839_1",
            "finding": "D_L transfer can be made algebraic in the Z_L candidate",
            "reason": "D_L<=U_B if H_L components are bounded and G_AB normalized; those are not parent-signed",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D839_2",
            "finding": "far-local gradient coefficient is available as closure smoke",
            "reason": "Delta_B=0.5 gives C_B=2, but transition-shell and Khat/metric response still block local-GR claim",
            "status": CLAIM_CEILING,
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
            "objective": "try to parent-sign the F2/C_DU closure-smoke inputs or convert transition-shell quarantine into equations",
            "include": "Ward identity for a_F/lambda_R, H_L/G_AB parent derivation, L_cg-gradient silence, Khat/metric response, quarantine equations",
            "exclude": "local-GR claim, transition-shell handwave, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "filled a sourced closure-smoke coefficient pack for F2, C_DU, and C_B",
            "what_is_not_claimed": "parent-signed F2_bound, parent-signed C_DU, q_loc pass, transition-shell safety, local GR/Newton",
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
    f2_rows: list[dict[str, object]],
    dl_rows: list[dict[str, object]],
    gradient_rows: list[dict[str, object]],
    smoke: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_838_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    f2_found = any(row["item_id"] == "F2839_0_formula" for row in f2_rows)
    closure_f2_nonclaim = any(
        row["item_id"] == "F2839_3_F2_bound_smoke" and row["claim_status"] == "usable_for_plumbing_only"
        for row in f2_rows
    )
    dl_candidate = any(row["item_id"] == "DL839_2_ZL_algebraic_transfer" for row in dl_rows)
    cb_value = any(row["item_id"] == "GR839_0_logistic_gradient" and "C_B=1/Delta_B=2" in row["value_or_formula"] for row in gradient_rows)
    transition_block = any(row["item_id"] == "GR839_2_transition_shell" for row in gradient_rows)
    smoke_nonclaim = bool(smoke) and all(row["claim_status"].startswith("closure_smoke_only") for row in smoke)
    smoke_positive = all(float(row["dimensionless_gamma_bound"]) > 0.0 for row in smoke)
    guards_forbid = {"CG839_0_no_numeric_Cgamma_claim", "CG839_1_no_transition_shell_claim"}.issubset(
        {row["guard_id"] for row in guard_rows if row["status"] == "forbidden"}
    )
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, f2_rows, dl_rows, gradient_rows, smoke, guard_rows, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V839_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V839_1_prior_838_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V839_2_F2_formula_found",
            "result": "pass" if f2_found else "fail",
            "detail": "F_2=a_F lambda_R recorded",
        },
        {
            "check_id": "V839_3_F2_smoke_nonclaim",
            "result": "pass" if closure_f2_nonclaim else "fail",
            "detail": "F2_bound=1 is plumbing-only closure smoke",
        },
        {
            "check_id": "V839_4_DLU_candidate_recorded",
            "result": "pass" if dl_candidate else "fail",
            "detail": "D_L<=U_B candidate recorded as closure-only C_DU=1",
        },
        {
            "check_id": "V839_5_CB_gradient_value_recorded",
            "result": "pass" if cb_value else "fail",
            "detail": "Delta_B=0.5 gives C_B=2 for logistic-gradient smoke",
        },
        {
            "check_id": "V839_6_transition_shell_blocks_claim",
            "result": "pass" if transition_block else "fail",
            "detail": "transition shell remains a local-GR blocker",
        },
        {
            "check_id": "V839_7_smoke_rows_positive_nonclaim",
            "result": "pass" if smoke_nonclaim and smoke_positive else "fail",
            "detail": "smoke rows have positive bounds and remain nonclaim",
        },
        {
            "check_id": "V839_8_claim_guards_forbid_overclaim",
            "result": "pass" if guards_forbid and no_claim else "fail",
            "detail": "numeric Cgamma and local-GR claims remain forbidden",
        },
        {
            "check_id": "V839_9_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V839_10_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V839_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V839_12_validation_rows_ready",
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
    f2_rows: list[dict[str, object]],
    dl_rows: list[dict[str, object]],
    gradient_rows: list[dict[str, object]],
    smoke: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 839 - Y5 R10 F2 Bound, D_L Transfer, And q-Gradient Source Pack",
        "",
        "Current result: **we can fill a coherent closure-smoke coefficient pack, but it is still not parent-signed**. The corpus supports `F_2=a_F lambda_R`, gives `a_F=1` only as canonical closure, provides a candidate `D_L<=U_B` algebraic transfer if `H_L/G_AB` are bounded/normalized, and gives a logistic-gradient smoke constant `C_B=2` from `Delta_B=0.5`. This is useful runner plumbing, not a local-GR claim, because `F_2`, `C_DU`, `L_cg` gradients, `Khat` response, and transition-shell quarantine remain open.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## F2 Source Pack",
        "",
        csv_table(f2_rows, ["item_id", "input_name", "value_or_formula", "source_status", "claim_status", "missing_to_promote", "valid_for_claim"]),
        "",
        "## D_L Transfer Pack",
        "",
        csv_table(dl_rows, ["item_id", "input_name", "value_or_formula", "source_status", "claim_status", "missing_to_promote", "valid_for_claim"]),
        "",
        "## q-Gradient Pack",
        "",
        csv_table(gradient_rows, ["item_id", "input_name", "value_or_formula", "source_status", "claim_status", "missing_to_promote", "valid_for_claim"]),
        "",
        "## Closure Smoke Rows",
        "",
        csv_table(smoke, ["row_id", "U_B", "F2_bound", "C_DU", "C_B", "dimensionless_gamma_bound", "dimensionless_gradient_prefactor", "claim_status", "valid_for_claim"]),
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
    f2_rows = f2_source_pack_rows(generated_utc)
    dl_rows = dl_transfer_pack_rows(generated_utc)
    gradient_rows = gradient_pack_rows(generated_utc)
    smoke = smoke_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, f2_rows, dl_rows, gradient_rows, smoke, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(F2_SOURCE_PACK_PATH, f2_rows, ["item_id", "input_name", "value_or_formula", "source_status", "claim_status", "missing_to_promote", "valid_for_claim", "generated_utc"])
    write_csv(DL_TRANSFER_PACK_PATH, dl_rows, ["item_id", "input_name", "value_or_formula", "source_status", "claim_status", "missing_to_promote", "valid_for_claim", "generated_utc"])
    write_csv(GRADIENT_PACK_PATH, gradient_rows, ["item_id", "input_name", "value_or_formula", "source_status", "claim_status", "missing_to_promote", "valid_for_claim", "generated_utc"])
    write_csv(SMOKE_ROWS_PATH, smoke, ["row_id", "U_B", "F2_bound", "C_DU", "C_B", "dimensionless_gamma_bound", "dimensionless_gradient_prefactor", "provenance", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, f2_rows, dl_rows, gradient_rows, smoke, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
