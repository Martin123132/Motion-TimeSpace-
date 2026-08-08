from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1360"
TITLE = "1360-Y5-R10-RAB-selector-action-locality-differentiability-or-MHref-surface-intake"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
LOCALITY_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_SELECTOR_LOCALITY_DIFFERENTIABILITY_ATTEMPT.csv"
STRESS_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_SELECTOR_STRESS_LEDGER.csv"
MHREF_SURFACE_INTAKE_PATH = OUT_DIR / f"{PACK_ID}_MHREF_SURFACE_INTAKE_ROWS.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1360_VALIDATION.csv"


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
            "source_id": "SRC1360_0_1359_doc",
            "source_path": "1359-Y5-R10-RAB-parent-topological-selector-action-or-Icommutator-source-intake.md",
            "required_anchor": "PSA1359_7_verdict",
            "purpose": "1359 blocks selector-action derivation and selects locality/differentiability test.",
        },
        {
            "source_id": "SRC1360_1_1359_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1359_NEXT_TARGET.csv",
            "required_anchor": "NEXT1359_0_1360",
            "purpose": "handoff to 1360.",
        },
        {
            "source_id": "SRC1360_2_1359_obstructions",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1359_SELECTOR_ACTION_OBSTRUCTION_LEDGER.csv",
            "required_anchor": "PSO1359_1_nonlocal_support",
            "purpose": "nonlocal support, selector stress, wrong-charge, and denominator obstruction rows.",
        },
        {
            "source_id": "SRC1360_3_1359_intake",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv",
            "required_anchor": "ISI1359_3_denominator",
            "purpose": "M_H_ref and S1/S2 source-intake requirements.",
        },
        {
            "source_id": "SRC1360_4_domain_clause",
            "source_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
            "required_anchor": "C0_parent_domain_sector",
            "purpose": "prior scalar-domain selector clause with auxiliary chi_D/lambda_D.",
        },
        {
            "source_id": "SRC1360_5_domain_variation",
            "source_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
            "required_anchor": "V2_metric_variation",
            "purpose": "metric variation and selector stress chain.",
        },
        {
            "source_id": "SRC1360_6_domain_gate",
            "source_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_GATE.csv",
            "required_anchor": "G1_parent_derivation",
            "purpose": "prior domain selector gate says clause is not parent-derived.",
        },
        {
            "source_id": "SRC1360_7_1016_doc",
            "source_path": "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "required_anchor": "PSC1016_3_support_selector",
            "purpose": "source-worldtube selector and M_H_ref schema.",
        },
        {
            "source_id": "SRC1360_8_1017_doc",
            "source_path": "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            "required_anchor": "HRL1017_5_MHref_denominator",
            "purpose": "same-frame Hamiltonian denominator remains blocked.",
        },
        {
            "source_id": "SRC1360_9_942_doc",
            "source_path": "942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md",
            "required_anchor": "SEL942_3_support_selector",
            "purpose": "conditional worldtube selector theorem and same-frame blockers.",
        },
        {
            "source_id": "SRC1360_10_687_tau",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv",
            "required_anchor": "STT687_4_tau_normalization",
            "purpose": "selector-to-tau attempt blocks tau normalization.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def locality_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "SLD1360_0_support_selector_nonlocality",
            "test": "W_M = closure(supp J_H[tau]) as an action ingredient",
            "mathematical_form": "W_M[Phi,psi,tau] := closure supp star(T_obs(tau,.))",
            "result": "NONLOCAL_NONSMOOTH_AS_ACTION_VARIABLE",
            "reason": "support/closure is a global set operation and its variation generally produces shape/boundary terms",
            "fallback": "use source-intake rows for S1/S2/domain derivative instead of a claim",
        },
        {
            "attempt_id": "SLD1360_1_local_chi_proxy",
            "test": "replace support by a local scalar selector field chi_M",
            "mathematical_form": "S_selector includes integral sqrt(-g) lambda_M(chi_M-Sigma_M) plus topological constraints",
            "result": "LOCAL_PROXY_POSSIBLE_BUT_AUXILIARY",
            "reason": "this can be written locally, but it introduces a new selector sector unless chi_M/Sigma_M are derived from existing MTS variables",
            "fallback": "label as extension/closure until parent origin is shown",
        },
        {
            "attempt_id": "SLD1360_2_covariant_closed_representative",
            "test": "closed normalized omega_M_top as local/covariant form",
            "mathematical_form": "d omega_M_top=0 and integral_link omega_M_top=1 enforced by multiplier or cohomology class",
            "result": "TOPOLOGICAL_GLOBAL_CONSTRAINT",
            "reason": "closure can be enforced, but normalization and same-worldtube PD identity are global/cohomological and can still conserve the wrong object",
            "fallback": "retain wrong-charge and source-measure equality gates",
        },
        {
            "attempt_id": "SLD1360_3_differentiable_domain",
            "test": "differentiability of W_M/A_ext/S1/S2 under metric, source, and frame variations",
            "mathematical_form": "delta W_M=0, delta[S_i]_M=0, or explicit shape derivative terms included",
            "result": "NOT_SIGNED_FOR_CURRENT_MTS",
            "reason": "compact regular support, fixed homology, and readout independence are not parent-signed",
            "fallback": "start S1/S2 and annulus source-intake rows",
        },
        {
            "attempt_id": "SLD1360_4_no_new_selector_stress",
            "test": "selector action has zero or bounded metric stress",
            "mathematical_form": "T_selector^{mu nu}:=-2/sqrt(-g) delta S_selector/delta g_munu = 0 or source-bounded",
            "result": "NOT_DERIVED",
            "reason": "chi/lambda/topological multiplier/boundary terms can carry stress unless double-zero and metric-independence clauses are parent-derived",
            "fallback": "retain selector-stress ledger and PPN/local-GR blocks",
        },
        {
            "attempt_id": "SLD1360_5_covariant_same_frame",
            "test": "selector uses the same observed coframe, tau, matter current, and charge readout",
            "mathematical_form": "e_obs=E[Phi], J_H[tau]=star(T_obs(tau,.)), tau_source=tau_charge=tau_clock=tau_readout",
            "result": "BLOCKED_BY_FRAME_TAU_LOCK",
            "reason": "942 and 687 keep unique observed frame and tau normalization as open gates",
            "fallback": "next target should attack observed coframe/tau/source-frame lock or source rows",
        },
        {
            "attempt_id": "SLD1360_6_MHref_denominator",
            "test": "selector residuals can be normalized by a same-frame Hamiltonian source denominator",
            "mathematical_form": "M_H_ref=G_ref^-1 int_S Q_tau^MTS with fixed H_ref and tau",
            "result": "MISSING_MHREF",
            "reason": "1017 blocks M_H_ref, integrability, reference, boundary flux, and tau lock",
            "fallback": "start M_H_ref intake row as nonclaim",
        },
        {
            "attempt_id": "SLD1360_7_verdict",
            "test": "selector action locality/differentiability/no-stress certificate for current MTS",
            "mathematical_form": "SLD1360_0 through SLD1360_6 all pass with parent evidence",
            "result": "CERTIFICATE_NOT_PROVED",
            "reason": "local proxy exists only as an auxiliary template; nonlocal support, domain differentiability, stress, frame/tau, and M_H_ref remain open",
            "fallback": "create nonclaim M_H_ref and S1/S2 source-intake rows",
        },
    ]
    return mark_nonclaim(rows)


