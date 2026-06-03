from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "EH-only-exterior-parent-premise-ladder"
CHECKPOINT_DOC = "439-EH-only-exterior-parent-premise-ladder.md"
STATUS = "EH_only_exterior_parent_premise_ladder_written_Lovelock_route_exact_parent_premises_open_no_EH_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "EH_only_parent_premise_ladder_only_no_EH_Newton_PPN_fifth_force_or_local_GR_pass"
NEXT_TARGET = "440-metric-only-second-order-sector-reduction-attempt.md"


SOURCE_DOCS = [
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "original EH sufficiency stack: Ward closure plus no-hair plus metric-only second-order exterior",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "operator-or-residual fork and coefficient-to-observable map",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action blocks and required variation identities",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "same-frame identity does not imply EH; Lovelock-style route retained",
    },
    {
        "path": "396-local-GR-reduction-sufficiency-stack-audit.md",
        "role": "local-GR sufficiency stack and promotion gates",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source theorem pair and Newtonian measured-GM obstruction",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "G0-G13 local GR/Newton stack partition",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "conditional EH-to-Poisson bridge and no-promotion policy",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "hidden-variable Euler ledger and retained R11 channels",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 executable operator-vector contract and next target",
    },
    {
        "path": "runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/EH_sufficiency_assumptions.csv",
        "role": "machine-readable EH sufficiency assumptions",
    },
    {
        "path": "runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/operator_basis_audit.csv",
        "role": "operator basis audit showing conserved non-EH families",
    },
    {
        "path": "runs/20260601-235000-EH-exterior-operator-or-residual-modified-gravity-ledger/results/operator_basis_residual_ledger.csv",
        "role": "residual operator family ledger",
    },
    {
        "path": "runs/20260602-010500-parent-local-action-minimal-contract/results/local_GR_sufficiency_stack.csv",
        "role": "parent-action local-GR sufficiency stack",
    },
    {
        "path": "runs/20260602-034500-parent-action-contract-v2-after-identity-stack/results/required_variation_identities_v2.csv",
        "role": "variation identities required after identity-branch cleanup",
    },
    {
        "path": "runs/20260602-050500-same-frame-EH-source-derived-stack-audit/results/gate_results.csv",
        "role": "derived-stack audit showing no physics rung parent-derived enough for promotion",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/operator_families.csv",
        "role": "current canonical R11 operator-family vector basis",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/theorem_zero_routes.csv",
        "role": "current R11 theorem-zero route table",
    },
]


