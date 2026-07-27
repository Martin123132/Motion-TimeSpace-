# 4949 - Covariant CTP-2PI occupation, static source and composite-route decision

Marker: `MTS_CTP_2PI_STATIC_SOURCE_OCCUPATION_NO_GO_4949`.

Date: `2026-07-13`.

Status: private analytic, source-executed and data-executed checkpoint. The
reflection-even two-point route selected at 4948 has now been carried through
the actual completed parent rather than left as a generic 2PI possibility.
The physical real-time equations, axisymmetric inverse propagator,
state-dependent stress and local-GR limit are derived. The result is a clean
rejection of the current minimal composite galaxy route: the displayed parent
has a positive, stationary quadratic scalar operator and no scalar CTP
collision/source kernel, so a static baryonic metric does not populate its
vacuum. A nonvacuum correlator is allowed and has conserved stress, but its
occupation is arbitrary initial-state data rather than a prediction. The next
route must derive a reflection-even pair-source/bifurcation operator or a
fully sourced time-dependent formation history; it may not insert an
occupation profile by hand.

## 1. Why the Euclidean contract is insufficient

Checkpoint 4948 used a Euclidean 2PI functional to identify a legitimate
reflection-even composite variable. That is sufficient for an equilibrium
effective action. A persistent physical occupation is instead encoded in the
closed-time-path correlators

```text
F(x,y)=< {psi(x),psi(y)} >/2,

rho(x,y)=i<[psi(x),psi(y)]>.
```

The exact CTP stationarity equation is

```text
G^-1=D^-1-Sigma,

Sigma=2i delta Gamma_2/delta G.
```

Separating statistical and spectral components gives the covariant
Kadanoff-Baym system

```text
D_x rho(x,y)
 =-int_(y0)^(x0) dz Sigma_rho(x,z)rho(z,y),

D_x F(x,y)
 =-int_(t0)^(x0) dz Sigma_rho(x,z)F(z,y)
  +int_(t0)^(y0) dz Sigma_F(x,z)rho(z,y).
```

Unlike the spectral equal-time data fixed by commutators, `F`, its first
time derivative and its mixed second derivative at `t0` must be supplied by
the initial density matrix unless the right-hand kernels dynamically erase
and replace that information. This is why a Euclidean stationary propagator
cannot silently stand for a galaxy occupation.

The primary source is J. Berges, *Introduction to Nonequilibrium Quantum
Field Theory*, `https://arxiv.org/abs/hep-ph/0409233`, especially its exact
2PI action, Dyson equation, Kadanoff-Baym equations and initial-data
discussion.

## 2. Parent-owned inverse propagator

The completed local motion action is

```text
S_psi
 =-1/2 int sqrt(-g)
   [A(x) g^mn nabla_m psi nabla_n psi+m_gap^2 psi^2],

A(x)=Z_psi+2u_O4 C_abcd C^abcd.
```

Therefore the Euclidean inverse propagator is not a guessed galaxy kernel:

```text
D
 =-1/sqrt(g) partial_m[sqrt(g)A g^mn partial_n]+m_gap^2.
```

For a static axisymmetric metric

```text
ds_E^2=N^2 d tau^2
       +gamma_ab dx^a dx^b
       +gamma_phiphi dphi^2,

a,b in {R,z},
```

and modes `exp(i omega tau+i j phi)`, the exact two-dimensional operator is

```text
D_(omega,j)
 =-1/(N sqrt(gamma))
   partial_a[N sqrt(gamma)A gamma^ab partial_b]
  +A omega^2/N^2
  +A j^2 gamma^phiphi
  +m_gap^2.
```

This is the renormalized axisymmetric Dyson problem that the current parent
actually owns. It contains no fitted radial support function.

## 3. Positivity and the static-production theorem

On the selected branch checkpoint 4942 proves `A>0` by an enormous margin,
and the physical gap branch has `m_gap^2>0`. For every regular test function,

```text
<f,Df>
 =int sqrt(g)[A|nabla f|^2+m_gap^2|f|^2]>0.
```

Thus the displayed operator has no zero mode, tachyonic mode or spontaneous
two-point bifurcation. The `O4` portal changes the static eigenfunctions but
does not make the quadratic form unstable.

At fixed mean metric the displayed scalar action is purely quadratic. There
is no cubic or quartic scalar vertex, so

```text
Gamma_2^scalar=0,
Sigma_F^scalar=0,
Sigma_rho^scalar=0.
```

The CTP equations are consequently homogeneous. In the stationary mode basis

```text
psi=sum_alpha[a_alpha u_alpha(x)e^(-i omega_alpha t)+h.c.],

n_alpha=<a_alpha^dagger a_alpha>,
```

every `n_alpha` is a collisionless constant fixed by the initial state. For
the regular stationary vacuum `n_alpha=0`. Because `partial_t D=0`, the
positive-frequency basis does not mix with its negative-frequency conjugate:

```text
beta_(alpha,beta)=0.
```

The static baryonic potential can scatter or distort modes and produce
renormalized vacuum polarization; it cannot create real occupation from the
stationary vacuum. The theorem assumes the weak-field static galaxy branch,
a timelike Killing vector, no horizon or ergoregion, positive `D`, and the
stationary ground state. Time-dependent galaxy assembly is a different CTP
problem and remains open.

