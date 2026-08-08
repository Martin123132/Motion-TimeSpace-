from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3575-Y5-R2FR-Req-zero-source-worldtube-Hamiltonian-glue-or-residual-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_REQ_ZERO_SINGLE_CHARGE_3575"
CHECKPOINT_ID = "3575"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3574": RESIDUALS / "P8_Y5_R2FR_3574_NEXT_TARGET.csv",
        "eq_gate_3574": RESIDUALS / "P8_Y5_R2FR_3574_JMTOP_EQUALS_PIMJH_GATE.csv",
        "drift_rows_3574": RESIDUALS / "P8_Y5_R2FR_3574_MEFF_DRIFT_SOURCE_ROWS.csv",
        "status_3574": RESIDUALS / "P8_Y5_R2FR_3574_STATUS.csv",
        "decision_3574": RESIDUALS / "P8_Y5_R2FR_3574_DECISION_LEDGER.csv",
        "pim_chainmap_3426": RESIDUALS / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
        "pim_top_demoter_3426": RESIDUALS / "P8_Y5_R2FR_3426_TOPOLOGICAL_PIM_DEMOTER.csv",
        "pc3400_update_3426": RESIDUALS / "P8_Y5_R2FR_3426_PC3400_3_UPDATE.csv",
        "worldtube_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "worldtube_proof": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
        "worldtube_clauses": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
        "parent_worldtube_clauses": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "parent_worldtube_noether": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_NOETHER_CHAIN.csv",
        "parent_worldtube_obstructions": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_OBSTRUCTIONS.csv",
        "ham_boundary_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "hilbert_worldtube_3423": RESIDUALS / "P8_Y5_R2FR_3423_HILBERT_WORLDTUBE_CLOSURE_THEOREM.csv",
        "source_mass_audit_2921": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
        "newton_zero_3399": RESIDUALS / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
        "newton_chain_3399": RESIDUALS / "P8_Y5_R2FR_3399_NEWTON_CLOSURE_CHAIN.csv",
        "pc3400_clauses": RESIDUALS / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
        "pc3400_activation": RESIDUALS / "P8_Y5_R2FR_3400_FIRST_ORDER_ACTIVATION_THEOREM.csv",
        "pc3400_adoption_3424": RESIDUALS / "P8_Y5_R2FR_3424_PC3400_ADOPTION_AUDIT.csv",
        "pc3400_lock_3425": RESIDUALS / "P8_Y5_R2FR_3425_PC3400_3_LOCK_AUDIT.csv",
        "poynting_bound": RESIDUALS / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv",
        "source_descent": RESIDUALS / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "mass_flatness_3515": RESIDUALS / "P8_Y5_R2FR_3515_MASS_FLATNESS_GATES.csv",
        "mass_flat_zero_3550": RESIDUALS / "P8_Y5_R2FR_3550_MASS_FLAT_ZERO_PROOF_ATTEMPT.csv",
        "eh_mass_theorem": RESIDUALS / "P8_Y5_EH_MASS_PARAMETER_THEOREM.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3574": "declares the 3575 R_eq zero target",
        "eq_gate_3574": "imports R_eq decomposition and Poynting guard",
        "drift_rows_3574": "imports R_eq/B_zero/Poynting/Meff residual rows",
        "status_3574": "imports topological current equality status",
        "decision_3574": "imports same-object next-action decision",
        "pim_chainmap_3426": "imports Hilbert identity/inclusion Pi_M chain-map theorem",
        "pim_top_demoter_3426": "imports old topological Pi_M demotion rules",
        "pc3400_update_3426": "imports PC3400_3 update after Hilbert identity branch",
        "worldtube_theorem": "imports worldtube source-measure theorem",
        "worldtube_proof": "imports source-measure proof sketch",
        "worldtube_clauses": "imports source-measure clauses",
        "parent_worldtube_clauses": "imports parent worldtube glue clauses",
        "parent_worldtube_noether": "imports Noether charge chain",
        "parent_worldtube_obstructions": "imports wrong-object and calibration obstructions",
        "ham_boundary_contract": "imports Hamiltonian boundary charge contract",
        "hilbert_worldtube_3423": "imports Hilbert worldtube closure theorem attempt",
        "source_mass_audit_2921": "imports source-mass identity audit",
        "newton_zero_3399": "imports first-order Newton zero theorem",
        "newton_chain_3399": "imports Newton residual closure chain",
        "pc3400_clauses": "imports parent signature clauses",
        "pc3400_activation": "imports activation theorem",
        "pc3400_adoption_3424": "imports adoption audit",
        "pc3400_lock_3425": "imports PC3400_3 lock audit",
        "poynting_bound": "imports Poynting source-worldtube flux bound",
        "source_descent": "imports source-coordinate descent certificate",
        "mass_flatness_3515": "imports mass-flat source-connection gates",
        "mass_flat_zero_3550": "imports mass-flat zero proof attempt",
        "eh_mass_theorem": "imports EH mass parameter and PPN guard",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def single_charge_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "SCT3575_0_single_source_current",
            "define one parent source current",
            "J_H[tau] := -T^mu_nu[e_obs,Psi] tau^nu epsilon_mu, with W_source := closure(supp J_H[tau])",
            "This gives one source object used by matter variation, support/worldtube selection, and mass readout.",
            "CONDITIONAL_DEFINITION_FROM_HILBERT_WORLDTUBE_BRANCH",
            "hilbert_worldtube_3423",
        ),
        (
            "SCT3575_1_identity_PiM",
            "choose Pi_M as Hilbert identity/inclusion",
            "Pi_M := Pi_M^H on the Hilbert mass-current complex, so Pi_M J_H = J_H and [d,Pi_M]J_H=0",
            "This kills the independent projector commutator and projector-stress problem in this branch.",
            "EXACT_CONDITIONAL_THEOREM",
            "pim_chainmap_3426",
        ),
        (
            "SCT3575_2_same_worldtube_top_class",
            "define the topological representative from the same charge",
            "Q_H[tau] := integral_{Sigma cap W_source} J_H[tau]; choose [J_M^top] as the linking cohomology class with period Q_H[tau]",
            "The topological mass charge is no longer an independent label; it is the same Hilbert worldtube charge represented in exterior cohomology.",
            "CONDITIONAL_CLASS_DEFINITION",
            "worldtube_theorem",
        ),
        (
            "SCT3575_3_period_zero_difference",
            "derive class-zero equality",
            "[Pi_M^H J_H - J_M^top] has zero periods on every linking S2 in the exterior annulus",
            "If the annulus has no extra harmonic/torsion class and support does not cross it, the difference is exact: Pi_M^H J_H-J_M^top=dC.",
            "DERIVED_IF_SINGLE_LINKING_CLASS_AND_NO_HARMONIC_REMAINDER",
            "parent_worldtube_clauses",
        ),
        (
            "SCT3575_4_Req_zero_flux",
            "absorb exact difference into B_zero",
            "Pi_M^H J_H = J_M^top + dB_zero with R_eq=0 at the flux/cohomology level",
            "Then int_A dR_eq=0 and epsilon_Req_annulus=0 in the single-charge Hilbert-identity branch.",
            "EXACT_CONDITIONAL_FLUX_THEOREM",
            "eq_gate_3574",
        ),
        (
            "SCT3575_5_Hamiltonian_charge_lock",
            "tie the same charge to H_tau",
            "M_H := H_tau[S_outer]-H_ref = integral_{Sigma cap W_source} J_H[tau] and mu_obs=G_ref M_H",
            "This converts source equality into measured GM only if H_tau is integrable, H_ref is fixed, tau is locked, and G_ref is constant.",
            "DOWNSTREAM_CONDITIONAL_NOT_SIGNED",
            "ham_boundary_contract",
        ),
        (
            "SCT3575_6_Newton_first_order_transfer",
            "transfer to first-order Newton only after PC3400",
            "PC3400_0..6 plus no retained rows imply Delta_Newton_v_coupled=0",
            "3575 closes the R_eq piece conditionally, but the full first-order Newton source branch still needs H_ref, no-extra-mass, and v coefficient signatures.",
            "PARTIAL_INPUT_TO_3399_NOT_FULL_PROMOTION",
            "newton_zero_3399",
        ),
        (
            "SCT3575_7_PPN_guard",
            "do not promote to local GR",
            "A same-object source charge does not by itself prove beta, gamma, preferred-frame silence, R10, or clock/orbital residuals",
            "The result is a coupling/source-identity improvement, not the end of the local GR proof.",
            "GUARDRAIL_RETAINED",
            "eh_mass_theorem",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "step": step,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, step, mathematical_form, derivation, status, source_key in specs
    ]