def stress_ledger() -> list[dict[str, object]]:
    rows = [
        {
            "stress_id": "SSL1360_0_chi_lambda_bulk",
            "source": "chi_M/lambda_M selector constraint",
            "stress_form": "T_chi_lambda from delta_g integral sqrt(-g) lambda_M(chi_M-Sigma_M)",
            "current_status": "OPEN",
            "required_to_close": "derive chi=lambda=0 double-zero or compute/bound T_chi_lambda",
        },
        {
            "stress_id": "SSL1360_1_shape_boundary",
            "source": "moving support boundary partial W_M",
            "stress_form": "shape derivative and delta-function boundary terms from delta W_M",
            "current_status": "OPEN",
            "required_to_close": "prove fixed smooth worldtube support and no readout/domain motion",
        },
        {
            "stress_id": "SSL1360_2_topological_multiplier",
            "source": "d omega_M_top and normalization multipliers",
            "stress_form": "boundary/cohomology multiplier response and representative variation",
            "current_status": "OPEN",
            "required_to_close": "prove metric-independent representative with zero boundary variation",
        },
        {
            "stress_id": "SSL1360_3_Hodge_metric_projector",
            "source": "any Hodge/DeWitt fallback for Pi_M",
            "stress_form": "delta_g Pi_M and induced T_PiM^{mu nu}",
            "current_status": "OPEN",
            "required_to_close": "avoid Hodge route or compute projector-stress map",
        },
        {
            "stress_id": "SSL1360_4_tau_frame",
            "source": "observed coframe/tau source-frame mismatch",
            "stress_form": "Delta_frame_source and Delta_tau contributions to source normalization",
            "current_status": "OPEN",
            "required_to_close": "single observed coframe and tau/source/charge/readout lock",
        },
        {
            "stress_id": "SSL1360_5_reference_denominator",
            "source": "H_ref and M_H_ref normalization",
            "stress_form": "Delta_ref, symplectic boundary flux, and denominator drift",
            "current_status": "OPEN",
            "required_to_close": "integrable H_tau, fixed H_ref, B_zero_flux/Delta_symp control, positive M_H_ref",
        },
    ]
    return mark_nonclaim(rows)


