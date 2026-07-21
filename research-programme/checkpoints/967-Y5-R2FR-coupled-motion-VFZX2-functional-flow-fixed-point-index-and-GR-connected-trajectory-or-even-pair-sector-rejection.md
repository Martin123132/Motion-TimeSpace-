# 4951 - Coupled `V-F-Z-X2` source theorem, fixed indices and static pair-route decision

Date: 2026-07-13

Status: private analytic, primary-source-acquired, source-executed and
data-reused checkpoint. It advances the 4950 functional target rather than
writing another missing-coefficient ledger. The exact parent result is a
zero-source theorem; the exact local result is a complete `psi=0` Hessian;
the executed result is an infrared running obstruction. Together they reject
the current static even-pair block as the parent origin of the galaxy state.
They do **not** reject the 4947 local GR/Newton/Maxwell branch or all possible
non-equilibrium composite mechanisms.

## 1. Declared functional block

Use the reflection-even local motion truncation

```text
Gamma_k = int sqrt(g) [V_k(psi)-F_k(psi)R+Z_k(psi)X+c_ess,k X^2],
X       = (nabla psi)^2/2,

V = V0 + m2 psi2/2 + lambda4 psi4/24 + ...,
F = F0 + xi psi2/2 + ...,
Z = Z0 + z2 psi2/2 + ....
```

This is the smallest joint block containing the regular potential, the
curvature function, field-dependent wave normalization and the generated
shift-symmetric derivative interaction. It is a truncation, not the final
MTS action.

## 2. Parent-scheme additive-source theorem

At

```text
m2=lambda4=xi=z2=0
```

the scalar action has constant-shift symmetry `psi -> psi+a`; `X` and `X^2`
are invariant. For a regulator constructed from the parent Laplacian and
independent of the scalar zero mode,

```text
delta_a Gamma_k=0
```

implies

```text
delta_a partial_t Gamma_k
 = -1/2 Tr[G_k (delta_a Gamma_k^(2)) G_k partial_t R_k]
 = 0.
```

Therefore the shift-symmetric subspace is exactly RG invariant:

```text
beta_m2|0 = beta_lambda4|0 = beta_xi|0 = beta_z2|0 = 0.
```

Gravity can and does additively source `c_ess X^2`, because this operator
respects the symmetry. That generated interaction cannot break the symmetry
and manufacture `V(psi)` or `F(psi)` field dependence. This statement is
nonperturbative and regulator-scheme local: it requires the declared
shift-preserving parent regulator, not a numerical fixed point imported from
another paper.

The theorem is scoped carefully. The physical MTS trajectory already has a
relevant mass deformation, so nonlinear terms proportional to that
shift-breaking datum may subsequently generate other coordinates. The
result is that `X^2` is not the missing additive pair source.

## 3. Source-complete fixed-point comparators

Three primary calculations were reconstructed.

### 3.1 Fixed-background universal flow

The curved scalar `V-F-Z` equations give, with
`V=lambda4 psi4/24`, `F=xi psi2/2` and constant `Z=1`,

```text
beta_lambda4 = 3 lambda4^2/(16 pi^2),
beta_xi      = lambda4 (xi-1/6)/(16 pi^2).
```

These are infrared universal terms, not the MTS quantum-gravity fixed-point
equations.

### 3.2 Dynamical physical-gauge comparator

The Percacci-Vacca `d=4` physical-gauge equations were expanded with

```text
v=v0+m2 varphi2/2+lambda4 varphi4/24,
f=f0+xi_pair varphi2/2.
```

The script verifies two exact polynomial fixed points:

```text
FP1: v0=3/(128 pi2), f0=41/(768 pi2), m2=lambda4=xi_pair=0,
FP2: v0=3/(128 pi2), f0=37/(768 pi2), m2=lambda4=0,
     f=f0+varphi2/6, hence F''=1/3.
```

At FP1 the five-coordinate stability eigenvalues are exactly

```text
{-4,-2,-2,0,0},
```

so the pair-breaking quartic/nonminimal block is marginal in this source
projection. The order-one FP2 curvature coefficient is at least
`2.7e6` below the easiest spherical galaxy threshold even under the generous
identification `B=F''=1/3`. It is not inserted into MTS.

### 3.3 Scheme sensitivity

The Narain-Percacci De-Donder GMFP has zero scalar self interactions but a
source-reported `phi2` block with critical exponents
`0.143 +/- 2.879 i`. The physical-gauge comparator instead has marginal
directions. This is direct evidence that the multiplicative `xi` index is
not portable between schemes. The common result is the invariant zero
coordinate, not either numerical index.

## 4. MTS parent indices

The existing source-diagonal MTS potential projection gives on its regular
low branch

```text
A_gravity      = 0.153338955052946,
theta_mass     = 1.846661044947054,
theta_quartic  = -0.153338955052946.
```

Thus the motion gap remains a relevant datum and the regular quartic is
irrelevant. The parent additive `xi` source is exactly zero, but its
multiplicative critical index is not claimed because the required natural
Type-II `F''R` projection has not been calculated. This remaining index does
not change the local onset result below.

