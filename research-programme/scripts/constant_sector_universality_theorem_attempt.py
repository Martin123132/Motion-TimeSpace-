from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "constant-sector-universality-theorem-attempt"
CHECKPOINT_DOC = "448-constant-sector-universality-theorem-attempt.md"
STATUS = "constant_sector_universality_theorem_attempt_written_conditional_superselection_route_not_parent_derived_P8_R1_R2_retained_no_local_GR_pass"
CLAIM_CEILING = "constant_sector_universality_conditional_only_no_source_charge_clock_WEP_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "449-source-current-Ward-universality-theorem-attempt.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv")


CONTRACT_COLUMNS = [
    "contract_id",
    "required_identity",
    "mathematical_form",
    "closes_component",
    "affected_rows",
    "current_status",
    "evidence_needed",
    "fallback_if_missing",
]


SOURCE_DOCS = [
    {
        "path": "447-no-species-source-charge-one-coframe-theorem-attempt.md",
        "role": "one-coframe theorem attempt and constant-sector next target",
    },
    {
        "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
        "role": "S2 constant-sector universality requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "A6 selector-blind source-action parent block",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 species/source charge and source-normalization residual template",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "empirical WEP/source locks for retained fallback rows",
    },
    {
        "path": "runs/20260601-191500-universal-matter-coupling-theorem-attempt/results/matter_action_contract.csv",
        "role": "single observed geometry and matter constants contract",
    },
    {
        "path": "runs/20260601-191500-universal-matter-coupling-theorem-attempt/results/forbidden_vertices.csv",
        "role": "forbidden constant/source vertices",
    },
    {
        "path": "runs/20260601-000057-universal-coupling-parent-contract-or-local-bound-data-runner/results/universal_coupling_contract.csv",
        "role": "universal coupling and constants-not-memory-fields contract",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/functor_requirements.csv",
        "role": "constant-sector independence as functor requirement",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/counterexample_functors.csv",
        "role": "species internal constants and quotient-invariant counterexamples",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/variation_identity_requirements.csv",
        "role": "species-blindness and source-owner variation requirements",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/parent_action_blocks.csv",
        "role": "parent source-action blocks and open source-blindness status",
    },
    {
        "path": "runs/20260602-151500-no-species-source-charge-one-coframe-theorem-attempt/results/source_charge_counterexamples.csv",
        "role": "species-internal constant counterexample to one-coframe proof",
    },
    {
        "path": "runs/20260602-151500-no-species-source-charge-one-coframe-theorem-attempt/results/no_species_source_charge_contract.csv",
        "role": "machine-readable no-species/source-charge contract",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_superselection_theorem",
        "statement": "If matter constants are superselection/representation data independent of MTS selectors, quotient invariants, material markers, and source labels, and the active source is the common stress-energy/coframe variation of the same matter action, then the constant sector contributes no extra species/source charge.",
        "mathematical_form": "partial_Z theta_A=partial_IQ theta_A=partial_m theta_A=0 and delta S_source/delta e_obs = kappa_univ sum_A delta S_A/delta e_obs => partial_A ln(mu_obs/M_inertial)=0",
        "status": "valid_conditional_route",
    },
    {
        "part": "not_equal_constants_claim",
        "statement": "Universality does not mean all particle masses, charges, or clock constants are numerically equal; it means the rule by which they enter the observed matter action and active gravitational source is common and MTS-marker independent.",
        "mathematical_form": "theta_A may label species representation; forbidden is theta_A(Z,I_Q,m) or kappa_A source weighting",
        "status": "definition_guardrail",
    },
    {
        "part": "current_corpus_status",
        "statement": "The current corpus has the required contract rows, but it has not derived the parent symmetry/no-extension/Ward identity that forces constant-sector independence.",
        "mathematical_form": "UC2/S2/C5 remain required contracts, not theorems",
        "status": "not_parent_derived",
    },
]


