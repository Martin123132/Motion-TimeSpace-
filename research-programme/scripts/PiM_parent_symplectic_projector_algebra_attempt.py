from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "PiM-parent-symplectic-projector-algebra-attempt"
CHECKPOINT_DOC = "454-PiM-parent-symplectic-projector-algebra-attempt.md"
STATUS = "PiM_parent_symplectic_projector_algebra_attempt_written_canonical_projector_conditions_flux_closure_not_derived_no_measured_GM_Newton_or_local_GR_pass"
CLAIM_CEILING = "PiM_projector_algebra_contract_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "455-PiM-flux-closure-Ward-or-topological-current-attempt.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv")


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
        "role": "minimal non-cheating P_mem split: P_mem=1-Pi_M-Pi_TF-Pi_matter",
    },
    {
        "path": "233-boundary-symplectic-metric-or-local-EH-operator.md",
        "role": "boundary Hodge/DeWitt metric candidate and orthogonal projector route",
    },
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional theorem: closed Pi_M flux gives radially conserved M_eff",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "GM absorption distinction and constant universal source-normalization requirements",
    },
    {
        "path": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "role": "A7 mass-flux projector Euler ledger row and projector-force policy",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole calibration requirements",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector closure attempt and Pi_M algebra next target",
    },
    {
        "path": "453-global-coupling-superselection-parent-action-contract.md",
        "role": "constant kappa/G_eff superselection contract needed after mass projector",
    },
    {
        "path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "MF0-MF8 mass-flux projector and calibration contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "HM1-HM3 mass projector closure and absolute calibration contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
        "role": "SC6 closed calibrated mass projector requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_global_coupling_superselection_CONTRACT.csv",
        "role": "GS rows required to stop G_eff/source coupling drift after Pi_M closure",
    },
    {
        "path": "runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv",
        "role": "machine A7 mass-flux projector ledger row",
    },
    {
        "path": "runs/20260602-160000-Hilbert-source-to-measured-monopole-calibration-gate/results/Hilbert_monopole_calibration_contract.csv",
        "role": "machine Hilbert-monopole calibration contract",
    },
    {
        "path": "runs/20260602-161500-mass-flux-projector-Euler-calibration-attempt/results/mass_flux_projector_contract.csv",
        "role": "machine mass-flux projector contract rows",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_symplectic_projector_theorem",
        "statement": "If the compact exterior source-current space carries a parent-derived boundary Hodge/DeWitt symplectic metric, the exterior topology supplies a normalized absolute S2 harmonic generator, and the mass charge functional is defined before readout, then Pi_M can be defined as the self-adjoint idempotent projection onto the absolute mass-flux harmonic class.",
        "mathematical_form": "Sigma_ext ~= S2 x I; ell_M(J)=int_S2 J; int_S2 omega_M=1; Pi_M J=ell_M(J) omega_M; Pi_M^2=Pi_M; Pi_M^dagger=Pi_M",
        "status": "valid_conditional_projector_algebra",
    },
    {
        "part": "orthogonal_decomposition_contract",
        "statement": "With Pi_M, Pi_TF, and Pi_matter mutually orthogonal under the parent boundary metric, P_mem=1-Pi_M-Pi_TF-Pi_matter is a legal complement only if the projectors are parent-defined, commute on the allowed source-current domain, and preserve the mass class rather than erase it.",
        "mathematical_form": "Pi_i Pi_j=0 for i != j; P_mem^2=P_mem; Pi_M P_mem=0; ell_M(P_mem J)=0",
        "status": "conditional_contract",
    },
    {
        "part": "flux_closure_not_from_projector",
        "statement": "Projector algebra does not by itself prove d(Pi_M J_H)=0. Closure requires a Ward/source-current equation, a topological-current equation, or an Euler equation for the projected mass channel. Otherwise radial drift and boundary/non-Hilbert source residuals remain active.",
        "mathematical_form": "Pi_M^2=Pi_M does not imply d(Pi_M J_H)=0; d(Pi_M J_H)=d ell_M(J_H) wedge omega_M + ell_M(J_H) d omega_M",
        "status": "blocks_overclaim",
    },
    {
        "part": "variation_warning",
        "statement": "If Pi_M depends on the boundary metric, Hodge representative, domain, or source-space splitting, the parent variation must own delta Pi_M terms. Dropping those terms turns the projector into a hidden external source.",
        "mathematical_form": "delta(Pi_M J)=Pi_M delta J + (delta Pi_M)J; (delta Pi_M)J -> T_projector or theorem-zero",
        "status": "variation_contract_not_derived",
    },
    {
        "part": "current_corpus_status",
        "statement": "The corpus now has a sharp Pi_M algebra candidate, but it has not derived the parent boundary symplectic metric, the projector variation stress, the flux-closure equation, absolute measured-GM calibration, or second-order source stability.",
        "mathematical_form": "PM0-PM8/MF0-MF8 remain open except conditional algebra rows",
        "status": "not_parent_derived",
    },
]


