# Identified candidate mechanism: a missing gravitating source in late RSA

This is an implementation-level approximation audit, not an amendment to
the retained covariant parent action or a new fitted coupling.

The retained native equations.f90 (derivs, approximately lines 2274-2347)
forms DM from baryons, CDM and massive neutrinos. It computes late photon
and massless-neutrino radiation-streaming approximations (RSA) before
adding dark-energy stress. MTS's heavy matter-like scalar is implemented
inside that dark-energy component. The order therefore matters even when
its mean equation of state is nearly dust-like.

The active native RSA has, in synchronous coordinates,

    zM=(DM/(2k)+k eta)/H,
    qr=qg=-4 zM/3,
    dzM=-H zM-DM/(2k),
    delta_r=-4 dzM/k,
    delta_g=delta_r-4 opacity(vb+zM)/k.

The later gravitational RHS instead uses

    zfull=(Dtotal/(2k)+k eta)/H,
    eta'=Qsync/(2k).

For either radiation species with R=8piG a^2 rho, the exact energy defect
under the saved gauge map is

    ED_r=R[delta_r,s'+k q_r,s+4k zfull/3]
        =R delta_r,s'+2R(Dtotal-DM)/(3H).

This identity uses the source's actual time derivative. It does not invoke
the Einstein momentum equation or a zero residual. Decompose
Dtotal-DM into heavy scalar, slow scalar and radiation feedback. The
measured components determine whether the omitted heavy source accounts
for the discrepancy; a visual similarity or a search result is insufficient.
Photon momentum diagnostics separately subtract the retained Thomson
exchange, evaluated from the baryon RHS.

The identity uses the retained homogeneous radiation equation R'=-2HR and
the live eta'=Qsync/(2k) equation. If those background/clock equations are
represented imperfectly, their residuals must accompany it: in particular
(R'+2HR)(delta_s-4H alpha) is an additional energy term. Numerical finite
differences are not asserted to satisfy these equations exactly. The
measured comparison retains its unchanged gate for both branches.

## Derived leading correction to test next, not yet applied

If a missing synchronous stress (DS,PS) belongs in the gravitating RSA
source, the leading trace/constraint approximation gives

    Delta z=DS/(2kH),
    Delta z'=-H Delta z-(DS+3PS)/(2k),
    Delta q=-2 DS/(3kH),
    Delta delta_r=(4DS+6PS)/k^2,
    Delta delta_g=Delta delta_r-4 opacity Delta z/k.

This retains the pressure source. A pressure gauge transformation must be
derived from the actual carried background, not assumed dust at the
perturbation level. Neglected radiation feedback, time-derivative orders
and optical terms must remain separately identified. This is a leading
RSA correction, not an exact conservation theorem or a valid closure at
all wavelengths/times.

A forward test must insert the changed radiation density/current into the
metric AND the species evolution, including photon-to-baryon drag. Merely
changing the final observer, forcing Ephi=0, or subtracting a measured
residual would conceal rather than repair the issue. Preserve the original
DLL and old results; use an isolated source-complete comparison with the
same cold control. The present stage diagnoses the existing approximation
and does not silently replace it.
