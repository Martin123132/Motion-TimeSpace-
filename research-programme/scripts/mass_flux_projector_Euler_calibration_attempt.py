from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "mass-flux-projector-Euler-calibration-attempt"
CHECKPOINT_DOC = "451-mass-flux-projector-Euler-calibration-attempt.md"
STATUS = "mass_flux_projector_Euler_calibration_attempt_written_conditional_flux_closure_contract_parent_origin_not_derived_absolute_calibration_open_no_measured_GM_Newton_or_local_GR_pass"
CLAIM_CEILING = "mass_flux_projector_Euler_calibration_attempt_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "452-constant-universal-Geff-kappa-identity-attempt.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv")


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
        "path": "232-parent-Pmem-projector-or-source-identity-variation.md",
        "role": "Pi_M/P_mem projector split and source identity origin",
    },
    {
        "path": "233-boundary-symplectic-metric-or-local-EH-operator.md",
        "role": "boundary symplectic metric candidate for Pi_M",
    },
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional closed Pi_M flux implies radially conserved M_eff",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "GM absorption distinction and constant universal monopole requirements",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "A7 mass-flux projector Euler ledger row",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole calibration gate",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "HM2/HM3 mass-flux closure and absolute calibration contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
        "role": "SC6 closed calibrated mass projector requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "C3 closed calibrated mass current requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "A4 mass-flux projector parent action block",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 source-normalization residual fallback rows",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "machine Euler ledger row A7",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv",
        "role": "mu_obs decomposition and source-normalization objects",
    },
    {
        "path": "runs/20260602-160000-Hilbert-source-to-measured-monopole-calibration-gate/results/Hilbert_monopole_calibration_contract.csv",
        "role": "machine Hilbert-monopole calibration contract",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_Euler_flux_closure",
        "statement": "If the parent action contains a physically owned mass-flux projector Pi_M and a source-normalization constraint whose Euler equation is d(Pi_M J_H)=0, then the projected Hilbert mass current is closed in the compact exterior and M_eff is radially conserved.",
        "mathematical_form": "E_lambdaM=delta S_parent/delta lambda_M=0 => d(Pi_M J_H)=0; M_eff(r2)-M_eff(r1)=int_{S2xI} d(Pi_M J_H)=0",
        "status": "valid_conditional_flux_closure",
    },
    {
        "part": "no_cheat_multiplier_limit",
        "statement": "Adding a multiplier solely to impose the desired GM result is not a parent derivation unless Pi_M, J_H, lambda_M, and the source-normalization constraint have an independent symmetry/topological/Ward/symplectic origin.",
        "mathematical_form": "S += int lambda_M d(Pi_M J_H) is closure-only without parent-origin evidence",
        "status": "blocks_overclaim",
    },
    {
        "part": "current_corpus_status",
        "statement": "The corpus has a sharp conditional flux theorem and candidate boundary/projector origins, but it has not derived Pi_M from a completed parent symplectic/source identity or calibrated M_eff to measured orbital GM.",
        "mathematical_form": "Pi_M origin, E_lambdaM equation, and M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H remain open",
        "status": "not_parent_derived",
    },
]


