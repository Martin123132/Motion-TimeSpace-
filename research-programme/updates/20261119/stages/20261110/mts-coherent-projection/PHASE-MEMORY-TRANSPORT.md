# Derived nonsingular first-order phase-stress transport

The displacement-curvature prediction is useful for the heavy branch but
ill-conditioned for the tiny slow-field pressure in both controls. In the
cold control it subtracts terms near2.48e-10 to recover a pressure near1.65e-24;
the saved result fails by millions of times that pressure. Do not suppress
this counterexample or infer a physical instability from the subtraction.

Instead retain pressure/phase in first-order variables derived from the SAME
native scalar equations. Let omega=sqrt(k^2+mu^2)>0 at the fixed k=1, and

    B=(b,v/omega)^T,    U=(us,ws/omega)^T,    M=B U^T.

There is one real coherent scalar, not a newly populated second quadrature.
The four entries of M obey two physical rank/direction constraints; U is
recoverable as M^T B/(B^T B). Since B^T B=b^2+(v/omega)^2, this division is
regular through individual field and velocity turning points. The zero-
background sector would need separate treatment; it is not used here.

With chi=omega'/omega=H*mu^2/(k^2+mu^2), the on-shell background and scalar
perturbation matrices are

    Ab0=[[0,omega],[-mu^2/omega,-2H-chi]],
    Au =[[0,omega],[-omega,       -2H-chi]],
    F=(0,-k*z*B2)^T.

Then U'=Au U+F, B'=Ab0 B on shell, and differentiating the outer product gives

    M'=Ab M+M Au^T+B F^T.                              (1)

This is first order and carries the phase products responsible for pressure.
The exact native stress readout is

    Ds=omega^2 M22+mu^2 M11,
    Ps=omega^2 M22-mu^2 M11,
    Qs=k*omega*M21.                                    (2)

Unlike the second-derivative virial prediction, slow-field(2) does not
subtract the much larger displacement and metric-force terms. No effective
sound speed, pressure fit, phase isotropization or arbitrary D0 seed is needed.
The initial M comes from the saved native field and velocity themselves.

## Source-history representation, not a new force

The accepted background interpolator has small but nonzero source defects.
Its equation-owned derivatives give

    delta=(H*b_N-v, (H*v_N+2H*v+mu^2*b)/omega)^T,
    Ab=Ab0+delta*B^T/(B^T B).

Hence Ab B equals the derivative of the actual source history, including its
recorded defects. This rank-one matrix extension is not unique off the
physical subspace; all such choices that agree on B describe the same exact
physical M=B U^T. The extension used here is fixed algebraically before
testing. It changes neither the native U equation nor the field action and
must not be promoted to a new physical interaction. Off-subspace drift is
checked numerically rather than interpreted as extra modes.

## Frozen test

Keep the902 original selected epochs, fixed extraction operator and all
physical inputs/tolerances. Advance M from its exact native first endpoint
for both cold+slow and MTS+slow/heavy. The metric/background history is the
saved coupled solution; THIS representation test is forced-history, not a
fresh coupled native evolution. The prior stage already supplies the native
coupled reference and is not rerun.

Use the same fine2/fine4/coarse4 RK4 controls as the retained canonical replay.
Keep original physical output times; internal substeps are only the numerical
refinement. A guarded a(tau) Hermite interpolation matches native a and aH
at each source knot; set H=a'/a on this interpolation. Derive Ab from that
same scale and the retained source interpolants. Interpolate the native z
history separately. The coarse control removes every other HISTORY knot,
not the output epochs or projection weights. No change to bank or acceptance.

Compare every stress history, weighted projected pressure, U recovered from M,
rank/direction constraint, and step/history refinements. Preserve failures
and absolute scales. A successful source transport supplies a stateful
alternative to forcing pressure to be an algebraic function of two averaged
moments; it does not by itself justify a positive temporal ensemble or a
globally averaged late-time closure.
