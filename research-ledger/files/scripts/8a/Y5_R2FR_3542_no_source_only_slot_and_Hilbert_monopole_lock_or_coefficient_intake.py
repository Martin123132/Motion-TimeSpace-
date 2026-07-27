from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3542-Y5-R2FR-no-source-only-slot-and-Hilbert-monopole-lock-or-coefficient-intake.md"
CANONICAL_STATUS = OUT / "P8_Y5_no_source_slot_Hilbert_monopole_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3542": {"path": Path(__file__).resolve(), "role": "3542 generator"},
    "doc_3541": {
        "path": ROOT / "3541-Y5-R2FR-Y5-Y6-source-coupling-lock-or-first-qloc-coefficients.md",
        "role": "Y5/Y6 source-coupling handoff",
    },
    "next_3541": {
        "path": OUT / "P8_Y5_R2FR_3541_NEXT_TARGET.csv",
        "role": "selected no-source-slot/Hilbert-monopole target",
    },
    "ceilings_3541": {
        "path": OUT / "P8_Y5_R2FR_3541_FIRST_QLOC_COEFFICIENT_CEILINGS.csv",
        "role": "numeric nonclaim ceilings to convert into intake rows",
    },
    "no_source_prefactor_2645": {
        "path": OUT / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv",
        "role": "no-source-prefactor parent clause and countermodel",
    },
    "no_source_projection_2645": {
        "path": OUT / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PROJECTION_REQUIREMENTS.csv",
        "role": "projection requirements for finite source coefficient rows",
    },
    "no_source_slot_2508": {
        "path": OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv",
        "role": "typed grammar/no-Hom no-source-only-slot attempt",
    },
    "no_source_gate_1902": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1902_NO_SOURCE_SLOT_GATE.csv",
        "role": "no-source slot gate and surviving blockers",
    },
    "hilbert_contract": {
        "path": OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "Hilbert monopole calibration contract",
    },
    "hamiltonian_source_measure": {
        "path": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "role": "Hamiltonian source measure contract",
    },
    "hilbert_source_contract": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1936_HILBERT_SOURCE_CONTRACT.csv",
        "role": "parent Hilbert source contract",
    },
    "hilbert_source_theorem": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv",
        "role": "conditional Hilbert source theorem",
    },
    "newton_stack": {
        "path": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
        "role": "source-normalized Newton branch stack",
    },
    "mu_extra_vector": {
        "path": OUT / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "mu_extra source-normalization coefficient vector",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "empirical WEP/PPN/Gdot/R10/R11 bounds",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def no_source_slot_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "NSS3542_0_target",
            "claim_piece": "NoSourceOnlyY5Slot",
            "formal_statement": "Allowed[S_matter] excludes w_A(Y5)S_A, kappa_A(Y5)T_A, source-only species weights, shifted source origins, and hidden marker covectors before variation.",
            "proof_step": "Make active-source coefficients untypeable, not merely set to zero.",
            "result": "TARGET_EXACT",
            "remaining_gap": "parent object grammar and constructor exhaustion are unsigned",
            "claim_allowed": "False",
        },
        {
            "proof_id": "NSS3542_1_typed_domain",
            "claim_piece": "source functor domain",
            "formal_statement": "SourceFunctor: StressTotal(e_obs) -> GeometrySource, not SourceFunctor: {(Stress_A,SpeciesLabel_A)} -> GeometrySource.",
            "proof_step": "Species labels enter stress-energy content only, not a gravitational-source coefficient slot.",
            "result": "EXACT_CONDITIONAL",
            "remaining_gap": "parent signature for StressTotal-only domain not derived",
            "claim_allowed": "False",
        },
        {
            "proof_id": "NSS3542_2_noHom",
            "claim_piece": "no active-source coefficient morphism",
            "formal_statement": "Hom_parent(SpeciesLabel,Coeff_active_source)=empty and Hom_parent(HiddenMarker,Coeff_active_source)=empty.",
            "proof_step": "If true, w_A and kappa_A cannot be written as parent terms.",
            "result": "EXACT_IF_PARENT_SORTS_SIGNED",
            "remaining_gap": "parent sorts and no-Hom theorem not signed",
            "claim_allowed": "False",
        },
        {
            "proof_id": "NSS3542_3_constructor_exhaustion",
            "claim_piece": "constructor list",
            "formal_statement": "Every coefficient entering S_matter is in Image(ParentGenerate[q(Phi),theta_rep,universal_constants]).",
            "proof_step": "This blocks hidden source-prefactor constructors after the visible quotient is fixed.",
            "result": "CORE_GAP",
            "remaining_gap": "constructor exhaustion is not derived from the corpus",
            "claim_allowed": "False",
        },
        {
            "proof_id": "NSS3542_4_action_measure_owner",
            "claim_piece": "single action/measure owner",
            "formal_statement": "All ordinary matter sectors share one parent action scale, one measure/Jacobian, and one Hilbert variation before readout.",
            "proof_step": "Pre-action weights cannot hide as species-dependent normalizations.",
            "result": "UNSIGNED",
            "remaining_gap": "action-scale/measure owner missing",
            "claim_allowed": "False",
        },
        {
            "proof_id": "NSS3542_5_countermodel",
            "claim_piece": "surviving legal countermodel",
            "formal_statement": "S_matter=sum_A w_A S_A is covariant, additive, and Ward-compatible, while T_source=sum_A w_A T_A.",
            "proof_step": "This proves Ward covariance does not remove source-only slots.",
            "result": "COUNTERMODEL_SURVIVES",
            "remaining_gap": "need parent grammar, not another Ward appeal",
            "claim_allowed": "False",
        },
        {
            "proof_id": "NSS3542_6_verdict",
            "claim_piece": "no-source-only theorem",
            "formal_statement": "NSS3542_1 through NSS3542_4 together imply partial S_matter/partial w_A is undefined.",
            "proof_step": "If signed, Y5 source-only leakage is structurally absent.",
            "result": "NOT_PARENT_DERIVED",
            "remaining_gap": "finite coefficient-intake rows remain required",
            "claim_allowed": "False",
        },
    ]


