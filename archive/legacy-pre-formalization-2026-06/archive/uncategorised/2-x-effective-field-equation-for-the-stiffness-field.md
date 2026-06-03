2.X Effective field equation for the stiffness field
===================================================

We treat the galactic stiffness as an effective static scalar field
m(x) governed by a baryon-sourced relaxation equation rather than as a
free screened Yukawa field. The baryonic loading field is defined from
the baryonic gravitational potential Φ_b through

    ∇²Φ_b = 4πGρ_b,
    g_b(x) = |∇Φ_b(x)|,

or, in the rotation-curve representation,

    g_b(r) = V_b(r)^2 / r.

We then define a local baryonic target stiffness

    m_targ(x) = m_0 [ g_b(x) / g_* ]^γ,

where m_0 is a stiffness scale, g_* is a reference acceleration, and γ
is the baryonic coupling exponent.

The effective stiffness field is taken to minimize the static
functional

    F[m] = ∫ d^3x [ (ℓ^2/2) |∇m|^2 + (1/2)(m - m_targ)^2 ],

where ℓ is the spatial coherence length of the stiffness field. Varying
this functional with respect to m gives

    ℓ^2 ∇^2 m - m + m_targ = 0.

Under spherical symmetry this becomes

    ℓ^2 (1/r^2) d/dr [ r^2 dm/dr ] - m(r) + m_targ(r) = 0,

with

    m_targ(r) = m_0 [ g_b(r) / g_* ]^γ.

The cumulative stiffness is then

    S(r) = ∫_0^r m(s) ds,

and the normalized rotation curve is generated through the saturation
law

    V(r)/V_inf = 1 - exp[-S(r)/S_c].

This closes the effective galaxy-scale theory:

    baryons → target stiffness → smoothed stiffness field
            → cumulative stiffness → rotation curve


------------------------------------------------------------
2.X WEIGHTED CUMULATIVE FIELD EQUATION
------------------------------------------------------------

The SPARC tests indicate that the cumulative stiffness budget is not
accumulated in the simple Euclidean radial measure dr, but in a mildly
weighted radial measure of the form

    dμ_r = r^κ dr.

The cumulative stiffness field is therefore defined by

    S(r) = ∫_0^r s^κ m(s) ds.

Differentiating gives

    dS/dr = r^κ m(r).

Define the weighted radial operator

    D_κ = r^(−κ) d/dr,

so that

    D_κ S = m.


------------------------------------------------------------
2.X.1 Green-kernel representation
------------------------------------------------------------

    S(r) = ∫_0^∞ G_κ(r,s) m(s) ds

    G_κ(r,s) = H(r−s) s^κ

For κ = 0:

    S(r) = ∫_0^r m(s) ds

For κ ≈ −0.2:

    G(r,s) = H(r−s) s^(−0.2)


------------------------------------------------------------
2.X.2 Effective accumulation coordinate
------------------------------------------------------------

    u(r) = ∫_0^r s^κ ds

    u(r) = r^(1+κ)/(1+κ),    κ ≠ −1

    S(r) = ∫_0^{u(r)} m(u) du

    dS/du = m

For κ ≈ −0.2:

    u(r) = r^0.8 / 0.8


------------------------------------------------------------
2.X.3 Coupling to baryonic field
------------------------------------------------------------

    m(r) = ( g_b(r) / g_* )^γ

    g_b(r) = V_b(r)^2 / r

    dS/dr = r^κ ( g_b(r) / g_* )^γ

For fitted values:

    κ ≈ −0.2
    γ ≈ 0.34

    dS/dr = r^(−0.2) ( g_b(r) / g_* )^0.34


------------------------------------------------------------
2.X.4 Response law
------------------------------------------------------------

    V(r)/V_inf = 1 − exp[−S(r)/S_c]

Full system:

    m(r) = ( g_b(r) / g_* )^0.34
    dS/dr = r^(−0.2) m(r)
    V(r)/V_inf = 1 − exp[−S(r)/S_c]


------------------------------------------------------------
2.X EFFECTIVE RADIAL GEOMETRY AND FIRST-PRINCIPLES REDUCTION
------------------------------------------------------------

    m(r) = ( g_b(r) / g_* )^γ
    dS/dr = r^κ m(r)

    γ ≈ 0.34
    κ ≈ −0.2

    dμ_r = r^κ dr

    S(r) = ∫_0^r s^κ m(s) ds


------------------------------------------------------------
2.X.1 Effective proper radial coordinate
------------------------------------------------------------

    u(r) = ∫_0^r s^κ ds

    u(r) = r^(1+κ) / (1+κ)

For κ ≈ −0.2:

    u(r) = r^0.8 / 0.8

    dS/du = m


------------------------------------------------------------
2.X.2 Minimal metric ansatz
------------------------------------------------------------

    dℓ^2 = r^(2κ) dr^2 + r^2 dΩ^2

    dΩ^2 = dθ^2 + sin^2θ dφ^2

    du = r^κ dr

    g_rr = r^(2κ)

For κ ≈ −0.2:

    g_rr = r^(−0.4)


------------------------------------------------------------
2.X.3 Variational formulation
------------------------------------------------------------

    I[m,S,λ] = ∫ du [
        A/(1 + 1/γ) m^(1 + 1/γ)
      - Λ g_b(u) m
      + λ(u) ( dS/du - m )
    ]

    dS/du = m

    A m^(1/γ) - Λ g_b - λ = 0

    dλ/du = 0  →  λ = λ_0

    m(u) = [ (Λ g_b(u) + λ_0) / A ]^γ


------------------------------------------------------------
2.X.4 Final tested system
------------------------------------------------------------

    m(r) = ( g_b(r) / g_* )^0.34

    dS/dr = r^(−0.2) m(r)

    V(r)/V_inf = 1 - exp[ -S(r)/S_c ]


------------------------------------------------------------
2.X BACKGROUND RESPONSE FIELD WITH BARYONIC MODULATION
------------------------------------------------------------

    m(r) = m_bg(r) + δm_b(r)


------------------------------------------------------------
2.X.1 Minimal baryonic modulation law
------------------------------------------------------------

    m(r) = m_0 + B ( g_b(r) / g_* )^γ

    g_b(r) = V_b(r)^2 / r

    γ ≈ 0.34


------------------------------------------------------------
2.X.2 Weighted cumulative field equation
------------------------------------------------------------

    S(r) = ∫_0^r s^κ m(s) ds

    dS/dr = r^κ m(r)

    dS/dr = r^κ [ m_0 + B ( g_b(r) / g_* )^γ ]


------------------------------------------------------------
2.X.3 Effective radial geometry
------------------------------------------------------------

    du = r^κ dr

    dS/du = m

    dℓ^2 = r^(2κ) dr^2 + r^2 dΩ^2

For κ ≈ −0.2:

    g_rr = r^(−0.4)


------------------------------------------------------------
2.X.4 Variational formulation
------------------------------------------------------------

    I[m,S,λ] = ∫ du [
        α/2 ( m - m_bg(u) )^2
      - β ( g_b(u) / g_* )^γ m
      + λ(u) ( dS/du - m )
    ]

    dS/du = m

    α ( m - m_bg ) - β ( g_b / g_* )^γ - λ = 0

    dλ/du = 0

    m(u) = m_bg*(u) + B ( g_b(u) / g_* )^γ


------------------------------------------------------------
2.X.5 Final tested system
------------------------------------------------------------

    m(r) = m_0 + B ( g_b(r) / g_* )^0.34

    dS/dr = r^(−0.2) m(r)

    V(r)/V_inf = 1 - exp[ -S(r) / S_c ]
