# 5233 - Outer-pole-subtracted patch quadrature smoke

## Result

Decision: `ADOPT_POLE_SUBTRACTED_PATCH_QUADRATURE_AND_BUILD_FULL_FAMILY_ATLAS`.

Checkpoint 5232's subtraction contract has now been executed, not merely
listed as a future target.  For each of the two independent factorization
poles and both E040/E020 regulators, the regular numerator `D(q) T(q)` was
fitted locally, continued to the complex pole, and divided by `D'(q_*)` to
obtain the outer residue.

The maximum cubic numerator-fit residual is
`8.50926692e-07`.

## Patch integral

On the symmetric patch `q_*^R +/- 0.01`, the calculation is

```text
integral T dq
  = integral [T - R/(q-q_*)] dq
    + R [Log_F(q_max-q_*) - Log_F(q_min-q_*)].
```

The same Gauss-Legendre nodes were used for the raw and regularized terms.
Order 1024 provides an independent direct finite-regulator crosscheck.

- `fresh_g1_decay_pole` `E040`: raw order-32 error `0.665008562`, subtracted order-32 error `2.20913874e-07`, improvement `3010261.64x`.
- `fresh_g1_decay_pole` `E020`: raw order-32 error `0.827860112`, subtracted order-32 error `1.74181433e-07`, improvement `4752860.85x`.
- `old_g2_soft_energy_pole` `E040`: raw order-32 error `0.533701138`, subtracted order-32 error `8.45301794e-05`, improvement `6313.73483x`.
- `old_g2_soft_energy_pole` `E020`: raw order-32 error `0.752596936`, subtracted order-32 error `7.99880405e-05`, improvement `9408.86828x`.

The raw order-32 integrals miss at least half of the answer in every case.
The subtracted order-32 integrals agree with the order-1024 subtracted
reference within `0.0001`.  The
high-order raw integrals then approach the same answer, confirming that the
analytic logarithm has the correct normalization and causal branch.

## Interpretation

The earlier pooling failure was not evidence that the local double-residue
identity was wrong.  It was the expected failure of low-order random
quadrature on an unresolved Feynman pole.  Analytic subtraction removes that
pole while retaining its principal-value and signed residue contribution.

This checkpoint validates the method on local active patches only.  It does
not yet prove that every A00 factorization channel has been enumerated, and
it does not establish the numeric UV coefficient, local GR, or full MTS.

## Next target

Build the complete active-family outer-pole atlas and apply this validated
subtraction to the full A00 integrand before any new pooled estimator is run.