def mhref_surface_intake() -> list[dict[str, object]]:
    rows = [
        {
            "intake_id": "MSI1360_0_M_H_ref_denominator",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "M_H_ref",
            "required_columns": "system_id;tau_id;surface_outer;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_M_H_REF",
            "units": "mass_or_energy_source_charge",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "MSI1360_1_inner_surface_S1",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "S1_or_r1",
            "required_columns": "system_id;surface_inner_id;r1;surface_definition;links_W_M;fixed_before_readout;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_INNER_RADIUS_OR_SURFACE",
            "units": "length_or_surface_identifier",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "MSI1360_2_outer_surface_S2",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "S2_or_r2",
            "required_columns": "system_id;surface_outer_id;r2;surface_definition;homology_class;fixed_before_readout;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_OUTER_RADIUS_OR_SURFACE",
            "units": "length_or_surface_identifier",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "MSI1360_3_annulus_homology",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "A_ext_and_homology_class",
            "required_columns": "system_id;annulus_A;boundary_relation;S1_homology;S2_homology;exterior_source_free;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_ANNULUS_HOMOLOGY_SOURCE",
            "units": "topological_class_plus_domain_metadata",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "MSI1360_4_tau_frame_lock",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "tau_frame_lock",
            "required_columns": "system_id;e_obs_id;tau_source;tau_charge;tau_clock;tau_readout;lock_certificate;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_TAU_FRAME_LOCK",
            "units": "dimensionless_certificate_or_bound",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "MSI1360_5_Qtau_integrability",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "Q_tau_integrability_and_reference",
            "required_columns": "system_id;delta_H_tau_curl;Q_tau_integral;H_ref;Delta_ref;B_zero_flux;Delta_symp;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_QTAU_INTEGRABILITY_REFERENCE",
            "units": "mass_or_energy_source_charge",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "MSI1360_6_domain_numerator",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "int_A_dPiM_domain_JH",
            "required_columns": "system_id;annulus_A;dPiM_domain;J_H_source;integral_value;M_H_ref;normalization;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_INT_A_DPiM_DOMAIN_JH",
            "units": "same_as_M_H_ref_before_normalization",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "MSI1360_7_acceptance_gate",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "quantity": "first_profile_acceptance_gate",
            "required_columns": "all_required_items_present;no_MISSING_markers;units_compatible;all_sources_verified;anti_cheat_flags_true;valid_for_claim",
            "current_value": "BLOCKED",
            "units": "dimensionless_after_M_H_ref_normalization",
            "status": "CLAIM_BLOCKED",
        },
    ]
    return mark_nonclaim(rows)


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1360_0_local_proxy_written",
            "claim": "a local scalar selector proxy can be written as a contract",
            "gate_pass": True,
            "reason": "chi/lambda style selector is a known local template, but this is not parent derivation",
        },
        {
            "gate_id": "GATE1360_1_selector_certificate",
            "claim": "selector action is local/covariant/differentiable/no-stress for current MTS",
            "gate_pass": False,
            "reason": "support nonlocality, shape variation, selector stress, frame/tau lock, and M_H_ref remain open",
        },
        {
            "gate_id": "GATE1360_2_MHref_source_ready",
            "claim": "M_H_ref denominator is source-backed and valid",
            "gate_pass": False,
            "reason": "Q_tau, H_ref, tau lock, and source path are missing",
        },
        {
            "gate_id": "GATE1360_3_surface_intake_ready",
            "claim": "S1/S2 and annulus homology are source-backed and fixed before readout",
            "gate_pass": False,
            "reason": "inner/outer surfaces and annulus homology rows are missing source input",
        },
        {
            "gate_id": "GATE1360_4_Icommutator_score_ready",
            "claim": "first I_commutator profile row can be scored",
            "gate_pass": False,
            "reason": "M_H_ref, surfaces, numerator, units, provenance, and anti-cheat flags are not complete",
        },
        {
            "gate_id": "GATE1360_5_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "reason": "selector, chain-map, M_H_ref, R_eq/B_zero, calibration, and PPN stability remain blocked",
        },
    ]
    return mark_nonclaim(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1360_0_local_proxy_not_enough",
            "decision": "A local selector proxy is possible, but not enough.",
            "why": "chi/lambda constraints can be written locally, yet they add an auxiliary sector unless parent-derived",
            "next_action": "do not promote the selector action without a parent-origin theorem",
        },
        {
            "decision_id": "DEC1360_1_selector_certificate_fails",
            "decision": "Selector locality/differentiability/no-stress certificate fails for current MTS.",
            "why": "support nonlocality, domain shape variation, topological boundary terms, and selector stress remain open",
            "next_action": "keep selector stress and I_commutator rows active",
        },
        {
            "decision_id": "DEC1360_2_intake_started",
            "decision": "M_H_ref and surface intake rows are now staged.",
            "why": "this gives a non-circular fallback path for the first I_commutator profile row",
            "next_action": "try observed coframe/tau/source-frame lock or source the denominator/surface rows",
        },
    ]
    return mark_nonclaim(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1360_0_1361",
            "target_file": "1361-Y5-R10-RAB-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
            "target_script": "scripts/Y5_R10_RAB_observed_coframe_tau_source_frame_lock_or_MHref_first_row.py",
            "task": "try to parent-sign one observed coframe and tau/source/charge/readout lock needed for M_H_ref; if not, fill the first nonclaim M_H_ref source-row schema",
            "success_condition": "same-frame coframe/tau lock theorem, or a complete nonclaim M_H_ref first-row schema with Q_tau/H_ref/surface/source requirements",
            "do_not": "do not use orbital GM, bare mass, reference-only 1, post-readout frame choice, formalization-workbench edits, or GitHub action",
        }
    ]
    return mark_nonclaim(rows)


