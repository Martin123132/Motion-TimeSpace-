from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3434-Y5-R2FR-source-normalized-Poisson-limit-and-first-PPN-residual-stack-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3433": ROOT / "3433-Y5-R2FR-MHref-tau-source-normalization-lock-or-residual-vector-under-AX1090.md",
    "source_lock_3433": OUT / "P8_Y5_R2FR_3433_MHREF_TAU_SOURCE_LOCK_THEOREM.csv",
    "epsilon_mu_3433": OUT / "P8_Y5_R2FR_3433_EPSILON_MU_RESIDUAL_VECTOR.csv",
    "newton_ppn_3433": OUT / "P8_Y5_R2FR_3433_NEWTON_PPN_READOUT_GATES.csv",
    "next_3433": OUT / "P8_Y5_R2FR_3433_NEXT_TARGET.csv",
    "source_stack": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
    "source_residual_template": OUT / "P8_source_normalization_residual_vector_TEMPLATE.csv",
    "constant_gm_runner": OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
    "local_gr_domain_vector": OUT / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
    "mu_extra_scorecard": OUT / "P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv",
    "mu_extra_summary": OUT / "P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv",
    "qloc_operator_3432": OUT / "P8_Y5_R2FR_3432_QLOC_PPN_R10_OPERATOR_UPDATE.csv",
    "qloc_bound_3432": OUT / "P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv",
    "domain_ppn_3431": OUT / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_PPN_COEFFICIENT_UPDATE.csv",
    "hidden_bound_3430": OUT / "P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv",
    "worldtube_510": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "source_measure_509": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "symbol_map_512": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
    "fixed_point_511": OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
    "constant_kappa_decision": OUT / "P8_CONSTANT_KAPPA_DECISION.csv",
    "mhref_candidates_3425": OUT / "P8_Y5_R2FR_3425_MHREF_CANDIDATE_ROWS.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3434_SOURCE_REGISTER.csv",
    "poisson_limit_theorem": OUT / "P8_Y5_R2FR_3434_SOURCE_NORMALIZED_POISSON_LIMIT_THEOREM.csv",
    "kepler_readout_theorem": OUT / "P8_Y5_R2FR_3434_KEPLER_READOUT_THEOREM.csv",
    "first_ppn_residual_stack": OUT / "P8_Y5_R2FR_3434_FIRST_PPN_RESIDUAL_STACK.csv",
    "residual_visibility_matrix": OUT / "P8_Y5_R2FR_3434_RESIDUAL_VISIBILITY_MATRIX.csv",
    "score_readiness_gate": OUT / "P8_Y5_R2FR_3434_SCORE_READINESS_GATE.csv",
    "pc3400_update": OUT / "P8_Y5_R2FR_3434_PC3400_NEWTON_PPN_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3434_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3434_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3434_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3434_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3434_VALIDATION.csv",
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
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3433": "M_H_ref/tau source-normalization handoff",
        "source_lock_3433": "source-lock theorem",
        "epsilon_mu_3433": "epsilon_mu residual vector",
        "newton_ppn_3433": "Newton/PPN gate split",
        "next_3433": "3434 target declaration",
        "source_stack": "source-normalized Newton branch stack",
        "source_residual_template": "source-normalization residual vector template",
        "constant_gm_runner": "constant GM residual runner input",
        "local_gr_domain_vector": "local GR residual vector rows",
        "mu_extra_scorecard": "mu_extra local bound scorecard",
        "mu_extra_summary": "mu_extra channel bound summary",
        "qloc_operator_3432": "q_loc PPN/R10 operator rows",
        "qloc_bound_3432": "q_loc residual bound pack",
        "domain_ppn_3431": "domain projector PPN coefficient rows",
        "hidden_bound_3430": "hidden/projector bound rows",
        "worldtube_510": "worldtube source-measure theorem",
        "source_measure_509": "source-measure flux theorem",
        "symbol_map_512": "local GR action symbol map",
        "fixed_point_511": "local GR fixed-point conditions",
        "constant_kappa_decision": "constant kappa route decision",
        "mhref_candidates_3425": "M_H_ref candidate/source row schema",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def poisson_limit_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PL3434_0_field_equation",
            "statement": "In the public EH/Hilbert branch, the weak static 00 equation has the standard Poisson coefficient.",
            "formula": "g_00=-1+2 Phi/c^2, T_00=rho_H c^2, kappa_eff=8 pi G0/c^4 => nabla^2 Phi=4 pi G0 rho_H",
            "status": "CONDITIONAL_EH_DERIVATION",
            "condition_or_missing": "EH-only exterior, same observed frame, constant universal kappa/G0, and Hilbert source density",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PL3434_1_source_denominator",
            "statement": "The source density must integrate to the same tau-normalized Hamiltonian/Hilbert denominator.",
            "formula": "int_D rho_H d^3x = M_H_ref = c^-2(H_tau[S_outer]-H_ref)",
            "status": "CONDITIONAL_SOURCE_NORMALIZATION",
            "condition_or_missing": "source-specific M_H_ref row with tau/surface/reference/units/source path is missing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PL3434_2_residual_poisson",
            "statement": "If source-normalization residuals survive, Poisson's equation carries explicit residual source terms.",
            "formula": "nabla^2 Phi=4 pi G0 rho_H + S_epsilon_mu + S_q_loc + S_domain + S_boundary + S_nonEH",
            "status": "RESIDUAL_SOURCE_FORM",
            "condition_or_missing": "residual profiles and Green/source maps are missing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PL3434_3_gauss_surface",
            "statement": "The Gauss monopole equals the same M_H_ref only if residual volume and boundary terms vanish or are bounded.",
            "formula": "oint_S grad Phi.dS = 4 pi G0 M_H_ref + int_D S_res d^3x + oint_boundary R_boundary",
            "status": "CONDITIONAL_GAUSS_LOCK",
            "condition_or_missing": "PiM/source closure, boundary silence, radial/range residuals not closed",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PL3434_4_newtonian_potential",
            "statement": "Outside a compact source, the inverse-square potential follows only after the residual monopole and finite-range pieces vanish.",
            "formula": "Phi(r)=-G0 M_H_ref/r + deltaPhi_res(r); deltaPhi_res=0 required for pure Newton",
            "status": "CONDITIONAL_INVERSE_SQUARE",
            "condition_or_missing": "range/radial/q_loc/domain/boundary maps are not zero or score-ready",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PL3434_5_scope_limit",
            "statement": "First-order Newton/Poisson success is not local GR; beta/gamma/preferred-frame rows remain separate obligations.",
            "formula": "Poisson pass does not imply gamma-1=0, beta-1=0, alpha_i=0, xi=0",
            "status": "NO_OVERCLAIM_RULE",
            "condition_or_missing": "second-order PPN source/operator stack still open",
            "valid_for_claim": False,
        },
    ]


