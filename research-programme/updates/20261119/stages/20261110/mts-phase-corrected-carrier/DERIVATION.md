# Phase-dependent carrier correction from the retained equations

Private continuation of the retained heavy-field normal form. No new action, coupling, occupation, fit or cutoff. The previous stage supplies the exact normal pair X=(d,q), its physical source rows, the current rest-source metric zeta=z_rest and the self-gravitating operator. All numerical comparisons retain k=1/Mpc; formulas below use that convention unless k is shown explicitly. Time and mass/frequency units are those in the preceding DERIVATION.md.

## 1. Actual phase and amplitude flow

Let b=R*cos(theta), v=-mu*R*sin(theta), R^2=b^2+v^2/mu^2>0, with theta=atan2(-v/mu,b). From

    b'=v+Ef, v'=-2H*v-mu^2*b+Eb, mu'=r*mu,

one obtains exactly

    theta'=mu+(2H+r)*b*v/(mu*R^2)+(v*Ef-b*Eb)/(mu*R^2),
    (R^2)'=-(4H+2r)*v^2/mu^2+2b*Ef+2v*Eb/mu^2.

Define E=beta*(v^2+mu^2*b^2)/2, beta'=r*beta. Then

    E'=E*[2(r-H)+(2H+r)*cos(2theta)]
       +beta*(v*Eb+mu^2*b*Ef).

The background does not advance at theta'=mu exactly. The formulas use the actual stored background derivatives and retain Ef,Eb as representation defects, not extra forces. R never divides through a field or velocity zero.

For the physical expansion part r=H, Ef=Eb=0,

    theta'-mu=-3H*sin(2theta)/2, E'=3H*E*cos(2theta).

Under the retained flat Friedmann/background conservation equations, the oscillatory part of H' is E*cos(2theta)/(2beta): heavy native pressure is -(E/beta)*cos(2theta). The remaining background pressure contributes a phase-independent part. This conditional relation is used in the analytic first drift correction; the saved-history verification uses the actual independently checked H', not an assertion that numerical representation defects vanish.

## 2. Explicit harmonic operator, including self-gravity

Augment the source pair by its rest metric: x=(d,q,zeta). This third entry is a readout of the retained rest species, not a new degree of freedom. Write

    x'=B_actual(t)*x+e3*zeta',

where B_actual has the exact self-gravitating normal operator in its upper-left block, the retained metric force in its last column and a zero last row. For a frozen physical phase control with r=H, Ef=Eb=0, that operator has only harmonics 2 and 4:

    B(theta)=B0+C2*cos(2theta)+S2*sin(2theta)
                 +C4*cos(4theta)+S4*sin(4theta).

For a compact coefficient specification set

    omega=sqrt(mu^2+1), Sigma=omega+mu, delta=1/Sigma,
    c2s=1/Sigma^2, t=mu/omega, Gamma=H*(5+t^2),
    g0=-E*Sigma/(2omega), gs=-E/(2omega), D=1/(2H*beta).

All unlisted entries, including every last-row entry, are zero:

    B0_11=-H*(1-t)^2/2+D*g0*(1+c2s/2), B0_12=-1, B0_13=g0,
    B0_21=c2s, B0_22=-H*(1+t^2)/2+D*gs*delta/2;
    C2_11=Gamma/2-D*g0*(1+c2s), C2_22=H*(1-t^2)/2, C2_13=-g0;
    S2_12=-Gamma*Sigma/2+D*g0*delta,
    S2_21=H*(1-t^2)/(2Sigma)+D*gs, S2_23=gs;
    C4_11=D*g0*c2s/2, C4_22=-D*gs*delta/2;
    S4_12=-D*g0*delta/2, S4_21=-D*gs*c2s/2.

These coefficients follow by multiplying the metric-force column and physical density row BEFORE averaging. In particular B0 retains the preceding stage's self-gravity correlation, not the product of separately averaged factors. Independent evaluation through the primitive-field coordinate matrix verifies this harmonic expansion.

## 3. Near-identity transformation and exact remainder

Choose the zero-mean phase primitive

    K=sum(n=2,4) [C_n*sin(n*theta)-S_n*cos(n*theta)]/(n*mu),
    P=I+K, x=P*y.

