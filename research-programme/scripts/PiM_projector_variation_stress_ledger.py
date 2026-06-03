from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "PiM-projector-variation-stress-ledger"
CHECKPOINT_DOC = "456-PiM-projector-variation-stress-ledger.md"
STATUS = "PiM_projector_variation_stress_ledger_written_Hodge_metric_dependence_retained_topological_route_conditional_no_measured_GM_Newton_or_local_GR_pass"
CLAIM_CEILING = "PiM_projector_variation_stress_ledger_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "457-mass-current-Hamiltonian-boundary-charge-attempt.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv")


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
        "path": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "immediate flux-closure checkpoint and projector variation next target",
    },
    {
        "path": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "Pi_M algebra checkpoint and variation warning",
    },
    {
        "path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "PM5 projector variation ownership contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "role": "FC rows requiring projector variation silence before flux closure",
    },
    {
        "path": "233-boundary-symplectic-metric-or-local-EH-operator.md",
        "role": "Hodge/DeWitt boundary metric candidate for projector orthogonality",
    },
    {
        "path": "245-exact-relative-memory-or-projector-stress-bianchi.md",
        "role": "N4 exact memory plus N5 projector-stress Bianchi warning",
    },
    {
        "path": "249-projector-boundary-only-condition-or-metric-only-reduction-fail.md",
        "role": "boundary-only condition and metric-only EH fail if bulk projector stress survives",
    },
    {
        "path": "251-N5-boundary-projector-parent-owner-or-modified-exterior-branch.md",
        "role": "topological projector route and Hodge projector no-go",
    },
    {
        "path": "252-topological-projector-parent-action-skeleton.md",
        "role": "metric-independent topological projector parent skeleton",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward identity with projector variation force ledger",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-force fates and retained PPN residual map",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "Euler ledger invalid fork: metric-dependent projector without stress",
    },
    {
        "path": "runs/20260601-000068-N5-boundary-projector-parent-owner-or-modified-exterior-branch/results/N5_variation_identities.csv",
        "role": "machine-readable N5 variation identities and Hodge no-go",
    },
    {
        "path": "runs/20260601-000068-N5-boundary-projector-parent-owner-or-modified-exterior-branch/results/modified_exterior_branch_implications.csv",
        "role": "machine-readable projector-stress exterior fates",
    },
    {
        "path": "runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/projector_variation_forks.csv",
        "role": "machine-readable projector variation forks",
    },
    {
        "path": "runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/force_ledger.csv",
        "role": "machine-readable Ward force ledger including F_P",
    },
    {
        "path": "runs/20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map/results/force_fate_map.csv",
        "role": "machine-readable force fate map and PPN targets",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/operator_families.csv",
        "role": "R11 projector-domain stress family and retained-symbolic policy",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/invalid_forks.csv",
        "role": "invalid fork list including metric-dependent projector without stress",
    },
    {
        "path": "runs/20260602-170000-PiM-parent-symplectic-projector-algebra-attempt/results/variation_ledger.csv",
        "role": "Pi_M variation ledger from 454",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "projector_variation_chain_rule",
        "statement": "Any parent use of Pi_M must vary the projected source as a product. The safe algebraic projector identity is not enough; if Pi_M depends on the metric, boundary metric, Hodge representative, domain, or source-space split, its variation is a physical source/stress term.",
        "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H; delta_g S_source_norm contains (delta_g Pi_M)J_H",
        "status": "exact_variation_gate",
    },
    {
        "part": "topological_zero_stress_route",
        "statement": "If Pi_M is the absolute cohomology charge map or a metric-independent topological/relative-chain projector, and the source-normalization term is wedge/topological in the compact exterior, then the bulk metric variation of Pi_M can vanish.",
        "mathematical_form": "delta_g Pi_M|E=0 and delta_g S_PiM|bulk=0 => T_PiM_munu|bulk=0",
        "status": "valid_conditional_route",
    },
    {
        "part": "Hodge_metric_dependence_no_go",
        "statement": "If Pi_M is implemented as a Hodge, DeWitt, least-energy, Green-operator, or orthogonal harmonic projector, metric dependence is generic. Dropping the induced stress is fake GR; the branch must retain projector stress or prove a cancellation/source-annihilation theorem.",
        "mathematical_form": "delta_g Pi_H(g) contains delta_g star, delta_g Delta_g, delta_g G_Delta, delta_g inner_product terms",
        "status": "generic_retained_residual",
    },
    {
        "part": "boundary_only_limit",
        "statement": "Boundary-supported projector variation is compatible with a metric-only exterior only if the boundary stress is class-only, monopole-only, and carries no trace-free, radial, vector, clock, WEP, time, or range hair.",
        "mathematical_form": "delta_g S_PiM = delta_g S_boundary, int_boundary Pi_M K_owner = constant_global or 0",
        "status": "conditional_boundary_route_not_derived",
    },
    {
        "part": "modified_exterior_fork",
        "statement": "If bulk projector stress survives and is retained honestly, the branch is a modified exterior equation, not a vacuum Einstein/local-GR reduction. It may still be testable, but must be scored as a residual deformation.",
        "mathematical_form": "G_munu+Lambda g_munu = 8 pi G T_PiM_munu + retained sectors",
        "status": "honest_retained_fork",
    },
    {
        "part": "current_corpus_status",
        "statement": "The corpus has a conditional topological no-bulk-stress route and a Hodge no-go warning, but it has not parent-derived Pi_M as metric-independent, boundary-only, stress-free, or coefficient-mapped.",
        "mathematical_form": "PV0-PV8 remain contract rows; R11/R5/R6/R7/R8 residuals retained",
        "status": "not_parent_derived",
    },
]


