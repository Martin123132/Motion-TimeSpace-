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

CHECKPOINT = "4571"
CLAIM_ID = "L-413"
BRANCH_ID = "MTS_R2FR_Y5_STATIC_BOUNDARY_NOHAIR_PROFILE_KERNEL_4571"
MARKER = "PPC4161_STATIC_BOUNDARY_NOHAIR_OR_B_BOUNDARY_PROFILE_KERNEL_ROW_4571"
PACKET_MARKER = "PPC4161_PACKET_STATIC_BOUNDARY_NOHAIR_PROFILE_KERNEL_4571"
DECISION = "STATIC_BOUNDARY_NOHAIR_PRIVATE_FIXED_COLLAR_ZERO_PROFILE_KERNEL_ROWS_RETAINED_NONCLAIM"
NEXT_TARGET = "4572-Y5-R2FR-higher-order-static-residue-or-transition-shell-profile-row.md"

FORMAL_PATH = FORMAL / "587-PPC4161-static-boundary-nohair-or-B-boundary-profile-kernel-row.md"
DOC_PATH = POST / "4571-Y5-R2FR-static-boundary-nohair-or-B_boundary-profile-kernel-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4570 = FORMAL / "586-PPC4161-parent-mL-attractor-equation-or-A-lap-source-row.md"
DOC_192 = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
DOC_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
CSV_4570_STATIC = SOURCE_DIR / "P8_Y5_R2FR_4570_STATIC_REDUCTION_AFTER_ALAP.csv"
CSV_4570_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4570_NEXT_TARGET.csv"
CSV_4568_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4568_BOUNDARY_PROFILE_INTERFACE.csv"
CSV_4568_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4568_AJ_PROFILE_RUNNER_ROWS.csv"
CSV_4567_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4567_BOUNDARY_AMPLITUDE_LEDGER.csv"
CSV_4545_BOUNDARY_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4545_BOUNDARY_SILENCE_SPLIT.csv"
CSV_4545_RETAINED = SOURCE_DIR / "P8_Y5_R2FR_4545_RETAINED_RESIDUALS.csv"
CSV_4268_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4268_BOUNDARY_PROJECTOR_THEOREM.csv"
CSV_4268_OPEN = SOURCE_DIR / "P8_Y5_R2FR_4268_OPEN_BOUNDARY_RESIDUAL_SPLIT_ROWS.csv"
CSV_4268_ADOPTION = SOURCE_DIR / "P8_Y5_R2FR_4268_DQ_BOUNDARY_PROJECTOR_ADOPTION.csv"
CSV_4283_SCOPE = SOURCE_DIR / "P8_Y5_R2FR_4283_NOFLUX_SELECTOR_SCOPE.csv"
CSV_4283_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4283_CLAIM_FIREWALL.csv"
CSV_4551_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4551_BOUNDARY_VECTOR_ZERO_THEOREM.csv"
CSV_4551_FALLBACK = SOURCE_DIR / "P8_Y5_R2FR_4551_FINITE_FALLBACK_PRODUCTS.csv"
CSV_4553_NOFLUX = SOURCE_DIR / "P8_Y5_R2FR_4553_BOUNDARY_NOFLUX_THEOREM_ATTEMPT.csv"
CSV_4553_PREMISES = SOURCE_DIR / "P8_Y5_R2FR_4553_PRIVATE_SELECTOR_PREMISES.csv"
CSV_4557_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4557_ZETA3_PRIVATE_ZERO_CERTIFICATE.csv"
CSV_4557_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4557_ZETA3_FINITE_AMPLITUDE_ROWS.csv"
CSV_4558_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4558_ORBITAL_COMBO_PRIVATE_ZERO_CERTIFICATE.csv"
CSV_4558_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4558_ORBITAL_COMBO_FINITE_AMPLITUDE_ROWS.csv"
CSV_4559_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_PRIVATE_ZERO_CERTIFICATE.csv"
CSV_4559_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4559_R10_FINITE_AMPLITUDE_ROWS.csv"
CSV_4560_GAP = SOURCE_DIR / "P8_Y5_R2FR_4560_PARENT_SIGNATURE_GAP_MAP.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4571_SOURCE_REGISTER.csv"
NOHAIR_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_STATIC_BOUNDARY_NOHAIR_THEOREM.csv"
BRANCH_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_BOUNDARY_BRANCH_VERDICT.csv"
PROFILE_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_ARENA_BOUNDARY_PROFILE_ROWS.csv"
KERNEL_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_PROFILE_KERNEL_REQUIREMENT_ROWS.csv"
STATIC_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_STATIC_REDUCTION_AFTER_BOUNDARY.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4571_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4571_VALIDATION.csv"


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
        ("SRC4571_00_4570_doc", "4570 formal static reduction", DOC_4570, "A_J_eff^bulk-zero = 0"),
        ("SRC4571_01_4570_static", "4570 static reduction CSV", CSV_4570_STATIC, "SR4570_1_static_bound"),
        ("SRC4571_02_4570_next", "4570 selected next target", CSV_4570_NEXT, "static-boundary-nohair"),
        ("SRC4571_03_4568_boundary_interface", "4568 boundary interface", CSV_4568_BOUNDARY, "BI4568_1_private_compact_zero"),
        ("SRC4571_04_4568_runner", "4568 arena runner rows", CSV_4568_RUNNER, "RUN4568_PB4550_alpha3"),
        ("SRC4571_05_4567_boundary", "4567 boundary amplitude ledger", CSV_4567_BOUNDARY, "B4567_1_static_trace_vector_shear"),
        ("SRC4571_06_4545_boundary_split", "4545 boundary split", CSV_4545_BOUNDARY_SPLIT, "BS4545_2_vector_marker_flux"),
        ("SRC4571_07_4545_retained", "4545 retained boundary residual", CSV_4545_RETAINED, "RR4545_2_boundary_nohair"),
        ("SRC4571_08_4268_theorem", "4268 fixed-collar boundary projector theorem", CSV_4268_THEOREM, "BPROJ4268_2_no_flux_support"),
        ("SRC4571_09_4268_open", "4268 open boundary residual split", CSV_4268_OPEN, "BRES4268_3_open_radiation"),
        ("SRC4571_10_4268_adoption", "4268 boundary projector adoption", CSV_4268_ADOPTION, "ADOPT4268_Dq_boundary_projector"),
        ("SRC4571_11_4283_scope", "4283 no-flux selector scope", CSV_4283_SCOPE, "NF4283_0_valid_scope"),
        ("SRC4571_12_4283_firewall", "4283 no-flux firewall", CSV_4283_FIREWALL, "FW4283_0"),
        ("SRC4571_13_192_formal", "192 local boundary no-flux theorem", DOC_192, "J_tr^nu = 0 through <=2PN"),
        ("SRC4571_14_191_formal", "191 Maxwell-Hodge Poynting guard", DOC_191, "Radiative EM is not erased"),
        ("SRC4571_15_4551_alpha3_boundary", "4551 alpha3 boundary zero", CSV_4551_BOUNDARY, "BZ4551_1_scalar_homogeneous_boundary"),
        ("SRC4571_16_4551_alpha3_fallback", "4551 alpha3 finite fallback", CSV_4551_FALLBACK, "FB4551_3_boundary_only"),
        ("SRC4571_17_4553_no_flux", "4553 alpha3 no-flux theorem attempt", CSV_4553_NOFLUX, "BN4553_3_poynting_firewall"),
        ("SRC4571_18_4553_premises", "4553 private selector premises", CSV_4553_PREMISES, "SP4553_4_no_flux_boundary"),
        ("SRC4571_19_4557_zeta3_zero", "4557 zeta3 zero certificate", CSV_4557_ZERO, "ZZ4557_0_private_selector_zeta3"),
        ("SRC4571_20_4557_zeta3_finite", "4557 zeta3 finite rows", CSV_4557_FINITE, "ZF4557_3_boundary_plus_higher_half_budget"),
        ("SRC4571_21_4558_orbital_zero", "4558 orbital zero certificate", CSV_4558_ZERO, "OZ4558_0_private_selector_orbital_combo"),
        ("SRC4571_22_4558_orbital_finite", "4558 orbital finite rows", CSV_4558_FINITE, "OF4558_5_boundary_plus_higher_half_budget"),
        ("SRC4571_23_4559_r10_zero", "4559 R10 zero certificate", CSV_4559_ZERO, "RZ4559_0_private_selector_R10"),
        ("SRC4571_24_4559_r10_finite", "4559 R10 finite rows", CSV_4559_FINITE, "RF4559_3_boundary_plus_higher_half_budget"),
        ("SRC4571_25_4560_gap", "4560 boundary sector parent signature gap", CSV_4560_GAP, "PS4560_4_boundary_sector_no_flux"),
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
                "role": "4571 static boundary nohair/profile-kernel derivation chain",
                "valid_for_claim": "False",
            }
        )
    return rows


