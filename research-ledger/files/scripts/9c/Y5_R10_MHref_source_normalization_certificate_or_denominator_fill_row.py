from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_MHref_source_normalization_certificate_conditional_not_parent_signed_denominator_fill_row_unfilled_nonclaim"
CLAIM_CEILING = "MHref_source_normalization_certificate_only_no_MHref_value_no_BTF_value_no_epsilon_TF_no_PPN_score_no_R10_no_local_GR_claim"
NEXT_TARGET = "698-Y5-R10-Hamiltonian-charge-to-Poisson-Gauss-MHref-calibration-or-residual-bound.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "697-Y5-R10-MHref-source-normalization-certificate-or-denominator-fill-row.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "545_doc": ROOT / "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
    "546_doc": ROOT / "546-Y5-parent-action-boundary-reference-clause-search-or-residual-score.md",
    "547_doc": ROOT / "547-Y5-boundary-reference-residual-input-template-and-local-lock-map.md",
    "548_doc": ROOT / "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "659_doc": ROOT / "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md",
    "662_doc": ROOT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
    "663_doc": ROOT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
    "664_doc": ROOT / "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md",
    "665_doc": ROOT / "665-Y5-R10-fill-or-prove-FB554-0-Hamiltonian-integrability-reference-row.md",
    "666_doc": ROOT / "666-Y5-R10-parent-boundary-reference-lock-or-FB554-0-source-value-hunt.md",
    "683_doc": ROOT / "683-Y5-R10-MH-ref-same-frame-denominator-or-Qedge-numerator-source.md",
    "684_doc": ROOT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
    "685_doc": ROOT / "685-Y5-R10-tau-generator-Killing-clock-lock-or-frame-residual-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "548_validation": RESIDUALS / "P8_Y5_BRR545_548_VALIDATION.csv",
    "657_validation": RESIDUALS / "P8_Y5_BRR545_657_VALIDATION.csv",
    "659_validation": RESIDUALS / "P8_Y5_BRR545_659_VALIDATION.csv",
    "683_validation": RESIDUALS / "P8_Y5_BRR545_683_VALIDATION.csv",
    "684_validation": RESIDUALS / "P8_Y5_BRR545_684_VALIDATION.csv",
    "685_validation": RESIDUALS / "P8_Y5_BRR545_685_VALIDATION.csv",
    "696_validation": RESIDUALS / "P8_Y5_BRR545_696_VALIDATION.csv",
    "mac545_contract": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
    "brc547_template": RESIDUALS / "P8_Y5_BRR545_THEOREM_CERTIFICATE_TEMPLATE.csv",
    "bri547_template": RESIDUALS / "P8_Y5_BRR545_INPUT_TEMPLATE.csv",
    "hilbert_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "hsm_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "657_cmu_fill": RESIDUALS / "P8_Y5_R10_657_CMU_SOURCE_NORMALIZATION_FILL.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "659_closure": RESIDUALS / "P8_Y5_R10_659_CLOSURE_IDENTITY.csv",
    "659_obstructions": RESIDUALS / "P8_Y5_R10_659_OBSTRUCTION_AUDIT.csv",
    "683_denominator": RESIDUALS / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
    "683_same_frame_gate": RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
    "684_impact": RESIDUALS / "P8_Y5_R10_684_MH_REF_IMPACT_MAP.csv",
    "685_impact": RESIDUALS / "P8_Y5_R10_685_MH_REF_IMPACT.csv",
    "696_denominator_audit": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
    "696_same_frame": RESIDUALS / "P8_Y5_R10_696_SAME_FRAME_CONTRACT.csv",
    "696_fill": RESIDUALS / "P8_Y5_R10_696_FIRST_DENOMINATOR_FILL_ROW.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
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


