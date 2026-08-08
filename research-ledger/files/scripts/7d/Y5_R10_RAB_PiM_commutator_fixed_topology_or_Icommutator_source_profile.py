from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1357"
TITLE = "1357-Y5-R10-RAB-PiM-commutator-fixed-topology-or-Icommutator-source-profile"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COMMUTATOR_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_PIM_COMMUTATOR_ZERO_ATTEMPT.csv"
PROFILE_ROWS_PATH = OUT_DIR / f"{PACK_ID}_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv"
CHAINMAP_GUARD_PATH = OUT_DIR / f"{PACK_ID}_CHAINMAP_GUARDRAILS.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1357_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1357_0_1356_doc",
            "source_path": "1356-Y5-R10-RAB-worldtube-Hilbert-source-equality-or-R_eq-Icommutator-fill.md",
            "required_anchor": "REQ1356_1_I_commutator",
            "purpose": "1356 retains I_commutator as a live source-profile obstruction.",
        },
        {
            "source_id": "SRC1357_1_1356_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1356_NEXT_TARGET.csv",
            "required_anchor": "NEXT1356_0_1357",
            "purpose": "handoff to Pi_M commutator fixed-topology route.",
        },
        {
            "source_id": "SRC1357_2_1356_residuals",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1356_REQ_ICOMMUTATOR_FILL.csv",
            "required_anchor": "REQ1356_1_I_commutator",
            "purpose": "current I_commutator residual row and affected arenas.",
        },
        {
            "source_id": "SRC1357_3_1014_doc",
            "source_path": "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            "required_anchor": "PCT1014_2_commutator_zero",
            "purpose": "prior commutator theorem attempt and product-rule obstruction.",
        },
        {
            "source_id": "SRC1357_4_commutator_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv",
            "required_anchor": "PC521_2_topological_zero_commutator",
            "purpose": "fixed-topological Pi_M route and Hodge/domain/readout guards.",
        },
        {
            "source_id": "SRC1357_5_topo_certificate",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv",
            "required_anchor": "PTEC534_5_commutator_zero",
            "purpose": "topological equality certificate clause for commutator zero.",
        },
        {
            "source_id": "SRC1357_6_topo_acceptance",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_ACCEPTANCE_GATES.csv",
            "required_anchor": "AG534_2_commutator_or_bound",
            "purpose": "acceptance gate requires theorem-zero or source-backed I_commutator bound.",
        },
        {
            "source_id": "SRC1357_7_input_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
            "required_anchor": "PIF537_1_I_commutator",
            "purpose": "schema requirements for filling I_commutator source rows.",
        },
        {
            "source_id": "SRC1357_8_radial_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
            "required_anchor": "PI521_1_commutator_profile",
            "purpose": "radial/profile definition of I_commutator.",
        },
        {
            "source_id": "SRC1357_9_1015_doc",
            "source_path": "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
            "required_anchor": "SOL1015_5_commutator_stress_silence",
            "purpose": "same-object lemma still requires fixed chain-map and projector-stress silence.",
        },
        {
            "source_id": "SRC1357_10_1017_doc",
            "source_path": "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            "required_anchor": "HRL1017_4_tau_lock",
            "purpose": "tau/source-frame/reference locks remain missing for a claim-ready denominator.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def commutator_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "PCZ1357_0_product_rule",
            "claim_piece": "projected-current product rule is the starting identity",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
            "derivation_attempt": "The only honest way to remove I_commutator is to prove Pi_M commutes with d on the physical Hilbert-current complex.",
            "current_evidence": "PC521_0 and PCT1014_0 retain the term explicitly.",
            "status": "IDENTITY_RETAINED",
            "failure_if_missing": "dropping [d,Pi_M]J_H would be algebraic handwaving",
        },
        {
            "clause_id": "PCZ1357_1_conditional_chainmap_lemma",
            "claim_piece": "fixed topological chain-map kills the commutator",
            "mathematical_form": "if Pi_M is a fixed chain-map and D_source is fixed, then d Pi_M = Pi_M d, hence [d,Pi_M]J_H=0",
            "derivation_attempt": "This is the clean route: Pi_M must be selected by parent topology before readout, independent of metric, radial domain, material fitting, and observational masks.",
            "current_evidence": "PTEC534_0 through PTEC534_2 state the needed certificate clauses, but they are not source-backed as current MTS evidence.",
            "status": "CONDITIONAL_LEMMA_ONLY",
            "failure_if_missing": "I_commutator remains a physical source-profile row",
        },
        {
            "clause_id": "PCZ1357_2_parent_fixed_domain",
            "claim_piece": "compact source/exterior domain and S2 class are fixed before readout",
            "mathematical_form": "delta_readout Sigma_ext = 0; delta_metric [S2]_M = 0; Pi_M has no fitted-domain dependence",
            "derivation_attempt": "A moving annulus or linking surface contributes a domain derivative to Pi_M, so fixed topology must be parent-owned.",
            "current_evidence": "PTEC534_0 is a certificate requirement, not a passed parent theorem.",
            "status": "NOT_PARENT_SIGNED",
            "failure_if_missing": "moving-domain terms feed I_commutator",
        },
        {
            "clause_id": "PCZ1357_3_metric_independent_projector",
            "claim_piece": "Pi_M is not Hodge/DeWitt/Green-function metric data",
            "mathematical_form": "delta_g Pi_M=0 and Pi_M J = ell_M(J) omega_M_top",
            "derivation_attempt": "Metric-independent topological data would silence projector stress; Hodge/DeWitt data would not.",
            "current_evidence": "PC521_3 says Hodge/DeWitt routes retain boundary metric, Green operator, representative, and domain variations.",
            "status": "NOT_PARENT_SIGNED",
            "failure_if_missing": "projector stress and I_commutator survive",
        },
        {
            "clause_id": "PCZ1357_4_source_current_domain",
            "claim_piece": "J_H lies in the same fixed current complex on which Pi_M is a chain-map",
            "mathematical_form": "J_H in C_source; dJ_H has only allowed compact-source/support terms; Pi_M dJ_H is not hiding extra channels",
            "derivation_attempt": "Even a topological Pi_M only commutes with d on its owned domain; extra current, species, memory, frame, or tau drift can leave the domain.",
            "current_evidence": "1355/1356 retain extra source channels and calibration tails.",
            "status": "SOURCE_DOMAIN_NOT_LOCKED",
            "failure_if_missing": "commutator-zero proof does not apply to physical J_H",
        },
        {
            "clause_id": "PCZ1357_5_compact_exterior_source_silence",
            "claim_piece": "no source, boundary, or anomaly support exists inside the compact exterior annulus",
            "mathematical_form": "support(dJ_H), support(dPi_M), support(A_parent), support(B_flux) are outside A or theorem-zero",
            "derivation_attempt": "The finite-annulus integral vanishes only when the exterior annulus is clean, not merely because a formal current is closed elsewhere.",
            "current_evidence": "REQ1356 rows keep A_parent, B_zero_flux, epsilon_radial_Meff, and calibration open.",
            "status": "NOT_DERIVED",
            "failure_if_missing": "finite-shell I_commutator profile can be nonzero",
        },
        {
            "clause_id": "PCZ1357_6_no_readout_mask_or_multiplier",
            "claim_piece": "Pi_M appears before readout and is not imposed by a late equality multiplier",
            "mathematical_form": "delta S_parent/delta Pi_read=0; no lambda_eq-only closure; no fitted post-orbit Pi_M",
            "derivation_attempt": "A post-readout projector can always make the obstruction look smaller, but gives no derivation credit.",
            "current_evidence": "PC521_4, PC521_5, and PTEC534_7 forbid this move.",
            "status": "GUARDRAIL_REQUIRED",
            "failure_if_missing": "closure becomes a fitted mask, not field theory",
        },
        {
            "clause_id": "PCZ1357_7_tau_and_reference_lock",
            "claim_piece": "same observed time generator/reference is used by source, charge, clocks, and readout",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_readout; delta tau=0; M_H_ref stable and not orbital GM",
            "derivation_attempt": "A drifting tau/reference can move the commutator into a normalization or clock-source residual.",
            "current_evidence": "HRL1017_4 and HRL1017_5 fail current claim.",
            "status": "NOT_PARENT_DERIVED",
            "failure_if_missing": "I_commutator cannot be normalized claim-safely",
        },
        {
            "clause_id": "PCZ1357_8_verdict",
            "claim_piece": "Pi_M commutator zero theorem for current MTS",
            "mathematical_form": "[d,Pi_M]J_H=0 for the physical source current in the physical compact exterior annulus",
            "derivation_attempt": "A conditional chain-map lemma is available, but current MTS has not parent-signed fixed domain, metric-independent Pi_M, current-domain lock, exterior silence, tau/reference lock, or no-readout ownership.",
            "current_evidence": "AG534_2 still requires theorem-zero or source-backed I_commutator bound.",
            "status": "COMMUTATOR_ZERO_NOT_PROVED",
            "failure_if_missing": "fill I_commutator source-profile rows as nonclaim",
        },
    ]
    return mark_nonclaim(rows)


