# Stage173 — adjacent incoming-frequency temperature test

New incoming frequency x=11.5649290917356; saved reference x=14.
The new node is the immediately lower inherited order7 node in the8-20 panel,
selected before source evaluation. No quadrature or temperature-rule changes.

## What was predicted
Applied the same microscopic temperature construction at the new frequency using
its own physically evaluated stencils. This is NOT a frequency interpolation from14.
All36 new electron/hard-angle target sources were evaluated after prediction freeze.
Anchor fraction .875; target .90625; log-temperature steps .01 and .005 unchanged.
The x=14 predictions and target sum are reused unchanged. The two-node partial-sum
comparison is partly prospective because x=14 target results were already known.
Frozen SHA256: `77344119958f4637d2586572f543c62c17d9f10117937e05a10edfe7478f060a`.
Frozen UTC: 2026-10-20T04:32:43.527589+00:00.

## Frozen quadratic comparisons
Maximum mass-dual photon-source error over the four inherited history columns.
Percentages follow sums of already-weighted source vectors, not averages of errors.

|Contribution|Incident history|Source|Linear error %|Quadratic error %|Quadratic stencil change %|
|---|---|---|---:|---:|---:|
|complete_sum|moving_history|control|1.60307895|0.0784218582|0.00635066953|
|complete_sum|moving_history|remainder|3.36770537|0.257408075|0.00829498496|
|complete_sum|moving_history|total|1.6014458|0.0782614669|0.00634991909|
|complete_sum|fixed_incident|control|1.13824267|0.0548652053|0.000797781373|
|complete_sum|fixed_incident|remainder|2.68421452|0.195037755|0.00283235545|
|complete_sum|fixed_incident|total|1.1368027|0.0547346325|0.00079588619|
|two_frequency_partial|moving_history|control|1.60522803|0.0785406781|0.0063616811|
|two_frequency_partial|moving_history|remainder|3.38427172|0.258639855|0.00818599992|
|two_frequency_partial|moving_history|total|1.60353054|0.0783741535|0.00636085957|
|two_frequency_partial|fixed_incident|control|1.13821168|0.0548623352|0.000797743799|
|two_frequency_partial|fixed_incident|remainder|2.68502677|0.195121853|0.00283357738|
|two_frequency_partial|fixed_incident|total|1.13672297|0.0547273356|0.000795784315|

complete_sum is the full inherited finite electron/hard-angle sum at the NEW node.
two_frequency_partial adds that weighted contribution to saved x=14. It is NOT the
full8-20 panel, an integral between the two nodes, or the complete incoming spectrum.
Control is the inherited leading microscopic baseline. Remainder is the matched MTS
difference+virtual+state increment; total includes both. Native incident histories are
the same for baseline/MTS, not refitted. These are numerical tests, not observational fits.

## Per-angle new-frequency prediction
|Hard-angle group|Moving baseline %|Moving MTS increment %|Fixed baseline %|Fixed MTS increment %|
|---|---:|---:|---:|---:|
|angle_negative|0.0783630338|0.258502295|0.0547992802|0.195085327|
|angle_central|0.0784924742|0.255080201|0.0549429518|0.194977838|
|angle_positive|0.0785651945|0.202534699|0.0550392638|0.18675058|

## Finite-difference stability
The1% coarse/fine D1 and D2 gates are unchanged. Native histories are piecewise
linear in time: this is finite-step variation, not classical curvature at a knot.

|Contribution|Incident history|Source|D1 change %|D2 change %|
|---|---|---|---:|---:|
|complete_sum|moving_history|control|0.00570599213|0.372324361|
|complete_sum|moving_history|difference|0.0128940355|0.182803555|
|complete_sum|moving_history|virtual|0.00136359584|25.7522011|
|complete_sum|moving_history|state|0.00142281144|20.4851928|
|complete_sum|moving_history|remainder|0.0128816758|0.202038843|
|complete_sum|moving_history|total|0.00569642045|0.372704719|
|complete_sum|fixed_incident|control|0.00498394955|0.00248818727|
|complete_sum|fixed_incident|difference|0.0112111135|0.00559897114|
|complete_sum|fixed_incident|virtual|0.0101362477|0.00502407851|
|complete_sum|fixed_incident|state|0.011018857|0.00505810283|
|complete_sum|fixed_incident|remainder|0.0111973278|0.00559203867|
|complete_sum|fixed_incident|total|0.00497462457|0.00248119922|
|two_frequency_partial|moving_history|control|0.00570893975|0.372448056|
|two_frequency_partial|moving_history|difference|0.0129001806|0.18291304|
|two_frequency_partial|moving_history|virtual|0.00133622183|26.094476|
|two_frequency_partial|moving_history|state|0.00143396103|20.4979972|
|two_frequency_partial|moving_history|remainder|0.0128911597|0.197941353|
|two_frequency_partial|moving_history|total|0.00569901982|0.372840267|
|two_frequency_partial|fixed_incident|control|0.00498374222|0.00248773545|
|two_frequency_partial|fixed_incident|difference|0.011209909|0.00559800648|
|two_frequency_partial|fixed_incident|virtual|0.010161338|0.00504154098|
|two_frequency_partial|fixed_incident|state|0.0110621936|0.00511027261|
|two_frequency_partial|fixed_incident|remainder|0.0112002589|0.00559319589|
|two_frequency_partial|fixed_incident|total|0.00497410033|0.00248050874|

## Reuse, batching and validation
216 new event-temperature combinations saved atomically in36 six-event batches.
The first six-event batch was run separately to test safe continuation. The production
restart skips those saved events and verifies their completed batch packet.
Saved x=14 predictions/derivatives and target sum, all native histories, basis and
available virtual-loop coefficients are reused. No previous payload is overwritten.
Protocol checks: 78; all pass: True.
Source energy/gas and component-closure checks: 25284; failures: 0.
Current failed numerical comparisons retained: 2040.
Immediate-parent/consumed files rehashed and authenticated: 572.
linear_fine: 344/2016 pass the unchanged1% prediction gate.
quadratic_fine: 2016/2016 pass the unchanged1% prediction gate.
quadratic_coarse: 2016/2016 pass the unchanged1% prediction gate.
Individual, angle, complete-node and partial-sum outcomes are correlated numerical
checks, not independent experiments. All failures remain visible. No fit, cutoff,
source-curve/history replacement, transport rerun, GitHub action or subagent.
One production worker, below-normal priority, one library thread.

## Next target
Extend the same frozen construction to the adjacent inherited node above14, in bounded
batches, reusing both completed nodes. Retain per-node outcomes while accumulating
the incoming panel; complete-node success is not a continuum integration bound.
