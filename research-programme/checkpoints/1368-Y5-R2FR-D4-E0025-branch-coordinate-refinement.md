# 5352: D4 E0025 branch-coordinate refinement

## Purpose

Checkpoint 5352 resolves the only failed contract in the first E0025 all-eight
attempt. It imports the independently completed checkpoint-5337 targeted
branch-existence bisections instead of inventing smaller coordinate errors.

## Derived coordinate bound

Checkpoint 5337 freezes

```text
EVENT_ROOT_WIDTH = 2.0e-11;
midpoint coordinate error <= 1.0e-11.
```

Each E0025 branch scan completed 27 bisection iterations, below the frozen cap
of 80, with its targeted event contract true. The refined coordinates are:

| Event | Coordinate | Shift from checkpoint 5334 | New error |
|---|---:|---:|---:|
| `E04` | `0.8557134944359164` | `-4.2978498537848964e-10` | `1e-11` |
| `E05` | `0.8551115262704948` | `-2.344280325417003e-11` | `1e-11` |
| `E06` | `0.8565604503861255` | `3.367951473265407e-09` | `1e-11` |
| `E07` | `0.85715641659227` | `-2.681248556513083e-09` | `1e-11` |

Every new interval lies strictly inside its earlier coordinate-error disk. The
support-event rows are copied unchanged.

## Validation and decision

All source hashes, event identities, contracts, slope windows, contact
residuals, interval containments and read-only checks pass. The decision is

```text
D4_E0025_BRANCH_COORDINATES_BRACKET_REFINED__RERUN_ALL_EIGHT_COEFFICIENT
```

Only

```text
valid_for_D4_E0025_branch_event_coordinate_refinement
```

is true. No all-eight, holdout, regulator-zero, GR or MTS claim follows from
the coordinate refinement alone.

No GitHub action is taken.
