# 4000 - EM/Poynting Stress Inside Hilbert Source Or Radiative MH Bound

Timestamp: `2026-07-01T19:12:21+00:00`

## Result

The Poynting route is now placed correctly in the local source ladder:

- static/bound EM field stress lives inside `J_H_total` once;
- internal Poynting circulation is allowed and must not be erased;
- only net boundary/radiative/background Poynting flux becomes `Delta_rad_Poynting` source-mass leakage.

## Derivation

Start with the observed Maxwell branch

`S_EM = -(1/(4 mu0)) int sqrt(-g_obs) F_ab F^ab + int A_a J^a`.

Metric variation gives

`T_EM^{ab}=(1/mu0)(F^{a c}F^b_c - (1/4)g_obs^{ab}F_cd F^cd)`.

In a local observed frame, `T_EM^{0i}=S_Poynting^i/c^2`. Therefore the Poynting vector is literally source-current flow. It is not a separate force to bolt on after the Hilbert source has already included EM stress.

The same-action Ward exchange gives

`nabla_a T_EM^{ab}=-F^{bc}J_c`, `nabla_a T_matter^{ab}=+F^{bc}J_c`.

So matter-only source tubes are forbidden. The conserved object is total matter+EM stress.

## Flux Split

The Poynting theorem gives

`dU_EM/dt + int_boundary S_Poynting.n dA = -int_W J.E dV`.

Stationary isolated branch: `time_avg(dU_EM/dt)=0` and `time_avg(int J.E)=0` imply zero net boundary leakage, while internal circulation may remain nonzero.

Radiative/open branch:

`|Delta_rad_Poynting| <= (|Delta U_EM| + |W_matter| + |Phi_external| + |B_improvement|)/(M_H c^2)`.

## Evaluator Results

- `CASE4000_0_static_bound_EM_inside_MH`: status `CONDITIONAL_STATIC_BOUND_BRANCH`, epsilon `0.000000000000e+00`, total_tube=True, once=True, claim=False
- `CASE4000_1_internal_Poynting_circulation`: status `INTERNAL_FLOW_ALLOWED_ZERO_BOUNDARY_FLUX`, epsilon `0.000000000000e+00`, total_tube=True, once=True, claim=False
- `CASE4000_2_radiative_boundary_flux`: status `RADIATIVE_FLUX_RETAINED`, epsilon `4.000000000000e-05`, total_tube=True, once=True, claim=False
- `CASE4000_3_nonminimal_EM_residuals`: status `NONMINIMAL_VECTOR_NONZERO`, epsilon `1.500000000000e-05`, total_tube=True, once=True, claim=False
- `CASE4000_4_matter_only_tube_refused`: status `MATTER_ONLY_SOURCE_TUBE`, epsilon `0.000000000000e+00`, total_tube=False, once=True, claim=False
- `CASE4000_5_double_count_refused`: status `DOUBLE_COUNTS_EM_STRESS`, epsilon `0.000000000000e+00`, total_tube=True, once=False, claim=False
- `CASE4000_6_missing_parent_rows`: status `MISSING_EM_SOURCE_COMPONENT_VECTOR`, epsilon `MISSING`, total_tube=True, once=True, claim=False

## Verdict

This closes a real bookkeeping confusion: Poynting is not ignored and not double-counted. It either sits inside the total Hilbert source for bound/stationary fields, or it is an explicit radiative source-drift residual.

No EM-origin claim follows from this rung. Charge normalization, alpha, unique Maxwell/Hodge owner, nonminimal `F^2`, and readout/radiative regeneration remain live gates.

## Next Target

With EM/Poynting placed, the sharpest remaining local source blocker is the mass projector itself: prove `D_A Pi_M=0` and `[d,Pi_M]J_H=0`, or make the commutator a source-backed residual.

- `4001-Y5-R2FR-parent-projector-constancy-or-PiM-commutator-bound.md`
- `scripts/Y5_R2FR_4001_parent_projector_constancy_or_PiM_commutator_bound.py`

## Source Count

- source needles found: `18/18`
