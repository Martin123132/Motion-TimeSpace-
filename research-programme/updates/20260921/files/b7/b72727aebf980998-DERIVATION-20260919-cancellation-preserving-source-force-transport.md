# Cancellation-preserving full-force transport

Private numerical/derivation checkpoint, September 19, 2026. No public claim, new live evolution, altered physical action, or change to the force-comparison acceptance threshold.

## Question and scope

The previous full-force endpoint telescope passed, but all four spatial forward/backward homogeneous transport tests failed their original roughly 3e-16 absolute gate. The reference also failed. The backward calculations subtract quantities whose absolute dot-product sums are about 0.21 (reference) and 12 (MTS), leaving a result of about 6e-10 and -3e-8 respectively. This is a numerical qualification problem, not a new observation against either model.

The present calculation treats the saved binary64 data as its exact input coefficients, uses genuinely higher-precision Decimal arithmetic, and retains the saved full source-force secant covector. It qualifies transport of that discrete covector; it does not prove its continuum accuracy or add precision to the underlying saved physical trajectories.

Prior report: `DERIVATION-20260919-full-source-force-spatial-budget-v2.md`.
Prior immutable seal: `source-intake/navier-stokes/20260914/annular-full-force-final-integrity-v3.json`.

## Cancellation-preserving derivation

For each fixed saved level, let A=M^-1 K and L=[[0,1],[-A,0]], E(t)=exp(tL), with phase Y=(u,v). Let I embed the coarse scalar/velocity into the fine grid using the original nonnested interpolation. The exact homogeneous cross-level difference is

    E_f Y_f0 - I E_c Y_c0
      = E_f (Y_f0 - I Y_c0) + (E_f I - I E_c) Y_c0.

Compute the first term by propagating the SMALL initial difference. For the second term, propagate the increment W=Y(t)-Y0 directly:

    W' = L W + L Y0,   W(0)=0.

Then the commutator is W_f(IY_c0) - I W_c(Y_c0): the two large, identical initial fields cancel algebraically before numerical propagation. Its exact differential form is also

    C' = L_f C + (L_f I - I L_c) E_c Y_c0,   C(0)=0,
    L_f I - I L_c = [[0,0],[I A_c - A_f I,0]].

For the fixed terminal full-force secant c=(c_u,c_v), compare the directly propagated difference with the INDEPENDENT backward action:

    forward  = c . [E_f(Y_f0-IY_c0) + W_f(IY_c0)-I W_c(Y_c0)],
    backward = (E_f^T c).Y_f0 - (E_c^T I^T c).Y_c0.

The original gate is unchanged:

    abs(forward-backward)
      <= 2e-10 * max(abs(forward),abs(backward),1e-9) + 3e-16.

No rescaled tolerance, fitted correction, filtered mode, or replacement small-norm observable is used.

## Arithmetic and independent controls

- Exact conversion of saved float coefficients, phases, transfer coefficients, and covectors into Decimal; 32 decimal digits/48 Taylor terms, then 48 digits/64 terms.
- K assembled at the active higher precision from the original gradient and Gram factors and weights. No change to couplings or retained modes.
- Original mass convention preserved: the old SPD solve explicitly consumes the LOWER triangle. Upper-band storage has tiny independent rounding differences and is not consumed by that solver. Attempt01 incorrectly required exact upper/lower storage equality; it failed before actual propagation and is retained. Attempt02 explicitly reconstructs the symmetric matrix from that original lower triangle; this is not a new mass model.
- Banded positive-pivot LDL solve, with a separate actual-matrix residual test and independent factor-versus-assembled stiffness test.
- A conservative mass-Jacobi/row-sum frequency bound supplies a scaling and substep choice. This is a scaling bound, not an interval arithmetic certificate.
- Primal, affine-increment, and transposed propagators use separate recurrences. An independent dense 80-digit mpmath exponential checks a nontrivial small fixture, including both adjoint directions.
- Actual reference/MTS matrix adjoints and deliberately incorrect transpose negative controls are checked separately. Every test uses both branches.
- Precision/order refinement checks each signed initial/operator contribution as well as both total pairings, not just a small cancellation residual.

These are numerical validation controls, not a proof of a full floating-point error enclosure. Windows longdouble was previously confirmed to have only 53 mantissa bits; it is not used as pretend extra precision.

### Why matching adjoints alone is insufficient

A polynomial in L and its transpose can agree by duality even when the polynomial poorly approximates the exponential. That is why the degree/precision refinement and independent dense exponential are required; the dual test alone would be too weak.

There is also an exact-arithmetic truncation bound for the frozen positive action. Write D=diag(M), rho=||D^-1(M-D)||_infinity<1 and k=max_i sum_j |K_ij|/D_ii. The Neumann bound gives ||M^-1 K||_infinity<=k/(1-rho)=s^2. Positivity of M and K implies real nonnegative modal frequencies omega<=s. In action-energy coordinates the generator is skew, so a degree-N Taylor step has modal error at most

    delta = exp(h*s) * (h*s)^(N+1) / (N+1)!.

For n identical steps, telescoping against the exact energy-isometric flow gives the action-energy operator error at most n*delta*(1+delta)^(n-1). The construction selects h*s<=4; it is not relying on a small total T*s (which is about 281 for the fine MTS scaling bound). The zero-frequency free-motion block is represented exactly for N>=1. If K has a nullspace, the action energy is a seminorm and does not bound a position-sensitive force in that nullspace: that component needs separate treatment.

