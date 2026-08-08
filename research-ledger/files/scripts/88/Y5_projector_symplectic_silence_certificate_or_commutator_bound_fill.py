from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_projector_symplectic_silence_certificate_failed_current_claim_commutator_projector_bound_row_written"
CLAIM_CEILING = "projector_symplectic_silence_attempt_and_commutator_projector_bound_row_only_no_BRR545_source_measure_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "551-Y5-BRR545-residual-envelope-and-first-local-lock-fill-or-demotion.md"

DOC_PATH = Path("550-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_550_SOURCE_REGISTER.csv")
PROJECTOR_THEOREM_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_SILENCE_THEOREM_ATTEMPT.csv")
PROJECTOR_OBSTRUCTIONS_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_OBSTRUCTION_LEDGER.csv")
COMMUTATOR_BOUND_FILL_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv")
COMMUTATOR_EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_EVALUATOR.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_550_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_550_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_550_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
        "role": "previous BRR545 boundary certificate failure and boundary flux bound row",
    },
    {
        "source_file": "548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md",
        "role": "reference-lock failure and Delta_symp retained row",
    },
    {
        "source_file": "547-Y5-boundary-reference-residual-input-template-and-local-lock-map.md",
        "role": "BRR545 certificate queue, residual template, and local lock map",
    },
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "Pi_M owner fork and commutator gate",
    },
    {
        "source_file": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "role": "Hamiltonian Pi_M repair candidate and topological demotion warning",
    },
    {
        "source_file": "534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md",
        "role": "Pi_M topological equality certificate and commutator template",
    },
    {
        "source_file": "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "role": "source-current closure theorem attempt and epsilon-charge decomposition",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "closed Pi_M flux source identity residual decomposition",
    },
    {
        "source_file": "456-PiM-projector-variation-stress-ledger.md",
        "role": "projector variation stress ledger",
    },
    {
        "source_file": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "Pi_M flux-closure Ward/topological current attempt",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "conditional Pi_M algebra and variation warning",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "machine-readable Pi_M symplectic/projector algebra contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "role": "machine-readable flux-closure Ward/topological contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "machine-readable projector variation stress contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "role": "parent source identity residual decomposition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "role": "source-current closure theorem attempt rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RESIDUAL_DECOMPOSITION.csv",
        "role": "epsilon-charge residual decomposition including commutator residual",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv",
        "role": "commutator/projector-stress input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
        "role": "Pi_M radial bound input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_MAP.csv",
        "role": "BRR545 local PPN/source lock map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_549_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "scripts/Y5_projector_symplectic_silence_certificate_or_commutator_bound_fill.py",
        "role": "this checkpoint generator",
    },
]


PROJECTOR_THEOREM_ROWS = [
    {
        "step_id": "PST550_0_target_certificate",
        "claim": "BRC547_3 requires Pi_M to be covariantly silent and symplectically stress-free in the local exterior",
        "mathematical_form": "nabla Pi_M=0; delta(Pi_M J_H)=Pi_M delta J_H; [d,Pi_M]J_H=0",
        "current_result": "target_defined",
        "why_not_enough": "a target condition is not a parent theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PST550_1_topological_absolute_charge_route",
        "claim": "a parent-owned absolute/topological charge projector could make Pi_M metric-independent and commute with exterior differentiation",
        "mathematical_form": "Pi_M J=ell_M(J) omega_M_top; d omega_M_top=0; delta_g Pi_M=0",
        "current_result": "conditional_route_available",
        "why_not_enough": "the corpus has not parent-derived the fixed domain, charge functional, and Hilbert/source equality before readout",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PST550_2_current_PiM_parent_ownership",
        "claim": "current MTS owns Pi_M as parent charge data rather than a Hodge/readout/fitted projector",
        "mathematical_form": "Pi_M is selected in S_parent and tied to J_H in the same observed frame before orbital scoring",
        "current_result": "not_derived",
        "why_not_enough": "Pi_M owner rows remain conditional; Hamiltonian repair is a candidate, not a signed theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PST550_3_product_rule_commutator",
        "claim": "projected current closure can drop the product-rule commutator",
        "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H with [d,Pi_M]J_H=0",
        "current_result": "obstruction_retained",
        "why_not_enough": "fixed-topology algebra alone does not prove source-current closure or topological-Hilbert equality",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PST550_4_variation_stress",
        "claim": "projector variation carries no stress and can be omitted from the local exterior equations",
        "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H with (delta Pi_M)J_H=0 or boundary-constant only",
        "current_result": "obstruction_retained",
        "why_not_enough": "Hodge, DeWitt, domain, boundary-metric, and source-space splitting routes generically vary unless topological silence is parent-owned",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PST550_5_boundary_domain_homology",
        "claim": "the S2 representative, compact exterior, boundary normal, and homology class are fixed covariantly before readout",
        "mathematical_form": "delta Sigma_ext=0 or topological; delta n_mu and delta chi_D owned; no fitted domain selector",
        "current_result": "not_derived",
        "why_not_enough": "domain/homology variation remains a possible preferred-frame/location and source-normalization leakage",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PST550_6_source_charge_equality",
        "claim": "Pi_M projects the same Hilbert/source current that calibrates measured mass",
        "mathematical_form": "Pi_M J_H = J_M_top or Pi_M^H J_H plus exact zero-boundary term",
        "current_result": "not_derived",
        "why_not_enough": "a closed current can still be the wrong conserved object; source-measure glue remains open",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PST550_7_certificate_verdict",
        "claim": "BRC547_3 can be signed for current MTS",
        "mathematical_form": "BRC547_3.valid_for_claim=true",
        "current_result": "fail_current_claim",
        "why_not_enough": "conditional topological/projector silence is not parent-owned; fallback commutator/projector bound row is required",
        "valid_for_claim": "false",
    },
]


