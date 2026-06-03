from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "global-coupling-superselection-parent-action-contract"
CHECKPOINT_DOC = "453-global-coupling-superselection-parent-action-contract.md"
STATUS = "global_coupling_superselection_parent_action_contract_written_exact_parent_options_kappa_global_not_parent_derived_Gdot_source_range_rows_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "global_coupling_superselection_contract_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "454-PiM-parent-symplectic-projector-algebra-attempt.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_global_coupling_superselection_CONTRACT.csv")


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
        "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "immediate constant G_eff/kappa identity attempt and CU0-CU8 contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "role": "constant universal G_eff/kappa contract feeding this superselection gate",
    },
    {
        "path": "448-constant-sector-universality-theorem-attempt.md",
        "role": "constant-sector superselection pattern and quotient-invariance warning",
    },
    {
        "path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
        "role": "constant-sector contract showing trivial MTS action requirements",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source normalization and G_eff algebra",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "Poisson reduction gate requiring same-frame constant kappa",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux closure attempt showing measured-GM still needs constant coupling",
    },
    {
        "path": "260-C3-unit-stress-normalization-parent-action-attempt.md",
        "role": "older unit/stress normalization caveat against typing constants into the action",
    },
    {
        "path": "255-memory-stress-exchange-normalization-or-kappa-mem-free.md",
        "role": "kappa_mem analogy and warning not to confuse cosmological memory normalization with local kappa_eff",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/Ward_identity_chain.csv",
        "role": "Bianchi/Ward chain exposing T_obs grad kappa_eff exchange term",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/source_residual_decomposition.csv",
        "role": "delta_kappa_source residual mapping",
    },
    {
        "path": "runs/20260601-191500-universal-matter-coupling-theorem-attempt/results/matter_action_contract.csv",
        "role": "single observed geometry and matter constants contract",
    },
    {
        "path": "runs/20260601-191500-universal-matter-coupling-theorem-attempt/results/forbidden_vertices.csv",
        "role": "forbidden matter-memory/source vertices",
    },
    {
        "path": "runs/20260601-000057-universal-coupling-parent-contract-or-local-bound-data-runner/results/universal_coupling_contract.csv",
        "role": "universal coupling and constants-not-memory-fields contract",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/parent_action_blocks.csv",
        "role": "source-owner parent-action blocks and coupling/source-normalization requirements",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_superselection_contract",
        "statement": "If the parent configuration space factorizes into dynamical fields times a global coupling sector, kappa_eff belongs only to the global sector, and all MTS selectors, matter labels, source labels, range labels, frames, and local variations act trivially on that sector, then d kappa_eff=0 and G_eff is constant and universal.",
        "mathematical_form": "Q_parent=Q_dyn x K_global; kappa_eff in K_global; delta_local kappa_eff=0; L_xi kappa_eff=0; partial_{Z,A,lambda,r,t,frame} kappa_eff=0 => dG_eff=0",
        "status": "valid_conditional_route",
    },
    {
        "part": "exact_parent_action_contract",
        "statement": "A future parent action must state whether kappa_eff is a non-varied sector label, a topological/integration constant with a derived zero-gradient equation, or a local scalar/source-normalization field. The first two can keep Newton alive; the last reopens scalar-tensor and source residual branches.",
        "mathematical_form": "kappa_eff notin Gamma(local scalar bundle) OR E_A3: d kappa_eff=0; otherwise q_loc contains kappa_eff^-1 P_loc[T_obs nabla kappa_eff]",
        "status": "contract_written_not_parent_derived",
    },
    {
        "part": "no_derivation_warning",
        "statement": "Declaring kappa_eff global is a legitimate theory-sector premise, but it is not yet a derivation from MTS primitives. The corpus currently has repeated requirements for constant kappa_eff, not a completed superselection proof.",
        "mathematical_form": "CU1/GS1 remain not_parent_derived",
        "status": "blocks_overclaim",
    },
    {
        "part": "Bianchi_arbitrary_source_route",
        "statement": "Bianchi can force local gradients of kappa_eff to vanish only under the stronger premise that the same-frame matter stress is separately conserved for arbitrary local sources and there are no hidden exchange owners. With exchange sectors retained, Bianchi maps gradients into residuals instead of killing them.",
        "mathematical_form": "nabla_mu T_obs^{mu nu}=0 for arbitrary T_obs and nabla E_EH=0 => T_obs^{mu nu} nabla_mu kappa_eff=0 => nabla kappa_eff=0; with exchange, term remains in q_loc",
        "status": "conditional_only",
    },
    {
        "part": "scalar_branch_fallback",
        "statement": "If kappa_eff is allowed to depend on MTS invariants, local memory, species/source labels, radius, range, or frame, it is no longer a Newton constant. It becomes an executable residual branch that must be derived zero or bounded.",
        "mathematical_form": "kappa_eff=kappa0 F(Z,I_Q,C_D,A,lambda,r,t,frame) => R1/R4/R9/R10/R11 active",
        "status": "retained_fallback",
    },
]


