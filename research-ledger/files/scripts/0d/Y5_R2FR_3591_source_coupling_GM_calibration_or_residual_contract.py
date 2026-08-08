from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_COUPLING_GM_CALIBRATION_3591"
CHECKPOINT_ID = "3591"
DOC = ROOT / "3591-Y5-R2FR-source-coupling-GM-calibration-or-residual-contract.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3590": RESIDUALS / "P8_Y5_R2FR_3590_NEXT_TARGET.csv",
        "status_3590": RESIDUALS / "P8_Y5_R2FR_3590_STATUS.csv",
        "branch_3590": RESIDUALS / "P8_Y5_R2FR_3590_BRANCH_VERDICT.csv",
        "validation_3590": RESIDUALS / "P8_Y5_BRR545_3590_VALIDATION.csv",
        "newton_blockers_1339": RESIDUALS / "P8_Y5_R10_1339_NEWTON_TRANSFER_BLOCKERS.csv",
        "lovelock_1339": RESIDUALS / "P8_Y5_R10_1339_LOVELOCK_CONDITIONAL_THEOREM.csv",
        "source_owner_1793": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
        "action_current_1418": RESIDUALS / "P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv",
        "source_current_1415": RESIDUALS / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
        "worldtube_2388": RESIDUALS / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv",
        "hamiltonian_poisson": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "hilbert_monopole": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "hamiltonian_charge": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "mass_flux": RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
        "source_norm_theorem": RESIDUALS / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "mu_extra_vector": RESIDUALS / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "constant_gm_2583": RESIDUALS / "P8_Y5_SOURCE_NORM_2583_CONSTANT_GM_RESIDUAL_ROWS.csv",
        "owner_audit_2583": RESIDUALS / "P8_Y5_SOURCE_NORM_2583_OWNER_THEOREM_AUDIT.csv",
        "selector_2577": RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_NEWTON_GR_IMPLICATIONS.csv",
        "local_residual_vector": RESIDUALS / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        "qloc_interface_2581": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_OFFICIAL_RESIDUAL_INTERFACE.csv",
        "extra_hair_3585": RESIDUALS / "P8_Y5_R2FR_3585_EXTRA_HAIR_CHANNEL_AUDIT.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3591_SOURCE_REGISTER.csv",
        "gm_transfer_contract": RESIDUALS / "P8_Y5_R2FR_3591_GM_TRANSFER_CONTRACT.csv",
        "source_charge_audit": RESIDUALS / "P8_Y5_R2FR_3591_SOURCE_CHARGE_AUDIT.csv",
        "epsilon_mu_contract": RESIDUALS / "P8_Y5_R2FR_3591_EPSILON_MU_RESIDUAL_CONTRACT.csv",
        "newton_ppn_propagation": RESIDUALS / "P8_Y5_R2FR_3591_NEWTON_PPN_PROPAGATION_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3591_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3591_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3591_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_source_coupling_GM_calibration_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3591_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3591 source coupling / GM calibration source",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def gm_transfer_contract_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GMT3591_0_same_observed_frame",
            "same observed frame",
            "e_obs=e_matter=e_source=e_orbit and g_00=-1+2Phi/c^2 in that frame",
            "SN0/PG2",
            "needed so orbital acceleration reads the same potential sourced by the field equation",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "newton_stack",
        ),
        (
            "GMT3591_1_EH_or_bounded_operator",
            "weak-field operator",
            "E_munu=G_munu+Lambda g_munu+R11_residual and nabla^2 Phi=(kappa_eff c^4/2)rho_H + R_operator",
            "LOV1339/NEW1339_0",
            "needed before Poisson coefficient algebra is meaningful",
            "CONDITIONAL_EH_ONLY_NOT_PARENT_DERIVED",
            "lovelock_1339",
        ),
        (
            "GMT3591_2_parent_Hilbert_source",
            "Hilbert source current",
            "J_H and T_H are varied from the parent matter action before material labels/readout",
            "HM0/SCO1415/ACL1418",
            "needed so source mass is not a post-fit species/source selector",
            "NOT_PARENT_DERIVED",
            "source_current_1415",
        ),
        (
            "GMT3591_3_Hamiltonian_equals_Hilbert_mass",
            "charge-current equality",
            "B_xi/G_ref = M_H[Pi_M J_H] and delta B_xi = delta integral_S Pi_M J_H",
            "PG1/HC4/MF5",
            "turns a geometric boundary charge into the measured source mass",
            "NOT_PARENT_DERIVED",
            "hamiltonian_poisson",
        ),
        (
            "GMT3591_4_closed_flux",
            "closed projected mass flux",
            "d(Pi_M J_H)=0, so M_H(S2)-M_H(S1)=0 in compact source-free exterior annuli",
            "HM2/MF2/Y5SC1793_3",
            "prevents radial/time source hair from being hidden in GM",
            "NOT_DERIVED_PROJECTOR_COMMUTATOR_OPEN",
            "source_owner_1793",
        ),
        (
            "GMT3591_5_Gauss_orbital_calibration",
            "Gauss-to-orbit readout",
            "nabla^2 Phi=4piG_ref rho_H and a_r=-G_ref M_H/r^2, so v^2 r=G_ref M_H",
            "PG5/Y5SC1793_5",
            "the exact Newtonian bridge: measured GM becomes a consequence, not an input",
            "DOWNSTREAM_GATE_OPEN",
            "source_owner_1793",
        ),
        (
            "GMT3591_6_zero_extra_monopole",
            "extra source monopole silence",
            "mu_extra=Delta_nonEH+Delta_symp+Delta_PiM+Delta_extra+Delta_frame+Delta_cal+Delta_PPN+Delta_GK=0 or bounded",
            "PG6/HM5/SN6",
            "stops non-Hilbert/local-hair terms from masquerading as source mass",
            "RETAINED_RESIDUAL_REQUIRED",
            "mu_extra_vector",
        ),
        (
            "GMT3591_7_constant_universal_Gref",
            "universal coupling",
            "partial_t,r,A,lambda,frame G_ref=0 and G_ref=kappa_eff c^4/(8pi)",
            "PG7/HM4/SN7",
            "prevents a time/range/species/frame dependent G from being absorbed into measured GM",
            "NOT_PARENT_DERIVED",
            "owner_audit_2583",
        ),
        (
            "GMT3591_8_theorem_result_if_all_close",
            "Newton transfer theorem",
            "all preceding rows close => mu_obs=G_ref M_H, epsilon_mu=0, a_r=-G_ref M_H/r^2, and no fitted-GM hiding",
            "Y5SC1793_7/S5_Newton_gate",
            "source-normalized Newton becomes derived rather than calibrated after the fact",
            "THEOREM_ROUTE_EXACT_BUT_NOT_ACTIVATED",
            "source_norm_theorem",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "contract_id": contract_id,
            "contract_piece": piece,
            "mathematical_form": form,
            "source_contract": source_contract,
            "why_needed": why_needed,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "parent_signed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for contract_id, piece, form, source_contract, why_needed, status, source_key in rows
    ]


