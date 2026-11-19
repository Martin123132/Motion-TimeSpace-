# Retaining the endpoint without fitting a pressure closure

This is a consequence of the checked scalar equations, not a new scalar potential,
force coupling, gauge transformation, or replacement physical stress tensor.
It identifies the next evolution variable to test; no new live evolution is
claimed in this stage.

Use the preceding notation and define d=beta D, p=beta P, q=beta k V f,
beta=a/rho0, r=a'/a. Direct differentiation of the retained field products gives

    d' = 2(r-H)d -(2H+r)p -k q -k beta V^2 z
         +beta(G g+mu2 F f).

In the coherent branch r=H and F=G=0. Its density exchange is therefore

    d' = -3H p -k q -k beta V^2 z.

The exact weighted pressure identity derived and numerically checked here is

    H p = H c_v d + B' + E + M + T,
    B = H beta s J/2,
    E = beta [s(2H^2-H'-Hr)-H s'] J/2,
    M = beta H s k Phi V z/2,
    T = -beta H s (G f+F g)/2.

Define the reversible auxiliary variable d_star=d+3B. Its equation is

    d_star' = -3H c_v (d_star-3B) -k q -k beta V^2 z
              -3(E+M+T) +(r-H)(2d-p)
              +beta(G g+mu2 F f).

For the coherent branch both contact expressions vanish. Thus the fast total
derivative of the endpoint need not be discarded or approximated: it is carried
in the auxiliary density itself and restored when reconstructing physical d.
At the initial epoch one MUST match d_star(initial)=d(initial)+3B(initial),
and at the final epoch recover d=d_star-3B. Resetting B to zero loses the very
boundary contribution this stage measured.

This is NOT yet a one-variable fluid closure. B still depends on the relative
background/perturbation phase through J=Vf+Phi g; q and the surrounding metric
remain coupled. Replacing J by an averaged constant would reintroduce the
uncontrolled step. The natural next test is to derive/evolve the phase-aware
auxiliary system and compare its reconstructed physical stress/exchange with
the SAME saved history and initial state, before extending it to new epochs.

These variables describe the retained perturbation convention. Neither d_star
nor the finite-window P/D ratio is silently promoted to an observable density,
background equation of state, or gauge-independent rest-frame sound speed.
