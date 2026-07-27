from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3404-Y5-R2FR-source-calibrated-EH-parent-ownership-audit-under-AX1090.md"

SOURCES = {
    "doc_1340": ROOT / "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
    "doc_3340": ROOT / "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
    "doc_3399": ROOT / "3399-Y5-R2FR-source-normalization-component-extractor-under-AX1090.md",
    "doc_3400": ROOT / "3400-Y5-R2FR-first-order-source-coupling-parent-signature-pack-under-AX1090.md",
    "doc_3401": ROOT / "3401-Y5-R2FR-kappav-second-order-beta-ledger-under-AX1090.md",
    "doc_3402": ROOT / "3402-Y5-R2FR-v-second-order-source-square-theorem-attempt-under-AX1090.md",
    "doc_3403": ROOT / "3403-Y5-R2FR-PiM-boundary-readout-operator-beta-residual-fill-under-AX1090.md",
    "sceh_stack": OUT / "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
    "eh_core_1340": OUT / "P8_Y5_R10_1340_EH_CORE_SELECTION_ATTEMPT.csv",
    "eh_zero_1340": OUT / "P8_Y5_R10_1340_ZERO_ROUTE_REQUIREMENTS.csv",
    "eh_bound_1340": OUT / "P8_Y5_R10_1340_BOUND_ROUTE_REQUIREMENTS.csv",
    "hilbert_clause_3340": OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
    "hilbert_theorem_3340": OUT / "P8_Y5_R2FR_3340_HILBERT_SOURCE_THEOREM_OR_FAIL.csv",
    "hilbert_score_3340": OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv",
    "newton_theorem_3399": OUT / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
    "parent_clauses_3400": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "activation_3400": OUT / "P8_Y5_R2FR_3400_FIRST_ORDER_ACTIVATION_THEOREM.csv",
    "component_ledger_3401": OUT / "P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv",
    "premise_audit_3402": OUT / "P8_Y5_R2FR_3402_PREMISE_AUDIT.csv",
    "source_square_3402": OUT / "P8_Y5_R2FR_3402_SOURCE_SQUARE_THEOREM.csv",
    "zeroes_3403": OUT / "P8_Y5_R2FR_3403_RETAINED_LANE_ZERO_THEOREMS.csv",
    "formulas_3403": OUT / "P8_Y5_R2FR_3403_RETAINED_LANE_RESIDUAL_FORMULAS.csv",
    "next_3403": OUT / "P8_Y5_R2FR_3403_NEXT_TARGET.csv",
    "r11_beta": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "local_eh_r11": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3404_SOURCE_REGISTER.csv",
    "ownership_clauses": OUT / "P8_Y5_R2FR_3404_PARENT_OWNERSHIP_CLAUSES.csv",
    "conditional_theorem": OUT / "P8_Y5_R2FR_3404_CONDITIONAL_EH_OWNERSHIP_THEOREM.csv",
    "obstruction_theorem": OUT / "P8_Y5_R2FR_3404_EH_IMPORT_OBSTRUCTION_THEOREM.csv",
    "premise_scorecard": OUT / "P8_Y5_R2FR_3404_PREMISE_SCORECARD.csv",
    "operator_survival": OUT / "P8_Y5_R2FR_3404_NONEH_OPERATOR_SURVIVAL_LAW.csv",
    "lane_impact": OUT / "P8_Y5_R2FR_3404_KAPPAV_LOCAL_GR_IMPACT.csv",
    "newton_g_policy": OUT / "P8_Y5_R2FR_3404_NEWTON_G_POLICY.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3404_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3404_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3404_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3404_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3404_VALIDATION.csv",
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
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "sceh_stack": "source-calibrated EH proof-stack rungs to be parent-owned",
        "eh_core_1340": "prior EH core selection obstruction and Lovelock route",
        "hilbert_clause_3340": "one-descended-geometry Hilbert source clause",
        "newton_theorem_3399": "first-order Newton/source-amplitude conditional theorem",
        "parent_clauses_3400": "candidate parent signature clauses PC3400_0..6",
        "component_ledger_3401": "kappa_v beta component ledger",
        "premise_audit_3402": "premises blocking source-square beta claim",
        "zeroes_3403": "retained beta lane conditional zero routes",
        "r11_beta": "non-EH operator beta family vector",
        "local_eh_r11": "local EH/R11 operator audit",
    }
    rows = []
    for source_id, path in SOURCES.items():
        rows.append({
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles.get(source_id, "supporting lineage/source evidence"),
            "valid_for_claim": False,
        })
    return rows