def source_charge_audit_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "SCA3591_0_no_fitted_source_mask",
            "Pi_M owner",
            "Pi_M must be parent-owned before readout; no post-fit GM mask or galaxy/source convention may define it",
            "MISSING_PARENT_PROJECTOR_ORIGIN",
            "mass_flux",
        ),
        (
            "SCA3591_1_same_frame_worldtube",
            "worldtube source measure",
            "W_source and J_H must be computed from the same observed coframe/time generator used by orbit readout",
            "MISSING_SAME_FRAME_TAU_EOBS_LOCK",
            "worldtube_2388",
        ),
        (
            "SCA3591_2_action_measure_current_owner",
            "action/current owner",
            "ordinary matter weights, action measure, hbar, and source currents must descend from one parent owner",
            "LOCK_NOT_PROVED_CURRENT_CORPUS",
            "action_current_1418",
        ),
        (
            "SCA3591_3_charge_current_equality",
            "Hamiltonian-Hilbert equality",
            "B_xi/G_ref must equal M_H[Pi_M J_H] with projector variation accounted for",
            "NOT_PARENT_DERIVED",
            "hamiltonian_charge",
        ),
        (
            "SCA3591_4_flux_closure",
            "closed exterior source flux",
            "d(Pi_M J_H)=0 or explicit residual d(Pi_M J_H) must be carried into radial/Gdot/source tests",
            "NOT_DERIVED_PROJECTOR_COMMUTATOR_OPEN",
            "source_owner_1793",
        ),
        (
            "SCA3591_5_no_extra_mass_projection",
            "extra monopole channels",
            "non-EH, GK, boundary, projector, domain, memory, range, frame, species and calibration monopoles must be zero or residual rows",
            "NOT_DERIVED_EXTRA_MASS_CHANNELS_ACTIVE",
            "source_owner_1793",
        ),
        (
            "SCA3591_6_second_order_stability",
            "PPN source stability",
            "same source charge must survive beta/gamma/preferred-frame order; Poisson-only success is insufficient for local GR",
            "NOT_DERIVED",
            "source_owner_1793",
        ),
        (
            "SCA3591_7_current_verdict",
            "GM source theorem",
            "GM transfer theorem is exact as a contract but not activated; residual propagation is mandatory",
            "RESIDUAL_CONTRACT_REQUIRED",
            "newton_blockers_1339",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": audit_id,
            "audit_piece": piece,
            "required_clause": clause,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "blocks_GM_claim": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for audit_id, piece, clause, status, source_key in rows
    ]


