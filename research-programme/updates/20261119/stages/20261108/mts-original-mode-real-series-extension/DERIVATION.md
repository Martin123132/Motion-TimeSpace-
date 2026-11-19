# Exact real-series contraction and longer original-mode transport

Parent: ../mts-contiguous-mode-extension-20261108 (seal8593146437412d04d2a1ee90806f85090580a809fb16fc9b60974335f4374f3d). Its DERIVATION.md supplies the unchanged equation y_N=M y+R y, the boundary-map correction and the initial-error transport identity. This stage advances the same candidate; it does not select new physical initial data.

## Real representation without a harmonic cutoff

For any complex finite coefficient arrays a_k (not assuming conjugate symmetry),

    Re[a_k exp(2ik theta)+a_-k exp(-2ik theta)]
      = (Re a_k+Re a_-k) cos(2k theta)
        + (Im a_-k-Im a_k) sin(2k theta).

The zero mode contributes Re a_0. For an even grid with P phase nodes, the FFT's single Nyquist mode is k=-P/2 and contributes

    Re a_Nyquist cos(P theta)+Im a_Nyquist sin(P theta).

Both Nyquist terms are retained. The imaginary zero mode makes no contribution to the original real-valued polynomial. No Hermitian assumption is imposed on roundoff: coefficient pairs are combined exactly as above. For the baseline's one-point polynomial only its real constant contributes. Every original coefficient's contribution to the real polynomial is therefore represented. This is a real-coordinate transformation of the same finite polynomial, not smoothing, harmonic truncation, projection onto a smaller physics model or fitted low-rank compression.

The transformation is real-linear and commutes in exact arithmetic with the retained real-knot cubic interpolation in N. The original two complex-valued splines and contractions can consequently be evaluated as one real spline and real matrix-vector product. Normal-form and coordinate-map components remain separately propagated. Rounding is tested against the original evaluator, including deliberately non-Hermitian synthetic inputs and all saved baseline/MTS source families. The previous half-wavenumber evolution is then repeated with the identical coefficients and steps as an independent end-to-end representation test before new predictions are accepted.

## Continuation, uncertainty and comparisons

The new y0 starts at the parent's corrected endpoint. The new increment starts at zero; this does not reset the inherited physical mode. Full boundary operators act on the updated incoming vector. The phase, global invariant normalization, slow backgrounds and complete G192 remote tails are inherited. The next .04 e-fold interval is selected from the original reference TIME GRID before inspecting its perturbation values. Time-step counts double with interval length; coefficient/phase grids and all original tolerances remain unchanged.

Carry previous discrepancy and numerical controls with the explicit identity

    e(N)=U(N,N_b)e(N_b)+integral[U(N,s)d(s) ds].

For exact first-response equations on the chosen background the new defect is -R delta. Source interpolation, integration, representation rounding and the true-background mismatch are separately named contributions. Measured controls do not become a uniform propagator bound by assumption. Test both models, all three wavenumbers, GR and spatial-Poisson, the ten original channels and five frozen probes. Observe accumulated error rather than resetting to the reference to manufacture agreement.

