# 5173 - Matched CDM formation baseline discrimination gate

Marker: `MTS_5173_MATCHED_CDM_FORMATION_BASELINE_DISCRIMINATION_GATE`.

Date: `2026-07-21`.

## Question

Checkpoint 5172 showed that source flattening does not repair the selected
formation response. That miss cannot be interpreted fairly until the same
pipeline is applied to a standard collisionless baseline. This checkpoint
therefore changes exactly one input: the MTS/FDM linear covariance
`P_CDM T_FDM^2` is replaced by its source-backed `P_CDM` parent curve. The
white phases, antithetic pairing, one-sigma constraint rule, nested force,
calibrated `G_N`, visible source, cooling solution, transport construction,
particle count, time step and scoring code are identical.

## Covariance difference

For UGC09133 the source table gives

```text
sigma_CDM=1.9544359736828194,
sigma_MTS=1.954435819834488,
sigma ratio=0.9999999212824909.
```

The power ratio is `0.999999999999383` at `1/R_L`,
`0.9999999617892193` at `2pi/R_L`, and
`0.8006483134230982` at the particle Nyquist scale.
Thus the halo-scale covariance is nearly identical while the resolved
small-scale tail supplies a genuine matched difference.

## Forward result

Before visible assembly, the matched pair gives

```text
MTS q=3.688824512640322,
CDM q=3.2803593820913157,
Delta q=-0.40846513054900635.
```

After the identical isobaric `Z=0.3` pair-consistent source history,

```text
MTS q=2.234007139940017,
CDM q=1.8295368288069433,
Delta q=-0.40447031113307363;

MTS RMSE=0.27740773926786666 dex,
CDM RMSE=0.2767978774229841 dex,
Delta RMSE=-0.0006098618448825421 dex.
```

The inherited selected-branch numerical envelopes are
`0.0041618798307934135` in q and
`3.7956742793165965e-05` dex in RMSE. The matched response is
classified as `CDM_CLOSER_ON_Q_AND_RMSE`.

## Interpretation

`THE_MATCHED_CDM_COVARIANCE_OUTPERFORMS_THE_CURRENT_MTS_STATE_IN_THIS_SHARED_PHASE_PATCH_SO_THE_MTS_STATE_SELECTION_ROUTE_REQUIRES_REVISION_BEFORE_PROMOTION`.

This is a baseline-symmetry result, not a CDM cosmological validation and not
an MTS galaxy claim. If the responses are indistinguishable, the one-patch
formation failure is a limitation shared by the comparator and cannot be used
as MTS-specific evidence. It still leaves the MTS parent state law underived.
If they are distinguishable, the sign is reported without retuning either
branch.

All `13` validations pass. Every row remains
nonclaim. The protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
