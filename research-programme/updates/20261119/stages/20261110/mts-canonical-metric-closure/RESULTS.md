# Canonical metric/source connection — 10 November 2026

## Concrete advance

The saved carrier-relative action now has an explicit unrestricted
canonical source map into the retained Einstein constraints. Its affine
response D becomes part of the momentum state, not a parameter held fixed
while varying gravity. The resulting scalar feedback matrix is given in
DERIVATION.md, including the other-species density/current ports and
anisotropic stress. The free fast component remains an initial datum.

This continues the existing Einstein/minimal-scalar branch. It does not
introduce a new field, change G, select galaxy occupation, or replace the
existing joint gravity Hamiltonian. Source identities carry the prior
pure-metric terms and boundary bookkeeping rather than dropping them.

The additional defect calculation gives an exact forced constraint law:

    E_constraint'+H E_constraint
      = ED_total+3H EQ_total/k+3 EH Q_total/k.

Thus the next full coupled calculation has a quantitative way to transport
background, field and species errors into its gravity-constraint budget.
There is also an explicit Newtonian comparison with separate enthalpy,
momentum and anisotropic-slip corrections. No uniform numerical enclosure
is claimed from saved sample maxima.

## Verified evidence

-18exact identities in proof.json, including action/Legendre metric-source
  agreement, source conservation, constraint propagation, feedback matrix
  and the affine-to-canonical source map.
-4additional identities in defects-proof.json retain off-shell field and
  background defects and give the Newtonian difference formula.
-75accepted source/replay/metric-port checks in precision-sources-result.json.
-7182saved MTS state/time/preparation combinations:399modes x9positions x2
  preparations. Maximum saved-source difference1.291e-15 in the existing
  normalized source blocks; this is arithmetic agreement, not new physical
  or observational accuracy.
-Independent rotated real-quadrature stress readout and the algebraic
  metric solve pass the unchanged1e-10 gate. Largest accepted check value
  2.346e-15. Omission of the metric measure source is detected; at the first
  D0sample its synthetic constraint residual is about0.364 in the declared
  normalization. This is a negative control, not an observational effect.
-Cold action/Euler replay remains6.167e-16; both cold endpoint metric-port
  checks pass. No scalar reference mass is inserted into cold gravity.

The metric-port tests use explicitly synthetic other-species initial
sources. They verify the algebra for nonzero rest density/current/slip,
not their physical evolution. All numerical comparisons reuse existing
histories; there is no new fit, data download or coupled late trajectory.

## Preserved failure and repair

The first independent rotated-quadrature readout failed the strict1e-10
algebra gate at1.9144e-9, despite passing the direct saved-source map. The
failed sources-result.json, worker receipt, packet and original script are
retained. Only that readout was reevaluated at60digits on the same double
inputs; all tolerances, histories, bank and grids are unchanged. This
removes cancellation without claiming60digit physical accuracy. See
READOUT-PRECISION.md and precision-representation.json.

## Executable next step

The old hierarchy adapter was inspected, not launched: it explicitly
rejects the late averaged heavy selector, excludes it from the numerical
state and restores excluded slots to zero. It also rejects the retained
massive-neutrino preparation memory. An early184/182state replay is not a
valid substitute. NEXT.md specifies the isolated late adapter and native
replay required before the derived new scalar block can be evolved with
all other species. The equations are now supplied; that runtime interface
is the next implementation task.

No GitHub, Galaxy Lab edits, outgoing relay, new timer, browser or unrelated
worker action. Prior scientific files are preserved; the resume note is
updated additively. See closeout.json and CLEANUP-VERIFIED.md for receipts.