This bounds polynomial truncation in exact arithmetic, not Decimal rounding or a force functional norm. Converting it into a full force-error certificate still requires the dual energy norm/nullspace treatment and rigorous arithmetic bounds. No such certificate is claimed here.

## Results

**The unchanged frozen homogeneous duality gate passes for all four spatial comparisons at both precisions.** This is a new successful numerical qualification, not a reinterpretation of the old failed run.

| Branch / comparison | Old dual discrepancy | New 48-digit discrepancy | Unchanged gate |
|---|---:|---:|---:|
| Reference, coarse32/fine | 1.604594e-15 | 3.815674e-49 | 3.002e-16 |
| Reference, coarse64/fine | 1.465993e-15 | 9.173407e-49 | 3.002e-16 |
| MTS, coarse32/fine | 2.345578e-12 | 1.021524e-45 | 3.063979e-16 |
| MTS, coarse64/fine | 1.803014e-12 | 1.244064e-46 | 3.063979e-16 |

The maximum change of any tested signed initial/operator term or forward/backward pairing on refinement from 32 digits/48 terms to 48 digits/64 terms is 2.652e-30. These tiny discrepancies describe consistency for the SAME saved floating-point inputs, not 45-digit physical accuracy.

The corrected coarse64/fine homogeneous terms are:

| Contribution | Reference | MTS |
|---|---:|---:|
| Initial representation | -6.4000467763e-10 | -1.9910488060e-9 |
| Frozen operator commutator | +1.2615464595e-9 | -2.9998298189e-8 |
| Total | +6.2154178189e-10 | -3.1989346995e-8 |

The old forward estimate changes by -1.38745e-15 (reference) and -4.78742e-13 (MTS). The old backward estimate changes by +7.85409e-17 and +1.32427e-12 respectively. Thus neither direction was automatically ground truth; the error is not solely a backward-dot-product problem. The corrected MTS forward value differs by roughly 15 parts per million from its old value, far too little to erase the physical mismatch.

The large negative MTS frozen-operator contribution persists under independent backward propagation and precision/order refinement. The much smaller initial representation term also persists. This supports targeting the actual spatial operator defect next rather than treating the entire commutator as numerical noise. It is still only one signed component of the complete force telescope, which includes endpoint operator/transfer cancellation and the remaining moving/path terms.

All four actual mass equations have relative residuals below 8e-48; independent factored/assembled stiffness errors are below 8e-47. Deliberately using the wrong transpose gives relative discrepancies between 0.269 and 0.972, so the adjoint control is nontrivial. The high-precision lower-triangle solves reproduce the original double-precision solves within 3.35e-16 relative error. No physical coefficients were repaired or fitted.

The transport and separate operator controls finish successfully: 30 + 29 scoped implementation/source checks. The transport run takes 1063.65 seconds (about 17.7 minutes) on one active single-core BelowNormal worker. The preliminary exact-storage-symmetry rejection is retained; no failed threshold was relaxed. Software/source checks are not counted as independent confirmations of the theory.

## Physical meaning and next derivation

Even a successful strict duality test repairs only the frozen discrete transport calculation. The original impulse mismatch (12.5718%), the fine-versus-continuum endpoint mismatch (13.5770%), and the coarse64-versus-fine MTS endpoint mismatch (32.5535%, a different denominator) are not removed by better arithmetic. No full GR limit or uniform continuum bound follows.

Once this calculation is qualified, the spatial operator commutator can be attacked without confusing its force contribution with subtraction noise. With lambda(s)=E_f(T-s)^T c, its exact source-weighted representation is

    c . C(T) = integral_0^T lambda_v(s) . [I A_c - A_f I] u_c(s) ds,
    A_f I - I A_c = M_f^-1 [K_f I - M_f I M_c^-1 K_c].

This retains the original mass projection, nonnested transfer, full force covector, initial representation, and all modes. The next substantive target is to resolve that mass/stiffness/transfer defect spatially and derive an actual force-weighted bound, rather than launching another blind time refinement. The existing measured path/sampling defect is still measured, not a certificate.

## Reproducibility

- Immutable base arithmetic: `scripts/annular_decimal_transport_20260919.py`.
- Original lower-triangle wrapper: `scripts/annular_decimal_transport_v2_20260919.py`.
- Retained rejected storage test: `scripts/derive_annular_decimal_duality_20260919.py`.
- Actual transport: `scripts/derive_annular_decimal_duality_v2_20260919.py`.
- Independent actual-operator controls: `scripts/validate_annular_decimal_operators_20260919.py`.
- Failed status: `source-intake/navier-stokes/20260914/annular-decimal-duality-attempt01/status.json`.
- Transport status: `source-intake/navier-stokes/20260914/annular-decimal-duality-attempt02/status.json`.
- Operator-control status: `source-intake/navier-stokes/20260914/annular-decimal-operators-attempt01/status.json`.

Execution uses one single-core BelowNormal worker, writes progress after blocks, has a two-hour computation guard, and does not edit prior executed evidence, the protected workbench, or galaxy work. No GitHub action or subagent.
