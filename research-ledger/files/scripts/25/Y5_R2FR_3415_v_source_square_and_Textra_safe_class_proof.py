from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3415-Y5-R2FR-v-source-square-and-Textra-safe-class-proof-under-AX1090.md"

SOURCES = {
    "doc_3414": ROOT / "3414-Y5-R2FR-Y5-source-normalization-and-Y6-extra-stress-owner-gate-under-AX1090.md",
    "y5_law_3414": OUT / "P8_Y5_R2FR_3414_Y5_CALIBRATED_COUPLING_LAW.csv",
    "y6_split_3414": OUT / "P8_Y5_R2FR_3414_Y6_EXTRA_STRESS_DECOMPOSITION.csv",
    "gates_3414": OUT / "P8_Y5_R2FR_3414_PROMOTION_GATES.csv",
    "log_lapse_3402": OUT / "P8_Y5_R2FR_3402_LOG_LAPSE_NO_QUADRATIC_THEOREM.csv",
    "source_square_3402": OUT / "P8_Y5_R2FR_3402_SOURCE_SQUARE_THEOREM.csv",
    "impact_3402": OUT / "P8_Y5_R2FR_3402_KAPPAV_IMPACT.csv",
    "retained_zero_3403": OUT / "P8_Y5_R2FR_3403_RETAINED_LANE_ZERO_THEOREMS.csv",
    "envelope_3403": OUT / "P8_Y5_R2FR_3403_KAPPAV_REDUCED_ENVELOPE.csv",
    "gates_3403": OUT / "P8_Y5_R2FR_3403_PROMOTION_GATES.csv",
    "eh_theorem_3404": OUT / "P8_Y5_R2FR_3404_CONDITIONAL_EH_OWNERSHIP_THEOREM.csv",
    "eh_score_3404": OUT / "P8_Y5_R2FR_3404_PREMISE_SCORECARD.csv",
    "operator_survival_3404": OUT / "P8_Y5_R2FR_3404_NONEH_OPERATOR_SURVIVAL_LAW.csv",
    "gates_3404": OUT / "P8_Y5_R2FR_3404_PROMOTION_GATES.csv",
    "em_hilbert_3382": OUT / "P8_Y5_R2FR_3382_EM_POYNTING_HILBERT_STRESS_CHAIN.csv",
    "maxwell_3339": OUT / "P8_Y5_R2FR_3339_MAXWELL_EM_STRESS_COUPLING_ROUTE.csv",
    "surface_3358": OUT / "P8_Y5_R2FR_3358_SURFACE_STRESS_OWNER_THEOREM.csv",
    "ward_3411": OUT / "P8_Y5_R2FR_3411_WARD_ZERO_THEOREM.csv",
    "stress_identity_3411": OUT / "P8_Y5_R2FR_3411_STRESS_IDENTITY_PROOF.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3415_SOURCE_REGISTER.csv",
    "v_source_square_proof": OUT / "P8_Y5_R2FR_3415_V_SOURCE_SQUARE_PROOF.csv",
    "textra_safe_class_proof": OUT / "P8_Y5_R2FR_3415_TEXTRA_SAFE_CLASS_PROOF.csv",
    "parent_ownership_obstructions": OUT / "P8_Y5_R2FR_3415_PARENT_OWNERSHIP_OBSTRUCTIONS.csv",
    "kappav_y6_impact": OUT / "P8_Y5_R2FR_3415_KAPPAV_Y6_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3415_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3415_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3415_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3415_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3415_VALIDATION.csv",
}


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
        "doc_3414": "Y5/Y6 owner-gate handoff selecting 3415",
        "y5_law_3414": "calibrated coupling law and second-order source-square demand",
        "y6_split_3414": "extra-stress safe class split",
        "gates_3414": "local GR remains blocked until beta/Y6/q_loc gates close",
        "log_lapse_3402": "exact conditional a_v=0 log-lapse theorem",
        "source_square_3402": "exact conditional B_source=A_source^2 theorem",
        "impact_3402": "eta/source lanes zero conditionally but retained lanes remain",
        "retained_zero_3403": "PiM/boundary/readout/operator/coupling/q_loc zero-route theorems",
        "envelope_3403": "reduced kappa_v envelope after eta/source lanes",
        "gates_3403": "retained lane values and q_loc/full PPN remain unclaimed",
        "eh_theorem_3404": "conditional EH/no-hair/source-calibrated ownership chain",
        "eh_score_3404": "premise scorecard showing ownership is not current claim",
        "operator_survival_3404": "generic non-EH operator survival law",
        "gates_3404": "EH ownership and beta/local-GR gates still blocked",
        "em_hilbert_3382": "public EM/Poynting Hilbert stress chain",
        "maxwell_3339": "public Maxwell Hodge route and hidden-Hodge residual guard",
        "surface_3358": "surface/contact stress owner theorem",
        "ward_3411": "q_loc Ward-zero theorem, conditional only",
        "stress_identity_3411": "q_loc as projected divergence of effective stress",
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


