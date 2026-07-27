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

CHECKPOINT = "4572"
CLAIM_ID = "L-414"
BRANCH_ID = "MTS_R2FR_Y5_HIGHER_ORDER_STATIC_RESIDUE_TRANSITION_SHELL_4572"
MARKER = "PPC4161_HIGHER_ORDER_STATIC_RESIDUE_OR_TRANSITION_SHELL_PROFILE_ROW_4572"
PACKET_MARKER = "PPC4161_PACKET_HIGHER_ORDER_STATIC_RESIDUE_TRANSITION_SHELL_4572"
DECISION = "PRIVATE_HIGHER_ORDER_ARENA_RESIDUES_ZERO_TRANSITION_SHELL_PROFILE_ROWS_RETAINED_NONCLAIM"
NEXT_TARGET = "4573-Y5-R2FR-transition-shell-source-lift-or-Sigma_metric-profile-runner.md"

FORMAL_PATH = FORMAL / "588-PPC4161-higher-order-static-residue-or-transition-shell-profile-row.md"
DOC_PATH = POST / "4572-Y5-R2FR-higher-order-static-residue-or-transition-shell-profile-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4571 = FORMAL / "587-PPC4161-static-boundary-nohair-or-B-boundary-profile-kernel-row.md"
EQ_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
CSV_4571_STATIC = SOURCE_DIR / "P8_Y5_R2FR_4571_STATIC_REDUCTION_AFTER_BOUNDARY.csv"
CSV_4571_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4571_NEXT_TARGET.csv"
CSV_4571_PROFILE = SOURCE_DIR / "P8_Y5_R2FR_4571_ARENA_BOUNDARY_PROFILE_ROWS.csv"
CSV_4554_FINAL = SOURCE_DIR / "P8_Y5_R2FR_4554_ALPHA3_PRIVATE_BRANCH_FINAL_ZERO.csv"
CSV_4554_CUBIC = SOURCE_DIR / "P8_Y5_R2FR_4554_CUBIC_REPRESENTATION_THEOREM.csv"
CSV_4554_COUNTER = SOURCE_DIR / "P8_Y5_R2FR_4554_COUNTERMODEL_GUARDS.csv"
CSV_4556_XI_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4556_XI_PRIVATE_ZERO_CERTIFICATE.csv"
CSV_4556_XI_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4556_XI_CHANNEL_SPLIT.csv"
CSV_4557_ZETA_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4557_ZETA3_PRIVATE_ZERO_CERTIFICATE.csv"
CSV_4557_CARRIER = SOURCE_DIR / "P8_Y5_R2FR_4557_STRESS_CONSERVATION_CARRIER_CLASSIFICATION.csv"
CSV_4558_ORB_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4558_ORBITAL_COMBO_PRIVATE_ZERO_CERTIFICATE.csv"
CSV_4558_ORB_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4558_ORBITAL_COMBO_FINITE_AMPLITUDE_ROWS.csv"
CSV_4559_R10_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_PRIVATE_ZERO_CERTIFICATE.csv"
CSV_4559_R10_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_YUKAWA_CHANNEL_SPLIT.csv"
CSV_4283_SCOPE = SOURCE_DIR / "P8_Y5_R2FR_4283_NOFLUX_SELECTOR_SCOPE.csv"
CSV_4283_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4283_SHELL_PROFILE_RUNNER_INPUTS.csv"
CSV_4283_RESULTS = SOURCE_DIR / "P8_Y5_R2FR_4283_SHELL_PROFILE_RUNNER_RESULTS.csv"
CSV_4283_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4283_STATUS.csv"
CSV_4283_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4283_CLAIM_FIREWALL.csv"
CSV_4560_GAP = SOURCE_DIR / "P8_Y5_R2FR_4560_PARENT_SIGNATURE_GAP_MAP.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4572_SOURCE_REGISTER.csv"
RESIDUE_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_HIGHER_ORDER_RESIDUE_THEOREM.csv"
ARENA_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_PRIVATE_ARENA_RESIDUE_VERDICT.csv"
TRANSITION_PROFILE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_TRANSITION_SHELL_PROFILE_ROWS.csv"
STATIC_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_STATIC_REDUCTION_AFTER_HIGHER_ORDER.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4572_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4572_VALIDATION.csv"


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
        ("SRC4572_00_4571_doc", "4571 formal boundary reduction", DOC_4571, "O(epsilon_U^3)"),
        ("SRC4572_01_4571_static", "4571 static reduction CSV", CSV_4571_STATIC, "SB4571_2_next_residue"),
        ("SRC4572_02_4571_next", "4571 selected next target", CSV_4571_NEXT, "higher-order-static-residue"),
        ("SRC4572_03_4571_profile", "4571 arena profile rows", CSV_4571_PROFILE, "BP4571_alpha3"),
        ("SRC4572_04_4554_alpha3_final", "4554 alpha3 final private zero", CSV_4554_FINAL, "AF4554_0_private_branch_alpha3"),
        ("SRC4572_05_4554_cubic", "4554 cubic representation theorem", CSV_4554_CUBIC, "CT4554_0_cubic_stability"),
        ("SRC4572_06_4554_counter", "4554 cubic countermodel guards", CSV_4554_COUNTER, "CGU4554_2_radiative_flux"),
        ("SRC4572_07_4556_xi_zero", "4556 xi private zero", CSV_4556_XI_ZERO, "XZ4556_0_private_selector_xi"),
        ("SRC4572_08_4556_xi_split", "4556 xi channel split", CSV_4556_XI_SPLIT, "XS4556_0_start"),
        ("SRC4572_09_4557_zeta_zero", "4557 zeta3 private zero", CSV_4557_ZETA_ZERO, "ZZ4557_0_private_selector_zeta3"),
        ("SRC4572_10_4557_carrier", "4557 stress carrier classification", CSV_4557_CARRIER, "ZC4557_2_Poynting_owned"),
        ("SRC4572_11_4558_orb_zero", "4558 orbital private zero", CSV_4558_ORB_ZERO, "OZ4558_0_private_selector_orbital_combo"),
        ("SRC4572_12_4558_orb_finite", "4558 orbital finite rows", CSV_4558_ORB_FINITE, "OF4558_5_boundary_plus_higher_half_budget"),
        ("SRC4572_13_4559_r10_zero", "4559 R10 private zero", CSV_4559_R10_ZERO, "RZ4559_0_private_selector_R10"),
        ("SRC4572_14_4559_r10_split", "4559 R10 channel split", CSV_4559_R10_SPLIT, "RS4559_3_memory"),
        ("SRC4572_15_4283_scope", "4283 no-flux selector scope", CSV_4283_SCOPE, "NF4283_1_shell_scope_fail"),
        ("SRC4572_16_4283_inputs", "4283 shell profile inputs", CSV_4283_INPUTS, "IN4283_0"),
        ("SRC4572_17_4283_results", "4283 shell profile runner results", CSV_4283_RESULTS, "RUN4283_live"),
        ("SRC4572_18_4283_status", "4283 shell profile status", CSV_4283_STATUS, "STATUS4283_0"),
        ("SRC4572_19_4283_firewall", "4283 shell firewalls", CSV_4283_FIREWALL, "FW4283_0"),
        ("SRC4572_20_4560_gap", "4560 parent signature gaps", CSV_4560_GAP, "PS4560_4_boundary_sector_no_flux"),
        ("SRC4572_21_eq_register", "equation register transition gate", EQ_REGISTER, "C3 = unknown"),
        ("SRC4572_22_red_team", "red-team transition warning", RED_TEAM, "transition shell still blocks derived local GR"),
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
                "role": "4572 higher-order residue and transition-shell profile derivation chain",
                "valid_for_claim": "False",
            }
        )
    return rows


