from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_TOPOLOGICAL_MASS_CURRENT_3574"
CHECKPOINT_ID = "3574"


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
        "handoff_3573": RESIDUALS / "P8_Y5_R2FR_3573_NEXT_TARGET.csv",
        "flux_fork_3573": RESIDUALS / "P8_Y5_R2FR_3573_PIM_FLUX_CLOSURE_FORK.csv",
        "drift_rows_3573": RESIDUALS / "P8_Y5_R2FR_3573_MEFF_DRIFT_RADIAL_BOUND_ROWS.csv",
        "status_3573": RESIDUALS / "P8_Y5_R2FR_3573_STATUS.csv",
        "pim_top_conditions": RESIDUALS / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv",
        "pim_top_parent_attempt": RESIDUALS / "P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv",
        "pim_top_failures": RESIDUALS / "P8_TOPOLOGICAL_PIM_FAILURE_ANALYSIS.csv",
        "pim_top_decision": RESIDUALS / "P8_TOPOLOGICAL_PIM_DECISION.csv",
        "hilbert_top_attempt": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "hilbert_top_obstructions": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
        "hilbert_top_decision": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_DECISION.csv",
        "bf_mass_candidate": RESIDUALS / "P8_Y5_R10_916_BF_MASS_CURRENT_CANDIDATE.csv",
        "mass_gauge_contract": RESIDUALS / "P8_Y5_R10_917_MASS_GAUGE_SOURCE_CONTRACT.csv",
        "ham_boundary_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "pim_jh_glue_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2180_PIM_JH_MASS_CURRENT_GLUE_AUDIT.csv",
        "parent_source_mass_audit": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
        "worldtube_clauses": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "worldtube_obstructions": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_OBSTRUCTIONS.csv",
        "worldtube_decision": RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_DECISION.csv",
        "hilbert_worldtube_theorem": RESIDUALS / "P8_Y5_R2FR_3423_HILBERT_WORLDTUBE_CLOSURE_THEOREM.csv",
        "poynting_bound": RESIDUALS / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv",
        "charge_residuals": RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "constant_gm_derivative": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "constant_gm_zero": RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "pg_gate": RESIDUALS / "P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3573": "declares the 3574 topological mass-current target",
        "flux_fork_3573": "imports the topological route and annulus flux law",
        "drift_rows_3573": "imports live Meff drift/radial fallback rows",
        "status_3573": "imports current closure status",
        "pim_top_conditions": "imports earlier topological PiM closure conditions",
        "pim_top_parent_attempt": "imports topological parent clause attempt",
        "pim_top_failures": "imports wrong-conserved-object failure analysis",
        "pim_top_decision": "imports prior topological PiM decision",
        "hilbert_top_attempt": "imports PiM Hilbert/topological equality attempt",
        "hilbert_top_obstructions": "imports equality obstructions",
        "hilbert_top_decision": "imports equality decision and best route",
        "bf_mass_candidate": "imports BF/closed-form mass current candidate",
        "mass_gauge_contract": "imports first-class mass-gauge source contract",
        "ham_boundary_contract": "imports Hamiltonian mass boundary charge contract",
        "pim_jh_glue_audit": "imports same-frame PiM/JH glue audit",
        "parent_source_mass_audit": "imports source-mass identity audit",
        "worldtube_clauses": "imports parent worldtube theorem clauses",
        "worldtube_obstructions": "imports worldtube obstruction ledger",
        "worldtube_decision": "imports parent worldtube route decision",
        "hilbert_worldtube_theorem": "imports Hilbert worldtube closure theorem attempt",
        "poynting_bound": "imports source-worldtube Poynting flux bound row",
        "charge_residuals": "imports charge-current residual decomposition",
        "constant_gm_derivative": "imports G/Meff derivative hair gate",
        "constant_gm_zero": "imports constant GM zero theorem attempt",
        "pg_gate": "imports Poisson/Gauss derive-or-fill gate",
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


