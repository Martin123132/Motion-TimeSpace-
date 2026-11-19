# Between-epoch source variation: equation-owned integral and response control

## Retained problem

The preceding `mts-external-current-curvature-20261112` prediction is unchanged. The selected own field and metric evolve together; the external sources are D_o and Q_o. Their values, first derivatives and second derivatives at each of the 902 signed preparation nodes were already derived from the native equations. This stage controls the difference between that frozen quadratic source and the surrounding time-dependent source. It does not change an action, physical parameter, scattering bank or physical integration grid.

Let F denote either external channel, t_i a preparation time and s elapsed conformal time. With K=F'', the exact quadratic remainder is

    F(t_i+s) - F_i - s F'_i - s^2 K_i/2
      = integral_0^s (s-u) [K(t_i+u)-K_i] du.

This needs F' absolutely continuous, not a globally continuous third derivative. In this retained regime the native layout/approximation branch stays fixed. The background splines and thermal interpolation supply piecewise derivatives; their curvature jumps must be treated one-sidedly. No derivative across a corner is silently substituted.

For a numerical piecewise polynomial Khat, define

    V_i = sup_[t_i,t_i+T] |Khat(t)-K_i|,
    epsilon_i >= sup_[t_i,t_i+T] |K(t)-Khat(t)|.

Then the source remainder obeys |e_i(s)| <= s^2 (V_i+epsilon_i)/2. The two channels have separate bounds. The saved absolute adjoint gains already include the s^2/2 weighting. For output c,

    |delta O_c(T)| <= sum_i |weight_i| sum_channel G_i,c,channel (V_i,channel + epsilon_i,channel).

The signed preparation weights are never replaced in the physical prediction; absolute weights occur only in this upper estimate. Saved gain-refinement allowances are added, not silently discarded. These are the existing numerical final-epoch gains, not new interval-certified gains or all-epoch guarantees.

## Polynomial enclosure, not a fitted physical law

Divide each original saved gap at the actual field and thermal interpolation boundaries. On each resulting cell, use five native curvature values (the two one-sided endpoints and three interior quarter/midpoint points) to construct a degree-four numerical reconstruction. These coefficients are quadrature/interpolation data, not new theory parameters and not fitted to final residuals.

With normalized cell coordinate v, Khat=sum_k a_k v^k. Restrict the polynomial to any clipped subinterval v=l+(r-l)w. Its power coefficients are

    a'_j = sum_(k>=j) binomial(k,j) a_k l^(k-j) (r-l)^j.

The Bernstein coefficients on 0<=w<=1 are

    b_j = sum_(k<=j) a'_k binomial(j,k)/binomial(4,k).

The Bernstein basis is nonnegative and sums to one. Therefore max_j |b_j-K_i| encloses |Khat-K_i| throughout that cell, including clipped ends. `cell_math.py` uses this identity, not the largest sampled value, for V_i. The identity is exact in exact arithmetic; floating coefficients and gains are not outward-rounded interval certificates.

For a cell starting at a with width h, the weighted source integral over normalized limits l,r has the closed expression

    sum_k a_k h [ (t_end-a)(r^(k+1)-l^(k+1))/(k+1)
                  -h(r^(k+2)-l^(k+2))/(k+2) ].

Summing cells keeps finite curvature jumps explicit. Synthetic affine/quartic, clipping, finite-jump and Bernstein controls exercise this independently of the physics packets.

## Native probe independence and the repaired corner mistake

At every saved native epoch, copy the full evolution state and its layout. Advance only this copy to the diagnostic times. Do not insert times into the original solve. Check layout identity, native equation regime, collision cancellation and original saved outputs. All original 224-column packets for the selected mode remain byte-identical. Main native source changes are limited to the readout hook and its dispatch/storage; the dynamical equations are untouched.

The first one-sided probe rule used offsets as small as 1.28e-13 Mpc. At two MTS thermal corners the floating logarithmic cell lookup rounded both sides onto the right branch. Requested time signs alone were insufficient to establish sidedness. Native packet column 18 exposed this:

- tau=89.46162540548127: expected cells 305050/305051; obtained 305051/305051.
- tau=89.63583293099947: expected cells 305093/305094; obtained 305094/305094.

The two left/right pairs were reacquired at offsets 1e-10 Mpc, smaller than the adjacent cell widths; native branch identities now match. Actual sample times, rather than falsely exact boundary times, enter the polynomial abscissas. The baseline had no wrongly sided thermal pair, but receives the same actual-abscissa treatment and fresh validation.

All failed diagnostic results remain saved. After the repair, predictions at fresh one-sixth/five-sixths positions were frozen before native evaluation: 2,396 baseline and 3,246 MTS tests. They pass the same 2e-5 gate. These are independent numerical probe times, not independent observational data or new galaxy/cosmology validation.

## What is controlled, and the remaining mathematical clause

The reconstructed curvature has an analytic cellwise enclosure. Its response estimate is small, and fresh native probes test its accuracy. The observed largest probe discrepancy plus restarted-endpoint discrepancy is carried as a numerical working allowance. It is NOT a proof that the true error has that supremum everywhere.

For final MTS pressure, after the reconstructed variation and observed numerical allowance, the remaining absolute margin is 4.7709724635968885e-9. A sufficient additional uniform residual requirement, in the retained native channel units, is

    9.662590567957012e-6 epsilon_D
      + 1.1984110932221908e-7 epsilon_Q <= 4.7709724635968885e-9.

Here epsilon denotes additional true-versus-polynomial curvature beyond the already budgeted numerical allowance; neither channel is assumed zero. Proving this continuously requires analytic derivative/enclosure work or validated numerics. This stage does not assert it from finite samples. The next direct evolution test can use the tested numerical reconstruction while keeping that qualification explicit.
