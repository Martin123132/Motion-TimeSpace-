# 5337 - D4 regulator-fold double-scaling and contrast gate

Date: `2026-08-10`

Marker: `MTS_5337_D4_REGULATOR_FOLD_DOUBLE_SCALING_CONTRAST_GATE`.

## Executive result

Checkpoint 5337 closes the regulator-geometry preflight that blocked the
checkpoint-5334 D4 outer calculation.  The targeted scan evaluates all eight
material pole-support events at seven regulators,

```text
epsilon = 0.000625, 0.00125, 0.0025, 0.005, 0.01, 0.02, 0.04.
```

All `56/56` event rows pass their contact and transversality contracts.  Every
rung retains the same eight-event order,

```text
E01|E02|E03|E05|E04|E06|E07|E08,
```

with three support entries, four one-sided branch deaths and one support exit.
The fitted scaling laws are

```text
minimum physical event gap  ~ epsilon^(3.78106256174e-6),
maximum regulator ratio eta ~ epsilon^(0.999996155930).
```

Thus the sampled event gap tends to a nonzero constant while the regulator
contact width tends to zero linearly.  The event-merger co-scaling route is
rejected on the seven-rung ladder.  The adaptive panel partition does not
alter this conclusion because it retains the complete fixed physical angular
domain.

This is a geometry preflight, not the D4 integral.  It licenses resumption of
the saved checkpoint-5334 `E0025` shards.  It does not promote a D4
regulator-zero, decay-angle, phase-space, UV, local-GR or full-MTS claim.

## 1. Exact double-scaling quantities

Let the ordered event coordinates at regulator `epsilon` be `x_i(epsilon)`.
Define the minimum physical separation

```text
g_min(epsilon)
 = min_i [x_(i+1)(epsilon)-x_i(epsilon)].
```

For event `i`, let

```text
a_i     = |Im p_i|/epsilon,
kappa_i = |d m_i/dx|,
```

where `p_i` is the geometric pole and `m_i` is its signed support margin.  The
local regulator contact width in the outer coordinate is

```text
w_i(epsilon)=a_i epsilon/kappa_i.
```

With nearest-event half-gap

```text
h_i = 1/2 min(x_i-x_(i-1), x_(i+1)-x_i),
```

the dimensionless separation diagnostics are

```text
eta_i  = w_i/h_i,
zeta_i = 1/eta_i.
```

A dangerous event-merger double scaling would keep `eta` finite or growing as
`epsilon -> 0` by shrinking a physical event gap with the regulator.  A fixed
topology limit instead requires

```text
g_min -> g_0 > 0,
eta_max -> 0,
zeta_min -> infinity.
```

These are physical pole-support separations.  A numerical quadrature-panel
width is not substituted for `h_i`.

## 2. Seven-rung D4 evidence

The executed summary is

```text
epsilon    g_min                 eta_max              zeta_min
0.000625   5.95966171831108e-4   1.80041004547590e-4  5554.29027133
0.00125    5.95966187459718e-4   3.60082029697999e-4  2777.14497677
0.0025     5.95966206144549e-4   7.20164007489244e-4  1388.57258847
0.005      5.95966362081701e-4   1.44032772398995e-3   694.286434500
0.01       5.95966938946146e-4   2.88065268146641e-3   347.143550638
0.02       5.95969240291039e-4   5.76128221742666e-3   173.572472630
0.04       5.95978470467440e-4   1.15223825489924e-2    86.7876062740
```

Even at the largest sampled regulator, the narrowest event separation is
about `86.8` regulator contact widths.  Separation improves monotonically as
the regulator decreases.  The largest event-coordinate shift relative to the
source `E0025` inventory is `6.48857869989e-7`, far below the minimum event
gap.  The recorded event-root bisections total `1533` iterations.

The fitted exponents are

```text
d ln g_min/d ln epsilon   = 3.7810625617428925e-6,
d ln eta_max/d ln epsilon = 0.9999961559296449.
```

The result is therefore consistent with

```text
g_min(epsilon)=g_0+O(epsilon^2),
eta_max(epsilon)=C epsilon[1+o(1)].
```

