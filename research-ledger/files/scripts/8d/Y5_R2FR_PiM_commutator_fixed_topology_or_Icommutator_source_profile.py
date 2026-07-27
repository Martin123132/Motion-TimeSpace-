from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1715"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md"

SOURCE_FILES = {
    "1714_doc": ROOT / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
    "1714_validation": OUT / "P8_Y5_BRR545_1714_VALIDATION.csv",
    "1714_next": OUT / "P8_Y5_PARENT_QLOC_1714_NEXT_TARGET.csv",
    "1714_residuals": OUT / "P8_Y5_PARENT_QLOC_1714_REQ_ICOMMUTATOR_RESIDUAL_ROWS.csv",
    "1714_guard": OUT / "P8_Y5_PARENT_QLOC_1714_CLOSED_WRONG_CHARGE_GUARD.csv",
    "1357_doc": ROOT / "1357-Y5-R10-RAB-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
    "1357_zero": OUT / "P8_Y5_R10_1357_PIM_COMMUTATOR_ZERO_ATTEMPT.csv",
    "1357_profiles": OUT / "P8_Y5_R10_1357_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
    "1357_guard": OUT / "P8_Y5_R10_1357_CHAINMAP_GUARDRAILS.csv",
    "1014_doc": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1014_commutator": OUT / "P8_Y5_R10_1014_PIM_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "1014_route": OUT / "P8_Y5_R10_1014_ROUTE_SPLIT.csv",
    "1014_coeffs": OUT / "P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv",
    "pim_gate": OUT / "P8_Y5_PIM_COMMUTATOR_GATE.csv",
    "topo_certificate": OUT / "P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv",
    "topo_acceptance": OUT / "P8_Y5_PIM_TOPO_EQUALITY_ACCEPTANCE_GATES.csv",
    "input_template": OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
    "radial_template": OUT / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
    "1017_doc": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    "1017_reference": OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
    "1017_mhref": OUT / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
}

