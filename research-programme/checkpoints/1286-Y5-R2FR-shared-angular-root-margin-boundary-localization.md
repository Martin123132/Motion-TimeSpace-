# 5270 - Shared angular root-margin boundary localization

## Derived boundary law

Checkpoint 5269 showed that reciprocal root transport is path-independent but
causal cycle occupation changes across the angular plane. This checkpoint
replaces the boolean occupation jump by its continuous parent function.

For a labelled global root evaluated at the sourced relative-chamber midpoint,

`m_label(c) = log |z_label(c)|`.

The ownership boundary is exactly

`m_label(c) = 0`.

A representing pair is active when its two margins have opposite signs. A
material component is active when this condition holds for both its
representative and reciprocal pairs. The source crossing labels and chamber
midpoints are identical for E040 and E020, so this boundary geometry is shared
by both regulators.

## Localization

Every one of the 24 labelled root margins is scanned in both angular
directions, at eight soft-energy witnesses and four fixed values of the
transverse angle. All sign changes are bisected to bracket width at most
`2.0e-10`.

- Boundary functions: `1536`.
- Raw labelled boundaries: `940`.
- Merged shared boundaries: `281`.
- Topology-uniform panels: `345`.
- Coarse checkpoint-5269 transitions explained: `291/291`.
- Additional labelled crossings exposed by dense scans: `354`.
- Maximum boundary bracket width: `1.15833342917e-10`.
- Maximum root-margin residual: `5.25723976846e-09`.
- Maximum merged-coordinate spread: `0`.
- Maximum panel coverage residual: `2.22044604925e-16`.

## Decision

`ADOPT_LOCALIZED_SHARED_ANGULAR_BOUNDARIES__CONTINUE_BOUNDARY_SURFACES_OVER_SOFT_ENERGY`

Validation passed: `true`.

This accepts localized, topology-uniform angular panels at the eight witness
energies. It does not yet prove continuous boundary surfaces between those
energies and therefore does not yet authorize full angular cubature, a
phase-space coefficient, numeric UV value, local GR, or full MTS.

## Next derivation

Continue each merged boundary in soft energy using the same equation
`log|z_label|=0`, detect births/mergers, and construct three-dimensional
topology-uniform cells in `(x,c_soft,c_decay)`. Only then evaluate the
checkpoint-5268 energy-first rule on nested angular panels.

## Artifacts

- Runner: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_5270_shared_angular_root_margin_boundary_localizer.py`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5270\shared_angular_boundary_localization_result.json`
- Root descriptors: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5270\shared_cycle_boundary_descriptors.csv`
- Raw boundaries: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5270\localized_root_margin_boundaries.csv`
- Merged boundaries: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5270\merged_shared_angular_boundaries.csv`
- Angular panels: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5270\topology_uniform_angular_panels.csv`
- Coarse-edge coverage: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5270\coarse_transition_coverage.csv`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5270\shared_angular_boundary_localization_validation.csv`