def ownership_clauses() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "EHO3404_0_q_basic_metric",
            "parent_clause": "one q-basic observed metric/coframe owns matter, clocks, photons, source variation and PPN readout through O(U^2)",
            "mathematical_content": "g_obs=g_matter=g_source=g_readout; Lie_vertical g_obs=0; no representative-dependent readout",
            "needed_to_derive": "PPN coefficients refer to one physical metric rather than a stitched readout",
            "current_status": "PARTIAL_SUPPORT_NOT_OU2_PARENT_SIGNED",
            "closes": "readout lane; source/current scale drift; observed-branch ambiguity",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_1_metric_second_order_selector",
            "parent_clause": "compact exterior quotient equations are local, four-dimensional, metric-only and second-order at the PPN order being claimed",
            "mathematical_content": "Fields_ext={g_obs}; E_mn[g] contains at most second derivatives; c_R2=c_fR=c_Weyl=c_scalar=c_vector=c_X=0 or silent",
            "needed_to_derive": "Lovelock activation: E_mn=a G_mn+b g_mn instead of importing the EH operator",
            "current_status": "NOT_PARENT_SIGNED_R11_OPERATORS_RETAINED",
            "closes": "operator lane; eta/source square route; EH-only exterior",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_2_levi_civita_connection",
            "parent_clause": "the observed connection is Levi-Civita or independent connection modes are pure gauge/source-silent",
            "mathematical_content": "Gamma=LC(g_obs); T^lambda_mn=0; Q_lambda_mn=0; hypermomentum/readout connection residual=0",
            "needed_to_derive": "Palatini/metric compatibility step and removal of torsion/nonmetricity PPN leakage",
            "current_status": "NOT_PARENT_SIGNED_CONNECTION_ROW_RETAINED",
            "closes": "torsion/nonmetricity R11 family; clock/light/source connection residual",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_3_same_Hilbert_source",
            "parent_clause": "ordinary matter and EM source tensors come from one descended Hilbert action before calibration",
            "mathematical_content": "T_total^mn=(-2/sqrt(-g)) delta(S_matter+S_EM)/delta g_mn; J^mn=kappa_* T_total^mn",
            "needed_to_derive": "universal source coupling and Ward/Bianchi balance",
            "current_status": "STRONG_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "closes": "delta_ellJ; species/tensor/EM source-selector residuals",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_4_single_mass_nohair",
            "parent_clause": "ordinary compact exteriors have one Hamiltonian/Pi_M mass parameter and no independent scalar/vector/domain/memory/boundary hair",
            "mathematical_content": "g_ext=g_Schwarzschild_or_SdS(mu)+background; d hair_i=0; hair_i=0 by constraint/boundary condition",
            "needed_to_derive": "B_source=A_source^2 and no hidden O(U^2) beta source response",
            "current_status": "CONDITIONAL_EH_MATH_NOT_MTS_OWNED",
            "closes": "source_quad; operator hair; boundary/domain leakage",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_5_fixed_boundary_reference",
            "parent_clause": "annulus, primitive/reference and boundary charge are parent-fixed and source-blind",
            "mathematical_content": "B_zero_flux=0; Delta_symp=0; delta_g H_ref=0; no physical Poynting/Hilbert flux hidden in boundary fit",
            "needed_to_derive": "boundary terms cannot act as post-readout mass/beta selectors",
            "current_status": "CONDITIONAL_STOKES_ROUTE_NOT_PARENT_SIGNED",
            "closes": "boundary lane; PiM mass drift; calibration feedback",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_6_measured_mu_lock",
            "parent_clause": "the exterior EH mass parameter equals the measured orbital source and the Hilbert/Pi_M charge in the same branch",
            "mathematical_content": "mu_EH=G_ref M_H[Pi_M J_H]=mu_obs; U=mu_EH/r; kappa_MTS=8 pi G_ref/c^4",
            "needed_to_derive": "Newtonian limit and source calibration without circular GM backfill",
            "current_status": "FIRST_ORDER_STAGED_SECOND_ORDER_UNSIGNED",
            "closes": "delta_kappa; epsilon_Gref_match; epsilon_M; source normalization",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_7_fixed_PPN_readout",
            "parent_clause": "the isotropic/PPN expansion is read by one fixed post-smoothing projector in one local patch",
            "mathematical_content": "P_PPN fixed; nabla P_PPN=0; smoothing before readout; no adaptive ray/frame fit through O(U^2)",
            "needed_to_derive": "beta/gamma are metric coefficients, not artefacts of a changing readout frame",
            "current_status": "CONDITIONAL_READOUT_THEOREM_NOT_PARENT_SIGNED",
            "closes": "readout lane; coframe/gauge drift; beta dictionary ambiguity",
            "valid_for_claim": False,
        },
        {
            "clause_id": "EHO3404_8_q_loc_vector_silence",
            "parent_clause": "q_loc has either a Ward-zero compact exterior profile or separately safe beta and preferred-frame/location projections",
            "mathematical_content": "P_loc(nabla Gamma_eff - nabla Khat)=0 through O(U^2), or beta/alpha_i/xi projections satisfy locks without cancellation",
            "needed_to_derive": "full local PPN, not just beta-only safety",
            "current_status": "OPEN_ALPHA_VECTOR_GUARD",
            "closes": "q_loc beta guard; alpha_i/alpha3/xi guard",
            "valid_for_claim": False,
        },
    ]


