from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_MATTER_DESCENT_GATE_2611"
CHECKPOINT_ID = "2611"

DOC = ROOT / "2611-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_LINEAGE_LEDGER.csv",
    "matter_descent": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
    "chain_rule": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv",
    "premise_audit": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv",
    "worldtube_audit": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
    "amatter_interface": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_AMATTER_BOUND_INTERFACE.csv",
    "source_zero": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2611_VALIDATION.csv",
}

COPY_TARGETS = {
    "matter_descent": LOCAL_BOUNDS / "Matter_worldtube_descent_attempt_2611_NONCLAIM.csv",
    "amatter_interface": LOCAL_BOUNDS / "Amatter_bound_interface_2611_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Matter_source_zero_status_2611_NONCLAIM.csv",
    "next_target": QUEUE / "JR2611_NO_DIRECT_MATTER_X_VERTEX_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "accepted_for_scoring": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2611_00_2610_handoff_doc",
            "source_path": ROOT / "2610-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "needles": ["NEXT2610_0_selected", "DEC2610_4_best_next", "VAL2610_OVERALL"],
            "role": "current handoff selecting matter/worldtube quotient descent",
        },
        {
            "source_id": "SRC2611_01_2610_source_status",
            "source_path": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_SOURCE_ZERO_STATUS.csv",
            "needles": ["SZ2610_4_source_silence", "SZ2610_5_GR_Newton"],
            "role": "current hidden-source status before matter/worldtube branch",
        },
        {
            "source_id": "SRC2611_02_1760_doc",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["MWD1760_1_conditional_theorem", "AM1760_8_A_matter", "VAL1760_OVERALL"],
            "role": "prior matter/worldtube quotient descent checkpoint",
        },
        {
            "source_id": "SRC2611_03_1760_descent",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1760_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
            "needles": ["MWD1760_0_target", "MWD1760_1_conditional_theorem", "MWD1760_4_current_verdict"],
            "role": "prior matter descent theorem attempt",
        },
        {
            "source_id": "SRC2611_04_1760_chain_rule",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1760_CHAIN_RULE_DECOMPOSITION.csv",
            "needles": ["CR1760_0_variation_identity", "CR1760_4_worldtube", "CR1760_6_direct_vertex"],
            "role": "prior matter vertical variation decomposition",
        },
        {
            "source_id": "SRC2611_05_1760_premises",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1760_DESCENT_PREMISE_AUDIT.csv",
            "needles": ["PRE1760_0_q_map", "PRE1760_4_no_shadow_prefactor", "PRE1760_8_verdict"],
            "role": "prior descent premise audit",
        },
        {
            "source_id": "SRC2611_06_1760_worldtube",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1760_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
            "needles": ["WTA1760_0_support_selector", "WTA1760_1_same_charge", "WTA1760_3_matter_worldtube_verdict"],
            "role": "prior worldtube source owner audit",
        },
        {
            "source_id": "SRC2611_07_1760_amatter",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1760_AMATTER_BOUND_INTERFACE.csv",
            "needles": ["AM1760_0_zero_condition", "AM1760_4_A_direct", "AM1760_8_A_matter"],
            "role": "prior A_matter finite fallback interface",
        },
        {
            "source_id": "SRC2611_08_1761_next_doc",
            "source_path": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
            "needles": ["NDV1761_0_target", "DEC1761_3_best_next", "VAL1761_OVERALL"],
            "role": "prior next route: no direct matter X vertex grammar",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    **false_flags(),
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2611_0_2610",
            "checkpoint": "2610",
            "question": "Which hidden source follows coupling-chain failure?",
            "result": "Ordinary matter/worldtube X coupling is next: prove matter descends through q or carry A_matter.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "matter quotient pullback and worldtube owner",
        },
        {
            "step_id": "LIN2611_1_1760_theorem",
            "checkpoint": "1760",
            "question": "Can ordinary matter be source-silent?",
            "result": "Yes conditionally: if S_matter factors through observed geometry q(Phi), fixed constants, owned lifts, Hilbert worldtubes and silent boundaries, vertical variation vanishes.",
            "status": "EXACT_CONDITIONAL_THEOREM_IMPORTED",
            "next_dependency": "parent signature of descent premises",
        },
        {
            "step_id": "LIN2611_2_1760_premises",
            "checkpoint": "1760",
            "question": "Are descent premises parent-signed?",
            "result": "No. q/coframe, constants, no-marker/source-prefactor, worldtube support, boundary and source-current owners remain unsigned.",
            "status": "PARENT_SIGNATURE_NOT_SIGNED",
            "next_dependency": "A_matter remains live",
        },
        {
            "step_id": "LIN2611_3_1760_worldtube",
            "checkpoint": "1760",
            "question": "Does source worldtube support descend through Hilbert source?",
            "result": "Only conditionally. Same-frame J_H, tau lock, compactness, charge map and coupling descent remain open.",
            "status": "WORLDTUBE_OWNER_OPEN",
            "next_dependency": "A_worldtube_matter retained",
        },
        {
            "step_id": "LIN2611_4_1761_preview",
            "checkpoint": "1761",
            "question": "What matter-specific obstruction remains sharpest?",
            "result": "Direct matter/source grammar: V_m[X,rho_A,W_source], source-only prefactors, hidden frames and material markers.",
            "status": "NEXT_ROUTE_IMPORTED",
            "next_dependency": "2612 no-direct matter X vertex grammar or A_direct pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def matter_descent_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MWD2611_0_target",
            "matter/worldtube X-source zero",
            "J_matter := delta_X V_m|_{X=0}=0, equivalently delta_v S_matter=0 for every local vertical v in ker(Dq)",
            "TARGET_EXACT",
            "ZERO_IF_FULL_DESCENT_CONTRACT_SIGNED",
            "parent q, observed coframe, constants, no-marker, worldtube support and boundary/source-current clauses are not simultaneously signed",
        ),
        (
            "MWD2611_1_conditional_theorem",
            "ordinary matter quotient pullback",
            "S_matter=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]+dB_A, with Dq[v]=0",
            "EXACT_CONDITIONAL_THEOREM",
            "CHAIN_RULE_KILLS_BULK_SOURCE_IF_CLAUSES_HOLD",
            "the theorem is mathematical, but current corpus supplies a contract rather than parent-action ownership",
        ),
        (
            "MWD2611_2_direct_vertex_exclusion",
            "no independent V_m[X,rho_A,W_source]",
            "partial_X V_m|_0=0 because no direct matter/source/worldtube slot may depend on X outside q",
            "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "NOT_SIGNED",
            "ordinary matter functor and no source-only prefactor/no marker grammar are still policy/contract rows",
        ),
        (
            "MWD2611_3_worldtube_support",
            "source worldtube descends through Hilbert support",
            "W_source=closure(supp J_H[tau]) and delta_v W_source=0 when J_H and tau descend through q",
            "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
            "WORLDTUBE_OWNER_OPEN",
            "parent action, same-frame J_H, tau lock, compactness, charge map and coupling descent remain unsigned",
        ),
        (
            "MWD2611_4_current_verdict",
            "J_matter=0 for current MTS",
            "delta_v S_matter=0 for local vertical v",
            "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "A_MATTER_RETAINED",
            "matter descent is exact as a sufficient theorem but cannot be promoted without parent-signing the descent stack",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "status": status,
                "proof_status": proof_status,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, claim_piece, mathematical_form, status, proof_status, gap in rows
    ]


