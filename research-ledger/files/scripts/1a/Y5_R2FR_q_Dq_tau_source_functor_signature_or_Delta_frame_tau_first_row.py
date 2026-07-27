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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1780"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1780_0_1779_handoff",
        "source_key": "1779_handoff",
        "source_path": ROOT / "1779-Y5-R2FR-parent-current-one-observed-source-functor-or-Delta-Hsrc-first-row.md",
        "needles": ["NEXT1779_0_primary", "CAJ1779_1_q_Dq_observed_coframe", "DHC1779_1_frame_tau"],
    },
    {
        "source_id": "SRC1780_1_1779_validation",
        "source_key": "1779_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1779_VALIDATION.csv",
        "needles": ["VAL1779_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1780_2_1779_join",
        "source_key": "1779_common_antecedent_join",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1779_COMMON_ANTECEDENT_JOIN.csv",
        "needles": ["CAJ1779_1_q_Dq_observed_coframe", "CAJ1779_2_tau_projectability"],
    },
    {
        "source_id": "SRC1780_3_1734_projectability",
        "source_key": "1734_projectability_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_DQ_TAU_PROJECTABILITY_AUDIT.csv",
        "needles": ["DTP1734_0_q_map", "DTP1734_6_verdict"],
    },
    {
        "source_id": "SRC1780_4_1734_leak_rows",
        "source_key": "1734_theta_qtau_leak_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv",
        "needles": ["TLR1734_0_Dq_tau_commutator", "TLR1734_4_total_theta_qtau_leak"],
    },
    {
        "source_id": "SRC1780_5_1737_qmap",
        "source_key": "1737_q_map_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv",
        "needles": ["QMAP1737_0_Q_vis", "QMAP1737_2_source_readout"],
    },
    {
        "source_id": "SRC1780_6_1737_vertical_basis",
        "source_key": "1737_vertical_basis_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv",
        "needles": ["VB1737_0_vZ", "VB1737_5_vtau_readout"],
    },
    {
        "source_id": "SRC1780_7_1737_coframe_zero",
        "source_key": "1737_coframe_functor_zero",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv",
        "needles": ["CFZ1737_0_exact_conditional", "CFZ1737_3_current_verdict"],
    },
    {
        "source_id": "SRC1780_8_1738_kernel",
        "source_key": "1738_kernel_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_KERNEL_THEOREM_ATTEMPT.csv",
        "needles": ["DOK1738_0_chain_rule_kernel", "DOK1738_2_current_verdict"],
    },
    {
        "source_id": "SRC1780_9_1738_clause_audit",
        "source_key": "1738_coframe_kernel_clause",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_COFRAME_KERNEL_CLAUSE_AUDIT.csv",
        "needles": ["OCK1738_0_parent_q", "OCK1738_6_verdict"],
    },
    {
        "source_id": "SRC1780_10_1739_owner",
        "source_key": "1739_parent_coframe_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_CLAUSE_GATE.csv",
        "needles": ["PCO1739_0_parent_q", "PCO1739_6_no_source_prefactor"],
    },
    {
        "source_id": "SRC1780_11_1740_shadow_frame",
        "source_key": "1740_no_shadow_frame",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_CLAUSE_GATE.csv",
        "needles": ["NSF1740_0_parent_matter_domain", "NSF1740_6_verdict"],
    },
    {
        "source_id": "SRC1780_12_1760_descent_premise",
        "source_key": "1760_matter_descent_premise",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_DESCENT_PREMISE_AUDIT.csv",
        "needles": ["PRE1760_0_q_map", "PRE1760_7_hilbert_source_owner"],
    },
    {
        "source_id": "SRC1780_13_1760_descent_attempt",
        "source_key": "1760_matter_worldtube_descent",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
        "needles": ["MWD1760_1_conditional_theorem", "MWD1760_4_current_verdict"],
    },
    {
        "source_id": "SRC1780_14_1720_matter_functor",
        "source_key": "1720_matter_functor_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_1_observed_coframe_descent", "MFS1720_8_verdict"],
    },
    {
        "source_id": "SRC1780_15_1768_source_map",
        "source_key": "1768_source_map_identity",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SOURCE_MAP_IDENTITY_GATE.csv",
        "needles": ["SMG1768_1_no_shadow_map_gate", "SMG1768_4_current_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_SOURCE_REGISTER.csv",
    "signature_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_FRAME_TAU_ZERO_THEOREM_ATTEMPT.csv",
    "delta_frame_tau_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_DELTA_FRAME_TAU_FIRST_ROW_SCHEMA.csv",
    "source_current_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_SOURCE_CURRENT_IMPACT_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1780_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1780 q/Dq/tau/source-functor signature and Delta_frame_tau evidence",
            }
        )
    return rows


