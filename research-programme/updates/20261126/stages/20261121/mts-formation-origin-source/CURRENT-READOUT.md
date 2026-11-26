> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# An independent polar-current measurement from covariant Cartesian fields

The momentum carried by the metric is Dⱼ Kʲᵢ−∂ᵢK. Compare it with the matter covector; do **not** define the metric momentum to equal the matter momentum. We use the saved currents for exactly the corresponding state. This calculation does not change the evolution, solve a constraint, remove cells or replace either accepted proper-aperture observable.

Set s=r², y=xᵀQx, u=Qx and γ=g(I+mxxᵀ), F=1+sm. The background mixed extrinsic curvature is L=kₜI+δk xxᵀ (δk is the radial-minus-tangential eigenvalue divided by s). For h=δγ/g and p=δK_cov/g, the mixed perturbation is M=(I−mxxᵀ/F)(p−hL). Expand M=aQ+b_L xuᵀ+b_R uxᵀ+c yI+d yxxᵀ; b_L and b_R need not coincide. Write the perturbed lower spatial current as Uu+Vy x. Only U contributes to the polar harmonic; its coefficient before ∂θY is sU/2. With z=(log g)_s/2:

    U = 2a_s + 2s(b_L)_s + 2b_L − b_R − 4c − 2s d
      + (4z+F_s/F)(a+s b_L) − (m−2z)(a+s b_R)/F
      − (δk/F)[rr(h) − (1+2sz)(a_h+s b_h)].

The first line is ∂ⱼMʲᵢ−∂ᵢtr M. The next line comes from the background connection acting on M. The last term comes from the varied connection acting on L: its kₜI part cancels, and contraction with xʲxₖ reduces to one covariant derivative of the radial metric component. This is a linearization in quadrupole amplitude, not in the spherical host. [Direct check](evidence-001.zip) (archive member: `polar_cartesian.py`): perturb explicit nonspherical three-dimensional metric and extrinsic-curvature tensors, form the divergence of the mixed tensor and the trace gradient, and extract the tangential component at off-axis points. Neither matter data nor the polar evolution equations enter that check.

The radial derivative part of the measured coefficient is (r a_r+r³(b_L)_r)/2. Thus for a taper W ending at a fixed L, its integral is

    −½ ∫₀ᴸ [(rW)′a + (r³W)′b_L] dr.

There is no origin boundary term for bounded a,b_L. In the quadrature one can subtract any constant from either coefficient in this derivative-only integral since rW and r³W vanish at both endpoints. The remaining undifferentiated terms are integrated as given. Neither the density nor the material current gets such a subtraction. [Weak tests](evidence-001.zip) (archive member: `weak_current.py`) use W=(1−r²/L²)⁶ with and without a radial r² weight, L=.025,.05,.1,.3 in the original radial units. The volume-weighted figures use coordinate r²dr, not a new physical proper-aperture detector. Normalization is ∫W|J|dr. The weak test preserves a deliberately injected nonzero mismatch on a smooth analytic fixture. Comparing midpoint sampling with spline-based interior quadrature is a numerical sensitivity test, not a proof of convergence at r=0.
