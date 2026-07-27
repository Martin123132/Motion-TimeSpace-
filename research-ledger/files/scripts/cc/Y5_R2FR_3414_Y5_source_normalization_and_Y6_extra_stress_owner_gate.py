from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3414-Y5-R2FR-Y5-source-normalization-and-Y6-extra-stress-owner-gate-under-AX1090.md"

SOURCES = {
    "doc_3413": ROOT / "3413-Y5-R2FR-response-doublet-Gamma-density-construction-test-under-AX1090.md",
    "coverage_3413": OUT / "P8_Y5_R2FR_3413_COMPONENT_COVERAGE_MATRIX.csv",
    "verdict_3413": OUT / "P8_Y5_R2FR_3413_CONSTRUCTION_VERDICT.csv",
    "gates_3413": OUT / "P8_Y5_R2FR_3413_PROMOTION_GATES.csv",
    "theorem_3399": OUT / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
    "chain_3399": OUT / "P8_Y5_R2FR_3399_NEWTON_CLOSURE_CHAIN.csv",
    "gates_3399": OUT / "P8_Y5_R2FR_3399_PROMOTION_GATES.csv",
    "clauses_3400": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "activation_3400": OUT / "P8_Y5_R2FR_3400_FIRST_ORDER_ACTIVATION_THEOREM.csv",
    "gates_3400": OUT / "P8_Y5_R2FR_3400_PROMOTION_GATES.csv",
    "eta_3401": OUT / "P8_Y5_R2FR_3401_ETA_V_EXPONENTIAL_READOUT_DERIVATION.csv",
    "square_3401": OUT / "P8_Y5_R2FR_3401_SOURCE_AB_SQUARE_LAW.csv",
    "kappav_3401": OUT / "P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv",
    "bound_3401": OUT / "P8_Y5_R2FR_3401_KAPPAV_BOUND_TARGET.csv",
    "ward_3411": OUT / "P8_Y5_R2FR_3411_WARD_ZERO_THEOREM.csv",
    "stress_identity_3411": OUT / "P8_Y5_R2FR_3411_STRESS_IDENTITY_PROOF.csv",
    "em_hilbert_3382": OUT / "P8_Y5_R2FR_3382_EM_POYNTING_HILBERT_STRESS_CHAIN.csv",
    "maxwell_route_3339": OUT / "P8_Y5_R2FR_3339_MAXWELL_EM_STRESS_COUPLING_ROUTE.csv",
    "surface_stress_3358": OUT / "P8_Y5_R2FR_3358_SURFACE_STRESS_OWNER_THEOREM.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3414_SOURCE_REGISTER.csv",
    "y5_calibrated_coupling_law": OUT / "P8_Y5_R2FR_3414_Y5_CALIBRATED_COUPLING_LAW.csv",
    "y5_owner_gate_matrix": OUT / "P8_Y5_R2FR_3414_Y5_OWNER_GATE_MATRIX.csv",
    "y6_extra_stress_decomposition": OUT / "P8_Y5_R2FR_3414_Y6_EXTRA_STRESS_DECOMPOSITION.csv",
    "joint_owner_gate_matrix": OUT / "P8_Y5_R2FR_3414_JOINT_OWNER_GATE_MATRIX.csv",
    "newton_gr_implications": OUT / "P8_Y5_R2FR_3414_NEWTON_GR_IMPLICATIONS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3414_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3414_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3414_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3414_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3414_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3413": "response-doublet formal double-zero and Y5/Y6 handoff",
        "coverage_3413": "Y5 hard fail and Y6 retained debt rows",
        "verdict_3413": "declares Y5/Y6 owner gate as next derivation-first target",
        "gates_3413": "q_loc/local-GR promotion remains blocked until Y5/Y6/source gates close",
        "theorem_3399": "exact conditional first-order Newton/source normalization theorem",
        "chain_3399": "delta_kappa/delta_ellJ/epsilon_Gref/delta_KC/epsilon_M closure chain",
        "gates_3399": "first-order theorem assembled but not parent-signed",
        "clauses_3400": "parent signature clauses that would activate the 3399 theorem",
        "activation_3400": "exact-if-signed first-order activation theorem",
        "gates_3400": "parent clause pack not adopted into core theory",
        "eta_3401": "second-order exponential readout derivation beta-1=a_v/2",
        "square_3401": "source square law B_source=A_source^2 needed after measured-GM calibration",
        "kappav_3401": "full beta/kappa_v component ledger",
        "bound_3401": "empirical beta/kappa_v target and absolute envelope",
        "ward_3411": "conditional q_loc Ward-zero theorem",
        "stress_identity_3411": "q_loc as projected divergence of T_GK",
        "em_hilbert_3382": "Poynting/EM stress included by public Hilbert stress route",
        "maxwell_route_3339": "public Maxwell/Hodge stress coupling route and hidden-Hodge residual guard",
        "surface_stress_3358": "surface/contact stress Hilbert ownership and monopole calibration guard",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def y5_calibrated_coupling_law() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "Y5LAW3414_0_calibration_principle",
            "statement": "A universal constant source-coupling normalization is not a local-GR violation by itself.",
            "derivation_or_rule": "GR also takes one fixed G/kappa as a measured coupling; MTS must derive one parent-owned constant before readout, not its SI value from nothing.",
            "closes_if": "kappa_MTS=8*pi*G_ref/c^4 is branch-constant and all matter/EM/source readouts use that same coefficient.",
            "survives_if": "the coupling depends on source, species, radius, frame, memory, domain, boundary, hidden labels, or later orbital backfit.",
            "current_status": "PRINCIPLE_ADOPTED_AS_GATE_NOT_CURRENT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "law_id": "Y5LAW3414_1_first_order_Newton",
            "statement": "The first-order Newton amplitude can be conditionally derived rather than fitted.",
            "derivation_or_rule": "T3399/ACT3400: PC3400 clauses imply delta_kappa=delta_ellJ=epsilon_Gref_match=delta_KC=epsilon_M=0, hence Delta_Newton_v_coupled=0.",
            "closes_if": "PC3400_0 through PC3400_6 are parent-signed in one branch.",
            "survives_if": "the clauses stay staged, or H_tau/Pi_M/source scale/v-coefficient ownership remains unsigned.",
            "current_status": "EXACT_CONDITIONAL_FIRST_ORDER_THEOREM",
            "valid_for_claim": False,
        },
        {
            "law_id": "Y5LAW3414_2_after_calibration_residual",
            "statement": "After measured-GM calibration, only differential/non-universal pieces should be counted as Y5 residuals.",
            "derivation_or_rule": "Define Y5_phys as the no-cancellation envelope over delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC, epsilon_M, source-square beta, drift, range and composition pieces.",
            "closes_if": "each component is theorem-zero in the same branch or has a source-backed numeric bound.",
            "survives_if": "unknown offsets are kept as absolute residual rows; no cancellation credit is allowed.",
            "current_status": "RESIDUAL_DEFINITION_SHARPENED",
            "valid_for_claim": False,
        },
        {
            "law_id": "Y5LAW3414_3_second_order_square_law",
            "statement": "A fitted first-order GM does not secure PPN beta.",
            "derivation_or_rule": "3401: with U=A_source W, beta_eff=B_source/A_source^2, so the safe source branch needs B_source=A_source^2.",
            "closes_if": "parent v/source equations give a_v=0 and B_source=A_source^2 through O(U^2).",
            "survives_if": "A_source and B_source are independently adjustable or uncomputed.",
            "current_status": "SECOND_ORDER_OPEN",
            "valid_for_claim": False,
        },
        {
            "law_id": "Y5LAW3414_4_EM_Poynting_source_rule",
            "statement": "Poynting flux is not a separate background force if it is the Hilbert stress of the public Maxwell action.",
            "derivation_or_rule": "3382/3339: T_EM from the same g_obs Hodge star gravitates through the same kappa/source current; hidden Hodge, hidden current weights or extra Poynting-background vertices reopen residuals.",
            "closes_if": "S_EM is public Maxwell on g_obs with fixed lambda_0 and current owner, varied before readout.",
            "survives_if": "lambda(Phi)F^2, hidden current weights, constitutive background tensors, or double-counted Poynting forces are present.",
            "current_status": "CONDITIONAL_SAFE_CLASS_FOR_EM_STRESS",
            "valid_for_claim": False,
        },
    ]


