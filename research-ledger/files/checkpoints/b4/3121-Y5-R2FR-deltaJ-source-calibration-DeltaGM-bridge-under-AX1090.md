# 3121 - `delta_J` Source-Calibration `DeltaGM` Bridge under AX1090

Private checkpoint. This is the promised leap from 3120: derive the leading bridge from hidden EM current normalization to source mass / measured `GM`, rather than only saying the bridge is missing.

## Verdict

There is a clean conditional zero route:

```text
same-current owner + public Hodge + fixed EM kinetic owner + variation-before-readout
=> Lie_v J_Q = 0
=> Lie_v F_Q = 0
=> Lie_v T_EM = 0
=> Delta_GM_J = 0.
```

There is also a useful finite residual route. In the weak-field, stationary, public-Maxwell branch, if:

```text
J_Q -> c_J(y) J_Q,
delta_J := Lie_v ln c_J,
```

then the leading source-calibration bridge is:

```text
Delta(GM)_S / (GM)_S
= [C_J,S^ADM - C_J,cal^ADM] delta_J
  + O(delta_J^2, gradients, nonstationary radiation, non-EM relaxation).
```

with:

```text
C_J,S^ADM = 2 tau_EM,S f_EM,S^ADM + C_relax,S.
```

This is the main advance: `delta_J` is no longer just an abstract current leak. Its first local-GR/Newton bridge is a calibrated ADM/source-mass response coefficient.

## Source Register

| source_id | path | role |
|---|---|---|
| 3116 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md` | public Maxwell stress, Poynting, source-coupling lock |
| 3119 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3119-Y5-R2FR-same-current-owner-or-deltaJ-source-test-residual-priority-under-AX1090.md` | same-current owner theorem and `delta_J` definition |
| 3120 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3120-Y5-R2FR-deltaJ-product-bound-runner-or-current-owner-source-intake-under-AX1090.md` | product-bound intake that named the missing `DeltaGM_J` bridge |
| local-bounds | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` | WEP, PPN, `Gdot`, and inverse-square-law anchors |
| 3121-inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3121_DELTAJ_GM_BRIDGE_INPUTS_TEMPLATE.csv` | executable bridge inputs |
| 3121-runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3121_deltaJ_GM_bridge_runner.py` | bridge evaluator and validation |

## Derivation

Start from the public Maxwell sector:

```text
d(Z_EM *_pub F_Q) = J_Q,
T_EM^munu = Z_EM(F^mu_alpha F^nu_alpha - 1/4 g_pub^munu F^2).
```

Hold `Z_EM`, `*_pub`, the public metric/coframe, and boundary/readout convention fixed. A hidden current-normalization branch changes:

```text
J_Q -> c_J(y) J_Q.
```

For a linear Maxwell Green operator in a fixed public background:

```text
F_Q[J_Q] -> F_Q[c_J J_Q].
```

If `c_J` is constant over the compact source support at leading order:

```text
F_Q -> c_J F_Q.
```

Therefore:

```text
T_EM[c_J J_Q] = c_J^2 T_EM[J_Q],
Lie_v T_EM = 2 delta_J T_EM.
```

For a nonuniform hidden profile the same result becomes a weighted projection:

```text
Delta M_EM,S / M_EM,S = 2 tau_EM,S delta_J,
```

where `tau_EM,S` is the source-support EM-energy weighting of the hidden current profile. This is not set to one unless the profile is constant or a parent theorem supplies the weighting.

Now let the far-field source mass be the ADM/Tolman mass after matter-plus-field stress balance:

```text
M_ADM,S = M_rest,S + M_EM,S + M_other,S.
```

Define:

```text
f_EM,S^ADM := M_EM,S / M_ADM,S.
```

Then:

```text
Delta M_ADM,S / M_ADM,S
= 2 tau_EM,S f_EM,S^ADM delta_J + C_relax,S delta_J.
```