PROOF_STEPS = [
    {
        "step": 1,
        "claim": "Define the constant sector as matter representation data rather than an MTS field.",
        "mathematical_step": "theta_A in Rep_A, not theta_A=theta_A[Z,I_Q,m]",
        "status": "definition_needed",
        "gap": "the corpus uses this as a contract but has not derived it from the parent action",
    },
    {
        "step": 2,
        "claim": "Require the MTS quotient/group action to be trivial on the constant sector.",
        "mathematical_step": "L_xi theta_A=0 for selector, quotient, memory, class, and marker directions xi",
        "status": "sufficient_if_parent_symmetry",
        "gap": "quotient invariance alone allows theta_A(I_Q), so the trivial action must be added or derived",
    },
    {
        "step": 3,
        "claim": "Require matter to enter through one observed geometry plus constants only.",
        "mathematical_step": "S_m=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
        "status": "conditional_from_universal_matter_contract",
        "gap": "direct vertices m_A(Z), alpha_EM(Z), q_A X_mu J_A^mu remain listed forbidden hazards",
    },
    {
        "step": 4,
        "claim": "Require active source ownership by the same matter stress/coframe variation.",
        "mathematical_step": "J_grav := delta S_m/delta e_obs, not sum_A kappa_A J_A",
        "status": "not_parent_derived",
        "gap": "source-owner contract A6 is present, but source-current Ward universality is not proved",
    },
    {
        "step": 5,
        "claim": "Then constants can change inertial composition without generating an extra gravitational source charge.",
        "mathematical_step": "delta mu_obs = kappa_univ delta M_inertial and eta_source_AB=0 after measured-GM normalization",
        "status": "valid_conditional_math",
        "gap": "measured-GM normalization and absolute source calibration remain open P8 rows",
    },
    {
        "step": 6,
        "claim": "The theorem fails if constants or source weights are allowed to be functions of MTS invariants or material markers.",
        "mathematical_step": "theta_A(I_Q), theta_A(m), kappa_A, or q_XA != universal reopens partial_A mu_obs",
        "status": "counterexample_visible",
        "gap": "no parent theorem currently forbids all listed deformations",
    },
    {
        "step": 7,
        "claim": "Therefore the constant-sector route is a sharp conditional lemma, not a local-GR promotion.",
        "mathematical_step": "P8_species_source_charge and R1/R2/R11 remain retained until C0-C7 are parent-derived or empirically bounded",
        "status": "no_promotion",
        "gap": "the next proof target is source-current Ward universality",
    },
]


