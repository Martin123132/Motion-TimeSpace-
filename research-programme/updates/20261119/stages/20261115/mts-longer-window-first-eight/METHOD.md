# First half of the frozen longer-window test

This stage implements the first acquisition batch in ../mts-duration-growth-law-20261115/next-window-contract.json: original reports2909..2916. It extends the existing history to25 reports, preserving all17 prior reports. It does not start the second batch2917..2924.

## Prediction and test ordering

1. Freeze code, native query plans and sealed inputs.
2. Reuse the same native DLL, full original clock and modes. Acquire construction source values at the new cell endpoints and quarter/midpoints, splitting at retained background corners.
3. Keep all previous source cells/coefficients unchanged. Freeze numerical source predictions at each fresh sixth/five-sixths query before launching validation acquisition. The validation worker checks the freeze SHA before loading these new probe values.
4. Test source curvature and boundary readouts at unchanged gates. Compare construction/validation main packets to each other and prior control packets.
5. Continue full, original-quadratic and independently conditioned difference states from2908, not from newly fitted initial conditions. Continue the nine saved Volterra terms Y0..Y8 from the same endpoint. Retain original signed weights and preparation.
6. Freeze these calculated outputs before direct-reference/response scoring. No target-dependent coefficients, exponent or thresholds are chosen.
7. Recompute response gains for2916. Compare against the direct native weighted reference and the independently evolved difference, then seal results and cleanup.

Source construction is numerical interpolation from prescribed equations, not an observational fit. Native main packets and reference probes can share a construction capture; the source/interpolation predictions are frozen before their new validation probes, while response outputs are frozen before scoring. This is not claimed to be an untouched observational holdout.

## Unchanged equations and controls

Each original node retains

    DeltaX' = A(t_i+s) DeltaX + B(t_i+s) R_i(s),
    R_i(s) = integral_0^s (s-v)[Khat(t_i+v)-K_i(0)]dv.

The time-dependent expansion remains

    Y0' = B R, Y(n+1)' = A Yn, n=0..7.

No term is reset at2908. A,B,C, the902 signed preparation nodes and weights, physical source bank, backgrounds, parameters, normalizations and original quadratic origin remain unchanged. Pure T^4/T^5 extrapolation is not used.

DOP853 rtol1e-10, normalizedatol1e-12; physical maximum steps are the ORIGINAL first-window duration divided by32 or64, not the now-longer duration divided by these numbers. Output reports use original saved epochs. New probes diagnose the source interpolation; they do not alter the physical mode/background grids.

## Endpoint reference and uncertainty

The25-row native boundary packet spans2892..2916, with the original918 main packets through2908 required byte-identical. For each of the eight new reports,902 shifted-time native readouts supply the same signed projection with the original matching anchor.

The prior17 reference rows and budgets are retained; they are not extrapolated. New numerical working allowances separate probe-schedule sensitivity, reference readout arithmetic, initial recapture and32/64 evolution differences.

The endpoint response gains are recomputed from the original origin through2916. Conservative source uncertainty includes the maximum previously retained and new source-reconstruction errors. Gain refinement and source variation enter the envelope in the same way as the prior stage. These finite checks are working numerical estimates, not certified continuum bounds.

The response expansion has an additional correction-amplitude test at2e-5, as in the frozen growth stage, besides the original observable-scale gate. Algebra/prefix checks retain1e-10 or exact equality as specified. All results apply equally to baseline and MTS. No observational fit, GitHub operation, native rebuild or new second-batch calculation is authorized.
