from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3563-Y5-R2FR-parent-sort-disjointness-active-source-prefactor-proof-or-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PARENT_SORT_DISJOINTNESS_ASP_3563"
CHECKPOINT_ID = "3563"


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


def sources() -> dict[str, Path]:
    return {
        "handoff_3562": RESIDUALS / "P8_Y5_R2FR_3562_NEXT_TARGET.csv",
        "nohom_theorem_3562": RESIDUALS / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv",
        "source_weight_bounds_3562": RESIDUALS / "P8_Y5_R2FR_3562_BOUND_VECTOR.csv",
        "nohom_attempt_1896": RESIDUALS / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv",
        "deltaw_basis_1896": RESIDUALS / "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
        "nohom_constructor_2651": RESIDUALS / "P8_Y5_NOHOM_DELTABASIS_2651_PARENT_SORT_NOHOM_CONSTRUCTOR_ATTEMPT.csv",
        "sort_requirements_2686": RESIDUALS / "P8_Y5_R2FR_2686_SORT_DISJOINTNESS_NOHOM_REQUIREMENTS_NONCLAIM.csv",
        "sort_constructor_2688": RESIDUALS / "P8_Y5_R2FR_2688_PARENT_SORT_CONSTRUCTOR_AUDIT.csv",
        "sort_impact_2688": RESIDUALS / "P8_Y5_R2FR_2688_SORT_TO_NOHOM_IMPACT_LEDGER.csv",
        "normal_form_2485": RESIDUALS / "P8_Y5_PARENT_NORMAL_FORM_2485_FIELD_SORT_TABLE.csv",
        "hom_audit_2612": RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
        "source_prefactor_classes_2612": RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        "density_theorem_3561": RESIDUALS / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3562": "declares 3563 target",
        "nohom_theorem_3562": "imports conditional no-Hom theorem",
        "source_weight_bounds_3562": "imports source-weight fallback rows",
        "nohom_attempt_1896": "earlier parent sort disjointness proof attempt",
        "deltaw_basis_1896": "finite Delta_w component basis and no-cancellation policy",
        "nohom_constructor_2651": "constructor-level no-Hom attempt",
        "sort_requirements_2686": "requirements for sort disjointness no-Hom promotion",
        "sort_constructor_2688": "parent sort constructor audit from MTS primitives",
        "sort_impact_2688": "impact ledger selecting source-label forgetting/fallback",
        "normal_form_2485": "parent normal-form sort table",
        "hom_audit_2612": "no-source-only Hom audit",
        "source_prefactor_classes_2612": "source-prefactor class/countermodel split",
        "density_theorem_3561": "density pullback theorem and countermodel context",
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


def constructor_theorem(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PSD3563_0_constructor_signature",
            "name": "parent sort constructor signature",
            "statement": "A parent constructor C_MTS must generate public geometry Q_obs, ordinary matter fields, representation constants, gauge/current data, universal calibration, readout maps and explicit residual slots before fitting.",
            "proof_or_derivation": "This is the minimum object-language signature needed for a no-Hom theorem to be a theorem rather than a syntax preference.",
            "required_premises": "MTS primitives generate all source/action arguments; constructor exhaustion; variation-before-readout",
            "current_status": "TARGET_SHARP_NOT_PARENT_DERIVED",
            "effect": "defines what would have to be proved",
            "source_path": str(source_paths["sort_constructor_2688"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PSD3563_1_conditional_disjointness_proof",
            "name": "conditional active-source-prefactor disjointness proof",
            "statement": "If ActiveSourcePrefactor is not a primitive parent sort and the only scalar endomorphism of the action-density line is common calibration, then no non-common Hom from SpeciesLabel, HiddenMarker, ReadoutSelector or WorldtubeSelector to ActiveSourcePrefactor exists.",
            "proof_or_derivation": "By constructor exhaustion, every well-typed source coefficient must be generated by an allowed constructor argument. Species labels and hidden/readout selectors are not arguments of the active source coefficient constructor. A common scalar endomorphism acts on the whole action-density line and is not a relative source coefficient.",
            "required_premises": "constructor exhaustion; active source coefficient domain excludes labels/markers/readout; single action-density line",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "effect": "would theorem-zero delta_w_species, kappa_A_source, hidden_marker_source and Delta_mask",
            "source_path": str(source_paths["nohom_constructor_2651"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PSD3563_2_product_sequester_corollary",
            "name": "product-category source-label forgetting corollary",
            "statement": "If C_parent factors into visible source data times bookkeeping labels and the source coefficient functor factors only through the visible projection, label tangents annihilate active-source coefficients.",
            "proof_or_derivation": "For F_source=Fbar(pi_vis(-)), D_label F_source=dFbar(D pi_vis(v_label))=0. This is the chain-rule form of source-label forgetting.",
            "required_premises": "product/sequester factorization derived from MTS primitives; source coefficient functor factors through visible data",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "effect": "alternative proof route to the same no-Hom result",
            "source_path": str(source_paths["nohom_attempt_1896"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PSD3563_3_counterexample_obstruction",
            "name": "constructor counterexample obstruction",
            "statement": "If parent constructor exhaustion is absent, species constants, hidden invariant scalars, domain/material markers, boundary masks, action-scale coefficients and readout selectors can still be legal active-source coefficient arguments.",
            "proof_or_derivation": "Each counterexample is a well-formed coefficient map unless the parent grammar excludes its argument slot. Ward identities, diffeomorphism covariance and common calibration do not erase a legal source coefficient constructor.",
            "required_premises": "none; this is the failure branch",
            "current_status": "COUNTEREXAMPLES_RETAINED",
            "effect": "blocks live no-Hom/source-density claim",
            "source_path": str(source_paths["source_prefactor_classes_2612"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PSD3563_4_fallback_promotion",
            "name": "official nonclaim source-weight fallback",
            "statement": "Because parent sort construction and constructor exhaustion are not signed, the 3562 source-weight rows become the official nonclaim density-owner fallback until the parent sort proof is actually derived.",
            "proof_or_derivation": "3562 already decomposes the channels; 1896 supplies a finite Delta_w basis and no-cancellation policy. Promoting this fallback prevents repeated restatement of the same missing no-Hom theorem.",
            "required_premises": "failed live sort proof and existing finite source-weight basis",
            "current_status": "OFFICIAL_NONCLAIM_FALLBACK_SELECTED",
            "effect": "future local-GR density work should use bound rows unless a new parent constructor proof appears",
            "source_path": str(source_paths["deltaw_basis_1896"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PSD3563_5_local_GR_effect",
            "name": "effect on local GR/Newton route",
            "statement": "A signed parent sort proof would narrow source universality but still would not by itself close local GR; EH origin, common coupling owner, source-current closure, PPN equations and residual silence remain separate gates.",
            "proof_or_derivation": "Sort disjointness removes relative source knobs only. It does not derive the gravitational field equations or the calibrated Newton/PPN readout.",
            "required_premises": "separate local-GR gates after density closure",
            "current_status": "NARROWS_NOT_CLOSES",
            "effect": "keeps expectations honest while preserving the real gain",
            "source_path": str(source_paths["sort_impact_2688"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def clause_audit(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("PSC3563_0_parent_sorts", "derive disjoint parent sorts from MTS primitives", "MISSING_PRIMITIVE_SORT_CONSTRUCTION", "sorts cannot be asserted as discipline only", "sort_requirements_2686"),
        ("PSC3563_1_constructor_exhaustion", "all source/action constructors factor through allowed arguments before readout", "MISSING_CONSTRUCTOR_EXHAUSTION", "otherwise source-only constructor can be added", "sort_requirements_2686"),
        ("PSC3563_2_active_source_domain", "ActiveSourcePrefactor domain only UniversalCalibration + total Hilbert source + retained residuals", "CONSTRUCTOR_DOMAIN_NOT_DERIVED", "source labels could still enter", "sort_constructor_2688"),
        ("PSC3563_3_source_label_forgetting", "source functor forgets species labels before choosing gravitational/source coupling", "SOURCE_LABEL_FORGETTING_NOT_DERIVED", "hinge for delta_w_species", "sort_constructor_2688"),
        ("PSC3563_4_no_marker_extension", "no hidden/material/readout marker extends active-source coefficient domain", "NO_MARKER_EXHAUSTION_UNSIGNED", "hinge for hidden_marker_source and Delta_mask", "sort_constructor_2688"),
        ("PSC3563_5_action_scale_stability", "one action-scale/measure owner and readout/radiative stability preserve no-Hom", "ACTION_SCALE_READOUT_STABILITY_UNSIGNED", "prevents source weights returning through effective/readout maps", "nohom_constructor_2651"),
        ("PSC3563_6_common_calibration_split", "common scalar mode separated from relative source weights", "COMMON_CALIBRATION_ALLOWED_NONPREDICTIVE", "keeps GR-style G calibration fair", "nohom_theorem_3562"),
        ("PSC3563_7_fallback_basis", "finite Delta_w/source-weight fallback basis exists", "BASIS_SCHEMA_NONCLAIM_AVAILABLE", "official fallback can be used immediately", "deltaw_basis_1896"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "required_clause": required_clause,
            "status": status,
            "effect": effect,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, required_clause, status, effect, source_key in rows
    ]


def fallback_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("FB3563_0_delta_w_species", "relative_species_weight", "delta_w_species", "relative species/action source prefactor after common-mode subtraction", "OFFICIAL_NONCLAIM_FALLBACK_ROW", "dimensionless", "WEP;composition;R10;source_normalization", "P8_noHom_species_or_delta_w_bound.csv", "source_weight_bounds_3562"),
        ("FB3563_1_kappa_A_source", "active_source_selector", "kappa_A_source", "post-variation kappa_A T_A selector", "OFFICIAL_NONCLAIM_FALLBACK_ROW", "dimensionless", "WEP;R10;PPN;orbital", "P8_noHom_kappa_source_or_bound.csv", "source_weight_bounds_3562"),
        ("FB3563_2_hidden_marker_source", "hidden_marker_source", "hidden_marker_source", "hidden/domain/material marker source coefficient", "OFFICIAL_NONCLAIM_FALLBACK_ROW", "dimensionless", "preferred_frame;PPN;source_composition", "P8_noHom_hidden_marker_or_bound.csv", "source_weight_bounds_3562"),
        ("FB3563_3_hidden_frame", "hidden_source_frame", "A_A(X);disformal_A(X)", "hidden conformal/disformal source frame", "OFFICIAL_NONCLAIM_FALLBACK_ROW", "dimensionless", "PPN;clocks;R10;source_normalization", "P8_hidden_source_frame_bound.csv", "source_weight_bounds_3562"),
        ("FB3563_4_readout_worldtube_mask", "readout_mask", "Delta_mask", "post-fit source-worldtube active source mask", "OFFICIAL_NONCLAIM_FALLBACK_ROW", "dimensionless", "anti-tautology;all local arenas", "P8_readout_worldtube_mask_bound.csv", "source_weight_bounds_3562"),
        ("FB3563_5_common_mode", "common_calibration", "w_*;D_t ln w_*", "universal common source/action prefactor separated into calibration/drift row", "COMMON_MODE_NOT_RELATIVE_SOURCE_RESIDUAL", "yr^-1_or_dimensionless", "Gdot;orbital_GM;clock", "P8_common_source_scale_calibration_bound.csv", "source_weight_bounds_3562"),
        ("FB3563_6_nonHilbert_bypass", "nonHilbert_current", "nonHilbert_source_bypass", "active source not generated by Hilbert variation", "OUTSIDE_SORT_NOHOM_OFFICIAL_FALLBACK", "flux_or_dimensionless", "PPN;source_normalization;boundary_flux", "P8_nonHilbert_bypass_after_noHom_bound.csv", "source_weight_bounds_3562"),
        ("FB3563_7_total_envelope", "source_weight_total", "R_source_weight", "no-cancellation source-weight envelope feeding E_rho_qbasic", "OFFICIAL_NONCLAIM_TOTAL_ENVELOPE", "dimensionless_or_declared", "WEP;R10;PPN;orbital;Gdot", "P8_source_weight_total_bound_vector.csv", "source_weight_bounds_3562"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "fallback_id": fallback_id,
            "channel": channel,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "units": units,
            "observable_links": observable_links,
            "required_artifact": required_artifact,
            "source_path": str(source_paths[source_key]),
            "official_density_fallback": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for fallback_id, channel, symbol, definition, status, units, observable_links, required_artifact, source_key in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3563_0",
            "decision": "Parent sort disjointness proof remains conditional, not live.",
            "meaning": "The typed proof is correct if constructor exhaustion is parent-derived, but current MTS has not derived the constructor from primitives.",
            "claim_effect": "no local source-density claim",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3563_1",
            "decision": "Official nonclaim density fallback selected.",
            "meaning": "Future local-GR source-density work should stop restating no-Hom and use the source-weight fallback rows unless a new parent constructor proof appears.",
            "claim_effect": "source-weight rows become canonical nonclaim fallback",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3563_2",
            "decision": "Common calibration remains allowed.",
            "meaning": "A universal common action/source scale is treated like GR's calibrated G, but relative species/hidden/readout weights remain forbidden-or-bounded.",
            "claim_effect": "fair comparison with GR-style calibration",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3563_3",
            "decision": "Next target should leave source weights and attack non-Hilbert bypass or common coupling owner.",
            "meaning": "Because the no-Hom proof is now officially fallbacked, the best next derivation target is a different live gate, not another no-Hom restatement.",
            "claim_effect": "sets up 3564",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3563_0",
            "status": "PARENT_SORT_DISJOINTNESS_CONDITIONAL_OFFICIAL_FALLBACK_SELECTED",
            "summary": "The parent sort/no-Hom constructor proof is exact conditionally but not parent-signed. The finite source-weight vector is now the official nonclaim density fallback until a genuine parent sort constructor is derived.",
            "strongest_result": "conditional constructor theorem plus official fallback selection",
            "still_missing": "primitive parent sort construction, constructor exhaustion, source-label forgetting, no-marker extension proof, action-scale/readout stability",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3563_0",
            "target_doc": "3564-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3564_nonHilbert_source_bypass_improvement_zero_or_bound.py",
            "objective": "try to prove retained non-Hilbert source currents are exact improvements with zero exterior flux; if not, promote nonHilbert_source_bypass and boundary_flux rows as the next official density/source-current fallback",
            "success_gate": "non-Hilbert bypass theorem signed, or non-Hilbert current/flux residual rows become source-ready nonclaim bound rows",
            "reason": "3563 makes source-only weights an official fallback; the next density obstruction is non-Hilbert current bypass",
            "valid_for_claim": False,
        }
    ]


def validation(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fallback: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [str(path) for path in source_paths.values() if not path.exists()]
    parse_failures: list[str] = []
    for path in outputs.values():
        if path.suffix.lower() == ".csv":
            try:
                read_csv(path)
            except Exception as exc:
                parse_failures.append(f"{path}: {exc}")
    theorem_ids = {str(row["theorem_id"]) for row in theorem}
    clause_ids = {str(row["clause_id"]) for row in clauses}
    fallback_ids = {str(row["fallback_id"]) for row in fallback}
    unsafe_claims = [
        str(row["fallback_id"])
        for row in fallback
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("score_ready", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    formalization_touched = any(path == FORMALIZATION or FORMALIZATION in path.parents for path in outputs.values())
    rows = [
        ("VAL3563_0_sources_exist", not missing_sources, f"{len(source_paths)-len(missing_sources)}/{len(source_paths)} cited source paths exist" if not missing_sources else "; ".join(missing_sources)),
        ("VAL3563_1_generated_csvs_parse", not parse_failures, f"{sum(1 for path in outputs.values() if path.suffix.lower()=='.csv')} generated CSV files parse" if not parse_failures else "; ".join(parse_failures)),
        ("VAL3563_2_constructor_theorem_present", {"PSD3563_1_conditional_disjointness_proof","PSD3563_3_counterexample_obstruction","PSD3563_4_fallback_promotion"}.issubset(theorem_ids), "conditional proof, counterexample and fallback theorem rows present"),
        ("VAL3563_3_required_clauses_present", {"PSC3563_0_parent_sorts","PSC3563_1_constructor_exhaustion","PSC3563_3_source_label_forgetting","PSC3563_7_fallback_basis"}.issubset(clause_ids), "parent sort, exhaustion, source forgetting and fallback basis clauses present"),
        ("VAL3563_4_fallback_rows_present", {"FB3563_0_delta_w_species","FB3563_1_kappa_A_source","FB3563_2_hidden_marker_source","FB3563_4_readout_worldtube_mask","FB3563_7_total_envelope"}.issubset(fallback_ids), "official fallback rows present"),
        ("VAL3563_5_fallback_rows_nonclaim", not unsafe_claims, "all fallback rows remain nonclaim" if not unsafe_claims else "; ".join(unsafe_claims)),
        ("VAL3563_6_official_fallback_marked", all(str(row.get("official_density_fallback", "")).lower() == "true" for row in fallback), "every fallback row marked official_density_fallback"),
        ("VAL3563_7_formalization_workbench_untouched", not formalization_touched, "3563 generated outputs only inside post-checkpoint-work"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
        }
        for validation_id, passes, detail in rows
    ]


def write_doc(
    output_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fallback: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# 3563 - Parent sort disjointness active-source-prefactor proof or bound",
        "",
        "## Verdict",
        "3563 takes the leap and rejects the live proof for now: the parent sort/no-Hom constructor theorem is exact conditionally, but current MTS does not parent-derive the constructor from primitives. Therefore the source-weight vector is now the official nonclaim density fallback.",
        "",
        "This is progress, not retreat. We stop spending cycles re-saying `no-Hom missing`; future density/local-GR work must either bring a new parent sort constructor proof or use the official fallback rows.",
        "",
        "## Constructor theorem",
        "If `ActiveSourcePrefactor` is not a primitive parent sort, and the active source coefficient constructor has domain only `UniversalCalibration + total Hilbert source + explicit residual slots`, then species labels, hidden markers, readout selectors and worldtube selectors have no non-common incoming `Hom` into active source weights.",
        "",
        "The proof fails live because constructor exhaustion, source-label forgetting, no-marker exhaustion and readout/action-scale stability are not parent-signed.",
        "",
        "## What moved",
        "- The conditional proof is preserved as an exact theorem target.",
        "- Counterexamples remain explicit instead of hand-waved.",
        "- The finite source-weight vector is promoted to official nonclaim fallback.",
        "- Next work should move to a different gate: non-Hilbert source bypass or common coupling owner.",
        "",
        "## Generated outputs",
    ]
    for name, path in output_paths.items():
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(["", "## Constructor theorem rows"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(["", "## Clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}`: {row['required_clause']} -> {row['status']}")
    lines.extend(["", "## Official fallback rows"])
    for row in fallback:
        lines.append(f"- `{row['fallback_id']}` `{row['symbol']}`: {row['status']}")
    lines.extend(["", "## Decision ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} {row['meaning']}")
    lines.extend(["", "## Next target", f"- `{next_rows[0]['target_doc']}`", f"- Objective: {next_rows[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    source_rows = source_register(source_paths)
    theorem = constructor_theorem(source_paths)
    clauses = clause_audit(source_paths)
    fallback = fallback_rows(source_paths)
    decisions = decision_rows()
    statuses = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3563_SOURCE_REGISTER.csv",
        "constructor_theorem": RESIDUALS / "P8_Y5_R2FR_3563_PARENT_SORT_CONSTRUCTOR_THEOREM.csv",
        "clause_audit": RESIDUALS / "P8_Y5_R2FR_3563_SORT_CLAUSE_AUDIT.csv",
        "official_fallback": RESIDUALS / "P8_Y5_R2FR_3563_OFFICIAL_DENSITY_FALLBACK_ROWS.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3563_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3563_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3563_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_parent_sort_disjointness_official_fallback_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3563_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["constructor_theorem"], theorem)
    write_csv(outputs["clause_audit"], clauses)
    write_csv(outputs["official_fallback"], fallback)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], statuses)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["canonical_status"], [{
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "canonical_status": statuses[0]["status"],
        "strongest_result": statuses[0]["strongest_result"],
        "still_missing": statuses[0]["still_missing"],
        "next_target": next_rows[0]["target_doc"],
        "claim_allowed": False,
        "valid_for_claim": False,
    }])
    validation_rows = validation(source_paths, {key: path for key, path in outputs.items() if key != "validation"}, theorem, clauses, fallback)
    write_csv(outputs["validation"], validation_rows)
    write_doc(outputs, theorem, clauses, fallback, decisions, next_rows)
    for path in [DOC, *outputs.values()]:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
