# Independent check at the identified low-frequency failure

After isolating the carrier/beat argument-rounding defect, add one physical
KG control at the worst original failing mode, k=0.0004371444812611/Mpc.
This is a post-diagnosis numerical regression control, not held-out evidence.
Preserve both real quadratures of the explicitly conditional dressed state.

Evolve q0,q0',qk,qk' directly with DOP853 at the same2e-11/2e-12 tolerances
and fixed microscopic normalizers. Use analytic derivatives of the identical
supplied metric cubic, not the repaired transport basis. Compare endpoint
fields and the density/current/pressure source block against the repaired
8192panel result with the unchanged2e-5 gate. Report failure if either
tolerance exceeds it; do not replace a source check with a field-only check.

This complements the four original physical controls, not a request to rerun
the full native hierarchy. One single-threaded worker, bounded900seconds.