def conditional_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "THM3404_0_descent",
            "statement": "If the observed metric/coframe is q-basic and matter/EM descend through it, parent variation projects to a quotient local field equation plus vertical residuals.",
            "derivation": "delta S_parent = <E_Phi,delta Phi>; q-basic variations split into Dq^dagger E_obs plus vertical terms. EHO3404_0 and EHO3404_3 silence the vertical/source-selector terms.",
            "result": "one observed source-coupled field equation is eligible for EH selection",
            "claim_status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "step_id": "THM3404_1_lovelock",
            "statement": "If the compact exterior quotient equation is local, 4D, metric-only, diffeomorphism covariant and second-order, it has EH form.",
            "derivation": "Lovelock-style uniqueness gives E_mn=a G_mn+b g_mn; background subtraction or local asymptotics fixes b/Lambda for the branch.",
            "result": "operator core is EH rather than a fitted GR import",
            "claim_status": "MATHEMATICALLY_CLEAN_IF_EHO3404_1_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "THM3404_2_connection",
            "statement": "If the parent connection is Palatini-EH with no hypermomentum or all independent connection modes are gauge/source-silent, the observed connection reduces to Levi-Civita.",
            "derivation": "delta_Gamma S_EH gives metric compatibility up to projective gauge; torsion/nonmetricity terms are zero or matter/readout silent by EHO3404_2.",
            "result": "no torsion/nonmetricity PPN or clock/light residual survives",
            "claim_status": "EXACT_CONDITIONAL_NOT_CURRENTLY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "THM3404_3_source",
            "statement": "If the same Hilbert source owns matter and EM, the source side is common-mode calibrated by one kappa_*.",
            "derivation": "Diffeomorphism invariance gives the Ward identity; the same action variation defines T_total, J_H, M_H and source density before calibration.",
            "result": "delta_ellJ=0 and noncommon source weights are excluded",
            "claim_status": "EXACT_CONDITIONAL_FROM_3340_3399",
            "valid_for_claim": False,
        },
        {
            "step_id": "THM3404_4_mass_family",
            "statement": "If the exterior is EH-only and one-mass/no-hair, the metric family has one mass parameter mu locked to the Hilbert/Pi_M source.",
            "derivation": "Birkhoff/Schwarzschild-family mathematics supplies the exterior; EHO3404_4 through EHO3404_6 identify mu with G_ref M_H rather than an after-the-fact orbital fit.",
            "result": "U=mu/r is the same U in Newton, PPN, H_tau and Pi_M",
            "claim_status": "CONDITIONAL_EH_MATH_WITH_MTS_OWNERSHIP_OPEN",
            "valid_for_claim": False,
        },
        {
            "step_id": "THM3404_5_beta_square",
            "statement": "The one-parameter EH family gives the source-square law needed for beta=1 after measured-U normalization.",
            "derivation": "With U=A_source W and one mu controlling both terms, B_source=A_source^2; the log-lapse expansion has no U^2 term in v.",
            "result": "kappa_eta=0 and kappa_source_quad=0 if EHO3404 clauses are signed",
            "claim_status": "EXACT_CONDITIONAL_FROM_3402",
            "valid_for_claim": False,
        },
        {
            "step_id": "THM3404_6_retained_lanes",
            "statement": "If PiM, boundary, readout, operator, coupling and q_loc ownership clauses are signed, every retained 3403 beta lane zeroes.",
            "derivation": "Substitute EHO3404_1..8 into the 3403 zero-route table and the 3401 kappa_v component ledger.",
            "result": "kappa_v=0, hence beta=1 in the local metric core",
            "claim_status": "EXACT_CONDITIONAL_NOT_CLAIM_LEVEL",
            "valid_for_claim": False,
        },
        {
            "step_id": "THM3404_7_local_GR_bridge",
            "statement": "If the above also kills gamma, alpha_i, zeta_i and xi residuals, the MTS local branch reduces to GR/PPN at tested orders.",
            "derivation": "beta alone is insufficient; the same operator/source/readout clauses must silence the full PPN residual vector without cancellation.",
            "result": "local-GR route exists as a precise parent-ownership contract, not yet as a claim",
            "claim_status": "CONDITIONAL_BRIDGE_WRITTEN_FULL_VECTOR_OPEN",
            "valid_for_claim": False,
        },
    ]


