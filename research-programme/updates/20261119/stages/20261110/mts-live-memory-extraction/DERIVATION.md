# Current-state memory and its evolution defect

This stage extends the accepted short-window calculation, without changing the retained homogeneous background, physical parameters or source coupling. Its input construction is `../mts-live-carrier-memory-20261110/checked_live_memory_model.py`, used through `ExtractionMemory` in this directory. The independent product-rule repair and its failed predecessors remain in that earlier stage.

## Evolving the other species, not prescribing their future

On the fixed background, let Z contain the retained rest-species perturbations and the two heavy-carrier coordinates. Write A(t) for the exact transformed native linear operator and B(t) for the derived reduced operator. These are actions on the CURRENT state, not matrices fitted to a saved future trajectory. Define R=A-B.

The implemented first memory correction is

    Z0' = B Z0,
    Delta' = B Delta + R Z0,
    Delta(t0) = 0,
    Zstar = Z0 + Delta.

The initial perturbation is the original native state at extraction index 1991. The original later native trajectory is only a comparator. In particular, the rest-source variable and its derivative are evaluated from the current rest state and its current native response, including their response to the heavy sector. The parent background tables remain prescribed coefficients; evolving all perturbations does not independently derive those background tables.

The direct rest rows of R vanish in this construction. That does NOT imply Delta_rest remains zero: B couples a heavy correction into the rest equations. This feedback is part of the evolved full correction, not added after the integration.

## The candidate's derivative is not the exact equation at its state

Linearity gives the exact algebraic identities for this reduced system:

    Zstar' = B Zstar + R Z0,
    Zstar' - A Zstar = -R Delta.

If Ze obeys Ze'=A Ze with the same initial data, then e=Ze-Zstar obeys

    e' = A e + R Delta,     e(t0)=0.

These identities identify the omitted second-and-higher memory contribution. They do not by themselves bound its growth: a continuum bound additionally needs control of the propagator of A and R Delta. The finite-window comparisons here are numerical tests of the stated candidate, not that unproved bound.

For each output state the code saves BOTH the exact native derivative at the reconstructed candidate and the candidate's actual derivative. Let I_t denote the linear inverse coordinate map into native perturbations at fixed time. Then

    native_actual_prime = native_rhs_at_candidate
                          + I_t(Zstar_prime - A Zstar).

The time dependence of the coordinate map is already included in A. The additional term therefore uses the fixed-time inverse map; adding another time derivative there would double count it. `actual_physical_derivative` is the quantity checked against the native evolution. Merely checking `native_rhs_at_candidate` would hide the reduced equation's residual.

## Physical stress readout and signed extraction

In the saved k=1 conformal convention, write b,v for the heavy background field and velocity, u,w for its native perturbation and velocity, mu2 for the squared conformal mass, and beta=a/density0 for the retained normalization. The ordered physical source triplet is

    [D,Q,P] = beta [v*w + mu2*b*u, v*u, v*w - mu2*b*u].

The cold control has [D,Q,P]=[beta*R_c*delta_c,0,0] in its own retained source convention. No new halo normalization, observed-velocity target or galaxy population is introduced. Signed extraction uses the original 902 weights without reweighting or fitting. A small signed pressure integral can expose cancellation errors not visible in a density-only comparison.

## Fixed numerical experiment

Both branches use original native indices 1991 through 2892 inclusive, three fixed integration/metric-step configurations, and the same 2e-5 numerical and 1e-10 algebra gates. The absolute steps come from the accepted short-window experiment; they are not enlarged in proportion to this longer window. The full-window independent chain-rule preflight must pass before evolution.

Each 902-node stream is split at indices 0,256,512,768,901. The restart carries the raw normalized state with an unchanged, initial-only normalization, including the accumulated correction. It must agree bit for bit at the shared node. The final comparison removes duplicate boundary samples and verifies the complete original clock before applying any signed weights. Native initialization parity, unchanged selected caches, physical readout reconstruction and refinement comparisons are checked separately from candidate agreement.

This is a k=1 current-rest-feedback test in the retained early native regime. The separate late interface uses k=5 and a different state chart. It cannot be validated by relabelling this calculation or by inserting its k=1 coefficients unchanged.
