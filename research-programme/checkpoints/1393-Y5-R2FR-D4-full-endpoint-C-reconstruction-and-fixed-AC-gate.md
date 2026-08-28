# 5377 - D4 full endpoint C reconstruction and fixed-A,C gate

## Decision

`D4_FULL_ENDPOINT_C_CANDIDATE_RECONSTRUCTED__FIXED_A_C_BRANCH_COMPATIBLE__INTERVAL_PROOF_OPEN`

The exact endpoint primitive was reconstructed at all six coefficient rungs with the full lower-log coefficient

`H=-s[C0(z0/z1)-(C1/2)(z0/z1)^2]`.

The first term reproduces every stored 5357 event coefficient. The second term is not optional at order epsilon squared. Defining `K=H/epsilon` gives the exact identity `C_log=K'(0)=H''(0)/2`, and event by event

`C_log,e=-s[C0' r'+(C0/2)r''-(C1/2)(r')^2]`, with `r=z0/z1`.

## Numerical reconstruction

- full-primitive C candidate: `0.2260726982635993 -0.0007303900894365201 i`;
- conservative candidate diagnostic disk: `0.0039847013964454`;
- fixed-A,C maximum normalized integral residual: `0.015793583354026412`;
- fixed-A,C relative intercept envelope: `0.003943788309645922`;
- unchanged one-percent comparison: `0.01`.

Fixing this parent candidate removes the freely fitted `C epsilon^2 Log epsilon` direction. The seven integrated rungs remain comfortably inside their conservative disks. This is a useful compatibility result, but the finite-rung slope is not relabeled as the exact zero-regulator derivative.

## Event atlas

All eight events retain their source ordering across `7` sampled regulator values from zero through `0.02`. Their fixed candidate tubes are disjoint, the largest sampled displacement occupies `2.7282657005481792e-05` of its tube, and the minimum sampled transverse slope is `0.11796326417890847`.

The next proof is now sharply defined: interval-certify those tubes, evaluate the parent derivative formula for C at zero, and enclose H3. Until that is done, the common-interval atlas, endpoint-C limit, uniform remainder, D4 outer limit and all broader claims remain false.
