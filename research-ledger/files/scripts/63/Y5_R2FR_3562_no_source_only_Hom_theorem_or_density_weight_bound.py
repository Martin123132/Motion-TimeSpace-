from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3562-Y5-R2FR-no-source-only-Hom-theorem-or-density-weight-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_NO_SOURCE_ONLY_HOM_3562"
CHECKPOINT_ID = "3562"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def sources() -> dict[str, Path]:
    return {
        "handoff_3561": RESIDUALS / "P8_Y5_R2FR_3561_NEXT_TARGET.csv",
        "density_theorem_3561": RESIDUALS / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
        "density_bounds_3561": RESIDUALS / "P8_Y5_R2FR_3561_BOUND_VECTOR.csv",
        "hom_audit_2612": RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
        "source_prefactor_classes_2612": RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        "source_zero_status_2612": RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_ZERO_STATUS.csv",
        "qbasic_no_source_2829": RESIDUALS / "P8_Y5_R2FR_2829_QBASIC_NO_SOURCE_PREFACTOR_THEOREM_AUDIT.csv",
        "no_source_only_3509": RESIDUALS / "P8_EM_no_source_only_matter_functor_residual.csv",
        "matter_normalization_2646": RESIDUALS / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv",
        "ordinary_matter_signature_2647": RESIDUALS / "P8_Y5_ORDINARY_MATTER_SIGNATURE_2647_SIGNATURE_ATTEMPT.csv",
        "minimal_matter_contract_2587": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
        "hilbert_signature_3293": RESIDUALS / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv",
        "current_source_ward_3508": RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3561": "declares 3562 target",
        "density_theorem_3561": "imports density pullback theorem and source-weight countermodel",
        "density_bounds_3561": "imports source-weight and hidden marker bound rows",
        "hom_audit_2612": "direct no-source-only Hom audit",
        "source_prefactor_classes_2612": "source-prefactor class split and countermodels",
        "source_zero_status_2612": "current zero/nonzero status for direct matter source channels",
        "qbasic_no_source_2829": "q-basic/no-source-prefactor theorem audit",
        "no_source_only_3509": "source-only matter functor residuals",
        "matter_normalization_2646": "matter normalization owner and source-weight countermodel",
        "ordinary_matter_signature_2647": "ordinary matter action signature and fallback kernels",
        "minimal_matter_contract_2587": "minimal parent matter contract and variation-before-readout",
        "hilbert_signature_3293": "Hilbert source signature and source-only exclusion theorem",
        "current_source_ward_3508": "source-current Ward residuals and non-Hilbert bypass",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3562_0_active_prefactor_sort",
            "name": "active-source-prefactor sort definition",
            "statement": "Introduce ActiveSourcePrefactor only as a typed diagnostic target: a map into it would create w_A, kappa_A, hidden-marker or readout-mask source weights before variation.",
            "derivation": "This makes the coupling loophole explicit. If the parent object language lacks this target except for a common scalar action-density endomorphism, relative active-source weights are not typeable.",
            "required_premises": "typed parent object language; source terms defined by Hilbert/Noether variation",
            "current_status": "EXACT_DIAGNOSTIC_SORT",
            "payoff": "separates common calibration from illegal relative source weights",
            "source_path": str(source_paths["source_prefactor_classes_2612"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3562_1_noHom_relative_weight_theorem",
            "name": "no-source-only Hom theorem",
            "statement": "If Hom_parent(SpeciesLabel or HiddenMarker or ReadoutWorldtubeSelector, ActiveSourcePrefactor) is empty, and End(ActionDensityLine)=R_+ common only, then all relative source weights vanish: delta_w_species=0, kappa_A_source=0, hidden_marker_source=0 and Delta_mask=0.",
            "derivation": "A source-only weight is precisely a morphism from labels/markers/readout selectors into the active source prefactor target. If the Hom-set is empty, no such term can appear in the parent grammar. A universal endomorphism multiplies the whole action-density line and is absorbed into common G/source calibration, not a relative source residual.",
            "required_premises": "parent sort disjointness; no active-source-prefactor object except common scalar; variation before readout; Hilbert source signature",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "payoff": "would close the main density-weight obstruction from 3561",
            "source_path": str(source_paths["hom_audit_2612"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3562_2_common_calibration_lemma",
            "name": "common scalar calibration lemma",
            "statement": "A common source prefactor w_* multiplying every ordinary matter sector is not a WEP/species source residual by itself; it belongs to the common calibration/G_ref/action-scale owner.",
            "derivation": "If S_src=w_* sum_A S_A, then Hilbert variation scales every source density equally. Relative source tests see no delta_w_AB; only time/range drift of the common calibration remains as a separate G/source-scale row.",
            "required_premises": "w_* common across species and arenas; no hidden dependence that changes with readout/source body",
            "current_status": "EXACT_CLASSIFICATION_NOT_G_CALIBRATION_PROOF",
            "payoff": "prevents over-penalizing GR-style common G calibration",
            "source_path": str(source_paths["source_prefactor_classes_2612"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3562_3_countermodel_survival",
            "name": "relative source-weight countermodel survival",
            "statement": "If the no-Hom theorem is not parent-signed, relative species weights, hidden marker weights, hidden frame weights, alpha/mass vertices and readout/worldtube masks remain legal diagnostic countermodels.",
            "derivation": "Existing audits classify these terms as live countermodels or policy-forbidden-but-not-parent-derived. Ward identities and common calibration do not remove them as active Hilbert source weights.",
            "required_premises": "none; this is the failure branch",
            "current_status": "COUNTERMODELS_RETAINED",
            "payoff": "prevents false density q-basic promotion",
            "source_path": str(source_paths["source_prefactor_classes_2612"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3562_4_density_consequence",
            "name": "density q-basic consequence",
            "statement": "If NH3562_1 fires together with the 3561 Hilbert density pullback clauses, then the source-only part of E_rho_qbasic is zero; remaining density gates are non-Hilbert bypass, EM coefficient/flux ownership, actual Dq verticality and boundary regularity.",
            "derivation": "3561 decomposes E_rho_qbasic. NH3562_1 removes the source-weight, marker and readout-mask components, but not independent non-Hilbert or EM/boundary channels.",
            "required_premises": "3561 source action pullback plus no-Hom theorem",
            "current_status": "CONDITIONAL_REDUCTION_NOT_FULL_DENSITY_CLAIM",
            "payoff": "shrinks the source-density obstruction to fewer gates",
            "source_path": str(source_paths["density_theorem_3561"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3562_5_current_verdict",
            "name": "current no-Hom verdict",
            "statement": "Current MTS cannot claim the no-source-only Hom theorem because parent sort derivation, hidden-invariant algebra triviality, readout/worldtube source ownership and action-density line uniqueness are not parent-signed together.",
            "derivation": "The corpus has exact conditional theorem rows, but every live source marks the parent object-language exclusion as missing or unsigned.",
            "required_premises": "all no-Hom and action-density clauses signed by parent action",
            "current_status": "CONDITIONAL_THEOREM_PLUS_BOUND_ROWS",
            "payoff": "turns the coupling issue into explicit source-weight rows",
            "source_path": str(source_paths["qbasic_no_source_2829"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def clause_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("NHC3562_0_parent_sorts", "parent sort/object-language derivation for SpeciesLabel, HiddenMarker, ReadoutSelector and ActiveSourcePrefactor", "MISSING_PARENT_OBJECT_LANGUAGE_EXCLUSION", "no-Hom theorem cannot be live without this", "hom_audit_2612"),
        ("NHC3562_1_species_noHom", "Hom(SpeciesLabel, ActiveSourcePrefactor)=common constants only", "NOT_DERIVED", "blocks delta_w_species zero", "hom_audit_2612"),
        ("NHC3562_2_hidden_noHom", "Hom(HiddenMarker, ActiveSourcePrefactor)=empty", "NOT_DERIVED", "blocks hidden_marker_source zero", "hom_audit_2612"),
        ("NHC3562_3_readout_noHom", "Hom(ReadoutWorldtubeSelector, ActiveSourcePrefactor)=empty before variation", "NOT_DERIVED", "blocks Delta_mask zero", "hom_audit_2612"),
        ("NHC3562_4_action_density_line", "single action-density line has only common scalar endomorphism", "ACTION_DENSITY_LINE_OWNER_NOT_DERIVED", "separates common calibration from relative source weights", "matter_normalization_2646"),
        ("NHC3562_5_variation_before_readout", "Hilbert source defined before support/readout/orbital calibration", "CONDITIONAL_WORKFLOW_CONTRACT", "prevents source masks from being fitted after the fact", "minimal_matter_contract_2587"),
        ("NHC3562_6_Hilbert_signature", "all active local source terms come from Hilbert/Noether variations", "CONDITIONAL_NOT_PARENT_SIGNED", "non-Hilbert bypass remains outside no-Hom theorem", "hilbert_signature_3293"),
        ("NHC3562_7_common_G_owner", "common w_* owner separated into G/source calibration row", "CALIBRATION_MODE_NOT_PREDICTION", "common calibration allowed like GR but cannot hide relative weights", "source_prefactor_classes_2612"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "required_clause": required_clause,
            "status": status,
            "effect": effect,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, required_clause, status, effect, source_key in rows
    ]


def residual_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("NHR3562_0_delta_w_species", "delta_w_species", "relative species/source weight w_A-w_B", "LIVE_COUNTERMODEL", "Hom(SpeciesLabel, ActiveSourcePrefactor)=common constants only", "species source weight", "source_prefactor_classes_2612"),
        ("NHR3562_1_kappa_A_source", "kappa_A_source", "source functor selects kappa_A T_A after variation", "LIVE_UNSIGNED", "source functor sees only total Hilbert source object", "active source selector", "no_source_only_3509"),
        ("NHR3562_2_hidden_marker_source", "hidden_marker_source", "hidden/domain/material marker feeds source coefficient", "LIVE_COUNTERMODEL", "Hom(HiddenMarker, ActiveSourcePrefactor)=empty", "hidden source marker", "source_prefactor_classes_2612"),
        ("NHR3562_3_hidden_frame", "A_A(X);disformal_A(X)", "hidden conformal/disformal source frame", "LIVE_UNLESS_DECLARED_EXTENSION", "ordinary matter sees only q-owned observed stack", "hidden source frame", "source_prefactor_classes_2612"),
        ("NHR3562_4_alpha_mass_vertex", "alpha_EM(X);m_A(X);q_A(X)", "direct constant/mass/charge vertex acts as source-density drift", "POLICY_FORBIDDEN_NOT_PARENT_THEOREM", "no direct alpha/mass/charge source vertex theorem", "constant/source vertex", "source_prefactor_classes_2612"),
        ("NHR3562_5_readout_worldtube_mask", "Delta_mask", "post-readout/source-worldtube active source mask", "LIVE_COUNTERMODEL", "support/worldtube owner before variation", "readout mask", "source_prefactor_classes_2612"),
        ("NHR3562_6_common_mode", "w_*", "universal action-density prefactor", "COMMON_CALIBRATION_ROW", "common scalar owner and G/source calibration stability", "common source calibration", "source_prefactor_classes_2612"),
        ("NHR3562_7_nonHilbert_bypass", "nonHilbert_source_bypass", "active source bypasses Hilbert variation entirely", "OUTSIDE_HOM_THEOREM_LIVE", "exact improvement with zero exterior flux or bound", "non-Hilbert source", "current_source_ward_3508"),
        ("NHR3562_8_source_weight_total", "R_source_weight", "total source-only active prefactor residual feeding E_rho_qbasic", "BOUND_VECTOR_REQUIRED_IF_THEOREM_UNSIGNED", "all source-only Hom channels zero or numeric", "source-weight total", "density_bounds_3561"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "zero_condition": zero_condition,
            "gate": gate,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for residual_id, symbol, meaning, status, zero_condition, gate, source_key in rows
    ]


def bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("BH3562_0_delta_w_species", "relative_species_weight", "delta_w_species", "relative active source density weight between matter species", "MISSING_NOHOM_SPECIES_THEOREM_OR_NUMERIC_EPSILON_A", "dimensionless", "WEP;composition;R10;source_normalization", "P8_noHom_species_or_delta_w_bound.csv", "density_bounds_3561"),
        ("BH3562_1_kappa_A_source", "active_source_selector", "kappa_A_source", "post-variation active-source coupling selector", "MISSING_SOURCE_LABEL_FORGETTING_OR_KAPPA_VECTOR", "dimensionless", "WEP;R10;PPN;orbital", "P8_noHom_kappa_source_or_bound.csv", "density_bounds_3561"),
        ("BH3562_2_hidden_marker_source", "hidden_marker_source", "hidden_marker_source", "hidden/domain/material marker to active-source coefficient", "MISSING_NOHOM_HIDDEN_MARKER_OR_BOUND", "dimensionless", "preferred_frame;PPN;source_composition", "P8_noHom_hidden_marker_or_bound.csv", "density_bounds_3561"),
        ("BH3562_3_hidden_frame", "hidden_source_frame", "A_A(X);disformal_A(X)", "hidden conformal/disformal source-frame coefficient", "MISSING_NO_HIDDEN_FRAME_THEOREM_OR_DISFORMAL_BOUND", "dimensionless", "PPN;clocks;R10;source_normalization", "P8_hidden_source_frame_bound.csv", "source_prefactor_classes_2612"),
        ("BH3562_4_alpha_mass_vertex", "direct_constant_vertex", "alpha_EM(X);m_A(X);q_A(X)", "direct alpha/mass/charge source-density vertex", "MISSING_NO_CONSTANT_VERTEX_THEOREM_OR_ALPHA_MASS_BOUND", "dimensionless_or_declared", "alpha_EM;clocks;WEP;fifth_force", "P8_direct_constant_vertex_bound.csv", "source_prefactor_classes_2612"),
        ("BH3562_5_readout_worldtube_mask", "readout_mask", "Delta_mask", "post-fit/source-worldtube active source mask", "MISSING_NO_READOUT_WORLDTUBE_MASK_THEOREM_OR_BOUND", "dimensionless", "anti-tautology;all local arenas", "P8_readout_worldtube_mask_bound.csv", "density_bounds_3561"),
        ("BH3562_6_common_mode", "common_calibration", "w_*;D_t ln w_*", "universal source/action prefactor to be treated as common G/source calibration", "MISSING_COMMON_SCALE_OWNER_OR_DRIFT_BOUND", "yr^-1_or_dimensionless", "Gdot;orbital_GM;clock", "P8_common_source_scale_calibration_bound.csv", "source_prefactor_classes_2612"),
        ("BH3562_7_nonHilbert_bypass", "nonHilbert_current", "nonHilbert_source_bypass", "active source not generated by Hilbert variation", "MISSING_IMPROVEMENT_ZERO_FLUX_OR_NONHILBERT_BOUND", "flux_or_dimensionless", "PPN;source_normalization;boundary_flux", "P8_nonHilbert_bypass_after_noHom_bound.csv", "current_source_ward_3508"),
        ("BH3562_8_source_weight_total", "source_weight_total", "R_source_weight", "total active-source-prefactor residual entering E_rho_qbasic", "NONCLAIM_SUM_UNTIL_ALL_SOURCE_WEIGHT_CHANNELS_ZERO_OR_NUMERIC", "dimensionless_or_declared", "WEP;R10;PPN;orbital;Gdot", "P8_source_weight_total_bound_vector.csv", "density_bounds_3561"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "channel": channel,
            "symbol": symbol,
            "definition": definition,
            "current_value_or_theorem": current_value_or_theorem,
            "units": units,
            "observable_links": observable_links,
            "required_artifact": required_artifact,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, channel, symbol, definition, current_value_or_theorem, units, observable_links, required_artifact, source_key in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3562_0",
            "decision": "The no-source-only Hom theorem is exact conditionally.",
            "meaning": "If the parent has no morphism from species/hidden/readout selectors into active-source prefactors, relative source weights cannot be written.",
            "claim_effect": "conditional theorem only",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3562_1",
            "decision": "Common calibration is separated from cheating.",
            "meaning": "A universal scalar multiplier is allowed as common G/source calibration, but it cannot hide species, material or readout-dependent source weights.",
            "claim_effect": "keeps GR-style G calibration fair",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3562_2",
            "decision": "Current MTS still cannot claim the Hom theorem live.",
            "meaning": "Parent sort disjointness, hidden-invariant triviality, readout/worldtube owner and action-density line uniqueness are all still unsigned together.",
            "claim_effect": "bound rows remain active",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3562_3",
            "decision": "Next target should attack parent sort disjointness directly.",
            "meaning": "The best remaining derivation route is to construct or reject the parent object-language proof that ActiveSourcePrefactor has no non-common incoming Hom.",
            "claim_effect": "sets up 3563",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3562_0",
            "status": "NO_SOURCE_ONLY_HOM_THEOREM_CONDITIONAL_BOUND_ROWS_ACTIVE",
            "summary": "If parent Hom(species/hidden/readout selector, active-source-prefactor) is empty except common scalar calibration, relative active source weights vanish. Current MTS has not parent-signed the sort/no-Hom theorem, so source-weight rows remain nonclaim.",
            "strongest_result": "conditional no-Hom theorem kills delta_w_species, kappa_A_source, hidden_marker_source and Delta_mask if parent sort clauses are signed",
            "still_missing": "parent object-language/sort derivation, hidden-invariant algebra triviality, readout/worldtube owner, action-density line uniqueness, non-Hilbert bypass silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3562_0",
            "target_doc": "3563-Y5-R2FR-parent-sort-disjointness-active-source-prefactor-proof-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3563_parent_sort_disjointness_active_source_prefactor_proof_or_bound.py",
            "objective": "try to construct the parent sort/object-language proof that ActiveSourcePrefactor has no non-common incoming Hom from species, hidden, readout or worldtube selectors; if not, promote the 3562 source-weight bound rows as the official density fallback",
            "success_gate": "parent sort disjointness proof signed, or source-weight fallback rows become the official nonclaim density-owner branch",
            "reason": "3562 reduces the coupling issue to a parent object-language/sort disjointness proof",
            "valid_for_claim": False,
        }
    ]


def validation(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    bounds: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [str(path) for path in source_paths.values() if not path.exists()]
    parse_failures: list[str] = []
    for path in outputs.values():
        if path.suffix.lower() == ".csv":
            try:
                read_csv(path)
            except Exception as exc:
                parse_failures.append(f"{path}: {exc}")
    theorem_ids = {str(row["theorem_id"]) for row in theorem}
    clause_ids = {str(row["clause_id"]) for row in clauses}
    residual_ids = {str(row["residual_id"]) for row in residuals}
    bound_ids = {str(row["bound_id"]) for row in bounds}
    unsafe_claims = [
        str(row["bound_id"])
        for row in bounds
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("score_ready", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    formalization_touched = any(path == FORMALIZATION or FORMALIZATION in path.parents for path in outputs.values())
    rows = [
        ("VAL3562_0_sources_exist", not missing_sources, f"{len(source_paths)-len(missing_sources)}/{len(source_paths)} cited source paths exist" if not missing_sources else "; ".join(missing_sources)),
        ("VAL3562_1_generated_csvs_parse", not parse_failures, f"{sum(1 for path in outputs.values() if path.suffix.lower()=='.csv')} generated CSV files parse" if not parse_failures else "; ".join(parse_failures)),
        ("VAL3562_2_noHom_theorem_present", {"NH3562_1_noHom_relative_weight_theorem","NH3562_2_common_calibration_lemma","NH3562_3_countermodel_survival"}.issubset(theorem_ids), "no-Hom theorem, common calibration lemma and countermodel rows present"),
        ("VAL3562_3_required_clauses_present", {"NHC3562_1_species_noHom","NHC3562_2_hidden_noHom","NHC3562_3_readout_noHom","NHC3562_4_action_density_line"}.issubset(clause_ids), "species, hidden, readout and action-density clauses present"),
        ("VAL3562_4_residuals_present", {"NHR3562_0_delta_w_species","NHR3562_1_kappa_A_source","NHR3562_2_hidden_marker_source","NHR3562_5_readout_worldtube_mask","NHR3562_8_source_weight_total"}.issubset(residual_ids), "key source-weight residuals present"),
        ("VAL3562_5_bound_rows_nonclaim", not unsafe_claims, "all bound rows remain nonclaim" if not unsafe_claims else "; ".join(unsafe_claims)),
        ("VAL3562_6_required_bound_rows_present", {"BH3562_0_delta_w_species","BH3562_1_kappa_A_source","BH3562_2_hidden_marker_source","BH3562_5_readout_worldtube_mask","BH3562_8_source_weight_total"}.issubset(bound_ids), "source-weight bound rows present"),
        ("VAL3562_7_formalization_workbench_untouched", not formalization_touched, "3562 generated outputs only inside post-checkpoint-work"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
        }
        for validation_id, passes, detail in rows
    ]


def write_doc(
    output_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# 3562 - No-source-only Hom theorem or density-weight bound",
        "",
        "## Verdict",
        "3562 reduces the coupling problem to a precise parent object-language gate: if there is no parent `Hom` from species labels, hidden markers, readout selectors or worldtube selectors into an active-source-prefactor object, then relative active source weights cannot be written.",
        "",
        "The theorem is exact conditionally: `Hom_parent(SpeciesLabel/HiddenMarker/ReadoutWorldtubeSelector, ActiveSourcePrefactor)=empty`, with only a common scalar action-density endomorphism allowed, gives `delta_w_species=0`, `kappa_A_source=0`, `hidden_marker_source=0`, and `Delta_mask=0`.",
        "",
        "But current MTS cannot claim it live. The parent sort/object-language proof is not signed, so the source-weight bound rows stay active.",
        "",
        "## No-Hom theorem",
        "A source-only weight is exactly a morphism into an active-source-prefactor slot. Empty Hom-set means no legal term. A universal common scalar is not a relative source residual; it belongs to common `G`/source calibration.",
        "",
        "## What moved",
        "- The vague coupling worry is now a typed Hom-set theorem.",
        "- Common calibration is separated from cheating-style species/source weights.",
        "- Species, hidden-marker, readout-worldtube and hidden-frame countermodels are retained unless the parent sort proof closes.",
        "- The next target is parent sort disjointness for `ActiveSourcePrefactor`.",
        "",
        "## Generated outputs",
    ]
    for name, path in output_paths.items():
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(["", "## Theorem rows"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(["", "## Clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}`: {row['required_clause']} -> {row['status']}")
    lines.extend(["", "## Residual decomposition"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['status']} ({row['meaning']})")
    lines.extend(["", "## Bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['current_value_or_theorem']}")
    lines.extend(["", "## Decision ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} {row['meaning']}")
    lines.extend(["", "## Next target", f"- `{next_rows[0]['target_doc']}`", f"- Objective: {next_rows[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    source_rows = source_register(source_paths)
    theorem = theorem_rows(source_paths)
    clauses = clause_rows(source_paths)
    residuals = residual_rows(source_paths)
    bounds = bound_rows(source_paths)
    decisions = decision_rows()
    statuses = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3562_SOURCE_REGISTER.csv",
        "nohom_theorem": RESIDUALS / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv",
        "clause_audit": RESIDUALS / "P8_Y5_R2FR_3562_HOM_CLAUSE_AUDIT.csv",
        "residual_decomposition": RESIDUALS / "P8_Y5_R2FR_3562_SOURCE_WEIGHT_RESIDUAL_DECOMPOSITION.csv",
        "bound_vector": RESIDUALS / "P8_Y5_R2FR_3562_BOUND_VECTOR.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3562_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3562_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3562_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_no_source_only_Hom_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3562_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["nohom_theorem"], theorem)
    write_csv(outputs["clause_audit"], clauses)
    write_csv(outputs["residual_decomposition"], residuals)
    write_csv(outputs["bound_vector"], bounds)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], statuses)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["canonical_status"], [{
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "canonical_status": statuses[0]["status"],
        "strongest_result": statuses[0]["strongest_result"],
        "still_missing": statuses[0]["still_missing"],
        "next_target": next_rows[0]["target_doc"],
        "claim_allowed": False,
        "valid_for_claim": False,
    }])
    validation_rows = validation(source_paths, {key: path for key, path in outputs.items() if key != "validation"}, theorem, clauses, residuals, bounds)
    write_csv(outputs["validation"], validation_rows)
    write_doc(outputs, theorem, clauses, residuals, bounds, decisions, next_rows)
    for path in [DOC, *outputs.values()]:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
