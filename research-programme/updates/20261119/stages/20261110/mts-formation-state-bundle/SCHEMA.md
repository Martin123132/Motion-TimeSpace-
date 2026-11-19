# Packet schema and units

Authoritative receipt: result.json plus validation-02.json. Spatial-measure
extension: volume-result.json and VOLUME-MEASURE.md. closeout.json hashes both.

Each ordinary NPZ contains columns (ordered strings), values (rows x columns),
raw_names and raw_values. Columns are explicit; never infer their order from
this prose. Each row is keyed uniquely by (nominal_a,k_Mpc_inverse).
Use numpy.load without allow_pickle.

- early-heavy.npz:1197rows; early-cold.npz:12rows.
- late-heavy.npz and late-cold.npz:1995rows each, matched mode/epoch order.
- paired-late.npz:1995 derived comparison rows, no independent raw bank.
- volume-state.npz:1995 paired spatial-measure rows; columns and values only,
  plus an approximation label. No classical-cold quantum phase is invented.

## Conventions

a, nominal_a and requested_a are dimensionless. a is the native interpolated
actual scale factor; requested_a is the target slice. The slight native
interpolation difference is retained. conformal_time_Mpc and alpha_Mpc are
lengths with c=1; H_conformal_Mpc_inverse, wave number and masses use inverse Mpc.
Phi and Psi are dimensionless Newtonian-gauge metric potentials.
delta_cdm_N/delta_baryon_N are dimensionless physical density contrasts.
theta_cdm_N/theta_baryon_N are velocity divergences, inverse Mpc.

For slow_ and early heavy_ fields, phi is normalized to the reduced Planck
mass. field_N and canonical_q are dimensionless. normal_velocity_N,
canonical_p, canonical_pi and conformal_velocity_background are inverse Mpc.
D_N,P_N,Q_N are the native scaled stress variables, inverse Mpc squared.
They are not SI density/pressure without restoring the declared Planck factors.
field_background and mean_q are background quantities, not random perturbations.

All transfer amplitudes multiply the same retained primordial curvature mode.
curvature_power is the dimensionless power per logarithmic k interval,
A_s(k/.05)^(-.0347). It is NOT a Fourier-box mode variance: the Fourier measure
and volume are still required for a sampled realization. A seed selects a
realization, not a new physical model parameter.

## Exact early chart

heavy_relative_B_real/imag describe delta b/b0 in the explicitly specified
canonical chart. heavy_covariance_rr/ri/ii are the rank-one classical covariance
at fixed k; heavy_anomalous_real/imag retain the complex pairing moment.
This is not a thermal density operator and does not assign each mode a
statistical occupation independently of the others.

## Averaged late chart

heavy_delta_N is physical density contrast; heavy_u_N=theta/k is dimensionless.
heavy_spatial_phase=-am theta/k^2. heavy_relative_NR_real=delta_N/2 and its imag
part is S: these are density/phase coordinates in the leading flat-measure
description. Read the separate spatial-measure correction before using a
coordinate-normalized wave function.

heavy_NR_covariance_ri=power*(delta_N/2)*S, whereas
heavy_density_phase_covariance=power*delta_N*S, differing by a factor of2.
heavy_source_scale=C/a scales the native heavy stress. heavy_comoving_density
is delta_N+3H u_N/k evaluated in its stable synchronous expression.
heavy_comoving_number_per_m3 is the homogeneous NR benchmark normalization.

heavy_pressure_retained and heavy_pressure_NR are dimensionless pressure/rho.
pressure_source_error uses the maximum of the recorded density and velocity
transfer magnitudes. pressure_fractional_difference instead divides by retained
pressure; the two measures must never be substituted for each other.
heavy_pressure_naive_cancellation records the ill-conditioned algebraic
evaluation, while heavy_pressure_stable_reconstruction checks the equivalent
stable expression against native pressure.

leading_frequency_error and horizon_scale_screen are dimensionless diagnostics.
both_scale_screens_pass is0or1, not a formation/galaxy accuracy certificate.
The cold columns use a reference test mass only for a matched comparison band.

## Precision and incompleteness

Rounding columns bound only the indicated float32-buffer contributions.
They are NOT total numerical, interpolation, modelling or observational errors.
Full late native fast phase and the full hidden radiation hierarchy are absent.
The explicit full_hierarchy_restart and exact_late_carrier_phase_supplied
flags remain false. Raw averaged heavy field slots are deliberately zero in
the native diagnostics, not evidence for zero physical wave occupation.

The variance diagnostics use the existing sampled finite band and trapezoidal
integration only. No UV extrapolation, missing multipole fill or nonlinear
realization is included. Old gauge-derivative resolution limitations survive.
