# 4961 - Integrated-H origin, induced Einstein residue and explicit parent boundary

Date: `2026-07-13`.

Marker: `MTS_4961_INTEGRATED_H_ORIGIN_AND_INDUCED_EH_BOUNDARY`.

Status: private analytic, corpus-executed and source-locked checkpoint.

Decision: the current fixed-background one-scalar, connected-covariance,
Hubbard-Stratonovich and composite-delta routes do **not** derive an
independent integrated tensor density with exact diffeomorphism redundancy.
The 4956 motion Hessian also cannot do so because it expands around an
inherited gravity Hessian and gravitational coupling. The competitive branch
therefore retains integrated `H` and exact Diff/BRST as explicit fundamental
parent field and symmetry data. A positive induced Einstein contribution is
available, but its total residue and the numerical value of `G_N` remain a
one-time matching/calibration rather than a prediction of the present motion
corpus.

This decision does not invalidate checkpoint 4960. It removes a circular
emergence claim while retaining its weak-local Einstein, Newton, Maxwell and
universal-source theorem inside a now explicit parent boundary. It is not a
no-go against every possible future microscopic tensor-gauge completion of
MTS, and it does not establish strong compact-body GR or full MTS.

## 1. What the supplied primitive corpus actually contains

The executable sweep covers all `43` Markdown files and the one PDF under

```text
core-mts-framework/
quantum-particle-field/
mathematics/
```

It finds four covariance-metric/readout documents, three internal gauge-field
extensions and no document that declares both

```text
an independent symmetric metric/tensor-density/coframe field,
and an exact Diff/BRST quotient acting on that field.
```

The three principal core documents instead declare a scalar motion field,

```text
psi:R^4->R,
```

define a metric readout using a fixed Minkowski scaffold,

```text
g_mn=eta_mn+<partial_m psi partial_n psi>_smooth,
```

then insert an Einstein-Hilbert term and vary the emergent metric as though it
were independent. That last step is not licensed by the printed definition:
if `g` is constrained to be a functional of `psi`, independent metric
variation enlarges the configuration space unless a new parent field and
quotient are declared.

The corpus result is an ownership statement, not an argument from missing
words. It source-locks the explicit fundamental-object declarations and the
metric construction used by the core papers.

## 2. Exact local-rank theorem and the covariance escape

For one local gradient `v_m=partial_m psi`, define

```text
O_mn(v)=v_m v_n.
```

There are ten independent symmetric components but only four gradient
components. The executed `10 x 4` Jacobian has generic rank four, while the
matrix `O_mn` itself has rank one. More generally, any local first-jet map

```text
H_mn=F_mn(psi,partial_0 psi,...,partial_3 psi)
```

has Jacobian rank at most five. It cannot be a locally invertible change of
variables to ten independent metric components.

This does **not** kill the connected-covariance idea. For a regular ensemble
covariance write

```text
C=L L^T.
```

The ten-parameter Cholesky map has a `10 x 10` Jacobian of rank ten around
`C=I`. Thus a genuine multimode state can algebraically span every symmetric
tensor direction. The price is exact and important: those extra directions
belong to a state/two-point kernel and its smoothing data, not to the local
first jet of one scalar. Full tensor rank is therefore possible as a
state-dependent readout, but it does not create an independent gauge field.

## 3. Exact collective-field transform

For a symmetric current vector `J_A` and an invertible kernel `K`, completion
of the square gives the exact auxiliary-field identity, with the usual
Euclidean or oscillatory contour prescription,

```text
exp[i J K J/2]
 =N integral Dchi exp{i[-chi K^-1 chi/2+chi J]}.
```

The script verifies symbolically

```text
-chi K^-1 chi/2+chi J
=-(chi-KJ)K^-1(chi-KJ)/2+J K J/2.
```

This introduces an auxiliary representative of a composite channel. Because
`K^-1` is invertible, it introduces no gauge orbit and no new physical
configuration direction. Integrating `chi` out returns the original theory
exactly.

The alternative exact identity

```text
1=integral DH delta[H-O(psi)]
```

has the same boundary: `H` is supported only on the image of `O`. Removing
the delta constraint and integrating `H` independently changes the theory.
Doing that modulo Diff is precisely the 4875 parent-field upgrade, not a
derivation from the scalar functional.

## 4. Why a regular auxiliary kernel cannot manufacture Diff

At nonzero momentum the linear spin-two gauge map is

```text
R(q): xi_n -> q_m xi_n+q_n xi_m.
```