PROJECTOR_OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "PSO550_0_topological_route_not_owned",
        "obstruction": "absolute/topological Pi_M would be enough, but current MTS has not derived it from the parent action before readout",
        "activated_residual": "epsilon_projector_symplectic_abs;epsilon_commutator",
        "repair": "derive parent-fixed charge functional/domain and same-frame Hilbert equality, or adopt Hamiltonian Pi_M with full integrability/source-measure proof",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "PSO550_1_commutator_product_rule",
        "obstruction": "d(Pi_M J_H) contains [d,Pi_M]J_H unless Pi_M is fixed/covariantly constant on the allowed current domain",
        "activated_residual": "epsilon_commutator;radial_source_hair;Gdot",
        "repair": "theorem-zero for the commutator or source-backed integral bound over the compact shell",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "PSO550_2_variation_product_rule",
        "obstruction": "delta(Pi_M J_H) contains (delta Pi_M)J_H and can induce projector stress",
        "activated_residual": "projector_stress;R3_gamma;R4_beta;R7_alpha3;R8_xi;R11",
        "repair": "prove delta Pi_M=0 topologically or retain and coefficient-map T_PiM_munu",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "PSO550_3_hodge_dewitt_metric_dependence",
        "obstruction": "Hodge/DeWitt/orthogonal projectors depend on boundary metric, Green operators, normals, and source-space splitting",
        "activated_residual": "projector_stress;preferred_frame;preferred_location",
        "repair": "avoid Hodge metric dependence through absolute charge data or vary every induced term",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "PSO550_4_domain_homology_variation",
        "obstruction": "S2 representative, exterior shell, homology class, and boundary normal are not parent-locked",
        "activated_residual": "alpha3;xi;beta;source_normalization;radial_profile",
        "repair": "parent topology/domain selector or explicit derivative/profile bounds",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "PSO550_5_wrong_conserved_object",
        "obstruction": "a closed topological current may not equal the measured Hilbert/source mass current",
        "activated_residual": "epsilon_PiM_equality;epsilon_charge_abs_envelope;R1_WEP_source_charge",
        "repair": "source-measure glue tying Hamiltonian/topological charge to the same observed Hilbert current",
        "valid_for_claim": "false",
    },
]


COMMUTATOR_BOUND_FILL_ROWS = [
    {
        "fill_id": "FB550_0_commutator_projector_bound",
        "residual_component": "epsilon_projector_symplectic_abs",
        "formula": "abs(int_A [d,Pi_M]J_H)/M_H_ref + abs(int_S (delta Pi_M)J_H)/M_H_ref",
        "commutator_over_MH": "MISSING_COMMUTATOR_NUMERIC_OR_THEOREM_ZERO",
        "projector_variation_over_MH": "MISSING_PROJECTOR_VARIATION_NUMERIC_OR_THEOREM_ZERO",
        "c_projector_to_gamma": "MISSING_GAMMA_COEFFICIENT",
        "c_projector_to_beta": "MISSING_BETA_COEFFICIENT",
        "c_projector_to_alpha3": "MISSING_ALPHA3_COEFFICIENT",
        "c_projector_to_xi": "MISSING_XI_COEFFICIENT",
        "partial_t_projector_residual": "MISSING_TIME_PROFILE",
        "partial_r_projector_residual": "MISSING_RADIAL_PROFILE",
        "mapped_lock_rows": "R1_WEP_source_charge;R3_gamma;R4_beta;R7_alpha3;R8_xi;R9_Gdot;R10_fifth_force;R11_EH_operator_ledger",
        "bound_rule": "commutator and projector-variation terms each pass individually or theorem-zero; no cancellation credit",
        "source_file": "MISSING_SOURCE_FILE",
        "derivation_status": "unfilled_after_projector_symplectic_silence_certificate_failure",
        "valid_for_claim": "false",
    }
]