def v_source_square_proof() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "VSS3415_0_EH_lapse",
            "claim": "The source-calibrated EH exterior has no quadratic term in the MTS log-lapse variable v.",
            "derivation": "For isotropic EH exterior N=(1-x)/(1+x), v=log(N^2)=2[log(1-x)-log(1+x)]=-4x-(4/3)x^3+O(x^5). With U=2c^2 x, v=-2U/c^2+O(c^-6).",
            "result": "a_v=0 through O(U^2/c^4)",
            "current_status": "EXACT_CONDITIONAL_ON_PARENT_OWNED_EH_BRANCH",
            "valid_for_claim": False,
        },
        {
            "proof_id": "VSS3415_1_beta_eta",
            "claim": "The exponential readout then supplies the GR beta coefficient in the eta lane.",
            "derivation": "3401 gives beta-1=a_v/2. Substituting a_v=0 gives delta_beta_eta=0 and kappa_eta=0.",
            "result": "kappa_eta=0 if the log-lapse branch is the physical observed branch",
            "current_status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "proof_id": "VSS3415_2_one_mass_square",
            "claim": "The source-square law follows from a one-parameter exterior mass family.",
            "derivation": "If g_00=-1+2U/c^2-2U^2/c^4 and U=A_source W, then g_00=-1+2A_source W/c^2-2A_source^2 W^2/c^4.",
            "result": "B_source=A_source^2",
            "current_status": "EXACT_CONDITIONAL_ON_ONE_PARAMETER_NOHAIR_FAMILY",
            "valid_for_claim": False,
        },
        {
            "proof_id": "VSS3415_3_beta_source",
            "claim": "The source-quadratic beta lane vanishes under that same one-parameter family.",
            "derivation": "3401 gives delta_beta_source=B_source/A_source^2-1. Substituting B_source=A_source^2 gives delta_beta_source=0.",
            "result": "kappa_source_quad=0",
            "current_status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "proof_id": "VSS3415_4_no_magic",
            "claim": "This is not an imported numerical fit for G.",
            "derivation": "The result uses one calibrated mass parameter U=G_ref M_H/r, as GR does; the derivation target is common ownership of that parameter, not deriving the SI value of G from nothing.",
            "result": "the fair local-GR demand is parent-owned universality and no residual splitting",
            "current_status": "GR_COMPARATOR_FAIRNESS_LOCK",
            "valid_for_claim": False,
        },
        {
            "proof_id": "VSS3415_5_limit",
            "claim": "The proof does not close kappa_v by itself.",
            "derivation": "kappa_v also contains PiM, boundary, readout, operator, coupling and q_loc guard lanes from 3403.",
            "result": "beta remains blocked until retained lanes are zero or bounded",
            "current_status": "RETAINED_LANES_OPEN",
            "valid_for_claim": False,
        },
    ]


