# 5211 - Selected-Trajectory Exact GR-Maxwell Consistent Truncation, Universal Source and Matched GR+SM Excess Theorem

Date: `2026-07-24`

Formal marker: `MTS_5211_SELECTED_LOCAL_GR_MATCHED_GRSM_BASELINE_THEOREM`.

## Executive result

This checkpoint produces a real promotion rather than another missing-input
ledger.

On the source-selected checkpoint-5208 trajectory,

```text
F_R(chi)=M_R^2;
Z_chi=1;
V(chi)=m_gap^2 chi^2/2;
P=P_ge2(X_chi);
delta S_visible/delta chi=0.
```

The restriction

```text
chi=0;
nabla_mu chi=0;
rho_local=rho_0
```

is an exact classical consistent truncation of the bulk equations.  The
motion equation evaluates to `0`, its
stress evaluates to `0`, and all
linear metric-motion, photon-motion and matter-motion cross blocks vanish.
After retaining only the two-derivative terms, the restricted nonlinear
action is exactly

```text
Gamma_2der =
 integral d4x e [
   M_R^2 (R-2 Lambda_cal)/2
  -F_mu_nu F^mu_nu/4
 ] + S_visible[e,omega_LC[e],A,Phi_SM].
```

Therefore the selected MTS parent contains an **exact nonlinear
GR + Lambda + Standard Model + Maxwell two-derivative branch**.  This is
stronger than merely recovering a fitted inverse-square force or matching
two weak-field coefficients.

The statement has two explicit boundaries:

1. `rho_local=rho_0` is an allowed, exactly silent state/preparation
   condition, not a parent-derived attractor;
2. `C3`, `CFF`, nonlocal logarithms and `p8+` operators are not erased.

Accordingly this is not an all-operator local-GR theorem and not a full-MTS
claim.

## 1. Exact consistent-truncation proof

The selected motion equation has the factorized form

```text
E_chi =
 nabla_mu [
  (1-2 P_X+2 u_O4 C^2) nabla^mu chi
 ] - m_gap^2 chi.
```

Checkpoint 5208 fixes the curvature function to a constant rather than just
requiring a double zero.  Fixed-metric visible factorization removes direct
matter and Maxwell sources.  Every term in `E_chi` therefore contains
`chi`, `nabla chi`, or a derivative thereof.  The zero-field substitution is
valid for arbitrary retained metric, electromagnetic and visible-matter
configurations.

The machine checks give

```text
P(0)     = 0;
P_X(0)   = 0;
V(0)     = 0;
V'(0)    = 0;
E_chi|0  = 0;
T_chi|0  = 0.
```

The `O4=C^2 X_chi` term may change the scalar Hessian through
`2*C_squared*u_O4 + 1`, but it cannot create a
zero-branch tadpole or stress.  Stationarity and stability are therefore
kept logically separate.

## 2. Universal source and Newtonian mechanics

The one-coframe variation defines one Hilbert source.  Local Lorentz,
diffeomorphism and visible-`U(1)` Ward identities then fix the stress
symmetry, energy-momentum exchange and current conservation.

For five source classes, the executed soft/Bianchi constraint matrix has

```text
rank    = 4;
nullity = 1;
kernel  = [[1, 1, 1, 1, 1]].
```

Thus species-dependent leading gravitational weights are absent.  The one
conserved-source pole is

```text
Gamma_12 =
 i/[M_R^2(q^2+i0)]
 [T1_mu_nu T2^mu_nu - T1 T2/2].
```

With `G_N=1/(8 pi M_R^2)`, its static slow-source limit is

```text
nabla^2 Phi = 4 pi G_N rho;
Phi = -G_N M/r;
d^2 x/dt^2 = -grad Phi.
```

Neutral, null and charged worldline variations then give the geodesic,
lensing and Lorentz-force equations with the same metric and no
arena-specific source calibration.

## 3. Full two-derivative PPN vector

Transporting the checkpoint-5201 calculation onto the checkpoint-5208
trajectory and the one frozen checkpoint-5210 vacuum datum gives

```text
(gamma,beta,xi,alpha_1,alpha_2,alpha_3,zeta_1,zeta_2,zeta_3,zeta_4)=(1,1,0,0,0,0,0,0,0,0).
```

All `10` standard PPN deltas are exactly zero at
two-derivative order.  The common `Lambda_cal` background and
higher-gradient EFT residuals are reported separately rather than being
mislabelled as constant PPN coefficients.

## 4. Maxwell stress and the Poynting vector

The restricted action gives

```text
nabla_mu F^mu_nu = J_nu;
nabla_[mu F_nu_rho] = 0;

T_EM^mu_nu =
 F^mu_alpha F^(nu alpha)
 -g^mu_nu F_alpha_beta F^(alpha beta)/4.
```

The exact machine reduction gives

```text
T_EM^00 = (E^2+B^2)/2;
T_EM^0i = (E cross B)^i;
T_EM^mu_mu = 0.
```

On the Maxwell and matter equations,

```text
nabla_mu T_EM^mu_nu      = -F_nu_mu J^mu;
nabla_mu T_visible^mu_nu = +F_nu_mu J^mu.
```

