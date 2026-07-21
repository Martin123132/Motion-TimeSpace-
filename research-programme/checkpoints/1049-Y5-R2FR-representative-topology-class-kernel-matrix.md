# 5033 Y5/R2FR representative topology-class kernel matrix

## Scope

Checkpoint 5032 established the projectively correct causal topology on a
nine-event finite-`x` grid but evaluated only one event kernel. This checkpoint
evaluates one causally corrected kernel for each of the eight observed topology
classes. It is an inner-kernel completion gate, not the outer phase-space
integral and not a full-MTS claim.

## Numerical derivation

The first matrix run exposed four distinct numerical defects. None was repaired
by weakening the acceptance thresholds.

### Strict pole coincidence

The global-cycle implementation had merged merely close roots at relative
tolerance `2e-7`. Adaptive quadrature must approach such pinches without
declaring them identical. Exact numerical coincidence is now tested at
relative tolerance `5e-12`; distinct opposite-ownership roots remain separate.

### Conditioned global base cycle

For global pole moduli `r_i=|x_i|`, the original discontinuous base-radius rule
could jump to a circle near unrelated poles. The replacement is

```text
r_sub = 0.2 min_i r_i.
```

When `r_sub >= 2e-3`, that sub-minimum circle is retained. If a chart-origin
collision drives it below the conditioning floor, the base cycle moves to the
widest pole-free logarithmic annulus,

```text
(r_-,r_+) = argmax_j log(r_(j+1)/r_j),
r_base = sqrt(r_- r_+).
```

Residue transport makes these base cycles analytically equivalent. The switch
is therefore a numerical conditioning choice, not a new physical prescription.

### Pair-local double residues

Computing a small relative residue as the difference of complete global cycles
caused catastrophic cancellation. For a relative collision `y_*`, the residue
is now evaluated directly on its local two-torus:

```text
R_y = (1/2pi i) integral_[|y-y_*|=rho_y] dy/y
        sum_(a in I_+) [(1/2pi i) integral_[|x-x_a(y)|=rho_x]
                         dx/x F(x,y)].
```

`I_+` contains the causally owned member of each opposite-ownership collision
pair. Each inner radius is `0.15` times the distance to the origin or nearest
distinct global pole. The outer nested-contour test first uses `0.10/0.05` of
the nearest relative-collision distance. It retries at `0.20/0.10` only if the
two estimates fail the unchanged `5e-3` residue-stability gate. All contours
remain strictly inside the nearest other collision.

This construction reproduces the previously stable order-one `C4` residues to
about twelve digits. It also resolves the small crossed `C4` pair as

```text
-3.254424897e-6 - 8.093840659e-6 i
```

and identifies the cancellation-dominated rows that are genuinely zero at the
declared `1e-7` numerical-zero threshold.

### Collision-scaled adaptive relative cycle

Each relative chamber is split at every collision projection and at scales set
by the collision distance. Stable simple-pole principal parts are subtracted,
integrated analytically, and restored. An embedded order-12/order-24 Gauss rule
then refines the regular remainder to relative tolerance `5e-5`, with a hard
cap of 1024 intervals.

The conditioned global cycle reduces the difficult `C6` calculation from 1066
combined intervals and a failed `4.32e-4` estimate to 67 intervals and a
passing global-32 chamber estimate of `1.36e-6`.

## Representative matrix

The reported value is the global-32, adaptive order-24 causally corrected
kernel.

| class | event | corrected kernel | global residual | adaptive residual |
|---|---|---:|---:|---:|
| C0 | E04 | `6.626147699-33.44638256i` | `1.857e-7` | `9.988e-7` |
| C1 | E00 | `11.49236186-13.28446645i` | `7.733e-8` | `1.861e-9` |
| C2 | E08 | `2.256226617+1.202050198i` | `2.794e-6` | `2.177e-5` |
| C3 | E07 | `-3.349348921-0.6189141952i` | `3.188e-12` | `3.444e-8` |
| C4 | E01 | `3.575761345-0.1320406190i` | `1.177e-11` | `7.500e-10` |
| C5 | E05 | `-5.090353836-1.555871838i` | `1.339e-13` | `1.500e-8` |
| C6 | E06 | `0.8991598596+0.2572776206i` | `7.266e-5` | `3.785e-5` |
| C7 | E03 | `0.1419775790+0.04565144850i` | `8.446e-13` | `1.027e-11` |

All eight classes pass. Across the global-32 representatives, all 190 selected
collision residues are stable, 114 are numerical zero, and only one requires
the wider local-torus retry. The maximum nonzero residue instability is
`6.657e-4`, below the unchanged `5e-3` gate. There are 52 crossed corrections,
24 of which are nonzero.

The worst global and adaptive residuals are both in `C6` and remain below the
declared `1e-3` and `2e-4` class limits. The maximum global-tier correction
difference is below serialized precision.

## Supersession

Checkpoint 5032's topology remains authoritative. Its baseline numerical
kernel is superseded by the `C1` result above: the change is

```text
Delta K = 6.877719924e-4 + 1.116165417e-3 i,
|Delta K|/|K_5033| = 7.464e-5.
```

The shift follows from the corrected base-cycle conditioning and pair-local
residue evaluation; it is not a topology change.

## Decision

- Eight projective causal topology classes: **retained from 5032**.
- One representative corrected kernel per class: **passed**.
- Pair-local crossed residues: **derived and passed**.
- Dual global-cycle and adaptive-relative convergence: **passed**.
- Outer `(x,s_z,d_z)` phase-space integration: **open**.
- Crossing-complete `hhh` cut and UV coefficient: **open**.
- Local GR, Newton, Maxwell, and full MTS: **not claimed by this checkpoint**.

Next: build a bounded, restartable outer phase-space smoke integrator. It must
classify every sampled event onto the validated causal sheet, use independent
scrambles and global-node tiers, checkpoint partial sums, and compare the
resulting cyclic `hhh` vector with the fixed checkpoint-5018 target. Do not
launch an unbounded production run or fit the target.

Marker: `MTS_5033_REPRESENTATIVE_CLASS_KERNEL_MATRIX_GATE`.
