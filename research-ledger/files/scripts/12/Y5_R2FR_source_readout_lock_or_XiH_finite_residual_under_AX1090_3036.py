from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3036"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3036-Y5-R2FR-source-readout-lock-or-XiH-finite-residual-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3036_00_3035_doc": ROOT / "3035-Y5-R2FR-K0-CN-normalization-or-JHrho-source-bridge-under-AX1090.md",
    "SRC3036_01_3035_ratio": RESIDUALS / "P8_Y5_R2FR_3035_RATIO_PROOF_ATTEMPT.csv",
    "SRC3036_02_3035_bridge": RESIDUALS / "P8_Y5_R2FR_3035_JHRHO_SOURCE_BRIDGE_AUDIT.csv",
    "SRC3036_03_3035_finite": RESIDUALS / "P8_Y5_R2FR_3035_XIH_FINITE_RESIDUAL_CONTRACT.csv",
    "SRC3036_04_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3036_05_same_coframe": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
    "SRC3036_06_frame_lock": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
    "SRC3036_07_tau_lock": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
    "SRC3036_08_coframe_coupling": RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
    "SRC3036_09_matter_functor": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "SRC3036_10_quotient_matter": RESIDUALS / "P8_Y5_R10_1156_QUOTIENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "SRC3036_11_ordinary_owner": RESIDUALS / "P8_Y5_R10_1487_ORDINARY_MATTER_SUBACTION_OWNER.csv",
    "SRC3036_12_current_chain": RESIDUALS / "P8_Y5_R10_1488_ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT.csv",
    "SRC3036_13_PG_bridge": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3036_14_source_mass": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
    "SRC3036_15_JH_current": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
    "SRC3036_16_worldtube_glue": RESIDUALS / "P8_Y5_PARENT_QLOC_2180_PIM_JH_MASS_CURRENT_GLUE_AUDIT.csv",
    "SRC3036_17_flux_obstruction": RESIDUALS / "P8_Y5_PIM_JH_FLUX_2584_EXACT_OBSTRUCTION_VECTOR.csv",
    "SRC3036_18_readout_order": RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_READOUT_ORDER_GATE.csv",
    "SRC3036_19_matter_descent": RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv",
    "SRC3036_20_worldtube_owner": RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
    "SRC3036_21_1361_doc": ROOT / "1361-Y5-R10-RAB-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
    "SRC3036_22_1518_doc": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
    "SRC3036_23_1149_doc": ROOT / "1149-Y5-R10-source-normalization-owner-minimal-lemma-or-channel-bound-fallback.md",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3036_SOURCE_REGISTER.csv",
    "lock_theorem": RESIDUALS / "P8_Y5_R2FR_3036_SOURCE_READOUT_LOCK_THEOREM_ATTEMPT.csv",
    "lock_matrix": RESIDUALS / "P8_Y5_R2FR_3036_LOCK_CLAUSE_MATRIX.csv",
    "finite_residuals": RESIDUALS / "P8_Y5_R2FR_3036_XIH_FINITE_RESIDUAL_ROWS.csv",
    "projection_map": RESIDUALS / "P8_Y5_R2FR_3036_LOCAL_GR_RESIDUAL_PROJECTION_MAP.csv",
    "shortcut_rejections": RESIDUALS / "P8_Y5_R2FR_3036_SHORTCUT_REJECTION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3036_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3036_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3036_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3036_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3036_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "lock_theorem_copy": PARENT_ACTION / "source_readout_lock_theorem_attempt_3036_NOT_SIGNED.csv",
    "lock_matrix_copy": PARENT_ACTION / "source_readout_lock_clause_matrix_3036_NONCLAIM.csv",
    "finite_residual_copy": LOCAL_BOUNDS / "XiH_finite_residual_rows_3036_NONCLAIM.csv",
    "projection_map_copy": LOCAL_BOUNDS / "local_GR_residual_projection_map_3036_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3036_MINIMUM_SOURCE_READOUT_LOCK_OR_XIH_BOUNDS_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3036_00_3035_doc": "3035 handoff: Xi_H ratio target and source-readout lock",
    "SRC3036_01_3035_ratio": "Xi_H and A_source ratio statements",
    "SRC3036_02_3035_bridge": "JHrho source bridge blockers",
    "SRC3036_03_3035_finite": "finite Xi_H/delta_XiH/Omega_GM contract",
    "SRC3036_04_3024_ansatz": "psi_N=-log(N) and Hcore source ansatz",
    "SRC3036_05_same_coframe": "one observed coframe clauses",
    "SRC3036_06_frame_lock": "frame/source/readout lock contract",
    "SRC3036_07_tau_lock": "tau/source/charge/clock/orbit lock contract",
    "SRC3036_08_coframe_coupling": "coframe-coupling and quotient clauses",
    "SRC3036_09_matter_functor": "parent matter functor signature audit",
    "SRC3036_10_quotient_matter": "quotient matter functor audit",
    "SRC3036_11_ordinary_owner": "ordinary matter subaction owner",
    "SRC3036_12_current_chain": "ordinary matter current-chain attempt",
    "SRC3036_13_PG_bridge": "Poisson/Gauss coefficient bridge",
    "SRC3036_14_source_mass": "parent source-mass identity audit",
    "SRC3036_15_JH_current": "observed Hilbert current theorem attempt",
    "SRC3036_16_worldtube_glue": "PiM/JH mass-current glue audit",
    "SRC3036_17_flux_obstruction": "Omega_GM exact obstruction vector",
    "SRC3036_18_readout_order": "variation-before-readout guardrail",
    "SRC3036_19_matter_descent": "matter descent premise audit",
    "SRC3036_20_worldtube_owner": "worldtube source owner audit",
    "SRC3036_21_1361_doc": "prior coframe/tau/source/readout lock checkpoint",
    "SRC3036_22_1518_doc": "PiM commutator and MHref denominator bottleneck",
    "SRC3036_23_1149_doc": "minimal source-owner lemma and product-rule guard",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

