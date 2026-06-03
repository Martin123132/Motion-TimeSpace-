from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "metric-only-second-order-sector-reduction-attempt"
CHECKPOINT_DOC = "440-metric-only-second-order-sector-reduction-attempt.md"
STATUS = "metric_only_second_order_sector_reduction_attempt_written_reduction_conditions_sharp_extra_sectors_retained_no_EH_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "metric_only_second_order_sector_reduction_attempt_only_no_EH_Newton_PPN_R10_R11_or_local_GR_pass"
NEXT_TARGET = "441-extra-sector-nohair-priority-gate.md"


SOURCE_DOCS = [
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH sufficiency theorem and operator obstruction ledger",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "operator-or-residual fork and coefficient-to-observable map",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action blocks and variation identities",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "identity branch does not derive EH; non-EH ledger retained",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux no-hair and local residual locks",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "canonical EH-operator retained ledger and source-normalization test plan",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "hidden auxiliary/projector/domain Euler ledger",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 coefficient-vector contract",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "P3/P6 central EH blockers and next target",
    },
    {
        "path": "runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/operator_basis_audit.csv",
        "role": "machine-readable operator basis audit",
    },
    {
        "path": "runs/20260601-235000-EH-exterior-operator-or-residual-modified-gravity-ledger/results/operator_basis_residual_ledger.csv",
        "role": "residual operator family ledger",
    },
    {
        "path": "runs/20260602-010500-parent-local-action-minimal-contract/results/action_blocks.csv",
        "role": "minimal parent action sectors that cannot be hidden",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/EH_operator_retained_ledger.csv",
        "role": "retained operator families and affected rows",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "A0-A9 hidden-variable rows and R11 linkage",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/operator_families.csv",
        "role": "canonical R11 operator-family vector basis",
    },
    {
        "path": "runs/20260602-131500-EH-only-exterior-parent-premise-ladder/results/EH_only_premise_ladder.csv",
        "role": "P0-P9 parent-premise ladder",
    },
    {
        "path": "runs/20260602-131500-EH-only-exterior-parent-premise-ladder/results/parent_variation_tests.csv",
        "role": "parent variation tests for EH-only theorem route",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "fallback executable R11 vector template",
    },
]


REDUCTION_THEOREM_CHAIN = [
    {
        "step": 1,
        "claim": "Start from the full parent exterior action, not from the already-reduced metric equation.",
        "mathematical_form": "S_ext[g,Z_A]=S_metric[g]+sum_A S_A[g,Z_A]+S_boundary[g,Z_A]",
        "status": "required",
        "meaning": "metric-only cannot be assumed before varying the extra sectors",
    },
    {
        "step": 2,
        "claim": "Vary every extra sector before eliminating it.",
        "mathematical_form": "E_A := delta S_ext/delta Z_A = 0",
        "status": "ledger_available_not_solved",
        "meaning": "dropping a field without its Euler equation is a fake reduction",
    },
    {
        "step": 3,
        "claim": "A sector is removable only if its solution is absent, gauge/topological, algebraically harmless, or source-free no-haired.",
        "mathematical_form": "Z_A -> Z_A^*[g] with delta_g S_A[g,Z_A^*] = 0, boundary/topological, or retained",
        "status": "conditional_theorem_shape",
        "meaning": "solving E_A=0 is not enough if stress, preferred frame, source charge, or nonlocal memory remains",
    },
    {
        "step": 4,
        "claim": "Substituting a solved sector must not generate higher-derivative, nonlocal, or source-normalization operators.",
        "mathematical_form": "S_eff[g]=S_metric[g]+Delta S_A[g] must satisfy local second-order filter",
        "status": "central_open",
        "meaning": "integrating out a field can create f(R), R^2, Yukawa, or nonlocal terms",
    },
    {
        "step": 5,
        "claim": "After all extra sectors are removed or retained, apply the metric operator filter.",
        "mathematical_form": "E_eff^{mu nu}=a G^{mu nu}+b g^{mu nu}+sum_i c_i H_i^{mu nu}",
        "status": "operator_filter_written",
        "meaning": "EH follows only when every c_i is theorem-zero or harmless boundary/topological",
    },
    {
        "step": 6,
        "claim": "If any sector or operator coefficient remains, the branch is not metric-only EH; it is R11-retained.",
        "mathematical_form": "c_i != 0 or unmapped => R11 operator vector plus induced R rows",
        "status": "current_policy",
        "meaning": "modified-gravity viability can still be tested, but it is not derived local GR",
    },
]