def obstruction_theorem() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "OBS3404_0_covariance_not_enough",
            "statement": "Diffeomorphism covariance, locality and an observed metric do not by themselves select EH.",
            "counter_family": "sqrt(-g)(aR+b+c1 R^2+c2 R_mn R^mn+c3 C_mnrs C^mnrs)+scalar/vector/connection/boundary terms",
            "why_it_matters": "these terms can preserve a Newtonian-looking first order while shifting beta, gamma, finite-range, clock, WEP or preferred-frame rows",
            "required_fix": "derive a parent normal-form selector, a double-zero coefficient law, or a sourced finite residual bound",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3404_1_EH_import_test",
            "statement": "Using Schwarzschild/SdS before proving EHO3404_1..6 is an EH import, not an MTS derivation.",
            "counter_family": "f(R) or scalar-tensor exterior with the same leading GM/r but extra scalar charge or range",
            "why_it_matters": "the 3402 beta-square theorem is exact only after the EH/no-hair family is parent-owned",
            "required_fix": "make EH-only/no-hair a theorem of the parent quotient branch",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3404_2_connection_gap",
            "statement": "A metric field does not automatically imply the observed connection is Levi-Civita.",
            "counter_family": "metric-affine/projective/torsion/nonmetricity modes with weak source or readout couplings",
            "why_it_matters": "connection modes can leak into clocks, spin, light propagation, WEP and PPN readout",
            "required_fix": "prove Palatini compatibility/source silence or carry the connection residual vector",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3404_3_G_derivation_not_required_but_G_ownership_is",
            "statement": "Local-GR reduction does not require deriving the dimensionful number G from nothing, but it does require one common G_ref across field, source and readout.",
            "counter_family": "separate kappa_field, kappa_source, G_orbit or post-readout GM calibration",
            "why_it_matters": "GR itself calibrates Newton's constant; the non-negotiable MTS task is common-branch ownership, not numerology",
            "required_fix": "sign kappa_MTS=8 pi G_ref/c^4 and mu=G_ref M_H[Pi_M J_H] before readout",
            "valid_for_claim": False,
        },
    ]


