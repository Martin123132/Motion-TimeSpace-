# 5182 - Static Hilbert pair projector and constrained Newtonian response

Marker: `MTS_5182_STATIC_HILBERT_PAIR_PROJECTOR_NEWTONIAN_RESPONSE_GATE`.

Date: `2026-07-23`.

## Decision

The actual static Hilbert `h chi chi` vertex has now been calculated and
passed through the two Newtonian-gauge scalar constraints. This closes the
main ambiguity left by checkpoint 5181.

The current shift-symmetric parent has no `R chi^2` vertex, so the
operational improvement coefficient defined below is `eta=0`. Its massless critical pair
therefore couples only to `Phi-Psi`, the gravitational-slip channel. For a
dust source,

```text
Phi=Psi=Phi_GR
```

exactly, independent of the positive pair susceptibility. Tuning the pair
weight to criticality only makes the unused slip constraint singular.

The strongest local curvature extension was also allowed rather than being
dismissed as absent. To avoid importing incompatible curvature or Wick-rotation
signs, define `eta` directly by the linear static vertex
`V_eta=eta k^2(Phi-2Psi)chi^2`. The theorem covers every real `eta`, so its
translation to a source's `xi` convention cannot change the result. On every
GR-connected no-pole branch a passive pair obeys

```text
Phi/Phi_GR
 =1-16 d eta^2/[a-d(48eta^2-16eta+1)]
 <=1.
```

Thus no real `eta` supplies the required extra attractive circular potential.
The passive zero-background pair-dressing route to checkpoint 5148 is
rejected. This is a projector-and-constraint result, not another missing
coefficient.

## 1. Exact static vertex

Use

```text
ds^2=-(1+2Phi)dt^2+(1-2Psi)delta_ij dx^i dx^j.
```

For a canonical static zero mode,

```text
S_chi
 =1/2 integral N sqrt(gamma) gamma^ij partial_i chi partial_j chi,

N sqrt(gamma) gamma^ij
 =sqrt[(1+2Phi)(1-2Psi)] delta^ij
 ={1+(Phi-Psi)-1/2(Phi+Psi)^2+O(h^3)}delta^ij.
```

The linear minimal pair vertex is consequently

```text
V_min=(Phi-Psi) [p.(p+k)]/2.
```

The quadratic term is the seagull

```text
S_seagull=-1/4 integral (Phi+Psi)^2 (grad chi)^2.
```

It contains one scalar tadpole and no two-particle cut. In dimensional
regularization it is scaleless at the critical point; with a mass or state
scale it remains analytic in external momentum and only renormalizes local
coefficients.

For the nonminimal extension,

```text
R^(1)=2 nabla^2(2Psi-Phi)=2 k^2(Phi-2Psi),

V_eta=eta k^2(Phi-2Psi) chi^2.
```

Its second metric variation also multiplies a one-propagator tadpole and
cannot alter the nonanalytic pair term.

## 2. Critical pair polarization

With `M=p.(p+k)` and the checkpoint-5181 massless bubble,

```text
B_0(k)=1/(8|k|),
I_MM=(k^4/4)B_0=|k|^3/32,
k^2 I_M0=-|k|^3/16.
```

The connected metric pair covariance is

```text
C_ab(k)
 =W |k|^3 w_a w_b/64,

w(eta)=(4eta-1, 1-8eta),
```

and the passive Euclidean cumulant gives

```text
Delta K_ab=-C_ab.
```

This matrix is rank one and positive semidefinite before the cumulant sign:

```text
det C=0,
tr[C/(W|k|^3)]=(40eta^2-12eta+1)/32>0.
```

At `eta=0`, `w=(-1,1)` is pure slip. At `eta=1/6`,
`w=(-1/3,-1/3)` is pure common mode. This is an operational static-vertex
statement, not an identification with checkpoint 4951's source coefficient.
The constrained response below shows that the pure-common rotation screens
rather than enhances.

The scalar-slip coefficient at `eta=0` is 32 times the checkpoint-5150 TT
coefficient, providing an independent normalization cross-check.

## 3. Exact scalar-constraint inversion

After all analytic local renormalizations define

```text
a=2 M_R^2 k^2>0,
d=W |k|^3/64>=0.
```

The static Einstein kernel and pair-dressed kernel are

```text
K_GR=a [[0,-1],[-1,1]],

K=K_GR-d w w^T.
```

Their determinant is

```text
det K=-a Delta,

Delta=a-d F(eta),
F(eta)=(4eta-1)(12eta-1)=48eta^2-16eta+1.
```

Continuity from the GR constraint inertia requires `Delta>0`. For a dust
source `J=(rho,0)`, exact inversion gives

```text
Phi/Phi_GR
 =1-16 d eta^2/Delta,

Psi/Psi_GR
 =1+4 d eta(4eta-1)/Delta,

(Phi+Psi)/(Phi+Psi)_GR
 =1-2 d eta/Delta,

(Phi-Psi)/Phi_GR
 =-4 d eta(8eta-1)/Delta.
```

Because `d>=0` and `Delta>0`,

```text
Phi/Phi_GR<=1,
```

with equality only for `d=0` or `eta=0`. This proves the no-enhancement
theorem for every positive scalar dressing of the derived rank-one
projector, not merely for one chosen normalization. Interactions that create
new tensor vertices would be a new parent mechanism and are not silently
covered by this result.

