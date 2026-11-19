# Accumulating the next feedback without changing the theory

The accepted slow approximation ys=y0+delta_s satisfies ys_N=M ys+fhat-g. The source stage calculated h=R_total delta_s with the full transformed operator. Define the next Duhamel response
    z_N=M z+h,   z(N0)=0.
Its initial zero is the zero additional response on the retained interval: it does not replace the inherited physical mode or assert that inherited errors vanish.

For each physical terminal row ell, solve the source-independent dual lambda_N=-M^T lambda, lambda(T)=ell. Then
    ell z(T)=integral(lambda^T h dN).
The prior stage's same-operator full-hierarchy adjoints and terminal maps can be reused. If interpolating the saved adjoint endpoint states, distinguish interpolation from original time-integration accuracy and check it against forward propagation.

For z computed from a retained interpolated source hhat, the remainder w=y-ys-z obeys
    w_N=(M+R+E_bg)w
         +R z+E_bg(ys+z)+(R y0-fhat)+g+(h-hhat),
plus the inherited initial discrepancy and numerical defects. Thus z explicitly removes the hhat source from the total residual, but does not remove R z or make a total-error certificate by itself.

## Numerical representation and unchanged gates

Use all saved phase harmonics in the real Fourier representation; no dropped Nyquist or high-order terms. Freeze nine original source times; use the five-node restriction solely as an interpolation control. Mean operator, background, initial mode and physical hierarchy remain unchanged.

Integrate separate normal-form/map response components and both metric branches. Normalize each response component by the maximum source-vector norm over its nine retained source nodes and phase grid. For an exactly zero component use scale one. This invertible constant scaling preserves z_N=M z+h while preventing an absolute solver tolerance from discarding a tiny nonzero source. Keep the original DOP853 tolerances and4096/2048 maximum-step controls.

At the terminal epoch, reuse the existing ten physical readouts and original reference scales. Report separately:
- forward time-step change relative to each feedback component;
- nine/five-source interpolation change relative to each feedback component;
- corresponding changes relative to original physical outputs;
- change to the previously saved ys prediction.

An unresolved strict relative source control is not a model failure or a physical-pass claim: retain its measured uncertainty and identify the next independent source test. Small effects must not be promoted to total closure, nor large relative fluctuations in tiny baseline rounding-level sources mistaken for observable instabilities.

## Adjoint reuse

The existing adjoint files retain64 chunk endpoints, not their interior solutions. If reused for a new source, construct an explicitly labeled Hermite interpolant using -M^T lambda at those saved endpoints; compare64/32-chunk interpolation and the two original adjoint integration step sizes. Apply quadrature refinement and compare signed results with the newly propagated z before accepting a numerical Cauchy budget. This is not an analytic continuous-source enclosure.

