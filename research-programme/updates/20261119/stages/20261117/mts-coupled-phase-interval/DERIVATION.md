# Retained local field equation and live-environment test

Use the same common-metric constraints H z=D/(2k)+eta_k, eta_k'=Q/2.
For the quadratic heavy scalar, write its background Phi,V=Phi',
mu2=a^2 m_h^2, and perturbation f,g=f'. Its bare sources are
D_h=V g+mu2 Phi f and Q_h=k V f. The field equation is
g'=-2H g-(k^2+mu2)f-k V z. Eliminating z gives the exact instantaneous
linear subsystem x=(f,g,eta_k):

    x'=A x + b,
    A=[[0,1,0],[-(k^2+mu2+V mu2 Phi/(2H)),-(2H+V^2/(2H)),-k V/H],
       [k V/2,0,0]],
    b=[0,-V D_other/(2H),Q_other/2].

For the cold control, x=(delta_c,eta_k), B_c=kappa a^2 rho_c:

    A=[[-B_c/(2H),-k/H],[0,0]], b=[-D_other/(2H),Q_other/2].

Neither equation introduces a new force coefficient. In the full evolution
D_other,Q_other include every retained surrounding species and remain live.
The instantaneous subsystem matches the native equation when those sources
are supplied. It is NOT closed by physics merely by writing a matrix.

Two deliberately approximate forecasts are frozen at2932: hold those other
sources constant, or use their derived endpoint slope. The slopes are the
sum of the saved native species D',Q' minus the owned species, not a fitted
future curve. The background is independently evolved with the same retained
autonomous background equations; it is not held constant or fitted to future
field outputs. All forecast inputs come from the completed checkpoint.

For the MTS source readout, beta=a/density0 multiplies
[V g+mu2 Phi f, k V f, V g-mu2 Phi f]. Cold readout is the retained
normalization times delta_c, with zero own pressure/current. Compare forecast
errors to the same old reference amplitudes and2e-5 threshold. Failure here
rejects a local environment approximation, not the full live MTS equations.

Native pressure/work/metric and32/64 gates are evaluated independently on
the live continuation. Tiny response-relative precision is separate from
accuracy of each full solution. No numerical gate or prior bank is changed.
Conformal time in Mpc; k,H,V have their retained rescaled-field conventions;
mu2 has units Mpc^-2 and eta_k has units Mpc^-1.
