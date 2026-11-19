# Dirac-adjoint completion of the conjugate coefficient check

The root run passes its stated gauge and coefficient-conjugation tests, but
its bare B^dagger partner is not yet tied to the spinor adjoint. Gauge
invariance cannot choose that relative sign. Preserve those results as a
gauge-only, bare-Euclidean-coefficient comparison; they are not the final
answer to the owner's request for the retained matter conjugate terms.

Declare the Dirac-adjoint coefficient continuation using Gamma4 (gamma4
tensor the internal identity). With bar_psi=psi^dagger Gamma4 as the
coefficient-audit map, the ordered conjugate of psi_L^T B psi_R is

    bar_psi_R Bsharp bar_psi_L^T,
    Bsharp = Gamma4_R B^dagger Gamma4_L^T.

Gamma4 is real symmetric and squares to one in the saved convention, so this
equals psi_R^dagger B^dagger psi_L* when tested on that map. For the saved
C=gamma2 gamma4, gamma4 C^dagger gamma4^T=-C^dagger. Thus each of our three
barred tensors acquires a minus sign relative to the original bare pairing.

The new dirac-adjoint copy computes Bsharp explicitly, propagates it through
barred/Higgs Euler terms, and checks both the Dirac-adjoint coefficient
identity and a deliberately wrong bare-spin conjugation. Independent barred
rows remain independent in the actual gauge/Noether tests. The coefficient
audit does not impose them as conjugates of overlap-projected columns.
No reflection positivity or complete finite-cutoff Lorentzian reconstruction
is asserted. Any different Wick/adjoint convention must carry its phases
consistently; the bare pairing alone did not establish that correspondence.

The classical link current is unchanged: the barred projector is fixed, so
barred Yukawa terms have no link derivative at fixed Higgs/barred fields.
The new barred contributions to the Euler contact cancel against their
Higgs partners in the gauge identity. We check that all link currents are
byte-identical to the original gauge-only run while rechecking the complete
action, Ward balance and both finite-difference steps.

No seed, fixture, coupling, grid, boundary sign or tolerance is changed.
Root artifacts are hash-pinned and retained. The authoritative final result
will be dirac-adjoint/result.json, not the root gauge-only result. This is a
completion of the conjugation convention, not evidence for a new interaction.
