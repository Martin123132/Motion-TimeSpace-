# 5256 - Outer topology bisection generation 2 and half-residue bound

## Generation-2 evaluation

- `D01A` / `I01_T00` at `-0.905779579376`: `(1348.86251502695+1393.7778210223219j)`, active poles `2`.
- `D01B` / `I01_T01` at `-0.797935135592`: `(-478.20923059185424+2339.9017390043123j)`, active poles `2`.
- `D06A` / `I06_T00` at `0.770974024646`: `(5426.884066636261-2.3176655552788885j)`, active poles `0`.
- `D06B` / `I06_T01` at `0.905779579376`: `(-1650.9722262974294-1393.7781124828282j)`, active poles `2`.

## Narrowed brackets

- `I01_T00` -> `[-0.919260134849, -0.905779579376]`, counts `0 -> 2`, next `-0.912519857112`.
- `I01_T01` -> `[-0.797935135592, -0.784454580119]`, counts `2 -> 0`, next `-0.791194857855`.
- `I06_T00` -> `[0.770974024646, 0.784454580119]`, counts `0 -> 2`, next `0.777714302382`.
- `I06_T01` -> `[0.905779579376, 0.919260134849]`, counts `2 -> 0`, next `0.912519857112`.

## Derived half-residue identity

The regulator combination and the physical A00/kernel normalization give

```text
R_epsilon(x) = N_epsilon(x)/D'_epsilon(x);
Delta f(x) = -i pi (P_A00 K) [2 R_E020(x)-R_E040(x)];
pi |P_A00 K| = 0.016.
```

Therefore, on a constant-topology chamber `C`,

```text
sup_C |Delta f|
 <= 0.016 [
    2 sup_C|N20|/inf_C|D20'|
      + sup_C|N40|/inf_C|D40'| ];

|delta I_boundary|
 <= J delta_x sup_C|Delta f|.
```

- `D01A`: `TWO_REGULATORS_FITTED`, predicted jump imaginary `1393.77867143`, physical imaginary `1393.77782102`, relative residual `6.10147095284e-07`.
- `D01B`: `TWO_REGULATORS_FITTED`, predicted jump imaginary `2339.89134852`, physical imaginary `2339.901739`, relative residual `4.44058230644e-06`.
- `D06A`: `INACTIVE_NO_RESIDUE_TERM`.
- `D06B`: `TWO_REGULATORS_FITTED`, predicted jump imaginary `-1393.77867143`, physical imaginary `-1393.77811248`, relative residual `4.01031750634e-07`.

- Maximum current half-residue imaginary residual: `4.44058230644e-06`.

## Stopping-gate status

The algebraic inequality is derived. The rows below insert sampled `N` and `D'` values only; they are not continuous interval enclosures and remain nonclaim.

- `I01_T00` active endpoint `D01A`, sampled half-residue envelope `4181.14862459`, location proxy `14.0910514937`, provisional generations `5`.
- `I01_T01` active endpoint `D01B`, sampled half-residue envelope `7019.38287738`, location proxy `23.6562950662`, provisional generations `6`.
- `I06_T00` active endpoint `C06A`, sampled half-residue envelope `10244.8681017`, location proxy `34.5266281896`, provisional generations `6`.
- `I06_T01` active endpoint `D06B`, sampled half-residue envelope `4181.14862459`, location proxy `14.0910514937`, provisional generations `5`.

## Decision

`ADOPT_BISECTION_GEN2_AND_HALF_RESIDUE_IDENTITY__BUILD_CONTINUOUS_ENCLOSURE`

## Claim boundary

No sampled extremum is called a supremum, and no sampled minimum is called an infimum. Outer convergence, the numeric p8 coefficient, all-operator local GR, and full MTS remain unclaimed.

## Next exact target

Construct interval enclosures for `N_epsilon(x)` and `D'_epsilon(x)` over each narrowed active-side chamber. Generation-3 bisection may run concurrently, but its stopping decision must use those continuous enclosures rather than another endpoint proxy.
