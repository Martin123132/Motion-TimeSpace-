# Moving finite-collar source: action, clocks, recoil and curved-history variation

Private derivation checkpoint, 2026-09-14. This extends the previous **continuum GR control**, not an observational claim or the unrestricted MTS-to-GR limit.

Conventions: c_light=1, with the same reduced spherical/angular normalization as the existing action. Numerical radii, source mass and amplitudes are normalized control inputs, not SI predictions. V denotes radial coordinate speed; it must not be confused with the preceding GR run's proper radial rate db/dtau.

## 1. What is actually new

The source is no longer held at a fixed radius in the scalar regulator test. Its acceleration follows from varying one scalar-plus-source action. Both the reference and MTS/Gram branches retain their complete old spatial factors. No source force is imported from the previous continuum calculation.

There is also an explicit curved-history moving-factor action candidate, with its necessary transport weights and link variations derived below. A manufactured-history variation check is not a coupled curved evolution.

The qualifications matter:

- The **minimal proper-time embedding extension**, ideal reflecting trace and a specific nodal derivative lift are declared choices. The fixed-radius action alone does not prove their uniqueness or forbid additional material interactions.
- The inherited unforced reservoir value S=0.003 is an input, not a newly derived fundamental mass.
- The numerical flat pilot uses three positive collar quadrature layers. They move independently; there is no artificially imposed rigid-width source. This is not a proof that a physical material collar remains rigid, nor a curved cross-layer convergence theorem.
- The flat initial annulus is [3,6], with an outgoing amplitude0.01 preparation. These choices permit full reflection before the inner boundary is reached. This is not the old held-source pulse rerun with different labels.
- We do not withdraw the earlier rigid-source stress/NEC failure.

## 2. The reservoir connection is a derivation, not a new mass postulate

The source term already present in `DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md` is

\[
 I_{\rm app}=\int dt\,dz\,w(z)
 [E\dot\theta-\ell E+\ell\lambda(\chi-D_z(\theta))].
\]

On the unforced branch \(D_z=0\), theta is cyclic: \(\dot E=0\).
At fixed conserved \(E=S>0\), Routh reduction subtracts \(S\dot\theta\), retaining its endpoint accounting when comparing actions. With the reflecting constraint imposed, the reduced term is \(-S\ell\). Dropping \(E\dot\theta\) without this fixed-momentum reduction would not be justified.

Use the inherited metric convention

\[
 ds^2=-N^2dt^2+\frac{(dR+\beta dt)^2}{U^2}+R^2d\Omega^2 .
\]

For a minimally embedded source \(R=b(t)\), \(V=\dot b\),

\[
 \ell=\sqrt{N^2-(V+\beta)^2/U^2},\qquad
 p_b=\frac{S(V+\beta)}{U^2\ell},\qquad
 H_b=N\sqrt{S^2+U^2p_b^2}-\beta p_b .
\]

The positive-energy branch is selected by \(N,U,S,\ell>0\).
At a static zero-shift source this is \(H_b=NS\), not \(NUS\).
The metric-source variations are

\[
 \partial_N L_b=-SN/\ell,\quad
 \partial_\beta L_b=p_b,\quad
 \partial_U L_b=-S(V+\beta)^2/(U^3\ell).
\]

This identifies a concrete continuation of the existing constant-energy source. It does not derive arbitrary matter content, reflectivity or all parent coefficients.

## 3. Motion changes the clocks and the spatial weight

Write a material map per layer

\[
 R(t,\xi)=a+H(t)\xi,\quad H=b-a>0,\quad W=R_t=\xi V
\]

(the link tests also allow a moving inner anchor). A dot on the material scalar \(\psi(t,\xi)=\chi(t,R(t,\xi))\) differs from the old fixed-areal-radius derivative:

\[
 \chi_t=\psi_t-\frac{W}{H}\psi_\xi,\quad
 \chi_R=\frac{\psi_\xi}{H}.
\]

The old physical horizontal connection and positive spatial coefficient are

\[
 c=\frac{\beta}{N^2U^2-\beta^2},\quad
 C=R^2NU\left(1-\frac{\beta^2}{N^2U^2}\right).
\]

