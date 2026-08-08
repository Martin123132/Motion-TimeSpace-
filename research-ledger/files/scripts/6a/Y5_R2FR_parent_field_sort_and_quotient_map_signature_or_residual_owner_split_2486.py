from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIELD_SORT_QUOTIENT_SIGNATURE_2486"
CHECKPOINT_ID = "2486"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_FIELD_QUOTIENT_2486_SOURCE_REGISTER.csv",
    "field_signature": OUT / "P8_Y5_FIELD_QUOTIENT_2486_FIELD_SIGNATURE_ATTEMPT.csv",
    "dq_vertical": OUT / "P8_Y5_FIELD_QUOTIENT_2486_DQ_VERTICAL_GENERATOR_LEDGER.csv",
    "matter_descent": OUT / "P8_Y5_FIELD_QUOTIENT_2486_MATTER_DESCENT_GATE.csv",
    "coefficient_descent": OUT / "P8_Y5_FIELD_QUOTIENT_2486_COEFFICIENT_DESCENT_GATE.csv",
    "readout_order": OUT / "P8_Y5_FIELD_QUOTIENT_2486_READOUT_ORDER_GATE.csv",
    "theorem_attempt": OUT / "P8_Y5_FIELD_QUOTIENT_2486_THEOREM_ATTEMPT.csv",
    "residual_split": OUT / "P8_Y5_FIELD_QUOTIENT_2486_RESIDUAL_OWNER_SPLIT.csv",
    "claim_gates": OUT / "P8_Y5_FIELD_QUOTIENT_2486_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_FIELD_QUOTIENT_2486_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_FIELD_QUOTIENT_2486_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_FIELD_QUOTIENT_2486_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2486_VALIDATION.csv",
}

COPY_TARGETS = {
    "field_signature": LOCAL_BOUNDS / "Parent_field_sort_quotient_attempt_2486_NONCLAIM.csv",
    "dq_vertical": LOCAL_BOUNDS / "Dq_vertical_generator_ledger_2486_NONCLAIM.csv",
    "residual_split": LOCAL_BOUNDS / "Residual_owner_split_2486_NONCLAIM.csv",
    "theorem_attempt": LOCAL_BOUNDS / "Quotient_chain_rule_theorem_attempt_2486_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2486_OBSERVED_COFRAME_FUNCTOR_VERTICAL_GENERATOR.csv",
}

