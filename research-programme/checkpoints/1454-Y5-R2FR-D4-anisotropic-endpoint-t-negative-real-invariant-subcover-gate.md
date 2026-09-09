# 5438: anisotropic endpoint-t negative-real invariant subcover gate

## Decision

**PASS FOR THE REPRESENTATIVE EXTERNAL01 INVARIANT SUBCOVER ONLY.**

The broad LR/R representative family has a finite negative-real subcover for `s01`. The pointwise endpoint is regular, the first nine coarse `t` cells close after adaptive refinement no deeper than `1/2048`, and the existing tail remains negative-real. Combined with the already-proved ratio disk, the exact identity `1/<01> = [01]/s01` gives a finite reciprocal bound without inventing an independent angle-edge closure.

## Certified cover

| target | x slabs | evaluations | leaves | max Re(s01) | min |s01| | max |1/<01>| |
|---|---:|---:|---:|---:|---:|---:|
| LR | 8 | 600 | 455 | -0.000135551615366 | 0.000135551615366 | 13157.6031298 |
| R | 32 | 2400 | 1463 | -0.000187298239289 | 0.000187298239289 | 9522.32916097 |

## Construction

- Keep the 5436 coarse tail `t >= 9/128`, whose union is already strictly negative-real.
- Cover LR with 8 `x` slabs and R with 32 `x` slabs.
- Adaptively bisect only the first nine coarse `t` cells, to maximum depth four (`Delta t = 1/2048`).
- Hull all leaves in the common negative-real half-plane.
- Use `|1/<01>| <= (1 + sup|R01|) / inf|s01|`, sourced from `[01] = R01 - 1` and `s01 = <01>[01]`.

## Scope

The declared regulator and contour-displacement boxes remain intact. This gate certifies one representative right-connector reciprocal family only. Parent v47 is unchanged and every broader claim flag remains false.

## Next target

Install the adaptive invariant subcover as parent v48, dry-run, migrate the saved state, and resume briefly to verify that the c0 external01 failure count stops increasing.