Pulling back the **same physical horizontal distribution** gives

\[
 d=1-cW,\qquad
 \widetilde c=\frac{cH}{d},\qquad
 \widetilde C=\frac{Cd^2}{H}.
\]

The regular chart used here requires \(d>0\) along the links, as well as positive lapse, U, C and timelike sources. At a timelike endpoint in the positive-C physical chart, endpoint transversality follows from

\[
 d=\frac{N^2U^2-\beta(\beta+V)}{N^2U^2-\beta^2}>0,
 \quad |\beta|<NU,\quad |\beta+V|<NU.
\]

Thus it is not a new independent endpoint material restriction in that chart. Endpoint timelikeness alone does not control every interior mesh/link trajectory or provide uniform bounds near a degenerate chart.

A common wrong shortcut would keep \(C/H\) while changing the link paths. The missing \(d^2\) is not optional. Likewise, flat physical spacetime has \(\beta=c=0\), so its old physical horizontal links remain simultaneous. Mesh motion belongs in the convective derivative; it must not be mistaken for a newly physical shift connection.

The exact continuum transformed action density is

\[
 \frac{HR^4}{2C}
 \left(\psi_t-\frac WH\psi_\xi\right)^2
 -\frac{\widetilde C}{2}
 \left(\psi_\xi+\widetilde c\psi_t\right)^2 .
\]

Direct expansion gives the ADM expression

\[
 \frac{HR^2}{2NU}
 \left(\psi_t-\frac{W+\beta}{H}\psi_\xi\right)^2
 -\frac{NUR^2}{2H}\psi_\xi^2 .
\]

This identity is exact, including nonzero shift and motion. At V=0 it returns the old static-coordinate expression; at c=0 it gives the flat moving action used below.

### Endpoint clock Jacobian

Alternatively integrate the old physical link \(dT/dR=c(T,R)\) from a moving anchor \(a(s)\) to a moving node \(R_i(T_i)\). If \(J_{\rm bulk}\) is the fixed-endpoint physical flow derivative,

\[
 \frac{dT_i}{ds}
 =J_{\rm bulk}\frac{1-c_aV_a}{1-c_iV_i},\qquad
 J_{\rm proper}=\frac{\ell_i}{\ell_a}\frac{dT_i}{ds}.
\]

For fixed physical c, endpoint shape variations satisfy

\[
 \delta T_i=
 \frac{-J_{\rm bulk}c_a\,\delta a+c_i\,\delta R_i}
      {1-c_iV_i}.
\]

Metric variations add the usual bulk connection variation. Independently integrating the material connection \(\widetilde c\) automatically includes the endpoint factors. The two integrations agree in the nonconstant manufactured metric test. Using \(J_{\rm bulk}\) alone demonstrably fails that test.

## 4. A complete-factor curved-history action candidate

Keep the old factor matrices \(B_{fi},S_{fi}\), including every MTS Gram row; \(S\) here is a sampling matrix, not the source energy. Let the fixed material spacing be \(\delta\xi\), and use each factor's material sampling-centre as its anchor. Solve

\[
 \partial_\xi T=\widetilde c(T,\xi),\quad T(s,\xi_f)=s,\quad J_i=\partial_sT_i .
\]

Define the uncut full-factor quantities

\[
 A_f=\sum_iB_{fi}\psi_i(T_i),\quad
 D_f=\sum_iS_{fi}J_i\widetilde C_i(T_i),\quad
 I_{\rm spatial}=-\int ds\sum_f\frac{A_f^2D_f}{2\delta\xi}.
\]

The nodal kinetic term is the positive quadrature of
\(HR^4( \psi_t-WD_\xi\psi/H)^2/(2C)\), using the same declared base derivative lift as the flat action. Add the proper-time source and the old reflecting multiplier, or eliminate the trace with its induced shape variation.

This candidate reduces **exactly at the finite-factor level** to the original static-node scalar action when the material map is time independent. In the flat chart it is the moving regulator below. It is not obtained by claiming that a fixed-boundary proof already covers moving boundaries.

The full shape derivative is explicit:

