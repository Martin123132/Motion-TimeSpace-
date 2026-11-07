# Quadratic-core source construction and expanded native-constraint attempt

Start 2 October 2026 01:15:51 UTC. Safe handoff by05:15:51 UTC. Private post-checkpoint work only, maximum two one-core BelowNormal/BLAS1 workers, no agents or GitHub.

Implement the source-core construction from the preceding checkpoint, rather than repeating the flat-core trial space. At each material node use the actual physical radii to construct the two tapered columns y*w and y^2*w/2, y=R-b. Add the retained24 interior columns. The taper is identically1 in the inner18% of each side, identically0 beyond82%, and the C3 septic transition in between.

The initial core slope is nonzero. Iterate its curvature-to-slope ratio using the actual freshly calculated metric and full coupled source acceleration:

    ratio_new(label)=-(d(label)+a_source(label))/c(label)^2.

This is a bounded fixed-point attempt at the source-corner equation, not a fit of the source acceleration. Keep the source configuration and zero rates, normalize the initial field to the previous central positive norm, and save every iterate. The full native field/source forces enter H*a=F. Recompute native radial loads, not the old fixed-reference loads. Test the resulting same initial data in the empty-native-operator reference as well.

## General compensated tangent

Unlike the previous exactly flat basis, finite material interpolation may leave small source-jet differences. They must not be deleted. With J=q_R(b+)-q_R(b-), h_j=(X_j-b)_+, v_j=q(X_j), use

    f=B*D_X*(v-J*h),
    delta f=B*[delta D_X*(v-J*h)+D_X*(delta v-delta J*h-J*delta h)].

For source-pinned generators delta b=0, delta h_j=eta(X_j) on the right, and delta v uses the inherited average nodal gradient. Compute delta J from the actual two source-adjacent P2 polynomials, including their width changes. This remains valid when J or delta J is not exactly zero. Verify against the atom-based image/tangent and the scalar adjoint before using any fast quadratic forms.

For a continuous physical quadratic core the exact J and delta J vanish and local native images vanish. Report material/roundoff defects separately rather than forcing those identities into the numerical representation.

## Decision order

Construct and check source-corner-compatible nonzero initial data first. Then build the expanded10/18/26-mode shape forms,33 generators, two material rules32/48, and both retained field grids. Fit n-1 constraints at positive norm; keep other generators withheld. The inner metric is declared frozen. A positive finite-matrix separator is an obstruction in that frozen space and prevents promotion of an inner root, not a global exclusion. A candidate must be rechecked with its own live metric and source equation before any preservation/evolution claim.

If the expanded shapes admit an inner root, the next calculation is the coupled source-corner/shape solve and the generic second-order preservation equation, including metric kinetic response. If they do not, preserve the actual obstruction and evaluate whether a different source/geometry response could change it; do not spend long runs evolving an inadmissible state or divide by vanishing mesh inertia.

Sources: `DERIVATION-20261002-quadratic-source-core-construction.md`; `DERIVATION-20261002-general-second-order-shape-preservation.md`; `DERIVATION-20261002-source-flat-native-compatible-initial-data.md`; `scripts/annular_native_trial_matrix_20261001.py`; `scripts/annular_zero_rate_euler_20261001.py`.
