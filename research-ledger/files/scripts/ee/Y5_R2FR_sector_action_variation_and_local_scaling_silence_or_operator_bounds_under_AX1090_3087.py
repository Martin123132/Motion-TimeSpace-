from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3087"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3087-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3087_00_3086_doc": ROOT / "3086-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack-under-AX1090.md",
    "SRC3087_01_3086_next": RESIDUALS / "P8_Y5_R2FR_3086_NEXT_TARGET.csv",
    "SRC3087_02_3086_sector_audit": RESIDUALS / "P8_Y5_R2FR_3086_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
    "SRC3087_03_3086_operator_pack": RESIDUALS / "P8_Y5_R2FR_3086_OPERATOR_COEFFICIENT_PACK_NONCLAIM.csv",
    "SRC3087_04_3086_bridge_status": RESIDUALS / "P8_Y5_R2FR_3086_GR_BRIDGE_STATUS.csv",
    "SRC3087_05_1841_doc": ROOT / "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
    "SRC3087_06_1841_sector_variation": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_SECTOR_ACTION_VARIATION_LEDGER.csv",
    "SRC3087_07_1841_scaling": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_LOCAL_SCALING_LEDGER.csv",
    "SRC3087_08_1841_transfer": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_OBSTRUCTION_TRANSFER_LEDGER.csv",
    "SRC3087_09_1841_bound_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_OPERATOR_BOUND_INPUT_PACK.csv",
    "SRC3087_10_1841_priority": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_SECTOR_PRIORITY_LEDGER.csv",
    "SRC3087_11_1841_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_GR_BRIDGE_STATUS.csv",
    "SRC3087_12_1841_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_CURRENT_CORPUS_GATE.csv",
    "SRC3087_13_1009_parent_contract": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "SRC3087_14_1013_pim_flux": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "SRC3087_15_1014_pim_commutator": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "SRC3087_16_1016_worldtube_selector": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "SRC3087_17_1017_hamiltonian_lock": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    "SRC3087_18_1842_old_next": ROOT / "1842-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
    "SRC3087_19_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3087_SOURCE_REGISTER.csv",
    "sector_variation": RESIDUALS / "P8_Y5_R2FR_3087_SECTOR_ACTION_VARIATION_LEDGER.csv",
    "scaling": RESIDUALS / "P8_Y5_R2FR_3087_LOCAL_SCALING_LEDGER.csv",
    "transfer": RESIDUALS / "P8_Y5_R2FR_3087_OBSTRUCTION_TRANSFER_LEDGER.csv",
    "bound_pack": RESIDUALS / "P8_Y5_R2FR_3087_OPERATOR_BOUND_INPUT_PACK_NONCLAIM.csv",
    "priority": RESIDUALS / "P8_Y5_R2FR_3087_SECTOR_PRIORITY_LEDGER.csv",
    "bridge_status": RESIDUALS / "P8_Y5_R2FR_3087_GR_BRIDGE_STATUS.csv",
    "corpus_gate": RESIDUALS / "P8_Y5_R2FR_3087_CURRENT_CORPUS_GATE.csv",
    "score_blockers": RESIDUALS / "P8_Y5_R2FR_3087_SCORE_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3087_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3087_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3087_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3087_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3087_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "sector_variation_copy": LOCAL_BOUNDS / "sector_action_variation_3087_NONCLAIM.csv",
    "scaling_copy": LOCAL_BOUNDS / "local_scaling_ledger_3087_NONCLAIM.csv",
    "bound_pack_copy": LOCAL_BOUNDS / "operator_bound_input_pack_3087_NONCLAIM.csv",
    "bridge_status_copy": LOCAL_BOUNDS / "GR_bridge_status_3087_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3087_sector_Lagrangian_boundary_owner_FB5540_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "gate_pass",
        "score_allowed",
        "bridge_claim",
        "local_gr_claim",
        "newton_claim",
        "operator_ready",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
                return True
    return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "sector_variation_local_scaling_evidence"
            if source_id != "SRC3087_19_dotg_target"
            else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

