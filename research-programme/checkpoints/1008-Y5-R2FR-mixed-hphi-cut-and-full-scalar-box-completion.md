# 4992 - Mixed h-phi cut and full scalar-box completion

Checked: `2026-07-14`.

Marker: `MTS_4992_MIXED_HPHI_CUT_AND_FULL_BOX_COMPLETION`.

## 1. Result

The scalar-box sector of the one-loop opposite-helicity
`h+(p1) h-(p2) phi(p3) phi(p4)` amplitude is now complete in four
dimensions. This is an actual crossed-cut calculation, not an inferred
crossing ansatz.

Three independently sewn discontinuities agree:

1. the sourced `hh` intermediate state on the `s` cut from checkpoint 4991;
2. the missing identical-`phi phi` intermediate state on the same `s` cut;
3. the distinguishable mixed `h phi` cuts in the `u` channel and its
   `t<->u` crossing image.

In the convention

```text
M1=kappa^4 F/<1|3|2]^4,
s+t+u=0,
```

the completed box kernel is

```text
F_box =
  B_st I4(s,t)+B_su I4(s,u)+B_tu I4(t,u),

B_st=t^4(s^4+t^4+u^4)/32,
B_su=u^4(s^4+t^4+u^4)/32,
B_tu=t^4 u^4/16.
```

The shared `I4(s,u)` coefficient agrees exactly between the `s` and `u`
cuts. The `I4(s,t)` coefficient agrees with the crossed mixed cut, and the
`I4(t,u)` coefficient is invariant under the same crossing.

## 2. Exact massless spinor chart

All momenta are incoming. A rational chart that solves momentum
conservation and keeps `t,u` symbolic is

```text
lambda1=(1,0),       tilde1=(-1,-1),
lambda2=(0,1),       tilde2=(u,-t),
lambda3=(1,-u),      tilde3=(1,0),
lambda4=(1,t),       tilde4=(0,1).
```

It gives

```text
p_i^2=0,
sum_i p_i=0,
(p1+p2)^2=s=-t-u,
(p2+p3)^2=t,
(p1+p3)^2=u,

Q=<2|3|1]=1,
Qbar=<1|3|2]=tu,
Q Qbar=tu.
```

The last identity restores the invariant external helicity phase after the
chart calculation.

## 3. Mixed h-phi u-channel cut

Set `K=p1+p3` and write the two on-shell cut momenta as

```text
lambda_l=lambda1-w lambda3,
tilde_lambda_l=(tilde1-z tilde3)/(1+zw),

lambda_q=lambda3+z lambda1,
tilde_lambda_q=(tilde3+w tilde1)/(1+zw).
```

Then `l^2=q^2=0` and `l+q=K` identically. Crossing the sourced
opposite-helicity scalar-graviton Compton tree onto both sides of this cut
gives four uncut propagators

```text
A=(l-p1)^2 =-u zw/(1+zw),
B=(l-p3)^2 =-u/(1+zw),
C=(l+p2)^2 =(1-w)(s-tz)/(1+zw),
D=(l+p4)^2 =(t+sw)(1+z)/(1+zw).
```

They obey

```text
A+B=-u,
C+D=-u,
```

and therefore

```text
1/(u^2 A B C D)
 =u^-4(1/A+1/B)(1/C+1/D).
```

The crossed product of the two Compton numerators reduces in this chart to

```text
N/u^4=Q^4 r^4,
r=(1+z)/(1+zw).
```

Thus the cut separates into the four box topologies `AC`, `AD`, `BC`, and
`BD`. Applying the standard half-sum over the two quadruple-cut solutions,
with no identical-state factor because `h` and `phi` are distinguishable,
gives

```text
AC -> I4(s,u):
  r^4={1,u^4/t^4},
  B_AC=u^4(t^4+u^4)/32;

BD -> I4(s,u):
  r^4={s^4/t^4,0},
  B_BD=s^4 u^4/32;

AD -> I4(t,u):
  r^4={1,0},
  B_AD=t^4 u^4/32;

BC -> I4(t,u):
  r^4={1,0},
  B_BC=t^4 u^4/32.
```