def req_zero_derivation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "REQ3575_0_start",
            "start from 3574 decomposition",
            "R_eq := Pi_M J_H - J_M^top - dB_zero",
            "This is an exact definition of the obstruction.",
            "EXACT",
            "eq_gate_3574",
        ),
        (
            "REQ3575_1_identity_branch",
            "select Hilbert identity branch",
            "Pi_M=Pi_M^H => Pi_M J_H=J_H and [d,Pi_M]J_H=0",
            "The projector is no longer a separate topological/readout operator; it is the inclusion of the same Hilbert source complex.",
            "EXACT_IF_BRANCH_ADOPTED",
            "pim_chainmap_3426",
        ),
        (
            "REQ3575_2_same_periods",
            "same linking periods",
            "integral_S Pi_M^H J_H = Q_H[tau] = integral_S J_M^top for every allowed linking surface S",
            "Because both sides are normalized by the same Hilbert worldtube source charge, their exterior periods match.",
            "DERIVED_IF_WORLD_TUBE_SOURCE_MEASURE_LOCKED",
            "worldtube_proof",
        ),
        (
            "REQ3575_3_exact_difference",
            "zero-period closed difference",
            "d(Pi_M^H J_H-J_M^top)=0 and all periods vanish => Pi_M^H J_H-J_M^top=dC",
            "This is the cohomology step; it requires a single linking mass class and no leftover harmonic/domain class.",
            "DERIVED_IF_TOPOLOGY_SELECTOR_CLEAN",
            "parent_worldtube_obstructions",
        ),
        (
            "REQ3575_4_absorb_C",
            "choose B_zero=C with zero compact flux",
            "Pi_M^H J_H=J_M^top+dB_zero and R_eq=0",
            "If int_boundary dB_zero=0, this is not hiding a monopole shift.",
            "CONDITIONAL_REQ_ZERO",
            "pim_top_demoter_3426",
        ),
        (
            "REQ3575_5_flux_result",
            "Meff radial/time flux result",
            "int_A d(Pi_M^H J_H)=int_A dR_eq=0",
            "The equality is strong enough for flux closure/Meff drift, but not necessarily a pointwise local-stress theorem.",
            "EXACT_CONDITIONAL_FLUX_CLOSURE",
            "drift_rows_3574",
        ),
        (
            "REQ3575_6_exchange_exception",
            "Poynting/extra exchange exception",
            "Pi_M dJ_extra, Poynting collar flux, boundary/reference flux, or non-EH charge re-enters as R_eq_eff",
            "Any extra source-owner current means the single-charge proof applies only after that channel is zero or bounded.",
            "RETAINED_EXCEPTION",
            "poynting_bound",
        ),
        (
            "REQ3575_7_verdict",
            "3575 proof verdict",
            "R_eq=0 is derivable for the Hilbert-identity single-charge branch at flux/cohomology level; current MTS has not yet parent-activated all branch clauses",
            "This is a genuine route to the coupling fix, but still nonclaim until adoption/zero rows close.",
            "CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "pc3400_update_3426",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": derivation_id,
            "step": step,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for derivation_id, step, mathematical_form, derivation, status, source_key in specs
    ]