def premise_scorecard() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCES["sceh_stack"]):
        rows.append({
            "score_id": "PS3404_" + row["rung_id"].split("_", 1)[-1],
            "source_rung": row["rung_id"],
            "required_identity": row["required_identity"],
            "current_status": row["current_status"],
            "parent_owned_now": False,
            "why_not_owned": "current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim",
            "valid_for_claim": False,
        })
    return rows


def operator_survival() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCES["r11_beta"]):
        rows.append({
            "operator_id": row["component_id"],
            "operator_family": row["operator_family"],
            "survival_law": "allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence",
            "zero_or_safe_condition": row["zero_or_safe_condition"],
            "needed_input": row["required_input"],
            "status": row["status"],
            "valid_for_claim": False,
        })
    return rows


def lane_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "IMP3404_0_first_order_Newton",
            "affected_quantity": "Delta_Newton_v_coupled",
            "if_EHO3404_signed": "0",
            "reason": "EHO3404_3 and EHO3404_6 activate PC3400/T3399 source-normalization zeroes",
            "current_status": "CONDITIONAL_FROM_3399_3400",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3404_1_eta_v",
            "affected_quantity": "kappa_eta",
            "if_EHO3404_signed": "0",
            "reason": "EH one-parameter log-lapse has no U^2 term in v after measured-U normalization",
            "current_status": "CONDITIONAL_FROM_3402",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3404_2_source_quad",
            "affected_quantity": "kappa_source_quad",
            "if_EHO3404_signed": "0",
            "reason": "one mass parameter gives B_source=A_source^2",
            "current_status": "CONDITIONAL_FROM_3402",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3404_3_operator",
            "affected_quantity": "kappa_operator",
            "if_EHO3404_signed": "0",
            "reason": "metric-only second-order selector kills R11 beta operators or moves them into explicit finite bounds",
            "current_status": "OPEN_R11_SELECTOR",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3404_4_PiM_boundary_readout",
            "affected_quantity": "kappa_PiM+kappa_boundary+kappa_readout",
            "if_EHO3404_signed": "0",
            "reason": "fixed parent mass projector, fixed annulus/reference and fixed PPN readout remove post-readout beta leakage",
            "current_status": "CONDITIONAL_FROM_3403",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3404_5_coupling",
            "affected_quantity": "kappa_coupling",
            "if_EHO3404_signed": "0",
            "reason": "same Hilbert source and common kappa extend PC3400 through O(U^2)",
            "current_status": "SECOND_ORDER_EXTENSION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3404_6_q_loc",
            "affected_quantity": "kappa_q_loc plus alpha_i/xi projections",
            "if_EHO3404_signed": "0 only if q_loc vector silence is included",
            "reason": "beta-only compact-shell number is not enough while preferred-frame projection is unsigned",
            "current_status": "OPEN_ALPHA_VECTOR_GUARD",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3404_7_local_GR",
            "affected_quantity": "beta/gamma/alpha_i/zeta_i/xi local PPN vector",
            "if_EHO3404_signed": "passes in the local branch at claimed order, subject to empirical locks",
            "reason": "EH metric core plus source/readout/operator silence is the route from MTS to GR, not a dark-sector patch",
            "current_status": "NOT_CLAIMED_FULL_VECTOR_OPEN",
            "valid_for_claim": False,
        },
    ]


