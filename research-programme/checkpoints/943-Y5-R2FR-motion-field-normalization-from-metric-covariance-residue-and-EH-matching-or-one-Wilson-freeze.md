# 4927 - Motion normalization, covariance residue and all-mass loop gate

Marker: `MTS_MOTION_NORMALIZATION_COVARIANCE_RESIDUE_4927`.

**Decision:** the attempted `C_N` determination produces a stronger result
than another fitted normalization. `C_N=M_N/M_Pl` is not a physical parameter:
it labels the unobservable normalization of the old motion-field coordinate.
The invariant quantities are

```text
g_psi=lambda_old M_N^(-1/3),
B_psi=B_old M_N,
mu=g_psi^(3/8),
M_R^2.
```

The old additive covariance map also needs correction. With the field
dimensions derived at checkpoint 4926, neither the original coefficient one
nor checkpoint 4872's `ell_*^2` makes the gradient covariance dimensionless.
The canonical coefficient must have mass dimension `-4`.

The Einstein residue cannot fix `C_N`: every old-coordinate stress vertex
contributes `M_N^-1`, every scalar propagator contributes `M_N`, and the factors
cancel in every closed stress correlator. The active integrated-`H` parent also
does not identify its public metric with the rejected scalar-only composite
metric.

A second exact result removes the physical gap `mu` as a **local loop-safety**
blocker. The complete massive-scalar Weyl form factor obeys

```text
-1/60 <= d k_W/d ln(q^2/m^2) <= 0
```

for every mass. Heavy, crossover and massless regimes can therefore be joined
without ever extrapolating `1/m^2` to zero mass. Across all displayed local
arena pairs the one-real-scalar metric transfer remains tiny; even the
deliberately extreme AU-to-nuclear unit-weight Newton envelope is only
`2.51e-39`.

This closes the motion-field normalization as a local-GR obstruction. It does
not predict the invariant motion gap, scalar state or abundance, and it does
not derive the finite integrated-metric/QCD Weyl-cubic boundary. Compact and
full MTS-to-GR claims remain unpromoted.

## 1. The covariance map must be dimensionally repaired

The core corpus wrote

```text
g_mn=eta_mn+<partial_m phi partial_n phi>.
```

Checkpoint 4872 replaced the raw moment by a connected moment and inserted
`ell_*^2`. Checkpoint 4926 now fixes the relevant dimensions. For the old field,

```text
[phi_old]=3/2,
[partial phi_old partial phi_old]=5.
```

Consequently a dimensionless metric perturbation needs

```text
C_old^mn
 =B_old <partial^m phi_old partial^n phi_old>_c,

[B_old]=-5.
```

Coefficient one gives dimension five; `ell_*^2` gives dimension three. Neither
is a metric term.

After canonicalization,

```text
psi=phi_old/sqrt(M_N),
[psi]=1,
[partial psi partial psi]=4,
```

and the same covariance is

```text
C^mn
 =B_psi <partial^m psi partial^n psi>_c,

B_psi=B_old M_N,
[B_psi]=-4.
```

It may be written as `B_psi=L_C^4` or
`B_psi=zeta_B Lambda_UV^-4`. The latter is dimensionally allowed but does not
derive `zeta_B`, the state covariance or equality between the covariance scale
and the regulator cutoff.

This supersedes one specific part of checkpoints 4872--4873:

```text
C=ell_*^2 <partial psi partial psi>_c,
Lambda_UV=ell_*^-1
```

cannot use the same `ell_*` after the canonical dimension audit. The generic
induced-Einstein formula in terms of an independently defined `Lambda_UV`
remains valid. The integrated-`H` branch selected at 4875 is unaffected because
its public metric is reconstructed from an independent principal density, not
from this additive covariance.

## 2. Exact field-coordinate orbit

Let the old field coordinate be changed by a positive constant,

```text
phi_old' = s phi_old.
```

Preserving the old action and covariance form requires

```text
M_N'       =s^2 M_N,
lambda_old'=s^(2/3) lambda_old,
B_old'     =s^-2 B_old.
```

Therefore

```text
g_psi'
 =lambda_old'(M_N')^(-1/3)
 =g_psi,

B_psi'
 =B_old'M_N'
 =B_psi.
```

The executable orbit varies `s` from `0.01` to `100`; `M_N` moves by eight
orders while both invariants remain fixed below `9e-16` numerical error.

In logarithmic variables the observable map is

```text
ln g_psi =-(1/3)ln M_N+ln lambda_old,
ln B_psi =ln M_N+ln B_old.
```

Its exact field-coordinate null vector is

```text
(delta ln M_N,delta ln lambda_old,delta ln B_old)
 =(3,1,-3) epsilon.
```

Thus `C_N=M_N/M_Pl` changes along a redundancy orbit. It must be removed from
the physical variable table rather than “derived” by choosing one coordinate.