PARENT_OPTIONS = [
    {
        "option": "P0_superselection_parameter",
        "mechanism": "kappa_eff is a non-dynamical global coupling labeling a theory sector.",
        "mathematical_form": "kappa_eff in K_global; not varied by compact-support local variations",
        "what_it_closes": "local d kappa_eff, Gdot, source/range/radial running if all MTS actions are trivial",
        "cost_or_warning": "closure-level unless the parent explains why K_global is part of the configuration category",
        "current_status": "sufficient_as_explicit_premise_not_derived",
    },
    {
        "option": "P1_topological_zero_form",
        "mechanism": "derive kappa_eff as a closed zero-form or integration constant using a motivated topological pair.",
        "mathematical_form": "delta A_3 gives d kappa_eff=0 on connected local domains",
        "what_it_closes": "spacetime gradients without adding scalar force if kappa_eff has no kinetic/local matter vertex",
        "cost_or_warning": "needs actual parent topological sector and boundary policy; otherwise it is a dressed constraint",
        "current_status": "promising_future_parent_route_not_in_corpus",
    },
    {
        "option": "P2_Lagrange_zero_gradient",
        "mechanism": "insert a constraint field imposing d kappa_eff=0.",
        "mathematical_form": "S_constraint=int Lambda^mu partial_mu kappa_eff",
        "what_it_closes": "formal local gradients",
        "cost_or_warning": "ad hoc unless Lambda has gauge/topological origin; variation may add unowned stress",
        "current_status": "not_acceptable_as_bare_patch",
    },
    {
        "option": "P3_Bianchi_for_arbitrary_sources",
        "mechanism": "use same-frame Bianchi identity plus separately conserved arbitrary matter stress to force gradients to zero.",
        "mathematical_form": "T_obs^{mu nu} nabla_mu kappa_eff=0 for arbitrary T_obs => nabla kappa_eff=0",
        "what_it_closes": "local spacetime gradients of kappa_eff",
        "cost_or_warning": "fails when hidden exchange, non-EH divergence, boundary flux, or nonmetric matter exchange remains active",
        "current_status": "conditional_narrow_route",
    },
    {
        "option": "P4_units_calibration",
        "mechanism": "treat a constant rescaling of kappa_eff as measured-G calibration.",
        "mathematical_form": "kappa_eff=kappa0 constant; G_measured absorbs kappa0",
        "what_it_closes": "absolute value overclaim only",
        "cost_or_warning": "does not derive constancy and does not predict numerical G",
        "current_status": "policy_only",
    },
    {
        "option": "P5_scalar_field_branch",
        "mechanism": "allow kappa_eff to be a local scalar or MTS function and carry it as a residual branch.",
        "mathematical_form": "kappa_eff=kappa0 F(Z,I_Q,C_D,A,lambda,r,t)",
        "what_it_closes": "nothing automatically",
        "cost_or_warning": "becomes scalar-tensor/source-normalization physics with Gdot, fifth-force, and source-charge locks",
        "current_status": "retained_fallback_if_P0_P1_P3_fail",
    },
]


