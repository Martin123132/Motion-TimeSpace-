> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The cancellation has a physical meaning: a flat transverse-traceless wave

This is a derivation in the weak-field limit of the retained local gravity equations, not an assumption that a matter-filled curved host is vacuum. It explains why passing or failing a scalar-constraint readout by itself does not tell us whether a physical tide is present.

Let Q be any constant symmetric trace-free Cartesian matrix, n the radial direction and Y=n·Qn a degree-two spherical harmonic. In an orthonormal spherical basis the spatial metric perturbation has radial entry 2LY, mixed entry v D_A Y and tangent block 2bY γ_AB + d (D_A D_B Y+3γ_AB Y). In the one radial chart channel of [the cancellation derivation](DERIVATION.md), b=−L/2, v=L+rL′/3 and d=rv′/2+3v/2−L/2. The trace vanishes. The radial divergence coefficient is 2L′+(4L−4b−6v)/r and the tangent divergence coefficient is v′+(3v+2b−2d)/r. Both vanish identically. The momentum of the corresponding velocity channel also satisfies the flat vacuum constraint. This is a transverse-traceless tensor, not just a cancellation in a single scalar.

Write s=x·x, X=x·Qx, q=Qx and L=f(s,t). A representation regular **at the origin**, obtained by converting the above tensor to Cartesian coordinates, is

    h = 2d Q − (4 f_s + 4s f_ss/3) (x qᵀ + q xᵀ)
             + (8 f_s/3 + 2s f_ss/3) X I + (2 f_ss/3) X x xᵀ,
    d = f + 8s f_s/3 + 2s² f_ss/3.

For flat lapse one and zero shift, a vacuum transverse-traceless perturbation obeys the Cartesian wave equation. Its radial component closes on f_tt = L″+6L′/r = 14 f_s + 4s f_ss. The radial physical tidal curvature is R₀ᵣ₀ᵣ=−f_tt Y, and generally **does not vanish** even while the Hamiltonian and momentum constraints are both zero. For local polynomial data f(s,0)=1−2s+s², f_t(s,0)=1+s/3, the recursion in time terminates. At the origin and t=0 the tidal matrix is 28 Q. Direct Cartesian differentiation verifies the tensor wave equation component by component without using the radial constraint observer. As non-vacuum numerical controls, adding an independent conformal metric perturbation 2s²I gives nonzero linear scalar curvature −80s, and adding sI to the extrinsic curvature gives nonzero momentum −4x. [Exact witness](evidence-001.zip) (archive member: `tensor_identity.py`). These local manufactured fields are not isolated finite-energy galaxy preparations.

## Reading the actual material runs

The two evolutions (order 12 and order 20) have the same signed preparation and the same curved monopoles. At a saved instant independently evaluate both complete right-hand sides, form their difference, and read ΔL̈=−ΔK̇/3−ΔṠ from the trace and shear evolution. Without using that acceleration as an input, predict the radial principal part from the two geometry profiles:

    a [ A₂₀ (L₂₀−L₁₂) + (A₂₀−A₁₂)L₁₂ ],       a=exp(−2ℓ₀).

These are propagation of the accumulated change and the continuous forcing due to the choice of numerical operator, respectively. The remaining primary chart term is a[2D_back(r_f ΔM_f)−D_back D_face(r²ΔT)]/r². Background curvature, time-dependent geometry, material stress, and other non-principal terms are not presumed absent. Test each term and their sum on both signs and matter branches, compare signed and shared states separately and retain differences in core and bulk. This instantaneous test of the numerical radial dynamics is not an identification of every perturbation in the actual host with a vacuum gravitational wave; nor does it derive a new physical source of gravitational radiation.
