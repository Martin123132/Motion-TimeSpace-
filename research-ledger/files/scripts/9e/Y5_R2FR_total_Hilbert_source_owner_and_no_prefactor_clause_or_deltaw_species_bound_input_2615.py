from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_TOTAL_HILBERT_SOURCE_GATE_2615"
CHECKPOINT_ID = "2615"

DOC = ROOT / "2615-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_LINEAGE_LEDGER.csv",
    "noether_collapse": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
    "source_owner": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
    "no_prefactor": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv",
    "countermodel": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_COUNTERMODEL_LEDGER.csv",
    "deltaw_block": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_DELTAW_BLOCK_BOUND_INPUT.csv",
    "source_zero": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2615_VALIDATION.csv",
}

COPY_TARGETS = {
    "noether_collapse": LOCAL_BOUNDS / "Noether_exchange_collapse_theorem_2615_NONCLAIM.csv",
    "deltaw_block": LOCAL_BOUNDS / "Deltaw_block_bound_input_2615_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Total_Hilbert_source_zero_status_2615_NONCLAIM.csv",
    "next_target": QUEUE / "JR2615_EXCHANGE_GRAPH_CONNECTIVITY_NEXT.csv",
}

FALSE_FLAGS = {
    "score_ready": False,
    "valid_prediction_row": False,
    "valid_for_claim": False,
    "claim_allowed": False,
    "accepted_for_scoring": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def false_flags() -> dict[str, bool]:
    return dict(FALSE_FLAGS)


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2615_00_2614_handoff_doc",
            "source_key": "2614_total_hilbert_next",
            "source_path": ROOT / "2614-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
            "needles": ["NEXT2614_0_primary", "NO_SOURCE_PREFACTOR_AND_TOTAL_HILBERT_OWNER_IS_NEXT", "VAL2614_OVERALL"],
            "role": "current 26xx handoff selecting total-Hilbert source owner/no-prefactor target",
        },
        {
            "source_id": "SRC2615_01_2614_parent_signature",
            "source_key": "2614_parent_signature_requirements",
            "source_path": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_PARENT_SIGNATURE_REQUIREMENTS.csv",
            "needles": ["PS2614_1_no_source_prefactors", "PS2614_2_total_Hilbert_owner", "PS2614_5_verdict"],
            "role": "current parent signature gap for source-side coupling",
        },
        {
            "source_id": "SRC2615_02_2614_deltaw_species",
            "source_key": "2614_delta_w_species_interface",
            "source_path": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_DELTAW_SPECIES_BOUND_INTERFACE.csv",
            "needles": ["DWS2614_0_delta_w_species", "DWS2614_4_R_source_species"],
            "role": "current species residual that 2615 refines to block residual",
        },
        {
            "source_id": "SRC2615_03_1765_doc",
            "source_key": "1765_prior_total_hilbert_checkpoint",
            "source_path": ROOT / "1765-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md",
            "needles": ["NEC1765_2_weight_collapse", "DEC1765_3_best_next", "VAL1765_OVERALL"],
            "role": "prior checkpoint proving conditional Noether exchange collapse",
        },
        {
            "source_id": "SRC2615_04_1765_noether",
            "source_key": "1765_noether_exchange_collapse",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
            "needles": ["NEC1765_2_weight_collapse", "NEC1765_5_current_verdict"],
            "role": "prior collapse theorem and parent-unsigned verdict",
        },
        {
            "source_id": "SRC2615_05_1765_source_owner",
            "source_key": "1765_total_hilbert_source_owner",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
            "needles": ["THO1765_3_source_shadow_ban", "THO1765_4_owner_verdict"],
            "role": "prior total Hilbert owner and source-shadow gap",
        },
        {
            "source_id": "SRC2615_06_1765_no_prefactor",
            "source_key": "1765_no_source_prefactor_attempt",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv",
            "needles": ["NSP1765_2_exchange_filter", "NSP1765_4_current_verdict"],
            "role": "prior no-prefactor partial theorem",
        },
        {
            "source_id": "SRC2615_07_1765_deltaw_block",
            "source_key": "1765_deltaw_block_input",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1765_DELTAW_BLOCK_BOUND_INPUT.csv",
            "needles": ["DWB1765_0_delta_w_block", "DWB1765_4_nonclaim_lock"],
            "role": "prior block-residual nonclaim interface",
        },
        {
            "source_id": "SRC2615_08_954_parent_action",
            "source_key": "954_parent_action_clause",
            "source_path": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative", "PAC954_4_nonHilbert_current_split"],
            "role": "source-side parent action signature clauses",
        },
        {
            "source_id": "SRC2615_09_955_minimal_matter",
            "source_key": "955_minimal_matter_lemma",
            "source_path": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "needles": ["MMA955_1_same_action_principle", "MMA955_6_verdict"],
            "role": "same-action principle and parent-unsigned minimal matter verdict",
        },
        {
            "source_id": "SRC2615_10_977_constant_certificate",
            "source_key": "977_constant_source_certificate",
            "source_path": OUT / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
            "needles": ["CSC977_3_hilbert_source_current", "CSC977_7_verdict"],
            "role": "Hilbert source current and constant/source universality guardrails",
        },
        {
            "source_id": "SRC2615_11_1488_delta_w_lock",
            "source_key": "1488_delta_w_residual_lock",
            "source_path": OUT / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
            "needles": ["WA1488_2_species_label_slot", "WA1488_5_current_norm_slot", "MISSING_PARENT_INPUT"],
            "role": "older delta_w lock confirming no source-weight claim without parent input",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_key": spec["source_key"],
                    "source_path": spec["source_path"],
                    "source_exists": spec["source_path"].exists(),
                    "needles": spec["needles"],
                    "needles_present": not missing,
                    "missing_needles": missing,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "lineage_id": "LIN2615_0_current_parent",
            "input_checkpoint": "2614",
            "input_artifact": "P8_Y5_SPECIES_FORGETTING_GATE_2614_*",
            "imported_result": "species-label forgetting depends on total Hilbert owner and no source-only prefactors",
            "2615_use": "turn coupling problem into Bianchi/Noether exchange-block law",
        },
        {
            "lineage_id": "LIN2615_1_prior_noether_branch",
            "input_checkpoint": "1765",
            "input_artifact": "P8_Y5_PARENT_QLOC_1765_*",
            "imported_result": "relative weights collapse along nonzero exchange-current edges but disconnected blocks remain",
            "2615_use": "preserve real derivation gain in current 26xx chain",
        },
        {
            "lineage_id": "LIN2615_2_parent_action_signature",
            "input_checkpoint": "954/955/977",
            "input_artifact": "parent action, minimal matter and constant-source certificates",
            "imported_result": "same-action source owner is clean but source-shadow/non-Hilbert bypasses remain unsigned",
            "2615_use": "identify exact parent clauses for source-side GR/Newton coupling",
        },
        {
            "lineage_id": "LIN2615_3_residual_refinement",
            "input_checkpoint": "2614+1765",
            "input_artifact": "delta_w_species and delta_w_block bound rows",
            "imported_result": "loose species residual is overbroad; block residual is the sharper nonclaim object",
            "2615_use": "rename live residual to delta_w_block for future bounds",
        },
        {
            "lineage_id": "LIN2615_4_claim_policy",
            "input_checkpoint": "all",
            "input_artifact": "claim gates and validation ledgers",
            "imported_result": "no local-GR/Newton/WEP/PPN/clock/orbital/R10 claim with block/source-shadow gates open",
            "2615_use": "keep all claim flags false",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def noether_collapse_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "NEC2615_0_setup",
            "claim_piece": "weighted source conservation problem",
            "mathematical_form": "E_munu=kappa sum_i w_i T_i_munu with nabla_mu E^{mu nu}=0",
            "status": "SETUP_EXACT",
            "derivation_result": "Bianchi requires nabla_mu(sum_i w_i T_i^{mu nu})=0 on matter shell",
            "parent_signed": False,
            "remaining_gap": "which T_i are legitimate parent source components is not yet signed",
        },
        {
            "theorem_id": "NEC2615_1_exchange_identity",
            "claim_piece": "Noether exchange graph",
            "mathematical_form": "nabla_mu T_i^{mu nu}=C_i^nu, sum_i C_i^nu=0",
            "status": "NOETHER_IDENTITY_FORM",
            "derivation_result": "interacting subcurrents need not be separately conserved; only the full Hilbert current is conserved",
            "parent_signed": False,
            "remaining_gap": "need parent decomposition and exchange-current owner",
        },
        {
            "theorem_id": "NEC2615_2_weight_collapse",
            "claim_piece": "relative weights collapse on every live exchange edge",
            "mathematical_form": "0=sum_i w_i C_i^nu; edge i<->j gives (w_i-w_j) C_ij^nu=0, hence w_i=w_j if C_ij is not identically zero",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "derivation_result": "Bianchi plus interaction exchange forbids relative source weights inside each connected exchange component",
            "parent_signed": False,
            "remaining_gap": "must prove ordinary matter source graph is connected and no source-shadow term bypasses the exchange graph",
        },
        {
            "theorem_id": "NEC2615_3_connected_component_law",
            "claim_piece": "block law for remaining prefactors",
            "mathematical_form": "w_i=w_C for all i in connected component C; T_active=sum_C w_C T_C",
            "status": "EXACT_BLOCK_LAW",
            "derivation_result": "relative species weights reduce to block weights over conserved disconnected components",
            "parent_signed": False,
            "remaining_gap": "source blocks and ordinary-matter connectivity are not yet parent-certified",
        },
        {
            "theorem_id": "NEC2615_4_common_mode",
            "claim_piece": "connected ordinary matter gives only common calibration",
            "mathematical_form": "connected graph => T_active=w_star T_total and kappa_eff=kappa w_star",
            "status": "CLEAN_IF_CONNECTED",
            "derivation_result": "if ordinary matter is one connected exchange component, delta_w_species=0 up to Newton/G calibration",
            "parent_signed": False,
            "remaining_gap": "connected-graph premise remains unsigned",
        },
        {
            "theorem_id": "NEC2615_5_current_verdict",
            "claim_piece": "current MTS no-source-prefactor proof",
            "mathematical_form": "delta_w_species -> delta_w_block, with zero only if one ordinary exchange component",
            "status": "PARTIAL_DERIVATION_PARENT_UNSIGNED",
            "derivation_result": "relative weights are not arbitrary species knobs; they are pushed down to disconnected conserved source blocks",
            "parent_signed": False,
            "remaining_gap": "ordinary matter exchange connectivity and source-shadow exclusion must be proved or bounded",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_owner_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "owner_id": "THO2615_0_total_action",
            "claim_piece": "ordinary active source is derived from one total matter action",
            "mathematical_form": "S_matter[Psi,e_obs,theta]=sum_i S_i + S_int",
            "why_it_matters": "source is an action derivative, not an independently chosen force law",
            "status": "CONDITIONAL_OWNER_CLEAN",
            "remaining_gap": "parent action signature not yet forced for all ordinary matter",
        },
        {
            "owner_id": "THO2615_1_total_hilbert_derivative",
            "claim_piece": "active source is total Hilbert/coframe derivative",
            "mathematical_form": "T_total := delta S_matter/delta e_obs",
            "why_it_matters": "interaction and binding terms contribute to the same conserved source",
            "status": "CONDITIONAL_OWNER_CLEAN",
            "remaining_gap": "non-Hilbert or post-readout source owners must be excluded",
        },
        {
            "owner_id": "THO2615_2_interaction_stress",
            "claim_piece": "interaction stress belongs to the same source object",
            "mathematical_form": "T_total=sum_i T_i + T_int, with nabla_mu T_total^{mu nu}=0",
            "why_it_matters": "species-only weighted sources cannot ignore exchange/binding stress without a conservation price",
            "status": "DERIVATION_PRESSURE_GAINED",
            "remaining_gap": "need explicit parent decomposition for ordinary matter/binding sectors",
        },
        {
            "owner_id": "THO2615_3_source_shadow_ban",
            "claim_piece": "no separate source-shadow functional",
            "mathematical_form": "not exists S_source=sum_i w_i S_i used only in E_munu while S_matter drives nongrav dynamics",
            "why_it_matters": "forbids pure source-only weights that do not appear in the matter theory",
            "status": "BEST_PARENT_OBJECT_LANGUAGE_CLAUSE",
            "remaining_gap": "must be signed by parent grammar or derived from quotient minimality",
        },
        {
            "owner_id": "THO2615_4_nonHilbert_bypass",
            "claim_piece": "no extra ordinary non-Hilbert/source-spurion current",
            "mathematical_form": "J_src = kappa_univ T_Hilbert with J_NH=0 or retained as explicit residual",
            "why_it_matters": "prevents label dependence returning outside the Hilbert current",
            "status": "OPEN_PARALLEL_GATE",
            "remaining_gap": "non-Hilbert current split and hidden species projector are not silenced",
        },
        {
            "owner_id": "THO2615_5_owner_verdict",
            "claim_piece": "total Hilbert source owner",
            "mathematical_form": "ordinary source owner = delta S_matter/delta e_obs",
            "why_it_matters": "would close source-side GR/Newton coupling up to left-hand field equation and hidden-current gates",
            "status": "CONTRACT_READY_PARENT_UNSIGNED",
            "remaining_gap": "source-shadow ban, non-Hilbert silence and ordinary exchange connectivity remain live",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def no_prefactor_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "proof_id": "NSP2615_0_target",
            "claim_piece": "no independent source-only species prefactors",
            "mathematical_form": "partial S_matter/partial w_A = 0 for source-only w_A; equivalently no w_A coordinate exists",
            "status": "TARGET_EXACT",
            "derivation_result": "would close the no-source-prefactor clause if parent object language signs it",
            "remaining_gap": "absence of a coordinate is a parent grammar theorem, not yet derived from existing corpus",
        },
        {
            "proof_id": "NSP2615_1_same_action_filter",
            "claim_piece": "same-action principle rejects source-only duplication",
            "mathematical_form": "E_Psi=delta S_matter/delta Psi and T=delta S_matter/delta e_obs from the same S_matter",
            "status": "DERIVED_FILTER",
            "derivation_result": "separate source weights are illegal if they live only in a shadow source functional",
            "remaining_gap": "does not exclude weights that multiply real disconnected matter subactions",
        },
        {
            "proof_id": "NSP2615_2_exchange_filter",
            "claim_piece": "Bianchi/Noether exchange rejects weights across interacting sectors",
            "mathematical_form": "sum_i w_i C_i^nu=0 forces w_i=w_j on every nonzero exchange edge",
            "status": "DERIVED_CONDITIONAL_FILTER",
            "derivation_result": "relative species prefactors collapse to conserved exchange-block prefactors",
            "remaining_gap": "ordinary matter graph connectivity is not yet proved from parent sources",
        },
        {
            "proof_id": "NSP2615_3_common_prefactor",
            "claim_piece": "common prefactor is not a WEP/local-GR residual",
            "mathematical_form": "S_matter -> w_star S_matter gives kappa_eff=kappa w_star",
            "status": "COMMON_MODE_ABSORBABLE",
            "derivation_result": "one common source normalization is calibration, not composition dependence",
            "remaining_gap": "only relative block weights remain dangerous",
        },
        {
            "proof_id": "NSP2615_4_current_verdict",
            "claim_piece": "current no-source-prefactor theorem",
            "mathematical_form": "no w_A source prefactors",
            "status": "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF",
            "derivation_result": "source-only shadow weights are forbidden-by-contract; interaction-connected relative weights are forbidden conditionally; disconnected block weights remain",
            "remaining_gap": "must prove no source shadow and one connected ordinary matter exchange block, or bound delta_w_block",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "countermodel_id": "CM2615_0_disconnected_conserved_blocks",
            "countermodel": "two independently conserved ordinary source blocks",
            "mathematical_form": "nabla T_A=0, nabla T_B=0, T_active=w_A T_A+w_B T_B",
            "survives_current_constraints": True,
            "why_survives": "Bianchi allows different weights for truly disconnected conserved blocks",
            "needed_to_kill": "prove ordinary matter is one connected exchange component for the tested regime",
        },
        {
            "countermodel_id": "CM2615_1_source_shadow_functional",
            "countermodel": "source functional separate from matter-dynamics functional",
            "mathematical_form": "S_dynamics=sum_i S_i, S_source=sum_i w_i S_i",
            "survives_current_constraints": True,
            "why_survives": "same-action principle is a contract unless parent grammar forbids the shadow functional",
            "needed_to_kill": "typed object-language theorem: the active source is only delta S_matter/delta e_obs",
        },
        {
            "countermodel_id": "CM2615_2_hidden_nonHilbert_source",
            "countermodel": "non-Hilbert source current carries material labels",
            "mathematical_form": "T_active=T_Hilbert + J_label",
            "survives_current_constraints": True,
            "why_survives": "Hilbert-source theorem does not silence extra parent currents until excluded",
            "needed_to_kill": "no non-Hilbert ordinary source current clause",
        },
        {
            "countermodel_id": "CM2615_3_wrong_decomposition",
            "countermodel": "chosen species decomposition hides interaction stress or binding energy",
            "mathematical_form": "T_total != sum_A T_A unless T_int/binding included",
            "survives_current_constraints": True,
            "why_survives": "bound rows need the actual composition/source projection, not loose labels",
            "needed_to_kill": "source-backed component basis with binding/interactions included",
        },
        {
            "countermodel_id": "CM2615_4_decoupled_source_sector",
            "countermodel": "a genuinely decoupled conserved sector carries an independent block weight",
            "mathematical_form": "T_total=T_vis+T_dec, nabla T_vis=0, nabla T_dec=0, T_active=w_vis T_vis+w_dec T_dec",
            "survives_current_constraints": True,
            "why_survives": "Noether exchange collapse cannot equate weights without an exchange edge",
            "needed_to_kill": "ordinary tested matter exchange graph must be connected or decoupled block must be projected/bounded",
        },
        {
            "countermodel_id": "CM2615_5_verdict",
            "countermodel": "delta_w_block residual",
            "mathematical_form": "T_active=sum_C (1+delta_w_C) T_C over disconnected exchange components",
            "survives_current_constraints": True,
            "why_survives": "2615 collapses species weights to block weights but does not yet prove only one block",
            "needed_to_kill": "2616 exchange-graph connectivity theorem plus source-shadow ban, or finite sourced block bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def deltaw_block_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DWB2615_0_delta_w_block",
            "quantity": "delta_w_block",
            "meaning": "residual source prefactor over disconnected Noether exchange components",
            "mathematical_form": "T_active=sum_C (1+delta_w_C) T_C",
            "units": "dimensionless",
            "needed_input": "prove one connected ordinary matter block or provide finite bound on block weights",
            "status": "MISSING_EXCHANGE_CONNECTIVITY_OR_NUMERIC_BOUND",
            "source_path": OUTPUTS["noether_collapse"],
        },
        {
            "row_id": "DWB2615_1_exchange_graph",
            "quantity": "ordinary matter exchange graph",
            "meaning": "nodes are source components; edges are nonzero Noether exchange currents",
            "mathematical_form": "edge i-j iff C_ij^nu is not identically zero in tested matter regime",
            "units": "graph",
            "needed_input": "parent/source-backed node list and interaction/binding edges",
            "status": "MISSING_SOURCE_GRAPH",
            "source_path": "TBD",
        },
        {
            "row_id": "DWB2615_2_source_shadow_coefficient",
            "quantity": "A_source_shadow",
            "meaning": "source-only functional bypass amplitude",
            "mathematical_form": "||delta_v S_source-shadow||_{E*} <= A_source_shadow",
            "units": "E*_dual_or_declared_arena_units",
            "needed_input": "parent theorem-zero or finite coefficient bound",
            "status": "MISSING_SOURCE_SHADOW_ZERO_OR_BOUND",
            "source_path": "TBD",
        },
        {
            "row_id": "DWB2615_3_projection",
            "quantity": "composition-to-block projection",
            "meaning": "map test-body composition to block-source fractions",
            "mathematical_form": "eta_AB ~ sum_C (f_C^A-f_C^B) delta_w_C",
            "units": "dimensionless",
            "needed_input": "material fractions, binding fractions, and experiment-specific source projection",
            "status": "MISSING_ARENA_PROJECTION",
            "source_path": "TBD",
        },
        {
            "row_id": "DWB2615_4_R_source_block",
            "quantity": "R_source_block",
            "meaning": "block-prefactor contribution to ordinary active-source residual",
            "mathematical_form": "||R_source,block||_{E*} <= U_B K_block ||delta_w_block|| + U_B A_source_shadow",
            "units": "E*_dual_or_declared_arena_units",
            "needed_input": "K_block, delta_w_block bound, A_source_shadow, and arena units",
            "status": "MISSING_K_BLOCK_OPERATOR_NORM_AND_ARENA_UNITS",
            "source_path": OUTPUTS["deltaw_block"],
        },
        {
            "row_id": "DWB2615_5_bound_table",
            "quantity": "delta_w_block_bound",
            "meaning": "finite empirical upper bound if exchange graph has more than one block",
            "mathematical_form": "|delta_w_C-delta_w_D| <= bound_from_WEP_R10_PPN_clock_or_orbital_projection",
            "units": "dimensionless",
            "needed_input": "source-backed local bound table with projection convention",
            "status": "MISSING_SOURCE_BACKED_BOUND_TABLE",
            "source_path": QUEUE / "JR2615_EXCHANGE_GRAPH_CONNECTIVITY_NEXT.csv",
        },
        {
            "row_id": "DWB2615_6_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "source coupling branch remains blocked until proof or bound closes",
            "mathematical_form": "claim_allowed=false until no source shadow + connected graph or finite sourced bound",
            "units": "status",
            "needed_input": "future 2616 proof/bound validation",
            "status": "NONCLAIM_LOCK",
            "source_path": OUTPUTS["claim_gates"],
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "SZ2615_0_derivation_gain",
            "quantity": "relative source prefactors",
            "current_status": "COLLAPSED_TO_EXCHANGE_BLOCKS_CONDITIONALLY",
            "evidence": "NEC2615_2 and NEC2615_3",
            "remaining_gap": "prove tested ordinary matter has one connected exchange block",
        },
        {
            "status_id": "SZ2615_1_no_source_shadow",
            "quantity": "source-shadow functional",
            "current_status": "NOT_PARENT_EXCLUDED",
            "evidence": "THO2615_3 identifies the needed typed object-language ban",
            "remaining_gap": "parent grammar must forbid a separate source functional",
        },
        {
            "status_id": "SZ2615_2_total_Hilbert_owner",
            "quantity": "total Hilbert/coframe source owner",
            "current_status": "CONDITIONAL_NOT_EXCLUSIVE",
            "evidence": "THO2615_1 is clean inside the contract",
            "remaining_gap": "exclude non-Hilbert, source-shadow and post-readout source owners",
        },
        {
            "status_id": "SZ2615_3_delta_w_species",
            "quantity": "delta_w_species",
            "current_status": "REFINED_TO_DELTA_W_BLOCK",
            "evidence": "Noether exchange collapse kills weights inside connected components",
            "remaining_gap": "block residual remains until connectivity/bound is closed",
        },
        {
            "status_id": "SZ2615_4_delta_w_block",
            "quantity": "delta_w_block",
            "current_status": "RETAINED_NONCLAIM",
            "evidence": "disconnected conserved block countermodel survives",
            "remaining_gap": "ordinary matter exchange graph or finite bound table",
        },
        {
            "status_id": "SZ2615_5_local_GR",
            "quantity": "local GR / Newton / WEP / R10 / PPN / clock / orbital branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "delta_w_block, source-shadow and non-Hilbert gates remain open",
            "remaining_gap": "no local pass until source side is theorem-zero or finite-source bounded",
        },
        {
            "status_id": "SZ2615_6_next",
            "quantity": "next derivation owner",
            "current_status": "EXCHANGE_GRAPH_CONNECTIVITY_AND_SOURCE_SHADOW_BAN_NEXT",
            "evidence": "2615 converts species-prefactor wound into graph-connectivity/source-shadow problem",
            "remaining_gap": "build 2616 exchange graph connectivity theorem or delta_w_block bound pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2615_0_noether_collapse",
            "claim": "relative weights collapse on each exchange-connected component",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_PARENT_SOURCE_COMPONENTS_AND_EXCHANGE_GRAPH_UNSIGNED",
        },
        {
            "gate_id": "GATE2615_1_connected_ordinary_matter",
            "claim": "tested ordinary matter is one connected source-exchange component",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_UNSIGNED",
        },
        {
            "gate_id": "GATE2615_2_no_source_shadow",
            "claim": "no separate source-shadow functional exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_OBJECT_LANGUAGE_SOURCE_SHADOW_BAN_UNSIGNED",
        },
        {
            "gate_id": "GATE2615_3_no_nonHilbert_label_current",
            "claim": "no non-Hilbert ordinary label-carrying source current exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NONHILBERT_SOURCE_CURRENT_SPLIT_UNSIGNED",
        },
        {
            "gate_id": "GATE2615_4_delta_w_block_zero",
            "claim": "delta_w_block=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DISCONNECTED_BLOCK_COUNTERMODEL_SURVIVES",
        },
        {
            "gate_id": "GATE2615_5_delta_w_block_bound",
            "claim": "delta_w_block finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_GRAPH_PROJECTION_BOUND_TABLE_MISSING",
        },
        {
            "gate_id": "GATE2615_6_local_GR_WEP_R10",
            "claim": "local GR / Newton / WEP / PPN / clock / orbital / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTA_W_BLOCK_AND_SOURCE_SHADOW_GATES_OPEN",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2615_0_derivation_gain",
            "decision": "NOETHER_EXCHANGE_COLLAPSE_IS_REAL_PROGRESS",
            "reason": "Bianchi conservation plus interaction exchange forces equal weights on every nonzero exchange edge",
            "next_action": "use block law instead of treating every species weight as independent",
        },
        {
            "decision_id": "DEC2615_1_no_promotion",
            "decision": "NO_LOCAL_SOURCE_CLAIM",
            "reason": "ordinary exchange graph connectivity, source-shadow exclusion and non-Hilbert source silence remain unsigned",
            "next_action": "retain nonclaim lock",
        },
        {
            "decision_id": "DEC2615_2_residual_refinement",
            "decision": "DELTA_W_SPECIES_REFINED_TO_DELTA_W_BLOCK",
            "reason": "species-level weights are overbroad if sectors exchange stress; only disconnected conserved blocks can carry independent weights",
            "next_action": "track delta_w_block rather than loose delta_w_species in future bound rows",
        },
        {
            "decision_id": "DEC2615_3_shadow_clause",
            "decision": "SOURCE_SHADOW_BAN_IS_A_NAMED_PARENT_CONTRACT",
            "reason": "same-action and exchange filters do not forbid a separate source-only functional unless parent grammar excludes it",
            "next_action": "make source-shadow ban an explicit clause in 2616",
        },
        {
            "decision_id": "DEC2615_4_best_next",
            "decision": "EXCHANGE_GRAPH_CONNECTIVITY_AND_SOURCE_SHADOW_BAN_IS_NEXT",
            "reason": "these are the exact remaining gates after the Noether collapse theorem",
            "next_action": "build 2616 ordinary matter exchange-graph connectivity theorem or delta_w_block bound pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2615_0_primary",
            "status": "selected",
            "doc": "2616-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
            "script": "scripts/Y5_R2FR_ordinary_matter_exchange_graph_connectivity_and_source_shadow_ban_or_deltaw_block_bound_2616.py",
            "task": "prove tested ordinary matter is one exchange-connected total-Hilbert source with no source-shadow functional; otherwise stage finite delta_w_block bound inputs",
            "success_condition": "delta_w_block theorem-zero or nonclaim block-bound rows with real source graph/projection/provenance",
            "guardrail": "no local-GR, Newton, WEP, PPN, clock, orbital or R10 claim from 2615",
        },
        {
            "next_id": "NEXT2615_1_fallback",
            "status": "held_fallback",
            "doc": "2616b-Y5-R2FR-deltaw-block-source-graph-bound-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_block_source_graph_bound_pack_2616b.py",
            "task": "source component graph, material projections, and experiment bounds for disconnected block weights",
            "success_condition": "finite delta_w_block envelope can be tested as nonclaim plumbing",
            "guardrail": "no placeholder row can be valid_for_claim",
        },
        {
            "next_id": "NEXT2615_2_nonHilbert_queue",
            "status": "queued_after_graph",
            "doc": "2616c-Y5-R2FR-nonHilbert-current-silence-or-label-current-bound.md",
            "script": "scripts/Y5_R2FR_nonHilbert_current_silence_or_label_current_bound_2616c.py",
            "task": "exclude or bound ordinary label-carrying non-Hilbert source currents",
            "success_condition": "J_label is theorem-zero or explicit finite residual",
            "guardrail": "Hilbert-current progress cannot hide non-Hilbert source current debt",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "noether": noether_collapse_rows(),
        "source_owner": source_owner_rows(),
        "no_prefactor": no_prefactor_rows(),
        "countermodel": countermodel_rows(),
        "deltaw_block": deltaw_block_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def copy_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        ok, count, error = csv_parses(target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2615_{key}",
                    "source_key": key,
                    "source_path": source,
                    "copy_path": target,
                    "copy_exists": target.exists(),
                    "csv_parse": ok,
                    "row_count": count,
                    "error": error,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = set(FALSE_FLAGS)
    for key, rows in rows_map.items():
        if key == "sources":
            continue
        for row in rows:
            for field in flag_fields:
                if str(row.get(field, "false")).lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(row_value(value) for value in row.values())
            if "MISSING_" not in text:
                continue
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return False
            status = str(row.get("status", row.get("attempt_status", ""))).upper()
            if status in {"READY", "PASS", "VALID_FOR_CLAIM"}:
                return False
    return True


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["source_exists"] and row["needles_present"] for row in rows_map["sources"])


def lineage_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    text = " ".join(row_value(value) for row in rows_map["lineage"] for value in row.values())
    return all(token in text for token in ["2614", "1765", "954/955/977"])


def noether_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("theorem_id") == "NEC2615_2_weight_collapse"
        and row.get("status") == "DERIVED_CONDITIONAL_THEOREM"
        for row in rows_map["noether"]
    )


