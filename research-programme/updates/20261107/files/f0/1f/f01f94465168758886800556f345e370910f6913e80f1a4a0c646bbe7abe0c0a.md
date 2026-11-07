# 5197 - Universal gap cross-arena compatibility and route separation

Marker: `MTS_5197_UNIVERSAL_GAP_CROSS_ARENA_ROUTE_SEPARATION`.

Date: `2026-07-24`.

## Decision

The minimal one-pole parent cannot use the same constant elementary motion
mass for both:

1. the checkpoint-5195 homogeneous late-time scalar, and
2. the checkpoint-5152--5176 oscillating massive-dust/FDM galaxy branch.

This is now an explicit theorem rather than a warning. The fitted cosmology
poles are of order `10^-33 eV`; even the weakest particle-population floor
used in the galaxy calculations is of order `10^-23 eV`, and the locked
formation comparator is `10^-20 eV`. Their invariant `J_gap` values and their
required cosmological epochs are disjoint.

That result does **not** reject the current galaxy programme. The current v19
galaxy route is explicitly a collective environmental phase. Its five live
phase scripts contain no `m_gap`, `J_gap`, Compton, pole-mass or particle-mass
parameter. They use the collective coordinate `R/L_eff`, and they explicitly
leave the four-dimensional action, environmental activation, finite boundary
and Hilbert stress underived.

The disciplined route decision is therefore:

```text
retain the checkpoint-5195 one-pole cosmology target;
demote the 10^-20 eV occupied-particle route to a conditional
  separate-component comparator;
do not identify L_eff with 1/m_pole;
derive a parent-owned composite/environmental Hessian and scale map next.
```

No local charge, arena-dependent Newton constant, direct baryon portal or
galaxy-only mass is added.

## 1. Exact one-pole premise

Checkpoint 5196 established the coordinate-free zero-field Hessian

```text
K_psipsi = Z_psi(-Box) + V_eff''(0),
m_pole^2 = V_eff''(0)/Z_psi,
J_gap = G_N m_pole^2.
```

For one elementary field in one fixed local action, `m_pole` is one number.
Changing field normalization does not change it. A different value in a
galaxy is not the same one-pole theory unless a covariant background-dependent
Hessian operator is first derived.

Let the cosmological and galaxy requirements be sets `C` and `G`. A single
constant pole exists only if

```text
C intersect G is nonempty.
```

The current matched cosmology set is

```text
C = {1.095668516985692e-33,
     1.773835953883273e-33} eV.
```

The weakest retained particle-style galaxy population floor is

```text
G_min = 8.882479043701029e-23 eV.
```

Therefore

```text
max(C) < G_min
```

by more than ten orders of magnitude. The intersection is empty.

## 2. Invariant scale comparison

The two checkpoint-5196 branches independently reconstruct

```text
G_N = 6.708832120298927e-57 eV^-2
```

with fractional branch spread `3.375e-16`. This gives:

| use | mass (eV) | `J_gap` | reduced Compton scale |
|---|---:|---:|---:|
| 5195, Lambda free | `1.773835953883273e-33` | `2.110929995508709e-122` | `3605.143 Mpc` |
| 5195, Lambda zero | `1.095668516985692e-33` | `8.053882511735061e-123` | `5836.557 Mpc` |
| 5163 all-patch floor | `8.882479043701029e-23` | `5.293163480041267e-101` | `0.071995 pc` |
| 5152 `0.1 R_n` WKB floor | `2.816691662155760e-21` | `5.322620971308338e-98` | `0.002270 pc` |
| 5152 equality `100 kpc` floor | `4.832363418098892e-21` | `1.566628779140364e-97` | `0.001323 pc` |
| 5176 locked comparator | `1.000000000000000e-20` | `6.708832120298927e-97` | `0.0006395 pc` |

For the locked `10^-20 eV` comparator, the exact separations are:

```text
Lambda-free cosmology:
  mass ratio = 5.637499892877945e12,
  mass separation = 12.7510865466 decades,
  J_gap ratio = 3.178140504219884e25,
  J_gap separation = 25.5021730933 decades;

Lambda=0 cosmology:
  mass ratio = 9.126847988213744e12,
  mass separation = 12.9603208172 decades,
  J_gap ratio = 8.329935419996127e25,
  J_gap separation = 25.9206416344 decades.
```

The identity

```text
J_galaxy/J_cosmology = (m_galaxy/m_cosmology)^2
```

is reproduced to below `5e-16` fractional residual in every comparison.
Consequently this is not a units or field-normalization mismatch.

## 3. Opposite epoch requirements

The checkpoint-5152 background rows give one consistent equality scale,

```text
H_eq = 2.3629115213047323e-28 eV.
```

The fitted cosmology poles obey

```text
m_pole/H_eq =
  7.506993e-6  for Lambda free,
  4.636943e-6  for Lambda=0.
```

They therefore have not begun rapid quadratic oscillation by equality. Their
present ratios are instead

```text
m_pole/H0 = 1.232099124744752,
m_pole/H0 = 0.7638680134687456.
```

That order-`H0` scale is precisely what permits late-time thawing.

The particle-style galaxy values have the opposite behavior:

```text
2.816691662155760e-21 eV / H_eq = 1.192e7,
4.832363418098892e-21 eV / H_eq = 2.045e7,
1e-20 eV / H_eq                 = 4.232e7.
```

They can be deeply oscillatory and dust-like by equality, but they satisfy
`m/H0` of order `10^12--10^13`; the same quadratic mode cannot then be an
order-`H0` thawing component.