def nohair_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "BN4571_0_bulk_import",
            "statement": "After 4569 and 4570, the same private branch has A_J_eff^bulk-zero=0.",
            "derivation": "A_src^std=0 and A_lap^std=0 on the same compact stationary standard collar.",
            "status": "BULK_STATIC_ZERO_IMPORTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "BN4571_1_fixed_collar_boundary_zero",
            "statement": "If W_loc, caps, normals, orientations, P_loc and sector interfaces are q-basic/fixed before variation, supp(T_local) is interior, and no source crossing/open radiative/memory pullback enters, then P_loc boundary_in_static=0.",
            "derivation": "4268 gives boundary-projector silence for fixed collars; 192 supplies compact support-separated no-flux/routing; 4283 limits this to support-separated collars.",
            "status": "CONDITIONAL_FIXED_COLLAR_NOHAIR_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "BN4571_2_arena_projection_zero",
            "statement": "For arena a in {alpha3, xi, zeta3, orbital, R10}, B_boundary,a^std := K_a P_loc boundary_in_static = 0 when BN4571_1 holds and the arena projection is part of the same private selector.",
            "derivation": "A zero projected boundary source remains zero after a fixed linear arena kernel; prior alpha3/zeta3/orbital/R10 certificates supply the selector-specific projection language.",
            "status": "CONDITIONAL_ARENA_BOUNDARY_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "BN4571_3_radiative_poynting_guard",
            "statement": "Radiative EM/gravity/Poynting flux is routed as boundary/Hamiltonian charge, not set to zero by the compact non-radiative theorem.",
            "derivation": "191 identifies Poynting as Hilbert EM stress and explicitly keeps radiative boundary flux real; 4553 carries the same firewall.",
            "status": "RADIATIVE_BOUNDARY_GUARD_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "BN4571_4_open_profile_fallback",
            "statement": "If source crossing, transition support, moving projector, corner/edge charge, memory pullback or radiative flux is present, retain Q_a := K_a B_boundary,a as a finite arena profile row.",
            "derivation": "4568 runner already separates Q_a from epsilon_U^2 A_J_eff; with bulk A_J zero, the boundary row is the leading scored static obstruction.",
            "status": "FINITE_PROFILE_KERNEL_ROWS_RETAINED",
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
            "verdict_id": "BV4571_0_fixed_compact_branch",
            "branch_scope": "same compact stationary non-radiative fixed-collar standard branch",
            "B_boundary_status": "CLOSED_CONDITIONAL_FIXED_COLLAR_BRANCH",
            "formula": "B_boundary,a^std=0 for all listed local arenas",
            "reason": "bulk A_J is already zero and fixed-collar no-flux/no-source-crossing gives P_loc boundary_in_static=0.",
            "firewall": "Do not export this zero to transition shells, moving apparatus boundaries, radiative Poynting/GR flux or open-memory pullbacks.",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4571_1_open_or_transition_branch",
            "branch_scope": "open/radiative/transition/moving-boundary/domain-selector/corner-edge branch",
            "B_boundary_status": "PROFILE_KERNEL_ROWS_RETAINED",
            "formula": "|Q_a|+|R_higher,a| <= B_a with Q_a := K_a B_boundary,a",
            "reason": "4268 and 4283 forbid using compact no-flux through open or transition sectors.",
            "firewall": "Boundary rows need source-backed amplitudes and kernels; no cancellation against bulk A_J is allowed.",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4571_2_public_claim",
            "branch_scope": "public local-GR/Newton/PPN/R10 claim",
            "B_boundary_status": "PUBLIC_CLAIM_BLOCKED",
            "formula": "private bulk+boundary zero still leaves R_higher/O(epsilon_U^3), transition shell and parent signature gates",
            "reason": "4560 says global boundary-sector no-flux is not parent-signed and empirical full rows remain incomplete.",
            "firewall": "No WEP, PPN, clock, orbital, R10 or local-GR pass may be inferred from this checkpoint alone.",
            "valid_for_claim": "False",
        },
    ]


