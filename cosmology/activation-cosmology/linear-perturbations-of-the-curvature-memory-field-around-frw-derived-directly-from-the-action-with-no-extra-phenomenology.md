LINEAR PERTURBATIONS OF THE CURVATURE–MEMORY FIELD AROUND FRW
Derived directly from the action, with no extra phenomenology
==============================================================

We adopt signature (-,+,+,+) and write the action as

    S = ∫ d^4x √(-g) [

            R/(16πG)
          - 1/2 g^{μν} ∂_μ M ∂_ν M
          - a M^4 / 4
          + b Π M
          + L_b

        ].

Here

    M(x)   = curvature–memory scalar
    a      = quartic self-interaction
    b      = overlap coupling
    Π      = source–response overlap invariant
    L_b    = baryonic matter Lagrangian.

The overlap invariant used in the toy model is

    Π = [ (∇_μ Φ_b ∇^μ Φ_b) (a_ν a^ν) ]^(1/2),

where

    Φ_b    = baryonic potential
    a_μ    = u^ν ∇_ν u_μ

is the four-acceleration of the chosen observer congruence.

--------------------------------------------------------------
1. BACKGROUND FRW EQUATIONS
--------------------------------------------------------------

Take a spatially flat FRW background

    ds^2 = -dt^2 + A(t)^2 δ_{ij} dx^i dx^j

with Hubble rate

    H = Ȧ / A.

Assume the homogeneous background field

    M(t,x) = M̄(t).

For exactly homogeneous FRW,

    ∂_i Φ_b = 0
    a_μ = 0

so

    Π̄ = 0.

Hence the background memory-field equation is

    M̈̄ + 3H Ṁ̄ + a M̄^3 = 0.

The background energy density and pressure of the memory field are

    ρ̄_M = 1/2 Ṁ̄^2 + a M̄^4 / 4
    p̄_M = 1/2 Ṁ̄^2 - a M̄^4 / 4.

The Friedmann equations are

    3H^2 = 8πG ( ρ̄_b + ρ̄_M )

    2Ḣ + 3H^2 = -8πG ( p̄_b + p̄_M ).

--------------------------------------------------------------
2. SCALAR PERTURBATIONS IN NEWTONIAN GAUGE
--------------------------------------------------------------

Perturb the metric in Newtonian gauge:

    ds^2 = -(1+2Ψ) dt^2 + A(t)^2 (1-2Φ) δ_{ij} dx^i dx^j.

Perturb the memory field and baryons as

    M(t,x) = M̄(t) + δM(t,x)

    ρ_b(t,x) = ρ̄_b(t) + δρ_b(t,x)

and introduce the baryon velocity divergence θ_b in Fourier space.

--------------------------------------------------------------
3. CRUCIAL FACT: Π VANISHES AT LINEAR ORDER
--------------------------------------------------------------

Because the FRW background is homogeneous:

    ∂_i Φ̄_b = 0
    ā_μ = 0

Thus

    Π̄ = 0
    δΠ = 0

at linear order.

Leading contributions:

    ∇_μ Φ_b ∇^μ Φ_b
      = A^(-2) δ^{ij} (∂_i δΦ_b)(∂_j δΦ_b)

    a_μ a^μ
      = A^(-2) δ^{ij} (∂_i Ψ)(∂_j Ψ)

Hence

    Π = O[ (∂δΦ_b)(∂Ψ) ]

So Π enters only at second order and higher.

--------------------------------------------------------------
4. LINEAR MEMORY-FIELD EQUATION
--------------------------------------------------------------

    □M + a M^3 = b Π

At linear order:

    δM̈ + 3H δṀ + (k^2/A^2 + 3a M̄^2) δM
      = Ṁ̄ ( Ψ̇ + 3Φ̇ ) - 2 a M̄^3 Ψ

Effective mass:

    m_eff^2 = 3a M̄^2

--------------------------------------------------------------
5. LINEAR STRESS–ENERGY OF THE MEMORY FIELD
--------------------------------------------------------------

    δρ_M = Ṁ̄ δṀ - Ṁ̄^2 Ψ + a M̄^3 δM

    δp_M = Ṁ̄ δṀ - Ṁ̄^2 Ψ - a M̄^3 δM

    δq_M = - Ṁ̄ δM

    π_M = 0

No anisotropic stress at linear order.

--------------------------------------------------------------
6. LINEARIZED EINSTEIN EQUATIONS
--------------------------------------------------------------

(00):

    (k^2/A^2) Φ - 3H ( Φ̇ + H Ψ )
      = 4πG ( δρ_b + δρ_M )

(0i):

    Φ̇ + H Ψ
      = 4πG [ ρ̄_b v_b + Ṁ̄ δM ]

(ii):

    Φ̈ + H( Ψ̇ + 3Φ̇ ) + (2Ḣ + 3H^2) Ψ
      - (1/3)(k^2/A^2)(Φ - Ψ)
      = 4πG δp_M

(i≠j):

    Φ - Ψ = 0

--------------------------------------------------------------
7. BARYON PERTURBATION EQUATIONS
--------------------------------------------------------------

    δ̇_b = - θ_b + 3 Φ̇

    θ̇_b + H θ_b - (k^2/A^2) Ψ = 0

Combined:

    δ̈_b + 2H δ̇_b - (k^2/A^2) Ψ
      = 3 ( Φ̈ + 2H Φ̇ )

--------------------------------------------------------------
8. SUBHORIZON QUASI-STATIC LIMIT
--------------------------------------------------------------

    (k^2/A^2) Φ ≈ 4πG ( δρ_b + δρ_M )

Growth equation:

    δ̈_b + 2H δ̇_b
      ≈ 4πG [ ρ̄_b δ_b + δρ_M ]

--------------------------------------------------------------
9. SCIENTIFIC CONSEQUENCE
--------------------------------------------------------------

At linear order:

    • background FRW is nontrivial
    • perturbations behave as canonical scalar
    • Π contributes only at second order

No automatic ε-like growth source at linear level.

--------------------------------------------------------------
10. WHAT THE THEORY PREDICTS
--------------------------------------------------------------

    background → quartic scalar field

    linear perturbations → canonical scalar with

        m_eff^2 = 3a M̄^2

    nonlinear regime → Π-activated transport

--------------------------------------------------------------
11. NEXT STEP
--------------------------------------------------------------

    • derive second-order perturbations, or
    • modify overlap invariant to activate at first order

==============================================================
END
==============================================================