CONTRACT = [
    {
        "contract_id": "GS0_configuration_factorization",
        "required_identity": "the parent configuration category splits dynamical MTS/local fields from a global coupling sector",
        "mathematical_form": "Q_parent=Q_dyn x K_global with kappa_eff in K_global",
        "closes_component": "local-field interpretation of kappa_eff",
        "affected_rows": "R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "parent action or categorical statement showing K_global is not a local scalar bundle",
        "fallback_if_missing": "kappa_eff remains a possible local source-normalization field",
    },
    {
        "contract_id": "GS1_kappa_not_local_field",
        "required_identity": "kappa_eff is not varied by compact-support local variations and has no local Euler-Lagrange equation",
        "mathematical_form": "delta_local kappa_eff=0; kappa_eff notin Gamma(E_local)",
        "closes_component": "local gradient, local scalar force, scalar-tensor leakage",
        "affected_rows": "R3;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "superselection or topological zero-form derivation",
        "fallback_if_missing": "retain scalar-kappa branch and PPN/fifth-force locks",
    },
    {
        "contract_id": "GS2_trivial_MTS_action_on_kappa",
        "required_identity": "MTS selectors, memory variables, quotient invariants, projector/domain data, and material markers act trivially on kappa_eff",
        "mathematical_form": "L_xi kappa_eff=0 and partial_Z kappa_eff=partial_IQ kappa_eff=partial_C kappa_eff=partial_D kappa_eff=0",
        "closes_component": "memory/domain/projector dependence of G_eff",
        "affected_rows": "R5;R6;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "parent symmetry/no-extension theorem forbidding kappa_eff(Z,I_Q,C_D,D_boundary)",
        "fallback_if_missing": "Gdot, domain, and fifth-force residual rows remain active",
    },
    {
        "contract_id": "GS3_no_species_marker_source_label",
        "required_identity": "kappa_eff carries no species, composition, source-owner, preparation-marker, or material label",
        "mathematical_form": "partial_A kappa_eff=partial_m kappa_eff=partial_source kappa_eff=0",
        "closes_component": "composition-dependent active gravitational source charge",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "source-current Ward universality plus kappa superselection",
        "fallback_if_missing": "R1 source charge and measured-GM residuals remain active",
    },
    {
        "contract_id": "GS4_no_range_radial_time_dependence",
        "required_identity": "kappa_eff has no radius, finite-range, clock-time, epoch, or local boundary dependence in the local branch",
        "mathematical_form": "partial_r kappa_eff=partial_lambda kappa_eff=partial_t kappa_eff=partial_boundary kappa_eff=0",
        "closes_component": "Gdot, radial G, Yukawa/range hair, preferred-location coupling",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "superselection/topological constant route plus boundary no-hair theorem",
        "fallback_if_missing": "execute Gdot, alpha(lambda), radial-source, and boundary residual bounds",
    },
    {
        "contract_id": "GS5_Bianchi_arbitrary_source_consistency",
        "required_identity": "Bianchi is used only in a same-frame, separately conserved, arbitrary-source branch or else grad kappa is retained as exchange",
        "mathematical_form": "if nabla T_obs=0 for arbitrary T_obs then nabla kappa_eff=0; otherwise q_loc includes kappa_eff^-1 P_loc[T_obs nabla kappa_eff]",
        "closes_component": "Bianchi overclaim and hidden exchange ambiguity",
        "affected_rows": "R0;R3;R4;R7;R9;R10;R11",
        "current_status": "conditional_only",
        "evidence_needed": "same-frame conservation theorem with all exchange owners absent, or explicit residual coefficient",
        "fallback_if_missing": "delta_kappa_source row remains in the exchange ledger",
    },
    {
        "contract_id": "GS6_constant_offset_policy",
        "required_identity": "a global constant offset in kappa_eff is calibration only unless the parent action predicts its absolute normalization",
        "mathematical_form": "delta kappa_eff/kappa_eff=constant_global with all derivatives zero",
        "closes_component": "false prediction of numerical G",
        "affected_rows": "R4;R9;R11",
        "current_status": "policy_written_not_parent_normalization",
        "evidence_needed": "absolute coupling normalization theorem if predicting G itself",
        "fallback_if_missing": "claim only derivative/source silence, not the numerical value of G",
    },
    {
        "contract_id": "GS7_scalar_branch_fallback",
        "required_identity": "if any dependence survives, it is promoted to an executable residual branch rather than hidden inside measured GM",
        "mathematical_form": "dln_Geff_dt, partial_A ln G_eff, partial_r ln G_eff, alpha(lambda), delta_kappa_source",
        "closes_component": "nothing; keeps falsifiable residuals visible",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "fallback_policy_only",
        "evidence_needed": "numeric coefficients, priors, and bound comparison for any nonzero branch",
        "fallback_if_missing": "no measured-GM, Newton, PPN, or local-GR claim",
    },
    {
        "contract_id": "GS8_evaluator_mapping",
        "required_identity": "failed GS rows activate the local residual evaluator and empirical locks",
        "mathematical_form": "GS failure -> residual_vector[R1,R4,R9,R10,R11] active",
        "closes_component": "silent loss of failed assumptions",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_yet_executable",
        "evidence_needed": "machine-readable mapping from GS0-GS7 to local-bound residual evaluator",
        "fallback_if_missing": "manual gate discipline required before any local-GR claim",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "typed_constant_in_action",
        "construction": "write kappa_eff as a symbol in S_EH but never state whether it is global, varied, or derived",
        "why_it_fails": "notation does not decide ontology; a typed constant can hide a local field assumption",
        "required_blocker": "configuration-factorization statement or topological zero-form derivation",
        "affected_contracts": "GS0;GS1;GS6",
    },
    {
        "counterexample": "bare_lambda_dk_constraint",
        "construction": "add Lambda^mu partial_mu kappa_eff only to force d kappa_eff=0",
        "why_it_fails": "without gauge/topological origin it is an inserted plateau axiom with possible unowned stress",
        "required_blocker": "motivated topological pair, boundary conditions, and Ward ledger ownership",
        "affected_contracts": "GS1;GS5",
    },
    {
        "counterexample": "kappa_of_memory",
        "construction": "kappa_eff=kappa0 F(Z_memory,I_Q,C_D)",
        "why_it_fails": "cosmological or memory success leaks into local Gdot/source normalization",
        "required_blocker": "trivial MTS action on K_global or local memory no-hair theorem",
        "affected_contracts": "GS2;GS4;GS7",
    },
    {
        "counterexample": "kappa_of_species",
        "construction": "kappa_A=kappa0(1+epsilon_A) or kappa_eff(A,m)",
        "why_it_fails": "composition-dependent active source coupling survives one observed coframe",
        "required_blocker": "source-current Ward universality plus species-blind kappa sector",
        "affected_contracts": "GS3;GS7",
    },
    {
        "counterexample": "kappa_of_range_or_radius",
        "construction": "G_eff(r,lambda)=G0[1+alpha exp(-r/lambda)]",
        "why_it_fails": "Newton inverse-square and local PPN limits gain fifth-force/radial-hair residuals",
        "required_blocker": "range/radial derivative theorem or executable alpha(lambda) bound",
        "affected_contracts": "GS4;GS7",
    },
    {
        "counterexample": "conformal_frame_kappa",
        "construction": "kappa_eff is constant in one frame but matter clocks and EH operator use different frames",
        "why_it_fails": "constant coupling can be a frame artefact rather than a measured-G statement",
        "required_blocker": "same observed coframe and source-normalization theorem",
        "affected_contracts": "GS0;GS5;GS6",
    },
    {
        "counterexample": "Bianchi_with_hidden_exchange",
        "construction": "use Bianchi to set grad kappa_eff=0 while non-EH, boundary, projector, or nonmetric exchange terms remain active",
        "why_it_fails": "Bianchi then owns exchange; it does not erase the exchange residual",
        "required_blocker": "all exchange owners theorem-zero or explicit residual mapping",
        "affected_contracts": "GS5;GS8",
    },
    {
        "counterexample": "constant_offset_value_claim",
        "construction": "treat kappa_eff=kappa0 constant as a prediction of the measured numerical value of G",
        "why_it_fails": "constant offset is calibration unless the parent fixes absolute normalization",
        "required_blocker": "absolute coupling normalization theorem",
        "affected_contracts": "GS6",
    },
]


