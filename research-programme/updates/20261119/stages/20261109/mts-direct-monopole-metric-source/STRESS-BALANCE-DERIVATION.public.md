> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Scalar stress coupling and explicit background-flow defects

This document corrects the metadata description in DERIVATION.md and extends its metric-source derivation. Zero-based metadata[3] is the MASSIVE-NEUTRINO QUADRATURE enthalpy, not a scalar enthalpy contribution. Scalar metadata occupy[4:11] and[14:21]. The numerical code always used the correct entry; no result changes.

## Retained action-sector equations

For either retained canonical scalar, let phi be the background field, v its conformal velocity, omega^2=a^2 m^2, and u,w its synchronous perturbation and perturbation velocity. Native linear equations are

    u_dot = w
    w_dot = -2H w - (k^2+omega^2)u - k z v.

The stress readouts, with the native a^2 gravitational normalization, are

    D = v w + omega^2 phi u
    P = v w - omega^2 phi u
    J = k v u
    E = v^2.

Do NOT assume that an interpolated background satisfies its differential equation exactly. Define

    F_phi = phi_dot - v
    F_v = v_dot + 2H v + omega^2 phi.

Differentiating the stress using the perturbation equation gives the exact identities

    D_dot + H(D+3P) + kJ + kzE
        = F_v w + omega^2 F_phi u
    J_dot + 2HJ - kP
        = k F_v u.

These are derived source-coupling conditions: vanishing background-flow defects imply the corresponding linear scalar energy/momentum balances. For nonzero defects the equations explicitly state the stress residual; it is not set to zero by a new closure.

Pointwise bounds follow directly:

    |epsilon_E| <= |F_v||w| + omega^2 |F_phi||u|
    |epsilon_J| <= k |F_v||u|.

They become continuum bounds only when the background and perturbation bounds hold throughout the interval. Sample maxima alone do not certify that.

## Exact retained source ownership

[Operational or machine-specific passage omitted from public reading copy.]

The native non-scalar approximations remain explicit. The baryon density equation retains the native rest-mass approximation, yielding a +3H P_b term in the total continuity accounting. Massive-neutrino metric forcing uses its quadrature enthalpy. Neither is silently promoted into a proof of exact total covariant conservation.

## Connection to the troublesome metric source

With R0 the existing metric-independent density-rate base, split it into native conservative transport, slow-field flow defect, heavy-field flow defect and remaining arithmetic/approximation residual. The analogous split applies to J_dot.

In GR the scalar defect in Phi_dot0 is

    epsilon_Phi = -epsilon_E/(2k^2) - 3H epsilon_J/(2k^3).

In Poisson-spatial it contributes -epsilon_E/(2k^2), while the existing background H/G derivatives remain separate. This is a partial source decomposition, not permission to replace all background derivatives.

The exact finite-background formula from DERIVATION.md propagates these pieces through the existing metric denominator and observable adjoint. We compare the SAME source before and after decomposition; no accepted source is replaced.

## Verified evidence

Full saved grid:1025MTS+1017baseline nodes; two metric branches. Independent90-digit expanded stress differentiation checks16336scalar/background/branch cases:
- algebraic stress identities agree to<=3.868e-86 in the chosen normalization;
- agreement with compiled scalar stress rates is<=4.367e-12 for MTS and<=2.319e-16 for baseline, below the unchanged1e-10 algebra gate;
- the total stress-balance accounting residual is<=6.623e-13 (MTS density) and<=5.259e-15 (MTS current); baseline<=2.291e-16;
- all diagnostic residuals remain stored, not zeroed.

On the MTS heavy reference background, normalized flow defects reach6.784e-9 in phi_dot-v and2.907e-9 in the acceleration equation. Retained instantaneous heavy defects stay below2.880e-16 by the same normalizations. This is a small background representation error, but it dominates the weak source channel's integration change.

The heavy-field flow-defect contribution to the signed refinement difference, divided by the ORIGINAL conditional source budget:

| Branch/channel | Heavy-flow contribution | Total Phi_dot0 contribution |
|---|---:|---:|
| GR/Pi | -3.78310354e-5 | -3.78376139e-5 |
| GR/delta_massless | +4.95710669e-5 | +4.95796489e-5 |
| Poisson-spatial/Pi | -2.35591900e-5 | -2.35150367e-5 |
| Poisson-spatial/delta_massless | +2.93699981e-5 | +2.93144175e-5 |

Small compensating terms explain values slightly exceeding100% of a signed total. Baseline heavy-field defects are identically zero because that field is absent; its separate small-signal conditioning is retained.

## Integration consequence and next step

The saved third-cell MTS interval crosses158background dense-polynomial segments (157internal boundaries); baseline crosses2segments. See DENSE-SEGMENT-INVENTORY.json. The existing uniform source quadrature does not explicitly respect those boundaries. This makes segment-aware integration a motivated next test, NOT a proven cure.

Retain the true background derivative and its measured defect. First derive the weighted defect in N and test integration on frozen saved dense segments, splitting at their actual boundaries. If using integration by parts,

    integral B dot (Y_N-f(Y)) dN
      = [B dot Y] - integral (B_N dot Y + B dot f(Y)) dN,

all boundary terms and weight derivatives must be retained. Do not use this formal identity to discard a defect or impose a canonical derivative inconsistent with the saved path. A local, cancellation-controlled implementation must be compared with direct integration under the unchanged gates.

This is a concrete route to improving the retained calculation without rebuilding MTS or modifying its action.

