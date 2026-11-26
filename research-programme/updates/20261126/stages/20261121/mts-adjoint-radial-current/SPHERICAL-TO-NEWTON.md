# Deriving the spherical evolution that the refined centre needs

This is the spherical sector of the retained common-metric Einstein equations, not a new hypothesis about galaxy occupation. The enclosed mass used here is the [Misner–Sharp mass](https://doi.org/10.1103/PhysRev.136.B571); the historical treatment is for a spherical ideal fluid. Below the radial pressure, tangential pressure and momentum of our source are independent, and constraint defects are retained. The known notion of spherical mass is not an original MTS result.

Use c=1, E,p,t,j equal to 8πG times the physical orthonormal energy density, radial and tangential pressure, and outward momentum density. Proper-time gauge, no time shift: dl²=A²dr²+B²dΩ². Define D_s=A⁻¹∂r, U=D_s B, v=∂t B, k=∂t log A, K=−k−2v/B. The geometric mass (length) is m=B(1+v²−U²)/2. Do not evaluate a tiny mass by a naive subtraction from one; use the factored expression in mass_on_history.py. Let

    Eg = 2m/B³ + 2(kv−D_s U)/B,        Jg = 2(D_s v−kU)/B,
    C = Eg−E,                          P = Jg−j.

These are geometric density and radial momentum, and their differences from the physical source. They are not equations imposing C=P=0. Curvature of spheres gives spatial Ric_nn=−2D_s U/B and Ric_perp=(1−U²−B D_s U)/B². Substitution into the actual trace-reversed spatial ADM evolution gives

    Bdot=v,                     vdot=−m/B²−B(p+C)/2,
    Udot=B Jg/2,                kdot=2m/B³−k²+p−(E+p+2t)/2−C,
    D_s m=B²[U(E+C)+v Jg]/2,   mdot=−B²[v(p+C)+U Jg]/2.

Five independent symbolic cancellations test the identities for arbitrary input values, not just a constraint-satisfying ideal fluid. On the outward branch U>0, recover U=+sqrt(1+v²−2m/B), A=B'/U, k=(D_s v−B Jg/2)/U and Eg=(2D_s m/B²−v Jg)/U. The inverse and Udot recovered via mdot have three additional algebraic checks. The geometric momentum update on this branch is

    Jg_dot = (K−k) Jg − D_s C − D_s p − 2U(p−t)/B .

It follows from the covariant momentum identity of the retained ADM system, using a unit radial component instead of a coordinate one. The pressure flux is actual stress; it is not inferred from Jg. Independently differentiated matter j must satisfy the same balance without the C gradient if there is no external work. An exchange defect belongs explicitly on the right of the constraint propagation law. Never replace Jg with j, or Eg with E, to initialize subsequent time steps. No integral over density is needed to evolve an independent geometric mass. The outward chart has to be patched rather than used blindly at U=0.

**Newton check.** When the constraints hold, and the normal-frame radial stress/current and velocities are negligible, D_s m≈B² U E/2 and Bddot≈−m/B². Restoring units yields dM_phys/dB=4πB² rho and d²B/dτ²≈−GM_phys/B² for the areal radius of a freely falling radial shell. Finite radial pressure adds −4πGB p_phys/c² in this gauge; this is not a test-particle force law in arbitrary coordinates. The normalization of G was already retained. This reduction identifies *where* the MTS energy, stress and flux enter, not why the coupling has its measured value. In vacuum on the constraint surface m is constant in space and time.

**Numerical implementation tested here, flat linear sector only.** m=r(ell−b−r b') at linear order; m=O(r³). C=2 Dm/r²−E at cells and P=−2 mdot/r_f²−j on interior faces. Use the adjoint face gradient G and divergence D, endpoint masses fixed in the closed test. The source-driven equation is

    mddot = r_f² G(Dm/r²) + r_f²[(div S)_r−GE]/2 .

It gives Cdot=−D(r_f² P)/r²−(Edot+div j) and Pdot=−G C−(jdot+div S) even with independent nonzero external residuals. Its vacuum energy is h/2 times the sum of (mdot/r_f)² on interior faces and (Dm/r)² on cells. It is positive, with the spatial part equal to the adjoint product. The test checks m=r³,r⁵,r⁷,r⁹ at the centre, a nonzero constrained-error wave against the analytic spherical standing wave, and independent material work. This is a constraint propagation test, not monopolar gravitational radiation. The separate quadrupolar tensor test is retained.

**Where this goes next.** Carry (B,v,m,Jg) into the fully curved evolution with actual saved stress, the correct geometric current and regular centre reconstruction. Keep geometric mass and momentum perturbations independent of the matter density and current. The saved slice check shows that the original/full spherical centre error is visible in the areal acceleration, even where a volume-weighted mass-work statistic looks small. Compare the *actual areal acceleration*, both constraints, and the unfrozen proper-ruler tides; do not select only a mass integral that passes.