Metric exchange does generate scalar-pair vertices in the full parent. A
quantum-complete 2PI system would therefore need the graviton correlator and
mixed kernels, or a derived metric influence functional. That prevents the
scalar-only `Gamma_2=0` result from being mislabelled as the full quantum
parent. It does not rescue a static nonvacuum source: the exact stationary
ground state remains a ground state, and choosing a populated density matrix
remains additional state data.

## 4. State stress and conservation

Separate a real state occupation from vacuum matching in one common
renormalization convention:

```text
Delta F_state=F_state-F_vac[g].
```

The canonical point-split contribution is

```text
Delta T_mn^can
 =Z_psi lim_(y->x)
  [nabla_m nabla_nprime
   -g_mn(g^abprime nabla_a nabla_bprime+m_gap^2/Z_psi)/2]
  Delta F_state(x,y).
```

The curvature-kinetic contribution is retained without an invalid partial
variation:

```text
Delta T_mn^O4
 =-2u_O4/sqrt(-g) delta/delta g^mn
   int sqrt(-g) C^2
   g^abprime nabla_a nabla_bprime Delta F_state(x,y)|_(y->x).
```

Equivalently their sum is the metric variation of the renormalized CTP
functional at stationary `F,rho`. Diffeomorphism invariance then gives

```text
nabla^m(T_matter,mn+Delta T_occ,mn)=0.
```

This closes the conservation contract. It does not choose `Delta F_state`.
For the stationary vacuum,

```text
Delta F_state=0
 -> Delta T_occ=0
 -> checkpoint 4947 GR/Newton/Maxwell branch.
```

The vacuum determinant `Tr ln D/2` is not discarded. Its local terms
renormalize `Lambda`, `G_N`, `a_R` and `a_C`, while any finite nonlocal vacuum
piece is a calculable quantum correction. It belongs in the existing Wilson
matching ledger and cannot be renamed as an adjustable galaxy occupation.

## 5. Public SPARC scale diagnostic

The locked public `MTS-Galaxy-Lab-` sample contains 175 LTG ROTMOD records.
Its outermost row was read without modifying the repository, using the locked

```text
ML_disk=0.5,
ML_bulge=0.7,

V_bar^2=V_gas|V_gas|+0.5V_disk^2+0.7V_bulge^2.
```

There are 173 positive outer residual rows. For a spherical flat-curve scale
diagnostic,

```text
epsilon_req
 =V_X^2 c^2/(4pi G_N R^2).
```

One relativistic quantum of wavelength `R` per correlation volume `R^3` has

```text
epsilon_1=hbar c/R^4.
```

The required occupation per such cell is therefore

```text
N_R
 =epsilon_req/epsilon_1
 =(V_X/c)^2(R/l_P)^2/(4pi).
```

Across the 173 positive rows,

```text
99.0777 <=log10 N_R<=105.2933,

median log10 N_R=102.5108.
```

The gap value whose Compton length equals each outer radius has median

```text
log10 J_gap=-110.6717.
```

These numbers are not a fit and are not advertised as a strict bound on all
vacuum polarization. They expose the physical distinction between a single
quantum correction and the macroscopic high-occupation state required for a
galaxy-scale stress. The current homogeneous CTP equation has no mechanism
that selects an occupation of order `10^99--10^105`.

## 6. Composite-route decision

```text
physical CTP 2PI equations                         = derived;
axisymmetric parent inverse propagator             = derived;
positive static quadratic form                     = proved on branch;
scalar fixed-metric Sigma_F and Sigma_rho           = zero;
static vacuum pair production                      = exact zero;
nonvacuum occupation                               = arbitrary initial data;
variational occupation stress                      = derived;
Ward conservation                                  = derived conditionally;
vacuum-subtracted local-GR recovery                = derived;
public 175-galaxy occupation scaling               = calculated;
source-selected C_n and C_b                        = absent;
current minimal scalar 2PI galaxy route            = rejected;
full metric quantum 2PI hierarchy                  = open;
full MTS galaxy unification                        = false.
```

This is a useful rejection, not another missing-input ledger. The 4948
projective logistic theorem remains valid as mathematics, but the current
minimal parent cannot populate its weights. The next theory move must alter
that fact through a parent-derived even operator, not through a fitted state.

## 7. Next route

The minimal static alternative must preserve `psi->-psi` and the 4943
one-scalar fifth-force zero while allowing a source-owned two-point branch.
The first candidate basis is

```text
-xi_R R psi^2/2,
-xi_T T_matter psi^2/(2M_R^2),
+lambda_4 psi^4/4,
```

or a derived nonlocal CTP influence kernel. None is adopted here. A viable
static bifurcation requires

```text
lowest_eigenvalue(D_environment)<0 in the target galaxy state,
lowest_eigenvalue(D_local)>0 in every local-GR test arena,
lambda_4>0 or an equally explicit stabilizer,
one universal J_gap,
conserved metric stress,
no arena retuning.
```

Next target:
`4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md`.

Derive whether the completed parent RG flow generates the even quadratic and
quartic operators, then calculate the galaxy-versus-local spectral window.
Reject the static pair route if no universal coefficient window exists.

No GitHub action is authorized.
