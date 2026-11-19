# Additional controls, fixed before transport runs

Use analytic sideband rotation/amplitude transport with8,16and32point
Gauss-Legendre integration of the beat phase. Retain all399rows in both
models. Compare the old full WKB template, the newly derived second-order
template, the saved retained closure and saved first-order completion.

For these source-coordinate comparisons, delta and S are initially held
fixed. Their microscopic initial q,p need not agree between reduction
orders. Therefore these differences are branch/interface comparisons, not
automatically truncation errors of one fixed microscopic initial state.

Independent exact KG controls use constant-H Bessel solutions with
nu^2=1-(k/H)^2. Test the homogeneous k=0carrier and the saved mode nearest
each of1e-5and.001inverseMpc. These nonstiff high-precision controls are
chosen before seeing their answers. Compare the same exact canonical
initial data/transfer operator, and compute coefficient-norm errors for
both WKB orders. The analytic certificate, not these three controls alone,
covers the complete frozen wave-number rectangle.

Use80decimal-digit arithmetic for the exact comparisons. Clearly separate
the analytical truncation bound from machine-precision transport errors;
ordinary double-precision output is not accurate to21digits merely because
the mathematical template has a tiny residual.
