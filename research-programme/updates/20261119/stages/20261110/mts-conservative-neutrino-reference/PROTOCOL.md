# Conservative thermal-neutrino reference from a single distribution

Previous goal turn made verified progress: it derived the actual numerical
source mismatch in both MTS and cold, reproduced its background contribution
and derived an endpoint-error expansion. No saved worker remains outstanding.
Start from seal 2705b69641c2f43546996052fe02123ddf5bbac5348dcb5009cd27cb764853fb.
Safe four-hour handoff before 15:39 UTC, 2026-11-10.

Do not tune a force, renormalize weights to cancel the measured residual,
or mix an altered background with unaltered perturbation coefficients.
Instead represent the SAME continuous Fermi-Dirac distribution by a positive
step-distribution reference. Its derivative has discrete momentum shells;
derive background density, pressure, their derivatives and perturbation
moments from that one distribution. Verify positivity, continuity and the
shared enthalpy identity before any production proposal.

Test the retained native five-node rule and separately labelled positive
16/32/64-node Gauss reference rules fixed over q=0..60. Those reference
grids are numerical controls only; the production bank and grids stay fixed.
Use the same 2e-5/1e-10 gates. Compare with independent continuum integrals
at retained cold/MTS initial/mid/final backgrounds and a broad am grid,
including the relativistic and nonrelativistic limits. Preserve failures
of a coarse rule rather than selecting a mass range after seeing results.

One numerical worker/thread, CPU4 below-normal, -B, 900sec worker deadline
and owner holds. No subagents, new native build, GitHub, Galaxy changes,
relay/timer, app/server/browser or other-worker intervention.
