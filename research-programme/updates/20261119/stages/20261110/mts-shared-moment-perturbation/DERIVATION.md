# Shared distribution: background to perturbations

## Scope and retained parent

This extends mts-conservative-background-bridge-20261110, not a replacement theory. Retain the same Einstein metric coupling, scalar action and all four real heavy-envelope coordinates. Massive neutrinos and the cold comparison are standard matter sectors in this retained calculation. Their numerical treatment must be consistent before attributing a metric defect to the MTS field.

The original five-node native operator is first reconstructed directly in Python and compared row by row against a fresh retained native capture. This separates changing reference quadrature from changing the physical equations and avoids altering the original native capture limit. Momentum nodes increase only in a separately labelled reference; the production bank, angular cutoff 16 and all original files stay fixed.

## Shared thermal distribution and exact source identities

Let a be dimensionless scale factor, tau conformal time in Mpc, H=a'/a, k=5/Mpc, mu=a*m_nu/T_nu0, epsilon_i=sqrt(q_i^2+mu^2), and v_i=q_i/epsilon_i. The positive shell distribution, its weights B_i and fixed normalization A are defined by the preceding sealed shared-distribution construction. No weight is adjusted to cancel a measured perturbation residual.

Define

    d_i = A B_i/(a^2 v_i), j_i = A B_i/a^2, p_i = A B_i v_i/a^2;
    D_nu = sum d_i F0_i, Q_nu = sum j_i F1_i;
    P_nu = (1/3) sum p_i F0_i, Pi_nu = sum p_i F2_i.

These are Einstein-normalized stress sources with units Mpc^-2, not SI densities. The background computed from the same shell distribution satisfies

    S_nu = R_nu + Pbar_nu = (4/3) sum d_i.

Since epsilon_i'/epsilon_i=H(1-v_i^2), the exact weight derivatives are

    d_i' = -H(d_i+p_i), j_i' = -2H j_i.

Insert the retained hierarchy equations

    F0_i' = -k(4z/3 + v_i F1_i),
    F1_i' = k v_i(F0_i-2F2_i)/3.

It follows without specifying the perturbation state that

    D_nu' + H(D_nu+3P_nu) + k Q_nu + k z S_nu = 0,
    Q_nu' + 2H Q_nu - k P_nu + (2k/3) Pi_nu = 0.

The previous mismatch between background enthalpy and perturbation quadrature is therefore removed by using one distribution, not by subtracting an error afterward. The first identity fails by k z[S_nu-(4/3)sum d_i] if unrelated moment rules are substituted. This is the already identified mechanism; no new force or fitted coefficient is introduced.

In the direct hierarchy, delta_c'=-kz. Consequently the first operator identity is checked against the actual corrected/canonical matrix using -S_nu times its CDM density row. This includes live metric feedback rather than an independent assumed metric. Test every state-vector coefficient, not merely one trajectory. Three sampled background points per model/rule validate the implementation; the algebra above supplies the conditional analytic identity throughout the supported regime.

## Canonical reuse and thermal inputs

The original canonical block is reused through an isolated background interface. Its carrier, pressure clock and mixed-gauge source map all read the new consistent background. The source-complete leading late radiation correction is reused, including the implicit scalar pressure feedback, baryon drag and rest-species response. No averaged-heavy fluid is substituted for the final MTS evolution. At the original five-node inputs, the complete canonical matrix and physical source rows must reproduce the retained implementation.

Opacity and baryon sound speed remain retained functions of a. A 33-node interpolant is tested at 32 interleaved points. A fresh thermal initialization differs from captured native values by up to 1.418e-6 (cold) and 3.685e-7 (heavy), below the unchanged 2e-5 gate; this is retained numerical context, not exact identity. It is not reionization inference or a self-consistent primordial thermal recalculation.

## Controlled initialization and evolution

For the first coupled reference, choose the explicit small thermal momentum dilation delta f=-q f_h'(q)Theta, Theta=1e-6. This yields F0=4Theta at every node and zero higher multipoles independent of the grid. The other initial coordinates and the conditional live-D0 canonical preparation are frozen in PREPARATION-CONTRACT.md. The canonical solve preserves physical Newtonian heavy density/current of the seed, not a claim of unique cosmic or galactic state selection.

Use the retained fourth-order commutator-free exponential method for Y'=A(tau)Y. With c_+-=1/2+-sqrt(3)/6, g_+-=(3+-2sqrt(3))/12 and step h,

    Y_next = exp[h(g_- A(c_-)+g_+ A(c_+))]
             exp[h(g_+ A(c_-)+g_- A(c_+))] Y.

The normalization is an invertible diagonal similarity transform, not a change of theory. Both cold and canonical-heavy use 64/128 steps, two fixed momentum references and unchanged gates. Saved restarts are hash-linked. At common scale-factor probes, use a final short exponential step from the previous saved time, never interpolate rapidly oscillating canonical coordinates. Compare coarse/fine evolution and 32/64 source readouts separately.

Differentiate the actual eliminated potential row: Phi'=(partial_tau row_Phi+row_Phi A)Y. Check E_Phi=Phi'+H Psi-Q/(2k), the Hamiltonian constraint and the previously derived energy/current budget with two derivative stencils. Conservation of the neutrino rows alone is not a proof that the remaining approximate radiation hierarchy is exact. Results must keep these distinctions.