\[
 \delta A_f=\sum_iB_{fi}(\delta\psi_i+\psi_{i,t}\delta T_i),
\]
\[
 \delta D_f=\sum_iS_{fi}
 [\delta J_i\,\widetilde C_i+
 J_i(\delta\widetilde C_i+\widetilde C_{i,t}\delta T_i)],
\]
\[
 \delta I_{\rm spatial}=-\int ds\sum_f
 \frac{2A_fD_f\delta A_f+A_f^2\delta D_f}{2\delta\xi}.
\]

Here values are evaluated on their own links. The endpoint variation and its anchor-time derivative are propagated, not frozen:

\[
 (\delta T)'=\widetilde c_t\,\delta T+\delta\widetilde c,\quad
 \delta J=\partial_s\delta T .
\]

At fixed material coordinates, total variations include the physical metric evaluated at the moved radius. In terms of those total variations,

\[
 \delta\widetilde c=
 \frac{H\,\delta c}{d^2}+\frac{c\,\delta H}{d}
 +\frac{c^2H\,\delta W}{d^2},
\]
\[
 \delta\widetilde C=
 \frac{d^2}{H}\delta C-\frac{2Cd}{H}(W\delta c+c\delta W)
 -\frac{Cd^2}{H^2}\delta H.
\]

The manufactured curved-history test differentiates the entire scalar-plus-source action with respect to an embedding deformation. It propagates T, J, deltaT and deltaJ, and checks the result against an independent five-point difference of the action. It also tests that freezing the links is detectably wrong.

What is still not proved: uniqueness of this moving discretization, unrestricted finite moving-coordinate covariance, or a well-posed coupled curved-history evolution. At nonzero c the links couple different times; simply feeding this action to the old instantaneous flat ODE would not be legitimate.

### Zero-shift matter current: vary first, then set beta=0

The first curved canonical-current ingredient can be written explicitly; it is not legitimate to discard the shift dependence before variation.

At beta=0, keep arbitrary source motion and set

\[
 C_{0i}=R_i^2N_iU_i/H,\quad
 A_f=\sum_iB_{fi}\psi_i,\quad D_f=\sum_iS_{fi}C_{0i}.
\]

For a smooth physical shift variation, evaluated on the material map,

\[
 \Theta_{fi}:=\delta T_{fi}
 =\int_{\xi_f}^{\xi_i}\frac{H}{N^2U^2}\delta\beta\,d\xi,\quad
 \delta J_{fi}=\partial_t\Theta_{fi}.
\]

The local coefficient derivative is
\(\delta\widetilde C_i=-2R_i^2W_i\delta\beta_i/(HN_iU_i)\).
The nodal kinetic term has zero first beta derivative at beta=0, but the linked spatial action does **not**. Integrating deltaJ by parts in time gives

\[
 K_{fi}=
 \frac{A_f\dot A_fS_{fi}C_{0i}
       -A_fD_fB_{fi}\dot\psi_i}{\delta\xi},
\]
\[
 \delta_\beta I_{\rm scalar}
 =\int dt\left[
 \sum_{fi}K_{fi}\Theta_{fi}
 +\sum_{fi}\frac{A_f^2S_{fi}R_i^2W_i}
                  {\delta\xi HN_iU_i}\delta\beta_i
 \right]+[\mathcal B_\beta]_{t_-}^{t_+},
\]
\[
 \mathcal B_\beta=
 -\sum_{fi}\frac{A_f^2S_{fi}C_{0i}\Theta_{fi}}{2\delta\xi}.
\]

The first term is an oriented cross-factor current, the second a necessary moving-node contribution. The source itself adds
\(\int dt\,SV\,\delta\beta_b/(U_b^2\ell_b)\) per layer. Positive collar quadrature weights multiply all these terms.

In the continuum limit, direct differentiation of the scalar density gives

\[
 \left.\partial_\beta L_{\rm scalar}\right|_0
 =-\frac{R^2}{NU}\psi_\xi
       \left(\psi_t-\frac WH\psi_\xi\right),
\]

not the result of simply setting beta=0 in the action before varying. For histories with compact temporal variations the endpoint term vanishes; in the manufactured finite-time test it is retained and independently checked.