It has rank four for every nonzero `q`. To see this without relying on a
numerical sample, choose an index `m` with `q_m != 0`. If `R(q)xi=0`, the
`mm` component gives `xi_m=0`; every `mn` component then gives `xi_n=0`.
Consequently an ungauge-fixed Diff Hessian must satisfy

```text
Gamma^(2)(q) R(q)=0,
nullity Gamma^(2)(q)>=4.
```

The execution checks timelike-axis, spacelike-axis, Minkowski-null and generic
momenta; all four `10 x 4` gauge maps have rank four. A regular
Hubbard-Stratonovich inverse kernel has rank ten and nullity zero, so it cannot
obey this Ward identity. An explicit quotient projector,

```text
Gamma_perp=I-R(R^T R)^-1R^T,
```

obeys `Gamma_perp R=0` and has rank six, nullity four and zero determinant.
Using it as `K^-1` makes the ordinary auxiliary identity singular unless a
gauge quotient, gauge fixing and ghost measure are supplied separately.
Those are new parent data.

Tuning a loop polarization so that one eigenvalue of

```text
Gamma(0)=K^-1+Pi(0)
```

vanishes gives `det Gamma(0)=epsilon`; it is an accidental pole displaced by
an arbitrarily small `epsilon`. It neither gives four Ward-aligned null
directions nor a nonlinear Diff identity. A massless pole and a gauge
redundancy are distinct gates.

Under the premises already audited at 4874-4875, retaining the exact
fixed-background composite theory also retains the Weinberg-Witten trigger.
The integrated-`H` Diff parent avoids that trigger because gravitational
energy is not represented by a gauge-invariant local Lorentz-covariant stress
tensor. The evasion comes from the declared gauge field space, not from the
heat-kernel coefficient.

## 5. The reference background does not disappear automatically

The sharpened covariance candidate is

```text
g_hat^mn=g_ref^mn+C^mn,
C^mn=ell_*^2[nabla_x^m nabla_y^n G_H(x,y)]_ren.
```

Primitive background independence requires the split Ward identity

```text
delta Gamma_IR/delta g_ref^mn |_(g_hat,public data)=0.
```

The printed scalar action has explicit `g_ref` dependence. For the ordinary
scalar kinetic term at `g_ref=eta` and the test gradient
`partial_m psi=(2,1,0,0)`, its reference Hilbert stress is

```text
T_mn=
[[5/2,2,0,0],
 [2,5/2,0,0],
 [0,0,3/2,0],
 [0,0,0,3/2]],

rank(T)=4,
sum_mn T_mn^2=25.
```

This is a direct nonzero witness. A compensating split symmetry or exact
dynamical cancellation could still remove the scaffold, but neither is
contained in the primitive action. Simultaneously transforming `g_ref` and
the scalar as tensors proves covariance; it does not prove that `g_ref` is a
gauge-redundant, unobservable split variable.

## 6. The 4956 motion Hessian is not an origin calculation

The hash-locked 4956 metric and mixed blocks are

```text
H_hh=I10+32 pi g K[p M0+x p' M1+x^2 p'' M2],

H_hpsi=sqrt(32 pi g) q K sqrt(x)[p' B1+x p'' B2].
```

Setting `g=0` gives

```text
H_hh=I10,
H_hpsi=0.
```

Moreover, `g*=0.1305603732179711` is imported from the completed 4935
gravity-photon trajectory, whose flow coordinates already include `g` and a
Newton-pole source. The identity metric block, inverse propagator, regulator
normalization and gravity coordinate therefore pre-exist the motion
correction. Removing that inherited block removes the operator whose inverse
defines the 4956 functional trace.

The functional `P(X)` work remains useful: it derives motion backreaction and
a GR-connected trajectory inside a metric theory. It cannot be reused as
evidence that the motion sector generated the metric theory it presupposes.

## 7. Induced Einstein residue and the scale gate

In the proper-time matching convention retained from 4876-4877,

```text
M_R^2=M_0^2+M_loop^2+delta M_threshold^2,

M_loop^2=W1 Lambda_UV^2/(96 pi^2),

W1=S_h+2N_D-4N_V,
S_h=sum_s(1-6 xi_s).
```

A positive induced contribution requires `W1>0`. If the bare and threshold
terms are set to zero only as a diagnostic, matching
`M_R=Mbar_Pl` requires

```text
m_Pl=sqrt(8 pi) Mbar_Pl,
```

and therefore

```text
Lambda_UV/Mbar_Pl=4 pi sqrt(6/W1),
Lambda_UV/m_Pl=sqrt(12 pi/W1),
ell_*/ell_Pl=sqrt(W1/(12 pi)).
```