ALGEBRA_OBJECTS = [
    {
        "object": "compact_exterior_shell",
        "symbol": "Sigma_ext ~= S2 x I",
        "definition": "ordinary compact-source exterior annulus with fixed topology and oriented S2 cross-sections",
        "current_status": "conditional_standard_branch",
        "open_issue": "boundary/domain topology must not be selected after fitting",
    },
    {
        "object": "source_current_space",
        "symbol": "V_J",
        "definition": "parent source-current space carrying Hilbert current, boundary improvements, shear blocks, direct matter vertices, and memory exchange",
        "current_status": "contract_only",
        "open_issue": "full parent source space and boundary conditions are not derived",
    },
    {
        "object": "boundary_symplectic_metric",
        "symbol": "G_B",
        "definition": "Hodge/DeWitt block metric defining orthogonality between mass flux, trace-free shear, matter vertices, and relative memory",
        "current_status": "candidate_not_parent_derived",
        "open_issue": "needs parent action origin and metric variation ledger",
    },
    {
        "object": "mass_charge_functional",
        "symbol": "ell_M(J)",
        "definition": "absolute S2 flux charge evaluated before readout",
        "current_status": "conditional_topological_functional",
        "open_issue": "must be tied to Hilbert/Ward current, not orbital fit mask",
    },
    {
        "object": "normalized_harmonic_generator",
        "symbol": "omega_M",
        "definition": "closed harmonic representative of absolute H2 with integral one over S2",
        "current_status": "conditional_Hodge_candidate",
        "open_issue": "Hodge representative depends on boundary metric unless only the integral charge is used",
    },
    {
        "object": "mass_projector",
        "symbol": "Pi_M",
        "definition": "self-adjoint idempotent projection onto ell_M(J) omega_M",
        "current_status": "algebra_written_not_parent_derived",
        "open_issue": "flux closure and variation ownership remain open",
    },
    {
        "object": "tracefree_projector",
        "symbol": "Pi_TF",
        "definition": "DeWitt/SO3 projection onto trace-free tangential shell stress and shear",
        "current_status": "candidate",
        "open_issue": "parent scalar-boundary theorem and stress fate not closed",
    },
    {
        "object": "matter_vertex_projector",
        "symbol": "Pi_matter",
        "definition": "direct memory-to-matter/clock vertex block that must be forbidden by universal coupling rather than fitted away",
        "current_status": "conditional_from_matter_contract",
        "open_issue": "matter action still carries conditional no-direct-memory-vertex premise",
    },
    {
        "object": "relative_memory_projector",
        "symbol": "P_mem",
        "definition": "orthogonal complement after preserving mass, shear, and direct matter blocks",
        "current_status": "conditional_complement",
        "open_issue": "P_mem is legal only if all component projectors are parent-owned and mutually orthogonal",
    },
]


