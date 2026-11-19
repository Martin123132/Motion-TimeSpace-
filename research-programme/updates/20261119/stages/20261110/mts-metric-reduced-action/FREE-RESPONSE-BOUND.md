# Keep the free component; bound rather than assume away its effect

Let A=lambda0+lambda_k and Dn be a chosen local particular approximation.
The full physical response satisfies Dexact'+A Dexact=S0-R_k Z for an
on-shell carrier. Write epsilon_n=Dn'+A Dn-S0 and E=Dexact-Dn. Then

    E'+A E=-epsilon_n-R_k Z,
    U(t,s)=exp[-integral_s^t A],
    E(t)=U(t,ti)E(ti)-integral_ti^t U(t,s)[epsilon_n+R_k Z](s)ds.

This follows exactly from variation of constants; it is not a population
model. A nonzero E(ti) is a legitimate free fast component, not a term that
can be set to zero merely because a local fit prefers it. If
M=exp(integral_ti^tf |Re A|), the immediate bound is

    |E(t)|<=M[|E(ti)|+integral_ti^t(|epsilon_n|+|R_k Z|)ds].

For Dn=D0, the oscillatory improvement is more informative. Since
epsilon0=D0'=-A D1, integration by parts gives

    E(t)=D1(t)+U(t,ti)[E(ti)-D1(ti)]
          -integral_ti^t U(t,s)D1'(s)ds
          -integral_ti^t U(t,s)R_k(s)Z(s)ds.

Consequently

    |E(t)|<=|D1(t)|+M|E(ti)-D1(ti)|
                 +M integral(|D1'|+|R_k Z|).

This displays both the driven correction and the persistent free transient.
Initializing at D0 creates the -U D1(ti) term even if E(ti)=0. Initializing
at D0+D1 instead has epsilon1=D1', so the immediate bound above is already
small when the next defect is controlled. Neither choice fixes the earlier
cosmological preparation, and neither implies dissipation of the free mode.

The restricted action adds the explicitly derived epsilon/(2Wk) and R_j
terms. Its state error relative to unrestricted transport can be estimated
by integrating their difference and E through Z'=(lambda_k-lambda0)Z+D.
For Re(lambda_k-lambda0)=gamma, define
Mz=exp(integral|gamma|). With identical initial Z,

    |delta Z(t)|<=Mz integral(|E|+|epsilon_n|/(2Wk)
                         +|R_k Z_reduced|/(2Wk)+|C R_0|/(2Wk)).

This is a conservative norm inequality, not a claim that each signed term
adds constructively. Map it to observables using the explicit T and affine
D dependence; a small phase-coordinate error alone does not guarantee a
small density error. The preceding phase-rounding defect demonstrated why.

These formulas are mathematical bounds conditional on integrable coefficients
and the specified background. The existing W2 residual has a whole-interval
certificate. This stage's sampled D1/D1' diagnostics are NOT certified
suprema and must not be substituted into these integrals as rigorous bounds.
A future uniform reduction certificate must enclose these additional source
derivatives as well. The current direct comparisons retain their2e-5 scope.