def y5_owner_gate_matrix() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "Y5G3414_0_constant_kappa",
            "gate": "one fixed kappa_MTS/G_ref before readout",
            "evidence": "PC3400_1 and WFS3377_0 give the exact conditional route",
            "result": "CONDITIONAL_ROUTE_EXTRACTED",
            "blocks_now": True,
            "needed_next": "parent-sign PC3400_1 or keep delta_kappa row",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3414_1_same_Hilbert_source",
            "gate": "same S_matter variation defines T, J_H, M_H and PPN source",
            "evidence": "PC3400_2 and T3399_P2 imply delta_ellJ=0 if adopted",
            "result": "CONDITIONAL_ROUTE_EXTRACTED",
            "blocks_now": True,
            "needed_next": "parent-sign observed-coframe matter descent and ell_J rule",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3414_2_Htau_PiM_Gauss",
            "gate": "Hamiltonian/Gauss/Poisson/PPN mass use the same G_ref branch",
            "evidence": "PC3400_3 and T3399_P3 define the chain but mark it unsigned",
            "result": "UNSIGNED_LINK",
            "blocks_now": True,
            "needed_next": "derive H_tau-H_ref = Pi_M J_H with fixed normalization",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3414_3_no_extra_mass",
            "gate": "no unowned boundary/domain/memory/projector/source mass survives calibration",
            "evidence": "PC3400_4 requires extra channels vanish or remain explicit residual rows",
            "result": "DEPENDENT_ON_Y6_AND_BOUNDARY_ROWS",
            "blocks_now": True,
            "needed_next": "use Y6 safe-class split or residual envelope",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3414_4_v_action_ratio",
            "gate": "v kinetic/source coefficient ratio gives Poisson amplitude",
            "evidence": "PC3400_5 and 3377 derive target L_v=-(c^4/32*pi*G_ref)|grad v|^2-rho_H*c^2*v/2",
            "result": "EXACT_TARGET_PARENT_COEFFICIENTS_UNSIGNED",
            "blocks_now": True,
            "needed_next": "extract A_v/B_v from parent action or keep delta_KC row",
            "valid_for_claim": False,
        },
        {
            "gate_id": "Y5G3414_5_second_order",
            "gate": "first-order calibration extends through beta/source-square order",
            "evidence": "3401 derives beta-1=a_v/2 and delta_beta_source=B_source/A_source^2-1",
            "result": "SECOND_ORDER_OPEN",
            "blocks_now": True,
            "needed_next": "prove a_v=0 and B_source=A_source^2 or bound kappa_v",
            "valid_for_claim": False,
        },
    ]


