# Derived correction to the restarted cancellation check

The first raw nodewise superposition test failed at one MTS entry: report2914, preparation node801, component u. Baseline had no failure. All source, native-reference, weighted-superposition and endpoint-envelope checks passed. The original failed result and the gate-blocked series-scoring receipt are retained unchanged.

The raw test assumed full-quadratic-difference should be zero at the new restart. However, the three independently saved finite-precision states already have a tiny known mismatch E0 at2908. Their linear equations imply exactly

    E = X_full-X_quadratic-DeltaX,
    E' = A E,
    E(T_old) = saved X_full-saved X_quadratic-saved DeltaX.

Thus the correct restarted identity is E(T)=U(T,T_old)E0, not E(T)=0. E0 is calculated with an accurate signed sum of the existing64-step restart values, before propagation. It is not fitted to the failing node. This is a numerical identity/error-accounting repair, not a new physical source or a change of theory.

transport_restart_defect.py transports this known initial mismatch for ALL nodes in BOTH baseline and MTS, with the existing A,32/64 physical steps and solver tolerances. No original state, source, bank, norm, grid, threshold or prediction changes. The original raw per-node allowance is retained. The residual after subtracting the independently transported mismatch, plus transport refinement/rounding, must fit that unchanged allowance.

At the failed entry:
- Raw error: -8.466789743970168e-20.
- Unchanged allowance: 7.556015712620861e-20.
- Known initial mismatch: -5.4147947948120993e-20.
- Equation-predicted transported mismatch: -7.693197450452328e-20.
- Remaining discrepancy: -7.735922935178397e-21.

All nodes now satisfy the corrected identity: maximum residual-plus-transport-uncertainty is10.0642% of the old allowance for baseline and19.4335% for MTS. MTS transport32/64 relative difference is5.2135e-14. The retained raw failure was12.0536% above its allowance; it is not erased or called a pre-registered pass. The adjustment is explained by the saved initial condition and the coupled equation, not a larger tolerance or fitted correction.

Authoritative overall status is batch-result.json after this explicit repair. result.json remains the original raw comparison. The first score-series worker correctly stopped at that raw gate; score-series-after-transport performs the separate response-expansion check only after the derived-identity validation passes.

For the next restarted batch, calculate and transport its own saved E0 when testing the same identity. Do not silently assume three separately stored float states have an exactly vanishing initial mismatch. A finite numerical allowance remains a working estimate, not a continuum certificate.