lock_theorem_rows = [
    base(
        {
            "theorem_id": "SRL3036_0_target",
            "claim_piece": "source-readout lock target",
            "formal_statement": "one parent branch owns psi_N=-log(N), J_H=JHrho rho_H, W/c^2 source density rho_H, tau_obs, M_H_ref, and C_WH",
            "current_result": "TARGET_DEFINED",
            "if_signed": "Xi_H and C_WH become comparable before measured-GM/orbital fitting",
            "missing_for_claim": "MISSING_PARENT_SOURCE_READOUT_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3036_00_3035_doc"]),
        }
    ),
    base(
        {
            "theorem_id": "SRL3036_1_conditional_theorem",
            "claim_piece": "conditional first-order Newton/GR source identity",
            "formal_statement": "if SRL clauses 0..8 sign and Omega_GM=0, then Xi_H=C_WH and A_source=1 through first order",
            "current_result": "VALID_CONDITIONAL_SHAPE_ONLY",
            "if_signed": "local first-order source normalization closes without field rescaling",
            "missing_for_claim": "MISSING_ALL_PARENT_CLAUSES; MISSING_PPN_FOLLOWTHROUGH",
            "source_path": str(SOURCE_PATHS["SRC3036_01_3035_ratio"]),
        }
    ),
    base(
        {
            "theorem_id": "SRL3036_2_current_attempt",
            "claim_piece": "current MTS signs the lock",
            "formal_statement": "current corpus supplies one parent action/functor clause for all source/readout objects",
            "current_result": "NOT_SIGNED",
            "if_signed": "Xi_H finite residual branch can be demoted",
            "missing_for_claim": "MISSING_Q_OBS; MISSING_OBS_E; MISSING_MATTER_FUNCTOR; MISSING_TAU_LOCK; MISSING_MHREF; MISSING_GREF_OWNER",
            "source_path": str(SOURCE_PATHS["SRC3036_21_1361_doc"]),
        }
    ),
    base(
        {
            "theorem_id": "SRL3036_3_residual_fallback",
            "claim_piece": "finite residual fallback",
            "formal_statement": "delta_A_source = Xi_H/C_WH - 1 + R_lock with R_lock decomposed into frame, tau, worldtube, flux, source-prefactor and G_ref terms",
            "current_result": "FALLBACK_VECTOR_STAGED",
            "if_signed": "each term can be theorem-zeroed or bounded in test arenas",
            "missing_for_claim": "MISSING_NUMERIC_OR_THEOREM_ROWS",
            "source_path": str(SOURCE_PATHS["SRC3036_03_3035_finite"]),
        }
    ),
]