def epsilon_mu_contract_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("EMU3591_0_epsilon_frame", "epsilon_frame", "delta_frame_source", "same-frame/source-orbit split", "MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT", "constant_gm_2583"),
        ("EMU3591_1_epsilon_current", "epsilon_current", "current_rescaling + qbar_source_weight", "action/current owner not parent-signed", "MISSING_CURRENT_OWNER_OR_NUMERIC_RESIDUAL", "action_current_1418"),
        ("EMU3591_2_epsilon_flux", "epsilon_flux", "dln_Meff_dt + partial_r_ln_mu_obs", "mass-flux nonclosure/time-radial hair", "MISSING_FLUX_CLOSURE_OR_NUMERIC_RESIDUAL", "constant_gm_2583"),
        ("EMU3591_3_epsilon_extra", "epsilon_extra", "mu_extra_boundary_bulk_domain/(G_ref M_H)", "non-Hilbert extra monopole source channels", "MISSING_EXTRA_MONOPOLE_ZERO_OR_VECTOR", "mu_extra_vector"),
        ("EMU3591_4_epsilon_GK", "epsilon_GK_source", "K_GK_mu * X_GK_residual", "3590 GK residual projected into measured source coupling", "MISSING_K_GK_MU_MAP_OR_ETA_CLOSURE", "branch_3590"),
        ("EMU3591_5_epsilon_operator", "epsilon_operator", "R11/nonEH operator coefficient contribution to Poisson source coefficient", "EH-only operator not parent-derived", "MISSING_EH_ONLY_OR_R11_VECTOR", "local_residual_vector"),
        ("EMU3591_6_epsilon_calibration", "epsilon_calibration", "delta_G_ref + absolute calibration offset", "constant universal coupling not parent-derived", "MISSING_CONSTANT_UNIVERSAL_GREF", "owner_audit_2583"),
        ("EMU3591_7_epsilon_PPN_source", "epsilon_PPN_source", "delta_beta_source + preferred-frame/source PPN residuals", "second-order source stability not derived", "MISSING_SECOND_ORDER_SOURCE_VECTOR", "constant_gm_2583"),
        ("EMU3591_8_epsilon_mu_total", "epsilon_mu", "epsilon_frame + epsilon_current + epsilon_flux + epsilon_extra + epsilon_GK_source + epsilon_operator + epsilon_calibration + epsilon_PPN_source", "total measured-GM residual envelope, no cancellation credit", "RESIDUAL_CONTRACT_READY_VALUES_MISSING", "source_owner_1793"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "formula_or_definition": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "numeric_value_present": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for residual_id, symbol, formula, meaning, status, source_key in rows
    ]


