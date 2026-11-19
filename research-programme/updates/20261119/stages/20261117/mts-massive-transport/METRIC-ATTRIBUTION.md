# Transfer-history test of the residual after restoring the slow-field table

Can the difference between the two saved metric histories account for what the velocity swap leaves? Use no endpoint fit and start the differential perturbation at zero (record the archived initial mismatch separately). This is attribution with reference inputs, not a forecast of the native metric.

Write x=kτ, C=δ_c, B=φ'_table/k, h=H/k, W=1+(am/k)². Put u equal to the already solved fixed-metric spectator and w equal to the archived-geometry perturbation minus u. The exact differential equation is

    w_xx + 2 h_N w_x + W_N w
        = B_N ΔC_x + (B_N−B_P) C_P,x − 2 Δh u_x − ΔW u.

Here N/P stand for saved native/physical geometry. Do not double count a changed pressure readout. Recover ΔC_x independently from the slope of the saved CDM contrast difference and from −Δσ+3Δη_x, with σ_N=−H_N v_Newtonian,cdm/k, η_N=etak_N/k (retained synchronous conventions, equations.f90). Use interpolation only on the original irregular output grid; record maximum gap and test both independent source representations, removal of alternating interior knots, and integration refinement. The native CDM transfer was saved in binary32, not as an exact derivative. A differential replay only passes if the residual plus the observed resolution/representation spread is within the original tolerance on both branches; do not force agreement, and do not count training inputs as predictions.