sector_variation_rows = [
    base(
        {
            "sector_id": "SAV3087_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative",
            "candidate_action_block": "S_HD = int sqrt(-g)(c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R + ...)",
            "variation_target": "E_HD_munu",
            "variation_status": "FORM_TEMPLATE_KNOWN_PARENT_ADOPTION_UNSIGNED",
            "local_silence_test": "sector absent from parent normal form, topological, or c_HD/L_local^2 below all local tolerances",
            "result": "RETAIN_BOUND_INPUT",
        }
    ),
    base(
        {
            "sector_id": "SAV3087_1_projector_PiM",
            "sector": "Pi_M/domain/projector source-measure",
            "candidate_action_block": "Hamiltonian/topological/projector source map Pi_M J_H",
            "variation_target": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H and delta_g Pi_M projector stress",
            "variation_status": "EXACT_OBSTRUCTION_NOT_SILENCED",
            "local_silence_test": "Pi_M is a fixed chain map on the same Hilbert worldtube and delta_g Pi_M stress vanishes or is bounded",
            "result": "CONCRETE_ROOT_BLOCKER_RETURNS_TO_SOURCE_CHARGE_OWNER",
        }
    ),
    base(
        {
            "sector_id": "SAV3087_2_boundary_reference",
            "sector": "boundary/reference/improvement",
            "candidate_action_block": "S_GHY + B_ref + exact/topological improvements + symplectic boundary terms",
            "variation_target": "theta_boundary, Q_boundary, B_zero_flux, Delta_symp, H_ref_shift",
            "variation_status": "REFERENCE_LOCK_UNSIGNED",
            "local_silence_test": "fixed-before-readout reference plus zero compact linked-boundary flux",
            "result": "RETAIN_BOUND_INPUT",
        }
    ),
    base(
        {
            "sector_id": "SAV3087_3_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "candidate_action_block": "S_nonmin = int sqrt(-g)c_NM f(X,Phi,labels)L_m or A(X)J_m",
            "variation_target": "E_nonmin_munu plus modified matter/source equations",
            "variation_status": "NOT_FORBIDDEN_BY_COMPLETE_PARENT_ACTION",
            "local_silence_test": "normal form forbids the channel or maps it to WEP/clock/PPN/R10 coefficient bounds",
            "result": "RETAIN_BOUND_INPUT",
        }
    ),
    base(
        {
            "sector_id": "SAV3087_4_memory_coframe",
            "sector": "memory/coframe/preferred-frame/current-chain",
            "candidate_action_block": "S_memory/coframe with theta_X,Q_X,C_tau and tau-lock terms",
            "variation_target": "E_memory_munu, E_coframe_munu, PPN alpha_i, clock drift residuals",
            "variation_status": "LOCAL_FRAME_AND_TAU_LOCK_UNSIGNED",
            "local_silence_test": "local coframe lock and tau_source=tau_charge=tau_clock=tau_readout make preferred-frame stress zero",
            "result": "RETAIN_BOUND_INPUT",
        }
    ),
    base(
        {
            "sector_id": "SAV3087_5_source_normalization",
            "sector": "worldtube/source normalization/Hamiltonian source charge",
            "candidate_action_block": "Pi_M^H J_H, H_tau[S]-H_ref, M_H_ref, worldtube source measure",
            "variation_target": "M_H_ref, R_eq, I_commutator, Delta_ref, symplectic_boundary_flux",
            "variation_status": "EXACT_CONTRACT_WRITTEN_NOT_SIGNED",
            "local_silence_test": "M_H_ref is a same-frame dressed Hamiltonian/Hilbert charge before orbital/PPN readout",
            "result": "PRIMARY_ROOT_BLOCKER_FOR_NEWTON_GR_BRIDGE",
        }
    ),
    base(
        {
            "sector_id": "SAV3087_6_verdict",
            "sector": "sector action variation for current MTS",
            "candidate_action_block": "all retained non-EH sectors",
            "variation_target": "all DeltaE_i and source-normalization residuals",
            "variation_status": "NO_SECTOR_FULLY_SILENCED",
            "local_silence_test": "not achieved",
            "result": "EH_DOMINANCE_AND_NEWTON_REMAIN_NONCLAIM",
        }
    ),
]

