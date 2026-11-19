# Rest-frame collision-energy bridge — 2026-11-17

## Physical result

For a paired collision four-force, h_b=E_b-v_b.F_b and h_gamma=-E_b+v_gamma.F_b imply h_b+h_gamma=J.(v_b-v_gamma)=D. In the cold-baryon elastic Thomson limit h_b=0, h_gamma=D: relative-flow dissipation enters photon rest energy; baryon lab energy changes through bulk work. No fitted sharing fraction. Thermal/recoil/emission contributions require their independent microscopic energy moment. DERIVATION.md specifies frame, order, normalization and overlap subtraction.

Reused7855 saved samples for baseline/MTS32/64, without physical reintegration. Stable fractional source includes the changed photon-density denominator. Parent endpoint coherent-minus-original source=-2.0412575955843487e-15 Mpc^-1: reduced positive dissipation, not negative total dissipation. Parent source32/64 uncertainty4.470933239458175e-7 and approximation4.6861573106142217e-7 pass unchanged2e-5. Tiny baseline source remains unresolved at1.97549%.

## Accumulation needs more accuracy

Parent collision-only integral over92.48010938639696..102.71763002905956Mpc=-1.2214168335938398e-14, in stored-mode fractional energy, NOT a sky-averaged spectrum. Combined32/64 and stride1/2/4 quadrature allowance1.036004689242732e-18 gives relative8.481991247774442e-5, FAILING unchanged2e-5. Approximation behaves similarly; baseline accumulation remains unresolved at1.53037%. Stride differences are not monotone; no fitted extrapolation or cumulative prediction promotion.

## Microscopic checks

Retained rays0/11/38 supply24 emission/absorption event cases with paired four-momentum and rest-energy projection invariant under an observer boost. Use their original warm temperature and no new weights.183 technical/representation checks pass in verification-v2.json. Radial orders18/26 each check9216 scalar photon/gas pairs for baseline/MTS; largest mismatch1.3227000814676406e-15 versus1e-10.

This is representation compatibility, not full source completion:39/128 directions, x14/event0; cached theta5.9525185110453025e-5 is25.90..36.99 times the late native temperature range. Do not transplant those cached values or infer all spectral/gas coordinates from integrated moments.

## Preserved implementation errors

Original serializer failed on a numpy boolean after six numerical histories had saved. result.json remains partial. complete_energy.py recomputed only cheap readouts, checked exact equality with all six saved histories and wrote result-complete.json; its later console print failed on the same type AFTER saving. No physical evolution rerun.

Initial checks mistook low residual limbs, then rawsum/corr audit accumulators, for independent physical sources. Original producer explicitly defines finite+finite_low, logarithm and total+total_low. verify_energy_v2.py uses those representations with compensated sums. Earlier failures remain in result-complete.json and verification.json. verification-v2.json supersedes ONLY the microscopic packet checks; thresholds and numerical arrays unchanged.

## Handover

Physical restart remains ../mts-carried-defect-budget-20261117/epoch4252 COMPLETE states/work/predictor, not this readout.102 consumed inputs unchanged. Quantum measure separate. No GitHub, galaxy-files, formalization-workbench, bank or scheduler edits.

Martin paused to switch models. Save and stop, no automatic new stage. Next localize the source-integral quadrature error using saved intervals/dense output and unchanged tolerances; then derive/evaluate or bound the late non-elastic energy moment with genuinely matched spectral/gas inputs and overlap subtraction.