VARIATION_FORKS = [
    {
        "fork": "absolute_charge_topological_PiM",
        "definition": "Pi_M is the integral/cohomology charge map on a fixed oriented S2 class, not a metric Hodge projector.",
        "bulk_stress_status": "zero_if_parent_owned",
        "local_GR_status": "best_conditional_route",
        "open_issue": "must parent-derive topology/domain selection and still calibrate measured GM",
        "residual_rows_if_open": "R4;R7;R8;R9;R11",
    },
    {
        "fork": "metric_independent_relative_chain_projector",
        "definition": "Pi_M/P_mem arise from relative-chain/topological data with delta_g projector zero in compact exterior.",
        "bulk_stress_status": "zero_if_wedge_topological_action",
        "local_GR_status": "conditional_N5_support",
        "open_issue": "same object must not become a local-only patch and must own boundary/domain variation",
        "residual_rows_if_open": "R5;R6;R7;R8;R11",
    },
    {
        "fork": "boundary_only_projector_stress",
        "definition": "projector variation has no compact bulk support but leaves boundary matching stress/flux.",
        "bulk_stress_status": "zero_away_from_boundary",
        "local_GR_status": "allowed_only_if_boundary_nohair",
        "open_issue": "boundary trace-free/vector/radial/time/source hair not derived zero",
        "residual_rows_if_open": "R3;R4;R7;R8;R9;R11",
    },
    {
        "fork": "Hodge_DeWitt_orthogonal_PiM",
        "definition": "Pi_M uses Hodge/DeWitt/orthogonal metric on source-current space to select harmonic mass channel.",
        "bulk_stress_status": "generically_nonzero",
        "local_GR_status": "modified_exterior_unless_cancelled",
        "open_issue": "delta_g star/Laplacian/Green/inner-product terms must be retained or theorem-cancelled",
        "residual_rows_if_open": "R3;R4;R7;R8;R10;R11",
    },
    {
        "fork": "fixed_external_projector_or_readout_mask",
        "definition": "Pi_M is chosen after solving/fitting and not varied in the parent action.",
        "bulk_stress_status": "hidden_force_forbidden",
        "local_GR_status": "invalid_branch",
        "open_issue": "explicit diffeomorphism/conservation cheat",
        "residual_rows_if_open": "R0-R11",
    },
    {
        "fork": "retained_bulk_projector_stress",
        "definition": "T_PiM is kept in the field equations with coefficient/profile to be bounded.",
        "bulk_stress_status": "nonzero_retained",
        "local_GR_status": "honest_modified_exterior",
        "open_issue": "needs coefficient/profile map to PPN/source-normalization observables",
        "residual_rows_if_open": "R3;R4;R5;R6;R7;R8;R10;R11",
    },
]


