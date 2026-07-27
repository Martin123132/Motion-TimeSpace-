# 5190 — Static Ward helicity, one-derivative mixing no-go, and direct-state route freeze

Marker: `MTS_5190_STATIC_WARD_HELICITY_AND_MIXING_NO_GO`

**Verdict:** The 5148 propagator-enhancement target is mathematically healthy
as an abstract nonlocal response, but the current selected zero-background
scalar/coframe operators cannot generate its required mixing. This is now a
theorem rather than another missing coefficient. Static stress conservation
and isotropy block Poynting from the scalar sector, while local scalar
derivative counting puts the parent massless pair two powers away from the
target. The passive scalar-pair and stationary-Poynting routes are closed.
The direct conserved motion-state stress remains viable, but only
conditionally until its state preparation and formation law are derived.

The theorem is scoped to nonzero spatial momentum, zero frequency, a regular
DC limit, local contact subtraction, and the homogeneous/isotropic,
parity-even, local diffeomorphism-invariant scalar sector. It does not reject
a parent-derived direct state, an independent vector background, or genuinely
active/nonlocal dynamics.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Why this is not a repeat of 5150–5183

The prior chain already established:

```text
B_0(k)=1/(8|k|)                         critical pair carrier;
Delta K_TT=-W_state |k|^3/2048          minimal passive TT sign;
w(eta=0)=(-1,1)                         minimal pair is pure slip;
pair/K_GR proportional x n_q(x)         local pair relative shape;
target proportional n_q(x)/x            5148 required shape;
pair/target=x^2                         exact mismatch.
```

Checkpoint 5181 also constructed a positive, passive generalized-field
Hessian that gives the target exactly. The unresolved question was whether
the current parent can own its cross block. Checkpoint 5190 answers that
question.

## 2. Exact static Ward decomposition

Take nonzero Fourier momentum along `z` and subtract local contact/seagull
terms from the connected nonanalytic kernel:

```text
k_mu=(0,0,0,k),    k!=0,
k_mu Delta T^mu_nu=0.
```

The exact rank-four Ward system gives

```text
T03=T13=T23=T33=0.
```

The original ten symmetric stress components therefore leave six:

```text
helicity 0: rho=T00, tau=(T11+T22)/2;
helicity 1: P_x=T01, P_y=T02;
helicity 2: T_plus=(T11-T22)/2, T_cross=T12.
```

The Ward matrix has rank `4` and nullity
`6`.

## 3. Exact isotropic covariance theorem

In basis `(rho,tau,Px,Py,Tplus,Tcross)`, solve

```text
[G_SO(2),C]=0
```

for a symmetric `6 x 6` covariance. The executed `21`-variable system has
rank `16` and solution dimension
`5`:

```text
C = diag-block(C_scalar[2x2], C_vector I_2, C_tensor I_2).
```

All scalar-vector, scalar-tensor and vector-tensor cross blocks vanish.
The scalar Newtonian metric vertex is

```text
-Phi*T00 - Psi*T11 - Psi*T22.
```

Thus a transverse Poynting fluctuation is not a hidden scalar response.

## 4. The derivative-counting theorem

Let a critical collective susceptibility scale as

```text
G_chi(k)~|k|^-alpha
```

and its unnormalized metric mixing as `B_hchi~|k|^d`. Since
`K_GR~M_R^2 k^2`, its Schur correction relative to Einstein scales as

```text
(B_hchi G_chi B_chih)/K_GR
  ~ |k|^(2d-alpha-2).
```

The 5148 target has exponent `-1`. For the parent pair `alpha=1`, this
requires

```text
d=1.
```

But every nonzero local critical scalar metric vertex in the current parent
starts at two derivatives:

```text
kinetic Hilbert vertex h (partial psi)^2: d=2;
curvature improvement R psi^2:            d=2;
```

so its relative response scales as `|k| n_q`, not `n_q/|k|`. A
zero-derivative `sqrt(-g)m^2 psi^2` vertex is proportional to the gap and
vanishes at the massless pair point; retaining it restores a finite gap and
an analytic bubble.

The abstract 5181 completion makes the issue transparent. Its normalized
metric variable is `u=sqrt(K_h)h`, and

```text
B_uchi=sqrt(A)
=> B_hchi=sqrt(A K_h)~sqrt(A) M_R |k|.
```

It requires precisely the missing one-spatial-derivative scalar mixing.

## 5. Why a local equilibrium critical scalar does not repair `d=2`

For a unitary local three-dimensional critical scalar primary,

```text
G_O(k)~k^(2 Delta-3),    Delta>=1/2,
```

so its singularity satisfies `alpha<=2`. A two-derivative metric vertex
would need

```text
alpha=3
```

to reproduce the target. Therefore the escape is unavailable inside that
local equilibrium class. This clause does not cover an active,
nonequilibrium or explicitly nonlocal CTP state; such a state would be new
parent dynamics and must prove its own passivity and stability.

## 6. Poynting-vector escape tested exactly