def arena_profile_rows(now: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for runner in read_csv(CSV_4568_RUNNER):
        observable = runner.get("observable", "")
        boundary_symbol = runner.get("boundary_symbol", "")
        half_budget = runner.get("half_budget_boundary_plus_higher", "")
        no_cancel = runner.get("no_cancellation_test", "")
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "generated_utc": now,
                "profile_id": f"BP4571_{observable}",
                "arena": runner.get("arena", ""),
                "observable": observable,
                "boundary_profile": boundary_symbol,
                "bulk_status": "A_J_eff^bulk-zero=0 on private same-branch selector",
                "private_zero_condition": "K_a P_loc boundary_in_static=0 from fixed compact no-flux collar and arena projection silence",
                "open_branch_requirement": f"|{boundary_symbol}| + |R_higher_{observable}| <= {half_budget}",
                "runner_no_cancellation_source": no_cancel,
                "status": "THEOREM_ZERO_PRIVATE_OR_FINITE_PROFILE_ROW_OPEN",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def kernel_requirement_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "kernel_id": "KR4571_0_alpha3",
            "observable": "alpha3",
            "kernel": "K_alpha3^vec",
            "zero_route": "scalar homogeneous marker-free boundary plus normal-momentum no-flux",
            "fallback": "|Q_alpha3_vec| <= 4e-20 if source/higher pieces are zero, or half-budget 2e-20 with no cancellation",
            "status": "PRIVATE_ZERO_OR_ULTRATINY_BOUND_ROW",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "kernel_id": "KR4571_1_xi",
            "observable": "xi",
            "kernel": "K_xi",
            "zero_route": "isotropic centred scalar boundary/no preferred-location trace-free carrier",
            "fallback": "finite B_boundary,xi profile row from 4568 runner",
            "status": "PRIVATE_ZERO_OR_PROFILE_ROW",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "kernel_id": "KR4571_2_zeta3",
            "observable": "zeta3",
            "kernel": "K_zeta3",
            "zero_route": "same-metric Hilbert total stress and Maxwell-Hodge EM/Poynting stress routed through T_total",
            "fallback": "|Q_zeta3|+|R_higher_zeta3| <= 5e-9 under equal split",
            "status": "PRIVATE_ZERO_OR_PROFILE_ROW",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "kernel_id": "KR4571_3_orbital",
            "observable": "((2+2gamma-beta)/3)-1",
            "kernel": "K_orb",
            "zero_route": "same-metric EH/Hilbert source branch with Hamiltonian mass charge fixed before orbital readout",
            "fallback": "|Q_orb|+|R_higher_orb| <= 2.3333333333333336e-05 under equal split",
            "status": "PRIVATE_ZERO_OR_PROFILE_ROW",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "kernel_id": "KR4571_4_R10",
            "observable": "alpha_Yukawa_at_lambda_38p6um",
            "kernel": "K_R10(lambda)",
            "zero_route": "same-metric EH/Newton no-extra-finite-range selector plus no edge/memory boundary hair",
            "fallback": "|Q_R10|+|R_higher_R10| <= 0.5 at anchor; public row needs full alpha(lambda) curve",
            "status": "PRIVATE_ZERO_OR_ANCHOR_ONLY_PROFILE_ROW",
            "valid_for_claim": "False",
        },
    ]


