from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_DELTA_P_BETA_DISFORMAL_COUPLING_VECTOR_2574"
CHECKPOINT_ID = "2574"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2574-Y5-R2FR-delta-p-beta-disformal-coupling-PPN-vector-or-parent-grammar-proof.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PPN_VECTOR_2574_SOURCE_REGISTER.csv",
    "delta_p_proof": OUT / "P8_Y5_PPN_VECTOR_2574_DELTA_P_ZERO_PROOF_AUDIT.csv",
    "beta_gate": OUT / "P8_Y5_PPN_VECTOR_2574_BETA_SECOND_ORDER_COUPLING_GATE.csv",
    "kernel_rows": OUT / "P8_Y5_PPN_VECTOR_2574_DISFORMAL_COUPLING_ENDPOINT_KERNEL_ROWS.csv",
    "vector_requirements": OUT / "P8_Y5_PPN_VECTOR_2574_FULL_VECTOR_REQUIREMENTS.csv",
    "live_input_contract": OUT / "P8_Y5_PPN_VECTOR_2574_LIVE_INPUT_CONTRACT.csv",
    "claim_gates": OUT / "P8_Y5_PPN_VECTOR_2574_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PPN_VECTOR_2574_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PPN_VECTOR_2574_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PPN_VECTOR_2574_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2574_VALIDATION.csv",
}