def signature_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_0_parent_q_map",
            "signature_clause": "parent quotient map q exists before readout",
            "mathematical_form": "q: Phi_parent -> Q_vis with Q_vis=(e_obs,g_obs,source/readout data,theta_owned)",
            "current_status": "Q_NOT_COMPUTABLE_CURRENT_CORPUS",
            "source_basis": "DTP1734_0;QMAP1737_0;OCK1738_0;PRE1760_0",
            "blocks": "Dq[v]=0, coframe factorisation, matter descent, tau pushforward",
            "exit_condition": "field chart plus explicit q and Dq on every retained local direction",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_1_Dq_kernel_basis",
            "signature_clause": "Dq kernel and vertical basis are explicit",
            "mathematical_form": "Dq[v_a]=0 for declared vertical directions v_Z,v_phi,v_RAB/Jq,v_boundary, or finite Dq rows",
            "current_status": "Dq_KERNEL_UNSIGNED",
            "source_basis": "DTP1734_1;VB1737_0..5;OCK1738_2",
            "blocks": "chain-rule zero and projectability cannot be applied componentwise",
            "exit_condition": "computed Dq matrix/components with source paths and units, or theorem-zero per direction",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_2_observed_coframe_functor",
            "signature_clause": "observed coframe factors through q",
            "mathematical_form": "e_obs(Phi)=Obs_e(q(Phi)); DObs_e[v]=DObs_e[Dq(v)]",
            "current_status": "COFRAME_FUNCTOR_ZERO_NOT_SIGNED",
            "source_basis": "CFZ1737_0;DOK1738_0;OCK1738_1;PCO1739_1",
            "blocks": "same frame could still carry residual common-frame derivative",
            "exit_condition": "Obs_e(q) parent owner plus b_g,X=0 theorem or finite b_g rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_3_tau_projectability",
            "signature_clause": "one observed tau is projectable through q and fixed across roles",
            "mathematical_form": "Dq(L_tau Phi)=L_tau_red q(Phi); tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary",
            "current_status": "MISSING_TAU_PROJECTABILITY_AND_LOCK",
            "source_basis": "DTP1734_2;TLR1734_0;MFS1720_5;CAJ1779_2",
            "blocks": "H_tau and J_H[tau] may use different time/readout directions",
            "exit_condition": "tau pushforward, stationarity/admissibility, and role-lock certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_4_source_readout_functor",
            "signature_clause": "source, clocks, orbits, boundary, and readout are functors of Q_vis",
            "mathematical_form": "Dsource_readout[Dq(v)]=0 and Dclock/Dorbit/Dboundary use the same Q_vis data",
            "current_status": "READOUT_FUNCTOR_NOT_PARENT_SIGNED",
            "source_basis": "QMAP1737_2;TLR1734_1;PCO1739_4;PRE1760_5",
            "blocks": "source-readout frame can reopen a killed coframe direction",
            "exit_condition": "one readout functor or finite source/clock/orbit/boundary leakage row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_5_matter_functor_signature",
            "signature_clause": "ordinary matter action is a functor of e_obs, owned connection, and fixed representation data",
            "mathematical_form": "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A] plus owned/gauge matter lift",
            "current_status": "MATTER_FUNCTOR_SIGNATURE_NOT_PARENT_SIGNED",
            "source_basis": "MFS1720_2;MFS1720_3;PRE1760_2;MWD1760_1",
            "blocks": "Hilbert current remains conditional rather than a parent-owned observed source",
            "exit_condition": "parent matter category, matter lift, and connection lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_6_constants_no_shadow",
            "signature_clause": "constants/material labels and source maps are quotient-owned, universal, or bounded",
            "mathematical_form": "Lie_v theta_A=0 and not exists F_shadow(T_H,labels) or source-only w_A(X)S_A",
            "current_status": "SOURCE_SHADOW_AND_CONSTANT_OWNER_UNSIGNED",
            "source_basis": "MFS1720_4;MFS1720_6;NSF1740_3;SMG1768_1",
            "blocks": "source-only prefactors can alter active source while preserving ordinary-looking matter equations",
            "exit_condition": "no-shadow/source-prefactor theorem plus constant superselection, or finite Delta_shadow row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QTS1780_7_verdict",
            "signature_clause": "q/Dq/tau/source-functor signature is signed in one parent branch",
            "mathematical_form": "QTS1780_0 through QTS1780_6 pass simultaneously",
            "current_status": "SIGNATURE_NOT_SIGNED",
            "source_basis": "1779 convergence handoff plus 1734/1737/1738/1739/1740/1760/1720 rows",
            "blocks": "Delta_frame_tau remains mandatory and source-measure proof cannot be promoted",
            "exit_condition": "all gate clauses theorem-zero/source-backed with no placeholders",
            "valid_for_claim": False,
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "FTZ1780_0_chain_rule_core",
            "claim": "coframe/tau/source leakage vanishes by quotient factorisation",
            "mathematical_form": "if e_obs=Obs_e(q(Phi)), Dq[v]=0, and tau is q-projectable, then DObs_e[v]=0 and Delta_tau[v]=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "q, Dq kernel, Obs_e(q), tau pushforward, and role lock are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "FTZ1780_1_matter_pullback",
            "claim": "ordinary Hilbert source is blind to vertical directions when the matter functor factors through q",
            "mathematical_form": "delta_v S_matter = 0 if S_matter=S_matter[Psi,e_obs(q),omega[e_obs],theta] and Lie_v theta=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "matter functor, constants, matter lift, worldtube support, and boundary silence remain unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "FTZ1780_2_no_shadow_guard",
            "claim": "same coframe is not sufficient if a common Weyl/disformal/source frame depends on residual variables",
            "mathematical_form": "e_obs=exp(b_g X)e0 gives DObs_e[partial_X]=b_g e_obs even though all matter sees one frame",
            "proof_status": "COUNTERMODEL_EXPOSED",
            "missing_for_current_claim": "b_g,X=0/no-shadow theorem or finite common-frame/source-prefactor rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "FTZ1780_3_Delta_frame_tau_definition",
            "claim": "failed signature becomes a first residual row rather than a hidden assumption",
            "mathematical_form": "Delta_frame_tau := ||DObs_e[Dq(v)]|| + ||Dsource_readout[Dq(v)]|| + ||Delta_tau_roles|| + ||Dtheta_A[v]|| + ||F_shadow-T_H||",
            "proof_status": "RESIDUAL_IDENTITY_STAGED",
            "missing_for_current_claim": "component values, norms, units, source paths, M_H_ref or declared normalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "FTZ1780_4_current_verdict",
            "claim": "current MTS proves Delta_frame_tau=0",
            "mathematical_form": "QTS1780_0 through QTS1780_6 pass and all frame/tau/source components vanish",
            "proof_status": "FAIL_CURRENT_PARENT_PROOF",
            "missing_for_current_claim": "q/Dq/tau/source-functor signature and no-shadow rows",
            "valid_for_claim": False,
        },
    ]