## 5. Exact `psi=0` onset operator

Set `psi=epsilon f`. Direct expansion gives

```text
Gamma^(2)[f]
 = 1/2 int sqrt(g)
   [Z0 (nabla f)^2 + (m2-xi R)f^2],

L_pair = -Z0 box + m2-xi R.
Gamma_psi_psi=-Z0 box+m2-xi R.
```

The orders of the remaining coordinates are

```text
lambda4 psi4 = O(epsilon4),
z2 psi2 X    = O(epsilon4),
c_ess X2     = O(epsilon4).
```

Consequently none enters the first bifurcation. A positive quartic or
derivative interaction may stabilize or screen an already nonzero state,
but cannot prevent a local object from crossing the same linear instability
first. Field dependence at nonzero `psi` likewise cannot alter the stability
of the shared `psi=0` branch.

## 6. GR-connected infrared trajectory

Let

```text
delta_xi = xi-1/6,
t        = ln k.
```

The universal stable low-energy equations integrate exactly:

```text
d lambda4/dt       = 3 lambda4^2/(16 pi^2),
d ln|delta_xi|/dt  = lambda4/(16 pi^2),

delta_xi(k2)/delta_xi(k1)
 = [lambda4(k2)/lambda4(k1)]^(1/3).
```

For `lambda4>=0` and `k_galaxy<k_local`, both `lambda4` and
`|delta_xi|` decrease into the infrared. Stable scalar running therefore has
the wrong sign to make the curvature coefficient much larger for galaxies
than for compact local systems.

Using the easiest massless public spherical row, NGC5005,

```text
Bcrit_galaxy = 9.1041088e5,
Bcrit_WD     = 1.9494100e3,
Bcrit_NS     = 2.3870326,

Bgal/BWD > 4.67019e2,
Bgal/BNS > 3.81399e5.
```

If one nevertheless assigns `k=1/L` separately to each system, the required
mean logarithmic exponents are

```text
<d ln B/d ln k> < -0.19479  (white dwarf to NGC5005),
<d ln B/d ln k> < -0.33889  (neutron star to NGC5005).
```

The derived stable flow has a nonnegative exponent and cannot meet either
condition. Four explicit trajectories with local `lambda4` from `0.01` to
`4 pi` suppress `|delta_xi|` by factors `0.9980` to `0.4894` instead of
amplifying it by `467`.

All 700 previously generated galaxy/Compton rows retain an empty spherical
window, and finite mass never lowers the galaxy threshold. The independent
potential-depth proxy remains at least `73.46` times above the white-dwarf
ceiling. The latter is not promoted to a full three-dimensional disk theorem.

## 7. Decision

```text
joint V-F-Z-X2 closure                           = required;
shift-symmetric parent surface                   = proved invariant;
additive m2/lambda4/xi/z2 source at GMFP          = zero;
gravity-generated X2                             = retained;
X2 contribution to psi=0 Hessian                 = zero;
MTS mass direction                               = relevant;
MTS regular quartic direction                    = irrelevant;
parent natural-TypeII xi multiplicative index    = open;
stable IR xi running supplies local/galaxy split = false;
current static VFZX2 galaxy bridge               = rejected as derived route;
full three-dimensional disk no-go                = not claimed;
4947 local GR/Newton/Maxwell branch               = retained;
full MTS galaxy unification                       = false.
```

The route is rejected as the **current claimed parent bridge**, not erased
from the EFT basis. Reopening it would require both a source-derived negative
infrared exponent large enough to satisfy the rows above and a full
axisymmetric spectrum. Neither may be inserted as an environmental scale
choice.

The constructive surviving route is non-equilibrium: the full parent CTP
hierarchy including visible-matter stress fluctuations and the graviton
noise/spectral kernel. Unlike the scalar-only static 4949 truncation, this can
in principle populate pairs through the already present `h psi psi` vertex.
It must be derived and frequency-gated before any occupation or galaxy fit.

Marker: `PPC4161_VFZX2_SHIFT_SOURCE_STATIC_PAIR_DECISION_4951`.

## 8. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4951_coupled_VFZX2_fixed_and_running_gate.py`
- `post-checkpoint-work/source-intake/functional_rg/4951/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4951/coupled_VFZX2_fixed_and_running_gate_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4951/coupled_VFZX2_linear_source_audit.csv`
- `post-checkpoint-work/source-intake/functional_rg/4951/pair_onset_Hessian_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4951/parent_and_source_fixed_point_indices.csv`
- `post-checkpoint-work/source-intake/functional_rg/4951/running_pair_window_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4951/pair_sector_decision.csv`

## Next target

`4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md`

Starting from the unchanged parent action, derive the `h psi psi` vertex,
the visible-matter stress noise kernel, the induced graviton Hadamard/spectral
function and the resulting scalar `Sigma_F`. Require Ward conservation and
spectral support above the pair threshold. Reject the route if a stationary
or slowly rotating galaxy cannot supply the required frequency support.
