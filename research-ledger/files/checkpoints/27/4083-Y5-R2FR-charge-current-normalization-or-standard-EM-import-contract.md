# 4083 - Charge-Current Normalization Or Standard EM Import Contract

- Timestamp: `2026-07-02T03:32:14+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `ABSOLUTE_CHARGE_ALPHA_NOT_DERIVED_STANDARD_VISIBLE_EM_IMPORT_CONTRACT_READY_LOCAL_GR_ROUTE_UNBLOCKED_NONCLAIM`
- Public charge/QED/alpha claim: `false`
- GitHub action: `false`

## Result

This checkpoint makes a hard fork decision instead of circling the coupling.

The exact theorem we can keep:

```text
compact U(1) + fixed representation labels n_A in Z
q_A = n_A q_star
D_X n_A = 0 on a fixed sector
```

So relative charge labels can be parent-owned conditionally.

The exact no-go:

```text
compact U(1) + Noether current + Maxwell equations
does not determine absolute e, w_EM, or alpha_EM
```

because the classical EM block still has a continuous gauge kinetic/current normalization unless the parent supplies a unique norm, level, no-extra-F2 theorem, or calibration.

## Standard Visible EM Import Contract

For the local GR/Newton branch, use the standard visible EM sector as calibrated matter:

```text
Delta_Hodge_EM = 0
C_JQ = 0
w_EM = 1
C_XF2 = 0
alpha_EM = CODATA measured constant
```

This is not an MTS derivation of charge. It is a disciplined import, like GR coupling to the Standard Model stress tensor without deriving the Standard Model.

## Constants Imported

```text
c = 299792458 m s^-1 exact
h = 6.62607015e-34 J Hz^-1 exact
e = 1.602176634e-19 C exact
alpha_EM = 7.2973525643000e-03 +/- 1.1e-12
alpha_EM^-1 = 137.035999177 +/- 2.1e-08
epsilon_0 = 8.8541878188e-12 F m^-1
mu_0 = 1.25663706127e-06 N A^-2
```

## What This Fixes

The alpha/charge loop is removed from the local-GR critical path:

```text
local source coupling can now use calibrated visible Hilbert stress
Poynting is counted once inside T_EM
nonzero MTS EM deviations remain testable residuals
```

## What It Does Not Fix

Still not claimed:

```text
MTS derives charge
MTS derives QED
MTS derives Coulomb law from first principles
MTS predicts alpha_EM
```

Those remain future parent-norm/particle-sector targets.

## Decision

```text
relative charge/current theorem = exact conditional
absolute e/alpha derivation = rejected for U(1)/Noether alone
standard visible EM import = accepted as private calibrated local branch
critical path returns to kappa/G/Newton/PPN
```

## Sources

- NIST/CODATA, `CODATA Recommended Values of the Fundamental Physical Constants: 2022`, NIST SP 961, May 2024.
- CODATA Task Group on Fundamental Constants, status page for the 2022/2026 adjustment cycle.

## Next

```text
4084-Y5-R2FR-kappa-G-source-denominator-to-Newton-Poisson-gate.md
```

That is the right next punch: source denominator, G/kappa normalization, Poisson limit, and PPN residuals using calibrated visible matter.
