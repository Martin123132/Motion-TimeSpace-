# 3969 - Single Exterior Mass Uniqueness Or Beta Obstruction Bounds

Timestamp: `2026-07-01T15:46:04+00:00`

## Result

3969 sharpens the 3968 square-law route.

The conditional theorem is:

```text
EH/SdS exterior + compact source-free collar + no extra local tensors
+ fixed boundary/reference + one observed readout + one parent-owned monopole
=> exterior metric has one mass parameter mu
=> g00=-1+2mu/(rho c^2)-2mu^2/(rho^2 c^4)+O(c^-6)
=> B_source=A_source^2
=> delta_beta_source=0
```

That is a real route to beta, but it is not yet an MTS claim.
The MTS-owned task is now narrower: prove that no hidden exterior monopole hair survives.

## Bound Fallback

If uniqueness does not close, beta receives:

```text
|delta_beta_source| <= Delta_B_square_abs / |A_source|^2
Delta_B_square_abs <= sum_i |Delta_B_i|
```

where the active obstruction channels are extra monopole charge, non-EH operator tail, boundary/reference flux, PiM/projector variation, q_loc second order, readout/coframe transfer, and coupling/source-scale drift.

## Source Intake

Source needles found: `20/20`.

## Decision

Next target: channelwise no-extra-exterior-monopole hair, or finite hidden-monopole bound rows.
