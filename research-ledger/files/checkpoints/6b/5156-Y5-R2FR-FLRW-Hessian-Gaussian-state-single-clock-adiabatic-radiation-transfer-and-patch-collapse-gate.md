# 5156 - FLRW Hessian, Gaussian-state theorem, single-clock adiabatic branch, radiation transfer and patch collapse gate

Marker: `MTS_5156_FLRW_COVARIANCE_ADIABATIC_TRANSFER_COLLAPSE_GATE`.

Date: `2026-07-20`.

## Decision

This checkpoint applies the machine-cog criterion before attempting nonlinear
formation. The same checkpoint-4947 Einstein metric and Hilbert source are
retained. On spatially flat FLRW, `C_mnrs=0`, so the retained
`u_O4 C^2 (nabla psi)^2` portal drops out of the homogeneous quadratic
operator. The motion sector is therefore the ordinary massive scalar coupled
to the same Einstein constraints. Maxwell energy and Poynting momentum remain
inside the same source; no galaxy-only coupling or arena switch is added.

The key theorem is now exact. The Hessian determines mode functions and the
spectral commutator, but it does **not** determine the statistical covariance.
Reflection-evenness removes odd scalar charge while leaving an infinite cone
of positive Gaussian two-point states. A parent cosmogenesis density matrix or
boundary law is required to predict the primordial amplitude, tilt and any
motion isocurvature.

Rather than stop at that theorem, one global source-backed adiabatic covariance
is executed as an explicit nonclaim comparator. CAMB supplies the standard
photon, baryon, neutrino and metric baseline; the Hu--Barkana--Gruzinov full
radiation-era FDM transfer is applied at all three locked masses. Every one of
the 1050 checkpoint-5155 Lagrangian patches is then integrated against the
resulting linear power spectrum.

## 1. Parent FLRW reduction

The checkpoint-4949 inverse scalar operator is

```text
D=-1/sqrt(-g) partial_m[sqrt(-g) A g^mn partial_n]+m_gap^2,
A=Z_psi+2u_O4 C_mnrs C^mnrs.
```

Spatially flat FLRW is conformally flat, hence

```text
C_mnrs[g_FLRW]=0,
A_FLRW=Z_psi.
```

With `v=a sqrt(Z_psi) delta psi`, the free canonical mode satisfies

```text
v_k''+[k^2+a^2 m_gap^2-a''/a]v_k=metric-constraint source.
```

During exact radiation domination `a''=0`. After coherent oscillations, the
same mode has the sourced WKB fluid sound speed

```text
c_X^2=[k^2/(4m_gap^2 a^2)]/[1+k^2/(4m_gap^2 a^2)].
```

The actual infrared `c_ess` remains unsigned. It is not inserted here.

## 2. Exact action-versus-state theorem

For a normalized mode basis `u_k`, canonical quantization fixes

```text
u_k partial_eta(u_k*) - partial_eta(u_k) u_k* = i.
```

A homogeneous Gaussian statistical correlator still contains independent
occupation and squeezing data:

```text
F_k(eta,eta')=(n_k+1/2)[u_k(eta)u_k*(eta')+c.c.]
              +c_k u_k(eta)u_k(eta')
              +c_k* u_k*(eta)u_k*(eta'),
n_k>=0,
|c_k|^2<=n_k(n_k+1).
```

Therefore the same quadratic action admits infinitely many positive
covariances. The reflection-even `+/-psi_i` mixture sets odd moments to zero
but does not select `n_k`, `c_k` or `P_delta(k)`. This proves why checkpoint
5155's homogeneous state cannot be upgraded to a formation spectrum by
notation.

For scalar cosmological modes the invariant initial covariance is a positive
matrix over curvature and relative entropy,

```text
C(k)=[[P_R,P_RS],[P_RS,P_S]].
```

The current parent transfer equations do not uniquely fix this matrix.

## 3. Minimal single-clock branch

If all components descend from one physical clock perturbation, then

```text
delta rho_i/rho_i' = delta rho_j/rho_j',
S_Xgamma=delta_X-3 delta_gamma/4=0
```

after the motion field oscillates. Before oscillation `w_X` approaches `-1`,
and the sourced adiabatic mode has `delta_X=u_X=0` at leading superhorizon
order. This is the standard continuation derived for an ultralight scalar and
matches the checkpoint-5152 frozen background.

