# Activation Regularity Repair Gate

## 1. Purpose

This file follows:

```text
45-memory-scalar-reconstruction-gate.md
```

The question is:

```text
What must an activation law satisfy before it can be parent-safe rather than a
fitted fractional onset, and what happens if we repair it?
```

Short answer:

```text
the current fractional Weibull activation fails the parent-safe regular action
gate. C2-safe replacement candidates exist, but every replacement must be
retested empirically from scratch before inheriting any closure survival.
```

This is the discipline gate: smoothness does not get to sneak in as a new fit.

## 2. Machine Run

Implemented:

```text
scripts/activation_regularity_repair_gate.py
```

Successful run:

```text
runs/20260531-013929-activation-regularity-repair-gate/status.json
```

Readout:

```text
activation_regularization_gate_requires_C2_parent_safe_retest_no_promotion
```

Generated:

```text
runs/20260531-013929-activation-regularity-repair-gate/results/source_checkpoint_register.csv
runs/20260531-013929-activation-regularity-repair-gate/results/activation_regularity_requirements.csv
runs/20260531-013929-activation-regularity-repair-gate/results/candidate_activation_laws.csv
runs/20260531-013929-activation-regularity-repair-gate/results/candidate_background_deviation.csv
runs/20260531-013929-activation-regularity-repair-gate/results/same_test_retest_manifest.csv
runs/20260531-013929-activation-regularity-repair-gate/results/activation_repair_gates.csv
runs/20260531-013929-activation-regularity-repair-gate/results/decision.csv
```

## 3. Parent-Safe Requirements

A support-capable activation law must satisfy:

```text
F(0)=0 and 0 <= F <= 1 on the physical branch;
F'(0)=0 so the source switches on smoothly;
C2 endpoint regularity;
finite canonical dV/dphi if using the scalar proxy;
real time-domain extension through N=0;
no new rescue knobs;
same-test empirical retest.
```

For an endpoint law:

```text
F(N) ~ N^p
```

the scalar-action safety threshold is:

```text
p >= 3
```

The current fitted branch has:

```text
p = nu_act = 1.7500073382761008
```

So it fails.

## 4. Candidate Repairs

The gate tested six candidates:

```text
original_fractional_weibull;
weibull_p3_match_N50;
weibull_p4_match_N50;
hill_p3_match_N50;
hill_p4_match_N50;
regularized_fractional_p3_Nreg_0p05.
```

No-knob C2/C1 candidates exist:

```text
weibull_p3_match_N50;
weibull_p4_match_N50;
hill_p3_match_N50;
hill_p4_match_N50.
```

The original fails:

```text
C2 endpoint: fail;
canonical C1 potential: fail;
real time-domain status: fail without a load invariant.
```

The two-scale regularized fractional option is shape-preserving-ish, but it adds
a new scale, so it is not the clean first choice.

## 5. Background Deviation

Regularity-safe repairs are not identical to the fitted branch.

Best small CMB-distance deviation among tested repair candidates:

```text
candidate = hill_p4_match_N50
fractional Delta D_M(z_star) vs original = 1.9633995319567887e-05
```

Low-redshift shape changes are still nonzero:

```text
weibull_p3_match_N50 max |Delta F| over z=0..2 = 0.1491318170836342
weibull_p4_match_N50 max |Delta F| over z=0..2 = 0.218505400287057
hill_p3_match_N50 max |Delta F| over z=0..2 = 0.07512874582181488
hill_p4_match_N50 max |Delta F| over z=0..2 = 0.1328510463034086
regularized_fractional_p3_Nreg_0p05 max |Delta F| over z=0..2 = 0.05388920870808467
```

So the conclusion is strict:

```text
no repaired activation law inherits the old fitted result.
```

It has to survive the same tests again.

## 6. Gate Results

Passed:

```text
C2/C1 no-knob repair candidates exist;
next background smoke is authorized.
```

Failed:

```text
original fractional Weibull parent-safe action;
repair preserves background without retest;
support claim after defining repair;
official CMB support readiness.
```

This means the repair is a real theory move, not a bookkeeping move.

## 7. Same-Test Retest Manifest

Required order:

```text
1. Predeclare one repaired activation candidate.
2. Run late-background smoke against LCDM, wCDM, CPL, original C0, and repaired C0.
3. Repeat compressed CMB and growth/H(z) checks without moving parameters.
4. Only later consider official spectra/lensing after perturbation closure.
5. Parent derivation remains mandatory for theory promotion.
```

No evidence language is allowed until the repaired branch earns it.

## 8. Decision

Decision:

```text
original_fails_parent_safe_regular_action_gate
```

and:

```text
C2_safe_candidates_exist_but_require_same_test_retest
```

Meaning:

```text
the fitted shape was useful as an empirical scout;
it is not yet a fundamental activation law;
regularity-safe replacements are possible but must face data honestly.
```

## 9. Next Target

Create:

```text
47-C2-activation-background-smoke.md
```

Purpose:

```text
run a short no-rescue background smoke for the C2-safe activation candidates
against the original C0 and standard baselines. If regularity destroys the
background signal, the scalar-action route is demoted. If one survives, it
becomes the next disciplined closure candidate.
```

That is the right next move: theory regularity just made a new empirical bet.
