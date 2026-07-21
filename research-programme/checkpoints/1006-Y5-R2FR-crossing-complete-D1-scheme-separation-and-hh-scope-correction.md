# 4990 - Crossing-complete D1 cancellation, flow-scheme separation, and hh scope correction

Checked: `2026-07-14`.

Marker: `MTS_4990_CROSSED_CUT_D1_SCHEME_BRIDGE_CORRECTION`.

## 1. Result

Checkpoint 4989 combined a direct physical `s`-channel cut with a
crossing-summed amplitude, inserted a Type-I/Litim FRG coefficient into an
on-shell dilatation equation without a finite scheme bridge, and promoted a
direct-channel helicity-support theorem to a crossing-summed zero. Those
premises are corrected here.

In the reduced rational-free on-shell convention, the complete crossed
scalar cut fixes

```text
beta_C^(S-matrix)=203/10,
D C^(S-matrix)=-203/10,
D1 ReF1=-(203/10)F1.
```

The nested logarithm then cancels exactly:

```text
2 D_phi,crossed,log-D1 ReF1=0.
```

Consequently, tree-by-tree three-particle cuts are not assigned artificial
`mu`-log slopes. Their finite contributions remain to be calculated. The
scalar `Delta K` values from 4988 are restored as additive cut subtotals,
while full `K_mu` and `K_ang` remain open.

## 2. Crossing-complete scalar identity

For cyclic channels

```text
(q,p,r)=(s,t,u),(t,u,s),(u,s,t),
s+t+u=0,
z_q=(p-r)/q,
```

the exact identities are

```text
q^3 P2(z_q)=q^3-6stu,
sum_cyclic q^3=3stu,
sum_cyclic q^3 P2(z_q)=-15stu.
```

Writing

```text
L_A=sum_cyclic q^3 ln(-q/mu^2),
L_B=stu sum_cyclic ln(-q/mu^2),
```

gives

```text
sum_cyclic q^3 P2(z_q)ln(-q/mu^2)=L_A-6L_B.
```

The 4988 direct-channel scalar slopes are

```text
d0_L=-2233/(72pi),
d2_L=-203/(1800pi),
```

and factor exactly as

```text
d0_L+d2_L P2=(203/(10pi))[-55/36-P2/180].
```

The 4985 mixed kernel obeys

```text
sum_cyclic q^3[-55/36-P2(z_q)/180]=-(9/2)stu.
```

Using the 4986 one-loop logarithm

```text
F1_log=(2/pi)[(23/15)L_A-(1/30)L_B],
```

the crossed scalar discontinuity is therefore

```text
D_phi,crossed,log
  =(d0_L+d2_L)L_A-6d2_L L_B
  =-(203/20)F1_log.
```

## 3. Exact on-shell D1 cancellation

Bern's convention gives

```text
2 Im F=U,
D_cut=Disc/(-2pi i)=-U/(2pi),
R_master=2 sum_cuts D_cut-D1 ReF1.
```

The factor two is real, but it must be applied after constructing the same
crossing object on both sides. Hence

```text
2D_phi,crossed,log=-(203/10)F1_log.
```

With `D=-mu partial_mu=-d/dlnmu`, the on-shell coefficient and its
dilatation sign are

```text
dC_Smatrix/dlnmu=203/10,
D C_Smatrix=-203/10.
```

Thus

```text
D1 ReF1=-(203/10)F1,
2D_phi,crossed,log-D1 ReF1=0.
```

The former 4989 targets

```text
3097/(72pi),
-21397/(1800pi)
```

for three-particle `mu` slopes are rejected. A tree-times-tree
three-particle cut has no renormalization-scale logarithm to supply them.

## 4. Corrected double logarithm

Define

```text
Q_A=sum_cyclic q^3 ln^2(-q/mu^2),
Q_B=stu sum_cyclic ln^2(-q/mu^2).
```

Since

```text
dQ_A/dlnmu=-4L_A,
dQ_B/dlnmu=-4L_B,
```

the exact double-log term is

```text
F2_double=(203/(20pi))[(23/15)Q_A-(1/30)Q_B],
dF2_double/dlnmu=-(203/10)F1_log.
```

Its direct `s`-channel discontinuity has scale slope

```text
-(203/(10pi))[23/15-x(1-x)/30]
=-2233/(72pi)-[203/(1800pi)]P2(1-2x),
```

which independently reproduces both 4988 slopes.

## 5. FRG and amplitude coordinates are distinct

Checkpoint 4982's coefficient