def profile_rows() -> list[dict[str, object]]:
    rows = [
        {
            "profile_id": "ICP1357_0_fixed_domain_derivative",
            "quantity": "I_commutator_domain",
            "definition": "finite-annulus contribution from a moving source/exterior domain or linking surface",
            "formula": "M_H_ref^-1 int_A (d Pi_M)_domain J_H",
            "required_columns": "system_id;annulus_A;surface_pair;domain_rule;dPiM_domain;J_H_source;M_H_ref;units;source_path;valid_for_claim",
            "units_required": "dimensionless after M_H_ref normalization or mass-flux before normalization",
            "affected_arenas": "R4;R7;R9;R10;R11",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "profile_id": "ICP1357_1_metric_Hodge_variation",
            "quantity": "I_commutator_Hodge",
            "definition": "Hodge/DeWitt/Green-operator metric variation of Pi_M",
            "formula": "M_H_ref^-1 int_A (delta_g Pi_M or dPi_M_Hodge) J_H",
            "required_columns": "system_id;operator_family;metric_variation;Green_operator;boundary_metric;M_H_ref;units;source_path;valid_for_claim",
            "units_required": "dimensionless projector-stress equivalent or mass-flux",
            "affected_arenas": "R3;R4;R7;R8;R10;R11",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "profile_id": "ICP1357_2_source_current_domain_escape",
            "quantity": "I_commutator_current_domain",
            "definition": "physical Hilbert current leaves the fixed topological current complex",
            "formula": "M_H_ref^-1 int_A [d,Pi_M] J_H_extra_or_frame",
            "required_columns": "system_id;current_channel;J_H_component;domain_membership_test;Pi_M_action;M_H_ref;units;source_path;valid_for_claim",
            "units_required": "dimensionless source-channel fraction",
            "affected_arenas": "R4;R7;R10;R11;WEP;clocks",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "profile_id": "ICP1357_3_boundary_representative_shift",
            "quantity": "I_commutator_boundary_rep",
            "definition": "boundary representative or exact-form choice changes Pi_M across the annulus",
            "formula": "M_H_ref^-1 int_boundary Delta(Pi_M representative) J_H",
            "required_columns": "system_id;boundary_rule;representative_class;boundary_flux;M_H_ref;units;source_path;valid_for_claim",
            "units_required": "dimensionless boundary GM fraction",
            "affected_arenas": "R4;R9;R10;R11",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "profile_id": "ICP1357_4_parent_anomaly_or_extra_operator",
            "quantity": "I_commutator_anomaly",
            "definition": "non-EH/parent anomaly term makes the projected source complex non-closed",
            "formula": "M_H_ref^-1 int_A Pi_M A_parent or [d,Pi_M]J_extra",
            "required_columns": "system_id;operator_family;A_parent;J_extra;Pi_M_action;M_H_ref;units;source_path;valid_for_claim",
            "units_required": "dimensionless anomaly fraction or mass-current divergence",
            "affected_arenas": "R4;R7;R10;R11",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "profile_id": "ICP1357_5_tau_reference_drift",
            "quantity": "I_commutator_tau_ref",
            "definition": "time-generator or Hamiltonian reference mismatch appears as source-current commutator leakage",
            "formula": "M_H_ref^-1 int_A (partial_tau Pi_M + partial_ref Pi_M)J_H",
            "required_columns": "system_id;tau_source;tau_charge;tau_readout;reference_rule;drift_profile;M_H_ref;units;source_path;valid_for_claim",
            "units_required": "dimensionless or per-time with normalization convention",
            "affected_arenas": "R7;R9;R11;clocks;Gdot_over_G",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "profile_id": "ICP1357_6_material_species_projector",
            "quantity": "I_commutator_species",
            "definition": "material/species source charge changes the Pi_M-selected current channel",
            "formula": "M_H_ref^-1 int_A [d,Pi_M_species]J_H_species",
            "required_columns": "system_id;species_pair;material_channel;Pi_M_species;J_H_species;M_H_ref;units;source_path;valid_for_claim",
            "units_required": "dimensionless species/source-charge fraction",
            "affected_arenas": "WEP;clock composition;R10;R11",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "profile_id": "ICP1357_7_total_abs_profile",
            "quantity": "epsilon_Icommutator_abs",
            "definition": "no-cancellation envelope of all I_commutator profile components",
            "formula": "sum_i abs(ICP1357_i)/M_H_ref with all components real or theorem-zero",
            "required_columns": "system_id;component_rows;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim",
            "units_required": "dimensionless",
            "affected_arenas": "R4;R7;R9;R10;R11;PPN;clocks;orbital",
            "value_or_theorem": "NOT_COMPUTED_COMPONENTS_MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
    ]
    return mark_nonclaim(rows)


def guard_rows() -> list[dict[str, object]]:
    rows = [
        {
            "guard_id": "GUARD1357_0_chainmap_not_projector_algebra",
            "guardrail": "Pi_M^2=Pi_M does not imply [d,Pi_M]J_H=0",
            "forbidden_move": "use projector idempotence as a commutator proof",
            "allowed_replacement": "prove fixed chain-map ownership on the Hilbert-current complex",
            "status": "INSTALLED",
        },
        {
            "guard_id": "GUARD1357_1_no_Hodge_silencing",
            "guardrail": "Hodge/DeWitt/domain projectors carry metric and boundary variation unless theorem-zeroed",
            "forbidden_move": "call Hodge projector stress absent without delta_g Pi_M calculation",
            "allowed_replacement": "derive metric-independent topological Pi_M or retain projector-stress rows",
            "status": "INSTALLED",
        },
        {
            "guard_id": "GUARD1357_2_no_post_readout_mask",
            "guardrail": "Pi_M must be parent-selected before source/orbit readout",
            "forbidden_move": "choose Pi_M after seeing residuals to force I_commutator=0",
            "allowed_replacement": "supply parent topology/source-measure selector before scoring",
            "status": "INSTALLED",
        },
        {
            "guard_id": "GUARD1357_3_no_normalization_shortcut",
            "guardrail": "I_commutator cannot be normalized by orbital GM or reference-only M_H_ref",
            "forbidden_move": "divide by the readout the theorem is meant to derive",
            "allowed_replacement": "use a same-frame Hamiltonian/Hilbert source denominator with source path",
            "status": "INSTALLED",
        },
    ]
    return mark_nonclaim(rows)


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1357_0_conditional_lemma",
            "claim": "fixed topological chain-map would imply [d,Pi_M]J_H=0",
            "gate_pass": True,
            "reason": "conditional mathematics is clean but not claim-valid for current MTS",
        },
        {
            "gate_id": "GATE1357_1_parent_chainmap_signed",
            "claim": "current MTS parent action signs fixed-domain metric-independent Pi_M",
            "gate_pass": False,
            "reason": "fixed topology, current domain, exterior silence, tau/reference lock, and no-readout ownership are not all signed",
        },
        {
            "gate_id": "GATE1357_2_Icommutator_zero_current_MTS",
            "claim": "[d,Pi_M]J_H=0 for the physical source current",
            "gate_pass": False,
            "reason": "conditional lemma cannot be applied to physical J_H yet",
        },
        {
            "gate_id": "GATE1357_3_Icommutator_profile_score_ready",
            "claim": "I_commutator profile rows are numeric/source-backed and can be scored",
            "gate_pass": False,
            "reason": "all profile rows remain MISSING/nonclaim",
        },
        {
            "gate_id": "GATE1357_4_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen from commutator route",
            "gate_pass": False,
            "reason": "Pi_M chain-map, R_eq, M_H_ref, calibration, and PPN residuals remain blocked",
        },
    ]
    return mark_nonclaim(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1357_0_conditional_route_real",
            "decision": "The fixed-topological chain-map route is mathematically real.",
            "why": "a parent-owned, metric-independent Pi_M on a fixed current complex would commute with d",
            "next_action": "try to parent-sign the fixed-domain/current-domain clauses rather than abandoning the route",
        },
        {
            "decision_id": "DEC1357_1_current_claim_fails",
            "decision": "Current MTS does not prove the Pi_M commutator zero.",
            "why": "domain, metric-independence, physical J_H membership, exterior silence, tau/reference, and before-readout ownership are unsigned",
            "next_action": "retain I_commutator as source-profile debt",
        },
        {
            "decision_id": "DEC1357_2_best_next_target",
            "decision": "Best next target is parent fixed-chain-map ownership.",
            "why": "if Pi_M ownership closes, I_commutator shrinks; if not, the first source-profile row becomes mandatory",
            "next_action": "try to derive fixed-domain/current-domain ownership or stage the first I_commutator profile input row",
        },
    ]
    return mark_nonclaim(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1357_0_1358",
            "target_file": "1358-Y5-R10-RAB-PiM-fixed-chainmap-parent-signature-or-Icommutator-first-profile-row.md",
            "target_script": "scripts/Y5_R10_RAB_PiM_fixed_chainmap_parent_signature_or_Icommutator_first_profile_row.py",
            "task": "try to parent-sign fixed domain, metric-independent Pi_M, current-domain membership, exterior source silence, and tau/reference lock; if not, create the first concrete I_commutator profile row schema",
            "success_condition": "claim-safe Pi_M chain-map certificate, or one source-ready nonclaim I_commutator profile row with denominator/units/source-path requirements",
            "do_not": "do not use Pi_M idempotence, Hodge silence, post-readout masks, orbital-GM normalization, formalization-workbench edits, or GitHub action",
        }
    ]
    return mark_nonclaim(rows)


