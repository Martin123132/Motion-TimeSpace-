# Preserve the failed replay; derive its background/metric defect ports

The frozen fine2/fine4/coarse4 comparisons are all retained. Their failed
slow-field comparisons must not be changed into passes by a new norm or by
adding artificial physical forces. The heavy field and cold-fluid controls
pass, while the heavy-case slow background has a large relative equation
defect. The original `solve_slow` used a common absolute tolerance 1e-13
on its dimensionless field and velocity, and max_step=.04 in ln(a), even
when the slow velocity was very small in an oscillatory heavy background.
This is a plausible numerical cause, not by itself proof of attribution.

## 1. Off-shell defects predicted without a fit

Use the original tabulated b and v. Define

    Eb = v' + 2H v + mu^2 b,       Ef = b'-v,
    Ea = alpha'-Psi+H alpha,
    Eg = Phi-eta+H alpha,
    Ez = k*z-k^2*alpha+3eta'.

In the native synchronous-CDM output, delta_c'=-k*z. Since
dstar_c=delta_c-3eta, Ez=-dstar_c'-k^2*alpha can be evaluated without
claiming that the saved output is a complete Einstein hierarchy.

Let u=u_s+v*alpha and p_alg=w_s-mu^2*b*alpha-3eta*v be the earlier
algebraic coordinates. Differentiate them using the native synchronous
scalar equation w_s'=-2H*w_s-(k^2+mu^2)u_s-k*z*v. Then, exactly,

    u' = p_alg+(Psi+3Phi)v + alpha*Eb+v*Ea-3v*Eg,
    p_alg' = -2H*p_alg-(k^2+mu^2)u+mu^2(3Phi-Psi)b
             -mu^2*alpha*Ef-3eta*Eb-mu^2*b*Ea-v*Ez-3mu^2*b*Eg.

These identities identify diagnostic forcing for the difference between
an on-shell parent replay and the retained off-shell numerical history.
They are not corrections to the physical field action. In particular,
p_alg is the true canonical p=u'-(Psi+3Phi)v only when the first defect
combination vanishes. The previous reconstruction is an algebraically
faithful coordinate/source recovery conditional on an on-shell background;
this dynamical test checks that previously untested numerical condition.

Propagate the predicted background and metric defect contributions separately
through the same linear canonical operator, starting with zero difference.
Compare their sum to the observed mismatch; never tune their coefficients.
Finite-differencing quantized metric outputs can be noisy, so repeat the
diagnostic with additional substeps if it is needed for a quantitative claim.
Any unexplained native integration error remains visible.

## 2. Derived stable repair, not an extra coupling

For the slow background define J=a^2*v. The original scalar equation gives

    J'=-a^4*m_s^2*b,     b'=J/a^2.

Store the tiny field change as b=b_start+delta_b, and scale J and delta_b
separately. This avoids a field-scale absolute tolerance governing the tiny
velocity and avoids subtracting nearly equal order-one fields to recover
their derivative. No mass, amplitude or coupling is fitted.

A local on-shell continuation from the saved start can test this repair
without editing the old bank. It does not validate the accuracy of that
saved starting velocity or replace a future regular-primordial replay.
For a fully consistent metric gauge control, obtain alpha from the same
cold-fluid velocity equation, set eta=Phi+H*alpha and derive z from its
definition. Do not quietly label these reconstructed metric coordinates
as the original quantized native columns.

The physical repair must remove the background defect by solving its
equation, not promote the diagnostic defect ports into the MTS action.