def first_row_with(rows: list[dict[str, str]], field: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(field) == value:
            return row
    return {}


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
        "545_doc": "MAC545 sufficient contract including positive measured denominator clause",
        "546_doc": "MAC545 ownership search and measured-denominator gap queue",
        "547_doc": "BRR545 denominator certificate template",
        "548_doc": "boundary reference certificate attempt and first bound fill predecessor",
        "657_doc": "source-normalization family and eight-channel c_mu decomposition",
        "659_doc": "projected Hilbert mass-flux closure identity",
        "662_doc": "Hilbert worldtube source-measure glue predecessor",
        "663_doc": "minimal parent-action source-current Euler/Ward test predecessor",
        "664_doc": "Hamiltonian-PiM integrability/source equality predecessor",
        "665_doc": "Hamiltonian integrability/reference row predecessor",
        "666_doc": "parent boundary-reference lock/source value hunt predecessor",
        "683_doc": "M_H_ref denominator attempt and anti-circularity rule",
        "684_doc": "observed frame tau/coframe lock predecessor",
        "685_doc": "tau generator/Killing clock lock predecessor",
        "696_doc": "same-frame denominator/product-bound guard predecessor",
        "548_validation": "548 validation gate",
        "657_validation": "657 validation gate",
        "659_validation": "659 validation gate",
        "683_validation": "683 validation gate",
        "684_validation": "684 validation gate",
        "685_validation": "685 validation gate",
        "696_validation": "696 validation gate",
        "mac545_contract": "minimal action denominator clause MAC545_6",
        "brc547_template": "measured-GM denominator theorem certificate template",
        "bri547_template": "BRR545 denominator input template",
        "hilbert_contract": "Hilbert monopole/source-normalization calibration contract",
        "pg_contract": "Hamiltonian charge to Poisson/Gauss/orbital calibration contract",
        "hsm_contract": "Hamiltonian source-measure pass-condition contract",
        "657_cmu_fill": "exact c_mu source-normalization decomposition",
        "657_channels": "eight source-normalization residual channels",
        "659_closure": "closed PiM flux conditional identity",
        "659_obstructions": "PiM flux obstruction audit",
        "683_denominator": "prior M_H_ref denominator attempt",
        "683_same_frame_gate": "same-frame GM gate from 683",
        "684_impact": "tau/coframe impact on M_H_ref",
        "685_impact": "tau generator impact on M_H_ref",
        "696_denominator_audit": "current M_H_ref denominator blockers",
        "696_same_frame": "same-frame denominator contract",
        "696_fill": "first denominator fill row from 696",
        "boundary_reference_status": "claim-valid M_H_ref status",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def certificate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "SNC697_0_charge_definition",
            "M_H_ref := H_tau[S_link] - H_ref",
            "delta H_tau is integrable and H_ref is fixed once",
            "HSM541_1 and MH683_0 remain not parent-derived",
            "fail_missing_integrable_charge_and_fixed_reference",
            "without this, M_H_ref is a named functional not a stable denominator",
            "hsm_contract;683_denominator;664_doc;665_doc",
        ),
        (
            "SNC697_1_observed_generator",
            "one observed time generator tau_obs owns source, charge, clocks, and orbit",
            "tau_source=tau_charge=tau_clock=tau_orbit with delta tau=0 in charge variation",
            "SFG683_0 and 685 impact rows say tau is not locked",
            "fail_missing_tau_lock",
            "prevents charge mass from being the measured orbital denominator",
            "683_same_frame_gate;685_impact;684_doc;685_doc",
        ),
        (
            "SNC697_2_same_coframe_source",
            "one observed coframe/metric frame owns Hilbert source, rods, clocks, and orbit",
            "S_matter[e_obs] produces J_H[e_obs] and the same e_obs defines orbital readout",
            "same-frame measure proof remains missing",
            "fail_missing_same_frame_source_certificate",
            "blocks frame-mixing denominator promotion",
            "683_same_frame_gate;684_impact;hilbert_contract",
        ),
        (
            "SNC697_3_positive_reference_mass",
            "M_H_ref is positive after reference subtraction",
            "source energy condition plus source-independent fixed H_ref imply M_H_ref>0",
            "positivity is conditional; reference shift and boundary flux remain open",
            "fail_missing_positive_reference_guard",
            "prevents safe division by M_H_ref",
            "mac545_contract;683_denominator;696_denominator_audit",
        ),
        (
            "SNC697_4_radial_closure",
            "the projected Hilbert mass charge is radially closed in the compact exterior",
            "d(Pi_M J_H)=0 or integral_A[-Pi_M dJ_extra+[d,Pi_M]J_H+A_parent]=0",
            "659 proves exact obstruction identity but not zero premises",
            "fail_missing_radial_closure",
            "allows radial/source hair to contaminate measured mass",
            "659_closure;659_obstructions;657_channels",
        ),
        (
            "SNC697_5_poisson_gauss_orbit",
            "the same charge sources Poisson/Gauss and pure inverse-square orbital acceleration",
            "nabla^2 Phi=4*pi*G_ref*rho_H and a_r=-G_ref*M_H_ref/r^2",
            "PG0-PG9 are conditional/not parent-derived",
            "fail_missing_PG_orbital_calibration",
            "GM_orbit/G_ref remains empirical readout, not a derived denominator",
            "pg_contract;hsm_contract;683_same_frame_gate",
        ),
        (
            "SNC697_6_universal_coupling",
            "G_ref/kappa is constant, universal, source-blind, range-blind, and frame-blind",
            "partial_t,r,A,lambda,frame G_ref=0",
            "constant universal coupling is conditional, not parent-derived",
            "fail_missing_universal_G_certificate",
            "prevents converting GM_orbit into M_H_ref without coupling residuals",
            "hilbert_contract;pg_contract;657_channels",
        ),
        (
            "SNC697_7_extra_sector_silence",
            "boundary, domain, bulk, memory, non-EH, species, time, and calibration source channels are zero or bounded",
            "mu_extra=sum_i mu_i is theorem-zero or every channel has a sourced bound",
            "657 decomposes channels exactly but leaves them unfilled",
            "fail_missing_extra_sector_silence",
            "hidden source-normalization channels could become the denominator",
            "657_cmu_fill;657_channels;659_obstructions",
        ),
        (
            "SNC697_8_second_order_followthrough",
            "the first-order source calibration survives beta/gamma/PPN order",
            "delta_beta_source=0 and gamma-1 branch uses the same denominator",
            "PG9/HM7 not derived and 696 blocks epsilon_TF",
            "fail_missing_PPN_followthrough",
            "Newton-looking denominator cannot become local-GR evidence",
            "hilbert_contract;pg_contract;696_denominator_audit",
        ),
        (
            "SNC697_9_verdict",
            "claim-ready M_H_ref source-normalization certificate",
            "SNC697_0 through SNC697_8 all pass with no MISSING markers",
            "multiple certificate clauses remain unsigned or conditional",
            "fail_current_corpus",
            "denominator fill row remains unfilled and nonclaim",
            "545_doc;683_doc;696_doc",
        ),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "claim_clause": claim_clause,
            "mathematical_form": mathematical_form,
            "observed_state": observed_state,
            "result": result,
            "claim_effect": claim_effect,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for certificate_id, claim_clause, mathematical_form, observed_state, result, claim_effect, source_ids in rows
    ]


