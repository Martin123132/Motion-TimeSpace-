from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_observed_frame_tau_coframe_lock_contract_written_parent_signature_still_blocked_nonclaim"
CLAIM_CEILING = "observed_frame_tau_coframe_contract_only_no_MH_ref_denominator_no_Qbar_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "685-Y5-R10-tau-generator-Killing-clock-lock-or-frame-residual-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "432_doc": ROOT / "432-same-frame-matter-functor-zero-route.md",
    "447_doc": ROOT / "447-no-species-source-charge-one-coframe-theorem-attempt.md",
    "same_coframe_clause": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
    "same_coframe_variation": RESIDUALS / "P8_Y5_SAME_COFRAME_VARIATION_DERIVATION.csv",
    "same_coframe_bound": RESIDUALS / "P8_Y5_SAME_COFRAME_BOUND_UPDATE.csv",
    "623_doc": ROOT / "623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md",
    "623_validation": RESIDUALS / "P8_Y5_BRR545_623_VALIDATION.csv",
    "623_factorization": RESIDUALS / "P8_Y5_R10_623_FACTORIZATION_GATE.csv",
    "624_doc": ROOT / "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md",
    "624_validation": RESIDUALS / "P8_Y5_BRR545_624_VALIDATION.csv",
    "624_signature": RESIDUALS / "P8_Y5_R10_624_PARENT_SIGNATURE_AUDIT.csv",
    "633_doc": ROOT / "633-Y5-R10-parent-matter-frame-source-search-or-zero-branch-closure.md",
    "633_validation": RESIDUALS / "P8_Y5_BRR545_633_VALIDATION.csv",
    "633_zero_gate": RESIDUALS / "P8_Y5_R10_633_ZERO_BRANCH_CLOSURE_GATE.csv",
    "636_doc": ROOT / "636-Y5-R10-zero-clause-covariance-and-constants-repair-or-finite-input-sourcing.md",
    "636_validation": RESIDUALS / "P8_Y5_BRR545_636_VALIDATION.csv",
    "636_no_shadow": RESIDUALS / "P8_Y5_R10_636_NO_SHADOW_FRAME_GATE.csv",
    "636_constants": RESIDUALS / "P8_Y5_R10_636_CONSTANT_OWNERSHIP_AUDIT.csv",
    "637_doc": ROOT / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
    "637_validation": RESIDUALS / "P8_Y5_BRR545_637_VALIDATION.csv",
    "637_obs_functor": RESIDUALS / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv",
    "637_constant_status": RESIDUALS / "P8_Y5_R10_637_CONSTANT_STATUS_UPDATE.csv",
    "638_doc": ROOT / "638-Y5-R10-constant-sector-zero-or-finite-beta-derivation.md",
    "638_validation": RESIDUALS / "P8_Y5_BRR545_638_VALIDATION.csv",
    "638_constant_verdict": RESIDUALS / "P8_Y5_R10_638_CONSTANT_VERDICT.csv",
    "639_doc": ROOT / "639-Y5-R10-finite-constant-beta-local-bound-matrix-runner.md",
    "639_validation": RESIDUALS / "P8_Y5_BRR545_639_VALIDATION.csv",
    "639_symbol_table": RESIDUALS / "P8_Y5_R10_639_CONSTANT_BETA_SYMBOL_TABLE.csv",
    "662_doc": ROOT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
    "662_validation": RESIDUALS / "P8_Y5_BRR545_662_VALIDATION.csv",
    "662_parent_clause": RESIDUALS / "P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
    "663_doc": ROOT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
    "663_validation": RESIDUALS / "P8_Y5_BRR545_663_VALIDATION.csv",
    "663_chain": RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
    "683_doc": ROOT / "683-Y5-R10-MH-ref-same-frame-denominator-or-Qedge-numerator-source.md",
    "683_validation": RESIDUALS / "P8_Y5_BRR545_683_VALIDATION.csv",
    "683_same_frame_gate": RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
    "683_mh_attempt": RESIDUALS / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "hamiltonian_measure_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "432_doc": "same-frame matter functor zero route",
        "447_doc": "one-coframe not sufficient for source-charge theorem",
        "same_coframe_clause": "machine one-coframe parent clauses",
        "same_coframe_variation": "same-coframe variation derivation rows",
        "same_coframe_bound": "same-coframe bound update rows",
        "623_doc": "observed coframe factorization lemma",
        "623_validation": "623 validation gate",
        "623_factorization": "factorization gate rows",
        "624_doc": "parent signature audit for coframe factorization",
        "624_validation": "624 validation gate",
        "624_signature": "parent signature audit rows",
        "633_doc": "matter-frame source hunt",
        "633_validation": "633 validation gate",
        "633_zero_gate": "zero branch closure gates",
        "636_doc": "covariance/no-shadow/constants repair",
        "636_validation": "636 validation gate",
        "636_no_shadow": "no-shadow frame gate",
        "636_constants": "constant ownership audit",
        "637_doc": "parent quotient/Obs partial derivation",
        "637_validation": "637 validation gate",
        "637_obs_functor": "observed functor derivation rows",
        "637_constant_status": "constant status rows",
        "638_doc": "constant sector zero or finite beta derivation",
        "638_validation": "638 validation gate",
        "638_constant_verdict": "constant verdict rows",
        "639_doc": "finite constant beta bound matrix",
        "639_validation": "639 validation gate",
        "639_symbol_table": "missing kappa/beta/tau symbol table",
        "662_doc": "Hilbert/worldtube source-measure glue",
        "662_validation": "662 validation gate",
        "662_parent_clause": "same-object parent clause audit",
        "663_doc": "Euler/Ward chain and PiM blocker",
        "663_validation": "663 validation gate",
        "663_chain": "Euler/Ward chain rows",
        "683_doc": "M_H_ref denominator predecessor checkpoint",
        "683_validation": "683 validation gate",
        "683_same_frame_gate": "same-frame GM gates",
        "683_mh_attempt": "M_H_ref denominator attempt rows",
        "boundary_reference_status": "M_H_ref claim-valid status",
        "hamiltonian_measure_contract": "Hamiltonian source-measure contract",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": bool_text(source_path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, source_path in SOURCE_PATHS.items()
    ]


