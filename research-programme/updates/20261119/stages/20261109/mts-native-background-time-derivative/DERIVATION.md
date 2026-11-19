# Time derivative and cancellation-safe heavy equation

For each retained model separately, E=T^-1 DeltaF T, C_T=T^-1 T_N and DeltaF=F_ref-F_ret. Product differentiation yields
    E_N=T^-1(DeltaF)_N T + E C_T-C_T E.
For a fixed retained vector v, the implementation evaluates
    E_N v=T^-1[(DeltaF)_N(Tv)+DeltaF(T_N v)]-T^-1 T_N(Ev).
The separate readout derivative is
    ((DeltaL)T)_N v=(DeltaL)_N(Tv)+DeltaL(T_Nv).
This stage tests these coefficient actions on the original left-end carried mode and four fixed seeded vectors, not the evolving current mode. To propagate the latter requires adding E(y_c)_N.

The native total derivative is approximated by a centered four-point formula at h,h/2,h/4, while holding encoded vector Tv fixed. Each offset follows the same saved slow background and a locally integrated physical phase equation with the SAME saved center phase; the common carrier also follows its original history. No perturbation preparation is restarted. Nominal fourth-order truncation applies only on sufficiently smooth stencils; piecewise thermal data can reduce that order. Step changes are numerical diagnostics, not proven bounds. Predictions and all three derivative levels are frozen before the direct index2 source test.

## Heavy-field cancellation derived from the original equation

In PoissonDriver.evaluate the encoded heavy amplitude obeys
    A_N=i(chi_N-omega/H-gamma)A
        +(3/2-i gamma)exp(2i chi)A*
        -i a k p exp(i chi) Z/(H sqrt(omega)),
    gamma=k^2/(2 omega H), omega=a m_h.
H here is the native conformal expansion rate, p the heavy conformal field velocity, and Z the synchronous metric expansion variable. The encoded CDM continuity equation gives Z/H=-k^-1(delta_c,sync)_N.

At identical N, a, omega, chi, chi_N and encoded A are common. Subtraction cancels chi_N A and (3/2)exp(2i chi)A* exactly. Therefore
    Delta A_N=-i(omega+k^2/(2omega)) Delta(1/H) A
              -i k^2/(2omega) Delta(1/H) exp(2i chi) A*
              -i a k exp(i chi)/sqrt(omega) Delta(p Z/H).
Evaluate the differences as
    Delta(1/H)=(H_ret-H_ref)/(H_ref H_ret),
    Delta(p V)=((p_ref+p_ret)/2)(V_ref-V_ret)
               +((V_ref+V_ret)/2)(p_ref-p_ret), V=Z/H.
These are algebraic identities, not new couplings or fitted coefficients. The implementation checks identical scale factors and compares the reconstructed heavy differences with saved native evaluations at the unchanged full-rate algebraic gate. A small difference-relative discrepancy remains a numerical precision diagnostic, not proof of arbitrary cancellation accuracy.

Only the two heavy encoded components are replaced in a separate diagnostic packet. Other components and all baseline packets remain unchanged. This cannot resolve cancellation in other components, native background rounding or thermal knots by itself. Derivative controls must decide whether it helps. Existing frozen interpolation predictions are not overwritten or rescored as if this repair had been selected before the held-out test.