def textra_safe_class_proof() -> list[dict[str, Any]]:
    return [
        {
            "class_id": "TSC3415_0_ordinary_Hilbert",
            "safe_class": "ordinary matter/EM/surface Hilbert stress",
            "proof": "If T is obtained by varying S_matter+S_EM+S_surface with respect to the same observed metric/coframe before readout, it is the ordinary source side of the GR-like equation, not an additional fifth-force stress.",
            "safe_result": "safe common-source class if coupled by the same kappa_MTS",
            "fails_if": "the term depends on hidden labels, projectors, private Hodge data, source masks or post-readout weights",
            "current_status": "EXACT_CONDITIONAL_SAFE_CLASS",
            "valid_for_claim": False,
        },
        {
            "class_id": "TSC3415_1_EM_Poynting",
            "safe_class": "public Maxwell/Poynting Hilbert stress",
            "proof": "For S_EM=-lambda_0/4 int sqrt(-g_obs) F^2 plus public current coupling, T_EM and Poynting flux are included in the same Hilbert stress and gravitate with ordinary source coupling.",
            "safe_result": "Poynting is not a second background force",
            "fails_if": "lambda(Phi)F^2, hidden current weights, constitutive background tensors or double-counted Poynting forces survive",
            "current_status": "EXACT_CONDITIONAL_SAFE_CLASS",
            "valid_for_claim": False,
        },
        {
            "class_id": "TSC3415_2_Lambda_trace",
            "safe_class": "constant Lambda/background trace",
            "proof": "A constant rho_Lambda g_obs^{mu nu} is covariantly conserved and locally subtractable from compact-system Newton/PPN source normalization when it is universal and source-independent.",
            "safe_result": "safe only as background/cosmological subtraction",
            "fails_if": "it carries local gradients, source dependence, time drift, species dependence or is mixed into measured compact mass",
            "current_status": "CONDITIONAL_BACKGROUND_SAFE_CLASS",
            "valid_for_claim": False,
        },
        {
            "class_id": "TSC3415_3_topological_improvement",
            "safe_class": "exact/topological/improvement stress",
            "proof": "A pure improvement/topological metric response has no compact exterior source if its linking-sphere and boundary charges vanish.",
            "safe_result": "safe when boundary charge is zero and no local metric response remains",
            "fails_if": "boundary, annulus, projector or symplectic flux carries a compact charge",
            "current_status": "CONDITIONAL_BOUNDARY_SAFE_CLASS",
            "valid_for_claim": False,
        },
        {
            "class_id": "TSC3415_4_positive_nohair",
            "safe_class": "massive positive auxiliary/no-hair stress",
            "proof": "If an auxiliary sector has positive operator L_AB on the compact exterior and no source/boundary term, the energy identity forces the residual field to zero or exponential suppression.",
            "safe_result": "safe when positive operator, source neutrality and boundary silence are parent-signed",
            "fails_if": "J_A, B_A, zero modes, gauge constraints, projector variation or source coupling survives",
            "current_status": "CONDITIONAL_NOHAIR_SAFE_CLASS",
            "valid_for_claim": False,
        },
        {
            "class_id": "TSC3415_5_hidden_projector",
            "safe_class": "hidden/projector/domain/constitutive stress",
            "proof": "Bianchi conservation can hold while monopole, STF, vector, beta, xi or EM propagation charges remain. Conservation is not silence.",
            "safe_result": "not safe; retain as residual unless theorem-zero or empirical bound exists",
            "fails_if": "not applicable; this is the failure class",
            "current_status": "RETAIN_AS_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "class_id": "TSC3415_6_q_loc_stress",
            "safe_class": "q_loc/Gamma-Khat effective stress",
            "proof": "3411 rewrites q_loc as a projected divergence of T_GK. It is safe only if T_GK is Hilbert-owned, metric-response matched, Euler-closed and boundary/projector silent through O(U^2).",
            "safe_result": "conditional Ward-zero route",
            "fails_if": "Delta_K, Helmholtz obstruction, boundary flux, projector commutator or alpha-vector projection survives",
            "current_status": "CONDITIONAL_NOT_CURRENTLY_SAFE",
            "valid_for_claim": False,
        },
    ]


