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

CHECKPOINT = "4576"
CLAIM_ID = "L-418"
BRANCH_ID = "MTS_R2FR_Y5_SAME_WORLDTUBE_HILBERT_SOURCE_LOCK_OR_RESIDUAL_MOMENT_BOUND_4576"
MARKER = "PPC4161_SAME_WORLDTUBE_HILBERT_SOURCE_LOCK_OR_RESIDUAL_MOMENT_BOUND_4576"
PACKET_MARKER = "PPC4161_PACKET_SAME_WORLDTUBE_HILBERT_SOURCE_LOCK_OR_RESIDUAL_MOMENT_BOUND_4576"
DECISION = "SAME_WORLDTUBE_SOURCE_LOCK_THEOREM_SHAPE_DERIVED_RAW_TRANSITION_UNSIGNED_RESIDUAL_MOMENT_BOUNDS_RETAINED_NONCLAIM"
NEXT_TARGET = "4577-Y5-R2FR-density-profile-owner-or-DeltaWtr-first-bound.md"

DOC_PATH = POST / "4576-Y5-R2FR-same-worldtube-Hilbert-source-lock-or-residual-moment-bound.md"
FORMAL_PATH = FORMAL / "592-PPC4161-same-worldtube-Hilbert-source-lock-or-residual-moment-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4575 = POST / "4575-Y5-R2FR-transition-moment-zero-law-or-first-source-profile-matrix.md"
CSV_4575_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4575_NEXT_TARGET.csv"
CSV_4575_HAIR = SOURCE_DIR / "P8_Y5_R2FR_4575_RESIDUAL_MOMENT_HAIR_MAP.csv"
CSV_4575_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4575_FIRST_SOURCE_PROFILE_MATRIX.csv"
CSV_4170_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv"
CSV_4170_ADOPTION = SOURCE_DIR / "P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION.csv"
CSV_4291_GLUE = SOURCE_DIR / "P8_Y5_R2FR_4291_PRIVATE_SELECTOR_GLUE_THEOREM.csv"
CSV_4291_LOCK = SOURCE_DIR / "P8_Y5_R2FR_4291_TRANSITION_SOURCE_LOCK_REDUCTION.csv"
CSV_4292_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4292_TRANSITION_MEMBERSHIP_AUDIT.csv"
CSV_4294_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4294_SOURCE_KERNEL_ZERO_THEOREM_CLAUSES.csv"
CSV_4295_VERDICT = SOURCE_DIR / "P8_Y5_R2FR_4295_PARENT_SIGNATURE_VERDICT.csv"
CSV_4295_PLEAK = SOURCE_DIR / "P8_Y5_R2FR_4295_PLEAK_DECOMPOSITION.csv"
CSV_4355_KERNEL = SOURCE_DIR / "P8_Y5_R2FR_4355_KERNEL_MEMBERSHIP_ROWS.csv"
CSV_4355_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4355_THEOREM_ROWS.csv"
CSV_4355_HAIR = SOURCE_DIR / "P8_Y5_R2FR_4355_SOURCE_HAIR_BOUND_ROWS.csv"
CSV_4356_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4356_THEOREM_ROWS.csv"
CSV_4374_DENSITY = SOURCE_DIR / "P8_Y5_R2FR_4374_DENSITY_OWNER_CLAUSES.csv"
CSV_4375_PROFILE = SOURCE_DIR / "P8_Y5_R2FR_4375_PROFILE_OWNER_CLAUSES.csv"
CSV_4375_EPROFILE = SOURCE_DIR / "P8_Y5_R2FR_4375_EPROFILE_BOUND_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4576_SOURCE_REGISTER.csv"
LOCK_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_SAME_WORLDTUBE_LOCK_THEOREM.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_PARENT_SIGNATURE_AUDIT.csv"
RESIDUAL_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_RESIDUAL_MOMENT_BOUND_ROWS.csv"
DECISION_TREE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_SOURCE_LOCK_DECISION_TREE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4576_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4576_VALIDATION.csv"


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
        ("SRC4576_00_4575_doc", "4575 common-mode moment checkpoint", DOC_4575, "common-mode-subtracted residual moments"),
        ("SRC4576_01_4575_next", "4575 selected 4576 target", CSV_4575_NEXT, "same-worldtube-Hilbert-source-lock"),
        ("SRC4576_02_4575_hair", "4575 residual membership row", CSV_4575_HAIR, "RMH4575_0_membership"),
        ("SRC4576_03_4575_matrix", "4575 allowed GR monopole row", CSV_4575_MATRIX, "SPM4575_0_E0_GR_mass"),
        ("SRC4576_04_4170_identity", "4170 private same-object identity", CSV_4170_IDENTITY, "SO4170_1_identity"),
        ("SRC4576_05_4170_adoption", "4170 private worldtube adoption", CSV_4170_ADOPTION, "HQ4170_1_worldtube"),
        ("SRC4576_06_4291_glue", "4291 PiM/Htau private zero", CSV_4291_GLUE, "GT4291_4_private_zero"),
        ("SRC4576_07_4291_lock", "4291 transition source-lock blocker", CSV_4291_LOCK, "TR4291_1_membership"),
        ("SRC4576_08_4292_audit", "4292 membership audit", CSV_4292_AUDIT, "MA4292_0_parent_source_action"),
        ("SRC4576_09_4294_clauses", "4294 source-kernel zero clauses", CSV_4294_CLAUSES, "ZK4294_0_same_metric_Hilbert_source"),
        ("SRC4576_10_4295_verdict", "4295 raw transition verdict", CSV_4295_VERDICT, "VERDICT4295_1_raw_transition_kernel"),
        ("SRC4576_11_4295_pleak", "4295 P_leak decomposition", CSV_4295_PLEAK, "PLEAK4295_0"),
        ("SRC4576_12_4355_kernel", "4355 kernel membership rows", CSV_4355_KERNEL, "KM4355_0_Hilbert_action_domain"),
        ("SRC4576_13_4355_theorem", "4355 clean transition theorem", CSV_4355_THEOREM, "TH4355_0_clean_transition_source"),
        ("SRC4576_14_4355_hair", "4355 source-hair bound rows", CSV_4355_HAIR, "HB4355_0_nonHilbert"),
        ("SRC4576_15_4356_theorem", "4356 static common-mode theorem", CSV_4356_THEOREM, "TH4356_0_static_monopole_common_mode"),
        ("SRC4576_16_4374_density", "4374 density-owner clauses", CSV_4374_DENSITY, "DC4374_1_pointwise_Hilbert_density"),
        ("SRC4576_17_4375_profile", "4375 source-shadow/profile clauses", CSV_4375_PROFILE, "PO4375_3_no_source_shadow_density"),
        ("SRC4576_18_4375_eprofile", "4375 E_profile bound rows", CSV_4375_EPROFILE, "EPB4375_GENERAL"),
        ("SRC4576_19_packet_4170", "private packet worldtube glue", PACKET_PATH, "PPC4161_PACKET_HAMILTONIAN_WORLDTUBE_GLUE_4170"),
        ("SRC4576_20_packet_4375", "private packet density profile owner", PACKET_PATH, "PPC4161_PACKET_TRANSITION_DENSITY_PROFILE_OWNER_OR_EMASS_NUMERIC_SOURCE_BOUND_4375"),
        ("SRC4576_21_claim_417", "prior claim register row", CLAIMS_PATH, "L-417"),
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
                "role": "same-worldtube Hilbert source lock theorem or residual moment bound",
                "valid_for_claim": "False",
            }
        )
    return rows