def kepler_readout_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "KR3434_0_slow_body",
            "statement": "A slow test body reads the same potential only if its matter action uses the same observed metric/coframe.",
            "formula": "S_test=-m int ds[g_obs] => d^2 x^i/dt^2=-partial_i Phi + O(v^2/c^2)",
            "status": "CONDITIONAL_GEODESIC_READOUT",
            "condition_or_missing": "same observed frame/source variation theorem remains unsigned",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KR3434_1_kepler",
            "statement": "Kepler/Newton GM follows when the Gauss monopole and orbital readout use the same M_H_ref.",
            "formula": "a_r=-G0 M_H_ref/r^2; v^2 r=G0 M_H_ref",
            "status": "CONDITIONAL_KEPLER_LOCK",
            "condition_or_missing": "same M_H_ref/tau, no frame split, no range/radial hair",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KR3434_2_residual_acceleration",
            "statement": "Any source-normalization or finite-range residual becomes an orbital acceleration correction, not a hidden GM shift.",
            "formula": "a_r=-G0 M_H_ref/r^2 - partial_r deltaPhi_res(r) + a_frame + a_q_loc",
            "status": "RESIDUAL_KEPLER_FORM",
            "condition_or_missing": "residual profiles, test-body coupling, and frame map missing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KR3434_3_calibration_split",
            "statement": "A constant universal offset in GM can be calibrated away, but radial/range/species/time/frame derivatives cannot.",
            "formula": "GM_obs=G0 M_H_ref(1+epsilon0) is harmless only if D_i epsilon0=0 for all local/source/range/frame directions",
            "status": "NO_CALIBRATION_CHEAT_APPLIED",
            "condition_or_missing": "derivative-zero identities or residual values missing",
            "valid_for_claim": False,
        },
    ]


