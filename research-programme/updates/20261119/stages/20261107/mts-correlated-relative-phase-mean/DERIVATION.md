# Correlated phase mean of the retained matter/metric system

Local continuation of `../mts-joint-relative-metric-20261107/DERIVATION.md`.
The action, masses, physical wavenumbers, source bank and acceptance gates
are inherited. This is a coordinate reduction of those equations, not a
new field, an effective sound-speed fit, or an independent dust closure.

## 1. The background and the generator must belong to the same state

Write N=ln(a), H for the CONFORMAL Hubble rate, and use the parent's
normalization 3H^2=R_total. The heavy scalar has
x=am phi, v=phi', rho=(x^2+v^2)/2, theta=atan2(-v,x).
Rho is the conformally rescaled energy density, not physical rho/a^0.
The exact relations are

    theta_N = omega = mu - (3/2) sin(2 theta),   mu=am/H,
    rho_N = [-1 + 3 cos(2 theta)] rho.

The positivity condition for this angular coordinate is mu>3/2. With
sigma=(N,phi_s,v_s,rho,tau), the instantaneous slow-state flow is

    f(sigma,theta) = f0(sigma) + fc(sigma) cos(2 theta),
    f0 = (1, v_s/H, -2v_s-(am_s)^2 phi_s/H, -rho, 1/H),
    fc = (0,0,0,3rho,0).

H is independent of theta at fixed sigma, but H_N/H is not. The native
thermal and other-matter coefficients remain functions of the same
state and clock. A phase fibre holds sigma fixed to inspect coefficients;
it is NOT a physical trajectory or a replacement late-time preparation.

For the parent's relative scalar and other matter, w_N=G w. Its exact
closed metric map is w=S zeta, R=S^-1, and therefore

    zeta_N = B(sigma,theta) zeta,
    B = R G S + R_N S.

Here R_N=D_sigma R f + R_theta omega, and includes the metric-row
derivative. This stage evaluates that derivative along the actual local
flow. It does not silently replace it by a partial phase derivative.
The native baryon pressure, radiation closure, quadrature enthalpy
defect, momentum/shear channels, and G192 tail remain in G.

## 2. A clock-weighted, correlated mean

All transformed coefficients are pi-periodic in theta. Because the
angular speed is not constant, the frozen-fibre period and mean are

    P(sigma) = integral_0^pi dtheta/omega,
    Bbar(sigma) = [integral_0^pi B(sigma,theta)/omega dtheta]/P.

For omega=mu-(3/2)sin(2theta),

    P = pi/sqrt(mu^2-9/4).

Integrating the derivative of log(omega) over a period gives
<cos(2theta)>_clock=0. Hence <f>_clock=f0 at fixed sigma. This identity
does NOT prove that solving sigma_N=f0 reproduces the physical background;
the oscillatory background transformation and its error remain separate.

The mean above is taken AFTER the matrix products and source feedback.
In particular it is not <R><G><S>+<R_N><S>. Separate averaging loses
covariances even though each factor may be accurately integrated.

## 3. Exact periodic primitive and the term that cannot be dropped

Define the zero-angle-mean periodic matrix Q by

    Q_theta = (B-Bbar)/omega,       integral_0^pi Q dtheta=0.

Its periodicity follows exactly from the definition of Bbar. On any
domain where I+Q is invertible, set zeta=(I+Q) chi. Direct substitution
gives the exact transformed equation

    chi_N = (Bbar+E) chi,
    E = (I+Q)^-1 [B Q - Q Bbar - D_sigma Q f].

No matrices have been commuted. In particular the background contribution

    D_sigma Q f = D_sigma Q f0 + cos(2theta) D_sigma Q fc

is part of the remainder. Holding the phase fibre fixed is legitimate for
defining Bbar and Q; it is not legitimate for erasing this derivative
from the physical evolution. `collect_drift.py` differentiates Q along
both anchored directions using independently frozen fourth-order
stencils, with widths 0.002 and 0.001 e-fold-direction units.

For any compatible submultiplicative norm, if q=||Q||<1, then

    ||E|| <= [||B Q-Q Bbar|| + ||D_sigma Q f||]/(1-q).

