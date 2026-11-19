# Propagation of the tested corner-safe external source

## Same equations, a resolved source history

The retained own-field/metric equation is linear in its perturbation state:

    X_i'(s) = A(t_i+s) X_i(s) + B(t_i+s) F_i(s),
    F=(D_o,Q_o).

Baseline X=(delta_c,eta_k); MTS X=(u,w,eta_k). The same background, geometry matrices, metric constraint, physical normalization and signed preparation weights are imported from `mts-live-metric-state-20261112/metric_math.py`. No coupling or mass is changed.

The prior control uses F_quad=F_i+s F'_i+s^2 K_i/2, with K_i=(D_o'',Q_o'')_i. This stage uses

    F_history(s) = F_quad(s) + R_i(s),
    R_i(s) = integral_0^s (s-v)[Khat(t_i+v)-K_i] dv,

where Khat is the already tested, frozen, one-sided cell polynomial. Its coefficients are not fitted again. Background values and the metric state remain live during evolution; no frozen-metric shortcut is introduced.

## Stable local integration

For each preparation time, clip the saved cells to its short future interval. In one segment of width h write Khat-K_i=sum_p a_p x^p, x in[0,1]. Store local prefix integrals

    I(s)=integral_0^s (Khat-K_i) dv,
    J(s)=integral_0^s (s-v)(Khat-K_i) dv.

At the segment end:

    I_new=I_old+h sum_p a_p/(p+1),
    J_new=J_old+h I_old+h^2 sum_p a_p/[(p+1)(p+2)].

Within the segment, replace the last sums by x^(p+1) and x^(p+2), and h I_old by h x I_old. Thus R_i(s)=J(s), with no subtraction of large global antiderivatives. Corners stay separate. This vectorized implementation is tested against the preceding independent cell-integral implementation and exact affine/constant-curvature examples.

The host NumPy longdouble is eight bytes, not extended precision. This stage relies on the stable representation and separate error equation, not a false claim of extra precision from a dtype name.

## Independent difference equation

Let DeltaX=X_history-X_quad. Since the same A,B and initial state are used,

    DeltaX'=A DeltaX+B R_i(s),  DeltaX(0)=0.

This equation resolves a tiny response without subtracting two large full states. It is evolved independently, not inferred from the final residual. The own-field D/Q/P readout is linear in the state, so its corresponding change is evaluated directly from DeltaX and then summed with the original signed weights.

For numerical conditioning only, the difference state uses amplitude

    a_i=0.5 T^3 max_component(sum_channel |B_normalized(0)| V_i),

where V_i is the preceding saved curvature-variation envelope. This scale is fixed before comparison, and neither the physical initial-state normalization nor its occupation weights change. All scales are positive for these retained cases. Both full and difference solves use DOP853 rtol1e-10, normalized atol1e-12 and the unchanged duration/32 and duration/64 maximum steps.

## Checks and allowances

The full evolution is checked against the saved native boundary state and metric constraint and against the saved weighted source reference at all nine reports. The initial report and all eight later reports are retained; no output is dropped. The weighted numerical allowance keeps these terms separate: saved target uncertainty, original-state recapture discrepancy, absolute-weighted32/64 evolution differences, and the retained weighted-arithmetic discrepancy.

Superposition is checked in every node's normalized state and in weighted D/Q/P. Its working allowance includes full/control/difference refinement and arithmetic. A64-epsilon readout allowance uses absolute kinetic/potential contributions and absolute signed weights, not merely the small cancelling final result.

At the final epoch, the resolved response is compared against the preceding Bernstein/adjoint envelope. The additional observed source-reconstruction allowance is included separately. Those gains are final-epoch-only: passing eight reported epochs is not advertised as an all-times envelope.

Baseline density's tiny change cannot be sign-resolved by conservative full-state subtraction; the independently evolved difference equation supplies its resolved value. The MTS changes are resolved by both routes and agree within their allowances. This distinction is recorded rather than treating roundoff agreement as a new physical measurement.

## Scope

These are numerical propagation/consistency tests conditional on the external source history extracted from the retained native solution. They are not a new independent cosmological fit, a new occupation prescription, or simultaneous evolution of all surrounding species after arbitrary changed initial data. The true-minus-polynomial continuous bound remains distinct from the tested numerical source, as in the preceding stage. No older physical checkpoint is replaced.