def chain_rule_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CR2611_0_variation_identity",
            "matter action vertical variation",
            "delta_v S_matter = G_e[v] + G_theta[v] + G_Psi[v] + G_W[v] + G_B[v] + G_V[v]",
            "all six terms vanish or are separately source-bounded",
            "EXACT_DECOMPOSITION",
            "A_matter",
        ),
        (
            "CR2611_1_geometry",
            "observed geometry/coframe pullback",
            "G_e[v]=1/2 int sqrt(-g_obs) T^{mu nu} Lie_v g_obs_{mu nu}",
            "g_obs=Obs_g(q(Phi)) and Dq[v]=0, up to owned gauge/Lorentz lift",
            "MISSING_PARENT_Q_AND_OBSERVED_COFRAME_DESCENT",
            "A_geom_matter",
        ),
        (
            "CR2611_2_constants",
            "matter constants/material standards",
            "G_theta[v]=sum_a int J_theta^a Lie_v theta_a",
            "theta_A are representation/superselection labels and Lie_v theta_A=0",
            "MISSING_PARENT_CONSTANT_SUPERSELECTION_AND_TRIVIAL_MTS_ACTION",
            "A_theta_matter",
        ),
        (
            "CR2611_3_matter_lift",
            "matter-field vertical lift",
            "G_Psi[v]=int E_Psi delta_v Psi plus gauge/Lorentz/diffeomorphism boundary terms",
            "delta_v Psi is zero, on-shell, or an owned gauge/local-Lorentz/diffeomorphism lift with proper boundary",
            "MISSING_PARENT_MATTER_LIFT_SIGNATURE",
            "A_lift_matter",
        ),
        (
            "CR2611_4_worldtube",
            "source support/worldtube selector",
            "G_W[v]=delta_v W_source contributions from support, source measure or fitted source domain",
            "W_source=closure(supp J_H[tau]) before readout and tau/J_H descend through q",
            "MISSING_PARENT_WORLDTUBE_SUPPORT_OWNER",
            "A_worldtube_matter",
        ),
        (
            "CR2611_5_boundary",
            "matter/worldtube boundary and exact terms",
            "G_B[v]=delta_v dB_A plus local projection/boundary flux",
            "B_A[v] is zero, exact/proper, compact-support silent, or retained in an absolute tail envelope",
            "MISSING_BOUNDARY_NOFLUX_OR_ABSOLUTE_TAIL_BOUND",
            "A_boundary_matter",
        ),
        (
            "CR2611_6_direct_vertex",
            "independent direct matter/source vertex",
            "G_V[v]=delta_v V_m[X,rho_A,W_source]|_{X=0}",
            "parent grammar forbids any X-dependent matter/source/worldtube slot outside q",
            "MISSING_NO_DIRECT_MATTER_X_VERTEX_THEOREM",
            "A_direct_matter",
        ),
    ]
    return [
        with_stamp(
            {
                "component_id": component_id,
                "component": component,
                "variation_piece": variation_piece,
                "zero_or_bound_condition": zero_or_bound_condition,
                "current_status": current_status,
                "fallback_quantity": fallback_quantity,
                **false_flags(),
            }
        )
        for component_id, component, variation_piece, zero_or_bound_condition, current_status, fallback_quantity in rows
    ]


