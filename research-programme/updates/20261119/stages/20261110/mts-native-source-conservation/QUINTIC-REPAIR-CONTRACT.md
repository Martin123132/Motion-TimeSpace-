# Equation-derived heavy interpolation candidate

Knot-split source attribution explains the heavy background/Friedmann
residual to1.88e-8 of its own amplitude after explicit scale-interpolation
accounting. The heavy scalar also predicts the dominant shear defect;
~1.3% of that small residual remains unassigned, and baseline has a distinct
residual. Do not declare complete shear closure or set other sources to zero.

Test the actual owner: native FieldValues independently cubic-interpolates
b(N) and v(N). Replace this only in a separate candidate with endpoint
quintic Hermite values. Keep ALL original heavy N,b,v nodes and original
physical parameters. Supply H and H_N from the same native standard species
plus retained scalar energy/pressure. Obtain standard densities read-only
from the retained native model; this is not fitting a new background.

The original field equation fixes at each node:

    b_N = v/H,             v_N = -2v-mu^2*b/H,
    b_NN = v_N/H - v*H_N/H^2,
    v_NN = -2v_N -(2mu^2*b+mu^2*b_N)/H +mu^2*b*H_N/H^2,
    H_N = -(R+3P)/(6H).

Use the unique quintic matching value, first and second derivatives at both
ends for each component. Its coefficients are determined, not learned.
This is a higher-order numerical representation of the retained equations,
not an exact new solution of those equations. Preserve knot values exactly;
test derivatives, component defects and independent native/Python evaluation.

If implemented natively, keep the original library intact, retain old
behaviour until explicit heavy-clock data are supplied, and test cold/MTS
with the same original output grid, phase window, native accuracy and
componentwise2e-5/algebra1e-10 gates. No tight-coupling guard bypass, new
shooting, new data, branch fitting or defect forcing is allowed.
