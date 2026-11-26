> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Response of two known microscopic theories

Everything is Euclidean in this derivation. Use W_E=−log Z. Photons are external sources; no photon or graviton loop is being simulated. The reference values are from the Drummond–Hathrell basis in [Bastianelli, Dávila & Schubert](https://arxiv.org/abs/0812.4849), with the sign of the functional accounted for. The following evaluation does **not** insert those coefficients in the loop. The transverse, traceless shear in [the measurement design](DESIGN.md) sets the improvement ξR to zero at one metric insertion for any ξ.

## Scalar

With h₂₂=−h₃₃=h, A₂=A, and no dependence on coordinates 2,3, use W_E=Tr log K for a complex scalar. At flat background K(l)=m²+l². Its single photon, double photon, shear, shear–photon and shear–double-photon vertices are respectively 2e l₂, 2e², −(l₂²−l₃²), −2e l₂ and −2e². The last two are consequences of the same covariant kinetic term. In the trace-log expansion both triangle orderings contribute. The bubble consisting of a shear and a double photon integrates to zero by transverse interchange in the continuum, not necessarily on the link lattice.

With P=p², S=k², Q=q², set z=1−x−y and D=xzP+yzS+xyQ on the unit simplex; put B_p=x(1−x)P on the unit interval. Gaussian integration over the shifted loop, after introducing proper time t, gives the bracket

    −2 + 2∫dx [exp(−t B_p)+exp(−t B_k)] − 4∫dxdy exp(−t D)

under e² exp(−m²t)dt/(4πt)². Its constant vanishes only with the mixed tadpole; its linear term is t(p·k)/3, proportional to the shear Maxwell vertex. Fix/subtract the order-two charge renormalization. With H(X)=(m²+X)log(1+X/m²)−X, the result in units e²/(4π)² is 2∫[H(B_p)+H(B_k)]−4∫H(D). Taylor coefficients follow from exact ∫xᵃyᵇzᶜ=a!b!c!/(a+b+c+2)!, independently of the mesh quadrature. At fourth total momentum order the result in units e²/[(4π)²m²] is

    [2P²+2S²−Q²−PS−PQ−SQ]/90.

It equals Ricci/45 + Weyl/180 − EOM/60 on the shear kinematics (operator *vertices*, not curvature scalars alone). The projections therefore give +1/180. Charge-renormalization or trace terms do not rescue a triangle-only calculation; it returns +7/180 even after removing its own lower powers.

## Dirac fermion

For unit charge normalize the Euclidean propagator as (m−iγ·l)/(m²+l²), {γ_a,γ_b}=2δ_ab, tr 1=4. The linear Dirac vertices are iγ₂A, −i(l₂γ₂−l₃γ₃)h/2 and −iγ₂hA/2. The contracted spin connection and volume variations vanish on this shear; this is not true for an arbitrary metric source. W_E=−Tr log D supplies the closed-fermion-loop sign. There are two mixed bubbles and two orientations of the triangle, not a scalar loop times a spin multiplicity.

To check the trace, in the triangle let a=−xp+yk, b=a+p, c=a−k. The propagator momenta after shifting the integration variable are l+a,l+b,l+c. Bringing the photon matrices together across the first numerator replaces γ·(l+a) by the slash of 2l₂e₂−(l+a). With U=l₂e₂−l₃e₃ the mass trace and four-gamma trace leave after Gaussian averaging a triangle weight −4[(d/2−1)+t(m²+b·c)] under the t⁻ᵈᐟ² measure. Each bubble contributes +2[(d/2−1)+t(m²−B)]. Terms [(d/2−1)+t(m²+D)]exp[−(m²+D)t]/t^(d/2) are total proper-time derivatives. In dimensional regularization, or after consistent local subtraction, they do not supply a fourth-order term. After the Maxwell subtraction the normalized finite result is

    4∫dx [B_p log(1+B_p/m²)+B_k log(1+B_k/m²)]
      + 4∫dxdy (b·c−D) log(1+D/m²).

[spinor.py](evidence-001.zip) (archive member: `spinor.py`) calculates the polynomial moments and integrates the full nonlocal logarithms. The quartic tensor on the deliberately unequal kinematics equals (22 Ricci−2 Weyl−24 EOM)/180. This gives −1/90 in W_E. The simple ratio −2 between the fermion and scalar Weyl coefficients does **not** apply to all terms at finite momentum.

## Independent finite-lattice check

At circumference N and a=1 let b_j=4sin²(l_j/2), G_l=1/(m²+Σ b_j). For a unit y link exp(iA_y), V_A=2sin l₂, V_AA=2cos l₂, V_h=b₃−b₂. The two mixed metric vertices are the corresponding negative photon vertices. If ∑ denotes the normalized periodic momentum sum, the real Fourier coefficient is

    ∑ G_l [−V_AA + V_A²(G_{l+p}+G_{l+k})
              −V_h V_AA G_{l+q} +2 V_h V_A² G_{l+p}G_{l−k}].

No continuum coefficient enters this expression. The independent determinant instead uses a nearest-neighbor two-dimensional difference matrix in coordinates 0,1 for every pair l₂,l₃; its diagonal includes 4exp(−h)sin²[(l₂+A_y)/2]+4exp(h)sin²(l₃/2). Differentiate its log determinant in three real standing-wave amplitudes by alternating the eight signs and then refining the step. This also checks the factor four for the real Fourier readout. The larger grids use the exact Fourier sum at finite cutoff, not the expensive finite differences. The window with mL fixed tests spacing; at fixed am, increasing N and the integer external mode proportionally tests volume at the same physical momentum. Neither result defines an interacting QCD EMT.
