# Transport, rather than setting constraints to zero

Use geodesic unit lapse/zero time shift and the retained even quadrupole, with angular harmonic Y, ΔΩY=−6Y, Y_AB=D_A D_B Y+3Ω_AB Y. The spherical spatial metric is A²dr²+B²dΩ². The perturbation has h_rr=2A²ℓY, h_rA=B²(v/r)D_A Y and h_AB=B²(2bΩ_AB Y+dY_AB). Dots mean proper-time derivatives. The orthonormal radial direction is normal to the angular spheres. Set L=B'/B, α=B/(rA). These formulas retain terms linear in the angular harmonic on an arbitrary spherical background, not just an expansion about Minkowski space.

## Scalar and spatial Einstein tensor

For J=−h/2 define m=rA (div J−grad tr J)_n and β=B (div J−grad tr J)_angular (coefficient of D_A Y). Then
```
u = ℓ+2b;      m = 2r b'+2rL(b−ℓ)+3v;
β = −(B/2A)[(αv)'+3Lαv]+ℓ+b+d .
```
For ℓ=2 angular order this is locally invertible: recover b algebraically, then v from m and d from β, using radial differences only. Neither m nor β is set to zero. Varying spatial scalar curvature gives
```
R₂ = −2 R̄_nn ℓ −4 R̄_perp b −2[(B² m/(rA))'/(AB²) − 6β/B²] .
```
This is the covariant first variation −Ric:h−2 div(div J−grad tr J). Radial Gauss gives X=G_nn=−R_sphere/2 + k²/4 at this angular order, where k₀=2L/A and k₂=(2b'+6v/r−2Lℓ)/A. Thus X₀=−1/B²+k₀²/4, X₂=−(4b+6d)/B²+k₀k₂/2. Let p=−R/6, s=X−p, C and T the mixed and angular trace-free coefficients of the spatial Einstein tensor. Its two contracted Bianchi equations give
```
6 C₂/B = (X₂'−ℓX₀')/A + (3/2)(k₀ s₂+k₂ s₀);
2 T₂ = B(C₂'+3L C₂)/A + p₂−s₂/2−3s₀ℓ/2 .
```
These determine the remaining curvature components locally; they introduce no matter coupling. Normal/tangential components are in the perturbed orthonormal frame, not bare coordinate components. Below, the independent metric oracle differentiates the coordinate metric, not these formulas.

## Flat master system and stress source

Define p=(ℓ,u,m,β) and use its true velocity. For flat A=1,B=r the radial Ricci identity and metric kinematics give, with D₇=∂²_r+6∂_r/r,
```
R = −2[(rm)'−6β]/r²;
ℓ̈ = D₇ℓ + [2(rm)'−(r²u)'']/r² + S_nn + (E−S)/2;
ü = −R + (3E−S)/2;
m̈ = −r R'/2 + r[E'−(div S)_r];
β̈ = −R/2 + E−r(div S)_θ .
```
E and S are the common-metric energy density and trace of the spatial stress, in the retained 8πG-normalized equations. The factors come from the sourced ADM equation K̇_ij=Ric_ij−S_ij+g_ij(S−E)/2 around Minkowski. When Ė=−div j, j̇=−div S, both Ḣ=−2 div M and Ṁ=−grad H/2 follow with H=R−2E and M the geometric momentum minus j. Equal face fluxes are required, not a refit. When stress is not conserved, the corresponding material residual belongs on the right hand side; it must not be hidden by evolving a sourceless constraint in its place.

At the centre the regular chart has m(0)=0. The shell-volume finite-volume differences are used consistently on both sides. The physical tensor branch has u=m=β=0 and arbitrary smooth ℓ satisfying ℓ̈=D₇ℓ, with v=ℓ+rℓ'/3 and d=r v'/2−ℓ/2+3v/2. Its discrete positive energy is half the sum of V₆ℓ̇² and r_face⁶(Dℓ)² times the grid spacing. The scalar constraint itself obeys the angular-order-two radial wave equation. These are distinct branches, not a projection to zero curvature. A standing tensor wave of independently specified frequency tests both time evolution and normalization. Neumann outer faces are used only in the closed-domain controls.

## Curved current kinematics

Let K₀ be the spherical expansion trace, s₀ the radial trace-free extrinsic curvature and P₀=s₀−2K₀/3. With δK=−u̇, s₂=2(ḃ−ℓ̇)/3, c₂=−αv̇/2, t₂=−ḋ/2, define J_g=div K−grad K (no matter subtraction). Then
```
rA δJ_g,n = ṁ + U_r ;
U_r = −2r L̇(b−ℓ) −rℓ P₀' +3r s₀(b'+3v/r−ℓ L).
B δJ_g,θ = β̇ + U_θ ;
U_θ = ½ (B/A)̇[(αv)'+3Lαv] + ½(B/A)[(α̇v)'+3L̇αv+3Lα̇v] − 3s₀ℓ/2 .
```
The coordinate radial current additionally includes rAℓ J_g,n0. With H_g=R+K²−K_ij K^ij, the geometrical coordinate momentum obeys J̇_g,i=K J_g,i−∂_i H_g/2+∂_i E−D_j S^j_i in sourced ADM. Matter's actual j̇_i must be tested against K j_i−D_j S^j_i, not used to force this comparison to pass. These formulas specify where background work, local stress and environmental momentum enter once the spherical background varies in space and time.
