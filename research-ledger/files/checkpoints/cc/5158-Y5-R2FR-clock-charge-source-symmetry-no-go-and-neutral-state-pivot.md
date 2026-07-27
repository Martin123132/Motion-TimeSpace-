# 5158 - Clock-charge source symmetry no-go and neutral-state pivot

Marker: `MTS_5158_CLOCK_CHARGE_SOURCE_SYMMETRY_NO_GO_NEUTRAL_STATE_PIVOT`.

Date: `2026-07-20`.

## Decision

Checkpoint 5157 did not leave charge generation as a paper target. This
checkpoint searches the existing pair, gravity, memory, open-bath and
`X2/X3` vertices for an actual source. The result is negative and sharp:
there is no regular parent-owned operator in the current corpus that evolves
zero signed internal clock charge into the macroscopic charged condensate.

The checkpoint-4890 pair remains a valid representation of an **already
precharged** sector. It is not a state-preparation mechanism. The least
additive active route is therefore the existing neutral real-scalar motion
state, with one global state calibration and an explicitly conditional
one-clock adiabatic law, followed now by the no-refit collapse test.

## 1. General symmetry theorem

For `theta=m_X U`, the relevant polar action is

```text
L=-[(grad A)^2+A^2((grad theta)^2+m_X^2)]/2
  +kappa_mix grad(phi).grad(theta).
```

It contains no undifferentiated `theta`. The exact Noether current obtained
symbolically is

```text
j_theta=-A**2*dtheta + dphi*kappa,
div j_theta=0
```

for the closed reversible sector. The phase-shift derivative is exactly
`0`. Gravity, curvature dressing and
CP-even derivative self-interactions do not change this conclusion when they
are completed as an `O(2)_X` doublet.

Consequently a neutral source can create only charge-balanced pairs. The
executed charge sum is
`(+1)+(-1)=0`. Gravitational particle
production may populate energy and total occupation, but it cannot orient the
macroscopic phase clock.

## 2. Why the old clock-memory mixing does not rescue it

The checkpoint-4890 microscopic mixing is

```text
L_mix proportional grad(phi).
 (X_1 grad X_2-X_2 grad X_1)/(X_1^2+X_2^2).
```

For `A>0` this reduces to `kappa_mix grad(phi).grad(theta)` and modifies the
conserved current. It is independent of `A`, so its amplitude derivative is
exactly `0`. The amplitude equation is
homogeneous and its `A=0` residual is
`0`. It can redistribute current on an
already occupied polar chart; it does not nucleate the amplitude.

At `A=0` its Cartesian denominator vanishes. This gives a strict dichotomy:

1. a regular Cartesian completion vanishes sufficiently fast at the origin,
   preserving the no-source result; or
2. the singular expression is not an admissible local parent at the exact
   GR vacuum.

Neither branch supplies a regular vacuum-to-clock transition.

## 3. Open bath and number-changing routes

The Schwinger--Keldysh clock equation permits subsystem exchange,

```text
div j_pair=-div j_bath=Q_SK,
```

but the closed total current is still conserved. Generating signed pair charge
requires the bath to carry the opposite signed charge and requires its state
to choose the asymmetry. No such signed bath-charge row exists, and checkpoints
4895--4896 retired the full bath cosmology after its reciprocal stress changed
the early gravitational normalization. It cannot be revived as an unnamed
charge reservoir.

The checkpoints 4952--4959 do derive neutral gravitational pair production
and real-scalar `2<->4`/finite-time number-changing channels. They are CP-even
and own total occupation, not an oriented `O(2)_X` charge. Complexifying those
results would require a new doublet flow and would still preserve net charge
unless an explicit asymmetric operator and state were added.

A direct linear tadpole could create an amplitude, but it breaks the
reflection/O(2) selection rule and reopens the local one-scalar source that
checkpoint 4947 removed. A chemical-potential current can bias a state at
fixed charge but cannot create charge in a closed system. Neither is an
existing safe solution.

## 4. What survives

Two state branches remain mathematically honest:

```text
precharged complex pair:
  exact WKB clock + exact conserved charge;
  Q_X is one global boundary datum, not dynamically derived;

neutral real scalar / neutral pair gas:
  current active parent and Schrodinger--Poisson limit retained;
  total frozen number can obey the 5157 charge/entropy-style
  one-clock adiabatic theorem after production;
  no unique internal phase clock is claimed.
```

The second branch adds less to the active parent. It is selected for the next
conditional collapse calculation. This selection does not promote its
abundance or primordial covariance to a fundamental prediction.

## 5. Machine-cog consequence

The no-go protects rather than weakens the local result. No unsafe tadpole,
direct matter charge, second metric or electromagnetic charge is introduced.
The exact Cartesian vacuum remains the checkpoint-4947 GR/Newton/Maxwell
branch; Maxwell and Poynting momentum remain in the same Hilbert source. An
occupied neutral motion state can still gravitate on galactic scales through
that same metric.

What is not yet known is whether nonlinear evolution of the globally fixed
state produces `q_parent`, the finite wave core and the `p=2` edge. The source
hunt has now been performed rather than deferred. The next move is execution,
not another relabelling of the source.

## 6. Status

```text
regular current-changing parent vertex              = absent by source audit;
4890 mix as amplitude nucleation                     = rejected exactly;
neutral gravitational pair production               = retained;
real-scalar number-changing hierarchy                = retained but not charge;
precharged composite clock                           = boundary sector only;
neutral one-clock state                              = selected conditional route;
local GR/Newton/Maxwell cog                          = retained;
q/core/p=2 formation                                 = still unproved.
```

All generated rows remain nonclaim. The protected `formalization-workbench`
digest remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