LEGAL_ELIMINATION_MODES = [
    {
        "mode": "absent_by_parent_symmetry",
        "required_evidence": "configuration space or symmetry excludes the sector before variation",
        "valid_result": "no field, no Euler equation, no stress, no source charge",
        "current_availability": "not_shown_for_all_extra_sectors",
    },
    {
        "mode": "pure_gauge_or_topological",
        "required_evidence": "first-class constraint/topological invariant with no local stress or observable charge",
        "valid_result": "sector carries no local degrees of freedom or PPN/fifth-force effect",
        "current_availability": "conditional_for_some_projector_boundary_ideas",
    },
    {
        "mode": "algebraic_harmless_constraint",
        "required_evidence": "E_A=0 gives local algebraic solution whose metric variation is zero or constant universal calibration",
        "valid_result": "no higher derivatives, no nonlocal memory, no species/range/time dependence",
        "current_availability": "not_derived",
    },
    {
        "mode": "positive_source_free_nohair",
        "required_evidence": "positive elliptic/massive local operator, source-free exterior, regular boundary data, decaying solution",
        "valid_result": "field vanishes or is harmless constant in compact ordinary exterior",
        "current_availability": "contract_written_for_bulk_X_not_parent_derived",
    },
    {
        "mode": "retained_R11_vector",
        "required_evidence": "coefficient, units, normalization, weak-field map, affected rows, source path",
        "valid_result": "empirical modified-gravity branch, not theorem-zero GR",
        "current_availability": "template_written_not_filled",
    },
]