PROJECTOR_IDENTITIES = [
    {
        "identity": "idempotence",
        "mathematical_form": "Pi_M(Pi_M J)=Pi_M J if ell_M(omega_M)=1",
        "status": "algebra_pass_conditional",
        "what_it_proves": "Pi_M is a projector onto the mass harmonic line",
        "what_it_does_not_prove": "d(Pi_M J_H)=0 or measured GM calibration",
    },
    {
        "identity": "self_adjointness",
        "mathematical_form": "<Pi_M J1,J2>_G_B=<J1,Pi_M J2>_G_B",
        "status": "conditional_on_GB",
        "what_it_proves": "mass channel is orthogonal under the parent boundary metric",
        "what_it_does_not_prove": "G_B has parent action origin or harmless metric variation",
    },
    {
        "identity": "charge_preservation",
        "mathematical_form": "ell_M(Pi_M J)=ell_M(J)",
        "status": "algebra_pass_conditional",
        "what_it_proves": "ordinary mass flux is preserved rather than erased",
        "what_it_does_not_prove": "ell_M(J) is constant in radius or time",
    },
    {
        "identity": "relative_memory_mass_silence",
        "mathematical_form": "ell_M(P_mem J)=0 and Pi_M P_mem=0",
        "status": "conditional_on_orthogonal_split",
        "what_it_proves": "relative memory cannot hide ordinary mass if the split is legal",
        "what_it_does_not_prove": "relative memory stress is exact, pure gauge, or no-hair",
    },
    {
        "identity": "commutation_domain",
        "mathematical_form": "P_mem^2=P_mem requires Pi_M, Pi_TF, Pi_matter mutually orthogonal/commuting on V_J",
        "status": "not_parent_derived",
        "what_it_proves": "the algebraic condition for non-cheating complements",
        "what_it_does_not_prove": "the parent action supplies those projectors",
    },
    {
        "identity": "closure_condition",
        "mathematical_form": "d(Pi_M J_H)=0 iff d ell_M(J_H)=0 on the exterior mass channel because d omega_M=0",
        "status": "requires_Ward_or_Euler_input",
        "what_it_proves": "exact remaining equation needed for radial M_eff conservation",
        "what_it_does_not_prove": "closure from projector algebra alone",
    },
    {
        "identity": "variation_identity",
        "mathematical_form": "delta(Pi_M J)=Pi_M delta J + (delta Pi_M)J",
        "status": "retained_variation_debt",
        "what_it_proves": "projector stress cannot be silently dropped",
        "what_it_does_not_prove": "delta Pi_M terms vanish or are harmless",
    },
]


DERIVATION_STEPS = [
    {
        "step": 1,
        "claim": "Fix the compact exterior topology and oriented S2 cross-sections before scoring.",
        "mathematical_step": "Sigma_ext ~= S2 x I; H2(Sigma_ext)=R",
        "status": "conditional_standard_input",
        "gap": "domain/boundary selector still needs parent ownership",
    },
    {
        "step": 2,
        "claim": "Define a charge functional that reads the absolute mass-flux class rather than a fitted orbital mask.",
        "mathematical_step": "ell_M(J)=int_S2 J",
        "status": "conditional_topological_input",
        "gap": "J must be the same-frame Hilbert/Ward source current",
    },
    {
        "step": 3,
        "claim": "Choose the normalized harmonic generator of the absolute H2 line.",
        "mathematical_step": "d omega_M=0; delta_GB omega_M=0; int_S2 omega_M=1",
        "status": "conditional_on_boundary_metric",
        "gap": "G_B is candidate, not parent-derived",
    },
    {
        "step": 4,
        "claim": "Define Pi_M algebraically as charge times harmonic generator.",
        "mathematical_step": "Pi_M J=ell_M(J) omega_M",
        "status": "algebra_pass_conditional",
        "gap": "does not yet provide d(Pi_M J_H)=0",
    },
    {
        "step": 5,
        "claim": "Require orthogonality against shear, direct matter, and relative-memory blocks.",
        "mathematical_step": "Pi_M Pi_TF=Pi_M Pi_matter=Pi_M P_mem=0",
        "status": "conditional_on_GB_block_diagonalization",
        "gap": "Pi_TF and Pi_matter are still contract-level",
    },
    {
        "step": 6,
        "claim": "Track variation of the projector if the harmonic representative or boundary metric changes.",
        "mathematical_step": "delta Pi_M contributes source/projector stress unless topological/no-stress",
        "status": "retained_variation_debt",
        "gap": "no parent proof that delta Pi_M is harmless",
    },
    {
        "step": 7,
        "claim": "Conclude only the algebraic projector contract, not Newtonian mass closure.",
        "mathematical_step": "Pi_M legal conditional; d(Pi_M J_H)=0 remains next equation",
        "status": "no_promotion",
        "gap": "measured GM/Newton/local GR remain unpromoted",
    },
]


