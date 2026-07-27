# 5137: A04 symmetric Laurent-cross order proof

## Derivation

For `f(t)=a_-2/t^2+a_-1/t+a_0+a_1 t+...`, paired samples give

`(t/2)[f(t)-f(-t)]=a_-1+O(t^2)`

and

`(t^2/2)[f(t)+f(-t)]=a_-2+O(t^2)`.

This separates simple and double principal parts without extracting a noisy
second Fourier mode from a surrounding contour.

## Result

- Outcome: `INCONCLUSIVE_A04_REMAINS_BLOCKED`.
- Real/imaginary `a_-2(t)` slopes: `{'real': 0.1528493246594605, 'imaginary': 0.22695331413580308}`.
- Residue axis disagreement: `0.386308391591`.
- Residue scale drift: `1.41033392458`.
- Nested/deep residue disagreement: `1.58665099654`.
- Conservative normalized `a_-2` bound: `7.7244589904e-05` against the unchanged `0.0002` gate.
- Deep chart repair authorized: `False`.

## Scope

No coefficient job was executed. This establishes only the local meromorphic
order needed by the numerical coefficient pipeline; it is not a UV, local-GR,
galaxy, or full-MTS result. The formalization tree remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