scaling_rows = [
    base(
        {
            "scale_id": "SCL3087_0_higher_derivative",
            "sector": "higher-derivative",
            "dimensionless_ratio": "epsilon_HD ~ |c_HD|/L_local^2 plus operator-basis factors",
            "local_silence_condition": "epsilon_HD below PPN/R10/orbital tolerance or c_HD=0 by parent normal form",
            "status": "MISSING_COEFFICIENT_SCALE_AND_TOLERANCE",
            "bound_row": "OBI3087_1_higher_derivative",
        }
    ),
    base(
        {
            "scale_id": "SCL3087_1_projector",
            "sector": "Pi_M/projector",
            "dimensionless_ratio": "epsilon_PiM ~ |I_commutator|/M_H_ref + |projector_stress_beta_equiv|",
            "local_silence_condition": "I_commutator=0 and projector stress=0, or both are source-backed below arena bounds",
            "status": "MISSING_I_COMMUTATOR_MHREF_AND_PROJECTOR_STRESS",
            "bound_row": "OBI3087_2_projector",
        }
    ),
    base(
        {
            "scale_id": "SCL3087_2_boundary",
            "sector": "boundary/reference",
            "dimensionless_ratio": "epsilon_boundary ~ |B_zero_flux + Delta_symp + H_ref_shift|/M_H_ref",
            "local_silence_condition": "fixed reference and zero compact linked-boundary flux before readout",
            "status": "MISSING_BOUNDARY_REFERENCE_LOCK",
            "bound_row": "OBI3087_3_boundary",
        }
    ),
    base(
        {
            "scale_id": "SCL3087_3_nonminimal",
            "sector": "nonminimal matter-geometry",
            "dimensionless_ratio": "epsilon_NM ~ |c_NM q_comp| or induced source/readout coupling leakage",
            "local_silence_condition": "channel forbidden by parent object-language or bounded by WEP/clock/PPN/R10",
            "status": "MISSING_NONMINIMAL_OPERATOR_AND_COMPOSITION_MAP",
            "bound_row": "OBI3087_4_nonminimal",
        }
    ),
    base(
        {
            "scale_id": "SCL3087_4_memory_coframe",
            "sector": "memory/coframe/current-chain",
            "dimensionless_ratio": "epsilon_frame ~ preferred-frame alpha_i + clock drift + tau-lock mismatch",
            "local_silence_condition": "parent tau/coframe lock makes local preferred-frame and clock residuals zero",
            "status": "MISSING_LOCAL_FRAME_TAU_LOCK",
            "bound_row": "OBI3087_5_memory_coframe",
        }
    ),
    base(
        {
            "scale_id": "SCL3087_5_source_normalization",
            "sector": "source normalization",
            "dimensionless_ratio": "epsilon_source ~ abs(R_eq,B_zero,I_commutator,Delta_ref,Delta_symp,delta_H_tau)/M_H_ref",
            "local_silence_condition": "same-frame M_H_ref plus zero/bounded numerator components with no cancellation",
            "status": "MISSING_MHREF_AND_NUMERATOR_COMPONENTS",
            "bound_row": "OBI3087_6_source_normalization",
        }
    ),
]

transfer_rows = [
    base(
        {
            "transfer_id": "OT3087_0_broad_DeltaE_to_sector_list",
            "input_obstruction": "DeltaE_munu broad non-EH residual",
            "source_evidence": "3086 operator pack",
            "transfer_result": "split into higher-derivative, projector, boundary, nonminimal, memory/coframe and source-normalization sectors",
            "claim_status": "NONCLAIM",
            "next_requirement": "sector-specific variation/local scaling rows",
        }
    ),
    base(
        {
            "transfer_id": "OT3087_1_projector_to_same_object",
            "input_obstruction": "[d,Pi_M]J_H and delta_g Pi_M stress",
            "source_evidence": "1013/1014",
            "transfer_result": "projector silence requires Pi_M to be a fixed chain map on the same Hilbert source worldtube",
            "claim_status": "NOT_PROVED",
            "next_requirement": "same-object Hilbert/topological equality and M_H_ref owner",
        }
    ),
    base(
        {
            "transfer_id": "OT3087_2_same_object_to_worldtube",
            "input_obstruction": "closed topological current can be the wrong conserved object",
            "source_evidence": "1015/1016 trail",
            "transfer_result": "must parent-select W_source=closure(supp J_H[tau]) and same-frame source measure",
            "claim_status": "CONDITIONAL_LEMMA_ONLY",
            "next_requirement": "parent worldtube/source-measure selector",
        }
    ),
    base(
        {
            "transfer_id": "OT3087_3_worldtube_to_Hamiltonian_lock",
            "input_obstruction": "source worldtube/source measure lacks stable charge denominator",
            "source_evidence": "1016/1017",
            "transfer_result": "need L_X, Theta_X, Q_X, boundary/reference class and tau lock before M_H_ref can normalize residuals",
            "claim_status": "PRIMARY_OWNER_GAP",
            "next_requirement": "sector Lagrangian/boundary owner or FB5540 source row",
        }
    ),
]