VARIATION_LEDGER = [
    {
        "ledger_id": "V0_topology_and_orientation",
        "variation_term": "delta Sigma_ext or changed S2 homology representative",
        "risk": "mass charge changes by domain/readout selection",
        "required_owner": "parent domain/boundary selector or fixed compact-topology branch",
        "current_status": "conditional_open",
    },
    {
        "ledger_id": "V1_boundary_metric",
        "variation_term": "delta G_B changes the Hodge representative omega_M and orthogonal split",
        "risk": "dropped projector stress or hidden source normalization",
        "required_owner": "boundary metric action and Bianchi-safe stress ledger",
        "current_status": "not_parent_derived",
    },
    {
        "ledger_id": "V2_source_current",
        "variation_term": "delta J_H from observed coframe/matter variation",
        "risk": "source current is not the same measured Hilbert current",
        "required_owner": "single observed coframe and source-current Ward theorem",
        "current_status": "conditional_from_prior_contracts",
    },
    {
        "ledger_id": "V3_projector_split",
        "variation_term": "delta Pi_TF, delta Pi_matter, delta P_mem",
        "risk": "nonorthogonal projectors make P_mem non-idempotent or erase mass/shear",
        "required_owner": "block-diagonal G_B algebra and no-direct-matter-vertex theorem",
        "current_status": "not_parent_derived",
    },
    {
        "ledger_id": "V4_mass_channel_closure",
        "variation_term": "d ell_M(J_H) along the exterior annulus",
        "risk": "M_eff(r) drifts or boundary/non-Hilbert flux enters measured GM",
        "required_owner": "Ward, topological current, or Euler equation for d(Pi_M J_H)=0",
        "current_status": "not_derived_next_target",
    },
    {
        "ledger_id": "V5_absolute_calibration",
        "variation_term": "normalization between ell_M(J_H), M_eff, and orbital mu_obs",
        "risk": "conserved mass charge is not the measured Newtonian monopole",
        "required_owner": "EH/Poisson/asymptotic/orbital matching theorem",
        "current_status": "not_parent_derived",
    },
]