def validate_outputs(
    sources: list[dict[str, object]],
    locality: list[dict[str, object]],
    stress: list[dict[str, object]],
    intake: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1360_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in locality if row["attempt_id"] == "SLD1360_7_verdict")
    add(
        "VAL1360_1_selector_certificate_not_promoted",
        "selector locality/differentiability/no-stress certificate is not promoted",
        verdict["result"] == "CERTIFICATE_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["reason"]),
    )

    add(
        "VAL1360_2_stress_ledger_open",
        "selector stress ledger has open bulk/boundary/topological/Hodge/frame/reference rows",
        len(stress) == 6 and all(row["current_status"] == "OPEN" and not row["claim_allowed"] for row in stress),
        f"stress_rows={len(stress)}",
    )

    required_intake = {
        "MSI1360_0_M_H_ref_denominator",
        "MSI1360_1_inner_surface_S1",
        "MSI1360_2_outer_surface_S2",
        "MSI1360_3_annulus_homology",
        "MSI1360_4_tau_frame_lock",
        "MSI1360_5_Qtau_integrability",
        "MSI1360_6_domain_numerator",
        "MSI1360_7_acceptance_gate",
    }
    add(
        "VAL1360_3_MHref_surface_intake_complete",
        "M_H_ref and S1/S2 intake rows are present with missing fields explicit",
        required_intake.issubset({str(row["intake_id"]) for row in intake}),
        f"intake_rows={len(intake)}",
    )

    add(
        "VAL1360_4_intake_nonclaim_missing",
        "intake rows remain missing/blocked/nonclaim",
        all(not row["claim_allowed"] and str(row["status"]) in {"MISSING_SOURCE_INPUT", "CLAIM_BLOCKED"} for row in intake),
        "no M_H_ref/surface row can score",
    )

    add(
        "VAL1360_5_claim_gates_block_claim",
        "selector certificate, MHref, surface, Icommutator, and local-GR claims remain blocked",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1360_0_local_proxy_written") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + locality + stress + intake + gates + decisions + next_target
    add(
        "VAL1360_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1360*", "*1360-Y5-R10-RAB-selector-action-locality*", "*Y5_R10_RAB_selector_action_locality*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1360_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1360_8_next_target_1361",
        "next target routes to observed coframe/tau/source-frame lock or MHref first row",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1361-Y5-R10-RAB-observed-coframe"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1360_9_overall",
        "overall 1360 validation",
        all(row["status"] == "PASS" for row in validations),
        "1360 blocks selector-locality certificate and stages M_H_ref/S1/S2 intake rows",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    locality: list[dict[str, object]],
    stress: list[dict[str, object]],
    intake: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1360 does not certify the selector action as local/covariant/differentiable/no-stress for current MTS. A local `chi/lambda` proxy can be written, but without parent origin it is an auxiliary closure sector, while `W_M=supp(J_H)` remains nonlocal and shape-sensitive.",
            "**Main progress:** the failure is productive: selector stress channels are explicit, and the fallback source-intake path now starts with `M_H_ref`, S1/S2 surfaces, annulus homology, tau/frame lock, Q_tau integrability, and the domain-commutator numerator.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Selector locality/differentiability attempt",
            table(["attempt_id", "test", "mathematical_form", "result", "reason", "fallback"], locality),
            "## Selector stress ledger",
            table(["stress_id", "source", "stress_form", "current_status", "required_to_close"], stress),
            "## MHref and surface intake rows",
            table(["intake_id", "row_ref", "quantity", "required_columns", "current_value", "units", "status"], intake),
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
    locality = locality_attempt()
    stress = stress_ledger()
    intake = mhref_surface_intake()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, locality, stress, intake, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(LOCALITY_ATTEMPT_PATH, locality)
    write_csv(STRESS_LEDGER_PATH, stress)
    write_csv(MHREF_SURFACE_INTAKE_PATH, intake)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, locality, stress, intake, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
