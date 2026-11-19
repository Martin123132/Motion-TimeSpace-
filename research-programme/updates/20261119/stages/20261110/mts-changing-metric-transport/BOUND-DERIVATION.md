# A true local interval bound, not a sampled residual

The initial values are the saved phi_s,v_s,H at the first z=10 slice,
treated as exact represented inputs for this conditional statement. The
standard-species cubic coefficients and matter budgets are also fixed inputs.
This does not certify their physical or calibration uncertainty.

The retained background ODE in N=ln a is

    phi_N=v/H,
    v_N=-2v-(a m_s)^2 phi/H,
    H_N=-(R+3P)/(6H).

Use the symmetric1%box about each initial coordinate, the entire saved
N interval and the original neutrino cubic segment. Rational interval
evaluation proves initial+[0,span]*RHS(box) is strictly inside the box for
all three coordinates. H stays positive and the vector field is smooth.
The first-exit/ODE-continuation argument therefore encloses the unique
solution over the full interval. No sampled maximum supplies this step.

All interval endpoints are rational. Each operation rounds its lower and
upper endpoint outward onto a192-bit dyadic grid. For exp(x), halve until
|x|<=1/8; sum through degree48 and enclose the tail by
|term48| |x|/49 /(1-|x|/50), then square outward back to the original scale.
This is absolute outward arithmetic, not192bits of cosmological accuracy.

Evaluate the stress-derived H',H'',H''' within that box. For all0<=k<=5,
1<=omega/mu<=1+25/(2mu_min^2). The91-term rational numerator is bounded
by its coefficient absolute sum on these intervals, while its denominator
and W2 are separately proved positive. Integrate the residual-rate upper
bound using duration<=span/H_min. For both retained backgrounds this gives

    B=integral |R_W|/W <=2.270e-24.

Exact rational bounds are stored; the displayed decimal is rounded upward.
The old constant-H certificate is not used. This is a coefficient-norm
truncation bound for the exact retained ODE and identical microscopic
initial state, not for source interpolation or binary64 calculations.

The prior variation-of-constants lemma applies without change:

    ||c_k-c_k,bar|| <= [exp(Bk)-1]||c_k,initial||
         +[exp(Bk+B0)-1]J||c0,initial||,
    J=integral||Yk^-1 F Y0||.

The force matrix remains F=[[-HC,C],[mu^2D-H^2C,HC]], C=Psi+3Phi,
D=3Phi-Psi. The box also bounds W, W'/W^2 and hence J's coefficients.
A bound on the supplied source polynomial and a separate source-error
envelope complete the forced estimate. Uncertain initial data is an
additional term, not a number silently set to zero in an observational claim.

Because stored initial H need not satisfy the Friedmann equality with
mathematical exactness, use the general W2 expression for the certificate.
The equivalent stable beat uses P_effective=-(2H'+H^2). It reduces to true
scaled pressure on the exact constraint surface. No initial constraint
rounding is erased by silently substituting P_effective=P.

Numerical transport samples the saved background through a smooth value
interpolant and derives pressure jets from the retained equations. Its
interpolation/rounding error is separate from this exact-ODE certificate;
direct field and background-resolution comparisons must check it.

Finally, saved perturbations are linear transfer coefficients. The prepared
carrier perturbations test derivatives of a state with respect to the seed,
not a finite-amplitude realization. Large phase transfer does not justify
using psi approximately1+iS globally or selecting a local halo occupation.
