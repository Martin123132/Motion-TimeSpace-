from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_source_identity_conditional_closure_theorem_written_PiM_flux_not_parent_signed_radial_profile_template_unfilled_nonclaim"
CLAIM_CEILING = "conditional_PiM_flux_closure_theorem_only_no_radial_zero_no_cmu_zero_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "660-Y5-R10-PiM-commutator-zero-or-projector-stress-vector.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "658_doc": ROOT / "658-Y5-R10-cmu-radial-calibration-zero-or-numeric-envelope.md",
    "658_validation": RESIDUALS / "P8_Y5_BRR545_658_VALIDATION.csv",
    "658_radial_identity": RESIDUALS / "P8_Y5_R10_658_RADIAL_IDENTITY.csv",
    "658_numeric_envelope": RESIDUALS / "P8_Y5_R10_658_NUMERIC_ENVELOPE_TEMPLATE.csv",
    "657_channel_vector": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "499_parent_source_identity": ROOT / "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
    "520_ward_closure": ROOT / "520-Y5-source-current-Ward-closure-or-bound-row.md",
    "521_pim_owner": ROOT / "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
    "455_flux_closure": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
    "454_pim_algebra": ROOT / "454-PiM-parent-symplectic-projector-algebra-attempt.md",
    "458_gauss_calibration": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
    "523_gauss_orbital_score": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "source_measure_flux_map": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "pg_residual_map": RESIDUALS / "P8_PG_calibration_residual_MAP.csv",
    "pg_residual_status": RESIDUALS / "P8_PG_residual_input_STATUS.csv",
    "local_bound_matrix": RESIDUALS / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv",
}