bound_rows = [
    base(
        {
            "row_id": "OBI3087_0_total_DeltaE",
            "quantity": "DeltaE_munu",
            "required_inputs": "sector basis; coefficient units; local scaling; absolute-sum no-cancellation guard; arena map",
            "status": "MISSING_SECTOR_BOUNDS",
            "priority": "global",
        }
    ),
    base(
        {
            "row_id": "OBI3087_1_higher_derivative",
            "quantity": "c_HD",
            "required_inputs": "parent action adoption/absence theorem; operator units; L_local; PPN/R10/orbit map",
            "status": "MISSING_OPERATOR_BASIS_UNITS_BOUNDS",
            "priority": "medium",
        }
    ),
    base(
        {
            "row_id": "OBI3087_2_projector",
            "quantity": "I_commutator;projector_stress_beta_equiv;Delta_PiM",
            "required_inputs": "Pi_M owner; M_H_ref; finite annulus integral; weak-field stress map; source paths",
            "status": "MISSING_PIM_COMMUTATOR_PROJECTOR_STRESS",
            "priority": "highest",
        }
    ),
    base(
        {
            "row_id": "OBI3087_3_boundary",
            "quantity": "B_zero_flux;Delta_symp;H_ref_shift",
            "required_inputs": "fixed reference; boundary/falloff rule; compact linked surface pair; M_H_ref; units",
            "status": "MISSING_BOUNDARY_REFERENCE_CERTIFICATE",
            "priority": "highest_coupled_to_MHref",
        }
    ),
    base(
        {
            "row_id": "OBI3087_4_nonminimal",
            "quantity": "c_nonminimal;B_obs_source_measure_over_MH",
            "required_inputs": "normal-form forbid theorem or WEP/clock/PPN/R10 projection with units and source paths",
            "status": "MISSING_NONMINIMAL_OPERATOR_MAP",
            "priority": "high",
        }
    ),
    base(
        {
            "row_id": "OBI3087_5_memory_coframe",
            "quantity": "c_memory;c_frame;tau_lock_mismatch",
            "required_inputs": "L_X/Theta_X/Q_X owner; tau generator lock; clock/PPN preferred-frame map",
            "status": "MISSING_FRAME_TAU_LOCK_OR_BOUND",
            "priority": "high",
        }
    ),
    base(
        {
            "row_id": "OBI3087_6_source_normalization",
            "quantity": "M_H_ref;R_eq_integral;delta_H_tau_nonintegrable;Delta_ref;symplectic_boundary_flux;epsilon_HPiM_integrability_abs",
            "required_inputs": "same-frame Hamiltonian source charge denominator plus all numerator components with source paths",
            "status": "MISSING_MHREF_AND_FB5540_COMPONENTS",
            "priority": "highest_root",
        }
    ),
]

priority_rows = [
    base(
        {
            "rank": "1",
            "target": "sector Lagrangian/boundary owner",
            "why": "without L_X,Theta_X,Q_X,B_ref,B_class/tau ownership, sector variation is notation not derivation",
            "next_action": "derive owners or fill FB5540 source row",
            "selection_status": "primary_next",
        }
    ),
    base(
        {
            "rank": "2",
            "target": "Hamiltonian PiM and M_H_ref denominator",
            "why": "Pi_M commutator/equality residuals cannot be normalized without a non-circular source charge",
            "next_action": "derive positive same-frame M_H_ref and reference lock",
            "selection_status": "coupled_primary",
        }
    ),
    base(
        {
            "rank": "3",
            "target": "R_eq/I_commutator/projector-stress rows",
            "why": "these are the concrete residual quantities if zero proof fails",
            "next_action": "keep nonclaim until source-backed values or theorem zeros exist",
            "selection_status": "bound_fallback",
        }
    ),
    base(
        {
            "rank": "4",
            "target": "nonminimal matter coupling descent",
            "why": "dangerous for WEP/clocks but downstream of parent action ownership",
            "next_action": "forbid by parent language or map to empirical coefficients",
            "selection_status": "queued",
        }
    ),
    base(
        {
            "rank": "5",
            "target": "higher-derivative and memory/coframe tails",
            "why": "important but need operator bases and local scale hierarchy before scoring",
            "next_action": "operator basis and scale map",
            "selection_status": "queued",
        }
    ),
]