def conditional_derivation_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "step_id": "CD697_0_define_charge",
            "statement": "Define M_H_ref as the same-frame Hamiltonian/Hilbert source charge",
            "mathematical_step": "M_H_ref := H_tau[S_link]-H_ref = integral_S Pi_M J_H once H_tau is integrable",
            "requires_certificate_ids": "SNC697_0;SNC697_1;SNC697_2;SNC697_3",
            "if_premises_owned": "positive source denominator exists",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
            "source_paths": source_list("hsm_contract", "683_denominator"),
            "generated_utc": now,
        },
        {
            "step_id": "CD697_1_surface_independence",
            "statement": "Show the charge is independent of the linked enclosing surface",
            "mathematical_step": "int_A d(Pi_M J_H)=0 follows only if Pi_M dJ_extra=[d,Pi_M]J_H=A_parent=0",
            "requires_certificate_ids": "SNC697_4;SNC697_7",
            "if_premises_owned": "no radial mass drift or hidden source-normalization hair",
            "current_status": "conditional_obstruction_identity_only",
            "valid_for_claim": "false",
            "source_paths": source_list("659_closure", "659_obstructions"),
            "generated_utc": now,
        },
        {
            "step_id": "CD697_2_EH_poisson_limit",
            "statement": "Use the observed-frame weak-field equation to identify the Newtonian potential source",
            "mathematical_step": "g_00=-1+2 Phi/c^2 and nabla^2 Phi=4*pi*G_ref rho_H",
            "requires_certificate_ids": "SNC697_2;SNC697_5;SNC697_6",
            "if_premises_owned": "the Hilbert charge sources the same potential used by test bodies",
            "current_status": "conditional_PG_contract_only",
            "valid_for_claim": "false",
            "source_paths": source_list("pg_contract", "hilbert_contract"),
            "generated_utc": now,
        },
        {
            "step_id": "CD697_3_gauss_surface",
            "statement": "Convert the Poisson source into a surface/orbital monopole",
            "mathematical_step": "surface_integral grad Phi dot dS = 4*pi*G_ref M_H_ref",
            "requires_certificate_ids": "SNC697_4;SNC697_5;SNC697_6",
            "if_premises_owned": "GM coefficient is the same charge as M_H_ref",
            "current_status": "conditional_not_parent_derived",
            "valid_for_claim": "false",
            "source_paths": source_list("pg_contract", "683_same_frame_gate"),
            "generated_utc": now,
        },
        {
            "step_id": "CD697_4_orbital_readout",
            "statement": "Read the same monopole as pure inverse-square acceleration",
            "mathematical_step": "a_r=-G_ref M_H_ref/r^2 so GM_orbit=G_ref M_H_ref",
            "requires_certificate_ids": "SNC697_5;SNC697_6;SNC697_7",
            "if_premises_owned": "M_H_ref=GM_orbit/G_ref is a derived equality, not a borrowed definition",
            "current_status": "conditional_not_parent_derived",
            "valid_for_claim": "false",
            "source_paths": source_list("pg_contract", "683_denominator"),
            "generated_utc": now,
        },
        {
            "step_id": "CD697_5_claim_theorem",
            "statement": "Claim-ready denominator theorem",
            "mathematical_step": "SNC697_0...SNC697_8 => M_H_ref=GM_orbit/G_ref>0 in the same observed frame",
            "requires_certificate_ids": "SNC697_0;SNC697_1;SNC697_2;SNC697_3;SNC697_4;SNC697_5;SNC697_6;SNC697_7;SNC697_8",
            "if_premises_owned": "B_TF_over_MH denominator can be filled",
            "current_status": "not_claimed_current_corpus",
            "valid_for_claim": "false",
            "source_paths": source_list("545_doc", "683_doc", "696_doc"),
            "generated_utc": now,
        },
    ]