def first_ppn_residual_stack() -> list[dict[str, Any]]:
    return [
        {
            "ppn_id": "PPRS3434_0_gamma",
            "observable": "gamma_minus_1",
            "source_formula": "gamma_minus_1 = R_gamma[c_nonEH_operator_vector, epsilon_mu, epsilon_q_loc, epsilon_boundary, epsilon_range]",
            "target": "2.3e-5 dimensionless or derived zero",
            "current_status": "BLOCKED_MAP_VALUES_MISSING",
            "blocks_Newton": False,
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_1_beta",
            "observable": "beta_minus_1",
            "source_formula": "beta_minus_1 = R_beta[delta_beta_source, epsilon_radial_Meff, epsilon_boundary, epsilon_nonEH, epsilon_q_loc]",
            "target": "7.8e-5 dimensionless or derived zero",
            "current_status": "BLOCKED_SECOND_ORDER_SOURCE_STACK",
            "blocks_Newton": False,
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_2_alpha1",
            "observable": "alpha1",
            "source_formula": "alpha1 = W_domain_alpha1 epsilon_domain_vector + R_alpha1[q_loc/frame/vector]",
            "target": "1e-4 dimensionless or derived zero",
            "current_status": "BLOCKED_DOMAIN_FRAME_VALUES_MISSING",
            "blocks_Newton": False,
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_3_alpha2",
            "observable": "alpha2",
            "source_formula": "alpha2 = W_domain_alpha2 epsilon_domain_vector + R_alpha2[q_loc/frame/vector]",
            "target": "2e-9 dimensionless or derived zero",
            "current_status": "BLOCKED_DOMAIN_FRAME_VALUES_MISSING",
            "blocks_Newton": False,
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_4_alpha3",
            "observable": "alpha3",
            "source_formula": "alpha3 = W_domain_alpha3 epsilon_domain_flux + W_boundary_alpha3 epsilon_boundary_flux + R_alpha3[q_loc]",
            "target": "4e-20 dimensionless or derived zero",
            "current_status": "BLOCKED_TIGHT_FLUX_ROW",
            "blocks_Newton": "indirect_source_normalization",
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_5_xi",
            "observable": "xi",
            "source_formula": "xi = W_domain_xi epsilon_domain_anisotropy + R_xi[boundary/projector/STF]",
            "target": "4e-9 dimensionless or derived zero",
            "current_status": "BLOCKED_PROJECTOR_STF_ROW",
            "blocks_Newton": False,
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_6_zeta_conservation",
            "observable": "zeta_i / conservation rows",
            "source_formula": "zeta_i = R_zeta[source nonconservation, q_loc exchange, boundary flux, frame split]",
            "target": "derived conservation or explicit row bounds",
            "current_status": "BLOCKED_SOURCE_CONSERVATION_MAP",
            "blocks_Newton": "if source flux changes M_H_ref",
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_7_R10_range",
            "observable": "alpha(lambda)",
            "source_formula": "alpha(lambda)=R_R10[epsilon_range, q_loc Yukawa source, nonEH operator, bulk_X]",
            "target": "real alpha_bound(lambda) curve or derived zero",
            "current_status": "BLOCKED_CURVE_AND_SOURCE_MAP_MISSING",
            "blocks_Newton": "if finite-range force survives",
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPRS3434_8_Gdot",
            "observable": "Gdot_over_G",
            "source_formula": "dln mu_obs/dt = dln G_eff/dt + dln M_H_ref/dt + d epsilon_mu/dt",
            "target": "9.6e-15 yr^-1 or derived zero",
            "current_status": "BLOCKED_TIME_DERIVATIVE_VALUES_MISSING",
            "blocks_Newton": "time-dependent GM",
            "blocks_local_GR": True,
            "valid_for_claim": False,
        },
    ]