EH_ONLY_PREMISE_LADDER = [
    {
        "rung": "P0_compact_ordinary_exterior",
        "required_parent_statement": "ordinary local test region has compact matter support and a well-defined exterior domain",
        "mathematical_form": "rho_matter=0 in E_ext except calibrated conserved monopole/boundary data",
        "current_status": "definition_plus_source_conditions_open",
        "if_failed": "radial source hair, boundary charge, or fifth-force/source-normalization residuals remain",
    },
    {
        "rung": "P1_parent_selected_observed_frame",
        "required_parent_statement": "one observed metric/coframe is selected by the parent action for matter, photons, clocks, rods, and the metric core",
        "mathematical_form": "S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A] with e not a post-readout relabel",
        "current_status": "closure_branch_not_parent_derived",
        "if_failed": "WEP, clock, nonmetric light, and frame-pullback residuals remain",
    },
    {
        "rung": "P2_full_Ward_Euler_ownership",
        "required_parent_statement": "all hidden/projector/domain/boundary/source variables are varied and on shell, pure gauge/topological, harmless, or retained",
        "mathematical_form": "nabla_mu T_total^{mu nu}+sum_A E_A nabla^nu Z_A+F_boundary^nu+F_domain^nu=0",
        "current_status": "mapped_not_closed",
        "if_failed": "q_loc, alpha3, Gdot, source, fifth-force, and operator rows remain retained",
    },
    {
        "rung": "P3_no_extra_local_propagating_fields",
        "required_parent_statement": "scalar, vector, bulk-X, projector/domain, torsion, nonmetricity, and nonlocal kernels are absent, gauge, topological, no-haired, or residualized",
        "mathematical_form": "Phi_extra={phi,V_mu,X,P_D,chi_D,T,Q,K_nonlocal}=0/gauge/topological in E_ext",
        "current_status": "not_derived",
        "if_failed": "R11 coefficient vector and induced R3-R10 residuals required",
    },
    {
        "rung": "P4_metric_compatibility_connection",
        "required_parent_statement": "the local observed connection is Levi-Civita and universally used by matter/light/spin",
        "mathematical_form": "nabla_mu g_{alpha beta}=0 and T^alpha_{mu nu}=0 in the observed local branch",
        "current_status": "not_parent_derived",
        "if_failed": "torsion/nonmetricity WEP, clock, spin, and light-cone channels remain",
    },
    {
        "rung": "P5_local_4D_diffeomorphic_metric_action",
        "required_parent_statement": "the surviving exterior bulk action is local, four-dimensional, diffeomorphism invariant, and built only from the observed metric/coframe",
        "mathematical_form": "S_ext=int_E d^4x sqrt(-g) L(g,Riemann,nabla Riemann,...) + boundary",
        "current_status": "structural_target_not_parent_derived",
        "if_failed": "nonlocal/memory, extra-dimensional, fixed-background, or domain operators remain in R11",
    },
    {
        "rung": "P6_second_order_metric_equations",
        "required_parent_statement": "the surviving local metric equations are at most second order through local tested scales",
        "mathematical_form": "E_ext^{mu nu}=E_ext^{mu nu}(g,partial g,partial^2 g), no independent higher-derivative propagating modes",
        "current_status": "central_blocker_not_derived",
        "if_failed": "R2/f(R), Ricci/Weyl squared, and nonlocal operators remain legal",
    },
    {
        "rung": "P7_boundary_topological_harmlessness",
        "required_parent_statement": "boundary and class terms are pure boundary/topological or Ward-owned with no local stress, shear, flux, radial hair, or preferred-location leakage",
        "mathematical_form": "delta S_boundary -> boundary terms only; T_boundary^{mu nu}|_local=0 or constant universal monopole",
        "current_status": "conditional_not_derived",
        "if_failed": "gamma, beta, alpha3, xi, Gdot, and boundary/operator coefficients remain retained",
    },
    {
        "rung": "P8_constant_source_normalization",
        "required_parent_statement": "kappa, G_eff, M_eff, and measured GM are constant, conserved, universal, and range independent",
        "mathematical_form": "mu_obs=G_eff M_eff, partial_{t,r,A,lambda} mu_obs=0, mu_extra=0",
        "current_status": "conditional_not_parent_derived",
        "if_failed": "Newtonian source, beta, WEP-source, Gdot, and fifth-force rows remain",
    },
    {
        "rung": "P9_weak_field_PPN_completion",
        "required_parent_statement": "the EH/source branch is solved through second post-Newtonian order in the observed matter frame",
        "mathematical_form": "gamma=1, beta=1, alpha1=alpha2=alpha3=xi=0 plus metric redshift/WEP in same frame",
        "current_status": "not_promoted",
        "if_failed": "local GR and Newtonian reduction remain unclaimed even if first-order Poisson algebra is clean",
    },
]


