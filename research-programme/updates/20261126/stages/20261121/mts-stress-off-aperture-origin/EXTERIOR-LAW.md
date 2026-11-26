> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# How much of the original current signal is accessible in a finite box?

The full scalar tide depends on P(ε−3Hj), not on an arbitrary local multiplier of the current. For the original two windows both are normalized, so the directly sourced *density* tide is exterior independent in the difference. The double inversion applied to the *current* is not. Let R be outside both supports, in homogeneous **physical** radius u=b r. Integrals here use the quadrupole normal and tangential coefficients of the orthonormal material current (per gradΩY). The only exterior datum needed for the two-window current difference is

    c_out(R) = (1/5) ∫_R^∞ [−3J_r(u)+6J_t(u)] du/u² .

This follows from the adjoint in [the derivation](DERIVATION.md): beyond both windows I₋=0 but I₊ can be nonzero. Equivalently the exterior source in the *first inversion* gives a regular inner potential c_out u²Y. A jump at R must be included if cutting the source; the formula uses currents directly and does not discard the divergence's surface term. For the second inversion the regular interior particular solution of Δφ=u²Y is u⁴Y/14, so P(u²)=−11u²/42 modulo a constant tide. Because ⟨u²⟩_width=CENTER²(1+width²/11), the exact coefficient in the narrow-minus-wide observable is

    I∞ = P_narrow(u²)−P_wide(u²) = CENTER²(0.30²−0.15²)/42.

The full momentum signal is the measured integral through R **minus** 3 I∞ times the change in H c_out(R), with the same signed wave/cold contrasts. Nothing here fixes the latter to zero. A radial solenoidal current is a null control for the **full** inversion; an arbitrarily truncated current need not be solenoidal. The third window in [the independent test](MOMENTUM-TEST.md) exactly removes this unknown for that new combination.

The two-window table (not bundled here) includes the integral through R=2, 2.5 and 2.8, a triangle-inequality upper estimate on the resolved quadrature (absolute normal and tangential contributions before summing), and the **required** exterior value if the leading measured shear were entirely scalar on this homogeneous ruler. The signed value is not an estimate of the actual exterior field; non-scalar shear or geometry could contribute instead. The upper estimate refers to the resolved signed change profiles on the integration grid, not unknown interpolation error or unobserved matter. The three-window absolute bound is reported alongside its much more strongly cancelling signed value.

An analytic current with j=u² exp(−u²) has nonzero support beyond the cut and c_out(R)=3 exp(−R²)/5. Integrating its current only inside the window without that term fails; adding the derived exterior term reproduces the full density-kernel result. [Independent two-resolution controls](evidence-001.zip) (archive member: `exterior-current-controls.csv`).