def newton_g_policy() -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "G3404_0_dimensionful_constant",
            "question": "Must MTS derive the numerical value of Newton's constant to reduce to GR/Newton?",
            "answer": "No. A dimensionful constant can be calibrated by measurement, as in GR. What must be derived is that the same branch constant is used everywhere.",
            "required_contract": "kappa_MTS=8*pi*G_ref/c^4 in the field equation and mu=G_ref*M_H[Pi_M J_H] before PPN readout",
            "failure_mode": "separate fitted GM, source kappa, field kappa or readout kappa creates an unowned closure assumption",
            "valid_for_claim": False,
        },
        {
            "policy_id": "G3404_1_predictive_upgrade",
            "question": "What would be stronger than GR-style calibration?",
            "answer": "A parent topological/superselection law for kappa_MTS or a dimensionless relation involving other measured constants.",
            "required_contract": "not required for local-GR reduction; useful later as an MTS-specific upgrade",
            "failure_mode": "chasing G numerology before common-branch ownership distracts from the local-GR bridge",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3404_0_contract",
            "claim": "source-calibrated EH parent-ownership contract is written",
            "gate_pass": True,
            "reason": "EHO3404_0..8 state the exact parent clauses needed to own the EH/no-hair branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3404_1_EH_owned",
            "claim": "EH-only/no-hair branch is derived by MTS parent clauses",
            "gate_pass": False,
            "reason": "metric second-order selector, connection silence and non-EH operator zeroes remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3404_2_source_calibrated",
            "claim": "the EH mass parameter is the same Hilbert/PiM/measured source through O(U^2)",
            "gate_pass": False,
            "reason": "first-order source chain is staged, but second-order parent ownership remains open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3404_3_beta",
            "claim": "kappa_v=0 or beta bound pass is derived",
            "gate_pass": False,
            "reason": "3402 and 3403 give exact conditional routes, but 3404 ownership clauses are not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3404_4_full_PPN",
            "claim": "local GR/PPN vector is derived",
            "gate_pass": False,
            "reason": "gamma and preferred-frame/location/vector residuals still require signed projection maps",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3404_0_progress",
            "finding": "the local-GR route is now an exact parent-ownership contract rather than a loose EH assumption",
            "reason": "3404 connects descent, Lovelock/Palatini, Hilbert source, no-hair, measured mu, readout and q_loc silence in one proof chain",
            "next_action": "attack the parent normal-form EH selector, because it kills the largest cluster of remaining beta lanes",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3404_1_no_claim",
            "finding": "current corpus still cannot claim local GR",
            "reason": "generic covariance allows non-EH operators; MTS-specific selector/zero laws are not signed",
            "next_action": "derive a vertical/quotient symmetry or normal-form principle that forces the non-EH coefficients to zero or makes them boundary/topological",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3404_2_G_constant",
            "finding": "deriving the numerical value of G is optional, but common ownership of G_ref is mandatory",
            "reason": "GR calibrates G; MTS must prevent field/source/readout G from splitting into hidden fit constants",
            "next_action": "keep kappa_MTS as a branch constant while proving kappa_field=kappa_source=kappa_readout",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3405-Y5-R2FR-parent-normal-form-EH-selector-proof-attempt-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3405_parent_normal_form_EH_selector_proof_attempt.py",
            "objective": "try to derive the metric-only second-order EH selector from MTS quotient/vertical symmetry rather than importing Lovelock premises",
            "why_next": "this is the central fork: if it works, eta/source/operator/readout/boundary lanes collapse together; if it fails, non-EH residual bounds become mandatory",
            "valid_for_claim": False,
        },
        {
            "target_id": "3406-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3406_q_loc_U2_alpha_vector_projection_split.py",
            "objective": "separate q_loc beta, alpha_i/alpha3 and xi projections so a beta-safe number cannot hide a preferred-frame failure",
            "why_next": "this is the highest-danger remaining vector guard if the EH selector route starts to close",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3404_0_scope",
            "check": "outputs written only under post-checkpoint-work",
            "status": "PASS_IF_VALIDATION_TRUE",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3404_1_no_public_claim",
            "check": "all generated rows keep valid_for_claim=false",
            "status": "PASS_IF_VALIDATION_TRUE",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3404_2_theory_result",
            "check": "conditional EH ownership theorem written; local-GR claim remains blocked",
            "status": "NONCLAIM_CHECKPOINT",
            "valid_for_claim": False,
        },
    ]


