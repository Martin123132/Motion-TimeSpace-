# Stable coupled scalar rows, following a preserved failed check

The first `half/drift-01` run is NOT accepted. Its spatial-Poisson drift
width difference is 2.5614709915e-5 against the unchanged 2e-5 gate.
GR gives 1.3659571884e-5. The spatial-Poisson absolute difference is
3.6595231984e-9, and the complete remainder differs by 8.5530483556e-8
relatively. Passing the latter does not excuse failing the drift check.

`half/drift-diagnosis/result.json` isolates the dominant discrepancy to
heavy density row151, gauge column0, not a changed radiation-tail row.
The original route subtracts the large carrier and gauge-coordinate
derivatives after native matrix transformations. It agrees with the
independently derived scalar equations on individual native vectors, but
differentiating those small residuals amplifies cancellation error.

The repair is an exact row identity, not smoothing or a changed step.
It reuses the already derived relative scalar generator A and its metric
forces F=(force_Psi,force_PhiN):

    G_h = A selector_h + F L.

The closed map has R_r=selector_r and R_N,r=0. Thus B_r=G_r S and

    B_h = R_hh G_h S + R_hr B_r + R_N,h S.

For the core-to-tail block the relative scalar has no direct l=3 source,
so B_h,tail=R_hr B_r,tail. All other matter and tail rows are reused
unchanged. This avoids subtracting the scalar carrier at the last step
while retaining metric feedback, phase correlations and the background
derivative of R. `stable_rows.py` evaluates this identity from saved
packets; `collect_stable.py` applies the same identity to fresh shifted
coefficients at the remaining inherited wavelengths.

`stable-01/` is separate output. The failed packets and receipts stay
intact. Phase quadratures64/128/256, drift widths0.002/0.001, inner
derivative width0.01, physical bank and gates are unchanged. We compare
the repaired and original equations before accepting the repair. Extra
precision from numpy.longdouble is platform-dependent; the algebraic
identity, not an assumed wider floating type, is the essential change.

## Physical interpretation of the mean's heavy block

The leading self-density contribution to W_N is

    [alpha^2/4 - b] delta,
    alpha=k^2/(amH), b=rho_h/(2H^2).

Here alpha^2/4 is scalar wave pressure and -b is Newtonian self-gravity
from (k^2/H^2)Psi with Psi_h=-rho_h delta/(2k^2). Other matter remains
an explicit source; GR current, shear, metric-time derivatives and
finite-phase corrections remain in the computed coupled mean.

At the qualified EARLY state, b=0.3346518601. The three pressure terms
are about0.0148218,0.237149 and3.794377. Thus the leading self-density
coefficient changes sign across the retained wavelengths. This is the
expected competition between attraction and scalar pressure, not an
observational fit or a complete stability result for the coupled system.

The mean's Euclidean logarithmic norms in the inherited mixed coordinate
weights are large at this early state (roughly407,809,1614 for GR).
Those constants must NOT be extrapolated into a useful long-interval
error certificate. A bound for the actual cold transfer must exploit
the physical energy/constraint structure or the retained prepared mode,
and include background replacement and endpoint maps. The exact remainder
formula supplies the necessary operator; sampled convergence does not
by itself supply that long-interval bound.
