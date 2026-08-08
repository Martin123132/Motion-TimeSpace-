# 5196 - Invariant mass-gap Hessian and homogeneous-state selection theorem

Marker: `MTS_5196_INVARIANT_MASS_GAP_AND_HOMOGENEOUS_STATE_SELECTION`.

Date: `2026-07-24`.

Status: private analytic, symbolic, source-executed, and branch-executed
checkpoint. No GitHub action.

## 1. Verdict

This checkpoint attacks the finite-mass and homogeneous-state target left by
5195. It corrects one potentially costly ambiguity before doing the
calculation:

```text
J_gap=m_gap^2 G_N
```

is an invariant dimensionless **mass coordinate**. It is not the additive
source in the scalar equation. The current reflection-even parent contains no
such additive source.

The constructive result is:

```text
m_pole^2 = V_eff''(0)/Z_psi,
J_gap    = G_N V_eff''(0)/Z_psi.
```

This relation is invariant under scalar-field rescaling. The parent Hessian
therefore owns the physical meaning and cross-arena universality of the
motion gap.

The fixed-functional calculation nevertheless has a regular relevant mass
eigenoperator. Its trajectory coefficient is free, and the already-derived
GR-separatrix transfer

```text
J_gap,IR=K R_UV+O(R_UV^2)
```

transports rather than selects it.

The homogeneous result is equally exact. Radiation-era regularity removes
the divergent mode and fixes the early velocity in terms of the field
amplitude, but leaves one finite amplitude `A`. A retarded/no-incoming rule
can remove that amplitude only by selecting the zero solution, because the
current additive source is zero.

Thus the unchanged parent gives:

```text
physical pole-mass relation             = derived;
one universal J_gap                     = derived;
numerical J_gap                          = one calibration, not derived;
regular FLRW phase/velocity relation     = derived;
nonzero homogeneous amplitude            = one state datum, not derived;
unique retarded source-selected solution = psi=0.
```

This is not a failure of field theory. Couplings and initial states are
different kinds of input. The gain is that their minimum count and exact
roles are now proved rather than hidden in fitted closure furniture.

## 2. Canonical and coordinate-invariant mass

At the zero-field background, write the quadratic motion action as

```text
Gamma_psi^(2)
 =1/2 int sqrt(-g) psi[
    Z_psi(-Box)+M_psi^2
   ]psi,

M_psi^2=V_eff''(0).
```

The inverse propagator is

```text
K_psipsi(q)=Z_psi q^2+M_psi^2,
```

so the physical pole is

```text
m_pole^2=M_psi^2/Z_psi.
```

Equivalently, with the canonical field

```text
psi_c=sqrt(Z_psi)psi,
```

the canonical potential has

```text
V_c''(0)=V_eff''(0)/Z_psi=m_pole^2.
```

Under `psi'=s psi`,

```text
Z_psi'=Z_psi/s^2,
M_psi'^2=M_psi^2/s^2,
M_psi'^2/Z_psi'=M_psi^2/Z_psi.
```

The symbolic residual generated at 5196 is exactly zero. The unambiguous
universal coordinate is therefore

```text
J_gap=G_N m_pole^2
     =G_N V_eff''(0)/Z_psi.
```

Earlier shorthand `J_gap=m_gap^2G_N` remains correct only when `m_gap`
denotes this canonical pole mass rather than the unnormalized coefficient of
`psi^2`.

There is also a dimensional obstruction to treating `J_gap` as a source. In
four natural spacetime dimensions,

```text
[J_gap]=0,
[delta Gamma/delta psi]=mass^3.
```

An additive source would require a separate dimension-three parent operator.
No such operator is present in the audited action.

## 3. Why the Hessian does not select the number

Checkpoint 4937 derives the regular even potential spectrum

```text
delta beta
 =(-4+A)delta u+varphi delta u'
  -(1/32pi^2)delta u'',

theta_n=4-A-n.
```

For the physical mass direction `n=2`,

```text
theta_mass=2-A
          =1.84666104495 to 1.85881728347 >0.
```

Hence

```text
delta u=C_2 varphi^2
```

is a relevant eigenoperator. The eigenvalue fixes its scaling law; it does
not fix `C_2`.

The gravity-motion stability matrix is block triangular at zero mass. Metric
thresholds rotate the mass eigenvector but do not remove the additional
relevant direction. Checkpoint 4938 then transports its independent UV
coordinate:

```text
J_gap,IR=K R_UV+O(R_UV^2),

K=0.262094420818  for v=+2lambda,
K=0.261707706805  for v=-2lambda.
```

For every sufficiently small positive `R_UV`, this produces a different
positive `J_gap` on the same GR-connected family. That counterfamily is the
exact scale-selection no-go within the current truncation.

## 4. Exhaustion of existing source routes

The action audit was repeated term by term rather than assuming that the
source was absent.