def y6_extra_stress_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "class_id": "Y6DEC3414_0_ordinary_Hilbert",
            "stress_class": "ordinary matter/EM/surface Hilbert stress",
            "mathematical_form": "T_extra is actually part of T_H = -2/sqrt(-g_obs) delta(S_matter+S_EM+S_surface)/delta g_obs",
            "local_effect": "not an extra force; it is the normal GR source side if coupled through the same kappa",
            "safe_if": "same public g_obs/e_obs action is varied before readout and no hidden labels enter",
            "current_status": "CONDITIONAL_SAFE_CLASS_NOT_Y6_ZERO",
            "valid_for_claim": False,
        },
        {
            "class_id": "Y6DEC3414_1_Lambda_trace",
            "stress_class": "constant vacuum trace",
            "mathematical_form": "T_extra^{mu nu}=-rho_Lambda g_obs^{mu nu} with rho_Lambda constant on the local branch",
            "local_effect": "background/cosmological subtraction; not a local Newton/PPN source at compact-system scale",
            "safe_if": "constant, universal, no gradients, no source dependence, and separated from local mass calibration",
            "current_status": "SAFE_CLASS_IF_PARENT_SUBTRACTION_SIGNED",
            "valid_for_claim": False,
        },
        {
            "class_id": "Y6DEC3414_2_topological_improvement",
            "stress_class": "exact/topological/improvement stress",
            "mathematical_form": "T_extra^{mu nu}=nabla_alpha U^{alpha mu nu}+metric variation of a topological density",
            "local_effect": "no local exterior source if linking-sphere and boundary charges vanish",
            "safe_if": "U has zero compact boundary charge and the topological density has no local metric response",
            "current_status": "CONDITIONAL_BOUNDARY_GATE_OPEN",
            "valid_for_claim": False,
        },
        {
            "class_id": "Y6DEC3414_3_massive_nohair",
            "stress_class": "positive massive auxiliary stress",
            "mathematical_form": "T_extra sourced by fields Z^A with positive operator L_AB and no local source J_A",
            "local_effect": "decays or vanishes on compact local vacuum if no source/boundary charge exists",
            "safe_if": "L_AB positive after constraints, J_A=B_A=0, and readout/projector variation is nonsingular",
            "current_status": "CONDITIONAL_DOUBLE_ZERO_ROUTE_OPEN",
            "valid_for_claim": False,
        },
        {
            "class_id": "Y6DEC3414_4_hidden_projector_stress",
            "stress_class": "hidden/domain/projector/constitutive stress",
            "mathematical_form": "T_extra depends on masks, hidden fields, private Hodge/current weights, memory kernels or unowned projectors",
            "local_effect": "can be conserved by Bianchi and still change beta, alpha_i, xi, zeta_i, source mass or EM propagation",
            "safe_if": "not safe without theorem-zero or empirical bound",
            "current_status": "RETAIN_AS_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "class_id": "Y6DEC3414_5_Bianchi_warning",
            "stress_class": "conserved extra stress in general",
            "mathematical_form": "nabla_mu T_extra^{mu nu}=0",
            "local_effect": "conservation is ownership, not silence; conserved stress can carry monopole/STF/vector charges",
            "safe_if": "one of Y6DEC3414_0..3 applies or a no-cancellation bound row passes",
            "current_status": "BIANCHI_ALONE_DOES_NOT_CLOSE_Y6",
            "valid_for_claim": False,
        },
    ]