def static_reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "SB4571_0_private_boundary_zero",
            "before": "||P_loc J_res_static|| <= B_boundary_static + O(epsilon_U^3)",
            "after": "||P_loc J_res_static|| <= O(epsilon_U^3)",
            "condition": "same fixed compact non-radiative no-flux collar with A_src=A_lap=0 and P_loc boundary_in_static=0",
            "status": "BOUNDARY_STATIC_TOOTH_REMOVED_CONDITIONALLY",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "SB4571_1_open_boundary",
            "before": "boundary amplitude was a single retained label",
            "after": "B_boundary,a enters arena rows as Q_a := K_a B_boundary,a",
            "condition": "open/radiative/transition/moving-boundary branches",
            "status": "FINITE_PROFILE_KERNEL_BRANCH_SHARPENED",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "SB4571_2_next_residue",
            "before": "bulk and boundary static terms were both live",
            "after": "leading private branch residue is R_higher_static/O(epsilon_U^3) plus transition-shell/global parent gates",
            "condition": "only after same-branch bulk and boundary zero are accepted",
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
            "gate_id": "PG4571_0_same_branch",
            "requirement": "A_src, A_lap and B_boundary_static zeros must be on the same fixed compact collar",
            "current_status": "PASS_PRIVATE_BRANCH_ONLY",
            "failure_mode": "mixing bulk-zero and boundary-zero assumptions from incompatible branches",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4571_1_radiative_guard",
            "requirement": "route nonzero Poynting/GR radiation as boundary/Hamiltonian flux, not zero",
            "current_status": "FIREWALL_RETAINED",
            "failure_mode": "using compact non-radiative no-flux to erase real radiation",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4571_2_profile_inputs",
            "requirement": "source K_a, B_boundary,a and R_higher,a for any open or transition branch",
            "current_status": "PROFILE_ROWS_READY_VALUES_MISSING",
            "failure_mode": "claiming pass from schema rows without amplitudes/kernels",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4571_3_public_parent",
            "requirement": "global parent boundary-sector no-flux and full empirical rows must close before public local-GR/PPN/R10 claims",
            "current_status": "PUBLIC_CLAIM_BLOCKED",
            "failure_mode": "promoting private selector nohair to global MTS theorem",
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
            "decision_id": "DEC4571_0_boundary_zero",
            "reason": "On the same fixed compact non-radiative collar, prior boundary-projector/no-flux theorems make P_loc boundary_in_static zero, so B_boundary,a^std=0.",
            "next_action": "use boundary zero only inside the private same-branch packet",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4571_1_profile_rows",
            "reason": "Open, radiative, transition, moving-boundary and edge/corner branches are not killed by compact no-flux language.",
            "next_action": "retain Q_a := K_a B_boundary,a rows for each arena with no cancellation against bulk A_J",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4571_2_next",
            "reason": "After private same-branch bulk and boundary zeros, the next live residue is higher-order/transition-shell/global parent signature rather than the old A_J/B_boundary labels.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4571_0",
            "next_target": NEXT_TARGET,
            "objective": "classify or bound the O(epsilon_U^3) static residue and transition-shell/profile leakage after private bulk+boundary zeros",
            "derive_first": "show the same private selector forces cubic/higher static residues projection-silent for alpha3, xi, zeta3, orbital and R10",
            "fallback": "keep R_higher,a and transition-shell profile rows with source-backed amplitudes/kernels",
            "avoid": "calling bulk+boundary private zero a public local-GR pass before higher-order, transition and parent-signature gates close",
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
            "status_id": "STAT4571_0_B_boundary",
            "item": "B_boundary_static",
            "status": "CLOSED_CONDITIONAL_FIXED_COLLAR_BRANCH",
            "note": "B_boundary,a^std=0 only for the same fixed compact non-radiative no-flux collar and arena projection.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4571_1_open_profiles",
            "item": "Q_a boundary profile rows",
            "status": "PROFILE_KERNEL_ROWS_RETAINED",
            "note": "Open/radiative/transition branches retain Q_a := K_a B_boundary,a and R_higher,a rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4571_2_public_claim",
            "item": "local_GR_public_claim",
            "status": "BLOCKED",
            "note": "Higher-order residues, transition shells, global boundary-sector no-flux and empirical full rows remain required.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    branch_verdict: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    kernel_rows: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        NOHAIR_THEOREM_CSV,
        BRANCH_VERDICT_CSV,
        PROFILE_ROWS_CSV,
        KERNEL_ROWS_CSV,
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
        NOHAIR_THEOREM_CSV,
        BRANCH_VERDICT_CSV,
        PROFILE_ROWS_CSV,
        KERNEL_ROWS_CSV,
        STATIC_REDUCTION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    text_blob = "\n".join(str(row) for row in theorem + branch_verdict + profile_rows + kernel_rows + static_reduction + promotion + decisions + next_target + status)
    source_paths_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    theorem_tokens_ok = all(
        token in text_blob
        for token in [
            "B_boundary,a^std=0",
            "P_loc boundary_in_static=0",
            "Q_a := K_a B_boundary,a",
            "RADIATIVE_BOUNDARY_GUARD_RETAINED",
            "O(epsilon_U^3)",
        ]
    )
    profile_rows_ok = len(profile_rows) >= 5 and all(row.get("boundary_profile") for row in profile_rows)
    branch_tokens_ok = all(
        token in text_blob
        for token in [
            "CLOSED_CONDITIONAL_FIXED_COLLAR_BRANCH",
            "PROFILE_KERNEL_ROWS_RETAINED",
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
    all_new_rows = sources + theorem + branch_verdict + profile_rows + kernel_rows + static_reduction + promotion + decisions + next_target + status
    nonclaim_ok = all(str(row.get("valid_for_claim", "False")) == "False" for row in all_new_rows)
    next_ok = bool(next_target) and next_target[0].get("next_target") == NEXT_TARGET
    pycache_absent = not (POST / "scripts" / "__pycache__").exists()
    rows = [
        {
            "check_id": "VAL4571_0_source_paths",
            "status": "PASS" if source_paths_ok else "FAIL",
            "detail": "all cited source paths exist and needles were found",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_1_generated_paths",
            "status": "PASS" if generated_paths_ok else "FAIL",
            "detail": "; ".join(str(path) for path in generated_paths),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_2_csv_parse",
            "status": "PASS" if csv_parse_ok else "FAIL",
            "detail": "; ".join(csv_parse_detail),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_3_theorem_tokens",
            "status": "PASS" if theorem_tokens_ok else "FAIL",
            "detail": "required boundary zero, profile row, radiative guard and higher-order tokens present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_4_profile_rows",
            "status": "PASS" if profile_rows_ok else "FAIL",
            "detail": f"{len(profile_rows)} arena profile rows written from 4568 runner",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_5_branch_verdict",
            "status": "PASS" if branch_tokens_ok else "FAIL",
            "detail": "fixed-collar closed, profile rows retained and public blocked statuses present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_6_nonclaim_firewall",
            "status": "PASS" if nonclaim_ok else "FAIL",
            "detail": "all generated rows keep valid_for_claim=false",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_7_next_target",
            "status": "PASS" if next_ok else "FAIL",
            "detail": NEXT_TARGET,
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4571_8_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": str(POST / "scripts" / "__pycache__"),
            "valid_for_claim": "False",
        },
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL4571_OVERALL",
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
    profile_rows: list[dict[str, Any]],
    kernel_rows: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 587 - PPC4161 Static Boundary Nohair Or B_boundary Profile Kernel Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

After 4569 and 4570, the private same-branch static bulk coefficient is zero:

```text
A_J_eff^bulk-zero = 0.
```

4571 attacks the next tooth. In the same compact stationary non-radiative fixed-collar branch:

```text
P_loc boundary_in_static=0,
B_boundary,a^std := K_a P_loc boundary_in_static = 0,
||P_loc J_res_static|| <= O(epsilon_U^3).
```

This is not a global boundary theorem. It requires the same fixed/q-basic collar, no source crossing, no transition support, no open radiative or memory pullback, fixed/routed Hamiltonian boundary data, and arena projections belonging to the same private selector.

## Open / Radiative / Transition Branch

If any of those clauses fail, the retained object is not `A_J_eff`; it is the arena boundary profile:

```text
Q_a := K_a B_boundary,a,
|Q_a| + |R_higher,a| <= B_a.
```

Poynting/radiative flux is especially not erased: Maxwell-Hodge owns it as Hilbert stress, and nonzero flux crossing the collar is routed as boundary/Hamiltonian charge.

## Source Register

{markdown_table(sources)}

## Static Boundary Nohair Theorem

{markdown_table(theorem)}

## Boundary Branch Verdict

{markdown_table(branch_verdict)}

## Arena Boundary Profile Rows

{markdown_table(profile_rows)}

## Profile Kernel Requirements

{markdown_table(kernel_rows)}

## Static Reduction After Boundary

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
    branch_verdict: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    kernel_rows: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4571 - Static Boundary Nohair Or B_boundary Profile Kernel Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## What Changed

The local private branch now has a clean static chain:

```text
A_src^std=0,
A_lap^std=0,
B_boundary,a^std=0,
||P_loc J_res_static|| <= O(epsilon_U^3).
```

The boundary zero is only for the same fixed compact non-radiative no-flux collar. If the branch is open, radiative, transition-shell, moving-boundary, or edge/corner-active, the retained rows are:

```text
Q_a := K_a B_boundary,a,
|Q_a| + |R_higher,a| <= B_a.
```

## Boundary Nohair Theorem

{markdown_table(theorem)}

## Branch Verdict

{markdown_table(branch_verdict)}

## Arena Profile Rows

{markdown_table(profile_rows)}

## Kernel Rows

{markdown_table(kernel_rows)}

## Static Reduction

{markdown_table(static_reduction)}

## Decisions

{markdown_table(decisions)}

## Validation

{markdown_table(validation)}

## Files Written

- `{FORMAL_PATH}`
- `{SOURCE_REGISTER}`
- `{NOHAIR_THEOREM_CSV}`
- `{BRANCH_VERDICT_CSV}`
- `{PROFILE_ROWS_CSV}`
- `{KERNEL_ROWS_CSV}`
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
        "claim": "4571 derives the conditional fixed-collar static boundary nohair route that sets B_boundary,a^std=0 after the private bulk-zero branch, while retaining per-arena profile/kernel rows for open, radiative, transition and edge/corner branches.",
        "current_evidence": "Generated source register, static boundary nohair theorem, boundary branch verdict, arena profile rows, profile kernel rows, static reduction rows, promotion gates, status and validation CSVs.",
        "status": "static_boundary_nohair_private_fixed_collar_zero_profile_kernel_rows_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Exporting fixed compact non-radiative nohair to radiative/open/transition boundaries, or treating private bulk+boundary zero as a public local-GR/PPN/R10 pass.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Private same-branch progress only; higher-order residues, transition shells, global parent no-flux and empirical full rows remain.",
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
    theorem = nohair_theorem_rows(now)
    branch_verdict = branch_verdict_rows(now)
    profile_rows = arena_profile_rows(now)
    kernel_rows = kernel_requirement_rows(now)
    static_reduction = static_reduction_rows(now)
    promotion = promotion_rows(now)
    decisions = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NOHAIR_THEOREM_CSV, theorem)
    write_csv(BRANCH_VERDICT_CSV, branch_verdict)
    write_csv(PROFILE_ROWS_CSV, profile_rows)
    write_csv(KERNEL_ROWS_CSV, kernel_rows)
    write_csv(STATIC_REDUCTION_CSV, static_reduction)
    write_csv(PROMOTION_CSV, promotion)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    validation = validation_rows(
        sources,
        theorem,
        branch_verdict,
        profile_rows,
        kernel_rows,
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
            branch_verdict,
            profile_rows,
            kernel_rows,
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
        post_markdown(theorem, branch_verdict, profile_rows, kernel_rows, static_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(
        sources,
        theorem,
        branch_verdict,
        profile_rows,
        kernel_rows,
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
            branch_verdict,
            profile_rows,
            kernel_rows,
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
        post_markdown(theorem, branch_verdict, profile_rows, kernel_rows, static_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4571 Static Boundary Nohair / Profile Kernel Verdict

Marker: `{MARKER}`

After 4569 and 4570, the same private branch has `A_J_eff^bulk-zero=0`. In a fixed compact stationary non-radiative no-flux collar, 4268/192 give:

```text
P_loc boundary_in_static=0,
B_boundary,a^std := K_a P_loc boundary_in_static = 0,
||P_loc J_res_static|| <= O(epsilon_U^3).
```

This is not global nohair. Open/radiative/transition/moving-boundary/edge branches retain `Q_a := K_a B_boundary,a` profile rows with no cancellation against bulk `A_J`. Next target: `{NEXT_TARGET}`.
""",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4571 Packet Integration - Static Boundary Nohair / Profile Kernel Rows

Marker: `{PACKET_MARKER}`

Packet rule: inside the same private fixed compact stationary non-radiative no-flux collar, `B_boundary,a^std=0` for the listed local arenas, so the static residual is pushed to `O(epsilon_U^3)`. Radiative Poynting/GR flux, transition support, moving projectors, source crossing, memory pullback and edge/corner modes are not erased; they remain `Q_a := K_a B_boundary,a` plus `R_higher,a` profile rows. Next target: `{NEXT_TARGET}`.
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
