from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4008"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4008-Y5-R2FR-source-label-forgetting-parent-functor-or-JR-coefficient-pack.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

ETA_SOURCE_BOUND = 2.8e-15

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4008_SOURCE_REGISTER.csv",
    "constructor": SRC / "P8_Y5_R2FR_4008_SOURCE_LABEL_FORGETTING_CONSTRUCTOR_PACKET.csv",
    "proof": SRC / "P8_Y5_R2FR_4008_NO_HOM_WEIGHT_REJECTION_PROOF.csv",
    "rejections": SRC / "P8_Y5_R2FR_4008_ILLEGAL_CONSTRUCTOR_REJECTION_LEDGER.csv",
    "coefficients": SRC / "P8_Y5_R2FR_4008_JR_COEFFICIENT_PACK.csv",
    "cases": SRC / "P8_Y5_R2FR_4008_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4008_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4008_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4008_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4008_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4008_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4008_VALIDATION.csv",
}

NEXT_DOC = "4009-Y5-R2FR-q-kernel-observed-coframe-single-branch-certificate-or-geom-JR-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4009_q_kernel_observed_coframe_single_branch_certificate_or_geom_JR_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        ("SRC4008_00_handoff", SRC / "P8_Y5_R2FR_4007_NEXT_TARGET.csv", "NEXT4007_0", "4007 handoff"),
        ("SRC4008_01_no_prefactor", SRC / "P8_Y5_R2FR_4007_JR_CHAIN_RULE_THEOREM.csv", "JRT4007_4_no_source_prefactor", "4007 no-prefactor theorem"),
        ("SRC4008_02_countermodel", SRC / "P8_Y5_R2FR_4007_JR_CHAIN_RULE_THEOREM.csv", "JRT4007_5_countermodel", "4007 prevariation weight countermodel"),
        ("SRC4008_03_prefactor_audit", SRC / "P8_Y5_R2FR_4007_MATTER_READOUT_DESCENT_AUDIT.csv", "AUD4007_3_no_prefactor", "live prefactor leak"),
        ("SRC4008_04_constants_audit", SRC / "P8_Y5_R2FR_4007_MATTER_READOUT_DESCENT_AUDIT.csv", "AUD4007_4_constants_markers", "constant marker leak"),
        ("SRC4008_05_readout_audit", SRC / "P8_Y5_R2FR_4007_MATTER_READOUT_DESCENT_AUDIT.csv", "AUD4007_5_readout_order", "readout regeneration leak"),
        ("SRC4008_06_same_branch", SRC / "P8_Y5_R2FR_4007_MATTER_READOUT_DESCENT_AUDIT.csv", "AUD4007_7_same_branch", "same branch guard"),
        ("SRC4008_07_prefactor_bound", SRC / "P8_Y5_R2FR_4007_JR_BOUND_ROWS.csv", "JRB4007_1_prefactor", "prefactor coefficient row"),
        ("SRC4008_08_theta_bound", SRC / "P8_Y5_R2FR_4007_JR_BOUND_ROWS.csv", "JRB4007_3_constants_markers", "theta coefficient row"),
        ("SRC4008_09_readout_bound", SRC / "P8_Y5_R2FR_4007_JR_BOUND_ROWS.csv", "JRB4007_4_readout", "readout coefficient row"),
        ("SRC4008_10_np_criterion", SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_0_no_prefactor_criterion", "no-Hom criterion"),
        ("SRC4008_11_np_counter", SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_1_countermodel_retained", "prefactor countermodel"),
        ("SRC4008_12_np_bound", SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv", "NP3989_2_bound_split", "bound split"),
        ("SRC4008_13_ward_owner", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_0_z_g", "current owner gate"),
        ("SRC4008_14_alpha_source", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_2_beta_source_alpha", "alpha/source marker gate"),
        ("SRC4008_15_preweight", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_5_prevariation_weight", "prevariation weight gate"),
        ("SRC4008_16_nonhilbert", SRC / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_6_nonHilbert_bypass", "non-Hilbert bypass"),
        ("SRC4008_17_matter_factorization", SRC / "P8_no_species_source_charge_CONTRACT.csv", "S1_matter_factorization", "matter factorization"),
        ("SRC4008_18_constants", SRC / "P8_no_species_source_charge_CONTRACT.csv", "S2_constant_sector_universality", "constant sector"),
        ("SRC4008_19_no_marker", SRC / "P8_no_species_source_charge_CONTRACT.csv", "S3_no_material_marker_extension", "no material marker"),
        ("SRC4008_20_source_blind", SRC / "P8_no_species_source_charge_CONTRACT.csv", "S4_source_normalization_species_blind", "source normalization species blind"),
        ("SRC4008_21_const_superselection", SRC / "P8_constant_sector_universality_CONTRACT.csv", "C1_superselection_independence", "superselection constants"),
        ("SRC4008_22_no_direct_const", SRC / "P8_constant_sector_universality_CONTRACT.csv", "C2_no_direct_constant_vertices", "no direct constant vertices"),
        ("SRC4008_23_universal_source", SRC / "P8_constant_sector_universality_CONTRACT.csv", "C3_universal_source_variation", "universal source variation"),
        ("SRC4008_24_selector_blind", SRC / "P8_source_owner_parent_action_terms_CONTRACT.csv", "A6_selector_blind_source_action", "selector-blind source action"),
        ("SRC4008_25_matter_functor", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", "PRE2611_2_matter_functor", "matter functor premise"),
        ("SRC4008_26_no_shadow", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", "PRE2611_4_no_shadow_prefactor", "no shadow prefactor"),
        ("SRC4008_27_hilbert_source", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv", "PRE2611_7_hilbert_source_owner", "Hilbert source owner"),
        ("SRC4008_28_chain_rule", SRC / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv", "MD2570_0_chain_rule", "quotient chain rule"),
        ("SRC4008_29_qmap_matter", SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_2_matter_constants", "q-map matter constants"),
        ("SRC4008_30_theorem_3646", SRC / "P8_Y5_R2FR_3646_MATTER_DESCENT_THEOREM_ATTEMPT.csv", "MDT3646_0_statement", "matter descent theorem"),
        ("SRC4008_31_clause_3646", SRC / "P8_Y5_R2FR_3646_MATTER_DESCENT_CLAUSE_AUDIT.csv", "MDC3646_4_no_marker_constants", "marker constants clause"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def constructor_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "constructor_id": "SLF4008_0_signature",
            "object": "ordinary matter parent constructor",
            "typed_statement": "S_ord := sum_A int_M L_A(psi_A,D_obs psi_A,e_obs(q(Phi)),omega_obs(q(Phi)),theta_A) dmu_obs",
            "allowed_arguments": "psi_A;D_obs psi_A;e_obs(q(Phi));omega_obs(q(Phi));fixed representation constants theta_A",
            "forbidden_arguments": "R_AB;X_hidden;source label as field;material marker as coupling;worldtube mask;post-readout projector;species-dependent kappa_A",
            "effect": "ordinary matter is a quotient pullback plus fixed representation data",
            "adopted_in_parent_action": False,
            "status": "CONSTRUCTOR_PACKET_READY_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constructor_id": "SLF4008_1_source_labels",
            "object": "source/species/material labels",
            "typed_statement": "A labels a direct-sum summand or representation object only; A is not a varied scalar, field, spurion, projector or source-coordinate argument",
            "allowed_arguments": "Rep_A index;fixed superselection sector;bookkeeping sum label",
            "forbidden_arguments": "Hom(A,R_+);Hom((A,R_AB),R_+);A -> kappa_A;A -> w_A;material label -> source weight",
            "effect": "no source/species label can generate a scalar active-mass weight before variation",
            "adopted_in_parent_action": False,
            "status": "NO_HOM_PACKET_READY_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constructor_id": "SLF4008_2_constants",
            "object": "representation constants",
            "typed_statement": "theta_A are fixed representation/superselection data with delta_R theta_A=0 in the local branch",
            "allowed_arguments": "m_A;q_A;spin representation;clock standard as fixed theta_A",
            "forbidden_arguments": "theta_A(R_AB);theta_A(X_hidden);alpha_EM(R_AB);material-marker-dependent constants",
            "effect": "kills b_theta_R only if adopted in the same branch as q/coframe descent",
            "adopted_in_parent_action": False,
            "status": "CONSTANT_PACKET_READY_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constructor_id": "SLF4008_3_hilbert_source",
            "object": "active gravitational source",
            "typed_statement": "tau_a^mu := |e_obs|^-1 delta S_ord/delta e_mu^a and J_src is this Hilbert/coframe current plus exact/improvement-owned terms",
            "allowed_arguments": "one observed coframe;one universal coupling kappa;variation-before-readout",
            "forbidden_arguments": "sum_A kappa_A T_A;non-Hilbert source bypass;post-variation current rescaling;source-only active-mass slot",
            "effect": "source normalization cannot be species-weighted inside ordinary matter",
            "adopted_in_parent_action": False,
            "status": "HILBERT_SOURCE_PACKET_READY_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "constructor_id": "SLF4008_4_readout_order",
            "object": "readout and calibration",
            "typed_statement": "readout maps are applied after parent variation or are q-basic fixed functionals declared before variation",
            "allowed_arguments": "fixed calibration convention;fixed projector;post-variation observable map",
            "forbidden_arguments": "readout mask inside S_ord;P_active in matter arguments;post-readout source refit before Euler variation",
            "effect": "blocks readout_regen_R for the ordinary matter constructor; boundary/readout finite rows remain if not adopted",
            "adopted_in_parent_action": False,
            "status": "READOUT_PACKET_READY_NOT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def proof_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "NOHOM4008_0_type_rejection",
            "target": "w_A(R_AB)S_A",
            "derivation": "The term requires both R_AB in args(S_ord) and a morphism Hom((A,R_AB),R_+) producing w_A. SLF4008_0 excludes R_AB and SLF4008_1 sets that Hom set empty.",
            "result": "pre-variation source/species weight is ill-typed in the constructor packet",
            "status": "EXACT_IF_PACKET_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "NOHOM4008_1_variation",
            "target": "delta_R S_ord",
            "derivation": "delta_R S_ord = sum_A[(delta L_A/d e_obs)DObs(Dq[v_R]) + (partial L_A/partial theta_A)delta_R theta_A + E_psi delta_R psi_A] + boundary. Under q-kernel, fixed theta_A and on-shell/gauge matter lift, the bulk terms vanish.",
            "result": "J_R^matter_bulk=0 follows by chain rule and typed constants, not by assumption",
            "status": "EXACT_CONDITIONAL_BULK_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "NOHOM4008_2_hilbert_owner",
            "target": "species source weights kappa_A",
            "derivation": "If active source is defined as the Hilbert/coframe variation of the same S_ord with one universal kappa, a parallel sum_A kappa_A T_A is a second source constructor and is not in args(S_ord).",
            "result": "kappa_A and epsilon_species_A are illegal ordinary-matter slots unless a new explicit source sector is added and bounded",
            "status": "EXACT_IF_PACKET_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "NOHOM4008_3_readout",
            "target": "readout_regen_R",
            "derivation": "A fixed post-variation observable map cannot contribute to the Euler derivative delta_R S_ord; if the map is inside the action, it is a forbidden readout mask and moves to the finite coefficient pack.",
            "result": "readout_regen_R is zero for the typed constructor but retained outside it",
            "status": "EXACT_IF_READOUT_PACKET_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "NOHOM4008_4_not_full_local_GR",
            "target": "local GR/Newton claim",
            "derivation": "The constructor packet kills only source-label/prevariation ordinary-matter weights. It does not by itself prove v_R in ker(Dq), observed coframe descent, boundary nohair, or second-order PPN closure.",
            "result": "J_R source-weight leak is narrowed; local GR remains unclaimed",
            "status": "SCOPE_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def rejection_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "rejection_id": "REJ4008_0_weight",
            "candidate_term": "sum_A w_A(R_AB) S_A",
            "why_rejected": "requires forbidden R_AB argument and forbidden Hom((A,R_AB),R_+) source weight",
            "fallback_if_kept": "w_R_source_4008 finite row with units per_RAB and WEP/PPN/R10 projections",
            "status": "REJECTED_BY_TYPED_CONSTRUCTOR_IF_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rejection_id": "REJ4008_1_species_kappa",
            "candidate_term": "sum_A kappa_A T_A or kappa_A J_A",
            "why_rejected": "duplicates Hilbert source owner and violates one universal observed-coframe source coupling",
            "fallback_if_kept": "epsilon_species_A finite row tied to eta_source_AB bound scale",
            "status": "REJECTED_BY_HILBERT_OWNER_IF_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rejection_id": "REJ4008_2_marker_constant",
            "candidate_term": "theta_A(R_AB), alpha_EM(R_AB), material_marker -> theta_A",
            "why_rejected": "theta_A are fixed representation data, not local MTS fields or material-marker functions",
            "fallback_if_kept": "b_theta_R coefficient pack plus clock/alpha/WEP projections",
            "status": "REJECTED_BY_CONSTANT_PACKET_IF_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rejection_id": "REJ4008_3_readout_mask",
            "candidate_term": "P_active(R_AB,A) inside S_ord before variation",
            "why_rejected": "readout/calibration belongs after parent variation or as fixed q-basic functional",
            "fallback_if_kept": "readout_regen_R finite row",
            "status": "REJECTED_BY_READOUT_ORDER_IF_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "rejection_id": "REJ4008_4_nonhilbert_bypass",
            "candidate_term": "J_src = kappa T_H + sum_A zeta_A J_NH,A",
            "why_rejected": "ordinary matter source is Hilbert/coframe current; non-Hilbert current must be an owned improvement or explicit new source sector",
            "fallback_if_kept": "nonHilbert_source_bypass finite row",
            "status": "REJECTED_FOR_ORDINARY_MATTER_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "JRCP4008_0_w_R_source",
            "coefficient": "w_R_source_4008",
            "formula": "sup_A |partial_R ln w_A| for forbidden S_ord=sum_A w_A(R_AB)S_A",
            "value": "ZERO_IF_SLF4008_PACKET_ADOPTED_ELSE_MISSING_NUMERIC_WEIGHT",
            "units": "per_RAB",
            "observable_link": "WEP;PPN;R10;source_composition;Newton_G",
            "source_path": str(OUTPUTS["constructor"]),
            "source_status": "DERIVED_ZERO_CONDITIONAL_OR_FINITE_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRCP4008_1_b_theta_R",
            "coefficient": "b_theta_R",
            "formula": "sup_a |partial_R theta_a/theta_a| over masses, charges, alpha_EM, clocks and material standards",
            "value": "ZERO_IF_FIXED_REPRESENTATION_PACKET_ADOPTED_ELSE_MISSING_COMPONENTS",
            "units": "per_RAB",
            "observable_link": "clocks;alpha_EM;charge_readout;WEP",
            "source_path": str(OUTPUTS["constructor"]),
            "source_status": "DERIVED_ZERO_CONDITIONAL_OR_FINITE_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRCP4008_2_readout_regen_R",
            "coefficient": "readout_regen_R",
            "formula": "delta_R(B_readout+S_eff) after variation-before-readout split",
            "value": "ZERO_IF_READOUT_PACKET_ADOPTED_ELSE_MISSING_KERNEL",
            "units": "same_as_J_R",
            "observable_link": "Newton_G;PPN;R10;orbits;clocks",
            "source_path": str(OUTPUTS["constructor"]),
            "source_status": "DERIVED_ZERO_CONDITIONAL_OR_FINITE_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRCP4008_3_epsilon_species_A",
            "coefficient": "epsilon_species_A",
            "formula": "partial_A ln(mu_obs/M_inertial) after common-mode unit calibration",
            "value": ETA_SOURCE_BOUND,
            "units": "dimensionless_bound_scale",
            "observable_link": "MICROSCOPE_WEP;source_normalization",
            "source_path": str(SRC / "P8_species_source_charge_residual_or_zero.csv"),
            "source_status": "BOUND_SCALE_ONLY_NOT_THEORY_VALUE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRCP4008_4_J_R_ord",
            "coefficient": "J_R_ordinary_matter",
            "formula": "|J_R_ord| <= |J_R_geom| + |w_R_source_4008| + |b_theta_R| + |readout_regen_R| + |boundary_worldtube_R|",
            "value": "ZERO_IF_SLF_PACKET_PLUS_Q_KERNEL_PLUS_BOUNDARY_CLOSE_ELSE_COMPONENT_ENVELOPE",
            "units": "same_as_J_R",
            "observable_link": "local_GR;Newton_G;PPN;R10",
            "source_path": str(OUTPUTS["proof"]),
            "source_status": "COMPONENT_ENVELOPE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JRCP4008_5_projection_required",
            "coefficient": "arena_projection",
            "formula": "map surviving J_R component to WEP/PPN/R10/clock/orbital kernels before claim",
            "value": "MISSING_ARENA_PROJECTION_IF_ANY_COMPONENT_SURVIVES",
            "units": "arena_dependent",
            "observable_link": "all_local_tests",
            "source_path": str(OUTPUTS["coefficients"]),
            "source_status": "MISSING_IF_NOT_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"case_id": "CASE4008_0_packet_adopted_all_local_clauses", "packet_adopted": True, "q_kernel": True, "coframe_descends": True, "boundary_open": False, "illegal_weight_requested": False, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4008_1_packet_adopted_weight_requested", "packet_adopted": True, "q_kernel": True, "coframe_descends": True, "boundary_open": False, "illegal_weight_requested": True, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4008_2_packet_not_adopted", "packet_adopted": False, "q_kernel": True, "coframe_descends": True, "boundary_open": False, "illegal_weight_requested": False, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4008_3_q_kernel_open", "packet_adopted": True, "q_kernel": False, "coframe_descends": True, "boundary_open": False, "illegal_weight_requested": False, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4008_4_coframe_open", "packet_adopted": True, "q_kernel": True, "coframe_descends": False, "boundary_open": False, "illegal_weight_requested": False, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4008_5_boundary_open", "packet_adopted": True, "q_kernel": True, "coframe_descends": True, "boundary_open": True, "illegal_weight_requested": False, "numeric_pack": False, "timestamp_utc": timestamp},
        {"case_id": "CASE4008_6_numeric_pack", "packet_adopted": False, "q_kernel": False, "coframe_descends": False, "boundary_open": True, "illegal_weight_requested": True, "numeric_pack": True, "timestamp_utc": timestamp},
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        packet_adopted = bool(case["packet_adopted"])
        q_kernel = bool(case["q_kernel"])
        coframe_descends = bool(case["coframe_descends"])
        boundary_open = bool(case["boundary_open"])
        illegal_weight_requested = bool(case["illegal_weight_requested"])
        numeric_pack = bool(case["numeric_pack"])

        if numeric_pack:
            constructor_status = "FINITE_COEFFICIENT_PACK_NONCLAIM"
            weight_status = "WEIGHT_RETAINED_AS_NUMERIC_ROW"
            jr_status = "J_R_COMPONENT_ENVELOPE"
            next_action = "source numeric coefficients and arena projections"
        elif not packet_adopted:
            constructor_status = "PACKET_WRITTEN_NOT_ADOPTED"
            weight_status = "WEIGHT_NOT_BANNED_IN_PARENT_ACTION"
            jr_status = "J_R_NOT_ZEROED"
            next_action = "adopt source-label-forgetting packet in one parent branch or keep coefficient pack"
        elif illegal_weight_requested:
            constructor_status = "ILLEGAL_TERM_REJECTED"
            weight_status = "w_A(R_AB) ILL_TYPED"
            jr_status = "J_R_PREF_WEIGHT_ZERO_CONDITIONAL"
            next_action = "continue with q-kernel/coframe/boundary clauses"
        elif not q_kernel:
            constructor_status = "MATTER_PACKET_OK_Q_KERNEL_OPEN"
            weight_status = "w_A BANNED_CONDITIONAL"
            jr_status = "J_R_GEOMETRY_COMPONENT_OPEN"
            next_action = "prove v_R in ker(Dq) for actual R_AB"
        elif not coframe_descends:
            constructor_status = "MATTER_PACKET_OK_COFRAME_OPEN"
            weight_status = "w_A BANNED_CONDITIONAL"
            jr_status = "J_R_HILBERT_GEOMETRY_OPEN"
            next_action = "prove observed coframe descends through q"
        elif boundary_open:
            constructor_status = "BULK_MATTER_ZERO_BOUNDARY_OPEN"
            weight_status = "w_A BANNED_CONDITIONAL"
            jr_status = "J_R_BOUNDARY_WORLD_TUBE_OPEN"
            next_action = "separate boundary/worldtube nohair pass"
        else:
            constructor_status = "CONDITIONAL_BULK_SOURCE_WEIGHT_ZERO"
            weight_status = "w_A BANNED_BY_TYPE"
            jr_status = "J_R_ORDINARY_MATTER_ZERO_CONDITIONAL"
            next_action = "single-branch certificate then boundary/PPN closure"

        rows.append(
            {
                "case_id": case["case_id"],
                "constructor_status": constructor_status,
                "weight_status": weight_status,
                "J_R_status": jr_status,
                "claim_allowed": False,
                "valid_for_claim": False,
                "next_action": next_action,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4008_0_forward_step",
            "decision": "source-label weights are banished by a typed matter constructor, not by fitting them small",
            "reason": "no Hom(source/species/material label -> R_+ source weight) and no R_AB argument makes w_A(R_AB) ill-typed",
            "effect": "the clean derivation route for J_R source-weight silence is now explicit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4008_1_no_claim",
            "decision": "do not claim J_R=0 yet",
            "reason": "constructor packet is written but not adopted into a final single parent branch, and q-kernel/coframe/boundary gates remain",
            "effect": "local GR/Newton remains blocked but closer",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4008_2_fallback",
            "decision": "if the constructor is not adopted, use the J_R coefficient pack",
            "reason": "the same rows now define w_R_source, b_theta_R and readout_regen_R with units and source paths",
            "effect": "no vague missing coupling; either typed-zero or finite parameterized residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4008_3_next",
            "decision": "next target is the q-kernel/observed-coframe single-branch certificate",
            "reason": "after source-label weights are typed out, the largest remaining bulk matter term is geometric descent of actual R_AB",
            "effect": "4009 should attack v_R in ker(Dq) and e_obs=Obs(q(Phi)) in the same branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4008_0_no_Hom_weight",
            "claim": "w_A(R_AB) source weights are impossible",
            "allowed": False,
            "blocker": "true only inside the typed constructor packet, which is not yet adopted in a final parent action branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4008_1_JR_zero",
            "claim": "J_R=0",
            "allowed": False,
            "blocker": "q-kernel, observed coframe descent, boundary/worldtube and same-branch adoption remain open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4008_2_local_GR",
            "claim": "local GR/Newton recovered",
            "allowed": False,
            "blocker": "4008 closes a source-weight route conditionally but not the full local-GR reduction",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4008_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove actual R_AB variation is vertical for the parent quotient and that observed coframe/metric descend through the same q, or keep J_R_geom as a finite row",
            "success_condition": "one branch has v_R in ker(Dq), e_obs=Obs_e(q(Phi)), omega_obs=omega[e_obs], and no hidden coframe leakage; otherwise J_R_geom gets units, source path and arena projections with valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "source-label-forgetting parent matter constructor packet written; w_A(R_AB) is ill-typed if adopted, while finite J_R coefficient pack remains for nonadoption",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4008 - Source-Label-Forgetting Parent Functor Or J_R Coefficient Pack",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The dangerous coupling is now targeted at the right level: the parent matter object language.",
        "",
        "The proposed ordinary-matter constructor is",
        "",
        "`S_ord := sum_A int_M L_A(psi_A, D_obs psi_A, e_obs(q(Phi)), omega_obs(q(Phi)), theta_A) dmu_obs`.",
        "",
        "Here `A` is only a direct-sum/representation label. It is not a field, not a source coordinate, not a scalar coupling slot, and not an argument of the parent action.",
        "",
        "## No-Hom Rule",
        "",
        "The constructor explicitly sets",
        "",
        "`Hom(source/species/material label, R_+ source weight) = empty`",
        "",
        "and also excludes `R_AB` from the ordinary matter argument list. Therefore",
        "",
        "`S_matter = sum_A w_A(R_AB) S_A`",
        "",
        "is ill-typed unless a new explicit source sector is added. That is the clean derivation route: do not tune `w_A`; ban the constructor that creates it.",
        "",
        "## What This Closes",
        "",
        "- source-label/prevariation weights are conditionally zero by type, not by optimism.",
        "- `b_theta_R` is conditionally zero if constants are fixed representation data.",
        "- `readout_regen_R` is conditionally zero if readout is post-variation or q-basic fixed.",
        "- `epsilon_species_A` remains a bound scale only, not a derived parent coefficient.",
        "",
        "## What This Does Not Close",
        "",
        "This does not yet prove the full local branch. We still need the same parent branch to prove `v_R in ker(Dq)`, `e_obs=Obs_e(q(Phi))`, boundary/worldtube nohair, and later PPN/second-order source closure.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: constructor=`{row['constructor_status']}`, weight=`{row['weight_status']}`, J_R=`{row['J_R_status']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is a real narrowing: the coupling leak is no longer a vague missing ingredient. It is either illegal by parent type signature, or it is a finite residual with named coefficients.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4008 - Source-Label-Forgetting Matter Constructor"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: proposed typed ordinary-matter constructor `S_ord=sum_A int L_A(psi_A,D_obs psi_A,e_obs(q(Phi)),omega_obs(q(Phi)),theta_A)dmu_obs`.
- No-Hom rule: source/species/material labels are direct-sum labels only, with no `Hom(label,R_+ source weight)` and no `R_AB` argument in ordinary matter.
- Consequence: `S_matter=sum_A w_A(R_AB)S_A` is ill-typed if this packet is adopted; otherwise `w_R_source_4008`, `b_theta_R`, and `readout_regen_R` remain finite nonclaim rows.
- No claim: packet is not adopted into a final parent branch; q-kernel, observed coframe descent and boundary/worldtube gates remain.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4008 - Source-Label-Forgetting Matter Constructor" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    constructor: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4008_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4008_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4008_02_signature", any(row["constructor_id"] == "SLF4008_0_signature" for row in constructor), "constructor signature present")
    add("VAL4008_03_nohom", any(row["constructor_id"] == "SLF4008_1_source_labels" and "Hom((A,R_AB),R_+)" in row["forbidden_arguments"] for row in constructor), "no-Hom rule present")
    add("VAL4008_04_constants", any(row["constructor_id"] == "SLF4008_2_constants" for row in constructor), "constant packet present")
    add("VAL4008_05_hilbert", any(row["constructor_id"] == "SLF4008_3_hilbert_source" for row in constructor), "Hilbert source packet present")
    add("VAL4008_06_readout", any(row["constructor_id"] == "SLF4008_4_readout_order" for row in constructor), "readout packet present")
    add("VAL4008_07_not_adopted", all(str(row["adopted_in_parent_action"]).lower() == "false" for row in constructor), "packet not silently adopted")
    add("VAL4008_08_type_rejection", any(row["proof_id"] == "NOHOM4008_0_type_rejection" and "ill-typed" in row["result"] for row in proof), "type rejection proof present")
    add("VAL4008_09_variation", any(row["proof_id"] == "NOHOM4008_1_variation" for row in proof), "variation proof present")
    add("VAL4008_10_owner", any(row["proof_id"] == "NOHOM4008_2_hilbert_owner" for row in proof), "Hilbert owner proof present")
    add("VAL4008_11_scope", any(row["proof_id"] == "NOHOM4008_4_not_full_local_GR" for row in proof), "scope guard present")
    add("VAL4008_12_reject_weight", any(row["rejection_id"] == "REJ4008_0_weight" for row in rejections), "weight rejection present")
    add("VAL4008_13_reject_kappa", any(row["rejection_id"] == "REJ4008_1_species_kappa" for row in rejections), "kappa rejection present")
    add("VAL4008_14_reject_marker", any(row["rejection_id"] == "REJ4008_2_marker_constant" for row in rejections), "marker rejection present")
    add("VAL4008_15_reject_readout", any(row["rejection_id"] == "REJ4008_3_readout_mask" for row in rejections), "readout mask rejection present")
    w_row = next(row for row in coefficients if row["row_id"] == "JRCP4008_0_w_R_source")
    theta_row = next(row for row in coefficients if row["row_id"] == "JRCP4008_1_b_theta_R")
    readout_row = next(row for row in coefficients if row["row_id"] == "JRCP4008_2_readout_regen_R")
    eta_row = next(row for row in coefficients if row["row_id"] == "JRCP4008_3_epsilon_species_A")
    add("VAL4008_16_w_coeff", "ZERO_IF" in w_row["value"] and w_row["units"] == "per_RAB", "w_R_source coefficient row present")
    add("VAL4008_17_theta_coeff", "ZERO_IF" in theta_row["value"] and theta_row["units"] == "per_RAB", "theta coefficient row present")
    add("VAL4008_18_readout_coeff", "ZERO_IF" in readout_row["value"], "readout coefficient row present")
    add("VAL4008_19_eta_bound", float(eta_row["value"]) == ETA_SOURCE_BOUND and eta_row["source_status"] == "BOUND_SCALE_ONLY_NOT_THEORY_VALUE", "eta bound scale remains nonclaim")
    add("VAL4008_20_projection", any(row["row_id"] == "JRCP4008_5_projection_required" for row in coefficients), "arena projection guard present")
    adopted = next(row for row in results if row["case_id"] == "CASE4008_0_packet_adopted_all_local_clauses")
    illegal = next(row for row in results if row["case_id"] == "CASE4008_1_packet_adopted_weight_requested")
    not_adopted = next(row for row in results if row["case_id"] == "CASE4008_2_packet_not_adopted")
    q_open = next(row for row in results if row["case_id"] == "CASE4008_3_q_kernel_open")
    coframe = next(row for row in results if row["case_id"] == "CASE4008_4_coframe_open")
    boundary = next(row for row in results if row["case_id"] == "CASE4008_5_boundary_open")
    finite = next(row for row in results if row["case_id"] == "CASE4008_6_numeric_pack")
    add("VAL4008_21_adopted_case", adopted["J_R_status"] == "J_R_ORDINARY_MATTER_ZERO_CONDITIONAL", "adopted case gives conditional ordinary-matter J_R zero")
    add("VAL4008_22_illegal_case", illegal["constructor_status"] == "ILLEGAL_TERM_REJECTED", "illegal weight rejected")
    add("VAL4008_23_not_adopted_case", not_adopted["constructor_status"] == "PACKET_WRITTEN_NOT_ADOPTED", "nonadoption keeps J_R open")
    add("VAL4008_24_q_case", q_open["J_R_status"] == "J_R_GEOMETRY_COMPONENT_OPEN", "q-kernel open case routed")
    add("VAL4008_25_coframe_case", coframe["J_R_status"] == "J_R_HILBERT_GEOMETRY_OPEN", "coframe open case routed")
    add("VAL4008_26_boundary_case", boundary["J_R_status"] == "J_R_BOUNDARY_WORLD_TUBE_OPEN", "boundary open case routed")
    add("VAL4008_27_finite_case", finite["constructor_status"] == "FINITE_COEFFICIENT_PACK_NONCLAIM", "finite pack case routed")
    add("VAL4008_28_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4008_29_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4008_30_doc_exists", DOC_PATH.exists() and "No-Hom Rule" in read_text(DOC_PATH), "document written")
    add("VAL4008_31_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4008_32_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4008_33_compile", compile_ok, "script compiles")
    add("VAL4008_34_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [sources, constructor, proof, rejections, coefficients, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4008_35_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4008_36_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4008_37_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4008_38_forward_target", "q-kernel" in read_text(OUTPUTS["next"]) and "coframe" in read_text(OUTPUTS["next"]), "forward target is geometric descent, not repeat audit")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    constructor = constructor_rows(timestamp)
    proof = proof_rows(timestamp)
    rejections = rejection_rows(timestamp)
    coefficients = coefficient_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["constructor"], constructor)
    write_csv(OUTPUTS["proof"], proof)
    write_csv(OUTPUTS["rejections"], rejections)
    write_csv(OUTPUTS["coefficients"], coefficients)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, constructor, proof, rejections, coefficients, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4008 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