def branch_selector_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "BSC3575_0_selector",
            "B_single_charge",
            "B_SC := I_same_JH * I_PiM_identity * I_same_worldtube_period * I_no_harmonic_remainder * I_Bzero_zero_flux * I_no_extra_exchange",
            "If B_SC=1, the 3575 R_eq flux theorem is active; otherwise residual rows remain live.",
            "SELECTOR_DEFINED_NONCLAIM",
            "pc3400_clauses",
        ),
        (
            "BSC3575_1_Req_flux",
            "epsilon_Req_annulus",
            "epsilon_Req_annulus = (1-B_SC) * epsilon_Req_input",
            "The single-charge branch sets the R_eq annulus flux to zero; nonidentity/topological branches must fill it.",
            "CONDITIONAL_ZERO_OR_INPUT",
            "drift_rows_3574",
        ),
        (
            "BSC3575_2_commutator",
            "I_commutator",
            "I_commutator = (1-B_PiM_identity) * I_commutator_topological",
            "Identity/inclusion Pi_M kills the commutator; old topological Pi_M still requires bounds.",
            "CONDITIONAL_ZERO_OR_INPUT",
            "pim_chainmap_3426",
        ),
        (
            "BSC3575_3_projector_stress",
            "T_PiM_projector",
            "T_PiM_projector = 0 in identity/inclusion branch; retained for Hodge/DeWitt/domain/readout projectors",
            "This prevents a mass projector from creating its own local fifth force in the adopted branch.",
            "CONDITIONAL_ZERO_OR_INPUT",
            "pim_chainmap_3426",
        ),
        (
            "BSC3575_4_mass_envelope",
            "epsilon_M_total",
            "epsilon_M_total <= epsilon_Req_annulus + epsilon_Bzero_flux + epsilon_Wsource_glue + epsilon_Poynting_worldtube + epsilon_extra_mass + epsilon_Href_lock + epsilon_cal",
            "This is the no-cancellation residual envelope if B_SC is not fully active.",
            "EXECUTABLE_ENVELOPE_NONCLAIM",
            "drift_rows_3574",
        ),
        (
            "BSC3575_5_Newton_product",
            "Delta_Newton_v_coupled",
            "Delta_Newton_v_coupled=(1+delta_KC)(1+epsilon_M_total)(1+delta_kappa)(1+delta_ellJ)-1",
            "3575 can reduce epsilon_M_total, but Newton still needs kappa, ell_J, and v coefficient routes.",
            "USES_3399_PRODUCT_LAW",
            "newton_chain_3399",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "selector_id": selector_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for selector_id, symbol, formula, meaning, status, source_key in specs
    ]


