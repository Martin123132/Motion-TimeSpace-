from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIRST_COMMON_FRAME_PPN_KERNEL_2489"
CHECKPOINT_ID = "2489"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2489_SOURCE_REGISTER.csv",
    "parent_clause": OUT / "P8_Y5_NO_SHADOW_2489_PARENT_NO_SHADOW_RETRY.csv",
    "ppn_kernel": OUT / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv",
    "ppn_bounds": OUT / "P8_Y5_NO_SHADOW_2489_PPN_BOUND_LEDGER.csv",
    "residual_vector": OUT / "P8_Y5_NO_SHADOW_2489_PPN_RESIDUAL_VECTOR_INTERFACE.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2489_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2489_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2489_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2489_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2489_VALIDATION.csv",
}

COPY_TARGETS = {
    "parent_clause": LOCAL_BOUNDS / "Parent_no_shadow_clause_retry_2489_NONCLAIM.csv",
    "ppn_kernel": LOCAL_BOUNDS / "First_common_frame_PPN_response_kernel_2489_NONCLAIM.csv",
    "ppn_bounds": LOCAL_BOUNDS / "PPN_bound_ledger_2489_NONCLAIM.csv",
    "residual_vector": LOCAL_BOUNDS / "PPN_residual_vector_interface_2489_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2489_DELTA_P_BETA_DISFORMAL_PPN_VECTOR_OR_NO_SHADOW_CLAUSE.csv",
}