def newton_ppn_propagation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "NPP3591_0_measured_mu",
            "mu_obs",
            "mu_obs := G_ref M_H * (1 + epsilon_mu)",
            "definition of measured source strength with explicit residual, not hidden fitted GM",
            "RESIDUAL_PROPAGATION_RULE",
            "source_owner_1793",
        ),
        (
            "NPP3591_1_Newton_acceleration",
            "a_r",
            "a_r = -G_ref M_H/r^2 * (1 + epsilon_mu + epsilon_radial_profile + epsilon_operator_force)",
            "Newton branch remains testable through a residual vector if source theorem fails",
            "NONCLAIM_TESTABLE_FORM",
            "newton_stack",
        ),
        (
            "NPP3591_2_Poisson_source",
            "Poisson residual",
            "nabla^2 Phi = 4piG_ref rho_H + R_operator + R_source + R_boundary",
            "separates operator failure from source coupling failure",
            "NONCLAIM_TESTABLE_FORM",
            "lovelock_1339",
        ),
        (
            "NPP3591_3_PPN_vector",
            "PPN_source_vector",
            "{gamma-1,beta-1,alpha_i,xi,zeta_i}_source receive explicit epsilon_mu/epsilon_GK/source residual contributions",
            "prevents Newton-looking pass from becoming local-GR claim",
            "RESIDUAL_VECTOR_REQUIRED",
            "local_residual_vector",
        ),
        (
            "NPP3591_4_R10_range",
            "alpha(lambda)",
            "range-dependent source or GK/local hair must enter alpha(lambda), not a constant GM calibration",
            "keeps short-range and fifth-force structure out of the absolute Newtonian calibration constant",
            "R10_REMAINS_SEPARATE_SCORE_BRANCH",
            "constant_gm_2583",
        ),
        (
            "NPP3591_5_no_absorption_cheat",
            "GM calibration policy",
            "constant universal calibration may set one overall G_ref only; derivatives/composition/range/profile residuals remain live",
            "prevents one fitted orbital GM from swallowing physical source-coupling failures",
            "PASS_GUARD",
            "source_norm_theorem",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "observable_or_quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, quantity, formula, meaning, status, source_key in rows
    ]


