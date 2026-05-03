MTS ACTIVATION COSMOLOGY
Expansion-History Activated Matter Coupling
Tested Against Pantheon+ SH0ES, DESI DR1 BAO, and Gold-2017 Growth Data

Author: Martin Ollett
Year: 2026


------------------------------------------------------------
ABSTRACT
------------------------------------------------------------

We investigate a phenomenological cosmological framework in which the
effective contribution of the matter sector to the expansion history
is modulated by an activation function derived from accumulated
expansion history.

The model modifies the standard Friedmann background through a
multiplicative activation factor g(z) applied to the matter density:

    H(z)^2 = H0^2 [ Ωm (1+z)^3 g(z) + (1 − Ωm) ]

We test several formulations of the activation law using the Pantheon+
SH0ES Type Ia supernova sample (1701 SNe), DESI DR1 baryon acoustic
oscillation measurements, and the Gold-2017 compilation of growth
rate measurements fσ8.

Three representations of the activation behaviour are examined:

1. Empirical redshift activation
2. Expansion-history activation using u = ln(1+z)
3. Equality-tied activation where the activation scale is linked
   to the matter–Λ equality epoch

All forms reproduce nearly identical observational behaviour. The
activation scale inferred from the data corresponds to a redshift

    z_s ≈ 0.21

occurring after matter–Λ equality at

    z_eq ≈ 0.50.

The model improves the expansion-history fit relative to ΛCDM by

    Δχ² ≈ −13

using Pantheon+ and DESI data, and remains consistent with Gold-2017
growth measurements.

These results indicate that late-time expansion behaviour may be
describable through a delayed response to accumulated expansion
history rather than a strictly constant dark energy component.


------------------------------------------------------------
1. INTRODUCTION
------------------------------------------------------------

The standard ΛCDM cosmological model describes the expansion of the
Universe through a constant dark energy density and cold dark matter.

Despite its empirical success, ΛCDM introduces a cosmological constant
whose physical origin remains uncertain.

In this work we investigate an alternative phenomenological
description in which the effective gravitational contribution of
the matter sector evolves through a delayed activation function.

The central idea is that the matter term in the Friedmann equation
is modulated by a dimensionless function g(z) that depends on
cosmological expansion history.

The modified background expansion becomes

    H(z)^2 = H0^2 [ Ωm (1+z)^3 g(z) + (1 − Ωm) ]

When g(z) = 1 the model reduces to ΛCDM.


------------------------------------------------------------
2. ACTIVATION FRAMEWORK
------------------------------------------------------------

We consider an activation function of the form

    g(z) = 1 − exp[ −(u(z))^ν ]

where ν is a shape parameter and u(z) represents accumulated
cosmological expansion history.


------------------------------------------------------------
2.1 Empirical Redshift Activation
------------------------------------------------------------

The original phenomenological form is

    g(z) = 1 − exp[ − ( z / (z_s x0) )^ν ]

where z_s is an activation scale.


------------------------------------------------------------
2.2 Expansion-History Activation
------------------------------------------------------------

A physically motivated loading variable is

    u(z) = ln(1+z)

representing the accumulated logarithmic expansion between
redshift z and the present epoch.

The activation law becomes

    g(z) = 1 − exp[ − ( ln(1+z) / u_s )^ν ]


------------------------------------------------------------
2.3 Equality-Tied Activation Scale
------------------------------------------------------------

Matter–Λ equality satisfies

    Ωm (1+z_eq)^3 = 1 − Ωm

which gives

    u_eq = (1/3) ln( (1 − Ωm) / Ωm )

The activation scale is parameterized as

    u_s = α u_eq

where α is a delay parameter.


------------------------------------------------------------
3. OBSERVATIONAL DATASETS
------------------------------------------------------------

Three late-time cosmological probes are used.

Pantheon+ SH0ES supernova sample  
1701 Type Ia supernovae providing distance moduli μ(z).

DESI DR1 BAO measurements  
Anisotropic BAO measurements of DM/rd and DH/rd along with the
isotropic DV/rd constraint.

Gold-2017 growth dataset  
18 measurements of the structure growth rate fσ8(z), including the
correlated WiggleZ subset at redshifts 0.44, 0.60, and 0.73.


------------------------------------------------------------
4. EXPANSION HISTORY ANALYSIS
------------------------------------------------------------

Pantheon+ and DESI datasets are fitted simultaneously.

ΛCDM reference fit:

    χ² ≈ 834.07

Empirical activation model:

    χ² ≈ 820.98

giving

    Δχ² ≈ −13

relative to ΛCDM.

The expansion-history activation model produces a nearly identical
fit:

    χ² ≈ 821.10.


------------------------------------------------------------
5. EQUALITY-TIED RESULTS
------------------------------------------------------------

For

    u_s = α u_eq

the best-fit parameters are

    H0 ≈ 74.57 km s⁻¹ Mpc⁻¹
    Ωm ≈ 0.229
    α ≈ 0.48

implying

    z_eq ≈ 0.50
    z_s ≈ 0.21