`C_relax,S` is retained because a real bound source may shift nuclear/electronic equilibrium, material stress, or binding conventions when the current normalization changes. If the parent action proves same-current descent, this whole branch goes to zero. If not, the finite coefficient is:

```text
C_J,S^ADM := 2 tau_EM,S f_EM,S^ADM + C_relax,S.
```

Measured `GM` is calibrated, not metaphysically raw. A universal constant current rescaling shared by the source and calibration convention is absorbed. The observable residual is:

```text
Delta(GM)_S / (GM)_S | obs
= [C_J,S^ADM - C_J,cal^ADM] delta_J.
```

This calibration subtraction is important: MTS does not have to make every constant normalization independently observable. Only non-universal, hidden-dependent, time-dependent, source-dependent, or composition-dependent pieces survive.

## Observable Projections

### Newton / orbital `GM`

For an orbiting test body around source `S`:

```text
a = GM_S/r^2 + ...
```

so:

```text
Delta a/a |_source = [C_J,S^ADM - C_J,cal^ADM] delta_J.
```

This is the source-mass route into Newtonian mechanics. It is not yet a claim because `f_EM,S^ADM`, `tau_EM,S`, `C_relax,S`, and the calibration reference are not sourced.

### WEP / composition

In a common source field, a pure source `GM_S` rescaling cancels from an Eotvos ratio at leading order. A `delta_J` WEP signal instead needs test-body gravitational/inertial mismatch or an extra source-test current force:

```text
eta_AB^J
~ [(C_J,A^g - C_J,A^i) - (C_J,B^g - C_J,B^i)] delta_J
  + source-test product terms.
```

So 3121 sharpens the WEP route: do not use source `DeltaGM_J` alone as a WEP prediction.

### PPN

PPN does not follow from `DeltaGM_J` alone. It needs a metric response kernel:

```text
Delta gamma_J = K_gamma^J [C_J,S^ADM - C_J,cal^ADM] delta_J,
Delta beta_J  = K_beta^J  [C_J,S^ADM - C_J,cal^ADM] delta_J.
```

If the only effect is a constant calibrated `GM`, PPN shape residuals can be zero even when a raw source mass normalization changes. This prevents a false overclaim.

### `Gdot`

If the hidden current normalization or source coefficient changes with public time:

```text
d ln(GM)_S/dt
= [C_J,S^ADM - C_J,cal^ADM] d(delta_J)/dt
  + d[C_J,S^ADM - C_J,cal^ADM]/dt delta_J.
```

This gives a clock/orbital route but only after the time profile is derived.

## Runner Result

3121 adds:

| artifact | path |
|---|---|
| input template | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3121_DELTAJ_GM_BRIDGE_INPUTS_TEMPLATE.csv` |
| output | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3121_DELTAJ_GM_BRIDGE_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3121_VALIDATION.csv` |
| bridge gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3121_DELTAJ_GM_BRIDGE_GATE.csv` |

The runner computes:

```text
predicted_residual = abs((source_kernel_CJ - calibration_kernel_CJ) * deltaJ_value)
```

and compares it to the selected local bound only if every term is numeric, sourced, direct, and marked claim-valid.

## Claim Status

No local-GR, Newtonian, WEP, PPN, orbital, `Gdot`, EM stress, derived-`G`, or unification claim follows from 3121.

The internal advance is:

```text
delta_J -> Delta_T_EM -> Delta_GM_J/GM is now derived at leading order;
the observable is calibration-subtracted;
universal constant current rescaling is separated from physical residuals;
WEP, PPN, and Gdot routes are no longer blurred together.
```

## Next Target

Write:

```text
3122-Y5-R2FR-current-owner-descent-or-CJ-source-coefficient-fill-under-AX1090.md
```

Direct target:

1. try to sign `C_J,S^ADM=0` from same-current descent and public Maxwell stress;
2. if not, source or estimate `f_EM,S^ADM`, `tau_EM,S`, and `C_relax,S` for at least one conservative local arena;
3. keep WEP separated from source `GM` unless a test-body current mismatch is derived.
