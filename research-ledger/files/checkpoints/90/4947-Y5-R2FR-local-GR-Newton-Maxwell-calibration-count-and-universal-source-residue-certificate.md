# 4947 - Local GR/Newton/Maxwell source-residue and calibration-count certificate

Marker: `MTS_LOCAL_GR_NEWTON_MAXWELL_SOURCE_RESIDUE_CALIBRATION_COUNT_4947`.

Date: `2026-07-13`.

Status: private analytic and source-executed checkpoint. The unchanged parent
action now supplies one explicit derivation chain from its massless metric pole
to the Einstein equation, universal graviton exchange, Poisson equation,
Newton force, neutral geodesics, leading light deflection and orbital gravity.
No independent Newton, lensing, orbital or waveform value of `G` is available
to tune. The same exercise closes the structural Maxwell-to-Lorentz-to-stress
chain. It does not predict the numerical values of `G_N`, `J_gap`, the QCD
part of `c_IR`, or the finite `a_R^r,a_C^r` matching sums, and it does not
derive the visible matter functor or `U(1)` representation data from motion
alone.

## 1. Unchanged low-energy parent

On the reflection-even local branch selected at 4942-4943, the relevant action
can be written, through the displayed local EFT order, as

```text
S_loc
 =integral sqrt(-g) [
    M_R^2(R-2Lambda_cal)/2
   -F_mn F^mn/4
   -(nabla psi)^2/2-m_gap^2 psi^2/2
   +a_R^r R^2+a_C^r C^2
   +c_IR C_mnrs F^mn F^rs
   +higher operators]
  +S_matter[g,A,Phi_SM].
```

The declared branch obeys

```text
psi=0,
delta S_matter/delta psi=0,
Q_psi=0.
```

The motion mass coordinate remains physical,

```text
J_gap=m_gap^2 G_N,
```

but it creates no classical one-scalar source residue on this branch. This is
not a statement that `J_gap` is absent from nonlocal, nonvacuum or galactic
motion states.

## 2. Rank-one gravitational source theorem

Metric variation gives

```text
M_R^2(G_mn+Lambda_cal g_mn)=T_total,mn,
G_N=1/(8 pi M_R^2).
```

Inverting the two-derivative Einstein Hessian between conserved sources gives

```text
Gamma_12(q)
 =i/[M_R^2(q^2+i0)]
  [T_1^mn T_2,mn-T_1 T_2/2].
```

Therefore the coefficient of every leading long-range metric exchange is
fixed by

```text
1/M_R^2=8 pi G_N.
```

Changing from the Einstein equation to a force, orbit, clock, null ray or
waveform does not add a coupling. It only changes the source tensor and the
kinematic projection of the same propagator. Equivalently, the leading
gravity source-normalization map has one parent column and hence rank one.
The curvature-squared terms can add derivative-suppressed contact or heavy-
pole structure, but they do not supply a second residue for the massless
`1/q^2` pole.

This proves the equalities represented schematically by

```text
G_Einstein=G_exchange=G_Newton=G_orbit=G_lensing=G_wave
          =G_N
```

inside the declared leading local branch. It does not predict the measured
number `G_N`; one measurement fixes it once.

## 3. Einstein to Newton without a closure

Write

```text
g_mn=eta_mn+h_mn,
hbar_mn=h_mn-eta_mn h/2,
partial^m hbar_mn=0.
```

Ignoring local `Lambda_cal` and higher derivatives at scales where they are
subleading, linearization of the same metric equation gives

```text
Box hbar_mn
 =-2T_mn/M_R^2
 =-16 pi G_N T_mn.
```

For a static nonrelativistic source, `T_00=rho` and the trace reverse gives

```text
nabla^2 hbar_00=-16 pi G_N rho,
h_00=hbar_00/2=-2 Phi/c^2,
nabla^2 Phi=4 pi G_N rho.
```

Using `nabla^2(1/r)=-4 pi delta^3(r)`, an isolated point source has

```text
Phi(r)=-G_N M/r.
```

The slow neutral geodesic then gives

```text
d^2 x/dt^2=-grad Phi
          =-G_N M rhat/r^2.
```

Newton's inverse-square law is consequently a limit of the same parent
residue, not an additional phenomenological motion equation.

## 4. Geodesics, PPN and light

The point-body action inherited from the one-metric matter functor is

```text
S_pp=-m integral ds.
```

Its variation gives

```text
u^a nabla_a u^m=0.
```

Mass cancels from the test-body acceleration. Combined with the 4943 scalar
selection rule, the leading test-body branch has no composition-dependent
metric coefficient and no classical one-scalar fifth force.

The same equation holds for the null eikonal ray. The two-derivative exterior
has the GR values `gamma=beta=1`, so

```text
alpha_lens=4G_N M/(b c^2)+higher-gradient corrections.
```

The 4942 five-system packet independently returns

```text
delta gamma=delta beta=0
```

at standard PPN order. This does not delete the nonstandard `C3` radial
residual or the `CFF` photon correction. Their radial/operator structures are
higher-gradient effects rather than new constant PPN values. Nor does the
test-body proof establish the strong equivalence principle for compact
self-gravitating interiors; that requires sensitivities and radiation/back-
reaction matching.

## 5. Maxwell, Lorentz force and EM stress use one action

With the photon kinetic term canonical, `U(1)` invariance gives

```text
J^m=-(1/sqrt(-g)) delta S_matter/delta A_m,
nabla_m J^m=0.
```

Variation with respect to `A_n` gives

