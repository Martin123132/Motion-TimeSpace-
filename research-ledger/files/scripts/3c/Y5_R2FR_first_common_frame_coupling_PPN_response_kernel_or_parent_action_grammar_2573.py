from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIRST_COMMON_FRAME_COUPLING_PPN_2573"
CHECKPOINT_ID = "2573"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2573-Y5-R2FR-first-common-frame-coupling-PPN-response-kernel-or-parent-action-grammar.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PPN_COUPLING_2573_SOURCE_REGISTER.csv",
    "parent_grammar": OUT / "P8_Y5_PPN_COUPLING_2573_PARENT_ACTION_GRAMMAR_RETRY.csv",
    "ppn_kernel": OUT / "P8_Y5_PPN_COUPLING_2573_RESPONSE_KERNEL.csv",
    "ppn_bounds": OUT / "P8_Y5_PPN_COUPLING_2573_BOUND_LEDGER.csv",
    "residual_vector": OUT / "P8_Y5_PPN_COUPLING_2573_RESIDUAL_VECTOR_INTERFACE.csv",
    "baseline_policy": OUT / "P8_Y5_PPN_COUPLING_2573_BASELINE_POLICY.csv",
    "claim_gates": OUT / "P8_Y5_PPN_COUPLING_2573_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PPN_COUPLING_2573_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PPN_COUPLING_2573_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PPN_COUPLING_2573_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2573_VALIDATION.csv",
}

COPY_TARGETS = {
    "parent_grammar": LOCAL_BOUNDS / "Parent_action_grammar_retry_2573_NONCLAIM.csv",
    "ppn_kernel": LOCAL_BOUNDS / "First_common_frame_coupling_PPN_response_kernel_2573_NONCLAIM.csv",
    "ppn_bounds": LOCAL_BOUNDS / "PPN_bound_ledger_2573_NONCLAIM.csv",
    "residual_vector": LOCAL_BOUNDS / "PPN_coupling_residual_vector_interface_2573_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2573_DELTA_P_BETA_DISFORMAL_COUPLING_PPN_VECTOR_OR_PARENT_GRAMMAR.csv",
}

