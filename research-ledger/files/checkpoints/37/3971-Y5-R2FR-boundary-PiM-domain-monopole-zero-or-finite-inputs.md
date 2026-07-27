# 3971 - Boundary PiM Domain Monopole Zero Or Finite Inputs

Timestamp: `2026-07-01T15:54:33+00:00`

## Result

3971 splits the highest-leverage hidden-monopole triad:

```text
epsilon_triad_abs =
 |epsilon_boundary| + |Delta_PiM| + |epsilon_domain_projector|
```

and feeds it into:

```text
epsilon_mu_extra_total <= epsilon_triad_abs + remaining_channels_abs
|Delta_B_single_mass|/A_source^2 <= C_mu (epsilon_triad_abs + remaining_channels_abs)
```

## Why This Matters

Boundary, `Pi_M/projector`, and domain are not just mass-bookkeeping nuisances.
They also feed beta, alpha1, alpha2, alpha3, xi, gamma, radial mass closure, and source calibration.

## Decision

The next best narrow target is boundary reference/no-flux:

```text
epsilon_boundary_reference_abs = (|B_zero_flux| + |Delta_symp|)/M_H_ref
```

Either prove `B_zero_flux=Delta_symp=0`, or make this the first finite nonclaim input row.

Source needles found: `25/25`.
