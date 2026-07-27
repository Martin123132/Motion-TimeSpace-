# 5225 - Permutation-control multiplier theorem and raw salvage

## Result

Checkpoint 5224 completed all `520/520` jobs with no failed or
unconverged job, but its frozen unit-multiplier control failed exactly as
the protocol required it to fail. The final decision is
`RETIRE_BETA_ONE_KEEP_ZERO_IDENTITY_AND_BUILD_DIRECT_SLOT_BALANCED_PAIR`.

This is an estimator correction, not a contradiction in the MTS amplitude.
The zero-mean permutation identity survives. The claim that permutation
symmetry fixes the *external* control multiplier to one does not.

## Exact multiplier theorem

Let

`C = Y13 - (w1/w3) Y31`, with `E[C]=0`.

For any deterministic multiplier `beta` chosen independently of the
evaluation sample,

`F_beta = F - beta C`

is unbiased, and

`Var(F_beta) = Var(F) - 2 beta Cov(F,C) + beta^2 Var(C)`.

Thus `beta*=Cov(F,C)/Var(C)` minimizes variance. Symmetry fixes the
internal reweighting `w1/w3`; it does not select `beta=1`. The historical
checkpoint-5214 identity remains valid, but its unit-multiplier wording is
superseded here.

## What the scaled test established

- Fresh events: `24`.
- Fresh raw-control correlation:
  `0.00517122324`.
- Fresh post-hoc optimum `beta`:
  `0.00176530119`
  (diagnostic only).
- Unit-`beta` A00 SD ratio:
  `3.09045649`.
- Pilot-derived `beta=1.04685792` applied unchanged to the fresh
  sample gives SD ratio
  `3.22064267`.
- The two fresh tranches select opposite/near-zero empirical multipliers:
  `-1.24275094` and
  `0.00102277094`.

The largest fresh control has `|C|=4714.73032`
and a rootwise partition-ratio magnitude up to
`389.733867`. Across the sample the
maximum ratio is
`389.733867`.
The ratio `(E3/E1)^2` therefore creates an importance-reweighting tail that
was not controlled by the small pilot. Infinite variance is not claimed:
square integrability remains unproved.

## Raw-estimator salvage

Removing the rejected control gives:

- Fresh `2+24`:
  `K_mu=-347.638839-112.205066 i`,
  with real/imaginary SE
  `329.538498` /
  `91.3950778`.
- Compatible raw pool `4+36`:
  `K_mu=-77.5051915-99.9102817 i`,
  with real/imaginary SE
  `509.084139` /
  `64.6477753`.

Both remain tail/precision non-claims. The useful result is that the raw
calculation is finite and recoverable; the failed unit control did not
destroy the underlying event data.

## Derived next route

The next estimator should pair *directly evaluated channels*, not
importance-reweight one source family:

`A3 = 3 w3 F3(q3)`,

`A1 = 3 w1 F1(q1)`,

`A_pair = (A3 + A1)/2`.

Under the exact `g1<->g3` chart bijection,
`E[A1]=E[A3]=I`. If the channels are square-integrable and identically
distributed,

`Var(A_pair) = (Var(A3)+Cov(A3,A1))/2 <= Var(A3)`.

This follows from Cauchy-Schwarz and gives a genuine non-increase theorem.
Each channel uses its own bounded partition weight; no `w1/w3` factor is
allowed. The next implementation must derive the chart Jacobian, make the
topology/homotopy code slot-agnostic, and blind-test the paired estimator.
If that map cannot be built, the fallback is a newly allocated raw run,
not a post-hoc retuning of `beta`.

## Claim boundary

No numerical UV coefficient, local-GR result, galaxy result, or full-MTS
claim follows. The crossed-`hhh` coefficient remains unresolved, and the
other cut classes remain outside this calculation.

## Evidence

- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5225\control_multiplier_and_raw_salvage.json`
- Event influence: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5225\permutation_control_event_influence.csv`
- Next-estimator contract: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5225\slot_balanced_estimator_contract.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5225_VALIDATION.csv`