CONTRACT = [
    {
        "contract_id": "PM0_fixed_exterior_topology",
        "required_identity": "the compact local exterior has a fixed oriented S2 x I topology before readout",
        "mathematical_form": "Sigma_ext ~= S2 x I; H2(Sigma_ext)=R",
        "closes_component": "post-fit domain/homology selection",
        "affected_rows": "R4;R7;R8;R9;R11",
        "current_status": "conditional_open",
        "evidence_needed": "parent domain/boundary branch or fixed-topology local exterior theorem",
        "fallback_if_missing": "Pi_M can be a domain/readout mask and source-normalization rows remain active",
    },
    {
        "contract_id": "PM1_parent_boundary_symplectic_metric",
        "required_identity": "a parent-derived Hodge/DeWitt boundary metric defines source-current orthogonality",
        "mathematical_form": "<.,.>_G_B = Hodge_mass + DeWitt_TF + matter_vertex + relative_memory",
        "closes_component": "arbitrary projector choice",
        "affected_rows": "R0;R1;R4;R7;R8;R11",
        "current_status": "candidate_not_parent_derived",
        "evidence_needed": "boundary symplectic metric from parent action plus variation ledger",
        "fallback_if_missing": "projectors remain conditional decomposition choices",
    },
    {
        "contract_id": "PM2_harmonic_mass_generator",
        "required_identity": "the absolute H2 mass generator is normalized and closed",
        "mathematical_form": "d omega_M=0; int_S2 omega_M=1; delta_GB omega_M=0 if no metric stress",
        "closes_component": "mass-channel normalization ambiguity",
        "affected_rows": "R4;R9;R11",
        "current_status": "conditional_Hodge_candidate",
        "evidence_needed": "Hodge representative or topological charge map with boundary metric dependence owned",
        "fallback_if_missing": "M_eff normalization remains convention-level",
    },
    {
        "contract_id": "PM3_charge_functional_before_readout",
        "required_identity": "the mass functional is defined on the parent Hilbert/Ward current before orbital scoring",
        "mathematical_form": "ell_M(J_H)=int_S2 J_H before readout",
        "closes_component": "post-fit measured-GM mask",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "conditional_from_source_current_contract",
        "evidence_needed": "same-frame Hilbert current and parent source-normalization map",
        "fallback_if_missing": "measured GM is a calibration/readout branch, not derived",
    },
    {
        "contract_id": "PM4_projector_algebra",
        "required_identity": "Pi_M is idempotent, self-adjoint, charge-preserving, and orthogonal to shear/matter/memory blocks",
        "mathematical_form": "Pi_M^2=Pi_M; Pi_M^dagger=Pi_M; ell_M(Pi_M J)=ell_M(J); Pi_M Pi_TF=Pi_M Pi_matter=Pi_M P_mem=0",
        "closes_component": "mass erasure and nonorthogonal projector leakage",
        "affected_rows": "R1;R3;R4;R7;R8;R11",
        "current_status": "algebra_written_conditional",
        "evidence_needed": "explicit projectors and block-orthogonality proof on V_J",
        "fallback_if_missing": "P_mem complement cannot be treated as legal",
    },
    {
        "contract_id": "PM5_projector_variation_owned",
        "required_identity": "delta Pi_M and other projector variation terms are included in the Ward/source ledger or proved harmless",
        "mathematical_form": "delta(Pi_M J)=Pi_M delta J + (delta Pi_M)J",
        "closes_component": "hidden projector stress/source force",
        "affected_rows": "R3;R4;R7;R8;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "Bianchi-safe projector stress theorem or topological/no-stress proof",
        "fallback_if_missing": "T_projector and source-normalization residuals remain active",
    },
    {
        "contract_id": "PM6_flux_closure_requires_Ward_or_Euler",
        "required_identity": "d(Pi_M J_H)=0 follows from a source Ward identity, topological current, or parent Euler equation, not from projector algebra alone",
        "mathematical_form": "d(Pi_M J_H)=0 as Ward_M or E_lambdaM=0",
        "closes_component": "M_eff radial drift and mass-flux exchange",
        "affected_rows": "R4;R7;R9;R10;R11",
        "current_status": "not_parent_derived_next_target",
        "evidence_needed": "derive mass-channel closure equation in compact exterior",
        "fallback_if_missing": "dln_Meff_dt and partial_r ln mu_obs residuals remain active",
    },
    {
        "contract_id": "PM7_absolute_calibration_deferred",
        "required_identity": "closed mass charge is calibrated to orbital/asymptotic measured GM",
        "mathematical_form": "M_eff=(4 pi G_ref)^-1 ell_M(J_H); mu_obs=G_eff M_eff",
        "closes_component": "conserved-but-miscalibrated mass",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "EH/Poisson/asymptotic matching plus constant universal G_eff",
        "fallback_if_missing": "closed Pi_M flux is not enough for Newton claim",
    },
    {
        "contract_id": "PM8_retained_residual_fallback",
        "required_identity": "any failed projector algebra or closure condition is mapped to executable source-normalization residuals",
        "mathematical_form": "failed PM row -> dln_Meff_dt, partial_r ln mu_obs, mu_extra/(GM), eta_source, alpha(lambda)",
        "closes_component": "silent loss of failed Pi_M premises",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "machine mapping from PM rows to P8/R residual evaluator",
        "fallback_if_missing": "manual no-promotion discipline remains required",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "readout_mass_projector",
        "construction": "choose Pi_M after fitting orbital GM so only the successful 1/r mode is retained",
        "why_it_fails": "the projector is a mask, not a parent source-normalization object",
        "required_repair": "define ell_M and Pi_M in the parent current space before scoring",
        "affected_contracts": "PM1;PM3;PM4",
    },
    {
        "counterexample": "nonorthogonal_complement",
        "construction": "set P_mem=1-Pi_M-Pi_TF-Pi_matter without proving projectors commute or are orthogonal",
        "why_it_fails": "P_mem need not be idempotent and can leak mass/shear into memory",
        "required_repair": "block-orthogonality proof under parent G_B",
        "affected_contracts": "PM1;PM4",
    },
    {
        "counterexample": "metric_dependent_Hodge_projector_stress_dropped",
        "construction": "use a Hodge projector whose representative changes with metric but omit delta Pi_M stress",
        "why_it_fails": "projector variation becomes an unowned source in the Ward identity",
        "required_repair": "include delta Pi_M terms or prove topological/no-stress status",
        "affected_contracts": "PM1;PM5",
    },
    {
        "counterexample": "idempotence_claims_closure",
        "construction": "argue Pi_M^2=Pi_M therefore d(Pi_M J_H)=0",
        "why_it_fails": "idempotence is algebraic; closure is differential/current conservation",
        "required_repair": "derive Ward_M, topological current, or E_lambdaM=0",
        "affected_contracts": "PM6",
    },
    {
        "counterexample": "radially_varying_charge",
        "construction": "ell_M(J_H;r2) differs from ell_M(J_H;r1) because boundary or non-Hilbert flux crosses the annulus",
        "why_it_fails": "Pi_M exists but M_eff(r) is not conserved",
        "required_repair": "zero flux theorem or retained radial source-hair residual",
        "affected_contracts": "PM6;PM8",
    },
    {
        "counterexample": "miscalibrated_harmonic_charge",
        "construction": "Pi_M extracts a conserved charge but its normalization is not the orbital/asymptotic mass",
        "why_it_fails": "Newton measures mu_obs=GM, not an arbitrary conserved source charge",
        "required_repair": "absolute calibration to EH/Poisson/asymptotic boundary data",
        "affected_contracts": "PM7",
    },
    {
        "counterexample": "constant_G_missing_after_PiM",
        "construction": "Pi_M flux is closed but G_eff carries time, species, range, radial, or frame dependence",
        "why_it_fails": "measured GM still drifts or gains source/fifth-force residuals",
        "required_repair": "global kappa/G_eff superselection plus no derivative/source/range hair",
        "affected_contracts": "PM7;PM8",
    },
]