def hamiltonian_gm_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "HGM3575_0_tau_lock",
            "one tau across source, charge, clocks and readout",
            "tau_source=tau_H=tau_clock=tau_orbit",
            "PARTIAL_OPEN",
            "pc3400_lock_3425",
        ),
        (
            "HGM3575_1_Htau_integrability",
            "integrable Hamiltonian charge",
            "delta H_tau finite and field-space curl zero after boundary/reference conditions",
            "PARTIAL_EH_ONLY_EXTRA_CURLS_OPEN",
            "pc3400_lock_3425",
        ),
        (
            "HGM3575_2_Href_lock",
            "fixed reference subtraction",
            "H_ref fixed before source/orbit comparison and derivative-silent",
            "OPEN",
            "pc3400_lock_3425",
        ),
        (
            "HGM3575_3_same_source_measure",
            "dressed source charge definition",
            "M_source[W] := H_tau[S_outer]-H_ref = integral_{Sigma cap W_source} J_H[tau]",
            "CONDITIONAL_DEFINITION_REQUIRED",
            "worldtube_clauses",
        ),
        (
            "HGM3575_4_constant_Gref",
            "constant universal G_ref",
            "kappa_MTS=8*pi*G_ref/c^4 with no source/species/range/frame labels",
            "CAN_SIGN_AS_PARENT_CONSTANT_NOT_SI_DERIVATION",
            "pc3400_adoption_3424",
        ),
        (
            "HGM3575_5_Poisson_Gauss",
            "measured-GM calibration",
            "B_xi/G_ref=M_eff[Pi_M J_H] and weak-field Poisson/Gauss/orbital readout agree",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "ham_boundary_contract",
        ),
        (
            "HGM3575_6_no_extra_mass",
            "no unowned mass channels",
            "Q_nonEH+Q_PiM+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa+Q_Poynting=0 or retained",
            "FAIL_OPEN_RETAIN_ROWS",
            "ham_boundary_contract",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "mathematical_form": mathematical_form,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, mathematical_form, status, source_key in specs
    ]


