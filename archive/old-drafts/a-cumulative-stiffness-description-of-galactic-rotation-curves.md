A Cumulative-Stiffness Description of Galactic Rotation Curves
=============================================================

Author: Martin Ollett
Year: 2026

------------------------------------------------------------
ABSTRACT
------------------------------------------------------------

We investigate a cumulative-stiffness description of galactic
rotation curves in which the gravitational response is governed not
primarily by Euclidean radius, but by an accumulated baryonic
stiffness coordinate

    u(r) = ∫_0^r m_b(s) ds,

with baryonic loading field

    m_b(r) = ( g_b(r) / g_* )^γ,
    g_b(r) = V_b(r)^2 / r.

The normalized rotational velocity is taken to follow exponential
saturation in a cumulative response field S(r),

    V(r)/V_inf = 1 − exp[−S(r)].

The central empirical result of the SPARC tests is that when the
response is expressed in the baryonic stiffness coordinate u, the
field becomes nearly linear:

    S(u) ≈ C + A u,

with median linear-fit goodness

    R^2 ≈ 0.999

across the working sample.

This implies that the previously inferred weighted radial operators
and nonlocal kernel reconstructions are effective r-space
representations of a simpler underlying accumulation law in source
coordinate.

Normalizing by the turnover-scale stiffness budget u(R_s) yields the
zero-free-parameter response law

    S(r) = u(r) / u(R_s),

and therefore

    V(r)/V_inf = 1 − exp[−u(r)/u(R_s)].

When tested directly against the validated pooled galaxy master curve,
this parameter-free model gives pooled stretched-exponential fit
parameters

    ν ≈ 0.961,
    x_0 ≈ 0.979,

close to the empirical target values

    ν ≈ 0.953,
    x_0 ≈ 1.003.

------------------------------------------------------------
1. INTRODUCTION
------------------------------------------------------------

Galaxy rotation curves exhibit a characteristic universal structure
when scaled by the asymptotic velocity V_inf and turnover radius R_s.

Empirically, normalized rotation curves collapse onto a stretched
exponential master curve

    V(r)/V_inf = 1 − exp[−(r/(R_s x_0))^ν].

The origin of this functional form is usually treated as empirical.

In this work we show that the same structure emerges naturally from a
cumulative-stiffness description of gravity in which the relevant
coordinate is not radius alone, but the accumulated baryonic loading
budget

    u(r) = ∫_0^r m_b(s) ds.

Within this framework the galaxy response field S is found to be
approximately linear in u, and the observed rotation-curve master
curve follows from exponential saturation of that accumulated response.

------------------------------------------------------------
2. THEORY
------------------------------------------------------------

2.1 Baryonic stiffness loading

    m_b(r) = ( g_b(r) / g_* )^γ

    g_b(r) = V_b(r)^2 / r

    u(r) = ∫_0^r ( g_b(s) / g_* )^γ ds

2.2 Response field

    V(r)/V_inf = 1 − exp[−S(r)]

2.3 First-principles reduction

    S(u) ≈ C + A u
    dS/du ≈ const

    S(r) = u(r) / u(R_s)

    V(r)/V_inf = 1 − exp[−u(r)/u(R_s)]

2.4 Relation to master curve

    V(r)/V_inf = 1 − exp[−(r/(R_s x_0))^ν]

2.5 Differential form

    dS/dr = ( g_b(r) / g_* )^γ / u(R_s)

------------------------------------------------------------
3. EARLIER EFFECTIVE DESCRIPTIONS
------------------------------------------------------------

    S(r) = ∫_0^r m(s) ds

    S(r) = ∫_0^r s^κ m(s) ds

    γ ≈ 0.34
    κ ≈ −0.2

    dS/du ≈ const

------------------------------------------------------------
4. DATA
------------------------------------------------------------

SPARC dataset
N = 70 galaxies

------------------------------------------------------------
5. EMPIRICAL TESTS
------------------------------------------------------------

    m_b(r) = ( g_b(r) / g_* )^γ

    S(r) = ∫_0^r s^κ m_b(s) ds

    u(r) = ∫_0^r ( g_b(s) / g_* )^γ ds

------------------------------------------------------------
6. RESULTS
------------------------------------------------------------

Model Results:

    power-law stiffness          ν ≈ 0.940
    density-coupled stiffness    ν ≈ 0.947
    exponential-core stiffness   ν ≈ 0.950

Baryonic loading:

    γ ≈ 0.34

Linear response:

    S(u) ≈ C + A u
    dS/du ≈ const

Zero-parameter model:

    S(r) = u(r) / u(R_s)

    V(r)/V_inf = 1 − exp[−u(r)/u(R_s)]

Fit results:

    ν_pred ≈ 0.961
    x_0_pred ≈ 0.979

------------------------------------------------------------
7. DISCUSSION
------------------------------------------------------------

Hierarchy:

    m_b(r) = ( g_b(r) / g_* )^γ

    u(r) = ∫_0^r m_b(s) ds

    dS/du ≈ const

    S(r) = u(r) / u(R_s)

    V(r)/V_inf = 1 − exp[−S(r)]

------------------------------------------------------------
8. TESTABLE PREDICTIONS
------------------------------------------------------------

    u(r) / u(R_s) is primary organizing variable

    deviations ↔ nonlinearity in S(u)

    dS/du ≈ const

------------------------------------------------------------
9. CONCLUSION
------------------------------------------------------------

Core result:

    u(r) = ∫_0^r m_b(s) ds

    S(u) ≈ C + A u

    dS/du ≈ const

    S(r) = u(r) / u(R_s)

    V(r)/V_inf = 1 − exp[−u(r)/u(R_s)]
