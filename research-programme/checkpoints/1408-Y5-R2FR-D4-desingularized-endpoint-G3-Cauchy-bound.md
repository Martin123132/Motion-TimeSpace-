# 5392 — D4 desingularized endpoint G3 Cauchy bound

## Decision

`DESINGULARIZED_ENDPOINT_G3_CAUCHY_BOUND_CERTIFIED__PROCEED_TO_W3`

## Exact split

For `R=u+i v`, the certified event equation gives `z0=2 i u v`. The material equations are invariant under `(epsilon,v)->(-epsilon,-v)`, so the analytic branch has `v=epsilon h`. Checkpoint 5392 does not merely divide two intervals containing zero: it substitutes `v=epsilon h` into the parent equations and divides the algebraic imaginary equation by epsilon before interval evaluation. A strict complex Krawczyk certificate then owns `(u,h,...)` through epsilon zero.

At the lower endpoint of the exact affine-log primitive, put `r=z0/z1`. Then

`-Phi(z0)=H Log(epsilon/epsilon_ref)+G`,

`H=-s[C0 r-(C1/2)r^2]`,

`G=s[C0 r-(3C1/4)r^2]+H Log(epsilon_ref z0/epsilon)`.

The normalized gap is `epsilon_ref z0/epsilon=2 i epsilon_ref u h`. Every certified box keeps it nonzero and in one open half-plane, so its principal logarithm is analytic and bounded. All upper-end, cutoff and model-mismatch terms are assigned to the mapped-away `W` sector; this freezes rather than hides the remaining owner.

## Certified bound

- desingularized boxes: `80/80`;
- minimum normalized-gap modulus: `7.986098152301859e-09`;
- maximum normalized-gap logarithm: `18.908374971015387`;
- uniform endpoint `G3` upper bound: `1.4516631424764905e+33`;
- endpoint-G Taylor constant: `2.4194385707941508e+32`.

| event | sup |G| | sup |G'''| |
|---|---:|---:|
| E01 | 352687021.78425384 | 1.6928977045644198e+28 |
| E02 | 29350803.523639496 | 1.408838569134697e+27 |
| E03 | 65809.34595637243 | 3.158848605905879e+24 |
| E04 | 1608320606575.3972 | 7.719938911561913e+31 |
| E05 | 28634273047587.848 | 1.374445106284218e+33 |
| E06 | 7506.698798945135 | 3.6032154234936684e+23 |
| E07 | 4592238.645426373 | 2.2042745498046608e+26 |
| E08 | 1777383.6142889452 | 8.531441348586945e+25 |

## Scope

This closes the endpoint nonlogarithmic `G3` owner in the frozen 5376 decomposition. It does not bound mapped-away `W3`; therefore the total uniform remainder, D4 outer limit, local GR and full MTS claims remain false.