SECTOR_REDUCTION_MATRIX = [
    {
        "sector": "observed_metric_core",
        "parent_variable": "g_munu or e^a_mu",
        "reduction_target": "kept as the only local propagating exterior field",
        "legal_zero_or_safe_route": "EH_plus_Lambda baseline after P1-P9 close",
        "current_status": "target_not_derived",
        "if_not_reduced_rows": "R3;R4;R11",
        "next_action": "derive metric-only local 4D second-order operator or retain R11",
    },
    {
        "sector": "scalar_class_metric",
        "parent_variable": "phi, C, class metric, quotient scalar",
        "reduction_target": "absent, constant universal, gauge/topological, or algebraically harmless",
        "legal_zero_or_safe_route": "no local scalar stress, no matter/source charge, no f(R)-like effective operator",
        "current_status": "retained_not_reduced",
        "if_not_reduced_rows": "R2;R3;R4;R9;R10;R11",
        "next_action": "prove local scalar/class invariant algebra trivial or supply coefficient/vector map",
    },
    {
        "sector": "vector_preferred_frame",
        "parent_variable": "V_mu, n_mu, domain normal, coframe-vector marker",
        "reduction_target": "absent, pure gauge, dynamically aligned without stress, or coefficient-mapped",
        "legal_zero_or_safe_route": "no independent timelike/spacelike vector survives in observed local exterior",
        "current_status": "retained_not_reduced",
        "if_not_reduced_rows": "R5;R6;R7;R8;R11",
        "next_action": "derive vector/domain no-hair or fill preferred-frame coefficient rows",
    },
    {
        "sector": "projector_domain_stress",
        "parent_variable": "P_D, chi_D, lambda_P, L_cg, P_read/P_active",
        "reduction_target": "topological/metric-independent projector or readout-after-variation only",
        "legal_zero_or_safe_route": "projector/domain stress is zero, pure boundary/topological, or retained explicitly",
        "current_status": "retained_symbolic",
        "if_not_reduced_rows": "R5;R6;R7;R8;R9;R10;R11",
        "next_action": "derive covariant first-class projector algebra or retain stress vector",
    },
    {
        "sector": "bulk_X_memory_load",
        "parent_variable": "X_A, memory/load fields, bulk auxiliaries",
        "reduction_target": "positive source-free no-hair or executable alpha_X(lambda_X)",
        "legal_zero_or_safe_route": "(-Delta+m_X^2)X=0 with m_X^2>0 and source-free exterior, or R10/R11 map",
        "current_status": "operator_and_sources_not_parent_derived",
        "if_not_reduced_rows": "R1;R3;R4;R9;R10;R11",
        "next_action": "derive source-free positive operator or fill R10/R11 maps",
    },
    {
        "sector": "boundary_class_terms",
        "parent_variable": "Y_boundary, B_TF, B_0i, B_rad, boundary class data",
        "reduction_target": "pure boundary/topological or Ward-owned harmless boundary data",
        "legal_zero_or_safe_route": "no local shear, vector, radial, flux, or preferred-location hair",
        "current_status": "conditional_open",
        "if_not_reduced_rows": "R3;R4;R7;R8;R9;R11",
        "next_action": "derive class-only topological boundary no-hair or retain boundary coefficients",
    },
    {
        "sector": "torsion_nonmetricity_connection",
        "parent_variable": "Gamma, omega, torsion T, nonmetricity Q",
        "reduction_target": "Levi-Civita compatibility in observed branch",
        "legal_zero_or_safe_route": "delta_Gamma S gives T=0 and nabla g=0 with universal matter/light/spin coupling",
        "current_status": "not_parent_derived",
        "if_not_reduced_rows": "R0;R1;R2;R11",
        "next_action": "derive connection compatibility or retain torsion/nonmetricity operator rows",
    },
    {
        "sector": "higher_curvature_metric_operators",
        "parent_variable": "R^2, f(R), Ricci^2, Weyl^2 coefficients",
        "reduction_target": "zero, topological boundary combination, decoupled infinite mass, or coefficient-mapped",
        "legal_zero_or_safe_route": "parent forbids higher derivative propagating modes through local tested scales",
        "current_status": "central_open",
        "if_not_reduced_rows": "R3;R4;R8;R10;R11",
        "next_action": "derive second-order restriction or use R11 vector",
    },
    {
        "sector": "nonlocal_memory_kernel",
        "parent_variable": "K(x,x'), Box^{-1}, history/domain kernel",
        "reduction_target": "local kernel silence/screening or retained kernel coefficient map",
        "legal_zero_or_safe_route": "kernel vanishes in compact ordinary exterior or reduces to constant universal calibration",
        "current_status": "retained_not_reduced",
        "if_not_reduced_rows": "R7;R9;R10;R11",
        "next_action": "derive local kernel silence or map alpha3/Gdot/fifth-force residuals",
    },
    {
        "sector": "source_normalization_operator",
        "parent_variable": "kappa, G_eff, M_eff, Pi_M J, mu_extra",
        "reduction_target": "constant universal measured GM with no range/time/species leakage",
        "legal_zero_or_safe_route": "mu_obs=G_eff M_eff and partial_{t,r,A,lambda} mu_obs=0",
        "current_status": "conditional_not_parent_derived",
        "if_not_reduced_rows": "R1;R4;R9;R10;R11",
        "next_action": "derive source-normalization variation or retain source residuals",
    },
]