The electromagnetic energy flux is therefore part of the same universal
Hilbert source.  It is not an extra phenomenological coupling.  The parent
`CFF` correction remains explicit at higher derivative order.

## 5. Fair matched GR+SM comparison

The relevant comparator is not bare classical GR.  Define both EFTs at the
same subtraction scale and scheme, with common

```text
G_N, Lambda_cal, alpha_EM, SM masses/couplings,
and the ordinary GR+SM Wilson coefficients.
```

Then

```text
Delta Gamma_MTS = Gamma_MTS - Gamma_GR+SM
```

contains only MTS-specific excess.  In particular:

- electron, muon, tau, electroweak and QCD photon-curvature thresholds are
  common visible-sector physics and cancel from the comparison;
- standard graviton/ghost loops are common;
- the extra real motion-scalar logarithm remains;
- parent-specific `C3`, `CFF`, `O4`, and `p8+` pieces remain according to
  their actual branch projection.

This does not make an unknown coefficient vanish.  It prevents standard
GR+SM corrections from being unfairly counted as MTS failures.

## 6. Calculated MTS-specific residuals

For one additional minimally coupled real scalar and `q >> m_gap`,

```text
epsilon_0 =
 ln(Mbar_Pl/q) q^2 /
 [96 pi^2 Mbar_Pl^2];

epsilon_2 =
 ln(Mbar_Pl/q) q^2 /
 [480 pi^2 Mbar_Pl^2].
```

The largest value in the locked local arena set is

```text
max |epsilon_scalar| =
 3.0468810931026259e-40.
```

The largest omitted mass-control ratio is

```text
max m_gap^2/q^2 =
 2.9428756307569549e-12.
```

For the locked parent `CFF` endpoint,

```text
c_parent =
 7.9226386878224367e-72 m^2;

c_parent/|c_visible_control| =
 8.2341145465117803e-42;

max local |Delta v_pol/c|_parent =
 1.1374144856001986e-79.
```

The common visible coefficient is roughly forty-one orders larger, but it
belongs to both GR+SM and MTS.  The displayed `C3` residuals are retained as
endpoint smoke values only: checkpoint 4971 proves that the absolute
physical on-shell `C3` anchor cannot be obtained from local running alone.

## 7. Compact-source branch

The ordinary-matter junction theorem gives

```text
Q_chi=0;
a_chi/a_Newton=0
```

at classical one-scalar order.  Across the locked Earth, Sun, white-dwarf
and neutron-star density corridor,

```text
max |Delta c_chi^2| =
 1.8116002546570096e-17;

max |Delta m_eff^2/m_gap^2| =
 7.7640010913900558e-18.
```

This establishes branch existence and stability in the tested corridor. It
does not replace all-equation-of-state sensitivities, binary radiation or
horizon-state calculations.

## 8. Exact result and remaining obstruction

The project can now state privately and precisely:

```text
exact selected bulk chi=0 branch                 = yes;
exact nonlinear two-derivative GR+Lambda         = yes;
one universal Hilbert source                     = yes;
Newtonian mechanics from the same residue        = yes;
all ten two-derivative PPN coefficients          = GR;
Maxwell Hilbert stress and Poynting flux         = exact;
direct classical one-scalar fifth force          = zero;
one frozen Lambda_cal without arena retuning     = yes;
universal extra-scalar nonlocal residual         = calculated;
parent CFF/C3 endpoint smoke residuals            = separated;
local state attractor/preparation theorem        = open;
physical absolute C3 amplitude anchor            = open;
complete MTS-specific p8+ matched excess         = open;
all-operator local GR                            = not claimed;
full MTS unification                             = not claimed.
```

The next derivation target is no longer source coupling, Newton, PPN, or
the classical Poynting vector.  It is:

```text
DERIVE_FIRST_CANONICAL_MTS_SPECIFIC_P8_ONSHELL_COEFFICIENT
FROM_THE_FULL_PARENT_HESSIAN_OR_BOUND_ITS_MATCHED_EXCESS.
```

Checkpoint 4971 already supplies the exact two-scale/helicity rank
contract.  The next calculation must supply a parent amplitude coefficient,
not another inventory of the missing object.

## Reproducibility

Run:

```text
post-checkpoint-work/.venv-score/Scripts/python.exe
post-checkpoint-work/scripts/
Y5_R2FR_5211_selected_local_GR_matched_baseline_gate.py --dry-run

post-checkpoint-work/.venv-score/Scripts/python.exe
post-checkpoint-work/scripts/
Y5_R2FR_5211_selected_local_GR_matched_baseline_gate.py

post-checkpoint-work/.venv-score/Scripts/python.exe
post-checkpoint-work/scripts/
Y5_R2FR_5211_selected_local_GR_matched_baseline_gate.py --validate-saved
```

Evidence CSV digest:

```text
25b894885dc16be11d63cf1a33de77818d925e51c7e86d92f04fb5ea54598942
```

The checkpoint is private.  Every generated row keeps
`valid_for_full_MTS_claim=false` and `claim_allowed=false`.
