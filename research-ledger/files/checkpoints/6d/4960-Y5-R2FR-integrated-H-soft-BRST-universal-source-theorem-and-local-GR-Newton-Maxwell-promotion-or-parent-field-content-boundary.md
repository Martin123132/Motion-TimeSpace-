# 4960 - Integrated-H universal source theorem and local GR/Newton/Maxwell boundary

Date: `2026-07-13`.

Marker: `MTS_4960_INTEGRATED_H_UNIVERSAL_SOURCE_THEOREM`.

Status: private analytic, primary-source-linked and source-executed checkpoint.
This checkpoint resolves the coefficient question left open at 4959. Inside
the selected integrated-`H`, exact-Diff/BRST parent, the leading coupling of
the massless spin-2 pole to matter is not an independently chosen matter
functor coefficient. The `H` source map is invertible, soft-spin-2
consistency leaves one species-coupling direction, Bianchi compatibility
preserves the same direction, and arbitrary graviton normalization cancels
from source exchange. The retained 4947 Einstein-to-Newton-to-Maxwell chain
therefore becomes a theorem of the declared parent rather than a collection
of separately normalized limits.

This does **not** derive the existence of integrated `H`, Diff, the visible
field spectrum or `U(1)` representations from the motion scalar alone. It
does not prove strong-field compact-body equivalence or full MTS.

## 1. Exact parent boundary

The selected route is the 4875 path integral

```text
Z = integral DH Dpsi_r Dpsi_a DX DPhi DA / Vol(Diff)
      exp i[S_0+S_gf+S_gh],

H^munu=sqrt(-g) g^munu.
```

The field/symmetry declarations are

```text
integrated nondegenerate Lorentzian H = parent field data;
Diff/BRST quotient, measure, regulator = parent gauge data;
visible fields and gauge representations = parent field data;
one positive massless spin-2 pole = induced spectral gate;
M_R^2 and Lambda_cal = induced/renormalized IR coefficients.
```

The fixed-background scalar-only composite-graviton route remains rejected
under the Weinberg-Witten premises. The viable route is not advertised as
"GR from one scalar with no additional field or symmetry data."

## 2. `H` contains the complete Hilbert source

In four dimensions,

```text
det(H^munu)=det(g_mn),
sqrt(-g)=sqrt(-det H),
g^munu=H^munu/sqrt(-det H).
```

Writing `s=sqrt(-det H)`, direct variation gives

```text
delta g^munu
 =s^-1[delta H^munu
       -(1/2)H^munu(H^-1)_ab delta H^ab].
```

Consequently,

```text
delta S_matter/delta H^munu
 =-(1/2)[T_mn-(1/2)g_mn T]
 =-(1/2)R4(T)_mn.
```

The ten-component trace-reversal operator has

```text
rank(R4)=10,
det(R4)=-1,
spectrum(R4)={+1 x 9,-1 x 1},
R4^2=I.
```

It therefore loses neither a species nor a trace component. For Maxwell,
`T_EM=0`; in particular the momentum density
`T_EM^0i=(E cross B)^i` passes through the same source map. Thirty-two new
Lorentzian finite-variation trials give maximum relative residuals

```text
determinant identity = 7.31e-16,
metric recovery      = 3.18e-16,
H Jacobian            = 2.49e-10,
source chain          = 1.56e-10.
```

## 3. Soft theorem leaves one coupling direction

For a soft graviton of momentum `q`, the leading amplitude is

```text
M_(n+1)
 =[sum_i eta_i kappa_i
   p_i^mu p_i^nu epsilon_mn/(p_i.q)] M_n+O(q^0).
```

The gauge replacement

```text
epsilon_mn -> epsilon_mn+q_m xi_n+q_n xi_m
```

requires

```text
sum_i eta_i kappa_i p_i^nu=0.
```

Momentum conservation supplies the same equation without `kappa_i`. For
arbitrary external momenta in one positive massless-spin-2 S-matrix sector,

```text
kappa_motion
 =kappa_Higgs
 =kappa_fermion
 =kappa_photon
 =kappa_composite
 =kappa.
```

The execution constructs the complete pair-difference matrix for these five
source classes. It has rank four and nullspace

```text
ker(C_soft)=span{(1,1,1,1,1)}.
```