SOURCES = [
    {
        "source_id": "SRC2573_00_2572_handoff",
        "source_path": ROOT / "2572-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
        "needles": ["NEXT2572_0_selected", "KER2572_0_PPN_metric_coupling", "VAL2572_OVERALL"],
        "role": "active handoff selecting parent action grammar or common-frame/coupling PPN response kernel",
    },
    {
        "source_id": "SRC2573_01_2489_precedent",
        "source_path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": ["PPNK2489_0_conformal_gamma_kernel", "PPNV2489_7_total_abs", "VAL2489_OVERALL"],
        "role": "earlier PPN gamma kernel and no-cancellation vector precedent",
    },
    {
        "source_id": "SRC2573_02_1881_gamma_kernel",
        "source_path": ROOT / "1881-Y5-R2FR-first-common-frame-response-kernel-or-parent-action-clause.md",
        "needles": ["RKR1881_0_C_R_conformal_PPN_gamma", "PGB1881_0_Cassini_gamma_to_sR", "VAL1881_OVERALL"],
        "role": "conformal-to-PPN-gamma response kernel and Cassini bridge",
    },
    {
        "source_id": "SRC2573_03_1882_cr_profile",
        "source_path": ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md",
        "needles": ["CRID1882_0_definitions", "SNCM1882_1_generalized_gamma", "VAL1882_OVERALL"],
        "role": "C_R weak-field identity and delta_p/b_R combination law",
    },
    {
        "source_id": "SRC2573_04_1883_full_vector",
        "source_path": ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md",
        "needles": ["FULL_PPN_RESIDUAL_VECTOR_BUILT_NONCLAIM", "PBOUND1883_1_beta", "VAL1883_OVERALL"],
        "role": "full PPN residual vector and gamma-only refusal precedent",
    },
    {
        "source_id": "SRC2573_05_2160_vector_envelope",
        "source_path": ROOT / "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md",
        "needles": ["PPV2160_6_total_abs_guard", "PBC2160_4_multi_component", "VAL2160_OVERALL"],
        "role": "PPN no-cancellation vector envelope and coupling/common-frame translation guard",
    },
    {
        "source_id": "SRC2573_06_2322_tau_ppn",
        "source_path": ROOT / "2322-Y5-R2FR-tau-PPN-or-common-frame-parent-signature.md",
        "needles": ["TPA2322_1_tau_standard_scalar_tensor", "SIG2322_4_ppn_gauge_source", "VAL2322_OVERALL"],
        "role": "tau_PPN normalization and readout/gauge/source blocker",
    },
    {
        "source_id": "SRC2573_07_ppn_contract",
        "source_path": OUT / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_2_spatial_curvature_gamma", "MEX524_3_gravitomagnetic_preferred_frame", "MEX524_6_no_cancellation_PPN_envelope"],
        "role": "baseline PPN metric expansion contract",
    },
    {
        "source_id": "SRC2573_08_local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["Cassini_Shapiro_gamma_2003", "Will_2014_PPN_beta_table", "Will_2014_PPN_alpha1_table"],
        "role": "source-backed local comparator bounds",
    },
    {
        "source_id": "SRC2573_09_2572_validation",
        "source_path": OUT / "P8_Y5_BRR545_2572_VALIDATION.csv",
        "needles": ["VAL2572_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def parent_grammar_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "grammar_id": "PAG2573_0_ordinary_sector_signature",
            "candidate_grammar": "S_ord = S_EH[e_pub,kappa_bar] + S_matter[Psi,e_pub,theta_pub,cbar] + S_boundary[e_pub] with e_pub=E(Q_vis)",
            "attempt_result": "NOT_PARENT_SIGNED",
            "reason": "2572 supplies the exact contract, but the current parent normal form still does not prove E(Q_vis), kappa_bar, ell_bar or cbar as typed primitive/derived slots",
            "effect_if_signed": "forbids hidden coframe/source/coupling arguments before PPN projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "grammar_id": "PAG2573_1_no_shadow_slots",
            "candidate_grammar": "Allowed[S_ord,Obs] excludes E(Q_vis,C_R,J_q), A_R(C_R,J_q), B_R(C_R,J_q), w_A(C_R,J_q), kappa(C_R,J_q), ell_J(C_R,J_q)",
            "attempt_result": "CLOSURE_CONTRACT_ONLY",
            "reason": "covariance, WEP, Ward and same-frame language still allow universal hidden common-frame and source-scale countermodels",
            "effect_if_signed": "sets b_R,d_R,w_R,epsilon_endpoint_R,Dln_kappa,Dln_ellJ to theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "grammar_id": "PAG2573_2_fixed_before_readout",
            "candidate_grammar": "kappa_MTS, ell_J, source support, PPN gauge and GM convention are fixed before empirical baselines are used",
            "attempt_result": "GUARDRAIL_ACTIVE_NOT_THEOREM",
            "reason": "the guardrail prevents circular scoring, but it is not itself a parent derivation of coupling ownership",
            "effect_if_signed": "prevents fitted GM/H0 from absorbing a local coupling/source leak",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "grammar_id": "PAG2573_3_verdict",
            "candidate_grammar": "typed parent ordinary-sector action grammar closes local no-shadow/coupling branch",
            "attempt_result": "PARENT_ACTION_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "terminal object, no-extra-slot grammar, EH/coupling origin, coefficient descent and source inheritance are still unsigned",
            "effect_if_signed": "would make the first PPN response kernel unnecessary for these components",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def ppn_kernel_rows() -> list[dict[str, Any]]:
    cassini_bound = 2.3e-5
    s_bound = cassini_bound / (2.0 + cassini_bound)
    rows = [
        {
            "kernel_id": "PPNK2573_0_gamma_common_frame_combo",
            "observable": "gamma_minus_1",
            "bound_id": "PBOUND2573_0_gamma",
            "derived_or_schema_response": "gamma_obs_minus_1=(delta_p+4*b_R*delta_p)/(1-2*b_R*delta_p) plus additive readout/source tails",
            "linear_envelope": "|Delta_gamma| <= |delta_p*(1+4*b_R)| + K_gamma_end|epsilon_endpoint| + K_gamma_k|Dln_kappa| + K_gamma_J|Dln_ellJ| + K_gamma_readout|alpha_readout|",
            "source_bound": "Cassini |gamma-1| <= 2.3e-5; equivalently |s_R| <= %.14e for pure conformal s_R" % s_bound,
            "kernel_status": "DERIVED_SYMBOLIC_COMPARATOR_READY_NONCLAIM",
            "missing_inputs": "MISSING_delta_p;MISSING_b_R;MISSING_ENDPOINT_KERNEL;MISSING_COUPLING_RESPONSE_COEFFICIENTS;MISSING_READOUT_GAUGE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2573_1_beta_second_order_coupling",
            "observable": "beta_minus_1",
            "bound_id": "PBOUND2573_1_beta",
            "derived_or_schema_response": "Delta_beta_total = delta_beta_field + beta_source(E_norm,Dln_kappa,Dln_ellJ) + beta_projector + beta_endpoint + beta_readout",
            "linear_envelope": "|Delta_beta| <= |delta_beta_field| + K_beta_k|Dln_kappa| + K_beta_J|Dln_ellJ| + K_beta_norm|E_norm| + K_beta_proj|epsilon_projector| + K_beta_end|epsilon_endpoint|",
            "source_bound": "Will 2014 comparator |beta-1| <= 7.8e-5",
            "kernel_status": "SCHEMA_READY_RESPONSE_KERNEL_MISSING",
            "missing_inputs": "MISSING_SECOND_ORDER_FIELD_EQUATION;MISSING_SOURCE_NORMALIZATION_KERNEL;MISSING_PROJECTOR_KERNEL;MISSING_FIXED_GM_BASELINE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2573_2_alpha1_preferred_frame",
            "observable": "alpha1",
            "bound_id": "PBOUND2573_2_alpha1",
            "derived_or_schema_response": "alpha1 receives disformal/current/tau/readout legs from d_R, tau_PPN, source current drift and coupling-current exchange",
            "linear_envelope": "|alpha1| <= K_a1_d|d_R| + K_a1_tau|epsilon_tau| + K_a1_kJ|Dln(kappa_MTS*ell_J)| + K_a1_boundary|epsilon_boundary|",
            "source_bound": "Will 2014 conservative comparator |alpha1| <= 1e-4",
            "kernel_status": "SCHEMA_READY_RESPONSE_KERNEL_MISSING",
            "missing_inputs": "MISSING_DISFORMAL_ANSATZ;MISSING_VECTOR_NORMALIZATION;MISSING_TAU_PPN_MAP;MISSING_COUPLING_CURRENT_KERNEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2573_3_alpha2_preferred_frame",
            "observable": "alpha2",
            "bound_id": "PBOUND2573_3_alpha2",
            "derived_or_schema_response": "alpha2 is the ultra-tight preferred-frame/domain projection for disformal, boundary and memory-frame leaks",
            "linear_envelope": "|alpha2| <= K_a2_d|d_R| + K_a2_tau|epsilon_tau| + K_a2_mem|epsilon_memory_frame| + K_a2_boundary|epsilon_boundary|",
            "source_bound": "Will 2014 comparator |alpha2| <= 2e-9",
            "kernel_status": "SCHEMA_READY_RESPONSE_KERNEL_MISSING",
            "missing_inputs": "MISSING_DOMAIN_VECTOR;MISSING_MEMORY_FRAME_KERNEL;MISSING_BOUNDARY_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2573_4_alpha3_source_exchange",
            "observable": "alpha3",
            "bound_id": "PBOUND2573_4_alpha3",
            "derived_or_schema_response": "alpha3 is the momentum-flux/source-exchange residual from nonconservation, source prefactor and coupling-current drift",
            "linear_envelope": "|alpha3| <= K_a3_w|w_R| + K_a3_J|Dln_ellJ| + K_a3_k|Dln_kappa| + K_a3_q|q_loc_source| + K_a3_boundary|epsilon_boundary|",
            "source_bound": "Will 2014 comparator |alpha3| <= 4e-20",
            "kernel_status": "SCHEMA_READY_RESPONSE_KERNEL_MISSING",
            "missing_inputs": "MISSING_CONSERVATION_CLOSURE;MISSING_SOURCE_EXCHANGE_KERNEL;MISSING_QLOC_SOURCE_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2573_5_xi_preferred_location",
            "observable": "xi",
            "bound_id": "PBOUND2573_5_xi",
            "derived_or_schema_response": "xi tracks preferred-location/boundary/domain memory leakage",
            "linear_envelope": "|xi| <= K_xi_end|epsilon_endpoint| + K_xi_boundary|epsilon_boundary| + K_xi_mem|epsilon_memory_frame| + K_xi_proj|epsilon_projector|",
            "source_bound": "Will 2014 comparator |xi| <= 4e-9",
            "kernel_status": "SCHEMA_READY_RESPONSE_KERNEL_MISSING",
            "missing_inputs": "MISSING_ENDPOINT_SILENCE;MISSING_BOUNDARY_DOMAIN_KERNEL;MISSING_PROJECTOR_RESPONSE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def ppn_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "PBOUND2573_0_gamma",
            "dataset_id": "Cassini_Shapiro_gamma_2003",
            "observable": "gamma_minus_1",
            "upper_bound": 2.3e-5,
            "units": "dimensionless",
            "reference": "https://www.nature.com/articles/nature01997; doi:10.1038/nature01997",
            "use_in_2573": "comparator for gamma common-frame/coupling kernel only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2573_1_beta",
            "dataset_id": "Will_2014_PPN_beta_table",
            "observable": "beta_minus_1",
            "upper_bound": 7.8e-5,
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2573": "comparator only; beta response kernel still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2573_2_alpha1",
            "dataset_id": "Will_2014_PPN_alpha1_table",
            "observable": "alpha1",
            "upper_bound": 1e-4,
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2573": "preferred-frame comparator; disformal/coupling-current kernel missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2573_3_alpha2",
            "dataset_id": "Will_2014_PPN_alpha2_table",
            "observable": "alpha2",
            "upper_bound": 2e-9,
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2573": "preferred-frame comparator; domain/vector projection missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2573_4_alpha3",
            "dataset_id": "Will_2014_PPN_alpha3_table",
            "observable": "alpha3",
            "upper_bound": 4e-20,
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2573": "source-exchange comparator; conservation/source-current closure missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2573_5_xi",
            "dataset_id": "Will_2014_PPN_xi_table",
            "observable": "xi",
            "upper_bound": 4e-9,
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2573": "preferred-location comparator; boundary/domain kernel missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "PPNV2573_0_delta_p_qR",
            "symbol": "delta_p_or_q_R_hat",
            "role": "spatial-curvature/reciprocal-lock residual entering gamma and beta",
            "ppn_observables": "gamma_minus_1;beta_minus_1",
            "current_status": "MISSING_RECIPROCAL_LOCK_OR_NUMERIC_INPUT",
            "required_next_input": "derive T^2S=1/delta_p=0 or provide source-normalized delta_p/q_R_hat row",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_1_bR",
            "symbol": "b_R",
            "role": "common Weyl no-shadow coefficient",
            "ppn_observables": "gamma_minus_1 with C_R combo law",
            "current_status": "CONDITIONAL_KERNEL_READY_VALUE_MISSING",
            "required_next_input": "b_R theorem-zero from parent grammar or sourced coefficient in same normalization",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_2_kappa",
            "symbol": "Dln_kappa_MTS",
            "role": "visible gravitational coupling/source-normalization residual",
            "ppn_observables": "gamma_minus_1;beta_minus_1;alpha_i via source/readout convention",
            "current_status": "COUPLING_OWNER_UNSIGNED",
            "required_next_input": "parent EH-leading coefficient theorem or fixed-before-readout PPN/source kernel",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_3_ellJ",
            "symbol": "Dln_ell_J",
            "role": "Hilbert source-current scale residual",
            "ppn_observables": "beta_minus_1;alpha3;orbital/source normalization;possibly gamma via readout",
            "current_status": "SOURCE_SCALE_OWNER_UNSIGNED",
            "required_next_input": "ell_J parent scale/gap/tau-normalization theorem or finite response row",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_4_beta",
            "symbol": "delta_beta_total",
            "role": "second-order g00/source/operator/readout residual",
            "ppn_observables": "beta_minus_1",
            "current_status": "MISSING_BETA_RESPONSE_KERNEL",
            "required_next_input": "second-order source-normalized field equation or finite beta row",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_5_dR",
            "symbol": "d_R",
            "role": "disformal/preferred-frame shadow coefficient",
            "ppn_observables": "alpha1;alpha2;possibly gamma",
            "current_status": "MISSING_DISFORMAL_PPN_PROJECTION",
            "required_next_input": "normalized disformal ansatz and preferred-frame response matrix",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_6_wR",
            "symbol": "w_R",
            "role": "source-only matter prefactor/source normalization leak",
            "ppn_observables": "beta_minus_1;gamma_minus_1;alpha3 via source exchange",
            "current_status": "MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL",
            "required_next_input": "source-current descent/no source slot theorem or source-normalization response kernel",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_7_endpoint",
            "symbol": "epsilon_endpoint_R",
            "role": "boundary/endpoint/local projection tail",
            "ppn_observables": "xi;alpha3;orbital_light_time;gamma/beta readout tails",
            "current_status": "MISSING_ENDPOINT_SILENCE_OR_PROJECTION",
            "required_next_input": "boundary endpoint silence theorem or finite endpoint PPN/orbital kernel",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_8_readout_gauge",
            "symbol": "alpha_readout_or_delta_GM",
            "role": "post-variation PPN gauge/measured-GM calibration tail",
            "ppn_observables": "gamma_minus_1;beta_minus_1;source normalization",
            "current_status": "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION",
            "required_next_input": "fixed-before-readout and measured-GM transfer theorem or source-backed tail bound",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2573_9_total_abs",
            "symbol": "Delta_PPN_coupling_abs",
            "role": "componentwise no-cancellation envelope",
            "ppn_observables": "all_PPN",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "required_next_input": "all components theorem-zero or numerically bounded with no pair-cancellation shortcut",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def baseline_policy_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "policy_id": "BASE2573_0_fixed_before_readout",
            "rule": "kappa_MTS, ell_J, source masses, PPN gauge and orbital GM convention must be fixed before comparing to PPN bounds",
            "reason": "otherwise coupling/source leaks can be absorbed into measured GM and falsely called local GR",
            "status": "GUARDRAIL_ACTIVE_NONCLAIM",
            "failure_mode_prevented": "fitted_GM_or_H0_absorption",
            "valid_for_claim": False,
        },
        {
            "policy_id": "BASE2573_1_no_gamma_only_pass",
            "rule": "gamma cannot be scored alone while beta, alpha_i, xi, source, endpoint and coupling rows are open",
            "reason": "gamma-only or cancellation-only fits can hide disformal/source/coupling residuals",
            "status": "GUARDRAIL_ACTIVE_NONCLAIM",
            "failure_mode_prevented": "moneyball_gamma_cherrypick",
            "valid_for_claim": False,
        },
        {
            "policy_id": "BASE2573_2_no_pair_cancellation",
            "rule": "opposite-sign components do not cancel unless a parent relation fixes the cancellation",
            "reason": "local GR requires structural silence or bounded residuals, not ad hoc sign tuning",
            "status": "GUARDRAIL_ACTIVE_NONCLAIM",
            "failure_mode_prevented": "accidental_counterpunch_sold_as_knockout",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2573_0_internal_kernel",
            "claim": "2573 may use PPN comparator bounds and symbolic response kernels internally.",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "bounds and formulas are staged, but MTS theory-side coefficients and kernels are not score-ready",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2573_1_parent_action_grammar",
            "claim": "parent ordinary-sector action grammar forbids hidden coframe/source/coupling slots.",
            "gate_status": "BLOCKED",
            "reason": "terminality, no-extra-slot grammar, EH/coupling origin and coefficient descent remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2573_2_ppn_gamma_score",
            "claim": "MTS passes Cassini/PPN gamma.",
            "gate_status": "BLOCKED",
            "reason": "delta_p, b_R, endpoint, coupling and readout/gauge rows are missing or nonclaim",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2573_3_full_ppn_score",
            "claim": "MTS passes the full PPN residual-vector test.",
            "gate_status": "BLOCKED",
            "reason": "beta, d_R preferred-frame, w_R source, coupling, endpoint and readout response kernels are not filled",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2573_4_local_GR_Newton",
            "claim": "local GR/Newton reduction is derived.",
            "gate_status": "BLOCKED",
            "reason": "PPN kernel is only one gate; EH origin, kappa/ell_J owner, source conservation, reciprocal lock and no-shadow remain open",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2573_5_no_shortcuts",
            "claim": "gamma-only, fitted-GM, cancellation-only, WEP/Ward, q_shape or R10 shortcut is accepted.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "all shortcut routes are explicitly refused by baseline policy, residual-vector and gate rows",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2573_0_parent_grammar",
            "decision": "PARENT_ACTION_GRAMMAR_STILL_UNSIGNED",
            "reason": "2573 retry found no signed ordinary-sector object language beyond the 2572 conditional contract",
            "effect": "finite common-frame/coupling PPN residual rows remain mandatory",
        },
        {
            "decision_id": "DEC2573_1_kernel",
            "decision": "FIRST_COMMON_FRAME_COUPLING_PPN_KERNEL_STAGED_NONCLAIM",
            "reason": "the gamma comparator is source-backed and the beta/alpha_i/xi rows now include coupling/source-scale legs",
            "effect": "PPN can become a real judge once theory-side coefficients or theorem-zero rows exist",
        },
        {
            "decision_id": "DEC2573_2_vector",
            "decision": "GAMMA_ONLY_AND_FITTED_GM_PASSES_FORBIDDEN",
            "reason": "coupling/source normalization can hide in measured GM, and gamma can be clean while beta/preferred-frame/source rows fail",
            "effect": "future testing must score a componentwise vector envelope or close components by theorem",
        },
        {
            "decision_id": "DEC2573_3_next",
            "decision": "DELTA_P_BETA_DISFORMAL_COUPLING_VECTOR_OR_PARENT_GRAMMAR_SELECTED",
            "reason": "the tightest next bottlenecks are reciprocal-lock delta_p, beta second-order closure, disformal preferred-frame kernel and coupling/source-scale ownership",
            "effect": "2574 should try delta_p=0/beta=0 derivation first, then fill d_R/kappa/ell_J/endpoint kernels as source-ready rows",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2573_0_selected",
            "selection_status": "selected",
            "target_file": "2574-Y5-R2FR-delta-p-beta-disformal-coupling-PPN-vector-or-parent-grammar-proof.md",
            "target_script": "scripts/Y5_R2FR_delta_p_beta_disformal_coupling_PPN_vector_or_parent_grammar_proof_2574.py",
            "task": "attempt to derive reciprocal-lock delta_p=0 and beta second-order closure in the same fixed-before-readout source-normalized gauge; if not, fill source-ready d_R preferred-frame, kappa_MTS, ell_J and endpoint/readout PPN response-kernel rows",
            "acceptance_target": "delta_p/beta theorem-zero route or explicit nonclaim PPN vector rows for b_R,d_R,w_R,kappa,ell_J,endpoint/readout with no gamma-only, fitted-GM or cancellation-only pass",
            "guardrails": "no gamma-only pass; no fitted GM/H0 shortcut; no WEP/Ward shortcut; no q_shape shortcut; no R10 shortcut; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "parent_grammar": OUTPUTS["parent_grammar"],
        "ppn_kernel": OUTPUTS["ppn_kernel"],
        "ppn_bounds": OUTPUTS["ppn_bounds"],
        "residual_vector": OUTPUTS["residual_vector"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2573_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2573_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2573_01_parent_grammar_blocked",
        any(row["grammar_id"] == "PAG2573_3_verdict" and row["attempt_result"] == "PARENT_ACTION_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS" for row in data["parent_grammar"]),
        "parent action grammar retry remains blocked",
    )
    add(
        "VAL2573_02_gamma_kernel_present",
        any(row["kernel_id"] == "PPNK2573_0_gamma_common_frame_combo" for row in data["ppn_kernel"]),
        "gamma common-frame/coupling kernel row is present",
    )
    add(
        "VAL2573_03_coupling_legs_present",
        any("Dln_kappa" in row["linear_envelope"] and "Dln_ellJ" in row["linear_envelope"] for row in data["ppn_kernel"]),
        "PPN kernel includes kappa and ellJ legs",
    )
    add(
        "VAL2573_04_ppn_bounds_present",
        len(data["ppn_bounds"]) == 6 and all(row["valid_for_claim"] is False for row in data["ppn_bounds"]),
        "PPN bound ledger covers gamma, beta, alpha1, alpha2, alpha3 and xi as comparators",
    )
    add(
        "VAL2573_05_vector_complete",
        len(data["residual_vector"]) >= 10 and any(row["symbol"] == "Dln_kappa_MTS" for row in data["residual_vector"]) and any(row["symbol"] == "Dln_ell_J" for row in data["residual_vector"]),
        "full no-cancellation PPN residual vector includes coupling/source-scale components",
    )
    add(
        "VAL2573_06_baseline_policy",
        len(data["baseline_policy"]) == 3 and all(row["valid_for_claim"] is False for row in data["baseline_policy"]),
        "fixed-before-readout, no gamma-only and no pair-cancellation policies are written",
    )
    add(
        "VAL2573_07_kernel_rows_nonclaim",
        all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["ppn_kernel"]),
        "all PPN response-kernel rows are nonclaim",
    )
    add("VAL2573_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]), "no gate allows no-shadow, gamma, PPN, local-GR, Newton or R10 claim")
    add(
        "VAL2573_09_no_shortcuts",
        any(row["gate_id"] == "GATE2573_5_no_shortcuts" and row["gate_pass"] is True for row in data["claim_gates"]),
        "gamma-only, fitted-GM, cancellation-only, WEP/Ward, q_shape and R10 shortcuts are refused",
    )
    add(
        "VAL2573_10_next_target_written",
        any(row["route_id"] == "NEXT2573_0_selected" for row in data["next_target"]),
        "2574 delta_p/beta/disformal/coupling PPN vector target selected",
    )
    add("VAL2573_11_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["branch_copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2573*", "*P8_Y5_PPN_COUPLING_2573*", "*JR2573*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2573_12_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2573 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2573_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2573_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2573_OVERALL",
        overall,
        "2573 stages the first common-frame/coupling PPN kernel, keeps parent grammar blocked, and selects delta_p/beta/disformal/coupling vector next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2573 Y5 R2FR First Common-Frame Coupling PPN Response Kernel Or Parent Action Grammar",
        "",
        "**Status:** private nonclaim checkpoint. The parent ordinary-sector action grammar is still unsigned, but the first common-frame plus coupling PPN response-kernel interface is now staged with fixed-before-readout guardrails.",
        "",
        "**Main result:** the useful PPN object is not a single Cassini gamma number. The current local branch needs a componentwise residual vector carrying `delta_p`, `b_R`, `d_R`, `w_R`, endpoint/readout tails, `Dln_kappa_MTS`, and `Dln_ell_J`. A coupling rescale can be hidden by fitted `GM`; therefore the baseline convention must be fixed before readout. This gives MTS a fair boxing scorecard rather than a fake knockout: gamma, beta, preferred-frame, preferred-location and source-normalization legs must either be theorem-zero or bounded together.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Parent Action Grammar Retry",
        markdown_table(data["parent_grammar"], ["grammar_id", "candidate_grammar", "attempt_result", "reason", "effect_if_signed", "valid_for_claim", "claim_allowed"]),
        "",
        "## PPN Coupling Response Kernel",
        markdown_table(data["ppn_kernel"], ["kernel_id", "observable", "bound_id", "derived_or_schema_response", "linear_envelope", "source_bound", "kernel_status", "missing_inputs", "valid_for_claim", "claim_allowed"]),
        "",
        "## PPN Bound Ledger",
        markdown_table(data["ppn_bounds"], ["bound_id", "dataset_id", "observable", "upper_bound", "units", "reference", "use_in_2573", "valid_for_claim", "claim_allowed"]),
        "",
        "## PPN Residual Vector Interface",
        markdown_table(data["residual_vector"], ["component_id", "symbol", "role", "ppn_observables", "current_status", "required_next_input", "valid_for_claim"]),
        "",
        "## Baseline Policy",
        markdown_table(data["baseline_policy"], ["policy_id", "rule", "reason", "status", "failure_mode_prevented", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["branch_copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "parent_grammar": parent_grammar_rows(),
        "ppn_kernel": ppn_kernel_rows(),
        "ppn_bounds": ppn_bound_rows(),
        "residual_vector": residual_vector_rows(),
        "baseline_policy": baseline_policy_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["parent_grammar"], data["parent_grammar"])
    write_csv(OUTPUTS["ppn_kernel"], data["ppn_kernel"])
    write_csv(OUTPUTS["ppn_bounds"], data["ppn_bounds"])
    write_csv(OUTPUTS["residual_vector"], data["residual_vector"])
    write_csv(OUTPUTS["baseline_policy"], data["baseline_policy"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2573_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
