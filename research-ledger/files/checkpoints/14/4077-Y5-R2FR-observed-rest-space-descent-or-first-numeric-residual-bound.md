# 4077 - Observed Rest-Space Descent Or First Numeric Residual Bound

- Timestamp: `2026-07-02T02:49:56+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `OBSERVED_REST_SPACE_DESCENT_CONDITIONAL_NOT_PARENT_SIGNED_FIRST_P0_NUMERIC_RECIPROCAL_LOCK_BOUND_SOURCED`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Descent Attempt

The direct descent route is still conditional:

```text
q(Phi) -> Q_obs
e_obs(Phi) = Obs_e(q(Phi))
v in ker(Dq) => Lie_v e_obs = D Obs_e[Dq(v)] = 0
```

If the parent signs `q` and `Obs_e`, representative-frame leakage vanishes by the chain rule.

But current files still mark the core pieces as not parent-signed:

```text
q(Phi) owner
observed coframe descent
clock normal n_mu
spatial rest metric h_mu_nu
same-readout matter/EM/clock/orbit functor
```

So 4077 does **not** promote the local-GR derivation.

## First Finite P0 Bound

4077 stops the all-symbolic P0 runner by sourcing one real residual scale.

The motion-load branch has:

```text
gamma = p
T^2 S = 1 -> p = 1
epsilon_reciprocal_lock := |p - 1| = |gamma - 1|
```

Cassini gives:

```text
gamma - 1 = (2.1 +/- 2.3) x 10^-5
```

Therefore the first finite P0 row is:

```text
central |epsilon_reciprocal_lock| = 2.10e-05
sigma = 2.30e-05
central + 1 sigma envelope = 4.40e-05
central + 2 sigma envelope = 6.70e-05
```

This is not an MTS pass. It is a numeric leash on the reciprocal-lock branch.

## Runner Update

The effective local-GR runner moves from:

```text
P0_BLOCKED_NOT_NUMERIC
```

to:

```text
P0_PARTLY_NUMERIC_STILL_BLOCKED
```

because `epsilon_reciprocal_lock` now has a source-backed finite bound, while the other P0 rows remain nonnumeric:

```text
epsilon_spatial_metric_owner
epsilon_theta_parent
epsilon_B_derivation
epsilon_torsion_nonmetricity
epsilon_kappa_normalization
```

## Decision

4077 does two useful things:

```text
observed rest-space descent = conditional, not claimed
first finite P0 residual bound = sourced from Cassini gamma
```

Future local-GR work should now obey this rule:

```text
each P0 gate must either be theorem-zeroed or assigned a finite sourced bound
```

No more purely symbolic P0 ladder unless it is closing a proof.

## Sources

- Bertotti, Iess, and Tortora, `A test of general relativity using radio links with the Cassini spacecraft`, DOI `10.1038/nature01997`.
- NIST page for Ashby and Bertotti, `Accurate light-time correction due to a gravitating mass`, records the Cassini gamma accuracy scale.

## Next

`4078` should either:

```text
derive the B^A translation-owner theorem
```

or source the next finite P0 bound row.