GATE_TESTS = [
    {
        "gate": "PiM_projector_algebra_written",
        "pass_condition": "Pi_M is defined by a charge functional and harmonic generator with idempotence and self-adjointness conditions",
        "current_result": "pass_conditional",
        "evidence": "projector identities and PM4 written",
    },
    {
        "gate": "mass_class_not_erased",
        "pass_condition": "ell_M(Pi_M J)=ell_M(J) and ell_M(P_mem J)=0 are explicit",
        "current_result": "pass_conditional",
        "evidence": "charge preservation identity recorded",
    },
    {
        "gate": "flux_closure_not_overclaimed",
        "pass_condition": "d(Pi_M J_H)=0 is not inferred from Pi_M^2=Pi_M",
        "current_result": "pass",
        "evidence": "PM6 and idempotence_claims_closure counterexample",
    },
    {
        "gate": "projector_variation_not_dropped",
        "pass_condition": "delta Pi_M terms are owned or retained",
        "current_result": "pass_policy",
        "evidence": "PM5 and variation ledger written",
    },
    {
        "gate": "parent_boundary_metric_derived",
        "pass_condition": "G_B comes from parent action with Bianchi-safe variation",
        "current_result": "fail",
        "evidence": "G_B remains candidate_not_parent_derived",
    },
    {
        "gate": "mass_flux_closure_parent_derived",
        "pass_condition": "Ward/topological/Euler equation proves d(Pi_M J_H)=0",
        "current_result": "fail",
        "evidence": "PM6 is next target",
    },
    {
        "gate": "measured_GM_parent_derived",
        "pass_condition": "Pi_M charge is closed, absolutely calibrated, and multiplied by constant universal G_eff with zero residuals",
        "current_result": "fail",
        "evidence": "PM6-PM8 and MF/HM rows remain open",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "P8 source-normalization and PPN rows are theorem-zero or empirically scored",
        "current_result": "fail",
        "evidence": "projector algebra checkpoint only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "canonical Pi_M algebra candidate written",
        "status": "pass_conditional",
        "evidence": "Pi_M J=ell_M(J) omega_M plus idempotence/self-adjointness/charge preservation",
    },
    {
        "claim": "P_mem complement made non-cheating",
        "status": "pass_conditional",
        "evidence": "P_mem is legal only as orthogonal complement preserving mass, shear, and matter blocks",
    },
    {
        "claim": "projector-closure overclaim blocked",
        "status": "pass",
        "evidence": "Pi_M^2=Pi_M explicitly separated from d(Pi_M J_H)=0",
    },
    {
        "claim": "projector variation debt exposed",
        "status": "pass",
        "evidence": "delta(Pi_M J)=Pi_M delta J+(delta Pi_M)J ledger written",
    },
    {
        "claim": "Pi_M parent-derived from current corpus",
        "status": "fail",
        "evidence": "boundary symplectic metric and variation remain candidate/open",
    },
    {
        "claim": "mass flux closure parent-derived",
        "status": "fail",
        "evidence": "requires next Ward/topological/Euler mass-channel derivation",
    },
    {
        "claim": "measured GM/Newton/local GR promoted",
        "status": "fail",
        "evidence": "absolute calibration, constant G_eff, zero mu_extra, and second-order source stability remain open",
    },
]