def residue_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "HR4572_0_static_import",
            "statement": "After 4569-4571, the fixed compact non-radiative private branch has ||P_loc J_res_static|| <= O(epsilon_U^3).",
            "derivation": "A_src^std=0, A_lap^std=0 and B_boundary,a^std=0 on the same collar.",
            "status": "PRIVATE_STATIC_REMAINDER_IMPORTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "HR4572_1_alpha3_cubic_zero",
            "statement": "R_higher_alpha3=0 in the private scalar-singlet/no-flux alphabet.",
            "derivation": "4554 proves C3_alpha3=0: scalar products remain scalar and cannot create an l=1 preferred-frame carrier without an admitted vector/pseudovector.",
            "status": "PRIVATE_HIGHER_ORDER_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "HR4572_2_xi_tracefree_zero",
            "statement": "R_higher_xi=0 in the compact centred stationary isotropic private selector.",
            "derivation": "4556 classifies xi as a trace-free preferred-location channel; centred scalar trace, homogeneous scalar boundary and support separation do not supply trace-free carriers.",
            "status": "PRIVATE_HIGHER_ORDER_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "HR4572_3_zeta3_stress_zero",
            "statement": "R_higher_zeta3=0 in the same-metric Hilbert/Maxwell-Hodge private selector.",
            "derivation": "4557 makes total Hilbert stress conserved; Maxwell-Hodge owns Poynting stress and Lorentz exchange is internal, so no independent zeta3 stress carrier remains.",
            "status": "PRIVATE_HIGHER_ORDER_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "HR4572_4_orbital_combo_zero",
            "statement": "R_higher_orbital=0 for the private same-metric EH/Hilbert orbital readout branch.",
            "derivation": "4558 uses gamma=1, beta=1 and Hamiltonian mass charge fixed before orbital readout; no independent orbital force term is admitted.",
            "status": "PRIVATE_HIGHER_ORDER_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "HR4572_5_R10_no_pole_zero",
            "statement": "R_higher_R10=0 at the private R10 anchor/comparator branch.",
            "derivation": "4559's same-metric EH/Newton/no-extra-mode selector has no finite-mass Yukawa pole and excludes edge/memory boundary hair inside the private comparator.",
            "status": "PRIVATE_HIGHER_ORDER_ZERO_ANCHOR_ONLY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "HR4572_6_transition_not_covered",
            "statement": "Transition-shell q_tr/Sigma_metric leakage is not killed by the private residue-zero theorem.",
            "derivation": "4283 and the red-team register say support-separated no-flux does not apply when W_loc intersects transition support; U_B^2 suppression can fail because U_B=O(1) in the shell.",
            "status": "TRANSITION_PROFILE_ROWS_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_verdict_rows(now: str) -> list[dict[str, Any]]:
    arenas = [
        ("alpha3", "PPN_conservation", "R_higher_alpha3", "PRIVATE_ZERO", "4554 cubic representation stability"),
        ("xi", "PPN", "R_higher_xi", "PRIVATE_ZERO", "4556 trace-free metric carrier classification"),
        ("zeta3", "PPN_conservation", "R_higher_zeta3", "PRIVATE_ZERO", "4557 same-metric total Hilbert stress conservation"),
        ("((2+2gamma-beta)/3)-1", "orbital", "R_higher_orbital", "PRIVATE_ZERO", "4558 same-metric EH/Hilbert orbital readout"),
        ("alpha_Yukawa_at_lambda_38p6um", "short_range_gravity", "R_higher_R10", "PRIVATE_ZERO_ANCHOR_ONLY", "4559 no-extra-finite-range private comparator"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": f"AV4572_{idx}_{observable}",
            "observable": observable,
            "arena": arena,
            "higher_residue": residue,
            "private_selector_status": status,
            "basis": basis,
            "scope_guard": "private compact stationary non-radiative same-branch selector only; scope changes reopen finite rows",
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for idx, (observable, arena, residue, status, basis) in enumerate(arenas)
    ]


def transition_profile_rows(now: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for input_row in read_csv(CSV_4283_INPUTS):
        quantity = input_row.get("quantity", "")
        threshold = input_row.get("threshold_or_requirement", "")
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "generated_utc": now,
                "transition_id": f"TS4572_{input_row.get('input_id', '')}",
                "quantity": quantity,
                "profile_value": input_row.get("value", ""),
                "threshold_or_requirement": threshold,
                "units": input_row.get("units", ""),
                "status": "RETAINED_PROFILE_REQUIRED",
                "reason": "transition shell is outside fixed compact support-separated no-flux branch",
                "next_input": "source real profile or derive source-lift/metric-null theorem",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "transition_id": "TS4572_metric_source_lift",
            "quantity": "Sigma_metric[q_tr]",
            "profile_value": "MISSING_SOURCE_LIFT",
            "threshold_or_requirement": "Sigma_metric[q_tr]=0 or PPN-small by theorem/source profile",
            "units": "metric response",
            "status": "NEXT_THEOREM_TARGET",
            "reason": "red-team and equation register both mark Sigma_metric[q_tr] as not derived",
            "next_input": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return rows


def static_reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "HO4572_0_private_arena_zero",
            "before": "private branch residual after 4571: listed arena projections are O(epsilon_U^3)",
            "after": "listed arena projections vanish in private scorecard: Delta_a^private=0",
            "condition": "same compact stationary non-radiative private selector and no transition-shell/source-lift leakage",
            "status": "PRIVATE_ARENA_SCORECARD_ZERO",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "HO4572_1_transition_open",
            "before": "transition shell sometimes hidden behind local no-flux/bulk suppression language",
            "after": "transition shell is an explicit profile/source-lift row: q_tr_shell_norm, Sigma_metric[q_tr], boundary response, K_perp",
            "condition": "Solar/vacuum transition or any collar intersecting transition support",
            "status": "TRANSITION_BRANCH_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "HO4572_2_public_status",
            "before": "bulk, boundary and higher-order private branches looked locally complete",
            "after": "public local-GR/Newton/PPN/R10 claim remains blocked by transition-shell source lift, global parent signatures and empirical full rows",
            "condition": "public theory claim",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4572_0_same_branch",
            "requirement": "higher-order zeros must share the 4569-4571 compact stationary non-radiative private branch",
            "current_status": "PASS_PRIVATE_SCORECARD_ONLY",
            "failure_mode": "using private cubic/metric zeros for radiative, rotating, off-centre, anisotropic or transition systems",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4572_1_transition_shell",
            "requirement": "derive Sigma_metric[q_tr]=0 or source q_tr/Sigma_metric profiles below thresholds",
            "current_status": "OPEN_NEXT_TARGET",
            "failure_mode": "pretending U_B^2/fixed-collar no-flux solves the Solar transition shell",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4572_2_R10_curve",
            "requirement": "R10 public row needs full alpha(lambda) curve/table, not anchor-only private comparator",
            "current_status": "OPEN_EMPIRICAL_GATE",
            "failure_mode": "calling lambda=38.6um anchor pass a public short-range-gravity claim",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4572_3_parent_signatures",
            "requirement": "global EH/IR, same-source coupling, no-flux, quotient no-pole and memory support signatures must close",
            "current_status": "PUBLIC_CLAIM_BLOCKED",
            "failure_mode": "promoting private scorecard completion to fundamental field theory completion",
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
            "decision_id": "DEC4572_0_private_residue_zero",
            "reason": "Existing 4554-4559 private certificates classify the listed O(epsilon_U^3) arena residues as zero in the same compact non-radiative selector.",
            "next_action": "record private arena scorecard zero without promoting it to public local-GR",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4572_1_transition_retained",
            "reason": "Transition shell sits outside the fixed support-separated branch; q_tr_shell_norm and Sigma_metric[q_tr] remain missing real profiles/theorems.",
            "next_action": "derive source-lift/metric-null theorem or build source-backed transition profile runner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4572_2_next",
            "reason": "The most honest next leap is the transition-shell source-lift: does q_tr become metric stress, projection-silent current, or a bounded profile?",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4572_0",
            "next_target": NEXT_TARGET,
            "objective": "derive whether transition current q_tr has zero metric source lift Sigma_metric[q_tr], or build the first real transition-shell profile runner",
            "derive_first": "prove q_tr is boundary/topological/projector-silent before metric variation for local collars, or that P_metric,loc q_tr=0",
            "fallback": "source q_tr_shell_norm, Sigma_metric_shell_response, boundary_response and K_perp profile rows against 4283 thresholds",
            "avoid": "using private compact no-flux or U_B^2 far-local suppression for collars that intersect transition support",
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
            "status_id": "STAT4572_0_private_scorecard",
            "item": "private listed local arenas",
            "status": "PRIVATE_ARENA_SCORECARD_ZERO",
            "note": "Within the same compact stationary non-radiative selector, listed PPN/orbital/R10 pressure channels are zero through higher order.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4572_1_transition_shell",
            "item": "q_tr / Sigma_metric[q_tr]",
            "status": "ACTIVE_BLOCKER_PROFILE_OR_THEOREM_REQUIRED",
            "note": "Solar/vacuum transition shell remains outside the private no-flux branch and needs source-lift derivation or real profiles.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4572_2_public_claim",
            "item": "local_GR_public_claim",
            "status": "BLOCKED",
            "note": "Transition shell, global parent signatures, R10 full curve and empirical robustness rows remain required.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    arena_verdict: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        RESIDUE_THEOREM_CSV,
        ARENA_VERDICT_CSV,
        TRANSITION_PROFILE_CSV,
        STATIC_REDUCTION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        FORMAL_PATH,
        DOC_PATH,
    ]
    csv_paths = [
        SOURCE_REGISTER,
        RESIDUE_THEOREM_CSV,
        ARENA_VERDICT_CSV,
        TRANSITION_PROFILE_CSV,
        STATIC_REDUCTION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    text_blob = "\n".join(str(row) for row in theorem + arena_verdict + transition_rows + static_reduction + promotion + decisions + next_target + status)
    source_paths_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    theorem_tokens_ok = all(
        token in text_blob
        for token in [
            "R_higher_alpha3=0",
            "R_higher_xi=0",
            "R_higher_zeta3=0",
            "R_higher_R10=0",
            "Sigma_metric[q_tr]",
            "TRANSITION_PROFILE_ROWS_RETAINED",
        ]
    )
    transition_rows_ok = len(transition_rows) >= 6 and any(row.get("quantity") == "Sigma_metric[q_tr]" for row in transition_rows)
    branch_tokens_ok = all(
        token in text_blob
        for token in [
            "PRIVATE_ARENA_SCORECARD_ZERO",
            "ACTIVE_BLOCKER_PROFILE_OR_THEOREM_REQUIRED",
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
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:ERROR:{exc}")
    all_new_rows = sources + theorem + arena_verdict + transition_rows + static_reduction + promotion + decisions + next_target + status
    nonclaim_ok = all(str(row.get("valid_for_claim", "False")) == "False" for row in all_new_rows)
    next_ok = bool(next_target) and next_target[0].get("next_target") == NEXT_TARGET
    pycache_absent = not (POST / "scripts" / "__pycache__").exists()
    rows = [
        {
            "check_id": "VAL4572_0_source_paths",
            "status": "PASS" if source_paths_ok else "FAIL",
            "detail": "all cited source paths exist and needles were found",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_1_generated_paths",
            "status": "PASS" if generated_paths_ok else "FAIL",
            "detail": "; ".join(str(path) for path in generated_paths),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_2_csv_parse",
            "status": "PASS" if csv_parse_ok else "FAIL",
            "detail": "; ".join(csv_parse_detail),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_3_theorem_tokens",
            "status": "PASS" if theorem_tokens_ok else "FAIL",
            "detail": "required private residue-zero and transition-retained tokens present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_4_transition_rows",
            "status": "PASS" if transition_rows_ok else "FAIL",
            "detail": f"{len(transition_rows)} transition rows including Sigma_metric[q_tr]",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_5_branch_verdict",
            "status": "PASS" if branch_tokens_ok else "FAIL",
            "detail": "private scorecard zero, transition blocker and public blocked statuses present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_6_nonclaim_firewall",
            "status": "PASS" if nonclaim_ok else "FAIL",
            "detail": "all generated rows keep valid_for_claim=false",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_7_next_target",
            "status": "PASS" if next_ok else "FAIL",
            "detail": NEXT_TARGET,
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4572_8_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": str(POST / "scripts" / "__pycache__"),
            "valid_for_claim": "False",
        },
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL4572_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": "False",
        }
    )
    return rows


def formal_markdown(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    arena_verdict: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 588 - PPC4161 Higher-Order Static Residue Or Transition-Shell Profile Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4571 reduced the same private compact stationary non-radiative branch to:

```text
||P_loc J_res_static|| <= O(epsilon_U^3).
```

4572 classifies that higher-order residue for the listed local arenas. In the same private selector:

```text
R_higher_alpha3 = 0,
R_higher_xi = 0,
R_higher_zeta3 = 0,
R_higher_orbital = 0,
R_higher_R10 = 0  (private anchor/no-pole comparator only).
```

So the private local pressure scorecard is zero for the listed arena projections. That is progress, but it is not public local GR. The Solar/vacuum transition shell is outside the support-separated no-flux branch:

```text
q_tr_shell_norm = MISSING_REAL_PROFILE,
Sigma_metric[q_tr] = MISSING_SOURCE_LIFT,
P_metric,loc q_tr = not yet theorem-zero.
```

## Transition-Shell Firewall

The checkpoint keeps the anti-cheat row explicit: `U_B^2` far-local suppression and fixed-collar no-flux do not solve collars intersecting transition support. The next route must either derive `Sigma_metric[q_tr]=0` before metric variation, or source real profile rows below the 4283 thresholds.

## Source Register

{markdown_table(sources)}

## Higher-Order Residue Theorem

{markdown_table(theorem)}

## Private Arena Residue Verdict

{markdown_table(arena_verdict)}

## Transition-Shell Profile Rows

{markdown_table(transition_rows)}

## Static Reduction After Higher Order

{markdown_table(static_reduction)}

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
    arena_verdict: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4572 - Higher-Order Static Residue Or Transition-Shell Profile Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## What Changed

The private local branch now has:

```text
A_src^std=0,
A_lap^std=0,
B_boundary,a^std=0,
R_higher,a^std=0
```

for the listed compact stationary non-radiative arena projections. But the transition shell is not closed:

```text
Sigma_metric[q_tr] = MISSING_SOURCE_LIFT,
q_tr_shell_norm = MISSING_REAL_PROFILE.
```

## Higher-Order Theorem

{markdown_table(theorem)}

## Arena Verdict

{markdown_table(arena_verdict)}

## Transition Rows

{markdown_table(transition_rows)}

## Static Reduction

{markdown_table(static_reduction)}

## Decisions

{markdown_table(decisions)}

## Validation

{markdown_table(validation)}

## Files Written

- `{FORMAL_PATH}`
- `{SOURCE_REGISTER}`
- `{RESIDUE_THEOREM_CSV}`
- `{ARENA_VERDICT_CSV}`
- `{TRANSITION_PROFILE_CSV}`
- `{STATIC_REDUCTION_CSV}`
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
        "claim": "4572 classifies the private compact selector's listed higher-order static residues as zero while retaining transition-shell q_tr/Sigma_metric profile rows as the active nonclaim blocker.",
        "current_evidence": "Generated source register, higher-order residue theorem, private arena verdict, transition-shell profile rows, static reduction rows, promotion gates, status and validation CSVs.",
        "status": "private_higher_order_residue_zero_transition_shell_profile_rows_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating private arena scorecard zero as public local-GR proof while transition-shell source lift, global parent signatures and full empirical rows remain open.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Transition shell and Sigma_metric[q_tr] remain the main local-GR obstruction.",
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
    theorem = residue_theorem_rows(now)
    arena_verdict = arena_verdict_rows(now)
    transition_rows = transition_profile_rows(now)
    static_reduction = static_reduction_rows(now)
    promotion = promotion_rows(now)
    decisions = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(RESIDUE_THEOREM_CSV, theorem)
    write_csv(ARENA_VERDICT_CSV, arena_verdict)
    write_csv(TRANSITION_PROFILE_CSV, transition_rows)
    write_csv(STATIC_REDUCTION_CSV, static_reduction)
    write_csv(PROMOTION_CSV, promotion)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    validation = validation_rows(
        sources,
        theorem,
        arena_verdict,
        transition_rows,
        static_reduction,
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
            arena_verdict,
            transition_rows,
            static_reduction,
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
        post_markdown(theorem, arena_verdict, transition_rows, static_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(
        sources,
        theorem,
        arena_verdict,
        transition_rows,
        static_reduction,
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
            arena_verdict,
            transition_rows,
            static_reduction,
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
        post_markdown(theorem, arena_verdict, transition_rows, static_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4572 Higher-Order Static Residue / Transition-Shell Verdict

Marker: `{MARKER}`

The private compact stationary non-radiative local scorecard now has listed arena residue zero through the higher-order static row:

```text
A_src^std=A_lap^std=B_boundary,a^std=R_higher,a^std=0
```

for alpha3, xi, zeta3, orbital combo and the private R10 anchor/no-pole comparator. This is not a public local-GR claim because the transition shell remains outside the fixed support-separated collar:

```text
Sigma_metric[q_tr] = MISSING_SOURCE_LIFT,
q_tr_shell_norm = MISSING_REAL_PROFILE.
```

Next target: `{NEXT_TARGET}`.
""",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4572 Packet Integration - Higher-Order Residue / Transition Shell

Marker: `{PACKET_MARKER}`

Packet rule: the private compact non-radiative local arena scorecard is zero through higher order for alpha3, xi, zeta3, orbital combo and private R10 anchor/no-pole rows. Do not export this to transition shells. Solar/vacuum transition still requires `Sigma_metric[q_tr]=0` or real `q_tr_shell_norm/Sigma_metric_shell_response` profile rows. Next target: `{NEXT_TARGET}`.
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
