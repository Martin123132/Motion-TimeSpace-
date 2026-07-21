# 5175 - Exact-low-mode-shared isotropic resolution discrimination gate

Marker: `MTS_5175_EXACT_LOW_MODE_SHARED_ISOTROPIC_RESOLUTION_GATE`.

Date: `2026-07-21`.

## Question

Checkpoint 5174 showed that the checkpoint-5173 CDM advantage was carried by
directionally under-resolved cube-corner modes. This checkpoint does not delete
the physical band. It resolves it isotropically by embedding the old low-mode
basis into a `96^3` source, adding one common high-mode realization, sampling it
with `144^3` particles and applying the same spherical taper to MTS and CDM.

## Exact shared-mode construction

For the standardized Gaussian Fourier basis `z_n`, every coarse integer mode
with component `|n_i|<32` is copied exactly into the extended grid. Coarse
Nyquist planes are excluded because they were removed by checkpoint 5174's
spherical control. New modes use one frozen independent seed and are shared by
both spectra. The maximum copied-mode error is
`0.0` and the inverse Hermitian
error is `1.5398946627761043e-18`.

The axis Nyquist rises from `20.15885441863777` to
`30.238281627956656 Mpc^-1`, above checkpoint 5174's
density-deficit `k90=29.08088339694904`.
The particle and force meshes supply respectively
`3.0` and
`4.0` cells per shortest
retained source wavelength.

## Forward result

```text
MTS preassembly q=3.0003735677908807,
CDM preassembly q=3.0779955071456984,
MTS forward q=1.3163215218202087,
CDM forward q=1.4120505307635705,
Delta q(CDM-MTS)=0.09572900894336178;
MTS q-band distance=0.19565611485980927,
CDM q-band distance=0.09992710591644749;

MTS RMSE=0.24952409629621566 dex,
CDM RMSE=0.24860397698800685 dex,
Delta RMSE(CDM-MTS)=-0.0009201193082088166 dex.
```

The inherited numerical envelopes are `0.0041618798307934135`
in q and `3.7956742793165965e-05` dex. Simultaneous passage
of the parent q band is `False`. The matched
branches are classified as `CDM_CLOSER_ON_Q_AND_RMSE_IN_ONE_RESOLVED_REALIZATION`.

This is a single shared realization. A resolved difference identifies the
need for a seed ensemble; it does not establish a model preference. An
unresolved difference shows only that the present formation gate does not
discriminate the spectra at this resolution.

## Decision

`THE_ISOTROPICALLY_RESOLVED_TRANSFER_BAND_FAVORS_CDM_IN_THIS_ONE_SHARED_REALIZATION_REQUIRE_A_PREDECLARED_MULTI_SEED_ENSEMBLE_BEFORE_REVISING_THE_PARENT_STATE_LAW`.

All `16` generated validations pass. Every output is
nonclaim. The protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