DECISION = [
    {
        "decision": "The Pi_M algebra route is now sharper and non-cheating. A canonical candidate exists: on Sigma_ext ~= S2 x I, define ell_M(J)=int_S2 J, choose normalized omega_M, and set Pi_M J=ell_M(J) omega_M. That gives an idempotent, charge-preserving mass projector if the parent supplies the boundary Hodge/DeWitt metric and owns projector variation. But the decisive Newton equation d(Pi_M J_H)=0 is not derived from projector algebra. It needs a source Ward identity, topological current, or parent Euler equation. Therefore Pi_M is improved from vague closure to exact algebra contract, but measured GM, Newton, PPN, and local GR remain unpromoted.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "why_next": "now that Pi_M algebra is sharp, the next hard equation is d(Pi_M J_H)=0 from Ward/topological/Euler origin",
    },
    {
        "rank": 2,
        "target": "456-PiM-projector-variation-stress-ledger.md",
        "why_next": "metric-dependent Hodge/projector variation must be theorem-zero or retained in R11/source rows",
    },
    {
        "rank": 3,
        "target": "map PM0-PM8 into P8 residual evaluator",
        "why_next": "failed Pi_M algebra/closure rows should activate dln_Meff, radial hair, mu_extra, and source-charge residuals automatically",
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
            "evidence": "Pi_M projector algebra contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 5 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "algebra_objects_written",
            "status": "pass" if len(ALGEBRA_OBJECTS) == 9 else "fail",
            "evidence": f"{len(ALGEBRA_OBJECTS)} algebra objects",
        },
        {
            "gate": "projector_identities_written",
            "status": "pass" if len(PROJECTOR_IDENTITIES) == 7 else "fail",
            "evidence": f"{len(PROJECTOR_IDENTITIES)} projector identities",
        },
        {
            "gate": "variation_ledger_written",
            "status": "pass" if len(VARIATION_LEDGER) == 6 else "fail",
            "evidence": f"{len(VARIATION_LEDGER)} variation ledger rows",
        },
        {
            "gate": "contract_written",
            "status": "pass" if len(CONTRACT) == 9 else "fail",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "flux_closure_not_overclaimed",
            "status": "pass",
            "evidence": "Pi_M idempotence separated from d(Pi_M J_H)=0",
        },
        {
            "gate": "projector_variation_not_dropped",
            "status": "pass",
            "evidence": "delta Pi_M terms retained unless parent-owned",
        },
        {
            "gate": "parent_boundary_metric_derived",
            "status": "fail",
            "evidence": "boundary Hodge/DeWitt metric remains candidate",
        },
        {
            "gate": "PiM_parent_projector_derived",
            "status": "fail",
            "evidence": "projector algebra is conditional on parent G_B and source-space definition",
        },
        {
            "gate": "mass_flux_closure_parent_derived",
            "status": "fail",
            "evidence": "d(Pi_M J_H)=0 requires next Ward/topological/Euler equation",
        },
        {
            "gate": "absolute_calibration_parent_derived",
            "status": "fail",
            "evidence": "PM7 remains not_parent_derived",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "PM6-PM8 plus MF/HM calibration rows remain open",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "Pi_M algebra checkpoint only",
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
    return f"""# 454 - PiM Parent Symplectic Projector Algebra Attempt

Private P8/R1/R4/R7/R9/R10/R11 mass-projector checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 451 made the mass-flux closure route exact but still closure-like: `d(Pi_M J_H)=0` was required, not derived.

Checkpoint 453 cleaned up the separate constant-coupling issue. This checkpoint returns to `Pi_M` itself: can the parent Hodge/DeWitt symplectic route make the mass projector canonical, non-cheating, and variation-owned?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/PiM_parent_symplectic_projector_algebra_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Algebra Objects

{markdown_table(ALGEBRA_OBJECTS)}

## 6. Projector Identities

{markdown_table(PROJECTOR_IDENTITIES)}

## 7. Derivation Steps

{markdown_table(DERIVATION_STEPS)}

## 8. Variation Ledger

{markdown_table(VARIATION_LEDGER)}

## 9. PiM Projector Contract

The Pi_M parent symplectic projector algebra contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 10. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 11. Gate Tests

{markdown_table(GATE_TESTS)}

## 12. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 13. Gate Results

{markdown_table(gate_results)}

## 14. Decision

{DECISION[0]["decision"]}

Practical read: this is a real tightening. `Pi_M` is no longer allowed to be a vague "take the good mass bit" operator. The clean algebra is `Pi_M J=ell_M(J) omega_M`, with charge preservation and orthogonality. But this is not yet Newton. The next equation is still the hard one: prove `d(Pi_M J_H)=0` from Ward/topology/Euler, then calibrate it to measured orbital `GM`.

## 15. Next Queue

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
    write_csv(results_dir / "algebra_objects.csv", ALGEBRA_OBJECTS)
    write_csv(results_dir / "projector_identities.csv", PROJECTOR_IDENTITIES)
    write_csv(results_dir / "derivation_steps.csv", DERIVATION_STEPS)
    write_csv(results_dir / "variation_ledger.csv", VARIATION_LEDGER)
    write_csv(results_dir / "PiM_projector_contract.csv", CONTRACT, CONTRACT_COLUMNS)
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
        "PiM_projector_algebra_written": True,
        "mass_class_preserved_conditionally": True,
        "flux_closure_not_overclaimed": True,
        "projector_variation_not_dropped": True,
        "parent_boundary_metric_derived": False,
        "PiM_parent_projector_derived": False,
        "mass_flux_closure_parent_derived": False,
        "absolute_calibration_parent_derived": False,
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
    parser = argparse.ArgumentParser(description="Write the MTS Pi_M parent symplectic projector algebra attempt.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-170000.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