def topological_origin_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "TOP3574_0_candidate_current",
            "closed topological current candidate",
            "J_M^top := Q_M omega_M^top + dB_M, with d omega_M^top=0, dQ_M=0 in the exterior, and d^2B_M=0.",
            "dJ_M^top=0 follows formally if Q_M and omega_M^top are parent-owned exterior data.",
            "FORMAL_CLOSED_CURRENT_AVAILABLE",
            "bf_mass_candidate",
            "This only conserves a topological object; it is not yet the measured Hilbert/Newton source.",
        ),
        (
            "TOP3574_1_parent_domain_selector",
            "parent domain and class selector",
            "The S2/worldtube class linking the compact source must be selected before readout and not by fitted orbital GM.",
            "Without this, Pi_M is a readout mask or preferred-domain selector rather than parent geometry.",
            "NOT_PARENT_SIGNED",
            "pim_top_parent_attempt",
            "No claim of exterior topological mass conservation as physical source.",
        ),
        (
            "TOP3574_2_same_source_charge",
            "same-source Hilbert charge",
            "Q_M must be defined from the same observed-frame Hilbert source worldtube as J_H, not introduced as an independent cohomology label.",
            "This is the only clean way to avoid conserving the wrong object.",
            "KEY_BLOCKER_NOT_DERIVED",
            "hilbert_top_decision",
            "The proof cannot promote J_M^top to Pi_M J_H.",
        ),
        (
            "TOP3574_3_first_class_origin",
            "independent gauge/BF origin",
            "A_M or Lambda_M may impose J_M^top-Pi_M J_H-dB_zero=0 only if its constraint is first-class/topological before Newton fitting.",
            "A late equality multiplier is just a Newton-closure axiom wearing a hat.",
            "CLOSURE_ONLY_IF_NOT_INDEPENDENT",
            "mass_gauge_contract",
            "Equality glue remains closure-only.",
        ),
        (
            "TOP3574_4_boundary_silence",
            "zero exact/boundary compact flux",
            "The exact term dB_zero and owner currents must have zero compact-boundary mass flux or a declared universal constant calibration.",
            "Otherwise topological equality hides mu_extra or radial mass hair.",
            "FAIL_OPEN",
            "hilbert_top_obstructions",
            "Boundary/improvement residuals remain live.",
        ),
        (
            "TOP3574_5_exchange_silence",
            "no extra projected exchange",
            "Pi_M dJ_extra must vanish for hidden, domain, non-EH, memory, range, Poynting, boundary, and source-owner flux channels.",
            "Poynting/wave/source-worldtube flux is retained as a physical background-field channel unless bounded or derived zero.",
            "NOT_DERIVED",
            "poynting_bound",
            "Extra source-current residuals remain live.",
        ),
        (
            "TOP3574_6_calibration_guard",
            "closed current to measured GM",
            "Even after closure, Q_M or int_S Pi_M J_H must reduce to EH/Poisson/Gauss/orbital mass with constant universal G_ref.",
            "Conservation is not the same as Newtonian measured-GM normalization.",
            "NOT_PARENT_DERIVED",
            "ham_boundary_contract",
            "No Newton/local-GR promotion from 3574.",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "origin_id": origin_id,
            "claim_piece": claim_piece,
            "candidate_or_condition": condition,
            "derivation_status": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "consequence": consequence,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for origin_id, claim_piece, condition, derivation, status, source_key, consequence in specs
    ]


