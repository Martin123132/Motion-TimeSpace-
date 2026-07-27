from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1763"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1763_0_1762_handoff",
        "source_key": "1762_generator_next",
        "source_path": ROOT / "1762-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md",
        "needles": ["NEXT1762_0_primary", "INVARIANT_GENERATOR_ELIMINATION_IS_NEXT_BEST_DERIVATION_ROUTE"],
    },
    {
        "source_id": "SRC1763_1_1762_invariant",
        "source_key": "1762_invariant_hom_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_INVARIANT_ALGEBRA_HOM_AUDIT.csv",
        "needles": ["IH1762_5_species_constants", "FAIL_CURRENT_CLAIM_GENERATOR_DEBTS_RETAINED"],
    },
    {
        "source_id": "SRC1763_2_1762_deltaw",
        "source_key": "1762_deltaw_bound_interface",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
        "needles": ["DW1762_2_delta_w_species", "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND"],
    },
    {
        "source_id": "SRC1763_3_1762_source_functor",
        "source_key": "1762_label_forgetting_source_functor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv",
        "needles": ["SF1762_0_label_forgetting", "FAIL_CURRENT_CLAIM_SOURCE_FUNCTOR_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1763_4_573_debt",
        "source_key": "573_invariant_generator_debt",
        "source_path": RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
        "needles": ["IG573_4_species_constants", "not_universalized"],
    },
    {
        "source_id": "SRC1763_5_1758_invariant",
        "source_key": "1758_invariant_algebra_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_INVARIANT_ALGEBRA_AUDIT.csv",
        "needles": ["IA1758_5_species_constants", "MISSING_CONSTANT_SOURCE_UNIVERSALITY"],
    },
    {
        "source_id": "SRC1763_6_953_doc",
        "source_key": "953_source_functor_doc",
        "source_path": ROOT / "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md",
        "needles": ["The good news", "The bad news"],
    },
    {
        "source_id": "SRC1763_7_953_theorem",
        "source_key": "953_source_functor_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["NSF953_1_domain_fork", "conditional_proof_not_parent_derivation"],
    },
    {
        "source_id": "SRC1763_8_953_contract",
        "source_key": "953_parent_category_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
        "needles": ["PMC953_1_label_forgetting_quotient", "PMC953_5_contract_verdict"],
    },
    {
        "source_id": "SRC1763_9_954_clause",
        "source_key": "954_parent_action_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
    },
    {
        "source_id": "SRC1763_10_955_minimal",
        "source_key": "955_minimal_matter_action",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_3_relative_prefactor", "MMA955_6_verdict"],
    },
    {
        "source_id": "SRC1763_11_977_constant",
        "source_key": "977_constant_source_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_1_theta_representation_data", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1763_12_1488_wA",
        "source_key": "1488_wA_deltaW_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
        "needles": ["WA1488_2_species_label_slot", "RETAINED_RESIDUAL_SYMBOLIC"],
    },
    {
        "source_id": "SRC1763_13_736_no_marker",
        "source_key": "736_no_marker_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv",
        "needles": ["NMC736_5_limit", "NMC736_3_shadow_frame_forbidden"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_SOURCE_REGISTER.csv",
    "generator_priority": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_INVARIANT_GENERATOR_PRIORITY.csv",
    "species_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_SPECIES_LABEL_ZERO_ATTEMPT.csv",
    "deltaw_acquisition": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_DELTAW_SOURCE_ACQUISITION_LEDGER.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1763_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "invariant generator elimination priority or delta_w source acquisition",
                "valid_for_claim": False,
            }
        )
    return rows


def generator_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 1,
            "generator": "species_charge_constants/source labels",
            "delta_w_channel": "delta_w_species",
            "zero_route": "parent label-forgetting source functor plus fixed representation-data constants",
            "why_this_rank": "directly targets the relative source-prefactor countermodel and has the cleanest existing conditional theorem",
            "scrutiny_level": "LOWEST_RELATIVE_SCRUTINY",
            "current_status": "BEST_NEXT_ZERO_ROUTE_UNSIGNED",
            "next_action": "attempt species label-forgetting proof; otherwise source delta_w_species bound",
            "selected": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 2,
            "generator": "post_readout_projector",
            "delta_w_channel": "delta_w_readout",
            "zero_route": "variation-before-readout theorem and before-readout source/worldtube owner",
            "why_this_rank": "dangerous because it can fake closure after solving, but less clean than source-label forgetting",
            "scrutiny_level": "HIGH",
            "current_status": "NO_CHEAT_RULE_ONLY",
            "next_action": "hold until species route or source-owner route is sharper",
            "selected": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 3,
            "generator": "relative_boundary_domain_class",
            "delta_w_channel": "delta_w_marker/delta_w_readout",
            "zero_route": "local trivial class or class-only stress-free no-hair theorem",
            "why_this_rank": "can source boundary/domain charge but needs harder topology/boundary arguments",
            "scrutiny_level": "HIGH",
            "current_status": "NOT_DERIVED",
            "next_action": "defer unless species/source route fails and boundary tail dominates",
            "selected": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 4,
            "generator": "finite_cell_fibre_spectrum",
            "delta_w_channel": "delta_w_hidden/delta_w_species",
            "zero_route": "prove fibre basis is gauge/relabeling only or universal constant",
            "why_this_rank": "could be important but object inventory is more abstract and harder to sell",
            "scrutiny_level": "HIGH",
            "current_status": "NOT_TRIVIALIZED",
            "next_action": "defer to invariant-algebra theorem or coefficient row",
            "selected": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 5,
            "generator": "chi_D/domain_selector",
            "delta_w_channel": "delta_w_hidden/source-normalization coefficient",
            "zero_route": "selector as gauge/readout-only or fixed local trivial branch",
            "why_this_rank": "already entangled with double-zero/cosmology/local selector machinery; attacking it here risks mixing branches",
            "scrutiny_level": "VERY_HIGH",
            "current_status": "NOT_DERIVED",
            "next_action": "keep separate from matter-source label proof",
            "selected": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": 6,
            "generator": "memory_or_class_scalar",
            "delta_w_channel": "delta_w_hidden/A_mu_even",
            "zero_route": "local value and gradient zero theorem or explicit bounded residual",
            "why_this_rank": "broad and physically meaningful but less directly tied to ordinary matter source prefactors",
            "scrutiny_level": "VERY_HIGH",
            "current_status": "NOT_SILENCED_AS_THEOREM",
            "next_action": "defer to memory/local-gradient branch",
            "selected": False,
            "valid_for_claim": False,
        },
    ]