```text
nabla_m F^mn
 -4c_IR nabla_m(C^mnrs F_rs)=J^n,
nabla_[m F_nr]=0.
```

For

```text
S_pp=-m integral ds+q integral A_m dx^m,
```

the worldline equation is

```text
u^a nabla_a u^m=(q/m)F^m_n u^n,
```

whose weak slow limit is

```text
a=-grad Phi+(q/m)(E+v cross B).
```

Metric variation of that same electromagnetic action gives

```text
T_EM,mn
 =F_ma F_n^a-g_mn F^2/4+c_IR H_CFF,mn,

T_EM^0i=(E cross B)^i,

nabla^m(T_EM,mn+T_matter,mn)=0.
```

Consequently there is no independent coefficient for Maxwell sourcing,
Lorentz force, electromagnetic gravitation or the Poynting vector. After a
general photon wave-function factor is removed by `A_c=sqrt(Z_A)A`, only the
renormalized combination `e_c=e/sqrt(Z_A)`, equivalently `alpha_EM`, remains
as the one physical leading electromagnetic normalization. The coefficient
`c_IR` is a distinct higher-derivative Wilson coefficient, but the same
`c_IR` controls propagation and stress.

## 6. Calibration-count theorem

The current displayed gravity-motion-photon truncation contains seven
independent scalar coordinates which are not duplicates:

| coordinate | current role |
|---|---|
| `G_N <-> M_R^2` | one measured massless metric residue |
| `Lambda_cal` | one background-curvature calibration |
| `alpha_EM` | inherited one-time electromagnetic normalization |
| `J_gap=m_gap^2 G_N` | one universal unselected motion scale |
| `c_IR` | one universal photon-curvature coefficient |
| `a_R^r` | one open finite `R^2` matching sum |
| `a_C^r` | one open finite `C^2` matching sum |

Only two of these normalize the leading local source laws: `G_N` and
`alpha_EM`. Four extension coordinates remain unselected or incompletely
matched: `J_gap`, `c_IR`, `a_R^r` and `a_C^r`. `Lambda_cal` is a measured
background datum rather than a local force residue.

The inherited Standard-Model packet `theta_SM` contains many visible-sector
parameters and is not falsely counted as one derived MTS number. Conversely,
body masses and charges are source-state data, not new values of gravitational
or electromagnetic coupling. The conditionally trajectory-derived
`A_C3,W_O4,W_C,parent` coordinates are not fitted per arena.

This count is exact only for the displayed truncation. A general untruncated
EFT has further Wilson coefficients, so no finite full-theory parameter count
is claimed.

## 7. Five-system execution

The source script reconstructs `GM/(rc^2)`, `Phi/c^2`, the Newton surface
acceleration and `12M/r^3` for the unchanged five systems.

| system | `GM/(rc^2)` | Newton `a` (`m/s^2`) | Newton gate |
|---|---:|---:|---|
| Earth | `6.96131e-10` | `9.82030` | pass |
| Sun | `2.12257e-6` | `274.208` | pass |
| one-solar-mass white dwarf | `2.10953e-4` | `2.70850e6` | pass |
| 1.4-solar-mass, 12 km neutron star | `1.72278e-1` | diagnostic only | not weak |
| ten-solar-mass Schwarzschild horizon | `5.00000e-1` | diagnostic only | not weak |

All five rows reuse the same `G_N`, `alpha_EM`, `J_gap` and `c_IR` tokens.
Every CFF curvature factor exactly reproduces the independently generated
4946 transfer table. The neutron-star and horizon rows retain the GR source
chain but are not mislabeled as Newtonian tests.

## 8. Claim boundary

```text
one massless metric residue for GR/Newton/orbits/lensing = derived;
Einstein -> Poisson -> inverse-square force              = derived;
neutral test-body geodesic                               = derived;
standard PPN beta/gamma shift on psi=0 branch            = zero;
classical one-scalar fifth force                         = zero;
Maxwell -> Lorentz -> stress -> Poynting chain            = derived;
arena-dependent source normalizations                    = absent;
numerical G_N predicted from MTS alone                    = false;
J_gap selected without one calibration                   = false;
physical c_IR calculated or calibrated                   = false;
a_R^r and a_C^r complete finite matching                 = false;
strong equivalence principle for compact bodies          = open;
visible U1/matter functor derived from motion alone       = false;
full untruncated EFT parameter count                      = open;
full MTS empirical unification                           = false.
```

This is a real promotion of the local derivation: Newton and Lorentz force are
now outputs of the parent action rather than asserted limits. It is not a
claim that the parent ontology is uniquely derived from motion, time and
space, or that the distinctive large-scale MTS phenomenology has yet been
generated by this same motion Hessian.

## 9. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4947_local_calibration_count_and_source_residues.py`
- `post-checkpoint-work/source-intake/functional_rg/4947/local_calibration_count_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4947/parent_low_energy_calibration_ledger.csv`
- `post-checkpoint-work/source-intake/functional_rg/4947/source_residue_chain.csv`
- `post-checkpoint-work/source-intake/functional_rg/4947/Newton_geodesic_Lorentz_limit_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4947/cross_arena_no_retuning_matrix.csv`

## Next target

`4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md`

Use the completed parent motion Hessian and read-only galaxy equations to test
whether one `J_gap` and one parent state variable derive
`dn/dlnR=q n(1-n)` and `db/dlnR=-s b(1-b)`, including their stress tensor and
boundary conditions. Do not import the galaxy phase flow as a fitted closure
and do not change the galaxy repository during the derivation audit.

No GitHub action is authorized.