PARENT_VARIATION_TESTS = [
    {
        "test_id": "V0_metric_variation",
        "variation_or_identity": "delta S_parent/delta g_{mu nu}",
        "must_show": "E_ext^{mu nu}=a G^{mu nu}+b g^{mu nu} plus only theorem-zero or retained H_i^{mu nu}",
        "rungs_controlled": "P3;P5;P6;P7;P9",
        "current_status": "not_satisfied",
    },
    {
        "test_id": "V1_matter_frame_variation",
        "variation_or_identity": "delta S_matter/delta Z_I at fixed observed e",
        "must_show": "no direct MTS matter vertices, no species spurions, and one observed coframe selected before readout",
        "rungs_controlled": "P1;P4;P9",
        "current_status": "closure_only",
    },
    {
        "test_id": "V2_hidden_Euler_equations",
        "variation_or_identity": "E_A=delta S_parent/delta Z_A for all hidden/projector/domain/source variables",
        "must_show": "E_A=0 locally or Z_A pure gauge/topological/harmless; otherwise residual rows are emitted",
        "rungs_controlled": "P2;P3;P7",
        "current_status": "ledger_written_not_closed",
    },
    {
        "test_id": "V3_connection_variation",
        "variation_or_identity": "delta S_parent/delta Gamma or spin connection",
        "must_show": "Levi-Civita compatibility and zero torsion/nonmetricity in observed branch",
        "rungs_controlled": "P4",
        "current_status": "not_parent_derived",
    },
    {
        "test_id": "V4_boundary_variation",
        "variation_or_identity": "delta S_boundary/delta boundary data",
        "must_show": "boundary terms are topological/class-only/Ward-owned with no local hair",
        "rungs_controlled": "P0;P7",
        "current_status": "conditional_open",
    },
    {
        "test_id": "V5_source_normalization_variation",
        "variation_or_identity": "delta S_source_norm/delta{kappa,G_eff,M_eff,Pi_M J}",
        "must_show": "constant universal measured-GM with mu_extra=0 and no range/time/species leakage",
        "rungs_controlled": "P0;P8;P9",
        "current_status": "conditional_open",
    },
    {
        "test_id": "V6_second_order_restriction",
        "variation_or_identity": "parent symmetry/regularity/low-energy theorem forbids higher derivatives as local propagating equations",
        "must_show": "R2/f(R)/Ricci^2/Weyl^2/nonlocal kernels are zero, topological, decoupled, or coefficient-mapped",
        "rungs_controlled": "P5;P6;R11",
        "current_status": "central_open",
    },
]


LOVELOCK_SELECTION_CONTRACT = [
    {
        "stage": 1,
        "statement": "Assume P1-P7 hold in the compact ordinary exterior.",
        "mathematical_form": "one observed metric, local 4D diffeo invariant metric-only second-order bulk equations",
        "status": "conditional_premises_not_parent_derived",
    },
    {
        "stage": 2,
        "statement": "The only local symmetric divergence-free rank-2 metric tensor with up-to-second derivatives in 4D is EH plus Lambda, up to boundary/topological pieces.",
        "mathematical_form": "E_ext^{mu nu}=a G^{mu nu}+b g^{mu nu}",
        "status": "conditional_theorem_shape",
    },
    {
        "stage": 3,
        "statement": "If a is constant and source-normalized, identify kappa_eff=1/a and Lambda_eff=-b/a.",
        "mathematical_form": "G^{mu nu}+Lambda_eff g^{mu nu}=kappa_eff T^{mu nu}",
        "status": "requires_P8",
    },
    {
        "stage": 4,
        "statement": "If Lambda_eff is negligible on local PPN scales and measured GM is constant/universal, recover Newtonian Poisson and GR PPN baseline.",
        "mathematical_form": "nabla^2 Phi=4 pi G_measured rho; gamma=beta=1; alpha_i=xi=0",
        "status": "requires_P8_P9",
    },
    {
        "stage": 5,
        "statement": "If any premise fails, EH is not derived; the failed premise emits retained residuals or R11 coefficient-vector rows.",
        "mathematical_form": "E_ext^{mu nu}=aG^{mu nu}+bg^{mu nu}+sum_i c_i H_i^{mu nu}",
        "status": "current_branch_policy",
    },
]