EULER_ATTEMPTS = [
    {
        "attempt_id": "E0_topological_flux_constraint",
        "proposed_action_term": "S_M = int lambda_M wedge d(Pi_M J_H)",
        "Euler_equation": "delta_lambdaM S_M=0 => d(Pi_M J_H)=0",
        "what_it_would_close": "radial M_eff conservation",
        "legality_condition": "lambda_M and Pi_M arise from parent gauge/topological/source identity, not ad hoc GM repair",
        "current_status": "conditional_contract_not_parent_derived",
    },
    {
        "attempt_id": "E1_boundary_symplectic_projector",
        "proposed_action_term": "Pi_M defined as the absolute H^2/S^2 harmonic component of the boundary symplectic current",
        "Euler_equation": "orthogonality of Pi_M, Pi_TF, Pi_matter, P_mem under the parent symplectic form",
        "what_it_would_close": "projector is not readout-defined and preserves the mass class",
        "legality_condition": "explicit symplectic metric, projector algebra, and variation of Pi_M are supplied",
        "current_status": "candidate_origin_not_completed",
    },
    {
        "attempt_id": "E2_source_Ward_current_closure",
        "proposed_action_term": "J_H is the Hilbert current and Pi_M is the conserved mass channel selected by Ward/source ownership",
        "Euler_equation": "d(Pi_M J_H)=0 follows from separate matter/source Ward identity plus zero retained exchange",
        "what_it_would_close": "mass-current closure without an extra multiplier",
        "legality_condition": "non-Hilbert q_retained=0 and zero boundary flux are separately derived",
        "current_status": "blocked_by_q_retained_and_boundary_flux",
    },
    {
        "attempt_id": "E3_absolute_calibration_constraint",
        "proposed_action_term": "S_cal = eta_M (M_eff - (4 pi G_ref)^-1 int_S2 Pi_M J_H)",
        "Euler_equation": "delta_etaM S_cal=0 => M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H",
        "what_it_would_close": "definition-level absolute monopole normalization",
        "legality_condition": "G_ref and orbital/asymptotic calibration are parent-selected or matched to EH/Poisson boundary data",
        "current_status": "calibration_constraint_not_physics_yet",
    },
    {
        "attempt_id": "E4_asymptotic_orbital_matching",
        "proposed_action_term": "match exterior weak-field solution Phi=-mu_obs/r to the parent-defined Hilbert monopole",
        "Euler_equation": "surface Gauss law fixes mu_obs=G_eff M_eff when no mu_extra survives",
        "what_it_would_close": "observed orbital GM equality",
        "legality_condition": "EH/Poisson operator, constant G_eff, and zero mu_extra are already derived",
        "current_status": "conditional_after_EH_source_gates",
    },
]


LEGALITY_TESTS = [
    {
        "test_id": "L0_projector_origin",
        "pass_condition": "Pi_M is derived from parent cohomology/symplectic/source identity before readout",
        "current_result": "fail_open",
        "evidence": "candidate Pi_M/H^2 language exists, but no completed projector algebra and variation",
    },
    {
        "test_id": "L1_constraint_not_ad_hoc",
        "pass_condition": "lambda_M constraint is required independently by parent symmetry/topology/Ward identity",
        "current_result": "fail",
        "evidence": "no independent origin for a mass-flux closure multiplier is supplied",
    },
    {
        "test_id": "L2_flux_closure",
        "pass_condition": "d(Pi_M J_H)=0 follows as an Euler equation or Ward identity in compact exterior",
        "current_result": "conditional_not_parent_derived",
        "evidence": "checkpoint 244 gives the theorem if closure is assumed",
    },
    {
        "test_id": "L3_no_radial_hair",
        "pass_condition": "partial_r M_eff=0 and no boundary/range/domain radial source enters mu_obs",
        "current_result": "fail_open",
        "evidence": "P8 radial/boundary/range rows remain active",
    },
    {
        "test_id": "L4_absolute_calibration",
        "pass_condition": "M_eff normalization is tied to measured orbital/asymptotic GM, not arbitrary units",
        "current_result": "fail",
        "evidence": "absolute calibration remains HM3 not_parent_derived",
    },
    {
        "test_id": "L5_constant_Geff_needed",
        "pass_condition": "G_eff/kappa_eff is constant and universal before GM absorption",
        "current_result": "fail",
        "evidence": "next target is constant universal Geff/kappa identity",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "ad_hoc_lambdaM_constraint",
        "construction": "append lambda_M d(Pi_M J_H) after identifying a GM problem",
        "why_it_fails": "it imposes the desired closure rather than deriving why the source channel must be closed",
        "required_repair": "independent gauge/topological/Ward/symplectic origin for lambda_M and Pi_M",
        "affected_rows": "R1;R4;R9;R11",
    },
    {
        "counterexample": "readout_projector",
        "construction": "choose Pi_M after orbital fitting to isolate the successful 1/r monopole",
        "why_it_fails": "post-readout masks cannot backreact into S_parent or earn theorem-zero",
        "required_repair": "Pi_M appears in parent action/source identity before scoring",
        "affected_rows": "R0;R1;R4;R11",
    },
    {
        "counterexample": "closed_but_miscalibrated_flux",
        "construction": "d(Pi_M J_H)=0 but M_eff normalization differs from measured orbital GM",
        "why_it_fails": "radial conservation is not absolute calibration",
        "required_repair": "surface/asymptotic/orbital calibration theorem",
        "affected_rows": "R1;R4;R9;R10;R11",
    },
    {
        "counterexample": "boundary_flux_monopole",
        "construction": "Pi_M J_H is closed in bulk but boundary improvement contributes int_partialSigma K_owner",
        "why_it_fails": "compact boundary flux shifts the measured monopole",
        "required_repair": "zero compact boundary flux or universal constant calibration theorem",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
    },
    {
        "counterexample": "range_or_species_dependent_calibration",
        "construction": "M_eff is closed but mu_obs=G_eff(A,lambda) M_eff",
        "why_it_fails": "WEP-source/fifth-force physics is hidden in calibration",
        "required_repair": "constant universal G_eff and no source/range charge",
        "affected_rows": "R1;R9;R10;R11",
    },
    {
        "counterexample": "second_order_source_failure",
        "construction": "first-order flux closure works but beta receives nonlinear source-normalization residue",
        "why_it_fails": "Poisson source success is not full local GR",
        "required_repair": "second-order source closure",
        "affected_rows": "R4;R11",
    },
]