SOURCES = [
    {
        "source_id": "SRC2489_00_2488_handoff",
        "source_path": ROOT / "2488-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
        "needles": ["NEXT2488_0_selected", "KER2488_0_PPN_metric_bR", "VAL2488_OVERALL"],
        "role": "current handoff selecting PPN response kernel or parent no-shadow clause",
    },
    {
        "source_id": "SRC2489_01_1881_gamma_kernel",
        "source_path": ROOT / "1881-Y5-R2FR-first-common-frame-response-kernel-or-parent-action-clause.md",
        "needles": ["RKR1881_0_C_R_conformal_PPN_gamma", "PGB1881_0_Cassini_gamma_to_sR", "VAL1881_OVERALL"],
        "role": "first common-frame conformal-to-PPN-gamma response kernel",
    },
    {
        "source_id": "SRC2489_02_1882_cr_profile",
        "source_path": ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md",
        "needles": ["CRID1882_0_definitions", "SNCM1882_1_generalized_gamma", "VAL1882_OVERALL"],
        "role": "C_R weak-field profile identity and noncircular gamma combination law",
    },
    {
        "source_id": "SRC2489_03_1883_full_vector",
        "source_path": ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md",
        "needles": ["FULL_PPN_RESIDUAL_VECTOR_BUILT_NONCLAIM", "PBOUND1883_1_beta", "VAL1883_OVERALL"],
        "role": "full PPN residual vector and bound ledger precedent",
    },
    {
        "source_id": "SRC2489_04_2160_vector_envelope",
        "source_path": ROOT / "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md",
        "needles": ["PPV2160_6_total_abs_guard", "PBC2160_4_multi_component", "VAL2160_OVERALL"],
        "role": "PPN no-cancellation vector envelope and one-parameter-refusal precedent",
    },
    {
        "source_id": "SRC2489_05_2322_tau_ppn",
        "source_path": ROOT / "2322-Y5-R2FR-tau-PPN-or-common-frame-parent-signature.md",
        "needles": ["TPA2322_1_tau_standard_scalar_tensor", "SIG2322_4_ppn_gauge_source", "VAL2322_OVERALL"],
        "role": "tau_PPN conditional normalization and readout/gauge blocker",
    },
    {
        "source_id": "SRC2489_06_ppn_contract",
        "source_path": OUT / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_2_spatial_curvature_gamma", "MEX524_3_gravitomagnetic_preferred_frame", "MEX524_6_no_cancellation_PPN_envelope"],
        "role": "baseline PPN metric expansion contract",
    },
    {
        "source_id": "SRC2489_07_local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["Cassini_Shapiro_gamma_2003", "Will_2014_PPN_beta_table", "Will_2014_PPN_alpha1_table"],
        "role": "source-backed local comparator bounds",
    },
    {
        "source_id": "SRC2489_08_2488_validation",
        "source_path": OUT / "P8_Y5_BRR545_2488_VALIDATION.csv",
        "needles": ["VAL2488_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
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


def parent_clause_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "clause_id": "PNC2489_0_terminal_public_action_domain",
            "candidate_clause": "S_matter and all ordinary readout factor through a terminal public coframe e_pub=E(Q_vis)",
            "attempt_result": "NOT_PARENT_SIGNED",
            "reason": "2488 made the action-domain contract precise, but no parent normal form yet proves terminality or Q_vis ownership",
            "effect_if_signed": "sets b_R,d_R,w_R,epsilon_endpoint_R to theorem-zero before PPN projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PNC2489_1_no_weyl_disformal_slot",
            "candidate_clause": "Allowed[S_matter,Obs] excludes A_R(C_R), B_R(C_R)u_mu u_nu, and E(Q_vis,C_R)",
            "attempt_result": "CLOSURE_ONLY",
            "reason": "covariance, WEP and same-frame language still allow universal common Weyl/disformal countermodels",
            "effect_if_signed": "sets conformal b_R and preferred-frame d_R to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PNC2489_2_no_endpoint_or_readout_tail",
            "candidate_clause": "boundary endpoints, measured-GM, clocks, photons and PPN gauge maps cannot regenerate C_R/J_q dependence after variation",
            "attempt_result": "NOT_DERIVED",
            "reason": "2322 and the PPN contract retain readout/gauge/source-normalization tails",
            "effect_if_signed": "sets endpoint/readout PPN tail to zero and protects gamma extraction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PNC2489_3_verdict",
            "candidate_clause": "parent no-shadow clause closes local PPN common-frame route",
            "attempt_result": "PARENT_NO_SHADOW_CLAUSE_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "terminality, no-extra-frame, no source-prefactor, endpoint and readout/gauge clauses are still unsigned",
            "effect_if_signed": "would reopen direct local-GR reduction route without empirical common-frame residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def ppn_kernel_rows() -> list[dict[str, Any]]:
    cassini_bound = 2.3e-5
    linear_s_bound = cassini_bound / (2.0 + cassini_bound)
    rows = [
        {
            "kernel_id": "PPNK2489_0_conformal_gamma_kernel",
            "component": "b_R_common_Weyl",
            "observable": "gamma_minus_1",
            "ansatz": "g_obs=exp(2 sigma_R)g_GR, sigma_R=s_R U/c^2, s_R=b_R x_U",
            "derived_response": "gamma_eff=(1+s_R)/(1-s_R); gamma_minus_1=2s_R/(1-s_R)",
            "bound_bridge": f"|s_R| <= {linear_s_bound:.14e} from Cassini |gamma-1|<={cassini_bound:.1e}",
            "kernel_status": "SOURCE_BACKED_CONDITIONAL_KERNEL_NONCLAIM",
            "missing_inputs": "MISSING_b_R_VALUE;MISSING_x_U_PROFILE_OR_DELTA_P;MISSING_BETA_CHANNEL;MISSING_NO_OTHER_PPN_CHANNELS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2489_1_CR_delta_p_combo_kernel",
            "component": "C_R_profile_times_b_R",
            "observable": "gamma_obs_minus_1",
            "ansatz": "C_R=ln(T^2S)=2 delta_p U/c^2+O(U^2/c^4), sigma_R=b_R C_R",
            "derived_response": "gamma_obs=(1+delta_p+2b_R delta_p)/(1-2b_R delta_p); gamma_obs-1=(delta_p+4b_R delta_p)/(1-2b_R delta_p)",
            "bound_bridge": "Cassini bounds the combined residual delta_p(1+4b_R)/(1-2b_R delta_p), not b_R alone",
            "kernel_status": "DERIVED_SYMBOLIC_COMBO_NONCLAIM",
            "missing_inputs": "MISSING_delta_p_ZERO_OR_VALUE;MISSING_b_R_VALUE;MISSING_NO_CANCELLATION_THEOREM;MISSING_FULL_VECTOR_CLOSURE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2489_2_beta_second_order_placeholder",
            "component": "beta_and_second_order_source",
            "observable": "beta_minus_1",
            "ansatz": "g00=-1+2U/c^2-2(1+delta_beta_total)U^2/c^4+O(c^-6)",
            "derived_response": "delta_beta_total must include source-normalization, operator, readout, endpoint and common-frame cross terms",
            "bound_bridge": "Will beta table supplies a comparator, but no MTS beta response kernel is derived here",
            "kernel_status": "MISSING_BETA_RESPONSE_KERNEL",
            "missing_inputs": "MISSING_SECOND_ORDER_FIELD_EQUATION;MISSING_SOURCE_NORMALIZATION;MISSING_READOUT_GAUGE;MISSING_ENDPOINT_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2489_3_disformal_preferred_frame_placeholder",
            "component": "d_R_common_disformal",
            "observable": "alpha1;alpha2;alpha3;xi",
            "ansatz": "g_obs=A(C_R)^2g_pub+D(C_R)u_mu u_nu plus possible boundary/domain vectors",
            "derived_response": "preferred-frame/location residuals require a normalized vector/current/domain projection; none is derived by common-frame language",
            "bound_bridge": "Will preferred-frame/location rows are comparators only until K_alpha_i_dR and endpoint kernels exist",
            "kernel_status": "MISSING_PREFERRED_FRAME_RESPONSE_KERNEL",
            "missing_inputs": "MISSING_DISFORMAL_METRIC_ANSATZ;MISSING_VECTOR_NORMALIZATION;MISSING_BOUNDARY_DOMAIN_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "PPNK2489_4_endpoint_readout_tail_placeholder",
            "component": "epsilon_endpoint_R_and_readout_tail",
            "observable": "gamma;beta;alpha_i;orbital_light_time",
            "ansatz": "e_obs=E(Q_vis,Q_endpoint) or post-variation measured-GM/PPN-gauge readout shifts the extracted metric coefficients",
            "derived_response": "endpoint/readout terms must be zero by theorem or kept as explicit additive PPN vector components",
            "bound_bridge": "no direct score; endpoint tails feed the absolute no-cancellation vector",
            "kernel_status": "MISSING_ENDPOINT_READOUT_KERNEL",
            "missing_inputs": "MISSING_ENDPOINT_SILENCE;MISSING_GM_CALIBRATION_MAP;MISSING_PPN_GAUGE_TRANSFORM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def ppn_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "PBOUND2489_0_gamma",
            "dataset_id": "Cassini_Shapiro_gamma_2003",
            "observable": "gamma_minus_1",
            "upper_bound": "2.3e-05",
            "units": "dimensionless",
            "reference": "https://www.nature.com/articles/nature01997; doi:10.1038/nature01997",
            "use_in_2489": "source-backed comparator for PPNK2489_0 and PPNK2489_1 only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2489_1_beta",
            "dataset_id": "Will_2014_PPN_beta_table",
            "observable": "beta_minus_1",
            "upper_bound": "7.8e-05",
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2489": "comparator only; beta response kernel missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2489_2_alpha1",
            "dataset_id": "Will_2014_PPN_alpha1_table",
            "observable": "alpha1",
            "upper_bound": "1e-04",
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2489": "preferred-frame comparator; d_R kernel missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2489_3_alpha2",
            "dataset_id": "Will_2014_PPN_alpha2_table",
            "observable": "alpha2",
            "upper_bound": "2e-09",
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2489": "preferred-frame comparator; vector/domain projection missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2489_4_alpha3",
            "dataset_id": "Will_2014_PPN_alpha3_table",
            "observable": "alpha3",
            "upper_bound": "4e-20",
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2489": "momentum-flux/source-exchange comparator; conservation/source closure missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND2489_5_xi",
            "dataset_id": "Will_2014_PPN_xi_table",
            "observable": "xi",
            "upper_bound": "4e-09",
            "units": "dimensionless",
            "reference": "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html",
            "use_in_2489": "preferred-location comparator; boundary/domain kernel missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "PPNV2489_0_delta_p_qR",
            "symbol": "delta_p_or_q_R_hat",
            "role": "spatial-curvature/reciprocal-lock residual",
            "ppn_observables": "gamma_minus_1;beta_minus_1",
            "current_status": "MISSING_RECIPROCAL_LOCK_OR_NUMERIC_INPUT",
            "required_next_input": "derive T^2S=1/delta_p=0 or provide source-normalized delta_p/q_R_hat row",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2489_1_bR",
            "symbol": "b_R",
            "role": "common Weyl no-shadow coefficient",
            "ppn_observables": "gamma_minus_1 with CR combo law",
            "current_status": "CONDITIONAL_KERNEL_READY_VALUE_MISSING",
            "required_next_input": "b_R theorem-zero from parent no-shadow clause or sourced coefficient in same normalization",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2489_2_beta",
            "symbol": "delta_beta_total",
            "role": "second-order g00/source/operator/readout residual",
            "ppn_observables": "beta_minus_1",
            "current_status": "MISSING_BETA_RESPONSE_KERNEL",
            "required_next_input": "second-order source-normalized field-equation closure or finite beta row",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2489_3_dR",
            "symbol": "d_R",
            "role": "disformal/preferred-frame shadow coefficient",
            "ppn_observables": "alpha1;alpha2;possibly gamma",
            "current_status": "MISSING_DISFORMAL_PPN_PROJECTION",
            "required_next_input": "normalized disformal ansatz and preferred-frame response matrix",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2489_4_wR",
            "symbol": "w_R",
            "role": "source-only matter prefactor/source normalization leak",
            "ppn_observables": "beta_minus_1;gamma_minus_1;alpha3 via source exchange",
            "current_status": "MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL",
            "required_next_input": "source-current descent/no source slot theorem or source-normalization response kernel",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2489_5_endpoint",
            "symbol": "epsilon_endpoint_R",
            "role": "boundary/endpoint/local projection tail",
            "ppn_observables": "xi;alpha3;orbital_light_time;gamma/beta readout tails",
            "current_status": "MISSING_ENDPOINT_SILENCE_OR_PROJECTION",
            "required_next_input": "boundary endpoint silence theorem or finite endpoint PPN/orbital kernel",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2489_6_readout_gauge",
            "symbol": "alpha_readout_or_delta_GM",
            "role": "post-variation PPN gauge/measured-GM calibration tail",
            "ppn_observables": "gamma_minus_1;beta_minus_1",
            "current_status": "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION",
            "required_next_input": "fixed-before-readout and measured-GM transfer theorem or source-backed tail bound",
            "valid_for_claim": False,
        },
        {
            "component_id": "PPNV2489_7_total_abs",
            "symbol": "Delta_PPN_abs",
            "role": "componentwise no-cancellation envelope",
            "ppn_observables": "all_PPN",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "required_next_input": "all components theorem-zero or numerically bounded with no pair-cancellation shortcut",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2489_0_internal_kernel",
            "claim": "2489 may use the conformal gamma kernel and PPN vector internally",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "kernel math and comparator rows are source-backed/needle-checked but not score-ready",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2489_1_parent_no_shadow",
            "claim": "parent no-shadow clause sets b_R=d_R=w_R=endpoint=0",
            "gate_status": "BLOCKED",
            "reason": "action-domain, terminality, source-prefactor, endpoint and readout clauses remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2489_2_ppn_gamma_score",
            "claim": "MTS passes Cassini/PPN gamma",
            "gate_status": "BLOCKED",
            "reason": "delta_p/q_R_hat, b_R, beta/source/preferred-frame/readout/endpoint channels remain missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2489_3_full_ppn_score",
            "claim": "MTS passes full PPN residual-vector test",
            "gate_status": "BLOCKED",
            "reason": "beta, d_R preferred-frame, w_R source, endpoint and readout response kernels are not filled",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2489_4_local_GR_Newton",
            "claim": "local GR/Newton reduction is derived",
            "gate_status": "BLOCKED",
            "reason": "PPN kernel is only one gate; EH/kappa/source conservation/reciprocal lock/no-shadow remain open",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2489_5_no_shortcuts",
            "claim": "gamma-only, cancellation-only, WEP-only, q_shape or R10 shortcut is accepted",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "all such shortcuts are explicitly refused by residual-vector and gate rows",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2489_0_parent_clause",
            "decision": "PARENT_NO_SHADOW_CLAUSE_STILL_UNSIGNED",
            "reason": "2489 retry found no new parent action-domain theorem beyond the 2488 conditional contract",
            "effect": "finite common-frame PPN residual rows remain mandatory",
        },
        {
            "decision_id": "DEC2489_1_kernel",
            "decision": "FIRST_PPN_GAMMA_KERNEL_RESTAGED_AS_CURRENT_BRANCH_OBJECT",
            "reason": "1881/1741 already provide the valid conformal response map; 2489 imports it into the current no-shadow branch",
            "effect": "Cassini constrains s_R=b_R x_U, and for C_R specifically the combined delta_p/b_R law must be used",
        },
        {
            "decision_id": "DEC2489_2_vector",
            "decision": "GAMMA_ONLY_PASS_FORBIDDEN",
            "reason": "beta, disformal/preferred-frame, source-prefactor, endpoint and readout tails can survive a gamma-only comparison",
            "effect": "next work must target delta_p/beta/disformal vector fill or a real no-shadow proof",
        },
        {
            "decision_id": "DEC2489_3_next",
            "decision": "DELTA_P_BETA_DISFORMAL_VECTOR_OR_NO_SHADOW_SELECTED",
            "reason": "the tightest next bottlenecks are reciprocal-lock delta_p, beta second-order closure, and d_R preferred-frame kernel",
            "effect": "2500 should try delta_p=0/beta=0 derivation first, then fill d_R/endpoint kernels as source-ready rows",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2489_0_selected",
            "selection_status": "selected",
            "target_file": "2500-Y5-R2FR-delta-p-beta-disformal-PPN-vector-or-parent-no-shadow-proof.md",
            "target_script": "scripts/Y5_R2FR_delta_p_beta_disformal_PPN_vector_or_parent_no_shadow_proof_2500.py",
            "task": "attempt to derive reciprocal-lock delta_p=0 and beta second-order closure in the same source-normalized gauge; if not, fill source-ready d_R preferred-frame and endpoint/readout PPN response-kernel rows",
            "acceptance_target": "delta_p/beta theorem-zero route or explicit nonclaim PPN vector rows for b_R,d_R,w_R,endpoint/readout with no gamma-only or cancellation-only pass",
            "guardrails": "no gamma-only pass; no fitted GM shortcut; no WEP/Ward shortcut; no q_shape shortcut; no R10 shortcut; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "parent_clause": OUTPUTS["parent_clause"],
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
                    "copy_id": f"COPY2489_{key}",
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
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2489_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2489_01_parent_clause_blocked",
        any(row["clause_id"] == "PNC2489_3_verdict" and row["attempt_result"] == "PARENT_NO_SHADOW_CLAUSE_NOT_DERIVED_CURRENT_CORPUS" for row in data["parent_clause"]),
        "parent no-shadow retry remains blocked",
    )
    add(
        "VAL2489_02_gamma_kernel_source_backed",
        any(row["kernel_id"] == "PPNK2489_0_conformal_gamma_kernel" and row["kernel_status"] == "SOURCE_BACKED_CONDITIONAL_KERNEL_NONCLAIM" for row in data["ppn_kernel"]),
        "conformal gamma response kernel is staged as source-backed conditional nonclaim",
    )
    add(
        "VAL2489_03_combo_law_present",
        any(row["kernel_id"] == "PPNK2489_1_CR_delta_p_combo_kernel" and "delta_p" in row["derived_response"] for row in data["ppn_kernel"]),
        "C_R delta_p/b_R combination law is recorded",
    )
    add(
        "VAL2489_04_missing_kernels_retained",
        all(row["valid_for_claim"] is False for row in data["ppn_kernel"]) and any(row["kernel_status"] == "MISSING_BETA_RESPONSE_KERNEL" for row in data["ppn_kernel"]),
        "beta, preferred-frame and endpoint kernels remain missing/nonclaim",
    )
    add(
        "VAL2489_05_ppn_bounds_present",
        len(data["ppn_bounds"]) >= 6 and all(row["valid_for_claim"] is False for row in data["ppn_bounds"]),
        "PPN bound ledger covers gamma, beta, alpha1, alpha2, alpha3 and xi as comparators",
    )
    add(
        "VAL2489_06_vector_complete",
        len(data["residual_vector"]) >= 8 and any(row["component_id"] == "PPNV2489_7_total_abs" for row in data["residual_vector"]),
        "full no-cancellation PPN residual vector interface is present",
    )
    add(
        "VAL2489_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows no-shadow, gamma, PPN, local-GR, Newton or R10 claim",
    )
    add(
        "VAL2489_08_no_shortcuts",
        any(row["gate_id"] == "GATE2489_5_no_shortcuts" and row["gate_status"] == "PASS_GUARDRAIL" for row in data["claim_gates"]),
        "gamma-only, cancellation-only, WEP/Ward, q_shape and R10 shortcuts are refused",
    )
    add(
        "VAL2489_09_next_target_written",
        any(row["route_id"] == "NEXT2489_0_selected" for row in data["next"]),
        "2500 delta_p/beta/disformal PPN vector target selected",
    )
    add("VAL2489_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2489*", "*P8_Y5_NO_SHADOW_2489*", "*JR2489*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2489_11_no_formalization_artifacts", not formalization_artifacts, "no 2489 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2489_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2489_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2489_OVERALL",
        overall,
        "2489 imports the first common-frame PPN gamma kernel, binds C_R to delta_p, keeps full vector gates blocked, and selects delta_p/beta/disformal follow-up",
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
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2489 Y5 R2FR First Common-Frame PPN Response Kernel Or Parent No-Shadow Clause",
        "",
        "**Status:** private nonclaim checkpoint. The parent no-shadow clause is still unsigned, but the first PPN response kernel is now imported into the current branch with the correct guardrails.",
        "",
        "**Main result:** the useful kernel is not `b_R` alone. In the generic conformal branch, `gamma_minus_1=2s_R/(1-s_R)` with `s_R=b_R x_U`, giving the Cassini target `|s_R| <= 1.14998677515e-5`. For the actual `C_R=ln(T^2S)` route, `x_U=2delta_p`, so Cassini constrains the combined residual `(delta_p+4b_R delta_p)/(1-2b_R delta_p)`. Therefore a gamma-only pass would be fake unless `delta_p`, beta, preferred-frame, source, endpoint and readout tails are also zeroed or bounded.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Parent No-Shadow Clause Retry",
        markdown_table(data["parent_clause"], ["clause_id", "candidate_clause", "attempt_result", "reason", "effect_if_signed", "valid_for_claim", "claim_allowed"]),
        "",
        "## PPN Response Kernel",
        markdown_table(data["ppn_kernel"], ["kernel_id", "component", "observable", "ansatz", "derived_response", "bound_bridge", "kernel_status", "missing_inputs", "valid_for_claim", "claim_allowed"]),
        "",
        "## PPN Bound Ledger",
        markdown_table(data["ppn_bounds"], ["bound_id", "dataset_id", "observable", "upper_bound", "units", "reference", "use_in_2489", "valid_for_claim", "claim_allowed"]),
        "",
        "## PPN Residual Vector Interface",
        markdown_table(data["residual_vector"], ["component_id", "symbol", "role", "ppn_observables", "current_status", "required_next_input", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
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
        "parent_clause": parent_clause_rows(),
        "ppn_kernel": ppn_kernel_rows(),
        "ppn_bounds": ppn_bound_rows(),
        "residual_vector": residual_vector_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["parent_clause"], data["parent_clause"])
    write_csv(OUTPUTS["ppn_kernel"], data["ppn_kernel"])
    write_csv(OUTPUTS["ppn_bounds"], data["ppn_bounds"])
    write_csv(OUTPUTS["residual_vector"], data["residual_vector"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