## 3. Stress-residue cancellation theorem

The quadratic old-coordinate action is

```text
S_2[phi_old]
 =1/(2M_N) integral (partial phi_old)^2.
```

Its propagator is proportional to `M_N`. The Hilbert tensor obtained from the
same action is proportional to `M_N^-1`. A closed scalar loop with `n` stress
insertions therefore scales as

```text
(M_N^-1)^n (M_N)^n=1.
```

The generator verifies this at two, three and four stress insertions across
`M_N={1e-12,1,1e12}`. Interactions do not restore `M_N`: after canonicalization
they depend on the invariant `g_psi`.

This proves that neither the stress two-point coefficient, the induced
Einstein term nor the stress three-point Weyl-cubic threshold can determine
the old field-coordinate normalization. They can determine physical pole
count, `g_psi`, masses and invariant Wilson coefficients.

The result mirrors checkpoint 4915's graviton-normalization theorem: an
arbitrary intermediate field normalization cancels between kinetic residue and
source vertices. Here the same cancellation occurs in the microscopic scalar
coordinate.

## 4. Why the Einstein residue cannot fix `C_N`

The active two-derivative matching equation is

```text
M_R^2
 =M_EH,boundary^2
  +W1 Lambda_UV^2/(96pi^2)
  +Delta M_threshold^2
  +Delta M_H+ghost^2.
```

`W1` depends on physical species and curvature couplings, not wavefunction
normalization. The calibrated `M_R` constrains one renormalized sum.

Combine

```text
x=(ln M_N,ln lambda_old,ln B_old,
   y_boundary,y_loop,y_threshold)
```

with the invariant observations

```text
u=(ln g_psi,ln B_psi,M_R^2).
```

The Jacobian is

```text
[-1/3, 1, 0, 0, 0, 0]
[ 1,   0, 1, 0, 0, 0]
[ 0,   0, 0, 1, 1, 1].
```

It has rank three and nullity three. The executable null vectors are

```text
(3,1,-3,0,0,0),
(0,0,0,1,-1,0),
(0,0,0,1,0,-1).
```

The first is the field-coordinate orbit. The others are the already-proved
Einstein boundary/loop/threshold non-identifiability. No algebraic inversion of
measured `G_N` can select `C_N`.

Three tempting alternatives fail cleanly:

1. identifying the public graviton with the old scalar covariance revives the
   fixed-background scalar-only composite branch rejected at 4875;
2. setting `B_psi=Lambda_UV^-4` and imposing pure induced gravity adds
   `zeta_B`, regulator, spectrum and zero-boundary assumptions, and still fixes
   only `B_old M_N`;
3. declaring the omitted coefficient one chooses a field coordinate with the
   wrong dimensions rather than deriving an observable.

The correct decision is

```text
C_N                         = redundant coordinate, removed;
g_psi or mu                 = physical scalar-sector matching data;
B_psi                       = physical historical covariance-map data;
M_R                         = independent calibrated integrated-H residue.
```

## 5. Exact massive Weyl-form-factor theorem

The locked primary source gives, for Euclidean

```text
u=q^2/m^2,
a^2=4u/(u+4),
A=1-(1/a)ln[(2+a)/(2-a)],

k_W(u)=8A/(15a^4)+2/(45a^2)+1/150.
```

This is exact in derivatives at quadratic order in curvature. Define

```text
x=a/2=sqrt[u/(u+4)],
0<=x<1.
```

Direct differentiation and expansion of `atanh(x)` gives

```text
d k_W/d ln u
 =-sum_(n>=1)
   x^(2n)/[6(2n+3)(2n+5)].
```

Every summand is nonnegative. At `x=1`,

```text
sum_(n>=1) 1/[6(2n+3)(2n+5)]
 =1/60
```

by telescoping. Hence the exact all-mass inequality is

```text
-1/60 <= d k_W/d ln u <=0.
```

For two arena momenta `q_h>q_l`, the scalar mass cancels from their ratio and

```text
abs[k_W(q_h^2/m^2)-k_W(q_l^2/m^2)]
 <=ln(q_h^2/q_l^2)/60
 =ln(q_h/q_l)/30.
```

The inequality includes the limits

```text
k_W=-q^2/(840m^2)+O(q^4/m^4)  for q<<m,
```

and the massless logarithmic slope. It therefore joins decoupling, crossover
and light regimes without a guessed interpolation.

The source's exact Eq. 95 expands to the `1/60` logarithmic slope used here and
reproduces checkpoint 4877's scalar heat-kernel transfer. The executable
calculation uses the exact formula rather than relying on an isolated printed
asymptotic coefficient.

## 6. Cross-arena metric bound independent of `mu`

In the `a_C C^2` convention used at checkpoint 4876, the scalar finite form
factor contributes

```text
a_C,nl=k_W/(64pi^2).
```

