# Forecast and readout are separate calculations

Let primes denote conformal-time derivatives, \(m\) the retained heavy mass, \(k\) an individual input wavenumber, \(b\) the homogeneous wave and \(v=b'\). In the units of the native Einstein equations the resolved-wave background satisfies \(v'=-2{\cal H}v-a^2m^2 b\). Its synchronous perturbation satisfies
\[
  \delta b''+2{\cal H}\delta b'+(k^2+a^2m^2)\delta b=-kz\,v .
\]
Its density perturbation, current and enthalpy are \(d_w=v\delta b'+a^2m^2 b\delta b,\ q_w=kv\delta b,\ W_w=v^2\). The background acceleration source \(\rho_w+3p_w\) in the same scaled units is \(2v^2-a^2m^2b^2\). These paired oscillations, not a chosen decay time, determine the predicted change in the flux.

On the averaged branch let \(r=\rho_{\rm match}/a,\ q_f=ru,\ d_f=rD\). With \(s=k^2/(am)^2,\ c_s^2=s/(\sqrt{1+s}+1)^2\),
\[
  P=c_s^2(D+3{\cal H}u/k),\qquad D'=-3{\cal H}P-ku-kz,\qquad u'=-{\cal H}u+kP .
\]
The initial \(D,u\) are the nonoscillating coefficients of the one-sided wave histories \(d_w/r,q_w/r\), evaluated at entry. This is a local approximation to the averaged state, not use of the saved centered projection. The given switch and normalization are common inputs, not quantities inferred here.

Subtract the resolved heavy contributions from the stored total current, density perturbation, background enthalpy and background acceleration source **before** estimating the local continuation. Use time-polynomial powers 0–4 for the smooth term and powers 0–2 multiplying \(\sin(2\theta),\cos(2\theta),\sin(4\theta),\cos(4\theta)\) for the nuisance oscillations. Extrapolate only the smooth term. Neither window nor order is optimized on the scoring data. This is a finite-time surrounding-source approximation, not independent evolution equations for every species.

At each step use \(a'=a{\cal H},\ {\cal H}'=-(\rho+3p)/6,\ (k\eta_{\rm sync})'=q_{\rm tot}/2,\ kz=(d_{\rm tot}/2+k(k\eta_{\rm sync}))/{\cal H}\) with the appropriate branch totals. The matched shear is \(\sigma_f=z_f+3q_{{\rm tot},f}/(2k^2)\). Start the wave from the last pre-switch native sample; carry its background scale, expansion and synchronous curvature to the matched initialization. Propagate both branches forward from their own initial data, not from saved post-switch samples.

The matched first-order flux and its heavy change are
\[
 F_f=-[q_{{\rm tot},f}+(W_{\rm rest}+r)\sigma_f]/(2k),\qquad
 \Delta F=-[q_w-q_f+(v^2-r)\sigma_f]/(2k).
\]
The output-mode source correction is exactly
\[
 \Delta U_{\rm pair}=\tfrac32\{\mathcal C(F_f,\Delta F)+\mathcal C(\Delta F,F_f)+\mathcal C(\Delta F,\Delta F)\}.
\]
Use the original ordered mode pairs and phases; the complex amplitudes are not adjusted after prediction. Audit the pair against both the stored heavy-only reconstruction and the difference of the independently constructed native squared fluxes. The latter includes small nonheavy differences omitted by construction here. Errors are peak-relative complex errors, not relative errors at zero crossings. The source value score uses knots within each window; the rate score uses the inherited quintic interpolant on the padded bank, including neighboring evaluation knots. The predictor never reads the post-entry target, even for the padding.

For downstream tests replace just this one geometric source in the previously checked matched calculation. The original 77-bin scattering, companion stress history, cold baseline, visibility measure and gravity-step refinements remain fixed. Thus the **geometric correction** is forward predicted; the entire experiment is not an independent forecast of the companion stress or of a cosmological observable.
