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

BRANCH_ID = "MTS_R2FR_SPECIES_FORGETTING_GATE_2614"
CHECKPOINT_ID = "2614"

DOC = ROOT / "2614-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_LINEAGE_LEDGER.csv",
    "label_forgetting": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "source_domain": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_SOURCE_DOMAIN_FORK_AUDIT.csv",
    "parent_signature": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_PARENT_SIGNATURE_REQUIREMENTS.csv",
    "countermodel": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_COUNTERMODEL_LEDGER.csv",
    "deltaw_species": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_DELTAW_SPECIES_BOUND_INTERFACE.csv",
    "source_zero": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2614_VALIDATION.csv",
}

COPY_TARGETS = {
    "label_forgetting": LOCAL_BOUNDS / "Species_label_forgetting_proof_attempt_2614_NONCLAIM.csv",
    "deltaw_species": LOCAL_BOUNDS / "Deltaw_species_bound_interface_2614_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Species_forgetting_source_zero_status_2614_NONCLAIM.csv",
    "next_target": QUEUE / "JR2614_TOTAL_HILBERT_SOURCE_OWNER_NEXT.csv",
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
            "source_id": "SRC2614_00_2613_handoff_doc",
            "source_key": "2613_species_forgetting_selected",
            "source_path": ROOT / "2613-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md",
            "needles": ["NEXT2613_0_primary", "SPECIES_LABEL_FORGETTING_IS_NEXT_BEST_DERIVATION_ROUTE", "VAL2613_OVERALL"],
            "role": "current 26xx handoff selecting species-label forgetting route",
        },
        {
            "source_id": "SRC2614_01_2613_source_functor",
            "source_key": "2613_source_functor_unsigned",
            "source_path": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv",
            "needles": ["SF2613_0_label_forgetting", "SF2613_4_verdict", "FAIL_CURRENT_CLAIM_SOURCE_FUNCTOR_PARENT_UNSIGNED"],
            "role": "current source-functor parent unsigned status",
        },
        {
            "source_id": "SRC2614_02_2613_deltaw",
            "source_key": "2613_delta_w_species_interface",
            "source_path": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_DELTAW_BOUND_INTERFACE.csv",
            "needles": ["DW2613_2_delta_w_species", "DW2613_7_R_source_direct"],
            "role": "current delta_w species and source residual interface",
        },
        {
            "source_id": "SRC2614_03_1764_doc",
            "source_key": "1764_prior_species_forgetting_doc",
            "source_path": ROOT / "1764-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
            "needles": ["SDF1764_0_unlabelled_domain", "DEC1764_3_best_next", "VAL1764_OVERALL"],
            "role": "prior species-forgetting checkpoint used as lineage evidence",
        },
        {
            "source_id": "SRC2614_04_1764_label_attempt",
            "source_key": "1764_label_forgetting_attempt",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1764_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
            "needles": ["LF1764_0_target", "LF1764_5_current_verdict", "DELTA_W_SPECIES_RETAINED"],
            "role": "prior exact conditional theorem and unsigned verdict",
        },
        {
            "source_id": "SRC2614_05_1764_countermodel",
            "source_key": "1764_countermodel_ledger",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1764_COUNTERMODEL_LEDGER.csv",
            "needles": ["CM1764_1_weighted_action_before_variation", "CM1764_5_verdict"],
            "role": "labelled and weighted source countermodels that survive current constraints",
        },
        {
            "source_id": "SRC2614_06_1764_deltaw_species",
            "source_key": "1764_delta_w_species_interface",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv",
            "needles": ["DWS1764_0_delta_w_species", "DWS1764_4_nonclaim_lock"],
            "role": "prior nonclaim species bound interface",
        },
        {
            "source_id": "SRC2614_07_953_theorem",
            "source_key": "953_source_functor_theorem",
            "source_path": OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needles": ["NSF953_1_domain_fork", "NSF953_5_verdict"],
            "role": "older no-species source-functor theorem attempt",
        },
        {
            "source_id": "SRC2614_08_954_action_clause",
            "source_key": "954_parent_action_clause",
            "source_path": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
            "role": "parent action clauses that would close the source-domain fork",
        },
        {
            "source_id": "SRC2614_09_955_minimal_matter",
            "source_key": "955_minimal_matter_lemma",
            "source_path": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "needles": ["MMA955_3_relative_prefactor", "MMA955_6_verdict"],
            "role": "minimal matter action lemma and relative-prefactor obstruction",
        },
        {
            "source_id": "SRC2614_10_977_constant_certificate",
            "source_key": "977_constant_source_certificate",
            "source_path": OUT / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
            "needles": ["CSC977_1_theta_representation_data", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
            "role": "constant/source certificate and unsigned relative-coupling status",
        },
        {
            "source_id": "SRC2614_11_1488_residual_lock",
            "source_key": "1488_wA_deltaW_lock",
            "source_path": OUT / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
            "needles": ["WA1488_2_species_label_slot", "RETAINED_RESIDUAL_SYMBOLIC"],
            "role": "older residual lock retaining w_A/delta_w symbolic branch",
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
            "lineage_id": "LIN2614_0_current_parent",
            "input_checkpoint": "2613",
            "input_artifact": "P8_Y5_HOM_EXCLUSION_GATE_2613_*",
            "imported_result": "Hom exclusion still depends on parent source functor forgetting species labels",
            "2614_use": "attack delta_w_species rather than the whole delta_w vector",
        },
        {
            "lineage_id": "LIN2614_1_prior_species_gate",
            "input_checkpoint": "1764",
            "input_artifact": "P8_Y5_PARENT_QLOC_1764_*",
            "imported_result": "label-forgotten source domain is clean, labelled/weighted domains remain countermodels",
            "2614_use": "port the result into the 26xx local-GR derivability chain",
        },
        {
            "lineage_id": "LIN2614_2_parent_action_clause",
            "input_checkpoint": "954/955/977",
            "input_artifact": "parent action, minimal matter, constant-source certificates",
            "imported_result": "the pressure point is no source-only species prefactors plus total Hilbert source ownership",
            "2614_use": "define the exact signature contract for 2615",
        },
        {
            "lineage_id": "LIN2614_3_bound_interface",
            "input_checkpoint": "1764/2613",
            "input_artifact": "delta_w_species nonclaim rows",
            "imported_result": "if proof stalls, species leakage must become finite sourced coefficients",
            "2614_use": "retain nonclaim bound rows with missing basis/projection/source markers",
        },
        {
            "lineage_id": "LIN2614_4_claim_policy",
            "input_checkpoint": "all",
            "input_artifact": "claim gates and source-zero ledgers",
            "imported_result": "no local-GR, WEP, PPN, clock, orbital or R10 claim while species source branch is live",
            "2614_use": "keep all claim flags false",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def label_forgetting_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "LF2614_0_target",
            "claim_piece": "parent source functor forgets species labels before coupling selection",
            "mathematical_form": "q_src({(T_A,A)})=T_total=sum_A T_A",
            "attempt_status": "TARGET_EXACT",
            "proof_result": "would remove species as an argument of F_src",
            "gap": "parent source-domain quotient is not signed",
        },
        {
            "attempt_id": "LF2614_1_conditional_theorem",
            "claim_piece": "label-forgotten source functor has one coupling",
            "mathematical_form": "S_matter=sum_A S_A; T_total=delta S_matter/delta e_obs; F_src(T_total)=kappa_univ T_total",
            "attempt_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_result": "if no w_A slot and no hidden source spurion exists, relative kappa_A/kappa_B cannot be written",
            "gap": "no-source-prefactor and no-spurion clauses remain unsigned parent premises",
        },
        {
            "attempt_id": "LF2614_2_variation_order",
            "claim_piece": "variation-before-decomposition mechanism",
            "mathematical_form": "delta(S_1+...+S_N)/delta e_obs = sum_A delta S_A/delta e_obs, with source object T_total formed before labels are exposed",
            "attempt_status": "DERIVED_WITHIN_CONTRACT",
            "proof_result": "bookkeeping labels disappear if active source owner is the total Hilbert/coframe derivative",
            "gap": "parent action must declare total Hilbert derivative as the only ordinary active-source owner",
        },
        {
            "attempt_id": "LF2614_3_needed_signatures",
            "claim_piece": "minimal parent signature for species zero",
            "mathematical_form": "single S_matter + no source-only w_A + total Hilbert derivative owner + fixed representation data + no hidden post-variation source spurion",
            "attempt_status": "CONTRACT_LIST_SHARP",
            "proof_result": "these clauses would make delta_w_species=0 structural rather than fitted",
            "gap": "no-source-prefactor and total-source-owner clauses are not yet parent-proved in the current chain",
        },
        {
            "attempt_id": "LF2614_4_normalization_owner",
            "claim_piece": "nongravitational constants are representation data, not source charges",
            "mathematical_form": "theta_A belongs to Rep_A/matter sector normalization; kappa_univ is calibrated once by measured G",
            "attempt_status": "CONDITIONAL_SUPPORT",
            "proof_result": "prevents using masses, charges, or material constants as independent gravitational source weights",
            "gap": "constant/source certificate is relative and parent unsigned",
        },
        {
            "attempt_id": "LF2614_5_current_verdict",
            "claim_piece": "delta_w_species=0 for current MTS local branch",
            "mathematical_form": "delta_w_species=0",
            "attempt_status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_result": "DELTA_W_SPECIES_RETAINED",
            "gap": "no-source-prefactor clause, total Hilbert owner and source-label quotient still need parent proof or sourced finite bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_domain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "SDF2614_0_unlabelled_domain",
            "domain_choice": "label-forgotten total Hilbert current",
            "mathematical_form": "Obj(Source)=T_total, not {(T_A,A)}",
            "consequence": "F_src has no species argument and can only carry one calibrated common scalar",
            "status": "CLEAN_ZERO_ROUTE_IF_PARENT_SIGNED",
            "gap": "parent category/source owner not signed",
        },
        {
            "audit_id": "SDF2614_1_total_hilbert_owner",
            "domain_choice": "source extracted by total variation of one matter functional",
            "mathematical_form": "T_total := delta S_matter[Psi,e_obs,theta]/delta e_obs",
            "consequence": "species decomposition becomes bookkeeping after source extraction",
            "status": "CONDITIONAL_MECHANISM_VALID",
            "gap": "must prove total Hilbert derivative is the only ordinary active-source owner",
        },
        {
            "audit_id": "SDF2614_2_labelled_domain",
            "domain_choice": "labelled species current family",
            "mathematical_form": "Obj(Source)={(T_A,A)} and F_src({(T_A,A)})=sum_A kappa_A T_A",
            "consequence": "relative species couplings remain covariant, additive and Ward-compatible",
            "status": "COUNTERDOMAIN_OPEN",
            "gap": "must exclude labels before source functor formation",
        },
        {
            "audit_id": "SDF2614_3_weighted_action_domain",
            "domain_choice": "weighted matter action before variation",
            "mathematical_form": "S_matter=sum_A w_A S_A gives T_source=sum_A w_A T_A",
            "consequence": "source quotient is not enough unless w_A slots are absent",
            "status": "PREFACTOR_OBSTRUCTION_OPEN",
            "gap": "no-source-prefactors clause is unsigned",
        },
        {
            "audit_id": "SDF2614_4_minimal_normalization_clause",
            "domain_choice": "nongravitational normalization fixes matter constants and forbids source-only weights",
            "mathematical_form": "theta_A fixed by Rep_A and experiments; w_A source-only slot is not an allowed parent coordinate",
            "consequence": "relative weights become forbidden double counting rather than physical couplings",
            "status": "BEST_NEXT_PARENT_CLAUSE",
            "gap": "needs explicit parent object-language/action signature",
        },
        {
            "audit_id": "SDF2614_5_fork_verdict",
            "domain_choice": "source-domain fork",
            "mathematical_form": "unlabelled source domain closes delta_w_species; labelled or weighted domain keeps it alive",
            "consequence": "next derivation must sign no-source-prefactor/total-Hilbert-source ownership",
            "status": "FORK_NOT_RESOLVED",
            "gap": "no current local-GR/WEP/R10 claim",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def parent_signature_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "signature_id": "PS2614_0_single_matter_functional",
            "required_clause": "one ordinary matter functional",
            "contract": "S_matter[Psi,e_obs,theta]=sum_A S_A[Psi_A,e_obs,theta_A] with no additional source-selector layer",
            "status": "NEEDED_NOT_PARENT_SIGNED",
            "would_close": "prevents post-hoc construction of a labelled source object",
            "if_missing": "species-decomposed source family can be chosen as primitive",
        },
        {
            "signature_id": "PS2614_1_no_source_prefactors",
            "required_clause": "no source-only species weights",
            "contract": "there is no allowed parent coordinate w_A multiplying S_A only for gravitational sourcing",
            "status": "HIGHEST_PRESSURE_UNSIGNED_CLAUSE",
            "would_close": "kills S_matter=sum_A w_A S_A countermodel",
            "if_missing": "delta_w_species remains covariant and Ward-compatible",
        },
        {
            "signature_id": "PS2614_2_total_Hilbert_owner",
            "required_clause": "ordinary active source is total Hilbert/coframe derivative",
            "contract": "T_active,ordinary := delta S_matter/delta e_obs before source coupling selection",
            "status": "NEEDED_NOT_PARENT_SIGNED",
            "would_close": "source functor receives T_total instead of labelled family",
            "if_missing": "F_src({(T_A,A)}) remains legal",
        },
        {
            "signature_id": "PS2614_3_fixed_representation_data",
            "required_clause": "matter constants are representation/nongravitational data",
            "contract": "theta_A is fixed inside Rep_A and cannot be re-used as an active gravitational source prefactor",
            "status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "would_close": "prevents mass/charge/material constants leaking into kappa_A",
            "if_missing": "constant-source leakage can mimic species charge",
        },
        {
            "signature_id": "PS2614_4_no_hidden_source_spurion",
            "required_clause": "no hidden post-variation species/material spurion",
            "contract": "T_active cannot be T_total + sum_A sigma_A P_A(T_A) after variation",
            "status": "NEEDED_NOT_PARENT_SIGNED",
            "would_close": "prevents source labels returning under projector/readout names",
            "if_missing": "hidden source projector countermodel survives",
        },
        {
            "signature_id": "PS2614_5_verdict",
            "required_clause": "parent signature sufficient for delta_w_species=0",
            "contract": "PS2614_0 through PS2614_4 all hold in one parent action",
            "status": "SIGNATURE_CONTRACT_READY_PARENT_UNSIGNED",
            "would_close": "Z_delta_w_species=true",
            "if_missing": "carry delta_w_species as explicit nonclaim residual",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "countermodel_id": "CM2614_0_labelled_additive_source_functor",
            "countermodel": "species labels remain source-functor arguments",
            "mathematical_form": "F_src({(T_A,A)})=sum_A kappa_A T_A",
            "survives_current_constraints": True,
            "why_survives": "covariance, additivity and Ward conservation do not force kappa_A=kappa_B",
            "needed_to_kill": "parent proof that q_src forgets A before F_src is formed",
        },
        {
            "countermodel_id": "CM2614_1_weighted_action_before_variation",
            "countermodel": "relative source-only weights multiply species actions",
            "mathematical_form": "S_matter=sum_A w_A S_A",
            "survives_current_constraints": True,
            "why_survives": "constant w_A can preserve diffeomorphism covariance and species Ward identities",
            "needed_to_kill": "no-source-prefactor parent clause plus nongravitational normalization owner",
        },
        {
            "countermodel_id": "CM2614_2_hidden_spurion_return",
            "countermodel": "material marker returns after variation",
            "mathematical_form": "T_active=T_total + sum_A sigma_A P_A(T_A)",
            "survives_current_constraints": True,
            "why_survives": "hidden source projector can reintroduce material labels unless object language forbids it",
            "needed_to_kill": "no hidden source-spurion/post-readout-source clause",
        },
        {
            "countermodel_id": "CM2614_3_nonHilbert_current_split",
            "countermodel": "non-Hilbert spin/torsion/boundary current carries species labels",
            "mathematical_form": "T_active=T_Hilbert + J_nonHilbert[A]",
            "survives_current_constraints": True,
            "why_survives": "Hilbert-current uniqueness does not silence extra parent currents by itself",
            "needed_to_kill": "explicit absence/silence theorem for non-Hilbert ordinary source currents",
        },
        {
            "countermodel_id": "CM2614_4_representation_constant_leakage",
            "countermodel": "matter constants depend on MTS invariant or material marker",
            "mathematical_form": "theta_A=theta_A(X,I_Q,m,h) or kappa_A=kappa(theta_A)",
            "survives_current_constraints": True,
            "why_survives": "constant-source certificate is relative and parent unsigned",
            "needed_to_kill": "fixed representation-data theorem for theta_A and one global kappa",
        },
        {
            "countermodel_id": "CM2614_5_verdict",
            "countermodel": "species source-prefactor leakage",
            "mathematical_form": "not(parent_forgets_A and no w_A and no hidden source spurion) => delta_w_species retained",
            "survives_current_constraints": True,
            "why_survives": "current parent action has contract gaps exactly where countermodels enter",
            "needed_to_kill": "2615 no-source-prefactor/total-Hilbert-owner proof or finite sourced bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def deltaw_species_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DWS2614_0_delta_w_species",
            "quantity": "delta_w_species",
            "meaning": "species-label leakage into active ordinary source prefactor",
            "mathematical_form": "T_active=sum_A (1+delta_w_A) T_A; delta_w_species is the label-dependent component",
            "units": "dimensionless",
            "status": "MISSING_PARENT_NO_PREFACTOR_OR_NUMERIC_BOUND",
        },
        {
            "row_id": "DWS2614_1_component_basis",
            "quantity": "species/component basis",
            "meaning": "which ordinary matter components carry independent source-weight residuals",
            "mathematical_form": "A in {electron, proton, neutron, nuclear binding, EM binding, ...} or a parent-derived smaller basis",
            "units": "labels",
            "status": "MISSING_COMPONENT_BASIS",
        },
        {
            "row_id": "DWS2614_2_test_body_projection",
            "quantity": "composition projection",
            "meaning": "map from delta_w_species to measured differential acceleration/source charge",
            "mathematical_form": "eta_AB ~ sum_i (f_i^A-f_i^B) delta_w_i",
            "units": "dimensionless",
            "status": "MISSING_ARENA_PROJECTION",
        },
        {
            "row_id": "DWS2614_3_bound_source",
            "quantity": "delta_w_species_bound",
            "meaning": "finite empirical upper bound if proof fails",
            "mathematical_form": "|delta_w_i-delta_w_j| <= bound_from_WEP_R10_PPN_clock_or_orbital_projection",
            "units": "dimensionless",
            "status": "MISSING_SOURCE_BACKED_BOUND_TABLE",
        },
        {
            "row_id": "DWS2614_4_R_source_species",
            "quantity": "R_source_species",
            "meaning": "species-prefactor contribution to ordinary active-source residual",
            "mathematical_form": "||R_source,species||_{E*} <= U_B K_species ||delta_w_species||",
            "units": "E*_dual_or_declared_arena_units",
            "status": "MISSING_K_SPECIES_OPERATOR_NORM_AND_ARENA_UNITS",
        },
        {
            "row_id": "DWS2614_5_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "species source-prefactor branch remains blocked",
            "mathematical_form": "claim_allowed=false until proof or finite sourced bound closes every required row",
            "units": "status",
            "status": "NONCLAIM_LOCK",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "SZ2614_0_q_src",
            "quantity": "q_src species label quotient",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence": "LF2614_1 gives exact conditional theorem; SDF2614_2 keeps labelled-domain countermodel open",
            "remaining_gap": "prove source object is T_total before any coupling selection",
        },
        {
            "status_id": "SZ2614_1_no_w_A",
            "quantity": "source-only species prefactors w_A",
            "current_status": "NOT_EXCLUDED",
            "evidence": "weighted action countermodel survives",
            "remaining_gap": "derive no-source-prefactor parent action clause",
        },
        {
            "status_id": "SZ2614_2_total_Hilbert_owner",
            "quantity": "total Hilbert/coframe source owner",
            "current_status": "CONDITIONAL_NOT_EXCLUSIVE",
            "evidence": "variation-before-decomposition works only inside a signed parent action contract",
            "remaining_gap": "prove no labelled, non-Hilbert or post-readout source owner exists",
        },
        {
            "status_id": "SZ2614_3_no_hidden_spurion",
            "quantity": "hidden material/source spurion",
            "current_status": "NOT_EXCLUDED",
            "evidence": "hidden projector countermodel can reintroduce labels after variation",
            "remaining_gap": "parent object language must forbid sigma_A/P_A source-spurion return",
        },
        {
            "status_id": "SZ2614_4_delta_w_species",
            "quantity": "delta_w_species",
            "current_status": "NOT_ZEROED",
            "evidence": "LF2614_5 retains residual",
            "remaining_gap": "parent-signed label forgetting plus no w_A, or finite bound interface filled",
        },
        {
            "status_id": "SZ2614_5_local_GR",
            "quantity": "local GR / WEP / R10 / PPN / clock / orbital branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "species source-prefactor leakage remains a live local source residual",
            "remaining_gap": "no local pass until source-prefactor proof or finite sourced bound closes",
        },
        {
            "status_id": "SZ2614_6_next",
            "quantity": "next derivation owner",
            "current_status": "NO_SOURCE_PREFACTOR_CLAUSE_IS_NEXT",
            "evidence": "all open countermodels enter through w_A/label/spurion source slots",
            "remaining_gap": "build total-Hilbert-source-owner and no-prefactor parent clause",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2614_0_label_forgetting",
            "claim": "parent source functor forgets species labels",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_SOURCE_DOMAIN_QUOTIENT_UNSIGNED",
        },
        {
            "gate_id": "GATE2614_1_no_source_prefactors",
            "claim": "no source-only species prefactors w_A",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NO_SOURCE_PREFACTOR_CLAUSE_UNSIGNED",
        },
        {
            "gate_id": "GATE2614_2_total_Hilbert_owner",
            "claim": "total Hilbert derivative is the only ordinary active-source owner",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_TOTAL_HILBERT_OWNER_NOT_EXCLUSIVE",
        },
        {
            "gate_id": "GATE2614_3_no_hidden_spurion",
            "claim": "no hidden material/source spurion returns after variation",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_HIDDEN_SOURCE_SPURION_EXCLUSION_UNSIGNED",
        },
        {
            "gate_id": "GATE2614_4_delta_w_species_zero",
            "claim": "delta_w_species=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_LABELLED_SOURCE_COUNTERMODEL_SURVIVES",
        },
        {
            "gate_id": "GATE2614_5_delta_w_species_bound",
            "claim": "delta_w_species finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_COMPONENT_BASIS_PROJECTION_BOUND_TABLE_MISSING",
        },
        {
            "gate_id": "GATE2614_6_local_GR_WEP_R10",
            "claim": "local GR / WEP / PPN / clock / orbital / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTA_W_SPECIES_RETAINED",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2614_0_conditional_win",
            "decision": "LABEL_FORGOTTEN_SOURCE_FUNCTOR_THEOREM_IS_CLEAN",
            "reason": "once the source domain is T_total only, relative species couplings are not available variables",
            "next_action": "do not re-litigate Ward conservation; attack source-domain ownership",
        },
        {
            "decision_id": "DEC2614_1_no_promotion",
            "decision": "DELTA_W_SPECIES_NOT_ZEROED",
            "reason": "labelled additive source maps, weighted matter actions and hidden source spurions remain current countermodels",
            "next_action": "retain delta_w_species as nonclaim residual",
        },
        {
            "decision_id": "DEC2614_2_bound_fallback",
            "decision": "DELTA_W_SPECIES_BOUND_INTERFACE_STAGED",
            "reason": "if no-source-prefactor proof fails, the residual must become a finite sourced coefficient",
            "next_action": "fill component basis, composition projection and experiment bound rows only with sources",
        },
        {
            "decision_id": "DEC2614_3_best_next",
            "decision": "NO_SOURCE_PREFACTOR_AND_TOTAL_HILBERT_OWNER_IS_NEXT",
            "reason": "this is the exact high-pressure missing clause that blocks the label-forgetting theorem",
            "next_action": "build 2615 total Hilbert source owner and no-prefactor parent proof or delta_w_species bound input",
        },
        {
            "decision_id": "DEC2614_4_no_claim",
            "decision": "LOCAL_SOURCE_BRANCH_REMAINS_PRIVATE_NONCLAIM",
            "reason": "2614 is a derivation gate and acquisition interface, not a local-GR/WEP pass",
            "next_action": "keep all claim gates closed",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2614_0_primary",
            "status": "selected",
            "doc": "2615-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md",
            "script": "scripts/Y5_R2FR_total_Hilbert_source_owner_and_no_prefactor_clause_or_deltaw_species_bound_input_2615.py",
            "task": "prove the active ordinary source is the total Hilbert/coframe derivative of one matter action with no source-only species prefactor slots; otherwise begin finite delta_w_species bound input",
            "success_condition": "delta_w_species theorem-zero from parent action signature or nonclaim source-bound rows with real basis/projection/provenance",
            "guardrail": "no local-GR, WEP, PPN, clock, orbital or R10 claim from 2614",
        },
        {
            "next_id": "NEXT2614_1_fallback",
            "status": "held_fallback",
            "doc": "2615b-Y5-R2FR-deltaw-species-component-projection-bound-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_species_component_projection_bound_pack_2615b.py",
            "task": "fill component basis, composition projection and WEP/R10/PPN/clock/orbital bound rows if no-prefactor proof remains unsigned",
            "success_condition": "finite delta_w_species envelope can be scored as nonclaim plumbing",
            "guardrail": "no placeholder bound can be valid_for_claim",
        },
        {
            "next_id": "NEXT2614_2_spurion_queue",
            "status": "queued_after_prefactor",
            "doc": "2615c-Y5-R2FR-no-hidden-source-spurion-or-species-projector-bound.md",
            "script": "scripts/Y5_R2FR_no_hidden_source_spurion_or_species_projector_bound_2615c.py",
            "task": "exclude or bound sigma_A/P_A source-spurion return after variation",
            "success_condition": "hidden species projector is theorem-zero or explicitly bounded",
            "guardrail": "do not call Hilbert-current uniqueness enough unless non-Hilbert currents are silenced",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "label_forgetting": label_forgetting_rows(),
        "source_domain": source_domain_rows(),
        "parent_signature": parent_signature_rows(),
        "countermodel": countermodel_rows(),
        "deltaw_species": deltaw_species_rows(),
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
                    "copy_id": f"COPY2614_{key}",
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
    return all(token in text for token in ["2613", "1764", "954/955/977"])


def conditional_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("attempt_id") == "LF2614_1_conditional_theorem"
        and row.get("attempt_status") == "EXACT_CONDITIONAL_THEOREM"
        for row in rows_map["label_forgetting"]
    )


def label_forgetting_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("attempt_id") == "LF2614_5_current_verdict"
        and row.get("attempt_status") == "THEOREM_CONTRACT_READY_PARENT_UNSIGNED"
        for row in rows_map["label_forgetting"]
    )


