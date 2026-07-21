# 5170 - Collective-stress residual, single-coupling no-go and conserved-kernel target

Marker: `MTS_5170_COLLECTIVE_STRESS_RESIDUAL_SINGLE_COUPLING_NO_GO`.

Date: `2026-07-21`.

## Result in one line

Checkpoint 5169 is not missing a larger gravitational coefficient. The
checkpoint-4960 parent already has one rank-one Hilbert source coupling, and
any constant rescaling leaves the measured transition exponent exactly
unchanged. The remaining discrepancy is a compensated radial redistribution
that only a state-dependent conserved response kernel could produce.

## Exact single-coupling theorem

The response score is

```text
q[V^2]=2 d ln V^2/d ln r.
```

For every positive constant `A`,

```text
q[A V^2]=q[V^2].
```

Therefore no second scalar source normalization can move the selected
`q=2.234007139940017` into the parent interval
`[1.511977636680018, 2.20499007120595]`. This is
independent of how `A` is estimated. The best log-amplitude over the existing
scoring window is `1.7324401962430662`,
which would duplicate the locally calibrated Newton residue by
`Delta G/G=0.7324401962430662`,
but it leaves the transition at
`0.6552336161759004` of target while making
the edge `2.052939757104537` times target.

Using only the transition and edge anchors, the exact minimax amplitude still
leaves an unavoidable multiplicative mismatch factor
`1.7700682716488823`. Introducing such an
amplitude would also duplicate the universal source residue already fixed by
the local Einstein/Newton/Maxwell chain.

## Reconstructed collective requirement

The target is used here only to reconstruct an inverse requirement, never as
a proposed predictive operator. For the selected branch the required gain is

```text
gain(R_n)    = 2.6440038384385716,
gain(R_edge) = 0.84388262746029.
```

The cumulative residual changes sign at
`283.8481283505484 kpc`: the state is too
diffuse inside and excessive outside. After matching the edge totals only to
separate normalization from shape, the unique one-dimensional monotone
transport lower bound moves essentially every internal quantile inward by
mean distance `60.38564635937875 kpc`
(RMS `64.35901954609716 kpc`). The existing
edge excess separately requires at least
`0.15611737253971003` of corrected enclosed mass
to leave the edge. Spread over the sourced assembly time, the mean-displacement
bound is `22.144458933210117 km/s`.

All four predeclared clocks give the same conclusion:

- `ISOCHORIC_Z0.1_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: gain contrast=`3.228098377749427`, mean inward transport=`61.55519642473791 kpc`
- `ISOCHORIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: gain contrast=`3.194222422004231`, mean inward transport=`60.59743550314856 kpc`
- `ISOBARIC_Z0.1_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: gain contrast=`3.208568734819129`, mean inward transport=`60.96888894176781 kpc`
- `ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: gain contrast=`3.1331416862980612`, mean inward transport=`60.38564635937875 kpc`

This is not an infinitesimal local correction or a positive component that
can simply be added. It is a sign-changing, mass-conserving collective
polarization/redistribution problem.

## Parent-basis projection

At the transition the selected profile needs fractional enhancement
`1.6440038384385716`. The largest canonical
wave bracket is smaller by factor
`59630.650686393856`; the derived `X^2` and `O4` envelopes are
smaller by factors `1.4121560547697633e+116` and
`3.749634411983126e+233`. The already-bounded local derivative terms
cannot produce the reconstructed response.

The remaining parent-owned class is the occupied-state retarded polarization

```text
delta T_X^munu(x)=int d4y Pi_R^munu,ab(x,y;F_X) delta g^ab(y),
```

with the Vlasov/CTP state equations enforcing its Ward identity. It must have
a compensated zero mode, the reconstructed radial sign change, causal stable
spectral support and exact vacuum silence. Those are now numerical and
algebraic gates, not an invitation to write an arbitrary kernel.

The already-constructed positive occupied-state existence branch has maximum
embedded Mercury tidal ratio `6.614360568718464e-19`
across its 175-galaxy smoke. This supports state-dependent local suppression;
it is not substituted for a full PPN or compact-body calculation.

## Decision

`ONE_UNIVERSAL_HILBERT_SOURCE_COUPLING_IS_ALREADY_FIXED_AND_CANNOT_CHANGE_Q_THE_5169_RESIDUAL_REQUIRES_A_COMPENSATED_OCCUPIED_STATE_POLARIZATION_WITH_INWARD_MASS_TRANSPORT_AND_LOCAL_VACUUM_SILENCE`.

```text
one universal leading Hilbert coupling                  = retained;
constant coupling can change q                          = no, exact;
known wave/X2/O4 stress can close residual              = no, bounded;
positive additive state density alone                   = no;
compensated occupied-state polarization required        = yes;
that retarded kernel derived from current state          = not yet;
local GR/Newton/Maxwell branch modified                  = no;
galaxy or full-MTS claim                                 = false.
```

All `20` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
