# A source prediction from radial momentum balance

This is a local consistency test of the retained Einstein-limit evolution, not a new field inserted into the action. Compare with the original time-integrated normal-expansion prediction. Set κ=4πG, α=a exp(U), ℓ=a exp(−V), x=U', y=V', A=1/r, Π=P_r−P_t. All E and P in the following identities include the background, and a vacuum term can be included as energy with P=−E. j is the covariant radial ADM momentum, not orthonormal momentum.

The gravitational starting equations use the standard [3+1 Einstein and matter formulation](https://arxiv.org/abs/gr-qc/0703035). Starting with ∇μ T^μ_r=0 for a spherical source, use the mixed-index balance in coordinate volume, ∂μ(√−g T^μ_r)=½√−g T^{μν}∂_r g_{μν}. The time momentum density is ℓ³r² j; the flux is αℓ³r² P_r (a common sin θ was removed). Expanding the derivative gives

    ∂η j = −3(∂η ln ℓ)j − α [ P_r' + x(E+P_r) + 2(A−y)Π ].

Independently put D=(x−y)A+y²/2−xy. On a shear-free slice h'=κj. The previously tested trace law for total h has right-hand side T=α[−3h²/2−κP_r+D/ℓ²]. The Hamiltonian and trace-free equations give

    y' = ℓ²(κE−3h²/2) + y²/2 −2Ay,
    x' = y' + (x−y)A + y² −2xy − x² −2κℓ²Π .
    D'+(x+2y)D = ℓ² [ x(3h²/2−κE) − 2κ(A−y)Π ].

Consequently T' is κ times the radial momentum evolution with ∂η ln ℓ replaced by αh. The symbolic check uses independent variables, not a physical trajectory. In particular pressure gradients and anisotropy cannot generally be replaced by one scalar effective force.

**Forecast without examining a fitted residual.** If smooth matter is treated as uniform with no radial current or pressure gradient, the explicit streams/wave omit its Euler acceleration. Relative to the independent trace, the predicted contribution to (measured minus predicted) over [lo,hi] in time is

    ∫ κ a (E_s+P_s) [exp U(hi)−exp U(lo)] dη.

Use 2κ(E_s+P_s)=−2 Ḣ−Σ c_dust/a³−c_wave |p_bg|²/a³ from the *existing* flat-FLRW table; the H derivative uses the previously frozen logarithmic step. This is a prediction of a bias from the homogeneous prescription, not evidence for a new component or an extra free coupling. A second independently observable contribution is ∫3(V_η−Vkin) dh dη, where Vkin=a(H−Nh). The projected stream error and any scalar discretization errors are still separate. Do not subtract these predictions to announce a passing physical trajectory.

**What a pressure-only repair would cost.** For zero j_s and spatially uniform E_s, an independently conserved isotropic source requires (E_s+P_s)N=E_s+P_s,bg from the radial equation and N(L)=1. Its normal energy equation also requires ∂η E_s+3(∂η ln ℓ)(E_s+P_s)=0. With separate background conservation these imply (∂η ln ℓ)/N=aH wherever the background enthalpy is nonzero. With the metric kinematics enforced that means h=H and thus zero *total* j there. A nonvacuum, motionless, separately conserved uniform density is therefore not an exact physical completion across a region carrying total radial current. A vacuum constant is exempt; permitting density perturbations, current, anisotropy or a derived exchange changes the hypotheses. This is a conditional incompatibility, not an exclusion of the retained parent action.
