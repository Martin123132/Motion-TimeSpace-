# Derived local repair: stable background momentum and two gauge controls

The original replay failures remain false. The parameter-free background
defect response reduces the heavy-case slow-field discrepancy from 0.1953844
to 2.20836e-6 and its momentum discrepancy from 0.1209590 to 8.62822e-7.
This explains the dominant discrepancy; inserting those defect forces into
the theory would be wrong. The derivative-based metric diagnostic worsens
some tiny-field comparisons and is retained as an unreliable use of the
quantized native output, not accepted as a precision correction.

Now test a separately labelled ON-SHELL local continuation. Original bank,
interval, metric histories, masses, physical starting field/velocity,
starting perturbations, and 2e-5/1e-10 gates remain fixed. This does not
overwrite or repair the old global background table in place.

## Background

Evolve J=a^2*v and the small offset delta_b=b-b_start:

    J'=-a^4*m_s^2*(b_start+delta_b),
    delta_b'=J/a^2.

Normalize J and delta_b independently using their saved starting scales.
Do not derive v by differencing nearly equal order-one field samples.

## Two independent coordinate implementations of the same scalar action

Alongside the Newtonian canonical pair (u,p), evolve a synchronous pair
(u_s,W_s), where W_s=w_s-v*delta_c. Let d_c=delta_c-3eta and U_c=k*alpha.
For the fixed k=1/Mpc mode, the cold component and gauge relation obey

    d_c'=-U_c,       U_c'=-H*U_c+Psi,
    eta=Phi+H*U_c,   delta_c=d_c+3eta.

Then the native synchronous scalar equation is equivalently

    u_s'=W_s+v*delta_c,
    W_s'=-2H*W_s-(1+mu^2)*u_s+mu^2*b*delta_c.

This follows by differentiating W_s and using the on-shell background;
it removes the derivative of a quantized delta_c column from the forcing.
The derivative-free transformation is

    u=u_s+v*U_c,
    p=W_s+v*d_c-mu^2*b*U_c.

The same Psi/Phi history drives both implementations. No derivative of a
metric output is taken. Initial W_s and u_s come from the recovered initial
u,p and the same background and cold state, not a new fitted seed.

Run two and four RK4 substeps per frozen interval in each case. Compare
both implementations and their D/P/Q/Dstar against each other, and check
step refinement with their own signal peaks. Also report their differences
from the old native history without treating that differing background as
the same problem. Bound the local background energy change relative to
3H^2 using difference-of-squares arithmetic, not cancellation of two large
potentials. This permits a fixed-metric bridge test only; the next fully
coupled run must carry the repaired background and actual early hierarchy.

Passing establishes a local on-shell numerical repair with the inherited
initial state. It does not validate that initial velocity's primordial
accuracy, constitute a refit, or retrospectively turn the original failed
native comparison green.
