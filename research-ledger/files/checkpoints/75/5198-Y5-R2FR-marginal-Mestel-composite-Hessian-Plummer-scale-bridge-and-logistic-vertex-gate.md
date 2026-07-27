# 5198 - Marginal-Mestel composite Hessian, Plummer scale bridge and logistic vertex gate

Marker: `MTS_5198_MARGINAL_MESTEL_COLLECTIVE_HESSIAN_SCALE_BRIDGE`.

Date: `2026-07-24`.

Status: private derived-and-executed checkpoint. No GitHub action. No
`formalization-workbench` or galaxy-repository edit.

## 1. Verdict

Checkpoint 5197 proved that the late-time cosmology pole cannot also be the
old massive-particle galaxy pole. This checkpoint takes the surviving route
seriously: the galaxy length is the scale of an **occupied collective
surface-stress mode**, not the Compton length of the elementary vacuum pole.

The calculation makes four real advances.

1. A conserved axisymmetric phase surface stress has the exact WKB
   metric-dressed eigenvalue

   ```text
   omega^2=lambda(k)
     =kappa^2+c_R^2 k^2
      -2 pi G Sigma_chi |k| exp(-|k|H_chi).
   ```

   The exponential is not an inserted screening function. It is the
   two-dimensional Fourier transform of the already selected Plummer
   vertical Green function.

2. The outer MTS phase is a finite Mestel-like disk. Requiring its
   phase-only outer branch to be marginal fixes the radial dispersion:

   ```text
   c_R^2=Gamma0 L_eff/8.
   ```

   This is one universal amplitude law, not one fitted sound speed per
   galaxy.

3. With the already selected phase values

   ```text
   q=0.77,
   c_q=4.640081689829917,
   H_chi/L_eff=0.02,
   B=8,
   s=4,
   ```

   the Plummer-softened mode at `R=L_eff` gives

   ```text
   k_star L_eff=2.9218908789809075.
   ```

   Checkpoint 5148 independently constructed the spectral-to-real scale
   conversion

   ```text
   mu_spectral L_eff=2.921396974200681.
   ```

   Their fractional difference is `1.6906458950560754e-4`, or `0.0169%`.
   Equating the two scale constructions while varying `q` gives

   ```text
   q_self-consistent=0.7698811733853892,
   ```

   only `0.0154%` below the locked `0.77`.

4. The quadratic carrier does **not** derive the exact logistic saturation.
   The required third- and fourth-order composite vertices are now written
   exactly. A canonical linear identification with the bare
   `|psi|^(4/3)` parent potential is rejected by a field-normalization
   invariant vertex ratio.

Therefore the collective route is retained as the best current owner of the
galaxy scale and radial phase stiffness. The result is not yet a galaxy
claim or a complete parent-action derivation.

## 2. Exact collective Hessian

Take an axisymmetric WKB surface perturbation

```text
delta Sigma, delta u_R, delta u_phi
  proportional to exp[i(kR-omega t)].
```

Continuity and the two Euler equations are

```text
-i omega delta Sigma+i k Sigma delta u_R=0,

-i omega delta u_R-2 Omega delta u_phi
  =-i k(delta h+delta Phi),

-i omega delta u_phi
  +kappa^2 delta u_R/(2 Omega)=0,

delta h=(c_R^2/Sigma)delta Sigma.
```

For the Plummer kernel used by the current phase disk,

```text
delta Phi_k(z=0)
  =-2 pi G delta Sigma_k exp(-|k|H_chi)/|k|.
```

Eliminating `delta Sigma`, `delta u_phi`, and `delta Phi` gives

```text
omega^2
  =kappa^2+c_R^2 k^2
   -2 pi G Sigma_chi |k| exp(-|k|H_chi).
```

In the razor-thin limit,

```text
k_star=pi G Sigma_chi/c_R^2,

lambda_min
  =kappa^2-(pi G Sigma_chi)^2/c_R^2
  =kappa^2(1-Q_chi^-2),

Q_chi=kappa c_R/(pi G Sigma_chi).
```

This is a Schur reduction of the gravitational constraint against a
conserved material mode. It does not dress the local vacuum graviton and it
is not an additional source to add after the phase stress has already been
included.

## 3. Derived radial amplitude

The current outer phase normalization is

```text
Sigma_chi=Gamma0/(2 pi G y),
V_chi^2=Gamma0 L_eff,
y=R/L_eff.
```

Its phase-only epicyclic frequency is

```text
kappa_chi^2=2 Gamma0/(L_eff y^2).
```

Setting the thin outer branch to marginality,

```text
Q_chi=1,
```

gives, without a fit,

```text
c_R^2
  =(pi G Sigma_chi)^2/kappa_chi^2
  =Gamma0 L_eff/8.
```

