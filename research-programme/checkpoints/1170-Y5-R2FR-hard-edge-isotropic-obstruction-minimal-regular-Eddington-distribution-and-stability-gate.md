# 5154 - Hard-edge isotropic obstruction, regular Eddington distribution and cog-preservation gate

Marker: `MTS_5154_EDDINGTON_PHASE_SPACE_POSITIVE_DF_GATE`.

Date: `2026-07-20`.

## Decision

Checkpoint 5154 makes the machine-cog requirement operational. It does not
switch gravity laws between Mercury and galaxies. It asks whether the same
checkpoint-5151 motion density can be a finite collisionless source, vanish
smoothly into the ordinary GR vacuum, preserve every measured galaxy radius,
and remain no larger than the already-bounded local metric residue.

The checkpoint-5153 hard cut is **not** a regular isotropic distribution. That
is now an exact theorem, not a numerical preference. A universal smooth branch
does exist at the discretized Eddington/Vlasov gate: the minimal even
polynomial `C1` taper passes positivity and the standard monotone-energy
sufficient stability test over all `1050` fixed
states without a per-galaxy edge parameter. The result is an existence and
compatibility advance, not a proof that parent collapse selects the taper.

## 1. Exact hard-edge obstruction

For relative potential `Psi=E_cut-Phi` and relative energy
`E=Psi-v^2/2`, every isotropic nonnegative distribution obeys

```text
rho(Psi)=4 pi sqrt(2) integral_0^Psi
          f(E) sqrt(Psi-E) dE.
```

If `f` is locally integrable at escape energy,

```text
0 <= rho(Psi)
   <= 4 pi sqrt(2 Psi) integral_0^Psi f(E)dE -> 0.
```

The 5153 hard edge instead has `rho(R_t^-)>0` and `rho(R_t^+)=0`.
Therefore no locally integrable nonnegative isotropic `f(E)` can own that
edge. A singular ansatz `f~E^k` gives

```text
rho ~ 4 pi sqrt(2) F B(k+1,3/2) Psi^(k+3/2),
```

and a nonzero boundary density would require `k=-3/2`, outside local
integrability. The circular `p_r=0` Einstein-cluster branch is not erased; it
is simply not allowed to masquerade as an isotropic halo.

## 2. Least-deforming regular edge

Write `y=r/R_t` and multiply only the finite-core density by

```text
E_p(y)=(1-y^2)^p_+.
```

Near the edge, `Psi proportional R_t-r`, so `rho proportional Psi^p` and
`f(E) proportional E^(p-3/2)`. A bounded escape-energy distribution requires
`p>=3/2`. The exact minimum is `p=3/2`. If the edge is additionally required
to be the lowest even polynomial in `y`, preserve the regular centre, and join
the vacuum with both density and density slope zero, the first member is

```text
E_2(y)=(1-y^2)^2_+,
f(E) proportional sqrt(E) at escape.
```

This selects one global candidate from stated regularity conditions; it is not
yet a coefficient derived from nonlinear parent evolution. The full execution
also retains `p=3/2` as the no-stronger-than-bounded comparator.

## 3. Self-consistent finite radius

For the lower-cut positive mixture, define

```text
D_q,c(x)=[S+x S']/x^2,
I_p(X)=integral_0^X [S+x S'](1-x^2/X^2)^p dx.
```

The unchanged metric-only spherical-collapse boundary gives the scalar root

```text
X^3 = 2 [v_infinity/(H0 R_n)]^2 I_p(X)
      /(f_X Delta_vir,c),
R_t=X R_n.
```

All roots are positive and unique in the executed bracket. For `p=2`,
`R_t/R_n` spans `9.92665178080655` to
`96.52894753606238`. The maximum independent
radial-versus-Gauss mass disagreement is
`6.437678283788273e-07` and the maximum virial
identity residual is `1.4166445794216997e-13`.

## 4. Eddington inversion rather than assumed circularization

The density and self-potential were inverted through the Abel equation itself.
For energy bins `[E_j,E_(j+1)]` with piecewise-constant `f_j`,