The current must be inserted into the **actual inherited canonical variables**, not treated as an independent equation saying matter current=0. The parent chart uses \(\beta=\kappa NU^3P\). At P=0, holding the other canonical fields fixed,

\[
 \delta\beta=\kappa NU^3\delta P,\qquad
 G_P^{(R)}=\kappa NU^3 G_\beta^{(R)}
          =\kappa NU^3G_\beta^{(\xi)}/H .
\]

Here the superscript states the integration measure. The old canonical equation is
\(\mu_t=(H_{\rm gravity})_P-G_P^{(R)}\), as recorded in the sourced 2026-09-12 scalar-action derivation. Thus this is a source for the canonical mass evolution (and its Einstein flux consistency), not permission to invent a separate shift variable or enforce a vanishing scalar flux.

For the already qualified **conditional continuum** polar Einstein-scalar equations, the derived bulk current has exactly the inherited sign and normalization,

\[
 \mu_t=\kappa R^2F\,\chi_t\chi_R,\qquad
 \mu_R=\frac{\kappa R^2}{2}
       \left(F\chi_R^2+\frac{\chi_t^2}{N^2}\right),\quad F=U^2 .
\]

Combining these with the moving Dirichlet trace, rather than replacing a partial derivative by a boundary derivative, yields

\[
 \frac{d\mu(b(t),t)}{dt}=\mu_t+V\mu_R
 =-\kappa b^2V\Pi,\qquad
 \Pi=\frac12\left(F-\frac{V^2}{N^2}\right)\chi_R^2 .
\]

Since \(db/d\tau=V/\ell\), this is precisely
\(d\mu_-/d\tau=-\kappa b^2\Pi\,db/d\tau\), the moving GR control's mass-work law. The lapse/radial constraint used in this reduction is the already conditional continuum one: it has not yet been solved for the new finite moving system. Neither this algebraic match nor the current identity supplies a coupled finite-collar GR evolution, a thin-shell matching theorem, or the source material's uniqueness.



## 5. Explicit flat finite-collar dynamics

For each layer retain the natural inner endpoint and \(\psi_{\rm outer}=0\). Define free nodal coordinates q and canonical momenta pi, and

\[
 R_i=a+H\xi_i,\quad M_i=H\omega_iR_i^2,\quad
 T=\mathrm{diag}(\xi)\mathrm{diag}(\omega)^{-1}S_0^TB_0/H,
\]
\[
 U_h=\tfrac12\sum_f d_f(B_fq)^2,\quad
 d_f=\frac{(SR^2)_f}{H\delta\xi}.
\]

Here \(B_0,S_0\) are only the old base factors. The positive-pairing derivative lift is a declared interpolation rule; the Gram factors are fully retained in the potential, not reinterpreted as a first derivative.

The endpoint is constrained in material coordinates, but its **Eulerian** scalar time derivative need not vanish. Keeping its half-cell yields

\[
 a_h=M_{\rm outer}(T_{\rm outer}q)^2,\qquad
 L_h=\tfrac12(\dot q-VTq)^TM(\dot q-VTq)
 +\tfrac12a_hV^2-U_h-S\sqrt{1-V^2}.
\]

Omitting this endpoint kinetic term breaks the tested action-energy identity. Let \(r=M^{-1}\pi\), \(F=\nabla_qU_h\), and subscripts b,q denote partial derivatives. The exact equations implemented are

\[
 \dot q=r+VTq,\qquad
 \dot\pi=-F-VT^T\pi+\tfrac12V^2a_{h,q},\qquad \dot b=V,
\]
\[
 (S\gamma^3+a_h)\dot V=
 \tfrac12r^TM_br-U_{h,b}-F^TTq+\pi^TTr
 -V a_{h,q}^Tr-\tfrac12V^2(a_{h,b}+a_{h,q}^TTq).
\]

The source canonical momentum includes scalar transport,

\[
 p_b=S\gamma V+a_hV-\pi^TTq,
\]

and the exact autonomous energy is