def anti_circularity_guard_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "ACG697_0_no_observed_GM_first",
            "GM_orbit/G_ref may not be inserted as M_H_ref before CD697_0 through CD697_4 are derived",
            "prevents borrowing Newton/orbits to prove Newton/source normalization",
            "guard_active",
            "683_denominator;pg_contract",
        ),
        (
            "ACG697_1_no_product_bound_denominator",
            "gamma product pressure cannot define M_H_ref or B_TF_over_MH",
            "prevents converting PPN bounds into a missing theory input",
            "guard_active",
            "696_doc;696_denominator_audit",
        ),
        (
            "ACG697_2_no_constant_offset_cheat",
            "absolute calibration offsets count only if parent-fixed universal and derivative-free",
            "prevents hiding source-normalization residuals inside G_ref or M_H_ref",
            "guard_active",
            "657_cmu_fill;657_channels;hilbert_contract",
        ),
        (
            "ACG697_3_no_cancellation_credit",
            "boundary/reference/source-normalization channels are summed as retained residuals unless individually zero/bounded",
            "prevents fragile cancellation proofs",
            "guard_active",
            "547_doc;657_channels;659_obstructions",
        ),
        (
            "ACG697_4_empirical_smoke_allowed_only_labelled",
            "a system-specific GM_orbit/G_ref row is allowed for private smoke only with valid_for_claim=false",
            "keeps engineering tests useful without becoming evidence",
            "guard_active",
            "683_denominator;696_fill",
        ),
    ]
    return [
        {
            "guard_id": guard_id,
            "rule": rule,
            "reason": reason,
            "current_status": current_status,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for guard_id, rule, reason, current_status, source_ids in rows
    ]


def denominator_fill_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fill_id": "MHR697_0_source_normalization_certificate_fill",
            "target_rows": "MHR696_0_first_M_H_ref_fill;BRC547_4_measured_GM_denominator;BRI547_3_denominator",
            "quantity": "M_H_ref",
            "candidate_law": "M_H_ref = H_tau[S_link]-H_ref = GM_orbit/G_ref only after certificate passes",
            "value": "MISSING_CERTIFIED_POSITIVE_M_H_REF",
            "units": "MISSING_MASS_OR_GM_UNITS",
            "positive_required": "true",
            "source_frame": "MISSING_OBSERVED_SOURCE_FRAME",
            "metric_frame": "MISSING_OBSERVED_METRIC_FRAME",
            "clock_frame": "MISSING_OBSERVED_CLOCK_FRAME",
            "boundary_domain": "MISSING_LINKED_SURFACE_DOMAIN",
            "counterterm_convention": "MISSING_FIXED_REFERENCE_CONVENTION",
            "measured_GM_link": "MISSING_DERIVED_GM_ORBIT_EQUALS_GREF_MHREF",
            "universal_G_certificate": "MISSING_CONSTANT_UNIVERSAL_GREF_CERTIFICATE",
            "radial_closure_certificate": "MISSING_RADIAL_CLOSURE_OR_PROFILE_BOUND",
            "extra_sector_silence_certificate": "MISSING_MU_EXTRA_ZERO_OR_CHANNEL_BOUNDS",
            "equation_ref": "MISSING_EQUATION_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "derivation_status": "unfilled_after_source_normalization_certificate_failure",
            "allowed_use_now": "private_smoke_template_only",
            "valid_for_claim": "false",
            "source_paths": source_list("696_fill", "brc547_template", "bri547_template", "683_denominator"),
            "generated_utc": now,
        }
    ]


