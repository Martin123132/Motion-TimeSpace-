# Forward construction

Use the retained conformal units and the flat synchronous Einstein equations for each input wavenumber \(k\). Write \(e=\mathrm{etak}\), \(H=a'/a\), \(q=\mathrm{dgq}\) and \(d=\mathrm{dgrho}\). The potential in the spatial contraction is **not** the native raw Weyl diagnostic:
\[
 kz=(d/2+ke)/H,\qquad \sigma=z+3q/(2k^2),\qquad
 \Phi=(e-H\sigma)/k=-[d+3Hq/k]/(2k^2).
\]
The last equality follows by substitution. Use the saved homogeneous and perturbed wave equations on branch \(w\) and the projected two-moment equations on the averaged branch \(f\); neither uses the later native histories. Use the identical earlier one-sided nonheavy continuation and mode geometry. For this spatial calculation enforce the flat Hamiltonian constraint at entry:
\(H_f^2=H_w^2+(\rho_{\rm match}/a-\rho_{h,w})/3\), with \(\rho_{h,w}=(v^2+a^2m^2b^2)/2\). This changes the initial expansion by about \(1.008\times10^{-9}\) in inverse conformal Mpc. Keep the already frozen squared-flux contribution exactly, rather than quietly replacing it with a new fit.

The native shear equation is \(\sigma'=e-2H\sigma-\Pi/k\), where \(\Pi\) is the total scaled anisotropic stress. For \(\Delta=w-f\),
\[
 (a_w^2\Delta\sigma)'=a_w^2(\Delta e-2\Delta H\,\sigma_f-\Delta\Pi/k).
\]
Initialize the shear difference from both branch constraints. Evolve it with **\(\Delta\Pi=0\) as a short-window approximation**, not an identity for the photon and neutrino hierarchies. The synchronous curvature evolution \(e'=q/2\) comes from the existing state integrations. Forecast
\[
 d_\Phi=(\Delta e-H_w\Delta\sigma-\Delta H\,\sigma_f)/k,\quad p=\Phi_f .
\]
As distinct controls, constrain both shears algebraically throughout with the shared nonheavy-density continuation, and shorten the causal input window. No later values choose the primary. Repeating the integration of the shear source with twice the resolution changes spatial terms by less than \(2\times10^{-10}\) peak-relative.

For each ordered quadratic operator \(B\), the desired correction is \(B(p,d_\Phi)+B(d_\Phi,p)+B(d_\Phi,d_\Phi)\). Use the native output-mode potential-square, potential–Laplacian and gradient operators with coefficients \(-k_{\rm out}^2,2,-1/2\). Keep the saved lengths, phases and contractions of the 782 input rows. Add the frozen squared-flux correction to obtain the total \(U_w-U_f\) forecast. The later native wave is used only for scoring, not as an input. Reference differences, including their small values, set the normalization; do not report only the absolute branch potentials.

**Independent rate check (after scoring).** For native Weyl potential \(W\), \(\Psi=2W-\Phi\). The momentum constraint gives \(\Phi'=-F-H\Psi\), \(F=-[q+(\rho+p_{\rm bg})\sigma]/(2k)\). Read the native rates at the original knots and apply the bilinear product rule to the *difference* of the two spatial contractions. Compare with symmetric time differences of the unaltered forward solution, halving that differentiation step. Integrate the native equation rates over pairs of cells by Simpson's rule and compare to the archived changes in the source. This check uses neither extrapolation from the far side of the switch nor a replacement reference in the original score. It does not grant a pass to a failed knot-derivative gate.
