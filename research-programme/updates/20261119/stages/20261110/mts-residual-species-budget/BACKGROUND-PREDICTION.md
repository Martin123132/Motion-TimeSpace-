# Frozen thermal-background prediction

The independent continuum comparison rejected the hypothesis that the
five-node perturbation rule alone explains the full mismatch. Preserve that
failed gate. The continuum enthalpy identity holds, but the native background
is about 9.30e-6 below that continuum reference, while the five-node rule is
about 1.12e-6 above it. The sum, not either alone, must explain the mismatch.

Reproduce the actual native `nuRhoPres` q=0..30, 100-step endpoint-corrected
sum and the 1400-point am table with its own spline-derivative recurrence.
This is a separate reference implementation, not a native-background edit.
Compare its rho+P directly with the previously extracted native value. Then
refine ONLY that diagnostic integration to 200,400,800 steps and compare
with the already computed adaptive continuum integral.

For f(q)=[q^2 sqrt(q^2+m^2)+q^4/(3 sqrt(q^2+m^2))]/(exp(q)+1), the lower
endpoint has f'(0)=0 and f'''(0)=-3m/2. Euler-Maclaurin therefore predicts

    continuum - native = m h^4/(480 C)
        + (5m/2-25/m)h^6/(30240 C) + O(h^8) + upper-tail terms,
    C=7 pi^4/120, h=30/nq.

Derive the h^8 coefficient from the same Taylor series before evaluating
the saved temperatures. No coefficient is fitted to the observed errors.
The finite upper-tail approximation and interpolation errors must remain
separate. This can explain and bound a numerical source mismatch without
introducing an MTS coupling or replacing the frozen production background.
