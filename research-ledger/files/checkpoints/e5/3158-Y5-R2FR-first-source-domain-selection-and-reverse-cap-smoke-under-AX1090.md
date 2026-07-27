# 3158 - First Source-Domain Selection and Reverse-Cap Smoke under AX1090

Private checkpoint. This follows 3157 by taking the concrete route instead of adding another abstract missing-input ledger.

3157 left the product gate:

```text
L_Wphys_Lambda * B_metric <= cap
```

with:

```text
L_Wphys_Lambda := L_W_phys ||Lambda||_*.
```

3158 asks:

```text
if we fill the first real local source/domain, how small would L_Wphys_Lambda actually need to be?
```

## Selected Source Domain

Chosen domain:

```text
Earth equatorial exterior shell at R = R_Earth_equatorial.
```

Reason:

- it directly matches the 3156 J2 quadrupole reverse cap;
- Earth GM, radius, and geopotential coefficients are public source-backed values;
- it is local-GR relevant without needing galaxy/cosmology machinery;
- it keeps the test simple enough that a failure would mean something.

Spin/frame dragging is not filled here because it needs a separately sourced Earth angular momentum or inertia convention.

## Source Values

The smoke runner uses:

```text
c = 299792458 m s^-1
GM_Earth = 3.98600435507e14 m^3 s^-2
R_Earth_equatorial = 6.3781366e6 m
Cbar20_zero_tide = -4.8416948e-4
J2 = sqrt(5) |Cbar20_zero_tide| = 1.082635869910725e-3
epsilon_G = GM_Earth/(c^2 R_Earth_equatorial) = 6.953485394305608e-10
```

The tide comparison uses:

```text
GM_Moon = 4.902800118e12 m^3 s^-2
d_Moon = 3.844e8 m
GM_Sun = 1.32712440041279419e20 m^3 s^-2
AU = 1.495978707e11 m
```

Source/provenance rows are written to:

```text
D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3158_SOURCE_VALUES.csv
```

## Reverse-Cap Results

The inherited caps are:

```text
single cap = 5.970964001482571e-4
equal diagnostic cap = 9.951606669137618e-5
```

For the Earth quadrupole with unit projection coefficient:

```text
B_J2/C2 = epsilon_G |J2| = 7.528092708775573e-13.
```

So:

```text
L_Wphys_Lambda <= 7.931576074404820e8 / C2         single cap
L_Wphys_Lambda <= 1.321929345734137e8 / C2         equal cap
```

For the Sun+Moon radial tide smoke with unit projection coefficient:

```text
B_tide/Ctide = 1.140243262621331e-16.
```

So:

```text
L_Wphys_Lambda <= 5.236570297951847e12 / Ctide     single cap
L_Wphys_Lambda <= 8.727617163253077e11 / Ctide     equal cap
```

## Interpretation

This is not a local-GR pass.

It is still useful.

The first real local source/domain does not force `L_Wphys_Lambda` to be tiny under unit projection coefficients. Earth J2 is the tightest first smoke row, and it still leaves a very large product ceiling unless `C2` is enormous.

So the immediate obstruction is not:

```text
local Earth source terms instantly blow AX1090 apart.
```

The obstruction is:

```text
C2, Ctide, and L_Wphys_Lambda must be derived in the same parent-owned norm/projection convention.
```

That is a better problem. It turns the next step into a coefficient derivation instead of another yes/no panic gate.

## Claim State

No claim is promoted.

3158 does not claim:

- local closure;
- local-GR recovery;
- WEP;
- R10;
- PPN;
- clock safety;
- orbital safety;
- Maxwell recovery;
- Newtonian recovery.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3158_first_source_domain_selection_and_reverse_cap_smoke.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3158_INPUTS.csv` |
| domain | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3158_SOURCE_DOMAIN_SELECTION.csv` |
| source values | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3158_SOURCE_VALUES.csv` |
| reverse cap smoke | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3158_REVERSE_CAP_NUMERIC_SMOKE.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3158_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3158_VALIDATION.csv` |

## Decision

3158 promotes the next target to:

```text
3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.
```

Target:

```text
derive C2 and Ctide from the actual metric/source projection convention,
or bound them tightly enough that the 3158 reverse caps become a real gate.
```

This is the right next attack because the first sourced domain says the numbers are not obviously fatal; the missing structure is the parent-owned projection/coupling map.
