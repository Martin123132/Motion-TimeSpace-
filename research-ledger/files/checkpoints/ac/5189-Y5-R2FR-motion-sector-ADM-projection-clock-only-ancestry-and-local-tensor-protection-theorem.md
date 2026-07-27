# 5189 — Motion-sector ADM projection, clock-only ancestry, and local tensor protection

Marker: `MTS_5189_MOTION_ADM_CLOCK_ONLY_AND_TENSOR_PROTECTION_THEOREM`

**Verdict:** This checkpoint makes a forward structural decision. The
surviving MTS motion scalar maps exactly into the coframe parent as a clock
and matter degree of freedom. It does **not** generate the spatial coframe.
The local `psi=0` branch protects the two GR tensor modes exactly at
quadratic order. A homogeneous cosmological clock is safe in the minimal
`P(X)` block, but the retained `C^2 X` operator is not automatically silent:
its background and first variation vanish on FLRW while its tensor Hessian
does not. The galaxy response therefore remains an occupied-state
susceptibility problem, not a classical scalar-profile problem.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Parent and convention

```text
Gamma_parent=Gamma_EH[e]+Gamma_Maxwell[e,A]+S_visible[e,A,Phi_SM]+int sqrt(-g) P(X,psi)+c_O4 int sqrt(-g) C^2 X+Gamma_contact+Gamma_nonlocal+Gamma_p8plus; X=g^munu nabla_mu psi nabla_nu psi; c_O4 is the signed coefficient actually multiplying C^2 X
```

Signature is `(-,+,+,+)`. The signed coefficient `c_O4` is used because
checkpoint 4935 displayed `+u_O4 C^2 X`, whereas the assembled 5187 action
displayed `-u_O4 C^2 X`. Thus `c_O4=+u_O4` in the former notation and
`c_O4=-u_O4` in the latter. No physical sign is inferred from the alias.

## 2. Exact scalar-to-ADM map

Let `n^mu n_mu=-1`,

```text
nabla_mu psi=-Pi n_mu+s_mu,    n.s=0,
X=-Pi^2+s^2.
```

For the inherited convention

```text
J^mu=2 P_X nabla^mu psi,
T^mu_nu=2 P_X nabla^mu psi nabla_nu psi-delta^mu_nu P,
```

the exact projections are

```text
rho=2 P_X Pi^2+P,
j_i=-2 P_X Pi s_i,
S_ij=2 P_X s_i s_j-P h_ij,
p_iso=(2/3)P_X s^2-P,
pi_ij=2 P_X(s_i s_j-s^2 h_ij/3).
```

The executed anisotropic-stress trace is `0`.
For `s_i=0`, `j_i=pi_ij=0`; a nonzero spatial gradient is anisotropic.
The exact identity

```text
nabla_mu T^mu_nu=(nabla_mu J^mu-P_psi)nabla_nu psi
```

then closes stress conservation on the scalar Euler equation.

## 3. What motion inherits — and what it cannot

If `X<0`,

```text
u_mu=-nabla_mu psi/sqrt(-X).
```

Since `u=f dpsi`, `u wedge du=0` identically. This is a
hypersurface-orthogonal clock congruence, not an independently vortical
spin-one field. Fixing that clock still leaves
`6` independent spatial-metric
directions. Therefore

```text
old scalar motion -> clock/time-flow;
non-scalar E/e     -> spatial geometry;
K_ij=(1/2)L_u h_ij -> motion of already existing space.
```

The 2048 spherical coframe remains useful, but it supplied a separate radial
function `S(r)` and never derived the decisive `T^2 S=1` law. It is a special
construction, not a general scalar origin of the three spatial legs.

## 4. Constraint and mode count

Minimal `P(X,psi)` contains no `dot(N)` or `dot(N^i)`. Diffeomorphism
invariance retains one Hamiltonian and three momentum first-class
constraints. In velocity order
`(dot(N),dot(N^1),dot(N^2),dot(N^3),dot(psi))`, its matter Hessian is

```text
diag(0,0,0,0,
     -2 sqrt(h)[P_X-2 Pi^2 P_XX]/N).
```

The first four null directions are exact; the scalar direction is regular
when `P_X-2 Pi^2 P_XX != 0`. Thus

```text
metric only:       (12-2*4)/2 = 2;
metric plus scalar:(14-2*4)/2 = 3.
```

The full regular two-derivative parent has two tensors plus one scalar. On
the unoccupied local branch below `m_gap`, the scalar pole is unresolved and
the **resolved gravity sector** has two modes. This is decoupling, not a
claim that the scalar was removed from the full field space.

An independently varied unit-flow/aether field instead carries two tensor,
two vector and one scalar gravitational/aether modes. Its finite PPN-safe
corridor remains a correspondence test layer. Exact GR is obtained by
removing that independent field from the local quotient, not by taking its
singular zero-coefficient endpoint.

## 5. Minimal `P(X)` tensor protection

For a homogeneous clock and a trace-free tensor perturbation,

```text
h_ij=a^2 [exp(gamma)]_ij,    tr(gamma)=0,
det(h)=a^6,                  X=-dot(psi)^2/N^2.
```

Therefore `N sqrt(h) P(X,psi)` is independent of `gamma` at all orders.
The executed first and second TT variations are
`0` and
`0`. Dynamic scalar/metric mixing remains in
the scalar constraint sector and vanishes in the static limit found at
5184.

## 6. The `O4=C^2 X` correction that cannot be skipped

FLRW has `Cbar=0`; this kills the background contribution and first
variation. It does **not** kill the second variation. For a flat local TT
wave with plus/cross amplitudes,