lock_matrix_rows = [
    base(
        {
            "lock_id": "LOCK3036_0_q_eobs",
            "object": "q and e_obs",
            "required_identity": "e_obs(Phi)=Obs_e(q(Phi)); ordinary readouts use g_obs=e_obs^T eta e_obs",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "failure_mode": "frame/source/readout mismatch",
            "source_path": str(SOURCE_PATHS["SRC3036_08_coframe_coupling"]),
            "observable_link": "WEP; clocks; PPN; source normalization",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_1_lapse_readout",
            "object": "psi_N=-log(N)",
            "required_identity": "psi_N is the observed lapse scalar in the same e_obs branch, not a freely rescaled auxiliary field",
            "current_status": "CANDIDATE_READOUT_NOT_PARENT_LOCKED",
            "failure_mode": "field-rescaling can fake A_source=1",
            "source_path": str(SOURCE_PATHS["SRC3036_04_3024_ansatz"]),
            "observable_link": "local Newton; PPN beta; clock redshift",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_2_matter_functor",
            "object": "ordinary matter action",
            "required_identity": "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A] before source/readout fitting",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "hidden matter/source frame or material marker",
            "source_path": str(SOURCE_PATHS["SRC3036_09_matter_functor"]),
            "observable_link": "WEP; clocks; EM; source charge",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_3_no_source_prefactor",
            "object": "source/action weight",
            "required_identity": "no Hom(species/source label -> gravitational source prefactor) exists in the parent grammar",
            "current_status": "COUNTERMODEL_SURVIVES",
            "failure_mode": "JHrho changes without changing ordinary matter EOM shape",
            "source_path": str(SOURCE_PATHS["SRC3036_12_current_chain"]),
            "observable_link": "Xi_H; WEP; source-normalized Newton",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_4_JH_rhoH",
            "object": "J_H=JHrho rho_H",
            "required_identity": "Hcore source current is the same observed Hilbert/source density used by W/c^2",
            "current_status": "BRIDGE_NOT_PARENT_SIGNED",
            "failure_mode": "Xi_H and C_WH source different densities",
            "source_path": str(SOURCE_PATHS["SRC3036_15_JH_current"]),
            "observable_link": "Xi_H; C_WH; measured GM",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_5_tau",
            "object": "tau_obs",
            "required_identity": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs",
            "current_status": "BLOCKED_NONCLAIM",
            "failure_mode": "source charge and clock/orbit normalization use different time generators",
            "source_path": str(SOURCE_PATHS["SRC3036_07_tau_lock"]),
            "observable_link": "M_H_ref; Gdot; clocks; orbital",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_6_worldtube",
            "object": "W_source and support",
            "required_identity": "W_source=closure(supp J_H[tau_obs]) fixed before orbital/readout fitting",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "failure_mode": "source mask/projector chosen after measurement",
            "source_path": str(SOURCE_PATHS["SRC3036_20_worldtube_owner"]),
            "observable_link": "measured GM; I_commutator; R_eq",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_7_MHref_Gref",
            "object": "M_H_ref and G_ref",
            "required_identity": "H_tau, H_ref, M_H_ref and G_ref are fixed by parent charge before orbital GM is used",
            "current_status": "MISSING_DENOMINATOR_OWNER",
            "failure_mode": "comparator GR/orbital GM imports the answer",
            "source_path": str(SOURCE_PATHS["SRC3036_14_source_mass"]),
            "observable_link": "Newton; local GR; orbital systems",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_8_OmegaGM",
            "object": "Omega_GM",
            "required_identity": "Omega_GM=-Pi_M dJ_extra+[d,Pi_M]J_H+A_parent+tails = 0 or finite below bounds",
            "current_status": "RETAINED_OBSTRUCTION",
            "failure_mode": "measured mass differs from source current mass",
            "source_path": str(SOURCE_PATHS["SRC3036_17_flux_obstruction"]),
            "observable_link": "GM flux; R10; PPN; orbital",
        }
    ),
    base(
        {
            "lock_id": "LOCK3036_9_verdict",
            "object": "source-readout lock",
            "required_identity": "LOCK3036_0 through LOCK3036_8 all parent-signed in one branch",
            "current_status": "LOCK_NOT_PROVED",
            "failure_mode": "A_source remains formula/residual, not GR limit",
            "source_path": str(SOURCE_PATHS["SRC3036_22_1518_doc"]),
            "observable_link": "local Newton/GR status",
        }
    ),
]