UNIVERSALITY_ROUTES = [
    {
        "route": "superselection_representation_data",
        "core_idea": "Masses, charges, and clock constants are fixed representation parameters, not dynamical MTS fields.",
        "what_it_can_prove": "partial_Z theta_A=partial_m theta_A=0 if the parent action declares a trivial MTS action on Rep_A",
        "what_it_cannot_prove_yet": "that active gravity weights all stress currents with one kappa_univ",
        "status": "promising_conditional_route",
    },
    {
        "route": "diffeomorphism_or_Ward_stress_current",
        "core_idea": "The common observed coframe variation defines one stress-energy source.",
        "what_it_can_prove": "universal geometric source if S_source is owned by delta S_m/delta e_obs",
        "what_it_cannot_prove_yet": "absence of extra kappa_A, boundary, bulk, or connection source charges",
        "status": "next_target",
    },
    {
        "route": "quotient_invariance",
        "core_idea": "Constants descend to quotient data.",
        "what_it_can_prove": "selector-relabeling blindness for non-invariant selector labels",
        "what_it_cannot_prove_yet": "theta_A(I_Q)=constant, because I_Q is quotient-invariant",
        "status": "insufficient_alone",
    },
    {
        "route": "empirical_constant_drift_bounds",
        "core_idea": "Clock/fine-structure/WEP data bound residual constant variation.",
        "what_it_can_prove": "numeric retained fallback rows if a model gives coefficients",
        "what_it_cannot_prove_yet": "theorem-zero or source-current universality",
        "status": "fallback_not_derivation",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "quotient_invariant_constant_function",
        "construction": "theta_A=theta_A(I_Q) with I_Q invariant under the parent quotient",
        "why_universality_not_forced": "the function is quotient-compatible but still MTS-dependent",
        "required_blocker": "trivial MTS action on constant-sector representations",
        "affected_rows": "R1;R2;R11",
    },
    {
        "counterexample": "species_source_weight",
        "construction": "S_source=sum_A kappa_A int e_obs J_A with kappa_A/kappa_B != 1",
        "why_universality_not_forced": "same observed geometry does not forbid species-weighted active source currents",
        "required_blocker": "source-current Ward universality theorem",
        "affected_rows": "R1;R4;R11",
    },
    {
        "counterexample": "universal_but_MTS_dependent_alpha",
        "construction": "alpha_EM=alpha_EM(I_Q) common to species",
        "why_universality_not_forced": "composition universality may survive, but clocks/spectroscopy and local-GR constant rows remain active",
        "required_blocker": "constant-sector no-running theorem or clock bounds",
        "affected_rows": "R2;R9;R11",
    },
    {
        "counterexample": "material_marker_constant_sector",
        "construction": "theta_A=theta_A(m) where m is a co-moving material or preparation marker",
        "why_universality_not_forced": "the marker can descend to an extended quotient unless a no-extension theorem forbids it",
        "required_blocker": "parent no-material-marker/no-extension theorem",
        "affected_rows": "R1;R2;R5;R11",
    },
    {
        "counterexample": "bulk_or_boundary_composition_charge",
        "construction": "q_XA X rho_A or boundary charge B_A sources composition-sensitive monopole",
        "why_universality_not_forced": "constant-sector universality in matter does not automatically erase non-matter source charges",
        "required_blocker": "bulk/boundary no-source-charge theorem",
        "affected_rows": "R1;R3;R4;R7;R10;R11",
    },
    {
        "counterexample": "renormalized_measured_GM_split",
        "construction": "mu_obs(A)=G_eff M_eff[A,theta_A]+mu_extra[A]",
        "why_universality_not_forced": "measured-GM calibration can absorb or hide source dependence unless the current is absolutely calibrated",
        "required_blocker": "closed calibrated source-current Ward identity",
        "affected_rows": "R1;R4;R9;R11",
    },
]


