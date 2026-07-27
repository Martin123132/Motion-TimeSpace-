from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4021"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4021-Y5-R2FR-parent-adoption-witness-or-first-PPN-score-input-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4021_SOURCE_REGISTER.csv",
    "witness": SRC / "P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv",
    "lemmas": SRC / "P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv",
    "score": SRC / "P8_Y5_R2FR_4021_WITNESS_PPN_SCORE_FILL.csv",
    "stress": SRC / "P8_Y5_R2FR_4021_WITNESS_STRESS_TEST_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4021_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4021_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4021_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4021_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4021_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4021_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4021_VALIDATION.csv",
}

NEXT_DOC = "4022-Y5-R2FR-parent-witness-stress-test-or-residual-coefficient-fill.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4022_parent_witness_stress_test_or_residual_coefficient_fill.py"


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
        ("SRC4021_00_handoff", SRC / "P8_Y5_R2FR_4020_NEXT_TARGET.csv", "NEXT4020_0", "4020 handoff"),
        ("SRC4021_01_rollup", SRC / "P8_Y5_R2FR_4020_LOCAL_GR_ROLLUP_CHAIN.csv", "ROLL4020_5_conditional_local_GR_vector", "4020 local-GR rollup"),
        ("SRC4021_02_audit_KG", SRC / "P8_Y5_R2FR_4020_ADOPTION_EVIDENCE_AUDIT.csv", "AUD4020_0_parent_action_KG", "K_G adoption blocker"),
        ("SRC4021_03_audit_EH", SRC / "P8_Y5_R2FR_4020_ADOPTION_EVIDENCE_AUDIT.csv", "AUD4020_1_parent_action_EH_only", "EH-only adoption blocker"),
        ("SRC4021_04_score_gamma", SRC / "P8_Y5_R2FR_4020_FIRST_EXECUTABLE_PPN_SCORE_ROWS.csv", "FES4020_0_delta_gamma_R11", "gamma score row"),
        ("SRC4021_05_score_beta_source", SRC / "P8_Y5_R2FR_4020_FIRST_EXECUTABLE_PPN_SCORE_ROWS.csv", "FES4020_1_delta_beta_source", "beta source score row"),
        ("SRC4021_06_4012_charge", SRC / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv", "CHG4012_0_parent_constraint_map", "Pi_M/H_tau construction"),
        ("SRC4021_07_4013_em", SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv", "MPE4013_1_Maxwell_Hilbert_stress", "EM stress once-only"),
        ("SRC4021_08_4014_hodge", SRC / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv", "OHN4014_0_observed_Hodge_lock", "observed Hodge owner"),
        ("SRC4021_09_4015_newton", SRC / "P8_Y5_R2FR_4015_GAUSS_POISSON_GREF_NEWTON_THEOREM.csv", "GPN4015_1_EH00_to_Poisson", "Poisson bridge"),
        ("SRC4021_10_4016_KG", SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "GSS4016_0_global_sector_factorization", "G_ref superselection"),
        ("SRC4021_11_4017_packet", SRC / "P8_Y5_R2FR_4017_KAPPA_SECTOR_INSERTION_PACKET.csv", "KSP4017_1_action", "kappa parent packet"),
        ("SRC4021_12_4017_nohom", SRC / "P8_Y5_R2FR_4017_KAPPA_VARIATION_AND_NOHOM_THEOREM.csv", "KVT4017_0_local_variation_zero", "no local kappa variation"),
        ("SRC4021_13_4018_gamma", SRC / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv", "PPN4018_1_gamma_EH_zero", "gamma theorem"),
        ("SRC4021_14_4018_beta", SRC / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv", "PPN4018_3_beta_EH_zero", "beta theorem"),
        ("SRC4021_15_4019_adoption", SRC / "P8_Y5_R2FR_4019_EH_ONLY_R11_ADOPTION_CLAUSES.csv", "EHA4019_1_R11_absent", "R11 adoption clause"),
        ("SRC4021_16_4019_theorem", SRC / "P8_Y5_R2FR_4019_NO_EXTRA_OPERATOR_THEOREM.csv", "NOX4019_0_operator_domain_theorem", "no-extra theorem"),
        ("SRC4021_17_4019_scorer", SRC / "P8_Y5_R2FR_4019_PPN_RESIDUAL_SCORER_ROWS.csv", "PPS4019_0_master", "PPN scorer"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def witness_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "witness_id": "WIT4021_0_configuration",
            "clause": "local parent configuration",
            "mathematical_form": "Q_parent^loc = Q_dyn^loc x K_G x Q_aux, q:Q_dyn^loc->Met_obs, V=ker(Dq), kappa_* in K_G, T_local K_G=0",
            "signs_block": "global coupling sector and vertical/observed split",
            "derivation_status": "candidate_witness_clause",
            "corpus_adopted": False,
            "witness_closes": True,
            "fallback_if_rejected": "Gdot/range/material-coupling scorer rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "witness_id": "WIT4021_1_action",
            "clause": "2PN local action witness",
            "mathematical_form": "S_loc^{<=2PN}=S_MTS^vert[Phi]+(1/(2*kappa_*)) int R[g_obs(q(Phi))] eps_obs + S_matter[psi,g_obs,theta] + S_EM[A,g_obs,mu0,J] + S_binding + dB + S_top + S_aux^double-zero",
            "signs_block": "EH-only local metric operator, same-source matter/EM slot",
            "derivation_status": "candidate_witness_clause",
            "corpus_adopted": False,
            "witness_closes": True,
            "fallback_if_rejected": "delta_gamma_R11, delta_beta_R11, delta_beta_source scorer rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "witness_id": "WIT4021_2_no_extra_operators",
            "clause": "non-EH operator exclusion",
            "mathematical_form": "O_nonEH^{<=2PN} in {exact, topological, vertical-only with Dq=0, auxiliary double-zero}; exclude f(Phi)R, R^2, R_abR^ab, vector-aether, disformal matter, source-prefactor terms unless scored",
            "signs_block": "R11/q_loc no-extra gate",
            "derivation_status": "sufficient_condition_not_corpus_fact",
            "corpus_adopted": False,
            "witness_closes": True,
            "fallback_if_rejected": "compute Pi_gamma/Pi_beta projections of surviving operators",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "witness_id": "WIT4021_3_source_current",
            "clause": "same Hilbert source current",
            "mathematical_form": "T_total^{ab}=(-2/sqrt|g_obs|) delta(S_matter+S_EM+S_binding)/delta g_obs_ab; J_H[tau]=-T_total^a_b tau^b eps_a; Pi_M^C J_H defines M_H_ref before orbital GM readout",
            "signs_block": "source charge, EM once-only, Newton bridge source normalization",
            "derivation_status": "candidate_witness_clause_plus_existing_chainmap_condition",
            "corpus_adopted": False,
            "witness_closes": True,
            "fallback_if_rejected": "C_PiM_H, delta_readout_frame, epsilon_EM_once scorer rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "witness_id": "WIT4021_4_observed_Hodge",
            "clause": "Maxwell owner",
            "mathematical_form": "S_EM=-(1/(4*mu0)) int F wedge *_obs F + int A wedge J with *_obs=*[g_obs(q(Phi)),orientation]",
            "signs_block": "observed Hodge, Poynting/current, EM stress once-only",
            "derivation_status": "candidate_witness_clause",
            "corpus_adopted": False,
            "witness_closes": True,
            "fallback_if_rejected": "Delta_Hodge_EM constitutive residual split",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "witness_id": "WIT4021_5_q_loc_kernel",
            "clause": "vertical q_loc/projector silence",
            "mathematical_form": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu Khat^{mu nu}) lies in im(V^*) plus exact/boundary-silent terms; Pi_PPN o q_loc = 0 for Pi in {Pi_gamma,Pi_beta,Pi_alpha,Pi_xi,Pi_zeta}",
            "signs_block": "q_loc PPN kernel and finite-range local tail",
            "derivation_status": "sufficient_kernel_clause_not_yet_corpus_fact",
            "corpus_adopted": False,
            "witness_closes": True,
            "fallback_if_rejected": "delta_beta_q_loc and alpha_lambda scorer rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "witness_id": "WIT4021_6_readout_boundary",
            "clause": "same observed readout and boundary silence",
            "mathematical_form": "U,gamma,beta,source charge and clocks are read from the same g_obs/e_obs; dB and exact terms have compact-support or matched-boundary zero flux on the PPN exterior annulus",
            "signs_block": "frame/readout/boundary residuals",
            "derivation_status": "candidate_witness_clause",
            "corpus_adopted": False,
            "witness_closes": True,
            "fallback_if_rejected": "delta_readout_frame and boundary-domain scorer rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "witness_id": "WIT4021_7_claim_guard",
            "clause": "nonclaim guard",
            "mathematical_form": "The witness is a sufficient local parent contract; it becomes a claim only after the actual MTS parent corpus adopts it or every rejected clause is numerically scored",
            "signs_block": "anti-smuggling guard",
            "derivation_status": "guard",
            "corpus_adopted": False,
            "witness_closes": False,
            "fallback_if_rejected": "keep private/nonclaim and score residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def lemma_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "LEM4021_0_KG_local_variation",
            "statement": "If Q_parent^loc factors as Q_dyn^loc x K_G and local variations have no K_G component, then delta_local kappa_*=0 and D_X ln G_ref=0 for local source/range/frame labels with no Hom into K_G.",
            "proof_skeleton": "For v in TQ_dyn x {0}, v(kappa_*)=0 by projection. Since G_ref=c^4*kappa_*/(8*pi), every admitted local derivative of ln G_ref vanishes.",
            "zeroed_score_terms": "Gdot/G, C_local_scalar, C_noHom",
            "requires_witness_ids": "WIT4021_0_configuration",
            "valid_under_witness": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "LEM4021_1_EH_operator_zero",
            "statement": "If all <=2PN metric-dependent local operators are EH, matter/EM, exact, topological, vertical-only, or auxiliary double-zero, then DeltaE_R11^(1)=DeltaE_R11^(2)=0 in observed metric equations.",
            "proof_skeleton": "Exact/topological terms vary to boundary/topological identities; vertical-only terms have Dq=0 and no g_obs variation; auxiliary double-zero terms vanish after eliminating auxiliary fields; only EH contributes to the metric Euler equation through O(U^2).",
            "zeroed_score_terms": "delta_gamma_R11, delta_beta_R11",
            "requires_witness_ids": "WIT4021_1_action; WIT4021_2_no_extra_operators; WIT4021_6_readout_boundary",
            "valid_under_witness": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "LEM4021_2_source_once_conservation",
            "statement": "If matter, Maxwell, binding and ordinary stresses are varied once against the same g_obs, the total Hilbert source is single-counted and covariantly conserved in the adopted branch.",
            "proof_skeleton": "Define T_total by one metric variation of S_matter+S_EM+S_binding. Diffeomorphism invariance with matter equations gives nabla_mu T_total^{mu nu}=0; no separate EM mass channel remains.",
            "zeroed_score_terms": "epsilon_EM_once, zeta_i, source double-count residuals",
            "requires_witness_ids": "WIT4021_3_source_current; WIT4021_4_observed_Hodge",
            "valid_under_witness": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "LEM4021_3_Newton_Poisson_readout",
            "statement": "With EH operator, nonrelativistic T_00^H and kappa_ref=8*pi*G_ref/c^4, the 00 equation gives nabla^2 Phi=4*pi*G_ref rho_H and the exterior readout gives Phi=-G_ref M_H_ref/r.",
            "proof_skeleton": "Use G_00^(1)=2 nabla^2 Phi/c^2 and T_00^H=rho_H c^2; Gauss readout on the same exterior annulus gives the Newtonian charge. G_ref is calibrated, not numerically predicted.",
            "zeroed_score_terms": "Delta_EH00, C_Gref_kappa under witness; no numerical-G claim",
            "requires_witness_ids": "WIT4021_0_configuration; WIT4021_1_action; WIT4021_3_source_current",
            "valid_under_witness": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "LEM4021_4_beta_square_law",
            "statement": "If the same EH source branch that fixes A_source is used through second order, the beta source coefficient is not free: B_source=A_source^2, so delta_beta_source=0.",
            "proof_skeleton": "The nonlinear O(U^2) term comes from the same EH field equation and same potential normalization fixed at O(U); there is no independent source prefactor left to tune, so beta_eff=B_source/A_source^2=1.",
            "zeroed_score_terms": "delta_beta_source",
            "requires_witness_ids": "WIT4021_1_action; WIT4021_3_source_current; WIT4021_6_readout_boundary",
            "valid_under_witness": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "LEM4021_5_q_loc_vertical_kernel",
            "statement": "If q_loc/Khat is vertical with respect to q and boundary-silent, every PPN projector built from g_obs annihilates it.",
            "proof_skeleton": "PPN observables are functionals of g_obs, source current and readout. Their Gateaux derivative along V=ker(Dq) is zero; exact/boundary-silent pieces integrate to zero on the exterior annulus.",
            "zeroed_score_terms": "delta_beta_q_loc, alpha_lambda local tail",
            "requires_witness_ids": "WIT4021_5_q_loc_kernel; WIT4021_6_readout_boundary",
            "valid_under_witness": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "LEM4021_6_PPN_zero_vector_under_witness",
            "statement": "Under WIT4021_0..6, the local branch has the GR PPN vector gamma=beta=1, alpha_i=xi=zeta_i=0 and Gdot/G=0.",
            "proof_skeleton": "LEM4021_0 kills coupling drift; LEM4021_1 kills R11 metric stress; LEM4021_2 gives total conserved source; LEM4021_4 fixes beta; LEM4021_5 kills q_loc; same observed readout removes frame shifts.",
            "zeroed_score_terms": "Delta_PPN_abs_4021 under witness",
            "requires_witness_ids": "WIT4021_0_configuration..WIT4021_6_readout_boundary",
            "valid_under_witness": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def score_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "score_id": "WPS4021_0_delta_gamma_R11",
            "quantity": "delta_gamma_R11",
            "4020_input": "FES4020_0_delta_gamma_R11",
            "witness_value": "0",
            "witness_reason": "LEM4021_1_EH_operator_zero",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "compute Pi_gamma[DeltaE_R11^(1)] for each surviving local non-EH operator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "WPS4021_1_delta_beta_source",
            "quantity": "delta_beta_source",
            "4020_input": "FES4020_1_delta_beta_source",
            "witness_value": "0",
            "witness_reason": "LEM4021_4_beta_square_law",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "source A_source and B_source from the same parent-current expansion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "WPS4021_2_delta_beta_R11",
            "quantity": "delta_beta_R11",
            "4020_input": "FES4020_2_delta_beta_R11",
            "witness_value": "0",
            "witness_reason": "LEM4021_1_EH_operator_zero",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "compute Pi_beta[DeltaE_R11^(2)] for surviving non-EH operators",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "WPS4021_3_delta_beta_q_loc",
            "quantity": "delta_beta_q_loc",
            "4020_input": "FES4020_3_delta_beta_q_loc",
            "witness_value": "0",
            "witness_reason": "LEM4021_5_q_loc_vertical_kernel",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "derive q_loc amplitude/profile or source alpha_lambda bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "WPS4021_4_preferred_frame",
            "quantity": "alpha1, alpha2, alpha3, xi",
            "4020_input": "FES4020_4_preferred_frame",
            "witness_value": "0",
            "witness_reason": "same observed metric/readout and no preferred selector in WIT4021_0..6",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "project domain/coframe/memory selectors onto alpha_i and xi",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "WPS4021_5_conservation_zeta",
            "quantity": "zeta_i",
            "4020_input": "FES4020_5_conservation_zeta",
            "witness_value": "0",
            "witness_reason": "LEM4021_2_source_once_conservation",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "compute nonconservation residual from total source action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "WPS4021_6_Gdot",
            "quantity": "Gdot/G",
            "4020_input": "FES4020_6_Gdot",
            "witness_value": "0",
            "witness_reason": "LEM4021_0_KG_local_variation",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "source Gdot/range/material coupling bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "WPS4021_7_master",
            "quantity": "Delta_PPN_abs_4021",
            "4020_input": "FES4020_7_master_abs_sum",
            "witness_value": "0 under WIT4021_0..6; unscored otherwise",
            "witness_reason": "LEM4021_6_PPN_zero_vector_under_witness",
            "corpus_score_ready": False,
            "claim_ready": False,
            "fallback_if_witness_rejected": "run absolute-sum scorer with sourced coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def stress_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "stress_id": "STR4021_0_motion_time_space_terms",
            "question": "Can original MTS motion/time/space terms enter the local 2PN metric equation?",
            "allowed_if": "they are vertical-only, exact/topological, auxiliary double-zero, or higher order than 2PN in the local branch",
            "fails_if": "they generate observed metric stress not proportional to EH/matter/EM",
            "result": "must be stress-tested in 4022",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "stress_id": "STR4021_1_galaxy_cosmology_memory",
            "question": "Can memory/galaxy/cosmology operators coexist with local GR?",
            "allowed_if": "their local projection is screened/vertical/boundary-silent or scales outside Solar-System 2PN sensitivity",
            "fails_if": "the same operator produces an unsuppressed q_loc or R11 PPN projection",
            "result": "must be either local-kernel theorem or residual coefficient",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "stress_id": "STR4021_2_source_prefactors",
            "question": "Can source/mass weights vary by material, range, or field sector?",
            "allowed_if": "no Hom into K_G/source slot and all ordinary/EM/binding stress varies once against g_obs",
            "fails_if": "material/range/source prefactors survive after parent descent",
            "result": "would break WEP/PPN unless scored below bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "stress_id": "STR4021_3_public_claim",
            "question": "Does the witness prove MTS local GR today?",
            "allowed_if": "actual parent corpus adopts WIT4021_0..6 or score rows become numeric/source-backed",
            "fails_if": "we treat this sufficient contract as already adopted",
            "result": "no public claim from 4021",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4021_0_witness_adopted",
            "assumption": "WIT4021_0..6 are adopted by the parent local branch",
            "result_expected": "all 4020 PPN score rows theorem-zero under witness",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4021_1_current_corpus",
            "assumption": "witness exists as candidate contract but is not yet adopted by the corpus",
            "result_expected": "progress yes; public claim no; next stress-test/adopt",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4021_2_R11_survives",
            "assumption": "an MTS local operator survives outside the allowed WIT4021 classes",
            "result_expected": "route to first executable Pi_gamma/Pi_beta residual coefficient fill",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4021_3_q_loc_survives",
            "assumption": "q_loc/Khat is not vertical/projector-silent",
            "result_expected": "route to delta_beta_q_loc and alpha_lambda bound inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case_id == "CASE4021_0_witness_adopted":
            verdict = "CONDITIONAL_LOCAL_GR_ZERO_VECTOR_UNDER_WITNESS"
            next_action = "stress-test the witness against actual MTS local operators before adoption"
        elif case_id == "CASE4021_1_current_corpus":
            verdict = "WITNESS_CONTRACT_AVAILABLE_NOT_CORPUS_ADOPTED"
            next_action = "4022 should try to adopt or falsify each witness clause against the corpus"
        elif case_id == "CASE4021_2_R11_survives":
            verdict = "R11_OPERATOR_SCORE_REQUIRED"
            next_action = "fill Pi_gamma/Pi_beta coefficients for the surviving operator"
        else:
            verdict = "QLOC_BOUND_REQUIRED"
            next_action = "derive q_loc amplitude/kernel or source local bounds"
        rows.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4021",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4021_0_construct_witness",
            "decision": "constructed a sufficient parent local action witness",
            "rationale": "this is the shortest derivation path: one typed parent branch zeros many PPN residuals",
            "effect": "local-GR route now has an explicit action-level contract",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4021_1_not_adopted_yet",
            "decision": "do not mark witness as corpus-adopted",
            "rationale": "a sufficient contract is not evidence that the existing full MTS corpus already satisfies it",
            "effect": "claim gates remain false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4021_2_score_fill_under_witness",
            "decision": "filled PPN scorer rows with conditional theorem-zero values under the witness",
            "rationale": "if 4022 adopts the witness, the first PPN score collapses to the GR vector without cancellation",
            "effect": "if rejected, the same rows identify exact coefficient fills needed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4021_3_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "the witness must now be stress-tested against actual MTS motion/time/space operators",
            "effect": "next turn should either adopt clauses or expose the first real residual coefficient",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4021_0_local_GR",
            "claim": "MTS locally reduces to GR/PPN",
            "allowed": False,
            "reason": "WIT4021 is a sufficient witness contract, not yet adopted by the actual corpus",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4021_1_PPN_score_pass",
            "claim": "PPN residual score passes",
            "allowed": False,
            "reason": "witness rows are conditional theorem-zero values; corpus score rows are not claim-ready",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4021_2_numerical_G",
            "claim": "MTS predicts numerical G",
            "allowed": False,
            "reason": "the witness preserves calibrated G_ref rather than predicting its dimensionful value",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4021_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "stress-test WIT4021 against actual MTS local motion/time/space operators; adopt every allowed clause or route the first surviving operator to an executable PPN residual coefficient",
            "success_condition": "each major MTS local operator is labelled admitted-by-witness, excluded-from-local-2PN, or routed to a concrete residual coefficient row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "constructed a sufficient parent-action witness and conditional PPN zero fill; corpus adoption remains pending",
            "current_best_route": "stress-test/adopt the witness against actual MTS operators, then score any survivor",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current = next(row for row in results if row["case_id"] == "CASE4021_1_current_corpus")
    DOC_PATH.write_text(
        f"""# 4021 - Parent Adoption Witness Or First PPN Score Input Fill

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

This checkpoint takes the derivation-first route. It constructs the sufficient local parent-action witness:

`Q_parent^loc = Q_dyn^loc x K_G x Q_aux`, with `q:Q_dyn^loc -> Met_obs`, `V=ker(Dq)`, `kappa_* in K_G`, and `T_local K_G=0`.

The proposed local 2PN action contract is:

`S_loc^{{<=2PN}} = S_MTS^vert[Phi] + (1/(2*kappa_*)) int R[g_obs(q(Phi))] eps_obs + S_matter[psi,g_obs,theta] + S_EM[A,g_obs,mu0,J] + S_binding + dB + S_top + S_aux^double-zero`.

Allowed non-EH local operators through 2PN are only:

`exact`, `topological`, `vertical-only with Dq=0`, or `auxiliary double-zero`.

Everything else must be scored.

## Derived Under The Witness

- `delta_local kappa_*=0`, hence `Gdot/G=0` inside the local branch.
- `DeltaE_R11^(1)=DeltaE_R11^(2)=0`, hence `delta_gamma_R11=delta_beta_R11=0`.
- Matter, EM, binding and Poynting stress enter the Hilbert current once.
- EH weak-field readout gives the Newton/Poisson bridge with calibrated `G_ref`.
- Same-source EH nonlinear completion gives `B_source=A_source^2`, hence `delta_beta_source=0`.
- If `q_loc/Khat` is vertical/projector-silent, then `delta_beta_q_loc=0`.
- Therefore the witness gives `gamma=beta=1`, `alpha_i=xi=zeta_i=0`, and `Gdot/G=0`.

## Current Corpus Verdict

- Current evaluator result: `{current["verdict"]}`.
- Claim result: `{current["claim_result"]}`.
- Source needles found: `{source_hits}/{source_total}`.

This is not a public local-GR claim. It is a serious action-level contract: adopt it and the local branch closes; violate it and the first surviving operator has to be scored.

## Stress Test Needed

4022 must test the actual MTS motion/time/space operators against this witness:

- admitted by witness;
- excluded from local 2PN;
- or routed to `delta_gamma_R11`, `delta_beta_R11`, `delta_beta_q_loc`, `delta_beta_source`, preferred-frame, conservation, or `Gdot/G`.

## Next Target

- `{NEXT_DOC}`
- `{NEXT_SCRIPT}`
""",
        encoding="utf-8",
    )


def append_spine(timestamp: str) -> None:
    marker = "## 4021 - Parent Local Action Witness"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: constructed a sufficient local parent-action witness: `Q_parent^loc=Q_dyn^loc x K_G x Q_aux`, `q:Q_dyn^loc->Met_obs`, `V=ker(Dq)`, `T_local K_G=0`.
- Action contract: `S_loc^{{<=2PN}}=S_MTS^vert+(1/(2*kappa_*))int R[g_obs]eps_obs+S_matter+S_EM+S_binding+dB+S_top+S_aux^double-zero`.
- Allowed non-EH local operators through 2PN: exact, topological, vertical-only with `Dq=0`, or auxiliary double-zero; everything else must be scored.
- Under this witness, the conditional PPN score fills as zero: `delta_gamma_R11=delta_beta_source=delta_beta_R11=delta_beta_q_loc=alpha_i=xi=zeta_i=Gdot/G=0`.
- Guard: witness is sufficient but not yet corpus-adopted, so no public local-GR claim.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4021 - Parent Local Action Witness" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    witness: list[dict[str, Any]],
    lemmas: list[dict[str, Any]],
    score: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4021_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4021_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, witness_id in enumerate(
        [
            "WIT4021_0_configuration",
            "WIT4021_1_action",
            "WIT4021_2_no_extra_operators",
            "WIT4021_3_source_current",
            "WIT4021_4_observed_Hodge",
            "WIT4021_5_q_loc_kernel",
            "WIT4021_6_readout_boundary",
            "WIT4021_7_claim_guard",
        ],
        start=2,
    ):
        add(f"VAL4021_{idx:02d}_witness", any(row["witness_id"] == witness_id for row in witness), f"{witness_id} present")
    for idx, lemma_id in enumerate(
        [
            "LEM4021_0_KG_local_variation",
            "LEM4021_1_EH_operator_zero",
            "LEM4021_2_source_once_conservation",
            "LEM4021_3_Newton_Poisson_readout",
            "LEM4021_4_beta_square_law",
            "LEM4021_5_q_loc_vertical_kernel",
            "LEM4021_6_PPN_zero_vector_under_witness",
        ],
        start=10,
    ):
        add(f"VAL4021_{idx:02d}_lemma", any(row["lemma_id"] == lemma_id for row in lemmas), f"{lemma_id} present")
    for idx, score_id in enumerate(
        [
            "WPS4021_0_delta_gamma_R11",
            "WPS4021_1_delta_beta_source",
            "WPS4021_2_delta_beta_R11",
            "WPS4021_3_delta_beta_q_loc",
            "WPS4021_4_preferred_frame",
            "WPS4021_5_conservation_zeta",
            "WPS4021_6_Gdot",
            "WPS4021_7_master",
        ],
        start=17,
    ):
        add(f"VAL4021_{idx:02d}_score", any(row["score_id"] == score_id for row in score), f"{score_id} present")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4021_25_witness_case", result_lookup["CASE4021_0_witness_adopted"]["verdict"] == "CONDITIONAL_LOCAL_GR_ZERO_VECTOR_UNDER_WITNESS", "witness-adopted case zeroes vector conditionally")
    add("VAL4021_26_current_case", result_lookup["CASE4021_1_current_corpus"]["verdict"] == "WITNESS_CONTRACT_AVAILABLE_NOT_CORPUS_ADOPTED", "current case remains adoption-pending")
    add("VAL4021_27_R11_case", result_lookup["CASE4021_2_R11_survives"]["verdict"] == "R11_OPERATOR_SCORE_REQUIRED", "R11 survivor routed to score")
    add("VAL4021_28_q_loc_case", result_lookup["CASE4021_3_q_loc_survives"]["verdict"] == "QLOC_BOUND_REQUIRED", "q_loc survivor routed to bound")
    add("VAL4021_29_witness_not_adopted", all(str(row.get("corpus_adopted", "")).lower() == "false" for row in witness), "witness rows not marked corpus-adopted")
    add("VAL4021_30_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates false")
    add("VAL4021_31_score_not_claim_ready", all(str(row.get("claim_ready", "")).lower() == "false" for row in score), "score fills are not claim-ready")
    add("VAL4021_32_stress_test_rows", len(stress) >= 4 and any(row["stress_id"] == "STR4021_0_motion_time_space_terms" for row in stress), "stress-test rows emitted")
    add("VAL4021_33_decision_witness", any(row["decision_id"] == "DEC4021_0_construct_witness" for row in decisions), "witness construction decision recorded")
    add("VAL4021_34_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    output_tables = [
        sources,
        witness,
        lemmas,
        score,
        stress,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4021_35_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4021_36_doc_exists", DOC_PATH.exists() and "sufficient local parent-action witness" in read_text(DOC_PATH), "document written with witness contract")
    add("VAL4021_37_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4021_38_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4021_39_compile", compile_ok, "script compiles")
    add("VAL4021_40_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4021_41_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4021_42_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4021_43_no_numerical_G_claim", any(row["claim_id"] == "CLAIM4021_2_numerical_G" and str(row["allowed"]).lower() == "false" for row in claims), "numerical G overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    witness = witness_rows(timestamp)
    lemmas = lemma_rows(timestamp)
    score = score_rows(timestamp)
    stress = stress_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["witness"], witness)
    write_csv(OUTPUTS["lemmas"], lemmas)
    write_csv(OUTPUTS["score"], score)
    write_csv(OUTPUTS["stress"], stress)
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

    validation = build_validation_rows(timestamp, sources, witness, lemmas, score, stress, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4021 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