def residual_visibility_matrix() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RVM3434_0_epsilon_mu",
            "residual": "epsilon_mu_residual_vector",
            "enters_poisson": "S_epsilon_mu",
            "enters_kepler": "delta GM_obs and derivative hair",
            "enters_ppn": "beta/gamma/source-normalization rows",
            "current_action": "derive zero or fill vector values",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVM3434_1_q_loc",
            "residual": "epsilon_q_loc_TGK_mass",
            "enters_poisson": "effective source-exchange term",
            "enters_kepler": "a_q_loc or finite-range tail",
            "enters_ppn": "inverse-divergence PPN operator and R10 Yukawa row",
            "current_action": "needs I_div/source map or Hilbert-owner zero",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVM3434_2_domain",
            "residual": "epsilon_domain_projector_abs",
            "enters_poisson": "domain source-normalization term",
            "enters_kepler": "frame/domain calibration split",
            "enters_ppn": "alpha1/alpha2/alpha3/xi and R11 rows",
            "current_action": "operator-bound values or fixed-topological zero",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVM3434_3_boundary",
            "residual": "epsilon_boundary_symplectic_abs",
            "enters_poisson": "surface/source charge shift",
            "enters_kepler": "boundary monopole/collar acceleration",
            "enters_ppn": "alpha3, xi, Gdot, beta rows",
            "current_action": "boundary flux zero or coefficient values",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVM3434_4_nonEH_operator",
            "residual": "c_nonEH_operator_vector",
            "enters_poisson": "modified weak-field operator",
            "enters_kepler": "non-inverse-square or changed coefficient",
            "enters_ppn": "gamma/beta/R10/R11",
            "current_action": "derive EH-only exterior or executable operator vector",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RVM3434_5_frame_species_range",
            "residual": "delta_frame_source + eta_source_AB + alpha(lambda)",
            "enters_poisson": "source density/readout mismatch",
            "enters_kepler": "composition/range/frame-dependent acceleration",
            "enters_ppn": "WEP, clocks, preferred-frame, R10",
            "current_action": "same-frame/source universality theorem or data-ready residual rows",
            "valid_for_claim": False,
        },
    ]


def score_readiness_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SRG3434_0_poisson_derivation",
            "item": "EH Poisson coefficient",
            "status": "PASS_CONDITIONAL_EH_ONLY",
            "missing_for_claim": "source purity and same-frame M_H_ref row",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SRG3434_1_kepler_readout",
            "item": "Kepler/inverse-square readout",
            "status": "FORMULA_READY_BLOCKED",
            "missing_for_claim": "same observed frame, no radial/range hair, no q_loc acceleration",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SRG3434_2_ppn_stack",
            "item": "first PPN residual stack",
            "status": "STRUCTURED_NOT_SCORE_READY",
            "missing_for_claim": "operator maps and numeric/theorem-zero residual values",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SRG3434_3_r10",
            "item": "R10/fifth-force row",
            "status": "BLOCKED_CURVE_AND_SOURCE_MAP",
            "missing_for_claim": "real alpha(lambda) curve plus MTS alpha(lambda) source map",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SRG3434_4_no_overclaim",
            "item": "Newton vs local GR distinction",
            "status": "PASS_GUARD",
            "missing_for_claim": "PPN still blocked even if Poisson is conditionally derived",
            "valid_for_claim": False,
        },
    ]


