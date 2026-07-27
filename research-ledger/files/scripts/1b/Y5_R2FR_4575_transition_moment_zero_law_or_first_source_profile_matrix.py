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

CHECKPOINT = "4575"
CLAIM_ID = "L-417"
BRANCH_ID = "MTS_R2FR_Y5_TRANSITION_MOMENT_ZERO_LAW_OR_SOURCE_PROFILE_MATRIX_4575"
MARKER = "PPC4161_TRANSITION_MOMENT_ZERO_LAW_OR_SOURCE_PROFILE_MATRIX_4575"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_COMMON_MODE_SUBTRACTED_MOMENT_LAW_4575"
DECISION = "COMMON_MODE_SUBTRACTED_MOMENT_LAW_DERIVED_RAW_SHELL_PARENT_SIGNING_AND_MATRIX_VALUES_MISSING_NONCLAIM"
NEXT_TARGET = "4576-Y5-R2FR-same-worldtube-Hilbert-source-lock-or-residual-moment-bound.md"

FORMAL_PATH = FORMAL / "591-PPC4161-transition-moment-zero-law-or-first-source-profile-matrix.md"
DOC_PATH = POST / "4575-Y5-R2FR-transition-moment-zero-law-or-first-source-profile-matrix.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4574 = POST / "4574-Y5-R2FR-P_metric-loc-zero-theorem-or-transition-profile-source-pack.md"
CSV_4574_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4574_GRAM_PROJECTOR_THEOREM.csv"
CSV_4574_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4574_SOURCE_PROFILE_MATRIX_PACK.csv"
CSV_4574_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4574_NEXT_TARGET.csv"
CSV_4289_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4289_STATUS.csv"
CSV_4289_DECOMP = SOURCE_DIR / "P8_Y5_R2FR_4289_TRANSITION_DECOMPOSITION.csv"
CSV_4291_LOCK = SOURCE_DIR / "P8_Y5_R2FR_4291_TRANSITION_SOURCE_LOCK_REDUCTION.csv"
CSV_4294_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4294_SOURCE_KERNEL_ZERO_THEOREM_CLAUSES.csv"
CSV_4355_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4355_THEOREM_ROWS.csv"
CSV_4355_KERNEL = SOURCE_DIR / "P8_Y5_R2FR_4355_KERNEL_MEMBERSHIP_ROWS.csv"
CSV_4356_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4356_THEOREM_ROWS.csv"
CSV_4356_COMMON = SOURCE_DIR / "P8_Y5_R2FR_4356_COMMON_MODE_ROWS.csv"
CSV_4356_HAIR = SOURCE_DIR / "P8_Y5_R2FR_4356_HAIR_BOUND_ROWS.csv"
CSV_4356_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4356_ZERO_CLAUSE_ROWS.csv"
CSV_4534_GRAMMAR = SOURCE_DIR / "P8_Y5_R2FR_4534_STRICT_MTS_PRIMITIVE_GRAMMAR.csv"
CSV_4534_INDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4534_CONSTRUCTOR_EXHAUSTION_INDUCTION.csv"
CSV_4537_RANK = SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv"
CSV_4538_COLLAPSE = SOURCE_DIR / "P8_Y5_R2FR_4538_LOCAL_RESIDUAL_VECTOR_COLLAPSE.csv"
EQ_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4575_SOURCE_REGISTER.csv"
COMMON_MODE_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_COMMON_MODE_SUBTRACTED_MOMENT_THEOREM.csv"
RESIDUAL_HAIR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_RESIDUAL_MOMENT_HAIR_MAP.csv"
PROFILE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_FIRST_SOURCE_PROFILE_MATRIX.csv"
CALIBRATION_GUARD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_CALIBRATION_GUARD.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_MOMENT_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4575_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4575_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
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


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        ("SRC4575_00_4574_doc", "4574 moment theorem document", DOC_4574, "P_metric,loc Sigma_metric[q_tr] = 0"),
        ("SRC4575_01_4574_theorem", "4574 Gram projector theorem", CSV_4574_THEOREM, "GPT4574_2_zero_equivalence"),
        ("SRC4575_02_4574_matrix", "4574 source profile matrix pack", CSV_4574_MATRIX, "SPM4574_0_basis"),
        ("SRC4575_03_4574_next", "4574 selected moment target", CSV_4574_NEXT, "transition-moment-zero-law"),
        ("SRC4575_04_4289_status", "4289 monopole split status", CSV_4289_STATUS, "TRANSITION_MONOPOLE_ROUTE_CONDITIONAL_RESIDUAL_VECTOR_DEFINED"),
        ("SRC4575_05_4289_decomp", "4289 Hilbert monopole/residual vector", CSV_4289_DECOMP, "TDS4289_0_same_Hilbert_monopole"),
        ("SRC4575_06_4291_lock", "4291 source-lock frontier", CSV_4291_LOCK, "TR4291_1_membership"),
        ("SRC4575_07_4294_clauses", "4294 source-kernel clauses", CSV_4294_CLAUSES, "ZK4294_6_leak_projector_zero"),
        ("SRC4575_08_4355_theorem", "4355 source-kernel hair law", CSV_4355_THEOREM, "TH4355_0_clean_transition_source"),
        ("SRC4575_09_4355_kernel", "4355 kernel membership rows", CSV_4355_KERNEL, "KM4355_7_total_kernel"),
        ("SRC4575_10_4356_theorem", "4356 common-mode theorem", CSV_4356_THEOREM, "TH4356_0_static_monopole_common_mode"),
        ("SRC4575_11_4356_common", "4356 common-mode guard rows", CSV_4356_COMMON, "CM4356_0_absorbable_G_mode"),
        ("SRC4575_12_4356_hair", "4356 hair bound rows", CSV_4356_HAIR, "HB4356_6_total_remaining"),
        ("SRC4575_13_4356_zero", "4356 zero clause rows", CSV_4356_ZERO, "ZC4356_2_species_frame_source"),
        ("SRC4575_14_4534_grammar", "4534 strict primitive grammar", CSV_4534_GRAMMAR, "GRAM4534_2_forbidden_constructors"),
        ("SRC4575_15_4534_induction", "4534 common-mode induction", CSV_4534_INDUCTION, "IND4534_3_common_mode_projection"),
        ("SRC4575_16_4537_rank", "4537 component graph rank result", CSV_4537_RANK, "RR4537_2_GR_parity_adopted_branch"),
        ("SRC4575_17_4538_collapse", "4538 residual vector collapse", CSV_4538_COLLAPSE, "RV4538_0_source_weight"),
        ("SRC4575_18_eq_register", "equation register P_metric threshold", EQ_REGISTER, "P_metric,loc <= 4.212667126774669e-17"),
        ("SRC4575_19_red_team", "red-team closure warning", RED_TEAM, "P_metric,loc = 0 is still a quarantine condition"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in source_specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "common-mode-subtracted transition moment law and first profile matrix",
                "valid_for_claim": "False",
            }
        )
    return rows