def residual_fill_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "RF3575_0_epsilon_Req_input",
            "epsilon_Req_input",
            "|int_A dR_eq|/|M_eff| for non-single-charge branches",
            "dimensionless",
            "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "eq_gate_3574",
            "wrong-object equality residual",
        ),
        (
            "RF3575_1_epsilon_Bzero_flux",
            "epsilon_Bzero_flux",
            "|int_boundary dB_zero|/|M_eff|",
            "dimensionless",
            "MISSING_BOUNDARY_REFERENCE_INPUT",
            "drift_rows_3574",
            "boundary/improvement monopole shift",
        ),
        (
            "RF3575_2_epsilon_Wsource_glue",
            "epsilon_Wsource_glue",
            "|Q_M-integral_W J_H[tau]|/|M_eff|",
            "dimensionless",
            "ZERO_IN_SINGLE_CHARGE_BRANCH_ELSE_MISSING_INPUT",
            "drift_rows_3574",
            "worldtube/source equality failure",
        ),
        (
            "RF3575_3_epsilon_Poynting_worldtube",
            "epsilon_Poynting_worldtube",
            "|int_W Pi_M dJ_Poynting|/|M_eff| or collar-flux bound",
            "dimensionless after common mass-flux normalization",
            "BOUND_FORMULA_READY_INPUTS_MISSING",
            "poynting_bound",
            "EM/wave momentum flux through source collar",
        ),
        (
            "RF3575_4_epsilon_Href_lock",
            "epsilon_Href_lock",
            "|D_X H_ref|/|M_eff| or field-space curl/reference mismatch envelope",
            "dimensionless or derivative-normalized",
            "MISSING_REFERENCE_FUNCTIONAL",
            "pc3400_lock_3425",
            "reference/backfill drift",
        ),
        (
            "RF3575_5_epsilon_extra_mass",
            "epsilon_extra_mass",
            "|Q_nonEH+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa|/|M_eff|",
            "dimensionless",
            "MISSING_ZERO_CERTIFICATES_OR_BOUNDS",
            "ham_boundary_contract",
            "unowned compact-source mass",
        ),
        (
            "RF3575_6_epsilon_cal",
            "epsilon_cal",
            "|M_eff[Pi_M J_H]-M_Gauss_orbital|/|M_eff|",
            "dimensionless",
            "CALIBRATION_GATE_OPEN",
            "ham_boundary_contract",
            "Poisson/Gauss/orbital measured-GM mismatch",
        ),
        (
            "RF3575_7_dlnMeff_dt",
            "dln_Meff_dt",
            "D_t ln int_S Pi_M J_H; zero in B_SC branch only after H_ref/extra/Poynting silence",
            "yr^-1 or s^-1",
            "LIVE_DERIVATIVE_ROW",
            "drift_rows_3574",
            "Gdot/local GM drift",
        ),
        (
            "RF3575_8_partial_r_ln_mu_obs",
            "partial_r_ln_mu_obs",
            "partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_M_total)",
            "m^-1 or AU^-1",
            "LIVE_RADIAL_ROW",
            "drift_rows_3574",
            "radial source hair/inverse-square residual",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "observable_link": observable,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, units, status, source_key, observable in specs
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3575_0_sources", "source audit", "PASS", "all required 3575 source paths exist"),
        ("GATE3575_1_identity_PiM", "Hilbert identity/inclusion Pi_M", "PASS_CONDITIONAL", "3426 gives exact commutator/projector-stress zero if parent adopts Pi_M^H"),
        ("GATE3575_2_Req_flux_zero", "R_eq annulus flux zero", "PASS_CONDITIONAL", "same-worldtube periods plus identity Pi_M imply R_eq=0 at flux/cohomology level"),
        ("GATE3575_3_parent_activation", "parent branch activation", "FAIL_CURRENT_CLAIM", "the current corpus has not adopted all B_SC clauses in one parent branch"),
        ("GATE3575_4_boundary_reference", "B_zero/H_ref boundary silence", "FAIL_CURRENT_CLAIM", "reference and compact-boundary flux remain open"),
        ("GATE3575_5_poynting_extra", "Poynting and extra source mass", "FAIL_CURRENT_CLAIM", "Poynting/exchange/no-extra-mass rows remain unfilled"),
        ("GATE3575_6_Newton", "first-order Newton source normalization", "PARTIAL_NOT_PROMOTED", "R_eq piece can close conditionally; kappa/ell_J/v-ratio/Href/no-extra-mass still decide the full product"),
        ("GATE3575_7_local_GR", "local GR/PPN", "FAIL_CURRENT_CLAIM", "PPN beta/gamma/preferred-frame and R10/clock/orbital rows remain downstream"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["status_3574"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3575_0_adopt_best_route",
            "prefer Hilbert identity/inclusion Pi_M over independent topological Pi_M for local source coupling",
            "It derives [d,Pi_M]J_H=0 and avoids conserving the wrong object if the topological representative is defined from the same worldtube source.",
            "Old topological Pi_M is kept only as a demoted/bounded branch.",
            "ADOPTED_AS_NEXT_PRIVATE_BRANCH_NONCLAIM",
            "pim_chainmap_3426",
        ),
        (
            "DEC3575_1_Req_progress",
            "count R_eq flux-zero as conditionally derived, not merely missing",
            "The single-charge theorem gives a clean exact route for epsilon_Req_annulus=0, contingent on parent activation.",
            "Future work should sign/adopt the branch or fill the named residual rows; do not re-audit generic topology.",
            "ADOPTED",
            "eq_gate_3574",
        ),
        (
            "DEC3575_2_G_constant_note",
            "do not try to derive the SI value of Newton's constant here",
            "As in GR, a universal branch constant G_ref may be signed as a coupling; the derivation target is no drift/species/range dependence and correct source normalization.",
            "This prevents wasting effort on deriving the numerical value of G while still blocking cheating by variable G.",
            "ADOPTED",
            "pc3400_adoption_3424",
        ),
        (
            "DEC3575_3_next_target",
            "write the adoption packet for PC3400_3 and PC3400_4 or fill the first residual rows",
            "3575 turns the coupling problem into a concrete parent-branch decision: sign Pi_M^H/H_tau/H_ref/no-extra-mass, or source epsilon_Href and epsilon_extra.",
            "3576 should attempt the parent adoption patch for the single-charge source branch.",
            "NEXT_TARGET_SELECTED",
            "pc3400_clauses",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "REQ_FLUX_ZERO_CONDITIONAL_THEOREM_DERIVED_FOR_HILBERT_IDENTITY_BRANCH_NOT_PROMOTED",
            "strongest_result": "If Pi_M is the Hilbert identity/inclusion and J_M^top is the exterior representative of the same Hilbert worldtube charge, then R_eq can be set to zero at flux/cohomology level and epsilon_Req_annulus=0.",
            "still_missing": "parent activation of the branch, H_tau integrability, fixed H_ref, zero compact B_zero flux, Poynting/extra-mass silence or bounds, constant G_ref readout, v coefficient signatures, and PPN residual closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3575_0",
            "target_doc": "3576-Y5-R2FR-PC3400-3-4-single-charge-parent-adoption-or-first-residual-fill.md",
            "target_script": "scripts/Y5_R2FR_3576_PC3400_3_4_single_charge_parent_adoption_or_first_residual_fill.py",
            "objective": "attempt to write a parent adoption packet for the Hilbert-identity single-charge branch that signs PC3400_3 and narrows PC3400_4; if not, fill first source-backed epsilon_Href/epsilon_extra/Poynting residual rows",
            "success_gate": "parent branch clauses for Pi_M^H, H_tau, H_ref, no B_zero flux, and no-extra-mass either signed as an internal candidate action or converted into source-backed residual inputs",
            "reason": "3575 derives the R_eq flux zero route conditionally; the next leap is adopting the branch in the parent action or filling the remaining residuals",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "R_eq_zero_single_charge_source_coupling",
            "status": "CONDITIONAL_FLUX_ZERO_ROUTE_FOUND_NOT_PARENT_ACTIVATED",
            "theorem_formula": "Pi_M^H J_H=J_M^top+dB_zero with R_eq=0 at flux/cohomology level",
            "selector_formula": "B_SC=I_same_JH I_PiM_identity I_same_worldtube_period I_no_harmonic I_Bzero_flux0 I_no_extra_exchange",
            "Newton_formula": "Delta_Newton_v_coupled=(1+delta_KC)(1+epsilon_M_total)(1+delta_kappa)(1+delta_ellJ)-1",
            "next_action": "sign PC3400_3/4 in parent branch or fill epsilon_Href/epsilon_extra/Poynting residual rows",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    derivation: list[dict[str, object]],
    selectors: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3575_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3575 source paths exist"))
    needles = {
        "handoff_3574": "NEXT3574_0",
        "eq_gate_3574": "EQ3574_3_worldtube_glue_route",
        "drift_rows_3574": "MEFF3574_0_R_eq_annulus",
        "status_3574": "TOPOLOGICAL_CURRENT_FORMAL_CLOSURE",
        "decision_3574": "DEC3574_3_next_target",
        "pim_chainmap_3426": "PCM3426_1_identity_chain_map",
        "pim_top_demoter_3426": "TDM3426_0_wrong_object",
        "pc3400_update_3426": "PC3400_3_verdict",
        "worldtube_theorem": "T510_1_worldtube_source_measure",
        "worldtube_proof": "P510_5",
        "worldtube_clauses": "WG510_7_dressed_source_definition",
        "parent_worldtube_clauses": "W504_4_worldtube_source_measure_glue",
        "parent_worldtube_noether": "N504_6_source_measure_readout",
        "parent_worldtube_obstructions": "O504_0_wrong_conserved_object",
        "ham_boundary_contract": "HC4_charge_equals_PiM_Hilbert_mass",
        "hilbert_worldtube_3423": "HWC3423_0_define_single_charge",
        "source_mass_audit_2921": "PSM2921_5_same_object_lemma",
        "newton_zero_3399": "T3399_D2_newton_zero",
        "newton_chain_3399": "NC3399_4_epsilon_M",
        "pc3400_clauses": "PC3400_4_no_boundary_extra_mass",
        "pc3400_activation": "ACT3400_2_newton_amplitude",
        "pc3400_adoption_3424": "PC3400_1_constant_kappa",
        "pc3400_lock_3425": "P3L3425_3_PiM_chain_map",
        "poynting_bound": "SWP3249_0_source_worldtube_Poynting_bound",
        "source_descent": "QSC3516_0_master_theorem",
        "mass_flatness_3515": "SBF3515_0_strong_zero",
        "mass_flat_zero_3550": "ZP3550_4_PiM_same_object",
        "eh_mass_theorem": "EH528_2_measured_mu_lock",
    }
    validations.append(("VAL3575_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3575 same-object/source-coupling needles found"))
    validations.append(("VAL3575_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3575 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3575_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3575_4_identity_theorem_present", any(row["theorem_id"] == "SCT3575_1_identity_PiM" and "[d,Pi_M]J_H=0" in str(row["mathematical_form"]) for row in theorem), "Hilbert identity/inclusion Pi_M theorem present"))
    validations.append(("VAL3575_5_Req_zero_flux_present", any(row["derivation_id"] == "REQ3575_4_absorb_C" and "R_eq=0" in str(row["mathematical_form"]) for row in derivation), "conditional R_eq zero row present"))
    validations.append(("VAL3575_6_selector_present", any(row["selector_id"] == "BSC3575_0_selector" and "B_SC" in str(row["formula"]) for row in selectors), "single-charge selector present"))
    validations.append(("VAL3575_7_residual_envelope_present", any(row["selector_id"] == "BSC3575_4_mass_envelope" and "epsilon_M_total" in str(row["formula"]) for row in selectors), "epsilon_M no-cancellation envelope present"))
    validations.append(("VAL3575_8_residual_rows_present", {"epsilon_Req_input", "epsilon_Bzero_flux", "epsilon_Wsource_glue", "epsilon_Poynting_worldtube", "epsilon_Href_lock", "epsilon_extra_mass", "epsilon_cal"}.issubset({str(row["symbol"]) for row in residuals}), "first residual fill rows present"))
    validations.append(("VAL3575_9_parent_not_promoted", any(row["gate_id"] == "GATE3575_3_parent_activation" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "parent activation remains unclaimed"))
    validations.append(("VAL3575_10_next_target_selected", any(row["decision_id"] == "DEC3575_3_next_target" for row in decisions), "PC3400_3/4 adoption next target selected"))
    validations.append(("VAL3575_11_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in theorem + derivation + selectors + residuals + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorem + derivation + selectors + residuals + gates + decisions)
    validations.append(("VAL3575_12_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3575*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3575_13_formalization_workbench_untouched", not formalization_touched, "no 3575 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    derivation: list[dict[str, object]],
    selectors: list[dict[str, object]],
    hamiltonian: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3575 - R_eq zero from source-worldtube/Hamiltonian glue or residual fill",
        "",
        "## Verdict",
        "3575 gets a real coupling foothold.  The old independent topological route can conserve the wrong object, but the Hilbert-identity single-charge branch gives a conditional theorem:",
        "",
        "`Pi_M = Pi_M^H`, `Pi_M^H J_H = J_H`, and `J_M^top` is chosen as the exterior representative of the same Hilbert worldtube charge.",
        "",
        "Then the exterior periods match, so `Pi_M^H J_H - J_M^top=dC`; choosing `B_zero=C` gives `Pi_M^H J_H=J_M^top+dB_zero` and `R_eq=0` at flux/cohomology level.  Therefore `epsilon_Req_annulus=0` in that branch.",
        "",
        "This is not yet a public Newton/local-GR claim.  It still needs parent activation, `H_tau/H_ref` reference lock, zero compact boundary flux, Poynting/extra-mass silence or bounds, and measured-GM calibration.  But it is no longer just 'missing coupling' fog: the best coupling route is now a single explicit branch selector.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Single-charge theorem"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## R_eq derivation"])
    for row in derivation:
        lines.append(f"- `{row['derivation_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Branch selector"])
    for row in selectors:
        lines.append(f"- `{row['selector_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Hamiltonian/GM gates"])
    for row in hamiltonian:
        lines.append(f"- `{row['gate_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Residual rows"])
    for row in residuals:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Activation gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    theorem = single_charge_theorem_rows(source_paths)
    derivation = req_zero_derivation_rows(source_paths)
    selectors = branch_selector_rows(source_paths)
    hamiltonian = hamiltonian_gm_gate_rows(source_paths)
    residuals = residual_fill_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3575_SOURCE_REGISTER.csv",
        "single_charge_theorem": RESIDUALS / "P8_Y5_R2FR_3575_SINGLE_CHARGE_THEOREM.csv",
        "Req_zero_derivation": RESIDUALS / "P8_Y5_R2FR_3575_REQ_ZERO_DERIVATION.csv",
        "branch_selector": RESIDUALS / "P8_Y5_R2FR_3575_BRANCH_SELECTOR_AND_RESIDUAL_ENVELOPE.csv",
        "Hamiltonian_GM_gates": RESIDUALS / "P8_Y5_R2FR_3575_HAMILTONIAN_GM_GLUE_GATES.csv",
        "residual_fill_rows": RESIDUALS / "P8_Y5_R2FR_3575_RESIDUAL_FILL_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3575_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3575_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3575_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3575_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_single_charge_Req_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3575_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["single_charge_theorem"], theorem)
    write_csv(outputs["Req_zero_derivation"], derivation)
    write_csv(outputs["branch_selector"], selectors)
    write_csv(outputs["Hamiltonian_GM_gates"], hamiltonian)
    write_csv(outputs["residual_fill_rows"], residuals)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, theorem, derivation, selectors, residuals, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, theorem, derivation, selectors, hamiltonian, residuals, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3575 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