SOURCES = [
    {
        "source_id": "SRC2486_00_2485_doc",
        "source_path": ROOT / "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md",
        "needles": ["NEXT2485_0_selected", "QD2485_0_parent_quotient", "VAL2485_OVERALL"],
        "role": "handoff selecting field-sort and quotient-map signature",
    },
    {
        "source_id": "SRC2486_01_863_chain_rule",
        "source_path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needles": ["CZT863_0_chain_rule_zero", "CZT863_1_matter_descent", "V863_4_coframe_chain_rule_zero"],
        "role": "conditional quotient chain-rule and matter-descent theorem shape",
    },
    {
        "source_id": "SRC2486_02_1874_RAB_visibility",
        "source_path": ROOT / "1874-Y5-R2FR-parent-domain-verticality-for-RAB-or-explicit-residual-field.md",
        "needles": ["PARENT_DOMAIN_VERTICALITY_NOT_DERIVED", "VAT1874_0_observer_cell_quotient", "VAL1874_OVERALL"],
        "role": "warning that R_AB is observer-cell visible under current map",
    },
    {
        "source_id": "SRC2486_03_1877_qshape",
        "source_path": ROOT / "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
        "needles": ["QSL1877_1_qshape_excludes_radial_cell", "EQ1877_3_readout_functor_test", "VAL1877_OVERALL"],
        "role": "q_shape attempt and DObs_e burden",
    },
    {
        "source_id": "SRC2486_04_1933_coefficient_descent",
        "source_path": ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
        "needles": ["QDT1933_1_vertical_zero", "TYPE1933_4_verdict", "VAL1933_OVERALL"],
        "role": "visible coefficient descent iff fiber-invariance is signed",
    },
    {
        "source_id": "SRC2486_05_1425_common_mode",
        "source_path": ROOT / "1425-Y5-R10-RAB-universal-metric-common-mode-WEP-zero-or-finite-source-demotion.md",
        "needles": ["CMZ1425_0_target", "PREM1425_0_parent_q_map", "VAL1425_9_overall"],
        "role": "matter quotient/common-mode WEP theorem remains unsigned",
    },
    {
        "source_id": "SRC2486_06_1427_parent_signature",
        "source_path": ROOT / "1427-Y5-R10-RAB-parent-action-signature-or-branch-locked-WEP-input-manifest.md",
        "needles": ["SIG1427_0_action_shape", "SIG1427_4_verdict", "VAL1427_7_overall"],
        "role": "ordinary matter action signature is closure candidate only",
    },
    {
        "source_id": "SRC2486_07_2237_vertical_null",
        "source_path": ROOT / "2237-Y5-R2FR-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
        "needles": ["NULL2237_0_parent_L_theta", "NULL2237_5_verdict", "VAL2237_OVERALL"],
        "role": "vertical generator requires parent theta/Omega and boundary-zero theorem",
    },
    {
        "source_id": "SRC2486_08_2300_q_normal_form",
        "source_path": ROOT / "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md",
        "needles": ["QEUL2300_0_q_equation", "QFC2300_6_verdict", "VAL2300_OVERALL"],
        "role": "q source-vector normal form and first-class removal failure",
    },
    {
        "source_id": "SRC2486_09_2466_source_bridge",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["CUR2466_A_Hilbert_energy_current", "HIL2466_0_define_T", "VAL2466_OVERALL"],
        "role": "Hilbert source current requires same observed coframe and no fitted GM",
    },
    {
        "source_id": "SRC2486_10_2485_validation",
        "source_path": OUT / "P8_Y5_BRR545_2485_VALIDATION.csv",
        "needles": ["VAL2485_OVERALL", "PASS"],
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


def field_signature_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "signature_id": "FSIG2486_0_public_geometry",
            "object": "g_mu_nu/e_obs",
            "proposed_sort": "public quotient geometry",
            "signature_attempt": "retain as q_parent-visible field varied in the EH/local branch",
            "current_result": "SIGNED_AS_CANDIDATE_NOT_PARENT_DERIVED",
            "missing_for_signature": "primitive definition of q_parent and proof no second public metric/coframe exists",
            "residual_owner_if_unsigned": "e_EH_hyp",
            "valid_for_claim": False,
        },
        {
            "signature_id": "FSIG2486_1_ordinary_matter",
            "object": "Psi and S_matter",
            "proposed_sort": "ordinary matter descends through public geometry",
            "signature_attempt": "S_matter=Sbar[Psi,e_obs(q_parent(Phi)),theta_obs]",
            "current_result": "CLOSURE_CANDIDATE_ONLY",
            "missing_for_signature": "parent argument list, no source-only prefactor theorem, constants owner",
            "residual_owner_if_unsigned": "finite_WEP_source_residual;E_norm",
            "valid_for_claim": False,
        },
        {
            "signature_id": "FSIG2486_2_q_private",
            "object": "q",
            "proposed_sort": "private reciprocal/source-vector representative",
            "signature_attempt": "q is vertical/first-class or has explicit source-vector equation",
            "current_result": "NOT_SIGNED_RESIDUAL_BRANCH_RETAINED",
            "missing_for_signature": "Omega/DCq first-class package or Ricci/Weyl source-vector split with bounds",
            "residual_owner_if_unsigned": "c_q_source;B_qW;C_qT;tail_q",
            "valid_for_claim": False,
        },
        {
            "signature_id": "FSIG2486_3_RAB_auxiliary",
            "object": "R_AB,lambda_R",
            "proposed_sort": "auxiliary compatibility variable or explicit residual field",
            "signature_attempt": "R_AB vertical under q_shape or removed by lambda_R/constraint before readout",
            "current_result": "VERTICALITY_REJECTED_FOR_CURRENT_OBSERVER_MAP",
            "missing_for_signature": "q_shape readout functor with DObs_e[v_R]=0 or constraint-first elimination",
            "residual_owner_if_unsigned": "c_aux;Z_R;q_R;DObs_e_R",
            "valid_for_claim": False,
        },
        {
            "signature_id": "FSIG2486_4_projector_readout",
            "object": "Pi_M,P_loc",
            "proposed_sort": "readout/projector operator fixed before variation",
            "signature_attempt": "variation-before-readout with fixed chain map",
            "current_result": "OBSTRUCTION_EXPLICIT_NOT_ZEROED",
            "missing_for_signature": "delta_g Pi_M=0, [d,Pi_M]J_H=0, and boundary/source support identity",
            "residual_owner_if_unsigned": "c_projector_operator",
            "valid_for_claim": False,
        },
        {
            "signature_id": "FSIG2486_5_memory_time_coframe",
            "object": "theta_obs,tau,Q_tau,C_tau",
            "proposed_sort": "public clock/coframe plus private memory residuals",
            "signature_attempt": "terminal public coframe and tau-lock make private memory locally invisible",
            "current_result": "TAU_FRAME_LOCK_UNSIGNED",
            "missing_for_signature": "tau_source=tau_charge=tau_clock=tau_readout and coframe descent",
            "residual_owner_if_unsigned": "c_memory_frame;e_clock_exchange",
            "valid_for_claim": False,
        },
        {
            "signature_id": "FSIG2486_6_boundary_reference",
            "object": "B_ref,Q_boundary,H_ref,S_GHY",
            "proposed_sort": "boundary/reference data fixed before local readout",
            "signature_attempt": "boundary terms are topological/reference-only or have zero local projection",
            "current_result": "BOUNDARY_CLASS_UNSIGNED",
            "missing_for_signature": "differentiable boundary charge, shared falloff class, zero compact linked-boundary flux",
            "residual_owner_if_unsigned": "c_boundary_operator;DeltaE_boundary",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def dq_vertical_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "dq_id": "DQ2486_0_chain_rule_template",
            "variable_direction": "any v in ker(Dq_parent)",
            "required_map": "Obs = Obs_bar(q_parent(Phi))",
            "dq_status": "EXACT_CONDITIONAL_TEMPLATE",
            "readout_status": "DObs[v]=DObs_bar(Dq[v])=0 if Obs is q-basic",
            "failure_mode": "template supplies no actual q_parent, v, or q-basic readout functor",
            "valid_for_claim": False,
        },
        {
            "dq_id": "DQ2486_1_public_metric",
            "variable_direction": "delta g or delta e_obs",
            "required_map": "Dq_parent[delta g] nonzero",
            "dq_status": "PUBLIC_NOT_VERTICAL",
            "readout_status": "varies EH and Hilbert stress",
            "failure_mode": "none; this is the public branch, not a zero direction",
            "valid_for_claim": False,
        },
        {
            "dq_id": "DQ2486_2_q_private",
            "variable_direction": "v_q",
            "required_map": "Dq_parent[v_q]=0 plus matter/boundary descent or first-class removal",
            "dq_status": "UNSIGNED",
            "readout_status": "q source-vector residual remains visible until first-class or Weyl/source channels close",
            "failure_mode": "B_qW Weyl tail, C_qT matter trace, body/boundary/readout tails",
            "valid_for_claim": False,
        },
        {
            "dq_id": "DQ2486_3_RAB",
            "variable_direction": "v_R changes R_AB=2 ln(J_q)",
            "required_map": "Dq_shape[v_R]=0 and DObs_e[v_R]=0, or constraint-first removal",
            "dq_status": "REJECTED_FOR_OBSERVER_CELL_MAP",
            "readout_status": "Dq[v_R] != 0 under current observer-cell map; q_shape alone leaves DObs_e burden",
            "failure_mode": "R_AB remains explicit residual field and cannot be called vertical by declaration",
            "valid_for_claim": False,
        },
        {
            "dq_id": "DQ2486_4_memory_frame",
            "variable_direction": "v_memory,v_tau_private",
            "required_map": "public coframe/time functor is insensitive to private memory directions",
            "dq_status": "UNSIGNED",
            "readout_status": "preferred-frame and clock residuals remain live",
            "failure_mode": "PPN alpha_i, clock drift, tau-lock mismatch",
            "valid_for_claim": False,
        },
        {
            "dq_id": "DQ2486_5_projector",
            "variable_direction": "delta Pi_M or post-readout projection",
            "required_map": "Pi_M fixed before variation or included in q_parent/readout derivative",
            "dq_status": "NOT_A_ZERO_DIRECTION_YET",
            "readout_status": "delta Pi_M and [d,Pi_M]J_H remain exact obstruction terms",
            "failure_mode": "source normalization can be readout-dependent",
            "valid_for_claim": False,
        },
        {
            "dq_id": "DQ2486_6_boundary",
            "variable_direction": "boundary/corner/reference variation",
            "required_map": "boundary changes have zero local projection or fixed variational class",
            "dq_status": "UNSIGNED",
            "readout_status": "boundary charge can survive even when bulk variation is vertical",
            "failure_mode": "H_ref/B_ref/corner charge contaminates local source/readout",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def matter_descent_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "MD2486_0_chain_rule",
            "statement": "If S_matter factors through e_obs(q_parent(Phi)) and theta_obs(q_parent(Phi)), then vertical representative variations do not directly source matter.",
            "proof_status": "EXACT_CONDITIONAL",
            "proof_sketch": "delta_v S_matter = (delta S/de_obs)DObs_e(Dq[v]) + (delta S/dtheta)Dtheta(Dq[v]) = 0 when v in ker(Dq) and readouts are q-basic",
            "current_blocker": "q_parent, q-basic readout functor, no-marker matter argument list and constants owner are unsigned",
            "residual_if_unsigned": "finite_WEP_source_residual;Pi_I_matter;c_memory_frame",
            "valid_for_claim": False,
        },
        {
            "gate_id": "MD2486_1_no_source_prefactor",
            "statement": "Ordinary matter has no active source-only prefactors w_A depending on hidden/representative data.",
            "proof_status": "NOT_DERIVED",
            "proof_sketch": "1425/1427 keep the common-mode theorem as a closure candidate only",
            "current_blocker": "parent object-language admissibility and action-measure owner missing",
            "residual_if_unsigned": "finite_WEP_source_weight",
            "valid_for_claim": False,
        },
        {
            "gate_id": "MD2486_2_Hilbert_source",
            "statement": "Hilbert stress T_H from the same observed geometry is the source of the local Poisson branch.",
            "proof_status": "PASS_AS_CONTRACT_NOT_FULL_ZERO",
            "proof_sketch": "2466/2481 give the least-circular Hilbert source-current route",
            "current_blocker": "ell_J parent scale, dynamic exchange, jump/support, e_kappaG and projector/readout order remain open",
            "residual_if_unsigned": "E_norm",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coefficient_descent_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "coeff_id": "CD2486_0_descent_theorem",
            "coefficient_family": "visible constants/couplings",
            "conditional_result": "if c_vis=q_parent^* c_bar, then dc_vis(v)=0 for all v in ker(Dq_parent)",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_parent_input": "fiber invariance for every visible coefficient and readout/boundary map",
            "residual_if_unsigned": "e_coeff_descent",
            "valid_for_claim": False,
        },
        {
            "coeff_id": "CD2486_1_kappa",
            "coefficient_family": "a1/kappa_MTS/G_parent",
            "conditional_result": "G_parent is downstream of a1 after parent normal form owns the EH coefficient",
            "current_status": "MISSING_COEFFICIENT_OWNER",
            "missing_parent_input": "primitive scale/coupling or parent normalization",
            "residual_if_unsigned": "e_kappaG",
            "valid_for_claim": False,
        },
        {
            "coeff_id": "CD2486_2_source_weight",
            "coefficient_family": "ordinary source weights w_A",
            "conditional_result": "WEP/common-mode zero follows if no hidden source-prefactor is allowed",
            "current_status": "NOT_DERIVED",
            "missing_parent_input": "action-measure owner and no-source-prefactor theorem",
            "residual_if_unsigned": "finite_WEP_source_weight",
            "valid_for_claim": False,
        },
        {
            "coeff_id": "CD2486_3_alpha_clock_mass",
            "coefficient_family": "alpha_EM, clock frequencies, masses/binding",
            "conditional_result": "local constants are silent if quotient-owned and fiber-invariant",
            "current_status": "UNSIGNED_HARD_BLOCKER",
            "missing_parent_input": "constants owner, radiative stability, material-marker exclusion",
            "residual_if_unsigned": "R_alpha;R_clock;R_mass;R_binding",
            "valid_for_claim": False,
        },
        {
            "coeff_id": "CD2486_4_boundary_projection",
            "coefficient_family": "boundary/readout projection coefficients",
            "conditional_result": "boundary constants are silent if fixed before readout or q-basic",
            "current_status": "UNSIGNED",
            "missing_parent_input": "boundary reference lock and readout-order theorem",
            "residual_if_unsigned": "c_boundary_operator;c_projector_operator",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def readout_order_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "readout_id": "RO2486_0_variation_before_readout",
            "rule": "derive Euler equations before applying observational projectors or fitted source maps",
            "current_status": "GUARDRAIL_ACTIVE",
            "blocked_shortcut": "post-readout projector treated as if it commuted with variation",
            "residual_if_unsigned": "c_projector_operator",
            "valid_for_claim": False,
        },
        {
            "readout_id": "RO2486_1_same_frame",
            "rule": "matter, clocks, rods, photons, source current and orbit readout use the same observed coframe/metric",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "blocked_shortcut": "using one frame for matter and another for clock/orbital normalization",
            "residual_if_unsigned": "c_memory_frame;E_norm;PPN_alpha_i",
            "valid_for_claim": False,
        },
        {
            "readout_id": "RO2486_2_no_fitted_GM",
            "rule": "source mass/coupling cannot be defined by observed orbital GM",
            "current_status": "PASS_GUARDRAIL",
            "blocked_shortcut": "using Newtonian target behavior to prove Newton",
            "residual_if_unsigned": "E_norm;e_kappaG",
            "valid_for_claim": False,
        },
        {
            "readout_id": "RO2486_3_local_global_split",
            "rule": "global/cosmological memory variables may be FLRW-visible only if locally invisible to rods/clocks/PPN readout",
            "current_status": "UNSIGNED_PARENT_SPLIT",
            "blocked_shortcut": "letting cosmology memory leak disappear locally without a quotient theorem",
            "residual_if_unsigned": "q_loc_trace_leak;PPN_clock_WEP_residuals",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "THM2486_0_chain_rule_descent",
            "statement": "For any parent variable direction v with Dq_parent[v]=0, every q-basic local observable O=Obar(q_parent(Phi)) satisfies DO[v]=0.",
            "proof_status": "PROVED_CONDITIONALLY",
            "proof_sketch": "DO[v]=DObar(Dq_parent[v])=DObar(0)=0",
            "current_application": "usable only after q_parent, v and q-basic readout functors are parent-signed",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2486_1_matter_blindness",
            "statement": "If S_matter is a q-basic functional of e_obs/theta_obs and visible constants descend through q, then vertical private variables do not source ordinary matter.",
            "proof_status": "PROVED_CONDITIONALLY",
            "proof_sketch": "combine THM2486_0 with Hilbert variation of S_matter and coefficient descent",
            "current_application": "blocked by no-source-prefactor, constants owner and q-basic coframe/readout clauses",
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM2486_2_current_signature_application",
            "statement": "Apply the quotient signature to current MTS field list.",
            "proof_status": "FAILS_CURRENT_SIGNATURE_GATE",
            "proof_sketch": "q_private, R_AB, projector, memory/coframe, constants and boundary slots lack parent-signed Dq/Omega/readout clauses; R_AB verticality is explicitly rejected under the current observer-cell map",
            "current_application": "split unsigned variables into residual owners rather than claiming local-GR silence",
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_split_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "owner_id": "RS2486_0_EH_hyp",
            "unsigned_object": "public geometry uniqueness and q_parent field list",
            "owner_residual": "e_EH_hyp",
            "zero_or_bound_requirement": "single public metric/coframe and q_parent field list parent-signed",
            "test_arenas": "local_GR;PPN;Newton",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_1_q_source",
            "unsigned_object": "q_private verticality/source-vector channels",
            "owner_residual": "c_q_source;B_qW;C_qT;tail_q",
            "zero_or_bound_requirement": "q first-class removal, source-vector zero, or source-backed bounds",
            "test_arenas": "PPN;R10;orbital;clocks",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_2_RAB",
            "unsigned_object": "R_AB/q_shape/readout functor",
            "owner_residual": "DObs_e_R;c_aux;Z_R;q_R",
            "zero_or_bound_requirement": "DObs_e[v_R]=0 from q-basic coframe functor or constraint-first elimination",
            "test_arenas": "PPN;R10;WEP;clocks;orbital",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_3_matter_descent",
            "unsigned_object": "ordinary matter no-marker/no-source-prefactor signature",
            "owner_residual": "finite_WEP_source_weight;Pi_I_matter",
            "zero_or_bound_requirement": "S_matter descends through one observed coframe and no active source-only weights",
            "test_arenas": "WEP;source_normalization;local_GR",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_4_coefficients",
            "unsigned_object": "visible coefficient descent",
            "owner_residual": "e_coeff_descent;R_alpha;R_clock;R_mass;R_binding",
            "zero_or_bound_requirement": "visible constants are q-fiber invariant or source-backed finite rows exist",
            "test_arenas": "EM;clocks;WEP;particle_mass",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_5_projector",
            "unsigned_object": "projector/readout order",
            "owner_residual": "c_projector_operator",
            "zero_or_bound_requirement": "Pi_M fixed chain map with delta_g Pi_M=0 and [d,Pi_M]J_H=0",
            "test_arenas": "source_normalization;R10;orbital;local_GR",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_6_memory_frame",
            "unsigned_object": "memory/coframe/tau-lock",
            "owner_residual": "c_memory_frame;e_clock_exchange;PPN_alpha_i",
            "zero_or_bound_requirement": "terminal public coframe and tau_source=tau_charge=tau_clock=tau_readout",
            "test_arenas": "PPN;clocks;orbital",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_7_boundary",
            "unsigned_object": "boundary/reference/falloff class",
            "owner_residual": "c_boundary_operator;DeltaE_boundary",
            "zero_or_bound_requirement": "differentiable boundary charge and zero compact linked-boundary flux",
            "test_arenas": "R10;orbital;local_GR;Green_bounds",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RS2486_8_source_normalization",
            "unsigned_object": "Hilbert source worldtube and parent coupling",
            "owner_residual": "E_norm;e_kappaG",
            "zero_or_bound_requirement": "kappa_MTS owner, dynamic exchange identity, jump/support theorem and no fitted GM",
            "test_arenas": "Newton;local_GR;orbital;R10",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2486_0_chain_rule",
            "claim": "Quotient chain-rule zero theorem is available conditionally.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "DObs[v]=DObar(Dq[v]) gives exact zero if q_parent and q-basic readout are signed.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2486_1_q_parent_signed",
            "claim": "Current MTS corpus signs q_parent and all needed vertical generators.",
            "gate_status": "BLOCKED",
            "reason": "field-by-field q_parent, ker(Dq), theta/Omega and boundary-zero proofs are missing.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2486_2_RAB_vertical",
            "claim": "R_AB is locally vertical/invisible.",
            "gate_status": "BLOCKED",
            "reason": "observer-cell map sees R_AB; q_shape still needs DObs_e[v_R]=0.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2486_3_matter_descent",
            "claim": "Ordinary matter is blind to representative variables.",
            "gate_status": "BLOCKED",
            "reason": "no-marker/no-source-prefactor and constants descent are not parent-signed.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2486_4_local_GR_Newton",
            "claim": "Newton/local-GR reduction is derived.",
            "gate_status": "BLOCKED",
            "reason": "q_parent, EH origin, kappa owner, residual silence, source normalization and PPN equations remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2486_5_no_shortcuts",
            "claim": "No variable is declared vertical without Dq/Omega/readout proof.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "R_AB/q_shape and matter descent shortcuts are explicitly refused as claims.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2486_0_result",
            "decision": "Keep quotient descent as the cleanest theorem route, but do not sign q_parent yet.",
            "reason": "The chain-rule theorem is exact, but the current corpus lacks field-by-field q_parent, Dq generators and q-basic readout functors.",
            "effect": "the work moves from vague quotient language to a precise proof checklist.",
        },
        {
            "decision_id": "DEC2486_1_RAB",
            "decision": "Classify R_AB as residual under the current observer-cell map.",
            "reason": "Dq[v_R] is nonzero unless q_shape/readout or constraint-first elimination is supplied.",
            "effect": "no R_AB verticality, beta-zero, C_R-zero, or local-GR language is allowed from this branch yet.",
        },
        {
            "decision_id": "DEC2486_2_next",
            "decision": "Attack observed coframe/readout functor and vertical-generator certificate next.",
            "reason": "Dq[v]=0 only matters for physics if e_obs, clocks, matter stress, source mass and boundary readouts are q-basic.",
            "effect": "2487 should try to prove DObs_e[v_X]=0 or emit finite readout-leak rows.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2486_0_selected",
            "selection_status": "selected",
            "target_file": "2487-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md",
            "target_script": "scripts/Y5_R2FR_observed_coframe_functor_and_vertical_generator_certificate_or_DObs_leak_row_2487.py",
            "task": "try to construct the observed coframe/readout functor E(q_parent) and field-by-field vertical generators v_X proving DObs_e[v_X]=0 for q/R_AB/memory/projector directions; if not, emit finite DObs/readout-leak residual rows",
            "acceptance_target": "DObs_e kernel theorem attempt, vertical generator table, q-basic readout checklist, residual leak rows, all GR/Newton claims blocked",
            "guardrails": "no declaring Dq=0 enough; no R_AB verticality under observer-cell map; no fitted GM; no EH import; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "field_signature": OUTPUTS["field_signature"],
        "dq_vertical": OUTPUTS["dq_vertical"],
        "residual_split": OUTPUTS["residual_split"],
        "theorem_attempt": OUTPUTS["theorem_attempt"],
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
                    "copy_id": f"COPY2486_{key}",
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

    add("VAL2486_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2486_01_chain_rule_written",
        any(row["theorem_id"] == "THM2486_0_chain_rule_descent" and row["proof_status"] == "PROVED_CONDITIONALLY" for row in data["theorems"]),
        "conditional quotient chain-rule theorem is written",
    )
    add(
        "VAL2486_02_q_parent_unsigned",
        any(row["dq_id"] == "DQ2486_0_chain_rule_template" and row["dq_status"] == "EXACT_CONDITIONAL_TEMPLATE" for row in data["dq"]),
        "q_parent route remains a template without parent signature",
    )
    add(
        "VAL2486_03_RAB_rejected_current_map",
        any(row["dq_id"] == "DQ2486_3_RAB" and row["dq_status"] == "REJECTED_FOR_OBSERVER_CELL_MAP" for row in data["dq"]),
        "R_AB verticality rejected under current observer-cell map",
    )
    add(
        "VAL2486_04_matter_descent_blocked",
        any(row["gate_id"] == "MD2486_1_no_source_prefactor" and row["proof_status"] == "NOT_DERIVED" for row in data["matter"]),
        "matter no-source-prefactor theorem remains blocked",
    )
    add(
        "VAL2486_05_coefficient_descent_blocked",
        any(row["coeff_id"] == "CD2486_0_descent_theorem" and row["current_status"] == "EXACT_CONDITIONAL_NOT_PARENT_SIGNED" for row in data["coefficients"]),
        "coefficient descent is exact conditional but not parent-signed",
    )
    add(
        "VAL2486_06_residual_split_complete",
        len(data["residuals"]) >= 9 and all(row["valid_for_claim"] is False for row in data["residuals"]),
        "unsigned variables split into nonclaim residual owners",
    )
    add("VAL2486_07_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2486_08_next_target_written",
        any(row["route_id"] == "NEXT2486_0_selected" for row in data["next"]),
        "2487 observed-coframe functor target selected",
    )
    add("VAL2486_09_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2486*", "*P8_Y5_FIELD_QUOTIENT_2486*", "*JR2486*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2486_10_no_formalization_artifacts", not formalization_artifacts, "no 2486 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2486_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2486_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2486_OVERALL",
        overall,
        "2486 proves the quotient chain-rule only conditionally, rejects cheap verticality, splits residual owners, and selects DObs/readout functor next",
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
        "# 2486 Y5 R2FR Parent Field Sort And Quotient Map Signature Or Residual Owner Split",
        "",
        "**Status:** quotient descent gives a real conditional theorem, but the current corpus does not parent-sign `q_parent`, the vertical generators, or the observed readout functors needed for a local-GR claim.",
        "",
        "**Main result:** `Dq[v]=0` is not enough. The useful theorem is `DObs[v]=DObs_bar(Dq[v])=0`, which requires the visible coframe, matter stress, clocks, source mass, coefficients and boundary/readout maps to be `q`-basic. Current sources prove this only conditionally. In particular, `R_AB` is visible under the available observer-cell map, and the `q_shape` escape still needs `DObs_e[v_R]=0`. Therefore every unsigned variable is split into an explicit residual owner.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Field Signature Attempt",
        markdown_table(data["fields"], ["signature_id", "object", "proposed_sort", "signature_attempt", "current_result", "missing_for_signature", "residual_owner_if_unsigned", "valid_for_claim"]),
        "",
        "## Dq / Vertical Generator Ledger",
        markdown_table(data["dq"], ["dq_id", "variable_direction", "required_map", "dq_status", "readout_status", "failure_mode", "valid_for_claim"]),
        "",
        "## Matter Descent Gate",
        markdown_table(data["matter"], ["gate_id", "statement", "proof_status", "proof_sketch", "current_blocker", "residual_if_unsigned", "valid_for_claim"]),
        "",
        "## Coefficient Descent Gate",
        markdown_table(data["coefficients"], ["coeff_id", "coefficient_family", "conditional_result", "current_status", "missing_parent_input", "residual_if_unsigned", "valid_for_claim"]),
        "",
        "## Readout Order Gate",
        markdown_table(data["readout"], ["readout_id", "rule", "current_status", "blocked_shortcut", "residual_if_unsigned", "valid_for_claim"]),
        "",
        "## Theorem Attempt",
        markdown_table(data["theorems"], ["theorem_id", "statement", "proof_status", "proof_sketch", "current_application", "claim_allowed"]),
        "",
        "## Residual Owner Split",
        markdown_table(data["residuals"], ["owner_id", "unsigned_object", "owner_residual", "zero_or_bound_requirement", "test_arenas", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
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
        "fields": field_signature_rows(),
        "dq": dq_vertical_rows(),
        "matter": matter_descent_rows(),
        "coefficients": coefficient_descent_rows(),
        "readout": readout_order_rows(),
        "theorems": theorem_attempt_rows(),
        "residuals": residual_split_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["field_signature"], data["fields"])
    write_csv(OUTPUTS["dq_vertical"], data["dq"])
    write_csv(OUTPUTS["matter_descent"], data["matter"])
    write_csv(OUTPUTS["coefficient_descent"], data["coefficients"])
    write_csv(OUTPUTS["readout_order"], data["readout"])
    write_csv(OUTPUTS["theorem_attempt"], data["theorems"])
    write_csv(OUTPUTS["residual_split"], data["residuals"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
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
