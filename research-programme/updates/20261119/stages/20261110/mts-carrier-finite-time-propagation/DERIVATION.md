# Finite-time conditional propagation and accumulated defect

This stage tests the derived first carrier correction through time, using the original saved initial state, homogeneous background and rest-source history. It does not change the action or test parameters. The qualifier conditional is essential: heavy self-gravity is evolved, but the other species' metric contribution is prescribed rather than independently recalculated from their perturbed state.

## Exact conditional reference

At the retained k=1/Mpc, write the native metric as

    z=zeta+(v*w+mu^2*b*u)/(2H),

where zeta is the rest/slow-species contribution and the heavy perturbation is (u,w). Substitution into the retained field equation gives the genuinely evolved reference

    u'=w,
    w'=[-omega^2-mu^2*b*v/(2H)]*u
        +[-2H-v^2/(2H)]*w-v*zeta,
    omega^2=mu^2+1.

Thus the heavy contribution is not frozen at its saved future value. Given the same prescribed rest and background histories, this reference must recover the saved native trajectory before its reduction error can be interpreted.

The actual CDM control has normalized density Dc=beta*Rc*delta_c and constant f=beta*Rc, with

    Dc'=-f*Dc/(2H*beta)-f*zeta.

It is evolved under the same conditional separation, not replaced by a fictitious scalar oscillator.

## Histories and initial conditions

The original 65-node live interval and 902-node extraction retain all output epochs. Cubic Hermite histories use saved values and checked first derivatives of a,H,zeta and, for MTS, b,v. At evaluation time mu=a*m, beta=a/R0 and all derivative/phase quantities follow consistently from these histories. Any interpolation representation defects therefore remain present rather than being declared zero.

For zeta', differentiate the source subtraction explicitly. With normalized heavy or dust density YD,

    zeta'=z' - [YD'-(r+H'/H)*YD]/(2H*beta).

The heavy live branch uses its saved current-native H'/z'; other cases use the previously checked memory-budget derivative. These are prescribed histories in THIS experiment, not a new live future-free RHS. Only initial heavy perturbations enter the reduced evolution; future heavy perturbation samples are not supplied to its RHS.

Each original initial primitive and derived coordinate transform is frozen before integration. Numerical scaling uses only that initial state and RHS. Dense versus every-other history knots test interpolation sensitivity separately from halving the integration maximum step. No physical bank, mass, wavelength, normalization, output grid or tolerance changes.

## Derived reduced evolution

The preceding stage supplies X=M(t)*(u,w), where X=(d,q), and

    x=(d,q,zeta)=P(t)*y, P=I+K,

with its derived first generator B_eff including both the commutator and physical phase/background drift. The first two reduced entries evolve independently as

    y2'=A_eff*y2+B_eff[1:2,3]*zeta
         +(P^-1*e3)[1:2]*zeta',

where A_eff is the upper-left 2x2 block. The third component remains the prescribed zeta. The metric response compensation is retained. Reconstruct X and then (u,w) through the original exact maps before comparing primitive fields and physical density/current/pressure. The same readout is applied to exact and reduced states.

The forward reduced RHS depends on its own current state and prescribed histories. The exact reference and the error channels do not feed their solutions into it. They share a numerical integrator only to use the same independent variable and declared precision.

## Defect transport, not residual fitting

Transform the evolved exact conditional solution to y_exact and differentiate it using the primitive equations and exact chain rule. Its defect with respect to the proposed generator is

    f_defect=y_exact'-(A_eff*y_exact+forcing).

With identical initial data, define e=y_exact-y_reduced. Linearity yields

    e'=A_eff*e+f_defect, e(t0)=0.

A separate error channel integrates this equation. The reconstructed y_reduced+e must recover y_exact at the algebra gate. The defect is derived/evaluated from the reference equations, not fitted to the difference of final states. Crucially, it is NOT added to the forward prediction and does not turn a failed reduction into a passing one.

For a componentwise envelope define A_abs with the SAME diagonal as A_eff and absolute off-diagonal entries. The comparison equation is

    B'=A_abs*B+abs(f_defect), B(t0)=0.

For an exact integration of a continuous linear system this bounds componentwise abs(e). Here it is numerically evaluated with the same frozen solver/refinements and checked at the saved epochs. Consequently the reported envelope is an a posteriori numerical conditional bound, not a certified continuum enclosure.

At each output, convert that envelope to physical stress using the absolute value of the composed linear map from reduced error to primitive variables and then native normalized stresses. This preserves signed physical predictions while using absolute coefficients only for the error envelope.

## Interpretation

A native-reference pass validates the conditional numerical setup. A reduced-state/stress pass tests this derived approximation on that setup. Neither establishes the response of newly evolved rest species, an independently predicted occupation, or compatibility with a different late-time background. The next coupled test must retain the full current-state rest response and original matching conventions.
