# 260 - C3 Unit Stress Normalization Parent-Action Attempt

Private derivation checkpoint. This directly attacks the hard condition from
259:

```text
C3_unit_stress_normalization:
metric variation gives rho_mem/rho_c0 = [Tr(P_active)/dim(V_cell)] F(N)
with no independent lambda_mem.
```

Result:

```text
C3a stress-form variation is conditionally derived.
C3b unit scale-lock is not derived.
```

So this is progress, but not amplitude promotion.

## 1. Trigger

The previous checkpoint proved:

```text
Bianchi fixes the pressure response,
not kappa_mem.
```

The exact next question is whether the parent memory action can produce the
right stress with unit normalization.

## 2. Machine Artifact

Script:

```text
scripts/C3_unit_stress_normalization_parent_action_attempt.py
```

Run:

```text
runs/20260601-000078-C3-unit-stress-normalization-parent-action-attempt
```

Command:

```text
python scripts/C3_unit_stress_normalization_parent_action_attempt.py --timestamp 20260601-000078
```

Status:

```text
C3a_metric_variation_stress_form_derived_C3b_unit_scale_lock_not_derived
```

Claim ceiling:

```text
partial_C3_derivation_no_unit_amplitude_promotion
```

## 3. The Useful Derivation

Use the FLRW reduced memory action:

```text
S_mem = - int dt lapse a^3 A_mem q F(N)
```

where:

```text
N = ln(a0/a),
q = r_active/D_cell.
```

Lapse variation gives:

```text
rho_mem = A_mem q F(N).
```

Scale-factor variation gives:

```text
p_mem = -rho_mem - (a/3) d rho_mem/da.
```

Since:

```text
dN/da = -1/a,
```

this becomes:

```text
p_mem = -rho_mem + (1/3) d rho_mem/dN.
```

That exactly matches the Bianchi pressure law from checkpoint 259.

So we have a real partial derivation:

```text
an FLRW memory action can own the stress form,
not merely assume a pressure closure.
```

## 4. The Factorization Problem

The dimensionless amplitude is:

```text
B_mem = (A_mem/rho_c0) q.
```

Equivalently:

```text
kappa_mem = A_mem/rho_c0.
```

Therefore:

```text
B_mem = 2/27
```

requires all of:

```text
D_cell = 27,
r_active = 2,
A_mem = rho_c0.
```

The first two are the rank theorem. The third is the unit scale-lock theorem.

This checkpoint derives the stress-form gate, but not:

```text
A_mem = rho_c0.
```

## 5. Parent-Action Routes

The route matrix is:

```text
pure topological wedge parent:
  good for local silence,
  fails to produce FLRW stress amplitude.

FLRW volume memory potential:
  derives rho and p form,
  leaves A_mem free.

critical-density inserted action:
  gives kappa=1 only by typing rho_c0 into the action.

geometric EH scale-lock:
  gives B_mem = q (H_star/H0)^2,
  so it works only if H_star = H0 is derived.

four-form / flux memory:
  may quantize an amplitude,
  but does not currently select rho_c0.

Lagrange multiplier density constraint:
  enforces the target by constraint,
  not a derivation unless the constraint itself is parent-owned.
```

The best honest route is now:

```text
geometric_EH_scale_lock
```

but it reduces the missing theorem to:

```text
H_star = H0.
```

## 6. The Split C3 Gate

The original C3 was too coarse. It now splits into:

```text
C3a_metric_variation_stress_form:
  derived conditionally.

C3b_unit_scale_lock:
  not derived.

C3c_local_silence_compatibility:
  open.
```

This is the cleanest current status.

## 7. No-Go Lemmas

The key no-go is:

```text
unit scale rescaling no-go:
replace A_mem by lambda A_mem.
```

The stress form, pressure law, Bianchi identity, and data pipeline all still
work, but:

```text
B_mem -> lambda B_mem.
```

Therefore no stress-form derivation alone can prove:

```text
lambda = 1.
```

That has to come from a separate scale-lock theorem.

## 8. Decision

Decision:

```text
C3a_metric_variation_stress_form_derived_C3b_unit_scale_lock_not_derived
```

Meaning:

```text
the theory now has an honest FLRW action-level route for the memory stress
shape and pressure, but the unit amplitude is still not parent-owned.
```

Allowed:

```text
C3a is conditionally derived.
fixed 2/27 remains the clean lead empirical closure.
```

Forbidden:

```text
C3 is fully derived,
kappa_mem=1 is proved,
B_mem=2/27 is parent-owned.
```

## 9. Why This Helps

This narrows the actual missing mathematics.

We no longer need to vaguely ask:

```text
where does memory stress come from?
```

We now ask:

```text
can the parent action derive H_star = H0,
or an equivalent A_mem = rho_c0 boundary scale-lock,
while preserving local vacuum silence?
```

That is a much sharper problem.

## 10. Next Target

Next:

```text
derive or reject H_star = H0 boundary scale-lock
and check local silence compatibility.
```

If it works, the 2/27 branch starts moving from closure toward theorem. If it
fails, fixed 2/27 remains a very clean empirical closure branch, not a derived
field-theory amplitude.
