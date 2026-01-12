TITLE
-----

Zero Stability of the Riemann ξ–Function Under Admissible Smoothing Operators
A Numerical Elimination Study


AUTHOR
------

Martin Ollett
Independent Researcher
2025


ABSTRACT
--------

We present a systematic numerical investigation into the stability of the
non-trivial zeros of the Riemann ξ–function under a broad class of admissible
operators acting along the critical line. The goal is not to assert a proof
of the Riemann Hypothesis, but to rigorously test — and eliminate — a large
family of commonly assumed mechanisms by which the zero set is conjectured
to remain invariant.

We show that while trivial multiplicative (pointwise) operators preserve
zero locations exactly, any nontrivial operator that mixes information in
the t–direction (including symmetric, moment-balanced convolution kernels)
induces coherent, macroscopic zero drift. This persists even when all
first-order transport bias is explicitly removed.

The results rule out an entire class of “heat flow”, “diffusive”, and
self-adjoint local-operator explanations for the rigidity of the Riemann
zeros, and strongly suggest that any true governing structure must be
fundamentally nonlocal.


------------------------------------------------------------
1. SETUP AND BASELINE
------------------------------------------------------------

We work exclusively with the Riemann ξ–function on the critical line:

    ξ(s) = ½ s(s−1) π^{−s/2} Γ(s/2) ζ(s)
    s = ½ + it

All experiments are conducted on the real-valued function

    f(t) = Re ξ(½ + it)

Zeros are detected by:
  • dense sampling in t
  • identification of sign changes or |ξ| minima
  • local refinement via interpolation

Baseline zero sets were established across multiple windows, e.g.

  t ∈ [0, 60], [60, 120], [120, 180]

with resolutions up to N ≈ 16,000 (dt ≈ 3.6×10⁻³), producing stable,
well-resolved reference zero locations.


------------------------------------------------------------
2. OPERATOR CLASSES TESTED
------------------------------------------------------------

We tested four broad classes of operators applied to f(t):


2.1 Multiplicative (Pointwise) Operators
----------------------------------------

Form:
    f(t) → g(t) · f(t)

Examples:
    g(t) = (1 + τ t²)^{-½}

Results:
    • Zeros invariant to machine precision
    • mean |Δt| = 0 for all τ tested

Interpretation:
    These operators do not mix information across t.
    Zero invariance here is trivial and non-informative.


2.2 Symmetric Convolution (Gaussian Smoothing)
-----------------------------------------------

Form:
    f_σ(t) = (K_σ * f)(t)

with K_σ even and normalized.

Results:
    • Zeros drift coherently
    • mean |Δt| grows rapidly with σ
    • clustering and near-degeneracies appear
    • drift persists across resolutions

Conclusion:
    Symmetry alone does not protect the zero set.


2.3 Interior-Only / Guard-Band Convolution
-------------------------------------------

To remove edge effects:
    • convolution performed on extended domain
    • zero tracking restricted to interior sub-window

Results:
    • Edge artifacts removed
    • Zero drift remains O(10⁻³ – 10⁻¹)
    • Drift scales approximately as σ² at higher t

Conclusion:
    Drift is intrinsic, not a boundary artifact.


2.4 Moment-Balanced Convolution (C1, C1b)
-----------------------------------------

We explicitly constructed kernels satisfying:

    ∫ K(t) dt = 1
    ∫ t K(t) dt = 0
    (no first-moment / transport bias)

C1:
    Pairwise matched zeros

C1b:
    Global balance over full zero set

Representative result (C1b):

    Σ Δt      ≈ −4.34×10¹
    mean Δt   ≈ −1.74
    Σ |Δt|    ≈ 4.34×10¹

Zeros exhibited:
    • coherent bulk migration
    • creation of artificial clusters
    • destruction of original spacing structure

Conclusion:
    Zero drift persists even when all linear bias is removed.


------------------------------------------------------------
3. SCALING AND LOCAL MODELS
------------------------------------------------------------

3.1 σ–Scaling
-------------

For mid and high t windows:

    mean |Δt| ∝ σ^p
    with p ≈ 2.0

Low t windows showed anomalous behavior, consistent with known
non-asymptotic irregularity near the first zeros.


3.2 Pairwise Interaction Models (A)
-----------------------------------

We tested whether drift could be explained by local zero–zero
interactions:

    Δt_i ≈ Σ_j F(|t_i − t_j|)

with bases:
    1/|d|, 1/|d|², sign(d)/|d|

Results:
    • R² ≈ 0 (or negative)
    • No predictive power

Conclusion:
    Drift is not explained by pairwise local repulsion or attraction.


3.3 Density-Gradient Models (B)
--------------------------------

Hypothesis:
    Drift controlled by local zero density gradient

Results:
    • Predicted drift orders of magnitude too small
    • R² < 0

Conclusion:
    Local density does not control drift.


------------------------------------------------------------
4. KEY NEGATIVE RESULT
------------------------------------------------------------

The central empirical finding is:

    Any nontrivial operator that mixes information along t
    causes coherent zero drift.

This includes:
    • symmetric kernels
    • Hermitian kernels
    • moment-balanced kernels
    • interior-only application

Therefore:

    The Riemann zero set is NOT invariant under any reasonable
    local smoothing, diffusion, or heat-flow operator.


------------------------------------------------------------
5. IMPLICATIONS
------------------------------------------------------------

These results eliminate an entire class of approaches to the
Riemann Hypothesis, including:

    • heat-flow stabilization arguments
    • local self-adjoint operator flows
    • diffusive rigidity mechanisms
    • Sturm–Liouville style intuitions in t

If the Riemann Hypothesis is true, its mechanism must be:

    • nonlocal
    • globally constrained
    • not expressible as a local operator in t
    • likely tied to explicit-formula / prime-side structure

Zero locations behave as global interference constraints,
not as equilibria of a smoothing dynamics.


------------------------------------------------------------
6. CONCLUSION
------------------------------------------------------------

We have not attempted to “prove RH”.
Instead, we have:

    • built controlled numerical experiments
    • systematically tested admissible operator classes
    • eliminated large families of plausible mechanisms

This sharply narrows the space of viable explanations for the
rigidity of the Riemann zeros.

The absence of local operator invariance is itself a strong,
positive result.


END