def pc3400_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_id": "PC3400_Newton",
            "requirement": "source-normalized Newton/Poisson limit",
            "3434_result": "EH/Hilbert Poisson coefficient and Kepler formula derived conditionally",
            "signed_part": "Poisson coefficient in EH public branch",
            "open_part": "same M_H_ref/tau/source purity and residual-zero/value rows",
            "status": "CONDITIONAL_NOT_PROMOTED",
            "valid_for_claim": False,
        },
        {
            "pc_id": "PC3400_PPN",
            "requirement": "local GR/PPN through required order",
            "3434_result": "first PPN residual stack assembled",
            "signed_part": "no-overclaim guard and residual visibility",
            "open_part": "gamma/beta/preferred-frame/R10/Gdot rows not score-ready",
            "status": "BLOCKED_NOT_PROMOTED",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3434_0_poisson",
            "gate": "Poisson coefficient derived",
            "result": "PASS_CONDITIONAL_EH_ONLY",
            "evidence": "PL3434_0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3434_1_newton_claim",
            "gate": "Newtonian mechanics derived for current MTS",
            "result": "BLOCKED",
            "evidence": "same M_H_ref/tau, residual-zero/value rows and Kepler readout remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3434_2_ppn_stack",
            "gate": "first PPN residual stack exists",
            "result": "PASS_STRUCTURE_VALUES_MISSING",
            "evidence": "PPRS3434 rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3434_3_local_GR",
            "gate": "local GR is derived",
            "result": "BLOCKED",
            "evidence": "PPN, q_loc, source-normalization, range/radial and second-order rows remain open",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3434_4_empirical_ready",
            "gate": "residuals can be tested numerically",
            "result": "FAIL_VALUES_MISSING",
            "evidence": "no q_loc/domain/boundary/R10/operator numeric maps",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3434_0_real_progress",
            "decision": "Accept conditional EH Poisson derivation as real progress but not a current MTS claim.",
            "reason": "it nails the coefficient route while preserving residual honesty.",
            "next_action": "attack residual-zero/value rows instead of re-deriving Poisson",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3434_1_no_newton_overreach",
            "decision": "Do not call Newton recovered until Kepler readout and residual source purity are signed.",
            "reason": "a correct Poisson coefficient can still have extra source, range, frame or q_loc hair.",
            "next_action": "derive same-frame slow-body readout or fill acceleration residuals",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3434_2_next",
            "decision": "Next target should make one residual row score-ready rather than broaden the audit.",
            "reason": "the symbolic stack is now coherent; empirical robustness needs executable rows.",
            "next_action": "build first score-ready residual runner for source-normalization/R10 or derive one zero theorem",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3435-Y5-R2FR-first-score-ready-source-normalization-residual-runner-or-zero-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3435_first_score_ready_source_normalization_residual_runner_or_zero_row.py",
            "objective": "choose one high-leverage residual row and make it score-ready: either theorem-zero it or create executable numeric/source inputs, starting with radial/range source hair or q_loc-to-R10 map",
            "success_condition": "at least one residual row moves from FORMULA_READY_VALUES_MISSING to DERIVED_ZERO or SCORE_READY_NONCLAIM with real units and source path",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3434_0",
            "purpose": "prevent Poisson-to-GR overclaim",
            "rule": "Poisson coefficient does not promote Newton/PPN/local-GR unless source denominator, Kepler readout and residual rows close",
            "current_value": "claim_allowed=false",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3434_1",
            "purpose": "keep residuals visible",
            "rule": "epsilon_mu, q_loc, domain, boundary, nonEH, range and frame residuals must enter PPN/R10/source rows",
            "current_value": "residual_visibility_required=true",
            "valid_for_claim": False,
        },
    ]


