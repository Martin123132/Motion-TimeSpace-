# Eliminate the unresolved angular tail, not the physics

## Mechanism identified by the longer run

At the original16-multipole cutoff, the longer controlled disturbance has appreciable weight near the last retained multipoles. The standard asymptotic last-row formula uses absolute conformal time and need not absorb a newly prepared late-time streaming front correctly. An independent characteristic solution on the same saved metric finds errors in density, current and anisotropic stress in both cold and MTS. Time refinement alone does not repair an incorrect angular boundary.

## Exact boundary inherited from the hierarchy

The untruncated equation at l=16 is

    F16' = k v (16 F15 - 17 F17)/33,

not the retained closure F16'=k v F15-17F16/tau. The characteristic solution in CHARACTERISTIC-CONTRACT.md supplies F17 from its known initial distribution and the metric's complete past. For general l, multiplying P_l by P2 gives

    P_l P2 = a_l P_(l+2) + b_l P_l + c_l P_(l-2),

with coefficients in ANGULAR-REPAIR-CONTRACT.md. Projection of exp(-i mu Delta s) then supplies K_l=b_l j_l-a_l j_(l+2)-c_l j_(l-2). The minus signs follow from i^l(-i)^(l+-2)=-1. No coefficient is obtained from a measured discrepancy or adjusted to reduce it.

F17 is therefore a known free-streaming term plus a causal integral of z and sigma. At each time, both z and sigma are linear readouts of the same coupled state through the retained metric constraints and source-complete radiation response. The new boundary is not independently selected data and must be iterated with those sources. It is an exact elimination of unresolved collisionless angular variables, conditional on the retained perturbation equations. It is not a newly postulated MTS memory law.

## Coupled finite-interval formulation

Let Y contain the retained rest species, F0..F16 for every fixed momentum, and all four heavy canonical coordinates where present. Let Abar(t) be the coupled matrix with the l16 row replaced by its explicit F15 term, and B(t) insert the missing F17 term. With M(u)Y(u)=(z(u),sigma(u)), the same system can be written

    Y'(t)=Abar(t)Y(t)+b_free(t)+B(t) integral[t0,t] K(t,u) M(u)Y(u)du.

This follows from substitution of the characteristic solution; it is not an extra closure assumption. The full heavy state and gravitational response remain coupled. The affine fixed-source evolution used in one numerical iterate is represented by appending a constant coordinate1. That representation does not introduce a physical degree of freedom or a coupling parameter.

For the finite interval, suppose the verified background remains regular, the metric elimination denominator is nonzero, and the retained coefficients are continuous. The finite-dimensional propagator U(t,s) exists. Variation of constants and interchange of the bounded triangular integrals yield

    Y(t)=Y_free(t)+integral[t0,t] L(t,u)Y(u)du,
    L(t,u)=integral[u,t] U(t,s)B(s)K(s,u)M(u)ds.

On a compact interval these continuous kernels are bounded. If sup||L||<=C and the interval length isT, the n-fold Volterra operator is bounded by(C T)^n/n!, by integration over the ordered n-simplex. Its Neumann series therefore converges and gives the unique continuous solution. This is a conditional finite-interval result for the retained LINEAR perturbation system, not nonlinear global stability, a rigorous numerical error certificate, a QFT existence proof or a mass-gap result. No practical bound C has been computed here; two numerical iterations do not follow automatically from this theorem.

## What verifies the numerical repair

The initial iterate uses the already saved fine l16 metric. Generate the first characteristic boundary, evolve the WHOLE coupled state, regenerate the boundary from that actual new metric, and evolve again. Reconstruct the final low neutrino moments and F17 independently from the final metric, and compare with the evolved state/supplied boundary. Also compare128/256time steps with the same bank and check the independent metric and scalar source equations.

The time-nonlocal boundary is banked at the actual requested Gauss times and readout probes; no interpolation of F17 is used in evolution. Source-history interpolation and time quadrature are separately checked. Every failed l16 result remains preserved, the original production angular settings stay unchanged, and cold/MTS receive identical treatment. A numerical failure means the iteration or approximation needs further work, not that a closure may be declared true.
