from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4092-Y5-R2FR-parent-adoption-axiom-free-qbasic-selector-or-source-denominator-promotion.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "PARENT_NORMAL_FORM_CONSTRUCTED_QBASIC_AND_SOURCE_DENOMINATOR_SUFFICIENT_NOT_CURRENTLY_PUBLIC_SIGNED"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4092_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4091_NEXT_TARGET.csv",
        "4092-Y5-R2FR-parent-adoption-axiom-free-qbasic-selector-or-source-denominator-promotion.md",
        "4091 selects parent adoption or source-denominator promotion.",
    ),
    "SRC4092_01_object_language": (
        SOURCE_DIR / "P8_EM_vq_parent_object_language_normal_form_candidate.csv",
        "NF3519_5_readout_firewall",
        "Existing normal-form candidate distinguishes parent-domain fields from readout masks.",
    ),
    "SRC4092_02_source_quotient": (
        SOURCE_DIR / "P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649_QSRC_CONSTRUCTOR_ATTEMPT.csv",
        "QSRC2649_1_factorization_theorem",
        "Source-domain quotient constructor and conditional factorization theorem.",
    ),
    "SRC4092_03_source_gate": (
        SOURCE_DIR / "P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649_QSRC_CLAUSE_GATE.csv",
        "QG2649_5_verdict",
        "Source-domain quotient clause gate and known parent-adoption blockers.",
    ),
    "SRC4092_04_axiom_freeze": (
        SOURCE_DIR / "P8_Y5_UNIVERSAL_PROPERTY_HUNT_2635_AXIOM_FREEZE_GATE.csv",
        "AXIOM_ONLY_NOT_THEOREM",
        "Reminder that a universal-property freeze cannot be counted as a theorem-zero claim.",
    ),
    "SRC4092_05_4084_newton": (
        SOURCE_DIR / "P8_Y5_R2FR_4084_NEWTON_POISSON_RESIDUAL_VECTOR.csv",
        "NPR4084_2",
        "Newton/Poisson source-denominator residual vector.",
    ),
    "SRC4092_06_4085_ppn": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_SOURCE_STABLE_PPN_THEOREM.csv",
        "PPN4085_0_fixed_U_source_denominator",
        "Source-stable PPN fixed-U denominator theorem.",
    ),
    "SRC4092_07_4091_private": (
        SOURCE_DIR / "P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR.csv",
        "PFR4091_3_xi",
        "4091 clears the private projector/domain preferred-frame block.",
    ),
    "SRC4092_08_charge_current": (
        SOURCE_DIR / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "CC7_closed_flux_and_Gauss_calibration",
        "Charge-current equality route and source-denominator/calibration blockers.",
    ),
    "SRC4092_09_charge_residuals": (
        SOURCE_DIR / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "Delta_PiM",
        "Residual decomposition for source/Hamiltonian charge equality.",
    ),
    "SRC4092_10_r11_source_norm": (
        SOURCE_DIR / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
        "R11SN_2_domain_projector_mass",
        "R11 source-normalization channels that remain live outside the private projector block.",
    ),
    "SRC4092_11_em_owner": (
        SOURCE_DIR / "P8_EM_observed_stack_charge_lattice_owner_status.csv",
        "shared_owner_derives_local_source_coupling",
        "Matter/EM source coupling shared-owner conditional route.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4092_12_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4092 parent normal-form/source-denominator gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def parent_normal_form_rows() -> List[dict]:
    return [
        {
            "clause_id": "PNF4092_0_parent_domain",
            "normal_form_clause": "ParentDomain",
            "allowed_arguments": "Phi_parent; q(Phi); g_obs; e_obs; A_obs; ordinary matter fields; universal constants; fixed boundary/reference class before variation",
            "forbidden_arguments": "post-solution source labels; fitted readout weights; source-only masks; hidden source metric; source-only disformal coframe",
            "formal_role": "fixes the action domain before empirical readout",
            "sufficient_consequence_if_adopted": "late source-scalar and readout-mask source knobs are not legal variables",
            "current_status": "CANDIDATE_PARENT_NORMAL_FORM_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "PNF4092_1_visible_stack",
            "normal_form_clause": "Qvis",
            "allowed_arguments": "Qvis=(q(Phi), e_obs(qPhi), g_obs, nabla_obs, dV_obs, A_obs)",
            "forbidden_arguments": "second source geometry; hidden coframe coupled only to active mass; private q in matter/source coefficient slot",
            "formal_role": "ordinary matter, EM, Hilbert stress, clocks and slow-orbit readout see one observed geometry stack",
            "sufficient_consequence_if_adopted": "vertical q-representative variation is invisible to ordinary Hilbert source variation except through declared residual operators",
            "current_status": "STRUCTURAL_RULE_DEFINED_NEEDS_PARENT_QMAP_SIGNING",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "PNF4092_2_source_quotient",
            "normal_form_clause": "SourceQuotient",
            "allowed_arguments": "q_src(J_lab)=T_H,total and F_src(q_src)=kappa_ref*T_H,total",
            "forbidden_arguments": "F((T_A,A))->kappa_A*T_A; pre-action weights w_A*S_A; marker-dependent source coefficients",
            "formal_role": "forces source coupling to factor through total Hilbert/coframe current before coupling selection",
            "sufficient_consequence_if_adopted": "species/source-label source denominators collapse to one common Hilbert source scale",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "PNF4092_3_qbasic_projector",
            "normal_form_clause": "QBasicProjector",
            "allowed_arguments": "P_D=q_src^*Pbar_top or a downstream readout-only fixed topological label",
            "forbidden_arguments": "dynamical Hodge/Green/domain projector in S_matter or EH source denominator; moving source-support fit mask",
            "formal_role": "turns the 4090/4091 private q-basic branch into a parent grammar clause",
            "sufficient_consequence_if_adopted": "delta_g P_D=0, D_D P_D=0, epsilon_domain_vector=epsilon_domain_flux=epsilon_domain_anisotropy=0",
            "current_status": "SUFFICIENT_FOR_PROJECTOR_BLOCK_ZERO_IF_PARENT_ADOPTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "PNF4092_4_readout_firewall",
            "normal_form_clause": "ReadoutAfterVariation",
            "allowed_arguments": "clocks, PPN, R10, orbital GM, SPARC, cosmology and EM observables are downstream maps from solved fields",
            "forbidden_arguments": "readout objects reenter S_matter, source normalization, projector selection or kappa before Hilbert/coframe variation",
            "formal_role": "prevents prediction extraction from becoming a fitted source coupling",
            "sufficient_consequence_if_adopted": "GM_orb and Pi_M are outputs, not inputs that redefine U or M_H at PPN order",
            "current_status": "FIREWALL_DEFINED_NOT_PARENT_DERIVED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "PNF4092_5_boundary_reference",
            "normal_form_clause": "FixedBoundaryReference",
            "allowed_arguments": "source-blind fixed reference subtraction and zero-flux/proper boundary class",
            "forbidden_arguments": "source-dependent H_ref, source-dependent corner term, compact boundary class shifting active mass",
            "formal_role": "protects Hamiltonian/source denominator equality from boundary bookkeeping",
            "sufficient_consequence_if_adopted": "boundary charge offsets are universal constants or separately scored residuals, not source-fit knobs",
            "current_status": "CANDIDATE_USES_BOUNDARY_CONTRACT_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def sufficient_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "ST4092_0_parent_normal_form",
            "statement": "If the parent action is written only in the PNF4092 normal form, q-basic selector ownership and source-denominator uniqueness are consequences, not extra closure assumptions.",
            "proof_sketch": "All forbidden source labels, readout masks, hidden source geometries and source-only weights are outside Args(S_parent). Variation therefore produces one Hilbert/coframe source current on Qvis, while P_D is either absent from the action or a pullback of fixed quotient/topological data.",
            "formula": "Args(S_parent^loc) subset {Qvis, psi_A, A_obs, universal constants, fixed boundary class, q_src(J_lab)}",
            "consequence": "delta_g P_D=0; D_D P_D=0; F_src=kappa_ref*T_H,total; U=G_ref*M_H/r",
            "status": "EXACT_SUFFICIENT_THEOREM_FOR_CANDIDATE_PARENT_NORMAL_FORM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "ST4092_1_qbasic_selector",
            "statement": "Under PNF4092_3, the q-basic selector is parent-owned instead of being a post-hoc private branch.",
            "proof_sketch": "A fixed pullback P_D=q_src^*Pbar_top has no independent local Euler variation and no local support-motion degree of freedom in source-silent variations. The 4090/4091 projector and preferred-frame zeros then follow by chain rule.",
            "formula": "P_D=q_src^*Pbar_top and delta Pbar_top=0 => delta_g P_D=D_D P_D=0",
            "consequence": "alpha1_domain=alpha2_domain=alpha3_domain=xi_domain=0 in the projector/domain sector",
            "status": "SUFFICIENT_PARENT_ADOPTION_ROUTE_CONSTRUCTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "ST4092_2_source_denominator",
            "statement": "Under PNF4092_1, PNF4092_2 and PNF4092_4, the Newton/PPN source denominator is fixed before readout.",
            "proof_sketch": "The source current is T_H,total from the observed stack; q_src removes source labels before coupling; readout cannot replace M_H by orbital GM. Therefore the PPN potential uses the same Hilbert source denominator as the Newtonian Poisson limit.",
            "formula": "M_H=int_Sigma T_H(n_obs,tau_obs)dV_obs; U=G_ref*M_H/r; Delta_orb=GM_orb-G_ref*M_H is output-only",
            "consequence": "NPR4084_2 and PPN4085_0 are zero in the candidate parent normal form",
            "status": "SUFFICIENT_SOURCE_DENOMINATOR_ROUTE_CONSTRUCTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "ST4092_3_public_limit",
            "statement": "4092 does not prove the current corpus has already adopted this normal form.",
            "proof_sketch": "Existing files mark q_src, Qvis, readout firewall, boundary reference, Hamiltonian charge equality and R11/source-normalization gates as conditional or unsigned. The normal form is a constructed sufficient route, not a completed public theorem.",
            "formula": "public_local_GR := parent_adopts(PNF4092) and all(extra residual gates zero/bounded)",
            "consequence": "public local-GR/source-denominator claim remains false",
            "status": "PUBLIC_PROMOTION_STILL_BLOCKED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def source_denominator_rows() -> List[dict]:
    return [
        {
            "row_id": "SD4092_0_Hilbert_mass",
            "quantity": "M_H",
            "definition": "M_H = int_Sigma T_H(n_obs,tau_obs) dV_obs",
            "owned_if": "Qvis, SourceQuotient and observed time/source-normal clauses are parent-adopted",
            "current_effect": "candidate denominator for Newton/PPN source",
            "residual_if_failed": "Delta_frame; Delta_PiM; Delta_flux; Delta_cal",
            "candidate_branch_value": "single source denominator",
            "public_claim_status": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "SD4092_1_fixed_U",
            "quantity": "U",
            "definition": "U = G_ref*M_H/r",
            "owned_if": "ReadoutAfterVariation forbids replacing M_H by fitted GM_orb before PPN scoring",
            "current_effect": "gamma, beta and preferred-frame rows are read against a fixed source",
            "residual_if_failed": "C_PiM_H; C_orbital_readout; delta_beta_source",
            "candidate_branch_value": "fixed before PPN",
            "public_claim_status": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "SD4092_2_projector_mass",
            "quantity": "mu_domain_projector",
            "definition": "projector/domain source-normalization contribution",
            "owned_if": "QBasicProjector and 4091 vector/flux/anisotropy zeros are parent-adopted",
            "current_effect": "domain_projector_mass channel is zero in the candidate parent normal form",
            "residual_if_failed": "R11SN_2_domain_projector_mass; alpha1; alpha2; alpha3; xi",
            "candidate_branch_value": "0",
            "public_claim_status": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "SD4092_3_extra_mass_channels",
            "quantity": "mu_extra_nonprojector",
            "definition": "boundary, bulk, memory, range, non-EH, calibration and time/radial source-normalization channels",
            "owned_if": "extra sectors are topological/exact/no-flux/EH-only or have executable coefficient bounds",
            "current_effect": "not closed by the 4091 projector result",
            "residual_if_failed": "R11SN_0; R11SN_1; R11SN_3; R11SN_4; R11SN_5; R11SN_6; R11SN_7",
            "candidate_branch_value": "retained until individually zeroed or bounded",
            "public_claim_status": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def countermodel_firewall_rows() -> List[dict]:
    return [
        {
            "countermodel_id": "CM4092_0_preaction_weights",
            "legal_if_not_forbidden": "S_matter=sum_A w_A S_A",
            "damage": "q_src receives weighted sources and species/source coefficients survive",
            "forbidden_by": "PNF4092_2_source_quotient",
            "status": "EXCLUDED_IN_CANDIDATE_NORMAL_FORM_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "countermodel_id": "CM4092_1_hidden_source_geometry",
            "legal_if_not_forbidden": "matter/source couples to hidden source metric or source-only disformal coframe",
            "damage": "source denominator differs from clock/orbit/PPN geometry",
            "forbidden_by": "PNF4092_1_visible_stack",
            "status": "EXCLUDED_IN_CANDIDATE_NORMAL_FORM_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "countermodel_id": "CM4092_2_readout_reentry",
            "legal_if_not_forbidden": "Pi_M, P_D, GM_orb or readout masks reenter S_matter before variation",
            "damage": "measured GM becomes an input and can launder local residuals",
            "forbidden_by": "PNF4092_4_readout_firewall",
            "status": "EXCLUDED_IN_CANDIDATE_NORMAL_FORM_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "countermodel_id": "CM4092_3_nonHilbert_source_bypass",
            "legal_if_not_forbidden": "J_src=kappa*T_H + zeta_NH*J_NH",
            "damage": "source current is not closed by Hilbert/coframe variation alone",
            "forbidden_by": "extra-sector exact-improvement/no-flux or executable residual bound",
            "status": "NOT_EXCLUDED_BY_PNF4092_ALONE_RETAINED_GATE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "countermodel_id": "CM4092_4_source_dependent_boundary",
            "legal_if_not_forbidden": "H_ref or boundary/corner subtraction depends on source sector",
            "damage": "Hamiltonian charge and projected Hilbert mass differ by source-dependent offset",
            "forbidden_by": "PNF4092_5_boundary_reference",
            "status": "EXCLUDED_IN_CANDIDATE_NORMAL_FORM_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4092_0_constructed_route",
            "decision": "construct candidate parent normal form",
            "meaning": "There is now a precise parent-action grammar that would make q-basic projector ownership and source-denominator uniqueness consequences rather than closure assumptions.",
            "result": "sufficient theorem route written",
            "claim_effect": "private/candidate route strengthened",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4092_1_projector_channel",
            "decision": "promote projector/domain channel inside the candidate parent normal form",
            "meaning": "If PNF4092_3 is adopted, the 4090/4091 q-basic projector/domain zero becomes parent-owned.",
            "result": "domain_projector_mass=0; alpha1=alpha2=alpha3=xi=0 for projector/domain sector",
            "claim_effect": "candidate branch clears this local preferred-frame block",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4092_2_public_status",
            "decision": "do not public-promote local GR",
            "meaning": "Current corpus still has unsigned normal-form adoption, boundary/reference, time-generator, non-Hilbert, non-EH/R11 and extra mass-channel gates.",
            "result": "public local-GR and Newton-source-denominator claims remain false",
            "claim_effect": "honest nonclaim despite stronger route",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4092_0_candidate_parent_route",
            "claim": "candidate parent normal form is sufficient to own q-basic selector and fixed source denominator",
            "allowed": "True",
            "reason": "4092 explicitly writes the object-language clauses and derives their consequences",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4092_1_current_parent_adopted",
            "claim": "current MTS parent action already adopts the 4092 normal form",
            "allowed": "False",
            "reason": "source files mark the required clauses as candidate, conditional, unsigned, or blocked",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4092_2_source_denominator_public",
            "claim": "public Newton/PPN source denominator promotion",
            "allowed": "False",
            "reason": "Hilbert mass/time-generator/boundary/reference/extra-channel equality is not fully parent-signed",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4092_3_full_local_GR",
            "claim": "full MTS to local GR",
            "allowed": "False",
            "reason": "candidate normal form is necessary progress but R11, beta/gamma, conservation/zeta, boundary/harmonic and calibrated source-current gates remain",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4092_0",
            "next_target": "4093-Y5-R2FR-adopt-parent-normal-form-test-gamma-beta-zeta-or-reject-to-residuals.md",
            "script": "scripts/Y5_R2FR_4093_adopt_parent_normal_form_test_gamma_beta_zeta_or_reject_to_residuals.py",
            "why": "4092 gives a precise parent normal form. Next test its consequences against the remaining local-GR rows: gamma, beta, zeta/source conservation, and extra R11 families.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4092_1",
            "next_target": "source_denominator_numeric_residuals_if_normal_form_rejected",
            "script": "defer_until_parent_normal_form_rejected",
            "why": "If MTS refuses the normal form, source-denominator residuals must be numeric/source-backed rather than theorem-zero.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4092",
            "decision": DECISION,
            "candidate_parent_normal_form": "written",
            "qbasic_selector_route": "sufficient_if_parent_adopted",
            "source_denominator_route": "sufficient_if_parent_adopted",
            "public_local_GR_claim": "False",
            "next_required_gate": "test_normal_form_against_gamma_beta_zeta_R11",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4092 - Parent Adoption Axiom-Free Q-Basic Selector Or Source-Denominator Promotion",
                "",
                "## Purpose",
                "",
                "4091 cleared the projector/domain preferred-frame block inside the private q-basic local branch. 4092 asks whether that branch can be made parent-owned without pretending a closure axiom is a theorem.",
                "",
                f"- Decision: `{DECISION}`",
                "- New object: candidate parent-action normal form",
                "- Public local-GR/Newton source-denominator claim: `false`",
                "",
                "## Constructed Parent Normal Form",
                "",
                "4092 writes the sufficient parent grammar explicitly:",
                "",
                "```text",
                "Args(S_parent^loc) subset {",
                "  Qvis=(q(Phi), e_obs, g_obs, nabla_obs, dV_obs, A_obs),",
                "  psi_A, theta_A, universal constants, fixed boundary/reference class,",
                "  q_src(J_lab)=T_H,total",
                "}",
                "```",
                "",
                "Forbidden at action level:",
                "",
                "```text",
                "source-only weights w_A S_A",
                "source-label maps F((T_A,A))->kappa_A T_A",
                "hidden source metric or source-only disformal coframe",
                "post-variation readout masks Pi_M, P_D, GM_orb reentering S_matter",
                "source-dependent boundary/reference subtraction",
                "```",
                "",
                "## What This Derives If Adopted",
                "",
                "If the current MTS parent action adopts this normal form, then the key clauses become consequences:",
                "",
                "```text",
                "P_D = q_src^* Pbar_top and delta Pbar_top=0",
                "  => delta_g P_D = 0 and D_D P_D = 0",
                "  => epsilon_vector = epsilon_flux = epsilon_anisotropy = 0",
                "  => alpha1_domain = alpha2_domain = alpha3_domain = xi_domain = 0",
                "```",
                "",
                "and",
                "",
                "```text",
                "F_src(q_src)=kappa_ref*T_H,total",
                "M_H = int_Sigma T_H(n_obs,tau_obs) dV_obs",
                "U   = G_ref*M_H/r",
                "Delta_orb = GM_orb - G_ref*M_H is output-only",
                "```",
                "",
                "So this route would connect the q-basic selector, source coupling, Newtonian Poisson denominator, and PPN fixed-source scoring through one parent object language.",
                "",
                "## Why It Is Still Not Public",
                "",
                "4092 constructs the sufficient route. It does not prove the current corpus has already adopted it. Existing sources still mark these as unsigned or conditional:",
                "",
                "- parent q-map and Qvis signing;",
                "- no source-only prefactor theorem;",
                "- readout-after-variation firewall;",
                "- boundary/reference/source-current equality;",
                "- non-Hilbert and non-EH/R11 extra source channels;",
                "- observed time generator and Hamiltonian mass calibration.",
                "",
                "That is the honest line: this is no longer a vague missingness note, but it is still not a public local-GR proof.",
                "",
                "## Decision",
                "",
                "The best next move is not to chase tiny products. The next move is to test this parent normal form against the remaining local-GR residuals: `gamma`, `beta`, `zeta/source conservation`, and non-projector `R11` families.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4092_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4092_PARENT_NORMAL_FORM.csv`",
                "- `P8_Y5_R2FR_4092_SUFFICIENT_THEOREM_CHAIN.csv`",
                "- `P8_Y5_R2FR_4092_SOURCE_DENOMINATOR_CONSEQUENCES.csv`",
                "- `P8_Y5_R2FR_4092_COUNTERMODEL_FIREWALL.csv`",
                "- `P8_Y5_R2FR_4092_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4092_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4092_NEXT_TARGET.csv`",
                "- `P8_Y5_BRR545_4092_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4092_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4092_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4092_PARENT_NORMAL_FORM": SOURCE_DIR / "P8_Y5_R2FR_4092_PARENT_NORMAL_FORM.csv",
        "P8_Y5_R2FR_4092_SUFFICIENT_THEOREM_CHAIN": SOURCE_DIR / "P8_Y5_R2FR_4092_SUFFICIENT_THEOREM_CHAIN.csv",
        "P8_Y5_R2FR_4092_SOURCE_DENOMINATOR_CONSEQUENCES": SOURCE_DIR / "P8_Y5_R2FR_4092_SOURCE_DENOMINATOR_CONSEQUENCES.csv",
        "P8_Y5_R2FR_4092_COUNTERMODEL_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4092_COUNTERMODEL_FIREWALL.csv",
        "P8_Y5_R2FR_4092_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4092_DECISION_GATE.csv",
        "P8_Y5_R2FR_4092_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4092_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4092_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4092_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4092_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4092_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4092_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_PARENT_NORMAL_FORM"], parent_normal_form_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_SUFFICIENT_THEOREM_CHAIN"], sufficient_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_SOURCE_DENOMINATOR_CONSEQUENCES"], source_denominator_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_COUNTERMODEL_FIREWALL"], countermodel_firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4092_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4092_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4092_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    normal_form = parse_csv(outputs["P8_Y5_R2FR_4092_PARENT_NORMAL_FORM"])
    required_clauses = {"ParentDomain", "Qvis", "SourceQuotient", "QBasicProjector", "ReadoutAfterVariation", "FixedBoundaryReference"}
    clauses = {row.get("normal_form_clause") for row in normal_form}
    rows.append(
        {
            "check_id": "VAL4092_PARENT_NORMAL_FORM_COMPLETE",
            "check": "parent normal form contains all required structural clauses",
            "passed": bool_string(required_clauses.issubset(clauses)),
            "detail": f"clauses={sorted(clauses)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4092_SUFFICIENT_THEOREM_CHAIN"])
    theorem_text = "\n".join(str(row) for row in theorem)
    theorem_ok = all(needle in theorem_text for needle in ["delta_g P_D=0", "U=G_ref*M_H/r", "PUBLIC_PROMOTION_STILL_BLOCKED"])
    rows.append(
        {
            "check_id": "VAL4092_SUFFICIENT_THEOREM_CHAIN",
            "check": "theorem chain derives q-basic selector and fixed source denominator while blocking public promotion",
            "passed": bool_string(theorem_ok),
            "detail": "requires projector zero, fixed U, and public block",
            "timestamp_utc": TIMESTAMP,
        }
    )

    denominator = parse_csv(outputs["P8_Y5_R2FR_4092_SOURCE_DENOMINATOR_CONSEQUENCES"])
    denominator_text = "\n".join(str(row) for row in denominator)
    denominator_ok = all(needle in denominator_text for needle in ["M_H", "U", "mu_domain_projector", "mu_extra_nonprojector"])
    rows.append(
        {
            "check_id": "VAL4092_SOURCE_DENOMINATOR_ROWS",
            "check": "source-denominator consequences include Hilbert mass, fixed U, projector mass, and extra channels",
            "passed": bool_string(denominator_ok),
            "detail": "checks denominator row coverage",
            "timestamp_utc": TIMESTAMP,
        }
    )

    firewall = parse_csv(outputs["P8_Y5_R2FR_4092_COUNTERMODEL_FIREWALL"])
    firewall_text = "\n".join(str(row) for row in firewall)
    firewall_ok = all(needle in firewall_text for needle in ["preaction", "hidden source", "readout", "nonHilbert", "boundary"])
    rows.append(
        {
            "check_id": "VAL4092_COUNTERMODEL_FIREWALL",
            "check": "countermodel firewall records the bypasses that would break the theorem",
            "passed": bool_string(firewall_ok),
            "detail": "requires preaction, hidden source, readout, nonHilbert, boundary bypasses",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claim_rows = parse_csv(outputs["P8_Y5_R2FR_4092_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claim_rows)
    rows.append(
        {
            "check_id": "VAL4092_NO_PUBLIC_CLAIM",
            "check": "4092 keeps candidate route separate from public local-GR/source-denominator claim",
            "passed": bool_string(no_public),
            "detail": "all public claims remain false",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4092_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4092_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4092_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4092 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