It satisfies mu*partial_theta K=B-B0. No coefficient is selected using a measured discrepancy. The sufficient frozen-parameter inverse bound is

    ||K|| <= sum (||C_n||+||S_n||)/(n*mu) < 1.

Using the actual theta', mu', H', E' and beta', the full K' includes both the phase term and every parameter derivative. The exact transformed equation is

    y'=P^-1*(B_actual*P-P')*y+P^-1*e3*zeta'.

The rest response MUST transform too. Since P has an upper-right column, replacing P^-1*e3*zeta' by e3*zeta' loses a compensating contribution to the first two equations. The rest metric is not silently frozen in the saved-history test.

For any proposed effective B_eff the exact remainder is

    R_exact=P^-1*(B_actual*P-P')-B_eff,
    y'=B_eff*y+P^-1*e3*zeta'+R_exact*y.

This identity is evaluated from the retained native source histories. It separates checking the coordinate representation from accepting an approximation that drops R_exact.

## 4. First generator correction, with background drift

Write K'=B_osc+D_s K, where D_s contains the departure theta'-mu and parameter evolution. To first near-identity order, the averaged generator is

    B_eff=B0+<B_osc*K>-<D_s K>.

The zero-mean terms involving B0*K-K*B0 disappear in this explicitly uniform frozen-phase algebraic control. Matrix multiplication order matters:

    <B_osc*K>=sum(n=2,4) [S_n,C_n]/(2*n*mu),
    [S,C]=S*C-C*S.

For physical expansion r=H, Ef=Eb=0, the phase-dependent theta', E' and H' above give

    -<D_s K>=3H*(S2+E*partial_E S2)/(4mu)
                +E*partial_H S2/(8beta*mu).

Phase-independent parameter rates have zero contribution to this first average because K has zero phase mean. The harmonic-4 drift terms and cross harmonics integrate to zero at this order. The commutator-only formula is appropriate for a constant-parameter periodic control, not automatically for the changing physical background.

Thus the tested first correction is

    B_eff=B0+[S2,C2]/(4mu)+[S4,C4]/(8mu)
             +3H*(S2+E*partial_E S2)/(4mu)
             +E*partial_H S2/(8beta*mu).

This is a derived first-order generator, not a theorem that its omitted remainder is uniformly negligible. Representation defects, higher orders, operator-state correlations during evolution and full rest-species feedback must still be controlled. The actual remainder is retained and measured; the expansion approximation is not used to redefine a passing tolerance.

## 5. Tests and source-response accounting

The original 902-node extraction and the 65-node live history retain their fields, masses, bank, grids, source normalization and gates. The actual phase and energy equations are checked against direct differentiation of their definitions. Complex-step parameter derivatives of K use two frozen precisions; saved degree5/degree7 metric-derivative histories and the live current-native derivative provide independent numerical variants.

For each actual saved state, form y=P^-1*x and its exact derivative, then predict the first two ORIGINAL normal-source rates through

    x'_pred=P*(B_eff*y+P^-1*e3*zeta')+P'*y.

This avoids comparing errors in different coordinate systems. Both instantaneous and original signed-weight projections are reported. It is a rate-level consistency test using saved states, not an independently propagated cosmological solution. The actual CDM baseline uses the identity transform and its unchanged source equation.

A separate propagation control freezes parameters and the rest-source component at first/middle/last locations from each saved window. It integrates one full operator period pi/mu at two numerical step sizes. Compare the fundamental matrix with

    P0*exp[(B0+commutator_correction)*period]*P0^-1.

The drift correction is deliberately absent in that constant-parameter control; its analytic angular average is tested separately. The shared boundary of the two windows is the same physical location, not another independent observation. No new actual-universe state or initial population is inferred from these controls.

## 6. What must be tested next

For a prescribed rest history with matched initial data, the omitted-remainder error obeys

    e'=B_eff*e+R_exact*y_exact,
    e(t)=integral U_eff(t,s)*R_exact(s)*y_exact(s) ds.

This gives a concrete finite-window propagation/error test, rather than treating a projected rate pass as enough. In a fully coupled calculation the rest variables and their error response must be included in the enlarged operator; the conditional formula does not authorize holding future rest histories fixed and calling the result a live prediction. The old late selector/background and its source normalization are not yet replaced by this first-order generator.