with fit quality essentially identical to the empirical model.


------------------------------------------------------------
6. STRUCTURE GROWTH TEST
------------------------------------------------------------

Linear growth of matter perturbations is computed using

    D'' + [ 2 + d ln H / d ln a ] D'
        − (3/2) Ωm(a) D = 0

The observable

    fσ8(z) = σ8 f(z) D(z)

is compared with the Gold-2017 dataset.

Resulting χ² values:

    ΛCDM           χ² ≈ 14.21
    MTS baseline   χ² ≈ 12.52
    equality-tied  χ² ≈ 12.63

indicating consistency with growth measurements.


------------------------------------------------------------
7. INTERPRETATION
------------------------------------------------------------

Across all tested formulations the activation scale consistently
appears at

    z_s ≈ 0.21

which occurs after matter–Λ equality at

    z_eq ≈ 0.50.

The observational data therefore favour a delayed response between
the epoch when matter and vacuum energy densities become comparable
and the epoch at which the effective matter contribution to the
expansion rate begins to deviate from ΛCDM.


------------------------------------------------------------
8. CONCLUSIONS
------------------------------------------------------------

We investigated a cosmological model in which the matter sector
contribution to the expansion rate is modulated by an activation
function dependent on expansion history.

Key results:

• Pantheon+ and DESI data favour the activation framework over ΛCDM  
  by Δχ² ≈ −13

• Activation scale:

      z_s ≈ 0.21

• Equality-tied delay factor:

      α ≈ 0.48

• Consistency with Gold-2017 growth measurements

These results demonstrate that a compact expansion-history activated
cosmology can reproduce late-time observations comparably to the
empirical formulation.

Further work is required to investigate the theoretical origin of
the activation law and implications for early-universe constraints.


------------------------------------------------------------
ACKNOWLEDGEMENTS
------------------------------------------------------------

The author thanks open cosmological data releases including
Pantheon+, DESI, and the Gold-2017 growth compilation.


------------------------------------------------------------
DATA AND CODE
------------------------------------------------------------

All numerical tests described in this work were performed using
single-cell reproducible pipelines combining Pantheon+ SH0ES,
DESI DR1 BAO measurements, and Gold-2017 growth data.


------------------------------------------------------------
9. CONSTITUTIVE DERIVATION OF THE ACTIVATION LAW
------------------------------------------------------------

The activation law may be written

    g(u) = 1 − exp(−u^ν)

where u is a dimensionless cosmological loading variable.

Define the inactive fraction

    S(u) = 1 − g(u)

and introduce the hidden memory load

    M(u) = −ln S(u)

which gives

    S(u) = exp(−M)
    g(u) = 1 − exp(−M)

Assuming the constitutive relation

    M(u) = u^ν

immediately yields

    g(u) = 1 − exp(−u^ν)


------------------------------------------------------------
Activation Differential Equation
------------------------------------------------------------

Differentiating gives

    dM/du = ν u^(ν−1)

and since

    M = −ln(1 − g)

we obtain

    dg/du = ν u^(ν−1) (1 − g)

which describes cumulative saturating activation.


------------------------------------------------------------
Expansion-History Loading Variable
------------------------------------------------------------

For cosmology

    u(z) = ln(1+z) / u_s

giving

    g(z) = 1 − exp[ − ( ln(1+z) / u_s )^ν ]


------------------------------------------------------------
Equality-Tied Activation
------------------------------------------------------------

Matter–Λ equality gives

    u_eq = (1/3) ln((1 − Ωm)/Ωm)

with activation scale

    u_s = α u_eq

so that

    g(z) = 1 − exp{ − [ ln(1+z) / (α u_eq) ]^ν }


------------------------------------------------------------
Threshold-Ensemble Interpretation
------------------------------------------------------------

If activation thresholds λ follow

    P(λ > u) = exp(−u^ν)

then the inactive fraction becomes

    S(u) = exp(−u^ν)

and the activated fraction

    g(u) = 1 − exp(−u^ν)

which corresponds mathematically to a Weibull survival law.


------------------------------------------------------------
10. LIMITING REGIMES
------------------------------------------------------------

Activation function

    g(z) = 1 − exp[ − ( ln(1+z) / u_s )^ν ]


Early-time limit (z >> 1):

    g(z) → 1

so

    H(z)^2 ≈ H0^2 Ωm (1+z)^3

recovering the standard matter-dominated expansion.


Present epoch:

    g(0) = 0


Small redshift expansion:

    ln(1+z) ≈ z

giving

    g(z) ≈ ( z / u_s )^ν


High redshift suppression:

    1 − g(z) = exp[ − ( ln(1+z) / u_s )^ν ] → 0


------------------------------------------------------------
Summary
------------------------------------------------------------

The activation cosmology therefore interpolates smoothly between

• a standard matter-dominated early Universe  
• a late-time activated matter-coupling regime

with activation scale

    z_s ≈ 0.21

occurring after matter–Λ equality

    z_eq ≈ 0.50