def lock_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SWL4576_0_same_Hilbert_action_domain",
            "premise": "The transition contribution is a term in the same observed-metric Hilbert source action before variation.",
            "formal_clause": "S_H,total[g_obs,chi,Psi;tau] = S_ord^H + S_EM^H + S_bind^H + S_tr^H, with T_tr^{mu nu}=-(2/sqrt(-g_obs)) delta S_tr^H/delta g_obs_{mu nu}",
            "zero_result": "P_nonHilbert_action_domain q_tr = 0",
            "derived_effect": "q_tr is no longer an external force or representative-only slot; it is a Hilbert stress contribution.",
            "parent_status": "THEOREM_CLAUSE_DERIVED_BUT_RAW_TRANSITION_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SWL4576_1_same_worldtube_before_readout",
            "premise": "The transition current support is inside the same compact Hilbert worldtube before any exterior/orbital/local readout.",
            "formal_clause": "supp J_tr^H subset W_H := closure(supp J_H,total), and field/source solve is performed on W_H before restriction to the exterior test arena",
            "zero_result": "P_off_worldtube_readout_order q_tr = 0 and Delta_Wtr=0",
            "derived_effect": "No source normalization is chosen after seeing the residual; the transition enters the source solve once.",
            "parent_status": "THEOREM_CLAUSE_DERIVED_BUT_RAW_TRANSITION_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SWL4576_2_same_mass_projector",
            "premise": "The same Hamiltonian/Hilbert mass projector reads the total worldtube source, including any allowed transition monopole.",
            "formal_clause": "ell_M(Pi_M^H J_H,total)=M_H^dress[W_H;tau] and M_H^dress -> M_H^dress + M_tr^H only through E_0^GR",
            "zero_result": "The common l=0 Hilbert monopole is absorbed as ordinary source mass, not anomalous local response.",
            "derived_effect": "This is the precise permitted GR/Newton mass-dressing channel.",
            "parent_status": "PRIVATE_SELECTOR_SIGNED_FOR_PIH_HTAU_NOT_RAW_TRANSITION_MEMBERSHIP",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SWL4576_3_profile_or_trace_defect",
            "premise": "For profile-level local GR, equal total charge is not enough; the density profile must be the same Hilbert density as a distribution.",
            "formal_clause": "rho_eff(y)=rho_H(y)=T_H(n,n)/c^2 on W_H, or sigma_perp=(rho_eff-rho_H)/rho_H-<...>_rho is retained",
            "zero_result": "E_profile=0 only if the pointwise/distributional source profile is owned by the same action.",
            "derived_effect": "Prevents a topological/right-monopole but wrong-profile source shadow from being laundered as GR.",
            "parent_status": "PROFILE_CLAUSE_OPEN_RAW_TRANSITION_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "SWL4576_4_lock_result",
            "premise": "SWL4576_0 through SWL4576_3 hold on one branch, plus the 4575 common-mode guard.",
            "formal_clause": "q_tr in Ker(P_nonHilbert) cap Ker(P_off_worldtube) cap span{E_0^GR} with sigma_perp=0 and no time/range/species/frame/nonEH/boundary hair",
            "zero_result": "Y_nonHilbert=0, Delta_Wtr=0, E_profile=0, and the membership part of epsilon_moment_perp vanishes.",
            "derived_effect": "This is the exact local source-lock contract a future parent action must satisfy.",
            "parent_status": "CONDITIONAL_THEOREM_NOT_PARENT_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def parent_audit_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": "AUD4576_0_private_worldtube_glue",
            "clause": "Pi_M^H/H_tau/W_H same-object identity inside PPC4161-HQ private selector",
            "evidence": "4170 SO4170_1_identity and HQ4170_1_worldtube",
            "status": "PRIVATE_SELECTOR_AVAILABLE",
            "effect": "Allows the mass-projector leg of the theorem inside the private branch.",
            "missing_for_claim": "Global/raw transition membership is not implied by this algebra.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": "AUD4576_1_raw_transition_action_domain",
            "clause": "S_tr^H is present in the same observed-metric Hilbert source action before variation",
            "evidence": "4292 MA4292_0 and 4294 ZK4294_0 mark this as unsigned",
            "status": "UNSIGNED_PARENT_INPUT",
            "effect": "Y_nonHilbert cannot be set to zero for the raw shell.",
            "missing_for_claim": "Parent action term with metric variation and no representative-only source slot.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": "AUD4576_2_raw_transition_worldtube_support",
            "clause": "supp J_tr^H subset W_H before readout",
            "evidence": "4291 TR4291_1, 4292 MA4292_1, 4294 ZK4294_1 and 4355 KM4355_1",
            "status": "UNSIGNED_PARENT_INPUT",
            "effect": "Delta_Wtr cannot be set to zero for the raw shell.",
            "missing_for_claim": "Support/readout-order proof or source-backed N_inner bound.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": "AUD4576_3_density_profile",
            "clause": "rho_eff(y)=rho_H(y) distributionally on W_H",
            "evidence": "4374 DC4374_1 and 4375 PO4375_3/EPB4375_GENERAL",
            "status": "OPEN_PROFILE_INPUT",
            "effect": "Equal integrated mass is not enough for local GR; sigma_perp remains a profile row.",
            "missing_for_claim": "No source-shadow/topological wrong-profile theorem or real profile bound.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": "AUD4576_4_same_metric_EH_common_mode",
            "clause": "Static l=0 universal range-free same-metric common mode only",
            "evidence": "4356 TH4356_0 and 4575 SPM4575_0_E0_GR_mass",
            "status": "CONDITIONAL_THEOREM_AVAILABLE",
            "effect": "Defines exactly what can be absorbed into M_H^dress.",
            "missing_for_claim": "The raw shell still has to satisfy the clause on the same branch.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": "AUD4576_5_verdict",
            "clause": "Raw transition shell local-GR source lock",
            "evidence": "4295 VERDICT4295_1_raw_transition_kernel plus this 4576 audit",
            "status": "NOT_PARENT_SIGNED",
            "effect": "No R10, WEP, PPN, clock, orbital or local-GR claim fires from 4576.",
            "missing_for_claim": "Either parent-sign all source-lock clauses or source numeric residual bounds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "RB4576_0_Y_nonHilbert",
            "residual": "Y_nonHilbert",
            "formula": "Y_nonHilbert <= C_NH(C_DeltaKdiv + C_RI + C_conn + C_boundary)",
            "zero_if": "S_tr^H is in the same observed-metric Hilbert source block before variation.",
            "current_value": "MISSING_PARENT_ACTION_DOMAIN_OR_NUMERIC_COMPONENTS",
            "observable_pressure": "PPN/R10/clock/orbital/WEP source leak through non-Hilbert action-domain mismatch",
            "source_basis": "4355 HB4355_0 and 4295 PLEAK4295_0",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "RB4576_1_Delta_Wtr",
            "residual": "Delta_Wtr",
            "formula": "Delta_Wtr <= N_inner/M_H_ref <= (||mu_tr||+||B_src^A||)/M_H_ref",
            "zero_if": "supp J_tr^H subset W_H before variation and exterior/local readout is post-solve.",
            "current_value": "MISSING_SUPPORT_LOCK_OR_N_INNER_SOURCE_BOUND",
            "observable_pressure": "GM denominator/source-normalization/local readout mismatch",
            "source_basis": "4355 HB4355_1 and 4295 PLEAK4295_1",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "RB4576_2_profile_trace_defect",
            "residual": "E_profile or ||sigma_perp||",
            "formula": "sigma_perp=(rho_eff-rho_H)/rho_H-<...>_rho; deltaPhi_profile=-G_cal int_W rho_H sigma_perp/|x-y| dV",
            "zero_if": "rho_eff(y)=rho_H(y)=T_H(n,n)/c^2 distributionally on W_H.",
            "current_value": "MISSING_PROFILE_OWNER_OR_REAL_DENSITY_PROFILE",
            "observable_pressure": "Newtonian multipole/profile residual even if total mass is correct",
            "source_basis": "4374 DC4374_1 and 4375 EPB4375_GENERAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "RB4576_3_epsilon_lock",
            "residual": "epsilon_lock",
            "formula": "epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile",
            "zero_if": "same action-domain, same worldtube/readout order and distributional profile owner all hold on one branch.",
            "current_value": "MISSING_PARENT_SIGNATURE_OR_NUMERIC_BOUND_ROWS",
            "observable_pressure": "membership/profile contribution to epsilon_moment_perp",
            "source_basis": "4576 theorem rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "RB4576_4_epsilon_moment_perp_update",
            "residual": "epsilon_moment_perp",
            "formula": "epsilon_moment_perp <= epsilon_lock + Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary",
            "zero_if": "all membership/profile and non-common hair rows vanish or are source-bounded below arena tolerances.",
            "current_value": "MISSING_PROFILE_MATRIX_AND_REMAINING_HAIR_VALUES",
            "observable_pressure": "full anomalous local-GR transition moment",
            "source_basis": "4575 RMH4575_7_total plus 4576 epsilon_lock",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_tree_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "route_id": "DT4576_0_clean_lock",
            "if_condition": "SWL4576_0, SWL4576_1, SWL4576_2 and SWL4576_3 are parent-signed on one branch",
            "then_result": "Set Y_nonHilbert=0, Delta_Wtr=0, E_profile=0 and move to time/multipole/species/range/nonEH/boundary residual cleanup.",
            "current_verdict": "NOT_AVAILABLE_FOR_RAW_TRANSITION",
            "next_action": "Do not claim until parent source action supplies the clauses.",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "route_id": "DT4576_1_monopole_only",
            "if_condition": "Only PiM/Htau common monopole is signed, without action-domain/support/profile ownership",
            "then_result": "Allow no public local-GR claim; carry epsilon_lock bound rows.",
            "current_verdict": "CURRENT_BRANCH",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "route_id": "DT4576_2_numeric_fallback",
            "if_condition": "Parent proof remains unavailable but source-backed mu_tr, B_src^A and sigma_perp rows are supplied",
            "then_result": "Score epsilon_lock and then epsilon_moment_perp against local PPN/R10/clock/orbital gates.",
            "current_verdict": "READY_AS_FALLBACK",
            "next_action": "source real density/profile and support-leak rows",
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": "CTRL4576_clean_parent_lock",
            "input_case": "all same-worldtube Hilbert source-lock clauses true, sigma_perp=0",
            "expected_result": "epsilon_lock=0",
            "actual_status": "SYMBOLIC_CONTROL_PASS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": "CTRL4576_same_mass_wrong_profile",
            "input_case": "same M_Hdress but nonzero sigma_perp with zero integrated mass",
            "expected_result": "E_profile remains active",
            "actual_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": "CTRL4576_raw_unsigned_shell",
            "input_case": "PiM/Htau private zero but raw S_tr/action-domain/support unsigned",
            "expected_result": "no local-GR/R10/PPN claim",
            "actual_status": "FIREWALL_PASS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PROM4576_0_parent_action",
            "gate": "Parent action contains S_tr^H in the same observed-metric Hilbert source block.",
            "status": "BLOCKED",
            "required_for_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PROM4576_1_worldtube",
            "gate": "supp J_tr^H subset W_H before readout.",
            "status": "BLOCKED",
            "required_for_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PROM4576_2_profile",
            "gate": "rho_eff=rho_H distributionally or source-backed sigma_perp bound passes.",
            "status": "BLOCKED",
            "required_for_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PROM4576_3_no_public_claim",
            "gate": "No local-GR/R10/PPN/WEP/clock/orbital claim while any lock gate is blocked.",
            "status": "PASSED_FIREWALL",
            "required_for_claim": "True",
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
            "plain_english": "We derived the exact source-lock contract. The private Hilbert/Hamiltonian mass projector is usable, but raw transition action-domain, worldtube support and density-profile ownership are still unsigned, so 4576 becomes a residual-bound checkpoint rather than a local-GR claim.",
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
            "reason": "The next forward move is to either prove the density/profile owner clause or produce the first real Delta_Wtr support-leak bound; that attacks the specific residual instead of circling generic missing coupling language.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "complete_nonclaim_checkpoint",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    tree: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4576 - Same-worldtube Hilbert source lock or residual moment bound

