# 4078 - Second P0 Bound Or B Translation Owner Theorem

- Timestamp: `2026-07-02T02:55:31+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `B_TRANSLATION_OWNER_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED_SECOND_P0_PREFERRED_FRAME_BOUND_SOURCED`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## B Translation Owner Theorem

4078 tries the derivation route first.

If MTS has a parent-owned local motion-origin symmetry:

```text
X^A -> X^A + a^A(x)
e^A = D_omega X^A + B^A
```

then:

```text
D_omega X^A -> D_omega X^A + D_omega a^A
```

so covariance of `e^A` forces:

```text
B'^A = Lambda^A_B B^B - D'a^A
```

That is an exact conditional theorem. It is the right mathematical route.

But it is still not a current MTS derivation, because the current corpus has not parent-signed local motion-origin translations and a varied `B^A` sector before local-GR readout.

## Second Finite P0 Bound

Since the owner theorem remains conditional, 4078 adds the next finite P0 residual scale.

Unowned frame/solder leakage can show up as preferred-frame PPN terms. The conservative weak-field row uses:

```text
|alpha_1| <= 1.0e-04
```

from Will's Living Reviews Table 4, listed as an orbital-polarization bound from Lunar laser ranging. The same table records a tighter companion value:

```text
|alpha_1| <= 4.0e-05
```

from PSR J1738+0333, and an `alpha_2` reference:

```text
|alpha_2| <= 2.0e-09
```

from millisecond-pulsar spin precession.

The active weak-field P0 row is therefore:

```text
epsilon_frame_gauge_quotient_alpha1 <= 1.0e-04
```

This is not a pass. It is a finite leash on preferred-frame leakage.

## Runner Update

The local-GR residual runner now has two numeric P0 teeth:

```text
epsilon_reciprocal_lock        Cassini gamma scale
epsilon_frame_gauge_quotient   alpha_1 preferred-frame scale
```

The aggregate remains blocked because these are still nonnumeric or theorem-open:

```text
epsilon_spatial_metric_owner
epsilon_theta_parent
epsilon_B_derivation core
epsilon_torsion_nonmetricity
epsilon_kappa_normalization
```

## Decision

```text
B-owner theorem = exact conditional theorem
current B derivation = not parent-signed
second finite P0 bound = sourced alpha_1 preferred-frame row
```

## Sources

- Will, `The Confrontation between General Relativity and Experiment`, Living Reviews in Relativity, Table 4: current PPN limits.

## Next

`4079` should either:

```text
prove torsion/nonmetricity zero or auxiliary suppression
```

or source a finite P0 torsion/nonmetricity bound row.
