# Source-conditioned accumulated response, with physical endpoints

N=ln(a). Work with the retained first-response equation, original coefficients and original leading history. No action or physical coupling is changed.

## Exact decomposition

The preceding stage derived delta=eta+J and
    eta_N=M eta+fbar+r,  r=MJ-J_N.
The exact physical-clock mean of r is
    rbar=-mean_clock((Omega_N/Omega)J),
provided J is normalized by that clock at every N.

A numerical interpolation of that mean, denoted a(N), need not satisfy the continuous normalization exactly. Keep the distinction explicit:
    q=fbar+a,   g=MJ-J_N-a.
Then eta_N=M eta+q+g holds identically for ANY chosen a. Interpolation error is carried in g, not dropped. The new slow solution obeys eta_slow,N=M eta_slow+q with eta_slow(initial)=-J(initial), the SAME initial offset as the full solution.

Thus e=eta_full-eta_slow satisfies
    e_N=M e+g,   e(initial)=0.
Both physical reconstructions add the same final J, so the difference in a terminal physical observable is ell(T)e(T), with ell including ALL native, energy, coordinate-correction and periodic endpoint maps. The local zero e(initial) does not erase inherited physical error.

## Derived mean representation

At the saved65 auxiliary clock nodes, evaluate the complete retained primitive with the actual clock weights and its fixed-phase derivative. The scalar coefficient row
    a_j(N)=-mean_clock((Omega_N/Omega)K_j)
multiplies the unchanged forcing-history coefficients F_j(N).
Use a cubic interpolation of this row. A33-node control and independent interior evaluations check this auxiliary representation; no original physical grid is altered.

The complete slow forcing q is the product of cubic scalar rows (mu_j+a_j) with the original cubic forcing coefficients F_j. On a common knot subdivision this is a degree-six polynomial, obtained by exact coefficient convolution. This is an algebraic acceleration, not a new source interpolation. Verify it against direct products at independent interior positions before use. No forcing Fourier mode is deleted.

## Full-hierarchy adjoint and absolute budget

For each terminal physical row, lambda_N=-M^T lambda with lambda(T)=ell(T). The derivative of lambda^T e is lambda^T g. Therefore
    ell(T)e(T)=integral lambda^T g dN,
    abs(ell(T)e(T))<=integral abs(lambda^T g) dN.

For the two retained forcing components g_normal and g_map, report signed integrals separately, their sum, the absolute integral of their combined projection, and the sum of componentwise absolute integrals. This exposes cancellation rather than treating it as error-free closure.

The sparse transpose reverses every saved directed remote link. The compact matrix transposes normally. Verify its bilinear identity and equality to an independently assembled full sparse matrix, on several fixed interior points and vectors in BOTH branches. No tail truncation, phase-average surrogate for M, assumption of small norm(M)/Omega or imported reference-gain constant is used.

Adjoints integrate backward in bounded chunks, each retaining all1064(or baseline equivalent) state entries; chunking changes memory use only.8192 auxiliary quadrature intervals and their4096-interval subset test the signed/absolute numerical integrals. Time-control integrations use the same4096/2048 caps, DOP8532e-12/2e-14, and terminal normalization. Endpoint maps and allten observables are tested on independently chosen vectors against the existing native evaluator.

## Relation to actual physical approximation

Freeze slow and adjoint predictions before reading the saved full-response perturbations for comparison. The existing full-response calculation provides an independent forward check of the signed accumulated prediction. All comparisons use the unchanged gates and retain baseline as the zero-rapid-phase control.

These budgets concern dropping g from the retained FIRST response. They are NOT the total difference from an exact MTS trajectory. If y1=y0+delta is the first response to y_N=(M+R_total)y, then the omitted first-response term is R_total delta. The total-error equation additionally includes R_total e, inherited error and the source/background defect. Any later physical claim must combine those terms with a justified response bound; this stage does not assign them numerical values it has not derived.

A sampled Simpson integral is not a rigorous continuous-time enclosure. Keep numerical convergence, signed identity, absolute inequality and original physical comparisons distinct. A failure of a diagnostic or a budget too loose for the intended use is reported as such; it does not authorize changing tolerances or resetting the physical mode.