Thus the contradiction is twofold:

```text
numerical pole value: incompatible;
required dynamical epoch: incompatible.
```

It cannot be repaired by changing the homogeneous amplitude, covariance or
field coordinate.

## 4. What the old particle branch actually established

The parent record does not justify calling `10^-20 eV` a measured MTS mass:

- Checkpoint 5152 called it an intentionally conservative internal benchmark.
  Its WKB and Jeans values were engineering floors, not fitted masses.
- Checkpoint 5163 used a weaker floor to make the canonical wave-pressure
  rejection conservative; it did not select a mass.
- Checkpoint 5174 explicitly found no stable monotone mass bound after the
  spherical-cutoff control.
- Checkpoint 5176 ended in a twelve-seed statistical draw or metric split.
- Checkpoint 5177 rejected a constant amplitude repair.
- Checkpoints 5178--5185 rejected the controlled Gaussian, weak-interaction,
  passive-pair and stationary-background repairs as independent order-one
  stress owners.
- Checkpoint 5186 proved that the free FLRW parent does not generate the
  required abundance; the occupied branch survives only as a conditional
  initial state.

These calculations remain useful. They show what an additional massive
component would do and which mechanisms fail. They are not erased. They are
reclassified as a conditional extension rather than the owner of the one-pole
MTS unification.

## 5. Why the current galaxy route is different

The current read-only galaxy sources are:

```text
D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\scripts\mts_phase_flow_closure.py
D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\scripts\mts_self_similar_phase_disk.py
D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\scripts\mts_phase_lensing_gate.py
D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\scripts\mts_nonanalytic_phase.py
D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\scripts\mts_axisymmetric_phase.py
```

Their shared candidate structure is collective:

```text
u = ln(R/L_eff),
dn/du = q n(1-n),
db/du = -s b(1-b),
Sigma_chi = (Gamma0/G) n b/(2 pi R/L_eff).
```

The source itself states that this is not a particle dark-disk fit. It also
sets all of the decisive ownership flags to false:

```text
covariantFourDimensionalActionDerived = false,
environmentalBoundaryDerived = false,
stressTensorDerived = false,
phaseActivationDerived = false,
phaseBoundaryDerived = false,
phaseStressTensorDerivedFromAction = false.
```

`L_eff` is therefore a similarity/domain scale, not an elementary pole.
Writing

```text
m_pole = hbar/(c L_eff)
```

without a parent dispersion relation would silently turn a galaxy-dependent
environmental length into an arena-dependent elementary mass. That is
forbidden by the checkpoint-5196 invariant-pole theorem.

The allowed constructive possibility is instead

```text
elementary Hessian:
  Gamma_psi_psi^(2) -> one universal cosmological m_pole;

composite/environmental Hessian:
  Gamma_chi_chi^(2)[state, environment] -> collective gap/domain scale.
```

These are different operators. A composite eigenvalue can soften or reach a
critical endpoint without changing the elementary vacuum pole, but only if the
actual parent 2PI/Bethe--Salpeter problem derives it.

## 6. Route arbitration

The options now have explicit costs:

1. **One pole for both old roles:** rejected by the disjoint mass and epoch
   theorem.
2. **One elementary pole plus a collective environmental phase:** selected
   derivation route. It adds no second elementary mass, but must derive the
   collective Hessian, state, activation, wall and stress tensor.
3. **Second elementary field/pole:** mathematically consistent but adds a
   field, a mass calibration and state preparation. It is not the current
   minimal parent.
4. **Environment-dependent elementary pole:** open only if a covariant parent
   operator produces the running while preserving stability and local GR.
   Per-arena numerical retuning is not acceptable.
5. **Gapless critical composite pair:** kinematically open after checkpoint
   5181, but its normalization, state, logistic filter and tensor projection
   are not parent-owned.

The minimal and most MTS-faithful option is number 2.

## 7. Next derivation

Checkpoint 5198 should not run another mass scan. It should construct or reject
the parent-owned collective eigenproblem:

```text
1. define chi as a reflection-even composite motion/stress operator;
2. derive Gamma_chi_chi^(2) from the existing parent 2PI/CTP action;
3. evaluate its vacuum and environmental stationary backgrounds;
4. prove chi=0 and a positive gap on the local invariant vacuum;
5. test whether one environmental eigenvalue can soften without changing
   m_pole or G_N;
6. derive, rather than insert, the radial occupation n, anti-wall b, L_eff
   map and Hilbert stress;
7. reject the route if positivity, Ward conservation, local silence or the
   phase-flow reduction fails.
```

This is the forward leap fixed by 5197. It addresses the actual current galaxy
mechanism rather than continuing to tune a particle mass that the current
galaxy route no longer contains.

## Claim boundary

```text
one-pole 5195 plus massive-dust 5152-5176 identification = rejected;
old occupied-particle calculations erased                   = no;
current collective galaxy phase rejected                   = no;
L_eff-to-J_gap map derived                                  = no;
composite environmental Hessian derived                     = no;
local GR/Newton/Maxwell branch modified                     = no;
galaxy claim                                                = false;
cosmology support claim                                     = false;
full MTS claim                                              = false.
```

Artifacts:

```text
script:
  scripts/Y5_R2FR_5197_universal_gap_cross_arena_compatibility.py
outputs:
  source-intake/functional_rg/5197/
validation:
  source-intake/mts_residuals/P8_Y5_BRR545_5197_VALIDATION.csv
```

No GitHub action is part of this checkpoint. The galaxy repository is
read-only, and `formalization-workbench` remains protected.
