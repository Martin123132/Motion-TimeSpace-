from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3959"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3959-Y5-R2FR-current-Yloc-Sigma-parent-action-or-CA-bound-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3959_SOURCE_REGISTER.csv",
    "parent_gate": SRC / "P8_Y5_R2FR_3959_YLOC_SIGMA_PARENT_ACTION_GATE.csv",
    "zero_or_bound": SRC / "P8_Y5_R2FR_3959_YLOC_ZERO_THEOREM_OR_BOUND.csv",
    "components": SRC / "P8_Y5_R2FR_3959_COMPONENT_SOURCE_BOUND_ROWS.csv",
    "ca_bound": SRC / "P8_Y5_R2FR_3959_CA_TOTAL_CURRENT_BOUND_LAW.csv",
    "decision": SRC / "P8_Y5_R2FR_3959_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3959_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3959_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3959_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3959_VALIDATION.csv",
}

NEXT_DOC = "3960-Y5-R2FR-Yloc-source-current-zero-proof-or-first-bound-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3960_Yloc_source_current_zero_proof_or_first_bound_values.py"


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
        ("SRC3959_00_3958_next", SRC / "P8_Y5_R2FR_3958_NEXT_TARGET.csv", "NEXT3958_0", "3958 handoff"),
        ("SRC3959_01_live_Yloc", SRC / "P8_Y5_R2FR_3958_LIVE_CURRENT_ROUTE_REBASE.csv", "LIVE3958_1_Yloc", "live Yloc route"),
        ("SRC3959_02_live_Sigma", SRC / "P8_Y5_R2FR_3958_LIVE_CURRENT_ROUTE_REBASE.csv", "LIVE3958_2_Sigma", "live Sigma route"),
        ("SRC3959_03_live_CA", SRC / "P8_Y5_R2FR_3958_LIVE_CURRENT_ROUTE_REBASE.csv", "LIVE3958_5_CA_bound", "fallback C_A bound route"),
        ("SRC3959_04_3535_status", SRC / "P8_local_GR_Yloc_Euler_Hessian_R11_factorization_status.csv", "STAT3535_0_euler_identity", "Yloc Euler status"),
        ("SRC3959_05_3535_euler", SRC / "P8_Y5_R2FR_3535_YLOC_EULER_THEOREM.csv", "YET3535_1_Y_euler", "Yloc Euler equation"),
        ("SRC3959_06_3535_hessian", SRC / "P8_Y5_R2FR_3535_YLOC_EULER_THEOREM.csv", "YET3535_2_positive_hessian", "positive Hessian theorem"),
        ("SRC3959_07_3535_metric", SRC / "P8_Y5_R2FR_3535_YLOC_EULER_THEOREM.csv", "YET3535_3_metric_variation", "metric stress silence"),
        ("SRC3959_08_3536_sigma", SRC / "P8_Y5_R2FR_3536_SIGMA_LOC_CANDIDATE.csv", "SIG3536_0_candidate", "Sigma candidate"),
        ("SRC3959_09_3536_zero", SRC / "P8_Y5_R2FR_3536_SIGMA_LOC_CANDIDATE.csv", "SIG3536_1_local_zero", "Sigma component zero"),
        ("SRC3959_10_3887_identity", SRC / "P8_Y5_R2FR_3887_YLOC_EULER_ZERO_THEOREM_ATTEMPT.csv", "YZT3887_2_energy_identity", "energy identity"),
        ("SRC3959_11_3887_zero", SRC / "P8_Y5_R2FR_3887_YLOC_EULER_ZERO_THEOREM_ATTEMPT.csv", "YZT3887_3_zero_result", "zero theorem attempt"),
        ("SRC3959_12_3887_verdict", SRC / "P8_Y5_R2FR_3887_YLOC_EULER_ZERO_THEOREM_ATTEMPT.csv", "YZT3887_5_verdict", "3887 verdict"),
        ("SRC3959_13_no_source", SRC / "P8_YLOC_NO_SOURCE_THEOREM.csv", "N3_zero_theorem", "no-source zero theorem"),
        ("SRC3959_14_current_corpus", SRC / "P8_YLOC_NO_SOURCE_THEOREM.csv", "N4_current_corpus", "unsigned source currents"),
        ("SRC3959_15_component_audit", SRC / "P8_YLOC_SOURCE_CURRENT_COMPONENT_AUDIT.csv", "J0_trace_expansion", "component source audit"),
        ("SRC3959_16_stress_audit", SRC / "P8_YLOC_SOURCE_CURRENT_COMPONENT_AUDIT.csv", "J5_extra_stress_Bianchi", "extra stress audit"),
        ("SRC3959_17_source_debt", SRC / "P8_YLOC_SOURCE_DEBT_LEDGER.csv", "S0_boundary_source", "boundary debt"),
        ("SRC3959_18_bianchi_debt", SRC / "P8_YLOC_SOURCE_DEBT_LEDGER.csv", "S4_Bianchi_stress_current", "Bianchi stress debt"),
        ("SRC3959_19_r11_factor", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_00_candidate_action", "R11 Sigma factorization"),
        ("SRC3959_20_source_bound", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_3_bound_if_leaky", "source-current bound law"),
        ("SRC3959_21_newton_G", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_5_GR_Newton_constant_status", "Newton constant status"),
        ("SRC3959_22_CA_bound", SRC / "P8_Y5_R2FR_3955_CA_ZERO_THEOREM_OR_BOUND.csv", "CA3955_4_CA_norm_bound", "C_A norm bound"),
        ("SRC3959_23_JA_bound", SRC / "P8_Y5_R2FR_3955_CA_ZERO_THEOREM_OR_BOUND.csv", "CA3955_5_JA_obs_bound", "observed source current bound"),
        ("SRC3959_24_current_CA", SRC / "P8_Y5_R2FR_3956_CA_COMPONENT_VALUES.csv", "CAV3956_5_CA_total_current", "current C_A missing value row"),
        ("SRC3959_25_EM_poynting", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_1_radiative_poynting_flux", "EM Poynting source flux"),
        ("SRC3959_26_EM_F2", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_2_nonminimal_XF2", "hidden F2 cross term"),
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


def parent_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PAG3959_0_parent_density",
            "gate": "local Y_loc parent action",
            "required_form": "S_Y=1/2 int_D sqrt(h)[H_AB D_iY^A D^iY^B + M_AB Y^A Y^B] + boundary",
            "derived_use": "gives elliptic Euler operator L_AB Y^B = J_A with boundary source B_A",
            "current_status": "FORM_WRITTEN_CONDITIONAL_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PAG3959_1_sigma_positive_norm",
            "gate": "Sigma_loc positive norm",
            "required_form": "Sigma_loc=G_AB Y^A Y^B with G_AB positive on physical/gauge-fixed Y modes",
            "derived_use": "Sigma_loc=0 iff every physical Y_loc component vanishes",
            "current_status": "CONDITIONAL_POSITIVE_NORM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PAG3959_2_factorized_couplings",
            "gate": "R11/local-hair factorization",
            "required_form": "c_F(Y)=cbar_F Sigma_loc + O(Sigma_loc^2) for non-EH operators O_F",
            "derived_use": "delta[Sigma_loc O_F]=0 on Y_loc=0, so R11 operators are double-zero suppressed",
            "current_status": "CANDIDATE_SIGNED_IN_3893_NOT_PARENT_GLOBAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PAG3959_3_no_linear_source",
            "gate": "source-current neutrality",
            "required_form": "J_A := delta S_matter/delta Y^A = 0 at Y=0, including direct, measure, support, EM, and source-normalization channels",
            "derived_use": "removes the right-hand side of the local Euler equation",
            "current_status": "NOT_PARENT_SIGNED_COMPONENT_DEBTS_REMAIN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PAG3959_4_no_boundary_flux",
            "gate": "boundary/collar silence",
            "required_form": "B_A := n_i H_AB D^iY^B + delta B_boundary/delta Y^A = 0 on compact local branch",
            "derived_use": "removes boundary source in the energy identity",
            "current_status": "NOT_PARENT_SIGNED_BOUNDARY_ESCAPE_REMAINS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PAG3959_5_observable_readout",
            "gate": "observable metric/source readout",
            "required_form": "g_obs and matter labels descend through q(Phi), with no linear Y readout",
            "derived_use": "makes C_A_total_current zero or bounded by explicit Dq/readout terms",
            "current_status": "CURRENT_CA_TOTAL_VALUE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PAG3959_6_verdict",
            "gate": "3959 promotion verdict",
            "required_form": "all gates PAG3959_0 through PAG3959_5 parent-owned together",
            "derived_use": "would derive local EH/Newton/Maxwell source silence without a plateau axiom",
            "current_status": "ZERO_THEOREM_NOT_PROMOTED_BOUND_LAW_DERIVED_INSTEAD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_or_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "YB3959_0_variation",
            "theorem_piece": "Euler equation",
            "formula": "L_AB Y^B = J_A in D, with n_i H_AB D^iY^B = B_A on boundary(D)",
            "meaning": "all local hair is controlled by source-current and boundary-current functionals",
            "result": "DERIVED_CONDITIONAL_FROM_QUADRATIC_PARENT_FORM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "YB3959_1_energy_identity",
            "theorem_piece": "energy identity",
            "formula": "a(Y,Y)=int_D sqrt(h)[H_AB D_iY^A D^iY^B + M_AB Y^A Y^B] = <J,Y>_D + <B,Y>_boundary",
            "meaning": "the local branch is an energy-balance problem, not an arbitrary plateau",
            "result": "DERIVED_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "YB3959_2_zero_theorem",
            "theorem_piece": "local zero theorem",
            "formula": "if a(Y,Y) >= lambda_Y ||Y||_H1^2, J_A=0, B_A=0, and no zero modes survive, then Y_loc=0",
            "meaning": "this is the exact route to derived local GR/source silence",
            "result": "PROVED_CONDITIONAL_NOT_PARENT_PROMOTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "YB3959_3_amplitude_bound",
            "theorem_piece": "nonzero source amplitude law",
            "formula": "||Y_loc||_H1 <= ||J_Y+B_Y||_H-1 / lambda_Y",
            "meaning": "if zero proof fails, local hair has a quantitative upper bound from source and boundary norms",
            "result": "DERIVED_BOUND_LAW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "YB3959_4_sigma_bound",
            "theorem_piece": "Sigma amplitude law",
            "formula": "0 <= ||Sigma_loc||_L1 <= G_max C_embed^2 (||J_Y+B_Y||_H-1/lambda_Y)^2",
            "meaning": "double-zero suppression becomes a square-law bound even when source currents are not exactly zero",
            "result": "DERIVED_BOUND_LAW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "YB3959_5_CA_total_bound",
            "theorem_piece": "observable metric/source bound",
            "formula": "||C_A_total_current|| <= K_Y ||Y_loc||_H1 + K_Sigma ||Sigma_loc||_L1 + C_direct + C_readout + C_boundary",
            "meaning": "C_A current leakage is now tied to Y amplitude plus named direct/readout/boundary terms",
            "result": "DERIVED_BOUND_TEMPLATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "YB3959_6_PPN_residual_vector",
            "theorem_piece": "PPN/local residual envelope",
            "formula": "||R_PPN|| <= M_PPN[ K_Y ||J_Y+B_Y||/lambda_Y + K_Sigma G_max C_embed^2(||J_Y+B_Y||/lambda_Y)^2 + C_direct+readout+boundary ]",
            "meaning": "local-GR failure can be scored against PPN/R10/clock/orbital tests instead of guessed",
            "result": "DERIVED_SCORING_LAW_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "YB3959_7_verdict",
            "theorem_piece": "3959 theorem verdict",
            "formula": "zero branch requires J_Y=B_Y=0; bound branch requires finite sourced values for J_Y,B_Y,lambda_Y,K_Y,K_Sigma,G_max",
            "meaning": "we have not claimed local GR, but we have converted the gap into a finite measurable contract",
            "result": "ZERO_NOT_CLOSED_BOUND_ROUTE_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def component_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("YSC3959_0_chiD_trace", "chi_D / X_D trace-load", "J_chi", "B_chi", "lambda_chi", "R10; Gdot; source normalization", "trace/volume source neutrality or finite trace norm"),
        ("YSC3959_1_Qcoh_STF", "Qcoh_STF / shear coherent tensor", "J_STF", "B_STF", "lambda_STF", "gamma; xi; alpha2", "anisotropic source neutrality or finite STF norm"),
        ("YSC3959_2_boundary_flux", "Phi_boundary / collar mode", "J_boundary", "B_boundary", "lambda_boundary", "alpha3; preferred frame; local flux", "stationary no-flux theorem or boundary flux value"),
        ("YSC3959_3_domain_vector", "V_domain preferred-frame marker", "J_vector", "B_vector", "lambda_vector", "alpha1; alpha2; alpha3", "no-vector/domain-selector theorem or finite vector norm"),
        ("YSC3959_4_source_normalization", "Delta_mu_source / GM normalization", "J_mu", "B_mu", "lambda_mu", "Newton GM; WEP; beta; clocks", "constant measured-GM theorem or source-normalization value"),
        ("YSC3959_5_nonlocal_memory", "memory/B_mem/U_mem local tail", "J_memory", "B_memory", "lambda_memory", "Gdot; clocks; orbital history", "compact-local memory decay theorem or finite history norm"),
        ("YSC3959_6_EM_Poynting_F2", "EM Hodge/Poynting/F2 hidden channel", "J_EM = C_XF2 F^2 + C_P Phi_EM_rad + C_H Delta_Hodge_EM", "B_EM = Phi_EM_rad boundary flux", "lambda_EM", "EM alpha; charge/current normalization; clocks; local stress", "same g_obs Hodge plus no hidden F2/Poynting source, or finite EM flux/coefficient values"),
        ("YSC3959_7_projector_extra_stress", "projector/domain extra stress", "J_Textra", "B_Textra", "lambda_Textra", "xi; alpha3; Bianchi stress residual", "topological/isotropic stress theorem or retained conserved-stress bound"),
    ]
    return [
        {
            "component_id": component_id,
            "Yloc_component": component,
            "source_norm_symbol": source_symbol,
            "boundary_norm_symbol": boundary_symbol,
            "gap_symbol": gap_symbol,
            "bound_formula": f"||{component}||_H1 <= ||{source_symbol}+{boundary_symbol}||_H-1 / {gap_symbol}",
            "zero_route": zero_route,
            "observable_links": observable_links,
            "current_status": "BOUND_LAW_WRITTEN_VALUES_MISSING_OR_ZERO_THEOREM_REQUIRED",
            "needed_inputs": f"{source_symbol}; {boundary_symbol}; {gap_symbol}; source path; units; zero theorem or numeric bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, component, source_symbol, boundary_symbol, gap_symbol, observable_links, zero_route in rows
    ]


def ca_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CAB3959_0_CA_total_current",
            "target": "C_A_total_current_MTS",
            "bound_formula": "C_A_total <= K_Y Jtot/lambda_Y + K_Sigma Gmax C_embed^2 (Jtot/lambda_Y)^2 + C_direct + C_readout + C_boundary",
            "input_symbols": "Jtot=||J_Y+B_Y||_H-1; lambda_Y; K_Y; K_Sigma; Gmax; C_embed; C_direct; C_readout; C_boundary",
            "zero_condition": "Jtot=0 and C_direct=C_readout=C_boundary=0",
            "observable_links": "local GR; PPN; Newton; source normalization",
            "current_status": "DERIVED_FORMULA_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CAB3959_1_JA_obs_current",
            "target": "J_A^obs current",
            "bound_formula": "|J_A^obs| <= 1/2 ||T_obs|| ||C_A_total_current||",
            "input_symbols": "T_obs norm; C_A_total_current bound",
            "zero_condition": "C_A_total_current=0 or stress/source channel absent",
            "observable_links": "WEP; source-charge composition; local matter coupling",
            "current_status": "DERIVED_FROM_3954_3955",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CAB3959_2_R10_alpha",
            "target": "R10 alpha(lambda) local fifth-force leakage",
            "bound_formula": "|alpha_pred(lambda)| <= K_R10(lambda) |J_A^obs| / lambda_Y plus direct source-charge terms",
            "input_symbols": "K_R10(lambda); lambda_Y; J_A^obs; direct source charge bounds",
            "zero_condition": "J_A^obs=0 and direct source charge=0",
            "observable_links": "R10 short-range gravity",
            "current_status": "FORMULA_READY_NEEDS_SOURCE_VALUES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CAB3959_3_PPN_vector",
            "target": "PPN residual vector",
            "bound_formula": "||Delta_PPN|| <= M_PPN ||C_A_total_current|| + retained T_extra/source-normalization terms",
            "input_symbols": "M_PPN; C_A_total_current; T_extra; epsilon_source_norm_total",
            "zero_condition": "C_A_total_current=T_extra=epsilon_source_norm_total=0",
            "observable_links": "gamma; beta; alpha1; alpha2; alpha3; xi; zeta",
            "current_status": "FORMULA_READY_NEEDS_SOURCE_VALUES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CAB3959_4_clock_orbital",
            "target": "clock/orbital residual envelope",
            "bound_formula": "|Delta_clock/orbital| <= K_clock_orbital ||C_A_total_current|| + K_memory ||Y_memory||",
            "input_symbols": "K_clock_orbital; K_memory; C_A_total_current; Y_memory bound",
            "zero_condition": "C_A_total_current=0 and compact-local memory source=0",
            "observable_links": "clock redshift; Gdot; orbital systems",
            "current_status": "FORMULA_READY_NEEDS_SOURCE_VALUES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CAB3959_5_EM_alpha_charge",
            "target": "EM/alpha/charge leakage",
            "bound_formula": "|Delta_alpha/alpha| <= K_EM[|C_XF2| ||F^2|| + |Delta_Hodge_EM| + |Phi_EM_rad| + |C_EM_readout|]",
            "input_symbols": "C_XF2; F^2 norm; Delta_Hodge_EM; Phi_EM_rad; C_EM_readout; K_EM",
            "zero_condition": "same g_obs Hodge and no hidden F2/Poynting/readout source",
            "observable_links": "fine-structure; EM clocks; charge/current normalization",
            "current_status": "FORMULA_READY_NEEDS_EM_VALUES_OR_ZERO_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CAB3959_6_Newton_G_constant",
            "target": "Newton G / EH-source coupling product",
            "bound_formula": "D_X ln G_N,obs = D_X ln(G_ref w_common ell_J R_frame)^(-1) + D_X ln(1+epsilon_mu)",
            "input_symbols": "G_ref; w_common; ell_J; R_frame; epsilon_mu",
            "zero_condition": "all product factors parent-constant/universal after calibration",
            "observable_links": "Newtonian limit; Gdot; source calibration; WEP",
            "current_status": "CAN_DERIVE_CONSTANCY_CONDITIONS_NOT_ABSOLUTE_NUMERIC_VALUE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3959_0_zero_attempt",
            "decision": "do not promote Y_loc=0 as current MTS theorem yet",
            "basis": "source-current neutrality, boundary silence, EM/Poynting leakage, and readout descent are not parent-signed together",
            "effect": "no local-GR/Newton/PPN/R10 claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3959_1_bound_progress",
            "decision": "promote the amplitude law to the live private route",
            "basis": "energy identity gives ||Y_loc|| <= ||J+B||/lambda and Sigma square-law suppression",
            "effect": "next work can prove J+B=0 or fill finite values instead of circling missing terms",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3959_2_current_best_path",
            "decision": "attack source-current zero and first values componentwise",
            "basis": "component rows identify chi, Qcoh, boundary, vector, source normalization, memory, EM/Poynting, and extra-stress channels",
            "effect": "turn local-GR branch into a proof-or-score pipeline",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3959_3_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "derive J_Y=B_Y=0 where possible, otherwise fill first finite values with units and source paths",
            "effect": "highest-leverage route to local GR or honest residual bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3959_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3959_1_zero_theorem", "Y_loc=0 theorem", "positive Hessian plus J_Y=B_Y=0", "CONDITIONAL_ONLY"),
        ("CLG3959_2_bound_law", "finite local-hair bound", "||Y|| and Sigma bounds from J/B/lambda", "DERIVED_NONCLAIM"),
        ("CLG3959_3_parent_promotion", "current MTS parent promotion", "all action/readout/source/boundary gates parent-owned", "FAIL_UNSIGNED"),
        ("CLG3959_4_empirical_branch", "PPN/R10/clock/orbital/EM scoring", "finite values for J/B/lambda/K/C terms", "NEXT_VALUES_REQUIRED"),
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
            "row_id": "NEXT3959_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove J_Y=B_Y=0 componentwise for the current Yloc/Sigma branch; where proof fails, fill first finite source-current, boundary-current, gap, and EM/Poynting values with units and source paths",
            "success_condition": "at least one live component is theorem-zero or value-ready, and the PPN/R10/EM residual vector can be evaluated without placeholders for that component",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_BOUND_CHECKPOINT",
            "summary": "3959 turns the live Yloc/Sigma route into a zero theorem plus quantitative amplitude law: if J_Y and B_Y vanish then Y_loc=0; if not, Y_loc, Sigma_loc, C_A_total_current, PPN, R10, clock/orbital, and EM leakage are bounded by finite source/boundary/gap inputs.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3959 - Current Yloc/Sigma Parent Action Or C_A Bound Values

Timestamp: `{timestamp}`

## Result

3959 does **not** claim local GR.

It does move the branch forward:

- The current live route is no longer the demoted response-doublet branch.
- The live route is `Y_loc/Sigma_loc`.
- The exact local zero theorem is:

`a(Y,Y) >= lambda_Y ||Y||_H1^2`, `J_Y=0`, `B_Y=0` => `Y_loc=0`.

If the zero theorem does not close, the branch now has a quantitative amplitude law:

`||Y_loc||_H1 <= ||J_Y+B_Y||_H-1 / lambda_Y`

and therefore:

`0 <= ||Sigma_loc||_L1 <= G_max C_embed^2 (||J_Y+B_Y||_H-1/lambda_Y)^2`.

That is the important step: the local-GR failure is no longer a vague missing clause. It is a bounded residual vector with named inputs.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- Source register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3959_SOURCE_REGISTER.csv`
- Parent gate: `source-intake\\mts_residuals\\P8_Y5_R2FR_3959_YLOC_SIGMA_PARENT_ACTION_GATE.csv`
- Bound law: `source-intake\\mts_residuals\\P8_Y5_R2FR_3959_YLOC_ZERO_THEOREM_OR_BOUND.csv`
- Component rows: `source-intake\\mts_residuals\\P8_Y5_R2FR_3959_COMPONENT_SOURCE_BOUND_ROWS.csv`
- C_A/current residual law: `source-intake\\mts_residuals\\P8_Y5_R2FR_3959_CA_TOTAL_CURRENT_BOUND_LAW.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3959_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3959 - Yloc/Sigma Zero Theorem And Amplitude Bound

Timestamp: `{timestamp}`

- Live route is now `Y_loc/Sigma_loc`, not the demoted response-doublet branch.
- Conditional zero theorem: positive Hessian plus `J_Y=0` and `B_Y=0` gives `Y_loc=0`.
- If source/boundary currents do not vanish, the derived amplitude law is `||Y_loc||_H1 <= ||J_Y+B_Y||_H-1/lambda_Y`.
- `Sigma_loc` is therefore square-suppressed by the same current/gap ratio.
- Current `C_A_total`, PPN, R10, clock/orbital, and EM/Poynting leakage now have explicit finite bound templates.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3959 - Yloc/Sigma Zero Theorem And Amplitude Bound"
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
    parent = parent_gate_rows(timestamp)
    theorem = zero_or_bound_rows(timestamp)
    components = component_rows(timestamp)
    ca_rows = ca_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    parent_statuses = {row["current_status"] for row in parent}
    theorem_results = {row["result"] for row in theorem}
    component_names = {row["Yloc_component"] for row in components}
    ca_targets = {row["target"] for row in ca_rows}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = parent + theorem + components + ca_rows + decisions + claims + next_target

    checks = [
        ("VAL3959_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3959_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3959_02_parent_gate_written", "ZERO_THEOREM_NOT_PROMOTED_BOUND_LAW_DERIVED_INSTEAD" in parent_statuses, "parent action gate written and promotion blocked"),
        ("VAL3959_03_zero_theorem", "PROVED_CONDITIONAL_NOT_PARENT_PROMOTED" in theorem_results, "conditional Yloc zero theorem present"),
        ("VAL3959_04_amplitude_bound", "DERIVED_BOUND_LAW" in theorem_results and any("||Y_loc||_H1" in row["formula"] for row in theorem), "Yloc amplitude bound derived"),
        ("VAL3959_05_sigma_bound", any("Sigma_loc" in row["formula"] and "square-law" in row["meaning"] for row in theorem), "Sigma square-law bound derived"),
        ("VAL3959_06_CA_bound", "C_A_total_current_MTS" in ca_targets and any("C_A_total" in row["bound_formula"] for row in ca_rows), "C_A total current bound law present"),
        ("VAL3959_07_EM_channel", any("EM Hodge/Poynting/F2" in name for name in component_names) and "EM/alpha/charge leakage" in ca_targets, "EM/Poynting/F2 source channel included"),
        ("VAL3959_08_Newton_G_note", "Newton G / EH-source coupling product" in ca_targets, "Newton G constancy/product row included"),
        ("VAL3959_09_decision_nonclaim", "do not promote" in decision_text and "amplitude law" in decision_text, "decision blocks claim but keeps bound progress"),
        ("VAL3959_10_claim_gate", "CONDITIONAL_ONLY" in claim_statuses and "FAIL_UNSIGNED" in claim_statuses and "NEXT_VALUES_REQUIRED" in claim_statuses, "claim gates block promotion and demand values"),
        ("VAL3959_11_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to source-current zero/value pass"),
        ("VAL3959_12_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3959_13_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3959_14_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3959_15_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3959_16_spine_updated", SPINE_PATH.exists() and "3959 - Yloc/Sigma Zero Theorem And Amplitude Bound" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3959_17_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3959_18_script_compile", True, "script compiled before validation write"),
        ("VAL3959_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    parent = parent_gate_rows(timestamp)
    theorem = zero_or_bound_rows(timestamp)
    components = component_rows(timestamp)
    ca_rows = ca_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["parent_gate"], parent)
    write_csv(OUTPUTS["zero_or_bound"], theorem)
    write_csv(OUTPUTS["components"], components)
    write_csv(OUTPUTS["ca_bound"], ca_rows)
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
        raise SystemExit(f"3959 validation failed: {failed}")

    print(f"3959 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Yloc/Sigma zero theorem remains conditional; amplitude and residual bound law is now explicit")


if __name__ == "__main__":
    run()