Equivalently, this is the familiar fluid marginality relation for a Mestel
disk:

```text
c_R=V_flat/(2 sqrt(2)).
```

For an isotropic two-dimensional pressure `P_R=c_R^2 Sigma`, stationary
radial conservation gives

```text
v_stream^2
  =V_total^2+c_R^2 d ln(Sigma_chi)/d ln R,

d ln(Sigma_chi)/d ln R
  =q(1-n)-s(1-b)-1.
```

The executed phase profile keeps this background streaming speed positive
through the active annulus. It crosses zero only in the unresolved central
core at approximately `R/L_eff=0.03445`. Thus the simple rotating
barotropic realization is not extended through `R=0`; the central regulator
still needs its own regular stress completion.

## 4. Scale bridge

At `y=1`, define

```text
n_1=c_q/(1+c_q),
b_1=1/[1+(1/B)^s],
x=k_star L_eff,
eta=H_chi/L_eff.
```

The stationary point of the Plummer-softened eigenvalue obeys

```text
x/8=(n_1 b_1/2) exp(-eta x)(1-eta x).
```

For the locked phase geometry this returns

```text
n_1=0.8226976035111017,
b_1=0.9997559189650964,
x=2.9218908789809075.
```

The same point has

```text
Q_phase=1.0316389135149029,
lambda_min/kappa_phase^2=0.16689357984608252,
static enhancement=kappa_phase^2/lambda_min=5.991842232171239,
2 pi/(k_star L_eff)=2.150383285145483.
```

So the present branch is soft but positive, and its physical wavelength is
of order `L_eff`.

The no-thickness control gives

```text
k_star L_eff=3.289987194514496,
```

which misses the checkpoint-5148 conversion by about `12.6%`. Conversely,
holding `q=0.77` and the checkpoint-5148 scale fixed predicts

```text
eta_required=0.02003144295023986,
```

within `0.157%` of the selected `0.02`.

This is an internal closure, not independent evidence. Both constructions
use the same locked phase shape, and the checkpoint-5148 least-squares scale
is broad: a `0.1%` increase in shape loss spans `0.0960` in `mu L`, while a
`1%` increase spans `0.3039`. The important result is that the collective
Hessian can own the old scale map without adding a new parameter, not that
the many printed digits are statistically measured.

## 5. Universal radial replay

The executed `B8-s4` disk kernel was differentiated directly. Across

```text
0.5 <= R/L_eff <= 2,
```

the phase-only thin `Q` values are

```text
minimum=1.0310543423768779,
median=1.035047406061021,
maximum=1.0461419549668172.
```

The maximum departure from unity is `4.614%`. The Plummer-softened minimum
eigenvalue is positive over the complete stored kernel, and the active
phase-only static enhancement has median `6.080455978037317`.

This is a structural result: the existing finite phase disk is already very
close to a marginal finite-Mestel state when supplied with the newly derived
`Gamma0 L_eff/8` radial dispersion. No galaxy-by-galaxy pressure coefficient
was used.

## 6. Clean 160-galaxy replay

The current read-only clean radius grid and baryonic curves were then added
to the same Hessian. Over `11,606` active-annulus points from `160` galaxies:

```text
collective-law median Q              =1.2318967151151314,
collective-law Q p16--p84            =[1.1435508648632142,
                                       1.4267061348527654],
fraction with 0.8 <= Q <= 1.25       =0.5635877994140962,
median phase fraction                =0.6807415595193027,
median positive response enhancement =2.3779259682473963,
median k_star L_eff                  =3.1965034685067053.
```

The per-galaxy active medians are

```text
median Q                             =1.2372389749191437,
median static enhancement            =2.3649473286482694.
```

The enhancement rises with phase dominance: the correlation between phase
fraction and log enhancement is `0.8017090476912597`. Baryon-dominated
systems are therefore stiffer and receive less collective amplification,
while phase-dominated systems remain nearer the soft branch. This is the
desired environmental direction, obtained from the common metric
constraint rather than an arena-specific coupling.

Four active points in two galaxies are not erased:

```text
NGC6015: R=26.3167, 26.5595 kpc,
NGC6946: R=15.8177, 15.9874 kpc.
```

Their one-dimensional interpolated `lambda_min` is negative. They are
explicit countercases requiring the native two-dimensional derivative and
stability replay; they are not silently clipped into a pass.

## 7. Spherical EOS decision

The earlier nonanalytic-phase file explicitly called its EOS a
**spherical-equivalent diagnostic** and required an axisymmetric anisotropic
stress. Treating that reconstructed sound speed as the disk radial sound
speed gives

```text
active median Q_EOS=2.5469398905272422,
median c_EOS^2/(Gamma0 L_eff/8)=4.344143528923965,
fraction with 0.8 <= Q_EOS <= 1.25
  =8.616232982939858e-5.
```