SECOND_ORDER_OPERATOR_FILTER = [
    {
        "operator_family": "EH_plus_Lambda",
        "operator_form": "sqrt(-g)(R-2 Lambda)",
        "second_order_status": "pass_if_source_normalized",
        "required_repair_if_failed": "derive coefficient normalization and local Lambda harmlessness",
        "R11_policy": "target_baseline_only",
    },
    {
        "operator_family": "Gauss_Bonnet_topological_4D",
        "operator_form": "sqrt(-g)(Riemann^2-4 Ricci^2+R^2)",
        "second_order_status": "boundary_topological_only",
        "required_repair_if_failed": "prove no local boundary/class hair",
        "R11_policy": "harmless_only_if_topological_and_boundary_safe",
    },
    {
        "operator_family": "R2_fR_scalar_mode",
        "operator_form": "sqrt(-g)(c_R2 R^2 + f_extra(R))",
        "second_order_status": "fail_unless_zero_or_decoupled",
        "required_repair_if_failed": "derive c=0/infinite scalar mass/zero coupling or map scalar residuals",
        "R11_policy": "retained_R11_plus_R10_if_finite_range",
    },
    {
        "operator_family": "Ricci_Weyl_squared",
        "operator_form": "sqrt(-g)(c_Ricci R_mn R^mn + c_Weyl C_mnrs C^mnrs)",
        "second_order_status": "fail_unless_topological_or_zero",
        "required_repair_if_failed": "derive topological combination/coefficient zero or weak-field slip map",
        "R11_policy": "retained_R11",
    },
    {
        "operator_family": "scalar_tensor_class_metric",
        "operator_form": "sqrt(-g)(F(phi,C)R - kinetic - V)",
        "second_order_status": "metric_only_fail_unless_scalar_harmless",
        "required_repair_if_failed": "prove phi/C constant universal with zero stress/source charge or map residuals",
        "R11_policy": "retained_R11_plus_possible_R10",
    },
    {
        "operator_family": "vector_aether_domain",
        "operator_form": "V_mu V_nu R^{mu nu}, domain normal, projector vector stress",
        "second_order_status": "metric_only_fail",
        "required_repair_if_failed": "derive vector absent/gauge/aligned without stress or map preferred-frame rows",
        "R11_policy": "retained_R11",
    },
    {
        "operator_family": "torsion_nonmetricity",
        "operator_form": "T^2, Q^2, independent connection couplings",
        "second_order_status": "metric_compatibility_fail_unless_eliminated",
        "required_repair_if_failed": "derive Levi-Civita compatibility theorem or retain source/light-cone rows",
        "R11_policy": "retained_R11",
    },
    {
        "operator_family": "nonlocal_memory",
        "operator_form": "R Box^{-1} R or history/domain kernel",
        "second_order_status": "locality_fail_unless_silent",
        "required_repair_if_failed": "derive compact-local kernel silence/screening or map residuals",
        "R11_policy": "retained_R11_plus_R10_R9",
    },
]


OBSTRUCTION_COUNTEREXAMPLES = [
    {
        "counterexample": "algebraic_scalar_generates_fR",
        "lesson": "solving an auxiliary scalar can leave an effective f(R) or higher-curvature operator",
        "blocked_shortcut": "E_phi=0 means scalar is harmless",
    },
    {
        "counterexample": "massive_scalar_with_source_charge",
        "lesson": "positive mass gap does not erase a finite-range force if source/test charges remain",
        "blocked_shortcut": "m_X large or finite means no fifth force",
    },
    {
        "counterexample": "covariant_vector_aether",
        "lesson": "a fully covariant vector can still define a preferred frame",
        "blocked_shortcut": "covariance kills alpha1/alpha2",
    },
    {
        "counterexample": "Palatini_or_metric_affine_branch",
        "lesson": "independent connection variables can survive unless compatibility is derived",
        "blocked_shortcut": "using g automatically means Levi-Civita",
    },
    {
        "counterexample": "boundary_flux_balanced_but_hairy",
        "lesson": "a boundary Euler equation can balance flux while leaving radial/shear/vector hair",
        "blocked_shortcut": "boundary owned means local no-hair",
    },
    {
        "counterexample": "conserved_higher_curvature_tensor",
        "lesson": "non-EH conserved tensors satisfy Bianchi-like conservation but are not GR",
        "blocked_shortcut": "conserved equation means Einstein equation",
    },
    {
        "counterexample": "local_EFT_suppressed_operator",
        "lesson": "small coefficients can be empirically viable while not theorem-zero",
        "blocked_shortcut": "EFT small equals derived GR",
    },
    {
        "counterexample": "field_redefinition_to_metric_frame",
        "lesson": "a metric relabel can move non-EH content into matter/source/operator sectors",
        "blocked_shortcut": "rename the observed metric and EH follows",
    },
]


