# Why the local predictor can fail while the full field evolution remains valid

This supplements the retained exact subsystem derivation; it changes no evolution,
forecast coefficient, normalization, or acceptance threshold.

Let x be the own-field/metric variables, u=(D_other,Q_other), and b the evolving
background. The exact subsystem is x'=A(b)x+B(b)u. For the heavy branch,

B = [[0,0],[-V/(2H),0],[0,1/2]].

The cold branch has B=[[-1/(2H),0],[0,1/2]]. A is the matrix already derived
in the preceding stage. These source terms are fixed by the common-metric
constraint and retained field equation, not adjustable force couplings.

For the frozen linear forecast u_L=u_0+(tau-tau_0)u'_0 and the same exact
background, define e=x_L-x and delta_u=u_L-u. Then

e'=A e+B delta_u, e(tau_0)=0,
e(tau)=integral[tau_0,tau] U(tau,s) B(s) delta_u(s) ds,

where dU(tau,s)/dtau=A(tau)U(tau,s), U(s,s)=I. This is exact conditional error
transport, not a claim that delta_u is small or known in advance.

Use the already-frozen state-unit diagonal R when taking norms:

||R^-1 e(tau)|| <= integral ||R^-1 U(tau,s) B(s) delta_u(s)|| ds.

One cannot infer a uniform error bound just from a small endpoint error:
oscillatory contributions can cancel, and the propagator need not be contractive.
An endpoint-only comparison is especially weak over several field periods.

If u is twice differentiable with a known second-derivative bound,

delta_u(tau) = -integral[tau_0,tau] (tau-s) u''(s) ds.

Across piecewise-smooth representation changes the exact remainder also includes
-sum_j [u]_j and -sum_j (tau-s_j)[u']_j for crossed boundaries s_j.
The value-jump term vanishes only after continuity has been established.
Do not silently omit contact terms from the retained interpolation/thermo
representation or call an empirical endpoint slope a global closure.

Numerically the predicted and full backgrounds can differ by integration error.
With A_L and B_L from the predicted background, the exact difference becomes

e'=A_L e+(A_L-A)x+(B_L-B)u+B_L delta_u.

The separate32/64 checks assess this numerical contribution; they do not
prove a rigorous bound on every source remainder. Observed local forecast
failures remain failures of the frozen approximation, not reasons to alter
the full retained hierarchy or its tolerance.

The long-gap test therefore checks every saved original table boundary and
reports sampled interior extrema separately from the two native report times.
No exact continuous maximum or observational likelihood is asserted.
