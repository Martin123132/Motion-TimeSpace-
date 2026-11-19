# Expansion derivatives from stress, not a frozen H

Conformal time, H=a'/a, mu=a m, flat retained FLRW. Define scaled stress
R=a^2 rho/M_Pl^2 and P=a^2 p/M_Pl^2, so R=3H^2. These use the retained
Einstein normalization, not a new value of G. Conservation and the spatial
Einstein equation give

    R'=-H(R+3P),          H'=-(R+3P)/6,
    H''=-(R'+3P')/6,
    R''=-H'(R+3P)-H(R'+3P'),
    H'''=-(R''+3P'')/6.

For a canonical real mode (phi,v=phi') with v'=-2Hv-mu^2 phi,

    R_phi=(v^2+mu^2 phi^2)/2,
    P_phi=(v^2-mu^2 phi^2)/2,
    P_phi'=-2Hv^2-Hmu^2 phi^2-2mu^2 phi v,
    P_phi''=(-2H'+8H^2-2mu^2)v^2
          +(-H'mu^2-2H^2mu^2+2mu^4)phi^2+2Hmu^2 phi v.

Dust contributes P=P'=P''=0 and R'=-HR. Radiation contributes P=R/3,
P'=-2HR/3, P''=(-2H'+4H^2)R/3. Sum all retained species; do not discard
radiation, neutrinos or the rolling slow mode.

The existing StandardSpecies owner tabulates g(N)=ln[a^4 rho_nu/rho_unit],
N=ln a. It defines w_nu=(1-g_N)/3. With L=g_N-2,

    R_nu=3(H0/c)^2 exp(g-2N),
    P_nu=R_nu w_nu,
    P_nu,N=R_nu[L w_nu-g_NN/3],
    P_nu,NN=R_nu[(L^2+g_NN)w_nu-2L g_NN/3-g_NNN/3],
    P_nu'=H P_nu,N,  P_nu''=H^2 P_nu,NN+H' P_nu,N.

This is an exact derivative of the retained background interpolation, whose
kinetic/tabulation accuracy remains inherited. At cubic-spline knots g'''
can jump; piecewise derivatives and knot boundaries cannot be ignored in a
future rigorous enclosure. It is not a derivative of float32 transfer output.

## The missing term in the constant-H special case

For q=a phi and omega=sqrt(k^2+mu^2), the real equation is
q''+[omega^2-H'-H^2]q=0. The second-adiabatic frequency is

    W2=omega-H'(2k^2+3mu^2)/(4omega^3)
             -H^2(4k^4+12k^2mu^2+3mu^4)/(8omega^5).

For the homogeneous carrier,

    W20=mu-3(2H'+H^2)/(8mu).

Thus the constant-H correction cannot just be carried into a matter-dominated
universe: for exact dust H'=-H^2/2, W20=mu. In fact the W=mu template is then
an exact homogeneous solution. That is a nontrivial pressure/background
control, not a fitted cancellation. A radiation-only background has
H'=-H^2 and the sign of the homogeneous correction is reversed.

## Stable residual and derivative representation

Set r=omega/mu, h=H/mu, p=H'/mu^2, u=H''/mu^3, v=H'''/mu^4.

    f=W2/mu=r-p(2r^2+1)/(4r^3)-h^2(4r^4+4r^2-5)/(8r^5),
    D= -h(r^2-1)/r d/dr +(p-h^2)d/dh
       +(u-2hp)d/dp +(v-3hu)d/du,
    g=h f+D f,       j=2h g+D g,
    W2'=mu^2 g,      W2''=mu^3 j,
    R_W/mu^2=r^2-p-h^2-f^2-j/(2f)+3g^2/(4f^2).

Cancel this expression symbolically before evaluating it. Subtraction of
the large individual frequency squares would erase the small residual in
ordinary arithmetic. The stored rational numerator keeps H',H'',H'''
explicit and gives the correct constant-H and dust controls.

The forced canonical action from the previous stage is unchanged:
f1=(Psi+3Phi)(p0-Hq0), f2=Hf1+mu^2(3Phi-Psi)q0. Its derivative-free form
allows changing potentials without differentiating their quantized exports.
Variable-H residuals require a new enclosure; the constant-H error bound
does not apply merely because H/mu is small.

## Retained ownership and scope

The matched heavy homogeneous density is the existing matching_density/a
in scaled units. It is not being derived afresh as a coherent carrier's
exact phase-resolved stress. The saved late perturbation chart is averaged;
the original fast phase and full late hierarchy are not inferred here.
The new forced microscopic interface remains an explicitly prepared test
until compared with that retained chart and its precision budget.

Source owners: ../MTS-HEAVY-BATH-COUNTERFLOW-AND-GALACTIC-STRESS.md;
../mts-metric-forcing-calibration-20261110/DERIVATION.md;
../condensate-origin-20261003/native-heavy-matching-20261007/native/fortran/MTSTwoField.f90;
../condensate-origin-20261003/native-heavy-matching-20261007/prepare_matching.py;
../condensate-origin-20261003/radiation-and-slow-field-transfer-20261007/radiation_common.py;
../condensate-origin-20261003/resolved-matter-spectrum-20261007/spectrum_common.py.
These are applications of existing Einstein/scalar conservation and WKB,
not a new general gravitational principle or an imported QFT existence claim.