```text
rho(Psi_i)=sum_j A_ij f_j,
A_ij=(8 pi sqrt(2)/3)
 [ (Psi_i-E_j)_+^(3/2)-(Psi_i-E_(j+1))_+^(3/2) ].
```

The endpoint-clustered lower-triangular system is unique. Across all
`2100` comparator and selected rows:

```text
p=3/2 positive rows = 1050
                     /1050,
p=3/2 monotone rows = 0
                     /1050,
p=2 positive rows   = 1050
                     /1050,
p=2 monotone rows   = 1050
                     /1050.
```

`df/dE>=0` in relative energy is the usual `df/dE_physical<=0` sufficient
stability sign. The `p=3/2` branch remains positive but is not promoted if its
global monotonic sign fails. The `p=2` branch's worst independent midpoint
density reconstruction error below normalized energy `0.999` is
`0.0018176368384881236`. Selected worst-case
profiles were repeated at energy orders 64, 128 and 256; positivity and the
monotonic sign survive the convergence audit.

This is a numerical distribution-existence certificate, not a nonlinear
stability theorem and not a relativistic Einstein-Vlasov solve.

## 5. Does the same construction jam either cog?

No `q_parent`, `L_eff`, `v_infinity`, baryonic term, mass, edge power or
per-galaxy shape was fitted. The fixed `p=2` state was evaluated for both
parent mappings, three predeclared masses, all 175 galaxies and all 3391
measured radii: `20346` point evaluations.

```text
maximum measured r/R_t                 = 0.2995150824346973,
maximum support change from parent      = 0.062369905328974684,
maximum per-galaxy absolute Delta RMSE  = 1.1145659531539565 km/s,
maximum pooled absolute Delta RMSE      = 0.16485407799665097 km/s.
```

The local branch is not activated by a second coupling. Since
`0<=E_2<=1`, its density and enclosed motion mass never exceed the already
bounded untapered parent source. The inherited checkpoint-5152 ceiling on the
Mercury halo-tide/solar ratio therefore remains
`3.100454538921604e-13` (Mercury specifically
`6.614360568718464e-19`); direct scalar fifth force remains zero on
the same reflection-even universal-metric branch. Outside `R_t`, density and
isotropic pressure vanish and the metric continuation is vacuum Schwarzschild
at leading weak-field order. A full embedded Solar-System PPN likelihood is
still required.

This is the intended machine behavior: the local cog is not replaced or
retuned, while the same positive source can remain active on galactic scales.

## 6. Exact status and next calculation

```text
hard isotropic density step                       = rejected exactly;
positive finite isotropic DF for universal p=2    = passes discrete gate;
monotone-energy sufficient stability sign         = passes discrete gate;
smooth finite mass and vacuum stress limit         = constructed;
all measured galaxy radii preserved without refit = tested;
local source ceiling not enlarged                  = proved by positivity;

parent collapse selects p=2 and q_parent           = not derived;
fully relativistic Einstein-Vlasov continuation    = not derived;
flattened rotating distribution and lensing        = not derived;
primordial perturbation probability                = not derived.
```

The next decisive calculation is the fixed initial-value problem, not another
source inventory: evolve the checkpoint-5152 reflection-even primordial state
under the parent weak-field Schrodinger--Poisson/Vlasov equations at the three
locked masses. Test whether coarse-graining approaches the projective core and
the universal regular edge without fitting either. Failure demotes the smooth
branch to closure; success supplies the missing formation mechanism.

Primary references:

- compact Vlasov support: https://arxiv.org/abs/gr-qc/9812061
- Eddington boundary consistency: https://arxiv.org/abs/1805.02403
- cored-profile inversion: https://arxiv.org/abs/1401.0726
- isotropic stability comparator: https://arxiv.org/abs/astro-ph/0208565
- static Einstein--Vlasov states: https://arxiv.org/abs/gr-qc/9304028

All `25` validation rows pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. The galaxy corpus was
read-only. No GitHub action occurred.