STRESS_SOURCES = [
    {
        "source": "Hodge_star_variation",
        "symbolic_origin": "delta_g star in harmonic representative or boundary Hodge pairing",
        "why_dangerous": "changes the selected mass/shear/memory split under metric variation",
        "safe_condition": "do not use Hodge star in the compact local bulk projector, or retain stress",
        "affected_rows": "R3;R4;R7;R8;R11",
        "current_status": "retained_if_used",
    },
    {
        "source": "Laplacian_Green_operator_variation",
        "symbolic_origin": "delta_g Delta_g and delta_g G_Delta in orthogonal harmonic projection",
        "why_dangerous": "produces nonlocal metric response and possible radial/shear source",
        "safe_condition": "topological charge map or explicit coefficient/profile map",
        "affected_rows": "R3;R4;R10;R11",
        "current_status": "generic_no_go_for_free_GR",
    },
    {
        "source": "DeWitt_inner_product_variation",
        "symbolic_origin": "delta_g source-space metric separating trace-free shell stress from mass block",
        "why_dangerous": "can reintroduce gamma/beta/slip-like stress even when mass is preserved",
        "safe_condition": "block is boundary-only/no-hair or retained as PPN residual",
        "affected_rows": "R3;R4;R8;R11",
        "current_status": "not_parent_derived",
    },
    {
        "source": "domain_homology_representative_variation",
        "symbolic_origin": "delta Sigma_ext, delta S2 representative, delta chi_D, delta n_mu",
        "why_dangerous": "changes what counts as the enclosed mass charge or preferred domain",
        "safe_condition": "fixed-topology branch or covariant/topological domain selector",
        "affected_rows": "R5;R6;R8;R9;R11",
        "current_status": "conditional_open",
    },
    {
        "source": "source_current_variation",
        "symbolic_origin": "Pi_M delta J_H from observed coframe/matter variation",
        "why_dangerous": "source current may not be the measured Hilbert/Ward current if frame or source split fails",
        "safe_condition": "same observed coframe and source-current Ward theorem",
        "affected_rows": "R0;R1;R4;R11",
        "current_status": "conditional_from_prior_contracts",
    },
    {
        "source": "constraint_multiplier_stress",
        "symbolic_origin": "lambda_M or lambda_P source-normalization/projector constraints",
        "why_dangerous": "a multiplier can impose closure while adding unowned stress or hidden source",
        "safe_condition": "first-class, gauge, topological, or independently Ward-owned multiplier",
        "affected_rows": "R1;R4;R7;R9;R11",
        "current_status": "not_parent_derived",
    },
    {
        "source": "readout_mask_backreaction",
        "symbolic_origin": "P_read or fitted Pi_M enters S_parent or cancels residuals after scoring",
        "why_dangerous": "post-fit success becomes a hidden parent source",
        "safe_condition": "readout after variation only",
        "affected_rows": "R0-R11",
        "current_status": "forbidden",
    },
]


DERIVATION_CHAIN = [
    {
        "step": 1,
        "claim": "Start from the exact product variation.",
        "mathematical_step": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H",
        "status": "exact",
        "gap": "delta Pi_M not yet theorem-zero",
    },
    {
        "step": 2,
        "claim": "If Pi_M is topological/absolute-charge data, bulk variation can vanish.",
        "mathematical_step": "delta_g Pi_M|E=0 and S_PiM wedge/topological => T_PiM|bulk=0",
        "status": "conditional_sufficient_route",
        "gap": "parent has not derived Pi_M as this object",
    },
    {
        "step": 3,
        "claim": "If Pi_M is Hodge/orthogonal, bulk variation is generically physical.",
        "mathematical_step": "delta_g Pi_H(g) != 0 through star, Delta, Green, or inner product",
        "status": "generic_no_go_for_free_GR",
        "gap": "requires retained stress or special cancellation theorem",
    },
    {
        "step": 4,
        "claim": "Boundary-only variation is allowed only with no boundary hair.",
        "mathematical_step": "T_PiM|bulk=0 but int_boundary Pi_M K_owner must be 0 or constant_global",
        "status": "conditional_not_derived",
        "gap": "boundary shear/vector/radial/time source locks remain open",
    },
    {
        "step": 5,
        "claim": "Retained bulk projector stress demotes the branch to modified exterior.",
        "mathematical_step": "G_munu+Lambda g_munu=8piG T_PiM_munu+...",
        "status": "honest_fork",
        "gap": "needs coefficient/profile map and PPN/source scorer",
    },
    {
        "step": 6,
        "claim": "Therefore 455 flux closure cannot be promoted until the variation fork is decided.",
        "mathematical_step": "d(Pi_M J_H)=0 plus unowned delta Pi_M still fails local-GR/source-normalization gate",
        "status": "no_promotion",
        "gap": "measured GM/Newton/local GR remain unpromoted",
    },
]


