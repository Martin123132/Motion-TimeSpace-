# Frozen native-slope interpolation test

The repaired background replay left an MTS field/current discrepancy near
6.02e-5 against the unchanged 2e-5 gate. The exact off-shell port diagnostic
attributes most of this to metric-history derivatives, not to the background
repair. Adding these ports was a diagnostic, not an accepted new force law.

Test a separate interpolation that uses the already saved double-precision
native derivatives. No new native evolution, source table, initial state,
acceptance tolerance, physical parameter or sampling point is changed.

For the retained flat k=1 Mpc^-1 run, H is conformal and R,Pbar are native
8*pi*G*a^2 density/pressure. The source and gauge equations give

    H' = -(R+3Pbar)/6,
    Phi' = eta' - H'*alpha - H*alpha',
    Psi' = 2*Weyl' - Phi',
    alpha' = sigma_prime,  alpha = sigma.

Check alpha'=Psi-H*alpha and the native Weyl/slip derivative relation at the
readout nodes. Use Phi,Psi and these slopes in piecewise cubic Hermite
interpolation, leaving the retained scale Hermite interpolation unchanged.
Test two/four RK4 substeps and every-second-node histories with boundary
guards. Check omitted-node metric values against their saved native values.
Both baseline and MTS must meet the same original componentwise gate.

Passing this test verifies a forced canonical replay on the native coupled
history, not an independently recoupled full hierarchy or primordial-state
selection. Failed original/value-cubic comparisons remain saved unchanged.
