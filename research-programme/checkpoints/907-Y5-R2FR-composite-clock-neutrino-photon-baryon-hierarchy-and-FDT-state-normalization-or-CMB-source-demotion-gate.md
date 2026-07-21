# 4891 - Standard species hierarchy, parent response and FDT covariance bound

Marker: `MTS_SPECIES_HIERARCHY_CAMB_FDT_BOUND_4891`

## 0. Decision

The 4890 finite-k parent has now been connected to an operational standard
photon--baryon--neutrino hierarchy instead of leaving “Boltzmann equations”
as a future label. CAMB `1.6.6` supplies the standard collision,
recombination, polarization, massless-neutrino and massive-neutrino
operators. The 4890 parent supplies explicit density, momentum and pressure
slots in the Einstein constraints and contributes no linear anisotropic
stress.

Three parent backgrounds run through the same CAMB engine. Their primary
geometry/spectra shifts are small rather than catastrophic. A separate
parent-versus-matched-GR calculation shows that the new Weyl response is
silent before the late era and reaches at most `1.921%` today on the sampled
grid. Projecting that response through CAMB's Weyl power gives a controlled
low-order CMB-lensing suppression of `0.21--1.24%` over `10<=L<=200`.

The FDT state is not guessed. A one-percent primordial metric-power budget
is converted into a numerical upper bound on its normalized covariance.

This is a real advance, but not an official CMB likelihood or a compiled
custom parent Boltzmann module. The correct decision is

```text
retain the composite-clock cosmology route;
close the standard-species and acoustic-geometry gates;
keep the full line-of-sight and physical bath-state gates open.
```

The 4889 local GR/Newton/Maxwell correspondence is unchanged.

## 1. Exact standard-species interface

Use conformal Newtonian gauge

\[
ds^2=a^2[(1+2\Psi_N)d\eta^2-(1-2\Phi_N)d\mathbf x^2].
\]

The installed CAMB symbolic source was evaluated directly in this gauge.
For photons and massless neutrinos,

\[
\Delta_\gamma'=-kq_\gamma+4\Phi_N',
\qquad
\Delta_\nu'=-kq_\nu+4\Phi_N',
\]

\[
q_\gamma'=\frac{k}{3}\Delta_\gamma
-\frac{2k}{3}\pi_\gamma+\frac{4k}{3}\Psi_N
+\dot\tau\left(\frac43v_b-q_\gamma\right),
\]

\[
q_\nu'=\frac{k}{3}\Delta_\nu
-\frac{2k}{3}\pi_\nu+\frac{4k}{3}\Psi_N.
\]

The baryon and cold-matter equations are

\[
\Delta_c'=-kv_c+3\Phi_N',
\qquad
v_c'=k\Psi_N-\mathcal H v_c,
\]

\[
\Delta_b'=-(1+p_b/\rho_b)(kv_b-3\Phi_N')
+3\mathcal H(p_b/\rho_b-c_b^2)\Delta_b,
\]