def species_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SLZ1763_0_target",
            "claim_piece": "species-label source-prefactor zero",
            "mathematical_form": "delta_w_species=0 iff species labels are not source-functor arguments before coupling selection",
            "attempt_status": "TARGET_EXACT",
            "proof_result": "ZERO_IF_LABEL_FORGETTING_PARENT_SIGNED",
            "gap": "parent source category label-forgetting is exact but not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SLZ1763_1_conditional_uniqueness",
            "claim_piece": "unique covariant additive source map after labels forgotten",
            "mathematical_form": "q_src({(T_A,A)})=T_total and F_src(T_total)=kappa_univ T_total",
            "attempt_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_result": "relative source weights cannot be written after q_src forgets A",
            "gap": "source functor domain is a contract, not a parent-action theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SLZ1763_2_representation_constants",
            "claim_piece": "constants are representation/superselection data",
            "mathematical_form": "theta_A in Rep_A and Lie_v theta_A=0, not theta_A(X,I_Q,m,h)",
            "attempt_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "proof_result": "would block direct constant/clock/mass source labels if parent-signed",
            "gap": "MTS action on constants and no direct constant vertices remain policy/contract rather than theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SLZ1763_3_countermodel",
            "claim_piece": "species-labelled additive source functor",
            "mathematical_form": "F_src({(T_A,A)})=sum_A kappa_A T_A",
            "attempt_status": "COUNTERMODEL_SURVIVES_IF_LABELS_REMAIN",
            "proof_result": "covariant/additive/Ward-compatible when A labels are source-domain data",
            "gap": "Ward conservation cannot kill species-labelled source weights",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SLZ1763_4_current_verdict",
            "claim_piece": "delta_w_species=0 for current MTS",
            "mathematical_form": "SLZ1763_0 through SLZ1763_2 parent-signed and SLZ1763_3 excluded",
            "attempt_status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_result": "DELTA_W_SPECIES_RETAINED",
            "gap": "label-forgetting quotient and constant/source parent certificate are not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaw_acquisition_rows() -> list[dict[str, Any]]:
    source_path = str(RESIDUALS / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv")
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA1763_0_delta_w_species",
            "quantity": "delta_w_species",
            "priority_rank": 1,
            "required_zero_or_bound": "label-forgetting source functor theorem or numeric bound on species-labelled source prefactor",
            "status": "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA1763_1_delta_w_readout",
            "quantity": "delta_w_readout",
            "priority_rank": 2,
            "required_zero_or_bound": "variation-before-readout/source-worldtube owner theorem or bound on readout source-mask transfer",
            "status": "MISSING_READOUT_TRANSFER_ZERO_OR_BOUND",
            "units": "dimensionless",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA1763_2_delta_w_marker",
            "quantity": "delta_w_marker",
            "priority_rank": 3,
            "required_zero_or_bound": "no-marker quotient-extension theorem or material/domain marker coefficient bound",
            "status": "MISSING_NO_MARKER_THEOREM_OR_BOUND",
            "units": "dimensionless",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA1763_3_delta_w_hidden",
            "quantity": "delta_w_hidden",
            "priority_rank": 4,
            "required_zero_or_bound": "fibre/chi/memory invariant zero theorem or hidden source coefficient bound",
            "status": "MISSING_HIDDEN_INVARIANT_ZERO_OR_BOUND",
            "units": "dimensionless",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA1763_4_A_direct_response",
            "quantity": "A_direct_matter",
            "priority_rank": 5,
            "required_zero_or_bound": "operator K_w and E* norm mapping delta_w vector into ||delta_v V_m||",
            "status": "MISSING_K_W_OPERATOR_NORM_DELTAW_NORM_OR_THEOREM_ZERO",
            "units": "E*_dual_or_declared_arena_units",
            "source_path": source_path,
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1763_0_priority",
            "quantity": "generator priority",
            "current_status": "SPECIES_LABEL_ROUTE_SELECTED",
            "evidence": "species labels directly source delta_w_species and have the cleanest conditional source-functor theorem",
            "remaining_gap": "source-domain label forgetting remains unsigned",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1763_1_species",
            "quantity": "delta_w_species",
            "current_status": "NOT_ZEROED",
            "evidence": "species-labelled additive source functor countermodel survives if labels remain",
            "remaining_gap": "parent proof that q_src forgets labels before F_src",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1763_2_delta_w",
            "quantity": "delta_w_A",
            "current_status": "RETAINED_NONCLAIM",
            "evidence": "1763 only ranks and selects the first generator; it does not zero the vector",
            "remaining_gap": "species/readout/marker/hidden components remain unsourced or unproved",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1763_3_local_GR",
            "quantity": "GR/Newton source side",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "relative source prefactor branch remains nonclaim",
            "remaining_gap": "source side, hidden-source envelope and source-to-Poisson/orbital calibration gates remain open",
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1763_0_ranking",
            "decision": "SPECIES_LABEL_ROUTE_IS_BEST_NEXT_ZERO_TARGET",
            "reason": "it directly targets delta_w_species and has the strongest conditional source-functor theorem already written",
            "next_action": "attack source-domain label forgetting before harder fibre/domain/chi/memory/readout debts",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1763_1_no_claim",
            "decision": "DELTA_W_SPECIES_NOT_ZEROED",
            "reason": "species-labelled additive source functor remains legal unless the parent source category forgets labels",
            "next_action": "retain delta_w_species as nonclaim residual",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1763_2_data",
            "decision": "NO_NUMERIC_DELTAW_ROWS_FILLED",
            "reason": "no component basis, numeric bound, units, or source-backed coefficient exists yet",
            "next_action": "do not score WEP/R10/PPN from placeholders",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1763_3_best_next",
            "decision": "SPECIES_LABEL_FORGETTING_PARENT_PROOF_IS_NEXT",
            "reason": "the least-scrutiny route is to prove q_src forgets species labels before the source functor is formed",
            "next_action": "build 1764 species-label forgetting source-functor parent proof or delta_w_species bound",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1763_0_species_label",
            "claim": "species labels are absent from parent source-functor domain",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_LABEL_FORGETTING_QUOTIENT_UNSIGNED",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1763_1_delta_w_species_zero",
            "claim": "delta_w_species=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SPECIES_LABEL_COUNTERMODEL_SURVIVES",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1763_2_delta_w_species_bound",
            "claim": "delta_w_species is finite and source-backed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NUMERIC_BOUND_COMPONENT_BASIS_SOURCE_PATH_MISSING",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1763_3_delta_w_vector",
            "claim": "delta_w_A vector is zero or fully source-backed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_OTHER_GENERATOR_COMPONENTS_REMAIN",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1763_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTAW_AND_SOURCE_SIDE_GATES_NOT_CLOSED",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1763_0_primary",
            "next_target": "1764-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
            "script": "scripts/Y5_R2FR_species_label_forgetting_source_functor_parent_proof_or_deltaw_species_bound.py",
            "objective": "try to prove q_src forgets species labels before source coupling selection; if not, stage source-ready delta_w_species bound rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1763_1_fallback",
            "next_target": "1764b-Y5-R2FR-deltaw-species-bound-source-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_species_bound_source_pack.py",
            "objective": "build nonclaim source-acquisition rows for delta_w_species with component basis, units, target bounds and provenance",
            "selection_status": "held_fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "generator_priority": generator_priority_rows(),
        "species_attempt": species_attempt_rows(),
        "deltaw_acquisition": deltaw_acquisition_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return bool(list(csv.DictReader(handle)))
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1763_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1763_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
        "selected",
    }