This branch is economical and global, but the current corpus has not yet
derived the single-clock cosmogenesis premise. Independent `P_S` and `P_RS`
remain allowed and are not silently set to zero as an MTS prediction.

## 4. Source-backed radiation transfer

The empirical comparator uses

```text
H0=67.4 km/s/Mpc,
Omega_m=0.315,
Omega_b=0.04924319136384048,
n_s=0.965,
sigma8=0.811.
```

CAMB `1.6.6` produces the full adiabatic
CDM baseline and is rescaled linearly from raw
`sigma8=0.8116235383321065` to the declared Planck value.
The independent top-hat reconstruction gives
`sigma8=0.8111011134172839`.

For each parent mass the full FDM transfer is

```text
P_X(k)=T_F(k)^2 P_CDM(k),
T_F=cos(x^3)/(1+x^8),
x=1.61 m_22^(1/18) k/k_J,eq.
```

The parent equality Jeans scales agree with the published
`9 sqrt(m_22) Mpc^-1` expression to at most
`0.004286361599371125`. Numerical and published
half-power scales agree to at most
`0.0230802577585294`.

This is a source-backed full-radiation transfer comparator, not a claim that
MTS derived the observed primordial covariance and not an independent
AxionCAMB likelihood.

## 5. Lagrangian patch result

- `ten_times_WKB_floor`: k_half=20.2979 Mpc^-1, minimum patch sigma=1.95443, maximum peak height=0.862654, five-sigma rows=350/350.
- `benchmark_1e_minus20_eV`: k_half=35.646 Mpc^-1, minimum patch sigma=1.95444, maximum peak height=0.862653, five-sigma rows=350/350.
- `benchmark_1e_minus18_eV`: k_half=275.994 Mpc^-1, minimum patch sigma=1.95444, maximum peak height=0.862653, five-sigma rows=350/350.

Across all rows, the smallest `sigma_MTS/sigma_CDM` is
`0.9989974535695083` and the largest peak height is
`0.8626535205330361`. Exactly
`1050/1050` rows are
within five sigma by `z=0` under the one empirical covariance. The maximum
high-k truncation change in patch sigma is
`1.3760432865383976e-06`.

This answers only whether the required mass patches are erased or rendered
implausibly rare by the linear wave transfer. It does not prove that nonlinear
evolution selects the checkpoint-5154 `p=2` edge, the parent projective `q`, a
finite core, or the required rotation/lensing stress.

## 6. Exact status and next calculation

```text
same parent FLRW quadratic operator                    = derived;
Weyl portal on FLRW background                         = exact zero;
Hessian fixes spectral mode evolution                  = derived;
Hessian uniquely fixes statistical covariance          = rejected exactly;
reflection-evenness fixes primordial power              = rejected exactly;
single-clock adiabatic branch                          = exact conditional;
source-backed radiation transfer                       = executed;
all 1050 Lagrangian patch variances                     = executed;
parent prediction of A_s, n_s and isocurvature          = open;
nonlinear projective-profile attractor                  = open.
```

The next formation calculation may now use one frozen global empirical
covariance, rather than arbitrary numerical noise, to seed a Vlasov
cosmological volume with wave-resolved zoom/core regions. In parallel, the
theory derivation must construct the missing parent state-preparation law: a
single physical clock or another density-matrix principle that predicts
`P_R`, `P_S` and `P_RS`. Neither task may add per-galaxy initial amplitudes.

## 7. Primary sources

- Ma and Bertschinger: https://arxiv.org/abs/astro-ph/9506072
- Hu, Barkana and Gruzinov: https://arxiv.org/abs/astro-ph/0003365
- Perrotta and Baccigalupi: https://arxiv.org/abs/astro-ph/9811156
- Hlozek, Grin, Marsh and Ferreira: https://arxiv.org/abs/1410.2896
- Planck 2018 cosmological parameters: https://arxiv.org/abs/1807.06209
- CAMB: https://arxiv.org/abs/astro-ph/9911177

All downloaded source archives, extracted TeX and hashes are recorded under
`source-intake/functional_rg/5156/sources` and `source_provenance.csv`.

All `26` validation checks pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