def equality_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "EQ3574_0_decomposition",
            "topological/Hilbert decomposition",
            "Pi_M J_H = J_M^top + dB_zero + R_eq",
            "By definition R_eq measures all failure of the topological current to be the same object as the projected Hilbert source.",
            "EXACT_DEFINITION",
            "hilbert_top_attempt",
            "R_eq",
        ),
        (
            "EQ3574_1_closure_implication",
            "closure implication",
            "d(Pi_M J_H)=dJ_M^top + dR_eq = dR_eq when dJ_M^top=0",
            "Topological closure proves Hilbert flux closure only if dR_eq=0, or equivalently R_eq has zero annulus/boundary flux.",
            "DERIVED_IF_R_EQ_ZERO",
            "pim_top_conditions",
            "dR_eq",
        ),
        (
            "EQ3574_2_wrong_object_test",
            "wrong conserved object test",
            "J_M^top closed but R_eq != 0",
            "This branch conserves a topological charge while the measured mass source can still drift.",
            "FAILS_LOCAL_NEWTON_SOURCE",
            "pim_top_failures",
            "epsilon_Req_annulus",
        ),
        (
            "EQ3574_3_worldtube_glue_route",
            "best non-cheat source route",
            "Q_M := integral_W J_H[tau] and J_M^top := PD(W_source) Q_M before readout",
            "If the parent action supplies W_source, tau, e_obs, and source measure covariantly, then the topological charge and Hilbert source can be the same object.",
            "PROMISING_CONDITIONAL_NOT_SIGNED",
            "worldtube_clauses",
            "Z_worldtube_source_glue",
        ),
        (
            "EQ3574_4_hamiltonian_route",
            "Hamiltonian charge route",
            "B_xi/G_ref = Q_M = M_eff[Pi_M J_H]",
            "This would connect topological charge, Hilbert projected mass, and measured exterior charge, but requires integrability/reference/no-extra-charge gates.",
            "DOWNSTREAM_NOT_DERIVED",
            "ham_boundary_contract",
            "Delta_cal",
        ),
        (
            "EQ3574_5_poynting_flux_guard",
            "wave/Poynting source-owner guard",
            "epsilon_Poynting_worldtube enters R_eq or mu_extra unless its compact source-worldtube flux is zero or bounded.",
            "This keeps the user's Poynting-vector intuition in the math as a real exchange channel, not a vibes note.",
            "BOUND_ROW_PRESENT_INPUTS_MISSING",
            "poynting_bound",
            "epsilon_Poynting_worldtube",
        ),
        (
            "EQ3574_6_verdict",
            "3574 equality verdict",
            "Z_top_to_Hilbert := Z_closed_top * Z_same_source * Z_domain * Z_boundary * Z_exchange = 0 in the current corpus",
            "The formal topological current exists, but equality to Pi_M J_H is not parent-signed; R_eq rows must stay active.",
            "EQUALITY_NOT_CLAIMED",
            "hilbert_top_obstructions",
            "Z_top_to_Hilbert",
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
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "residual_symbol": residual_symbol,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, mathematical_form, derivation, status, source_key, residual_symbol in specs
    ]


