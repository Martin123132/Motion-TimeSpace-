# 5150 - Minimal occupied `P(X)` zero-mode TT polarization and critical-sign gate

Marker: `MTS_5150_MINIMAL_OCCUPIED_PX_ZERO_MODE_TT_CRITICAL_SIGN_GATE`.

Date: `2026-07-20`.

## Decision

The actual smallest occupied-state calculation has now been performed. The
route is granted its most favorable gapless limit; the current positive
`m_gap^2` would only strengthen the analytic/gapped obstruction. A regular
reflection-even `P(X)` action on an occupied background has a stable gapless
scalar mode when

```text
Z_t=P_X+2 Xbar P_XX>0,
Z_s=P_X>0,
c_s^2=Z_s/Z_t>0.
```

Its tree static Hessian is local and rational in `k^2`; on a homogeneous
timelike state the scalar has no linear transverse-traceless metric mixing.
The first universal nonanalytic TT term therefore comes from the occupied
zero-mode stress loop.

## Exact zero-mode loop

Take external momentum along `z`. After static canonical normalization,
`T_xy=partial_x phi partial_y phi`, so the connected correlator is

```text
<T_xy(k)T_xy(-k)>_c
 =2 W_state integral d^3p/(2pi)^3
   p_x^2 p_y^2/[p^2(p+k)^2].
```

Dimensional regularization isolates the scheme-independent nonanalytic term.
Feynman parametrization, the `d=3` tensor average
`<l_x^2 l_y^2>=l^4/[d(d+2)]`, and
`integral_0^1 [x(1-x)]^(3/2) dx=B(5/2,5/2)` give

```text
integral p_x^2 p_y^2/[p^2(p+k)^2] = |k|^3/1024,
<T_xy T_xy>_c = W_state |k|^3/512.
```

The executed coefficient is `0.0019531250000000004`.
For a thermal state `W_state=T_chi`; for a general passive Gaussian
occupation it is the positive zero-mode weight.

## Effective-action sign

The universal metric vertex is `S_int=(1/2) integral h_xy T_xy`. Expanding
`-ln Z[h]` gives the connected term

```text
Delta Gamma2 = -(1/8) h_xy h_xy <T_xy T_xy>_c,
Delta K_TT   = -W_state |k|^3/2048.
```

The calculated coefficient is
`-0.0004882812500000001`. Analytic seagulls and
counterterms can renormalize constant and `k^2` terms but cannot change this
nonanalytic coefficient.

Checkpoint 5149 proved that the desired stable critical kernel requires

```text
K_TT,desired = +M_R^2 |k|^3/(A mu)+... .
```

If an analytic medium susceptibility first enforces the required unit-mixing
`k^2` cancellation, the minimal passive scalar leaves a **negative** `|k|^3`
coefficient. It crosses into a gradient/Jeans instability instead of the
positive checkpoint-5148 response. The homogeneous passive one-scalar
realization is therefore rejected for the common no-slip/TT kernel.

## Scale magnitude

Ignoring the sign only to expose the required state size, coefficient matching
would demand

```text
N_eff W_state = 2048 M_R^2/(A mu).
```

At the median read-only `L_eff=9.29254645998695 kpc`, with
`mu L_eff=2.921396974200681` and
`A=1.0691523388681814`, the required product is
`10^84.75199653414262 eV`. This is not a fitted
parameter or a pass; it confirms that an ordinary small occupation cannot
repair the sign or magnitude.

## What survives

This result rejects only the minimal homogeneous passive `P(X)` realization
of the checkpoint-5148 **common metric response**. It does not reject:

- a non-equilibrium active state, provided full CTP stability and positive
  dissipation are proved rather than assumed;
- additional parent vector/tensor or fermionic collective modes with a
  different TT sign;
- the motion field acting as a genuine conserved gravitating state stress
  rather than as a dressed vacuum/common-projector propagator.

The third route changes the next question in a useful way. Instead of forcing
the scalar to renormalize every metric polarization identically, derive its
occupied stress profile and calculate rotation **and lensing** from the same
Hilbert tensor. The local branch remains exactly `psi=0`; no Mercury coupling
is reopened.

## Next calculation

Derive the most general stationary axisymmetric reflection-even motion-state
stress permitted by the current CTP two-point function, impose conservation
and regularity, and invert the weak Einstein equations for both metric
potentials. Test whether the resulting circular-speed support can match the
5148 `S_q` target while its lensing slip remains acceptable. No occupation or
radial stress may be inserted by hand.

All `12` validation checks pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub or galaxy-repo
write occurred.
