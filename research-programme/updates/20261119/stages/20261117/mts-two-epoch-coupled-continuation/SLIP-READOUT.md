# Stable relative-velocity response from saved fields

This complementary diagnostic is specified after the frozen midpoint packet
projection exposed cancellation. It does not replace that failed diagnostic,
change any propagation, or establish new observational evidence.

The retained `mts_metric_hook.inc` defines B_b times vector(4) as Q_b,
and B_gamma times vector(g_ix+1) as Q_gamma. Its signature routine stores
g_ix in signature(4). Consequently, at each positive-density background,

    slip = Q_b/B_b - (3/4) Q_gamma/B_gamma
         = v_b - (3/4) q_gamma.

For the same saved old/change variables used by the coupled evolution,

    delta_slip = delta_v_b - (3/4) delta_q_gamma.

This identity holds even when B_b and B_gamma change: their factors cancel
within each branch before taking the difference. It requires the retained
momentum definitions and active hierarchy; it is not a general rule for a
different stress convention. Native g_ix is read from saved signatures,
not assumed. Baryon velocity is Fortran component4, Python component3.

Extract changes directly from COMPLETE normalized states and their original
delta_units. The independent parent is taken from its stored parent_indices
block, not reconstructed by subtracting the transported error. The baseline
uses the same representation and arithmetic. All original files stay fixed.

Checks: single-branch identities against existing packets, stable differences
against packet subtraction within its original primitive-rounding allowance,
and 80-digit Decimal recomputation from exact stored binary inputs, including
normalization products. The latter checks arithmetic only, not lost accuracy
in the ODE solution. Compare saved32/64 refinements; for approximation versus
parent add BOTH refinements and64eps times the change-variable primitive sum.
Keep the original2e-5 numerical and1e-10 algebraic gates. Report unresolved
baseline signals explicitly. Do not call a zero-over-zero ratio a detection.

Use the full joined3041..3044 history, without new propagation or interpolation.
Save source/history hashes and separate old packet and stable-field results.
No new fit, native rebuild, model parameter, boundary, bank or grid change.