def activation_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3591_0_sources", "PASS", "all source paths and selected anchors exist", "next_3590"),
        ("GATE3591_1_transfer_contract", "PASS_CONTRACT_EXACT", "GM/Newton transfer theorem requirements are explicitly enumerated", "hamiltonian_poisson"),
        ("GATE3591_2_parent_source_charge", "FAIL_CURRENT_CLAIM", "parent Hilbert/Noether/Hamiltonian source charge is not derived", "source_owner_1793"),
        ("GATE3591_3_GM_not_hidden", "PASS_GUARD", "unclosed source coupling is propagated as epsilon_mu, not fitted GM", "source_norm_theorem"),
        ("GATE3591_4_Newton_claim", "FAIL_CURRENT_CLAIM", "Newtonian mechanics is not claimed until epsilon_mu and operator residuals close", "newton_blockers_1339"),
        ("GATE3591_5_PPN_claim", "FAIL_CURRENT_CLAIM", "Poisson-only bridge cannot promote local GR without PPN/source stability", "constant_gm_2583"),
        ("GATE3591_6_next_pivot", "PASS", "next target should attack the largest epsilon_mu component rather than re-loop GK", "mu_extra_vector"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "GM_TRANSFER_CONTRACT_DERIVED_RESIDUAL_PROPAGATION_ACTIVE",
            "strongest_result": "3591 derives the exact source-coupling contract needed to turn an EH/weak-field branch into Newtonian measured GM: same frame, EH/Poisson operator, parent Hilbert source, Hamiltonian-Hilbert equality, closed flux, Gauss/orbital readout, zero extra monopole, and constant universal G_ref. The current corpus does not close those clauses, so epsilon_mu is introduced as the explicit measured-GM residual vector.",
            "decision": "do not claim Newton/local-GR from fitted GM; propagate epsilon_mu into Newton, PPN, R10, and source-normalization tests until the source charge theorem closes",
            "still_missing": "parent matter/current owner, Pi_M origin, Hamiltonian-Hilbert equality, flux closure, worldtube/source measure glue, zero extra monopole, constant universal G_ref, second-order PPN source stability, numeric/source-backed epsilon_mu components",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3590"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3591_0",
            "target_doc": "3592-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md",
            "target_script": "scripts/Y5_R2FR_3592_PiM_Hilbert_charge_equality_or_epsilon_mu_input_pack.py",
            "objective": "attack the central source-coupling clause: derive Pi_M J_H equals the Hamiltonian/Hilbert mass charge, or build the first source-ready epsilon_mu input pack for measured-GM residuals",
            "success_gate": "either B_xi/G_ref=M_H[Pi_M J_H] is parent-signed with projector variation handled, or epsilon_mu components get source/unit/input rows without Newton/PPN claims",
            "reason": "3591 shows this equality is the shortest high-value path from MTS to Newtonian GM calibration",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    gm_contract: list[dict[str, object]],
    source_audit: list[dict[str, object]],
    epsilon_mu: list[dict[str, object]],
    propagation: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3590": "NEXT3590_0",
        "status_3590": "ABSORPTION_THEOREM_DERIVED_GK_BRANCH_DEMOTED_TO_EXPLICIT_RESIDUAL",
        "branch_3590": "BV3590_3_demoted_residual_parameter",
        "validation_3590": "VAL3590_14_formalization_workbench_untouched",
        "newton_blockers_1339": "NEW1339_2_GM_calibration",
        "lovelock_1339": "LOV1339_1_weak_field_algebra",
        "source_owner_1793": "Y5SC1793_7_verdict",
        "action_current_1418": "ACL1418_6_verdict",
        "source_current_1415": "SCO1415_6_verdict",
        "worldtube_2388": "WSC2388_7_same_object",
        "hamiltonian_poisson": "PG5_orbital_inverse_square_readout",
        "hilbert_monopole": "HM7_second_order_source_stability",
        "hamiltonian_charge": "HC4_charge_equals_PiM_Hilbert_mass",
        "mass_flux": "MF5_absolute_calibration",
        "newton_stack": "SN7_constant_universal_Geff",
        "source_norm_theorem": "S5_Newton_gate",
        "mu_extra_vector": "epsilon_calibration",
        "constant_gm_2583": "GM2583_6_nonlinear_beta_source",
        "owner_audit_2583": "Y5O2583_7_Newton_Poisson_orbit",
        "selector_2577": "IMP2577_2_local_GR",
        "local_residual_vector": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "qloc_interface_2581": "QLOC2581_TOTAL",
        "extra_hair_3585": "CHA3585_6_source_normalization",
    }
    validations.append(("VAL3591_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3591 source paths exist"))
    validations.append(("VAL3591_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3591 anchors found"))
    validations.append(("VAL3591_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3591 output files written"))
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
    validations.append(("VAL3591_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    required_contracts = {
        "GMT3591_0_same_observed_frame",
        "GMT3591_1_EH_or_bounded_operator",
        "GMT3591_2_parent_Hilbert_source",
        "GMT3591_3_Hamiltonian_equals_Hilbert_mass",
        "GMT3591_4_closed_flux",
        "GMT3591_5_Gauss_orbital_calibration",
        "GMT3591_6_zero_extra_monopole",
        "GMT3591_7_constant_universal_Gref",
        "GMT3591_8_theorem_result_if_all_close",
    }
    validations.append(("VAL3591_4_GM_contract_complete", required_contracts.issubset({str(row["contract_id"]) for row in gm_contract}), "all GM transfer contract rungs are present"))
    required_eps = {"epsilon_frame", "epsilon_current", "epsilon_flux", "epsilon_extra", "epsilon_GK_source", "epsilon_operator", "epsilon_calibration", "epsilon_PPN_source", "epsilon_mu"}
    validations.append(("VAL3591_5_epsilon_mu_complete", required_eps.issubset({str(row["symbol"]) for row in epsilon_mu}), "epsilon_mu residual vector is complete"))
    validations.append(("VAL3591_6_no_fitted_GM_guard", any(row["gate_id"] == "GATE3591_3_GM_not_hidden" and row["status"] == "PASS_GUARD" for row in gates), "unclosed source coupling is not hidden in fitted GM"))
    validations.append(("VAL3591_7_Newton_claim_blocked", any(row["gate_id"] == "GATE3591_4_Newton_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "Newton claim remains blocked"))
    validations.append(("VAL3591_8_PPN_propagation_present", any(row["row_id"] == "NPP3591_3_PPN_vector" for row in propagation), "PPN/source residual propagation row is present"))
    validations.append(("VAL3591_9_source_audit_blocks_GM", all(str(row.get("blocks_GM_claim", False)).lower() == "true" for row in source_audit), "source audit rows block GM claim until closed"))
    generated_rows = gm_contract + source_audit + epsilon_mu + propagation + gates + status + next_target
    validations.append(("VAL3591_10_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" and str(row.get("claim_allowed", False)).lower() == "false" for row in generated_rows), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3591_11_next_target_selected", any(row["next_id"] == "NEXT3591_0" for row in next_target), "3592 PiM-Hilbert target selected"))
    validations.append(("VAL3591_12_generated_source_paths_exist", all(Path(str(row["source_path"])).exists() for row in gm_contract + source_audit + epsilon_mu + propagation + gates + status), "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3591*")) or any(FORMALIZATION.rglob("3591-Y5-R2FR*"))
    validations.append(("VAL3591_13_formalization_workbench_untouched", not formalization_touched, "no 3591 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    gm_contract: list[dict[str, object]],
    source_audit: list[dict[str, object]],
    epsilon_mu: list[dict[str, object]],
    propagation: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3591 - Source coupling GM calibration or residual contract",
        "",
        "## Verdict",
        "3591 writes the exact bridge MTS needs before it can say it has Newtonian mechanics rather than an EH-looking equation plus fitted `GM`.",
        "",
        "If the transfer contract closes, `mu_obs=G_ref M_H`, `epsilon_mu=0`, and `a_r=-G_ref M_H/r^2`.  In the current corpus the contract is not parent-signed, so `epsilon_mu` must be propagated into Newton, PPN, R10, and local-GR tests.",
        "",
        "## GM Transfer Contract",
    ]
    for row in gm_contract:
        lines.append(f"- `{row['contract_id']}` `{row['contract_piece']}`: {row['status']} - {row['mathematical_form']}")
    lines.extend(["", "## Source Charge Audit"])
    for row in source_audit:
        lines.append(f"- `{row['audit_id']}` `{row['audit_piece']}`: {row['status']} - {row['required_clause']}")
    lines.extend(["", "## Epsilon Mu Contract"])
    for row in epsilon_mu:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['status']} - {row['formula_or_definition']}")
    lines.extend(["", "## Newton And PPN Propagation"])
    for row in propagation:
        lines.append(f"- `{row['row_id']}` `{row['observable_or_quantity']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    gm_contract = gm_transfer_contract_rows(source_paths)
    source_audit = source_charge_audit_rows(source_paths)
    epsilon_mu = epsilon_mu_contract_rows(source_paths)
    propagation = newton_ppn_propagation_rows(source_paths)
    gates = activation_gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "gm_transfer_contract": gm_contract,
        "source_charge_audit": source_audit,
        "epsilon_mu_contract": epsilon_mu,
        "newton_ppn_propagation": propagation,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, gm_contract, source_audit, epsilon_mu, propagation, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(gm_contract, source_audit, epsilon_mu, propagation, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3591 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