def all_outputs_scoped() -> bool:
    root_resolved = ROOT.resolve()
    return all(root_resolved in path.resolve().parents or path.resolve() == root_resolved for path in [DOC, *OUTPUTS.values()])


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    poisson_rows = rows_by_name["poisson_limit_theorem"]
    kepler_rows = rows_by_name["kepler_readout_theorem"]
    ppn_rows = rows_by_name["first_ppn_residual_stack"]
    visibility_rows = rows_by_name["residual_visibility_matrix"]
    score_rows = rows_by_name["score_readiness_gate"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_ts = start_utc.timestamp()
        modified_count = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start_ts)
    validations = [
        {
            "check_id": "VAL3434_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3434_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all_outputs_scoped(),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3434_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3434_3_poisson_coefficient",
            "condition": "EH Poisson coefficient derivation is present",
            "passed": any(row["theorem_id"] == "PL3434_0_field_equation" for row in poisson_rows),
            "detail": "conditional EH Poisson row present",
        },
        {
            "check_id": "VAL3434_4_residual_poisson",
            "condition": "residual source terms are retained in Poisson equation",
            "passed": any(row["theorem_id"] == "PL3434_2_residual_poisson" for row in poisson_rows),
            "detail": "S_res terms visible",
        },
        {
            "check_id": "VAL3434_5_kepler_readout",
            "condition": "Kepler readout is conditional and residual-corrected",
            "passed": any(row["theorem_id"] == "KR3434_1_kepler" for row in kepler_rows)
            and any(row["theorem_id"] == "KR3434_2_residual_acceleration" for row in kepler_rows),
            "detail": "conditional Kepler and residual acceleration rows present",
        },
        {
            "check_id": "VAL3434_6_ppn_stack",
            "condition": "first PPN residual stack covers major rows",
            "passed": len(ppn_rows) >= 9 and any(row["ppn_id"] == "PPRS3434_7_R10_range" for row in ppn_rows),
            "detail": f"{len(ppn_rows)} PPN/residual rows",
        },
        {
            "check_id": "VAL3434_7_visibility_matrix",
            "condition": "major residuals are mapped to Poisson/Kepler/PPN visibility",
            "passed": len(visibility_rows) >= 6 and any(row["residual_id"] == "RVM3434_1_q_loc" for row in visibility_rows),
            "detail": f"{len(visibility_rows)} visibility rows",
        },
        {
            "check_id": "VAL3434_8_no_overclaim_gate",
            "condition": "Poisson-to-GR overclaim is explicitly blocked",
            "passed": any(row["gate_id"] == "SRG3434_4_no_overclaim" and row["status"] == "PASS_GUARD" for row in score_rows),
            "detail": "Newton/GR distinction guard present",
        },
        {
            "check_id": "VAL3434_9_local_GR_blocked",
            "condition": "local GR remains blocked until residual rows close",
            "passed": any(row["gate_id"] == "PG3434_3_local_GR" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3434_10_next_target",
            "condition": "next target makes one residual row score-ready or zero",
            "passed": next_rows[0]["target_doc"].startswith("3435-Y5-R2FR-first-score-ready"),
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3434_11_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3434_12_overall",
            "condition": "3434 Poisson/PPN checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3434 - Source-Normalized Poisson Limit and First PPN Residual Stack

## Summary
- This checkpoint derives the clean part: in the public EH/Hilbert branch, the weak static 00 equation gives the standard Poisson coefficient.
- It also draws the hard line: a correct Poisson coefficient is not yet Newtonian mechanics unless the same `M_H_ref`, `tau`, source frame, Gauss surface, and Kepler readout are locked.
- Every non-EH/source-normalization residual is carried forward explicitly: `epsilon_mu`, `q_loc`, domain/projector, boundary, non-EH operators, range/radial hair, species/frame split, and second-order PPN source residue.
- Result: conditional Newton stack is cleaner, but current MTS is still nonclaim until residual rows are theorem-zero or score-ready.
- The next useful move is no longer another broad audit; it is making one high-leverage residual row executable or derived-zero.

## Source Register
{md_table(rows_by_name["source_register"])}

## Source-Normalized Poisson Limit Theorem
{md_table(rows_by_name["poisson_limit_theorem"])}

## Kepler Readout Theorem
{md_table(rows_by_name["kepler_readout_theorem"])}

## First PPN Residual Stack
{md_table(rows_by_name["first_ppn_residual_stack"])}

## Residual Visibility Matrix
{md_table(rows_by_name["residual_visibility_matrix"])}

## Score Readiness Gate
{md_table(rows_by_name["score_readiness_gate"])}

## PC3400 Newton/PPN Update
{md_table(rows_by_name["pc3400_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is the clean boxing round: MTS can now say the EH/Hilbert branch has the right Poisson coefficient conditionally, but it cannot call the match won until source-normalization and PPN residuals are either zero or below bounds. No fitted `GM` carpet. No Poisson-to-GR overclaim.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "poisson_limit_theorem": poisson_limit_theorem(),
        "kepler_readout_theorem": kepler_readout_theorem(),
        "first_ppn_residual_stack": first_ppn_residual_stack(),
        "residual_visibility_matrix": residual_visibility_matrix(),
        "score_readiness_gate": score_readiness_gate(),
        "pc3400_update": pc3400_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3434 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
