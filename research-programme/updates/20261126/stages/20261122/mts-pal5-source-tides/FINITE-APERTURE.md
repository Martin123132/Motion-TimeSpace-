# Finite aperture without replacing the Galaxy by an affine tide

For a Lagrangian selection of initially non-streaming stars inside a sphere of radius A, measure the specific energy E in the cluster alone. At each star let b_j(x)=a_j(X+x)−a_j(X) and b=sum_j b_j. At this instant the terms linear in internal velocity average to zero even on a translating trajectory and for a time-dependent external acceleration. With the initial stellar density ρ* and velocity second-moment tensor P, differentiation of the work gives

    M* <E_j''> = integral [ρ* b·b_j + ρ* a_cluster·b_j + P:grad b_j] dV.

An initially stationary Jeans population obeys div P=ρ* a_cluster. Integration by parts cancels the last volume derivative. For a spherical pressure tensor with P n=p_r(A)n on the boundary, Gauss's law for the external field gives the exact Newtonian identity

    <E_j''> = <b·b_j>_A − [4πG p_r(A)/M*(A)] M_j(ball centred at X, radius A).

In particular the second term is not the density *at the centre*. The result holds at the initial instant in a fixed freely falling, nonrotating Cartesian frame for this labelled population, not as a long-time escape law. A force interpolator may have an effective enclosed mass defined by its own flux; that quantity must not be silently substituted for the physical mass of ordinary matter. No mass belonging to the cluster is counted in the external term.

Test locally using the original one-, two- and three-scale Plummer apertures and saved reset wave at snapshot 586. Use explicit quadrature over the stellar positions; no fit to any trajectory or tidal target. Preselect a 3x3 then 5x5 cosine-node table of cylindrical acceleration over ±3a in R,z, taken from the direct continuous Newton integral. Subtract the central force after rotating to local Cartesian axes. Test new relative forces at off-grid points (0.43,0.53), (−0.33,0.26), (0.65,−0.72) in half-width units, with higher quadrature order, against their same-order central force. Check separately the inferred flux and actual enclosed mass; compute the latter independently using the continuous stellar+gas law. Use the unchanged 0.5% gate; keep small or cancelling quantities on their own scales and flag any failure. Do not promote an interpolated trace that fails the local density test. Check the Jeans boundary identity against integrated velocity moments on a non-affine manufactured force as well as the local controls. The saved wave is a fixed source for an instantaneous conditional test, not a replay in the changed potential.