```text
C1_abcd C1^abcd
 =(gamma_plus^2+gamma_cross^2)(omega^2-k^2)^2.
```

The executed Weyl identity residual is
`0`. With `q2=omega^2-k^2`, the principal
kernel per polarization pair is

```text
q2*(M_R2 + 4*X*c_O4*q2)/4.
```

It factorizes into the GR massless pole and, if `c_O4 X !=0`, a second pole

```text
q2=-M_R2/(4*X*c_O4).
```

Consequences:

1. `psi=0 -> X=0` protects the local vacuum tensor Hessian exactly.
2. A homogeneous cosmological clock generally activates the `q^4` term.
3. A low-energy order-reduced claim requires
   `epsilon_O4=|4 c_O4 X q2/M_R^2| << 1` over the whole tested band.
4. An exact all-scale two-mode claim requires a parent degeneracy,
   cancellation, or `c_O4 X=0` theorem.

This corrects the tempting but false shortcut “background Weyl is zero, so
the operator has no tensor Hessian.”

## 7. Local, cosmological, and galaxy branches

```text
local psi=0:
  exact quadratic metric/scalar block diagonal;
  O4 pure-metric Hessian zero;
  leading local GR/Newton/Maxwell chain retained.

homogeneous FLRW clock:
  P(X) changes background/scalar dynamics;
  P(X) pure TT Hessian zero;
  O4 tensor EFT gate open.

stationary classical galaxy profile:
  rejected by the healthy P(X) no-lump theorem.

occupied isotropic galaxy state:
  retained as the only current route to the required nonlocal
  common-scalar susceptibility.
```

The same action coefficients must be used in every branch. Arena dependence
may enter through a derived state/boundary preparation law, not by refitting
the parent Wilson coefficients.

## 8. Exact occupied-state target

Use common/slip variables

```text
c=(Phi+Psi)/sqrt(2),    s=(Phi-Psi)/sqrt(2).
```

For `K_eff=K_GR-Sigma`, the 5148 target is

```text
C_q(y)=y^(1+q)/(1+y^q),  y=mu/|k|, q=0.77,
Sigma_cc/K_GR,cc=A C_q/(1+A C_q),
K_eff,cc/K_GR,cc=1/(1+A C_q).
```

For `A>=0` this is positive, monotone and statically stable. The executed
sample gives

```text
min(Sigma_cc/K_GR)=5.364821e-21,
max(Sigma_cc/K_GR)=1.000000e+00,
min(K_eff/K_GR)=1.072475e-13.
```

No-slip for arbitrary ordinary scalar sources requires
`Sigma_cs=Sigma_sc=0` with an invertible slip block. Tensor protection
requires `Pi_TT Sigma Pi_TT=0` or an explicit frequency-dependent bound.
The full CTP kernel must also satisfy its diffeomorphism Ward identity and
retarded/noise positivity.

## 9. A real origin no-go and the remaining constructive target

After the local Einstein residue is matched, a local gapped vacuum
polarization is analytic in `k^2` near zero. The target instead has

```text
C_q~mu/|k|                    (deep infrared),
K_eff/K_GR~|k|/(A mu),
```

so the absolute inverse kernel contains a nonanalytic `|k|^3` term. A
gapped local vacuum loop cannot generate it. The viable origin class is
therefore narrowed to a gapless continuum or an occupied-state retarded
stress spectral density.

The next actual derivation is not another missing-variable ledger. It is:

```text
derive rho_cc(omega,k) from the parent occupied motion state;
prove the Ward identity;
project rho_cs and rho_TT;
recover or reject C_q and its mu law with one cross-arena parameter set.
```

The Poynting vector remains relevant as the universal `T^0i_EM` momentum
source. A stationary Poynting vector is not, by itself, the missing common
scalar susceptibility; any transfer must be derived dynamically in the
same CTP kernel.

## 10. Claim boundary

Established here:

```text
motion-scalar ADM map                 = exact;
clock-only ancestry                   = exact;
six spatial metric directions remain = exact;
EH+P(X) mode count                    = 2 tensor + 1 scalar;
local psi=0 tensor protection         = exact at quadratic order;
homogeneous P(X) TT Hessian           = zero;
O4 TT Hessian on Cbar=0               = nonzero off shell;
O4 low-energy control parameter       = derived;
galaxy common/slip/TT target          = exact;
gapped-vacuum origin                  = rejected under stated assumptions.
```

Not established:

```text
old-scalar derivation of spatial coframe;
numeric or symmetry proof for c_O4 X in cosmology;
occupied-state CTP spectral density;
derived q=0.77 or mu state law;
full MTS unification or galaxy claim;
numerical first-principles G_N.
```

## 11. Machine artifacts

- `source-intake/functional_rg/5189/motion_ancestry_and_field_ownership.csv`
- `source-intake/functional_rg/5189/scalar_ADM_stress_and_current_projection.csv`
- `source-intake/functional_rg/5189/branch_Hessian_irrep_projection.csv`
- `source-intake/functional_rg/5189/O4_TT_principal_symbol_and_EFT_gate.csv`
- `source-intake/functional_rg/5189/ADM_constraint_and_mode_count.csv`
- `source-intake/functional_rg/5189/unit_flow_correspondence_compatibility.csv`
- `source-intake/functional_rg/5189/local_cosmology_galaxy_branch_matrix.csv`
- `source-intake/functional_rg/5189/occupied_state_response_target.csv`
- `source-intake/functional_rg/5189/source_provenance.csv`
- `source-intake/functional_rg/5189/motion_ADM_projection_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5189_VALIDATION.csv`