NEEDLES = {
    "1714_doc": ["CHAIN1714_3_projector_commutator", "NEXT1714_0_primary"],
    "1714_validation": ["VAL1714_OVERALL", "PASS"],
    "1714_next": ["1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md", "selected"],
    "1714_residuals": ["REQ1714_1_I_commutator", "RETAINED_NONCLAIM"],
    "1714_guard": ["GUARD1714_0_closed_wrong_charge", "INSTALLED"],
    "1357_doc": ["parent-owned fixed topological chain-map", "`I_commutator` obstruction is now split"],
    "1357_zero": ["PCZ1357_8_verdict", "COMMUTATOR_ZERO_NOT_PROVED"],
    "1357_profiles": ["ICP1357_0_fixed_domain_derivative", "ICP1357_7_total_abs_profile"],
    "1357_guard": ["GUARD1357_0_chainmap_not_projector_algebra", "INSTALLED"],
    "1014_doc": ["[d,Pi_M]J_H=0", "not derived"],
    "1014_commutator": ["PCT1014_7_verdict", "fail_current_claim"],
    "1014_route": ["PRS1014_1_topological_Hilbert_equality", "fail_open"],
    "1014_coeffs": ["PCC1014_1_I_commutator", "retained_unfilled"],
    "pim_gate": ["PC521_0_product_rule", "active_obstruction"],
    "topo_certificate": ["PTEC534_5_commutator_zero", "not_derived_bound_template_required"],
    "topo_acceptance": ["AG534_2_commutator_or_bound", "fail_unfilled"],
    "input_template": ["PIF537_1_I_commutator", "not_filled"],
    "radial_template": ["PI521_1_commutator_profile", "template_from_499_not_filled"],
    "1017_doc": ["tau lock", "M_H_ref"],
    "1017_reference": ["HRL1017_4_tau_lock", "fail_current_claim"],
    "1017_mhref": ["MHR1017_0_M_H_ref_denominator", "MISSING_STABLE_MH_REF"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1715_SOURCE_REGISTER.csv"
COMMUTATOR_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1715_PIM_COMMUTATOR_ZERO_ATTEMPT.csv"
PROFILE_ROWS = OUT / "P8_Y5_PARENT_QLOC_1715_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv"
GUARDRAILS = OUT / "P8_Y5_PARENT_QLOC_1715_CHAINMAP_GUARDRAILS.csv"
SIGNATURE_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1715_PARENT_SIGNATURE_REQUIREMENTS.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1715_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1715_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1715_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1715_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    COMMUTATOR_ATTEMPT,
    PROFILE_ROWS,
    GUARDRAILS,
    SIGNATURE_REQUIREMENTS,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    COMMUTATOR_ATTEMPT,
    PROFILE_ROWS,
    GUARDRAILS,
    SIGNATURE_REQUIREMENTS,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    COMMUTATOR_ATTEMPT: [
        QUARANTINE / "PIM_COMMUTATOR_ZERO_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_PiM_commutator_zero_attempt_1715.csv",
        QUEUE / "JR1715_PIM_COMMUTATOR_ZERO_ATTEMPT.csv",
    ],
    PROFILE_ROWS: [
        QUARANTINE / "ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
        BRANCH_RESIDUALS / "R2FR_Icommutator_source_profile_rows_1715.csv",
        QUEUE / "JR1715_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
    ],
    GUARDRAILS: [
        QUARANTINE / "CHAINMAP_GUARDRAILS.csv",
        BRANCH_RESIDUALS / "R2FR_chainmap_guardrails_1715.csv",
        QUEUE / "JR1715_CHAINMAP_GUARDRAILS.csv",
    ],
    SIGNATURE_REQUIREMENTS: [
        QUARANTINE / "PARENT_SIGNATURE_REQUIREMENTS.csv",
        BRANCH_RESIDUALS / "R2FR_parent_signature_requirements_1715.csv",
        QUEUE / "JR1715_PARENT_SIGNATURE_REQUIREMENTS.csv",
    ],
    RUNNER_REFUSAL: [
        QUARANTINE / "RUNNER_REFUSAL.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_1715.csv",
        QUEUE / "JR1715_RUNNER_REFUSAL.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1715.csv",
        QUEUE / "JR1715_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1715.csv",
        QUEUE / "JR1715_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _field in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1715_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1715": "PiM commutator fixed-topology gate and I_commutator source-profile rows",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def commutator_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PCZ1715_0_product_rule",
            "projected-current product rule is retained",
            "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
            "IDENTITY_RETAINED",
            "dropping the commutator would be algebraic handwaving",
            "keeps I_commutator visible",
        ),
        (
            "PCZ1715_1_conditional_chainmap_lemma",
            "fixed topological chain-map kills the commutator",
            "if Pi_M is fixed on the source-current complex, d Pi_M=Pi_M d and [d,Pi_M]J_H=0",
            "CONDITIONAL_LEMMA_ONLY",
            "I_commutator remains physical until parent signature exists",
            "mathematics is clean but not current-MTS proof",
        ),
        (
            "PCZ1715_2_parent_fixed_domain",
            "compact source/exterior domain and linking class are parent-fixed",
            "delta_readout W_M=0; delta_g[S2]_M=0; A_ext ~= S2 x I before orbital fitting",
            "NOT_PARENT_SIGNED",
            "domain derivative feeds I_commutator",
            "moving-domain source-profile row remains live",
        ),
        (
            "PCZ1715_3_metric_independent_PiM",
            "Pi_M is topological, not Hodge/DeWitt/Green metric data",
            "Pi_M J=ell_M(J) omega_M_top, d omega_M_top=0, delta_g Pi_M=0",
            "NOT_PARENT_SIGNED",
            "projector stress and Hodge variation survive",
            "metric/Hodge profile row remains live",
        ),
        (
            "PCZ1715_4_source_current_domain",
            "physical Hilbert current lies in the fixed chain-map complex",
            "J_H[e_obs,tau] in C_H(W_M,A_ext), with extra/source/species/frame channels included or theorem-zero",
            "SOURCE_DOMAIN_NOT_LOCKED",
            "commutator-zero lemma may not apply to physical J_H",
            "current-domain escape profile row remains live",
        ),
        (
            "PCZ1715_5_exterior_source_silence",
            "compact exterior annulus has no hidden source/boundary/anomaly support",
            "support(dJ_H), support(dPi_M), support(A_parent), support(B_flux) absent from A_ext or theorem-zero",
            "NOT_DERIVED",
            "finite-shell commutator profile can be nonzero",
            "anomaly/boundary/radial leakage rows remain live",
        ),
        (
            "PCZ1715_6_no_readout_mask",
            "Pi_M is not a late readout mask or equality multiplier",
            "Pi_M appears before readout in parent derivation; no fitted post-orbit projector",
            "GUARDRAIL_REQUIRED",
            "closure becomes a fitted mask rather than field theory",
            "guard installed, theorem still open",
        ),
        (
            "PCZ1715_7_tau_reference_lock",
            "same observed tau/reference normalizes source, charge, clock and readout",
            "tau_source=tau_charge=tau_clock=tau_readout; M_H_ref stable and same-frame",
            "NOT_PARENT_DERIVED",
            "I_commutator cannot be normalized claim-safely",
            "tau/reference profile row remains live",
        ),
        (
            "PCZ1715_8_verdict",
            "Pi_M commutator zero theorem for live R2FR branch",
            "[d,Pi_M]J_H=0 for the physical source current in the physical compact exterior annulus",
            "COMMUTATOR_ZERO_NOT_PROVED",
            "fill I_commutator source-profile rows as nonclaim",
            "conditional theorem retained; claim gates stay shut",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "claim_piece": claim_piece,
            "mathematical_form": math_form,
            "current_status": status,
            "failure_if_missing": failure,
            "effect": effect,
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, claim_piece, math_form, status, failure, effect in rows
    ]


def profile_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ICP1715_0_fixed_domain_derivative",
            "I_commutator_domain",
            "finite-annulus contribution from moving source/exterior domain or linking surface",
            "M_H_ref^-1 int_A (d Pi_M)_domain J_H",
            "system_id;annulus_A;surface_pair;domain_rule;dPiM_domain;J_H_source;M_H_ref;units;source_path;valid_for_claim",
            "dimensionless after M_H_ref normalization or mass-flux before normalization",
            "R4;R7;R9;R10;R11",
            "MISSING",
        ),
        (
            "ICP1715_1_metric_Hodge_variation",
            "I_commutator_Hodge",
            "Hodge/DeWitt/Green-operator metric variation of Pi_M",
            "M_H_ref^-1 int_A (delta_g Pi_M or dPiM_Hodge) J_H",
            "system_id;operator_family;metric_variation;Green_operator;boundary_metric;M_H_ref;units;source_path;valid_for_claim",
            "dimensionless projector-stress equivalent or mass-flux",
            "R3;R4;R7;R8;R10;R11",
            "MISSING",
        ),
        (
            "ICP1715_2_source_current_domain_escape",
            "I_commutator_current_domain",
            "physical Hilbert current leaves the fixed topological current complex",
            "M_H_ref^-1 int_A [d,Pi_M] J_H_extra_or_frame",
            "system_id;current_channel;J_H_component;domain_membership_test;Pi_M_action;M_H_ref;units;source_path;valid_for_claim",
            "dimensionless source-channel fraction",
            "R4;R7;R10;R11;WEP;clocks",
            "MISSING",
        ),
        (
            "ICP1715_3_boundary_representative_shift",
            "I_commutator_boundary_rep",
            "boundary representative or exact-form choice changes Pi_M across annulus",
            "M_H_ref^-1 int_boundary Delta(Pi_M representative) J_H",
            "system_id;boundary_rule;representative_class;boundary_flux;M_H_ref;units;source_path;valid_for_claim",
            "dimensionless boundary GM fraction",
            "R4;R9;R10;R11",
            "MISSING",
        ),
        (
            "ICP1715_4_parent_anomaly_or_extra_operator",
            "I_commutator_anomaly",
            "non-EH/parent anomaly term makes projected source complex non-closed",
            "M_H_ref^-1 int_A Pi_M A_parent or [d,Pi_M]J_extra",
            "system_id;operator_family;A_parent;J_extra;Pi_M_action;M_H_ref;units;source_path;valid_for_claim",
            "dimensionless anomaly fraction or mass-current divergence",
            "R4;R7;R10;R11",
            "MISSING",
        ),
        (
            "ICP1715_5_tau_reference_drift",
            "I_commutator_tau_ref",
            "time-generator or Hamiltonian reference mismatch leaks into source-current commutator",
            "M_H_ref^-1 int_A (partial_tau Pi_M + partial_ref Pi_M)J_H",
            "system_id;tau_source;tau_charge;tau_readout;reference_rule;drift_profile;M_H_ref;units;source_path;valid_for_claim",
            "dimensionless or per-time with normalization convention",
            "R7;R9;R11;clocks;Gdot_over_G",
            "MISSING",
        ),
        (
            "ICP1715_6_material_species_projector",
            "I_commutator_species",
            "material/species source charge changes the Pi_M-selected current channel",
            "M_H_ref^-1 int_A [d,Pi_M_species]J_H_species",
            "system_id;species_pair;material_channel;Pi_M_species;J_H_species;M_H_ref;units;source_path;valid_for_claim",
            "dimensionless species/source-charge fraction",
            "WEP;clock composition;R10;R11",
            "MISSING",
        ),
        (
            "ICP1715_7_total_abs_profile",
            "epsilon_Icommutator_abs",
            "no-cancellation envelope of all I_commutator profile components",
            "sum_i abs(ICP1715_i)/M_H_ref with every component real or theorem-zero",
            "system_id;component_rows;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim",
            "dimensionless",
            "R4;R7;R9;R10;R11;PPN;clocks;orbital",
            "NOT_COMPUTED_COMPONENTS_MISSING",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "profile_id": profile_id,
            "quantity": quantity,
            "definition": definition,
            "formula": formula,
            "required_columns": required_columns,
            "units_required": units,
            "affected_arenas": arenas,
            "value_or_theorem": value,
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for profile_id, quantity, definition, formula, required_columns, units, arenas, value in rows
    ]


def guardrail_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GUARD1715_0_chainmap_not_projector_algebra",
            "Pi_M^2=Pi_M does not imply [d,Pi_M]J_H=0",
            "use projector idempotence as a commutator proof",
            "prove fixed chain-map ownership on the Hilbert-current complex",
        ),
        (
            "GUARD1715_1_no_Hodge_silencing",
            "Hodge/DeWitt/domain projectors carry metric and boundary variation unless theorem-zeroed",
            "call Hodge projector stress absent without delta_g Pi_M calculation",
            "derive metric-independent topological Pi_M or retain projector-stress rows",
        ),
        (
            "GUARD1715_2_no_post_readout_mask",
            "Pi_M must be parent-selected before source/orbit readout",
            "choose Pi_M after seeing residuals to force I_commutator=0",
            "supply parent topology/source-measure selector before scoring",
        ),
        (
            "GUARD1715_3_no_normalization_shortcut",
            "I_commutator cannot be normalized by orbital GM or reference-only M_H_ref",
            "divide by the readout the theorem is meant to derive",
            "use same-frame Hamiltonian/Hilbert source denominator with source path",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "guardrail": guardrail,
            "forbidden_move": forbidden,
            "allowed_replacement": allowed,
            "status": "INSTALLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, guardrail, forbidden, allowed in rows
    ]


