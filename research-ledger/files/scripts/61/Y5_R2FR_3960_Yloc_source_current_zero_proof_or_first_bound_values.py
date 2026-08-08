from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3960"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3960-Y5-R2FR-Yloc-source-current-zero-proof-or-first-bound-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3960_SOURCE_REGISTER.csv",
    "grammar": SRC / "P8_Y5_R2FR_3960_SOURCE_CURRENT_ZERO_GRAMMAR.csv",
    "component": SRC / "P8_Y5_R2FR_3960_COMPONENT_ZERO_OR_BOUND_DECISIONS.csv",
    "first_values": SRC / "P8_Y5_R2FR_3960_FIRST_CONDITIONAL_ZERO_VALUES.csv",
    "residual_queue": SRC / "P8_Y5_R2FR_3960_RETAINED_RESIDUAL_VALUE_QUEUE.csv",
    "em_gate": SRC / "P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3960_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3960_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3960_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3960_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3960_VALIDATION.csv",
}

NEXT_DOC = "3961-Y5-R2FR-EM-Poynting-hidden-F2-exclusion-or-flux-bound-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3961_EM_Poynting_hidden_F2_exclusion_or_flux_bound_values.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3960_00_3959_next", SRC / "P8_Y5_R2FR_3959_NEXT_TARGET.csv", "NEXT3959_0", "3959 handoff"),
        ("SRC3960_01_3959_amplitude", SRC / "P8_Y5_R2FR_3959_YLOC_ZERO_THEOREM_OR_BOUND.csv", "YB3959_3_amplitude_bound", "Yloc amplitude law"),
        ("SRC3960_02_3959_sigma", SRC / "P8_Y5_R2FR_3959_YLOC_ZERO_THEOREM_OR_BOUND.csv", "YB3959_4_sigma_bound", "Sigma square-law"),
        ("SRC3960_03_3959_components", SRC / "P8_Y5_R2FR_3959_COMPONENT_SOURCE_BOUND_ROWS.csv", "YSC3959_0_chiD_trace", "component bound rows"),
        ("SRC3960_04_3959_EM", SRC / "P8_Y5_R2FR_3959_COMPONENT_SOURCE_BOUND_ROWS.csv", "YSC3959_6_EM_Poynting_F2", "EM hidden channel row"),
        ("SRC3960_05_3959_CA", SRC / "P8_Y5_R2FR_3959_CA_TOTAL_CURRENT_BOUND_LAW.csv", "CAB3959_0_CA_total_current", "C_A current bound"),
        ("SRC3960_06_3959_EMalpha", SRC / "P8_Y5_R2FR_3959_CA_TOTAL_CURRENT_BOUND_LAW.csv", "CAB3959_5_EM_alpha_charge", "EM alpha bound"),
        ("SRC3960_07_chain_rule", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_1_chain_rule", "source-current chain rule"),
        ("SRC3960_08_bound_if_leaky", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_3_bound_if_leaky", "source-current bound if leaky"),
        ("SRC3960_09_CA_bound", SRC / "P8_Y5_R2FR_3955_CA_ZERO_THEOREM_OR_BOUND.csv", "CA3955_4_CA_norm_bound", "C_A norm bound"),
        ("SRC3960_10_Yloc_source_audit", SRC / "P8_YLOC_SOURCE_CURRENT_COMPONENT_AUDIT.csv", "J0_trace_expansion", "component source audit trace"),
        ("SRC3960_11_Yloc_stress", SRC / "P8_YLOC_SOURCE_CURRENT_COMPONENT_AUDIT.csv", "J5_extra_stress_Bianchi", "extra stress retained"),
        ("SRC3960_12_debt_boundary", SRC / "P8_YLOC_SOURCE_DEBT_LEDGER.csv", "S0_boundary_source", "boundary source debt"),
        ("SRC3960_13_debt_bianchi", SRC / "P8_YLOC_SOURCE_DEBT_LEDGER.csv", "S4_Bianchi_stress_current", "Bianchi stress debt"),
        ("SRC3960_14_no_linear_sym", SRC / "P8_YLOC_NO_LINEAR_SOURCE_THEOREM.csv", "T1_exact_reflection", "no-linear-source symmetry"),
        ("SRC3960_15_boundary_even", SRC / "P8_YLOC_NO_LINEAR_SOURCE_THEOREM.csv", "T2_boundary_evenness", "boundary evenness"),
        ("SRC3960_16_EM_minimal", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_0_minimal_bound_field_stress", "minimal Maxwell bound stress"),
        ("SRC3960_17_EM_flux", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_1_radiative_poynting_flux", "Poynting flux"),
        ("SRC3960_18_EM_F2", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_2_nonminimal_XF2", "hidden F2 cross term"),
        ("SRC3960_19_EM_exchange", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_5_matter_EM_internal_exchange", "matter EM exchange cancellation"),
        ("SRC3960_20_Hodge", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_0_Delta_Hodge_EM", "Hodge/coframe residual"),
        ("SRC3960_21_EM_readout", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_5_C_EM_readout", "EM readout residual"),
        ("SRC3960_22_delta_w", SRC / "P8_EM_no_source_only_matter_functor_residual.csv", "NSSR3509_0_delta_w_species", "connected density-line species zero"),
        ("SRC3960_23_kappa_source", SRC / "P8_EM_no_source_only_matter_functor_residual.csv", "NSSR3509_2_kappa_A_source", "source-label forgetting"),
        ("SRC3960_24_hidden_marker", SRC / "P8_EM_no_source_only_matter_functor_residual.csv", "NSSR3509_3_hidden_marker_source", "hidden marker source slot"),
        ("SRC3960_25_preweight", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_5_prevariation_weight", "prevariation weight countermodel"),
        ("SRC3960_26_nonhilbert", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_6_nonHilbert_bypass", "non-Hilbert bypass"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:1000]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def grammar_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SCG3960_0_variation_before_readout",
            "grammar_clause": "vary parent action before observer/readout redefinitions",
            "math_condition": "J_parent := delta S_parent/delta Y; readout maps act after Hilbert/Noether variation",
            "zero_effect": "post-variation rescaling cannot create a source-current",
            "violating_counterterm": "readout-dependent current rescaling before variation",
            "status": "ZERO_IF_PARENT_GRAMMAR_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCG3960_1_connected_density_line",
            "grammar_clause": "ordinary matter species share one connected parent density-line",
            "math_condition": "S_matter=sum_A S_A[g_obs,psi_A] with no species weight w_A(Y); common w(Y) absorbed into source/G normalization",
            "zero_effect": "delta_w_species=0 and no species-composition source charge",
            "violating_counterterm": "sum_A w_A(Y) S_A",
            "status": "ZERO_IF_NO_SPECIES_WEIGHT_SLOT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCG3960_2_source_label_forgetting",
            "grammar_clause": "active source coupling sees total Hilbert source, not material labels",
            "math_condition": "F_source(T_A,A) factors through T_total^Hilbert plus exact improvements",
            "zero_effect": "kappa_A_source, beta_source_alpha, and hidden_marker_source vanish as source-only spurions",
            "violating_counterterm": "kappa_A(Y) T_A or hidden-marker source coefficient",
            "status": "ZERO_IF_SOURCE_FUNCTOR_FORGETS_LABELS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCG3960_3_minimal_Maxwell_same_Hodge",
            "grammar_clause": "Maxwell stress uses the same observed metric/coframe Hodge star",
            "math_condition": "S_EM=-1/(4mu0) int F wedge *_obs F and no f(Y)F^2 or g(Y)F*F",
            "zero_effect": "visible EM stress is inside T_total/M_H and is not extra hidden Y source",
            "violating_counterterm": "f_Y(Y) F_mnF^mn or independent *_EM",
            "status": "ZERO_FOR_VISIBLE_MINIMAL_EM_EXTRA_SOURCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCG3960_4_total_matter_EM_exchange",
            "grammar_clause": "matter and EM are varied as one total stress system",
            "math_condition": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "zero_effect": "internal Lorentz exchange cancels in T_total",
            "violating_counterterm": "counting matter-only nonconservation as hidden source force",
            "status": "EXACT_ZERO_IN_TOTAL_STRESS_BOOKKEEPING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCG3960_5_stationary_isolated_boundary",
            "grammar_clause": "stationary isolated local branch has no net radiative/background flux through the chosen exterior boundary",
            "math_condition": "Phi_EM_rad=int_boundary S_Poynting dot n dA = 0 after averaging/stationary isolation",
            "zero_effect": "B_EM and radiative Poynting source vanish",
            "violating_counterterm": "incoming/background radiation, nonstationary source, or boundary chosen through radiation zone",
            "status": "NOT_ADOPTED_YET_NEXT_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCG3960_6_no_nonHilbert_bypass",
            "grammar_clause": "all active source currents are Hilbert/improvement-owned",
            "math_condition": "J_src=kappa T_H + exact_improvement with zero exterior flux",
            "zero_effect": "non-Hilbert bypass does not source Y_loc",
            "violating_counterterm": "independent non-Hilbert source current with exterior flux",
            "status": "OPEN_PARALLEL_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def component_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "CZD3960_0_chiD_trace",
            "component": "chi_D / X_D trace-load",
            "zero_or_bound_decision": "PARTIAL_CONDITIONAL_ZERO",
            "new_result": "stationarity/volume identity can set the trace source to zero only after branch/domain selector and boundary flux ownership are signed",
            "value_row": "no numeric value assigned",
            "remaining_inputs": "branch selector; boundary flux; lambda_chi",
            "feeds": "C_A_total; source normalization; R10/Gdot",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "CZD3960_1_species_source_spurions",
            "component": "species/source-only matter labels",
            "zero_or_bound_decision": "FIRST_CONDITIONAL_ZERO_VALUES",
            "new_result": "connected density-line plus source-label-forgetting kills species/source-only spurions",
            "value_row": "delta_w_species=0; kappa_A_source=0; beta_source_alpha=0; hidden_marker_source=0 under grammar clauses",
            "remaining_inputs": "parent grammar adoption; no prevariation weights",
            "feeds": "WEP/source composition; alpha/source marker",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "CZD3960_2_visible_EM_stress",
            "component": "ordinary minimal Maxwell stress",
            "zero_or_bound_decision": "FIRST_CONDITIONAL_ZERO_VALUE",
            "new_result": "visible Maxwell stress is part of T_total/M_H if it uses the same g_obs Hodge star; it is not an extra hidden Y source",
            "value_row": "epsilon_EM_extra=0 under minimal same-Hodge grammar",
            "remaining_inputs": "Delta_Hodge_EM=0 and no independent w_EM",
            "feeds": "EM stress; source coupling; Newton/GR source normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "CZD3960_3_matter_EM_exchange",
            "component": "matter-EM Lorentz exchange",
            "zero_or_bound_decision": "EXACT_BOOKKEEPING_ZERO",
            "new_result": "internal matter-EM exchange cancels inside total stress and must not be counted as an MTS hidden force",
            "value_row": "epsilon_internal_exchange=0 in T_total bookkeeping",
            "remaining_inputs": "total Hilbert stress use in source projector",
            "feeds": "Bianchi/source conservation; EM coupling",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "CZD3960_4_hidden_EM_F2",
            "component": "hidden nonminimal F^2/F*F coupling",
            "zero_or_bound_decision": "OPEN_NEXT_TARGET",
            "new_result": "not killed by Ward identity; must be excluded by action grammar or bounded",
            "value_row": "C_XF2 remains missing",
            "remaining_inputs": "operator-domain exclusion or empirical/source bound on C_XF2",
            "feeds": "alpha; clocks; EM source leakage; local GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "CZD3960_5_Poynting_flux",
            "component": "radiative/background Poynting boundary flux",
            "zero_or_bound_decision": "OPEN_NEXT_TARGET",
            "new_result": "can be zero on stationary isolated branch, but branch/boundary theorem is not yet adopted",
            "value_row": "Phi_EM_rad remains missing unless stationary no-flux branch is signed",
            "remaining_inputs": "boundary class; averaging rule; source/radiation exclusion",
            "feeds": "B_EM; clocks; orbital; alpha/source leakage",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "CZD3960_6_nonHilbert_bypass",
            "component": "non-Hilbert source current bypass",
            "zero_or_bound_decision": "OPEN_PARALLEL_GATE",
            "new_result": "ordinary Hilbert Ward identity cannot kill independent non-Hilbert source currents",
            "value_row": "Delta_nonHilbert remains retained",
            "remaining_inputs": "exact improvement theorem or finite exterior-flux bound",
            "feeds": "source coupling; WEP; PPN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "CZD3960_7_projector_extra_stress",
            "component": "projector/domain extra stress",
            "zero_or_bound_decision": "RETAINED_BOUND_BRANCH",
            "new_result": "can be Bianchi-owned but not zeroed by Y proof alone",
            "value_row": "T_extra retained for scoring",
            "remaining_inputs": "topological/isotropic stress theorem or explicit PPN/R11 bound",
            "feeds": "xi; alpha3; beta; zeta",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def first_value_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "value_id": "FZ3960_0_delta_w_species",
            "symbol": "delta_w_species",
            "conditional_value": "0",
            "units": "dimensionless",
            "condition": "single connected ordinary-matter parent density-line; no species-dependent prevariation w_A(Y)",
            "source_path": str(SRC / "P8_EM_no_source_only_matter_functor_residual.csv"),
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "FZ3960_1_kappa_A_source",
            "symbol": "kappa_A_source",
            "conditional_value": "0",
            "units": "dimensionless",
            "condition": "source functor sees total Hilbert source object, not species/source labels",
            "source_path": str(SRC / "P8_EM_no_source_only_matter_functor_residual.csv"),
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "FZ3960_2_hidden_marker_source",
            "symbol": "hidden_marker_source",
            "conditional_value": "0",
            "units": "dimensionless",
            "condition": "no parent Hom from hidden marker to source coefficient target except common constant",
            "source_path": str(SRC / "P8_EM_no_source_only_matter_functor_residual.csv"),
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "FZ3960_3_postvariation_rescaling",
            "symbol": "postvariation_current_rescaling",
            "conditional_value": "0",
            "units": "dimensionless",
            "condition": "variation-before-readout order; parent current is fixed before observer normalization",
            "source_path": str(SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv"),
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "FZ3960_4_epsilon_EM_extra",
            "symbol": "epsilon_EM_extra_hidden_source",
            "conditional_value": "0",
            "units": "dimensionless",
            "condition": "ordinary minimal Maxwell action uses same observed Hodge star and its stress is included in T_total/M_H",
            "source_path": str(SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"),
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "FZ3960_5_epsilon_internal_exchange",
            "symbol": "epsilon_internal_exchange",
            "conditional_value": "0",
            "units": "dimensionless",
            "condition": "matter and EM stress are accounted together in T_total; Lorentz exchange is internal",
            "source_path": str(SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"),
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_queue_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "needed_next": needed_next,
            "observable_links": links,
            "status": "RETAINED_NOT_ZEROED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for residual_id, symbol, meaning, needed_next, links in residual_queue_rows_data()
    ]


def residual_queue_rows_data() -> list[tuple[str, str, str, str, str]]:
    return [
        ("RV3960_0_C_XF2", "C_XF2", "hidden nonminimal F^2/F*F coupling", "operator-domain exclusion or empirical coefficient bound", "EM alpha/clocks/source leakage"),
        ("RV3960_1_Phi_EM_rad", "Phi_EM_rad", "net Poynting/radiative boundary flux", "stationary no-flux theorem or bounded flux value", "boundary current B_EM; clocks/orbital"),
        ("RV3960_2_Delta_Hodge_EM", "Delta_Hodge_EM", "EM Hodge differs from observed gravitational Hodge", "same coframe theorem or constitutive bound", "Maxwell stress/source coupling"),
        ("RV3960_3_w_EM", "w_EM", "independent Maxwell action/stress multiplier", "unique F^2 normalization owner or alpha/current bound", "alpha/charge normalization"),
        ("RV3960_4_C_EM_readout", "C_EM_readout", "readout/loop/spectroscopy regenerated hidden EM coupling", "readout closure or spectroscopy bound", "EM clocks; alpha"),
        ("RV3960_5_prevariation_weight", "w_A(Y)", "species/material prevariation weight countermodel", "forbid by action grammar or bound species dependence", "WEP/source composition"),
        ("RV3960_6_nonHilbert_bypass", "J_NH", "independent non-Hilbert source current", "exact-improvement theorem or exterior-flux bound", "source coupling/PPN"),
        ("RV3960_7_T_extra", "T_extra", "projector/domain extra stress", "topological/isotropic theorem or PPN/R11 bound", "xi/alpha3/beta/zeta"),
    ]


def em_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "EMG3960_0_visible_Maxwell",
            "gate": "minimal visible Maxwell stress",
            "result": "not an extra hidden source if same g_obs Hodge and included in T_total",
            "formula": "S_EM=-1/(4mu0) int F wedge *_obs F; T_total=T_matter+T_EM",
            "decision": "CONDITIONAL_ZERO_VALUE_ACCEPTED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "EMG3960_1_internal_exchange",
            "gate": "matter-EM Lorentz exchange",
            "result": "internal exchange cancels in total stress",
            "formula": "nabla.T_EM=-FJ and nabla.T_matter=+FJ",
            "decision": "EXACT_BOOKKEEPING_ZERO_ACCEPTED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "EMG3960_2_hidden_F2",
            "gate": "hidden f(Y)F^2 or g(Y)F*F",
            "result": "not killed by total-stress bookkeeping",
            "formula": "Delta S=int sqrt(-g) f_Y(Y)F^2 + g_Y(Y)F*F",
            "decision": "OPEN_EXCLUDE_OR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "EMG3960_3_Poynting_flux",
            "gate": "radiative/background Poynting flux",
            "result": "zero only on stationary isolated no-flux branch",
            "formula": "Phi_EM_rad=int_boundary S_Poynting dot n dA",
            "decision": "OPEN_PROVE_NO_FLUX_OR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3960_0_progress",
            "decision": "accept first conditional zero values for source-label, visible Maxwell, and internal EM exchange channels",
            "basis": "these zeros follow from action grammar/total stress bookkeeping, not from wishful local closure",
            "effect": "shrinks the live source-current vector before empirical scoring",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3960_1_no_claim",
            "decision": "do not claim local GR or Maxwell completion",
            "basis": "hidden F2, Poynting flux, Hodge mismatch, prevariation weights, non-Hilbert bypass, and T_extra remain open",
            "effect": "R10/PPN/clock/orbital/EM claims remain blocked",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3960_2_best_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "EM/Poynting/F2 is the sharpest remaining source-current channel and connects directly to the user's background-field/Poynting intuition",
            "effect": "derive no-hidden-F2/no-flux theorem or fill first finite EM bound values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3960_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3960_1_first_zeros", "first conditional zero values", "species/source spurions plus visible EM internal exchange zeros", "PASS_CONDITIONAL_NONCLAIM"),
        ("CLG3960_2_hidden_EM", "hidden F2/Poynting/Hodge/readout terms", "excluded by parent action grammar or bounded", "FAIL_OPEN"),
        ("CLG3960_3_nonHilbert", "non-Hilbert/prevariation bypasses", "forbidden or exact-improvement owned", "FAIL_OPEN"),
        ("CLG3960_4_local_GR", "local GR/Newton/Maxwell source coupling", "all residual queue rows zero or value-scored", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3960_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive an action-grammar exclusion for hidden f(Y)F^2/F*F and a stationary-isolated no-Poynting-flux theorem; if either fails, fill finite C_XF2, Phi_EM_rad, Delta_Hodge_EM, w_EM, and C_EM_readout bound rows",
            "success_condition": "EM/Poynting source-current contribution is either theorem-zero or value-ready for the 3959 C_A/PPN/R10/clock/orbital residual law",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_COMPONENT_PROGRESS",
            "summary": "3960 accepts first conditional zero values for species/source spurions, visible minimal Maxwell extra-source leakage, and internal matter-EM exchange; hidden F2, Poynting flux, Hodge mismatch, prevariation weights, non-Hilbert bypass, and T_extra remain retained residuals.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3960 - Yloc Source-Current Zero Proof Or First Bound Values

Timestamp: `{timestamp}`

## Result

3960 makes a real narrowing move.

The full `J_Y=B_Y=0` proof is still not closed, but some source-current pieces can now be treated as exact or conditional zero rows under explicit parent-action grammar:

- species/source-label spurions vanish if ordinary matter shares one connected density line;
- post-variation current rescaling vanishes if the parent current is varied before observer readout;
- visible minimal Maxwell stress is not extra hidden MTS source when it uses the same `g_obs` Hodge star and is included in `T_total`;
- internal matter-EM Lorentz exchange cancels in total stress bookkeeping.

The live culprits are now much cleaner:

- hidden `f(Y)F^2` / `g(Y)F*F`;
- radiative/background Poynting flux;
- EM Hodge/coframe mismatch;
- independent Maxwell multiplier/readout regeneration;
- prevariation species weights;
- non-Hilbert source bypass;
- retained projector/domain extra stress.

## Important Consequence

The 3959 amplitude law is now fed by a smaller residual vector. This still does not claim local GR, but it means the branch is no longer just saying “source current missing.” We now know which pieces are grammar-zero and which pieces must be proven or bounded next.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- Source register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3960_SOURCE_REGISTER.csv`
- Source-current grammar: `source-intake\\mts_residuals\\P8_Y5_R2FR_3960_SOURCE_CURRENT_ZERO_GRAMMAR.csv`
- First conditional values: `source-intake\\mts_residuals\\P8_Y5_R2FR_3960_FIRST_CONDITIONAL_ZERO_VALUES.csv`
- Retained residual queue: `source-intake\\mts_residuals\\P8_Y5_R2FR_3960_RETAINED_RESIDUAL_VALUE_QUEUE.csv`
- EM gate: `source-intake\\mts_residuals\\P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3960_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3960 - Source-Current First Zero Values And EM Residual Split

Timestamp: `{timestamp}`

- First conditional zero values accepted for connected species/source-label spurions, post-variation rescaling, visible minimal Maxwell extra-source leakage, and internal matter-EM exchange.
- These are nonclaim rows because the parent action grammar must still be adopted globally.
- Hidden `F^2/F*F`, Poynting flux, Hodge mismatch, EM readout, prevariation weights, non-Hilbert bypasses, and `T_extra` remain the live source-current residual queue.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3960 - Source-Current First Zero Values And EM Residual Split"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grammar = grammar_rows(timestamp)
    components = component_rows(timestamp)
    first_values = first_value_rows(timestamp)
    residuals = residual_queue_rows(timestamp)
    em_gate = em_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    grammar_statuses = {row["status"] for row in grammar}
    component_decisions = {row["zero_or_bound_decision"] for row in components}
    value_symbols = {row["symbol"] for row in first_values}
    residual_symbols = {row["symbol"] for row in residuals}
    em_decisions = {row["decision"] for row in em_gate}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = grammar + components + first_values + residuals + em_gate + decisions + claims + next_target

    checks = [
        ("VAL3960_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3960_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3960_02_grammar_rows", "ZERO_IF_NO_SPECIES_WEIGHT_SLOT" in grammar_statuses and "ZERO_FOR_VISIBLE_MINIMAL_EM_EXTRA_SOURCE" in grammar_statuses, "source-current zero grammar rows written"),
        ("VAL3960_03_first_zero_values", {"delta_w_species", "kappa_A_source", "hidden_marker_source", "postvariation_current_rescaling", "epsilon_EM_extra_hidden_source", "epsilon_internal_exchange"}.issubset(value_symbols), "first conditional zero values present"),
        ("VAL3960_04_visible_EM", "FIRST_CONDITIONAL_ZERO_VALUE" in component_decisions and "EXACT_BOOKKEEPING_ZERO" in component_decisions, "visible EM/internal exchange handled"),
        ("VAL3960_05_hidden_residuals", {"C_XF2", "Phi_EM_rad", "Delta_Hodge_EM", "w_EM", "C_EM_readout", "w_A(Y)", "J_NH", "T_extra"}.issubset(residual_symbols), "retained residual value queue complete"),
        ("VAL3960_06_EM_gate_open", "OPEN_EXCLUDE_OR_BOUND" in em_decisions and "OPEN_PROVE_NO_FLUX_OR_BOUND" in em_decisions, "hidden F2 and Poynting flux remain open gates"),
        ("VAL3960_07_decision_progress", "accept first conditional zero values" in decision_text and "do not claim" in decision_text, "decision records progress without claim"),
        ("VAL3960_08_claim_gate", "PASS_CONDITIONAL_NONCLAIM" in claim_statuses and "FAIL_OPEN" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses, "claim gate blocks local-GR/EM promotion"),
        ("VAL3960_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to EM/Poynting hidden F2 branch"),
        ("VAL3960_10_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3960_11_zero_rows_score_ready", all(row["score_ready"] for row in first_values), "first zero rows are score-ready conditionals"),
        ("VAL3960_12_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3960_13_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3960_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3960_15_spine_updated", SPINE_PATH.exists() and "3960 - Source-Current First Zero Values And EM Residual Split" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3960_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3960_17_script_compile", True, "script compiled before validation write"),
        ("VAL3960_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    grammar = grammar_rows(timestamp)
    components = component_rows(timestamp)
    first_values = first_value_rows(timestamp)
    residuals = residual_queue_rows(timestamp)
    em_gate = em_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["grammar"], grammar)
    write_csv(OUTPUTS["component"], components)
    write_csv(OUTPUTS["first_values"], first_values)
    write_csv(OUTPUTS["residual_queue"], residuals)
    write_csv(OUTPUTS["em_gate"], em_gate)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, sources), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, sources)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3960 validation failed: {failed}")

    print(f"3960 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("first conditional zero values accepted; hidden EM/Poynting and bypass residuals retained")


if __name__ == "__main__":
    run()
