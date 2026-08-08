# 5333 - E040 finite rung and regulator-zero closure

## E040 completion

The event-aligned E040 traversal completes with `420/420` shards accepted,
zero failed shards, zero pending shards, and zero unresolved poles.  Every
adaptive leaf gate passes.

The finite result is

```text
I_D2(E040)                    = 36.5167365582 + 3.41542001120 i;
|I_D2(E040)|                  = 36.6761113358;
total conservative error     = 8.43149106283e-2;
relative conservative error  = 2.29890540620e-3.
```

## Off-support quadrature theorem branch

For a failed local node with no inactive selected terms, no unresolved poles,
at least one geometric pole, and no pole inside the real reduced-term support,
failure of the topology-safe near-support Laurent fit does not create a pole on
the integration contour.  The real integrand remains smooth on each support
cell, so direct panel refinement is the valid fallback.  The controller now
executes the source-owned `64|128|256|512` ladder and accepts only through the
unchanged node convergence gates.

The first target closes at 64 subdivisions:

```text
pre-repair Q4/Q8 change   = 7.71038977830e-3;
post-repair Q4/Q8 change  = 1.99783413934e-5;
post-repair error budget  = 1.99786249989e-5.
```

The same semantic rule independently closes the second encountered target.
No node identifier appears in the selector.  Historical failed near-support
attempts are superseded only when the final shard contains a successful
source-bound analytic-divisor certificate or an accepted off-support
quadrature row.

## Seven-rung ladder

Checkpoint 5327 now collects the seven finite regulators
`E000625|E00125|E0025|E005|E010|E020|E040` and validates with decision
`D2_SEVEN_POINT_FINITE_REGULATOR_LADDER_COMPLETE__FIT_ZERO_LIMIT`.

## Regulator-zero result

Checkpoint 5328 executes and validates:

```text
reference zero limit                     = 36.4288701854 + 4.08427928405 i;
reference magnitude                      = 36.6571128194;
pairwise Richardson maximum shift        = 1.04833197728e-2;
leading-family relative bound            = 5.11710630388e-3;
complete-remainder relative bound        = 7.44703818449e-3;
topology-excluded half-power shift       = 3.01573971390e-4 relative;
acceptance limit                         = 1.0e-2 relative.
```

All 49 event normal-form rows pass, all seven derived model fits pass, and no
eighth regulator is required.  The validated decision is
`D2_MIDPOINT_REGULATOR_ZERO_ACCEPTED__BUILD_DECAY_ANGLE_QUADRATURE`.

## Claim boundary and next action

This checkpoint proves the D2 midpoint regulator-zero numerical gate under the
implemented source and normal-form contracts.  It does not prove the
decay-angle integral, full angular convergence, full phase-space coefficient,
UV coefficient, local GR or full MTS.

Checkpoint 5324 already derives the paired decay measure, sign-orbit reduction,
topology events, soft panels and GL2/GL4 topology-safe quadrature contracts.
The next implementation must use those contracts to run two new fixed-decay
finite-regulator ladders, compare GL2 against GL4, and enforce the 0.5-percent
endpoint cap.  It must not revive the obsolete order-9 path or introduce a
fitted angular closure.

The protected formalization-workbench digest remains
`0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f`,
with modified-file count zero.  Both checkpoint-5327 and checkpoint-5328
validation tables have zero failed gates, generated `.pyc` count is zero, and
no GitHub action occurred.
