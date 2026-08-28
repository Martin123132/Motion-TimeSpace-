# 5345 - D4 Regulator-Zero Endpoint Asymptotic and Fit Preregistration

Date: `2026-08-10`

Formal marker: `MTS_5345_D4_REGULATOR_ZERO_NORMAL_FORM_PREREGISTRATION`.

Private derivation checkpoint. No GitHub action, no edit to
`formalization-workbench`, and no regulator-zero, local-GR or full-MTS claim.

## Executive result

The D4 regulator-zero fit is now derived and preregistered before the second
finite rung is known. This prevents choosing whichever extrapolation happens
to give the most attractive intercept.

For every separated transverse pole-support contact, checkpoint 5337 gives

```text
z0_e(epsilon)=a_e epsilon+O(epsilon^2),
x_e(epsilon)=x_e(0)+O(epsilon^2).
```

Checkpoints 5339 and 5342 derive the complete local outer-integrand form

```text
F_e(delta,epsilon)
 =s_e(C0_e+C1_e delta) Log[z0_e(epsilon)+z1_e delta].
```

Its exact primitive contains both `z Log z` and `z^2 Log z`. Therefore the
parent topology fixes

```text
I_D4(epsilon)
 =I0
 +A epsilon Log(epsilon/epsilon_ref)
 +B epsilon
 +O(epsilon^2 Log epsilon),

epsilon_ref=0.0025.
```

The complete second-order family is

```text
I_D4(epsilon)
 =I0
 +A epsilon Log(epsilon/epsilon_ref)
 +B epsilon
 +C epsilon^2 Log(epsilon/epsilon_ref)
 +D epsilon^2
 +O(epsilon^3 Log epsilon).
```

No `sqrt(epsilon)` term belongs to the derived family because the physical
event gaps approach nonzero constants while the regulator widths vanish
linearly. Half-power fits remain falsifiers only.

## 1. Exact coefficient law

Writing

```text
a_e=lim_(epsilon->0) z0_e(epsilon)/epsilon,
```

the coefficient of the leading event logarithm is

```text
A_e=-s_e C0_e a_e/z1_e.
```

This follows from the lower endpoint of the exact primitive, not from a fit.
At finite regulator the source estimator is

```text
A_e(epsilon)
 =-s_e C0_e(epsilon) z0_e(epsilon)/[epsilon z1_e(epsilon)].
```

For the four two-sided support contacts already derived at `E00125`,

```text
sum_(E01,E02,E03,E08) A_e
 =0.000380062060684
  +0.470737108591 i,

|sum A_e|/sum|A_e|
 =0.9999999726.
```

These four contributions reinforce rather than cancel. The E08 imaginary
coefficient agrees between `E0025` and `E00125` at better than `1e-5`
relative. This is strong evidence that the logarithmic term is real
regulator structure rather than numerical drift.

It is not yet the total `A`: the four one-sided branch-death coefficients
`E04-E07` remain unevaluated. Exact total cancellation is not assumed either
way. A fixed-`A` fit is forbidden until all eight coefficients are evaluated
at two or more regulators.

## 2. Rung-count theorem

The leading family has three complex parameters `(I0,A,B)`. Consequently:

```text
2 accepted rungs -> underdetermined;
3 accepted rungs -> exactly determined, no residual test;
4 accepted rungs -> minimum overdetermined leading-family gate.
```

The complete second-order family has five complex parameters. Therefore:

```text
5 accepted rungs -> exactly determined;
6 accepted rungs -> minimum overdetermined complete-family gate;
7 accepted rungs -> preferred full stability ladder.
```

The geometric seven-rung designs are full rank after column normalization,
and all condition-number times machine-epsilon checks pass. This is a design
certificate only; it does not replace finite integral values.

## 3. Frozen acceptance contract

The future zero-fit runner must use the following rules without changing them
after seeing the intercept:

1. Every input must be an independently accepted D4 finite-rung value with a
   conservative complex disk.
2. Four rungs are the minimum for an overdetermined leading-family fit.
3. A zero limit may pass only if the conservative intercept envelope is below
   `1%` relative.
4. The envelope includes input disks, weighted/unweighted shift,
   leave-one-out spread, smallest-epsilon-window shift, normalized complex
   residuals, and leading-versus-second-order model shift.
5. With only four or five rungs, a source-derived remainder bound is required
   because the complete second-order family is not overdetermined.
6. At six rungs the complete second-order family becomes independently
   testable; seven remains preferred.
7. Analytic-only fits may be reported only as cancellation diagnostics.
8. Half-power fits may be reported only as topology-excluded falsifiers.
9. No fit may promote the decay-angle, full phase-space, UV, local-GR or
   full-MTS claim.

At preregistration time only `E0025` is accepted. The active `E00125` worker
therefore cannot by itself establish a zero limit even if it passes.

## 4. Immediate execution sequence

```text
1. finish and validate E00125;
2. evaluate E04-E07 one-sided A_e coefficients without changing the parent;
3. run E000625 next, reusing its already-derived event geometry;
4. acquire at least E005 as the fourth accepted finite rung;
5. execute the frozen leading-family gate;
6. continue to six/seven rungs if the remainder envelope does not close.
```

The sequence is derivation-first: it uses the endpoint primitive to reduce
the model family and then asks the numerical ladder to falsify that family.
It does not infer the regulator law from whichever four points are cheapest.

## Reproducibility

Run:

```text
post-checkpoint-work/.venv-score/Scripts/python.exe -B
post-checkpoint-work/scripts/
Y5_R2FR_5345_D4_regulator_zero_normal_form_preregistration.py --dry-run

post-checkpoint-work/.venv-score/Scripts/python.exe -B
post-checkpoint-work/scripts/
Y5_R2FR_5345_D4_regulator_zero_normal_form_preregistration.py

post-checkpoint-work/.venv-score/Scripts/python.exe -B
post-checkpoint-work/scripts/
Y5_R2FR_5345_D4_regulator_zero_normal_form_preregistration.py --validate-saved
```

All output rows keep every regulator-zero and broader claim flag false.
