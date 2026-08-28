# 5351: D4 E0025 support-endpoint coefficient extraction

## Purpose

Checkpoint 5351 evaluates the four two-sided support events at `epsilon =
0.0025` while leaving the checkpoint-5334 source geometry read-only.

## Exact-contact treatment

The generic parent fit is used directly for `E01` and `E08`. At `E02` and
`E03`, the exact contact centre has zero fit radius and is undefined for the
parent selector. Only that measure-zero centre is reconstructed from two-sided
off-contact traces. Derivatives, residues and primitives still use four direct
off-contact parent evaluations.

The accepted support run has:

```text
events = E01, E02, E03, E08;
selected stencil scale = 0.5 for all four events;
maximum gap trace mismatch = 1.2738804080370377e-08;
maximum coefficient trace mismatch = 2.6732359018849454e-09;
maximum primitive error = 3.392961411642806e-11;
coordinate sensitivity sum = 0.00030766056236188267;
validation = pass.
```

## First all-eight diagnostic

The first all-eight attempt, using the older checkpoint-5334 branch
coordinates, produced the provisional total

```text
A_E0025 = 0.0007535408879213424 + 0.470736824159685 i;
diagnostic radius = 7.941319234844445e-07.
```

That attempt is not accepted: all support, fit, primitive and opposite-side
checks pass, but all four one-sided branch gaps fail coordinate-resolution.
This identifies a branch-coordinate uncertainty problem rather than licensing
the provisional total.

## Claim boundary

Only

```text
valid_for_D4_E0025_support_endpoint_coefficients
```

is true. The all-eight coefficient, affine holdout, regulator-zero coefficient,
GR and MTS claims remain false at this checkpoint.

No GitHub action is taken.
