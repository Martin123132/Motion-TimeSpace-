# 5290 — All-family stored-node subtraction reassembly

## Result

This checkpoint reuses all `42,624` component-node evaluations from 5287.
It adds no new point evaluations. The stored component integrals are
corrected by the analytic integrals minus the stored-node quadrature sums
of:

- the `MC03/MC08` promoted material poles from 5288;
- the `MC04/MC12` promoted material poles from 5289;
- the paired lower-endpoint `A_X/E` terms from 5288.

The endpoint analytic terms remain pair-cancelled; their maximum relative
pair residual is
`1.4224375355e-10`.

## Convergence

- material pole terms: `12`;
- endpoint terms: `16`;
- maximum nodewise energy `4 -> 8` change:
  `0.000989102076335`;
- order-two outer energy `4 -> 8` change:
  `0.00273355599476`;
- order-two energy-8 value:
  `{'imaginary': 1.6754448714685068, 'real': 15.942591743447988}`;
- validation passed: `True`.

## Decision

`ACCEPT_ORDER2_ALL_FAMILY_ENERGY_CONVERGENCE__ADVANCE_ANGULAR_ORDER_COMPARISON`

This closes the inner-energy convergence gate at angular order two. It
does not yet close angular-order convergence, angular endpoint caps, full
phase space, UV, local-GR, or full-MTS claims.
