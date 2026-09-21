# Action-consistent moving source: recoil, stress and clock matching

Date: 2026-09-14. Private continuation of the annular restricted-GR-limit programme.

## Result in plain language

The old reflecting shell was forced to remain still. Under the tested impact, the stress required to do that violated its proposed classical energy condition. That is a real failure of that particular rigid, low-energy source model; it is not a proof that every dynamical source fails.

Here we construct a **conditional covariant dynamical completion**. A surface-fluid action supplies stress, an explicit ideal-reflection coupling supplies the scalar reaction, and the junction equations supply acceleration. There is no prescribed mechanical force history. The held-shell formula is recovered when acceleration is set to zero. A freely moving shell instead acquires kinetic energy.

Two distinct controls now work:

- A self-gravitating, vacuum-interior/exterior source has an explicit causal material example with a radially stable quiet equilibrium.
- A flat-space spherical scalar pulse and freely recoiling dust shell have an exact nonlinear characteristic solution. Three independent numerical checks agree: time-domain shell evolution, null-coordinate reconstruction, and a direct integral of the reconstructed bulk scalar energy.

This is **not** a derivation of the source material or perfect reflectivity from the MTS parent action. Nor have we yet evolved the moving source coupled to the curved-space scalar PDE or transferred this boundary action to the finite-collar MTS regulator.

## 1. Local dependencies and what stays unchanged

Read the previous source failure and the restricted limit before interpreting this result:

- `DERIVATION-20260914-active-source-reflection-and-support-law.md`
- `DERIVATION-20260914-independent-continuum-GR-comparison.md`
- `DERIVATION-20260914-layer-locking-and-restricted-evolving-GR-limit.md`
- `source-intake/navier-stokes/20260914/annular-source-collision-final-integrity.json`

The existing rigid-source trajectories and their failed energy-condition result remain immutable. Nothing here re-labels them as a physical pass. The new flat pulse is declared control data, not a refit or replay of the old curved-space pulse.

