# 4989 - Global D1 master, exact cut sum rules, and opposite-helicity hh support

Checked: `2026-07-14`.

Marker: `MTS_4989_GLOBAL_D1_MASTER_SUM_RULES_HH_SUPPORT`.

> **Superseded in part by checkpoint 4990.** Sections 2, 3, 5, 6, 7, and
> 8 used a direct-channel/crossing mismatch. The corrected statements are:
> the 4988 values are additive scalar-cut subtotals; the amplitude-scheme
> coefficient is `D C=-203/10`, not the FRG value `+16`; tree-level
> three-particle cuts are not assigned `mu` slopes; and the `hh` low-spin
> zero is direct-channel only. See
> `4990-Y5-R2FR-crossing-complete-D1-scheme-separation-and-hh-scope-correction.md`.

## 1. Result

This checkpoint closes the once-global anomalous-action subtraction and
reduces the missing low-spin two-loop calculation from three cut classes to
two.

The exact master is

```text
R_master(z,L)=2 sum_cuts D_cut(z,L)-G(z,L),
G=D1 ReF1=16 ReF1.
```

The opposite-helicity graviton two-particle cut starts at `J=4`. It therefore
has exactly zero projection onto the `J=0,2` coordinates that determine
`K_mu` and `K_ang`. The only remaining low-spin unknowns are the mixed `hhh`
and `phiphih` three-particle cuts.

This is a genuine reduction, not a closure assumption. Numeric full `K_mu`,
`K_ang`, exact all-operator local GR, and full MTS remain open.

## 2. Factor-of-two normalization correction

Bern's optical-theorem convention is

```text
2 Im F=U.
```

For the physical logarithm,

```text
Disc ln(-s/mu^2)=-2pi i,
```

so a coefficient `c ln(-s/mu^2)` obeys

```text
c=-U/(2pi).
```

Checkpoint 4988 calculated

```text
D_phiphi=Disc_s/(-2pi i s^3)=-U_phiphi/(2pi s^3).
```

The real two-loop master instead contains `-U/pi`. Therefore

```text
-U_phiphi/(pi s^3)=2D_phiphi.
```

The exact 4988 values

```text
-85.0641390166317,
 23.6697802325722
```

are consequently raw half-master projector coordinates
`Khat_mu_cut^(phiphi)` and `Khat_ang_cut^(phiphi)`, not additive
`Delta K_mu` and `Delta K_ang` invariants. The 4988 generator, validator,
formal note, handoffs, claim row, and variable row have been corrected.

## 3. Exact global D1 operator

The 4986 reduced amplitude and one-loop flow are

```text
R=-3W stu+C F1+F2,
dC/dlnmu=16.
```

At the order entering the real two-loop master, the one-loop dilatation
operator acts on the `C F1` term. Hence

```text
G=D1 ReF1=beta_C partial_C(C ReF1)=16 ReF1.
```

No cut-by-cut allocation of `G` is permitted. It is subtracted exactly once
after the complete cut sum.

## 4. Physical-channel kernel

Set

```text
s=1,
t=-x,
u=-(1-x),
L=ln(s/mu^2),
0<x<1.
```

Using

```text
F1=(2/pi)[(23/15)L_A-(1/30)L_B],
```

the global subtraction becomes

```text
G(x,L)=G0(x)+[144/pi]x(1-x)L,
```

where

```text
G0(x)=-(32/pi){
 (23/15)[x^3 ln x+(1-x)^3 ln(1-x)]
 +(1/30)x(1-x)[ln x+ln(1-x)]
}.
```

The scale polynomial is exactly

```text
coefficient_L[G]
 =144x(1-x)/pi
 =(24/pi)[P0(z)-P2(z)],
z=1-2x.
```

The physical `s`-channel logarithmic discontinuity of this subtraction is

```text
Disc_s G/(-2pi i s^3)
 =(32/pi)[23/15-x(1-x)/30]
 =440/(9pi)+[8/(45pi)]P2(z).
```

## 5. Exact Legendre tower

Define

```text
A_J(m)=integral_0^1 dx x^m P_J(1-2x) ln x.
```

For `J>m`, direct polynomial integration gives

```text
A_J(m)=(-1)^(m+1)(m!)^2(J-m-1)!/(J+m+1)!.
```

For every even `J`, the constant moment of `G0` is

```text
g_J=-(32/pi)[(46/15)A_J(3)+(1/15)(A_J(1)-A_J(2))],
G_J=(2J+1)g_J.
```

The first exact coefficients are

```text
G_0 = 868/(135pi),
G_2 =-3716/(675pi),
G_4 =-6/(7pi),
G_6 =-442/(10125pi),
G_8 =-8296/(779625pi),
G_10=-68/(15015pi).
```

