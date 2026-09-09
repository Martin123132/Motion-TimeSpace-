# 5454: D4 epsilon-connected superprojection smoke

## Exact reduction

The `2074` checkpoint-5452 projection rectangles contain only `85` connected groups with identical event, cell, epsilon bin, x interval and imaginary-epsilon interval. Adjacent real-epsilon slabs in each group tile one closed interval with maximum reconstruction error `0.0`. No interpolation or physical closure is introduced.

The exact compression factor is `24.4`. Every source projection id occurs exactly once in the source map: `True`.

## Correlated smoke

One largest merged component per event is evaluated through all 32 exact parent Q arcs with the checkpoint-5452 adaptive x policy. Completed jobs: `8/8`; passed: `8`.

## Claim boundary

This checkpoint tests whether exact adjacent-slab merging can replace the measured 178-hour naïve enumeration. It does not certify all superprojections, the outer parent atlas, event-local W3, the D4 regulator limit, local GR or full MTS.