def validation(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": bool(passed), "detail": detail})

    generated_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC)]
    all_nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for name, table in outputs.items()
        if name != "validation"
        for row in table
    )

    add("VAL3404_0_sources", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3404_1_clauses", "parent ownership clauses written", len(outputs["ownership_clauses"]) >= 9, "")
    add("VAL3404_2_conditional_theorem", "conditional EH ownership proof chain written", len(outputs["conditional_theorem"]) >= 7 and any("Lovelock" in row["derivation"] for row in outputs["conditional_theorem"]), "")
    add("VAL3404_3_obstruction", "EH import obstruction theorem written", len(outputs["obstruction_theorem"]) >= 4 and any("Diffeomorphism" in row["statement"] for row in outputs["obstruction_theorem"]), "")
    add("VAL3404_4_operator_survival", "non-EH operator survival law covers R11 beta families", len(outputs["operator_survival"]) >= 12, "")
    add("VAL3404_5_impact", "kappa_v/local-GR impact rows written", len(outputs["lane_impact"]) >= 8, "")
    add("VAL3404_6_g_policy", "Newton G policy recorded", any("dimensionful" in (row["question"] + row["answer"]) for row in outputs["newton_g_policy"]), "")
    add("VAL3404_7_gates_block_claim", "local-GR/beta gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3404_1_EH_owned", "GATE3404_2_source_calibrated", "GATE3404_3_beta", "GATE3404_4_full_PPN"}), "")
    add("VAL3404_8_no_overclaim", "all generated rows are nonclaim", all_nonclaim, "")
    add("VAL3404_9_scope", "no 3404 output path targets formalization-workbench", "formalization-workbench" not in "\n".join(generated_paths), "")
    add("VAL3404_10_next", "next target is parent normal-form EH selector", any("parent-normal-form-EH-selector" in row["target_id"] for row in outputs["next_target"]), "")
    overall = all(row["passed"] for row in rows)
    add("VAL3404_11_overall", "3404 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    parts = [
        "# 3404 - Y5/R2FR source-calibrated EH parent ownership audit under AX1090",
        "",
        "## Verdict",
        "",
        "- The useful result is not a local-GR claim. The useful result is a precise contract for when MTS would own the source-calibrated EH/no-hair branch instead of importing GR.",
        "- The conditional bridge is now explicit: q-basic observed metric, EH selector, Levi-Civita connection, one Hilbert source, one mass parameter, fixed boundary/readout, common G_ref, and q_loc vector silence imply the beta/local metric core route.",
        "- The current corpus does not yet sign the central EH selector. Generic covariance still permits R^2/f(R), Weyl/Ricci-squared, scalar/vector, torsion/nonmetricity, nonlocal, projector/domain and boundary families.",
        "- Newton's constant does not need to be numerically derived for local-GR reduction, but the same G_ref must be owned by the field equation, source charge and readout before fitting.",
        "",
        "## Parent Ownership Clauses",
        md_table(outputs["ownership_clauses"]),
        "",
        "## Conditional EH Ownership Theorem",
        md_table(outputs["conditional_theorem"]),
        "",
        "## EH Import Obstruction Theorem",
        md_table(outputs["obstruction_theorem"]),
        "",
        "## Premise Scorecard",
        md_table(outputs["premise_scorecard"]),
        "",
        "## Non-EH Operator Survival Law",
        md_table(outputs["operator_survival"]),
        "",
        "## Local-GR Impact",
        md_table(outputs["lane_impact"]),
        "",
        "## Newton G Policy",
        md_table(outputs["newton_g_policy"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "ownership_clauses": ownership_clauses(),
        "conditional_theorem": conditional_theorem(),
        "obstruction_theorem": obstruction_theorem(),
        "premise_scorecard": premise_scorecard(),
        "operator_survival": operator_survival(),
        "lane_impact": lane_impact(),
        "newton_g_policy": newton_g_policy(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    outputs["validation"] = validation(outputs)
    for key, path in OUTPUTS.items():
        write_csv(path, outputs[key])
    write_doc(outputs)

    if not all(row["passed"] for row in outputs["validation"]):
        raise RuntimeError("3404 validation failed")

    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print("; ".join(f"{path.name}={len(outputs[key])}" for key, path in OUTPUTS.items()))


if __name__ == "__main__":
    main()
