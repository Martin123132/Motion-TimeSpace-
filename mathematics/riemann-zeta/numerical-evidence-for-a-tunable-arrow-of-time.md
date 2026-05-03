MEMORY-CONTROLLED IRREVERSIBILITY IN A ψ–Γ DYNAMICAL SYSTEM
Numerical Evidence for a Tunable Arrow of Time

Martin Ollett (2025)
Independent Researcher


ABSTRACT
--------

We present numerical evidence that irreversibility and hysteresis can be
dynamically generated, weakened, and erased in a time-reversal-symmetric
system through the introduction of a curvature-memory field Γ. Using a
minimal ψ–Γ dynamical model with no explicit dissipation, friction, noise,
or stochasticity, we demonstrate that hysteresis arises solely from
curvature-memory back-reaction. Instantaneous removal of Γ collapses
hysteresis in real time, while gradual decay of Γ produces a continuous
weakening of irreversibility. A parameter sweep shows that hysteresis loop
area correlates monotonically with mean Γ and saturates at large Γ,
indicating that the arrow of time has a finite, regulated magnitude.
These results support the interpretation of irreversibility as a
geometric memory effect rather than a statistical or probabilistic
phenomenon.


1. INTRODUCTION
---------------

The origin of irreversibility remains a foundational problem in physics.
Microscopic equations are typically invariant under time reversal, yet
macroscopic systems exhibit hysteresis, dissipation, and a preferred
temporal direction. Conventional explanations rely on statistical
arguments, coarse-graining, or environmental coupling, all of which
presuppose ensembles or external baths.

In the Motion–TimeSpace framework, irreversibility is attributed to
curvature memory: a geometric field Γ that accumulates during
interactions and resists subsequent motion. Here we isolate and test
this mechanism numerically in the simplest possible setting.

The central question addressed is:

Can irreversibility be created, weakened, and removed dynamically
without breaking time-reversal symmetry in the equations of motion?


2. MODEL
--------

We consider a one-dimensional periodic ψ field coupled to a
curvature-memory field Γ.

Motion field:
    d²ψ/dt² = c² ∇²ψ − λ ψ |ψ|^(1/3) − Γ dψ/dt + F(t)

Curvature-memory field:
    dΓ/dt = |∇²ψ|² − μ Γ

Key properties:
• The ψ equation is formally time-reversal symmetric
• Γ ≥ 0 by construction
• No explicit friction, viscosity, noise, or stochastic terms
• Momentum is conserved to numerical precision

The external drive F(t) is ramped up and down symmetrically, allowing
direct measurement of hysteresis.


3. NUMERICAL SETUP
------------------

• One-dimensional periodic lattice (256 sites)
• Second-order time integration
• Deterministic evolution
• Identical drive protocol across all runs

Diagnostics:
• Mean system response ⟨ψ⟩
• Mean curvature memory ⟨Γ⟩
• Hysteresis loop area (forward/backward integration)


4. RESULTS
----------

4.1 Emergence of hysteresis from curvature memory

With Γ active, the system exhibits:
• Response plateaus under increasing drive
• Phase lag between drive and response
• Multi-valued response curves
• Oscillatory release at high drive

No hysteresis is observed when Γ is absent.


4.2 Instantaneous removal of Γ

When Γ is set to zero mid-trajectory:
• Hysteresis collapses immediately
• The response becomes single-valued
• Phase lag vanishes
• No numerical instability occurs

This demonstrates that curvature memory is necessary for
irreversibility in the system.


4.3 Gradual decay of Γ

Replacing instantaneous removal with gradual decay produces:
• Continuous narrowing of the hysteresis loop
• Progressive weakening of phase lag
• Relaxation of Γ toward a nonzero steady state while motion persists

Irreversibility weakens smoothly rather than disappearing abruptly,
indicating that the arrow of time is graded rather than binary.


4.4 Loop area versus mean Γ

A parameter sweep over Γ decay rates shows:
• Hysteresis loop area increases monotonically with ⟨Γ⟩
• At large ⟨Γ⟩, loop area saturates
• At small ⟨Γ⟩, hysteresis approaches zero

Γ therefore acts as a control parameter for irreversibility strength.


4.5 Log–log scaling and saturation

A log–log plot of hysteresis loop area versus ⟨Γ⟩ yields a near-zero
slope in the sampled regime, indicating saturation rather than linear
response. This behavior is consistent with a constitutive relation of
the form:

    Loop Area ≈ Γ / (1 + Γ / Γ*)

Irreversibility grows linearly only at very small Γ and is bounded at
large Γ.


5. INTERPRETATION
-----------------

These results demonstrate that:

• Irreversibility can arise without asymmetric equations
• Irreversibility can be weakened or erased by modifying a single
  geometric state variable
• The arrow of time has a finite, regulated magnitude
• Hysteresis is a geometric memory effect, not a statistical artifact
• Entropy-like measures diagnose curvature memory but do not generate it

The observed saturation shows that time asymmetry is regulated rather
than divergent.


6. IMPLICATIONS
---------------

The ψ–Γ system suggests a reinterpretation of irreversibility across
physics:

• Thermodynamics: entropy measures accumulated curvature memory
• Hysteresis: path dependence arises from Γ back-reaction
• Critical slowing: Γ saturation suppresses evolution without
  singularities
• Arrow of time: a material-like response, not a binary law

This provides a minimal, falsifiable mechanism for time asymmetry
without ensembles, coarse-graining, or probabilistic assumptions.


7. CONCLUSION
-------------

Numerical experiments show that the arrow of time can be treated as a
tunable geometric response controlled by curvature memory. Irreversibility
emerges, weakens, saturates, and disappears exactly as predicted by the
ψ–Γ dynamics.

Time asymmetry is not imposed.
It is generated, regulated, and remembered.

END