def frame_lock_contract_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "contract_id": "FLC684_0_single_observed_coframe",
            "object": "e_obs",
            "contract_statement": "e_source = e_clock = e_photon = e_ruler = e_orbit = e_obs on the local branch",
            "mathematical_form": "g_obs = eta_ab e_obs^a e_obs^b and every ordinary readout functional uses e_obs",
            "current_status": "conditional_clause_written_not_parent_derived",
            "what_it_would_buy": "removes frame/source/readout split as an independent denominator failure",
            "what_remains_open": "parent selector, constants, source charge, boundary/reference, and PPN/operator debts",
            "valid_for_claim": "false",
            "source_paths": source_list("same_coframe_clause", "432_doc", "623_doc", "624_doc"),
            "generated_utc": now,
        },
        {
            "contract_id": "FLC684_1_tau_from_observed_frame",
            "object": "tau_obs",
            "contract_statement": "the Hamiltonian time generator is the same observed clock/orbit/source time generator",
            "mathematical_form": "tau_source = tau_charge = tau_clock = tau_orbit = tau_obs[e_obs]",
            "current_status": "tau_lock_not_parent_signed",
            "what_it_would_buy": "allows H_tau and J_H[tau] to be compared to clock/orbit readout without a frame residual",
            "what_remains_open": "stationary/Killing normalization, boundary reference, and charge integrability",
            "valid_for_claim": "false",
            "source_paths": source_list("683_same_frame_gate", "663_chain", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
        {
            "contract_id": "FLC684_2_matter_descent",
            "object": "S_matter",
            "contract_statement": "ordinary matter descends through the observed quotient/coframe before local readout",
            "mathematical_form": "S_matter = sum_A S_A[psi_A, Obs(q(Phi)), omega[e_obs], theta_A]",
            "current_status": "conditional_descent_not_all_species_parent_signed",
            "what_it_would_buy": "kills direct vertical geometry pullback in the source current",
            "what_remains_open": "theta_A constants, material labels, source normalization, and boundary/domain charges",
            "valid_for_claim": "false",
            "source_paths": source_list("637_obs_functor", "638_constant_verdict", "447_doc"),
            "generated_utc": now,
        },
        {
            "contract_id": "FLC684_3_no_shadow_frame",
            "object": "representative Weyl/disformal frame",
            "contract_statement": "no A_g(Xhat), B_g(Xhat), or hidden clock/source frame is inserted after variation",
            "mathematical_form": "any matter-affecting frame map either factors through q or is finite-coupled and scored",
            "current_status": "classification_gate_written_not_parent_theorem",
            "what_it_would_buy": "prevents M_H_ref from being silently calibrated by a post-hoc frame map",
            "what_remains_open": "ordinary observable completeness is a parent principle, not a derived theorem",
            "valid_for_claim": "false",
            "source_paths": source_list("636_no_shadow", "624_signature", "633_zero_gate"),
            "generated_utc": now,
        },
        {
            "contract_id": "FLC684_4_Hilbert_source_before_GM",
            "object": "J_H[tau_obs]",
            "contract_statement": "source current is varied from S_matter with respect to e_obs before measured-GM/orbital fitting",
            "mathematical_form": "J_H[tau_obs] := (delta S_matter / delta e_obs) contracted with tau_obs",
            "current_status": "definition_conditional_not_source_measure_theorem",
            "what_it_would_buy": "separates source charge from fitted orbital mass",
            "what_remains_open": "dressed Hamiltonian charge equality and Poisson/Gauss/orbit calibration",
            "valid_for_claim": "false",
            "source_paths": source_list("same_coframe_clause", "662_parent_clause", "663_chain", "683_mh_attempt"),
            "generated_utc": now,
        },
        {
            "contract_id": "FLC684_5_readout_functor",
            "object": "clock/ruler/orbit readout",
            "contract_statement": "clock, ruler, photon, and slow-orbit readouts are functors of e_obs rather than independent calibration maps",
            "mathematical_form": "L_clock[e_obs], L_photon[e_obs], geodesic_orbit[g_obs], no e_clock/e_source split",
            "current_status": "conditional_support_only",
            "what_it_would_buy": "makes delta_frame_source a conditional zero under the one-coframe clause",
            "what_remains_open": "clock constants, EM constants, mass ratios, and source-normalization residuals",
            "valid_for_claim": "false",
            "source_paths": source_list("same_coframe_variation", "same_coframe_bound", "638_constant_verdict", "639_symbol_table"),
            "generated_utc": now,
        },
        {
            "contract_id": "FLC684_6_verdict",
            "object": "observed-frame lock",
            "contract_statement": "the exact frame-lock contract is written, but not parent-signed for current MTS",
            "mathematical_form": "e_obs and tau_obs can be the common denominator frame only after FLC684_0..FLC684_5 are derived together",
            "current_status": "blocked_nonclaim",
            "what_it_would_buy": "one major M_H_ref blocker would close",
            "what_remains_open": "M_H_ref, Qbar, R10, PPN, clocks, orbital, and local GR claims",
            "valid_for_claim": "false",
            "source_paths": source_list("683_doc", "boundary_reference_status"),
            "generated_utc": now,
        },
    ]


def tau_generator_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "TGA684_0_source_tau",
            "tau_role": "source variation",
            "required_identity": "tau used in J_H[tau] is selected before orbital fitting",
            "current_state": "definition_conditional",
            "blocker": "MISSING_PARENT_SELECTED_TAU_SOURCE",
            "impact_on_MH_ref": "source charge not yet tied to observed time",
            "valid_for_claim": "false",
            "source_paths": source_list("same_coframe_clause", "662_parent_clause"),
            "generated_utc": now,
        },
        {
            "audit_id": "TGA684_1_charge_tau",
            "tau_role": "Hamiltonian charge",
            "required_identity": "same tau makes delta H_tau integrable with fixed reference",
            "current_state": "not_derived_for_current_MTS",
            "blocker": "MISSING_INTEGRABLE_CHARGE_AND_REFERENCE_LOCK",
            "impact_on_MH_ref": "H_tau cannot define stable denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("hamiltonian_measure_contract", "663_chain", "683_same_frame_gate"),
            "generated_utc": now,
        },
        {
            "audit_id": "TGA684_2_clock_tau",
            "tau_role": "clock readout",
            "required_identity": "clock standards use the same tau_obs and e_obs as source variation",
            "current_state": "constants_and_clock_ratios_open",
            "blocker": "MISSING_CLOCK_CONSTANT_SILENCE",
            "impact_on_MH_ref": "clock/source comparison can retain alpha_EM/mass/transition drift",
            "valid_for_claim": "false",
            "source_paths": source_list("638_constant_verdict", "639_symbol_table", "same_coframe_bound"),
            "generated_utc": now,
        },
        {
            "audit_id": "TGA684_3_orbit_tau",
            "tau_role": "orbital readout",
            "required_identity": "slow-orbit geodesic readout uses the same g_obs and tau_obs as H_tau",
            "current_state": "Poisson_Gauss_orbit_not_parent_derived",
            "blocker": "MISSING_POISSON_GAUSS_ORBITAL_READOUT",
            "impact_on_MH_ref": "GM_orbit/G_ref remains empirical readout, not denominator proof",
            "valid_for_claim": "false",
            "source_paths": source_list("683_same_frame_gate", "663_chain"),
            "generated_utc": now,
        },
        {
            "audit_id": "TGA684_4_boundary_reference_tau",
            "tau_role": "boundary/reference",
            "required_identity": "H_ref and boundary counterterms are fixed using the same tau_obs",
            "current_state": "reference_boundary_lock_open",
            "blocker": "MISSING_FIXED_REFERENCE_TAU_BOUNDARY_CLASS",
            "impact_on_MH_ref": "reference shift can contaminate denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
        {
            "audit_id": "TGA684_5_stationary_generator",
            "tau_role": "local stationary/Killing normalization",
            "required_identity": "tau_obs is the stationary exterior generator normalized to observed clocks at the boundary",
            "current_state": "not_constructed",
            "blocker": "MISSING_LOCAL_STATIONARY_KILLING_OR_CLOCK_LOCK",
            "impact_on_MH_ref": "charge normalization remains conventional",
            "valid_for_claim": "false",
            "source_paths": source_list("662_doc", "663_doc", "683_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "TGA684_6_total",
            "tau_role": "all tau roles",
            "required_identity": "source, charge, clock, orbit, and boundary tau are one parent-selected generator",
            "current_state": "blocked_nonclaim",
            "blocker": "NO_PARENT_SIGNED_TAU_LOCK",
            "impact_on_MH_ref": "M_H_ref remains conditional",
            "valid_for_claim": "false",
            "source_paths": source_list("683_same_frame_gate", "same_coframe_clause", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
    ]


def mh_ref_impact_map_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "impact_id": "MHI684_0_frame_split",
            "object": "delta_frame_source",
            "if_frame_lock_passes": "conditional zero for source/readout frame split",
            "current_result": "not_promoted",
            "remaining_MH_ref_debt": "charge integrability, H_ref, M_H_ref positivity, Poisson/Gauss/orbit",
            "claim_effect": "supporting condition only",
            "valid_for_claim": "false",
            "source_paths": source_list("same_coframe_bound", "683_same_frame_gate"),
            "generated_utc": now,
        },
        {
            "impact_id": "MHI684_1_Hilbert_source_current",
            "object": "J_H[tau_obs]",
            "if_frame_lock_passes": "source current becomes same-frame before orbital calibration",
            "current_result": "definition_guardrail_only",
            "remaining_MH_ref_debt": "dressed Noether/Hamiltonian equality and radial closure",
            "claim_effect": "no measured-GM proof",
            "valid_for_claim": "false",
            "source_paths": source_list("662_parent_clause", "663_chain", "683_mh_attempt"),
            "generated_utc": now,
        },
        {
            "impact_id": "MHI684_2_GM_candidate",
            "object": "GM_orbit/G_ref",
            "if_frame_lock_passes": "anti-circularity blocker is reduced, not removed",
            "current_result": "empirical_readout_only",
            "remaining_MH_ref_debt": "Poisson/Gauss/orbit derivation plus constant universal G and extra-sector silence",
            "claim_effect": "cannot fill M_H_ref denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("683_mh_attempt", "hamiltonian_measure_contract"),
            "generated_utc": now,
        },
        {
            "impact_id": "MHI684_3_Qbar",
            "object": "Qbar_edge_XH(lambda)",
            "if_frame_lock_passes": "denominator frame becomes less ambiguous",
            "current_result": "still_blocked",
            "remaining_MH_ref_debt": "M_H_ref not claim-ready and Q_edge numerator still missing",
            "claim_effect": "no Qbar or alpha_edge claim",
            "valid_for_claim": "false",
            "source_paths": source_list("683_doc", "boundary_reference_status"),
            "generated_utc": now,
        },
    ]


def constant_and_source_residual_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "residual_id": "CSR684_0_alpha_EM",
            "channel": "EM/fine-structure constants",
            "frame_lock_effect": "does not close",
            "remaining_residual": "kappa_alpha = d ln alpha_EM / dXhat unless topological/quotient-owned",
            "why_it_matters": "clocks, spectra, WEP, and charge-sector coupling",
            "valid_for_claim": "false",
            "source_paths": source_list("638_constant_verdict", "639_symbol_table"),
            "generated_utc": now,
        },
        {
            "residual_id": "CSR684_1_mass_ratios",
            "channel": "particle masses/binding/composition",
            "frame_lock_effect": "does not close",
            "remaining_residual": "beta_A from mass-ratio and binding sensitivities",
            "why_it_matters": "source/test charge, WEP, R10, and orbital normalization",
            "valid_for_claim": "false",
            "source_paths": source_list("638_constant_verdict", "447_doc"),
            "generated_utc": now,
        },
        {
            "residual_id": "CSR684_2_clock_ratios",
            "channel": "clock transitions",
            "frame_lock_effect": "only supplies comparison frame",
            "remaining_residual": "tau_clock and kappa_clock remain until constants are parent-owned",
            "why_it_matters": "redshift/clock tests can still see nonmetric drift",
            "valid_for_claim": "false",
            "source_paths": source_list("638_constant_verdict", "same_coframe_bound"),
            "generated_utc": now,
        },
        {
            "residual_id": "CSR684_3_source_normalization",
            "channel": "measured GM/source charge",
            "frame_lock_effect": "necessary support, not proof",
            "remaining_residual": "delta_GM, mu_extra, source_normalization_residual",
            "why_it_matters": "M_H_ref and local Newton/PPN cannot be claimed",
            "valid_for_claim": "false",
            "source_paths": source_list("638_constant_verdict", "hamiltonian_measure_contract", "boundary_reference_status"),
            "generated_utc": now,
        },
    ]