def repair_queue_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "RQ697_0_PG_orbital_calibration",
            "SNC697_5_poisson_gauss_orbit",
            "highest",
            "it is the clean anti-circularity bridge from Hamiltonian charge to measured GM",
            NEXT_TARGET,
            "if it fails, retain a calibrated residual bound rather than filling M_H_ref",
            "pg_contract;hsm_contract",
        ),
        (
            "RQ697_1_integrability_reference",
            "SNC697_0_charge_definition;SNC697_3_positive_reference_mass",
            "high",
            "without an integrable fixed-reference charge there is no denominator functional",
            "derive H_tau integrability and fixed H_ref from the parent boundary action",
            "retain Delta_symp/reference residual",
            "664_doc;665_doc;666_doc",
        ),
        (
            "RQ697_2_tau_coframe_lock",
            "SNC697_1_observed_generator;SNC697_2_same_coframe_source",
            "high",
            "frame splitting can mimic source-normalization failure",
            "close tau/coframe observed-frame lock or keep frame residual",
            "retain frame/tau residual",
            "684_doc;685_doc;683_same_frame_gate",
        ),
        (
            "RQ697_3_radial_and_extra_silence",
            "SNC697_4_radial_closure;SNC697_7_extra_sector_silence",
            "medium",
            "hidden channels can contaminate the denominator even if PG works",
            "derive PiM flux closure and source-normalization channel zeros/bounds",
            "carry eight-channel c_mu envelope",
            "657_channels;659_closure;659_obstructions",
        ),
        (
            "RQ697_4_universal_G_and_PPN_followthrough",
            "SNC697_6_universal_coupling;SNC697_8_second_order_followthrough",
            "medium",
            "Newton recovery is not local GR unless coupling and PPN order survive",
            "derive constant G and second-order source stability",
            "retain Gdot/source-charge/beta/gamma residuals",
            "hilbert_contract;pg_contract;696_denominator_audit",
        ),
    ]
    return [
        {
            "repair_id": repair_id,
            "target_certificate": target_certificate,
            "priority": priority,
            "why": why,
            "next_action": next_action,
            "fallback_if_fails": fallback_if_fails,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for repair_id, target_certificate, priority, why, next_action, fallback_if_fails, source_ids in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "eval_id": "E697_0_certificate",
            "target": "M_H_ref source-normalization certificate",
            "observed_state": "conditional theorem chain written but certificate clauses are unsigned",
            "result": "fail_blocked",
            "claim_effect": "no claim-ready M_H_ref",
            "valid_for_claim": "false",
            "source_paths": source_list("683_denominator", "696_denominator_audit"),
            "generated_utc": now,
        },
        {
            "eval_id": "E697_1_derivation_chain",
            "target": "M_H_ref=GM_orbit/G_ref derivation",
            "observed_state": "valid only if charge, frame, radial closure, PG calibration, universal G, and extra-sector silence pass",
            "result": "conditional_only",
            "claim_effect": "useful theorem contract, not evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("conditional_derivation_self",) if False else source_list("pg_contract", "hsm_contract"),
            "generated_utc": now,
        },
        {
            "eval_id": "E697_2_fill_row",
            "target": "MHR697_0_source_normalization_certificate_fill",
            "observed_state": "MISSING_CERTIFIED_POSITIVE_M_H_REF and MISSING_DERIVED_GM_ORBIT_EQUALS_GREF_MHREF",
            "result": "unfilled_nonclaim",
            "claim_effect": "cannot feed B_TF_over_MH or epsilon_TF",
            "valid_for_claim": "false",
            "source_paths": source_list("696_fill", "brc547_template"),
            "generated_utc": now,
        },
        {
            "eval_id": "E697_3_next_route",
            "target": "PG/orbital calibration bridge",
            "observed_state": "PG0-PG9 conditional/not parent-derived",
            "result": "selected_next_target",
            "claim_effect": "attack the highest-value denominator bridge next",
            "valid_for_claim": "false",
            "source_paths": source_list("pg_contract", "683_same_frame_gate"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    gates = [
        ("CG697_0_integrable_charge", "integrable H_tau and fixed H_ref", "not_derived_for_current_MTS", "fail_blocked", "no stable M_H_ref functional", "hsm_contract"),
        ("CG697_1_tau_frame_lock", "same tau/coframe for source, clock, metric, and orbit", "MISSING_SAME_OBSERVED_TIME_GENERATOR", "fail_blocked", "no same-frame denominator", "683_same_frame_gate"),
        ("CG697_2_positive_mass", "M_H_ref>0 after fixed reference subtraction", "positivity_not_signed", "fail_blocked", "unsafe division by M_H_ref", "683_denominator"),
        ("CG697_3_radial_closure", "closed projected Hilbert mass flux", "conditional_theorem_proved_not_parent_signed", "fail_blocked", "radial/source hair remains", "659_closure"),
        ("CG697_4_PG_orbit", "GM_orbit=G_ref*M_H_ref derived in this order", "PG0-PG9 conditional or not parent-derived", "fail_blocked", "GM_orbit/G_ref is empirical readout only", "pg_contract"),
        ("CG697_5_universal_G", "constant universal G_ref", "conditional_not_parent_derived", "fail_blocked", "coupling drift/source dependence remains", "hilbert_contract"),
        ("CG697_6_extra_sector_silence", "mu_extra channels zero or bounded", "EXACT_SUM_RULE_NON_NUMERIC_CHANNELS_UNFILLED", "fail_blocked", "hidden denominator contamination remains", "657_cmu_fill"),
        ("CG697_7_PPN_followthrough", "second-order source stability", "not_derived", "fail_blocked", "no local-GR promotion", "pg_contract"),
        ("CG697_8_denominator_fill", "MHR697 row has no MISSING markers", "MISSING_CERTIFIED_POSITIVE_M_H_REF", "fail_blocked", "no B_TF/e_TF/R10/PPN score", "696_fill"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed_state,
            "result": result,
            "claim_effect": claim_effect,
            "valid_for_claim": "false",
            "source_paths": source_list(source_id),
            "generated_utc": now,
        }
        for gate_id, gate, observed_state, result, claim_effect, source_id in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D697_0_certificate_attempt",
            "target": "M_H_ref source-normalization certificate",
            "result": "conditional_chain_written_not_signed",
            "reason": "the exact proof shape exists, but integrability/reference, same frame, radial closure, PG/orbit, universal G, and source channels are not all parent-owned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D697_1_fill_row",
            "target": "M_H_ref denominator fill",
            "result": "unfilled",
            "reason": "filling GM_orbit/G_ref now would be circular because PG/orbital equality is not derived",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D697_2_next",
            "target": "Hamiltonian charge to Poisson/Gauss calibration",
            "result": "selected",
            "reason": "this is the cleanest route to turn the denominator from a symbol into a measured-GM theorem",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S697_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "M_H_ref has a precise conditional source-normalization theorem but no parent-signed certificate or fill value",
            "hardest_blocker": "deriving GM_orbit=G_ref*M_H_ref from Hamiltonian charge through Poisson/Gauss without borrowing the orbital readout",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, str]],
    certificate_rows_: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    anti_circularity_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "certificate": certificate_rows_,
        "derivation": derivation_rows,
        "anti_circularity": anti_circularity_rows,
        "fill": fill_rows,
        "repair": repair_rows,
        "evaluator": evaluator_rows_,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["548_validation", "657_validation", "659_validation", "683_validation", "684_validation", "685_validation", "696_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    boundary_status = first_row_with(read_csv(SOURCE_PATHS["boundary_reference_status"]), "quantity", "M_H_ref")
    certificate_complete = len(certificate_rows_) == 10 and all(row["valid_for_claim"] == "false" for row in certificate_rows_)
    certificate_fails = any(row["result"] == "fail_current_corpus" for row in certificate_rows_) and all(
        row["result"].startswith("fail") for row in certificate_rows_
    )
    derivation_conditional = len(derivation_rows) == 6 and all(row["valid_for_claim"] == "false" for row in derivation_rows)
    anti_circularity_active = len(anti_circularity_rows) == 5 and all(row["current_status"] == "guard_active" for row in anti_circularity_rows)
    fill_complete = len(fill_rows) == 1 and fill_rows[0]["valid_for_claim"] == "false"
    missing_fill_fields = [
        "value",
        "units",
        "source_frame",
        "metric_frame",
        "clock_frame",
        "boundary_domain",
        "counterterm_convention",
        "measured_GM_link",
        "universal_G_certificate",
        "radial_closure_certificate",
        "extra_sector_silence_certificate",
        "equation_ref",
        "source_path",
    ]
    fill_missing = all("MISSING_" in fill_rows[0][field] for field in missing_fill_fields)
    repair_selected = any(row["next_action"] == NEXT_TARGET for row in repair_rows)
    gates_block = len(gate_rows) == 9 and all(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    boundary_mhref_still_blocked = (
        boundary_status.get("claim_valid_data_rows") == "0"
        and boundary_status.get("valid_for_claim") == "false"
    )
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_697_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_697_MHREF_SOURCE_NORMALIZATION_CERTIFICATE.csv",
        RESIDUALS / "P8_Y5_R10_697_CONDITIONAL_DERIVATION_CHAIN.csv",
        RESIDUALS / "P8_Y5_R10_697_ANTI_CIRCULARITY_GUARD.csv",
        RESIDUALS / "P8_Y5_R10_697_DENOMINATOR_FILL_ROW.csv",
        RESIDUALS / "P8_Y5_R10_697_REPAIR_QUEUE.csv",
        RESIDUALS / "P8_Y5_R10_697_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_697_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_697_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_697_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_697_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V697_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V697_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V697_2_boundary_MHref_still_blocked", boundary_mhref_still_blocked, f"claim_valid_data_rows={boundary_status.get('claim_valid_data_rows', 'missing')};status={boundary_status.get('status', 'missing')}"),
        ("V697_3_certificate_complete_and_failed", certificate_complete and certificate_fails, f"certificate_rows={len(certificate_rows_)}"),
        ("V697_4_conditional_derivation_written", derivation_conditional, f"derivation_rows={len(derivation_rows)}"),
        ("V697_5_anti_circularity_guards_active", anti_circularity_active, f"guard_rows={len(anti_circularity_rows)}"),
        ("V697_6_denominator_fill_unfilled", fill_complete and fill_missing, "denominator fill row keeps missing markers"),
        ("V697_7_repair_queue_selects_next", repair_selected, NEXT_TARGET),
        ("V697_8_claim_gates_block", gates_block, f"gate_rows={len(gate_rows)}"),
        ("V697_9_no_claim_rows_promoted", no_claim_rows, "all generated 697 rows remain valid_for_claim=false"),
        ("V697_10_next_target_selected", next_selected, NEXT_TARGET),
        ("V697_11_generated_outputs_scoped", scoped_outputs, "all 697 outputs target post-checkpoint-work"),
        ("V697_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V697_13_status_nonclaim", "no_MHref_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(
    source_rows: list[dict[str, str]],
    certificate_rows_: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    anti_circularity_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    repair_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 697 - Y5 R10 MHref Source Normalization Certificate Or Denominator Fill Row

## Verdict

697 tries the clean route for the missing denominator:

```text
M_H_ref := H_tau[S_link] - H_ref
M_H_ref = GM_orbit / G_ref
```

but only if the equality is derived in the right order: Hamiltonian/Hilbert charge first, then same-frame weak-field Poisson/Gauss calibration, then orbital readout. That conditional proof chain can be written precisely.

The current corpus still does not sign the certificate. Integrability/reference lock, tau/coframe lock, positivity after reference subtraction, radial projected-mass closure, Poisson/Gauss/orbital calibration, universal `G_ref`, extra-sector silence, and second-order PPN followthrough all remain open. So `M_H_ref` is not filled.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## MHref Source Normalization Certificate

{markdown_table(certificate_rows_, ["certificate_id", "claim_clause", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Conditional Derivation Chain

{markdown_table(derivation_rows, ["step_id", "statement", "mathematical_step", "requires_certificate_ids", "current_status", "valid_for_claim"])}

## Anti-Circularity Guard

{markdown_table(anti_circularity_rows, ["guard_id", "rule", "reason", "current_status", "valid_for_claim"])}

## Denominator Fill Row

{markdown_table(fill_rows, ["fill_id", "quantity", "candidate_law", "value", "measured_GM_link", "universal_G_certificate", "valid_for_claim"])}

## Repair Queue

{markdown_table(repair_rows, ["repair_id", "target_certificate", "priority", "why", "next_action", "fallback_if_fails", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_rows_, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    certificate_rows_ = certificate_rows()
    derivation_rows = conditional_derivation_rows()
    anti_circularity_rows = anti_circularity_guard_rows()
    fill_rows = denominator_fill_rows()
    repair_rows = repair_queue_rows()
    evaluator_rows_ = evaluator_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        certificate_rows_,
        derivation_rows,
        anti_circularity_rows,
        fill_rows,
        repair_rows,
        evaluator_rows_,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_697_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_MHREF_SOURCE_NORMALIZATION_CERTIFICATE.csv", certificate_rows_, ["certificate_id", "claim_clause", "mathematical_form", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_CONDITIONAL_DERIVATION_CHAIN.csv", derivation_rows, ["step_id", "statement", "mathematical_step", "requires_certificate_ids", "if_premises_owned", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_ANTI_CIRCULARITY_GUARD.csv", anti_circularity_rows, ["guard_id", "rule", "reason", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_DENOMINATOR_FILL_ROW.csv", fill_rows, ["fill_id", "target_rows", "quantity", "candidate_law", "value", "units", "positive_required", "source_frame", "metric_frame", "clock_frame", "boundary_domain", "counterterm_convention", "measured_GM_link", "universal_G_certificate", "radial_closure_certificate", "extra_sector_silence_certificate", "equation_ref", "source_path", "derivation_status", "allowed_use_now", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_REPAIR_QUEUE.csv", repair_rows, ["repair_id", "target_certificate", "priority", "why", "next_action", "fallback_if_fails", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_EVALUATOR.csv", evaluator_rows_, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_697_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_697_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, certificate_rows_, derivation_rows, anti_circularity_rows, fill_rows, repair_rows, evaluator_rows_, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"certificate_rows={len(certificate_rows_)}")
    print(f"derivation_rows={len(derivation_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
