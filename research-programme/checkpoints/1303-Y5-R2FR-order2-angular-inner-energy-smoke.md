# 5287 — Order-two angular inner-energy smoke

## Purpose

This is the first nested calculation after the fixed-angle certificate.
At each of four angular Gauss nodes it:

1. rebuilds the local material-channel problems;
2. classifies exact-mask activity at each geometric pole;
3. derives active residues as `N(E_p)/D'(E_p)`;
4. constructs exact mask and endpoint-refined energy panels;
5. compares inner Gauss orders 4 and 8;
6. forms the physical two-regulator and order-two angular sum.

## Result

- selected active poles:
  `4`;
- energy component-node rows:
  `42624`;
- maximum pole-fit residual:
  `2.06380667309e-11`;
- maximum nodewise inner-energy change:
  `1.17477561013`;
- outer order-4 to order-8 change:
  `1.00632624329`;
- order-two / energy-order-eight value:
  `26.3713770692-1.81857014459i`;
- inner smoke passed:
  `False`.

Decision:
`ORDER2_INNER_ENERGY_SMOKE_VALID_BUT_NOT_CONVERGED__LOCALIZE_FAILED_ANGULAR_NODE`.

Validation: **PASS**.

## Claim boundary

No angular-convergence or full phase-space claim is made. Passing this
checkpoint only authorizes an adaptive angular convergence runner.
