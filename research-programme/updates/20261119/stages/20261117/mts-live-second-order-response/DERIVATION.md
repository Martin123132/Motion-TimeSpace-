# Second-order response with live gravitational feedback

Use the accepted rotating equation u'=(A_s+C)u+j and recurrence
K1'=[A_s,K1]+C, K2'=[A_s,K2]+C K1. With S=I+K1+K2,
the derived approximation is v'=A_s v+S^-1 j, u=S v. Its exact field defect is

    u'=(A_s+C)u+j-C K2 v.

For the first live test, retain ORIGINAL physical field coordinates x=(f,g).
If u=E x, then this approximation is equivalently

    x'=L x+b-R, R=E^-1 C K2 S^-1 E x.

This residual-form implementation lets the existing native common metric and
all species respond to the actual reconstructed physical stress at every RHS.
It avoids attributing a coordinate roundoff change to the physics truncation.
It is not yet a slow-step solver or a claimed speed-up. The unmodified full
parent equations remain the control. The extra matrices are derived coefficient
memory, with no fitted parameters or additional freely selected physical state.

## Stable old/change arithmetic

All coefficients, E, A_s, C and K matrices are pairs(base,change). Products use
Delta(AB)=A1 DeltaB+DeltaA B0, and a solve y=A^-1 b uses

    y0=A0^-1 b0, Delta y=A1^-1(Delta b-Delta A y0).

For positive scalar a, Delta sqrt(a)=Delta a/[sqrt(a+Delta a)+sqrt(a)].
The same pair arithmetic computes the phase direction from
(sqrt(mu)Phi,-V/sqrt(mu)), without subtracting nearly equal angles.
Coherent background contacts are zero; original contacts and rate r-H are kept.
Original physical field and old/change normalization are unchanged. K1/K2 use
fixed numerical units1e-3/1e-5, with change units another factor1e-5; these do
not change the physical source error norms or the approximation order.

K1=K2=0 matches the complete3040 physical state once. No rematching or resetting
occurs inside the test window. Future source/metric histories are not inputs.
Background/thermodynamic tables remain the retained model's original inputs.

## Exchange and actual metric derivatives

Since f'=g-R_f and g'=g'_KG-R_g, the extra unweighted source derivatives are

    delta D'=-mu^2 Phi R_f-V R_g,
    delta Q'=-k V R_f,
    delta P'=+mu^2 Phi R_f-V R_g.

Multiply the first two by beta=a/rho0 for their additional integrated work.
Keep the original pressure/exchange accumulators unchanged and save these extra
terms separately. A successful accounted identity cannot replace the RAW
exchange test: both must be reported with the original tolerances.

The native metric diagnostic assumes the unmodified KG RHS. It therefore needs
an explicit derivative correction for the actual approximate trajectory:

    delta z'=delta D'/(2kH),
    delta sigma'=delta z'+3 delta Q'/(2k^2),
    delta R_trace=delta z', delta R_shear=delta sigma'.

Update the heavy species D'/Q', total density/current defects and the derived
contact predictions by these independently computed terms. Algebraic metric
values, eta_k' and background equations are unchanged at a given state. Keep
the original native-equation diagnostic as a separate array; never present it
as the actual derivative after changing f'/g'. Independently recompute the
constraint derivatives from the modified species RHS and verify these formulas.
Conventions remain z,sigma dimensionless and eta_k Mpc^-1; the older metric
document's units typo was corrected in the retained phase-stage clarification.

## Frozen test

Original3040..3041 clocks and existing background boundaries; full cold and
heavy direct32/64, heavy second-order32/64. Original934 seed/norms, known1050
owner prefix inside1051 capture, same bank, binary, parameters, grids and
1e-10 algebra/2e-5 numerical gates. Preflight stable pairs against80-digit
controls, exact initial native/source/RHS parity and nonzero-residual controls
before new evolution. Freeze code/window/scorer before comparison.

Test raw ACTUAL pressure/exchange/trace/shear/constraints, complete physical
outputs versus direct parent, independent native endpoints and separate small
response precision. Record the derived defect account additionally. The prior
fixed-forcing remainder bound is not a coupled metric error bound; agreement
with full live controls is the evidence here. Do not promote a closure or
change tolerances if the raw coupled tests fail.
