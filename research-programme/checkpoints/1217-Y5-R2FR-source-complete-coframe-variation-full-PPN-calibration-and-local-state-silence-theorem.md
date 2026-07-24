# 5201 - Source-complete coframe variation, full PPN calibration and local-state silence theorem

Marker: `MTS_5201_SOURCE_COMPLETE_COFRAME_PPN_LOCAL_SILENCE_THEOREM`.

Checked: `2026-07-24`.

## Decision

This checkpoint returns to the primary programme spine after checkpoint 5200
closed the bulk galaxy-projector ownership loop. It does not merely repeat
that “local GR is a target.” It varies the current parent source action,
executes the weak-field reduction, extends the old `beta/gamma` check to the
full ten-parameter constant PPN vector, calculates the source-calibration
rank, and proves the exact conditions under which the retained CTP boundary
sector is locally silent.

The explicit local parent under test is

```text
S_parent
 =(M_R^2/2) int d^4x e [R[e]-2 Lambda_cal]
 -(Z_A/4) int d^4x e F_mn F^mn
 +S_visible[e,omega_LC[e],A,Phi_visible]
 +S_motion[e,psi]
 +Gamma_controlled_EFT
 +Gamma_rho0.
```

It has one torsionless coframe, one Levi--Civita spin connection, one
canonical visible `U(1)` connection and the reflection-even motion sector.
These are explicit parent premises. The old one-scalar MTS corpus has not
derived the non-scalar coframe or visible charge representations.

The executed coframe Jacobian has

```text
16 coframe components;
rank(delta g/delta e)=10;
nullity=6;
rank(local Lorentz generators)=6;
maximum Lorentz-null residual=0.
```

Thus one coframe variation retains all ten symmetric Hilbert source
components and removes exactly the six local-Lorentz gauge directions. It
does not discard pressure, spin-improved stress, electromagnetic stress or a
trace component.

For visible matter,

```text
T_a^m=-(1/e) delta S_visible/delta e^a_m,
J^m=-(1/e) delta S_visible/delta A_m.
```

Local Lorentz, diffeomorphism and `U(1)` invariance give

```text
T_[ab]+(1/2)nabla_m S^m_ab=0,

nabla_m T_visible^m_n
 =F_nm J^m+sum_i E_i nabla_n Phi_i,

nabla_m J^m=0
```

and therefore, on all field equations,

```text
nabla_m(
 T_visible^m_n
 +T_EM^m_n
 +T_psi^m_n
 +DeltaT_EFT^m_n
 +DeltaT_state^m_n
)=0.
```

The same variation gives

```text
M_R^2(G_mn+Lambda_cal g_mn)
 =T_visible_mn+T_EM_mn+T_psi_mn
  +DeltaE_EFT_mn+DeltaT_state_mn.
```

The weak-field Einstein tensor was recalculated symbolically rather than
copied from a ledger. For

```text
ds^2=-(1+2 Phi)dt^2+(1-2 Psi)delta_ij dx^i dx^j,
```

the executable returns

```text
G00^(1)=2 nabla^2 Psi,
G12^(1)=partial_x partial_y(Psi-Phi).
```

With negligible local anisotropic stress and vanishing boundary values,

```text
Phi=Psi.
```

The `00` equation then gives

```text
2 M_R^2 nabla^2 Phi=rho,

nabla^2 Phi
 =rho/(2M_R^2)
 =4 pi G_N rho,

G_N=1/(8 pi M_R^2).
```

Hence

```text
Phi=-G_N M/r,
a=-grad Phi,
```

with the same `G_N` that multiplies the Einstein source and graviton
exchange. No separate Newton, orbital, lensing or wave coupling appears.

The exact isotropic Schwarzschild witnesses expand as

```text
g00
 =-[(1-U/2)/(1+U/2)]^2
 =-1+2U-2U^2+O(U^3),

gij
 =(1+U/2)^4 delta_ij
 =[1+2U+(3/2)U^2+O(U^3)]delta_ij.
```

Therefore

```text
beta=1,
gamma=1.
```

The remaining constant PPN parameters are fixed by the same local branch:

```text
xi=0;
alpha_1=alpha_2=alpha_3=0;
zeta_1=zeta_2=zeta_3=zeta_4=0.
```

This is not inferred merely from “looking like GR.” On the branch

```text
psi=0,
nabla psi=0,
DeltaT_state=0,
```

there is one local Lorentz coframe, no preferred timelike/vector background,
no additional local pole, no Whitehead/preferred-location term and an
action-based covariantly conserved total Hilbert stress. Those conditions
remove the preferred-frame and nonconservation PPN structures. The
checkpoint therefore derives the complete constant vector

