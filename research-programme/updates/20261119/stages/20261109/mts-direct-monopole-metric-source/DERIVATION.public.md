> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Direct finite-background monopole source from metric and stress

## Retained problem

Use the same saved physical state and the two existing backgrounds, reference r and retained t. No action, physical history, source node, parameter, massless-fluid branch or tolerance is changed. Both GR and Poisson-spatial metric branches are tested, for MTS and baseline.

The construction evaluates the metric expansion directly from independent native stress readouts. The monopole rate is a COMPARISON OUTPUT, never an input used to reconstruct the expansion.

[Operational or machine-specific passage omitted from public reading copy.]

This is an exact rearrangement of those retained equations, conditional on their existing native stress and background approximations. Exact rational or90-digit arithmetic does not make the native input histories exact.

## Primitive quantities and conventions

N=ln(a), dot=d/dtau, H=dN/dtau is the CONFORMAL expansion rate. k is the unchanged wave number. Native units give tau a length and H,k inverse lengths. Delta means reference minus retained; bars below mean the arithmetic average of those two values, NOT an ensemble or time average.

The independent native getters supply:
- density perturbation rho1, current J, anisotropic stress Pi;
- enthalpy E=rho+p;
- quadrature enthalpy Eq;
- native synchronous shear sigma_native;
- species density-rate and current-rate terms.
The saved background spline supplies H_N and G_N, where G=3HE/(2k^2).

With T_i,j the retained species-stress table and metadata_3 its scalar enthalpy contribution:

    Eq = sum_i T_i,5 - T_4,5 + metadata_3
    z_native = sigma_native - 3J/(2k^2)
    R0 = sum_i T_i,3 + k Eq z_native
    J_dot = sum_i T_i,4
    H_dot = H H_N
    G_dot = H G_N.

The subtraction/addition in Eq and R0 follows the existing driver. It is not a newly chosen stress prescription. The finite-increment evaluation operates on the independently captured individual primitive entries.

The state contains the fixed metric time-shift alpha and massless dipole q. These are identical on the two backgrounds for this operator comparison, even though the resulting metric and rates differ.

## Metric solve

GR branch:

    Phi = -rho1/(2k^2) - 3HJ/(2k^3)
    Psi = Phi - Pi/k^2
    alpha_dot = Psi - H alpha
    Phi_dot0 = -R0/(2k^2) - 3(H_dot J + H J_dot)/(2k^3).

Poisson-spatial branch:

    Psi = -(rho1 - 3HE alpha)/(2k^2)
    Phi = Psi
    alpha_dot = Psi - H alpha
    Phi_dot0 = -R0/(2k^2) + G_dot alpha + G alpha_dot.

For these two branches (both factor=1 in the existing driver):

    Dmetric = 1 + 3Eq/(2k^2) > 0
    X = k alpha - (3/k)(Phi_dot0 + H_dot alpha + H alpha_dot)
    z = X/Dmetric.

The new dust-force branch is NOT introduced or substituted. The source of z is the stress/metric constraint, not an inversion of a measured monopole derivative.

## Monopole and finite increments

For native monopole d, scaling U0 and fixed dipole q,

    d_dot = -k(q + 4z/3)
    r0 = d_N/U0 = -(k/U0)(q + 4z/3)/H
    Delta r0 = -(k/U0)[q Delta(1/H) + (4/3)Delta(z/H)].

For arbitrary paired scalars A,B, exact finite increments satisfy

    Delta(AB) = mean(A) Delta B + mean(B) Delta A
    Delta(A/B) =
      [mean(B) Delta A - mean(A) Delta B]/(B_r B_t).

These are not tangent approximations. With L=Dmetric H:

    Delta(z/H) =
      [mean(L) Delta X - mean(X) Delta L]/(L_r L_t).

Split X into k alpha, -3Phi_dot0/k, -3H_dot alpha/k, -3H alpha_dot/k. Their four numerator contributions, the L-denominator contribution and q Delta(1/H) give six exactly additive contributions to Delta r0. The fixed-alpha numerator contribution is zero here and is retained as a check.

monopole_math.Pair applies these product/quotient identities with exact fractions of the saved binary primitives, checking every propagated increment against its endpoint difference. An independent90-digit Decimal implementation uses separately rearranged endpoint equations. Identity/swap controls test zero difference and sign reversal.

## Pair projection without changing the accepted source

The previous source-derived fluid identity gives

    U0 Delta r0 + U2 Delta r2 = -3p Delta[1/(tau H)].

For the same original observable covector a, the candidate pair contribution is

    (a0 - a2 U0/U2) Delta r0
      - 3a2 p/U2 Delta[1/(tau H)].

Everything outside this pair is retained from the original accepted source. Original adjoints, quadratic weights, phase Jacobians and reference scales are reused. The decomposition includes the six direct monopole contributions, clock damping and all other original coordinates.

The projection is a diagnostic counterfactual. Using the ORIGINAL conditional budget allows a like-for-like measure of change; it does not recompute or qualify all full-source Cauchy, phase, history or interpolation controls. No candidate is silently promoted to the live source.

## Execution contract

Freeze18nodes before new stress evaluation, including old even/new odd points; independently qualify them. Then evaluate only the remaining2024nodes on the EXISTING grid, reusing the18probe captures. At every point require the saved native backgrounds and rates to replay bitwise, plus the direct metric/rate algebra gate1e-10. Original numerical gate2e-5 remains untouched.

All full-grid source cases receive independent90-digit checks. Independent weighted integration and sampled forward-map versus covector projection checks provide a different verification route. Report normalized native-rate error separately from the possibly ill-conditioned difference of two almost equal rates. In particular a large relative change in a nearly zero baseline difference is not evidence of a large observable effect.