def validate_outputs(
    sources: list[dict[str, object]],
    attempt: list[dict[str, object]],
    profiles: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1357_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    conditional = next(row for row in attempt if row["clause_id"] == "PCZ1357_1_conditional_chainmap_lemma")
    verdict = next(row for row in attempt if row["clause_id"] == "PCZ1357_8_verdict")
    add(
        "VAL1357_1_conditional_not_promoted",
        "conditional chain-map lemma is written but not promoted",
        conditional["status"] == "CONDITIONAL_LEMMA_ONLY" and verdict["status"] == "COMMUTATOR_ZERO_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["failure_if_missing"]),
    )

    add(
        "VAL1357_2_profile_rows_present",
        "I_commutator profile rows cover domain, Hodge, current, boundary, anomaly, tau, species, and total envelope",
        len(profiles) == 8 and any(row["profile_id"] == "ICP1357_7_total_abs_profile" for row in profiles),
        f"profile_rows={len(profiles)}",
    )

    add(
        "VAL1357_3_profiles_nonclaim",
        "profile rows remain missing/unscored/nonclaim",
        all(not row["accepted_for_scoring"] and not row["claim_allowed"] and str(row["value_or_theorem"]).startswith(("MISSING", "NOT_COMPUTED")) for row in profiles),
        "all profile rows reject scoring",
    )

    guard_ids = {str(row["guard_id"]) for row in guards}
    add(
        "VAL1357_4_guardrails_installed",
        "chain-map/idempotence/Hodge/readout/normalization guardrails are installed",
        {"GUARD1357_0_chainmap_not_projector_algebra", "GUARD1357_1_no_Hodge_silencing", "GUARD1357_2_no_post_readout_mask", "GUARD1357_3_no_normalization_shortcut"}.issubset(guard_ids),
        ";".join(sorted(guard_ids)),
    )

    add(
        "VAL1357_5_claim_gates_block_claim",
        "current MTS commutator/local-GR claim gates remain blocked",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1357_0_conditional_lemma") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + attempt + profiles + guards + gates + decisions + next_target
    add(
        "VAL1357_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1357*", "*1357-Y5-R10-RAB-PiM-commutator*", "*Y5_R10_RAB_PiM_commutator*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1357_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1357_8_next_target_1358",
        "next target routes to fixed-chainmap parent signature or first profile row",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1358-Y5-R10-RAB-PiM-fixed-chainmap"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1357_9_overall",
        "overall 1357 validation",
        all(row["status"] == "PASS" for row in validations),
        "1357 records the conditional commutator-zero route and keeps I_commutator profiles nonclaim",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    attempt: list[dict[str, object]],
    profiles: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1357 writes the clean conditional route: if `Pi_M` is a parent-owned fixed topological chain-map on the physical Hilbert-current complex, then `[d,Pi_M]J_H=0`. Current MTS has not signed the needed fixed-domain, metric-independence, current-domain, exterior-silence, tau/reference, and before-readout clauses.",
            "**Main progress:** the `I_commutator` obstruction is now split into concrete source-profile channels instead of one foggy symbol. The live channels are domain motion, Hodge/metric projector variation, physical-current domain escape, boundary representative shift, parent anomaly, tau/reference drift, material/species projection, and a no-cancellation total envelope.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Pi_M commutator zero attempt",
            table(["clause_id", "claim_piece", "mathematical_form", "status", "failure_if_missing"], attempt),
            "## I_commutator source-profile rows",
            table(["profile_id", "quantity", "definition", "formula", "units_required", "affected_arenas", "value_or_theorem", "accepted_for_scoring", "status"], profiles),
            "## Chain-map guardrails",
            table(["guard_id", "guardrail", "forbidden_move", "allowed_replacement", "status"], guards),
            "## Claim gates",
            table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    attempt = commutator_attempt()
    profiles = profile_rows()
    guards = guard_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, attempt, profiles, guards, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(COMMUTATOR_ATTEMPT_PATH, attempt)
    write_csv(PROFILE_ROWS_PATH, profiles)
    write_csv(CHAINMAP_GUARD_PATH, guards)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, attempt, profiles, guards, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
