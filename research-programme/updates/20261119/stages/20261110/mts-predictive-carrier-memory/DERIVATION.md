# Predictive memory from the retained carrier equations

This continues the preceding derived normal-form and phase-drift work. It does not postulate a new pressure, force, particle population or coupling. All formulae use the retained numerical conformal-time convention at k=1; no new physical scale is introduced. The saved background and rest-species history remain prescribed for this controlled test.

## Exact conditional operator

The retained primitive heavy pair p=(u,w) obeys p'=A_p p+f_p. Its coefficients include the metric response of the heavy density and the prescribed rest-source zeta. The already derived normal and phase-coordinate maps give X=M p=T y+h zeta. T is the upper 2x2 block of the augmented P, whose last row is (0,0,1). M and T are invertible on the tested positive-energy expanding branch; their zeros/limits are not replaced by divisions by the background field itself.

Differentiating the map and substituting the primitive equation gives

    A_X = (M'+M A_p) M^-1,
    T y' = (A_X T-T')y + (A_X h-h')zeta + M f_p-h zeta'.

Consequently

    A_exact = T^-1(A_X T-T'),
    f_exact = T^-1[(A_X h-h')zeta+M f_p-h zeta'].

The implementation uses matrix solves. The previous effective generator B and forcing f are retained without retuning. Define R=A_exact-B and g=f_exact-f. These are current-coefficient differences: neither requires the exact heavy solution, measured final residual, or observed galaxy/CMB data. Omitting g would discard a real source-column remainder. The corrected equation is y'=(B+R)y+f+g.

## First predictive memory

Let y0'=B y0+f, with the original frozen initial value. Define a new auxiliary response with no free initial amplitude:

    delta1'=B delta1+R y0+g, delta1(t0)=0,
    y1=y0+delta1.

If U_B is the fundamental propagator of B, then delta1(t)=integral from t0 to t of U_B(t,s)[R(s)y0(s)+g(s)] ds. This is the first variation-of-constants/Picard response to the explicit operator and forcing remainder. B and R may be time dependent and noncommuting. No replacement by an ordinary exponential of an averaged matrix is assumed.

Direct addition and subtraction yield

    y1'=(B+R)y1+f+g-R delta1,
    e1'=(B+R)e1+R delta1, e1(t0)=0,

where e1=y_exact-y1. Thus the residual source R delta1 is independently computable from the candidate. For example, any valid induced-norm propagator estimate gives

    ||e1(t)|| <= integral from t0 to t of
      exp(integral from s to t of ||A_exact(r)|| dr) ||R(s)delta1(s)|| ds.

This is an analytical conditional inequality, not a claim that its numerical value is sharp. A componentwise alternative replaces the off-diagonal entries of A_exact with their absolute values, keeps its diagonal, and is driven by |R delta1|. Continuity/piecewise integrability of the retained coefficients gives the usual comparison inequality for |e1|. A numerically integrated envelope still needs convergence and rounding control before a certified numerical bound could be asserted. No such certification is claimed here.

## What is and is not being predicted

The first four heavy integration channels are y0 and delta1. The last four carry the independently sourced e1 transport and componentwise diagnostic envelope. The candidate readout is ONLY y1, mapped back through T, h and M to the original density/current/pressure stresses. Neither diagnostic channel feeds the first four; the error-transport channel is never added to the advertised prediction. The previously saved exact primitive trajectory is loaded for comparison only, after propagation.

Reconstructing y1+e1 would recover the exact conditional equation and is useful for checking the error transport, but would not demonstrate a cheaper reduced description. This stage claims no runtime speedup. It tests whether a derived finite memory response repairs the specific signed-pressure prediction without fitting it.

The genuine cold baseline retains its exact dust equation. There is no oscillator carrier to approximate on that branch, so no analogous invented correction is introduced. The same source histories, frozen output grids, numerical accuracy settings and saved reference controls apply.

## Route to live feedback

The current test isolates conditional reduction error. It does not make the externally prescribed future rest history a new physical axiom. The prior LIVE-FEEDBACK-LIFT.md gives a block-operator construction in which zeta and zeta' are evaluated from CURRENT rest-species state and native equations. If this conditional memory test succeeds, that is the next implementation target. Keep a distinction between importing the original source equations, deriving the memory response here, and demonstrating it on the retained numerical branch.
