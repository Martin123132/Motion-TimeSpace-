# An exact sign for the surviving dipole, and its first correction

This is an analytic statement about the regular *ordinary extremal static branch*, not a sign inferred from the numerical MTS runs. Take η=+1, smooth nonnegative compact density, g=1−N/r>0, no incident external field, zero total canonical spin, and a nonnegative cumulative spin I(N) not identically zero where charge is enclosed. These are conditions on the stationary reference with first-order counterrotation. The primary preparation satisfies them; the second sign-changing I does not. Reversing all layer spins reverses the conclusion.

From α=Fg, (ln F)'=rD/g and N'=r²D, obtain α'=F N/r² and u=α'/α=N/(r²g). The regular homogeneous dipole y=r²c obeys
    T[c]=c''+(4/r+B'/B)c'−(3D/g+6u²)c=0,   c(0)=1, c'(0)=0.
Writing this in divergence form shows c stays positive and nondecreasing. Take z=α³. Differentiating u gives u'=D/g−2u/r+u(rD/g)−u²; B'/B=2u−rD/g. Substitution cancels all density and density-gradient terms:
    T[z]=6u(1/r+u)z,
    [r⁴B(c z'−z c')]'=6r⁴B c z u(1/r+u).
The bracket vanishes at the regular centre. Hence 3u c−c' is nonnegative and becomes strictly positive beyond a nonempty charged interior. The kernel in the signed Green identity is exactly α(3u c−c'), not the difference of two arbitrary fitted response coefficients. The exterior decaying d is positive with d'<0: starting from d~1/r at infinity, (Bd')'=U d>0 preserves these signs inwards. Therefore W=B(y'd−yd')>0. **The stationary exterior magnetic moment is strictly positive despite exactly zero total spin and a vanishing Newtonian dipole for this preparation.** The proof does not require an expansion in compactness and does not hold merely because a time-dependent pulse passed a detector. Its size and unit conversion still require independently specified charge and source rotation.

For a quantitative check, expand the original scale-b family at fixed radius, not at fitted radii. Use the unscaled D,N,I, ν=N/r, L₁=−∫ᵣ⁵sD ds, c=1+b c₁+b² c₂+… and cᵢ(0)=cᵢ'(0)=0. The leading equations are
    (r⁴c₁')'=3r⁴D,
    (r⁴c₂')'=r⁴[3D(c₁+ν)+6N²/r⁴−(2N/r²−rD)c₁'].
At the outer surface the first-order tail normalization d=r⁻¹+3bM/(2r²)+… cancels the explicit B expansion, leaving W₁=3c₁(5)+5c₁'(5). Then
    μ∞=b²μ₂+b³μ₃+O(b⁴),
    3μ₂=∫I[3N/r²−c₁'] dr,
    3μ₃=∫I[3N(L₁+c₁)/r²−c₂'−(L₁−ν)c₁'] dr−W₁μ₂.
For the actual density profile all these integrals are polynomials on [0,5]. Evaluate their coefficients exactly as rationals, comparing against the independent stationary solution without reading any of its moments to set these coefficients. Finite-b numerical checks of size are separate from the analytic sign proof.