```text
(gamma,beta,xi,alpha_1,alpha_2,alpha_3,
 zeta_1,zeta_2,zeta_3,zeta_4)

=(1,1,0,0,0,0,0,0,0,0)
```

inside the declared local branch.

The Maxwell calculation is also executed from the same coframe. Variation
of

```text
S_EM
 =int e[-Z_A F^2/4+c_IR C_mnrs F^mn F^rs]
```

gives

```text
Z_A nabla_m F^mn
-4 c_IR nabla_m(C^mnrs F_rs)
=J^n.
```

In a local flat frame, `C_mnrs=0` and ordinary Maxwell theory is exact for
every `c_IR`. Direct symbolic contraction gives

```text
F_mn F^mn=2(B^2-E^2),

T_EM^00=(E^2+B^2)/2,

T_EM^0i=(E cross B)^i,

T_EM^m_m=0.
```

On the Maxwell and matter equations,

```text
nabla_m T_EM^m_n=-F_nm J^m,
nabla_m T_visible^m_n=+F_nm J^m,
```

so the Poynting vector is the energy flux of the same Hilbert source. It is
not an additional background field or an independent gravitational
coupling.

The ten-observable calibration matrix was then evaluated using primitive
normalizations

```text
(ln M_R, ln e, ln Z_A).
```

For Einstein, exchange, Newton, orbit, lensing and waves, every sensitivity
row is

```text
(-2,0,0).
```

For Coulomb, Lorentz, Maxwell energy and Poynting, every row is

```text
(0,2,-1).
```

The ranks are

```text
gravity block rank=1;
electromagnetic block rank=1;
combined rank=2.
```

The field-normalization direction `(0,1,2)` is an exact null direction.
There are therefore exactly two leading local source normalizations:

```text
G_N <-> M_R,
alpha_EM <-> e^2/Z_A.
```

There are no arena-dependent calibrations.

For six representative source classes, the soft/Bianchi difference matrix
has

```text
rank=5,
nullity=1,
nullspace span=(1,1,1,1,1,1).
```

Thus ordinary mass, binding energy, electromagnetic stress, motion stress,
clock energy and radiation all lie on one common spin-two source direction.

Using the locked locally calibrated value

```text
G_N=6.708832120298927e-57 eV^-2,
```

the derived reduced gravitational scale is

```text
M_R=[8 pi G_N]^-1/2
   =2.435323210689248e27 eV.
```

The relation and cross-arena universality are derived. The numerical value
of `G_N` is not predicted by the present dimensionless parent: it remains one
absolute gravitational calibration. This is not a local-GR failure—GR also
takes its Newton scale from measurement—but it remains an honest unification
boundary if MTS aims eventually to predict all scales.

The CTP boundary-state issue is now equally sharp. For the binary state

```text
rho(n)=(1-n)rho_0+n rho_1,
```

vacuum subtraction gives the exact identity

```text
DeltaT_mn[n]
 =Tr[(rho(n)-rho_0)T_mn]
 =n(T1_mn-T0_mn).
```

Therefore

```text
DeltaT_mn[0]=0.
```

However its divergence is

```text
nabla_m DeltaT^m_n
 =(partial_m n)DeltaT10^m_n
 +n nabla_m DeltaT10^m_n.
```

Exact local silence consequently requires

```text
n=0 and partial_m n=0
```

on an open local domain. A pointwise zero alone is insufficient. Moreover,
for finite `u` and finite positive `q`,

```text
n(u)=1/[1+exp(-q(u-u0))]
```

obeys strictly `0<n<1`. A universal finite logistic profile cannot supply an
exact local vacuum. The mathematically clean route is the separation already
selected in checkpoint 5197:

```text
rho_local=rho_0,
rho_collective=rho[n_environment].
```

These can be different state branches of one parent action. This proves
compatibility; it does not yet derive a preparation/attractor mechanism that
selects `rho_0` locally.

The final result is:

```text
one coframe source variation:
  derived;

all ten symmetric metric source components:
  retained;

total stress Ward identity:
  derived on shell;

Einstein -> Poisson -> Newton:
  executed;

same residue for orbit, lensing and waves:
  derived;

full constant PPN vector:
  GR on the declared local-vacuum branch;

Maxwell -> stress -> Poynting:
  executed from the same coframe;

leading local calibration rank:
  two, with no arena retuning;

G_N relation:
  derived;

absolute numerical G_N:
  one measured scale, not predicted;

local boundary-state silence:
  exact on an open P0-vacuum domain;

dynamic selection of that local vacuum:
  open;

non-scalar coframe from old one-scalar MTS:
  not derived;

full MTS unification:
  not claimed.
```