finite_residual_rows = [
    base(
        {
            "residual_id": "XIR3036_0_XiH",
            "quantity": "Xi_H",
            "definition": "-JHrho/(C_N K0)",
            "formula": "MISSING_RATIO_VALUE",
            "units": "same_as_C_WH once rho_H and C_H0 units are fixed",
            "needed_to_score": "source-backed finite Xi_H or theorem Xi_H=C_WH",
            "observable_link": "local Newton first-order source normalization",
            "current_status": "MISSING_VALUE_NONCLAIM",
        }
    ),
    base(
        {
            "residual_id": "XIR3036_1_delta_XiH",
            "quantity": "delta_XiH",
            "definition": "Xi_H/C_WH - 1",
            "formula": "Xi_H/(4*pi*G_ref/c^2)-1",
            "units": "dimensionless",
            "needed_to_score": "Xi_H, C_WH and G_ref parent-owned or source-backed",
            "observable_link": "PPN beta/gamma source stability; R10; orbital",
            "current_status": "MISSING_VALUE_NONCLAIM",
        }
    ),
    base(
        {
            "residual_id": "XIR3036_2_R_frame",
            "quantity": "R_frame",
            "definition": "source/readout frame mismatch contribution",
            "formula": "Delta_frame_source + b_g + b_dis + b_A",
            "units": "dimensionless after M_H_ref normalization",
            "needed_to_score": "one observed coframe theorem or finite frame leak rows",
            "observable_link": "WEP; clocks; PPN; source charge",
            "current_status": "RETAINED_NONCLAIM",
        }
    ),
    base(
        {
            "residual_id": "XIR3036_3_R_tau",
            "quantity": "R_tau",
            "definition": "tau/source/charge/clock/orbit mismatch",
            "formula": "Delta_tau_n plus boundary/reference time normalization terms",
            "units": "dimensionless or rate after arena projection",
            "needed_to_score": "tau_obs lock or finite tau residual profile",
            "observable_link": "Gdot; clocks; orbital; local GR",
            "current_status": "RETAINED_NONCLAIM",
        }
    ),
    base(
        {
            "residual_id": "XIR3036_4_R_prefactor",
            "quantity": "R_prefactor",
            "definition": "source-only/species/action prefactor mismatch",
            "formula": "delta_w_A or delta_JHrho after common-mode subtraction",
            "units": "dimensionless",
            "needed_to_score": "no-source-prefactor theorem or finite WEP/source rows",
            "observable_link": "WEP; source-normalized Newton",
            "current_status": "RETAINED_NONCLAIM",
        }
    ),
    base(
        {
            "residual_id": "XIR3036_5_R_worldtube",
            "quantity": "R_worldtube",
            "definition": "source support/worldtube/projector mismatch",
            "formula": "R_eq + I_commutator + B_zero_flux",
            "units": "dimensionless after M_H_ref normalization",
            "needed_to_score": "worldtube glue or equality/commutator/source rows",
            "observable_link": "measured GM; R10; orbital",
            "current_status": "RETAINED_NONCLAIM",
        }
    ),
    base(
        {
            "residual_id": "XIR3036_6_Omega_GM",
            "quantity": "Omega_GM",
            "definition": "compact-exterior measured-GM obstruction",
            "formula": "-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent + tails",
            "units": "GM_flux_or_dimensionless_after_MHref_normalization",
            "needed_to_score": "theorem-zero or finite obstruction vector",
            "observable_link": "Newton; PPN; orbital; R11",
            "current_status": "RETAINED_NONCLAIM",
        }
    ),
    base(
        {
            "residual_id": "XIR3036_7_delta_A_total",
            "quantity": "delta_A_source_total_abs",
            "definition": "no-cancellation envelope for first-order source normalization",
            "formula": "abs(delta_XiH)+abs(R_frame)+abs(R_tau)+abs(R_prefactor)+abs(R_worldtube)+abs(Omega_GM/M_H_ref)",
            "units": "dimensionless",
            "needed_to_score": "all component values or theorem-zero rows in one norm convention",
            "observable_link": "local-GR/Newton promotion gate",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
        }
    ),
]

