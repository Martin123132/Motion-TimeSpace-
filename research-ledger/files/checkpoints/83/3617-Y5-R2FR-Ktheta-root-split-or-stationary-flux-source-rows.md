# 3617 Y5 R2FR: K_theta root split or stationary flux source rows

## Verdict
- The useful derivation route is the polarization-screen operator, not a raw scalar quartic residual.
- `K_theta` is now derived symbolically: it maps the normalized screen spectral split into accumulated polarization rotation.
- This is real progress, but still no claim: the parent action must own the screen perturbation `h_AB`, its energy power `s`, the scale `M_*`, and the amplitude `B_Fresnel_MTS`.

## Why the scalar route is rejected
- A scalar quartic written as `F=u^2+a u+b` has root split `Delta_u=sqrt(a^2-4b)`.
- Near a repeated GR cone, that is not a safe linear bound unless the underlying reciprocal two-polarization operator is supplied.
- So the framework should not pretend that a scalar `B_Fresnel` number alone gives a clean `K_theta`.

## Screen-operator derivation
- Define the physical transverse screen perturbation `h_AB(k,U)=omega^-2 e_A^a delta P_ab(k) e_B^b`.
- Mode shifts: `delta u_pm = -omega^2 lambda_pm(h)/gamma0`.
- Frequency split: `Delta_omega = omega diam_spec(h)/(2 gamma0)`.
- Polarization rotation: `Delta_theta_MTS = integral omega diam_spec(h)/(4 gamma0) dt`.

## Cosmological K_theta
- If `diam_spec(h)<=C_screen B_Fresnel_MTS (k/M_*)^s`, then
- `K_theta(s)=C_screen k0^(s+1) I_s(z)/(4 gamma0 M_*^s H0)`.
- `I_s(z)=int_0^z (1+z')^s dz'/sqrt(Omega_m(1+z')^3+Omega_Lambda)`.
- Into the Wei GRB `xi` convention:
- `K_Fresnel(s)=C_screen M_pl I_s(z)/(4 gamma0 M_*^s k0^(1-s) I_1(z))`.
- Special case `s=1`: `K_Fresnel=C_screen M_pl/(4 gamma0 M_*)`.

## Practical read
- `s=1` is the least awkward route because it shares the same redshift/energy kernel as the acquired GRB bound.
- `s=0` is likely brutally constrained unless the local amplitude is tiny or theorem-zero.
- The next derivation must not choose `s=1` by taste; it has to come from the parent operator dimension or a high-frequency relic/flow mechanism.

## Outputs
- `P8_Y5_R2FR_3617_KTHETA_SCREEN_ROOT_SPLIT_DERIVATION.csv` contains the derivation.
- `P8_Y5_R2FR_3617_GRB_BANDPASS_INTEGRALS.csv` contains the GRB redshift kernels.
- `P8_Y5_R2FR_3617_KTHETA_PROJECTION_RUNNER.csv` contains a blocked-but-ready comparator.
- `P8_Y5_R2FR_3617_HTAU_STATIONARY_SOURCE_ROWS.csv` preserves the backup flux route.

## Next target
- `3618-Y5-R2FR-screen-operator-parent-origin-or-energy-scaling-gate.md`.
- Best route: prove `h_AB=0` from local Hodge/same-metric descent, or derive the nonzero branch's `s`, `M_*`, `gamma0`, `C_screen`, and `B_Fresnel_MTS`.

## Claim status
- `NO_CLAIM`: this checkpoint derives the bridge, not the amplitude.