CONTRACT = [
    {
        "contract_id": "C0_constant_sector_definition",
        "required_identity": "constant-sector symbols are split into ordinary species representation constants and active MTS/source charges",
        "mathematical_form": "theta_A=(m_A,q_A,y_A,clock_A,...) but active hazards are partial_Z theta_A, partial_m theta_A, kappa_A, q_XA",
        "closes_component": "definition guardrail",
        "affected_rows": "R1;R2;R11",
        "current_status": "written_definition",
        "evidence_needed": "variable audit maps each theta symbol to ordinary representation data or active source charge",
        "fallback_if_missing": "ambiguous constants remain retained P8/R2 rows",
    },
    {
        "contract_id": "C1_superselection_independence",
        "required_identity": "MTS selectors, memory variables, quotient invariants, and material markers act trivially on matter constants",
        "mathematical_form": "partial_Z theta_A=partial_IQ theta_A=partial_m theta_A=0",
        "closes_component": "constant-sector MTS dependence",
        "affected_rows": "R1;R2;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "parent symmetry or superselection theorem for Rep_A",
        "fallback_if_missing": "theta_A(I_Q) and theta_A(m) counterexamples remain legal",
    },
    {
        "contract_id": "C2_no_direct_constant_vertices",
        "required_identity": "matter constants do not generate direct MTS vertices at fixed observed coframe",
        "mathematical_form": "no m_A(Z), alpha_EM(Z)F^2, q_A X_mu J_A^mu, lambda_A V_def O_A",
        "closes_component": "direct WEP/clock/fifth-force constant vertices",
        "affected_rows": "R1;R2;R3;R10;R11",
        "current_status": "forbidden_vertex_policy_only",
        "evidence_needed": "parent action argument theorem excluding direct memory/projector fields from S_m",
        "fallback_if_missing": "forbidden vertices become executable residual rows",
    },
    {
        "contract_id": "C3_universal_source_variation",
        "required_identity": "active gravitational source is the common observed-coframe variation of the same matter action",
        "mathematical_form": "J_grav=delta S_m/delta e_obs and S_source not sum_A kappa_A J_A",
        "closes_component": "species source-weight split",
        "affected_rows": "R1;R4;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "source-current Ward universality theorem",
        "fallback_if_missing": "kappa_A source weights remain retained",
    },
    {
        "contract_id": "C4_no_constant_running_from_local_MTS",
        "required_identity": "universal constants do not run with local MTS invariants in the local-GR branch",
        "mathematical_form": "nabla_mu theta_univ=0 locally or coefficient vector below clock/fine-structure bounds",
        "closes_component": "clock/redshift/constant-drift pressure",
        "affected_rows": "R2;R9;R11",
        "current_status": "not_derived",
        "evidence_needed": "local no-running theorem or executable clock/fine-structure residual model",
        "fallback_if_missing": "R2/R9 clock and drift rows remain retained",
    },
    {
        "contract_id": "C5_no_bulk_boundary_constant_charge",
        "required_identity": "bulk, boundary, connection, and class sectors carry no composition-dependent constant/source charge",
        "mathematical_form": "q_XA=q_BA=q_connection,A=0",
        "closes_component": "non-matter source-charge bypass",
        "affected_rows": "R1;R3;R4;R7;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "bulk/boundary/connection no-source-charge theorem",
        "fallback_if_missing": "R1 direct source-charge and R10 fifth-force rows remain visible",
    },
    {
        "contract_id": "C6_measured_GM_absolute_calibration",
        "required_identity": "measured source monopole is calibrated to the same conserved mass/stress current independent of composition",
        "mathematical_form": "mu_obs=kappa_univ M_inertial plus theorem-zero mu_extra, so partial_A ln(mu_obs/M_inertial)=0",
        "closes_component": "source-normalization species split",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "closed calibrated source-current identity",
        "fallback_if_missing": "P8_species_source_charge and measured-GM rows remain retained",
    },
    {
        "contract_id": "C7_empirical_fallback",
        "required_identity": "any surviving constant/source dependence must be parameterized with units, source path, and bound",
        "mathematical_form": "eta_source_AB, alpha_clock, dot_alpha/alpha, delta_G/G, or alpha_X(lambda)",
        "closes_component": "none; retained executable branch only",
        "affected_rows": "R1;R2;R3;R4;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "numeric residual coefficients or derived theorem-zero",
        "fallback_if_missing": "no WEP/Newton/PPN/local-GR claim",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_superselection_theorem_written",
        "pass_condition": "constant-sector superselection route implies no extra species source charge if source current is universal",
        "current_result": "pass_conditional",
        "evidence": "proof chain recorded",
    },
    {
        "gate": "ordinary_species_constants_not_overforbidden",
        "pass_condition": "the checkpoint does not claim all particle constants must be numerically equal",
        "current_result": "pass",
        "evidence": "definition guardrail recorded",
    },
    {
        "gate": "quotient_invariance_not_overclaimed",
        "pass_condition": "theta_A(I_Q) counterexample remains visible",
        "current_result": "pass",
        "evidence": "counterexample table recorded",
    },
    {
        "gate": "constant_sector_parent_derived",
        "pass_condition": "C0-C6 are parent-derived identities",
        "current_result": "fail",
        "evidence": "superselection, source-current Ward, no-running, and measured-GM calibration theorems remain open",
    },
    {
        "gate": "P8_species_source_charge_theorem_zero",
        "pass_condition": "partial_A ln(mu_obs/M_inertial)=0 by theorem",
        "current_result": "fail",
        "evidence": "contract only; source-current universality not derived",
    },
    {
        "gate": "local_GR_promoted",
        "pass_condition": "full R0-R11 vector and parent premises are cleared",
        "current_result": "fail",
        "evidence": "constant-sector checkpoint only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "constant-sector conditional theorem written",
        "status": "pass_conditional",
        "evidence": "superselection plus universal source-current proof chain",
    },
    {
        "claim": "ordinary species constants preserved",
        "status": "pass",
        "evidence": "the theorem targets active MTS/source dependence, not numerical equality of masses/charges",
    },
    {
        "claim": "constant-sector contract written",
        "status": "pass",
        "evidence": str(CONTRACT_PATH),
    },
    {
        "claim": "constant-sector universality parent-derived",
        "status": "fail",
        "evidence": "the parent symmetry/no-extension/source-current Ward theorem is still missing",
    },
    {
        "claim": "P8/R1/R2 theorem-zero promoted",
        "status": "fail",
        "evidence": "counterexamples remain legal",
    },
    {
        "claim": "Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "source-charge and clock constant rows remain retained",
    },
]


