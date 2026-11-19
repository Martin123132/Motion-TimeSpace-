# Do not feed an archived velocity back as a driving force

The scalar slip test takes the supplied baryon velocity in its expansion term. For an independent test, evolve both species velocities on each fixed cell; only their density and photon quadrupole driving terms remain supplied. Let p=3q_gamma/4, s=v-p, P=k c_b² delta_b and J=k(delta_gamma/4-Pi_gamma/2). The retained Euler equations are v'=-Hv+P-w chi s, p'=J+chi s. Multiplying the photon row by w and adding eliminates all collision terms. For M=v+w p the extra derivative is w' p. At fixed w the separate collision step gives s'=-(1+w)chi s and M'=0: fast slip damping is not erasure of total photon-baryon momentum.

For the finite background difference use g=1/(1+alpha), w1=w0 g, chi1=chi0 g². With Dv=v1-v0, Dp=p1-p0, Ds=Dv-Dp:

    Dv'=-H1 Dv-DH v0+DP-w0 chi0 [g³ Ds+(g³-1)s0],
    Dp'=DJ+chi0 [g² Ds+(g²-1)s0].

Use factored g^n-1, and do not subtract the two bright Euler rates. The finite collision columns obey D[C_b+w C_p]=DC_b+w1 DC_p+(w1-w0)C_p0=0. Rest-energy gain is the previously derived elastic rate; it is not the total momentum or an independent new energy coupling.

Use the four existing 257-point cell fixtures, without new fits, changing a left state, or solving the external photon density and quadrupole. Recover J0 from the saved exact F0 and the *reference* H0,v0,P0 only as an input density/quadrupole combination. Cross-check by reconstructing both original scalar driving rows on the saved velocities. Evolve all four old/changed velocities and the energy together on the matched clock, and retain both 32/64 histories' own initial states. Compare a second representation using v and s (not v and p); disagreement between them is a numerical conditioning test. Split the 32/64 left state into an equal-velocity shift and a relative velocity shift at fixed total weighted momentum. These are counterfactual controls at fixed density/metric histories, not physical perturbation IC changes. Look at the right-end budget on each velocity's own amplitude and the accumulated radiation. Do not move a failing cell to an easier test.