def monopole_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "HML3542_0_same_frame",
            "identity": "matter, clocks, source variation and orbital readout use one observed coframe",
            "mathematical_form": "e_obs=e_matter=e_source=e_orbit; delta_frame_source=0",
            "if_signed": "source coupling cannot hide in frame conversion",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "residual_if_failed": "eta_WEP_direct_geometry; alpha_clock_redshift; delta_frame_source",
            "claim_allowed": "False",
        },
        {
            "lock_id": "HML3542_1_Hilbert_current",
            "identity": "ordinary source is the Hilbert/coframe current from the same matter action",
            "mathematical_form": "J_H ~ T_H^{mu nu}=2/sqrt(-g) delta S_matter/delta g_munu",
            "if_signed": "ordinary matter has one variational source owner",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_FORCED",
            "residual_if_failed": "eta_source_AB; nonHilbert current residual",
            "claim_allowed": "False",
        },
        {
            "lock_id": "HML3542_2_Hamiltonian_equals_Hilbert",
            "identity": "Hamiltonian/Gauss charge equals projected Hilbert mass current",
            "mathematical_form": "B_tau/G_eff = M_eff[Pi_M J_H] and delta B_tau = delta integral_S Pi_M J_H",
            "if_signed": "the conserved geometric charge becomes the Newtonian source mass",
            "current_status": "CONTRACT_EXISTS_NOT_PARENT_DERIVED",
            "residual_if_failed": "dln_Meff_dt; mu_extra_boundary_bulk_domain; source-measure residual",
            "claim_allowed": "False",
        },
        {
            "lock_id": "HML3542_3_flux_closure",
            "identity": "projected mass flux is closed in compact exterior",
            "mathematical_form": "d(Pi_M J_H)=0; partial_t M_eff=0; partial_r M_eff=0 outside compact support",
            "if_signed": "no time/radial source hair or alpha3 mass flux",
            "current_status": "NOT_PARENT_DERIVED",
            "residual_if_failed": "Gdot_over_G; partial_r_ln_mu_obs; alpha3",
            "claim_allowed": "False",
        },
        {
            "lock_id": "HML3542_4_zero_mu_extra",
            "identity": "non-Hilbert monopole channels vanish or are scored",
            "mathematical_form": "mu_extra=mu_boundary+mu_bulk+mu_domain+mu_memory+mu_range+mu_connection=0 or mapped",
            "if_signed": "measured GM is not hiding boundary/domain/bulk physics",
            "current_status": "NOT_PARENT_DERIVED",
            "residual_if_failed": "R3/R4/R7/R8/R9/R10/R11 source-normalization rows",
            "claim_allowed": "False",
        },
        {
            "lock_id": "HML3542_5_Gauss_orbital",
            "identity": "same monopole controls Poisson/Gauss and inverse-square orbital readout",
            "mathematical_form": "nabla^2 Phi=4*pi*G_eff*rho_H; a_r=-G_eff*M_eff/r^2",
            "if_signed": "Newtonian mechanics is sourced by the same Hilbert mass",
            "current_status": "NOT_DERIVED",
            "residual_if_failed": "alpha(lambda); radial hair; orbital source projection",
            "claim_allowed": "False",
        },
        {
            "lock_id": "HML3542_6_verdict",
            "identity": "Hilbert monopole lock",
            "mathematical_form": "HML3542_0 through HML3542_5 hold in one parent action",
            "if_signed": "Y5 source normalization can be derived away for local Newton at first order",
            "current_status": "NOT_CLAIMED",
            "residual_if_failed": "coefficient-intake branch",
            "claim_allowed": "False",
        },
    ]


