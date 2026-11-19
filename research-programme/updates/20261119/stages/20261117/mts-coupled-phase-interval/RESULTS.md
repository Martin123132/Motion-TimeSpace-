# Coupled phase interval and frozen local prediction — 17 November 2026

## New physical evidence

Continued the complete paired states from2932 through3038:106 new existing
native-clock epochs, about0.130515 Mpc of conformal time (0.714 of the local
principal heavy-field period at the starting state). Baseline and MTS use
the same frozen bank, original grids, parameters,32/64 step settings,
1e-10 algebra and2e-5 numerical gates. All surrounding native species remain
live in the authoritative evolution.

Both cases pass full-output refinement, pressure, coherent exchange, common-
metric constraints and an independent original-CAMB solver comparison.
The latter checks our old-background branch against the native original
observer, not against a different cosmological model.

## A source prediction derived before the test

DERIVATION.md eliminates the same metric constraint from the retained heavy
Klein–Gordon equation, producing an exact instantaneous3-variable subsystem
for heavy displacement, its derivative and eta_k. The cold control has its
corresponding2-variable subsystem. These are not independently closed:
the remaining matter/radiation density and current drive them.

Before running the future live trajectory, we froze two approximations:
constant surrounding sources, and sources evolved using their endpoint
derivatives from the actual collision/field stress equations. The background
was independently evolved with its retained equations in both predictions.
No coefficients, future source samples, endpoint residuals, or new fit entered.
The local equations match the saved native endpoint derivatives at1e-10.

| Coherent density-source forecast | Baseline error / frozen norm | MTS error / frozen norm |
|---|---:|---:|
| Constant surroundings | 8.52136e-9, passes | 1.90231e-4, fails |
| Equation-derived linear surroundings | 1.19837e-9, passes | 1.62054e-6, passes |
| Fixed tolerance | 2e-5 | 2e-5 |

The MTS density-source error drops by about117-fold. Its frozen linear
prediction also passes the field-state, current and pressure readouts.
Its pressure error is1.33453e-7 of the frozen pressure amplitude; its largest
state comparison is eta_k at2.16436e-6. Old-background branches have the same
pass/fail pattern. Constant MTS surroundings fail density on both branches;
those failures are preserved.

This does not turn the approximation into a universal closure. For example,
the linear surrounding-current history itself differs from the actual MTS
history by about0.00585 of its own amplitude. The projected field response
is less sensitive to that error over this finite window. Accurate outputs
do not prove every approximate input is accurate. The full native evolution,
not the reduced predictor, remains authoritative.

## Full coupled checks

Selected errors include refinement and the stated working rounding allowance:

| Check | Baseline | MTS |
|---|---:|---:|
| Coherent trace residual / reference | 4.41432e-8 | 4.47087e-8 |
| Coherent shear residual / reference | 4.41432e-8 | 4.54398e-8 |
| Coherent density-exchange residual / reference | 2.94066e-14 | 4.44396e-11 |
| Coherent current-exchange residual / reference | structural zero | 3.49748e-12 |

All pass2e-5. The finite-neutrino metric floor is retained, not subtracted.
Cold own current/pressure zeros are structural, not measured accuracy of
nonzero quantities.

A separate review recomputes output rounding from primitive terms before
cancellation, rather than final small readouts. All full-output refinement and
independent-control gates still pass. The MTS native-velocity correction
refinement including this more conservative estimate is5.48410e-6 relative
to its maximum correction, below2e-5. The baseline correction is still
unresolved. These remain working numerical estimates, not rigorous interval
bounds or a transported complete spectrum/source uncertainty budget.

The MTS coherent-minus-original native-velocity correction spans
[-2.35910e-7,+2.80729e-7] and ends at approximately-1.43251e-7.
It is neither constant nor a claimed MTS-versus-LambdaCDM observation.
The old projected preparation pressure budget87.5966% is not automatically
extended to this pointwise history; no902-window projection or sky likelihood
was computed. Quantum-measure and galaxy-population questions remain separate.

## Reuse and verification

Use cold-live-64-terminal.npz and heavy-live-64-terminal.npz for complete3038
restarts. Each of seven bounded batches per case/step has its own full
terminal and history; all28 batch joins are verified exactly. Original942
native prefix rows, supported signatures, and initial restarted derivatives
remain exact. Prior full coupled evolution was not replayed from1991.

90 verification checks pass. Frozen forecast files and score definitions
predate the live runs. Main physical gates and independent controls pass;
constant-MTS approximation failures and tiny baseline response failure remain.
Native owner releases and worker exits are recorded.

One driver NameError was fixed before any forecast was generated, by using
the already imported retained background module. The initial failed receipt
and old input manifest are preserved; no physics, tolerance or prediction
selection changed. See driver-fix.json.

All work stays private and local. No rebuild, external download, publication,
scheduler, browser/server or other-chat process change occurred.