GATE_TESTS = [
    {
        "gate": "contract_makes_global_status_explicit",
        "pass_condition": "kappa_eff global/superselection status is a named parent-action requirement",
        "current_result": "pass",
        "evidence": "GS0 and GS1 written",
    },
    {
        "gate": "topological_route_not_overclaimed",
        "pass_condition": "topological zero-form route is treated as possible future derivation, not current corpus result",
        "current_result": "pass",
        "evidence": "P1 status is promising_future_parent_route_not_in_corpus",
    },
    {
        "gate": "Bianchi_not_used_as_magic",
        "pass_condition": "Bianchi only kills grad kappa under arbitrary separately conserved same-frame matter stress",
        "current_result": "pass",
        "evidence": "GS5 and Bianchi_arbitrary_source_route",
    },
    {
        "gate": "constant_offset_not_prediction",
        "pass_condition": "constant kappa offset is calibration without absolute normalization",
        "current_result": "pass",
        "evidence": "GS6 written",
    },
    {
        "gate": "global_coupling_parent_derived",
        "pass_condition": "corpus derives why kappa_eff cannot be local or MTS-dependent",
        "current_result": "fail",
        "evidence": "P0/P1/P3 are not established in the parent corpus",
    },
    {
        "gate": "all_local_dependencies_forbidden",
        "pass_condition": "MTS, species, source, range, radius, time, and frame dependencies are theorem-forbidden",
        "current_result": "fail",
        "evidence": "GS2-GS4 remain not_parent_derived",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "constant coupling plus measured-GM plus PPN rows are theorem-zero or empirically scored",
        "current_result": "fail",
        "evidence": "this is a parent contract only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "exact global-coupling parent-action contract written",
        "status": "pass",
        "evidence": "GS0-GS8 define the required parent identities and fallbacks",
    },
    {
        "claim": "safe superselection route identified",
        "status": "pass_conditional",
        "evidence": "P0 is sufficient if explicitly adopted as a global sector premise",
    },
    {
        "claim": "possible derivation route identified",
        "status": "pass_conditional",
        "evidence": "P1 topological zero-form/integration-constant route could derive d kappa_eff=0 if built into the parent theory",
    },
    {
        "claim": "Bianchi route bounded",
        "status": "pass",
        "evidence": "Bianchi arbitrary-source branch is distinguished from hidden-exchange branch",
    },
    {
        "claim": "global kappa parent-derived from current MTS corpus",
        "status": "fail",
        "evidence": "no completed parent superselection or topological derivation exists in cited sources",
    },
    {
        "claim": "scalar/source residual branch eliminated",
        "status": "fail",
        "evidence": "if kappa_eff depends on MTS/source/range/frame data, R1/R4/R9/R10/R11 remain active",
    },
    {
        "claim": "Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "constant-coupling superselection contract only",
    },
]