## 1. Parent premises versus derived consequences

The no-smuggling split is:

| Item | Status |
|---|---|
| One nondegenerate coframe `e^a_m` | parent field-content premise |
| `omega=omega_LC[e]` | torsionless parent premise |
| One visible `U(1)` connection | parent field-content premise |
| Visible matter uses `e,omega,A` | universal matter-functor premise |
| Reflection-even motion sector | sourced parent result |
| Fierz--Pauli/Einstein two-derivative kinetic structure | selected by gauge/nullspace theorem |
| Ten-component Hilbert source map | derived and rank-verified here |
| Ward identities | derived here |
| Poisson/Newton normalization relation | derived here |
| Full constant PPN vector | derived here under the local-vacuum conditions |
| Maxwell energy and Poynting stress | derived and symbolically verified here |
| Absolute value of `G_N` | one empirical scale input |
| Visible charge representations | not derived from motion |
| Non-scalar coframe ancestry | not derived from the old scalar |
| Local state selection | not derived |

This distinction is the exact sense in which the local chain now works
without pretending that the whole field content has already emerged.

## 2. Coframe source and spin Ward identity

Before imposing the Levi--Civita relation, a visible matter variation can be
written schematically as

```text
delta S_visible
 =-int e[
   T_a^m delta e^a_m
  +(1/2)S^m_ab delta omega_m^ab
  +J^m delta A_m
  -sum_i E_i delta Phi_i
 ].
```

When `omega=omega_LC[e]`, the connection variation is not an independent
hypermomentum equation. Local Lorentz invariance gives

```text
T_[ab]+(1/2)nabla_m S^m_ab=0.
```

The connection contribution therefore supplies the standard Belinfante
improvement and the metric/coframe source is symmetric. Fermion spin has not
been thrown away; it is included in the Hilbert source.

At the identity coframe, the machine Jacobian for

```text
delta g_mn
 =eta_ab(delta e^a_m e^b_n+e^a_m delta e^b_n)
```

is a `10 x 16` matrix of rank ten. The six explicitly constructed
antisymmetric Lorentz generators span its entire nullspace. This is the
source-completeness witness.

## 3. Diffeomorphism and electromagnetic exchange

An infinitesimal diffeomorphism and gauge transformation yield the off-shell
identities

```text
nabla_m T_visible^m_n
 -F_nm J^m
 -sum_i E_i nabla_n Phi_i
 =0,

nabla_m J^m
 =sum_i q_i E_i Phi_i.
```

On the charged-matter equations, these reduce to the exchange equations used
above. The Maxwell stress carries exactly the opposite force density, so the
total coframe source obeys the Bianchi identity.

The CFF term exchanges momentum with curvature as part of the complete
coframe variation. Its flat limit vanishes. Its physical total coefficient
still requires charged-field/QCD matching and is not silently set equal to
the tiny parent-only value.

## 4. Full PPN gate

The full constant PPN result applies only if all of the following hold in the
local domain:

```text
one metric/coframe pole;
psi=0 and nabla psi=0;
no reflection-odd visible scalar source;
renormalized boundary state rho_0;
no additional local timelike or vector background;
controlled higher derivatives treated as momentum-dependent residuals.
```

Under these conditions the two-derivative equations are exactly the
Einstein equations with one source residue. The preferred-frame parameters
cannot be generated because there is no local preferred tensor. The
nonconservation parameters cannot be generated because the source follows
from one invariant action and its total Ward identity. `xi` cannot be
generated because no preferred-location/Whitehead interaction exists.

If a nonzero state occupation, scalar gradient or additional pole is allowed
locally, this PPN result must be recalculated. The checkpoint does not grant
those sectors a free pass.

## 5. Higher-derivative quarantine

The locked checkpoint-4942 residual vector is retained. On its declared
local branch:

```text
O4 scalar cone shift=0;
O4 tree metric stress at psi=0=0;
Delta gamma_standard=0;
Delta beta_standard=0.
```

The sourced `C3` and parent `CFF` terms produce nonzero higher-gradient
effects with different radial/momentum dependence, not new constant PPN
parameters. Across the five locked benchmark systems,

```text
max |Delta a_C3/a_N|=1.512455748599783e-158,
max |Delta v_CFF,parent/c|=1.1374144856001986e-79.
```