It is too stiff to own the collective soft branch. The direct identification
is rejected. This does not reject the earlier diagnostic; it supplies the
axisymmetric radial component that diagnostic said was missing.

## 8. Local-vacuum theorem and counting rule

The phase coordinate is a fluctuation of an occupied surface stress. In the
local vacuum,

```text
Sigma_chi=0,
state occupation=0,
delta Sigma_chi is absent.
```

There is therefore no extra collective residue and no second vacuum pole.
The block-diagonal checkpoint-5187 local metric, photon and motion Hessian is
unchanged.

The mode must also not be double counted. It can be used to derive or test
the phase state and its response, but its polarization cannot then be added
again as a second source on top of `T_phase`. This distinguishes the route
from replaying the already counted classical Vlasov response.

## 9. Exact logistic vertex contract

The present radial flows are

```text
dn/du=q n(1-n),
db/du=-s b(1-b),
u=ln(R/L_eff).
```

The inner equation follows from the Bogomolny functional

```text
F_n=E0 integral du {
  1/2 (dn/du)^2
 +q^2 n^2(1-n)^2/2
}.
```

Writing the potential as

```text
V(n)=m2 n^2/2+g3 n^3/3!+g4 n^4/4!,
```

requires exactly

```text
m2=q^2=0.5929,
g3=-6q^2=-3.5574,
g4=12q^2=7.1148.
```

The outer anti-kink requires

```text
m2=s^2=16,
g3=-96,
g4=192.
```

A reflection-even completion is possible if `n` is a normalized two-point
occupation or a composite such as `psi^2/v^2`; the reduced potential then
contains the allowed `psi^4`, `psi^6`, and `psi^8` sequence.

The bare parent potential does not directly give these vertices. About any
nonzero canonical background,

```text
V=(3/4)g_psi |psi|^(4/3),

V''   =g_psi/(3|psi|^(2/3)),
V'''  =-2g_psi/(9|psi|^(5/3)),
V'''' =10g_psi/(27|psi|^(8/3)).
```

The canonical-linear field-rescaling invariant

```text
I=(V''')^2/(V'' V'''')
```

is

```text
I_fractional=2/5,
I_logistic=3.
```

They differ by a factor `7.5`. Thus no canonical linear identification of
the one-field bare potential with the logistic order parameter works. A
nonlinear field redefinition would also change the kinetic metric and is not
a derivation.

The surviving route is precise: the occupied-state 2PI action for the
reflection-even covariance/occupation must generate the displayed
`m2:g3:g4` ratios. The quadratic Hessian derived here fixes only `m2`; it
cannot determine `g3` and `g4`.

## 10. Claim boundary

Checkpoint 5198 derives:

- the metric-dressed collective surface-mode Hessian;
- the outer marginal-Mestel radial amplitude law;
- exact local-vacuum silence of that state mode;
- an internal spectral/collective scale closure;
- the exact nonlinear vertex contract;
- rejection of the spherical-EOS and direct bare-fractional shortcuts.

It does **not** yet derive:

- formation and self-regulation of the occupied state from the four-
  dimensional parent action;
- the composite 2PI cubic and quartic vertices;
- the complete conserved anisotropic stress through the central and outer
  regulators;
- `Gamma0` from the parent couplings;
- a galaxy, lensing, local-GR, or full-MTS claim.

The next non-circular calculation is therefore the composite 2PI nonlinear
vertex calculation. It must either return the logistic ratios from the
parent occupied state or demote the exact `n,b` flows to an explicit
reduced-state closure.

## 11. Artifacts

Generator:

- `scripts/Y5_R2FR_5198_marginal_Mestel_collective_Hessian_scale_bridge.py`

Outputs:

- `source-intake/functional_rg/5198/collective_Hessian_derivation.csv`
- `source-intake/functional_rg/5198/universal_phase_soft_mode_profile.csv`
- `source-intake/functional_rg/5198/spectral_collective_scale_bridge.csv`
- `source-intake/functional_rg/5198/q_scale_self_consistency_sweep.csv`
- `source-intake/functional_rg/5198/clean_galaxy_collective_case_summary.csv`
- `source-intake/functional_rg/5198/radial_band_collective_summary.csv`
- `source-intake/functional_rg/5198/spherical_EOS_rejection_and_radial_stress_selection.csv`
- `source-intake/functional_rg/5198/logistic_composite_vertex_contract.csv`
- `source-intake/functional_rg/5198/route_decision.csv`
- `source-intake/functional_rg/5198/source_provenance.csv`
- `source-intake/functional_rg/5198/marginal_Mestel_collective_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5198_VALIDATION.csv`