projection_rows = [
    base(
        {
            "projection_id": "PROJ3036_0_Newton",
            "arena": "source-normalized Newton",
            "requires": "delta_XiH=0 and R_lock=0 or finite below Newton/orbital bounds",
            "current_status": "BLOCKED",
            "blocking_rows": "XIR3036_1; XIR3036_5; XIR3036_6",
        }
    ),
    base(
        {
            "projection_id": "PROJ3036_1_PPN",
            "arena": "PPN beta/gamma/preferred-frame",
            "requires": "first-order Newton source identity plus second-order Hcore/readout stability",
            "current_status": "BLOCKED_UPSTREAM",
            "blocking_rows": "XIR3036_1 through XIR3036_7",
        }
    ),
    base(
        {
            "projection_id": "PROJ3036_2_R10",
            "arena": "short-range/R10",
            "requires": "source charge and range/coupling rows projected into alpha(lambda)",
            "current_status": "NONCLAIM_SMOKE_ONLY",
            "blocking_rows": "Xi_H, Omega_GM, source-prefactor rows",
        }
    ),
    base(
        {
            "projection_id": "PROJ3036_3_clocks",
            "arena": "clock/redshift/fine-structure",
            "requires": "same e_obs/tau and constant-sector lock",
            "current_status": "BLOCKED",
            "blocking_rows": "R_frame; R_tau; matter constants",
        }
    ),
    base(
        {
            "projection_id": "PROJ3036_4_orbital",
            "arena": "orbital/GM transfer",
            "requires": "M_H_ref and G_ref before orbital readout",
            "current_status": "BLOCKED",
            "blocking_rows": "Omega_GM; R_worldtube; G_ref owner",
        }
    ),
]