bridge_rows = [
    base(
        {
            "status_id": "GB3087_0_sector_variation",
            "bridge_piece": "sector-by-sector action variation",
            "current_status": "INCOMPLETE_NONCLAIM",
            "evidence": "SAV3087 rows",
            "remaining_gap": "no retained non-EH sector has action owner + first variation + local scaling + empirical bound certificate",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "GB3087_1_EH_dominance",
            "bridge_piece": "EH dominance",
            "current_status": "NOT_PROVED",
            "evidence": "RSS3086 plus SAV3087_6",
            "remaining_gap": "DeltaE sectors retained and source normalization unresolved",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "GB3087_2_Newton_Poisson",
            "bridge_piece": "Newton/Poisson/source normalization",
            "current_status": "BLOCKED_AT_HAMILTONIAN_SOURCE_CHARGE",
            "evidence": "1016/1017 plus OBI3087_6",
            "remaining_gap": "M_H_ref, reference lock, tau lock, and no-cancellation numerator components missing",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "GB3087_3_empirical_route",
            "bridge_piece": "PPN/R10/clock/orbit residual scoring",
            "current_status": "NOT_SCORE_READY",
            "evidence": "OBI3087 rows",
            "remaining_gap": "rows have quantities but no source-backed numeric values or theorem zeros",
            "bridge_claim": "false",
        }
    ),
    base(
        {
            "status_id": "GB3087_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT",
            "evidence": "priority rank 1; 1017 next target",
            "remaining_gap": "derive L_X/Theta_X/Q_X plus boundary/tau ownership, or fill first FB5540 row",
            "bridge_claim": "false",
        }
    ),
]

gate_rows = [
    base(
        {
            "gate_id": "GATE3087_0_sector_silence",
            "claim": "all non-EH sectors are locally silent or suppressed",
            "gate_pass": "false",
            "status": "BLOCKED",
            "blocker": "NO_SECTOR_HAS_FULL_VARIATION_SCALING_CERTIFICATE",
        }
    ),
    base(
        {
            "gate_id": "GATE3087_1_EH_dominance",
            "claim": "EH dominance follows for current MTS",
            "gate_pass": "false",
            "status": "BLOCKED",
            "blocker": "PROJECTOR_BOUNDARY_NONMINIMAL_FRAME_SOURCE_RESIDUALS_RETAINED",
        }
    ),
    base(
        {
            "gate_id": "GATE3087_2_MHref",
            "claim": "M_H_ref is a stable same-frame Hamiltonian source denominator",
            "gate_pass": "false",
            "status": "BLOCKED",
            "blocker": "L_X_THETA_X_Q_X_REFERENCE_TAU_OWNERS_MISSING",
        }
    ),
    base(
        {
            "gate_id": "GATE3087_3_Newton_GR",
            "claim": "Newton/local GR recovery is derived",
            "gate_pass": "false",
            "status": "BLOCKED",
            "blocker": "EH_DOMINANCE_AND_SOURCE_NORMALIZATION_OPEN",
        }
    ),
    base(
        {
            "gate_id": "GATE3087_4_empirical_scoring",
            "claim": "PPN/R10/clock/orbit residual rows are score-ready",
            "gate_pass": "false",
            "status": "BLOCKED",
            "blocker": "NO_SOURCE_BACKED_THEOREM_ZERO_OR_NUMERIC_ROWS",
        }
    ),
]

