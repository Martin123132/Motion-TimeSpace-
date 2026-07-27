from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4099-Y5-R2FR-Hilbert-density-no-source-only-Hom-theorem-or-prefactor-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "NO_SOURCE_ONLY_HOM_THEOREM_RECORDED_CONDITIONAL_PARENT_SORT_PROOF_NOT_LIVE_SOURCE_WEIGHT_VECTOR_PROMOTED_AS_OFFICIAL_NONCLAIM_DENSITY_FALLBACK"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4099_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4098_NEXT_TARGET.csv",
        "4099-Y5-R2FR-Hilbert-density-no-source-only-Hom-theorem-or-prefactor-bound.md",
        "4098 selects Hilbert-density no-source-only Hom theorem or prefactor bound.",
    ),
    "SRC4099_01_4098_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4098_BOUND_VECTOR.csv",
        "B4098_3_source_weight",
        "4098 bound vector identifies source-only active prefactor as the next countermodel.",
    ),
    "SRC4099_02_4098_clause": (
        SOURCE_DIR / "P8_Y5_R2FR_4098_IDENTITY_CLAUSE_AUDIT.csv",
        "CLA4098_1_density_qbasic",
        "4098 identity clause requiring q-basic density with no source-only weights.",
    ),
    "SRC4099_03_4098_radial": (
        SOURCE_DIR / "P8_Y5_R2FR_4098_RADIAL_HAIR_DECOMPOSITION.csv",
        "RHD4098_3_source_density_weight",
        "4098 radial/source-hair decomposition contains source-density-weight countermodel.",
    ),
    "SRC4099_04_density_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
        "HDQ3561_3_source_weight_countermodel",
        "3561 q-basic density theorem and source-weight countermodel.",
    ),
    "SRC4099_05_density_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3561_BOUND_VECTOR.csv",
        "BD3561_1_delta_w_species",
        "3561 density bound vector includes source-only weights.",
    ),
    "SRC4099_06_nohom_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv",
        "NH3562_1_noHom_relative_weight_theorem",
        "3562 conditional no-source-only Hom theorem.",
    ),
    "SRC4099_07_nohom_clauses": (
        SOURCE_DIR / "P8_Y5_R2FR_3562_HOM_CLAUSE_AUDIT.csv",
        "NHC3562_0_parent_sorts",
        "3562 Hom clause audit showing parent sort proof is unsigned.",
    ),
    "SRC4099_08_nohom_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3562_SOURCE_WEIGHT_RESIDUAL_DECOMPOSITION.csv",
        "NHR3562_8_source_weight_total",
        "3562 source-weight residual decomposition.",
    ),
    "SRC4099_09_nohom_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3562_BOUND_VECTOR.csv",
        "BH3562_8_source_weight_total",
        "3562 source-weight bound vector.",
    ),
    "SRC4099_10_sort_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3563_PARENT_SORT_CONSTRUCTOR_THEOREM.csv",
        "PSD3563_4_fallback_promotion",
        "3563 parent sort constructor theorem and fallback promotion.",
    ),
    "SRC4099_11_sort_clauses": (
        SOURCE_DIR / "P8_Y5_R2FR_3563_SORT_CLAUSE_AUDIT.csv",
        "PSC3563_0_parent_sorts",
        "3563 sort clause audit: parent primitive sort construction missing.",
    ),
    "SRC4099_12_official_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_3563_OFFICIAL_DENSITY_FALLBACK_ROWS.csv",
        "FB3563_0_delta_w_species",
        "3563 official density fallback rows.",
    ),
    "SRC4099_13_sort_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_3563_DECISION_LEDGER.csv",
        "DEC3563_1",
        "3563 decision selecting official nonclaim density fallback.",
    ),
    "SRC4099_14_nonhilbert_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3564_NONHILBERT_BYPASS_THEOREM.csv",
        "NHB3564_0_decomposition",
        "3564 non-Hilbert bypass decomposition for next gate.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4099_15_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4099 no-source-only Hom/source-weight fallback gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def no_source_only_hom_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "NH4099_0_active_source_prefactor_sort",
            "claim_piece": "diagnostic active-source-prefactor object",
            "statement": "A source-only weight is a parent morphism into an ActiveSourcePrefactor slot before Hilbert variation.",
            "formula": "f: SpeciesLabel/HiddenMarker/ReadoutWorldtubeSelector -> ActiveSourcePrefactor",
            "if_signed": "source-only weights become object-language illegal rather than merely tuned small",
            "current_status": "DIAGNOSTIC_SORT_RECORDED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NH4099_1_noHom_relative_weight_theorem",
            "claim_piece": "no-source-only Hom theorem",
            "statement": "If the parent Hom-set from species, hidden, readout or worldtube selectors into ActiveSourcePrefactor is empty except common calibration, then all relative active source weights vanish.",
            "formula": "Hom_parent(Label/Marker/Readout,ActiveSourcePrefactor)=empty_noncommon and End(ActionDensityLine)=R_+ common => delta_w_species=kappa_A_source=hidden_marker_source=Delta_mask=0",
            "if_signed": "the source-only part of E_rho_qbasic is zero",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NH4099_2_common_calibration",
            "claim_piece": "common source/action calibration",
            "statement": "A universal common action-density prefactor is not a relative source residual by itself; it belongs to calibrated common G/source scale if derivative-free.",
            "formula": "w_A=w_* for all A, D_X w_*=0 => kappa_eff=kappa_ref*w_*",
            "if_signed": "fair GR-style calibration remains allowed without hiding species/source weights",
            "current_status": "COMMON_MODE_ALLOWED_NONPREDICTIVE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NH4099_3_countermodel",
            "claim_piece": "source-only prefactor countermodel",
            "statement": "Without parent sort disjointness, relative species weights, hidden marker weights, source frames, direct constant/mass/charge vertices and readout/worldtube masks remain legal diagnostic countermodels.",
            "formula": "S_src=sum_A(1+epsilon_A(X))S_A or T_source=sum_A kappa_A(X)T_A",
            "if_signed": "not_applicable",
            "current_status": "LIVE_COUNTERMODEL_UNTIL_PARENT_SORT_CONSTRUCTOR_EXISTS",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NH4099_4_density_impact",
            "claim_piece": "impact on Hilbert density q-basicness",
            "statement": "If the no-Hom theorem and the 3561 Hilbert density pullback clauses both fire, then the source-only active-prefactor contribution to E_rho_qbasic vanishes.",
            "formula": "NH4099_1 + density_pullback => E_rho_qbasic[source_weight]=0",
            "if_signed": "support descent and source-mass identity move closer",
            "current_status": "CONDITIONAL_IMPACT_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NH4099_5_current_verdict",
            "claim_piece": "current parent status",
            "statement": "Current MTS does not parent-derive primitive sort construction, constructor exhaustion, action-density line uniqueness, or hidden/readout no-Hom clauses together.",
            "formula": "missing parent sort constructor => no live no-Hom claim",
            "if_signed": "not_applicable",
            "current_status": "OFFICIAL_FALLBACK_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def hom_clause_audit_rows() -> List[dict]:
    return [
        {
            "clause_id": "HCA4099_0_parent_sorts",
            "required_clause": "derive SpeciesLabel, HiddenMarker, ReadoutSelector, WorldtubeSelector and ActiveSourcePrefactor as disjoint parent sorts from MTS primitives",
            "current_status": "MISSING_PRIMITIVE_SORT_CONSTRUCTION",
            "effect": "no-Hom theorem cannot be live without this",
            "fallback_if_missing": "source-weight vector remains official",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "HCA4099_1_constructor_exhaustion",
            "required_clause": "all active source/action constructors factor only through allowed arguments before readout",
            "current_status": "MISSING_CONSTRUCTOR_EXHAUSTION",
            "effect": "otherwise source-only constructor can be added",
            "fallback_if_missing": "delta_w_species;kappa_A_source;Delta_mask",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "HCA4099_2_species_forgetting",
            "required_clause": "source coupling functor forgets species/material labels before choosing active source prefactor",
            "current_status": "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "effect": "would zero relative species weights",
            "fallback_if_missing": "delta_w_species",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "HCA4099_3_hidden_marker",
            "required_clause": "hidden/material/domain markers cannot enter active-source coefficient domain",
            "current_status": "NO_MARKER_EXHAUSTION_UNSIGNED",
            "effect": "would zero hidden_marker_source",
            "fallback_if_missing": "hidden_marker_source;hidden_frame",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "HCA4099_4_readout_worldtube",
            "required_clause": "readout/worldtube selectors cannot create active source masks before variation",
            "current_status": "READOUT_WORLDTUBE_OWNER_UNSIGNED",
            "effect": "would zero post-fit/source-worldtube active masks",
            "fallback_if_missing": "Delta_mask",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "HCA4099_5_action_density_line",
            "required_clause": "single action-density line has only common scalar endomorphism",
            "current_status": "ACTION_DENSITY_LINE_OWNER_NOT_DERIVED",
            "effect": "separates common calibration from relative source weights",
            "fallback_if_missing": "w_*;D_t ln w_*",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "HCA4099_6_hilbert_signature",
            "required_clause": "all active local source terms come from Hilbert/Noether variation or retained residual slots",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "effect": "prevents non-Hilbert bypass outside no-Hom theorem",
            "fallback_if_missing": "nonHilbert_source_bypass",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def source_weight_residual_rows() -> List[dict]:
    return [
        {
            "residual_id": "SWR4099_0_delta_w_species",
            "symbol": "delta_w_species",
            "meaning": "relative species/material active source prefactor after common-mode subtraction",
            "zero_condition": "Hom(SpeciesLabel,ActiveSourcePrefactor)=common constants only",
            "status": "OFFICIAL_NONCLAIM_FALLBACK_ROW",
            "observable_links": "WEP;composition;R10;source_normalization",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_1_kappa_A_source",
            "symbol": "kappa_A_source",
            "meaning": "post-variation source selector kappa_A T_A",
            "zero_condition": "source functor sees only total Hilbert source object",
            "status": "OFFICIAL_NONCLAIM_FALLBACK_ROW",
            "observable_links": "WEP;R10;PPN;orbital",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_2_hidden_marker_source",
            "symbol": "hidden_marker_source",
            "meaning": "hidden/domain/material marker feeds active source coefficient",
            "zero_condition": "Hom(HiddenMarker,ActiveSourcePrefactor)=empty",
            "status": "OFFICIAL_NONCLAIM_FALLBACK_ROW",
            "observable_links": "preferred_frame;PPN;source_composition",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_3_hidden_frame",
            "symbol": "A_A(X);disformal_A(X)",
            "meaning": "hidden conformal/disformal source frame",
            "zero_condition": "ordinary matter sees only q-owned observed stack",
            "status": "OFFICIAL_NONCLAIM_FALLBACK_ROW",
            "observable_links": "PPN;clocks;R10;source_normalization",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_4_alpha_mass_vertex",
            "symbol": "alpha_EM(X);m_A(X);q_A(X)",
            "meaning": "direct constant/mass/charge source-density vertex",
            "zero_condition": "no direct alpha/mass/charge source vertex theorem",
            "status": "RETAINED_FROM_3562_POLICY_FORBIDDEN_NOT_PARENT_THEOREM",
            "observable_links": "alpha_EM;clocks;WEP;fifth_force",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_5_readout_worldtube_mask",
            "symbol": "Delta_mask",
            "meaning": "post-fit/source-worldtube active source mask",
            "zero_condition": "support/worldtube owner before variation",
            "status": "OFFICIAL_NONCLAIM_FALLBACK_ROW",
            "observable_links": "anti-tautology;all_local_arenas",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_6_common_mode",
            "symbol": "w_*;D_t ln w_*",
            "meaning": "universal source/action prefactor separated into calibration/drift row",
            "zero_condition": "common scalar owner and derivative-free G/source calibration stability",
            "status": "COMMON_MODE_NOT_RELATIVE_SOURCE_RESIDUAL",
            "observable_links": "Gdot;orbital_GM;clock",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_7_nonHilbert_bypass",
            "symbol": "nonHilbert_source_bypass",
            "meaning": "active source not generated by Hilbert variation",
            "zero_condition": "exact improvement with zero exterior flux or explicit residual slot",
            "status": "OUTSIDE_NOHOM_NEXT_GATE",
            "observable_links": "PPN;source_normalization;boundary_flux",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "SWR4099_8_source_weight_total",
            "symbol": "R_source_weight",
            "meaning": "no-cancellation source-weight envelope feeding E_rho_qbasic",
            "zero_condition": "all source-only Hom channels zero or numeric",
            "status": "OFFICIAL_NONCLAIM_TOTAL_ENVELOPE",
            "observable_links": "WEP;R10;PPN;orbital;Gdot",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def density_impact_rows() -> List[dict]:
    return [
        {
            "impact_id": "DI4099_0_if_nohom_signed",
            "condition": "parent no-Hom theorem plus 3561 density pullback clauses",
            "impact": "source-only contribution to E_rho_qbasic vanishes",
            "mass_identity_effect": "support descent and Pi_M^H source-mass identity lose one major countermodel",
            "status": "CONDITIONAL_UNLOCK",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "DI4099_1_current_state",
            "condition": "parent sort constructor proof not signed",
            "impact": "source-weight vector remains active and official",
            "mass_identity_effect": "Hamiltonian/Gauss/Newton source-mass identity remains nonclaim",
            "status": "OFFICIAL_FALLBACK_ACTIVE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "DI4099_2_common_mode",
            "condition": "only universal derivative-free common prefactor exists",
            "impact": "absorbed into common calibrated kappa/G_ref scale, not treated as relative source residual",
            "mass_identity_effect": "allowed only if D_t w_*=D_r w_*=D_species w_*=0",
            "status": "COMMON_CALIBRATION_ALLOWED_WITH_DRIFT_GUARD",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "DI4099_3_next_gate",
            "condition": "source weights officially fallbacked",
            "impact": "do not spend another loop restating no-Hom missing",
            "mass_identity_effect": "move to non-Hilbert source bypass and common coupling owner",
            "status": "NEXT_GATE_NONHILBERT_BYPASS",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def bound_vector_rows() -> List[dict]:
    return [
        {
            "bound_id": "BH4099_0_delta_w_species",
            "channel": "relative species/source weight",
            "symbol": "delta_w_species",
            "definition": "relative active source density weight between matter species",
            "needed_input": "parent no-Hom species theorem or numeric epsilon_A vector",
            "observable_links": "WEP;composition;R10;source_normalization",
            "current_value": "MISSING_NOHOM_SPECIES_THEOREM_OR_NUMERIC_EPSILON_A",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_1_kappa_A_source",
            "channel": "active-source selector",
            "symbol": "kappa_A_source",
            "definition": "post-variation active-source coupling selector",
            "needed_input": "source-label-forgetting theorem or kappa_A vector",
            "observable_links": "WEP;R10;PPN;orbital",
            "current_value": "MISSING_SOURCE_LABEL_FORGETTING_OR_KAPPA_VECTOR",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_2_hidden_marker_source",
            "channel": "hidden marker source",
            "symbol": "hidden_marker_source",
            "definition": "hidden/domain/material marker to active-source coefficient",
            "needed_input": "no-Hom hidden marker theorem or bound",
            "observable_links": "preferred_frame;PPN;source_composition",
            "current_value": "MISSING_NOHOM_HIDDEN_MARKER_OR_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_3_hidden_frame",
            "channel": "hidden source frame",
            "symbol": "A_A(X);disformal_A(X)",
            "definition": "hidden conformal/disformal source-frame coefficient",
            "needed_input": "no hidden frame theorem or disformal bound",
            "observable_links": "PPN;clocks;R10;source_normalization",
            "current_value": "MISSING_NO_HIDDEN_FRAME_THEOREM_OR_DISFORMAL_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_4_alpha_mass_vertex",
            "channel": "direct constant/mass/charge source vertex",
            "symbol": "alpha_EM(X);m_A(X);q_A(X)",
            "definition": "direct alpha/mass/charge source-density vertex",
            "needed_input": "no constant-vertex theorem or alpha/mass bound",
            "observable_links": "alpha_EM;clocks;WEP;fifth_force",
            "current_value": "MISSING_NO_CONSTANT_VERTEX_THEOREM_OR_ALPHA_MASS_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_5_readout_worldtube_mask",
            "channel": "readout/worldtube source mask",
            "symbol": "Delta_mask",
            "definition": "post-fit/source-worldtube active source mask",
            "needed_input": "no readout/worldtube mask theorem or bound",
            "observable_links": "anti-tautology;all_local_arenas",
            "current_value": "MISSING_NO_READOUT_WORLDTUBE_MASK_THEOREM_OR_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_6_common_mode",
            "channel": "common calibration/drift",
            "symbol": "w_*;D_t ln w_*",
            "definition": "universal source/action prefactor as common G/source calibration plus drift guard",
            "needed_input": "common scale owner or drift bound",
            "observable_links": "Gdot;orbital_GM;clock",
            "current_value": "MISSING_COMMON_SCALE_OWNER_OR_DRIFT_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_7_nonHilbert_bypass",
            "channel": "non-Hilbert source bypass",
            "symbol": "nonHilbert_source_bypass",
            "definition": "active source not generated by Hilbert variation",
            "needed_input": "improvement zero-flux theorem or non-Hilbert bound",
            "observable_links": "PPN;source_normalization;boundary_flux",
            "current_value": "MISSING_IMPROVEMENT_ZERO_FLUX_OR_NONHILBERT_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "BH4099_8_source_weight_total",
            "channel": "total source-weight envelope",
            "symbol": "R_source_weight",
            "definition": "total active-source-prefactor residual entering E_rho_qbasic",
            "needed_input": "all source-weight channels theorem-zero or numeric",
            "observable_links": "WEP;R10;PPN;orbital;Gdot",
            "current_value": "NONCLAIM_SUM_UNTIL_ALL_SOURCE_WEIGHT_CHANNELS_ZERO_OR_NUMERIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_gate_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4099_0_theorem",
            "decision": "record no-source-only Hom theorem as exact conditional mathematics",
            "meaning": "If the parent object language has no incoming non-common Hom into ActiveSourcePrefactor, relative source weights cannot be written.",
            "result": "clear theorem route exists",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4099_1_fallback",
            "decision": "do not claim the theorem live; promote source-weight vector as official nonclaim density fallback",
            "meaning": "Parent sort construction and constructor exhaustion are not derived from primitives.",
            "result": "delta_w_species/kappa_A/hidden/readout rows remain active",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4099_2_common_calibration",
            "decision": "allow common derivative-free calibration but forbid hiding relative source weights inside it",
            "meaning": "This matches GR's calibrated G standard while keeping WEP/source-charge tests honest.",
            "result": "common mode split from relative source residuals",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4099_3_next",
            "decision": "move next to non-Hilbert source bypass rather than re-looping no-Hom",
            "meaning": "3563 already made no-Hom fallback official until a new parent constructor proof appears.",
            "result": "4100 target selected",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4099_0_conditional_nohom",
            "claim": "no-source-only Hom theorem would zero relative active source weights if parent-signed",
            "allowed": "True",
            "reason": "empty non-common Hom into ActiveSourcePrefactor forbids source-only prefactor terms by parent grammar",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4099_1_live_nohom",
            "claim": "MTS currently derives the no-source-only Hom theorem live",
            "allowed": "False",
            "reason": "parent sort construction, constructor exhaustion and action-density line uniqueness are unsigned",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4099_2_density_qbasic",
            "claim": "Hilbert density q-basicness is proved",
            "allowed": "False",
            "reason": "source-weight vector, non-Hilbert bypass, EM flux and boundary regularity remain active",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4099_3_Newton",
            "claim": "source-normalized Newtonian mechanics is publicly derived",
            "allowed": "False",
            "reason": "4099 only handles one density countermodel; source-mass identity and other density gates remain nonclaim",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4099_4_local_GR",
            "claim": "local GR/PPN is derived",
            "allowed": "False",
            "reason": "PPN/R11/EM/non-Hilbert source-current gates remain downstream",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4099_0",
            "next_target": "4100-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md",
            "script": "scripts/Y5_R2FR_4100_nonHilbert_source_bypass_improvement_zero_or_bound.py",
            "why": "4099 makes source-weight rows official fallback. The next live density/source-current gate is non-Hilbert source bypass: exact improvements can be silent, but spin/torsion, boundary/worldtube, readout and projector tails remain live.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4099_1",
            "next_target": "4101-Y5-R2FR-common-coupling-owner-or-Gdot-bound.md",
            "script": "defer_until_nonHilbert_bypass_gate",
            "why": "Common calibration is allowed only if derivative-free and parent-owned; otherwise it becomes Gdot/source-drift.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4099",
            "decision": DECISION,
            "noHom_theorem": "conditional_exact",
            "live_noHom_claim": "False",
            "source_weight_fallback": "official_nonclaim",
            "density_qbasic_public": "False",
            "Newton_source_public": "False",
            "next_required_gate": "nonHilbert_source_bypass_improvement_zero_or_bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4099 - Hilbert Density No-Source-Only Hom Theorem Or Prefactor Bound",
                "",
                "## Purpose",
                "",
                "4098 reduced the source-mass identity to q-basic Hilbert density/support plus Hamiltonian equality. 4099 handles the dangerous density countermodel: source-only active prefactors.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public density q-basic claim: `false`",
                "- Public Newton/local-GR claim: `false`",
                "",
                "## Conditional Theorem",
                "",
                "A source-only weight is a parent morphism into an active-source-prefactor slot:",
                "",
                "```text",
                "Hom_parent(SpeciesLabel/HiddenMarker/ReadoutWorldtubeSelector, ActiveSourcePrefactor)",
                "```",
                "",
                "If that Hom-set is empty except common calibration, then",
                "",
                "```text",
                "delta_w_species = 0",
                "kappa_A_source = 0",
                "hidden_marker_source = 0",
                "Delta_mask = 0",
                "```",
                "",
                "and the source-only part of `E_rho_qbasic` vanishes.",
                "",
                "## Current Verdict",
                "",
                "The theorem is exact conditionally, but current MTS does not derive the parent sort constructor, constructor exhaustion, hidden/readout no-Hom clauses, or action-density line uniqueness from primitives. So the theorem is not live.",
                "",
                "## Official Fallback",
                "",
                "The official density fallback is now the source-weight vector: `delta_w_species`, `kappa_A_source`, `hidden_marker_source`, `hidden_frame`, `alpha/mass/charge vertices`, `Delta_mask`, common-mode drift, `nonHilbert_source_bypass`, and `R_source_weight`.",
                "",
                "## Next Target",
                "",
                "`4100-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md` should handle the next live density/source-current gate. Exact improvements may cancel, but total non-Hilbert bypass does not vanish unless spin/torsion, boundary/worldtube, readout, projector/support and decoupled blocks are zeroed or bounded.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4099_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4099_NO_SOURCE_ONLY_HOM_THEOREM.csv`",
                "- `P8_Y5_R2FR_4099_HOM_CLAUSE_AUDIT.csv`",
                "- `P8_Y5_R2FR_4099_SOURCE_WEIGHT_RESIDUALS.csv`",
                "- `P8_Y5_R2FR_4099_DENSITY_IMPACT.csv`",
                "- `P8_Y5_R2FR_4099_BOUND_VECTOR.csv`",
                "- `P8_Y5_R2FR_4099_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4099_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4099_NEXT_TARGET.csv`",
                "- `P8_Y5_R2FR_4099_STATUS.csv`",
                "- `P8_Y5_BRR545_4099_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4099_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4099_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4099_NO_SOURCE_ONLY_HOM_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4099_NO_SOURCE_ONLY_HOM_THEOREM.csv",
        "P8_Y5_R2FR_4099_HOM_CLAUSE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4099_HOM_CLAUSE_AUDIT.csv",
        "P8_Y5_R2FR_4099_SOURCE_WEIGHT_RESIDUALS": SOURCE_DIR / "P8_Y5_R2FR_4099_SOURCE_WEIGHT_RESIDUALS.csv",
        "P8_Y5_R2FR_4099_DENSITY_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4099_DENSITY_IMPACT.csv",
        "P8_Y5_R2FR_4099_BOUND_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4099_BOUND_VECTOR.csv",
        "P8_Y5_R2FR_4099_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4099_DECISION_GATE.csv",
        "P8_Y5_R2FR_4099_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4099_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4099_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4099_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4099_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4099_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4099_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_NO_SOURCE_ONLY_HOM_THEOREM"], no_source_only_hom_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_HOM_CLAUSE_AUDIT"], hom_clause_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_SOURCE_WEIGHT_RESIDUALS"], source_weight_residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_DENSITY_IMPACT"], density_impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_BOUND_VECTOR"], bound_vector_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4099_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4099_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4099_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4099_NO_SOURCE_ONLY_HOM_THEOREM"])
    theorem_text = "\n".join(str(row) for row in theorem)
    theorem_ok = all(
        needle in theorem_text
        for needle in ["ActiveSourcePrefactor", "Hom_parent", "delta_w_species", "COMMON_MODE_ALLOWED", "OFFICIAL_FALLBACK_REQUIRED"]
    )
    rows.append(
        {
            "check_id": "VAL4099_NOHOM_THEOREM",
            "check": "no-Hom theorem records conditional zero, common calibration and current fallback verdict",
            "passed": bool_string(theorem_ok),
            "detail": "requires ActiveSourcePrefactor, Hom, delta_w, common mode and fallback verdict",
            "timestamp_utc": TIMESTAMP,
        }
    )

    clauses = parse_csv(outputs["P8_Y5_R2FR_4099_HOM_CLAUSE_AUDIT"])
    clause_text = "\n".join(str(row) for row in clauses)
    clause_ok = all(
        needle in clause_text
        for needle in ["parent sorts", "constructor", "species", "hidden", "readout", "action-density", "non-Hilbert"]
    )
    rows.append(
        {
            "check_id": "VAL4099_CLAUSE_AUDIT",
            "check": "clause audit covers parent sorts, constructor exhaustion, species, hidden, readout, action-density and non-Hilbert gates",
            "passed": bool_string(clause_ok),
            "detail": f"clause_rows={len(clauses)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    residuals = parse_csv(outputs["P8_Y5_R2FR_4099_SOURCE_WEIGHT_RESIDUALS"])
    residual_text = "\n".join(str(row) for row in residuals)
    residual_ok = all(
        needle in residual_text
        for needle in [
            "delta_w_species",
            "kappa_A_source",
            "hidden_marker_source",
            "A_A(X);disformal_A(X)",
            "alpha_EM(X);m_A(X);q_A(X)",
            "Delta_mask",
            "w_*",
            "nonHilbert_source_bypass",
            "R_source_weight",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4099_RESIDUAL_COVERAGE",
            "check": "source-weight residual rows cover all official fallback channels",
            "passed": bool_string(residual_ok),
            "detail": f"residual_rows={len(residuals)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    impact = parse_csv(outputs["P8_Y5_R2FR_4099_DENSITY_IMPACT"])
    impact_text = "\n".join(str(row) for row in impact)
    impact_ok = all(needle in impact_text for needle in ["E_rho_qbasic", "OFFICIAL_FALLBACK_ACTIVE", "COMMON_CALIBRATION_ALLOWED", "NEXT_GATE_NONHILBERT_BYPASS"])
    rows.append(
        {
            "check_id": "VAL4099_DENSITY_IMPACT",
            "check": "density impact separates conditional unlock, official fallback, common calibration and next gate",
            "passed": bool_string(impact_ok),
            "detail": f"impact_rows={len(impact)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    bounds = parse_csv(outputs["P8_Y5_R2FR_4099_BOUND_VECTOR"])
    bound_text = "\n".join(str(row) for row in bounds)
    bound_ok = all(
        needle in bound_text
        for needle in [
            "MISSING_NOHOM_SPECIES_THEOREM_OR_NUMERIC_EPSILON_A",
            "MISSING_SOURCE_LABEL_FORGETTING_OR_KAPPA_VECTOR",
            "MISSING_NOHOM_HIDDEN_MARKER_OR_BOUND",
            "MISSING_NO_CONSTANT_VERTEX_THEOREM_OR_ALPHA_MASS_BOUND",
            "NONCLAIM_SUM_UNTIL_ALL_SOURCE_WEIGHT_CHANNELS_ZERO_OR_NUMERIC",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4099_BOUND_VECTOR",
            "check": "bound vector preserves source-weight fallback rows and nonclaim total envelope",
            "passed": bool_string(bound_ok),
            "detail": f"bound_rows={len(bounds)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claims = parse_csv(outputs["P8_Y5_R2FR_4099_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    rows.append(
        {
            "check_id": "VAL4099_NO_PUBLIC_CLAIM",
            "check": "4099 does not promote live no-Hom, density q-basicness, Newton or local-GR claims",
            "passed": bool_string(no_public),
            "detail": "all claim rows remain private/nonclaim",
            "timestamp_utc": TIMESTAMP,
        }
    )

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4099_NEXT_TARGET"])
    next_text = "\n".join(str(row) for row in next_rows)
    next_ok = "4100-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md" in next_text
    rows.append(
        {
            "check_id": "VAL4099_NEXT_TARGET",
            "check": "next target moves to non-Hilbert source bypass instead of restating no-Hom",
            "passed": bool_string(next_ok),
            "detail": "requires 4100 non-Hilbert bypass target",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4099_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4099_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4099_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4099 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