def signature_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("SIG1715_0_parent_selector", "parent selects topological mass channel before readout", "chi_M or ell_M selected by S_parent and compact source support W_M", "MISSING_PARENT_SELECTOR"),
        ("SIG1715_1_fixed_domain", "source worldtube/exterior linking class fixed", "delta W_M=0 and delta[S2]_M=0 under metric/readout/orbit variations", "MISSING_DOMAIN_LOCK"),
        ("SIG1715_2_metric_independent_representative", "closed normalized representative independent of metric", "d omega_M_top=0, integral_link omega_M_top=1, delta_g omega_M_top=0", "CONDITIONAL_TEMPLATE_ONLY"),
        ("SIG1715_3_chainmap_proof", "Pi_M is a chain-map on Hilbert-current complex", "d(Pi_M J)=Pi_M dJ for all physical J in C_H(W_M,A_ext)", "CONDITIONAL_LEMMA_ONLY"),
        ("SIG1715_4_physical_current_lock", "physical J_H belongs to fixed chain-map domain", "J_H[e_obs,tau] and all source channels are in C_H or theorem-zero outside it", "MISSING_CURRENT_DOMAIN_LOCK"),
        ("SIG1715_5_exterior_silence", "finite annulus contains no commutator source", "support(dPi_M), support(A_parent), support(B_flux), support(J_extra) absent from A_ext or theorem-zero", "MISSING_EXTERIOR_SILENCE_THEOREM"),
        ("SIG1715_6_tau_MHref_lock", "same tau and denominator are parent-owned", "tau_source=tau_charge=tau_clock=tau_readout; M_H_ref positive same-frame source charge", "MISSING_TAU_MHREF_LOCK"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "parent_requirement": requirement,
            "minimal_form": minimal_form,
            "current_status": status,
            "evidence_needed": "parent action/theorem or source-backed row with path and units",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for requirement_id, requirement, minimal_form, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1715_0_commutator_zero", "claim [d,Pi_M]J_H=0", "REJECT_CONDITIONAL_ONLY", "fixed-domain, metric-independent Pi_M, current-domain, exterior silence and tau/M_H_ref are unsigned"),
        ("RUN1715_1_projector_algebra", "use Pi_M^2=Pi_M to prove closure", "REJECT_IDEMPOTENCE_SHORTCUT", "projector algebra does not imply flux closure"),
        ("RUN1715_2_Hodge_silence", "drop Hodge/metric projector variation", "REJECT_HODGE_SILENCE", "delta_g Pi_M stress must be theorem-zero or bounded"),
        ("RUN1715_3_post_readout_mask", "choose Pi_M after readout to zero residual", "FORBIDDEN_POST_READOUT_MASK", "post-readout masking is closure-only, not derivation"),
        ("RUN1715_4_profile_score", "score I_commutator profile rows", "NOT_RUN_TEMPLATE_ONLY", "profile rows are MISSING values/theorems and not source-backed"),
        ("RUN1715_5_Newton_GR", "reopen Newton/local-GR source normalization", "BLOCKED_NO_CLAIM", "Pi_M chain-map, R_eq, M_H_ref and calibration remain blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT1715_0_primary",
            "1716-Y5-R2FR-PiM-fixed-chainmap-parent-signature-or-Icommutator-first-profile-row.md",
            "scripts/Y5_R2FR_PiM_fixed_chainmap_parent_signature_or_Icommutator_first_profile_row.py",
            "try to parent-sign fixed domain, metric-independent Pi_M, current-domain membership, exterior source silence, and tau/reference lock; if not, create the first concrete I_commutator profile row schema",
            "selected",
        ),
        (
            "NEXT1715_1_parallel_Req",
            "1716b-Y5-R2FR-R_eq-bound-input-row-or-topological-Hilbert-equality-contract.md",
            "scripts/Y5_R2FR_R_eq_bound_input_row_or_topological_Hilbert_equality_contract.py",
            "parallel R_eq route remains secondary until PiM chain-map ownership is clearer",
            "held_parallel",
        ),
        (
            "NEXT1715_2_parallel_MHref",
            "1716c-Y5-R2FR-MHref-denominator-source-intake.md",
            "scripts/Y5_R2FR_MHref_denominator_source_intake.py",
            "parallel M_H_ref denominator intake if profile scoring becomes necessary",
            "held_until_profile_row",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "success_condition": "claim-safe Pi_M chain-map certificate or one source-ready nonclaim I_commutator profile row with denominator/units/source-path requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1715_0_conditional_lemma", "fixed topological chain-map would imply I_commutator=0", "CONDITIONAL_ONLY_NO_CLAIM", "mathematics is clean but not current-MTS evidence"),
        ("CG1715_1_parent_chainmap_signed", "current MTS parent-signs fixed-domain metric-independent Pi_M on physical J_H", "BLOCKED_NO_CLAIM", "selector/domain/current/exterior/tau locks are missing"),
        ("CG1715_2_Icommutator_zero", "[d,Pi_M]J_H=0 for the physical source current", "BLOCKED_NO_CLAIM", "conditional lemma cannot be applied to physical source rows yet"),
        ("CG1715_3_Icommutator_profile_score", "I_commutator profile rows are numeric/source-backed and scoreable", "BLOCKED_NO_CLAIM", "all profile rows remain MISSING/nonclaim"),
        ("CG1715_4_Newton_GR", "Newton/local-GR gates can reopen from commutator route", "BLOCKED_NO_CLAIM", "Pi_M chain-map, R_eq, M_H_ref, calibration and PPN residuals remain blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def parse_all(paths: list[Path]) -> bool:
    for path in paths:
        read_csv(path)
    return True


def claim_flags_false(paths: list[Path]) -> bool:
    checked_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "score_emitted",
        "parent_signed",
        "source_backed",
        "accepted_for_scoring",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in checked_keys and truthy(value):
                    return False
    return True


def formalization_1715_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [
        path
        for path in FORMALIZATION.rglob("*1715*")
        if path.is_file() and ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    source_rows: list[dict[str, Any]],
    commutator_rows: list[dict[str, Any]],
    profile_rows_: list[dict[str, Any]],
    guard_rows_: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    remove_pycache()
    checks = [
        ("VAL1715_0_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL1715_1_needles_present", all(row["needles_present"] for row in source_rows), "required source needles are present"),
        (
            "VAL1715_2_commutator_not_promoted",
            any(row["clause_id"] == "PCZ1715_8_verdict" and row["current_status"] == "COMMUTATOR_ZERO_NOT_PROVED" for row in commutator_rows),
            "PiM commutator zero theorem remains unproved for current MTS",
        ),
        (
            "VAL1715_3_profiles_present",
            len(profile_rows_) == 8
            and any(row["profile_id"] == "ICP1715_0_fixed_domain_derivative" for row in profile_rows_)
            and any(row["profile_id"] == "ICP1715_7_total_abs_profile" for row in profile_rows_),
            "I_commutator profile rows cover domain/Hodge/current/boundary/anomaly/tau/species/total",
        ),
        (
            "VAL1715_4_profiles_nonclaim",
            all(row["status"] == "RETAINED_NONCLAIM" and row["accepted_for_scoring"] is False for row in profile_rows_),
            "profile rows remain missing/unscored/nonclaim",
        ),
        (
            "VAL1715_5_guardrails_installed",
            len(guard_rows_) >= 4 and all(row["status"] == "INSTALLED" for row in guard_rows_),
            "chain-map/idempotence/Hodge/readout/normalization guardrails installed",
        ),
        (
            "VAL1715_6_signature_requirements_open",
            len(signature_rows) >= 7 and all(row["current_status"] != "SIGNED" for row in signature_rows),
            "parent signature requirements are explicit and open",
        ),
        (
            "VAL1715_7_runner_refuses_shortcuts",
            all("REJECT" in row["status"] or "NOT_RUN" in row["status"] or "FORBIDDEN" in row["status"] or "BLOCKED" in row["status"] for row in runner_rows_),
            "runner refuses projector algebra/Hodge/readout/profile/Newton shortcuts",
        ),
        (
            "VAL1715_8_next_selected",
            any(row["route_id"] == "NEXT1715_0_primary" and row["selection_status"] == "selected" for row in next_rows_),
            "next target selects fixed-chainmap parent signature or first profile row",
        ),
        (
            "VAL1715_9_claim_gates_blocked",
            all("NO_CLAIM" in row["status"] or "CONDITIONAL_ONLY" in row["status"] for row in claim_rows_),
            "claim gates do not promote commutator/Newton/local-GR",
        ),
        ("VAL1715_10_csv_parse", parse_all(GENERATED_CSVS), "all generated 1715 CSVs parse"),
        (
            "VAL1715_11_no_claim_flags",
            claim_flags_false(CLAIM_CHECKED_CSVS),
            "all generated scoring and claim flags remain false",
        ),
        (
            "VAL1715_12_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets),
            "branch/quarantine/queue copies exist",
        ),
        (
            "VAL1715_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1715_14_formalization_untouched",
            not formalization_1715_hits(),
            "no 1715 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1715_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1715 PiM commutator fixed-topology and I_commutator source-profile validation",
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    commutator_rows: list[dict[str, Any]],
    profile_rows_: list[dict[str, Any]],
    guard_rows_: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    content = "\n\n".join(
        [
            "# 1715 - PiM Commutator Fixed Topology Or I_commutator Source Profile",
            "## Verdict\n"
            "- 1715 records the clean conditional theorem: a parent-owned fixed topological chain-map `Pi_M` would give `[d,Pi_M]J_H=0`.\n"
            "- Current MTS does not sign the parent prerequisites: fixed domain, metric-independent `Pi_M`, physical-current membership, exterior silence, no readout mask, and tau/`M_H_ref` lock.\n"
            "- Therefore `I_commutator` remains a live finite source-normalization residual, not a solved theorem.\n"
            "- The obstruction is now split into eight source-profile channels: domain, Hodge/metric, current-domain escape, boundary representative, anomaly/extra operator, tau/reference drift, species/material projection, and total no-cancellation envelope.\n"
            "- No Newton, local-GR, R10, PPN, clock, orbital, source-normalization or q_loc-zero claim is made.",
            "## Source Register\n" + table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
            "## PiM Commutator Zero Attempt\n"
            + table(commutator_rows, ["clause_id", "claim_piece", "mathematical_form", "current_status", "failure_if_missing", "effect"]),
            "## I_commutator Source-Profile Rows\n"
            + table(profile_rows_, ["profile_id", "quantity", "definition", "formula", "value_or_theorem", "status"]),
            "## Chain-Map Guardrails\n"
            + table(guard_rows_, ["guard_id", "guardrail", "forbidden_move", "allowed_replacement", "status"]),
            "## Parent Signature Requirements\n"
            + table(signature_rows, ["requirement_id", "parent_requirement", "minimal_form", "current_status", "evidence_needed"]),
            "## Runner Refusal\n" + table(runner_rows_, ["runner_id", "case", "status", "reason"]),
            "## Next Target\n" + table(next_rows_, ["route_id", "next_target", "script", "objective", "selection_status"]),
            "## Claim Gates\n" + table(claim_rows_, ["claim_id", "claim", "status", "reason"]),
            "## Validation\n" + table(validation_rows_, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "This is one of the better-shaped gaps now. The math route is real: fixed chain-map implies no commutator. The physics route is still unsigned: MTS must own the selector, domain, current complex, exterior silence, and denominator. If 1716 cannot parent-sign those, the first concrete `I_commutator` row becomes the honest empirical path.",
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    commutator_rows = commutator_attempt_rows()
    profile_rows_ = profile_rows()
    guard_rows_ = guardrail_rows()
    signature_rows = signature_requirement_rows()
    runner_rows_ = runner_rows()
    next_rows_ = next_rows()
    claim_rows_ = claim_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(COMMUTATOR_ATTEMPT, commutator_rows)
    write_csv(PROFILE_ROWS, profile_rows_)
    write_csv(GUARDRAILS, guard_rows_)
    write_csv(SIGNATURE_REQUIREMENTS, signature_rows)
    write_csv(RUNNER_REFUSAL, runner_rows_)
    write_csv(NEXT_TARGET, next_rows_)
    write_csv(CLAIM_GATE, claim_rows_)
    copy_outputs()

    validation_rows_ = validation_rows(
        source_rows,
        commutator_rows,
        profile_rows_,
        guard_rows_,
        signature_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
    )
    write_csv(VALIDATION, validation_rows_)
    write_doc(
        source_rows,
        commutator_rows,
        profile_rows_,
        guard_rows_,
        signature_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
        validation_rows_,
    )

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"1715 validation {validation_rows_[-1]['result']}")


if __name__ == "__main__":
    main()
