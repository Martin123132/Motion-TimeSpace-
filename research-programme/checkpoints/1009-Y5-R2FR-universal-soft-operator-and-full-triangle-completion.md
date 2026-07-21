# 4993 - Universal soft operator and full triangle completion

Checked: `2026-07-14`.

Marker: `MTS_4993_UNIVERSAL_SOFT_OPERATOR_AND_TRIANGLE_COMPLETION`.

## 1. Result

All three one-mass scalar-triangle coefficients in the one-loop
opposite-helicity `h h phi phi` amplitude are now fixed exactly. This uses
the completed 4992 box sector and the universal one-loop gravitational soft
operator, not a fitted crossing polynomial.

In the convention

```text
M1=kappa^4 F/<1|3|2]^4,
s+t+u=0,
```

the triangle kernel is

```text
F_triangle=T_s I3(s)+T_t I3(t)+T_u I3(u),

T_s=(t+u)
    [t^6+t^5u+2t^4u^2+2t^2u^4+tu^5+u^6]/8,

T_t=-t^5(t^2+tu+2u^2)/8,

T_u=-u^5(2t^2+tu+u^2)/8.
```

These coefficients reproduce every channel’s universal
`log(-x)/epsilon` pole, obey `T_t(t,u)=T_u(u,t)`, and cancel the entire
box-plus-triangle `1/epsilon^2` coefficient.

## 2. Source normalization

Dunbar and Norridge give the one-loop gravitational soft factor as

```text
N_epsilon kappa^2/(4 epsilon^2) A_tree
  sum_pairs (-s_ij)^(1-epsilon),
```

and explicitly state that it is universal when the external legs are
gravitons or scalars. For four massless external legs, each of `s,t,u`
occurs twice:

```text
sum_pairs =
  2[(-s)^(1-epsilon)+(-t)^(1-epsilon)+(-u)^(1-epsilon)].
```

Expanding,

```text
sum_pairs|epsilon^0=-2(s+t+u)=0,

d/d epsilon sum_pairs|0
 =2[s log(-s)+t log(-t)+u log(-u)].
```

The universal four-point singularity is therefore

```text
N_epsilon kappa^2/(2 epsilon)
 [s L_s+t L_t+u L_u] A_tree,
```

with no universal double pole.

## 3. Integral pole basis

After stripping the common `N_epsilon`, the sourced massless basis is

```text
I4(x,y)=1/(xy)
 [4/epsilon^2-2(L_x+L_y)/epsilon+...],

I3(x)=-1/x
 [1/epsilon^2-L_x/epsilon+...],

I2(x)=1/epsilon-L_x+2+....
```

Consequently:

- boxes and triangles own the `L_x/epsilon` coefficients;
- each `I3(x)` is the only remaining owner after the boxes are known;
- bubbles can alter constant simple poles and finite single logs, but cannot
  alter this triangle solve.

## 4. Tree phase

The opposite-helicity tree is

```text
M0=kappa^2 Q^4/(4stu),
Q=<2|3|1],
Qbar=<1|3|2],
Q Qbar=tu.
```

Rewriting it in the one-loop phase convention gives

```text
M0=kappa^2/Qbar^4 [t^3u^3/(4s)].
```

The reduced universal logarithmic targets are therefore

```text
U_s=t^3u^3/8,
U_t=t^4u^3/(8s),
U_u=t^3u^4/(8s).
```

## 5. Unique triangle solve

With the 4992 box coefficients `B_st,B_su,B_tu`, the box contributions
to each logarithmic pole are

```text
X_s=-2B_st/(st)-2B_su/(su),
X_t=-2B_st/(st)-2B_tu/(tu),
X_u=-2B_su/(su)-2B_tu/(tu).
```

The three equations are diagonal in the unknown triangle coefficients:

```text
X_s+T_s/s=U_s,
X_t+T_t/t=U_t,
X_u+T_u/u=U_u.
```

Their Jacobian determinant is

```text
det=1/(stu),
```

which is nonzero away from physical factorization boundaries. The solution
is therefore unique in the declared integral basis and gives the
coefficients in section 1.

For the `s` channel, checkpoint 4991 supplied the sourced component

```text
T_s^(hh)=-(t^7+u^7)/16.
```

The difference `T_s-T_s^(hh)` is the infrared-fixed
identical-scalar-intermediate remainder; it is not falsely attributed to
the 4991 source.

## 6. Pole reconstruction

The exact residuals are

```text
[X_s+T_s/s]-U_s=0,
[X_t+T_t/t]-U_t=0,
[X_u+T_u/u]-U_u=0.
```

The complete double-pole coefficient is

```text
4B_st/(st)+4B_su/(su)+4B_tu/(tu)
 -T_s/s-T_t/t-T_u/u
=0.
```

This is a stronger checksum than the partial 4991 double pole: the latter
was nonzero because it represented only one state/channel component.

## 7. Remaining work

The standard box and one-mass triangle sectors are now complete. The full
one-loop amplitude still requires:

- `I2(s)`, `I2(t)`, and `I2(u)` coefficients from cut IBP;
- separation of constant infrared and ultraviolet simple poles;
- `D`-dimensional `mu^2`, evanescent, and rational completion;
- one common finite infrared subtraction;
- only then, insertion into the outer crossed `hh` cut.

The next calculation should reduce the mixed and scalar cut numerators to
the bubble masters in `D=4-2epsilon` and use channel crossing as a baseline
consistency test.

## 8. Reproducibility

Generator:

`scripts/Y5_R2FR_4993_universal_soft_operator_and_full_triangle_completion.py`

Independent validator:

`scripts/Y5_R2FR_4993_universal_soft_operator_and_full_triangle_completion_validation.py`

The generator closes `16/25` gates. The validator independently solves a
fresh symbolic three-by-three system and passes `404/404` checks.

No complete-one-loop, outer-cut, local-GR, or full-MTS claim is promoted.