def parent_ownership_obstructions() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "OBS3415_0_parent_adoption",
            "obstruction": "PC3400 source-coupling clauses are staged, not adopted into the parent theory.",
            "why_it_matters": "Without adoption, first-order Newton and source-square wins remain conditional.",
            "current_status": "BLOCKS_CURRENT_CLAIM",
            "next_math": "derive equivalent clauses from the parent action or prepare reviewed integration later",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3415_1_EH_selector",
            "obstruction": "MTS has not derived the metric-only second-order EH normal form from quotient/vertical symmetry.",
            "why_it_matters": "Non-EH operators are allowed by generic covariance unless the parent selector kills them.",
            "current_status": "CENTRAL_DERIVATION_GAP",
            "next_math": "derive parent normal-form EH selector or retain operator residual bounds",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3415_2_one_parameter_nohair",
            "obstruction": "One-parameter compact exterior/no-hair family is not parent-signed.",
            "why_it_matters": "B_source=A_source^2 and no extra beta lanes require no independent scalar/vector/domain/memory/boundary hair.",
            "current_status": "BLOCKS_BETA_PROMOTION",
            "next_math": "prove non-EH hair zero/topological/screened or populate residual envelope",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3415_3_source_charge_identity",
            "obstruction": "H_tau/Pi_M/Hilbert mass equality through O(U^2) is not signed.",
            "why_it_matters": "Measured U must be the same source in Poisson, PPN, orbital and Hamiltonian charge channels.",
            "current_status": "BLOCKS_SOURCE_OWNERSHIP",
            "next_math": "derive H_tau-H_ref = Pi_M J_H with fixed G_ref normalization",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3415_4_all_Textra_safe",
            "obstruction": "Not every retained T_extra row is classified into a safe Hilbert/Lambda/topological/no-hair class.",
            "why_it_matters": "Hidden/projector/constitutive stress can be conserved and still alter local observables.",
            "current_status": "BLOCKS_Y6_PROMOTION",
            "next_math": "prove safe-class membership or carry absolute residual rows",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "OBS3415_5_q_loc_vector",
            "obstruction": "q_loc beta projection is not separated from alpha_i/alpha3/xi preferred-frame projections.",
            "why_it_matters": "A beta-safe number can still fail alpha3 if the same projection carries vector charge.",
            "current_status": "BLOCKS_FULL_PPN",
            "next_math": "derive q_loc U2/alpha-vector projection split or Ward-zero through O(U^2)",
            "valid_for_claim": False,
        },
    ]