```text
beta_C^(FRG)=16
```

comes from an effective-average-action calculation using a Type-I regulator
and Litim profile. It remains valid in that declared Wilsonian truncation.
It is not, without further work, the perturbative on-shell coefficient.

The required relation

```text
C_Smatrix=f(C_FRG,g,regulator,frame,...)
```

has not been derived. No claim is made that either coefficient is wrong;
the corrected statement is that `16` and `203/10` cannot be identified
without a finite regulator/coordinate bridge.

## 6. Propagation through the 4985-4987 scheme orbit

The same correction propagates through every amplitude-scheme descendant.
With

```text
dC/dlnmu=203/10,
dW/dlnmu=B_gc C+S,
B_gc=-6/pi,
```

the exact trajectory is

```text
C(t)=C_c+(203/10)t,
W(t)=C_w+(S+B_gc C_c)t-[609/(10pi)]t^2.
```

For finite changes `C'=C+beta`, `W'=W+alpha C+delta`, amplitude invariance
requires

```text
r4'=r4-beta,
rho'=rho+3alpha,
S'=S+(203/10)alpha-B_gc beta,
A'=A-beta f_A,
B'=B-beta f_B.
```

The fixed-p4 combination and full finite-orbit invariants are therefore

```text
I=3S-(203/10)rho,
I'=I-3B_gc beta,

K_mu=3S-(203/10)rho+(18/pi)r4,
K_ang=A-B-[47/(15pi)]r4.
```

Both full combinations are exactly invariant. In the double-rational-free
scheme `r4_rf=rho_rf=0`, they still reduce to

```text
K_mu=3S_rf,
K_ang=A_rf-B_rf.
```

Thus the correction changes the inherited coefficient but does not disturb
the 4988 rational-free scalar subtotals.

## 7. Scalar invariant subtotals

The exact 4988 constants reconstruct

```text
Delta A_phi=d0+d2,
Delta B_phi=-6d2,
Delta K_mu_phi=-6(d0-5d2)
 =(-135061+1500pi^2)/(450pi)
 =-85.0641390166317,
Delta K_ang_phi=d0+7d2
 =(13357+24075pi^2)/(3375pi)
 =23.6697802325722.
```

The `-6` inverse map already implements the crossed local-amplitude map in
the declared normalization. These values must not be multiplied by two a
second time. They are additive scalar-cut subtotals, not complete physical
invariants.

## 8. Correct scope of the hh support theorem

For the direct opposite-helicity `hh` state,

```text
abs(lambda_hh)=4,
d^J_04=0 for J<4.
```

Therefore its direct `s`-channel `J=0,2` projections vanish. Legendre spin
in one channel is not crossing invariant, however. A direct counterexample
is obtained by crossing a `P4` toy into the physical `s` channel:

```text
T(x)=t^4P4((u-s)/t)+u^4P4((s-t)/u)
    =2x^4-4x^3+126x^2-124x+71,
s=1, t=-x, u=x-1.
```

It has nonzero low-spin projections

```text
T_0=252/5,
T_2=144/7.
```

The allowed conclusion is therefore only

```text
direct-channel D_hh,J=0 for J=0,2;
crossing-summed Delta K_hh remains unknown.
```

The full crossed `hh` cut remains on the critical path together with the
mixed `hhh` and `phiphih` three-particle cuts.

## 9. Validation and claim boundary

The generator closes `12/20` gates. The eight open gates are deliberate:
the finite FRG/on-shell bridge, the full crossed `hh` cut, both
three-particle cuts, numeric full `K_mu`, numeric full `K_ang`, exact
all-operator local GR, and full MTS. The independent validator passes
`263/263` checks.

Authoritative outputs:

- `source-intake/functional_rg/4990/crossed_scalar_cut_identity.csv`
- `source-intake/functional_rg/4990/flow_scheme_separation.csv`
- `source-intake/functional_rg/4990/scheme_orbit_propagation_correction.csv`
- `source-intake/functional_rg/4990/corrected_D1_cancellation.csv`
- `source-intake/functional_rg/4990/hh_crossing_support_scope.csv`
- `source-intake/functional_rg/4990/4989_supersession_matrix.csv`
- `source-intake/functional_rg/4990/corrected_master_gate.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_4990_VALIDATION.csv`

Numeric full `K_mu/K_ang`, finite `C_w`, exact all-operator local GR, and
full MTS are not claimed. The next calculation is a crossing-complete
evaluation of the `hh` finite cut or one genuine three-particle finite cut,
not another scale-slope closure.
