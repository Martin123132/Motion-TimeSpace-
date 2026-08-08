# 5035 — paired epsilon-zero and outer-scramble convergence ladder

## Question

Checkpoint 5034 produced a finite-regulator cyclic `hhh` smoke vector but did
not establish the Feynman boundary value. This checkpoint asks the narrower
question that must be answered first:

```text
Does the central cyclic component approach a stable limit as epsilon -> 0+
when the same outer phase-space events are paired across epsilon?
```

No 5018 target value is used in the calculation or in any gate.

## Exact paired estimator

At physical cosine `z=0`, the crossed ratios are

```text
t/s = u/s = -1/2,
(t/s)^3 = (u/s)^3 = -1/8.
```

Consequently each fixed Sobol event supplies the exact central cyclic
estimator

```text
C_epsilon = D(0+i epsilon)
          - D(3+i epsilon)/8
          - D(-3+i epsilon)/8.
```

The unit-cube event is held fixed across `epsilon=(0.08,0.04,0.02)`. Thus

```text
Delta C_ab(event) = C_b(event) - C_a(event)
```

is a paired regulator difference. Its scramble variance does not contain the
much larger unpaired outer-event variance. Global-32 uses the same first event
only as a quadrature audit; it is not counted as another outer sample.

## Restart and provenance contract

Run `central_eps008_004_002_s4_v1` contains four independent scrambled Sobol
events, one point per scramble, three direct arguments per epsilon, a
global-24 primary tier, and a first-scramble global-32 audit. There are 45
terminal jobs. Nine exact `epsilon=0.08` event/argument/tier matches are
imported from checkpoint 5034 only after source-config, job-digest, Sobol-event,
argument, sheet and convergence checks. The remaining 36 jobs are computed on
their own target-specific canonical Feynman homotopies. Raised paths and
representative kernels are forbidden.

The production runner stopped after `10198.9 s`, within its three-hour
numerical budget. The result is restartable at job boundaries.

## Residue-radius correction

The first pass made all 45 jobs terminal but marked six kernels unconverged.
Their adaptive quadratures had actually converged; each failure came from one
unstable pair-local residue. The inherited `v3` rule tried radius
`0.1*safe_scale` and, on failure, enlarged it to `0.2*safe_scale`. Enlargement
cannot repair contamination by a neighbouring pole and did contaminate these
six circles.

The audited `v4` correction keeps the same center, ownership, contour sheet,
nodes and kernel, but searches nested local circles in the order

```text
0.1, 0.05, 0.025, 0.0125 times safe_scale,
```

using `0.2` only as a last diagnostic. It accepts the first radius for which
the outer and half-radius residues agree under the pre-existing stability
criterion (or are jointly below the pre-existing numerical-zero threshold).
All six failures close at fraction `0.05`; none uses `0.2`. Four contaminated
residues become jointly numerical zero. The two nonzero cases settle to
approximately

```text
epsilon=0.04 : 147.9602651 + 6.9897624 i
epsilon=0.02 : 148.0513741 + 3.4952196 i.
```

Original and repaired job/kernel files and their SHA-256 digests are retained
under `source-intake/functional_rg/5035/repairs/pair_local_shrinking_radius_v1`.
This is a numerical contour-isolation correction, not a fitted physics term.

## Central ladder

| epsilon | primary cyclic mean | outer scramble standard error | scrambles |
|---:|---:|---:|---:|
| 0.08 | `-65.94550 - 16.31238 i` | `72.29810 + 13.65503 i` | 4/4 |
| 0.04 | `-76.81181 - 11.59450 i` | `81.52399 + 10.25776 i` | 4/4 |
| 0.02 | `-80.53964 - 6.54195 i` | `84.77308 + 5.87577 i` | 4/4 |

The large real outer variance is genuine at this four-event resolution and is
not hidden. Pairing makes the regulator motion much sharper:

| paired step | mean difference | paired standard error | pairs |
|---:|---:|---:|---:|
| `0.08 -> 0.04` | `-10.86631 + 4.71788 i` | `10.83435 + 3.40849 i` | 4/4 |
| `0.04 -> 0.02` | `-3.72784 + 5.05255 i` | `3.72101 + 4.38225 i` | 4/4 |

The complex mean-step norm contracts from `11.84631` to `6.27893`. For the
two halvings this gives the diagnostic effective order

```text
p_eff = log_2(|Delta_1|/|Delta_2|) = 0.915846.
```

This is compatible with a leading near-linear regulator correction but three
epsilon levels do not prove that expansion. Testing, rather than assuming, a
linear Richardson form gives

```text
C_0 diagnostic = 2 C_0.02 - C_0.04
               = -84.26748 - 1.48940 i,
SE             =  88.05952 + 1.49532 i.
```

The imaginary mean moves toward zero, but neither zero imaginary part nor this
linear extrapolation is imposed as a gate.

## Independent quadrature audit

For the first Sobol event, global-24 and global-32 central values agree at all
three regulator levels:

| epsilon | relative tier difference |
|---:|---:|
| 0.08 | `6.61e-15` |
| 0.04 | `1.98e-14` |
| 0.02 | `1.72e-14` |

The observed uncertainty is therefore outer phase-space variance and regulator
motion, not global-node drift at this event.

## Decision

The central convergence smoke gate **passes**: all 45 jobs are numeric and
converged after the local-radius correction, all four paired scrambles are
present, both mean steps contract, and the independent global-node audit is
stable. This authorizes a bounded paired-epsilon extension to the full
five-component cyclic vector.

It does **not** establish the epsilon-zero limit or production precision. Four
one-point scrambles leave very large real outer variance, only three epsilon
levels were tested, and only the central crossing component was extrapolated.
No crossing-complete `hhh` coefficient, 5018 match, local-GR result or full-MTS
claim follows from this checkpoint.

Marker: `MTS_5035_PAIRED_EPSILON_ZERO_OUTER_SCRAMBLE_LADDER`.

## Next target

`5036-Y5-R2FR-paired-epsilon-full-cyclic-vector-and-local-nonlocal-decomposition.md`

Carry the repaired shrinking-radius rule into a restartable full-vector
runner. Reuse the locked `epsilon=0.08` jobs, compute the missing direct and
crossed arguments at `epsilon=0.04` and `0.02` for the first two paired
scrambles within a four-hour boundary, and test regulator convergence of the
local `1-z^2` projection and each untouched nonlocal component. Do not fit the
5018 target or treat two scrambles as production precision.