CONTRACT = [
    {
        "contract_id": "PV0_product_variation_included",
        "required_identity": "all Pi_M source-normalization variations use the full product rule",
        "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H",
        "closes_component": "hidden projector-source stress",
        "affected_rows": "R3;R4;R7;R8;R10;R11",
        "current_status": "written_exact_gate",
        "evidence_needed": "future parent action includes Pi_M variation terms before reduction",
        "fallback_if_missing": "branch is rejected as dropped projector stress",
    },
    {
        "contract_id": "PV1_topological_absolute_charge_route",
        "required_identity": "Pi_M is parent-derived as metric-independent absolute cohomology/charge data in the compact local exterior",
        "mathematical_form": "delta_g Pi_M|E=0; Pi_M J=ell_M(J) omega_M_top with ell_M topological",
        "closes_component": "bulk projector stress from mass projection",
        "affected_rows": "R4;R7;R8;R9;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "parent topology/domain theorem fixing absolute S2 charge map before readout",
        "fallback_if_missing": "Pi_M stress or readout ambiguity remains retained",
    },
    {
        "contract_id": "PV2_Hodge_DeWitt_metric_dependence_retained",
        "required_identity": "any Hodge/DeWitt/orthogonal implementation of Pi_M is varied and its stress retained or theorem-cancelled",
        "mathematical_form": "delta_g Pi_H(g) -> T_PiM_munu or cancellation theorem",
        "closes_component": "fake metric-only EH reduction",
        "affected_rows": "R3;R4;R7;R8;R10;R11",
        "current_status": "retained_if_used",
        "evidence_needed": "explicit delta_g star/Delta/Green/inner-product stress map or no-use theorem",
        "fallback_if_missing": "Hodge Pi_M cannot support local-GR reduction",
    },
    {
        "contract_id": "PV3_boundary_only_nohair",
        "required_identity": "boundary-supported projector stress is class-only, monopole-only, and derivative-silent",
        "mathematical_form": "T_PiM|bulk=0 and int_boundary Pi_M K_owner=0 or constant_global with partial_{t,r,A,lambda}=0",
        "closes_component": "boundary/improvement source monopole and shear/vector hair",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_status": "fail_open",
        "evidence_needed": "boundary no-flux/no-shear/no-vector/no-radial theorem",
        "fallback_if_missing": "boundary coefficient vector blocks Newton/local-GR claim",
    },
    {
        "contract_id": "PV4_domain_homology_variation_owned",
        "required_identity": "the S2 representative, domain selector, normal, and homology class used by Pi_M are covariant/topological or varied",
        "mathematical_form": "delta Sigma_ext, delta chi_D, delta n_mu, delta L_cg -> zero/topological or retained",
        "closes_component": "preferred-frame/preferred-location/domain source leakage",
        "affected_rows": "R5;R6;R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "domain/homology parent selector theorem or coefficient map",
        "fallback_if_missing": "preferred-frame/location and Gdot/range residual rows remain active",
    },
    {
        "contract_id": "PV5_multiplier_stress_owned",
        "required_identity": "lambda_M and projector/source-normalization multipliers have independent gauge/topological/Ward origin and no unowned stress",
        "mathematical_form": "delta_g S_lambdaM included; T_lambdaM=0/topological or retained",
        "closes_component": "fake Euler closure and hidden multiplier stress",
        "affected_rows": "R1;R4;R7;R9;R11",
        "current_status": "not_satisfied",
        "evidence_needed": "first-class/topological multiplier derivation and stress ledger",
        "fallback_if_missing": "closure counted as assumption only",
    },
    {
        "contract_id": "PV6_modified_exterior_residual_map",
        "required_identity": "any retained T_PiM bulk stress is mapped into observable PPN/source-normalization coefficients",
        "mathematical_form": "T_PiM_munu -> gamma-1, beta-1, alpha_i, xi, delta_G, radial/source residual vector",
        "closes_component": "symbolic modified exterior",
        "affected_rows": "R3;R4;R5;R6;R7;R8;R10;R11",
        "current_status": "not_yet_executable",
        "evidence_needed": "coefficient/profile, units, normalization, weak-field map, and local bounds",
        "fallback_if_missing": "retained_symbolic and no local-GR/Newton claim",
    },
    {
        "contract_id": "PV7_readout_masks_after_variation_only",
        "required_identity": "P_read, P_active, or fitted Pi_M masks never enter the parent variation",
        "mathematical_form": "delta S_parent does not contain post-readout projector choices",
        "closes_component": "post-fit Bianchi/source-normalization cheat",
        "affected_rows": "R0-R11",
        "current_status": "policy_written",
        "evidence_needed": "future scripts/actions keep readout operators outside S_parent",
        "fallback_if_missing": "branch rejected, not retained as small",
    },
    {
        "contract_id": "PV8_retained_residual_fallback",
        "required_identity": "unproved projector variation silence activates retained residual rows automatically",
        "mathematical_form": "PV failure -> R3/R4/R5/R6/R7/R8/R10/R11 projector-domain stress vector",
        "closes_component": "silent loss of failed variation premise",
        "affected_rows": "R3;R4;R5;R6;R7;R8;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "machine mapping into local residual evaluator",
        "fallback_if_missing": "manual no-promotion discipline remains required",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "Hodge_projector_stress_dropped",
        "construction": "Pi_M is defined using a Hodge harmonic representative but delta_g star/Delta/Green terms are omitted",
        "why_it_fails": "metric-dependent projector has physical stress",
        "required_repair": "topological charge map, no-use theorem, cancellation proof, or retained stress",
        "affected_contracts": "PV2;PV6",
    },
    {
        "counterexample": "topological_name_metric_action",
        "construction": "call the projector topological while the action uses sqrt(-g), Hodge star, or metric inner product in the bulk",
        "why_it_fails": "metric dependence reappears through the action even if labels are topological",
        "required_repair": "wedge/chain/topological action or retained stress",
        "affected_contracts": "PV1;PV2",
    },
    {
        "counterexample": "boundary_only_with_shear",
        "construction": "projector stress is boundary-supported but contains trace-free/angular/vector/radial flux",
        "why_it_fails": "boundary stress still affects PPN/source-normalization matching",
        "required_repair": "class-only monopole/no-hair boundary theorem",
        "affected_contracts": "PV3",
    },
    {
        "counterexample": "domain_selected_mass_surface",
        "construction": "the S2 surface or domain used by ell_M is chosen by a physical local normal or fitted boundary",
        "why_it_fails": "mass charge becomes preferred-frame/location/source selection",
        "required_repair": "covariant/topological domain selector or retained preferred-frame residual",
        "affected_contracts": "PV4",
    },
    {
        "counterexample": "lambdaM_closure_with_stress",
        "construction": "lambda_M imposes d(Pi_M J_H)=0 but its metric variation is not included",
        "why_it_fails": "closure equation adds an unowned stress channel",
        "required_repair": "first-class/topological multiplier or retained T_lambdaM",
        "affected_contracts": "PV5",
    },
    {
        "counterexample": "readout_mask_enters_action",
        "construction": "a mask selected after fitting orbital GM is placed into S_parent",
        "why_it_fails": "post-fit readout becomes a hidden source and breaks the variation order",
        "required_repair": "readout after variation only",
        "affected_contracts": "PV7",
    },
    {
        "counterexample": "retained_stress_called_GR",
        "construction": "keep nonzero T_PiM but still announce vacuum EH/local GR",
        "why_it_fails": "the exterior equation is modified unless stress is zero/boundary-harmless",
        "required_repair": "score as modified exterior or prove theorem-zero",
        "affected_contracts": "PV6;PV8",
    },
]