RESIDUAL_MAP = [
    {"failed_condition": "scalar_class_metric_not_reduced", "fallback": "R11 scalar/class vector row plus R2/R3/R4/R9/R10 maps", "claim_policy": "modified_gravity_retained"},
    {"failed_condition": "vector_domain_not_reduced", "fallback": "R11 vector row plus R5/R6/R7/R8 preferred-frame maps", "claim_policy": "preferred_frame_retained"},
    {"failed_condition": "projector_domain_stress_not_reduced", "fallback": "R11 projector/domain row plus alpha_i/xi/Gdot/fifth-force maps", "claim_policy": "projector_stress_retained"},
    {"failed_condition": "bulk_X_not_reduced", "fallback": "R10 alpha(lambda) curve plus R11 bulk-X row", "claim_policy": "fifth_force_retained"},
    {"failed_condition": "boundary_not_topological_harmless", "fallback": "boundary coefficients feeding R3/R4/R7/R8/R9/R11", "claim_policy": "boundary_nohair_not_claimed"},
    {"failed_condition": "torsion_nonmetricity_not_eliminated", "fallback": "R11 connection row plus WEP/clock/light/spin caveats", "claim_policy": "metric_compatibility_not_claimed"},
    {"failed_condition": "higher_curvature_not_forbidden", "fallback": "R11 R2/fR/Ricci/Weyl coefficient rows plus PPN/fifth-force maps", "claim_policy": "EH_not_claimed"},
    {"failed_condition": "nonlocal_kernel_not_silent", "fallback": "R11 nonlocal row plus R7/R9/R10 maps", "claim_policy": "locality_not_claimed"},
    {"failed_condition": "source_normalization_not_constant", "fallback": "source residual rows R1/R4/R9/R10/R11", "claim_policy": "Newtonian_reduction_not_claimed"},
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "legal sector-elimination modes written",
        "status": "pass",
        "evidence": "absent, gauge/topological, algebraic harmless, positive no-hair, and retained-vector routes recorded",
    },
    {
        "claim": "all extra sectors reduced to metric-only",
        "status": "fail",
        "evidence": "scalar/class, vector/domain, projector, bulk-X, boundary, connection, higher-curvature, nonlocal, and source sectors remain open",
    },
    {
        "claim": "second-order metric operator restriction derived",
        "status": "fail",
        "evidence": "no parent theorem forbids R2/fR/Ricci/Weyl/nonlocal operators through local tested scales",
    },
    {
        "claim": "metric-only exterior derived",
        "status": "fail",
        "evidence": "extra sectors are not absent/gauge/topological/no-haired by parent variation",
    },
    {
        "claim": "R11 fallback made sharper",
        "status": "pass",
        "evidence": "every failed reduction maps to retained R11 coefficient-vector rows and induced residual rows",
    },
    {
        "claim": "EH/Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "this is a reduction attempt and retained-residual map, not a completed parent theorem",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "reduction_theorem_chain_written",
        "status": "pass",
        "evidence": "6-step sector-reduction chain recorded",
    },
    {
        "gate": "legal_elimination_modes_written",
        "status": "pass",
        "evidence": "5 legal sector fates recorded",
    },
    {
        "gate": "sector_reduction_matrix_written",
        "status": "pass",
        "evidence": "10 local exterior sectors audited",
    },
    {
        "gate": "second_order_filter_written",
        "status": "pass",
        "evidence": "8 operator families filtered",
    },
    {
        "gate": "obstruction_counterexamples_written",
        "status": "pass",
        "evidence": "8 fake-reduction shortcuts rejected",
    },
    {
        "gate": "residual_map_written",
        "status": "pass",
        "evidence": "failed reductions mapped to R rows",
    },
    {
        "gate": "all_extra_sectors_reduced",
        "status": "fail",
        "evidence": "no all-sector absent/gauge/topological/no-hair proof supplied",
    },
    {
        "gate": "metric_only_second_order_derived",
        "status": "fail",
        "evidence": "P3/P6 remain open; R11 retained",
    },
    {
        "gate": "R11_promoted",
        "status": "fail",
        "evidence": "R11 still requires theorem-zero or executable coefficient vector",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "sector-reduction attempt only; no EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The metric-only second-order route is now reduced to a sector-by-sector theorem test. A sector may disappear only if it is absent by parent symmetry, pure gauge/topological, algebraically harmless, positive source-free no-haired, or retained as an executable R11 vector row. Applying that test to the current corpus does not derive a metric-only second-order exterior: scalar/class, vector/domain, projector, bulk-X, boundary, torsion/nonmetricity, higher-curvature, nonlocal, and source-normalization sectors remain open or retained. Therefore the route is sharper but not closed; EH, Newton, PPN, R10, R11, and local GR are not promoted.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "441-extra-sector-nohair-priority-gate.md",
        "why_next": "rank which extra sector has the best chance of theorem-zero versus which must immediately become R11 data",
    },
    {
        "rank": 2,
        "target": "filled R11 nonEH operator vector",
        "why_next": "if sector no-hair fails, the branch needs actual coefficient rows to become testable",
    },
    {
        "rank": 3,
        "target": "metric compatibility theorem attempt",
        "why_next": "torsion/nonmetricity is a crisp subproblem: derive Levi-Civita observed branch or retain connection rows",
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
    text = f"""# 440 - Metric-Only Second-Order Sector-Reduction Attempt

Private EH/local-GR derivation checkpoint. This is not a public Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, cosmology, local-GR, or unified-field claim.

## 1. Purpose

Checkpoint 439 identified P3 and P6 as the central EH blockers:

```text
P3: no extra local propagating fields.
P6: second-order metric equations.
```

This checkpoint attempts the reduction honestly. It asks which sectors can be eliminated by parent variation and which sectors must stay as R11 coefficient-vector data.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/metric_only_second_order_sector_reduction_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Reduction Theorem Chain

{markdown_table(REDUCTION_THEOREM_CHAIN, ["step", "claim", "mathematical_form", "status", "meaning"])}

Core rule:

```text
An extra sector Z_A is eliminated only if parent variation proves one of:

  absent by symmetry,
  pure gauge/topological,
  algebraically harmless with no extra metric operator,
  positive source-free no-hair,
  or retained as R11 coefficient data.

Solving E_A=0 is not enough if substituting Z_A creates stress, source charge,
higher derivatives, nonlocal kernels, preferred frames, or finite-range forces.
```

## 5. Legal Elimination Modes

{markdown_table(LEGAL_ELIMINATION_MODES, ["mode", "required_evidence", "valid_result", "current_availability"])}

## 6. Sector Reduction Matrix

{markdown_table(SECTOR_REDUCTION_MATRIX, ["sector", "parent_variable", "reduction_target", "current_status", "if_not_reduced_rows", "next_action"])}

## 7. Second-Order Operator Filter

{markdown_table(SECOND_ORDER_OPERATOR_FILTER, ["operator_family", "operator_form", "second_order_status", "required_repair_if_failed", "R11_policy"])}

## 8. Obstruction Counterexamples

{markdown_table(OBSTRUCTION_COUNTEREXAMPLES, ["counterexample", "lesson", "blocked_shortcut"])}

## 9. Residual Map

{markdown_table(RESIDUAL_MAP, ["failed_condition", "fallback", "claim_policy"])}

## 10. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 11. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is the cleanest version of the hard news. The path to GR is not dead, but "metric-only" is not free. Every extra sector has to either leave by a real theorem or walk into the R11 vector with its gloves on.

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
    write_csv(results_dir / "reduction_theorem_chain.csv", REDUCTION_THEOREM_CHAIN)
    write_csv(results_dir / "legal_elimination_modes.csv", LEGAL_ELIMINATION_MODES)
    write_csv(results_dir / "sector_reduction_matrix.csv", SECTOR_REDUCTION_MATRIX)
    write_csv(results_dir / "second_order_operator_filter.csv", SECOND_ORDER_OPERATOR_FILTER)
    write_csv(results_dir / "obstruction_counterexamples.csv", OBSTRUCTION_COUNTEREXAMPLES)
    write_csv(results_dir / "residual_map.csv", RESIDUAL_MAP)
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
        "reduction_theorem_steps": len(REDUCTION_THEOREM_CHAIN),
        "legal_elimination_modes": len(LEGAL_ELIMINATION_MODES),
        "sector_reduction_rows": len(SECTOR_REDUCTION_MATRIX),
        "second_order_filter_rows": len(SECOND_ORDER_OPERATOR_FILTER),
        "obstruction_counterexamples": len(OBSTRUCTION_COUNTEREXAMPLES),
        "residual_map_rows": len(RESIDUAL_MAP),
        "all_extra_sectors_reduced": False,
        "metric_only_second_order_derived": False,
        "R11_promoted": False,
        "EH_promoted": False,
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
        description="Write checkpoint 440 metric-only second-order sector-reduction attempt artifacts."
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
