# 4991 - Massless hh-channel amplitude seed and completeness test

Checked: `2026-07-14`.

Marker: `MTS_4991_MASSLESS_HH_CHANNEL_AMPLITUDE_SEED`.

## 1. Result

The first non-scalar contribution required by checkpoint 4990 has now been
recovered from a primary one-loop amplitude source rather than represented by
an unknown cut coefficient. H.-H. Chi's exact `D`-dimensional ancillary
coefficients determine the opposite-helicity two-graviton intermediate state
in the `s`-channel of the scalar-graviton amplitude. Taking the massless
scalar limit and reducing in the Dunbar-Norridge integral convention gives a
source-complete component

```text
M1_hh,s=kappa^4 F_hh,s/<1|3|2]^4.
```

This is a genuine one-loop hard kernel for the outer two-loop `hh` cut. It is
not the full one-loop `phi phi h h` amplitude: the scalar-intermediate and
mixed `h phi` crossed discontinuities remain to be derived.

## 2. Source scope

The source explicitly restricts the retained terms to an `s`-channel cut and
gives the basis

```text
b1 I4(s,t)+b2 I4(s,u)+t1 I3(s)+t2 I3(s,M)+b I2(s).
```

The five coefficients are supplied in `Coeff-of-Integrals.txt` with the
overall factor

```text
kappa^4/<1|3|2]^4.
```

The statement that `I3(s,M)` degenerates to `I3(s)` at `M=0` is our
mathematical limit, not a quotation or unsupported attribution to the paper.

## 3. Exact massless reduction

With `s+t+u=0` and `D=4-2 epsilon`, the bubble coefficient is

```text
b_I2(D=4)
 =tu[2(t^4+u^4)-3tu(t^2+u^2)]/32.
```

The term multiplying the bubble pole must be retained one order higher in
`epsilon`:

```text
b_I2^(epsilon)
 =-tu[180(t^4+u^4)-333tu(t^2+u^2)+605t^2u^2]/2880.
```

At zero scalar mass, the two source triangles share the same integral and
their coefficients collapse exactly to

```text
t1+t2=-(t^7+u^7)/16.
```

The two box coefficients are

```text
b_st=t^4(t^4+u^4)/32,
b_su=u^4(t^4+u^4)/32.
```

Therefore

```text
F_hh,s=
 b_I2(D) I2(s)
 -(t^7+u^7)I3(s)/16
 +(t^4+u^4)[t^4 I4(s,t)+u^4 I4(s,u)]/32.
```

Every coefficient is invariant under the required simultaneous
`t<->u`, `I4(s,t)<->I4(s,u)` exchange.

## 4. Physical tree interference

For the opposite-helicity tree,

```text
M0=kappa^2 <2|3|1]^4/(4stu),
<1|3|2]<2|3|1]=tu.
```

The helicity phase cancels in the physical interference:

```text
M1_hh,s M0*=kappa^6 F_hh,s/(4stu).
```

The outer-cut integration may consequently be formulated with the scalar
kernel `F_hh,s` once the missing channels and common infrared subtraction are
supplied.

## 5. Partial infrared checksum

Using

```text
I4(s,t)=N_epsilon/(st)[4/epsilon^2+...],
I3(s)=-N_epsilon/s[1/epsilon^2+...],
```

the retained component has double-pole coefficient

```text
-(3t^6-3t^5u+3t^4u^2-t^3u^3
  +3t^2u^4-3tu^5+3u^6)/16.
```

This is a checksum for the crossed completion. It is not the universal soft
factor of the full amplitude because the source intentionally omits the
other channel discontinuities.

## 6. What remains mathematically missing

The complete massless one-loop basis can also contain

```text
I4(t,u), I3(t), I3(u), I2(t), I2(u), rational terms.
```

At `M>0`, Chi's selected `s`-channel cut isolates the two-graviton threshold.
At `M=0`, scalar and mixed `h phi` thresholds are also massless. Merely
setting `M=0` in the selected component cannot create their discontinuities.
The next derivation must construct the two crossed `h phi` cuts from products
of scalar-graviton Compton trees and then impose full soft-factor consistency.

## 7. Validation and claim boundary

The generator closes `9/16` gates. The seven open gates are the complete
one-loop amplitude, the mixed `h phi` channel, full infrared subtraction,
the crossing-complete outer `hh` cut, numeric full `K_mu/K_ang`, exact
all-operator local GR, and full MTS. The independent validator reparses the
primary ancillary file and passes `301/301` checks, including 24 exact
rational kinematic events.

Authoritative outputs:

- `source-intake/functional_rg/4991/massless_hh_channel_integral_coefficients.csv`
- `source-intake/functional_rg/4991/massless_hh_channel_identity_checks.csv`
- `source-intake/functional_rg/4991/one_loop_amplitude_scope_and_IR_test.csv`
- `source-intake/functional_rg/4991/massless_hh_channel_amplitude_gate.csv`
- `source-intake/functional_rg/4991/massless_hh_channel_amplitude_seed_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_4991_VALIDATION.csv`

This checkpoint advances the full crossed `hh` calculation from an unknown
amplitude to a sourced exact channel component. It does not claim the full
one-loop amplitude, a numeric two-loop invariant, exact local GR, or full
MTS.
