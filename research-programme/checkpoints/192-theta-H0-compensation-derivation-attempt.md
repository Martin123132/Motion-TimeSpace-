# 192 - Theta H0 Compensation Derivation Attempt

Private CMB/theory checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 191 showed:

```text
same-density MTS is mock-competitive after theta/H0 profiling,
and a linear H0 bridge predicts the CAMB profile root very well.
```

But it also flagged:

```text
the compensation is not parent-derived,
and the same-density CMB H0 conflicts with the late-reference H0.
```

This checkpoint attempts the next derivation:

```text
derive the sign and scale of the required H0 compensation directly from the
fixed-physical-density FLRW distance integral.
```

## 2. Machine Artifact

Script:

```text
scripts/theta_H0_compensation_derivation_attempt.py
```

Run:

```text
runs/20260601-000009-theta-H0-compensation-derivation-attempt
```

Command:

```text
python scripts/theta_H0_compensation_derivation_attempt.py --timestamp 20260601-000009
```

Status:

```text
theta_H0_compensation_FLRW_distance_law_partially_derived_parent_owner_still_missing
```

Claim ceiling:

```text
FLRW_compensation_law_internal_only_no_parent_derivation_no_CMB_claim
```

## 3. Derivation

Use:

```text
theta_* ~= r_s(z_*) / D_A(z_*).
```

In the same-physical-density family, write:

```text
q_LCDM^2(z) = h^2
            + omega_m [(1+z)^3 - 1]
            + omega_r [(1+z)^4 - 1],
```

where:

```text
q = H/100.
```

The locked MTS memory closure adds:

```text
q_MTS^2(z) = q_LCDM^2(z) + h^2 B_mem A(z).
```

The first-order distance response is:

```text
delta chi = -1/2 Integral[delta q^2 / q^3] dz.
```

To cancel the MTS distance deficit using a shift in `h`, the first-order
condition gives:

```text
delta ln h ~= -(B_mem / 2) <A>_{q^-3},
```

with:

```text
<A>_{q^-3} =
Integral[A(z)/q^3 dz] / Integral[1/q^3 dz].
```

This is the first real derivation bridge:

```text
MTS adds positive late expansion,
positive late expansion lowers D_A,
lowering H0 compensates the D_A loss.
```

## 4. Numerical Law

The integral gives:

| quantity | value |
|---|---:|
| fixed `omega_m h^2` proxy | `0.14301419153961778` |
| fixed `omega_r h^2` proxy | `0.000041769773884035365` |
| ordinary distance-weighted `<A>` | `0.9244151363439522` |
| response-weighted `<A>_{q^-3}` | `0.6609614177977554` |
| predicted `delta ln h` | `-0.024480052511027976` |
| predicted `H0` | `65.84759645550561` |

The actual CAMB profile root from checkpoint 188 was:

```text
H0 = 65.92050790786743.
```

So the FLRW integral law misses by only:

```text
-0.07291145236182217 km/s/Mpc.
```

The more local finite-difference bridge from checkpoint 191 misses by:

```text
-0.013476520486563004 km/s/Mpc.
```

## 5. What This Means

This is genuinely useful.

We can now say:

```text
The direction and scale of the same-density CMB H0 compensation are not random.
They follow from the FLRW distance response to the locked MTS memory term.
```

But we still cannot say:

```text
The parent MTS theory derives the compensation.
```

The bridge currently depends on:

```text
B_mem = 2/27,
p = 3,
u3 = 1/4,
same-physical-density CMB parametrization,
high-c_s effective perturbation closure.
```

Those are not all parent-owned yet.

## 6. Remaining Parent Gaps

| gap | why it matters |
|---|---|
| `B_mem` amplitude owner | compensation is linear in `B_mem` |
| activation law owner | response-weighted `<A>` sets the H0 shift |
| clock/calibration owner | same-density CMB H0 conflicts with late-reference H0 |
| exact perturbation owner | CAMB still uses high-cs effective fluid |
| local GR owner | fundamental theory still needs GR/PPN recovery |

The biggest new gap is not “can the CMB H0 shift be explained?”.

It is:

```text
which H0/calibration branch is parent-owned?
```

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| FLRW integral law predicts H0 profile scale | pass |
| local theta derivative predicts H0 profile | pass |
| parent theory derives compensation | fail |
| late-reference H0 consistency | warning |
| official CMB likelihood | not run |
| support claim allowed | fail |

## 8. Decision

Decision:

```text
theta_H0_compensation_FLRW_distance_law_partially_derived_parent_owner_still_missing
```

Meaning:

```text
The same-density H0 compensation is now partially derived as an FLRW distance
law. It is no longer just a numerical trick. But parent ownership is still
missing, especially for B_mem, activation, calibration/H0 ownership,
perturbations, and local GR.
```

Next target:

```text
193-calibration-bridge-H0-owner-or-demotion.md
```