Thus no material-labelled leading gravitational coefficient survives. This
is Weinberg's soft-spin-2 universality result applied only after the 4875 pole
and gauge gates have closed.

## 4. Bianchi compatibility is a nonlinear cross-check

Suppose an attempted nonlinear source equation assigned weights `c_i`,

```text
M_R^2(G_mn+Lambda g_mn)=sum_i c_i T_i,mn,
nabla_m T_i^mn=Q_i^n,
sum_i Q_i^n=0.
```

The geometric Bianchi identity requires

```text
sum_i c_i Q_i^n=0.
```

On a connected basis of allowed exchange vectors, the corresponding
difference matrix again has rank four and kernel

```text
ker(C_Bianchi)=span{(1,1,1,1,1)}.
```

Bianchi conservation alone does not prove equality between hypothetical
strictly disconnected sectors. Here it is a nonlinear compatibility check;
the soft theorem is the universality proof. Their common kernel is one
dimensional.

## 5. Field normalization cannot hide a second coupling

For `g_mn=eta_mn+a h_mn`, the conserved-source Einstein Hessian, propagator
and source vertex are

```text
Gamma2 =M_R^2 a^2 q^2 K/4,
D_a    =4 K^-1/(M_R^2 a^2 q^2),
V_a    =a/2.
```

The exchange kernel is exactly

```text
V_a^2 D_a=K^-1/(M_R^2 q^2),
d(V_a^2 D_a)/da=0.
```

Changing the graviton coordinate therefore cannot create a second Newton,
lensing, orbital, waveform or matter-source normalization.

## 6. Nonlinear two-derivative completion

The imported primary theorem content is deliberately explicit. Under

1. Lorentz invariance and locality;
2. one positive massless helicity-two pole;
3. exact gauge/Diff consistency;
4. a two-derivative local infrared truncation; and
5. no additional massless pole,

consistent spin-2 self-coupling gives the Einstein interaction structure.
Up to field redefinitions, boundary/topological terms and a cosmological
term, the massless-pole action is

```text
Gamma_IR
 =M_R^2/2 integral sqrt(-g)(R-2Lambda_cal)
  +S_matter[g,Phi,A]
  +Gamma_higher.
```

The relevant primary sources are Weinberg 1964 and 1965 and Deser's explicit
self-coupling construction. Checkpoint 4960 imports this established theorem;
it does not pretend that a finite matrix calculation re-proves every order of
the nonlinear bootstrap.

The important ownership refinement is

```text
which matter fields and representations exist = parent content;
their leading long-range gravitational coefficient = derived universal;
nonminimal local operators = explicit EFT residuals, not extra G values.
```

## 7. One residue reaches Einstein and Newton

Metric variation gives

```text
M_R^2(G_mn+Lambda_cal g_mn)=T_total,mn,
G_N=1/(8 pi M_R^2).
```

The relation between `G_N` and the pole residue is derived; its numerical
value is measured once. Linearizing the same equation gives

```text
Box hbar_mn=-16 pi G_N T_mn.
```

For a static nonrelativistic source,

```text
nabla^2 Phi=4 pi G_N rho,
Phi=-G_N M/r,
d^2x/dt^2=-G_N M rhat/r^2.
```

The point-body action `-m integral ds` gives the geodesic equation and the
same metric controls null rays. On the retained reflection-even `psi=0`
branch,

```text
PPN gamma=1,
PPN beta=1,
Q_psi=0,
a_psi/a_N=0
```

at the declared weak local order. No separate inertial, active, passive,
lensing or orbital gravitational calibration is introduced.

## 8. Maxwell, Lorentz force and Poynting stress

The retained electromagnetic action is

```text
S_EM
 =integral sqrt(-g)[-F^2/4+c_IR C_mnrs F^mn F^rs]
  +integral sqrt(-g) A_m J^m.
```

One variation gives

```text
nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n,
nabla_m J^m=0.
```

The charged worldline gives

```text
u.nabla u^m=(q/m)F^m_n u^n.
```

Metric variation of that same action gives

```text
T_EM,mn=F_ma F_n^a-g_mn F^2/4+c_IR H_CFF,mn,
T_EM^0i=(E cross B)^i,
nabla^m(T_EM,mn+T_matter,mn)=0.
```