\[
 {\cal E}_h=\tfrac12\pi^TM^{-1}\pi+U_h+S\gamma+\tfrac12a_hV^2.
\]

All layer energies/actions are averaged with positive normalized collar weights. The displayed pi and p_b are momenta **per layer weight**: the actual canonical momenta for the quadrature-summed action are w_z*pi and w_z*p_b. Dividing each layer's Euler-Lagrange equations by its positive constant weight gives the equations above; an unweighted canonical bracket with the summed Hamiltonian would be incorrect. The source acceleration denominator stays positive for a timelike source and S>0. Energy conservation alone does not establish continuum accuracy.

### Continuum recoil and work, derived by shape variation

At the moving reflecting trace \(\chi_t+V\chi_R=0\), integration by parts over the moving domain and variation of its upper endpoint give

\[
 \frac{d(S\gamma V)}{dt}=b^2\Pi,\qquad
 \Pi=\tfrac12(1-V^2)\chi_R^2,\qquad
 \dot E_{\rm field}=-Vb^2\Pi,\quad \dot E_{\rm source}=Vb^2\Pi .
\]

The time-boundary part of the moving-domain integration by parts is essential. In detail the scalar endpoint coefficient is
\(b^2[\chi_R^2/2+V\chi_t\chi_R+\chi_t^2/2]\), which reduces to \(b^2\Pi\), not just a static-wall stress inserted into a moving equation.

## 5a. Conditional action consistency, including the full Gram contribution

There is a useful analytical result beyond the numerical energy check. It is **consistency of the action and its first variation on smooth test histories**, not existence or convergence of its dynamical solutions.

Fix a regular material chart with H bounded above/below, d bounded away from zero, uniformly bounded time-link Jacobians, and the needed history/embedding derivatives. For a factor's transported history \(g(\xi)=\psi(T(\xi),\xi)\),

\[
 \Delta_{\delta\xi}^3g(x)=
 \int_{[0,\delta\xi]^3}g'''(x+s_1+s_2+s_3)\,d^3s,
 \quad |\Delta^3g|\le\delta\xi^3\|g'''\|_\infty .
\]

Every inherited Gram row is a bounded positive square of a third difference or a signed sum of two such differences. No special treatment of endpoint rows is needed. Let \(c_f\) be sqrt(margin) for a single row, and \(2\sqrt{|w_f|}\) for a two-difference row. From the actual inherited rational coefficients, margins and absolute coupling weights are below1. With n nodes there are n-3 single rows, n-4 adjacent rows, and two extra rows, hence

\[
 \delta\xi\sum_fc_f^2
 <\frac{(n-3)+4(n-4)+8}{n-1}<5 .
\]

The sampling weights are nonnegative and sum to1. If \(D_{\max}\) bounds all sampled \(J\widetilde C\), M3 bounds the transported third derivatives, and T0 is the anchor-time interval length,

\[
 |I_{\rm Gram}|
 \le\frac{5T_0D_{\max}M_3^2}{2}\delta\xi^4 .
\]

For a smooth deformation with corresponding bounds deltaM3 and deltaD,

\[
 |\delta I_{\rm Gram}|
 \le\frac{5T_0}{2}
 (2D_{\max}M_3\delta M_3+\delta D\,M_3^2)\delta\xi^4 .
\]

The complete base factors use symmetric material endpoints, so their central difference and coefficient sampling give second-order spatial quadrature consistency. The nodal kinetic lift is second order in the interior and first order at endpoints; endpoint quadrature weights are O(delta-xi), leaving an O(delta-xi squared) action defect for smooth histories. The same argument applies to a smooth first variation with uniform mixed-derivative bounds. The proper-time source term is not replaced by an approximate static energy.

Thus, in this declared family and on such histories,

\[
 I_h^{\rm reference}-I_{\rm continuum}=O(\delta\xi^2),\qquad
 I_h^{\rm MTS}-I_h^{\rm reference}=O(\delta\xi^4),
\]

and the same orders hold for the tested class of first variations. The constants need not remain bounded near loss of transversality, high-frequency growth or singular geometry. This neither proves uniform moving-source stability nor licenses transferring the old fixed-boundary convergence theorem. It also does not prove convergence of an arbitrary collar quadrature or all physical MTS sectors.