def delta_frame_tau_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DFT1780_0_DObs_e",
            "quantity": "DObs_e_vertical_leak",
            "definition": "observed coframe derivative along retained vertical directions",
            "formula": "sum_a ||DObs_e[v_a]|| for v_a in declared vertical basis",
            "required_columns": "direction_id;Dq_component;DObs_e_value;coframe_norm;source_path;units;valid_for_claim",
            "current_status": "MISSING_PARENT_Q_DQ_OBS_E_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DFT1780_1_Dreadout",
            "quantity": "Dsource_readout_leak",
            "definition": "source, clock, orbit, boundary, or detector readout derivative along quotient leak directions",
            "formula": "||Dsource_readout[Dq(v)]||+||Dclock[Dq(v)]||+||Dorbit[Dq(v)]||+||Dboundary[Dq(v)]||",
            "required_columns": "system_id;readout_map;direction_id;component_value;norm;source_path;units;valid_for_claim",
            "current_status": "MISSING_SOURCE_READOUT_FUNCTOR_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DFT1780_2_tau_roles",
            "quantity": "Delta_tau_role_lock",
            "definition": "difference between source, charge, clock, orbit, and boundary tau roles",
            "formula": "||tau_source-tau_charge||+||tau_clock-tau_charge||+||tau_orbit-tau_charge||+||tau_boundary-tau_charge||",
            "required_columns": "tau_source;tau_charge;tau_clock;tau_orbit;tau_boundary;norm;source_path;units;valid_for_claim",
            "current_status": "MISSING_TAU_PROJECTABILITY_ROLE_LOCK",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DFT1780_3_constants_marker",
            "quantity": "Dtheta_marker_leak",
            "definition": "material constants, mass scales, fine-structure/charge units, or source labels vary along residual directions",
            "formula": "sum_A ||Lie_v theta_A|| + ||D_marker[Dq(v)]||",
            "required_columns": "constant_id;direction_id;Lie_v_theta;marker_component;source_path;units;valid_for_claim",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DFT1780_4_shadow_frame_source",
            "quantity": "Delta_shadow_frame_source",
            "definition": "hidden Weyl/disformal/source-only prefactor or post-readout source map",
            "formula": "abs(b_g,X)+abs(C_X)+abs(D_X)+abs(delta_w_shadow)+abs(delta_w_block)",
            "required_columns": "shadow_type;coefficient;operator_basis;arena_projection;source_path;units;valid_for_claim",
            "current_status": "MISSING_NO_SHADOW_THEOREM_OR_BOUND",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DFT1780_5_worldtube_boundary",
            "quantity": "Delta_worldtube_boundary_tau",
            "definition": "worldtube support or boundary term changes under vertical/frame/tau variation",
            "formula": "||delta_v W_source||+||Pi_local delta_v B_A||+||boundary_tau_shift||",
            "required_columns": "worldtube_id;surface_pair;boundary_term;support_variation;tau_shift;source_path;units;valid_for_claim",
            "current_status": "MISSING_WORLDTUBE_BOUNDARY_SILENCE_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DFT1780_6_total_abs",
            "quantity": "epsilon_Delta_frame_tau_abs",
            "definition": "absolute no-cancellation envelope for frame/tau/source-functor mismatch",
            "formula": "abs(DFT1780_0)+abs(DFT1780_1)+abs(DFT1780_2)+abs(DFT1780_3)+abs(DFT1780_4)+abs(DFT1780_5)",
            "required_columns": "component_values;component_source_paths;normalizer;units;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def source_current_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "SCI1780_0_Delta_Hsrc",
            "open_quantity": "Delta_frame_tau feeds Delta_Hsrc",
            "impact": "if frame/tau/source functor is not signed, H_tau and Pi_M^H J_H^dress are not comparable",
            "claim_effect": "source-measure lemma remains unpromoted",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "SCI1780_1_Newton",
            "open_quantity": "source-normalized Newton",
            "impact": "Poisson/Gauss mass cannot be derived until the same observed source and charge frame is owned",
            "claim_effect": "Newton source normalization blocked",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "SCI1780_2_PPN_clock_orbit",
            "open_quantity": "PPN, clock, WEP, orbital consistency",
            "impact": "tau/frame/source leakage directly maps to beta/gamma/preferred-frame/clock/source-charge residuals",
            "claim_effect": "PPN/R10/WEP/clock/orbit pass refused until component rows close",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1780_0_common_frame_derivative",
            "countermodel": "all matter sees one frame, but that frame depends on residual X",
            "survives_current_constraints": True,
            "why_survives": "same-coframe clauses do not prove b_g,X=0",
            "what_kills_it": "Obs_e(q) parent factorisation plus zero/finite common-frame derivative rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1780_1_tau_role_split",
            "countermodel": "charge tau, clock tau, source tau, boundary tau, and orbit tau are not the same generator",
            "survives_current_constraints": True,
            "why_survives": "tau projectability and role lock are not parent-signed",
            "what_kills_it": "projectable tau theorem plus stationarity/admissibility and role-lock certificate",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1780_2_source_readout_map",
            "countermodel": "source or detector readout applies an X-dependent map after Hilbert variation",
            "survives_current_constraints": True,
            "why_survives": "readout functor and no post-readout frame clauses remain unsigned",
            "what_kills_it": "single Q_vis readout functor or finite Dsource_readout row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1780_3_constant_marker_leak",
            "countermodel": "masses, charge units, material labels, or clock constants vary along residual directions",
            "survives_current_constraints": True,
            "why_survives": "constant superselection and marker ownership are not signed",
            "what_kills_it": "Lie_v theta_A=0 theorem or finite Dtheta_marker residual",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1780_4_worldtube_boundary_reopens",
            "countermodel": "worldtube support or boundary endpoint changes with q/tau frame choices",
            "survives_current_constraints": True,
            "why_survives": "worldtube Hilbert support and boundary silence are only conditional",
            "what_kills_it": "parent-owned Hilbert support plus boundary/exact/proper theorem or finite support row",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1780_0_signature",
            "claim": "q/Dq/tau/source-functor signature is parent-signed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "QTS1780_7 remains SIGNATURE_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1780_1_Delta_frame_tau",
            "claim": "Delta_frame_tau=0 or source-bounded",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "DFT1780 component rows are missing values/source paths/common norm",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1780_2_Delta_Hsrc",
            "claim": "Delta_Hsrc source-measure mismatch is closed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "Delta_frame_tau remains a required component of Delta_Hsrc",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1780_3_Newton_GR",
            "claim": "Newton/GR/local/PPN/R10/WEP/clock/orbit pass follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "frame/tau/source signature and source-measure proof remain upstream",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1780_0_exact_theorem",
            "decision": "Q_DQ_TAU_SOURCE_FUNCTOR_ZERO_THEOREM_IS_EXACT_CONDITIONAL",
            "reason": "chain rule plus matter pullback kill frame/tau/source leakage if all parent antecedents are signed",
            "next_action": "keep theorem as a contract, not a claim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1780_1_current_status",
            "decision": "FAIL_CURRENT_PARENT_PROOF",
            "reason": "q, Dq, Obs_e, tau role lock, matter functor, constants/no-shadow, worldtube and boundary clauses are not jointly signed",
            "next_action": "retain Delta_frame_tau components",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1780_2_first_row",
            "decision": "DELTA_FRAME_TAU_FIRST_ROW_SCHEMA_STAGED_NONCLAIM",
            "reason": "the first row now has explicit DObs_e, Dreadout, tau, constants, shadow, worldtube, and boundary components",
            "next_action": "fill no component without source path, units, and no-cancellation normalization",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1780_3_best_next",
            "decision": "PARENT_Q_AND_DQ_MATRIX_FIRST_ROW_OR_OBS_E_FACTORISATION_IS_NEXT",
            "reason": "the signature cannot improve until q and Dq are computable or Obs_e(q) is parent-factorized",
            "next_action": "build 1781 parent q/Dq matrix first row or Obs_e factorisation proof gate",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1780_0_primary",
            "next_target": "1781-Y5-R2FR-parent-q-Dq-matrix-first-row-or-Obs-e-factorisation-proof.md",
            "script": "scripts/Y5_R2FR_parent_q_Dq_matrix_first_row_or_Obs_e_factorisation_proof.py",
            "objective": "try to construct the parent q/Dq matrix and Obs_e(q) factorisation for retained directions; if not, stage the first DObs_e/Dq component row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1780_1_parallel",
            "next_target": "1781b-Y5-R2FR-tau-role-lock-first-row-pack.md",
            "script": "scripts/Y5_R2FR_tau_role_lock_first_row_pack.py",
            "objective": "prepare tau_source/tau_charge/tau_clock/tau_orbit/tau_boundary component rows with units and source paths",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1780_2_later",
            "next_target": "1782-Y5-R2FR-no-shadow-source-functor-and-worldtube-support-zero-or-Delta-shadow-row.md",
            "script": "scripts/Y5_R2FR_no_shadow_source_functor_and_worldtube_support_zero_or_Delta_shadow_row.py",
            "objective": "attack source-shadow/worldtube support after q/Dq/frame machinery is sharper",
            "selection_status": "later",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "signature_gate": signature_gate_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "delta_frame_tau_rows": delta_frame_tau_rows(),
        "source_current_impact": source_current_impact_rows(),
        "countermodel": countermodel_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1780_{key.upper()}.csv")


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return all(boolish(row["exists"]) for row in rows), all(boolish(row["needles_present"]) for row in rows)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                if any(boolish(row.get(flag, False)) for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring")):
                    return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1780_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add("1780-Y5-R2FR-q-Dq-tau-source-functor-signature-or-Delta-frame-tau-first-row.md")
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1780_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1780_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1780_2_signature_gate_complete",
            any(row["gate_id"] == "QTS1780_7_verdict" for row in rows_map["signature_gate"]) and all(not boolish(row["valid_for_claim"]) for row in rows_map["signature_gate"]),
            "q/Dq/tau/source-functor signature gate is complete and nonclaim",
        ),
        (
            "VAL1780_3_conditional_theorem_written",
            any(row["theorem_id"] == "FTZ1780_0_chain_rule_core" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["theorem_attempt"]),
            "exact conditional chain-rule theorem is written",
        ),
        (
            "VAL1780_4_current_proof_not_promoted",
            any(row["theorem_id"] == "FTZ1780_4_current_verdict" and row["proof_status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["theorem_attempt"]),
            "current Delta_frame_tau proof remains unpromoted",
        ),
        (
            "VAL1780_5_delta_rows_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["delta_frame_tau_rows"]),
            "Delta_frame_tau rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1780_6_impact_nonclaim",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["source_current_impact"]),
            "source-current impact rows remain nonclaim",
        ),
        (
            "VAL1780_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "countermodels remain live until theorem or bound rows close them",
        ),
        (
            "VAL1780_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1780_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1780_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1780_11_decision_next",
            any(row["decision_id"] == "DEC1780_3_best_next" and "PARENT_Q_AND_DQ_MATRIX" in row["decision"] for row in rows_map["decision"]),
            "decision selects parent q/Dq matrix or Obs_e factorisation next",
        ),
        (
            "VAL1780_12_next_selected",
            any(row["route_id"] == "NEXT1780_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1780_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1780 CSVs parse"),
        ("VAL1780_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1780_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1780_16_formalization_untouched", formalization_untouched(), "no 1780 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1780_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1780 q/Dq/tau/source-functor signature or Delta_frame_tau checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1780 - Y5/R2FR q-Dq-Tau Source-Functor Signature or Delta-Frame-Tau First Row",
            "",
            "## Verdict",
            "",
            "1780 proves the shape of the clean route but does not sign it for current MTS. If the parent quotient `q`, its kernel `Dq`, the observed coframe functor `Obs_e(q)`, one projectable `tau`, and the ordinary matter/source functor are all parent-owned, then the frame/tau/source leakage term `Delta_frame_tau` vanishes by a straight chain-rule and pullback argument.",
            "",
            "The live problem is that every word in that sentence still has to be owned in one parent branch. Current MTS has the right conditional theorem, but the actual `q/Dq/tau/source` signature is not signed. Therefore `Delta_frame_tau` is now staged as explicit nonclaim component rows rather than hidden in a local-GR assumption.",
            "",
            "**Claim ceiling:** no q/Dq/tau/source-functor proof, no `Delta_frame_tau=0`, no `Delta_Hsrc=0`, no measured-GM/Newton/Gauss/orbit reduction, no PPN/R10/R11/WEP/clock/local-GR pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1780.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Signature Gate",
            markdown_table(rows_map["signature_gate"], ["gate_id", "signature_clause", "mathematical_form", "current_status", "source_basis", "blocks", "exit_condition", "valid_for_claim"]),
            "",
            "## Frame-Tau Zero Theorem Attempt",
            markdown_table(rows_map["theorem_attempt"], ["theorem_id", "claim", "mathematical_form", "proof_status", "missing_for_current_claim", "valid_for_claim"]),
            "",
            "## Delta-Frame-Tau First Row Schema",
            markdown_table(rows_map["delta_frame_tau_rows"], ["row_id", "quantity", "definition", "formula", "required_columns", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Source-Current Impact",
            markdown_table(rows_map["source_current_impact"], ["impact_id", "open_quantity", "impact", "claim_effect", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a good narrowing. The route is not 'trust the motion field'; it is `q`, `Dq`, `Obs_e(q)`, and one `tau` doing exact work. If those are parent-signed, the same mechanism helps the current and the source. If not, the first honest empirical/theorem fallback is a `Delta_frame_tau` row with declared components and units.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1780-Y5-R2FR-q-Dq-tau-source-functor-signature-or-Delta-frame-tau-first-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1780 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