| Existing term or sector | Scalar equation at `psi=0` | Selection result |
|---|---|---|
| `P(X)` kinetic germ | derivative operator only | no mass or amplitude selection |
| `m_pole^2 psi^2/2` | restoring term proportional to `psi` | defines mass, minimum at zero |
| metric-only ordinary matter | `delta S_matter/delta psi=0` | no additive source |
| `O4=C^2X` | zero on flat FLRW because `C=0` | no homogeneous source |
| `C3` and `CFF` | no scalar variation | no source |
| `X^2` | zero quadratic Hessian at `psi=0` | no onset source |
| direct `T_matter psi^2` | not an independent parent operator | unavailable |
| `R psi^2` | current operational parent value `xi=0` | unavailable; multiplicative even if added |
| Gaussian CTP kernel | selects covariance only after a density matrix | action Hessian does not choose it |
| `alpha_4` CTP surface kernel | functional form derived, value state-dependent | no mean-field source |
| free FLRW Bogoliubov production | neutral squeezed pairs with zero mean | not the homogeneous thaw amplitude |

The most plausible apparent escape, a generic nonminimal term, gives

```text
m_eff^2=m_pole^2-xi R.
```

It is still proportional to `psi` in the field equation, so `psi=0` remains
an exact solution for every `xi`. A nonzero state would require a derived
tachyonic crossing plus a derived stabilizing potential and its full
scalar-tensor stress. The current parent owns `xi=0`; inserting a fitted
`xi` or quartic would be an extension, not a derivation.

Moreover, in a single constant-equation-of-state epoch,

```text
R/H^2=0   radiation,
R/H^2=3   matter,
R/H^2=12  de Sitter.
```

A massless curvature term therefore supplies a dimensionless ratio per epoch,
not an absolute Hubble scale. It cannot by itself select finite
`m_gap/H0`.

## 5. Exact homogeneous-state theorem

For the canonical infrared branch define

```text
chi=psi_c/(sqrt(6)M_R),
N=ln a,
h=dlnH/dN.
```

The homogeneous equation is

```text
chi''+(3+h)chi'+(m_gap^2/H^2)chi=S_psi/H^2.
```

The audited parent has

```text
S_psi=0.
```

During radiation domination,

```text
h=-2,
H^2/H0^2=Omega_r e^(-4N).
```

The regular series is

```text
chi
 =A[1-mu^2 e^(4N)/(20 Omega_r)+O(e^(8N))],

chi'
 =-A mu^2 e^(4N)/(5 Omega_r)+O(e^(8N)),

mu=m_gap/H0.
```

The generated symbolic residual vanishes through `O(e^(4N))`. The second
independent early solution is

```text
B e^(-N),
```

which diverges as `N -> -infinity`. Regularity therefore gives

```text
B=0
```

but leaves arbitrary finite `A`.

The same result appears in matter domination:

```text
chi''+(3/2)chi'=0,
chi=A+B e^(-3N/2).
```

Again regularity removes `B` and leaves `A`.

For a general additive source,

```text
L chi=S,
chi=chi_ret[S]+A u_reg+B u_sing.
```

Regularity removes `B`. A separately specified no-incoming homogeneous-mode
condition can set `A=0`. With the current `S=0`, however,

```text
chi_ret[0]=0,
```

so that extra state rule selects only

```text
chi=0.
```

For a constant source the equilibrium would be

```text
psi_star=S_star/m_pole^2.
```

The current value `S_star=0` again gives `psi_star=0`. Therefore no hidden
retarded or equilibrium interpretation of `J_gap` produces the nonzero 5195
state.

This is the precise theorem:

```text
A local second-order reflection-even source-free action plus early regularity
fixes one phase relation but leaves one finite homogeneous amplitude.
```

## 6. Match to the finite 5195 branches

The exact 5195 primary parameters were reloaded and both backgrounds were
rebuilt from the forward `N=-12` regular series.

| Branch | `mu=m_gap/H0` | `m_gap` (eV) | `J_gap` | `chi(-12)` | `chi(0)` | retained |
|---|---:|---:|---:|---:|---:|---:|
| free `Lambda` | `1.2320991247` | `1.77383595e-33` | `2.110929996e-122` | `0.4267395644` | `0.3434943649` | `0.804927393` |
| `Lambda=0` | `0.7638680135` | `1.09566852e-33` | `8.053882512e-123` | `1.1524890880` | `1.0630982295` | `0.922436699` |

The reconstructed masses and `mu` values match the locked 5195 rows to
machine precision.

The corresponding UV trajectory coordinates in the 4938 eigenvector
convention are:

```text
free Lambda:
  R_UV=8.05408e-122 to 8.06598e-122;

Lambda=0:
  R_UV=3.07289e-122 to 3.07743e-122.
```

These are finite and interior. They demonstrate that the parent RG map can
carry the empirical target. They do not turn the target into a fixed-point
prediction.