def coefficient_intake_rows() -> list[dict[str, Any]]:
    return [
        {
            "intake_id": "INT3542_0_species_source",
            "coefficient_symbol": "epsilon_species_A",
            "projection_formula": "eta_source_AB = |epsilon_species_A - epsilon_species_B| after common-mode GM removal",
            "required_inputs": "material source-basis vector for A/B; common-mode projector; no-cancellation rule; source path",
            "numeric_ceiling": "2.8e-15 if projection coefficient is one",
            "observable_rows": "R1_WEP_source_charge;R2_clock_redshift;R11_EH_operator_ledger",
            "source_bound": "local_bound_claims.csv:MICROSCOPE_final_TiPt_source_charge_proxy",
            "current_status": "PROJECTION_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "INT3542_1_beta_source",
            "coefficient_symbol": "delta_beta_source",
            "projection_formula": "beta_eff-1 = delta_beta_source + delta_beta_R11 + delta_beta_q_loc + delta_beta_boundary_domain + delta_beta_readout",
            "required_inputs": "second-order weak-field source coefficients A_source,B_source; no-cancellation component values; source path",
            "numeric_ceiling": "7.8e-5 under direct beta projection",
            "observable_rows": "R4_beta;R11_EH_operator_ledger",
            "source_bound": "local_bound_claims.csv:Will_2014_PPN_beta_table",
            "current_status": "PROJECTION_FORMULA_READY_SECOND_ORDER_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "INT3542_2_gamma_extra_stress",
            "coefficient_symbol": "delta_gamma_extra",
            "projection_formula": "gamma-1 = C_gamma^ij T_extra_ij + C_gamma^R11 c_R11 + C_gamma^q q_loc",
            "required_inputs": "weak-field metric solution or topological/improvement zero certificate; source path",
            "numeric_ceiling": "2.3e-5 under direct gamma projection",
            "observable_rows": "R3_gamma;R11_EH_operator_ledger",
            "source_bound": "local_bound_claims.csv:Cassini_Shapiro_gamma_2003",
            "current_status": "PROJECTION_FORMULA_READY_STRESS_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "INT3542_3_alpha3_flux",
            "coefficient_symbol": "C_alpha3_boundary_domain",
            "projection_formula": "alpha3 = C_alpha3^B B_GK + C_alpha3^D F_D + C_alpha3^q q_loc",
            "required_inputs": "boundary/domain flux components; projection coefficient; no-flux theorem or source path",
            "numeric_ceiling": "4e-20 under direct alpha3 projection",
            "observable_rows": "R7_alpha3;R11_EH_operator_ledger",
            "source_bound": "local_bound_claims.csv:Will_2014_PPN_alpha3_table",
            "current_status": "PROJECTION_FORMULA_READY_HIGHEST_PRESSURE_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "INT3542_4_xi_STF",
            "coefficient_symbol": "epsilon_STF_xi",
            "projection_formula": "xi = C_xi^ij T_STF_ij + C_xi^D epsilon_domain_anisotropy",
            "required_inputs": "STF stress projection; external-environment coupling; source path",
            "numeric_ceiling": "4e-9 under direct xi projection",
            "observable_rows": "R8_xi;R11_EH_operator_ledger",
            "source_bound": "local_bound_claims.csv:Will_2014_PPN_xi_table",
            "current_status": "PROJECTION_FORMULA_READY_STF_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "INT3542_5_time_drift",
            "coefficient_symbol": "epsilon_time_drift",
            "projection_formula": "Gdot/G = d ln G_eff/dt + d ln M_eff/dt + d ln(1+mu_extra/(G_eff M_eff))/dt",
            "required_inputs": "tau-normalized time derivative; stationary theorem or drift coefficient; source path",
            "numeric_ceiling": "9.6e-15 yr^-1 under direct Gdot projection",
            "observable_rows": "R9_Gdot;R11_EH_operator_ledger",
            "source_bound": "local_bound_claims.csv:LLR_Biskupek_Muller_Torre_2021",
            "current_status": "PROJECTION_FORMULA_READY_DRIFT_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "INT3542_6_R10_bulk_tail",
            "coefficient_symbol": "epsilon_bulk_X, lambda_X, alpha_X(lambda)",
            "projection_formula": "delta a/a_GR = alpha_X(lambda)(1+r/lambda_X) exp(-r/lambda_X)",
            "required_inputs": "Z_X; M_X^2; lambda_X=sqrt(Z_X/M_X^2); source charge; real alpha(lambda) curve",
            "numeric_ceiling": "curve-valued, not a scalar ceiling",
            "observable_rows": "R10_fifth_force;R11_EH_operator_ledger",
            "source_bound": "local_bound_claims.csv:Adelberger_Heckel_Nelson_2003_ISL_curve",
            "current_status": "PROJECTION_FORMULA_READY_CURVE_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "intake_id": "INT3542_7_R11_operator",
            "coefficient_symbol": "c_domain_source_normalization_operator;T_extra_operator_vector",
            "projection_formula": "Delta_PPN_i = sum_j M_ij c_R11_j with operator-specific units and weak-field maps",
            "required_inputs": "operator family, coefficient value/theorem, normalization, weak-field map, source artifact",
            "numeric_ceiling": "operator-family bound required",
            "observable_rows": "R11_EH_operator_ledger",
            "source_bound": "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
            "current_status": "PROJECTION_FORMULA_READY_OPERATOR_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3542_0_no_source_slot_exact_but_unsigned",
            "decision": "No-source-only Y5 slot is the correct proof target, but it is not derived from the current corpus.",
            "rationale": "The countermodel S_matter=sum_A w_A S_A remains covariant and Ward-compatible unless parent grammar forbids w_A.",
            "effect": "Stop using Ward conservation as source-coupling proof; use grammar or coefficients.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3542_1_Hilbert_monopole_chain_precise",
            "decision": "Hilbert/Gauss monopole lock is now expressed as a finite chain of required identities.",
            "rationale": "Local Newton needs the same Hilbert current to source Poisson/Gauss and orbital GM.",
            "effect": "The source-normalization route is concrete enough to attack clause-by-clause.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3542_2_coefficient_intake_upgraded",
            "decision": "3541 ceilings are converted into projection-formula intake rows.",
            "rationale": "This makes the fallback branch executable: each coefficient has observable rows, projection formula, and missing inputs.",
            "effect": "Next work can fill real values rather than restating missing coupling.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3542_3_next",
            "decision": "Attack constructor exhaustion or fill the first material/source projection coefficient.",
            "rationale": "Either w_A becomes untypeable, or the species/source coefficient must be scored against MICROSCOPE.",
            "effect": "3543 should choose between parent grammar proof and first coefficient fill.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3542_0_no_source_slot",
            "quantity": "no_source_only_Y5_slot",
            "value": "exact_conditional_countermodel_survives",
            "meaning": "source-only coefficients vanish only if parent grammar/no-Hom/constructor exhaustion is signed",
            "claim_effect": "Y5 not derived away yet",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3542_1_monopole",
            "quantity": "Hilbert_Gauss_monopole_lock",
            "value": "finite_chain_written_not_signed",
            "meaning": "same-frame Hilbert current, Hamiltonian charge, flux closure, zero mu_extra, and orbital Gauss readout must all hold",
            "claim_effect": "Newton source normalization not claimed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3542_2_intake",
            "quantity": "source_coefficient_intake",
            "value": "projection_formulas_ready_inputs_missing",
            "meaning": "ceilings now have projection formulas and required inputs for WEP/beta/gamma/alpha3/xi/Gdot/R10/R11",
            "claim_effect": "fallback branch more executable",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3542_3_next",
            "quantity": "next_best_target",
            "value": "constructor_exhaustion_or_species_coefficient_fill",
            "meaning": "prove w_A is untypeable or fill the first material/source projection coefficient",
            "claim_effect": "directly attacks source-coupling bottleneck",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3543-Y5-R2FR-constructor-exhaustion-or-first-species-source-coefficient-fill.md",
            "next_script": "scripts/Y5_R2FR_3543_constructor_exhaustion_or_first_species_source_coefficient_fill.py",
            "objective": "Try to prove parent constructor exhaustion/no-Hom makes species source coefficients untypeable; if not, fill the first species/source coefficient row with material projection inputs and MICROSCOPE-compatible normalization.",
            "success_gate": "Either source-only w_A is structurally impossible, or INT3542_0_species_source has concrete material vectors, projection normalization, and a score-ready nonclaim value.",
            "why_next": "3542 reduces Y5 to the exact source-slot seam and turns ceilings into intake rows; the first live branch is species/source charge.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    no_source: list[dict[str, Any]],
    monopole: list[dict[str, Any]],
    intake: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    proof_ids = {row["proof_id"] for row in no_source}
    lock_ids = {row["lock_id"] for row in monopole}
    intake_ids = {row["intake_id"] for row in intake}
    checks.append({"check_id": "VAL3542_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3542_1_no_source_slot_countermodel_kept", "passed": bool_text({"NSS3542_0_target", "NSS3542_2_noHom", "NSS3542_3_constructor_exhaustion", "NSS3542_5_countermodel", "NSS3542_6_verdict"} <= proof_ids), "detail": "no-source-slot theorem and countermodel rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3542_2_monopole_chain_complete", "passed": bool_text({"HML3542_0_same_frame", "HML3542_1_Hilbert_current", "HML3542_2_Hamiltonian_equals_Hilbert", "HML3542_3_flux_closure", "HML3542_4_zero_mu_extra", "HML3542_5_Gauss_orbital"} <= lock_ids), "detail": "same-frame, Hilbert, Hamiltonian, flux, mu_extra and Gauss clauses present", "valid_for_claim": "False"})
    required_intake = {"INT3542_0_species_source", "INT3542_1_beta_source", "INT3542_2_gamma_extra_stress", "INT3542_3_alpha3_flux", "INT3542_4_xi_STF", "INT3542_5_time_drift", "INT3542_6_R10_bulk_tail", "INT3542_7_R11_operator"}
    checks.append({"check_id": "VAL3542_3_intake_rows_cover_all_ceilings", "passed": bool_text(required_intake <= intake_ids), "detail": "WEP, beta, gamma, alpha3, xi, Gdot, R10 and R11 intake rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3542_4_projection_formulas_present", "passed": bool_text(all(row["projection_formula"] and "MISSING" in row["current_status"] for row in intake)), "detail": "each intake row has a projection formula and missing-input status", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3542_5_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3543-Y5-R2FR-constructor-exhaustion")), "detail": "3543 constructor/species coefficient target selected", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3542_6_no_claims_promoted", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + intake + status) and all(row.get("claim_allowed", "False") == "False" for row in no_source + monopole + decisions + next_rows)), "detail": "no local Newton/GR/source coupling claim promoted", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3542_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3542_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3542_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3542_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    no_source: list[dict[str, Any]],
    monopole: list[dict[str, Any]],
    intake: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3542 - No Source-Only Slot And Hilbert Monopole Lock Or Coefficient Intake

## Summary
- **No-source slot result:** the exact proof route is typed grammar/no-Hom/constructor exhaustion, not Ward conservation.
- **Countermodel retained:** `S_matter=sum_A w_A S_A` remains covariant and Ward-compatible unless the parent grammar makes `w_A` untypeable.
- **Hilbert monopole lock:** local Newton requires one chain: same frame, Hilbert current, Hamiltonian/Gauss equality, flux closure, zero `mu_extra`, and orbital Gauss readout.
- **Fallback upgraded:** the 3541 ceilings are now coefficient-intake rows with projection formulas, required inputs, source bounds, and nonclaim status.
- **Next hinge:** either prove constructor exhaustion, or fill the first species/source coefficient row against the MICROSCOPE source-charge ceiling.

## Core Theorem Shape
To derive `Y5` away, the parent action must forbid source-only slots:

`Hom_parent(SpeciesLabel,Coeff_active_source)=empty`

and every source coefficient must lie in

`Image(ParentGenerate[q(Phi),theta_rep,universal_constants])`.

Then a term like

`S_matter=sum_A w_A(Y5) S_A`

is not merely zero; it is not a well-typed parent term. That is the clean route. The current corpus has the contract, but the constructor-exhaustion premise is not signed.

For measured Newtonian source coupling, the required lock is

`B_tau/G_eff = M_eff[Pi_M J_H]`,

`d(Pi_M J_H)=0`,

`mu_extra=0`,

and

`nabla^2 Phi=4*pi*G_eff*rho_H`, `a_r=-G_eff M_eff/r^2`

in the same observed frame.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## No-Source-Slot Proof Attempt
{markdown_table(no_source, ["proof_id", "claim_piece", "formal_statement", "proof_step", "result", "remaining_gap", "claim_allowed"])}

## Hilbert Monopole Lock
{markdown_table(monopole, ["lock_id", "identity", "mathematical_form", "if_signed", "current_status", "residual_if_failed", "claim_allowed"])}

## Coefficient Intake Rows
{markdown_table(intake, ["intake_id", "coefficient_symbol", "projection_formula", "required_inputs", "numeric_ceiling", "observable_rows", "source_bound", "current_status", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    no_source = no_source_slot_rows()
    monopole = monopole_lock_rows()
    intake = coefficient_intake_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3542_SOURCE_REGISTER.csv",
        "no_source_slot": OUT / "P8_Y5_R2FR_3542_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv",
        "monopole_lock": OUT / "P8_Y5_R2FR_3542_HILBERT_MONOPOLE_LOCK.csv",
        "coefficient_intake": OUT / "P8_Y5_R2FR_3542_COEFFICIENT_INTAKE_ROWS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3542_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3542_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3542_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3542_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["no_source_slot"], no_source, ["proof_id", "claim_piece", "formal_statement", "proof_step", "result", "remaining_gap", "claim_allowed"])
    write_csv(outputs["monopole_lock"], monopole, ["lock_id", "identity", "mathematical_form", "if_signed", "current_status", "residual_if_failed", "claim_allowed"])
    write_csv(outputs["coefficient_intake"], intake, ["intake_id", "coefficient_symbol", "projection_formula", "required_inputs", "numeric_ceiling", "observable_rows", "source_bound", "current_status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, no_source, monopole, intake, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, no_source, monopole, intake, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