CONTRACT = [
    {
        "contract_id": "MF0_parent_projector_origin",
        "required_identity": "Pi_M is derived from parent cohomology/symplectic/source identity before readout",
        "mathematical_form": "Pi_M: J_H -> H^2_abs(Sigma_ext) mass-flux class",
        "closes_component": "projector not fitted/readout-defined",
        "affected_rows": "R0;R1;R4;R11",
        "current_status": "candidate_origin_not_completed",
        "evidence_needed": "explicit symplectic metric/projector algebra and variation",
        "fallback_if_missing": "mass projector remains closure-only",
    },
    {
        "contract_id": "MF1_source_current_input",
        "required_identity": "projected current is the Hilbert/Ward matter source from the same observed coframe",
        "mathematical_form": "J_H from delta S_m/delta e_obs",
        "closes_component": "ordinary source-current input",
        "affected_rows": "R1;R4;R11",
        "current_status": "conditional_from_449",
        "evidence_needed": "one observed coframe and source-current Ward theorem",
        "fallback_if_missing": "source current remains fitted/readout-defined",
    },
    {
        "contract_id": "MF2_Euler_flux_closure",
        "required_identity": "parent Euler equation or Ward source identity closes the projected mass current",
        "mathematical_form": "E_lambdaM=0 or Ward_M => d(Pi_M J_H)=0",
        "closes_component": "P8_Meff_conservation",
        "affected_rows": "R4;R7;R9;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "derive the lambda_M/Pi_M Euler equation or separate mass Ward identity",
        "fallback_if_missing": "M_eff drift/source-flux residual row",
    },
    {
        "contract_id": "MF3_no_ad_hoc_multiplier",
        "required_identity": "closure constraint has independent parent reason and is not added solely to force GM success",
        "mathematical_form": "lambda_M is gauge/topological/Ward/symplectic-owned",
        "closes_component": "no-cheat closure rule",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "not_satisfied",
        "evidence_needed": "independent origin for lambda_M and source-normalization constraint",
        "fallback_if_missing": "closure counted as assumption only",
    },
    {
        "contract_id": "MF4_radial_conservation",
        "required_identity": "closed projected flux makes M_eff radially constant over exterior annuli",
        "mathematical_form": "M_eff(r2)-M_eff(r1)=int_{S2xI} d(Pi_M J_H)=0",
        "closes_component": "P8_radial_source_hair if no boundary/range terms",
        "affected_rows": "R3;R4;R10;R11",
        "current_status": "conditional_from_244",
        "evidence_needed": "MF2 plus no boundary/range/domain source terms",
        "fallback_if_missing": "radial source hair remains active",
    },
    {
        "contract_id": "MF5_absolute_calibration",
        "required_identity": "M_eff normalization equals the orbital/asymptotic measured monopole",
        "mathematical_form": "M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H and mu_obs=G_eff M_eff",
        "closes_component": "measured-GM normalization",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "EH/Poisson/asymptotic matching and parent-selected G_ref",
        "fallback_if_missing": "closed mass flux is not measured Newtonian mass",
    },
    {
        "contract_id": "MF6_zero_boundary_and_nonHilbert_flux",
        "required_identity": "no owned boundary, bulk, domain, memory, range, or connection flux shifts the monopole",
        "mathematical_form": "mu_extra=0 or retained with units and row locks",
        "closes_component": "P8_boundary_bulk_domain_mu_extra",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "K_owner formula, zero-flux theorem, no-hair theorem, or executable residuals",
        "fallback_if_missing": "P8 residual vector blocks Newton claim",
    },
    {
        "contract_id": "MF7_constant_universal_coupling_needed",
        "required_identity": "G_eff/kappa_eff does not carry time/range/species/frame dependence",
        "mathematical_form": "partial_{t,r,A,lambda}G_eff=0",
        "closes_component": "Gdot/source/fifth-force calibration drift",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant universal Geff/kappa identity",
        "fallback_if_missing": "next target remains active; no Newton/local-GR claim",
    },
    {
        "contract_id": "MF8_retained_residual_fallback",
        "required_identity": "any failed mass-flux condition becomes executable residual data",
        "mathematical_form": "dln_Meff_dt, partial_r ln mu_obs, mu_extra/(GM), eta_source, alpha(lambda)",
        "closes_component": "none; retained branch only",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "numeric residual coefficient/curve or theorem-zero",
        "fallback_if_missing": "no measured-GM/Newton/PPN/local-GR claim",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_Euler_flux_closure_written",
        "pass_condition": "Euler/constraint route to d(Pi_M J_H)=0 is explicit",
        "current_result": "pass_conditional",
        "evidence": "E0 and MF2 recorded",
    },
    {
        "gate": "ad_hoc_multiplier_blocked",
        "pass_condition": "lambda_M closure is not accepted without independent parent origin",
        "current_result": "pass",
        "evidence": "MF3 and counterexample recorded",
    },
    {
        "gate": "radial_conservation_conditional",
        "pass_condition": "closed flux implies M_eff(r) constant by Stokes/Gauss",
        "current_result": "pass_conditional",
        "evidence": "checkpoint 244 theorem imported",
    },
    {
        "gate": "Pi_M_parent_origin_derived",
        "pass_condition": "Pi_M projector algebra and variation are parent-derived",
        "current_result": "fail",
        "evidence": "candidate H^2/symplectic route not completed",
    },
    {
        "gate": "absolute_calibration_derived",
        "pass_condition": "M_eff normalization is tied to measured orbital GM",
        "current_result": "fail",
        "evidence": "MF5 remains not_parent_derived",
    },
    {
        "gate": "measured_GM_parent_derived",
        "pass_condition": "MF0-MF7 close with no active residuals",
        "current_result": "fail",
        "evidence": "flux closure, calibration, zero mu_extra, and constant G_eff remain open",
    },
]