DEPENDENCY_EDGES = [
    {"from": "P1_parent_selected_observed_frame", "to": "R0/R2/WEP_clock_same_frame", "edge": "without one frame, local observables are not GR-comparable"},
    {"from": "P2_full_Ward_Euler_ownership", "to": "R7/R9/source_flux_rows", "edge": "unowned hidden Euler terms source q_loc and flux residuals"},
    {"from": "P3_no_extra_local_propagating_fields", "to": "R11_operator_vector", "edge": "extra fields are non-EH operator families unless theorem-zero"},
    {"from": "P4_metric_compatibility_connection", "to": "R0/R1/R2/R11", "edge": "torsion/nonmetricity affects WEP, clocks, light, spin, and operator ledger"},
    {"from": "P5_local_4D_diffeomorphic_metric_action", "to": "Lovelock_selection", "edge": "EH selection requires local 4D diffeo metric action"},
    {"from": "P6_second_order_metric_equations", "to": "R2_fR_Ricci_Weyl_rows", "edge": "higher derivatives are legal non-EH operators if not forbidden"},
    {"from": "P7_boundary_topological_harmlessness", "to": "R3/R4/R7/R8", "edge": "boundary hair contaminates gamma, beta, alpha3, and xi"},
    {"from": "P8_constant_source_normalization", "to": "Newtonian_measured_GM", "edge": "EH equation alone is not measured Newtonian gravity"},
    {"from": "P9_weak_field_PPN_completion", "to": "local_GR_claim", "edge": "first-order Poisson is not a full PPN/local-GR reduction"},
]


FAKE_EH_SHORTCUTS = [
    {
        "shortcut": "same_frame_matter_implies_EH",
        "why_rejected": "a scalar-tensor, f(R), vector, or nonlocal gravity branch can share one matter frame",
        "correct_route": "derive separate EH operator-selection premises P3-P6",
    },
    {
        "shortcut": "Bianchi_or_Ward_conservation_implies_EH",
        "why_rejected": "conserved non-EH tensors exist",
        "correct_route": "derive metric-only local 4D second-order exterior or retain c_i H_i^{mu nu}",
    },
    {
        "shortcut": "first_order_Poisson_implies_GR",
        "why_rejected": "gamma, beta, preferred-frame, source-normalization, and fifth-force rows can still fail",
        "correct_route": "solve weak-field expansion through PPN order in the observed frame",
    },
    {
        "shortcut": "set_all_nonEH_coefficients_to_zero",
        "why_rejected": "typed zeros are placeholders unless parent-derived or sourced",
        "correct_route": "supply derived_zero sources or a valid R11 coefficient vector",
    },
    {
        "shortcut": "boundary_terms_are_harmless_by_name",
        "why_rejected": "boundary/class terms can leave radial, shear, flux, and preferred-location hair",
        "correct_route": "prove class-only topological/Ward-owned boundary no-hair",
    },
    {
        "shortcut": "EFT_small_means_local_GR",
        "why_rejected": "suppressed coefficients may be empirically viable but are not theorem-zero GR reduction",
        "correct_route": "declare units/cutoff, map residuals, and score as retained modified-gravity branch",
    },
    {
        "shortcut": "field_redefinition_hides_nonEH_sector",
        "why_rejected": "renaming the metric can move residues into source, matter, or operator sectors",
        "correct_route": "show the whole parent action is EH-only in the observed frame",
    },
]


