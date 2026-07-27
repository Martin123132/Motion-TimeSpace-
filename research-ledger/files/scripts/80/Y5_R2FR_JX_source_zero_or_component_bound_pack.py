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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1801"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1801_0_1800_doc",
        "source_key": "1800_handoff",
        "source_path": ROOT / "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md",
        "needles": ["DEC1800_3_next", "NEXT1800_0_primary"],
        "role": "selects J_X source zero or component bound pack as 1801 target",
    },
    {
        "source_id": "SRC1801_1_1800_validation",
        "source_key": "1800_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1800_VALIDATION.csv",
        "needles": ["VAL1800_OVERALL", "PASS"],
        "role": "confirms 1800 passed before 1801 starts",
    },
    {
        "source_id": "SRC1801_2_1800_activation",
        "source_key": "1800_activation_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_POSITIVE_OPERATOR_ACTIVATION_AUDIT.csv",
        "needles": ["XPA1800_2_JX_zero", "XPA1800_5_verdict"],
        "role": "marks J_X=0 as missing activation input for positive-operator route",
    },
    {
        "source_id": "SRC1801_3_973_jx_decomposition",
        "source_key": "973_jx_decomposition",
        "source_path": RESIDUALS / "P8_Y5_R10_973_JX_DECOMPOSITION_GATE.csv",
        "needles": ["JXD973_0_kinetic_affine", "JXD973_6_verdict"],
        "role": "older component split for J_X source-zero gate",
    },
    {
        "source_id": "SRC1801_4_970_action",
        "source_key": "970_quadratic_action",
        "source_path": RESIDUALS / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "needles": ["QMA970_3_source_silence", "QMA970_7_verdict"],
        "role": "quadratic X action candidate and J_X source decomposition",
    },
    {
        "source_id": "SRC1801_5_1043_jx_audit",
        "source_key": "1043_jx_channel_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1043_JX_ZERO_CHANNEL_AUDIT.csv",
        "needles": ["JX1043_0_matter_pullback", "JX1043_6_verdict"],
        "role": "channel audit for total J_X zero premise",
    },
    {
        "source_id": "SRC1801_6_1044_matter_doc",
        "source_key": "1044_matter_pullback_doc",
        "source_path": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
        "needles": ["MPD1044_7_exact_theorem_if_signed", "CG1044_4_local_GR_reduction"],
        "role": "exact conditional matter-pullback theorem and qbarXT fallback",
    },
    {
        "source_id": "SRC1801_7_1044_qbar_envelope",
        "source_key": "1044_qbar_envelope",
        "source_path": RESIDUALS / "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
        "needles": ["QBC1044_0_qbar_geom", "QBC1044_5_total_abs_guard"],
        "role": "ordinary matter/test charge component envelope",
    },
    {
        "source_id": "SRC1801_8_1027_source_zero",
        "source_key": "1027_source_zero_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv",
        "needles": ["QZ1027_0_chain_rule", "QZ1027_6_verdict"],
        "role": "source-zero proof audit and hidden-source blockers",
    },
    {
        "source_id": "SRC1801_9_1042_source_zero",
        "source_key": "1042_source_zero_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv",
        "needles": ["SZ1042_0_matter_pullback", "SZ1042_5_verdict"],
        "role": "pre-1043 J_X source-zero clause audit",
    },
    {
        "source_id": "SRC1801_10_1720_matter_functor",
        "source_key": "1720_matter_functor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"],
        "role": "latest branch matter-functor signature audit",
    },
    {
        "source_id": "SRC1801_11_1761_no_direct_vertex",
        "source_key": "1761_no_direct_vertex",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
        "needles": ["NDV1761_0_target", "NDV1761_4_current_verdict"],
        "role": "no direct ordinary matter X vertex grammar attempt",
    },
    {
        "source_id": "SRC1801_12_1786_boundary_matter",
        "source_key": "1786_boundary_matter_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
        "needles": ["BMC1786_1_matter_interface", "BMC1786_5_verdict"],
        "role": "current branch boundary/matter closure gate",
    },
    {
        "source_id": "SRC1801_13_557_force_map",
        "source_key": "557_force_map",
        "source_path": RESIDUALS / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
        "needles": ["BMRF557_0_static_bulk_operator", "BMRF557_3_Hamiltonian_projection"],
        "role": "finite-range force law and projection map if J_X is nonzero",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_SOURCE_REGISTER.csv",
    "jx_source_silence_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_JX_SOURCE_SILENCE_GATE.csv",
    "jx_component_bound_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_JX_COMPONENT_BOUND_PACK.csv",
    "observable_interface": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_OBSERVABLE_INTERFACE.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_ACCEPTANCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1801_VALIDATION.csv",
}

