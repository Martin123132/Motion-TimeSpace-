from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_PiM_commutator_conditional_topological_zero_written_parent_unsigned_projector_stress_vector_template_nonclaim"
CLAIM_CEILING = "PiM_commutator_gate_only_no_flux_closure_no_radial_zero_no_cmu_zero_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "661-Y5-R10-topological-Hilbert-current-equality-or-projector-stress-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "660-Y5-R10-PiM-commutator-zero-or-projector-stress-vector.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "659_doc": ROOT / "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md",
    "659_validation": RESIDUALS / "P8_Y5_BRR545_659_VALIDATION.csv",
    "659_obstruction_audit": RESIDUALS / "P8_Y5_R10_659_OBSTRUCTION_AUDIT.csv",
    "659_radial_template": RESIDUALS / "P8_Y5_R10_659_RADIAL_PROFILE_TEMPLATE.csv",
    "454_pim_algebra": ROOT / "454-PiM-parent-symplectic-projector-algebra-attempt.md",
    "456_projector_variation": ROOT / "456-PiM-projector-variation-stress-ledger.md",
    "500_topological_pim": ROOT / "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
    "521_pim_owner": ROOT / "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
    "523_gauss_orbital": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "pim_algebra_contract": RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
    "pim_variation_contract": RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "source_measure_flux_map": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "local_bound_matrix": RESIDUALS / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv",
}


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
            "role": "input_or_prior_contract_for_660_PiM_commutator_gate",
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def implementation_fork_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fork_id": "FORK660_0_topological_fixed_charge",
            "implementation": "topological_fixed_charge_map",
            "mathematical_form": "Pi_M J = ell_M(J) omega_M_top with d omega_M_top=0, delta_g Pi_M=0, and Pi_M d=d Pi_M on the exterior current complex",
            "commutator_status": "conditional_zero_if_parent_signed",
            "projector_stress_status": "zero_if_metric_independent_and_domain_fixed",
            "current_parent_status": "conditional_clause_written_not_Hilbert_equal_not_parent_signed",
            "risk": "closed topological charge may be the wrong object unless Pi_M J_H equals the topological current",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fork_id": "FORK660_1_Hodge_DeWitt_projector",
            "implementation": "Hodge_DeWitt_metric_projector",
            "mathematical_form": "Pi_M depends on G_B, Hodge representative, source-space inner product, or Green operator",
            "commutator_status": "not_zero_without_metric_variation_and_domain_stress_theorem",
            "projector_stress_status": "retained_as_T_PiM_or_commutator_integral",
            "current_parent_status": "candidate_not_parent_derived",
            "risk": "dropping delta Pi_M or [d,Pi_M]J_H smuggles an external source into the parent action",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fork_id": "FORK660_2_readout_or_fitted_mask",
            "implementation": "post_readout_or_fitted_mass_mask",
            "mathematical_form": "Pi_M chosen after orbital/source readout to select desired mass component",
            "commutator_status": "invalid_for_derivation",
            "projector_stress_status": "branch_rejected_or_closure_only",
            "current_parent_status": "policy_forbidden",
            "risk": "post-fit projector makes Newton source normalization circular",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def commutator_zero_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "CZ660_0_fixed_exterior_domain",
            "needed_statement": "compact exterior topology and S2 class are parent-selected before readout",
            "mathematical_form": "Sigma_ext ~= S2 x I and [S2] fixed by parent/domain theorem",
            "current_status": "conditional_open",
            "parent_signed": "false",
            "commutator_effect": "prevents domain/readout motion from entering [d,Pi_M]",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CZ660_1_metric_independent_projector",
            "needed_statement": "Pi_M is metric-independent/topological in the compact local exterior",
            "mathematical_form": "delta_g Pi_M=0 and Pi_M uses no Hodge star, Green operator, or fitted boundary metric",
            "current_status": "conditional_topological_route_not_parent_signed",
            "parent_signed": "false",
            "commutator_effect": "kills Hodge/projector variation stress if true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CZ660_2_closed_generator",
            "needed_statement": "mass generator is closed and normalized",
            "mathematical_form": "d omega_M_top=0 and integral_S2 omega_M_top=1",
            "current_status": "formal_topological_shape_available",
            "parent_signed": "conditional_shape_only",
            "commutator_effect": "removes ell_M(J_H)d omega_M term",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CZ660_3_chain_map_property",
            "needed_statement": "Pi_M commutes with d on the allowed source-current complex",
            "mathematical_form": "[d,Pi_M]J_H=0 for all allowed local Hilbert mass currents J_H",
            "current_status": "not_parent_derived",
            "parent_signed": "false",
            "commutator_effect": "directly zeros the 659 commutator obstruction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CZ660_4_Hilbert_current_domain",
            "needed_statement": "J_H lies in the source-current domain on which Pi_M is defined",
            "mathematical_form": "J_H in V_J and dJ_H remains in domain(Pi_M)",
            "current_status": "conditional_from_source_contract_not_parent_closed",
            "parent_signed": "false",
            "commutator_effect": "prevents source-current domain mismatch from becoming projector stress",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CZ660_5_variation_ownership",
            "needed_statement": "any delta Pi_M or domain/homology variation is owned by parent Ward/Bianchi ledger",
            "mathematical_form": "delta(Pi_M J)=Pi_M delta J+(delta Pi_M)J and (delta Pi_M)J=0/topological or retained",
            "current_status": "not_parent_derived",
            "parent_signed": "false",
            "commutator_effect": "if false, projector stress vector must be retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "CZ660_6_Hilbert_topological_equality",
            "needed_statement": "closed topological current equals the observed Hilbert Pi_M mass current up to exact zero-boundary terms",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero with integral_boundary dB_zero=0",
            "current_status": "not_derived_key_blocker_from_500",
            "parent_signed": "false",
            "commutator_effect": "without equality, commutator zero can close the wrong current",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def projector_stress_vector_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "stress_id": "TPS660_0_commutator_integral",
            "symbol": "I_commutator",
            "definition": "integral_A [d,Pi_M]J_H",
            "units": "same_units_as_projected_source_current_integral",
            "normalization": "epsilon_comm = c_M I_commutator / M_eff_ref",
            "affected_rows": "R4;R10;R11",
            "observable_link": "radial M_eff hair; fifth-force/radial source-normalization; R11 source ledger",
            "required_input": "parent commutator-zero theorem or sourced I_commutator with units and assumptions",
            "current_status": "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "stress_id": "TPS660_1_metric_projector_stress",
            "symbol": "T_PiM_munu",
            "definition": "stress from metric/Hodge/DeWitt dependence of Pi_M",
            "units": "stress_energy_units_or_dimensionless_after_EH_normalization",
            "normalization": "relative_to_EH_local_source_scale_or_measured_GM",
            "affected_rows": "R3;R4;R7;R8;R10;R11",
            "observable_link": "gamma, beta, alpha3, xi, R10, R11",
            "required_input": "delta_g Pi_M stress map or metric-independent no-stress theorem",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "stress_id": "TPS660_2_domain_homology_drift",
            "symbol": "Delta_domain_PiM",
            "definition": "variation of S2 representative, domain selector, normal, or homology class used by Pi_M",
            "units": "dimensionless_or_declared_domain_variation_units",
            "normalization": "domain variation contribution to epsilon_comm or preferred-frame coefficients",
            "affected_rows": "R5;R6;R7;R8;R9;R10;R11",
            "observable_link": "alpha1, alpha2, alpha3, xi, Gdot, R10, R11",
            "required_input": "topological/domain parent selector theorem or coefficient vector",
            "current_status": "MISSING_DOMAIN_SELECTOR_THEOREM_OR_VECTOR",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "stress_id": "TPS660_3_boundary_Hodge_reference",
            "symbol": "Delta_GB_or_boundary_ref",
            "definition": "boundary Hodge/DeWitt metric or reference subtraction contribution to Pi_M",
            "units": "dimensionless_or_boundary_charge_units",
            "normalization": "relative_to_measured_GM_or_boundary_charge_scale",
            "affected_rows": "R3;R4;R7;R8;R9;R11",
            "observable_link": "beta, alpha3, xi, Gdot, R11",
            "required_input": "boundary metric parent origin plus no-reference-hair theorem or coefficient",
            "current_status": "MISSING_BOUNDARY_PROJECTOR_STRESS_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "stress_id": "TPS660_4_readout_mask_rejection",
            "symbol": "P_read_or_fit_mask",
            "definition": "post-readout or fitted mass projector choice",
            "units": "not_applicable",
            "normalization": "not_claimable",
            "affected_rows": "R0-R11",
            "observable_link": "branch validity policy",
            "required_input": "prove projector is absent from parent variation or reject/demote branch to closure",
            "current_status": "POLICY_REJECT_IF_USED_FOR_DERIVATION",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def local_row_map_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "map_id": "MAP660_R3_GAMMA",
            "affected_row": "R3",
            "observable": "gamma_minus_1",
            "source": "T_PiM_munu or non-EH/projector stress in weak-field spatial metric",
            "current_status": "symbolic_missing_projector_stress_map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "map_id": "MAP660_R4_BETA_RADIAL",
            "affected_row": "R4",
            "observable": "beta_minus_1 and radial source hair",
            "source": "epsilon_comm plus second-order projector/source residual",
            "current_status": "symbolic_missing_commutator_integral_and_beta_map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "map_id": "MAP660_R7_ALPHA3",
            "affected_row": "R7",
            "observable": "alpha3",
            "source": "projector/domain/boundary stress with preferred-frame or flux component",
            "current_status": "symbolic_missing_alpha3_projection",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "map_id": "MAP660_R8_XI",
            "affected_row": "R8",
            "observable": "xi",
            "source": "preferred-location/domain/homology variation of Pi_M",
            "current_status": "symbolic_missing_xi_projection",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "map_id": "MAP660_R10_RANGE",
            "affected_row": "R10",
            "observable": "delta_G_or_fifth_force_yukawa",
            "source": "range/radial dependence from commutator integral or projector stress",
            "current_status": "symbolic_missing_alpha_lambda_or_no_range_theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "map_id": "MAP660_R11_LEDGER",
            "affected_row": "R11",
            "observable": "non_EH_operator_coefficients",
            "source": "projector stress vector as retained non-EH/source-normalization family",
            "current_status": "retained_symbolic_projector_stress_vector",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows(
    fork_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    stress_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    unsigned_zero = [row for row in zero_rows if row["parent_signed"] == "false"]
    missing_stress = [row for row in stress_rows if row["current_status"].startswith("MISSING_")]
    return [
        {
            "gate_id": "G660_0_fork_written",
            "gate": "topological/Hodge/readout fork is explicit",
            "result": "pass_structure" if len(fork_rows) == 3 else "fail",
            "detail": f"fork_rows={len(fork_rows)}",
            "claim_effect": "no hidden projector implementation",
            "generated_utc": now,
        },
        {
            "gate_id": "G660_1_conditional_topological_zero",
            "gate": "conditional topological commutator-zero route exists",
            "result": "pass_conditional",
            "detail": "fixed topological Pi_M with d omega=0 and chain-map property would kill [d,Pi_M]J_H",
            "claim_effect": "conditional theorem only",
            "generated_utc": now,
        },
        {
            "gate_id": "G660_2_parent_signed_commutator_zero",
            "gate": "all commutator-zero clauses are parent-signed",
            "result": "blocked",
            "detail": f"unsigned_required_clauses={len(unsigned_zero)}",
            "claim_effect": "blocks closing 659 commutator obstruction",
            "generated_utc": now,
        },
        {
            "gate_id": "G660_3_projector_stress_vector",
            "gate": "projector stress vector has numeric/theorem inputs",
            "result": "blocked",
            "detail": f"missing_projector_stress_rows={len(missing_stress)}",
            "claim_effect": "blocks R3/R4/R7/R8/R10/R11 scoring",
            "generated_utc": now,
        },
        {
            "gate_id": "G660_4_readout_mask_guard",
            "gate": "post-readout projector masks cannot derive source normalization",
            "result": "pass_policy",
            "detail": "readout/fitted mask branch is rejected or closure-only",
            "claim_effect": "blocks circular Newton proof",
            "generated_utc": now,
        },
        {
            "gate_id": "G660_5_local_row_map",
            "gate": "local residual rows are mapped",
            "result": "pass_structure" if len(map_rows) == 6 else "fail",
            "detail": f"map_rows={len(map_rows)}",
            "claim_effect": "mapping only; no score-ready rows",
            "generated_utc": now,
        },
        {
            "gate_id": "G660_6_claim_guard",
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
            "decision_id": "D660_0_commutator_route",
            "status": "conditional_topological_zero_written",
            "meaning": "a fixed topological Pi_M would kill the commutator and avoid projector stress",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D660_1_parent_status",
            "status": "not_parent_signed",
            "meaning": "the parent action has not yet supplied fixed domain, metric independence, chain-map property, and Hilbert equality",
            "claim_status": "false",
            "next_action": "try topological-Hilbert current equality next",
            "generated_utc": now,
        },
        {
            "decision_id": "D660_2_projector_stress",
            "status": "retained_template_written",
            "meaning": "if the topological route fails, [d,Pi_M]J_H becomes I_commutator/T_PiM/projector-domain stress rows",
            "claim_status": "false",
            "next_action": "fill only with sourced coefficients or theorem-zero proof",
            "generated_utc": now,
        },
        {
            "decision_id": "D660_3_local_GR",
            "status": "blocked",
            "meaning": "local GR remains blocked because projector commutator silence is not parent-signed",
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
    prior_validation_659: list[dict[str, str]],
    obstruction_rows_659: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    stress_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = [row for row in prior_validation_659 if row.get("result") != "pass"]
    commutator_imported = any(row.get("obstruction_id") == "OBS659_0_projector_commutator" for row in obstruction_rows_659)
    claim_rows = []
    for group in (fork_rows, zero_rows, stress_rows, map_rows, gate_rows, decision):
        claim_rows.extend(
            [row for row in group if row.get("valid_for_claim") == "true" or row.get("claim_status") == "true"]
        )
    generic_fill_markers = []
    for group in (fork_rows, zero_rows, stress_rows, map_rows, gate_rows, decision):
        for row in group:
            for value in row.values():
                if isinstance(value, str) and "fill_" in value.lower():
                    generic_fill_markers.append(value)
    blocked_gates = [row for row in gate_rows if row["result"] == "blocked"]
    formalization_changed = formalization_changed_count()
    checks = [
        (
            "V660_0_source_paths_exist",
            not missing_sources,
            "all cited local source paths exist" if not missing_sources else f"missing={';'.join(missing_sources)}",
        ),
        (
            "V660_1_prior_659_validation_clean",
            not prior_failures,
            "659 validation remains clean" if not prior_failures else f"659_failures={len(prior_failures)}",
        ),
        (
            "V660_2_commutator_obstruction_imported",
            commutator_imported,
            "OBS659_0_projector_commutator loaded",
        ),
        (
            "V660_3_fork_coverage",
            {row["implementation"] for row in fork_rows}
            == {"topological_fixed_charge_map", "Hodge_DeWitt_metric_projector", "post_readout_or_fitted_mass_mask"},
            f"fork_rows={len(fork_rows)}",
        ),
        (
            "V660_4_zero_clause_coverage",
            len(zero_rows) == 7,
            f"zero_clause_rows={len(zero_rows)}",
        ),
        (
            "V660_5_commutator_zero_not_parent_signed",
            any(row["clause_id"] == "CZ660_3_chain_map_property" and row["parent_signed"] == "false" for row in zero_rows),
            "chain-map commutator zero remains unsigned",
        ),
        (
            "V660_6_projector_stress_template",
            len(stress_rows) == 5 and all(row["valid_for_claim"] == "false" for row in stress_rows),
            f"stress_rows={len(stress_rows)}",
        ),
        (
            "V660_7_local_row_map",
            {row["affected_row"] for row in map_rows} == {"R3", "R4", "R7", "R8", "R10", "R11"},
            f"mapped_rows={';'.join(sorted(row['affected_row'] for row in map_rows))}",
        ),
        (
            "V660_8_scoreability_blocked",
            len(blocked_gates) >= 2,
            f"blocked_gates={len(blocked_gates)}",
        ),
        (
            "V660_9_no_claim_rows",
            not claim_rows,
            f"claim_rows={len(claim_rows)}",
        ),
        (
            "V660_10_no_generic_fill_placeholders",
            not generic_fill_markers,
            f"fill_markers={len(generic_fill_markers)}",
        ),
        (
            "V660_11_next_target_selected",
            NEXT_TARGET.startswith("661-") and "topological-Hilbert" in NEXT_TARGET,
            NEXT_TARGET,
        ),
        (
            "V660_12_claim_ceiling_active",
            CLAIM_CEILING.startswith("PiM_commutator_gate_only"),
            CLAIM_CEILING,
        ),
        (
            "V660_13_formalization_workbench_untouched",
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
    fork_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    stress_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "fork_rows": len(fork_rows),
            "zero_clause_rows": len(zero_rows),
            "projector_stress_rows": len(stress_rows),
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
    fork_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    stress_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 660 Y5/R10: PiM Commutator Zero Or Projector Stress Vector

## Verdict

Status: `{STATUS}`.

The commutator can be killed cleanly only by a parent-owned topological/fixed `Pi_M` that commutes with exterior `d` on the Hilbert source-current domain. The current corpus has a conditional topological route, but it is not parent-signed and not yet proved equal to the observed Hilbert mass current. Therefore `[d,Pi_M]J_H` remains a retained obstruction or projector-stress vector.

## Source Register

{markdown_table(source_rows, ["source_id", "exists", "role"], limit=20)}

## Implementation Fork

{markdown_table(fork_rows, ["implementation", "commutator_status", "projector_stress_status", "current_parent_status", "valid_for_claim"])}

## Commutator-Zero Audit

{markdown_table(zero_rows, ["clause_id", "needed_statement", "mathematical_form", "current_status", "parent_signed", "valid_for_claim"])}

## Projector-Stress Vector

{markdown_table(stress_rows, ["stress_id", "symbol", "definition", "current_status", "affected_rows", "score_ready", "valid_for_claim"])}

## Local Row Map

{markdown_table(map_rows, ["affected_row", "observable", "source", "current_status", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "fork_rows", "zero_clause_rows", "projector_stress_rows", "blocked_scoreability_gates", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This narrows the route sharply. Hodge/DeWitt `Pi_M` is not dead, but it carries `delta Pi_M` and projector stress unless the parent action explicitly owns the variation. The clean route is topological:

`Pi_M J = ell_M(J) omega_M_top`, with `d omega_M_top=0`, `delta_g Pi_M=0`, and `[d,Pi_M]=0` on the allowed source-current complex.

But the topological route still has a hard equality bill: prove `Pi_M J_H = J_M_top + dB_zero`. Without that, we may have closed the wrong current.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    prior_validation_659 = read_csv(SOURCE_PATHS["659_validation"])
    obstruction_rows_659 = read_csv(SOURCE_PATHS["659_obstruction_audit"])

    fork_rows = implementation_fork_rows()
    zero_rows = commutator_zero_audit_rows()
    stress_rows = projector_stress_vector_rows()
    map_rows = local_row_map_rows()
    gate_rows = scoreability_gate_rows(fork_rows, zero_rows, stress_rows, map_rows)
    decision = decision_rows()
    validation = validation_rows(
        source_rows,
        prior_validation_659,
        obstruction_rows_659,
        fork_rows,
        zero_rows,
        stress_rows,
        map_rows,
        gate_rows,
        decision,
    )
    summary_rows = nonclaim_summary_rows(fork_rows, zero_rows, stress_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_660_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_660_IMPLEMENTATION_FORK.csv",
        fork_rows,
        [
            "fork_id",
            "implementation",
            "mathematical_form",
            "commutator_status",
            "projector_stress_status",
            "current_parent_status",
            "risk",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
        zero_rows,
        [
            "clause_id",
            "needed_statement",
            "mathematical_form",
            "current_status",
            "parent_signed",
            "commutator_effect",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv",
        stress_rows,
        [
            "stress_id",
            "symbol",
            "definition",
            "units",
            "normalization",
            "affected_rows",
            "observable_link",
            "required_input",
            "current_status",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_660_LOCAL_ROW_MAP.csv",
        map_rows,
        [
            "map_id",
            "affected_row",
            "observable",
            "source",
            "current_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_660_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_660_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_660_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "fork_rows",
            "zero_clause_rows",
            "projector_stress_rows",
            "blocked_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_660_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(
        source_rows,
        fork_rows,
        zero_rows,
        stress_rows,
        map_rows,
        gate_rows,
        decision,
        summary_rows,
        validation,
    )

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"fork_rows={len(fork_rows)}")
    print(f"zero_clause_rows={len(zero_rows)}")
    print(f"projector_stress_rows={len(stress_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