OBSTRUCTION_CHANNELS = [
    {
        "obstruction_id": "OBS659_0_projector_commutator",
        "term": "[d,Pi_M]J_H",
        "zero_condition": "Pi_M is parent-owned and covariantly/topologically constant on the exterior mass-current complex",
        "current_status": "not_parent_signed",
        "why_open": "454/521 improve Pi_M algebra but do not prove projector commutes with exterior d or owns projector stress",
        "affected_rows": "R3;R4;R7;R8;R10;R11",
        "fallback_input": "I_commutator profile or projector-stress vector",
    },
    {
        "obstruction_id": "OBS659_1_boundary_extra_current",
        "term": "Pi_M dJ_boundary",
        "zero_condition": "boundary/class source is exact, topological harmless, or has zero absolute mass projection",
        "current_status": "not_derived",
        "why_open": "boundary no-hair/no-flux and reference subtraction are not parent-fixed",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "fallback_input": "boundary flux coefficient row",
    },
    {
        "obstruction_id": "OBS659_2_domain_projector_current",
        "term": "Pi_M dJ_domain",
        "zero_condition": "domain/projector sector has no vector, no anisotropy, no flux, and no mass projection",
        "current_status": "not_derived_high_pressure",
        "why_open": "domain projector mass remains a retained c_mu channel",
        "affected_rows": "R5;R6;R7;R8;R11",
        "fallback_input": "domain/projector product vector",
    },
    {
        "obstruction_id": "OBS659_3_bulk_memory_X_current",
        "term": "Pi_M dJ_bulk_memory_X",
        "zero_condition": "bulk/memory/X branch is source-free, mass-gapped, has zero Pi_M projection, or supplies bounded alpha(lambda)",
        "current_status": "not_derived_numeric_curve_preferred",
        "why_open": "mass gap/source charge/range curve inputs remain missing",
        "affected_rows": "R4;R10;R11",
        "fallback_input": "R10 alpha(lambda) curve and source charge integral",
    },
    {
        "obstruction_id": "OBS659_4_nonEH_source_current",
        "term": "Pi_M dJ_nonEH",
        "zero_condition": "local exterior is EH-only or non-EH source coefficients are theorem-zero/bounded",
        "current_status": "conditional_not_parent_derived",
        "why_open": "R11 non-EH vector is skeleton/fill work, not closed",
        "affected_rows": "R3;R4;R10;R11",
        "fallback_input": "R11 non-EH executable vector",
    },
    {
        "obstruction_id": "OBS659_5_coupling_frame_species_drift",
        "term": "Pi_M dJ_kappa_frame_species",
        "zero_condition": "G_eff/kappa/source frame/species labels are parent-fixed and derivative-free",
        "current_status": "not_parent_derived",
        "why_open": "same-frame closure is not a full source-calibration proof and species/time/range labels remain retained",
        "affected_rows": "R1;R2;R4;R9;R10;R11",
        "fallback_input": "source-charge/time/frame derivative residual rows",
    },
    {
        "obstruction_id": "OBS659_6_parent_anomaly_or_multiplier",
        "term": "A_parent",
        "zero_condition": "any multiplier/readout-mask/source-normalization constraint is first-class, topological, Ward-owned, or absent",
        "current_status": "not_satisfied",
        "why_open": "a multiplier that simply imposes closure is closure-only unless independently parent-owned",
        "affected_rows": "R1;R4;R7;R9;R11",
        "fallback_input": "anomaly/multiplier stress ledger",
    },
]


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": "input_or_prior_contract_for_659_PiM_flux_closure_attempt",
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def closure_identity_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "identity_id": "ID659_0_total_parent_current",
            "statement": "total parent source accounting",
            "mathematical_form": "J_tot = J_H + J_extra",
            "status": "decomposition_written",
            "proves": "all source-normalization hiding places are named",
            "does_not_prove": "Hilbert/measured mass current is separately closed",
            "parent_signed": "decomposition_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID659_1_parent_Ward",
            "statement": "total Ward/source identity",
            "mathematical_form": "dJ_tot = A_parent, with A_parent=0 only if all parent Euler/Ward/multiplier terms are owned and vanish",
            "status": "conditional_total_accounting",
            "proves": "total current can be conserved on the full parent equations",
            "does_not_prove": "A_parent=0 in the Hilbert mass channel",
            "parent_signed": "false_for_mass_channel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID659_2_product_rule",
            "statement": "projected-current product rule",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "status": "exact_identity",
            "proves": "projector commutator is a real term, not optional bookkeeping",
            "does_not_prove": "[d,Pi_M]J_H=0",
            "parent_signed": "identity_not_zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID659_3_obstruction_identity",
            "statement": "parent source identity for the Hilbert mass channel",
            "mathematical_form": "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "status": "derived_as_exact_decomposition_not_zero",
            "proves": "radial source hair is exactly extra-current projection plus Pi_M commutator plus parent anomaly",
            "does_not_prove": "any obstruction term vanishes",
            "parent_signed": "identity_not_zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID659_4_conditional_zero_theorem",
            "statement": "closed projected mass flux theorem",
            "mathematical_form": "Pi_M dJ_extra=0 and [d,Pi_M]J_H=0 and A_parent=0 => d(Pi_M J_H)=0",
            "status": "conditional_theorem_proved",
            "proves": "the exact sufficient conditions for epsilon_radial_Meff=0",
            "does_not_prove": "the current parent action satisfies the sufficient conditions",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "ID659_5_radial_profile_law",
            "statement": "fallback radial profile law",
            "mathematical_form": "epsilon_radial_Meff = c_M/M_eff_ref integral_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
            "status": "exact_template_formula_written",
            "proves": "if the theorem fails, the missing input is a bounded source-current integral",
            "does_not_prove": "the profile is zero or below local locks",
            "parent_signed": "identity_not_numeric",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def obstruction_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            **row,
            "zero_signed": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for row in OBSTRUCTION_CHANNELS
    ]


