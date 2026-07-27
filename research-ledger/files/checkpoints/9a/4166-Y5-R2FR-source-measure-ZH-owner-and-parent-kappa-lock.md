# 4166 - Source-Measure ZH Owner And Parent Kappa Lock

Timestamp UTC: `2026-07-03T01:03:18+00:00`  
Branch: `MTS_R2FR_Y5_ZH_SOURCE_MEASURE_AND_KAPPA_LOCK_4166`  
Decision: `ZH_COMMON_SOURCE_FACTOR_SPLIT_AND_KAPPA_LOCK_CONTRACT_DERIVED_ZH_ONE_ONLY_AS_NORMALIZATION_GAUGE`

## Recovery Note
This checkpoint continues from the verified drive-upgrade recovery bookmark:

```text
post-checkpoint-work/000-recovery-bookmark-20260703-drive-upgrade.md
```

## Coupling Throat
4165 left:

```text
kappa_eff = kappa_* Z_H,
G_N = c^4 kappa_* Z_H/(8*pi).
```

The new result is the source-measure split:

```text
Z_H = Z_0 exp(delta_ZH).
```

`Z_0` is one common source normalization. It can be absorbed into:

```text
kappa_bar = kappa_* Z_0.
```

This means `Z_H -> 1` is not a miracle. It is a legitimate local normalization gauge only after all physical leak channels in `delta_ZH` vanish or are bounded.

## Physical Leak Vector
The physical content is:

```text
D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH,
A in {time,species,frame,range,environment,readout}.
```

So measured `G_N` can hide one common factor, but cannot hide:

- time drift;
- species/source-composition dependence;
- frame/readout dependence;
- range dependence;
- local-environment leakage.

## Conditional ZH Theorem
If the parent matter/source measure descends to one common Hilbert source factor and all leak channels vanish, then:

```text
Z_H=Z_0,  kappa_bar=kappa_*Z_0,  Z_H -> 1.
```

This is a conditional private theorem inside the PPC4161 local branch. It is not a public local-GR claim and not a prediction of the numerical value of `G_N`.

## Kappa Lock
The remaining parent question is now sharp:

```text
D_A ln kappa_* = 0
```

must follow from a parent topological/superselection sector, or else `kappa_bar=8*piG_N/c^4` remains an empirical calibration exactly as in GR.

## Next Target
`4167-Y5-R2FR-topological-kappa-star-lock-or-ZH-derivative-bound.md`

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_ZH_FACTORIZATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_ZH_LEAK_CHANNELS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_KAPPA_LOCK_CONTRACT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_THEOREM_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_VERDICT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_CLAIM_FIREWALL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4166_NEXT_TARGET.csv`