Therefore propagation, Lorentz force, gravitational sourcing and Poynting
momentum do not receive independently fitted coefficients. `alpha_EM` fixes
the canonical leading normalization once. The physical `c_IR` remains one
higher-derivative matching/calibration problem shared by propagation and
stress.

## 9. Residual quarantine rather than a minimal-coupling axiom

Covariance does not make the minimal matter lift unique. The surviving
counteroperators are handled explicitly:

| class | current local status |
|---|---|
| one-motion-scalar matter source | exact zero on the reflection-even `psi=0` branch |
| curvature-Higgs packet | present but current residue/EFT bound makes it negligible in declared weak local arenas |
| `R^2,C^2` | perturbative contact/heavy-pole class; weak corridor controlled, finite matching open |
| `C^3` | nonzero higher-gradient residual retained; not a constant PPN shift |
| `CFF` | structure derived, coefficient matching/calibration open |
| preferred-flow/disformal terms | absent only on the selected Lorentz-invariant zero-enthalpy state |
| hidden-visible re-entry | tree fixed-`H` zero; selected-vacuum local re-entry quarantined, no global all-orders zero |
| compact-body sensitivities | open |
| visible matter ontology | explicit parent content, not motion-derived |

This is why the result is not circularly called "unique minimal coupling."
The leading **massless-pole residue** is universal; allowed nonminimal EFT
operators retain their own zero, bound or open status.

## 10. Executed result

The source-locked runner checks 17 inputs and imports the complete 4947 pack:

```text
14 source-chain rows,
10 limit gates,
9 calibration rows,
5 no-retuning arena rows.
```

Every imported row passes its declared gate. The five arenas use one `G_N`,
one `alpha_EM`, one `J_gap` and one `c_IR` token and contain no arena-specific
source normalization. All eleven 4960 internal checks pass. Every generated
row remains `valid_for_full_MTS_claim=false`.

## 11. Decision

```text
integrated H and exact Diff/BRST                 = explicit parent data;
strict scalar-only composite graviton            = rejected;
H-to-Hilbert source map                          = exact and invertible;
leading species gravity-coupling vector          = derived rank one;
graviton coordinate normalization                = cancels exactly;
two-derivative nonlinear spin-2 completion        = established theorem under stated premises;
Einstein -> Poisson -> Newton                     = derived in the retained branch;
geodesic and standard weak PPN beta=gamma=1       = derived in the retained branch;
Maxwell -> Lorentz -> stress -> Poynting          = derived structurally;
arena-dependent leading source coefficients       = excluded;
numerical G_N                                     = calibrated once, not predicted;
visible fields and U(1) representations from MTS  = false;
strong compact-body GR                            = open;
full MTS                                          = false.
```

This closes the leading local **source-coupling coefficient** throat. The
remaining conceptual bridge is no longer "find a missing coupling." It is to
derive, or explicitly retain as fundamental, the integrated-`H`/Diff and
visible-field content of the parent while extending the controlled theorem
to compact strong fields and nonvacuum MTS states.

## 12. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4960_integrated_H_universal_source_theorem.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4960_integrated_H_universal_source_theorem_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4960/integrated_H_universal_source_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4960/parent_definition_vs_derived_source_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4960/H_Hilbert_source_invertibility.csv`
- `post-checkpoint-work/source-intake/functional_rg/4960/soft_Bianchi_species_coupling_nullspace.csv`
- `post-checkpoint-work/source-intake/functional_rg/4960/local_limit_chain_and_calibrations.csv`
- `post-checkpoint-work/source-intake/functional_rg/4960/local_residual_quarantine.csv`
- `post-checkpoint-work/source-intake/functional_rg/4960/universal_source_decision.csv`
- `post-checkpoint-work/source-intake/functional_rg/4960/PROVENANCE.md`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4960_VALIDATION.csv`

## Next target

`4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-motion-Hessian-or-explicit-fundamental-field-boundary.md`

Attempt the remaining noncircular bridge directly: construct an independent
tensor-density Hubbard-Stratonovich/collective-field origin whose exact gauge
redundancy survives the measure and regulator and whose motion Hessian induces
the positive `M_R^2` residue. If that cannot be derived without re-entering the
Weinberg-Witten premises, retain `H` and Diff as fundamental parent data and
stop calling their existence emergent. Do not reopen the now-closed universal
coefficient or add another local source normalization.

No GitHub action is authorized.