GATE_TESTS = [
    {
        "gate": "projector_variation_chain_rule_written",
        "pass_condition": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H is explicit",
        "current_result": "pass",
        "evidence": "PV0 and theorem statement recorded",
    },
    {
        "gate": "topological_safe_route_written",
        "pass_condition": "metric-independent absolute/topological Pi_M route gives conditional bulk stress zero",
        "current_result": "pass_conditional",
        "evidence": "PV1 and variation forks recorded",
    },
    {
        "gate": "Hodge_stress_not_overclaimed",
        "pass_condition": "Hodge/DeWitt projector is not treated as local-GR safe without retaining stress",
        "current_result": "pass",
        "evidence": "PV2 and counterexample recorded",
    },
    {
        "gate": "readout_mask_forbidden",
        "pass_condition": "post-fit/readout projectors cannot enter S_parent",
        "current_result": "pass",
        "evidence": "PV7 written",
    },
    {
        "gate": "PiM_variation_parent_derived",
        "pass_condition": "current corpus derives Pi_M as metric-independent/topological or supplies full stress cancellation",
        "current_result": "fail",
        "evidence": "PV1/PV2 remain conditional or retained",
    },
    {
        "gate": "boundary_projector_nohair_derived",
        "pass_condition": "boundary-supported projector stress has no shear/vector/radial/time/source hair",
        "current_result": "fail",
        "evidence": "PV3 remains fail_open",
    },
    {
        "gate": "retained_stress_executable",
        "pass_condition": "nonzero T_PiM has coefficient/profile map to PPN/source observables",
        "current_result": "fail",
        "evidence": "PV6 remains not_yet_executable",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "projector stress is theorem-zero/boundary-harmless or empirically scored with all P8 rows closed",
        "current_result": "fail",
        "evidence": "variation stress ledger only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "Pi_M variation stress ledger written",
        "status": "pass",
        "evidence": "product rule, forks, stress sources, and PV0-PV8 contract recorded",
    },
    {
        "claim": "topological zero-bulk-stress route identified",
        "status": "pass_conditional",
        "evidence": "metric-independent absolute/topological Pi_M would give delta_g Pi_M=0 in the compact exterior",
    },
    {
        "claim": "Hodge/DeWitt overclaim blocked",
        "status": "pass",
        "evidence": "metric-dependent projector stress is retained unless cancelled",
    },
    {
        "claim": "modified-exterior fork kept honest",
        "status": "pass",
        "evidence": "nonzero T_PiM means modified exterior, not vacuum EH",
    },
    {
        "claim": "Pi_M variation parent-derived",
        "status": "fail",
        "evidence": "no completed parent theorem makes Pi_M metric-independent/topological or stress-cancelled",
    },
    {
        "claim": "projector stress coefficient map executable",
        "status": "fail",
        "evidence": "retained T_PiM lacks coefficient/profile mapping to local bounds",
    },
    {
        "claim": "measured GM/Newton/local GR promoted",
        "status": "fail",
        "evidence": "projector variation gate only; flux closure and calibration still open",
    },
]