DECISION = [
    {
        "decision": "The exact contract is now clear. MTS can keep a constant universal G_eff in the local branch if kappa_eff is an explicit global/superselection coupling, or if a future parent action derives it as a topological/integration constant with d kappa_eff=0 and no local matter/source/range/frame dependence. The current corpus does not yet derive either route. Therefore the honest status is conditional-superselection-or-closure: adopt kappa_eff as a global sector premise for the local GR branch, or keep scalar/source-normalization residuals active. This checkpoint does not promote measured-GM, Newton, PPN, or local GR.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "why_next": "constant coupling can be carried as a clean superselection premise while mass-flux closure still needs actual Pi_M projector algebra",
    },
    {
        "rank": 2,
        "target": "map GS0-GS8 into P8/R9/R10 residual evaluator",
        "why_next": "failed global-coupling identities should automatically activate Gdot/source/range/local-bound rows",
    },
    {
        "rank": 3,
        "target": "parent topological zero-form kappa route",
        "why_next": "if we want derivation rather than closure, this is the sharpest future path for d kappa_eff=0",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    csv_fieldnames = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    table_fieldnames = fieldnames or list(rows[0].keys())
    lines = [
        "| " + " | ".join(table_fieldnames) + " |",
        "| " + " | ".join(["---"] * len(table_fieldnames)) + " |",
    ]
    for item in rows:
        values = []
        for fieldname in table_fieldnames:
            value = str(item.get(fieldname, ""))
            value = value.replace("|", "/")
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
            "evidence": "global coupling superselection contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 5 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "parent_options_written",
            "status": "pass" if len(PARENT_OPTIONS) == 6 else "fail",
            "evidence": f"{len(PARENT_OPTIONS)} parent options",
        },
        {
            "gate": "counterexamples_written",
            "status": "pass" if len(COUNTEREXAMPLES) == 8 else "fail",
            "evidence": f"{len(COUNTEREXAMPLES)} counterexamples",
        },
        {
            "gate": "contract_written",
            "status": "pass" if len(CONTRACT) == 9 else "fail",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "Bianchi_not_used_as_magic",
            "status": "pass",
            "evidence": "same-frame arbitrary-source route separated from retained exchange route",
        },
        {
            "gate": "constant_offset_not_prediction",
            "status": "pass",
            "evidence": "GS6 calibration policy recorded",
        },
        {
            "gate": "scalar_branch_retained",
            "status": "pass",
            "evidence": "P5 and GS7 retain kappa_eff local-dependence fallback",
        },
        {
            "gate": "global_coupling_parent_derived",
            "status": "fail",
            "evidence": "no completed parent superselection/topological derivation exists in cited sources",
        },
        {
            "gate": "MTS_invariant_dependence_forbidden",
            "status": "fail",
            "evidence": "GS2 remains not_parent_derived",
        },
        {
            "gate": "species_source_blind_kappa_derived",
            "status": "fail",
            "evidence": "GS3 remains not_parent_derived",
        },
        {
            "gate": "range_radial_time_running_zero",
            "status": "fail",
            "evidence": "GS4 remains not_parent_derived",
        },
        {
            "gate": "residual_evaluator_mapping_executable",
            "status": "fail",
            "evidence": "GS8 mapping is contract-only",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "global-coupling contract only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "P8 and PPN rows remain retained",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 453 - Global Coupling Superselection Parent Action Contract

Private P8/R4/R9/R10/R11 coupling checkpoint. This is not a public Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 452 showed that `G_eff=kappa_eff c^4/(8 pi)` is harmless only if `kappa_eff` is constant and universal.

This checkpoint writes the exact parent-action contract needed to make `kappa_eff` a true global/superselection coupling rather than a local MTS scalar hidden inside source normalization.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/global_coupling_superselection_parent_action_contract.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Parent Options

{markdown_table(PARENT_OPTIONS)}

## 6. Superselection Contract

The global-coupling superselection contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 7. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 8. Gate Tests

{markdown_table(GATE_TESTS)}

## 9. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 10. Gate Results

{markdown_table(gate_results)}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is not grim, but it is not magic either. The clean boxing-footwork version is to carry `kappa_eff` as a declared global sector label for the local GR branch, while refusing to claim the numerical value of `G`. The more ambitious derivation route is a topological zero-form/integration-constant parent sector. If neither is adopted, then `kappa_eff` is a local scalar/source-normalization residual and the local GR branch does not pass yet.

## 12. Next Queue

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
    write_csv(results_dir / "parent_options.csv", PARENT_OPTIONS)
    write_csv(results_dir / "global_coupling_contract.csv", CONTRACT, CONTRACT_COLUMNS)
    write_csv(results_dir / "counterexamples.csv", COUNTEREXAMPLES)
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
        "conditional_superselection_contract_written": True,
        "topological_zero_form_route_identified": True,
        "Bianchi_not_used_as_magic": True,
        "constant_offset_not_prediction": True,
        "scalar_branch_retained": True,
        "global_coupling_parent_derived": False,
        "MTS_invariant_dependence_forbidden": False,
        "species_source_blind_kappa_derived": False,
        "range_radial_time_running_zero": False,
        "residual_evaluator_mapping_executable": False,
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
    parser = argparse.ArgumentParser(description="Write the MTS global coupling superselection parent-action contract.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-164500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