The `B`-propagator solutions occur in the reciprocal projective charts
`z->infinity` or `w->infinity`; they are not discarded as nonexistent
finite-chart roots. The mixed cut therefore fixes

```text
B_su^(mixed u)=u^4(s^4+t^4+u^4)/32,
B_tu^(mixed u)=t^4 u^4/16.
```

Its `t<->u` image fixes `B_st` and independently reproduces `B_tu`.

## 4. Identical-scalar s-channel cut

For `K=p1+p2`, use

```text
lambda_l=lambda1-w lambda2,
tilde_lambda_l=(tilde1-z tilde2)/(1+zw).
```

The two Compton propagators and the two channels of the sourced
four-scalar graviton-exchange tree are

```text
L1=(p2-l)^2 =-s/(1+zw),
L2=(l-p1)^2 =-s zw/(1+zw),

R1=(p4+l)^2 =(w+t)(1+zu)/(1+zw),
R2=(p3+l)^2 =(u-w)(1-zt)/(1+zw),

L1+L2=R1+R2=-s.
```

The Compton phase and the four-scalar numerator are

```text
<2|l|1]/Q=s z/(1+zw),
H(R)=(s^2+sR+R^2)^2.
```

On every quadruple residue, the selected right-tree channel has `R=0`, so
`H=s^4`. The four partial-fraction routings occur in equal pairs:

```text
L2R1,L1R2 -> I4(s,t), each s^4 t^4/32 before state counting;
L2R2,L1R1 -> I4(s,u), each s^4 u^4/32 before state counting.
```

The two cut scalars are identical. The explicit `1/2` state factor removes
the routing duplication and leaves

```text
B_st^(phi phi)=s^4 t^4/32,
B_su^(phi phi)=s^4 u^4/32.
```

## 5. Three-channel closure

Checkpoint 4991 supplied

```text
B_st^(hh)=t^4(t^4+u^4)/32,
B_su^(hh)=u^4(t^4+u^4)/32.
```

Adding the scalar intermediate state gives

```text
B_st^(s cut)=t^4(s^4+t^4+u^4)/32,
B_su^(s cut)=u^4(s^4+t^4+u^4)/32.
```

The exact channel residuals are

```text
B_su^(s cut)-B_su^(mixed u)=0,
B_st^(s cut)-cross[B_su^(mixed u)]=0,
B_tu^(mixed u)-cross[B_tu^(mixed u)]=0.
```

This is the nontrivial consistency condition expected because every scalar
box has discontinuities in two channels. No coefficient was fitted to make
the cuts agree.

## 6. What remains

This checkpoint is complete only for the four-dimensional scalar-box
sector. It does not yet determine:

- `I3(s)`, `I3(t)`, and `I3(u)` coefficients after all state sums;
- `I2(s)`, `I2(t)`, and `I2(u)` coefficients;
- `mu^2`, evanescent, or rational information requiring a
  `D`-dimensional cut;
- the common gravitational infrared subtraction;
- the complete one-loop `phi phi h h` hard kernel;
- the outer two-loop crossed `hh` cut or numeric `K_mu/K_ang`.

The next derivation is to use the universal one-loop gravitational soft
operator in exactly the same integral normalization to constrain the
triangle sector, then perform a `D`-dimensional cut reduction for the
bubbles and rational remainder.

## 7. Reproducibility

Generator:

`scripts/Y5_R2FR_4992_mixed_hphi_cut_and_full_box_completion.py`

Independent validator:

`scripts/Y5_R2FR_4992_mixed_hphi_cut_and_full_box_completion_validation.py`

The generator closes `20/29` gates. The validator reconstructs both spinor
charts without importing the generator and passes `351/351` checks.

No local-GR or full-MTS claim is promoted by this checkpoint.