### Exact flat collar-width law, without a rigid-layer assumption

Use null coordinates u=t-b, v=t+b and \(D=\sqrt{(1+V)/(1-V)}\). For this common incident pulse and equal positive S, all initial source radii \(b_0>5.8\) lie outside its support. Therefore \(D(u)\) is universal across the exact layers, and

\[
 v(u;b_0)=u+2b_0+I(u),\qquad I'(u)=D(u)^2-1,
\]
\[
 t=u+b_0+\tfrac12 I(u),\qquad b=b_0+\tfrac12 I(u).
\]

Differentiating at fixed laboratory time, rather than fixed retarded time, gives

\[
 \left.\frac{\partial u}{\partial b_0}\right|_t=-\frac{2}{1+D^2},
 \qquad
 \left.\frac{\partial b}{\partial b_0}\right|_t
 =\frac{2}{1+D^2}=1-V>0 .
\]

Thus exact flat layers **remain ordered and contract rather than remaining rigid**. For any two initial radii and a uniform speed bound \(V\le V_{\max}<1\),

\[
 (1-V_{\max})\Delta b_0\le\Delta b(t)\le\Delta b_0 .
\]

After the whole pulse is reflected, D and V are constant and common to all layers, so the width is exactly \((1-V_{\rm final})\Delta b_0\). This derives a width rule for this particular flat unforced reflecting family. It is not a theorem for arbitrary matter, gravitational coupling, repeated reflections, or unqualified coarse regulator solutions.


## 6. Test setup and results

Use the inherited compact outgoing function f, initially \(\chi=f(-R)/R\). The independent flat mirror target obeys

\[
 D_u=2f'(u)^2/S,\quad v_u=D^2,\quad
 t=(v+u)/2,\quad b=(v-u)/2,\quad
 V=(D^2-1)/(D^2+1),
\]
\[
 g(v(u))=-f(u),\quad
 g'(v(u))=-f'(u)/D^2,\quad
 \chi(t,R)=[f(t-R)+g(t+R)]/R .
\]

Each layer starts at its own actual \(b_0=6+\epsilon z\), with \(\epsilon=h_{\rm initial}/2\), not an incorrectly copied central-layer target. No target enters the numerical action RHS. Run to lab time1.1; the first inner return is later than3.18 even on the coarsest grid.

Both branches use identical preparation, three-point Gauss/beta22 collar weights, mass, time integrator, step rule and gates. The physical waveform norm is the R-squared weighted error in \(\chi_t,\chi_R\), using the same nodal derivative for both branches, including the moving endpoint's Eulerian time derivative. Its target is evaluated at actual numerical positions. The source errors are separately recorded. Reported maxima are over45 saved times, not continuous-time rigorous bounds. Only one amplitude/weak-field flat preparation is tested here.

**Both branches pass the original flat accuracy gates at8193 nodes per layer.** All9 grids33/65/129/257/513/1025/2049/4097/8193 are retained for each branch, together with two independent half-step controls.

| Nodes per layer | Reference waveform error | MTS waveform error |
|---:|---:|---:|
| 513 | 13.17211% | 12.81943% |
| 1025 | 5.668931% | 5.528751% |
| 2049 | 1.908116% | 1.879194% |
| 4097 | 0.5393484% | 0.5356768% |
| 8193 | 0.1394950% | 0.1391713% |

The first attempt failed at513; the second failed at4097, even though the latter missed the0.5% waveform gate only narrowly. Both are preserved. The third attempt refines to8193 without changing the action, source parameters, preparation, diagnostic norms or gates.

At8193, reference/MTS respectively:

- Maximum source-position absolute error: 1.131118035e-6 / 1.130312950e-6.
- Maximum source-velocity absolute error: 9.664975704e-6 / 9.662879520e-6.
- Maximum relative autonomous energy drift: 2.596360930e-15 / 5.192721859e-15.
- Central final source radius: 6.2707069408334 / 6.2707069416383.
- Central final coordinate speed: 0.47332458639513 / 0.47332458629705.
- Maximum endpoint kinetic inertia divided by S: 0.00106109229 / 0.00106109905; this finite-grid contribution decreases under refinement.
- Every sampled layer ordering remains positive. This is measured regulator behaviour, not a replacement for a general moving-collar stability proof.