def meff_drift_source_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "MEFF3574_0_R_eq_annulus",
            "epsilon_Req_annulus",
            "epsilon_Req_annulus := |int_A dR_eq|/|M_eff| with Pi_M J_H=J_M^top+dB_zero+R_eq",
            "dimensionless",
            "zero iff the topological/Hilbert equality residual has no annulus flux",
            "FORMULA_READY_PARENT_INTEGRAL_MISSING",
            "hilbert_top_attempt",
            "radial/time mass-source drift from wrong-object topological conservation",
        ),
        (
            "MEFF3574_1_B_zero_flux",
            "epsilon_Bzero_flux",
            "epsilon_Bzero_flux := |int_boundary dB_zero|/|M_eff|",
            "dimensionless",
            "zero iff the exact improvement has no compact-boundary monopole flux",
            "FORMULA_READY_BOUNDARY_INPUT_MISSING",
            "hilbert_top_obstructions",
            "boundary/improvement monopole shift",
        ),
        (
            "MEFF3574_2_source_worldtube_glue",
            "epsilon_Wsource_glue",
            "epsilon_Wsource_glue := |Q_M - integral_W J_H[tau]|/|M_eff|",
            "dimensionless",
            "zero iff Q_M is the same parent source charge as the Hilbert worldtube mass",
            "FORMULA_READY_SOURCE_MEASURE_MISSING",
            "worldtube_obstructions",
            "source-worldtube equality failure",
        ),
        (
            "MEFF3574_3_Poynting_worldtube",
            "epsilon_Poynting_worldtube",
            "epsilon_Poynting_worldtube := |int_W Pi_M dJ_Poynting|/|M_eff| or bounded by source-worldtube collar flux norm",
            "dimensionless after common mass-flux normalization",
            "zero or bound required before wave/Poynting exchange can be ignored",
            "BOUND_FORMULA_READY_INPUTS_MISSING",
            "poynting_bound",
            "Poynting/vector-wave source-owner flux",
        ),
        (
            "MEFF3574_4_dlnMeff_dt",
            "dln_Meff_dt",
            "dln_Meff_dt = D_t ln int_S Pi_M J_H = D_t ln int_S (J_M^top+dB_zero+R_eq)",
            "yr^-1 or s^-1 after declared time unit",
            "topological closure kills only the J_M^top part; R_eq/B_zero/exchange terms still need zero or data",
            "LIVE_FROM_3573_REFINED_BY_REQ",
            "drift_rows_3573",
            "Gdot/local GM drift",
        ),
        (
            "MEFF3574_5_partial_r_ln_mu_obs",
            "partial_r_ln_mu_obs",
            "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff[R_eq,B_zero,J_extra] + partial_r ln(1+epsilon_mu)",
            "m^-1, AU^-1, or dimensionless per declared radial interval",
            "radial source hair remains live until R_eq, boundary flux, exchange, and G_eff are closed",
            "LIVE_FROM_3573_REFINED_BY_REQ",
            "drift_rows_3573",
            "inverse-square/Newton radial source hair",
        ),
        (
            "MEFF3574_6_Delta_cal",
            "Delta_cal",
            "Delta_cal := M_eff[Pi_M J_H] - M_Gauss_orbital",
            "mass or dimensionless after division by M_eff",
            "even R_eq=0 does not set Newton's measured GM unless calibration and constant G_ref are signed",
            "CALIBRATION_GATE_STILL_OPEN",
            "ham_boundary_contract",
            "Poisson/Gauss/orbital source calibration",
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
            "zero_or_bound_condition": condition,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "observable_link": observable,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, units, condition, status, source_key, observable in specs
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3574_0_sources", "source audit", "PASS", "all required 3574 source paths exist"),
        ("GATE3574_1_closed_topological_current", "J_M^top closure", "PASS_FORMULA_NONCLAIM", "dJ_M^top=0 follows for closed parent topological data, but physical source identity is separate"),
        ("GATE3574_2_same_source_charge", "Q_M equals Hilbert source charge", "FAIL_CURRENT_CLAIM", "Q_M is not parent-signed as the same source-worldtube Hilbert charge"),
        ("GATE3574_3_equality_residual", "R_eq zero", "FAIL_CURRENT_CLAIM", "Pi_M J_H=J_M^top+dB_zero+R_eq is written, but R_eq=0 is not derived"),
        ("GATE3574_4_boundary_exchange", "boundary/exchange/Poynting silence", "FAIL_CURRENT_CLAIM", "B_zero, extra channels, and Poynting worldtube flux are unbounded or unsigned"),
        ("GATE3574_5_drift_rows", "Meff drift source rows", "PASS_NONCLAIM", "R_eq/B_zero/worldtube/Poynting/dlnMeff rows generated as non-claim source inputs"),
        ("GATE3574_6_Newton_claim", "Newton measured-GM", "FAIL_CURRENT_CLAIM", "constant G_ref and Poisson/Gauss/orbital calibration are still downstream gates"),
        ("GATE3574_7_local_GR_claim", "local GR", "FAIL_CURRENT_CLAIM", "no PPN/local-GR promotion follows from a closed wrong object"),
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
            "source_path": str(source_paths["status_3573"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3574_0_topological_current_kept",
            "keep the topological current as a real candidate, not a discarded route",
            "A closed BF/cohomological current is mathematically legal and cleanly metric-silent in shape.",
            "It remains useful if future parent action defines Q_M from the same Hilbert source worldtube.",
            "ADOPTED_NONCLAIM",
            "bf_mass_candidate",
        ),
        (
            "DEC3574_1_no_wrong_object_promotion",
            "do not promote J_M^top closure to Newton/source closure",
            "The main danger is conserving a beautiful topological object that is not the measured source mass.",
            "R_eq is now the named failure variable rather than a vague missing coupling.",
            "ADOPTED",
            "pim_top_failures",
        ),
        (
            "DEC3574_2_Poynting_retained",
            "retain Poynting/wave flux as a source-owner residual",
            "If EM/wave momentum flux rides the background field, it belongs in R_eq or mu_extra until a zero theorem or bound exists.",
            "This widens the search instead of trying once and calling it dead.",
            "ADOPTED",
            "poynting_bound",
        ),
        (
            "DEC3574_3_next_target",
            "next derive R_eq=0 through source-worldtube/Hamiltonian glue or start filling residual rows",
            "The best route is no longer generic topology; it is the same-object theorem Q_M=integral_W J_H[tau]=B_xi/G_ref.",
            "3575 should attack the source-worldtube/Hamiltonian glue chain directly, then fall back to numeric/source rows if it fails.",
            "NEXT_TARGET_SELECTED",
            "worldtube_decision",
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
            "status": "TOPOLOGICAL_CURRENT_FORMAL_CLOSURE_FOUND_EQUALITY_NOT_CLAIMED_REQ_ROWS_ACTIVE",
            "strongest_result": "A closed topological mass current can be written, and the exact decomposition Pi_M J_H=J_M^top+dB_zero+R_eq shows precisely what must vanish for topological closure to become Hilbert/source closure.",
            "still_missing": "parent-signed same-source Q_M, covariant worldtube/domain selector, independent first-class equality origin, zero B_zero boundary flux, zero projected exchange/Poynting flux, constant G_ref, and measured-GM calibration",
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
            "next_id": "NEXT3574_0",
            "target_doc": "3575-Y5-R2FR-Req-zero-source-worldtube-Hamiltonian-glue-or-residual-fill.md",
            "target_script": "scripts/Y5_R2FR_3575_Req_zero_source_worldtube_Hamiltonian_glue_or_residual_fill.py",
            "objective": "try to prove R_eq=0 by deriving the same-object chain Q_M=integral_W J_H[tau]=B_xi/G_ref in one parent branch; if not, fill source-backed R_eq/B_zero/Poynting/Meff drift rows",
            "success_gate": "parent-signed same-source worldtube/Hamiltonian charge equality with zero boundary/exchange flux, or source-backed residual inputs",
            "reason": "3574 shows generic topological closure is too weak; the missing leap is equality to the same observed Hilbert source charge",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "topological_mass_current_to_Hilbert_source_glue",
            "status": "FORMAL_TOPOLOGICAL_CURRENT_YES_HILBERT_EQUALITY_NO",
            "closure_formula": "dJ_M^top=0",
            "equality_formula": "Pi_M J_H=J_M^top+dB_zero+R_eq",
            "drift_formula": "d(Pi_M J_H)=dR_eq when dJ_M^top=0",
            "next_action": "derive R_eq=0 from source-worldtube/Hamiltonian same-object glue or fill residual rows",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    origin: list[dict[str, object]],
    equality: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3574_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3574 source paths exist"))
    needles = {
        "handoff_3573": "NEXT3573_0",
        "flux_fork_3573": "FLUX3573_2_topological_route",
        "drift_rows_3573": "DRIFT3573_0_dlnMeff_dt",
        "status_3573": "PIM_FLUX_CLOSURE_FORK_DERIVED",
        "pim_top_conditions": "TC500_3_Hilbert_equality",
        "pim_top_parent_attempt": "TP500_3_Hilbert_equality_gate",
        "pim_top_failures": "F500_0_conserved_wrong_object",
        "pim_top_decision": "D500_1_Hilbert_equality",
        "hilbert_top_attempt": "EH501_0_equality_statement",
        "hilbert_top_obstructions": "OB501_0_independent_topological_label",
        "hilbert_top_decision": "D501_1_best_route",
        "bf_mass_candidate": "BF916_0_closed_form_current",
        "mass_gauge_contract": "MGC917_0_parent_field",
        "ham_boundary_contract": "HC4_charge_equals_PiM_Hilbert_mass",
        "pim_jh_glue_audit": "MCG2180_5_success_package",
        "parent_source_mass_audit": "PSM2921_5_same_object_lemma",
        "worldtube_clauses": "W504_4_worldtube_source_measure_glue",
        "worldtube_obstructions": "O504_0_wrong_conserved_object",
        "worldtube_decision": "D504_0_best_route",
        "hilbert_worldtube_theorem": "HWC3423_6_verdict",
        "poynting_bound": "SWP3249_0_source_worldtube_Poynting_bound",
        "charge_residuals": "Delta_flux",
        "constant_gm_derivative": "CGM1_time_drift",
        "constant_gm_zero": "Z2_calibrated_PiM_flux_conservation",
        "pg_gate": "P8_Meff_conservation",
    }
    validations.append(("VAL3574_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3574 source-current needles found"))
    validations.append(("VAL3574_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3574 output files written"))
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
    validations.append(("VAL3574_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3574_4_closed_top_current_present", any(row["origin_id"] == "TOP3574_0_candidate_current" and "dJ_M^top=0" in str(row["derivation_status"]) for row in origin), "formal closed topological current row present"))
    validations.append(("VAL3574_5_Req_decomposition_present", any(row["gate_id"] == "EQ3574_0_decomposition" and "R_eq" in str(row["mathematical_form"]) for row in equality), "R_eq decomposition present"))
    validations.append(("VAL3574_6_closure_implication_present", any(row["gate_id"] == "EQ3574_1_closure_implication" and "d(Pi_M J_H)" in str(row["mathematical_form"]) for row in equality), "d(Pi_M J_H)=dR_eq implication present"))
    validations.append(("VAL3574_7_residual_rows_present", {"epsilon_Req_annulus", "epsilon_Bzero_flux", "epsilon_Poynting_worldtube", "dln_Meff_dt", "partial_r_ln_mu_obs"}.issubset({str(row["symbol"]) for row in residuals}), "R_eq/boundary/Poynting/Meff residual rows present"))
    validations.append(("VAL3574_8_equality_not_claimed", any(row["gate_id"] == "GATE3574_3_equality_residual" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "R_eq zero remains unclaimed"))
    validations.append(("VAL3574_9_next_target_selected", any(row["decision_id"] == "DEC3574_3_next_target" for row in decisions), "source-worldtube/Hamiltonian glue next target selected"))
    validations.append(("VAL3574_10_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in origin + equality + residuals + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in origin + equality + residuals + gates + decisions)
    validations.append(("VAL3574_11_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3574*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3574_12_formalization_workbench_untouched", not formalization_touched, "no 3574 checkpoint output appears in formalization-workbench"))
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
    origin: list[dict[str, object]],
    equality: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3574 - Topological mass-current origin or Meff drift source row",
        "",
        "## Verdict",
        "3574 gets a real step forward, not just another missing-list: a closed topological mass current is easy to write, but the exact obstruction is now named.",
        "",
        "`J_M^top := Q_M omega_M^top + dB_M` gives `dJ_M^top=0` if the parent action owns `Q_M`, `omega_M^top`, and the exterior class.  The decisive equality is",
        "",
        "`Pi_M J_H = J_M^top + dB_zero + R_eq`.",
        "",
        "Therefore, in the closed-topological branch, `d(Pi_M J_H)=dR_eq`.  So topological closure only becomes Hilbert/Newton source closure if `R_eq=0` or at least has zero annulus and compact-boundary flux.  Current corpus does not prove that.",
        "",
        "This is not a dead end.  It sharpens the coupling hunt: the missing object is the same-source glue `Q_M = integral_W J_H[tau] = B_xi/G_ref`, with boundary, Poynting/wave, extra-sector, and calibration terms either zero or source-bounded.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Topological current origin"])
    for row in origin:
        lines.append(f"- `{row['origin_id']}`: {row['candidate_or_condition']} ({row['status']})")
    lines.extend(["", "## Equality gate"])
    for row in equality:
        lines.append(f"- `{row['gate_id']}` `{row['residual_symbol']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Drift/source rows"])
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
    origin = topological_origin_rows(source_paths)
    equality = equality_gate_rows(source_paths)
    residuals = meff_drift_source_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3574_SOURCE_REGISTER.csv",
        "topological_origin": RESIDUALS / "P8_Y5_R2FR_3574_TOPOLOGICAL_MASS_CURRENT_ORIGIN_ATTEMPT.csv",
        "equality_gate": RESIDUALS / "P8_Y5_R2FR_3574_JMTOP_EQUALS_PIMJH_GATE.csv",
        "drift_source_rows": RESIDUALS / "P8_Y5_R2FR_3574_MEFF_DRIFT_SOURCE_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3574_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3574_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3574_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3574_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_topological_mass_current_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3574_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["topological_origin"], origin)
    write_csv(outputs["equality_gate"], equality)
    write_csv(outputs["drift_source_rows"], residuals)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, origin, equality, residuals, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, origin, equality, residuals, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3574 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