score_blocker_rows = [
    base(
        {
            "blocker_id": "SBL3087_0_sector_certificates",
            "blocks": "EH dominance",
            "missing": "action owner + first variation + local scaling + empirical bound certificate for every non-EH sector",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3087_1_source_charge_owner",
            "blocks": "source-normalization and Newton bridge",
            "missing": "L_X, Theta_X, Q_X, boundary/reference/tau ownership, and same-frame M_H_ref",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3087_2_FB5540_components",
            "blocks": "operator-bound fallback",
            "missing": "M_H_ref and numerator components with units, signs, source paths and no-cancellation ledger",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3087_3_arena_projection",
            "blocks": "PPN/R10/clock/orbit residual scoring",
            "missing": "operator coefficients to observable residual maps",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3087_0_sector_result",
            "decision": "NO_NON_EH_SECTOR_FULLY_SILENCED",
            "reason": "each sector lacks at least one of action ownership, variation, theta/Q accounting, boundary/reference lock, local scaling, or empirical coefficient",
            "next_action": "retain operator bound pack",
        }
    ),
    base(
        {
            "decision_id": "DEC3087_1_projector_result",
            "decision": "PIM_COMMUTATOR_REDUCES_TO_SOURCE_CHARGE_OWNER",
            "reason": "1014-1017 show fixed-chain-map/equality/selector/reference-lock clauses are the real blockers",
            "next_action": "do not repeat broad Pi_M slogans; attack Hamiltonian source owner",
        }
    ),
    base(
        {
            "decision_id": "DEC3087_2_no_claim",
            "decision": "LOCAL_GR_NEWTON_NOT_CLAIMED",
            "reason": "EH dominance and source-normalization gates remain blocked",
            "next_action": "keep all local and empirical gates false",
        }
    ),
    base(
        {
            "decision_id": "DEC3087_3_best_next",
            "decision": "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT",
            "reason": "this is the first missing structure that could make Pi_M^H, M_H_ref, boundary lock, and tau lock derivable rather than fitted",
            "next_action": "3088-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3087_0_sector_silence",
            "claim": "all non-EH sectors are silent or locally suppressed",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "no sector has full variation/scaling certificate",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3087_1_EH_dominance",
            "claim": "EH dominance follows",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "projector, boundary, nonminimal, memory and source residuals are retained",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3087_2_Newton_GR",
            "claim": "Newton/local GR recovery is derived",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "M_H_ref and source-normalization owner are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3087_3_empirical_scoring",
            "claim": "PPN/R10/clock/orbit residual rows can score",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "no source-backed theorem-zero or numeric rows exist",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3087_0_3088",
            "next_checkpoint": "3088-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_sector_Lagrangian_boundary_owner_or_FB5540_source_row_under_AX1090_3088.py",
            "mission": "derive L_X/Theta_X/Q_X plus B_ref/B_class/tau ownership for the Hamiltonian source charge, or fill a source-backed FB5540 row with M_H_ref and all numerator components",
            "starting_equation": "epsilon_source ~ abs(R_eq,B_zero,I_commutator,Delta_ref,Delta_symp,delta_H_tau)/M_H_ref",
            "claim_policy": "no Newton/local-GR claim until M_H_ref and every FB5540 numerator component are theorem-zero or source-backed nonclaim rows with units, signs, source paths and no-cancellation bookkeeping",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["sector_variation"], sector_variation_rows)
write_csv(OUTPUTS["scaling"], scaling_rows)
write_csv(OUTPUTS["transfer"], transfer_rows)
write_csv(OUTPUTS["bound_pack"], bound_rows)
write_csv(OUTPUTS["priority"], priority_rows)
write_csv(OUTPUTS["bridge_status"], bridge_rows)
write_csv(OUTPUTS["corpus_gate"], gate_rows)
write_csv(OUTPUTS["score_blockers"], score_blocker_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["sector_variation"], BRANCH_OUTPUTS["sector_variation_copy"])
copy_csv(OUTPUTS["scaling"], BRANCH_OUTPUTS["scaling_copy"])
copy_csv(OUTPUTS["bound_pack"], BRANCH_OUTPUTS["bound_pack_copy"])
copy_csv(OUTPUTS["bridge_status"], BRANCH_OUTPUTS["bridge_status_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(copy_path),
            "copy_exists": str(copy_path.exists()),
            "copy_parse_ok": str(csv_ok(copy_path)),
            "status": "BRANCH_COPY_READY_NONCLAIM" if copy_path.exists() else "BRANCH_COPY_MISSING",
        }
    )
    for copy_id, source_path, copy_path in [
        ("BR3087_0_sector_variation", OUTPUTS["sector_variation"], BRANCH_OUTPUTS["sector_variation_copy"]),
        ("BR3087_1_scaling", OUTPUTS["scaling"], BRANCH_OUTPUTS["scaling_copy"]),
        ("BR3087_2_bound_pack", OUTPUTS["bound_pack"], BRANCH_OUTPUTS["bound_pack_copy"]),
        ("BR3087_3_bridge_status", OUTPUTS["bridge_status"], BRANCH_OUTPUTS["bridge_status_copy"]),
        ("BR3087_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)

DOC.write_text("# 3087 - Sector Action Variation\n\nPreparing validation.\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    source_register
    + sector_variation_rows
    + scaling_rows
    + transfer_rows
    + bound_rows
    + priority_rows
    + bridge_rows
    + gate_rows
    + score_blocker_rows
    + decision_rows
    + claim_rows
    + next_rows
    + branch_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_sector_ids = {
    "SAV3087_0_higher_derivative",
    "SAV3087_1_projector_PiM",
    "SAV3087_2_boundary_reference",
    "SAV3087_3_nonminimal",
    "SAV3087_4_memory_coframe",
    "SAV3087_5_source_normalization",
    "SAV3087_6_verdict",
}
required_scaling_ids = {
    "SCL3087_0_higher_derivative",
    "SCL3087_1_projector",
    "SCL3087_2_boundary",
    "SCL3087_3_nonminimal",
    "SCL3087_4_memory_coframe",
    "SCL3087_5_source_normalization",
}
required_bound_ids = {
    "OBI3087_0_total_DeltaE",
    "OBI3087_1_higher_derivative",
    "OBI3087_2_projector",
    "OBI3087_3_boundary",
    "OBI3087_4_nonminimal",
    "OBI3087_5_memory_coframe",
    "OBI3087_6_source_normalization",
}
required_gate_ids = {
    "GATE3087_0_sector_silence",
    "GATE3087_1_EH_dominance",
    "GATE3087_2_MHref",
    "GATE3087_3_Newton_GR",
    "GATE3087_4_empirical_scoring",
}
sector_verdict = next(row for row in sector_variation_rows if row["sector_id"] == "SAV3087_6_verdict")
source_bound_row = next(row for row in bound_rows if row["row_id"] == "OBI3087_6_source_normalization")
primary_priority = next(row for row in priority_rows if row["rank"] == "1")
bridge_next = next(row for row in bridge_rows if row["status_id"] == "GB3087_4_next")

validation_rows = [
    base(
        {
            "validation_id": "VAL3087_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs if output_path != OUTPUTS["validation"])),
            "requirement": "all generated and branch-copy CSVs parse cleanly before validation write",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3087_03_sector_variation_complete",
            "passed": str(required_sector_ids.issubset({row["sector_id"] for row in sector_variation_rows}) and not has_claim_true(sector_variation_rows)),
            "requirement": "sector action variation rows cover all retained non-EH sectors and remain nonclaim",
            "evidence": OUTPUTS["sector_variation"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_04_no_sector_silenced",
            "passed": str(sector_verdict["variation_status"] == "NO_SECTOR_FULLY_SILENCED" and sector_verdict["result"] == "EH_DOMINANCE_AND_NEWTON_REMAIN_NONCLAIM"),
            "requirement": "no non-EH sector is promoted as fully silent",
            "evidence": OUTPUTS["sector_variation"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_05_scaling_rows_complete",
            "passed": str(required_scaling_ids.issubset({row["scale_id"] for row in scaling_rows}) and not has_claim_true(scaling_rows)),
            "requirement": "local scaling ledger covers higher-derivative, projector, boundary, nonminimal, memory and source-normalization sectors",
            "evidence": OUTPUTS["scaling"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_06_transfer_primary_owner_gap",
            "passed": str(any(row["transfer_id"] == "OT3087_3_worldtube_to_Hamiltonian_lock" and row["claim_status"] == "PRIMARY_OWNER_GAP" for row in transfer_rows)),
            "requirement": "obstruction transfer identifies Hamiltonian/source-charge owner as primary gap",
            "evidence": OUTPUTS["transfer"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_07_bound_pack_complete_nonclaim",
            "passed": str(required_bound_ids.issubset({row["row_id"] for row in bound_rows}) and not has_claim_true(bound_rows)),
            "requirement": "operator-bound input pack covers total DeltaE and all retained sectors as nonclaim rows",
            "evidence": OUTPUTS["bound_pack"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_08_source_normalization_root",
            "passed": str(source_bound_row["priority"] == "highest_root" and "M_H_ref" in source_bound_row["quantity"]),
            "requirement": "source-normalization/M_H_ref row is marked as highest-root blocker",
            "evidence": OUTPUTS["bound_pack"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_09_priority_primary_owner",
            "passed": str(primary_priority["target"] == "sector Lagrangian/boundary owner" and primary_priority["selection_status"] == "primary_next"),
            "requirement": "sector Lagrangian/boundary owner selected as primary next target",
            "evidence": OUTPUTS["priority"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_10_bridge_next_owner",
            "passed": str(bridge_next["current_status"] == "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT" and not has_claim_true(bridge_rows)),
            "requirement": "GR bridge status selects source-owner/FB5540 next without claim promotion",
            "evidence": OUTPUTS["bridge_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_11_current_gates_block",
            "passed": str(required_gate_ids.issubset({row["gate_id"] for row in gate_rows}) and all(row["gate_pass"] == "false" for row in gate_rows) and not has_claim_true(gate_rows)),
            "requirement": "all local/empirical claim gates remain blocked",
            "evidence": OUTPUTS["corpus_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_12_score_blockers_active",
            "passed": str(not has_claim_true(score_blocker_rows) and all(row["status"] == "BLOCKS_SCORE" for row in score_blocker_rows)),
            "requirement": "sector certificates, source-charge owner, FB5540 components and arena projection blockers remain active",
            "evidence": OUTPUTS["score_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_13_no_claim_promoted",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no EH-dominance, Newton, local-GR, PPN, WEP, R10, clock, orbital or source-normalization claim is promoted",
            "evidence": "claim field scan",
        }
    ),
    base(
        {
            "validation_id": "VAL3087_14_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3088-Y5-R2FR-sector-Lagrangian-boundary-owner")),
            "requirement": "next target selects sector Lagrangian/boundary owner or FB5540 source row",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_15_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3087_16_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3087_17_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3087_18_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3087 outputs remains zero",
            "evidence": f"formalization_3087_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3087_19_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3087_20_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3087 - Sector Action Variation and Local Scaling Silence or Operator Bounds

Status: `Y5_R2FR_3087_no_sector_silenced_source_charge_owner_next`

Generated: `{RUN_UTC}`

## Verdict

3087 forces every retained non-EH local sector through the same discipline: action owner, first variation, boundary/theta/Q accounting, local scaling, and empirical fallback row.

No retained non-EH sector is fully silenced. That means EH dominance and Newton/local-GR recovery remain nonclaim.

The useful narrowing is sharper than before: the generic `DeltaE_munu` problem has become a source-charge owner problem. Without `L_X`, `Theta_X`, `Q_X`, boundary/reference ownership, tau lock, and a stable same-frame `M_H_ref`, the PiM/worldtube route cannot derive Newton or local GR without fitting the source normalization.

## Sector Action Variation Ledger

{md_table(sector_variation_rows, ["sector_id", "sector", "variation_status", "local_silence_test", "result"])}

## Local Scaling Ledger

{md_table(scaling_rows, ["scale_id", "sector", "dimensionless_ratio", "status", "bound_row"])}

## Obstruction Transfer Ledger

{md_table(transfer_rows, ["transfer_id", "input_obstruction", "transfer_result", "claim_status", "next_requirement"])}

## Operator Bound Input Pack

{md_table(bound_rows, ["row_id", "quantity", "required_inputs", "status", "priority"])}

## Sector Priority Ledger

{md_table(priority_rows, ["rank", "target", "why", "next_action", "selection_status"])}

## GR Bridge Status

{md_table(bridge_rows, ["status_id", "bridge_piece", "current_status", "remaining_gap", "bridge_claim"])}

## Current Corpus Gate

{md_table(gate_rows, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Score Blockers

{md_table(score_blocker_rows, ["blocker_id", "blocks", "missing", "status"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Sector action variation ledger: `{OUTPUTS["sector_variation"]}`
- Local scaling ledger: `{OUTPUTS["scaling"]}`
- Obstruction transfer ledger: `{OUTPUTS["transfer"]}`
- Operator bound input pack: `{OUTPUTS["bound_pack"]}`
- Sector priority ledger: `{OUTPUTS["priority"]}`
- GR bridge status: `{OUTPUTS["bridge_status"]}`
- Current corpus gate: `{OUTPUTS["corpus_gate"]}`
- Score blockers: `{OUTPUTS["score_blockers"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["sector_variation_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["scaling_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["bound_pack_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["bridge_status_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
remove_pycache()

print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")
