FIRST-ORDER COVARIANT OVERLAP INVARIANTS
Searching for a linear cosmological growth source
==============================================================

Goal:

Construct a scalar overlap invariant Π such that

    1. Π is covariant
    2. Π couples source and response sectors
    3. Π reduces in the weak-field galaxy limit to something
       proportional to g_b g_obs
    4. δΠ ≠ 0 at linear order around FRW

The previous choice

    Π_old = sqrt[(∇Φ_b)^2 (a_μ a^μ)]

fails condition (4), because both factors vanish in exactly
homogeneous FRW and therefore Π_old begins at quadratic order
in perturbations.

--------------------------------------------------------------
1. GENERAL STRATEGY
--------------------------------------------------------------

To get a nonzero linear perturbation, Π must contain a factor with a
nonzero FRW background value multiplied by a factor with a first-order
perturbation.

Desired structure:

    Π = X_bg · δY  +  Y_bg · δX

rather than

    Π = δX · δY

--------------------------------------------------------------
2. NATURAL BACKGROUND OBJECTS
--------------------------------------------------------------

Nonzero in FRW:

    H               = expansion rate
    θ = ∇_μ u^μ     = expansion scalar = 3H
    ρ_b             = baryon density
    T               = trace of stress-energy
    M̄              = homogeneous memory field
    Ṁ̄             = homogeneous memory time derivative

--------------------------------------------------------------
3. CANDIDATE CLASS A: DENSITY × RESPONSE SCALAR
--------------------------------------------------------------

    ρ_b = T_{μν} u^μ u^ν

    Π_A = ρ_b M

Background:

    Π̄_A = ρ̄_b M̄ ≠ 0

Perturbation:

    δΠ_A = ρ̄_b δM + M̄ δρ_b

--------------------------------------------------------------
4. CANDIDATE CLASS B: DENSITY × EXPANSION
--------------------------------------------------------------

    θ = ∇_μ u^μ

    Π_B = ρ_b θ

Background:

    Π̄_B = 3H ρ̄_b ≠ 0

Perturbation:

    δΠ_B = θ̄ δρ_b + ρ̄_b δθ

--------------------------------------------------------------
5. CANDIDATE CLASS C: SOURCE VECTOR × MEMORY GRADIENT
--------------------------------------------------------------

    s_μ = h_μ^ν ∇_ν ρ_b

    Π_C = s_μ ∇^μ M

    h_{μν} = g_{μν} + u_μ u_ν

Conclusion:

    Not ideal for linear cosmology

--------------------------------------------------------------
6. CANDIDATE CLASS D: MATTER TRACE × MEMORY FIELD
--------------------------------------------------------------

    T = T^μ_μ

For dust:

    T ≈ -ρ_b

Define:

    Π_D = T M

Background:

    Π̄_D = T̄ M̄ ≠ 0

Perturbation:

    δΠ_D = T̄ δM + M̄ δT

--------------------------------------------------------------
7. CANDIDATE CLASS E: EXPANSION-HISTORY ACTIVATION
--------------------------------------------------------------

Define:

    U̇ = H
    U = ln a

    Π_E = ρ_b f(U)

or

    Π_E = ρ_b M f(U)

--------------------------------------------------------------
8. SCIENTIFIC TRIAGE
--------------------------------------------------------------

Best simple first-order candidates:

    Π_D = T M
    Π_A = ρ_b M

Strategy:

    cosmology → first-order Π
    galaxies  → nonlinear Π → g_b g_obs

--------------------------------------------------------------
9. RECOMMENDED NEXT STEP
--------------------------------------------------------------

Choose:

    Π = T M

Action:

    L = √(-g)[
            R/(16πG)
          - 1/2 (∇M)^2
          - a M^4/4
          + b T M^2
          + L_b
        ]

--------------------------------------------------------------
10. CONCLUSION
--------------------------------------------------------------

Original invariant:

    Π_old = sqrt[(∇Φ_b)^2(a_μ a^μ)]

is nonlinear (second order).

To obtain first-order cosmological sourcing:

    Π must include a background term.

Best candidates:

    Π = ρ_b M
    Π = T M

==============================================================
END
==============================================================
