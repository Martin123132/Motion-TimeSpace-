# Exterior launch tide: a bound for any balanced rotation, not just our three shapes
**Statement.** In the retained extremal charged, scalar-free spherical background with the matched conformal release, zero free even metric/momentum data and no applied exterior tide, let the conserved spin profile be any smooth, regular ℓ(N) of finite launch kinetic cost W. Assume compact baryons on [0,S], J(N)=∫₀ᴺ ℓ dN, J(M)=0. Use the parent's geometrical units, unspun areal radius and per-squared-spin perturbations. The launch pole-minus-equator radial curvature on a physically round sphere R≥S is nonnegative, and is bounded by an explicit constant times W S²/R⁵. This is not a statement about the full time-dependent volume, general gravitational initial data, non-axisymmetric rotation, an arbitrary scalar potential, or nonlinear large spin.

**1. Eliminate the unknown angular-momentum profile from a source norm.** Work in L²(dN), fₗ=ℓ/r, so ‖fₗ‖²=3W. Define A(r)=∫₀ᴺ⁽ʳ⁾ r(N')² dN'. Balance means ⟨fₗ,r⟩=0. Project r 1_{[0,r]} orthogonally to r before applying Cauchy–Schwarz. This gives
    J(r)² ≤ 3W A(r)[1−A(r)/A(S)].
It is the sharp pointwise Hilbert-space bound (the extremizer may be approximated by smooth profiles); separate maximizers at different radii need not coincide. The extremal background has b=√f=1−N/r; N≤min(D₀ r³/3,M). Therefore b≥b₀=1−(D₀ M²/3)^(1/3)>0 everywhere. With d=Db and the retained S₂=(4J²/r⁶+dℓ²/r²)/6,
    I₂=∫₀ˢ r² S₂/b dr = W/2 + (2/3)∫₀ˢ J²/(b r⁴)dr,
    W/2 ≤ I₂ ≤ C W,    C=1/2 + D₀ S²/(5 b₀).
The last conservative number uses A≤D₀r⁵/5; the preceding projected bound permits a tighter integral for a known density. No assumption about the sign of ℓ, its number of reversals or its membership in our source basis enters.

**2. Control the elliptic response at the emitter edge.** Write the regular, decaying parent problem as L u=−r²S₂/b, with L=−(r²b u')'+q u and q=(6+r²d+N²/r²)/b≥6. The inverse is positive: the regular left and decaying right homogeneous solutions can be chosen positive, with the left solution increasing since (r²b y')'=q y. For r≤S, 0≤G(S,r)≤G(S,S). The energy form dominates b₀ times the flat quadrupole form ∫[r²y'²+6y²]dr. By the variational characterization G(S,S)=sup y(S)²/⟨y,Ly⟩, the diagonal is at most 1/(5 S b₀): in flat space the regular and decaying solutions are r²,r⁻³ and the diagonal is exactly 1/(5S). Thus 0≤−u(S)≤CW/(5 S b₀). These bounds concern the continuum; finite-grid checks are separate.

**3. Propagate the bound with the correct radial power.** Exterior b_R=1−M/R, f=b_R², q=(6+M²/r²)/b. The logarithmic derivative of the decaying exterior solution is fixed independently of the source. Its exterior Dirichlet-to-Neumann coefficient at R is
    γ_R=−R² b_R u'(R)/u(R)=inf_{y(R)=1}∫_R^∞ [r²b y'²+q y²]dr.
The flat infimum is 3R, attained by (R/r)³. On [R,∞) the form lies between b_R and k_R=(1+M²/(6R²))/b_R times the flat form. Hence
    3/R ≤ −u'/u ≤ 3 k_R/(R b_R).
Integrating the lower bound gives −u(R)≤[CW/(5 S b₀)](S/R)³. At a matched, physically round release sphere the parent Gauss-equation result reduces to
    ΔE_R=(3/2){4 f u'/R−[12/R²+4M/R³−4M²/R⁴]u}.
Here E=R_(nR nR); positive ΔE means *more negative relative radial acceleration* at the pole, not extra outward acceleration. Together,
    0 ≤ ΔE_R ≤ (3 C W S²)/(10 b₀ R⁵) [12+4M/R−4M²/R²+12 b_R k_R].
It vanishes for the empty rotational perturbation. No claim that this conservative upper bound is saturated. In particular, equal W, equal mass and equal net angular momentum do not fix the tide.

**4. Relate cost to an asymptotic measurement if it exists.** The retained minimal spin-cost calculation (cited in the parent CONSTRAINT-AND-RULER note) gives δADM=(2/3)∫[αDℓ²/2+2F J²/r⁴]dr, F positive. Thus δADM≥α_min W, not δADM=W. On the static extremal background (ln α)'=(m+r³p_r)/(r²f)=N/(r²b), normalized by α(S)=1−M/S. A certified lower bound on the central lapse is α₀=(1−M/S)exp[−D₀S²/(6b₀)]. Consequently one may replace W in the upper bound by an independently bounded spin-added ADM energy divided by α₀. An unspun reference with the same material preparation is required; merely measuring the total galaxy mass is not such a measurement. In SI, W_phys is an energy in joules and measured radial relative acceleration per displacement is c²E/L*²: the far-zone dimensional scale is (G W_phys/c²) S_phys²/R_phys⁵. This establishes the Newtonian quadrupolar radial falloff as a **bound** for this source class without selecting a rotation law or calibrating to a tide.
