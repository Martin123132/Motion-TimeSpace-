# 5174 - Mass-gap continuation and spherical-cutoff discrimination gate

Marker: `MTS_5174_MASS_GAP_CONTINUATION_AND_SPHERICAL_CUTOFF_GATE`.

Date: `2026-07-21`.

## Question

Checkpoint 5173 found a matched CDM advantage over the empirical adiabatic
`m_gap=1e-20 eV` MTS/FDM comparator. This checkpoint asks two calculations
before changing the parent state law: is the response ordered along the
source-backed parent mass transfer, and does it survive removal of Fourier-cube
corner modes above the coarse-grid axis Nyquist?

## Derived continuation

The same checkpoint-5156 transfer is used without a new response coefficient,

```text
k_J,eq(m)=k_J,eq(m_ref) sqrt(m/m_ref),
x=1.61 m_22^(1/18) k/k_J,eq,
P_m(k)=P_CDM(k)[cos(x^3)/(1+x^8)]^2.
```

Every family uses its own covariance-derived one-sigma patch constraint, the
same fixed phases, nested force, calibrated `G_N`, visible history and scoring
operator. Only the spectrum changes. The target slope enters after evolution
solely to bracket a conditional empirical mass bound.

| family | m_gap (eV) | k_half (Mpc^-1) | preassembly q | forward q | RMSE (dex) | q band |
|---|---:|---:|---:|---:|---:|---:|
| `MTS_WKB_FLOOR_FULL` | `2.816691662e-21` | `19.839974` | `3.09704716` | `1.33525838` | `0.251622719` | `False` |
| `MTS_1E_MINUS20_FULL` | `1.000000000e-20` | `35.646025` | `3.68882451` | `2.23400714` | `0.277407739` | `False` |
| `MTS_BOUND_MID_1P778279410EMINUS20` | `1.778279410e-20` | `45` | `3.2586167` | `1.8261832` | `0.27616765` | `True` |
| `MTS_3P162277660E_MINUS20_FULL` | `3.162277660e-20` | `58.119735` | `3.25908769` | `1.81117952` | `0.27662592` | `True` |
| `MTS_1E_MINUS19_FULL` | `1.000000000e-19` | `96.949561` | `3.30327702` | `1.87036403` | `0.276732147` | `True` |
| `MTS_1E_MINUS18_FULL` | `1.000000000e-18` | `269.76791` | `3.27492333` | `1.82321462` | `0.276812113` | `True` |
| `CDM_FULL` | `infinity/CDM` | `inf` | `3.28035938` | `1.82953683` | `0.276797877` | `True` |

## Resolved-mode audit

The actual seed field is a `64^3` Fourier cube resampled
onto `96^3` particles. Its axis Nyquist is
`20.15885441863777` Mpc^-1 and its corner magnitude
is `34.91616007546498` Mpc^-1. The CDM-minus-MTS
density-deficit median is `24.14497544643008`
Mpc^-1; the displacement-deficit median is
`22.272597906829947` Mpc^-1.

The shared spherical-cutoff control gives

```text
full Delta q (CDM-MTS)=-0.40447031113307363,
cutoff Delta q=-0.0002568716802830995,
retained absolute fraction=0.0006350816690686276,
q advantage survives=False,
full Delta RMSE=-0.0006098618448825421,
cutoff Delta RMSE=0.0015974341841448192,
RMSE same sign=False,
checkpoint-5173 CDM advantage survives=False.
```

## Conditional mass diagnostic

```text
status=NUMERIC_Q_UPPER_CROSSING_PRESENT_BUT_NONMONOTONE_NO_STABLE_MASS_BOUND,
lower_mass_eV=1e-20,
upper_mass_eV=1.7782794100389228e-20,
lower_q=2.234007139940017,
upper_q=1.8261831992352753,
parent_q_upper=2.20499007120595.
```

This is not a derived parent mass and not a universal galaxy limit. A numerical
crossing is a bound only if the continuation is monotone within the numerical
envelope. Otherwise it is retained solely as evidence of UV/realization
sensitivity. An isotropically resolved calculation, an ensemble and a parent
state-preparation law remain necessary.

## Decision

`THE_5173_CDM_ADVANTAGE_DOES_NOT_SURVIVE_THE_SHARED_SPHERICAL_NYQUIST_CONTROL_THE_Q_SEPARATION_COLLAPSES_AND_THE_RMSE_SIGN_REVERSES_SO_DO_NOT_REVISE_THE_PARENT_STATE_LAW_FROM_THE_CUBE_CORNER_RESULT_REQUIRE_HIGHER_RESOLUTION_ISOTROPIC_SHARED_MODES`.

All `14` generated validations pass. Every output is
nonclaim. The protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