The field itself retains about `80.5%` and `92.2%` of its regular early
amplitude respectively. Hubble friction has not erased the initial datum.
This is not merely a formal parameter count: the present branch remembers it
numerically.

For each fitted mass the script also constructs four distinct radiation-era
regular rows with amplitude multipliers

```text
0, 0.5, 1, 1.5.
```

All satisfy the same regular velocity relation to displayed order. Only the
unit row additionally imposes the fitted present flatness condition. This is
the explicit regular counterfamily.

## 7. Minimum honest parameter/state contract

The current low-energy theory should distinguish:

```text
G_N:
  one leading gravitational scale calibration;

J_gap:
  one universal essential action parameter calibrated once;

Lambda_cal:
  one background action calibration unless the zero-Lambda branch is chosen;

A_reg or Omega_scalar:
  one global homogeneous state datum, not an action coupling;

theta:
  derived from regularity and not fitted;

primordial covariance:
  separate quantum/statistical state data if perturbations or occupation are
  predicted.
```

For the free-`Lambda` parent, `mu` and the scalar fraction are independent
shape/state coordinates. For the `Lambda=0` branch, flatness fixes the scalar
amplitude after `Omega_m`, `H0`, and the mass are specified. This removes one
independent fit coordinate, explaining why 5195 could compare that branch at
the same count as `wCDM`.

Flatness does not make the amplitude action-derived. It is a conditional
cosmological boundary relation. The distinction matters, but the reduced
parameter count is real.

## 8. What this resolves

The project should stop repeatedly searching for a separate coefficient
called a `J_gap source`. That object does not exist in the current action.

The choices are now finite and explicit:

1. treat `J_gap` as one universal measured constant, just as the current
   parent calibrates `G_N`;
2. retain one global cosmological state datum, or use the economical
   `Lambda=0` plus flatness branch;
3. derive a genuinely new parent state-preparation event if prediction of the
   amplitude is required;
4. enlarge the action only with a complete derived instability/stabilizer
   sector, not a fitted `R psi^2` coefficient.

The first two choices already define a legitimate testable field theory.
They weaken a parameter-free unification claim, not the leading local
GR/Newton/Maxwell derivation.

## 9. Claim boundary

```text
coordinate-invariant pole-mass Hessian          = derived;
field-rescaling invariance                       = exact;
J_gap dimensional/source distinction             = exact;
regular fixed-functional mass relevance          = derived;
finite J_gap selected by current fixed point      = false;
GR-separatrix transport of finite J_gap           = derived;
all current additive scalar-source candidates     = zero or unavailable;
radiation regular phase relation                  = derived;
one regular homogeneous amplitude remains         = proved;
retarded source-free nonzero state                 = false;
5195 finite branches reconstructed                = passed;
Lambda=0 reduced parameter count                  = retained conditionally;
leading local GR/Newton/Maxwell branch             = unchanged;
cosmology-support claim                           = false;
full MTS unification claim                        = false.
```

## 10. Next target

Checkpoint 5197 should enforce the universal-coordinate rule across the
whole theory rather than add another source ledger:

```text
compare the 5195 J_gap interval with every still-live galaxy, formation,
local, and occupied-state use of m_gap;
separate genuinely rejected historical mass rows from live parent
requirements;
prove compatibility, derive a scale-dependent pole from one covariant
operator if allowed, or reject the claim that one canonical scalar mass owns
both branches.
```

No arena-specific mass may be retuned. If the cosmological `~10^-33 eV`
target and any live galactic `~10^-21--10^-20 eV` requirement refer to the
same pole, that is a decisive conflict rather than a notation issue. If the
galaxy response is instead a collective Hessian scale, its relation to
`J_gap` must be derived explicitly.

This cross-arena universal-gap test should precede an official CMB likelihood
because it tests the unification claim itself.

## 11. Machine artifacts

- `scripts/Y5_R2FR_5196_invariant_mass_gap_and_homogeneous_state_selection_theorem.py`
- `source-intake/functional_rg/5196/invariant_mass_gap_Hessian.csv`
- `source-intake/functional_rg/5196/regular_FLRW_mode_and_state_theorem.csv`
- `source-intake/functional_rg/5196/existing_source_operator_exhaustion.csv`
- `source-intake/functional_rg/5196/fitted_5195_mass_and_state_match.csv`
- `source-intake/functional_rg/5196/regular_amplitude_counterfamily.csv`
- `source-intake/functional_rg/5196/curvature_pair_cosmology_gate.csv`
- `source-intake/functional_rg/5196/parameter_and_state_count.csv`
- `source-intake/functional_rg/5196/route_decision.csv`
- `source-intake/functional_rg/5196/source_provenance.csv`
- `source-intake/functional_rg/5196/mass_gap_and_state_selection_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5196_VALIDATION.csv`

Reproduction:

```powershell
& "D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\.venv-score\Scripts\python.exe" -B "D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_5196_invariant_mass_gap_and_homogeneous_state_selection_theorem.py"
```