def radial_profile_template_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "template_id": "RPF659_0_total_parent_radial_integral",
            "required_quantity": "I_parent_radial",
            "definition": "integral_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
            "required_columns": "system_id;r1;r2;c_M;M_eff_ref;I_parent_radial;norm_convention;units;source_file;assumptions",
            "maps_to": "epsilon_radial_Meff=c_M*I_parent_radial/M_eff_ref; R4;R10;R11",
            "current_status": "MISSING_PARENT_SOURCE_IDENTITY_OR_NUMERIC_INTEGRAL",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "RPF659_1_commutator_integral",
            "required_quantity": "I_commutator",
            "definition": "integral_A [d,Pi_M]J_H",
            "required_columns": "system_id;projector_type;projector_owner_status;I_commutator;units;source_file;assumptions",
            "maps_to": "projector stress; radial source hair; R3;R4;R7;R8;R10;R11",
            "current_status": "MISSING_COMMUTATOR_ZERO_OR_PROJECTOR_STRESS_VECTOR",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "RPF659_2_extra_channel_integrals",
            "required_quantity": "I_extra_by_channel",
            "definition": "integral_A Pi_M dJ_extra split by boundary/domain/bulk/nonEH/kappa/frame/species/memory",
            "required_columns": "system_id;channel;I_extra;units;affected_rows;source_file;assumptions",
            "maps_to": "c_mu eight-channel vector; R1;R4;R7;R8;R9;R10;R11",
            "current_status": "MISSING_EXTRA_CURRENT_ZERO_OR_CHANNEL_INTEGRALS",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "RPF659_3_parent_anomaly_integral",
            "required_quantity": "I_anomaly",
            "definition": "integral_A A_parent",
            "required_columns": "system_id;anomaly_or_multiplier_term;owner_status;I_anomaly;units;source_file;assumptions",
            "maps_to": "closure-only anomaly/multiplier ledger; R1;R4;R7;R9;R11",
            "current_status": "MISSING_PARENT_ANOMALY_ZERO_OR_SOURCE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "template_id": "RPF659_4_observable_radial_bound",
            "required_quantity": "radial_measured_GM_bound",
            "definition": "empirical or derived envelope for dln(mu_obs)/dlnr or finite-shell Delta mu/mu",
            "required_columns": "system_id;r_or_shell;mu_obs_proxy;dln_mu_dlnr_or_delta_mu;bound_source;units;source_file;assumptions",
            "maps_to": "R4 beta/source hair; R10 fifth-force/radial profile; R11 source-normalization ledger",
            "current_status": "MISSING_OBSERVABLE_RADIAL_BOUND_OR_MAPPING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows(
    identity_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    unsigned_obstructions = [row for row in obstruction_rows if row["zero_signed"] == "false"]
    return [
        {
            "gate_id": "G659_0_obstruction_identity",
            "gate": "exact d(Pi_M J_H) obstruction identity is written",
            "result": "pass_identity",
            "detail": "d(Pi_M J_H)=-Pi_M dJ_extra+[d,Pi_M]J_H+A_parent",
            "claim_effect": "identity only; not radial-zero proof",
            "generated_utc": now,
        },
        {
            "gate_id": "G659_1_conditional_zero_theorem",
            "gate": "finite sufficient conditions for closed PiM flux are written",
            "result": "pass_conditional",
            "detail": "Pi_M dJ_extra=0; [d,Pi_M]J_H=0; A_parent=0",
            "claim_effect": "theorem target exists but premises are unsigned",
            "generated_utc": now,
        },
        {
            "gate_id": "G659_2_parent_signed_zero",
            "gate": "all obstruction terms are parent-signed zero",
            "result": "blocked",
            "detail": f"unsigned_obstructions={len(unsigned_obstructions)}",
            "claim_effect": "blocks epsilon_radial_Meff=0",
            "generated_utc": now,
        },
        {
            "gate_id": "G659_3_radial_profile_numeric",
            "gate": "radial profile fallback has sourced numeric/theorem inputs",
            "result": "blocked",
            "detail": f"template_rows={len(template_rows)}; all current_status values are MISSING_*",
            "claim_effect": "blocks R4/R10/R11 scoring",
            "generated_utc": now,
        },
        {
            "gate_id": "G659_4_total_Ward_overclaim_guard",
            "gate": "total Ward conservation is not counted as Hilbert mass-channel closure",
            "result": "pass_policy",
            "detail": "dJ_tot=0 still permits exchange between J_H and J_extra",
            "claim_effect": "prevents fake Newton/source-normalization pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G659_5_multiplier_closure_guard",
            "gate": "a closure multiplier is not accepted unless parent-owned",
            "result": "pass_policy",
            "detail": "imposing d(Pi_M J_H)=0 by hand is closure-only",
            "claim_effect": "blocks circular proof",
            "generated_utc": now,
        },
        {
            "gate_id": "G659_6_claim_guard",
            "gate": "no row is score-ready or claim-valid",
            "result": "pass",
            "detail": "score_ready_true=0; valid_for_claim_true=0",
            "claim_effect": CLAIM_CEILING,
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D659_0_conditional_theorem",
            "status": "proved_as_conditional_theorem",
            "meaning": "closed projected mass flux follows if extra-current projection, PiM commutator, and parent anomaly all vanish",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D659_1_parent_proof",
            "status": "not_parent_signed",
            "meaning": "current corpus has not proved the three zero premises, so epsilon_radial_Meff is not theorem-zero",
            "claim_status": "false",
            "next_action": "attack the PiM commutator first because it is upstream of every projected-current proof",
            "generated_utc": now,
        },
        {
            "decision_id": "D659_2_numeric_fallback",
            "status": "template_written_unfilled",
            "meaning": "if the commutator/extra/anomaly route fails, the exact radial integral must be filled or bounded",
            "claim_status": "false",
            "next_action": "do not score until source paths and units exist",
            "generated_utc": now,
        },
        {
            "decision_id": "D659_3_local_GR",
            "status": "blocked",
            "meaning": "local GR remains blocked because radial source normalization and measured-GM calibration are not closed",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    count = 0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            if mtime > FORMALIZATION_CUTOFF:
                count += 1
    return count


def validation_rows(
    source_rows: list[dict[str, str]],
    prior_validation_658: list[dict[str, str]],
    radial_identity_658: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = [row for row in prior_validation_658 if row.get("result") != "pass"]
    claim_rows = []
    for group in (identity_rows, obstruction_rows, template_rows, gate_rows, decision):
        claim_rows.extend(
            [row for row in group if row.get("valid_for_claim") == "true" or row.get("claim_status") == "true"]
        )
    generic_fill_markers = []
    for group in (identity_rows, obstruction_rows, template_rows, gate_rows, decision):
        for row in group:
            for value in row.values():
                if isinstance(value, str) and "fill_" in value.lower():
                    generic_fill_markers.append(value)
    blocked_gates = [row for row in gate_rows if row["result"] == "blocked"]
    formalization_changed = formalization_changed_count()
    checks = [
        (
            "V659_0_source_paths_exist",
            not missing_sources,
            "all cited local source paths exist" if not missing_sources else f"missing={';'.join(missing_sources)}",
        ),
        (
            "V659_1_prior_658_validation_clean",
            not prior_failures,
            "658 validation remains clean" if not prior_failures else f"658_failures={len(prior_failures)}",
        ),
        (
            "V659_2_radial_identity_imported",
            any(row.get("radial_id") == "RAD658_3_normalized_residual" for row in radial_identity_658),
            "658 normalized radial residual loaded",
        ),
        (
            "V659_3_obstruction_identity_written",
            any("-Pi_M dJ_extra" in row["mathematical_form"] for row in identity_rows),
            "d(Pi_M J_H) obstruction identity written",
        ),
        (
            "V659_4_conditional_zero_theorem_written",
            any("Pi_M dJ_extra=0" in row["mathematical_form"] and row["status"] == "conditional_theorem_proved" for row in identity_rows),
            "conditional zero theorem written",
        ),
        (
            "V659_5_obstruction_coverage",
            len(obstruction_rows) == 7,
            f"obstruction_rows={len(obstruction_rows)}",
        ),
        (
            "V659_6_zero_not_parent_signed",
            all(row["zero_signed"] == "false" for row in obstruction_rows),
            "all obstruction zero claims remain unsigned/nonclaim",
        ),
        (
            "V659_7_radial_profile_template_unfilled",
            len(template_rows) == 5 and all(row["current_status"].startswith("MISSING_") for row in template_rows),
            f"template_rows={len(template_rows)}",
        ),
        (
            "V659_8_scoreability_blocked",
            len(blocked_gates) >= 2,
            f"blocked_gates={len(blocked_gates)}",
        ),
        (
            "V659_9_no_claim_rows",
            not claim_rows,
            f"claim_rows={len(claim_rows)}",
        ),
        (
            "V659_10_no_generic_fill_placeholders",
            not generic_fill_markers,
            f"fill_markers={len(generic_fill_markers)}",
        ),
        (
            "V659_11_next_target_selected",
            NEXT_TARGET.startswith("660-") and "PiM-commutator" in NEXT_TARGET,
            NEXT_TARGET,
        ),
        (
            "V659_12_claim_ceiling_active",
            CLAIM_CEILING.startswith("conditional_PiM_flux_closure_theorem_only"),
            CLAIM_CEILING,
        ),
        (
            "V659_13_formalization_workbench_untouched",
            formalization_changed == 0,
            f"formalization_changed_after_cutoff={formalization_changed}",
        ),
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


def nonclaim_summary_rows(
    identity_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "identity_rows": len(identity_rows),
            "obstruction_rows": len(obstruction_rows),
            "radial_template_rows": len(template_rows),
            "blocked_scoreability_gates": sum(1 for row in gate_rows if row["result"] == "blocked"),
            "validation_failures": sum(1 for row in validation if row["result"] != "pass"),
            "next_target": NEXT_TARGET,
            "generated_utc": generated_utc(),
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str], limit: int | None = None) -> str:
    visible_rows = rows if limit is None else rows[:limit]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in visible_rows
    ]
    if limit is not None and len(rows) > limit:
        body.append("| " + " | ".join(["..."] * len(columns)) + " |")
    return "\n".join([header, separator, *body])


def write_document(
    source_rows: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 659 Y5/R10: Parent Source Identity For Closed PiM Flux Or Radial Profile Fill

## Verdict

Status: `{STATUS}`.

The proof attempt succeeds as a conditional theorem and fails as a parent-signed MTS theorem. We can now state exactly what would close the radial source-normalization channel:

`Pi_M dJ_extra = 0`, `[d,Pi_M]J_H = 0`, and `A_parent = 0`.

Those premises are not yet signed by the parent action, so `epsilon_radial_Meff` is not zero-claimed.

## Source Register

{markdown_table(source_rows, ["source_id", "exists", "role"], limit=20)}

## Closure Identity

{markdown_table(identity_rows, ["identity_id", "statement", "mathematical_form", "status", "parent_signed", "valid_for_claim"])}

## Obstruction Audit

{markdown_table(obstruction_rows, ["obstruction_id", "term", "zero_condition", "current_status", "affected_rows", "zero_signed", "valid_for_claim"])}

## Radial Profile Template

{markdown_table(template_rows, ["template_id", "required_quantity", "definition", "current_status", "score_ready", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "identity_rows", "obstruction_rows", "radial_template_rows", "blocked_scoreability_gates", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is a useful failure. Total Ward conservation is not enough, because the observed Hilbert mass current can exchange charge with hidden/source-normalization sectors. The exact obstruction is:

`d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent`.

That means the next best move is upstream: kill the commutator first. If `Pi_M` is not parent-owned/topological/covariantly constant, every later flux proof carries projector stress hair.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    prior_validation_658 = read_csv(SOURCE_PATHS["658_validation"])
    radial_identity_658 = read_csv(SOURCE_PATHS["658_radial_identity"])

    identity_rows = closure_identity_rows()
    obstruction_rows = obstruction_audit_rows()
    template_rows = radial_profile_template_rows()
    gate_rows = scoreability_gate_rows(identity_rows, obstruction_rows, template_rows)
    decision = decision_rows()
    validation = validation_rows(
        source_rows,
        prior_validation_658,
        radial_identity_658,
        identity_rows,
        obstruction_rows,
        template_rows,
        gate_rows,
        decision,
    )
    summary_rows = nonclaim_summary_rows(identity_rows, obstruction_rows, template_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_659_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_659_CLOSURE_IDENTITY.csv",
        identity_rows,
        [
            "identity_id",
            "statement",
            "mathematical_form",
            "status",
            "proves",
            "does_not_prove",
            "parent_signed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_659_OBSTRUCTION_AUDIT.csv",
        obstruction_rows,
        [
            "obstruction_id",
            "term",
            "zero_condition",
            "current_status",
            "why_open",
            "affected_rows",
            "fallback_input",
            "zero_signed",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_659_RADIAL_PROFILE_TEMPLATE.csv",
        template_rows,
        [
            "template_id",
            "required_quantity",
            "definition",
            "required_columns",
            "maps_to",
            "current_status",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_659_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_659_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_659_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "identity_rows",
            "obstruction_rows",
            "radial_template_rows",
            "blocked_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_659_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(
        source_rows,
        identity_rows,
        obstruction_rows,
        template_rows,
        gate_rows,
        decision,
        summary_rows,
        validation,
    )

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"identity_rows={len(identity_rows)}")
    print(f"obstruction_rows={len(obstruction_rows)}")
    print(f"radial_template_rows={len(template_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