The classical variational-fluid method is established background, not an MTS novelty: [Brown, 1993](https://arxiv.org/abs/gr-qc/9304026). The geometrical shell junction framework is likewise established: [Israel, 1966](https://doi.org/10.1007/BF02710419), with an accessible computational treatment by [Musgrave and Lake, 1995/1996](https://arxiv.org/abs/gr-qc/9510052v3). The calculation below specializes these ingredients to the conventions and source problem in this workspace.

## 2. Conventions and declared candidate action

Set \(c=1\), \(\kappa=4\pi G\), metric signature \((-+++)\). The shell history is \(\mathcal S\), with induced metric \(h_{ab}\), proper time \(\tau\), areal radius \(b(\tau)\), and outward normal from the minus/interior side to the plus/exterior side.

Let \(\sigma\) and \(P\) be surface energy density and isotropic tangential pressure. Define \(S=b^2\sigma\); its actual rest energy is \(4\pi S\). It is not entropy. The geometric mass \(m\) has length units. The numerical examples use the inherited pilot normalization, not SI observational calibration.

Use the candidate action

\[
 I={1\over4\kappa}\sum_{\pm}\int_{\Omega_\pm}\sqrt{-g}\,R
 +I_{\rm GHY}
 -{1\over2}\int_{\Omega_-}\sqrt{-g}\,\nabla_\mu\chi\nabla^\mu\chi
 -\int_{\mathcal S}\sqrt{-h}\,\rho(n)
 +\int_{\mathcal S}\sqrt{-h}\,\lambda\chi|_{\mathcal S}.
\]

The GHY terms use each domain's outward boundary orientation; fixed external boundary data and end-time variations are understood. The exterior is vacuum. The scalar is a canonical massless **scalar**, not a demonstrated electromagnetic or gravitational-wave sector. \(\lambda\) is a surface multiplier, not a wavelength or cosmological constant.

The surface number current is conserved, with no particle creation. One local realization in terms of material labels \(z^1,z^2\) is

\[
 \widetilde J^a=\eta(z)\epsilon^{abc}\partial_b z^1\partial_c z^2,\qquad
 \partial_a\widetilde J^a=0,\qquad
 n={\sqrt{-h_{ab}\widetilde J^a\widetilde J^b}\over\sqrt{-h}}.
\]

This fixes the meaning of variation at conserved current. It does **not** fix \(\rho(n)\) microscopically.

Assumptions, not results:

1. Einstein bulk in the already identified restricted continuum sector.
2. A timelike infinitesimally thin, isotropic, isentropic surface fluid.
3. The chosen material energy function \(\rho(n)\).
4. Ideal comoving Dirichlet reflection, imposed by a stated action term.
5. A regular outward-normal chart with \(S>0,F_\pm>0,\beta_+>0\).

This chart does not cover a horizon, a null shell, a wormhole branch, or arbitrary topology. No claim about those follows from the tests.

## 3. Derive the stress and reflection force before reducing

Write \(v^a\) for the unit material velocity. At fixed current density,

\[
 \delta n=-{n\over2}(h^{ab}+v^av^b)\delta h_{ab}.
\]

Varying the material action therefore gives

\[
 S^{ab}=(\sigma+P)v^av^b+P h^{ab},\qquad
 \sigma=\rho(n),\qquad P=n\rho_n-\rho.
\]

For a spherical conserved population, \(n\propto b^{-2}\). Consequently,

\[
 {dS\over db}=-2bP,\qquad \dot S=-2bP\dot b.
\]

Pressure is no longer an independently prescribed time series.

Let \(\eta_\chi=n^\mu\nabla_\mu\chi\). The scalar boundary variation is
\(-\eta_\chi\delta\chi+\lambda\delta\chi\); the multiplier variation gives \(\chi|_{\mathcal S}=0\). Hence \(\lambda=\eta_\chi\).

For a normal displacement \(\xi\), the interior scalar domain contributes
\(-\eta_\chi^2\xi/2\), while the multiplier contributes \(+\lambda\eta_\chi\xi\). Their on-shell sum is

\[
 +\Pi\xi,\qquad \Pi={1\over2}\eta_\chi^2.
\]

The factor \(1/2\) matters. Substituting the boundary condition into the action *before* varying its position would wrongly discard the reaction. The ideal multiplier describes perfect reflection; it does not explain which MTS constituents realize a reflector or its frequency range.

The normal shape equation is consistent with

\[
 S^{ab}\overline K_{ab}=[T_{nn}]=-\Pi,
\]

where brackets mean plus minus minus, and the bar is the average of the two extrinsic curvatures. Below we verify it independently against the temporal junction equation.

## 4. Moving scalar trace and bulk work

Put

\[
 ds_-^2=-N_-^2dt_-^2+{dR^2\over F_-}+R^2d\Omega^2,\quad
 F_-=1-{2m_-\over b},\quad L_-=N_-\sqrt{F_-}.
\]

All boundary quantities in this section are evaluated at \(R=b\). Let

\[
 w=\dot b,\quad \beta_\pm=\sqrt{F_\pm+w^2},\quad
 {dt_-\over d\tau}={\beta_-\over L_-}.
\]

In the \((t_-,R)\) chart, \(v^\mu=(\beta_-/L_-,w)\) and
\(n^\mu=(w/L_-,\beta_-)\). The prior bulk canonical convention is
\(\chi_{t_-}=L_-p/R^2\).

The comoving boundary condition and its consequences are

\[
 \chi_{t_-}+{L_-w\over\beta_-}\chi_R=0,\qquad
 p_b=-{b^2w\over\beta_-}\chi_R,
\]
\[
 \eta_\chi={F_-\over\beta_-}\chi_R,\qquad
 \Pi={F_-^2\chi_R^2\over2\beta_-^2},\qquad T_{vn}=0.
\]

Thus fixed-wall \(p_b=0\) cannot simply be carried to a moving wall. Zero rest-frame absorption does not mean zero mechanical work.

The bulk Einstein-scalar identities in the inherited convention are

\[
 e={1\over2}\left(R^2\chi_R^2+{p^2\over R^2}\right),\quad
 m_R=\kappa F e,\quad m_t=\kappa F Lp\chi_R.
\]

Taking the derivative along the moving boundary, rather than at fixed radius, gives

\[
 \boxed{\dot m_-=-\kappa b^2\Pi w},\qquad
 \boxed{\dot S=-2bPw}.
\]

The scalar loses geometric energy as it drives an outward moving shell.

## 5. Derive acceleration from the junction equations

With the chosen normal orientation,

\[
 [K_{ab}]-h_{ab}[K]=-2\kappa S_{ab},\quad
 [K^\theta{}_\theta]=-\kappa\sigma,\quad
 [K^\tau{}_\tau]=\kappa(\sigma+2P).
\]

The angular equation implies

\[
 \beta_- -\beta_+={\kappa S\over b},\qquad
 M=m_+=m_-+\kappa S\beta_- -{(\kappa S)^2\over2b}.
\]

For the time-dependent scalar interior, direct curvature calculation gives

\[
 K^\tau{}_{\tau-}={a+m_-/b^2+\kappa b\Pi\over\beta_-},\quad
 K^\tau{}_{\tau+}={a+M/b^2\over\beta_+},\quad
 K^\theta{}_{\theta\pm}={\beta_\pm\over b},\quad a=\dot w.
\]

One way to audit the interior expression is to put \(U=\sqrt F\) and start from

\[
 K^\tau{}_{\tau-}={a\over\beta_-}
 +\beta_-{N_R\over N}
 -{w^2\over\beta_-}{U_R\over U}
 -2w{U_t\over NU^2}.
\]

Substitute
\(N_R/N=m/(b^2F)+\kappa e/b\),
\(U_R/U=m/(b^2F)-\kappa e/b\),
\(U_t/(NU^2)=-\kappa p\chi_R/b\), and the moving scalar trace. The stated \(\kappa b\Pi\) term follows, including the time-dependent metric contribution.

The temporal jump now solves for acceleration:

\[
 \boxed{
 \dot w={b^2\Pi\beta_+\over S}
        +{2bP\beta_-\beta_+\over S}
        -{m_-\over b^2}
        -{\kappa S\beta_-\over2b^2}.}
\]

This equation does **not** divide by \(w\). It remains meaningful at initial rest and at turning points. Differentiating only the mass first integral and cancelling \(w\) would not be a sufficient derivation there.

Together with \(\dot b=w\), the two work laws and a material EOS, this is the local shell response law. The bulk wave must still determine its own evolving \(\Pi\). Substitution verifies \(\dot M=0\) and the mean-curvature normal shape equation identically.

### Required limiting checks

For a held source, \(w=a=0\), \(U_\pm=\sqrt{F_\pm}\), \(p_b=0\):

\[
 P={\sigma\over4}\left({1\over U_-U_+}-1\right)
   -{U_-e_b\over2b}.
\]

This is exactly the old rigid loading law. It is recovered, not erased.

For dust, \(P=0,\Pi=0\), put \(m_-=\kappa\mathcal M\) and take
\(\kappa\to0\) at fixed reduced physical masses \(\mathcal M,S\). Then

\[
 {a\over\kappa}\longrightarrow
 -{\mathcal M+S/2\over b^2}.
\]

This is the central plus half-self-mass Newtonian shell acceleration. It is a weak-gravity check, not a derivation of the numerical value of \(G\).

## 6. A moving clock cannot be copied from the fixed boundary

The shell's proper time gives the correct relation separately on each side:

\[
 {dt_\pm\over d\tau}={\beta_\pm\over N_\pm\sqrt{F_\pm}}.
\]

If one insists on one shared polar coordinate time and velocity \(V=db/dt\), induced-metric matching instead demands

\[
 N_+^2-N_-^2=V^2(F_+^{-1}-F_-^{-1}).
\]

Equal lapses are therefore generally wrong for a moving shell with a jump in \(F\). They are compatible in the static \(V=0\) limit. The old midpoint-clock choice cannot be silently extended to finite motion. A negative numerical control detects the mismatch.

The proper-time law above is covariant within its declared shell model. A corresponding finite-collar MTS time/embedding map remains to be derived.

## 7. Explicit material example and radial quiet stability

Dust follows from \(\rho=m_dn\): \(S\) is constant and \(P=0\). It satisfies ordinary surface energy conditions but does not hold a gravitating shell at rest without another force.

For an example that can support a quiet shell, choose

\[
 \rho(n)=\rho_v+C n^{1+c_s^2},\quad
 P=c_s^2 C n^{1+c_s^2}-\rho_v,
\]

with \(C>0,\rho_v\ge0,0\le c_s^2\le1\). Then
\(dP/d\rho=c_s^2\), \(\rho+P=(1+c_s^2)C n^{1+c_s^2}>0\), and
\(\rho-P=2\rho_v+(1-c_s^2)C n^{1+c_s^2}\ge0\).
These establish the intrinsic sound-speed and dominant-energy inequalities for this material family. They do not prove stability of nonspherical coupled gravity-wave perturbations.

At a declared quiet reference \((b_0,S_0,P_0)\), define

\[
 \sigma_0=S_0/b_0^2,\quad
 \rho_v={c_s^2\sigma_0-P_0\over1+c_s^2},\quad
 \rho_p(b)={\sigma_0+P_0\over1+c_s^2}
          \left({b_0\over b}\right)^{2(1+c_s^2)}.
\]

Then \(S(b)=b^2(\rho_v+\rho_p)\), \(P(b)=c_s^2\rho_p-\rho_v\).
The chosen constants are a material example calibrated to a quiet state, **not** parent-derived predictions.

Let \(A(b)\) be the zero-wave, zero-velocity acceleration along this EOS, with fixed interior Schwarzschild mass. Linear spherical displacement obeys
\(\delta\ddot b=A'(b_0)\delta b\). If \(\omega=P/\sigma\), the exact coefficient is

\[
 {\partial A'(b_0)\over\partial c_s^2}
 =-{4(1+\omega_0)U_-U_+\over b_0^2}.
\]

Thus finite compressibility can stabilize this radial mode; causality alone does not guarantee stability.

Using \(b_0=6,S_0=.003,\kappa=.1\) and
\(m_-=.8043365648636244\) gives:

| Quantity | Result |
|---|---:|
| Quiet pressure \(P_0\) | \(7.63353095425\,10^{-6}\) |
| \(P_0/\sigma_0\) | 0.091602371451 |
| Critical \(c_s^2\) for the radial linear mode | 0.148933847336 |
| Illustrative chosen \(c_s^2\) | 0.5 |
| \(A'(b_0)\) | -0.031162339350 |
| Proper radial frequency \(\sqrt{-A'}\) | 0.176528579413 |

Vacuum control evolutions:

- Unsupported dust falls from radius 6 to 5.95519592789 by \(\tau=2\); no artificial support inserted.
- The causal material remains at its quiet equilibrium through \(\tau=80\).
- Starting instead at radius 6.001 with zero velocity gives bounded radial oscillation over the tested interval, minimum radius 5.99900006282. Half-step/tighter-tolerance state difference is \(2.14\,10^{-14}\).
- Maximum exterior mass drift is \(1.12\,10^{-16}\), a conservation diagnostic rather than total solution accuracy.

Only the old initial **enclosed mass value** is borrowed. The vacuum control deliberately removes the distributed scalar wave; it is not the original pulse propagated in a moving GR geometry.

## 8. Exact self-consistent flat scalar recoil control

For \(G=0\), before a reflected pulse reaches the centre,

\[
 \chi(t,r)={f(u)+g(v)\over r},\qquad u=t-r,\quad v=t+r.
\]

Here \(v\) denotes the advanced null coordinate, not material velocity.
At a dust shell of rapidity \(\zeta\), \(db/dt=\tanh\zeta\). Define \(D=e^\zeta\).
Reflection gives

\[
 g(v_s)=-f(u_s),\qquad
 g'(v_s)=-D^{-2} f'(u_s),\qquad
 \eta_\chi=-{2f'(u_s)\over bD}.
\]

The action-derived shell equation reduces to

\[
 {d\zeta\over d\tau}={2f'(u)^2\over SD^2},\qquad
 {du\over d\tau}=D^{-1},\qquad
 {dD\over du}={2f'(u)^2\over S}.
\]

For initial rest, define \(E_{\rm in}(u)=\int_{u_0}^u f'(s)^2ds\). Then

\[
 D=1+{2E_{\rm in}\over S},\qquad
 E_{\rm ref}={S\over2}(1-D^{-1}),\qquad
 \Delta E_{\rm shell}={S\over2}(D+D^{-1}-2),
\]
\[
 E_{\rm in}=E_{\rm ref}+\Delta E_{\rm shell}.
\]

The trajectory follows from \(dv/du=D^2\), \(t=(u+v)/2\), \(b=(v-u)/2\).
These formulas determine both recoil and the reflected waveform from incoming initial data. Holding the old reflected energy unchanged *while also adding recoil energy* fails the energy balance; the valid fixed-wall problem itself is a different problem, not an erroneous control.

Also \(S\sinh\zeta=E_{\rm in}+E_{\rm ref}\), a **reduced radial null-mode impulse identity**. It must not be called nonzero total Cartesian momentum of a spherically symmetric system.

### Direct bulk energy rather than shell bookkeeping alone

With \(\phi=f+g\), the physical angular-reduced scalar energy density is

\[
 {r^2\over2}(\chi_t^2+\chi_r^2)
 =f'^2+g'^2-\partial_r\!\left({\phi^2\over2r}\right).
\]

Before centre return, the field is quiet at the centre and \(\phi=0\) at the mirror; the integrated boundary term vanishes. Directly integrating the reconstructed \(\chi_t,\chi_r\), rather than inferring energy from the shell, independently checks this statement.

The new compact input is
\(f=A\exp[1-1/(1-x^2)]\) for \(|x|<1\), zero otherwise,
\(x=(u+5.5)/.3\), with initial shell radius 6 and \(S=.003\).
The leading reflected front reaches the centre at \(t=6.2\); all reported evolution ends earlier.

| Amplitude \(A\) | Incident energy | Final speed | Energy fraction to recoil | Pulse-end time |
|---|---:|---:|---:|---:|
| .005 | .000252205147442 | .154170773935 | 14.3936% | .853104723114 |
| .01 | .001008820589766 | .473325748740 | 40.2109% | 1.044383215967 |
| .02 | .004035282359064 | .863177597268 | 72.9011% | 2.288962040031 |

These are dimensionless/reduced **control examples**, not predicted speeds for astronomical matter.

The time-domain shell ODE matches an independent characteristic quadrature trajectory within \(8.27\,10^{-14}\). Its energy ledger residual is below \(1.97\,10^{-17}\). Independent null-coordinate reconstruction plus direct bulk integration over 15 time slices gives maximum total-energy defect \(6.68\,10^{-17}\). These small residuals do not establish an equivalent error bound for an unperformed GR PDE evolution.

## 9. Reproducibility and preserved failures

Executable mathematical core:
`scripts/annular_dynamical_source_20260914.py`.

| Completed validation | Checks | Evidence |
|---|---:|---|
| Symbolic junction/work/material identities | 18 | `source-intake/navier-stokes/20260914/annular-dynamical-source-algebra-attempt02/status.json` |
| Material law, GR shell, clocks and vacuum controls | 28 | `source-intake/navier-stokes/20260914/annular-dynamical-source-numerics-attempt01/status.json` |
| Exact flat recoil and waveform boundary | 37 | `source-intake/navier-stokes/20260914/annular-exact-flat-recoil-attempt02/status.json` |
| Independent reconstructed bulk energy | 37 | `source-intake/navier-stokes/20260914/annular-flat-bulk-energy-attempt01/status.json` |

Total: 120 completed checks. They check the declared equations and examples, not the truth of the entire MTS framework. The action derivation is a paper-level calculation with symbolic identity checks, not machine-certified functional analysis.

Preserved, not overwritten:

- `source-intake/navier-stokes/20260914/annular-dynamical-source-algebra-attempt01/status.json`: curvature audit substituted a pressure-dependent acceleration on one side only. Corrected using an independent acceleration in a new script. An unexecuted pseudo-Newton test was replaced by the genuine fixed-physical-mass weak-gravity limit.
- `source-intake/navier-stokes/20260914/annular-exact-flat-recoil-attempt01/status.json`: a floating-point time-grid endpoint lay outside the integration interval; failure occurred before evolution. The new version uses a closed time grid and deduplicates the terminal event. Physical equations and tolerances were not changed.

Source provenance is recorded in
`source-intake/navier-stokes/20260914/annular-dynamical-source-provenance.json`.

## 10. What is actually closed, and the next implementation

**Closed conditionally in this model:** stress from a surface action; comoving scalar reaction; acceleration regular at turning points; local energy transfer; recovery of the old rigid law; Newtonian dust limit; moving induced-metric clock matching; one causal radially stable quiet material example; exact flat finite-amplitude recoil control.

**Not closed:** parent-selected surface constituents/material coefficients; physical perfect-reflection mechanism; a matched moving finite-collar action; coupled curved-space scalar evolution; nonspherical/global stability; horizons/black holes; unrestricted MTS-to-GR limit; observational viability.

The useful advance is therefore from “required reaction written down” to “an explicit action-consistent source law with independently checked motion and energy transfer.” It is not a declaration that the complete MTS source sector is derived.

Next, implement a **coupled moving-boundary spherical Einstein-scalar control**, validating its moving boundary against the exact flat recoil solution first. Evolve the scalar trace and source together; use proper-time-induced clock matching; verify radial constraints and conserved exterior mass. Only then put the same boundary action into both MTS and reference regulators and compare at equal accuracy criteria.

The original inner annular boundary remains an ideal boundary unless separately replaced; a moving outer shell does not turn that annulus into a centre or a horizon.