DECISION = [
    {
        "decision": "The Pi_M variation gate is now explicit. The clean local-GR route requires Pi_M to be parent-derived as metric-independent absolute/topological charge data, or for any metric-dependent Hodge/DeWitt implementation to have its stress retained or theorem-cancelled. The current corpus has a conditional topological no-bulk-stress route but not a parent derivation. Therefore Hodge/orthogonal Pi_M remains a retained modified-exterior source unless repaired, boundary-only projector stress remains open, and no measured-GM, Newton, PPN, or local-GR promotion is allowed.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "why_next": "after the projector stress gate, the clean GR-like path is a conserved Hamiltonian/asymptotic mass charge",
    },
    {
        "rank": 2,
        "target": "map PV0-PV8 into R11/P8 residual evaluator",
        "why_next": "failed projector-variation rows should activate projector-domain stress, source-normalization, preferred-frame, and radial hair rows automatically",
    },
    {
        "rank": 3,
        "target": "topological-absolute-PiM-parent-route",
        "why_next": "derive Pi_M as absolute cohomology charge data rather than Hodge metric projector",
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
            "evidence": "Pi_M projector variation stress contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 6 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "variation_forks_written",
            "status": "pass" if len(VARIATION_FORKS) == 6 else "fail",
            "evidence": f"{len(VARIATION_FORKS)} variation forks",
        },
        {
            "gate": "stress_sources_written",
            "status": "pass" if len(STRESS_SOURCES) == 7 else "fail",
            "evidence": f"{len(STRESS_SOURCES)} stress sources",
        },
        {
            "gate": "derivation_chain_written",
            "status": "pass" if len(DERIVATION_CHAIN) == 6 else "fail",
            "evidence": f"{len(DERIVATION_CHAIN)} derivation steps",
        },
        {
            "gate": "contract_written",
            "status": "pass" if len(CONTRACT) == 9 else "fail",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "Hodge_stress_not_overclaimed",
            "status": "pass",
            "evidence": "metric-dependent Hodge/DeWitt branch retained unless cancelled",
        },
        {
            "gate": "readout_mask_forbidden",
            "status": "pass",
            "evidence": "PV7 keeps readout operators after variation only",
        },
        {
            "gate": "PiM_variation_parent_derived",
            "status": "fail",
            "evidence": "no completed parent theorem makes Pi_M metric-independent/topological or stress-cancelled",
        },
        {
            "gate": "boundary_projector_nohair_derived",
            "status": "fail",
            "evidence": "PV3 remains fail_open",
        },
        {
            "gate": "domain_homology_variation_derived",
            "status": "fail",
            "evidence": "PV4 remains not_parent_derived",
        },
        {
            "gate": "multiplier_stress_owned",
            "status": "fail",
            "evidence": "PV5 remains not_satisfied",
        },
        {
            "gate": "retained_stress_executable",
            "status": "fail",
            "evidence": "PV6 lacks coefficient/profile map",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "variation gate only; flux closure and calibration still open",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "Pi_M variation stress ledger only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "projector stress and P8/R11 rows remain retained",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 456 - PiM Projector Variation Stress Ledger

Private P8/R3/R4/R5/R6/R7/R8/R10/R11 projector-stress checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 455 made `d(Pi_M J_H)=0` an exact parent-action target.

This checkpoint asks whether even a successful `Pi_M` route leaks stress through the variation of the projector itself. The key rule is simple: if `Pi_M` depends on the metric, Hodge representative, domain, or boundary metric, then `delta Pi_M` must be owned, retained, or theorem-zero.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/PiM_projector_variation_stress_ledger.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Variation Forks

{markdown_table(VARIATION_FORKS)}

## 6. Stress Sources

{markdown_table(STRESS_SOURCES)}

## 7. Derivation Chain

{markdown_table(DERIVATION_CHAIN)}

## 8. PiM Variation-Stress Contract

The Pi_M projector variation stress contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 9. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 10. Gate Tests

{markdown_table(GATE_TESTS)}

## 11. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 12. Gate Results

{markdown_table(gate_results)}

## 13. Decision

{DECISION[0]["decision"]}

Practical read: this is the key tension. The Hodge/DeWitt route gives a beautiful canonical projector, but it usually carries metric stress. The topological absolute-charge route is locally quiet, but then the parent must derive it and still recover calibration/cosmology coupling. No projector gets to be both metric-dependent and stress-free by vibes.

## 14. Next Queue

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
    write_csv(results_dir / "variation_forks.csv", VARIATION_FORKS)
    write_csv(results_dir / "stress_sources.csv", STRESS_SOURCES)
    write_csv(results_dir / "derivation_chain.csv", DERIVATION_CHAIN)
    write_csv(results_dir / "PiM_projector_variation_stress_contract.csv", CONTRACT, CONTRACT_COLUMNS)
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
        "projector_variation_chain_rule_written": True,
        "topological_safe_route_written": True,
        "Hodge_stress_not_overclaimed": True,
        "readout_mask_forbidden": True,
        "PiM_variation_parent_derived": False,
        "boundary_projector_nohair_derived": False,
        "domain_homology_variation_derived": False,
        "multiplier_stress_owned": False,
        "retained_stress_executable": False,
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
    parser = argparse.ArgumentParser(description="Write the MTS Pi_M projector variation stress ledger.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-173000.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