COPY_TARGETS = {
    "delta_p_proof": LOCAL_BOUNDS / "Delta_p_zero_proof_audit_2574_NONCLAIM.csv",
    "beta_gate": LOCAL_BOUNDS / "Beta_second_order_coupling_gate_2574_NONCLAIM.csv",
    "kernel_rows": LOCAL_BOUNDS / "Disformal_coupling_endpoint_PPN_kernel_rows_2574_NONCLAIM.csv",
    "vector_requirements": LOCAL_BOUNDS / "Full_PPN_vector_requirements_2574_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2574_QR_PARENT_ZERO_OR_LIVE_DELTA_P_COUPLING_INPUT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2574_00_2573_handoff",
        "source_path": ROOT / "2573-Y5-R2FR-first-common-frame-coupling-PPN-response-kernel-or-parent-action-grammar.md",
        "needles": ["NEXT2573_0_selected", "PPNV2573_2_kappa", "VAL2573_OVERALL"],
        "role": "active handoff selecting delta_p/beta/disformal/coupling PPN vector",
    },
    {
        "source_id": "SRC2574_01_2500_precedent",
        "source_path": ROOT / "2500-Y5-R2FR-delta-p-beta-disformal-PPN-vector-or-parent-no-shadow-proof.md",
        "needles": ["DPP2500_1_zero_flux_lemma", "BETA2500_4_verdict", "VAL2500_OVERALL"],
        "role": "earlier delta_p/beta/disformal vector checkpoint without upgraded coupling legs",
    },
    {
        "source_id": "SRC2574_02_1884_zero_flux",
        "source_path": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
        "needles": ["NBC1884_1_exact_zero_flux_lemma", "DPQR1884_2_delta_p", "VAL1884_OVERALL"],
        "role": "zero-flux lemma and strict delta_p/q_R_hat input contract",
    },
    {
        "source_id": "SRC2574_03_1883_vector",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
        "needles": ["PPNV1883_2_beta_second_order", "PPNV1883_3_dR_preferred_frame", "PPNV1883_7_total_no_cancellation"],
        "role": "full PPN residual-vector precedent",
    },
    {
        "source_id": "SRC2574_04_2231_ppn_coefficients",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2231_PPN_COEFFICIENT_DERIVATION.csv",
        "needles": ["PPNC2231_4_delta_beta_definition", "PPNC2231_6_perihelion_degeneracy"],
        "role": "PPN coefficient dictionary for q_R and beta",
    },
    {
        "source_id": "SRC2574_05_2234_ward_beta",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2234_WARD_PPN_GATE.csv",
        "needles": ["WPPN2234_2_beta", "WPPN2234_5_local_claim"],
        "role": "conditional EH/Ward beta route and blocked local claim",
    },
    {
        "source_id": "SRC2574_06_2572_no_shadow_coupling",
        "source_path": ROOT / "2572-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
        "needles": ["CS2572_0_kappa_MTS", "CS2572_1_ell_J", "VAL2572_OVERALL"],
        "role": "coupling shadow audit for kappa_MTS and ell_J",
    },
    {
        "source_id": "SRC2574_07_ppn_contract",
        "source_path": OUT / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_1_g00_quadratic_beta", "MEX524_3_gravitomagnetic_preferred_frame", "MEX524_6_no_cancellation_PPN_envelope"],
        "role": "baseline PPN metric expansion contract",
    },
    {
        "source_id": "SRC2574_08_local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["Will_2014_PPN_beta_table", "Will_2014_PPN_alpha2_table", "Will_2014_PPN_alpha3_table"],
        "role": "PPN beta/preferred-frame comparator bounds",
    },
    {
        "source_id": "SRC2574_09_2573_validation",
        "source_path": OUT / "P8_Y5_BRR545_2573_VALIDATION.csv",
        "needles": ["VAL2573_OVERALL", "PASS"],
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


def delta_p_proof_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "proof_id": "DPP2574_0_exterior_current",
            "statement": "In the exterior, partial_r(W partial_r C_R)=J_R and J_R=0 imply W partial_r C_R=Q_R.",
            "status": "CONDITIONAL_CURRENT_EQUATION_AVAILABLE",
            "missing_premise": "parent action must define the reciprocal generator, source silence and readout descent, not just an exterior integration constant",
            "coupling_interaction": "kappa_MTS and ell_J must be fixed before defining Q_R and M_source, otherwise q_R_hat normalization can move",
            "consequence": "identifies the finite charge that controls delta_p",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DPP2574_1_zero_flux_lemma",
            "statement": "If Q_R=0, W>0, J_R=0 in the exterior, and C_R(infinity)=0, then C_R=0.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "missing_premise": "Q_R=0/no-boundary-charge theorem is not parent-signed",
            "coupling_interaction": "source-current scale ownership is needed so Q_R=0 is not a fitted-source convention",
            "consequence": "delta_p=0 at first PPN order because C_R=2 delta_p U/c^2+O(U^2/c^4)",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DPP2574_2_finite_bridge",
            "statement": "If exterior C_R=-Q_R/r and q_R_hat=Q_R c^2/(G M_source), then delta_p=-q_R_hat/2.",
            "status": "DERIVED_CONDITIONAL_BRIDGE_NONCLAIM",
            "missing_premise": "live q_R_hat value, fixed GM convention, source body, matter/readout descent and coupling/source-scale ownership",
            "coupling_interaction": "q_R_hat must use the same fixed-before-readout kappa_MTS/ell_J/source convention as the PPN vector",
            "consequence": "strict finite input row can feed the full PPN vector without closure cheating",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DPP2574_3_parent_zero_verdict",
            "statement": "Current MTS parent derives Q_R=0 and therefore delta_p=0.",
            "status": "NOT_DERIVED_CURRENT_CORPUS",
            "missing_premise": "boundary charge zero, source descent, matter descent, projection silence, no-shadow readout and coupling ownership must close in one action",
            "coupling_interaction": "Dln_kappa_MTS and Dln_ell_J remain live unless the same parent package owns them",
            "consequence": "delta_p remains the first local-GR finite/theorem-zero input",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def beta_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "BETA2574_0_definition",
            "statement": "beta_minus_1 is the second-order g00 residual delta_beta_total.",
            "status": "PPN_DICTIONARY_AVAILABLE",
            "required_inputs": "source-normalized second-order field equation; measured-GM convention; readout/gauge transform",
            "coupling_blocker": "Dln_kappa_MTS and Dln_ell_J can enter beta through source normalization and U^2 terms",
            "failure_mode": "gamma or delta_p closure does not imply beta=1",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2574_1_EH_conditional",
            "statement": "EH core plus correctly normalized Hilbert source and no extra modes gives beta=1.",
            "status": "EXACT_CONDITIONAL_GR_LIMIT",
            "required_inputs": "EH/kappa owner; source closure; boundary silence; no extra scalar/vector/tensor modes; readout fixed before comparison",
            "coupling_blocker": "e_kappaG and e_ellJ_owner are still unsigned, so EH beta=1 cannot be imported as an MTS prediction",
            "failure_mode": "using GR Schwarzschild beta=1 as an imported axiom would smuggle the target result",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2574_2_source_coupling",
            "statement": "source-prefactor w_R, kappa_MTS, ell_J and non-Hilbert current tails must not re-enter beta through U^2 terms.",
            "status": "MISSING_SOURCE_COUPLING_SECOND_ORDER_CLOSURE",
            "required_inputs": "source-current descent/no source-only slot theorem or finite beta source/coupling kernel",
            "coupling_blocker": "stationary mass cancellation does not prove dynamic second-order source-current silence",
            "failure_mode": "WEP-clean source shifts can survive composition tests and move beta/source normalization",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2574_3_readout_gauge",
            "statement": "PPN gauge and measured-GM calibration must not absorb or create beta/gamma residuals.",
            "status": "MISSING_READOUT_GAUGE_TRANSFER",
            "required_inputs": "fixed-before-readout theorem; GM calibration map; observed PPN gauge transform",
            "coupling_blocker": "coupling rescale can be hidden by fitted GM unless the baseline convention is fixed first",
            "failure_mode": "a fitted-GM shortcut can hide a source/readout tail rather than derive local GR",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2574_4_verdict",
            "statement": "Current MTS derives beta=1 in the active local branch.",
            "status": "BETA_CLOSURE_NOT_DERIVED_CURRENT_CORPUS",
            "required_inputs": "BETA2574_1 through BETA2574_3 must all be parent-signed or source-bounded",
            "coupling_blocker": "beta gate remains coupled to kappa_MTS, ell_J, source normalization and readout order",
            "failure_mode": "local-GR claim remains blocked even if gamma channel is bounded",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "DPK2574_0_dR_alpha1_alpha2",
            "component": "d_R common disformal/preferred-frame",
            "candidate_map": "alpha1,alpha2 = K_dis*d_R plus current/domain/tau/coupling normalization terms",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Will_2014_PPN_alpha1_table:R5_alpha1;Will_2014_PPN_alpha2_table:R6_alpha2",
            "required_inputs": "normalized disformal ansatz, current field normalization, preferred-frame gauge, same matter metric convention",
            "coupling_extension": "include K_alpha_i_kJ*Dln(kappa_MTS*ell_J) if source-current normalization feeds preferred-frame terms",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DPK2574_1_flux_alpha3",
            "component": "source exchange/boundary flux/w_R/ell_J",
            "candidate_map": "alpha3 = K_flux*(w_R + q_boundary + source_exchange + Dln_ell_J + Dln_kappa_MTS)",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Will_2014_PPN_alpha3_table:R7_alpha3",
            "required_inputs": "momentum conservation/source-current descent, boundary flux silence or finite coefficient row",
            "coupling_extension": "alpha3 is the hardest source-exchange warning because its comparator is ultra-tight",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DPK2574_2_endpoint_xi",
            "component": "epsilon_endpoint_R/domain/boundary",
            "candidate_map": "xi = K_xi_endpoint*epsilon_endpoint_R + K_xi_domain*q_domain + K_xi_proj*epsilon_projector",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Will_2014_PPN_xi_table:R8_xi",
            "required_inputs": "endpoint local projection kernel, domain/support vector, boundary no-hair theorem or finite input",
            "coupling_extension": "endpoint/source support must use the same fixed-before-readout source convention as kappa and ell_J",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DPK2574_3_readout_gamma_beta_tail",
            "component": "post-variation readout/measured-GM tail",
            "candidate_map": "delta_gamma_readout,delta_beta_readout = K_readout*C_readout + K_GM*delta_GM_fit",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Cassini_Shapiro_gamma_2003:R3_gamma;Will_2014_PPN_beta_table:R4_beta",
            "required_inputs": "fixed-before-readout proof or explicit readout calibration residual with units",
            "coupling_extension": "delta_GM_fit cannot be used to absorb Dln_kappa_MTS or Dln_ell_J",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DPK2574_4_coupling_source_beta",
            "component": "kappa_MTS/ell_J source-normalization beta leg",
            "candidate_map": "delta_beta_source = K_beta_k*Dln_kappa_MTS + K_beta_J*Dln_ell_J + K_beta_norm*E_norm",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Will_2014_PPN_beta_table:R4_beta",
            "required_inputs": "parent EH coefficient, ell_J owner, Hilbert source-current map, second-order source-normalized field equation",
            "coupling_extension": "this row is the explicit no-fitted-GM coupling backstop",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def vector_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "VREQ2574_0_delta_p",
            "required_for_claim": "delta_p=0 theorem or source-normalized q_R_hat/delta_p row satisfying delta_p=-q_R_hat/2",
            "current_status": "MISSING_PARENT_ZERO_OR_LIVE_INPUT",
            "blocks": "gamma kernel; C_R no-shadow combo",
            "coupling_dependency": "q_R_hat uses fixed kappa/source-mass convention",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_1_bR",
            "required_for_claim": "b_R=0 theorem or finite coefficient in same C_R normalization",
            "current_status": "MISSING_NO_SHADOW_ZERO_OR_VALUE",
            "blocks": "common Weyl gamma/clock/source row",
            "coupling_dependency": "b_R scoring must share the same source/readout convention as coupling legs",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_2_kappa",
            "required_for_claim": "Dln_kappa_MTS=0 theorem or finite source-normalized response below PPN/source bounds",
            "current_status": "MISSING_PARENT_EH_COUPLING_OWNER",
            "blocks": "beta/source normalization/readout PPN vector",
            "coupling_dependency": "cannot be inferred from G_ref or fitted GM",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_3_ellJ",
            "required_for_claim": "Dln_ell_J=0 theorem or finite source-current response row",
            "current_status": "MISSING_SOURCE_SCALE_OWNER",
            "blocks": "beta, alpha3, source-normalization and orbital vector",
            "coupling_dependency": "must be parent-owned before local/cosmology fits",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_4_beta",
            "required_for_claim": "beta=1 theorem or delta_beta_total row below beta bound",
            "current_status": "MISSING_SECOND_ORDER_CLOSURE",
            "blocks": "local-GR PPN completion",
            "coupling_dependency": "source-coupling legs feed beta unless excluded or bounded",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_5_dR",
            "required_for_claim": "d_R=0 theorem or alpha1/alpha2 response kernel below preferred-frame bounds",
            "current_status": "MISSING_DISFORMAL_KERNEL",
            "blocks": "preferred-frame PPN",
            "coupling_dependency": "current normalization may couple d_R to kappa*ell_J source flow",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_6_wR_source",
            "required_for_claim": "w_R/source-only slot theorem-zero or source-normalization kernel below PPN/WEP bounds",
            "current_status": "MISSING_SOURCE_PREFACTOR_CLOSURE",
            "blocks": "beta, alpha3, measured-GM transfer",
            "coupling_dependency": "source prefactor must be separated from kappa/ell_J owner rows",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_7_endpoint_readout",
            "required_for_claim": "endpoint/readout/gauge tails theorem-zero or source-bounded",
            "current_status": "MISSING_ENDPOINT_READOUT_KERNEL",
            "blocks": "xi, gamma/beta extraction, orbital/light-time",
            "coupling_dependency": "endpoint/source support uses the same fixed-before-readout source convention",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2574_8_total_no_cancellation",
            "required_for_claim": "componentwise absolute envelope below all relevant bounds or parent identity proving cancellation",
            "current_status": "VECTOR_VALUES_MISSING",
            "blocks": "any PPN/local-GR claim",
            "coupling_dependency": "no cancellation between delta_p, b_R, kappa, ell_J, beta or endpoint legs without parent identity",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def live_input_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "input_id": "LIVE2574_0_parent_zero",
            "route_type": "parent_zero_theorem",
            "required_fields": "Q_R=0;delta_p=0;q_R_hat=0;boundary_charge_status=SIGNED;source_descent=SIGNED;matter_readout_descent=SIGNED;coupling_owner=SIGNED",
            "relation": "delta_p=-q_R_hat/2",
            "reject_if": "closure_used;comparator_only;missing_coupling_owner;missing_projection;fitted_GM_absorption",
            "status": "TEMPLATE_NONCLAIM_PARENT_INPUT_MISSING",
            "valid_for_claim": False,
        },
        {
            "input_id": "LIVE2574_1_finite_delta_p",
            "route_type": "finite_qR_hat",
            "required_fields": "numeric_delta_p;numeric_q_R_hat;GM_convention;source_body;source_path;projection_status;full_vector_ready;coupling_baseline_fixed",
            "relation": "abs(delta_p + q_R_hat/2) <= tolerance",
            "reject_if": "missing_numeric;bad_relation;gamma_only;cancellation_only;fitted_GM_absorption;missing_kappa_or_ellJ_baseline",
            "status": "TEMPLATE_NONCLAIM_NO_LIVE_ROW",
            "valid_for_claim": False,
        },
        {
            "input_id": "LIVE2574_2_beta_source",
            "route_type": "finite_beta_or_theorem_zero",
            "required_fields": "delta_beta_total or beta_zero_theorem;source_coupling_kernel;kappa_owner;ellJ_owner;readout_gauge_transfer",
            "relation": "abs(delta_beta_total) <= beta_bound and all source/coupling legs accounted componentwise",
            "reject_if": "GR_import;gamma_only;missing_source_kernel;fitted_GM_absorption",
            "status": "TEMPLATE_NONCLAIM_NO_LIVE_ROW",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2574_0_internal",
            "claim": "2574 may guide private derivation/testing.",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "exact conditional lemmas and source-ready templates are separated from claims",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2574_1_delta_p_zero",
            "claim": "delta_p=0 is derived for active MTS.",
            "gate_status": "BLOCKED",
            "reason": "Q_R=0/no-boundary-charge/source-descent/coupling-owner theorem remains unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2574_2_beta_one",
            "claim": "beta=1 is derived for active MTS.",
            "gate_status": "BLOCKED",
            "reason": "EH/source/readout/no-extra-mode route is exact conditional but not parent-signed and coupling legs remain open",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2574_3_coupling_silence",
            "claim": "kappa_MTS and ell_J are silent in local PPN/source normalization.",
            "gate_status": "BLOCKED",
            "reason": "e_kappaG, e_ellJ_owner and second-order source-coupling kernels remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2574_4_preferred_frame_zero",
            "claim": "d_R/endpoint/source/coupling tails do not affect alpha_i or xi.",
            "gate_status": "BLOCKED",
            "reason": "preferred-frame, boundary, source-exchange and readout kernels are source-ready templates only",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2574_5_full_ppn",
            "claim": "full PPN vector is passed.",
            "gate_status": "BLOCKED",
            "reason": "component values/theorem-zero rows are missing and gamma-only/fitted-GM/cancellation-only routes are rejected",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2574_6_local_GR_Newton",
            "claim": "local GR/Newton is derived.",
            "gate_status": "BLOCKED",
            "reason": "delta_p, beta, preferred-frame, source, endpoint, coupling and EH/source-normalization gates remain open",
            "gate_pass": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2574_0_delta_p",
            "decision": "ZERO_FLUX_ROUTE_REMAINS_BEST_DELTA_P_DERIVATION_TARGET",
            "reason": "Q_R=0 would cleanly force C_R=0 and delta_p=0 without fitting",
            "effect": "hunt the parent no-boundary-charge/source-descent/coupling-owner signature rather than treat gamma bounds as proof",
        },
        {
            "decision_id": "DEC2574_1_beta",
            "decision": "BETA_REQUIRES_SECOND_ORDER_SOURCE_COUPLING_GATE",
            "reason": "gamma closure does not imply beta=1; EH/source/readout/no-extra-mode plus kappa/ellJ ownership must close",
            "effect": "beta gets its own source-coupling gate, not a footnote under gamma",
        },
        {
            "decision_id": "DEC2574_2_vector",
            "decision": "DISFORMAL_ENDPOINT_COUPLING_ROWS_STAGED_AS_SOURCE_READY_TEMPLATES",
            "reason": "preferred-frame/location/source-exchange bounds exist, but MTS response kernels do not",
            "effect": "d_R, alpha_i, xi, kappa, ell_J and endpoint kernels are the empirical backstop if proof route stalls",
        },
        {
            "decision_id": "DEC2574_3_next",
            "decision": "QR_PARENT_ZERO_SIGNATURE_OR_LIVE_DELTA_P_COUPLING_INPUT_SELECTED_NEXT",
            "reason": "the biggest leverage theorem is still Q_R=0/no-boundary-charge plus source descent, now with coupling/source-scale ownership included",
            "effect": "2575 should attack the Q_R parent-zero signature or produce the first live finite q_R_hat/delta_p/kappa/ellJ input contract",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2574_0_selected",
            "selection_status": "selected",
            "target_file": "2575-Y5-R2FR-QR-parent-zero-signature-or-live-delta-p-coupling-input-row.md",
            "target_script": "scripts/Y5_R2FR_QR_parent_zero_signature_or_live_delta_p_coupling_input_row_2575.py",
            "task": "try to parent-sign Q_R=0 using boundary-charge, source-descent, matter/readout descent, projection-silence and coupling-owner clauses; if not, create the first live finite q_R_hat/delta_p/kappa/ellJ input-row contract for the PPN vector",
            "acceptance_target": "parent Q_R=0 theorem package or a strict source-normalized finite delta_p/q_R_hat/kappa/ellJ row that refuses closure/comparator/gamma-only/fitted-GM/cancellation-only scoring",
            "guardrails": "no GR Schwarzschild AB=1 import; no gamma-only pass; no closure zero; no fitted GM/H0 shortcut; no WEP/Ward shortcut; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "delta_p_proof": OUTPUTS["delta_p_proof"],
        "beta_gate": OUTPUTS["beta_gate"],
        "kernel_rows": OUTPUTS["kernel_rows"],
        "vector_requirements": OUTPUTS["vector_requirements"],
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
                    "copy_id": f"COPY2574_{key}",
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

    add("VAL2574_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2574_01_zero_flux_conditional",
        any(row["proof_id"] == "DPP2574_1_zero_flux_lemma" and row["status"] == "EXACT_CONDITIONAL_LEMMA" for row in data["delta_p"]),
        "delta_p zero route is exact conditional",
    )
    add(
        "VAL2574_02_parent_delta_p_not_claimed",
        any(row["proof_id"] == "DPP2574_3_parent_zero_verdict" and row["status"] == "NOT_DERIVED_CURRENT_CORPUS" for row in data["delta_p"]),
        "Q_R=0/delta_p=0 is not promoted",
    )
    add(
        "VAL2574_03_beta_gate_blocked",
        any(row["gate_id"] == "BETA2574_4_verdict" and row["status"] == "BETA_CLOSURE_NOT_DERIVED_CURRENT_CORPUS" for row in data["beta"]),
        "beta second-order closure is explicit and blocked",
    )
    add(
        "VAL2574_04_coupling_beta_present",
        any(row["gate_id"] == "BETA2574_2_source_coupling" for row in data["beta"]) and any(row["kernel_id"] == "DPK2574_4_coupling_source_beta" for row in data["kernels"]),
        "coupling/source-scale beta rows are present",
    )
    add(
        "VAL2574_05_preferred_templates",
        len(data["kernels"]) >= 5 and all(row["valid_for_claim"] is False for row in data["kernels"]),
        "disformal, endpoint, coupling, alpha_i, xi and readout kernels are source-ready nonclaim templates",
    )
    add(
        "VAL2574_06_vector_requirements",
        len(data["vector"]) >= 9 and any(row["component_id"] == "VREQ2574_2_kappa" for row in data["vector"]) and any(row["component_id"] == "VREQ2574_3_ellJ" for row in data["vector"]),
        "full PPN no-cancellation vector requirements include kappa and ellJ",
    )
    add(
        "VAL2574_07_live_input_contract",
        len(data["live_inputs"]) == 3 and all(row["valid_for_claim"] is False for row in data["live_inputs"]),
        "live input contract refuses missing/circular delta_p, beta and coupling rows",
    )
    add("VAL2574_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]), "no gate allows delta_p, beta, coupling, preferred-frame, PPN, local-GR or Newton claim")
    add(
        "VAL2574_09_next_target_written",
        any(row["route_id"] == "NEXT2574_0_selected" for row in data["next"]),
        "2575 Q_R parent-zero or live delta_p/coupling input target selected",
    )
    add("VAL2574_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2574*", "*P8_Y5_PPN_VECTOR_2574*", "*JR2574*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2574_11_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2574 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2574_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2574_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2574_OVERALL",
        overall,
        "2574 preserves delta_p zero as exact conditional, blocks beta/coupling/local claims, stages disformal endpoint coupling PPN kernels, and selects Q_R parent-zero/live input next",
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
        "# 2574 Y5 R2FR Delta_p Beta Disformal Coupling PPN Vector Or Parent Grammar Proof",
        "",
        "**Status:** private nonclaim checkpoint. The local-GR route is sharper but not claimed: `delta_p=0` follows from the exact zero-flux lemma only if `Q_R=0` is parent-signed, while beta remains a separate second-order source/coupling/readout gate.",
        "",
        "**Main result:** the best derivation target is now exact and upgraded for the coupling issue. Prove the parent no-boundary-charge/source-descent/coupling-owner package `Q_R=0`, and `C_R=0 -> delta_p=0` follows. Separately, prove EH/source/readout/no-extra-mode closure with fixed `kappa_MTS` and `ell_J`, and beta goes to one. If either route stalls, the full PPN vector must carry `d_R`, `w_R`, endpoint/readout tails, `Dln_kappa_MTS`, and `Dln_ell_J`; gamma-only and fitted-GM wins are refused.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Delta_p Zero Proof Audit",
        markdown_table(data["delta_p"], ["proof_id", "statement", "status", "missing_premise", "coupling_interaction", "consequence", "valid_for_claim"]),
        "",
        "## Beta Second-Order Coupling Gate",
        markdown_table(data["beta"], ["gate_id", "statement", "status", "required_inputs", "coupling_blocker", "failure_mode", "valid_for_claim"]),
        "",
        "## Disformal Coupling Endpoint PPN Kernel Rows",
        markdown_table(data["kernels"], ["kernel_id", "component", "candidate_map", "status", "bound_rows", "required_inputs", "coupling_extension", "valid_for_claim"]),
        "",
        "## Full PPN Vector Requirements",
        markdown_table(data["vector"], ["component_id", "required_for_claim", "current_status", "blocks", "coupling_dependency", "valid_for_claim"]),
        "",
        "## Live Input Contract",
        markdown_table(data["live_inputs"], ["input_id", "route_type", "required_fields", "relation", "reject_if", "status", "valid_for_claim"]),
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
        "delta_p": delta_p_proof_rows(),
        "beta": beta_gate_rows(),
        "kernels": kernel_rows(),
        "vector": vector_requirement_rows(),
        "live_inputs": live_input_contract_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["delta_p_proof"], data["delta_p"])
    write_csv(OUTPUTS["beta_gate"], data["beta"])
    write_csv(OUTPUTS["kernel_rows"], data["kernels"])
    write_csv(OUTPUTS["vector_requirements"], data["vector"])
    write_csv(OUTPUTS["live_input_contract"], data["live_inputs"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2574_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
