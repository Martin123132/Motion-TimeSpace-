# Why the two source contributions can be added

Let N denote the saved e-fold coordinate, M(N) the unchanged retained linear evolution operator, and y_app(N) the saved five-channel approximation including its original periodic correction. This stage evaluates the background-generator source r_bg(N)=E_bg(N)y_app(N), where E_bg=T^{-1}(F_reference-F_retained)T in the common retained coordinates. Each native generator uses its own physical H in the original conversion to N. The source is not made zero for the baseline.

For an isolated linear response w_N=Mw+r_bg and a fixed terminal observable row ell, define lambda_N=-M^T lambda, lambda(N_f)=ell. Direct differentiation gives

    d(lambda^T w)/dN = lambda^T r_bg.

Consequently the background-source contribution to that terminal observable from a cell [N_a,N_b] is I_ab=integral(lambda^T r_bg dN). On adjacent cells [N_0,N_1] and [N_1,N_2], I_02=I_01+I_12. The SAME final-epoch adjoint is used on both cells, so no additional propagator is inserted between these integrals. The inherited physical current is not reset. A shared finite endpoint has zero integration measure; no delta-function interface source has been introduced. Incoming contributions already accounted for by I_01 must not be added a second time as an independent initial-condition response.

For MTS the integration uses the original monotonically increasing phase: dN=dtheta/omega(N,theta). The positive phase derivative of each saved DOP853 polynomial is certified by exact rational Bernstein coefficients. The difference between its inverse derivative and the original physical clock evaluated at the quadrature nodes is retained as a separate numerical control. The baseline has no heavy relative phase and is integrated directly in N.

For g=lambda^T r_bg, Cauchy-Schwarz gives |I_ab| <= sqrt((N_b-N_a) integral(g^2 dN))=B_ab. Thus |I_01+I_12| <= B_01+B_12. These are exact identities/inequalities for the indicated functions; our saved B values evaluate their integrals numerically. Nested quadrature and time/phase controls do not by themselves certify the continuum error of the original physical solution.

Numerical changes are retained both signed and as sums of absolute cell changes. In particular, |delta I_01+delta I_12| <= |delta I_01|+|delta I_12|. A combined numerical pass additionally requires both cells to pass separately, so cancellation cannot hide a failing cell. This applies equally to baseline and MTS. Current, source-phase and their cross term remain separate, with E_c y_c-E_f y_f=E_f delta_y+delta_E y_f+delta_E delta_y.

This calculation isolates the E_bg y_app term in the saved full residual identity. It is not a replacement for the other bridge, feedback, approximation and final readout-map terms. Values divided by reference_scale refer to the existing terminal comparison normalization, not observational fit scores or a universal cosmological amplitude. This stage extends the original branch and preparation; it does not introduce a new theory or fit parameter.
