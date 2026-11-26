# Short-time wave-only stellar impulse, at a fixed stripping site

Use the native semidiscrete Schrödinger equation with the same isolated Poisson solver as the time evolution. Time is measured in Myr, position in kpc, the stored potential in (km/s)², and C converts km/s to kpc/Myr. Denote the initial state u, native Hamiltonian H=K+V and a change of its real diagonal drive D=C² δΦ/κ. At release the two wave states are identical and the gravitational response of the wave and its first derivative vanish. A common additive potential or potential-rate offset is unobservable.

On a link i,j put z=conj(u_i)u_j, b=−iHu, q=D_i−D_j, J=[K,D]u. Subtraction between the corrected and original evolution gives
- δz' = i q z;
- δz'' = −conj(J_i)u_j − conj(u_i)J_j + 2 i q [conj(b_i)u_j+conj(u_i)b_j] − q²z + i (D'_i−D'_j)z.

The native radial and angular particle currents are the link conductance times κ Im z. Taking their signed divergence gives δn'' and δn''' without subtracting two large nearly equal densities. Summing with the cell volumes cancels every internal link. The last term is explicit host evolution; the remainder of δn''' is odd under conjugating the initial field for a given real drive. The second derivative is even. Apply the isolated Poisson map separately to both density derivatives **in the inertial grid**, then differentiate the potentials at the moving stellar and cluster positions. Gravitating a density already transformed into the moving cluster frame would double count its motion.

Let A₂ and A₃ be the resulting inertial acceleration derivatives in native force units, and let brackets mean star minus cluster evaluated at their initial positions and velocities. The wave-only velocity increment with the direct ordinary stellar source held fixed is

    δv_rel(t) = C t³ [A₂]/6 + C t⁴ B₃/24 + O(t⁵),
    B₃ = [A₃] + 3 [(v · ∇)A₂].

Here v inside the spatial derivative is in kpc/Myr. For example t² A₂(x(t))/2 adds t³ (v·∇)A₂/2 to the acceleration, accounting for the factor of three. Transport by the common stellar tide acting on the wave-only difference in position first contributes at order t⁵ in velocity. This prediction is not the full difference caused by changing ordinary gravity, nor is either difference the velocity difference between the two flow directions. Derive each at its own site before contrasting. No fitted time law.

Numerical controls: independent full Hamiltonian differentiation on an irregular manufactured mesh, parity, constant-drive and gauge tests, conserved total response, halved spatial directional-derivative probe, two spatial meshes, comparison with the previously derived A₂, and the actual finite impulse vector. A small error in the full vector does not mean we predict its smaller departure from cubic growth: report both denominators. For measurements, opposite directions are compared only at a common observation epoch; neither a 2,048-year series nor its Taylor law estimates a gigayear of stream drift.