Those numbers refer to the locked parent-only coefficients. They do not
replace the unresolved physical total `c_IR` matching.

## 6. Calibration theorem

Field normalization cannot manufacture a new observable source strength.
Under

```text
A -> lambda A,
e -> e/lambda,
Z_A -> Z_A/lambda^2,
```

the combination `e^2/Z_A` is unchanged. The exact null vector in logarithmic
coordinates is the machine witness of this redundancy.

Similarly, rescaling the graviton variable moves factors between its kinetic
term and source vertex but cancels from exchange. The one physical
gravitational residue is `1/M_R^2`.

Thus:

```text
G_Einstein
 =G_exchange
 =G_Newton
 =G_orbit
 =G_lensing
 =G_wave,
```

and the electromagnetic chain has one independent normalization. This is a
real calibrated-source result, not a declaration that all EFT coefficients
have been predicted.

## 7. Local-state silence theorem

There are three distinct statements:

1. **Algebraic silence:** vacuum-subtracted binary state stress is exactly
   zero at `n=0`.
2. **Local Ward silence:** an open region with `n=0` also has `partial n=0`,
   so the state source and its divergence vanish.
3. **Dynamic selection:** the parent evolution chooses that vacuum state in
   every local high-density arena.

The first two are proved. The third is open. A finite logistic profile proves
only asymptotic suppression and cannot be relabelled exact silence.

This is why the local and collective routes must remain state-separated
until a preparation theorem or a quantitative local occupation bound is
derived.

## 8. What is now missing

The leading local source mechanics is no longer the ambiguous part. The
remaining fundamental bridge is field-content ancestry:

```text
Can the non-scalar coframe be derived from a minimal MTS time/space
relational multiplet without introducing extra propagating ghosts or a
preferred frame?
```

Checkpoint 5188 proved that one scalar clock cannot do it; its pullback has
rank one. Checkpoint 5189 proved that the surviving motion scalar maps to a
clock/matter degree of freedom but not the spatial coframe.

The next calculation should therefore construct and test the smallest
non-scalar ancestry candidate—four relational clock/rod fields plus the
minimal internal distortion—or reject it and state plainly that the coframe
is fundamental MTS field content. It must check:

```text
rank and invertibility;
Diff and local-Lorentz gauge identities;
constraint count and two tensor modes;
absence of Boulware--Deser/vector/scalar ghosts;
recovery of the source-complete parent above;
whether the old motion variable enters as clock, matter or distortion.
```

That is the shortest honest route from the original intuitive
motion/time/space language to the now-working local GR spine.

## 9. Claim boundary

Derived or executed here:

```text
rank-ten coframe source map and six Lorentz null directions;
spin-improved symmetric Hilbert source;
Diff/local-Lorentz/U1 Ward chain;
symbolic linear Einstein tensor;
Poisson and Newton normalization relation;
isotropic Schwarzschild beta and gamma;
full ten-parameter constant PPN vector on the local-vacuum branch;
symbolic Maxwell invariant, energy, trace and Poynting vector;
rank-one gravity and rank-one EM calibration blocks;
rank-one universal species source nullspace;
numerical M_R from the one calibrated G_N;
binary local-state silence and finite-logistic obstruction;
higher-derivative residual quarantine.
```

Not derived or not claimed:

```text
absolute numerical G_N from dimensionless MTS data;
physical total c_IR;
visible U1 charge representations from motion;
dynamic selection of the local CTP vacuum;
non-scalar coframe from old one-scalar MTS;
all-operator strong-field GR;
full MTS unification.
```

## 10. Reproduction and files

Executable:

```text
scripts/Y5_R2FR_5201_source_complete_coframe_PPN_local_silence_gate.py
```

Generated evidence:

```text
source-intake/functional_rg/5201/
  coframe_matter_variation_and_Ward_chain.csv
  linearized_Einstein_Newton_symbolic_reduction.csv
  full_PPN_residual_vector.csv
  Maxwell_stress_Poynting_symbolic_reduction.csv
  source_residue_calibration_sensitivity.csv
  species_universality_nullspace.csv
  GN_scale_calibration_contract.csv
  boundary_state_local_silence_gate.csv
  higher_derivative_local_residual_quarantine.csv
  route_decision.csv
  source_provenance.csv
  source_complete_coframe_PPN_local_silence_results.json
```

Validation:

```text
source-intake/mts_residuals/P8_Y5_BRR545_5201_VALIDATION.csv
```

The protected `formalization-workbench`, checkpoint-5200 output tree, public
worktree and read-only galaxy repository are locked during execution. This
checkpoint performs no GitHub action.