ROW_IMPLICATIONS = [
    {"row_id": "R0_identity_coframe_direct", "ladder_dependency": "P1;P4", "current_transition": "closure_control_only_not_parent_derived"},
    {"row_id": "R1_WEP_source_charge", "ladder_dependency": "P1;P4;P8", "current_transition": "source_charge_retained"},
    {"row_id": "R2_clock_redshift", "ladder_dependency": "P1;P4;P8;P9", "current_transition": "same_frame_clock_budget_not_promoted"},
    {"row_id": "R3_gamma", "ladder_dependency": "P3;P5;P6;P7;P9", "current_transition": "EH_operator_slip_retained"},
    {"row_id": "R4_beta", "ladder_dependency": "P3;P6;P7;P8;P9", "current_transition": "source_and_nonlinear_operator_retained"},
    {"row_id": "R5_alpha1", "ladder_dependency": "P2;P3;P9", "current_transition": "preferred_frame_vector_retained"},
    {"row_id": "R6_alpha2", "ladder_dependency": "P2;P3;P9", "current_transition": "preferred_frame_vector_retained"},
    {"row_id": "R7_alpha3", "ladder_dependency": "P2;P7;P9", "current_transition": "Ward_flux_contingent_retained"},
    {"row_id": "R8_xi", "ladder_dependency": "P3;P6;P7;P9", "current_transition": "domain_boundary_location_retained"},
    {"row_id": "R9_Gdot", "ladder_dependency": "P2;P7;P8", "current_transition": "source_memory_drift_retained"},
    {"row_id": "R10_fifth_force", "ladder_dependency": "P0;P3;P7;P8", "current_transition": "R10_curve_or_theorem_zero_required"},
    {"row_id": "R11_EH_operator_ledger", "ladder_dependency": "P3;P4;P5;P6;P7;P8", "current_transition": "R11_vector_or_EH_only_theorem_required"},
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "EH-only parent-premise ladder written",
        "status": "pass",
        "evidence": "10 rungs P0-P9 with variation tests and dependencies recorded",
    },
    {
        "claim": "Lovelock-style conditional route identified",
        "status": "pass_conditional",
        "evidence": "P1-P7 would select EH plus Lambda up to harmless boundary/topological terms",
    },
    {
        "claim": "same-frame matter parent-selected",
        "status": "fail",
        "evidence": "identity/coframe row is closure-labelled, not parent-derived",
    },
    {
        "claim": "all hidden sectors varied and locally on shell/harmless",
        "status": "fail",
        "evidence": "C1 Euler ledger remains open for projector/domain/boundary/source/nonEH rows",
    },
    {
        "claim": "metric-only exterior variables derived",
        "status": "fail",
        "evidence": "scalar, vector, bulk, projector/domain, torsion/nonmetricity, and nonlocal sectors are retained",
    },
    {
        "claim": "local 4D second-order metric operator derived",
        "status": "fail",
        "evidence": "R2/f(R), Ricci/Weyl squared, and nonlocal operators are not parent-forbidden",
    },
    {
        "claim": "source-normalized Newtonian measured-GM derived",
        "status": "fail",
        "evidence": "kappa/G_eff/M_eff/mu_extra constancy remains conditional",
    },
    {
        "claim": "PPN/local-GR promoted",
        "status": "fail",
        "evidence": "R0-R11 still include closure, retained, contingent, unscored, and symbolic rows",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "EH_only_premise_ladder_written",
        "status": "pass",
        "evidence": "P0-P9 parent-premise ladder recorded",
    },
    {
        "gate": "parent_variation_tests_written",
        "status": "pass",
        "evidence": "7 parent variation tests recorded",
    },
    {
        "gate": "Lovelock_selection_contract_written",
        "status": "pass",
        "evidence": "5-stage conditional EH selection route recorded",
    },
    {
        "gate": "fake_EH_shortcuts_rejected",
        "status": "pass",
        "evidence": "7 common false shortcuts explicitly rejected",
    },
    {
        "gate": "row_implications_written",
        "status": "pass",
        "evidence": "R0-R11 dependencies mapped to ladder rungs",
    },
    {
        "gate": "EH_only_parent_derived",
        "status": "fail",
        "evidence": "central P1-P8 rungs remain closure, conditional, retained, or open",
    },
    {
        "gate": "R11_theorem_zero_promoted",
        "status": "fail",
        "evidence": "R11 still requires EH-only theorem-zero or executable coefficient vector",
    },
    {
        "gate": "Newtonian_reduction_promoted",
        "status": "fail",
        "evidence": "source-normalized measured-GM remains conditional",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "premise ladder only; no EH/Newton/PPN/fifth-force/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The EH-only exterior route is now an explicit parent-premise ladder. If the parent action derives one observed frame, full Ward/Euler ownership, no extra local propagating fields, Levi-Civita compatibility, a local 4D diffeomorphic metric-only exterior, second-order metric equations, harmless boundary/topological terms, and constant source normalization, then the Lovelock-style route selects EH plus Lambda and the weak-field GR/Newton baseline follows conditionally. The current corpus does not derive those rungs. Therefore this checkpoint sharpens the route but does not promote EH, Newton, PPN, R11, or local GR.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "440-metric-only-second-order-sector-reduction-attempt.md",
        "why_next": "P3 and P6 are the central EH blockers: either reduce all extra sectors to gauge/topological/no-hair, or retain R11 coefficients",
    },
    {
        "rank": 2,
        "target": "filled R11 nonEH operator vector",
        "why_next": "if P3/P6 cannot be derived, the branch must become an executable modified-gravity coefficient vector",
    },
    {
        "rank": 3,
        "target": "local residual scorer curve/vector mode",
        "why_next": "R10/R11 templates are now written; scorer should eventually parse real curve/vector files",
    },
]


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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    return [source_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 439 - EH-Only Exterior Parent-Premise Ladder

Private EH/local-GR derivation checkpoint. This is not a public Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, cosmology, local-GR, or unified-field claim.

## 1. Purpose

Checkpoints 437 and 438 made the symbolic R10/R11 gates executable. This checkpoint turns the theorem-zero side of R11 into a precise parent-premise ladder. The question is no longer "can we say EH locally?" The question is:

```text
Exactly which parent-derived rungs force the surviving compact local exterior
to be Einstein-Hilbert plus Lambda, and which residual rows stay alive if a rung fails?
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/EH_only_exterior_parent_premise_ladder.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. EH-Only Premise Ladder

{markdown_table(EH_ONLY_PREMISE_LADDER, ["rung", "required_parent_statement", "mathematical_form", "current_status", "if_failed"])}

## 5. Parent Variation Tests

{markdown_table(PARENT_VARIATION_TESTS, ["test_id", "variation_or_identity", "must_show", "rungs_controlled", "current_status"])}

## 6. Lovelock Selection Contract

{markdown_table(LOVELOCK_SELECTION_CONTRACT, ["stage", "statement", "mathematical_form", "status"])}

Compact theorem shape:

```text
If the parent action derives P1-P7 in the compact ordinary exterior,
then the surviving local bulk equation has the form

  E_ext^{{mu nu}} = a G^{{mu nu}} + b g^{{mu nu}}.

If P8 also holds, this becomes

  G^{{mu nu}} + Lambda_eff g^{{mu nu}} = kappa_eff T^{{mu nu}}

in the observed matter frame. If P9 is solved, the local Newton/PPN
baseline follows. If any rung fails, the failed rung emits retained
R0-R11 residuals rather than a GR claim.
```

## 7. Dependency Edges

{markdown_table(DEPENDENCY_EDGES, ["from", "to", "edge"])}

## 8. Rejected EH Shortcuts

{markdown_table(FAKE_EH_SHORTCUTS, ["shortcut", "why_rejected", "correct_route"])}

## 9. Row Implications

{markdown_table(ROW_IMPLICATIONS, ["row_id", "ladder_dependency", "current_transition"])}

## 10. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 11. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is the GR route with the referee holding the scorecard. If the rungs close, EH follows cleanly. If they do not, MTS is not dead; it is a retained residual/modified-gravity branch that must fight on the measured rows. No shortcut gets to wear the belt.

## 13. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "EH_only_premise_ladder.csv", EH_ONLY_PREMISE_LADDER)
    write_csv(results_dir / "parent_variation_tests.csv", PARENT_VARIATION_TESTS)
    write_csv(results_dir / "Lovelock_selection_contract.csv", LOVELOCK_SELECTION_CONTRACT)
    write_csv(results_dir / "dependency_edges.csv", DEPENDENCY_EDGES)
    write_csv(results_dir / "fake_EH_shortcuts.csv", FAKE_EH_SHORTCUTS)
    write_csv(results_dir / "row_implications.csv", ROW_IMPLICATIONS)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "EH_only_premise_rungs": len(EH_ONLY_PREMISE_LADDER),
        "parent_variation_tests": len(PARENT_VARIATION_TESTS),
        "Lovelock_selection_stages": len(LOVELOCK_SELECTION_CONTRACT),
        "dependency_edges": len(DEPENDENCY_EDGES),
        "fake_EH_shortcuts_rejected": len(FAKE_EH_SHORTCUTS),
        "row_implications": len(ROW_IMPLICATIONS),
        "EH_only_parent_derived": False,
        "R11_theorem_zero_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 439 EH-only exterior parent-premise ladder artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
