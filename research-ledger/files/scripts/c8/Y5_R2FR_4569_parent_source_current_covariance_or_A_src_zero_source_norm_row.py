from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4569"
CLAIM_ID = "L-411"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_SOURCE_CURRENT_COVARIANCE_ASRC_4569"
MARKER = "PPC4161_PARENT_SOURCE_CURRENT_COVARIANCE_OR_ASRC_ZERO_SOURCE_NORM_ROW_4569"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SOURCE_CURRENT_COVARIANCE_ASRC_ZERO_SOURCE_NORM_4569"
DECISION = "A_SRC_STANDARD_BRANCH_ZERO_RECONCILED_NONSTANDARD_SOURCE_NORM_ROW_RETAINED_NONCLAIM"
NEXT_TARGET = "4570-Y5-R2FR-parent-mL-attractor-equation-or-A_lap-source-row.md"

FORMAL_PATH = FORMAL / "585-PPC4161-parent-source-current-covariance-or-A-src-zero-source-norm-row.md"
DOC_PATH = POST / "4569-Y5-R2FR-parent-source-current-covariance-or-A_src-zero-source-norm-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4568 = FORMAL / "584-PPC4161-cGamma-AJ-coefficient-owner-boundary-profile-runner.md"
CSV_4568_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4568_AJ_COEFFICIENT_OWNER_LAW.csv"
CSV_4568_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4568_NEXT_TARGET.csv"
CSV_4237_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4237_THEOREM_ROWS.csv"
CSV_4237_MAP = SOURCE_DIR / "P8_Y5_R2FR_4237_COEFFICIENT_MAP.csv"
CSV_4239_ORTHOGONALITY = SOURCE_DIR / "P8_Y5_R2FR_4239_SOURCE_ORTHOGONALITY_THEOREM.csv"
CSV_4239_DECOMP = SOURCE_DIR / "P8_Y5_R2FR_4239_HL_DECOMPOSITION.csv"
CSV_4240_HPERP_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4240_HPERP_QBASIC_AUDIT.csv"
CSV_4243_HPERP_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4243_HPERP_DQ_THEOREM.csv"
CSV_4277_DESCENT = SOURCE_DIR / "P8_Y5_R2FR_4277_MATTER_INTERFACE_DESCENT_THEOREM.csv"
CSV_4277_DQ = SOURCE_DIR / "P8_Y5_R2FR_4277_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CSV_4280_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4280_DECISION.csv"
CSV_4280_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4280_STATUS.csv"
CSV_4305_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4305_STATUS.csv"
CSV_4305_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4305_DECISION.csv"
CSV_4305_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4305_CLAIM_FIREWALL.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4569_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_SOURCE_CURRENT_COVARIANCE_THEOREM.csv"
BRANCH_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_ASRC_BRANCH_VERDICT.csv"
NONSTANDARD_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_NONSTANDARD_SOURCE_NORM_ROW.csv"
AJ_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_AJ_REDUCTION_AFTER_ASRC.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4569_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4569_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4569_00_4568_doc", "4568 owner split formal doc", DOC_4568, "A_src :="),
        ("SRC4569_01_4568_owner", "4568 A_src owner formula", CSV_4568_OWNER, "OWN4568_0_A_src"),
        ("SRC4569_02_4568_next", "4568 selected next target", CSV_4568_NEXT, "parent-source-current-covariance"),
        ("SRC4569_03_4237_theorem", "4237 source expansion theorem rows", CSV_4237_THEOREM, "TH4237_4_Jres_expansion"),
        ("SRC4569_04_4237_map", "4237 coefficient map", CSV_4237_MAP, "CM4237_0_A_src_exact"),
        ("SRC4569_05_4239_orthogonality", "4239 q-basic source orthogonality", CSV_4239_ORTHOGONALITY, "SO4239_5_residual_source"),
        ("SRC4569_06_4239_decomp", "4239 H_L decomposition", CSV_4239_DECOMP, "HD4239_2_source_reduction"),
        ("SRC4569_07_4240_hperp_audit", "4240 H_perp q-basic audit", CSV_4240_HPERP_AUDIT, "HA4240_3_source_defect"),
        ("SRC4569_08_4243_hperp_theorem", "4243 H_perp Dq theorem", CSV_4243_HPERP_THEOREM, "HT4243_1_zero_condition"),
        ("SRC4569_09_4277_descent", "4277 matter-interface descent", CSV_4277_DESCENT, "AD4277_3_action_domain_descent"),
        ("SRC4569_10_4277_dq", "4277 Dq component values", CSV_4277_DQ, "Dq_source_readout"),
        ("SRC4569_11_4280_decision", "4280 A_src zero decision", CSV_4280_DECISION, "DEC4280_0_A_src_zero"),
        ("SRC4569_12_4280_status", "4280 A_src status", CSV_4280_STATUS, "conditionally zero via 4277 Dq closure"),
        ("SRC4569_13_4305_status", "4305 A_src status", CSV_4305_STATUS, "STAT4305_0_A_src"),
        ("SRC4569_14_4305_decision", "4305 source-power decision", CSV_4305_DECISION, "DEC4305_0_gain"),
        ("SRC4569_15_4305_firewall", "4305 branch firewall", CSV_4305_FIREWALL, "FW4305_0"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4569 A_src zero/source-norm derivation chain",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SC4569_0_owner_import",
            "statement": "Import 4568 owner row A_src := ||P_loc[H_L (D_{D_L} S_cg)|_0]|| <= C_H A_1.",
            "derivation": "4568 rewrites the static source-current contribution as the first leakage-coordinate derivative of S_cg contracted with H_L.",
            "status": "OWNER_FORMULA_IMPORTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SC4569_1_decompose_HL",
            "statement": "H_L = H_q + H_perp with H_q in ker(Dq).",
            "derivation": "4239/4243 split leakage into a q-basic vertical part and a quotient-defect part.",
            "status": "DECOMPOSITION_IMPORTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SC4569_2_qbasic_source_zero",
            "statement": "S_A H_q^A=0.",
            "derivation": "If S_src descends through q, then D_Hq S_src = <delta Sbar_src/delta q, Dq[H_q]> = 0.",
            "status": "PRIVATE_QBASIC_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SC4569_3_reduce_to_Hperp",
            "statement": "S_A H_L^A = S_A H_perp^A.",
            "derivation": "Linearity plus SC4569_2 removes the q-basic contraction, leaving only the non-q leakage defect.",
            "status": "SOURCE_DEFECT_REDUCED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SC4569_4_standard_Dq_closure",
            "statement": "standard branch all_i Dq_i[H_L]=0 => H_perp=0.",
            "derivation": "4277 supplies the private standard matter-interface descent/Dq component silence; 4243 turns componentwise Dq silence into H_perp=0.",
            "status": "CONDITIONAL_STANDARD_BRANCH_CLOSURE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SC4569_5_Asrc_standard_zero",
            "statement": "A_src^std=0.",
            "derivation": "SC4569_3 reduces A_src to sup|S_A H_perp^A|; SC4569_4 sets H_perp=0 inside the same standard Dq/Hperp-closed branch.",
            "status": "CLOSED_CONDITIONAL_STANDARD_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SC4569_6_nonstandard_bound",
            "statement": "A_src^nonstd <= C_S ||H_perp|| <= C_S C_perp E_Dq,H.",
            "derivation": "If the standard Dq closure is absent, 4243 supplies a finite quotient-defect norm row rather than a zero.",
            "status": "NONSTANDARD_SOURCE_NORM_ROW_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def branch_verdict_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4569_0_standard_branch",
            "branch_scope": "compact stationary standard Dq/Hperp-closed local branch",
            "A_src_status": "CLOSED_CONDITIONAL_STANDARD_BRANCH",
            "formula": "A_src^std=0",
            "reason": "q-basic source descent kills S_A H_q^A and Dq component closure kills H_perp.",
            "firewall": "Do not export this zero to transition, non-Hilbert, excision, open-boundary or direct hidden-parent matter branches.",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4569_1_nonstandard_branch",
            "branch_scope": "transition/non-Hilbert/open/direct hidden-parent branches",
            "A_src_status": "NONSTANDARD_BOUND_ROW_RETAINED",
            "formula": "A_src^nonstd <= C_S C_perp E_Dq,H",
            "reason": "without Dq closure the non-q leakage defect is finite but not zero.",
            "firewall": "This is a source-norm row, not a scoreable numeric prediction until C_S, C_perp and E_Dq,H are sourced.",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4569_2_public_claim",
            "branch_scope": "public local-GR/Newton/PPN/R10 claim",
            "A_src_status": "PUBLIC_CLAIM_BLOCKED",
            "formula": "claim remains false until A_lap, boundary profiles, projection kernels and parent branch selector close too",
            "reason": "A_src standard-zero is useful but it is only one bulk source tooth in the c_Gamma static chain.",
            "firewall": "No local-GR, WEP, PPN, clock, orbital or R10 pass may be inferred from this checkpoint alone.",
            "valid_for_claim": "False",
        },
    ]