## 4. No-slip and pure-common cases

For nonzero pair weight the dust slip vanishes only at

```text
eta=0 or eta=1/8.
```

The first is exactly invisible to dust. The second gives

```text
Phi/Phi_GR=Psi/Psi_GR=4a/(4a+d)<1.
```

Therefore the only nontrivial no-slip extension is screening.

At the operational pure-common value `eta=1/6`,

```text
w=(-1/3,-1/3),
Delta=a+d/3,

Phi/Phi_GR=(9a-d)/(9a+3d),
Psi/Psi_GR=(9a+d)/(9a+3d),
lensing/GR=3a/(3a+d).
```

The bubble is in the common metric projector, but both the circular
potential and total lensing response are suppressed; a slip is also
generated. Approaching `Delta=0` where it exists is a loss of scalar
constraint rank, not the positive critical Schur residual of checkpoint
5181.

## 5. Parent ownership and gap endpoint

Checkpoint 4951 proved that the exact shift-symmetric parent trajectory has
no additive `R chi^2` source, so the parent-owned operational value is
`eta=0`. Checkpoint 4950 showed that a curvature-pair coefficient becomes an
allowed RG coordinate only after
adding a pair-breaking even potential; that extension did not derive a
viable local/galaxy activation window.

More importantly, the theorem above already grants arbitrary real `eta` and
still rejects attractive enhancement. Parent ownership therefore cannot
reverse this decision inside the audited vertex class.

A finite pair gap has an analytic infrared bubble and cannot produce the
required `1/|k|` carrier. Granting an exact environmental collapse to
`m=0` reaches the endpoint just rejected. The gap mechanism is therefore no
longer the next bottleneck for this route.

## 6. What survives

This checkpoint does not reject:

- the universal local GR/Newton/Maxwell chain;
- checkpoint 5151's direct conserved positive state stress, whose
  source-selected occupation remains to be derived;
- a nonzero parent motion background that creates a genuine linear
  `h-delta chi` Hessian block `B`, rather than a zero-background quadratic
  pair loop.

The next calculation is consequently:

```text
5183:
derive or reject a parent-owned stationary motion background and its
linear metric-motion Hessian; if it does not exist, return to the direct
conserved-state-stress source-selection problem.
```

No local-GR, galaxy, cosmology or full-MTS claim is made. The protected
formalization digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758` and checkpoint 5176
remains `254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`.

## Evidence

- `source-intake/functional_rg/5182/static_Hilbert_vertex_and_seagull_audit.csv`
- `source-intake/functional_rg/5182/critical_pair_scalar_polarization.csv`
- `source-intake/functional_rg/5182/constrained_Newtonian_response_theorem.csv`
- `source-intake/functional_rg/5182/critical_target_and_gap_endpoint_gate.csv`
- `source-intake/functional_rg/5182/nonminimal_coupling_parent_ownership.csv`
- `source-intake/functional_rg/5182/static_pair_route_decision.csv`
- `source-intake/functional_rg/5182/source_provenance.csv`
- `source-intake/functional_rg/5182/static_Hilbert_pair_projector_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5182_VALIDATION.csv`

## Machine decision

`THE_ACTUAL_STATIC_HILBERT_PAIR_VERTEX_HAS_NOW_BEEN_PROJECTED_THROUGH_THE_NEWTONIAN_SCALAR_CONSTRAINTS_THE_CURRENT_SHIFT_SYMMETRIC_PARENT_HAS_ETA_EQUALS_ZERO_SO_THE_CRITICAL_PAIR_COUPLES_ONLY_TO_GRAVITATIONAL_SLIP_AND_IS_EXACTLY_INVISIBLE_TO_A_DUST_SOURCE_ALLOWING_THE_STRONGEST_LOCAL_CURVATURE_IMPROVEMENT_DOES_NOT_RESCUE_THE_ROUTE_BECAUSE_EVERY_POSITIVE_DRESSING_OF_THIS_DERIVED_PAIR_PROJECTOR_ON_THE_GR_CONNECTED_NO_POLE_BRANCH_SATISFIES_PHI_OVER_PHI_GR_LESS_THAN_OR_EQUAL_TO_ONE_THE_ONLY_NONTRIVIAL_NO_SLIP_VALUE_ETA_EQUALS_ONE_EIGHTH_SCREENS_GRAVITY_AND_THE_PURE_COMMON_VALUE_ETA_EQUALS_ONE_SIXTH_ROTATES_THE_BUBBLE_INTO_THE_COMMON_PROJECTOR_BUT_ALSO_SCREENS_THE_NEWTONIAN_AND_LENSING_RESPONSE_LOCAL_SEAGULLS_CANNOT_CHANGE_THE_NONANALYTIC_PAIR_TERM_AND_EVEN_AN_EXACT_GAP_COLLAPSE_REACHES_THIS_REJECTED_ENDPOINT_THEREFORE_PASSIVE_ZERO_BACKGROUND_HILBERT_PAIR_DRESSING_IS_REJECTED_AS_THE_5148_GALAXY_BRIDGE_THE_NEXT_PARENT_CALCULATION_MUST_DERIVE_A_NONZERO_BACKGROUND_LINEAR_METRIC_MOTION_MIXING_OR_SOURCE_SELECT_THE_ALREADY_CONSERVED_DIRECT_STATE_STRESS_WITHOUT_RETUNING`

Summary route rejection:
`True`.
