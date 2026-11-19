# Diagnostic repair: reconstruct physical background, subtract exact reference

The initial frozen experiment remains unchanged: full-work comparisons pass,
but branch-change interpolation does not converge, and a tiny integrated split
residual exceeds the raw algebraic gate. This is a separately frozen follow-up.
No native trajectory is rerun or altered; original science-score.json stays.

The stored background uses CubicSpline field tables and a piecewise cubic
thermodynamic clock. The coherent-minus-reference correction cancels their
representation defects. Interpolating that correction alone across neighboring
table knots need not inherit the smoothness of the physical KG solution.
This is a diagnosis to TEST, not an assumption that the failed score is false.

Let X_1=X_0+deltaX, with X_0(t) known from retained tables. Reconstruct

    deltaX_H(t)=H[X_0+deltaX](t)-X_0(t),

not merely H[deltaX](t). Here H is a fixed Hermite interpolation operator.
In stable centered form, with Hermite value/derivative weights a_i,b_i,

    deltaX_H=sum a_i*(X_0(t_i)-X_0(t)+deltaX_i)
             +sum b_i*(X_0'(t_i)+deltaX_i').

Use compensated sums. For alpha=deltaa/a0, reconstruct deltaa first:
deltaa_i=a0_i alpha_i, deltaa_i'=a0_i(alpha_i'+rate0_i alpha_i),
then divide reconstructed deltaa by the exact local a0(t). These are algebraic
identities in the reference, not a new fitted temperature/background curve.
Keep the error-field components h,f,e in their saved old/change coordinates.

Test BOTH three-node degree5 and four-node degree7 physical-background Hermite,
with the already specified strides1/2/4 and Gaussian orders3/5/7. Four-node is
the prospectively selected refined representation; report three-versus-four
differences as an additional diagnostic. Keep original full-work, tiny-error
and2e-5 gates. A failure remains a failure; no physical continuation in this
stage. Check manufactured polynomial full backgrounds with nonpolynomial
references, exact endpoint recovery and input hashes before reporting scores.

## Account for the actual saved split residual

Saved numerical solutions have s=e-h-f, not mathematical zero bit-for-bit.
Linearity gives an independently computable expected integral discrepancy:

    J_e-J_h-J_f=integral -3 H B_P s dt.

Evaluate s from the saved/interpolated physical error fields with compensated
sums and apply the SAME derived pressure operator. Do not define this integral
by subtracting the three integrated answers. Report raw failed zero test and
the new defect-accounted test separately. This accounts for known numerical
state residuals; it cannot repair a genuine pressure-law mismatch or justify
relaxing precision. Add the defect contribution to the displayed work budget.