At finite frequency, the longitudinal Ward identity gives

```text
T_L^0=(omega/k)T00.
```

It vanishes in a regular DC limit. The surviving electromagnetic Poynting
components are transverse:

```text
k_i P_T^i=0.
```

The apparent one-derivative scalar `a_i P^i`, with
`a_i~partial_i Phi`, consequently vanishes:

```text
a_i P_T^i proportional k_i P_T^i=0.
```

SO(2) invariance independently gives zero scalar-vector covariance. A
singular noncommuting `omega->0` limit must retain the conserved density and
its Ward partners, reducing to a full hydrodynamic/Vlasov or new active-state
problem—not a Poynting-only patch.

An independent longitudinal vector can support `a_i V^i`, but this is the
unit-flow/aether correspondence extension. It adds preferred-flow modes and
requires microscopic Kubo ownership plus PPN and stability gates. It is not
present in the selected metric-only local parent.

The Maxwell conclusion remains positive:

```text
T_EM^0i=(E cross B)^i
```

is a real same-coframe vector/gravitomagnetic source. It simply is not the
stationary common-scalar galaxy kernel.

## 7. Route arbitration

```text
local gapped vacuum:
  rejected for C_q; analytic in k^2.

minimal passive scalar pair:
  rejected; pure slip at parent eta=0, wrong TT sign, wrong k shape.

nonminimal R psi^2 pair:
  not parent-owned and still two powers too soft.

controlled X2/X3 interactions:
  Ward-correct but far too small; regular clustering cannot create |k|.

stationary Poynting:
  exact helicity-one source; rejected as scalar kernel.

free Vlasov response:
  already evolved and must not be double counted; frozen response failed
  to close the required radial hierarchy.

5181 abstract nonlocal completion:
  positive and causal, but its d=1 cross block is not generated by the
  current parent.

direct conserved state stress:
  survives conditionally; stress map derived, state selection not derived.
```

The current-parent propagator-enhancement verdict is therefore
`False`.

## 8. Propagator response is not direct state stress

The two equations are

```text
Schur response:  (K_GR-Sigma)h=J_visible;
direct state:     K_GR h=J_visible+J_state.
```

They become equivalent only after deriving
`J_state[h,J_visible]` and integrating out the state without double
counting. Checkpoint 5171 already calculates the frozen Vlasov response, so
it cannot be added again as a new kernel.

The direct 5151 state is useful because a positive conserved,
nonrelativistic state sources rotation and lensing through the same Einstein
metric while leaving the local unoccupied `psi=0` branch intact. But until
the parent selects its occupation, transition, core and edge, it is a
conditional matter-state pillar rather than a derived modification of
gravity.

## 9. Consequence for the unified programme

This closes a loop that should not be run again:

```text
do not retry the passive zero-background scalar pair;
do not retry stationary Poynting as a scalar response;
do not multiply the failed Vlasov response by a fitted constant;
do not call the abstract 5181 cross block parent-derived.
```

There are now two honest forward choices:

1. derive the direct motion-state preparation and nonlinear formation law
   with one cross-arena parameter set; or
2. introduce only through an actual parent derivation a nonlocal/active
   collective mode that supplies the missing `d=1` cross block and passes
   Ward, slip, TT, passivity and local-vacuum gates.

Because the separate galaxy programme already owns nonlinear formation,
the next unified-framework calculation should return to the other newly
exposed root gate: determine whether the cosmological
`c_O4 C^2 X` tensor Hessian is degenerate/redundant or only an
order-reduced EFT correction.

## 10. Claim boundary

Established:

```text
static Ward rank/nullity                 = 4/6;
static helicity dimensions               = 2 scalar +2 vector +2 tensor;
isotropic cross-helicity covariance      = zero;
regular DC longitudinal Poynting         = zero;
transverse Poynting scalar contraction   = zero;
pair local-mixing derivative order       = 2;
target-required derivative order         = 1;
pair/target shape ratio                  = x^2;
current-parent propagator route          = rejected;
direct conserved state route             = conditional survivor.
```

Not established:

```text
parent direct-state preparation or formation;
new nonlocal/active d=1 collective mode;
galaxy claim;
all-scale cosmological O4 tensor safety;
full MTS unification.
```

## 11. Machine artifacts

- `source-intake/functional_rg/5190/static_Ward_constraint_and_helicity_decomposition.csv`
- `source-intake/functional_rg/5190/SO2_invariant_stress_covariance.csv`
- `source-intake/functional_rg/5190/local_scalar_mixing_power_count.csv`
- `source-intake/functional_rg/5190/Poynting_and_unit_flow_escape_gate.csv`
- `source-intake/functional_rg/5190/occupied_state_route_arbitration.csv`
- `source-intake/functional_rg/5190/direct_state_vs_propagator_response.csv`
- `source-intake/functional_rg/5190/source_provenance.csv`
- `source-intake/functional_rg/5190/static_Ward_and_mixing_no_go_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5190_VALIDATION.csv`
