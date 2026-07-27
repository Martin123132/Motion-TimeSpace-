# 3191 - Selected Profile Transfer Runner Or Parent Action Profile Equation Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, solar-J2 pass, clock pass, orbital pass, or public-facing result.

## Result

3190 selected the smooth candidate:

```text
w = 0.435,
N4_D2 = 3.392613563564943.
```

3191 asks how fragile this candidate is if the future PPN/orbital transfer bound is tighter than the current public `P2` pressure proxy.

For the selected profile:

```text
|P_H| <= (5/4)|s_K2 kappa_STF|N4_D2.
```

So:

```text
|P_H| <= 4.240766954456179 |s_K2 kappa_STF|.
```

## Transfer Sensitivity

For:

```text
|s_K2 kappa_STF| = 1,
```

the selected profile uses only:

```text
1.740693644208775e-11
```

of the current tight pressure proxy.

Equivalently, the transfer bound can become:

```text
5.744839923640726e10
```

times tighter before the order-one coupling/profile cell fails.

For:

```text
|s_K2 kappa_STF| = 1e9,
```

the transfer bound can still become about:

```text
57.44839923640726
```

times tighter before failure.

So the selected profile is not delicate unless the transfer upgrade is extremely tighter or the coupling product is huge.

## Parent Profile Equation Contract

The selected smoothstep profile is still an ansatz.

If the parent action selects profiles by minimizing quadratic projected source stress:

```text
J[F] = integral x^4 (D2[F])^2 dx,
```

where:

```text
D2[F]=(2/5)F''+2F'/x+6F/(5x^2),
```

then the Euler-Lagrange contract is:

```text
D2^dagger[x^4 D2[F]] = 0,
```

with:

```text
D2^dagger[u] = (2/5)u'' - (2u/x)' + 6u/(5x^2).
```

This is not claimed as the MTS parent equation. It is the next clean derivation target.

## Decision

The selected profile survives substantial transfer tightening for moderate couplings.

The remaining fork is:

```text
solve/source the parent profile equation,
```

or:

```text
derive the actual PPN/orbital transfer bound.
```

Next target:

```text
3192-Y5-R2FR-solve-quadratic-profile-EL-or-upgrade-slip-transfer-bound-under-AX1090
```
