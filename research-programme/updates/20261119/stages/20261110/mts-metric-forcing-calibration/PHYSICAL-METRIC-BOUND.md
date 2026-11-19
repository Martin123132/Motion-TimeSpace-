# Physical-coordinate check and tighter constant-metric bound

Additional validation fixed before its run; original protocol and gates stay
unchanged. The canonical/action implementation has completed. Independently
assemble its physical-coordinate alternative, rather than refining the
already converged quadrature again.

For exact background q0, eliminating P gives, for arbitrary H,

    q''+Omega_k^2 q=C'(p0-Hq0)-2mu^2 Psi q0.

Therefore, for this probe's constant potentials, kinetic coordinates
z_k=(q,q') have F_phys=[[0,0],[-2mu^2 Psi,0]]. All dependence on constant
Phi cancels, provided the initial physical q,q' are fixed. The previous
bound applies with

    J_phys <= 2 JD |Psi|,
    J_delta_phys <= 2 JD epsilon_Psi,

where JD is the exact rational J_coefficient_D in proof.json. Initial-state
uncertainty and changing metric histories remain separate. The Phi/Psi
bound for fixed canonical P is still valid, but answers a different initial
data question and is more conservative.

Using a W2 off-shell background in the action representation adds C R0 q0
when eliminating P. The physical-equation representation instead drops
that residual along with E0,Ek. Each has its own valid template bound
relative to the same exact system with matched initial data. Their difference
must not be mislabeled an independent physical coupling. Check the algebra
with a symbolic background residual, and compare all399numeric modes.

Validation uses the frozen512panels,16Gauss nodes,eight panels per batch.
It integrates G_phys separately, reuses the same prepared physical states,
and compares against the canonical implementation. Pressure refinements
are also checked with the saved fixed energy/density-block normalizer,
not divided by a near-zero pressure. This is an absolute source-block check,
not a claim of relative accuracy for arbitrarily small pressure.

The saved amplitudes are transfer coefficients multiplying the same retained
primordial curvature mode (formation bundle SCHEMA.md). Large coefficients
are not literal order-one metric disturbances or a nonlinear solution.
No new primordial amplitude is chosen. The two carrier quadratures are
controlled microscopic preparations, not a derived local halo population.

Reported metric uncertainty bounds are in template coefficient norm per
unit initial carrier norm. They cannot be compared directly to a fractional
observational tolerance, and do not certify initial-data or whole-history
uncertainty. Exact rational enclosures, binary64 comparison accuracy and
the saved transfer buffer's finite precision are distinct error sources.