| branch | `W1` | `Lambda_UV/Mbar_Pl` | `Lambda_UV/m_Pl` | `ell_*/ell_Pl` |
|---|---:|---:|---:|---:|
| one minimal real scalar | `1` | `30.7812` | `6.13996` | `0.162868` |
| one minimal complex scalar | `2` | `21.7656` | `4.34161` | `0.230329` |
| imported SM plus three right-handed neutrinos | `4` | `15.3906` | `3.06998` | `0.325735` |

Conversely, a cutoff equal to the reduced Planck mass needs
`W1=96 pi^2=947.482`; a cutoff equal to the usual Planck mass needs
`W1=12 pi=37.6991`. `W1` is an effective signed weight, not necessarily a
literal species count. For one real scalar alone these targets would require
large negative nonminimal couplings (`xi=-157.747` or `-6.11652`), which the
current corpus does not derive.

The one-scalar row is therefore a formal positive contribution but not a
controlled absolute prediction: it places the matching cutoff above the
resulting Planck scale. Keeping `M_0^2`, thresholds and gravity/ghost matching
only increases the underdetermination. One measured Newton residue constrains
the sum of three coefficient groups; the executed Jacobian has rank one and
nullity two.

The robust result is

```text
G_N=1/(8 pi M_R^2)
```

with one universal measured residue. Neither the covariance scale nor the
old formulas containing `G` may be used to claim a derivation of the value of
`G` itself.

## 8. Architecture selected after the failed origin attempt

The current serious branch is now stated without hidden closure:

```text
fundamental parent data:
  integrated nondegenerate Lorentzian H^mn,
  exact Diff/BRST quotient and compatible measure,
  visible fields and gauge representations;

derived or matched inside that parent:
  public metric g(H),
  one positive massless spin-two pole,
  one universal Hilbert-source coupling direction,
  Einstein nonlinear completion at two derivatives,
  M_R^2 and Lambda_cal as renormalized coefficients,
  motion-sector corrections and higher operators;

not presently derived:
  H and Diff from one motion scalar,
  numerical G_N from microscopic MTS data,
  visible matter ontology,
  strong compact-body equivalence,
  full MTS unification.
```

This is not a retreat to an arbitrary closure. It is the exact boundary
forced by the attempted construction. A future emergence claim must add a
real microscopic tensor-gauge sector whose measure already owns the Ward
identity, positive pole and background-independence map; it cannot obtain
them by renaming the current scalar covariance.

## 9. What remains established

Checkpoint 4960 remains intact inside the explicit parent:

```text
delta S_m/delta H^mn=-(T_mn-g_mn T/2)/2,

ker(C_soft)=span{(1,1,1,1,1)},

M_R^2(G_mn+Lambda g_mn)=T_total,mn,
G_N=(8 pi M_R^2)^-1,
nabla^2 Phi=4 pi G_N rho,

S_EM -> Maxwell -> Lorentz -> T_EM -> Poynting.
```

Thus weak-local GR, Newtonian mechanics and Maxwell stress are not reopened,
and no source-, species- or arena-specific gravitational coefficient is
introduced. Their claim remains conditional on the declared parent and the
selected weak-local state. Strong compact objects are still outside that
proof.

## 10. Next target

The origin fork is decided cleanly enough to stop circling it. Checkpoint
4962 should attack the remaining local-GR boundary that can change observable
physics:

```text
4962-Y5-R2FR-compact-body-sensitivity-binary-flux-and-junction-matching-or-strong-GR-residual-boundary.md
```

The derivation should compute whether the reflection-even motion sector gives
zero compact-body scalar/vector sensitivity, whether the same `M_R` residue
controls conservative binding and radiation, and which higher-curvature or
state coefficients survive neutron-star and binary matching. Failure must
produce explicit sensitivity and flux residuals, not another generic missing
input list.

No GitHub action is authorized.

## 11. Executed evidence

- `post-checkpoint-work/scripts/Y5_R2FR_4961_integrated_H_origin_and_induced_EH_boundary.py`
- `post-checkpoint-work/source-intake/functional_rg/4961/microscopic_tensor_density_candidate_inventory.csv`
- `post-checkpoint-work/source-intake/functional_rg/4961/local_and_ensemble_metric_map_rank_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4961/collective_field_transform_and_Diff_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4961/reference_background_split_Ward_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4961/motion_Hessian_no_bootstrap_audit.csv`
- `post-checkpoint-work/source-intake/functional_rg/4961/induced_EH_residue_scale_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4961/integrated_H_origin_boundary_decision.csv`
- `post-checkpoint-work/source-intake/functional_rg/4961/integrated_H_origin_and_induced_EH_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4961/PROVENANCE.md`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4961_VALIDATION.csv`