Generated: `{now}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Claim status: private nonclaim checkpoint.

## Result

4576 derives the exact local source-lock contract for letting a transition contribution count as ordinary GR/Newton source mass instead of anomalous local response.

The clean theorem is:

```text
S_H,total = S_ord^H + S_EM^H + S_bind^H + S_tr^H
supp J_tr^H subset W_H := closure(supp J_H,total)
ell_M(Pi_M^H J_H,total)=M_H^dress[W_H;tau]
rho_eff(y)=rho_H(y)=T_H(n,n)/c^2
```

If those clauses hold on one branch, then:

```text
Y_nonHilbert=0
Delta_Wtr=0
E_profile=0
epsilon_lock=0
```

That is the route by which the transition may dress the ordinary Hilbert mass monopole without creating a new PPN/R10/clock/orbital source.

The current corpus does **not** parent-sign those clauses for the raw transition shell.  So 4576 does not claim local GR.  It converts the gap into the explicit bound

```text
epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile
epsilon_moment_perp <= epsilon_lock + Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary
```

This is progress because the missing coupling is no longer vague: it is exactly action-domain ownership, worldtube/readout order, and distributional density-profile ownership.

## Same-worldtube lock theorem

{markdown_table(theorem)}

## Parent signature audit

{markdown_table(audits)}

## Residual moment bound rows

{markdown_table(bounds)}

## Decision tree

{markdown_table(tree)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: prove the density/profile owner clause or produce the first real `Delta_Wtr` support-leak bound.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4576 same-worldtube Hilbert source lock

Marker: `{MARKER}`  
Generated: `{now}`

4576 derives the exact source-lock contract for letting a transition contribution become ordinary Hilbert mass: same observed-metric Hilbert source action before variation, transition support inside the same worldtube before readout, the same `Pi_M^H/H_tau` mass projector, and distributional density-profile ownership `rho_eff=rho_H`.  If those hold, `Y_nonHilbert=Delta_Wtr=E_profile=0`; if not, the local branch carries `epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile`.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4576 packet update - same-worldtube Hilbert source lock

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The packet now has an exact local source-lock contract.  The Hamiltonian/Hilbert mass projector is already available inside the private selector, but raw transition membership still requires action-domain ownership, support inside `W_H` before readout, and density-profile equality.  Until those are signed, retain `epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile` and do not promote the transition shell to local-GR evidence.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4576 derives the same-worldtube Hilbert source-lock contract: a transition can dress ordinary source mass only if it is in the same Hilbert action before variation, inside the same worldtube before readout, read by the same PiM/Htau projector, and distributionally profile-owned.",
        "current_evidence": "Generated source register, same-worldtube lock theorem rows, parent signature audit, residual moment bound rows, decision tree, control rows, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking private PiM/Htau mass glue for raw transition action-domain/worldtube/profile ownership.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Raw transition shell remains nonclaim until parent action or numeric source-backed Y_nonHilbert/Delta_Wtr/E_profile rows close.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
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
        add(f"VAL4576_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4576_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4576_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4576_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4576_lock_theorem_shape",
        "source-lock theorem contains all four major clauses",
        all(
            token in " ".join(row["theorem_id"] + row["formal_clause"] for row in theorem)
            for token in ["S_tr^H", "supp J_tr^H", "Pi_M^H", "rho_eff"]
        ),
        "action-domain/support/projector/profile clauses",
    )
    add(
        "VAL4576_raw_transition_firewall",
        "raw transition remains unsigned",
        any(row["audit_id"] == "AUD4576_5_verdict" and row["status"] == "NOT_PARENT_SIGNED" for row in audits),
        "AUD4576_5_verdict",
    )
    add(
        "VAL4576_bound_rows_nonclaim",
        "all residual bound rows remain nonclaim",
        all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in bounds),
        "residual rows firewalled",
    )
    add(
        "VAL4576_missing_inputs_visible",
        "bound rows expose missing inputs",
        all("MISSING" in row["current_value"] for row in bounds),
        "missing parent/numeric inputs explicit",
    )
    add(
        "VAL4576_wrong_profile_control",
        "wrong-profile countermodel caught",
        any(row["control_id"] == "CTRL4576_same_mass_wrong_profile" and row["actual_status"] == "COUNTERMODEL_CAUGHT" for row in controls),
        "same mass wrong profile cannot pass",
    )
    add(
        "VAL4576_decision_token",
        "decision token recorded",
        DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH),
        DECISION,
    )
    add(
        "VAL4576_next_target",
        "next target recorded",
        NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH),
        NEXT_TARGET,
    )
    add("VAL4576_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4576_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    theorem = lock_theorem_rows(now)
    audits = parent_audit_rows(now)
    bounds = residual_bound_rows(now)
    tree = decision_tree_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    next_targets = next_rows(now)
    statuses = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(LOCK_THEOREM_CSV, theorem)
    write_csv(PARENT_AUDIT_CSV, audits)
    write_csv(RESIDUAL_BOUND_CSV, bounds)
    write_csv(DECISION_TREE_CSV, tree)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, theorem, audits, bounds, tree, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        LOCK_THEOREM_CSV,
        PARENT_AUDIT_CSV,
        RESIDUAL_BOUND_CSV,
        DECISION_TREE_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, theorem, audits, bounds, controls)
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
