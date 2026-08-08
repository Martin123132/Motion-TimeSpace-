# 5288 — Failed angular-node singularity derivation

## Purpose

Checkpoint 5287 completed the first four-node angular smoke calculation,
but its inner-energy convergence failed at three nodes. This checkpoint
does not add quadrature points blindly. It derives the singular objects
that the failed rules were integrating untreated.

## Derived structures

- geometric pole candidates scanned: `20`;
- exact-mask active candidates: `20`;
- candidates promoted by the angular mask: `20`;
- material simple poles: `8`;
- material pole components: `['MC03', 'MC08']`;
- material lower endpoints: `16`;
- endpoint targets: `['A02_S01_D01|MC12', 'A02_S01_D01|MC15', 'A02_S01_D02|MC04', 'A02_S01_D02|MC14', 'A02_S02_D01|MC04', 'A02_S02_D01|MC14', 'A02_S02_D02|MC12', 'A02_S02_D02|MC15']`.

The lower endpoint law is

`F_X(E) = A_X / E + O(1)`.

The fitted exponent differs from `-1` by at most
`0.000394311276668`.
Each individual component has a nonzero coefficient, but the coefficients
occur in opposing `MC04|MC14` or `MC12|MC15` pairs. Their pair sums vanish
within the fitted error budget. The next runner must subtract and add the
paired terms together so quadrature does not destroy this analytic
infrared cancellation.

For the upper-energy failures, the angular mask promotes geometric poles
that were inactive in the fixed-angle calculation. Their roots are
refined channel zeros and their residues are obtained as

`Res(F_X,E_X) = N_X(E_X) / D'_X(E_X)`.

## Numerical controls

- maximum channel-root residual:
  `3.20769529435e-11`;
- maximum selected numerator-fit residual:
  `3.62897862563e-07`;
- maximum pole radius refinement change:
  `0.965225781449`;
- maximum pole degree change:
  `1.04534708174`;
- maximum endpoint fit residual:
  `3.73515622386e-11`;
- validation passed: `True`.

## Decision

`DERIVE_NEW_ANGULAR_POLES_AND_LOG_ENDPOINTS__BUILD_COMBINED_SUBTRACTION_RUNNER`

This is a singularity inventory and subtraction contract. It is not an
angular-convergence, full phase-space, UV, local-GR, or full-MTS claim.
