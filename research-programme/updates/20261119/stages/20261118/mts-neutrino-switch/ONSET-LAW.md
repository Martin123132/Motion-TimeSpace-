# How a change in neutrino shear reaches the scalar

Use a matched state at x*=52; t=x−x*, and Δ means fluid minus free, never MTS minus baseline. Let f_r be the massless radiation fraction in this normalization, g=ka/α, and J=Δπ_x at the switch. Write D,F,π for the massless density, flux and shear. The first discontinuity is in a derivative, not in stress or in the metric. Directly from the hierarchy, Δπ=Jt+O(t²), ΔF=−Jt²/3+O(t³) and Δ(D−4C/3)=Jt³/9+O(t⁴), where C is synchronous CDM contrast.

The Einstein momentum constraint gives Δη=−f_r J t³/(6g*²)+O(t⁴). The radiation half-density in the Hamiltonian constraint contributes +f_r J t³/(6g*²). These two cubic terms cancel. Independently, the traced Einstein equation is ΔC_xx+hΔC_x=(Δd+3Δp)/2. Only this relativistic density enters its right side at cubic order: the massless contribution is 3 f_r ΔD/g*². Other species start from the same state and have no direct shear-switch forcing. Therefore

    ΔC_x = f_r J t⁴/(12 g*²) + O(t⁵).
    ΔC   = f_r J t⁵/(60 g*²) + O(t⁶).

For the common minimally metric-coupled scalar, LΔu=(φ′/k)ΔC_x with zero initial difference. The pressure readout thus has the one-sided law

    Δ(a²δp in native units) = (φ′*)² f_r J t⁵/(60 g*²) + O(t⁶).

This is an analytic response to the specified perturbation, not a fifth-order universal law for arbitrary cosmologies. The same derivation applies to the diagnostic spectator using its archived velocity. Test the coefficients on their own scale on both actual preparations. A pressure prediction derived this way does not require reading the changed pressure to choose its coefficient.

For a well-conditioned numerical test, evolve the *difference* itself from zero. All perturbation equations are linear on the common background. Drive the fluid shear equation by S(x)=−3π_free/x−D_free,x−π_free,x, sampled independently from the free arm; no native output, changed pressure, or fitted amplitude is an input. All metric, matter, collision, and scalar feedback evolves with the difference. Use trace and Hamiltonian formulations, refine source sampling and steps, and compare to subtracting independent full runs where subtraction resolves a signal. Also run zero-source and sign-reversal controls. This avoids falsely declaring a fifth-order signal zero because two nearly equal absolute fields rounded to the same value.