DECISION_ROWS = [
    {
        "decision_id": "D550_0_projector_silence_certificate_failed",
        "status": "BRC547_3_not_signed",
        "meaning": "current MTS has conditional topological/projector routes but no parent-owned Pi_M silence theorem",
        "claim_status": "epsilon_projector_symplectic_abs_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D550_1_commutator_projector_bound_row_written",
        "status": "epsilon_projector_symplectic_abs_bound_row_written_unfilled",
        "meaning": "fallback row now states exactly what a theorem or numeric/profile fill must supply",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D550_2_BRR545_status",
        "status": "reference_boundary_projector_rows_retained",
        "meaning": "BRR545 now has explicit retained rows for reference lock, boundary flux, and projector symplectic silence",
        "claim_status": "not_BRR545_pass",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D550_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BRC547_3_PROJECTOR_SYMPLECTIC_SILENCE",
        "previous_status": "missing_certificate",
        "new_status": "attempted_failed_current_claim_commutator_projector_bound_row_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BRR545_DELTA_SYMPLECTIC_REFERENCE",
        "previous_status": "epsilon_Delta_symp_abs_retained_with_first_bound_fill_row",
        "new_status": "still_retained_projector_silence_failed_current_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BRR545_BOUNDARY_FLUX",
        "previous_status": "epsilon_B_flux_abs_retained_with_first_bound_fill_row",
        "new_status": "still_retained_projector_silence_failed_current_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BRR545_PROJECTOR_SYMPLECTIC",
        "previous_status": "input_template_unfilled",
        "new_status": "epsilon_projector_symplectic_abs_retained_with_first_bound_fill_row",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_boundary_cohomology_nohair_failed_current_claim",
        "new_status": "still_blocked_projector_symplectic_silence_failed_current_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_no_boundary_zero_or_bound_value",
        "new_status": "still_blocked_no_reference_boundary_projector_zero_or_bound_values",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def commutator_projector_evaluator_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in COMMUTATOR_BOUND_FILL_ROWS:
        rows.append(
            {
                "fill_id": row["fill_id"],
                "residual_component": row["residual_component"],
                "numeric_status": "not_computed_missing_commutator_projector_variation_coefficients_and_profiles",
                "mapped_lock_rows": row["mapped_lock_rows"],
                "pass_status": "not_claimable",
                "valid_for_claim": "false",
                "notes": "projector symplectic silence certificate failed for current claim; fill only with theorem-zero source or source-backed commutator/projector-stress data",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]], evaluator_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_549_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    prior_certificates = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_THEOREM_CERTIFICATE_TEMPLATE.csv"))
    prior_lock_map = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_LOCAL_LOCK_MAP.csv"))
    algebra_contract = read_csv(Path("source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"))
    flux_contract = read_csv(Path("source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv"))
    variation_contract = read_csv(Path("source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv"))
    source_identity = read_csv(Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv"))
    source_current = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv"))
    epsilon_charge = read_csv(Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_RESIDUAL_DECOMPOSITION.csv"))
    commutator_template = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv"))
    radial_template = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"))
    claim_theorem_rows = [row for row in PROJECTOR_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_obstruction_rows = [row for row in PROJECTOR_OBSTRUCTION_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in COMMUTATOR_BOUND_FILL_ROWS if row["valid_for_claim"] == "true"]
    claim_eval_rows = [row for row in evaluator_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V550_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V550_1_prior_549_clean",
            "result": "pass" if len(prior_validation) == 8 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V550_2_prior_templates_loaded",
            "result": "pass" if len(prior_certificates) == 5 and len(prior_lock_map) == 10 else "fail",
            "detail": f"certificate_rows={len(prior_certificates)};lock_rows={len(prior_lock_map)}",
        },
        {
            "check_id": "V550_3_PiM_evidence_loaded",
            "result": "pass"
            if len(algebra_contract) == 9
            and len(flux_contract) == 9
            and len(variation_contract) == 9
            and len(source_identity) >= 8
            and len(source_current) == 8
            and len(epsilon_charge) == 7
            else "fail",
            "detail": f"algebra={len(algebra_contract)};flux={len(flux_contract)};variation={len(variation_contract)};source_identity={len(source_identity)};source_current={len(source_current)};epsilon_charge={len(epsilon_charge)}",
        },
        {
            "check_id": "V550_4_bound_templates_loaded",
            "result": "pass" if len(commutator_template) == 5 and len(radial_template) == 5 else "fail",
            "detail": f"commutator_template={len(commutator_template)};radial_template={len(radial_template)}",
        },
        {
            "check_id": "V550_5_theorem_attempt_complete",
            "result": "pass" if len(PROJECTOR_THEOREM_ROWS) == 8 and len(PROJECTOR_OBSTRUCTION_ROWS) == 6 else "fail",
            "detail": f"theorem_rows={len(PROJECTOR_THEOREM_ROWS)};obstruction_rows={len(PROJECTOR_OBSTRUCTION_ROWS)}",
        },
        {
            "check_id": "V550_6_commutator_bound_row_written",
            "result": "pass" if len(COMMUTATOR_BOUND_FILL_ROWS) == 1 and len(evaluator_rows) == 1 else "fail",
            "detail": f"fill_rows={len(COMMUTATOR_BOUND_FILL_ROWS)};evaluator_rows={len(evaluator_rows)}",
        },
        {
            "check_id": "V550_7_no_claim_rows",
            "result": "pass" if not claim_theorem_rows and not claim_obstruction_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": f"claim_theorem={len(claim_theorem_rows)};claim_obstruction={len(claim_obstruction_rows)};claim_fill={len(claim_fill_rows)};claim_eval={len(claim_eval_rows)}",
        },
        {
            "check_id": "V550_8_no_overclaim",
            "result": "pass" if not claim_theorem_rows and not claim_obstruction_rows and not claim_fill_rows and not claim_eval_rows else "fail",
            "detail": "projector_silence_certificate_signed=false; epsilon_projector_symplectic_abs_filled=false; BRR545_filled=false; source_measure=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    evaluator_rows: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 550 - Y5 Projector Symplectic Silence Certificate or Commutator Bound Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The projector symplectic silence certificate does not close for current MTS.

This is not a collapse of the route. It is the referee saying the same thing in sharper language:

```text
Pi_M can be made quiet only if the parent action owns it as fixed charge data
or if every commutator / variation term is retained and bounded.
```

So `epsilon_projector_symplectic_abs` remains active, and the first commutator/projector fallback row is now explicit.

## 2. Projector Symplectic Silence Theorem Attempt

{markdown_table(PROJECTOR_THEOREM_ROWS)}

## 3. Obstruction Ledger

{markdown_table(PROJECTOR_OBSTRUCTION_ROWS)}

## 4. Commutator and Projector Bound Fill Row

{markdown_table(COMMUTATOR_BOUND_FILL_ROWS)}

## 5. Commutator and Projector Evaluator

{markdown_table(evaluator_rows)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has attempted the projector symplectic silence certificate.
MTS has identified why current Pi_M cannot be treated as covariantly constant / stress-free.
MTS has written the first fallback bound row for epsilon_projector_symplectic_abs.
```

Forbidden:

```text
MTS has signed the projector symplectic silence certificate.
MTS has filled epsilon_projector_symplectic_abs.
MTS has completed BRR545.
MTS has derived source-measure, measured GM, Newton, PPN, or local GR.
```

## 11. Practical Read

This is a useful narrowing. The local branch is no longer allowed to smuggle in a silent `Pi_M`. Either `Pi_M` becomes parent-owned Hamiltonian/topological charge data, or it produces a measurable commutator/projector-stress residual that must pass the local locks.

## 12. Next Target

`{NEXT_TARGET}`

Next: assemble the reference, boundary, and projector residual rows into a first BRR545 envelope, then either fill the first local lock numerically/theoremically or demote this local-GR route to explicit closure-only.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    evaluator_rows = commutator_projector_evaluator_rows()
    validations = validation_rows(sources, evaluator_rows)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (PROJECTOR_THEOREM_PATH, PROJECTOR_THEOREM_ROWS),
        (PROJECTOR_OBSTRUCTIONS_PATH, PROJECTOR_OBSTRUCTION_ROWS),
        (COMMUTATOR_BOUND_FILL_PATH, COMMUTATOR_BOUND_FILL_ROWS),
        (COMMUTATOR_EVALUATOR_PATH, evaluator_rows),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, evaluator_rows, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "projector_theorem": str(ROOT / PROJECTOR_THEOREM_PATH),
        "projector_obstructions": str(ROOT / PROJECTOR_OBSTRUCTIONS_PATH),
        "commutator_projector_fill": str(ROOT / COMMUTATOR_BOUND_FILL_PATH),
        "commutator_projector_evaluator": str(ROOT / COMMUTATOR_EVALUATOR_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "projector_theorem_rows": len(PROJECTOR_THEOREM_ROWS),
        "obstruction_rows": len(PROJECTOR_OBSTRUCTION_ROWS),
        "commutator_projector_fill_rows": len(COMMUTATOR_BOUND_FILL_ROWS),
        "projector_symplectic_silence_certificate_signed": False,
        "epsilon_projector_symplectic_abs_filled": False,
        "BRR545_values_filled": False,
        "source_measure_theorem_derived": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nprojector_symplectic_silence_certificate_failed_commutator_projector_bound_row_written_no_BRR545_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