The complete `J=0` through `J=20` table is generated in
`source-intake/functional_rg/4989/D1_legendre_moment_tower.csv`.

Only `J=0,2` carry an `L` slope:

```text
G_0,L= 24/pi,
G_2,L=-24/pi,
G_J,L=0 for even J>=4.
```

## 6. Remaining-cut scale sum rules

Scale independence of

```text
R_master=2 sum D_cut-G
```

requires

```text
sum_cuts d0_L= 12/pi,
sum_cuts d2_L=-12/pi.
```

The exact scalar-cut slopes from 4988 are

```text
d0_phi,L=-2233/(72pi),
d2_phi,L=-203/(1800pi).
```

After subtracting the scalar contribution, the missing low-spin cuts must
satisfy

```text
d0_hhh,L+d0_phiphih,L= 3097/(72pi),
d2_hhh,L+d2_phiphih,L=-21397/(1800pi).
```

The graviton two-particle cut is absent from these equations by the support
theorem below.

For every even `J>=4`, locality of the final single-log target instead gives
the exact infinite checksum

```text
D_hh,J+D_hhh,J+D_phiphih,J=G_J/2.
```

The scalar cut has no support in this tower because its regularized Einstein
tree contains only `J=0,2`.

## 7. Opposite-helicity hh support theorem

For two-particle helicity partial waves, an amplitude with incoming helicity
difference `lambda` and outgoing difference `lambda'` is expanded in
`d^J_{lambda,lambda'}`. Here

```text
lambda_scalar=0,
abs(lambda_hh)=abs(+2-(-2))=4.
```

The scalar-to-opposite-helicity-graviton tree therefore uses

```text
d^J_{0,4},
```

which exists only when `J>=4`. The reverse amplitude uses `d^J_{4,0}` and
obeys the same bound. Their convolution can produce only `P_J(z)` with
`J>=4`.

The possible `lambda_hh=0` loophole is absent because the same-helicity tree
is source-exactly zero:

```text
M_tree(phi,+,+,phi)=0.
```

Hence

```text
D_hh,J=0 for J=0,2,
Delta K_mu^(hh)=0,
Delta K_ang^(hh)=0.
```

The higher-spin `hh` coefficients remain necessary as checks of the infinite
`J>=4` cancellation tower, but they cannot change the two desired low-spin
invariants.

## 8. Exact affine reduction of the remaining unknowns

Let

```text
r0=[d0_hhh+d0_phiphih]_(L=0),
r2=[d2_hhh+d2_phiphih]_(L=0).
```

Then the complete low-spin master is

```text
R0=2(d0_phi+r0)-868/(135pi),
R2=2(d2_phi+r2)+3716/(675pi).
```

The exact inverse projector gives

```text
K_mu
 =(-89221+1500pi^2)/(225pi)-12(r0-5r2)
 =-105.277943888086-12(r0-5r2),

K_ang
 =2(67537+24075pi^2)/(3375pi)+2(r0+7r2)
 =57.5594298775520+2(r0+7r2).
```

This is not a numerical determination of either invariant. It is the exact
two-number target the remaining three-particle calculation must fill.

## 9. Validation and next target

The generator closes `9/17` gates. The eight open gates are deliberate:
higher-spin numeric `hh`, both three-particle cuts, numeric full `K_mu` and
`K_ang`, finite `C_w`, exact all-operator local GR, and full MTS.

The independent validator does not import the generator. It reconstructs the
channel kernel, checks twenty rational events, derives and hard-codes eleven
Legendre coefficients through `J=20`, reassembles both scale rules, verifies
the affine slopes and helicity support, and passes `231/231` checks.

Primary outputs:

- `post-checkpoint-work/source-intake/functional_rg/4989/master_factor_two_normalization.csv`
- `post-checkpoint-work/source-intake/functional_rg/4989/D1_ReF1_channel_kernel.csv`
- `post-checkpoint-work/source-intake/functional_rg/4989/D1_legendre_moment_tower.csv`
- `post-checkpoint-work/source-intake/functional_rg/4989/remaining_cut_sum_rules.csv`
- `post-checkpoint-work/source-intake/functional_rg/4989/opposite_helicity_hh_support.csv`
- `post-checkpoint-work/source-intake/functional_rg/4989/master_affine_invariant_coordinates.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4989_VALIDATION.csv`

Next target: calculate the low-spin projections of the two three-particle
cuts. They alone determine `r0` and `r2`. The higher-spin `hh` calculation is
now a parallel locality checksum rather than a blocker for `K_mu/K_ang`.

No GitHub action.