This establishes the sampled fixed-topology route.  It is not promoted into
an unsampled global theorem about every positive regulator.

## 3. Relation to the imported fold source

The locked maths-exploration fold source distinguishes two limits.  Its
reproduced exponents are

```text
fixed mass:       tail/root ~ delta^1.99998695551,
fixed xi=m delta: tail/root ~ delta^(-2.40378113e-18).
```

The source therefore supplies the correct double-scaling question: does a
physical scale stay fixed while the regulator vanishes, or is another scale
silently driven with it?  Checkpoint 5337 transfers that diagnostic logic to
the dimensionless D4 ratio `eta`.

It does not identify the source fold with the D4 pole-support mechanism.  The
former is a fold/tail model; the latter is an event-aligned regulated
phase-space geometry.  Agreement of scaling logic is not microscopic
equivalence and adds no parent-owned coefficient, state or value of
`q_target`.

## 4. Orthogonal regulator contrast

The source's orthogonal mass-contrast idea becomes a Helmert contrast on the
already completed D2 seven-rung ladder.  It removes the common intercept with

```text
constant-channel annihilation error = 1.1102230246251565e-16,
contrast orthonormality error        = 2.220446049250313e-16.
```

The derived transverse endpoint-log family is full rank and has

```text
residual/conservative bound = 0.0120342123422.
```

It survives, but it is not selected uniquely.  All five comparison families
are compatible with the conservative D2 numerical disks:

```text
analytic linear;
analytic quadratic;
transverse endpoint log;
endpoint log plus epsilon^2;
fold square-root stress.
```

Consequently topology remains the selector of the allowed D2 normal form; the
finite numerical errors do not identify a unique subleading family.

No D4 contrast is executed.  The seven geometry rungs are not seven accepted
D4 integral values.  An overdetermined D4 contrast remains blocked until at
least four finite-regulator D4 integrals pass their own numerical contracts.

## 5. Numerical-domain statement

The checkpoint-5334 event-aligned plan adaptively moves quadrature partition
boundaries.  Those boundaries are numerical bookkeeping, not physical
integration limits.  The plan retains the complete source-owned angular
domain, so subdivision motion cannot change the exact integral:

```text
integral over full fixed domain
 = sum of integrals over any complete non-overlapping partition.
```

The relevant uniformity condition is instead the physical one tested above:
regulated pole-contact neighborhoods must remain parametrically narrower than
the separation between distinct material events.

## 6. Execution durability

The first monolithic scan exited before producing an artifact.  The runner was
therefore hardened before repetition.  It now writes each completed event and
each completed regulator rung atomically, records live status and tracebacks,
and resumes only cache entries matching the locked source signature.  The
successful run recovered from its saved cache rather than recomputing all
completed events.

This changes execution durability only.  It does not alter event equations,
thresholds, source rows or acceptance gates.

## 7. Decision and next action

The checkpoint decision is

```text
D4_EVENT_GEOMETRY_FIXED_TOPOLOGY_LIMIT_SUPPORTED__
EVENT_MERGER_COSCALING_REJECTED_ON_SEVEN_TARGETED_REGULATORS__
D2_CONTRAST_METHOD_VALID_BUT_NONSELECTIVE__
RESUME_5334_SAVED_SHARDS.
```

The next executable action is

```powershell
.\.venv-score\Scripts\python.exe .\scripts\Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py --mode refinement-run --max-runtime-hours 2
```

The runner must reuse and hash-check the `413` completed `E0025` shards, finish
the pending shard and adaptive tree, and only then decide whether `E0025` is an
accepted finite-regulator D4 value.  If accepted, the remaining D4 regulator
rungs can be populated and the contrast gate revisited.

## 8. Claim and integrity boundary

All `15/15` validation gates pass.  The `20` source rows are locked, the `14`
parent checkpoint inputs are unchanged, and the protected
`formalization-workbench` digest remains
`0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f`.

All claim flags remain false.  In particular, checkpoint 5337 is not evidence
for a completed D4 regulator-zero integral, physical phase-space coefficient,
new parent ownership, derived `q`, galaxy result, local GR or full MTS theory.
The runner compiles and the generated non-virtual-environment `.pyc` count is
zero.  No GitHub action occurred.