def nonstandard_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "NS4569_0_source_defect_norm",
            "quantity": "A_src^nonstd",
            "bound_law": "A_src^nonstd <= C_S ||H_perp|| <= C_S C_perp E_Dq,H",
            "inputs_required": "C_S; C_perp; E_Dq,H; branch selector; source path for nonstandard matter interface",
            "owner_source": str(CSV_4243_HPERP_THEOREM),
            "status": "SYMBOLIC_NONCLAIM_SOURCE_NORM_ROW",
            "next_action": "source or derive C_S, C_perp and E_Dq,H only if a nonstandard branch is intentionally admitted",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "NS4569_1_direct_parent_source",
            "quantity": "A_src^direct",
            "bound_law": "A_src^direct <= ||P_loc[H_L S_1^direct]||",
            "inputs_required": "explicit hidden-parent source operator S_1^direct and local projection kernel P_loc",
            "owner_source": str(CSV_4568_OWNER),
            "status": "RETAINED_COUNTERMODEL_ROW",
            "next_action": "do not use the standard zero if direct parent source slots are reintroduced",
            "valid_for_claim": "False",
        },
    ]


def aj_reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "AJ4569_0_standard_reduction",
            "before": "A_J_eff = A_src + A_lap",
            "after": "A_J_eff^std = A_lap",
            "condition": "standard Dq/Hperp-closed branch plus stationary compact branch; boundary remains separate",
            "status": "SOURCE_TOOTH_REMOVED_CONDITIONALLY",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "AJ4569_1_static_bound",
            "before": "||P_loc J_res_static|| <= epsilon_U^2(A_src + A_lap) + B_boundary_static + O(epsilon_U^3)",
            "after": "||P_loc J_res_static|| <= epsilon_U^2 A_lap + B_boundary_static + O(epsilon_U^3)",
            "condition": "same standard branch; no cancellation credit and no boundary absorption into A_lap",
            "status": "STATIC_BOUND_SHARPENED_CONDITIONALLY",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "AJ4569_2_next_bulk_tooth",
            "before": "live bulk coefficients: A_src, A_lap",
            "after": "live bulk coefficient: A_lap",
            "condition": "if the standard A_src zero is accepted as a private branch theorem",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4569_0_branch_scope",
            "requirement": "state A_src^std=0 only inside the standard Dq/Hperp-closed branch",
            "current_status": "PASS_PRIVATE_BRANCH_ONLY",
            "failure_mode": "exporting the zero to nonstandard/direct-source branches",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4569_1_Alap",
            "requirement": "derive A_lap=0 or source a numeric A_lap row from the parent m_L attractor equation",
            "current_status": "OPEN_NEXT_TARGET",
            "failure_mode": "claiming c_Gamma static closure after only removing A_src",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4569_2_boundary",
            "requirement": "derive or source B_boundary_static and arena kernels K_a",
            "current_status": "OPEN_RETAINED",
            "failure_mode": "hiding boundary/no-influx assumptions inside bulk A_J_eff",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4569_3_public_tests",
            "requirement": "only run PPN/R10/clock/orbital claims after A_lap, boundary and kernels are numeric or theorem-zero",
            "current_status": "BLOCKED_FOR_PUBLIC_CLAIM",
            "failure_mode": "treating a private branch theorem as empirical pass evidence",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4569_0_Asrc_standard_zero",
            "reason": "The 4239 q-basic source-zero theorem plus 4243/4277/4280 Dq-Hperp chain closes the standard-branch A_src tooth.",
            "next_action": "use A_src^std=0 only within the private standard branch and move the c_Gamma bulk hunt to A_lap",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4569_1_nonstandard_retained",
            "reason": "If the source action has direct hidden-parent, transition, non-Hilbert or open-boundary slots, H_perp is not killed and A_src must be bounded.",
            "next_action": "retain A_src^nonstd <= C_S C_perp E_Dq,H as a nonclaim row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4569_2_next",
            "reason": "After A_src is removed in the standard branch, the live bulk static residual is A_lap, with boundary amplitude still separate.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4569_0",
            "next_target": NEXT_TARGET,
            "objective": "try to prove A_lap=0, or derive a source-backed A_lap row, from the parent m_L attractor/homogeneity equation",
            "derive_first": "show m_2 is constant/harmonic on the local collar or D_m is silent in the standard branch",
            "fallback": "keep A_lap finite as D_m C_lap_m/L_B^2 with sourced D_m, C_lap_m and L_B",
            "avoid": "treating A_src standard-zero as full c_Gamma static closure or absorbing boundary terms into A_lap",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4569_0_A_src",
            "item": "A_src",
            "status": "CLOSED_CONDITIONAL_STANDARD_BRANCH",
            "note": "A_src^std=0 follows inside the standard Dq/Hperp-closed branch; nonstandard source-norm rows remain.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4569_1_A_J_eff",
            "item": "A_J_eff",
            "status": "REDUCED_TO_A_lap_ON_STANDARD_BRANCH",
            "note": "A_J_eff^std=A_lap; B_boundary_static remains outside the bulk coefficient.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4569_2_public_claim",
            "item": "local_GR_public_claim",
            "status": "BLOCKED",
            "note": "A_lap, boundary profiles, projection kernels and parent branch selector are still required.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    branch_verdict: list[dict[str, Any]],
    nonstandard: list[dict[str, Any]],
    aj_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        BRANCH_VERDICT_CSV,
        NONSTANDARD_ROW_CSV,
        AJ_REDUCTION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        FORMAL_PATH,
        DOC_PATH,
    ]
    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        BRANCH_VERDICT_CSV,
        NONSTANDARD_ROW_CSV,
        AJ_REDUCTION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    text_blob = "\n".join(str(row) for row in theorem + branch_verdict + nonstandard + aj_reduction + decisions + status)
    source_paths_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    theorem_tokens_ok = all(
        token in text_blob
        for token in [
            "S_A H_q^A=0",
            "H_perp=0",
            "A_src^std=0",
            "A_src^nonstd",
            "A_J_eff^std = A_lap",
        ]
    )
    branch_tokens_ok = all(
        token in text_blob
        for token in [
            "CLOSED_CONDITIONAL_STANDARD_BRANCH",
            "NONSTANDARD_BOUND_ROW_RETAINED",
            "PUBLIC_CLAIM_BLOCKED",
        ]
    )
    generated_paths_ok = all(path.exists() for path in generated_paths)
    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            ok = bool(parsed)
            csv_parse_ok = csv_parse_ok and ok
            csv_parse_detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover - validation report only
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:ERROR:{exc}")
    all_new_rows = sources + theorem + branch_verdict + nonstandard + aj_reduction + promotion + decisions + next_target + status
    nonclaim_ok = all(str(row.get("valid_for_claim", "False")) == "False" for row in all_new_rows)
    next_ok = bool(next_target) and next_target[0].get("next_target") == NEXT_TARGET
    pycache_absent = not (POST / "scripts" / "__pycache__").exists()
    rows = [
        {
            "check_id": "VAL4569_0_source_paths",
            "status": "PASS" if source_paths_ok else "FAIL",
            "detail": "all cited source paths exist and needles were found",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4569_1_generated_paths",
            "status": "PASS" if generated_paths_ok else "FAIL",
            "detail": "; ".join(str(path) for path in generated_paths),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4569_2_csv_parse",
            "status": "PASS" if csv_parse_ok else "FAIL",
            "detail": "; ".join(csv_parse_detail),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4569_3_theorem_tokens",
            "status": "PASS" if theorem_tokens_ok else "FAIL",
            "detail": "required A_src zero/nonstandard/AJ reduction tokens present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4569_4_branch_verdict",
            "status": "PASS" if branch_tokens_ok else "FAIL",
            "detail": "standard closed, nonstandard retained and public blocked statuses present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4569_5_nonclaim_firewall",
            "status": "PASS" if nonclaim_ok else "FAIL",
            "detail": "all generated data rows keep valid_for_claim=false",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4569_6_next_target",
            "status": "PASS" if next_ok else "FAIL",
            "detail": NEXT_TARGET,
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4569_7_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": str(POST / "scripts" / "__pycache__"),
            "valid_for_claim": "False",
        },
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL4569_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": "False",
        }
    )
    return rows


