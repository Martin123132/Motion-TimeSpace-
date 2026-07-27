# 5239 — Matched-event A00 regular complement and regulator extrapolation

## Scope

This checkpoint selects source event `S522124_N0000` and integrates its conditional `soft_cosine` slice. Unlike the separate 5237/5238 method pools, the direct and endpoint-owned summands now coexist inside one event integrand.

## Why this event

The source topology contains 15 safe reciprocal components. 6 are nonzero at the parent event: 4 direct and 2 endpoint-owned. Along `soft_cosine`, both owner sectors contain a causally active pole, so the test exercises a genuine mixed singular slice rather than combining disconnected convergence scores.

## Derived event contract

For regulator $\epsilon$, the matched conditional integrand is

$$
\mathcal I_\epsilon(x)=\sum_{c\in\mathcal C_{\rm mat}}\Delta w_c\,\sigma_c\,\frac{C_c(x)}{r_c(x)z_c(x)J_c(x)}.
$$

Every term is inherited from the parent reciprocal topology. No event-level closure coefficient is introduced. The six material components reproduce the full parent safe-family integrand at the source point with maximum relative residual `1.677297e-09`. Dynamic merged-topology witnesses close to `0.000000e+00`.

The source winding cannot be frozen over the full outer domain. The branch-aware target homotopy is therefore evaluated on a bounded coarse grid, each integer transition is bisected, and the resulting piecewise winding difference multiplies the local residue. This removes two geometrically real but causally inactive poles per regulator rather than silently integrating their fixed-source continuation.

For each causally active outer pole $p_j$,

$$
\mathcal I_\epsilon(x)=\sum_j\frac{R_j}{x-p_j}+\mathcal I_{\epsilon,\rm reg}(x),$$

Every topology-resolved segment is evaluated as the globally regularized remainder plus $R_j[\log(b-p_j)-\log(a-p_j)]$. Pole-patch edges and all integer-winding transitions are explicit segment boundaries. Those segments cover the complete source domain without overlap.

The inherited two-level physical slice is

$$
I_{A00}^{(2)}=w_{A00}K\left(2I_{E020}-I_{E040}\right),$$

with `w_A00=-0.008` and `K=-0.6366197723675814`. Component matching reconstructs the stored parent family decomposition with maximum relative residual `1.963068e-16`.

## Numerical result

- Material regulator jobs: `12`.
- Geometric poles: `8`.
- Causally active poles: `4`.
- Dynamic winding intervals: `28` (`cache_hit=true`).
- Accepted full-component residue fits: `4/4`.
- Domain coverage residuals: `E040=0.000e+00`, `E020=0.000e+00`.
- Order-32 raw relative error: `0.00516656695447`.
- Order-32 subtracted relative error: `2.30719162132e-07`.
- Order-128 subtracted relative error: `8.59364587385e-08`.
- Low-order improvement factor: `22393.3153481`.
- Order-512 subtracted two-level slice: `36.03367871995233 -5.664052117920976 i`.
- Runtime: `254.247 s`.

## Decision

`ADOPT_MATCHED_EVENT_REGULAR_COMPLEMENT_AND_TWO_LEVEL_REGULATOR_EXTRAPOLATION`

This closes the first event-level direct-plus-endpoint conditional A00 integration contract. It replaces the prior sum of independent method pools with one source-matched integrand, explicit regular complement, and inherited E040/E020 extrapolation.

## Claim boundary

The result is **not** a numeric UV coefficient, local-GR derivation, or full-MTS result. It is a one-dimensional conditional slice. A physical coefficient still requires the remaining outer integrations and a source-pool replication; a third regulator level would independently test, rather than merely apply, the inherited linear extrapolation law.

## Next target

Promote the matched event contract to nested integration over the remaining outer coordinates, while carrying the same component matching, causal-pole subtraction, regular complement, and regulator checks.

## Validation

- `SOURCE_PATHS_EXIST`: `PASS`.
- `SAFE_COMPONENT_COUNT`: `PASS`.
- `MATERIAL_COMPONENT_COUNT`: `PASS`.
- `REGULATOR_MATCH_RESIDUAL`: `PASS`.
- `BASE_SOURCE_CLOSURE`: `PASS`.
- `DYNAMIC_WITNESS_CLOSURE`: `PASS`.
- `DYNAMIC_WINDING_INTERVAL_COVERAGE`: `PASS`.
- `DYNAMIC_WINDING_TRACK_RESOLUTION`: `PASS`.
- `POLE_CAUSAL_GATE_CONSISTENT`: `PASS`.
- `STORED_FAMILY_REGULATOR_CLOSURE`: `PASS`.
- `ACTIVE_POLES_FITTED`: `PASS`.
- `REGULAR_DOMAIN_COVERED`: `PASS`.
- `LOW_ORDER_SUBTRACTED_CONVERGENCE`: `PASS`.
- `MID_ORDER_SUBTRACTED_CONVERGENCE`: `PASS`.
- `SUBTRACTION_IMPROVES_LOW_ORDER`: `PASS`.
- `FORMALIZATION_WORKBENCH_UNCHANGED`: `PASS`.
- `RUNTIME_BOUNDED`: `PASS`.
- `CLAIMS_REMAIN_FALSE`: `PASS`.
