# Extension from circular probes to an equilibrium stellar population
This is an analytic consequence of the same Newtonian equations, not a fitted stream relation. Consider a bounded initial set of stars selected inside radius A, followed as a Lagrangian ensemble. Assume a non-streaming spherical cluster in equilibrium in its own potential before the tide acts; take a spatially uniform linear external tide T=sum T_j across the cluster. The energy E is the specific energy in the cluster alone. Opposite velocities have equal probability. At the initial instant <E_j'>=0 but

    <E_j''>_A = <r²>_A Tr(Tᵀ T_j)/3 + <v² − r Φ_c'>_A Tr(T_j)/3.

This also holds for a spherically symmetric anisotropic velocity dispersion after averaging angular directions. For a stationary spherical system Jeans gives d p_r/dr + 2β p_r/r = −ρ Φ_c'. Integrating after multiplication by 4πr³ gives

    M_A <v² − r Φ_c'>_A = 4π A³ p_r(A).

Thus circular shells in the first test, for which v²=r Φ_c', are special. A subset cut out of an isotropic equilibrium can have a nonzero internal stress term even when not initially streaming. In a positive external source density Tr(T)=−4πGρ_ext, so this term can *reduce* the early energy gain. It is a moment of the initial selection, not mechanical pressure being applied at an artificial wall. For a complete isolated finite distribution with zero outer pressure, only the tensor-square term survives, provided the second moment exists.

For the assumed isotropic Plummer model with length a, ψ=GM/(r²+a²)^(1/2), σ_r²=ψ/6. Define x=A/a and y=x/sqrt(1+x²). Then M_A=M y³,
    
    <r²>_A=3 a² [asinh(x) − y − y³/3]/y³,
    4π A³ p_r(A)/(3M_A) = GM/(6a) (1+x²)^(-3/2).

The untruncated Plummer <r²> diverges logarithmically. One cannot silently use the full-population tensor-square coefficient for that model. A measured outer stellar profile or a physically justified finite selection is needed. Nor does positive E'' prove irreversible heating, escape or late mass loss.

Check the closed expressions against independent radial quadrature of the stellar density and velocity moments and short direct evolution in a frozen *affine* field with the local tidal tensors taken from the saved reset/inherited/ordinary and matched controls. This is a test of the equilibrium/aperture derivation, not a claim that the affine approximation is valid across the actual outer stream. Evaluate apertures at one, two, three scale radii, both total and component work. Retain any discrepancy; do not fit a pressure term or rescale a tide.