def block_law_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("theorem_id") == "NEC2615_3_connected_component_law"
        and row.get("status") == "EXACT_BLOCK_LAW"
        for row in rows_map["noether"]
    )


def theorem_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("theorem_id") == "NEC2615_5_current_verdict"
        and row.get("status") == "PARTIAL_DERIVATION_PARENT_UNSIGNED"
        for row in rows_map["noether"]
    )


def source_owner_unsigned(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("owner_id") == "THO2615_5_owner_verdict"
        and row.get("status") == "CONTRACT_READY_PARENT_UNSIGNED"
        for row in rows_map["source_owner"]
    )


def no_prefactor_partial(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("proof_id") == "NSP2615_4_current_verdict"
        and row.get("status") == "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF"
        for row in rows_map["no_prefactor"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("countermodel_id") == "CM2615_5_verdict"
        and str(row.get("survives_current_constraints", "false")).lower() == "true"
        for row in rows_map["countermodel"]
    )


def deltaw_block_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["deltaw_block"]
    return any(row.get("row_id") == "DWB2615_0_delta_w_block" for row in rows) and all(
        str(row.get("valid_for_claim", "false")).lower() == "false" for row in rows
    )


def ub_power_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("row_id") == "DWB2615_4_R_source_block" and "U_B" in row.get("mathematical_form", "")
        for row in rows_map["deltaw_block"]
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("status_id") == "SZ2615_5_local_GR" and row.get("current_status") == "NOT_CLAIMABLE"
        for row in rows_map["source_zero"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(str(row.get("gate_pass", "false")).lower() == "false" for row in rows_map["claim_gates"])


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("decision_id") == "DEC2615_4_best_next"
        and "EXCHANGE_GRAPH_CONNECTIVITY" in row.get("decision", "")
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("next_id") == "NEXT2615_0_primary"
        and row.get("status") == "selected"
        and "ordinary-matter-exchange-graph" in row.get("doc", "")
        for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2615*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL2615_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present"),
        ("VAL2615_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2614 current gate plus 1765 and 954/955/977 prior inputs"),
        ("VAL2615_02_noether_theorem", noether_theorem_recorded(rows_map), "Noether exchange collapse theorem recorded"),
        ("VAL2615_03_block_law", block_law_recorded(rows_map), "connected-component block law recorded"),
        ("VAL2615_04_not_promoted", theorem_not_promoted(rows_map), "2615 theorem remains parent-unsigned/nonclaim"),
        ("VAL2615_05_source_owner_unsigned", source_owner_unsigned(rows_map), "total Hilbert owner remains contract-ready but unsigned"),
        ("VAL2615_06_no_prefactor_partial", no_prefactor_partial(rows_map), "no-prefactor theorem is partial rather than full parent proof"),
        ("VAL2615_07_countermodel_retained", countermodel_retained(rows_map), "delta_w_block countermodel remains retained"),
        ("VAL2615_08_deltaw_block_nonclaim", deltaw_block_nonclaim(rows_map), "delta_w_block input rows remain nonclaim"),
        ("VAL2615_09_U_B_power_retained", ub_power_retained(rows_map), "explicit U_B block-source residual factor retained"),
        ("VAL2615_10_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked"),
        ("VAL2615_11_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim"),
        ("VAL2615_12_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false"),
        ("VAL2615_13_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        ("VAL2615_14_formalization_untouched", no_formalization_artifacts(), "no 2615 outputs found under formalization-workbench"),
        ("VAL2615_15_decision_next", decision_next(rows_map), "decision selects exchange-graph/source-shadow route"),
        ("VAL2615_16_next_selected", next_selected(rows_map), "next target selected"),
        (
            "VAL2615_17_branch_copies",
            all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"]),
            "nonclaim branch copies exist and parse",
        ),
        ("VAL2615_18_pycache_absent", pycache_absent(), "scripts __pycache__ absent"),
    ]

    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": detail,
                    "detail": "",
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2615_CSV_{path.stem}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"CSV parses with {count} rows" if ok else "CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in COPY_TARGETS.items():
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2615_COPY_CSV_{key}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        with_stamp(
            {
                "check_id": "VAL2615_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "notes": "2615 Noether exchange collapse refines species coupling to exchange-block residual and selects graph/source-shadow proof next",
                "detail": "",
                "valid_for_claim": False,
            }
        )
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        [
            "# 2615 Y5 R2FR Total Hilbert Source Owner And No-Prefactor Clause Or Delta-W Species Bound Input",
            "## Summary\n"
            "- This checkpoint makes a genuine derivation gain on the coupling problem.\n"
            "- Bianchi conservation plus Noether exchange means arbitrary relative species source weights cannot survive across interacting ordinary matter subcurrents.\n"
            "- The surviving residual is sharper: `delta_w_species` refines to `delta_w_block`, a block weight over disconnected conserved exchange components.\n"
            "- A full local-GR/Newton source claim is still blocked by ordinary exchange-graph connectivity, source-shadow exclusion and non-Hilbert current silence.\n"
            "- Next target: prove one connected ordinary matter exchange graph with no source-shadow functional, or source finite `delta_w_block` bounds.",
            "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "source_key", "source_path", "source_exists", "needles_present"]),
            "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "imported_result", "2615_use"]),
            "## Noether Exchange Collapse Theorem\n" + markdown_table(rows_map["noether"], ["theorem_id", "claim_piece", "mathematical_form", "status", "derivation_result", "parent_signed", "remaining_gap"]),
            "## Total Hilbert Source Owner Audit\n" + markdown_table(rows_map["source_owner"], ["owner_id", "claim_piece", "mathematical_form", "why_it_matters", "status", "remaining_gap"]),
            "## No-Source-Prefactor Proof Attempt\n" + markdown_table(rows_map["no_prefactor"], ["proof_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
            "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "needed_to_kill"]),
            "## Delta-W Block Bound Input\n" + markdown_table(rows_map["deltaw_block"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "needed_input", "status"]),
            "## Source Zero Status\n" + markdown_table(rows_map["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
            "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
            "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
            "## Next Target\n" + markdown_table(rows_map["next"], ["next_id", "status", "doc", "script", "task", "success_condition", "guardrail"]),
            "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
            "## Validation\n" + markdown_table(validations, ["check_id", "status", "notes", "detail", "valid_for_claim"]),
            "## Working Verdict\n"
            "This is better than merely saying the coupling is missing. Arbitrary species weights are now too crude: Bianchi plus Noether exchange collapses them to exchange-block weights. The remaining loopholes are sharply named: a source-shadow functional, a label-carrying non-Hilbert current, or genuinely disconnected conserved source blocks. That is the next battlefield for deriving the GR/Newton source side.",
        ]
    ) + "\n"


def main() -> None:
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["noether_collapse"], rows_map["noether"])
    write_csv(OUTPUTS["source_owner"], rows_map["source_owner"])
    write_csv(OUTPUTS["no_prefactor"], rows_map["no_prefactor"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["deltaw_block"], rows_map["deltaw_block"])
    write_csv(OUTPUTS["source_zero"], rows_map["source_zero"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"2615 validation {validations[-1]['status']}")


if __name__ == "__main__":
    main()