def common_mode_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "CMM4575_0_basis_split",
            "statement": "Split the local metric response basis into one allowed GR/Newton Hilbert monopole mode E_0 and anomalous residual modes E_a^perp.",
            "formula": "H_metric(W_loc)=span{E_0^GR} direct_sum H_perp; P_perp E_0^GR=0",
            "derivation": "A common static Hilbert monopole is ordinary source mass, not anomalous local-GR leakage.",
            "status": "COMMON_MODE_SPLIT_DERIVED",
            "parent_signed_for_raw_shell": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "CMM4575_1_subtracted_moments",
            "statement": "The relevant transition safety moments are common-mode-subtracted residual moments.",
            "formula": "M_a^perp[q_tr] := <E_a^perp, Sigma_metric[q_tr] - C_0 Sigma_metric[q_tr]>_loc",
            "derivation": "C_0 projects the stationary l=0 Hilbert monopole into M_H^dress before local readout.",
            "status": "RESIDUAL_MOMENT_DEFINITION_DERIVED",
            "parent_signed_for_raw_shell": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "CMM4575_2_zero_equivalence_after_subtraction",
            "statement": "Local transition anomaly vanishes iff every common-mode-subtracted residual moment vanishes.",
            "formula": "P_anom Sigma_metric[q_tr]=0 iff M_a^perp[q_tr]=0 for all a",
            "derivation": "Apply the 4574 Gram theorem on H_perp after removing the permitted E_0^GR source-mass direction.",
            "status": "COMMON_MODE_SUBTRACTED_MOMENT_ZERO_LAW_DERIVED",
            "parent_signed_for_raw_shell": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "CMM4575_3_common_mode_guard",
            "statement": "The common mode can be absorbed only if it is universal, stationary, range-free, species/frame/source-label blind, same-metric/EH and boundary-owned before readout.",
            "formula": "D_tau sigma_0=D_lambda sigma_0=D_species sigma_0=D_frame sigma_0=D_source_weight sigma_0=0",
            "derivation": "This imports the 4356 calibrated-G guard and forbids hiding physical hair in measured G or GM.",
            "status": "COMMON_MODE_GUARD_INSTALLED",
            "parent_signed_for_raw_shell": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "CMM4575_4_finite_norm",
            "statement": "If exact residual moments do not vanish, the finite profile norm is the no-cancellation residual score.",
            "formula": "epsilon_moment_perp^2 = M_a^perp (G_perp^-1)^{ab} M_b^perp",
            "derivation": "This is the 4574 matrix bound restricted to anomalous modes after common-mode subtraction.",
            "status": "FINITE_RESIDUAL_MOMENT_BOUND_READY",
            "parent_signed_for_raw_shell": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_hair_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("RMH4575_0_membership", "same-worldtube Hilbert membership", "P_nonHilbert_action_domain + P_off_worldtube_readout_order", "M_a^perp undefined/active until q_tr is in the same Hilbert source before readout", "same source action and support-before-readout theorem", "4291/4294/4355"),
        ("RMH4575_1_time", "time drift", "Y_tau := ||Lie_tau q_tr||/M_H_ref", "clock/Gdot/orbital secular moment", "stationary Hamiltonian collar Lie_tau q_tr=0", "4356"),
        ("RMH4575_2_multipole", "multipoles", "Y_l>=1 := sum_l>=1 |Q_l,tr|/M_H_ref", "anisotropic Newton/PPN/orbital moment", "static exterior response has only l=0 Hilbert monopole", "4356"),
        ("RMH4575_3_species_frame_source", "species/frame/source-label hair", "Y_species_frame_source := |D_species q_tr|+|D_frame q_tr|+|Delta_source_weight_tr|", "WEP/preferred-frame/source-normalization moment", "NoSourceOnlySpeciesSlot plus same-frame descent", "4356/4534/4537"),
        ("RMH4575_4_range", "finite-range hair", "Y_lambda := |D_lambda q_tr|+|q_range_tail|", "R10/Yukawa moment", "no independent finite-range pole or lambda-dependent kernel", "4356"),
        ("RMH4575_5_nonEH", "non-EH metric readout", "Y_nonEH := ||Pi_arena Sigma_nonEH[q_tr]||", "PPN gamma/beta/clock moment", "same observed EH/coframe metric readout", "4356/4538"),
        ("RMH4575_6_boundary", "boundary/nonlocal hair", "Y_boundary := |B_tr_nonlocal|/M_H_ref", "boundary/Kperp/local-collar moment", "exact/fixed/projection-null/Hamiltonian-routed boundary", "4356/4572"),
        ("RMH4575_7_total", "total residual moment envelope", "epsilon_moment_perp <= Y_nonHilbert + Delta_Wtr + Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary", "all anomalous moment pressure", "all previous rows zero on one branch or profile matrix bound passes", "4575"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "residual_id": residual_id,
            "hair_component": component,
            "moment_component": formula,
            "local_observable_pressure": pressure,
            "zero_if": zero_if,
            "source_basis": source_basis,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, component, formula, pressure, zero_if, source_basis in components
    ]