This is a pointwise analytic inequality. A finite list of phase samples
checks its implementation but does not prove a continuum supremum.
For the computed Fourier polynomial Qp=sum Qhat_j exp(2ij theta),
sum_j ||Qhat_j|| bounds ||Qp|| for EVERY phase. Extending that certificate
to exact Q additionally requires a bound on Q-Qp. Nested quadrature and
held-out angles are numerical evidence, not a directed-rounding proof.

## 4. Why only a small block is needed for the exact remainder

Partition the retained hierarchy into core, l=3 and l>=4 moments. At
fixed sigma the phase dependence lives in the core and its l=3 boundary
couplings. Interior streaming and diagonal tail rates have no phase
dependence. Consequently Q and its slow-state derivatives have support
only in core plus l=3. Products BQ and QBbar extend at most to l=4.
Thus E has support in core plus l=3,4, despite the full G192 generator.

`reduced_operator` is exactly this local submatrix, NOT a new l=4 closure
for evolving perturbations. The full propagation still uses the original
G192 tail. The code checks phase independence and native full-tail rates.
The interior streaming becomes antisymmetric in the inherited energy
weights; its symmetric part is just the phase-independent diagonal.
This also permits a full-hierarchy logarithmic-norm bound from the
core/l=3 symmetric block and the remaining tail diagonal, when this
antisymmetry has been checked.

## 5. The finite-interval error contract and physical endpoints

Let Ubar solve chi_N=Bbar(sigma(N))chi along the specified background,
lambda(N)=lambda_max[(Bbar+Bbar^T)/2], and suppose an ALL-STATE/ALL-PHASE
bound epsilon(N)>=||E|| holds on that background. Then

    ||U_exact_chi-Ubar||
       <= exp(integral lambda) [exp(integral epsilon)-1].

This follows from variation of constants and the logarithmic norm; it
does not require Bbar at different times to commute. A physical readout
O w has the approximation

    O(N) S(N) [I+Q(N)] Ubar(N,N0) [I+Q(N0)]^-1 R(N0) w0.

Both endpoint factors and the original prepared w0 are mandatory.
The readout error inherits their operator norms multiplying the bound.
Replacing sigma by the retained mean cold background introduces an
additional background-replacement term. The previous scalar-only
background certificate is not automatically a full-matter certificate.

This contract identifies the quantities to bound for a controlled
coupled cold transfer without inventing a late initial mode or phase.
The present native qualifications are on the original resolved EARLY
background. They are not a new evolution on the saved LATE cold interval.

## 6. Baseline, parameter ownership and known scalar-field results

The retained baseline has no heavy scalar. Its heavy relative map is
the identity, its coefficients do not depend on the absent heavy phase,
and Q=0, E=0 for THIS phase reduction. Its physical metric/matter
evolution and ordinary numerical errors remain present and are tested.

The scalar pressure term already obtained in the parent,
k^4/(4a^2 m^2 H^2) in N/conformal conventions, is a known oscillating
massive-scalar mechanism, not a unique MTS discovery. Hwang and Noh derive
the linear scalar-fluid relation for a minimally coupled quadratic
field, neglecting higher H_phys/m terms; their gauge and truncation must
be matched before importing its fluid equations. See their 2009 paper:
https://arxiv.org/html/0902.4738 .

Passaglia and Hu distinguish exact effective-variable construction from
approximating its evolution, including separate matching and evolution
errors. That is a useful methodological cross-check, not a substitute
for our retained operator, gauge and error gates. Their 2022 paper is:
https://arxiv.org/html/2201.10238v2 .

The inherited MTS mass and action coefficients are still inherited
inputs here; this calculation derives the coupled reduction from them.

## 7. Implementation and evidence boundaries

`phase_fibre.py` changes only worker-private DLL state during a coefficient
probe and restores the context. No DLL file, parent checkpoint or source
bank is edited. `fibre_operator.py` obtains fresh native matrices rather
than reusing a matrix from the wrong scalar phase. `mean_math.py` builds
the weighted mean, periodic primitive and noncommuting remainder.

All runs freeze their inputs and grids before evaluation. Physical
wavenumbers and history grids are unchanged. The new 64/128/256 phase
quadratures and the two slow-state derivative stencils are diagnostics
for this reduction, not changes to the source bank or model tolerances.
The saved packets allow independent re-analysis without another
microscopic scattering or background run. See RESULTS.md for measured
errors and the scope of the accepted evidence.