def fork_unresolved(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("audit_id") == "SDF2614_5_fork_verdict"
        and row.get("status") == "FORK_NOT_RESOLVED"
        for row in rows_map["source_domain"]
    )


def parent_signature_unsigned(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("signature_id") == "PS2614_5_verdict"
        and row.get("status") == "SIGNATURE_CONTRACT_READY_PARENT_UNSIGNED"
        for row in rows_map["parent_signature"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("countermodel_id") == "CM2614_5_verdict"
        and str(row.get("survives_current_constraints", "false")).lower() == "true"
        for row in rows_map["countermodel"]
    )


def deltaw_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["deltaw_species"]
    return any(row.get("row_id") == "DWS2614_0_delta_w_species" for row in rows) and all(
        str(row.get("valid_for_claim", "false")).lower() == "false" for row in rows
    )


def ub_power_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("row_id") == "DWS2614_4_R_source_species" and "U_B" in row.get("mathematical_form", "")
        for row in rows_map["deltaw_species"]
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("status_id") == "SZ2614_5_local_GR" and row.get("current_status") == "NOT_CLAIMABLE"
        for row in rows_map["source_zero"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(str(row.get("gate_pass", "false")).lower() == "false" for row in rows_map["claim_gates"])


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("decision_id") == "DEC2614_3_best_next"
        and "NO_SOURCE_PREFACTOR" in row.get("decision", "")
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("next_id") == "NEXT2614_0_primary"
        and row.get("status") == "selected"
        and "total-Hilbert-source-owner" in row.get("doc", "")
        for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2614*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL2614_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present"),
        ("VAL2614_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2613 current gate plus 1764 and 954/955/977 prior inputs"),
        ("VAL2614_02_conditional_theorem", conditional_theorem_recorded(rows_map), "conditional label-forgetting theorem recorded"),
        ("VAL2614_03_not_promoted", label_forgetting_not_promoted(rows_map), "label-forgetting branch remains unpromoted"),
        ("VAL2614_04_fork_unresolved", fork_unresolved(rows_map), "source-domain fork remains unresolved"),
        ("VAL2614_05_parent_signature_unsigned", parent_signature_unsigned(rows_map), "parent signature contract remains unsigned"),
        ("VAL2614_06_countermodel_retained", countermodel_retained(rows_map), "source countermodel remains retained"),
        ("VAL2614_07_deltaw_interface_nonclaim", deltaw_interface_nonclaim(rows_map), "delta_w_species interface rows remain nonclaim"),
        ("VAL2614_08_U_B_power_retained", ub_power_retained(rows_map), "explicit U_B species-source residual factor retained"),
        ("VAL2614_09_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked"),
        ("VAL2614_10_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked"),
        ("VAL2614_11_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false"),
        ("VAL2614_12_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        ("VAL2614_13_formalization_untouched", no_formalization_artifacts(), "no 2614 outputs found under formalization-workbench"),
        ("VAL2614_14_decision_next", decision_next(rows_map), "decision selects no-source-prefactor/total-Hilbert-owner route"),
        ("VAL2614_15_next_selected", next_selected(rows_map), "next target selected"),
        (
            "VAL2614_16_branch_copies",
            all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"]),
            "nonclaim branch copies exist and parse",
        ),
        ("VAL2614_17_pycache_absent", pycache_absent(), "scripts __pycache__ absent"),
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
                    "check_id": f"VAL2614_CSV_{path.stem}",
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
                    "check_id": f"VAL2614_COPY_CSV_{key}",
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
                "check_id": "VAL2614_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "notes": "2614 species-label forgetting remains conditional and selects total-Hilbert/no-prefactor parent proof next",
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
            "# 2614 Y5 R2FR Species-Label Forgetting Source-Functor Parent Proof Or Delta-W Species Bound",
            "## Summary\n"
            "- This checkpoint attacks the coupling wall directly: can the source functor forget species labels before coupling selection?\n"
            "- Conditional answer: yes. If the source domain is the total Hilbert/coframe current of one matter action, and source-only `w_A` slots are forbidden, `delta_w_species=0` follows structurally.\n"
            "- Current answer: not yet. Labelled additive source maps, weighted matter actions, hidden source spurions and non-Hilbert current splits remain legal countermodels.\n"
            "- Therefore `delta_w_species` remains an explicit nonclaim residual, with a bound interface but no sourced numeric row.\n"
            "- Next target: prove the total-Hilbert-source-owner/no-source-prefactor parent signature, or fill finite sourced bounds.",
            "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "source_key", "source_path", "source_exists", "needles_present"]),
            "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "imported_result", "2614_use"]),
            "## Label-Forgetting Proof Attempt\n" + markdown_table(rows_map["label_forgetting"], ["attempt_id", "claim_piece", "mathematical_form", "attempt_status", "proof_result", "gap"]),
            "## Source-Domain Fork Audit\n" + markdown_table(rows_map["source_domain"], ["audit_id", "domain_choice", "mathematical_form", "consequence", "status", "gap"]),
            "## Parent Signature Requirements\n" + markdown_table(rows_map["parent_signature"], ["signature_id", "required_clause", "contract", "status", "would_close", "if_missing"]),
            "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "needed_to_kill"]),
            "## Delta-W Species Bound Interface\n" + markdown_table(rows_map["deltaw_species"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status"]),
            "## Source Zero Status\n" + markdown_table(rows_map["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
            "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
            "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
            "## Next Target\n" + markdown_table(rows_map["next"], ["next_id", "status", "doc", "script", "task", "success_condition", "guardrail"]),
            "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
            "## Validation\n" + markdown_table(validations, ["check_id", "status", "notes", "detail", "valid_for_claim"]),
            "## Working Verdict\n"
            "This is progress, but not a claim. The coupling wound is now localized to a small parent-action signature: one total matter source, no source-only species prefactors, fixed representation data, and no hidden source-spurion return. If that signature is derived, `delta_w_species` closes cleanly. If it is not, the only honest route is finite sourced bounds for the species residual vector.",
        ]
    ) + "\n"


def main() -> None:
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["label_forgetting"], rows_map["label_forgetting"])
    write_csv(OUTPUTS["source_domain"], rows_map["source_domain"])
    write_csv(OUTPUTS["parent_signature"], rows_map["parent_signature"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["deltaw_species"], rows_map["deltaw_species"])
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
    print(f"2614 validation {validations[-1]['status']}")


if __name__ == "__main__":
    main()