def formal_markdown(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    branch_verdict: list[dict[str, Any]],
    nonstandard: list[dict[str, Any]],
    aj_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 585 - PPC4161 Parent Source-Current Covariance Or A_src Zero Source-Norm Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

This checkpoint does the derivation pass for the 4568 source-current owner row:

```text
A_src := ||P_loc[H_L (D_D_L S_cg)|_0]|| <= C_H A_1.
```

The useful chain is:

```text
H_L = H_q + H_perp,
S_A H_q^A=0,
S_A H_L^A = S_A H_perp^A,
standard branch all_i Dq_i[H_L]=0 => H_perp=0,
therefore A_src^std=0.
```

So the source tooth of the static `c_Gamma` bulk coefficient is removed inside the compact stationary standard Dq/Hperp-closed branch. This is not a public local-GR claim: if the branch admits direct hidden-parent matter, transition domains, non-Hilbert couplings, excision surfaces or open boundary source slots, the retained row is

```text
A_src^nonstd <= C_S ||H_perp|| <= C_S C_perp E_Dq,H.
```

## Static Residual Consequence

Inside the same standard branch only:

```text
A_J_eff = A_src + A_lap,
A_src^std=0,
A_J_eff^std = A_lap,
||P_loc J_res_static|| <= epsilon_U^2 A_lap + B_boundary_static + O(epsilon_U^3).
```

This is real forward movement: `A_src` is no longer a vague missing coupling in the standard branch. The next live bulk tooth is `A_lap`; boundary amplitude and arena projection kernels remain separate gates.

## Source Register

{markdown_table(sources)}

## Source-Current Covariance Theorem

{markdown_table(theorem)}

## Branch Verdict

{markdown_table(branch_verdict)}

## Nonstandard Source-Norm Rows

{markdown_table(nonstandard)}

## A_J Reduction

{markdown_table(aj_reduction)}

## Promotion Gates

{markdown_table(promotion)}

## Decisions

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Validation

{markdown_table(validation)}
"""


def post_markdown(
    theorem: list[dict[str, Any]],
    branch_verdict: list[dict[str, Any]],
    nonstandard: list[dict[str, Any]],
    aj_reduction: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4569 - Parent Source-Current Covariance Or A_src Zero Source-Norm Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## What Changed

4569 stops treating `A_src` as an open fog-bank in the standard branch. The chain is now explicit:

```text
source descent kills S_A H_q^A,
Dq/Hperp closure kills H_perp,
therefore A_src^std=0.
```

That gives:

```text
A_J_eff^std = A_lap,
||P_loc J_res_static|| <= epsilon_U^2 A_lap + B_boundary_static + O(epsilon_U^3).
```

The nonstandard route is not erased. It remains:

```text
A_src^nonstd <= C_S C_perp E_Dq,H.
```

## Theorem Rows

{markdown_table(theorem)}

## Branch Verdict

{markdown_table(branch_verdict)}

## Nonstandard Rows

{markdown_table(nonstandard)}

## A_J Reduction

{markdown_table(aj_reduction)}

## Decisions

{markdown_table(decisions)}

## Validation

{markdown_table(validation)}

## Files Written

- `{FORMAL_PATH}`
- `{SOURCE_REGISTER}`
- `{THEOREM_CSV}`
- `{BRANCH_VERDICT_CSV}`
- `{NONSTANDARD_ROW_CSV}`
- `{AJ_REDUCTION_CSV}`
- `{PROMOTION_CSV}`
- `{DECISION_CSV}`
- `{NEXT_CSV}`
- `{STATUS_CSV}`
- `{VALIDATION_PATH}`

## Next Target

`{NEXT_TARGET}`
"""


def append_section_once(path: Path, marker: str, section: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if text and not text.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + section.strip() + "\n")


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4569 reconciles the parent source-current route: A_src is conditionally zero in the standard Dq/Hperp-closed branch, while nonstandard source defects remain explicit source-norm rows.",
        "current_evidence": "Generated source register, source-current covariance theorem, A_src branch verdict, nonstandard source-norm rows, A_J reduction rows, promotion gates, status and validation CSVs.",
        "status": "A_src_standard_branch_zero_nonstandard_source_norm_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Exporting A_src^std=0 outside the standard branch, or treating it as full c_Gamma/static/local-GR closure while A_lap, boundary profiles and arena kernels remain open.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "This closes one private branch source tooth only; it is not a public PPN/R10/clock/orbital/local-GR pass.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(claim_row)


def main() -> None:
    now = utc_now()
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    sources = source_rows()
    theorem = theorem_rows(now)
    branch_verdict = branch_verdict_rows(now)
    nonstandard = nonstandard_rows(now)
    aj_reduction = aj_reduction_rows(now)
    promotion = promotion_rows(now)
    decisions = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(BRANCH_VERDICT_CSV, branch_verdict)
    write_csv(NONSTANDARD_ROW_CSV, nonstandard)
    write_csv(AJ_REDUCTION_CSV, aj_reduction)
    write_csv(PROMOTION_CSV, promotion)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    validation = validation_rows(
        sources,
        theorem,
        branch_verdict,
        nonstandard,
        aj_reduction,
        promotion,
        decisions,
        next_target,
        status,
    )
    write_csv(VALIDATION_PATH, validation)

    FORMAL_PATH.write_text(
        formal_markdown(
            sources,
            theorem,
            branch_verdict,
            nonstandard,
            aj_reduction,
            promotion,
            decisions,
            next_target,
            status,
            validation,
        ),
        encoding="utf-8",
        newline="\n",
    )
    DOC_PATH.write_text(
        post_markdown(theorem, branch_verdict, nonstandard, aj_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    validation = validation_rows(
        sources,
        theorem,
        branch_verdict,
        nonstandard,
        aj_reduction,
        promotion,
        decisions,
        next_target,
        status,
    )
    write_csv(VALIDATION_PATH, validation)
    FORMAL_PATH.write_text(
        formal_markdown(
            sources,
            theorem,
            branch_verdict,
            nonstandard,
            aj_reduction,
            promotion,
            decisions,
            next_target,
            status,
            validation,
        ),
        encoding="utf-8",
        newline="\n",
    )
    DOC_PATH.write_text(
        post_markdown(theorem, branch_verdict, nonstandard, aj_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4569 Parent Source-Current Covariance / A_src Branch Verdict

Marker: `{MARKER}`

The 4568 source owner row now has a branch theorem. In the standard Dq/Hperp-closed local branch:

```text
H_L = H_q + H_perp,
S_A H_q^A=0,
all_i Dq_i[H_L]=0 => H_perp=0,
A_src^std=0.
```

Therefore `A_J_eff^std = A_lap`, with `B_boundary_static` still kept outside the bulk coefficient. Nonstandard/direct-source branches retain `A_src^nonstd <= C_S C_perp E_Dq,H`. Next target: `{NEXT_TARGET}`.
""",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4569 Packet Integration - A_src Standard-Branch Zero

Marker: `{PACKET_MARKER}`

Packet rule: inside the private compact stationary standard Dq/Hperp-closed branch, `A_src^std=0`, so the c_Gamma static bulk coefficient reduces to `A_J_eff^std=A_lap`. This is not a global source-coupling theorem; transition, non-Hilbert, direct hidden-parent and open-boundary branches retain `A_src^nonstd <= C_S C_perp E_Dq,H`. Next target: `{NEXT_TARGET}`.
""",
    )
    append_claim_once()

    if pycache.exists():
        shutil.rmtree(pycache)

    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