The spin-two inverse-propagator correction is `4a_C q^2/M_R^2`. Therefore the
exact slope theorem gives

```text
abs(delta epsilon_2)
 <=q_h^2 ln(q_h/q_l)/(480pi^2 M_R^2)
```

per real scalar. This is precisely the conservative massless transfer used in
checkpoint 4877, now proved to bound every scalar mass in the Weyl channel.

The script evaluates 405 exact form-factor rows over

```text
10^-20 <=m/q_h<=10^20
```

for five arena pairs. Every row satisfies the analytic bound; the largest
floating-point ratio is `1+2e-16`, reached in the massless asymptote.

Representative one-real-scalar envelopes are

| transfer | spin-2 | minimal spin-0 envelope | conservative unit-weight Newton envelope |
|---|---:|---:|---:|
| GW250114 to 12 km NS | `2.06e-80` | `1.03e-79` | `6.18e-79` |
| 1 AU to R10 50 micrometres | `1.98e-62` | `9.88e-62` | `5.93e-61` |
| 1 AU to one Angstrom | `6.76e-51` | `3.38e-50` | `2.03e-49` |
| 1 AU to one femtometre | `8.35e-41` | `4.18e-40` | `2.51e-39` |

The spin-zero and inverse-Newton columns deliberately use the larger
source-backed massless/minimal or unit-weight envelopes from checkpoint 4877
and the locked four-dimensional decoupling paper. They are not advertised as
new exact `k_R` formulas. Massive thresholds decouple quadratically.

Even the final deliberately extreme hierarchy would need approximately
`4.0e36` equal real scalar contributions to reach one percent in the largest
displayed envelope. A one/few-pole MTS scalar is therefore safe for every
possible mass as a loop correction to local gravity.

## 7. Complete mass-domain routing

The motion scalar now has a non-overlapping rule:

```text
m>=10Q:
    use the local heavy threshold;

0.1Q<m<10Q:
    use exact k_W(u), never 1/m^2;

m<=0.1Q including m=0:
    use the renormalized nonlocal logarithm and cross-scale running.
```

This resolves the apparent `C_N` compact floor. That floor was the condition
for applying the **heavy local C3 approximation**, not a statement that a
lighter scalar destroys local GR. Once the exact crossover and massless
domains are included, no physical divergence occurs.

The conclusion has finite-multiplicity scope. It does not cover an unbounded
tower, a macroscopic coherent scalar background, an independently large local
counterterm, or a nonperturbative scalar abundance. Those are distinct parent
or state questions.

## 8. GR, Newton and Maxwell consequences

On the selected integrated-`H` baseline,

```text
M_R^2(G_mn+Lambda g_mn)=T_mn^total,
G_N=(8pi M_R^2)^-1.
```

Replacing `phi_old` by canonical `psi` is a field redefinition inside the same
matter action. It cannot change:

- the Hilbert source coefficient;
- the universal soft-graviton coupling;
- the Newton/Poisson normalization;
- Maxwell's Hilbert stress;
- `T_EM^(0i)=(E cross B)^i`, the Poynting momentum source.

The new all-mass form-factor bound also shows that motion-scalar loop running
cannot produce observable species, frame, clock or Maxwell leakage at any
displayed local scale for finite ordinary multiplicity.

Thus

```text
motion old-field normalization       = removed as redundant;
motion-loop mass uncertainty         = removed as local-GR blocker;
weak GR/Newton/Maxwell source chain   = retained;
physical invariant motion gap        = still unpredicted;
finite H/QCD Weyl-cubic remainder     = still one open a_IR;
compact and full MTS-to-GR            = not promoted.
```

## 9. Next route

Because `mu` no longer controls local loop safety, the priority returns to the
actual compact-GR obstruction:

`4928-Y5-R2FR-integrated-H-C3-functional-flow-boundary-or-observational-Wilson-freeze.md`.

It should calculate the selected integrated-`H` functional flow of the
dimensionless Weyl-cubic coupling far enough to decide whether its ultraviolet
direction is irrelevant and fixes the finite boundary. If the actual MTS flow
cannot be closed, it should finish the one-parameter observational Wilson
freeze without reopening microscopic provenance labels as extra fit
parameters.

The invariant scalar gap remains a particle/cosmology derivation target, not a
local-GR prerequisite.

No GitHub action is authorized.

## Sources

- `post-checkpoint-work/source-intake/nonlocal_form_factors/4927/PROVENANCE.md`.
- `core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md`.
- `post-checkpoint-work/4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md`.
- `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`.
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`.
- `post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md`.
- `post-checkpoint-work/4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md`.
- `post-checkpoint-work/4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md`.
- `post-checkpoint-work/4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-normalization-or-low-energy-Wilson-posterior.md`.
- `post-checkpoint-work/scripts/Y5_R2FR_4927_motion_normalization_covariance_residue.py`.