def profile_matrix_rows(now: str) -> list[dict[str, Any]]:
    matrix_rows = [
        ("SPM4575_0_E0_GR_mass", "E_0^GR", "common Newton/Hilbert mass monopole", "M_0=<E_0,Sigma_metric[q_tr]>", "ALLOWED_ONLY_AS_M_H_DRESS", "same-worldtube static l=0 universal range-free same-metric boundary-owned", "not counted in epsilon_moment_perp"),
        ("SPM4575_1_time", "E_tau", "Gdot/clock/orbital time drift", "M_tau^perp ~ Lie_tau q_tr/M_H_ref", "MISSING_PARENT_ZERO_OR_PROFILE_VALUE", "Lie_tau q_tr=0", "Y_tau"),
        ("SPM4575_2_multipole", "E_l>=1", "anisotropic multipole/tidal source", "M_l^perp ~ Q_l>=1,tr/M_H_ref", "MISSING_PARENT_ZERO_OR_PROFILE_VALUE", "Q_l>=1,tr=0", "Y_l>=1"),
        ("SPM4575_3_species_frame_source", "E_species_frame_source", "composition/frame/source-weight residual", "M_sfs^perp ~ D_species q_tr + D_frame q_tr + Delta_source_weight_tr", "MISSING_PARENT_ZERO_OR_PROFILE_VALUE", "NoSourceOnlySpeciesSlot and same-frame descent", "Y_species_frame_source"),
        ("SPM4575_4_range", "E_lambda", "finite-range R10/Yukawa residual", "M_lambda^perp ~ D_lambda q_tr + q_range_tail", "MISSING_PARENT_ZERO_OR_PROFILE_VALUE", "no finite-range pole/range tail", "Y_lambda"),
        ("SPM4575_5_nonEH", "E_nonEH", "non-EH gamma/beta/clock readout", "M_nonEH^perp ~ Pi_arena Sigma_nonEH[q_tr]", "MISSING_PARENT_ZERO_OR_PROFILE_VALUE", "same observed EH metric/coframe readout", "Y_nonEH"),
        ("SPM4575_6_boundary", "E_boundary", "boundary/Kperp/nonlocal collar residual", "M_boundary^perp ~ B_tr_nonlocal/M_H_ref", "MISSING_PARENT_ZERO_OR_PROFILE_VALUE", "fixed/exact/projection-null/Hamiltonian-routed boundary", "Y_boundary"),
        ("SPM4575_7_total_norm", "G_perp^-1 norm", "common-mode-subtracted leakage score", "epsilon_moment_perp^2=M_a^perp(G_perp^-1)^abM_b^perp", "MISSING_PROFILE_MATRIX", "all residual rows numeric/zero", "epsilon_moment_perp"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "matrix_id": matrix_id,
            "basis_element": basis,
            "role": role,
            "moment_formula": formula,
            "current_value": value,
            "zero_condition": zero_condition,
            "maps_to_hair_row": hair,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for matrix_id, basis, role, formula, value, zero_condition, hair in matrix_rows
    ]


def calibration_guard_rows(now: str) -> list[dict[str, Any]]:
    guards = [
        ("CG4575_0_allowed", "constant universal common l=0 Hilbert monopole", "may enter M_H^dress before readout", "not a residual claim", "False"),
        ("CG4575_1_forbidden_range", "finite-range lambda-dependent tail", "must remain Y_lambda or R10 row", "cannot be hidden in G_cal", "False"),
        ("CG4575_2_forbidden_time", "time-varying transition monopole", "must remain Y_tau/Gdot/clock/orbital row", "cannot be hidden in measured GM", "False"),
        ("CG4575_3_forbidden_species", "species/frame/source-weight transition hair", "must remain Y_species_frame_source/WEP/source row", "cannot be hidden in universal calibration", "False"),
        ("CG4575_4_forbidden_nonEH", "non-EH metric readout", "must remain gamma/beta/clock source row", "cannot be renamed common mass", "False"),
        ("CG4575_5_forbidden_boundary", "unrouted boundary/nonlocal flux", "must remain boundary/Kperp row", "cannot be absorbed into bulk M_Hdress", "False"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "guard_id": guard_id,
            "case": case,
            "routing": routing,
            "forbidden_move": forbidden,
            "claim_allowed": "False",
            "valid_for_claim": valid,
        }
        for guard_id, case, routing, forbidden, valid in guards
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4575_common_only", "M_0 nonzero and all M_a^perp=0", "0.0", "4.212667126774669e-17"),
        ("CTRL4575_small_residual", "epsilon_moment_perp", "1.0e-18", "4.212667126774669e-17"),
        ("CTRL4575_large_residual", "epsilon_moment_perp", "1.0e-10", "4.212667126774669e-17"),
        ("LIVE4575_missing_profile", "epsilon_moment_perp", "MISSING_PROFILE_MATRIX", "4.212667126774669e-17"),
    ]
    rows: list[dict[str, Any]] = []
    for control_id, quantity, value, threshold in controls:
        try:
            verdict = "CONTROL_PASS_NONCLAIM" if float(value) <= float(threshold) else "CONTROL_FAIL_NONCLAIM"
        except ValueError:
            verdict = "BLOCKED_PENDING_PROFILE_MATRIX"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "generated_utc": now,
                "control_id": control_id,
                "quantity": quantity,
                "value": value,
                "threshold": threshold,
                "verdict": verdict,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4575_0_common_mode_law",
            "gate": "Common-mode-subtracted moment law is written and tied to 4574 Gram theorem.",
            "status": "PASS",
            "reason": "P_anom Sigma=0 iff all M_a^perp vanish after E_0^GR subtraction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4575_1_raw_shell_parent_signature",
            "gate": "Raw transition shell satisfies same-worldtube Hilbert source lock plus all zero-hair clauses.",
            "status": "FAIL",
            "reason": "Membership, source-lock and raw-shell parent signing remain open.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4575_2_profile_matrix_values",
            "gate": "All residual profile matrix values are numeric/source-backed or zero by theorem.",
            "status": "FAIL",
            "reason": "First matrix is symbolic and profile values remain missing.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4575_3_calibration_firewall",
            "gate": "Measured G/GM absorbs only a constant universal common mode.",
            "status": "PASS",
            "reason": "Range/time/species/frame/nonEH/boundary hair is explicitly routed to residual rows.",
            "claim_allowed": "False",
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
            "common_mode_subtracted_law_derived": "True",
            "raw_shell_parent_signed": "False",
            "first_source_profile_matrix_staged": "True",
            "profile_values_missing": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "next_target": NEXT_TARGET,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STATUS4575_0",
            "status": "COMMON_MODE_SUBTRACTED_MOMENT_LAW_READY_RAW_SHELL_UNSIGNED",
            "summary": "4575 turns the moment problem into the GR/Newton-style split: the stationary l=0 Hilbert monopole may dress M_H^dress, while residual moments M_a^perp carry all anomalous local tests. Raw shell parent signing and source-backed profile values remain missing.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The next non-circling move is to prove the same-worldtube Hilbert source lock for q_tr, because that is the first clause needed before residual moment zero can become a parent theorem; if it fails, fill the residual moment bound rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4575 — Transition moment-zero law or first source-profile matrix

Marker: `{MARKER}`  
Generated: `{now}`  
Decision: `{DECISION}`

## Short verdict

4575 improves the 4574 theorem by making the moment condition GR/Newton compatible.

The transition source does **not** need every metric moment to vanish.  The allowed exception is the ordinary, stationary, universal `l=0` Hilbert monopole that dresses the source mass:

```text
Sigma_metric[q_tr] = sigma_0 E_0^GR + Sigma_perp
M_H^dress -> M_H^dress + M_tr^H
```

The real local-GR condition is:

```text
P_anom Sigma_metric[q_tr] = 0
iff
M_a^perp[q_tr] := <E_a^perp, Sigma_metric[q_tr] - C_0 Sigma_metric[q_tr]>_loc = 0
for every anomalous local response mode a.
```

So the project has moved from:

```text
delete the transition shell
```

to:

```text
allow only the same-worldtube GR/Newton mass monopole; bound or kill every residual hair moment.
```

That is the right shape for reducing to GR/Newton without pretending `G` or `GM` is derived numerically.

## Common-mode-subtracted theorem

{markdown_table(theorem)}

## Residual moment hair map

{markdown_table(residuals)}

## First source-profile matrix

This is symbolic/source-staged, not a claim-grade numeric matrix.

{markdown_table(matrix)}

## Calibration guard

{markdown_table(guards)}

## Control rows

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: try to parent-sign the same-worldtube Hilbert source lock first; if that fails, fill the residual moment rows.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4575 transition common-mode-subtracted moment law

Marker: `{MARKER}`  
Generated: `{now}`

4575 upgrades the 4574 moment criterion by splitting the local response space into the allowed GR/Newton mass monopole `E_0^GR` and anomalous residual modes `E_a^perp`.  The transition can dress `M_H^dress` only as a stationary `l=0`, universal, range-free, species/frame/source-label blind, same-metric/EH, boundary-owned Hilbert monopole.  The local-GR condition is now `P_anom Sigma_metric[q_tr]=0 iff M_a^perp[q_tr]=0` for every residual mode.  The first source-profile matrix is staged, but raw-shell parent signing and numeric/source-backed residual moments are still missing.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4575 packet update — common-mode-subtracted transition moments

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The packet should phrase transition safety as common-mode-subtracted residual moment silence, not total deletion of `q_tr`.  A same-worldtube static Hilbert monopole may enter `M_H^dress`; time, multipole, species/frame/source, range, non-EH and boundary hair remain explicit residual moments.  This keeps the GR/Newton reduction route live while blocking measured-G backfill.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4575 derives the common-mode-subtracted transition moment law: the allowed GR/Newton Hilbert monopole may dress M_H^dress, while anomalous local-GR moments vanish only if all residual moments M_a^perp[q_tr] vanish.",
        "current_evidence": "Generated source register, common-mode-subtracted theorem rows, residual moment hair map, first source-profile matrix, calibration guard, control rows, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the common monopole exception as permission to hide time/range/species/frame/nonEH/boundary hair in measured G or GM.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Raw transition shell still needs same-worldtube Hilbert source lock or source-backed residual moment bounds.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4575_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4575_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4575_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4575_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4575_matrix_firewall",
        "all matrix rows remain nonclaim",
        all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in matrix),
        "matrix rows firewalled",
    )
    add(
        "VAL4575_missing_profile_values",
        "live residual rows expose missing profile values",
        any("MISSING" in row["current_value"] for row in matrix),
        "missing profile matrix values explicit",
    )
    add(
        "VAL4575_common_control",
        "common-only control passes",
        any(row["control_id"] == "CTRL4575_common_only" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in controls),
        "common-only control",
    )
    add(
        "VAL4575_fail_control",
        "large residual control fails",
        any(row["control_id"] == "CTRL4575_large_residual" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in controls),
        "large residual control",
    )
    add(
        "VAL4575_theorem_token",
        "common-mode-subtracted theorem token recorded",
        "M_a^perp[q_tr]" in read_text(DOC_PATH) and "COMMON_MODE_SUBTRACTED_MOMENT_ZERO_LAW_DERIVED" in read_text(COMMON_MODE_THEOREM_CSV),
        "M_a^perp theorem",
    )
    add(
        "VAL4575_decision_token",
        "decision token recorded",
        DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH),
        DECISION,
    )
    add(
        "VAL4575_next_target",
        "next target recorded",
        NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH),
        NEXT_TARGET,
    )
    add("VAL4575_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4575_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    theorem = common_mode_theorem_rows(now)
    residuals = residual_hair_rows(now)
    matrix = profile_matrix_rows(now)
    guards = calibration_guard_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    next_targets = next_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COMMON_MODE_THEOREM_CSV, theorem)
    write_csv(RESIDUAL_HAIR_CSV, residuals)
    write_csv(PROFILE_MATRIX_CSV, matrix)
    write_csv(CALIBRATION_GUARD_CSV, guards)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, theorem, residuals, matrix, guards, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        COMMON_MODE_THEOREM_CSV,
        RESIDUAL_HAIR_CSV,
        PROFILE_MATRIX_CSV,
        CALIBRATION_GUARD_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, matrix, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