THEOREM_STATUS = [
    {
        "claim": "mass-flux Euler closure route written",
        "status": "pass_conditional",
        "evidence": "E0/MF2 supply exact equation that would close Pi_M J_H",
    },
    {
        "claim": "fake multiplier shortcut blocked",
        "status": "pass",
        "evidence": "MF3 requires independent parent origin",
    },
    {
        "claim": "radial M_eff conservation recovered conditionally",
        "status": "pass_conditional",
        "evidence": "d(Pi_M J_H)=0 implies M_eff(r2)=M_eff(r1)",
    },
    {
        "claim": "Pi_M parent-derived",
        "status": "fail",
        "evidence": "projector origin remains candidate/symplectic route only",
    },
    {
        "claim": "absolute measured-GM calibration parent-derived",
        "status": "fail",
        "evidence": "surface/orbital/asymptotic calibration is not derived",
    },
    {
        "claim": "Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "P8 source-normalization rows remain retained",
    },
]


DECISION = [
    {
        "decision": "The mass-flux projector Euler route has been attempted. It gives a clean conditional mechanism: if Pi_M has a parent symplectic/cohomological/source identity origin and the parent variation supplies E_lambdaM=0, then d(Pi_M J_H)=0 and M_eff is radially conserved by Stokes. But this is not yet a parent derivation. A multiplier added solely to force closure is closure-only, Pi_M projector algebra is not completed, absolute calibration to orbital GM is not derived, boundary/non-Hilbert fluxes remain open, and constant universal G_eff is still missing. Therefore the path is sharpened but measured GM, Newton, PPN, and local GR remain unpromoted.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": NEXT_TARGET,
        "why_next": "even a closed calibrated mass flux is not Newtonian unless G_eff/kappa is constant and universal",
    },
    {
        "rank": 2,
        "target": "453-PiM-parent-symplectic-projector-algebra-attempt.md",
        "why_next": "Pi_M still needs an actual parent projector algebra and variation",
    },
    {
        "rank": 3,
        "target": "map MF0-MF8 into P8 residual evaluator",
        "why_next": "failed mass-flux conditions should activate measured-GM residual rows automatically",
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
    gate_results = [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "contract_schema_matches",
            "status": "pass" if list(CONTRACT[0].keys()) == CONTRACT_COLUMNS else "fail",
            "evidence": "mass-flux projector contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 3 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "Euler_attempts_written",
            "status": "pass" if len(EULER_ATTEMPTS) == 5 else "fail",
            "evidence": f"{len(EULER_ATTEMPTS)} Euler attempts",
        },
        {
            "gate": "legality_tests_written",
            "status": "pass" if len(LEGALITY_TESTS) == 6 else "fail",
            "evidence": f"{len(LEGALITY_TESTS)} legality tests",
        },
        {
            "gate": "counterexamples_written",
            "status": "pass" if len(COUNTEREXAMPLES) == 6 else "fail",
            "evidence": f"{len(COUNTEREXAMPLES)} counterexamples",
        },
        {
            "gate": "contract_written",
            "status": "pass",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "ad_hoc_multiplier_blocked",
            "status": "pass",
            "evidence": "MF3 requires independent parent origin",
        },
        {
            "gate": "radial_conservation_conditional",
            "status": "pass",
            "evidence": "closed Pi_M flux implies M_eff(r) constant",
        },
        {
            "gate": "Pi_M_parent_origin_derived",
            "status": "fail",
            "evidence": "parent symplectic/cohomology projector algebra not completed",
        },
        {
            "gate": "Euler_flux_closure_parent_derived",
            "status": "fail",
            "evidence": "d(Pi_M J_H)=0 remains conditional, not parent-derived",
        },
        {
            "gate": "absolute_calibration_parent_derived",
            "status": "fail",
            "evidence": "M_eff to measured orbital GM calibration remains open",
        },
        {
            "gate": "zero_boundary_nonHilbert_flux_derived",
            "status": "fail",
            "evidence": "boundary/non-Hilbert source flux remains open",
        },
        {
            "gate": "constant_Geff_parent_derived",
            "status": "fail",
            "evidence": "next target remains active",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "MF0-MF7 not all closed",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "mass-flux projector attempt only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "P8 and PPN source-normalization rows remain retained",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 451 - Mass-Flux Projector Euler Calibration Attempt

Private P8/R1/R4/R9/R10/R11 mass-flux projector checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 450 isolated the missing measured-GM machine: the Hilbert source must be projected by a closed, absolutely calibrated mass-flux projector `Pi_M`.

This checkpoint attempts the Euler route: can the parent action supply an equation whose content is `d(Pi_M J_H)=0`, and can that be treated as a derivation rather than an inserted calibration closure?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/mass_flux_projector_Euler_calibration_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Euler Attempts

{markdown_table(EULER_ATTEMPTS)}

## 6. Legality Tests

{markdown_table(LEGALITY_TESTS)}

## 7. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 8. Mass-Flux Projector Contract

The mass-flux projector Euler/calibration contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 9. Gate Tests

{markdown_table(GATE_TESTS)}

## 10. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 11. Gate Results

{markdown_table(gate_results)}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is a useful almost-derivation. The mathematical closure is easy once `d(Pi_M J_H)=0` is honestly supplied; the hard part is earning `Pi_M` and the closure equation from the parent theory. No sneaky `lambda_M` magic wand. Write the projector algebra or keep the source-normalization row retained.

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
    write_csv(results_dir / "Euler_attempts.csv", EULER_ATTEMPTS)
    write_csv(results_dir / "legality_tests.csv", LEGALITY_TESTS)
    write_csv(results_dir / "counterexamples.csv", COUNTEREXAMPLES)
    write_csv(results_dir / "mass_flux_projector_contract.csv", CONTRACT, CONTRACT_COLUMNS)
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
        "conditional_Euler_flux_closure_written": True,
        "ad_hoc_multiplier_blocked": True,
        "radial_conservation_conditional": True,
        "Pi_M_parent_origin_derived": False,
        "Euler_flux_closure_parent_derived": False,
        "absolute_calibration_parent_derived": False,
        "zero_boundary_nonHilbert_flux_derived": False,
        "constant_Geff_parent_derived": False,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
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
    parser = argparse.ArgumentParser(description="Write the MTS mass-flux projector Euler/calibration attempt.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-161500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