def joint_owner_gate_matrix() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "JOG3414_0_Y5_first_order",
            "claim": "Y5 first-order Newton/source amplitude is derivable under parent signature clauses",
            "gate_result": "PASS_CONDITIONAL",
            "evidence": "3399 theorem plus 3400 clause pack imply Delta_Newton_v_coupled=0 if signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "JOG3414_1_Y5_current_core",
            "claim": "Y5 first-order Newton/source amplitude is currently active in core MTS",
            "gate_result": "FAIL_NOT_PARENT_SIGNED",
            "evidence": "3400 promotion gates keep parent adoption false",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "JOG3414_2_Y5_second_order",
            "claim": "Y5 is closed through beta/full PPN source order",
            "gate_result": "FAIL_KAPPAV_OPEN",
            "evidence": "3401 leaves a_v, B_source/A_source^2, PiM, boundary, readout, operator and coupling components unscored",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "JOG3414_3_Y6_EM_Poynting",
            "claim": "EM/Poynting stress is safe if Hilbert-owned by public Maxwell action",
            "gate_result": "PASS_CONDITIONAL_SAFE_CLASS",
            "evidence": "3382/3339/3358 identify ordinary Hilbert stress and forbid hidden Hodge/current double count",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "JOG3414_4_Y6_extra_stress",
            "claim": "all extra stress is topological/invisible/no-hair or below bounds",
            "gate_result": "FAIL_CURRENT_RESIDUAL_CLASS_RETAINS",
            "evidence": "Y6DEC3414_4 and Y6DEC3414_5 show Bianchi conservation alone is insufficient",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "JOG3414_5_local_GR",
            "claim": "MTS has derived local GR/Newton/PPN",
            "gate_result": "BLOCKED_BUT_SHARPER",
            "evidence": "first-order source amplitude is conditionally routed; local GR still needs parent adoption, kappa_v/full PPN and Y6 residual closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def newton_gr_implications() -> list[dict[str, Any]]:
    return [
        {
            "implication_id": "NGI3414_0_G_constant",
            "finding": "MTS does not need to derive the numerical SI value of G to reduce to GR.",
            "why": "The GR comparator itself uses a calibrated universal coupling; the real demand is one fixed parent-owned coefficient used consistently.",
            "effect": "source normalization becomes a universality/constancy/signature gate rather than an impossible from-nothing constant derivation.",
            "valid_for_claim": False,
        },
        {
            "implication_id": "NGI3414_1_first_order_Newton",
            "finding": "There is a coherent exact conditional path to first-order Newton.",
            "why": "PC3400 clauses activate T3399 and give Delta_Newton_v_coupled=0 algebraically.",
            "effect": "the coupling problem is no longer formless; it is a parent-signature adoption problem.",
            "valid_for_claim": False,
        },
        {
            "implication_id": "NGI3414_2_beta_full_PPN",
            "finding": "Full local GR is not won by first-order Newton.",
            "why": "beta needs a_v=0 and B_source=A_source^2 plus PiM/boundary/readout/operator/q_loc/vector stress closure.",
            "effect": "the next derivation should hit v second order and source square law before broad residual scans.",
            "valid_for_claim": False,
        },
        {
            "implication_id": "NGI3414_3_EM_stress",
            "finding": "Poynting/vector EM stress can help if treated as ordinary Hilbert stress, not a private background shove.",
            "why": "public Maxwell on g_obs makes Poynting part of T_EM; hidden Hodge/current/background terms are residuals.",
            "effect": "EM stress can be integrated cleanly into the source-coupling spine without double counting.",
            "valid_for_claim": False,
        },
        {
            "implication_id": "NGI3414_4_q_loc",
            "finding": "q_loc is less mystical but still not gone.",
            "why": "3411 rewrites q_loc as projected extra-stress/Ward residual; 3413 gives a formal double-zero; 3414 shows source/stress clauses decide physical promotion.",
            "effect": "the local-GR route now runs through parent action signature plus second-order/stress owner gates.",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3414_0_Y5_reclassified",
            "gate": "Y5 is reclassified from pure hard fail to calibrated-coupling theorem plus residual envelope",
            "current_result": "PASS_INTERNAL",
            "promotes_if": "not a public claim; it sharpens the private route",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3414_1_first_order_newton",
            "gate": "first-order Newton amplitude closes",
            "current_result": "CONDITIONAL_ONLY_NOT_ADOPTED",
            "promotes_if": "PC3400 clauses are parent-signed in core or equivalent parent action is derived",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3414_2_beta",
            "gate": "beta/kappa_v closes",
            "current_result": "BLOCKED_SECOND_ORDER",
            "promotes_if": "a_v=0, B_source=A_source^2, and all kappa_v components zero/bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3414_3_Y6",
            "gate": "extra stress is harmless",
            "current_result": "PARTIAL_SAFE_CLASSES_RETAINED_RESIDUAL",
            "promotes_if": "T_extra is ordinary Hilbert/Lambda/topological/no-hair or bounded in all local arenas",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3414_4_local_GR",
            "gate": "local GR/Newton/PPN is derived",
            "current_result": "BLOCKED",
            "promotes_if": "PG3414_1, PG3414_2, PG3414_3 and q_loc metric-response gates pass in one branch",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3414_0_actual_progress",
            "finding": "Y5 is no longer just a missing coupling complaint.",
            "reason": "The correct standard is GR-like calibrated universality: one parent-owned G_ref/kappa/source current, then no differential residual.",
            "next_action": "use PC3400 as the private source-coupling contract while deriving second-order terms",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3414_1_do_not_overclaim",
            "finding": "First-order Newton can be conditionally derived but not claimed as current MTS.",
            "reason": "formalization-workbench was not changed and PC3400 remains staged/not adopted.",
            "next_action": "later write a reviewed core integration diff only after the local branch is coherent",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3414_2_Y6_split",
            "finding": "Extra stress has safe classes, and Poynting is safe only in the public Hilbert class.",
            "reason": "Bianchi conservation does not erase hidden/projector/constitutive stress; Hilbert-owned EM stress is ordinary source stress.",
            "next_action": "prove safe-class membership or keep absolute residual bounds for hidden stress",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3414_3_best_next",
            "finding": "The best leap is second-order v/source-square plus Y6 safe-class ownership.",
            "reason": "a_v=0 and B_source=A_source^2 attack beta directly; Y6 safe-class proof prevents stress from re-opening the same door.",
            "next_action": "build 3415 v-source-square and T_extra safe-class proof attempt",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3415-Y5-R2FR-v-source-square-and-Textra-safe-class-proof-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3415_v_source_square_and_Textra_safe_class_proof.py",
            "objective": "try to prove a_v=0, B_source=A_source^2, and safe-class membership for ordinary EM/Poynting/Lambda/topological stresses under the PC3400 parent-coupling clauses",
            "why_next": "3414 reduces Y5 to calibrated first-order coupling plus second-order beta/source-square, and reduces Y6 to safe stress classes versus retained residual stress",
            "valid_for_claim": False,
        },
        {
            "target_id": "3416-Y5-R2FR-q_loc-residual-bound-demotion-after-Y5Y6-failure-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3416_q_loc_residual_bound_demotion_after_Y5Y6_failure.py",
            "objective": "if the second-order/source-square and stress safe-class route fails, demote q_loc/Y5/Y6 to explicit residual components with source-backed bounds",
            "why_next": "do not let a conditional coupling law become a hidden closure assumption",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3414_0",
            "script": str(Path(__file__).resolve()),
            "claim_status": "OWNER_GATE_SYNTHESIS_ONLY",
            "main_result": "Y5 first-order Newton is exact-if-parent-signed; Y6 has safe Hilbert/EM/Lambda/topological/no-hair classes but hidden stress remains residual; local GR remains blocked.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]).lower() == "true" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    y5_reclassified = any(
        row.get("law_id") == "Y5LAW3414_2_after_calibration_residual"
        and row.get("current_status") == "RESIDUAL_DEFINITION_SHARPENED"
        for row in generated["y5_calibrated_coupling_law"]
    )
    first_order_conditional = any(
        row.get("gate_id") == "JOG3414_0_Y5_first_order"
        and row.get("gate_result") == "PASS_CONDITIONAL"
        for row in generated["joint_owner_gate_matrix"]
    )
    second_order_blocked = any(
        row.get("gate_id") == "PG3414_2_beta"
        and row.get("current_result") == "BLOCKED_SECOND_ORDER"
        for row in generated["promotion_gates"]
    )
    y6_residual_retained = any(
        row.get("class_id") == "Y6DEC3414_4_hidden_projector_stress"
        and row.get("current_status") == "RETAIN_AS_RESIDUAL"
        for row in generated["y6_extra_stress_decomposition"]
    )
    poynting_safe_class = any(
        row.get("law_id") == "Y5LAW3414_4_EM_Poynting_source_rule"
        and row.get("current_status") == "CONDITIONAL_SAFE_CLASS_FOR_EM_STRESS"
        for row in generated["y5_calibrated_coupling_law"]
    )
    local_gr_blocked = any(
        row.get("gate_id") == "PG3414_4_local_GR"
        and row.get("current_result") == "BLOCKED"
        for row in generated["promotion_gates"]
    )
    next_derivation = "v-source-square" in generated["next_target"][0]["target_id"]
    rows = [
        {
            "check_id": "VAL3414_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3414_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3414_2_all_nonclaim",
            "check": "all rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3414 is an owner-gate synthesis, not a claim",
        },
        {
            "check_id": "VAL3414_3_Y5_reclassified",
            "check": "Y5 calibrated residual definition is sharpened",
            "passed": y5_reclassified,
            "detail": "constant universal G/kappa is calibration; differential residuals are the testable issue",
        },
        {
            "check_id": "VAL3414_4_first_order_conditional",
            "check": "first-order Newton source amplitude is exact-if-parent-signed",
            "passed": first_order_conditional,
            "detail": "JOG3414_0 passes conditionally",
        },
        {
            "check_id": "VAL3414_5_second_order_retained",
            "check": "beta/kappa_v blocker is not hidden",
            "passed": second_order_blocked,
            "detail": "a_v, source-square, PiM, boundary, readout, operator and coupling remain open",
        },
        {
            "check_id": "VAL3414_6_Y6_residual_retained",
            "check": "hidden/projector/constitutive stress remains residual",
            "passed": y6_residual_retained,
            "detail": "Bianchi alone is not treated as silence",
        },
        {
            "check_id": "VAL3414_7_Poynting_policy",
            "check": "Poynting is routed through Hilbert stress or retained as hidden residual",
            "passed": poynting_safe_class,
            "detail": "public Maxwell safe class recorded",
        },
        {
            "check_id": "VAL3414_8_local_GR_blocked",
            "check": "local-GR promotion remains blocked",
            "passed": local_gr_blocked,
            "detail": "no local-GR/Newton/PPN claim is made",
        },
        {
            "check_id": "VAL3414_9_next_target",
            "check": "next target remains derivation-first",
            "passed": next_derivation,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3414_10_overall",
            "check": "3414 Y5/Y6 owner gate is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3414 - Y5 Source Normalization and Y6 Extra Stress Owner Gate",
            "## Summary\n"
            "- This checkpoint attacks the coupling bottleneck exposed by 3413.\n"
            "- The key improvement is conceptual but mathematical: a universal calibrated `G_ref/kappa_MTS` is allowed, as in GR; the testable Y5 problem is any non-universal, source/range/frame/species/time/readout residual after that calibration.\n"
            "- Existing 3399/3400 work gives an exact conditional first-order Newton closure: if the PC3400 parent clauses are signed in one branch, `Delta_Newton_v_coupled=0`.\n"
            "- This does not close local GR. Beta/full PPN still needs `a_v=0`, `B_source=A_source^2`, and the rest of the `kappa_v` ledger.\n"
            "- Y6 is split into safe stress classes. Public Maxwell/Poynting stress is safe only when it is ordinary Hilbert stress of the observed metric; hidden/projector/constitutive stress remains a residual.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## Y5 Calibrated Coupling Law\n" + md_table(generated["y5_calibrated_coupling_law"]),
            "## Y5 Owner Gate Matrix\n" + md_table(generated["y5_owner_gate_matrix"]),
            "## Y6 Extra Stress Decomposition\n" + md_table(generated["y6_extra_stress_decomposition"]),
            "## Joint Owner Gate Matrix\n" + md_table(generated["joint_owner_gate_matrix"]),
            "## Newton/GR Implications\n" + md_table(generated["newton_gr_implications"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "This is not a local-GR proof, but it is a real tightening of the route. Y5 is no longer treated as 'derive G from nothing'. "
            "The fair GR-level demand is one parent-owned universal coupling and no differential residuals after calibration. "
            "That first-order path is exact-if-signed; the surviving fight is second-order beta/source-square plus hidden extra stress.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "y5_calibrated_coupling_law": y5_calibrated_coupling_law(),
        "y5_owner_gate_matrix": y5_owner_gate_matrix(),
        "y6_extra_stress_decomposition": y6_extra_stress_decomposition(),
        "joint_owner_gate_matrix": joint_owner_gate_matrix(),
        "newton_gr_implications": newton_gr_implications(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3414 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
