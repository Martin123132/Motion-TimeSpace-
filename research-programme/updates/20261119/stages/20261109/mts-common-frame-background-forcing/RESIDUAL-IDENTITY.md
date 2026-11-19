# Completing the numerical common-frame residual

The stored native pullback discrepancy must be retained as a separate source, not erased by a pass flag. With B = D_bridge and E = E_bg, the reconstructed native equation is

    y_N = (M + R + E + B)y.

Here B records the finite implemented pullback discrepancy. It may contain representation, approximation or arithmetic error; these pointwise checks alone do not identify its origin. Treating it as known zero would be unjustified.

For y_s = y_0 + delta_s and the already saved correction z, define w = y-y_s-z. With the inherited source conventions,

    w_N = (M+R+E+B)w + R z + (E+B)(y_s+z)
          + (R y_0-fhat) + g + (h-hhat).

Inherited initial and numerical errors remain separate. This stage evaluates E(y_s+z), B(y_s+z), and R z at the original source epochs; it does not integrate their unsampled history. E is a within-model background comparison, never baseline minus MTS.

The independently reconstructed identity is D_total y = E y + B y. Its algebraic check is normalized to the full pulled-back rate, with the small-forcing-relative residual also reported as a diagnostic. Subtracting nearly equal rates cannot establish a physically resolved tiny baseline forcing merely because the operator-scale identity passes. Every native pullback and carrier test is repeated for all six vectors, not only the final random vector.

Terminal readout differences are recorded at fixed native encoded state and normalized using the existing reference-output scales. They are not added to a prior prediction that may already use the original physical readout. Their purpose is to preserve the separate observable map in subsequent error propagation.