Independent source integration in laboratory time agrees with the null-coordinate target to1.11e-12; the earlier independently implemented flat wave target agrees to2.74e-13. Halving the numerical time step at257 changes the full saved state by1.51e-14 /2.94e-14. Thus the coarse failures here are spatial under-resolution, not repaired by relabelling a conservation check or fitting a new source force.

For the8193 runs, the constructor uses sparse factors to avoid multi-gigabyte dense matrices. A16-check audit verifies the same factor/sampling entries and unchanged action RHS/energy;8193 factor storage is below5MB. The evolution, diagnostics and gates are inherited unchanged. The two retained SciPy FutureWarnings concern conversion of integer difference stencils to floating point, not an overflow or changed equation. Current coefficients agree with the old construction; future library upgrades must repeat this equivalence check rather than assume their defaults.

The smooth-history action consistency test independently reproduces second-order base action/variation errors and fourth-order Gram differences. The full curved-history embedding variation agrees with an independent action difference to1.54e-14. The zero-shift current's explicit time-integrated adjoint agrees with tangent transport to5.43e-19, and with an independent full-action difference to1.49e-14; its endpoint and direct moving-node terms are nonzero.

109 successful mathematical, numerical and implementation checks are recorded across eight completed evidence packs. The two failed refinement attempts remain separate records. **This qualifies one flat moving-source control and two manufactured curved-variation controls, not full GR, unrestricted stability, physical material selection or observational agreement.**


Original acceptance gates, declared before runs: maximum sampled waveform error<0.5%, source position and velocity absolute errors<0.001, relative autonomous energy drift<1e-8. Coarse failed data remain preserved; the waveform gate is not replaced by energy conservation.

## 7. Evidence and next calculation

Source ancestry:

- `DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md`
- `DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md`
- `DERIVATION-20260914-action-consistent-moving-source.md`
- `DERIVATION-20260914-coupled-moving-source-GR-control.md`
- `scripts/annular_covariant_scalar_action_20260912.py`
- `scripts/annular_compatible_h_evolution_20260914.py`

New derivations/implementation:

- `scripts/annular_moving_collar_action_20260914.py`
- `scripts/derive_annular_moving_collar_action_20260914.py`
- `scripts/derive_annular_moving_link_clock_20260914.py`
- `scripts/derive_annular_moving_material_pullback_20260914.py`
- `scripts/verify_annular_moving_curved_factor_variation_20260914.py`
- `scripts/run_annular_moving_collar_flat_20260914.py`
- `scripts/run_annular_moving_collar_flat_v2_20260914.py`
- `scripts/run_annular_moving_collar_flat_v3_20260914.py`
- `scripts/annular_moving_collar_sparse_20260914.py`
- `scripts/verify_annular_moving_collar_sparse_20260914.py`
- `scripts/verify_annular_moving_action_consistency_20260914.py`
- `scripts/derive_annular_moving_zero_shift_current_20260914.py`
- `source-intake/navier-stokes/20260914/annular-moving-collar-variation-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-link-clock-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-material-pullback-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-curved-factor-variation-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-zero-shift-current-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-action-consistency-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-collar-sparse-equivalence-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-collar-flat-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-collar-flat-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-moving-collar-flat-attempt03/status.json`

NEXT: assemble the derived zero-shift scalar/source current with the inherited canonical mass equation; obtain the remaining lapse/radial-metric and embedding equations of the curved moving-factor action **with all link and coefficient variations retained**. Check the source stress against the previously qualified moving GR shell law, then attempt a short coupled curved reference/MTS evolution. Do not set the shift to zero before varying the parent momentum. Keep the continuum shell control independent and retain the flat exact target as a regression gate.

This checkpoint does not supply an unrestricted GR limit, parent-selected source microphysics, a black-hole regularity theorem, or a new empirical result. Its concrete advance is the action-derived moving-source construction, rather than another unexplained force prescription.