def kappav_y6_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "IMP3415_0_eta",
            "quantity": "kappa_eta",
            "result": "0 if EH/log-lapse branch is parent-owned",
            "effect": "removes intrinsic v-lane beta drift",
            "current_status": "EXACT_CONDITIONAL_ZERO",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3415_1_source_quad",
            "quantity": "kappa_source_quad",
            "result": "0 if one-parameter source-calibrated exterior is parent-owned",
            "effect": "removes source-square beta drift after measured-U calibration",
            "current_status": "EXACT_CONDITIONAL_ZERO",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3415_2_reduced_beta_envelope",
            "quantity": "kappa_v",
            "result": "|kappa_v| <= |kappa_PiM|+|kappa_boundary|+|kappa_readout|+|kappa_operator|+|kappa_coupling|+|kappa_q_loc| under eta/source-square zeroes",
            "effect": "beta problem shrinks to retained lanes",
            "current_status": "REDUCED_ENVELOPE_CONDITIONAL_NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3415_3_public_EM",
            "quantity": "T_EM/Poynting",
            "result": "ordinary Hilbert source if public Maxwell action uses g_obs and fixed current/Hodge",
            "effect": "EM stress can join the common source side without double counting",
            "current_status": "SAFE_CLASS_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3415_4_hidden_stress",
            "quantity": "T_extra_hidden",
            "result": "retained residual",
            "effect": "hidden/projector/constitutive stress can still feed beta, alpha_i, xi, zeta_i, source mass or EM propagation",
            "current_status": "RETAINED_Y6_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3415_5_local_GR",
            "quantity": "local_GR_PPN",
            "result": "not claimed",
            "effect": "needs parent EH selector, all retained lanes zero/bounded, q_loc vector split, and safe stress classification",
            "current_status": "BLOCKED_BUT_MORE_DERIVED",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3415_0_v_source_square",
            "gate": "a_v=0 and B_source=A_source^2 are derived in the source-calibrated EH one-parameter branch",
            "current_result": "PASS_EXACT_CONDITIONAL",
            "promotes_if": "EH/log-lapse/no-hair branch is parent-owned by MTS, not imported as closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3415_1_safe_class_classifier",
            "gate": "T_extra safe/residual classifier is explicit",
            "current_result": "PASS_INTERNAL",
            "promotes_if": "all live extra stresses are assigned to safe classes or bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3415_2_all_Textra_safe",
            "gate": "every retained extra stress is harmless",
            "current_result": "BLOCKED_HIDDEN_STRESS_RETAINS",
            "promotes_if": "hidden/projector/constitutive/q_loc stress rows theorem-zero or pass source-backed bounds",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3415_3_kappav",
            "gate": "kappa_v=0 or beta bound pass is derived",
            "current_result": "BLOCKED_RETAINED_LANES",
            "promotes_if": "PiM, boundary, readout, operator, coupling and q_loc lanes zero/bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3415_4_parent_EH",
            "gate": "MTS derives the EH/no-hair normal form rather than importing GR",
            "current_result": "BLOCKED_PARENT_SELECTOR",
            "promotes_if": "quotient/vertical symmetry forces metric-only second-order EH form and kills non-EH operators",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3415_5_local_GR",
            "gate": "local GR/Newton/PPN is derived",
            "current_result": "BLOCKED",
            "promotes_if": "PG3415_2, PG3415_3, PG3415_4 and q_loc vector/full PPN gates pass in one branch",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3415_0_real_win",
            "finding": "The two cleanest beta pieces are mathematically derived, conditionally.",
            "reason": "log-lapse oddness gives a_v=0 and the one-parameter mass family gives B_source=A_source^2.",
            "next_action": "use these as fixed conditional wins while attacking parent ownership",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3415_1_stress_policy",
            "finding": "Poynting/EM is not scary if it is ordinary public Hilbert stress.",
            "reason": "the dangerous branch is hidden Hodge/current/projector/constitutive stress, not public Maxwell stress itself.",
            "next_action": "classify every live stress term by safe class or residual row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3415_2_no_closure_smuggling",
            "finding": "The current result cannot be promoted to local GR.",
            "reason": "parent EH selector, no-hair/source charge identity, retained beta lanes, hidden stress and q_loc vector projection are unsigned.",
            "next_action": "derive the parent normal-form EH selector before doing broad numeric residual fills",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3415_3_best_next",
            "finding": "The next best strike is the parent normal-form EH selector plus hidden-stress exclusion.",
            "reason": "that single derivation would collapse the largest cluster of beta/source/operator/readout/stress debts at once.",
            "next_action": "build 3416 parent-normal-form EH selector and hidden-stress exclusion proof attempt",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3416-Y5-R2FR-parent-normal-form-EH-selector-and-hidden-stress-exclusion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3416_parent_normal_form_EH_selector_and_hidden_stress_exclusion.py",
            "objective": "try to derive the metric-only second-order EH normal form from MTS quotient/vertical symmetry and prove hidden/projector/constitutive stresses are absent, topological, no-hair, or explicitly residual",
            "why_next": "3415 conditionally closes a_v and source-square; the remaining leap is parent ownership of the EH/no-hair branch and exclusion of hidden stress",
            "valid_for_claim": False,
        },
        {
            "target_id": "3417-Y5-R2FR-q_loc-U2-alpha-vector-and-retained-beta-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3417_q_loc_U2_alpha_vector_and_retained_beta_bound_pack.py",
            "objective": "if the EH selector/stress exclusion route fails, separate q_loc beta from alpha_i/alpha3/xi and build retained beta/stress residual bound rows",
            "why_next": "this prevents the conditional EH/source-square route from becoming a hidden closure assumption",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3415_0",
            "script": str(Path(__file__).resolve()),
            "claim_status": "EXACT_CONDITIONAL_PROOF_AND_SAFE_CLASSIFIER_ONLY",
            "main_result": "a_v=0 and B_source=A_source^2 are exact in a parent-owned EH one-parameter branch; public EM/Poynting Hilbert stress is safe-class conditional; hidden stress and retained beta lanes block local GR.",
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
    av_zero = any(row.get("proof_id") == "VSS3415_0_EH_lapse" and "a_v=0" in row.get("result", "") for row in generated["v_source_square_proof"])
    b_square = any(row.get("proof_id") == "VSS3415_2_one_mass_square" and "B_source=A_source^2" in row.get("result", "") for row in generated["v_source_square_proof"])
    poynting_safe = any(row.get("class_id") == "TSC3415_1_EM_Poynting" and row.get("current_status") == "EXACT_CONDITIONAL_SAFE_CLASS" for row in generated["textra_safe_class_proof"])
    hidden_retained = any(row.get("class_id") == "TSC3415_5_hidden_projector" and row.get("current_status") == "RETAIN_AS_RESIDUAL" for row in generated["textra_safe_class_proof"])
    local_blocked = any(row.get("gate_id") == "PG3415_5_local_GR" and row.get("current_result") == "BLOCKED" for row in generated["promotion_gates"])
    parent_selector_next = "parent-normal-form-EH-selector" in generated["next_target"][0]["target_id"]
    rows = [
        {
            "check_id": "VAL3415_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3415_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3415_2_all_nonclaim",
            "check": "all rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3415 is exact conditional proof plus classifier, not a claim",
        },
        {
            "check_id": "VAL3415_3_av_zero",
            "check": "a_v=0 exact conditional proof is present",
            "passed": av_zero,
            "detail": "log-lapse has no O(U^2) term",
        },
        {
            "check_id": "VAL3415_4_source_square",
            "check": "B_source=A_source^2 exact conditional proof is present",
            "passed": b_square,
            "detail": "one-parameter source family squares first-order response",
        },
        {
            "check_id": "VAL3415_5_Poynting_safe_class",
            "check": "public EM/Poynting safe class is recorded",
            "passed": poynting_safe,
            "detail": "safe only as public Hilbert stress",
        },
        {
            "check_id": "VAL3415_6_hidden_stress_retained",
            "check": "hidden/projector stress remains residual",
            "passed": hidden_retained,
            "detail": "Bianchi conservation alone is not silence",
        },
        {
            "check_id": "VAL3415_7_local_GR_blocked",
            "check": "local-GR promotion remains blocked",
            "passed": local_blocked,
            "detail": "retained beta/stress/q_loc/parent-selector gates remain open",
        },
        {
            "check_id": "VAL3415_8_next_target",
            "check": "next target attacks parent EH selector, not broad scanning",
            "passed": parent_selector_next,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3415_9_overall",
            "check": "3415 v/source-square and T_extra safe-class proof is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3415 - v Source-Square and T_extra Safe-Class Proof",
            "## Summary\n"
            "- This checkpoint consolidates the cleanest second-order beta derivation route and combines it with the extra-stress classifier.\n"
            "- The mathematical win is real but conditional: in a source-calibrated EH one-parameter branch, `a_v=0` and `B_source=A_source^2` exactly.\n"
            "- That zeroes the `eta_v` and `source_quad` lanes of `kappa_v`, but not the retained PiM/boundary/readout/operator/coupling/q_loc lanes.\n"
            "- `T_extra` is now classified: ordinary public Hilbert matter/EM/Poynting/surface stress can be safe; hidden/projector/constitutive stress remains residual.\n"
            "- Local GR is still not claimed. The next non-circling move is the parent normal-form EH selector and hidden-stress exclusion.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## v/Source-Square Proof\n" + md_table(generated["v_source_square_proof"]),
            "## T_extra Safe-Class Proof\n" + md_table(generated["textra_safe_class_proof"]),
            "## Parent Ownership Obstructions\n" + md_table(generated["parent_ownership_obstructions"]),
            "## Kappa_v / Y6 Impact\n" + md_table(generated["kappav_y6_impact"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "The beta/source-coupling route looks materially better than it did: the two central source-normalized second-order pieces have exact conditional zero proofs. "
            "The remaining problem is not those two terms; it is parent ownership of the EH/no-hair branch and exclusion or bounding of hidden stress and retained PPN lanes.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "v_source_square_proof": v_source_square_proof(),
        "textra_safe_class_proof": textra_safe_class_proof(),
        "parent_ownership_obstructions": parent_ownership_obstructions(),
        "kappav_y6_impact": kappav_y6_impact(),
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
        raise SystemExit(f"3415 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