def boolish_claim_true(key: str, value: Any) -> bool:
    if key.lower() == "selected":
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_claim_true(key, value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "attempt_status", "proof_result"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1763_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1763_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1763() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1763*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def species_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["generator"] == "species_charge_constants/source labels"
        and row["priority_rank"] == 1
        and row["selected"] is True
        for row in rows_map["generator_priority"]
    )


def species_attempt_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "SLZ1763_4_current_verdict"
        and row["proof_result"] == "DELTA_W_SPECIES_RETAINED"
        and row["valid_for_claim"] is False
        for row in rows_map["species_attempt"]
    )


def acquisition_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["deltaw_acquisition"]
    return any(row["quantity"] == "delta_w_species" and row["valid_for_claim"] is False for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1763_3_local_GR"
        and row["current_status"] == "NOT_CLAIMABLE"
        and row["claim_allowed"] is False
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1763_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1763_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1763_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1763_2_species_selected", species_selected(rows_map), "species-label generator selected as best next zero route", "species-label generator not selected"),
        check_row("VAL1763_3_species_not_promoted", species_attempt_not_promoted(rows_map), "species-label zero attempt remains unpromoted", "species-label zero attempt promoted or verdict missing"),
        check_row("VAL1763_4_acquisition_nonclaim", acquisition_nonclaim(rows_map), "delta_w acquisition rows remain nonclaim", "delta_w acquisition rows missing or promoted"),
        check_row("VAL1763_5_source_zero_blocked", source_zero_blocked(rows_map), "source/local-GR status remains blocked", "source/local-GR status missing or promoted"),
        check_row("VAL1763_6_claim_gates_safe", all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates), "all claim gates remain blocked", "one or more claim gates opened"),
        check_row("VAL1763_7_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1763_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1763_9_decision_next",
            any(row["decision_id"] == "DEC1763_3_best_next" and row["decision"] == "SPECIES_LABEL_FORGETTING_PARENT_PROOF_IS_NEXT" for row in rows_map["decision"]),
            "decision selects species-label forgetting route",
            "best-next decision missing",
        ),
        check_row("VAL1763_10_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1763_11_csv_parse", csv_parse_all(), "all generated 1763 CSVs parse", "one or more generated 1763 CSVs fail to parse"),
        check_row("VAL1763_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1763_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1763_14_formalization_untouched", formalization_untouched_for_1763(), "no 1763 outputs found under formalization-workbench", "1763 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1763_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1763 invariant generator priority or delta_w source acquisition",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1763 - Invariant Generator Elimination Priority Or Delta_w Source Acquisition",
        "",
        "## Verdict",
        "- 1763 ranks the live no-Hom generator debts instead of treating them as one fog bank.",
        "- The best next derivation target is `species_charge_constants/source labels`: it directly sources `delta_w_species` and already has the cleanest conditional theorem through source-domain label forgetting.",
        "- The attempted zero proof is still not a claim. If species labels remain source-functor arguments, `F_src({(T_A,A)})=sum_A kappa_A T_A` remains covariant, additive and Ward-compatible.",
        "- Therefore `delta_w_species` is retained as a nonclaim residual, and no numeric `delta_w` rows are filled from placeholders.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Generator Priority",
        markdown_table(rows_map["generator_priority"], ["priority_rank", "generator", "delta_w_channel", "zero_route", "why_this_rank", "scrutiny_level", "current_status", "selected"]),
        "",
        "## Species Label Zero Attempt",
        markdown_table(rows_map["species_attempt"], ["attempt_id", "claim_piece", "mathematical_form", "attempt_status", "proof_result", "gap"]),
        "",
        "## Delta-w Source Acquisition Ledger",
        markdown_table(rows_map["deltaw_acquisition"], ["row_id", "quantity", "priority_rank", "required_zero_or_bound", "status", "units"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is a tactical checkpoint. The shortest clean route through the source-coupling wall is not fibre topology or memory yet; it is proving that the parent source functor forgets species labels before coupling selection. If that closes, the worst relative source-prefactor channel dies cleanly. If it does not, `delta_w_species` becomes the first finite source-weight component to bound.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1763-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-acquisition.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1763 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