shortcut_rows = [
    base(
        {
            "rejection_id": "REJ3036_0_field_rescale",
            "shortcut": "rescale psi_N or C_N to force A_source=1",
            "status": "REJECTED",
            "reason": "psi_N=-log(N) fixes a physical lapse readout unless the parent readout map changes with it",
        }
    ),
    base(
        {
            "rejection_id": "REJ3036_1_orbital_GM",
            "shortcut": "use measured orbital GM as M_H_ref or G_ref proof",
            "status": "REJECTED",
            "reason": "orbital GM is the output of the source transfer, not an allowed denominator proof",
        }
    ),
    base(
        {
            "rejection_id": "REJ3036_2_EH_import",
            "shortcut": "import EH/GR Poisson coefficient as parent C_WH",
            "status": "REJECTED",
            "reason": "comparator GR can define the target but cannot prove the MTS parent coupling",
        }
    ),
    base(
        {
            "rejection_id": "REJ3036_3_Ward_only",
            "shortcut": "Ward conservation alone proves measured source mass",
            "status": "REJECTED",
            "reason": "projected product rule and Pi_M/worldtube equality remain active",
        }
    ),
    base(
        {
            "rejection_id": "REJ3036_4_post_readout_mask",
            "shortcut": "choose Pi_M, W_source, or source support after fitting readout",
            "status": "REJECTED",
            "reason": "variation-before-readout and source support ownership are required",
        }
    ),
    base(
        {
            "rejection_id": "REJ3036_5_declare_no_prefactor",
            "shortcut": "declare no source-only weights without parent grammar",
            "status": "REJECTED",
            "reason": "source-prefactor countermodel survives until ordinary matter action grammar is parent-owned",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3036_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "source-readout lock synthesis is grounded in existing corpus rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3036_1_conditional_theorem",
            "gate": "conditional lock theorem is explicitly written",
            "result": any(row["theorem_id"] == "SRL3036_1_conditional_theorem" for row in lock_theorem_rows),
            "notes": "conditional only, not claim",
        }
    ),
    base(
        {
            "gate_id": "GATE3036_2_lock_matrix_complete",
            "gate": "lock matrix contains q/eobs, lapse, matter, JH, tau, worldtube, MHref/Gref and Omega_GM",
            "result": all(
                any(row["object"] == object_name for row in lock_matrix_rows)
                for object_name in ["q and e_obs", "psi_N=-log(N)", "ordinary matter action", "J_H=JHrho rho_H", "tau_obs", "W_source and support", "M_H_ref and G_ref", "Omega_GM"]
            ),
            "notes": "one-branch lock remains unproved",
        }
    ),
    base(
        {
            "gate_id": "GATE3036_3_finite_residual_vector",
            "gate": "finite residual vector covers delta_XiH, frame, tau, prefactor, worldtube and Omega_GM",
            "result": all(
                any(row["quantity"] == quantity for row in finite_residual_rows)
                for quantity in ["delta_XiH", "R_frame", "R_tau", "R_prefactor", "R_worldtube", "Omega_GM"]
            ),
            "notes": "values are not filled",
        }
    ),
    base(
        {
            "gate_id": "GATE3036_4_shortcuts_rejected",
            "gate": "known fake closure routes are rejected",
            "result": len(shortcut_rows) >= 6 and all(row["status"] == "REJECTED" for row in shortcut_rows),
            "notes": "prevents convention/local-GR overclaim",
        }
    ),
    base(
        {
            "gate_id": "GATE3036_5_lock_parent_signed",
            "gate": "source-readout lock is parent-signed",
            "result": False,
            "notes": "q/Obs_e, matter functor, tau, source prefactor, MHref/Gref and Omega_GM remain unsigned",
        }
    ),
    base(
        {
            "gate_id": "GATE3036_6_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no local Newton/GR/PPN claim is made",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3036_0_lock_result",
            "question": "does 3036 prove the source-readout lock?",
            "answer": "NO",
            "reason": "the theorem package is exact enough to state, but the parent q/eobs, matter functor, no-prefactor grammar, tau/MHref/Gref and Omega_GM clauses remain unsigned",
            "next_action": "try the minimum parent action clause that owns source current, lapse readout, W source density and charge normalization together",
        }
    ),
    base(
        {
            "decision_id": "DEC3036_1_progress",
            "question": "what changed?",
            "answer": "the local-GR first-order gate is now one theorem or one finite residual vector",
            "reason": "A_source is no longer a vague coupling; it is Xi_H/C_WH plus named lock residuals",
            "next_action": "either prove the lock package or acquire/bound delta_XiH and the residual vector",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3036_0_3037",
            "next_checkpoint": "3037-Y5-R2FR-minimum-source-readout-lock-parent-clause-or-XiH-bound-inputs-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_minimum_source_readout_lock_parent_clause_or_XiH_bound_inputs_under_AX1090_3037.py",
            "mission": "derive the minimum parent action/functor clause that simultaneously owns J_H, psi_N=-log(N), W/c^2 source density, tau/M_H_ref and G_ref, or stage source-backed Xi_H/delta_XiH/Omega_GM input rows",
            "starting_equation": "delta_A_source = Xi_H/C_WH - 1 + R_lock",
            "do_not_repeat": "do not rerun K0-only, Ward-only, or coframe-only gates as if sufficient",
            "claim_policy": "no Newton/local-GR/PPN claim until source-readout lock signs or finite residuals are sourced and below arena bounds",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "lock_theorem": lock_theorem_rows,
    "lock_matrix": lock_matrix_rows,
    "finite_residuals": finite_residual_rows,
    "projection_map": projection_rows,
    "shortcut_rejections": shortcut_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["lock_theorem"], BRANCH_OUTPUTS["lock_theorem_copy"])
shutil.copyfile(OUTPUTS["lock_matrix"], BRANCH_OUTPUTS["lock_matrix_copy"])
shutil.copyfile(OUTPUTS["finite_residuals"], BRANCH_OUTPUTS["finite_residual_copy"])
shutil.copyfile(OUTPUTS["projection_map"], BRANCH_OUTPUTS["projection_map_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for source-readout-lock route",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for output_key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for output_key, path in OUTPUTS.items() if output_key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + lock_theorem_rows
    + lock_matrix_rows
    + finite_residual_rows
    + projection_rows
    + shortcut_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3036_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3036_02_conditional_theorem",
            "passed": any(row["theorem_id"] == "SRL3036_1_conditional_theorem" for row in lock_theorem_rows),
            "requirement": "conditional source-readout lock theorem is written",
            "evidence": OUTPUTS["lock_theorem"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_03_lock_matrix",
            "passed": bool(gates[2]["result"]),
            "requirement": "lock matrix includes all source/readout clauses",
            "evidence": OUTPUTS["lock_matrix"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_04_lock_not_claimed",
            "passed": any(row["current_status"] == "LOCK_NOT_PROVED" for row in lock_matrix_rows),
            "requirement": "source-readout lock remains explicitly unproved",
            "evidence": OUTPUTS["lock_matrix"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_05_residual_vector",
            "passed": bool(gates[3]["result"]),
            "requirement": "finite residual vector covers required components",
            "evidence": OUTPUTS["finite_residuals"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_06_total_envelope",
            "passed": any(row["quantity"] == "delta_A_source_total_abs" for row in finite_residual_rows),
            "requirement": "no-cancellation total envelope row exists",
            "evidence": OUTPUTS["finite_residuals"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_07_shortcuts_rejected",
            "passed": len(shortcut_rows) >= 6 and all(row["status"] == "REJECTED" for row in shortcut_rows),
            "requirement": "fake closure shortcuts are rejected",
            "evidence": OUTPUTS["shortcut_rejections"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_08_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3036 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3036_09_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_10_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3036_11_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3036_12_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3037-"),
            "requirement": "next target selects minimum parent lock or XiH bound inputs",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3036_13_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3036 - Source-Readout Lock Or XiH Finite Residual under AX1090

Status: `Y5_R2FR_3036_source_readout_lock_not_proved_XiH_residual_vector_staged_3037_next`

## Verdict

3036 attacks the exact bridge instead of circling `K0`, `C_N`, or Ward conservation. The conditional theorem is now sharp:

If one parent branch owns the Hcore source current, the physical lapse readout `psi_N=-log(N)`, the `W/c^2` source density, the same observed coframe, the same `tau`, the same compact worldtube, and the parent `M_H_ref/G_ref` charge normalization, with `Omega_GM=0`, then

`Xi_H=C_WH`

and therefore

`A_source=1`

at first order.

That theorem package is **not** parent-signed in the current corpus. The good news is that the failure is no longer foggy: the local-GR first-order gate is now

`delta_A_source = Xi_H/C_WH - 1 + R_lock`,

where `R_lock` is decomposed into frame, tau, prefactor, worldtube/projector, and measured-GM obstruction terms.

## Source-Readout Lock Theorem Attempt

{md_table(lock_theorem_rows, ["theorem_id", "claim_piece", "formal_statement", "current_result", "missing_for_claim"])}

## Lock Clause Matrix

{md_table(lock_matrix_rows, ["lock_id", "object", "required_identity", "current_status", "failure_mode", "observable_link"])}

## XiH Finite Residual Rows

{md_table(finite_residual_rows, ["residual_id", "quantity", "definition", "formula", "needed_to_score", "current_status"])}

## Local-GR Residual Projection Map

{md_table(projection_rows, ["projection_id", "arena", "requires", "current_status", "blocking_rows"])}

## Shortcut Rejection Ledger

{md_table(shortcut_rows, ["rejection_id", "shortcut", "status", "reason"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "do_not_repeat", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print("3036 verdict: source-readout lock not proved; Xi_H residual vector staged.")
