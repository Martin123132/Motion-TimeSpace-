# Metric-output precision is distinct from background accuracy

The native equations.f90 declares OutputTransfer as default `real`, while
the field/velocity diagnostics are double precision. The retained Weyl,
v_newtonian_cdm and delta_cdm columns are verified to be exactly float32
representable in both cases. Merely storing those outputs in a float64
NumPy array does not recover their missing precision.

For nearest IEEE float32 rounding let eV,eW be half the larger neighboring
ULP of the saved velocity and Weyl columns. At k=1, with the saved H and eta
held fixed,

    e_alpha=|H| eV,
    e_Phi=|H| e_alpha,
    e_Psi<=2 eW+e_Phi.

The cubic interpolation is linear in its input values. A piecewise cubic
cardinal basis C_j(t) gives |error(t)|<=sum_j |C_j(t)| e_j. The script
bounds each interval by the sum of the absolute polynomial coefficients
times the corresponding interval powers, rather than only checking a
few values of the cardinal functions.

For the slow canonical scalar write Y=(omega_ref*u,p), where omega_ref is
the largest oscillator frequency on the interval. Its homogeneous matrix
is [[0,omega_ref],[-Omega(t)^2/omega_ref,-2H]]. With H>0, its logarithmic
Euclidean norm is bounded above by

    beta = max |omega_ref-Omega(t)^2/omega_ref|/2.

If the forcing uncertainty has norm <=F and the initial state uncertainty
has norm <=E0, then E(t)<=exp(beta*t)E0+(exp(beta*t)-1)F/beta, with the
continuous beta=0 limit. Add the final gauge-readout uncertainty separately.

The implemented numerical envelope uses the sampled background force maxima
and ordinary float64 arithmetic, not directed-rounding interval enclosures
of every background coefficient. It is therefore a documented conservative
precision ESTIMATE, not a formally certified global error bound. Primitive
integration errors, background defects and unknown original metric dynamics
are outside this estimate.

The cold slow-field discrepancy is at most 0.5192 of this estimated field
envelope and its momentum discrepancy at most 0.06942 of the momentum
envelope. This is consistent with a precision-limited comparison; it does
not establish rounding as the unique cause or reverse the original failure.
The heavy-case slow-field discrepancy exceeds this estimate by about
9.49e4, so rounding cannot plausibly explain its dominant background defect.

The direct derivative-based metric-defect replay is retained but not accepted
as a precision repair: differentiating quantized density/velocity outputs
worsens several small-source comparisons. The derived derivative-free
synchronous momentum and a future full-precision native state/readout are
the appropriate routes, not a fitted cancellation of that diagnostic.
