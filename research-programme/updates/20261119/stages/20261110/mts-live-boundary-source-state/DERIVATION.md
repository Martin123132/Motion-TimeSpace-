# Live boundary-adapted sources with no future-history input

This implements the previous stage's exact coordinate map in the retained parent dynamics. It is a coordinate change of the same real-scalar action, not a new fluid law or new population. The old averaged selector remains zero; every derived correction is retained. Numerical evaluation is at the original k=1/Mpc, original background/normalization and65 output times.

## State and regular inverse

For beta=a/R0, mu=a*m and physical heavy perturbation(u,w),

    YD=beta*(v*w+mu²*b*u), YQ=beta*v*u,
    J=beta*b*v, S=beta*(b*w+v*u),
    WD=YD+(3H*S+z*J)/2, WQ=YQ-S/2.

Restoring general k in the mathematical map places k with zJ and S in the respective coordinates, as proved in the previous DERIVATION.md. The two new variables replace only the four constrained heavy moment entries; those four contained two physical degrees of freedom. No physical phase mode is discarded. The slow scalar's constrained phase matrix and all other active native coordinates remain live.

At each RHS evaluation, temporarily set ONLY the heavy perturbation moments to zero while retaining the current rest/slow state and homogeneous heavy background. The existing native constraint then supplies z_rest independently. With t=b*v/(4H), recover(u,w) from

    [WD-J*z_rest/2, WQ]^T
      = beta * [[(1+t)*mu²*b+3H*v/2, (1+t)*v+3H*b/2],
                [v/2, -b/2]] [u,w]^T.

Pack the physical heavy moment matrix B U^T, where B=(b,v/omega), U=(u,w/omega), omega²=1+mu². The existing native phase RHS then computes the fully coupled metric, species derivatives and source readouts. The inverse does not use future source samples, divide by v or fit a coefficient. Its sufficient regularity condition and positive-energy assumptions are checked at every RHS call.

This reduces the numerical heavy block by two redundant entries, not by two physical modes. It is not yet an averaged approximation; the remaining phase information and corrections are explicit.

## Present-state metric derivative

The retained native C API supplies H,z and the phase/rest RHS f(t,m), but not their total time derivatives. Because the perturbation equations and metric constraint are linear in the state m,

    z(t,m)=L(t)m,
    dz/dt = partial_t z(t,m) + z(t,f(t,m)).

H is homogeneous/background-only, so its total derivative is its partial time derivative. The implementation evaluates the partial derivative with a five-point local stencil of the existing native readout, holding the CURRENT m fixed. It subtracts the central value before weighted summation to reduce constant-value cancellation. The state-direction term uses the actual current RHS through the same linear native constraint.

Centered stencils are used inside the owner interval, one-sided stencils near its boundaries. Time shifts change the known background but never substitute saved future perturbations or a predicted future trajectory. The derivative is a numerical approximation to the current local operator, not an imported future history and not an assertion of an exact new native derivative export.

Physical metric steps span/4096 and span/8192 are tested separately from integration steps span/128 and span/256. A saved-history derivative is used ONLY as a preflight comparison. It is absent from SourceState's evolved RHS. The independent coordinate-map finite-difference check needs larger balanced steps because its subtraction is more cancellation-sensitive; STENCIL-DIAGNOSIS.md preserves the failed original check and the separately frozen repair. Neither physical metric step nor either tolerance changes.

## Full derived source RHS

Let b'=r*b_N, v'=r*v_N, beta'=r*beta and(mu²)'=2r*mu² use the actual retained representation. The native physical derivative provides u',w'. Form

    YD'=r*YD+beta*(v'*w+v*w'+2r*mu²*b*u+mu²*b'*u+mu²*b*u'),
    YQ'=r*YQ+beta*(v'*u+v*u'),
    J'=r*J+beta*(b'*v+b*v'),
    S'=r*S+beta*(b'*w+b*w'+v'*u+v*u'),
    WD'=YD'+(3H'*S+3H*S'+z'*J+z*J')/2,
    WQ'=YQ'-S'/2.

All unmodified rest/slow coordinates use their native phase derivatives directly. The independent check assembles the previous BD+HD, BQ+HQ expression from pressure, kinetic, metric and representation terms. Product and tail formulations must agree. Neither sets the tails to zero; BD/BQ are functions of physical Y sources, not blindly relabelled W.

This composition is closed on the CURRENT full retained state and background. Its prescribed homogeneous background is the same retained background as the native comparison; it does not claim to evolve a new homogeneous solution or independently prepare a primordial/galactic population.

## Scientific test scope

Captured and projection-reconstructed starts, both branches, full state/derivative/observable/cache comparisons, zero/sign controls, quantitative rest-to-metric and heavy-to-metric feedback, source reconstruction and physical moment rank are checked. Step and local derivative refinements stay separate. At exact-zero field or velocity, synthetic instantaneous phase controls at retained positive energy test the algebraic inverse; these controls are not new cosmological solutions. Actual evolved background sign changes are reported separately.

The completed calculation supports using these exact source variables with live gravity. Connecting them to the old late averaged selector/background still requires deriving or bounding the operator reduction, rather than equating their names or dropping the retained corrections.