def claim_gate_evaluation_rows(
    frame_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    claim_rows = [
        row
        for row in frame_rows + tau_rows + impact_rows + residual_rows
        if row.get("valid_for_claim") == "true"
    ]
    return [
        {
            "evaluation_id": "CGE684_0_frame_lock",
            "target": "observed frame/coframe lock",
            "status": "contract_written_not_parent_signed",
            "reason": "one-coframe clauses exist, but parent selector and no-shadow/constant conditions remain open",
            "claim_effect": "no same-frame theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE684_1_tau_lock",
            "target": "tau_obs generator",
            "status": "blocked_nonclaim",
            "reason": "source, Hamiltonian, clock, orbit, and boundary tau roles are not one parent-signed generator",
            "claim_effect": "M_H_ref denominator remains unsafe",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE684_2_constants",
            "target": "constant/source channels",
            "status": "still_open",
            "reason": "alpha_EM, mass ratios, clocks, source normalization, and measured GM remain finite/theorem targets",
            "claim_effect": "frame lock alone cannot close WEP/clock/R10/orbital/PPN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE684_3_claim_guard",
            "target": "684 generated rows",
            "status": "pass_nonclaim",
            "reason": f"generated_claim_rows={len(claim_rows)}",
            "claim_effect": "no M_H_ref, Qbar, R10, PPN, orbital, or local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D684_0_frame_contract",
            "target": "observed e_obs frame",
            "result": "conditional_contract_only",
            "reason": "same-frame/coframe clauses are sharp but not parent-selected for current MTS",
            "next_action": "do not promote same-frame theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D684_1_tau_generator",
            "target": "tau_obs",
            "result": "hard_next_hinge",
            "reason": "even if e_obs is accepted, the Hamiltonian generator needs stationary/clock/boundary normalization",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D684_2_MH_ref",
            "target": "M_H_ref",
            "result": "still_blocked",
            "reason": "frame lock would remove one blocker but not integrability, reference, positivity, constants, extra channels, or Poisson/Gauss/orbit",
            "next_action": "keep denominator nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S684_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "observed-frame tau/coframe contract written; parent signature still blocked",
            "blocked_claims": "M_H_ref;Qbar;alpha_edge;R10;PPN;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def boundary_reference_mh_ref_claim_ready() -> bool:
    status_path = SOURCE_PATHS["boundary_reference_status"]
    if not status_path.exists():
        return False
    for source_row in read_csv(status_path):
        if source_row.get("quantity") == "M_H_ref":
            return (
                source_row.get("valid_for_claim") == "true"
                and source_row.get("claim_valid_data_rows") not in {"", "0"}
            )
    return False


def validation_rows(
    source_register: list[dict[str, str]],
    frame_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [source_row["source_id"] for source_row in source_register if source_row["exists"] != "true"]
    rows.append({
        "check_id": "V684_0_source_paths_exist",
        "result": "pass" if not missing_sources else "fail",
        "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
        "generated_utc": now,
    })

    validation_ids = [
        "623_validation",
        "624_validation",
        "633_validation",
        "636_validation",
        "637_validation",
        "638_validation",
        "639_validation",
        "662_validation",
        "663_validation",
        "683_validation",
    ]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({
        "check_id": "V684_1_prior_validations_clean",
        "result": "pass" if all(failure_count == 0 for failure_count in prior_failures.values()) else "fail",
        "detail": ";".join(f"{source_id}={failure_count}" for source_id, failure_count in prior_failures.items()),
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V684_2_frame_contract_complete",
        "result": "pass" if len(frame_rows) >= 7 else "fail",
        "detail": f"frame_rows={len(frame_rows)}",
        "generated_utc": now,
    })

    required_tau_roles = ["source variation", "Hamiltonian charge", "clock readout", "orbital readout", "boundary/reference", "local stationary/Killing normalization"]
    observed_tau_roles = {source_row["tau_role"] for source_row in tau_rows}
    missing_tau_roles = [role for role in required_tau_roles if role not in observed_tau_roles]
    rows.append({
        "check_id": "V684_3_tau_roles_audited",
        "result": "pass" if not missing_tau_roles else "fail",
        "detail": "all required tau roles audited" if not missing_tau_roles else "missing_roles=" + ";".join(missing_tau_roles),
        "generated_utc": now,
    })

    tau_claim_rows = [source_row for source_row in tau_rows if source_row["valid_for_claim"] == "true"]
    rows.append({
        "check_id": "V684_4_tau_lock_not_promoted",
        "result": "pass" if not tau_claim_rows and any("MISSING" in source_row["blocker"] for source_row in tau_rows) else "fail",
        "detail": f"tau_rows={len(tau_rows)};claim_rows={len(tau_claim_rows)}",
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V684_5_MH_ref_not_claim_ready",
        "result": "pass" if not boundary_reference_mh_ref_claim_ready() else "fail",
        "detail": "boundary reference status has no claim-ready M_H_ref row",
        "generated_utc": now,
    })

    residual_open = all(source_row["valid_for_claim"] == "false" for source_row in residual_rows) and len(residual_rows) >= 4
    rows.append({
        "check_id": "V684_6_constant_source_residuals_retained",
        "result": "pass" if residual_open else "fail",
        "detail": f"residual_rows={len(residual_rows)}",
        "generated_utc": now,
    })

    impact_claim_rows = [source_row for source_row in impact_rows if source_row["valid_for_claim"] == "true"]
    rows.append({
        "check_id": "V684_7_MH_impact_nonclaim",
        "result": "pass" if not impact_claim_rows and len(impact_rows) >= 4 else "fail",
        "detail": f"impact_rows={len(impact_rows)};claim_rows={len(impact_claim_rows)}",
        "generated_utc": now,
    })

    generated_rows = frame_rows + tau_rows + impact_rows + residual_rows + claim_gate_rows + decision
    promoted_rows = [source_row for source_row in generated_rows if source_row.get("valid_for_claim") == "true"]
    rows.append({
        "check_id": "V684_8_no_claim_rows_promoted",
        "result": "pass" if not promoted_rows else "fail",
        "detail": "all generated 684 rows remain valid_for_claim=false" if not promoted_rows else f"claim_rows={len(promoted_rows)}",
        "generated_utc": now,
    })

    blocked_text = ";".join(";".join(source_row.values()) for source_row in generated_rows).lower()
    rows.append({
        "check_id": "V684_9_blocking_markers_retained",
        "result": "pass" if any(token in blocked_text for token in ["missing", "blocked", "not_parent", "not parent", "nonclaim"]) else "fail",
        "detail": "blocking markers retained",
        "generated_utc": now,
    })

    selected_rows = [source_row for source_row in decision if source_row["next_action"] == NEXT_TARGET]
    rows.append({
        "check_id": "V684_10_next_target_selected",
        "result": "pass" if selected_rows else "fail",
        "detail": NEXT_TARGET,
        "generated_utc": now,
    })

    output_paths = [
        RESIDUALS / "P8_Y5_R10_684_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
        RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_684_MH_REF_IMPACT_MAP.csv",
        RESIDUALS / "P8_Y5_R10_684_CONSTANT_AND_SOURCE_RESIDUALS.csv",
        RESIDUALS / "P8_Y5_R10_684_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_684_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_684_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_684_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({
        "check_id": "V684_11_generated_outputs_scoped",
        "result": "pass" if all(str(output_path).startswith(str(ROOT)) for output_path in output_paths) else "fail",
        "detail": "all 684 outputs target post-checkpoint-work",
        "generated_utc": now,
    })

    changed_count = formalization_changed_count()
    rows.append({
        "check_id": "V684_12_formalization_workbench_untouched",
        "result": "pass" if changed_count == 0 else "fail",
        "detail": f"formalization_changed_after_cutoff={changed_count}",
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V684_13_status_nonclaim",
        "result": "pass" if "no_MH_ref" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail",
        "detail": CLAIM_CEILING,
        "generated_utc": now,
    })

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for source_row in rows:
        rendered_values = [
            str(source_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        lines.append("| " + " | ".join(rendered_values) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    frame_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    impact_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 684 - Y5 R10 Observed Frame Tau Coframe Lock For MH Ref

## Verdict

684 writes the exact contract a future parent action must satisfy before `M_H_ref` can be treated as a same-frame denominator.

The necessary lock is:

```text
e_source = e_clock = e_photon = e_ruler = e_orbit = e_obs
tau_source = tau_charge = tau_clock = tau_orbit = tau_obs[e_obs]
J_H[tau_obs] := (delta S_matter / delta e_obs) contracted with tau_obs
M_H_ref := H_tau_obs[S_link] - H_ref
```

This is the right structure, but current MTS has not parent-signed it. One-coframe clauses exist only conditionally; `tau_obs` is not yet constructed as the same stationary/clock/Hamiltonian generator; and constants/source-normalization channels remain open. So `M_H_ref`, `Qbar`, `alpha_edge`, R10, PPN, orbital, and local-GR claims remain blocked.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## Frame Lock Contract

{markdown_table(frame_rows, ["contract_id", "object", "contract_statement", "mathematical_form", "current_status", "what_it_would_buy", "what_remains_open", "valid_for_claim"])}

## Tau Generator Audit

{markdown_table(tau_rows, ["audit_id", "tau_role", "required_identity", "current_state", "blocker", "impact_on_MH_ref", "valid_for_claim"])}

## MH Ref Impact Map

{markdown_table(impact_rows, ["impact_id", "object", "if_frame_lock_passes", "current_result", "remaining_MH_ref_debt", "claim_effect", "valid_for_claim"])}

## Constant And Source Residuals

{markdown_table(residual_rows, ["residual_id", "channel", "frame_lock_effect", "remaining_residual", "why_it_matters", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(claim_gate_rows, ["evaluation_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: construct or reject `tau_obs` itself. The next proof must show that the local stationary/Killing/clock generator used by clocks is the same generator used by the Hamiltonian charge and boundary reference. If not, fill a frame residual instead of using `M_H_ref` as a safe denominator.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    frame_rows = frame_lock_contract_rows()
    tau_rows = tau_generator_audit_rows()
    impact_rows = mh_ref_impact_map_rows()
    residual_rows = constant_and_source_residual_rows()
    claim_gate_rows = claim_gate_evaluation_rows(frame_rows, tau_rows, impact_rows, residual_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, frame_rows, tau_rows, impact_rows, residual_rows, claim_gate_rows, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_684_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv", frame_rows, ["contract_id", "object", "contract_statement", "mathematical_form", "current_status", "what_it_would_buy", "what_remains_open", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv", tau_rows, ["audit_id", "tau_role", "required_identity", "current_state", "blocker", "impact_on_MH_ref", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_684_MH_REF_IMPACT_MAP.csv", impact_rows, ["impact_id", "object", "if_frame_lock_passes", "current_result", "remaining_MH_ref_debt", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_684_CONSTANT_AND_SOURCE_RESIDUALS.csv", residual_rows, ["residual_id", "channel", "frame_lock_effect", "remaining_residual", "why_it_matters", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_684_CLAIM_GATE_EVALUATION.csv", claim_gate_rows, ["evaluation_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_684_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_684_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_684_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, frame_rows, tau_rows, impact_rows, residual_rows, claim_gate_rows, decision, validation)

    failures = [source_row for source_row in validation if source_row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"frame_rows={len(frame_rows)}")
    print(f"tau_rows={len(tau_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
