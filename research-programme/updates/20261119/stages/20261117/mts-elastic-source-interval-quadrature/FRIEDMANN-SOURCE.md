# Derive the expansion-rate input, rather than interpolating it

In the two sampled parent cells, the largest single-input change to the integrated source comes from replacing the interior of -Delta H v_b0 with a line between its endpoints. To get this term from the retained matter/metric coupling, use the native flat-branch Friedmann constraint: in the notation of the metric packet, C=3 H²-sum_i B_i, B_i=8 pi G a² rho_i (c=1), H=a'/a on the dynamical branch. The packet also has a represented clock rate; it is not interchangeable with H. Direct subtraction gives the exact finite identity

    Delta H = (sum_i Delta B_i + Delta C) / [3(H1+H0)].

On the positive expansion branch the denominator is regular. A zero theoretical constraint does not authorize dropping a numerical or representation defect unless it is bounded on the scale of the response. Computing C by subtracting large totals in double precision is not an independent high-precision check.

With g=1/(1+alpha), the ordinary nonrelativistic components contribute (g-1)B0 and massless radiation contributes (g²-1)B0, with the small factors factored as in SLIP-EQUATION.md. For each massive neutrino eigenstate B=C_n a^-2 r(a m_n), write x=a0 m_n and use

    Delta B=(C_n/a0²)[(g²-1)r(x)+g²(r(x(1+alpha))-r(x))].

The last divided difference must use the actual native thermal function (including its region boundaries), not an assumed massless species. For each active quadratic scalar the local packet contains B=(v²+U²)/2, U=a m phi. On the same mass convention,

    Delta U = a0 m [alpha phi0+(1+alpha) Delta phi],
    Delta B = v0 Delta v + (Delta v)²/2 + U0 Delta U + (Delta U)²/2.

The scale and field differences must refer to the *same native original field jet* used in B0, not a close but unequal interpolated parent field. These formulae follow by finite differencing the existing common-metric constraint; they do not introduce a new force or a fitted coupling. Source: ../mts-coupled-metric-consistency-20261117/native/fortran/equations.f90 (flat adotoa) and native/fortran/mts_metric_hook.inc in that same directory (species energy, field jets and constraint readout).

Next implementation: compare each species contribution and the constraint/representation remainder against the direct native expansion change at the saved physical probe times before inserting the reconstructed forcing. Use separate scales for the large Friedmann terms and tiny response; certify neither from the former alone. Test baseline and MTS at both native step sizes. Follow with fresh cells, not a full-history promotion based on these two.