\[
v_b'=k\Psi_N-\mathcal H v_b
+\frac{k\rho_bc_b^2\Delta_b
-\rho_\gamma\dot\tau(4v_b/3-q_\gamma)}{\rho_b+p_b}
-\frac{p_b'}{\rho_b+p_b}v_b.
\]

The photon quadrupole and E-polarization quadrupole include the same opacity
and polarization source used by CAMB:

\[
\pi_\gamma'=-\frac{k}{5}(3J_3-2q_\gamma)
-\dot\tau\pi_\gamma+\dot\tau\,\mathcal P,
\]

\[
E_2'=-\frac{k}{3}E_3-\dot\tau E_2+\dot\tau\,\mathcal P.
\]

CAMB's compiled momentum-bin hierarchy owns the massive-neutrino sector.
Both massless and massive neutrino transfer variables are nonzero in the
executed test.

The standard anisotropic stress gives

\[
\boxed{\Phi_N-\Psi_N=\kappa a^2\Pi/k^2}.
\]

The 4890 parent contributes

\[
\delta\rho_{\rm parent}
=3\overline M_{\rm Pl}^2H_0^2(\delta x_X+\delta x_\phi),
\]

\[
-\frac{\delta q_{\rm parent}}{\overline M_{\rm Pl}^2H_0}
=3x_XP_U+(E\phi_N-\bar\sigma)\delta\phi,
\]

and its varied scalar/clock pressure, but

\[
\boxed{\Pi_{\rm parent}=0}
\]

at linear order. Therefore photons and neutrinos continue to own the slip;
no fitted MTS shear or lensing-rescale function has been inserted.

This is the exact algebraic source interface. The current checkpoint runs
the standard hierarchy and parent response in an operator split; compiling
these source replacements inside CAMB remains a stronger future step.

## 2. Parent background mapped without using today's matter density early

The bath receives damping energy. Therefore the matter normalization seen by
the early plasma is

\[
\Omega_{m,{\rm early}}
=\Omega_{o,0}+\Omega_{X,0}s_X,
\]

where `s_X` is the reshot initial clock scale. Subtracting today's
`Omega_m=0.315` at early times would create a spurious negative effective
dark-energy density. The correct values are

| `Omega_memory,0` | `Omega_m,early` | `Delta Omega_m created` | `omega_c` |
|---:|---:|---:|---:|
| `1e-4` | `0.3149991915` | `8.085e-7` | `0.1200823812` |
| `1e-3` | `0.3149654535` | `3.455e-5` | `0.1200670548` |
| `1e-2` | `0.3141106759` | `8.893e-4` | `0.1196787499` |

Define the residual background supplied to CAMB by

\[
\rho_{\rm eff}/\rho_{c0}
=E_{\rm parent}^2-\Omega_r a^{-4}
-\Omega_{m,{\rm early}}a^{-3},
\]

\[
w_{\rm eff}=-1-\frac{1}{3}\frac{d\ln\rho_{\rm eff}}{d\ln a}.
\]

The residual remains positive on all three rays. It crosses `w=-1` by less
than about one percent, so CAMB's PPF object is used only as a background
geometry/standard-hierarchy comparator. PPF perturbations are not relabelled
as the parent perturbations.

The CAMB-to-parent `H(z)` residual is below `4.06e-4` on the sampled
`0<=z<=30` grid; the remainder is dominated by the more detailed CAMB
radiation/neutrino background convention.

## 3. Three-ray acoustic and primary-spectra smoke

Each parent background and its matched-early-density LambdaCDM control were
run with identical

```text
H0=67.4 km/s/Mpc, omega_b=0.02237, tau=0.0544,
A_s=2.1e-9, n_s=0.965, sum m_nu=0.06 eV.
```

No parameter was profiled after seeing the spectra.

| `Omega_memory,0` | `Delta theta*/theta*` | max `|Delta TT/TT|` | max `|Delta EE/EE|` |
|---:|---:|---:|---:|
| `1e-4` | `1.223e-5` | `4.376e-5` | `1.031e-4` |
| `1e-3` | `1.2466e-4` | `4.467e-4` | `1.056e-3` |
| `1e-2` | `6.8326e-4` | `4.423e-3` | `5.836e-3` |

These values cover `2<=ell<=400`. Fractional TE maxima are not interpreted
because TE crosses zero; its robust likelihood treatment belongs in the
future line-of-sight/likelihood step.

This result is materially better than the old empirical `2/27` background's
`~0.47%` acoustic-angle warning. It applies to the newly derived
expansion-source parent, not to that older closure.

No official Planck/ACT/SPT likelihood is run here.

## 4. Recombination and hierarchy health

The executed CAMB hierarchy gives

```text
visibility peak redshift                 1089.1667
opacity at z=30                          8.307e-8
maximum sampled photon quadrupole        0.24417
massless-neutrino transfer               nonzero
massive-neutrino transfer                nonzero
all sampled transfer arrays              finite
```

The tiny opacity at `z=30` supports a controlled late operator split. Before
that matching surface, CAMB owns the complete primary plasma evolution.
After it, baryons and CDM are effectively pressureless while radiation
backreaction rapidly decays.

## 5. Parent-derived Weyl response

For the central `Omega_memory,0=10^-3` branch, define

\[
R_W(k,z)=\frac{\Phi_{\rm parent}(k,z)}
{\Phi_{\rm matched\ GR}(k,z)}.
\]

The numerator and denominator use the same superhorizon seed and
early-matter normalization. Since the parent has no new linear anisotropic
stress, this ratio is the late Weyl response after standard-species slip is
factored out.

Across `k={0.001,0.003,0.01,0.03,0.1} h/Mpc`:

```text
max |R_W-1| for z>=30                    2.666e-7
max |R_W-1| for z<=10                    1.921e-2
max sampled momentum-constraint residual 2.053e-4
```

At `z=0`:

| `k [h/Mpc]` | `R_W-1` |
|---:|---:|
| `0.001` | `-0.001225` |
| `0.003` | `-0.007276` |
| `0.01` | `-0.016575` |
| `0.03` | `-0.018899` |
| `0.1` | `-0.019212` |

Thus the parent is genuinely early-silent and predicts a scale-dependent
late weakening rather than an arbitrary lensing knob.

## 6. First lensing projection

CAMB's linear Weyl power was reweighted by `R_W^2` in the same lowest-order
Limber kernel used by its local post-processing utilities. The result is

| `L` | `Delta C_L^kappa/C_L^kappa` | parent-response kernel coverage |
|---:|---:|---:|
| `10` | `-1.238%` | `99.44%` |
| `20` | `-1.024%` | `99.13%` |
| `40` | `-0.752%` | `98.42%` |
| `60` | `-0.597%` | `97.54%` |
| `80` | `-0.494%` | `96.46%` |
| `100` | `-0.420%` | `95.17%` |
| `150` | `-0.295%` | `90.91%` |
| `200` | `-0.206%` | `85.30%` |

This is a prediction-shaped bounded response, not a lensing likelihood. It
does not include the complete non-Limber low-`L` line of sight, nonlinear
power, or feedback from a compiled parent source module.

## 7. FDT state-normalization bound

Take the baseline primordial curvature power `A_s=2.1e-9`. The matter-era
metric reference is

\[
P_\Phi^{\rm ref}=\frac{9}{25}A_s=7.56\times10^{-10}.
\]

Reserve one percent of that power for the bath noise,

\[
P_\Phi^{\rm noise}\le7.56\times10^{-12}.
\]

Using the four 4890 unit-impulse Green functions at
`k=0.01 h/Mpc`, equal independent impulse variance must obey

\[
\boxed{\operatorname{Var}I_k<2.82438\times10^{-2}},
\]

\[
\boxed{I_{k,{\rm rms}}<0.16806}.
\]

For the normalized Markov map

\[
\operatorname{Var}I_k=2\bar\gamma\Theta_k\Delta N,
\]

and `gamma_bar=1`,

\[
\boxed{\Theta_k\Delta N<1.41219\times10^{-2}}.
\]

This is a bound in the dimensionless `xi/H0^2` Fourier-cell convention of
4890. It is not converted to kelvin or electron-volts because the parent has
not yet derived the comoving spectral cell measure. Doing that conversion
without the measure would be fake precision.

The state decision is now sharp: any proposed KMS/nonthermal bath state must
respect this covariance bound, or the branch fails its one-percent metric
noise budget.

## 8. What is now closed

| requirement | status |
|---|---|
| Photon--baryon collisions/recombination/polarization | Operational CAMB owner |
| Massless and massive neutrino hierarchies | Operational CAMB owner |
| Parent density/momentum/pressure slots | Derived |
| New parent anisotropic stress | Derived zero |
| Three-ray acoustic geometry | Executed |
| Parent late Weyl response | Derived and sampled |
| Low-order lensing projection | Bounded, not full line of sight |
| FDT covariance | Empirically bounded, state not realized |
| Official CMB likelihood | Not run |

Five of eight promotion requirements in the executable arbitration are
closed. The remaining three are not vague: full line-of-sight parent
feedback, a physically normalized bath state, and an official likelihood.

## 9. Next target

`4892-Y5-R2FR-parent-late-ISW-lensing-line-of-sight-and-FDT-state-realization-or-CMB-source-demotion-gate.md`

The next step should compute the non-Limber late ISW/lensing source with the
parent `R_W(k,z)`, attempt a microscopic coherent/vacuum/KMS state whose
spectral covariance satisfies the bound, and only then decide whether an
official fixed-row CMB likelihood is warranted.

## Sources

- `post-checkpoint-work/4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md`.
- `post-checkpoint-work/scripts/Y5_R2FR_4891_species_hierarchy_camb_FDT_bound.py`.
- `post-checkpoint-work/.venv-score/Lib/site-packages/camb/symbolic.py`.
- `post-checkpoint-work/187-CAMB-density-convention-and-locked-transfer-theta-gate.md`.