def premise_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("PRE2611_0_q_map", "parent quotient q and Dq exist before readout", "q: Phi_parent -> Q_obs with Dq[v_X]=0 for local vertical representative directions", "NOT_PARENT_SIGNED", "geometry pullback and matter descent cannot be promoted"),
        ("PRE2611_1_observed_geometry", "observed coframe/metric descends through q", "e_obs=Obs_e(q(Phi)), g_obs=Obs_g(q(Phi)), omega=omega[e_obs]", "NOT_PARENT_SIGNED", "T^{mu nu} Lie_v g_obs term becomes a physical local source"),
        ("PRE2611_2_matter_functor", "ordinary matter action is a functor of observed geometry and fixed representation data", "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]", "CONTRACT_WRITTEN_NOT_PARENT_DERIVED", "direct X/source/worldtube vertices remain legal"),
        ("PRE2611_3_constants", "masses, charges, alpha_EM, clocks and material standards are X-blind", "Lie_v theta_A=0 and no theta_A(X,I_Q,m,h)", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED", "clock, WEP, fine-structure and source-normalization channels remain"),
        ("PRE2611_4_no_shadow_prefactor", "no hidden conformal/disformal frame, source-only weight, marker or post-readout EFT counterterm", "forbid S_ord=sum_A w_A(X,m,W) S_A or g_A=A_A(X)^2 g_obs", "POLICY_CONTRACT_NOT_THEOREM", "relative source/test charge can hide while ordinary-looking matter remains"),
        ("PRE2611_5_worldtube_support", "source worldtube is parent-owned Hilbert support", "W_source=closure(supp J_H[tau]) before source/readout fitting", "CONDITIONAL_NOT_PARENT_SIGNED", "source domain and material support can inject J_matter or source-normalization hair"),
        ("PRE2611_6_boundary", "matter boundary/worldtube terms are zero, exact/proper, or explicitly bounded", "Pi_local delta_v B_A=0 or ||Pi_local delta_v B_A|| is source-backed", "OPEN", "boundary/local projection flux re-enters the X Euler-Lagrange equation"),
        ("PRE2611_7_hilbert_source_owner", "ordinary active source is the same Hilbert/coframe current", "tau_a^mu=det(e)^-1 delta S_matter/delta e_mu^a and one global kappa multiplies sum_A T_A", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED", "non-Hilbert or species-weighted source current remains live"),
        ("PRE2611_8_verdict", "all descent premises hold in one parent branch", "PRE2611_0 through PRE2611_7 all signed", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED", "A_matter remains mandatory"),
    ]
    return [
        with_stamp(
            {
                "premise_id": premise_id,
                "premise": premise,
                "required_statement": required_statement,
                "current_status": current_status,
                "risk": risk,
                **false_flags(),
            }
        )
        for premise_id, premise, required_statement, current_status, risk in rows
    ]


def worldtube_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("WTA2611_0_support_selector", "worldtube source support is not fitted", "W_source=closure(supp J_H[tau]) with compact regular support and linked exterior surfaces", "CONDITIONAL_LEMMA_ONLY", "parent action, same-frame J_H, tau lock, compactness and coupling descent are unsigned"),
        ("WTA2611_1_same_charge", "Hilbert source equals exterior/topological mass source before orbital calibration", "Pi_M J_H = J_M_top + dB_zero and int_W Pi_M J_H = int_S Q_M[tau]", "NOT_DERIVED_KEY_BLOCKER", "R_eq, I_commutator, B_zero_flux and parent Q_M remain nonclaim residuals"),
        ("WTA2611_2_no_readout_domain_mask", "source domain/projector is parent-owned before readout", "Pi_M and W_source are fixed by the parent branch/topology, not selected after seeing orbital data", "GUARDRAIL_INSTALLED_NOT_THEOREM", "projector/domain mismatch can still source N_domain or A_worldtube_matter"),
        ("WTA2611_3_matter_worldtube_verdict", "worldtube terms do not source X", "delta_v W_source=0 and delta_v M_source[W]=0 for vertical v", "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED", "retain A_worldtube_matter inside A_matter until support/charge equality closes"),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, claim_piece, mathematical_form, current_status, gap in rows
    ]


def amatter_interface_rows() -> list[dict[str, Any]]:
    rows = [
        ("AM2611_0_zero_condition", "Z_matter", "Z_matter=True only if q/coframe descent, constants, matter lift, no direct V_m, worldtube support and boundary clauses all pass", "FALSE_PARENT_UNSIGNED", "J_matter=0 condition"),
        ("AM2611_1_A_geom", "A_geom_matter", "||1/2 int sqrt(-g_obs) T^{mu nu} Lie_v g_obs_{mu nu}||_{E*}", "MISSING_Q_COFRAME_DESCENT_OR_A_GEOM", "geometry/coframe pullback leak"),
        ("AM2611_2_A_theta", "A_theta_matter", "||sum_a int J_theta^a Lie_v theta_a||_{E*}", "MISSING_CONSTANT_SUPERSELECTION_OR_A_THETA", "matter constants/material standards leak"),
        ("AM2611_3_A_lift", "A_lift_matter", "||int E_Psi delta_v Psi + proper-boundary lift terms||_{E*}", "MISSING_MATTER_LIFT_OR_A_LIFT", "matter field vertical lift leak"),
        ("AM2611_4_A_direct", "A_direct_matter", "||delta_v V_m[X,rho_A,W_source]|_{X=0}||_{E*}", "MISSING_NO_DIRECT_MATTER_X_VERTEX_OR_A_DIRECT", "direct matter/worldtube X vertex"),
        ("AM2611_5_A_worldtube", "A_worldtube_matter", "||delta_v W_source or source-measure support terms||_{E*}", "MISSING_WORLDTUBE_SUPPORT_OWNER_OR_A_WORLDTUBE", "source support/worldtube selector leak"),
        ("AM2611_6_A_boundary", "A_boundary_matter", "||Pi_local delta_v B_A||_{E*}", "MISSING_MATTER_BOUNDARY_NOFLUX_OR_A_BOUNDARY_MATTER", "matter/worldtube boundary projection leak"),
        ("AM2611_7_A_nonHilbert", "A_nonHilbert_matter", "||J_nonHilbert||_{E*} or theorem-zero from source-owner certificate", "MISSING_NONHILBERT_SOURCE_ZERO_OR_A_NONHILBERT", "non-Hilbert/source-current leak"),
        ("AM2611_8_A_matter", "A_matter", "A_matter <= A_geom_matter + A_theta_matter + A_lift_matter + A_direct_matter + A_worldtube_matter + A_boundary_matter + A_nonHilbert_matter in one E* norm", "MISSING_COMMON_ESTAR_NORM_AND_COMPONENT_VALUES", "||J_matter||_{E*} <= A_matter"),
        ("AM2611_9_R_source_matter", "R_source_matter", "||R_source,matter||_{E*} <= U_B A_matter", "MISSING_AMATTER_AND_ESTAR_UNITS", "retains repaired p_total=1 for bounded matter source unless internal silence is separately proved"),
        ("AM2611_10_R_matter_arena", "R_matter_arena", "||R_matter,arena|| <= U_B ||P_arena L_X^{-1}|| A_matter", "MISSING_OPERATOR_INVERSE_ARENA_PROJECTION_AND_UNITS", "source residual response to matter/worldtube hidden current"),
    ]
    return [
        with_stamp(
            {
                "interface_id": interface_id,
                "quantity": quantity,
                "definition": definition,
                "current_status": current_status,
                "notes": notes,
                **false_flags(),
            }
        )
        for interface_id, quantity, definition, current_status, notes in rows
    ]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("SZ2611_0_matter", "J_matter", "NOT_ZEROED", "1760/2611 give an exact conditional pullback theorem, but all premise gates are not signed", "parent matter functor, q/coframe descent, constants, no-marker/source-prefactor, worldtube support, boundary and source-current owner"),
        ("SZ2611_1_Amatter", "A_matter", "RETAINED_NONCLAIM", "A_matter component interface is explicit and nonclaim", "component values, common E* norm, operator/projection response and source paths for numeric inputs"),
        ("SZ2611_2_direct_vertex", "V_m[X,rho_A,W_source]", "NOT_EXCLUDED", "direct matter/source/worldtube X slot remains a legal countermodel", "parent object-language grammar must forbid the slot or carry A_direct_matter"),
        ("SZ2611_3_worldtube", "W_source support", "NOT_PARENT_OWNED", "worldtube Hilbert/support equality is conditional and unsigned", "A_worldtube_matter remains live"),
        ("SZ2611_4_source_silence", "S_cg(D_L=0,Y)", "NOT_DERIVED", "affine, coupling-chain and matter hidden sources are nonzero/nonclaim; boundary/history/tower/mu/kernel channels remain", "J_hidden still includes A_shift, A_marker, A_matter, A_chain, A_boundary, A_hist, A_tower, A_mu_even and A_kernel"),
        ("SZ2611_5_GR_Newton", "local GR/Newton bridge", "CLOSER_BUT_BLOCKED", "ordinary matter can be made source-silent by exact conditional quotient theorem, but parent signature is missing", "no local-GR source silence follows without matter grammar, worldtube owner and sibling residual closure"),
    ]
    return [
        with_stamp(
            {
                "status_id": status_id,
                "quantity": quantity,
                "current_status": current_status,
                "evidence": evidence,
                "remaining_gap": remaining_gap,
                **false_flags(),
            }
        )
        for status_id, quantity, current_status, evidence, remaining_gap in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2611_0_matter_descent_parent", "ordinary matter descends through q in the parent action", "BLOCKED_Q_COFRAME_MATTER_FUNCTOR_CONSTANTS_NO_MARKER_BOUNDARY_WORLDTUBE"),
        ("GATE2611_1_no_direct_vertex", "no V_m[X,rho_A,W_source] direct matter/worldtube vertex exists", "BLOCKED_NO_DIRECT_MATTER_X_VERTEX_THEOREM"),
        ("GATE2611_2_worldtube_owner", "worldtube support is parent-owned Hilbert support", "BLOCKED_WORLDTUBE_HILBERT_SUPPORT_OWNER_UNSIGNED"),
        ("GATE2611_3_Amatter_zero", "A_matter=0", "BLOCKED_MATTER_DESCENT_NOT_PARENT_SIGNED"),
        ("GATE2611_4_Amatter_bound", "A_matter is finite and sourced in a declared E* norm", "BLOCKED_COMPONENT_VALUES_COMMON_NORM_AND_PROJECTION_RESPONSE_MISSING"),
        ("GATE2611_5_local_GR_Newton", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "status": "BLOCKED_NO_CLAIM",
                "blocker": blocker,
                **false_flags(),
            }
        )
        for gate_id, claim, blocker in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2611_0_conditional_theorem",
            "decision": "matter descent chain-rule theorem is exact conditional",
            "reason": "if S_matter factors through q and the matter/constants/worldtube/boundary clauses hold, vertical variation vanishes",
            "effect": "keep the theorem as a parent-action contract, not a claim",
        },
        {
            "decision_id": "DEC2611_1_parent_signature",
            "decision": "parent signature is not signed",
            "reason": "current evidence still has q/coframe, constants, no-marker/source-prefactor, worldtube support and boundary/source-owner gaps",
            "effect": "retain A_matter and expose its components rather than smuggling local GR",
        },
        {
            "decision_id": "DEC2611_2_A_matter",
            "decision": "write A_matter interface as nonclaim residual",
            "reason": "the zero theorem failed for current MTS, so matter/worldtube hidden source must be bounded or derived later",
            "effect": "do not set A_matter=0; use component rows only as nonclaim plumbing",
        },
        {
            "decision_id": "DEC2611_3_power_convention",
            "decision": "keep explicit U_B on matter source residual",
            "reason": "bounded matter hidden source has p_int=0 unless a separate internal silence theorem is derived",
            "effect": "no accidental U_B^2 promotion from quotient-descent prose",
        },
        {
            "decision_id": "DEC2611_4_best_next",
            "decision": "select no-direct matter X vertex grammar or A_direct/A_worldtube coefficient pack",
            "reason": "the sharpest remaining matter-specific obstruction is V_m[X,rho_A,W_source] or a source-only prefactor",
            "effect": "2612 should attack the typed parent grammar of direct matter/source slots",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2611_0_selected",
            "selection_status": "selected",
            "target_file": "2612-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
            "target_script": "scripts/Y5_R2FR_no_direct_matter_X_vertex_grammar_or_Amatter_coefficient_pack_2612.py",
            "task": "try to prove the parent grammar forbids V_m[X,rho_A,W_source], source-only prefactors, hidden matter frames and material markers; otherwise stage A_direct/A_worldtube/A_theta coefficients",
            "success_condition": "direct matter/worldtube hidden source is theorem-zero or explicit finite A_direct/A_worldtube residual in E* units",
            "fallback_condition": "if grammar remains unsigned, move to parent object-language Hom exclusion or delta_w bound",
            "guardrails": "do not hide material source charge inside readout definitions; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2611_1_Amatter_fallback",
            "selection_status": "held_fallback",
            "target_file": "2612b-Y5-R2FR-Amatter-E-star-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_Amatter_E_star_bound_runner_2612b.py",
            "task": "turn A_geom/A_theta/A_direct/A_worldtube/A_boundary into a runnable nonclaim source-envelope interface with units and projection norms",
            "success_condition": "finite matter residual can be evaluated as nonclaim input",
            "fallback_condition": "local branch remains closure-only",
            "guardrails": "score only after units, E* norm, operator inverse and arena projections are real",
        },
        {
            "route_id": "NEXT2611_2_worldtube_fallback",
            "selection_status": "held_fallback",
            "target_file": "2612c-Y5-R2FR-worldtube-Hilbert-support-owner-or-Aworldtube-bound.md",
            "target_script": "scripts/Y5_R2FR_worldtube_Hilbert_support_owner_or_Aworldtube_bound_2612c.py",
            "task": "try to parent-own W_source=closure(supp J_H[tau]) and same-charge support equality; otherwise carry A_worldtube_matter",
            "success_condition": "worldtube support is parent-zero under vertical variation or explicitly bounded",
            "fallback_condition": "keep A_worldtube_matter as active residual",
            "guardrails": "no fitting source domain after orbital/readout data",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2611_{key}",
                    "source_path": source,
                    "target_path": target,
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    **false_flags(),
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"}
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            joined = " ".join(row_value(value) for value in row.values())
            if "MISSING" in joined:
                if row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True:
                    return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(with_stamp({"check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail, "valid_for_claim": False}))

    add("VAL2611_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2611_01_lineage_complete", {"2610", "1760", "1761"}.issubset({row["checkpoint"] for row in data["lineage"]}), "lineage covers current handoff, prior matter route and next direct-vertex route")
    add("VAL2611_02_conditional_theorem", any(row["audit_id"] == "MWD2611_1_conditional_theorem" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in data["matter_descent"]), "matter descent theorem recorded as exact conditional")
    add("VAL2611_03_matter_not_promoted", any(row["audit_id"] == "MWD2611_4_current_verdict" and row["proof_status"] == "A_MATTER_RETAINED" for row in data["matter_descent"]), "matter/worldtube source remains unpromoted")
    add("VAL2611_04_chain_rule_complete", {"CR2611_1_geometry", "CR2611_4_worldtube", "CR2611_6_direct_vertex"}.issubset({row["component_id"] for row in data["chain_rule"]}), "variation decomposition includes geometry, worldtube and direct vertex")
    add("VAL2611_05_premise_verdict_blocks", any(row["premise_id"] == "PRE2611_8_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED" for row in data["premise_audit"]), "premise audit blocks claim")
    add("VAL2611_06_worldtube_not_signed", any(row["audit_id"] == "WTA2611_3_matter_worldtube_verdict" and row["current_status"] == "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED" for row in data["worldtube_audit"]), "worldtube descent remains unsigned")
    add("VAL2611_07_Amatter_interface_nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["amatter_interface"]), "A_matter interface remains nonclaim")
    add("VAL2611_08_U_B_power_retained", any(row["interface_id"] == "AM2611_9_R_source_matter" and "U_B A_matter" in row["definition"] for row in data["amatter_interface"]), "explicit U_B source-residual factor retained")
    add("VAL2611_09_source_zero_blocked", any(row["status_id"] == "SZ2611_0_matter" and row["current_status"] == "NOT_ZEROED" for row in data["source_zero"]), "matter source zero remains blocked")
    add("VAL2611_10_source_silence_blocked", any(row["status_id"] == "SZ2611_4_source_silence" and row["current_status"] == "NOT_DERIVED" for row in data["source_zero"]), "source silence remains blocked")
    add("VAL2611_11_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2611_12_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2611_13_missing_not_ready", missing_rows_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*MATTER_DESCENT_GATE_2611*", "2611-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md", "*JR2611_NO_DIRECT_MATTER_X_VERTEX_NEXT*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2611_14_no_formalization_artifacts", not formalization_artifacts, "no 2611 matter-descent artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2611_15_decision_next", any(row["decision_id"] == "DEC2611_4_best_next" for row in data["decisions"]), "decision selects no-direct-matter-X-vertex route")
    add("VAL2611_16_next_selected", any(row["route_id"] == "NEXT2611_0_selected" and row["selection_status"] == "selected" for row in data["next"]), "next target selected")
    add("VAL2611_17_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2611_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2611_CSV_{path.stem}", parsed, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2611_COPY_CSV_{key}", parsed, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(with_stamp({"check_id": "VAL2611_OVERALL", "status": "PASS" if overall else "FAIL", "notes": "2611 matter/worldtube descent gate records exact conditional theorem, keeps A_matter nonclaim and selects no-direct-vertex next", "detail": "", "valid_for_claim": False}))
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, divider, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2611: R2FR Matter/Worldtube Quotient Descent Or A_matter Bound",
        "",
        "**Status:** private nonclaim current-branch matter/worldtube checkpoint. This does not claim `J_matter=0`, source silence, local GR, Newton, PPN, R10, WEP, clocks, or orbital closure.",
        "",
        "**Main result:** the matter route has the right GR-shaped theorem but not the parent signature yet. If ordinary matter only sees `e_obs(q(Phi))`, fixed representation data, owned matter lifts, parent-owned Hilbert worldtubes, and silent/proper boundary terms, then `delta_v S_matter=0` for vertical `v in ker(Dq)` and `J_matter=0`. That is the exact chain-rule route to source silence. Current MTS cannot promote it because q/coframe descent, constant/source universality, no hidden source prefactor, worldtube support ownership, boundary silence, non-Hilbert source exclusion, and no direct `V_m[X,rho_A,W_source]` grammar are not all parent-signed. Therefore `A_matter` remains an explicit nonclaim residual, with `||R_source,matter||<=U_B A_matter` unless a separate internal silence theorem is proved.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Matter/Worldtube Descent Attempt",
        markdown_table(data["matter_descent"], ["audit_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Chain Rule Decomposition",
        markdown_table(data["chain_rule"], ["component_id", "component", "variation_piece", "zero_or_bound_condition", "current_status", "fallback_quantity", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Descent Premise Audit",
        markdown_table(data["premise_audit"], ["premise_id", "premise", "required_statement", "current_status", "risk", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Worldtube Source Owner Audit",
        markdown_table(data["worldtube_audit"], ["audit_id", "claim_piece", "mathematical_form", "current_status", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## A_matter Bound Interface",
        markdown_table(data["amatter_interface"], ["interface_id", "quantity", "definition", "current_status", "notes", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source-Zero Status",
        markdown_table(data["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Private Verdict",
        "",
        "This is a useful bridge-to-GR checkpoint. The ordinary-matter theorem has the right shape: if matter is a quotient pullback, vertical hidden-source variation dies. The reason we still cannot claim local GR is equally precise: the parent grammar still allows direct matter/source slots, source-only prefactors, hidden frames, markers, worldtube support leaks, boundary tails, and non-Hilbert currents. Next best punch: prove those direct matter/source slots cannot exist, or keep `A_direct_matter` and `A_worldtube_matter` as honest finite residuals.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def build_data() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "matter_descent": matter_descent_rows(),
        "chain_rule": chain_rule_rows(),
        "premise_audit": premise_audit_rows(),
        "worldtube_audit": worldtube_audit_rows(),
        "amatter_interface": amatter_interface_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def main() -> None:
    data = build_data()

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["matter_descent"], data["matter_descent"])
    write_csv(OUTPUTS["chain_rule"], data["chain_rule"])
    write_csv(OUTPUTS["premise_audit"], data["premise_audit"])
    write_csv(OUTPUTS["worldtube_audit"], data["worldtube_audit"])
    write_csv(OUTPUTS["amatter_interface"], data["amatter_interface"])
    write_csv(OUTPUTS["source_zero"], data["source_zero"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2611_OVERALL")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"overall={overall['status']}")


if __name__ == "__main__":
    main()