DECISION = [
    {
        "decision": "Constant-sector universality has a clean conditional route: treat matter constants as superselection/representation data with trivial MTS action, forbid direct memory/projector/marker vertices, and derive the active source as the common observed-coframe Ward current. Under those premises, constants change inertial composition but do not create an extra species/source charge. The current corpus does not yet derive those premises, and quotient invariance alone is insufficient because theta_A(I_Q) is legal. Therefore P8_species_source_charge plus R1/R2/R11 remain retained, with no Newton, PPN, WEP, measured-GM, or local-GR promotion.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": NEXT_TARGET,
        "why_next": "source-current Ward universality is the missing bridge from constant-sector independence to measured-GM/source-charge zero",
    },
    {
        "rank": 2,
        "target": "derive no-material-marker/no-extension theorem",
        "why_next": "theta_A(m) remains legal until co-moving material markers are parent-forbidden",
    },
    {
        "rank": 3,
        "target": "map constant-sector residuals into R2/R9 clock and fine-structure rows",
        "why_next": "universal but MTS-dependent constants may evade WEP while still failing local GR",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as output_handle:
        writer = csv.DictWriter(output_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for data_row in rows:
        values = []
        for fieldname in fieldnames:
            value = str(data_row.get(fieldname, ""))
            value = value.replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    source_register = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        source_register.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return source_register


def build_gate_results(source_register: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]
    expected_contract_columns = CONTRACT_COLUMNS
    gate_results = [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "contract_schema_matches",
            "status": "pass" if list(CONTRACT[0].keys()) == expected_contract_columns else "fail",
            "evidence": "constant-sector contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 3 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem statement rows",
        },
        {
            "gate": "proof_steps_written",
            "status": "pass" if len(PROOF_STEPS) == 7 else "fail",
            "evidence": f"{len(PROOF_STEPS)} proof steps recorded",
        },
        {
            "gate": "universality_routes_written",
            "status": "pass" if len(UNIVERSALITY_ROUTES) == 4 else "fail",
            "evidence": f"{len(UNIVERSALITY_ROUTES)} route rows recorded",
        },
        {
            "gate": "counterexamples_written",
            "status": "pass" if len(COUNTEREXAMPLES) == 6 else "fail",
            "evidence": f"{len(COUNTEREXAMPLES)} counterexamples recorded",
        },
        {
            "gate": "constant_sector_contract_written",
            "status": "pass",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "ordinary_species_constants_not_overforbidden",
            "status": "pass",
            "evidence": "the theorem distinguishes species representation data from active MTS/source charges",
        },
        {
            "gate": "quotient_invariance_not_overclaimed",
            "status": "pass",
            "evidence": "theta_A(I_Q) remains a legal counterexample",
        },
        {
            "gate": "constant_sector_parent_derived",
            "status": "fail",
            "evidence": "superselection/trivial-MTS-action theorem is not parent-derived",
        },
        {
            "gate": "source_current_universality_derived",
            "status": "fail",
            "evidence": "J_grav=delta S_m/delta e_obs is next target, not established here",
        },
        {
            "gate": "P8_species_source_charge_theorem_zero",
            "status": "fail",
            "evidence": "kappa_A/q_XA/mu_obs(A) counterexamples remain legal",
        },
        {
            "gate": "R2_clock_constant_rows_zero",
            "status": "fail",
            "evidence": "universal but MTS-dependent alpha_EM(I_Q) remains possible",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "constant-sector theorem attempt only",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 448 - Constant-Sector Universality Theorem Attempt

Private P8/R1/R2 constant-sector checkpoint. This is not a public WEP, clock, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, R10/R11, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 447 showed that one observed coframe is not enough to kill source charge. The sharpest remaining subcondition is whether matter constants and source charges are genuinely universal with respect to MTS selectors, quotient invariants, material markers, and active source weighting.

The important guardrail: this checkpoint does not demand equal particle masses or charges. It asks whether the parent action forbids MTS-dependent constants and species-weighted active gravitational source currents.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/constant_sector_universality_theorem_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Conditional Proof Steps

{markdown_table(PROOF_STEPS)}

## 6. Universality Routes

{markdown_table(UNIVERSALITY_ROUTES)}

## 7. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 8. Constant-Sector Contract

The constant-sector universality contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 9. Gate Tests

{markdown_table(GATE_TESTS)}

## 10. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 11. Gate Results

{markdown_table(gate_results)}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this route is alive, but not closed. The clean way through is not “all constants equal”; it is `theta_A` as ordinary species representation data, no MTS-dependent constant functions, and one Ward-owned source current. If the parent can prove that, source charge starts to look like GR-style universality rather than a closure patch. If it cannot, the constant sector remains an explicit residual branch.

## 13. Next Queue

{markdown_table(NEXT_QUEUE)}
"""


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_register = build_source_register()
    gate_results = build_gate_results(source_register)
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]

    write_csv(results_dir / "source_register.csv", source_register)
    write_csv(results_dir / "theorem_statement.csv", THEOREM_STATEMENT)
    write_csv(results_dir / "proof_steps.csv", PROOF_STEPS)
    write_csv(results_dir / "universality_routes.csv", UNIVERSALITY_ROUTES)
    write_csv(results_dir / "counterexamples.csv", COUNTEREXAMPLES)
    write_csv(results_dir / "constant_sector_contract.csv", CONTRACT, CONTRACT_COLUMNS)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_status.csv", THEOREM_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_results)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / CONTRACT_PATH, CONTRACT, CONTRACT_COLUMNS)

    doc_text = render_doc(run_dir, source_register, gate_results)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status_payload = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "conditional_superselection_theorem_written": True,
        "ordinary_species_constants_not_overforbidden": True,
        "quotient_invariance_alone_sufficient": False,
        "constant_sector_parent_derived": False,
        "source_current_universality_derived": False,
        "P8_species_source_charge_derived_zero": False,
        "R1_source_charge_promoted": False,
        "R2_clock_constant_rows_zero": False,
        "local_GR_claim_allowed": False,
        "counterexamples": len(COUNTEREXAMPLES),
        "contract_rows": len(CONTRACT),
        "failed_gates": [gate_row["gate"] for gate_row in gate_results if gate_row["status"] == "fail"],
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\n{datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the MTS constant-sector universality theorem attempt checkpoint.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-153000.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
