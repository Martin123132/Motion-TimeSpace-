# Physical early state recovered; coherent quadrature bridge derived

10 November 2026. Continuation of the retained parent quadratic subfamily.
No fit, new coupling, halo normalization or change to the original bank.

## What advances

1. The original early calculation retained the real field perturbation AND
   its conformal velocity. Both have now been recovered in the canonical
   Newtonian-gauge coordinates from 4253 saved epochs at k=1/Mpc, separately
   for the cold baseline and heavy MTS case. Both retain the slow scalar;
   only the heavy case contains the heavy scalar. The conversion requires
   no numerical metric derivative and remains regular at field/velocity
   turning points. The heavy sampled history includes 152 field and 151
   velocity sign changes; these counts are not a complete oscillation count
   because parts of the old output schedule are sparse.
2. Exact field/momentum -> complex-envelope and source maps are derived.
   The two averaged density/current coefficients alone leave a two-dimensional
   nullspace in the four-real-coordinate ensemble. An explicit null direction
   changes pressure while leaving those two moments unchanged.
3. There is a constructive route which preserves the recovered state:
   carry its rank-one quadrature second moment in the background and stress
   contractions. The same parent action then reproduces the coherent real
   sources exactly. Its matter energy/current identities are proved for a
   constant positive-semidefinite second-moment matrix. Uniform phase averaging
   is the separate rank-two choice, not a coordinate transformation of the
   rank-one state. No D0 or fictitious occupied quadrature is needed for this
   coherent reference.

## Verified against retained calculations

- 34 gauge/carrier/source-map identities and 30 quadrature/source-conservation
  identities reduce exactly to zero: 64 symbolic identities total, not 64
  independent physical predictions.
- All 46 numerical recovery/reproduction checks pass the unchanged 2e-5
  reconstruction and 1e-10 algebra gates. Maximum saved-native stress
  reconstruction discrepancy is 1.85833e-13 under the documented peak
  component-sum normalization. The largest algebra/reproduction normalized
  discrepancy is 3.83044e-14. This establishes faithful reconstruction of
  the saved calculation, not equivalent physical accuracy of its evolution.
- The old a225-w6-d8 density/current/pressure projection is reproduced from
  the original k=1 packet without a fit or new phase window. Its existing
  pressure-closure discrepancy remains 6.36893e-8 on its original mode norm,
  compared with its original 2e-6 gate. This is a reproduction of an old
  result, not an additional independent pass.
- That 902-node secular projection has 429 negative weights, total negative
  weight -0.3512206, and unit total weight. It is a signed regression
  extraction, not automatically a positive ensemble average. The old fit
  has not been invalidated or changed; its physical interpretation needs
  to preserve this distinction.

## Saved deliverables

- `DERIVATION.md`: gauge conversion, full carrier map, symplectic form,
  two-moment rank/nullspace and verification contract.
- `STATE-COVARIANCE-BRIDGE.md`: source/action bridge for coherent and
  phase-averaged states, conservation and basis invariance.
- `cold-canonical-early-state.npz`, `heavy-canonical-early-state.npz`: actual
  a, conformal clock, metric coordinates, fields, canonical momenta, D/P/Q
  and compensated density. The physical momentum is stored as Pi=a^2*p;
  it is NOT anisotropic stress in these packet keys.
- `recovery-result.json`: values at the nearest saved epochs to the three
  original anchor scales, explicit actual scales and all check denominators.
- `projection-reproduction.json`, `symbolic-result.json`,
  `state-covariance-result.json`: reproducible evidence and negative control.

## Scope that accompanies the result

These are the native linear transfer solutions with their retained seed
normalization, not a measured primordial random realization. Original
adiabatic/native seed, seed_scale=1, masses, heavy fraction=0.5 and homogeneous
amplitude remain inherited inputs. No primordial power amplitude or local
galaxy occupation is derived here. The retained metric output columns can
have single-precision origin; their algebraic use is not an independent
metric-accuracy check. The displayed state is unaveraged; it has not yet
been propagated forward through the new coherent quadrature interface.

No Galaxy files, workers or laws were changed. Galaxy update 09 remains an
attributed conditional baryonic-force result, as recorded in the preceding
stage; it does not supply the parent population. No browser, relay, timer,
subagent, external download, GitHub action or native rebuild was used.

Next: the bounded paired coherent-state replay in `NEXT.md`, rather than
another arbitrary wavelength or another missing-input search.