DOC_PATH = ROOT / "1801-Y5-R2FR-JX-source-zero-or-component-bound-pack.md"


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
                "role": source["role"],
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(str(by_key[key]) for key in keys)


def jx_source_silence_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_0_definition",
            "component": "J_X total",
            "required_statement": "J_X = J_kin_affine + J_matter + J_chiD_wall + J_boundary + J_readout + J_history plus source-normalization/projection tails",
            "derivation_attempt": "use 970/973/1043 split and require channelwise zero or channelwise absolute bounds; no cancellation between components",
            "current_status": "DECOMPOSITION_IMPORTED_NOT_ZERO",
            "missing_input": "MISSING_CHANNEL_ZERO_OR_COMPONENT_BOUNDS",
            "source_paths": src("970_quadratic_action", "973_jx_decomposition", "1043_jx_channel_audit"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_1_kin_affine",
            "component": "J_kin_affine",
            "required_statement": "X action is centered homogeneous quadratic around the physical local branch with no X0(q) linear marker",
            "derivation_attempt": "positive quadratic identity can kill X only after action origin, sign/gap, source and boundary clauses are signed",
            "current_status": "SOURCE_FREE_KINETIC_ORIGIN_NOT_PARENT_SIGNED",
            "missing_input": "MISSING_CENTERED_X_ORIGIN;MISSING_NO_LINEAR_MARKER",
            "source_paths": src("973_jx_decomposition", "970_quadratic_action"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_2_matter_pullback",
            "component": "J_matter",
            "required_statement": "ordinary matter sees only e_obs(q(Phi)) and fixed representation constants, with v_X in ker(Dq)",
            "derivation_attempt": "chain rule gives delta_v S_matter=0 if observed geometry, constants, matter lift and boundary support all descend",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "missing_input": "MISSING_PARENT_MATTER_FUNCTOR;MISSING_CONSTANT_SUPERSELECTION;MISSING_NO_MARKER_THEOREM",
            "source_paths": src("1044_matter_pullback_doc", "1044_qbar_envelope", "1720_matter_functor", "1761_no_direct_vertex"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_3_chiD_wall",
            "component": "J_chiD_wall",
            "required_statement": "f(0)=f'(0)=0 and no local chi_D wall/source tail contributes inside the exterior domain",
            "derivation_attempt": "double-zero route suppresses local stress only if wall support, branch origin and active X operator remain parent-owned",
            "current_status": "DOUBLE_ZERO_CONDITIONAL_WALL_TAIL_OPEN",
            "missing_input": "MISSING_F_ORIGIN;MISSING_WALL_SUPPORT_ZERO;MISSING_OPERATOR_ACTIVE_WHEN_DOUBLE_ZERO_USED",
            "source_paths": src("970_quadratic_action", "973_jx_decomposition"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_4_boundary",
            "component": "J_boundary",
            "required_statement": "boundary variation is Dirichlet/zero-flux/exact primitive with no improper edge charge and no measured-source projection",
            "derivation_attempt": "proper compact representative subbranch is useful but does not remove physical source worldtube, reference or edge charges",
            "current_status": "BOUNDARY_WORLDLINE_SOURCE_OPEN",
            "missing_input": "MISSING_BOUNDARY_FLUX_ZERO;MISSING_EDGE_CHARGE_ZERO;MISSING_REFERENCE_SUBTRACTION_OWNER",
            "source_paths": src("1043_jx_channel_audit", "1786_boundary_matter_gate"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_5_readout",
            "component": "J_readout",
            "required_statement": "readout/calibration occurs after variation and cannot re-enter as an X source or hidden frame/source mask",
            "derivation_attempt": "variation-before-readout policy is structurally right, but current branch still retains source/readout frame and calibration tails",
            "current_status": "READOUT_NO_REENTRY_PARENT_UNSIGNED",
            "missing_input": "MISSING_READOUT_ORDER_THEOREM;MISSING_NO_SHADOW_FRAME;MISSING_CALIBRATION_TAIL_BOUND",
            "source_paths": src("1027_source_zero_audit", "1720_matter_functor", "1786_boundary_matter_gate"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_6_history",
            "component": "J_history",
            "required_statement": "memory/history kernel is compact-local, causal, stable, source-free, and relaxes to a universal constant or zero exterior profile",
            "derivation_attempt": "positive/stable kernel templates exist, but nonlocal history injection and source-memory couplings are not excluded by parent variation",
            "current_status": "HISTORY_KERNEL_SOURCE_OPEN",
            "missing_input": "MISSING_LOCAL_KERNEL_THEOREM;MISSING_HISTORY_TAIL_BOUND;MISSING_SOURCE_MEMORY_COUPLING_ZERO",
            "source_paths": src("1042_source_zero_clause", "1043_jx_channel_audit", "557_force_map"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_7_source_normalization",
            "component": "Pi_M projection/source normalization",
            "required_statement": "measured GM/source mass uses the same parent Hilbert charge that sources the local metric, or X charge is orthogonal to Pi_M^H",
            "derivation_attempt": "projection map is known as the right place to test the leak, but coefficient/orthogonality theorem is not signed",
            "current_status": "SOURCE_NORMALIZATION_PROJECTION_OPEN",
            "missing_input": "MISSING_PIM_H_ORTHOGONALITY;MISSING_SOURCE_MEASURE_COEFFICIENT;MISSING_MH_REF_NORMALIZATION",
            "source_paths": src("557_force_map", "1786_boundary_matter_gate", "1720_matter_functor"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "JZS1801_8_verdict",
            "component": "J_X source silence",
            "required_statement": "all JZS1801_1 through JZS1801_7 vanish by one parent branch, or every live component has a source-backed absolute bound",
            "derivation_attempt": "current corpus has exact conditional sublemmas, but not one signed parent action proving source silence",
            "current_status": "JX_SOURCE_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED",
            "missing_input": "MISSING_PARENT_MATTER_BOUNDARY_READOUT_HISTORY_SOURCE_PACK",
            "source_paths": src("1800_activation_audit", "1043_jx_channel_audit", "1044_matter_pullback_doc"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def jx_component_bound_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "JCB1801_0_matter",
            "j_component": "J_matter",
            "source_charge_symbol": "qbar_XT",
            "absolute_bound_formula": "|J_matter| <= M_T |qbar_XT| with qbar_XT bounded by |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|",
            "required_inputs": "parent matter functor theorem or qbar component values; M_T; source paths; units",
            "current_value": "MISSING_QBAR_XT_COMPONENT_VALUES",
            "units": "action_variation_per_X_or_declared_source_charge",
            "status": "NONCLAIM_COMPONENT_SCHEMA_READY_VALUES_MISSING",
            "source_paths": src("1044_qbar_envelope", "1720_matter_functor", "1761_no_direct_vertex"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "JCB1801_1_chiD_wall",
            "j_component": "J_chiD_wall",
            "source_charge_symbol": "A_chiD_wall",
            "absolute_bound_formula": "|J_chiD_wall| <= |f_prime(chi_D)L_X|_wall + |wall_boundary_tail|, zero only if f(0)=f_prime(0)=0 and wall support is absent",
            "required_inputs": "f origin; f_prime(0); wall support measure; L_X wall norm; source paths",
            "current_value": "MISSING_CHID_WALL_AMPLITUDE",
            "units": "source_density_or_declared_wall_amplitude",
            "status": "NONCLAIM_COMPONENT_SCHEMA_READY_VALUES_MISSING",
            "source_paths": src("970_quadratic_action", "973_jx_decomposition"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "JCB1801_2_boundary",
            "j_component": "J_boundary",
            "source_charge_symbol": "Q_edge_X;Phi_boundary_local",
            "absolute_bound_formula": "|J_boundary| <= |B_X| + |Q_edge_X| + |Phi_boundary_local| + |reference_tail| after common projection convention",
            "required_inputs": "boundary primitive or finite edge charge; reference subtraction rule; source worldtube flux; units",
            "current_value": "MISSING_BOUNDARY_EDGE_FLUX",
            "units": "boundary_flux_or_projected_source_charge",
            "status": "NONCLAIM_COMPONENT_SCHEMA_READY_VALUES_MISSING",
            "source_paths": src("1043_jx_channel_audit", "1786_boundary_matter_gate"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "JCB1801_3_readout",
            "j_component": "J_readout",
            "source_charge_symbol": "C_readout_X",
            "absolute_bound_formula": "|J_readout| <= ||delta R_readout/delta X|| + |shadow_frame_tail| + |calibration_source_mask|",
            "required_inputs": "variation-before-readout theorem or finite readout coefficients; no shadow frame; calibration tail units",
            "current_value": "MISSING_READOUT_REENTRY_COEFFICIENTS",
            "units": "readout_response_per_X",
            "status": "NONCLAIM_COMPONENT_SCHEMA_READY_VALUES_MISSING",
            "source_paths": src("1027_source_zero_audit", "1720_matter_functor", "1786_boundary_matter_gate"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "JCB1801_4_history",
            "j_component": "J_history",
            "source_charge_symbol": "A_history_X",
            "absolute_bound_formula": "|J_history(t)| <= int |K_mem(t,t',r,r')| |J_past(t',r')| dmu' plus boundary/history injection tails",
            "required_inputs": "kernel norm; support; decay time; source-memory coupling; stationary-domain theorem or finite tail value",
            "current_value": "MISSING_HISTORY_KERNEL_NORM",
            "units": "source_density_or_memory_tail_amplitude",
            "status": "NONCLAIM_COMPONENT_SCHEMA_READY_VALUES_MISSING",
            "source_paths": src("1042_source_zero_clause", "1043_jx_channel_audit", "557_force_map"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "JCB1801_5_total_abs_guard",
            "j_component": "J_X total",
            "source_charge_symbol": "JX_abs_envelope",
            "absolute_bound_formula": "|J_X| <= |J_matter| + |J_chiD_wall| + |J_boundary| + |J_readout| + |J_history| + |Pi_M_projection_tail|",
            "required_inputs": "all component theorem-zero certificates or all numeric absolute component bounds in a shared convention",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "shared_projected_source_charge",
            "status": "NO_CANCELLATION_ENVELOPE_READY_VALUES_MISSING",
            "source_paths": src("1800_activation_audit", "557_force_map", "1044_qbar_envelope"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def observable_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1801_0_R10",
            "observable_arena": "R10 short-range fifth force",
            "source_quantity": "alpha_X(lambda_X)",
            "projection_formula": "alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT plus boundary/readout/history tails in an absolute envelope",
            "required_inputs": "Z_X;M_X^2;K_X;Qbar_XH;qbar_XT;tail coefficients;real alpha_bound(lambda)",
            "current_status": "NOT_SCOREABLE_MTS_AND_BOUND_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1801_1_WEP",
            "observable_arena": "WEP/source-charge composition",
            "source_quantity": "qbar_XT material pair differences",
            "projection_formula": "eta_AB source proxy requires source-backed qbar_XA and qbar_XB in the same frame",
            "required_inputs": "material sensitivities;constant/no-marker coefficients;source normalization;MICROSCOPE or equivalent source",
            "current_status": "NOT_SCOREABLE_QBAR_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1801_2_PPN_Newton",
            "observable_arena": "PPN and measured GM/Newton limit",
            "source_quantity": "Pi_M^H J_X and non-Hilbert source tail",
            "projection_formula": "mu_EH=mu_obs only if X charge is orthogonal to measured source mass or bounded below PPN residuals",
            "required_inputs": "Pi_M projection coefficient;M_H_ref;gamma/beta/preferred-frame residual vector",
            "current_status": "NOT_SCOREABLE_SOURCE_NORMALIZATION_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1801_3_clocks_constants",
            "observable_arena": "clocks/fine-structure/material constants",
            "source_quantity": "qbar_constants and readout calibration tail",
            "projection_formula": "clock residual is coefficient-vector dot Lie_v(theta_A) plus readout/order tails",
            "required_inputs": "dtheta_A/dX;clock sensitivities;readout order theorem or finite calibration coefficients",
            "current_status": "NOT_SCOREABLE_CONSTANTS_READOUT_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1801_4_orbital_history",
            "observable_arena": "orbital systems/history drift",
            "source_quantity": "history kernel and boundary/source support tail",
            "projection_formula": "orbital residual requires memory kernel norm and support relative to measured source mass/current",
            "required_inputs": "kernel norm;decay/support;source worldtube projection;orbital denominator",
            "current_status": "NOT_SCOREABLE_HISTORY_KERNEL_OPEN",
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1801_0_source_zero",
            "gate": "J_X source silence theorem",
            "current_status": "FAIL_PARENT_UNSIGNED_CHANNELS",
            "reason": "matter, chiD wall, boundary, readout, history and projection channels are not all theorem-zero",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1801_1_component_bounds",
            "gate": "finite component bound envelope",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "reason": "absolute formulas are written, but all live component values/source paths are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1801_2_no_cancellation",
            "gate": "no hidden cancellation credit",
            "current_status": "POLICY_ACTIVE_NOT_SCORE",
            "reason": "component signs cannot be used to cancel; only theorem-zero or absolute bounds count",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1801_3_verdict",
            "gate": "J_X nohair or bounded fallback readiness",
            "current_status": "JX_NOT_ZERO_AND_NOT_BOUNDED",
            "reason": "the branch has the right decomposition but no claim-ready zero theorem or numeric component pack",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1801_0_direct_matter_marker",
            "countermodel": "ordinary matter action contains an X-sensitive hidden frame, marker, constant, or source-only prefactor",
            "survives_current_constraints": True,
            "why_survives": "matter functor, no-marker theorem and no direct vertex grammar are conditional, not parent-signed",
            "what_kills_it": "signed parent matter functor plus constant/superselection/no-marker clause",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1801_1_wall_tail",
            "countermodel": "chi_D transition wall leaves a finite X source even when the local plateau value is zero",
            "survives_current_constraints": True,
            "why_survives": "double-zero origin and wall support/no-tail conditions are not parent-owned",
            "what_kills_it": "derive f(0)=f_prime(0)=0 from parent action and prove no local wall support/source tail",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1801_2_boundary_edge_charge",
            "countermodel": "boundary/reference/source-worldtube edge charge contributes to J_X or Phi_boundary_local",
            "survives_current_constraints": True,
            "why_survives": "proper compact representative sublemma does not cover physical source edges and reference subtraction",
            "what_kills_it": "parent boundary class/no-flux theorem or source-backed edge charge bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1801_3_readout_reentry",
            "countermodel": "readout/calibration map re-enters as an effective X source or shadow frame",
            "survives_current_constraints": True,
            "why_survives": "variation-before-readout policy is not yet a parent no-reentry theorem",
            "what_kills_it": "readout order theorem plus finite calibration/source-mask residual bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1801_4_history_memory_tail",
            "countermodel": "nonlocal history kernel sources local X hair or measured-GM drift",
            "survives_current_constraints": True,
            "why_survives": "kernel locality, decay and source-memory coupling are not derived",
            "what_kills_it": "compact-local stable kernel theorem or finite history-tail bound",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1801_0_JX_zero",
            "claim": "J_X=0 in the local exterior",
            "status": "BLOCKED",
            "reason": "JZS1801_8 verdict is source-zero not proved",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1801_1_X_nohair",
            "claim": "positive X nohair theorem proves X=0 or I_X=0",
            "status": "BLOCKED",
            "reason": "J_X, boundary/zero-mode, sign/gap and projection clauses remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1801_2_finite_alpha",
            "claim": "finite alpha_X(lambda) fallback is scoreable",
            "status": "BLOCKED",
            "reason": "component values, K_X, source/test charges and real R10 bound curve are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1801_3_local_GR_Newton",
            "claim": "local GR/Newton source normalization is derived",
            "status": "BLOCKED",
            "reason": "source normalization, matter functor, boundary and history tails remain active residual channels",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1801_0_theorem_attempt",
            "decision": "JX_ZERO_NOT_PROVED",
            "reason": "the exact source-silence contract is now assembled, but no single parent action signs all channels",
            "next_action": "do not activate X nohair; keep component bounds live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1801_1_component_pack",
            "decision": "COMPONENT_BOUND_PACK_STAGED_NONCLAIM",
            "reason": "component formulas are ready, but every live component needs a theorem-zero certificate or source-backed value",
            "next_action": "fill one component at a time, starting with the upstream matter/readout functor signature",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1801_2_best_first_component",
            "decision": "MATTER_FUNCTOR_AND_READOUT_NO_REENTRY_NEXT",
            "reason": "J_matter is the cleanest chain-rule theorem, and readout/no-marker re-entry is the largest loophole that can undo it",
            "next_action": "build 1802 to try signing parent ordinary-matter functor plus readout no-reentry, or emit qbar/readout component rows",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1801_0_primary",
            "next_target": "1802-Y5-R2FR-parent-matter-functor-readout-no-reentry-or-qbar-readout-row.md",
            "script": "scripts/Y5_R2FR_parent_matter_functor_readout_no_reentry_or_qbar_readout_row.py",
            "objective": "try to sign ordinary matter functor, no-marker constants and readout no-reentry so J_matter=0; if not, emit qbar_XT and C_readout component rows",
            "selection_status": "selected",
            "success_condition": "parent-signed J_matter=0 route or finite source-backed qbar/readout component envelope",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1801_1_parallel_boundary",
            "next_target": "1802b-Y5-R2FR-boundary-edge-flux-source-pack.md",
            "script": "scripts/Y5_R2FR_boundary_edge_flux_source_pack.py",
            "objective": "derive boundary no-flux/no-edge-charge or emit Phi_boundary/Q_edge rows",
            "selection_status": "held_parallel",
            "success_condition": "boundary theorem-zero or finite source-backed edge projection rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1801_2_parallel_history",
            "next_target": "1802c-Y5-R2FR-history-kernel-tail-bound-pack.md",
            "script": "scripts/Y5_R2FR_history_kernel_tail_bound_pack.py",
            "objective": "derive compact-local history silence or emit finite kernel tail bounds",
            "selection_status": "held_parallel",
            "success_condition": "history theorem-zero or source-backed kernel norm row",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "jx_source_silence_gate": jx_source_silence_gate_rows(),
        "jx_component_bound_pack": jx_component_bound_pack_rows(),
        "observable_interface": observable_interface_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1801_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "valid_prediction_row",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            for flag in claim_flags:
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ready_flags = (
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "valid_prediction_row",
        "theorem_zero",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in ready_flags:
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1801_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1801_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1801_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1801_2_jx_zero_not_proved",
            any(
                row["gate_id"] == "JZS1801_8_verdict"
                and row["current_status"] == "JX_SOURCE_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED"
                and not boolish(row["theorem_zero"])
                for row in rows_map["jx_source_silence_gate"]
            ),
            "J_X source-zero theorem is not promoted",
        ),
        (
            "VAL1801_3_component_pack_nonclaim",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["claim_allowed"])
                and "MISSING" in row["current_value"]
                for row in rows_map["jx_component_bound_pack"]
            ),
            "all component bound rows are nonclaim and value-missing",
        ),
        (
            "VAL1801_4_observable_interfaces_blocked",
            all(not boolish(row["valid_for_claim"]) and row["current_status"].startswith("NOT_SCOREABLE") for row in rows_map["observable_interface"]),
            "observable projection rows remain blocked",
        ),
        (
            "VAL1801_5_acceptance_blocks",
            any(
                row["gate_id"] == "AC1801_3_verdict"
                and row["current_status"] == "JX_NOT_ZERO_AND_NOT_BOUNDED"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks both nohair and finite-bound claims",
        ),
        (
            "VAL1801_6_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "all countermodels remain live",
        ),
        (
            "VAL1801_7_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1801_8_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1801_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1801_10_decision_next",
            any(
                row["decision_id"] == "DEC1801_2_best_first_component"
                and row["decision"] == "MATTER_FUNCTOR_AND_READOUT_NO_REENTRY_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects matter functor/readout no-reentry next",
        ),
        (
            "VAL1801_11_next_selected",
            any(row["route_id"] == "NEXT1801_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1801_12_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1801 CSVs parse"),
        ("VAL1801_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1801_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1801_15_formalization_untouched", formalization_untouched(), "no 1801 outputs found under formalization-workbench"),
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
            "check_id": "VAL1801_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1801 J_X source zero or component bound pack checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1801 - Y5/R2FR J_X Source Zero or Component Bound Pack",
            "",
            "## Verdict",
            "",
            "1801 tries the clean route first: prove `J_X=0` channel by channel so the positive-operator `X` nohair branch can activate.",
            "",
            "That proof does not close. The useful result is sharper: `J_X` now has a no-cancellation component contract with five live pieces:",
            "",
            "`J_matter`, `J_chiD_wall`, `J_boundary`, `J_readout`, and `J_history`, plus the measured-source projection tail.",
            "",
            "The matter channel is the strongest mathematical foothold because the chain-rule theorem is exact if the parent matter functor, no-marker constants, and readout no-reentry clauses are signed. They are not signed yet.",
            "",
            "**Claim ceiling:** no `J_X=0`, no `X=0`, no finite `alpha_X(lambda)` score, no local-GR/Newton source-normalization claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1801.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## J_X Source Silence Gate",
            markdown_table(rows_map["jx_source_silence_gate"], ["gate_id", "component", "required_statement", "current_status", "missing_input", "theorem_zero", "valid_for_claim"]),
            "",
            "## J_X Component Bound Pack",
            markdown_table(rows_map["jx_component_bound_pack"], ["component_id", "j_component", "source_charge_symbol", "absolute_bound_formula", "current_value", "status", "valid_for_claim"]),
            "",
            "## Observable Interface",
            markdown_table(rows_map["observable_interface"], ["interface_id", "observable_arena", "source_quantity", "projection_formula", "current_status", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "The coupling problem has narrowed again. We do not need to guess whether the whole local branch fails; we need to kill or bound the source that feeds the extra `X` channel. The best first punch is not boundary or history yet. It is the ordinary-matter/readout contract, because if that closes then the largest source/test charge path drops out by theorem rather than fit.",
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
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1801 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
