ANALYTIC BACKGROUND SOLUTIONS FOR THE HOMOGENEOUS MEMORY FIELD
==============================================================

We start from the homogeneous FRW background equation derived from the
action with interaction term b T M^2.

For pressureless matter (dust),

    T = -ρ_b

so the background memory-field equation is

    M̈ + 3H Ṁ + a M^3 + 2 b ρ_b M = 0.

This can be written as

    M̈ + 3H Ṁ + dV_eff/dM = 0

with effective potential

    V_eff(M,a_cos)
      = a M^4 / 4 + b ρ_b(a_cos) M^2

    ρ_b(a_cos) = ρ_b0 a_cos^(-3)


--------------------------------------------------------------
1. EFFECTIVE MASS
--------------------------------------------------------------

    m_eff^2(a_cos) = 2 b ρ_b(a_cos)

    m_eff^2(M,a_cos) = 3 a M^2 + 2 b ρ_b(a_cos)


--------------------------------------------------------------
2. e-FOLD FORMULATION
--------------------------------------------------------------

    N = ln a_cos

    d/dt = H d/dN

    M̈ = H^2 M'' + Ḣ M'

    M'' + (3 + Ḣ/H^2) M'
        + (a/H^2) M^3
        + (2 b ρ_b/H^2) M
        = 0


--------------------------------------------------------------
3. MATTER-DOMINATED ERA
--------------------------------------------------------------

    H^2 = (8πG/3) ρ_b

    Ḣ/H^2 = -3/2

    ρ_b/H^2 = 3/(8πG)

So

    M'' + (3/2) M'
        + (a/H^2) M^3
        + (3b/(4πG)) M
        = 0


--------------------------------------------------------------
3.1 LINEARIZED SOLUTION
--------------------------------------------------------------

If quartic term negligible:

    M'' + (3/2) M' + μ^2 M = 0

    μ^2 = 3b/(4πG)

Characteristic equation:

    r^2 + (3/2) r + μ^2 = 0

    r_± = -3/4 ± sqrt(9/16 - μ^2)

Solution:

    M(N) = C_+ exp(r_+ N) + C_- exp(r_- N)

    M(a_cos) = C_+ a_cos^(r_+) + C_- a_cos^(r_-)


--------------------------------------------------------------
3.2 WEAK COUPLING LIMIT
--------------------------------------------------------------

If μ^2 << 1:

    r_+ ≈ - (2/3) μ^2
    r_- ≈ -3/2 + (2/3) μ^2

    M_fast ∝ a_cos^(-3/2)
    M_slow ∝ a_cos^(-(2/3) μ^2)


--------------------------------------------------------------
4. QUARTIC-DOMINATED REGIME
--------------------------------------------------------------

If

    a M^2 >> 2 b ρ_b

then

    M̈ + 3H Ṁ + a M^3 = 0

Oscillatory regime:

    w_M = 1/3
    ρ_M ∝ a_cos^(-4)

    M_amp ∝ a_cos^(-1)


--------------------------------------------------------------
5. LATE-TIME Λ-DOMINATED ERA
--------------------------------------------------------------

    H → const
    ρ_b → 0

    M̈ + 3H Ṁ + a M^3 = 0


--------------------------------------------------------------
5.1 FROZEN REGIME
--------------------------------------------------------------

If friction dominates:

    3H Ṁ >> a M^3

    3H Ṁ + a M^3 ≈ 0

Solution:

    1/M^2 = (2a / 3H) t + const

    M(t) ≈ [ (2a / 3H) t + const ]^(-1/2)


--------------------------------------------------------------
5.2 CONSTANT SOLUTION
--------------------------------------------------------------

Exact constant requires:

    Ṁ = 0
    M̈ = 0

    a M^3 = 0

    M = 0

So nonzero field is only approximately frozen.


--------------------------------------------------------------
6. BACKGROUND SCALE FOR GALAXIES
--------------------------------------------------------------

Relevant quantities:

    M̄(a_cos)
    m_eff^2 = 3 a M̄^2 + 2 b ρ_b

Key behaviour:

    • slow decay during matter era
    • near-freezing at late times


--------------------------------------------------------------
7. MATCHING FORM
--------------------------------------------------------------

    M̄(a_cos) ≈ M_* a_cos^(-s)

    M̄(t) ≈ [α t + β]^(-1/2)

    s = (2/3) μ^2 = b/(2πG)


--------------------------------------------------------------
8. EFFECTIVE NEWTON CONSTANT
--------------------------------------------------------------

    G_eff(k,a_cos) = G [1 + β(k,a_cos)]

    β(k,a_cos)
      = b M̄^2
        - 2 b M̄ (a M̄^3 + 2 b ρ̄_b M̄)
          /(k^2/A^2 + m_eff^2)

    m_eff^2 = 3 a M̄^2 + 2 b ρ̄_b


--------------------------------------------------------------
9. GALAXY ACCELERATION SCALE
--------------------------------------------------------------

    g_†^2 ~ (a/b) M̄^3

    g_†(a_cos) ~ (a/b)^(1/2) M̄^(3/2)

If

    M̄ ∝ a_cos^(-s)

then

    g_† ∝ a_cos^(-3s/2)


--------------------------------------------------------------
10. SCIENTIFIC CONSEQUENCES
--------------------------------------------------------------

    • slow evolution of M̄
    • evolving G_eff
    • evolving galaxy acceleration scale
    • testable drift in BTFR / RAR normalization


--------------------------------------------------------------
11. NEXT STEP
--------------------------------------------------------------

    1. fix sign/magnitude of b
    2. identify growth-enhancing vs suppressing branch
    3. insert M̄(a_cos) into β(k,a_cos)
    4. solve δ_b(a_cos,k)
    5. compare with fσ8, S8, DESI, Pantheon

==============================================================
END
==============================================================
